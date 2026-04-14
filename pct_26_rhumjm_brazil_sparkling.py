import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='Martinique — Le Marigot, Macouba (Rhum JM AOC, Northern Atlantic Coast, Volcanic Basalt)',
    output_dir='.',
    starting_entry=1,
    session_number=27,
    running_total=86
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'Distillerie J.M.',
    'location': 'Macouba, northern Martinique, French West Indies',
    'description': 'Established 1845 on the northern Atlantic coast of Martinique near Macouba — the most rugged and isolated commune on the island, sitting in the shadow of Mount Pelée (the active stratovolcano that erupted in 1902 and destroyed Saint-Pierre, then Martinique\'s cultural capital). The distillery was founded by Crassous de Médeuil and acquired by Gustave de Marigot in the 1880s, whose initials J.M. (Jean-Marie) became the house name. The northern Atlantic coast terroir where J.M. grows its cane is the most climatically extreme on Martinique: higher rainfall (2,500–3,500mm annually vs 1,800–2,200mm for southern Atlantic and 1,200–1,600mm for Leeward coast), volcanic basalt soils from the Pelée geological system, and persistent Atlantic trade wind exposure that slows cane maturation and concentrates terroir character. J.M. is one of seven distilleries still producing under the Rhum Agricole Martinique AOC — the only rum appellation in the world — and maintains the most extreme terroir differentiation within the AOC due to its northern volcanic position.',
    'founded': '1845',
    'region': 'Macouba, northern Martinique',
    'website': 'rhum-jm.com',
    'verified': True
})

session.add_purveyor({
    'name': 'Rhum Agricole Selections — USA / Caribbean Spirit Imports Canada',
    'type': 'importer',
    'description': 'J.M. is imported to the US through Maison Ferrand / Plantation Rum distribution network (following LMDW Spirits\' acquisition of J.M. in 2019) and direct state distribution in key markets. In Canada through private import and select LCBO and BCLDB listings. The J.M. Gold (VO) is the most widely distributed expression; the J.M. XO and Vintage releases are allocated through specialist spirits retailers.',
    'markets_served': ['US', 'Canada', 'UK', 'France', 'EU'],
    'traditions_carried': ['spirits'],
    'website': 'rhum-jm.com',
    'verified': False
})

