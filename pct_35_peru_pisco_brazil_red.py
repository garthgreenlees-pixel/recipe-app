import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Peru — Ica and Arequipa Valleys (Pisco GI, Quebranta and Italia Varieties, Desert Coast Viticulture)',
    output_dir='.',
    starting_entry=1,
    session_number=37,
    running_total=104
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Bodegas y Viñedos Tabernero — Ica Valley',
    'location': 'Chincha Alta, Ica Region, Peru',
    'description': 'Tabernero is one of Peru\'s largest and most diversified wine and pisco producers, operating on 500 hectares of vineyards in the Chincha and Ica valleys on the Peruvian desert coast. Founded 1897 by Italian immigrant Hector Tabernero, the estate produces both Italian-variety (Italia, Moscatel, Albilla) and non-aromatic (Quebranta, Mollar) pisco varieties under the Peruvian GI designation. Tabernero\'s Gran Pisco Italia is consistently one of the most awarded aromatic piscos in international competition, while their Quebranta single-variety is the reference for the earthy, non-aromatic pisco style that forms the base of the classic Pisco Sour. The estate also produces wines including Malbec and Sauvignon Blanc from the desert-irrigated coastal valleys.',
    'founded': '1897',
    'region': 'Ica Valley, Peru',
    'website': 'tabernero.com',
    'verified': True
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Macchu Pisco — The Last Drop Family Distillery',
    'location': 'Ica Valley, Peru',
    'description': 'Small artisan pisco producer founded by Melanie Asher, an American of Peruvian heritage, producing single-variety and multi-variety pisco expressions from Quebranta, Italia, and blended varietals. Macchu Pisco emphasizes the GI distinction between Peruvian pisco (produced in 5 specific coastal regions, distilled from fresh grape wine to proof without water addition) and Chilean pisco (different production rules). The distillery uses traditional copper pot alembic stills in a single distillation that produces pisco at the final serving proof without dilution — the distinguishing feature of Peruvian pisco production that separates it from Cognac and Armagnac standards.',
    'founded': '2003',
    'region': 'Ica Valley, Peru',
    'website': 'macchupisco.com',
    'verified': True
})

