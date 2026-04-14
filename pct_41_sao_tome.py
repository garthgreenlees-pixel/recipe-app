import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition='spirits',
    region='São Tomé and Príncipe — São Tomé Island (Cane Spirit and Cocoa Liqueur, Equatorial Terroir)',
    output_dir='.',
    starting_entry=1,
    session_number=43,
    running_total=0
)

session.add_producer({
    'tradition': 'spirits',
    'name': 'ROC — Roça Agostinho Neto Cane Distillery',
    'location': 'Roça Agostinho Neto, São Tomé Island',
    'description': "São Tomé's cane spirits are produced on the island's historic roças — the colonial sugar and cocoa plantation estates that dominated São Tomé's landscape from the 16th to 20th centuries. The Roça Agostinho Neto (formerly Roça Boa Entrada) is one of the largest surviving roça complexes with a functioning agricultural operation, producing both sugarcane aguardente (the local cane spirit) and cocoa products. São Tomé sits almost exactly on the Equator at 0°N and produces both cane spirits (from Portuguese colonial sugarcane culture) and the island's internationally celebrated single-origin dark chocolate, creating a unique pairing of cane distillate and cacao that is rooted in the same plantation soil.",
    'founded': 'Colonial era (18th century); modern production reconstituted post-independence 1975',
    'region': 'São Tomé Island',
    'website': None,
    'verified': False
})

session.add_producer({
    'tradition': 'spirits',
    'name': 'Claudio Corallo — São Tomé Cacao Spirit and Chocolate',
    'location': 'Roça Terreiro Velho, São Tomé Island',
    'description': "Claudio Corallo is an Italian-born chocolate producer based on São Tomé since 1993, operating the Roça Terreiro Velho with both cacao cultivation and fermentation/drying operations on the island, plus finishing on Príncipe Island at Roça Ramadas. Corallo produces what many specialists consider the world's most distinctive single-origin dark chocolate from Forastero cacao grown at 200-450m elevation in the island's volcanic equatorial forest. Corallo has also developed cacao-based spirits and unique 70-80% dark chocolate with cacao nibs and coffee — the complete equatorial terroir expression in confectionery form.",
    'founded': '1993',
    'region': 'São Tomé Island / Príncipe Island',
    'website': 'corallo.st',
    'verified': True
})

session.add_purveyor({
    'name': 'Friis-Holm / Claudio Corallo EU Import / Bittersweet (Toronto)',
    'type': 'importer',
    'description': "Claudio Corallo chocolate is distributed in Europe through specialty importers including Friis-Holm (Denmark). In Canada, Bittersweet chocolate shops in Toronto carry Corallo products. São Tomé cane spirit has no commercial distribution in North America; the chocolate serves as the accessible PCT São Tomé connection for culinary programming.",
    'markets_served': ['EU', 'Canada', 'US'],
    'traditions_carried': ['spirits', 'coffee'],
    'website': None,
    'verified': False
})

