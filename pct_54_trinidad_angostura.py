import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Trinidad — Caroni Estate Region (Angostura 1919, Sugarcane Northeast Coast, Coffey Still Column)',
    output_dir='.',
    starting_entry=1,
    session_number=58,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Angostura Ltd — Port of Spain, Trinidad',
    'location': 'Laventille, Port of Spain, Trinidad',
    'description': (
        'Angostura Ltd is Trinidad\'s primary rum producer and the company that manufactures the globally '
        'ubiquitous Angostura Aromatic Bitters — a product whose presence in virtually every bar in the '
        'world has made the Angostura name more widely recognized than any other spirits company brand. '
        'Founded in 1824 in Angostura (now Ciudad Bolívar, Venezuela) by German physician Johann Gottlieb '
        'Benjamin Siegert as a medicinal stomach bitters, the company relocated to Port of Spain, Trinidad '
        'in 1875 after Venezuelan political instability made operations untenable. Angostura Ltd produces '
        'the Angostura rum range — including the 1919, 1824, and aged expressions — using large Coffey '
        'continuous column stills operated from the House of Angostura complex at Laventille on the '
        'outskirts of Port of Spain, while maintaining the bitters production that funds the rum operation '
        'and connects the Trinidadian rum narrative to the PCT pisco-to-bitters connection in the '
        'classic Pisco Sour cocktail.'
    ),
    'founded': '1824 (Venezuela); Trinidad operations from 1875',
    'region': 'Laventille, Port of Spain, Trinidad',
    'website': 'angostura.com',
    'verified': True
})

