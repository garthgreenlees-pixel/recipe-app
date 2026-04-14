import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Barbados — Christ Church Parish (Mount Gay XO Rum, Pot-Column Double Distillation, Coral Limestone)',
    output_dir='.',
    starting_entry=1,
    session_number=57,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Mount Gay Distilleries — St Lucy Parish, Barbados',
    'location': 'Bridgetown and Mount Gay Estate, Saint Lucy Parish, Barbados',
    'description': (
        'Mount Gay Rum holds the documented distinction of the oldest surviving rum production record '
        'in the world — a deed dated 1703 references rum equipment at the Gay\'s estate in Saint Lucy '
        'Parish, establishing Barbados as the origin point of rum documentation. The Mount Gay '
        'distillery operates from the northern Barbados estate in Saint Lucy and a production facility '
        'in the Bridgetown port area, producing both pot still and column still distillates that are '
        'blended by master blender Allen Smith. Mount Gay was acquired by Rémy Cointreau in 1989, '
        'giving the distillery global distribution through the Rémy Cointreau network. The Mount Gay '
        'XO (Extra Old) is the flagship aged expression: a blend of pot still and column still rums '
        'aged minimum 17 years in American white oak ex-bourbon barrels, representing the full '
        'expression of Barbadian double distillation and coral limestone water terroir.'
    ),
    'founded': '1703 (documented)',
    'region': 'Saint Lucy Parish, Barbados',
    'website': 'mountgayrum.com',
    'verified': True
})

