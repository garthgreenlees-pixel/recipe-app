import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Setúbal Peninsula (Moscatel de Setúbal DOC, José Maria da Fonseca, 20-Year Oxidative Fortified)',
    output_dir='.',
    starting_entry=1,
    session_number=71,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'José Maria da Fonseca — Azeitão, Setúbal Peninsula',
    'location': 'Azeitão, Setúbal Peninsula, Portugal',
    'description': (
        'José Maria da Fonseca is the oldest continuously operating wine company '
        'in Portugal, founded in 1834 by José Maria da Fonseca in Azeitão on the '
        'Setúbal Peninsula — predating the phylloxera crisis, the founding of the '
        'modern Douro Port trade regulatory system, and the establishment of most '
        'of the major Port shippers. The company has remained in the Fonseca family '
        'for seven generations and is unique in Portuguese wine history for its '
        'continuous unbroken production record since the early 19th century. '
        'José Maria da Fonseca is the benchmark producer for Moscatel de Setúbal '
        'DOC — the fortified sweet wine made from the Moscatel de Setúbal '
        '(Muscat of Alexandria) grape on the limestone hillsides of the '
        'Setúbal Peninsula south of Lisbon. The company\'s Moscatel de Setúbal '
        '20 Years is the reference expression for the extended oxidative '
        'aging style of Portuguese fortified Moscatel, with barrel-aged '
        'expressions dating back to the 1920s and 1930s remaining in the '
        'company cellar in Azeitão as both commercial product and historical archive.'
    ),
    'founded': '1834',
    'region': 'Setúbal Peninsula, Portugal',
    'website': 'jmf.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Broadbent Selections / Global Wine and Spirits (US and Canada)',
    'type': 'importer',
    'description': (
        'José Maria da Fonseca wines including Moscatel de Setúbal are distributed '
        'in the United States through Broadbent Selections, which handles the full '
        'Fonseca portfolio including the 20-year and single-vintage Moscatel '
        'expressions. In Canada, BCLDB BC and LCBO Ontario list selected Fonseca '
        'Moscatel de Setúbal expressions on regular allocation, making it one of '
        'the more accessible Portuguese fortified wines in the Canadian market. '
        'The Setúbal 20-Year expression is available in UK through specialist '
        'Portuguese wine retailers including The Wine Society and Davy\'s Wine '
        'Merchants. Pricing in North America is USD $30–55 for the 20-year '
        'expression, making it significantly undervalued relative to its '
        'complexity and aging heritage compared to equivalent Madeira or '
        'aged Tawny Port expressions.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['fortified'],
    'website': 'jmf.pt',
    'verified': False
})

