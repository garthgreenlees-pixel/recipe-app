import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Madeira (Malmsey Malvasia, Sweetest Style, Blandy\'s Reserve, 100-Year Aging Potential)',
    output_dir='.',
    starting_entry=1,
    session_number=31,
    running_total=94
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Blandy\'s Wine Lodge — Madeira Wine Company',
    'location': 'Funchal, Madeira Island, Portugal',
    'description': 'Blandy\'s is the oldest and most historically significant Madeira wine producer still operating under the founding family name. The Blandy family arrived in Madeira in 1811 when Charles Blandy was shipwrecked on the island — a beginning as fortuitous as many of Madeira\'s greatest fortified wines, which were discovered to improve during long sea voyages after barrels were taken onto ships as ballast water replacement. The Blandy family was instrumental in establishing the British merchant community in Funchal that dominated the Madeira wine trade for 200 years. Today Blandy\'s is part of the Madeira Wine Company (MWC), which owns the historic Funchal Wine Lodge where visitors can taste from casks dating back to 1920. The Blandy\'s Malmsey range — from 5 Year Reserve through vintage declarations from 1920 to 1941 — represents the global benchmark for sweet, aged Madeira and some of the longest-lived wines produced anywhere on Earth.',
    'founded': '1811',
    'region': 'Funchal, Madeira Island',
    'website': 'blandys.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Broadbent Selections (US) / The Rare Wine Co. (Premium) — Madeira Specialists',
    'type': 'importer',
    'description': 'Blandy\'s is imported to the US through Broadbent Selections (standard range) and The Rare Wine Co. in partnership with Blandy\'s for their historic vintage releases. In Canada through LCBO (Ontario) and private import for premium expressions. The Rare Wine Co. (Nicasio, CA) is the North American specialist in aged Madeira, distributing both the NV and vintage Blandy\'s range.',
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['wine'],
    'website': 'rarewineco.com',
    'verified': True
})

