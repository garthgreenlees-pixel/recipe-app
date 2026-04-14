import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Cuba — Santiago de Cuba (Ron Santiago de Cuba, Eastern Province, Colonial Cane Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=53,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Cuba Ron S.A. — Santiago de Cuba Distillery',
    'location': 'Santiago de Cuba, Oriente Province, Cuba',
    'description': (
        'Cuba Ron S.A. is the state-owned corporation managing all Cuban rum production following '
        'nationalization of the spirits industry after the 1959 Revolution. The Santiago de Cuba '
        'distillery — one of the oldest operating rum facilities in Cuba — produces the Santiago '
        'de Cuba brand expressions from eastern Cuban sugarcane, a tradition with roots in the '
        'Spanish colonial sugar plantations of the Oriente province. Before nationalization, the '
        'Bacardí family operated their original distillery in Santiago de Cuba from 1862; the '
        'state-owned successor operations continue the eastern Cuban rum tradition using column '
        'still distillation and aging in American white oak to produce the characteristically '
        'light, dry, aromatic Cuban ron style.'
    ),
    'founded': '1862 (original Bacardí Santiago foundation); state operation from 1960',
    'region': 'Santiago de Cuba, Oriente Province, Cuba',
    'website': 'rondesantiagodecuba.com',
    'verified': True
})