session.add_purveyor({
    'name': 'World\'s End Imports — Pisco Specialist (US) / Wines & Spirits of the World (Canada)',
    'type': 'importer',
    'description': 'World\'s End Imports handles premium Peruvian pisco distribution in the US including Macchu Pisco and Caravedo ranges. In Canada, Peruvian pisco is distributed through specialty importers including Authentic Wine & Spirits (BC) and LCBO product submissions. Pisco availability has grown significantly in North America following the Pisco Sour\'s recognition as a signature cocktail in premium cocktail culture since 2010.',
    'markets_served': ['US', 'Canada', 'UK', 'EU'],
    'traditions_carried': ['spirits'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Peruvian Pisco GI Quebranta — Ica Valley Desert Coast, Single Variety Non-Aromatic, Copper Pot Still',
    'category': 'spirits',
    'subcategory': 'pisco',
    'origin': 'Peru',
    'region': 'Ica Valley, Peru',
    'producer': 'Bodegas y Viñedos Tabernero — Ica Valley',
    'alcohol_content': 42.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Ica Valley is Peru\'s most historically significant pisco-producing zone — located in the hyper-arid Atacama Desert coastal zone at approximately 400m elevation above sea level, where the Ica River (fed by Andean glacier and snowmelt) creates an irrigated oasis in one of the driest environments on Earth. Annual rainfall in the Ica Valley averages 2–4mm — essentially zero precipitation — making viticulture entirely dependent on the gravity-fed irrigation channels (canales de riego) built during the Inca Empire and expanded under Spanish colonial administration from the 16th century onward. The Quebranta grape variety cultivated in Ica is a non-aromatic Vitis vinifera variety developed in Peru during the colonial era from a cross between Mission (Listán Negro, brought from Spain) and Mollar — a grape with no direct European parent variety, making it the first New World grape variety developed from colonial hybridization. Quebranta thrives in the desert heat and near-zero humidity of the Ica Valley: it has adapted over 400+ years to minimal water stress, intense UV radiation at low altitude with no cloud cover, and sandy alluvial soils over the Ica Valley floor that produce very low yields of concentrated, low-acid, high-sugar grapes. The resulting must ferments to a dry wine at 12–14% ABV with very high sugar concentration but low acidity — a profile that produces the distinctively full-bodied, earthy, slightly phenolic character of non-aromatic Quebranta pisco.'
    ),
    'production_technique': (
        'Peruvian pisco production is governed by the most restrictive technical standard of any brandy category in the world: the Peruvian GI regulation requires that pisco be distilled exclusively from freshly fermented grape juice (mosto verde — must distilled before fermentation completes) or from completely fermented grape wine (mosto fermentado) in copper pot alembic stills, with no dilution after distillation — the pisco must be brought to the final serving strength (38–48% ABV for most styles) entirely by the distillation cut, with no water addition permitted. This no-dilution requirement fundamentally shapes the character of Peruvian pisco: it is a "true" grape distillate in which the water content of the final bottling comes entirely from the original grape juice water, not from added water. Tabernero\'s Quebranta production follows the "mosto fermentado" method: freshly pressed Quebranta juice ferments to complete dryness over 10–14 days in stainless steel tanks with selected Saccharomyces cerevisiae, producing a dry wine at 12–14% ABV. Single distillation in copper pot stills — the alembic de cobre of the colonial Peruvian tradition — at 42–48% ABV final cut; the distiller controls the cut point to bring the spirit exactly to the target bottling strength, since post-distillation dilution is prohibited. The hearts cut in Peruvian pisco is considerably wider than in Cognac or Armagnac, incorporating more of the heads fraction to preserve the complex ester and fusel alcohol notes that define the pisco\'s grape variety character. No aging required by Peruvian GI regulations; rested in neutral stainless steel for 3 months minimum after distillation before bottling.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Armagnac single vintage (grape-variety distillate, pot still, unaged or minimally aged)',
            'connection': 'Peruvian pisco and young Armagnac share the category of grape-based pot still spirits where the primary character comes from the grape variety itself (Quebranta or Folle Blanche/Ugni Blanc) rather than from wood aging — both are among the world\'s most transparent expressions of how a specific Vitis vinifera variety translates into distillate character when copper pot still and single distillation preserve maximum varietal aromas'
        },
        {
            'tradition': 'Mezcal Espadín (unaged, desert cultivation, terroir transparency)',
            'connection': 'Peruvian pisco and unaged mezcal Espadín both produce transparent, unaged spirits from desert-grown plants that rely on extreme irrigation scarcity and UV radiation to concentrate sugars — both are expressions of how plants under stress in arid environments produce the most concentrated aromatic substrates for distillation'
        },
        {
            'tradition': 'Grappa di Moscato (Italian grape marc distillate, aromatic variety)',
            'connection': 'Peruvian Italia pisco and Grappa di Moscato both derive intense floral-aromatic character (lychee, rose, white flower) from the Muscat-family grape varieties — Muscat of Alexandria (Italia) in Peru\'s Ica Valley and Moscato Bianco in Italy\'s Asti zone — demonstrating how Muscat terpene compounds survive distillation to produce one of the most identifiable aromatic distillate profiles in the world'
        }
    ],
    'sensory_profile': {
        'appearance': 'Water-clear and brilliant; Peruvian GI requires no aging for non-acholado expressions, producing a completely uncolored spirit; slight oiliness from the fusel alcohol content retained through the wide hearts cut',
        'nose': 'Distinctly earthy and herbal for Quebranta variety: dried herbs (sage, thyme), earthy stone fruit (dried apricot, dried peach), slight mineral, light floral undertone — the "non-aromatic" variety profile is subtler and more earthy than the explosive floral of Italia; characteristic dried-fruit-and-herb complexity that serious pisco drinkers identify as distinctly Peruvian',
        'palate': 'Full body from the no-dilution production requirement (all water content from the original grape juice rather than added water), warm and complex, earthy stone fruit mid-palate, grape varietal character unmistakable in the finish, slightly phenolic warmth from the wide heads cut — the Pisco Sour (lime, sugar, egg white, Angostura) is specifically designed around Quebranta\'s earthy character as the base'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commercial Peruvian Pisco (standard grade)',
            'criteria': 'Volume production pisco from Ica or other GI zone, single variety Quebranta or Mollar, standard mosto fermentado method — the accessible baseline for Pisco Sour production'
        },
        {
            'tier': 2,
            'tier_name': 'Tabernero or Macchu Pisco Single Variety',
            'criteria': 'Named single-variety Quebranta from identified estate vineyards, controlled fermentation, precise distillation cut at target ABV without dilution — the premium tier for connoisseur Pisco Sour and neat service'
        },
        {
            'tier': 3,
            'tier_name': 'Acholado Blend (Multi-Variety)',
            'criteria': 'Blended pisco from multiple varieties (typically aromatic Italia or Torontel combined with earthy Quebranta) — the most complex pisco style, with the aromatic variety contributing floral intensity and the non-aromatic contributing body and earthy depth'
        },
        {
            'tier': 4,
            'tier_name': 'Mosto Verde (Partially Fermented, Premium)',
            'criteria': 'Pisco distilled from must that has not completed fermentation — the residual unfermented sugar transfers as glycerol and sugar compounds to the distillate through the copper pot still, producing a rounder, more complex spirit at higher cost due to lower conversion efficiency; the luxury tier of Peruvian pisco production'
        }
    ],
    'service_intelligence': {
        'temperature': 'Room temperature (20–22°C) for neat tasting; chilled at 4–6°C in the Pisco Sour preparation; a few drops of still water at room temperature opens the earthy Quebranta aromatics effectively for neat assessment',
        'vessel': 'Pisco Sour: coupe glass (traditional) or rocks glass with frothy egg white foam; Neat: tulip or small wine glass to concentrate the subtle earthy aromatics; Copa glass for a Pisco and Tonic (pisco + tonic + lime + salt rim)',
        'pisco_sour_protocol': 'Classic Pisco Sour: 60ml pisco Quebranta, 30ml fresh lime juice, 20ml simple syrup, 1 egg white, shake violently with ice, strain into coupe, dash of Angostura bitters on the foam; the Angostura connects the Peru PCT narrative to the Trinidad production origin of the bitters that complete the classic cocktail'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Bodegas y Viñedos Tabernero (Ica Valley) — the accessible premium benchmark; Caravedo (Ica) — the fine artisan benchmark; Tres Generaciones and Macchu for specialist allocation',
        'north_america_access': 'Peruvian pisco growing availability in US through specialty spirits retailers; in BC Canada through BCLDB (Tabernero and Macchu listed); the Pisco Sour\'s popularity in Latin American restaurants in Vancouver (Yuwa, Coppino\'s) has driven retail demand',
        'culinary_application': 'The Pisco Sour is the gateway cocktail but Quebranta pisco also works as a Singani-style base for Andean-inspired cocktails: pairing with fresh herb garnishes (huacatay, muña) in South American diaspora restaurant programming; the desert-terroir origin connects narratively to cacti-inspired garnishes and Peruvian botanical ingredients'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('wine', 'Brazil — Vale dos Vinhedos DOCG (Serra Gaúcha Red, Merlot-Tannat-Cabernet Blend, Italian Immigrant Heritage)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Miolo Wine Group — Vale dos Vinhedos DOCG',
    'location': 'Bento Gonçalves, Serra Gaúcha, Rio Grande do Sul, Brazil',
    'description': 'Miolo Wine Group is Brazil\'s largest family-owned wine producer and the primary architect of the Vale dos Vinhedos DOCG — Brazil\'s most prestigious wine appellation. The Miolo family are fourth-generation descendants of Italian immigrants from Treviso and Vicenza provinces of Veneto who arrived in Serra Gaúcha in the 1890s. The DOCG designation (Brazil\'s highest wine quality classification, modeled on Italian DOCG) was achieved in 2012, covering reds from Merlot, Cabernet Sauvignon, Cabernet Franc, and Tannat. Miolo\'s Lote 43 (named after the original land grant number assigned to the Miolo family in 1897) is the flagship red blend that has defined the Vale dos Vinhedos red wine style internationally.',
    'founded': '1897 (farm); winery 1989',
    'region': 'Vale dos Vinhedos, Serra Gaúcha, Brazil',
    'website': 'miolo.com.br',
    'verified': True
})

