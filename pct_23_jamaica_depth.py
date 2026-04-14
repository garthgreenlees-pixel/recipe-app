import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Jamaica — Trelawny and St Elizabeth Parishes (Hampden Estate, Worthy Park, High-Ester Rum)',
    output_dir='.',
    starting_entry=1,
    session_number=24,
    running_total=80
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Hampden Estate Distillery',
    'location': 'Trelawny Parish, Jamaica',
    'description': 'Jamaica\'s oldest continuously operated rum estate, founded 1753 on the Hampden Great House property in Trelawny Parish, central Jamaica. Hampden is the global benchmark for the "Hogo" style of Jamaican rum — an extremely high-ester production using open wooden fermenters (called "dunder pits") that recirculate the dead wash (stillage) from previous distillations to create a hyper-concentrated microbial environment. The distillery operates four copper pot stills of varying age and character, producing marks ranging from 500 g/hL AA (ester level) for accessible styles to 1,600+ g/hL AA for the legendary HLCF (High Ester Continental Flavoured) mark used by European blenders for more than 150 years. The Hampden Great House estate encompasses 3,000 acres of sugar cane cultivation at 150–300m elevation in the Trelawny hills. Hampden remained in the Clarke family from 1760 until 2009 when it was sold to the Proprietors of Hampden Estate Ltd — the first time the property had changed hands since colonial era. Since 2018 under distillery director Vivian Wisdom, Hampden has begun releasing its own bottled expressions for the first time in its 270-year history (previously selling exclusively to European blenders).',
    'founded': '1753',
    'region': 'Trelawny Parish, Jamaica',
    'website': 'hampdenrum.com',
    'verified': True
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Worthy Park Estate',
    'location': 'St Elizabeth Parish (Lluidas Vale), Jamaica',
    'description': 'Worthy Park is Jamaica\'s highest-altitude cane estate (350m above sea level in Lluidas Vale, inland St Elizabeth Parish) and one of the few estates growing all its own sugar cane for rum production — no purchased molasses. Founded 1720, the estate uses pot still and column still distillation to produce a range of marks from light (used in own-label blends) to very high ester (for European blender allocation). Worthy Park\'s rum is distinctive for its combination of altitude-influenced cane character — cooler temperatures produce slower cane maturation and higher sucrose concentration — with the traditional Jamaican spontaneous fermentation dunder system. The estate began direct bottling in 2015 under proprietor Gordon Clarke\'s direction, releasing single-mark expressions that have become reference bottles for the Jamaican pot still rum renaissance.',
    'founded': '1720',
    'region': 'Lluidas Vale, St Elizabeth Parish, Jamaica',
    'website': 'worthypark.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Velier SpA — Hampden Official Bottler',
    'type': 'importer_bottler',
    'description': 'Genoa-based Italian spirits importer and independent bottler, the primary international distributor for Hampden Estate rum following a 2018 partnership with distillery director Vivian Wisdom. Velier releases the Hampden Estate single-mark series including LFCH, HGML, C<OB, OWH, and the legendary HLCF mark at various ages and strengths. Velier is also the North American importer through various regional distributors. In Canada, Hampden is available through private import channels; in the US, through Spec\'s (Texas), K&L Wine Merchants (California), and Total Beverage (mid-Atlantic).',
    'markets_served': ['EU', 'US', 'Canada', 'UK', 'Japan'],
    'traditions_carried': ['spirits'],
    'website': 'velier.it',
    'verified': True
})

