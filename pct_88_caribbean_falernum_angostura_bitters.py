import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fermented',
    region='Caribbean — Lesser Antilles (Falernum, Spiced Sugarcane Syrup, Bajan Heritage, PCT Cocktail Bridge)',
    output_dir='.',
    starting_entry=1,
    session_number=92,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'John D. Taylor\'s Velvet Falernum (R.L. Seale & Co. — Foursquare Distillery production)',
    'location': 'Christ Church, Barbados',
    'country': 'Barbados',
    'region': 'Barbados — Christ Church Parish; produced at Foursquare Distillery, the Barbadian craft distillery of R.L. Seale & Co.',
    'key_person': 'Richard Seale — Master Distiller, Foursquare; the Seale family are the custodians of the Foursquare Distillery that produces John D. Taylor\'s Velvet Falernum under the original 19th-century formula',
    'founded': '1890 (original John D. Taylor recipe); the Taylor\'s Velvet Falernum brand was acquired and is currently produced by R.L. Seale & Co. at Foursquare Distillery',
    'production_volume': 'Moderate commercial production; Velvet Falernum is a widely distributed cocktail ingredient in the international bartending trade',
    'notable_products': [
        'John D. Taylor\'s Velvet Falernum (11% ABV — the reference alcoholic falernum)',
        'Foursquare Exceptional Cask Series (the distillery\'s rum flagship)',
        'BRT (Barbados Rum Distillery products)',
    ],
    'certifications': ['Barbados rum production regulatory compliance; Foursquare is the most award-winning rum distillery in Barbados as of 2026'],
    'website': 'www.foursquaredistillery.com',
    'philosophy': (
        'R.L. Seale and Foursquare Distillery represent the Barbadian '
        'craft production tradition — the production of both the John D. '
        'Taylor\'s Velvet Falernum and the Foursquare Exceptional Cask '
        'Series within the same facility demonstrates the range of the '
        'Bajan distilling tradition from cocktail ingredient to internationally '
        'acclaimed aged rum.'
    ),
    'trail_connection': 'PCT (Caribbean — Barbados cocktail ingredient node)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Falernum — Barbados Spiced Lime-Ginger-Almond Liqueur, John D. Taylor\'s Velvet Falernum, '
        'PCT Caribbean Cocktail Bridge Ingredient, Pisco Sour Connection'
    ),
    'tradition': 'fermented',
    'sub_tradition': 'cocktail_syrup — alcoholic falernum (11% ABV); Barbados-origin spiced sugarcane liqueur with lime, ginger, almond, cloves; the reference cocktail bridge ingredient of the PCT Caribbean arc',
    'region': 'Caribbean — Lesser Antilles (Falernum, Spiced Sugarcane Syrup, Bajan Heritage, PCT Cocktail Bridge)',
    'terroir_origin': (
        'Falernum is a Barbados-origin spiced sugarcane liqueur '
        'with roots in the 18th-century colonial Caribbean rum culture — '
        'the combination of Barbadian sugarcane spirit (rum) '
        'with the spices, citrus, and botanical flavourings '
        'available in the colonial Caribbean trade: '
        'lime (Citrus aurantifolia — the West Indian lime, '
        'dominant in Barbados since colonial importation '
        'from the Malay Archipelago by Portuguese and '
        'Spanish traders), ginger (Zingiber officinale — '
        'introduced to the Caribbean from South and Southeast '
        'Asia via the Indian Ocean and Atlantic spice trade), '
        'almonds (Prunus dulcis — brought to the Caribbean '
        'from the Mediterranean trade via the same colonial '
        'networks), and cloves (Syzygium aromaticum — '
        'from the Maluku Islands through the Portuguese '
        'spice trade). The geographical terroir of '
        'falernum is thus not a single place but a '
        'convergence of the entire PCT spice trade '
        'network in a single bottle: the Barbados rum '
        'base (Caribbean colonial sugarcane), the lime '
        '(Southeast Asian citrus via Portuguese maritime '
        'botany), the ginger (South Asian spice via '
        'Indian Ocean trade), the almond (Mediterranean), '
        'and the clove (Maluku Islands via Portuguese spice '
        'monopoly). Falernum is the PCT cocktail ingredient '
        'in its most concentrated form — a colonial trade '
        'route in liquid form. The John D. Taylor formula '
        'dates to approximately 1890 in Barbados; '
        'the alcoholic version (Velvet Falernum, 11% ABV) '
        'is the professional bartending reference expression, '
        'as distinguished from the non-alcoholic syrup '
        'version used in domestic contexts.'
    ),
    'production_technique': (
        'John D. Taylor\'s Velvet Falernum production begins '
        'with a Barbadian white rum base (pot-column hybrid '
        'distillate from Foursquare, diluted to 11% ABV '
        'in the finished product) into which the botanical '
        'maceration takes place: fresh West Indian limes '
        '(zest and juice), fresh ginger root (Zingiber '
        'officinale, grated), blanched almonds (Prunus '
        'dulcis, ground to a coarse paste), whole cloves '
        '(Syzygium aromaticum), and aromatic sweetener '
        '(sugarcane-derived syrup or sucrose solution). '
        'The maceration period is proprietary but '
        'approximately 2–4 weeks for the fresh botanicals '
        'in the rum base; the botanical infusion is '
        'filtered and blended with additional sugarcane '
        'syrup to achieve the target sweetness (falernum '
        'is a liqueur — typically 200–300g/L sugar '
        'in the non-alcoholic syrup; 150–200g/L in the '
        'alcoholic Velvet Falernum). Some small-batch '
        'bartender-produced falernum recipes also include '
        'vanilla (Vanilla planifolia — the Mexican vanilla '
        'orchid introduced to the Caribbean via the same '
        'colonial botanical transfer networks) and '
        'allspice (Pimenta dioica — the only major spice '
        'indigenous to the New World, from Jamaica, '
        'giving Caribbean falernum a within-hemisphere '
        'botanical alongside the imported spice complex). '
        'The production of falernum in the 18th–19th '
        'century Barbados context was the household-level '
        'spice maceration of the colonial Caribbean '
        'domestic tradition — every household in '
        'Barbados with access to the colonial spice '
        'trade would have produced its own version '
        'of the lime-ginger-almond-rum maceration '
        'as a digestif, cocktail ingredient, and '
        'medicinal cordial. The John D. Taylor\'s '
        'formula codified one version of this '
        'household tradition into the commercial '
        'product that became the international '
        'bartending reference in the 20th century.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Italian amaro (Campari, Aperol — botanical maceration in spirit base)',
            'beverage': 'Campari — Italian Bitter Botanical Liqueur, Milanese Aperitivo Tradition',
            'connection': (
                'Caribbean falernum and Italian amaro (Campari, Aperol, '
                'Cynar) are both botanical maceration spirits — the same '
                'production architecture (dried or fresh botanicals '
                'macerated in an alcohol base, filtered, sweetened, '
                'and bottled at liqueur strength) applied to radically '
                'different botanical palettes in different colonial '
                'trade contexts. Campari\'s formula (1860, Gaspare '
                'Campari, Milan) uses a bitter botanical palette '
                '(gentian, cascarilla, rhubarb root) optimised '
                'for the Italian aperitivo tradition; falernum '
                'uses a sweet-spiced palette (lime, ginger, almond, '
                'clove) optimised for the Caribbean rum cocktail '
                'tradition. Both are colonial-era commercial '
                'codifications of household botanical maceration '
                'practices that preceded the commercial product '
                '— Campari formulating the domestic Italian '
                'digestif tradition; falernum codifying the '
                'Barbadian colonial spice liqueur tradition. '
                'The PCT connection: falernum and Campari both '
                'appear in the PCT cocktail programme — falernum '
                'in the Zombie and ti\' punch extensions; '
                'Campari in the Negroni which itself connects '
                'to the British colonial gin tradition.'
            )
        },
        {
            'tradition': 'spirits — Orgeat (French almond syrup — the same almond-sweet botanical base)',
            'beverage': 'Orgeat — Almond Syrup, French Provençal, Mediterranean Almond Heritage',
            'connection': (
                'Caribbean falernum and French orgeat share the '
                'same almond botanical foundation — both are '
                'almond-flavoured cocktail sweetening agents '
                'built on the Mediterranean Prunus dulcis '
                'harvest tradition. Orgeat (from French orge, '
                'barley — the original medieval recipe used '
                'barley as well as almond) is a pure almond '
                'emulsion sweetener without alcohol; falernum '
                'uses the almond as one of its botanical components '
                'in a complex spiced-citrus-rum maceration. '
                'The connection illuminates the PCT botanical '
                'transfer network: the same Prunus dulcis '
                'from the Mediterranean almond groves '
                'that arrived in Caribbean falernum also '
                'arrived in French orgeat through '
                'parallel trade routes, and both are '
                'used as cocktail sweetening agents '
                'across the global bartending repertoire — '
                'orgeat in the Mai Tai (which itself '
                'has Caribbean rum connections); '
                'falernum in the Zombie and Corn \'n\' Oil '
                '(Barbados rum and falernum). '
                'In the PCT programme, both appear '
                'as complementary botanical sweeteners '
                'in the cocktail section.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Water-clear to very pale straw-gold — the falernum '
            'is filtered clear of the botanical macerate particles; '
            'the slight golden tinge from the rum base and the '
            'lime zest oils; at 11% ABV (Velvet Falernum) '
            'the liquid has the slightly viscous, oily texture '
            'of a liqueur; the legs are slow and sweet '
            'from the 150–200g/L dissolved sugar. '
            'The non-alcoholic syrup version is thicker '
            'and more golden from the additional sugarcane '
            'syrup concentration.'
        ),
        'nose': (
            'The dominant aromatic of Velvet Falernum is the '
            'West Indian lime zest — the essential oil compounds '
            '(limonene, citral) of Citrus aurantifolia, which '
            'has a more floral-citral intensity than the '
            'Persian lime (Citrus latifolia) of the European '
            'market; this lime-zest freshness is the defining '
            'aromatic of the Barbados falernum tradition. '
            'Behind the lime: the sharp-warm spice of ginger '
            '(gingerol and shogaol volatile compounds '
            'from the Zingiber officinale maceration); '
            'the marzipan sweetness of the almond maceration '
            '(benzaldehyde — the characteristic bitter almond '
            'aromatic compound of Prunus dulcis); '
            'the warm clove background (eugenol — '
            'the phenolic compound of Syzygium aromaticum '
            'that gives clove its characteristic warm-spice '
            'register); and the underlying Barbadian rum '
            'base (the light, clean funnel-character of '
            'a pot-column hybrid distillate at 11% ABV).'
        ),
        'palate': (
            'The entry of Velvet Falernum is sweetness-forward '
            '(150–200g/L sugar) with the immediate lime-citral '
            'brightness cutting through the sugar; the mid-palate '
            'develops the ginger heat (gingerol is not volatile '
            'on the nose at 11% ABV but is released on the '
            'palate by saliva enzymes) and the marzipan-almond '
            'sweetness simultaneously; the clove eugenol '
            'provides the warm, slightly numbing spice finish '
            '(eugenol is a mild local anaesthetic — the '
            'characteristic slight mouth-warming of clove '
            'in cocktail applications); the rum base is '
            'barely perceptible at 11% ABV but provides '
            'the backbone structure for the sweetener. '
            'The finish is medium (20–25 seconds) with '
            'the lime-ginger-clove spice triad persisting; '
            'the almond benzaldehyde contributes the '
            'classic marzipan aftertaste. Consumed neat '
            'over ice as a sipping drink in Caribbean '
            'tradition (Corn \'n\' Oil: Bajan dark rum, '
            'falernum, lime, Angostura bitters) or '
            'as a cocktail modifier in international '
            'bartending.'
        ),
        'conclusion': (
            'The PCT Caribbean cocktail bridge ingredient par excellence — '
            'a single bottle encoding the colonial trade route spice '
            'convergence of lime (Southeast Asia), ginger (South Asia), '
            'almond (Mediterranean), clove (Maluku Islands), '
            'and sugarcane rum (West African-Caribbean plantation). '
            'The entire PCT geographic arc in a cocktail modifier.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Hand-crafted bartender falernum produced in small batches '
                'using fresh West Indian limes (not lime juice concentrate), '
                'fresh ginger root (not dried powder), high-grade raw almonds, '
                'and a premium Barbadian aged rum base (Foursquare '
                'reserve-grade white rum at 50%+ ABV pre-dilution); '
                'extended maceration (4–6 weeks); filtered through '
                'fine muslin; sweetened with raw cane syrup (not '
                'commercial glucose solution). The reserve tier '
                'exists in the craft bartending world (New York, '
                'London, Sydney craft cocktail bars produce their '
                'own house falernum) but no commercial product '
                'has been identified at this quality tier. '
                'Expected aromatic: the most vivid lime-ginger-clove '
                'complex with rum integration.'
            ),
            'markers': (
                'Fresh botanicals; premium rum base; extended maceration; '
                'cane syrup; hand-crafted; craft bar production.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'John D. Taylor\'s Velvet Falernum (11% ABV, Foursquare, '
                'Barbados) — the international commercial benchmark; '
                'the formula that defines the falernum flavour profile '
                'for professional bartending globally; clean lime-ginger-'
                'almond-clove complexity with a Barbadian rum backbone; '
                'consistent across all international markets. '
                'EUR/USD 15–25 per 750ml.'
            ),
            'markers': (
                'John D. Taylor\'s Velvet Falernum; Foursquare production; '
                '11% ABV; lime-ginger-almond-clove; Barbados rum base; '
                'international benchmark.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Non-alcoholic falernum syrup (0% ABV) — the domestic '
                'Caribbean version and cocktail modifier used in '
                'tropical drinks at beach bars and commercial venues; '
                'the sugarcane syrup base replaces the rum base; '
                'the botanical complexity is reduced but the '
                'lime-ginger-almond character is present; '
                'suitable for Alcohol Removed (AR) programme '
                'contexts. USD 8–15 per 750ml.'
            ),
            'markers': (
                'Non-alcoholic syrup; no rum base; reduced complexity; '
                'lime-ginger-almond character; commercial tropical use.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic "falernum flavour" products using artificial '
                'lime flavouring, dried ginger powder, and almond '
                'extract rather than fresh botanical maceration; '
                'the synthetic aromatic compound versions lack '
                'the fresh volatile complexity of the '
                'genuine Velvet Falernum production and '
                'produce a flat, one-dimensional sweetness '
                'without the multi-register spice complexity '
                'that defines professional-grade falernum. '
                'Avoid in any PCT programme context.'
            ),
            'markers': (
                'Artificial flavouring; dried spice powder; flat '
                'one-dimensional sweetness; no botanical complexity.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Falernum is not consumed neat in programme service — '
            'it is a cocktail modifier. The Corn \'n\' Oil '
            '(the classic Bajan falernum cocktail: '
            'Foursquare dark rum, Velvet Falernum, lime, Angostura bitters) '
            'is served on crushed ice at 0–4°C — the cold temperature '
            'suppresses the sweetness and sharpens the lime-ginger '
            'spice register. In PCT programme use: a small tasting '
            'portion (15–20ml) of undiluted Velvet Falernum '
            'served at 16–18°C allows the full botanical '
            'aromatic complex to be assessed directly before '
            'presenting it in its cocktail application. '
            'Never heat falernum — the volatile lime-citral '
            'aromatics dissipate above 25°C.'
        ),
        'vessel': (
            'For direct tasting (PCT programme educational use): '
            'a small copita or Glencairn (30–50ml vessel; '
            '15–20ml pour of undiluted Velvet Falernum at 18°C) '
            'to assess the botanical aromatic complex directly. '
            'For cocktail service (Corn \'n\' Oil application): '
            'a heavy-based rocks glass over crushed ice; '
            '30ml Foursquare XO or Doorly\'s XO, 15ml Velvet Falernum, '
            '10ml lime juice, 2 dashes Angostura bitters — '
            'stir gently over the ice to chill and dilute '
            'to the correct serving concentration. '
            'Present the three PCT cocktail ingredients '
            'together: Velvet Falernum, Foursquare rum, '
            'Angostura bitters — the complete Barbados '
            'cocktail ingredient arc in a single glass.'
        ),
        'technique': (
            'Present undiluted (15ml, 18°C, small copita) before '
            'cocktail application; identify the five botanical '
            'compounds (lime-citral, ginger-gingerol, almond-benzaldehyde, '
            'clove-eugenol, cane-rum base); then demonstrate the '
            'Corn \'n\' Oil cocktail application with Foursquare rum '
            'and Angostura bitters for the complete Barbados '
            'cocktail heritage presentation.'
        ),
        'programme_position': (
            'PCT Caribbean cocktail bridge: Velvet Falernum alongside '
            'Foursquare Exceptional Cask rum and Angostura bitters '
            'for the three-ingredient Barbados-Trinidad cocktail '
            'heritage presentation; or in the global cocktail '
            'modifier comparative alongside Angostura (bitters), '
            'Orgeat (almond syrup), and Campari (bitter botanical) '
            'to demonstrate the PCT botanical modifier ingredient arc.'
        ),
        'verbal_presentation': (
            'This bottle contains five colonial trade routes. '
            'The lime came from Southeast Asia via Portugal. '
            'The ginger came from India. The almond from the Mediterranean. '
            'The clove from the Maluku Islands — the spice route '
            'that started the Portuguese colonial era. '
            'The rum is Barbadian sugarcane. This is not a cocktail ingredient. '
            'This is the entire Portuguese Colonial Trail in a bottle.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'John D. Taylor\'s Velvet Falernum produced by '
            'R.L. Seale & Co. at Foursquare Distillery, '
            'Christ Church, Barbados — the world reference '
            'expression of alcoholic falernum; available in '
            'virtually all international spirits markets '
            'through Foursquare\'s international distribution network. '
            'Secondary: Fee Brothers Falernum (non-alcoholic syrup, '
            'Rochester NY — the North American non-alcoholic '
            'market benchmark; available through cocktail '
            'supply distributors globally).'
        ),
        'producer_location': 'Christ Church, Barbados (Foursquare Distillery)',
        'key_person': 'Richard Seale — Master Distiller, Foursquare',
        'production_volume': 'Commercial production; widely distributed internationally',
        'certifications': ['Barbados rum production regulations'],
        'bc_distributor': '[PROVIDER: Foursquare products distributed in BC through Authentic Hospitality/Pacific Wine & Spirits or similar Barbados rum specialist — verify current BCLDB listing]',
        'us_distributor': '[PROVIDER: Haus Alpenz (Minneapolis) distributes Velvet Falernum in the USA — verify current availability]',
        'uk_distributor': '[PROVIDER: Velvet Falernum widely available in the UK through major spirits wholesalers (Matthew Clark, Cellar Trends) — verify current stock levels]',
        'price_tier': 'Estate',
        'availability_notes': (
            'John D. Taylor\'s Velvet Falernum is widely available '
            'internationally through spirits distributors and '
            'cocktail ingredient suppliers. The Foursquare '
            'Distillery\'s international profile (Richard Seale '
            'is one of the most respected rum producers globally) '
            'ensures consistent distribution. '
            'Programme buyers should confirm availability through '
            'their local premium spirits distributor or '
            'cocktail supply specialist.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Falernum is the PCT programme\'s most compressed geographic statement — '
        'a single product encoding the colonial trade route connections of '
        'Barbados (rum-sugarcane), Southeast Asia (lime), South Asia '
        '(ginger), Maluku Islands (clove), and the Mediterranean (almond) '
        'in a cocktail modifier that appears across the PCT cocktail '
        'programme in the Zombie (Barbados rum, Jamaican rum, Puerto Rican rum, '
        'falernum), the Corn \'n\' Oil (Bajan classic), and the '
        'ti\' punch extensions. Its inclusion in the PCT system '
        'as an independent entry recognises its function as '
        'a geographic and historical index of the colonial '
        'trade route network in a single ingredient.'
    ),
    'food_pairings': [
        {
            'technique_id': 'CAR-001',
            'dish': 'Bajan fish cakes (salt cod fritters with West Indian lime and scotch bonnet — the Barbadian street food staple)',
            'pairing_type': 'complement',
            'rationale': (
                'Falernum in the Corn \'n\' Oil cocktail alongside '
                'Bajan fish cakes completes the within-Barbados '
                'food-and-drink terroir pairing — the lime-ginger-'
                'clove spice register of the falernum resonating '
                'with the scotch bonnet heat and lime seasoning '
                'of the fish cake while the rum base of the '
                'cocktail provides a sugarcane-sweet counterpoint '
                'to the salt cod saltiness.'
            )
        },
        {
            'technique_id': 'CAR-002',
            'dish': 'Jerk chicken (Jamaican spiced grilled chicken with allspice and scotch bonnet)',
            'pairing_type': 'bridge',
            'rationale': (
                'The falernum cocktail bridges with jerk chicken '
                'through the allspice (Pimenta dioica) component — '
                'allspice is indigenous to the Caribbean and appears '
                'in both the bartender-produced falernum recipe '
                '(some house recipes add allspice to the botanical complex) '
                'and the jerk marinade; the shared allspice aromatic '
                '(the convergence of cinnamon, clove, and nutmeg '
                'phenolic compounds) creates a botanical bridge '
                'between the cocktail modifier and the spiced '
                'protein preparation.'
            )
        }
    ],
    'source': 'Davidson Alan — Oxford Companion to Food (Falernum entry); Wondrich David — Imbibe! and Punch (Caribbean cocktail history); Foursquare Distillery production documentation; Waddington Barry — Caribbean Spirits bibliography; Fee Brothers cocktail ingredient catalogue; IWSC (International Wine & Spirits Competition) Barbados rum category documentation',
    'price_trajectory': 'stable'
})

