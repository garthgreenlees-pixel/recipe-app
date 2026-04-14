import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='coffee',
    region='Cape Verde — Fogo Island (Volcanic Altitude Coffee, Pico do Fogo Slopes, Atlantic Arabica)',
    output_dir='.',
    starting_entry=1,
    session_number=42,
    running_total=0
)

session.add_producer({
    'tradition': 'coffee',
    'name': 'Cooperative Agropecuária do Fogo — Chã das Caldeiras',
    'location': "Chã das Caldeiras, Fogo Island, Cape Verde",
    'description': "Fogo Island's extraordinary coffee grows in the volcanic caldera of Pico do Fogo — an active stratovolcano rising to 2,829m that last erupted in 2014-2015, destroying the primary coffee-growing villages of Portela and Bangaeira. The farming community of Chã das Caldeiras (1,700m elevation inside the caldera) rebuilt after the eruption and resumed coffee cultivation on the fresh volcanic lava fields, producing a coffee of exceptional mineral intensity on the newly deposited mineral-rich basalt. The cooperative operates on approximately 40 hectares inside the caldera at altitudes ranging from 1,600-1,900m — among the highest coffee cultivation sites in Africa.",
    'founded': '2016 (post-eruption reconstitution)',
    'region': 'Fogo Island, Cape Verde',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Baddu Coffee (Cape Verde) / Specialty Import EU',
    'type': 'distributor',
    'description': "Cape Verdean Fogo coffee is distributed primarily through specialty importers in Portugal and the Netherlands. Baddu Coffee (a Cape Verde-based social enterprise) handles export through EU channels. Availability in North America is extremely limited; specialty coffee importers (Onyx, Intelligentsia) occasionally feature Fogo lots. The extraordinary terroir story (eruption, caldera reconstruction) makes this a compelling specialty coffee narrative.",
    'markets_served': ['Portugal', 'Netherlands', 'US'],
    'traditions_carried': ['coffee'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Fogo Island Volcanic Arabica — Chã das Caldeiras Caldera, Active Volcano Terroir, Post-Eruption Rebuild',
    'category': 'coffee',
    'subcategory': 'arabica_single_origin',
    'origin': 'Cape Verde',
    'region': 'Cape Verde — Fogo Island (Volcanic Altitude Coffee, Pico do Fogo Slopes, Atlantic Arabica)',
    'producer': 'Cooperative Agropecuária do Fogo — Chã das Caldeiras',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Fogo Island is the most actively volcanic island in the Cape Verde archipelago and the highest point of any Atlantic island south of the Azores, with Pico do Fogo reaching 2,829m above sea level. The island's dramatic landscape — a single massive stratovolcano surrounded by ocean — creates the exceptional conditions for Arabica coffee cultivation that rival Ethiopia's highland growing zones: altitude above 1,600m inside the volcanic caldera, Atlantic trade wind moisture throughout the year, volcanic mineral soils from the most recent lava flows (2014-15 eruption created entirely new mineral substrate), and consistent cloud cover from the Atlantic providing natural shade. The coffee plants growing on the post-2015 eruption lava fields represent a unique agricultural situation globally: the Arabica varieties are growing in volcanic substrate that is geologically younger than any commercial coffee terroir on Earth, producing a mineral intensity traceable directly to the freshness of the volcanic mineral release rather than the weathered volcanic soils of Ethiopia, Colombia, or Hawaii Kona."
    ),
    'production_technique': (
        "Fogo Arabica is produced from mixed Bourbon and Typica varieties originally introduced by Portuguese colonial settlers in the 18th century, growing at 1,600-1,900m inside the Pico do Fogo caldera. Hand-picking of red-ripe cherries during the harvest season (June-September); processing via both washed (wet) and natural (dry) methods depending on cooperative member preference. The washed Fogo lots show the clearest volcanic mineral expression: cherry, parchment, and mucilage removed by fermentation in water tanks for 24-36 hours, then sun-drying on raised beds inside the caldera for 15-21 days in the high-altitude Atlantic trade wind environment. Natural-process lots (cherries dried with pulp intact) show more fruit-forward, fermented character. Milling removes the parchment layer; the beans are sorted by hand (defect rate extremely low given the artisanal scale). Total annual production is under 30 tonnes — making Fogo Arabica one of the smallest-volume specialty coffee origins in Africa."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Hawaii Kona Arabica (volcanic island, altitude, Pacific trade wind, small-scale)',
            'connection': "Fogo Arabica and Hawaii Kona both represent Atlantic and Pacific volcanic island coffee traditions where Arabica grows at moderate altitude on recent volcanic soils in the trade wind climate belt — both are defined by extraordinary mineral intensity, small production volume, and premium pricing that reflects both the genuine terroir distinction and the physical difficulty of production on active volcanic islands; Kona's legacy in the PCT narrative connects through the Hawaiian-Portuguese agricultural history"
        },
        {
            'tradition': 'Ethiopia Harrar Natural Process (dry-processed, fruit-forward, minimal intervention)',
            'connection': "Fogo natural-process Arabica and Ethiopia Harrar share the category of African Arabica processed with minimal water intervention, allowing extended contact between fruit and bean to develop the fruit-forward, fermented-complex character that distinguishes natural processing from the cleaner mineral expression of washed Arabica — both demonstrate how the same volcanic island or highland terroir produces fundamentally different cup profiles depending on the processing decision"
        }
    ],
    'sensory_profile': {
        'appearance': 'Green bean: dense, sea-green with blue tints indicative of high-density altitude growing; roasted: dark caramel to dark chocolate coloration at medium-light roast levels; brewed: golden-brown with fine reddish tints',
        'nose': 'Washed lot: volcanic mineral (wet stone, petrichor), red cherry, citrus blossom, dark chocolate — the Atlantic island mineral quality is distinctive and not found in Ethiopian or Central American comparators; natural lot: dried fruit (date, raisin), dark berries, cacao, rum-like fermentation character from the volcanic caldera fermentation environment',
        'palate': 'Medium-high acidity (the volcanic mineral acidity is different from Ethiopian citric acidity — more mineral, less fruity); medium body from the Atlantic island altitude; clean finish with volcanic mineral persistence; the extraordinary terroir story is legible in the cup: this does not taste like any other African origin',
        'conclusion': 'Rare and compelling specialty origin of genuine terroir distinction; the post-eruption rebuild narrative adds provenance depth; quality at specialty grade (SCA 87-90 for best lots)'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard Fogo Arabica (mixed lot)',
            'criteria': 'Blended lots from multiple caldera producers without cherry selection; adequate specialty grade (SCA 82-85) without the mineral intensity of selected lots'
        },
        {
            'tier': 2,
            'tier_name': 'Cooperative Select Washed Fogo',
            'criteria': 'Fully washed, selected cherry, raised-bed drying inside caldera (SCA 86-88); the benchmark washed mineral expression of Fogo terroir'
        },
        {
            'tier': 3,
            'tier_name': 'Chã das Caldeiras Natural Post-Eruption Lot',
            'criteria': "Natural-process Fogo from post-2015 lava field soils; fruit-forward with volcanic mineral backbone; SCA 88-90; the 'reconstruction coffee' with the strongest terroir story"
        },
        {
            'tier': 4,
            'tier_name': 'Fogo Microlot Competition Grade',
            'criteria': "Rare competition-grade lots submitted to Cup of Excellence-equivalent competitions; SCA 90+; essentially unavailable outside specialty auction circuits; the highest expression of the caldera's agricultural potential"
        }
    ],
    'service_intelligence': {
        'temperature': 'Brew water at 92-94°C (the high-altitude mineral acidity benefits from slightly lower water temperature than lower-acid African origins to avoid over-extraction of the volcanic mineral sharpness)',
        'vessel': 'Pour-over (V60, Chemex) for the washed lot to emphasize the volcanic mineral clarity; French press or AeroPress for the natural lot to support the fruit-forward fermented character',
        'programme_position': 'Post-dinner coffee course as an alternative to the more familiar Ethiopian or Colombian origins; the terroir story — the most active volcano in the Atlantic, rebuilding after 2014 eruption — provides compelling narrative for a post-dinner coffee presentation alongside traditional Cape Verdean sweets (doce de papaia, pudim de leite)'
    },
    'purveyor_intelligence': {
        'benchmark_producer': "Cooperative Agropecuária do Fogo (Chã das Caldeiras) — only commercial producer of note; Baddu Coffee for the EU export channel",
        'north_america_access': 'Extremely limited; specialty roasters with African sourcing focus (Onyx Coffee Lab, Intelligentsia, Counter Culture) have occasionally featured Fogo lots; the PCT narrative justifies direct sourcing inquiry',
        'culinary_application': 'The Cape Verde coffee narrative connects the PCT story from its beginning (colonial trade routes from Portugal through the Atlantic islands) to the agriculture established by the Portuguese in their island colonies — Fogo coffee, grogue from Santiago, and cane production from the colonial era represent the complete colonial agricultural system in a single island chain'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
