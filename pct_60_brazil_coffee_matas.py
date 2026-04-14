import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='Brazil — Matas de Minas (Alta Mogiana Sub-Region, Catuaí Yellow, Red Fruits Honey Process, Atlantic Forest Coffee)',
    output_dir='.',
    starting_entry=1,
    session_number=64,
    running_total=0
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Fazenda Santuário Sul — Carmo de Minas, Matas de Minas, Minas Gerais',
    'location': 'Carmo de Minas, Sul de Minas / Matas de Minas transition zone, Minas Gerais, Brazil',
    'description': (
        'Fazenda Santuário Sul is operated by the Pereira family in Carmo de Minas — a '
        'municipality in the Sul de Minas / Matas de Minas overlap zone of southern Minas '
        'Gerais that is consistently ranked among Brazil\'s highest-scoring coffee production '
        'areas at international competitions including Cup of Excellence. The Carmo de Minas '
        'cluster of farms produces coffee at 950–1,200m elevation in the Serra da Mantiqueira '
        'foothills, where the Atlantic Forest biome\'s temperature regulation and the deep '
        'red latosol soils create the conditions for natural and honey processed coffees '
        'with exceptional cup scores. Fazenda Santuário Sul produces Yellow Catuaí and '
        'Bourbon Amarelo varieties through both natural and honey processing, with multiple '
        'Brazil Cup of Excellence placements. The farm\'s honey-process Catuaí regularly '
        'achieves 87–90+ SCA scores, placing it at the specialty apex of Brazilian coffee '
        'production.'
    ),
    'founded': 'ca. 1980s (current family operation)',
    'region': 'Carmo de Minas, Minas Gerais, Brazil',
    'website': 'fazendas-santuario.com.br',
    'verified': False
})

