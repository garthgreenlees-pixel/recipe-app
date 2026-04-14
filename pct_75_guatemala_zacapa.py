import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Guatemala — La Finca La Hermosa (Ron Zacapa 23 Sistema Solera, Highland Aging at 2300m, Sugarcane Honey Not Molasses)',
    output_dir='.',
    starting_entry=1,
    session_number=79,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Industrias Licoreras de Guatemala (ILG) — Zacapa, Guatemala',
    'location': 'Zacapa, Guatemala',
    'description': (
        'Ron Zacapa is produced by Industrias Licoreras de Guatemala, '
        'the state-affiliated rum distiller established in 1976 under the '
        'auspices of the Guatemalan government\'s distilling operations. '
        'The Zacapa brand itself was created in 1976, the same year the '
        'distillery was founded, and was named for the Zacapa Department '
        'in eastern Guatemala — a dry, hot, low-lying agricultural region '
        'where the sugarcane for Zacapa production is grown. Despite the '
        'name, Ron Zacapa is aged not in the Zacapa valley but at La Finca '
        'La Hermosa — "The Beautiful Farm" — at 2,300m above sea level '
        'in the Guatemalan highlands near Quetzaltenango, where the '
        'cool mountain air slows the maturation process compared to '
        'sea-level Caribbean aging environments. Industrias Licoreras '
        'de Guatemala is now a majority-owned subsidiary of Diageo '
        '(since 2008), which manages global distribution of the Zacapa '
        'brand. The master blender is Lorena Vásquez, one of the few '
        'female master blenders in the rum industry, who has directed '
        'Zacapa production since the 1990s and is responsible for '
        'the Sistema Solera blending philosophy that defines '
        'the Zacapa Centenario 23 expression.'
    ),
    'founded': '1976',
    'region': 'Zacapa Department / La Finca La Hermosa, Quetzaltenango Highlands, Guatemala',
    'website': 'ronzacapa.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Diageo / Zacapa global distribution',
    'type': 'importer',
    'description': (
        'Ron Zacapa is distributed globally through Diageo\'s international '
        'spirits distribution network. In the United States, Diageo '
        'distributes Zacapa Centenario 23 nationally through fine spirits '
        'retailers at USD $50–70 per 750ml — positioned as an ultra-premium '
        'rum in the Diageo portfolio alongside Johnnie Walker Blue Label '
        'and Don Julio 1942. In Canada, BCLDB BC and LCBO Ontario '
        'carry Zacapa 23 on regular allocation at CAD $70–90 per 750ml. '
        'Zacapa XO (the premium expression with greater average solera '
        'age) is available through specialist fine spirits retailers '
        'at USD $80–100 per 750ml. Zacapa 23 has won multiple awards '
        'at international rum competitions including IWSC and ISC, '
        'and is the most recognized ultra-premium rum brand in the '
        'European and North American markets by international '
        'competition performance.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Global'],
    'traditions_carried': ['spirits'],
    'website': 'ronzacapa.com',
    'verified': True
})

