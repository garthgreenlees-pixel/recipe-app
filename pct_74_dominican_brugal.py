import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Dominican Republic — Santiago and Puerto Plata (Brugal Añejo 1888 Doble Añejamiento, Caribbean Rum, Column-Still Dry Style)',
    output_dir='.',
    starting_entry=1,
    session_number=78,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Brugal y Cía — Puerto Plata, Dominican Republic',
    'location': 'Puerto Plata, Dominican Republic',
    'description': (
        'Brugal is the dominant rum producer of the Dominican Republic, '
        'founded in 1888 by Don Andres Brugal Montaner, a Catalan immigrant '
        'from Sitges, Spain, who established the distillery in Puerto Plata '
        'on the northern coast of Hispaniola. Brugal is the most consumed '
        'rum in the Dominican Republic by a significant margin — the brand '
        'occupies in the DR the same relationship to the national rum '
        'identity that Bacardí holds in Cuba or Angostura in Trinidad. '
        'The house style is the "Dominican dry" — column-still distillation '
        'to high purity, light body, and deliberate avoidance of the heavy '
        'ester and molasses character of Jamaican or Barbadian pot-still rum; '
        'the Brugal production philosophy prioritizes structural cleanliness '
        'and refinement over raw tropical character. The 1888 Doble '
        'Añejamiento (double aging) expression is the premium tier of the '
        'Brugal range, named for the founding year and using a two-stage '
        'aging approach in American white oak bourbon barrels followed by '
        'sherry-seasoned casks — the double aging producing a more complex, '
        'darker, richer rum than the standard Brugal Añejo without departing '
        'from the house\'s fundamental dry and clean column-still character.'
    ),
    'founded': '1888',
    'region': 'Puerto Plata, Dominican Republic',
    'website': 'brugal-rum.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Edrington Group / William Grant & Sons (Brugal US and Canada distribution)',
    'type': 'importer',
    'description': (
        'Brugal was acquired by the Edrington Group (Scotland) in 2008 — '
        'the same group that owns Macallan and Highland Park Scotch. '
        'William Grant & Sons handles Brugal distribution in the United '
        'States and Canada. Brugal 1888 is widely available at BCLDB BC '
        'and LCBO Ontario at CAD $45–65 per 750ml — one of the more '
        'accessible premium rum expressions in the Canadian market. '
        'In the United States, William Grant distributes Brugal 1888 '
        'nationally through fine spirits retailers at USD $35–50 per '
        '750ml. The brand has strong market penetration in the '
        'Dominican community in New York and Miami, and is the '
        'rum most associated with the Dominican Republic in '
        'North American spirits retail.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Dominican Republic'],
    'traditions_carried': ['spirits'],
    'website': 'brugal-rum.com',
    'verified': True
})

