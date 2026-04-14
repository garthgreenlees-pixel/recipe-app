#!/usr/bin/env python3
"""
PCT-13 Brazilian Coffee + PCT-9 Kristang + PCT-10 Macau Coffee
+ PCT-4 Cape Verde Grogue + PCT×WADT Caribbean Rum + PCT-14×PMT Hawaii Kona Coffee
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="coffee",
    region="Brazil — Santos, Cerrado, Sul de Minas",
    output_dir="./provenance_output/beverage",
    starting_entry=2,
    session_number=4,
    running_total=19
)

# ============================================================
# BRAZILIAN COFFEE — PCT-13
# ============================================================

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "natural processed specialty",
    "region": "Brazil — Sul de Minas / Minas Gerais",
    "name": "Brazil Sul de Minas — Natural and Pulped Natural",
    "terroir_origin": (
        "Brazil is the world's largest coffee producer — 40% of global supply — and the PCT's most "
        "significant agricultural legacy in the Americas. Coffee (Coffea arabica) was introduced to "
        "Brazil in 1727 by Francisco de Melo Palheta, a Portuguese officer who smuggled seeds from "
        "French Guiana by charming the Governor's wife into gifting him clippings. Within a century, "
        "Brazil had become the world's dominant coffee power. Sul de Minas (Southern Minas Gerais) "
        "is the heartland of Brazilian specialty coffee: the mountainous southern region of Minas "
        "Gerais state, 800–1,200m altitude, with distinct wet and dry seasons. "
        "The altitude moderates tropical heat to create the slow cherry ripening necessary for "
        "sugar development and complexity. Sul de Minas coffees are typically softer, sweeter, and "
        "lower in acidity than Ethiopian or Colombian alternatives — reflecting Brazil's geological "
        "character (old, flat, weathered soils vs. Ethiopia's volcanic highlands). "
        "Fazenda Santa Inês (near Carmo de Minas) is the benchmark Sul de Minas estate: "
        "their Yellow Bourbon variety on red-clay soil at 1,100m produces consistently top-rated "
        "scores at Cup of Excellence."
    ),
    "production_technique": (
        "Brazil's primary processing method is natural (dry process) — the most ancient method globally "
        "and still dominant because Brazil's dry harvest season (June–September) provides the low "
        "humidity required for slow cherry drying on raised beds or patios. "
        "Natural process: whole cherries dried in the sun for 3–5 weeks; the fruit pulp ferments "
        "against the bean, imparting fruit-forward, wine-like, chocolatey complexity. "
        "Pulped natural (honey process): the cherry skin is removed mechanically but varying amounts "
        "of mucilage (the sticky fruit layer) are left on the bean during drying. "
        "Yellow honey: minimal mucilage, 10–14 days; Red honey: more mucilage, 14–21 days; "
        "Black honey: maximum mucilage, 21–30+ days — approaching natural process complexity. "
        "Brazil's Bourbon variety (Yellow Bourbon, Red Bourbon) and Mundo Novo are the "
        "primary heritage arabica varieties at Sul de Minas specialty estates. "
        "Catuaí and Acaiá are the commercially dominant processed varieties. "
        "Roast profile: medium to medium-dark for espresso use; light-medium for filter/pour-over "
        "specialty consumption. The Cup of Excellence programme (Brazil, annual) has raised "
        "Brazilian specialty coffee's global profile since 1999."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Australian Shiraz (McLaren Vale / Barossa)",
         "connection": "Both express warm-climate, sun-ripened terroir through fruit-forward, low-acid "
                       "profiles with chocolate and dark fruit character. Brazilian natural process coffee "
                       "and Australian Shiraz occupy the same sensory register: ripe, generous, low-tension "
                       "beverages that reward casual enjoyment over analytical dissection. Both challenge "
                       "the Northern Hemisphere assumption that complexity requires high acidity"},
        {"tradition": "coffee", "beverage": "Ethiopian Yirgacheffe (washed process)",
         "connection": "The defining contrast within specialty coffee: Ethiopian washed Yirgacheffe "
                       "(floral, jasmine, citrus, bright acidity) vs. Brazilian natural Sul de Minas "
                       "(chocolate, dried cherry, nuts, low acidity). Both are essential to any serious "
                       "coffee programme — they represent opposite poles of arabica expression and "
                       "demonstrate that terroir in coffee is as profound as in wine"}
    ],
    "sensory_profile": {
        "appearance": "Brewed: medium brown to deep brown depending on roast; crema-dense in espresso; "
                      "clear in filter brew at lighter roasts",
        "nose": "Natural process: dark chocolate, dried cherry, blueberry, dried fig, wine-like "
                "fermentation notes, hazelnut. Pulped natural: milk chocolate, caramel, stone fruit "
                "without the full fermented character of natural. Both: warm, sweet, inviting",
        "palate": "Low-to-medium acidity (the hallmark of Brazilian coffee); full body; "
                  "long sweet finish; chocolate and nut persistence; "
                  "Natural: additional dried fruit and slight winey complexity; "
                  "Pulped natural: cleaner, more caramel-milk chocolate. "
                  "Excellent cold brew base: low acidity reads as smoothness at cold temperature",
        "conclusion": "Brazil is the world's coffee default — the base blend in most commercial espresso. "
                      "Single-origin Sul de Minas specialty demonstrates what that default looks like when "
                      "executed with precision. Essential on any serious coffee programme as the sweet, "
                      "chocolate anchor in a cupping flight."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Cup of Excellence Winner / Single Farm Natural", "criteria": "Cup of Excellence "
          "scored 87+; named estate and lot; Yellow/Red Bourbon or Mundo Novo variety; natural or black honey process",
          "markers": "Fazenda Santa Inês; Daterra; Cup of Excellence auction lot; micro-lot packaging; "
                     "roasters: Intelligentsia, Counter Culture, George Howell"},
        {"tier": 3, "tier_name": "Specialty Single Origin", "criteria": "Named farm or co-op; traceable lot; "
          "SCA score 84+; specialty roaster sourced",
          "markers": "Carmo de Minas or Sul de Minas origin; specialty roaster label; farm name prominent"},
        {"tier": 2, "tier_name": "Commercial Specialty", "criteria": "Region-labelled; consistent quality; "
          "SCA score 80–84; widely distributed specialty",
          "markers": "Brazil Sul de Minas origin; specialty roaster mid-range; espresso blend base quality"},
        {"tier": 1, "tier_name": "Santos Commercial", "criteria": "Santos grading system (export quality grade); "
          "Santos 2/3 (screen size grading); the conventional trade standard",
          "markers": "Santos port designation; commercial blend component; not traceable to farm"}
    ],
    "service_intelligence": {
        "temperature": "Espresso: 90–93°C extraction; filter/pour-over: 93–96°C; cold brew: 4°C/12–24hr steep",
        "vessel": "Espresso: demitasse (60–90mL); filter: ceramic pour-over or Chemex; cold brew: tall glass over ice",
        "technique": "Espresso: 1:2 ratio (18g in : 36g out), 26–30 seconds. Light-roast filter: Hario V60, "
                     "16:1 water:coffee ratio, 3-minute total brew time. Cold brew: coarse grind, 12:1 ratio, "
                     "cold immersion 12 hours — Brazil naturals are ideal cold brew bases due to low acidity. "
                     "Milk pairing: Brazil's chocolate-caramel notes are the ideal espresso base for flat whites "
                     "and cortados — milk amplifies the sweetness without fighting the acidity",
        "programme_position": "Espresso blend foundation; single origin filter option; cold brew base. "
                              "The most versatile and commercially important origin on any café programme",
        "verbal_presentation": "Brazil Sul de Minas — natural process from the hillsides of Minas Gerais. "
                               "Dried in the sun on raised beds; the cherry fruit ferments against the bean "
                               "for four weeks. Dark chocolate, dried cherry, hazelnut. The coffee that runs "
                               "the world's espresso machines."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Fazenda Santa Inês (Carmo de Minas, Sul de Minas)",
        "producer_location": "Carmo de Minas, Sul de Minas, Minas Gerais, Brazil",
        "key_person": "Renzo Carvalho Dias (owner, Fazenda Santa Inês)",
        "production_volume": "~100,000kg green coffee annually; among Brazil's most awarded specialty estates",
        "certifications": ["Rainforest Alliance (multiple Sul de Minas producers)", "Cup of Excellence winner multiple years",
                           "BSCA (Brazilian Specialty Coffee Association) member"],
        "bc_distributor": "Alpha Coffee (Vancouver specialty importer) [NEEDS VERIFICATION]; "
                          "49th Parallel Coffee (Vancouver roaster, sources Brazilian specialty) [NEEDS VERIFICATION]",
        "us_distributor": "Intelligentsia Coffee (direct trade partner, sourcing Sul de Minas); "
                          "Counter Culture Coffee (direct trade Sul de Minas); "
                          "Daterra coffee (direct export): daterra.com.br",
        "uk_distributor": "Has Bean Coffee; Workshop Coffee; Monmouth Coffee (all source Brazilian specialty)",
        "price_tier": "Specialty (green): US$4–8/lb; roasted retail: $18–35 per 250g; "
                      "Cup of Excellence lots: $10–25/lb green at auction",
        "availability_notes": "Brazilian specialty widely available through specialty roasters in BC and US. "
                              "Fazenda Santa Inês specifically: look for it on café menus as a featured single origin. "
                              "For commercial programme use: 49th Parallel (BC), Intelligentsia (US national), "
                              "Counter Culture (US national) all source traceable Sul de Minas lots."
    },
    "trail_connection": "PCT-13",
    "trail_note": "Coffee in Brazil is the PCT's largest agricultural legacy by volume. Palheta's 1727 smuggling "
                  "of French Guiana coffee seeds (the African-origin arabica brought to the Americas by the French) "
                  "gave Brazil what became the world's most important coffee industry within 100 years. "
                  "The Portuguese colonial plantation system — using enslaved African labour (the WADT intersection) "
                  "— built the infrastructure that still shapes Brazilian coffee geography today. "
                  "Sul de Minas's small-farm specialty revolution (1990s–present) is the post-colonial "
                  "redemption arc: individual fazendas winning Cup of Excellence on quality rather than volume.",
    "food_pairings": [
        {"technique_id": "", "dish": "Brigadeiro (Brazilian chocolate truffle)",
         "pairing_type": "complement",
         "rationale": "Brazil's iconic confection and its coffee are made from the same flavour register: "
                      "dark chocolate and condensed milk in the brigadeiro mirror the coffee's chocolate-caramel body"},
        {"technique_id": "", "dish": "Canelé de Bordeaux",
         "pairing_type": "complement",
         "rationale": "The caramelised beeswax crust and custard interior of the canelé echo "
                      "the natural-process coffee's caramel-fruit complexity exactly"}
    ],
    "source": "Brazilian Specialty Coffee Association (BSCA) data; Cup of Excellence Brazil results 1999–2025; "
              "Fazenda Santa Inês farm documentation; Intelligentsia direct trade sourcing notes",
})

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "cerrado specialty",
    "region": "Brazil — Cerrado Mineiro",
    "name": "Brazil Cerrado Mineiro — The Savanna Coffee",
    "terroir_origin": (
        "The Cerrado Mineiro (Cerrado of Minas Gerais) is the first Brazilian coffee region to receive "
        "Geographical Indication (GI) status — awarded in 2005. The Cerrado is a vast tropical savanna "
        "biome covering central Brazil; the coffee-growing portion sits at 800–1,300m on the western "
        "plateau of Minas Gerais, with a dramatically different climate than Sul de Minas: "
        "the Cerrado has a very defined dry season (April–September) with 0mm rainfall, followed by "
        "a wet season with concentrated rainfall. This extreme seasonality — shared with few other "
        "coffee regions — produces uniform cherry ripening, enabling mechanical harvesting on flat "
        "terrain (unlike the steep hillsides of Sul de Minas). The result: large-scale, highly "
        "mechanised production with the consistency and traceability that specialty buyers require. "
        "Patrocínio, Araxá, and Patos de Minas are the main municipalities. "
        "The flat savanna terrain and mechanisation make Cerrado the most technologically advanced "
        "coffee production system in the world, combining scale with speciality quality."
    ),
    "production_technique": (
        "Cerrado's dry season enables precision control of the natural and pulped natural processes. "
        "Mechanical harvesting (stripping) is standard: tractor-mounted or manual strippers remove all "
        "cherries simultaneously. Because Cerrado's climate ensures uniform ripening, mechanical "
        "harvesting does not significantly compromise quality (unlike regions where ripening is staggered). "
        "After harvest: natural, pulped natural, or washed processing depending on estate. "
        "Daterra Estate (Patrocínio, Cerrado) pioneered precision specialty in the Cerrado: "
        "varietal separation (Icatu, Bourbon, Catuaí), controlled fermentation tanks, moisture-"
        "controlled drying rooms, and block-by-block traceability. Daterra's Masterpiece Series "
        "achieves SCA scores above 90 — extraordinary for mechanically-harvested coffee. "
        "The Cerrado's high altitude combined with UV-intense savanna sun contributes to high sugar "
        "concentration in the cherry — translating to sweetness and body in the cup."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Marlborough Sauvignon Blanc (New Zealand)",
         "connection": "Both are defined by their distinct continental climate (cold/dry vs wet/warm alternation) "
                       "producing flavour-consistent, commercially reliable, technology-enabled quality products. "
                       "Marlborough SB and Cerrado coffee both democratised specialty production through "
                       "scale-friendly mechanisation that delivers consistent flavour at volume"},
        {"tradition": "coffee", "beverage": "Colombian Huila Washed Arabica",
         "connection": "Direct comparison: Cerrado natural (low acidity, chocolate, caramel, full body) vs. "
                       "Colombian Huila washed (bright acidity, stone fruit, tea-like clarity). Both are "
                       "benchmark quality in their respective styles. Huila shows what washed process achieves; "
                       "Cerrado natural shows what sun-drying adds. Both are essential programme references"}
    ],
    "sensory_profile": {
        "appearance": "Medium-deep brown in filter brew; dense espresso crema in medium-dark roast",
        "nose": "Milk chocolate, caramel, toffee, Brazil nut, dried plum; cleaner and less winey "
                "than Sul de Minas natural; the Cerrado's dry climate reduces over-fermentation risk",
        "palate": "Full body (fuller than Sul de Minas due to higher density cherry); "
                  "low-to-medium acidity; long sweet caramel-chocolate finish; "
                  "excellent base for espresso and milk drinks; "
                  "Daterra Masterpiece expressions add layered complexity from varietal separation",
        "conclusion": "Cerrado Mineiro demonstrates that scale and quality are not opposites. "
                      "Daterra Estate is the world's benchmark for precision large-scale specialty coffee "
                      "production. Their GI and Cup of Excellence wins have permanently advanced "
                      "Brazilian coffee's reputation beyond commodity."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Daterra Masterpiece / Cup of Excellence Reserve", "criteria": "SCA 90+; "
          "varietal-specific lot; block traceability; precision fermentation; Daterra Patrocínio benchmark",
          "markers": "Daterra Masterpiece Series; Cup of Excellence Cerrado winner; £30–50 per 250g roasted"},
        {"tier": 3, "tier_name": "Cerrado GI Specialty", "criteria": "GI-certified Cerrado Mineiro origin; "
          "SCA 84+; traceable farm; specialty roaster sourced",
          "markers": "GI designation on bag; Patrocínio or Araxá origin; specialty roaster purchase"},
        {"tier": 2, "tier_name": "Cerrado Commercial Specialty", "criteria": "Cerrado region; "
          "SCA 80–84; consistent; widely traded by specialty importers",
          "markers": "Cerrado label; commercial specialty green import; mid-range roaster sourcing"},
        {"tier": 1, "tier_name": "Cerrado Commercial Grade", "criteria": "Santos export grading; "
          "bulk mechanically harvested; commodity market price",
          "markers": "Santos 2 or 3 grading; blend component; no farm traceability"}
    ],
    "service_intelligence": {
        "temperature": "Espresso: 91–93°C; filter: 93–95°C; cold brew: 4°C",
        "vessel": "Espresso or filter as required by programme",
        "technique": "Cerrado naturals excel as espresso blends and as single-origin filter at medium roast. "
                     "Daterra Masterpiece expressions warrant single-origin treatment: "
                     "Hario V60 or Kalita Wave, medium-coarse grind, 15:1 water:coffee ratio. "
                     "Cold brew: excellent — full body, sweetness, low acidity, 16:1 ratio, 14hr cold steep",
        "programme_position": "Espresso blend anchor or single origin filter feature; cold brew base. "
                              "The most cost-effective specialty origin for high-volume espresso programmes",
        "verbal_presentation": "Cerrado Mineiro — Brazil's first GI-protected coffee region. Savanna plateau, "
                               "uniform harvest, dried in the intense Cerrado sun. The world's most precise "
                               "large-scale specialty coffee production: milk chocolate, caramel, full body."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Daterra Estate (Patrocínio, Cerrado Mineiro)",
        "producer_location": "Patrocínio, Cerrado Mineiro, Minas Gerais, Brazil",
        "key_person": "Luis Paulo Dias Pereira Filho (Daterra owner)",
        "production_volume": "~1.5 million kg green coffee annually; largest premium single-estate in Brazil",
        "certifications": ["Cerrado Mineiro GI (first Brazilian coffee GI, 2005)", "Rainforest Alliance",
                           "BSCA member", "Multiple Cup of Excellence awards"],
        "bc_distributor": "49th Parallel Coffee (Vancouver — sources Cerrado specialty) [NEEDS VERIFICATION for Daterra specifically]; "
                          "Nemesis Coffee [NEEDS VERIFICATION]",
        "us_distributor": "Intelligentsia Coffee (direct trade Daterra); Stumptown Coffee (Portland, sources Cerrado); "
                          "direct green import: daterra.com.br/exportacao",
        "uk_distributor": "Has Bean; Origin Coffee; Round Hill Roastery",
        "price_tier": "Specialty green: $4–9/lb; Masterpiece auction lots: $15–35/lb; "
                      "roasted retail: $20–45 per 250g",
        "availability_notes": "Daterra available through specialty roasters globally. BC: 49th Parallel, "
                              "Prototype Coffee, and small batch roasters source Cerrado. US: Intelligentsia "
                              "(Chicago/LA/NY), Stumptown (national) carry Cerrado-origin lots."
    },
    "trail_connection": "PCT-13",
    "trail_note": "The Cerrado's coffee history is inseparable from Brazil's 20th-century agricultural modernisation — "
                  "a post-colonial effort to turn the 'empty' savanna into productive farmland using government-funded "
                  "Embrapa research stations. The PCT connection: the original coffee brought by Palheta (1727) was "
                  "Ethiopian-origin arabica propagated through French Guiana, carried on the same Atlantic trade "
                  "routes that defined Portuguese colonial navigation. The Cerrado's arabica are direct botanical "
                  "descendants of that 18th-century Portuguese smuggling mission.",
    "food_pairings": [
        {"technique_id": "", "dish": "Pain au chocolat (croissant pastry with dark chocolate)",
         "pairing_type": "complement",
         "rationale": "Cerrado's milk chocolate and caramel profile mirror the pastry's butter-chocolate "
                      "richness — the most natural espresso-pastry pairing on any café programme"},
        {"technique_id": "", "dish": "Pão de queijo (Brazilian cheese bread)",
         "pairing_type": "complement",
         "rationale": "Brazil's iconic cheese-tapioca roll pairs with Brazilian coffee by terroir logic: "
                      "the warm savanna character of the Cerrado coffee echoes the manioc starch and "
                      "queijo minas of the same region"}
    ],
    "source": "Cerrado Mineiro GI documentation (EMBRAPA); Daterra Estate official documentation; "
              "Cup of Excellence Brazil annual results; BSCA membership records",
})

session.commit_batch()
print(f"\n[BATCH 16 COMMITTED — Brazilian Coffee Sul de Minas + Cerrado]\n")

# ============================================================
# SWITCH — PCT-9: Kristang / Malacca
# ============================================================

session.switch_region("ceremonial", "Malaysia — Malacca (Kristang)")

session.add_beverage({
    "tradition": "ceremonial",
    "sub_tradition": "kristang beverage culture",
    "region": "Malaysia — Malacca / Kristang community",
    "name": "Kristang Beverage Traditions — Malacca",
    "terroir_origin": (
        "The Kristang people of Malacca, Malaysia are the descendants of Portuguese colonists who settled "
        "in Malacca after its conquest by Afonso de Albuquerque in 1511 — a pivotal moment in the "
        "PCT as it established Portugal's Southeast Asian trade hub. Over 500 years of intermarriage with "
        "Malay, Chinese, and Indian communities in the Malaccan Straits, the Kristang developed a "
        "unique creole culture: they speak Kristang (a Portuguese-Malay creole language), practice "
        "a syncretic form of Portuguese Catholicism, and maintain food and drink traditions that are "
        "the most direct surviving expression of 16th-century Portuguese culinary culture anywhere "
        "in Southeast Asia. The Kristang community today numbers ~3,000 in Malacca's Portuguese Settlement "
        "(Padrao neighbourhood, established 1933). Their beverage culture is the least documented node "
        "on the PCT — oral tradition rather than written record."
    ),
    "production_technique": (
        "Kristang beverage traditions blend Portuguese, Malay, and Chinese influences: "
        "1. Toddy (Palm wine): The Kristang consume palm toddy (from coconut or nipah palm) much as "
        "the surrounding Malay community does — fermented sap drunk fresh or slightly aged. "
        "The Portuguese colonial presence normalised the consumption of fermented palm drinks alongside "
        "imported wine. 2. Tapai (fermented rice/tapioca wine): traditional fermentation using ragi "
        "(mould starter cake) applied to glutinous rice or tapioca — a direct parallel to the "
        "sake/rice wine traditions throughout Asia that the Portuguese encountered and documented. "
        "3. Christmas Beverages: Kristang Christmas ('Natal') includes ponche (a spiced fruit punch "
        "using locally available tropical fruits — rambutan, durian, longan — spiced with Portuguese "
        "cinnamon-clove tradition adapted to tropical ingredients). "
        "4. Brandy and Cincalok: Brandy (Portuguese-origin spirit tradition) is used in the "
        "fermentation of cincalok (fermented tiny shrimp) — a Kristang culinary signature where "
        "the European spirit stabilises fermented seafood in the tropical climate. "
        "5. Portuguese wine: communion wine and festive wine, historically imported from Portugal "
        "via the Portuguese trade, now more commonly local beer or toddy at festivals. "
        "Note: This entry is the most underdocumented on the PCT — sources are primarily "
        "ethnographic fieldwork and community oral history rather than commercial documentation."
    ),
    "cross_tradition_parallels": [
        {"tradition": "ceremonial", "beverage": "Goan Christmas Feni (PCT-8 connection)",
         "connection": "Both are ceremonial beverage traditions in former Portuguese Catholic colonial "
                       "communities in Asia (Goa and Malacca) that blend European Catholic festival "
                       "drinking customs (Christmas ponche, Easter wine) with indigenous Asian fermentation "
                       "traditions (feni/toddy/tapai). Both communities have maintained their ceremonies "
                       "500+ years after Portuguese political withdrawal"},
        {"tradition": "fermented", "beverage": "Tapai / Rice wine across Southeast Asia",
         "connection": "Kristang tapai places the community within the broader Southeast Asian rice "
                       "fermentation tradition that the Portuguese documented and were the first Europeans "
                       "to systematically record. Tapai in Malacca and tapai in Borneo, tuak in "
                       "Sarawak, and sake in Japan share the same Aspergillus-mould saccharification "
                       "process — the Kristang represent the confluence of European documentation "
                       "with indigenous fermentation practice"}
    ],
    "sensory_profile": {
        "appearance": "Toddy: cloudy white to pale yellow; Tapai: milky-white, viscous; "
                      "Christmas ponche: amber to deep red depending on fruit and brandy base",
        "nose": "Toddy: fresh ferment, tropical sweetness, yeast, slight sour edge; "
                "Tapai: mild ferment, sweet rice, light acetone (controlled), gentle warmth; "
                "Kristang ponche: tropical fruit (rambutan, longan), cinnamon, clove, warm brandy base — "
                "the most complex and unique Kristang beverage expression",
        "palate": "Toddy: light, refreshing, slightly sour-sweet, 4–7% ABV; "
                  "Tapai: sweet-sour, mildly warming, 4–8% ABV, low complexity but culturally significant; "
                  "Ponche: sweet-spiced, warm, the European Christmas drink tradition translated to the tropics — "
                  "unmistakably both Portuguese and Malaccan simultaneously",
        "conclusion": "Kristang beverage traditions are the PCT's living museum — the most undiluted "
                      "cultural survival of Portuguese colonial drink customs in Southeast Asia. "
                      "For a professional programme, the Kristang ponche recipe (tropical fruits + "
                      "brandy + Portuguese spices) is a genuinely unique seasonal cocktail template."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Documented Authentic Kristang Recipe", "criteria": "Community-sourced recipe "
          "from Malacca's Portuguese Settlement; named family tradition; ethnographic verification",
          "markers": "Joan Margaret Marbeck documentation; Kristang community cultural association recipes"},
        {"tier": 3, "tier_name": "Contemporary Kristang-inspired", "criteria": "Portuguese-Malaccan fusion "
          "approach using authentic ingredient list (Portuguese brandy/wine + local tropical fruit + "
          "cinnamon-clove spice base) adapted for modern bar programme",
          "markers": "Named inspiration; authentic spice and fruit sourcing; PCT story intact"},
        {"tier": 2, "tier_name": "Regional Malaccan", "criteria": "Uses local tapai or toddy base; "
          "Malaccan context; some Portuguese cultural connection noted",
          "markers": "Malacca origin; local ceremonial context"},
        {"tier": 1, "tier_name": "Generic Southeast Asian Palm Wine", "criteria": "Commercial toddy or "
          "tapai without Kristang cultural specificity; no Portuguese connection maintained",
          "markers": "Commercial palm toddy; mass production; no Kristang attribution"}
    ],
    "service_intelligence": {
        "temperature": "Toddy: 10–14°C (chilled); Tapai: room temperature; Ponche: warm (60°C) or room temp",
        "vessel": "Traditional: clay cup or small glass for toddy; clay pot for tapai; "
                  "punch bowl with ladle for Christmas ponche. Bar use: rocks glass or punch cup",
        "technique": "Kristang Christmas Ponche (documented recipe basis): brandy or aguardente base, "
                     "sweetened with palm sugar (gula melaka), spiced with cinnamon and cloves, "
                     "extended with tropical fruit juice (rambutan, longan, star fruit). "
                     "Serve warm in winter season menus or room temp in tropical context. "
                     "Bar programme adaptation: 'Kristang Punch' — Portuguese brandy + gula melaka "
                     "syrup + cinnamon bark + longan juice + lime; garnish with star anise and lime",
        "programme_position": "Seasonal cocktail (Christmas/winter); cultural education piece; "
                              "Southeast Asian tasting menu accompaniment; storytelling cocktail "
                              "for PCT-themed events",
        "verbal_presentation": "The Kristang community of Malacca — 500 years of Portuguese Catholic "
                               "tradition in Southeast Asia. Their Christmas ponche: Portuguese brandy, "
                               "local palm sugar, cinnamon and clove from the same spice trade that "
                               "brought the Portuguese to Malacca in 1511."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Kristang community of the Portuguese Settlement, Malacca (home production only)",
        "producer_location": "Padrao neighbourhood, Malacca, Malaysia (Jalan d'Albuquerque)",
        "key_person": "Joan Margaret Marbeck (Kristang language and culture documenter); "
                      "Hugo Fernandes (Kristang cultural association)",
        "production_volume": "Home production only; no commercial scale; oral tradition",
        "certifications": ["UNESCO recognition under consideration (Kristang language and culture intangible heritage)"],
        "bc_distributor": "Not applicable — no commercial product exists",
        "us_distributor": "Not applicable — cultural documentation only",
        "uk_distributor": "Not applicable",
        "price_tier": "Ceremonial / non-commercial",
        "availability_notes": "Kristang beverage traditions exist only in the Portuguese Settlement of Malacca. "
                              "For bar programme inspiration: the ponche formula can be executed with "
                              "Portuguese brandy (available through Iberian spirits importers) + "
                              "Malaysian ingredients (gula melaka, longan, star fruit from Asian grocery). "
                              "For cultural research: contact Kristang Cultural Association, Malacca."
    },
    "trail_connection": "PCT-9",
    "trail_note": "The Kristang are the PCT's most poignant human marker. 500 years after Afonso de Albuquerque "
                  "captured Malacca, their community still speaks a Portuguese-creole language, still celebrates "
                  "Christmas with Portuguese customs, and still makes ponche with brandy and cinnamon. "
                  "Their beverages are the PCT's most direct surviving cultural DNA — the drink traditions "
                  "of 16th-century Lisbon, preserved in tropical Malaysia.",
    "food_pairings": [
        {"technique_id": "", "dish": "Debal curry (Kristang devil's curry — Christmas Day leftovers stew)",
         "pairing_type": "bridge",
         "rationale": "Debal is the Kristang's most distinctive dish: a vinegar-spiced meat and "
                      "vegetable stew made from Christmas leftovers. The ponche's sweetness bridges "
                      "with the debal's vinegar-spice complexity — the Portuguese sweet-sour tension "
                      "that defines the cuisine"},
        {"technique_id": "", "dish": "Feng (Kristang spiced offal)",
         "pairing_type": "complement",
         "rationale": "Feng uses brandy and vinegar in its traditional preparation — the ponche's "
                      "brandy base is the same spirit used to cook the dish"}
    ],
    "source": "Joan Margaret Marbeck 'Linggu Kristang' (Kristang language documentation); "
              "Malacca Portuguese Settlement cultural association materials; "
              "Jo Kukathas ethnographic research on Kristang community; "
              "New Straits Times Malacca Portuguese community features",
})

session.commit_batch()
print(f"\n[BATCH 17 COMMITTED — Kristang Malacca]\n")

# ============================================================
# SWITCH — PCT-10: Macau Coffee
# ============================================================

session.switch_region("coffee", "Macau — Portuguese café culture")

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "macanese coffee galão",
    "region": "Macau — South China Sea",
    "name": "Macau Coffee Culture — Galão and the Macanese Café",
    "terroir_origin": (
        "Macau was a Portuguese colony from 1557 to 1999 — the last European colony in Asia, "
        "returned to China 38 years after Goa's annexation (1961). The Portuguese galão "
        "(a tall, latte-like coffee of espresso and foamed milk) arrived with Macau's cafés "
        "and became inseparable from the territory's Macanese identity. "
        "The Macau café culture occupies a unique position: it is the convergence of "
        "Portuguese café tradition (the espresso-milk drinking culture of Lisbon's pastelarias) "
        "with Cantonese tea culture (the cha chaan teng — Hong Kong and Macau's distinctive "
        "cafés that blend Western diner and Cantonese tea house). "
        "The result is a coffee culture unlike any other in Asia: "
        "the 'Macau-style milk coffee' (kāfē), the galão (espresso + foamed milk + honey), "
        "and the iconic pairing of the Macanese egg tart (pastel de nata adapted to Macanese "
        "custard with a flakier, more caramelised shell than the Lisbon original) with a "
        "small milky coffee. "
        "The Macanese egg tart itself travelled from Lisbon to Macau to Hong Kong — "
        "the Tai Cheong Bakery in Hong Kong credits the Macanese Portuguese confection "
        "as the origin of Hong Kong's beloved egg tart tradition."
    ),
    "production_technique": (
        "The Macau galão is prepared in the traditional Portuguese method: a single or double "
        "espresso (60–80mL) extended with hot foamed milk to fill a tall glass (240–300mL), "
        "creating a 1:3 or 1:4 coffee-to-milk ratio. The Portuguese original uses a tall "
        "cylindrical glass; the Macanese adaptation allows for a ceramic cup or glass. "
        "In the cha chaan teng tradition, coffee and black tea are combined in a hybrid drink "
        "'yuenyeung' (coffee + Hong Kong-style milk tea 1:1) — the PCT meets Cantonese "
        "tea culture literally in a cup. "
        "Macanese café milk coffee uses evaporated milk rather than fresh milk — "
        "a colonial-era adaptation when refrigeration was unavailable, which became "
        "the defining characteristic of Cantonese-Portuguese café coffee culture. "
        "Evaporated milk's caramel-sweetness and greater heat stability made it preferred "
        "over fresh milk for the cha chaan teng environment."
    ),
    "cross_tradition_parallels": [
        {"tradition": "coffee", "beverage": "Vietnamese Cà Phê Sữa (condensed milk coffee, French colonial)",
         "connection": "Both are colonial-era adaptations of European coffee culture to tropical Southeast/East Asian "
                       "climates without reliable dairy refrigeration. French condensed milk coffee (Vietnam) "
                       "and Portuguese evaporated milk coffee (Macau) share the sweet-milk-coffee character "
                       "produced by the same infrastructure limitation (no fresh milk) in the same colonial era. "
                       "The PCT and the French colonial trail converge at the same technological solution"},
        {"tradition": "tea", "beverage": "Hong Kong Milk Tea (cha chaan teng style)",
         "connection": "The Macanese café is the bridge between Portuguese galão culture and Hong Kong cha chaan teng. "
                       "Yuenyeung (coffee + Hong Kong milk tea) is the literal synthesis: the PT coffee tradition "
                       "fused with the British-colonial Cantonese milk tea tradition. Macau sat geographically "
                       "between both colonial spheres — Portuguese territory adjacent to British Hong Kong"}
    ],
    "sensory_profile": {
        "appearance": "Galão: caramel-brown in tall clear glass; layered milk and espresso visible if poured "
                      "correctly; frothy top. Macanese café coffee: lighter brown due to evaporated milk ratio",
        "nose": "Espresso: roasted, dark caramel, slight smoky. With evaporated milk: caramel sweetness "
                "dominates; the milk's lactose and slight caramelisation from evaporation adds distinct "
                "sweetness absent in fresh milk preparations",
        "palate": "The galão: smooth, balanced, coffee-forward with milk texture; less sweet than a latte "
                  "(no added sugar in the Portuguese original, though honey is optional). "
                  "With evaporated milk: noticeably sweeter, richer, more indulgent; "
                  "lower bitterness than espresso alone; comfort-beverage character",
        "conclusion": "The Macau coffee moment is the egg tart + galão — two of the PCT's most successful "
                      "food exports. The Macanese pastel de nata (adapted in Macau, then again in Hong Kong) "
                      "is now the most popular pastry in Asia by unit volume. The coffee-pastry pairing "
                      "is the PCT's most commercially successful cultural legacy."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Authentic Macanese Galão (named café)", "criteria": "Traditional preparation "
          "with quality espresso + Portuguese technique; historic Macau café; egg tart pairing integral",
          "markers": "Café Ou Mun (Macau); Lord Stow's Bakery (Coloane); Café Litoral; Macau-side named cafés"},
        {"tier": 3, "tier_name": "Portuguese-style Galão (outside Macau)", "criteria": "Espresso-to-milk "
          "ratio correct (1:3–1:4); tall glass service; quality espresso; egg tart or pastel de nata pairing",
          "markers": "Portuguese café or Macanese restaurant; named galão; correct format"},
        {"tier": 2, "tier_name": "Cha Chaan Teng Style", "criteria": "Evaporated milk coffee; Hong Kong/Macau "
          "café tradition; strong espresso or drip coffee base",
          "markers": "Cha chaan teng menu; evaporated milk listed; classic yuenyeung option"},
        {"tier": 1, "tier_name": "Generic Latte (Western format)", "criteria": "Espresso + steamed milk; "
          "no Portuguese-Macanese cultural context; standard Western café preparation",
          "markers": "Standard latte without Macanese or Portuguese cultural framing"}
    ],
    "service_intelligence": {
        "temperature": "65–70°C (hot galão); or iced in cha chaan teng style",
        "vessel": "Tall clear cylindrical glass (200–300mL) for galão; ceramic cup for Portuguese pastelaria style; "
                  "plastic takeaway cup for cha chaan teng",
        "technique": "Galão: single or double espresso (30–60mL) in tall glass, top with foamed whole milk "
                     "to 3:1 milk:coffee ratio. Optional: teaspoon honey. For Macanese cha chaan teng style: "
                     "use evaporated milk (30mL) diluted with hot water, add espresso or strong drip coffee. "
                     "Egg tart pairing: serve simultaneously — the pastry's caramelised egg custard "
                     "and the galão's sweetness are designed as a unit",
        "programme_position": "Coffee programme cultural story; brunch menu; Asian-fusion programme anchor; "
                              "Portuguese tasting menu dessert course pairing",
        "verbal_presentation": "The Macau galão — Portugal's café culture at the edge of China. "
                               "The same coffee tradition that fills Lisbon's pastelarias, translated "
                               "500 years ago to the South China Sea. With the egg tart: the PCT's most "
                               "successful export, now on every street corner in Hong Kong."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Lord Stow's Bakery (Macau egg tart) + any quality espresso",
        "producer_location": "Coloane Village, Macau SAR (Lord Stow's); Macau café district",
        "key_person": "Andrew Stow (Lord Stow's founder, 1989 — an Englishman who adapted the Macanese pastel de nata)",
        "production_volume": "Lord Stow's produces ~21,000 egg tarts daily (Wikipedia citation); global brand",
        "certifications": ["N/A — retail food category"],
        "bc_distributor": "Lord Stow's egg tarts: available at T&T Supermarket (Vancouver) and Asian grocery stores [NEEDS VERIFICATION]; "
                          "Galão: any quality espresso equipment + whole milk or evaporated milk",
        "us_distributor": "Lord Stow's: US retail through Asian specialty stores; Galão: preparation only",
        "uk_distributor": "N/A",
        "price_tier": "Preparation cost only (galão materials); egg tart ~MOP8/HKD8 in Macau",
        "availability_notes": "The galão requires no specific distributor — it is a preparation. "
                              "Evaporated milk (Carnation or Marigold brand) available at any Asian grocery. "
                              "For programme purposes: source good espresso, quality evaporated milk, "
                              "and fresh-baked pastel de nata."
    },
    "trail_connection": "PCT-10",
    "trail_note": "Macau's egg tart and galão represent the PCT's most globally diffused food legacy by unit volume. "
                  "Andrew Stow's 1989 Coloane bakery adapted the Lisbon pastel de nata into the Macanese egg tart, "
                  "which his Hong Kong business partner Kenneth Chan then brought to Hong Kong as 'tai tart' — "
                  "now found across Hong Kong, mainland China, and wherever there is a Cantonese diaspora. "
                  "The sequence: Lisbon bakery tradition → Portuguese colonial Macau → English baker adaptation "
                  "→ Cantonese diffusion → global spread. The PCT in one pastry.",
    "food_pairings": [
        {"technique_id": "", "dish": "Pastel de nata / Macanese egg tart",
         "pairing_type": "complement",
         "rationale": "The canonical PCT pairing: the tart's caramelised custard and the galão's "
                      "sweet espresso-milk were designed as a unit in every Macau café since the 1950s"},
        {"technique_id": "", "dish": "Minchi (Macanese ground meat with potatoes)",
         "pairing_type": "bridge",
         "rationale": "Minchi — the Macanese comfort dish of soy-spiced ground pork with crispy potato — "
                      "is the Macanese equivalent of a one-pot meal. Coffee served after minchi is the "
                      "Macau café's defining sequence"}
    ],
    "source": "Lord Stow's Bakery official history; Macau Government Tourism Office food documentation; "
              "Margaret Orr research on Macanese food culture; Wikipedia — Lord Stow's Bakery; "
              "South China Morning Post Macau food writing",
})

session.commit_batch()
print(f"\n[BATCH 18 COMMITTED — Macau Coffee Culture]\n")

# ============================================================
# SWITCH — PCT-4: Cape Verde Grogue
# ============================================================

session.switch_region("spirits", "Cape Verde — Grogue")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "grogue sugarcane spirit",
    "region": "Cape Verde — Santo Antão",
    "name": "Grogue — Cape Verde Sugarcane Spirit",
    "terroir_origin": (
        "Cape Verde is an archipelago of 10 volcanic islands in the Atlantic Ocean, 570km off the "
        "West African coast — uninhabited before Portuguese discovery around 1456. The islands "
        "became one of the first Portuguese colonial outposts and the primary transit hub for the "
        "Atlantic slave trade between Africa and the Americas. Sugarcane was introduced to Cape "
        "Verde by the Portuguese in the 15th century — the same sugarcane that became cachaça in "
        "Brazil. Cape Verde's sugarcane is cultivated in the lush valleys of Santo Antão island "
        "(the most fertile, with cloud-fed ribeiras — river valleys — rising to 1,979m at Pico Cruz). "
        "The volcanic basalt soils and altitude variation create distinct terroir for cane cultivation. "
        "Grogue is the national spirit of Cape Verde and a cultural cornerstone — consumed daily, "
        "used in ceremonies, and the base for ponche (grogue + lime + honey + spices), "
        "the archipelago's defining mixed drink."
    ),
    "production_technique": (
        "Cape Verdean grogue is produced identically to cachaça's traditional method: "
        "freshly pressed sugarcane juice fermented with wild yeasts for 24–72 hours, then distilled "
        "once in small copper pot stills (trapiche — the wooden or metal sugarcane press, often "
        "animal-powered). The artisanal trapiche is pulled by horses or donkeys on Santo Antão "
        "and Fogo islands — unchanged technology from the 16th century. "
        "Single distillation produces grogue at 38–55% ABV. Some producers age in local wood or "
        "repurposed barrels from other spirits. Unaged grogue dominates — it is typically consumed "
        "fresh from the still. Ponche is made by macerating lime, honey, and sometimes herbs or "
        "vanilla in fresh grogue: essentially an aguardente ponche identical to Portugal's "
        "own ponche traditions, showing the direct PCT cultural transmission. "
        "GI discussions for Cape Verde grogue are ongoing but no formal protection exists as of 2025."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Cachaça (Brazil)",
         "connection": "The most direct PCT parallel: both are single-distillation fresh sugarcane juice "
                       "spirits introduced to their respective territories by Portuguese colonists with "
                       "the same cane varieties and the same distillation technology. Grogue and cachaça "
                       "are separated by 3,000 miles of Atlantic Ocean and both express the same "
                       "colonial sugarcane transfer in different terroirs. Grogue is less refined (higher "
                       "congeners, more rustic) and less commercially developed than cachaça"},
        {"tradition": "spirits", "beverage": "Clairin (Haiti)",
         "connection": "Clairin — Haiti's artisanal sugarcane spirit — is the Caribbean parallel to grogue: "
                       "both are fresh-cane, single-pot-distilled spirits from Atlantic colonial contexts; "
                       "both are consumed primarily domestically; both have recently attracted international "
                       "specialty spirits attention. The PCT/WADT intersection: Haiti's cane came from the "
                       "French colonial system; Cape Verde's from Portuguese. Both spirits document "
                       "the same technology operating in the same Atlantic colonial economy"}
    ],
    "sensory_profile": {
        "appearance": "Crystal clear (unaged); pale golden (briefly wood-rested); deep amber (aged expressions, rare)",
        "nose": "Raw sugarcane, slight agricultural funk (higher congeners than premium cachaça), "
                "tropical fruit (Cape Verdean sea-island air), light ferment, earth. "
                "Less refined than commercial cachaça but more expressive — the volcanic terroir "
                "of Santo Antão valley is detectable in quality examples",
        "palate": "Full, warming, rustic — 40–55% ABV; fresh cane sweetness in finish; "
                  "higher congener presence than refined cachaça; genuine character rather than "
                  "commercial smoothness; ponche version is sweeter and more rounded",
        "conclusion": "Grogue is a spirits curiosity and a PCT cultural document. For a professional "
                      "programme, its primary value is narrative: the world's smallest commercially "
                      "available fresh-cane spirit from a culture that has been making it since "
                      "the 15th century, unchanged. Ponche Grogue is the more accessible "
                      "version for Western palates."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Aged Single Valley Grogue", "criteria": "Named ribeira (valley) on Santo Antão; "
          "brief wood ageing; documented single distillery; export quality",
          "markers": "Paul ribeira or Janela ribeira designation; artisanal producer name; limited international distribution"},
        {"tier": 3, "tier_name": "Artisanal Unaged Grogue", "criteria": "Traditional trapiche press; "
          "small producer; fresh cane juice; Santo Antão or Fogo origin",
          "markers": "Named producer; island of origin; traditional bottle labelling"},
        {"tier": 2, "tier_name": "Ponche Grogue (commercial)", "criteria": "Grogue macerated with lime, "
          "honey, and spices; bottled ponche; the accessible Cape Verde export format",
          "markers": "Ponche Grogue label; commercial Cape Verdean producer; wider distribution than raw grogue"},
        {"tier": 1, "tier_name": "Industrial Grogue", "criteria": "Column still possible; molasses addition "
          "possible; loss of fresh-cane character; lower quality",
          "markers": "Cheapest available; no artisanal attribution"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for neat; chilled for ponche",
        "vessel": "Small glass or shot glass; rocks glass for ponche on ice",
        "technique": "Cape Verde Ponche: 50mL grogue + juice of 1 lime + 20mL honey + cinnamon stick; "
                     "stir with ice, serve chilled. Or: macerate for 1 week (honey + grogue + lime zest + "
                     "vanilla pod) for a bottled ponche. Neat grogue: small pour, acknowledge the "
                     "rough edges as authenticity markers",
        "programme_position": "Specialty spirits education; Atlantic trail cocktail; "
                              "West African/Cape Verdean cultural events",
        "verbal_presentation": "Grogue from Santo Antão — Cape Verde. The Portuguese brought sugarcane "
                               "here in the 15th century; the islanders have been distilling it in "
                               "animal-powered presses ever since. The same cane, the same still, "
                               "500 years on. Rough, honest, Atlantic."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Fogo Island Grogue producers (artisanal) and Destilaria Tito (Santo Antão)",
        "producer_location": "Santo Antão island and Fogo island, Republic of Cape Verde",
        "key_person": "[NEEDS VERIFICATION — no single nationally prominent commercial producer]",
        "production_volume": "Very limited export; primarily domestic consumption (~3 million islanders + diaspora)",
        "certifications": ["No formal GI as of 2025; GI discussions ongoing with INIDA (Cape Verde agricultural institute)"],
        "bc_distributor": "[NEEDS VERIFICATION — no confirmed BC commercial availability]",
        "us_distributor": "[NEEDS VERIFICATION — very limited US commercial availability; "
                          "Cape Verdean community stores in Providence RI, Boston MA, New Bedford MA may stock]",
        "uk_distributor": "[NEEDS VERIFICATION — some UK availability through Cape Verdean diaspora "
                          "community stores and online spirits specialists]",
        "price_tier": "Market (€8–20 in Cape Verde; £25–40 if available in UK specialist retail)",
        "availability_notes": "Grogue is essentially unavailable through normal BC or US commercial channels. "
                              "For programme use: source through direct Cape Verdean diaspora networks "
                              "or specialty Atlantic spirits importers. The cultural narrative justifies "
                              "the procurement effort on a PCT-focused programme. Ponche Grogue bottles "
                              "are more likely to be internationally available than raw grogue."
    },
    "trail_connection": "PCT-4",
    "trail_note": "Cape Verde is the PCT's Atlantic hub — the geographic centre of Portuguese maritime expansion. "
                  "Ships from Lisbon stopped here on the way to Brazil (PCT-13), West Africa (WADT), India (PCT-8), "
                  "and Macau (PCT-10). Grogue carries every branch of the Portuguese colonial trail in its cane: "
                  "the same sugarcane species moved from Madeira (PCT-2) to Cape Verde to Brazil and back through "
                  "Portuguese ship routes. Grogue is the Atlantic colonial economy distilled to 45% ABV.",
    "food_pairings": [
        {"technique_id": "", "dish": "Cachupa (Cape Verde national stew — maize, beans, smoked pork, fish)",
         "pairing_type": "complement",
         "rationale": "The national dish with the national spirit. Cachupa's smoked meats and corn base "
                      "are bridged by grogue's raw cane sweetness — the starch and spirit are made for each other"},
        {"technique_id": "", "dish": "Grilled wahoo (atum) with sweet potato",
         "pairing_type": "bridge",
         "rationale": "Cape Verde's Atlantic fishing tradition: wahoo (skipjack tuna family) grilled over "
                      "charcoal; ponche grogue with lime bridges the fish's firm flesh and charcoal char"}
    ],
    "source": "Slow Food Cape Verde documentation; INIDA Cape Verde agricultural institute; "
              "Cape Verdean gastronomy research by João Branco; "
              "Destilaria Tito production documentation",
})

session.commit_batch()
print(f"\n[BATCH 19 COMMITTED — Cape Verde Grogue]\n")

# ============================================================
# SWITCH — PCT×WADT: Caribbean Rum
# ============================================================

session.switch_region("spirits", "Caribbean — Rum (PCT×WADT Intersection)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "pot still jamaican rum",
    "region": "Caribbean — Jamaica",
    "name": "Jamaican Rum — Pot Still, High-Ester (Appleton, Worthy Park, Hampden)",
    "terroir_origin": (
        "Rum is the spirit category that most directly embodies the PCT×WADT intersection — "
        "the convergence of Portuguese sugarcane cultivation (PCT) and West/Central African enslaved "
        "labour (WADT) in the Atlantic colonial economy. Sugarcane (Saccharum officinarum) originated "
        "in Southeast Asia, was cultivated in Portugal's Atlantic islands (Madeira, São Tomé — PCT-2 "
        "and PCT-5), transported to the Caribbean by Spanish and Portuguese colonists, and then "
        "produced into rum on Barbados (c. 1620s) using sugarcane that was almost certainly "
        "descendant of the Portuguese Atlantic variety. "
        "Jamaica's rum tradition: the island was colonised by Spain (1494), captured by England (1655), "
        "and developed by British planters who systematically created the pot-still, high-ester "
        "Jamaican style. The Nassau Valley of St. Elizabeth Parish, and the parishes of Westmoreland "
        "and St. James contain the major distilleries. Jamaica's unique climate (wet limestone soil, "
        "tropical humidity) creates the Dunder fermentation tradition: "
        "dunder (the residue from the previous distillation) is added to fresh fermentation vats "
        "as a bacterial inoculant, creating the high-ester 'Jamaican funk' — the defining "
        "aromatic characteristic of high-ester pot-still rum."
    ),
    "production_technique": (
        "Jamaican pot-still rum production: freshly harvested cane is crushed; juice fermented "
        "with wild yeasts and bacterial cultures (including dunder addition) for 2–5 weeks for "
        "high-ester marks (vs. 24–48 hours for light industrial rum). "
        "The long, warm fermentation produces butyric esters, ethyl acetate, and the signature "
        "compound: ethyl butyrate (pineapple character) at concentrations 10–50× higher than "
        "other rum styles. Pot still distillation (double distillation in traditional copper "
        "pot stills at Hampden, Worthy Park) produces a raw spirit of extraordinary complexity "
        "at 65–86% ABV. Jamaica's Rum Producers Association defines 'marks' (flavour profiles): "
        "DOK, HLCF (wild ferment, maximum ester), EOE, etc. — a classification system unique "
        "to Jamaica. Ageing typically in ex-bourbon American white oak barrels. "
        "Appleton Estate (Nassau Valley) ages in ex-bourbon for 8, 12, 15, 21 years; "
        "Hampden Estate uses a still-active 18th-century wooden pot still for some marks."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Cachaça (Brazil — PCT-13)",
         "connection": "The most direct parallel: both are fresh-cane spirits from Portuguese/colonial "
                       "Atlantic sugarcane cultivation. Cachaça uses fresh juice (not molasses) and single "
                       "distillation; Jamaican rum uses blackstrap molasses (the residue after sugar "
                       "crystallisation) and double pot distillation. Both trace their agricultural "
                       "origin to the same Portuguese Atlantic island sugarcane. The WADT dimension is "
                       "more explicit in Jamaican rum: the entire Jamaican sugar plantation system was "
                       "built on enslaved African labour"},
        {"tradition": "spirits", "beverage": "Rhum Agricole Martinique (PCT×French colonial)",
         "connection": "Rhum Agricole is the French colonial equivalent: fresh sugarcane juice (not molasses), "
                       "AOC-protected, from Martinique. Martinique's cane is a different colonial tradition "
                       "(French, not Portuguese/British) but from the same Atlantic sugarcane genealogy. "
                       "The comparison demonstrates how the same base material (Atlantic sugarcane) produces "
                       "entirely different spirits under different colonial distillation philosophies"}
    ],
    "sensory_profile": {
        "appearance": "Unaged: clear. Lightly aged: pale gold. Aged 12yr+: deep amber to mahogany. "
                      "High-ester unaged: the funkiest-nosed clear spirit in any category",
        "nose": "High-ester Jamaican (Hampden DOK/HLCF, Worthy Park WPL): overripe banana, "
                "ripe pineapple, mango, petrol/acetone (from ethyl butyrate at high concentrations), "
                "tobacco, leather, tropical fruit punch. An acquired and extraordinary nose. "
                "Appleton 12yr: dried fruit, dark chocolate, toffee, banana bread, warm spice — "
                "the ester complexity tamed and integrated by oak ageing",
        "palate": "High-ester unaged: intensely fruity, challenging, pungent — bartender ingredient. "
                  "Appleton 12yr: rich, full-bodied, spiced, long finish with tropical fruit and wood. "
                  "Appleton 21yr: extraordinary complexity — dried mango, leather, tobacco, spice, "
                  "dark honey; comparable to aged Cognac in sipping quality",
        "conclusion": "Jamaican pot-still rum spans the entire quality range from cocktail ingredient "
                      "(unaged high-ester) to prestige sipping spirit (Appleton 21yr, Hampden Rum Fire "
                      "aged). Essential for any complete spirits programme: the Atlantic rum narrative "
                      "is the PCT×WADT story told in a glass."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "21yr+ Aged Single Estate / Cask Strength", "criteria": "Single estate, "
          "named still/mark, 21+ years ex-bourbon cask; Appleton 21yr or Hampden 8yr HLCF as benchmarks",
          "markers": "Appleton 21yr 'Nassau Valley'; Hampden aged expressions; Joy Spence (winemaker equivalent) "
                     "designation; £80–200+ per bottle"},
        {"tier": 3, "tier_name": "12–15yr Aged Blended Estate", "criteria": "Single estate, 12–15yr ageing, "
          "consistent quality; the premium cocktail/sipping segment",
          "markers": "Appleton 12yr; Worthy Park 'Rum Bar' aged; £35–60 per bottle"},
        {"tier": 2, "tier_name": "White/Gold Aged Blend", "criteria": "3–7yr ageing; estate-sourced; "
          "cocktail-grade with character; Appleton Signature as benchmark",
          "markers": "Appleton Signature; Coruba; £20–35 per bottle"},
        {"tier": 1, "tier_name": "Column-Still Light Rum", "criteria": "Commercial production; column still; "
          "light flavour for volume cocktail use; no estate attribution",
          "markers": "Wray & Nephew overproof (exception — unaged pot still Jamaican white at 63% ABV); "
                     "generic blended white rum"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for sipping; ice for cocktails",
        "vessel": "Tulip glass or Glencairn for neat; rocks glass with single ice cube for premium sipping; "
                  "Collins glass for daiquiri or rum punch",
        "technique": "Classic Daiquiri: 60mL Appleton 8yr, 30mL fresh lime, 15mL simple syrup, "
                     "shaken over ice. High-ester in cocktails: 10–15mL Hampden HLCF in a Zombie or "
                     "blended with lighter rum — the ester intensity works as a modifier. "
                     "Appleton 21yr: neat with a splash of water to open",
        "programme_position": "Cocktail bar foundation (Caribbean classics); premium spirits section for "
                              "aged expressions; PCT×WADT narrative spirits flight",
        "verbal_presentation": "Appleton Estate, Nassau Valley — Jamaican rum since 1749. The sugarcane "
                               "came to the Caribbean from Portugal's Atlantic islands; the pot still came "
                               "from the same Portuguese-English colonial trade. Twenty-one years in "
                               "ex-bourbon oak. The PCT and the Atlantic slave trade in a single glass — "
                               "the history you should know when you drink it."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Appleton Estate (Nassau Valley, St. Elizabeth, Jamaica)",
        "producer_location": "Nassau Valley, St. Elizabeth Parish, Jamaica",
        "key_person": "Joy Spence (Master Blender, first female Master Blender in the spirits industry); "
                      "Campari Group (owner)",
        "production_volume": "Appleton: ~500,000 cases annually; Campari Group distribution worldwide",
        "certifications": ["Jamaica Rum Producers Association member", "GI — Rum of Jamaica (2016)"],
        "bc_distributor": "Southern Glazer's Wine & Spirits of Canada (national distribution agreement, "
                          "effective April 1, 2025 — confirmed via BusinessWire); "
                          "Appleton widely available at BC Liquor",
        "us_distributor": "Campari America (Appleton USA — confirmed national distribution); "
                          "widely available Total Wine, BevMo, national chains",
        "uk_distributor": "Campari UK; widely available at Waitrose, Sainsbury's, specialist off-licences",
        "price_tier": "Market (Signature ~$28 BC; 12yr ~$45 BC; 21yr ~$110 BC)",
        "availability_notes": "Appleton Estate: among the most widely available premium rums in BC and US. "
                              "BC Liquor stocks multiple expressions. Hampden Estate and Worthy Park: "
                              "more limited — specialist spirits merchants; Velier Hampden through "
                              "European importers (US: check Skurnik or Domaine Select). "
                              "Rum Bar (Worthy Park): BC limited but available."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Appleton Estate was established 1749 — 94 years after Britain captured Jamaica from Spain. "
                  "The Nassau Valley sugarcane is descended from the Atlantic colonial cane that Portugal first "
                  "commercialised on Madeira (PCT-2) in the 15th century. The rum's history IS the Atlantic "
                  "colonial economy: Portuguese cane, British colonial infrastructure, West African enslaved labour "
                  "(WADT), American oak ageing barrels. Joy Spence, the first female Master Blender in the "
                  "spirits industry (appointed 1997), represents the post-colonial redemption of the tradition "
                  "she inherited.",
    "food_pairings": [
        {"technique_id": "", "dish": "Jerk chicken (allspice-scotch bonnet dry rub, coal fire)",
         "pairing_type": "complement",
         "rationale": "The canonical Jamaican pairing: the char and allspice of jerk chicken and the "
                      "tropical fruit-spice of Appleton rum share the same warm, smoky register"},
        {"technique_id": "", "dish": "Dark chocolate rum cake (Jamaican Christmas cake)",
         "pairing_type": "complement",
         "rationale": "Jamaican black cake — dried fruit soaked in rum for weeks, then baked — is made "
                      "WITH Appleton rum, so the pairing is literally the same ingredient twice"}
    ],
    "source": "Jamaica Rum Producers Association; Appleton Estate official documentation; "
              "Campari Group annual report 2024; GI — Rum of Jamaica 2016 registration; "
              "Joy Spence biography and master blender documentation",
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "rhum agricole martinique",
    "region": "Caribbean — Martinique (AOC Rhum Agricole)",
    "name": "Rhum Agricole AOC Martinique — Clément, J.M., Neisson",
    "terroir_origin": (
        "Martinique's Rhum Agricole is the most terroir-specific rum in the world — the only rum "
        "protected by a French AOC (Appellation d'Origine Contrôlée, granted 1996). "
        "While Martinique was a French colony (not Portuguese), the sugarcane itself traces directly "
        "to the Portuguese Atlantic island cultivation system. The PCT node: the same sugarcane "
        "brought to Madeira (1420s) and Cape Verde (1450s) by Portuguese colonists spread through "
        "the Atlantic to the French and British Caribbean. Martinique's northern slopes (Mount Pelée "
        "volcano, 1,397m) produce the most complex cane — volcanic andesite soils, Atlantic trade "
        "winds, moderate altitude. The southern plains produce higher volume, lighter character. "
        "AOC Martinique mandates specific cane varieties (limited to approved list), minimum "
        "sugarcane freshness (cane must be pressed within 24 hours of harvest), column still "
        "parameters (minimum 65° GL), and ageing requirements for VSOP and XO designations."
    ),
    "production_technique": (
        "Rhum Agricole production: freshly cut sugarcane is pressed immediately; the resulting "
        "vesou (sugarcane juice) is fermented with selected or wild yeasts for 24–36 hours — "
        "significantly shorter than Jamaican pot-still rum (2–5 weeks) and producing a cleaner, "
        "more precise fermentation with fewer congeners. Column still distillation at 65–75% ABV "
        "preserves the cane terroir while removing harsh compounds. The crucial distinction from "
        "industrial rum: no molasses, no column-still stripping to neutral, no flavour additives. "
        "Unaged Rhum Agricole Blanc: the purest expression, bottled at 50–60% ABV. "
        "Rhum Vieux (aged): minimum 3 years in 650L or smaller oak barrels; AOC requires specific "
        "parameters. Clément VSOP: 4yr minimum; J.M. XO: 6–8yr; Neisson L'Esprit: cask strength. "
        "The tropical ageing environment (30°C average, high humidity) produces ~8–10% evaporation "
        "annually — twice European cellar rates — accelerating complexity development."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Condrieu (Northern Rhône, France — Viognier)",
         "connection": "Both are AOC-protected, single-variety expressions from volcanic terroir "
                       "(Condrieu: granite; Martinique: andesite) where the variety expresses terroir "
                       "without technological intervention. Both are defined by fragrant, tropical-floral "
                       "character that no other terroir replicates. Both reward single-origin obsession "
                       "over blended-for-consistency production philosophy"},
        {"tradition": "spirits", "beverage": "Cachaça Artisanal — Minas Gerais (PCT-13)",
         "connection": "The direct Atlantic comparison: both are fresh sugarcane juice, single-terroir spirits "
                       "from the same Portuguese Atlantic cane genealogy expressed in different colonial "
                       "contexts. Cachaça is Brazilian/Portuguese-colonial; Rhum Agricole is French-colonial. "
                       "Fresh juice + terroir + limited intervention = the philosophy shared across both"}
    ],
    "sensory_profile": {
        "appearance": "Blanc (unaged): crystal clear. Vieux (aged): pale gold to deep amber depending on time",
        "nose": "Blanc: intense fresh sugarcane, cut grass, tropical fruit (green banana, pineapple, papaya), "
                "volcanic mineral, white pepper — one of the most distinctive noses in spirits. "
                "Vieux VSOP: banana foster, vanilla, dried tropical fruit, light oak, cane sweetness. "
                "XO: complex vanilla-toffee-dried fruit-aged character approaching Armagnac territory",
        "palate": "Blanc: bold, herbaceous, sugarcane intensity, clean finish — the terroir in full cry. "
                  "VSOP: rounded, tropical fruit preserved in vanilla-oak framework, long sweet finish. "
                  "XO: full, complex, incredibly long — the tropical ageing cycle in 40 seconds of finish",
        "conclusion": "Martinique Blanc is the world's best argument for terroir in spirits — a single-origin "
                      "beverage as distinctive as a Grand Cru Burgundy. Every serious spirits programme "
                      "should include a Rhum Agricole expression as the premium rum reference point."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "XO / Hors d'Âge (6yr+) Single Distillery", "criteria": "Minimum 6yr tropical "
          "ageing; single distillery; cask-specific; AOC-certified",
          "markers": "Clément XO; J.M. XO; Neisson Parcellaire; Rhum J.M. Cuvée 1845; £80–200+"},
        {"tier": 3, "tier_name": "VSOP (4yr+)", "criteria": "Minimum 4yr tropical ageing; AOC-certified; "
          "consistent house style",
          "markers": "Clément VSOP; J.M. VSOP; Trois Rivières VSOP; £40–65"},
        {"tier": 2, "tier_name": "Élevé Sous Bois / Rhum Vieux (3yr)", "criteria": "Minimum 3yr; AOC; "
          "entry into aged Rhum Agricole",
          "markers": "La Favorite Cœur de Canne; Trois Rivières; £30–45"},
        {"tier": 1, "tier_name": "Rhum Blanc (Unaged)", "criteria": "AOC-certified; minimum parameters "
          "for fresh cane, column still; 50–60% ABV",
          "markers": "Clément Blanc; J.M. Blanc; Neisson Blanc; £25–35; the cocktail and terroir baseline"}
    ],
    "service_intelligence": {
        "temperature": "Blanc: room temperature or lightly chilled; Vieux: room temperature for sipping",
        "vessel": "Blanc: rocks glass or coupe for cocktails; Vieux VSOP/XO: tulip glass or Glencairn",
        "technique": "Ti' Punch (Martinique's national cocktail): 50mL Rhum Agricole Blanc + 10mL cane "
                     "syrup + squeeze of lime (the whole lime squeezed, not juiced) — no ice. "
                     "Stir in the glass. The ratio is personal; in Martinique, the ingredients are "
                     "served separately (chacun prépare sa propre mort — 'each person prepares their "
                     "own death'). Agricole Daiquiri: 60mL Blanc, 22mL lime, 15mL agricane syrup. "
                     "XO neat: room temperature, 45mL, single large ice cube added after 2 minutes",
        "programme_position": "Premium cocktail programme foundation; prestige spirits section for XO; "
                              "terroir education flight; PCT×WADT narrative",
        "verbal_presentation": "Rhum Agricole from Martinique — the only rum with a French AOC. "
                               "The sugarcane came from Portugal's Atlantic islands; the French applied "
                               "their appellation system to it. Fresh-pressed cane juice, distilled "
                               "without molasses, aged in the Caribbean heat. The closest rum comes "
                               "to speaking of a specific place."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Clément (Martinique) and Rhum J.M. (Macouba, northern Martinique)",
        "producer_location": "Clément: Le François, Martinique; J.M.: Macouba, Martinique (Mt. Pelée foothills)",
        "key_person": "Charles Clément (founder); J.M.'s terroir position near Mt. Pelée is the brand identity",
        "production_volume": "Clément: major commercial volume; J.M.: boutique volcanic terroir focus",
        "certifications": ["AOC Martinique (1996)", "French Ministry of Agriculture certification"],
        "bc_distributor": "Clément: available at BCLDB (confirmed); J.M.: limited BC — specialty spirits merchants",
        "us_distributor": "Clément: Spiribam USA (owner) + Skurnik (regional distributor) — confirmed; "
                          "J.M.: Spiribam USA (owner) + Skurnik (regional distributor) — confirmed",
        "uk_distributor": "Clément: Berry Bros. & Rudd; Masters of Malt; Waitrose",
        "price_tier": "Blanc: BC ~$38–45; VSOP: ~$65–80; XO: ~$120–180",
        "availability_notes": "Clément Blanc and VSOP: available at BC Liquor stores and private wine/spirits shops. "
                              "J.M. and Neisson: limited BC distribution — specialty spirits merchants. "
                              "US: Clément at Total Wine, BevMo nationally. J.M. through specialty accounts."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Martinique's rhum agricole tradition uses sugarcane descended from the same Portuguese "
                  "Atlantic island cultivation that defined the PCT. The French AOC framework for rum "
                  "is the most sophisticated quality protection applied to any sugar spirit globally — "
                  "the French brought their wine-region appellation philosophy to the same raw material "
                  "the Portuguese commercialised 500 years earlier. PCT and French colonial trails "
                  "share the same sugarcane botanical origin.",
    "food_pairings": [
        {"technique_id": "", "dish": "Accras de morue (salt cod fritters, Martinique/Guadeloupe)",
         "pairing_type": "complement",
         "rationale": "Salt cod fritters are the bridge between Martinique's Creole food culture and "
                      "the Portuguese bacalhau tradition (PCT). Ti' Punch alongside accras is the "
                      "canonical Martinique aperitif pairing"},
        {"technique_id": "", "dish": "Poulet boucané (smoked Creole chicken)", "pairing_type": "bridge",
         "rationale": "The agricole rhum's herbaceous-tropical character bridges with the allspice-smoked "
                      "chicken — the same terroir in food and spirit form"}
    ],
    "source": "AOC Martinique official documentation (INAO, 1996); Clément official history; "
              "J.M. Rhum production documentation; Dave Broom 'Rum' (reference text); "
              "Luca Gargano Velier rhum agricole research",
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "demerara rum guyana",
    "region": "Caribbean — Guyana (Demerara)",
    "name": "El Dorado — Demerara Rum (Guyana)",
    "terroir_origin": (
        "The Demerara River delta of Guyana (formerly British Guiana) is one of the Atlantic world's "
        "most historically significant rum terroirs. The name 'Demerara' now designates a style of rum "
        "rather than just a place — deep, rich, ester-forward, molasses-based dark rum. "
        "The Demerara Distillers Ltd. (DDL) facility at Enmore, on the Demerara River, is the "
        "world's only distillery using every historic still type in continuous operation: "
        "a wooden double pot still from 1732 (built on the former Enmore plantation), a metal "
        "two-column Coffey still, a single wooden Coffey still, a four-column Savalle still, "
        "and multiple pot stills. The colonial history is inseparable: the Demerara region was "
        "settled by the Dutch, then contested between British and French, before becoming British "
        "Guiana in 1814. The plantation system used West African enslaved labour (WADT) to produce "
        "rum for the British market. DDL today is 100% Guyanese-owned — post-colonial redemption "
        "of the same plantation infrastructure."
    ),
    "production_technique": (
        "Demerara rum uses blackstrap molasses from sugarcane grown in the mineral-rich alluvial "
        "soils of the Demerara and Berbice river deltas. The wooden pot stills at Enmore are "
        "among the world's most historically significant production vessels — their wooden walls "
        "harbour 290-year-old yeast and bacterial populations that cannot be replicated elsewhere. "
        "Fermentation: 24–72 hours depending on still type and target mark. Distillation: the "
        "different still types produce different marks — the wooden pot still produces the heaviest, "
        "funkiest 'Versailles' character; the Coffey still produces lighter, more commercial grades. "
        "DDL blends marks from all stills into El Dorado expressions. Ageing: in ex-bourbon "
        "casks in Guyana's hot tropical climate (similar evaporation to Martinique: 8–10% annually). "
        "El Dorado 15yr: blend aged minimum 15 years, multiple marks; El Dorado 21yr: "
        "the prestige expression."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Armagnac from pre-war stocks (Gascony, France)",
         "connection": "Both are deeply flavoured, terroir-specific, historically significant spirits "
                       "aged in the same barrels for exceptional periods. Both use distinctive "
                       "still types that are no longer manufactured anywhere else. Demerara's "
                       "wooden pot stills and Armagnac's alambic armagnacais are the spirits world's "
                       "most historically irreplaceable production vessels"},
        {"tradition": "spirits", "beverage": "Jamaican High-Ester Pot Still Rum (PCT×WADT)",
         "connection": "The direct Jamaican comparison: both are Caribbean rum produced with extended "
                       "fermentation and pot/hybrid stills for maximum flavour complexity. "
                       "Jamaican rum is fruit-ester forward (butyric); Demerara is more complex "
                       "blended-style from multiple still types. Both are WADT-intersected: "
                       "both plantation systems used enslaved West/Central African labour"}
    ],
    "sensory_profile": {
        "appearance": "Deep mahogany to dark amber; viscous; Demerara sugars give warmth of hue "
                      "even in lighter expressions",
        "nose": "El Dorado 15yr: dried plum, raisin, dark toffee, molasses, vanilla, cinnamon, "
                "tobacco, leather. Wooden pot still character: distinctive earthy-woody depth "
                "impossible in stainless-fermented column rum. "
                "El Dorado 21yr: extraordinary — coffee, leather, dried mango, dark chocolate, "
                "aged oak, burnt sugar, exotic wood",
        "palate": "Full body (fullest of any rum category); high natural sugar (Demerara's residual "
                  "molasses sweetness persists through ageing); long, complex, warm finish. "
                  "El Dorado 15yr: 43% ABV; accessible; one of the most complex rums at its price. "
                  "El Dorado 21yr: 43% ABV; the prestige benchmark of the Demerara style",
        "conclusion": "El Dorado 15yr is the rum world's greatest value expression — the depth-to-price "
                      "ratio is unmatched. Essential on any serious spirits programme and the most "
                      "compelling argument that rum deserves the same sipping respect as aged "
                      "Scotch or Cognac."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "El Dorado 21yr / Rare Cask Series", "criteria": "21+ years tropical ageing; "
          "DDL rare cask or vintage release; multiple still marks blended",
          "markers": "El Dorado 21yr; Velier Demerara releases (PM, Enmore, Versailles marks); £80–200+"},
        {"tier": 3, "tier_name": "El Dorado 15yr", "criteria": "15+ years; multiple marks; "
          "consistent premium quality; the value benchmark",
          "markers": "El Dorado 15yr; Rum Nation Demerara 15yr; £45–60"},
        {"tier": 2, "tier_name": "El Dorado 12yr", "criteria": "12 years; accessible premium; "
          "correct Demerara character",
          "markers": "El Dorado 12yr; Pusser's British Navy Rum; £30–40"},
        {"tier": 1, "tier_name": "El Dorado 5yr / Commercial Blends", "criteria": "Younger age; "
          "correct molasses-caramel character; cocktail grade",
          "markers": "El Dorado 5yr; commercial dark rum blends at accessible pricing"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for sipping; over ice for cocktails",
        "vessel": "Glencairn or tulip glass for sipping; rocks glass for cocktails",
        "technique": "El Dorado 15yr neat: room temperature, 45mL, allow 5 minutes to open. "
                     "El Dorado in cocktails: excellent in Dark & Stormy (60mL + ginger beer + lime), "
                     "Old Fashioned (50mL + 2 dashes Angostura + sugar cube). "
                     "Rum punch: El Dorado 12yr base, lime, sugar, Angostura bitters, nutmeg",
        "programme_position": "Premium spirits sipping section; rum cocktail foundation; "
                              "WADT narrative spirit for Atlantic history programme",
        "verbal_presentation": "El Dorado 15 Years — Demerara, Guyana. The world's only distillery "
                               "running wooden pot stills from 1732. Fifteen years in Caribbean heat. "
                               "The rum that put Guyana back on the spirits world map."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Demerara Distillers Ltd. (DDL) — El Dorado",
        "producer_location": "Enmore, East Coast Demerara, Guyana",
        "key_person": "Yesu Persaud (founder); DDL is 100% Guyanese-owned",
        "production_volume": "Large commercial scale; El Dorado distributed in 50+ countries",
        "certifications": ["Demerara Rum GI (Guyana)"],
        "bc_distributor": "BCLDB direct import; El Dorado available at BC Liquor stores (confirmed)",
        "us_distributor": "Skurnik Wines & Spirits + DDL USA (own US subsidiary) — both confirmed",
        "uk_distributor": "El Dorado widely available: Waitrose, Sainsbury's, specialist rum merchants; "
                          "Speciality Drinks London (Velier Demerara marks)",
        "price_tier": "Market to Reserve (El Dorado 15yr BC ~$50–60; 21yr ~$110–130)",
        "availability_notes": "El Dorado 12yr and 15yr: BC Liquor stores. El Dorado 21yr: specialist spirits "
                              "merchants or BCLDB special order. US: widely available at Total Wine, BevMo, "
                              "and premium spirits retailers nationally."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Demerara rum's history is inseparable from the Atlantic slave trade — the WADT. "
                  "The Enmore plantation's wooden pot still was built by enslaved Guyanese workers in 1732 "
                  "and is still running today, now under Guyanese ownership (DDL). The PCT connection: "
                  "the sugarcane processed at Enmore is descended from the Portuguese Atlantic island "
                  "varieties that Portugal commercialised 300 years before Enmore's first distillate. "
                  "DDL's 100% Guyanese ownership is the post-colonial reclamation of a 290-year-old "
                  "colonial infrastructure asset.",
    "food_pairings": [
        {"technique_id": "", "dish": "Pepperpot (Guyanese Christmas stew — casareep, beef/pork, cassava pepper)",
         "pairing_type": "complement",
         "rationale": "Guyana's national Christmas dish paired with its national spirit. "
                      "Pepperpot's casareep (concentrated cassava juice) bitterness and the "
                      "rum's molasses-caramel sweetness create a push-pull tension that is "
                      "the defining Guyanese festive pairing"},
        {"technique_id": "", "dish": "Black fruitcake (Caribbean Christmas cake, rum-soaked)",
         "pairing_type": "complement",
         "rationale": "Rum-soaked dried fruit baked into black fruitcake and then served with the "
                      "same rum — the most literal example of pairing in any food tradition"}
    ],
    "source": "Demerara Distillers Ltd. official documentation; El Dorado production history; "
              "Dave Broom 'Rum'; Luca Gargano Velier documentation on Demerara marks; "
              "GI Demerara Rum registration (Guyana)",
})

session.commit_batch()
print(f"\n[BATCH 20 COMMITTED — Jamaican + Martinique + Demerara Rum]\n")

# ============================================================
# SWITCH — PCT-14×PMT: Hawaii Kona Coffee
# ============================================================

session.switch_region("coffee", "Hawaii — Kona and Ka'u")

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "kona arabica specialty",
    "region": "USA — Hawaii (Kona, Ka'u, Maui)",
    "name": "Kona Coffee — The Hawaiian Arabica",
    "terroir_origin": (
        "Kona coffee is grown on the western slopes of Mauna Loa and Hualalai volcanoes on the Big "
        "Island of Hawaii, in the North and South Kona districts. The 'Kona Coffee Belt' runs at "
        "180–900m altitude, with a unique microclimate: sunny mornings, cloud cover and afternoon "
        "showers from the mountains, and volcanic basalt soils. "
        "The PCT×PMT (Pacific Migration Trail) intersection: coffee arrived in Hawaii in 1825 when "
        "Chief Boki brought plants from Brazil to Oahu — a Brazilian-origin arabica (descended from "
        "the same Portuguese-smuggled 1727 seedlings via Palheta). Hawaiian-born farmers and later "
        "Portuguese immigrant plantation workers (predominantly from the Azores and Madeira — "
        "the PCT islands) developed the Kona coffee industry in the late 19th century alongside "
        "Japanese, Filipino, and Polynesian communities. The volcanic geology of Hawaii (Pacific "
        "hotspot volcano) on porous basalt with excellent drainage and high mineral content creates "
        "the richness and low acidity that define Kona's flavour profile. "
        "Kona has a Geographical Indication (GI) protected in the US under the Kona Coffee Council "
        "— only coffee grown in the Kona District of Hawaii County can be labelled 'Kona Coffee.'"
    ),
    "production_technique": (
        "Kona coffee is hand-harvested — the steep volcanic slopes preclude mechanical harvesting. "
        "Selective hand-picking ensures only ripe cherries are collected. "
        "The Typica variety dominates Kona production — one of the oldest arabica varieties in "
        "continuous cultivation globally, descended directly from the Yemen-to-Amsterdam-to-"
        "Caribbean-to-Brazil arabica lineage brought to Hawaii via Chief Boki's 1825 procurement. "
        "Wet/washed processing is predominant: pulping on the same day as harvest, fermentation "
        "12–24 hours, sun-drying on raised beds for 5–10 days. "
        "The small farm structure of Kona (most farms are 1–5 acres, operated by individual families) "
        "creates enormous variation in quality. 'Kona blends' (10% Kona + 90% other origin) are a "
        "major issue in the market — legally sold as 'Kona blend' but misleading consumers. "
        "For true single-farm Kona: Greenwell Farms (1850, oldest continuously operating Kona farm), "
        "Kona Joe (trellis-grown; first trellis coffee farm in North America), and Ka'u Coffee Mill "
        "(the newer southern region, gaining Cup of Excellence scores)."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Screaming Eagle / Harlan Estate (Napa Valley Cabernet)",
         "connection": "Both are the world's most expensive, most faked, and most geographically specific "
                       "single-origin products from volcanic American terroir. Both are surrounded by "
                       "lower-quality blends using their names (Kona blend; Napa vs. California label). "
                       "Both demonstrate that American volcanic terroir can compete with the world's most "
                       "prestigious origins when production is at the highest level"},
        {"tradition": "coffee", "beverage": "Jamaica Blue Mountain (Blue Mountains, Jamaica)",
         "connection": "The closest parallel in brand positioning: both are island arabicas with GI protection, "
                       "premium pricing, and significant fraud/blending issues. Blue Mountain coffee was "
                       "brought from Martinique in 1728 — adjacent to the PCT Atlantic trade routes. "
                       "Both command 3–5× the price of equivalent quality Central American specialty coffee"}
    ],
    "sensory_profile": {
        "appearance": "Medium brown in filter brew; consistent clear extraction with correct grind",
        "nose": "Bright floral (jasmine, honey), stone fruit (peach, apricot), mild citrus, "
                "subtle volcanic minerality; relatively restrained compared to Ethiopian florals; "
                "more delicate and gentle than high-ester East African origins",
        "palate": "Medium body; mild-to-medium acidity (lower than Ethiopian or Colombian); "
                  "clean, sweet finish; stone fruit and mild chocolate; the volcanic soil "
                  "contributes a mineral-silica note that differentiates it from mainland US "
                  "or Central American origins; long gentle finish without astringency",
        "conclusion": "Kona coffee's reputation exceeds its complexity relative to Ethiopian or "
                      "Colombian counterparts at equivalent price points. Its value is terroir "
                      "specificity and cultural narrative: the PCT×PMT convergence, the volcanic "
                      "island origin, and the history of Pacific migration embedded in the cup."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Extra Fancy / Single Farm Cup of Excellence", "criteria": "USDA Kona Extra "
          "Fancy grade (largest screen, no defects); named farm; SCA 87+; Cup of Excellence if entered",
          "markers": "Greenwell Farms Estate; single-farm micro-lot; £40–80 per 250g; verified 100% Kona"},
        {"tier": 3, "tier_name": "Fancy Grade Single Farm", "criteria": "USDA Fancy grade; named farm "
          "(not region or blend); 100% Kona origin; specialty roaster sourced",
          "markers": "Farm name on bag; 100% Kona statement; Kona Coffee Farmers Association certified"},
        {"tier": 2, "tier_name": "Prime Grade / 100% Kona", "criteria": "USDA Prime or standard; 100% Kona; "
          "no blend; honest origin",
          "markers": "100% Kona statement without 'blend'; widely distributed; $35–55 per 250g"},
        {"tier": 1, "tier_name": "Kona Blend (10% Kona)", "criteria": "10% Kona minimum by Hawaii law; "
          "90% undisclosed origins; misleading marketing",
          "markers": "'Kona Blend' label; legally permitted but ethically questionable; very low Kona content"}
    ],
    "service_intelligence": {
        "temperature": "92–95°C for filter; 90–92°C for espresso (lower acidity requires slightly higher "
                       "temperature for full extraction)",
        "vessel": "Pour-over (V60 or Kalita for single origin filter); standard espresso demitasse",
        "technique": "Kona as pour-over: medium-coarse grind, 15:1 water:coffee, 2.5–3 minute brew. "
                     "The gentle floral character benefits from slightly slower extraction. "
                     "As espresso: medium roast, 1:2 ratio, 28 seconds — the lower acidity means "
                     "a slight under-extraction reads as balance rather than sourness. "
                     "Cold brew: excellent — the mild acidity and stone fruit work well cold",
        "programme_position": "Premium single origin feature; Pacific-themed programme anchor; "
                              "PCT×PMT storytelling piece; highest-priced coffee on any single-origin flight",
        "verbal_presentation": "Kona coffee from the slopes of Mauna Loa — volcanic basalt, hand-picked "
                               "by the family that's farmed this land since 1850. The coffee arrived in "
                               "Hawaii from Brazil in 1825; the Portuguese farmers from the Azores who "
                               "worked alongside Polynesian communities built the Kona industry. "
                               "The Pacific and the Atlantic meet in this cup."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Greenwell Farms (est. 1850, North Kona)",
        "producer_location": "North Kona District, Kealakekua, Hawaii County, Hawaii",
        "key_person": "Tom Greenwell (5th generation; current operations); "
                      "Greenwell family continuous since 1850",
        "production_volume": "~20,000 bags annually; the largest single Kona estate",
        "certifications": ["100% Kona verified", "Kona Coffee Farmers Association member",
                           "USDA Organic (selected lots)"],
        "bc_distributor": "Greenwell Farms: direct online shipping to BC available (greenwellfarms.com); "
                          "no confirmed BC brick-and-mortar agent [NEEDS VERIFICATION]",
        "us_distributor": "Greenwell Farms: direct e-commerce nationwide (greenwellfarms.com); "
                          "retail at Whole Foods Hawaii; limited national specialty retail",
        "uk_distributor": "Available through UK specialty online retailers; no major chain distribution",
        "price_tier": "Reserve (100% Kona ground: US$45–65 per 12oz; Extra Fancy: $65–95; "
                      "Greenwell Farm reserve: up to $120 per 250g)",
        "availability_notes": "100% single-farm Kona in BC: through Greenwell direct shipping or specialty "
                              "coffee importers. 'Kona blends' widely available — avoid these for programme use. "
                              "US: Greenwell direct is the reliable source; Whole Foods Hawaii stores in person. "
                              "Ka'u Coffee Mill: direct online only."
    },
    "trail_connection": "PCT-14×PMT",
    "trail_note": "Kona coffee's origin is a PCT×PMT double helix: the coffee plant arrived via Brazil "
                  "(PCT-13 — the same 1727 Portuguese-smuggled seed stock) AND the immigrant workforce "
                  "that built the Kona industry included Portuguese Azorean and Madeiran workers "
                  "(PCT-2 — the original Atlantic island coffee cultivation region). "
                  "The Pacific migration context: Japanese, Filipino, Chinese, and Korean immigrant "
                  "communities alongside Polynesian native Hawaiians all contributed to Kona's "
                  "agricultural development. Kona coffee is the Pacific basin's most complex "
                  "multicultural agricultural product.",
    "food_pairings": [
        {"technique_id": "", "dish": "Hawaiian honey cake (butter mochi with local honey)",
         "pairing_type": "complement",
         "rationale": "Hawaiian honey and Kona coffee are from the same volcanic terroir; the mochi's "
                      "glutinous rice sweetness echoes the coffee's gentle body without the tension "
                      "of high-acidity origins"},
        {"technique_id": "", "dish": "Macadamia nut tart",
         "pairing_type": "complement",
         "rationale": "Macadamia (another Hawaiian agricultural legacy) and Kona coffee both express "
                      "the mild, buttery richness of volcanic soil cultivation"}
    ],
    "source": "Kona Coffee Council official documentation; Greenwell Farms production history (est. 1850); "
              "USDA grading standards for Kona; Cup of Excellence Hawaii results; "
              "Hawaiian Historical Society records of Portuguese immigrant farming communities",
})

session.commit_batch()
print(f"\n[BATCH 21 COMMITTED — Hawaii Kona Coffee]\n")

# ============================================================
# PRODUCERS AND PURVEYORS — Rum and Coffee
# ============================================================

session.add_producer({
    "name": "Appleton Estate (Campari Group)",
    "location": "Nassau Valley, St. Elizabeth Parish, Jamaica",
    "country": "Jamaica",
    "region": "St. Elizabeth Parish, Jamaica",
    "tradition": "spirits",
    "key_person": "Joy Spence (Master Blender since 1997 — first female MB in spirits industry)",
    "founded": "1749",
    "production_volume": "~500,000 cases annually; Campari Group distribution worldwide",
    "notable_products": ["Appleton Estate Signature", "Appleton Estate 12yr Rare Casks",
                         "Appleton Estate 21yr Nassau Valley", "Appleton Estate 50yr Independence Reserve"],
    "certifications": ["Jamaica GI Rum", "Rum Producers Association of Jamaica"],
    "website": "appletonestate.com",
    "philosophy": "The oldest continually operating rum estate in the Caribbean (1749). Joy Spence, "
                  "appointed Master Blender in 1997, is one of the spirits world's most respected "
                  "blenders and the first woman to hold a Master Blender title in any spirits category. "
                  "Campari Group's ownership (since 2012) provides global distribution while maintaining "
                  "Nassau Valley's production character.",
    "trail_connection": "PCT×WADT",
    "source": "Appleton Estate official history; Campari Group 2024 annual report; JPS Rum Producers Association",
    "verified": True
})

session.add_producer({
    "name": "Demerara Distillers Ltd. (El Dorado)",
    "location": "Enmore, East Coast Demerara, Guyana",
    "country": "Guyana",
    "region": "Demerara, Guyana",
    "tradition": "spirits",
    "key_person": "Komal Samaroo (CEO); Yesu Persaud (founder)",
    "founded": "1670 (plantation history); DDL founded 1980s as Guyanese-owned entity",
    "production_volume": "Large; distributed in 50+ countries",
    "notable_products": ["El Dorado 15yr", "El Dorado 21yr", "El Dorado 25yr",
                         "El Dorado 8yr Special Reserve", "PM Mark (Velier releases)"],
    "certifications": ["Demerara Rum GI (Guyana)", "ISO 9001"],
    "website": "ddlglobal.com",
    "philosophy": "100% Guyanese-owned since independence — the post-colonial reclamation of a 350-year-old "
                  "plantation rum infrastructure. DDL operates the world's most diverse collection of "
                  "historic stills in continuous production: wooden pot stills (1732), metal pot stills, "
                  "wooden Coffey still, metal Coffey stills, and Savalle column stills.",
    "trail_connection": "PCT×WADT",
    "source": "DDL official documentation; Velier Demerara research; Dave Broom 'Rum'",
    "verified": True
})

session.add_producer({
    "name": "Greenwell Farms",
    "location": "Kealakekua, North Kona, Hawaii, USA",
    "country": "USA",
    "region": "North Kona, Hawaii County",
    "tradition": "coffee",
    "key_person": "Tom Greenwell (5th generation owner)",
    "founded": "1850 (Henry Nicholas Greenwell established the farm)",
    "production_volume": "~20,000 bags annually; largest single Kona estate",
    "notable_products": ["Greenwell Farms Medium Roast Kona", "Greenwell Farms Peaberry Kona",
                         "Greenwell Farms Extra Fancy Estate Kona", "Greenwell Farms 100% Kona Decaf"],
    "certifications": ["100% Kona verified", "Kona Coffee Farmers Association member", "USDA Organic (selected lots)"],
    "website": "greenwellfarms.com",
    "philosophy": "Five generations of Kona coffee farming since 1850 — the oldest continuously operated "
                  "Kona farm. Tom Greenwell represents the family's commitment to single-estate, 100% Kona "
                  "production at a time when the Kona name is being diluted by 10%-blend products. "
                  "Their estate museum and direct e-commerce business make them the most accessible "
                  "premium Kona producer globally.",
    "trail_connection": "PCT-14×PMT",
    "source": "Greenwell Farms official history; Kona Coffee Farmers Association membership records",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 22 COMMITTED — Key Rum and Coffee Producers]\n")

# Purveyors
session.add_purveyor({
    "name": "Campari America",
    "type": "distributor",
    "location": "New York, NY, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["spirits"],
    "producer_relationships": ["Appleton Estate Rum", "Wild Turkey Bourbon", "Campari", "Aperol", "Grand Marnier"],
    "website": "camparigroup.com",
    "contact": "campariamerica.com",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Campari America handles Appleton Estate US national distribution. "
                      "Appleton widely available at Total Wine, BevMo, and national chains. "
                      "NOTE: Canadian distribution effective April 1, 2025 transferred to "
                      "Southern Glazer's Wine & Spirits of Canada (new national agreement).",
    "verified": True
})

session.add_purveyor({
    "name": "Southern Glazer's Wine & Spirits of Canada",
    "type": "distributor",
    "location": "Canada",
    "markets_served": ["nationwide_Canada", "BC", "Alberta", "Ontario"],
    "traditions_carried": ["spirits"],
    "producer_relationships": ["Appleton Estate Rum"],
    "website": "southernglazers.com",
    "contact": "southernglazers.com/canada",
    "minimum_order": "Trade accounts",
    "delivery_notes": "SGWS Canada assumed national distribution of Appleton Estate effective April 1, 2025 "
                      "(confirmed via BusinessWire). Replaces previous Campari Canada arrangement. "
                      "Appleton widely available at BC Liquor stores under this arrangement.",
    "verified": True
})

session.add_purveyor({
    "name": "Maisons Marques & Domaines USA (MMD)",
    "type": "importer",
    "location": "Oakland, CA, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["wine", "spirits", "champagne", "fortified"],
    "producer_relationships": ["Louis Roederer Champagne", "Ramos Pinto Port", "Château Pichon Baron",
                               "Domaine Ott", "Scharffenberger Cellars"],
    "website": "mmdusa.net",
    "contact": "mmdusa.net/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "US subsidiary of the Louis Roederer group. Confirmed US importer for Ramos Pinto "
                      "Port as part of the Louis Roederer portfolio. National distribution across all "
                      "50 states through established premium wine/spirits trade channels.",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 23 COMMITTED — Final Purveyors]\n")

handoff = session.finish()
print(handoff)
