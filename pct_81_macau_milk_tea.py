import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='tea',
    region='Macau — Taipa and Coloane (Portuguese Galão Tradition, Macanese Milk Tea, Colonial Café Culture, Tea-Coffee Blend Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=85,
    running_total=0
)

session.add_producer({
    'tradition': 'tea',
    'name': 'Lord Stow\'s Bakery and Historic Macau Café Culture',
    'location': 'Coloane Village and Taipa Old Town, Macau SAR',
    'country': 'Macau (SAR of China)',
    'region': 'Coloane and Taipa, Macau peninsula',
    'key_person': 'Andrew Stow (founder, Lord Stow\'s Bakery — the pastel de nata anchor of Macau colonial café culture)',
    'founded': 'Lord Stow\'s: 1989; Colonial café culture: 17th century Portuguese settlement',
    'production_volume': 'Artisan café tradition — not industrial production',
    'notable_products': [
        'Lord Stow\'s Bakery pastel de nata (the definitive Macau Portuguese egg tart)',
        'Macanese milk tea (cha de leite) service at Café Seac Pai Van and heritage cafés',
        'Galão service at Portuguese pastelerias in Taipa Village',
    ],
    'certifications': [],
    'website': 'lordstow.com',
    'philosophy': (
        'Macau\'s colonial café culture preserves the point of maximum '
        'cultural contact between Portuguese galão and East Asian tea '
        'service traditions — the Macanese milk tea is neither '
        'Portuguese nor Cantonese but a distinct hybrid developed '
        'over four centuries of colonial coexistence between '
        'the Portuguese pasteleria and the Cantonese cha-chaan-teng '
        'tradition at the pivot point of the PCT Indian Ocean trade.'
    ),
    'trail_connection': 'PCT-10 (Macau café culture node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Macanese Milk Tea (Cha de Leite) — Portuguese Galão Heritage, '
        'Cantonese Cha-Chaan-Teng Convergence, Colonial Pasteleria '
        'Service, PCT Macau Café Culture'
    ),
    'tradition': 'tea',
    'sub_tradition': 'milk_tea — colonial hybrid, galão-Cantonese convergence',
    'region': 'Macau — Taipa and Coloane (Portuguese Galão Tradition, Macanese Milk Tea, Colonial Café Culture, Tea-Coffee Blend Heritage)',
    'terroir_origin': (
        'Macau occupies a unique position in the PCT beverage architecture: '
        'it is the only surviving territory where Portuguese colonial '
        'café culture (the galão, the café com leite, the pasteleria '
        'tradition of the metropolitan Portuguese cities) coexisted '
        'continuously with East Asian tea service for more than '
        '450 years. The Portuguese colonised Macau from 1557 as '
        'a trading post on the Pearl River estuary, 60km from '
        'the Guangzhou tea market — the largest tea trading '
        'centre in Asia. For the Portuguese in Macau, the tea '
        'was Cantonese oolong and black tea from the Guangdong '
        'hinterland; the milk was from the small herds of '
        'Macau-kept cattle and goats supplemented by condensed '
        'milk from Portuguese and later British colonial trade; '
        'the sugar came from the Macau traders\' access to '
        'both Portuguese colonial cane sugar (from Brazil, '
        'Cape Verde, São Tomé) and the Fujian rock sugar '
        '(peng tang) of the Cantonese tradition. The galão '
        '— Portugal\'s signature hot drink of espresso topped '
        'with foamed milk in a tall glass (75% foamed milk, '
        '25% espresso) — arrived in Macau through the '
        'Portuguese pasteleria tradition that the colonial '
        'community maintained on the peninsula\'s main '
        'streets. The Macanese milk tea (cha de leite in '
        'Portuguese; naai cha in Cantonese) developed '
        'at the intersection of these traditions: '
        'a strong black tea (typically a blend of '
        'Cantonese black tea with Ceylon for body, '
        'brewed through a cotton-sock strainer to '
        'produce maximum extraction with minimum '
        'bitterness) combined with evaporated or '
        'condensed milk in a proportion closer to '
        'the Portuguese café com leite (equal parts '
        'coffee and heated milk) than to the '
        'British Empire tea-with-milk tradition.'
    ),
    'production_technique': (
        'The preparation of Macanese cha de leite follows a '
        'distinct protocol that differs from both Hong Kong '
        'milk tea and Portuguese galão in specific ways. '
        'The tea base: a blend of three to five Cantonese '
        'and Ceylon black teas (the traditional Macau blend '
        'uses Guangdong Yunwu black tea for body, Ceylon '
        'BOP — broken orange pekoe — for astringency and '
        'brightness, and occasionally a small addition '
        'of Assam for the malty background) is brewed '
        'using the "silk stocking" method (cotton sock '
        'strainer in the traditional Cantonese convention) '
        'at 95°C water temperature for 3–5 minutes '
        'to produce a concentrate of approximately '
        '200ml at 3x normal tea strength. The sock '
        'strainer is the critical technical element: '
        'the cotton fibers trap the fine tea particles '
        'and tannic compounds that would pass through '
        'a paper filter, producing a smooth-bodied '
        'tea base without the astringent harshness '
        'of direct-infusion brewing. The milk component: '
        'Macau tradition uses evaporated full-fat cow\'s '
        'milk (Carnation or equivalent — the same tin '
        'used in Hong Kong and Singapore milk tea) '
        'rather than the fresh steamed and foamed '
        'milk of the Portuguese galão, producing '
        'a richer, more caramelised milk character '
        'from the evaporation-concentration process. '
        'The specific Macau distinction from Hong Kong '
        'milk tea: Macau cafés traditionally add a '
        'single short espresso (25ml) to the tea base '
        'before adding the evaporated milk — a direct '
        'inheritance from the Portuguese coffee culture '
        'that creates the "yuanyang" (half-and-half) '
        'hybrid character, but with the milk tea as '
        'the dominant base rather than the coffee. '
        'This espresso addition (optional — not standard '
        'at all Macau cafés) is the clearest '
        'documentation of the galão-Cantonese milk '
        'tea convergence that defines Macanese café '
        'culture as distinct from both Hong Kong '
        'and Lisbon models. The drink is served '
        'hot in a tall glass (the galão glass shape '
        'preserved) or cold over ice in a '
        'Cantonese-style plastic cup — both '
        'service conventions coexist in modern '
        'Macau cafés depending on the establishment\'s '
        'heritage orientation.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'tea — Hong Kong milk tea (cha-chaan-teng tradition)',
            'beverage': 'Hong Kong Silk Stocking Milk Tea — Cotton Strainer, Ceylon-Cantonese Blend, Cha-Chaan-Teng',
            'connection': (
                'Macanese cha de leite and Hong Kong silk stocking '
                'milk tea are derived from the same Cantonese tea-with-'
                'evaporated-milk base tradition that spread through '
                'the British and Portuguese colonial settlements of '
                'the Pearl River delta simultaneously. The Hong Kong '
                'version (shaped by British colonial tea service '
                'norms and the cha-chaan-teng working-class café '
                'culture of Kowloon and Wan Chai) uses a heavier '
                'Ceylon BOP dominant blend brewed to near-opaque '
                'concentration; the Macanese version is lighter '
                'in tea concentration and frequently includes '
                'the espresso addition from the Portuguese '
                'galão heritage. Both use the cotton sock '
                'strainer as the defining preparation element '
                '— silk stocking in the Hong Kong name, '
                'meia calça (cotton sock) in the Macau '
                'Portuguese vocabulary. The two traditions '
                'have diverged across 60km of Pearl River '
                'estuary into two distinct national '
                'beverage identities despite sharing '
                'the same technological origin in the '
                'same decade of the same colonial era.'
            )
        },
        {
            'tradition': 'tea — Portuguese galão (Lisbon café culture, espresso-foamed milk)',
            'beverage': 'Portuguese Galão — Espresso with Foamed Milk, Tall Glass Service, Lisbon Pasteleria',
            'connection': (
                'The Macanese cha de leite is the direct descendant '
                'of the galão tradition carried by Portuguese colonial '
                'families from metropolitan Lisbon to Macau between '
                'the 17th and 20th centuries — but transformed by '
                'the substitution of Cantonese black tea for coffee '
                'as the caffeinated base, and evaporated milk for '
                'fresh foamed milk as the dairy component. The galão '
                'glass shape, the proportion of milk to caffeinated '
                'base (75% milk / 25% espresso in galão; similar '
                'ratio in cha de leite when milk-forward), and '
                'the service alongside a pastel de nata egg tart '
                '(the Macau egg tart tradition — codified by Andrew '
                'Stow at Lord Stow\'s Bakery in 1989 — is a '
                'direct derivative of the Portuguese pastel de '
                'Belém) are all direct PCT transmissions from '
                'the Lisbon pasteleria tradition. The PCT narrative: '
                'galão in Lisbon → cha de leite in Macau → '
                'adaptation into a Cantonese-Portuguese hybrid '
                'that is now a UNESCO-recognised element of '
                'Macanese intangible cultural heritage.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Warm caramel-tan in the hot milk tea service — '
            'the colour of evaporated milk blended with '
            'strongly brewed black tea concentrate at a '
            '60:40 milk:tea ratio; lighter in tone than '
            'Hong Kong silk stocking milk tea (which uses '
            'a darker, more concentrated brew); the galão '
            'heritage is visible in the lighter colour '
            'and the occasional fine-bubble foam on the '
            'surface from the hot milk contact; served '
            'in the tall galão glass, the drink is '
            'visually distinct from both the opaque '
            'dark Hong Kong milk tea and the layered '
            'Cantonese yuanyang.'
        ),
        'nose': (
            'The aromatic register opens with the evaporated milk '
            'sweetness — the Maillard caramelisation of concentrated '
            'full-fat cow\'s milk (the characteristic "cooked milk" '
            'toffee note of evaporated milk versus the neutral dairy '
            'note of fresh milk); beneath, the tannic-astringent '
            'aromatic of strongly brewed Ceylon BOP black tea '
            '(the lactone and polyphenol aromatic complex that '
            'is distinct from the flower-and-fruity character '
            'of lighter infusion teas); when the espresso '
            'addition is present, the bitter roast aromatic '
            'of the espresso weaves through the milk-tea '
            'complex, producing the characteristic yuanyang '
            'aroma of coffee-and-tea that is unmistakably '
            'Macanese; an underlying caramel sweetness from '
            'the evaporated milk\'s lactose concentration.'
        ),
        'palate': (
            'Medium body from the evaporated milk fat and the '
            'cotton-strainer-filtered tea concentration; the '
            'entry is immediately sweet-creamy from the '
            'evaporated milk, followed by the tannic black '
            'tea astringency at mid-palate; the cotton sock '
            'straining has removed the harsh tannin particles, '
            'leaving a smooth astringency that provides '
            'structure without bitterness; the espresso '
            'element (when present) introduces a roasty '
            'bitter note at the finish that the milk '
            'sweetness resolves to a café-au-lait-style '
            'finish; the finish length is medium '
            '(20–30 seconds) with milk toffee and '
            'black tea tannin in persistence; the '
            'overall balance is richer and less '
            'astringent than Hong Kong milk tea, '
            'reflecting the Macanese tradition\'s '
            'preference for the Portuguese café '
            'com leite proportion of milk over '
            'the Cantonese strong-tea tradition.'
        ),
        'conclusion': (
            'A living record of 450 years of Portuguese-Cantonese '
            'cultural contact in a single glass — the galão '
            'glass shape, the Ceylon tea, the evaporated milk, '
            'and the optional espresso shot each carrying '
            'a different layer of the Macau colonial history.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Cha de leite at historic Macau colonial cafés '
                '(Café Seac Pai Van, Taipa Village pastelerias, '
                'the Pousada de Coloane café) using traditional '
                'cotton-sock straining, hand-selected Guangdong-Ceylon '
                'tea blend, full-fat evaporated milk, and the '
                'espresso addition from the café\'s own espresso machine; '
                'served in the authentic galão glass alongside a '
                'Lord Stow\'s or Margaret\'s pastel de nata; the '
                'cultural experience inseparable from the liquid quality.'
            ),
            'markers': (
                'Cotton-sock straining; evaporated milk; espresso addition; '
                'galão glass; pastel de nata accompaniment; '
                'historic Macau café address.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Cha de leite at contemporary Macau heritage cafés '
                'and the Lord Stow\'s Bakery café (Coloane) that '
                'maintain traditional preparation with cotton sock '
                'straining and evaporated milk, without the espresso '
                'addition — the standard Macau milk tea experience '
                'available to visitors; technically correct preparation '
                'using the traditional method even if the espresso '
                'hybrid element is absent.'
            ),
            'markers': (
                'Cotton-sock straining; evaporated milk; no espresso; '
                'correct tea concentration; galão glass service '
                'optional but preferred.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Commercially produced Macau milk tea at tourist '
                'restaurants and hotel cafés — technically correct '
                'category but without the artisan preparation; '
                'paper-filter brewing rather than cotton sock; '
                'reduced concentration; fresh milk substituted '
                'for evaporated; the milk tea character recognisable '
                'but the historical depth absent.'
            ),
            'markers': (
                'Paper filter; fresh milk optional; lower '
                'tea concentration; hotel or resort context; '
                'no cotton-sock astringency filtering.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic Asian milk tea (bubble tea chains, convenience '
                'stores) at Macau tourist areas using tea powder, '
                'non-dairy creamer, and sugar syrup without any '
                'connection to the galão or Cantonese cha-chaan-teng '
                'traditions — the category name but not the tradition.'
            ),
            'markers': (
                'Tea powder base; non-dairy creamer; sugar syrup; '
                'no artisan preparation; no cultural context.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve hot at 65–70°C in the traditional galão-style '
            'glass for Macanese cha de leite — the specific '
            'service temperature at which the evaporated milk '
            'toffee character and the black tea tannic complex '
            'are in maximum aromatic expression; the drink cools '
            'rapidly in the tall glass and should be consumed '
            'within 10 minutes of service for the ideal '
            'temperature range; for ice service (the Cantonese '
            'iced milk tea variant), pour hot concentrate over '
            'ice in a paper cup or plastic cup, Cantonese-style — '
            'the rapid dilution from the ice produces a lighter, '
            'more refreshing expression that is the standard '
            'Macau summer service convention.'
        ),
        'vessel': (
            'Traditional service: a tall (300ml) clear glass in '
            'the Portuguese galão style — the transparency of '
            'the glass is a deliberate service choice that '
            'shows the caramel-tan colour contrast of the '
            'milk-tea blend to the drinker, connecting '
            'the visual experience to the Portuguese galão '
            'glass tradition; the height of the galão glass '
            '(taller than a British teacup, taller than a '
            'Hong Kong milk tea glass) signals the '
            'Portuguese café cultural heritage. '
            'In a programme context (PCT café culture flight), '
            'present alongside a pastel de nata on the '
            'saucer — the combination of the milk tea '
            'and the egg tart is the definitive '
            'sensory experience of colonial Macau '
            'and should never be separated in a '
            'formal educational setting.'
        ),
        'technique': (
            'Cotton-sock straining for the tea concentrate; '
            'heat milk without boiling; pour tea first, '
            'milk second; espresso addition optional '
            'but historically authentic; '
            'galão glass; pastel de nata always alongside.'
        ),
        'programme_position': (
            'PCT café culture flight: serve alongside Portuguese '
            'galão (Lisbon tradition), Hong Kong silk stocking '
            'milk tea (cha-chaan-teng), and Singapore teh tarik '
            '(pulled milk tea) for a four-glass arc of '
            'colonial café culture from the Portuguese '
            'trade network to the East.'
        ),
        'verbal_presentation': (
            'Macau. Four hundred and fifty years of Portuguese '
            'presence in the Pearl River delta. The galão glass '
            'is Lisbon. The tea is Guangdong. The evaporated '
            'milk is from a can that came by ship. '
            'This glass holds a colonial archive.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Lord Stow\'s Bakery café (Coloane Village, Macau SAR) — '
            'the anchor institution of Macau colonial café culture '
            'since 1989; the pastel de nata from Lord Stow\'s '
            'is the definitive accompaniment to authentic '
            'Macanese cha de leite; Andrew Stow\'s adaptation '
            'of the Portuguese pastel de Belém recipe for the '
            'Macau context created the most replicated '
            'single pastry in East Asia (the Hong Kong-style '
            '"egg tart" industry traces directly to Lord Stow\'s).'
        ),
        'producer_location': 'Coloane Village and Taipa Old Town, Macau SAR',
        'key_person': 'Andrew Stow (founded 1989); the Stow family legacy management',
        'production_volume': 'Artisan café tradition — not applicable',
        'certifications': ['UNESCO Macau Historic Centre — Intangible Cultural Heritage context'],
        'bc_distributor': '[NOT APPLICABLE: Macanese cha de leite is a café-prepared tradition, not a bottled product; for PCT programme context in BC, prepare using cotton-sock straining method with Ceylon BOP/Cantonese blend from local Asian tea specialists]',
        'us_distributor': '[NOT APPLICABLE: same as above]',
        'uk_distributor': '[NOT APPLICABLE: same as above]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Macanese cha de leite is available only as a café-prepared '
            'drink in Macau. The ingredients (Ceylon BOP black tea, '
            'Guangdong black tea, Carnation evaporated milk) are '
            'globally available. Cotton sock straining bags are '
            'available from any Asian café equipment supplier. '
            'For professional programme reproduction outside '
            'Macau, contact Lord Stow\'s Bakery for their '
            'pastel de nata supply (available at Lord Stow\'s '
            'Margaret\'s Café on Taipa for tourist visitors; '
            'wholesale via lordstow.com for large orders). '
            'Lord Stow\'s have authorised retail in Hong Kong '
            'and franchise operations in Japan and Taiwan.'
        )
    },
    'trail_connection': 'PCT-10',
    'trail_note': (
        'Macanese cha de leite is the beverage centrepiece of the '
        'PCT Macau node — the most concentrated physical record '
        'of the Portuguese colonial trade network\'s cultural '
        'legacy in East Asia. The tea is Guangdong (the terminal '
        'port of the ancient tea trade), the milk and the glass '
        'are Lisbon (the metropolitan origin), and the '
        'evaporated milk is the industrial colonial food '
        'technology that connected British tin-processing '
        'industry (Carnation was originally Swiss-American, '
        'adopted into the British colonial supply chain) '
        'into the Portuguese colonial café vocabulary. '
        'This is PCT terroir expressed as a beverage.'
    ),
    'food_pairings': [
        {
            'technique_id': 'MAC-001',
            'dish': 'Pastel de nata (Lord Stow\'s Bakery Macau egg tart — puff pastry, egg custard, caramelised top)',
            'pairing_type': 'complement',
            'rationale': (
                'The definitive within-tradition pairing: '
                'the caramelised custard of the pastel de nata '
                'shares its Maillard aromatic base (caramel, '
                'egg, vanilla) with the evaporated milk '
                'toffee and black tea tannin of the cha '
                'de leite; the pastry\'s buttery richness '
                'is buffered by the tannin of the tea '
                'concentrate while the milk sweetness '
                'echoes the custard sweetness — a '
                '450-year pairing that has never been improved.'
            )
        },
        {
            'technique_id': 'MAC-002',
            'dish': 'Macanese serradura pudding (sawdust pudding — cream, Marie biscuit, condensed milk)',
            'pairing_type': 'bridge',
            'rationale': (
                'The condensed milk and cream base of serradura '
                '(the Macanese adaptation of a Portuguese no-bake '
                'pudding using Marie biscuit crumbs) bridges '
                'to the evaporated milk of the cha de leite '
                'through shared lactose caramelisation — '
                'both are derived from the condensed milk '
                'tradition of the Portuguese colonial larder; '
                'the biscuit tannin in serradura mirrors '
                'the tea tannin in the cha de leite.'
            )
        }
    ],
    'source': 'UNESCO Macau Historic Centre documentation; Lord Stow\'s Bakery records; Macau Government Tourism Office heritage café documentation; João Pina-Cabral Macanese cultural identity research; Catia Miriam Costa PCT food heritage research',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
