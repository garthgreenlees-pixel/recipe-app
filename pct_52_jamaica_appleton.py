import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Jamaica — St Elizabeth Parish (Appleton Estate 21-Year, Nassau Valley, Pot-Column Hybrid)',
    output_dir='.',
    starting_entry=1,
    session_number=56,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Appleton Estate — Nassau Valley, Black River, St Elizabeth Parish',
    'location': 'Nassau Valley, Saint Elizabeth Parish, Jamaica',
    'description': (
        'Appleton Estate operates the oldest sugar estate and distillery complex in Jamaica, with '
        'documented rum production records extending to 1749, making it the oldest continuously '
        'documented rum-producing estate in the Caribbean. The estate encompasses 2,400 hectares '
        'of the Nassau Valley in Saint Elizabeth Parish — Jamaica\'s southernmost and driest parish — '
        'where the Black River and its tributaries flow through a limestone karst valley ringed by '
        'the Santa Cruz Mountains. The estate grows its own Saccharum officinarum sugarcane for '
        'fermentation and maintains a legacy of pot still distillation that preserves the high-ester '
        'character defining Jamaican rum internationally. Master Blender Joy Spence, appointed in '
        '1997 as the first woman to serve as master blender of a major Caribbean rum estate, '
        'oversees the Appleton range including the 21-year aged apex expression.'
    ),
    'founded': '1749 (documented rum production)',
    'region': 'Nassau Valley, Saint Elizabeth Parish, Jamaica',
    'website': 'appletonestate.com',
    'verified': True
})

