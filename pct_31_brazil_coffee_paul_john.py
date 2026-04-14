import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='Brazil — Sul de Minas (Carmo de Minas, Sitio Santa Ines, Classical Terroir)',
    output_dir='.',
    starting_entry=1,
    session_number=32,
    running_total=96
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Sítio Santa Inês — Carmo de Minas',
    'location': 'Carmo de Minas, Sul de Minas, Minas Gerais, Brazil',
    'description': 'The Paulo Sílvia family farm that produced the 2006 World Barista Championship winning coffee — a moment that placed Brazilian specialty coffee on the global stage for the first time. Sítio Santa Inês is a 42-hectare farm at 1,150–1,250m elevation in Carmo de Minas municipality — the southern Minas Gerais town that is Brazil\'s highest-concentration specialty coffee production zone. The farm maintains heritage Bourbon Amarelo (Yellow Bourbon) variety trees alongside newer specialty varieties, producing naturals and pulped naturals at exceptional quality levels. The farm is certified by the Rainforest Alliance and operates under a carbon-reduction program. Sítio Santa Inês is the most internationally recognized Brazilian single-farm coffee producer and the origin that defined what "world-class Brazilian coffee" means for the specialty trade.',
    'founded': 'Family farming 1930s; specialty production recognized 2006',
    'region': 'Carmo de Minas, Sul de Minas, Minas Gerais, Brazil',
    'website': None,
    'verified': True
})

session.add_producer({
    'tradition': 'coffee',
    'name': 'Fazenda Ambiental Fortaleza (FAF) — Mococa, Sul de Minas',
    'location': 'Mococa, Minas Gerais, Brazil',
    'description': 'Fazenda Ambiental Fortaleza is an 800-hectare Sul de Minas estate producing exceptionally clean, fruit-forward specialty coffees at 900–1,200m elevation in Mococa municipality. FAF is notable for its environmental restoration program — 200+ hectares of the original farm have been restored to Atlantic Forest — and for developing innovative processing methods that extend the natural and anaerobic fermentation techniques that transformed Brazilian specialty coffee\'s reputation from reliable-but-plain to genuinely complex and distinctive. Their Yellow Bourbon natural process and their honey-process expressions have won multiple Cup of Excellence awards.',
    'founded': '1980s; specialty processing from 2008',
    'region': 'Mococa, Minas Gerais, Brazil',
    'website': 'fafcoffees.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Intelligentsia Coffee — Brazilian Origins (US) / 49th Parallel Coffee (Canada)',
    'type': 'roaster_importer',
    'description': 'Intelligentsia Coffee (Chicago/Los Angeles) pioneered direct trade relationships with Brazilian specialty farms including Sítio Santa Inês, establishing the premium Brazilian single-origin market in North America. In Canada, 49th Parallel Coffee (Vancouver) has been a consistent source of Carmo de Minas Sul de Minas coffees for the Canadian Pacific Northwest market.',
    'markets_served': ['US', 'Canada'],
    'traditions_carried': ['coffee'],
    'website': 'intelligentsiacoffee.com',
    'verified': True
})

