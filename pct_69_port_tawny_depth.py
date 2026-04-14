import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Douro Valley (10-Year Tawny Port, Ramos Pinto Quinta dos Bons Aires, Blended Barrel Age)',
    output_dir='.',
    starting_entry=1,
    session_number=73,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Ramos Pinto — Vila Nova de Gaia, Douro Valley',
    'location': 'Vila Nova de Gaia, Porto, Portugal',
    'description': (
        'Ramos Pinto is one of the historic Porto Port shippers, founded in 1880 '
        'by Adriano Ramos Pinto — known as much for its innovative art nouveau '
        'poster advertising of the early 20th century as for its Port quality. '
        'The house owns three Douro Valley quintas including Quinta dos Bons '
        'Aires, Quinta de Ervamoira in the Douro Superior, and Quinta do Bom '
        'Retiro in Cima Corgo. Ramos Pinto is a specialist in both Tawny Port '
        '(particularly the 10 and 20-year age-indicated expressions) and Colheita '
        'single-vintage Tawny Port, with one of the most consistent quality '
        'records in the Vila Nova de Gaia lodges. The Quinta dos Bons Aires '
        '10-year Tawny is the entry benchmark for the Ramos Pinto tawny '
        'programme, and the Ervamoira 10-year (from the Douro Superior quinta) '
        'is the parallel expression showing the hotter, more concentrated '
        'Douro Superior terroir character in the tawny style.'
    ),
    'founded': '1880',
    'region': 'Vila Nova de Gaia, Porto, Portugal',
    'website': 'ramospinto.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Ramos Pinto / Champagne Louis Roederer group distribution',
    'type': 'importer',
    'description': (
        'Ramos Pinto has been owned by Champagne Louis Roederer since 1990 — '
        'the Roederer group using the same philosophy of quality and estate '
        'ownership that defines Roederer Champagne to transform Ramos Pinto '
        'into one of the leading estate-focused Port houses. Ramos Pinto is '
        'distributed in the United States through the Roederer group import '
        'network, available through fine wine retailers nationally. In Canada, '
        'BCLDB BC and LCBO Ontario carry the 10-year and 20-year Tawny '
        'expressions on regular allocation. The Quinta dos Bons Aires 10-year '
        'is widely available in BC specialty wine shops at CAD $35–50 per '
        '750ml, making it one of the most accessible benchmark Tawny Port '
        'expressions in the Canadian market.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Global'],
    'traditions_carried': ['fortified'],
    'website': 'ramospinto.pt',
    'verified': True
})

