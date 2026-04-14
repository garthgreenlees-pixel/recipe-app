import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Haiti — Artibonite Valley (Barbancourt VSOP, Rhum Agricole, Haitian Highland Cane)',
    output_dir='.',
    starting_entry=1,
    session_number=50,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Distillerie Barbancourt — Port-au-Prince, Haiti',
    'location': 'Domaine de Barbancourt, Croix des Bouquets, Haiti',
    'description': (
        'Distillerie Barbancourt was founded in 1862 by Dupré Barbancourt, a French immigrant from the Cognac region '
        'of Charente who applied double-distillation principles from the Cognac tradition to fresh Haitian sugarcane juice. '
        'The distillery operates from the Domaine de Barbancourt estate near Port-au-Prince, drawing fresh cane from the '
        'Artibonite Valley — the most fertile agricultural zone in Haiti — and the plains surrounding the estate. '
        'Barbancourt is the only Haitian rum producer with consistent international export presence and one of a small '
        'number of Caribbean rhum agricole producers that ages its spirit in Limousin French oak in a manner directly '
        'derived from Cognac tradition. The distillery survived the 2010 earthquake that devastated much of the '
        'Port-au-Prince metropolitan region and continues to be operated by the Gardère family, descendants of the '
        'original Barbancourt founder.'
    ),
    'founded': '1862',
    'region': 'Artibonite Valley / Croix des Bouquets, Haiti',
    'website': 'barbancourt.net',
    'verified': True
})

