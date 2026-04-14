import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fermented',
    region='Malaysia — Malacca (Peranakan Nyonya Cordials, Bunga Telang Blue Pea, Tamarind Coolers, Portuguese Settlement)',
    output_dir='.',
    starting_entry=1,
    session_number=63,
    running_total=0
)

session.add_producer({
    'tradition': 'fermented',
    'name': 'Kristang Community Producers — Portuguese Settlement (Kampung Portugis), Malacca',
    'location': 'Kampung Portugis (Portuguese Settlement), Ujong Pasir, Malacca City, Malaysia',
    'description': (
        'The Kristang community of Malacca\'s Portuguese Settlement (Kampung Portugis, established '
        '1933 on land allocated by the British colonial government to the descendants of Portuguese '
        'colonizers from the 1511 conquest) maintains a living tradition of Kristang culinary '
        'and beverage culture that blends 16th-century Portuguese techniques with Malay '
        'botanical ingredients. The Settlement sits on the southwestern edge of Malacca City '
        'near the Straits of Malacca, 3km from the A Famosa fortress ruins. Kristang beverage '
        'traditions include Portuguese-Malay hybrid cordials made from local botanical '
        'ingredients introduced through the Portuguese spice trade network: the same cinnamon, '
        'clove, and nutmeg that Portuguese traders carried from the Maluku Islands to Lisbon '
        'are used in Kristang festival drinks alongside Malay ingredients like pandan (Pandanus '
        'amaryllifolius), bunga telang (Clitoria ternatea blue pea flower), and tamarind '
        '(Tamarindus indica). The community numbers approximately 2,000–3,000 individuals '
        'and maintains cultural programming through the Portuguese Square (Medan Portugis) '
        'seafood market and cultural performances, where Kristang food and drink are '
        'served to visitors and community members alike.'
    ),
    'founded': 'Cultural tradition from 1511; Portuguese Settlement formalized 1933',
    'region': 'Malacca, Malaysia',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'fermented',
    'name': 'Nyonya-Peranakan Heritage Households — Jonker Street Corridor, Malacca',
    'location': 'Jonker Street (Jalan Hang Jebat), Malacca City UNESCO World Heritage Site, Malaysia',
    'description': (
        'The Peranakan (Baba-Nyonya) Chinese community of Malacca represents the descendants '
        'of 15th-century Hokkien-Fujian Chinese merchants who settled in Malacca during the '
        'Malacca Sultanate era (1400–1511) and intermarried with local Malay women, creating '
        'a hybrid Chinese-Malay culture. The Nyonya (Peranakan Chinese women) are the primary '
        'custodians of the Peranakan culinary and beverage tradition, which is inseparable from '
        'the Jonker Street heritage precinct — Malacca\'s UNESCO World Heritage-listed historic '
        'district where 17th-century shophouses maintain intact Peranakan domestic traditions. '
        'Nyonya cordial and ceremonial drink preparation uses bunga telang (blue pea flower), '
        'pandan leaf, tamarind water, and fermented fruit preparations — all sourced from '
        'the domestic garden that every traditional Nyonya household maintains. The Peranakan '
        'Museum on Jonker Street documents and preserves these traditions for living community '
        'practice and culinary heritage tourism.'
    ),
    'founded': 'Cultural tradition from ca. 1400s; current UNESCO heritage designation 2008',
    'region': 'Malacca, Malaysia',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Medan Portugis (Portuguese Square) Seafood Market / Jonker Street Heritage Cafes',
    'type': 'cultural_institution',
    'description': (
        'The Portuguese Square (Medan Portugis) operates as the Kristang community\'s '
        'primary public food and beverage service venue — an open-air seafood restaurant '
        'precinct adjacent to the Portuguese Settlement where Kristang drinks including '
        'cinnamon-clove cordials and hybrid Portuguese-Malay beverages are served alongside '
        'devil curry (the most famous Kristang dish). The Jonker Street heritage cafes '
        '(Baba Charlie, Nancy\'s Kitchen, and others) serve Nyonya cordials including '
        'bunga telang and tamarind preparations to culinary tourists within the UNESCO '
        'heritage district. North American access is through Malaysian diaspora communities '
        'in Vancouver BC (Richmond), Toronto, and San Francisco Bay Area where Nyonya '
        'cordial ingredients (dried bunga telang, tamarind blocks, pandan extract) '
        'are available through T&T Supermarket and specialty Southeast Asian grocers.'
    ),
    'markets_served': ['Malaysia', 'Singapore'],
    'traditions_carried': ['fermented'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': (
        'Bunga Telang Cordial — Clitoria ternatea Blue Pea Flower, Nyonya '
        'Peranakan Ceremonial Drink, Malacca Portuguese Settlement Crossroads'
    ),
    'category': 'fermented',
    'subcategory': 'ceremonial_cordial',
    'origin': 'Malaysia',
    'region': 'Malaysia — Malacca (Peranakan Nyonya Cordials, Bunga Telang Blue Pea, Tamarind Coolers, Portuguese Settlement)',
    'producer': 'Nyonya-Peranakan Heritage Households — Jonker Street Corridor, Malacca',
    'alcohol_content': 0.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'Malacca (Melaka) sits at 2.2°N latitude on the southwestern coast of the Malay '
        'Peninsula, directly on the Strait of Malacca — the maritime chokepoint that '
        'Portuguese admiral Afonso de Albuquerque conquered in 1511 specifically to '
        'control the spice trade route between the Maluku Islands and Lisbon. The '
        'Malacca Sultanate (1400–1511) had created a polyglot trading entrepôt at this '
        'location that handled spice trade between Arab, Indian, Chinese, and Malay '
        'merchants, and the Portuguese conquest was driven by the commercial imperative '
        'to insert the Crown of Portugal directly into this trade rather than purchase '
        'through Arab intermediaries. The physical geography of the city is determined '
        'by the Malacca River — the original port of the Sultanate — and the two hills '
        '(Bukit St Paul and Bukit China) that formed the defensive core of the '
        'Portuguese-era A Famosa fortress (1511–1641). The UNESCO World Heritage '
        'designation of Malacca City (2008, together with George Town Penang) '
        'recognized this layered colonial geography: Malay Sultanate, Portuguese '
        'colonial (1511–1641), Dutch colonial (1641–1824), and British colonial '
        '(1824–1957) layers physically present in the surviving built fabric. '
        'The bunga telang (Clitoria ternatea, butterfly pea flower) that defines '
        'Nyonya cordial culture grows throughout the Malacca lowlands as a garden '
        'and domestic-herb plant — a tropical legume vine whose intense anthocyanin '
        'pigment (the same ternatein compound that gives the flower its deep blue '
        'color) is the primary colorant in Nyonya rice dishes, cordials, and '
        'ceremonial drinks. The Kristang Portuguese Settlement at Ujong Pasir, '
        '3km south of the Jonker Street Nyonya heartland, represents a separate '
        'but adjacent cultural tradition that intersects with Nyonya beverage culture '
        'through shared spice sourcing and shared colonial inheritance.'
    ),
    'production_technique': (
        'Nyonya bunga telang cordial is prepared from fresh or dried Clitoria ternatea '
        'flowers steeped in hot water (70–80°C, not boiling) for 5–10 minutes to extract '
        'the anthocyanin ternatein pigment without degrading the color. Fresh petals produce '
        'the deepest indigo-blue color (approximately 100 fresh flowers per liter of water); '
        'dried flowers produce a slightly less intense blue that is shelf-stable. The blue '
        'extract is sweetened with palm sugar (gula melaka) syrup — the dark, fragrant '
        'Sarawak or Malacca palm sugar made from Arenga pinnata or Cocos nucifera sap, '
        'reduced and set in bamboo cylinders — at a ratio of 80–100g palm sugar per liter '
        'of bunga telang extract. The sweetened extract is typically acidulated with fresh '
        'squeezed lime juice (Citrus aurantifolia, the small calamansi lime) or preserved '
        'tamarind water just before service. The acid addition from lime or tamarind '
        'triggers a color change reaction with the anthocyanin pigment: the blue cordial '
        'shifts to violet-purple-pink depending on the quantity of acid added, creating '
        'the visual transformation that makes bunga telang preparations a centerpiece '
        'of Nyonya festive presentation. In the Kristang Portuguese Settlement, a '
        'related tradition uses bunga telang extract as a colorant for caldo verde-'
        'inspired rice preparations and festival drinks that add cinnamon and clove '
        '(from the Portuguese spice trade heritage) to the Nyonya blue-pea base — '
        'the most direct physical intersection of Portuguese colonial spice trade '
        'materials and Peranakan Chinese botanical traditions in a single beverage. '
        'The fermented variant (low-alcohol, 0.5–2% ABV) is made by adding a small '
        'amount of ragi rice starter to the sweetened extract and allowing light '
        'fermentation for 24–36 hours, producing a slightly effervescent, mildly '
        'alcoholic version served at Chinese New Year ancestor ceremonies where '
        'the Peranakan tradition requires a fermented offering distinct from '
        'the non-alcoholic daily cordial.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Hibiscus agua fresca (Mexico, Mesoamerican floral infusion culture)',
            'connection': (
                'Bunga telang cordial and hibiscus agua fresca represent parallel '
                'global traditions of anthocyanin-rich floral infusions used as '
                'primary non-alcoholic cultural beverages: Clitoria ternatea in '
                'Southeast Asian Peranakan culture; Hibiscus sabdariffa in Mexican '
                'and Caribbean agua fresca tradition. Both derive their distinctive '
                'color from anthocyanin pigments (ternatein in bunga telang; '
                'cyanidin and delphinidin in hibiscus), both use sugar sweetening '
                'and citric acid for tartness, and both shift color with pH change '
                '(blue to pink in bunga telang; deep red intensifying with lime '
                'addition in hibiscus). The parallel was independent — '
                'Mesoamerican and Southeast Asian floral beverage traditions '
                'developed without contact — but demonstrates universal human '
                'aesthetic response to pH-sensitive anthocyanin chromatics '
                'across cultures.'
            )
        },
        {
            'tradition': 'Kristang Portuguese-Malay hybrid drinks (Malacca Portuguese Settlement)',
            'connection': (
                'The Kristang community of Malacca\'s Portuguese Settlement and the '
                'Nyonya Peranakan community of Jonker Street represent two distinct '
                'but intersecting beverage traditions within 3km of each other in '
                'UNESCO-listed Malacca City: the Kristang drinks incorporate '
                'Portuguese colonial spice trade materials (cinnamon, clove, nutmeg) '
                'into Malay botanical bases, while the Nyonya cordials use Chinese '
                'herbal aesthetics with Malay botanicals. The bunga telang cordial '
                'with cinnamon variation practiced in both communities is the most '
                'direct intersection — a single beverage carrying Portuguese colonial '
                'spice heritage, Chinese botanical aesthetics, and Malay-indigenous '
                'plant material simultaneously.'
            )
        },
        {
            'tradition': 'Goa feni (Portuguese colonial tropical fermentation, India)',
            'connection': (
                'Both Malacca Nyonya cordial culture and Goa feni production represent '
                'the peripheral edges of the Portuguese Colonial Trade network where '
                'European colonial botanical knowledge intersected with indigenous '
                'tropical fermentation and botanical traditions. Goa feni distills '
                'coconut sap within the Portuguese colonial territory; Malacca\'s '
                'Nyonya and Kristang traditions use the spice trade\'s cinnamon and '
                'clove within the post-Portuguese Malacca multicultural heritage. '
                'Both traditions survive in UNESCO heritage-recognized locations '
                '(Goa\'s World Heritage Fort and Velha Goa churches; Malacca\'s '
                'UNESCO City) and both are the primary beverage heritage expression '
                'of the Portuguese colonial presence in their respective territories.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Fresh preparation: intense indigo-blue, clear and brilliant, the most '
            'visually striking of all natural botanical beverages; with lime acid '
            'addition: dramatic shift to violet-purple or pink-magenta depending '
            'on quantity of acid — the color transformation is the defining visual '
            'event of Nyonya cordial service; in fermented variant: slight turbidity '
            'from yeast activity; color depth comparable to blueberry juice without '
            'the cloudiness of fruit-based beverages.'
        ),
        'nose': (
            'Delicate floral-vegetal aroma from Clitoria ternatea extract — subtle '
            'green pea and mild floral character without the intense perfume of '
            'rose or jasmine; palm sugar gula melaka adds caramel and coconut '
            'aromatic depth; calamansi lime addition introduces sharp citrus '
            'zest; cinnamon variant adds warm spice; the aromatic profile is '
            'restrained compared to the dramatic visual presentation — the '
            'bunga telang cordial performs visually more than aromatically, '
            'with the flavor experience delivering gently sweet-tart-floral rather '
            'than complex multi-layered intensity.'
        ),
        'palate': (
            'Light body; sweetness from palm sugar (80–100g/L) balanced by calamansi '
            'lime tartness; the ternatein anthocyanin contributes a mild astringency '
            'similar to weak green tea on the finish; palm sugar caramel depth '
            'distinguishes it from simple sugar syrup; the fermented variant '
            'adds a gentle lactic fizz and mild yeast character; the cinnamon-clove '
            'Kristang variant adds Portuguese colonial spice warmth to the '
            'sweet-floral-tart Nyonya base; clean finish, medium length.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Tourist Version',
            'criteria': (
                'Pre-made bunga telang syrup with artificial blue food coloring '
                'supplement, white sugar rather than gula melaka, bottled lime juice '
                'rather than fresh calamansi — sold at Jonker Street tourist shops '
                'for easy preparation; lacks gula melaka caramel depth and fresh '
                'lime brightness.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Heritage Café Standard',
            'criteria': (
                'Genuine Clitoria ternatea extract (fresh or dried flowers), gula '
                'melaka sweetening, fresh calamansi lime — served at Nancy\'s '
                'Kitchen and established Nyonya cafes; authentic but not '
                'ceremonial-grade preparation frequency.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Nyonya Home Ceremonial',
            'criteria': (
                'Grandmother-prepared from garden-grown bunga telang, Sarawak gula '
                'melaka blocks, freshly squeezed calamansi, optional pandan infusion '
                '(Pandanus amaryllifolius) for additional aromatic depth — the '
                'festive register served at Chinese New Year, ancestor ceremonies, '
                'and Peranakan wedding preparations.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Kristang-Nyonya Hybrid Ceremonial (Portuguese Square)',
            'criteria': (
                'The rare fusion preparation produced at major Kristang community '
                'festivals in the Portuguese Settlement — bunga telang base with '
                'cinnamon-clove Portuguese spice addition, gula melaka sweetening, '
                'light calamansi acid, presented in ancestral ceramic vessels — '
                'the beverage that encodes the complete Malacca multicultural '
                'heritage: Chinese-Malay Peranakan botanical culture, Portuguese '
                'colonial spice trade materials, and Malay tropical ingredients '
                'in a single ceremonial preparation at the UNESCO heritage site.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Bunga telang cordial served at 10–14°C to balance the sweet-tart character '
            'and preserve the vivid blue color — warm temperatures accelerate anthocyanin '
            'degradation and color loss within hours; serve chilled from cold storage '
            'with large ice sphere or rocks to maintain temperature without excessive '
            'dilution; the color transformation ritual (adding lime juice to change '
            'blue to purple-pink at tableside) should be performed at service temperature '
            'for maximum visual impact; lime should be fresh and cold, not room-temperature, '
            'to maintain the acid shock concentration that drives the fastest color change.'
        ),
        'vessel': (
            'Clear glass — ideally a transparent cylindrical or straight-sided glass '
            'that maximizes the visibility of the color transformation ritual — is the '
            'only appropriate vessel for bunga telang cordial; the visual performance '
            'of the drink requires clarity and volume for the color shift to register '
            'fully; a 300ml clear tumbler or a 250ml straight-sided cocktail glass '
            'with fresh lime expressed at tableside provides the complete Nyonya '
            'ceremonial service experience; the Kristang Portuguese Settlement '
            'variant may be served in traditional clay cups for heritage '
            'programming at Medan Portugis events.'
        ),
        'programme_position': (
            'In a PCT Malacca / Peranakan heritage programme: serve as the opening '
            'reception drink — the color transformation ritual immediately establishes '
            'the botanical complexity and cultural depth of Malacca\'s heritage; '
            'follow with Kristang festival food (devil curry, debal curry) and '
            'Nyonya kuih before transitioning to the wine and spirits components '
            'of the programme. The non-alcoholic nature makes it suitable as the '
            'welcoming drink for all guests across dietary and religious requirements.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Nancy\'s Kitchen and Nyonya heritage households — Jonker Street, Malacca '
            '(benchmark for authentic Nyonya cordial preparation using gula melaka and '
            'fresh calamansi); Kristang community at Medan Portugis for the '
            'Portuguese-spice variant; both within UNESCO World Heritage precinct.'
        ),
        'north_america_access': (
            'Dried bunga telang flowers available through T&T Supermarket (Vancouver, '
            'Toronto), Ranch 99 (San Francisco, Los Angeles), and online through '
            'Amazon (bulk dried butterfly pea flower tea). Gula melaka palm sugar '
            'blocks available through Southeast Asian grocery importers. Fresh '
            'calamansi lime available seasonally through Asian produce suppliers. '
            'The complete Nyonya cordial preparation is achievable in North American '
            'commercial kitchens with sourced ingredients and creates a high-visual-'
            'impact non-alcoholic option for Malacca heritage beverage programmes.'
        ),
        'culinary_application': (
            'In PCT culinary programming, bunga telang cordial serves as the '
            'non-alcoholic anchor for Malacca heritage menus — the color transformation '
            'from lime juice addition is the single most visually dramatic natural '
            'beverage preparation available to programme designers; the palm sugar '
            'and calamansi base pairs with Nyonya and Kristang seafood preparations; '
            'the fermented variant (0.5–2% ABV with ragi) provides a culturally '
            'authentic low-alcohol option.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
