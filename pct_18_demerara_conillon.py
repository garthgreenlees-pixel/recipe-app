#!/usr/bin/env python3
# PCT-18: Mozambique Beverages + Angola Coffee Depth + Demerara Rum Depth
# Running total entering: 70
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="Caribbean — Guyana (Demerara Rum, ICBU/DDL)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=19,
    running_total=70
)

session.add_producer({
    "tradition": "spirits",
    "name": "Demerara Distillers Ltd (DDL)",
    "location": "Diamond, East Bank Demerara, Guyana",
    "description": "The sole surviving distillery in the Demerara region of Guyana, "
        "DDL operates a unique collection of antique stills: "
        "the Versailles wooden pot still (1703), "
        "the Enmore coffey still (1880s), "
        "the Port Mourant double wooden pot still (1732), "
        "and two metal pot stills. "
        "The El Dorado brand is DDL's premium consumer range. "
        "The bulk rum they produce is sold to blenders globally — "
        "most 'Demerara rum' in blended British rums originates from DDL.",
    "founded": "1670 (original still system); DDL consolidated 1983",
    "region": "East Bank Demerara, Guyana",
    "website": "https://www.eldoradorum.com",
    "verified": True
})

session.add_producer({
    "tradition": "coffee",
    "name": "Fazenda Camocim (Seabra family)",
    "location": "Domingos Martins, Espirito Santo, Brazil",
    "description": "The leading biodynamic coffee estate in Brazil. "
        "Fazenda Camocim was the first Brazilian coffee estate to achieve "
        "full biodynamic certification (Demeter). "
        "Pedro Domingo Seabra practices Rudolf Steiner's biodynamic "
        "agricultural principles at 900-1,100m altitude in the Pedra Azul mountains "
        "of Espirito Santo state. Known for the Bourbon Amarelo natural-processed "
        "and the rare Catucai 785 variety.",
    "founded": "1987",
    "region": "Espirito Santo, Brazil",
    "website": "https://www.cafecamocim.com.br",
    "verified": True
})

