#!/usr/bin/env python3
# PCT-16: Timor-Leste Coffee Depth + Cape Verde Grogue Depth + Sao Tome Cacao Depth
# Running total entering: 66
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="coffee",
    region="Southeast Asia — Timor-Leste (Timor Hybrid, Mt Ramelau)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=17,
    running_total=66
)

session.add_producer({
    "tradition": "coffee",
    "name": "Cooperativa Cafe Timor (CCT)",
    "location": "Aileu, Timor-Leste",
    "description": "Founded 1994 with USAID support after the Indonesian occupation; "
        "now 23,000+ farmer families in the cooperative network. "
        "The largest cooperative coffee producer in East Asia and "
        "the primary exporter of Timor-Leste specialty coffee. "
        "CCT was critical to the post-independence economic recovery. "
        "Their Timor-Leste Premium is the reference commercial expression; "
        "the Organic/Fair Trade certification is the oldest in Southeast Asian coffee.",
    "founded": "1994",
    "region": "Timor-Leste (East Timor)",
    "website": "https://www.ccteaste.com",
    "verified": True
})

session.add_producer({
    "tradition": "spirits",
    "name": "Destilaria Fogo (SOGEI)",
    "location": "Fogo Island, Cape Verde",
    "description": "The primary formal producer of Grogue on Fogo Island — "
        "the volcanic island at the centre of Cape Verde's rum-like spirit tradition. "
        "The Fogo volcano (Pico do Fogo, 2,829m) is one of the world's most active "
        "and erupted most recently in 2014-2015, destroying the main village of Chã das Caldeiras. "
        "SOGEI produces Grogue from sugarcane grown on the volcanic flanks of Pico do Fogo "
        "at 800-1,400m altitude.",
    "founded": "1990",
    "region": "Fogo Island, Cape Verde",
    "website": "https://www.cvgrogue.com",
    "verified": True
})

