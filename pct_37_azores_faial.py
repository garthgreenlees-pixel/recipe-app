import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Azores (Faial Island, Volcanic Crater Vineyards, Verdelho Descendant Varieties)',
    output_dir='.',
    starting_entry=1,
    session_number=39,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Cooperativa Vitivinícola do Faial — Caldas do Faial',
    'location': 'Caldas do Faial, Faial Island, Azores, Portugal',
    'description': "The Faial cooperative brings together the smallholder vineyard families of Faial Island, where grape growing has continued since the 15th century on the flanks of the Caldeira volcano — a still-geologically-active caldera at the island's center. Faial's vineyards were devastated by the 1957-58 Capelinhos volcanic eruption that covered the western third of the island in ash and lava; the island's wine culture recovered through the 1970s-80s cooperative movement. The primary varieties on Faial are Verdelho (the same variety as Madeira) and Terrantez do Pico (a local red variety), producing wines of exceptional volcanic mineral intensity at very low yields.",
    'founded': '1955 (cooperative reconstituted post-Capelinhos)',
    'region': 'Faial Island, Azores',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Azores Wine Company (Pico) / Borda d\'Água (Faial) — Local Export (EU/US)',
    'type': 'distributor',
    'description': "Faial wines have limited export outside Portugal and the Azorean diaspora in the US (significant Portuguese-American communities in New Bedford MA, Fall River MA, and Newark NJ who import Azorean wines directly). The Azores Wine Company (based on Pico Island but also trading Faial wines) handles the primary export through specialty importers. Availability in BC/Canada is effectively zero through regular channels; special order through Portuguese specialty importers is the only path.",
    'markets_served': ['Portugal', 'US', 'France'],
    'traditions_carried': ['wine'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Faial Island Verdelho Branco — Azores Volcanic White, Post-Capelinhos Terroir, Atlantic Deep-Ocean Minerality',
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Portugal — Azores (Faial Island, Volcanic Crater Vineyards, Verdelho Descendant Varieties)',
    'producer': 'Cooperativa Vitivinícola do Faial — Caldas do Faial',
    'alcohol_content': 12.5,
    'price_tier': 'premium',
    'terroir_origin': (
        "Faial Island sits in the central group of the Azores archipelago at 38°N, 28°W — isolated in the mid-Atlantic at a distance of 1,500km from Portugal and 3,900km from the eastern coast of the US. The island is geologically one of the most active in the Azores: the Caldeira caldera at the center reaches 1,043m and remains volcanically active, while the Capelinhos volcano on the western peninsula erupted spectacularly in 1957-58, adding 2.4 km² of new land to Faial and depositing a thick layer of volcanic ash across the island that, over the subsequent decades, has weathered into some of the most mineral-rich, drainage-perfect agricultural soils in the Atlantic. Faial's vineyards are concentrated on the southeastern slopes below the Caldeira, where the residual geothermal warmth in the basaltic soils promotes root development, and the Atlantic Ocean provides a natural temperature moderator: no frost, consistent humidity from the prevailing southwest trade winds, and year-round cloud cover that slows grape ripening and produces wines of naturally high acidity at modest alcohol levels. The Verdelho variety on Faial is genetically related to Madeira's Verdelho but has adapted over 500 years to Faial's specific conditions: the higher latitude, more oceanic climate, and post-Capelinhos ash soils produce a wine with even greater mineral intensity and lower potential alcohol than its Madeira counterpart."
    ),
    'production_technique': (
        "Faial Verdelho Branco is produced from small-yield hand-harvested grapes from the cooperative's 35-hectare vineyard network around the Caldeira slopes. The volcanic soils require no irrigation — the volcanic rock acts as a moisture reservoir throughout the Atlantic summer — and yields are naturally low at 2-3 tonnes per hectare. The grapes are crushed and fermented in stainless steel at 16-18°C with ambient yeast (the wild yeast population on Faial includes Atlantic-adapted strains that produce distinctive fermentation profiles different from mainland Portuguese yeasts). Fermentation continues to complete dryness, producing a dry white at 12-12.5% ABV with residual carbon dioxide from the cold fermentation preserved in the bottle to provide the slight spritz characteristic of Azorean whites. No oak contact — the wine is bottled directly from stainless steel to preserve the primary volcanic mineral character. The resulting wine is typically released within 8-12 months of harvest for consumption within 2-3 years; unlike Madeira (where the volcanic terroir is transformed by aging), Faial Verdelho is at its best in its fresh expression when the mid-Atlantic minerality and crisp acidity are at their most vivid."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Pico Island Lajido Verdelho (neighboring Azores island, UNESCO landscape)',
            'connection': "Faial and Pico Island Verdelho are produced from the same grape variety separated by only 8km of ocean but on dramatically different soils — Pico's world-famous basalt wall Lajido currais (UNESCO World Heritage landscape since 2004) versus Faial's post-Capelinhos ash deposits; both express the same mid-Atlantic volcanic mineral quality but Pico's basalt gives a more structured, saline mineral while Faial's ash soils produce a lighter, more floral mineral expression"
        },
        {
            'tradition': 'Canary Islands Listán Blanco (Atlantic volcanic island white wine)',
            'connection': "Faial Verdelho and Canary Islands Listán Blanco (Tenerife, Lanzarote) represent parallel Atlantic volcanic island white wine traditions developed under Spanish and Portuguese colonial frameworks respectively — both produce high-acid, low-alcohol whites from varieties adapted to volcanic soils and oceanic climates that have no direct counterpart on the European mainland, and both are slowly emerging from complete obscurity into international specialty wine market recognition"
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale gold with silver-green tints; slight natural turbidity from minimal filtration; fine persistent spritz from residual dissolved CO2 preserved during cold stainless steel fermentation',
        'nose': 'Intense volcanic minerality — wet volcanic rock (petrichor), saline Atlantic sea air, fresh lemon and white grapefruit, green apple, slight white flower; the characteristic Azorean expression where the ocean and volcano work simultaneously on a white wine at the edge of the habitable ripening window',
        'palate': 'Light-medium body; high acidity (the defining structural element at this latitude); light spritz on entry from residual CO2; dry and mineral with citrus fruit mid-palate; saline-mineral finish that lingers; low alcohol (12-12.5%) means the acidity rather than warmth drives the finish — a wine of brisk Atlantic energy rather than Iberian warmth',
        'conclusion': 'Dry, minerally vivid; best within 2-3 years of harvest; quality at estate level from the cooperative\'s best parcels'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Cooperativa Faial White',
            'criteria': 'Blended Verdelho from multiple cooperative members; variable quality depending on individual vineyard management; competent island wine without the precision of the single-slope expressions'
        },
        {
            'tier': 2,
            'tier_name': 'Faial Verdelho Estate Selection',
            'criteria': 'Selected parcels from Caldeira slopes; hand-harvested; the benchmark expression of Faial volcanic mineral character with consistent acid structure and aromatic precision'
        },
        {
            'tier': 3,
            'tier_name': 'Faial Verdelho Single Quinta',
            'criteria': 'Rare single-vineyard expressions from identified basaltic slopes of the Caldeira; extremely limited production (under 1000 bottles); available primarily in Azorean restaurants and to direct buyers'
        },
        {
            'tier': 4,
            'tier_name': 'Azores Wine Company Multi-Island Blend (Pico+Faial)',
            'criteria': "The Azores Wine Company's cross-island expressions blend Pico and Faial fruit to achieve a complexity neither island achieves alone — the benchmark for export-market Azorean wine, widely considered the category's finest achievement and winner of international recognition"
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve very cold at 8-10°C — the volcanic mineral character and high acidity require cold service to show at their best; too warm and the low alcohol leaves the wine feeling thin and acidic without the mineral freshness that defines it',
        'vessel': 'White wine glass or small tulip; the light body and fresh character do not benefit from a large bowl that allows rapid oxidation and temperature rise',
        'programme_position': 'First course wine or aperitif — particularly with shellfish (clams, cockles, percebes barnacles, açorda de mariscos) where the volcanic mineral acidity and slight spritz create the classic Azorean pairing; also exceptional with the local cozido das Furnas (stew slow-cooked in the volcanic hot springs of São Miguel)'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Cooperativa Vitivinícola do Faial — the primary producer; Azores Wine Company (Pico) for cross-island export quality; Casal de Ventozelo for comparison with mainland volcanic expression',
        'north_america_access': 'Effectively unavailable through standard channels in BC or US; Portuguese-American community direct import in Massachusetts (New Bedford) is the primary North American access point; the PCT narrative justifies seeking out through specialist importers for programmatic use',
        'culinary_application': 'Faial wine connects directly to the Azorean-Portuguese diaspora tradition in California and Massachusetts — the largest Portuguese immigrant communities in North America originated from the Azores (particularly Faial, Flores, and São Miguel), making this wine a genuine connection to diaspora food culture rather than a novelty; service with Azorean-influenced clam chowder or linguiça preparations creates authentic community narrative'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
