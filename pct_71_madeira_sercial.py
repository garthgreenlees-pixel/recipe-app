import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fortified',
    region='Portugal — Madeira (Sercial Dry, Lowest-Sugar Style, Barbeito 10-Year, Volcanic Northern Terroir)',
    output_dir='.',
    starting_entry=1,
    session_number=75,
    running_total=0
)

session.add_producer({
    'tradition': 'fortified',
    'name': 'Barbeito — Câmara de Lobos, Madeira',
    'location': 'Câmara de Lobos, Madeira, Portugal',
    'description': (
        'Barbeito is one of Madeira\'s youngest and most technically progressive '
        'shippers, founded in 1946 by Mário Barbeito and now under the direction '
        'of Ricardo Freitas, who trained in oenology in France and returned to '
        'Madeira to transform Barbeito from a conventional commercial shipper '
        'into the island\'s most innovative quality producer. Barbeito is '
        'distinguished by three practices that set it apart from the Madeira '
        'establishment: first, the house exclusively uses the traditional '
        'canteiro aging method (natural heat from Madeira\'s subtropical '
        'climate in the top-floor lodges) rather than the estufagem '
        '(artificial heating tanks) used by most commercial Madeira '
        'producers; second, the house specialises in single-vintage '
        'colheita and garrafeira bottlings from individual cask selections; '
        'and third, Ricardo Freitas has revived the most obscure Madeira '
        'grape varieties — including Terrantez and Bastardo — that were '
        'nearly extinct after phylloxera and Oídium destroyed most of '
        'Madeira\'s pre-disease vineyard. Barbeito\'s 10-year Sercial is '
        'the benchmark expression for the Sercial dry style in the '
        'canteiro-only production tier.'
    ),
    'founded': '1946',
    'region': 'Câmara de Lobos, Madeira, Portugal',
    'website': 'barbeito.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Skurnik Wines / Mannie\'s Wines and Spirits (US) — Madeira specialists',
    'type': 'importer',
    'description': (
        'Barbeito Madeira is distributed in the United States primarily through '
        'Skurnik Wines (New York) and through specialist Madeira importers '
        'including Mannie\'s Wines and Spirits. In Canada, BCLDB BC and '
        'LCBO Ontario carry selected Barbeito Madeira expressions on '
        'regular and Vintages allocation. The Barbeito 10-year Sercial '
        'is available at specialist Portuguese wine retailers and Madeira-focused '
        'fine wine shops in North America at USD $40–65 per 500ml. '
        'Barbeito is considered by Madeira specialist merchants to be '
        'one of the three essential Madeira houses (alongside Blandy\'s '
        'and Pereira d\'Oliveira) for professional wine programme sourcing.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['fortified'],
    'website': 'barbeito.com',
    'verified': False
})

session.add_beverage({
    'name': (
        'Barbeito 10-Year Sercial Madeira — Dry Style, Volcanic Northern Terroir, '
        'Canteiro Natural Aging, Câmara de Lobos'
    ),
    'category': 'fortified',
    'subcategory': 'madeira',
    'origin': 'Portugal',
    'region': 'Portugal — Madeira (Sercial Dry, Lowest-Sugar Style, Barbeito 10-Year, Volcanic Northern Terroir)',
    'producer': 'Barbeito — Câmara de Lobos, Madeira',
    'alcohol_content': 19.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Sercial (Cerceal Branco on the mainland) is grown on Madeira at the '
        'highest elevations on the island\'s steep volcanic terraces — '
        'specifically on the northern slopes of the island at 400–800m '
        'elevation, where the Atlantic-facing aspect reduces sun exposure '
        'and the altitude creates significantly cooler conditions than '
        'the southern coast. Madeira itself is a volcanic island of the '
        'Macaronesian archipelago in the Atlantic Ocean, 950km southwest '
        'of Lisbon: the volcanic basalt and tuff soils of the island '
        'terraces (poios) have no equivalent in mainland European '
        'viticulture — the basalt retains heat during the day and '
        'releases it slowly at night, while the tuff (volcanic ash '
        'layers) contributes exceptional mineral complexity to the '
        'wines. The Sercial vine, with its naturally high acidity and '
        'late ripening cycle, requires the longest growing season '
        'on the island — the cool northern-slope terraces at '
        '400–800m altitude are the only locations where Sercial '
        'achieves the slow, balanced ripening necessary for '
        'quality production. Harvest for Sercial on northern '
        'high-altitude terraces occurs in late October or November '
        '— 4–6 weeks later than the lower-altitude southern-coast '
        'varieties — with potential alcohol of only 10–11%, the '
        'lowest of all Madeira varieties and the basis for '
        'Sercial\'s maximum residual dryness after fortification. '
        'The annual rainfall of 1,500–2,000mm on Madeira\'s northern '
        'slopes (double the southern coast rainfall of 600–700mm) '
        'maintains soil moisture through the dry summer and creates '
        'the fresh, high-acid character of northern-slope Sercial '
        'versus the more concentrated low-altitude southern fruit.'
    ),
    'production_technique': (
        'Barbeito produces Sercial Madeira exclusively through the canteiro '
        'method — natural aging in the top-floor lodge rooms (estufas de '
        'canteiro) where Madeira\'s subtropical climate creates temperatures '
        'of 25–35°C in summer, producing the oxidative aging and heat- '
        'driven chemical transformation (Maillard reactions, Strecker '
        'degradation) that characterizes Madeira without the artificial '
        'estufagem heating tanks used in commercial production. The '
        'Sercial grape is harvested at 10–11% potential alcohol and '
        'pressed immediately after harvest to preserve the naturally '
        'high free-run acidity (pH 2.9–3.1, titratable acidity '
        '8–10 g/L) that defines the Sercial variety. Fermentation '
        'proceeds in stainless steel at 18–20°C until 9–10% ABV '
        'is achieved — a very high pre-fortification alcohol for '
        'Madeira production, producing the minimum residual sugar '
        '(under 35 g/L) that defines the Sercial dry designation. '
        'Fortification with 96% ABV neutral spirit (Madeira uses '
        'higher-strength spirit than Port\'s 77% ABV aguardente) '
        'to a final 19–20% ABV arrests fermentation while preserving '
        'the high natural acidity of Sercial. The fortified wine '
        'enters the canteiro aging programme in the Barbeito '
        '\'Lodge at Câmara de Lobos: 600L American oak barrels '
        'placed on the top floor where summer temperatures of '
        '25–35°C drive the deliberate heat-oxidative transformation '
        'unique to Madeira. The 10-year age-indicated Sercial '
        'is a blend of multiple vintages with an average age of '
        '10 years in canteiro — the blending assessment by Ricardo '
        'Freitas selecting lots that show the classic Sercial dry '
        'mineral and citrus character rather than the tropical '
        'fruit register of lower-altitude varieties. Unlike most '
        '10-year Madeira produced commercially through estufagem '
        '(3 months at 45–50°C), the Barbeito canteiro 10-year '
        'has undergone 10 years of genuine slow heat-oxidative '
        'transformation that produces a fundamentally different '
        'aromatic and structural complexity.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Amontillado Fino Sherry (dry fortified, oxidative aging, saline mineral)',
            'connection': (
                'Barbeito 10-year Sercial and Amontillado Sherry occupy the same '
                'sensory position in the dry fortified wine spectrum: both are '
                'the driest, most austere expressions of their respective fortified '
                'wine traditions, with under 40 g/L residual sugar, dominant '
                'mineral-saline character, and oxidative complexity (rancio, '
                'hazelnut, dried citrus) from extended barrel aging. The '
                'structural parallel is in the acid backbone: Sercial\'s '
                'extreme natural acidity (8–10 g/L titratable) and Fino '
                'Sherry\'s Albariza-chalk mineral acidity both provide the '
                'structural framework that survives oxidative aging without '
                'losing freshness — the acid being the preservation mechanism '
                'that allows genuinely dry fortified wine to age without '
                'becoming flat or fatigued.'
            )
        },
        {
            'tradition': 'Bairrada Baga Vinhas Velhas (extreme acidity, volcanic/limestone terroir, demanding)',
            'connection': (
                'Barbeito Sercial and Bairrada Baga Vinhas Velhas share the '
                'quality architecture of extremely high natural acidity as '
                'the defining structural element — Sercial\'s 8–10 g/L '
                'titratable acidity (pH 2.9–3.1) mirrors Baga\'s high natural '
                'acidity from the Atlantic-maritime Bairrada terroir. Both '
                'are the most demanding expressions of their respective '
                'Portuguese wine traditions: the driest Madeira style '
                '(Sercial) and the highest-tannin Portuguese table wine '
                '(Baga Vinhas Velhas). Both reward patience and informed '
                'service: Sercial requires the correct temperature '
                'and glass to reveal its mineral complexity; Baga requires '
                'years of bottle aging and mandatory decanting to '
                'integrate its structural tannin. Both are also among '
                'the most historically significant and currently '
                'under-appreciated wines in the Portuguese quality hierarchy.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale amber-gold with green highlights in the youngest expressions — '
            'the Sercial pale amber is lighter than other Madeira styles due '
            'to the lower sugar content reducing the degree of Maillard '
            'browning during canteiro aging; in older expressions (20+ years '
            'canteiro) the color deepens to amber; brilliant clarity; '
            'lighter viscosity than Bual or Malmsey due to the lower '
            'residual sugar (under 35 g/L versus 65–130 g/L for the '
            'sweeter styles); a distinctive green-gold mineral luminosity '
            'in the colour that is the visual marker of the Sercial '
            'dry style\'s volcanic northern terroir character.'
        ),
        'nose': (
            'Volcanic mineral and salt as the dominant opening register — '
            'the defining aromatic characteristic of Sercial grown on '
            'Madeira\'s northern basalt and tuff terraces that no '
            'other Madeira variety produces at this intensity; beneath '
            'the mineral, dried lemon peel and crystallized citrus from '
            'the Maillard transformation of Sercial\'s natural citrus '
            'fruit during canteiro aging; dried almond and hazelnut '
            'from the rancio development; the canteiro natural aging '
            'produces a subtler, more integrated caramel register than '
            'estufagem commercial production — less burnt caramel, '
            'more toasted almond and honey; the high natural acidity '
            'of Sercial creates a lifted, sharp quality to the aromatic '
            'register that distinguishes it from all other Madeira styles.'
        ),
        'palate': (
            'Bone dry or near-dry entry (under 35 g/L residual sugar '
            'perceived as dry against the extreme natural acidity); '
            'immediate volcanic mineral-saline character on the tongue; '
            'dried lemon and preserved citrus through the mid-palate '
            'from the canteiro heat transformation; the natural acidity '
            '(8–10 g/L titratable) creates extraordinary freshness '
            'and length on the finish — the acid the dominant structural '
            'element rather than the residual sugar; the rancio almond '
            'and hazelnut building on the persistent finish; the '
            'combination of extreme acidity, mineral character, '
            'and rancio complexity from canteiro aging creates a '
            'finish architecture unique in the fortified wine world — '
            'simultaneously austere, complex, and vivid.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Sercial (3-year estufagem, bulk production)',
            'criteria': (
                'Sercial produced through the estufagem method — 3 months '
                'at 45–50°C in stainless steel tanks — which creates the '
                'Madeira oxidative character through accelerated heat '
                'rather than slow canteiro natural aging; the result '
                'is a wine with Maillard caramel and burnt sugar '
                'character from the rapid heating, but lacking the '
                'depth of rancio complexity and the mineral terroir '
                'character that only slow canteiro aging produces.'
            )
        },
        {
            'tier': 2,
            'tier_name': '10-Year Sercial (canteiro, age-indicated)',
            'criteria': (
                'Ten-year average age in canteiro natural aging — the '
                'Barbeito benchmark; genuine volcanic mineral and '
                'rancio complexity from a decade of slow heat-oxidative '
                'canteiro aging; the Sercial dry style at full '
                'expression in the standard commercial tier; '
                'the acid backbone fully integrated after '
                '10 years of canteiro transformation.'
            )
        },
        {
            'tier': 3,
            'tier_name': '20-Year Sercial (extended canteiro, rare complexity)',
            'criteria': (
                'Twenty-year canteiro aging; the rancio and mineral '
                'complexity at maximum development for the 10-year tier; '
                'greater dried fruit and caramel concentration than '
                'the 10-year while retaining the characteristic '
                'Sercial dry-acid structure; Barbeito\'s 20-year '
                'Sercial is among the most sought-after Madeira '
                'expressions in this age category at specialist auction.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Sercial Colheita or Garrafeira (single cask, collector tier)',
            'criteria': (
                'Single-vintage Sercial colheita or garrafeira (bottle-aged '
                'expression) from Barbeito\'s archive — the apex of Sercial '
                'production at individual cask level; extraordinary mineral '
                'concentration and rancio complexity unique to single-cask '
                'Sercial from the high-altitude northern terraces; '
                'pricing USD $100–400+ for older expressions; '
                'available only through specialist Madeira retailers '
                'and auction.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Barbeito 10-year Sercial at 10–12°C — colder than '
            'most wine service to preserve the extreme natural acidity '
            'and the volatile mineral aromas that are the defining '
            'quality markers of canteiro-aged Sercial; above 14°C '
            'the high alcohol (19–20% ABV) becomes dominant and '
            'the delicate volcanic mineral-citrus register is '
            'partially obscured; serve as the opening fortified '
            'wine in a Madeira tasting sequence, before the '
            'progressively sweeter Verdelho, Bual, and Malmsey '
            'styles — the dry-to-sweet progression is the canonical '
            'Madeira service arc in a formal programme.'
        ),
        'vessel': (
            'Serve in a white wine tulip glass (150–175ml format) '
            'with 60–80ml pour — a slightly larger glass than '
            'a Port copita to allow the volatile mineral and '
            'dried citrus aromatics to expand; the Sercial dry '
            'style benefits from a wider opening than copita '
            'format to prevent the high acidity from dominating '
            'the aromatic register at the aperture; serve the '
            'glass chilled before pouring to maintain the '
            '10–12°C service temperature in the glass; present '
            'with a verbal explanation of the canteiro natural '
            'aging method versus estufagem commercial production '
            '— the distinction is essential for professional '
            'Madeira service and is the primary quality '
            'differentiator that most guests have never encountered.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Barbeito — Câmara de Lobos, Madeira (1946; the benchmark '
            'canteiro-only producer for Sercial dry Madeira; Ricardo '
            'Freitas is the reference winemaker for the Sercial style '
            'in the current generation of Madeira producers; the '
            '10-year Sercial is the starting point for any professional '
            'comparison of canteiro versus estufagem Madeira quality).'
        ),
        'north_america_access': (
            'Barbeito Madeira is distributed in the United States through '
            'Skurnik Wines at USD $40–65 per 500ml for the 10-year Sercial. '
            'In Canada, BCLDB BC and LCBO Ontario Vintages carry selected '
            'Barbeito expressions. Barbeito is considered an essential '
            'producer reference alongside Blandy\'s and Pereira '
            'd\'Oliveira for professional Madeira education; the '
            'three houses together cover the full spectrum from '
            'commercial estufagem (Blandy\'s) to canteiro specialist '
            '(Barbeito) to historic colheita archive (d\'Oliveiras).'
        ),
        'culinary_application': (
            'Sercial Madeira is the fortified wine equivalent of Fino '
            'Sherry for food pairing — the extreme acidity and dry '
            'mineral character creates pairings with smoked and salted '
            'fish (bacalhau, smoked mackerel, salt cod fritters) '
            'where the citric acid-mineral structure cuts through '
            'the salt and smoke; the volcanic mineral character of '
            'Sercial also bridges to oysters and shellfish — a '
            'pairing rare in fortified wine but natural for '
            'the bone-dry Sercial style; serve as an aperitif '
            'alongside Madeiran entremeada (limpets with garlic) '
            'for the defining within-region food and fortified '
            'wine pairing of the island.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
