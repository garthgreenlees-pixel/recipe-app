#!/usr/bin/env python3
"""terminal4_batch15_tech_links.py — technique_product links for refs 81-137 that have no links"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """
INSERT INTO beverage_technique_products (technique_id, product_id, relevance_note)
VALUES (%(technique_id)s, %(product_id)s, %(relevance_note)s)
ON CONFLICT (technique_id, product_id) DO NOTHING
"""

LINKS = [
    # Ref 81 — PNW Viticulture History
    {"technique_id": 81, "product_id": 447, "relevance_note": "Garry Oaks embodies the Gulf Islands expression of BC viticulture — a product of the modern appellation era described in this reference."},
    {"technique_id": 81, "product_id": 453, "relevance_note": "Wilridge Rattlesnake Hills Syrah represents the evolution of Washington viticulture from missionary-era plantings to defined AVA terroir."},
    {"technique_id": 81, "product_id": 458, "relevance_note": "Snipes Family Old Vine Grenache roots trace to some of WA's oldest vines, directly relevant to PNW viticulture heritage."},
    {"technique_id": 81, "product_id": 461, "relevance_note": "Cristom exemplifies the Willamette Valley Pinot Noir story that defines Oregon's place in PNW wine history."},
    {"technique_id": 81, "product_id": 464, "relevance_note": "Cowhorn's Applegate Valley Rhône blend illustrates Southern Oregon AVA development — a frontier appellation in the PNW story."},
    {"technique_id": 81, "product_id": 454, "relevance_note": "Destiny Ridge Wahluke Slope Cab demonstrates the AVA-designation era of Washington viticulture central to this reference."},

    # Ref 82 — Fermentation Science
    {"technique_id": 82, "product_id": 80, "relevance_note": "Seasoning Kombucha is a live fermented beverage; its SCOBY-driven chemistry directly illustrates the bacterial and yeast fermentation principles in this reference."},
    {"technique_id": 82, "product_id": 84, "relevance_note": "Tonica Kombucha's dry fermentation profile illustrates how fermentation time and temperature control complexity."},
    {"technique_id": 82, "product_id": 86, "relevance_note": "Wild Tonic Jun's honey and black tea substrate demonstrates symbiotic fermentation culture mechanics."},
    {"technique_id": 82, "product_id": 190, "relevance_note": "GT's Synergy illustrates commercial lacto-fermentation standardisation and its flavour science."},
    {"technique_id": 82, "product_id": 469, "relevance_note": "Lambanog's coconut sap-to-spirit fermentation is a direct illustration of tropical sugar-to-ethanol conversion described in fermentation science."},
    {"technique_id": 82, "product_id": 470, "relevance_note": "Basi's sugarcane fermentation with camias fruit represents traditional Philippine fermentation chemistry using indigenous acidulants."},

    # Ref 83 — Wine List Architecture / BTG Programme
    {"technique_id": 83, "product_id": 193, "relevance_note": "Rousseau Chambertin represents the prestige anchor required in a world-class wine list — the pinnacle Burgundy BTG or reserve benchmark."},
    {"technique_id": 83, "product_id": 299, "relevance_note": "Dagueneau Silex is the Loire reference point for a balanced list — producers of this calibre are the cornerstone of credible regional representation."},
    {"technique_id": 83, "product_id": 327, "relevance_note": "Giacosa Barolo Falletto represents Italian list architecture — a Piedmont benchmark that commands premium BTG pricing."},
    {"technique_id": 83, "product_id": 357, "relevance_note": "Tio Pepe Fino is the Sherry list entry point — an essential value proposition in a financially sound wine programme."},
    {"technique_id": 83, "product_id": 461, "relevance_note": "Cristom Mt. Jefferson demonstrates strategic Oregon Pinot positioning — credible terroir at accessible price within a BTG margin architecture."},

    # Ref 84 — Deductive Tasting (Competitive / Examination)
    {"technique_id": 84, "product_id": 193, "relevance_note": "Rousseau Chambertin is an examination-level benchmark for Burgundy red deduction — its pinot DNA in a grand cru context tests candidate mastery."},
    {"technique_id": 84, "product_id": 325, "relevance_note": "Gaja Barbaresco is a classic blind tasting challenge — Nebbiolo's high acid/tannin profile with Langhe modernism."},
    {"technique_id": 84, "product_id": 328, "relevance_note": "Conterno Monfortino is the traditionalist Barolo benchmark for deductive examination — its extended maceration and tar-rose structure is immediately diagnostic."},
    {"technique_id": 84, "product_id": 334, "relevance_note": "Biondi-Santi Brunello's Sangiovese Grosso expression is a key deductive endpoint — differentiated from Barolo's Nebbiolo by its structure and vintage dependency."},
    {"technique_id": 84, "product_id": 351, "relevance_note": "Vega Sicilia Unico is a deductive examination challenge — Tempranillo-based but with atypical international varieties and extreme age."},

    # Ref 85 — NA Beverage Programme Design
    {"technique_id": 85, "product_id": 80, "relevance_note": "Seasoning Kombucha represents fermented NA complexity — a pillar product for a genuine NA programme with depth."},
    {"technique_id": 85, "product_id": 81, "relevance_note": "Seedlip Spice 94 is the distilled spirit NA reference product — central to any professional NA programme."},
    {"technique_id": 85, "product_id": 82, "relevance_note": "Gruvi Bubbly Rosé illustrates the dealcoholised wine category in NA programme architecture."},
    {"technique_id": 85, "product_id": 83, "relevance_note": "Cawston Press exemplifies premium pressed juice as a sophisticated NA alternative — important for all-day NA programme depth."},
    {"technique_id": 85, "product_id": 89, "relevance_note": "Curious Elixirs No. 1 represents the cocktail-inspired NA category — highest margin, highest-engagement NA programme product."},
    {"technique_id": 85, "product_id": 188, "relevance_note": "Leitz Eins Zwei Zero demonstrates premium dealcoholised wine as a programme pillar alongside other NA categories."},

    # Ref 86 — Burgundy Classification System
    {"technique_id": 86, "product_id": 193, "relevance_note": "Rousseau Chambertin — Grand Cru level, the apex of Burgundy's classification and the ultimate reference point for this hierarchy."},
    {"technique_id": 86, "product_id": 194, "relevance_note": "Roumier Musigny — another Grand Cru, illustrating how different vineyard names relate within the same classification tier."},
    {"technique_id": 86, "product_id": 195, "relevance_note": "Leflaive Montrachet — white Grand Cru counterpart, essential to understanding how the classification applies across both colours."},
    {"technique_id": 86, "product_id": 197, "relevance_note": "Raveneau Chablis Grand Cru illustrates how Chablis sits within the broader Burgundy classification despite geographical distance."},
    {"technique_id": 86, "product_id": 202, "relevance_note": "Faiveley Corton-Charlemagne demonstrates the Côte de Beaune Grand Cru landscape relevant to the classification system."},
    {"technique_id": 86, "product_id": 435, "relevance_note": "Bouchard Côte de Nuits-Villages exemplifies the village-level tier at the base of the Burgundy quality pyramid."},

    # Ref 87 — Burgundy Pinot Noir Deductive Tasting
    {"technique_id": 87, "product_id": 193, "relevance_note": "Chambertin Grand Cru is the structural apex of Burgundy red deduction — its power and terroir signature calibrate the top of the deductive grid."},
    {"technique_id": 87, "product_id": 198, "relevance_note": "Mugnier Musigny represents Chambolle-Musigny's signature — silky, perfumed, Pinot at its most ethereal, key to understanding commune variation."},
    {"technique_id": 87, "product_id": 199, "relevance_note": "Jadot Chambertin Clos de Bèze is the Gevrey-Chambertin signature — deeper, more structured, essential contrast to Chambolle in deductive context."},
    {"technique_id": 87, "product_id": 417, "relevance_note": "Ponsot Clos de la Roche VV demonstrates Morey-Saint-Denis terroir — necessary for complete commune-level deduction in the Côte de Nuits."},
    {"technique_id": 87, "product_id": 420, "relevance_note": "Gouges Nuits-Saint-Georges represents the Nuits village signature — more structured, less perfumed, key deductive marker for appellation id."},
    {"technique_id": 87, "product_id": 435, "relevance_note": "Côte de Nuits-Villages demonstrates the regional appellation tier — understanding its lighter character is essential for complete deductive framework."},

    # Ref 88 — Chablis Kimmeridgian Terroir
    {"technique_id": 88, "product_id": 197, "relevance_note": "Raveneau Chablis Grand Cru Les Clos is the benchmark expression of Kimmeridgian terroir — its saline, oyster-shell minerality directly expresses the fossil limestone influence described in this reference."},
    {"technique_id": 88, "product_id": 200, "relevance_note": "Dauvissat Premier Cru La Forest is the entry point to understanding how Chablis limestone terroir expresses at the 1er cru tier."},
    {"technique_id": 88, "product_id": 197, "relevance_note": "Used as dual reference: Raveneau Les Clos is the canonical Kimmeridgian mineral palate benchmark for service and education."},

    # Ref 93 — Lambanog / Austronesian Fermentation Trail
    {"technique_id": 93, "product_id": 469, "relevance_note": "Barako Lambanog is the primary product of the Austronesian coconut palm fermentation trail — this reference is its core educational text."},
    {"technique_id": 93, "product_id": 467, "relevance_note": "Lehua Hawaiian Awa is part of the Pacific kava/awa network tracing Austronesian migration; Hawaiian awa shares the Pacific root with Philippine lambanog."},
    {"technique_id": 93, "product_id": 468, "relevance_note": "Samoan Ava embodies Polynesian fermentation ceremony as the Pacific counterpart to the Philippine fermentation tradition."},
    {"technique_id": 93, "product_id": 465, "relevance_note": "Tanna Kava roots are prepared by the same Pacific chewing/fermentation technique discussed in the Austronesian fermentation trail."},
    {"technique_id": 93, "product_id": 470, "relevance_note": "Ilocos Basi is the sugarcane fermentation counterpart to Lambanog within the Filipino beverage tradition covered by this reference."},
    {"technique_id": 93, "product_id": 154, "relevance_note": "Taki Mai Noble Kava is the commercial Polynesian kava expression that bridges the traditional Austronesian fermentation trail to modern service."},

    # Ref 96 — Ethiopian Coffee
    {"technique_id": 96, "product_id": 71, "relevance_note": "Ethiopia Yirgacheffe Washed is the canonical reference product for the Yirgacheffe standard described in this reference."},
    {"technique_id": 96, "product_id": 77, "relevance_note": "Bows & Arrows Ethiopia Shantawene demonstrates specialty roastery treatment of Ethiopian heirloom varieties."},
    {"technique_id": 96, "product_id": 389, "relevance_note": "Yirgacheffe YCFCU Grade 1 Washed represents cooperative-model Ethiopian origin quality — the benchmark for fair-trade Yirgacheffe."},
    {"technique_id": 96, "product_id": 390, "relevance_note": "Konga Natural Process Yirgacheffe illustrates how processing method (natural vs washed) creates dramatic variation within the same Ethiopian origin."},
    {"technique_id": 96, "product_id": 393, "relevance_note": "Harrar Longberry Natural demonstrates Ethiopia's second major heirloom region — the wild, blueberry natural process described in the reference."},
    {"technique_id": 96, "product_id": 394, "relevance_note": "Harrar HFCU Cooperative Grade 1 illustrates the co-op quality structure for Ethiopian Harrar origin."},

    # Ref 107 — Loire Valley Appellations and Grape Diversity
    {"technique_id": 107, "product_id": 299, "relevance_note": "Dagueneau Pouilly-Fumé Silex is the Loire Sauvignon Blanc reference — demonstrates Pouilly-Fumé's mineral expression at the top of the Loire hierarchy."},
    {"technique_id": 107, "product_id": 301, "relevance_note": "Domaine Huet Vouvray Sec demonstrates the Chenin Blanc appellation diversity described in the Loire Valley reference."},
    {"technique_id": 107, "product_id": 304, "relevance_note": "Domaine Cotat Sancerre demonstrates the Left Bank Sauvignon Blanc expression in the Loire's appellation diversity."},
    {"technique_id": 107, "product_id": 306, "relevance_note": "Pépière Muscadet illustrates Melon de Bourgogne's place in the Loire hierarchy — the Atlantic gateway appellation."},
    {"technique_id": 107, "product_id": 430, "relevance_note": "Charles Joguet Chinon demonstrates the red Cabernet Franc appellations of the Loire — Touraine's tuffeau terroir."},
    {"technique_id": 107, "product_id": 442, "relevance_note": "Henry Marionnet Touraine illustrates the everyday Loire expression — the broad Touraine appellation providing reference for value-tier Loire."},

    # Ref 108 — Chenin Blanc / Vouvray Style Spectrum
    {"technique_id": 108, "product_id": 301, "relevance_note": "Huet Vouvray Le Mont Sec is the dry Chenin Blanc reference point — illustrating the Sec tier of the Vouvray style spectrum."},
    {"technique_id": 108, "product_id": 302, "relevance_note": "Huet Vouvray Clos du Bourg Demi-Sec demonstrates the Demi-Sec sweetness tier — central to understanding Vouvray's style range."},
    {"technique_id": 108, "product_id": 442, "relevance_note": "Marionnet Touraine demonstrates how Chenin Blanc expresses outside Vouvray in the broader Touraine appellation."},
    {"technique_id": 108, "product_id": 430, "relevance_note": "Joguet Chinon demonstrates the Touraine context in which Vouvray's Chenin exists as one of many regional expressions."},

    # Ref 109 — Alsace Grand Cru Soil Types and Variety Mapping
    {"technique_id": 109, "product_id": 307, "relevance_note": "Trimbach Clos Sainte Hune is the iconic Riesling Alsace benchmark — grown on Rosacker Grand Cru, directly relevant to the Grand Cru soil mapping."},
    {"technique_id": 109, "product_id": 309, "relevance_note": "Zind-Humbrecht Riesling Clos Windsbuhl demonstrates single-lieu-dit Riesling expression in the Alsace Grand Cru terroir hierarchy."},
    {"technique_id": 109, "product_id": 310, "relevance_note": "Zind-Humbrecht Pinot Gris Hengst GC illustrates Pinot Gris on a specific Grand Cru — essential for variety-to-terroir mapping."},
    {"technique_id": 109, "product_id": 311, "relevance_note": "Weinbach Riesling Schlossberg GC demonstrates the diversity of Alsace Grand Cru soils (granite at Schlossberg) vs other GC soil types."},
    {"technique_id": 109, "product_id": 315, "relevance_note": "Ostertag Riesling Muenchberg GC illustrates biodynamic estate Grand Cru expression and volcanic soil type."},
    {"technique_id": 109, "product_id": 316, "relevance_note": "Marcel Deiss Bergheim demonstrates the blending approach to Alsace Grand Cru — complementary to the variety-mapping framework."},

    # Ref 110 — Alsace VT and SGN
    {"technique_id": 110, "product_id": 313, "relevance_note": "Hugel Riesling Vendange Tardive is the textbook VT (Vendange Tardive) style — directly illustrates the late harvest category described in this reference."},
    {"technique_id": 110, "product_id": 314, "relevance_note": "Trimbach Gewurztraminer Seigneurs de Ribeaupierre demonstrates the VT-tier aromatics and residual sugar framework for Gewurz."},
    {"technique_id": 110, "product_id": 312, "relevance_note": "Hugel Jubilee Riesling represents the late-harvest tradition within which VT and SGN selections are made."},
    {"technique_id": 110, "product_id": 309, "relevance_note": "Zind-Humbrecht Clos Windsbuhl is the baseline from which Zind-Humbrecht's VT/SGN tier selections emerge."},

    # Ref 111 — Cognac Cru Hierarchy, Aging, Style
    {"technique_id": 111, "product_id": 317, "relevance_note": "Remy Martin XO Excellence represents Grande Champagne and Petite Champagne-sourced Cognac at XO tier — primary product reference for Cognac education."},
    {"technique_id": 111, "product_id": 318, "relevance_note": "Delamain Pale and Dry XO represents Grande Champagne single-cru Cognac — illustrates the cru hierarchy premium described in this reference."},
    {"technique_id": 111, "product_id": 319, "relevance_note": "Hine Antique XO Premier Cru is a single Grande Champagne cru Cognac — directly illustrates Premier Cru Cognac positioning."},

    # Ref 112 — Armagnac vs Cognac
    {"technique_id": 112, "product_id": 317, "relevance_note": "Remy Martin XO represents the Cognac side of the Armagnac-Cognac comparison — double distillation, blended style."},
    {"technique_id": 112, "product_id": 318, "relevance_note": "Delamain Pale and Dry provides the Cognac benchmark for comparison against Armagnac's single distillation character."},
    {"technique_id": 112, "product_id": 320, "relevance_note": "Francis Darroze Bas-Armagnac 10 Year is the primary Armagnac reference product — single distillation, column still, directly compared in this reference."},
    {"technique_id": 112, "product_id": 321, "relevance_note": "Domaine Dupont Calvados demonstrates the apple brandy third axis in the French grape/grain distillate context."},
    {"technique_id": 112, "product_id": 324, "relevance_note": "Lemorton Calvados Domfrontais 15 Year illustrates aged apple brandy complexity alongside the Cognac/Armagnac comparison."},

    # Ref 113 — Pastis and Mediterranean Anise Family
    {"technique_id": 113, "product_id": 322, "relevance_note": "Ricard Pastis de Marseille is the definitive commercial pastis — directly illustrates the louche effect, anethole chemistry, and Marseille origin described."},
    {"technique_id": 113, "product_id": 323, "relevance_note": "Henri Bardouin demonstrates artisan Haute-Provence pastis — the complexity of wild herbal maceration beyond the standard commercial style."},
    {"technique_id": 113, "product_id": 365, "relevance_note": "Barbayanni Blue Label Ouzo illustrates the Greek anise distillate in the Mediterranean anise family covered by this reference."},
    {"technique_id": 113, "product_id": 366, "relevance_note": "Plomari Ouzo demonstrates Lesbos-specific ouzo production — the ouzo appellation context within the Mediterranean anise family."},
    {"technique_id": 113, "product_id": 368, "relevance_note": "Massaya Arak Silver represents the Levantine anise tradition — the third major Mediterranean anise spirit covered in this reference."},

    # Ref 114 — Barolo DOCG / MGA System
    {"technique_id": 114, "product_id": 327, "relevance_note": "Giacosa Barolo Falletto di Serralunga demonstrates the Serralunga d'Alba commune's power and longevity — key for MGA commune mapping."},
    {"technique_id": 114, "product_id": 328, "relevance_note": "Conterno Monfortino Riserva from Cascina Francia (Serralunga) is the iconic traditionalist Barolo — its MGA origin is central to commune terroir discussion."},
    {"technique_id": 114, "product_id": 329, "relevance_note": "Bartolo Mascarello Barolo is a single-cru-unspecified traditionalist wine — represents the older blended Barolo style preceding the MGA system."},
    {"technique_id": 114, "product_id": 330, "relevance_note": "Vietti Castiglione is a multi-commune Barolo blend — illustrates village appellation tier below MGA single-vineyard."},
    {"technique_id": 114, "product_id": 331, "relevance_note": "G.D. Vajra Bricco delle Viole is a La Morra commune MGA — contrasts with Serralunga's more tannic character for comprehensive commune mapping."},
    {"technique_id": 114, "product_id": 333, "relevance_note": "Ceretto Bricco Rocche is Castiglione Falletto MGA — the most sought-after commune for teaching Barolo DOCG wine hierarchy."},

    # Ref 115 — Nebbiolo Deductive Tasting
    {"technique_id": 115, "product_id": 325, "relevance_note": "Gaja Barbaresco is the iconic modernist Nebbiolo benchmark — its accessible structure contrasts with traditionalist Barolo for deductive grid understanding."},
    {"technique_id": 115, "product_id": 326, "relevance_note": "Gaja Sori Tildin demonstrates single-vineyard Barbaresco expression — key for deductive differentiation of Barbaresco village MGA variations."},
    {"technique_id": 115, "product_id": 327, "relevance_note": "Giacosa Falletto di Serralunga is the Barolo deductive benchmark — its tar-rose-anise Nebbiolo fingerprint defines the tasting framework."},
    {"technique_id": 115, "product_id": 328, "relevance_note": "Conterno Monfortino Riserva pushes Nebbiolo deduction to its extreme — 10+ year aged Barolo challenges candidate assessment of grape vs oak."},
    {"technique_id": 115, "product_id": 332, "relevance_note": "Roagna Barbaresco Crichet Paje demonstrates the traditional Barbaresco style — high acid, high tannin, long ageing, the counterpart to Gaja's modernism."},

    # Ref 116 — Brunello di Montalcino DOCG
    {"technique_id": 116, "product_id": 334, "relevance_note": "Biondi-Santi Brunello Riserva is the founding estate and definitive Brunello reference — its Sangiovese Grosso expression and Riserva DOCG regulations are directly described in this reference."},

    # Ref 117 — Super Tuscans / IGT Revolution
    {"technique_id": 117, "product_id": 335, "relevance_note": "Sassicaia is the founding Super Tuscan — its Cabernet Sauvignon origins and IGT status before DOC elevation are central to this reference."},
    {"technique_id": 117, "product_id": 336, "relevance_note": "Ornellaia Bolgheri Superiore is the second generation of Super Tuscans — Merlot-dominant, directly relevant to the IGT revolution's spread beyond Cabernet."},
    {"technique_id": 117, "product_id": 337, "relevance_note": "Tignanello is the Sangiovese + Cabernet Super Tuscan — the intermediate expression bridging traditional Italian varieties with international grapes."},
    {"technique_id": 117, "product_id": 380, "relevance_note": "Poliziano Vino Nobile demonstrates the indigenous Sangiovese DOC response that evolved alongside the Super Tuscan revolution."},

    # Ref 118 — Amarone / Appassimento Technique
    {"technique_id": 118, "product_id": 342, "relevance_note": "Dal Forno Romano Amarone is the benchmark for modern power-style Amarone — its extended appassimento and concentration directly illustrates the appassimento technique."},
    {"technique_id": 118, "product_id": 343, "relevance_note": "Giuseppe Quintarelli Amarone is the artisan appassimento benchmark — traditional long drying, handcrafted method central to the appassimento style spectrum."},
    {"technique_id": 118, "product_id": 345, "relevance_note": "Allegrini Amarone Classico demonstrates modern appellation Amarone using controlled appassimento — accessible benchmark for the style."},

    # Ref 119 — Grappa, Amaro, Italian Digestif
    {"technique_id": 119, "product_id": 346, "relevance_note": "Nonino UE Grappa Monovitigno Moscato illustrates single-variety grappa distillation — the artisan expression of pomace distillate described in this reference."},
    {"technique_id": 119, "product_id": 347, "relevance_note": "Fernet-Branca is the canonical Italian amaro — its Alpine herb maceration and bitterness are the defining reference for the digestif category."},
    {"technique_id": 119, "product_id": 348, "relevance_note": "Amaro Montenegro illustrates the lighter, more accessible amaro style — contrasts with Fernet-Branca's intensity for the full Italian digestif spectrum."},

    # Ref 120 — Sherry: Solera, Style Spectrum, Flor Biology
    {"technique_id": 120, "product_id": 356, "relevance_note": "Hidalgo La Gitana Manzanilla is the primary Manzanilla reference — under-flor, Sanlucar-seaside style that directly illustrates flor yeast biology and biologically aged Sherry."},
    {"technique_id": 120, "product_id": 357, "relevance_note": "Gonzalez Byass Tio Pepe Fino is the iconic Fino — the standard reference for biologically aged Sherry and the solera system's application."},
    {"technique_id": 120, "product_id": 358, "relevance_note": "Lustau Los Arcos Amontillado demonstrates the transition from Fino to Oloroso — the biological-to-oxidative aging shift central to Sherry style spectrum."},
    {"technique_id": 120, "product_id": 359, "relevance_note": "Lustau Peninsula Palo Cortado illustrates the enigmatic in-between style — neither pure biological nor oxidative, key to understanding the full Sherry spectrum."},
    {"technique_id": 120, "product_id": 361, "relevance_note": "Equipo Navazos La Bota demonstrates the En Rama unfiltered Sherry movement — extension of the solera system to artisan expression."},

    # Ref 121 — Tempranillo / Rioja Aging Classifications
    {"technique_id": 121, "product_id": 39, "relevance_note": "Tempranillo Reserve illustrates the Reserva tier of Rioja aging classification — the standard benchmark for understanding Crianza/Reserva/Gran Reserva hierarchy."},
    {"technique_id": 121, "product_id": 353, "relevance_note": "Muga Prado Enea Gran Reserva is the canonical Rioja Gran Reserva benchmark — long oak ageing, traditional Tempranillo expression at the apex of the classification."},
    {"technique_id": 121, "product_id": 354, "relevance_note": "Lopez de Heredia Viña Tondonia Gran Reserva is the iconic traditional Rioja reference — its extended aging in American oak directly illustrates the classification's Gran Reserva regulations."},
    {"technique_id": 121, "product_id": 352, "relevance_note": "Dominio de Pingus illustrates the modern single-vineyard Ribera del Duero expression — Tempranillo's extension beyond Rioja described in the regional context."},
    {"technique_id": 121, "product_id": 463, "relevance_note": "Abacela Tempranillo in Oregon demonstrates how Spanish varieties translate globally — extending the Tempranillo narrative beyond Spain."},

    # Ref 127 — Yerba Mate Ceremony
    {"technique_id": 127, "product_id": 468, "relevance_note": "Samoan Ava ceremony parallels yerba mate's shared-vessel tradition — both are communal, bitter herb preparations with ceremonial hierarchy, directly comparable in a cross-cultural service context."},
    {"technique_id": 127, "product_id": 465, "relevance_note": "Tanna Kava embodies the Pacific communal ceremony context analogous to mate circle protocols described in this reference."},
    {"technique_id": 127, "product_id": 467, "relevance_note": "Hawaiian Awa shares the shared-vessel ceremony format with yerba mate — both are prepared communally and consumed without individual cups in traditional settings."},

    # Ref 128 — Ceremonial Cacao
    {"technique_id": 128, "product_id": 472, "relevance_note": "Bafoussam Matango (fermented banana wine) shares the ancestral fermentation and ceremonial context with ceremonial cacao — both are indigenous prepared beverages with deep ritual significance."},
    {"technique_id": 128, "product_id": 467, "relevance_note": "Hawaiian Awa is a ceremonial beverage context that parallels ceremonial cacao — both represent Mesoamerican/Pacific indigenous preparation traditions for guided ceremony use."},
    {"technique_id": 128, "product_id": 465, "relevance_note": "Vanuatu Kava ceremony shares the meditative, ceremony-focused consumption framework with ceremonial cacao described in this reference."},

    # Ref 129 — Barolo and Barbaresco (Communes, MGAs, Modernist/Traditionalist)
    {"technique_id": 129, "product_id": 325, "relevance_note": "Gaja Barbaresco is the definitive modernist expression — early barriques, approachable structure, the catalyst for the Modernist-Traditionalist debate described in this reference."},
    {"technique_id": 129, "product_id": 328, "relevance_note": "Conterno Monfortino is the definitive traditionalist Barolo — extended maceration, large Slavonian oak, Cascina Francia MGA, the counterpoint to Gaja's modernism."},
    {"technique_id": 129, "product_id": 327, "relevance_note": "Giacosa Falletto di Serralunga bridges traditionalism and quality excellence — its Serralunga commune character is essential for MGA commune analysis."},
    {"technique_id": 129, "product_id": 332, "relevance_note": "Roagna Barbaresco Crichet Paje represents traditional Barbaresco — old vines, minimal intervention, long ageing in large cask."},
    {"technique_id": 129, "product_id": 331, "relevance_note": "G.D. Vajra Bricco delle Viole demonstrates La Morra commune terroir — softer, earlier drinking, essential for the commune variation comparison."},

    # Ref 130 — Rioja: Ageing Classification and Alta/Alavesa/Baja Diversity
    {"technique_id": 130, "product_id": 353, "relevance_note": "Muga Prado Enea Gran Reserva from Alta Rioja demonstrates the Alta sub-region's contribution to the Gran Reserva tier."},
    {"technique_id": 130, "product_id": 354, "relevance_note": "Lopez de Heredia Tondonia from Rioja Alta is the canonical sub-region demonstration for the Alta/Alavesa/Baja diversity described in this reference."},
    {"technique_id": 130, "product_id": 39, "relevance_note": "Tempranillo Reserve represents the Reserva tier of the Rioja aging classification system."},
    {"technique_id": 130, "product_id": 352, "relevance_note": "Pingus from Ribera del Duero demonstrates how Tempranillo expresses outside Rioja, providing contrast to the Rioja classification framework."},

    # Ref 133 — Brunello di Montalcino (Sangiovese Grosso / Biondi-Santi Legacy)
    {"technique_id": 133, "product_id": 334, "relevance_note": "Biondi-Santi Brunello Riserva is the subject and founding reference for this entry — the estate that defined Brunello di Montalcino's Sangiovese Grosso expression and legacy."},
    {"technique_id": 133, "product_id": 337, "relevance_note": "Tignanello's Sangiovese-dominant blend provides context for how Sangiovese evolves across Tuscany — the IGT counterpoint to Brunello's DOCG rigour."},

    # Ref 134 — Greek Indigenous Varieties
    {"technique_id": 134, "product_id": 362, "relevance_note": "Domaine Sigalas Santorini Assyrtiko is the flagship Greek indigenous white — its volcanic Santorini terroir and basket-trained vines are central to the native wine renaissance described."},
    {"technique_id": 134, "product_id": 364, "relevance_note": "Kir-Yianni Ramnista Naoussa is the benchmark Xinomavro — northern Greece's indigenous red grape, essential to the Greek variety renaissance covered in this reference."},
    {"technique_id": 134, "product_id": 445, "relevance_note": "Lyrarakis Dafni demonstrates Crete's indigenous variety revival — the Dafni grape is an example of the native wine renaissance beyond the Assyrtiko/Xinomavro flagship varieties."},
    {"technique_id": 134, "product_id": 446, "relevance_note": "Douloufakis Dafnios Red (Kotsifali/Mandilari blend) illustrates Cretan indigenous red varieties — the island's distinct grape diversity within the Greek native wine renaissance."},

    # Ref 135 — Arak, Ouzo, Raki
    {"technique_id": 135, "product_id": 365, "relevance_note": "Barbayanni Blue Label Ouzo is a top-tier Lesbos ouzo — its double-distilled anise and ouzo appellation status directly illustrate the Greek component of the Eastern Mediterranean anise spirit family."},
    {"technique_id": 135, "product_id": 366, "relevance_note": "Plomari Original Ouzo demonstrates the ouzo style spectrum — traditional Lesbos production and the louche dilution service context described in this reference."},
    {"technique_id": 135, "product_id": 368, "relevance_note": "Massaya Arak Silver is the Lebanese Arak reference — its grape spirit base, aniseed distillation, and dilution service protocol are directly covered in this reference."},
    {"technique_id": 135, "product_id": 322, "relevance_note": "Ricard Pastis bridges the Eastern Mediterranean anise family to the Western Mediterranean — demonstrating the pan-Mediterranean distribution of anethole spirits."},

    # Ref 136 — Moroccan Mint Tea Ceremony
    {"technique_id": 136, "product_id": 369, "relevance_note": "Moroccan Atay — Gunpowder Green Tea with Nana Mint is the direct product of this reference — the precise preparation described in the ceremony protocol."},

    # Ref 137 — Turkish Coffee Cezve Technique
    {"technique_id": 137, "product_id": 370, "relevance_note": "Kurukahveci Mehmet Efendi Turkish Coffee is the canonical product for cezve preparation — used in the cultural heritage and hospitality protocol described in this reference."},
    {"technique_id": 137, "product_id": 71, "relevance_note": "Ethiopia Yirgacheffe Washed provides origin context for coffee beans used in Turkish preparation — the trade routes from Ethiopian origin to Ottoman coffee culture."},
    {"technique_id": 137, "product_id": 73, "relevance_note": "House Blend Espresso provides the modern service contrast to Turkish cezve technique — the reference distinguishes traditional from contemporary coffee culture."},
]

def main():
    conn = psycopg2.connect(CONN)
    inserted = 0
    skipped = 0
    failed = 0
    for lnk in LINKS:
        try:
            with conn.cursor() as cur:
                cur.execute(SQL, lnk)
                conn.commit()
                inserted += 1
                print(f"  OK ref={lnk['technique_id']} prod={lnk['product_id']}")
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            skipped += 1
            print(f"  SKIP ref={lnk['technique_id']} prod={lnk['product_id']} (exists)")
        except Exception as e:
            conn.rollback()
            failed += 1
            print(f"  FAIL ref={lnk['technique_id']} prod={lnk['product_id']}: {e}")
    conn.close()
    print(f"\nDone: inserted={inserted}, skipped={skipped}, failed={failed}")

if __name__ == "__main__":
    main()