session.commit_batch()

# Entry 2: Angostura Bitters
session.switch_region(
    'spirits',
    'Caribbean — Trinidad and Tobago (Angostura Aromatic Bitters, 1824 Formula, 200-Year PCT Bridge Ingredient)'
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Angostura Limited (House of Angostura)',
    'location': 'Laventille, Port of Spain, Trinidad and Tobago',
    'country': 'Trinidad and Tobago',
    'region': 'Trinidad — Laventille Hills, Port of Spain; the bitters formula is produced exclusively in Trinidad though the original recipe was formulated in Angostura (present-day Ciudad Bolívar), Venezuela, in 1824',
    'key_person': 'Dr Johann Gottlieb Benjamin Siegert — German military surgeon in Simón Bolívar\'s Venezuelan army who formulated the original bitters recipe in 1824 in Angostura, Venezuela; the Siegert family later moved production to Trinidad in 1875; current CEO: Genevieve Jodhan',
    'founded': '1824 — Dr Siegert formulated the bitters in Angostura, Venezuela, as a medicinal digestive for Venezuelan army soldiers; 1875 — production relocated to Trinidad; 2024 — 200th anniversary of the Angostura bitters formula',
    'production_volume': 'One of the world\'s highest-volume spirit ingredient producers; Angostura bitters is distributed to 165+ countries; exact production volume proprietary but estimated tens of millions of bottles per year',
    'notable_products': [
        'Angostura Aromatic Bitters (44.7% ABV — the original formula, the world\'s most widely distributed cocktail bitters)',
        'Angostura Orange Bitters (28% ABV — citrus-based companion product)',
        'Angostura 1919 Rum (Trinidad premium rum — Coffey still production)',
        'Angostura 1824 Rum (the 12-year-aged premium expression)',
        'Angostura 7-Year Rum (the accessible premium tier)',
    ],
    'certifications': ['Trinidad and Tobago rum production regulations; the bitters formula is a Trade Secret — the full recipe is known only to five Angostura employees at any given time'],
    'website': 'www.angostura.com',
    'philosophy': (
        'Angostura Limited is the custodian of the world\'s most famous '
        'cocktail ingredient — a product whose formula has remained '
        'unchanged since Dr Siegert\'s 1824 original, whose label '
        '(infamously too large for the bottle, the result of a '
        '19th-century printing error that was retained as branding) '
        'is recognised globally, and whose presence in the cocktail '
        'repertoire spans from the Pisco Sour to the Old Fashioned '
        'to the Pink Gin to the Champagne cocktail to the Manhattan.'
    ),
    'trail_connection': 'PCT (Trinidad — the PCT\'s most widely distributed single ingredient)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Angostura Aromatic Bitters — 1824 Venezuelan Formula, Trinidad Production, '
        '44.7% ABV, 200-Year PCT Bridge Ingredient, World\'s Most Distributed '
        'Cocktail Bitters'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'bitters — aromatic botanical bitters; 44.7% ABV; gentian-root base; Venezuelan origin formula; Trinidad production; used in dashes (4ml) not pours',
    'region': 'Caribbean — Trinidad and Tobago (Angostura Aromatic Bitters, 1824 Formula, 200-Year PCT Bridge Ingredient)',
    'terroir_origin': (
        'Angostura bitters has a dual geographic identity: '
        'the formula was created in Angostura (present-day '
        'Ciudad Bolívar), Venezuela, in 1824 by Dr Johann '
        'Gottlieb Benjamin Siegert, a German military surgeon '
        'serving in Simón Bolívar\'s army during the South '
        'American independence wars. The original Angostura '
        'formula was designed as a medicinal digestive '
        'using tropical botanical ingredients available '
        'in the Orinoco River basin of Venezuela — gentian '
        '(Gentiana lutea, the primary bittering agent), '
        'galangal (Alpinia galanga, the ginger-family '
        'rhizome from Southeast Asia — present in Venezuela '
        'through the colonial spice trade), cascarilla '
        '(Croton eluteria, the Caribbean bark with cinchona-'
        'like bittering properties), and other botanicals '
        'whose full composition remains a Trade Secret. '
        'The production moved to Trinidad in 1875 when '
        'the Siegert family relocated from Venezuela after '
        'political instability; the Trinidad production has '
        'continued without interruption since 1875. '
        'The current Laventille, Port of Spain production '
        'facility uses the identical formula from 1824 — '
        'the terroir of Angostura bitters is thus a '
        'historical compound: Venezuelan forest botanicals '
        '(gentian, galangal, cascarilla) combined with '
        'Trinidad-produced spirit base and bottled '
        'in a 200-year-old formula that has outlasted '
        'the country of its origin (Venezuela), '
        'the army it was designed for (Bolívar\'s Venezuelan '
        'forces), and most of the cocktails it was '
        'first used in. The PCT places Angostura '
        'as the connecting ingredient between '
        'the British colonial Pink Gin tradition '
        '(the Royal Navy\'s adoption of the bitters '
        'in the 1830s–1840s), the Manhattan (1870s New York), '
        'the Champagne cocktail (Victorian British), '
        'the Old Fashioned (Kentucky bourbon), '
        'and the Pisco Sour (Peru) — the most geographically '
        'distributed single cocktail ingredient in the PCT system.'
    ),
    'production_technique': (
        'Angostura bitters production is the most tightly '
        'guarded formula in the spirits industry — '
        'the full ingredient list is classified as a '
        'Trade Secret with only five Angostura employees '
        'knowing the complete formulation at any given time. '
        'The documented production architecture is: '
        'a grain spirit base (produced at the Angostura '
        'Limited rum facility in Trinidad from '
        'column-still distillation of molasses, '
        'the same raw material as the Angostura rums) '
        'is used as the extraction medium for the '
        'botanical maceration; the gentian root '
        '(Gentiana lutea — sourced from continental '
        'Europe, the primary bittering compound) '
        'and the other botanicals are macerated '
        'in the grain spirit at high ABV (50%+ '
        'to maximise extraction of the bitter '
        'amarogentin compound from the gentian) '
        'for a proprietary period before blending, '
        'dilution to the final 44.7% ABV, and '
        'bottling with the characteristic '
        'oversized label (a 19th-century printing '
        'error retained as brand identity '
        'for 150+ years). The final product '
        'is 44.7% ABV — high enough to be '
        'shelf-stable indefinitely without '
        'refrigeration, which was critical '
        'for the Naval rum ration and colonial '
        'distribution use cases of the original '
        'production. The characteristic dose '
        'in cocktail use is 2–4 dashes '
        '(approximately 2–4ml) — a usage rate '
        'that means a single 100ml bottle '
        'of Angostura contains 25–50 cocktail '
        'servings, the most economical cocktail '
        'ingredient on the PCT programme bar per '
        'serving. The galangal (Alpinia galanga) '
        'in the formula — the Southeast Asian '
        'ginger-family rhizome — is the direct '
        'botanical link from Venezuela through '
        'the Portuguese Indian Ocean spice trade '
        'network that brought the galangal plant '
        'from its Malay Archipelago origin '
        'to the colonial Caribbean through '
        'the same trade routes that built '
        'the Portuguese Colonial Trail.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Peychaud\'s Bitters (New Orleans, 1830s — Creole aromatic bitters)',
            'beverage': 'Peychaud\'s Aromatic Cocktail Bitters — New Orleans Creole Pharmacy Origin, Sazerac Tradition',
            'connection': (
                'Angostura and Peychaud\'s are the two founding '
                'pillars of the aromatic cocktail bitters tradition — '
                'both formulated in the 1820s–1830s as medicinal '
                'digestives by trained pharmacists or physicians '
                '(Dr Siegert: German military surgeon, Venezuela, 1824; '
                'Antoine Amédée Peychaud: Creole Haitian-born pharmacist, '
                'New Orleans, 1830s), both using a grain spirit base '
                'with botanical maceration, and both transitioning '
                'from medicinal to cocktail use through the '
                '19th-century American bar culture. The PCT '
                'connection: Peychaud\'s is the New Orleans '
                'Creole tradition (itself part of the French '
                'and Haitian colonial heritage arc); Angostura '
                'is the South American-Caribbean colonial arc. '
                'Together they define the two poles of the '
                'aromatic bitters tradition that underpins '
                'the entire classic cocktail canon — the '
                'Sazerac (Peychaud\'s) and the Old Fashioned '
                '(Angostura) representing the French-Creole '
                'and British-Caribbean colonial cocktail heritage.'
            )
        },
        {
            'tradition': 'spirits — Campari (Milan, 1860 — Italian bitter liqueur, aperitivo tradition)',
            'beverage': 'Campari — Gaspare Campari 1860 Formula, Italian Bitter Botanical, Aperitivo Tradition',
            'connection': (
                'Angostura aromatic bitters and Campari represent '
                'the same 19th-century botanical bitterness tradition '
                'in its colonial-Caribbean and European expressions: '
                'both are gentian-root-based bitter botanical '
                'macerations (Angostura uses Gentiana lutea '
                'as its primary bittering compound; Campari '
                'uses a similar bitter root botanical complex '
                'whose full formula is also a Trade Secret); '
                'both were originally formulated as medicinal '
                'digestives (Angostura for Venezuelan army dysentery; '
                'Campari for the Milanese digestivo tradition); '
                'both transitioned to cocktail use in the '
                'late 19th–early 20th century; and both are '
                'used across the PCT cocktail programme — '
                'Angostura as a dash modifier in the Old '
                'Fashioned, Champagne cocktail, and Pisco Sour; '
                'Campari as a primary ingredient in the Negroni. '
                'The fundamental distinction is concentration: '
                'Angostura is used in 2–4ml dashes as a '
                'modifier; Campari is used in 25–30ml pours '
                'as a principal ingredient. Both are part '
                'of the same 19th-century bitterness-in-cocktail '
                'tradition that the PCT programme documents '
                'across its colonial-geographic arc.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep red-brown, nearly opaque — the colour of '
            'the gentian root and cascarilla bark tannin '
            'extraction in the high-ABV spirit base; '
            'the characteristic Angostura colour is the '
            'result of the tannin pigments of the botanical '
            'maceration rather than added caramel colour '
            '(the formula includes no artificial colouring); '
            'at 44.7% ABV the legs are thin and fast '
            'on the glass wall, reflecting the spirit '
            'base rather than a liqueur sugar concentration; '
            'diluted in a cocktail at 2–4 dashes per serving '
            'the colour contribution is a slight amber tinge '
            'in the drink.'
        ),
        'nose': (
            'The aromatic profile of Angostura undiluted (neat, '
            '44.7% ABV) is dominated by the gentian bittering '
            'compounds (amarogentin and gentiopicroside — '
            'the most bitter naturally occurring compounds '
            'known to food science, detectable at 50 parts per million) '
            'as a bitter-medicinal background; the foreground '
            'is the warm-spice complex of the galangal '
            '(Alpinia galanga — the Southeast Asian spice '
            'rhizome producing a peppery-camphor aromatic '
            'distinct from ordinary ginger), cascarilla bark '
            '(Croton eluteria — a Caribbean spice bark with '
            'a characteristic warm-nutmeg-cinnamon-vanilla '
            'aromatic), cinnamon (Cinnamomum verum — '
            'the high-volatile cinnamaldehyde top note), '
            'and the grain spirit base (the characteristic '
            'clean ethanol of the column-still Trinidad spirit). '
            'In cocktail dilution (2 dashes in 60ml of spirit): '
            'the bitterness becomes a supportive base note '
            'and the warm-spice aromatic complex integrates '
            'into the principal spirit\'s aromatic profile.'
        ),
        'palate': (
            'Neat (as presented in PCT programme tasting): '
            'the initial impression is the warm alcohol '
            '(44.7% ABV) carrying the complex botanical '
            'spice onto the palate; the gentian bitterness '
            'arrives mid-palate as a persistent, '
            'long-duration bitter note (the amarogentin '
            'compound binds to the same TAS2R bitter '
            'taste receptors as quinine, producing a '
            'characteristic cinchona-adjacent bitterness '
            'that the Victorian era associated with '
            'medicinal digestives and anti-malarial use); '
            'the finish is extraordinarily long (60+ seconds '
            'neat) with the gentian bitterness fading '
            'through the warm-spice cascarilla-galangal '
            'complex; the spirit base is clean and neutral '
            'beneath the botanical domination. '
            'In cocktail application: the 2–4 dash dose '
            'transforms the perception — the bitterness '
            'becomes a structural note that adds depth '
            'to the primary spirit without dominating; '
            'the warm-spice complex integrates as a '
            'background complexity that distinguishes '
            'the finished cocktail from the un-bittered version.'
        ),
        'conclusion': (
            'The most widely distributed cocktail ingredient in the PCT system '
            'and possibly the world — a 200-year-old formula encoding '
            'Venezuelan forest botanicals, Southeast Asian spice trade '
            'connections, and Caribbean colonial production in 44.7% ABV. '
            'The Angostura Aromatic Bitters is the closing PCT entry '
            'that connects every geographic node of the trail '
            'through a single 100ml bottle.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Angostura 200th Anniversary expressions (2024) or '
                'vintage-dated Angostura bitters from the pre-1960s '
                'production era (available through cocktail history '
                'specialist auctions) that demonstrate the formula '
                'consistency and the aromatic evolution of long-stored '
                'bitters; or craft artisanal bitters from specialist '
                'producers (The Bitter Truth, Germany; Dr Adam '
                'Elmegirab\'s Dandelion & Burdock Bitters, Scotland) '
                'using comparable botanical complexity to the '
                'Angostura formula but with transparency of ingredient '
                'declaration. The reserve tier for the PCT programme '
                'is the original Angostura formula at the 200th '
                'anniversary — 2024 production.'
            ),
            'markers': (
                'Anniversary expression; consistent formula; '
                'complete botanical complexity; 44.7% ABV; '
                'gentian-galangal-cascarilla register.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Standard Angostura Aromatic Bitters (100ml, 44.7% ABV) '
                '— the international commercial benchmark; the formula '
                'unchanged since 1824; the correct and essential '
                'programme expression. Available in every international '
                'spirits market. EUR/USD 8–12 per 100ml bottle; '
                '25–50 cocktail servings per bottle at 2–4 dash dose.'
            ),
            'markers': (
                'Standard 100ml; 44.7% ABV; 1824 formula; '
                'oversized label; gentian-bitter; international availability.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Angostura Orange Bitters (28% ABV) or '
                'Fee Brothers aromatic bitters (the North American '
                'bar-supply equivalent with similar gentian-spice '
                'character but a different proprietary formula '
                'and less aromatic complexity than the Angostura '
                'original). Market tier for programme buyers who '
                'cannot source the original Angostura at their '
                'venue — the Fee Brothers is a competent substitute '
                'for cocktail production but does not represent '
                'the PCT historical narrative of the 1824 original.'
            ),
            'markers': (
                'Fee Brothers or Angostura Orange; gentian base; '
                'different formula; less historical significance.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic "cocktail bitters" without gentian root '
                'as the primary bittering compound — products using '
                'artificial bitter flavouring or low-quality '
                'dried herb blends that mimic the Angostura '
                'colour profile without the botanical depth; '
                'identifiable by the absence of the characteristic '
                'gentian-galangal-cascarilla aromatic register '
                'and the flat, one-dimensional bitterness '
                'of artificial bittering agents. Not appropriate '
                'for any PCT programme context.'
            ),
            'markers': (
                'No gentian; artificial bitters; flat one-dimensional; '
                'no botanical depth; avoid in PCT programme.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Angostura bitters is a cocktail modifier — it is never '
            'served solo in standard programme service. '
            'For PCT educational tasting (direct botanical assessment): '
            'present 5ml (approximately one cocktail serving) '
            'undiluted in a small snifter or aroma glass at '
            '18–20°C to assess the botanical aromatic complex '
            'directly before cocktail application. The high '
            'ABV (44.7%) makes the direct tasting challenging '
            'for non-spirit-trained palates — a 1ml drop on '
            'a demitasse spoon for direct palate assessment '
            'is the most educational approach. In cocktail '
            'application: always used chilled in the finished '
            'drink (0–5°C for rocks-based cocktails; 0–2°C '
            'for stirred cocktails).'
        ),
        'vessel': (
            'For direct tasting: a small aroma glass (50ml) '
            'or demitasse spoon with 1–2ml. In cocktail '
            'application: 2 dashes from the proprietary '
            'Angostura bottle dropper into the cocktail '
            'vessel — the bottle\'s built-in dropper '
            'delivers approximately 2ml per shake of '
            'the inverted bottle; the iconic Angostura '
            'label and bottle shape is itself a '
            'programme presentation element. '
            'For the PCT three-ingredient Barbados-Trinidad '
            'programme: present the Angostura bottle '
            'alongside the Velvet Falernum and Foursquare '
            'rum — the three bottles together constitute '
            'a visual summary of the Caribbean colonial '
            'beverage heritage of Barbados and Trinidad.'
        ),
        'technique': (
            'Direct tasting (1ml on spoon); cocktail application '
            '(2–4 dash dose in stirred or shaken cocktail); '
            'present the 200-year production continuity narrative — '
            'the 1824 formula, the Venezuela-Trinidad transfer, '
            'the Royal Navy adoption, and the five-cocktail '
            'PCT arc from Pisco Sour to Old Fashioned.'
        ),
        'programme_position': (
            'PCT bridge ingredient: Angostura alongside Velvet Falernum '
            '(Barbados) and Foursquare rum (Barbados) for the '
            'Trinidad-Barbados ingredient heritage comparison; '
            'or as the closing ingredient in the PCT cocktail '
            'programme — the ingredient that appears in the '
            'Pisco Sour (Peru), the Champagne cocktail (France), '
            'the Old Fashioned (USA-Kentucky), the Pink Gin '
            '(British Royal Navy), and the Manhattan (New York) — '
            'demonstrating the single ingredient that connects '
            'every node of the PCT cocktail geography.'
        ),
        'verbal_presentation': (
            'This bottle was first made in Venezuela in 1824. '
            'Dr Siegert was a German surgeon in Bolívar\'s army. '
            'The British Royal Navy adopted it as a remedy for seasickness. '
            'It became the Pink Gin. Then the Manhattan. '
            'Then the Old Fashioned. Then it appeared in the Pisco Sour. '
            'This 100ml bottle connects Peru, Venezuela, Trinidad, '
            'Kentucky, and the British Navy through a single formula '
            'unchanged for 200 years. That is the PCT in 44.7% ABV.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Angostura Limited (House of Angostura), Laventille, '
            'Port of Spain, Trinidad and Tobago — the sole producer '
            'of the original Angostura Aromatic Bitters; '
            'no other producer has access to the 1824 formula. '
            'For comparable aromatic bitters: The Bitter Truth '
            'Aromatic Bitters (Germany) and Dr Adam Elmegirab\'s '
            'Dandelion Bitters (Scotland) are the closest '
            'artisanal alternatives in the European market.'
        ),
        'producer_location': 'Laventille, Port of Spain, Trinidad and Tobago',
        'key_person': 'Dr Johann Gottlieb Benjamin Siegert (1824 formulator, deceased); current CEO Genevieve Jodhan; five unnamed formula custodians',
        'production_volume': 'Tens of millions of 100ml bottles per year; distributed to 165+ countries; the world\'s most distributed cocktail bitters',
        'certifications': ['Trinidad and Tobago spirits production regulations; Trade Secret formula registration'],
        'bc_distributor': '[PROVIDER: Angostura bitters available at BCLDB (BC Liquor Stores) — standard on-shelf availability; verify current stock through BCLDB website]',
        'us_distributor': '[PROVIDER: Angostura USA through Diageo or direct Angostura Limited import; available in virtually all US spirits retailers and bar supply chains]',
        'uk_distributor': '[PROVIDER: Angostura UK through Matthew Clark or Cellar Trends — standard UK on-trade and off-trade distribution; widely available]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Angostura Aromatic Bitters is the single most available '
            'ingredient in this entire PCT programme — it is stocked '
            'by virtually every bar, liquor store, and grocery in '
            'any country where alcohol is sold. Programme buyers '
            'need only confirm their local BCLDB, state liquor '
            'board, or spirits retailer carries the standard '
            '100ml bottle. The 200th anniversary (2024) expressions '
            'may require pre-ordering through specialty spirits merchants.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Angostura Aromatic Bitters closes the PCT Caribbean cocktail arc '
        'as the most widely distributed single ingredient of the entire '
        'PCT beverage programme — a 200-year-old formula connecting '
        'Venezuela (origin), Trinidad (production), the British Royal Navy '
        '(first international distribution), and the five continents '
        'of the global cocktail repertoire (Pisco Sour: South America; '
        'Old Fashioned: North America; Champagne cocktail: Europe; '
        'Singapore Sling: Southeast Asia; Trinidad Sour: Caribbean) '
        'through a single botanical bitters formula unchanged since 1824. '
        'No single product in the PCT system demonstrates the geographic '
        'reach of the Portuguese Colonial Trail\'s colonial trade routes '
        'more concisely than the galangal-gentian-cascarilla formula '
        'of Angostura — the Maluku Islands spice trade convergent '
        'with the Caribbean colonial infrastructure in a 100ml bottle.'
    ),
    'food_pairings': [
        {
            'technique_id': 'TRT-001',
            'dish': 'Trinidad bake and shark (fried bread with shark fillet, tamarind sauce, and pepper sauce)',
            'pairing_type': 'bridge',
            'rationale': (
                'A Trinidad Rum Sour (Angostura 1919 rum, lime, sugar, '
                '2 dashes Angostura bitters) alongside Trinidad bake '
                'and shark bridges through the tamarind-pepper sauce '
                'acidity resonating with the lime and bitters in the '
                'cocktail while the rum\'s sugarcane sweetness '
                'complements the fried bread starchiness — '
                'a within-Trinidad terroir pairing connecting '
                'the island\'s food street tradition '
                'with its most famous export ingredient.'
            )
        },
        {
            'technique_id': 'TRT-002',
            'dish': 'Pelau (Trinidad one-pot rice with pigeon peas, Gallus gallus domesticus pieces, coconut milk, and browning)',
            'pairing_type': 'complement',
            'rationale': (
                'The Angostura Old Fashioned (bourbon, Angostura bitters, '
                'sugar cube — or with rum, the Trinidad variation) '
                'alongside pelau complements through the caramel-browning '
                'aromatic of the browned sugar in both the cocktail '
                '(the sugar cube caramelisation in the bitters) '
                'and the pelau (the browning — caramelised sugar '
                'used to colour the rice-peas mixture), '
                'while the spirit alcohol cuts the coconut-milk '
                'richness of the one-pot.'
            )
        }
    ],
    'source': 'Siegert family historical records; Wondrich David — Imbibe! (Angostura bitters history); Zandvliet Kees — Mapping for Money (Caribbean colonial trade documentation); Angostura Limited 200th anniversary documentation (2024); Davidson Alan — Oxford Companion to Food; IWSC Caribbean spirits category documentation; Robinson Jancis Oxford Companion to Wine (bitters entry)',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
