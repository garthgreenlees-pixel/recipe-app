import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='Timor-Leste — Ermera and Manufahi Districts (Arabica Heritage Varieties, Shade-Forest, Colonial Portuguese and Indonesian Legacy)',
    output_dir='.',
    starting_entry=1,
    session_number=44,
    running_total=0
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Cooperativa Café Timor (CCT) — Ermera District',
    'location': 'Gleno, Ermera District, Timor-Leste',
    'description': "Cooperativa Café Timor (CCT) is the largest agricultural cooperative in Timor-Leste, established in 1994 by USAID during the Indonesian occupation period to provide an economic alternative to the conflict-torn coffee sector. CCT represents over 21,000 smallholder farmer families across Ermera, Aileu, and Ainaro districts — the primary coffee-growing highlands of western Timor at 1,200-1,800m elevation. Ermera District is Timor-Leste's most important coffee zone, with some of the oldest surviving Arabica plantations in Asia: the Portuguese established coffee cultivation on Timor in the 1860s under the forced cultivation system (Timor Coffee Regulation 1863) that required all Timorese households to cultivate a minimum number of coffee trees. Many of these trees survive today as old-growth Arabica specimens of 100-150 years old — among the oldest cultivated Arabica trees in the world.",
    'founded': '1994',
    'region': 'Ermera District, Timor-Leste',
    'website': 'cafetimor.com',
    'verified': True
})

session.add_producer({
    'tradition': 'coffee',
    'name': 'Timor Morningstar Coffee — Manufahi Specialty',
    'location': 'Same, Manufahi District, Timor-Leste',
    'description': "Timor Morningstar is a specialty-focused exporter working with smallholder producers in Manufahi (Same) and Ainaro districts to produce competition-grade washed and natural-process Arabica lots for the international specialty market. The company works with the hybrid Timor-Hybrido variety — a spontaneous cross between Arabica and Robusta discovered on Timor in 1927 that has become one of the most important genetic resources in global coffee breeding for its natural resistance to coffee leaf rust (CLR) disease. All specialty Timor-Hybrido work contributes to the global understanding of disease-resistant Arabica breeding.",
    'founded': '2012',
    'region': 'Manufahi District, Timor-Leste',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'PT. Imex Maju Bersama / Equal Exchange (US) / Ethical Bean (Canada)',
    'type': 'importer',
    'description': "CCT exports through Equal Exchange (US fair trade importer) which distributes Timor-Leste coffee widely through fair trade and natural food channels in the US. Ethical Bean (Vancouver, BC) has sourced Timor-Leste coffee through the fair trade network. The PCT narrative around Timor-Leste's Portuguese colonial heritage and Indonesian occupation makes this origin compelling for ethically-minded restaurant and café programming in Vancouver.",
    'markets_served': ['US', 'Canada', 'EU', 'Australia'],
    'traditions_carried': ['coffee'],
    'website': 'equalexchange.coop',
    'verified': True
})

