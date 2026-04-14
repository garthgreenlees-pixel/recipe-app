import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Belize — Stann Creek District (Travellers Rum, Corozal Sugarcane, Caribbean Colonial Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=51,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Travellers Liquors Ltd — Belize City',
    'location': 'Belize City, Belize',
    'description': (
        'Travellers Liquors Ltd is the primary commercial rum producer in Belize, founded in 1953 by '
        'Omario Perdomo and operating from its Belize City headquarters with sugarcane sourced from '
        'the northern districts of Corozal and Orange Walk — the traditional Belizean sugarcane belt '
        'along the border with Mexico\'s Yucatán Peninsula. Travellers is the producer of the One Barrel '
        'rum brand, Belize\'s most exported rum expression, as well as the locally consumed Travellers '
        'white and gold rums that form the backbone of Belizean rum culture. The distillery uses a '
        'combination of column and pot still distillation, aging in American white oak ex-bourbon barrels '
        'in a climate similar to Jamaica and Trinidad — warm, humid tropical conditions that promote '
        'rapid maturation.'
    ),
    'founded': '1953',
    'region': 'Belize City / Corozal District, Belize',
    'website': 'travellersrumbelize.com',
    'verified': True
})

session.add_beverage({
    'name': 'Travellers One Barrel Rum — Stann Creek District, Corozal Cane, Belizean Colonial Heritage',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Belize',
    'region': 'Belize — Stann Creek District (Travellers Rum, Corozal Sugarcane, Caribbean Colonial Heritage)',
    'producer': 'Travellers Liquors Ltd — Belize City',
    'alcohol_content': 40.0,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'Belize occupies a unique geographic position in the Caribbean rum world — the only Central '
        'American nation with an English colonial heritage (formerly British Honduras until independence '
        'in 1981), sitting on the Caribbean coast of the Central American mainland between Mexico\'s '
        'Yucatán Peninsula to the north and Guatemala to the west. The Stann Creek District on Belize\'s '
        'southern coast is the administrative region containing the Caribbean coastal lowlands where '
        'the Stann Creek River system drains the Maya Mountains before reaching the Caribbean Sea. '
        'The primary sugarcane cultivation occurs further north in the Corozal and Orange Walk districts, '
        'where the flat limestone karst plain adjacent to the Río Hondo border river with Mexico '
        'supports large-scale commercial cane cultivation under tropical lowland conditions — mean '
        'annual temperatures of 26–28°C, 1,500–2,000mm annual rainfall with a pronounced dry season '
        'from February to May. Belizean sugarcane agriculture has colonial roots extending to the British '
        'plantation system of the 17th and 18th centuries, during which Belize (then British Honduras) '
        'served as a timber-extraction colony for mahogany and logwood dyewood rather than a sugar '
        'plantation colony in the manner of Barbados, Jamaica, or Trinidad. The sugarcane industry '
        'developed later, primarily in the 20th century, following independence movements and the '
        'transition from timber to agriculture as the colonial export economy. The Mennonite communities '
        'of the Cayo and Orange Walk districts, German-speaking Protestant settlers who arrived from '
        'Mexico and Paraguay in the 1950s–1970s, now operate some of the most productive agricultural '
        'land in Belize, though not directly in the rum supply chain.'
    ),
    'production_technique': (
        'Travellers produces One Barrel rum from Corozal District molasses — the byproduct of sugar '
        'refining at the Belize Sugar Industries mill at Tower Hill in Orange Walk District, which '
        'processes the cane harvest from approximately 5,000 small-holder farmers in the northern '
        'districts. The molasses is transported to the Belize City distillery for fermentation and '
        'distillation. Fermentation uses selected Saccharomyces cerevisiae cultures in closed '
        'stainless steel fermenters for 48–72 hours at controlled temperatures of 28–32°C, producing '
        'a wash of 6–8% ABV. Distillation occurs in a hybrid system: an initial stripping column '
        'removes heavy compounds and brings the low-wine to 40–50% ABV, followed by a pot still '
        'doubler pass that refines and concentrates the spirit to 65–70% ABV. This column-then-pot '
        'hybrid approach, common in Caribbean production, extracts more congener complexity than '
        'pure column distillation while maintaining consistency across production batches. One Barrel '
        'is aged in American white oak ex-bourbon barrels — previously used 200-litre bourbon '
        'casks from Kentucky distilleries including Buffalo Trace and Heaven Hill cooperages — '
        'for a minimum of 3–5 years in the tropical Belize City warehouse. The ex-bourbon barrel '
        'contributes vanillin, caramel, and coconut lactone character from the charred American oak '
        'interior, which integrates with the molasses congeners over tropical aging to produce the '
        'characteristic sweet, vanilla-forward character that distinguishes Caribbean ex-bourbon aged '
        'rums from Barbancourt\'s ex-Cognac Limousin oak style. Proofed to 40% ABV for the standard '
        'One Barrel export expression.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Barbados rum (Mount Gay, Foursquare) — ex-bourbon barrel, tropical aging',
            'connection': (
                'Travellers One Barrel and Barbados premium rums share the ex-bourbon barrel tropical '
                'aging paradigm that defines the English-heritage Caribbean rum style: both use American '
                'white oak previously charred for bourbon, both age in tropical warehouses where annual '
                'angel\'s share losses of 8–12% rapidly concentrate and darken the spirit, and both '
                'produce the vanilla-caramel-coconut oak character that is the sensory signature of '
                'ex-bourbon aged Caribbean rum as distinct from the Cognac-oak Barbancourt tradition '
                'or the pot-still ester-heavy Jamaican tradition.'
            )
        },
        {
            'tradition': 'Guatemalan Ron Zacapa — Central American plantation rum, sugar-belt geography',
            'connection': (
                'Travellers Belize rum and Ron Zacapa Guatemala share the Central American mainland '
                'sugarcane belt geography and the English/Spanish colonial agricultural heritage of '
                'Caribbean-facing Central American coastal lowlands. Both are produced from molasses '
                'derived from commercial sugar mills processing industrial-scale cane harvest, and '
                'both represent national rum traditions from mainland Central American countries '
                'that sit at the periphery of the Caribbean island rum canon — producing spirits '
                'recognizably in the Caribbean tradition but with mainland terroir and colonial '
                'histories distinct from the island producers.'
            )
        },
        {
            'tradition': 'Jamaican pot-still rum (Appleton Estate) — Caribbean English colonial heritage',
            'connection': (
                'Belize and Jamaica share the British colonial heritage that distinguishes English-tradition '
                'Caribbean rum from the French agricole tradition and Spanish-heritage ron tradition: '
                'both nations were governed under the British West Indies colonial framework, both '
                'developed molasses-based rum production using ex-bourbon barrels as the primary aging '
                'vessel, and both maintain domestic rum cultures where local white and aged rum serve '
                'as the foundation of national drinking culture independent of export prestige markets.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Warm amber-gold from ex-bourbon barrel aging; medium depth of colour consistent with '
            '3–5 year tropical maturation in charred American oak; clear and bright with good legs '
            'at 40% ABV indicating moderate glycerol content from the molasses fermentation base.'
        ),
        'nose': (
            'Vanilla and caramel from the ex-bourbon barrel dominate the primary aromatics; '
            'underneath, the Corozal molasses base contributes a sweet, slightly sulfurous '
            'cane character that the tropical aging has rounded but not eliminated; dried '
            'coconut from the charred American oak lactone chemistry; a light tropical fruit '
            'quality from ester development during fermentation — banana, ripe plantain; '
            'the overall aromatic register is warm, accessible, and commercial in the positive '
            'sense of a spirit that clearly communicates its Caribbean ex-bourbon heritage.'
        ),
        'palate': (
            'Medium body; the vanilla and caramel from the bourbon barrel arrive immediately '
            'and carry through the mid-palate; the molasses sweetness is present but not '
            'cloying at 40% ABV; moderate warmth; the finish is of medium length with a '
            'clean, sweet oak and residual cane character — a technically correct and '
            'satisfying Caribbean ex-bourbon aged rum that performs above its price tier '
            'in cocktail contexts where the vanilla-forward profile integrates well with '
            'citrus and aromatic bitters.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Travellers White Rum (unaged)',
            'criteria': (
                'Clear, unaged column still rum for mixing and domestic consumption; the raw '
                'molasses character and clean distillation — the entry point for domestic Belizean '
                'rum culture and the base for local cocktail applications including the Belize '
                'rum punch and local bar pours.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Travellers Gold (light aged, 1–2 years)',
            'criteria': (
                'Light amber expression aged 1–2 years in ex-bourbon barrels, showing initial '
                'vanilla and light caramel while retaining the fresh molasses character — the '
                'domestic premium tier, priced for regular consumption rather than connoisseur service.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Travellers One Barrel (3–5 year aged)',
            'criteria': (
                'The flagship export expression: 3–5 year ex-bourbon barrel aging in tropical '
                'Belize City conditions producing full vanilla-caramel-coconut oak integration '
                'with the molasses base transformed rather than dominated — the benchmark for '
                'Belizean rum quality in international spirits evaluation.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Travellers Reserve (limited aged expressions)',
            'criteria': (
                'Periodic limited releases of extended-aged casks (8–12 years) from the Belize '
                'City warehouse: maximum tropical ex-bourbon concentration, deeper amber colour, '
                'richer dried fruit and vanilla complexity — the apex of the Travellers range '
                'competing with premium Caribbean aged rums at international market pricing.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve One Barrel at 18–20°C neat or over a single large sphere of ice at 12–14°C; '
            'the vanilla-caramel character is best expressed at room temperature for neat evaluation; '
            'for cocktail service in the Dark \'n\' Stormy format (rum, ginger beer, lime), serve '
            'chilled over cubed ice — the cold temperature suppresses the alcohol and allows the '
            'molasses-vanilla character to integrate with the ginger spice of the beer.'
        ),
        'vessel': (
            'Rocks glass or highball for cocktail service; Glencairn or tulip for neat evaluation '
            'to assess the ex-bourbon vanilla aromatics; the One Barrel is a versatile cocktail '
            'spirit that works in both spirit-forward builds (Old Fashioned format with rum) and '
            'long drinks (Rum Collins, Rum Punch), with the ex-bourbon character providing a '
            'familiar framework for spirits drinkers transitioning from bourbon to rum.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Travellers Liquors Ltd — One Barrel is the internationally distributed benchmark for '
            'Belizean rum; the sole Belizean rum expression with consistent North American availability '
            'and the reference point for English-heritage Central American rum production.'
        ),
        'north_america_access': (
            'One Barrel available through specialty spirits retailers in US markets with Caribbean '
            'import access; limited BCLDB and LCBO listings in Canada; pricing in the USD $20–30 '
            'range makes it competitive with mid-range Caribbean rums including Barbancourt Five '
            'Star and Banks Five Island Blend.'
        ),
        'culinary_application': (
            'One Barrel works in any cocktail calling for a vanilla-forward, ex-bourbon aged Caribbean '
            'rum: rum Old Fashioned, Rum Manhattan, or plated dessert service with tropical fruit and '
            'rum caramel — the ex-bourbon vanilla character bridges the gap between whiskey and rum '
            'for guests transitioning between the two categories.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
