import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Azores (São Jorge Island, Cliff Vineyards, Fajã Viticulture, Extreme Atlantic Terroir)',
    output_dir='.',
    starting_entry=1,
    session_number=40,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Uniber — União das Adegas das Fajãs de São Jorge',
    'location': 'Topo, São Jorge Island, Azores, Portugal',
    'description': "São Jorge's wine cooperative unites the smallholder producers of the island's unique fajã viticulture — vineyards grown on the narrow lava-flow ledges (fajãs) at sea level below the island's 1,053m cliffs. The fajãs are created when ancient lava flows reached the Atlantic and cooled, forming flat agricultural platforms of 0.5-5 hectares separated by vertical cliff faces, accessible only by footpath or boat. The grapes grown on São Jorge's fajãs — primarily Verdelho, Terrantez do Pico, and the local Barcelo variety — represent one of the world's most extreme terroir situations: at sea level, exposed to Atlantic spray, surrounded by 300m cliff walls that create a unique microclimate warm enough for grape ripening despite the 38°N latitude.",
    'founded': '1988',
    'region': 'São Jorge Island, Azores',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Diálogo Wines — Portugal Specialist (US) / Garrafeira Nacional (PT export)',
    'type': 'importer',
    'description': "São Jorge wines have extremely limited international distribution. Diálogo Wines (US) handles some Azorean wines. In Canada, São Jorge wine is effectively unavailable outside Portuguese specialty stores in Toronto and Montreal. The PCT narrative and extreme terroir story make São Jorge a compelling addition to specialist wine programming despite the sourcing difficulty.",
    'markets_served': ['Portugal', 'US'],
    'traditions_carried': ['wine'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': "São Jorge Fajã de Santo Cristo Verdelho — Extreme Atlantic Cliff Viticulture, Sea-Level Volcanic Ledge, UNESCO-Listed Landscape",
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Portugal — Azores (São Jorge Island, Cliff Vineyards, Fajã Viticulture, Extreme Atlantic Terroir)',
    'producer': 'Uniber — União das Adegas das Fajãs de São Jorge',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "São Jorge Island is one of the most dramatically configured agricultural landscapes on Earth: a narrow ridge of basalt 55km long and 8km wide, rising from sea level to 1,053m in a single continuous slope with no coastal plain. The island's only agricultural land at sea level exists on the fajãs — lava-flow ledges created over thousands of years of volcanic activity where lava rivers reached the Atlantic and solidified into flat platforms 100-500m wide, clinging to the base of the island's vertical sea cliffs. The Fajã de Santo Cristo, on São Jorge's north coast, is the island's most famous viticultural fajã: a 25-hectare lava platform at sea level, surrounded on three sides by 300-400m vertical basalt cliffs and open to the North Atlantic on the fourth side. The unique microclimate of the fajãs results from the cliff-wall protection from prevailing winds combined with the direct reflection of Atlantic sunlight from the water surface — temperatures are significantly warmer than the island's slopes, growing seasons are longer, and humidity from Atlantic spray rather than rain creates a distinctive marine fog culture for the vines. The basalt soils at sea level are rich in minerals from centuries of Atlantic spray deposition, producing wines of extraordinary saline mineral intensity."
    ),
    'production_technique': (
        "São Jorge fajã viticulture is entirely hand-managed — no machinery can access the sea-level ledges except by boat or via the narrow cliff paths. The vines grow in an untrained bush vine formation (pé franco, on their own rootstock since phylloxera never reached São Jorge's remote location) on volcanic basalt soils without any irrigation, their roots reaching deep into the fissured lava for moisture during the dry Atlantic summers. Harvest occurs in September-October, later than Faial or Pico due to the sea-level microclimate's extended growing season; the grapes are carried up the cliff paths in small containers (60kg maximum) by the harvesting teams and transported by boat to the cooperative winery in Topo. Fermentation in stainless steel with native yeast at 16°C preserves the primary saline mineral character; the wine is bottled with approximately 2g/L residual CO2 to maintain freshness. Total annual production of São Jorge fajã wine is under 30,000 bottles, making it among the smallest-production DOC wines in Portugal."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Priorat Garnacha (Spain, extreme slate terroir, tiny yields, cliff viticulture)',
            'connection': "São Jorge fajã wine and Priorat Garnacha share the category of 'extreme terroir viticulture' — vineyards in physically demanding landscapes (São Jorge's sea-level cliff ledges, Priorat's steep llicorella slate slopes) that require entirely manual cultivation, produce tiny yields of intensely mineral fruit, and command premium pricing commensurate with the physical difficulty of production; both are wines where the landscape cost is directly legible in the glass"
        },
        {
            'tradition': 'Santorini Assyrtiko (Greek island, basket vines, sea-salinity, volcanic basalt)',
            'connection': "São Jorge fajã wine and Santorini Assyrtiko represent the two Atlantic and Aegean poles of volcanic island viticulture where the combination of volcanic soils, ambient saline sea air, and traditional bush vine training (kouloura in Santorini, pé franco in São Jorge) produces white wines of extreme mineral salinity that cannot be replicated in continental wine regions — both are genuine expressions of how proximity to the sea transforms basalt and granite terroir into a saline mineral register in the glass"
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale straw with silver highlights; fine persistent spritz; clear with natural turbidity from minimal filtration; extremely light body for a white wine of this mineral intensity',
        'nose': 'Atlantic sea spray and volcanic rock dominate: iodine, sea salt, wet basalt, lemon pith, white flower, slight green herb; the saline character is more pronounced than Faial or Pico due to the sea-level cliff exposure of the fajã — this is one of the most clearly marine-influenced white wine aromas in the world',
        'palate': 'Very high acidity; bone dry; the saline mineral character arrives immediately with the acidity and persists through a long, salty finish; citrus and white flower mid-palate; very low alcohol (11.5-12%) means the finish is driven entirely by acidity and mineral salt rather than warmth — extremely refreshing and precise',
        'conclusion': 'Rare expression of extreme Atlantic cliff viticulture; exceptional with shellfish and Atlantic seafood; quality level: estate from the fajã de Santo Cristo parcels'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'São Jorge Island White (non-fajã slopes)',
            'criteria': 'Grapes from the island slopes above the cliff-level fajãs; competent volcanic white without the extreme saline intensity of sea-level production; standard cooperative blend'
        },
        {
            'tier': 2,
            'tier_name': 'São Jorge Fajã Blend',
            'criteria': 'Blended fruit from multiple fajãs; captures the saline character of sea-level production without the precision of a single fajã expression'
        },
        {
            'tier': 3,
            'tier_name': 'Fajã de Santo Cristo Single-Ledge Verdelho',
            'criteria': "The benchmark São Jorge expression from the island's most famous fajã; identified by fajã name on label; extreme saline mineral character with the full Atlantic sea-level terroir expression"
        },
        {
            'tier': 4,
            'tier_name': 'Azores Wine Company "Fajã dos Vimes" (rare collaboration)',
            'criteria': "Collaborative production between São Jorge's cooperative and the Azores Wine Company applying premium production standards to the island's most historic fajã; essentially unavailable outside Portugal and specialized collector markets"
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve ice cold at 6-8°C — the extreme saline minerality and very high acidity require the coldest service of any white wine in this collection; the wine opens up and softens to a vivid saline expression as it warms in the glass over 10-15 minutes',
        'vessel': 'Small white wine glass or tulip; the saline intensity and light body do not need a large bowl',
        'programme_position': 'First course exclusively — with raw shellfish, clams, percebes (goose barnacles), ceviche, or any dish where saline mineral acidity is the primary pairing driver; an extraordinary aperitif for any seafood-driven tasting menu'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Uniber São Jorge fajã production — the only consistent producer; Azores Wine Company for the cross-island blended access point',
        'north_america_access': 'Effectively unavailable in North America through standard channels; the PCT research and extreme terroir context justify including as a reference entry even without practical sourcing; Portuguese specialty importers occasionally bring small allocations',
        'culinary_application': "São Jorge is also famous for its aged raw milk cheese (Queijo São Jorge DOP — a semi-hard cheese aged 3-6 months with a firm grain and peppery bite) which pairs exceptionally with the island wine; the combination represents the complete island terroir narrative: both wine and cheese from the same volcanic ledges, both expressing the Atlantic mineral identity of the fajã landscape"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Portugal — Azores (Graciosa Island, Limestone Terroir, Anizeto and Fernão Pires Varieties)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Adega Cooperativa de Graciosa — Fontes and Luz Parishes',
    'location': 'Santa Cruz da Graciosa, Graciosa Island, Azores, Portugal',
    'description': "Graciosa is the flattest and driest island in the Azores — unlike the dramatically volcanic Pico, Faial, and São Jorge, Graciosa's landscape is dominated by limestone and tuff rather than basalt, creating a fundamentally different terroir from the other Azorean wine islands. The Graciosa cooperative has been producing wine since 1969 and manages approximately 120 hectares of vineyards growing the local Anizeto (white) and Agudelo varieties unique to Graciosa, as well as mainland Portuguese varieties including Fernão Pires. The island's caldera (the Furna do Enxofre — a volcanic cave lake) and limestone soils produce wines of greater roundness and lower acidity than the purely basaltic islands.",
    'founded': '1969',
    'region': 'Graciosa Island, Azores',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Graciosa Anizeto Branco — Limestone-Volcanic Atlantic Island White, Local Heritage Variety, Pre-Phylloxera Survivor',
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Portugal — Azores (Graciosa Island, Limestone Terroir, Anizeto and Fernão Pires Varieties)',
    'producer': 'Adega Cooperativa de Graciosa — Fontes and Luz Parishes',
    'alcohol_content': 12.5,
    'price_tier': 'estate',
    'terroir_origin': (
        "Graciosa Island occupies a unique position within the Azorean archipelago as the least volcanic and most geologically stable island in the central group. Where Pico, Faial, and São Jorge are dominated by recent basaltic lavas (in geological terms — the last 5,000-50,000 years), Graciosa's bedrock is predominantly tuff and limestone from earlier volcanic activity, creating agricultural soils with a fundamentally different mineral profile: more calcareous, better water retention, and less purely basaltic than the neighboring islands. The island's relatively flat terrain and calcareous soils produce a completely different wine character from the extreme volcanic expressions of São Jorge or Pico: the Anizeto variety, unique to Graciosa and thought to be a pre-phylloxera survivor from the island's 15th-century Portuguese settlement, produces wines with greater body and roundness than the high-acid, mineral-dominant styles of the basaltic islands. Graciosa's climate is the driest in the Azores — the limestone topography drains quickly, requiring the island's vine roots to penetrate deeply for moisture, producing the same drought-stressed concentration mechanism seen in limestone wine regions of southern Portugal and Spain."
    ),
    'production_technique': (
        "The Anizeto grape on Graciosa grows on its own rootstock (pé franco — phylloxera never reached the island's isolation) on calcareous-volcanic soils in traditional low-trained bush vine formation. Harvest in September-October by hand; fermentation in stainless steel with selected yeast at 17-19°C. The limestone-influenced soils produce a less acidic, rounder wine than the purely basaltic islands: natural acidity runs approximately 5.5-6.5 g/L total acidity versus 7-8 g/L in Pico or São Jorge Verdelho. The cooperative blends Anizeto with small amounts of Fernão Pires (imported variety from mainland Portugal, used to add aromatic lift to the rounder Anizeto structure) before bottling. The result is a white wine that bridges the austere volcanic mineral style of São Jorge and Pico with the warmer, more aromatic character of mainland Portuguese whites — unique to Graciosa and difficult to replicate elsewhere."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Vinho Verde (mainland Portugal, lime-rich granitic and schist soils, Atlantic influence)',
            'connection': "Graciosa Anizeto and Vinho Verde share the category of Atlantic-influenced Portuguese white wines grown on calcareous-influenced soils, both producing fresh, aromatic whites of moderate alcohol with natural effervescence — but where Vinho Verde's character comes from the humid Minho River valley granite, Graciosa's derives from the intersection of Atlantic ocean and volcanic-limestone island terroir, making the comparison useful for showing how a shared climatic influence (Atlantic) produces different mineral expressions on limestone versus granite"
        },
        {
            'tradition': 'Santorini Nykteri (Assyrtiko, late-harvest, richer style, volcanic limestone)',
            'connection': "Graciosa Anizeto and Santorini Nykteri both represent the fuller, rounder style of volcanic island white wines — compared to the extreme lean austerity of the basaltic Santorini barrel Assyrtiko or São Jorge Verdelho, both Graciosa and Nykteri benefit from limestone influence to add roundness to the volcanic mineral backbone, demonstrating how the limestone versus basalt spectrum within volcanic wine regions produces fundamentally different body profiles"
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale gold with golden-green tints; slightly deeper color than Faial or São Jorge whites due to the warmer limestone terroir and richer grape variety; clear; moderate legs at 12.5% ABV',
        'nose': 'Rounder and more aromatic than the other Azorean whites: white peach, apricot, honeysuckle, green apple, crushed limestone dust, slight volcanic mineral in the background — the Anizeto variety contributes a stone fruit aromatic profile that distinguishes Graciosa from the more austere citrus-mineral profile of basaltic island wines',
        'palate': 'Medium body (fuller than São Jorge or Faial); medium-high acidity but notably rounder than the purely basaltic islands; dry with a slight stone fruit mid-palate; limestone mineral finish with less aggressive salinity than sea-level fajã wines; medium length',
        'conclusion': 'Competent, distinctive island white; best expression of how limestone-volcanic soils produce different Azorean character; drink within 3 years'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Graciosa White (cooperative blend)',
            'criteria': 'Blended Anizeto and Fernão Pires without parcel selection; accessible island wine for local consumption'
        },
        {
            'tier': 2,
            'tier_name': 'Graciosa Anizeto Single Variety',
            'criteria': 'Pure Anizeto variety from selected calcareous parcels; the heritage variety expression showing the distinctive stone fruit-mineral character of Graciosa vs. the basaltic islands'
        },
        {
            'tier': 3,
            'tier_name': 'Graciosa Reserva (barrel-aged Anizeto)',
            'criteria': 'Anizeto aged briefly in second-use Portuguese oak adding breadth to the limestone mineral character without compromising the island freshness; rare, essentially unavailable outside the Azores'
        },
        {
            'tier': 4,
            'tier_name': 'Graciosa Colheita Tardia (late-harvest)',
            'criteria': 'Extremely rare late-harvest Anizeto showing the botrytis potential of the limestone-influenced warmer island; under 500 bottles per year when produced; collector-only'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 10-12°C — slightly warmer than the more austere basaltic island whites due to the rounder body and stone fruit aromatics that benefit from a degree or two more',
        'vessel': 'Standard white wine glass; moderate bowl size appropriate for the medium body',
        'programme_position': 'Versatile first or second course wine; works well with grilled fish, mild aged Azorean cheese (Queijo da Ilha — São Jorge DOP but available throughout the archipelago), and any preparation where a rounder, more aromatic Atlantic white is appropriate versus the extreme minerality of São Jorge or Pico'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Adega Cooperativa de Graciosa — only commercial producer; small quantities occasionally appear in Portuguese specialty wine merchants in Lisbon and Porto',
        'north_america_access': 'Essentially unavailable; research and reference use in PCT programming; order through Portuguese wine specialist for single-case allocations',
        'culinary_application': 'The Graciosa terroir narrative connects to the broader Azorean wine culture that is slowly gaining international recognition through the Azores Wine Company (Pico) success — positioning Graciosa as the limestone counterpoint to Pico\'s basalt creates compelling programmatic contrast within a single Azorean wine course'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
