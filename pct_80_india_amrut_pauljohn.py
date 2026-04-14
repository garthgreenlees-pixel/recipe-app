import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='India — Bangalore Karnataka (Amrut Intermediate Sherry Single Malt, Oloroso Cask Finish, 920m Deccan Plateau)',
    output_dir='.',
    starting_entry=1,
    session_number=84,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Amrut Distilleries',
    'location': 'Bangalore, Karnataka, India',
    'country': 'India',
    'region': 'Bangalore, Karnataka — 920m Deccan Plateau',
    'key_person': 'Rakshit Jagdale (Managing Director); Surendra Pai (founding distiller)',
    'founded': '1948',
    'production_volume': 'Approximately 3–4 million cases per year across all products; single malt production is a boutique fraction of total output',
    'notable_products': [
        'Amrut Single Malt (original expression)',
        'Amrut Fusion (Indian + Scottish barley)',
        'Amrut Intermediate Sherry (Oloroso cask)',
        'Amrut Cask Strength',
        'Amrut Peated',
        'Amrut Portonova (port finish)',
    ],
    'certifications': ['ISO 9001', 'FSSAI certified'],
    'website': 'amrutdistilleries.com',
    'philosophy': (
        'Amrut was the first Indian distillery to release a single malt '
        'whisky for international sale (2004, Edinburgh) and the first '
        'to document the scientific basis of tropical aging — '
        'the combination of 920m altitude and Bangalore\'s '
        'semi-arid tropical climate produces an angel\'s share '
        '(evaporation loss) of 12–16% per year versus 2–3% '
        'in Scotland, meaning that a 3-year Amrut single malt '
        'undergoes the equivalent wood-extract interaction '
        'of a 9–12 year Scottish whisky.'
    ),
    'trail_connection': 'PCT-8 (India spirits node)',
    'verified': True
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'John Distilleries (Paul John)',
    'location': 'Cuncolim, Goa; maturation warehouses in Goa and Karnataka, India',
    'country': 'India',
    'region': 'Goa (distillation and primary maturation)',
    'key_person': 'Michael D\'Souza (Master Distiller); Paul P. John (founder)',
    'founded': '1996 (distillery); Paul John whisky launched 2012',
    'production_volume': 'Boutique single malt — under 500,000 bottles per year internationally',
    'notable_products': [
        'Paul John Brilliance (unpeated Indian barley)',
        'Paul John Bold (heavily peated)',
        'Paul John Edited (lightly peated)',
        'Paul John Christmas Edition (annual release)',
    ],
    'certifications': ['IWSC award recognition', 'Icons of Whisky (UK) — Indian Whisky Distillery of the Year 2018'],
    'website': 'pauljohnwhisky.com',
    'philosophy': (
        'Paul John uses 100% Indian six-row barley (from Rajasthan '
        'and Uttar Pradesh) and distills in copper pot stills '
        'in Goa — using the monsoon climate and coastal humidity '
        'of the Goan coast as a deliberate aging tool that '
        'produces a distinctive spice-forward aromatic profile '
        'unlike either Scottish single malt or Amrut\'s '
        'inland plateau style.'
    ),
    'trail_connection': 'PCT-8 (Goa — India spirits node)',
    'verified': True
})

