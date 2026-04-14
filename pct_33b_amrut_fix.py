import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='India — Bangalore Karnataka (Amrut Single Malt, Tropical Aging Pioneer, 920m Elevation)',
    output_dir='.',
    starting_entry=1,
    session_number=35,
    running_total=101
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Amrut Distilleries — Bangalore',
    'location': 'Bangalore, Karnataka, India',
    'description': 'Founded 1948 as a spirit alcohol producer for industrial purposes, Amrut began single malt whisky production in 1987 and released its first internationally exported single malt in 2004. In 2010, Amrut Fusion received 97 points from whisky critic Jim Murray — the first time a non-Scotch, non-Japanese whisky had received a score comparable to the world\'s best malts. The Bangalore distillery sits at 920m elevation on the Deccan Plateau in a climate that is drier and cooler than Goa coastal tropical, creating slower-but-still-accelerated barrel maturation compared to Scotland.',
    'founded': '1948 (industrial); single malt 1987',
    'region': 'Bangalore, Karnataka, India',
    'website': 'amrutdistilleries.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Amrut Global — US and Canadian Distribution',
    'type': 'importer',
    'description': 'Amrut is imported to the US through John Emerald Distilling\'s import arm and Anchor Distilling. In Canada through Fine Estate Wines and Spirits (BC) and LCBO (Ontario). The Amrut Fusion and Amrut Peated are standard stock at BCLDB; special releases through private import and specialist retailers.',
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Australia'],
    'traditions_carried': ['spirits'],
    'website': 'amrutdistilleries.com',
    'verified': True
})