session.add_beverage({
    'name': 'Hampden Estate HLCF Classic — High-Ester Continental Flavoured, Trelawny Jamaica Pot Still',
    'category': 'spirits',
    'subcategory': 'rum_pot_still',
    'origin': 'Jamaica',
    'region': 'Trelawny Parish, Jamaica',
    'producer': 'Hampden Estate Distillery',
    'alcohol_content': 46.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Hampden Estate occupies 3,000 acres of the Trelawny hills in central Jamaica — a parish known historically as "the breadbasket of Jamaica" for its combination of rich red clay soils overlying limestone karst, adequate highland rainfall (1,400–1,800mm annually), and altitude (150–300m) that moderates the tropical heat to allow slower cane maturation than coastal estates. The Trelawny terroir produces cane with particularly high sucrose concentration and a mineral-rich character from the limestone aquifer irrigation. The critical terroir element for Hampden\'s HLCF mark, however, is not the cane itself but the distillery\'s microbial ecosystem: the open wooden fermenting vessels (called "puncheons" or vats) and the dunder pits that recirculate dead wash — the acidic, bacteria-rich stillage from previous distillations — have been accumulating microbial diversity for 270+ years of continuous operation. The dunder pit at Hampden is one of the most complex microbial environments in artisan spirits production: it contains live cultures of Clostridium bacteria, wild Schizosaccharomyces pombe yeast strains, Lactobacillus species, and multiple Acetobacter cultures that convert alcohol precursors into the esters that give Jamaican high-ester rum its defining character. The HLCF mark targets 1,600–1,800 g/hL AA (grams of ester per hectoliter of pure alcohol) — approximately 80–100 times higher ester concentration than standard Caribbean rum.'
    ),
    'production_technique': (
        'HLCF production begins with molasses from the Hampden Estate\'s own sugar milling — the same cane grown on the property provides both sugar and molasses substrate. Molasses is diluted with water in the puncheon vats to approximately 15–20 Brix and inoculated with a mixture of dunder (dead wash from previous distillation, seething with Clostridium and Lactobacillus bacteria) and muck (the bottom residue of the dunder pits, containing the most concentrated microbial culture). The addition of muck and dunder begins the esterification chemistry before yeast even begins alcoholic fermentation: the Clostridium bacteria produce butyric acid from molasses carbohydrates; Lactobacillus produces lactic acid; these short-chain organic acids combine with ethanol produced by Saccharomyces pombe in the subsequent fermentation to form esters — principally ethyl acetate, ethyl butyrate, and isoamyl acetate — at concentrations determined by the length of dunder fermentation (7–21 days for HLCF vs 3–5 days for lower-mark expressions). The fully fermented wash (10–12% ABV) is distilled in Hampden\'s copper pot stills in a double distillation: first in the wash still (producing "low wines" at 25–30% ABV) then redistillation in the spirit still to the final cut at 78–86% ABV. The high-ester character concentrates through distillation rather than being diminished by it. HLCF is then diluted to bottling strength and aged minimally (often 1–3 years in ex-bourbon barrels) to soften the raw distillate intensity while preserving the funky ester profile. The classic "HLCF Continental" style was historically aged in Europe (in Hamburg or Amsterdam bonded warehouses) under the British-era "rum trade" system — the "Continental" designation refers to this European aging rather than Caribbean tropical aging.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Rhum agricole AOC Martinique (Neisson, JM)',
            'connection': 'Both Hampden HLCF and rhum agricole represent the highest-ester, most terroir-expressive tier of Caribbean rum production — but they achieve this through opposite philosophies: Hampden through extended dunder fermentation that builds ester through bacterial chemistry, Martinique through fresh cane juice that preserves the vegetal ester precursors present in the cane itself before yeast contact'
        },
        {
            'tradition': 'Clairin Haiti (Barbancourt opposite: unaged pot still)',
            'connection': 'Hampden HLCF and Clairin represent the two extremes of Caribbean artisan rum production — Hampden maximizing ester through extended bacterial dunder fermentation in a 270-year-old microbial culture, Clairin maximizing terroir transparency through immediate bottling of unaged Haitian regional cane juice distillates — both defying the industrial blended rum paradigm from opposite directions'
        },
        {
            'tradition': 'Islay Scotch whisky (Laphroaig, Ardbeg peat character)',
            'connection': 'Hampden HLCF\'s extreme flavor intensity — the "Hogo" character (likely from "haut goût," French for "high taste/gamey") — occupies the same radical flavor territory as heavily peated Islay malt: both are acquired-taste, producer-terroir-expressive spirits beloved by connoisseurs and challenging to newcomers, both require context to understand as the apex of their tradition rather than flaws to be corrected'
        }
    ],
    'sensory_profile': {
        'appearance': 'Golden amber to deep gold depending on aging duration; clear; the color tells little — the ester intensity is the primary story',
        'nose': 'Explosive: overripe banana, nail polish remover (ethyl acetate), pineapple, passion fruit, rotting mango, furniture polish, rum-soaked raisin, tropical funk that hits immediately and fills the room — the "Hogo" is not subtle; 15 minutes in glass reveals the more structured fruit underneath the firework display',
        'palate': 'Full body, surprising sweetness from concentrated cane molasses base, massive fruit ester intensity, volcanic pineapple-banana-tropical mid-palate, long finish with waves of butyric and lactic acid complexity, residual warmth that is more comfortable than the nose suggests — the spirit\'s intensity integrates better on palate than nose implies'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Lower-Mark Hampden (LFCH, OWH)',
            'criteria': 'Ester level 500–800 g/hL AA, shorter dunder fermentation, more accessible flavor intensity — gateway into Hampden\'s production hierarchy; available at lower price points through Velier and independent bottlers'
        },
        {
            'tier': 2,
            'tier_name': 'HLCF Classic (Bottled at Strength)',
            'criteria': 'The signature 1,600+ g/hL AA mark, standardized recipe, released at 46% ABV in the Velier Classic series — the internationally available reference expression'
        },
        {
            'tier': 3,
            'tier_name': 'HLCF Single Vintage / Cask',
            'criteria': 'Identified vintage year and cask selection, variable ABV (often cask strength 58–70%), limited release through Velier and specialist independent bottlers — each vintage shows how dunder culture and harvest character interact in specific production years'
        },
        {
            'tier': 4,
            'tier_name': 'Grand Arôme Vintage Reserve (Limited)',
            'criteria': 'The rarest Hampden expressions: identified mark, single cask or micro-batch, extended aging (8–15 years), cask strength — allocated exclusively to top-tier spirits programs globally; Clairin Saccharin and Hampden Grand Arôme occupy the same rarefied tier as the world\'s most sought-after single malt expressions'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature (20–22°C) or slight warming in palm — never chilled; the ester compounds that define HLCF\'s character volatilize most expressively at 20–25°C; a single small ice block (5–10g) can reduce nose intensity for those finding it overwhelming without destroying the palate character',
        'vessel': 'Tulip glass or Glencairn to concentrate and focus the explosive ester aromatics; nosing in wide-open wine glass disperses the intensity too fast; allow 5 full minutes of nose contact before tasting — the "Hogo" character separates into its component fruits over time',
        'cocktail_philosophy': 'The Mai Tai (Trader Vic\'s 1944 original recipe) calls for aged Jamaican rum as one component specifically because the high-ester character of Hampden-style rum provides the backbone that makes the drink work; HLCF at 25% of the rum blend (mixed with a lighter aged Caribbean rum) delivers authentic Mai Tai character'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Hampden Estate Distillery — HLCF mark; Velier SpA official bottler for international markets',
        'north_america_access': 'Velier Hampden range through Spec\'s (Texas), K&L Wine Merchants (CA), Astor Wines (NYC); Canada through private import; exceptional sommelier wine lists in Vancouver (The Botanist Hotel bar program) and Seattle (Rob Roy) carry Hampden expressions',
        'culinary_application': 'HLCF used in reduction-based sauces adds an extraordinary tropical depth to Caribbean-influenced preparations; the ester chemistry that makes it intense neat becomes complex background note when heat-reduced by 80% in a sauce; works in dark chocolate ganache as a counter-intuitive pairing where the butyric acid characters merge into a truffled dark chocolate note'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('spirits', 'Jamaica — Lluidas Vale St Elizabeth (Worthy Park Estate, Altitude Pot Still, Single Mark)')

session.add_beverage({
    'name': 'Worthy Park Estate WPE Single Estate — Altitude Pot Still, 350m Lluidas Vale Jamaica',
    'category': 'spirits',
    'subcategory': 'rum_pot_still',
    'origin': 'Jamaica',
    'region': 'Lluidas Vale, St Elizabeth Parish, Jamaica',
    'producer': 'Worthy Park Estate',
    'alcohol_content': 45.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Worthy Park Estate sits at 350m elevation in Lluidas Vale — a highland agricultural basin in the interior of St Elizabeth Parish, hemmed in by the Nassau Mountains to the north and the Dry Harbour Mountains to the south. This altitude is exceptional for Caribbean sugar cane cultivation: the Jamaican coast averages 27–32°C year-round, but Lluidas Vale at 350m reaches only 22–26°C during the day and 16–18°C at night — a diurnal range that fundamentally alters cane physiology. Slower maturation at altitude produces higher sucrose concentration per unit of cane at harvest, greater phenolic complexity from the cane\'s extended growing season, and a different ester precursor profile than coastal cane. Worthy Park grows all its own cane on 1,200 acres of the valley, controlling the full supply chain from field to bottle — an agricultural self-sufficiency almost unheard of in Caribbean rum production, where most distilleries purchase molasses from external sugar refineries. The estate\'s terroir specificity is further defined by the unique Lluidas Vale ecology: the valley floor is a flat alluvial plain of dark brown clay loam over limestone bedrock, while the valley walls rise steeply to forest reserve. The microclimate is drier than Trelawny (Hampden\'s parish) and cooler, producing a cane character that is less tropical-exuberant and more structured — evident in the Worthy Park rum\'s restrained fruit character compared to Hampden\'s explosive high-ester profile.'
    ),
    'production_technique': (
        'Worthy Park\'s cane is cut by a combination of mechanical and manual harvesting on the valley floor, transported to the on-site milling facility where it is crushed to extract juice. The juice is clarified and concentrated to molasses (approximately 80 Brix) in the estate\'s own evaporators, rather than purchasing external molasses — a choice that maintains full traceability from field to fermenter. Fermentation occurs in stainless steel closed vats for 5–7 days using a mix of indigenous wild yeast and a house Saccharomyces cerevisiae culture — a hybrid approach between the fully spontaneous fermentation of the highest-ester Jamaican producers and the fully commercial-yeast production of Caribbean industrial rum. The dunder recycling system at Worthy Park operates at moderate intensity: dunder is returned to fermentations at 15–20% of wash volume (compared to Hampden\'s more aggressive 40–60% additions). This produces ester levels in the moderate range — 200–600 g/hL AA for the WPE expression — creating a Jamaican pot still rum that is recognizably funky without the extremity of the Hampden marks. Double distillation occurs in Worthy Park\'s copper pot stills (a pair of 5,000-litre wash stills and a 2,500-litre spirit still), with hearts cut taken conservatively to preserve the house character. Aging occurs in ex-bourbon American oak barrels (mainly Jim Beam cooperage) in a single aging warehouse on the estate at ambient altitude temperature — the cooler Lluidas Vale climate produces slower but more even barrel interaction than low-altitude Caribbean aging, contributing to a more restrained oak integration.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Armagnac single estate (Domaine Tariquet style)',
            'connection': 'Worthy Park\'s single-estate philosophy — all cane grown on property, full supply-chain control from field to bottle — directly parallels the single-estate Armagnac model where all grapes are grown, distilled, and aged on the property; both produce spirits of identifiable terroir specificity rather than blended consistency'
        },
        {
            'tradition': 'Japanese single malt (altitude production, restrained character)',
            'connection': 'Worthy Park\'s altitude cooling and restrained dunder intensity producing a moderate-ester, structured rum mirrors the character of Japanese highland single malts (Hakushu, Yoichi) — both represent how altitude modifies spirit character toward greater structure and restraint compared to tropical/coastal productions of the same category'
        },
        {
            'tradition': 'Barbados pot still rum (Mount Gay XO, Foursquare Exceptional Cask)',
            'connection': 'Worthy Park and the great Barbados pot still houses (Foursquare, Mount Gay) represent the "terroir-expressive traditional Caribbean" tier against Hampden\'s "maximum ester intensity" tier — Worthy Park occupies the same quality register as Foursquare but through Jamaican rather than Barbadian production philosophy, with higher ester and more funk than Barbados but more restraint than Hampden'
        }
    ],
    'sensory_profile': {
        'appearance': 'Warm amber gold, clear, medium viscosity, good legs from 45% ABV natural dilution',
        'nose': 'Ripe banana, baking spices, vanilla from ex-bourbon oak, moderate Jamaican funk (butyric, fruity esters at manageable intensity), dried fruit, brown sugar cane — welcoming rather than challenging, the Jamaican character present but not dominating; more structured than coastal Jamaican rum with the Lluidas Vale altitude evident as a cooler, more restrained fruit register',
        'palate': 'Medium-full body, balanced sweetness from molasses concentration, warm spice mid-palate, moderate ester intensity that builds in the middle, clean finish with lingering cane sugar and dried fruit — a rum that communicates its Jamaican heritage without demanding specialist knowledge to appreciate'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Worthy Park Single Estate (White Unaged)',
            'criteria': 'Pot still distillate bottled at 63% without aging — the naked terroir expression used by cocktail bartenders for Ti\' Punch and Daiquiri applications requiring Jamaican character without oak influence'
        },
        {
            'tier': 2,
            'tier_name': 'WPE Single Estate (3-5 year)',
            'criteria': 'Standard bottling at 45% with 3–5 years ex-bourbon aging — the internationally distributed reference expression balancing Jamaican character with accessible oak integration'
        },
        {
            'tier': 3,
            'tier_name': 'WPE Cask Collection (8-15 year)',
            'criteria': 'Selected casks at extended age, variable bottling strength (often 54–58% cask strength), limited quantities — each release shows how altitude aging transforms the moderate-ester base spirit over time into something of genuine complexity'
        },
        {
            'tier': 4,
            'tier_name': 'WPE Special Releases (Mark-Specific)',
            'criteria': 'Identified mark expressions (using Jamaican rum mark coding system for ester level), independent bottler collaboration, cask strength — the specialist tier connecting Worthy Park to the connoisseur Jamaican rum market alongside Hampden and Clarendon'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature to slightly warmed — 20–23°C — to open the moderate ester character; WPE is more versatile than Hampden HLCF and performs well both neat and in cocktails without the overwhelming intensity management required for high-ester marks',
        'vessel': 'Glencairn or tulip for neat service; wide-mouthed rocks glass for on-the-rocks service; works well in a wide range of cocktail glassware given its moderate intensity',
        'cocktail_applications': 'WPE is the most versatile Jamaican pot still rum for cocktail use: authentic Jamaican Daiquiri character without overpowering delicate citrus; backbone for rum old fashioned with Angostura and orange; the altitude-cooled structure holds up in Jungle Bird (Campari, pineapple) without being overwhelmed by sweet-bitter modifiers'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Worthy Park Estate — WPE Single Estate bottling (self-produced, distributed through independent spirits importers)',
        'north_america_access': 'Widely distributed in US through Total Beverage Solution (national importer); in Canada through both LCBO (Ontario) and BC Liquor (limited listing); Longitude 122 in Vancouver and The Rum House in NYC carry full range',
        'culinary_application': 'WPE at moderate intensity works as a marinade base for Caribbean-influenced fish preparations (escovitch, jerk-spiced Pacific salmon); the moderate ester character complements rather than competes with Pacific Northwest cold-smoked salmon in a rum-smoked preparation; outstanding in rum cake and rum raisin applications where the altitude-structured character adds depth without the aggression of high-ester marks'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
