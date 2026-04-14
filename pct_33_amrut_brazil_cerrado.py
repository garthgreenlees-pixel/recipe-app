import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='India — Bangalore Karnataka (Amrut Single Malt, Tropical Aging Pioneer, 920m Elevation)',
    output_dir='.',
    starting_entry=1,
    session_number=34,
    running_total=100
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Amrut Distilleries — Bangalore',
    'location': 'Bangalore, Karnataka, India',
    'description': 'Founded 1948 as a spirit alcohol producer for industrial purposes, Amrut began single malt whisky production in 1987 and released its first internationally exported single malt in 2004 — the first Indian whisky to be exported to the UK and distributed internationally as a single malt in direct competition with Scotch. In 2010, Amrut Fusion (a blend of Indian unpeated and Scottish peated malt) received 97 points from whisky critic Jim Murray in his Whisky Bible — the first time a non-Scotch, non-Japanese whisky had received a score comparable to the world\'s best malts. The Bangalore distillery sits at 920m elevation in the Deccan Plateau — the same basaltic plateau that underlies the Nashik wine region to the northwest — in a climate very different from the humid Goa terroir of Paul John: dry tropical with a distinct cool season (November–February, 15–22°C) that creates slower-but-still-accelerated barrel maturation compared to Scotland. Amrut ages exclusively at Bangalore rather than using altitude facilities, producing a tropical-single-malt character that is distinctly different from the coastal-tropical character of Goa-produced Paul John.',
    'founded': '1948 (industrial); single malt 1987',
    'region': 'Bangalore, Karnataka, India',
    'website': 'amrutdistilleries.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Amrut Global — US and Canadian Distribution',
    'type': 'importer',
    'description': 'Amrut is imported to the US through John Emerald Distilling\'s import arm and Anchor Distilling (for some expressions). In Canada through Fine Estate Wines and Spirits (BC) and LCBO (Ontario). The Amrut Fusion and Amrut Peated are standard stock at BCLDB; Naarangi, Kadhambam, and special releases through private import and specialist retailers.',
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
        'The Amrut Distillery sits at 920m elevation on the Deccan Plateau — the ancient basaltic lava plateau that covers much of peninsular India and represents one of the largest volcanic geological formations on Earth. The Deccan Traps (the Indian name for this formation) were created by massive volcanic eruptions approximately 66 million years ago, producing basaltic rock of extraordinary mineral richness that has weathered over millions of years into India\'s characteristic black cotton soils (regosol). Bangalore\'s specific climate on the Deccan Plateau is drier and cooler than the Goa coastal climate: the city experiences a distinct cool dry season from November to February (15–22°C) and a hot dry season from March to May (28–35°C) before the monsoon (June–September). This bimodal temperature pattern creates a different barrel maturation profile than the consistently warm coastal climate: the cool dry season slows barrel extraction significantly, while the hot pre-monsoon season accelerates it — producing a cycle of "fast" and "slow" extraction that may contribute to the layered complexity observed in Amrut\'s aged expressions. The 920m altitude produces lower oxygen partial pressure than sea level, which affects both the fermentation (slightly slower yeast respiration) and the barrel aging (different oxidation rate). Amrut ages its Fusion expression at Bangalore altitude — angel\'s share is 8–10% per year, lower than Paul John in humid Goa (10–12%) but significantly higher than Scottish 2%. The Indian six-row barley used for the unpeated component is grown in Rajasthan and Haryana under similar latitude and climate conditions to Egyptian barley — the Indian subcontinental barley expresses a spicier, more grain-assertive character than the two-row Scottish barley used for the Fusion\'s peated component.'
    ),
    'production_technique': (
        'Amrut Fusion is a vatting of two separately distilled and aged whiskies: Indian unpeated malt (from Rajasthan/Haryana six-row barley, milled and mashed at Bangalore, distilled in Amrut\'s copper pot stills) and Scottish peated malt (barley malted at Crisp Malt or Bairds in Scotland, specifically at 30–35 ppm phenol level, shipped to Bangalore as malted grain for distillation). The Scottish peated malt component retains its Islay-style phenolic character from malting despite being distilled and aged in India — the phenols survive distillation and barrel contact, contributing the medicinal-coastal peat note that Islay single malts achieve through smoking barley over local peat. Both components are independently distilled in Amrut\'s pot stills and aged separately: the Indian unpeated in ex-bourbon American oak casks, the Scottish peated in a combination of ex-bourbon and ex-sherry casks. After the target aging period (typically 4–6 years per component), the two aged whiskies are vatted at a ratio approximately 60% Indian unpeated to 40% Scottish peated, creating the Fusion. The result achieves the integration of Indian plateau tropical character (spice, dried fruit, coconut from American oak) with Scottish Islay medicinal peat (tar, sea air, antiseptic) in a combination that neither pure Indian nor pure Scottish expression can produce. The 50% ABV non-chill filtered bottling preserves the natural body and slight haze from long-chain fatty acids at cold temperatures — the same transparency policy as Paul John.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Laphroaig Quarter Cask (Scottish peated, intense, complex)',
            'connection': 'The Scottish peated malt component of Amrut Fusion comes from the same production tradition as Laphroaig — barley peated to 30–35 ppm in Scotland — but the tropical Deccan Plateau aging transforms the phenolic character from the coastal-salt-sea character of Islay to a drier, spicier, more medicinal-warm expression; Fusion demonstrates how geography of aging rather than geography of malting determines ultimate spirit character'
        },
        {
            'tradition': 'Paul John Bold (same category, different Indian terroir)',
            'connection': 'Amrut Fusion and Paul John Bold represent the two great Indian peated single malts from different geographic and geological positions: Paul John from the humid Goa coastal tropical environment on Portuguese colonial land, Amrut from the drier Bangalore Deccan Plateau at 920m — the same Indian six-row barley and Scottish peated malt producing fundamentally different spirits based on their aging geography'
        },
        {
            'tradition': 'Japanese Nikka From the Barrel (blended, complex, non-convention)',
            'connection': 'Amrut Fusion and Nikka From the Barrel both challenge the convention that great whisky must be from a single country, single grain, or single aging environment — both achieve complexity through thoughtful blending of complementary components (Indian+Scottish for Amrut, pot still malt+continuous still grain for Nikka), and both received critical recognition that legitimized their respective categories internationally at key historical moments'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep gold to light amber from ex-bourbon tropical aging; clear at room temperature with natural slight haze possible at cold temperatures from no-chill filtration; good viscosity at 50% ABV',
        'nose': 'Complex and immediately compelling: Indian spice (cardamom, white pepper from the six-row barley character), Deccan Plateau dried tropical fruit (raisin, fig), vanilla from American oak, then the unmistakable Scottish peat arrives in the second wave — tarry, medicinal, sea salt — the two components presenting distinctly before integrating; the interaction between tropical fruit sweetness and Islay-style peat smoke is unique to this expression',
        'palate': 'Full body from no-chill filtration, spiced fruit-chocolate mid-palate from the Indian component, then the peated wave arrives with medicinal-salt-smoke complexity, long warm finish with alternating fruit-sweetness and peat-smoke persistence — the 97-point character is in this integration: neither component overwhelms the other'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Amrut Indian Single Malt (Unpeated)',
            'criteria': 'The unpeated Indian barley-only expression at 46% — the purest Deccan Plateau terroir expression without Scottish peat intervention; less complex than Fusion but shows the Indian terroir transparently'
        },
        {
            'tier': 2,
            'tier_name': 'Amrut Fusion (50%)',
            'criteria': 'The internationally-recognized 97-point expression: Indian unpeated + Scottish peated vatting — the benchmark of the category'
        },
        {
            'tier': 3,
            'tier_name': 'Amrut Naarangi (Orange Wine Cask)',
            'criteria': 'Amrut Indian malt finished in ex-Naarangi (Indian orange wine) casks — using domestically produced wine casks for final aging, adding citrus-wine complexity to the Indian single malt base; a distinctly Indian finishing cask available nowhere else'
        },
        {
            'tier': 4,
            'tier_name': 'Amrut Kadhambam (Rum, Port, Brandy, and Sherry Multi-Cask)',
            'description': 'The most complex Amrut expression: Indian single malt finished sequentially in rum casks, then Port casks, then brandy casks, and finally sherry casks — four-stage finishing producing extraordinary layered complexity; available only through specialist import'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature 20–22°C; 5–10ml of water opens the Fusion dramatically by reducing the peated-Indian integration to its component parts before reintegrating in the glass — the standard whisky dilution technique here reveals the construction of the blend rather than simply softening it',
        'vessel': 'Glencairn or tulip; the Fusion benefits from nose concentration to appreciate the layered Indian-then-peat presentation; wide-open wine glass acceptable if exploring the aromatic complexity over 20–30 minutes of slow reveal',
        'comparative_tasting': 'The optimal Amrut Fusion service for a PCT-themed tasting is alongside Paul John Brilliance (unpeated Goa) and Paul John Bold (peated Goa) — the three whiskies form a comparative study of how different Indian geographical positions (920m Deccan Plateau vs sea-level Goa tropical) and production choices (Indian+Scottish peat blend vs Indian single barley pure) produce fundamentally different spirits under the same "Indian single malt" category'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Amrut Distilleries — Fusion and Naarangi are the internationally recognized benchmark expressions; 97-point Jim Murray score (2010) remains the most significant critical validation in the Indian single malt category\'s history',
        'north_america_access': 'BCLDB standard stock (Amrut Fusion and Peated); LCBO Ontario; Spec\'s Texas; K&L Wine Merchants California; The Whisky Exchange online shipping internationally; Vancouver specialty spirits retailers stock the full range',
        'culinary_application': 'Amrut Fusion at 50% creates a compelling pairing with Indian-spiced preparations where the whisky\'s inherent Indian spice register resonates with curry leaf, cardamom, and black pepper; the peat component integrates with smoked preparations — a Fusion Old Fashioned alongside smoked duck or smoked Pacific salmon creates the Pacific-Indian flavor bridge that defines PCT cross-tradition thinking'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('coffee', 'Brazil — Cerrado Mineiro (Patrocínio, Altitude Savanna, Mechanical Harvest Natural Process)')

session.add_producer({
    'tradition': 'coffee',
    'name': 'Fazenda Samambaia — Patrocínio, Cerrado Mineiro',
    'location': 'Patrocínio municipality, Cerrado Mineiro, Minas Gerais, Brazil',
    'description': 'Fazenda Samambaia is a 600-hectare estate in the Cerrado Mineiro — the high-altitude savanna zone of western Minas Gerais that produces a distinctly different style of Brazilian coffee from the mountainous Sul de Minas: flatter, drier topography at 1,000–1,200m elevation on the Cerrado plateau, with a longer dry season that concentrates sugars in the coffee cherry and enables reliable mechanical harvesting. The Cerrado Mineiro was the first Brazilian coffee region to receive a Geographical Indication (GI) from the Brazilian INPI in 2005, establishing the region\'s identity separate from the broader Minas Gerais designation. Fazenda Samambaia has been a multiple Cup of Excellence winner and consistently produces coffees above 88 points from the Cerrado\'s distinctive terroir.',
    'founded': '1960s',
    'region': 'Patrocínio, Cerrado Mineiro, Minas Gerais, Brazil',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Brazil Cerrado Mineiro Pulped Natural — Patrocínio GI, Flat Savanna 1,100m, Caramel Chocolate Profile',
    'category': 'coffee',
    'subcategory': 'pulped_natural_process',
    'origin': 'Brazil',
    'region': 'Cerrado Mineiro, Minas Gerais, Brazil',
    'producer': 'Fazenda Samambaia — Patrocínio, Cerrado Mineiro',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Cerrado Mineiro sits on the Brazilian Central Plateau at 900–1,250m elevation — a flat-to-gently-rolling savanna landscape that contrasts sharply with the steep, mountainous Sul de Minas terrain. The Cerrado biome is characterized by distinctive vegetation: twisted, fire-resistant savanna trees (cerrado sensu stricto), extensive grassland, and gallery forests along the watercourses. Annual rainfall is concentrated in a 6-month wet season (October–March) with a remarkably dry 6-month dry season (April–September) — a bimodal pattern that is more pronounced than Sul de Minas and creates reliable, predictable drying conditions for natural and pulped-natural processing. The flat topography and reliable dry season make Cerrado Mineiro the primary zone for mechanized harvesting in Brazilian specialty coffee: the terrain allows strip-pick mechanical harvesting machines that operate efficiently on flat land, reducing labor costs while maintaining acceptable quality at the 87–90 point tier (compared to the 90+ point handpicked tier achievable only in the steeper Sul de Minas). The soils of the Cerrado plateau are deep red latosol over weathered Precambrian basement rock — poor in nutrients but excellent in drainage and depth, providing the long root access to subsoil water reserves that coffee plants require during the dry season. The basaltic mineral composition of the basement rock contributes iron and manganese to the soil that the coffee plant absorbs, contributing to the distinctly clean, sweet cup character of Cerrado Mineiro — different from the more complex, acidic Sul de Minas character.'
    ),
    'production_technique': (
        'Fazenda Samambaia uses mechanical strip-pick harvesting during the July–September dry season, deploying Brastoft harvesting machines on the flat Cerrado terrain. The mechanical harvesting removes all cherries (ripe, underripe, and overripe) simultaneously from each tree pass — the quality is maintained through selective field management (multiple passes at staggered ripeness) and through post-harvest flotation sorting that separates overripe and damaged cherries from ripe by density. The farm uses the pulped-natural process — a Brazilian innovation that has largely replaced traditional dry natural processing in the Cerrado: cherries are passed through a depulper that removes the outer cherry skin but leaves the mucilage (the sticky sugar layer between skin and parchment) intact on the parchment bean. The mucilage-covered parchment is then transferred to raised drying beds or cemented terraces and dried for 15–18 days, turning every 4 hours during peak daylight. The mucilage ferments gently during drying, contributing soft fruit acids and a residual sweetness to the parchment that transfers to the green bean and ultimately to the cup. The result: more sugar-sweetness and body than a fully washed coffee (no mucilage) but less wild-fruit intensity than a full natural (whole cherry drying). The pulped natural process from the Cerrado produces the characteristic "classic Brazilian" profile of chocolate, caramel, and nut that has made Brazil the world\'s preferred espresso base by volume for 50+ years.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Brazil Sul de Minas Yellow Bourbon Natural (same country, different terroir)',
            'connection': 'Cerrado Mineiro and Sul de Minas are the definitive within-Brazil terroir contrast: Cerrado\'s flat savanna terrain produces the clean, chocolatey, commercially reliable Brazilian baseline; Sul de Minas\'s steep mountain terrain produces the fruity, complex, specialty-benchmark Brazilian ceiling — the same fermentable substrate (coffee cherry) and similar processing (natural vs pulped-natural) produces dramatically different cup profiles based entirely on altitude, terrain, and climate variation within a single state'
        },
        {
            'tradition': 'Colombian Huila Washed (clean, consistent, technically precise)',
            'connection': 'Cerrado Mineiro pulped natural and Huila washed Caturra occupy the same commercial-to-premium quality segment globally: both are the reliable, consistently clean coffees that provide the backbone of specialty roasters\' offerings — Cerrado with chocolate-caramel body, Huila with bright citrus acidity — both produced at scale with consistent mechanical or semi-mechanical processing that delivers 87–89 point quality reliably across large production volumes'
        },
        {
            'tradition': 'Ethiopian Sidama Natural (fruit process, African savanna altitude)',
            'connection': 'The Cerrado Mineiro\'s savanna altitude (cerrado biome at 1,000–1,200m) parallels Ethiopia\'s Sidama highland savanna at 1,500–2,000m in geographical type — both are high-altitude savanna coffee growing environments that produce coffees of full body with natural sweetness, the Cerrado through pulped-natural processing and the Sidama through full natural processing of indigenous Heirloom varieties'
        }
    ],
    'sensory_profile': {
        'appearance': 'Dark brown to mahogany filter brew; medium-full body visible in texture; natural process character shows as slight translucence compared to washed coffees; espresso produces a rich, persistent crema of deep chestnut color',
        'nose': 'Classic Brazilian: dark chocolate, milk chocolate, toasted almond, caramel, dried tropical fruit (very subtle from the pulped-natural mucilage contact) — clean and immediately recognizable as the "Brazilian" baseline that professional tasters identify reliably; less fruity than Sul de Minas natural, less floral than washed Colombian, more structured than full natural',
        'palate': 'Full body from the pulped-natural process (more body than washed, less than full natural), chocolate mid-palate, caramel sweetness from the mucilage fermentation residual, clean finish without fermented off-notes, low acidity — the globally preferred espresso base character: body and sweetness without acid that can fight milk or blending'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Cerrado Grade (Santos commercial export)',
            'criteria': 'Mechanical strip-pick, basic pulped natural, exported through Santos port as Brazilian commercial specialty grade — the backbone of global espresso blending at 83–86 points; reliable but undifferentiated'
        },
        {
            'tier': 2,
            'tier_name': 'Cerrado Mineiro GI Certified (87–89 points)',
            'criteria': 'Estate-certified Cerrado Mineiro GI production, careful pulped-natural processing, Q-grader cupped 87–89 — the accessible specialty tier from named farms including Fazenda Samambaia; available through direct-trade roasters'
        },
        {
            'tier': 3,
            'tier_name': 'Cup of Excellence Cerrado (89–91 points)',
            'criteria': 'Brazil COE lots from the Cerrado zone, achieving jury-verified 89+ points — the specialist tier commanding premium prices through online auction; Fazenda Samambaia and neighboring estates regularly submit winning lots'
        },
        {
            'tier': 4,
            'tier_name': 'Cerrado Experimental Processing (Natural, Anaerobic)',
            'criteria': 'Full natural or anaerobic fermentation processing from Cerrado producers experimenting beyond the traditional pulped-natural method — produces fruit-forward coffees that challenge the Cerrado\'s "clean and chocolatey" identity while demonstrating the terroir\'s flexibility'
        }
    ],
    'service_intelligence': {
        'temperature': 'Filter: 94–95°C at 60g/L (slightly stronger than typical to appreciate the body); Espresso: 93°C at 9 bars for 25 seconds; the Cerrado character is best as espresso or espresso-based preparation where the full body and chocolate-caramel profile dominates without the dilution of pour-over',
        'vessel': 'Espresso: standard demitasse; Filter: ceramic drip cup or Aeropress for concentrated body; the pulped natural process body benefits from vessels that retain heat — avoid glass cups',
        'roast_profile': 'Cerrado Mineiro peaks at medium-dark roast (Full City to Vienna): lighter roasts expose an unexpected citric acidity that is atypical and may disappoint drinkers expecting the classic Brazilian profile; the chocolate-caramel character fully develops at medium-dark and is destroyed by dark roast'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Fazenda Samambaia (Patrocínio) and Fazenda Bom Jesus (Araxá) — the consistent Cup of Excellence contenders from the Cerrado Mineiro zone',
        'north_america_access': 'Counter Culture Coffee (Durham NC) and Intelligentsia (Chicago) source Cerrado Mineiro; in Vancouver, 49th Parallel and Matchstick Coffee carry Cerrado origins seasonally; Hatch Coffee (Victoria) sources direct-trade Brazilian coffees including Cerrado',
        'culinary_application': 'Cerrado Mineiro espresso concentrate is the preferred base for dark chocolate ganache in professional pastry due to the clean chocolate-caramel profile that integrates without competing with cacao bitterness; works in Brazilian-inspired dessert preparations (brigadeiro, café com leite) where the full-bodied coffee character anchors the sweet element; the PCT connection to Portuguese colonial coffee agriculture in Brazil makes it a natural pairing with Portuguese pastéis de nata in heritage café programming'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