# --- REGION 1: Amrut Intermediate Sherry ---
session.add_beverage({
    'name': (
        'Amrut Intermediate Sherry Single Malt — Oloroso Cask Maturation, '
        '920m Bangalore Deccan Plateau, Tropical Aging Compression, '
        'PCT India Whisky Depth'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'indian_single_malt — Oloroso sherry cask, tropical aging',
    'region': 'India — Bangalore Karnataka (Amrut Intermediate Sherry Single Malt, Oloroso Cask Finish, 920m Deccan Plateau)',
    'terroir_origin': (
        'Amrut Distilleries operates from Bangalore at 920m above sea '
        'level on the Deccan Plateau of Karnataka — a semi-arid '
        'tropical highland with a distinctive bimodal climate: '
        'two monsoon seasons (southwest June–September, northeast '
        'October–December) separated by warm dry periods at '
        '18–35°C. This climate profile produces the most '
        'scientifically documented "tropical aging effect" '
        'in the world: at Bangalore\'s elevation and temperature, '
        'the whisky in cask loses 12–16% of its volume per year '
        'to evaporation (the "angel\'s share"), compared to '
        '1–3% per year in Scotland and 5–8% per year in '
        'lowland tropical aging environments. The consequence '
        'is a 3x–5x acceleration of the barrel extraction '
        'process compared to Scottish maturation conditions — '
        'a 3-year Amrut cask has undergone approximately '
        'the same wood-surface-area-to-spirit-volume '
        'interaction as a 9–15 year Scottish malt at '
        'equivalent fill strength. The Intermediate Sherry '
        'expression adds the Oloroso sherry cask dimension '
        'to this accelerated extraction: the spent Oloroso '
        'sherry cask contributes ellagitannins, oxidised '
        'Palomino grape residue (the source of the dried '
        'fig, raisin, and walnut character), and the '
        'colour-contributing anthocyanin-tannin complex '
        'of the Pedro Ximénez or Oloroso residue. '
        'The barley is sourced from the Rajasthan and '
        'UP six-row barley cultivars with higher protein '
        'content than Scottish two-row barley — the '
        'protein difference is a significant terroir '
        'factor in the spirit character, producing a '
        'richer, more cereal-forward new-make spirit.'
    ),
    'production_technique': (
        'Amrut Intermediate Sherry production begins with '
        'Indian six-row barley (primarily from Rajasthan) '
        'that is malted in India (Amrut operates its own '
        'malting floor) and mashed at Bangalore. The '
        'mash tun operates on a standard infusion mash '
        'protocol (65°C single-temperature infusion) '
        'producing a wort at 1.056–1.060 original gravity. '
        'Fermentation uses Amrut\'s house yeast strain '
        '(undisclosed; a Scotch distillery-type S. cerevisiae '
        'strain) for 72–96 hours at 28–32°C — warmer than '
        'Scottish distillery fermentation (18–22°C) '
        'but deliberately managed to develop the higher '
        'ester profile that contributes to the Amrut '
        'tropical fruit character. The wash (8–9% ABV) '
        'is double-distilled in copper pot stills — '
        'the traditional Scotch whisky distillation '
        'protocol adopted by Amrut — with the spirit '
        'still producing a new-make spirit at approximately '
        '67–70% ABV. The new-make spirit is filled into '
        'the first-fill Oloroso sherry butts (500L '
        'Spanish oak, Jerez-seasoned) at 63.5% ABV — '
        'the standard Scottish barrel entry proof adopted '
        'by Amrut. The critical production distinction '
        'of Intermediate Sherry: the whisky is first '
        'matured in ex-bourbon American white oak '
        'barrels for approximately 1.5–2 years '
        '(the "intermediate" aging phase), then '
        'transferred to the Oloroso sherry butts for '
        'a final 0.5–1 year of finishing. This '
        '"interrupted" maturation protocol — '
        'bourbon base, sherry finish — is designed '
        'to develop the clean cereal-and-fruit '
        'character of the bourbon maturation while '
        'adding the dried fruit, walnut, and '
        'oxidised-wine tannin of the Oloroso '
        'cask without over-extracting the '
        'sulphur compounds that can result from '
        'full-term sherry butt maturation. '
        'At Bangalore\'s 12–16% annual evaporation '
        'rate, a total maturation of 2–3 years '
        'in the tropical highland climate produces '
        'a spirit with the flavour development '
        'equivalent to 6–15 years in Scotland.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Scotch single malt, GlenDronach 15 Year Oloroso (Highland, Speyside)',
            'beverage': 'GlenDronach 15 Year — Oloroso Sherry Cask Maturation, Highland, Scotland',
            'connection': (
                'Amrut Intermediate Sherry and GlenDronach 15 Year share '
                'the defining production decision of full Oloroso sherry '
                'cask maturation — both use the same Jerez Oloroso '
                'butts (500L Spanish oak) to develop the dried fruit, '
                'walnut, and oxidised wine tannin character that '
                'defines the sherry-matured single malt style. '
                'The divergence is the aging duration and climate: '
                'GlenDronach achieves its sherry character in 15 years '
                'of Scottish highland maturation (2–3% annual loss); '
                'Amrut achieves a comparable sherry character '
                'in 2.5–3.5 years of Bangalore tropical plateau '
                'maturation (12–16% annual loss). This is the '
                'central technical demonstration of the '
                'Amrut Intermediate Sherry expression: '
                'that tropical accelerated maturation can '
                'replicate the qualitative output of extended '
                'cool-climate maturation in a fraction of the '
                'calendar time, challenging the assumption '
                'that "age" is a quality proxy in whisky.'
            )
        },
        {
            'tradition': 'spirits — rum (Jamaica pot still, high-ester tropical aging)',
            'beverage': 'Appleton Estate 15 Year — Jamaica Tropical Aging, Pot Still, High Ester Rum',
            'connection': (
                'The tropical aging compression effect documented '
                'at Amrut Bangalore has a direct parallel in '
                'Jamaica\'s long tradition of high-ester tropical '
                'rum maturation, where the combination of pot '
                'still distillation and Caribbean tropical '
                'climate aging (6–8% annual evaporation) '
                'produces a spirit depth and complexity per '
                'calendar year that exceeds temperate-climate '
                'aging. Appleton Estate\'s 15-year expressions '
                'and Amrut\'s 3-year expressions occupy similar '
                'quality registers not despite their different '
                'ages but because both are calibrated to the '
                'maximum wood extraction the tropical climate '
                'makes possible — both are "fully matured" '
                'in the technical sense of complete barrel '
                'integration at their respective ages; '
                'the calendar difference is the climate, '
                'not the spirit.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber with red-mahogany highlights from the '
            'Oloroso sherry cask contribution — the characteristic '
            'colour of sherry-matured Indian single malt after '
            '2.5–3 years in 500L Oloroso butts under '
            'tropical acceleration; significantly darker than '
            'bourbon-only Indian single malt at equivalent age; '
            'brilliant clarity (light chill filtration at '
            '46–48% ABV bottling strength for the Intermediate '
            'Sherry); pronounced legs from the full body '
            'of the Oloroso-enriched spirit.'
        ),
        'nose': (
            'Rich dried fruit (raisins, dried fig, Medjool dates) '
            'as the immediate sherry cask signature — the Oloroso '
            'residue anthocyanin-tannin complex contributing '
            'the characteristic dark fruit register; beneath, '
            'the Indian six-row barley cereal character '
            '(richer and more biscuity than Scottish two-row '
            'malt) persists through the sherry overlay; '
            'dark chocolate and walnut from the Oloroso '
            'oxidised wine tannin; cinnamon and clove from '
            'the Spanish oak ellagitannin extraction; '
            'the characteristic Amrut tropical fruit '
            'freshness (mango, dried tropical fruit) '
            'from the Bangalore plateau ester development; '
            'very little sulphur (the intermediate protocol '
            'was designed to avoid the "match stick" '
            'sulphur compound that can afflict '
            'full-term poorly vented sherry butt maturation); '
            'at 46–48% ABV, the aromatic concentration '
            'is substantial without the burning heat '
            'that obscures aroma at cask strength.'
        ),
        'palate': (
            'Full body with notable viscosity from the Oloroso '
            'tannin-glycerol contribution; the entry is '
            'immediately dominated by the dried fruit and dark '
            'chocolate of the sherry cask, transitioning '
            'through the mid-palate to the rich Indian '
            'barley cereal sweetness; the Bangalore '
            'tropical fruit ester register (mango, '
            'dried apricot) emerges at mid-palate '
            'as a distinctive signature that has '
            'no parallel in Scottish sherry-matured '
            'malt — a "tropical sherry" hybrid '
            'character unique to Indian single malt; '
            'the tannin from the Oloroso cask '
            'provides gentle drying structure at '
            'the finish without astringency; '
            'very long finish (50–70 seconds) '
            'with dried fruit, dark chocolate, '
            'and the lingering warmth of the '
            'well-integrated alcohol at '
            '46% ABV.'
        ),
        'conclusion': (
            'The technical reference for tropical accelerated '
            'sherry cask maturation: demonstrating that '
            'Oloroso cask character of equivalent complexity '
            'to Scottish 12–15 year sherry maturation '
            'can be achieved in 2.5–3.5 years at '
            'Bangalore\'s 920m Deccan plateau climate.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Amrut Intermediate Sherry Single Malt (46% ABV, '
                'limited release) — the benchmark tropical Oloroso '
                'cask expression; or Amrut Cask Strength (61–63% ABV) '
                'from a single exceptional Oloroso butt; consistent '
                'gold and platinum recognition at IWSC, ISC, and '
                'Jim Murray\'s Whisky Bible (scored 97.5/100 for '
                'Amrut Fusion in 2010, establishing the distillery\'s '
                'international credibility); priced at USD $50–80 '
                'per 750ml internationally.'
            ),
            'markers': (
                'Oloroso cask intermediate protocol; 46%+ ABV; '
                'tropical fruit-sherry hybrid aromatic; '
                'award recognition; no chill filtration.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Amrut Single Malt (46% ABV, ex-bourbon only) '
                'or Amrut Fusion (Indian + Scottish barley blend) '
                '— the distillery\'s entry-level single malt '
                'expressions that established Indian single malt '
                'in international fine spirits retail; '
                'demonstrates the Bangalore tropical aging '
                'character without the sherry cask overlay; '
                'priced at USD $35–50 per 750ml.'
            ),
            'markers': (
                'Ex-bourbon maturation; 46% ABV; tropical fruit '
                'forward; Indian barley cereal base; '
                'consistent international distribution.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Other Indian single malt expressions in the '
                'professional retail range — Rampur Select (Allied '
                'Blenders), Indri Trini (Piccadily Distilleries) '
                '— competent single malt distillation from '
                'Indian barley with tropical aging character '
                'but without the specific Bangalore plateau '
                'altitude terroir of Amrut; priced at '
                'USD $30–45 per 750ml.'
            ),
            'markers': (
                'Indian barley; tropical aging; professional '
                'quality level; growing international '
                'distribution; without Amrut\'s altitude terroir.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Blended Indian whisky labelled as Indian malt '
                'or Indian whisky — McDowell\'s No. 1, Royal Stag, '
                'Officer\'s Choice — which uses a small percentage '
                'of malt spirit blended with high-proportion '
                'neutral grain spirit (typically from sugarcane '
                'molasses); the dominant Indian domestic whisky '
                'market segment by volume but not related in '
                'production or quality to the Amrut single malt '
                'tradition; the entry-level Indian spirits category.'
            ),
            'markers': (
                'High neutral grain spirit proportion; '
                'molasses base; domestic Indian market; '
                'no altitude or terroir character; '
                'priced under USD $5 domestically.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Amrut Intermediate Sherry at room temperature '
            '(18–22°C) in a Glencairn without ice; the full '
            'aromatic complexity of the Oloroso cask-tropical '
            'aging combination requires room temperature to '
            'express — cold temperatures suppress the dried '
            'fruit volatiles and the Indian barley tropical '
            'fruit esters that define the Bangalore single '
            'malt character; a small water addition '
            '(2–4ml to a 45ml pour) can open the nose '
            'significantly if the spirit was just opened; '
            'never serve over ice as dilution destroys '
            'the carefully balanced Oloroso-sherry '
            'aromatic architecture.'
        ),
        'vessel': (
            'Glencairn glass exclusively for evaluation and '
            'programme service; 40–45ml pour; the Glencairn\'s '
            'chimney concentrates the dried fruit-tropical '
            'fruit aromatic complex for evaluation while '
            'preventing the high-ester volatiles from '
            'dispersing too rapidly. In a programme context, '
            'the verbal presentation of the tropical aging '
            'acceleration is the essential service element: '
            '"this three-year-old whisky from 920 metres '
            'above sea level in Bangalore has lost more '
            'than a third of its original volume to the '
            'angel\'s share — there is no other '
            'distillery in the world where the wood '
            'works this fast."'
        ),
        'technique': 'Neat; Glencairn; tropical aging explanation is the verbal centrepiece.',
        'programme_position': (
            'Indian single malt comparison flight alongside Paul John '
            'Brilliance (Goa coastal climate, unpeated) — same '
            'category, different Indian terroirs; or in a '
            'global single malt climate comparison alongside '
            'Kavalan (Taiwan sub-tropical), Starward (Melbourne '
            'maritime), and Glenfarclas 15 (Scottish highland) '
            'to demonstrate how climate shapes whisky character.'
        ),
        'verbal_presentation': (
            'Bangalore, 920 metres. The air here takes 12 to 16 '
            'percent of the barrel every year. This three-year-old '
            'malt has been through what a Scottish whisky '
            'would take fifteen years to achieve. '
            'The sherry cask is from Jerez. The barley is from Rajasthan. '
            'Nothing about this is Scottish except the still.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Amrut Distilleries, Bangalore, Karnataka, India '
            '(est. 1948; single malt launched internationally 2004 — '
            'the benchmark for Indian single malt and the first '
            'to document the tropical aging acceleration at Bangalore '
            'altitude; Intermediate Sherry is the definitive '
            'sherry cask expression of the Amrut range).'
        ),
        'producer_location': 'Bangalore, Karnataka, India — 920m Deccan Plateau',
        'key_person': 'Rakshit Jagdale (Managing Director)',
        'production_volume': 'Boutique single malt fraction of larger Amrut group production',
        'certifications': ['IWSC multiple Gold', 'Jim Murray Whisky Bible top 10'],
        'bc_distributor': 'Amrut has been distributed in BC through private agents; verify current status with BCLDB specialty spirits or private import',
        'us_distributor': 'Amrut is distributed in the US by Prestige Beverage Group (national); available at major fine spirits retailers in key markets',
        'uk_distributor': 'Amrut is available at The Whisky Exchange, Master of Malt, and Harvey Nichols in the UK',
        'price_tier': 'Reserve',
        'availability_notes': (
            'Amrut single malt expressions are consistently available '
            'through international fine spirits retailers and online '
            'merchants; Intermediate Sherry is a limited-production '
            'allocation release, not always in stock; Amrut Single '
            'Malt and Fusion are the most widely available expressions. '
            'India retail pricing: INR 4,000–6,000 per 750ml '
            '(USD $48–72); international retail: USD $50–75.'
        )
    },
    'trail_connection': 'PCT-8',
    'trail_note': (
        'Amrut Intermediate Sherry positions the Indian single malt '
        'tradition within the PCT Indian Ocean spirits corridor — '
        'the Bangalore Deccan Plateau altitude and the Rajasthan '
        'six-row barley are distinctly Indian raw material and '
        'terroir, while the Oloroso cask and the double copper '
        'pot still distillation protocol reflect the Portuguese '
        'colonial era exchange of European distillation technology '
        'into the Indian subcontinent that also produced Goa feni.'
    ),
    'food_pairings': [
        {
            'technique_id': 'IND-004',
            'dish': 'Malabar prawn curry with coconut, tamarind, and curry leaf (Kerala-Karnataka coast)',
            'pairing_type': 'bridge',
            'rationale': (
                'The tropical fruit ester character of Amrut '
                'Bangalore maturation (mango, dried apricot) '
                'bridges directly to the coconut-tamarind '
                'sweet-sour balance of Malabar coast curry — '
                'both express the tropical Karnataka-Kerala '
                'terroir through entirely different production '
                'paths; the dried fruit from the Oloroso cask '
                'echoes the tamarind acidity of the curry.'
            )
        }
    ],
    'source': 'Amrut Distilleries technical sheets; IWSC competition records; Jim Murray Whisky Bible 2010; Charles MacLean tropical aging documentation; Milk & Honey distillery comparative aging research',
    'price_trajectory': 'rising'
})

# Switch to Region 2: Paul John
session.switch_region(
    'spirits',
    'India — Goa North (Paul John Brilliance Single Malt, Indian Barley, Monsoon Climate Aging, PCT Distillation Heritage)'
)

session.add_beverage({
    'name': (
        'Paul John Brilliance Single Malt — Indian Six-Row Barley, '
        'Cuncolim Goa Copper Pot Still, Monsoon Climate Coastal Aging, '
        'PCT India Goa Spirits Heritage'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'indian_single_malt — unpeated, ex-bourbon, monsoon coastal',
    'region': 'India — Goa North (Paul John Brilliance Single Malt, Indian Barley, Monsoon Climate Aging, PCT Distillation Heritage)',
    'terroir_origin': (
        'Paul John whisky is distilled at Cuncolim in South Goa '
        '(administrative address in North Goa for production purposes) '
        'by John Distilleries — the same company that produces the '
        'Paul John domestic blended whisky range, with the single '
        'malt production separated as a distinct artisan operation '
        'from 2012 onward. The Goa coastal climate is the defining '
        'terroir factor: at sea level on the Konkan coast, the '
        'maturation environment is significantly warmer and more '
        'humid than Bangalore (where Amrut operates at 920m), '
        'with temperatures of 24–36°C year-round and the '
        'two monsoon seasons (southwest June–September, '
        'northeast October–December) providing high humidity '
        '(70–90% relative humidity during monsoon) that '
        'slows the evaporation rate compared to Bangalore\'s '
        'drier plateau but accelerates the flavour extraction '
        'through wood hydration — the water molecules in '
        'humid air facilitate the transfer of '
        'lignin-breakdown compounds (vanillin, guaiacol) '
        'from the barrel stave into the spirit. '
        'Paul John uses exclusively Indian six-row barley '
        '(from Rajasthan) — the same raw material as Amrut — '
        'but the copper pot still design and the coastal '
        'Goan maturation climate produce a measurably '
        'different spirit character: spicier, more '
        'assertive, and with a distinctive coastal '
        'marine note from the Atlantic (Arabian Sea) '
        'humidity cycling through the warehouse during '
        'monsoon and dry-season alternation. '
        'The PCT historical dimension: Paul John distills '
        'in the same territory — Goa — where the Portuguese '
        'colonial administration documented the first '
        'continuous distillation tradition on the Indian '
        'subcontinent through the feni bhatti system; '
        'the copper pot still in Cuncolim stands on '
        'the same ground where 400 years of Indian '
        'coastal distillation heritage has accumulated.'
    ),
    'production_technique': (
        'Paul John Brilliance begins with Indian six-row barley '
        '(unpeated, typically from Rajasthan) that is malted '
        'and mashed at the Cuncolim facility. The mashing '
        'protocol follows standard Scottish infusion mash '
        'practice (65°C single temperature, 3 waters) '
        'producing a wort at 1.058–1.062 OG; fermentation '
        'uses selected Saccharomyces cerevisiae for '
        '72–96 hours at 28–34°C (the higher temperature '
        'versus Scottish 18–22°C fermentation produces '
        'a more ester-rich wash and a spicier, more '
        'assertive new-make spirit character). The wash '
        'is double-distilled in copper pot stills of '
        'Paul John\'s own design — slightly larger still '
        'necks than the Amrut stills, designed to retain '
        'more of the heavy ester fraction while removing '
        'the lightest heads fraction for a richer '
        'new-make. The Brilliance expression uses '
        'only American white oak ex-bourbon barrels '
        '(180–200L, first fill) with no additional cask '
        'finishing — the maturation is entirely in '
        'ex-bourbon American oak for 4–5 years in '
        'the Cuncolim coastal warehouse. The '
        'humidity cycling of the Goan monsoon '
        'seasons produces a different wood extraction '
        'profile from Bangalore\'s drier plateau: '
        'during monsoon (high humidity), the staves '
        'swell and contract, forcing the spirit deeper '
        'into the wood; during the dry season, '
        'the stave compression releases the '
        'wood-extracted compounds back into the spirit. '
        'This monsoon cycling produces a characteristic '
        'spice-forward profile (cinnamon, clove, nutmeg) '
        'from the lignin-breakdown phenolics released '
        'during the humidity-driven stave compression, '
        'creating the distinctly spicy Goan coastal '
        'Indian single malt character that differentiates '
        'Paul John from the tropical fruit-forward '
        'Bangalore plateau style of Amrut. '
        'Brilliance is bottled at 46% ABV '
        'without chill filtration.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Amrut Single Malt (Bangalore, 920m, Deccan Plateau)',
            'beverage': 'Amrut Intermediate Sherry Single Malt — Bangalore Tropical Plateau Aging',
            'connection': (
                'Paul John Brilliance (Goa coastal, sea level, monsoon humid) '
                'and Amrut Single Malt (Bangalore plateau, 920m, semi-arid) '
                'are the two primary poles of Indian single malt terroir — '
                'both using Indian six-row barley and copper pot still '
                'double distillation, but producing measurably different '
                'characters from their contrasting maturation climates. '
                'The professional comparison: Amrut is tropical fruit '
                'forward (mango, dried apricot, guava) from the dry '
                'plateau ester development; Paul John Brilliance is '
                'spice forward (cinnamon, nutmeg, clove) from the '
                'monsoon humidity-driven lignin phenolic extraction. '
                'Together they define the geographic range of '
                'Indian single malt terroir in the same way that '
                'Islay and Speyside define the geographic range '
                'of Scottish single malt terroir — same raw '
                'material and process, entirely different '
                'environments, entirely different spirits.'
            )
        },
        {
            'tradition': 'spirits — Kavalan single malt (Taiwan, subtropical maritime aging)',
            'beverage': 'Kavalan Concertmaster Port Cask Finish — Yilan Subtropical, Pacific Maritime, Taiwan',
            'connection': (
                'Paul John Brilliance (Goa monsoon coastal) and '
                'Kavalan (Taiwan subtropical maritime) are the two '
                'most technically similar Asian single malt operations: '
                'both distill in tropical/subtropical coastal conditions '
                'with high humidity and significant temperature variation '
                'between seasons; both use copper pot stills and '
                'ex-bourbon casks as the primary maturation vessel; '
                'both produce single malts with accelerated maturation '
                'rates (6–10% annual loss versus 2–3% in Scotland) '
                'that achieve complex aromatic profiles in 4–7 years. '
                'The monsoon-humidity cycling of Paul John and '
                'the Pacific typhoon season of Kavalan are '
                'climatically analogous — both distilleries have '
                'built warehouse designs specifically to manage '
                'the dramatic seasonal humidity variation of '
                'their Asian coastal locations, and both have '
                'developed house styles that celebrate rather '
                'than attempt to mitigate the tropical '
                'aging acceleration.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Pale amber-gold with green-yellow highlights — '
            'the characteristic colour of young ex-bourbon '
            'American white oak maturation on an Indian barley '
            'new-make spirit; lighter in colour than Amrut '
            'Intermediate Sherry (no sherry cask contribution); '
            'brilliant clarity; medium-weight legs at 46% ABV '
            'indicating good extract without the heavy viscosity '
            'of sherry-matured expressions.'
        ),
        'nose': (
            'The opening register is immediately distinctive: '
            'cinnamon, dried ginger, and nutmeg from the '
            'monsoon-cycling phenolic extraction dominate '
            'the spice register in a way that has no equivalent '
            'in Scottish or Irish single malt; beneath, '
            'vanilla pod and light caramel from the '
            'American white oak lactone extraction; '
            'dried mango and jackfruit from the '
            'Indian barley ester development under '
            'Goa coastal conditions; a distinctive '
            'coastal marine note (dried seaweed, '
            'sea salt minerality) from the Arabian '
            'Sea humidity influence in the warehouse; '
            'light fresh oak from the ex-bourbon '
            'barrel contribution; the overall profile '
            'is cleaner and more aromatic than the '
            'Intermediate Sherry expression — '
            'Brilliance is designed to demonstrate '
            'the house Indian barley character '
            'without cask overlay.'
        ),
        'palate': (
            'Medium-full body; the entry is spice-forward '
            '(cinnamon, nutmeg) consistent with the nose — '
            'the Goa coastal phenolic profile is immediately '
            'apparent; the mid-palate develops the vanilla '
            'and dried mango tropical fruit character '
            'of the Indian barley; light marine saltiness '
            'in the mid-to-finish transition from the '
            'coastal humidity influence; the finish '
            'is long (40–55 seconds) with warming '
            'spice (cinnamon, black pepper) and '
            'persistent vanilla from the American '
            'oak; the 46% ABV is well-integrated '
            'with the spirit character — not hot '
            'or burning but gently warming through '
            'the finish; a second sip without water '
            'develops the dried fruit and spice '
            'integration further as the glass '
            'temperature opens the lighter '
            'aromatic compounds.'
        ),
        'conclusion': (
            'Paul John Brilliance is the single-varietal, '
            'no-cask-overlay expression of what Goa coastal '
            'monsoon climate does to Indian six-row barley '
            'in an American oak barrel — spicy, aromatic, '
            'and distinctly non-Scottish in character. '
            'The PCT reference for the Goa spirits terroir.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Paul John Christmas Edition (annual limited release — '
                'the most decorated Paul John expression each year) '
                'or Paul John Selected Cask (single barrel, cask strength) '
                '— the benchmark tier for Goa coastal Indian single '
                'malt; typically wins IWSC Gold or ISC Gold in the '
                'year of release; limited allocation internationally; '
                'priced at USD $70–120 per 750ml.'
            ),
            'markers': (
                'Limited annual release; cask strength or '
                'special cask; IWSC/ISC gold recognition; '
                'spice-forward aromatic at full expression; '
                'single barrel documentation.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Paul John Brilliance (46% ABV, unpeated) and '
                'Paul John Bold (peated, 46% ABV) — the core '
                'range expressions demonstrating the two poles '
                'of Paul John\'s production range (unpeated '
                'for the coastal spice character; peated for '
                'the peat-smoke interaction with the monsoon '
                'climate); consistently available internationally '
                'at USD $40–55 per 750ml.'
            ),
            'markers': (
                'Core range; 46% ABV; ex-bourbon only; '
                'unpeated or peated expression; '
                'consistent international distribution.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Paul John Edited (lightly peated, entry-level '
                'in the Paul John range) — a competent expression '
                'of the Goa coastal character at a lower price '
                'point with less aging depth than Brilliance '
                'or Bold; suitable for cocktail use in Indian '
                'single malt highballs where the full aromatic '
                'complexity of the higher expressions would '
                'be diluted by mixer; priced at USD $30–40.'
            ),
            'markers': (
                'Lightly peated; entry Paul John range; '
                'less aging depth; cocktail tier use.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Paul John domestic blended whisky (the John '
                'Distilleries primary volume production) — '
                'the high-volume domestic Indian blended '
                'whisky market product using neutral grain '
                'spirit blended with a small single malt '
                'fraction; the same company but an entirely '
                'different product category from Paul John '
                'single malt; not exported internationally.'
            ),
            'markers': (
                'Blended Indian whisky; high neutral grain spirit; '
                'domestic market only; no single malt character.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve Paul John Brilliance neat at 18–22°C; '
            'the spice-forward character of the Goa coastal '
            'climate aging is best expressed at room temperature; '
            'the warming cinnamon-nutmeg register amplifies '
            'with the slight temperature increase that occurs '
            'as the glass is held; a 2–3ml water addition '
            'to a 45ml pour opens the dried tropical fruit '
            'character considerably if the bottle has just '
            'been opened; never chill as the spice volatiles '
            'are suppressed below 15°C.'
        ),
        'vessel': (
            'Glencairn or Copita (100–150ml) with 40–45ml pour; '
            'for a formal programme comparison flight with Amrut, '
            'use identical Glencairns with small water vessels '
            'alongside to allow guests to find their preferred '
            'dilution; the comparative presentation of Amrut '
            '(tropical fruit forward, dry plateau) versus '
            'Paul John Brilliance (spice forward, coastal '
            'monsoon) is the most instructive Indian single '
            'malt education possible in two glasses. '
            'Service phrase: "Same Indian barley. Same copper '
            'pot still. One made 920 metres above sea level '
            'in the Deccan. One made at sea level in Goa '
            'during the monsoon. Find the difference."'
        ),
        'technique': 'Neat; comparative service with Amrut recommended; Glencairn essential.',
        'programme_position': (
            'Indian single malt comparison flight (position 2 after Amrut); '
            'or global single malt climate flight alongside Kavalan '
            '(Taiwan), Starward (Melbourne), and Glenfarclas '
            '(Scottish highland); PCT India spirits flight '
            'alongside Goa feni as the colonial distillation '
            'heritage arc from bhatti pot to modern copper pot.'
        ),
        'verbal_presentation': (
            'Goa. Sea level. Monsoon. The same barley as Amrut, '
            'the same Scottish distillation method, but here '
            'the humidity swings 40 percent between June and '
            'December. That swing is in the glass. '
            'Find the spice — that is the monsoon.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'John Distilleries (Paul John), Cuncolim, Goa, India '
            '(est. 1996; single malt launched internationally 2012; '
            'the benchmark for Goa coastal Indian single malt; '
            'Icons of Whisky Indian Distillery of the Year 2018; '
            'Michael D\'Souza is the defining master distiller '
            'for the monsoon-coastal style).'
        ),
        'producer_location': 'Cuncolim, South Goa, India',
        'key_person': 'Michael D\'Souza (Master Distiller)',
        'production_volume': 'Under 500,000 bottles/year internationally',
        'certifications': ['Icons of Whisky — Indian Distillery of the Year 2018', 'IWSC Gold multiple years'],
        'bc_distributor': 'Paul John has distribution in BC; verify current BCLDB listing or private import agent',
        'us_distributor': 'Paul John is distributed in the US by Quintessential Brands / Proximo Spirits; nationally available at fine spirits retailers',
        'uk_distributor': 'Paul John is widely distributed in the UK — The Whisky Exchange, Master of Malt, and Harvey Nichols carry the core range',
        'price_tier': 'Estate',
        'availability_notes': (
            'Paul John Brilliance is the most widely available '
            'Paul John expression internationally; USD $40–55 '
            'per 750ml; India retail INR 3,500–4,500 per 750ml. '
            'Bold (peated) and Christmas Edition are also '
            'available at major fine spirits retailers. '
            'Paul John has strong UK and European distribution '
            'through the Icons of Whisky recognition; '
            'North American distribution is growing rapidly '
            'through 2025–2026.'
        )
    },
    'trail_connection': 'PCT-8',
    'trail_note': (
        'Paul John Brilliance connects the PCT Goa spirits heritage '
        'narrative directly — Cuncolim is within the same Goa '
        'coastal geography as the South Goa coconut feni bhatti '
        'villages; the copper pot still in Cuncolim stands as '
        'the modern successor to the copper bhann of the '
        'traditional feni tradition, both tracing their '
        'distillation technology to the Portuguese colonial '
        'exchange of European copper-pot distillation '
        'into the Konkan coastal region from the 16th century.'
    ),
    'food_pairings': [
        {
            'technique_id': 'IND-005',
            'dish': 'Goan xacuti (chicken or goat curry with roasted coconut, Kashmiri chilli, star anise, cinnamon)',
            'pairing_type': 'complement',
            'rationale': (
                'The cinnamon-nutmeg-clove spice register of Paul John '
                'Brilliance directly bridges to the roasted coconut '
                'and whole-spice base of Goan xacuti — the same '
                'spice profile that the monsoon climate extracts '
                'from the American oak barrel is the core spice '
                'vocabulary of Goan colonial spice cuisine; '
                'the spirit spice amplifies the xacuti spice '
                'without competing.'
            )
        },
        {
            'technique_id': 'IND-006',
            'dish': 'Bebinca (Goan layered coconut-egg-sugar pudding)',
            'pairing_type': 'bridge',
            'rationale': (
                'The vanilla and caramel of the American oak aging '
                'in Paul John Brilliance bridges to the slowly '
                'baked caramelised coconut-egg layers of bebinca; '
                'within-Goa pairing where the spice of the whisky '
                'provides aromatic contrast to the sweet richness '
                'of the colonial confection.'
            )
        }
    ],
    'source': 'Paul John Distillery technical documentation; John Distilleries export records; IWSC competition records; Icons of Whisky award records; Michael D\'Souza interview records via whisky trade press',
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
