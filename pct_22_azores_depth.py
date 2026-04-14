import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Azores (Pico Island Volcanic Verdelho, Basalt Currais UNESCO Landscape)',
    output_dir='.',
    starting_entry=1,
    session_number=23,
    running_total=78
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Adega do Vulcão — Cooperativa Vitivinícola da Ilha do Pico',
    'location': 'Madalena, Pico Island, Azores, Portugal',
    'description': 'The largest wine cooperative on Pico Island, vinifying grapes from member smallholders whose plots are interlocked within the UNESCO-listed basalt currais landscape. The cooperative maintains traditional Verdelho do Pico production alongside the newer Arinto dos Açores variety. Adega do Vulcão is the primary commercial conduit for the island\'s wine culture, operating from a modern facility in Madalena port town with direct views across the Pico-Faial channel to Horta harbor. The cooperative\'s work is inseparable from the landscape preservation effort: the currais system requires constant stone wall maintenance, and the cooperative\'s financial viability determines whether smallholders can justify the labor cost of upkeep.',
    'founded': '1949',
    'region': 'Pico Island, Azores',
    'website': 'adegadovulcao.pt',
    'verified': False
})

session.add_producer({
    'tradition': 'wine',
    'name': 'Azores Wine Company — António Maçanita',
    'location': 'Biscoitos, Terceira Island; Criação Velha, Pico Island, Azores',
    'description': 'The most internationally visible Azorean wine producer, founded by winemaker António Maçanita to bring the volcanic island wines to world markets. Maçanita vinifies across multiple Azorean islands — Pico, Terceira, Faial, Graciosa — producing varietal expressions from the native Verdelho do Pico, Terrantez do Pico, Arinto dos Açores, and Barcelo varieties. His Pico wines are produced entirely from currais-grown grapes in the UNESCO heritage zone. The AWC is the primary export ambassador for Azorean wine globally, with distribution in North America through Classical Wines from Spain (US) and Select Wines (Canada).',
    'founded': '2014',
    'region': 'Pico Island and Terceira Island, Azores',
    'website': 'azoreswinecompany.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Azores Wine Company — Direct Export / Vineyard Brands',
    'type': 'producer_direct',
    'description': 'António Maçanita\'s AWC exports directly to importers in 25+ countries. In North America: Vineyard Brands (US national importer) and Select Wines (Canada). Also available through volcanic wine specialist retailers including Chambers Street Wines (NYC) and Les Caves de Pyrène (UK).',
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Japan'],
    'traditions_carried': ['wine'],
    'website': 'azoreswinecompany.com',
    'verified': True
})

