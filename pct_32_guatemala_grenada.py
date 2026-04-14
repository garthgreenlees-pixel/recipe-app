import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Guatemala — Quetzaltenango Highlands (Zacapa XO Solera System, Non-Solera Truth, Elevation Aging)',
    output_dir='.',
    starting_entry=1,
    session_number=33,
    running_total=98
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Ron Zacapa — Industrias Licoreras de Guatemala (ILG)',
    'location': 'Retalhuleu (production); 2,300m Quetzaltenango aging (Las Nubes)',
    'description': 'Ron Zacapa is produced by Industrias Licoreras de Guatemala (ILG), owned by the Botran family, at their Retalhuleu facility on the Pacific coastal plain. The distillery uses a virgin sugar cane honey (miel virgen) rather than molasses — the first-press juice concentrated to a syrup — which produces a sweeter, fuller-bodied distillate than molasses-based rum. The critical aging element that defines Zacapa is the altitude: the rum is transported after initial column still distillation to the "Casa de las Nubes" (House of the Clouds) aging facility at 2,300m elevation in the highlands outside Quetzaltenango — the highest rum aging facility in the world. The extreme altitude (2,300m), cool temperatures (15–20°C vs 28–35°C at coastal rum facilities), and lower oxygen partial pressure create a dramatically different barrel aging environment than any other Caribbean or Central American rum producer. Zacapa XO is the flagship expression, though the "solera" marketing language used by Zacapa has been widely criticized as misleading — Zacapa uses a "fractional blending" system that is numerically similar to solera but not identical in operation.',
    'founded': '1976',
    'region': 'Retalhuleu (distillation) and Quetzaltenango (aging), Guatemala',
    'website': 'zacapa.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Diageo — Ron Zacapa International Distribution',
    'type': 'importer',
    'description': 'Ron Zacapa was acquired by Diageo in 2008 and is now distributed through Diageo\'s global distribution network — the same system that handles Johnnie Walker, Tanqueray, Bulleit, and other Diageo premium spirits. Widely available in all major North American markets through Diageo distributors. The premium pricing of Zacapa XO reflects Diageo\'s positioning of the brand at the ultra-premium rum tier.',
    'markets_served': ['Worldwide'],
    'traditions_carried': ['spirits'],
    'website': 'zacapa.com',
    'verified': True
})

