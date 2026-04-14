import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Guyana — Demerara River (El Dorado Single Still, Diamond Distillery, Wooden Coffey Still Heritage)',
    output_dir='.',
    starting_entry=1,
    session_number=52,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Demerara Distillers Limited — Diamond Estate',
    'location': 'Diamond, East Bank Demerara, Guyana',
    'description': (
        'Demerara Distillers Limited (DDL) operates the Diamond Estate distillery on the east bank of the '
        'Demerara River south of Georgetown, and is the custodian of the most extraordinary collection of '
        'antique rum distillation apparatus in the world. DDL operates seven distinct stills: the famous '
        'double wooden pot still (Port Mourant), the single wooden pot still (Versailles), two wooden '
        'Coffey continuous stills (Enmore — the only operational wooden continuous stills in the world), '
        'a four-column metal Coffey still (Diamond), a single metal pot still (Savalle), and an Alberosia '
        'multi-column still. Each still was originally operated at a now-closed Guyanese sugar estate — '
        'the stills were moved to Diamond when their original estates shut down during the consolidation '
        'of the Guyanese sugar industry in the 20th century. El Dorado Single Still rums bottle '
        'distillates from individual stills, allowing comparison of how different antique still '
        'architectures produce radically different ester profiles from the same Demerara molasses base.'
    ),
    'founded': '1670 (Port Mourant estate); DDL consolidated 1983',
    'region': 'Demerara River, Guyana',
    'website': 'eldoradorum.com',
    'verified': True
})

