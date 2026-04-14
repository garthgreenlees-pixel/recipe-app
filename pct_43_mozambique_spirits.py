import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Mozambique — Nampula and Zambézia Provinces (Nipa Palm Spirit, Caju Spirit, Colonial Sugar Cane Legacy)',
    output_dir='.',
    starting_entry=1,
    session_number=45,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Companhia de Desenvolvimento de Açúcar de Moçambique — Mafambisse Sugar Estate',
    'location': 'Mafambisse, Sofala Province, Mozambique',
    'description': "Mafambisse Sugar Estate in Sofala Province is the primary commercial sugarcane distillery in Mozambique, producing the country's main industrial spirit (aguardente de cana — Mozambican cane spirit, locally called nipa when produced from palm) for both local consumption and limited export. The Mafambisse estate was established during the Portuguese colonial period (1880s) and was nationalized after independence in 1975 before being partially privatized in the 1990s. The estate produces both raw sugarcane (for sugar refining) and the spirit that comes from the molasses by-product of sugar processing — a molasses-based rum rather than the fresh-cane agricole tradition of Cape Verde or São Tomé.",
    'founded': '1880s (colonial); privatized 1990s',
    'region': 'Sofala Province, Mozambique',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Artisan Nipa Palm Distillers — Zambézia Province Traditional Production',
    'location': 'Quilimane, Zambézia Province, Mozambique',
    'description': "Traditional nipa (niipa) palm spirit production in Mozambique's Zambézia Province is carried out by an estimated 3,000-5,000 artisan distillers using the Nipa fruticans mangrove palm (locally called nipa or maceira) that grows in the tidal estuaries and mangrove zones of the Zambézia and Nampula coastlines. The nipa palm produces a sweet sap (toddy) that is fermented and distilled into a spirit of 30-60% ABV using clay and improvised metal pot stills — a tradition with roots in the Indian Ocean trading network that predates Portuguese arrival and connects Mozambique's spirits culture to the palm toddy distillation traditions of India, Sri Lanka, and Southeast Asia.",
    'founded': 'Pre-colonial traditional production',
    'region': 'Zambézia Province, Mozambique',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Mozambique Export Development Fund / Portuguese Specialty Import',
    'type': 'importer',
    'description': "Mozambican spirits have no commercial distribution in North America. Limited export occurs through the Portuguese diaspora network in Lisbon and through specialist African spirits importers in Europe. The PCT narrative places Mozambique spirits in the research and reference category for this collection.",
    'markets_served': ['Portugal', 'South Africa', 'EU'],
    'traditions_carried': ['spirits'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': "Mozambique Nipa Palm Spirit — Zambézia Mangrove Estuary, Pre-Colonial Indian Ocean Trade Tradition, Tidal Fermentation",
    'category': 'spirits',
    'subcategory': 'palm_spirit',
    'origin': 'Mozambique',
    'region': 'Mozambique — Nampula and Zambézia Provinces (Nipa Palm Spirit, Caju Spirit, Colonial Sugar Cane Legacy)',
    'producer': 'Artisan Nipa Palm Distillers — Zambézia Province Traditional Production',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Mozambique's nipa palm spirit tradition originates in the Zambézia and Nampula coastal estuaries of northern Mozambique, where the Nipa fruticans palm grows in the tidal mangrove zones along the Indian Ocean coast. The nipa palm is the same species that provides lambanog (Philippines), arrack (Sri Lanka, Indonesia), and coconut toddy spirits across the Indian Ocean trade network — its presence in Mozambique is a direct physical record of the pre-colonial Indian Ocean Dhow trade routes that connected East Africa to India, the Persian Gulf, and Southeast Asia before European contact. The mangrove estuaries of the Zambézia coast (particularly the Quelimane Delta) provide the specific ecological conditions for nipa palm growth: brackish tidal water rich in minerals from both the Indian Ocean salt and the freshwater runoff from the Zambezi and Quelimane rivers inland. The sap tapped from the nipa palm's fruiting stalks carries the mineral signature of the tidal estuary — ocean salt, river minerals, mangrove organic acids — into the fermentation and distillation, producing a palm spirit character specific to the Mozambican coastal terroir."
    ),
    'production_technique': (
        "Traditional Mozambican nipa palm spirit production begins with tapping the flower stalks of mature nipa palms in the tidal mangrove zones — the stalk is cut and a collection vessel tied below the cut to catch the sweet sap (toddy) that flows over 8-12 hours. The fresh toddy (7-12% natural sugar) begins fermenting within hours of collection in the warm coastal temperatures (25-32°C year-round) with native wild yeast and bacteria. Fermented toddy at 4-8% ABV is collected and distilled in improvised clay or metal alembic pot stills over wood fires, producing a raw spirit at 30-60% ABV in a single pass. The resulting spirit is consumed either fresh (white, raw, 60%) or diluted with water to 30-40% for distribution. No aging in the traditional production — nipa spirit is consumed fresh, within days of distillation, giving it a raw but intensely aromatic character very different from the oak-aged cane spirits of the Caribbean. The fresh nipa spirit captures the mangrove terroir directly: saline, mineral, slightly marine, with a distinctive floral sweetness from the palm sap fermentation."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Lambanog Philippines (nipa palm or coconut toddy, traditional pot still, Pacific Indian Ocean trade connection)',
            'connection': "Mozambique nipa palm spirit and Philippine lambanog are the Indian Ocean and Pacific expressions of the same palm toddy distillation tradition that spread across the Indian Ocean trade network before Portuguese contact — both use Nipa fruticans palm sap fermented with wild yeast and distilled in pot stills, both producing raw white spirits of 30-60% ABV with the distinctive saline-floral character of mangrove palm terroir; the PCT connection is direct: Portuguese traders encountered lambanog in Manila (est. 1571) and nipa spirit in Mozambique (est. 1498) within the same trading network"
        },
        {
            'tradition': 'Goan Coconut Feni (palm sap distillate, single copper pot still, colonial Portuguese India)',
            'connection': "Mozambique nipa spirit and Goan coconut feni share the category of Portuguese colonial-encountered palm spirit traditions — both were distilled locally before Portuguese contact, both used copper or clay pot stills, and both were documented by Portuguese colonial administrators as local spirits distinct from their own wine-based alcohol tradition; the comparison demonstrates how the Indian Ocean trade network created a palm spirit belt stretching from Mozambique through Goa to the Philippines"
        }
    ],
    'sensory_profile': {
        'appearance': 'Clear, water-white; no aging, no coloring; moderate legs at 40% ABV',
        'nose': 'Distinctive mangrove estuary character: saline sea air, fresh palm sap sweetness, floral (white flower, slight citrus blossom from the fermentation), mineral-marine quality specific to the tidal production environment; the raw fermentation shows as a slight lactic or grassy note in the background',
        'palate': 'Medium body; the saline-mineral character arrives immediately with the initial warmth; floral sweetness mid-palate; marine finish with persistent salinity; raw and unaged but with sufficient complexity from the mangrove terroir to be intelligible as a spirits expression rather than mere alcohol; the finish is shorter than aged expressions but the immediate aromatic impact is distinctive',
        'conclusion': 'Cultural reference spirit of genuine Indian Ocean tradition; serves PCT programming as the East African leg of the Indian Ocean palm spirit belt; quality at artisan traditional grade'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Nipa Toddy (60%, raw)',
            'criteria': 'Freshly distilled raw nipa spirit at 60% without dilution; the local consumption form; harsh and raw but the most direct expression of the mangrove terroir'
        },
        {
            'tier': 2,
            'tier_name': 'Diluted Nipa Spirit (30-40%)',
            'criteria': 'Standard commercial dilution; the form distributed for broader consumption; more accessible but still raw and unaged'
        },
        {
            'tier': 3,
            'tier_name': 'Selected Batch Nipa (artisan production)',
            'criteria': 'Carefully controlled fermentation and clean distillation by the most skilled traditional producers; the best expressions show genuine saline-floral elegance within the raw unaged style'
        },
        {
            'tier': 4,
            'tier_name': 'Aged Mozambican Cane Spirit (Mafambisse)',
            'criteria': "Mafambisse sugar estate's aged cane spirit — molasses-based rum aged briefly in tropical conditions; a different character from the fresh nipa tradition but representing the colonial-era industrial tier of Mozambican spirits production"
        }
    ],
    'service_intelligence': {
        'temperature': 'Traditional service at room temperature (25-30°C in coastal Mozambique); for tasting presentation purposes, neat at 20°C in small vessel; the raw spirit does not benefit from ice',
        'vessel': 'Small glass tumbler (the traditional serving vessel in Mozambican coastal communities); for professional tasting, small tulip glass to concentrate the mangrove aromatic profile',
        'programme_position': 'Cultural reference tasting in a PCT Indian Ocean narrative; service in a traditional coconut shell cup with a short educational note on the Indian Ocean palm spirit belt creates authentic cultural engagement'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Traditional Zambézia Province artisan producers — no commercial benchmark equivalent to other PCT spirits; Mafambisse cane spirit for the industrial comparison; compare to Goan coconut feni (more available in North America) for the parallel Indian Ocean palm spirit tradition',
        'north_america_access': 'Unavailable commercially; reference entry for PCT research and programming context; the Goan coconut feni provides the accessible analog for menu use',
        'culinary_application': "The Mozambique coastal spirit narrative connects to Mozambican seafood cuisine (piri-piri prawns, amêijoas — Mozambican clams, camarão) which has achieved significant restaurant recognition in Portugal and South Africa; pairing the regional spirits narrative with Mozambican prawn preparations creates a complete coast-to-table East African story"
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
