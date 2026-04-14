#!/usr/bin/env python3
# PCT-13: Vinho Verde Depth + Alentejo Wine
# Moncao Melgaco Alvarinho, Baiao Loureiro, Alentejo Blend
# Running total entering: 60
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="wine",
    region="Portugal — Vinho Verde (Moncao e Melgaco, Alvarinho)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=14,
    running_total=60
)

session.add_producer({
    "tradition": "wine",
    "name": "Anselmo Mendes Vinhos",
    "location": "Moncao, Vinho Verde, Portugal",
    "description": "Anselmo Mendes is widely considered the reference winemaker for "
        "premium Alvarinho in Portugal. His Muros Antigos Alvarinho and Curtimenta "
        "Alvarinho (24hr skin contact) define the premium end of the sub-region. "
        "Trained in Bordeaux and Burgundy; returned to introduce low-yield, "
        "single-quinta Alvarinho production in the 1990s.",
    "founded": "1995",
    "region": "Vinho Verde DOC — Moncao e Melgaco sub-region",
    "website": "https://www.anselmomendes.pt",
    "verified": True
})

session.add_producer({
    "tradition": "wine",
    "name": "Quinta do Crasto",
    "location": "Sabrosa, Douro, Portugal (also Alentejo production)",
    "description": "One of the Douro's leading estates for both Port and table wine. "
        "The Roquette family has owned Crasto since 1903. Now produces Vinho Alentejano "
        "through acquired vineyard land in the Alentejo.",
    "founded": "1903",
    "region": "Douro DOC / Alentejo DOC",
    "website": "https://www.quintadocrasto.pt",
    "verified": True
})

