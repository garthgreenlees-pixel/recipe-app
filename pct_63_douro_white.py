import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Douro Valley (White Wine, Rabigato and Gouveio Varieties, Schist Terraces, Non-Port Table Wine)',
    output_dir='.',
    starting_entry=1,
    session_number=67,
    running_total=0
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Quinta do Crasto — Cima Corgo, Douro Valley',
    'location': 'Gouvinhas, Sabrosa, Cima Corgo, Douro DOC, Portugal',
    'description': (
        'Quinta do Crasto is one of the Douro Valley\'s most historically rooted properties, '
        'documented in title deeds from 1615 and currently operated by the Roquette family. '
        'The estate occupies steep schist terraces above the Douro River in the Cima Corgo '
        '(Middle Douro) sub-zone at elevations of 100–400m, with the characteristic '
        'pre-phylloxera terracing structure that defines the Douro viticultural landscape. '
        'Quinta do Crasto produces both Port and exceptional dry table wines; their '
        'Douro white wine programme features Rabigato and Gouveio from old-vine pre-'
        'phylloxera schist sites that produce the mineral intensity and acid structure '
        'for world-class white wine. The winemaking team, led by Miguel Roquette, '
        'has pioneered the modern Douro white wine style — low-temperature fermentation '
        'in stainless steel, minimal intervention, and emphasis on varietal character '
        'from indigenous varieties over oak imposition.'
    ),
    'founded': '1615 (documented); Roquette family ownership from 1955',
    'region': 'Cima Corgo, Douro DOC, Portugal',
    'website': 'quintadocrasto.pt',
    'verified': True
})

session.add_purveyor({
    'name': 'Signature Wines (UK) / Rare Wine Co (US) / Bacalhôa (PT)',
    'type': 'importer',
    'description': (
        'Quinta do Crasto and leading Douro white wine producers are distributed '
        'internationally through specialist Portuguese wine importers. In North America, '
        'the Rare Wine Co (Sonoma CA) specializes in Douro Valley table wines including '
        'white wine expressions; BCLDB BC and LCBO Ontario carry selected Douro white '
        'wine expressions from Crasto, Niepoort, and Dirk van der Niepoort\'s white '
        'wine programme. The expansion of Douro white wine awareness in North America '
        'is closely linked to the Port wine trade\'s effort to introduce consumers '
        'to the Douro beyond fortified expressions.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Brazil'],
    'traditions_carried': ['wine'],
    'website': 'quintadocrasto.pt',
    'verified': False
})

