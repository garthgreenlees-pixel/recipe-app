import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Puerto Rico — San Juan Karst (Bacardí Reserva Ocho, Limestone Aquifer, Molasses Column Still)',
    output_dir='.',
    starting_entry=1,
    session_number=54,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Bacardí Corporation — Cataño, Puerto Rico',
    'location': 'Cataño, San Juan Bay, Puerto Rico',
    'description': (
        'Bacardí Corporation operates the world\'s largest rum distillery at Cataño, on the southern '
        'shore of San Juan Bay in Puerto Rico, producing more than 100,000 barrels of rum annually '
        'across the full Bacardí range. The Bacardí family fled Cuba in 1960 following nationalization '
        'of their original 1862 Santiago de Cuba distillery and established the primary production '
        'operations in Cataño, which had operated as a Bacardí facility since 1936. The Cataño '
        'distillery is one of the most visited tourist attractions in the Caribbean, receiving '
        'approximately 500,000 visitors annually. The Bacardí Reserva Ocho (8-year aged) is the '
        'premium sipping expression positioned against aged Cuban ron and premium Caribbean rums '
        'in the international luxury spirits category, produced from Puerto Rican molasses in '
        'column stills following the original Cuban light-style method that founder Facundo Bacardí '
        'Massó developed in Santiago de Cuba in 1862.'
    ),
    'founded': '1862 (Santiago de Cuba); Cataño facility 1936',
    'region': 'Cataño, San Juan Bay, Puerto Rico',
    'website': 'bacardi.com',
    'verified': True
})