session.add_purveyor({
    "name": "Velier SpA (Italy)",
    "type": "importer_bottler",
    "description": "Genoa-based spirits importer and bottler; "
        "the most important single-cask, single-distillery rum bottler in the world. "
        "Luca Gargano (Velier's director) created the independent rum bottling category "
        "with his DDL/Demerara single-still single-cask releases (2004 onward). "
        "Velier is also the primary European importer of Clairin (Haiti) and "
        "is responsible for the global recognition of the Demerara still heritage.",
    "markets_served": ["Italy", "UK", "US", "worldwide"],
    "traditions_carried": ["spirits"],
    "website": "https://www.velier.it",
    "verified": True
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "demerara rum antique wooden pot still guyana",
    "region": "Caribbean — Guyana (Demerara River, East Bank)",
    "name": "El Dorado Demerara Rum — Antique Wooden Pot Still Heritage, Last of Its Kind",
    "terroir_origin": (
        "The Demerara River in Guyana is the last location on earth where "
        "17th and 18th century wooden pot stills are still in operation for commercial rum production. "
        "The Versailles wooden pot still dates to 1703; "
        "the Port Mourant double wooden pot still dates to 1732. "
        "These are not museum exhibits — DDL uses them weekly "
        "to produce the distinctive heavy ester Demerara character "
        "that cannot be replicated in any modern still design. "
        "The wooden pot still contribution: the wood of the still itself "
        "contributes to the fermentation and distillation character. "
        "The bacterial populations in the wood create ester compounds "
        "(ethyl acetate, isoamyl acetate) that are absent from metal stills. "
        "This is the 'Demerara funk' — a deeply estery, leather-and-dried-fruit "
        "character that defines the Demerara style and is the foundation of "
        "most British Navy rum blends and many rum cocktail recipes. "
        "The PCT connection: the Demerara sugar trade was established by "
        "Dutch colonists following the Portuguese Atlantic cane chain. "
        "The Dutch brought sugarcane cultivation methods from their Brazilian colony "
        "(Recife/Pernambuco, captured from the Portuguese in 1630) "
        "to Guyana. The PCT sugarcane lineage runs directly "
        "through the Dutch-Portuguese colonial exchange."
    ),
    "production_technique": (
        "DDL Demerara still system: "
        "Molasses source: Demerara Sugar Refinery (adjacent to DDL) — "
        "one of the world's last working Demerara sugar estates. "
        "Fermentation: 48-72 hours in open-top fermenters with wild yeast populations "
        "that have colonised the fermentation hall over decades. "
        "The specific ester compounds in Demerara rum (principally ethyl esters of "
        "fatty acids) are produced by the bacterial population in the fermentation "
        "environment — a living biome accumulated across centuries of production. "
        "Still selection: DDL blends distillate from multiple stills for El Dorado. "
        "Port Mourant (double wooden pot): produces the heaviest, most funky rum — "
        "ethyl acetate and isoamyl acetate dominant; the darkest and richest component. "
        "Versailles (single wooden pot): lighter than PM; more fruity and floral. "
        "Enmore Coffey (continuous): the lightest component; adds approachability "
        "to the PM-dominated blend. "
        "Ageing: El Dorado 12yr (12 years minimum in ex-bourbon American oak); "
        "El Dorado 15yr (15 years minimum); "
        "El Dorado 21yr (21 years minimum) — the most complex standard expression. "
        "Velier single-still releases: DDL supplies Luca Gargano (Velier) "
        "with single-cask, single-still rum at cask strength — "
        "the most sought-after rum in the world for connoisseurs."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Springbank 15yr (Campbeltown Scotch, direct-fired wash still)",
            "connection": (
                "Both are distilleries that maintain archaic equipment "
                "because it produces a character that modern technology cannot replicate. "
                "Springbank's direct-fired copper wash still and DDL's wooden pot stills "
                "are both expensive, inefficient, and irreplaceable. "
                "Both produce the most character-driven spirits in their respective traditions."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Worthy Park 109 Jamaica Rum (high-ester pot still)",
            "connection": (
                "Both are high-ester Caribbean pot still rums from the British colonial "
                "rum tradition. Demerara wooden pot: earthy-leathery ester. "
                "Jamaican metal pot: fruity-banana ester. "
                "The comparison teaches guests that 'pot still' is a hardware category "
                "with enormous variability in outcome depending on material and configuration."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Armagnac Blanc de Blancs (Gascony, single continuous still)",
            "connection": (
                "Both traditions preserve a single antique still design that was "
                "superseded by technological improvement elsewhere. "
                "Armagnac's alembic armagnacais (single continuous still) and "
                "DDL's wooden pot still both produce character through inefficiency — "
                "the inefficiency is the character."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Rhum Barbancourt Reserve du Domaine (Haiti, Cognac double-distillation)",
            "connection": (
                "Both are South American/Caribbean rums whose production method "
                "was determined by European colonial heritage. "
                "Demerara wooden pot still: Dutch/British industrial heavy rum. "
                "Barbancourt double-distillation: French Cognac method applied to Caribbean cane. "
                "The PCT×WADT colonial technology comparison in two pours."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "El Dorado 12yr: deep amber-mahogany, thick legs; 15yr: deeper, more red-mahogany; 21yr: dark amber with exceptional viscosity from long tropical ageing",
        "nose": "Port Mourant component: leather, dried prune, overripe banana, ethyl acetate (nail varnish at full strength, pineapple-candy when diluted), roasted coffee, dark molasses. The Demerara funk is unmistakable — not subtle",
        "palate": "Full body from high-ester fermentation; the wooden still contribution creates a weight and texture unlike metal-still rum; caramelised molasses sweetness; dried fruit; coffee; persistent leather",
        "texture": "Dense, almost syrupy at 21yr; the high-ester content and long ageing create a coating texture; the sugar refinery context means natural sweetness from the Demerara molasses is present",
        "finish": "90+ seconds; the longest finish of any Caribbean rum style; the ester compounds persist well after the sweetness resolves; leather and dried fruit in the final breath",
        "conclusion": "The living museum of colonial rum production — the stills that were operating when the sugar trade was at its height are still producing rum today"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Velier DDL Single-Still Single-Cask (Port Mourant or Versailles)",
            "criteria": "Single still; single cask; cask strength (50-65%); "
                "no blending or dilution; the maximum expression of the wooden still character; "
                "produced for the connoisseur market by Luca Gargano",
            "markers": "Velier DDL Port Mourant; US and UK ~$150-400+; allocations through specialty retailers"
        },
        {
            "tier": 3,
            "tier_name": "El Dorado 21yr",
            "criteria": "21 years minimum; multi-still blend at its most complex; "
                "rancio developing; the highest standard production expression",
            "markers": "El Dorado 21yr; BC ~$90-120; US ~$80-100; BCLDB Signature stores"
        },
        {
            "tier": 2,
            "tier_name": "El Dorado 15yr",
            "criteria": "15 years minimum; the balanced benchmark; "
                "accessible premium for cocktail programme and neat service",
            "markers": "El Dorado 15yr; BC ~$60-80; US ~$55-70; BCLDB listed"
        },
        {
            "tier": 1,
            "tier_name": "El Dorado 12yr",
            "criteria": "12 years minimum; the accessible entry to Demerara character; "
                "full ester contribution from wooden stills detectable",
            "markers": "El Dorado 12yr; BC ~$40-55; US ~$35-48; BCLDB listed"
        }
    ],
    "service_intelligence": {
        "temperature": "El Dorado 15yr and 21yr: room temperature, neat first before any ice. The wooden still ester character needs no dilution to open — it is present from the first pour",
        "vessel": "Glencairn or tulip for neat service; the ester nose needs concentration not dissipation",
        "technique": "The education tool for ester chemistry: El Dorado 12yr in a Glencairn, neat. "
            "The first nose: most guests identify pineapple-candy or banana. "
            "Explain: 'That is ethyl acetate — produced by the bacteria in the wooden still walls. "
            "The wood is 320 years old. The bacteria are part of the recipe.' "
            "The history tool: El Dorado 15yr + a map of the Demerara river. "
            "The stills are still on the same bank. The sugar refinery is next door. "
            "The Dutch brought cane from Brazil. The Portuguese brought it to Brazil. "
            "The PCT chain ends (begins?) in Demerara.",
        "programme_position": "Caribbean rum education; PCT×WADT heritage sequence; cocktail programme anchor for Demerara character",
        "verbal_presentation": "El Dorado — Demerara River, Guyana. "
            "The last wooden pot stills from 1703. "
            "They have been making rum on the same bank of the same river for 320 years."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Demerara Distillers Ltd (DDL) — El Dorado brand; Velier bottlings",
        "producer_location": "Diamond, East Bank Demerara, Guyana",
        "key_person": "Shaun Caleb (Master Blender, DDL); Luca Gargano (Velier, Italy — independent bottlings)",
        "bc_distributor": "BCLDB stocks El Dorado 12yr and 15yr; 21yr at Signature stores",
        "us_distributor": "DropCo Beverages (US national for El Dorado); "
            "Velier distributed through select US importers (Italian importers vary by state)",
        "uk_distributor": "Speciality Brands (El Dorado); Velier through Master of Malt and The Whisky Exchange",
        "price_tier": "Entry: $40-55 (12yr). Mid: $60-80 (15yr). Premium: $90-120 (21yr). Ultra: $150-400+ (Velier single-still).",
        "availability_notes": "El Dorado 12yr and 15yr are among the most widely available premium aged rums in North America. "
            "Velier single-still releases sell out immediately on release — allocation required."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Pepperpot (Guyanese national dish — Amerindian cassareep-braised beef and pork)",
            "pairing_type": "complement",
            "rationale": "Pepperpot — Guyana's national dish, a slow-cooked beef and pork stew "
                "in cassareep (reduced cassava juice) with aromatic spices — "
                "and El Dorado 15yr is the canonical Guyanese meal pairing. "
                "The cassareep's dark bitter sweetness and the rum's molasses caramel "
                "and leather create a colonial-Caribbean food culture dialogue."
        },
        {
            "technique_id": "",
            "dish": "Dark Demerara sugar cake (pecan and molasses)",
            "pairing_type": "bridge",
            "rationale": "The Demerara sugar in the cake is from the same Sugar Refinery "
                "adjacent to DDL — the cane was processed on the same land "
                "that produced the molasses for the rum. "
                "The bridge pairing is literal: both the dessert and the rum "
                "come from the same raw material, the same location, the same history."
        }
    ],
    "source": "Demerara Distillers Ltd production documentation; "
        "Velier SpA DDL release notes; "
        "DropCo Beverages US distribution portfolio; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-WADT",
    "trail_note": "PCT×WADT: Demerara rum is the most historically loaded rum in the Atlantic. "
        "The wooden stills from 1703 and 1732 predate American independence. "
        "The sugar was grown by enslaved West Africans on Dutch colonial land "
        "where cane cultivation was brought by the Dutch from Portuguese Brazil. "
        "The Demerara wooden still pot rum is the PCT's most concentrated "
        "expression of the colonial cane chain."
})

session.commit_batch()

session.switch_region("coffee", "Brazil — Espirito Santo (Biodynamic, Fazenda Camocim)")

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "brazil biodynamic espirito santo mountain robusta conillon specialty",
    "region": "Brazil — Espirito Santo (Pedra Azul Mountains, 900-1100m)",
    "name": "Espirito Santo Conillon Specialty — Brazil's Robusta Reinvention, Mountain Biodynamic",
    "terroir_origin": (
        "Espirito Santo is a small coastal state in southeastern Brazil — "
        "the second-largest producer of coffee in Brazil after Minas Gerais, "
        "but the first in Conillon (Coffea canephora var. canephora, "
        "Brazilian robusta equivalent). "
        "The PCT connection: Espirito Santo was among the first Brazilian states "
        "to receive Portuguese colonists after the initial settlements in Bahia. "
        "The state's Portuguese name (Espirito Santo — Holy Spirit) was given by "
        "Vasco Fernandes Coutinho in 1535. Coffee arrived in the state in the "
        "19th century as part of the same expansion from the Coffee Belt "
        "that reached Sao Paulo and Minas Gerais. "
        "Conillon distinction: standard Conillon is Brazil's commercial robusta — "
        "primarily used for instant coffee, expresso blends, and bulk export. "
        "The quality revolution: since 2015, a small number of producers in "
        "the Pedra Azul mountains (900-1,100m) have been producing Conillon "
        "at specialty grade — the first time the variety has been treated "
        "with the same quality framework as arabica. "
        "Fazenda Camocim (Seabra family): the leader of this revolution. "
        "At 900-1,100m on basalt-derived soils in the Pedra Azul mountains, "
        "with biodynamic certification, the Camocim Conillon is not "
        "a compromise — it is a different kind of coffee. "
        "The distinction: specialty Conillon has less acidity than arabica "
        "but more body and a deeper, darker flavour profile. "
        "It is the first robusta-type coffee to achieve international specialty recognition."
    ),
    "production_technique": (
        "Fazenda Camocim Conillon production: "
        "Biodynamic certification: Demeter-certified since 2004; "
        "Rudolf Steiner's biodynamic calendar governs planting, harvest, and processing. "
        "Variety: Conillon (Coffea canephora var. canephora) — Brazilian robusta selection; "
        "the Camocim clonal selection has been selected over 20 years for cup quality "
        "rather than yield. "
        "Altitude: 900-1,100m on the Pedra Azul basalt massif — "
        "exceptional for Conillon (standard Conillon is grown at 200-500m). "
        "Harvest: manual selective picking; Conillon ripens unevenly "
        "so selective picking is essential for specialty quality. "
        "Processing: natural/sun-dried on raised beds; the biodynamic farm calendar "
        "determines processing days (fruit days preferred for harvest and drying). "
        "The natural process on Conillon at altitude creates a dramatically different "
        "cup from standard Conillon: dark chocolate, tobacco, dried fruit, "
        "low acidity with high sweetness from the natural processing fermentation. "
        "Roasting: medium-dark to medium; Conillon needs more heat than arabica "
        "due to its higher moisture content and denser bean structure. "
        "The 80-20 blend context: Camocim Conillon is also used in high-end "
        "espresso blends by specialty roasters to add body and reduce acidity — "
        "a direct reversal of the traditional 'robusta for cheapness' model."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "coffee",
            "beverage": "Uganda Sipi Falls Fine Robusta (Ugandan specialty canephora)",
            "connection": (
                "Both are specialty-grade Coffea canephora from different continents. "
                "Uganda's Sipi Falls (Elgon sub-region) and Espirito Santo's Pedra Azul "
                "are the two most cited examples of 'specialty robusta' globally. "
                "The comparison teaches that robusta's reputation for low quality "
                "is a growing-condition problem, not a variety limitation."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Brazil Sul de Minas Natural Arabica (same state cluster, opposite variety)",
            "connection": (
                "The internal Brazilian comparison: same natural processing method, "
                "same mountain Brazilian context, opposite variety (arabica vs Conillon). "
                "Sul de Minas: lighter body, higher acidity, stone fruit. "
                "Camocim Conillon: heavier body, lower acidity, dark chocolate and tobacco. "
                "The comparison dismantles the arabica-superiority assumption."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Vietnam Arabica Da Lat (mountain robusta-to-arabica transition region)",
            "connection": (
                "Both are examples of the quality transition happening in traditional "
                "robusta-producing regions. Vietnam's Da Lat highlands and Brazil's "
                "Espirito Santo mountains are both producing arabica-level quality "
                "from canephora varieties through altitude and careful farming."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Indonesia Kopi Luwak (civet coffee, Sumatra — variety indeterminate)",
            "connection": (
                "Both are examples of how context transforms a commodity coffee variety "
                "into a premium narrative. Kopi Luwak transforms robusta through civet digestion; "
                "Camocim transforms Conillon through biodynamic altitude farming. "
                "Both challenge the assumption that variety alone determines quality."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Dark brown at medium-dark roast; the Conillon bean is smaller and denser than arabica; less crema on espresso but more body",
        "nose": "Dark chocolate, roasted grain, dried tobacco leaf, faint dried mushroom, earthy mineral from the basalt mountain soils",
        "palate": "Entry: low-acidity, full body from high-solids Conillon extraction. Mid-palate: dark chocolate and roasted grain dominant. Finish: clean and dry with a tobacco-mineral persistence",
        "texture": "The highest body of any Brazilian coffee tradition; the Conillon's higher caffeine and different lipid profile creates a syrupy weight that arabica cannot match",
        "finish": "25-35 seconds (shorter than arabica from equivalent altitude); dark chocolate and grain; the biodynamic mineral character adds a dry stone finish",
        "conclusion": "The category-redefining coffee — proof that quality is a cultivation choice, not a variety limitation"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Fazenda Camocim Conillon Biodynamic (natural, single harvest)",
            "criteria": "Demeter biodynamic; natural process; single harvest; "
                "the reference expression for specialty Conillon globally",
            "markers": "Fazenda Camocim Conillon; BC: specialty roasters only; US ~$20-28/250g"
        },
        {
            "tier": 3,
            "tier_name": "Espirito Santo Conillon Specialty (other farms, mountain grade)",
            "criteria": "Mountain-grown Conillon (800m+); specialty grade processing; "
                "the regional category without single-farm pricing",
            "markers": "ES Conillon Specialty; BC: specialty roasters; US ~$15-22/250g"
        },
        {
            "tier": 2,
            "tier_name": "Espirito Santo Conillon Fine Cup (certified)',",
            "criteria": "Fine cup certification from CoE or BSCA; above-standard quality; "
                "introduction to the specialty Conillon character",
            "markers": "ES Fine Cup; BC/US ~$12-18/250g"
        },
        {
            "tier": 1,
            "tier_name": "Brazilian espresso blend with Conillon component",
            "criteria": "Commercial espresso blend; Conillon as body-contributor component; "
                "widely available; introduction to the variety character in a familiar format",
            "markers": "Various commercial espresso blends; BC/US ~$10-15/250g"
        }
    ],
    "service_intelligence": {
        "temperature": "Espresso: 93-94 degrees C, 9 bar, 25-28s; the higher temperature develops the chocolate character. Filter: 94-96 degrees C (higher than arabica to extract the denser bean)",
        "vessel": "Espresso: pre-heated demitasse; the body requires containment. Filter: ceramic flat-bottom for maximum body extraction",
        "technique": "Camocim Conillon as a specialty coffee education tool: "
            "blind tasting against a Sul de Minas arabica natural. "
            "The result: most guests cannot identify which is robusta because "
            "the altitude and biodynamic farming have produced a quality level "
            "that the variety distinction no longer predicts. "
            "The sales script: 'The coffee world has been wrong about robusta for 100 years. "
            "This is the correction.'",
        "programme_position": "Specialty coffee education; Brazil origin depth; espresso bar single-origin robusta offering",
        "verbal_presentation": "Espirito Santo Conillon — Pedra Azul mountains, Brazil. "
            "Biodynamic. Mountain-grown at 1,000 metres. "
            "The robusta that rewrites the rulebook."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Fazenda Camocim (Seabra family) — Demeter-certified biodynamic Conillon pioneer",
        "producer_location": "Domingos Martins, Espirito Santo, Brazil",
        "key_person": "Pedro Domingo Seabra (owner; biodynamic advocate)",
        "bc_distributor": "Specialty roasters in BC source Camocim directly; no mass-market distribution",
        "us_distributor": "Counter Culture Coffee and Intelligentsia have featured Camocim Conillon; "
            "specialty importers (Cafe Imports, Mercanta) carry Espirito Santo specialty Conillon",
        "uk_distributor": "Has Bean Coffee (UK); Square Mile Coffee",
        "price_tier": "Entry: $10-15 (blended). Mid: $12-18 (Fine Cup). Premium: $15-22 (specialty mountain). Ultra: $20-28 (Camocim biodynamic single harvest).",
        "availability_notes": "Fazenda Camocim is available seasonally through specialty importers. "
            "Espirito Santo specialty Conillon is increasingly stocked by leading specialty roasters "
            "as the 'specialty robusta' category grows in recognition."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Moqueca de peixe (Espirito Santo fish stew with coconut milk and dendê oil)",
            "pairing_type": "complement",
            "rationale": "Moqueca Capixaba is the regional dish of Espirito Santo — "
                "a fish stew with tomato, coconut milk, and dendê (palm oil), "
                "served in a clay pot. A cup of Camocim Conillon after the moqueca "
                "is the authentic Espirito Santo meal close. "
                "The dark chocolate and grain of the coffee cuts through the "
                "coconut oil richness and prepares the palate for the meal's finish."
        },
        {
            "technique_id": "",
            "dish": "Brigadeiro (Brazilian chocolate truffle with condensed milk)",
            "pairing_type": "bridge",
            "rationale": "Brigadeiro — Brazil's national confection — uses condensed milk "
                "and cocoa powder to create a dark-sweet truffle. "
                "The dark chocolate and tobacco character of Conillon bridges "
                "the cocoa-condensed milk sweetness of the brigadeiro "
                "through the shared dark chocolate register."
        }
    ],
    "source": "BSCA (Brazilian Specialty Coffee Association) Conillon specialty classification; "
        "Fazenda Camocim production documentation; "
        "Demeter biodynamic certification records; "
        "Cafe Imports Brazil sourcing documentation",
    "trail_connection": "PCT-13",
    "trail_note": "PCT Region 13: Brazil (Coffee). "
        "Espirito Santo is the PCT's most historically continuous coffee state — "
        "Portuguese since 1535, coffee-growing since the 19th century, "
        "now producing the world's first specialty Conillon. "
        "The biodynamic Conillon of Fazenda Camocim represents the "
        "Portuguese colonial agricultural legacy producing "
        "its highest quality expression in the 21st century."
})

session.commit_batch()

session.finish()