session.add_purveyor({
    "name": "Selection Massale (previously Kermit Lynch Wine Merchant)",
    "type": "importer",
    "description": "Berkeley-based importer of Portuguese, French, and Italian wines. "
        "Primary US importer for Anselmo Mendes Alvarinho and premium Vinho Verde. "
        "Known for representing authentic artisan production without commercial correction.",
    "markets_served": ["US", "nationwide_US"],
    "traditions_carried": ["wine"],
    "website": "https://www.kermitlynch.com",
    "verified": True
})

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "vinho verde alvarinho premium moncao melgaco",
    "region": "Portugal — Vinho Verde (Moncao e Melgaco sub-region)",
    "name": "Alvarinho Moncao e Melgaco — Portugal's Most Mineral and Age-Worthy Vinho Verde",
    "terroir_origin": (
        "Moncao e Melgaco is the most northerly and most continental of Vinho Verde's nine sub-regions — "
        "positioned at the Portuguese-Spanish border where the Minho River creates a natural boundary. "
        "The sub-region's continental character (drier, hotter summers than coastal Vinho Verde) "
        "fundamentally differentiates Alvarinho from Moncao e Melgaco from the lighter, "
        "more neutral versions produced in the coastal sub-regions. "
        "Soils: granite decomposed into sandy loam (areia granitica) with occasional schist outcrops — "
        "the granite gives Alvarinho its distinctive floral and mineral precision. "
        "The Minho River valley channels cool Atlantic air up from the coast but "
        "the continental summer allows full phenolic ripeness — a balance point no other "
        "Portuguese white wine region achieves with such consistency. "
        "Vine training: traditional bordura (vertical trellis) at Anselmo Mendes, "
        "replacing the traditional ramada (overhead pergola) to improve air circulation "
        "and reduce disease pressure. Average vine age for premium parcels: 30-45 years. "
        "The Galicia connection: the identical variety (Albarino in Galicia) is grown on the "
        "Spanish side of the same river valley — the most direct PCT cultural-terroir link "
        "in the Iberian peninsula."
    ),
    "production_technique": (
        "Harvest: manual, mid-September for standard; late September for premium parcels "
        "(the extra 2 weeks in the continental heat creates the phenolic ripe character "
        "that separates Moncao e Melgaco from coastal Alvarinho). "
        "Crushing: whole-cluster pressing; no skin contact for standard expressions. "
        "Curtimenta (Anselmo Mendes): 24hr skin contact on premium Alvarinho parcels — "
        "the skin contact extracts phenolic texture and aromatic oils that create "
        "the copper-tinged, textural 'orange wine adjacent' style. "
        "Fermentation: indigenous yeasts in stainless steel; no oak contact for fresh style; "
        "older 300L French oak for premium expression (Muros Antigos 'Vinhas Velhas'). "
        "Sulphur: very low SO2 regime at Anselmo Mendes; natural winemaking philosophy. "
        "Ageing on lees: 6-9 months on gross lees with weekly battonage "
        "for the Muros Antigos range — this builds the oily texture that makes Alvarinho "
        "from Moncao e Melgaco one of the most food-resistant whites in Portugal. "
        "The wines age: unlike standard Vinho Verde (drink within 18 months), "
        "premium Moncao e Melgaco Alvarinho from low-yield old vine parcels "
        "develops for 5-8 years; the 2016 Anselmo Mendes Curtimenta is drinking beautifully in 2026."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "wine",
            "beverage": "Albarino Rias Baixas DO (Galicia, Spain)",
            "connection": (
                "The identical grape variety from the identical river valley — "
                "Alvarinho on the Portuguese side, Albarino on the Spanish. "
                "The comparison reveals how IVDP vs DO regulatory frameworks, "
                "different winemaker philosophies, and slightly different sub-regional "
                "microclimates create divergent expressions from the same genetic material."
            )
        },
        {
            "tradition": "wine",
            "beverage": "White Burgundy Macon-Villages (Chardonnay, lees-aged)",
            "connection": (
                "Both are granite-grown whites with lees ageing providing oily texture. "
                "The comparison shows how two different varieties (Alvarinho and Chardonnay) "
                "can reach a similar textural register through identical "
                "winemaking choices (lees ageing, no oak, cool fermentation)."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Gruner Veltliner Smaragd (Wachau, Austria)",
            "connection": (
                "Both are mineral-driven, food-versatile Central/Western European whites "
                "with the ability to age 5-10 years from optimal vintages. "
                "The Wachau Gruner and Moncao e Melgaco Alvarinho both "
                "carry a distinctive white pepper and mineral saline character."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Vermentino di Gallura DOCG (Sardinia)",
            "connection": (
                "Both are Atlantic/Mediterranean-influenced granite-grown whites "
                "with pronounced mineral salinity and aromatic citrus-floral precision. "
                "The Sardinian granite and the Portuguese Minho granite produce "
                "a mineral signature more similar than their geographic distance suggests."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Pale gold with green-gold reflections; medium viscosity; slight spritz in very young examples (CO2 retained during bottling at Vinho Verde tradition)",
        "nose": "White peach, lemon zest, jasmine, salted sea air, white flowers, faint granite mineral; the aromatic precision of Alvarinho is unlike any other Portuguese white variety",
        "palate": "Entry: fresh, dry, with citrus-driven acidity. Mid-palate: stone fruit and oily texture from lees ageing. Finish: saline mineral persistence, bone-dry on the palate",
        "texture": "Medium body; the lees-aged examples are oily and grippy — the textural register of a white Burgundy achieved through lees contact rather than oak",
        "finish": "45-60 seconds; saline mineral and citrus pith persist; the dryness is complete — no residual sugar in premium Moncao e Melgaco",
        "conclusion": "The most mineral and food-versatile Portuguese white wine — can replace Burgundy in contexts where Burgundy is too expensive or too heavy"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Anselmo Mendes Alvarinho Curtimenta (Skin Contact)",
            "criteria": "24hr skin contact; old vine parcels; 6-9 months lees ageing; natural low-SO2; "
                "the most demanding and distinctive Alvarinho expression in the sub-region",
            "markers": "Anselmo Mendes Curtimenta; BC ~$45-60; US ~$40-55; limited distribution"
        },
        {
            "tier": 3,
            "tier_name": "Anselmo Mendes Muros Antigos Vinhas Velhas (Old Vine)",
            "criteria": "Old vine Alvarinho (40+ year parcels); no oak; 6 months lees; "
                "the benchmark for age-worthy Alvarinho from Moncao e Melgaco",
            "markers": "Muros Antigos Vinhas Velhas; BC ~$35-45; US ~$30-40"
        },
        {
            "tier": 2,
            "tier_name": "Soalheiro Alvarinho or Quinta de Santiago Alvarinho",
            "criteria": "Single-quinta Moncao e Melgaco; 3-5 months lees; clean and mineral; "
                "the mid-tier reference for the sub-region character",
            "markers": "Soalheiro Alvarinho; BC ~$25-35; US ~$22-30; BCLDB listed"
        },
        {
            "tier": 1,
            "tier_name": "Quinta da Aveleda Alvarinho or Casal Garcia Vinho Verde",
            "criteria": "Entry Vinho Verde; some Alvarinho content; light and fresh; "
                "introduction to the Vinho Verde category for new guests",
            "markers": "Casal Garcia; BC ~$12-18; US ~$10-15; BCLDB widely available"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 10-12 degrees C for the fresh standard expressions; 12-14 degrees C for premium skin-contact and old-vine versions to show textural depth",
        "vessel": "Narrow-mouthed white wine glass (Riesling style) to preserve the aromatic precision; a wide-bowled Burgundy glass will dissipate the floral character",
        "technique": "Premium Moncao e Melgaco Alvarinho as a Burgundy alternative: "
            "on a wine-by-the-glass program, position the Anselmo Mendes Muros Antigos "
            "as the house white for those who want white Burgundy character at half the price. "
            "The sales script: 'Portuguese granite, Atlantic climate — the white wine "
            "that gives you the mineral-lees texture of Burgundy from the edge of the Atlantic.' "
            "For food: Alvarinho's saline mineral is the most food-friendly match for shellfish, "
            "grilled white fish, ceviche, and light poultry in any price category.",
        "programme_position": "House white alternative to Burgundy; shellfish course pairing; by-the-glass premium white wine program",
        "verbal_presentation": "Alvarinho, Moncao e Melgaco — the northernmost corner of Portugal, "
            "at the Spanish border on the Minho River. "
            "Granite soils, Atlantic air, stone fruit and sea salt. "
            "The white wine of the Portuguese Atlantic coast."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Anselmo Mendes Vinhos — the reference producer for premium skin-contact and old-vine Alvarinho",
        "producer_location": "Moncao, Vinho Verde DOC, Portugal",
        "key_person": "Anselmo Mendes (winemaker; trained Bordeaux and Burgundy)",
        "bc_distributor": "No direct BCLDB listing for Anselmo Mendes; Soalheiro Alvarinho is BCLDB-listed",
        "us_distributor": "Kermit Lynch Wine Merchant (Berkeley) for Anselmo Mendes; "
            "distributor varies by state for Soalheiro",
        "uk_distributor": "Caves de Pyrene, Indigo Wine (London)",
        "price_tier": "Entry: $12-18 (standard Vinho Verde). Mid: $25-35 (Soalheiro). Premium: $35-55 (Anselmo Mendes old vine/skin contact).",
        "availability_notes": "Anselmo Mendes Curtimenta is limited production — contact Kermit Lynch for allocation. "
            "Soalheiro Alvarinho widely available across North America."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Percebes (Galician barnacles, boiled in seawater) or Portuguese crab",
            "pairing_type": "complement",
            "rationale": "The saline mineral character of Alvarinho from Moncao e Melgaco "
                "is the direct counterpart to percebes — the iodine sea mineral in the shellfish "
                "and the granite mineral in the wine create the quintessential Atlantic pairing."
        },
        {
            "technique_id": "",
            "dish": "Grilled sea bass or turbot with lemon and olive oil",
            "pairing_type": "bridge",
            "rationale": "The citrus-mineral axis of Alvarinho bridges the delicate white fish "
                "and the brightness of the lemon oil finish — "
                "the most effortless white wine-fish pairing on the Atlantic coast."
        }
    ],
    "source": "CVRVV (Comissao de Viticultura da Regiao dos Vinhos Verdes) sub-region specifications; "
        "Anselmo Mendes Vinhos production documentation; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1 (northern extension): Moncao e Melgaco Alvarinho "
        "sits at the linguistic and cultural boundary between Portugal and Galicia. "
        "The identical Alvarinho/Albarino grape grown on both sides of the Minho River "
        "is one of the clearest examples of how the PCT's Portugal-Atlantic "
        "cultural continuity extends into the Iberian peninsula itself."
})