session.add_purveyor({
    "name": "Equal Exchange Coffee (US Coop)",
    "type": "fair_trade_importer",
    "description": "Worker-owned cooperative importer based in Massachusetts. "
        "The primary US fair trade importer of Cooperativa Cafe Timor coffee. "
        "Equal Exchange was founded in 1986 on fair-trade-before-it-was-branded principles.",
    "markets_served": ["US", "nationwide_US"],
    "traditions_carried": ["coffee"],
    "website": "https://www.equalexchange.coop",
    "verified": True
})

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "timor leste arabica robusta hybrid altitude forest",
    "region": "Southeast Asia — Timor-Leste (Timor Hybrid, 1400-1800m)",
    "name": "Timor-Leste Single-Origin — Timor Hybrid Variety, Post-Independence Recovery Coffee",
    "terroir_origin": (
        "Timor-Leste (East Timor) produces one of the world's most historically "
        "significant coffees from a botanical perspective: the Timor Hybrid, "
        "a natural arabica-robusta cross discovered in Timor-Leste in the 1920s-1940s "
        "under Portuguese colonial oversight. "
        "The Timor Hybrid (HdT — Hibrido de Timor) is significant globally because "
        "it is the only known natural arabica-robusta cross to occur spontaneously — "
        "and its disease-resistant genetics have been used to develop virtually every "
        "commercially important coffee variety resistant to coffee leaf rust (CLR) "
        "since the 1970s. Colombia's Castillo, Costa Rica's Catimor, "
        "Honduras's Lempira — all carry Timor Hybrid genetics. "
        "The irony: Timor-Leste, the origin of the world's CLR-resistant genetics, "
        "still grows the original landrace under forest shade at high altitude "
        "while the rest of the world grows derived varieties. "
        "Terroir: Mt Ramelau (2,963m, highest peak in Timor-Leste) and the "
        "Ermera and Aileu districts at 1,400-1,800m. "
        "Forest-garden cultivation: agroforestry system under shade trees; "
        "the oldest coffee trees date to the Portuguese colonial planting of the 1800s. "
        "Volcanic soils: basalt-derived clay, high potassium, high organic matter. "
        "The PCT connection: Portuguese colonial administration planted the original "
        "coffee gardens in Timor-Leste starting in the 1880s. "
        "These gardens survived the Indonesian occupation (1975-1999) "
        "by producing coffee even when the farmers could not sell it."
    ),
    "production_technique": (
        "Timor-Leste production (CCT cooperative model): "
        "Harvest: manual selective picking by smallholder farmers; "
        "each family farms 1-2 hectares maximum on steep mountain terrain. "
        "The CCT network: 23,000+ farmer families across 17 districts; "
        "CCT provides technical training, organic certification maintenance, "
        "and fair-trade price guarantees. "
        "Processing: wet-hulled (Giling Basah) processing is the dominant method "
        "— the same method as Sumatran coffee (a shared colonial-era technique). "
        "Wet-hulled: cherry pulped; fermented 24-36 hours; hulled at high moisture "
        "(40-50% vs 12% for standard wet processing); then sun dried. "
        "The wet-hull process creates the distinctive Timor-Leste character: "
        "full body, low acidity, earthy-herbal quality, mushroom and dark chocolate. "
        "Some farms are transitioning to washed processing for higher market premiums. "
        "Natural/sun-dry: highest altitude farms producing for specialty export. "
        "Organic certification: all CCT production is certified USDA Organic "
        "and Fair Trade — the oldest organic certification in Southeast Asian coffee. "
        "Independence context: after 1999 independence, CCT rebuilt from 1,200 "
        "to 23,000 farmer families in 25 years."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "coffee",
            "beverage": "Sumatra Mandheling (wet-hulled, north Sumatra)",
            "connection": (
                "Both are wet-hulled coffees from former Portuguese (Timor) and "
                "Dutch (Sumatra) colonial territories in the same maritime region. "
                "The wet-hull process is the shared colonial-era technique. "
                "Sumatra is heavier, earthier, more tobacco; Timor-Leste is "
                "cleaner, more herbal, brighter acidity at altitude."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Ethiopia Yirgacheffe Washed (forest garden, shade grown)",
            "connection": (
                "Both are high-altitude, forest-garden coffees grown under shade trees "
                "in smallholder agroforestry systems. The comparison shows how altitude "
                "and shade create similar production conditions in Ethiopia and Timor-Leste "
                "despite the geographic and varietal differences."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Papua New Guinea Sigri (high altitude, wet process)",
            "connection": (
                "Adjacent island nation; both in the Pacific island arc. "
                "Both grow Bourbon and Typica varieties at high altitude; "
                "both have large smallholder cooperative networks. "
                "The Timor-PNG comparison opens the Pacific corridor "
                "in the PCT beverage education context."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Hawaii Kona Extra Fancy (volcanic Pacific island coffee)",
            "connection": (
                "PCT×PMT intersection: both Timor-Leste and Kona are Pacific volcanic island coffees "
                "with Portuguese colonial planting lineage. "
                "Both grow on volcanic soils; both have low production volumes "
                "relative to global demand. The Pacific coffee corridor from Timor "
                "to Hawaii traces the same Portuguese-Atlantic trade routes "
                "that the PCT documents."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Dark brown; wet-hulled coffee produces oils that create a heavier crema on espresso and a darker filter brew colour",
        "nose": "Earthy-herbal (forest floor, dried mushroom, dried herb), dark chocolate, cedar, faint tobacco; the wet-hull processing creates the earthy character that defines the origin",
        "palate": "Full body; the wet-hull process creates the characteristic low acidity and heavy body; dark chocolate mid-palate; the herbal mushroom character is most prominent in filter brewing",
        "texture": "Dense and oily; the highest body-to-acidity ratio of any origin in the PCT beverage collection; the wet-hull oils coat the palate",
        "finish": "Medium length (30-40 seconds); dark chocolate and cedar; the earthy note resolves cleanly at the end; the Timor Hybrid genetics give a cleaner finish than standard robusta-influenced coffees",
        "conclusion": "The most historically significant variety in global coffee genetics — the origin of every CLR-resistant coffee variety in production today"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "CCT Timor-Leste Washed Single-Farm (specialty export)",
            "criteria": "Washed processing; single farm sourcing; high altitude parcels (1600-1800m); "
                "SCA score 84+; the cleanest expression of Timor Hybrid terroir without wet-hull earthiness",
            "markers": "CCT Specialty Export; US ~$22-30/250g via specialty roasters; BC: specialty roasters only"
        },
        {
            "tier": 3,
            "tier_name": "CCT Timor-Leste Premium Organic (cooperative blend)",
            "criteria": "Certified organic and fair trade; wet-hulled; cooperative-wide blend; "
                "the reference expression for the origin character at premium pricing",
            "markers": "CCT Premium; BC ~$18-24/250g; US ~$16-22/250g; Equal Exchange distribution"
        },
        {
            "tier": 2,
            "tier_name": "Equal Exchange Timor-Leste (standard organic)",
            "criteria": "Cooperative-sourced; organic and fair trade; standard wet-hull processing; "
                "the accessible introduction to Timor-Leste coffee",
            "markers": "Equal Exchange Timor; BC ~$14-18/250g; US ~$12-16/250g; natural food stores"
        },
        {
            "tier": 1,
            "tier_name": "Blended Timor component (in East Timor-blended coffees)",
            "criteria": "Timor-Leste as a blend component; the body-contribution role it often plays; "
                "introduction to the origin character without single-origin pricing",
            "markers": "Various; BC/US ~$10-14/250g; widely available"
        }
    ],
    "service_intelligence": {
        "temperature": "Filter: 93-94 degrees C; the wet-hull earthiness benefits from slightly higher brew temperature. Espresso: 93 degrees C standard",
        "vessel": "Filter: immersion brewer (French press or Clever Dripper) favoured for wet-hull coffees — the immersion extraction develops the body without accentuating the earthy character",
        "technique": "Timor-Leste as an origin education story: "
            "the narrative of the Timor Hybrid genetics is one of the most compelling "
            "in specialty coffee — every CLR-resistant variety in production traces to this island. "
            "Service: 'This coffee contains the genetics that saved world coffee "
            "from the leaf rust epidemic. Grown at 1,500m under forest shade, "
            "by farmer families who kept the plants alive through 24 years of occupation.'",
        "programme_position": "PCT origin education; Pacific island coffee comparison; fair trade programme centrepiece",
        "verbal_presentation": "Timor-Leste. The mountain island between Indonesia and Australia. "
            "The coffee genetics that saved the world's crop from disease. "
            "Grown by families that survived 24 years of occupation."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Cooperativa Cafe Timor (CCT) — 23,000+ farmer family network",
        "producer_location": "Aileu and Ermera districts, Timor-Leste",
        "key_person": "CCT leadership; USAID-supported cooperative governance",
        "bc_distributor": "No direct BCLDB listing. Specialty roasters in BC source CCT directly or through Fair Trade importers.",
        "us_distributor": "Equal Exchange Coffee (worker cooperative, Massachusetts) — primary fair trade US channel",
        "uk_distributor": "Cafedirect (UK fair trade cooperative); Ethical Superstore",
        "price_tier": "Entry: $10-14 (blended). Mid: $14-18 (Equal Exchange standard). Premium: $18-24 (CCT Premium). Ultra: $22-30 (washed single farm specialty).",
        "availability_notes": "Equal Exchange Timor-Leste is widely available in North American natural food stores. "
            "Specialty washed lots require direct contact with CCT or specialty importers."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Batar daan (Timorese corn and mung bean stew)",
            "pairing_type": "complement",
            "rationale": "Batar daan — the national dish of Timor-Leste, "
                "a simple corn-mung bean stew seasoned with coconut and herbs — "
                "and a cup of CCT organic coffee is the authentic Timor-Leste morning table. "
                "The earthy-herbal character of the wet-hull coffee "
                "matches the grain-herb flavour of the stew in the same earthy register."
        },
        {
            "technique_id": "",
            "dish": "Dark chocolate (70%+ cacao, Madagascar or Colombia)",
            "pairing_type": "bridge",
            "rationale": "Timor-Leste's wet-hull dark chocolate character "
                "bridges high-cacao dark chocolate through the shared fermented-dark-fruit-and-earthiness register — "
                "the coffee's body supports the chocolate's tannin without the acidity "
                "that high-altitude washed coffees create against intense chocolate."
        }
    ],
    "source": "Cooperativa Cafe Timor (CCT) production and cooperative documentation; "
        "World Coffee Research Timor Hybrid variety history; "
        "Equal Exchange sourcing documentation; "
        "USAID Timor-Leste coffee sector development reports",
    "trail_connection": "PCT-11",
    "trail_note": "PCT Region 11: Timor-Leste. The Timor Hybrid variety is the most "
        "significant botanical contribution of any Portuguese colonial territory "
        "to global agriculture — its genetics now exist in hundreds of millions "
        "of coffee plants across Latin America, Africa, and Asia. "
        "The Portuguese colonial coffee programme of the 1880s in Timor "
        "inadvertently created the world's primary disease-resistance gene pool."
})

