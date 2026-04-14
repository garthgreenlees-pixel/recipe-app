import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

# Fix: São Jorge entry was flagged for 'platform' in terroir text. Resume session (entry will be -002).
session = BeverageSession(
    tradition='wine',
    region='Portugal — Azores (São Jorge Island, Cliff Vineyards, Fajã Viticulture, Extreme Atlantic Terroir)',
    output_dir='.',
    starting_entry=1,
    session_number=47,
    running_total=0
)

session.add_beverage({
    'name': "São Jorge Fajã de Santo Cristo Verdelho — Extreme Atlantic Cliff Viticulture, Sea-Level Lava Ledge, UNESCO-Listed Landscape",
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Portugal — Azores (São Jorge Island, Cliff Vineyards, Fajã Viticulture, Extreme Atlantic Terroir)',
    'producer': 'Uniber — União das Adegas das Fajãs de São Jorge',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "São Jorge Island is one of the most dramatically configured agricultural landscapes on Earth: a narrow ridge of basalt 55km long and 8km wide, rising from sea level to 1,053m in a single continuous slope with no coastal shelf. The island's only agricultural land at sea level exists on the fajãs — lava-flow ledges created over thousands of years of volcanic activity where lava rivers reached the Atlantic and solidified into flat agricultural terraces of 100-500m width, clinging to the base of the island's vertical sea cliffs. The Fajã de Santo Cristo, on São Jorge's north coast, is the island's most famous viticultural fajã: a 25-hectare lava terrace at sea level, surrounded on three sides by 300-400m vertical basalt walls and open to the North Atlantic on the fourth side. The unique microclimate of the fajãs results from the cliff-wall protection from prevailing winds combined with the direct reflection of Atlantic sunlight from the water surface — temperatures are significantly warmer than the island's slopes, growing seasons are longer, and humidity from Atlantic spray rather than rain creates a distinctive marine fog culture for the vines. The basalt soils at sea level are rich in minerals from centuries of Atlantic spray deposition, producing wines of extraordinary saline mineral intensity."
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
            'connection': "São Jorge fajã wine and Santorini Assyrtiko represent the two Atlantic and Aegean poles of volcanic island viticulture where the combination of volcanic soils, ambient saline sea air, and traditional bush vine training (kouloura in Santorini, pé franco in São Jorge) produces white wines of extreme mineral salinity that cannot be replicated in continental wine regions — both are genuine expressions of how proximity to the sea transforms basalt terroir into a saline mineral register in the glass"
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale straw with silver highlights; fine persistent spritz; clear with natural turbidity from minimal filtration; extremely light body for a white wine of this mineral intensity',
        'nose': 'Atlantic sea spray and volcanic rock dominate: iodine, sea salt, wet basalt, lemon pith, white flower, slight green herb; the saline character is more pronounced than Faial or Pico due to the sea-level cliff exposure of the fajã — among the most clearly marine-influenced white wine aromas in the world',
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
        'culinary_application': "São Jorge is also famous for its aged raw-milk cheese (Queijo São Jorge DOP — a semi-hard aged 3-6 months with a firm grain and peppery bite) which pairs exceptionally with the island wine; the combination represents the complete island terroir narrative: both wine and cheese from the same volcanic ledges, both expressing the Atlantic mineral identity of the fajã landscape"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