session.commit_batch()

session.switch_region("wine", "Portugal — Alentejo (Vinho Alentejano DOC)")

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "vinho alentejano tinto blend old vine",
    "region": "Portugal — Alentejo (Vinho Alentejano DOC)",
    "name": "Alentejo Red Blend — Touriga-Aragonez Continental Mediterranean Style",
    "terroir_origin": (
        "The Alentejo — meaning 'across the Tagus' — is the largest wine region in Portugal "
        "by area and arguably the most dramatically different from the Atlantic-influenced north. "
        "The Alentejo is a flat, hot, semi-arid plain with a strongly continental climate: "
        "summer temperatures reach 40+ degrees C, annual rainfall drops to 500-700mm, "
        "and the daily temperature range between summer day and night can exceed 20 degrees C. "
        "Soils: schist and marble-limestone alternating across the sub-regions; "
        "Borba, Redondo, Reguengos de Monsaraz, Evora, and Portalegre are the key sub-DOCs. "
        "The Alentejo was historically a grain-producing region — cork oaks and olive groves "
        "interrupted by vast wheat fields. Wine was the secondary agricultural product. "
        "The quality revolution: in the 1990s, with EU subsidies and "
        "temperature-controlled stainless steel winemaking arriving simultaneously, "
        "the Alentejo transformed from bulk production (cooperatives sold at 1.50 euros per litre) "
        "to a leading premium DOC producing wines competitive with Rioja and Priorat. "
        "The varieties: Aragonez (Tempranillo) + Touriga Nacional + Trincadeira + Alicante Bouschet. "
        "Alicante Bouschet is a teinturier variety (red flesh as well as skin) — grown across "
        "the Mediterranean but reaching its highest expression in the Alentejo's heat."
    ),
    "production_technique": (
        "Harvest: manual, late August to early October depending on sub-region altitude. "
        "Portalegre (high-altitude 400-700m): latest harvest, most acid retention, most freshness. "
        "Reguengos de Monsaraz (low-altitude, hottest): earliest harvest, most fruit concentration. "
        "Fermentation: temperature-controlled stainless steel (the key modernisation of the 1990s); "
        "extended maceration (15-25 days for premium) to extract Alicante's deep tannin and colour. "
        "Oak regime: French 225L barriques for premium; 12-18 months for mid-tier; "
        "Portuguese 500L balseiro for artisan production (Esporao Reserva, Jose de Sousa). "
        "The modern Alentejo style: full-bodied (13.5-15% ABV), dark fruit, "
        "Mediterranean herb (dried thyme, rosemary, cistus), warm mineral, "
        "18+ months oak for premium releases. "
        "Jose de Sousa (Jose Maria da Fonseca): terracotta amphora fermentation — "
        "the pre-Roman production method revived; creates textural wines without oak influence. "
        "Esporao Reserva: benchmark large-estate expression; consistent house style in two decades."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "wine",
            "beverage": "Priorat DOCa (Garnacha-Carinena blend, Catalonia)",
            "connection": (
                "Both are warm-climate, schist-dominant Mediterranean reds with high concentration "
                "and extract. Priorat is steeper and more mineral-driven; Alentejo is flatter "
                "and more Mediterranean-herbal. The comparison demonstrates the granite-limestone "
                "vs schist influence on identical warm-climate winemaking."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Chateau Musar (Bekaa Valley, Lebanon)",
            "connection": (
                "Both are Mediterranean-influenced blended reds from non-canonical European wine regions "
                "that achieved international recognition through character rather than appellation prestige. "
                "Both feature Carignan/Cinsault (Musar) or Alicante Bouschet (Alentejo) "
                "as the defining secondary variety."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Rioja Reserva (Tempranillo-dominant, aged in American oak)",
            "connection": (
                "Both are Tempranillo/Aragonez dominant blends with 12-18 months oak ageing. "
                "Rioja uses American oak creating vanilla-coconut register; "
                "Alentejo uses French oak creating darker fruit and spice. "
                "The oak nationality comparison is the key structural teaching point."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Mourvedre-dominant Bandol Rouge (Domaine Tempier)",
            "connection": (
                "Both are densely-structured Mediterranean reds requiring 5-10 years from vintage. "
                "Both carry a garrigue-herb character (dried Mediterranean herbs) "
                "that marks continental sun-exposed viticulture across the Mediterranean basin."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Deep ruby-garnet with purple rim in youth; garnet with brick edge at 8-10yr; the Alicante Bouschet contributes unusual colour depth even at mid-price",
        "nose": "Dark plum, blackberry, dried Mediterranean herbs (thyme, rosemary, cistus), warm leather, vanilla from French oak, black olive mineral",
        "palate": "Full body; concentrated dark fruit; firm but ripe tannins; the heat of the Alentejo summer is present as a warm texture rather than harsh alcohol; finish extends through the herb-mineral register",
        "texture": "Structured and dense in youth; opens considerably at 5-8 years; the ripe tannins from low-yield old vine Aragonez are the structural foundation",
        "finish": "60-75 seconds; dark fruit yields to dried herb and mineral; the Alicante Bouschet adds a purple fruit persistence unusual for Tempranillo-based blends",
        "conclusion": "The Alentejo red challenges the northern Portugal dominance in premium wine — a Mediterranean character entirely distinct from the Douro or Alentejo coast"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Jose de Sousa Maior (terracotta amphora, old vine)",
            "criteria": "Terracotta amphora fermentation; Grand Noir de la Calmette and Aragonez from 80-100yr vines; "
                "the most intellectually demanding and age-worthy Alentejo expression; "
                "no oak influence — pure terroir and variety character",
            "markers": "Jose de Sousa Maior; BC ~$80-120; US ~$75-100; limited availability"
        },
        {
            "tier": 3,
            "tier_name": "Esporao Reserva Tinto or Herdade do Mouchao Tinto",
            "criteria": "Estate-grown; French oak 12-18 months; old vine sourcing; "
                "consistent benchmark expression for the modern Alentejo premium tier",
            "markers": "Esporao Reserva; BC ~$30-40; US ~$28-38; BCLDB listed"
        },
        {
            "tier": 2,
            "tier_name": "Quinta da Malho Tinto or Monte da Ravasqueira Seleccao",
            "criteria": "Mid-tier estate production; correct Alentejo character; "
                "accessible introduction to the regional style at by-the-glass pricing",
            "markers": "Various mid-tier; BC ~$18-28; US ~$16-24; BCLDB listed"
        },
        {
            "tier": 1,
            "tier_name": "Loios Tinto or Herdade do Esporao Dois Polvos",
            "criteria": "Entry production; cooperative or large estate sourcing; "
                "fruit-forward, drinking young; introduction to Alentejo at entry price",
            "markers": "Loios Tinto; BC ~$12-16; US ~$10-14; BCLDB widely available"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 16-18 degrees C — the Alentejo tannin structure needs warmth to open fully; too cold makes the tannins grippy and the fruit hidden",
        "vessel": "Large Bordeaux glass — the full-bodied structure needs the widest bowl available to release the dark fruit and dried herb nose",
        "technique": "Premium Alentejo red requires 1 hour decanting minimum before service. "
            "At table: the Mediterranean herb character of Alentejo reds is the natural match "
            "for grilled meats (lamb with rosemary, Iberian pork, beef with thyme), "
            "hard aged cheeses, and slow-braised preparations. "
            "The service narrative: the continental Portuguese hinterland vs the Atlantic coast — "
            "guests who know Douro wines are immediately challenged by the Alentejo's different character.",
        "programme_position": "House red alternative to Rioja; grilled meat pairing; red wine programme depth-coverage for Portuguese wine identity",
        "verbal_presentation": "Alentejo — the inland plain south of the Tagus. "
            "Hot, flat, ancient. Touriga, Aragonez, and Alicante. "
            "The red wine of continental Portugal."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Jose Maria da Fonseca (Jose de Sousa) and Esporao — the two defining estates for different Alentejo philosophies",
        "producer_location": "Reguengos de Monsaraz / Evora, Alentejo, Portugal",
        "key_person": "Joao Portugal Ramos (the most influential consulting winemaker in Alentejo)",
        "bc_distributor": "BCLDB stocks Esporao Reserva and several Alentejo mid-tier wines; Jose de Sousa through private import",
        "us_distributor": "Kermit Lynch (Jose de Sousa); Jorge Ordonez Selections (Esporao); "
            "Wide national distribution for Esporao",
        "uk_distributor": "Bibendum (Esporao); Caves de Pyrene; widely available in Waitrose and Majestic",
        "price_tier": "Entry: $12-16. Mid: $18-28. Premium: $30-40 (Esporao Reserva). Ultra: $80-120 (Jose de Sousa Maior).",
        "availability_notes": "Esporao Reserva is the most widely available premium Alentejo red in North America. "
            "BCLDB stocks consistently. Jose de Sousa Maior requires private order."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Lamb shoulder slow-roasted with rosemary, garlic, and Alentejo olive oil",
            "pairing_type": "complement",
            "rationale": "The dried rosemary and thyme character of Alentejo red "
                "mirrors the herb profile of slow-roasted lamb — "
                "both reflecting the same Mediterranean garrigue landscape, "
                "one in the glass, one on the plate."
        },
        {
            "technique_id": "",
            "dish": "Aged Manchego (18 months) or Pecorino Sardo with quince",
            "pairing_type": "bridge",
            "rationale": "The ripe dark fruit of Alentejo bridges aged sheep cheese and quince "
                "through a Mediterranean fruit-fat-acid triangle — "
                "the same pairing logic that works for Rioja and Spanish sheep cheese "
                "but with the Alentejo's darker fruit register."
        }
    ],
    "source": "CVA (Comissao Vitivinicola do Alentejo) technical specifications; "
        "Esporao and Jose Maria da Fonseca production documentation; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1: Portugal (Alentejo extension). "
        "The Alentejo's Roman-era wine and olive culture predates the Portuguese nation itself. "
        "The cork oak forests of the Alentejo also supply virtually all of the world's "
        "natural wine corks — meaning every Madeira, Port, Vinho Verde, and fortified wine "
        "in the PCT is sealed with a product from this same region."
})

session.commit_batch()

session.finish()
