import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='fermented',
    region='Malaysia — Malacca and Penang (Peranakan Fermented Traditions, Tuak, Temple Drinks)',
    output_dir='.',
    starting_entry=1,
    session_number=21,
    running_total=74
)

session.add_producer({
    'tradition': 'fermented',
    'name': 'Tuak Dayak Community Producers (Sarawak)',
    'location': 'Kuching and Serian divisions, Sarawak, Malaysian Borneo',
    'description': 'Collective of Iban Dayak longhouse communities producing traditional fermented rice wine (tuak) for ceremonial, festival, and harvest contexts. Production follows pre-Portuguese oral traditions but intersects with Malacca trade-route influence through spiced variants developed for coastal Peranakan consumption. The Gawai Dayak festival (June 1–2) drives the largest production cycles; communities maintain grandmother-transmitted recipes specifying local glutinous rice varieties, wild yeast cultures (ragi), and fermentation vessel types (clay sura pots or woven bamboo containers).',
    'founded': None,
    'region': 'Sarawak, Malaysian Borneo',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'fermented',
    'name': 'Nyonya Heritage Producers — Malacca',
    'location': 'Malacca City (Bandar Hilir), Malacca, Malaysia',
    'description': 'Informal network of Peranakan (Baba-Nyonya) home producers maintaining fermented temple offerings and ceremonial drink preparation in Jonker Street heritage corridor. Their traditions blend Hokkien-Chinese fermentation techniques introduced by 15th-century Malacca Chinese merchant settlers with Malay botanical aromatics (pandan, lemongrass, galangal). Portuguese colonial-era cinnamon and clove trade routes enriched spice vocabularies still present in festive fermented drinks. Products include pulut hitam (fermented black glutinous rice extract), rice wine for ancestral altar offerings, and tuak variants for Chinese New Year longhouse-style communal ceremonies.',
    'founded': None,
    'region': 'Malacca, Malaysia',
    'website': None,
    'verified': False
})

session.add_purveyor({
    'name': 'Sarawak Cultural Village Shop / Borneo Heritage Foods',
    'type': 'cultural_institution',
    'description': 'State-operated cultural institution in Kuching selling certified traditional Dayak food and beverage products including packaged ragi cultures, fermented rice wine sets, and tuak extract concentrates for diaspora and culinary tourism markets. Exports select items to Singapore and Australia.',
    'markets_served': ['Malaysia', 'Singapore', 'Australia'],
    'traditions_carried': ['fermented', 'indigenous_malaysia'],
    'website': 'sarawakmuseum.gov.my',
    'verified': False
})

