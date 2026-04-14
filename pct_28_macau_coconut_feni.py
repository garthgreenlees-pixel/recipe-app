import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='tea',
    region='Macau — Peninsula and Taipa (Portuguese-Macanese Milk Tea, Galão Heritage, Colonial Café Culture)',
    output_dir='.',
    starting_entry=1,
    session_number=29,
    running_total=90
)

session.add_producer({
    'tradition': 'tea',
    'name': 'Café Safari — Macau Colonial Heritage Café',
    'location': 'Travessa do Aterro Novo, Macau Peninsula, Macau SAR',
    'description': 'One of the oldest continuously operating Portuguese-Macanese cafés in Macau, producing the distinctive Macau milk tea (galão-style preparation using evaporated and condensed milk with a blend of Ceylon and local tea) alongside the signature Macanese egg tart (pastéis de nata) in the Portuguese colonial tradition. The café culture of Macau represents a 450-year synthesis of Portuguese café and confectionery traditions (from mainland Portugal via Portuguese sailors who arrived in Macau from 1557) with local Chinese milk tea and Cantonese pastry culture. The Macanese galão is prepared differently from both Lisbon galão and Hong Kong-style milk tea: a Ceylon black tea base blended with oolong for fragrance, combined with a specific ratio of evaporated and condensed milk that gives the Macanese version a richer, denser sweetness than the Hong Kong style, and served warm in a traditional Portuguese handle glass.',
    'founded': 'ca. 1970s (current location)',
    'region': 'Macau SAR, China',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'tea',
    'name': 'Margaret\'s Café e Nata — Macau',
    'location': 'Rua Almirante Sérgio, Macau Peninsula, Macau SAR',
    'description': 'Macau\'s most internationally famous café, founded by Margaret Wong, producing what many consider the finest Portuguese-Macanese egg tarts and galão milk tea in the SAR. Margaret\'s egg tart (pastéis de nata Macau-style) differs from the Lisbon original in the pastry shell (flakier, richer in lard content) and the custard filling (set slightly harder, more cooked through than the wobbly center of Belém-style nata). The café is a pilgrimage destination for both Hong Kong visitors and food writers, and represents the living preservation of Portuguese café culture 25 years after Macau\'s 1999 handover to China ended Portuguese colonial administration. The café produces its own tea blend — a specific combination of Ceylon OP (orange pekoe) and Taiwanese high-mountain oolong — for its galão and milk tea service.',
    'founded': '1992',
    'region': 'Macau SAR, China',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Macau Tourism Cultural Association — Café Culture Documentation',
    'type': 'cultural_institution',
    'description': 'The government tourism board of Macau SAR documenting and promoting surviving elements of Portuguese-Macanese culture including café traditions, galão preparation, pastéis de nata, and the distinctive Macanese language (Patuá). Not a commercial purveyor but the institutional body through which Macau\'s café culture products reach international awareness.',
    'markets_served': ['Macau', 'Hong Kong', 'China', 'International'],
    'traditions_carried': ['tea', 'coffee'],
    'website': 'macaotourism.gov.mo',
    'verified': False
})