session.add_purveyor({
    'name': 'Vias Imports (US) / Authentic Wine & Spirits Merchants (Canada)',
    'type': 'importer',
    'description': (
        'Barbancourt is distributed in the United States through multiple regional importers; '
        'in Canada through provincial liquor boards and specialty importers. '
        'BC distribution through BCLDB special orders and private import. '
        'Haiti rum is growing in North American premium cocktail programming following the '
        'resurgence of interest in rhum agricole beyond Martinique and Guadeloupe.'
    ),
    'markets_served': ['US', 'Canada', 'UK', 'EU', 'Caribbean'],
    'traditions_carried': ['spirits'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'Barbancourt VSOP Réserve Spéciale — Artibonite Valley Rhum Agricole, Fresh Cane Juice, Limousin Oak 8-Year',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Haiti',
    'region': 'Haiti — Artibonite Valley (Barbancourt VSOP, Rhum Agricole, Haitian Highland Cane)',
    'producer': 'Distillerie Barbancourt — Port-au-Prince, Haiti',
    'alcohol_content': 43.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The Artibonite Valley is Haiti\'s primary agricultural plain — a broad, irrigated alluvial valley stretching '
        'inland from the Gulf of Gonâve between the Chaîne des Matheux and the Montagnes Noires, at elevations '
        'between 50 and 200 metres above sea level. The valley is fed by the Artibonite River, the longest river '
        'in Hispaniola at 320km, which drains the central plateau and brings sediment-rich water to the coastal '
        'plain, creating deep, fertile alluvial soils with excellent moisture retention. Barbancourt sources fresh '
        'sugarcane (Saccharum officinarum) from the Artibonite Valley as well as from the Cul-de-Sac plain '
        'surrounding the distillery near Croix des Bouquets — an area of flat, intensely cultivated land east of '
        'Port-au-Prince at 30–60m elevation with calcareous soils and a tropical wet-dry climate. Haiti sits at '
        'the western third of Hispaniola, sharing the island with the Dominican Republic, in the northern '
        'Caribbean. The maritime tropical climate brings consistent heat (average 27°C), high humidity, and a '
        'pronounced wet season from April to October that promotes vigorous cane growth. Haiti\'s colonial history '
        'as Saint-Domingue — once the wealthiest colony in the Western Hemisphere and the source of 40% of '
        'European sugar and 60% of European coffee in the 1780s — means its sugarcane agriculture has roots '
        'going back to the earliest phase of Columbian Exchange crop transplantation in the Caribbean from the '
        'Spanish colonization of 1492 onward.'
    ),
    'production_technique': (
        'Barbancourt is produced by the rhum agricole method — pressing fresh-cut sugarcane to juice (vesou) '
        'within hours of harvest rather than fermenting molasses, the byproduct of sugar refining. This '
        'fundamental distinction between agricole (fresh juice) and traditionnel (molasses-based) rum defines '
        'the character of Barbancourt as a fresh, vegetal, grassy spirit with immediate cane character versus '
        'the deeper, more molasses-inflected character of most Caribbean rums. The fresh cane juice is '
        'inoculated with selected Saccharomyces cerevisiae and fermented in open-top stainless steel '
        'fermenters for 30–36 hours — a relatively short, warm fermentation that preserves the primary cane '
        'aromatics without generating excess ester complexity. Distillation follows the Cognac double-distillation '
        'principle that founder Dupré Barbancourt imported from Charente: first distillation in continuous column '
        'stills produces a low-wine at approximately 25–30% ABV (the brouillis equivalent); second distillation '
        'through copper pot stills produces the spirit at 65–70% ABV, concentrating and refining the cane '
        'character. This pot still second-distillation step distinguishes Barbancourt from standard column-only '
        'agricole producers and gives the spirit additional copper contact and reflux that shapes its texture. '
        'The VSOP (Réserve Spéciale) is aged a minimum of 8 years in Limousin French oak casks — the same '
        'forest oak used in Cognac aging — at the Domaine de Barbancourt estate in Haiti\'s tropical climate. '
        'Tropical aging accelerates maturation: the angel\'s share loss is approximately 10–12% per year in '
        'Haiti compared to 2–3% in Cognac, meaning that 8 years of tropical aging imparts colour and oak '
        'integration equivalent to 30–40 years of temperate aging. Final proofing to 43% ABV for export.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Cognac (Charente, France) — double distillation, Limousin oak',
            'connection': (
                'Barbancourt is the direct Caribbean heir of the Cognac distillation tradition: founder '
                'Dupré Barbancourt transplanted the double-distillation method (brouillis + repasse in copper '
                'pot stills) and Limousin oak aging from his native Charente to Haiti in 1862, creating the '
                'only Caribbean spirit whose technical lineage traces explicitly to the Cognac production '
                'code rather than to British or Spanish colonial rum traditions. The parallels are structural: '
                'both use double pot still distillation for texture, both age in the same forest oak, both '
                'produce VSOP and XO age designations following French brandy nomenclature.'
            )
        },
        {
            'tradition': 'Martinique AOC Rhum Agricole — fresh cane juice distillation',
            'connection': (
                'Barbancourt and Martinique rhum agricole share the fresh-cane-juice fermentation base that '
                'distinguishes both from molasses-based rums: both capture the grassiness, floral cane '
                'character, and vegetal freshness of vesou fermented within 24–36 hours of cane cutting. '
                'The key technical difference is that Martinique AOC requires column-still distillation '
                'with precise cut points, while Barbancourt adds a Cognac-derived copper pot second pass '
                'that introduces rounder texture and greater phenolic complexity absent from pure column '
                'agricole distillates.'
            )
        },
        {
            'tradition': 'Clairin (Haiti) — small-producer wild-ferment cane spirit',
            'connection': (
                'Barbancourt and Haitian clairin represent the two poles of Haitian cane spirit production: '
                'Barbancourt is the industrialized, export-oriented, Cognac-heritage aged spirit; clairin '
                'is the small-batch, wild-fermented, unaged cane spirit made by village distillers '
                'throughout rural Haiti using indigenous Saccharomyces and pit fermentation. Both draw from '
                'the same Artibonite Valley agricultural base but express the terroir through radically '
                'different technical lenses — Barbancourt through French colonial viticultural refinement, '
                'clairin through pre-industrial subsistence distillation unchanged since the colonial era.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep amber-gold with mahogany tints from 8 years in Limousin oak; tropical aging produces '
            'a richer, deeper colour than equivalent age in temperate conditions; good legs indicating '
            '43% ABV and residual glycerol from the pot still distillation.'
        ),
        'nose': (
            'Fresh sugarcane and vegetal green character from the agricole base persists beneath the oak '
            'influence; vanilla and caramel from the Limousin oak integration; dried tropical fruit (ripe '
            'mango, guava) from the ester development during tropical aging; floral cane blossom on the '
            'mid-nose; a faint Cognac-like rancio quality beginning to develop in older bottlings from '
            'long oak contact — a character formed by fatty acid ester oxidation that is the signature '
            'of pot still distillation aged in used French oak over extended periods.'
        ),
        'palate': (
            'Medium-full body from the dual distillation and oak contact; the fresh cane character of the '
            'agricole base remains present as a green, vegetal thread beneath the oak-derived vanilla and '
            'dried fruit; warm but balanced at 43% ABV; the Limousin oak tannin is fine-grained and '
            'integrative rather than harsh; long finish with agricultural raw cane character transitioning '
            'through oak spice to a clean, dry end — the Cognac double-distillation heritage showing in '
            'the precision of the spirit\'s architecture despite the tropical origin.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Barbancourt Three Stars (unaged)',
            'criteria': (
                'The unaged Barbancourt expression aged only 1–2 years before release, showing fresh green '
                'cane, young spirit heat, and minimal oak development — the entry point to the Barbancourt '
                'range used primarily in cocktail applications where the raw agricole character is an asset.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Barbancourt Five Star (aged 4 years)',
            'criteria': (
                'The 4-year-aged expression in Limousin oak showing initial oak integration — vanilla and '
                'light caramel beginning to emerge while the fresh cane character still dominates; the '
                'standard rum bar reference point for accessible aged agricole quality without the price '
                'of the VSOP.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Barbancourt VSOP Réserve Spéciale (8 years)',
            'criteria': (
                'The 8-year flagship: full Limousin oak integration, tropical rancio development beginning, '
                'the fresh cane and oak in genuine balance — the benchmark expression that defines '
                'Barbancourt\'s position as a Cognac-heritage Caribbean aged agricole of international '
                'standard, suitable for neat service at fine dining level.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Barbancourt Reserve du Domaine (15 years)',
            'criteria': (
                'The 15-year estate reserve aged in oak at the Domaine de Barbancourt: maximum tropical '
                'aging concentration, deep mahogany colour, pronounced rancio complexity, dried fruit '
                'and exotic spice dominating the palate — Barbancourt at its most Cognac-like in '
                'character, with the fresh cane origin now serving as a structural foundation beneath '
                'layers of oak-derived complexity.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve the VSOP at 18–20°C for neat appreciation; a single large ice sphere reduces the '
            'serving temperature to 12–14°C while diluting slowly enough to open the tropical fruit '
            'aromatics without washing out the Limousin oak character; avoid refrigeration which '
            'suppresses the volatile cane aromatics that distinguish agricole from molasses rum.'
        ),
        'vessel': (
            'Glencairn or tulip glass for neat tasting to concentrate the agricole vegetal-fruit-oak '
            'aromatics; a wide rocks glass with a single large sphere for cocktail service; the '
            'Barbancourt Sour (VSOP, fresh lime, falernum, egg white) served in a coupe demonstrates '
            'how the agricole cane character interacts with citrus acid in a way that molasses rum '
            'cannot replicate.'
        ),
        'programme_note': (
            'In a PCT-themed spirits programme, Barbancourt VSOP anchors the West African Diaspora Trail '
            'connection: Haiti was the first Black republic in history (independence 1804), its sugarcane '
            'agriculture was built on African enslaved labour transported via the Middle Passage, and '
            'Barbancourt\'s survival through earthquake, political instability, and economic embargo '
            'represents the persistence of a distilling tradition rooted in both French colonial technique '
            'and Haitian resistance heritage.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Distillerie Barbancourt — the only internationally exported aged Haitian rum; '
            'the VSOP and Reserve du Domaine are the PCT standard-bearer expressions for Haiti '
            'in any rhum agricole or PCT colonial spirits programme.'
        ),
        'north_america_access': (
            'Barbancourt is distributed in most US states through regional spirits importers; '
            'available in Canada through provincial boards including LCBO Ontario listings and '
            'BC special orders; growing presence in premium cocktail bars across North America '
            'following the rhum agricole category expansion since 2015.'
        ),
        'culinary_application': (
            'Barbancourt VSOP works as the agricole component in a ti\' punch (pure cane sugar syrup, '
            'lime, spirit — the canonical French Antilles service) or as a Cognac analogue in '
            'preparations calling for aged brandy where the fresh cane note adds Caribbean agricultural '
            'register to sauces, reductions, or plated spirits service.'
        )
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region(
    'spirits',
    'Haiti — Grande Anse Department (Barbancourt Reserve Spéciale, 15-Year Aged, Plantation Heritage)'
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Distillerie Barbancourt — Domaine de Barbancourt Estate',
    'location': 'Croix des Bouquets, Département de l\'Ouest, Haiti',
    'description': (
        'The Domaine de Barbancourt estate encompasses the distillery and aging warehouses at Croix '
        'des Bouquets on the Cul-de-Sac plain east of Port-au-Prince, where the 15-year Reserve du '
        'Domaine is produced from the same agricultural base as the VSOP but with extended tropical '
        'warehouse aging. The domaine has been operated continuously since 1862 and survived the '
        '2010 earthquake that caused an estimated 316,000 deaths — the distillery itself sustained '
        'structural damage but the aging casks were preserved, representing the continuity of the '
        'Barbancourt heritage through Haiti\'s most catastrophic modern event.'
    ),
    'founded': '1862',
    'region': 'Cul-de-Sac Plain, Département de l\'Ouest, Haiti',
    'website': 'barbancourt.net',
    'verified': True
})

session.add_beverage({
    'name': 'Barbancourt Reserve du Domaine — 15-Year Tropical Aged, Limousin Oak, Haitian Plantation Heritage',
    'category': 'spirits',
    'subcategory': 'rum',
    'origin': 'Haiti',
    'region': 'Haiti — Grande Anse Department (Barbancourt Reserve Spéciale, 15-Year Aged, Plantation Heritage)',
    'producer': 'Distillerie Barbancourt — Domaine de Barbancourt Estate',
    'alcohol_content': 43.0,
    'price_tier': 'super_premium',
    'terroir_origin': (
        'The Grande Anse Department is Haiti\'s southernmost administrative region, facing the '
        'Caribbean Sea along the southwestern peninsula — a more isolated, less industrially '
        'developed zone than the Artibonite corridor, with traditional small-holder sugarcane '
        'cultivation persisting in the coastal river valleys. The Cul-de-Sac plain where the '
        'Barbancourt domaine sits is geologically a tectonic graben — a down-dropped rift valley '
        'bounded by the Chaîne des Matheux to the north and the Massif de la Selle to the south, '
        'at elevations of 20–80m above sea level with deep calcareous alluvial soils. The tropical '
        'climate at the domaine is characterized by mean annual temperatures of 26–28°C, '
        'approximately 600mm annual precipitation (supplemented by irrigation from the Artibonite '
        'drainage system), and the consistency of tropical maritime conditions — minimal seasonal '
        'temperature variation — that creates the unique accelerated aging environment of tropical '
        'rum maturation. In a tropical warehouse at 28°C average, the cask oak expands and contracts '
        'daily with ambient temperature fluctuations, driving spirit in and out of the wood at '
        'rates 4–6 times greater than a Cognac cellar in Charente at 12–15°C average. The angel\'s '
        'share loss at the domaine runs 8–12% per year, meaning that after 15 years of tropical '
        'aging, the original cask volume has been reduced by approximately 60–80%, concentrating '
        'the remaining spirit to remarkable intensity of colour, flavour, and oak-derived complexity.'
    ),
    'production_technique': (
        'The Reserve du Domaine 15-year is produced from the same agricole base as the VSOP: '
        'fresh Artibonite Valley cane juice fermented 30–36 hours, double-distilled through '
        'column brouillis pass followed by copper pot second distillation at 65–70% ABV final '
        'strength. The critical distinction is extended aging in a selection of Limousin oak '
        'casks — both new and previously used — for a minimum of 15 years in the tropical warehouse '
        'at Domaine de Barbancourt. The master blender selects individual casks that have developed '
        'the characteristic tropical rancio note — a complex oxidative quality combining dried fruit, '
        'mushroom, walnut, and exotic spice formed through long-chain fatty acid ester oxidation '
        'in the presence of French oak tannins at tropical temperatures. This rancio development '
        'in aged Caribbean rum mirrors the rancio that develops in 20–30 year Cognac but at a '
        'compressed timescale due to the tropical aging climate. Selected casks are blended to '
        'produce the Reserve du Domaine at consistent quality; the final blend is proofed to 43% '
        'ABV with demineralized water before bottling. No caramel colouring is added — the deep '
        'mahogany colour is entirely derived from 15 years of tropical Limousin oak contact. '
        'The Reserve du Domaine is Barbancourt\'s argument that the Caribbean tropics can produce '
        'aged spirits of equivalent complexity to temperate-aged European brandies — on a shorter '
        'chronological timeline but with more dramatic cumulative oak contact.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'XO Cognac (Charente, 10+ years in Limousin oak)',
            'connection': (
                'Barbancourt Reserve du Domaine and XO Cognac are the most structurally comparable '
                'spirits across the French brandy and Caribbean rum categories: both use double '
                'pot still distillation, both age exclusively in Limousin forest French oak, both '
                'develop rancio quality through extended oxidative aging, and both use the French '
                'brandy age designation vocabulary (Réserve, Reserve du Domaine, XO, VSOP). '
                'The fundamental difference is that 15 years of Haitian tropical aging produces '
                'colour depth and rancio development equivalent to approximately 40–50 years in '
                'a Charente cellar — demonstrating how tropical climate compresses aging time '
                'without shortcutting the underlying oak chemistry.'
            )
        },
        {
            'tradition': 'El Dorado 21-Year (Guyana, Demerara, aged column-still rum)',
            'connection': (
                'Barbancourt 15-Year and El Dorado 21-Year are both the premium apex expressions '
                'of their respective national rum traditions, both aged in tropical warehouses '
                'for extended periods to develop maximum complexity, and both marketed at price '
                'points that position Caribbean rum against aged Cognac and single malt Scotch '
                'in the luxury spirits category. The key structural difference is distillation '
                'heritage: Barbancourt uses Cognac pot-still double distillation, El Dorado uses '
                'antique wooden Coffey still column distillation — producing different textural '
                'and ester profiles in the spirit base that then age into different rancio characters.'
            )
        }
    ],
    'sensory_profile': {
        'appearance': (
            'Deep mahogany with garnet tints; full opacity; heavy, slow-moving legs indicating '
            'high glycerol content from 15 years of tropical oak extraction; the colour alone '
            'communicates the extended tropical aging — darker than most 30-year Cognac by volume '
            'of oak contact despite shorter chronological age.'
        ),
        'nose': (
            'Pronounced tropical rancio: dried exotic fruit (tamarind, dried mango, prune), '
            'Limousin oak tannin expressed as furniture polish and nutmeg, dark caramel, '
            'a thread of fresh cane blossom still visible beneath the aged complexity — the '
            'agricole origin persisting through 15 years of oak. Beeswax and leather from '
            'long cask contact; the Cognac heritage unmistakable in the rancio register '
            'despite the unmistakably Caribbean fruit character from the ester development '
            'during tropical fermentation and aging.'
        ),
        'palate': (
            'Full-bodied and warming; the fresh cane base has been transformed by 15 years of '
            'tropical Limousin oak into a rich, layered spirit in which dried tropical fruit, '
            'vanilla, dark chocolate, and warm oak spice succeed each other through a very long '
            'finish; tannin grip is present but fully integrated; the 43% ABV gives warmth '
            'without heat; the finish extends through oak-derived bitterness into a clean, '
            'dry agricultural cane character that is the signature of Barbancourt\'s agricole '
            'base surviving even the most intense aging program in the Caribbean.'
        )
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Barbancourt Three Stars (white / minimally aged)',
            'criteria': (
                'Entry expression aged 1–2 years or unaged: green cane, young spirit character, '
                'minimal oak — the cocktail workhorse and the starting point for understanding '
                'the fresh agricole cane base before aging transforms it.'
            )
        },
        {
            'tier': 2,
            'tier_name': 'Barbancourt VSOP Réserve Spéciale (8 years)',
            'criteria': (
                'Eight-year tropical aged: the balance point between fresh cane character and '
                'oak development — sufficient Limousin oak integration for neat service but '
                'retaining the vegetal, floral cane thread that identifies the agricole origin.'
            )
        },
        {
            'tier': 3,
            'tier_name': 'Barbancourt Estate Reserve (small batch selections)',
            'criteria': (
                'Periodic small-batch releases from exceptional cask selections aged 10–12 years: '
                'intermediate between the VSOP and the Reserve du Domaine, showing accelerated '
                'tropical rancio development in standout individual casks before blending.'
            )
        },
        {
            'tier': 4,
            'tier_name': 'Barbancourt Reserve du Domaine (15 years)',
            'criteria': (
                'The apex of the Barbancourt range: maximum tropical Limousin oak integration, '
                'full rancio development, deep mahogany colour — the expression that positions '
                'Barbancourt in direct comparison with XO Cognac and demonstrates how the '
                'Haitian tropical aging environment compresses French brandy maturation timelines '
                'while preserving the agricole cane character as the spirit\'s foundation.'
            )
        }
    ],
    'service_intelligence': {
        'temperature': (
            'Serve neat at 18–20°C in a warmed glass to open the full tropical rancio and dried '
            'fruit complexity; avoid ice, which suppresses the evolved volatiles that make the '
            '15-year expression distinct from younger Barbancourt expressions; a few drops of '
            'still water at room temperature opens the rancio register and softens the oak '
            'tannin for the first tasting pour.'
        ),
        'vessel': (
            'Tulip or Glencairn glass exclusively for the Reserve du Domaine — the concentrated '
            'aromatics require a vessel that focuses vapour at the rim; a snifter is acceptable '
            'for tableside presentation but the wider aperture disperses the rancio aromatics '
            'too rapidly; serve in a flight context following the VSOP to demonstrate the '
            'vertical aging progression from 8 to 15 years of tropical Limousin oak.'
        )
    },
    'purveyor_intelligence': {
        'benchmark_producer': (
            'Distillerie Barbancourt — Reserve du Domaine 15-Year is the undisputed apex of '
            'Haitian rum production and the sole Caribbean expression with structural Cognac '
            'heritage (double distillation, Limousin oak) at this aging level; no comparable '
            'Haitian producer at this quality tier exists for cross-reference.'
        ),
        'north_america_access': (
            'Available through specialty spirits retailers in major US markets; BCLDB private '
            'import in BC; allocation-basis availability given limited production from extended '
            'tropical aging and high angel\'s share losses; price tier positions the Reserve du '
            'Domaine at USD $80–120 retail, competing directly with aged single malts and XO Cognac.'
        ),
        'culinary_application': (
            'The Reserve du Domaine is a prestige spirits service item at the close of a PCT-themed '
            'tasting dinner: its Cognac heritage connects the Charente to the Caribbean through the '
            'French colonial maritime network; its Haitian origin connects to the West African '
            'Diaspora Trail and the agricultural history of Saint-Domingue as the Caribbean\'s '
            'most productive colonial plantation economy before the 1804 revolution.'
        )
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