session.add_beverage({
    'name': 'Rhum J.M. AOC Martinique VO — Northern Volcanic Basalt, Atlantic Macouba Cane Spirit',
    'category': 'spirits',
    'subcategory': 'rum_agricole',
    'origin': 'France',
    'region': 'Macouba, northern Martinique, French West Indies',
    'producer': 'Distillerie J.M.',
    'alcohol_content': 50.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'The J.M. estate occupies the slopes immediately below Mount Pelée — the active stratovolcano at the northern tip of Martinique whose 1902 eruption (the deadliest volcanic event of the 20th century) destroyed the city of Saint-Pierre and killed 30,000 people, preserving the rum barrels in Guérin\'s Distillery (predecessor to Depaz) under ash that protected them for decades. The agricultural terroir surrounding J.M.\'s Macouba distillery sits on young basaltic volcanic soils derived from Pelée\'s most recent geological activity — soils that are mineralogically richer in iron, magnesium, and potassium than the older, more weathered sedimentary soils of central and southern Martinique. Annual rainfall at Macouba averages 2,500–3,500mm — among the highest in Martinique — from the persistent northeastern Atlantic trade winds that dump moisture on the windward northern slopes before descending drier onto the Leeward coast. This combination of mineral-rich volcanic basalt, high rainfall, and cool Atlantic wind exposure produces cane of unusual aromatic complexity: the stress of wind exposure and high moisture drives the plant to concentrate secondary metabolites in the stalk, which translate directly to the rum\'s flavor profile. J.M.\'s cane varieties include both the dominant POJ 2878 and several heirloom cultivars maintained on the estate specifically for their aromatic contribution — the northern basalt terroir is perceptible as a distinct mineral-volcanic signature in the finished rhum, differentiating it from the cleaner, fresher profiles of southern Martinique producers like Clément.'
    ),
    'production_technique': (
        'J.M. harvests fresh sugar cane by hand and machine on its northern Macouba slopes from February to June, crushing within 4 hours of harvest to preserve the volatile aromatic compounds that degrade rapidly after cutting — the fundamental discipline of rhum agricole that distinguishes it from molasses-based rum. Fresh cane juice is analyzed for Brix (targeting 14–18° depending on cane variety and harvest date) and transferred to stainless steel fermentation tanks at 30–32°C. A domesticated Saccharomyces cerevisiae culture descended from J.M.\'s 1845 house yeast is added to initiate fermentation, which runs 24–36 hours — the standard AOC maximum fermentation time for rhum agricole white and short-aged expressions. The fast fermentation preserves the fresh cane aromatics while allowing sufficient ester development from yeast metabolism. Distillation occurs in a Créole column still (a single-column continuous still specific to AOC Martinique, with 7–15 plates depending on the house style) at 65–75% ABV — the AOC minimum for column distillation. J.M. takes a more concentrated cut than some Martinique houses, retaining more heads aromatics to build the volcanic mineral complexity that defines the house style. The VO (Vieux Orange — meaning "aged 3 years or more") is aged in 180-litre ex-bourbon American oak barrels in a tropical warehouse on the Macouba property, where the hot-humid aging environment accelerates barrel interaction and angel\'s share (8–12% per year in tropical Martinique vs 2% in Scotland). Diluted to 50% ABV before bottling with Macouba spring water.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Neisson AOC Martinique (same island, different terroir expression)',
            'connection': 'J.M. and Neisson are the most direct within-AOC contrast: J.M. from volcanic northern basalt in the Pelée shadow at 2,500+ mm rainfall, Neisson from western Leeward coast in drier conditions — the same AOC production rules applied to fundamentally different volcanic microclimates produce dramatically different rhum character: J.M.\'s mineral volcanic depth versus Neisson\'s tropical fruity brightness'
        },
        {
            'tradition': 'Armagnac Bas-Armagnac (black sand volcanic terroir, direct terroir expression)',
            'connection': 'J.M.\'s terroir-specificity — the volcanic basalt of Macouba embedded in the VO\'s mineral character — mirrors the way Bas-Armagnac\'s specific sand-and-clay black soil (boulbènes) imprints directly on the Armagnac\'s flavor; both represent agricultural spirits where the geological substrate is legible in the glass rather than obscured by production technique'
        },
        {
            'tradition': 'Islay single malt whisky (volcanic island, maritime extreme)',
            'connection': 'J.M. in Macouba and Laphroaig on Islay both represent island spirit production in the shadow of geological and maritime extremity — the volcanic presence of Pelée for J.M., the peat bogs and Atlantic gales for Islay — both producing spirits of distinctive character that derive as much from the island\'s physical nature as from the production recipe'
        }
    ],
    'sensory_profile': {
        'appearance': 'Warm golden amber from tropical aging in ex-bourbon oak; clear and brilliant; medium viscosity at 50%; the color is a deeper, more saturated amber than southern Martinique producers at the same age from the higher-density tropical barrel interaction',
        'nose': 'Complex and layered: banana flambé, vanilla from American oak, volcanic mineral (iron, wet basalt), roasted coconut, dried tropical fruit (mango, papaya), light caramel — the northern volcanic terroir is unmistakable as a mineral depth underlying the fruit richness; more structured and mineral than southern Martinique producers',
        'palate': 'Full body, powerful at 50%, balanced tropical fruit and mineral-volcanic mid-palate, American oak vanilla integration without woodiness, long finish with basalt mineral and dried mango — the northern Martinique character shows as a firmer, more mineral-structured framework compared to the rounder, fruitier southern house styles'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'J.M. Blanc (Unaged, 50%)',
            'criteria': 'The white rhum agricole expression — the base spirit immediately after distillation, showing the raw northern basalt cane character without oak modification; used in Ti\' Punch and Daiquiri applications'
        },
        {
            'tier': 2,
            'tier_name': 'J.M. VO (3-year Tropical Aged)',
            'criteria': 'The benchmark J.M. expression: 3 years minimum in ex-bourbon oak, 50% bottling strength — the most internationally distributed J.M. product and the signature demonstration of northern volcanic Martinique character'
        },
        {
            'tier': 3,
            'tier_name': 'J.M. XO (6+ year)',
            'criteria': 'Extended tropical aging showing how the basalt mineral complexity integrates with oak tannin over time; 45% bottling strength for broader accessibility; the house signature at its most refined pre-vintage expression'
        },
        {
            'tier': 4,
            'tier_name': 'J.M. Millésime (Single Vintage, Cask Strength)',
            'criteria': 'Specific harvest year bottlings at cask strength (typically 42–58% depending on vintage and aging duration), showing the annual variation in northern Martinique cane character — available through allocation to specialist retailers and premium restaurants'
        }
    ],
    'service_intelligence': {
        'temperature': 'Neat at 20–22°C for full aromatic expression; Ti\' Punch service at room temperature with a single lime disk and small cane syrup addition — the classic Martinique serving tradition that respects the rhum\'s terroir character; avoid diluting too much which masks the mineral volcanic signature',
        'vessel': 'Ti\' Punch: small rock glass with a single lime peel disk; Neat: tulip glass or white wine glass to capture the layered aromatics; Old Fashioned: wide rocks glass with single large ice block; the mineral character benefits from a clean, neutral-taste glass',
        'ti_punch_philosophy': 'The Ti\' Punch protocol for J.M. VO: squeeze a small disk of lime rind (not juice) into a small glass, add 5ml cane syrup, add 45ml J.M. VO at room temperature — the acid, sugar, and rhum reach equilibrium without dilution from ice; each person adjusts the balance at table ("chacun prépare sa mort" — each prepares their own death)'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Distillerie J.M. — VO expression is the benchmark for northern volcanic Martinique rhum agricole character',
        'north_america_access': 'J.M. widely distributed through Plantation Rum network in US: Total Wine, BevMo (CA), Total Beverage (mid-Atlantic); in Canada through select LCBO and BCLDB listings plus private import; The Cocktail Kingdom (NYC) stocks full J.M. range',
        'culinary_application': 'J.M. VO\'s basalt mineral character creates an exceptional pairing with dark chocolate preparations where the volcanic mineral note resonates with the cacao\'s iron character; outstanding in banana foster where the banana note in the rhum merges with the caramelized banana preparation; used as a Ti\' Punch at the table in Caribbean restaurants where the rhum is part of the dining ritual rather than a separate bar program'
    },
    'price_trajectory': 'stable'
})

