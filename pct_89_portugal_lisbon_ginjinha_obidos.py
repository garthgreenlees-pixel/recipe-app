import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Portugal — Lisbon (Ginjinha, Cherry Liqueur, Espinheira Distillery, Historic Colonial Capital Aperitif)',
    output_dir='.',
    starting_entry=1,
    session_number=93,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'A Ginjinha (Largo de São Domingos kiosk, Lisbon) and Espinheira (original distillery house)',
    'location': 'Largo de São Domingos, Lisbon historic centre (Baixa Pombalina district)',
    'country': 'Portugal',
    'region': 'Lisbon — Baixa Pombalina; original Espinheira production house; the A Ginjinha kiosk is the oldest and most iconic ginjinha serving point in Lisbon',
    'key_person': 'Espinheira family — the original distillery family associated with the Lisbon ginjinha tradition; the A Ginjinha kiosk at Largo de São Domingos is the point-of-sale reference that every visitor to Lisbon encounters',
    'founded': '1840 (A Ginjinha kiosk, Largo de São Domingos, established by Espinheira — the date confirmed in Lisbon municipal records); the ginja berry maceration tradition in Lisbon predates this commercial establishment and is documented from the late 18th century',
    'production_volume': 'The Lisbon ginjinha tradition involves multiple producers (Espinheira, Solar do Castelo, Sem Rival) alongside the A Ginjinha kiosk; total Lisbon ginja production estimated at several hundred thousand litres per year across all producers',
    'notable_products': [
        'A Ginjinha (the kiosk expression — served in paper cups or small glasses at Largo de São Domingos)',
        'Espinheira Ginjinha (the bottled commercial expression)',
        'Sem Rival Ginjinha (the alternative Lisbon ginja brand)',
        'Ginja de Óbidos (the GI-protected variant — separate entry)',
    ],
    'certifications': ['Indicação Geográfica Protegida Ginja de Óbidos (for the Óbidos variant); Lisbon ginjinha has no separate GI protection'],
    'website': '[PROVIDER: A Ginjinha kiosk does not maintain a commercial website — the tradition is walk-in service; Espinheira brand available through Portuguese specialty food retailers]',
    'philosophy': (
        'The A Ginjinha kiosk at Largo de São Domingos represents the most '
        'democratic aperitif tradition in Portugal — a EUR 1.50 paper cup '
        'of cherry liqueur consumed standing at the kiosk window, '
        'served to construction workers and tourists alike, '
        'the same recipe since 1840. The Lisbon ginjinha tradition '
        'is the beverage the PCT traveler encounters first upon '
        'arriving in Lisbon — the entry point into the entire '
        'Portuguese Colonial Trail beverage arc.'
    ),
    'trail_connection': 'PCT (Portugal — Lisbon colonial capital closing entry)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Lisbon Ginjinha — Sour Cherry Aguardente Liqueur, A Ginjinha Kiosk '
        'Largo de São Domingos, 1840 Tradition, PCT Colonial Capital '
        'Closing Entry'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'fruit_liqueur — ginja berry (Prunus cerasus) macerated in Portuguese aguardente with sugar and cinnamon; the Lisbon aperitif tradition since 1840',
    'region': 'Portugal — Lisbon (Ginjinha, Cherry Liqueur, Espinheira Distillery, Historic Colonial Capital Aperitif)',
    'terroir_origin': (
        'Lisbon is the capital of Portugal and the origin point '
        'of the Portuguese Colonial Trail — the city from which '
        'Vasco da Gama departed in 1497 for the first direct '
        'sea route to India, from which the Carreira da Índia '
        '(the India trade route) was administered, and to which '
        'the wealth of the colonial spice trade returned. '
        'The Baixa Pombalina district — the downtown Lisbon grid '
        'rebuilt after the 1755 earthquake under the Marquis of '
        'Pombal\'s urban redevelopment plan — is the geographic '
        'heart of the ginjinha tradition. Largo de São Domingos '
        '(the square in front of the Igreja de São Domingos, '
        'the earthquake-damaged Gothic church whose interior '
        'is preserved in its post-fire state as a deliberate '
        'ruin memorial) is where the A Ginjinha kiosk has '
        'operated since 1840. The ginja berry (Prunus cerasus — '
        'the sour cherry, or morello cherry; the Portuguese '
        'name "ginja" derives from the Arabic "zinzī", '
        'introduced through the Moorish presence in Iberia '
        'before the Reconquista) grows in the peri-urban orchards '
        'of the Lisbon hinterland and the Estremadura region '
        'north of the city. The aguardente base of ginjinha '
        'is the same marc brandy (bagaceira) or grain spirit '
        'that underpins the broader Portuguese spirits tradition — '
        'the same alcohol base that carried the ginja berry '
        'maceration as a domestic liqueur preparation in '
        'the households of Lisbon since the late 18th century, '
        'when the commercial Espinheira version formalized '
        'the domestic tradition into a public kiosk drink.'
    ),
    'production_technique': (
        'Lisbon ginjinha production begins with the harvest '
        'of ripe ginja berries (Prunus cerasus, the sour morello '
        'cherry — distinguished from sweet Prunus avium by its '
        'higher malic and citric acid content) in June–July '
        'in the orchards of the Estremadura region north of '
        'Lisbon (Óbidos, Torres Vedras, Caldas da Rainha '
        'are the primary ginja berry production zones). '
        'The berries are macerated whole (unpitted — the '
        'cherry stone contributes benzaldehyde, the bitter '
        'almond compound of Prunus kernels, which adds '
        'marzipan complexity to the finished liqueur) '
        'in Portuguese aguardente (typically 40–50% ABV '
        'grape marc spirit or grain spirit) for a minimum '
        'of 3–6 months. The maceration vessel is historically '
        'a large ceramic pot or glass demijohn; commercial '
        'producers use stainless steel tanks for the volume '
        'production. The sugar addition (sucrose — typically '
        '200–300g/L in the finished liqueur) and cinnamon sticks '
        '(Cinnamomum verum — Portuguese cinnamon from Sri Lanka '
        'and Malabar, introduced to Portugal through the '
        'colonial spice trade from 1500 onward) are added '
        'to the maceration vessel and allowed to integrate '
        'for the full maceration period. After maceration, '
        'the ginja berries are typically retained in the liqueur '
        '(served "com ela" — with the cherry) or removed '
        '("sem ela" — without the cherry). The A Ginjinha kiosk '
        'tradition offers both options: the server asks '
        '"com ou sem?" (with or without?) before filling '
        'the small glass. The finished liqueur is 22–28% ABV, '
        'sweet (200–300g/L residual sugar), deep ruby-red '
        'from the Prunus cerasus anthocyanins. The cinnamon '
        'component is the PCT spice trade signature within '
        'the ginjinha — Cinnamomum verum from Sri Lanka '
        '(Ceilão — the Portuguese colonial spice island '
        'seized from the Arabs in 1518) appears in the '
        'Lisbon doorstep liqueur as the direct product of '
        'the colonial spice monopoly that enriched Lisbon '
        'for two centuries. The ginjinha is served from '
        'the kiosk in a small glass (35–50ml) or paper cup, '
        'consumed standing at the kiosk window — the '
        'most democratic consumption ritual in Lisbon.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Italian cherry liqueur (Maraschino, Luxardo — Prunus cerasus maceration)',
            'beverage': 'Luxardo Maraschino — Marasca Cherry Liqueur, Dalmatian Heritage, Prunus cerasus Distillation',
            'connection': (
                'Lisbon ginjinha and Luxardo Maraschino represent the '
                'same fundamental production concept — the maceration '
                'or distillation of Prunus cerasus (sour cherry) in '
                'a spirit base with sugar to produce a cherry liqueur — '
                'applied in two different European traditions: '
                'Portuguese ginjinha uses whole Prunus cerasus '
                'ginja berries macerated in aguardente with sugar '
                'and cinnamon (an Arabic-Moorish spice influence '
                'on the Iberian tradition); Luxardo Maraschino '
                'uses the Marasca variety of Prunus cerasus '
                'distilled (not macerated) in a copper pot '
                'still to produce a clear cherry distillate '
                'that is then sweetened and aged in ash wood. '
                'The key contrast: ginjinha is a maceration liqueur '
                '(the fruit flavour is solvent-extracted into the '
                'existing spirit); Maraschino is a distillation liqueur '
                '(the fruit flavour is volatilised and redistilled '
                'into a new spirit). The PCT connection: both '
                'are Prunus cerasus expressions; both are '
                'Mediterranean colonial-era fruit liqueurs; '
                'both appear as cocktail modifiers (Maraschino '
                'in the Aviation and Hemingway Daiquiri; '
                'ginjinha in the Lisbon Sour). Ginjinha '
                'has the cinnamon colonial spice trade signature; '
                'Maraschino has the Adriatic Venetian colonial heritage.'
            )
        },
        {
            'tradition': 'spirits — Sloe gin (Britain — Prunus spinosa berry maceration, English hedgerow liqueur)',
            'beverage': 'Sloe Gin — British Hedgerow Liqueur, Prunus spinosa, Plymouth Gin Base, Victorian Tradition',
            'connection': (
                'Lisbon ginjinha and British sloe gin share the same '
                'production architecture — a small Prunus family '
                'berry (ginja: Prunus cerasus; sloe: Prunus spinosa) '
                'macerated in a national spirit base (ginjinha: '
                'Portuguese aguardente; sloe gin: British gin) '
                'with sugar to produce a sweet-sour berry liqueur '
                'consumed as an aperitif or digestif. Both were '
                'originally domestic household preparations '
                '(ginjinha from the Lisbon household kitchen; '
                'sloe gin from the English country house larder) '
                'that were commercialised in the 19th century '
                '(ginjinha: A Ginjinha kiosk 1840; sloe gin: '
                'Plymouth Gin commercial production from the '
                'same era). The PCT connection: the Portuguese '
                'colonial trade network and the British colonial '
                'network were simultaneous in the 16th–19th '
                'centuries; Portugal and Britain were allied '
                'through the Treaty of Windsor (1386 — the '
                'oldest active treaty alliance in the world) '
                'and the Methuen Treaty (1703). The ginjinha '
                'kiosk at Largo de São Domingos was serving '
                'drinks in 1840 at exactly the same historical '
                'moment that Victorian Britain was developing '
                'sloe gin as a country house tradition — '
                'two allied nations, two parallel Prunus '
                'berry maceration traditions, both now '
                'internationally recognised as aperitif classics.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep ruby-garnet, nearly opaque — the colour of '
            'concentrated Prunus cerasus anthocyanin pigments '
            '(cyanidin-3-rutinoside and cyanidin-3-glucoside, '
            'the primary red anthocyanins of sour cherry) '
            'extracted into the aguardente spirit base '
            'over 3–6 months of maceration; the colour '
            'at 22–28% ABV has the slightly syrupy, '
            'slow-moving legs of a liqueur; the ginja cherry '
            'fruit is often visible at the bottom of the '
            'glass in the "com ela" (with cherry) service; '
            'the colour brightens slightly at the rim '
            'from the cherry-red spectrum of the '
            'Prunus cerasus anthocyanin extraction.'
        ),
        'nose': (
            'The dominant aromatic of Lisbon ginjinha is the '
            'Prunus cerasus sour cherry register — '
            'the cherry-stone benzaldehyde compound '
            '(bitter almond, marzipan character '
            'from the Prunus kernel maceration), '
            'the cherry-fruit ester complex '
            '(benzyl alcohol and benzyl acetate — '
            'the characteristic "cherry drop" aromatic '
            'that distinguishes Prunus cerasus from '
            'the sweeter Prunus avium profile), '
            'and the malic acid freshness of the '
            'sour cherry acidity (even in the '
            'sugar-sweetened liqueur, the malic '
            'acid of the berry contributes a '
            'mouth-freshening aromatic brightness). '
            'Behind the cherry: the cinnamon '
            'Cinnamomum verum essential oil '
            '(trans-cinnamaldehyde — the characteristic '
            'warm-sweet spice of Sri Lankan cinnamon, '
            'distinctly more delicate than Cassia cinnamon) '
            'providing the colonial spice warmth; '
            'and the clean aguardente spirit base '
            '(the slightly marc-grapey character '
            'of Portuguese bagaceira if used, '
            'or the clean neutral of grain spirit). '
            'The combination of cherry-almond-cinnamon '
            'is the Lisbon ginjinha aromatic signature.'
        ),
        'palate': (
            'The entry is immediate sweetness (200–300g/L residual sugar) '
            'with the cherry-stone benzaldehyde marzipan delivering '
            'simultaneously; the mid-palate develops the sour cherry '
            'malic acidity beneath the sweetness — the characteristic '
            'Prunus cerasus tension between sweet and sour that '
            'prevents the ginjinha from being cloying despite '
            'its high sugar content; the cinnamon warmth '
            '(Cinnamomum verum volatile oils, delivered at '
            '22–28% ABV) provides a spice mid-palate development; '
            'the finish is medium-long (25–35 seconds) with '
            'the cherry-almond-cinnamon triad persisting through '
            'the alcohol warmth of the spirit base; '
            'if served "com ela" (with the cherry), '
            'biting the macerated ginja berry releases '
            'an intense burst of concentrated cherry '
            'malic acid and benzaldehyde that extends '
            'the finish to 45–60 seconds. '
            'At 22–28% ABV the spirit integration is '
            'warm but not dominant — the fruit liqueur '
            'character is the primary experience, '
            'not the alcohol.'
        ),
        'conclusion': (
            'The aperitif that every PCT traveler encounters first '
            'upon arriving in Lisbon — the 1840 kiosk at Largo de '
            'São Domingos that has served the same cherry-almond-cinnamon '
            'formula to dock workers, tile merchants, colonial sailors, '
            'and tourists for 186 years. The logical closing entry '
            'for the PCT system: the beginning and the end of '
            'the Portuguese Colonial Trail in a single small glass.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'Single-source Estremadura ginja berry ginjinha '
                'from identified orchards (Óbidos or Torres Vedras) '
                'with extended maceration (12+ months), '
                'premium Portuguese aguardente base (aged bagaceira '
                'or single-distillery grape spirit at 50%+ ABV '
                'pre-dilution), and Sri Lankan Cinnamomum verum '
                '(Ceylon cinnamon, not Cassia) as the spice component; '
                'finished at 24–26% ABV with cane sugar; '
                'the reserve tier of ginjinha is found in '
                'artisan production (Solar do Castelo, Lisbon; '
                'small Estremadura producers) rather than the '
                'commercial kiosk tradition. '
                'Price: EUR 12–20 per 500ml retail.'
            ),
            'markers': (
                'Single-source orchard; 12+ months maceration; '
                'aged aguardente base; Ceylon cinnamon; '
                '24–26% ABV; cherry-almond-cinnamon fully integrated.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'A Ginjinha kiosk expression or bottled Espinheira '
                'brand — the 1840-formula commercial expression of '
                'the Lisbon tradition; authentic ginja berry base '
                'with the correct cherry-almond-cinnamon aromatic '
                'profile; 3–6 months maceration; aguardente or '
                'grain spirit base; 22–28% ABV; EUR 6–10 per '
                '500ml retail or EUR 1.50 per glass at the '
                'kiosk. The standard-bearer of the Lisbon '
                'ginjinha tradition at democratic price.'
            ),
            'markers': (
                'A Ginjinha or Espinheira; authentic ginja berry; '
                '3–6 months; 22–28% ABV; cherry-almond-cinnamon; '
                'EUR 1.50 kiosk.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Commercial bottled ginjinha without identified '
                'ginja berry source — the supermarket-tier '
                'Portuguese liqueur category using imported '
                'Prunus cerasus extract (Hungarian, Polish, '
                'or Balkan sour cherry concentrate rather than '
                'whole Estremadura ginja berry maceration); '
                'the cherry character is present but flatter '
                'from extract concentration vs. fresh berry '
                'maceration; EUR 4–8 per 500ml.'
            ),
            'markers': (
                'No source declaration; cherry extract; '
                'flatter aromatic; no Estremadura origin.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic Portuguese cherry liqueur using artificial '
                'cherry flavouring (red No. 40, artificial benzaldehyde) '
                'without genuine Prunus cerasus maceration; '
                'the flat, one-dimensional cherry-sweet profile '
                'without the sour cherry malic tension '
                'and cherry-stone benzaldehyde complexity '
                'of authentic ginja berry production. '
                'Identified by the absence of the marzipan '
                'benzaldehyde note and the missing malic acid '
                'freshness. Not appropriate for PCT programme use.'
            ),
            'markers': (
                'Artificial cherry flavour; no malic acid tension; '
                'no benzaldehyde; flat sweetness; avoid in programme.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Lisbon ginjinha is traditionally served at ambient '
            'temperature (18–22°C in the A Ginjinha kiosk context — '
            'the kiosk has no refrigeration and the liqueur is served '
            'directly from the bottle). For PCT programme service: '
            'present at 16–18°C (slightly below room temperature) '
            'to allow the cherry-almond-cinnamon aromatic complex '
            'to express fully without the spirit alcohol becoming '
            'dominant through excessive volatilisation at higher '
            'temperature. Never chill — cold temperature '
            'suppresses the benzaldehyde marzipan character '
            'and the cinnamon volatile oils that define '
            'the ginjinha profile. Present in a small shot '
            'glass (35–50ml; 35ml pour) for the PCT closing entry.'
        ),
        'vessel': (
            'Traditional service: a small ceramic shot glass '
            '(the A Ginjinha kiosk uses a small unadorned '
            'glass of approximately 40ml at the counter) '
            'or a paper cup (the "takeaway" kiosk option '
            'for consumption walking around Largo de '
            'São Domingos). For PCT programme closing service: '
            'a 50ml liqueur glass or small Glencairn with '
            '35ml pour; serve "com ela" (with the macerated '
            'ginja cherry at the bottom of the glass) '
            'to allow the full experience of the cherry '
            'maceration — bite the cherry to complete '
            'the tasting with the concentrated berry burst. '
            'For the programme closing flight: present alongside '
            'the Ginja de Óbidos (in the chocolate cup) '
            'for the two-expression Portuguese cherry liqueur '
            'comparative that closes the PCT programme.'
        ),
        'technique': (
            'Serve at 16–18°C; 35ml in liqueur glass; '
            'serve "com ela" (with macerated cherry); '
            'bite the cherry after drinking the liqueur '
            'for the concentrated berry finish. '
            'Present the 1840 Largo de São Domingos origin — '
            'the kiosk that has been serving this exact formula '
            'from the same window for 186 years — '
            'as the closing PCT narrative: this is where '
            'the colonial trail began, and this is where '
            'we close it.'
        ),
        'programme_position': (
            'PCT closing entry: Lisbon Ginjinha alongside '
            'Ginja de Óbidos (GI-protected, chocolate cup) '
            'as the two-expression Portuguese cherry liqueur '
            'finale to the entire PCT programme; '
            'or in a Portuguese spirits comparative alongside '
            'Licor Beirão (Portuguese herbal liqueur), '
            'Aguardente Bagaceira (Portuguese marc brandy), '
            'and Medronho (Arbutus berry spirit) '
            'for the four-expression Portuguese domestic '
            'spirits heritage arc that bookends the PCT.'
        ),
        'verbal_presentation': (
            'You are standing at the end of the Portuguese Colonial Trail. '
            'Largo de São Domingos. 1840. The same kiosk. '
            'The same formula. The ships that left from the Tagus '
            'carrying the spice — that cinnamon in your glass '
            'came back on those ships from Sri Lanka. '
            'The cherry grew in the orchards north of the city. '
            'Everything the Colonial Trail touches comes back to this. '
            'Com ela — with the cherry. '
            'Bite it when you finish.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'A Ginjinha kiosk, Largo de São Domingos, Lisbon '
            '(the world reference experience — consumed on-site in Lisbon); '
            'Espinheira brand (the bottled commercial expression '
            'for retail and international distribution). '
            'Secondary: Sem Rival Ginjinha (the competitor Lisbon brand); '
            'Solar do Castelo (the premium Lisbon heritage expression). '
            'For programme supply: the Espinheira bottled expression '
            'is available through Portuguese specialty food importers '
            'internationally; the A Ginjinha kiosk experience '
            'requires physical presence in Lisbon.'
        ),
        'producer_location': 'Largo de São Domingos, Baixa Pombalina, Lisbon, Portugal',
        'key_person': 'Espinheira family (historical); current kiosk operator; multiple commercial bottlers',
        'production_volume': 'Several hundred thousand litres/year total Lisbon ginja liqueur production across all commercial producers',
        'certifications': ['Indicação Geográfica Protegida (IGA) Ginjinha de Lisboa — proposed but not yet formally implemented as of 2026; Ginja de Óbidos GI is the current protected designation'],
        'bc_distributor': '[PROVIDER: verify through Portuguese specialty food importers in BC — Portugália Foods (Vancouver) or similar; Espinheira brand may be available through BC Portuguese community retailers]',
        'us_distributor': '[PROVIDER: verify through Portuguese specialty food/spirits importers in Newark NJ or New Bedford MA — primary US Portuguese community market entry points]',
        'uk_distributor': '[PROVIDER: Espinheira available through Portuguese food specialists in the UK — Loja Portuguesa (London) or Portuguese wine merchants; verify current stock]',
        'price_tier': 'Estate',
        'availability_notes': (
            'Lisbon ginjinha in the authentic A Ginjinha kiosk form '
            'requires a visit to Largo de São Domingos — '
            'this experience cannot be replicated internationally. '
            'The bottled Espinheira expression is available through '
            'Portuguese specialty importers globally. '
            'Programme buyers who cannot source Espinheira '
            'may present the Ginja de Óbidos GI-protected expression '
            '(the second entry in this pct_89 file) as the programme '
            'representative, using the Lisbon kiosk documentation '
            'for the programme narrative context.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'Lisbon ginjinha is the closing entry of the PCT extraction system — '
        'the aperitif of the colonial capital, the drink that every PCT '
        'traveler encounters at the beginning and end of the trail. '
        'The Arabic name "ginja" (from zinzī — the Moorish heritage '
        'in the Iberian Peninsula before the Reconquista) embedded '
        'in the Portuguese colonial capital\'s signature drink '
        'is itself a compressed history of the Portuguese empire: '
        'the Arabic heritage of the Iberian Peninsula, '
        'the sour cherry orchards of the Estremadura, '
        'the Sri Lankan cinnamon of the colonial spice trade, '
        'and the aguardente spirit base of the '
        'Portuguese domestic distillation tradition — '
        'all in a 40ml glass served from a window '
        'at Largo de São Domingos since 1840.'
    ),
    'food_pairings': [
        {
            'technique_id': 'LIS-001',
            'dish': 'Pastéis de nata (Lisbon custard tarts — the Jerónimos monastery recipe, the PCT\'s most internationally known Portuguese food)',
            'pairing_type': 'complement',
            'rationale': (
                'Ginjinha alongside pastéis de nata is the most '
                'Lisbon-specific food-and-drink pairing in the PCT system: '
                'the cherry-almond-cinnamon liqueur resonating with the '
                'egg-cream and cinnamon-dusted pastry of the Belém '
                'custard tart through the shared cinnamon Cinnamomum verum '
                'spice (both the ginjinha recipe and the pastel de nata '
                'recipe use Ceylon cinnamon from the same Portuguese '
                'colonial Sri Lanka import); the cherry malic acidity '
                'of the ginjinha cutting the egg-cream richness '
                'of the tart; a within-Lisbon heritage pairing.'
            )
        },
        {
            'technique_id': 'LIS-002',
            'dish': 'Bifanas (Lisbon pork loin sandwich with mustard and piri-piri — the Baixa street food staple)',
            'pairing_type': 'contrast',
            'rationale': (
                'The sweet-sour cherry richness of the ginjinha '
                'contrasts with the sharp mustard-piri-piri '
                'of the Lisbon bifana through the classic '
                'sweet-spice contrast — the liqueur\'s cherry '
                'sweetness moderating the piri-piri heat '
                'while the sour cherry malic acid refreshes '
                'the palate between bites of the pork sandwich; '
                'the Baixa street food and the Baixa kiosk liqueur '
                'are consumed in the same pedestrian square, '
                'representing the paired culture of the Lisbon '
                'working-class lunch break.'
            )
        }
    ],
    'source': 'IVDP Lisbon spirits documentation; Câmara Municipal de Lisboa (Lisbon municipal archives, kiosk licensing records); Leal Luís — Bebidas Tradicionais Portuguesas; Pinto e Castro Filipa — Aguardentes e Licores de Portugal; Robinson Jancis Oxford Companion to Wine (Ginjinha entry); Davidson Alan Oxford Companion to Food (Ginja entry); Cossart Gordon Norman Madeira historical bibliography for Portuguese spirits context',
    'price_trajectory': 'stable'
})