session.add_beverage({
    'name': 'Pico Island Verdelho do Pico White — UNESCO Basalt Currais, Azores Volcanic Mineral',
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Pico Island, Azores',
    'producer': 'Azores Wine Company — António Maçanita',
    'alcohol_content': 12.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'Pico Island sits at the base of the highest mountain in Portugal — the 2,351m Pico volcano — rising from the Atlantic Ocean 1,500km west of mainland Portugal, positioned between the Mid-Atlantic Ridge and the Azores Triple Junction of tectonic plates. The UNESCO-listed Landscape of the Pico Island Vineyard Culture (2004) covers the entire western coastal strip of Pico: a network of low black basalt stone walls (currais) built by Portuguese settlers from the 15th century onward to divide the lava flow landscape into small rectangular plots of 0.1–0.3 hectares each. Over 20,000 such currais structures cover 987 hectares of certified vineyard — the most extraordinary man-made viticultural landscape on Earth, comparable only to the Lavaux terraces of Switzerland or the Douro schist slopes in its physical demands. The soils are classified as Andosols (volcanic ash soils): dark, high-organic, extremely water-retentive, with a pH of 5.5–6.5 and natural phosphorus fixing from volcanic minerals. The black basalt currais walls serve multiple functions: wind protection from the North Atlantic gales (critical at sea level); thermal mass absorbing solar radiation and re-emitting warmth through cold Azorean nights; moisture retention in the drip zone along wall bases where vine roots concentrate. Sea spray from the surrounding Atlantic contributes saline mineral complexity detectable in the wine — a signature that no mainland Portuguese wine can replicate. The Verdelho do Pico cultivar is a genetically distinct population from mainland Verdelho, adapted over 500 years to Azorean volcanic conditions: thicker skins, smaller berries, lower natural sugar accumulation that produces characteristically lean wines at 11.5–13% ABV.'
    ),
    'production_technique': (
        'Harvest on Pico Island is entirely manual — the currais layout makes mechanical access impossible. Pickers work bent double through narrow stone wall gates to reach individual vines trained in the traditional "baixo" (low) system, with cordons running horizontally along the ground surface to benefit from basalt thermal radiation. Harvest timing runs late September through October, later than mainland Portugal due to Atlantic cooling. Grapes are hand-sorted at the winery before whole-cluster pressing in pneumatic presses. António Maçanita\'s AWC philosophy emphasizes minimal intervention: fermentation occurs in stainless steel at controlled 15–18°C with indigenous yeasts (no commercial yeast addition) — the wild Azorean yeast population produces a distinctive fermentation profile with more volatile acidity precursors than mainland Portuguese yeasts, contributing to the wine\'s complex aromatics at low alcohol levels. No malolactic fermentation — the natural high acidity of Atlantic-influenced Azorean grapes is preserved as the primary structural element. Aging for 4–6 months on fine lees in stainless steel, with bâtonnage every two weeks, builds the textural weight needed to balance the vibrant acidity. No new oak contact for the varietal expressions; limited oak barrel use only for the reserve tier. Bottled unfined with minimal filtration, resulting in a natural turbidity that settles with time. The production volume of the AWC\'s Pico wines is constrained by currais plot access and manual labor availability — annual production rarely exceeds 15,000 bottles from the heritage parcels.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Canary Islands Lanzarote Malvasia (volcanic black basalt)',
            'connection': 'Both Pico Verdelho and Lanzarote Malvasia grow in black volcanic basalt landscapes created by recent lava flows, producing wines with pronounced saline-mineral character from Atlantic sea spray and volcanic soil mineral absorption — the closest parallel to Pico\'s terroir signature anywhere in the wine world'
        },
        {
            'tradition': 'Santorini Assyrtiko (volcanic pumice/basalt, Aegean)',
            'connection': 'Pico\'s Verdelho and Santorini\'s Assyrtiko represent the two great Atlantic and Mediterranean volcanic white wine traditions: both thrive on volcanic substrates, produce high-acid low-alcohol whites with saline sea air minerality, and are cultivated in labor-intensive traditional training systems (currais and kouloura baskets) that resist mechanization — producing wines of precision that only their specific volcanic islands can produce'
        },
        {
            'tradition': 'Madeira Verdelho (same cultivar, different thermal regime)',
            'connection': 'Verdelho do Pico is the ancestor of Madeira Verdelho — or a parallel evolution of the same Portuguese cultivar under different island conditions. Madeira Verdelho produces an off-dry fortified wine with volcanic sulfurous notes and orange peel acidity; Pico Verdelho produces a bone-dry unfortified table wine with saline Atlantic freshness — the same grape showing how dramatically terroir and technique diverge outcomes across the Macaronesian archipelagos'
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale straw with faint green tint; water-clear brilliance or slight natural turbidity in unfiltered versions; medium legs on a cold glass surface',
        'nose': 'Saline sea air, green apple, white peach, volcanic sulfur mineral, lemon zest, subtle crushed limestone, ocean spray — the Atlantic signature unmistakable and unlike any mainland white wine; low aromatic intensity at first pour, opening over 20 minutes in glass',
        'palate': 'Lean body, piercing acidity (malic-dominant), saline mineral texture from sea spray absorption, green apple fruit, long finish with persistent volcanic mineral and salt — the wine\'s greatness is in structure and length rather than aromatic exuberance; lees aging adds a subtle creamy texture that softens the stony austerity'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Cooperative Basic (Adega do Vulcão standard)',
            'criteria': 'Commercial yeast fermentation, stainless steel, early release — accessible but lacks the depth and mineral precision of single-parcel production; the accessible entry into Azorean wine culture'
        },
        {
            'tier': 2,
            'tier_name': 'AWC Currais Verdelho Varietal',
            'criteria': 'Indigenous yeast fermentation, 4–6 months lees aging, heritage currais plot selection, minimal filtration — the signature expression of Pico Island wine currently achieving international recognition'
        },
        {
            'tier': 3,
            'tier_name': 'AWC Rezerva / Single-Parcel Selections',
            'criteria': 'Identified individual currais parcels with oldest vine age (60–100 year old ungrafted Verdelho do Pico vines), extended 8–12 months lees aging, no fining or filtration — production under 3,000 bottles, internationally allocated through specialist importers'
        },
        {
            'tier': 4,
            'tier_name': 'Heritage Terrantez do Pico',
            'criteria': 'Separate cultivar tier: Terrantez do Pico (the rarest Azorean variety with only 15ha island-wide) produces the highest-complexity, longest-lived expression of Pico volcanic wine — structured for 10–20 year aging, showing volcanic sulfur, oxidative complexity, and extraordinary mineral tension'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 10–12°C — colder than most whites to suppress the initial sulfurous reduction note and focus the saline mineral signature; allow 10 minutes in glass before first assessment as the wine needs time to express its full aromatic range',
        'vessel': 'White Burgundy glass (wider bowl than Riesling format) to concentrate the subtle volcanic aromatics; avoid narrow tulip which suppresses the sea air character; larger format is better here given the wine\'s slow aromatic development',
        'food_philosophy': 'The classic pairing is Azorean percebes (barnacles) and lapas (limpets grilled with garlic butter) — the saline mineral wine mirrors the briny ocean character of the shellfish; for PNW service: Dungeness crab, Pacific oysters, Haida Gwaii halibut — any seafood where Atlantic-mineral wine character resonates with Pacific-mineral seafood character'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Azores Wine Company (António Maçanita) — AWC Currais Verdelho and Terrantez do Pico are the international benchmark expressions',
        'north_america_access': 'AWC available through Vineyard Brands (US); Select Wines (Canada); direct allocation from AWC export team for restaurants; Chambers Street Wines (NYC) carries full AWC range; in Vancouver BC through private import channels — not yet widely listed in BC Liquor',
        'culinary_application': 'Outstanding alternative to Muscadet or Chablis in oyster bar programs; the UNESCO heritage narrative and volcanic production story makes it highly compelling for sommelier wine lists; under-ordered relative to its quality-to-price ratio because Azorean wine is still largely unknown to North American diners'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Portugal — Azores (Terceira Island Biscoitos, Ramisco do Pico, Heritage Red Varieties)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Quinta dos Açores — Biscoitos, Terceira Island',
    'location': 'Biscoitos, Terceira Island, Azores, Portugal',
    'description': 'Terceira Island estate in the Biscoitos wine subregion, where Azorean reds are produced from Rabo de Ovelha, Verdelho Tinto, and other pre-phylloxera heritage varieties. Biscoitos (meaning "biscuits" — referring to the lava rock landscape) sits on Terceira\'s north coast within the UNESCO Natural Park. The estate works with both the AWC and independently to produce small quantities of Azorean red wine — the most obscure and collectible expression of the archipelago\'s wine culture.',
    'founded': None,
    'region': 'Terceira Island, Azores',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Terceira Island Biscoitos Tinto — Pre-Phylloxera Heritage Red, Azores Volcanic',
    'category': 'wine',
    'subcategory': 'red_wine',
    'origin': 'Portugal',
    'region': 'Terceira Island, Azores',
    'producer': 'Azores Wine Company — António Maçanita',
    'alcohol_content': 12.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Terceira Island\'s Biscoitos wine subregion (the only officially demarcated wine zone on Terceira) sits on the north coast, where volcanic lava flows from the Guilherme Moniz caldera and Serra de Santa Bárbara created the most recent (geological time) viticultural surfaces in the Azores. The key terroir distinction is phylloxera: the Azores archipelago, despite being part of Portugal, was never systematically affected by the phylloxera devastation that swept mainland Europe in the 1860s–1890s. Biscoitos maintains a population of ungrafted pre-phylloxera vines — the same genetic material that produced pre-1860 European wine — growing on their own roots in volcanic basalt soils. These ungrafted Vitis vinifera vines (Rabo de Ovelha, Verdelho Tinto, Arinto dos Açores) are believed to be 80–150+ years old, representing what European viticulture looked like before phylloxera forced the continent to graft European vines onto American rootstock. The phenolic structure of ungrafted vines grown in volcanic soil at Atlantic latitude produces a red wine profile unlike any mainland Portuguese expression: lower alcohol (10.5–12.5%), higher natural acidity, deeper mineral-saline character, and extremely fine tannin from low-sugar slow-ripening in Atlantic conditions.'
    ),
    'production_technique': (
        'Biscoitos red production follows the same currais-landscape manual harvest as Pico, but Terceira\'s volcanic topography allows slightly more mechanization in transport (donkeys and small tractors on the lava paths between walled plots). AWC vinifies Biscoitos red from multiple heritage variety parcels — Rabo de Ovelha Tinto, Verdelho Tinto, and trace amounts of Barcelo and Agronómica — maintaining varietal separation through harvest and early vinification. Fermentation occurs in open-top stainless tanks with twice-daily punch-down of the cap for 10–14 days at 22–24°C, using indigenous Azorean yeasts. Extended maceration of 20–30 days post-fermentation builds tannin extract from the naturally thin-skinned Atlantic varieties. Malolactic fermentation proceeds naturally, converting the sharp malic acid from Atlantic-cooled grapes into lactic acid. No new oak — aging in large old Portuguese chestnut or neutral French oak vats for 8–12 months preserves the volcanic mineral character rather than superimposing wood aromatics. The resulting wine is structured, medium-bodied, with aggressive natural acidity that requires 3–5 years of bottle aging to integrate.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Jura Poulsard (thin-skinned, high-acid, pre-phylloxera character)',
            'connection': 'Biscoitos Tinto and Jura Poulsard occupy the same register of thin-skinned, high-acid, low-alcohol, finely tannic reds that are challenging to understand without context but reveal profound complexity with time — both represent pre-industrial wine culture preserved in geographic isolation (Atlantic island vs alpine valley) from modern viticulture\'s obsession with extraction'
        },
        {
            'tradition': 'Madeira Bastardo (same pre-phylloxera variety origin)',
            'connection': 'The heritage red varieties of the Azores and Madeira share pre-phylloxera Portuguese genetic heritage — both archipelagos preserved what mainland Portugal lost. While Madeira Bastardo became a fortified oddity, Biscoitos red varieties remained as table wine in their original unfortified form, representing what pre-1860 Portuguese red wine tasted like'
        },
        {
            'tradition': 'Alentejo heritage varieties (pre-grafting complexity)',
            'connection': 'Post-phylloxera mainland Portugal lost the nuance of ungrafted vine character in Alentejo and Douro, replaced by American-rootstock vigor that tends toward higher yield and lower concentration. Biscoitos demonstrates what those mainland varieties would still express if ungrafted — a living counter-factual of European wine history'
        }
    ],
    'sensory_profile': {
        'appearance': 'Medium garnet with violet tint; clear to slightly hazy; lighter color than expected given Atlantic slow ripening; visible fine sediment in aged expressions',
        'nose': 'Red cherry, crushed volcanic rock, Atlantic sea air, dried herbs, light pepper, minimal oak — fresher and more aromatic than the extraction-focused style of modern Portuguese reds; the volcanic mineral signature is the primary identification marker',
        'palate': 'Light-medium body, sharp acidity that dominates youth but integrates beautifully at 5+ years, fine-grained tannin, red fruit mid-palate, long mineral-saline finish — a Burgundian register expressed through Azorean volcanic geology, deeply original and unlike any other Portuguese red wine'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Cooperative Biscoitos Tinto',
            'criteria': 'Blended production from cooperative members, commercial yeast, some new oak contact — accessible Azorean red with volcanic character but without the precision of single-estate production'
        },
        {
            'tier': 2,
            'tier_name': 'AWC Biscoitos Varietal',
            'criteria': 'Indigenous yeast, neutral vessel aging, varietal separation — the current international reference expression at accessible premium pricing'
        },
        {
            'tier': 3,
            'tier_name': 'AWC Old Vine Reserve',
            'criteria': 'Selection from identified 80–150 year ungrafted vines, extended maceration and lees contact, 12 months neutral vessel aging — limited production under 2,000 bottles, available through allocation to specialist importers'
        },
        {
            'tier': 4,
            'tier_name': 'Single-Vine Heritage (Rarissima)',
            'criteria': 'Individual ungrafted centenary vine selection, whole-cluster fermentation, non-interventional aging — fewer than 500 bottles when produced; the ultimate expression of pre-phylloxera Azorean viticulture, priced accordingly and allocated exclusively to top-tier wine programs'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 14–16°C — warmer than most light reds to open the volcanic mineral aromatics; do not chill like Beaujolais, which would suppress the saline Atlantic character; young vintages benefit from 30 minutes decanting',
        'vessel': 'Burgundy glass to concentrate the subtle volcanic aromatics and allow the thin-skinned fruit to express itself without the bowl dominating — these are not extraction-forward wines that need Bordeaux glass size; aged expressions can be served in a slightly larger format',
        'aging_potential': 'Biscoitos Tinto from the AWC Old Vine selection rewards 5–10 year cellaring; the aggressive malic acid of youth transforms into a saline, mineral, tertiary-complexity profile at 8–12 years — one of the most dramatically age-transforming wines in the Portuguese portfolio despite its low alcohol and delicate appearance'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Azores Wine Company (António Maçanita) — AWC Biscoitos Tinto and Rezerva selections are the only internationally distributed Terceira Island red wines as of 2024–2025',
        'north_america_access': 'Available through same AWC import channels as Pico Verdelho; extremely limited allocation; Chambers Street Wines (NYC) and Kermit Lynch Wine Merchant (Berkeley CA) are the primary US retailers carrying AWC Biscoitos Tinto',
        'culinary_application': 'Volcanic red acidity and minerality makes Biscoitos Tinto exceptional with Pacific Northwest mushrooms (chanterelles, porcini, morels) — the volcanic mineral register resonates with the earthy umami of Cascadia foraged fungi; also outstanding with Dungeness crab bisque where the wine\'s acidity cuts through the richness while the saline character mirrors the ocean'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