session.add_beverage({
    'name': (
        'Ron Zacapa Centenario 23 Sistema Solera — Guatemala Highland Aged, '
        'Virgen de Caña Sugarcane Honey, 2300m Elevation, Lorena Vásquez'
    ),
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Guatemala',
    'region': 'Guatemala — La Finca La Hermosa (Ron Zacapa 23 Sistema Solera, Highland Aging at 2300m, Sugarcane Honey Not Molasses)',
    'producer': 'Industrias Licoreras de Guatemala (ILG) — Zacapa, Guatemala',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Ron Zacapa\'s raw material and aging environment occupy two '
        'completely different Guatemalan terroirs that together define '
        'the Zacapa character. The sugarcane is grown in the Zacapa '
        'Department — a hot, dry lowland valley at 180–300m above sea '
        'level in eastern Guatemala between the Sierra de las Minas '
        'mountains and the Motagua River, with a semi-arid tropical '
        'climate (800–1,200mm annual rainfall) and volcanic alluvial '
        'soils that concentrate the natural sucrose content of the '
        'Zacapa-region cane at levels above typical molasses-producing '
        'regions. The critical raw material distinction: Zacapa uses '
        '"virgen de caña" — the first-pressed juice concentrate (jugo '
        'de caña concentrado) extracted before the sugar crystallization '
        'and molasses separation process. The virgen de caña retains '
        'the full spectrum of sugarcane flavor compounds that are '
        'stripped or degraded during the industrial molasses production '
        'process; the concentrate is richer in glucose, fructose, and '
        'aromatic precursors than the blackstrap molasses used by '
        'most Caribbean rum producers. The aging takes place entirely '
        'at La Finca La Hermosa at 2,300m elevation in the Guatemalan '
        'highlands near Quetzaltenango — the "House Above the Clouds" '
        'where the temperature ranges from 10–18°C year-round, compared '
        'to 25–32°C in Caribbean sea-level aging environments. The '
        'cool highland air slows the oxidative barrel maturation rate '
        'by approximately 50% compared to Caribbean sea-level conditions, '
        'but the lower atmospheric pressure at altitude means the spirit '
        'penetrates deeper into the wood staves per unit time than at '
        'sea level — the highland aging producing a different flavor '
        'extraction profile (less volatilization, deeper wood penetration) '
        'that explains the characteristic richness and vanilla-caramel '
        'intensity of Zacapa relative to equally aged Caribbean rums.'
    ),
    'production_technique': (
        'The Zacapa production chain begins with the pressing of fresh '
        'Zacapa-region sugarcane to extract virgen de caña (caldo de '
        'caña) — the raw cane juice before any industrial processing. '
        'The fresh juice is immediately concentrated under vacuum to '
        'remove water, producing a dark, viscous syrup of approximately '
        '65–70 Brix (sugar concentration) called jugo de caña concentrado. '
        'This concentrate is not blackstrap molasses (the byproduct of '
        'crystallized sugar extraction) — it is the full-spectrum '
        'cane juice at concentrated form, retaining the maximum '
        'natural flavor compounds from the fresh sugarcane. '
        'The concentrated cane juice is diluted to approximately '
        '25 Brix and inoculated with the ILG house yeast for a '
        '72–96 hour fermentation at 28–32°C, producing a wine '
        'of 7–9% ABV with moderate ester development (higher '
        'than Dominican column-still rum; lower than Jamaican '
        'heavy rum). The fermented cane wine is distilled in '
        'continuous column stills to 95–96% ABV, then diluted '
        'to 65% ABV for barrel entry. The Sistema Solera '
        'at La Finca La Hermosa is organized as a traditional '
        'Spanish solera with four to six aging tiers: the oldest '
        'rum (up to 23 years, which provides the "Centenario 23" '
        'name) in the foundation barrels; the most recently '
        'distilled rum (6 years) in the criadera (nursery) '
        'barrels. Three different cask types are used: American '
        'white oak ex-bourbon barrels (180–200L) for the initial '
        'aging; Pedro Ximénez sherry-seasoned casks for the middle '
        'solera tiers; and ex-Zacapa barrels (previously used '
        'for Zacapa itself) for the final blending phase. '
        'The "23" designation refers to the maximum age of '
        'the oldest rum in the solera blend, not to the '
        'average age — the actual average age of the '
        'Sistema Solera blend in Zacapa 23 is approximately '
        '6–15 years across all solera fractions. Master blender '
        'Lorena Vásquez assesses the solera lots annually and '
        'determines the final blend proportions from the '
        'various aged fractions before bottling at 40% ABV '
        'without chill filtration to preserve the natural '
        'triglycerides and texture from the cane juice base.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Oloroso Sherry Solera VORS (Spanish solera blending, multiple age tiers, cask diversity)',
            'connection': (
                'Ron Zacapa Sistema Solera and Oloroso Sherry VORS share '
                'the fundamental solera blending philosophy: a multi-tier '
                'system of fractional blending from oldest to youngest '
                'that creates a consistent style through the proportional '
                'contribution of different age fractions. Both Zacapa\'s '
                'Sistema Solera and Jerez\'s traditional solera system '
                'use cask diversity (ex-bourbon, sherry-seasoned in '
                'Zacapa; American and European oak criadera and solera '
                'in Jerez) to build complexity through progressive '
                'blending from young to old fractions. The philosophical '
                'parallel is in the rejection of single-vintage thinking: '
                'both traditions hold that the solera blend produces '
                'greater complexity and consistency than any single-vintage '
                'expression from the same production.'
            )
        },
        {
            'tradition': 'Armagnac Bas-Armagnac Highland (French brandy, high-altitude, slow maturation, cane vs. grape)',
            'connection': (
                'Ron Zacapa highland aging at 2,300m and Armagnac production '
                'in the highland zones of Bas-Armagnac share the winemaker\'s '
                'understanding that altitude-driven cool temperatures slow '
                'the maturation rate, producing a more integrated, complex '
                'spirit character than rapid sea-level or valley-floor '
                'aging. At 2,300m, the Guatemalan highland air temperature '
                '(10–18°C year-round) approaches the cool conditions of '
                'French southwest highland zones (10–15°C winter; '
                '20–25°C summer) where Armagnac achieves its distinctive '
                'slow, refined barrel extraction. Both traditions use '
                'the cool highland environment as a deliberate quality '
                'tool — the slower maturation producing depth and '
                'integration that warmer, faster-maturing spirits '
                'cannot replicate regardless of barrel selection.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber-mahogany with red-gold highlights — the rich color '
            'of the Sistema Solera multi-cask blending including the '
            'darkening contribution of PX sherry-seasoned barrels; '
            'darker and more complex in color than single-cask '
            'bourbon-aged rum at equivalent average age; brilliant '
            'clarity; slow, rich legs from the full body of '
            'the virgen de caña base spirit and the 40% ABV; '
            'no added caramel coloring in the premium expression.'
        ),
        'nose': (
            'Rich vanilla and crème brûlée as the immediate opening '
            'aromatic register — the signature of highland-aged rum '
            'from multiple ex-bourbon barrels with deep wood penetration '
            'at 2,300m altitude; beneath the vanilla, dried fruit '
            '(raisin, prune, fig) from the PX sherry cask contribution; '
            'dark chocolate and mocha from the combination of '
            'highland barrel extract and the concentrated cane '
            'honey base — the virgen de caña provides a richer, '
            'more complex background than blackstrap molasses rum '
            'at the same age; honey and caramel from the natural '
            'sugars of the concentrated cane juice; baking spice '
            '(cinnamon, allspice, vanilla pod) from the highland '
            'wood extraction; a subtle floral-fruity register '
            'from the fermentation esters of the virgen de '
            'caña base that is absent in molasses-based rum.'
        ),
        'palate': (
            'Full body and richly textured from the virgen de caña '
            'base and the multi-cask solera complexity — noticeably '
            'more viscous and mouth-coating than molasses-based rum '
            'at equivalent ABV; the vanilla-crème brûlée from the '
            'nose at full intensity through the entry; dried fruit '
            'and dark chocolate from the PX sherry contribution '
            'through the mid-palate; the highland altitude aging '
            'character is apparent in the deep wood extract '
            'integration — the tannin fully polymerized and '
            'contributing structure without harshness; very '
            'long finish (60–90+ seconds) from the combination '
            'of the virgen de caña natural sweetness (no added '
            'sugar in the standard bottling), the solera complexity, '
            'and the highland barrel depth; the warmth of 40% ABV '
            'is clean and round, consistent with the long '
            'highland maturation.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Ron Zacapa Edición Negra (modified solera, darker cask profile)',
            'criteria': (
                'Zacapa Edición Negra uses a modified Sistema Solera '
                'with a higher proportion of sherry and cognac-type casks; '
                'darker, more fruit-forward and spiced than the Centenario 23; '
                'the entry point for the Zacapa premium range in some '
                'markets; lower average solera age than the Centenario 23.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Ron Zacapa Centenario 23 Sistema Solera (benchmark expression)',
            'criteria': (
                'The reference Zacapa expression with Sistema Solera '
                'blending aged 6–23 years at 2,300m La Finca La Hermosa; '
                'the virgen de caña base and the highland altitude aging '
                'at full expression; the benchmark for Guatemalan and '
                'Central American rum in international premium spirits '
                'competition; consistent award winner at IWSC and ISC '
                'since the 1990s.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Ron Zacapa XO (extended solera, cognac cask finish)',
            'criteria': (
                'Zacapa XO uses a Sistema Solera with a greater proportion '
                'of aged fractions (higher average age than Centenario 23) '
                'and adds a cognac Limousin oak finishing stage — producing '
                'a drier, more structured expression with greater barrel '
                'tannin complexity and an additional dried fruit and spice '
                'register from the French oak finishing; priced at '
                'USD $80–100 per 750ml; the connoisseur and collector '
                'tier within the Zacapa range.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Ron Zacapa Royal (ultra-premium, decanter format, highest solera allocation)',
            'criteria': (
                'Zacapa Royal is the apex expression — a limited production '
                'selection of the oldest and finest solera fractions from '
                'La Finca La Hermosa with maximum cask diversity and '
                'Lorena Vásquez\'s personal selection from the archive lots; '
                'the luxury packaging (crystal decanter, leather presentation '
                'box) reflects the collector positioning; pricing '
                'USD $300–500 per decanter; the definitive expression '
                'of the Guatemalan highland rum tradition at its '
                'technical apex.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Ron Zacapa 23 neat at room temperature (20–22°C) '
            'in a spirits glass without ice — the full Sistema Solera '
            'aromatic complexity (vanilla, dried fruit, dark chocolate) '
            'requires room temperature to express completely; the '
            'virgen de caña natural texture and the highland barrel '
            'richness are most perceptible at room temperature '
            'where the high-molecular-weight flavor compounds '
            'are fully volatile; a single large ice sphere (for '
            'the guest who prefers a cooled serve) is acceptable '
            'but should be mentioned as a temperature reduction '
            'that mutes some of the solera aromatic complexity; '
            'do not serve over crushed ice as the rapid dilution '
            'eliminates the highland depth that distinguishes '
            'Zacapa 23 from less complex rum expressions.'
        ),
        'vessel': (
            'Serve in a Glencairn glass or a Copita tulip (100–150ml) '
            'with 45–60ml pour for sipping service; the chimney '
            'aperture of the Glencairn concentrates the vanilla-dried '
            'fruit aromatic register and prevents rapid volatilization '
            'of the high-alcohol aromatic compounds; for a formal '
            'programme presentation, serve alongside the Zacapa '
            '23 bottle showing the palm-leaf hat design — '
            'the distinctive packaging is part of the brand '
            'identity and the palma real (the Guatemalan royal '
            'palm) traditional hat woven around each bottle '
            'is the visual signature of the Zacapa premium '
            'positioning; present with the explanation of '
            'virgen de caña versus molasses, highland '
            'aging at 2,300m, and the Sistema Solera — '
            'the three technical distinctions that explain '
            'why Zacapa 23 occupies a different quality '
            'category from Caribbean molasses-based rum.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Industrias Licoreras de Guatemala — Zacapa/La Finca La Hermosa '
            '(1976; the reference for Guatemalan rum and the benchmark '
            'for the virgen de caña production method in the Americas; '
            'Lorena Vásquez is the defining master blender for the '
            'Sistema Solera philosophy; Zacapa 23 is the entry point '
            'for the high-altitude Central American rum tradition '
            'that is distinct from both Caribbean molasses rum '
            'and South American agricole rhum traditions).'
        ),
        'north_america_access': (
            'Ron Zacapa 23 is distributed through Diageo nationally '
            'in the United States at USD $50–70 per 750ml — the '
            'benchmark price for the ultra-premium Caribbean '
            'and Central American rum tier. In Canada, BCLDB BC '
            'and LCBO Ontario carry Zacapa 23 on regular allocation '
            'at CAD $70–90. Zacapa XO is available through specialist '
            'fine spirits retailers at USD $80–100. For professional '
            'spirits programme buyers, Zacapa 23 is the essential '
            'comparison point for a Central American rum flight '
            'alongside Dominican (Brugal 1888) and Guatemalan '
            'agricole (Guaro) expressions.'
        ),
        'culinary_application': (
            'Ron Zacapa 23 is the premium rum for chocolate dessert '
            'pairing — the virgen de caña natural richness and the '
            'PX sherry solera dried fruit create a direct sensory '
            'bridge to 70–80% single-origin dark chocolate from '
            'Guatemala\'s Lachua region; the Guatemalan cacao '
            'and Guatemalan rum pairing is the definitive '
            'within-region food and spirits pairing of Central '
            'America. In a formal programme context, Zacapa 23 '
            'functions as the dessert spirits course after '
            'a Central American dinner — the vanilla-dark '
            'chocolate-dried fruit character bridging from '
            'the savoury mole negro of the main course '
            'to the cacao dessert of the closing course '
            'in a Guatemala-focused tasting menu.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