session.add_beverage({
    'name': 'Appleton Estate 21-Year Nassau Valley — St Elizabeth Limestone Karst, Pot-Column Hybrid, Joy Spence Blend',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Jamaica',
    'region': 'Jamaica — St Elizabeth Parish (Appleton Estate 21-Year, Nassau Valley, Pot-Column Hybrid)',
    'producer': 'Appleton Estate — Nassau Valley, Black River, St Elizabeth Parish',
    'alcohol_content': 43.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'The Nassau Valley in Saint Elizabeth Parish is a confined limestone karst depression in '
        'Jamaica\'s southwestern interior, enclosed by the Santa Cruz Mountains to the north and '
        'east and the Cockpit Country karst plateau to the north. Saint Elizabeth is Jamaica\'s '
        'driest parish — receiving approximately 1,200–1,500mm of annual rainfall compared to '
        '2,500–4,000mm in the Blue Mountains of eastern Jamaica — creating a more concentrated, '
        'slower-growing sugarcane than the wetter parishes of Jamaica\'s northern coast. The '
        'Black River — Jamaica\'s longest navigable river — flows through the Nassau Valley and '
        'historically provided the transport link that made the Appleton Estate commercially '
        'viable in the colonial era, when rum barrels moved by river to the Black River harbor '
        'for loading onto ships bound for England. The limestone karst geology of the Nassau '
        'Valley floor creates the specific water chemistry that defines Appleton rum production: '
        'mineral-rich, slightly alkaline water filtered through Cenozoic limestone formations '
        'at the valley floor, with calcium and magnesium content that influences the yeast '
        'fermentation mineral environment and the extraction of specific oak compounds during '
        'aging. The Appleton Estate\'s own cane cultivation on 2,400 hectares of valley floor '
        'and lower hillside terrain gives the distillery direct control over raw material quality '
        'through varietal selection, irrigation management, and harvest timing — an integrated '
        'agricultural-distillation operation with continuity from the 18th century plantation '
        'system through to modern estate management.'
    ),
    'production_technique': (
        'Appleton Estate 21-Year is produced through a hybrid distillation system that defines '
        'the Jamaican rum style: pot still distillation for high-ester, heavy-bodied spirit '
        'components, blended with lighter column still fractions to create the final assemblage '
        'that Joy Spence ages in American white oak ex-bourbon barrels. The pot still operation '
        'at Appleton uses traditional copper pot stills with a large capacity retort for the '
        'low-wine stripping run, followed by a second pot still pass for the spirit run with '
        'careful heads and tails management to preserve the characteristic Jamaican ester '
        'register — primarily ethyl acetate, isoamyl acetate, and ethyl butyrate in concentrations '
        'substantially higher than column-still rums. The column still fractions are produced '
        'at higher proof (85–90% ABV) and lower ester content, providing the blending palette '
        'with lighter, cleaner components that Joy Spence uses to balance the pot still\'s '
        'richness without diluting its character. The fermentation preceding both pot and column '
        'distillation uses the classic Jamaican long fermentation method: 5–10 days in open '
        'wooden washbacks (staves of Queensland kauri and local timber, accumulated with decades '
        'of yeast and lactic acid bacteria culture) at warm ambient temperatures, producing '
        'washes of unusually high ester and organic acid content. The Appleton 21-year aged '
        'expression requires Joy Spence to identify and select barrels from the aging warehouses '
        'that have developed the specific dried fruit, chocolate, and spice profile she designates '
        'for the 21-year blend: typically American white oak ex-bourbon barrels between 18 and '
        '25 years old, showing mahogany colour, full rancio development, and the integration of '
        'Jamaican pot still ester character with oak-derived vanilla and dried fruit compounds. '
        'Proofed to 43% ABV; no caramel colouring added to the 21-year expression.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Single Malt Scotch (Islay, heavy pot still, high ester character)',
            'connection': (
                'Appleton Estate 21-Year and Islay single malt Scotch whisky are both premium aged '
                'pot still spirits that are defined by their high congener complexity — the Jamaican '
                'rum by ethyl esters from long open fermentation and pot still distillation, the '
                'Islay malt by phenol compounds from peat-smoked barley and copper pot distillation. '
                'Both are aged for extended periods in American ex-bourbon barrels (the primary aging '
                'vessel in both categories), both develop rancio or equivalent oxidative complexity '
                'over time, and both command premium pricing on the basis of distillery-specific '
                'character rather than regional genericness — Appleton Nassau Valley and Bowmore '
                'Islay are both expressions where the specific production site\'s terroir is '
                'preserved through the aging process rather than blended away.'
            )
        },
        {
            'tradition': 'Armagnac (Gascony, pot still Armagnac, age-dated vintages)',
            'connection': (
                'Joy Spence\'s master blending philosophy at Appleton parallels the Armagnac '
                'négociant tradition: both disciplines involve selecting aged distillates from '
                'a range of cask maturities, still types (for Armagnac: alembic Armagnacais '
                'versus column), and vintage years to construct a final blended expression '
                'whose coherence reflects the master blender\'s sensory vision rather than '
                'any single cask\'s individual character. Both Armagnac and Jamaican estate '
                'rum operate within a tradition of named vintage and age-dated releases that '
                'situate the spirit in a specific agricultural and temporal context — the '
                'blender\'s art in both cases producing expressions of greater complexity '
                'than any individual component could achieve alone.'
            )
        },
        {
            'tradition': 'Port Wine LBV (Portugal, extended barrel aging, blended vintage)',
            'connection': (
                'Appleton 21-Year and Late Bottled Vintage Port both represent extended tropical/warm-'
                'climate barrel-aging programs in which a master blender makes the key '
                'decisions about when a specific cask\'s maturation peak has been reached '
                'and how to assemble component parts into a coherent final blend. Both '
                'achieve their complexity through the interaction of a rich, high-congener '
                'spirit base (pot still rum fermented from molasses; port wine from high-sugar '
                'Douro red varieties) with extended American or French oak barrel contact in '
                'a warm aging environment that accelerates the oxidative and extraction processes '
                'fundamental to the aged spirit\'s quality.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep mahogany with amber-red tints; full opacity from 21 years of tropical ex-bourbon '
            'barrel aging at Nassau Valley; heavy, slow-moving legs indicating the high glycerol '
            'content from the long fermentation and pot still distillation; the colour signals '
            'the extended Jamaican tropical aging without any caramel addition.'
        ),
        'nose': (
            'The Jamaican high-ester pot still character is present even after 21 years of '
            'aging: overripe tropical fruit (tamarind, black mango, ripe plantain) layered '
            'over the ex-bourbon oak vanilla and caramel; dark chocolate and espresso from '
            'the molasses compounds transformed through extended tropical barrel contact; '
            'a distinctive Jamaican funk — the ethyl butyrate and isoamyl ester compounds '
            'from long open fermentation — that persists beneath the oak integration; '
            'dried orange peel and warm spice from the 21-year barrel development; the '
            'Joy Spence signature of exceptional aromatic complexity held in precise balance.'
        ),
        'palate': (
            'Full body from the pot still fermentation and distillation heritage; the attack '
            'is rich and warming at 43% ABV with immediate dark chocolate and tropical dried '
            'fruit; the pot still ester character shows on the mid-palate as a lively, '
            'complex texture beneath the oak-derived caramel and vanilla; the Nassau Valley '
            'limestone water character contributes a fine mineral thread through the finish; '
            'very long finish — 60–90 seconds — with the Jamaican funk note persisting '
            'through the oak integration to a clean, warm, dry conclusion that confirms '
            '21 years of tropical barrel maturation without losing the Nassau Valley '
            'pot still identity.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Appleton Estate Signature Blend (aged 4+ years)',
            'criteria': (
                'The entry-level aged Appleton range: minimum 4-year ex-bourbon tropical aging '
                'showing initial Jamaican pot still ester character with oak integration beginning '
                '— the accessible reference for understanding the Nassau Valley style before the '
                'extended aged expressions demonstrate full complexity development.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Appleton Estate 8-Year Reserve',
            'criteria': (
                'Eight-year tropical aged Nassau Valley rum: the balance point between Jamaican '
                'ester freshness and ex-bourbon oak integration — sufficient barrel aging to '
                'produce vanilla and caramel complexity while the pot still funk and tropical '
                'fruit remain vivid; the cocktail and sipping premium tier.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Appleton Estate 12-Year Rare Casks',
            'criteria': (
                'Twelve-year select cask expressions from Joy Spence\'s warehouse: the ester '
                'complexity of the Nassau Valley pot still tradition beginning to integrate with '
                'full ex-bourbon barrel development — dried fruit, dark chocolate, and the '
                'Jamaican terroir in mature harmony; the connoisseur tier for neat service.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Appleton Estate 21-Year Nassau Valley',
            'criteria': (
                'Twenty-one year aged apex expression: maximum integration of Jamaican high-ester '
                'pot still character with tropical ex-bourbon barrel aging; Joy Spence\'s benchmark '
                'blending achievement; the expression that positions Jamaican estate rum in direct '
                'comparison with 21-year single malt Scotch and aged XO Cognac at international '
                'luxury spirits pricing and quality level.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Appleton 21-Year at 18–20°C neat in a warmed glass to open the full tropical '
            'dried fruit and Jamaican ester aromatic complexity; the 21-year expression has '
            'sufficient barrel integration to accept a single ice sphere at 12–14°C for relaxed '
            'sipping without losing its character; a few drops of still water at room temperature '
            'opens the dark chocolate and tamarind mid-palate register; do not refrigerate — '
            'cold temperature suppresses the evolved ester volatiles that distinguish 21-year '
            'Jamaican rum from younger expressions.'
        ),
        'vessel': (
            'Glencairn or tulip glass for neat service — the full mahogany colour and complex '
            'aromatics of the 21-year expression merit a vessel designed to concentrate vapour '
            'at the rim; a wide copita is acceptable for tableside service; serve in a flight '
            'context progressively from the Signature Blend through 12-Year to 21-Year to '
            'demonstrate the tropical aging arc from fresh Jamaican ester character to full '
            'Nassau Valley maturity — one of the most instructive vertical flights in the '
            'Caribbean rum category.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Appleton Estate (Nassau Valley, Saint Elizabeth, Jamaica) — the 21-Year Nassau '
            'Valley is the apex expression of Jamaican estate rum and the definitive benchmark '
            'for pot-column hybrid distillation aged in the Jamaican tropical environment; '
            'Joy Spence as master blender is the most recognized individual in Caribbean rum '
            'production by name and credential.'
        ),
        'north_america_access': (
            'Appleton Estate widely distributed in the US through Campari Group (which acquired '
            'the J. Wray & Nephew parent company in 2012); available in Canada through BCLDB, '
            'LCBO, SAQ; 21-Year pricing at USD $80–110 retail; Signature Blend and 8-Year '
            'available in mainstream liquor retail across North America.'
        ),
        'culinary_application': (
            'Appleton Estate 21-Year is the PCT\'s Jamaican rum anchor: the British colonial '
            'heritage of Jamaica (Royal Navy rum provisioning, 1749 documented estate record), '
            'the African diaspora labor history of the Nassau Valley plantation system, and '
            'the continuation of the pot still tradition that preserves Jamaican rum\'s '
            'highest-ester character through Joy Spence\'s blending philosophy creates the '
            'complete narrative for a PCT West African Diaspora Trail spirits programme.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