session.add_beverage({
    'name': 'Bacardí Reserva Ocho — Puerto Rico Limestone Aquifer, San Juan Karst, 8-Year Column Still Aged',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Puerto Rico',
    'region': 'Puerto Rico — San Juan Karst (Bacardí Reserva Ocho, Limestone Aquifer, Molasses Column Still)',
    'producer': 'Bacardí Corporation — Cataño, Puerto Rico',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Puerto Rico is a limestone-dominated island in the northeastern Caribbean, the easternmost '
        'of the Greater Antilles, situated between Hispaniola to the west and the Virgin Islands '
        'to the east at approximately 18°N latitude. The geological foundation of Puerto Rico is '
        'an uplifted limestone karst terrain — the northern coastal plain, where Cataño and San Juan '
        'are located, sits atop a thick Tertiary limestone formation pocked with sinkholes, caves, '
        'and underground river systems. The San Juan metropolitan area\'s water supply derives '
        'substantially from this limestone aquifer, filtered through Cenozoic carbonate rock to '
        'produce mineral-balanced, slightly alkaline water used in rum proofing and production. '
        'The Bacardí Cataño facility sits at sea level on San Juan Bay — directly exposed to the '
        'northeast trade winds that blow across the Atlantic from Africa at 15–25 knots year-round, '
        'moderating the tropical temperatures (24–28°C average) and maintaining the constant '
        'airflow through the aging warehouses that affects how the ex-bourbon barrels breathe '
        'and how the angel\'s share evaporates. Puerto Rico\'s tropical maritime climate (1,400–1,800mm '
        'annual rainfall, concentrated in the summer hurricane season) is similar to Cuba\'s western '
        'zone and produces comparable tropical aging acceleration. Puerto Rico\'s status as a US '
        'territory exempts Bacardí from the US rum tariff and allows the Cataño operation to supply '
        'the US market — the world\'s largest rum consumer — from a Caribbean production base '
        'without import duty complications that affect Cuban, Barbadian, or Jamaican competitors.'
    ),
    'production_technique': (
        'Bacardí Reserva Ocho is produced at Cataño using the column still light-style method '
        'that Facundo Bacardí Massó invented and refined in Santiago de Cuba: distillation to '
        'high proof (90–95% ABV) in large-capacity continuous column stills, followed by charcoal '
        'filtration to remove heavier congeners, and aging in American white oak ex-bourbon barrels. '
        'The Reserva Ocho specifically designates an 8-year minimum aging in a selected set of '
        'ex-bourbon barrels from the Bacardí aging warehouses at Cataño. The charcoal filtration '
        'step — a technical signature of the Bacardí method dating from 1862 — uses activated '
        'charcoal to selectively remove specific sulfur compounds and heavier fusel alcohols from '
        'the distillate after distillation and before barrel entry, contributing to the exceptional '
        'clarity and aromatic cleanness of the Bacardí column still spirit base. This filtered, '
        'high-proof spirit base enters new and previously used ex-bourbon American white oak barrels '
        'for 8 years of tropical aging at Cataño: the northeast trade winds and consistent Caribbean '
        'temperatures drive barrel respiration at accelerated rates (5–8% angel\'s share annually), '
        'concentrating the vanilla, caramel, and dried fruit compounds extracted from the charred '
        'American oak interior. The Reserva Ocho is finished with a small addition of the Bacardí '
        'proprietary "reserva" blend — aged distillate reserves from the oldest stocks in the '
        'Cataño warehouse — that adds depth without compromising the clean column-still foundation. '
        'Final proofing to 40% ABV with Puerto Rico limestone aquifer water; no caramel colouring '
        'added to the Reserva Ocho expression — the amber-gold colour is entirely from 8 years '
        'of ex-bourbon barrel contact in tropical Puerto Rican conditions.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Jack Daniel\'s Tennessee Whiskey (charcoal filtering before barrel aging)',
            'connection': (
                'Bacardí Reserva Ocho and Jack Daniel\'s Tennessee Whiskey are the two most prominent '
                'expressions of the charcoal filtration principle applied before barrel aging — '
                'Jack Daniel\'s Lincoln County Process filters new-make corn whiskey through '
                '10 feet of sugar maple charcoal before barrel entry; Bacardí filters the column '
                'still rum distillate through activated charcoal before barrel entry. Both achieve '
                'the same technical goal: selective removal of heavier congeners that would '
                'produce off-notes during barrel aging, creating a cleaner, lighter spirit base '
                'that allows the oak contact to express without interference from sulfur compounds '
                'or heavy fusel alcohols.'
            )
        },
        {
            'tradition': 'Ron Havana Club 7 Años (Cuban light-style, same colonial tradition)',
            'connection': (
                'Bacardí Reserva Ocho and Havana Club Añejo 7 Años are the two competing heirs '
                'of the Cuban light-style ron tradition developed by Facundo Bacardí Massó in '
                '1862 Santiago de Cuba: after the 1960 Cuban nationalization, the Bacardí family '
                'took their production method to Puerto Rico while Cuba Ron S.A. continued the '
                'state version of the tradition in Havana. Both use column distillation, charcoal '
                'treatment, ex-bourbon barrel aging, and maestro ronero blending philosophy — '
                'making the 8-year Bacardí and 7-year Havana Club the most direct technical '
                'parallels in the global rum market, divided only by the US embargo politics '
                'that prevent direct side-by-side comparison in US retail channels.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Warm amber-gold; 8 years of ex-bourbon barrel aging in Puerto Rico\'s tropical coastal '
            'conditions produces a deeper colour than equivalent temperate-climate aging; brilliant '
            'clarity from the charcoal filtration step; moderate legs at 40% ABV.'
        ),
        'nose': (
            'Clean and aromatic from the charcoal filtration foundation: vanilla from the charred '
            'ex-bourbon American oak dominates; caramelized brown sugar from the molasses base '
            'transformed through 8 years of tropical oak contact; dried apricot and light banana '
            'from ester development; a faint almond and marzipan quality from the charcoal-filtered '
            'column spirit interacting with the oak compounds over extended tropical aging; '
            'the Bacardí signature of exceptional aromatic cleanliness and precision that '
            'distinguishes it from heavier congener Caribbean rums.'
        ),
        'palate': (
            'Light to medium body — the Bacardí column still method produces a thinner, drier '
            'spirit texture than pot still or blended column-pot styles; the vanilla and caramel '
            'from the ex-bourbon oak arrive cleanly on the attack; the 8-year aging gives the '
            'dried fruit depth absent from the standard Bacardí Superior; medium-length finish '
            'with oak spice and light toffee; the charcoal filtration\'s legacy shows as an '
            'exceptional cleanness through the finish — no off-notes, no sulfur, no harshness '
            'at the back-palate despite 40% ABV.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Bacardí Superior (white, charcoal filtered)',
            'criteria': (
                'The world\'s best-selling white rum: column distilled, charcoal filtered, minimally '
                'aged (1–2 years) then filtered clear — the foundational Mojito and Daiquiri base '
                'rum that has defined the category globally since the 1960s, serving the '
                'cocktail trade where neutral, clean, light character is required.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Bacardí Gold (4-year, light amber)',
            'criteria': (
                'Four-year ex-bourbon aged and lightly charcoal filtered: the intermediate tier '
                'between the white and the Reserva Ocho, showing initial vanilla and caramel '
                'development without the full 8-year complexity — the Cuba Libre and rum punch '
                'premium tier at accessible pricing.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Bacardí Reserva Ocho (8-year aged)',
            'criteria': (
                'The premium flagship: 8-year tropical Caribbean aging in ex-bourbon American oak, '
                'the charcoal-filtered column still spirit base expressing maximum vanilla-caramel-dried '
                'fruit complexity — the reference expression for understanding the Bacardí light-style '
                'philosophy applied to aged sipping rum at international quality level.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Bacardí Facundo Neo / Paraíso (limited ultra-aged)',
            'criteria': (
                'The Facundo collection — ultra-aged expressions from Bacardí\'s oldest barrel '
                'reserves, including Neo (unaged white from the finest column still cuts) and '
                'Paraíso (23-year-average aged blend) — representing the apex of the Bacardí '
                'production philosophy at collector-level pricing and complexity, positioned '
                'directly against the finest aged Cognac and single malt Scotch.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Reserva Ocho at 18–20°C neat for full appreciation of the 8-year ex-bourbon '
            'character; the Puerto Rico trade wind climate means the warehouse angels\' share '
            'was taken at ambient Caribbean temperatures — serve in the same temperature '
            'range to approximate the production environment; a single 30mm ice sphere '
            'reduces to 12–14°C for a more casual sipping context without rapid dilution; '
            'for a premium Daiquiri using the Reserva Ocho as base (displacing Superior), '
            'serve the final cocktail at 4–6°C in a chilled coupe.'
        ),
        'vessel': (
            'Tulip or copita for neat evaluation of the clean column-still aromatics; rocks '
            'glass with a large sphere for relaxed sipper service; the Reserva Ocho is '
            'versatile enough for a premium Rum Old Fashioned (Reserva Ocho, demerara sugar '
            'syrup, aromatic bitters, orange peel) served in a wide rocks glass over a large '
            'ice cube — a build that demonstrates how the 8-year aged character positions '
            'Puerto Rican light-style rum in the same service register as bourbon.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Bacardí Corporation (Cataño, Puerto Rico) — Reserva Ocho is the premium sipping '
            'reference for the light-style column still Caribbean rum; globally the most '
            'distributed premium rum brand; the PCT canonical expression for Puerto Rican '
            'rum and for the Bacardí family\'s historic Cuban-to-Puerto Rico production migration.'
        ),
        'north_america_access': (
            'Bacardí Reserva Ocho widely available in all US states and Canadian provinces '
            'through BCLDB, LCBO, SAQ, and all major liquor retail networks; pricing '
            'USD $25–35 in the US, CAD $38–48 in Canada; the Facundo collection requires '
            'specialty retailer or allocation access at USD $80–250+ depending on expression.'
        ),
        'culinary_application': (
            'The Reserva Ocho is the premium rum anchoring a PCT Caribbean spirits flight: '
            'its Puerto Rico US-territory status, Cuban colonial heritage, and family exile '
            'narrative connect the PCT colonial trade network to the 20th-century political '
            'geography of Caribbean rum through the embargo that separated the Cuban original '
            'from its Puerto Rican successor.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