session.add_beverage({
    'name': 'Brazil Sul de Minas Yellow Bourbon Natural — Carmo de Minas 1,200m, Sítio Santa Inês Heritage',
    'category': 'coffee',
    'subcategory': 'natural_process',
    'origin': 'Brazil',
    'region': 'Sul de Minas, Minas Gerais, Brazil',
    'producer': 'Sítio Santa Inês — Carmo de Minas',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Carmo de Minas sits in the southern Minas Gerais highlands at approximately 1,100–1,300m elevation — the highest and coolest production zone in Sul de Minas, and consequently the zone producing the most nuanced, complex Bourbon variety coffees in Brazil. The terroir of Sul de Minas is defined by three geological factors: weathered Precambrian granite and gneiss-derived red latosol soils with naturally acidic pH (5.0–5.8), excellent drainage from the highland topography, and the consistent cloud and mist cover from the Serra da Mantiqueira mountain range to the east (the same mountains that create Espírito Santo\'s Conillon growing conditions further north, in a different climate zone). Annual rainfall of 1,400–1,800mm arrives in a single wet season (October–March), allowing a dry harvest period (May–September) critical for natural and pulped-natural processing where the whole cherry must dry without excessive moisture. The Yellow Bourbon (Bourbon Amarelo) variety cultivated at Sítio Santa Inês is a Brazilian mutation of the Red Bourbon variety — the yellow fruit characteristic signals a different lycopene-to-xanthophyll ratio in the ripe cherry that correlates with slightly higher sucrose content and a softer, less tannic cup character than red Bourbon at comparable sugar levels. The combination of altitude cooling (slow maturation), granite-latosol mineral absorption, and Yellow Bourbon\'s natural sugar expression creates the multilayer cup complexity that distinguished the 2006 WBC-winning coffee from all previous Brazilian entries.'
    ),
    'production_technique': (
        'Sítio Santa Inês harvests Yellow Bourbon by selective hand-picking (colheita seletiva) — the most labor-intensive Brazilian harvest method, where pickers make multiple passes through each tree section selecting only ripe yellow cherries while leaving green and overripe cherries for subsequent passes. Natural (dry) processing: whole ripe cherries are spread on raised cement terraces (terreiros) at the farm, turned every 2–4 hours during peak sun hours to ensure even drying, and dried for 20–30 days until the cherry moisture content reaches 11–12%. The extended natural drying at high altitude (cooler temperatures slow drying, allowing longer fermentation within the fruit) enables the development of the fruit-forward natural process character — the cherry mucilage and fruit flesh have extended contact with the parchment and seed during drying, transferring complex sugars and fruit acids that produce the distinctive berry-fruit and chocolate character of premium Brazilian naturals. Quality control: every batch is cupped by the farm\'s own Q-grader (the Paulo Sílvia family has trained Q-graders on-site) against a 86-point minimum standard for specialty designation. Lots that cup above 90 points are separated for direct export to the specialty trade through Intelligentsia and similar direct-trade roasters; 87–89 point lots are sold through the Brazil specialty export market at premium commodity prices.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Ethiopia Yirgacheffe Natural (African natural process, fruit-forward)',
            'connection': 'Both Sul de Minas Yellow Bourbon Natural and Yirgacheffe Natural represent the gold standard of natural process coffee from their respective continents — both achieve the balance between fruit-forward intensity and clean cup character that distinguishes premium naturals from fermented, uncontrolled naturals; the Brazil expression is chocolate-caramel with berry accent while Yirgacheffe is blueberry-citrus, demonstrating how the same process produces different results from different varieties and terroir'
        },
        {
            'tradition': 'Colombia Huila Washed (opposite processing philosophy, complementary quality)',
            'connection': 'Sul de Minas Yellow Bourbon Natural and Colombia Huila Washed represent the definitive New World coffee contrast: Brazilian natural achieves complexity through extended fruit contact and drying, Colombian washed achieves clarity through immediate depulping and fermentation tank removal of fruit — both producing 90+ point coffees but through opposite processing philosophies, ideal as a side-by-side tasting to understand how process shapes cup character'
        },
        {
            'tradition': 'Douro Valley Port Wine (same latitude, same heritage narrative)',
            'connection': 'Brazilian Sul de Minas coffee and Douro Valley Port share the same Portuguese colonial agricultural heritage: both were introduced and developed as commercial agricultural products under Portuguese colonial administration, both are now among their respective category\'s global benchmarks, and both express the volcanic-to-granite mineral terroir character of their specific Portuguese-colonial-era agricultural landscapes'
        }
    ],
    'sensory_profile': {
        'appearance': 'Dark caramel to mahogany brown brew; natural process translucence slightly lower than washed; medium-full body visible in the cup\'s surface texture; crema in espresso preparation is richly colored and persistent',
        'nose': 'Ripe tropical fruit (peach, guava), dried cherry, dark chocolate, caramel, very faint wine-grape fermentation undertone from natural processing — the nose is fruity and inviting without the funky fermented note of lower-quality naturals; at espresso extraction: intensified chocolate and caramel with berry top note',
        'palate': 'Full body, low acidity (characteristic of Brazilian altitude naturals), chocolate mid-palate, ripe fruit sweetness from the extended cherry drying, long finish with caramel and dried fruit persistence — the World Barista Championship character: clean enough to show every aromatic layer while complex enough to provide depth across multiple cups'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Brazil Sul de Minas Commercial Grade',
            'criteria': 'Strip-picked or mechanical harvested, dry natural process at high volumes with less turning, 84–86 point range — the standard Brazilian specialty baseline widely available through commercial roasters'
        },
        {
            'tier': 2,
            'tier_name': 'Sul de Minas Direct Trade (87–89 points)',
            'criteria': 'Selective pick, raised-bed or managed terrace drying, cupper-verified 87–89 points — the accessible specialty tier available from direct-trade roasters like 49th Parallel in Vancouver'
        },
        {
            'tier': 3,
            'tier_name': 'Sítio Santa Inês Yellow Bourbon Natural (90+ points)',
            'criteria': 'The 2006 WBC benchmark tier: full selective harvest, controlled natural process, Q-grader cupped 90+, direct export through specialty trade — the internationally recognized pinnacle of Sul de Minas natural-process expression'
        },
        {
            'tier': 4,
            'tier_name': 'Cup of Excellence Lot (91–94 points)',
            'criteria': 'Brazil COE auction lots from Carmo de Minas zone, submitted to international jury cupping, achieving 91+ points — available through online auction to direct roasters globally; the collector tier of Brazilian specialty coffee'
        }
    ],
    'service_intelligence': {
        'temperature': 'Filter: 94–95°C pour-over (V60 or Kalita Wave optimal for natural process body); Espresso: 92–93°C extraction; serve filter at 70°C, allow to cool to 55–60°C before final assessment — the natural process complexity reveals itself more at lower drinking temperature',
        'vessel': 'Wide ceramic cup or Fellow Stagg pour-over mug for filter to maintain heat and concentrate aromatics; standard espresso demitasse for espresso; avoid glass cups which cool too rapidly for natural-process body appreciation',
        'roast_profile': 'Sul de Minas Yellow Bourbon Natural peaks at medium roast (City+ to Full City): light roast emphasizes green fruit acidity at the expense of the characteristic chocolate-caramel depth; dark roast destroys the fruit character entirely; the medium-roast sweet spot produces the chocolate-fruit integration that defines great Brazilian natural expression'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Sítio Santa Inês (Paulo Sílvia family) — Carmo de Minas — the international benchmark for Sul de Minas natural-process Yellow Bourbon',
        'north_america_access': 'Intelligentsia Coffee (US); 49th Parallel Coffee (Vancouver, BC) — the primary PNW source for premium Sul de Minas lots; Hatch Coffee Roasters (Victoria, BC) also sources Sul de Minas directly',
        'culinary_application': 'Yellow Bourbon natural process espresso creates a distinctive dessert sauce base: espresso reduction with chocolate and caramel notes for churros dipping; filter coffee cold-brew concentrate works in Brazilian-inspired chocolate cake glazes; the PCT Portuguese colonial narrative connects Sul de Minas coffee to the same agricultural legacy as Goa cashew feni, Cape Verde grogue, and São Tomé cacao — all products of the same colonial agricultural transfer system'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('spirits', 'India — Goa (Paul John Whisky, Indian Single Malt, Portuguese Colonial Distillation Heritage)')

session.add_producer({
    'tradition': 'spirits',
    'name': 'John Distilleries — Paul John Single Malt',
    'location': 'Cuncolim, South Goa, India',
    'description': 'Paul John Single Malt is produced by John Distilleries at their Cuncolim distillery in South Goa — the same Portuguese colonial territory where cashew feni and coconut feni have been produced since the 16th century. John Distilleries was founded by Paul P. John in 1996, establishing an Indian single malt program at the same time that other global producers were beginning to recognize that tropical aging could produce exceptional whisky in dramatically shorter timeframes than Scottish aging. The Paul John distillery uses 100% Indian six-row barley malted at Crisp Malt (UK) and distilled in copper pot stills at Cuncolim, then aged in ex-bourbon American oak and virgin American oak casks in the Goan tropical warehouse. The tropical aging in Goa — where ambient temperature stays between 26–36°C year-round — accelerates barrel maturation by approximately 3x compared to Scottish aging conditions, producing whiskies of 5–7 years that show development equivalent to 12–15 year Scotch. Paul John has achieved consistent 90+ point scores from Whisky Advocate and represents the most internationally successful Indian single malt outside of Amrut.',
    'founded': '1996',
    'region': 'South Goa, India',
    'website': 'pauljohnwhisky.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Aspri Spirits (India distributor) / Prestige Imports (US) — Paul John International',
    'type': 'importer',
    'description': 'Paul John is distributed internationally through a network including Prestige Imports (US), Specialty Drinks Ltd (UK), and Select Wines (Canada). The Brilliance, Edited, Bold, and Peated expressions form the core international range, with the Mithuna and Kanya anniversary expressions available through allocation. In BC Canada, Paul John is available through the BCLDB and private import.',
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Australia'],
    'traditions_carried': ['spirits'],
    'website': 'pauljohnwhisky.com',
    'verified': True
})

session.add_beverage({
    'name': 'Paul John Brilliance Indian Single Malt — South Goa Tropical Aged, Portuguese Colonial Distillation Heritage',
    'category': 'spirits',
    'subcategory': 'whisky_single_malt',
    'origin': 'India',
    'region': 'South Goa, India',
    'producer': 'John Distilleries — Paul John Single Malt',
    'alcohol_content': 46.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'South Goa\'s Cuncolim distillery sits within the Portuguese colonial territory that Portugal administered from 1510 to 1961 — 451 years of Lusophone governance that established the copper alembic distillation tradition in Goa through cashew and coconut feni production. The PCT connection for Paul John is direct: the distillation technology brought to Goa by Portuguese colonizers in the 16th century — copper pot stills, double distillation methodology, cold-water condensing coils — is the same technical lineage that Paul P. John applied when establishing his single malt program in 1996. He purchased copper pot stills that are direct descendants of the Portuguese bhaati (alembic) technology, made by Indian coppersmith families who had maintained the craft since the colonial era. The Goan tropical climate — year-round warmth (26–36°C), significant humidity (70–85% RH in the monsoon, 55–70% in dry season), and the specific sea air influence from the Arabian Sea coast 30km west of Cuncolim — creates an aging environment that has no direct parallel in traditional whisky-producing regions. The tropical heat drives accelerated barrel breathing: in a single Goa summer (April–June, 36°C+), a Paul John cask absorbs and releases wood compounds at a rate that would take 3–4 years of Scottish cellar aging. The annual angel\'s share in Goa is 8–12% compared to Scotland\'s 1.5–2%, meaning that a 5-year-aged Paul John cask has the equivalent of 25–35 extraction cycles compared to a 5-year Scottish cask — explaining why Paul John at 5 years shows development that takes Scotch 15+ years to achieve.'
    ),
    'production_technique': (
        'Paul John\'s single malt production uses 100% Himalayan six-row barley (sourced from Rajasthan and Haryana, malted in India with the same floor malting techniques used in Scottish maltings). The mash is prepared in a traditional mash tun, fermented for 72–96 hours in stainless steel fermenters with a proprietary Indian Saccharomyces cerevisiae strain — a longer fermentation than standard Scotch production, which Paul John\'s team argues develops more ester complexity appropriate for tropical aging. Double distillation occurs in copper pot stills (wash still and spirit still) with the distiller\'s cut taken conservatively — the middle fraction heart is more narrowly defined than most Indian whisky producers to maintain aromatic purity. The new make spirit enters ex-bourbon American white oak barrels and virgin American oak charred barrels at 63–65% for initial aging of 3–5 years in Goa\'s tropical warehouse. The "Brilliance" expression is a vatting of carefully selected casks from the optimal aging window (approximately 5–7 years), vatted and diluted to 46% ABV with Indian spring water. No chill filtration — Paul John\'s no-chill filtration policy preserves the long-chain fatty acids responsible for the whisky\'s natural body and the slight chill haze that would otherwise appear when the whisky is served cold. Non-coloured: no E150 caramel addition. The combination of no-chill filtration and no coloring places Paul John in the same transparency tier as Glenfarclas, Springbank, and other quality-committed Scotch producers.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Amrut Indian Single Malt (Bangalore, same category pioneer)',
            'connection': 'Paul John and Amrut Distilleries are the two founders of the Indian single malt category that Jim Murray gave Amrut Fusion 97 points in 2010 — the same score as Ardbeg — launching the category internationally; Paul John follows Amrut\'s path with its own South Goa tropical aging expression, demonstrating that Indian single malt quality is not a fluke of one distillery but a consistent consequence of tropical aging accelerating wood extraction'
        },
        {
            'tradition': 'Highland Park Single Malt (maritime climate, complex house style)',
            'connection': 'Both Paul John Brilliance and Highland Park 12 Year achieve their complexity from maritime climate influence: Paul John from the Arabian Sea proximity in South Goa, Highland Park from the North Sea and Atlantic exposure on Orkney — both produce single malts with more weight and complexity than their continental counterparts because of sea air influence on cask maturation and on the barley\'s mineral absorption during growing'
        },
        {
            'tradition': 'Cashew Feni GI (same Goa, Portuguese distillation lineage)',
            'connection': 'Paul John single malt and cashew feni share the same South Goa copper pot still heritage — both produced in Portuguese-colonial-era distillation infrastructure, both expressing the Goan terroir through different agricultural substrates (malted barley vs fresh cashew apple juice), and both demonstrating how the PCT\'s technical legacy of copper alembic distillation produced world-class spirits from Goa\'s unique combination of tropical climate and Portuguese craft tradition'
        }
    ],
    'sensory_profile': {
        'appearance': 'Warm gold to deep amber; natural color from tropical ex-bourbon aging without E150 addition; the depth of color at 5–7 years reflects the accelerated tropical barrel extraction; clear and brilliant from no-chill filtration at room temperature',
        'nose': 'Tropical fruit (ripe mango, banana), vanilla from ex-bourbon American oak, coconut from the new American oak component, dried apricot, light spice (cardamom, white pepper) from the Indian barley character, warm aromatic wood — the Goa climate is directly evident in the tropical fruit register that no Scottish whisky achieves at equivalent age',
        'palate': 'Full body from no-chill filtration, tropical fruit mid-palate, oak tannin present but soft from the fast extraction rate, vanilla-caramel backbone, spice finish (cardamom, ginger from Indian barley character), long warm finish — the whisky communicates both its Scottish-heritage production technique and its Indian tropical aging environment simultaneously'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Paul John Edited (Light Peat, Entry)',
            'criteria': 'Lightly peated expression at 46% — the most accessible Paul John for Scotch drinkers; introduces Indian single malt through a familiar peated frame; widely available'
        },
        {
            'tier': 2,
            'tier_name': 'Paul John Brilliance (Unpeated)',
            'criteria': 'The unpeated flagship: pure malt character without peat interference, 46% no-chill filtration, natural color — the benchmark for Indian single malt character and the wine most recommended as a Scotch alternative at equivalent pricing'
        },
        {
            'tier': 3,
            'tier_name': 'Paul John Bold (Heavily Peated)',
            'criteria': 'Heavily peated Indian single malt using Scottish-peated malt at 55–60 ppm phenols, aged in Goa — produces a dramatically different tropical-peat intersection; the only whisky combining Islay-level peat with tropical aging'
        },
        {
            'tier': 4,
            'tier_name': 'Paul John Mithuna / Kanya Special Releases',
            'criteria': 'Special edition releases at cask strength from individually selected casks in the Paul John library — the connoisseur tier showing the Indian single malt at its maximum complexity; limited allocation through specialist importers'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature to slightly warmed (20–23°C) — the tropical character opens generously at room temperature; no need for the warming in the palm required by more closed Highland whiskies; a few drops of water (5–10ml) on the Bold or higher-strength expressions opens the tropical fruit dramatically',
        'vessel': 'Glencairn or tulip glass; the tropical fruit aromatics of Paul John are fragrant enough that a wide-open wine glass also works well; for cocktail use, highball glass for a whisky and soda application where the tropical fruit character complements ginger beer or light tonic',
        'cultural_context': 'Paul John Brilliance served in the context of a PCT beverage progression — from cashew feni aperitif to coconut feni digestive to Paul John single malt nightcap — tells the 500-year story of Goa\'s Portuguese colonial distillation heritage in a single evening\'s beverage program'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'John Distilleries — Paul John Brilliance and Bold are the international benchmarks for South Goa Indian single malt',
        'north_america_access': 'Paul John through Prestige Imports (US); BCLDB lists Paul John Brilliance and Edited in BC; Select Wines (Canada); Total Wine (US); Whisky Exchange (UK); growing availability in PNW specialty spirits retailers',
        'culinary_application': 'Paul John Brilliance\'s tropical fruit-vanilla character creates natural resonance with PNW Pacific Rim preparations: a single malt Old Fashioned with Paul John and Thai lemongrass bitters; reduction glaze for Malaysian-influenced salmon where the coconut-mango character in the whisky resonates with the coconut milk sauce; the Goa-PCT narrative makes it the ideal whisky for restaurants exploring Portuguese colonial food heritage programs'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
