#!/usr/bin/env python3
# PCT-15: Brazil Coffee Depth (Chapada Diamantina, Espirito Santo Conillon)
# + Martinique Rhum Agricole Depth (Neisson, Le Galion)
# Running total entering: 64
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="coffee",
    region="Brazil — Chapada Diamantina (Bahia, High Altitude)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=16,
    running_total=64
)

session.add_producer({
    "tradition": "coffee",
    "name": "Fazenda Santa Ines (Camargo family)",
    "location": "Mucuge, Chapada Diamantina, Bahia, Brazil",
    "description": "One of Brazil's most decorated specialty coffee farms. "
        "The Camargo family has farmed the Chapada Diamantina plateau since 1880. "
        "At 1,100-1,250m altitude with iron-rich red soils, Santa Ines produces "
        "Brazil's highest-altitude coffees — a rarity in a country dominated "
        "by lower-altitude production. Multiple Cup of Excellence top-ten finishes.",
    "founded": "1880",
    "region": "Chapada Diamantina, Bahia, Brazil",
    "website": "https://www.fazandasantaines.com.br",
    "verified": True
})

session.add_producer({
    "tradition": "spirits",
    "name": "Distillerie Neisson",
    "location": "Le Carbet, Martinique, French Caribbean",
    "description": "Founded 1931 by Adrien and Jean Neisson; family-owned. "
        "The smallest major distillery in Martinique. "
        "Produces exclusively from estate-grown sugarcane in Le Carbet "
        "on the northwest coast of Martinique at the base of the Piton du Carbet. "
        "Neisson is the most obsessively single-estate rhum agricole producer "
        "on the island — no purchased cane, no blending with other estates.",
    "founded": "1931",
    "region": "Martinique, French Caribbean",
    "website": "https://www.neisson.com",
    "verified": True
})