session.add_beverage({
    'name': 'Amrut Fusion Single Malt — Bangalore 920m Deccan Plateau, Indian-Scottish Barley Blend, 97-Point Pioneer',
    'category': 'spirits',
    'subcategory': 'whisky_single_malt',
    'origin': 'India',
    'region': 'Bangalore, Karnataka, India',
    'producer': 'Amrut Distilleries — Bangalore',
    'alcohol_content': 50.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Amrut Distillery sits at 920m elevation on the Deccan Plateau — the ancient basaltic lava plateau covering much of peninsular India, created by massive volcanic eruptions approximately 66 million years ago. Bangalore\'s specific climate is drier and cooler than the Goa coastal climate: distinct cool dry season from November to February (15–22°C) and hot pre-monsoon from March to May (28–35°C), creating a bimodal extraction cycle in barrel maturation. The 920m altitude produces lower oxygen partial pressure than sea level, affecting both fermentation and barrel aging. Angel\'s share at Bangalore is 8–10% per year — lower than humid Goa (10–12%) but far higher than Scottish 2%. The Indian six-row barley from Rajasthan and Haryana expresses a spicier, more grain-assertive character than two-row Scottish barley, contributing the Indian spice signature that defines the Fusion\'s first aromatic wave before the peated component arrives.'
    ),
    'production_technique': (
        'Amrut Fusion is a vatting of two separately distilled and aged whiskies: Indian unpeated malt (from Rajasthan six-row barley, distilled at Bangalore in copper pot stills) and Scottish peated malt (barley malted in Scotland at 30–35 ppm phenol, shipped to Bangalore for distillation). Both components are independently distilled and aged separately in ex-bourbon American oak casks (Indian unpeated) and a combination of ex-bourbon and ex-sherry (Scottish peated). After 4–6 years, the two aged whiskies are vatted at approximately 60% Indian unpeated to 40% Scottish peated, achieving the integration of Indian plateau tropical character with Scottish Islay medicinal peat that defines the Fusion house style. Bottled at 50% ABV, no-chill filtered, no added color — the same production transparency as Paul John.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Laphroaig Quarter Cask (Scottish peated, intense, maritime)',
            'connection': 'The Scottish peated malt component of Amrut Fusion comes from the same production tradition as Laphroaig — barley peated to 30–35 ppm — but the tropical Deccan Plateau aging transforms the phenolic character from coastal-salt-sea (Islay) to drier, spicier, more medicinal-warm (Bangalore); Fusion demonstrates how geography of aging rather than malting determines ultimate spirit character'
        },
        {
            'tradition': 'Paul John Bold (same Indian single malt category, different coastal terroir)',
            'connection': 'Amrut Fusion and Paul John Bold represent the two great Indian peated single malts from opposite Indian geographical positions: Paul John from humid Goa coastal tropical on Portuguese colonial land, Amrut from drier Bangalore Deccan Plateau at 920m — the same Indian barley and Scottish peated malt producing fundamentally different spirits through aging geography alone'
        },
        {
            'tradition': 'Japanese Nikka From the Barrel (blended complexity, non-conventional)',
            'connection': 'Amrut Fusion and Nikka From the Barrel both achieve complexity through thoughtful blending of complementary components (Indian+Scottish malt for Amrut, pot still malt+continuous grain for Nikka), and both received landmark critical recognition that legitimized their respective categories internationally at key historical moments'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep gold to light amber from ex-bourbon tropical aging; clear at room temperature with natural slight haze possible when cold from no-chill filtration; good viscosity at 50% ABV',
        'nose': 'Complex dual-wave: Indian spice (cardamom, white pepper from six-row barley) and Deccan Plateau dried tropical fruit (raisin, fig), vanilla from American oak — then the Scottish peat arrives in a second wave: tarry, medicinal, sea salt; the two components present distinctly before integrating over 15 minutes in glass',
        'palate': 'Full body from no-chill filtration, spiced fruit-chocolate mid-palate from the Indian component, then the peated wave with medicinal-salt-smoke complexity, long warm finish alternating fruit-sweetness and peat-smoke persistence — the integration of tropical and cold-maritime character in a single expression'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Amrut Indian Single Malt (Unpeated)',
            'criteria': 'The unpeated Indian barley-only expression at 46% — the purest Deccan Plateau terroir expression without Scottish peat; less complex than Fusion but shows the Indian plateau character transparently'
        },
        {
            'tier': 2,
            'tier_name': 'Amrut Fusion (50%)',
            'criteria': 'The internationally-recognized 97-point expression: Indian unpeated + Scottish peated vatting at 50% no-chill filtered — the benchmark of the Indian single malt category'
        },
        {
            'tier': 3,
            'tier_name': 'Amrut Naarangi (Orange Wine Cask)',
            'criteria': 'Amrut Indian malt finished in ex-Naarangi (Indian orange wine) casks — adding citrus-wine complexity from domestically produced wine casks available nowhere else in the world whisky market'
        },
        {
            'tier': 4,
            'tier_name': 'Amrut Kadhambam (Multi-Cask Sequential Finish)',
            'criteria': 'Indian single malt finished sequentially in rum casks, then Port casks, then brandy casks, then sherry casks — four-stage finishing producing extraordinary layered complexity; available only through specialist import'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature 20–22°C; 5–10ml of water opens the Fusion dramatically — the standard whisky dilution technique here reveals the construction of the blend rather than simply softening it',
        'vessel': 'Glencairn or tulip to concentrate the layered Indian-then-peat aromatic presentation; wide-open wine glass acceptable for exploring the aromatic complexity over 20–30 minutes of slow reveal',
        'comparative_tasting': 'Optimal PCT-themed service alongside Paul John Brilliance (unpeated Goa) and Paul John Bold (peated Goa) — the three whiskies form a comparative study of how different Indian geographical positions produce fundamentally different spirits under the "Indian single malt" category'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Amrut Distilleries — Fusion is the internationally recognized benchmark; 97-point Jim Murray score (2010) remains the most significant critical validation in the Indian single malt category',
        'north_america_access': 'BCLDB standard stock (Amrut Fusion and Peated); LCBO Ontario; Spec\'s Texas; K&L Wine Merchants California; full range at Vancouver specialty spirits retailers',
        'culinary_application': 'Amrut Fusion creates a compelling pairing with Indian-spiced preparations where the whisky\'s inherent Indian spice register resonates with curry leaf, cardamom, and black pepper; the peat component integrates with smoked preparations — a Fusion Old Fashioned alongside smoked Pacific salmon creates the Pacific-Indian flavor bridge that defines PCT cross-tradition thinking'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
