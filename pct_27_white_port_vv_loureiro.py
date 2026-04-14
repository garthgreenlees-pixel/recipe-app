import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='wine',
    region='Portugal — Douro Valley (White Port, Dry to Off-Dry, Cocktail Culture, Rabigato, Gouveio)',
    output_dir='.',
    starting_entry=1,
    session_number=28,
    running_total=88
)

session.add_producer({
    'tradition': 'wine',
    'name': 'Ramos Pinto — White Port Division',
    'location': 'Gaia (Vila Nova de Gaia), Porto, Portugal',
    'description': 'Established 1880 by Adriano Ramos Pinto, whose turn-of-the-century art nouveau advertising posters remain some of the most iconic images in Portuguese wine history. Ramos Pinto is owned by Champagne Louis Roederer since 1990 and maintains estates in both the Cima Corgo (Quinta da Ervamoira) and Douro Superior (Quinta dos Bons Ares). Their White Port program is among the most distinctive in the Douro: the Ervamoira White Port is produced from estate Rabigato, Gouveio, Viosinho, and Códega do Larinho varieties grown in the schist terroir of the Cima Corgo, fermented and fortified to produce both dry and off-dry expressions that have become the reference for the modern White Port cocktail movement.',
    'founded': '1880',
    'region': 'Vila Nova de Gaia and Douro Valley estates, Portugal',
    'website': 'ramospinto.pt',
    'verified': True
})

session.add_producer({
    'tradition': 'wine',
    'name': 'Niepoort Vinhos — White Port',
    'location': 'Porto and Douro Valley estates, Portugal',
    'description': 'Niepoort\'s White Port program extends the estate\'s philosophy of minimal intervention and terroir transparency to the fortified white category. Niepoort produces both a Dry White Port (fermented to near-dryness before fortification, 0–30 g/L residual sugar) and the NV Tawny blanc, exploring the oxidative aging potential of white Port varieties in small used oak. Dirk Niepoort championed the cocktail use of dry White Port — particularly the Port & Tonic ("P&T") which became the defining Portuguese summer aperitif of the 2010s decade — through advocacy with bartenders in Porto\'s Rua das Flores cocktail scene.',
    'founded': '1842',
    'region': 'Porto and Douro Valley, Portugal',
    'website': 'niepoort-vinhos.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Quintessential Wines / Broadbent Selections — White Port Specialists',
    'type': 'importer',
    'description': 'Same importers as Niepoort and Ramos Pinto table wines also carry White Port in markets where fortified wine regulations allow. The "P&T" (Port and Tonic) has driven significant White Port category growth in UK and EU; North American adoption is growing driven by bartender discovery of the category as an alternative to Lillet Blanc, Noilly Prat, and other aperitif fortified wines.',
    'markets_served': ['UK', 'EU', 'US', 'Canada'],
    'traditions_carried': ['wine'],
    'website': 'ramospinto.pt',
    'verified': False
})