session.add_beverage({
    'name': 'Tuak — Iban Dayak Fermented Glutinous Rice Wine, Sarawak',
    'category': 'fermented',
    'subcategory': 'rice_wine',
    'origin': 'Malaysia',
    'region': 'Sarawak, Malaysian Borneo',
    'producer': 'Tuak Dayak Community Producers (Sarawak)',
    'alcohol_content': 8.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'Tuak is anchored in the interior highlands of Sarawak — Borneo\'s Malaysian state — where Iban Dayak longhouse communities cultivate several distinct glutinous rice varieties across swidden (shifting cultivation) plots at 100–600m elevation in the Rejang and Saribas river drainage systems. The rice ecology is inseparable from Borneo\'s equatorial monsoon pattern: a single annual harvest in November–December, followed by fermentation ceremonies tied to the Gawai agricultural cycle. The ragi (wild yeast starter culture) is produced from sun-dried rice flour mixed with wild herb compounds specific to each longhouse lineage — many containing antimicrobial forest botanicals unavailable commercially. Water sources are upland streams filtered through sandstone and laterite, imparting mineral softness characteristic of Borneo interior waterways. The tradition predates Malacca Sultanate (1400 AD) and shows no Portuguese influence in core technique, though coastal tuak variants absorbed Peranakan spice vocabulary (clove, star anise) through 16th–17th century trade contact along the Sarawak River trade routes.'
    ),
    'production_technique': (
        'Traditional tuak production begins with steaming glutinous rice (pulut) in woven bamboo steamers, cooling on palm-leaf mats, then inoculating with crushed ragi starter. The ragi culture contains multiple wild yeast strains (predominantly Saccharomyces cerevisiae var. chevalieri and Mucor sp.) mixed with dried herbs including Alpinia galanga (greater galangal), Zingiber officinale (ginger), and locally gathered forest roots that vary by lineage. The inoculated rice is packed into clay sura pots or sealed bamboo tubes and fermented at ambient Borneo temperature (28–32°C) for 3–10 days. Primary fermentation produces carbon dioxide evident as a dense white foam on day 2–3; the pot is sealed with banana leaf and bamboo strip binding after foam subsides. At 7–10 days, water is added (ratio 1:1 by volume) and the mixture re-sealed for secondary infusion lasting 3–7 more days. The resulting liquid is strained through woven bamboo filters and consumed fresh within 2–4 weeks. No distillation, pasteurization, or sulfite addition. Alcohol content ranges 6–12% depending on ragi potency, water addition ratio, and ambient temperature. Ceremonial grades use less water addition for 12–15% strength, reserved for Gawai opening offerings.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Japanese sake',
            'connection': 'Both tuak and sake use rice as fermentable substrate with mold-assisted saccharification — koji mold (Aspergillus oryzae) in sake, Mucor sp. in tuak ragi — followed by yeast fermentation, making both parallel discoveries of simultaneous saccharification-fermentation (SSF) long predating European beer-wine traditions'
        },
        {
            'tradition': 'Korean makgeolli',
            'connection': 'Tuak and makgeolli share cloudy, unfiltered rice wine character with live yeast cultures, short shelf life of 1–2 weeks, and deep ceremonial significance in ancestral offering contexts — both representing the oldest tier of national fermented beverage culture'
        },
        {
            'tradition': 'Portuguese colonial spice trade',
            'connection': 'Coastal Malacca-influenced tuak variants absorbed Portuguese-era spice vocabulary (clove from Maluku, cinnamon from Ceylon) through 16th-century Sarawak River trade, creating spiced tuak styles that mirror how Portuguese merchants blended Old World techniques with Asian botanical networks'
        }
    ],
    'sensory_profile': {
        'appearance': 'Opaque white to pale cream; naturally cloudy from suspended rice solids and yeast; no clarity intended; occasional fine foam ring at rim in fresh product within 48 hours of straining',
        'nose': 'Fresh cooked glutinous rice, ripe banana, mild lactic acid sourness, subtle galangal warmth, faint forest floor earthiness from ragi botanicals — alive and metabolically active',
        'palate': 'Silky body, moderate sweetness from residual rice sugars, gentle lactic tartness, clean yeast presence, galangal-ginger spice finish, low tannic grip, lingering warm rice sweetness that fades into clean mineral dryness'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Packaged',
            'criteria': 'Standardized ragi cultures, industrial glutinous rice, consistent ABV targeting 6–8%, bottled with preservatives for 30-day shelf life, available in Sarawak supermarkets and cultural village shops'
        },
        {
            'tier': 2,
            'tier_name': 'Longhouse Communal',
            'criteria': 'Family ragi cultures maintained across generations, local swidden rice varieties, fresh 7–14 day fermentation, consumed on-site or within 2 weeks, no additives — the authentic baseline of the tradition'
        },
        {
            'tier': 3,
            'tier_name': 'Gawai Ceremonial Grade',
            'criteria': 'Best available glutinous rice from the season\'s harvest, senior matriarch-controlled ragi cultures, minimal water addition for 12–15% ABV, consumed as the first-glass offering to Petara (spirits) at Gawai harvest festival opening ceremony'
        },
        {
            'tier': 4,
            'tier_name': 'Heirloom Lineage Reserve',
            'criteria': 'Single-lineage ragi cultures documented to specific longhouse ancestry (5+ generations), heritage glutinous rice varieties from controlled swidden plots, presented in decorated sura clay vessels as ceremonial gifts — rarely commercialized, exchanged as inter-community diplomatic gifts'
        }
    ],
    'service_intelligence': {
        'temperature': 'Served at 18–22°C (ambient Borneo room temperature); slight chilling to 15°C acceptable for urban service contexts; never ice-cold, which kills live yeast and suppresses aromatic expression',
        'vessel': 'Traditional: small ceramic or clay cups (mangkok); Modern service: wide-mouthed ceramic bowl or clear glass tumbler showing cloudy white color; communal drinking from shared clay jar via bamboo straws in ceremonial contexts',
        'ritual_context': 'Tuak is inseparable from the Gawai toast sequence: the senior host offers the first cup skyward for Petara (spirits), second to ancestors, third to distinguished guests — refusal of the offered cup is considered cultural disrespect in longhouse contexts',
        'food_context': 'Natural accompaniment to Iban festival foods: ayam pansuh (chicken in bamboo), umai (raw fish salad), paku fern, wild boar preparations — the lactic acidity cuts through fat and amplifies jungle herb aromatics'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Tuak Dayak Community Producers — Serian Division, Sarawak (the gold standard for ceremonial-grade tuak)',
        'north_america_access': 'Not commercially exported to North America; accessible through Sarawak diaspora community networks in Vancouver BC and Toronto; some ragi starter cultures available via specialty Asian fermentation suppliers',
        'culinary_application': 'Emerging use in PNW Borneo-influenced restaurants as sauce base (reduces beautifully into a rice-sweet glaze), fermented beverage pairing alternative to sake in Japanese-fusion contexts, lactic acid source in modernist fermentation menus'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region('fermented', 'Malaysia — Penang (Peranakan Heritage, Nyonya Ceremonial Drinks, Temple Offerings)')

session.add_producer({
    'tradition': 'fermented',
    'name': 'Penang Peranakan Mansion Heritage Kitchen',
    'location': 'George Town, Penang, Malaysia',
    'description': 'Living museum and heritage institution preserving Baba-Nyonya (Peranakan Chinese-Malay) culinary traditions in George Town UNESCO World Heritage Site. Maintains documentation and demonstration of pre-colonial and colonial-era fermented beverage traditions including nyonya kuih ferments, rice wine for ancestral altar ceremonies, and fermented tamarind water for temple offerings. The culinary heritage intersects Portuguese colonial spice trade history directly: George Town was established 1786 under Francis Light for the East India Company, but Peranakan culture predates this by 300 years — the Baba community emerged from Malacca Chinese traders who married Malay women ca. 1400–1500 AD during the peak of the Malacca Sultanate era when Portuguese conquest in 1511 drove many north to Penang.',
    'founded': 'ca. 1400s (cultural tradition); Penang Peranakan Mansion museum: 2002',
    'region': 'Penang, Malaysia',
    'website': 'pinangperanakansion.com.my',
    'verified': False
})

session.add_beverage({
    'name': 'Pulut Hitam Fermented Black Glutinous Rice Extract — Peranakan Penang Temple Offering',
    'category': 'fermented',
    'subcategory': 'ritual_rice_ferment',
    'origin': 'Malaysia',
    'region': 'Penang, Malaysia',
    'producer': 'Penang Peranakan Mansion Heritage Kitchen',
    'alcohol_content': 4.0,
    'price_tier': 'everyday',
    'terroir_origin': (
        'Pulut hitam (black glutinous rice) is the deep-purple heritage rice variety cultivated across river delta lowlands of Kelantan, Terengganu, and Penang hinterland. Its dark color derives from anthocyanin-rich outer bran layers — the same compounds that give acai, black sesame, and purple yam their antioxidant character. In Peranakan Penang, pulut hitam fermentation connects three cultural strata: indigenous Malay rice cultivation predating the Malacca Sultanate; Hokkien-Chinese temple offering traditions carried by 15th-century merchant settlers; and Portuguese colonial-era spice trade influence that introduced palm sugar (gula melaka) from Borneo as the standard sweetener, replacing earlier honey-based preparations. The George Town UNESCO heritage precinct where Nyonya fermented beverage traditions survive most intact sits within 2km of Fort Cornwallis, the 1786 British East India Company fort that formalized Penang as a trading hub along the same Portuguese-pioneered spice routes.'
    ),
    'production_technique': (
        'Pulut hitam fermented extract begins with soaking the black glutinous rice for 8–12 hours in filtered water, releasing the anthocyanin pigments into a deep purple liquid. The soaked grains are steamed in a bamboo steamer lined with banana leaf until fully cooked, then spread on rattan trays to cool to 30–35°C. Crushed ragi (wild yeast starter containing Mucor sp. and Saccharomyces cerevisiae) is dusted evenly across the cooked grains, which are then placed in glazed ceramic fermentation crocks and covered with muslin cloth. Fermentation proceeds for 3–5 days at ambient tropical temperature (28–33°C), during which the ragi converts residual starches to sugars and alcohols simultaneously. The resulting mash is pressed through cheesecloth to extract a deep purple liquid with natural sweetness from residual sugars and gentle lactic tartness. In ceremonial preparation, gula melaka (palm sugar blocks) is dissolved into the extract at 1:20 ratio, creating a mildly alcoholic (3–6% ABV), sweet-tart, violet-colored beverage. Coconut milk is sometimes layered over the top for ancestral altar presentations — the visual separation of white-over-purple representing heaven and earth in Peranakan cosmology. Commercial versions available in Penang market are typically non-alcoholic or very low alcohol (under 0.5%), with the fermented depth replaced by sour plum or tamarind acidulants.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Japanese amazake',
            'connection': 'Both pulut hitam extract and amazake are low-alcohol (under 6% ABV) sweet rice ferments consumed warm or at room temperature as ceremonial and nourishing beverages, with a mildly sweet-sour character from simultaneous saccharification-fermentation rather than discrete mashing and fermentation stages'
        },
        {
            'tradition': 'Ethiopian tej (honey wine)',
            'connection': 'Both beverages occupy the sweet, low-tannin, low-acid fermented drink register used for ceremonial and daily nourishment across non-European traditions, combining local agricultural staples (rice vs honey) with wild fermentation cultures in unfiltered, short-shelf-life preparations tied to agricultural calendars'
        },
        {
            'tradition': 'Portuguese vinho verde (green wine)',
            'connection': 'The light body, residual sweetness, natural carbonation from live fermentation, and short consumption window of pulut hitam extract parallel the fresh, low-alcohol, slightly effervescent character of young Vinho Verde — both represent beverages designed for immediate, context-specific consumption rather than cellaring'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep violet-purple, nearly opaque; rich color from anthocyanin extraction; natural cloudiness from suspended rice solids; surface sheen from residual palm sugar; visually striking — one of the most colorful natural fermented beverages globally',
        'nose': 'Dark berry, palm sugar caramel, faint lactic sourness, warm coconut undertone if traditional preparation, subtle yeasty bread note, clean finish without harshness',
        'palate': 'Medium-full body, natural sweetness balanced by gentle lactic tartness, purple rice nuttiness, gula melaka caramel depth, low alcohol warmth, lingering coconut-sweet finish — more dessert-beverage than fermented wine in character'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Hawker',
            'criteria': 'Non-fermented or minimal fermentation, artificial sweeteners, food coloring to deepen color, sold chilled in styrofoam cups at Penang hawker markets — taste profile is sweet-starchy without authentic lactic complexity'
        },
        {
            'tier': 2,
            'tier_name': 'Heritage Market (Pasar Malam)',
            'criteria': 'Authentic pulut hitam variety, ragi fermentation 3–4 days, gula melaka sweetening, sold in glass containers at night markets — represents accessible traditional preparation with genuine fermented character'
        },
        {
            'tier': 3,
            'tier_name': 'Nyonya Home Preparation',
            'criteria': 'Heritage Nyonya recipes with grandmother-transmitted ragi cultures, organic pulut hitam, Sarawak gula melaka blocks, 5-day fermentation, coconut milk layer — the authentic ceremonial register'
        },
        {
            'tier': 4,
            'tier_name': 'Ancestral Temple Grade',
            'criteria': 'Prepared exclusively by senior Nyonya matriarchs for Chinese New Year, Hungry Ghost Festival, and ancestral anniversary ceremonies — uses the eldest available pulut hitam variety, coldest water available for slower fermentation, presented in heirloom ceramic vessels'
        }
    ],
    'service_intelligence': {
        'temperature': 'Served warm (40–50°C) in ceremonial contexts as a nourishing ancestral offering drink; chilled (8–12°C) in modern café contexts as a sweet fermented dessert beverage; room temperature also common at hawker stalls',
        'vessel': 'Traditional: small handleless ceramic tea cups or shallow ceremonial bowls; Modern: clear glass tumbler to showcase the violet color; Ceremonial: the family\'s heirloom porcelain bowls reserved for altar presentations',
        'pairing_philosophy': 'Natural accompaniment to Nyonya kuih (steamed rice cakes, coconut-pandan sweets); the anthocyanin acidity cuts through rich coconut milk preparations; works as a non-alcoholic or very low-alcohol digestive alternative in multicourse Peranakan banquets'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Penang Peranakan Mansion Heritage Kitchen (George Town, Penang) — the most documented source of ceremonial-grade preparation',
        'north_america_access': 'Not commercially exported; available through Penang diaspora communities in Vancouver BC Chinatown; packaged pulut hitam rice widely available in Asian supermarkets for home preparation; ragi cultures available through Breadtopia and specialty Southeast Asian fermentation suppliers',
        'culinary_application': 'PNW culinary application: anthocyanin extract as natural purple colorant for vinaigrettes; reduced extract as dessert sauce for coconut panna cotta; fermented extract as non-alcoholic alternative in multicourse beverage pairings for guests who do not consume alcohol'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
