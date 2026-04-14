import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Brazil — Minas Gerais (Cachaça Alambique, Pot Still Artisan, Sugarcane Terroir, Salinas de Minas)',
    output_dir='.',
    starting_entry=1,
    session_number=65,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Weber Haus and Cachaça Artesanal Producers — Salinas, Norte de Minas, Minas Gerais',
    'location': 'Salinas, Norte de Minas region, Minas Gerais State, Brazil',
    'description': (
        'Salinas (full name: Salinas de Minas) is a municipality in the Norte de Minas '
        'region of northern Minas Gerais State that has achieved the status of the most '
        'celebrated cachaça production town in Brazil — producing at its height over 800 '
        'registered alambique (artisan pot still) operations within the municipality and '
        'its surrounding zone, more cachaça producers per capita than any comparable '
        'location in the world. The Salinas tradition produces almost exclusively '
        'alambique cachaça (pot still, single distillation from fermented fresh sugarcane '
        'juice), in contrast to the industrial cachaça (Cachaça Industrial, column-still, '
        'mass-produced) that accounts for 95%+ of Brazil\'s total cachaça volume. '
        'Weber Haus (full name: Engenho Weber Haus) represents the artisan Salinas '
        'tradition at its apex — founded in 1972 in São Leopoldo, Rio Grande do Sul '
        'but with Minas Gerais artisan cachaça methodology as its reference standard. '
        'The most celebrated Salinas producers include Havana, Anísio Santiago '
        '(producer of the legendary Havana 40-year aged cachaça), and the '
        'Sagatiba Pura Minas Gerais production collaborative.'
    ),
    'founded': '18th century (Salinas alambique tradition); current major producers from 1930s–1970s',
    'region': 'Salinas, Minas Gerais, Brazil',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Avua Cachaça / Leblon Cachaça (US importers, artisan Brazil)',
    'type': 'importer',
    'description': (
        'Avua Cachaça (New York) is the primary US importer of barrel-aged artisan '
        'alambique cachaça, importing the Avua Amburana and Avua Balsam expressions '
        'from pot still producers in Rio de Janeiro State and Minas Gerais. '
        'Leblon Cachaça (Cognac-owned, mass distribution) handles the mid-tier '
        'commercial alambique sector. For the Salinas artisan tradition specifically, '
        'specialty spirits importers including Sagatiba and Copa Cachaça handle '
        'small-batch Minas Gerais alambique lots for the US on-premise specialty market. '
        'Canadian availability through BCLDB (BC) and LCBO (Ontario) for Leblon and '
        'Avua; artisan Salinas expressions through specialty private import agents.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['spirits'],
    'website': 'avuacachaca.com',
    'verified': False
})

