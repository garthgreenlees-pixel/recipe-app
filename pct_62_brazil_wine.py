import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Brazil — Campanha Meridional (Lidio Carraro Quorum, Uruguayan Border, Pampa Grassland Wine)',
    output_dir='.',
    starting_entry=1,
    session_number=66,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Lidio Carraro Vinhos — Bento Gonçalves and Campanha Meridional',
    'location': 'Bento Gonçalves, Serra Gaúcha (winery) / Bagé, Campanha Meridional (estate vineyards), Rio Grande do Sul, Brazil',
    'description': (
        'Lidio Carraro is a Rio Grande do Sul winery founded by winemaker Lidio Carraro '
        'and family, with the winery base in Bento Gonçalves (Serra Gaúcha) and key estate '
        'vineyards in the Campanha Meridional region near Bagé, close to the Uruguayan '
        'border. The Quorum blend (Merlot, Cabernet Sauvignon, and Cabernet Franc) is '
        'the winery\'s flagship expression from Campanha Meridional terroir, representing '
        'one of the first internationally distributed wines to make the case for Campanha '
        'as Brazil\'s premium red wine region. Lidio Carraro\'s winemaking philosophy '
        'emphasizes site-specific expression over varietal fruit — a philosophy shaped '
        'by the contrast between Serra Gaúcha\'s humid, high-yield granite hills and '
        'the dry, flat basalt-alluvial Campanha Meridional pampa grassland where '
        'concentration through water stress is natural.'
    ),
    'founded': '1995',
    'region': 'Bento Gonçalves / Campanha Meridional, Rio Grande do Sul, Brazil',
    'website': 'lidiocarraro.com',
    'verified': True
})

session.add_producer({
    'tradition': 'wine',
    'name': 'Cave Geisse — Pinto Bandeira, Serra Gaúcha, Rio Grande do Sul',
    'location': 'Pinto Bandeira, Bento Gonçalves Municipality, Serra Gaúcha, Rio Grande do Sul, Brazil',
    'description': (
        'Cave Geisse was established by Chilean-born Mario Geisse (son of Manuel Geisse, '
        'who founded Viña Casa Silva in Chile) in the Pinto Bandeira sub-zone of '
        'Serra Gaúcha in the 1980s. Mario Geisse brought the méthode traditionnelle '
        'sparkling wine methodology from Champagne to Pinto Bandeira, establishing '
        'the Brazilian case for high-quality Charmat-and-traditional-method sparkling '
        'production from Chardonnay and Pinot Noir at 700–800m elevation in the '
        'granite-based Serra Gaúcha. Cave Geisse Brut Nature (zero dosage, '
        'Chardonnay-Pinot Noir, 36+ months on lees) is consistently rated among '
        'South America\'s finest sparkling wines and receives annual recognition '
        'at Champagne-competitive international sparkling wine competitions.'
    ),
    'founded': '1979',
    'region': 'Pinto Bandeira, Serra Gaúcha, Rio Grande do Sul, Brazil',
    'website': 'cavegeisse.com.br',
    'verified': True
})

