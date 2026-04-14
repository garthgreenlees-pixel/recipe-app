import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Dominican Republic — Santiago and Puerto Plata (Brugal Extra Viejo, Sugarcane Norte Cibao Lowlands)',
    output_dir='.',
    starting_entry=1,
    session_number=36,
    running_total=102
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Brugal & Co. — Distilería San Felipe',
    'location': 'Puerto Plata, Dominican Republic',
    'description': 'Andrés Brugal Montaner founded Brugal in 1888 in Puerto Plata on the Dominican Republic\'s northern coast, establishing what would become the country\'s dominant rum producer and one of the Caribbean\'s most historically significant distilleries. Brugal operates continuous multi-column stills (the most technologically sophisticated light rum production in the Caribbean) and ages in a combination of ex-bourbon and ex-sherry American white oak barrels in the company\'s Puerto Plata warehouses. Brugal is notable for the dryness of its style — a deliberate production choice distinguishing Dominican Republic rum from the sweeter profiles of Barbados, Jamaica, or Guatemala. The Extra Viejo (launched 1965) is the most critically regarded expression, combining the DR\'s light column-still distillate character with extended ex-bourbon and ex-sherry aging of 3–8 years. Brugal was acquired by Edrington Group (owners of The Macallan, Highland Park) in 2008, which has brought significant investment in quality and transparency to the brand.',
    'founded': '1888',
    'region': 'Puerto Plata, Dominican Republic',
    'website': 'brugal.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Edrington Americas — Brugal US and Canada',
    'type': 'importer',
    'description': 'Brugal is distributed in the US and Canada through Edrington\'s Americas distribution network — the same system that handles The Macallan and Highland Park in North America. Widely available in all major US markets; in Canada through LCBO and BCLDB; Brugal Extra Viejo is standard-stocked at most premium spirits retailers in BC and Ontario.',
    'markets_served': ['US', 'Canada', 'EU', 'Caribbean'],
    'traditions_carried': ['spirits'],
    'website': 'brugal.com',
    'verified': True
})

