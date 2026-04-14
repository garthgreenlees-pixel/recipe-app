import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='India — Nashik District Maharashtra (Sula Vineyards Rasa Shiraz, Godavari Basin Basalt, Colonial Wine Legacy)',
    output_dir='.',
    starting_entry=1,
    session_number=61,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Sula Vineyards — Nashik District, Maharashtra',
    'location': 'Gat No. 36/2, Dindori Road, Nashik 422 212, Maharashtra, India',
    'description': (
        'Sula Vineyards was founded in 1999 by Rajeev Samant (Stanford MBA, former Oracle '
        'engineer) after acquiring land in Nashik\'s basalt plateau zone and partnering with '
        'Kerry Damskey, a California winemaker from Fetzer Vineyards, to establish the first '
        'commercial international-style winery in Nashik. Sula now commands approximately 65% '
        'of India\'s premium wine market by volume, producing 12 million bottles annually '
        'across 17 wine styles from 1,800 acres of owned and contract-farmed vineyards in '
        'Nashik, Dindori, and the Sahyadri sub-regions. The winery pioneered Indian wine '
        'tourism with the SulaFest annual music and wine festival (February) and the on-site '
        'resort, making it the dominant force in India\'s wine culture formation. The Rasa '
        'Shiraz expression specifically demonstrates Nashik basalt terroir impact on '
        'Syrah/Shiraz — the same grape that defines the Northern Rhône and Barossa Valley '
        'but expresses distinctly Indian tropical character at 600m Nashik elevation.'
    ),
    'founded': '1999',
    'region': 'Nashik, Maharashtra, India',
    'website': 'sulawines.com',
    'verified': True
})

session.add_producer({
    'tradition': 'wine',
    'name': 'York Winery — Nashik Dindori Sub-Region',
    'location': 'Gangapur-Savargaon Road, Dindori, Nashik 422 202, Maharashtra, India',
    'description': (
        'York Winery was established in 2008 by Kapil Sekhri with a deliberate focus on the '
        'Dindori sub-region of Nashik, where basalt-loam soils at 600–650m elevation produce '
        'wine of greater concentration than the lower Nashik plains. York\'s Reserve Chenin '
        'Blanc is considered the benchmark for Indian Chenin Blanc — a grape well-suited to '
        'Nashik\'s hot-days/cool-nights diurnal swing of 15–18°C in the growing season, '
        'which preserves natural acidity in the white varieties. York produces under 300,000 '
        'bottles annually, focusing on premium single-variety expressions that have received '
        'recognition at international competitions including Decanter World Wine Awards.'
    ),
    'founded': '2008',
    'region': 'Dindori, Nashik, Maharashtra, India',
    'website': 'yorkwinery.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Sula Vineyards Direct / India Wine Company (US importer)',
    'type': 'importer',
    'description': (
        'Sula Vineyards distributes internationally through dedicated US and UK import agents. '
        'Indian wine availability in North America is expanding as the Indian diaspora restaurant '
        'sector grows; LCBO Ontario and select BC private wine stores carry Sula expressions. '
        'York Winery has limited North American availability through specialty importers. '
        'The India Wine Company handles distribution for multiple Indian producers in the '
        'US market, with New York and California as primary markets.'
    ),
    'markets_served': ['India', 'US', 'UK', 'Canada', 'Singapore'],
    'traditions_carried': ['wine'],
    'website': 'sulawines.com',
    'verified': False
})