session.add_purveyor({
    'name': 'Intelligentsia Coffee / Counter Culture Coffee (US importers, Brazil specialty)',
    'type': 'importer',
    'description': (
        'Matas de Minas and Sul de Minas specialty lots are imported to North America '
        'through specialty roasters with direct trade relationships in Brazil: '
        'Intelligentsia Coffee (Chicago, LA), Counter Culture Coffee (Durham NC), '
        'and Onyx Coffee Lab (Rogers AR) maintain direct relationships with Carmo '
        'de Minas farms and import high-scoring honey and natural lots annually. '
        'Canadian importers include Detour Coffee (Hamilton ON) and 49th Parallel '
        '(Vancouver BC), both of which source Brazilian Sul de Minas and Matas de '
        'Minas specialty coffee for single-origin filter and espresso programmes.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['coffee'],
    'website': 'intelligentsiacoffee.com',
    'verified': False
})

session.add_beverage({
    'name': (
        'Matas de Minas Honey Process Catuaí Amarelo — Atlantic Forest Biome, '
        'Serra da Mantiqueira Foothills, 900–1100m, Red Fruit and Chocolate SCA Specialty'
    ),
    'category': 'coffee',
    'subcategory': 'honey_process',
    'origin': 'Brazil',
    'region': 'Brazil — Matas de Minas (Alta Mogiana Sub-Region, Catuaí Yellow, Red Fruits Honey Process, Atlantic Forest Coffee)',
    'producer': 'Fazenda Santuário Sul — Carmo de Minas, Matas de Minas, Minas Gerais',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Matas de Minas (literally "Forests of Minas") is a coffee region designation '
        'in eastern Minas Gerais, Brazil, covering the Atlantic Forest biome transitional '
        'zone between the coffee highlands of Sul de Minas (Serra da Mantiqueira) and the '
        'coastal forests of Espírito Santo. The region occupies the Serra do Caparaó '
        'watershed at 800–1,200m elevation across municipalities including Carangola, '
        'Manhuaçu, Lajinha, and the higher-elevation Carmo de Minas cluster that '
        'sits at the border of Matas de Minas and Sul de Minas designations. The '
        'Alta Mogiana sub-region reference in the entry\'s regional identity acknowledges '
        'that the Carmo de Minas cluster shares altitude (900–1,200m) and quality '
        'characteristics with the Alta Mogiana zone of São Paulo State, the '
        'highest coffee zone in the São Paulo coffee belt. The soil type '
        'across Matas de Minas is deep red latosol (terra roxa equivalent) — '
        'well-drained, iron and aluminum oxide-rich, deeply weathered Precambrian '
        'gneiss and schist basement — that drains rainfall rapidly and forces '
        'Coffea arabica roots deep for water and mineral access. The Atlantic Forest '
        'biome creates a specific microclimate effect: Atlantic Forest remnants at '
        '20–60% canopy cover within the production area moderate temperature extremes '
        'and maintain the natural humidity that slows coffee fruit development, '
        'extending the maturation period by 2–3 weeks compared to cerrado (savanna) '
        'coffee zones. This extended maturation window is the primary driver of '
        'Matas de Minas cup quality: the additional weeks of fruit development allow '
        'greater sucrose accumulation in the coffee cherry (measured at 14–18% Brix '
        'at optimal harvest) that translates directly to sweetness and body in the '
        'cup. The Yellow Catuaí variety (Coffea arabica Catuaí Amarelo) is a '
        'Brazilian IAPAR-developed hybrid of Mundo Novo and Caturra, selected for '
        'compact plant architecture and high production — but at Matas de Minas '
        'altitudes above 900m, Catuaí Amarelo demonstrates cup quality that '
        'approaches Ethiopia Guji and Colombia Huila specialty benchmarks, '
        'disproving the assumption that hybrid commercial varieties cannot achieve '
        'specialty cup scores.'
    ),
    'production_technique': (
        'Matas de Minas honey process begins with selective hand-picking of fully ripe '
        'coffee cherries (deep red or, for Catuaí Amarelo, deep yellow at peak brix) '
        'in the harvest window of May–September — Brazil\'s dry season that coincides '
        'with coffee cherry maturation. Selective picking at Fazenda Santuário Sul and '
        'comparable Carmo de Minas farms targets 18+ Brix cherry sugar content and '
        'uniform ripeness, typically requiring 3–5 passes through the same trees over '
        '4–6 weeks as individual fruits ripen sequentially. Post-harvest, cherries are '
        'pulped mechanically to remove the outer skin (exocarp) while leaving the '
        'mucilage layer (the sticky, sugar-rich mesocarp) intact on the parchment-covered '
        'seed. The mucilage retention percentage defines the honey process type: '
        'yellow honey (20–30% mucilage retained), red honey (50–70%), and black honey '
        '(90–100%). Matas de Minas producers typically target red honey for the optimal '
        'balance between controlled drying and flavor complexity — black honey risks '
        'fermentation and off-flavor development in humid Atlantic Forest conditions '
        'where relative humidity during the drying period may reach 75–85%. Drying '
        'takes place on raised African beds in full sun for 18–28 days, with frequent '
        'raking (every 2–3 hours during sunlight hours) to prevent anaerobic fermentation '
        'in the mucilage layer. The target moisture content at the end of drying is '
        '10.5–11.5%. Drying slower than this increases fermentation complexity (positive '
        'contribution to red fruit cup character from controlled lactic acid bacteria '
        'activity on the mucilage layer); faster drying produces a cleaner cup with '
        'less fruit character. Post-drying, the parchment-covered coffee rests in '
        'warehouses for 30–60 days before milling (hulling, sorting, grading). '
        'The honey process at Matas de Minas elevations produces a cup profile '
        'that bridges Brazil\'s traditionally clean-sweet-chocolate natural cup style '
        'and Ethiopian washed coffee\'s red fruit and floral character: honey-process '
        'Matas de Minas Catuaí Amarelo typically scores 86–90+ SCA on clean cups '
        'with red fruit (plum, cherry, raspberry) character from the controlled '
        'mucilage fermentation, chocolate and caramel sweetness from the natural '
        'sugar development, and the medium body characteristic of Brazilian coffee '
        'at altitude.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Ethiopia Yirgacheffe Washed (acidic, floral, Heirloom Arabica)',
            'connection': (
                'Matas de Minas honey process Catuaí Amarelo and Ethiopia Yirgacheffe '
                'washed represent opposite poles of the specialty coffee flavor '
                'spectrum from the same Coffea arabica species: Yirgacheffe achieves '
                'its defining citrus-floral-tea-like character through complete mucilage '
                'removal in washed processing that maximizes acidity expression from '
                'the high-altitude Ethiopian terroir; Matas de Minas honey process '
                'retains 50–70% mucilage that converts sugar to lactic acid '
                'during drying, producing red fruit character that partially '
                'bridges Yirgacheffe\'s washed intensity with Brazil\'s natural '
                'sweetness. Both approaches demonstrate how post-harvest processing '
                'rather than just origin determines the fundamental cup character '
                'within the same species at comparable altitudes (1,750–2,200m '
                'Yirgacheffe; 900–1,200m Matas de Minas).'
            )
        },
        {
            'tradition': 'Colombia Huila Natural Process (Pacific drainage, red fruit specialty)',
            'connection': (
                'Both Matas de Minas honey process and Colombia Huila natural process '
                'coffees represent the emergence of Latin American specialty production '
                'that challenges the Ethiopia-Kenya African terroir assumption about '
                'the origins of red-fruit cup character. Colombia Huila natural and '
                'honey process lots at 1,700–2,000m now achieve SCA scores of 87–92, '
                'directly comparable to Matas de Minas honey process at 900–1,200m; '
                'both demonstrate that altitude moderates the flavor impact of latitude '
                '(both are 2–10°N tropical) and that processing technique can shift '
                'flavor character across the clean-to-fermented spectrum independent '
                'of terroir parameters.'
            )
        },
        {
            'tradition': 'Timor-Leste Ermera Arabica (Atlantic colonial connection)',
            'connection': (
                'Both Brazilian Matas de Minas Coffea arabica and Timor-Leste Ermera '
                'Coffea arabica descend from Portuguese colonial agricultural transfer: '
                'Portugal introduced Coffea arabica to Brazil from Africa (via the '
                'Portuguese colonial network, ca. 1727) and to Timor from Portuguese '
                'colonial Mozambique/East Africa connections. Both coffees retain '
                'genetic heritage from the same Portuguese colonial botanical '
                'network that connected Ethiopia, Brazil, and Timor through Lisbon — '
                'making the PCT the agricultural DNA connector between the world\'s '
                'two most geographically distant major coffee origins.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Dry fragrance: red cherry compote, dark chocolate, dried mango — '
            'the honey process mucilage character immediately apparent as aromatic '
            'intensity before water contact; brewed liquor (filter): '
            'medium amber-gold, clear and bright, no sedimentation from careful '
            'honey process drying; espresso: deep mahogany with reddish tints, '
            'medium-fine crema from the balanced CO2 release of honey process '
            'drying; no defect colors (no yellow indicating under-ripe; no '
            'black indicating over-fermented).'
        ),
        'nose': (
            'Aroma (wet, bloomed): red plum, black cherry, dried cranberry from '
            'the honey process lactic fermentation character; underlying dark '
            'chocolate and brown sugar from the Catuaí Amarelo natural sweetness '
            'at 900–1,100m maturation; faint jasmine and stone fruit florality '
            'from the 2–3 week extended maturation of Atlantic Forest moderated '
            'cherry development; in espresso, the same characters concentrated '
            'with additional chocolate intensity and maple syrup sweetness from '
            'the Maillard reaction compounds developing at roast.'
        ),
        'palate': (
            'Medium body with honey process texture — the retained mucilage '
            'contributes a silky, round mouthfeel that washed Brazil coffees '
            'do not achieve; sweetness high and clean from Catuaí Amarelo sucrose '
            'content (18+ Brix cherry); acidity medium, bright and citrus-adjacent '
            'from the lactic acid development in the drying mucilage; red fruit '
            '(cherry, plum, dried cranberry) through the mid-palate resolving '
            'into dark chocolate on the finish; aftertaste: long, sweet, '
            'lingering red fruit and chocolate; SCA balance score: 9+ on well-'
            'executed red honey process lots from Carmo de Minas at Cup of Excellence.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Brazilian Santos Grade 2',
            'criteria': (
                'Strip-harvested, mechanically processed, washed or pulped-natural '
                'without selective picking or quality-sort drying — the commodity '
                'benchmark at 80–82 SCA; the baseline Brazilian arabica that '
                'establishes the category\'s signature chocolate-nut-low-acid '
                'character without specialty distinction.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Sul de Minas Yellow Honey Process',
            'criteria': (
                '20–30% mucilage retention, selective picking, raised-bed drying; '
                '84–86 SCA; the accessible entry tier for honey process Brazil '
                'specialty, demonstrating clean sweetness and mild red fruit '
                'character without the complexity of red honey process.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Matas de Minas Red Honey Process (estate lot)',
            'criteria': (
                '50–70% mucilage retention, 18+ Brix selective harvest, 18–28 day '
                'raised-bed drying, Atlantic Forest elevation 900–1,100m; 87–90 SCA; '
                'the benchmark Matas de Minas specialty tier demonstrating red fruit, '
                'chocolate, and honey-sweetness integration that defines the region\'s '
                'identity.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Cup of Excellence Carmo de Minas (auction lot)',
            'criteria': (
                'Cup of Excellence-placed lots from the Carmo de Minas cluster — '
                '90+ SCA, exceptional fruit clarity, honey process precision with '
                'controlled fermentation; typically available only through COE '
                'auction (bids at USD $10–40/lb) and the specialty roasters who '
                'purchase direct from auction; the apex Brazilian coffee quality '
                'demonstrating that Matas de Minas altitude and honey process '
                'discipline can produce African-benchmarking cup quality in South America.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Filter (pour-over, V60 or Chemex): brew at 93–95°C with a water '
            'temperature no lower than 90°C to extract the honey process red '
            'fruit compounds that require higher extraction temperature than '
            'washed coffees; serve at 70–80°C for immediate tasting; allow to '
            'cool to 50–60°C for the full red fruit and chocolate character '
            'to emerge — the honey process Matas de Minas gains sweetness and '
            'fruit clarity as temperature drops from brew temperature to '
            '55°C. Espresso: extract at 93°C at 9 bar, 25–30 second pull, '
            '1:2 ratio (18g in, 36g out) for maximum sweetness and red fruit '
            'character from the honey process base.'
        ),
        'vessel': (
            'For pour-over service: wide-mouthed ceramic pour-over server or '
            'glass Chemex to showcase the amber-red liquor color and allow '
            'the red fruit aromatics to open at 70°C; white ceramic cup for '
            'cupping evaluation following SCA protocol (cupping ratio 8.25g '
            'per 150ml water, 93°C brew). For espresso service: white '
            'ceramic demitasse (60ml capacity, 36ml espresso fill) at '
            'pre-warmed 45°C cup temperature to prevent heat shock at '
            'the brew temperature transition; the red honey process '
            'Catuaí Amarelo is equally suited to filter and espresso '
            'service — a versatility rare in Brazilian coffee at this quality tier.'
        ),
        'programme_position': (
            'In a PCT Brazil beverages programme: serve as the post-cachaça '
            'palate-cleanser before the sparkling wine tier — the coffee\'s '
            'sweetness and red fruit character after cachaça\'s sugarcane '
            'intensity demonstrates the full Brazilian agricultural spectrum '
            'from fermented spirits to specialty coffee within the same '
            'Portuguese colonial agricultural heritage zone.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Fazenda Santuário Sul — Carmo de Minas, Minas Gerais (Pereira family, '
            'multiple Cup of Excellence placements, benchmark for Matas de Minas '
            'honey process Catuaí Amarelo); Fazenda Santa Inês (Carmo de Minas) '
            'as secondary benchmark with Bourbon Amarelo focus.'
        ),
        'north_america_access': (
            'Intelligentsia Coffee, Counter Culture Coffee, Onyx Coffee Lab, '
            'and Chromatic Coffee direct-import Carmo de Minas lots; '
            '49th Parallel (Vancouver BC) and Pilot Coffee (Toronto) carry '
            'Brazilian Sul de Minas/Matas de Minas specialty lots seasonally. '
            'Cup of Excellence auction lots: bids open at cuppingscores.com '
            'annually (Brazil COE: June–August auction window). '
            'Retail: USD $22–40 per 250g for honey process specialty lots; '
            'COE lots at USD $50–150+ depending on auction results.'
        ),
        'culinary_application': (
            'Matas de Minas honey process Catuaí Amarelo in PCT culinary programming: '
            'the red fruit and chocolate character pairs with Brazilian chocolate '
            '(Amma Chocolate, Bahia State) for a within-country agricultural '
            'pairing demonstration; the honey-process sweetness also bridges '
            'with Brazilian dessert preparations (brigadeiro, quindim) for '
            'a post-dinner coffee programme that stays within the Portuguese '
            'colonial agricultural network from Brazil across to São Tomé and Cape Verde.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