session.add_beverage({
    'name': (
        'Quinta do Crasto Douro White — Rabigato and Gouveio, '
        'Cima Corgo Schist Terraces, Mineral Dry Table Wine, Non-Port Expression'
    ),
    'category': 'wine',
    'subcategory': 'wine_still',
    'origin': 'Portugal',
    'region': 'Portugal — Douro Valley (White Wine, Rabigato and Gouveio Varieties, Schist Terraces, Non-Port Table Wine)',
    'producer': 'Quinta do Crasto — Cima Corgo, Douro Valley',
    'alcohol_content': 13.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Douro Valley DOC encompasses 250,000 hectares in northeastern Portugal, '
        'following the Douro River from the Spanish border at 600m elevation to '
        'the Cima Corgo sub-zone near Pinhão at 100–500m. The defining geological '
        'character is schist — specifically the Silurian-age metamorphic schist '
        '(xisto) that fractures vertically into thin plates, creating a self-draining '
        'root medium that forces vine roots 10–15m deep to access water and minerals. '
        'The Cima Corgo (Middle Douro) occupies the viticultural quality epicenter '
        'between the cooler, wetter Baixo Corgo (Lower Douro near Peso da Régua) '
        'and the extreme continental climate of the Douro Superior (Upper Douro near '
        'the Spanish border). Cima Corgo temperatures during the growing season '
        'reach 35–40°C daily maximum in July–August, with nights dropping to '
        '18–22°C — a 15–20°C diurnal swing that preserves aromatic compounds '
        'and natural acidity in white varieties despite the extreme daytime heat. '
        'Annual rainfall at Cima Corgo is 550–700mm, concentrated in winter '
        '(October–March) with a pronounced summer drought that creates natural '
        'vine water stress during berry development. The indigenous white varieties '
        'grown for Douro table wine — Rabigato, Gouveio (Verdelho do Douro), '
        'Viosinho, Arinto do Douro, and Codega do Larinho — have co-evolved with '
        'the Douro schist-heat environment over centuries and express terroir '
        'character that imported international varieties cannot replicate in '
        'this demanding geological and climatic setting. Rabigato (the most '
        'planted Douro white variety, literally "cat tail" from its elongated '
        'bunch shape) and Gouveio (the Douro clone of Verdelho, most famous '
        'as a Madeira variety) are the foundation of the finest Douro white '
        'table wines, contributing complementary characters: Rabigato\'s '
        'mineral, firm acidity and stone fruit precision versus Gouveio\'s '
        'fuller body and floral-lemon oil aromatic richness.'
    ),
    'production_technique': (
        'Quinta do Crasto Douro White is produced from estate Rabigato and Gouveio '
        'vines on schist terrace sites at 200–350m elevation in the Cima Corgo, '
        'including old-vine plots with pre-phylloxera root systems (ungrafted '
        'Vitis vinifera on own roots, 50–100 years old). Harvest takes place '
        'late August to mid-September, timed to balance sugar accumulation '
        '(target 12.5–13.5% potential alcohol) with natural acidity retention '
        '(7.0–8.5 g/L total acidity as tartaric) before the extreme late-'
        'September Douro heat further concentrates sugars and reduces acidity. '
        'Handpicking in vineyard-temperature pre-dawn harvesting (starting at 4 AM) '
        'maintains fruit temperature below 20°C; grapes arrive at the winery '
        'in 15–20 kg trays under refrigerated transport. Whole-cluster pneumatic '
        'pressing at maximum 0.6 bar extracts free-run juice only; the pressed '
        'juice is cold-settled at 4–6°C for 24 hours to clarify before '
        'fermentation. Temperature-controlled fermentation at 14–16°C in '
        'stainless steel takes 14–21 days to complete to dry. The premium '
        'Douro white wine expression includes 20–25% partial barrel fermentation '
        'in 500L used French oak tonéis — larger than barriques and previously '
        'used for 3–5 vintages to minimize new oak character — to add '
        'textural complexity without overwhelming the mineral-citrus variety '
        'character. Sur lie aging for 4–6 months with periodic bâtonnage '
        '(lees stirring) contributes the characteristic creamy mid-palate '
        'texture that distinguishes premium Douro white wine from the fresh, '
        'unoaked commercial tier. Malolactic conversion is blocked to preserve '
        'the high natural acidity that gives Douro white wine its structural '
        'longevity and mineral intensity. Total production: approximately '
        '30,000–50,000 bottles of the Crasto white wine estate expression annually.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'White Burgundy Chassagne-Montrachet (Chardonnay, limestone, sur lie aging)',
            'connection': (
                'Douro white wine and white Burgundy share the winemaking architecture '
                'of partial barrel fermentation, extended sur lie aging with bâtonnage, '
                'and malolactic conversion management as the three technical levers '
                'for building complexity in dry white wine from a warm viticultural '
                'region — Burgundy\'s continental heat in the Côte d\'Or versus '
                'the Douro\'s extreme summer heat on schist. The critical difference '
                'is geological: Burgundy\'s Bathonian limestone and marl gives '
                'Chardonnay its distinctive chalky mineral character; Douro\'s '
                'Silurian schist gives Rabigato and Gouveio their specific '
                'flint-and-apricot mineral register that is as terroir-driven '
                'as any Chassagne Premier Cru but from a completely distinct '
                'geological substrate.'
            )
        },
        {
            'tradition': 'Rhône Valley White (Roussanne-Marsanne, granite and limestone, warm climate)',
            'connection': (
                'Both Douro white wine and Northern Rhône white (Hermitage Blanc, '
                'Crozes-Hermitage Blanc) are produced from indigenous grape varieties '
                '(Rabigato-Gouveio versus Roussanne-Marsanne) in warm continental '
                'climates with extreme summer heat and dramatic diurnal swings, '
                'on hard-rock geological substrates (schist versus granite) that '
                'produce wines of high natural acid and mineral intensity. Both '
                'wine styles were historically overshadowed by their respective '
                'region\'s red wine reputation (Douro red and Port; Hermitage Rouge '
                'and Côte-Rôtie) and both are now recognized as capable of '
                '10–20 year aging trajectories that challenge the white Burgundy '
                'orthodoxy for warm-climate white wine ageability.'
            )
        },
        {
            'tradition': 'Madeira Verdelho dry (Atlantic volcanic, Gouveio heritage variety)',
            'connection': (
                'Douro Gouveio and Madeira Verdelho share direct variety heritage: '
                'Gouveio is the Douro Valley name for the same grape as Madeira\'s '
                'Verdelho, transported from the Douro to Madeira during the '
                'Portuguese colonial era when the Madeira wine trade required '
                'mainland grape varieties for the island\'s viticultural expansion. '
                'The PCT connection is explicit: Madeira Verdelho (in its unfortified, '
                'dry expression) demonstrates the same mineral-lemon oil-stone fruit '
                'aromatic profile as Douro Gouveio, with the volcanic Atlantic '
                'soil character of Madeira (basalt) versus the continental '
                'schist character of the Douro producing two distinct but '
                'variety-related mineral registers.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale gold with pale green tints reflecting the high natural acidity '
            'and low pH typical of well-made Douro white wine; brilliant clarity '
            'after cold stabilization; medium-light intensity from the 13% ABV '
            'and the schist terroir\'s tendency to produce wines of precision '
            'over extraction; the sur lie aging contributing a slight golden '
            'warmth to the otherwise pale-green base color in the estate tier.'
        ),
        'nose': (
            'The Douro schist mineral signature is immediate: flint, wet stone, '
            'and apricot from the Rabigato-Gouveio combination; beneath the '
            'mineral core, citrus blossom and lemon oil from Gouveio\'s '
            'characteristic terpene richness; ripe stone fruit (white peach, '
            'apricot) from the 35–40°C daytime Douro heat tempered by the '
            '18–22°C nights; the partial barrel fermentation contributing '
            'cream and brioche undertones without obscuring the mineral-citrus '
            'primary character; clean and precise, with no reductive or '
            'oxidative off-notes from careful whole-cluster pressing and '
            'temperature-controlled production.'
        ),
        'palate': (
            'Medium body with textural richness from bâtonnage; high natural '
            'acidity (7.0–8.5 g/L) provides the structural backbone for the '
            'wine\'s 5–10 year aging potential; mineral flint-and-citrus through '
            'the mid-palate with the Gouveio full-body character adding weight; '
            'apricot stone-fruit sweetness (phenolic ripeness without residual '
            'sugar) on the finish; long, mineral, clean conclusion; the wine '
            'demonstrates the fundamental quality claim for Douro white wine: '
            'that the schist terroir and indigenous varieties produce white '
            'wine of structural complexity and mineral intensity independent '
            'of the Port wine tradition that has historically dominated '
            'the Douro wine identity internationally.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Douro White (commercial cooperative production)',
            'criteria': (
                'Rabigato-dominant blend from irrigated lower-elevation sites, '
                'stainless steel fermentation without lees contact, early bottling '
                '— fresh, clean, no mineral complexity; the commodity Douro white '
                'wine tier at under EUR 8 retail, primarily for local Portuguese '
                'restaurant house wine consumption.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Douro White DOC Estate (4 months lees)',
            'criteria': (
                'Single-estate Rabigato-Gouveio blend, cold fermentation, 4 months '
                'sur lie without bâtonnage — the competent estate tier with '
                'genuine mineral character from schist terroir but without '
                'the barrel fermentation texture of premium expressions.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Quinta do Crasto / Niepoort Tiara (partial barrel, bâtonnage)',
            'criteria': (
                'Old-vine schist terroir, 20–25% barrel fermentation in used tonéis, '
                '4–6 months bâtonnage, malolactic blocked — the benchmark Douro '
                'white wine at premium tier; mineral, textured, 5–8 year aging '
                'potential; the expression that established Douro white wine\'s '
                'international reputation independent of Port.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Niepoort Tiara Reserva / Crasto White Reserve (old-vine apex)',
            'criteria': (
                'Single-block pre-phylloxera schist vine selection, full barrel '
                'fermentation in large format used tonéis, 8–10 months bâtonnage, '
                'low yield (20–30 hl/ha) — the collector tier for Douro white wine; '
                '10–15 year aging trajectory; the definitive statement of what '
                'Rabigato and Gouveio achieve in the finest old-vine schist '
                'expressions of the Cima Corgo Douro.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Quinta do Crasto Douro White at 10–12°C to preserve the mineral '
            'intensity and high acidity structure — the schist mineral character '
            'and Gouveio terpene richness both need slightly more warmth than '
            'Vinho Verde (8–10°C) to express fully. For older vintages (5+ years), '
            'serve at 12–14°C to allow the developed petrol-and-honey secondary '
            'aromas of aged Gouveio to emerge: the variety develops a Riesling-like '
            'tertiary character in well-made expressions from the best schist sites. '
            '25 minutes in a wine refrigerator from cellar temperature '
            '(16°C) achieves the optimal 10–12°C service window.'
        ),
        'vessel': (
            'White Burgundy or Chardonnay-style glass (larger bowl than a '
            'Riesling glass) to capture the mineral-and-stone-fruit aromatic '
            'complexity; avoid narrow Riesling glasses that concentrate acidity '
            'too aggressively for the Gouveio terpene character; a 150ml pour '
            'for table service. In a PCT Douro programme, contrast the white '
            'wine with Tawny Port served from a sherry copita to demonstrate '
            'the full range of Douro production from dry white table wine '
            'to aged fortified — the same schist terroir expressing through '
            'completely different winemaking traditions within 30km of each other.'
        ),
        'programme_position': (
            'In a PCT Portuguese wine programme: serve Douro white before Dão '
            'Encruzado (cooler highland white) — the Douro white\'s schist '
            'mineral intensity and stone-fruit fullness contrasts with Dão\'s '
            'granite-citrus precision to demonstrate how geology determines '
            'white wine character within 100km in central Portugal.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Quinta do Crasto — Cima Corgo (benchmark for Douro white wine '
            'at premium estate tier); Niepoort Tiara Reserva (the apex '
            'collector expression for Douro white wine from pre-phylloxera '
            'old-vine schist sites); both available internationally through '
            'specialist Portuguese wine importers.'
        ),
        'north_america_access': (
            'Quinta do Crasto available through specialist Portuguese wine '
            'importers in major US markets; BCLDB BC and LCBO Ontario on '
            'request; approximately USD $20–35 for estate white expression. '
            'Niepoort Tiara available through Rare Wine Co (Sonoma) and '
            'specialty importers at USD $35–55. Growing North American '
            'awareness of Douro white wine through Port wine trade events '
            'and sommelier education programmes.'
        ),
        'culinary_application': (
            'Douro white wine\'s high acidity and schist mineral character '
            'pairs with bacalhau (salt cod) preparations — the primary Portuguese '
            'national dish — in a within-country agricultural and culinary '
            'pairing that is the most authentic expression of Douro table wine '
            'in its original context; also pairs with rich river fish (lamprey, '
            'river trout) from the Douro River itself, connecting the wine\'s '
            'terroir origin directly to the river that defines the production landscape.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
