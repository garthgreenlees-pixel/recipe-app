import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Grenada — St Patrick Parish (River Antoine Rum Estate, 18th-Century Water-Driven Pot Still, Oldest Working Rum Distillery)',
    output_dir='.',
    starting_entry=1,
    session_number=80,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'River Antoine Rum Estate',
    'location': 'St Patrick Parish, Grenada, Eastern Caribbean',
    'country': 'Grenada',
    'region': 'St Patrick Parish, northern Grenada',
    'key_person': 'The Antoine family (multi-generational ownership)',
    'founded': '1785',
    'production_volume': 'Fewer than 20,000 litres per year — entire production consumed domestically in Grenada and small-volume export',
    'notable_products': [
        'River Antoine Royal Grenadian Rum (cask strength, 75% ABV)',
        'River Antoine Lower-Proof Expression (69% ABV)',
    ],
    'certifications': [],
    'website': 'riverantoine.com',
    'philosophy': (
        'River Antoine is not a heritage preservation project — it is an '
        'active distillery that has never stopped using its original 1785 '
        'water-wheel-driven copper pot still. No column still. No industrial '
        'process. The estate grows its own sugarcane, harvests it by hand, '
        'crushes it with the water wheel, ferments the fresh cane juice in '
        'open wooden cisterns without temperature control, and distills '
        'in the original pot still to a raw, high-ester, cask-strength spirit '
        'bottled without aging or dilution — the same process for 240 years.'
    ),
    'trail_connection': 'PCT (Portuguese Colonial Trail) — Caribbean rum node',
    'verified': True
})

