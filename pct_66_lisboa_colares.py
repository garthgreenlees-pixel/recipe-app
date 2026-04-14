import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Lisboa (Colares Ramisco, Sandy Atlantic Dunes, Pre-Phylloxera Ungrafted Vines)',
    output_dir='.',
    starting_entry=1,
    session_number=70,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Adega Regional de Colares — Colares, Sintra, Lisboa',
    'location': 'Colares, Sintra Peninsula, Lisboa, Portugal',
    'description': (
        'Adega Regional de Colares is the surviving cooperative winery of the '
        'Colares DOC — one of the rarest and most historically significant wine '
        'institutions in Europe. Founded in 1931 as the Adega Cooperativa Regional de '
        'Colares, it became the de facto guardian of the Ramisco grape and the sandy '
        'Atlantic dune vineyards of Colares when suburban expansion from Lisbon began '
        'consuming the coastal vineyard land from the 1960s onward. The adega '
        'controls the only significant remaining production of Colares DOC wine — '
        'the Ramisco red DOC wine that survived phylloxera because the sandy soil '
        'of the Atlantic dunes prevented the louse from establishing. Colares '
        'represents one of the last surviving pre-phylloxera ungrafted wine regions '
        'in Europe, alongside the sandy soils of Champagne\'s La Marne and '
        'the coastal sands of Colares itself. Annual production has declined to '
        'fewer than 50,000 bottles, making Adega Regional de Colares among the '
        'smallest DOC producers in the Portuguese wine system by volume.'
    ),
    'founded': '1931',
    'region': 'Colares DOC, Sintra Peninsula, Lisboa, Portugal',
    'website': 'adegadecolares.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Wines of Portugal / specialist Portuguese importers',
    'type': 'importer',
    'description': (
        'Colares DOC is among the hardest Portuguese wines to source in North America '
        'due to the extremely limited production volumes and the rarity of the wine '
        'in international distribution. Specialty Portuguese wine importers in the '
        'United States — including Broadbent Selections (San Francisco) and '
        'Skurnik Wines (New York) — occasionally carry Adega Regional de Colares '
        'on allocation. In Canada, BCLDB and LCBO rarely list Colares on permanent '
        'allocation; access is primarily through specialty retailers importing '
        'directly from Portugal. The wine is primarily consumed in Portugal, '
        'particularly in Lisbon restaurants with serious national wine programmes. '
        'For North American trade buyers, pre-arranged direct import through '
        'Wines of Portugal trade network is the most reliable sourcing route.'
    ),
    'markets_served': ['Portugal', 'UK', 'US'],
    'traditions_carried': ['wine'],
    'website': 'adegadecolares.pt',
    'verified': False
})