session.add_beverage({
    'name': (
        'Cachaça Alambique Envelhecida — Salinas de Minas, Minas Gerais, '
        'Pot Still Artisan, Amburana Wood Aging, Sugarcane Terroir Norte de Minas'
    ),
    'category': 'spirits',
    'subcategory': 'cachaca',
    'origin': 'Brazil',
    'region': 'Brazil — Minas Gerais (Cachaça Alambique, Pot Still Artisan, Sugarcane Terroir, Salinas de Minas)',
    'producer': 'Weber Haus and Cachaça Artesanal Producers — Salinas, Norte de Minas, Minas Gerais',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Salinas sits at 16.2°S latitude in the Norte de Minas region at 880m elevation '
        'in the São Francisco River drainage basin — a transitional zone between the '
        'Atlantic Forest biome of the Minas Gerais highlands and the caatinga (dry '
        'scrubland) biome of Bahia and Pernambuco to the north. The Norte de Minas '
        'climate is semi-arid relative to the main Minas Gerais coffee zone: annual '
        'rainfall 800–1,100mm concentrated in the November–March wet season, with '
        'a pronounced dry season from April to October during which Saccharum '
        'officinarum (sugarcane) achieves its maximum sugar concentration from '
        'water stress. The sugarcane variety cultivated for Salinas alambique '
        'cachaça is predominantly RB92579 and SP791011 — varieties selected for '
        'the semi-arid Norte de Minas growing conditions rather than maximum yield, '
        'which in industrial Minas Gerais production would prioritize ethanol output '
        'from the most productive cane varieties. The soil type at Salinas is '
        'deep red-yellow latosol over crystalline rock basement — well-drained, '
        'iron-rich, with low natural fertility that forces extensive root system '
        'development and concentrates sugarcane flavour compounds. The town\'s '
        'fame as Brazil\'s cachaça capital is documented in the Museu da Cachaça '
        'in Salinas, which houses over 5,000 bottles of artisan production and '
        'serves as the institutional center for the Indicação Geográfica (IG) '
        'petition for Cachaça de Minas Gerais that received federal GI recognition '
        'in 2012 — the first agricultural spirits GI in Brazil. Anísio Santiago\'s '
        'Havana cachaça, produced in Salinas from the same location since the 1960s '
        'and aged in 40-year wooden tonéis, is the most celebrated single expression '
        'of the Salinas tradition and commands prices comparable to Scotch single '
        'malt ultra-aged expressions.'
    ),
    'production_technique': (
        'Salinas artisan alambique cachaça begins with fresh-cut sugarcane crushed '
        'on-site at the engenho (mill) within 24 hours of harvest to prevent '
        'enzymatic degradation of the fermentable sugars. The garapa (fresh sugarcane '
        'juice) at 17–22 Brix is transferred directly to fermentation vessels — '
        'the traditional choice is clay or wooden vats (dornas), often built from '
        'native Brazilian hardwoods (jequitibá, cedro, amburana) that contribute '
        'botanical complexity to the fermentation through wood compound extraction. '
        'Wild ambient yeast cultures dominate in the traditional Salinas engenhos, '
        'supplemented by a "pé-de-cuba" (foot of the cask) — the retained heel '
        'of the previous fermentation, containing the producer\'s house yeast '
        'population developed over decades. Fermentation is non-temperature-controlled '
        'at ambient Salinas temperature (25–32°C during harvest season), taking '
        '18–36 hours for primary fermentation to complete to approximately 7–9% '
        'ABV wash. The rapid fermentation at warm temperatures produces a wine '
        '(vinho) with higher ester concentration than slow, cool-fermented '
        'industrial cachaça wash — a characteristic that drives the volatile '
        'aromatic profile of artisan alambique cachaça. Single distillation takes '
        'place in copper pot stills (alambiques de cobre) of 50–500 liter capacity '
        'at a single pass from 7–9% ABV wash to a cut of 38–55% ABV spirit. '
        'The distiller makes three cuts: the heads (cabeça, discarded — approximately '
        '5–10% of total volume) containing the highest-boiling volatile acids; '
        'the heart (coração, retained for cachaça), and the tails (cauda, partially '
        'retained depending on producer style). The heart cut at 38–45% ABV is '
        'the basis for unaged (branca/prata) cachaça; for aged (envelhecida) '
        'cachaça, the heart is transferred to wooden casks for aging. The most '
        'distinctive Salinas aging wood is amburana (Amburana cearensis, also '
        'called Brazilian spice tree or "cumaru de cheiro") — a native '
        'Brazilian hardwood that imparts intense cinnamon, vanilla, clove, and '
        'anise character to cachaça through the transfer of coumarin, vanillin, '
        'and linalool from the wood during aging. Amburana-aged Salinas cachaça '
        'achieves its characteristic profile in 1–3 years that other wood species '
        'require 8–12 years to achieve — the native Brazilian wood creating a '
        'unique flavor development pathway unavailable to non-Brazilian spirits '
        'traditions. Additional aging woods used in Salinas include carvalho '
        '(Brazilian oak, Quercus species), ipê (Tabebuia avellanedae, dark iron '
        'wood), and bálsamo — each imparting distinct character to the base '
        'cachaça spirit.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Rhum agricole (Martinique AOC, fresh cane juice distillation)',
            'connection': (
                'Both Brazilian alambique cachaça and Martinique rhum agricole are '
                'produced by the immediate distillation of fresh sugarcane juice '
                '(rather than molasses), making both the global alternative to '
                'molasses-based rum in the fresh-cane spirits category. The '
                'fresh-cane juice base gives both spirits a characteristic green '
                'vegetal, grassy, earthy character that molasses rum does not '
                'possess — the terroir expression of fresh sugarcane directly '
                'in the spirit. The distinction between the traditions is the '
                'distillation equipment: Martinique rhum agricole uses a Creole '
                'column still (one rectification column) at 65–70% ABV distillation '
                'strength; Salinas alambique cachaça uses copper pot stills at '
                '38–55% ABV — the lower distillation strength of the pot still '
                'retaining more congeners and creating the greater aromatic '
                'complexity that defines artisan cachaça quality.'
            )
        },
        {
            'tradition': 'Cognac (Charentais pot still, native wood aging, Appellation Controlée)',
            'connection': (
                'The Salinas alambique cachaça tradition parallels Cognac in three '
                'dimensions: artisan copper pot still production in a defined '
                'geographic area; wood-aging that transforms the base spirit through '
                'extractive compounds unique to the native wood species (amburana '
                'cinnamon-vanilla paralleling Limousin and Tronçais oak tannin '
                'in Cognac); and a GI protection system (Cachaça de Minas Gerais '
                'IG 2012; Cognac AOC) that formalizes the geographic-quality '
                'connection. Anísio Santiago\'s 40-year Havana cachaça commands '
                'Cognac XO pricing in specialist markets, demonstrating that '
                'the quality premium of long-aged artisan cachaça has reached '
                'international benchmark standing.'
            )
        },
        {
            'tradition': 'Goa feni (Portuguese colonial India, coconut sap pot still)',
            'connection': (
                'Both Salinas alambique cachaça and Goa coconut feni are single-'
                'distillation pot still spirits produced within the Portuguese '
                'colonial trade zone from fresh tropical plant sap (sugarcane '
                'in Brazil; coconut palm in Goa) by hereditary communities '
                'using clay and copper pot stills in geographic GI-protected '
                'regions. The Portuguese colonial introduction of copper alembic '
                'distillation technology to both Brazil (16th century) and Goa '
                '(16th century) created parallel artisan pot still traditions '
                'on opposite sides of the world that both survive as distinct '
                'GI-protected spirits in 2026.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Amburana-aged Salinas cachaça: warm gold to deep amber depending on '
            'aging duration; 1-year amburana shows pale gold with yellow tints; '
            '3-year amburana shows deep amber comparable to 8-year bourbon '
            'from the rapid color extraction of amburana wood; brilliant clarity '
            'from careful filtration; good legs at 40% ABV reflecting the pot '
            'still glycerol contribution; color intensity more rapid than oak '
            'aging due to amburana\'s higher extractable compound concentration.'
        ),
        'nose': (
            'The amburana dominance is immediate and distinctive: cinnamon spice, '
            'vanilla, anise, dried orange peel from coumarin, vanillin, and linalool '
            'wood extraction in the first pass; beneath the amburana character, '
            'the fresh sugarcane base provides green tropical fruit (fresh sugar '
            'cane, ripe mango, overripe banana) from the garapa fermentation '
            'volatile esters; ester fruit from the warm wild-yeast fermentation '
            '(ethyl acetate, isoamyl acetate); the combination of fresh-cane '
            'fermentation esters and amburana wood spice is unique in the global '
            'spirits landscape — no other spirit category replicates this specific '
            'aromatic register.'
        ),
        'palate': (
            'Medium body with warmth from 40% ABV; the amburana cinnamon and '
            'vanilla from wood aging arrive with the first sip and define the '
            'structural character; the fresh sugarcane ester fruit from pot '
            'still distillation supports the mid-palate with tropical fruit '
            'and green cane sweetness; tannin from the amburana wood is soft '
            'and rounded compared to oak tannin — the amburana imparts spice '
            'character without astringency; medium-long finish with cinnamon '
            'and vanilla lingering; the distinctive quality of Salinas alambique '
            'amburana cachaça is the integration of wood spice and fresh cane '
            'terroir in a single spirit that demonstrates both the fermentation '
            'base and the aging wood simultaneously.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Cachaça Industrial (column still, Pirassununga, São Paulo)',
            'criteria': (
                'Column still production from molasses or industrial sugarcane '
                'juice at 96% ABV rectified spirit; proofed with distilled water '
                'and bottled without aging — the Cachaça 51 and Velho Barreiro '
                'commercial tier; high volume, no terroir or wood character; '
                'the baseline definition of the category without artisan quality.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Cachaça Alambique Branca (unaged pot still)',
            'criteria': (
                'Fresh-cane juice single pot still distillation bottled without '
                'wood aging — the Salinas prata (silver) tier; full fresh-cane '
                'ester character, no wood contribution; the authentic expression '
                'of terroir and yeast without the transformation of aging; '
                'represents the base cachaça as distilled before artisan '
                'producers develop it through wood aging.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Cachaça Alambique Envelhecida em Amburana (1–3 years)',
            'criteria': (
                '1–3 years amburana wood aging of Salinas pot still cachaça: '
                'the benchmark Salinas expression — cinnamon, vanilla, and anise '
                'wood character integrating with fresh-cane ester fruit; the '
                'Avua Amburana and Leblon premium tier in this range; the '
                'reference for international cocktail and on-premise specialty '
                'cachaça programmes.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Anísio Santiago Havana (40-year, Salinas apex)',
            'criteria': (
                'The most celebrated single expression of Salinas cachaça: Anísio '
                'Santiago\'s Havana, aged 40 years in amburana and carvalho wood '
                'tonéis in the same Salinas cellar — deep amber, extraordinary '
                'integration of wood spice and fresh-cane heritage, complex dried '
                'fruit and leather development from four decades of tropical aging; '
                'limited allocation, collector pricing at USD $200–400 per bottle; '
                'the reference that establishes artisan cachaça as a world-class '
                'aged spirits category independent of comparison to whisky or Cognac.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Artisan alambique cachaça envelhecida at 18–20°C for neat evaluation '
            'to appreciate the amburana wood spice and fresh-cane ester character '
            'at full volatility; the amburana vanilla-cinnamon aromatic profile '
            'shuts down below 15°C and becomes harsh above 22°C — the window is '
            'narrow and intentional. For the Caipirinha (Brazil\'s canonical '
            'mixed drink: cachaça, fresh lime, cane sugar, ice), use unaged '
            'branca cachaça at ambient temperature with crushed ice — the Caipirinha '
            'must not use aged amburana cachaça, as the wood character competes '
            'destructively with the fresh lime acidity. The aged envelhecida '
            'is a sipping spirit, not a mixing spirit.'
        ),
        'vessel': (
            'For neat sipping: Glencairn or tulip glass to concentrate the '
            'amburana aromatic intensity at the rim; a small water addition '
            '(5ml in 40ml pour) opens the cinnamon-spice character by reducing '
            'alcohol surface tension — more effective for amburana cachaça than '
            'for any other spirit category due to the coumarin water-solubility. '
            'For programme tasting: 25ml pour in white-interior ISO tasting glass '
            'to assess color, nose, and palate structure sequentially. For cocktail '
            'use (unaged branca): the traditional Caipirinha glass — old-fashioned '
            'rocks glass (250–300ml) with crushed ice to dilute appropriately.'
        ),
        'programme_position': (
            'In a PCT Brazil spirits programme: serve after Brazilian sparkling '
            'wine and before coffee — the amburana spice and tropical fruit '
            'of aged cachaça bridges between the wine\'s yeast and fruit '
            'character and the coffee\'s roast intensity. In a pure spirits '
            'programme, the Salinas aged cachaça is the emotional centerpiece: '
            'explaining amburana wood as a uniquely Brazilian ingredient '
            'unavailable outside South America makes the cachaça category '
            'irreplaceable rather than substitutable.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Anísio Santiago — Havana Cachaça, Salinas, Minas Gerais '
            '(the undisputed apex of artisan Brazilian cachaça; 40-year aged '
            'expression is the reference benchmark for the category); '
            'Avua Amburana (pot still, amburana-aged, commercially available '
            'internationally) as the accessible benchmark for artisan '
            'amburana cachaça in the North American market.'
        ),
        'north_america_access': (
            'Avua Cachaça (Amburana and Balsam expressions) widely available '
            'in US specialty spirits retailers and BCLDB/LCBO Canada; '
            'retail USD $40–65. Leblon Reserva (pot still aged) available '
            'at USD $35–45. Anísio Santiago Havana available through '
            'specialty Brazilian spirits importers in New York and São Paulo; '
            'USD $200–400 depending on age statement and allocation. '
            'Sagatiba Velha (Minas Gerais alambique) through specialty '
            'importers at USD $50–70.'
        ),
        'culinary_application': (
            'In PCT culinary programming, amburana-aged Salinas cachaça is '
            'served with Brazilian desserts featuring cinnamon and caramel '
            '(doce de leite, canjica) to demonstrate the wood-spice to '
            'dessert pairing that makes amburana cachaça uniquely suited '
            'to Brazilian cuisine accompaniment; the spirit also bridges '
            'to Portuguese custard tarts (pastel de nata) for a within-'
            'PCT colonial culinary connection between Brazil and Portugal.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