session.add_beverage({
    'name': (
        'River Antoine Royal Grenadian Rum — Oldest Working Distillery '
        'Caribbean, Water-Driven Pot Still 1785, Raw High-Ester Cane Spirit, '
        'St Patrick Parish Grenada'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'rum — traditional pot still, unaged',
    'region': 'Grenada — St Patrick Parish (River Antoine Rum Estate, 18th-Century Water-Driven Pot Still, Oldest Working Rum Distillery)',
    'terroir_origin': (
        'River Antoine Estate sits in the St Patrick Parish of northern '
        'Grenada, on the eastern Caribbean island known principally for '
        'its nutmeg, cocoa, and spice production but also home to the '
        'oldest continuously operating rum distillery in the Caribbean. '
        'The estate was established in 1785 — predating Haitian independence '
        '(1804), predating the end of the British slave trade (1807), and '
        'predating the Napoleonic wars — making it the oldest working rum '
        'distillery in the Western Hemisphere. The sugarcane grown on the '
        'estate is a heritage variety maintained without significant '
        'agrochemical input on the volcanic loam soils of the Grenadine '
        'interior, where the Atlantic trade winds provide natural '
        'ventilation and the rainfall from the Central Ridge (400–600mm '
        'per year on the leeward northern slopes) supports cane growth '
        'without irrigation. The production facility is powered entirely '
        'by a water wheel fed from the Antoine River — hence the estate '
        'name — which drives the cane crushing mill at the same speed '
        'it has turned for 240 years. The resulting distillery character '
        'is shaped by the combination of the fresh Grenadian cane juice '
        '(not molasses), the open wooden fermentation cisterns exposed '
        'to the ambient Grenadian microflora, and the single-pass copper '
        'pot still that produces a raw, high-ester spirit at 75% ABV '
        'without the rectification or dilution that would strip the '
        'terroir character of the Grenadian cane base.'
    ),
    'production_technique': (
        'The River Antoine production process is entirely pre-industrial '
        'and unchanged since the distillery\'s founding in 1785. '
        'The harvested sugarcane is brought from the estate fields '
        'to the water-wheel-powered crushing mill, where the water wheel '
        '(fed by the Antoine River) turns the horizontal cane rollers '
        'to extract the fresh cane juice (vesou/guarapo) directly. '
        'Unlike industrial Caribbean rum producers who use molasses '
        '— the residual byproduct of crystallized sugar extraction — '
        'River Antoine ferments the fresh sugarcane juice itself, '
        'making it a rhum agricole production method in the French '
        'Caribbean tradition rather than a molasses-based rum in '
        'the British tradition. The fresh cane juice runs by gravity '
        'into large open wooden fermentation cisterns, where no '
        'commercial yeast is added — the fermentation proceeds '
        'entirely on the ambient wild yeasts and bacteria present '
        'in the estate environment (including the bacteria coating '
        'the wooden cistern walls, which have accumulated over '
        'generations of fermentation). The fermentation takes '
        '5–7 days at ambient Grenadian temperatures (26–32°C), '
        'producing a highly complex, high-ester wash with dunder '
        'characteristics (the Grenadian tradition includes '
        'retaining spent still residue — dunder — in the wash '
        'to amplify ester development, creating the characteristic '
        'pungent, high-ester profile). The fermented wash is '
        'charged to the single copper pot still, which is heated '
        'by direct fire from a wood furnace below. A single '
        'distillation run produces the spirit at approximately '
        '75% ABV — unusually high proof for a single-pass '
        'pot still, achieved by careful management of the '
        'cut points by the stillman. The spirit is bottled '
        'at cask strength (75% ABV for the Royal Grenadian '
        'expression, 69% ABV for the lower-proof version) '
        'without aging, without dilution, and without '
        'any additive — raw from the still to the bottle. '
        'Total production is fewer than 20,000 litres per year, '
        'with the vast majority consumed by Grenadian workers '
        'and locals (particularly cane cutters and fishermen '
        'of St Patrick Parish) and a small volume sold '
        'to international specialist rum importers.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — mezcal (Oaxaca, Mexico)',
            'beverage': 'Papalometl Mezcal Ancestral — Tehuantepec Isthmus, Single-Pass Clay Pot Still',
            'connection': (
                'River Antoine and ancestral mezcal producers of Oaxaca '
                'share the same fundamental commitment to pre-industrial '
                'production that is active and functional, not museum-piece. '
                'Both use the simplest possible distillation vessel (copper '
                'pot still at River Antoine; clay or copper pot still in '
                'ancestral mezcal), ferment on wild ambient microflora '
                'without commercial yeast inoculation, and produce a '
                'raw, high-proof spirit bottled without aging or '
                'intervention. The ester profile of both — pungent, '
                'funky, with organic fermentation character — is '
                'the direct result of the long, uncontrolled open '
                'fermentation in natural vessels, contrasting sharply '
                'with the clean, neutral profile achieved by controlled '
                'industrial fermentation. Both traditions are also '
                'defined by the fact that most production is consumed '
                'locally by the farming and working communities that '
                'produce them, with international "discovery" being '
                'a recent phenomenon that has not yet transformed '
                'the production method.'
            )
        },
        {
            'tradition': 'spirits — rhum agricole (Martinique, French Caribbean)',
            'beverage': 'Rhum Agricole Blanc AOC Martinique — Sugarcane Juice Distillation, Creole Column Still',
            'connection': (
                'River Antoine and Martinique rhum agricole share the '
                'same essential raw material decision — both ferment and '
                'distill fresh sugarcane juice (vesou/guarapo) rather '
                'than molasses — which is the single most important '
                'production distinction in Caribbean rum. The fresh '
                'cane juice base provides a green, vegetal, grassy '
                'aromatic register (from the volatile compounds in '
                'fresh cane juice that are destroyed or transformed '
                'in the molasses production process) that is the '
                'defining character of both River Antoine and '
                'Martinique agricole blanc. The divergence is in '
                'distillation: Martinique agricole uses the Creole '
                'column still (producing a cleaner, more refined '
                'spirit at 65–72% ABV), while River Antoine uses '
                'the original 1785 copper pot still with dunder '
                '(producing a rawer, higher-ester, more complex '
                'and funky spirit). Both traditions are the Caribbean '
                'preservation of a cane juice distillation method '
                'that predates the industrialisation of sugar '
                'production and the shift to molasses as the '
                'standard rum raw material in the 19th century.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Water-clear to very pale gold — the spirit is unaged and '
            'bottled directly from the still without cask contact or '
            'any colorant; the clarity is absolute, with no colloidal '
            'haze despite the very high ABV (75%); the viscosity is '
            'noticeably higher than standard 40% ABV spirits, with '
            'thick, clinging legs and a surface tension that indicates '
            'the concentration of natural congeners in the unfiltered '
            'high-proof spirit.'
        ),
        'nose': (
            'Powerfully assertive at 75% ABV — immediate dilution with '
            'water (add 2–3 drops to bring below 50% ABV for nosing) '
            'is necessary for full aromatic assessment. At working '
            'strength: pungent acetate esters (isoamyl acetate, '
            'ethyl acetate) from the open dunder fermentation dominate '
            'the opening; beneath, fresh sugarcane juice (bagasse, '
            'green cane flesh, raw cane sugar) from the agricole '
            'production method; banana and overripe tropical fruit '
            'from the high-ester wild-yeast fermentation; the '
            'characteristic "funk" of pot-still Caribbean rum '
            '— the combination of esters, fusel alcohols, and '
            'bacterial fermentation compounds that cannot be '
            'achieved in column-still distillation; very little '
            'vanilla or caramel (no barrel aging); the finish '
            'aromatic register is raw, agricultural, and intensely '
            'alive with microbial fermentation character.'
        ),
        'palate': (
            'At cask strength (75% ABV), River Antoine must be diluted '
            'for any palate assessment — neat consumption at 75% is '
            'possible only for Grenadian workers accustomed to the '
            'expression (and is culturally standard in St Patrick '
            'Parish). Diluted to 40–45% ABV: medium-full body '
            'from the natural congeners and undiluted volatile '
            'compounds of the pot still; the ester blast of '
            'the nose resolves on the palate to a complex '
            'mix of fresh cane juice sweetness, raw fermentation '
            'character, and the persistent funk of the dunder '
            'ester compounds; very dry finish with the '
            'characteristic heat of a high-strength spirit '
            'even after dilution — the fusel alcohol profile '
            'from open fermentation is present but not harsh '
            'in the context of the full-spectrum pot still '
            'production; the finish lingers for 30–45 seconds '
            'with a persistent cane-juice and ester character '
            'that identifies this immediately as a traditional '
            'Caribbean agricole pot-still expression.'
        ),
        'conclusion': (
            'Historically and technically distinctive: the only '
            'spirit in the world produced continuously on an '
            '18th-century water-wheel-driven pot still. The '
            'quality register is defined entirely by the '
            'authenticity of the production method rather than '
            'by the conventional wine-scoring descriptors of '
            'refinement and balance — this spirit is raw, '
            'assertive, and agricultural by design.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'River Antoine Royal Grenadian Rum at 75% ABV — the benchmark '
                'expression of the oldest working distillery in the Caribbean, '
                'direct from the 1785 copper pot still without dilution, '
                'filtration, or modification. The definitive record of what '
                '18th-century Caribbean rum production produced before '
                'industrialisation. Award recognition in specialist rum '
                'competitions (Tales of the Cocktail Spirited Awards, '
                'Ministry of Rum) as a heritage benchmark, not a commercial '
                'competitor.'
            ),
            'markers': (
                'Authentic dunder ester profile; 75% ABV pot still raw '
                'strength; water-driven distillation; open wooden cistern '
                'wild-yeast fermentation; unaged and unfiltered.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'River Antoine Lower-Proof Expression at 69% ABV — the '
                'same production method with a slightly lower distillation '
                'cut, producing a marginally more refined ester profile '
                'while retaining the full pot still agricole character. '
                'The preferred expression for international specialist '
                'rum consumers who want the authentic River Antoine '
                'character without the extreme 75% ABV intensity.'
            ),
            'markers': (
                'Same water-driven pot still; same open fermentation; '
                'lower proof entry point; same lack of aging or additives.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Other Grenadian rum expressions (Clarke\'s Court, Westerhall) '
                'that use column distillation and partial industrialisation — '
                'competent commercial Caribbean rum production with Grenadian '
                'terroir elements but without the heritage pot still character '
                'of River Antoine; suitable for cocktail use where the raw '
                'agricole character of River Antoine would be excessive.'
            ),
            'markers': (
                'Column still; molasses or partial cane juice base; '
                'cleaner, more neutral profile; conventional Caribbean '
                'rum aging (2–5 years in ex-bourbon barrels).'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic Caribbean white rum production (Bacardi, '
                'Captain Morgan, etc.) using column distillation of '
                'molasses to near-neutral spirit, then diluted and '
                'charcoal-filtered — the antipode of River Antoine; '
                'all terroir character eliminated; no fermentation '
                'complexity; the industrial rum that River Antoine '
                'has never been and has no commercial interest in becoming.'
            ),
            'markers': (
                'Industrial molasses column still; neutral spirit base; '
                'charcoal filtration; no agricultural character; '
                'standardised flavour profile regardless of origin.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'River Antoine at 75% ABV must be approached differently from '
            'any conventional spirits service protocol. For professional '
            'programme use: serve in the traditional Grenadian manner '
            '— a small measure (15–20ml) neat at ambient temperature '
            '(22–25°C) alongside a water chaser, with verbal explanation '
            'of the ABV and the cultural context of cane-field consumption. '
            'For tasting/evaluation service: dilute to 45–50% ABV '
            'by adding 10–15ml of still water before presentation; '
            'serve at 20–22°C. Never chill — cold temperatures '
            'suppress the ester volatilisation that is the entire '
            'point of nosing a traditional pot-still rum at working strength.'
        ),
        'vessel': (
            'Serve in a small spirits Glencairn (50–75ml pour capacity) '
            'or a copita for evaluation at diluted strength (45% ABV); '
            'for the authentic Grenadian cultural service, a small '
            'shot glass or a traditional Grenadian tin cup with '
            'water alongside captures the agricultural heritage '
            'of how this spirit is actually consumed by the '
            'cane workers and fishermen who represent the '
            'primary market for River Antoine production. '
            'In a formal programme context (PCT heritage flight, '
            'Caribbean rum depth session), present alongside '
            'a bottle of still water and a card describing '
            'the 1785 water wheel, the open fermentation, '
            'and the dunder tradition — the education '
            'context is as important as the liquid for '
            'communicating why River Antoine occupies a '
            'unique position in the world spirits archive.'
        ),
        'technique': (
            'Always dilute to working strength before guest service '
            'unless the guest has specifically requested cask-strength '
            'presentation with full ABV disclosure. The correct '
            'professional service phrase: "River Antoine from '
            'Grenada — the oldest working rum distillery in '
            'the Caribbean, established 1785. The still is '
            'powered by a water wheel to this day. This is '
            'bottled at 75% ABV, directly from the pot still '
            'without aging. I have diluted it to 45% for '
            'our service — may I add a drop more water '
            'to your preference?"'
        ),
        'programme_position': (
            'Historical anchor position in a Caribbean rum depth flight: '
            'serve first as the 18th-century baseline before progressing '
            'to Haitian Clairin (19th-century agricole tradition), '
            'Martinique rhum agricole AOC (20th-century regulated '
            'agricole), and Ron Zacapa 23 Sistema Solera '
            '(21st-century highland aged) — a four-glass arc '
            'of Caribbean spirits history.'
        ),
        'verbal_presentation': (
            'The oldest working rum distillery in the Caribbean. '
            'Still powered by water. Still distilling in the '
            'original 1785 copper pot. No aging. No filtering. '
            'Nothing added. This is what Caribbean rum tasted '
            'like before industrialisation.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'River Antoine Rum Estate, St Patrick Parish, Grenada '
            '(est. 1785 — the benchmark for Caribbean heritage '
            'pot-still rum production; the only operational '
            '18th-century water-wheel-driven rum distillery '
            'in the world; all other rum distilleries '
            'claiming heritage production are either '
            'museum exhibits or have modernised their '
            'machinery; River Antoine alone has not).'
        ),
        'producer_location': 'St Patrick Parish, northern Grenada, Eastern Caribbean',
        'key_person': 'Antoine family (multi-generational ownership)',
        'production_volume': 'Under 20,000 litres per year — primarily domestic Grenadian consumption',
        'certifications': [],
        'bc_distributor': '[PROVIDER: verify specialist Caribbean rum importer for BC — check Authentic Seacoast or Caribbean specialty importers]',
        'us_distributor': 'K&L Wine Merchants and specialty rum retailers in the US have carried River Antoine at various points; verify current distributor',
        'uk_distributor': 'The Whisky Exchange and Master of Malt have carried River Antoine; verify current stock',
        'price_tier': 'Reserve',
        'availability_notes': (
            'River Antoine is extremely limited outside Grenada. '
            'International availability is primarily through specialist '
            'rum retailers and online spirits merchants who maintain '
            'connections to the small-volume export allocation. '
            'Grenadian state shops (duty free) carry River Antoine '
            'at the most accessible pricing. International prices '
            'range from USD $25–40 per 750ml for the 75% ABV '
            'expression when available — surprisingly affordable '
            'for a spirit of this historical significance, '
            'reflecting the artisanal production economics '
            'and limited marketing of the estate.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'River Antoine connects the Portuguese Colonial Trail beverage '
        'narrative through the colonial history of Grenada: the island '
        'was a French colony (1649–1762) before becoming British '
        '(1762–1974), with the rum tradition established during '
        'the colonial sugar plantation era that was shaped by '
        'both French and British colonial agricultural practices. '
        'The agricole production method (fresh cane juice) '
        'connects River Antoine to the French Caribbean '
        'rhum agricole tradition that is itself a PCT-adjacent '
        'production heritage preserved in Martinique and '
        'Guadeloupe under French AOC protection.'
    ),
    'food_pairings': [
        {
            'technique_id': 'GRD-001',
            'dish': 'Grenadian oil-down (one-pot breadfruit, callaloo, dasheen, salted meat)',
            'pairing_type': 'bridge',
            'rationale': (
                'The raw ester pungency of River Antoine at working '
                'strength cuts directly through the fat richness of '
                'coconut-milk braised oil-down; the agricultural '
                'character of the rum bridges to the earthy '
                'root vegetable base of the dish through '
                'shared provenance of the Grenadian estate.'
            )
        },
        {
            'technique_id': 'CAR-002',
            'dish': 'Nutmeg-cured Grenadian fish (fresh mahi-mahi, nutmeg, lime, Scotch bonnet)',
            'pairing_type': 'complement',
            'rationale': (
                'River Antoine\'s high-ester agricole character '
                'mirrors the volatile aromatic compounds of freshly '
                'grated Grenadian nutmeg — both express the same '
                'tropical island terroir through entirely different '
                'production paths; the lime acidity in the cure '
                'cuts the spirit\'s ABV intensity.'
            )
        }
    ],
    'source': 'River Antoine Estate records; Ministry of Rum documentation; Tales of the Cocktail Spirited Awards records; Caribbean rum heritage research',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
