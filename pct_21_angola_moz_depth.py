import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='Angola — Uige and Malanje Provinces (Robusta Revival, Colonial-Era Arabica Estates)',
    output_dir='.',
    starting_entry=1,
    session_number=22,
    running_total=76
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Fazenda Capanda — Malanje Province',
    'location': 'Malanje Province, central Angola',
    'description': 'Post-civil-war estate revival producing Angolan Arabica on colonial-era plantation infrastructure. The Capanda irrigation scheme (anchored by the Capanda hydroelectric dam on the Cuanza River) enabled revival of estates that had been producing world-class coffee — particularly Angolan Arabica (Coffea arabica var. laurina and var. typica) — before the 1975–2002 civil war destroyed most export infrastructure. Angola was once the world\'s fourth-largest coffee producer. These farms focus on heritage varieties maintained at altitude 900–1,200m with colonial-era shade-grown systems under native canopy trees.',
    'founded': '1950s original; revived post-2002',
    'region': 'Malanje Province, Angola',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'coffee',
    'name': 'COCACUL — Cooperativa de Cafeicultores do Uige',
    'location': 'Uige Province, northern Angola',
    'description': 'Farmer cooperative in Uige Province — Angola\'s primary Robusta-producing region — working with smallholder producers across the Uige plateau (900–1,400m elevation). Established with international development assistance post-civil-war to revive Angola\'s once-dominant Robusta export industry. The Uige plateau Robusta (Coffea canephora var. robusta) is processed using traditional wet washing methods carried forward from Portuguese colonial wet-milling infrastructure that survived in fragmentary form. COCACUL works with the Angolan Coffee Institute (INCA) on quality grading and is establishing specialty-tier Robusta certification for export to European roasters.',
    'founded': '2008',
    'region': 'Uige Province, Angola',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Sucafina SA — African Origins Portfolio',
    'type': 'trader',
    'description': 'Geneva-headquartered green coffee trading company with dedicated African origins desk including Angola. Sucafina\'s Angola program sources through COCACUL and estate partners in Malanje, providing traceable lot separation and export logistics across Luanda port. Primary supply channel for specialty roasters in EU and North America accessing Angolan coffee in the current revival period.',
    'markets_served': ['EU', 'US', 'Canada', 'UK'],
    'traditions_carried': ['coffee'],
    'website': 'sucafina.com',
    'verified': False
})