session.add_beverage({
    'name': 'Ramos Pinto Ervamoira Dry White Port — Schist Rabigato Gouveio, P&T Aperitif Cocktail Heritage',
    'category': 'wine',
    'subcategory': 'fortified_white',
    'origin': 'Portugal',
    'region': 'Cima Corgo, Douro Valley, Portugal',
    'producer': 'Ramos Pinto — White Port Division',
    'alcohol_content': 19.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'White Port is produced from the Douro Valley\'s white grape varieties — Rabigato, Gouveio (Verdelho de Douro), Viosinho, Códega do Larinho, Malvasia Fina — grown on the same steep schist slopes that produce the red varieties destined for vintage Port. The white varieties, historically planted on north-facing slopes and higher-elevation plots within the Douro demarcated region to benefit from slightly cooler ripening, were traditionally viewed as secondary to the red-wine-destined varieties. The creation of a sophisticated Dry White Port expression by producers like Ramos Pinto and Niepoort from the 2000s onward rehabilitated the white Douro varieties as capable of producing wines of complexity and character in their own right. Quinta da Ervamoira — Ramos Pinto\'s principal estate in the Cima Corgo above Peso da Régua — grows Rabigato and Gouveio at 300–500m elevation on thin schist soils with the same ancient vine populations and schist mineral substrate that defines the red variety production. The white varieties in this schist environment develop a distinctive saline-mineral-citrus character: the schist\'s iron-rich composition transfers through root uptake into the fermentable juice, creating the mineral complexity that makes Douro Dry White Port fundamentally different from the blanker, less mineral white Port expressions from less distinguished vineyard sources.'
    ),
    'production_technique': (
        'Ervamoira white grapes are harvested in mid-September — earlier than red varieties to preserve acidity — and immediately pressed in pneumatic presses without skin contact. The free-run and first-press juice is fermented in stainless steel tanks at 16–18°C with selected Portuguese white wine yeast cultures until the target residual sugar level is reached (0–30 g/L for dry expressions; 30–65 g/L for off-dry). The critical fortification decision in White Port production: neutral grape spirit (77–78% ABV, produced from Portuguese grapes) is added to stop fermentation at the moment the winemaker judges the sugar-alcohol-acid balance to be optimal for the desired style. For Dry White Port, this occurs when fermentation has converted nearly all sugar; for traditional sweet White Port, fortification arrests fermentation at 100–150 g/L. After fortification, the wine stabilizes at 19–20% ABV. Aging occurs in used oak tonéis (large casks) for 3–6 months minimum — longer aging develops the oxidative complexity that defines the finest White Ports. The Ervamoira expression is bottled with 30–50 g/L residual sugar ("dry" by Port standards, though technically off-dry by table wine standards), producing the balance between mineral freshness and port sweetness that makes it work in the "P&T" cocktail. The P&T (Port and Tonic) uses Dry White Port as the base spirit poured over ice in a Copa glass with Mediterranean tonic water, a slice of lemon, and fresh mint — the low alcohol (19.5% vs 40% for gin) and citrus mineral character of the dry white port producing a lower-alcohol, more mineral aperitif than a gin-tonic.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Fino Sherry (Palomino-based dry fortified, oxidative aging, aperitif role)',
            'connection': 'Dry White Port and Fino Sherry occupy the same aperitif-fortified-wine register: both are produced from white grapes in schist or chalk soils, fortified to 15–20% ABV, intended for chilled aperitif service, and dramatically improved in quality over the past 20 years as bartenders and sommeliers discovered their cocktail potential beyond traditional sweet service'
        },
        {
            'tradition': 'Sercial Madeira (bone dry fortified from volcanic island)',
            'connection': 'Dry White Port and Sercial Madeira represent the two great dry expressions of Portuguese fortified wine tradition — both fortified with grape spirit to stop fermentation, both developing mineral and oxidative complexity with age, both long overlooked in favor of sweeter styles and now experiencing critical reassessment as the finest dry aperitif wines Portugal produces'
        },
        {
            'tradition': 'Vermouth Bianco (Italian fortified wine cocktail base)',
            'connection': 'Dry White Port functions identically to white vermouth in cocktail applications — as a lower-ABV fortified wine base for long cocktails and as a modifier in short cocktails — but with the Douro schist mineral character and Portuguese grape variety complexity rather than wormwood and botanical infusion, creating a natural and wine-forward alternative'
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale gold with slight amber tint from oak aging; clear and brilliant; slightly viscous at 19.5% ABV; no cloudiness in well-stored expressions',
        'nose': 'Fresh citrus (lemon, blood orange), almond blossom, white peach, subtle schist mineral (chalk, wet stone), light vanilla from oak, honey and dried apricot in off-dry expressions — the nose is more wine-like than spirit-like, closer to a rich white Burgundy than to any other fortified category',
        'palate': 'Off-dry to medium-sweet balance depending on style, schist mineral mid-palate, citrus acidity balancing residual sugar, warm fortification (evident but not harsh), long mineral-citrus finish — in the P&T cocktail preparation, the tonic water amplifies the citrus while diluting the sweetness and alcohol, producing a perfectly balanced 9–10% ABV aperitif drink'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard White Port (cooperative, off-dry)',
            'criteria': 'Non-estate fruit, commercial yeast, minimal oak aging, 80–100 g/L residual sugar — the traditional British market sweet White Port style used as dessert wine or sweet cocktail modifier; widely available but lacks mineral complexity'
        },
        {
            'tier': 2,
            'tier_name': 'Ervamoira Dry White Port (Ramos Pinto)',
            'criteria': 'Estate Cima Corgo white varieties, minimal oak, 30–50 g/L residual sugar — the reference expression for the modern Dry White Port category and the P&T cocktail movement'
        },
        {
            'tier': 3,
            'tier_name': 'Niepoort Dry White / Malvasia',
            'criteria': 'Niepoort\'s single-variety expressions of Malvasia Fina and Gouveio in fortified form — more mineral and precise than the Ramos Pinto house style; produced in small quantities for sommelier allocation'
        },
        {
            'tier': 4,
            'tier_name': 'Colheita White (Single Vintage Aged)',
            'criteria': 'Single-vintage White Port aged for 10+ years in used oak, developing oxidative complexity that rivals mature dry Sherry — extremely rare category; Ramos Pinto and Niepoort both produce limited colheita White Port from exceptional vintages'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 8–10°C for straight aperitif service; in P&T preparation, 4–6°C over ice in Copa glass with Mediterranean tonic; the low alcohol and mineral character of Dry White Port is best expressed chilled, unlike most fortified wines',
        'vessel': 'P&T: Copa de Balon (large balloon glass) over ice, 60ml White Port + 120ml Mediterranean tonic + lemon slice + fresh mint; Straight: white wine tulip at 8°C; as a substitute for Lillet in a Vesper martini, serve in chilled martini glass',
        'p_and_t_protocol': 'The Porto & Tónico (P&T) has been the defining Portuguese aperitif cocktail since approximately 2012 when Porto\'s bartender community adopted it: 2 parts Dry White Port over ice in Copa, 3 parts Mediterranean tonic (Fever-Tree or 1724 preferred), lemon wheel, fresh mint sprig, optional twist of lemon peel — the resulting 8% ABV drink is crushable as a session aperitif in a way that gin-tonic at 16%+ is not'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Ramos Pinto Ervamoira Dry White Port — the definitive P&T cocktail base and the international benchmark for the Dry White Port category',
        'north_america_access': 'Ramos Pinto White Port through Quintessential Wines (US) and select Canadian provincial boards; growing availability as the P&T trend crosses the Atlantic; in Vancouver, available at Liberty Wine Merchants and Marquis Wine Cellars by special order',
        'culinary_application': 'Dry White Port as a cooking wine is extraordinary: deglazes seafood pans with mineral-citrus depth; reduces into a Portuguese-style escabeche acid with Atlantic mineral character; the P&T cocktail works as a welcome drink at multicourse dinners where the low alcohol signals a marathon rather than a sprint — culturally significant as the modern expression of Portuguese aperitif culture before the meal'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Portugal — Vinho Verde (Lima Sub-Region, Loureiro Variety, Aromatic Florality)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Quinta de Ameal — Lima Sub-Region, Vinho Verde',
    'location': 'Ponte de Lima, Lima Sub-Region, Vinho Verde, Portugal',
    'description': 'Quinta de Ameal is the benchmark producer of single-variety Loureiro in the Lima sub-region of Vinho Verde — the most aromatically distinctive of the Vinho Verde subzones, where the Loureiro grape variety expresses its maximum florality in the granite-and-clay soils of the Lima River valley. The estate was founded in the 18th century and reconstructed as a quality wine producer by Pedro Araujo in the 1990s, who introduced temperature-controlled fermentation and reduced yields to produce Loureiro of depth and complexity rather than the thin, neutral Vinho Verde of industrial production. Quinta de Ameal\'s Loureiro is the wine that established Loureiro as one of Portugal\'s most distinctive aromatic white varieties internationally, and is the benchmark reference for the Lima sub-region within the broader Vinho Verde DOC.',
    'founded': '18th century estate; modern production from 1990s',
    'region': 'Ponte de Lima, Lima Sub-Region, Vinho Verde DOC, Portugal',
    'website': 'quintadeameal.com',
    'verified': True
})

