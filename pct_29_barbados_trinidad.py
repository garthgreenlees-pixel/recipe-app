import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Barbados — St Philip Parish (Foursquare Distillery, Exceptional Cask Series, Pot-Column Hybrid)',
    output_dir='.',
    starting_entry=1,
    session_number=30,
    running_total=92
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Foursquare Distillery — Richard Seale',
    'location': 'St Philip Parish, Barbados',
    'description': 'Foursquare Distillery is operated by Richard Seale, fourth-generation member of the Seale family who have owned the property since 1926. The distillery occupies a former sugar factory in St Philip Parish — the southeastern corner of Barbados, where the coral limestone soil and sea breeze from the Atlantic coast influence both cane character and aging conditions. Seale is the most influential figure in the modern Caribbean rum renaissance: his "Exceptional Cask Series" began in 2012 as an attempt to demonstrate that Barbados rum could be aged and presented with the same seriousness as Cognac or Scotch whisky. Foursquare operates both a pot still (2,000-litre copper) and a two-column Coffey still, blending both distillates at varying ratios for different expressions. Seale is a prominent critic of unauthorized additive practices in Caribbean rum labeling — his campaigns against undisclosed coloring and sweetening agents have driven regulatory transparency discussions across the Caribbean rum industry.',
    'founded': '1926 (Seale family acquisition)',
    'region': 'St Philip Parish, Barbados',
    'website': 'foursquaredistillery.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Velier SpA (International) / Skurnik Wines (US) — Foursquare Exceptional Cask',
    'type': 'importer',
    'description': 'Foursquare\'s Exceptional Cask Series is distributed internationally through a partnership with Velier SpA for European markets and directly to US importers through Skurnik Wines and K&L Wine Merchants direct allocation. In Canada through private import channels and the LCBO\'s occasional product submissions. The annual Exceptional Cask releases sell out within hours of notification to registered buyers — one of the most sought-after Caribbean rum releases globally.',
    'markets_served': ['EU', 'US', 'Canada', 'UK', 'Australia'],
    'traditions_carried': ['spirits'],
    'website': 'foursquaredistillery.com',
    'verified': True
})