session.add_beverage({
    'name': 'Brugal Extra Viejo — Dominican Republic Light Rum, Dry Style, Ex-Bourbon and Sherry Oak',
    'category': 'spirits',
    'subcategory': 'rum_aged',
    'origin': 'Dominican Republic',
    'region': 'Puerto Plata, Dominican Republic',
    'producer': 'Brugal & Co. — Distilería San Felipe',
    'alcohol_content': 38.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'The Dominican Republic produces sugar cane in the Cibao Valley — the fertile agricultural plain running east-west across the island\'s north-central region between the Cordillera Central (the island\'s highest mountain range, rising to 3,175m at Pico Duarte) and the Cordillera Septentrional along the northern coast. The Cibao Valley\'s deep alluvial soils, formed from centuries of mountain erosion, produce extraordinarily high-sucrose sugar cane in a lowland tropical climate: abundant rainfall from the Caribbean and North Atlantic (1,400–2,000mm annually), consistent warmth (26–34°C year-round), and the fertile alluvial plain provide ideal conditions for high-yield, high-sucrose molasses production. The northern coast location of Puerto Plata — where Brugal has produced rum since 1888 — provides the sea air aging environment: humidity from the Atlantic, and the trade wind exposure that maintains ventilation in the warehouse without the extreme heat of inland Caribbean aging facilities. The terroir of Dominican rum is primarily defined by the molasses substrate (high-sucrose Cibao Valley cane) and the aging environment (humid, Atlantic-influenced Puerto Plata coast) rather than the distillation character, since Brugal\'s multi-column stills produce a very light, neutral distillate that derives most of its character from barrel aging rather than fermentation congeners.'
    ),
    'production_technique': (
        'Brugal uses molasses from Cibao Valley sugar estates, fermented in closed stainless steel tanks for 24–36 hours with a domesticated Saccharomyces cerevisiae strain. The multi-column distillation system at San Felipe includes both a beer still column and a rectifying column, producing a clean, light distillate at 95–96% ABV — even cleaner than Angostura\'s 200-plate still output. The light distillate enters ex-bourbon American white oak barrels (180–220 litres) at 62–65% for tropical aging at Puerto Plata. The Extra Viejo blend uses rums aged 3–8 years in a combination of first-fill ex-bourbon (for vanilla-coconut character) and ex-sherry American oak (for dried fruit and nut complexity). The blending philosophy at Brugal distinguishes it from sweeter Caribbean styles: master blender Jassil Villanueva deliberately produces a drier, less sweet profile (residual sugar below 5 g/L, confirmed by Edrington\'s transparency reporting) — emphasizing the oak-derived complexity rather than sweetness. The Brugal house style is the driest major aged rum in the Caribbean: less sweet than Angostura 1919, significantly less sweet than Zacapa XO, and more similar in structural dryness to a well-aged Irish whiskey than to the conventional sweet rum profile. Bottled at 38% ABV — lower than most Caribbean premium rum — reflecting the Dominican tradition of lower-proof service.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Irish single pot still whiskey (dry, grain-forward, medium body)',
            'connection': 'Brugal Extra Viejo\'s deliberate dryness and medium body occupy a similar tasting register to Irish pot still whiskey — Green Spot, Redbreast at lower ages — both prioritizing the dry oak-grain character over sweetness or fruit intensity, making them the "food-friendly" alternatives to their more indulgent category counterparts'
        },
        {
            'tradition': 'Foursquare Barbados (additive-free transparency, oak-forward character)',
            'connection': 'Brugal Extra Viejo and Foursquare share the Caribbean light-to-medium rum category defined by transparency and dryness, though from opposite distillation philosophies: Brugal from ultra-light column-only distillation achieving dryness through oak aging, Foursquare from pot-column hybrid achieving complexity through both distillation congeners and extended aging'
        },
        {
            'tradition': 'Spanish fino Sherry (dry style in a category defined by sweetness)',
            'connection': 'Brugal Extra Viejo\'s position as the driest aged rum in a category where sweetness is the default parallels fino Sherry\'s position as the driest expression of a category dominated by sweetened cream sherries — both make the case that the most food-versatile and intellectually interesting style in their category is also the driest'
        }
    ],
    'sensory_profile': {
        'appearance': 'Light amber gold; clear; lighter color than equivalent-age Caribbean rums from the combination of light distillation and relatively short aging; excellent clarity without visible sediment',
        'nose': 'Elegant and restrained: vanilla from ex-bourbon, dried fruit (raisin, dried apricot from sherry cask), light caramel, faint coconut, dried tobacco leaf — the dryness of the house style is immediately evident in the absence of the candied-sweet note of most light aged Caribbean rums; clean and dignified rather than exuberant',
        'palate': 'Light-medium body, dry entry (under 5 g/L residual sugar evident immediately), oak tannin present but gentle, vanilla-dried fruit mid-palate, clean dry finish with minimal sweetness — the driest premium aged rum in the Caribbean portfolio; very long oak-mineral finish without the cloying sweetness of the category\'s industrial expressions'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Brugal Especial (White Rum)',
            'criteria': 'The unaged mixing rum base; filtered for clarity, minimal congener content from multi-column distillation — the Dominican standard for cocktail use'
        },
        {
            'tier': 2,
            'tier_name': 'Brugal Extra Viejo',
            'criteria': 'The flagship aged expression: 3–8 year ex-bourbon and ex-sherry blend, dry style under 5 g/L residual sugar, 38% ABV — the benchmark for dry Dominican rum'
        },
        {
            'tier': 3,
            'tier_name': 'Brugal 1888 (Dual Cask)',
            'criteria': 'Extended aging in American bourbon casks followed by Spanish oak Sherry casks — more complex oak layering than Extra Viejo at a higher price point; the premium tier'
        },
        {
            'tier': 4,
            'tier_name': 'Brugal Papá Andrés (Ultra-Premium Reserve)',
            'criteria': 'The ultra-premium limited release from the oldest barrels in the Brugal heritage cellar — natural color, single identified barrels, priced at collector level; fewer than 1,000 units per release'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature 18–20°C for neat service; the dryness works well with minimal dilution; a single ice cube is acceptable but unnecessary for the Extra Viejo at 38%; the Especial white rum is specifically designed for cocktail use at any temperature',
        'vessel': 'Rocks glass or tulip for neat service; highball for rum-and-soda (the Dominican national drink: Brugal Especial + soda water + lime); the Extra Viejo works in a rum Old Fashioned where the dryness creates a whiskey-adjacent cocktail profile',
        'food_pairing_philosophy': 'Brugal Extra Viejo\'s dryness makes it the most food-versatile premium rum in the Caribbean — the low residual sugar does not conflict with savory preparations the way sweeter rums do; works as a digestive alongside aged cheese and charcuterie where Zacapa XO would be overwhelming'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Brugal & Co. — Extra Viejo is the benchmark for dry, clean Dominican Republic aged rum; the Edrington acquisition ensures transparency and quality investment going forward',
        'north_america_access': 'Edrington Americas distribution through all major North American markets; BCLDB and LCBO standard stock; Total Wine, BevMo California; the Extra Viejo is one of the most accessible premium aged Caribbean rums at approximately $30–35 CAD retail',
        'culinary_application': 'Extra Viejo\'s dryness makes it an outstanding cooking rum for deglazing pans in the way a dry sherry or brandy would be used: Dominican-style seafood rice preparations, rum-and-citrus marinades for fish, Caribbean escabeche where the dry rum provides the acid vehicle without added sweetness; the low residual sugar is essential for recipes where sweetness balance matters'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region('coffee', 'Brazil — Bahia (Chapada Diamantina Highlands, São Desidério Cerrado Baiano, Atlantic Forest Coffee)')

session.add_producer({
    'tradition': 'coffee',
    'name': 'Fazenda Santa Alina — Barra, Bahia',
    'location': 'Barra, Bahia, Brazil',
    'description': 'Fazenda Santa Alina operates in the western Bahia cerrado zone — the savanna lowlands surrounding the town of Barra in the São Francisco River valley, at 800–950m elevation. The Bahia cerrado (locally called the "Cerrado Baiano" or "Oeste Baiano") is the westernmost frontier of Brazilian specialty coffee cultivation, producing coffees in a semi-arid subtropical climate where irrigation from the São Francisco River aquifer system is essential. The farm produces both natural and pulped-natural coffees from Catuaí and Bourbon variety trees, targeting the 85–88 point commercial specialty range for export.',
    'founded': '1990s',
    'region': 'Bahia, Brazil',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'coffee',
    'name': 'Finca Ibiraba — Chapada Diamantina Highland Cooperative',
    'location': 'Mucugê and Abaíra municipalities, Chapada Diamantina, Bahia, Brazil',
    'description': 'Cooperative of smallholder producers in the Chapada Diamantina — the spectacular highland plateau of central Bahia at 1,000–1,200m elevation, designated a National Park (PARNA Chapada Diamantina, 152,000 hectares). The Chapada\'s quartzite and granite geology, combined with the semi-arid climate moderated by altitude, produces coffees of unusual clarity and delicate citrus acidity — the signature "diamond terroir" character that distinguishes Chapada Diamantina from the heavier-bodied Sul de Minas and Cerrado Mineiro styles. The high-altitude semi-arid production environment is unique in Brazilian coffee: it is the closest Brazilian approximation to Ethiopian or Colombian highland coffee growing conditions.',
    'founded': '2005 (cooperative formation)',
    'region': 'Chapada Diamantina, Bahia, Brazil',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Brazil Chapada Diamantina Washed Catuaí — Quartzite Highlands 1,100m, Delicate Citrus, Atlantic Forest Edge',
    'category': 'coffee',
    'subcategory': 'washed_process',
    'origin': 'Brazil',
    'region': 'Chapada Diamantina, Bahia, Brazil',
    'producer': 'Finca Ibiraba — Chapada Diamantina Highland Cooperative',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Chapada Diamantina (Diamond Plateau) is Brazil\'s most geologically distinctive coffee-growing region — a 1,200km² quartzite sandstone plateau rising abruptly from the Bahia semi-arid backlands (sertão) to elevations of 1,000–1,600m. The plateau was formed by Precambrian quartzite and sandstone formations, creating some of the oldest and most mineralogically unique soils in Brazilian agriculture: the quartzite-derived sandy soils are extremely nutrient-poor (necessitating organic amendment), highly acidic (pH 4.5–5.5), and remarkably well-drained due to the sandstone fracture network. The resulting terroir is unlike any other Brazilian coffee-growing zone: the combination of nutrient-limited sandy quartzite soils, high altitude (1,000–1,200m), the semi-arid Bahia climate moderated by plateau altitude, and the Atlantic Forest transition zone ecosystems creates a growing environment closer to Ethiopian or Colombian highland coffee conditions than to the classic Minas Gerais Brazilian profile. The Chapada Diamantina produces coffees with significantly higher acidity than Sul de Minas or Cerrado — delicate citrus (yellow peach, lemon, tangerine) rather than the chocolate-caramel baseline — from the same Catuaí and Bourbon varieties that produce rich, low-acid coffees in the warmer, lower-altitude Minas Gerais zones. The altitude and sandstone geology create the longest ripening cycle in Brazilian coffee production, with harvest extending into September-October (later than any other Brazilian zone), producing exceptional sucrose concentration in the cherry.'
    ),
    'production_technique': (
        'Chapada Diamantina washed production is the exception in Brazil — where the vast majority of production uses natural or pulped-natural processing, Chapada\'s semi-arid highland climate creates ideal conditions for the washed process (full depulping and fermentation in water) that is standard in Ethiopia and Colombia but rare in Brazil. Finca Ibiraba cooperative members harvest Catuaí by selective hand-picking, brought to the cooperative processing station where the cherries are de-pulped within 4 hours of harvest. The de-pulped parchment is fermented in tanks for 18–24 hours — shorter fermentation than Ethiopian washed coffees due to the drier Chapada climate reducing the spontaneous microbial diversity — then washed through clean water channels and transferred to raised drying beds. The Chapada\'s dry highland climate enables raised-bed sun drying for 15–18 days without the excessive moisture that would trigger mold in the more humid Minas Gerais zones. The resulting washed Chapada coffee is Brazil\'s closest approximation to the "clean, bright, acidic" coffee profile that specialty roasters source from Ethiopia and Colombia — a fundamentally different cup character from the dominant Brazilian natural-process style. The cooperative QC cupper targets 87–89 points for the specialty lot minimum, with the best micro-lots achieving 90+ points that qualify for Brazil Cup of Excellence submission.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Ethiopia Yirgacheffe Washed (citrus-floral, highland quartzite)',
            'connection': 'Chapada Diamantina washed Catuaí and Yirgacheffe washed Heirloom are the closest cup-character parallels across different continents: both produce citrus-delicate, floral-bright washed coffees from high-altitude soils derived from ancient crystalline rock (quartzite for Chapada, gneiss for Yirgacheffe) — Chapada is Brazil\'s answer to the Ethiopian washed coffee profile'
        },
        {
            'tradition': 'Colombia Huila Washed (altitude-citrus, contrasting Brazilian normal)',
            'connection': 'The Chapada washed contradicts the expectation that Brazilian coffee is always chocolatey, low-acid, and natural-processed — demonstrating that when Brazilian coffee grows in the right altitude-terroir combination (quartzite plateau, 1,100m, semi-arid), it produces coffees structurally indistinguishable from Andean highland Colombia Huila: bright citrus, clean cup, delicate floral mid-palate'
        },
        {
            'tradition': 'Brazil Sul de Minas Natural (same country, opposite terroir)',
            'connection': 'Chapada Diamantina washed and Sul de Minas natural represent the maximum poles of Brazilian specialty coffee terroir: Sul de Minas produces full-bodied, chocolatey, fruit-forward naturals from granite-clay volcanic soils; Chapada produces bright, acidic, delicate washeds from nutrient-poor quartzite sandstone soils — demonstrating that Brazilian coffee is not a monolithic flavor profile but a continental diversity'
        }
    ],
    'sensory_profile': {
        'appearance': 'Clear, light to medium amber; washed process produces higher clarity than natural; medium body visible in the brew; delicate crema in espresso from the lighter congener load of washed processing',
        'nose': 'Citrus-forward and delicate: yellow peach, tangerine peel, jasmine, lemon blossom, very light brown sugar from the natural sweetness of the highland Catuaí variety — completely unexpected from a Brazilian origin; if served blind, would be identified as Colombian or Ethiopian by most specialty coffee professionals',
        'palate': 'Light-medium body (the quartzite sandstone mineral terroir produces less body than the volcanic-clay Minas Gerais coffees), bright malic-citric acidity unusual for Brazil, clean citrus fruit mid-palate, clean finish without the chocolate-caramel baseline of Sul de Minas — a coffee that challenges Brazilian coffee identity assumptions'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Bahia Commercial (Cerrado Baiano natural)',
            'criteria': 'Western Bahia lowland cerrado production at 800–950m, mechanical harvest natural process — the standard commercial Bahia grade with chocolatey-nutty Sul de Minas-adjacent character'
        },
        {
            'tier': 2,
            'tier_name': 'Chapada Diamantina Cooperative Washed (87–89 points)',
            'criteria': 'Finca Ibiraba and similar cooperative production from the Chapada highland quartzite zone, full washed process, Q-grader cupped 87–89 — the distinctive citrus-delicate Chapada character at accessible specialty pricing'
        },
        {
            'tier': 3,
            'tier_name': 'Chapada Diamantina Micro-Lot (89–91 points)',
            'criteria': 'Individual farm micro-lots from named Chapada producers, exceptional vintage character, 89+ points — available through direct-trade roasters sourcing the Chapada zone as an alternative-to-Colombia option'
        },
        {
            'tier': 4,
            'tier_name': 'Chapada Cup of Excellence (92+ points)',
            'criteria': 'Brazil COE lots from the Chapada zone achieving jury-verified 92+ points — the rare occasion when a Brazilian coffee achieves the acidity and delicacy scores that Ethiopian and Colombian coffees routinely achieve; represents the frontier of the Chapada terroir\'s potential'
        }
    ],
    'service_intelligence': {
        'temperature': 'Filter: 92–93°C pour-over (lower than Sul de Minas to preserve delicate citrus aromatics); V60 or Chemex recommended; serve at 65–70°C and allow to cool to 55°C for best citrus expression — the delicate Chapada character is heat-sensitive',
        'vessel': 'Ceramic pour-over cup or clean glass cup that does not add metallic interference; the light-medium body does not need heat retention as much as the heavier Sul de Minas naturals',
        'roast_profile': 'Light roast (City level) is essential for Chapada washed to preserve the unusual citrus-delicate character; medium roast immediately converts the citrus to caramel-chocolate and makes the coffee indistinguishable from standard Brazilian; avoid dark roast entirely'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Finca Ibiraba cooperative and individual Mucugê farms — the consistent Chapada Diamantina specialty zone; niche but growing recognition among specialty roasters seeking Brazilian coffee with non-standard profiles',
        'north_america_access': 'Rare in North America — Counter Culture Coffee (Durham NC) and Heart Coffee Roasters (Portland OR) have sourced Chapada Diamantina; in Vancouver, Nemesis Coffee and 49th Parallel occasionally feature Chapada lots; extremely limited availability compared to Sul de Minas',
        'culinary_application': 'Chapada washed citrus character makes it an outstanding cold brew concentrate for cocktail applications where Ethiopian-style coffee is traditionally used: espresso martini, coffee tonic (cold brew + tonic water + lemon), and food pairings where the bright acidity provides the acid element in a preparation (coffee-cured gravlax uses Chapada cold brew as the acid rather than lemon in the most modern applications)'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