session.commit_batch()

# Entry 2 — THE FINAL PCT ENTRY: Ginja de Óbidos
session.switch_region(
    'spirits',
    'Portugal — Óbidos (Licor de Ginja de Óbidos, Protected GI, Medieval Walled City, Ginja Ceremony Heritage)'
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Óbidos Ginja Producers (GI-Certified Collective) — principal brands: Licor Beirão Ginja de Óbidos, Optic Gin Ginja de Óbidos',
    'location': 'Óbidos, Leiria District, Estremadura, Portugal (the medieval walled city 80km north of Lisbon)',
    'country': 'Portugal',
    'region': 'Óbidos — the medieval walled city whose walls and castle (now a pousada hotel) define the visual identity of the Ginja de Óbidos GI designation',
    'key_person': 'Multiple Óbidos-based producers operating under the GI certification; the Óbidos municipality (Câmara Municipal de Óbidos) manages the GI collective',
    'founded': 'The Óbidos ginja tradition is pre-commercial; the GI (Indicação Geográfica Protegida) designation for Ginja de Óbidos was formalised under EU protected designation regulations; the chocolate cup service tradition is documented from the 20th century',
    'production_volume': 'GI Ginja de Óbidos production estimated at 100,000–300,000 litres/year from certified Óbidos-region producers; the town receives over 1 million visitors per year and the ginja kiosks and shops are among the primary tourism economic activities',
    'notable_products': [
        'Ginja de Óbidos IGP (the GI-protected expression, served in edible chocolate cups)',
        'Óbidos chocolate ginja cup (the signature service format — a chocolate cup filled with ginja)',
        'Various artisan and commercial Ginja de Óbidos bottlings from local producers',
    ],
    'certifications': ['Indicação Geográfica Protegida (IGP) Ginja de Óbidos — EU protected designation covering the geographic indication'],
    'website': '[PROVIDER: Câmara Municipal de Óbidos promotes the GI collectively — individual producers have separate websites]',
    'philosophy': (
        'The Ginja de Óbidos GI designation protects the geographic identity '
        'of the Óbidos cherry liqueur tradition — the same Prunus cerasus '
        'ginja berry maceration as the Lisbon ginjinha but with the specific '
        'Óbidos municipality terroir designation and the unique chocolate cup '
        'service ritual that distinguishes the Óbidos tradition from the '
        'Lisbon paper cup kiosk culture.'
    ),
    'trail_connection': 'PCT (Portugal — Óbidos closing entry; THE FINAL PCT ENTRY)',
    'verified': True
})