session.add_beverage({
    'name': 'El Dorado Single Still PM — Port Mourant Double Wooden Pot, Demerara High Ester, Antique Still Heritage',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Guyana',
    'region': 'Guyana — Demerara River (El Dorado Single Still, Diamond Distillery, Wooden Coffey Still Heritage)',
    'producer': 'Demerara Distillers Limited — Diamond Estate',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Demerara River is one of Guyana\'s major coastal rivers, draining the interior rainforest '
        'highlands and depositing its sediment load across the broad alluvial coastal plain where '
        'Georgetown, the capital, and the historic sugar estates of Guyana\'s colonial era are '
        'concentrated. The coastal plain of Guyana lies at sea level or below — much of the agricultural '
        'land is polderized, maintained by a Dutch-engineered system of sluices and seawalls dating from '
        'the 17th and 18th century Dutch colonial period (then called Berbice and Demerara-Essequibo '
        'colonies). The deep alluvial soils of the Demerara coastal plain are among the richest in the '
        'Caribbean basin: the combination of equatorial rainfall (2,000–2,500mm annually with no dry '
        'season), equatorial temperatures (27–30°C year-round), and intense solar radiation at near-zero '
        'latitude creates sugarcane growth conditions of extraordinary vigour. The original Port Mourant '
        'estate on the Corentyne Coast (Berbice region) operated from 1670 — one of the oldest '
        'continuously documented sugarcane operations in the Americas — until consolidation shut down '
        'individual estate operations, leaving the Diamond Estate at East Bank Demerara as the sole '
        'surviving operational site. The still architecture at Diamond is not merely historical: '
        'the different woods, geometries, and heat distributions of each antique still produce '
        'systematically different ester profiles from the same Demerara molasses, making the still '
        'itself a terroir variable in the sense that the fermentation vessel and distillation geometry '
        'shape the spirit\'s chemical composition as distinctly as soil and climate shape wine character.'
    ),
    'production_technique': (
        'El Dorado Single Still PM is produced from Demerara molasses fermented in open wooden '
        'wash backs using the traditional long fermentation method: wild and semi-wild Saccharomyces '
        'yeast cultures with strains accumulated over decades in the wooden fermentation vessels '
        'produce a wash of 6–8% ABV over 36–72 hours. Long fermentation at warm Guyanese ambient '
        'temperatures (28–32°C) promotes high ester production through organic acid-alcohol esterification '
        'reactions, producing washes with exceptionally high ester content compared to standard '
        'controlled-temperature fermentations. The washed ferment is then distilled through the '
        'Port Mourant double wooden pot still — two wooden retorts connected in series, each '
        'holding approximately 2,500 litres, heated indirectly through a coil rather than direct '
        'flame. The wooden construction of the Port Mourant still is the critical technical element: '
        'wood is porous, allowing the spirit to interact with wood-derived tannins, mineral compounds, '
        'and decades of accumulated yeast and bacterial microflora within the wooden structure of '
        'the still itself. This interaction produces a high-ester distillate with a distinctive '
        'Demerara character — molasses richness combined with fruit esters (ethyl acetate, isoamyl '
        'acetate, ethyl butyrate) and the woody, slightly phenolic note of the wooden still interior '
        'at levels not achievable in copper or stainless steel pot stills. The final distillate from '
        'the PM still runs at approximately 70–75% ABV and is proofed to 40% ABV for the Single Still '
        'bottling without aging — the raw character of the wooden pot still expressed in unaged form '
        'to allow full sensory appreciation of the still\'s unique contribution to the Demerara character.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Mezcal de olla (clay pot distillation, Oaxaca) — vessel-as-terroir',
            'connection': (
                'El Dorado PM single wooden pot still rum and clay pot mezcal de olla share the same '
                'fundamental principle: the distillation vessel itself — whether Guyanese teak and '
                'pitch pine or Oaxacan clay — is a terroir variable as significant as geography. '
                'The wood of the Port Mourant still contributes accumulated microbiological cultures, '
                'lignin-derived tannin compounds, and mineral content from decades of seasoning, '
                'exactly as a clay pot imparts mineral notes from the fired clay\'s silicate and '
                'iron content — both producing spirits that cannot be replicated in copper or steel '
                'regardless of equivalent raw material and fermentation conditions.'
            )
        },
        {
            'tradition': 'Islay Single Malt Scotch (Bowmore, Bruichladdich) — wooden washback fermentation',
            'connection': (
                'Demerara DDL wooden fermentation washbacks and some Islay distilleries\' retention of '
                'wooden washbacks represent the parallel principle that fermentation vessel material '
                'shapes spirit character through accumulated microbiological culture: the yeast and '
                'lactic acid bacteria colonizing wooden washbacks over decades produce fermentation '
                'profiles distinct from stainless steel fermentation, contributing to the characteristic '
                'ester and organic acid complexity of both high-ester Demerara rum and the phenolic-ester '
                'complexity of traditional Islay single malt character.'
            )
        },
        {
            'tradition': 'Cognac single-still estate bottling (single distillery, unblended) — provenance transparency',
            'connection': (
                'El Dorado Single Still PM and single-estate unblended Cognac both pursue the same '
                'philosophical goal: maximum transparency of a specific still and fermentation location\'s '
                'contribution to the spirit\'s character, without blending to a house style. Both '
                'represent the argument that individual still architecture is a form of terroir expression '
                'as legitimate as vineyard or cane field geography — the Port Mourant double wooden pot '
                'producing a specific ester signature as distinctive and traceable as the Cognac estate\'s '
                'vineyard producing a recognizable base wine character.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale gold for the unaged Single Still expression; brilliant clarity from careful '
            'distillation cut management; the light colour belies the intensity of the aromatic '
            'and flavour complexity — the Single Still PM is among the most aromatically complex '
            'unaged rums in the world despite showing almost no colour development from the still itself.'
        ),
        'nose': (
            'Extraordinarily high ester character: ethyl acetate and isoamyl acetate produce '
            'overripe tropical fruit (banana, ripe guava, overripe mango) at intensities rarely '
            'encountered in other unaged spirits categories; beneath the ester register, the wooden '
            'still contributes a faintly earthy, slightly musty depth reminiscent of old barrel '
            'wood — the accumulated decades of fermentation culture in the Port Mourant still '
            'structure expressing in volatile compounds; molasses richness as a warm, caramelized '
            'base note beneath the explosive ester fruit; genuinely unlike any other rum category '
            'in aromatic intensity and specificity.'
        ),
        'palate': (
            'Medium body — thinner than the nose suggests — with massive ester intensity on the '
            'attack that resolves through the mid-palate into molasses richness and the earthy, '
            'woody character of the Port Mourant still interior; warming at 40% ABV; the finish '
            'is extremely long with ester fruit and wood phenolics fading slowly over 45–60 seconds '
            'after swallowing — demonstrating why Demerara high-ester rum is the blending agent '
            'of choice for premium blend creators in the Caribbean tradition seeking complexity '
            'and finish extension.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'El Dorado 3-Year (column still blend)',
            'criteria': (
                'Entry-level aged blend from the Diamond multi-column still: lighter ester character, '
                'clean molasses-caramel profile, 3-year tropical aging — the commercial baseline for '
                'Guyanese rum at accessible price points, suitable for cocktail applications where '
                'the extreme ester character of the wooden still expressions would overwhelm.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'El Dorado 12-Year (blended, multiple stills)',
            'criteria': (
                'Twelve-year tropical aged blend from multiple Diamond Estate stills: the wooden and '
                'metal still expressions combined in proportions that create the characteristic El Dorado '
                'house style of rich molasses, tropical fruit, and integrated oak — the international '
                'benchmark for aged Guyanese rum.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'El Dorado 21-Year (blended apex, multiple stills)',
            'criteria': (
                'Twenty-one year tropical aged blend representing maximum tropical maturation from '
                'the full range of Diamond Estate stills: deep mahogany colour, rancio character, '
                'complex dried fruit and spice — the peak expression of El Dorado house-style blending '
                'and one of the world\'s premier aged rum expressions by critical consensus.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'El Dorado Single Still PM (unaged, wooden double pot)',
            'criteria': (
                'Unaged distillate from the Port Mourant double wooden pot still: maximum ester '
                'character, wooden still microbiological complexity, no oak-aging influence — the '
                'most technically revealing expression of the Demerara wooden pot still tradition '
                'and the reference point for understanding how antique still architecture functions '
                'as a form of terroir expression in rum production.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'The Single Still PM is best evaluated at room temperature (20–22°C) for full ester '
            'aromatic expression; the extreme ester volatility means that serving chilled suppresses '
            'the most complex and distinctive aromatic compounds from the wooden pot still; a small '
            'addition of still water (5–10ml) at room temperature opens the mid-palate without '
            'washing the esters; serve as a spirits education reference before tasting aged '
            'El Dorado expressions to demonstrate how aging transforms but does not eliminate '
            'the Port Mourant still character.'
        ),
        'vessel': (
            'Tulip or Glencairn glass is mandatory for the Single Still PM — the extreme ester '
            'volatility requires vessel geometry that concentrates vapour at the rim to allow full '
            'aromatic evaluation; a wide glass disperses the esters too rapidly; pour at 30ml for '
            'evaluation to avoid nose fatigue from the high ester concentration; in cocktail use, '
            'the PM single still works as a float on a darker, aged Demerara rum base to add '
            'aromatic intensity and ester complexity to Tiki-style long drinks.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Demerara Distillers Limited (DDL) — sole custodian of the antique Port Mourant, '
            'Versailles, and Enmore wooden still heritage; El Dorado Single Still PM is the '
            'definitive expression of Guyanese wooden pot still character available in international '
            'markets; no other producer operates comparable antique wooden still architecture.'
        ),
        'north_america_access': (
            'El Dorado range widely distributed in the US through Paramount Brands; Canadian '
            'distribution through provincial liquor boards (BCLDB, LCBO); Single Still expressions '
            'available through specialty spirits retailers and direct import; pricing for Single '
            'Still PM at USD $45–60 retail.'
        ),
        'culinary_application': (
            'The extreme ester character of PM single still makes it a powerful culinary ingredient: '
            'a few drops added to a rum reduction sauce or tropical fruit dessert contributes '
            'concentrated ester fruit complexity impossible to achieve with aged blends; in cocktail '
            'programming, the PM single still is the definitive Tiki base spirit for maximally '
            'complex Demerara-style cocktails including the Zombie and the Jet Pilot.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