session.add_beverage({
    'name': "Timor-Leste Ermera Arabica — Old-Growth Colonial Plantation, Shade Forest, 100-Year Tree Heritage, CCT Cooperative",
    'category': 'coffee',
    'subcategory': 'arabica_single_origin',
    'origin': 'Timor-Leste',
    'region': 'Timor-Leste — Ermera and Manufahi Districts (Arabica Heritage Varieties, Shade-Forest, Colonial Portuguese and Indonesian Legacy)',
    'producer': 'Cooperativa Café Timor (CCT) — Ermera District',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Ermera District sits in the central highlands of Timor-Leste (the eastern half of Timor island; the western half is Indonesian West Timor) at 1,200-1,800m elevation above the Comoro River valley. The district's volcanic highlands — part of the same Australian tectonic plate thrust that created Timor island's distinctive geology — produce soils with exceptional mineral content: a mixture of sandstone, limestone, and alluvial volcanic deposits from the ancient collision of the Australian and Sunda plates that formed the island approximately 5 million years ago. The equatorial location at 8°S and the elevation combine to produce a tropical highland climate: afternoon cloud cover (natural shade for coffee cultivation), high humidity from the monsoon season (December-March), and a distinct dry season (May-October) that concentrates sugars in the maturing coffee cherries. The 100-150 year old coffee trees in Ermera's forest gardens represent a living library of pre-industrial Arabica genetic diversity: the Portuguese forced-cultivation system of the 1860s introduced Typica and Bourbon varieties from Indonesia (Sumatra and Java) and the trees have adapted to Timor's unique soil and climate conditions over multiple generations — these old-growth trees produce very low yields (under 0.5 tonnes per hectare) but with exceptional flavor concentration."
    ),
    'production_technique': (
        "CCT's Ermera Arabica is produced using the washed process: ripe red cherries are hand-picked from the old-growth shade trees by CCT smallholder members, depulped at village-level processing stations to remove the fruit skin and pulp, then fermented in water for 24-48 hours to break down the mucilage layer before washing and sun-drying on raised drying beds for 10-15 days. The quality control program — unusually rigorous for a developing-country cooperative of this scale — includes cherry sorting at harvest (red-only picking), fermentation monitoring to prevent over-fermentation defects, and export-grade moisture measurement before sacking. The result is a washed Arabica of clean mineral clarity and distinct terroir character: the old-growth trees' concentrated cherry production translates into a cup with more complexity and body than younger-tree Arabica from the same region. The Timor-Hybrido component (where present in the blend) contributes a distinctive earthy-chocolate body that is specific to Timor's genetic heritage. CCT exports approximately 3,000 tonnes of green coffee annually, of which roughly 15% qualifies for specialty grade (SCA 84+)."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Ethiopia Yirgacheffe Washed (African Arabica heritage origin, forest-garden, genetic diversity)',
            'connection': "Timor-Leste Ermera Arabica and Ethiopia Yirgacheffe both represent Arabica coffee grown in forest-garden systems where old-growth trees adapted to shade conditions produce exceptional terroir-specific character — Ethiopia from the original Arabica wild genetic pool, Timor from the 19th-century colonial plantation adaptation of the same variety to Southeast Asian volcanic highland conditions; both are reference expressions of how the forest ecology transforms coffee character"
        },
        {
            'tradition': 'Hawaii Kona Arabica (PCT connection, volcanic island, colonial plantation heritage)',
            'connection': "Timor-Leste Ermera and Hawaii Kona both produce Arabica from colonial-era plantations on volcanic islands in the Pacific trade wind zone, both with origin stories rooted in 19th-century colonial agricultural policy (Portuguese forced cultivation in Timor, missionary agricultural experiments in Hawaii), and both producing small-volume specialty coffee of genuine terroir distinction that commands premium pricing commensurate with the production difficulty"
        }
    ],
    'sensory_profile': {
        'appearance': 'Green bean: dense, olive-green with good uniformity; roasted at medium: milk chocolate brown with slight red tints; brewed: golden amber clarity',
        'nose': 'Clean and fruit-forward for a washed Southeast Asian origin: dark cherry, mild citrus (lime, orange zest), earthy chocolate undertone from the Timor-Hybrido heritage, hint of forest undergrowth and cedar from the shade-forest cultivation environment; less floral than Ethiopian but more complex than Indonesian commercial grades',
        'palate': 'Medium-full body (fuller than Ethiopia, lighter than Sumatra); bright acidity (the washed process preserves the volcanic highland acidity); clean mid-palate of dark cherry and mild chocolate; the finish shows the earthy-mineral character of the old-growth volcanic terroir; long, clean finish without the harsh astringency of lower-elevation or natural-process Indonesian origins',
        'conclusion': 'Specialty-grade Pacific colonial heritage coffee of genuine terroir distinction; best served as pour-over or Chemex to highlight the clean fruity-mineral character; quality at SCA 85-88 for CCT premium lots'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'CCT Standard Blend (commodity fair trade)',
            'criteria': "CCT's primary export: blended Ermera and Ainaro coffee at fair trade premium pricing; SCA 80-83; the volume expression of Timor-Leste's coffee heritage without parcel selection"
        },
        {
            'tier': 2,
            'tier_name': 'CCT Premium Ermera Washed (specialty grade)',
            'criteria': 'Selected-cherry washed lots from Ermera old-growth trees; SCA 84-86; the accessible premium expression of Timor-Leste Arabica for specialty roasters'
        },
        {
            'tier': 3,
            'tier_name': 'CCT Old-Growth Single-Village Washed',
            'criteria': "Single-village lots from identified Ermera villages with the oldest tree populations; SCA 86-88; the precision tier showing how the 100-year-old trees express Timor's volcanic terroir with concentrated complexity"
        },
        {
            'tier': 4,
            'tier_name': 'Timor Morningstar Manufahi Natural Lot',
            'criteria': 'Natural-process specialty lot from Manufahi District; SCA 88-90; the fruit-forward expression of Timor heritage showing the Timor-Hybrido genetic complexity in natural-process style; available through specialty roaster auctions'
        }
    ],
    'service_intelligence': {
        'temperature': 'Brew water at 93-95°C; the washed Ermera benefits from standard specialty coffee brew temperature; slightly higher than Ethiopia recommendation due to the fuller body and lower acidity relative to East African origins',
        'vessel': 'Pour-over (V60 or Chemex) to emphasize the clean cherry-mineral clarity; AeroPress for the earthy-chocolate character of the Timor-Hybrido component',
        'programme_position': 'Post-dinner coffee course as an alternative to more familiar origins; the PCT narrative — Portuguese colonial forced cultivation, Indonesian occupation, independence 2002 — provides a complete food-politics story for engaged dining contexts; pair with dark chocolate (70%+) from São Tomé for the Pacific-Atlantic Portuguese colonial cacao-coffee pairing'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Cooperativa Café Timor (CCT) — the benchmark producer for volume and fair trade; Timor Morningstar for specialty lot depth',
        'north_america_access': 'Equal Exchange (US): widely available in natural food retail; Ethical Bean (Vancouver BC): occasional Timor sourcing through fair trade network; the PCT narrative and East Timor political story make this a compelling choice for ethically-focused restaurant coffee programming',
        'culinary_application': 'The Timor-Leste narrative is the most politically resonant of all PCT origins — Portuguese colonial forced cultivation, 24 years of Indonesian occupation (1975-1999), the independence referendum and UN intervention in 1999, and the youngest nation in Asia. CCT coffee represents the economic recovery built from the coffee trees the Portuguese planted 160 years ago — the most direct connection in the PCT between colonial agricultural history and post-colonial food sovereignty'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('coffee', 'Timor-Leste — Aileu and Ainaro Districts (Timor-Hybrido Genetic Heritage, Rust-Resistant Arabica, Mountain Spring Water Processing)')

session.add_producer({
    'tradition': 'coffee',
    'name': 'Seeds of Life / Oxfam Australia — Ainaro Specialty Coffee Program',
    'location': 'Ainaro, Ainaro District, Timor-Leste',
    'description': "Ainaro District in the southern highlands of Timor-Leste (1,300-1,700m elevation) is the source of some of the country's highest-quality specialty Arabica, particularly from the Timor-Hybrido variety — the naturally occurring Arabica × Robusta hybrid first documented on Timor in 1927 that has become a critical genetic resource for global coffee breeding programs. The Seeds of Life agricultural development program (Australian DFAT-funded) supports smallholder coffee producers in Ainaro with post-harvest processing infrastructure including wet mills and drying beds, upgrading quality from commercial grade to specialty level.",
    'founded': '2000 (Seeds of Life program)',
    'region': 'Ainaro District, Timor-Leste',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': "Timor-Hybrido Ainaro Natural Process — Rust-Resistant Genetic Heritage, Mountain Spring Water, Southeast Pacific Terroir",
    'category': 'coffee',
    'subcategory': 'arabica_single_origin',
    'origin': 'Timor-Leste',
    'region': 'Timor-Leste — Aileu and Ainaro Districts (Timor-Hybrido Genetic Heritage, Rust-Resistant Arabica, Mountain Spring Water Processing)',
    'producer': 'Seeds of Life / Oxfam Australia — Ainaro Specialty Coffee Program',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Ainaro District occupies the southern face of Timor's central mountain range, where the 2,963m summit of Tatamailau (the highest peak in Timor-Leste and all of the Timor island chain) creates an orographic rainfall shadow that concentrates humidity on the upper slopes while the lower valleys experience distinct dry seasons. The Timor-Hybrido — first documented in the Ainaro and Ermera districts in 1927 by Dutch colonial scientists studying coffee leaf rust resistance — is the most genetically significant coffee discovery of the 20th century: a spontaneous interspecific hybrid between Coffea arabica and Coffea canephora (Robusta) that occurred naturally in Timor's forest gardens when the two species grown in close proximity produced a fertile cross. The Timor-Hybrido's genes have been introduced into the CLR-resistant varieties now grown in Central America (Catimor, Sarchimor), Colombia (Castillo, Colombia variety), and Ethiopia's breeding programs, making it the genetic ancestor of the majority of disease-resistant Arabica cultivated globally. Growing this variety in its original Ainaro highland terroir — on volcanic soils, in forest-garden conditions, at 1,300-1,700m — produces a coffee that is both a taste and a genetic record of one of the most important agricultural events of the 20th century."
    ),
    'production_technique': (
        "Ainaro Timor-Hybrido is processed using the natural (dry) method at Ainaro: fully ripe red-yellow cherries are hand-sorted and spread on elevated drying beds at the highland dry season temperatures (22-28°C day, 12-15°C night) for 25-35 days. The extended drying in the highland Ainaro climate (lower humidity than the coast) produces a controlled fermentation of the cherry pulp around the bean: slow, even, and non-vinegary due to the dry conditions and cool nights that moderate the fermentation rate. The Timor-Hybrido variety produces slightly more Robusta-like body in the natural process than standard Typica or Bourbon — the hybrid's genetic heritage shows as increased body and chocolate notes compared to pure Arabica natural process. The mountain spring water used in the water flotation sorting before natural process drying adds the distinctive mineral quality of Ainaro's high-altitude aquifer to the initial sorting process. Final moisture controlled to 11-11.5% before milling and export."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Colombia Castillo Variety (Timor-Hybrido genetic descendant, CLR-resistant)',
            'connection': "Ainaro Timor-Hybrido and Colombia Castillo are parent and progeny in the global coffee breeding program — the Castillo variety (Colombia's dominant CLR-resistant Arabica) was developed by the Colombian Cenicafé using Timor-Hybrido genes crossed with Colombian Caturra; drinking Ainaro natural-process Timor-Hybrido alongside a Castillo lot demonstrates how the same genetic heritage expresses differently in equatorial Pacific volcanic highland versus South American Andean terroir"
        },
        {
            'tradition': 'Ethiopia Heirloom Varieties (wild genetic diversity, forest-garden, minimal intervention)',
            'connection': "Ainaro Timor-Hybrido and Ethiopia's uncatalogued heirloom varieties represent the two poles of the Arabica genetic diversity spectrum — Ethiopia as the origin of pure-species genetic diversity, Timor as the only location on Earth where Arabica and Robusta crossed naturally to produce a fertile hybrid; both are irreplaceable genetic resources for the global coffee industry and both produce coffees of distinctive terroir character when grown in their original forest-garden habitats"
        }
    ],
    'sensory_profile': {
        'appearance': 'Green bean: larger than standard Arabica (the Robusta genetic heritage shows in bean size); roasted at medium-light: dark brown with mahogany tints; brewed: dark amber-brown',
        'nose': 'Natural process fruit-forward with the distinctive Timor hybrid body: dark berry (blackcurrant, dark plum), fermented tropical fruit, dark chocolate, earthy volcanic mineral, slight floral lift — the hybrid character shows as a deeper, earthier backdrop to the natural-process fruit than pure Arabica natural process',
        'palate': 'Full body (the most distinctive characteristic — fuller than any pure Arabica natural process at this altitude due to the Robusta genetic heritage); fruit-forward entry (dark berry, dried plum); chocolate and earth mid-palate; long finish with mild bitterness and mineral persistence; the body-acidity balance is unique to Timor-Hybrido and irreproducible in other origins',
        'conclusion': 'Genetically significant and terroir-distinct; the fullest-bodied natural-process Arabica in the PCT collection; the Timor-Hybrido genetic heritage is literally unique on Earth; quality at SCA 86-88 for Ainaro specialty lots'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Ainaro Timor-Hybrido Washed',
            'criteria': 'Washed process Timor-Hybrido showing the genetic body without the natural-process fruit complexity; the commercial reference point for the variety character'
        },
        {
            'tier': 2,
            'tier_name': 'Ainaro Honey Process Timor-Hybrido',
            'criteria': 'Partial natural processing (mucilage retained on bean during drying); intermediate between washed clarity and natural richness; SCA 84-86'
        },
        {
            'tier': 3,
            'tier_name': 'Ainaro Full Natural Timor-Hybrido',
            'criteria': 'The benchmark expression: full natural-process at highland altitude with the Timor-Hybrido genetic body-fruit-earth combination; SCA 86-88; available from Seeds of Life and specialty exporters'
        },
        {
            'tier': 4,
            'tier_name': 'Competition Grade Tatamailau Natural (above 1700m)',
            'criteria': 'Highest-elevation natural-process lots from the slopes of Tatamailau; SCA 88+; essentially unavailable outside specialty auction; the precision tier of Timor-Leste specialty coffee'
        }
    ],
    'service_intelligence': {
        'temperature': 'Brew at 90-92°C — lower than standard for the natural process to avoid over-extraction of the fuller body; the Robusta heritage means this coffee extracts faster than pure Arabica',
        'vessel': 'French press or AeroPress to honor the full body; pour-over works but should use a longer bloom time to compensate for the denser bean structure of the hybrid variety',
        'programme_position': 'Post-dinner coffee as the conversation-starter origin; the Timor-Hybrido genetic story (the most important coffee variety discovered in the last century) is the coffee equivalent of serving a wine from a historic pre-phylloxera vineyard — it requires the sommelier to explain the context for the diner to fully appreciate what they are experiencing'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'CCT / Seeds of Life Ainaro program — the benchmark; specialty roasters such as Onyx Coffee Lab and Intelligentsia have featured Timor-Leste natural-process lots; Equal Exchange for volume fair trade access',
        'north_america_access': 'Growing specialty availability as Timor-Leste gains recognition; Equal Exchange (US) widely distributed; Ethical Bean (Vancouver) occasional lots; specialty coffee subscription services (Trade, Mistobox) occasionally feature Timor single origins',
        'culinary_application': "The Timor-Leste coffee narrative is unique in the PCT for its combination of political significance (occupation, independence), genetic significance (Timor-Hybrido), and practical accessibility (Equal Exchange in every natural food store) — it is the most accessible PCT origin for mainstream restaurant programming while still having depth for specialist engagement"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