session.add_beverage({
    'name': (
        'José Maria da Fonseca Moscatel de Setúbal 20 Years — DOC Setúbal, '
        'Muscat of Alexandria, Oxidative Barrel Aging, Azeitão Limestone'
    ),
    'category': 'fortified',
    'subcategory': 'moscatel',
    'origin': 'Portugal',
    'region': 'Portugal — Setúbal Peninsula (Moscatel de Setúbal DOC, José Maria da Fonseca, 20-Year Oxidative Fortified)',
    'producer': 'José Maria da Fonseca — Azeitão, Setúbal Peninsula',
    'alcohol_content': 19.0,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'The Setúbal Peninsula extends south from Lisbon between the Tagus '
        'estuary to the north and the Sado estuary to the south, bounded '
        'by the Atlantic Ocean to the west. The limestone hillsides of the '
        'Serra da Arrábida — a national park running along the southern '
        'spine of the peninsula at 100–500m elevation — provide the specific '
        'terroir for Moscatel de Setúbal DOC: calcareous white limestone and '
        'clay soils of Jurassic and Cretaceous age, with southern and '
        'southeastern exposure maximizing solar radiation for the warm-climate '
        'Muscat of Alexandria variety. The Mediterranean microclimate of the '
        'Arrábida limestone ridge (sheltered from Atlantic winds by the rock '
        'mass) creates the warm, dry conditions necessary to achieve full '
        'phenolic and sugar maturity in Moscatel de Setúbal\'s thick-skinned '
        'berries: harvest potential alcohol of 13–14% before fortification, '
        'with 250–350 g/L residual sugar preserved by the arresting grape '
        'spirit addition. The Tagus and Sado estuaries on both sides of the '
        'peninsula create a maritime moderating influence that prevents the '
        'extreme summer heat of the Alentejo interior — maximum temperatures '
        'of 28–32°C versus 35–42°C in the Alentejo — while maintaining the '
        'warmth and sunshine hours necessary for Moscatel berry development. '
        'The Azeitão village and the surrounding Fonseca estate vineyards sit '
        'at 80–150m on the Arrábida limestone — the classic Setúbal terroir '
        'for Moscatel de Setúbal DOC production.'
    ),
    'production_technique': (
        'Moscatel de Setúbal production at José Maria da Fonseca follows the '
        'Portuguese fortified wine method of mutage — stopping fermentation '
        'by adding neutral grape spirit (aguardente vínica) to arrest yeast '
        'activity and preserve natural grape sugar. The Muscat of Alexandria '
        '(Moscatel de Setúbal) grape is harvested in mid-September when '
        'the berries reach 13–14% potential alcohol and 250–350 g/L '
        'natural sugar concentration. After gentle de-stemming and '
        'destalking to preserve the delicate Muscat aromatics, the must '
        'ferments at 18–20°C for 3–5 days until approximately 6–8% '
        'alcohol has been achieved, at which point the 77% ABV grape spirit '
        'is added at a rate of approximately 100L per 1000L of must — '
        'arresting fermentation and producing a wine of 17.5–19.5% ABV '
        'with 100–150 g/L residual sugar. The defining feature of the '
        'Fonseca Moscatel production is the post-fortification maceration: '
        'the Moscatel grape skins remain in contact with the fortified '
        'must for 4–6 weeks after fortification, extracting the terpene '
        'aromatic compounds (linalool, geraniol, nerol, citronellol) that '
        'define the Muscat aromatic profile — the terpene extraction from '
        'extended skin contact with Moscatel is the key quality differentiator '
        'between Setúbal and other fortified Muscat wines that do not '
        'use extended post-fortification maceration. After pressing, the '
        'wine is transferred to small 300–500L chestnut and oak toneis '
        'for oxidative barrel aging — a process of deliberate controlled '
        'oxidation over years that concentrates the wine through evaporation '
        '(the "angel\'s share"), develops the characteristic amber-orange '
        'color through oxidative browning of the terpene aromatics, and '
        'generates the complex dried fruit, caramel, and preserved citrus '
        'peel character that defines the 20-year Setúbal style. The 20-year '
        'expression is a solera-style blend of multiple vintages with an '
        'average age of 20 years — the young wines are added to the solera '
        'to replace the wine drawn off for bottling, maintaining a continuous '
        'average age. The oldest barrels in the Fonseca solera contain '
        'wine from the 1920s and 1930s.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Madeira 20-Year Malmsey (volcanic island, oxidative barrel aging, fortified)',
            'connection': (
                'Moscatel de Setúbal 20 Years and Madeira 20-Year Malmsey '
                '(Malvasia) occupy the same structural tier in Portuguese fortified '
                'wine: both are extended oxidative barrel-aged fortified wines '
                'from volcanic or limestone terroirs, both built on aromatic grape '
                'varieties (Muscat of Alexandria versus Malvasia) that survive '
                'decades of oxidative aging with their core aromatic character '
                'intact, and both represent the Portuguese fortified wine '
                'tradition outside the Port/Douro axis. The parallel oxidative '
                'aging chemistry is direct: both wines develop amber color through '
                'phenolic oxidation, caramel character through Maillard reactions '
                'under heat, and rancio character (oxidative nut, dried fruit) '
                'through long ester development in barrel. Madeira has higher '
                'international recognition; Setúbal offers comparable complexity '
                'at significantly lower price positioning.'
            )
        },
        {
            'tradition': 'Muscat de Beaumes-de-Venise (Rhône Valley VDN, Muscat Blanc)',
            'connection': (
                'Moscatel de Setúbal and Muscat de Beaumes-de-Venise are both '
                'fortified Muscat wines of the vin doux naturel (VDN) or '
                'mutage type — fermentation arrested by grape spirit to '
                'preserve natural sugar. The technical parallel is identical: '
                'both use Muscat varieties (Alexandria in Portugal; Blanc à '
                'Petits Grains in France), both add neutral spirit to arrest '
                'fermentation, and both preserve terpene aromatic compounds '
                '(linalool, geraniol) as the defining sensory character. '
                'The critical distinction is aging philosophy: Beaumes-de-Venise '
                'is generally consumed young (1–3 years) without extended '
                'oxidative barrel aging; Setúbal 20 Years undergoes two decades '
                'of deliberate oxidative aging that transforms the fresh Muscat '
                'aromatics into the complex dried-fruit and rancio register '
                'impossible to achieve from young-harvest fortified Muscat.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber with orange-tawny reflections — the characteristic '
            'colour of 20-year oxidative aging in chestnut and oak barrels; '
            'the colour is more intense than 20-year Tawny Port due to the '
            'higher residual sugar concentration (100–150 g/L versus 80–110 g/L '
            'in Tawny) which drives deeper Maillard browning during oxidative '
            'aging; viscous legs on the glass from the raised residual sugar '
            'and the 19% ABV; brilliant clarity after decanting off any '
            'bottle sediment from long barrel and bottle aging.'
        ),
        'nose': (
            'The dominant register of Moscatel de Setúbal 20 Years is dried '
            'orange peel and candied citrus zest — the terpene aromatics of '
            'Muscat of Alexandria (linalool, geraniol) transformed by oxidative '
            'aging from fresh floral Muscat into the concentrated preserved '
            'citrus character; caramel and burnt sugar from the Maillard '
            'reactions during barrel aging; dried fig, apricot jam, and '
            'raisin from the concentration of fruit sugars over 20 years; '
            'beneath the fruit and caramel, a rancio note (oxidative nut, '
            'walnut oil) from the extended ester development; honey and '
            'beeswax from the high residual sugar in an oxidative environment; '
            'the aromatic complexity is greater than equivalent-age Tawny Port '
            'due to the Moscatel terpene foundation that survives and '
            'transforms through the oxidative aging period.'
        ),
        'palate': (
            'Sweet but not cloying — the 100–150 g/L residual sugar is balanced '
            'by the bright natural acidity of Muscat of Alexandria and by the '
            'sharp, clean finish of the 19% ABV. Concentrated dried orange '
            'and citrus peel through the entry; caramel, toffee, and dried '
            'apricot through the mid-palate; the rancio oxidative character '
            'building on the finish; very long finish (60–90 seconds) from '
            'the combination of sugar concentration, terpene aromatic '
            'persistence, and rancio ester development; the fortification '
            'spirit fully integrated after 20 years of barrel and bottle '
            'aging — no harshness or raw spirit character remains; the '
            'balance between sweetness, acidity, and oxidative complexity '
            'is the defining quality marker of properly aged Moscatel de Setúbal.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Moscatel de Setúbal DOC (commercial cooperative, no age statement)',
            'criteria': (
                'Young Moscatel de Setúbal without age statement from cooperative '
                'production; 2–5 years barrel aging; the fresh Muscat aromatics '
                'still dominant before oxidative transformation; sweet and '
                'aromatic but without the dried fruit and rancio complexity '
                'of extended aging; suitable for immediate consumption with '
                'dessert but lacking the structural depth of aged expressions.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'José Maria da Fonseca Moscatel de Setúbal Superior (5-year)',
            'criteria': (
                'Five-year oxidative aging in the Fonseca solera; the fresh '
                'Moscatel terpenes beginning to transform into dried citrus and '
                'caramel character; still retaining significant primary Muscat '
                'fruit; 5-year expression is the entry point for the Fonseca '
                'quality tier with demonstrable barrel aging complexity that '
                'separates it from cooperative no-age-statement production.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'José Maria da Fonseca Moscatel de Setúbal 20 Years (benchmark)',
            'criteria': (
                'Twenty-year solera-average oxidative aging in the Fonseca cellar; '
                'complete terpene transformation from fresh Muscat to dried orange '
                'peel and rancio; the benchmark expression for the Setúbal style; '
                'compares directly with 20-year Tawny Port and Madeira 20-year '
                'age-indicated expressions at a lower price point; the definitive '
                'reference for the extended-oxidative Portuguese fortified '
                'Moscatel tradition.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'José Maria da Fonseca Setúbal Single Vintage Colheita (collector tier)',
            'criteria': (
                'Single-vintage Moscatel de Setúbal colheita aged 30–50+ years in '
                'the Fonseca cellar; the oldest expressions from the 1920s–1940s '
                'represent the apex of Portuguese fortified Moscatel production '
                'with extraordinary rancio and oxidative complexity; a collector '
                'category comparable in scarcity to single-vintage 40-year Tawny '
                'Port or Madeira Solera of similar age; pricing USD $200–500 '
                'for surviving mid-20th century colheita expressions.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Moscatel de Setúbal 20 Years at 12–14°C — slightly cooler '
            'than room temperature to preserve the aromatic intensity of the '
            'terpene compounds, which volatilize rapidly at higher service '
            'temperatures and are less perceptible above 16°C. Do not serve '
            'fully chilled (below 10°C) as the viscosity of the high residual '
            'sugar becomes texturally dominant and the aromatic complexity is '
            'suppressed; decant gently through a fine mesh if sediment is '
            'present in older expressions; the 20-year expression is stable '
            'after opening for 4–6 weeks if recorked and refrigerated.'
        ),
        'vessel': (
            'Serve in a white-wine style tulip glass (ISO tasting glass or '
            'small-format white wine glass) rather than a spirit glass or Port '
            'copita — the terpene aromatic complexity of Moscatel de Setúbal '
            'benefits from a wider bowl than Port copita format; pour 60–80ml '
            'per service as a dessert wine or digestif; the amber colour and '
            'legs from the residual sugar are best displayed in a clear crystal '
            'glass against a white background; serve after a formal dinner '
            'programme as a digestif alongside almond-based Portuguese pastry '
            '(tarte de amêndoa, bolo de amêndoa) or aged cheeses — the '
            'sweet-oxidative character of the 20-year creates the classic '
            'Portuguese fortified wine and cheese service combination.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'José Maria da Fonseca — Azeitão, Setúbal Peninsula: the oldest '
            'continuously operating wine company in Portugal (founded 1834) '
            'and the benchmark producer for Moscatel de Setúbal DOC in all '
            'age-indicated expressions. The 20-year solera is the reference '
            'point for the extended oxidative style; the colheita single-vintage '
            'expressions from the Fonseca cellar archive are the apex of '
            'Portuguese fortified Moscatel production and a unique historical '
            'wine record going back to the early 20th century.'
        ),
        'north_america_access': (
            'José Maria da Fonseca Moscatel de Setúbal 20 Years is distributed '
            'in the United States through Broadbent Selections (San Francisco) '
            'at USD $30–45 per 500ml bottle — representing exceptional value '
            'for the complexity and heritage of the expression. BCLDB BC and '
            'LCBO Ontario carry selected Fonseca Moscatel on regular allocation. '
            'The 20-year expression is a strong sommelier recommendation for '
            'dessert wine programmes seeking alternatives to Sauternes, '
            'aged Tawny Port, or Madeira at lower price positioning.'
        ),
        'culinary_application': (
            'Moscatel de Setúbal 20 Years is the canonical pairing with '
            'Portuguese almond and egg-based pastry — tarte de amêndoa, '
            'pastel de nata com amêndoa, or Setubalense almond cake — '
            'where the oxidative dried citrus and caramel character of the '
            'wine bridges to the roasted almond and egg custard flavours '
            'of the pastry. The high residual sugar and rancio oxidative '
            'character also creates a direct pairing with aged sheep\'s '
            'milk cheese (Azeitão DOP, Serpa DOP) from the Setúbal '
            'Peninsula — the cheese and wine share the same terroir and '
            'the same oxidative-fat flavour architecture.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