session.add_beverage({
    'name': 'Quinta de Ameal Loureiro — Lima Sub-Region Vinho Verde, Single Variety Aromatic Floral White',
    'category': 'wine',
    'subcategory': 'white_wine',
    'origin': 'Portugal',
    'region': 'Lima Sub-Region, Vinho Verde DOC, Portugal',
    'producer': 'Quinta de Ameal — Lima Sub-Region, Vinho Verde',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Lima sub-region occupies the Lima River valley in the northwestern corner of Portugal, where the river flows south from the Spanish Galician border through a deeply incised granite valley before reaching Ponte de Lima — one of the oldest continuously inhabited towns in Portugal, famous for its Roman bridge. The Lima valley\'s climate is the wettest and most Atlantic-influenced within Vinho Verde: annual rainfall of 1,600–1,900mm (compared to 1,200–1,400mm for the southern Braga sub-region and 1,000–1,200mm for the Monção e Melgaço sub-region in the northwest). The granite soils of the Lima valley have a specific mineralogy: coarse-grained granite with high quartz and feldspar content, naturally acidic (pH 5.0–5.8), with excellent drainage that prevents waterlogging despite the high rainfall. The Loureiro grape variety — genetically distinct from Laurel (Laurus nobilis) but sharing a common aromatic compound profile dominated by linalool and geraniol terpenoids — produces dramatically different wine depending on where it is grown within the Vinho Verde DOC. In the Lima sub-region, the combination of cooler temperatures, higher humidity, and weathered granite soils produces Loureiro of exceptional floral intensity: rose petal, jasmine, lime blossom, and white peach aromatics at concentrations that make it one of the most recognizable aromatic varieties in Portugal. The Lima granite contributes a saline mineral structure that prevents the high aromatic intensity from becoming heavy or cloying — the same granite mineral freshness that makes Albariño from neighboring Galicia (across the border) so vivid.'
    ),
    'production_technique': (
        'Quinta de Ameal harvests Loureiro manually in early-to-mid September — early for Vinho Verde — to capture the aromatic compounds at peak expression before they degrade with advancing sugar accumulation. Pedro Araujo\'s harvest timing targets 12–12.5% potential alcohol with 7–8 g/L natural acidity — unusually high for a southern European white wine but necessary for the varietal\'s characteristic aromatic-mineral balance. After destemming and gentle pressing (whole cluster pressed without crushing to minimize phenolic extraction from the thick Loureiro skins), the juice is cold-settled at 6–8°C for 12–16 hours to remove gross lees. Fermentation in stainless steel at 14–16°C with selected Portuguese aromatic yeast strains (chosen to preserve linalool and geraniol rather than modify them) for 15–20 days. No malolactic fermentation — the natural malic acid of the Lima granite Loureiro is a structural element rather than a fault to be converted. Sur lies aging for 3–4 months with bi-weekly bâtonnage to build textural weight that balances the aromatic intensity. Minimal SO2 addition (25 mg/L free SO2 at bottling) preserves the floral profile without antioxidant addition that could muffle the aromatic delicacy. Bottled without filtration in Portuguese tradition, requiring slight chilling to settle any light turbidity before service. Annual production of the standard Loureiro is approximately 50,000 bottles; the single-vineyard "Loureiro Escolha" from the oldest estate vines (40–60 years) is approximately 5,000 bottles.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Galician Albariño DO Rías Baixas (same granite terroir, across the border)',
            'connection': 'Quinta de Ameal Loureiro and Rías Baixas Albariño are the closest terroir siblings in the wine world: both grow in granite soils of the same geological formation (the Galician-Minho granite massif), both use related Atlantic-influenced grape varieties, both produce wines of saline mineral freshness with floral aromatic intensity — the Spanish-Portuguese border creates regulatory separation between two expressions of the same geological identity'
        },
        {
            'tradition': 'Alsace Riesling Grand Cru (aromatic white with granite mineral structure)',
            'connection': 'The combination of intense aromatics and firm acidic-mineral structure in Quinta de Ameal Loureiro parallels Alsace Riesling from granite Grand Cru sites like Brand or Sommerberg — both show how granite soils produce aromatic white wines of precision and longevity rather than the fat, generous style associated with clay-limestone white wines'
        },
        {
            'tradition': 'Condrieu Viognier (aromatic white, floral intensity)',
            'connection': 'Loureiro and Condrieu Viognier share a similar aromatic register (rose, jasmine, white peach, lime) but Loureiro maintains the granite mineral structure and higher acidity that Viognier often lacks in warm southern Rhône conditions — making Loureiro a more food-versatile expression of the same aromatic white wine aesthetic'
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale lemon-gold with faint green tint; brilliantly clear; very light viscosity at 12% ABV; the color signals freshness rather than concentration — appropriate to the variety\'s aromatic-rather-than-extract character',
        'nose': 'Intense and immediately identifiable: rose petal, jasmine, lime blossom, white peach, grapefruit zest, granite mineral freshness underneath — the Loureiro aromatic signature is distinct enough to be recognized in blind tasting by experienced Portugal specialists; 30 minutes in glass reveals secondary flavors of wet stone and crushed limestone under the floral intensity',
        'palate': 'Light-medium body, vibrant malic acidity (the malolactic fermentation-free character is evident), floral mid-palate that mirrors the nose, saline granite mineral finish, clean and direct — the wine\'s transparency of expression is its defining quality; no new oak, no malolactic, no filtration masking the Lima River valley granite character'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Vinho Verde Loureiro Commercial',
            'criteria': 'Co-operative or industrial production Loureiro at high yields (10,000+ kg/ha), minimal floral character, residual CO2 added artificially — the thin, neutral baseline that Quinta de Ameal was established to transcend'
        },
        {
            'tier': 2,
            'tier_name': 'Quinta de Ameal Loureiro Standard',
            'criteria': 'Estate fruit, 50,000 bottles annual, 4 months sur lies, no malolactic — the reference expression of Lima sub-region Loureiro character at the premium price point'
        },
        {
            'tier': 3,
            'tier_name': 'Quinta de Ameal Loureiro Escolha',
            'criteria': 'Single-vineyard selection from the oldest estate Loureiro vines (40–60 years), 6 months extended sur lies, no fining or filtration, 5,000 bottles — the deepest expression of the Lima granite terroir available commercially'
        },
        {
            'tier': 4,
            'tier_name': 'Quinta de Ameal Loureiro Reserva Especial',
            'criteria': 'Micro-selections from centenary parcels (80+ year vines), vinified in used acacia or chestnut wood for a further aromatic dimension, under 1,000 bottles when produced — the frontier of Loureiro\'s aging and complexity potential in the Lima sub-region'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 10–12°C — slightly warmer than most Vinho Verde to allow the complex Loureiro aromatics to express fully; the light body makes it vulnerable to over-chilling which flattens the floral profile; pour only small measures initially and allow to warm in glass',
        'vessel': 'White wine tulip or white Burgundy glass to concentrate the floral aromatics; do not use a narrow champagne flute which disperses the aromatic intensity upward without allowing olfactory concentration; the Loureiro character rewards generous nosing before tasting',
        'aging_potential': 'Quinta de Ameal Loureiro rewards 2–3 years of bottle age for the Escolha tier: the primary floral aromatics integrate with developing honey and waxy secondary notes, and the granite mineral becomes more prominent as the aromatic intensity softens — an underappreciated aging candidate in a region known for young consumption'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Quinta de Ameal — the international benchmark for Lima sub-region single-variety Loureiro and the wine that established Loureiro\'s international reputation',
        'north_america_access': 'Quinta de Ameal imported by Skurnik Wines (US national) — widely available in New York, California, and major US wine markets; in Canada through LCBO and private import; BC Liquor does not typically list but available through private import to restaurants',
        'culinary_application': 'Loureiro\'s floral-saline character creates a distinctive pairing with Pacific halibut ceviche where the lime and floral notes mirror the citrus marinade; outstanding with chèvre and Dungeness crab where the granite mineral and floral combination resonates with the ocean-mineral character of the shellfish; the PCT provenance story (same granite formation as neighboring Galicia, the Atlantic wine culture that shaped Portuguese maritime exploration) makes it compelling for restaurants with Portuguese culinary focus'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
