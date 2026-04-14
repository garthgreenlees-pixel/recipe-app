import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Martinique — Macouba and Basse-Pointe (Neisson AOC, Organic Rhum Agricole, Atlantic Windward Coast)',
    output_dir='.',
    starting_entry=1,
    session_number=55,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Distillerie Neisson — Carbet, Martinique',
    'location': 'Le Carbet, Martinique (French Overseas Department)',
    'description': (
        'Distillerie Neisson is one of the smallest and most artisan producers within the AOC Martinique '
        'rhum agricole appellation, operating from Le Carbet on the western Caribbean coast of Martinique '
        'at the base of the Mont Pelée volcano. Founded in 1931 by the Neisson family, the distillery '
        'operates a single column still — a rare alembic creole column still of the type specified in '
        'the AOC Martinique regulations — and sources certified organic Saccharum officinarum sugarcane '
        'from its own parcels in the Macouba and Basse-Pointe communes on the northern Atlantic-facing '
        'coast of Martinique. Neisson is certified organic (Agriculture Biologique) for both cane '
        'cultivation and distillery operations, making it one of the handful of AOC Martinique producers '
        'with full organic certification. The distillery produces approximately 300,000 bottles annually '
        '— among the smallest AOC Martinique production volumes — and has achieved significant critical '
        'recognition for the intensity of terroir expression in its blanche (unaged) expressions.'
    ),
    'founded': '1931',
    'region': 'Le Carbet / Macouba-Basse-Pointe, Martinique',
    'website': 'neisson.com',
    'verified': True
})