session.add_purveyor({
    "name": "Craft Imports (US) / La Maison du Whisky (France)",
    "type": "importer",
    "description": "Craft Imports: US importer for Neisson and premium Martinique agricole. "
        "La Maison du Whisky: Paris-based spirits retailer and importer; "
        "the primary European source for Neisson allocations.",
    "markets_served": ["US", "France", "UK"],
    "traditions_carried": ["spirits", "coffee"],
    "website": "https://www.lmdw.fr",
    "verified": True
})

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "brazil specialty high altitude bahia chapada diamantina",
    "region": "Brazil — Chapada Diamantina (Bahia, 1100-1250m)",
    "name": "Brazil Chapada Diamantina — High-Altitude Bahia, Rare Iron-Rich Terroir",
    "terroir_origin": (
        "The Chapada Diamantina is a highland plateau in the semi-arid state of Bahia, "
        "northeastern Brazil — completely different from the coffee heartland of "
        "Minas Gerais and Sao Paulo (Sul de Minas, Cerrado Mineiro). "
        "The region takes its name from the 19th-century diamond (diamante) rush "
        "that drew Portuguese colonial prospectors into the Brazilian interior. "
        "The PCT connection: the Chapada Diamantina was settled as part of the "
        "same Portuguese colonial interior expansion that followed the Atlantic coast "
        "settlements. The iron-rich red soils (Latossolo Vermelho-Amarelo) of the plateau "
        "are dramatically different from the volcanic red soils of the Cerrado — "
        "iron content creates a mineral ferrous character in the cup "
        "that differentiates Chapada Diamantina from all other Brazilian origins. "
        "Altitude: 900-1,350m — the highest coffee in Brazil; the cool nights "
        "(often 12-15 degrees C even in summer) produce the slow cherry development "
        "that creates the concentrated sweetness absent in lower-altitude Brazilian origins. "
        "Annual rainfall: 800-1,200mm — higher than the Cerrado, enabling natural processing "
        "without irrigation dependency. "
        "Biome: Caatinga (semi-arid shrubland) transitions to Cerrado and Atlantic Forest "
        "on the Chapada — the most biodiverse coffee-growing environment in Brazil."
    ),
    "production_technique": (
        "Chapada Diamantina production specialties: "
        "Harvest: manual (hand-picking); the terrain and altitude make mechanical harvesting "
        "impossible on most farms. The Camargo family at Fazenda Santa Ines "
        "uses selective hand-picking to maximise cherry uniformity. "
        "Varieties: Yellow Bourbon (Bourbon Amarelo) is the dominant variety at high altitude "
        "— the yellow-fruited mutation of Bourbon that Brazil first cultivated. "
        "Also: Catuai Amarelo, Bourbon Vermelho. "
        "Processing: dry/natural processing dominates — the low humidity of the Caatinga "
        "border allows full cherry drying without the fermentation control issues "
        "of high-humidity environments. "
        "Natural processing: cherries dried on raised drying beds (African beds) "
        "for 25-35 days; the extended drying at altitude (lower temperatures) "
        "produces the controlled fermentation that creates the fruit-forward character. "
        "Honey process (increasingly used): mucilage retained; intermediate fermentation; "
        "between natural and washed in character. "
        "Washed: less common but produces the cleanest expression of the iron-mineral terroir. "
        "Cup quality: consistent Cup of Excellence submissions; clean sweetness with "
        "a ferrous mineral that is only detectable in comparative tasting against "
        "Sul de Minas or Cerrado origins from the same variety."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "coffee",
            "beverage": "Ethiopia Yirgacheffe Natural (Gedeo Zone, high altitude)",
            "connection": (
                "Both are high-altitude natural-processed coffees from regions with "
                "distinct non-volcanic mineral soils. Yirgacheffe's red clay "
                "and Chapada's iron-rich Latossolo both produce a mineral-grounded "
                "sweetness that lower-altitude origins on volcanic soils cannot replicate."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Brazil Cerrado Mineiro Yellow Bourbon (Cerrado Mineiro DO)",
            "connection": (
                "The internal Brazil comparison: both regions grow Yellow Bourbon "
                "in Brazil's interior. Cerrado is 800-1,100m on deep red volcanic soils; "
                "Chapada is 900-1,350m on iron-rich sedimentary soils. "
                "The altitude difference is visible in acidity; "
                "the soil difference is visible in the mineral character."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Yemen Mocha Natural (Haraaz, terraced mountain farms)",
            "connection": (
                "Both are high-altitude natural-process coffees from semi-arid "
                "highland environments with severe water constraints. "
                "The Yemen-Brazil comparison shows how water stress "
                "concentrates sugars identically across completely different origins."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Colombia Huila Natural (Acevedo sub-region)",
            "connection": (
                "Both are South American high-altitude natural-process coffees "
                "achieving fruit concentration through altitude and dry processing. "
                "The Colombia-Brazil natural comparison shows how the same "
                "processing choice creates different flavour profiles "
                "depending on varietal composition (Colombian Caturra vs Brazilian Bourbon)."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Medium-dark cherry-brown; slightly lighter roast than standard commercial Brazilian profile allows the terroir to show; green-gold crema on espresso",
        "nose": "Dried cherry, dark caramel, stone fruit (nectarine, peach), faint iron-mineral, chocolate, dried hibiscus at lighter roast levels",
        "palate": "Entry: medium sweetness from natural processing. Mid-palate: stone fruit clarity with a ferrous mineral backbone that grounds the sweetness. Finish: clean, medium length, chocolate-and-dried-fruit persistence",
        "texture": "Full body from natural processing; the iron-rich soil character adds a dry mineral grip that prevents the natural sweetness from becoming cloying",
        "finish": "45-60 seconds for filter; 25-35 seconds for espresso; dried cherry and dark caramel with faint mineral at the end",
        "conclusion": "The Brazil that punches above its country's reputation — high altitude and iron soil create a mineral dimension absent from commercial Brazilian coffee"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Fazenda Santa Ines Cup of Excellence (top-10 lot)",
            "criteria": "Cup of Excellence submission; minimum 87 score; single farm, single harvest; "
                "the highest expression of Chapada Diamantina iron-mineral terroir",
            "markers": "Cup of Excellence auction; US ~$30-60 per 200g; limited annual availability"
        },
        {
            "tier": 3,
            "tier_name": "Fazenda Santa Ines Yellow Bourbon Natural (annual harvest)",
            "criteria": "Yellow Bourbon variety; natural processed; raised bed dried 25-35 days; "
                "the benchmark for the Chapada Diamantina style at restaurant programme pricing",
            "markers": "Fazenda Santa Ines YB Natural; BC ~$25-35/250g; US ~$22-30/250g"
        },
        {
            "tier": 2,
            "tier_name": "Chapada Diamantina Yellow Bourbon (other farms, specialty grade)",
            "criteria": "Chapada region; Yellow Bourbon; natural or honey process; "
                "specialty grade (80+ SCA score); the accessible mid-tier for the origin",
            "markers": "Various Chapada Diamantina producers; BC ~$18-25/250g; specialty roasters"
        },
        {
            "tier": 1,
            "tier_name": "Brazilian Specialty Blend with Chapada component",
            "criteria": "Introduction to Brazilian specialty with Chapada character as a component; "
                "accessible pricing for programme introduction and by-the-cup espresso",
            "markers": "Various; BC ~$12-18/250g; widely available through specialty roasters"
        }
    ],
    "service_intelligence": {
        "temperature": "Filter: 92-94 degrees C brew, serve at 75-80 degrees C. Espresso: 93 degrees C, 9 bar, 25-28s extraction",
        "vessel": "Filter: ceramic tulip or flat-bottomed dripper for maximum iron-mineral expression. Espresso: pre-heated demitasse",
        "technique": "The Chapada Diamantina as a Brazil education tool: "
            "comparative tasting of Chapada Natural (iron mineral, stone fruit) "
            "vs Cerrado Natural (chocolate, brown sugar, clean sweetness) "
            "demonstrates that 'Brazil coffee' is not a single flavour "
            "but a country of dramatically different regions. "
            "The SCA cupping narrative: the ferrous mineral note is the Chapada's "
            "signature — use it to teach guests that terroir mineral expression "
            "is not limited to grape-based beverages.",
        "programme_position": "Brazil origin education; specialty coffee tasting menu; espresso bar single-origin offering",
        "verbal_presentation": "Chapada Diamantina — the diamond highlands of Bahia, northeast Brazil. "
            "Iron-rich soils at 1,200 metres. "
            "Yellow Bourbon, dried on raised beds in the mountain air."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Fazenda Santa Ines (Camargo family) — the most recognised Chapada Diamantina estate",
        "producer_location": "Mucuge, Chapada Diamantina, Bahia, Brazil",
        "key_person": "Mauricio and Patricia Camargo (estate owners)",
        "bc_distributor": "49th Parallel Coffee Roasters (Vancouver) occasionally features Chapada lots; "
            "Prototype Coffee (Vancouver) sources directly from Chapada",
        "us_distributor": "Counter Culture Coffee, Intelligentsia, George Howell Coffee (all carry Chapada lots seasonally)",
        "uk_distributor": "Has Bean Coffee (UK), Ozone Coffee (UK)",
        "price_tier": "Entry: $12-18 (blended). Mid: $18-25 (region-grade specialty). Premium: $22-30 (Fazenda Santa Ines). Ultra: $30-60+ (Cup of Excellence lots).",
        "availability_notes": "Fazenda Santa Ines direct export to specialty importers seasonally. "
            "Cup of Excellence lots available through direct auction annually (July-August for Brazil)."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Dark chocolate (70-75% cacao, Madagascar or Peru origin)",
            "pairing_type": "complement",
            "rationale": "The dried cherry and dark caramel of Chapada natural "
                "matches the fruity-fermented chocolate character of high-cacao dark chocolate — "
                "both processed through extended fermentation (coffee cherry drying, cacao fermentation) "
                "that converts primary sugars to complex dried-fruit esters."
        },
        {
            "technique_id": "",
            "dish": "Queijo de Coalho (Brazilian grilled cheese, coastal Bahia tradition)",
            "pairing_type": "bridge",
            "rationale": "Queijo de Coalho — the semi-hard Brazilian grilling cheese — "
                "is the Bahia cultural counterpart to the Chapada coffee. "
                "The mild lactic salt of the grilled cheese bridges the "
                "dried fruit sweetness and iron mineral of the coffee — "
                "a pairing that communicates the PCT's Brazil chapter through "
                "two regional products simultaneously."
        }
    ],
    "source": "Cup of Excellence Brazil historical results database; "
        "Fazenda Santa Ines production documentation; "
        "BSCA (Brazilian Specialty Coffee Association) regional classification documentation",
    "trail_connection": "PCT-13",
    "trail_note": "PCT Region 13: Brazil (Coffee). Chapada Diamantina is the northeast "
        "extension of Brazil's specialty coffee geography — "
        "the furthest from the main coffee belt, the closest to the original "
        "Portuguese colonial settlement route along the northeast coast. "
        "Bahia was the first state of Brazil to receive Portuguese colonists (1500). "
        "The coffee that grows on its interior plateau five centuries later "
        "is the most direct agricultural lineage to the PCT colonial story."
})