session.add_beverage({
    'name': 'Angostura 1919 Rum — Trinidad Caroni Coast, Coffey Still Column, Oloroso Sherry Cask Aged',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Trinidad',
    'region': 'Trinidad — Caroni Estate Region (Angostura 1919, Sugarcane Northeast Coast, Coffey Still Column)',
    'producer': 'Angostura Ltd — Port of Spain, Trinidad',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Trinidad is the southernmost island of the Caribbean Lesser Antilles, located just '
        '11km from the Venezuelan mainland coast and geologically distinct from the other '
        'Caribbean islands: unlike the volcanic islands to the north and the coral limestone '
        'of Barbados, Trinidad is a continental fragment that separated from the South American '
        'mainland, with geological formations including the Northern Range (folded sedimentary '
        'and metamorphic rock reminiscent of South American geology) rising to 940m in the '
        'northeast, and the broad coastal plains of the south and west where sugarcane '
        'cultivation concentrated during the colonial era. The Caroni Estate district — '
        'the historic sugarcane growing region in the southeast of Trinidad, named for the '
        'Caroni River that flows through the cane plains to the Gulf of Paria — was the '
        'heart of the British colonial sugar plantation system in Trinidad and the location '
        'of the Caroni Distillery, which operated from 1918 until its controversial closure '
        'in 2003 (a decision that has been widely criticized by rum connoisseurs who '
        'identified the distinctive heavy, funky Caroni heavy rum style as one of the most '
        'unique in the Caribbean). The Caroni Swamp, immediately south of the Caroni Estate '
        'cane fields, is one of the largest mangrove ecosystems in the Caribbean, creating '
        'the ecological backdrop for the Trinidadian sugarcane agriculture zone. Angostura\'s '
        'Laventille distillery draws molasses from the remaining Trinidadian sugar industry, '
        'supplemented by regional Caribbean molasses, for fermentation and Coffey still '
        'column distillation — maintaining the Trinidadian rum production tradition in '
        'an entirely continuous-column-still format after the closure of the Caroni pot '
        'still operation.'
    ),
    'production_technique': (
        'Angostura 1919 is produced exclusively from Coffey continuous column still distillation '
        '— the large-scale Angostura columns at Laventille producing a lighter, more aromatic '
        'spirit at 85–90% ABV compared to the heavier Caroni pot still expression. The '
        'Coffey still (invented by Aeneas Coffey, an Irish excise officer, in 1831) uses two '
        'connected columns — the analyzer and the rectifier — through which steam strips '
        'alcohol from the fermented wash in the analyzer, and the rectifier column concentrates '
        'and purifies the alcohol vapor to the desired proof. Angostura\'s specific Coffey still '
        'configuration and cut point management produces a clean, aromatic spirit with moderate '
        'ester content that the master blender Loretta Butler-Thomas shapes into the 1919 '
        'expression. The name 1919 commemorates the year a fire destroyed most of the '
        'Angostura aging warehouse stocks, leaving only the barrels that had been aging for '
        '8 years or more — the company turned the disaster into a brand narrative by releasing '
        'the surviving aged rum as a premium expression. The 1919 is aged in American white '
        'oak ex-bourbon barrels for a primary aging of 8–10 years in the Laventille warehouses, '
        'followed by a secondary maturation period of 6–12 months in ex-Oloroso sherry casks '
        '— the same sherry-finishing approach used by Foursquare/Doorly\'s in Barbados, '
        'demonstrating the Caribbean-wide adoption of the sherry cask finishing technique '
        'as the primary premium differentiation tool in the aged rum category. Final proofing '
        'to 40% ABV with Trinidad water; no added sugar or caramel colouring in the 1919 expression.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Angostura Aromatic Bitters (Trinidad, same production house)',
            'connection': (
                'Angostura 1919 rum and Angostura Aromatic Bitters are produced at the same '
                'House of Angostura complex in Laventille, Trinidad — creating the unique '
                'PCT connection that the bitters that complete the classic Pisco Sour cocktail '
                '(the drink that connects Peru to Haiti in the pct_46 entry) and the rum that '
                'anchors the Trinidadian arm of the West African Diaspora Trail are produced '
                'by the same company on the same site. The aromatic bitters formula incorporates '
                'gentian, cinnamon, clove, and other botanical compounds that overlap with '
                'the aromatic profile developed in aged Trinidad rum — the terroir of the '
                'Angostura botanical sourcing connecting the medicine heritage of 1824 '
                'Venezuela to the colonial rum tradition of 1875 Trinidad.'
            )
        },
        {
            'tradition': 'Highland Scotch (Dalmore, sherry-finished column-still base)',
            'connection': (
                'Angostura 1919 sherry finish and the Dalmore Highland single malt (which uses '
                'Matusalem, Apostoles, and Gonzalez Byass sherry casks for extensive finishing) '
                'both represent the principle of secondary Oloroso sherry maturation applied '
                'to a spirit whose primary character was established in American ex-bourbon oak: '
                'both achieve the dried fruit, walnut, and raisin complexity that sherry wood '
                'uniquely contributes, layered over an American oak vanilla-caramel foundation — '
                'the Trinidadian Coffey still spirit and the Scottish pot still spirit reaching '
                'comparable aromatic profiles through equivalent finishing methodology despite '
                'their entirely different geographic, agricultural, and distillation origins.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Medium-deep amber with sherry-influenced red-brown tints from the Oloroso cask '
            'finishing; clear and brilliant; moderate legs at 40% ABV indicating standard '
            'glycerol content from the column still production.'
        ),
        'nose': (
            'The sherry cask finish establishes the primary aromatic character: dried Medjool '
            'dates, raisin, and walnut from the Oloroso wood compounds; beneath the sherry '
            'influence, the Angostura Coffey still base contributes aromatic freshness '
            'and tropical fruit from the moderate ester level of the column distillate; '
            'vanilla and caramel from the primary American ex-bourbon oak aging; a '
            'specific warm spice register from the Angostura production site proximity '
            'to the bitters botanical formulation — though the bitters and rum are '
            'technically separate products, the aromatic vocabulary of warm spice, '
            'dried fruit, and gentle bitterness connects the two as complementary '
            'expressions of the same Trinidadian production tradition.'
        ),
        'palate': (
            'Medium body from the Coffey still column base; the sherry cask finish delivers '
            'dried fruit and walnut on the attack; the primary American oak vanilla and '
            'caramel through the mid-palate; warm at 40% ABV with moderate structure '
            'from the Oloroso tannin; medium-long finish with dried fruit, the '
            'residual sherry wood bitterness, and the tropical-fruit-and-caramel '
            'character of the Coffey still base persisting to a clean, dry conclusion '
            '— a well-crafted Trinidadian column-still rum that demonstrates how '
            'sherry cask finishing bridges the lightness of column distillation with '
            'the richness required for premium neat service.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Angostura White Oak (unaged)',
            'criteria': (
                'Unaged white Trinidad column still rum: the clean Coffey still distillate '
                'without barrel aging contribution — the cocktail base tier for Trinidadian '
                'rum in mixed drink applications where a neutral, high-proof column still '
                'spirit is required.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Angostura 5-Year (light aged)',
            'criteria': (
                'Five-year ex-bourbon barrel aged: initial vanilla and caramel from American '
                'oak, the Coffey still lightness preserved, no sherry cask finishing — '
                'the accessible premium tier for sipping and mixing where the full '
                '1919 sherry complexity is not required.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Angostura 1919 (8-year, sherry finish)',
            'criteria': (
                'The 1919 flagship: 8-year primary American oak aging plus Oloroso sherry '
                'cask finishing, the fire-of-1919 heritage narrative, the benchmark for '
                'Trinidadian Coffey still aged rum with secondary maturation — the '
                'reference expression for the Caribbean sherry-finish rum category '
                'at premium price positioning.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Angostura 1824 (12-year, limited)',
            'criteria': (
                'The 1824 heritage expression named for the Angostura company founding year: '
                '12-year aged Trinidad column still rum with maximum sherry cask influence, '
                'the apex of the Angostura rum range; deep sherry-derived complexity '
                'demonstrating the full potential of Trinidad Coffey still production '
                'given extended dual-cask maturation.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Angostura 1919 at 18–20°C for neat evaluation; the sherry cask character '
            'shows best at ambient temperature where the dried fruit and walnut volatile '
            'compounds are active; a single ice sphere reduces to 12–14°C for relaxed '
            'sipper service; the 1919 is excellent in a Trinidad Rum Punch (rum, lime, '
            'sugar, water, and Angostura Aromatic Bitters — the only cocktail in the '
            'canon where the bitters and the rum are produced by the same company '
            'on the same site) served over ice in a highball at 6–8°C.'
        ),
        'vessel': (
            'Tulip or Glencairn for neat evaluation; rocks glass for casual service; '
            'highball for the Trinidad Rum Punch; the PCT narrative moment is to serve '
            'the 1919 neat alongside a small dipping bowl of the 1824 bitters — '
            'demonstrating visually how the bitter botanical compound that completes '
            'every classic cocktail and the aged rum that forms the premium spirit '
            'of Trinidad share a production home in the House of Angostura at Laventille.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Angostura Ltd (Laventille, Port of Spain, Trinidad) — producer of both the '
            '1919 rum and the Aromatic Bitters that appear in virtually every classic '
            'cocktail recipe globally; the 1919 is the Trinidadian rum benchmark and '
            'the PCT\'s most narratively connected expression given the bitters-rum '
            'dual-production significance.'
        ),
        'north_america_access': (
            'Angostura 1919 widely distributed in the US and Canada through spirits '
            'importers with Caribbean focus; Angostura Bitters available in every '
            'grocery and liquor store in North America; 1919 pricing at USD $30–45 '
            'retail; the 1824 limited expression at USD $50–70 through specialty retailers.'
        ),
        'culinary_application': (
            'Angostura 1919 is the PCT Pisco Sour connection point made material: the '
            'bitters that complete the Peruvian pisco sour (see pct_35) come from the '
            'same Trinidadian company that produces Trinidad\'s premier aged rum — '
            'serving both together at a PCT-themed evening creates the most condensed '
            'demonstration of the PCT colonial trade network\'s geographic reach from '
            'Peru to Venezuela to Trinidad in a single spirits pairing.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