session.add_beverage({
    'name': (
        'Ramos Pinto 10-Year Tawny Port Quinta dos Bons Aires — '
        'Blended Age-Indicated Tawny, Douro Valley, Vila Nova de Gaia Lodge Aging'
    ),
    'category': 'fortified',
    'subcategory': 'port_tawny',
    'origin': 'Portugal',
    'region': 'Portugal — Douro Valley (10-Year Tawny Port, Ramos Pinto Quinta dos Bons Aires, Blended Barrel Age)',
    'producer': 'Ramos Pinto — Vila Nova de Gaia, Douro Valley',
    'alcohol_content': 19.5,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'Ramos Pinto\'s Quinta dos Bons Aires is located in the Cima Corgo '
        'sub-zone of the Douro Valley DOC — the central and most prestigious '
        'Port wine production zone, centred on the Pinhão tributary valley '
        'at 150–500m elevation above the Douro River. The Cima Corgo schist '
        'terraces at Quinta dos Bons Aires face south and southwest — the '
        'maximum solar radiation exposure on the dark Douro schist, which '
        'retains heat into the night and creates the extreme diurnal '
        'temperature range (35–40°C day; 15–18°C night) that is the '
        'fingerprint of Douro Cima Corgo viticulture. The primary soil '
        'is dark phyllite-schist — the metamorphic rock that fractures '
        'into thin plates allowing vine roots to penetrate to 10–15m '
        'depth, accessing both deep soil moisture reserves and the '
        'mineral-rich schist fracture matrix. This deep root penetration '
        'is the primary factor in Douro Port quality: the vine\'s access '
        'to mineral reserves through deep schist roots versus the shallow '
        'roots of sandy or clay soils creates the characteristic dark, '
        'concentrated, mineral-structured base wines that define premium '
        'Port production. The Cima Corgo microclimate is drier than '
        'the coastal Baixo Corgo (400–500mm rainfall annually, versus '
        '700–900mm for Baixo Corgo) and cooler than the Douro Superior '
        'interior, creating the balance of heat-concentration and '
        'aromatic precision that characterizes the classic Cima Corgo '
        'Tawny style.'
    ),
    'production_technique': (
        'The 10-year age-indicated Tawny Port is a solera-style blend '
        'of multiple vintages with an average age of 10 years in barrel — '
        'the "10-year" designation is a legal average age, not a single '
        'vintage. The base wines for Ramos Pinto 10-year Tawny are produced '
        'from Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca, '
        'and Tinta Amarela harvested from Quinta dos Bons Aires and contracted '
        'Cima Corgo growers in September-October. Foot-treading in granite '
        'lagares at the Quinta begins maceration and extraction; the '
        'winemaker monitors the fermentation closely to determine the '
        'precise moment of fortification (the baumé point) — typically '
        'when 6–8% ABV has been achieved and 80–120 g/L residual sugar '
        'remains. Fortification with 77% ABV aguardente vínica arrests '
        'fermentation and produces the 19–21% ABV base Port. '
        'The young fortified wine enters the tawny-designated aging '
        'pipeline: 550L seasoned oak pipes in the Gaia lodge at 15–18°C '
        'year-round (the Atlantic maritime temperature of Gaia versus '
        'the extreme heat of Douro Valley aging). The deliberate oxidative '
        'aging in small seasoned oak allows controlled evaporation '
        '(approximately 3% annually in Gaia conditions — the "angel\'s '
        'share"), oxidative color transformation (garnet → tawny amber), '
        'and the development of rancio complexity through ester reactions '
        'with dissolved oxygen through the porous oak staves. The blending '
        'team at Ramos Pinto maintains the 10-year average by annually '
        'assessing the solera lots and adding young wine to replace '
        'wine drawn off for bottling — the continuous addition and '
        'drawing-off maintaining the 10-year average age across the '
        'entire solera volume. The 10-year Tawny is lighter, fresher, '
        'and more fruit-retaining than the 20, 30, or 40-year expressions '
        '— the shorter average age preserving more residual primary '
        'red fruit character alongside the emerging dried fruit and '
        'oxidative complexity.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Amontillado Sherry (oxidative barrel aging, tawny development, fortified)',
            'connection': (
                '10-Year Tawny Port and Amontillado Sherry share the oxidative '
                'barrel aging methodology that produces the amber-tawny color '
                'and rancio complexity characteristic of both styles: both are '
                'fortified wines aged under deliberate oxidative conditions (no '
                'flor yeast protection in Amontillado; small seasoned oak pipes '
                'in Tawny) that transform the primary red or white fruit character '
                'into dried fruit, nutty, and caramel oxidative registers. The '
                'critical structural difference is sugar: 10-year Tawny retains '
                '80–100 g/L residual sugar from the arrested fermentation, while '
                'Amontillado is completely dry (0–5 g/L residual sugar); the '
                'sweetness of Tawny and the bone dryness of Amontillado represent '
                'the two primary service contexts for oxidatively aged fortified '
                'wine in professional programme design.'
            )
        },
        {
            'tradition': 'Madeira 10-Year Boal (age-indicated oxidative fortified, blended average)',
            'connection': (
                '10-Year Tawny Port and 10-Year Madeira Boal are direct '
                'structural parallels within the Portuguese fortified tradition: '
                'both are age-indicated expressions (the "10-year" is a legal '
                'average age blended from multiple vintages in both cases), '
                'both undergo oxidative barrel aging in small wood vessels, '
                'and both develop the amber color and dried fruit complexity '
                'characteristic of a decade of controlled oxidation. The '
                'sensory distinction is the Maillard heating component in '
                'Madeira (estufagem — the deliberate heat treatment that '
                'caramelizes sugars and creates the distinctive burnt caramel '
                'and tropical fruit character of Madeira) versus the purely '
                'oxidative aging of Tawny Port without heat treatment.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Tawny amber with orange-gold highlights — the beginning of the '
            'oxidative color transformation; less deeply amber than 20-year '
            'Tawny, retaining some residual orange-garnet from the primary '
            'fruit character not yet fully transformed by 10-year average '
            'barrel oxidation; brilliant clarity from filtration before '
            'bottling; viscous, slow legs from 19–20% ABV and 80–100 g/L '
            'residual sugar.'
        ),
        'nose': (
            'Fresh dried fruit — dried cherry and cranberry — still present '
            'from the 10-year average barrel aging (less oxidative transformation '
            'than 20+ year expressions); alongside the fresh dried fruit, the '
            'beginning of rancio development (light walnut and hazelnut); '
            'orange zest and caramel from the beginning of Maillard browning '
            'at this age; a fresh, lifted quality to the aromatic register '
            'that distinguishes 10-year from more oxidized older expressions; '
            'the Douro schist mineral character still traceable beneath '
            'the dried fruit and oxidative complexity.'
        ),
        'palate': (
            'Medium-sweet with bright acidity; the dried cherry and cranberry '
            'from the nose carrying through the entry; caramel and light '
            'rancio building through the mid-palate; medium finish with '
            'clean sweetness and the beginning of the oxidative complexity '
            'that reaches full expression in the 20-year; the 10-year is '
            'the most food-versatile Tawny tier — the residual primary '
            'fruit character and lighter oxidative complexity making it '
            'more demanding with dessert contexts than the fully '
            'oxidized 20-year and 30-year expressions.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Generic Tawny Port (no age statement, commercial grade)',
            'criteria': (
                'Tawny Port without an age statement — typically young Ruby '
                'Port blended with small amounts of aged wine to achieve a '
                'tawny color through minimal oxidation or through blending '
                'rather than genuine extended barrel aging; lacks the dried '
                'fruit and rancio complexity of age-indicated Tawny; the '
                'color is achieved through blending rather than through '
                'genuine oxidative transformation in barrel.'
            )
        },
        {
            'tier': 2,
            'tier_name': '10-Year Age-Indicated Tawny (Ramos Pinto Quinta dos Bons Aires)',
            'criteria': (
                'Minimum 10-year average barrel aging with genuine oxidative '
                'transformation; dried fruit character replacing primary red '
                'fruit; the beginning of rancio development; the benchmark '
                'commercial tier for genuine age-indicated Tawny; Ramos Pinto '
                'Quinta dos Bons Aires is the reference expression for the '
                '10-year style at consistent quality, available widely '
                'in North American specialty retail.'
            )
        },
        {
            'tier': 3,
            'tier_name': '20-Year Age-Indicated Tawny (Niepoort, Ramos Pinto, Quinta do Crasto)',
            'criteria': (
                'Twenty-year average barrel aging with complete oxidative '
                'transformation; full rancio development; dried fig, apricot, '
                'and orange peel replacing primary fruit entirely; the '
                'classic service tier for Tawny Port at formal dinner '
                'programmes; Niepoort Tawny 20-year is the sommelier '
                'benchmark for this tier alongside Ramos Pinto Ervamoira.'
            )
        },
        {
            'tier': 4,
            'tier_name': '30-40 Year Age-Indicated Tawny (apex oxidative complexity)',
            'criteria': (
                'Thirty to forty-year average barrel aging; extraordinary rancio '
                'and dried fruit concentration with maximum oxidative complexity; '
                'the Douro schist mineral character surviving as a dry, '
                'earthy persistence beneath the dominant oxidative register; '
                'Niepoort 40-year and Ramos Pinto 30-year are the benchmark '
                'expressions; very limited production and high price — '
                'USD $150–300 per 750ml — reflecting decades of '
                'barrel space occupied for the long aging programme.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve 10-year Tawny at 14–16°C to preserve the fresh dried '
            'cherry and lighter aromatic register that distinguishes the '
            '10-year from more oxidized expressions; the lighter body '
            'and residual primary fruit character of the 10-year is '
            'best appreciated at a slightly cooler temperature than the '
            '20-year style; stable after opening for 4–6 weeks recorked '
            'and refrigerated — Tawny Port\'s oxidative aging makes it '
            'significantly more stable after opening than Vintage Port '
            'or Ruby Port.'
        ),
        'vessel': (
            'Serve in a Port copita or small tulip glass (80–100ml format) '
            'with 60–75ml pour; the narrow aperture concentrates the dried '
            'fruit and emerging rancio aromatics; present with a verbal '
            'explanation of the "10-year average age" designation versus '
            'the common misconception that "10-year Tawny" means a '
            '10-year-old single vintage — the solera blending methodology '
            'that maintains the average age is frequently misunderstood '
            'and the explanation adds significant value to the service '
            'context.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Ramos Pinto — Vila Nova de Gaia (1880; the benchmark 10-year and '
            '20-year Tawny producer for consistent quality across declared '
            'vintages and age-indicated tawny programme); also: Niepoort '
            '(the most celebrated independent Port house for tawny and '
            'Colheita quality, with 40-year Tawny as the apex expression); '
            'Graham\'s 10-year Tawny is the primary quality comparison '
            'point in North American distribution.'
        ),
        'north_america_access': (
            'Ramos Pinto 10-year Tawny is distributed through the Roederer '
            'group import network in the US at USD $25–40 per 750ml. '
            'In Canada, BCLDB BC carries Ramos Pinto 10-year on regular '
            'allocation at CAD $35–50. The Quinta dos Bons Aires label '
            'is the standard commercial expression; the Ervamoira 10-year '
            'Tawny (Douro Superior fruit) is the premium parallel expression '
            'available at specialist Portuguese wine retailers.'
        ),
        'culinary_application': (
            '10-Year Tawny Port is the classic pairing with crème brûlée, '
            'tarte tatin, and almond-based pastry — the lighter dried fruit '
            'and emerging caramel character of the 10-year creates a direct '
            'flavour bridge to caramelized sugar and roasted almond desserts. '
            'The 10-year style is more food-flexible than the 20-year: '
            'the partial retention of primary dried cherry character makes '
            'it serviceable alongside blue cheese (Roquefort, Gorgonzola) '
            'as well as dessert, while the 20-year and older Tawny '
            'expressions are primarily dessert and digestif service wines.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

# Switch to 20-year Tawny depth entry
session.switch_region(
    new_region='Portugal — Douro Valley (20-Year Tawny Port, Niepoort Tawny, Extended Oxidative Aging, Nut and Dried Fruit)',
    new_tradition='fortified'
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Niepoort — Vila Nova de Gaia, Douro Valley',
    'location': 'Vila Nova de Gaia, Porto, Portugal',
    'description': (
        'Niepoort is the most celebrated of the independent Port houses — a '
        'family-owned Port shipper founded in 1842 by Eduard Niepoort, a Dutch '
        'merchant who settled in Porto and established a small Port trading '
        'company. Under the fifth generation, Dirk Niepoort (the current '
        'family director), Niepoort has become the reference house for '
        'both Colheita single-vintage Tawny Port and for a new generation '
        'of dry Douro table wines that established the Douro as a serious '
        'table wine region in the 1990s. Niepoort\'s Tawny Port programme '
        'is the sommelier benchmark for age-indicated tawny quality across '
        'all age expressions (10, 20, 30, 40-year) — the house maintains '
        'one of the deepest Colheita archives in the Port trade, with '
        'single-vintage Colheita dating back to the 1870s. The 20-year '
        'Niepoort Tawny is the reference expression for the extended '
        'oxidative style of blended age-indicated Tawny Port.'
    ),
    'founded': '1842',
    'region': 'Vila Nova de Gaia, Porto, Portugal',
    'website': 'niepoort-vinhos.com',
    'verified': True
})

session.add_beverage({
    'name': (
        'Niepoort 20-Year Tawny Port — Extended Oxidative Barrel Aging, '
        'Douro Valley Touriga Nacional and Franca, Vila Nova de Gaia Lodge'
    ),
    'category': 'fortified',
    'subcategory': 'port_tawny',
    'origin': 'Portugal',
    'region': 'Portugal — Douro Valley (20-Year Tawny Port, Niepoort Tawny, Extended Oxidative Aging, Nut and Dried Fruit)',
    'producer': 'Niepoort — Vila Nova de Gaia, Douro Valley',
    'alcohol_content': 20.0,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'Niepoort sources fruit for its Tawny Port programme from owned and '
        'contracted vineyards across the Douro Valley DOC, with primary '
        'emphasis on Cima Corgo — the central Douro sub-zone centred on '
        'the Pinhão Valley and its tributary valleys at 150–500m elevation. '
        'The Cima Corgo schist terraces provide the concentrated, high-alcohol '
        'base wines (13–14% potential alcohol before fortification) necessary '
        'for the extended oxidative barrel aging programme. For the 20-year '
        'Tawny, Niepoort specifically selects lots with high natural acidity '
        '(pH 3.2–3.4 in the base wine) — the acidity framework being '
        'essential for the wine to survive 20+ years of oxidative barrel '
        'aging without losing freshness or structure. The aging takes place '
        'entirely in the Vila Nova de Gaia lodge (15–18°C year-round) '
        'in 550L seasoned oak pipes — the Gaia maritime temperature being '
        '10–15°C cooler than equivalent Douro Valley summer temperatures, '
        'producing a slower, more complex oxidative aging trajectory with '
        'lower evaporation rates (2.5–3.0% annually in Gaia versus '
        '3.5–5.0% in the Douro Valley) and greater aromatic complexity '
        'development in the final 20-year expression.'
    ),
    'production_technique': (
        'The Niepoort 20-Year Tawny is produced through the same base '
        'wine production as the 10-year (foot-treading in stone lagares, '
        'fortification at baumé point, small seasoned oak pipes at Gaia) '
        'but maintained in the aging solera to an average of 20 years '
        'rather than 10. The additional decade of oxidative barrel aging '
        'transforms the 10-year dried cherry and caramel character '
        'into the fully developed rancio register — walnut oil, hazelnut, '
        'and the complex ester compounds that characterize properly aged '
        'tawny Port at the 20-year level. The Niepoort winemaking team '
        '(led by Dirk Niepoort) distinguishes the 20-year solera through '
        'selection of base wine lots with specific acidity and varietal '
        'composition: a higher proportion of Touriga Franca (for aromatic '
        'complexity and floral rancio character) and Tinta Amarela (for '
        'freshness and acid structure) relative to the darker, more '
        'tannic Touriga Nacional. The 20-year undergoes annual blending '
        'assessment in which the solera lots are evaluated for color '
        'consistency (the amber-tawny must be uniform across all barrels), '
        'aromatic profile (the rancio and dried fruit development must '
        'be balanced), and structural integrity (the acid backbone '
        'must remain fresh despite two decades of oxidative aging). '
        'Young base wine (5–7 years old) is added annually to replace '
        'wine drawn off for bottling, maintaining the 20-year average '
        'through continuous blending additions. The Niepoort 20-year '
        'is bottled without vintage date and without the mandatory '
        'bottling date of the Colheita style — the age statement '
        '("20 years") and the NV nature of the blended solera are '
        'the only temporal markers on the label.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Oloroso Sherry 20-year VORS (oxidative barrel aging, complete oxidation)',
            'connection': (
                'Niepoort 20-Year Tawny and an Oloroso VORS (Very Old Rare Sherry, '
                'minimum 30 years but comparable 20-year tier in the Oloroso '
                'aging hierarchy) share the complete oxidative transformation '
                'from primary grape fruit to secondary rancio-and-dried-fruit '
                'complexity through extended barrel aging in small seasoned wood. '
                'The critical distinction is sweetness and structure: the 20-year '
                'Tawny retains 80–110 g/L residual sugar from the Port fortification '
                'method, while Oloroso VORS is completely dry (2–5 g/L residual '
                'sugar); the rancio character in both is created through the same '
                'oxidative ester chemistry, making them directly comparable '
                'as oxidative fortified wines at different sugar levels.'
            )
        },
        {
            'tradition': 'Armagnac 20-year Hors d\'Age (French brandy, oxidative barrel aging, dried fruit)',
            'connection': (
                'Niepoort 20-Year Tawny and a 20-year Armagnac Hors d\'Age '
                'develop similar oxidative complexity profiles through extended '
                'aging in small French oak barrels: both develop rancio (walnut, '
                'hazelnut oxidative ester), dried fruit (fig, prune, apricot), '
                'and caramel through 20 years of controlled oxidative barrel '
                'contact. The structural distinction is fundamental: Armagnac '
                'is a dry distillate (no residual sugar) aged in new or '
                'seasoned oak; Tawny Port is a fortified wine (80–110 g/L '
                'residual sugar) aged in old seasoned pipes. Both demonstrate '
                'that 20 years of oxidative barrel aging produces a rancio '
                'complexity that cannot be replicated through any accelerated '
                'aging process — time in barrel is the irreducible requirement '
                'for genuine rancio character in both traditions.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Rich tawny amber with orange-gold highlights — more deeply amber '
            'and less orange than the 10-year; the complete oxidative color '
            'transformation from garnet to tawny amber has occurred through '
            '20 years of barrel oxidation; brilliant clarity; viscous, '
            'slow legs from 19–20% ABV and 80–110 g/L residual sugar; '
            'the amber intensity of the 20-year is the visual benchmark '
            'for distinguishing genuine age-indicated Tawny from '
            'commercial blended tawny of uncertain age.'
        ),
        'nose': (
            'Dried apricot and fig as the dominant primary register — the '
            'red fruit has been fully transformed by 20 years of oxidative '
            'barrel aging into the dried stone fruit character of genuine '
            'extended-age Tawny; rancio (walnut oil, hazelnut) at full '
            'development from two decades of ester accumulation in '
            'seasoned oak; orange peel and caramel from the Maillard '
            'browning of residual sugar under oxidative conditions; honey '
            'and beeswax from the high residual sugar; the Douro schist '
            'mineral character still perceptible as a dry, earthy note '
            'beneath the dried fruit and rancio complexity — the terroir '
            'marker of the Cima Corgo schist that survives two decades '
            'of barrel transformation.'
        ),
        'palate': (
            'Medium-sweet with bright, persistent acidity balancing the '
            '80–110 g/L residual sugar; dried apricot and fig from entry '
            'through mid-palate; the rancio walnut and hazelnut building '
            'on the finish; very long finish (75–90 seconds) from the '
            'combination of sugar concentration and rancio ester complexity; '
            'the tannin from the Douro base wine has been completely '
            'transformed through 20 years of oxidative polymerization — '
            'the palate is silky and smooth despite the structural intensity; '
            'the fortification spirit fully integrated and imperceptible '
            'except as a warming heat on the finish.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Generic Age-Indicated Tawny 20-year (major commercial houses)',
            'criteria': (
                'Age-indicated 20-year Tawny from large Port houses with high '
                'volume production (Sandeman, Taylor Fladgate, Calem); the '
                'age statement is legally verified but the solera management '
                'prioritizes consistency over complexity; rancio development '
                'is present but less nuanced than the specialist independent '
                'house expressions; the benchmark commercial tier for the '
                '20-year Tawny style.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Ramos Pinto Ervamoira 20-year / Graham\'s 20-year',
            'criteria': (
                'Premium age-indicated 20-year Tawny from quality-focused '
                'houses with identifiable estate fruit; the Ervamoira expression '
                '(Douro Superior schist) shows a distinct terroir character '
                'within the 20-year oxidative framework; Graham\'s 20-year '
                'is the UK and North American quality benchmark at the '
                'mid-premium tier; greater aromatic complexity and more '
                'defined rancio than the commercial volume tier.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Niepoort 20-Year Tawny (benchmark independent quality)',
            'criteria': (
                'The reference expression for the 20-year Tawny style at '
                'benchmark independent house quality; the Niepoort solera '
                'management — with Dirk Niepoort\'s personal supervision '
                'of the Tawny programme — produces the most complex dried '
                'fruit and rancio profile in the 20-year tier; the '
                'acid backbone is more pronounced than equivalent commercial '
                'expressions, providing greater structure and aging '
                'potential in the blended solera wine.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Niepoort 30-Year / 40-Year Tawny (apex age-indicated)',
            'criteria': (
                'The apex of age-indicated Tawny production at 30 and 40-year '
                'average barrel aging; extraordinary rancio and mineral complexity '
                'at maximum development; the Niepoort 40-year is among the '
                'finest age-indicated Tawny expressions produced in the '
                'Douro system; very limited production and pricing of '
                'USD $120–250 per 750ml reflects the multi-decade barrel '
                'space cost and the exceptional complexity of the '
                'finished wine.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Niepoort 20-year Tawny at 14–16°C for dessert service '
            'or at 12–14°C as a digestif after a formal dinner — the '
            'slightly cooler digestif temperature preserves the '
            'rancio aromatic complexity and reduces the viscosity '
            'of the high residual sugar; stable after opening '
            'for 6–8 weeks recorked and refrigerated; the 20-year '
            'style is the most stable after opening of all Tawny '
            'Port tiers due to the complete oxidative transformation '
            'that has already occurred during barrel aging.'
        ),
        'vessel': (
            'Serve in Port copita (80–100ml) or small tulip glass '
            'with 60–80ml pour; the narrow aperture concentrates '
            'the rancio and dried apricot aromatics above the '
            'wine surface; the amber color is displayed '
            'optimally in a clear crystal glass against '
            'a white table cloth; present alongside dessert or '
            'aged cheese with a verbal explanation of the 20-year '
            'average age concept and the distinction between '
            'age-indicated Tawny (blended average) and Colheita '
            '(single vintage) — the two tiers of extended '
            'wood-aged tawny Port that represent different '
            'quality philosophies within the same aging tradition.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Niepoort — Vila Nova de Gaia (1842; the sommelier benchmark '
            'for age-indicated Tawny Port quality across all expressions; '
            'the 20-year and 40-year Tawny are the reference points for '
            'independent house quality in the tawny Port category; '
            'also the most celebrated Colheita specialist with archive '
            'single-vintage expressions dating to the 1870s).'
        ),
        'north_america_access': (
            'Niepoort is distributed in the United States through '
            'Skurnik Wines (New York), available at fine wine retailers '
            'nationally; USD $45–70 per 750ml for the 20-year expression. '
            'In Canada, BCLDB BC Vintages and LCBO Vintages Ontario '
            'carry selected Niepoort Tawny expressions; the 20-year '
            'is the recommended trade buyer choice for any professional '
            'wine programme comparing Portuguese fortified wine '
            'quality at the benchmark independent house level.'
        ),
        'culinary_application': (
            'Niepoort 20-year Tawny is the canonical pairing with '
            'crème caramel, tarte tatin, and almond pastry (tarte de '
            'amêndoa) — the dried apricot and rancio walnut character '
            'of the 20-year creates a direct sensory bridge to '
            'caramelized sugar and roasted nut desserts. At a '
            'professional level, the 20-year Tawny is also the '
            'benchmark pairing with aged hard sheep\'s milk cheese '
            '(Manchego Reserva, Serrano, Azeitão DOP) — the shared '
            'rancio and crystallized amino acid character of the '
            'cheese and the wine creating one of the most coherent '
            'within-tradition food and wine pairings in the '
            'Portuguese culinary canon.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