session.add_beverage({
    'name': 'Neisson AOC Rhum Agricole Blanc — Macouba Atlantic Windward, Organic Cane, Alembic Creole Column',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Martinique',
    'region': 'Martinique — Macouba and Basse-Pointe (Neisson AOC, Organic Rhum Agricole, Atlantic Windward Coast)',
    'producer': 'Distillerie Neisson — Carbet, Martinique',
    'alcohol_content': 52.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Macouba and Basse-Pointe communes occupy the northern Atlantic-facing coast of '
        'Martinique — the windward side of the island exposed to the full force of the northeast '
        'Atlantic trade winds that define the climate distinction between the leeward (Caribbean '
        'coast) and windward (Atlantic coast) zones of the Windward Islands. The northernmost '
        'communes of Martinique lie in the rain shadow of the Mont Pelée volcanic massif (1,397m), '
        'which captures the moist Atlantic air masses and releases them as intense orographic '
        'rainfall on the Atlantic-facing slopes: the Macouba zone receives 3,000–4,000mm of annual '
        'rainfall compared to 1,500–2,000mm on the Caribbean-facing western coast. This high '
        'rainfall, combined with the volcanic soils derived from Mont Pelée\'s eruption materials '
        '— andisols and andosols of extraordinary mineral richness from the rapid weathering of '
        'basaltic volcanic tephra — creates the most intensely flavored Saccharum officinarum cane '
        'in Martinique. The Neisson organic parcels in Macouba sit on steep volcanic hillside '
        'terrain at 50–200m elevation, where the drainage through porous volcanic soil concentrates '
        'the cane\'s mineral character while the constant Atlantic trade winds stress the cane '
        'plants in ways that intensify sugar and aromatic compound development. The AOC Martinique '
        'designation (established 1996, the only rum AOC in the world) specifies the precise '
        'geographic zone, permitted cane varieties (Saccharum officinarum or hybrid varieties '
        'approved by the INAO), distillation method (single column still, the alembic creole, '
        'with specific cut point parameters), and minimum aging requirements — creating the most '
        'detailed and protective quality regulation in the global rum category, directly '
        'modeled on the French wine AOC system.'
    ),
    'production_technique': (
        'AOC Martinique rhum agricole production at Neisson begins with the harvest of organic '
        'Saccharum officinarum cane from the Macouba parcels by manual cutting, followed by '
        'immediate transport to the Carbet distillery for pressing within 4–6 hours of cutting '
        '— the critical agricultural timing requirement of the agricole method, ensuring that '
        'the fresh cane juice (vesou) retains maximum volatile aromatic compounds before '
        'fermentation. The vesou is fermented in open stainless steel vats without added '
        'sulfur or temperature control at ambient Martinique temperatures (28–32°C) for '
        '24–30 hours, using a proprietary Neisson yeast culture that the distillery maintains '
        'in continuous production and has evolved in symbiosis with the Macouba cane microbiome '
        'over decades of fermentation. This open-tank, natural-temperature fermentation at '
        'Neisson produces a more complex, slightly higher-ester wash than some AOC competitors '
        'using temperature-controlled closed fermenters — the trade-off being less consistency '
        'batch to batch but greater expression of the Macouba volcanic terroir. The AOC '
        'Martinique column still (alembic creole) is a highly specific piece of equipment: '
        'a single continuous column with a specific internal plate geometry and cooling '
        'system that produces the distillate at a mandated range of 65–75% ABV, preserving '
        'the cane aromatic esters at lower proof than high-efficiency modern column stills '
        'while achieving the consistency of continuous operation. The Neisson Blanc 52.5% '
        'is bottled at cask strength (from still) without dilution or aging — presenting the '
        'raw terroir character of the Macouba volcanic cane through the AOC alembic creole '
        'at its most undiluted and transparent expression. The 52.5% ABV standard (higher '
        'than the 45% minimum for AOC Martinique blanche) reflects the Neisson house position '
        'that the full aromatic impact of the volcanic terroir requires higher proof for '
        'maximum expression.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Chablis Premier Cru (Kimmeridgian limestone, mineral terroir transparency)',
            'connection': (
                'Neisson Blanc 52.5% and Chablis Premier Cru share the defining quality of '
                'mineral terroir transparency in a high-quality unaged or minimally processed '
                'expression: Chablis Kimmeridgian limestone expresses marine-mineral character '
                'through Chardonnay on specific soil, exactly as the Neisson Macouba volcanic '
                'andisol expresses mineral intensity through fresh cane on specific volcanic '
                'terrain. Both are expressions of place in liquid form where the substrate '
                '(limestone mineral solution in wine, volcanic mineral content in fresh vesou) '
                'communicates directly to the palate — the agricultural transparency principle '
                'at the core of both the French AOC wine system and the AOC Martinique rum system.'
            )
        },
        {
            'tradition': 'Calvados AOC Pays d\'Auge (French AOC agricultural spirit, orchard terroir)',
            'connection': (
                'AOC Martinique rhum agricole and Calvados AOC Pays d\'Auge are the two most '
                'technically rigorous French AOC agricultural spirits: both are regulated under '
                'INAO oversight with specific geographic demarcation, approved plant varieties, '
                'mandated distillation equipment and methods, and minimum aging requirements '
                'for aged expressions. Both demonstrate how the French AOC system can be '
                'applied to fruit-based agricultural spirits outside the wine category to '
                'protect geographic and production integrity — Calvados for Norman apple/pear '
                'terroir, rhum agricole for Martinique volcanic cane terroir.'
            )
        },
        {
            'tradition': 'Mezcal Tobalá (wild agave, high-altitude, artisan distillation)',
            'connection': (
                'Neisson organic rhum agricole and Mezcal Tobalá both represent artisan-scale '
                'agricultural spirit production from high-stress, high-terroir substrates — '
                'the Tobalá wild agave at 2,000–2,500m altitude and the Neisson Macouba cane '
                'on steep volcanic hillside terrain — where the extreme growing conditions '
                'concentrate aromatic compounds that column or pot still distillation then '
                'captures and transmits to the drinker. Both are certified-organic '
                'expressions in their respective categories and both command pricing premiums '
                'on the basis of small-scale, terroir-specific production rather than aged '
                'complexity.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Water-clear and brilliant at 52.5% ABV; no color from the unaged AOC blanche '
            'expression; slight oiliness visible on the glass from the higher proof glycerol '
            'and ester content of the full-strength volcanic cane distillate.'
        ),
        'nose': (
            'Intensely vegetal and mineral: raw fresh-cut sugarcane, wet volcanic stone, '
            'a specific green grassy character from Saccharomyces fermentation of Macouba '
            'volcanic-soil cane distinct from lower-mineral-content cane bases; '
            'high-intensity floral esters (ethyl acetate) from the open fermentation at '
            'Martinique ambient temperatures; linalool-driven floral notes from the cane '
            'blossom; the 52.5% ABV delivers these aromatics with intensity that diluted '
            'expressions cannot match — a genuinely volcanic, minerally terroir expression '
            'in a spirit context.'
        ),
        'palate': (
            'Full body from 52.5% ABV; the attack is warm with immediate raw cane intensity '
            'and mineral character from the Macouba volcanic soil — a wet stone and mineral '
            'quality that distinguishes Neisson from Caribbean cane bases on less volcanic '
            'terrain; the open fermentation ester complexity shows through the mid-palate; '
            'the finish is long and warming with the green cane grassiness and volcanic mineral '
            'persisting for 30–45 seconds — an unaged spirit with more terroir transparency '
            'than most aged expressions in any category.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'AOC Martinique generic blanche (45% ABV)',
            'criteria': (
                'The minimum AOC Martinique standard for blanche expressions at 45% ABV: correct '
                'agricole character, fresh cane and light floral, minimal mineral complexity — '
                'the reference baseline for understanding the AOC production method before '
                'evaluating terroir-specific higher-proof expressions like the Neisson 52.5%.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Neisson Blanc 50° (standard export expression)',
            'criteria': (
                'The standard Neisson blanche at 50% ABV: full agricole character from the Macouba '
                'organic parcels at a proof slightly below the 52.5% flagship — the everyday '
                'reference for the Neisson house style and the accessible entry to the Macouba '
                'volcanic terroir without the intensity of the full-proof expression.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Neisson Blanc 52.5° (full proof)',
            'criteria': (
                'The flagship unaged expression at full distillation strength: maximum volcanic '
                'mineral and fresh cane aromatic intensity, open fermentation ester complexity, '
                'Macouba terroir at its most direct and undiluted — the critical reference for '
                'AOC Martinique rhum agricole evaluated against wine AOC standards of terroir '
                'transparency.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Neisson XO (aged 6–12 years, ex-bourbon and French oak)',
            'criteria': (
                'The Neisson aged apex: the Macouba volcanic terroir character preserved through '
                '6–12 years of tropical barrel aging in both ex-bourbon American oak and French '
                'oak, creating a layered spirit in which the volcanic mineral foundation of the '
                'blanche is dressed in tropical dried fruit, vanilla, and fine-grain tannin — '
                'Neisson\'s argument that the Macouba terroir character survives and is enhanced '
                'by extended AOC tropical aging.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve the Neisson Blanc 52.5% at room temperature (20–22°C) without ice for primary '
            'terroir evaluation — the mineral and vegetal character of the Macouba volcanic cane '
            'is most accessible at ambient Caribbean-equivalent temperature; adding 10–15ml of '
            'still water reduces to approximately 45% ABV and opens the floral ester register '
            'while maintaining the mineral core; for ti\' punch service (the canonical French '
            'Antilles presentation: rhum agricole, fresh cane sugar syrup, lime wedge squeezed '
            'and dropped in, no ice), serve at room temperature as the Martinique tradition dictates '
            '— the absence of ice is essential to the ti\' punch expression of rhum agricole character.'
        ),
        'vessel': (
            'A tulip or small wine glass for terroir evaluation at full proof — the constricted '
            'rim focuses the vegetal-mineral-floral volatile complex at the nose; for ti\' punch '
            'service, a small tumbler (verre punch) is traditional and correct; the Neisson '
            'blanche at 52.5% makes an exceptional Daiquiri base where the higher proof and '
            'mineral intensity create a more complex cocktail architecture than standard '
            '40% ABV column-still Caribbean rum alternatives.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Distillerie Neisson (Le Carbet, Martinique) — the organic AOC Martinique benchmark '
            'for volcanic terroir expression in unaged rhum agricole; the 52.5% Blanc is the '
            'critical reference against which other Martinique blanches are evaluated for '
            'mineral intensity and raw cane character; Clément and Saint James are the volume '
            'benchmarks for the wider AOC Martinique appellation.'
        ),
        'north_america_access': (
            'Neisson available in US through Rhum Barbancourt\'s US importers and specialist '
            'agricole-focused distributors; BCLDB private import in BC; limited but growing '
            'Canadian availability through specialty agents; pricing USD $40–55 for the '
            'Blanc 52.5% — premium positioning relative to Barbancourt VSOP but justified '
            'by the organic certification, AOC status, and Macouba terroir specificity.'
        ),
        'culinary_application': (
            'Neisson Blanc 52.5% is the PCT\'s AOC Martinique reference: the French overseas '
            'department status of Martinique (the island is legally France, not a colony or '
            'territory) makes the AOC Martinique the most rigorous protected designation in '
            'the rum category and the strongest argument for applying French AOC terroir '
            'philosophy to agricultural spirits — connecting the PCT colonial trade network '
            'to the French Caribbean in its most institutionally French expression.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