session.add_purveyor({
    'name': 'Mistral Importadora (Brazil to North America) / Brazil Wine Co (US)',
    'type': 'importer',
    'description': (
        'Brazilian wine exports to North America are handled by specialty importers '
        'including the Brazil Wine Company (US) and Missão Importadores. '
        'Cave Geisse is available in select US and Canadian markets through '
        'specialty wine importers; Lidio Carraro Quorum is distributed through '
        'Brazilian wine specialists in New York, Florida, and California. '
        'BCLDB in British Columbia and LCBO in Ontario carry select Brazilian '
        'wine expressions on special order. The expanding Brazilian wine '
        'export programme is driven by APEX-Brasil (Brazilian Trade and '
        'Investment Promotion Agency) which organizes annual trade tastings '
        'in North America and Europe.'
    ),
    'markets_served': ['Brazil', 'US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['wine'],
    'website': 'brazilwineco.com',
    'verified': False
})

session.add_beverage({
    'name': (
        'Lidio Carraro Quorum — Campanha Meridional Red Blend, '
        'Merlot-Cabernet Franc, Pampa Grassland Terroir, Uruguayan Border Zone'
    ),
    'category': 'wine',
    'subcategory': 'wine_still',
    'origin': 'Brazil',
    'region': 'Brazil — Campanha Meridional (Lidio Carraro Quorum, Uruguayan Border, Pampa Grassland Wine)',
    'producer': 'Lidio Carraro Vinhos — Bento Gonçalves and Campanha Meridional',
    'alcohol_content': 14.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Campanha Meridional (Southern Campanha) is a wine region in the extreme '
        'south of Rio Grande do Sul, Brazil, bordering Uruguay at 30–32°S latitude '
        'on the flat Pampa grassland plateau at 100–300m elevation. The terroir '
        'is defined by contrast with Serra Gaúcha, Brazil\'s dominant wine region: '
        'where Serra Gaúcha is a humid, steep-slope granite and basalt mountain '
        'zone at 600–800m with 1,800mm annual rainfall and difficult mechanized '
        'access, Campanha Meridional is flat-to-gently-undulating alluvial-basalt '
        'plain at 100–300m elevation with 1,200–1,400mm annual rainfall, '
        'mechanical harvest feasibility, and a semi-continental climate influenced '
        'by the La Plata Basin atmospheric systems. The soils of the Campanha '
        'Meridional wine zone near Bagé and Santana do Livramento divide into '
        'two types: deep red latosol over basalt in the eastern sector, and '
        'sandy alluvial soils with quartz-rock inclusions in the western sector '
        'near the Uruguayan border crossing at Quaraí. The Cabernet Sauvignon, '
        'Merlot, and Cabernet Franc planted by Lidio Carraro and other Campanha '
        'pioneer producers (Almadén, Don Guerino) in the 1990s are now mature '
        '(20–30 year old vines) and demonstrate the concentration potential of '
        'Campanha Meridional water-stressed dry farming: the region\'s rainfall '
        'is 35–45% less than Serra Gaúcha, and the sandy-to-basalt soils drain '
        'rapidly, creating natural vine water stress during the January–February '
        'ripening period that concentrates phenolics and flavour compounds. '
        'The GI Campanha Gaúcha was formally recognized in 2020, establishing '
        'Campanha Meridional as Brazil\'s second formally GI-protected wine '
        'region after Serra Gaúcha Vale dos Vinhedos (DOCG 2012).'
    ),
    'production_technique': (
        'Lidio Carraro Quorum is assembled from Campanha Meridional estate '
        'vineyards near Bagé at 150–250m elevation, with Merlot and Cabernet '
        'Franc as the primary varieties in a blend proportion that varies by '
        'vintage. Harvest at Campanha takes place February–March when natural '
        'sugar accumulation reaches 23–25 Brix from the summer water stress; '
        'mechanized harvest is used for efficiency and overnight cool-temperature '
        'picking to preserve fruit integrity in the 30–35°C summer ambient. '
        'The harvested grapes are transported to the Serra Gaúcha winery '
        '(500km north) in temperature-controlled trucks — a logistics decision '
        'that reflects the current Campanha wine infrastructure gap (most '
        'major Campanha wineries process grapes in Serra Gaúcha). Whole-berry '
        'sorting on the sorting table, followed by destemming and crushing '
        'into stainless steel temperature-controlled tanks; alcoholic fermentation '
        'at 24–26°C for 14–18 days with daily pump-overs to extract colour and '
        'tannin from the water-stressed Campanha fruit that produces relatively '
        'concentrated skins. Malolactic conversion in barrel (225L French oak '
        'barriques, 40% new) for 100% of the blend over 6–8 months; '
        'total oak aging 12–14 months. The Quorum blend is assembled from '
        'barrel selection post-malolactic, targeting the expression of Campanha '
        'Meridional concentration (dark plum, blackberry, tobacco) balanced '
        'by Merlot\'s textural roundness. Final blend is fined and cold-stabilized '
        'before bottling under cork with 6–12 months additional bottle rest '
        'before commercial release.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Uruguay Tannat (Canelones and Cerro Chapeu, Pampa wine)',
            'connection': (
                'Campanha Meridional wine and Uruguayan wine share the same geological '
                'and climatic basis — the La Plata-Pampa grassland terroir that extends '
                'across the Brazil-Uruguay border without meaningful viticultural '
                'discontinuity: Lidio Carraro\'s Campanha estate is closer to '
                'Uruguayan Canelones vineyards than to Serra Gaúcha in both '
                'distance and climate. The primary varietal difference — Uruguay\'s '
                'commitment to Tannat as its national variety versus Campanha\'s '
                'Cabernet-Merlot focus — reflects historical planting choices '
                '(Basque immigrant Tannat introduction in Uruguay; Bordeaux-focused '
                'Italian and German immigrant planting in Brazil) rather than '
                'terroir differences, and both regions produce concentrated, '
                'full-bodied reds from the flat Pampa grassland that challenge '
                'the mountain-viticulture orthodoxy of South American fine wine.'
            )
        },
        {
            'tradition': 'Argentina Mendoza Malbec (Andes foothills, irrigation viticulture)',
            'connection': (
                'Both Campanha Meridional and Mendoza produce warm-climate full-bodied '
                'South American red wines that have positioned themselves as '
                'internationally competitive alternatives to European benchmarks, '
                'but they represent opposite viticultural strategies: Mendoza relies '
                'on Andean snowmelt irrigation in a desert climate at 600–1,100m '
                'elevation to achieve concentration through controlled water '
                'management; Campanha relies on natural rainfall-and-drought '
                'cycles in a semi-humid grassland climate at 100–300m elevation '
                'to achieve concentration through uncontrolled seasonal water '
                'stress. Both produce wines with high natural alcohol (14–15% ABV) '
                'and dark fruit concentration from warm-climate ripening, but '
                'the flavor register differs: Mendoza Malbec\'s violet-plum '
                'purity versus Campanha\'s tobacco-dark plum-leather character '
                'from the alluvial-basalt grassland soils.'
            )
        },
        {
            'tradition': 'Douro Valley table red (schist terroir, heat-concentrated fruit)',
            'connection': (
                'The Portuguese colonial connection to Campanha Meridional is literal: '
                'the first vines planted in the Rio Grande do Sul / Campanha zone '
                'were brought by Portuguese colonizers and Azorean immigrants in the '
                '18th–19th century, following the same PCT agricultural transfer '
                'pattern that moved Coffea arabica from Africa to Brazil. The '
                'current Campanha Bordeaux-variety focus is the commercial evolution '
                'of the Portuguese vine-planting tradition, and the concentration '
                'of Campanha red wines in the water-stressed Pampa grassland '
                'parallels the Douro Valley\'s heat-and-schist concentration '
                'of the Touriga Nacional, Tinta Roriz, and Tinta Barroca '
                'field blends that produce Douro table wine and Port.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep ruby-garnet, near-opaque core, the concentration typical of '
            'Campanha water-stressed Merlot-Cabernet Franc; excellent color '
            'saturation from 14–18 day maceration on mature vine fruit; '
            'clear and brilliant after fining; good viscous legs at 14% ABV; '
            'color comparable to Napa Valley Cabernet Sauvignon at similar '
            'extraction but with a slightly more garnet (less purple) hue '
            'consistent with the southern latitude (30°S) ripening character.'
        ),
        'nose': (
            'Dark plum and ripe blackberry from the warm Campanha harvest '
            'at 23–25 Brix; tobacco and dried herbs from the basalt-alluvial '
            'soil character of the Pampa grassland terroir; cedar and vanilla '
            'from French oak barriques; characteristic Merlot mocha-chocolate '
            'undertone; Cabernet Franc contributes subtle graphite and dried '
            'violet at the tertiary layer; full aromatic intensity from the '
            'water-stressed mature vine fruit; a distinctly South American '
            'warm-grassland character that is neither Andean (Mendoza\'s '
            'violet purity) nor Serra Gaúcha (Italian-immigrant lighter style).'
        ),
        'palate': (
            'Full body, round tannins from Merlot-dominant assemblage, warm '
            '14% ABV well-integrated with the Campanha fruit concentration; '
            'dark plum and tobacco through the mid-palate; the French oak '
            'cedar and vanilla supporting without dominating; malolactic '
            'conversion contributing the characteristic roundness of the '
            'Quorum palate that distinguishes it from the firmer Cabernet '
            'Sauvignon-dominant expressions from the region; long finish '
            'with dark fruit, tobacco, and a mineral graphite closing note '
            'from the basalt soil character; the wine demonstrates that '
            'Campanha Meridional water-stressed terroir produces genuinely '
            'structured reds, not merely warm-climate fruit bombs.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Brazilian Serra Gaúcha Standard (cooperative production)',
            'criteria': (
                'Humid Serra Gaúcha granite-slope Merlot or Isabel hybrid, '
                'cooperative-produced, commercial pricing — lighter body, '
                'lower concentration than Campanha, the high-volume Brazilian '
                'red wine baseline that shaped the market expectation before '
                'Campanha Meridional emerged as the quality tier.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Campanha Meridional Commercial (yield-managed)',
            'criteria': (
                'Campanha Meridional Cabernet Sauvignon or Merlot at commercial '
                'yield levels (10–12 tons/ha), mechanical harvest, shorter maceration '
                '(10–12 days) — more concentrated than Serra Gaúcha but without '
                'the extended maceration and barrel program of premium expressions.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Lidio Carraro Quorum (estate premium)',
            'criteria': (
                'Campanha Meridional mature vine estate fruit (20+ years), extended '
                'maceration 14–18 days, 12–14 months French oak — the benchmark '
                'Campanha red blend that established the region\'s international '
                'quality claim; the commercially available reference for southern '
                'Brazil wine at premium tier.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Don Guerino Reserve / Lidio Carraro Dádivas (apex Campanha)',
            'criteria': (
                'Single-vineyard or ultra-selection Campanha Meridional red wines '
                'from the oldest vines (25–35 years), extended barrel program '
                '(18–24 months new French oak), low yield selection — the collector '
                'tier for southern Brazil wine at international benchmark pricing; '
                'the proof-of-concept for Campanha Meridional as a world-class '
                'red wine region independent of Serra Gaúcha\'s sparkling wine '
                'heritage.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Lidio Carraro Quorum at 17–18°C for optimal dark fruit and tobacco '
            'aromatic expression — the Campanha Meridional tannin structure is '
            'robust enough to handle slightly warmer service than a lighter '
            'European red, but above 20°C the 14% ABV heat dominates; '
            'decant 30–45 minutes to soften the oak structure and allow '
            'the graphite-mineral character of the Pampa grassland terroir '
            'to develop. Young vintages (1–3 years) benefit from longer '
            'decanting (45–60 minutes) to integrate the barrel character; '
            'wines with 5+ years of bottle age may need only 20 minutes.'
        ),
        'vessel': (
            'Bordeaux-style Cabernet glass with vertical orientation to direct '
            'aromas to the nose while managing the full-bodied tannin structure; '
            '150ml pour for table service; a decanter for young vintages; '
            'in a South American wine flight, serve between Argentine Malbec '
            '(lighter, fruit-purer) and Chilean Carménère (more herbal) to '
            'position the Campanha tobacco-plum character within the South '
            'American red wine spectrum.'
        ),
        'programme_position': (
            'In a PCT Brazil programme: serve as the red wine component after '
            'the Cave Geisse Brut Nature sparkling opener — the transition '
            'from Serra Gaúcha sparkling (Italian immigrant methodology) to '
            'Campanha Meridional red (Portuguese-Pampa grassland terroir) '
            'demonstrates the full geographic range of Rio Grande do Sul '
            'wine within a single state.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Lidio Carraro Vinhos — Campanha Meridional estate (benchmark for '
            'Campanha Meridional red blend at premium tier; Quorum is the '
            'international reference expression for the region); Don Guerino '
            'Reserve as the Campanha single-vineyard apex alternative.'
        ),
        'north_america_access': (
            'Lidio Carraro available through specialty Brazilian wine importers '
            'in New York and Miami; BCLDB BC and LCBO Ontario on special order; '
            'approximately USD $30–50 for Quorum in US specialty retail. '
            'Brazil Wine Company and APEX-Brasil promotional events in North '
            'America provide the primary channel for trade buyers to access '
            'Campanha Meridional samples.'
        ),
        'culinary_application': (
            'Campanha Meridional Quorum\'s tobacco-plum-leather character pairs '
            'with Brazilian churrasco (grilled beef), specifically the picanha '
            '(top sirloin cap, the national cut) and fraldinha (flank steak) '
            'preparations from Rio Grande do Sul gaucho tradition — the wine '
            'was produced in the same Pampa grassland as the cattle, making '
            'this the most direct land-to-table pairing in South American wine.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region(
    'wine',
    'Brazil — Serra Gaúcha (Cave Geisse Brut Nature, Chardonnay-Pinot Noir Sparkling, Italian Immigrant Method Traditionnelle)'
)

session.add_beverage({
    'name': (
        'Cave Geisse Brut Nature — Serra Gaúcha Pinto Bandeira, '
        'Chardonnay-Pinot Noir Méthode Traditionnelle, Italian Immigrant Sparkling Heritage'
    ),
    'category': 'wine',
    'subcategory': 'wine_sparkling',
    'origin': 'Brazil',
    'region': 'Brazil — Serra Gaúcha (Cave Geisse Brut Nature, Chardonnay-Pinot Noir Sparkling, Italian Immigrant Method Traditionnelle)',
    'producer': 'Cave Geisse — Pinto Bandeira, Serra Gaúcha, Rio Grande do Sul',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Pinto Bandeira is a sub-zone of the Serra Gaúcha wine region in Rio Grande '
        'do Sul, situated at 700–800m in the Serra Gaúcha mountains approximately '
        '20km northwest of Bento Gonçalves — the center of Italian immigrant '
        'settlement in southern Brazil. The Serra Gaúcha was settled primarily by '
        'northern Italian immigrants (Veneto, Trentino, Lombardy) from 1875–1914, '
        'who brought Vitis vinifera vine cuttings (primarily Isabel/Isabella hybrid '
        'initially, later Chardonnay, Pinot Noir, and Trebbiano) and the cultural '
        'tradition of sparkling wine production from their native Prosecco, '
        'Franciacorta, and Trento DOC backgrounds. Pinto Bandeira was raised '
        'to a separate sub-appellação (sub-appellation) within the Indicação '
        'Geográfica Vale dos Vinhedos in 2010, recognizing its distinct '
        'topographic and climatic conditions versus the main valley floor: '
        'Pinto Bandeira sites receive more direct Atlantic Maritime air influence '
        'from the easterly trade winds than the main Serra Gaúcha valley, '
        'moderating summer temperatures and extending the growing season '
        'by 2–3 weeks compared to the valley floor. This extended growing '
        'season is the critical factor for Chardonnay and Pinot Noir quality: '
        'the 700–800m elevation combined with Atlantic air influence creates '
        'a temperature range of 12–25°C during October–January ripening '
        'that preserves natural acidity (7.5–9.5 g/L total acidity as '
        'tartaric) at the high-Brix levels (19–21°) required for sparkling '
        'wine base quality. The Serra Gaúcha granite and basalt subsoils '
        'at Pinto Bandeira contribute the mineral complexity that distinguishes '
        'Cave Geisse from Charmat-method (Prosecco-style) Brazilian sparkling.'
    ),
    'production_technique': (
        'Cave Geisse Brut Nature is produced by the méthode traditionnelle '
        '(second fermentation in bottle) from a base wine of Chardonnay and '
        'Pinot Noir harvested from Pinto Bandeira vineyards at 19–21 Brix '
        'with 7.5–9.5 g/L total acidity. The base wine undergoes alcoholic '
        'fermentation in stainless steel at 16–18°C and partial malolactic '
        'conversion (40–60% for Brut Nature to preserve acidity freshness). '
        'The base wine is assembled (assemblage) from Chardonnay and Pinot '
        'Noir in proportions that vary by vintage but typically target '
        '60–65% Chardonnay for structure and 35–40% Pinot Noir for body '
        'and red fruit character. Tirage (bottling with yeast and sugar for '
        'second fermentation) takes place in heavy sparkling wine bottles '
        'sealed with crown caps. The second fermentation in bottle takes '
        'place at 12–14°C over 6–8 weeks, producing the carbon dioxide '
        'dissolved in the wine and the dead yeast cells that will form '
        'the lees during aging. Cave Geisse Brut Nature is aged on lees '
        'for a minimum of 36 months — considerably longer than the '
        'Champagne NV minimum of 15 months — allowing extended autolysis '
        '(yeast cell self-digestion) to develop the characteristic bread '
        'dough, brioche, and toasted almond character of extended-lees '
        'sparkling wine. The Brut Nature (zero dosage) receives no '
        'liqueur d\'expédition (sugar addition) at disgorgement — the '
        'residual sweetness is entirely from the natural grape sugar '
        'retained through fermentation and the 36+ month autolysis process, '
        'typically reaching 4–6 g/L residual sugar naturally from the '
        'incomplete third fermentation. The pressure in the finished '
        'Brut Nature is 5.5–6.0 atm, comparable to Champagne NV. '
        'Production: approximately 80,000–120,000 bottles annually '
        'for the Brut Nature, with very limited Blanc de Blancs and '
        'Rosé Brut Nature expressions produced from the best vintage lots.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Champagne NV Blanc de Blancs (Côte des Blancs, Chardonnay, méthode champenoise)',
            'connection': (
                'Cave Geisse Brut Nature and Champagne Blanc de Blancs NV share '
                'the méthode traditionnelle production architecture: second '
                'fermentation in bottle, extended lees aging, disgorgement, '
                'and zero dosage philosophy at the Brut Nature tier. The '
                'critical difference is terroir: Champagne\'s chalk soils '
                '(Belemnite chalk, Cretaceous formation) provide the unique '
                'mineral substrate that imparts the specific Champagne character; '
                'Cave Geisse\'s granite and basalt at Pinto Bandeira provide '
                'a different mineral foundation that produces a wine of comparable '
                'structural complexity and autolytic depth but with a distinctly '
                'Brazilian tropical character beneath the brioche and mineral '
                'sparkling wine architecture — demonstrating that méthode '
                'traditionnelle mastery is fully achievable outside Champagne '
                'when the elevation and climate conditions support it.'
            )
        },
        {
            'tradition': 'Trento DOC (Northern Italy, méthode classique, granite terroir)',
            'connection': (
                'Cave Geisse and Trento DOC are the most direct parallel in the '
                'global sparkling wine landscape: both produce méthode traditionnelle '
                'Chardonnay-Pinot Noir sparkling wines from granite-based mountain '
                'terroir at 700–900m elevation with Atlantic/Alpine air influence '
                'that extends the growing season and preserves natural acidity. '
                'The parallel is not coincidental — Serra Gaúcha was settled by '
                'Trentino-Alto Adige Italian immigrants who brought their sparkling '
                'wine methodology from the same Trento Alpine zone that produces '
                'Ferrari and Rotari Trento DOC today. Cave Geisse\'s founder '
                'Mario Geisse explicitly acknowledges the Trento DOC reference '
                'model as the structural template for his Pinto Bandeira production.'
            )
        },
        {
            'tradition': 'Portugal — Espumante Brut from Vinho Verde (Atlantic influence, high-acidity sparkling)',
            'connection': (
                'Both Cave Geisse Brut Nature and high-quality Vinho Verde Espumante '
                '(Alvarinho-based méthode traditionnelle from producers like Soalheiro '
                'and Quinta de Soalheiro) use extended lees aging to build autolytic '
                'complexity in high-acid sparkling base wines from granite-terroir '
                'Atlantic-influenced growing regions. The Portuguese colonial '
                'connection to Brazilian sparkling wine is through the Italian '
                'immigrant channel: Portuguese colonial agricultural transfer '
                'brought European vine culture to Brazil, which the subsequent '
                'Italian immigrant wave (1875–1914) transformed into the Serra '
                'Gaúcha wine tradition that Cave Geisse now leads in sparkling quality.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale gold with green tints from high natural acidity of Pinto Bandeira '
            'Chardonnay-Pinot Noir base; fine, persistent bead from the 36+ month '
            'lees aging that produces fine CO2 bubbles rather than the coarse bead '
            'of short-lees production; brilliant clarity after disgorgement and '
            'post-disgorgement bottle rest; foam that rises fine, white, and persistent '
            'in the flute; color slightly deeper than Champagne NV Blanc de Blancs '
            'from the Pinot Noir component and the tropical light intensity at '
            '700–800m Serra Gaúcha latitude (29°S, more solar intensity than Champagne).'
        ),
        'nose': (
            'The 36+ month autolysis defines the aromatic identity: fresh brioche, '
            'toasted bread crust, and dried yeast character from extended lees contact; '
            'beneath the autolytic character, the Chardonnay contributes citrus '
            '(lemon zest, green apple) and the Pinot Noir adds a light red fruit '
            'undertone (strawberry, raspberry) from the Pinto Bandeira granite '
            'character; stone fruit (apricot, white peach) from the tropical '
            'latitude ripening; zero dosage ensures no caramel or honey sweetness '
            'obscures the mineral and autolytic complexity.'
        ),
        'palate': (
            'Fine persistent mousse from the 36-month in-bottle secondary fermentation; '
            'high natural acidity (7.5–9.5 g/L) creates the backbone for the '
            'zero-dosage balance — the wine achieves apparent dryness from the '
            'acid structure without any residual sugar manipulation; medium body '
            'from the Pinot Noir component; brioche and mineral from the '
            'autolysis and granite terroir through the mid-palate; long '
            'mineral-and-citrus finish demonstrating that 36 months of extended '
            'lees aging at Pinto Bandeira elevation produces autolytic complexity '
            'competitive with Champagne at equivalent aging duration; '
            'clean, precise, with no tropical fruit heaviness overwhelming '
            'the sparkling wine structure.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Brazilian Charmat (Prosecco-method sparkling)',
            'criteria': (
                'Charmat secondary fermentation in pressurized tanks, 30–90 day '
                'lees contact — the majority of Brazilian espumante production; '
                'fresh, fruit-forward, no autolytic complexity; the high-volume '
                'Brazilian sparkling wine category from Isabel hybrid and Moscatel '
                'varieties rather than Chardonnay-Pinot Noir.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Serra Gaúcha Méthode Traditionnelle (12–18 months lees)',
            'criteria': (
                'Bottle fermentation with 12–18 months lees aging — early autolytic '
                'development but without the complexity of 24–36 month extended '
                'lees; achieves Cava-comparable quality at Serra Gaúcha competitive '
                'pricing; the competent but not distinguished tier of Brazilian '
                'méthode traditionnelle.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Cave Geisse Brut Nature (36+ months lees)',
            'criteria': (
                'The benchmark: Pinto Bandeira Chardonnay-Pinot Noir, 36+ months '
                'lees, zero dosage — the South American sparkling wine that most '
                'directly challenges Champagne structural standards within the '
                'méthode traditionnelle category; Decanter Gold and Champagne-'
                'competitive international recognition.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Cave Geisse Millésime / Ultra Brut (vintage apex)',
            'criteria': (
                'Vintage-dated single-harvest expressions from the best Pinto '
                'Bandeira years (cooler, slower ripening) with 48–60 months '
                'extended lees aging and ultra-brut (below 3 g/L residual sugar) '
                'zero-dosage philosophy; the apex demonstration of Serra Gaúcha\'s '
                'capacity for extended-lees sparkling wine aging and the reference '
                'for South American sparkling wine quality at its highest expression.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Cave Geisse Brut Nature at 7–9°C for service — slightly warmer than '
            'the standard Champagne service temperature of 6–8°C because the '
            'Serra Gaúcha base wine\'s tropical character and the autolytic '
            'complexity both express better with marginal additional warmth '
            'that opens the brioche-and-stone-fruit aromatic register. '
            'Ice bucket service from a standard 10°C refrigerator temperature '
            'to 7–9°C takes approximately 20–25 minutes. The Brut Nature\'s '
            'high natural acidity means it tolerates up to 11°C service without '
            'losing structural balance — a wider service window than zero-dosage '
            'Champagne, which tightens rapidly above 10°C.'
        ),
        'vessel': (
            'Standard Champagne tulip or white wine tulip (not the flat '
            'coupe) to concentrate the fine bead and the autolytic brioche-'
            'mineral aromatics; avoid the champagne flute — the narrow '
            'flute inhibits aromatic development and is inappropriate for '
            'a Brut Nature of 36-month complexity; 100ml pour to allow '
            'the mousse to settle and the aromas to develop in the first '
            '30 seconds after pouring. At a Cave Geisse programme tasting, '
            'compare the aroma and bead character between the 36-month '
            'Brut Nature and a 15-month commercial espumante to demonstrate '
            'how extended lees aging transforms sparkling wine character.'
        ),
        'programme_position': (
            'In a PCT Brazil programme: serve as the opening wine — Cave Geisse '
            'Brut Nature\'s Italian immigrant heritage, méthode traditionnelle '
            'mastery, and Serra Gaúcha granite terroir establish the Brazilian '
            'wine narrative at a quality level that immediately signals the '
            'programme\'s ambition before the Campanha Meridional red wine '
            'and cachaça expressions follow.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Cave Geisse — Pinto Bandeira, Serra Gaúcha, Rio Grande do Sul '
            '(benchmark for South American méthode traditionnelle sparkling; '
            'Brut Nature 36+ months is the reference expression; founder '
            'Mario Geisse is the leading practitioner of extended-lees '
            'Brazilian sparkling wine methodology).'
        ),
        'north_america_access': (
            'Cave Geisse available through specialty Brazilian wine importers '
            'in New York, Florida, and California; BCLDB BC and LCBO Ontario '
            'on special order; approximately USD $25–40 for Brut Nature '
            'in US specialty retail. Growing international recognition at '
            'Champagne-comparison tastings is improving North American '
            'distribution annually.'
        ),
        'culinary_application': (
            'Cave Geisse Brut Nature\'s high acidity and brioche character '
            'pairs with fresh-water fish preparations from Rio Grande do Sul '
            '(pintado, dourado from the Paraná River basin) and with Nyonya-'
            'influenced seafood at Malacca-themed programmes — the sparkling '
            'wine\'s mineral acidity bridges both the European-method heritage '
            'and the Brazilian coastal seafood tradition simultaneously.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