session.add_beverage({
    'name': 'Blandy\'s Malmsey 10 Year — Madeira Malvasia Dolce, Estufagem Canteiro, Sweetest Madeira Style',
    'category': 'wine',
    'subcategory': 'fortified_sweet',
    'origin': 'Portugal',
    'region': 'Madeira Island, Portugal',
    'producer': 'Blandy\'s Wine Lodge — Madeira Wine Company',
    'alcohol_content': 19.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Malmsey Madeira is produced from the Malvasia grape variety — in Madeira called Malvasia Cândida or simply Malmsey after the English corruption of "Malvasia" used since the 15th century when Venetian traders introduced the grape to the Atlantic islands. In Shakespeare\'s Richard III (1592), the Duke of Clarence is murdered by drowning in a butt of Malmsey wine — evidence that Madeira Malmsey was familiar enough to English audiences as a luxury product to serve as a recognizable literary metaphor 400 years ago. The Malvasia Cândida grape is the rarest of Madeira\'s noble varieties: after the phylloxera and oidium devastation of the 1850s–1880s, Malvasia Cândida vines were nearly eradicated on the island, replaced by the less disease-susceptible Tinta Negra Mole hybrid. The modern revival of authentic Malmsey production requires the small surviving population of Malvasia Cândida vines grown on the warmer south-facing coastal terraces at 200–400m elevation — the lowest elevation Madeira vineyard zone, where the sugar accumulation driven by Atlantic sun exposure and volcanic thermal radiation from the dark basalt walls produces the ultra-ripe character necessary for Malmsey\'s characteristic sweetness of 90–120 g/L residual sugar after fortification. The volcanic basalt and tuff soils of the southern Madeira coast, combined with the ocean proximity, create a saline-mineral context that prevents the extreme sweetness from becoming cloying — the volcanic minerality is the balancing force that preserves freshness across decades of aging.'
    ),
    'production_technique': (
        'Malmsey production begins with late-harvest Malvasia Cândida grapes picked at high sugar levels (23–28 Brix) from south-coast terraces, processed within 24 hours of harvest. After gentle pressing, the must ferments briefly (2–3 days) until the winemaker judges the sugar-alcohol balance for fortification: for Malmsey (the sweetest standard Madeira style), neutral grape spirit is added to arrest fermentation at 95–110 g/L residual sugar, producing a sweet fortified wine at 18–20% ABV. The critical transformation that distinguishes Madeira from all other fortified wines is estufagem — the deliberate heating of the wine. In the canteiro method used for premium Blandy\'s Malmsey, the wine is placed in small (approximately 600-litre) American or French oak casks in lofts (adegas) at the top of the Blandy\'s Wine Lodge building in Funchal, where the subtropical Madeiran sun heats the wine through the roof naturally to 30–45°C over multiple summers. This canteiro estufagem — heating by the sun rather than industrial hot water coils — is gentler and more complex than the industrial estufagem and is the only method used for premium quality Madeira. The heat drives the Maillard reaction, caramelization, and esterification reactions in the wine that create Madeira\'s characteristic rancio flavors (walnut, dried citrus, caramel, toffee). Extended aging in canteiro followed by glass demijohn or old cask storage produces the 10-year, 15-year, 20-year, and vintage Blandy\'s Malmsey expressions. A 10-year reserve blends wines averaging 10 years of age in cask before bottling; vintage Malmsey declarations represent wines from single harvests aged 20+ years. The wine is virtually indestructible once bottled — oxidative stability from the estufagem process means that opened bottles remain drinkable for weeks or months.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Tawny Port 20 Year (oxidative aging, nut-dried fruit character)',
            'connection': 'Blandy\'s Malmsey 10 Year and 20-year Tawny Port occupy the same tasting register of oxidatively aged, fortified sweet wines with nut-caramel-dried fruit character — but Malmsey\'s volcanic island terroir and canteiro heating produce additional layers of volcanic mineral and toffee complexity absent in the cooler, cellar-aged Port tawny style'
        },
        {
            'tradition': 'Vin Santo Toscano (Italian dried grape sweet wine, very long aging)',
            'connection': 'Both Malmsey and Vin Santo represent the "seemingly immortal sweet wine" category that ages in a semi-oxidative environment for decades and produces concentrated dried-fruit, nut, and caramel complexity from the process rather than from primary fruit — both survive accidental exposure to heat and oxygen that would destroy most wines'
        },
        {
            'tradition': 'Oloroso Sherry (oxidative fortified, walnut-caramel character)',
            'connection': 'Malmsey and Oloroso Sherry are the two great sweet-to-semi-sweet oxidative fortified wine traditions from volcanic Atlantic islands (Madeira) and limestone Andalucia — both develop walnut, dried fig, and caramel complexity through long oxidative aging, but Malmsey\'s volcanic origin imparts a saline mineral depth and higher acidity that gives it a more structured, acidic finish than the rounder Oloroso'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep amber-mahogany with green-gold oxidative rim; viscous and rich; the color at 10 years is already remarkably deep from the canteiro heating and oxidative aging; older expressions approach dark treacle in color',
        'nose': 'Sweet and complex: toffee, salted caramel, walnut skin, dried fig, orange marmalade, volcanic mineral smoke in background, dried apricot, coffee toffee at full canteiro development — the nose is dense and rewarding at room temperature; warming the glass in the palm reveals additional dried citrus peel and volcanic sulfur layers',
        'palate': 'Rich medium-full body, the sweetness (90–110 g/L) perfectly balanced by the Malvasia\'s naturally high acidity and the volcanic mineral structure, toffee-caramel core, long oxidative finish with rancio (walnut-rancid) complexity that signals genuine canteiro aging — the acid-sugar balance in great Malmsey is extraordinary: despite 110 g/L sugar it finishes more like a fortified dry wine than a dessert wine due to the volcanic acidity baseline'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Blandy\'s Malmsey 5 Year Reserve',
            'criteria': 'The entry to the Malmsey style: younger wines with fresher fruit character, good sweetness-acid balance, toffee beginning to develop — widely available at accessible premium pricing; the best introduction to the Malmsey style'
        },
        {
            'tier': 2,
            'tier_name': 'Blandy\'s Malmsey 10 Year',
            'criteria': 'The reference expression: 10-year average canteiro aging, full toffee-walnut-dried fruit development, volcanic mineral evident — the benchmark for age-expression Madeira at the accessible super-premium level'
        },
        {
            'tier': 3,
            'tier_name': 'Blandy\'s Malmsey 15 and 20 Year',
            'criteria': 'Extended canteiro and cask aging producing deeper rancio complexity, more pronounced volcanic mineral, longer finish — the specialist tier for serious fortified wine collectors'
        },
        {
            'tier': 4,
            'tier_name': 'Blandy\'s Malmsey Vintage Declarations (1920–1941)',
            'criteria': 'Single-vintage releases from Blandy\'s historic solera and individual cask stocks — wines of 80+ years of age producing some of the most complex and long-lived beverages on Earth; a 1920 Blandy\'s Malmsey opened in 2024 is 104 years old and still improving; priced at auction at $500–$3,000 per bottle depending on condition and vintage'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 16–18°C — slightly warmer than most fortified wines to allow the canteiro-developed aromatic complexity to express fully; the high viscosity benefits from warming in the palm; refrigerating Malmsey masks the volcanic mineral and rancio character',
        'vessel': 'Small tulip glass (80–100ml) to concentrate the complex aromatics; the sweetness and complexity mean small pours (40–60ml) are appropriate; at 10+ years, the wine is best treated like a spirit (25–40ml) and sipped slowly over 20–30 minutes; never serve in a wide-mouthed glass that disperses the dense aromatics',
        'food_pairing_philosophy': 'Malmsey is one of the few wines that matches aged blue cheese without being destroyed by it — the volcanic acidity cuts through Roquefort or Gorgonzola\'s fat while the sweetness resonates with the creamy base; also exceptional with duck liver preparations, Christmas pudding, pecan pie, and any preparation where caramelized sugar meets salt (salted caramel desserts)'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Blandy\'s Wine Lodge — the benchmark 10 Year and Vintage Malmsey expressions; also Barbeito (whose Malvasia produces even drier, more mineral Malmsey expressions) for specialist comparison',
        'north_america_access': 'Broadbent Selections (US standard range); The Rare Wine Co. (US vintage and special releases); LCBO Ontario carries Blandy\'s standard range; private import for 15, 20, and vintage expressions in BC',
        'culinary_application': 'Malmsey as a cooking wine: extraordinary for reduction sauces where the sweet-acid-volcanic balance creates multi-dimensional depth in Portuguese-inspired preparations (caldo verde variation, duck cataplana); as a dessert wine pairing, the volcanic mineral element creates resonance with dark chocolate (the mineral-iron note in cacao mirrors the volcanic mineral in Malmsey); the 100-year aging capacity is a compelling cellar investment narrative for restaurants with multi-year wine programs'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Portugal — Douro (Quinta do Vesúvio Single Quinta Vintage Port, Douro Superior Terroir)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Quinta do Vesúvio',
    'location': 'Douro Superior, Portugal',
    'description': 'Quinta do Vesúvio is the most dramatic single vineyard in the Douro Valley — a 90-hectare estate surrounded on three sides by the Douro River and the tributary Tua, creating an island-like micro-terroir in the Douro Superior at approximately 400–600m elevation. Originally owned by Dona Antónia Adelaide Ferreira (the legendary 19th-century Douro wine empress), acquired by the Symington family in 1989. Quinta do Vesúvio is one of the few Douro estates that produces a declared Vintage Port every single year — rather than the selective declarations typical of the Port trade (roughly 3–4 declarations per decade). The annual declaration is justified by the estate\'s exceptional terroir: the river peninsula topography creates a unique wind tunnel microclimate that prevents the extreme heat and humidity that compromise other Douro Superior estates.',
    'founded': '1827 (Ferreira estate); Symington acquisition 1989',
    'region': 'Douro Superior, Portugal',
    'website': 'quintadovesuvio.com',
    'verified': True
})