session.add_beverage({
    'name': 'São Tomé Aguardente de Cana — Equatorial Roça Cane Spirit, Colonial Atlantic Heritage, Zero-Degree Volcanic Terroir',
    'category': 'spirits',
    'subcategory': 'cane_spirit',
    'origin': 'São Tomé and Príncipe',
    'region': 'São Tomé and Príncipe — São Tomé Island (Cane Spirit and Cocoa Liqueur, Equatorial Terroir)',
    'producer': 'ROC — Roça Agostinho Neto Cane Distillery',
    'alcohol_content': 45.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "São Tomé Island sits at 0°20'N — essentially on the Equator — in the Gulf of Guinea, 250km off the coast of Gabon in the Atlantic Ocean. The island was uninhabited when Portuguese sailors arrived in 1470 and was immediately established as the first sugar-producing colony in sub-Saharan Africa, using enslaved West and Central African agricultural labor to create what became the model for the plantation agricultural system later exported to Brazil and the Caribbean. The volcanic island's extraordinary fertility — equatorial rainfall of 3,000-10,000mm per year on the southern slopes, volcanic basalt and alluvial soils enriched by the Congo River discharge that creates the Gulf of Guinea's unusual oceanographic conditions, and year-round growing temperatures of 24-28°C — made São Tomé one of the most productive agricultural territories in the Portuguese colonial system. Sugarcane cultivation on the island's northern, drier plateau (800-1,200mm annual rainfall) and the plantation roças (estates) created the social and agricultural structure that defines the island to this day. The roça-produced cane spirit is made from fresh-pressed cane juice in the same tradition as Cape Verde's grogue and Martinique's rhum agricole, but on an Equatorial volcanic island that produces the most extreme terroir conditions of any cane spirit producing territory."
    ),
    'production_technique': (
        "São Tomé aguardente de cana is produced by direct pressing of fresh sugarcane cultivated in the roça plantations, fermented with native equatorial yeast (the fermentation character at Equatorial temperatures, 26-30°C year-round, is distinct from temperate or subtropical fermentation — faster completion, higher ester production, more complex fruity character) in open fermentation vessels for 3-5 days. Single pot still distillation at 60-70% ABV final cut; proofed with rainwater (São Tomé's abundant precipitation) to 45% for bottling. The equatorial climate drives extremely rapid ester development during even short rest periods — unaged São Tomé cane spirit has more complex ester character than 2-3 year aged Caribbean rum because the equatorial temperature drives esterification at twice the rate of subtropical production. No systematic aging operation exists on São Tomé currently; the spirit is primarily consumed locally, with small artisanal quantities reaching the EU through specialty channels. The roças operate with rebuilt colonial-era pot stills in some cases, adding to the historical authenticity of the production."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Cape Verde Santiago Grogue (Atlantic island cane spirit, colonial Portuguese heritage)',
            'connection': "São Tomé aguardente and Cape Verde grogue represent the two poles of the Portuguese Atlantic island cane spirit tradition — Cape Verde at 15°N (subtropical) and São Tomé at 0°N (equatorial) — both established under the same colonial agricultural framework, both producing fresh-cane-juice spirits using single pot still distillation, but with dramatically different fermentation and terroir character driven by the extreme difference in temperature and rainfall between the subtropical Atlantic and the equatorial Gulf of Guinea"
        },
        {
            'tradition': 'Martinique Rhum Agricole AOC (French Caribbean, fresh cane, volcanic terroir)',
            'connection': "São Tomé aguardente and Martinique rhum agricole share the fresh-cane-juice distillation tradition and volcanic island terroir, but São Tomé's equatorial location produces fermentation at 6-8°C higher temperature than Martinique's tropical climate — the faster, hotter fermentation produces more complex ester development without the structured floral character of the cooler Martinique fermentation; both are expressions of how volcanic island terroir is transformed by the geography of the trade wind belt"
        }
    ],
    'sensory_profile': {
        'appearance': 'Clear to very pale yellow (slight natural color from equatorial heat and brief cask contact even in unaged expressions); moderate legs at 45% ABV',
        'nose': 'Intense fresh cane and tropical fruit: ripe plantain, fermented sugarcane juice, tropical flower (frangipani), burnt caramel, volcanic mineral note from the basaltic soils — the equatorial fermentation produces an ester intensity that surpasses more recognized cane spirits at comparable ages; distinctive Gulf of Guinea maritime quality from the Atlantic equatorial breeze',
        'palate': 'Full body from the high-ester equatorial fermentation; tropical fruit and fresh cane dominate mid-palate; warm and slightly raw finish at 45% ABV without oak integration; mineral-mineral undertone from the volcanic basalt soils; the finish is shorter than aged expressions but the initial impact is intense',
        'conclusion': 'Raw but complex cane spirit of genuine equatorial terroir character; the reference expression of São Tomé colonial Portuguese agricultural heritage; serves as cultural context entry for PCT programming'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Standard São Tomé Aguardente (unaged, local consumption)',
            'criteria': 'Unaged, roughly distilled cane spirit consumed locally; the baseline category expression; ester-rich but rough and unrefined'
        },
        {
            'tier': 2,
            'tier_name': 'Roça Production Aguardente (artisan pot still)',
            'criteria': 'Single roça production from fresh-pressed cane juice; cleaner distillation than local consumption grade; the benchmark for export-quality São Tomé cane spirit'
        },
        {
            'tier': 3,
            'tier_name': 'Short-Aged São Tomé Aguardente (6-12 months tropical)',
            'criteria': 'Brief cask rest (6-12 months) in tropical equatorial climate; the equivalent of 3-5 years of temperate aging in terms of wood-spirit interaction; shows vanilla and caramel integration while preserving the equatorial ester character'
        },
        {
            'tier': 4,
            'tier_name': 'Roça Reserve (18+ months, collector)',
            'criteria': 'Extended equatorial aging; essentially a curiosity category given the tiny production volume; comparison to 5-7 year Caribbean aged rum in sensory complexity while at 18 months age'
        }
    ],
    'service_intelligence': {
        'temperature': 'Neat at room temperature (20-22°C); the tropical ester complexity opens with warmth; no ice for the premium expressions as dilution suppresses the volcanic terroir character',
        'vessel': 'Small tulip or grappa glass to concentrate the intense equatorial ester aromatics',
        'programme_position': "Spirits course in a PCT-themed tasting menu; exceptional as a pairing digestif with São Tomé dark chocolate (Claudio Corallo's 73% single-origin from the same island), creating the complete equatorial agricultural narrative — cane spirit and cacao from the same roça soil"
    },
    'purveyor_intelligence': {
        'benchmark_producer': 'ROC Roça Agostinho Neto (artisan, limited); Claudio Corallo for the chocolate accompaniment that makes São Tomé accessible in North American restaurant programming',
        'north_america_access': 'São Tomé cane spirit: effectively unavailable; Claudio Corallo chocolate: available in Toronto (Bittersweet) and some specialty chocolate shops in US; the chocolate is the practical São Tomé connection for menu programming',
        'culinary_application': "The São Tomé narrative is the most important cacao origin story in the PCT: the island's cacao was among the first cultivated cacao in Africa, and São Tomé single-origin chocolate is now recognized internationally. Pairing São Tomé 73% dark chocolate (Claudio Corallo) with a comparison of Cape Verde grogue and Caribbean rum creates a complete 'Equatorial Atlantic cane and cacao' tasting experience that is unique in the world"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()

session.switch_region('food', 'São Tomé and Príncipe — Cacao (Forastero Single-Origin, Equatorial Volcanic, Roça Terroir)')

session.add_producer({
    'tradition': 'food',
    'name': 'Claudio Corallo — Príncipe Island Single-Origin 70% Cacao',
    'location': 'Roça Ramadas, Príncipe Island / Roça Terreiro Velho, São Tomé',
    'description': "Claudio Corallo's single-origin chocolate operation on São Tomé and Príncipe is considered by many chocolate specialists to produce the world's most transparent expression of equatorial African cacao terroir. Corallo cultivates Forastero cacao on Príncipe Island (a UNESCO Biosphere Reserve and the smaller, more remote twin to São Tomé) at the Roça Ramadas estate, processes the beans on-site, and finishes the chocolate at his São Tomé facility with minimal additives. The 80% Príncipe dark chocolate contains only cacao and cacao butter — no vanilla, no lecithin, no additional sugars. The flavor profile is the direct expression of Forastero cacao grown in equatorial volcanic forest soils at 200-400m altitude.",
    'founded': '1993',
    'region': 'Príncipe Island, São Tomé and Príncipe',
    'website': 'corallo.st',
    'verified': True
})

session.add_beverage({
    'name': "Claudio Corallo Príncipe Forastero 80% — Equatorial Single-Origin Cacao Tasting Reference, Volcanic Forest Terroir",
    'category': 'food',
    'subcategory': 'single_origin_chocolate',
    'origin': 'São Tomé and Príncipe',
    'region': 'São Tomé and Príncipe — Cacao (Forastero Single-Origin, Equatorial Volcanic, Roça Terreiro Velho)',
    'producer': 'Claudio Corallo — Príncipe Island Single-Origin 70% Cacao',
    'alcohol_content': 0.0,
    'price_tier': 'premium',
    'terroir_origin': (
        "Príncipe Island (UNESCO Biosphere Reserve since 2012) is the smaller, more remote twin to São Tomé in the Gulf of Guinea — at 1°N, even more directly equatorial than São Tomé, covered primarily by equatorial rainforest at 80-90% forest cover, with the Roça Ramadas estate occupying one of the few agroforestry zones on the island. The Forastero cacao cultivated on Príncipe is the oldest continuously cultivated cacao strain in Africa, introduced to the island by the Portuguese from Brazil in the 18th century and allowed to adapt to the equatorial volcanic conditions over 200+ years without significant genetic intervention — creating a genetically distinct Príncipe Forastero with different aromatic character from the same variety grown in West Africa, South America, or Southeast Asia. The volcanic soils at 200-400m on Príncipe are extremely rich in minerals from the ancient basaltic lava flows that built the island, and the equatorial forest canopy provides natural shade for the cacao, mimicking the wild shade-grown conditions of cacao's origin in the Mesoamerican rainforest understory. Annual rainfall of 7,000-10,000mm on Príncipe (among the highest in Africa) creates the humidity conditions that allow the fermentation of cacao pulp to produce the complex flavor precursors that distinguish Corallo's chocolate from any other African single-origin."
    ),
    'production_technique': (
        "Corallo harvests Forastero cacao pods by hand at precise ripeness from the Roça Ramadas estate, assessing each pod individually for color change from green to yellow-orange (the external indicator of internal pulp fermentation readiness). The cacao beans are extracted from pods, pulped, and fermented in wooden boxes on the estate for 4-6 days — the equatorial heat (26-30°C year-round) drives the fermentation at higher intensity than Caribbean or South American production, producing the complex aldehyde and ester precursors that develop into the final flavor during roasting. After fermentation, the beans are sun-dried on elevated drying racks for 7-10 days in the equatorial sun before being shipped to Corallo's processing facility in São Tomé for roasting, winnowing, and grinding. Corallo uses very low roasting temperatures (below 100°C in most stages) to preserve the fragile floral and fruity volatile compounds developed during fermentation — the antithesis of the high-heat roasting used for commodity chocolate. The resulting 80% chocolate (cacao, cacao butter, no additional ingredients) is conched for 48-72 hours to develop smoothness without destroying the fermentation-derived complexity. The extraordinary result is a dark chocolate where the terroir of Príncipe's equatorial volcanic forest is the only flavor — no vanilla to mask, no sugar to sweeten, no lecithin to smooth: pure Forastero from one of the world's most remote and unspoiled cacao terroirs."
    ),
    'cross_tradition_parallels': [
        {
            'tradition': 'Kopi Luwak Sumatra / Ethiopia Yirgacheffe natural (extreme terroir single-origin fermented beverage)',
            'connection': "Corallo Príncipe 80% and Ethiopia Yirgacheffe natural-process coffee share the category of single-origin fermented agricultural products where the production process minimizes intervention to let the equatorial terroir speak directly — both rely on natural fermentation (cacao pulp fermentation, coffee cherry fermentation during natural processing) as the primary flavor development mechanism, and both achieve their distinctive character by allowing the equatorial microflora to transform the raw agricultural product with minimal control or addition"
        },
        {
            'tradition': 'São Tomé Aguardente de Cana (same island, same roça agricultural heritage)',
            'connection': "Corallo Príncipe cacao and São Tomé aguardente represent the two products of the same equatorial colonial plantation system — sugarcane and cacao were cultivated side by side on the roças using the same labor and in the same volcanic soils; pairing the cane spirit with the dark chocolate creates the complete São Tomé colonial agricultural narrative that is both historically authentic and gastronomically compelling"
        }
    ],
    'sensory_profile': {
        'appearance': 'Very dark brown with reddish undertones; matte surface (no tempering additives); snaps cleanly with a sharp crack indicating proper temper from pure cacao butter',
        'nose': 'Dry assessment: fermented fruit (ripe fig, dark cherry, dried plum), slightly smoky, volcanic mineral, tropical flower undertone — the Forastero variety shows more dark fruit and earthy character than Trinitario or Criollo, but the Príncipe terroir adds floral complexity not typical of West African Forastero',
        'palate': 'Very high intensity at 80% cacao; bitter entry (the Forastero variety characteristic) immediately followed by dark fruit (black cherry, dried fig), volcanic mineral mid-palate, floral element (frangipani, jasmine) in the mid-finish, very long finish with bitter dark chocolate and mineral persistence; the complexity develops over 2-3 minutes in the mouth as the cacao butter melts and releases the volatile compounds; no artificial sweetness or vanilla to divert from the pure terroir expression',
        'conclusion': 'The most transparent expression of equatorial African Forastero cacao terroir available; serves both as culinary ingredient and as a tasting reference for PCT programming; quality: highest available in the single-origin Forastero category'
    },
    'quality_hierarchy': [
        {
            'tier': 1,
            'tier_name': 'Commodity São Tomé Cacao (70% industrial blend)',
            'criteria': "Mass-produced 70% São Tomé chocolate using commodity-grade cacao with vanilla and lecithin additions; available from major European chocolate manufacturers who source São Tomé cacao; drinkable as a category reference but lacking the terroir precision of Corallo's production"
        },
        {
            'tier': 2,
            'tier_name': "Corallo São Tomé 75% (island blend, not Príncipe single estate)",
            'criteria': "Corallo's accessible island expression using São Tomé (not Príncipe) cacao; the entry to Corallo's range with the volcanic mineral character of the island without the extreme intensity of the Príncipe estate"
        },
        {
            'tier': 3,
            'tier_name': "Corallo Príncipe 80% (single estate, minimal intervention)",
            'criteria': "The benchmark Corallo expression from Príncipe Island Roça Ramadas; 80% cacao with no additions; the highest expression of equatorial volcanic Forastero cacao currently in commercial production"
        },
        {
            'tier': 4,
            'tier_name': "Corallo Príncipe Cacao Nibs with Coffee (terroir combination)",
            'criteria': "Corallo's unique expression combining Príncipe cacao with São Tomé coffee — the complete equatorial island terroir in a single product; available only directly from Corallo or specialist import"
        }
    ],
    'service_intelligence': {
        'temperature': 'Serve at room temperature (20-22°C) for tasting assessment; cold from refrigerator will suppress the volatile floral-fruity compounds; warm hands during handling will melt the pure cacao butter and release the full aroma profile',
        'vessel': 'Break into 3-5g pieces for tasting; allow to melt slowly in the mouth rather than chewing to allow the full time-released flavor development',
        'programme_position': "Final course of a PCT tasting menu — the São Tomé chocolate is the endpoint of the colonial agricultural trail; pair with Madeira Malmsey or a 10-year Bual (the Madeira-chocolate pairing is historically documented in 19th-century colonial Portuguese dining records) or with the São Tomé aguardente as the complete island narrative"
    },
    'purveyor_intelligence': {
        'benchmark_producer': "Claudio Corallo — the reference producer; Menakao (Madagascar) for comparison of Forastero from a different Indian Ocean volcanic island; Pacari (Ecuador) for comparison of South American Forastero heritage",
        'north_america_access': 'Bittersweet (Toronto) carries Corallo; specialty chocolate retailers in US (Mast Brothers NY, Compartés LA) occasionally stock; direct order from corallo.st ships to North America',
        'culinary_application': "The PCT chocolate service narrative: São Tomé was the source of the cacao that supplied the Portuguese and Spanish colonial courts in Lisbon and Madrid; the chocolate we know today was first a Portuguese colonial agricultural product before it became a global commodity; pairing Corallo Príncipe 80% with a Bual Madeira and describing the 16th-century colonial trade route creates one of the most substantive food history narratives possible in a tasting menu context"
    },
    'price_trajectory': 'rising'
})

session.commit_batch()
session.finish()