session.add_beverage({
    'name': 'Macanese Galão — Portuguese-Colonial Milk Tea, Ceylon-Oolong Blend, Condensed Evaporated Milk',
    'category': 'tea',
    'subcategory': 'milk_tea',
    'origin': 'Macau',
    'region': 'Macau SAR, China',
    'producer': 'Margaret\'s Café e Nata — Macau',
    'alcohol_content': 0.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'The Macanese galão is the beverage artifact of Portugal\'s longest-lasting colonial presence: Macau was a Portuguese territory from 1557 to 1999 — 442 years of Lusophone administration on a small peninsula at the mouth of the Pearl River Delta, creating the most complex cultural synthesis in the Portuguese colonial world. The galão itself originated in mainland Portugal as a foamy coffee drink (one-quarter espresso, three-quarters steamed milk foam), but Macau\'s version evolved through contact with both Cantonese milk tea culture and the colonial import of Ceylon tea and sweetened condensed milk (introduced to East Asia by European traders from the 1860s onward). The specific tea blend used in Macanese galão — traditionally a Ceylon OP base for body with Taiwanese or Chinese oolong for fragrance — reflects the geographic position of Macau as a trading hub between Portugal\'s Ceylon (Sri Lanka) and India tea sources and the regional East Asian tea culture. The condensed and evaporated milk combination used in Macau (rather than fresh milk used in Portugal or the Hong Kong-style strained-milk preparation) is a direct consequence of the refrigeration limitations of colonial Macau before the 20th century, when canned milk products were more reliable than fresh dairy in the subtropical climate. The resulting drink is denser, sweeter, and more tea-forward than the Lisbon galão while being less "silky" than the finest Hong Kong milk teas — a genuinely hybrid preparation that belongs fully to neither tradition.'
    ),
    'production_technique': (
        'Margaret\'s and the best Macanese café operators prepare the galão through a specific multi-step process that distinguishes the Macanese style from both its Portuguese and Hong Kong cousins. First, a Ceylon OP tea is brewed at high concentration: 15–20g of tea per liter of water at 94–96°C for 4–5 minutes (compared to the 2–3 minute steep of delicate teas), producing a very dark, tannic, astringent concentrate. This is blended 1:4 with a separately brewed high-mountain oolong tea at 90–92°C for 3 minutes — the oolong infusion adds floral complexity (orchid, grapefruit, osmanthus) to the tannin foundation of the Ceylon base. The tea blend is then strained through a fine mesh sock (known as the "silk stocking" method in Hong Kong, adapted in Macau) into a ceramic pitcher. Condensed milk (sweetened, approximately 320g sugar per 1L) and evaporated milk (unsweetened, concentrated) are combined in a 3:1 ratio (evaporated to condensed) and heated to 60–70°C. The Macanese galão is assembled by pouring the hot tea blend over the hot milk mixture at a ratio of 3:2 (tea to milk), creating the characteristic amber color and sweetened-milk fragrance. Served in a traditional Portuguese handle glass (copo de vidro com asa) at approximately 65°C — the drinking temperature standard in Macanese café culture.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Hong Kong-style milk tea (silk stocking, Ceylon-Assam blend)',
            'connection': 'Macanese galão and Hong Kong milk tea share the strained Ceylon tea base and condensed/evaporated milk tradition, but diverge in the oolong addition (Macau) vs pure black tea blend (Hong Kong) and in the milk ratio — Hong Kong milk tea is typically less sweet and more tea-forward than the Macanese version, reflecting the British colonial influence on Hong Kong versus the Portuguese colonial influence on Macau'
        },
        {
            'tradition': 'Portuguese galão (mainland origin, coffee-based)',
            'connection': 'The Macanese galão retains the name and glass format of the Lisbon original but substitutes tea for coffee — a substitution that occurred through 442 years of adaptation to the tea-drinking culture of China and the availability of Ceylon and India tea through Portuguese colonial trade routes, demonstrating how a beverage format can migrate across substance while retaining its cultural identity'
        },
        {
            'tradition': 'Sri Lanka Ceylon milk tea (the source tradition)',
            'connection': 'The Ceylon tea that forms the Macanese galão\'s backbone traces directly to Portuguese Ceylon (Sri Lanka was Portuguese from 1505 to 1658 before Dutch and then British colonial succession) — the tea plant was established in Ceylon after the Portuguese colonial period, but Portuguese trade routes through Ceylon and India created the channel through which Ceylon tea reached Macau in the 19th century, completing the PCT beverage loop'
        }
    ],
    'sensory_profile': {
        'appearance': 'Warm amber-ochre; the milk-tea combination creates a naturally cloudy, rich appearance distinct from black tea clarity or coffee opacity; medium viscosity from the condensed milk sugar; thin skin of foam if steamed milk is used in modern preparation',
        'nose': 'Ceylon tea astringency, warm milk-caramel sweetness from condensed milk, subtle oolong florality (orchid, grapefruit), bread-like warmth from evaporated milk reduction — the character is immediately identifiable as Portuguese-influenced East Asian hybrid: Western dairy-sweet over Eastern tea structure',
        'palate': 'Full body from condensed milk density, sweet-milky entry, strong Ceylon tea astringency in the mid-palate that cuts through the sweetness, oolong floral finish, long warm-milk aftertaste — the balance of sugar and tannin is the defining quality of superior Macanese galão preparation'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Hotel Lobby / Tourist Standard',
            'criteria': 'Commercial tea bags, standard condensed milk, no oolong addition, made in advance and held warm — convenient but lacks the depth of fresh preparation; widely available in Macau\'s casino hotels'
        },
        {
            'tier': 2,
            'tier_name': 'Traditional Café Standard (Margaret\'s, Café Safari)',
            'criteria': 'High-quality Ceylon OP loose leaf, oolong addition, freshly brewed in correct ratios, served in traditional handle glass — the authentic Macanese galão tradition at its accessible best'
        },
        {
            'tier': 3,
            'tier_name': 'Heritage Café (Privately Sourced Tea Blend)',
            'criteria': 'Specific house tea blends developed over decades (some cafés maintain proprietary Ceylon-oolong ratio recipes), fresh dairy elements, traditional silk-sock straining — the connoisseur tier that regulars seek out and that represents peak Macanese café culture'
        },
        {
            'tier': 4,
            'tier_name': 'Heritage Galão with Pastéis de Nata Pairing',
            'criteria': 'The complete Macanese café ritual: galão prepared to house specification alongside freshly baked Macanese pastéis de nata (egg tarts with flaky lard-based pastry and softly set custard), consumed at a marble-topped table in a historic café space — the cultural experience cannot be separated from the product quality'
        }
    ],
    'service_intelligence': {
        'temperature': 'Served at 65–70°C in traditional cafés — hot enough to maintain temperature through slow consumption; the condensed milk sweetness is best expressed warm; cold versions exist (Macanese "iced galão") but are a modern adaptation rather than the traditional form',
        'vessel': 'Traditional Portuguese handle glass (clear glass with a small metal or ceramic handle); or a ceramic café cup in modern contexts; the visual amber color through clear glass is part of the Macanese café aesthetic and should not be obscured in opaque vessels',
        'cultural_context': 'The galão in Macau is inseparable from the pastéis de nata and the space of the heritage café — ordering a galão at Margaret\'s or Café Safari is participating in the 442-year Portuguese colonial legacy in East Asia; for PNW restaurant programming, the Macanese galão-with-nata pairing represents the PCT\'s most photogenic and culturally distinct beverage moment'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Margaret\'s Café e Nata, Macau — the internationally recognized benchmark for Macanese galão and pastéis de nata preparation',
        'north_america_access': 'Not commercially exported; the galão is a made-to-order café drink accessible only in Macau (and Hong Kong\'s Portuguese-influenced cafés); however, the Ceylon-oolong tea blend and condensed/evaporated milk components are universally available and can be prepared in PNW café or restaurant contexts',
        'culinary_application': 'PNW implementation: the Macanese galão preparation method (Ceylon-oolong blend, condensed/evaporated milk, silk-sock straining, handle glass service) is reproducible in restaurant café programs as part of a PCT beverage menu; the cultural narrative of 442 years of Portuguese-Chinese synthesis is compelling for menus exploring colonial food history; pairs naturally with Portuguese-inspired egg tart preparations where the tannin-sweet tea cuts through the rich custard'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region('spirits', 'India — Goa South (Coconut Feni, Coconut Palm Sap Spirit, Neura Village Tradition)')

session.add_producer({
    'tradition': 'spirits',
    'name': 'Goa Kokni Distillers — Traditional Coconut Feni',
    'location': 'Neura and Pilerne, North Goa, India',
    'description': 'Collective term for traditional coconut feni distillers in the Neura, Pilerne, and Calangute zones of North Goa, where the toddy-tapper (rendeiro) tradition has been maintained for 500+ years. Coconut feni (as distinct from cashew feni — a separate GI-protected spirit) is produced from freshly tapped coconut palm sap (neero/toddy) that begins spontaneous fermentation within hours of collection. The rendeiro tapper climbs the coconut palms twice daily (dawn and dusk) using a specialized climbing ring (math), collecting the neero in clay pots strapped to the trunk. The tradition of palm-sap collection and immediate copper-pot distillation was introduced by or refined under Portuguese colonial administration, which regulated feni production from the early 16th century and established the copper alembic (bhaati) still as the standard production apparatus.',
    'founded': 'ca. 1510 (Portuguese colonial period)',
    'region': 'North Goa, India',
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Coconut Feni — Goa Palm Sap Spirit, Toddy Tapper Dawn-to-Dusk Collection, Copper Bhaati Still',
    'category': 'spirits',
    'subcategory': 'palm_spirit',
    'origin': 'India',
    'region': 'Goa, India',
    'producer': 'Goa Kokni Distillers — Traditional Coconut Feni',
    'alcohol_content': 42.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'Coconut feni (also spelled "fenny") is produced exclusively from coconut palm sap collected in Goa — a legal restriction that links the spirit entirely to the Goan coastal ecosystem where the Cocos nucifera palm has been cultivated for 3,000+ years. The terroir of coconut feni is the palm ecology itself: individual coconut palms produce sap of different chemical composition depending on the palm\'s age (older trees produce higher-Brix sap), soil salinity (coastal palms near the Arabian Sea produce a distinctly saline neero), seasonal variation (pre-monsoon March–May tapping produces the richest sap; post-monsoon October–January produces lighter, more aromatic neero), and the specific clay pot in which the neero is collected (the clay contributes mineral complexity through leaching into the fresh sap). The Portuguese colonial presence in Goa from 1510 onward is directly encoded in coconut feni\'s production: the copper alembic (bhaati) pot still was introduced by Portuguese distillers who brought the technology from their Atlantic island estates (Madeira, Azores, Cape Verde), where a similar sap-to-spirit tradition existed for sugar cane. The Portuguese technical transfer to Goa created a new application: applying Madeira-era copper still technology to the local palm sap tradition that predated Portuguese arrival, creating a genuinely hybrid production system. Unlike cashew feni (which received GI protection in 2009), coconut feni remains unprotected under any Indian geographical indication, leaving the tradition more vulnerable to standardization and commercial dilution.'
    ),
    'production_technique': (
        'The rendeiro tapper begins before dawn, climbing coconut palms using a math (climbing ring) looped around ankles and the palm trunk, ascending trees of 15–25m height. At the top, the tapper slices the tip of an immature coconut flower bud (inflorescence) and attaches a clay collection pot (madds) that will fill with neero over 12 hours. The incision is refreshed with each collection — the tapper shaves a thin slice from the previous cut to expose fresh tissue for maximum sap flow. Each productive palm yields 1.5–2.5 liters of neero per 12-hour collection period; a traditional rendeiro manages 30–60 palms in a morning circuit. The freshly collected neero (sweet, 15–18 Brix, pH 7.0) begins spontaneous fermentation from wild Saccharomyces yeasts within 2–4 hours at ambient Goa temperature (28–36°C). By the afternoon collection, the morning neero has typically reached 6–8% ABV from spontaneous fermentation — this mildly alcoholic "toddy" is consumed fresh by local drinkers as a beverage separate from feni. For feni production, the rendeiro combines the twice-daily collections into a copper bhaati (pot still system) for double distillation. The first distillation produces "urrack" — a single-distilled 15–20% ABV spirit that is consumed as a lighter intermediate product. The second distillation of urrack produces "cazulo" or "feni" at 42–45% ABV — the traditional coconut feni that has been produced in this form since the Portuguese colonial era. No aging, no filtration — coconut feni is consumed fresh within weeks of production for maximum aromatic expression.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Cashew Feni GI (Goa sibling tradition, same copper still)',
            'connection': 'Coconut feni and cashew feni are Goa\'s twin spirit traditions using identical copper bhaati pot still technology but different fermentable substrates — palm sap (coconut) vs cashew apple juice — producing dramatically different aromatic profiles: coconut feni is more delicate, floral, and lightly sweet; cashew feni is more pungent, tropical-fruity, and assertive'
        },
        {
            'tradition': 'Thai and Filipino lambanog (coconut palm wine spirits)',
            'connection': 'Coconut feni occupies the same register as Philippine lambanog (distilled coconut palm toddy) and Thai toddy spirits — all produced from spontaneously fermented coconut sap using simple pot still distillation inherited from colonial contact (Spanish in the Philippines, Portuguese in Goa) — representing the pan-tropical coconut spirit tradition that Portuguese colonial trade routes connected across Asia'
        },
        {
            'tradition': 'Mezcal sotol (desert spoon agave, similar sap-collection tradition)',
            'connection': 'Both coconut feni and sotol (distilled from Dasylirion whipplei desert spoon plants) require skilled climber-tappers to access the sap production organ of the plant (coconut palm inflorescence bud vs agave heart) using climbing and cutting techniques maintained as specialist artisan knowledge — both represent the intersection of agricultural skill, botanical knowledge, and distillation technology in indigenous-colonial beverage traditions'
        }
    ],
    'sensory_profile': {
        'appearance': 'Water-clear, no color from non-aging; light viscosity at 42% ABV; slight oiliness visible when swirled from the natural esters in the palm sap-derived spirit; no cloudiness in well-made expression',
        'nose': 'Delicate and distinctive: fresh coconut water (not coconut meat — the sap rather than the endosperm character), light floral (frangipani, jasmine trace), subtle tropical sweetness, acetone-adjacent note from rapid fermentation of the fresh sap, light lactic sourness from the fermentation microbiology — gentler and more aromatic than cashew feni',
        'palate': 'Light-medium body, immediate coconut sweetness, floral mid-palate, clean finish with light warmth from 42% ABV — more delicate than cashew feni\'s assertive pungency; the freshness of the sap character is preserved through the rapid collection-to-distillation cycle'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Bottled Coconut Feni',
            'criteria': 'Industrial-scale production using stored neero (sap collected and held before fermentation), standardized yeast addition, column still distillation — consistent but lacking the fresh sap character of artisanal production'
        },
        {
            'tier': 2,
            'tier_name': 'Traditional Rendeiro Production (Direct Purchase)',
            'criteria': 'Twice-daily fresh collection, spontaneous fermentation, copper bhaati double distillation — the authentic traditional form; available by direct purchase from licensed rendeiro distillers in Goa at very low cost'
        },
        {
            'tier': 3,
            'tier_name': 'Named Rendeiro Reserve (Coastal Palm Selection)',
            'criteria': 'Identified individual palms with documented sap character (some rendeiros maintain "estate" palms known for exceptional neero quality), seasonal selection for maximum Brix sap, careful distillation — the craft tier emerging in Goa\'s premium feni movement'
        },
        {
            'tier': 4,
            'tier_name': 'Aged Coconut Feni (Clay Pot or Oak, Experimental)',
            'criteria': 'Brief aging in traditional clay pots (which add mineral complexity from the unglazed earthenware) or ex-bourbon barrels — the aspirational tier being developed by a small number of Goa craft spirits producers who received export market interest after the cashew feni GI success'
        }
    ],
    'service_intelligence': {
        'temperature': 'Served at room temperature in traditional Goan context (28–33°C ambient) — the delicate fresh sap character is best expressed without cooling; modern bar service at 20°C is acceptable; never chilled below 15°C which closes the aromatic freshness',
        'vessel': 'Traditional: small ceramic cup or shot glass for the Goan "feni shot" culture; Modern service: small tulip glass or copita to concentrate the delicate floral aromatics; Cocktail: the "Feni Sour" (coconut feni, lime, sugar, egg white) showcases the feni\'s floral character while managing the raw spirit intensity',
        'cultural_context': 'Coconut feni in Goa is the "every occasion" spirit — consumed as a digestive after the midday meal, as a sundowner on beach shacks, in cocktails at beach-bar culture, and medicinally (with ajwain seeds or turmeric) in traditional Goan home medicine; the rendeiro tradition is an endangered craft, with younger Goans often not learning the climbing technique that requires physical conditioning and traditional knowledge from childhood'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Traditional rendeiro distillers in Neura and Pilerne, North Goa — the artisanal standard; for export, Cazulo Premium Feni (primarily known for cashew) also produces a limited coconut feni expression',
        'north_america_access': 'Not commercially exported; accessible through Goa travel; Santra Beverages (US importer for cashew feni) has expressed interest in coconut feni export as a follow-on to the cashew GI program',
        'culinary_application': 'Coconut feni\'s delicate character works in cocktail applications where the coconut sap origin creates natural resonance: Piña Colada base where the spirit\'s coconut note amplifies the coconut cream; tropical fruit daiquiri where the feni\'s floral character complements mango or passion fruit; the Goan beach-shack Feni Sour (lime-sugar-egg white) transfers elegantly to PNW bar programs with a Pacific Islands cross-cultural narrative'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
