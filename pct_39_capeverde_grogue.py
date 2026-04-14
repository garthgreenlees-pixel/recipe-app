import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Cape Verde — Santiago Island (Grogue Aged, Oak-Rested Cane Spirit, Colonial Rum Ancestor)',
    output_dir='.',
    starting_entry=1,
    session_number=41,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Destilaria Royal — Santiago, Cape Verde',
    'location': 'Praia, Santiago Island, Cape Verde',
    'description': "Destilaria Royal is the largest commercial producer of Cape Verdean grogue (Creole: grogu; from Portuguese aguardente de cana), the sugarcane spirit that has been produced on Cape Verde's Santiago Island since the Portuguese colonial establishment of the island in the 15th century — making Cape Verdean grogue one of the oldest continuously-produced cane spirits in the world, predating Barbadian rum by nearly 200 years. The distillery processes fresh-pressed sugarcane juice (not molasses) from Santiago's interior valleys using traditional pot stills and produces both unaged white grogue and barrel-rested amber expressions. Royal's aged expressions use ex-whisky and ex-bourbon American oak casks and represent the premium tier of the category.",
    'founded': '1975 (modern company; production lineage to 17th century)',
    'region': 'Santiago Island, Cape Verde',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Grogue de Maio — Ilha do Maio Small-Batch Cane Spirit',
    'location': 'Vila do Maio, Maio Island, Cape Verde',
    'description': "Maio Island (the flattest and most arid island in the Cape Verde archipelago) produces a distinctive style of grogue from drought-stressed sugarcane grown in the island's interior — the combination of extreme aridity, volcanic sandy soils, and Atlantic trade winds produces a cane spirit of intense caramel and mineral concentration unlike Santiago's wetter, more lush production. Maio grogue is produced in tiny quantities by a small number of family distilleries using traditional alembic pot stills and represents the most artisanal end of the Cape Verde cane spirit tradition.",
    'founded': 'Traditional family production',
    'region': 'Maio Island, Cape Verde',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Cape Verde Trade Network — Diaspora Import (US Boston/Providence / Portugal)',
    'type': 'importer',
    'description': "Cape Verdean grogue enters North America almost exclusively through the Cape Verdean diaspora community — the largest concentration of Cape Verdean immigrants outside Cape Verde is in New Bedford and Brockton, Massachusetts (second largest Cape Verdean community globally after Lisbon). Grogue is imported informally through community networks and occasionally through Portuguese specialty importers. Commercial availability in BC or wider Canada is effectively zero.",
    'markets_served': ['US', 'Portugal'],
    'traditions_carried': ['spirits'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': "Destilaria Royal Grogue Reserva — Santiago Island Aged Cane Spirit, Ex-Bourbon Oak, Volcanic Subtropical Terroir",
    'category': 'spirits',
    'subcategory': 'cane_spirit',
    'origin': 'Cape Verde',
    'region': 'Cape Verde — Santiago Island (Grogue Aged, Oak-Rested Cane Spirit, Colonial Rum Ancestor)',
    'producer': 'Destilaria Royal — Santiago, Cape Verde',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Santiago Island is the largest and most densely populated island in the Cape Verde archipelago, located at 15°N in the North Atlantic off the West African coast — at the same latitude as Dakar, Senegal. The island was uninhabited when Portuguese explorers arrived in 1460 and was immediately established as a trading post and slave transshipment hub in the Portuguese Atlantic commercial system — the capital, Cidade Velha (Ribeira Grande), was the first European colonial city in the tropics and a UNESCO World Heritage Site. Sugarcane cultivation on Santiago began with the first colonial settlers using enslaved West African agricultural labor, establishing the Caribbean-pattern plantation economy that would later be exported to Brazil, São Tomé, and eventually the American colonies. The interior valleys of Santiago (the Serra da Malagueta, rising to 1,394m) receive significantly more rainfall than the arid coast, creating pockets of productive agricultural land in the volcanic island's interior ravines where sugarcane grows at altitude with the combination of tropical sun, Atlantic trade wind moisture, and volcanic mineral soils. The grogue produced from Santiago's highland cane shares the category position of rhum agricole: made from fresh cane juice rather than the molasses by-product characteristic of industrial Caribbean rum, producing a spirit of direct cane terroir expression."
    ),
    'production_technique': (
        "Santiago grogue is produced by expression of fresh-pressed sugarcane juice from the island's interior plantations, fermented with native wild yeast (the subtropical Atlantic yeast population on Santiago produces distinctive funky-fruity fermentation notes different from mainland Brazilian or Caribbean fermentations) in open concrete or stainless steel vats for 3-5 days. Single distillation in traditional copper pot alembics at 60-70% ABV, then proofed with distilled water to 40-50% for bottling. For the aged Reserva expression, Destilaria Royal fills ex-bourbon American oak barrels (200L) and rests the spirit for 18-36 months in the tropical Atlantic climate of Praia — the subtropical temperature (averaging 25°C year-round) drives a rapid wood-spirit interaction comparable to Caribbean rum aging: 18 months in tropical Cape Verde equates approximately to 4-5 years in a Scottish or Irish temperate warehouse. The resulting spirit shows vanilla and caramel from the oak, underlying cane freshness from the juice-based production, and the distinctive Cape Verdean mineral note that traces to the volcanic soils of Santiago's interior. No artificial coloring or flavoring; the amber color comes entirely from the oak contact."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Rhum Agricole AOC Martinique (French Caribbean, fresh cane juice, terroir expression)',
            'connection': "Santiago grogue Reserva and Martinique rhum agricole share the production identity of cane spirits made from fresh-pressed juice rather than molasses — both express the direct terroir of the volcanic island where the cane grows rather than the generic molasses character of industrial rum; the key PCT historical connection is that Cape Verde's grogue predates Martinique's rhum by nearly two centuries, representing the Atlantic colonial ancestor of the entire fresh-cane-juice spirit tradition"
        },
        {
            'tradition': 'Goan Feni (India, fresh palm sap or cashew apple distillate, single distillation)',
            'connection': "Santiago grogue and Goan feni represent the two ends of the Portuguese colonial cane and palm spirit tradition — both are colonial-era distillates produced from fresh agricultural juice (cane on Santiago, cashew or coconut palm on Goa) by techniques established under Portuguese colonial administration, both using traditional pot still single distillation with minimal processing, and both largely unknown outside their home communities despite representing genuinely distinctive terroir spirits"
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale amber-gold from 18-24 months of ex-bourbon oak contact in tropical climate; clear and bright; moderate legs at 40% ABV',
        'nose': 'Fresh cane juice and vanilla from the oak dominate: sugarcane, vanilla, dried tropical fruit, Atlantic sea salt minerality, slight volcanic mineral, caramel from the tropical aging — more direct and less complex than aged Martinique agricole but showing the same fresh cane terroir backbone; a distinctive grassy-mineral note specific to Cape Verde volcanic terroir',
        'palate': 'Medium body; the fresh cane character arrives first, followed by vanilla-caramel from the oak, then the volcanic mineral and sea salt finish that distinguishes Cape Verde production from Brazilian or Caribbean comparators; medium-length finish; warming but not harsh at 40% ABV; the tropical aging has integrated the spirit well without over-oaking',
        'conclusion': 'Age-worthy cane spirit of genuine character; best expression of Cape Verde colonial spirits heritage; serves as cultural reference in PCT programming'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'White Grogue (unaged, traditional)',
            'criteria': 'Clear, unaged Santiago cane spirit; the traditional form consumed locally; strong, raw cane character without oak softening; the category baseline'
        },
        {
            'tier': 2,
            'tier_name': 'Grogue Reserva (6-12 months oak)',
            'criteria': 'Light oak contact in tropical climate; beginning to show vanilla integration with the fresh cane character; accessible entry to aged Cape Verde spirits'
        },
        {
            'tier': 3,
            'tier_name': 'Destilaria Royal Reserva (18-24 months)',
            'criteria': 'Full tropical oak development; cane-vanilla-mineral balance achieved; the benchmark commercial expression of aged Cape Verdean grogue for the export and fine dining market'
        },
        {
            'tier': 4,
            'tier_name': 'Small-Batch Aged Grogue (48+ months)',
            'criteria': 'Extended tropical aging producing rum-comparable complexity; extremely limited production; the artisan tier demonstrating Cape Verde\'s potential for complex oak-aged cane spirits of international standing'
        }
    ],
    'service_intelligence': {
        'temperature': 'Neat at room temperature (20-22°C) for the Reserva — the tropical aging integration benefits from slight warmth that releases the vanilla-cane aromatic complexity; a single drop of water at room temperature opens the spirit for assessment; over ice for the unaged white grogue',
        'vessel': 'Small tulip glass for neat assessment; rocks glass for service with ice or in cocktail use',
        'programme_position': 'Pre-dinner digestif or mid-programme spirits course in a PCT tasting menu; exceptional in a grogue ponche (Cape Verdean grog punch: grogue + honey + lemon + cane sugar) as a cultural service note alongside the colonial history narrative'
    },
    'purveyor_intelligence': {
        'benchmark_producer': "Destilaria Royal Reserva (Santiago) — commercial benchmark; Maio Island family distilleries for artisan comparison; compare to Martinique JM or Clément for the rhum agricole parallel",
        'north_america_access': 'US: diaspora import through Cape Verdean community networks in Massachusetts; no commercial channel in BC or Canada; sourcing for programmatic use requires specialty spirits import',
        'culinary_application': "Cape Verde grogue connects the PCT narrative to the pre-Caribbean colonial cane spirit tradition: service alongside Cachupa (the Cape Verdean national dish — corn, bean, and vegetable stew) or as the base spirit for ponche (the island grog tradition) allows direct engagement with African Atlantic food culture that is almost entirely absent from North American restaurant programming"
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