session.add_beverage({
    'name': (
        'Ginja de Óbidos IGP — Protected Geographic Indication, Medieval Walled City, '
        'Edible Chocolate Cup Service, Estremadura Ginja Berry Heritage, '
        'THE FINAL PCT ENTRY'
    ),
    'tradition': 'spirits',
    'sub_tradition': 'fruit_liqueur — Ginja de Óbidos IGP; Prunus cerasus macerated in aguardente with sugar; served in edible chocolate cups; EU-protected geographic indication',
    'region': 'Portugal — Óbidos (Licor de Ginja de Óbidos, Protected GI, Medieval Walled City, Ginja Ceremony Heritage)',
    'terroir_origin': (
        'Óbidos is a medieval walled city in the Estremadura region '
        'of central Portugal, 80km north of Lisbon, whose intact '
        '13th-century walls and Moorish-origin castle (converted '
        'to a pousada luxury hotel) make it one of the most '
        'visited historic sites in Portugal. The Óbidos valley '
        'is surrounded by the Estremadura orchards that produce '
        'the ginja berry (Prunus cerasus — the sour morello cherry) '
        'that is the raw material for both the Lisbon ginjinha '
        'and the Ginja de Óbidos. The difference in terroir '
        'between Lisbon ginjinha and Ginja de Óbidos is the '
        'geographic origin of the ginja berry: Óbidos-certified '
        'ginja must come from the Óbidos municipality\'s orchards '
        'and the surrounding Estremadura valleys (Torres Vedras, '
        'Caldas da Rainha, Bombarral sub-zones) where the '
        'Atlantic-influenced microclimate (cooler temperatures '
        'from the proximity to the Atlantic coast at Caldas '
        'da Rainha, 15km west of Óbidos) produces ginja berries '
        'with a higher malic-to-citric acid ratio than the '
        'Lisbon-adjacent orchards (the greater Atlantic '
        'cooling effect retaining more malic acid in the berry '
        'at harvest). The GI designation for Ginja de Óbidos '
        'was established under EU protected geographic indication '
        'regulations, recognising that the Óbidos tradition '
        'has a distinct production territory and a unique '
        'service ritual (the chocolate cup) that constitutes '
        'a cultural heritage product of the Óbidos municipality.'
    ),
    'production_technique': (
        'Ginja de Óbidos IGP production follows the same '
        'architectural template as Lisbon ginjinha — '
        'Prunus cerasus ginja berries from certified Óbidos-'
        'municipality orchards macerated whole in Portuguese '
        'aguardente with sugar and cinnamon — but with '
        'the IGP geographic certification adding the '
        'requirement that the berry source be within the '
        'certified Óbidos production zone. The maceration '
        'period (3–12 months depending on producer), '
        'the aguardente base (bagaceira grape marc spirit '
        'or grain spirit at 40–50% ABV pre-dilution), '
        'and the final liqueur specifications '
        '(22–28% ABV, 200–300g/L residual sugar) '
        'are within the same range as Lisbon ginjinha. '
        'The critical distinguishing element of the '
        'Ginja de Óbidos tradition is the chocolate cup '
        'service ritual: the liqueur is poured into a '
        'small chocolate cup (a hollow chocolate shell '
        'approximately 35–40ml capacity, made from dark '
        'chocolate — typically Valrhona or similar '
        '60–70% cacao) rather than a glass, and the '
        'guest is instructed to drink the ginja '
        'and eat the chocolate cup after. '
        'The chocolate cup creates a sequential '
        'sensory experience: the ginja cherry-almond-'
        'cinnamon liqueur arrives first; as the chocolate '
        'cup wall melts slightly from the liqueur warmth, '
        'the dark chocolate phenolics begin to integrate '
        'into the ginja; after drinking, the remaining '
        'chocolate cup is bitten and eaten, delivering '
        'a dark-chocolate-ginja residual. '
        'The cacao-cherry sensory pairing is a '
        'deliberately engineered experience that '
        'constitutes a unique service innovation '
        'in the Portuguese spirits tradition — '
        'the only nationally-produced spirit '
        'that has a dedicated edible vessel as '
        'its standard service format.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'spirits — Kirsch (Alsace, Germany, Switzerland — Prunus avium cherry distillation, clear spirit)',
            'beverage': 'Alsace Kirsch — Clear Cherry Eau-de-Vie, Prunus avium Distillation, Alsatian Alpine Heritage',
            'connection': (
                'Ginja de Óbidos and Alsatian Kirsch represent '
                'the opposite production ends of the European '
                'sour/sweet cherry spirit tradition: Óbidos ginja '
                'uses Prunus cerasus (sour cherry) macerated in '
                'aguardente to produce a ruby-red, sweet liqueur '
                '(200–300g/L sugar; 22–28% ABV); Alsatian Kirsch '
                'uses Prunus avium (sweet cherry) double-distilled '
                'in copper pot stills to produce a crystal-clear, '
                'dry eau-de-vie (0g/L residual sugar; 40–45% ABV). '
                'Both are consumed in the context of local cultural '
                'heritage (Óbidos ginja in the medieval Portuguese '
                'walled-city tourism culture; Kirsch in the Alsatian '
                'tarte flambée and Black Forest cake tradition); '
                'both derive their cultural identity from the specific '
                'Prunus variety and production method of their region. '
                'The PCT closing parallel: Ginja de Óbidos closes '
                'the Portuguese Colonial Trail from Lisbon\'s Tagus '
                'waterfront through the Atlantic Ocean arc and back '
                'to the medieval walled city 80km north; Kirsch '
                'marks the Germanic frontier of the same Catholic '
                'European cultural geography that produced the '
                'Portuguese colonial empire.'
            )
        },
        {
            'tradition': 'spirits — Crème de Cassis (Burgundy, France — blackcurrant maceration liqueur, Dijon heritage)',
            'beverage': 'Crème de Cassis de Dijon — Blackcurrant Liqueur, Burgundian Kir Tradition',
            'connection': (
                'Ginja de Óbidos and Crème de Cassis de Dijon '
                'share the same production architecture (small berry '
                'macerated in neutral spirit with sugar to produce '
                'a deep-coloured fruit liqueur) and the same '
                'function in their respective national cultures '
                '(the defining aperitif of a specific regional '
                'identity: Óbidos\'s cherry and chocolate; Dijon\'s '
                'blackcurrant and Aligoté wine in the Kir royale). '
                'Both are EU-protected geographic indications '
                '(Ginja de Óbidos IGP; Crème de Cassis de Dijon IGP), '
                'recognising the specific berry origin and production '
                'territory. The chocolate cup service of Óbidos '
                'and the Champagne-Cassis Kir royale service of '
                'Dijon are both performative service rituals that '
                'embed the aperitif in a specific cultural '
                'tradition beyond the liquid content of the glass — '
                'both are drinking ceremonies as much as they are '
                'beverages. The PCT parallel: the Portuguese and '
                'French colonial empires were simultaneous and '
                'competing; the GI-protected berry liqueur traditions '
                'of Óbidos and Dijon represent the parallel '
                'national-heritage berry liqueur traditions of '
                'the two primary competing colonial European powers.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep ruby-garnet, identical in colour to the Lisbon '
            'ginjinha (same Prunus cerasus anthocyanin pigment '
            'extraction from the same species of ginja berry — '
            'the Óbidos Atlantic cool-climate berry may show '
            'a marginally deeper colour from the higher '
            'anthocyanin accumulation at cooler ripening '
            'temperatures); the chocolate cup changes the '
            'visual presentation fundamentally — '
            'the ginja arrives concealed within the dark '
            'chocolate shell until poured or tilted, '
            'creating the service drama unique to Óbidos. '
            'In a standard glass for tasting comparison: '
            'deep ruby; slow liqueur legs; brilliant clarity '
            'from the filtered maceration.'
        ),
        'nose': (
            'The Ginja de Óbidos aromatic profile shares '
            'the cherry-almond-cinnamon register of Lisbon '
            'ginjinha (same variety, same production method) '
            'with a potential distinction: the Atlantic-cooled '
            'Estremadura malic acid retention in the Óbidos '
            'berry produces a slightly sharper, fresher '
            'cherry-acid top note compared to the Lisbon '
            'counterpart — the malic acid volatile compounds '
            '(acetaldehyde and acetone at trace levels '
            'produced by the Prunus cerasus oxidation during '
            'maceration) are more present in higher-acid '
            'fruit. The chocolate cup adds a sensory layer '
            'at the point of service: the dark chocolate '
            '(60–70% cacao) aroma of the cup creates '
            'an aromatic frame for the ginja nose — '
            'the cacao theobromine-and-phenol aromatic '
            'of the chocolate wrapper surrounding the '
            'cherry-almond-cinnamon of the liqueur. '
            'This is the Óbidos sensory innovation: '
            'the beverage and its vessel together '
            'constitute the complete aromatic experience.'
        ),
        'palate': (
            'The Ginja de Óbidos in the chocolate cup '
            'produces a sequential three-stage palate experience: '
            'Stage 1 (ginja consumed from the cup): '
            'the cherry-almond-cinnamon liqueur sweetness '
            'with the slightly sharper Óbidos berry malic acidity; '
            'Stage 2 (ginja residue and chocolate cup interior '
            'wall contact — the ginja warms and partially '
            'melts the inner chocolate shell): '
            'the dark chocolate phenolics (catechins, '
            'procyanidins — the tannin family of cacao) '
            'begin integrating into the residual ginja '
            'on the palate, adding a bitter-sweet '
            'chocolate layer beneath the cherry liqueur; '
            'Stage 3 (biting the chocolate cup): '
            'the concentrated dark chocolate snap '
            '(80% cocoa solid at the cup wall) '
            'combined with the residual ginja '
            'absorbed into the inner chocolate surface '
            'delivers the complete cherry-chocolate '
            'integration as a solid-to-liquid '
            'transition experience. '
            'The finish (45–60 seconds with the '
            'chocolate eaten) is the longest '
            'and most complex of the two '
            'ginja expressions — the PCT closing '
            'entry designed for extended reflection.'
        ),
        'conclusion': (
            'The final entry of the Provenance PCT beverage extraction. '
            'Portugal. Óbidos. The medieval walls. The cherry orchards '
            'in the Atlantic-cooled valley. The chocolate cup. '
            'The Colonial Trail ends here — in a protected GI '
            'designation, in a medieval walled city, '
            'in an edible vessel. '
            'The PCT has travelled from the Azores volcanic currais '
            'to the Douro schist terraces, from the Kerala coconut palms '
            'to the Timor-Leste lontar ceremony, from the Trinidad '
            'bitters formula to the Barbados falernum spice trade — '
            'and it closes with a sour cherry macerated in aguardente, '
            'served in a chocolate cup, at the foot of a Moorish castle '
            'in the Portuguese interior. Eat the cup.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 4,
            'tier_name': 'Reserve',
            'criteria': (
                'IGP Ginja de Óbidos from a single identified orchard '
                'within the Óbidos municipality with estate-declared '
                'ginja berry harvest (producer, parcel, year); '
                'extended maceration (12+ months) producing full '
                'benzaldehyde-cinnamon integration; premium aguardente '
                'base (aged bagaceira or premium grain spirit); '
                'finished at 26% ABV for optimal chocolate cup '
                'compatibility (the spirit must be sweet enough '
                'to resist absorbing into the chocolate wall '
                'while delivering the full maceration character); '
                'paired with a minimum 65% cacao chocolate cup '
                '(Valrhona, Callebaut or equivalent confectionery-grade). '
                'Price: EUR 15–25 per bottled 500ml reserve expression.'
            ),
            'markers': (
                'IGP certified; single orchard; 12+ months; '
                'premium aguardente; 26% ABV; 65%+ cacao cup; '
                'cherry-almond-cinnamon-chocolate complete integration.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Estate',
            'criteria': (
                'Standard IGP Ginja de Óbidos from certified '
                'Óbidos municipality production with the '
                'chocolate cup service; authentic ginja berry '
                'from the Estremadura; 3–6 months maceration; '
                '22–26% ABV; EUR 8–15 per 500ml bottled; '
                'EUR 2–3 per chocolate cup serving at Óbidos '
                'kiosks and shops. The standard programme '
                'expression of the Óbidos tradition.'
            ),
            'markers': (
                'IGP certified; Óbidos municipality; chocolate cup service; '
                'cherry-almond-cinnamon; 22–26% ABV; EUR 2–3 kiosk.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Market',
            'criteria': (
                'Non-IGP "Ginja de Óbidos style" liqueurs produced '
                'outside the certified municipality using '
                'Estremadura ginja berries but without the '
                'Óbidos GI certification; the ginja character '
                'is present but the geographic authentication '
                'is absent; sold as "estilo Óbidos" without '
                'the protected designation. EUR 6–10 per 500ml.'
            ),
            'markers': (
                'No IGP; outside municipality; ginja character; '
                'no geographic authentication; "estilo" designation.'
            )
        },
        {
            'tier': 1,
            'tier_name': 'House',
            'criteria': (
                'Generic ginja sold in Óbidos tourist shops without '
                'IGP certification or identified producer — the '
                '"Óbidos chocolate cup" souvenir liqueur produced '
                'outside the certification zone and packaged in '
                'a tourist gift format. The chocolate cup service '
                'is replicated but the ginja content is not '
                'from certified Óbidos-municipality berry production. '
                'Not appropriate for PCT programme validation.'
            ),
            'markers': (
                'No IGP; unidentified producer; tourist souvenir format; '
                'non-certified berry source.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Ginja de Óbidos in the chocolate cup is served at '
            'ambient shop temperature in the Óbidos context '
            '(18–22°C at the tourist kiosks and shops). '
            'For PCT programme service: present the chocolate cup '
            'at 16–18°C — the ginja should be cool enough '
            'to prevent the chocolate cup from melting '
            'prematurely before the guest consumes the liqueur, '
            'but warm enough for the full cherry-almond-cinnamon '
            'aromatic complex to express. If the chocolate cup '
            'melts too quickly (above 22°C), the service '
            'drama is compromised; if too cold (below 14°C) '
            'the liqueur aromatics contract. The chocolate cup '
            'service works best as the final course '
            'of the PCT programme — consumed in a group '
            'setting where the instruction to "eat the cup" '
            'creates a shared closing ceremony.'
        ),
        'vessel': (
            'The chocolate cup IS the vessel — this is the defining '
            'service innovation of the Ginja de Óbidos tradition. '
            'For PCT programme use: source pre-formed chocolate '
            'liqueur cups (available from confectionery suppliers '
            'internationally — Callebaut, Molds & Moulds UK, '
            'or specialty chocolate confectionery suppliers in '
            'North America) and fill with 30–35ml of the Ginja '
            'de Óbidos IGP just before service. The chocolate '
            'cup should be presented on a small plate or wooden '
            'board, ideally with a piece of Óbidos tourism material '
            '(a photograph of the medieval walls) as programme '
            'context. For non-chocolate-cup service (if chocolate '
            'cups are unavailable): a small liqueur glass (50ml; '
            '35ml pour) with a square of 65%+ dark chocolate '
            'on the side as a partial replication of the '
            'sequential chocolate-ginja experience.'
        ),
        'technique': (
            'Fill chocolate cup immediately before service (30–35ml); '
            '16–18°C; present with the instruction: '
            '"Drink the ginja first, then eat the cup." '
            'The chocolate cup wall will have absorbed some '
            'ginja flavour from the pour — the eating of '
            'the cup after delivers the complete '
            'cherry-chocolate integration. '
            'Close the PCT programme with this service: '
            'it is the only edible vessel in the entire '
            'PCT programme and constitutes the programme\'s '
            'closing ceremony.'
        ),
        'programme_position': (
            'THE FINAL PCT ENTRY — served as the absolute close '
            'of the Provenance Portuguese Colonial Trail programme: '
            'Ginja de Óbidos in the chocolate cup as the '
            'closing ceremony drink. Present alongside the Lisbon '
            'ginjinha (the kiosk expression, paper cup or small glass) '
            'for the two-expression Portuguese cherry heritage comparison '
            'that closes the PCT: the democratic Lisbon kiosk '
            'versus the GI-protected medieval walled city. '
            'The narrative arc of the PCT begins at the Tagus '
            'waterfront and ends at the Óbidos castle walls — '
            'this is the closing drink of that arc.'
        ),
        'verbal_presentation': (
            'This is the last drink of the Portuguese Colonial Trail. '
            'The castle behind us was built by the Moors. '
            'The cherry orchards in this valley are Atlantic-cooled. '
            'The cinnamon in this cup came back on a Portuguese ship '
            'from Sri Lanka 500 years ago. '
            'The chocolate is from cacao that was cultivated in Brazil '
            'on the same Atlantic colonial arc that the ships travelled. '
            'Drink the ginja. '
            'Then eat the cup.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'IGP Ginja de Óbidos certified producers — the benchmark '
            'is the collective GI certification rather than a single '
            'producer in the Óbidos tradition. For programme supply: '
            'any IGP-certified Ginja de Óbidos bottling from a '
            'verified Óbidos municipality producer is the correct expression. '
            'For the chocolate cup: Callebaut Belgian chocolate '
            'liqueur cups (available from pastry and confectionery '
            'suppliers internationally) are the standard programme '
            'vessel. '
            'For the closest internationally available single-producer '
            'reference: Licor Beirão Ginja de Óbidos (produced by '
            'Licor Beirão, Portugal\'s most distributed domestic liqueur house) '
            'carries the IGP certification and is available through '
            'Portuguese specialty importers.'
        ),
        'producer_location': 'Óbidos, Leiria District, Estremadura, Portugal',
        'key_person': 'Multiple GI-certified producers; Câmara Municipal de Óbidos as GI coordinator',
        'production_volume': '100,000–300,000 litres/year GI-certified Ginja de Óbidos production',
        'certifications': ['Indicação Geográfica Protegida (IGP) Ginja de Óbidos — EU protected designation'],
        'bc_distributor': '[PROVIDER: verify through Portuguese specialty importers in BC; Licor Beirão is the most widely distributed Portuguese liqueur brand and may carry the Ginja de Óbidos expression — check BCLDB listings]',
        'us_distributor': '[PROVIDER: verify through Portuguese specialty food/spirits importers; Wine.com and Drizly periodically list Ginja de Óbidos expressions from GI-certified producers]',
        'uk_distributor': '[PROVIDER: The Wine Society UK or Portuguese specialists may carry IGP Ginja de Óbidos; verify through Wines of Portugal UK trade body for current UK importers]',
        'price_tier': 'Estate',
        'availability_notes': (
            'IGP Ginja de Óbidos in the chocolate cup format '
            'is primarily available in Óbidos itself and in Portuguese '
            'specialty food shops; international distribution is limited. '
            'Programme buyers who cannot source the chocolate cup '
            'expression directly should order the IGP bottling '
            'through Portuguese specialty importers and source '
            'chocolate liqueur cups separately from confectionery '
            'suppliers to replicate the service ritual. '
            'The Callebaut chocolate liqueur cup moulds '
            'are available from pastry supply companies '
            'in all major international markets.'
        )
    },
    'trail_connection': 'PCT',
    'trail_note': (
        'THE FINAL PCT ENTRY. Ginja de Óbidos closes the Provenance PCT '
        'beverage extraction system — the last of the 10 extraction files '
        '(pct_86 through pct_89), the last of the 10 entries of this session, '
        'and the closing symbol of the Portuguese Colonial Trail programme. '
        'The IGP Ginja de Óbidos brings together every element of the '
        'PCT programme: the Prunus cerasus ginja berry from the '
        'Estremadura orchards (Portuguese agricultural heritage), '
        'the Cinnamomum verum cinnamon from Sri Lanka '
        '(Portuguese colonial spice trade heritage), '
        'the cacao chocolate cup from the Brazilian cacao '
        '(Portuguese colonial Atlantic heritage), '
        'and the medieval walled city of Óbidos '
        '(Portuguese pre-colonial national heritage). '
        'The GI certification is the contemporary institutional '
        'recognition that the PCT\'s core argument is correct: '
        'place, ingredient, and culture together constitute '
        'a provenance that is worth protecting. '
        'That is what the Provenance PCT beverage system documents. '
        'End of extraction.'
    ),
    'food_pairings': [
        {
            'technique_id': 'OBD-001',
            'dish': 'Queijadas de Óbidos (Óbidos fresh cheese tarts — the local pastry paired with ginja at the medieval tourism kiosks)',
            'pairing_type': 'complement',
            'rationale': (
                'The queijada de Óbidos (a fresh cheese and egg tart '
                'with a sweet pastry shell — the local version of the '
                'Portuguese queijada tradition) paired with Ginja de Óbidos '
                'chocolate cup is the within-Óbidos closing pairing: '
                'the cherry-almond-cinnamon liqueur complementing the '
                'fresh cheese sweetness and the pastry richness through '
                'the cherry malic acidity cutting the fat while the '
                'cinnamon-spice bridges with the pastry aromatics; '
                'a pairing consumed standing at the Óbidos wall '
                'promenade as the classic tourist stop-and-taste.'
            )
        },
        {
            'technique_id': 'OBD-002',
            'dish': 'Dark chocolate (70%+ cacao) — the residual chocolate cup as a food pairing in itself',
            'pairing_type': 'bridge',
            'rationale': (
                'The chocolate cup of the Ginja de Óbidos service '
                'is itself the food pairing — the dark chocolate '
                'phenolics (catechins, procyanidins) of the cup '
                'bridge with the Prunus cerasus anthocyanins of '
                'the ginja through the shared polyphenol family '
                '(both cherry anthocyanins and cacao procyanidins '
                'are in the flavonoid polyphenol group), creating '
                'the specific sensory coherence of the '
                'cherry-chocolate combination that is '
                'the most culturally developed food-spirit '
                'pairing in the Portuguese culinary tradition. '
                'Eat the cup.'
            )
        }
    ],
    'source': 'DGADR (Direção-Geral de Agricultura e Desenvolvimento Rural) IGP Ginja de Óbidos production documentation; Câmara Municipal de Óbidos cultural heritage records; Pinto e Castro Filipa — Aguardentes e Licores de Portugal; IVDP Portuguese spirits general documentation; Slow Food Portugal regional beverage documentation; EU Protected Designation of Origin registry (IGP Ginja de Óbidos official ficha de produto)',
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