session.add_beverage({
    'name': (
        'Adega Regional de Colares Ramisco Tinto — Colares DOC, Sandy Atlantic Dunes, '
        'Pre-Phylloxera Ungrafted Vines, Sintra Peninsula'
    ),
    'category': 'wine',
    'subcategory': 'wine_still',
    'origin': 'Portugal',
    'region': 'Portugal — Lisboa (Colares Ramisco, Sandy Atlantic Dunes, Pre-Phylloxera Ungrafted Vines)',
    'producer': 'Adega Regional de Colares — Colares, Sintra, Lisboa',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Colares DOC occupies a narrow band of Atlantic coastal dune land on the '
        'Sintra Peninsula, approximately 35km west of Lisbon between the Serra de '
        'Sintra granite ridge and the Atlantic Ocean at altitudes of 0–50m. The '
        'defining geological feature of Colares is its soil: deep windblown maritime '
        'sand lying over clay and rock, in some places 4–8 metres deep. This sand '
        'is the reason Colares survived phylloxera (Daktulosphaira vitifoliae) — '
        'the insect that destroyed virtually all ungrafted Vitis vinifera in Europe '
        'between 1860 and 1900. Phylloxera cannot travel through deep, loose, dry '
        'sand; the louse requires compacted moist soil to burrow to vine roots. '
        'In Colares\' maritime sand, phylloxera never established, and the '
        'indigenous Ramisco grape has been growing on its own ungrafted Vitis '
        'vinifera roots for centuries — one of the only places in Europe where '
        'this is true at DOC scale. The Atlantic Ocean is 1–2km distant, '
        'moderating temperatures year-round: Colares records mean summer temperatures '
        'of 19–21°C (cooler than Lisbon\'s 25–27°C), with persistent Atlantic '
        'fog (the nevoeiro) reducing UV radiation and slowing Ramisco\'s ripening '
        'cycle. Annual rainfall of 600–700mm is concentrated in winter; '
        'the summer months are dry and salt-laden from Atlantic winds that '
        'stress the surface vegetation. Ramisco vines are planted in a unique '
        'way to survive the dune conditions: the vines are trained along the '
        'ground on pergola-type structures (ramadas) to reduce wind exposure '
        'and keep the fruiting zone away from the salt spray at ground level.'
    ),
    'production_technique': (
        'Colares Ramisco production is among the most labour-intensive and '
        'technically demanding in Portugal. The sandy dune soil makes mechanical '
        'harvesting impossible — the loose sand cannot support tractor weight '
        'and the ramada vine training system requires hand harvesting of each '
        'bunch individually. Workers must dig down through the sand to reach '
        'the clay layer beneath before planting replacement vines — a process '
        'called "galloping" in which a trench is dug 4–8 metres deep to plant '
        'the vine below the sand into the underlying clay, then the trench is '
        'refilled with sand. The vine then grows upward through the sand on its '
        'own ungrafted Ramisco root system. This planting method takes 3–5 '
        'years of labour before the first harvest, making vine replacement '
        'economically marginal for a DOC wine with production under 50,000 '
        'bottles annually. Ramisco is harvested in October — the variety is '
        'late-ripening with naturally high acidity and very high tannin, '
        'similar in structural character to Baga of Bairrada. At Adega '
        'Regional de Colares, the harvested Ramisco is foot-trodden in '
        'stone lagares to begin extraction before transferring to old large-format '
        'oak toneis (500–2000L) for fermentation and extended skin contact of '
        '25–40 days — far longer than modern Portuguese winemaking practice '
        'and consistent with the cooperative\'s pre-modern production methods '
        'that have been maintained since 1931. The extended maceration extracts '
        'the maximum colour and tannin from the thick-skinned Ramisco variety; '
        'the wine is then aged 2–5 years in large-format old oak before '
        'bottling without filtration. The result is a wine of extraordinary '
        'tannin concentration and natural acidity that requires a minimum of '
        '10–15 years bottle aging in the finest vintages. Colares red wine '
        'has historical documentation of 30–50 year aging potential from '
        'early 20th century vintages still drinking in the 1970s and 1980s.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Champagne Les Sables (sandy coastal vineyards, phylloxera survival)',
            'connection': (
                'Colares and the sandy soils of Champagne\'s La Marne Valley represent '
                'two of the most documented examples of phylloxera-free wine production '
                'in Europe due to the same mechanism: the inability of the phylloxera '
                'louse to travel through deep, dry maritime or alluvial sand. In both '
                'cases, ungrafted indigenous vines survived the 19th-century epidemic '
                'that destroyed all neighbouring vineyards. The parallel extends to '
                'the winemaking philosophy: both Colares and Champagne\'s sandy-soil '
                'plots produce wines of unusual longevity attributed to the direct '
                'root expression of ungrafted vines without American rootstock '
                'mediation — a terroir argument that is contested by ampelographers '
                'but supported by empirical aging evidence at both appellations.'
            )
        },
        {
            'tradition': 'Bairrada Baga Vinhas Velhas (pre-phylloxera ungrafted, heavy clay, Atlantic)',
            'connection': (
                'Colares Ramisco and Bairrada Baga Vinhas Velhas are the two benchmark '
                'pre-phylloxera Portuguese reds — both surviving through a geological '
                'accident that repelled phylloxera (Colares: sand; Bairrada: heavy '
                'blue clay). Both produce wines of extreme tannin concentration and '
                'high natural acidity that demand long bottle aging (10–20+ years) '
                'and that have been historically undervalued because of their '
                'structural austerity in youth. Both are produced in declining '
                'vineyard areas under existential economic pressure — Colares from '
                'Lisbon suburban expansion; Bairrada from replanting with '
                'international varieties. Both are also produced by cooperatives '
                'or single-champion producers (Adega Regional de Colares; Luis '
                'Pato) who have maintained the indigenous variety against commercial '
                'pressure — making them the twin pillars of Portuguese wine '
                'heritage preservation.'
            )
        },
        {
            'tradition': 'Santorini Assyrtiko (volcanic sandy island terroir, ungrafted basket vines)',
            'connection': (
                'Santorini Assyrtiko and Colares Ramisco share the survival of '
                'ungrafted indigenous vines through volcanic or sandy soils hostile '
                'to phylloxera, producing wines of extreme mineral concentration '
                'and high natural acidity from low-yield, old-vine material. '
                'The Santorini kouloura (basket-trained) vine system trained close '
                'to the volcanic pumice and ash soil parallels the Colares ramada '
                'system trained along the sandy dune surface — both are adaptations '
                'to harsh Atlantic or Aegean wind conditions. Both wines occupy '
                'the same collector tier as near-extinct indigenous expressions '
                'with documented 20–40 year aging trajectories from their '
                'respective pre-phylloxera old vine material.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep garnet-ruby with purple-tinted rim in young vintages (3–5 years), '
            'reflecting the high anthocyanin extraction from extended maceration '
            'of thick-skinned Ramisco in stone lagares; the colour intensity is '
            'exceptional for a 12% ABV wine — the low alcohol does not reflect '
            'a dilute extraction. In mature vintages (10–20 years), the garnet '
            'transitions to brick-tawny at the rim with the orange-red development '
            'typical of long-aged high-tannin Portuguese reds; the core remains '
            'deeply coloured well into the second decade.'
        ),
        'nose': (
            'Young Colares Ramisco (3–8 years): Atlantic salt minerality as the '
            'immediate register — the proximity of the ocean and the maritime '
            'sand substrate project a saline, iodine-tinged character unique in '
            'Portuguese red wine; beneath the salt, dark cherry, blackberry, and '
            'dried herbs (rosemary, thyme from the Atlantic coastal garrigue); '
            'old leather and tobacco from the extended large-oak aging; the '
            'Ramisco varietal character includes a distinctive graphite and '
            'iron mineral note attributed to the clay layer beneath the sand. '
            'Mature expressions (15–25 years): the primary fruit recedes into '
            'dried fig, leather, tobacco, and forest floor secondary aromas; '
            'the saline Atlantic character persists through decades of '
            'bottle aging as a defining aromatic signature of the appellation.'
        ),
        'palate': (
            'Austere and demanding in youth: very high, very firm tannin from '
            'the 25–40 day maceration of thick-skinned Ramisco; very high '
            'natural acidity (pH 3.2–3.4) from the cool Atlantic climate '
            'and late Ramisco harvest; medium body despite the tannin '
            'concentration — the 11.5–12.5% ABV level means the wine is '
            'built on structure rather than extract weight. Dark cherry '
            'and blackberry fruit through the mid-palate; the Atlantic '
            'salt-mineral character threading through the finish; the '
            'long, austere finish defined by tannin and acidity rather '
            'than fruit — a finish architecture that does not resolve '
            'until 10–15 years of bottle aging have allowed tannin '
            'polymerization to soften the structural grip.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Colares Branco (white wine from Malvasia grape, lesser tier)',
            'criteria': (
                'Colares DOC white wine from the Malvasia variety grown on the same '
                'sandy Atlantic soils; less structurally demanding than Ramisco red, '
                'earlier drinking (3–7 years), lower tannin, the saline Atlantic '
                'mineral character present but at lower intensity than the red; '
                'the white is the entry point to Colares appellation character '
                'without the full structural commitment of Ramisco red wine.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Colares DOC Ramisco (cooperative standard, mid-vintage)',
            'criteria': (
                'Adega Regional de Colares standard Ramisco production from '
                'cooperative-sourced fruit; full extended maceration and large-oak '
                'aging; the complete Ramisco structural profile; best vintages '
                '(2017, 2019, 2011) show the full Atlantic-mineral and tannin '
                'concentration; lesser vintages produce wine that never fully '
                'resolves its structural austerity even with extended bottle aging.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Colares DOC Ramisco (single-quinta old vine selection)',
            'criteria': (
                'Single-vineyard selection from the oldest pre-phylloxera Ramisco '
                'plots within the Colares dune system; lowest yields (10–15 hl/ha) '
                'from ungrafted vines of 80–150 years old; extended maceration '
                '30–40 days; additional large-oak aging to 4–5 years before '
                'bottling; the apex of Colares aromatically and structurally, '
                'with a documented 20–40 year aging potential comparable to '
                'historic early 20th century Colares vintages.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Colares DOC Historic Vintages (pre-1970s, cellar library)',
            'criteria': (
                'Historic Colares Ramisco from the mid-20th century, before Lisbon '
                'suburban expansion began eliminating the dune vineyards; production '
                'volumes were significantly higher (the DOC once covered hundreds '
                'of hectares versus the current fewer than 20 hectares under vine). '
                'These historic vintages from the 1940s–1970s represent the apex '
                'of Colares production volume and quality simultaneously; surviving '
                'bottles are held in the Adega Regional de Colares cellar and '
                'at specialist Portuguese wine auction, and demonstrate the '
                '40–50 year aging potential of Ramisco from the Sandy Atlantic dunes.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Young Colares Ramisco (3–8 years) at 17–18°C after mandatory '
            'decanting of 2–3 hours minimum — the tannin concentration from '
            '25–40 day maceration requires substantial oxygen contact to '
            'begin softening before the wine can be assessed; serve without '
            'decanting and the tannin will dominate every other sensory '
            'dimension. Mature expressions (12–25 years) at 16°C with '
            '45–60 minutes decanting — enough to open the secondary leather '
            'and dried fruit aromas without dissipating them through excessive '
            'oxidation; older vintages (pre-1980) should be decanted gently '
            'through a fine mesh or coffee filter to remove the heavy '
            'unfiltered sediment before service.'
        ),
        'vessel': (
            'Large-format Burgundy or Barolo glass with wide bowl to capture '
            'the Atlantic salt-mineral aromatic register and allow the '
            'extraordinary tannin structure to expand through the surface area; '
            'pour 100–120ml maximum per service — Colares Ramisco at high '
            'concentration rewards considered, analytical tasting more than '
            'generous pours; the saline Atlantic character is most apparent '
            'in the first nosing before the glass warms; serve with a '
            'verbal presentation explaining the pre-phylloxera ungrafted '
            'vine status and the sandy Atlantic dune provenance — Colares '
            'is one of the most historically significant wines in the '
            'European viticultural record and merits the full contextual '
            'introduction in a professional programme.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Adega Regional de Colares — the only significant remaining producer '
            'of Colares DOC Ramisco red; the cooperative has been the guardian '
            'of the Ramisco grape and the pre-phylloxera sandy dune vineyards '
            'since 1931; without the cooperative, Colares DOC would effectively '
            'cease to exist as a commercial wine appellation. Any Colares DOC '
            'red wine in professional trade is sourced from or through Adega '
            'Regional de Colares.'
        ),
        'north_america_access': (
            'Colares Ramisco is among the rarest Portuguese wines in North '
            'American distribution — annual production under 50,000 bottles '
            'means most production is consumed in Portugal and the UK. '
            'Broadbent Selections (San Francisco) and Wines of Portugal '
            'trade network are the primary access routes for US trade buyers. '
            'Pricing reflects scarcity rather than production cost: USD $40–80 '
            'for standard vintages; older vintages from the Adega cellar '
            'reserve command USD $100–200+ at auction.'
        ),
        'culinary_application': (
            'Colares Ramisco demands food with structural weight and fat to '
            'absorb the tannin — historically served with leitão da Bairrada '
            '(suckling pig) in Lisbon restaurants, or with bacalhau com broa '
            '(salt cod with cornbread) which provides the starch to buffer '
            'the tannin concentration. The Atlantic saline character of '
            'Ramisco also creates an unusual affinity with grilled fish — '
            'the high tannin is too much for delicate fish, but the salt-mineral '
            'register bridges to grilled sardines or sea bream in a way that '
            'most red wines cannot.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