session.add_beverage({
    'name': (
        'Sula Rasa Shiraz — Nashik District Basalt Plateau, Godavari Basin, '
        'Tropical Monsoon Viticulture at 600m Elevation'
    ),
    'category': 'wine',
    'subcategory': 'wine_still',
    'origin': 'India',
    'region': 'India — Nashik District Maharashtra (Sula Vineyards Rasa Shiraz, Godavari Basin Basalt, Colonial Wine Legacy)',
    'producer': 'Sula Vineyards — Nashik District, Maharashtra',
    'alcohol_content': 13.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'Nashik District sits at 18–20°N latitude in the Sahyadri ranges of the Western Ghats, '
        'at 550–700m elevation in the upper Godavari River basin. The viticultural zone extends '
        'across two geologically distinct zones: the Nashik plains (550–580m), dominated by '
        'deep alluvial soils from Godavari sedimentation, and the Dindori plateau (600–650m), '
        'where black Deccan basalt (Deccan Traps formation, 65 million years old) with shallow '
        'laterite topsoil over fractured basalt bedrock creates the most distinctive terroir. '
        'The Deccan Traps basalt is the same volcanic geological formation that underlies much '
        'of central India; the basalt retains heat through the night and releases it slowly, '
        'moderating the extreme diurnal temperature swing of 15–20°C between the 35–40°C '
        'daytime maximum and the 18–22°C nighttime minimum during October harvest. The '
        'monsoon viticulture cycle is the defining production challenge: vines are pruned '
        'twice annually (January and June) because the June–September southwest monsoon '
        'delivers 400–600mm of concentrated rainfall that interrupts the normal northern '
        'hemisphere annual cycle — Indian viticulture is fundamentally counter-seasonal '
        'to European wine production. British colonial presence in Maharashtra from 1818 '
        'created an administrative and economic infrastructure that brought European wine '
        'culture to Pune and Mumbai, generating the first wine consumption demand in '
        'India that Nashik now serves as the primary production zone.'
    ),
    'production_technique': (
        'Sula Rasa Shiraz is produced from estate and contract-farmed Syrah/Shiraz vines '
        'on Nashik basalt plateau sites at 600–620m elevation, planted at 1,650–2,000 vines/ha '
        'on trellised overhead pergola systems (mandap training) — the dominant Nashik vine '
        'training architecture adapted from Goa Portuguese-era grape cultivation and later '
        'standardized by Indian viticulturists to manage the monsoon canopy. The double-pruning '
        'cycle is managed so that the second pruning (June–July) forces fruit-set timing into '
        'September–October, after the monsoon retreats and the cool dry season begins. Harvest '
        'takes place October–November at 22–24 Brix, with hand-harvesting at dawn to preserve '
        'fruit temperature below 25°C before transport to the winery. The Rasa (meaning '
        '"essence" in Sanskrit) tier receives extended maceration of 18–21 days with active '
        'pump-overs twice daily during fermentation in temperature-controlled stainless steel '
        'at 24–26°C. Post-fermentation, the wine undergoes malolactic conversion in barrel '
        'and ages for 9–12 months in a combination of French and American oak barriques '
        '(225L, 50% new oak for Rasa tier), contributing vanilla and spice character that '
        'integrates with the inherently rich tropical fruit character of Nashik Shiraz. '
        'Total production of Sula Rasa Shiraz: approximately 30,000–50,000 bottles annually. '
        'The wine is fined and cold-stabilized before bottling under cork.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Barossa Valley Shiraz (South Australia, continental influence)',
            'connection': (
                'Nashik Shiraz and Barossa Valley Shiraz share the structural character of '
                'warm-climate Syrah — dense dark fruit, high natural sugar ripeness (both '
                'harvesting at 22–25 Brix), and American oak affinity — but differ in '
                'tannin architecture: Barossa Shiraz develops polyphenol richness from '
                'the diurnal temperature swing of a continental interior, while Nashik '
                'Shiraz is shaped by tropical humidity that produces silkier tannins '
                'and more forward tropical fruit (mango, guava) versus Barossa\'s plum '
                'and blackberry. Both represent hot-climate Shiraz styles that use '
                'American oak to frame rather than restrain the inherent fruit intensity.'
            )
        },
        {
            'tradition': 'Cape Winelands Shiraz (Stellenbosch, South African colonial wine)',
            'connection': (
                'Nashik and Stellenbosch share the post-colonial wine narrative: both '
                'wine industries were shaped by European colonial agricultural transfer '
                '(British in Maharashtra; Dutch then British in the Cape), and both '
                'produce Shiraz in warm-to-hot growing climates where canopy management '
                'is the dominant technical challenge. The British colonial administration '
                'connection is direct: the same administrative class that developed '
                'Stellenbosch wine culture from Cape Colony wine also created the '
                'Indian civil service wine demand that drove Nashik winery development '
                'in the post-Independence era.'
            )
        },
        {
            'tradition': 'Portuguese Dão Touriga Nacional (highland India wine parallel)',
            'connection': (
                'Both Nashik Shiraz and Dão Touriga Nacional represent wines produced '
                'in elevated plateaus (Nashik 600m basalt; Dão 400–600m granite) '
                'where highland altitude moderates daytime heat and preserves natural '
                'acidity in warm-climate settings. The Portuguese colonial wine '
                'heritage connection to India is also direct via Goa: the Portuguese '
                'established viticulture in Goa (Portuguese India 1510–1961), creating '
                'the first commercial winemaking infrastructure on the Indian subcontinent '
                'that preceded Nashik\'s modern wine industry by four centuries.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep ruby-garnet, opaque core, purple rim tinge reflecting the young '
            'fruit concentration typical of tropical Nashik Shiraz; excellent color '
            'saturation from 18–21 day maceration on basalt-terroir fruit; '
            'brilliant clarity after cold stabilization and fining; good legs '
            'at 13.5% ABV indicating the glycerol contribution of warm-climate ripeness.'
        ),
        'nose': (
            'Tropical dark fruit dominates: overripe blackberry, mulberry, and '
            'a distinctly Indian tropical register of ripe guava and black plum '
            'from the monsoon-modulated warm-climate ripening; behind the fruit, '
            'vanilla and cedar from French and American oak barriques; '
            'a characteristic white pepper and violet note from Syrah variety '
            'expressed in the 600m Nashik altitude; warm spice (black pepper, '
            'cinnamon) from the American oak component; full aromatic intensity '
            'with no reduction or VA defects in the Rasa tier.'
        ),
        'palate': (
            'Full body, warm 13.5% ABV, ripe tannins silky rather than grippy '
            'from the tropical fruit concentration and monsoon-modulated ripening; '
            'the mid-palate delivers the tropical fruit intensity of the nose — '
            'dark mulberry, blackcurrant, ripe plum; oak spice and vanilla frame '
            'the finish without overwhelming the fruit character; medium-long '
            'finish with warm spice lingering; acidity moderate, consistent with '
            'warm-climate Shiraz from basalt-retained heat sites; the wine '
            'demonstrates that Nashik basalt terroir produces Shiraz of genuine '
            'structural complexity, not merely warm-climate fruit richness.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Sula Classic Shiraz (entry)',
            'criteria': (
                'The high-volume entry tier: Nashik plains alluvial-soil Shiraz, '
                'stainless steel fermentation without extended maceration, no barrel '
                'aging — fresh, fruit-forward, no structural complexity; '
                'the Indian restaurant house wine tier at accessible pricing.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Sula Reserve Shiraz',
            'criteria': (
                'Dindori basalt-site fruit, 12-day maceration, 6 months American oak '
                'aging; more structured than Classic but without the Rasa tier\'s '
                'extended maceration and French oak component; the premium commercial '
                'tier representing accessible Nashik basalt character.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Sula Rasa Shiraz',
            'criteria': (
                'The estate benchmark: 18–21 day maceration, 9–12 months French and '
                'American oak, Dindori plateau basalt-site selection, full malolactic '
                'conversion — the expression that demonstrates Nashik\'s capacity '
                'for international-standard Shiraz at the premium tier.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Sula The Source (single-vineyard apex)',
            'criteria': (
                'Single-vineyard selection from the oldest Sula estate vines on '
                'Dindori plateau basalt — maximum concentration from oldest vine '
                'root depth, extended maceration to 28 days, 16 months new French '
                'oak aging; the collector tier and India\'s reference benchmark '
                'for estate-level Shiraz at international quality standards.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Sula Rasa Shiraz at 17–19°C for maximum aromatic expression of '
            'the tropical fruit character — cooler than standard red wine service '
            'at 20°C suppresses the warm-climate fruit intensity; in a climate-controlled '
            'environment, 60 minutes in a standard refrigerator from room temperature '
            'achieves the optimal window. Decanting for 30–45 minutes opens the '
            'oak structure and allows the pepper-violet Syrah aromatics to develop. '
            'Do not serve above 20°C — the warm-climate fruit base becomes '
            'jammy and the alcohol heat dominates above this threshold.'
        ),
        'vessel': (
            'Standard Syrah/Shiraz Burgundy-style glass with wide bowl to capture '
            'the aromatic complexity of the tropical fruit and spice character; '
            'a decanter for 30–45 minutes before service allows the warm-climate '
            'tannins to soften and the oak spice to integrate; pour at 120ml for '
            'programme tasting flight or 150ml for table service. In a PCT '
            'colonial India narrative programme, the wine connects the Portuguese '
            'Goa viticultural heritage (first Indian wine production) to the '
            'British colonial Maharashtra administrative demand that created the '
            'modern Nashik wine industry.'
        ),
        'programme_position': (
            'In a Malabar Coast / Indian beverages programme: serve after Kerala '
            'kallu (the pre-colonial fermented baseline) and before Goa feni '
            '(distilled coconut) — the Sula Rasa Shiraz represents the modern '
            'Indian wine industry built on the colonial wine consumption infrastructure '
            'that British and Portuguese colonial administration created in Maharashtra.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Sula Vineyards — Nashik District, Maharashtra (market leader, 65% of Indian '
            'premium wine; Rasa Shiraz is the Nashik benchmark for international-standard '
            'Indian red wine); York Winery Dindori for Reserve Chenin Blanc as the '
            'benchmark Indian white wine at estate-quality level.'
        ),
        'north_america_access': (
            'Sula wines available through specialty Indian wine importers in Ontario (LCBO '
            'special order), select BC private wine stores, and New York/California specialty '
            'wine retailers. Pricing approximately USD $18–25 for Rasa Shiraz in US market. '
            'Growing diaspora restaurant demand driving improved North American distribution.'
        ),
        'culinary_application': (
            'Sula Rasa Shiraz pairs with the spice-heat character of Indian cuisine in a '
            'way that Old World European reds do not: the warm-climate tropical fruit '
            'base and gentle tannin structure complement rather than clash with '
            'chili heat, tamarind tartness, and coconut richness — the wine was '
            'developed in the same culinary climate that produces the food.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region(
    'wine',
    'India — Nashik Dindori Sub-Region (York Winery Reserve Chenin Blanc, Basalt Loam, Tropical Monsoon Viticulture)'
)

session.add_beverage({
    'name': (
        'York Winery Reserve Chenin Blanc — Nashik Dindori Basalt-Loam, '
        'Diurnal Swing Acid Preservation, Tropical Monsoon Viticulture'
    ),
    'category': 'wine',
    'subcategory': 'wine_still',
    'origin': 'India',
    'region': 'India — Nashik Dindori Sub-Region (York Winery Reserve Chenin Blanc, Basalt Loam, Tropical Monsoon Viticulture)',
    'producer': 'York Winery — Nashik Dindori Sub-Region',
    'alcohol_content': 12.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'Nashik\'s Dindori sub-region at 600–650m elevation represents the highest and '
        'coolest growing zone within the Nashik District viticultural area, sitting on '
        'the eastern slope of the Sahyadri Ghats where the black Deccan basalt (Deccan '
        'Traps, Cretaceous-Paleogene era) is covered with shallow lateritic loam of '
        '25–40cm depth over fractured basalt rock. This thin soil depth forces vine '
        'roots to penetrate fractured basalt for water and mineral access — a root '
        'system architecture comparable to the schist root penetration in the Douro '
        'Valley. The Dindori plateau sits within the rain shadow of the Sahyadri Ghats: '
        'the southwest monsoon (June–September) delivers 350–450mm concentrated rainfall '
        'at Dindori versus 600–800mm on the windward western slopes, creating the '
        'drier growing conditions that reduce disease pressure and concentrate fruit. '
        'The Nashik District Geographical Indication (GI) for wine was formally '
        'recognized by the Government of India in 2020, codifying the basalt terroir '
        'claim that York and Sula producers had been asserting informally since 2005. '
        'The Chenin Blanc variety was first planted experimentally in Nashik in the '
        'early 2000s and proved uniquely well-suited to the 15–18°C diurnal temperature '
        'swing of the October harvest season at Dindori elevation — the cool nights '
        'preserve the natural malic acid that Chenin Blanc requires for structural '
        'longevity while the warm days achieve phenolic ripeness at 20–22 Brix.'
    ),
    'production_technique': (
        'York Reserve Chenin Blanc is harvested from the highest Dindori plateau sites '
        '(630–650m) in mid-October, when natural acidity (7.5–9.0 g/L total acidity '
        'as tartaric) and potential alcohol (20–22 Brix) intersect for the optimal '
        'balance specific to York\'s winemaking style. Hand-harvest at dawn maintains '
        'fruit temperature below 20°C for transport to the winery in insulated bins. '
        'Whole-cluster pressing in a pneumatic press at 0.5–0.8 bar maximum pressure '
        'extracts free-run juice without skin tannin or phenolic extraction; the free-run '
        'fraction (typically 60–65% of total press volume) is settled cold at 4–6°C '
        'for 18–24 hours to clarify. Fermentation takes place in a combination of '
        'stainless steel temperature-controlled tanks (at 16–18°C) and 228L French '
        'oak pièces (20–30% new) for the Reserve tier. The partial barrel fermentation '
        'adds textural complexity without the heavy oak character that would overwhelm '
        'Chenin\'s natural quince-and-citrus aromatic profile. The Reserve tier undergoes '
        '4–5 months sur lie aging with weekly bâtonnage (lees stirring) to build the '
        'characteristic creamy mid-palate texture. Malolactic conversion is blocked '
        'to preserve the high natural acidity that defines Nashik Dindori Chenin Blanc '
        'and gives the wine its structural backbone for 3–5 year aging. Total '
        'production: approximately 15,000–20,000 bottles of Reserve tier annually.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Loire Valley Vouvray (Chenin Blanc, Touraine, tuffeau limestone)',
            'connection': (
                'York Reserve Nashik Chenin Blanc and Vouvray sec share the Chenin '
                'Blanc variety\'s characteristic tension between high natural acidity '
                'and full phenolic ripeness — the variety preserves acidity in cool '
                'Loire nights and in Nashik\'s diurnal 15–18°C swing equally. Both '
                'express the quince, green apple, and lanolin character that defines '
                'the Chenin Blanc aromatic profile independent of terroir, while '
                'demonstrating how dramatically the same grape adapts: Vouvray\'s '
                'honeyed wax and wet stone versus Nashik\'s tropical mango-citrus '
                'and volcanic mineral register.'
            )
        },
        {
            'tradition': 'South African Chenin Blanc (Swartland and Stellenbosch, old-vine)',
            'connection': (
                'Both Nashik and South African Chenin Blanc represent warm-climate '
                'expressions of a grape more commonly associated with cool Loire '
                'origins. South Africa has the world\'s oldest-vine Chenin Blanc '
                'plantings (some exceeding 40 years), and the Cape wine industry\'s '
                'warm-climate Chenin expertise — particularly in Swartland bush-vine '
                'Chenin — provides the closest technical parallel to Nashik\'s '
                'monsoon-viticulture approach: both manage heat-stress with elevated '
                'altitude or maritime cooling, both produce Chenin with tropical fruit '
                'character absent in Loire, and both have driven the variety\'s '
                'international rehabilitation from workhorse to benchmark white grape.'
            )
        },
        {
            'tradition': 'Douro Valley White (Rabigato and Gouveio, granite and schist)',
            'connection': (
                'Both Nashik Dindori Chenin Blanc and Douro white wines are produced '
                'from vineyards where shallow hard-rock soils (basalt at Dindori; '
                'schist and granite at Douro) force root penetration into fractured '
                'bedrock for water and mineral access — the same terroir mechanism '
                'producing concentrated, mineral-inflected white wines in both '
                'contexts. The Portuguese colonial connection is also direct: the '
                'Douro viticultural tradition that produced Port for the British '
                'market is the same colonial wine culture that created Indian '
                'administrative demand for European-style wine in Maharashtra.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale gold with green tints typical of Chenin Blanc from cool-harvested '
            'high-altitude sites; brilliant clarity after cold settling and filtration; '
            'no oxidative browning — the preserved natural acidity at Dindori elevation '
            'protects color integrity; light-bodied appearance at 12.5% ABV consistent '
            'with the high-acid, moderate-alcohol Nashik Dindori white wine style.'
        ),
        'nose': (
            'Chenin Blanc\'s characteristic tension between citrus freshness and '
            'ripe stone fruit: green apple, fresh quince, kaffir lime zest from '
            'the high natural acidity; beneath the citrus, tropical mango and '
            'lychee from the warm Nashik growing days; sur lie aging contributing '
            'fresh bread dough and a subtle lanolin-waxy note characteristic of '
            'the variety; the partial barrel fermentation adding a light vanilla '
            'and cream undertone without dominating the fruit character; clean '
            'and precise, with no heavy oak or reductive character.'
        ),
        'palate': (
            'Medium body with textural richness from 4–5 months bâtonnage; the '
            'high natural acidity (7.5–9.0 g/L) arrives immediately and structures '
            'the entire palate experience; ripe quince and tropical citrus through '
            'the mid-palate; the partial barrel fermentation adds cream and brioche '
            'texture that integrates with the acidity rather than softening it; '
            'long, clean finish with the defining Chenin Blanc combination of '
            'acidity and phenolic grip; the Indian tropical character (mango, '
            'lychee) distinguishes the finish from Loire Chenin without compromising '
            'the variety\'s structural integrity.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'York Classic Chenin Blanc',
            'criteria': (
                'Nashik plains alluvial-soil fruit, stainless steel fermentation only, '
                'no lees contact, early bottling at 3–4 months — fresh, clean, '
                'no structural complexity; the entry-level reference for Nashik '
                'Chenin Blanc character at accessible pricing.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'York Estate Chenin Blanc',
            'criteria': (
                'Dindori basalt-site fruit, full stainless steel fermentation with '
                '3 months sur lie, no oak — more mineral structure and lees texture '
                'than Classic but without the barrel-fermentation complexity of '
                'the Reserve tier; the competent mid-range expression.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'York Reserve Chenin Blanc',
            'criteria': (
                'Highest Dindori plateau sites (630–650m), 20–30% new French oak '
                'barrel fermentation, 4–5 months bâtonnage, malolactic blocked — '
                'the benchmark for Indian Chenin Blanc at international estate-quality '
                'level, demonstrating Nashik basalt terroir\'s capacity for structured '
                'white wine aging potential.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'York Reserve Chenin Blanc Aged 3+ Years',
            'criteria': (
                'The Reserve tier with 3–5 years of bottle aging: Chenin Blanc\'s '
                'capacity for secondary development (honey, beeswax, yellow stone '
                'fruit) begins to emerge at 3 years in bottle; the high natural '
                'acidity of Nashik Dindori Chenin Blanc provides the structural '
                'framework for this development, distinguishing it from warm-climate '
                'white wines that collapse within 2–3 years. The aged Reserve '
                'represents the apex demonstration of Indian Chenin Blanc quality.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'York Reserve Chenin Blanc at 10–12°C to preserve the high natural '
            'acidity character that defines the wine — too cold (under 8°C) '
            'suppresses the tropical fruit aromatics; too warm (above 14°C) '
            'makes the 12.5% ABV and the oak component both more prominent. '
            'One hour in a standard wine refrigerator or 20 minutes in an ice '
            'bucket achieves the optimal 10–12°C window for service. '
            'The wine shows significantly better at 12°C versus 8°C in terms '
            'of aromatic expression — the tropical mango-lychee character '
            'needs slight warmth to volatilize.'
        ),
        'vessel': (
            'White Burgundy or Chardonnay-style glass with moderate bowl to '
            'concentrate the complex aromatic layers — Chenin\'s acid-driven '
            'structure benefits from a narrower rim than Chardonnay to retain '
            'volatile acidity aromatics; a 150ml pour for table service; '
            'in a tasting flight context, 80ml allows the full aromatic evolution '
            'across 10 minutes in the glass as temperature rises from 10°C to '
            'the natural ambient. The Reserve benefits from 15 minutes in the '
            'glass before tasting as the barrel fermentation notes integrate.'
        ),
        'programme_position': (
            'In a PCT colonial India / Nashik wine programme: serve as the first wine '
            'after the Kerala kallu palate-opener — the high Chenin acidity resets '
            'the palate for the Sula Rasa Shiraz richness that follows; the '
            'white-then-red sequence mirrors traditional European service while '
            'demonstrating the full range of Nashik terroir expression.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'York Winery — Dindori sub-region, Nashik (India\'s benchmark Chenin Blanc '
            'producer; Reserve tier is the reference expression for Indian white wine '
            'at international quality standards). Sula The Founder\'s Reserve Sauvignon '
            'Blanc as secondary white wine reference from the same Nashik GI zone.'
        ),
        'north_america_access': (
            'York Winery has limited North American distribution — specialty Indian wine '
            'importers in Ontario and select US states carry the Reserve tier. '
            'Availability is improving as Indian restaurant sector demand for '
            'Indian wine grows in Toronto, Vancouver, and New York. '
            'Estimated USD $20–30 for Reserve Chenin Blanc in US specialty retail.'
        ),
        'culinary_application': (
            'York Reserve Chenin Blanc\'s high natural acidity and tropical fruit '
            'character make it the most versatile Indian wine for South Asian cuisine '
            'pairing: the acidity cuts through coconut milk richness, the '
            'quince-mango character bridges with tamarind and curry leaf, '
            'and the lees texture handles the fat content of Malabar seafood '
            'preparations without the oak weight of Chardonnay overriding the food.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