session.add_beverage({
    'name': 'Angola Uige Plateau Robusta — COCACUL Washed, Post-War Revival Specialty Tier',
    'category': 'coffee',
    'subcategory': 'robusta_specialty',
    'origin': 'Angola',
    'region': 'Uige Province, Angola',
    'producer': 'COCACUL — Cooperativa de Cafeicultores do Uige',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Uige plateau in northern Angola sits at 900–1,400m elevation within the Congo Basin transition zone — the ecological border between equatorial rainforest and savanna woodland. Annual rainfall averages 1,400–1,800mm, arriving in a bimodal pattern (March–May, October–December) that separates cherry ripening into two annual harvests. The soils are red-brown lateritic clay over weathered basement rock, with naturally occurring manganese deposits that contribute to a distinctive mineral quality documented in pre-war Angolan export-grade Robusta. The Coffea canephora var. robusta trees on the Uige plateau are predominantly naturalized forest-edge populations — semi-wild in character — growing under partial canopy of native Milicia excelsa (iroko) and Pericopsis elata (afromosia) timber trees. This semi-wild character creates genotypic diversity absent in monoculture plantation Robusta: individual trees show divergent cup profiles ranging from standard chocolate-earthy to berry-inflected outliers that cup above 80 points — the threshold of specialty classification that most Robusta globally cannot achieve. Angola was the world\'s fourth-largest coffee exporter by 1973, predominantly Robusta. Civil war (1975–2002) destroyed 90% of production infrastructure; the current revival represents both agricultural and cultural reconstruction.'
    ),
    'production_technique': (
        'COCACUL members harvest ripe red cherries by selective hand-picking on staggered schedules across the extended Uige plateau ripening window (October–January primary, April–June secondary). Cherries are delivered to wet-processing stations — partial reconstructions of Portuguese colonial wet-mill infrastructure — within 6 hours of harvest. Processing follows the washed (fully washed) method: cherries are de-pulped on Colombian-style drum pulpers within 12 hours, then fermented in cement tanks for 24–36 hours. The tank fermentation duration varies by ambient temperature; higher elevation farms (above 1,200m) extend fermentation to 36+ hours for fuller mucilage breakdown. After fermentation, parchment coffee is washed in consecutive clean water channels and then sun-dried on raised African raised beds for 15–21 days, turned every 2 hours during peak sun hours (10am–3pm). The resulting green beans are hulled and graded by hand, with INCA-certified quality inspectors providing export-grade sorting. Specialty-tier Robusta lots scoring 80+ points are separated for export to EU and North American specialty roasters; below-80 lots remain in domestic or commodity export channels. The cup profile of the specialty tier shows an unusually clean Robusta character — less of the harsh rubbery notes typical of commodity Robusta, with prominent cocoa mass, forest floor, and dried black fruit character that reflects the semi-wild terroir.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Vietnam Da Lat Arabica',
            'connection': 'Both Angola and Da Lat Vietnam represent post-war coffee revival projects where commodity infrastructure (Robusta in both cases) is being upgraded through specialty processing methods and genotypic diversity research — and both highlight how war disruption can paradoxically preserve traditional growing systems that intensive modernization would have erased'
        },
        {
            'tradition': 'Ethiopian Jimma Robusta (wild collected)',
            'connection': 'Angola Uige plateau\'s semi-wild Coffea canephora parallels the Ethiopian wild Robusta populations in Jimma and Kaffa zones — both representing the species in naturalized, genotypically diverse forest-edge contexts that produce specialty-capable cup profiles distinct from cultivated plantation Robusta'
        },
        {
            'tradition': 'Port wine revival (Douro replanting post-phylloxera)',
            'connection': 'Angola\'s post-civil-war coffee revival mirrors Portugal\'s own post-phylloxera Douro replanting of the 1880s–1910s: both involve rebuilding a destroyed agricultural export system from heritage rootstock on land that retained terroir character despite production collapse — agricultural memory encoded in soil and wild genetics rather than in institutions'
        }
    ],
    'sensory_profile': {
        'appearance': 'Dark brown to black brew with mahogany rim; full-bodied crema in espresso applications; medium-heavy viscosity in filter preparation',
        'nose': 'Dark cocoa mass, forest floor, dried black cherry, roasted peanut, faint tobacco leaf — more structured than commodity Robusta with less of the harsh rubber-petroleum character typical of the species',
        'palate': 'Full body, low-moderate acidity, bitter-cocoa core, dried black fruit mid-palate, clean finish without harshness — the hallmark of the specialty tier that separates Uige plateau Robusta from commodity Vietnamese or Indian Robusta'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commodity Robusta Export',
            'criteria': 'Below-80 point lots, strip-picked or machine-harvested, natural or semi-washed processing, destined for espresso blends or instant coffee — represents 80%+ of current Angola production'
        },
        {
            'tier': 2,
            'tier_name': 'INCA Certified Grade A',
            'criteria': 'Angolan government quality certification for export-grade Robusta meeting minimum moisture, defect count, and screen size standards — improved commercial quality but not specialty tier'
        },
        {
            'tier': 3,
            'tier_name': 'COCACUL Specialty Tier (80–83 points)',
            'criteria': 'Selective hand-picking, 24–36 hour tank fermentation, raised-bed drying, cupper-verified — the current ceiling of Angola\'s revival production, available through Sucafina African desk'
        },
        {
            'tier': 4,
            'tier_name': 'Single-Garden Reserve',
            'criteria': 'Individual smallholder lots from identified semi-wild tree populations, micro-processed separately, 85+ point target — aspirational tier currently being developed by COCACUL with SCA (Specialty Coffee Association) technical assistance as of 2024–2025'
        }
    ],
    'service_intelligence': {
        'temperature': 'Espresso: 93–94°C extraction; Filter: 95–96°C pour-over or 92°C immersion (AeroPress); Serve at 65–70°C — the full-bodied Robusta character is best expressed at higher drinking temperature than delicate Arabica',
        'vessel': 'Espresso: standard demitasse (60–90ml) or lungo glass to observe crema thickness; Filter: ceramic cup or Chemex — the body benefits from a vessel that retains heat; the bitter-cocoa character is best in unglazed ceramic that does not add metallic interference',
        'barista_notes': 'Uige specialty Robusta responds well to shorter roast profiles than conventional Robusta wisdom suggests — medium-dark is optimal; avoid dark roast that destroys the fruit-forward outlier character; works exceptionally in flat white or cortado where the cocoa depth integrates with milk fat'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'COCACUL Cooperativa de Cafeicultores do Uige — INCA certified specialty lots via Sucafina African Origins',
        'north_america_access': 'Limited — Sucafina exports green lots to specialty importers; Onyx Coffee Lab (Rogers AR) and Passenger Coffee (Lancaster PA) have trialed Angola revival lots; DreamCoffee (Vancouver BC) has expressed sourcing interest as of 2024',
        'culinary_application': 'High-caffeine Robusta character makes concentrated Angola extract ideal for cocktail applications: espresso martini with Angolan Robusta produces a more bitter-forward, structured cocktail than Arabica; cold brew concentrate works in savory applications — meat glazes, mushroom sauces — where the cocoa depth pairs with umami'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('spirits', 'Mozambique — Maputo and Zambezia (Matope, Chibuku, Colonial-Era Sugar Cane Spirits)')

session.add_producer({
    'tradition': 'spirits',
    'name': 'Companhia Industrial da Matola (CIM) — Fábrica de Aguardente',
    'location': 'Matola, Maputo Province, Mozambique',
    'description': 'Historical Mozambican industrial distillery established during Portuguese colonial period to process sugar cane from the Zambezia and Maputo sugar estates. The Matola industrial complex was one of Portuguese East Africa\'s key processing centers, producing aguardente (cane spirit) for domestic consumption and export to Portugal. Post-independence (1975) and through the civil war (1977–1992), production continued under FRELIMO government ownership before partial privatization in the 1990s. The distillery maintains one of the few functioning column stills in Mozambique, producing a raw cane spirit that is both the basis for artisanal blending and the direct descendant of Portuguese colonial aguardente production.',
    'founded': '1940s (colonial); current form post-1992',
    'region': 'Matola, Maputo Province, Mozambique',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Mozambique Aguardente de Cana — Maputo Province Colonial-Legacy Sugar Cane Spirit',
    'category': 'spirits',
    'subcategory': 'cane_spirit',
    'origin': 'Mozambique',
    'region': 'Maputo Province, Mozambique',
    'producer': 'Companhia Industrial da Matola (CIM) — Fábrica de Aguardente',
    'alcohol_content': 40.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'Mozambique\'s cane spirit tradition is rooted in the colonial-era sugar estates of Zambezia Province (Luabo and Marromeu) and the Maputo Province lowlands — both areas of intensive Portuguese agricultural development from the 1890s onward. Sugar cane (Saccharum officinarum) was introduced to Mozambique by Portuguese colonizers who brought Madeira and São Tomé estate management techniques to East Africa, creating plantations along the Zambezi River delta and the Limpopo lowlands. The Maputo-Matola industrial corridor developed as the processing hub: cane was cut by hand-labor on the coastal plains (sea-level to 100m elevation), transported to Matola by narrow-gauge rail, and processed in colonial-era mills whose copper pot still aguardente infrastructure was established by Portuguese technicians trained in Madeira aguardente production. The resulting spirit carries a directness that reflects the flat lowland cane character — no altitude cooling that slows tropical sugar concentration, no volcanic mineral complexity, but a raw tropical-sweet cane identity that is distinctly Mozambican in its heat and directness. The production territory sits within the Portuguese colonial trade arc connecting Lisbon → Madeira → Cape Verde → São Tomé → Mozambique → Goa → Macau, completing the aguardente technical transfer that seeded cane spirit production across the Lusophone world.'
    ),
    'production_technique': (
        'The Matola distillery processes cane juice from contracted sugar estates in Maputo Province, using direct juice extraction rather than molasses-based fermentation — a colonial-era technical choice that maintains the fresh cane character preferred in the Mozambican domestic market over the darker, more structured molasses rums of the Caribbean. Extracted cane juice is clarified by brief settling, then inoculated with a domesticated Saccharomyces cerevisiae culture maintained at the distillery since its colonial-era founding. Fermentation proceeds in open concrete or steel vats for 24–36 hours at ambient tropical temperature (28–35°C) — a rapid fermentation cycle that produces a high-congener wine at 8–12% ABV. Distillation occurs in a single-pass column still at 85–90% ABV, followed by dilution to 40% with filtered water. No oak aging, no filtering beyond basic centrifugation. The resulting aguardente is bottled immediately for domestic market distribution, or held in large steel tanks for informal redistribution as bulk spirit to artisanal blenders and market vendors. In rural Mozambique, artisanal versions (locally called matope or ntombo depending on region) are produced by informal distillers using simple pot still configurations made from repurposed oil drums and copper tubing — a direct technical descendant of the colonial alembic introduced by Portuguese settlers in the 16th–17th century.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Brazilian cachaça (industrial grade)',
            'connection': 'Mozambique aguardente de cana and industrial Brazilian cachaça share direct juice fermentation over molasses, rapid high-temperature tropical fermentation, column still distillation to high ABV, immediate bottling without oak aging — both representing the industrial expression of a technical tradition rooted in the same Portuguese colonial sugar estate architecture'
        },
        {
            'tradition': 'Cape Verde grogue',
            'connection': 'Both Mozambique aguardente and Cape Verde grogue are direct technical descendants of Portuguese colonial cane spirit production, but grogue retained pot still distillation and artisanal production context while Mozambique industrialized — the contrast illustrates how colonial-era technical choices diverge post-independence based on local economic conditions'
        },
        {
            'tradition': 'Timor-Leste palm spirits (tuak arak)',
            'connection': 'Both Mozambique and Timor-Leste inherited Portuguese colonial distillation knowledge but applied it to locally available agricultural substrates — sugar cane in Mozambique, palm sap and rice wine in Timor-Leste — demonstrating how the same technical tradition adapts to different tropical agricultural contexts across the Lusophone world'
        }
    ],
    'sensory_profile': {
        'appearance': 'Clear, water-white; no color from aging; slight oiliness visible when swirled; bottled at 40% without dilution variations',
        'nose': 'Raw tropical cane sweetness, cooked sugar, light acetone from high-congener column still production, faint green cane herbaceousness, alcohol warmth predominant — direct and simple rather than complex',
        'palate': 'Immediate alcohol heat on entry, sweet tropical cane mid-palate, thin body from column still dilution, short finish — the domestic Mozambican preference for immediate heat and sweetness over complexity; artisanal matope versions show more congener richness and longer finish from pot still concentration'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Informal Matope (Artisanal)',
            'criteria': 'Illegal or semi-legal village-scale pot still production from fermented cane juice or sugar water; variable ABV 30–70%; consumed directly in rural areas; the base layer of Mozambican cane spirit culture with highest risk of methanol contamination from improper still operation'
        },
        {
            'tier': 2,
            'tier_name': 'CIM Industrial Aguardente',
            'criteria': 'Regulated column still production, tested ABV at 40%, domestic bottling — the standard commercial product widely available in Maputo and provincial centers'
        },
        {
            'tier': 3,
            'tier_name': 'Artisanal Registered Distillers',
            'criteria': 'Small licensed distillers using copper pot stills, fresh cane juice, longer fermentation — emerging as a quality tier with support from Mozambican spirits associations and some EU development aid programs'
        },
        {
            'tier': 4,
            'tier_name': 'Export-Grade Aged Cane Spirit',
            'criteria': 'The aspirational tier: oak-aged Mozambique cane spirit has not yet achieved consistent production — isolated producers experiment with ex-bourbon barrels — representing the frontier of the tradition\'s development toward international specialty spirits markets'
        }
    ],
    'service_intelligence': {
        'temperature': 'Served at ambient tropical room temperature (28–32°C) in traditional context — Mozambican drinking culture does not typically chill spirits; for international service, 18–20°C with one large ice block to dilute without over-chilling',
        'vessel': 'Traditional: small shot glass or repurposed glass; Modern: rocks glass with one ice block; Cocktail context: works as a high-proof base spirit in tropical preparations where the raw cane character acts as the aggressive backbone',
        'cocktail_notes': 'In Maputo bar culture, aguardente de cana is mixed with citrus (local lime or passion fruit juice) and sugar syrup in a preparation analogous to the Brazilian caipirinha — a direct parallel that reflects the shared Portuguese colonial cane spirit architecture across the Lusophone Atlantic'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Companhia Industrial da Matola (CIM) for the industrial-regulated baseline; artisanal Beira district producers for the pot still craft tier',
        'north_america_access': 'Not commercially exported to North America; accessible through Mozambican diaspora communities; specialty spirits importers with Lusophone focus (e.g., Liquid Amber, which carries Cape Verde grogue) have expressed interest in Mozambique products as of 2024–2025',
        'culinary_application': 'PNW culinary application: raw cane character works as a caipirinha-style cocktail base with Okanagan peaches; high congener content makes it useful as a flambé spirit in tableside preparations; the Lusophone cane spirit narrative pairs naturally with menus exploring Portuguese colonial food history'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