session.add_beverage({
    'name': 'Quinta do Vesúvio Vintage Port — River-Peninsula Single Quinta, Annual Declaration, Douro Superior',
    'category': 'wine',
    'subcategory': 'fortified_red',
    'origin': 'Portugal',
    'region': 'Douro Superior, Portugal',
    'producer': 'Quinta do Vesúvio',
    'alcohol_content': 20.5,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Quinta do Vesúvio\'s extraordinary peninsula position — surrounded on three sides by the Douro River and its tributary — creates one of the most distinctive microclimates in the entire Douro demarcated region. The river water surface around the estate moderates temperature extremes: during the extreme Superior summer heat (40–45°C), the river evaporation creates a 3–5°C cooling effect on the estate\'s vineyard surface temperature; during winter frost periods, the river\'s thermal mass prevents the killing frosts that damage interior Superior vineyards. The specific schist geology of the Vesúvio estate is the "xisto argiloso" (argillaceous schist) — a more clay-bearing metamorphic rock than the harder, more mineralized schist of the Cima Corgo, producing a different mineral contribution to the wine: less iron and graphite-mineral in Vesúvio, more saline-clay earthiness. The 90 hectares of vineyards are planted at steep gradients (30–45%) in traditional socalcos (terraced walls of dry-stone schist) — the most labor-intensive configuration in Portuguese viticulture, maintained by a permanent team of 60 workers year-round. The topographic position also creates a wind tunnel effect as the Atlantic-origin cold air descends the Tua valley and meets the rising hot air from the Superior: the resulting wind exposure maintains vine health during the critical post-veraison period (August–September) that is the most disease-prone in the Douro\'s continental heat.'
    ),
    'production_technique': (
        'Quinta do Vesúvio harvests all 90 hectares of vineyards manually over approximately 3–4 weeks in September–October, with the Symington family\'s team overseeing hand selection of the grapes at each picking pass. The field-blend vineyards contain Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca, Tinta Cão, and more than 20 other Douro indigenous varieties co-planted in the traditional mixed planting that Quinta do Vesúvio maintains as a deliberate biodiversity decision. Fermentation occurs in the estate\'s famous open-top stone lagares — large flat granite troughs where foot-treading (pisa) was practiced for the entire estate\'s production. Since 2012, Vesúvio uses "robotic lagares" (autovinification systems that mimic the gentle pressures of foot-treading in a mechanical system) for the majority of production, with traditional foot-treading reserved for the highest-tier selections. Fermentation runs 24–36 hours in the lagares at 26–32°C; fortification with neutral grape spirit arrests fermentation at 80–100 g/L residual sugar. The resulting new vintage Port is aged for 18–24 months in used oak tonéis (600-litre to 2,000-litre) at Vesúvio\'s own lodge before bottling, at which point the vintage Port enters its critical bottle aging period of 15–50+ years. The annual declaration means every year\'s harvest becomes a vintage Port — giving the trade a continuous vintage comparison that reveals how the Douro Superior climate variation expresses itself across time in the same estate.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Pétrus (Pomerol, river terroir influence, annual declarations)',
            'connection': 'Quinta do Vesúvio and Pétrus share a river-adjacent terroir position (Vesúvio surrounded by the Douro/Tua, Pétrus on the Pomerol plateau above the Isle River) and a philosophy of annual declarations that communicate annual vintage variation to collectors — both are river-moderated terroirs producing wines of exceptional concentration from river-thermal influence'
        },
        {
            'tradition': 'Vintage Champagne annual declaration (terroir declaration over house blending)',
            'connection': 'Vesúvio\'s annual declaration of vintage Port parallels the Champagne tradition of annual vintage declarations from exceptional houses — both communicate that quality is not about selecting only exceptional years but about the consistent excellence of a single terroir\'s expression across all years; the philosophy of annual declaration is rare and prestigious in both the Port and Champagne worlds'
        },
        {
            'tradition': 'Barolo Brunate Cru (single-vineyard, annual declaration, 20+ year aging)',
            'connection': 'Both Quinta do Vesúvio Vintage Port and Barolo from named single crus (Brunate, Cerequio, Lazzarito) represent the single-vineyard, annual-declaration, long-aging tier of their respective traditional wine cultures — both are acquired-taste wines requiring patience and investment but delivering extraordinary complexity at 15–30 years of bottle age'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep opaque ruby-purple in youth (10–15 years); developing garnet-brick rim at 20+ years; the Douro Superior concentration produces an almost black central density in the first decade; slow clearing with age reveals the elegance developing in the wine',
        'nose': 'In youth (5–10 years): dark cherry, blackcurrant, chocolate, dense fruit concentration, structured tannin aromatic, faint schist mineral — needs time and decanting to open; at 20 years: dried fruit, leather, iron-mineral, dried rosemary, tobacco, graphite — the full terroir complexity emerges as primary fruit integrates',
        'palate': 'Full-bodied, massive sweet tannin in youth (the 80–100 g/L residual sugar supports the tannin rather than competing with it), dark fruit-chocolate core, very long finish with Superior schist mineral — requires 15+ years of bottle age for tannin integration and 25+ years for full complexity'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Off-Vintage Declarations (cooler years)',
            'criteria': 'Years where the Superior heat produced lower concentration — still excellent vintage Port from the estate\'s consistently high-quality base, but lighter body and shorter aging potential than the outstanding declarations'
        },
        {
            'tier': 2,
            'tier_name': 'Standard Annual Declarations',
            'criteria': 'The majority of Vesúvio annual declarations: full concentration, excellent schist-mineral character, 20–30 year drinking window — represents the consistent benchmark of the estate\'s production philosophy'
        },
        {
            'tier': 3,
            'tier_name': 'Outstanding Vintage Declarations (e.g., 1994, 2000, 2011, 2016, 2017)',
            'criteria': 'Outstanding years where the Superior climate aligned perfectly — exceptional fruit concentration, tannin structure, and aging potential of 40–60 years; Vesúvio 1994 is considered one of the greatest single-quinta vintage Ports produced in the 20th century'
        },
        {
            'tier': 4,
            'tier_name': 'Vesúvio 1994 (historic benchmark)',
            'criteria': 'The definitive Quinta do Vesúvio vintage, widely considered one of the 10 greatest vintage Ports of the 20th century — still actively aging and improving at 30 years; available at auction at $400–$700 per bottle; a benchmark for what single-quinta Douro Superior terroir can achieve at maximum expression'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 18°C — slightly below room temperature — to preserve the freshness of the fruit concentration; younger declarations (under 15 years) benefit from 3–4 hours decanting to soften the massive tannin; mature expressions (25+ years) may show sediment and should be decanted slowly over candlelight',
        'vessel': 'Large Bordeaux glass for younger expressions to allow maximum oxygen contact and tannin softening; older expressions can be served in a slightly smaller glass as the tannin has integrated; never serve in a narrow tulip glass that traps the tannin without allowing it to blow off',
        'cellaring_guidance': 'Quinta do Vesúvio annual declarations need minimum 10 years before showing well; the best vintage years need 20–30 years; the 1994 is potentially a 60–80 year wine; a case purchase of multiple consecutive vintages allows a progressive education in how the Douro Superior terroir and annual climate variation express themselves across time at the same estate'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Quinta do Vesúvio — the definitive single-quinta vintage Port and the Symington family\'s most prestigious single-estate expression',
        'north_america_access': 'Symington Family Estates distribution through Broadbent Selections (US); widely available at premium wine retailers; BC Liquor and LCBO carry current releases; auction houses (Zachys, Hart Davis Hart) carry back-vintages including 1994',
        'culinary_application': 'Vesúvio vintage Port is the premier pairing wine for aged Portuguese hard cheese (queijo da serra, queijo de azeitão) — the tannin-sweet balance cuts through the cheese fat while the schist mineral resonates with the aged milk\'s mineral complexity; in PNW context, pairs with aged Alpine-style cheese from Quebec (Comté-style) and with dark chocolate preparations where the 20+ year tertiary complexity merges with cacao\'s mineral character'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