session.add_beverage({
    'name': 'Miolo Lote 43 Red — Vale dos Vinhedos DOCG, Merlot-Tannat-Cabernet Blend, Italian Immigrant Heritage 1897',
    'category': 'wine',
    'subcategory': 'red_wine',
    'origin': 'Brazil',
    'region': 'Vale dos Vinhedos DOCG, Serra Gaúcha, Brazil',
    'producer': 'Miolo Wine Group — Vale dos Vinhedos DOCG',
    'alcohol_content': 13.5,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Vale dos Vinhedos (Valley of the Vineyards) sits at the heart of Serra Gaúcha — the highlands of Rio Grande do Sul state at 700–900m elevation, where the steep-sided valley of the Pelotas River tributary has accumulated deep soils on the valley walls while maintaining cold air drainage through the valley floor that prevents frost damage to the highest-elevation vineyards. The valley was settled by Venetian immigrants (predominantly from Treviso, Vicenza, and Verona provinces) brought to Brazil by the Portuguese colonial government from 1875 onward to populate the southern highlands after Brazilian abolition reduced the plantation labor supply — creating the most direct contemporary Italian viticulture transplant to a Portuguese colonial agricultural framework in the world. The soils of Vale dos Vinhedos are derived from the weathering of the same Paraná-Santa Catarina basaltic flood volcanic complex that also underlies parts of Argentina\'s Mendoza wine region — deep, iron-rich red basaltic soils with excellent drainage and strong mineral content. The tropical highlands of Rio Grande do Sul receive 1,600–1,800mm of annual rainfall distributed throughout the year without a true dry season, creating the most challenging viticulture conditions of any major DOCG in the world: humidity management is the primary technical challenge, requiring both canopy management to promote air circulation and grape variety selection that resists downy mildew and botrytis in high-humidity conditions. Merlot was identified early as the variety best adapted to these conditions — its thicker skin and earlier ripening allow harvest before the heaviest autumn rains.'
    ),
    'production_technique': (
        'Miolo harvests manually from their certified Vale dos Vinhedos DOCG parcels in February-March (Southern Hemisphere harvest), selecting Merlot (approximately 70%), Tannat (15%), Cabernet Sauvignon (10%), and Cabernet Franc (5%) in separate passes timed to variety-specific ripening. The varieties are fermented separately in temperature-controlled stainless steel tanks at 26–28°C for 10–12 days with selected Saccharomyces cerevisiae, then blended for malolactic fermentation and subsequent barrel aging. The Lote 43 blend is designed to balance the ripe plum-chocolate character of Merlot (the backbone variety best adapted to Vale dos Vinhedos) with the structure and tannin of Tannat (a Basque-origin variety introduced to Rio Grande do Sul by French-Basque immigrants who settled adjacent to the Italian community) and the aromatic depth of Cabernet Sauvignon and Franc. Aging occurs in 225-litre French and American oak barrels (approximately 30–40% new oak) for 12–16 months, followed by 6 months of bottle aging before release. The resulting wine represents Brazil\'s closest approximation to a Bordeaux or Pomerol blend: Merlot-dominant, medium-bodied, accessible in youth but structured for 5–8 year aging. The DOCG certification (Brazil\'s first) requires all fruit to originate from the demarcated Vale dos Vinhedos zone, harvest by hand (machine harvest prohibited), and meeting minimum chemical and sensory standards for the Vinho com Indicação de Procedência designation.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Pomerol Merlot (France, Merlot-dominant, clay soil)',
            'connection': 'Miolo Lote 43 and Pomerol both anchor on Merlot as the primary variety contributing plum-chocolate body, with supporting Cabernet Franc providing aromatic precision — both from high-clay-content volcanic or sedimentary soils (basalt-derived red clay in Vale dos Vinhedos, Pomerol\'s famous blue clay plateau) that produce Merlot of exceptional depth and softness'
        },
        {
            'tradition': 'Argentine Malbec Mendoza (South American high-altitude, Italian immigrant parallel)',
            'connection': 'Both Brazil Vale dos Vinhedos and Argentina Mendoza are South American wine regions built by European immigrant communities under colonial agricultural frameworks (Portuguese in Brazil, Spanish in Argentina) who adapted European viticulture to New World volcanic mountain terrain — Vale dos Vinhedos with Italian Veneto immigrants, Mendoza with Italian and Spanish Andalucian immigrants producing distinctly South American expressions of Old World varieties'
        },
        {
            'tradition': 'Cave Geisse Serra Gaúcha Sparkling (same valley, same immigrant heritage)',
            'connection': 'Miolo Lote 43 red and Cave Geisse Brut Nature represent the two signature expressions of Vale dos Vinhedos wine culture — the still red and the sparkling white — both produced by descendants of the same 1890s Italian immigrant wave on the same volcanic highland terrain, creating the complete "New World Portuguese colonial Italian wine culture" narrative of Serra Gaúcha'
        }
    ],
    'sensory_profile': {
        'appearance': 'Deep ruby with purple tint; medium opacity; good legs at 13.5% ABV; clear without sediment in youth',
        'nose': 'Accessible and ripe: plum, dark cherry, subtle vanilla from French oak, mocha from the Merlot-Tannat combination, dried herbs in the Cabernet component — the tropical highland character shows as a slightly more exuberant, fruit-forward approach than Bordeaux while maintaining European grape variety recognition',
        'palate': 'Medium-full body, accessible in youth with soft Merlot tannins, plum-chocolate mid-palate, the Tannat contribution shows as a firmer backbone than standard Merlot-only blends, medium-long finish with sweet oak integration — a wine that communicates its Merlot heritage while showing the Brazilian highland origin through the tropical ripeness'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Miolo Reserva Range',
            'criteria': 'Single-variety wines from Vale dos Vinhedos (Merlot Reserva, Cabernet Sauvignon Reserva) — accessible entry to the DOCG quality tier at modest pricing'
        },
        {
            'tier': 2,
            'tier_name': 'Miolo Lote 43',
            'criteria': 'The flagship blend: Merlot-Tannat-Cabernet, hand-harvested, French and American oak, 16 months barrel — the benchmark Vale dos Vinhedos red and Brazil\'s most internationally recognized red wine'
        },
        {
            'tier': 3,
            'tier_name': 'Miolo Merlot DOCG Single Vineyard',
            'criteria': 'Identified single-vineyard Merlot expressions from the Vale dos Vinhedos demarcated zone, 24+ months barrel aging, lower production — the precision tier demonstrating how specific valley micro-terroirs express differently within the DOCG'
        },
        {
            'tier': 4,
            'tier_name': 'Miolo Seival Reserva (Tannat Dominant)',
            'criteria': 'Tannat-dominant expressions from cooler, higher-altitude parcels — demonstrating the Basque immigrant Tannat variety\'s ability to produce structured, age-worthy red wine in the Serra Gaúcha highlands'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 16–18°C — standard red wine temperature appropriate for the Merlot-dominant blend; slightly cooler serving temperature than Bordeaux because the tropical ripeness can overwhelm at 20°C; 30 minutes decanting recommended for wines under 5 years old',
        'vessel': 'Standard Bordeaux or Burgundy glass appropriate for the Merlot-dominant character; no special requirements given the accessible tannin structure and medium body',
        'food_pairing_philosophy': 'Vale dos Vinhedos red is the natural companion for the churrasco tradition of southern Brazil: the tropical ripeness and Tannat structure cut through the fat of grilled meat beautifully; in PNW context, works with BC lamb, wild Pacific salmon in a reduction sauce, and any preparation where a fruit-forward but structured red is needed rather than a highly tannic or highly acidic expression'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Miolo Wine Group — Lote 43 is the internationally exported benchmark for Vale dos Vinhedos DOCG red wine; also Quinta do Seival (Miolo) and Casa Valduga for comparison within the appellation',
        'north_america_access': 'Miolo through Vias Imports (US); limited BCLDB listing in BC but available through private import; growing availability in Brazilian restaurant programs in Vancouver and Toronto; Lote 43 is available on LCBO Ontario product submissions',
        'culinary_application': 'The Portuguese colonial narrative connecting Vale dos Vinhedos to the same immigration-in-colonial-framework as Macau and Goa creates compelling cross-cultural menu storytelling; serve with Brazilian churrasco-inspired preparations at PCT-themed dinners; the Tannat-Merlot structure works with gamey preparations where a lighter New World red would be overwhelmed'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()
session.finish()