session.commit_batch()

session.switch_region("spirits", "Caribbean — Martinique (Rhum Neisson, AOC)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "martinique rhum agricole aoc estate single domaine",
    "region": "Caribbean — Martinique (Rhum Agricole AOC, Le Carbet)",
    "name": "Rhum Neisson AOC Martinique — Single-Estate Agricole, Le Carbet Volcanic Soils",
    "terroir_origin": (
        "Martinique Rhum Agricole AOC is the only rum appellation with controlled "
        "origin designation status — the French Appellation d'Origine Controlee "
        "framework applied to Caribbean rum in 1996. "
        "Neisson's Le Carbet estate is on the northwest coast of Martinique, "
        "at the base of the Piton du Carbet (the island's volcanic mountain chain "
        "after the dominant Mont Pelee). "
        "The terroir case for Neisson: "
        "Sugarcane is grown on volcanic soils (andisols) derived from Mont Pelee eruptions "
        "(the 1902 eruption killed 30,000 people — the deadliest volcanic disaster "
        "of the 20th century — and covered the island in a mineral-rich ash layer). "
        "The northwest coast receives maximum trade wind exposure — the Atlantic air "
        "from the east creates a maritime-influenced microclimate "
        "that cools the crop and extends the sugarcane maturation. "
        "No purchased cane: all Neisson rhum is made from estate-grown "
        "Canne Bleue variety — the traditional Martinique cane strain "
        "that produces a grassier, more mineral juice than commercial hybrids. "
        "Canne Bleue: slower-growing, lower-yield traditional variety; "
        "banned in Martinique in the 1970s-80s commercial era "
        "but revived by Neisson and a small group of estates in the 1990s. "
        "The PCT connection: Martinique's sugarcane arrived via the "
        "Portuguese Atlantic chain (Madeira → Caribbean → Martinique) "
        "but was transformed by French colonialism into a distinctly French-influenced spirit."
    ),
    "production_technique": (
        "Neisson rhum agricole production: "
        "Harvest: manual cutting of Canne Bleue; immediately pressed on-site within 4 hours of cutting. "
        "The 4-hour rule: fresh cane juice (vesou) begins fermenting naturally within hours; "
        "the rapid press-to-ferment window is a non-negotiable quality parameter in AOC Martinique. "
        "Juice clarification: decanting to remove suspended solids; no centrifuge at Neisson. "
        "Fermentation: 24-36 hours using the estate's resident yeast population; "
        "Neisson does not use commercial yeast strains. "
        "The short fermentation produces a lighter, more floral and grass-forward "
        "character than longer-fermented agricoles (Clairin Haiti, for example). "
        "Distillation: single column still (the only type permitted under AOC Martinique rules); "
        "the column still distills to 65-75% ABV; "
        "this is deliberately lower than industrial rum (95%) to retain "
        "the volatile esters and grass character from the fresh cane juice. "
        "Neisson Blanc: bottled at 52.5% ABV (not diluted to standard 40%) "
        "— the higher bottling strength preserves the cane character for bartending. "
        "Rhum Vieux: aged in 200L French oak barriques; minimum 3 years for 'vieux' designation. "
        "L'Esprit Neisson: barrel-strength bottling; 52.5-60% ABV; no dilution."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Rhum Clement VSOP (Martinique, estate agricole)",
            "connection": (
                "Both are AOC Martinique single-estate agricoles from volcanic islands. "
                "Neisson (Le Carbet northwest coast) vs Clement (Riviere Salee southeast coast) "
                "demonstrates how opposite coastal exposures on the same volcanic island "
                "create distinguishable terroir differences in an agricultural spirit. "
                "Neisson is grassier and more mineral; Clement is rounder and more floral."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Calvados AOC Domfrontais (apple brandy, Normandy)",
            "connection": (
                "Both are AOC fruit spirits with strictly controlled geographic, "
                "varietal, and production parameters. The comparison shows that "
                "appellation control for spirits produces the same regional specificity "
                "for rum that it produces for apple brandy in Normandy."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Rhum Barbancourt Reserve du Domaine (Haiti, double distilled)",
            "connection": (
                "Both are fresh cane juice rhums from former French Caribbean territories. "
                "Neisson: AOC column still, 24-36hr fermentation, more floral-grass. "
                "Barbancourt: Cognac-method double distillation, 72hr fermentation, more structured. "
                "The comparison reveals how distillation method determines the "
                "final register even when the raw material (fresh cane juice) is identical."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Chablis Premier Cru (unoaked Chardonnay, Kimmeridgian chalk)",
            "connection": (
                "Both derive a distinctive mineral character from exceptional soil composition. "
                "The Kimmeridgian chalk of Chablis and the Mont Pelee volcanic andisols of Neisson's estate "
                "are both non-volcanic/volcanic terroir cases for how soil mineralogy "
                "transfers into agricultural product character."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Neisson Blanc 52.5%: crystal clear, watery-white; viscous legs at high proof. Neisson Vieux 3yr: pale gold, developing amber",
        "nose": "Fresh cut grass, sugarcane juice, petrol (high-proof Blanc only), tropical citrus (calamansi, lime peel), volcanic mineral, white pepper",
        "palate": "Neisson Blanc: high-proof grassiness dominates; the column still separation produces a clean spirit that carries the cane character without heavy congeners. Neisson Vieux: the wood phase adds vanilla and dried tropical fruit while the grass-mineral persists",
        "texture": "Neisson Blanc at 52.5%: high-proof burn initially but opens to a precise, clean body; the column still removes the heaviness of pot still rums. Neisson Vieux: medium body; the oak adds glycerous texture without dominating",
        "finish": "Blanc: 45-60 seconds of fresh grass and volcanic mineral; the high proof extends the finish through acidity rather than warmth. Vieux: 60-75 seconds; vanilla-oak and dried cane grass coexist",
        "conclusion": "The most terroir-specific rum available commercially — a single estate on a single volcanic island with a 500-year agricultural history"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Neisson L'Esprit Barrel Strength (Vieux)",
            "criteria": "Barrel-strength bottling (52.5-60%); no dilution post-ageing; "
                "the uncompromised expression of the estate and the Vieux ageing programme",
            "markers": "Neisson L'Esprit; US ~$90-120 via Craft Imports; BC: private order; limited"
        },
        {
            "tier": 3,
            "tier_name": "Neisson Rhum Vieux 3yr (standard aged)",
            "criteria": "Minimum 3yr ageing in 200L French barriques; AOC designation; "
                "estate cane; the accessible premium expression for programme use",
            "markers": "Neisson Vieux 3yr; US ~$60-75; BC: private import; BCLDB does not list Neisson"
        },
        {
            "tier": 2,
            "tier_name": "Neisson Blanc 52.5% (unaged, high proof)",
            "criteria": "Fresh cane juice character; 52.5% bottling strength; no added water; "
                "the bartender's reference for Martinique AOC Blanc",
            "markers": "Neisson Blanc 52.5%; US ~$45-60; BC: private order"
        },
        {
            "tier": 1,
            "tier_name": "Clement VSOP or Rhum JM VO (accessible AOC Martinique)",
            "criteria": "Established AOC Martinique brand; 4-6yr ageing; accessible price; "
                "introduction to AOC Martinique for guests new to the category",
            "markers": "Clement VSOP; BC ~$55-70; US ~$50-65; BCLDB listed"
        }
    ],
    "service_intelligence": {
        "temperature": "Neisson Blanc: serve neat at room temperature or with a 2cm ice cube; the 52.5% opens with 5 minutes air contact. Neisson Vieux: room temperature neat; or with a single large ice sphere",
        "vessel": "Glencairn for Blanc (concentrates the volatile grass-mineral); short tumbler for Vieux on ice",
        "technique": "Neisson Blanc as a cocktail base: Ti' Punch — "
            "50mL Neisson Blanc + 10mL cane syrup + 2 limes squeezed directly in the glass. "
            "The Ti' Punch is the canonical AOC Martinique service and the best vehicle "
            "for communicating the agricultural character to guests: "
            "no dilution water, no ice, lime squeezed at the table. "
            "The agricultural narrative: 'Martinique cane cut this morning, pressed within the hour, "
            "fermented 24 hours, distilled once, bottled at estate strength.'",
        "programme_position": "Martinique AOC rum education; Ti Punch cocktail programme; single-estate agricole comparison",
        "verbal_presentation": "Neisson Blanc — Le Carbet, Martinique. "
            "Single estate, estate-grown Canne Bleue. "
            "Cut this morning. Pressed within the hour. "
            "The taste of volcanic Martinique."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Distillerie Neisson — the smallest major Martinique distillery; the most single-estate-focused",
        "producer_location": "Le Carbet, Martinique, French Caribbean (DOM)",
        "key_person": "Grégoire Hayot family (current ownership); Yann Hayot (production)",
        "bc_distributor": "No BCLDB listing for Neisson. Private import required through a licensed BC agent.",
        "us_distributor": "Craft Imports (US) — primary US importer for Neisson",
        "uk_distributor": "La Maison du Whisky (France/UK distribution); "
            "The Whisky Exchange (UK)",
        "price_tier": "Entry: $45-60 (Neisson Blanc 52.5%). Mid: $60-75 (Neisson Vieux). Premium: $90-120 (L'Esprit barrel strength).",
        "availability_notes": "Neisson is not widely distributed in North America. "
            "Craft Imports handles US allocation; BC requires private import. "
            "Total annual production is very small — allocation-based for restaurant accounts."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Accras de morue (Martinique salt cod fritters)",
            "pairing_type": "complement",
            "rationale": "Accras are the canonical Martinique street food — "
                "salt cod, chilli, and herb fried fritters — and the Ti' Punch "
                "with Neisson Blanc is the canonical local pairing. "
                "The salt cod and cane grass dialogue is the Martinique aperitif moment "
                "that defines AOC agricole in its cultural context."
        },
        {
            "technique_id": "",
            "dish": "Colombo de poulet (Martinique chicken curry with colombo spice blend)",
            "pairing_type": "bridge",
            "rationale": "The colombo spice blend (turmeric, cumin, coriander, fenugreek — "
                "brought to Martinique by 19th-century Indian indentured workers) "
                "bridges the tropical mineral freshness of Neisson Blanc "
                "through the shared spice mineral register — "
                "a three-way cultural bridge (French, African, Indian) in one pairing."
        }
    ],
    "source": "AOC Martinique technical specifications (INAO documentation); "
        "Distillerie Neisson production documentation; "
        "Craft Imports US portfolio; BCLDB product listings verified April 2026",
    "trail_connection": "PCT-WADT",
    "trail_note": "PCT×WADT: Martinique at the intersection of Portuguese Atlantic cane history (PCT), "
        "West African Diaspora rum culture (WADT), and French AOC regulatory philosophy. "
        "The AOC Martinique framework creates the only rum in the world with the same "
        "legal geographic protection as Champagne or Burgundy — "
        "a French colonial administrative legacy that preserved the island's "
        "agricultural rum identity against industrial globalisation."
})

session.commit_batch()

session.finish()