session.commit_batch()

session.switch_region('wine', 'Brazil — Serra Gaúcha (Vale dos Vinhedos DOCG, Bento Gonçalves, Espumante)')

session.add_producer({
    'tradition': 'wine',
    'name': 'Cave Geisse — Pinto Bandeira, Serra Gaúcha',
    'location': 'Pinto Bandeira, Rio Grande do Sul, Brazil',
    'description': 'Mario Geisse and family produce Brazil\'s finest traditional method sparkling wines in the Pinto Bandeira subregion of Serra Gaúcha — the sub-appellation with the highest elevation (750–800m) and coolest temperatures in the Rio Grande do Sul wine region. Geisse, a Chilean-Brazilian winemaker who trained in Spain and France, established Cave Geisse in 1979 specifically to produce premium sparkling wine from Chardonnay and Pinot Noir in the cooler, higher-altitude portions of Serra Gaúcha that other producers found too challenging for still wine. The Cave Geisse Espumante Brut Nature is produced by the méthode champenoise (traditional method with riddling and dégorgement in-house) and has achieved international recognition as one of the finest New World traditional method sparkling wines, regularly competing with Champagne in international comparative tastings.',
    'founded': '1979',
    'region': 'Pinto Bandeira, Rio Grande do Sul, Brazil',
    'website': 'cavegeisse.com.br',
    'verified': True
})