session.add_beverage({
    'name': 'Foursquare Exceptional Cask Series — Barbados Pot-Column Blend, Natural Color and Proof',
    'category': 'spirits',
    'subcategory': 'rum_blended',
    'origin': 'Barbados',
    'region': 'St Philip Parish, Barbados',
    'producer': 'Foursquare Distillery — Richard Seale',
    'alcohol_content': 56.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'The Foursquare estate sits on the coral limestone plateau of St Philip Parish — the oldest and most mineralogically complex geological formation in Barbados, composed of compacted coral and marine sediment raised from the ocean floor by tectonic uplift approximately 700,000 years ago. The coral limestone has three critical effects on Foursquare\'s production: the sub-surface limestone aquifer provides the purest, most mineral-neutral water in Barbados for dilution (a direct influence on finished spirit character); the porous limestone soil provides superior drainage for the cane fields, limiting water stress while concentrating the sucrose and aromatic precursors in the cane stalk; and the limestone\'s thermal mass moderates the extreme Caribbean heat slightly in the St Philip coastal zone, where the Atlantic trade wind exposure from the eastern coast provides an additional cooling effect. The combination of coral limestone agriculture, Atlantic trade wind influence, and the specific Barbados flying fish-current microclimate around the island produces a cane character that Richard Seale describes as "restrained and refined" compared to the more exuberant tropical character of Jamaican or Haitian cane — a character that translates into Foursquare\'s disciplined house style. The coral limestone aging warehouse environment is a further terroir factor: the tropical humidity accelerates barrel interaction while the Atlantic breeze moderates temperature extremes, producing what Seale calls "tropical aging without tropical excess" — a more controlled barrel interaction than inland Caribbean distilleries.'
    ),
    'production_technique': (
        'Foursquare\'s hybrid distillation approach combines pot still complexity with column still cleanliness in proportions that vary by expression. The pot still (a 2,000-litre copper traditional pot) is charged with fully fermented molasses wash (from Barbados sugar estates) and double-distilled in the traditional Barbadian method — a technique that produces a heavy, ester-rich rum at 86–88% ABV from the spirit still. The two-column Coffey (continuous) still produces a lighter, cleaner distillate at 94–96% ABV from the same molasses wash source. Richard Seale blends pot and column distillates at different ratios for different Exceptional Cask Series expressions — some vintages lean 60:40 pot-to-column for more body and ester character; others run 40:60 for cleaner, more refined structure. The specific blend ratio is determined by Seale\'s tasting of the individual distillate batches against his vision for the vintage expression. Fermentation at Foursquare runs 48–72 hours with a proprietary Saccharomyces cerevisiae culture maintained at the distillery — a moderate fermentation time that produces a clean, moderately estered wash without the extreme dunder-driven character of Jamaican high-ester producers. Aging occurs in a combination of ex-bourbon American oak (first-fill, second-fill, and third-fill barrels) and ex-Cognac French Limousin oak — the Cognac cask introduction in the Exceptional Cask Series adds dried fruit, spice, and floral complexity from the used French oak. Extended aging of 10–20 years depending on the specific Exceptional Cask bottling produces extraordinary tertiary complexity. Zero additives: no caramel coloring, no sugar addition, no glycerol, no artificial flavoring — the natural aging color and proof dilution (with limestone aquifer water) are the only modifications to the distillate.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Cognac VS/VSOP/XO (Charentais pot still, Limousin oak aging)',
            'connection': 'Foursquare\'s use of ex-Cognac Limousin oak barrels in the Exceptional Cask Series creates the most direct technical connection between Barbados rum and Cognac in the Caribbean spirits world — Richard Seale explicitly positions the Exceptional Cask Series as the Caribbean equivalent of single-château Cognac: terroir-specific, additive-free, aged for complexity rather than consistency'
        },
        {
            'tradition': 'Hampden Estate HLCF (Jamaican high-ester, opposite philosophy)',
            'connection': 'Foursquare and Hampden represent the definitional contrast in the Caribbean artisan rum renaissance: Foursquare optimizing for refined structure, minimal ester, transparency of aging, additive-free authenticity; Hampden optimizing for maximum ester intensity, terroir-extreme "Hogo" character, wild fermentation — both are world-class expressions of Caribbean rum culture but through opposite philosophies'
        },
        {
            'tradition': 'Blanton\'s Single Barrel Bourbon (additive-free, terroir-specific, allocated)',
            'connection': 'Both Foursquare Exceptional Cask and single-barrel premium Bourbon occupy the same consumer position: additive-free declarations from named single estates, strict barrel-level quality selection, cask-strength bottling, extremely limited allocation that creates immediate sell-out on release day — the "fine wine" rum positioning that Seale pioneered for Barbados rum in 2012'
        }
    ],
    'sensory_profile': {
        'appearance': 'Rich mahogany amber-brown from extended ex-bourbon and ex-Cognac oak aging; perfectly clear; natural color variation vintage to vintage (no standardization through caramel); significant viscous legs from 56% ABV',
        'nose': 'Complex and structured: dried tropical fruit (raisin, fig, dried mango), dark caramel, vanilla from American oak, dried flower and dried fruit spice from the Cognac cask contribution, coral limestone mineral in background, warm and elegant rather than aggressive — the restraint of the Barbados pot-column blend evident in every aromatic layer',
        'palate': 'Full body, warming 56% that integrates rather than burns, dark fruit-caramel core, oak-derived dried spice, long finish with coral limestone mineral dryness — the benchmark of how elegant, additive-free, extended-aged Barbados rum can be; the pot-column blend gives both richness (pot still) and cleanliness (column) in a final integration that is the most technically sophisticated in Caribbean rum production'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Foursquare 2S (Entry Expression)',
            'criteria': 'Foursquare\'s accessible expression from shorter aging and higher column still proportion — the entry to the house philosophy at a more accessible price point'
        },
        {
            'tier': 2,
            'tier_name': 'Foursquare Probitas (Collaboration, White Rum)',
            'criteria': 'Collaboration with Hampden Estate producing a 50/50 Barbados/Jamaica white rum — bridges the two great Caribbean rum philosophies in a single unaged expression'
        },
        {
            'tier': 3,
            'tier_name': 'Exceptional Cask Series (Named Vintage)',
            'criteria': 'The flagship: named vintage year, specific pot-column ratio, specific cask combination, 10–20 years aging, cask strength, additive-free — each annual release is a distinct expression of that harvest year\'s distillate aged in Seale\'s specific cask selection'
        },
        {
            'tier': 4,
            'tier_name': 'Exceptional Cask Triptych (Three-Expression Set)',
            'criteria': 'The highest-tier release: three bottles from the same vintage distillate aged in different cask types (ex-Cognac, ex-Bourbon, ex-Sherry) released as a set to demonstrate how cask type modifies the same distillate base — limited to under 500 sets globally, priced at Cognac XO collector level'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature at 20–22°C for the Exceptional Cask expressions — the 56% ABV works at room temperature with 5–10ml of still water to open aromatics rather than ice dilution; Seale recommends adding water drop-by-drop until the palate opens, a technique borrowed from Scotch whisky service',
        'vessel': 'Glencairn or tulip nosing glass to concentrate the complex aromatics from the blended distillate; the fine aromatic architecture of the Exceptional Cask Series rewards slow, patient nosing rather than the quick pour-and-drink approach appropriate for simpler rums; large Riedel Vinum Cognac glass also works excellently',
        'aging_potential': 'Once bottled, Foursquare Exceptional Cask continues to develop in the bottle for 5–10 years — the high ABV and residual wood compounds allow ongoing micro-oxidation through the cork; collectors who have opened bottles at 2 years post-release versus 7 years post-release report dramatically different aromatic profiles'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Foursquare Distillery (Richard Seale) — the international benchmark for Barbados artisan rum and the most influential Caribbean spirits producer in the quality transparency movement',
        'north_america_access': 'Exceptional Cask via Skurnik Wines (US) and K&L direct allocation — requires email list registration for allocation notification; BC Liquor carries Foursquare portfolio items; private import for Exceptional Cask releases in Canada through specialist retailers',
        'culinary_application': 'Foursquare Exceptional Cask at lower-tier expressions (2S, 12-year) serves as the base for the most sophisticated rum cocktail programs in the PNW — the additive-free character means the spirit\'s natural flavors are not masked by sweeteners, making it honest in any preparation; at Exceptional Cask tier, serve neat as a contemplative digestive spirit rather than as a cocktail component'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('spirits', 'Trinidad and Tobago — Laventille Hills (Angostura Bitters, 1824 Formula, 200-Year Production Heritage)')

session.add_producer({
    'tradition': 'spirits',
    'name': 'Angostura Ltd — House of Angostura',
    'location': 'Laventille, Port of Spain, Trinidad and Tobago',
    'description': 'House of Angostura produces both the world\'s most famous cocktail bitters (Angostura Aromatic Bitters, created 1824 in Angostura Venezuela by Dr. Johann Siegert, German physician to Simón Bolívar\'s liberating army) and a full portfolio of Trinidadian rum. The company moved from Venezuela to Trinidad in 1875, establishing its current Laventille distillery where the original bitters formula has been continuously produced for 200 years. Angostura\'s rum portfolio uses a unique 200-plate continuous still — the most sophisticated column still in the Caribbean — producing a lighter, more neutral distillate than pot still production, which is then aged in first-fill ex-bourbon barrels in Laventille\'s tropical warehouse. The 1919 Single Barrel and the Royal Oak Select Cask represent the finest expressions of the Angostura rum portfolio beyond the famous bitters.',
    'founded': '1824 (bitters creation); 1875 (Trinidad establishment)',
    'region': 'Laventille, Port of Spain, Trinidad and Tobago',
    'website': 'angostura.com',
    'verified': True
})

session.add_beverage({
    'name': 'Angostura 1919 Single Barrel — Trinidad Column Still, First-Fill Bourbon Oak, Laventille Tropical Aged',
    'category': 'spirits',
    'subcategory': 'rum_aged',
    'origin': 'Trinidad and Tobago',
    'region': 'Port of Spain, Trinidad and Tobago',
    'producer': 'Angostura Ltd — House of Angostura',
    'alcohol_content': 40.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The House of Angostura in Laventille sits on the eastern edge of Port of Spain, at the base of the Northern Range mountains that form the spine of Trinidad island. The Laventille Hills create a specific microclimate for barrel aging: warm and humid (85–90% RH annual average) but with breezes channeled through the mountain gaps that create diurnal temperature cycling between 26°C (night) and 34°C (day). This temperature cycling drives barrel breathing — wood expansion during the heat of day pushing spirit into the wood grain, contraction during cooler nights withdrawing the spirit back with barrel-extracted compounds — at a rate significantly faster than continental aging environments. The first-fill American white oak ex-bourbon barrels used for 1919 are sourced from the same Kentucky cooperages that supply top-tier Bourbon producers, typically aged for 4 years in Kentucky before being exported to Trinidad for re-use — the two aging stages (4 years in Kentucky + 8+ years in Trinidad) create a layered wood interaction combining the vanilla-coconut character from the Tennessee/Kentucky season with the tropical fruit-accelerated maturation from Laventille\'s heat and humidity. Trinidad as a PCT territory has a specific historical identity: the island was Spanish colonial from 1498 (Columbus\'s third voyage) to 1797 when Britain captured it — the German-Venezuelan origin of the Angostura bitters formula, combined with the Spanish-to-British colonial succession, makes Angostura Trinidad one of the most multi-layered colonial heritage beverage producers in the Caribbean.'
    ),
    'production_technique': (
        'Angostura\'s 200-plate Coffey still produces the cleanest, lightest rum distillate in the Caribbean — the 200 plates create extraordinary rectification, removing virtually all the congener-heavy heads and tails fractions that give pot-still rums their character. The base distillate emerges at 95–96% ABV, essentially a pure ethanol-water mixture from molasses fermented with Angostura\'s proprietary Saccharomyces cerevisiae culture. This very light base spirit is reduced to 62–65% for barrel entry — the barrel entry proof is lower than many Caribbean producers, which allows more rapid wood extraction and flavor development in the first-fill barrels. Fermentation runs 36–48 hours in closed stainless steel tanks with minimal dunder addition — Angostura does not use the aggressive dunder systems of Jamaican high-ester producers, as the 200-plate still would remove the ester compounds anyway. The 1919 Single Barrel selection involves Richard Seale\'s equivalent at Angostura (the master blender team) hand-sampling individual barrels that show exceptional development after 8+ years of Laventille tropical aging. Selected barrels are bottled individually without blending — each barrel becomes a distinct 1919 release with slight variation in color and character from barrel-specific development. Reduction to 40% with filtered Port of Spain municipal water (itself mineralogically influenced by the Northern Range geology). No additives confirmed by GC-MS analysis that Angostura publishes annually as part of Richard Seale\'s industry transparency advocacy support.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Foursquare Barbados (Caribbean quality transparency movement)',
            'connection': 'Angostura 1919 and Foursquare Exceptional Cask are the two flagship expressions of the Caribbean rum quality transparency movement — both additive-free, single-estate, extended-aged, with published production information — though from opposite distillation philosophies: Angostura\'s 200-plate column produces exceptional cleanliness while Foursquare\'s pot-column blend produces more textural complexity'
        },
        {
            'tradition': 'Cognac VS/VSOP (multi-stage aging, high-proof barrel entry)',
            'connection': 'The 1919\'s combination of first-fill ex-bourbon followed by tropical aging parallels Cognac\'s new-oak-to-old-oak barrel progression used by producers like Louis Roederer\'s Hine estate — both create layered wood character through sequential barrel types rather than a single cask type throughout aging'
        },
        {
            'tradition': 'Japanese single malt (extreme cleanliness, 200-plate refinement)',
            'connection': 'Angostura\'s 200-plate Coffey still philosophy — maximizing distillate cleanliness to allow barrel-derived character to emerge without competition from distillation congeners — parallels the Japanese whisky philosophy of Nikka and Suntory, which use multi-plate column stills to produce clean grain whisky that is then aged for maximum barrel character expression'
        }
    ],
    'sensory_profile': {
        'appearance': 'Rich amber gold from first-fill ex-bourbon and Laventille tropical aging; clear and brilliantly clean; the natural color from 8+ years of Caribbean barrel interaction is noticeably deeper than continental 8-year spirits from the same wood type',
        'nose': 'Elegant and clean: vanilla, toasted oak, dried apricot, light butterscotch, very subtle tropical fruit (the 200-plate cleanliness means no heavy esters compete with the barrel character), warm caramel — the house style is restrained elegance rather than tropical exuberance; the Angostura bitters influence shows as the faintest background note of dried botanicals from the shared Laventille warehouse environment',
        'palate': 'Light-medium body from the ultra-clean distillate base, vanilla-caramel core, tropical fruit mid-palate from Caribbean aging acceleration, clean finish without heaviness — the easiest-drinking of the serious Caribbean rum expressions due to the extreme column rectification; the 40% ABV is genuinely calibrated for neat service rather than cocktail use'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Angostura 5 Year',
            'criteria': 'Entry expression with shorter Laventille aging and standard blended production — the widely available commercial benchmark for Trinidadian rum'
        },
        {
            'tier': 2,
            'tier_name': 'Angostura 7 and 12 Year',
            'criteria': 'Extended column still aging in the progressive Angostura age statement series — the 12-year is a reference for clean, elegant, additive-free Caribbean rum at accessible pricing'
        },
        {
            'tier': 3,
            'tier_name': 'Angostura 1919 Single Barrel',
            'criteria': 'Individual barrel selection at 8+ years, natural color and proof, minimal production — the benchmark Angostura expression showing what the 200-plate distillate becomes with time and tropical wood interaction'
        },
        {
            'tier': 4,
            'tier_name': 'Angostura Royal Oak Select Cask',
            'criteria': 'The ultra-premium expression from the oldest and most developed barrels in Angostura\'s warehouse — natural color, cask strength, no filtration; extremely limited production reserved for the most serious collector and sommelier programs'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 18–20°C neat — the 40% ABV and ultra-clean column still character makes 1919 one of the most accessible neat sipping rums in the Caribbean portfolio; the ultra-clean distillate also makes it the most versatile cocktail rum for Daiquiri, Mai Tai, and rum Old Fashioned applications where the clean base spirit should not compete with modifiers',
        'vessel': 'Rocks glass for neat service (the lighter body benefits from the visual weight of a short glass); Glencairn or tulip acceptable for focused nosing; standard highball for long cocktail applications where the clean base character integrates with other elements',
        'angostura_bitters_connection': 'Serving 1919 with a single dash of Angostura Bitters as a nose modifier is a classic Trinidad service — the botanical complexity of the bitters (gentian, cinchona bark, cinnamon, clove) adds depth to the clean rum\'s vanilla-caramel profile; this also creates an opportunity to explain the shared House of Angostura heritage of both products to guests'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'House of Angostura — 1919 Single Barrel; also Angostura Aromatic Bitters as the essential cocktail companion',
        'north_america_access': 'Angostura 1919 through Diageo distribution (Angostura is Diageo-affiliated); widely available at premium spirits retailers across US and Canada; BCLDB and LCBO carry the standard Angostura age statement range; 1919 Single Barrel through specialty allocation',
        'culinary_application': 'Angostura 1919\'s ultra-clean character makes it the superior base for rum-based cocktail programs in PNW restaurants: Daiquiri classic with Okanagan citrus, rum Old Fashioned with Angostura Bitters and coconut sugar, the Trinidad Sour (Angostura Aromatic Bitters at 1 oz with orgeat and lemon) — the entire Angostura range creates a coherent cocktail program narrative around the House of Angostura\'s 200-year history'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
