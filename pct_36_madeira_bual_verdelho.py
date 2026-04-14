import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Madeira (Bual Medium-Sweet, Volcanic Atlantic, Residual Sugar 50-80g/L)',
    output_dir='.',
    starting_entry=1,
    session_number=38,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': "Blandy's Madeira — Bual Reserve and Colheita",
    'location': 'Funchal, Madeira, Portugal',
    'description': "Blandy's is the oldest continuous Madeira wine producer in family ownership, established 1811 by John Blandy of Dorset. The firm owns the Quinta do Bom Sucesso (Tinta Negra) and sources Bual from the Câmara de Lobos district on Madeira's southern coast — the traditional heartland of Bual cultivation at 150-350m elevation. Blandy's 10-Year-Old Bual is the benchmark medium-sweet Madeira for the international market, aged under estufagem (for the 5-year tier) or canteiro (natural convection aging in warm attics) for 10-year reserves.",
    'founded': '1811',
    'region': 'Funchal/Câmara de Lobos, Madeira',
    'website': 'blandys.com',
    'verified': True
})

session.add_producer({
    'tradition': 'fortified',
    'name': 'Henriques & Henriques — Câmara de Lobos Bual',
    'location': 'Câmara de Lobos, Madeira, Portugal',
    'description': 'Henriques & Henriques is Madeira\'s largest single-estate producer, owning 35 hectares of vineyards including the Quinta Grande estate on Madeira\'s south coast. Founded 1850, the firm is one of the few Madeira shippers that grows a substantial portion of its own grapes rather than purchasing from smallholders. Their Monte Seco dry Sercial and medium Bual are benchmarks for canteiro-aged Madeira.',
    'founded': '1850',
    'region': 'Câmara de Lobos, Madeira',
    'website': 'henriquesehenriques.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Broadbent Selections — Madeira Specialist (US) / Fine Wine Reserve (Canada)',
    'type': 'importer',
    'description': "Broadbent Selections (San Francisco) is the primary US importer for Blandy's Madeira and Henriques & Henriques. In Canada, Madeira is distributed through Fine Wine Reserve (BC) and available through LCBO (Ontario). Blandy's 10-Year Bual is widely available in BC through the BCLDB private import system.",
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['fortified'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': "Blandy's 10-Year-Old Bual — Madeira Medium-Sweet, Canteiro Aging, Volcanic Atlantic Terroir",
    'category': 'fortified',
    'subcategory': 'madeira',
    'origin': 'Portugal',
    'region': 'Portugal — Madeira (Bual Medium-Sweet, Volcanic Atlantic, Residual Sugar 50-80g/L)',
    'producer': "Blandy's Madeira — Bual Reserve and Colheita",
    'alcohol_content': 19.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Bual (Boal) grape variety grows primarily in the Câmara de Lobos district on Madeira\'s southern coast, at 150-350m elevation on steep volcanic terraces built from basaltic lava flows that created the island over the past 5 million years. Câmara de Lobos was Winston Churchill\'s favored painting location and the source of some of Madeira\'s most important Bual vineyards: the warm southern exposure, Atlantic-moderated temperatures, and volcanic mineral-rich soils produce grapes of concentrated sugar content with naturally high acidity (the critical balance for Madeira\'s century-long aging potential). The Atlantic Ocean acts as the fundamental terroir moderator: Madeira sits in the North Atlantic subtropical gyre at 32°N, 17°W — surrounded by ocean on all sides, it experiences no temperature extremes, no frost, and consistent trade wind humidity that allows grapes to achieve full phenolic ripeness without the oxidative stress that would characterize continental viticulture at the same latitude. Bual produces wines with residual sugar of 50-80g/L after fortification (medium-sweet on the Madeira scale, between the drier Verdelho at 35-50g/L and the sweeter Malmsey at 90-120g/L) — a sweetness level that provides the glycerol body needed to carry the oxidative complexity developed over 10-30 years of canteiro aging.'
    ),
    'production_technique': (
        'Bual for Blandy\'s 10-Year is harvested in August-September from the steep terraces of the Câmara de Lobos district, where the volcanic soil retains heat effectively through the Atlantic summer. The hand-picked Bual grapes are crushed and fermented until approximately 6% ABV is reached (for the medium-sweet profile), at which point fermentation is arrested by the addition of 96% grape spirit — the fortification that brings the wine to 19% ABV and preserves the residual sugar at 50-80g/L. The critical differentiator of 10-year quality is canteiro aging: the fortified must is transferred to 600-litre American oak casks and stored in the warm upper-floor attics of the Blandy\'s wine lodge in Funchal, where summer temperatures reach 35-40°C naturally. This thermal cycling — warm in summer, cooler in Atlantic winter — drives the accelerated oxidation and esterification that characterizes Madeira\'s distinctive flavor development, without the artificial heating of the estufagem system (used for 3-5 year tiers). The 10-year designation requires a minimum of 10 years in cask before blending from multiple vintage years; the result is a solera-influenced blend with the complexity of extended oxidative aging but without the vintage variability of single-year expressions. The wine\'s extraordinary stability against further oxidation — Madeira is the only wine in the world that can be recorked and preserved for decades after opening — results from the pre-exhaustion of oxidizable compounds during the canteiro aging process.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Malmsey Madeira (sweeter tier of same island)',
            'connection': "Bual and Malmsey Madeira are the two sweet tiers of the same volcanic island wine tradition, differentiated by residual sugar level (50-80g/L vs 90-120g/L) and grape variety — Bual produces a medium-sweet expression with more pronounced acidity and slightly less glycerol sweetness than Malmsey's honeyed richness, demonstrating how the same canteiro oxidative aging process produces distinctly different sensory outcomes when applied to varieties with different sugar accumulation curves"
        },
        {
            'tradition': 'Sherry Pedro Ximénez (Andalucian oxidative fortified, extreme sweetness)',
            'connection': "Blandy's Bual and Sherry PX both achieve extreme longevity through pre-oxidation during production — PX through raisination of Pedro Ximénez grapes in the Andalucian sun, Bual through canteiro thermal cycling on the Atlantic — both producing fortified wines that resist further oxidation because the oxidizable compounds have already been transformed during production; but where PX achieves its sweetness through sugar concentration, Bual preserves sweetness through fermentation arrest"
        },
        {
            'tradition': 'Colheita Tawny Port (single-vintage oxidative fortified, extended cask aging)',
            'connection': "Blandy's Bual 10-Year and Colheita Tawny Port both undergo extended oxidative cask aging that transforms primary fruit character into complex tertiary flavors (dried fruit, caramel, walnut, spice) — both represent the Portuguese tradition of transforming wine through time and oxygen exposure rather than seeking to preserve primary freshness; the key difference is that Tawny Port retains date-like sweetness while Bual balances residual sugar against the island's characteristic high acidity"
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep amber-mahogany with a distinctive green tinge at the rim — the characteristic Madeira color from decades of oxidative development; bright and clear; viscous legs from the glycerol content at 50-80g/L residual sugar and 19% ABV',
        'nose': 'Complex oxidative aromatics: dried fig and raisin (the primary fruit), caramel and toffee (from Maillard reactions during thermal aging), dried apricot, roasted hazelnut, Atlantic sea air mineral quality, a distinctive rancio note (the French term for the pleasant oxidative staleness of aged fortified wines — buttery, nutty, slightly varnish-like in the best sense), and the characteristic "tangy" high-acid counterpoint that prevents the sweetness from cloying',
        'palate': 'Medium-full body; the residual 50-80g/L sugar is immediately perceptible but balanced by the volcanic island acidity (approximately 7-8 g/L total acidity, high for a fortified wine) that gives Madeira its characteristic "lift" after the sweet entry; intense dried fruit and caramel mid-palate; very long finish with walnut and bitter almond complexity from the rancio development; the acidity persists through the finish, preventing the sweetness from dominating — the defining Bual characteristic',
        'conclusion': 'Medium-sweet with genuine complexity; ready to drink but will develop further over 10-20 more years in bottle; quality level: reserve (10-year canteiro certified)'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Bual (3-year estufagem)',
            'criteria': 'Heated estufagem aging at 45-50°C for 3 months — the industrial Madeira method; produces drinkable medium-sweet wine but lacks the complexity of canteiro; identifiable by the slightly "cooked" character that estufagem imparts versus the natural rancio of canteiro'
        },
        {
            'tier': 2,
            'tier_name': '5-Year-Old Bual (Reserve)',
            'criteria': "Minimum 5 years in cask; blended from multiple vintages; entry to the canteiro quality tier for Blandy's; shows the characteristic Madeira acidity and initial oxidative development without the full complexity of 10+ years"
        },
        {
            'tier': 3,
            'tier_name': '10-Year-Old Bual (Special Reserve)',
            'criteria': "Minimum 10 years canteiro aging; the benchmark Bual expression with full rancio development, dried fruit complexity, and the long acid-sweet finish that defines quality Madeira; Blandy's 10-Year is the international standard-bearer for the style"
        },
        {
            'tier': 4,
            'tier_name': 'Colheita Bual (Single Vintage, 15+ years)',
            'criteria': "Single-vintage Bual aged 15+ years in canteiro; identified by vintage year and bottling date on label; the precision tier showing how a specific harvest year expresses through decades of volcanic-island oxidative aging; extremely limited production, collector-level pricing"
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve slightly chilled at 12-14°C for the 10-year tier — cool enough to emphasize the high volcanic acidity that defines Madeira\'s freshness, but not so cold as to mute the dried fruit and rancio complexity; room temperature (18°C) for very old vintages where cold can suppress complexity',
        'vessel': 'Small tulip glass or ISO tasting glass; the medium-sweet style works with a slightly larger pour than dry Sercial; avoid wide-mouthed dessert glasses that allow excessive oxidation of the already oxidative wine',
        'programme_position': "Classically positioned after dessert or paired with dessert (particularly chocolate, dried fruit tart, almond-based confections) — but also exceptional as a pairing with aged Manchego, Comté, or mature Cheddar, where the Madeira's acidity cuts through the fat and the sweetness complements the crystalline texture of aged cheese"
    },
    'purveyor_intelligence': {
        'benchmark_producer': "Blandy's 10-Year Bual (canteiro, Funchal) — the international benchmark; Henriques & Henriques Medium Bual for estate-grown comparison; D'Oliveiras vintage Bual for colheita depth",
        'north_america_access': "Blandy's widely available through BCLDB private import in BC and specialty wine merchants; available in Ontario through LCBO; in US through Broadbent Selections distribution to all major markets; aging 10-year Madeira increasingly available in Vancouver fine dining wine programs",
        'culinary_application': "The PCT narrative connecting Madeira to Portuguese colonial trade routes makes Bual the natural choice for pairing with Macanese egg tart (pastel de nata), Brazilian brigadeiro (cocoa confection), or São Tomé chocolate — the volcanic island's medium-sweet acidity cuts through the fat of all three while the dried fruit character creates aromatic resonance with the cocoa and vanilla of colonial Portuguese confectionery"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('fortified', 'Portugal — Madeira (Verdelho Semi-Dry, Volcanic Minerality, Residual Sugar 35-50g/L)')

session.add_producer({
    'tradition': 'fortified',
    'name': 'Justino\'s Madeira Wines — Verdelho and Tinta Negra',
    'location': 'Cancela, Madeira, Portugal',
    'description': "Justino's is Madeira's largest producer by volume, operating from a modern winery in Cancela since 2000 while maintaining the canteiro aging lodges in Funchal. Founded 1870 by Justino Henriques, the company was acquired by the French La Martiniquaise group in 1993 but continues to operate under Portuguese management with full focus on the Madeira DOC. Justino's produces the broadest range of Verdelho expressions from entry 3-year to 40-year-old colheita, making them the reference producer for the semi-dry style.",
    'founded': '1870',
    'region': 'Funchal/Cancela, Madeira',
    'website': 'justinosmadeira.com',
    'verified': True
})

session.add_beverage({
    'name': "Justino's 10-Year-Old Verdelho — Madeira Semi-Dry, Volcanic Minerality, Atlantic Trade Wind Aging",
    'category': 'fortified',
    'subcategory': 'madeira',
    'origin': 'Portugal',
    'region': 'Portugal — Madeira (Verdelho Semi-Dry, Volcanic Minerality, Residual Sugar 35-50g/L)',
    'producer': "Justino's Madeira Wines — Verdelho and Tinta Negra",
    'alcohol_content': 19.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "The Verdelho grape is Madeira's second oldest documented variety, referenced in 16th-century records as the grape favored for the island's most important trade wine — the Madeira shipped to the American colonies, India, and Brazil as the primary ballast wine of the Portuguese carreira da India trading fleet. Verdelho vineyards are concentrated at higher elevations than Bual (200-500m on the north coast, particularly in the São Vicente and Porto Moniz districts) where the Atlantic trade winds provide natural ventilation against the fungal pressure of the island's humidity. The volcanic soils at these elevations — weathered basalt with high mineral content, excellent drainage, and significant iron and magnesium — produce grapes with naturally lower sugar accumulation than south-facing Bual and Malmsey vineyards, yielding a lighter-bodied, more mineral, less viscous wine after fortification. The Verdelho style at 35-50g/L residual sugar occupies the space between dry (Sercial, under 35g/L) and medium-sweet (Bual) — a versatile profile that historically made it the most traded Madeira style because it could accompany both savory courses (as an aperitif) and lighter desserts without requiring the full sweet register of Malmsey."
    ),
    'production_technique': (
        "Verdelho grapes are harvested from the high-altitude north coast terraces in late August, where the dramatically different microclimate (cooler, windier, more exposed than the south coast) produces grapes with higher acidity and lower sugar than Bual or Malmsey at the same harvest date. After crushing, the must ferments to approximately 8-9% ABV before fortification with 96% grape spirit — slightly longer fermentation than Bual (which is arrested earlier) because Verdelho's drier target style requires more sugar conversion. The resulting wine at 19% ABV and 35-50g/L residual sugar then enters the canteiro system in the warm attics of Justino's Funchal lodge, where 10 years of thermal cycling transforms the primary fruit character into the complex tertiary aromatics of aged Madeira. The Verdelho style's defining production characteristic is the balance point between acid structure and residual sweetness — the winemaker must arrest fermentation at the precise moment when the acidity (naturally high in north coast Verdelho) and residual sugar (35-50g/L) reach the balance that will remain coherent after decade-scale oxidative development. Too sweet and the wine will lose the mineral freshness that defines quality Verdelho; too dry and it lacks the body to carry 10+ years of canteiro complexity."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Oloroso Sherry (dry oxidative fortified, Palomino grape)',
            'connection': 'Verdelho Madeira and Oloroso Sherry both undergo extended oxidative aging in warm warehouses (Madeira canteiro attics, Sherry bodegas) with periodic topping up to manage evaporation, both producing tertiary complexity (walnut, dried fruit, leather) through the same mechanism of slow controlled oxidation — but Verdelho retains 35-50g/L residual sugar while Oloroso is dry, making the Madeira the more versatile aperitif-to-dessert crossover style'
        },
        {
            'tradition': 'Amontillado Sherry (intermediate dry-oxidative fortified, flor transition)',
            'connection': 'Verdelho Madeira and Amontillado Sherry share the same intermediate sweetness register (both semi-dry) and the same tension between oxidative complexity and preserved freshness — Amontillado achieves this by transitioning from flor protection to open oxidation, while Verdelho achieves it by fortification at the semi-dry point before canteiro thermal cycling; both are considered the most gastronomically versatile of their respective fortified wine traditions'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep amber-tawny; lighter than Bual or Malmsey due to slightly lower glycerol content; characteristic green tinge at the rim; bright and clear with 19% ABV viscosity',
        'nose': 'More mineral and less sweet than Bual: dried green herbs, roasted hazelnut, sea salt minerality, dried citrus peel, rancio (aged fortified wine oxidative quality), dried apricot and fig in the background rather than foreground — the north coast terroir shows as a more austere, mineral aromatic profile versus the rich southern coast',
        'palate': 'Medium body; the entry shows the residual sweetness immediately but the volcanic acidity surges through the mid-palate, creating the characteristic Madeira "tart-sweet" tension that makes it exceptional with food; savory mid-palate (walnut, roasted almond) with dried fruit in the finish; long, slightly bitter almond finish with persistent minerality — the hallmark of quality Verdelho canteiro aging',
        'conclusion': 'Semi-dry with mineral backbone; the most food-versatile Madeira style, capable of serving as aperitif, mid-meal wine with rich fish or poultry, or light dessert accompaniment'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Verdelho 3-Year (estufagem)',
            'criteria': 'Heated estufagem production for entry-level Verdelho; drinkable but lacks the mineral complexity of north coast canteiro aging; cooked character from artificial heating is detectable'
        },
        {
            'tier': 2,
            'tier_name': 'Verdelho 5-Year Reserve',
            'criteria': 'Canteiro minimum 5 years; beginning to develop the mineral-rancio complexity but still primarily in the dried fruit and nut register without the full layering of 10-year expressions'
        },
        {
            'tier': 3,
            'tier_name': "Justino's 10-Year-Old Verdelho",
            'criteria': "Minimum 10 canteiro years; the semi-dry style with full north coast mineral expression and developed rancio complexity; the benchmark for Verdelho served in fine dining as aperitif or food pairing Madeira"
        },
        {
            'tier': 4,
            'tier_name': "D'Oliveiras Colheita Verdelho (single vintage, 20+ years)",
            'criteria': "Single-vintage Verdelho from D'Oliveiras' historic cellars with colheita ranging back to the 1980s–2000s; the precision expression demonstrating vintage character through extended canteiro aging; extremely limited, collector and restaurant allocation only"
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve chilled at 10-12°C as aperitif — the cool temperature emphasizes the volcanic minerality and acid structure that makes Verdelho the most refreshing Madeira style; slightly warmer at 14°C if serving with food',
        'vessel': 'Standard white wine glass or small ISO tasting glass; the semi-dry style benefits from a slightly larger vessel than Malmsey to allow the mineral aromas to develop; avoid very large Burgundy glasses that dilute the concentration',
        'programme_position': "Classically served as aperitif with salted almonds, olives, or Ibérico ham — the semi-dry register and volcanic acidity cut through salt and fat with precision; also exceptional with aged sheep's milk cheese (Castelo Branco, Afuega'l Pitu) and with Pacific smoked salmon or any preparation where a fortified wine's body is needed but a full sweet register would overwhelm"
    },
    'purveyor_intelligence': {
        'benchmark_producer': "Justino's 10-Year Verdelho — the volume benchmark; Blandy's Verdelho for the Funchal lodge style comparison; D'Oliveiras for colheita depth",
        'north_america_access': "Justino's available through specialty importers in US; Madeira Verdelho growing in BC through private import; the semi-dry aperitif style is finding market with restaurants offering pre-dinner Madeira service as an alternative to Sherry in fine dining contexts",
        'culinary_application': "The PCT narrative: Verdelho was the Madeira style most used as ballast wine on the Portuguese carreira da India and the ships that traded along the PCT — reaching Macau, Goa, Mozambique, and Brazil in the same ships that carried spices, textiles, and enslaved people. Service as aperitif with Macanese shrimp paste crostini, Goan prawn balchão, or West African piri-piri preparations creates direct historical resonance with the wine's actual 16th-18th century service contexts"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