session.add_beverage({
    'name': 'Cave Geisse Espumante Brut Nature — Pinto Bandeira Serra Gaúcha, Italian Descent Methode Champenoise',
    'category': 'wine',
    'subcategory': 'sparkling_wine',
    'origin': 'Brazil',
    'region': 'Serra Gaúcha, Rio Grande do Sul, Brazil',
    'producer': 'Cave Geisse — Pinto Bandeira, Serra Gaúcha',
    'alcohol_content': 12.0,
    'price_tier': 'premium',
    'terroir_origin': (
        'Serra Gaúcha — the mountainous wine region of Rio Grande do Sul state in southern Brazil — represents the most culturally dense Portuguese colonial beverage origin in the Americas after the obvious Lusophone tradition: the region was settled by Italian immigrants (primarily from Veneto and Trento provinces) brought to Brazil by the Portuguese colonial government from 1875 onward to populate the southern highland after abolition reduced the plantation labor supply. These Italian settlers brought Vitis vinifera cultivars (Barbera, Moscato, Trebbiano, Malvasia) that struggled in the subtropical humidity but acclimated across generations — the hybrid varieties developed in Serra Gaúcha to survive the high rainfall (1,800–2,200mm annually) became the basis for a distinctive Brazilian wine culture. The Portuguese colonial framework — land distribution, infrastructure, legal framework — enabled Italian agricultural settlement that produced an inadvertent vine-growing tradition, creating what is today Brazil\'s most important fine wine region. Pinto Bandeira, where Cave Geisse operates, sits at 750–800m elevation at the northern edge of Serra Gaúcha — cooler than the Bento Gonçalves valley floor by 5–7°C, with granitic sandy soils and significantly lower humidity than lower elevations. The altitude and lighter soils produce slower cane maturation and preserve the acidity essential for sparkling wine production — a terroir insight that Mario Geisse identified in 1979 when Pinto Bandeira was undifferentiated from the broader Serra Gaúcha wine zone.'
    ),
    'production_technique': (
        'Cave Geisse produces its Brut Nature from approximately 70% Chardonnay and 30% Pinot Noir grown on the Pinto Bandeira estate at 750–800m elevation. Harvest occurs in January–February (Southern Hemisphere summer) at carefully monitored sugar-to-acidity ratios: Geisse targets 11–12° Brix (relatively low by Brazilian standards) and 7–8 g/L total acidity for the sparkling wine base — a balance that would be unacceptable for still wine but ideal for the secondary fermentation required in traditional method sparkling. The base wines are fermented in stainless steel at 12–14°C with selected Champagne yeasts (Geisse uses French Champagne yeast cultures rather than Brazilian indigenous yeasts, maintaining the méthode champenoise integrity). Tirage (second fermentation in bottle) occurs with a measured addition of liqueur de tirage (sugar + yeast) in early autumn, targeting 6 atmospheres of natural carbonation. The bottles undergo 36+ months of sur lies aging in Geisse\'s underground cellar — significantly longer than required by Brazilian legislation and comparable to Champagne non-vintage minimums. Riddling occurs by hand on traditional pupitres (A-frame riddling racks) — one of the very few South American producers maintaining manual riddling rather than mechanized gyropalettes. Dégorgement by hand removes the spent yeast plug; Brut Nature receives no dosage (zero added sugar), allowing the Pinto Bandeira terroir acidity to determine the final balance. The combination of extended lees aging and zero dosage produces a sparkling wine of austere precision that communicates the Brazilian highland terroir without sweetness masking.'
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Champagne Blanc de Blancs (Chardonnay-dominant, mineral precision)',
            'connection': 'Cave Geisse Brut Nature occupies the same technical and philosophical category as Champagne Blanc de Blancs — long lees aging, zero dosage, Chardonnay-driven precision — but from an altitude-cooled Brazilian granite soil rather than Champagne\'s chalk; the granitic mineral signature of Pinto Bandeira versus the chalk-mineral signature of Le Mesnil-sur-Oger represents two different geological expressions of the same winemaking philosophy'
        },
        {
            'tradition': 'Italian Franciacorta DOCG (Italian immigrant heritage connection)',
            'connection': 'Cave Geisse traces a direct cultural line to Franciacorta: both regions were shaped by Italian immigrant winemaking families (Cave Geisse by Veneto/Trento settlers, Franciacorta by local Lombard families) who applied traditional method sparkling techniques to local terroir, producing distinctive sparkling wine identities independent of Champagne\'s dominance'
        },
        {
            'tradition': 'Vinho Verde Espumante (Portuguese colonial territory, Atlantic minerality)',
            'connection': 'Both Cave Geisse and Vinho Verde Espumante represent the tradition of high-acidity, lighter-alcohol sparkling wines produced in Atlantic-influenced or altitude-cooled Portuguese colonial territories — Vinho Verde in northwestern Iberia and Serra Gaúcha in southern Brazil both owe their sparkling wine potential to humidity and cool temperatures that preserve natural acidity in grapes'
        }
    ],
    'sensory_profile': {
        'appearance': 'Pale golden with persistent fine mousse (3mm bubble stream from well-maintained traditional method carbonation); brilliant clarity; the color is slightly deeper than Champagne non-vintage from the Pinto Bandeira granite soil mineral influence',
        'nose': 'Fresh brioche and autolytic yeast from 36+ months lees, green apple, citrus pith, white flowers, subtle toasted almond from extended sur lies — the traditional method character is unmistakable; the granitic mineral note appears as a clean stone-water freshness underneath the autolytic complexity',
        'palate': 'Fine-beaded mousse, high acidity from zero dosage, autolytic complexity mid-palate, clean citrus fruit, mineral finish with granite freshness — the Brut Nature zero dosage means the wine\'s balance depends entirely on the vintage\'s natural acidity, which the Pinto Bandeira altitude consistently delivers'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Cave Geisse Brut (with dosage)',
            'criteria': 'The gateway expression with 4–6 g/L dosage softening the granite mineral austerity — most widely distributed internationally, accessible to those finding Brut Nature too dry'
        },
        {
            'tier': 2,
            'tier_name': 'Cave Geisse Brut Nature',
            'criteria': 'Zero dosage, 36+ months sur lies, manual riddling — the benchmark expression of Pinto Bandeira terroir precision and the wine most frequently compared to Champagne in international tastings'
        },
        {
            'tier': 3,
            'tier_name': 'Cave Geisse Millesimado (Vintage)',
            'criteria': 'Single-vintage declarations in outstanding years (lower rainfall, ideal temperature balance), extended 48+ months sur lies — limited production showing the specific Serra Gaúcha growing season character in individual harvest years'
        },
        {
            'tier': 4,
            'tier_name': 'Cave Geisse Centenário (Reserve Blend)',
            'criteria': 'Multi-vintage reserve blend incorporating perpetual reserve wines (solera-style) from the Geisse family\'s continuous production since 1979 — representing the deepest expression of the house style and the only South American sparkling wine with true multi-generational complexity'
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at 6–8°C — standard sparkling wine serving temperature; do not serve below 5°C which flattens the autolytic complexity and granite mineral character; allow to rise to 10°C in the glass over 20 minutes to fully appreciate the lees-derived breadth',
        'vessel': 'White tulip flute or Champagne tulip (not the wide coupe which disperses mousse too quickly); or a standard white wine glass in the Burgundy format for extended nosing sessions — the autolytic complexity benefits from the oxygen of a larger vessel',
        'service_philosophy': 'Position Cave Geisse Brut Nature as the "Champagne alternative with Brazilian provenance narrative" on restaurant wine lists — the Portuguese colonial immigration story (Veneto Italians in a Portuguese colonial land grant system) creates a compelling cross-cultural provenance narrative that connects to the Lusophone PCT tradition while celebrating Brazilian cultural synthesis'
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'Cave Geisse — the international benchmark for Brazilian traditional method sparkling wine, and the most internationally recognized Brazilian wine producer',
        'north_america_access': 'Cave Geisse available through specialty wine importers in US (Vias Imports, Brazilian Wine Association programs); in Canada through LCBO by special order and private import; not yet widely listed in BCLDB but available through private import to BC restaurants',
        'culinary_application': 'Cave Geisse Brut Nature is exceptional with fresh chèvre and Dungeness crab where the granite mineral resonates with ocean minerality and the autolytic complexity adds depth; outstanding as an aperitif sparkling at multicourse Brazilian-influenced dinners; the Brazilian cultural narrative (Italian immigrant × Portuguese colonial framework × subtropical granite terroir) is one of the most compelling beverage provenance stories available to PNW restaurant programs'
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