session.add_beverage({
    'name': (
        'Brugal 1888 Doble Añejamiento — Dominican Republic Column Still, '
        'Double Aging Bourbon and Sherry Cask, Puerto Plata'
    ),
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Dominican Republic',
    'region': 'Dominican Republic — Santiago and Puerto Plata (Brugal Añejo 1888 Doble Añejamiento, Caribbean Rum, Column-Still Dry Style)',
    'producer': 'Brugal y Cía — Puerto Plata, Dominican Republic',
    'alcohol_content': 40.0,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'The Dominican Republic occupies the eastern two-thirds of Hispaniola, '
        'the second-largest Caribbean island, between Cuba to the west and '
        'Puerto Rico to the east. Brugal\'s operations span the northern coast '
        'from Puerto Plata (the primary distillery and bonded warehouses) '
        'to Santiago de los Caballeros (the largest inland city of the DR '
        'and the agricultural hub of the Cibao Valley where sugarcane '
        'cultivation historically concentrated). The Dominican sugar '
        'industry developed under Spanish colonial rule in the 16th '
        'century and expanded under US occupation (1916–1924), which '
        'modernized Dominican sugar infrastructure and oriented '
        'production toward export markets. The Cibao Valley is the '
        'primary Dominican sugarcane growing zone — a broad, '
        'fertile lowland between the Cordillera Septentrional to '
        'the north and the Cordillera Central to the south at '
        '50–200m elevation, with a humid tropical climate '
        '(1,500–2,000mm annual rainfall) and volcanic alluvial soils '
        'that produce high-yield sugarcane with moderate sucrose '
        'concentration. The northern coastal climate at Puerto Plata '
        '(where Brugal\'s aging warehouses are located) is influenced '
        'by the Atlantic trade winds, moderating temperatures to '
        '24–28°C year-round — a slightly cooler aging environment '
        'than Jamaica or Barbados warehouses, which contributes to '
        'the slower, more refined barrel aging character of '
        'Dominican rum versus faster-maturing tropical rums '
        'in warmer aging environments.'
    ),
    'production_technique': (
        'Brugal production begins with blackstrap molasses from Dominican '
        'Republic sugar mills — the residual byproduct of crystallized '
        'sugar extraction, containing approximately 35–40% fermentable '
        'sugar and the complex flavor compounds that survive the sugar '
        'extraction process. The molasses is diluted with water to '
        'approximately 25 Brix and fermented with the Brugal house '
        'yeast strain for 24–48 hours (a short fermentation by '
        'Caribbean rum standards — versus 3–5 days for Jamaican '
        'heavy rum) at 28–32°C, producing a wine of 7–9% ABV '
        'with low ester development (under 100 g/100L of pure alcohol) '
        'relative to the high-ester Jamaican marque production. '
        'The fermented molasses wine is distilled in continuous '
        'column stills (Coffey still design) to 95–96% ABV — '
        'a very high distillation proof that strips the majority '
        'of congeners and volatile flavor compounds to produce '
        'the light, clean, neutral spirit base that characterizes '
        'the Dominican/Cuban rum style versus the heavier '
        'pot-still or low-proof column-still production of '
        'Jamaica and Barbados. The 95–96% ABV distillate is '
        'diluted to 65–70% ABV for barrel entry. For the 1888 '
        'Doble Añejamiento, the production follows a two-stage '
        'aging programme: Stage 1 — American white oak ex-bourbon '
        'barrels (180–200L) for 3–5 years in the Puerto Plata '
        'warehouse, developing vanilla, caramel, and light oak '
        'character from the charred oak staves; Stage 2 — the '
        'partially aged rum is transferred to sherry-seasoned '
        'casks (Pedro Ximénez and Oloroso seasoned 225L barrels) '
        'for an additional 2–4 years of finishing, adding dried '
        'fruit, spice, and the characteristic dark sweetness of '
        'sherry cask influence. After double aging, the 1888 is '
        'blended by the Brugal master distiller (currently Jassil '
        'Villanueva, the fourth-generation family member directing '
        'production) from multiple barrel lots to achieve the '
        'consistent house profile before dilution to 40% ABV '
        'and bottling.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Diplomatico Reserva Exclusiva (Venezuela column-still, double cask finishing)',
            'connection': (
                'Brugal 1888 and Diplomatico Reserva Exclusiva represent '
                'the same quality philosophy in Spanish Caribbean rum '
                'production: column-still base spirit aged in American '
                'white oak bourbon barrels with sherry cask finishing to '
                'add dried fruit and complexity to the clean column-still '
                'foundation. Both houses prioritize the refined, dry, '
                'structural character of high-proof column distillation '
                'over the heavy ester and funk of pot-still production; '
                'both use sherry cask finishing as the premium quality '
                'tier differentiation. Diplomatico is sweeter '
                '(higher residual sugar addition) than Brugal 1888; '
                'Brugal 1888 is drier and more structurally austere — '
                'the two represent the "dry" and "rich" poles of '
                'the Spanish Caribbean premium rum style.'
            )
        },
        {
            'tradition': 'Bacardí Reserva Ocho (Cuba column-still, 8-year, clean dry style)',
            'connection': (
                'Brugal 1888 and Bacardí Reserva Ocho are the direct '
                'historical and stylistic parallels within the Spanish '
                'Caribbean dry rum tradition — both produced on the same '
                'island chain (Hispaniola/Cuba), both using continuous '
                'column distillation to high purity, and both representing '
                'the founding family\'s premium aged tier. The Cuban '
                'dry style (Bacardí) and the Dominican dry style (Brugal) '
                'share a common heritage in the Spanish colonial rum '
                'production tradition of the Greater Antilles — both '
                'use column distillation to high ABV, short fermentation '
                'with low ester development, and American oak aging '
                'to produce a structurally refined, dry spirit '
                'that contrasts with the heavier, funkier rums '
                'of the English Caribbean tradition.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber-mahogany with red-brown highlights — the color '
            'of double aging in ex-bourbon and sherry casks at 5–9 '
            'total years in barrel; darker than standard Brugal Añejo '
            '(3 years in ex-bourbon only) due to the additional '
            'sherry cask color and tannin extraction; brilliant '
            'clarity from chill filtration before bottling; '
            'medium legs from 40% ABV with no residual sugar '
            'additions.'
        ),
        'nose': (
            'Vanilla and toasted caramel from the ex-bourbon cask '
            'stage as the immediate aromatic register; dried fruit '
            '(raisin, dried plum, fig) from the PX sherry cask '
            'finishing overlaid on the bourbon oak base; dark '
            'chocolate and coffee from the deeper barrel extraction '
            'at the sherry cask stage; beneath the cask character, '
            'the clean column-still molasses spirit provides a '
            'subtle background of sugarcane and brown sugar; '
            'the Dominican house style is perceptible in '
            'the relative dryness and structural cleanliness '
            'of the aromatic base — no heavy ester or '
            '"funky" volatile compounds from the short '
            'Dominican fermentation; warm baking spice '
            '(cinnamon, clove) from the sherry cask '
            'extraction at the top of the aromatic register.'
        ),
        'palate': (
            'Full body from the double cask aging extract; dry '
            'to off-dry entry (no residual sugar additions — '
            'the sweetness perception from oak tannin and '
            'sherry cask extract rather than added sugar); '
            'vanilla and caramel from the bourbon oak '
            'through the entry; dried fruit and dark '
            'chocolate from the sherry finishing through '
            'the mid-palate; warm cinnamon and clove spice '
            'building on the long finish; 40% ABV providing '
            'a clean heat without sharpness; the column-still '
            'distillate base is perceptible in the clean, '
            'structural quality of the spirit beneath '
            'the cask character — distinguishing 1888 '
            'from heavy pot-still Caribbean rum at '
            'the same aging level.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Brugal Especial Blanco / Brugal Extra Dry (unaged, column-still house style)',
            'criteria': (
                'Unaged or lightly filtered column-still Dominican rum '
                'showing the clean, neutral, high-purity base spirit '
                'character of Brugal without barrel influence; the '
                'entry point for the Dominican dry house style; '
                'the benchmark unaged column-still rum for mixing '
                'and cocktail use in the Dominican and Caribbean '
                'tradition.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Brugal Añejo (single-stage bourbon cask aging, 3-5 years)',
            'criteria': (
                'Standard Brugal Añejo aged 3–5 years in ex-bourbon '
                'American white oak barrels; vanilla, caramel, and '
                'light wood tannin from single-stage aging; the '
                'domestic Dominican market standard for Brugal '
                'sipping rum; cleaner and lighter than the '
                '1888 double-aged expression; the baseline '
                'for the Brugal house style comparison.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Brugal 1888 Doble Añejamiento (double cask, premium tier)',
            'criteria': (
                'Double aging in ex-bourbon and sherry casks for '
                '5–9 total years; the premium domestic and export '
                'tier of the Brugal range; dried fruit, dark '
                'chocolate, and spice from the sherry finishing '
                'added to the vanilla-caramel bourbon base; '
                'the benchmark expression for the Dominican '
                'dry rum style at collector and trade level.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Brugal Extra Viejo / Leyenda (extended aging, ultra-premium)',
            'criteria': (
                'Extended multi-cask aging at 10–15+ years; the '
                'apex of Brugal production complexity with maximum '
                'dried fruit, rancio, and vanilla-spice cask '
                'character; Brugal Leyenda is the collector and '
                'gifting tier of the Dominican dry rum tradition; '
                'limited production and premium pricing of '
                'USD $80–150 per 750ml reflects the extended '
                'barrel space and the hand-selection of '
                'exceptional lot barrels by the master distiller.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Brugal 1888 neat at room temperature (20–22°C) '
            'in a rocks glass without ice — the full barrel-extract '
            'complexity (vanilla, dried fruit, cacao) is best '
            'expressed at room temperature where the volatile '
            'aromatic compounds from the double-cask aging are '
            'fully open; a single large ice cube (if preferred) '
            'reduces the serving temperature to 14–16°C and '
            'slightly slows the aromatic volatilization without '
            'eliminating the sherry cask dried fruit character; '
            'avoid heavy dilution with water which strips the '
            'structural column-still base that distinguishes '
            'Dominican dry rum from more aromatic pot-still '
            'Caribbean spirits.'
        ),
        'vessel': (
            'Serve in a Glencairn whisky glass or a tulip-format '
            'spirits nosing glass (100–150ml) with 45–60ml pour '
            'for sipping service; the Glencairn concentrates '
            'the vanilla-dried fruit aromatics at the chimney '
            'aperture and is the professional standard for '
            'comparative rum tasting; for cocktail service, '
            'serve 60ml Brugal 1888 over a single large ice '
            'rock in an Old Fashioned glass as the Dominican '
            'equivalent of the bourbon Old Fashioned — '
            'the double-cask character provides the complexity '
            'to carry the cocktail format without additional '
            'sweetener, consistent with the Brugal dry house '
            'style philosophy.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Brugal y Cía — Puerto Plata, Dominican Republic (1888; '
            'the definitive Dominican rum producer and the reference '
            'for the Caribbean column-still dry style in the '
            'Greater Antilles tradition; 1888 Doble Añejamiento '
            'is the benchmark double-cask Dominican rum expression '
            'and the reference point for North American trade '
            'buyers assessing the Dominican rum category).'
        ),
        'north_america_access': (
            'Brugal 1888 is distributed through William Grant & Sons '
            'nationally in the United States at USD $35–50 per 750ml — '
            'excellent value for the complexity of the double-cask '
            'aging at this price. In Canada, BCLDB BC and LCBO Ontario '
            'carry Brugal 1888 on regular allocation at CAD $45–65. '
            'The brand has strong presence in the Dominican and '
            'Latin Caribbean communities in New York, New Jersey, '
            'and Miami; for professional spirits programme buyers, '
            '1888 is the essential Dominican rum in a Caribbean '
            'rum comparison flight alongside Jamaican (Appleton '
            'Estate), Barbadian (Mount Gay), and Trinidadian '
            '(Angostura 1824) expressions.'
        ),
        'culinary_application': (
            'Brugal 1888 is the Dominican republic\'s pairing rum '
            'for sancocho (the national stew of 7 meats and '
            'tropical root vegetables) and for pernil (roasted '
            'pork shoulder marinated in citrus and garlic) — '
            'the dried fruit and cacao complexity of the 1888 '
            'double aging creates a flavour bridge to roasted '
            'pork and concentrated stew that lighter unaged '
            'rum cannot achieve. In a professional programme '
            'context, Brugal 1888 is the rum selection '
            'for a cacao or chocolate dessert course — '
            'the PX sherry finishing contributes the '
            'dried fruit and dark chocolate register '
            'that makes it a natural complement to '
            '70–80% single-origin dark chocolate.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