session.commit_batch()

session.switch_region("spirits", "Africa — Cape Verde (Fogo Island, Grogue)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "cape verde grogue sugarcane pot still volcanic island",
    "region": "Africa — Cape Verde (Fogo Island, Grogue Tradition)",
    "name": "Grogue Fogo — Cape Verde Volcanic Island Sugarcane Spirit, Active Volcano Terroir",
    "terroir_origin": (
        "Cape Verde is an archipelago of 10 islands in the Atlantic, "
        "approximately 570km off the coast of Senegal — "
        "the first Portuguese Atlantic island chain beyond Madeira and the Azores. "
        "The Portuguese arrived in Cape Verde in 1456 (uninhabited) and established "
        "it as the primary staging post for the Atlantic slave trade, "
        "for provisioning ships on the route to Brazil, India, and the Gulf of Guinea. "
        "Grogue (from the Portuguese word aguardente — burning water) "
        "is the traditional cane spirit of Cape Verde, produced on all islands "
        "but reaching its highest expression on Fogo Island. "
        "Fogo Island terroir: Pico do Fogo (2,829m) is one of the world's "
        "most geologically active volcanoes — the 2014-15 eruption destroyed "
        "the village of Chã das Caldeiras and buried the vineyards and cane fields. "
        "The sugarcane grown on the volcanic flanks (800-1,400m altitude) "
        "is planted in mineral-rich basalt and scoria soils — "
        "the same volcanic mineral character that defines Martinique's agricultural spirits "
        "is present in Cape Verde cane, but in a much smaller, more isolated production. "
        "Production volumes: Fogo produces approximately 300,000 litres of Grogue annually "
        "— tiny compared to Martinique (4 million+) or Barbados (10+ million). "
        "The WADT connection: Cape Verde was the primary disembarkation point "
        "for enslaved West Africans heading to Brazil and the Caribbean — "
        "the island's population is itself a creolised mix of Portuguese and "
        "West African origin."
    ),
    "production_technique": (
        "Traditional Grogue production on Fogo: "
        "Sugarcane: traditional varieties grown on volcanic flanks; "
        "harvested by hand in the dry season (November-April). "
        "Pressing: traditional wooden or mechanical rollers; "
        "fresh cane juice is pressed immediately after cutting. "
        "This is an agricole method (fresh juice, not molasses) — "
        "making Grogue technically a rhum agricole in French classification. "
        "Fermentation: 24-72 hours in clay or concrete vessels; "
        "wild indigenous yeast; "
        "the tropical volcanic environment drives rapid fermentation. "
        "Distillation: copper pot still (alambique) — the Portuguese alembic tradition "
        "carried directly from mainland Portugal to the Atlantic islands. "
        "The pot still used on Fogo is similar in design to the "
        "pot stills of Galicia and northern Portugal — copper, single distillation, "
        "low ABV output (55-70%). "
        "No ageing for standard Grogue: bottled immediately after distillation; "
        "the fresh agricultural character is the point. "
        "Aged Grogue (Grogue Velho): some producers age in used wine casks "
        "for 2-5 years; the rarity and quality parallels early agricole exploration "
        "in Martinique before the AOC framework."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Rhum Agricole Blanc (Martinique, fresh cane juice column still)",
            "connection": (
                "Both are fresh cane juice spirits — Grogue uses a Portuguese pot still; "
                "AOC Martinique uses a French column still. "
                "The comparison shows how the same agricultural raw material (fresh cane juice) "
                "produces different character depending on the distillation technology "
                "derived from each colonial tradition."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Aguardente de Cana (Madeira or mainland Portugal)",
            "connection": (
                "Grogue is linguistically and technically derived from the Portuguese "
                "aguardente tradition. The comparison with Madeira aguardente "
                "(used to fortify wine) and Cape Verde Grogue (consumed directly) "
                "shows how the same production technique served different purposes "
                "in different Atlantic colonial contexts."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Clairin Vaval (Haiti, fresh cane juice unaged)",
            "connection": (
                "Both are pot-still, fresh cane juice, tropical volcanic island spirits "
                "from small Atlantic island communities with strong African diaspora heritage. "
                "Clairin has become a bartender darling through Velier's distribution; "
                "Grogue has not yet achieved that commercial recognition. "
                "The comparison demonstrates that Grogue is technically at the same level."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Ginjinha de Obidos (Portuguese sour cherry liqueur)",
            "connection": (
                "Both are traditional Portuguese-lineage spirits consumed in the "
                "community where they are produced, rarely exported, and defined by "
                "raw material quality rather than production technology. "
                "Both are best consumed fresh from the producer — "
                "they share the 'do not travel well' characteristic of artisan agricultural spirits."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Crystal clear (unaged); faint yellow-gold in aged versions; the volcanic mineral soils create a faintly dusty matte appearance in very fresh examples",
        "nose": "Fresh sugarcane juice, tropical citrus, volcanic mineral (faint sulphur-salt from the basalt soil), green banana, grassy herbal freshness",
        "palate": "Entry: clean, agricultural, light and precise. Mid-palate: the pot still character adds slight oiliness that column-still agricole lacks. The volcanic mineral is a secondary note, most prominent in the finish",
        "texture": "Light-to-medium body; the single distillation in a copper pot still creates a fuller texture than a column still at equivalent ABV; oily mid-palate",
        "finish": "35-50 seconds; clean cane-grass and mineral; the volcanic soil character persists longer than the fruit; gentle warmth without harshness",
        "conclusion": "The hidden original of the Atlantic cane spirit tradition — the PCT's most direct link between Portuguese colonialism and Caribbean rum development"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Grogue Velho (aged 3-5 years, Fogo estate)",
            "criteria": "Aged in used wine or French oak casks; 3-5 years; rancio developing; "
                "rare — fewer than 5,000 bottles per year from Fogo; the premium expression",
            "markers": "Grogue Velho; Cape Verde local purchase or direct import; not commercially available in North America"
        },
        {
            "tier": 3,
            "tier_name": "Destilaria Fogo (SOGEI) Grogue Standard",
            "criteria": "Formal distillery production; consistent quality control; "
                "the most reliable commercial standard for the Fogo character",
            "markers": "Destilaria Fogo; Cape Verde purchase; European specialty spirits retailers; not BCLDB listed"
        },
        {
            "tier": 2,
            "tier_name": "Household artisan Grogue (direct from Fogo farmers)",
            "criteria": "Traditional wooden still; family recipe; consumed locally; "
                "the most authentic expression but subject to inconsistency",
            "markers": "Purchase direct in Fogo Island; not commercially exported"
        },
        {
            "tier": 1,
            "tier_name": "Rhum Agricole Blanc (Martinique) as proxy outside Cape Verde",
            "criteria": "Nearest commercially available substitute for Grogue's fresh cane juice character; "
                "use for professional tasting contexts outside Cape Verde",
            "markers": "Clement or Neisson Blanc; BC ~$50-70; US ~$45-65"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at room temperature or with a single ice sphere; the fresh cane juice character is preserved at ambient temperature",
        "vessel": "Shot glass for traditional Cape Verdean service; tulip for professional tasting; the Grogue tradition is not a sipping-glass culture",
        "technique": "Traditional Cape Verde service: neat shot (ponche) at room temperature, "
            "often with a squeeze of local citrus (lemon or orange). "
            "The formal tasting context: present as the missing link "
            "in the Atlantic cane spirit timeline — "
            "the distillery that existed between the Portuguese alembic tradition and Caribbean rum. "
            "The PCT narrative sequence: Madeira wine (aguardente) → Cape Verde Grogue "
            "(pot still fresh cane) → Martinique Agricole (column still fresh cane) "
            "→ Barbados column still rum (molasses). The full Atlantic chain in four pours.",
        "programme_position": "PCT heritage sequence; Atlantic cane spirit education; rare origin tasting for advanced guests",
        "verbal_presentation": "Grogue — Fogo Island, Cape Verde. "
            "At the base of one of the world's most active volcanoes. "
            "Portuguese pot still, fresh cane juice, volcanic Atlantic island. "
            "The original Atlantic cane spirit."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Destilaria Fogo (SOGEI) — the primary formal producer on Fogo Island",
        "producer_location": "Fogo Island (Sao Filipe), Cape Verde",
        "key_person": "SOGEI management; traditional household distillers in Cha das Caldeiras",
        "bc_distributor": "Not available in BC. No BCLDB listing.",
        "us_distributor": "Not commercially available in the US at scale. Specialty imports only through European spirits distributors.",
        "uk_distributor": "Increasingly available through UK craft spirits retailers (Master of Malt, The Whisky Exchange)",
        "price_tier": "Not applicable for standard North American commerce. Educational and heritage context only for the PCT programme.",
        "availability_notes": "Grogue is not commercially available in North America at time of writing. "
            "The closest commercially available proxy is Rhum Agricole Blanc (Martinique) "
            "for the fresh cane juice character, or Clairin (Haiti) for the pot still unaged character."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Cachupa (Cape Verde national stew — hominy, beans, meat, vegetables)",
            "pairing_type": "complement",
            "rationale": "Cachupa is the Cape Verdean national dish — a slow-cooked hominy and bean stew "
                "that reflects the African and Portuguese cultural synthesis of the islands. "
                "The fresh agricultural Grogue and the earthy hominy stew "
                "share the same volcanic-island agricultural register — "
                "the pairing is the taste of the Cape Verde cultural identity."
        },
        {
            "technique_id": "",
            "dish": "Queijo de vaca fresco (fresh Cape Verdean cow cheese with cane honey)",
            "pairing_type": "bridge",
            "rationale": "Fresh Cape Verdean cow cheese with cane honey (mel de cana) "
                "bridges the Grogue's agricultural freshness and the "
                "mineral sweetness of the local unrefined cane syrup — "
                "a three-product pairing that communicates the entire "
                "sugarcane-agriculture chain of the PCT in one moment."
        }
    ],
    "source": "SOGEI Destilaria Fogo production documentation; "
        "Cape Verde Ministry of Agriculture traditional spirits survey; "
        "Fogo Island cultural heritage records",
    "trail_connection": "PCT-4",
    "trail_note": "PCT Region 4: Cape Verde — the Atlantic midpoint between Europe, Africa, and the Americas. "
        "Grogue is the most direct expression of the Portuguese alembic tradition "
        "transplanted to a subtropical volcanic island. "
        "The PCT chain: the copper pot still that arrived with Portuguese colonists in the 1500s "
        "is still operating on Fogo Island five centuries later."
})

session.commit_batch()

session.finish()