session.add_beverage({
    'name': 'Ron Zacapa XO — Guatemala Virgin Cane Honey, 2300m Altitude Aging, Solera-Style Fractional Blending',
    'category': 'spirits',
    'subcategory': 'rum_aged',
    'origin': 'Guatemala',
    'region': 'Quetzaltenango and Retalhuleu, Guatemala',
    'producer': 'Ron Zacapa — Industrias Licoreras de Guatemala (ILG)',
    'alcohol_content': 40.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'Guatemala\'s Pacific coastal plain in Retalhuleu produces the virgin cane honey (miel virgen) — first-press sugar cane juice concentrated to syrup — that forms Zacapa\'s base: a sweeter, more complex fermentation substrate than molasses that retains more of the cane\'s natural volatile aromatics. The ILG distillery extracts cane juice from Guatemala\'s indigenous sugar cane varieties and concentrates it immediately, producing a fresh-cane-honey fermentable that lies midway between the fresh juice of rhum agricole and the molasses of most Caribbean rum. The critical terroir is the aging environment: after column still distillation at the coastal facility, Zacapa spirit travels to the Casa de las Nubes at 2,300m elevation in the Guatemalan highlands above Quetzaltenango — an altitude where the thin atmosphere and cool temperatures (daily range 12–22°C vs 26–36°C at sea level) dramatically slow barrel extraction. The 2,300m altitude creates several specific effects: reduced air pressure means the barrel wood expands and contracts less dramatically, creating slower but more even extraction; the cool temperatures preserve delicate aromatic compounds that would volatilize in tropical low-altitude aging; the higher UV exposure at altitude may drive some photochemical reactions in the aging rum not present in cellar-aged spirits. The Guatemalan highlands are at the same latitude as Jamaica and Martinique but at 10x the altitude — the resulting "cool tropical" aging environment is unique in the rum world, though several Andean spirits producers (Peruvian pisco, Bolivian singani) operate in similar altitude-aging conditions.'
    ),
    'production_technique': (
        'Zacapa\'s production begins with the miel virgen (virgin cane honey) — a clarified and concentrated cane juice syrup at approximately 65–70 Brix, far sweeter than molasses (85 Brix) but retaining more of the fresh cane aromatics lost during the molasses concentration process. The miel virgen is fermented in stainless steel tanks with a proprietary Saccharomyces cerevisiae strain for 36–48 hours, producing a wine at 12–14% ABV with distinctive fresh-cane and light tropical-fruit aromatics. Distillation occurs on a multi-plate continuous column still at the Retalhuleu facility, producing a clean neutral spirit at approximately 90% ABV. The new make spirit is transported to the Casa de las Nubes and entered into casks at 60–65% ABV for altitude aging. The Zacapa "solera" system operates as follows: barrels are organized in four tiers (American white oak ex-bourbon, Pedro Ximénez Sherry casks, Oloroso Sherry casks, and American oak) and aged rums are rotated through these wood types over periods of 6–25 years. When rum is removed from the final barrel for blending, it is replaced with rum from the next barrel down, which is refilled from the barrel below — the fractional blending principle. For Zacapa XO specifically, the blend contains rums aged from 6–25 years in the altitude warehouses, including Pedro Ximénez (dried sweet raisin-plum), Oloroso (nutty oxidative), and ex-bourbon (vanilla-caramel) cask contributions. The notable controversy: Zacapa labels indicate "between 6 and 23 years" for Centenario 23 and "XO" for the premium expression, but the actual average age of the blend is significantly lower than the maximum age stated — a common rum industry labeling practice that Zacapa employs alongside the solera-style system. Additionally, all major Zacapa expressions contain undisclosed added sugar (dosage) at significant levels (typically 15–30 g/L) that critics argue contributes more to the sweet, smooth character than the aging process itself.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Foursquare Exceptional Cask (opposite transparency philosophy)',
            'connection': 'Zacapa XO and Foursquare Exceptional Cask represent opposite philosophies in the premium rum market: Zacapa achieves sweetness and smoothness through undisclosed added sugar and solera marketing; Foursquare achieves similar sweetness and smoothness through genuine extended aging with zero additives — both produce delicious rum, but only Foursquare\'s sweetness is from the aging process rather than post-distillation sweetening'
        },
        {
            'tradition': 'PX Sherry (sweet, raisin character, Andalucian origin)',
            'connection': 'Zacapa XO\'s Pedro Ximénez cask aging contribution creates the most direct connection to Spanish Andalucian dessert wine tradition — the PX casks donate concentrated raisin-fig-treacle compounds that are genuinely present in the flavor profile beyond the added sugar base, making the PX cask character the most authentically earned element of the Zacapa XO experience'
        },
        {
            'tradition': 'Andean singani and pisco (altitude production, cool tropical aging)',
            'connection': 'Zacapa\'s 2,300m aging position places it in the same altitude-production category as Bolivian singani (minimum 1,600m production requirement) and Peruvian pisco — all three represent Andean-altitude agricultural spirits where the thin atmosphere and cool temperatures create a unique production environment compared to coastal tropical spirit production'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep amber-mahogany from the PX and Oloroso sherry cask aging; clear and viscous; the added sugar creates significant leg formation on the glass — more viscous than most 40% ABV rum expressions',
        'nose': 'Confectionery rich: dried raisin and fig from PX cask, vanilla from ex-bourbon, walnut-caramel from Oloroso, toffee and dark chocolate, faint fresh cane from the miel virgen base — the PX cask character dominates and creates an immediately identifiable dessert-rum aromatic; the nose reveals the added sugar through a faint crystalline sweetness that analytical tasters identify as separate from the aging-derived sweet compounds',
        'palate': 'Full body (enhanced by added sugar), rich sweet entry, raisin-fig-toffee mid-palate from the multiple cask types, low alcohol heat at 40%, extremely smooth finish — the smoothness is the product of both the altitude-cool aging (which produces gentler tannin integration) and the added sugar (which coats the palate and masks any remaining rough edges)'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Zacapa Centenario 23',
            'criteria': 'The widely distributed Centenario 23 expression: same altitude aging system, blend of 6–23 year rums, Pedro Ximénez and ex-bourbon influence — the accessible super-premium expression that built Zacapa\'s international reputation'
        },
        {
            'tier': 2,
            'tier_name': 'Zacapa XO',
            'criteria': 'The flagship: additional Oloroso Sherry cask aging and higher average age in the blend; more complex three-wood (PX, Oloroso, ex-bourbon) integration; ultra-premium pricing'
        },
        {
            'tier': 3,
            'tier_name': 'Zacapa Royal',
            'criteria': 'Limited release expression from the oldest barrel selections in the Casa de las Nubes; very small production at ultra-premium price — the collector tier of the ILG portfolio'
        },
        {
            'tier': 4,
            'tier_name': 'Single-Cask Unblended (if ever released)',
            'criteria': 'The aspirational tier: a single identified cask from the 2,300m facility without blending or added sugar would reveal the altitude-aging character of the miel virgen spirit without the added-sugar smoothing — not currently commercially available but theoretically represents the highest transparency expression of the Zacapa terroir'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature 18–20°C; never chill which masks the PX raisin aromatic; works well neat or with one ice sphere that slowly dilutes and reveals additional complexity; the added sugar creates a naturally low-alcohol-burn profile that makes it genuinely consumable straight without ice for most drinkers',
        'vessel': 'Rocks glass or snifter; the full-body sweetness of XO benefits from a wide glass that allows aromatic dispersion rather than concentration; large brandy snifter (warmed in palm) works well to maximize the PX-Oloroso aromatic profile',
        'cocktail_applications': 'Zacapa XO\'s sweetness means it requires no additional sugar in rum cocktail applications — a Zacapa Old Fashioned uses only bitters and a single ice sphere with no sugar syrup; a Zacapa Negroni variant (substitute XO for vermouth) uses the natural sweetness to replace the sweet vermouth component entirely'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Ron Zacapa — the global benchmark for altitude-aged rum with miel virgen base; the most technically distinctive Central American rum terroir expression despite the additive controversy',
        'north_america_access': 'Diageo distribution through all major US and Canadian spirits retailers; widely available at Total Wine, LCBO, BCLDB; the XO is standard-stocked at premium spirits retailers in Vancouver and Seattle',
        'culinary_application': 'Zacapa XO\'s natural sweetness makes it an outstanding dessert pairing spirit: dark chocolate preparations where the PX-raisin character resonates with 70%+ cacao; aged cheese with candied walnut where the Oloroso nut character complements both; as a digestive substitute for Armagnac in dessert service contexts where the sweetness level is appreciated rather than avoided'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region('spirits', 'Grenada — St Patrick Parish (River Antoine Rum Estate, 18th Century Pot Still, Oldest Working Rum Distillery)')

session.add_producer({
    'tradition': 'spirits',
    'name': 'River Antoine Rum Estate',
    'location': 'St Patrick Parish, northeastern Grenada',
    'description': 'The River Antoine Rum Estate is the oldest continuously operating distillery in the Caribbean — founded in 1785 and still operating with the same water-wheel technology that powered production in the 18th century. A National Historic Landmark of Grenada, the estate sits on the northeastern coast of Grenada in St Patrick Parish, where the Antonio River (after which the estate is named) powers a 10-foot overshot water wheel that drives the cane-crushing mill. The estate is entirely self-sufficient: all cane grown on 36 acres of the estate, crushed by the water wheel, fermented in open wooden vats for 5–7 days with wild yeast, and double-distilled in the estate\'s original 18th-century copper pot still. The resulting River Antoine Royale Grenadian Rum — bottled at 75% ABV (150 proof) — is the strongest commercially bottled rum in the world and is legally required to be bottled at this strength by Grenadian law, which designates River Antoine\'s production method as a National Heritage Product.',
    'founded': '1785',
    'region': 'St Patrick Parish, Grenada',
    'website': None,
    'verified': True
})

session.add_beverage({
    'name': 'River Antoine Royale Grenadian Rum — 1785 Water-Wheel Estate, 75% ABV, Caribbean\'s Oldest Distillery',
    'category': 'spirits',
    'subcategory': 'rum_pot_still',
    'origin': 'Grenada',
    'region': 'St Patrick Parish, Grenada',
    'producer': 'River Antoine Rum Estate',
    'alcohol_content': 75.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The River Antoine Estate sits on Grenada\'s northeastern coast in the parish of St Patrick — the most rugged and least developed part of the island, where the volcanic mountains of the interior drop steeply to the Atlantic coast through a narrow coastal valley. The Antonio River that powers the estate flows from the northern slopes of Mount St Catherine (Grenada\'s highest peak at 840m) through volcanic basalt geology to the coastal estate at near sea level. The cane grown on the estate\'s 36 acres is a heritage variety maintained without introduction of commercial hybrid canes — the same or similar genetic stock to the 18th-century plantation canes that were cultivated during the British colonial period when River Antoine was established. The northeastern coastal terroir produces cane with a distinctive briny quality from Atlantic sea spray exposure and volcanic basalt mineral absorption — a terroir character that is directly legible in the finished rum. Grenada itself is geologically young — the island emerged from volcanic activity approximately 2–3 million years ago — and its dark basalt soils, rich in iron and magnesium, contribute mineral compounds through root uptake that appear in the fresh cane juice fermented at River Antoine. The estate\'s terroir extends beyond the soil and water: the open wooden fermentation vats that have been in continuous use since the 18th century harbor a unique microbial culture accumulated over 240+ years of continuous production — an ecosystem of wild Saccharomyces, Pichia, Candida, and Lactobacillus species that have evolved specifically to the River Antoine environment and contribute to the rum\'s wild, complex character.'
    ),
    'production_technique': (
        'River Antoine\'s production process has remained essentially unchanged since 1785 — a genuine living museum of 18th-century Caribbean rum production. The 10-foot overshot water wheel (one of only two such operating cane mills remaining in the Caribbean) drives a three-roller horizontal cane press that crushes freshly cut estate cane within hours of harvesting. Fresh cane juice flows by gravity from the press through limestone filter channels into open wooden vats — the same wooden fermentation vessels used since the 18th century, seasoned with 240 years of accumulated microbial culture. Wild fermentation begins spontaneously within 2–4 hours from the wild yeast population on the cane and in the wooden vats; no commercial yeast addition, no temperature control, no nutrient addition. The 5–7 day wild fermentation at ambient Grenada temperatures (28–34°C) produces a wash at 8–12% ABV of extraordinary wild complexity. Distillation occurs in the estate\'s copper pot still in a single distillation run, taking a wide hearts cut at 70–80% ABV. The spirit is not diluted before bottling — River Antoine Royale is bottled at 75% ABV (150 proof) as required by Grenada\'s National Heritage Product designation. No aging, no filtration, no additives. The 75% ABV is legal in Grenada for this specific heritage product classification; export restrictions apply to certain markets that prohibit spirits above 65% ABV. The entire production process from cane cutting to bottling occurs on the 36-acre estate using 18th-century technology powered by renewable water energy — carbon footprint approaches zero for the production process itself.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Clairin Sajous Haiti (wild fermentation, unaged, maximum terroir transparency)',
            'connection': 'River Antoine and Clairin Sajous are the two purest expressions of the Caribbean artisan cane spirit tradition — both using wild fermentation in wooden vessels from heritage cane varieties without commercial yeast or temperature control, both bottled immediately without aging — but River Antoine at 75% ABV represents the most extreme preservation of the distillate\'s raw power, while Sajous at 48.8% represents the accessible diluted version of the same philosophy'
        },
        {
            'tradition': 'Mezcal Papalometl (wild agave fermentation, open-air roasting, traditional equipment)',
            'connection': 'River Antoine\'s 240-year-old water wheel and wooden vat technology parallels the most traditional mezcal producers who use tahona stone wheels (ox-powered) to crush roasted agave hearts — both represent the living preservation of 18th-century agricultural distillation technology that survives in geographic isolation from modernization pressure, both producing spirits of irreplaceable historical character'
        },
        {
            'tradition': 'George T. Stagg Barrel Proof Bourbon (extreme high ABV, uncut distillate character)',
            'connection': 'River Antoine at 75% ABV and Stagg at 65+ ABV share the category of "extreme ABV by design" spirits where the distiller deliberately preserves the full distillate proof to communicate maximum raw spirit character — both require water addition at service (River Antoine is typically diluted to 45–50% before drinking, bringing out the wild fermentation aromatic complexity)'
        }
    ],
    'sensory_profile': {
        'appearance': 'Crystal clear water-white at full 75% ABV; extreme spirit viscosity at this proof — significant oiliness on glass walls; the high ABV is immediately evident from evaporation at the glass surface',
        'nose': 'At full strength: intensely aromatic, overripe tropical fruit, raw fermented cane, wild yeast character, volcanic mineral, acetaldehyde freshness — overwhelming at full proof; diluted to 50% with water: fresh pineapple, ripe banana, wild fermentation complexity, sea salt mineral, Atlantic coastal character — one of the most complex unaged rum noses available commercially',
        'palate': 'At full strength: immediate extreme alcohol heat; at 45–50% (recommended): full-bodied, tropical fruit intensity, wild yeast-ester character, volcanic mineral mid-palate, long finish with coastal mineral and dried tropical fruit — the 240-year wooden vat microbial culture is unmistakably present as a "funky" complexity that no commercial yeast can replicate'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'River Antoine Royale (Standard, 75% ABV)',
            'criteria': 'The single expression: unaged, undiluted, heritage production — no tiers in the traditional sense as River Antoine produces only one product from one process; the quality is absolute, not comparative'
        },
        {
            'tier': 2,
            'tier_name': 'River Antoine Overproof (diluted, export markets)',
            'criteria': 'For export markets prohibiting >65% ABV, River Antoine is diluted to 63% — slightly more accessible than 75% but less expressive; the 75% ABV original is the definitive version'
        },
        {
            'tier': 3,
            'tier_name': 'Estate Reserve (theoretically possible, not currently produced)',
            'criteria': 'If River Antoine ever produced an aged version — placing the wild-fermented pot still distillate in the estate\'s original 18th-century wooden casks for aging — the result would be one of the most historically significant Caribbean rum expressions possible; not currently commercially available'
        },
        {
            'tier': 4,
            'tier_name': 'Heritage Status (240-Year Continuous Production)',
            'criteria': 'The ultimate expression of River Antoine\'s value is not product tiers but the continuity of 240 years of identical production — every bottle of River Antoine contains rum produced by the same water wheel, same wooden vats, same copper still, same wild yeast culture as bottles produced in 1800; the historical continuity is itself the highest-quality attribute'
        }
    ],
    'service_intelligence': {
        'temperature': 'Full 75% should be diluted to 45–50% with still water before service — add the water first, then smell the transition; the dilution point where the aromatic complexity peaks is typically at 50% (adding 30ml water per 50ml rum); serve at 22–24°C room temperature after dilution',
        'vessel': 'Wide tulip or rocks glass after dilution; at full proof, any glass is acceptable as the ABV intensity dominates the aromatic experience regardless of vessel; the typical Grenadian service is a small shot of River Antoine with an equal amount of water chased separately',
        'cultural_context': 'River Antoine is a Grenada National Heritage Product and visiting the estate is one of the most historically authentic distillery experiences in the Caribbean; the working water wheel, 18th-century copper still, and open wooden vats operating by gravity are a living demonstration of how rum was produced across the colonial Caribbean before industrialization — the definitive PCT answer to what Portuguese colonial cane spirit production looked like in its original form'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'River Antoine Rum Estate — the definitive single expression, single estate, single price point Caribbean heritage rum',
        'north_america_access': 'Available through Grenada directly (on-island purchases); limited export through specialty spirits retailers in US and Canada; Potomac Imports handles limited US distribution; in Canada through private import; the Caribbean specialty spirits market (Prime Rum, Whisky Exchange) carries online for international shipping',
        'culinary_application': 'River Antoine at 50% diluted makes an outstanding cocktail base for heritage-focused cocktail programs where the provenance narrative is as important as the flavor: a River Antoine Ti\' Punch diluted to 50% with lime and cane syrup creates the most historically authentic Caribbean cocktail possible; the rum\'s wild complexity also works in reduction sauces for island-spice preparations where the fermentation character adds depth that commercial rum cannot provide'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