session.add_beverage({
    'name': 'Ron Santiago de Cuba Añejo 11 Años — Eastern Province, Oriente Cane, Column Still Cuban Style',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Cuba',
    'region': 'Cuba — Santiago de Cuba (Ron Santiago de Cuba, Eastern Province, Colonial Cane Heritage)',
    'producer': 'Cuba Ron S.A. — Santiago de Cuba Distillery',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Santiago de Cuba occupies the southeastern corner of Cuba — the island\'s most mountainous '
        'region, where the Sierra Maestra range rises steeply from the Caribbean coast to peaks '
        'exceeding 1,900m. The Oriente region (of which Santiago de Cuba is the capital) was the '
        'center of Spanish colonial Cuba\'s most intensively developed sugarcane economy, built on '
        'enslaved African agricultural labour from the 17th century onward. The city of Santiago '
        'de Cuba itself sits at the head of a natural harbour formed by a narrow coastal inlet '
        'backed by the Sierra Maestra foothills — a subtropical Mediterranean climate zone with '
        'more pronounced seasonality than Havana: hot, humid summers (30–35°C) with heavy '
        'Caribbean-facing rainfall from the Sierra Maestra rain shadow effect on the northern '
        'slopes, and drier winters (22–26°C) influenced by the Oriente\'s southern exposure. '
        'The sugarcane grown in the Oriente region benefits from the combination of volcanic '
        'soil derived from the Sierra Maestra\'s igneous basement and the intense solar radiation '
        'of the Caribbean-facing southern coastal plain. Cuba\'s national Saccharum officinarum '
        'sugarcane varieties, developed and selected over 400 years of plantation agriculture, '
        'produce a high-sucrose, high-yield cane that is processed at large centralized sugar '
        'mills (centrales) before the resulting molasses is transported to the Santiago de Cuba '
        'distillery for fermentation and distillation. Cuba\'s sugarcane agricultural heritage '
        'is inseparable from its history of African enslaved labour: the Transatlantic Slave Trade '
        'brought an estimated 750,000 enslaved Africans to Cuba between 1500 and 1860, creating '
        'the labour base of the plantation economy that produced Cuban rum\'s agricultural foundation.'
    ),
    'production_technique': (
        'Cuban ron production follows a technical tradition established in the 19th century under '
        'Spanish colonial rule and codified in the Cuban rum regulations that distinguish ron cubano '
        'from other Caribbean rum styles. The defining characteristics of the Cuban method are: '
        'distillation to high proof (90–95% ABV) in multiple-column continuous stills, producing '
        'a very light, clean, low-congener spirit base; deliberate low-ester fermentation using '
        'selected pure Saccharomyces cultures in closed stainless steel fermenters for 24–30 hours '
        'at 28–32°C; and blending with a portion of aguardiente — a lower-proof, higher-congener '
        'column still distillate aged separately — to provide complexity and body to the light '
        'column still spirit base. The Santiago de Cuba Añejo 11 Años is aged in American white '
        'oak ex-bourbon barrels for a minimum of 11 years in Cuban tropical warehouse conditions '
        '(28–30°C average, 70–80% relative humidity), producing an accelerated maturation that '
        'would require 20–25 years in temperate European conditions. The Cuban master blender '
        '(maestro ronero) applies a solera-influenced approach to aging: younger distillates are '
        'blended with older reserves before final barrel aging, ensuring consistency across batches '
        'despite the variable angel\'s share loss of tropical aging. Final proofing to 40% ABV '
        'for the Añejo 11 Años expression. No caramel colouring added to the premium expressions '
        '— the amber colour is entirely derived from 11 years of ex-bourbon barrel contact in '
        'tropical Cuban conditions.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Bacardí (Puerto Rico/global) — Cuban light-style column still rum heritage',
            'connection': (
                'Ron Santiago de Cuba and Bacardí share direct historical lineage: Facundo Bacardí '
                'Massó founded the original Bacardí distillery in Santiago de Cuba in 1862, and '
                'the technical approach he developed — high-proof column distillation for lightness, '
                'filtered charcoal treatment for clarity, ex-bourbon barrel aging for vanilla character — '
                'became the template for both the modern Bacardí operation in Puerto Rico (after '
                'nationalization forced the family to relocate in 1960) and the continuing state-owned '
                'Santiago de Cuba production. Both express the Cuban light-style ron tradition defined '
                'by Bacardí\'s 19th century innovation.'
            )
        },
        {
            'tradition': 'Spanish brandy (Jerez solera system) — solera aging influence in Cuban ron',
            'connection': (
                'Cuba\'s colonial relationship with Spain introduced the Jerez solera-influence to '
                'rum maturation: the Cuban maestro ronero tradition of blending younger and older '
                'distillate reserves before final barrel aging mirrors the Jerez criadera y solera '
                'system in which younger wine fractions are added to progressively older reserves '
                'to maintain consistency and accelerate maturation — both systems use the fractional '
                'blending principle to manage aging variance and produce consistent expressions '
                'across production years in tropical and sub-tropical aging environments.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Medium amber with golden tints; 11 years of tropical ex-bourbon aging produces colour '
            'depth greater than equivalent age in temperate conditions; clear and brilliant with '
            'moderate legs at 40% ABV.'
        ),
        'nose': (
            'The Cuban light-style column still character shows as a clean, aromatic base: vanilla '
            'and dried coconut from ex-bourbon American oak dominate the primary aromatics; '
            'dried apricot and raisin from 11 years of tropical ester development; light tobacco '
            'and cedar from the Cuban terroir expressed through the extended barrel contact; '
            'a faint anise thread from the column still congener profile — more restrained and '
            'elegant than the heavy ester profiles of Jamaican or Demeraran pot still rum, '
            'reflecting the Cuban design philosophy of lightness and aromatic precision.'
        ),
        'palate': (
            'Light to medium body — the Cuban column distillation style produces a thinner, '
            'drier texture than pot still rums; the vanilla-caramel oak character from the '
            'ex-bourbon barrel arrives cleanly on the mid-palate without molasses richness '
            'competing; the 11-year aging has added dried fruit depth without adding weight; '
            'the finish is medium-long, dry, with cedar and light tobacco lingering — the '
            'classic Cuban añejo profile that defines the light-style aged rum category.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Ron Santiago de Cuba Carta Blanca (white, unaged)',
            'criteria': (
                'Unaged or minimally aged white rum filtered to water-clarity: the raw column '
                'still expression, clean, light, and primarily useful as a cocktail base for '
                'Daiquiri and Mojito production where the light Cuban style requires a neutral, '
                'low-congener white rum base.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Ron Santiago de Cuba Añejo 8 Años',
            'criteria': (
                'Eight-year tropical aged Cuban ron: sufficient ex-bourbon integration for neat '
                'service, the classic Cuban añejo profile of vanilla, dried fruit, and light oak '
                'without the complexity of the 11-year — the standard premium reference for '
                'Cuban rum evaluation at accessible price points.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Ron Santiago de Cuba Añejo 11 Años',
            'criteria': (
                'Eleven-year tropical aged: maximum integration of the Cuban column-still light '
                'spirit and ex-bourbon American oak, dried fruit and cedar development, the '
                'definitive expression of the Santiago de Cuba style for international connoisseur '
                'consumption and spirits programme deployment.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Ron Santiago de Cuba Extra Añejo 25 Años',
            'criteria': (
                'Twenty-five year ultra-aged Cuban rum at the apex of state production: very '
                'deep amber, concentrated dried fruit, leather, tobacco, and cedar from maximum '
                'tropical barrel contact — the prestige expression demonstrating that the light '
                'Cuban column-still style can develop equivalent complexity to aged Cognac or '
                'single malt through extended tropical warehouse maturation.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Añejo 11 Años served neat at 18–20°C to appreciate the full dried fruit and cedar '
            'aromatics from 11 years of tropical aging; the Cuban light style is particularly '
            'sensitive to temperature — serving warm opens the volatile aromatic profile fully; '
            'a single small ice cube reduces serving temperature to 14–16°C while providing '
            'slow dilution that opens the mid-palate without washing the delicate column-still '
            'aromatic character.'
        ),
        'vessel': (
            'Tulip or copita glass for neat service to concentrate the light, aromatic Cuban '
            'rum character; a wide snifter disperses the delicate aromatics too rapidly; for '
            'the classic Cuban cocktail context (Daiquiri: white rum, lime, sugar; Mojito: '
            'white rum, lime, sugar, mint, soda), use the Carta Blanca rather than the añejo '
            'as the cocktail base; the Añejo 11 Años works in an Old Fashioned format with '
            'Cuban sugarcane syrup and a tobacco-forward bitters.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Cuba Ron S.A. (Santiago de Cuba) — state-owned custodian of the eastern Cuban rum '
            'tradition; Ron Santiago de Cuba is the primary expression of the Oriente province '
            'style available internationally; Havana Club (Pernod Ricard partnership) is the '
            'alternative reference for western Cuban light-style ron from the Havana area.'
        ),
        'north_america_access': (
            'US embargo significantly restricts Cuban rum import — Ron Santiago de Cuba and Havana '
            'Club are not legally available in the US market; available through BCLDB British Columbia, '
            'LCBO Ontario, and SAQ Quebec in Canada; widely available in EU and UK markets; pricing '
            'in Canada approximately CAD $50–80 for the Añejo 11 Años expression.'
        ),
        'culinary_application': (
            'In a PCT-themed programme, Cuban ron represents the Spanish colonial contribution to '
            'Caribbean rum culture: the Oriente province\'s plantation heritage, the Bacardí '
            'foundation narrative, and the post-revolutionary state continuation of the light-style '
            'rum tradition as Cuban national identity — the spirits equivalent of the cultural '
            'preservation story that defines PCT engagement with colonial-heritage production systems.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region(
    'spirits',
    'Cuba — Havana Province (Ron Havana Club Añejo 7 Años, Western Limestone Coast)'
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Havana Club International — San José de las Lajas Distillery',
    'location': 'San José de las Lajas, Mayabeque Province, Cuba',
    'description': (
        'Havana Club is Cuba\'s most internationally recognized rum brand, a joint venture between '
        'Cuba Ron S.A. (the Cuban state rum corporation) and Pernod Ricard since 1993. The '
        'production facility at San José de las Lajas, south of Havana, operates large-scale '
        'column still distillation producing the Havana Club range from western Cuban molasses. '
        'The brand is the global market leader for the Cuban ron style outside the United States '
        '(where the Arechabala family trademark dispute with Bacardí has prevented distribution). '
        'The Havana Club 7-Year (Añejo 7 Años) is the flagship aged expression used as the '
        'global cocktail reference for Cuban-style ron in premium bar programming worldwide.'
    ),
    'founded': '1934 (José Arechabala SA original); 1993 joint venture established',
    'region': 'Mayabeque Province, western Cuba',
    'website': 'havana-club.com',
    'verified': True
})

session.add_beverage({
    'name': 'Havana Club Añejo 7 Años — Western Limestone Coast, Havana Province, Cuban Light-Style Ron',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Cuba',
    'region': 'Cuba — Havana Province (Ron Havana Club Añejo 7 Años, Western Limestone Coast)',
    'producer': 'Havana Club International — San José de las Lajas Distillery',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Havana Province and the adjacent Mayabeque Province in western Cuba occupy a different '
        'geological and climatic zone from the Oriente region: the western Cuban lowland plain '
        'is primarily underlain by Eocene and Miocene limestone — the karst-forming carbonate '
        'rock sequence that creates Cuba\'s characteristic mogote (haystack hill) landscape and '
        'the famous red laterite soils (tierra colorada) of the Vuelta Abajo tobacco region to '
        'the west. The Havana zone climate is influenced by the Gulf of Mexico to the north and '
        'the Caribbean to the south, producing a humid subtropical regime with mean annual '
        'temperatures of 24–26°C, 1,200–1,500mm annual rainfall with a pronounced dry season '
        'from November to April, and the constant northeast trade winds that moderate temperatures '
        'along the northern coastline. The limestone aquifer system underlying the Havana lowlands '
        'provides mineral-rich groundwater used in rum production — Cuban water quality, derived '
        'from the filtration through Cenozoic limestone formations, contributes low mineral '
        'content and high alkalinity appropriate for column-still rum production. The San José '
        'de las Lajas facility sources molasses from the western Cuban sugar industry, where '
        'the Vuelta Abajo region\'s red laterite soils and the Havana plain\'s black clay soils '
        'produce sugarcane with slightly different sucrose and mineral content from the volcanic '
        'soils of the Oriente region — though the high-proof column distillation method strips '
        'most regional character from the fermentation substrate before aging in ex-bourbon oak.'
    ),
    'production_technique': (
        'Havana Club Añejo 7 Años is produced by the Cuban ron production method refined at the '
        'Havana Club San José facility: column still distillation to 90–95% ABV, producing a '
        'clean, light-bodied spirit base with minimal congener complexity; blending with a '
        'proportion of aged aguardiente (lower-proof, higher-congener distillate) to add body '
        'and complexity; and extended aging in American white oak ex-bourbon barrels for 7 years '
        'in the western Cuban climate. The San José distillery operates large-scale continuous '
        'column stills capable of producing consistent volume at the high proof required by the '
        'Cuban light-style ron standard. The maestro ronero team — a title carried by Cuban rum '
        'masters with decades of apprenticeship within the Cuban state rum system — makes blending '
        'decisions that maintain the Havana Club 7 Años profile year-to-year across production '
        'batches: selecting casks of appropriate vanilla, dried fruit, and tobacco development '
        'from the aging warehouse; adding the aguardiente proportion at the right point in the '
        'aging cycle; and final water reduction to 40% ABV with Cuban mineral water. The Cuban '
        'Geographical Indication for ron cubano (secured through the EU GI framework) protects '
        'the technical standards of Cuban rum production: minimum 3 years aging in oak, '
        'distillation in Cuba from Cuban agricultural raw materials, and the light-style column '
        'distillation method that distinguishes Cuban ron from Jamaican pot still and Barbadian '
        'blended rum traditions.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Armagnac blanche (Gascony, unaged Armagnac as fresh grape distillate)',
            'connection': (
                'Havana Club white rum (the base for Mojito and Daiquiri) and Armagnac blanche '
                'both serve as transparent, unaged distillate expressions revealing the raw character '
                'of the fermentation substrate before wood aging transforms them — the Cuban column '
                'still captures a clean, light molasses spirit as Armagnac blanche captures the '
                'raw Folle Blanche character, and both are used as the foundation for understanding '
                'how the aged expressions in oak develop their complexity from a transparent starting point.'
            )
        },
        {
            'tradition': 'Pisco Sour (Peru/Chile) — column distillation, light-style spirit production',
            'connection': (
                'Cuban ron and Peruvian pisco both demonstrate how column still distillation '
                'deliberately aimed at high proof and lightness produces spirits that define their '
                'national identity through aromatic delicacy rather than congener complexity: '
                'the Cuban maestro ronero selecting for vanilla, dried fruit, and tobacco elegance '
                'parallels the Peruvian pisco tradition\'s emphasis on grape variety aromatic '
                'transparency in a single-pass pot distillation — both seeking lightness as a '
                'quality standard in opposition to the ester-heavy, dark-rum alternative.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Rich amber with copper tints; 7 years of tropical ex-bourbon aging in western Cuban '
            'conditions produces full colour development; clear, brilliant, with slow legs at 40% ABV '
            'indicating good glycerol retention from the aguardiente blending component.'
        ),
        'nose': (
            'Vanilla and caramel from ex-bourbon American oak dominate with characteristic '
            'Cuban elegance; dried tobacco leaf and cedar from the western Cuban terroir expressed '
            'through barrel contact; light dried apricot and raisin from 7-year ester development; '
            'the aguardiente proportion contributes a subtle richness beneath the column still '
            'lightness — the classic Havana Club 7 profile that has defined the reference for '
            'aged Cuban ron in international cocktail culture for three decades.'
        ),
        'palate': (
            'Light to medium body; the Cuban light style shows as a clean, dry texture with '
            'vanilla and caramel from the oak arriving first, followed by dried fruit and the '
            'characteristic tobacco-cedar dryness that distinguishes western Cuban ron from '
            'the sweeter, more molasses-forward English-heritage Caribbean rum styles; '
            'medium-long finish with cedar and dried fruit persisting; the 40% ABV provides '
            'warmth without heaviness — a spirit designed for both neat appreciation and '
            'cocktail integration in equal measure.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Havana Club Añejo 3 Años (white-gold)',
            'criteria': (
                'Three-year minimum aged and charcoal filtered: the Mojito and Daiquiri workhorse, '
                'retaining enough aged character for complexity while maintaining the light clarity '
                'required for classic Cuban cocktail production; the entry point to the Havana Club '
                'aged range.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Havana Club Añejo Especial (5-Year Blend)',
            'criteria': (
                'Five-year blend with deeper amber colour and more pronounced oak character than '
                'the 3-Year: the intermediate tier for rum-and-cola and longer cocktail applications '
                'where the full Añejo 7 Años character is not required but the white rum is insufficient.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Havana Club Añejo 7 Años',
            'criteria': (
                'The flagship: 7-year tropical aged, maestro ronero blended, the global benchmark '
                'for the Cuban light-style añejo ron — the expression that defines Cuban rum\'s '
                'international identity and serves as the reference for spirits education on the '
                'Cuban style versus Jamaican, Barbadian, and Guyanese alternatives.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Havana Club Selección de Maestros (aged reserve)',
            'criteria': (
                'Special releases of exceptional cask selections by the maestro ronero team: '
                'maximum Cuban ron complexity from select ex-bourbon barrels showing outstanding '
                'tobacco, cedar, and dried fruit development — the prestige tier positioning '
                'Cuban rum in direct competition with aged Cognac at fine dining service level.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Añejo 7 Años at 18–20°C for neat evaluation; the Cuban light style shows its fullest '
            'aromatic complexity at room temperature where the tobacco and cedar volatile compounds '
            'are most active; for the classic Cuba Libre format (7 Años, Coca-Cola, lime, ice), '
            'serve cold at 4–8°C over cubed ice — the cold temperature and carbonation of the '
            'cola complement the dry tobacco character of the 7-year ron; for an Old Cuban cocktail '
            '(7 Años, lime, sugar, Angostura, Champagne), serve the finished cocktail at 8–10°C.'
        ),
        'vessel': (
            'Copita or tulip glass for neat service to capture the delicate tobacco and cedar '
            'aromatics that are the hallmark of western Cuban ron character; highball glass '
            'for Cuba Libre service; coupe for the Old Cuban; the Añejo 7 Años is the global '
            'standard for Cuban rum cocktail programming and its light-style character makes it '
            'one of the most versatile aged rum bases available for mixed drink applications.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Havana Club International (Cuba Ron S.A. / Pernod Ricard JV) — Añejo 7 Años is the '
            'global benchmark for aged Cuban light-style ron; distributed in 120+ countries outside '
            'the United States (where the trademark dispute with Bacardí prevents sales); '
            'the international reference for Cuban rum in any spirits programme.'
        ),
        'north_america_access': (
            'Available in Canada through all major provincial liquor boards (BCLDB, LCBO, SAQ) at '
            'CAD $38–48 for the Añejo 7 Años — one of the most widely distributed premium aged '
            'rums in Canada; the US embargo prevents legal import in the US market; UK and EU '
            'widely available.'
        ),
        'culinary_application': (
            'The Havana Club 7 Años is the PCT\'s Cuban rum standard: its connection to the '
            'colonial sugar trade, the Transatlantic Slave Trade\'s Cuban labor history, and '
            'the revolutionary nationalization that transformed private Cuban rum production '
            'into a state institution creates a layered historical narrative for PCT-themed '
            'spirits programming around the Caribbean.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