session.add_beverage({
    'name': 'Mount Gay XO Rum — Christ Church Parish, Coral Limestone Water, Pot-Column Double Distillation 17-Year',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Barbados',
    'region': 'Barbados — Christ Church Parish (Mount Gay XO Rum, Pot-Column Double Distillation, Coral Limestone)',
    'producer': 'Mount Gay Distilleries — St Lucy Parish, Barbados',
    'alcohol_content': 43.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Barbados is a flat, entirely limestone island — unlike the volcanic Windward Islands (Martinique, '
        'St Vincent) or the karst-limestone Greater Antilles (Jamaica, Cuba), Barbados is composed '
        'entirely of raised coral reef limestone, a thin veneer of reddish-orange coral-derived soil '
        'over a bedrock of coralline limestone formed from the accumulated skeletons of coral organisms '
        'over millions of years. The island sits at the easternmost point of the Caribbean arc, fully '
        'exposed to the northeast Atlantic trade winds, and its limestone geology produces the most '
        'alkaline, mineral-rich water aquifer in the Caribbean rum world: Barbados groundwater filtered '
        'through coral limestone contains high calcium carbonate content that provides an optimal '
        'mineral environment for the yeast fermentation of molasses wash and contributes a specific '
        'mineral character to the final proofing water. Christ Church Parish occupies the southern '
        'tip of Barbados — a flat, wind-exposed limestone plateau with extremely permeable coral '
        'rock soils that drain rapidly after tropical rainfall. The Barbadian climate is drier '
        'than Jamaica or Martinique (approximately 1,300mm annual rainfall) with the constant '
        'northeast trade wind producing evaporative cooling that moderates temperatures. '
        'Barbados\'s central position in the English colonial Caribbean trade network made it '
        'the first island where Saccharum officinarum sugarcane cultivation produced commercial-'
        'scale rum — the 1703 Mount Gay deed establishes this primacy — and the island\'s '
        'documented production history longer than any other Caribbean territory by primary '
        'archival evidence.'
    ),
    'production_technique': (
        'Mount Gay XO is produced through the Barbadian double distillation hybrid method: '
        'molasses from Barbadian sugar production (primarily from the Andrew\'s Sugarcane '
        'Factory in Saint George Parish, the last operating sugar factory in Barbados) is '
        'fermented in closed stainless steel fermenters using selected Saccharomyces cerevisiae '
        'cultures for 30–36 hours at controlled temperatures of 28–32°C, producing a clean, '
        'consistent wash at 6–8% ABV. Distillation uses both a traditional copper double-retort '
        'pot still (producing high-ester, heavy-bodied spirit at 65–72% ABV) and a '
        'double-column continuous Coffey still (producing lighter, cleaner spirit at 85–95% '
        'ABV). The master blender Allen Smith creates the blending recipe for the XO from '
        'the pot still and column still distillates: typically a majority column still base '
        'for lightness and consistency, with the pot still component providing the ester '
        'richness, body, and aromatic complexity that distinguish Barbadian rum from the '
        'purely column-still Cuban and Puerto Rican traditions. Both components age separately '
        'in American white oak ex-bourbon barrels for a minimum of 17 years in the Mount Gay '
        'warehouses in northern Barbados, where the trade wind ventilation moderates the '
        'tropical aging rate compared to more sheltered warehouses in leeward-coast Caribbean '
        'islands. Blending occurs after the individual components reach their target maturity, '
        'followed by short rest (3–6 months) in cask for integration, then proofing to '
        '43% ABV with Barbados coral limestone water and bottling.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Blended Scotch Whisky (single malt blended with grain whisky)',
            'connection': (
                'Mount Gay XO and premium blended Scotch whisky share the fundamental blending '
                'philosophy of combining a high-congener, pot still distillate with a lighter, '
                'column still spirit to achieve complexity and consistency simultaneously: '
                'Mount Gay pot still rum provides the ester richness and body exactly as '
                'Highland single malt provides aromatic complexity to a blended Scotch; '
                'the column still rum fraction provides the same clean, neutral structure '
                'as grain whisky. Both the Barbadian blending tradition and the Scotch '
                'blending tradition operate through a master blender who manages the '
                'pot-to-column ratio across batches to maintain a house style — the '
                'oldest institutional expression of the master blender art in spirits.'
            )
        },
        {
            'tradition': 'Cognac Fine Champagne (blend of Grande and Petite Champagne crus)',
            'connection': (
                'Mount Gay\'s blend of pot still and column still components parallels the '
                'Cognac Fine Champagne blend of Grande Champagne (richer, more concentrated) '
                'and Petite Champagne (lighter, more aromatic) cru expressions: both are '
                'deliberate assemblages of complementary components where neither part alone '
                'produces the target expression, and both operate under a master blender '
                'whose institutional knowledge — accumulated over decades of tasting the '
                'component parts at different stages of aging — determines the final blend '
                'quality and character.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber with mahogany tones; 17 years of Barbadian ex-bourbon tropical aging '
            'in trade-wind-ventilated warehouses produces a somewhat lighter colour intensity '
            'than sheltered Caribbean warehouse aging at equivalent age; clear and brilliant; '
            'good legs from the pot still glycerol contribution.'
        ),
        'nose': (
            'Banana and tropical fruit from the pot still ester component, integrated with '
            'vanilla and caramel from 17 years of ex-bourbon American oak — the classic '
            'Barbadian blended rum aromatic profile of fruit complexity and oak refinement; '
            'dried apricot and toasted coconut from the long barrel contact; a fine mineral '
            'quality from the coral limestone water integration in both fermentation and '
            'proofing; the Allen Smith signature of precise balance between fruit freshness '
            'and aged barrel depth.'
        ),
        'palate': (
            'Medium-full body with the pot still\'s glycerol richness providing texture beneath '
            'the column still base\'s clean structure; vanilla and caramel from the ex-bourbon '
            'oak arrive immediately; dried tropical fruit through the mid-palate from the '
            '17-year aging; the coral limestone mineral character threads through the finish '
            'as a clean, dry mineral note; long, warm finish with the Barbadian pot still '
            'ester quality persisting — banana, dried apricot, light tropical spice — before '
            'resolving to a clean oak-and-mineral conclusion.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Mount Gay Eclipse (Silver/Gold, 3-year blend)',
            'criteria': (
                'The entry-level Barbadian rum: 3-year minimum aged blend from the same pot-column '
                'combination, showing initial ester and oak character without the dried fruit '
                'depth of the XO — the cocktail baseline for Barbadian rum in mixed drink applications.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Mount Gay Black Barrel (port cask finish)',
            'criteria': (
                'Eclipse blend finished for 6–12 months in ex-American oak casks previously used '
                'for port wine: the secondary maturation adds toffee, dark fruit, and a gentle '
                'sweetness from the port cask tannin — the premium mid-tier accessible expression '
                'that demonstrates the Barbadian rum\'s responsiveness to secondary maturation.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Mount Gay XO (17-year blend)',
            'criteria': (
                'The flagship expression: 17-year minimum aged pot-column blend, the full Barbadian '
                'rum architecture in maturity — the Allen Smith benchmark that defines the '
                'Christ Church Parish aged rum standard internationally.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Mount Gay 1703 Old Cask Selection (ultra-aged)',
            'criteria': (
                'Selected barrels aged 10–30 years, the oldest stock in the Mount Gay warehouses: '
                'maximum Barbadian coral limestone terroir expression through extended ex-bourbon '
                'aging, the apex of the oldest documented rum production tradition in the world '
                'presented at collector-tier pricing.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Mount Gay XO at 18–20°C for neat evaluation — the 17-year ex-bourbon character '
            'is most accessible at ambient temperature where the dried tropical fruit volatile '
            'compounds are fully active; a single ice sphere reduces to 12–14°C for a '
            'relaxed sipping context; the XO is also exceptional in a premium Rum Sour '
            '(XO, fresh lime, sugarcane syrup, egg white) served at 6–8°C in a chilled coupe '
            'where the Barbadian pot still character provides textural richness absent from '
            'column-only rum alternatives.'
        ),
        'vessel': (
            'Glencairn or tulip for neat evaluation; rocks glass for casual sipping with ice; '
            'the XO works in a prestige Rum Old Fashioned format (XO, Barbados sugarcane syrup, '
            'aromatic bitters, orange peel) in a wide rocks glass over a 40mm ice cube — '
            'one of the most instructive side-by-side comparisons available is the XO Old '
            'Fashioned alongside a bourbon Old Fashioned to demonstrate how Barbadian '
            'coral limestone terroir and pot-column distillation produce a spirit of equivalent '
            'cocktail-building capability to Kentucky bourbon from a completely different '
            'agricultural and geographic base.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Mount Gay Distilleries (Saint Lucy, Barbados) — the world\'s oldest documented '
            'rum estate (1703); XO is the Barbadian aged rum benchmark; Rémy Cointreau '
            'ownership provides global distribution; Allen Smith as master blender is '
            'the recognized authority for the Mount Gay house style.'
        ),
        'north_america_access': (
            'Mount Gay distributed in all US states through Rémy Cointreau USA; available '
            'throughout Canada through provincial liquor boards; XO pricing at USD $45–60 '
            'retail; the 1703 limited edition at USD $120–180; Eclipse widely available '
            'at mainstream retail price points.'
        ),
        'culinary_application': (
            'Mount Gay XO anchors the Barbados rum narrative in a PCT colonial spirits programme: '
            'Barbados as the first documented Caribbean rum producer (1703), the English '
            'colonial plantation system that established the Transatlantic rum trade, and '
            'the coral limestone geology that creates the most geologically unique water '
            'chemistry in Caribbean rum production — the PCT\'s deepest terroir argument '
            'for the Barbados rum category.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region(
    'spirits',
    'Barbados — St Philip Parish (Doorly\'s XO, Foursquare, Pot Still Blended, Barbadian Rum Style)'
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Foursquare Rum Distillery — Saint Philip Parish, Barbados',
    'location': 'Foursquare, Saint Philip Parish, Barbados',
    'description': (
        'Foursquare Rum Distillery operates on the site of a historic sugar estate in Saint Philip '
        'Parish on the eastern coast of Barbados, under the direction of master distiller and blender '
        'Richard Seale. Foursquare is the most critically acclaimed Barbadian rum producer in the '
        'contemporary period — Richard Seale\'s Exceptional Cask Selection series, annual single '
        'vintage releases aged in combinations of American ex-bourbon, Cognac, and Sauternes casks, '
        'have received the highest scores awarded to any rum expression in major spirits competitions '
        'including Rum XP and World Rum Awards. The Doorly\'s brand, produced by Foursquare under '
        'license, represents the accessible tier of Barbadian rum using the same distillation '
        'infrastructure but standard ex-bourbon aging without the Exceptional Cask Selection '
        'dual-maturation complexity.'
    ),
    'founded': '1996 (current Foursquare operation); estate dates to 18th century',
    'region': 'Saint Philip Parish, eastern Barbados',
    'website': 'foursquaredistillery.com',
    'verified': True
})

session.add_beverage({
    'name': 'Doorly\'s XO — Foursquare Distillery, St Philip Parish, Pot-Column Barbadian Blend, Sherry Cask Finish',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Barbados',
    'region': 'Barbados — St Philip Parish (Doorly\'s XO, Foursquare, Pot Still Blended, Barbadian Rum Style)',
    'producer': 'Foursquare Rum Distillery — Saint Philip Parish, Barbados',
    'alcohol_content': 40.0,
    'price_tier': 'mid_range',
    'terroir_origin': (
        'Saint Philip Parish occupies the southeastern corner of Barbados — the most trade-wind-'
        'exposed zone of the island, facing the Atlantic directly on the eastern coast. The '
        'Foursquare estate sits on the southeastern coral limestone plateau at 30–50m elevation, '
        'where the full northeast Atlantic trade wind accelerates across the low terrain and '
        'creates the most evaporative aging environment on the island — the trade wind-driven '
        'evaporation through the Foursquare warehouse structures actively manages the angel\'s '
        'share and aging rate, which Richard Seale has identified as a key differentiator of '
        'the Saint Philip Parish aging microclimate versus more sheltered parish locations. '
        'The Foursquare estate\'s coral limestone geology is identical to the rest of Barbados '
        '— all Barbadian rum production benefits from the same coral limestone aquifer water '
        'chemistry — but the exposure and trade wind airflow of the Saint Philip site creates '
        'a specific aging environment that Seale has studied and documented more thoroughly '
        'than any other contemporary Caribbean rum distiller. The estate encompasses the '
        'original plantation-era buildings including a working windmill (no longer used for '
        'production but maintained as the visual centerpiece of the Foursquare heritage site) '
        'and the original cane crusher building that is now the visitor center, connecting '
        'the contemporary rum operation directly to the 18th-century plantation-era '
        'agricultural infrastructure of Barbadian sugar production.'
    ),
    'production_technique': (
        'Foursquare produces both pot still and column still distillates from Barbadian molasses '
        'using a hybrid distillation system that Richard Seale operates with the most publicly '
        'documented transparency in the Caribbean rum industry. Seale is notable for explicitly '
        'rejecting caramel colouring and added sugar in all Foursquare and Doorly\'s expressions '
        '— a position he has advocated publicly in the rum trade as a consumer protection issue. '
        'The Doorly\'s XO is a blend of pot still rum (approximately 40% of the blend, providing '
        'ester richness, tropical fruit, and body) and column still rum (approximately 60%, '
        'providing lightness and aromatic elegance) aged separately in American white oak '
        'ex-bourbon barrels for 6–7 years before blending, followed by a finishing period of '
        '6–12 months in ex-Oloroso sherry casks for the XO expression. The sherry cask finish '
        'is the technical signature of the Doorly\'s XO versus the standard aged range: the '
        'Oloroso sherry cask contributes dried fruit, walnut, and raisin compounds from the '
        'residual Oloroso wine solids in the wood, adding a specifically Jerez-derived complexity '
        'to the Barbadian rum base without masking the coral limestone terroir or the pot-column '
        'distillation character. This secondary maturation approach mirrors the Scotch whisky '
        'industry\'s use of sherry cask finishing: using Spanish fortified wine casks to add '
        'the distinctive dried fruit and nutty character that sherry-seasoned wood uniquely '
        'contributes. Proofed to 40% ABV with Barbados coral limestone water; no added sugar '
        'or caramel colouring — Seale\'s production standards guarantee full transparency.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Sherry-finished Single Malt Scotch (Macallan, GlenDronach) — dual maturation',
            'connection': (
                'Doorly\'s XO sherry cask finish and the Scottish sherry-cask finishing tradition '
                '(Macallan exclusively sherry seasoned oak; GlenDronach heavily sherried) share '
                'the same technical principle: a spirit primary-aged in American ex-bourbon oak '
                'for structure, vanilla, and caramel, then transferred to ex-Oloroso sherry casks '
                'for a secondary maturation that adds dried fruit, walnut, and raisin complexity '
                'from the sherry wood tannin-polyphenol chemistry. Both the Barbadian rum and '
                'the Scottish whisky categories have seen the sherry cask finish become the '
                'primary differentiating premium tier — the Foursquare/Doorly\'s adoption of '
                'this technique connects the Barbadian rum tradition to the Scottish whisky '
                'innovation that has defined premium aged spirits globally.'
            )
        },
        {
            'tradition': 'Amontillado Sherry (Jerez-Xérès-Sherry, oxidative aging after flor)',
            'connection': (
                'The Oloroso sherry casks that finish Doorly\'s XO represent the direct material '
                'connection between the Jerez sherry solera system and Caribbean rum production: '
                'the compounds that defined Amontillado and Oloroso character in the sherry wine '
                '(aldehyde and acetal compounds from flor aging; tannin-derived compounds from '
                'American oak oxidative aging) migrate into the rum during the finishing period, '
                'creating a hybrid expression that bridges the PCT colonial trade network\'s Spanish '
                'colonial contribution (Jerez sherry as the export beverage of the Spanish empire) '
                'with the British colonial rum tradition of Barbados in a single glass.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber with walnut-brown tints from the sherry cask finish; darker and more '
            'saturated than American ex-bourbon aged rums at equivalent age; clear and '
            'brilliant; good legs from the pot still glycerol contribution.'
        ),
        'nose': (
            'The sherry cask finish immediately distinguishes Doorly\'s XO from standard '
            'ex-bourbon Caribbean rums: dried raisins, Medjool dates, and walnut from the '
            'Oloroso sherry wood compounds; beneath the sherry influence, the Barbadian '
            'pot still ester character shows as banana and tropical fruit; the coral '
            'limestone mineral quality of Barbadian rum adds a clean, dry mineral note '
            'as a foundation beneath the dried fruit richness of the sherry finish.'
        ),
        'palate': (
            'Medium-full body with the sherry cask finish contributing a richer, more '
            'wine-like texture than standard ex-bourbon Caribbean rums; the dried fruit '
            'and walnut from the Oloroso arrive immediately with the Barbadian pot still '
            'tropical fruit through the mid-palate; the tannin from the sherry cask '
            'provides fine-grained grip that extends the finish; long, complex conclusion '
            'with dried fruit, mineral limestone, and the faint banana-and-tropical-fruit '
            'signature of the Barbadian pot still base persisting through the sherry-derived '
            'dried fruit and walnut finish — a multi-register complexity at exceptional value.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Doorly\'s 3-Year (white/gold)',
            'criteria': (
                'Entry-level Foursquare production: minimal aging, clean pot-column character, '
                'Richard Seale\'s no-added-sugar guarantee at the most accessible price point '
                'in the range — the honest baseline for Barbadian rum without the secondary '
                'maturation complexity.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Doorly\'s 8-Year (ex-bourbon only)',
            'criteria': (
                'Eight-year ex-bourbon aged blend from the same pot-column Foursquare production '
                'base, without sherry cask finishing: the American oak vanilla and tropical '
                'fruit character of Barbadian rum in clean expression — the comparison tier '
                'against which the sherry-finished XO demonstrates the cask finish contribution.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Doorly\'s XO (sherry cask finish)',
            'criteria': (
                'The Doorly\'s flagship with Oloroso sherry cask finishing: the most complex '
                'expression in the standard Doorly\'s range, combining Barbadian pot-column '
                'distillation with dual American-oak and Spanish-sherry-cask maturation — '
                'Richard Seale\'s best-value argument in the Barbadian premium rum category.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Foursquare Exceptional Cask Selection (annual vintage release)',
            'criteria': (
                'Richard Seale\'s annual single-vintage Exceptional Cask Selection releases: '
                'specified vintage year, specific cask combinations (ex-bourbon + Cognac cask, '
                'ex-bourbon + Sauternes cask, etc.), non-chill-filtered, no added sugar or '
                'colouring, cask strength or 59% ABV — the apex of contemporary Barbadian '
                'rum artisanship and the expressions that have received the highest scores '
                'in modern rum evaluation.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Doorly\'s XO at 18–20°C for neat evaluation to appreciate the sherry cask-derived '
            'dried fruit and walnut register alongside the Barbadian pot still character; '
            'the sherry finish makes the XO more temperature-tolerant than lighter Barbadian '
            'rums — the wine-derived compounds in the sherry cask tannin remain aromatic '
            'across a wider temperature range; a single ice sphere at 12–14°C is acceptable '
            'without loss of the key sherry-derived aromatic characteristics; for cocktail '
            'use, the sherry finish makes Doorly\'s XO an excellent base for the Bamboo '
            'format (split spirit / sherry vermouth / orange bitters) where the Oloroso '
            'connection is made explicit in the cocktail construction.'
        ),
        'vessel': (
            'Tulip or Glencairn for neat evaluation; rocks glass for casual sipping; the '
            'combination of Barbadian rum mineral character and sherry-derived dried fruit '
            'makes the Doorly\'s XO one of the most versatile aged rum expressions for '
            'spirits service programming — it bridges the Scotch whisky drinker (familiar '
            'with sherry-cask finishing) and the rum connoisseur (familiar with Barbadian '
            'coral limestone terroir) in a single expression at mid-range pricing.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Foursquare Rum Distillery (Saint Philip, Barbados) / Richard Seale master distiller — '
            'Doorly\'s XO is the benchmark for accessible Barbadian rum with sherry cask finish; '
            'Foursquare Exceptional Cask Selection is the critical collector benchmark; '
            'Richard Seale is the most influential advocate for production transparency '
            'standards in the global rum industry.'
        ),
        'north_america_access': (
            'Doorly\'s XO distributed in the US through specialty spirits importers; BCLDB '
            'private import and specialty retailers in BC; LCBO Ontario listings; pricing '
            'USD $25–35 for Doorly\'s XO — exceptional value relative to comparably '
            'complex expressions in the Scotch whisky or Cognac categories; Foursquare '
            'Exceptional Cask Selection at USD $60–100 through allocation-basis specialty retail.'
        ),
        'culinary_application': (
            'The Doorly\'s XO sherry finish creates a natural bridge cocktail for a PCT spirits '
            'programme connecting the Barbadian rum colonial heritage to the Spanish Jerez '
            'trade — the most explicit material connection in the rum category to the '
            'Portuguese-Spanish colonial maritime trade network that PCT traces.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
