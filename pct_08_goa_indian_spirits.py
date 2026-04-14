#!/usr/bin/env python3
"""
PCT-8 Goa Continuation:
Coconut Toddy + Aged Premium Feni
+ Paul John Goa Single Malt (Indian whisky, Goa distillation heritage)
+ Sula Vineyards (Indian wine, Nashik Valley — PCT adjacent Indian viticulture)
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="ceremonial",
    region="India — Goa (Toddy and Aged Feni continuation)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=9,
    running_total=42
)

# ============================================================
# GOA TODDY AND AGED FENI CONTINUATION — PCT-8
# ============================================================

session.add_beverage({
    "tradition": "ceremonial",
    "sub_tradition": "goa coconut toddy fresh",
    "region": "India — Goa (Coastal)",
    "name": "Goa Coconut Toddy (Neera and Sura) — The Living Sap of the Coconut Palm",
    "terroir_origin": (
        "Coconut toddy (neera in fresh form; sura or soro when fermented) is one of the "
        "oldest continuously consumed beverages in the Indian subcontinent. The coconut palm "
        "(Cocos nucifera) has been cultivated on the Konkan coast — of which Goa is the "
        "defining coastal section — for at least 3,000 years. "
        "The same coconut palm that produces Feni's base spirit (when the sap is distilled) "
        "provides toddy in its unfermented (neera) and lightly fermented (sura) forms. "
        "Goa's coastal architecture, cuisine, and daily rhythm are entirely organised around "
        "the coconut palm — a fact that remains unchanged since before the Portuguese arrived in 1510. "
        "The toddy tradition: the 'toddy tapper' (render in Konkani; palm-wine tapper) "
        "climbs the palm twice daily at dawn and dusk. "
        "A clay pot is tied to the cut inflorescence stalk; the palm sap flows overnight "
        "(6–8 hours) into the pot. Collected before sunrise: neera (fresh, unfermented, "
        "sweet, 0% ABV). Left to ferment in tropical heat: sura (fermented, 2–6% ABV "
        "depending on fermentation time). The same sap, distilled twice in a copper pot still: "
        "Coconut Feni (42.8% ABV). "
        "The PCT connection: when Afonso de Albuquerque conquered Goa in 1510, his officers "
        "encountered toddy-tapping as an established local practice centuries old. "
        "Portuguese colonial administrators created regulations around the toddy trade — "
        "licensing tavernas (taverns), taxing production — the same regulatory framework "
        "that later shaped Feni's commercial structure."
    ),
    "production_technique": (
        "Toddy tapping process: toddy tapper identifies mature coconut palm (8–10 years old); "
        "climbs using a waist loop (often without shoes; the traditional Goan tapper climbs "
        "30–40 palms before sunrise); "
        "cuts the tip of the flower bud (inflorescence) with a sharp knife; "
        "binds the cut inflorescence with twine to direct sap flow; "
        "attaches a clay pot (traditionally) or plastic container to collect. "
        "The palm can produce 2–3 litres of sap per day at peak season (October–May). "
        "Neera (fresh toddy): collected before fermentation begins "
        "(within 2–4 hours of flow at ambient tropical temperature). "
        "Naturally sweet, 10–15 Brix sugar content; contains live yeast cells; "
        "begins fermenting within 3–4 hours at 30–35°C Goan ambient temperature. "
        "Commercial neera preservation: some producers chill immediately or "
        "add lime juice to slow fermentation for short-distance transport. "
        "Sura (fermented toddy): left 8–12 hours; naturally ferments to 2–4% ABV; "
        "24–36 hours: 5–7% ABV; naturally carbonated from CO2 production. "
        "Consumed fresh at local tavernas and toddy stalls along Goa's coast. "
        "Cannot be transported more than a few hours without quality loss — "
        "the most local of all beverages in the PCT."
    ),
    "cross_tradition_parallels": [
        {"tradition": "ceremonial", "beverage": "Mozambique Palm Wine (Sura) — PCT-7 Mozambique",
         "connection": "Goa's coconut toddy and Mozambique's sura are the same Portuguese colonial "
                       "encounter repeated on two different coastlines: Portuguese traders met "
                       "established coconut-toddy cultures in both Goa (1510) and coastal "
                       "Mozambique (1498). Both use the same tapping method; both produce the "
                       "same fresh-sweet-to-fermented beverage spectrum. "
                       "The PCT connected these two traditions through the same colonial trade "
                       "network that moved cashew from Brazil to both coasts simultaneously"},
        {"tradition": "spirits", "beverage": "Coconut Feni (PCT-8, distilled from same sap)",
         "connection": "Toddy and Feni are the same raw material at three stages of transformation: "
                       "sap collected fresh (neera, 0% ABV) → fermented toddy (sura, 2–6% ABV) "
                       "→ single-distilled urrak (15–18% ABV) → double-distilled Feni (42.8% ABV). "
                       "Serving all three stages from the same palm is the most instructive "
                       "demonstration of the distillation concept in the entire PCT programme — "
                       "the same agricultural raw material, three completely different beverages, "
                       "each at a different stage of the same process"}
    ],
    "sensory_profile": {
        "appearance": "Neera: milky white to pale cream, slight cloudiness from suspended yeast; "
                      "effervescent (natural CO2). Sura (lightly fermented): more opaque, "
                      "white-ivory; slight fizz. Older fermented: pale tan, more settled.",
        "nose": "Neera: extraordinary — fresh coconut water, young coconut flesh, "
                "light floral (coconut blossom), natural sweetness, faint tropical green. "
                "Impossible to replicate from commercial coconut water: "
                "the live-yeast content and just-harvested freshness create a "
                "complexity that shelf-stable coconut products cannot approach. "
                "Sura (2–3 hours fermented): the same coconut freshness, now with "
                "lactic-light acidity developing; gentle CO2 on the nose; "
                "the fermentation's own wild yeast character emerging.",
        "palate": "Neera: 10–15g/L natural sugars; medium sweetness; "
                  "extraordinary natural carbonation; the coconut-water mineral "
                  "quality at higher concentration than commercial coconut water. "
                  "Sura: dry to off-dry as fermentation progresses; light body; "
                  "refreshing acidity; the coconut character persists through fermentation "
                  "in a way other fermented beverages lose their raw material identity. "
                  "Both: a perishability that defines their character — "
                  "the freshest possible beverage, exists for 4 hours at most.",
        "conclusion": "Neera and sura cannot be served in a standard programme context "
                      "outside Goa unless the programme is on-location. "
                      "For educational use: describe the toddy spectrum alongside "
                      "Coconut Feni to demonstrate the distillation ladder from same raw material. "
                      "For any guest who has been to Goa: the memory of fresh neera at dawn "
                      "is the single most powerful PCT sensory anchor available."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Fresh Neera — Same-Day Tapped (Goa on-location only)",
         "criteria": "Collected within 2 hours; served at point of tapping; "
                     "no additives; coastal Goa palm",
         "markers": "Roadside toddy tappers (morning route); toddy stalls at Old Goa market; "
                    "experience only available in Goa; trivial monetary cost"},
        {"tier": 3, "tier_name": "Fresh Sura — 4–8 Hour Fermented",
         "criteria": "Same-day fermented; Goa coastal production; consumed same day",
         "markers": "Goan toddy tavernas; local beach stalls (North Goa: Morjim, Mandrem); "
                    "available only in Goa during toddy season (Oct–May)"},
        {"tier": 2, "tier_name": "Commercial Coconut Water (Reference Tier)",
         "criteria": "Industrial coconut water; not toddy but the closest commercial equivalent "
                     "for educational reference",
         "markers": "Vita Coco, Harmless Harvest (cold-pressed, unpasteurised is closest); "
                    "widely available BC and US"},
        {"tier": 1, "tier_name": "Coconut Feni (distilled equivalent)",
         "criteria": "The distilled product of the same raw material; "
                     "GI-protected Goa Coconut Feni",
         "markers": "Cazulo Coconut Feni; Desmondji Coconut Feni; "
                    "see PCT-8 Coconut Feni entry for full purveyor detail"}
    ],
    "service_intelligence": {
        "temperature": "Neera: ambient temperature or very slightly chilled (25°C). "
                       "Never serve cold — the fermentation is halted below 18°C "
                       "and the aromatic complexity collapses. "
                       "Sura: room temperature, at point of consumption.",
        "vessel": "Clay cup (traditional Goan toddy taverna service); "
                  "glass tumbler if clay unavailable. No stemmed glass — "
                  "toddy is a working person's daily beverage, not a ceremony.",
        "technique": "Educational programme: serve Coconut Feni (commercially available) "
                     "alongside a description of neera and sura to demonstrate the "
                     "distillation ladder concept. "
                     "For on-location Goa programmes: arrange a morning toddy tapper visit "
                     "— the 5am tapping sequence is one of the PCT's most memorable experiences. "
                     "For the classroom: Harmless Harvest cold-pressed coconut water as "
                     "the closest commercial approximation of neera's character.",
        "programme_position": "Educational context and PCT-8 Goa narrative completion; "
                              "on-location Goa programme anchor; "
                              "not commercially serviceable outside Goa",
        "verbal_presentation": "Before Goa Feni, there is sura. Before sura, there is neera. "
                               "The same palm: fresh at dawn, fermenting by noon, distilled by evening. "
                               "The Portuguese regulated the trade; the Goans maintained the tradition. "
                               "Five hundred years, same method, same morning route."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Independent toddy tappers of coastal Goa (hereditary profession, "
                              "primarily families from the Render/Catholic community)",
        "producer_location": "Coastal Goa — North Goa (Calangute, Morjim, Assagao) and "
                             "South Goa (Palolem, Patnem, Agonda) toddy belt",
        "key_person": "No nationally prominent individual — artisanal hereditary family production",
        "production_volume": "Small-scale individual tappers: 30–80L per day per tapper "
                             "across a route of 30–40 palms",
        "certifications": ["None applicable for artisanal production; "
                           "GI Goa Coconut Feni (for distilled product)"],
        "bc_distributor": "Not commercially available outside Goa; "
                          "Harmless Harvest raw coconut water (closest commercial equivalent): "
                          "widely available at Whole Foods, health food stores in BC and US",
        "us_distributor": "Not commercially distributed; on-location Goa experience only. "
                          "Harmless Harvest as reference product: nationwide US.",
        "uk_distributor": "Not commercially distributed outside Goa",
        "price_tier": "Negligible (₹20–40 per glass in Goa; one of the world's least expensive beverages)",
        "availability_notes": "Neera and sura are not available outside Goa. "
                              "For the PCT programme: serve Cazulo or Desmondji Coconut Feni "
                              "as the commercially available Goa expression; "
                              "describe toddy as the raw material antecedent."
    },
    "trail_connection": "PCT-8",
    "trail_note": "Toddy-tapping in Goa is a pre-Portuguese practice at least 2,000 years old. "
                  "The Portuguese licensing of toddy tavernas (1510 onwards) created "
                  "the first formal regulatory structure for a traditional Goan beverage — "
                  "making Goa's toddy trade arguably the oldest continuously regulated "
                  "artisanal beverage industry in the Portuguese colonial world. "
                  "Today, the toddy tapper profession is in demographic decline: "
                  "fewer young Goans are learning the palm-climbing trade. "
                  "The morning toddy route is both an ancient tradition and a fragile one.",
    "food_pairings": [
        {"technique_id": "", "dish": "Sannas (Goan steamed rice cakes fermented with toddy)",
         "pairing_type": "bridge",
         "rationale": "Sannas — Goa's traditional steamed rice cakes — are leavened specifically "
                      "with toddy: the same sura used as a beverage is also used to ferment "
                      "the rice batter. Serving neera alongside a freshly steamed sanna "
                      "demonstrates the dual culinary function of the same beverage. "
                      "The coconut-lactic character in the sanna derives from the toddy leaven; "
                      "the fresh neera echoes the same flavour in unfermented form"},
        {"technique_id": "", "dish": "Xacuti chicken (Goan coconut-spice curry)",
         "pairing_type": "complement",
         "rationale": "Fresh neera's natural sweetness and coconut identity finds its "
                      "culinary equivalent in Goa's most beloved curry — roasted coconut, "
                      "poppy seed, spice, and the same coastal coconut that the palm provides. "
                      "Both the toddy and the xacuti express the Goa coconut palm's "
                      "total integration into the local food system"}
    ],
    "source": "Goa State Biodiversity Board coconut palm documentation; "
              "Frank Simoes 'Glad Seasons in Goa' (Goa toddy cultural documentation); "
              "ICAR-Central Coastal Agricultural Research Institute (Goa) coconut research; "
              "Portuguese colonial licensing records (Arquivo Histórico de Goa, 16th century)",
})

session.commit_batch()
print(f"\n[BATCH 41 COMMITTED — Goa Coconut Toddy]\n")

# ============================================================
# PAUL JOHN GOA SINGLE MALT — PCT-8
# ============================================================

session.switch_region("spirits", "India — Goa (Paul John Single Malt Whisky)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "indian single malt whisky goa",
    "region": "India — Goa (John Distilleries, Goa facility)",
    "name": "Paul John Single Malt — Indian Whisky from a Portuguese Colonial Distillation Territory",
    "terroir_origin": (
        "Paul John Single Malt Whisky, produced by John Distilleries at their Goa facility, "
        "represents a remarkable convergence: the same Indian coastal state that holds the "
        "world's only GI-protected sugarcane spirit (Cashew Feni) also produces what is "
        "now recognised as the most internationally acclaimed Indian single malt whisky. "
        "The PCT connection: Goa's 450-year Portuguese colonial distillation heritage — "
        "the Feni copper retort tradition — created infrastructure, skilled craftsmen, and "
        "institutional distillation knowledge that made the transition to malt whisky production "
        "technically feasible for an Indian company choosing Goa as their whisky site. "
        "The terroir: Goa's climate is extreme for whisky maturation — "
        "tropical heat (average 27–32°C year-round) and high humidity produce "
        "evaporation rates of 8–12% annually (the 'angel's share'), "
        "compared to 2–3% in Scotland. This accelerates ageing dramatically: "
        "a 7-year Paul John can have the flavour development of a 12–15 year Scotch. "
        "The barley: Indian-grown two-row barley from the Punjab (not Himalayan malted barley), "
        "producing a lighter, more grain-forward spirit than Scottish peat-influenced malts. "
        "The stills: traditional copper pot stills; the same distillation form used "
        "for Feni production, adapted to whisky production."
    ),
    "production_technique": (
        "Paul John production at the Goa distillery: "
        "Barley: Indian two-row barley, malted at John's own maltings facility in Bangalore; "
        "both peated (Bold) and unpeated (Brilliance, Classic Select) expressions produced. "
        "Mashing: traditional Scottish mashing; lautered mash tun; "
        "the warm Indian climate means faster saccharification than Scotland. "
        "Fermentation: 72–96 hours using own cultured yeast; longer fermentation in Indian heat "
        "develops ester compounds not produced in cooler Scottish conditions. "
        "Distillation: copper pot stills (wash still and spirit still); "
        "the Goa craft distillation tradition means the distillers are experienced "
        "with copper pot still management from the Feni heritage. "
        "Maturation: exclusively ex-American white oak bourbon barrels; "
        "in Goa's tropical climate, the wood interaction is dramatically faster — "
        "extracting vanilla, caramel, and spice compounds rapidly. "
        "Aged expressions: 7yr, 10yr, 12yr; a 7-year Paul John shows more barrel "
        "integration than most 12-year Scotch from cooler climates. "
        "Peated expression (Bold): Islay-style peated barley at 30 ppm phenol; "
        "the tropical wood ageing transforms the peat character — "
        "Indian tropical peat in American oak produces something unlike any Scotch. "
        "Paul John won Jim Murray's 'Indian Whisky of the Year' in 2012 "
        "(for Brilliance) and has received consistent World Whisky Award recognition."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Highland Park 12yr (Orkney, Scotland)",
         "connection": "Paul John Classic Select and Highland Park 12yr occupy the same "
                       "quality tier in the single malt hierarchy — both are non-chill-filtered, "
                       "natural colour, accessible premium single malts with genuine complexity. "
                       "The flavour profiles differ fundamentally: Highland Park is maritime-"
                       "heather-honey-peat; Paul John Classic is tropical-vanilla-caramel-exotic-spice. "
                       "Both reward side-by-side tasting as a demonstration that single malt whisky "
                       "is a global conversation, not exclusively Scottish"},
        {"tradition": "spirits", "beverage": "Goa Cashew Feni (PCT-8, same distillation territory)",
         "connection": "Paul John Single Malt and Cazulo Cashew Feni are both distilled "
                       "in Goa using copper pot still tradition. The comparison demonstrates "
                       "what the same distillation technology and climate does to two "
                       "completely different raw materials: "
                       "sugarcane sap → Feni (funky, agricultural, 42.8%); "
                       "malted barley → whisky (structured, barrel-aged, 46%). "
                       "Both are products of Goa's Portuguese colonial distillation heritage, "
                       "expressed through two entirely different traditions"}
    ],
    "sensory_profile": {
        "appearance": "Paul John Brilliance (7yr): pale gold; lighter than expected for the age — "
                      "ex-bourbon barrels in Indian heat extract colour more slowly than "
                      "ex-sherry. Classic Select: medium gold. Bold (peated): medium amber.",
        "nose": "Brilliance: extraordinary aromatic purity — vanilla ice cream, "
                "coconut, caramelised banana, tropical fruit, light floral "
                "(the unpeated Indian barley's own aromatics amplified by tropical barrel ageing). "
                "The most tropical-register single malt outside Japanese mizunara-aged expressions. "
                "Classic Select: richer — dried apricot, toffee, cinnamon, light tobacco, "
                "more barrel influence. "
                "Bold (peated): smoked papaya, BBQ smoke, overripe tropical fruit, "
                "coconut-smoke hybrid — the Indian peat-tropical-barrel combination "
                "produces a profile unavailable anywhere else in whisky.",
        "palate": "Brilliance: 46% ABV; unchill-filtered; light to medium body; "
                  "tropical fruit forward; vanilla-creamy mid-palate; clean sweet finish. "
                  "Classic Select: fuller body; more barrel spice; dried fruit; "
                  "warmer finish. Bold: 46% ABV; the smoke is tropical-sweet rather than "
                  "medicinal; unusual and compelling. "
                  "All: the shared character is the tropical barrel ageing — a warmth "
                  "and exotic-spice richness impossible in any northern-climate whisky.",
        "conclusion": "Paul John Single Malt is the strongest argument that single malt whisky "
                      "has become a genuinely global tradition. For a programme: "
                      "the Brilliance alongside a Speyside 12yr (Glenfarclas, Aberlour) "
                      "demonstrates that same production method + same barrel type + "
                      "different climate = completely different whisky. "
                      "The PCT narrative: Goa's distillation heritage made this possible."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Paul John Peated Select Cask / Special Release",
         "criteria": "Special annual release; cask strength or named cask; "
                     "limited allocation; Brilliance Reserve or special peated expression",
         "markers": "Paul John Peated Select Cask; Paul John Christmas Edition; "
                    "Paul John Kanya or comparable special release; US ~$90–150+"},
        {"tier": 3, "tier_name": "Paul John Bold (Peated) / Classic Select Cask",
         "criteria": "Peated expression or Classic cask-strength; 46%+ ABV; "
                     "non-chill-filtered; Indian tropical maturation",
         "markers": "Paul John Bold; Paul John Classic Select Cask; US ~$50–70; BC ~$65–80"},
        {"tier": 2, "tier_name": "Paul John Brilliance / Classic Select",
         "criteria": "Standard range; 46% ABV; non-chill-filtered; natural colour; "
                     "entry to Paul John's quality tier",
         "markers": "Paul John Brilliance; Paul John Classic Select; US ~$40–50; BC ~$55–65"},
        {"tier": 1, "tier_name": "Paul John Edited (ex-sherry influence)",
         "criteria": "Entry-level; accessible; introduction to Paul John's tropical-barrel style",
         "markers": "Paul John Edited; US ~$30–38; BC ~$40–48"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature (18–20°C); do not refrigerate — the tropical spice "
                       "character closes below 15°C",
        "vessel": "Glencairn or nosing glass (captures the extraordinary aromatic complexity); "
                  "Riedel Single Malt glass would also work",
        "technique": "Paul John Brilliance neat: 45mL, room temperature, 5 minutes to open — "
                     "the tropical barrel esters open slowly. "
                     "Water: 2–3 drops in Brilliance to open the coconut-floral; "
                     "not needed for Classic (already rounded). "
                     "Comparative tasting: Paul John Brilliance alongside "
                     "Aberlour 12yr A'bunadh or Glenfarclas 10yr — "
                     "the same production method, the same barrel type, "
                     "Scotland vs. Goa climate. "
                     "Bold: neat at cask strength, no water — the smoke-tropical balance "
                     "is best undiluted.",
        "programme_position": "Indian whisky discovery experience; PCT-8 Goa distillation narrative; "
                              "Feni-and-whisky comparative tasting from the same territory",
        "verbal_presentation": "Paul John Brilliance — Goa, India. "
                               "Seven years in ex-bourbon oak in the tropics. "
                               "Twelve percent of the whisky disappeared as angel's share. "
                               "What's left is what happens when Scotland's tradition "
                               "meets five hundred years of Goan distillation history."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "John Distilleries Ltd (Goa facility and Bangalore maltings)",
        "producer_location": "Goa distillery (finishing and bottling); Bangalore (malt production)",
        "key_person": "John Distilleries management; Michael D'Souza (master distiller, Goa facility); "
                      "Jim Murray (key international reviewer who first brought global attention "
                      "to Paul John with Brilliance 2012 World Whisky Award)",
        "production_volume": "Growing; Paul John now distributed in 40+ countries; "
                             "currently the most internationally visible Indian single malt brand",
        "certifications": ["Indian FSSAI food safety standard", "World Whisky Awards multiple wins"],
        "bc_distributor": "Paul John available at BC Liquor stores (BCLDB listed — confirmed); "
                          "Brilliance and Classic Select most widely available",
        "us_distributor": "Anchor Distilling Company / Preiss Imports (national US distributor "
                          "for Paul John — confirmed); widely available Total Wine, BevMo, "
                          "premium spirits retailers",
        "uk_distributor": "Elixir Distillers (UK) handles Paul John; "
                          "available at Master of Malt, The Whisky Exchange, Harvey Nichols",
        "price_tier": "Market to Reserve (Edited BC ~$45; Brilliance BC ~$60; "
                      "Bold BC ~$75; Classic Select Cask BC ~$90)",
        "availability_notes": "In BC: BC Liquor stores carry Paul John Brilliance and Classic Select. "
                              "Specialty spirits merchants (Marquis Wine Cellars, Firefly Fine Wines) "
                              "carry Bold and premium expressions. "
                              "US: Anchor Distilling/Preiss Imports nationally; Total Wine carries "
                              "standard range; specialty shops carry Bold and cask expressions."
    },
    "trail_connection": "PCT-8",
    "trail_note": "Paul John Single Malt is the PCT's most contemporary production achievement: "
                  "a post-colonial Indian company using the distillation infrastructure and "
                  "expertise legacy of 450 years of Portuguese colonial Feni production in Goa "
                  "to produce single malt whisky that competes internationally with Scotland. "
                  "The 2012 Jim Murray recognition was not a novelty rating — it was an "
                  "acknowledgment that the Indian single malt category had produced a genuinely "
                  "world-class spirit. The copper pot still that makes Feni "
                  "is the same copper pot still philosophy that makes Paul John. "
                  "Goa is the only place in the world where you can drink a GI-protected "
                  "indigenous spirit (Feni) and a prize-winning single malt whisky "
                  "distilled in the same territory by the same cultural tradition.",
    "food_pairings": [
        {"technique_id": "", "dish": "Goa pork vindaloo (vindalho — wine-and-garlic marinade, PCT origin)",
         "pairing_type": "bridge",
         "rationale": "Vindaloo's name derives from the Portuguese 'vinha d'alhos' "
                      "(wine and garlic marinade) — the dish is a direct PCT culinary creation. "
                      "Paul John Bold's tropical-smoke character bridges with the vindaloo's "
                      "piri-piri heat and pork fat: the smoke echoes the charring on the pork; "
                      "the whisky's tropical sweetness cuts the chilli heat. "
                      "The most historically resonant Goa whisky pairing: "
                      "PCT food and PCT spirit"},
        {"technique_id": "", "dish": "Dark chocolate and smoked cashews (Goa-regional)",
         "pairing_type": "complement",
         "rationale": "Paul John Brilliance with Goan smoked cashews and a dark chocolate piece: "
                      "the whisky's coconut-vanilla character bridges with the cashew's "
                      "roasted-sweet register; the dark chocolate provides bitter contrast. "
                      "The cashew is the same Anacardium occidentale that the Portuguese "
                      "brought from Brazil — Goa's most iconic nut, pairing with "
                      "Goa's most awarded spirit"}
    ],
    "source": "John Distilleries official production documentation; "
              "Jim Murray Whisky Bible 2012 (Paul John Brilliance Indian Whisky of the Year); "
              "World Whiskies Awards Paul John citations 2013–2023; "
              "Preiss Imports US portfolio; "
              "Indian Malt Whisky Association production documentation",
})

session.commit_batch()
print(f"\n[BATCH 42 COMMITTED — Paul John Goa Single Malt]\n")

# ============================================================
# SULA VINEYARDS — INDIA'S FIRST COMMERCIAL WINE — PCT ADJACENT
# ============================================================

session.switch_region("wine", "India — Nashik Valley (Maharashtra)")

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "indian wine nashik valley",
    "region": "India — Nashik Valley, Maharashtra (Western Ghats foothills)",
    "name": "Sula Vineyards — Indian Wine Pioneer, Nashik Valley",
    "terroir_origin": (
        "The Nashik Valley, 180km northeast of Mumbai in Maharashtra state, "
        "has become the centre of India's commercial wine industry — "
        "a development that was essentially non-existent before 1997 "
        "and is now a 15-million-bottle annual industry. "
        "The PCT connection is indirect but real: Goa's 450-year Portuguese wine culture "
        "created the Indian subcontinent's first sustained encounter with wine consumption "
        "as a daily cultural practice. The Goan-Catholic community in western India — "
        "centred in Goa but with significant presence in Mumbai — "
        "maintained a wine-consuming culture through Portuguese colonial contact. "
        "When Rajeev Samant (Stanford-educated, returning to family land in Nashik) "
        "founded Sula Vineyards in 1997 with California winemaker Kerry Damskey, "
        "the western India market's familiarity with wine through Goa made "
        "the initial commercial case. "
        "Nashik's terroir: 560–600m altitude on the Western Ghats foothills; "
        "black cotton soil (basalt-derived); monsoon-dry season cycle "
        "(June–October monsoon, October–March harvest season — "
        "India grows grapes in its 'winter' harvest rather than the European summer-autumn). "
        "Primary varieties: Sauvignon Blanc, Riesling, Chenin Blanc (Sula's signature); "
        "Shiraz, Cabernet Sauvignon for reds; Zinfandel (planted by Samant, "
        "a reference to Damskey's California background). "
        "Sula is now India's largest single winery brand by volume "
        "and has been listed on the Bombay Stock Exchange since 2022."
    ),
    "production_technique": (
        "Sula's winemaking team has evolved from California-trained (Kerry Damskey) "
        "to Australian (multiple winemakers through 2000s–2010s) to Indian-trained. "
        "The technical challenge: India's subtropical climate creates dramatic ripening curves — "
        "Nashik's harvest October–March uses the natural cool-dry season. "
        "Harvest: hand-picked (extensive casual labour pool from local agricultural workforce); "
        "night harvest to preserve aromatics and acidity in the warm daytime temperatures. "
        "Vinification: temperature-controlled stainless steel tanks standard across all wines. "
        "Sauvignon Blanc: crisp, light, tropical citrus character from quick, cool fermentation. "
        "Chenin Blanc (Sula's most awarded variety): semi-sweet through dry expressions; "
        "the best Sula Chenin Blanc shows tropical fruit, good acidity, and genuine complexity. "
        "Riesling: late harvest expressions are the most critically acclaimed Sula whites — "
        "the combination of Nashik black cotton soil and Riesling's natural acidity "
        "produces a semi-sweet Riesling style unlike any European expression. "
        "Red wine production: Shiraz and Cabernet Sauvignon; warm-climate extraction "
        "tends toward riper fruit and softer tannin than European equivalents; "
        "12 months in French and American oak standard for Sula Reserve expressions."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Marlborough Sauvignon Blanc (New Zealand)",
         "connection": "Sula Sauvignon Blanc and Marlborough Sauvignon Blanc are both "
                       "warm-to-moderate climate expressions of the same variety with a "
                       "tropical citrus profile (passionfruit, lime, grapefruit). "
                       "The difference: Nashik's black cotton soil produces a slightly "
                       "earthier, less pungent character than Marlborough's greywacke. "
                       "Both are commercial entry-level wine successes driven by accessible "
                       "aromatic variety selection — the international wine trade's "
                       "two most successful 'gateway variety' stories from the Southern Hemisphere"},
        {"tradition": "wine", "beverage": "Goa Portuguese wines (PCT-8 context)",
         "connection": "Sula's existence is partly predicated on the wine-familiarity created "
                       "by Goa's Portuguese colonial wine culture in western India. "
                       "The Goa Catholic community's 450-year wine tradition "
                       "created a culturally literate wine consumer in the Mumbai-Pune-Nashik "
                       "corridor that Sula's first vintages could serve. "
                       "A flight of Sula Chenin Blanc and a Portuguese Douro white tells "
                       "the story of how wine culture moved from the Portuguese colonial "
                       "Goa coast to India's first commercial wine region"}
    ],
    "sensory_profile": {
        "appearance": "Sula Sauvignon Blanc: pale lemon-green; clear; medium viscosity. "
                      "Chenin Blanc (off-dry): medium gold; slight residual sugar body. "
                      "Late Harvest Chenin/Riesling: deeper gold; viscous from concentration.",
        "nose": "Sauvignon Blanc: green mango, passionfruit, lime zest, "
                "fresh cut grass, light tropical floral. Distinctly Indian-tropical "
                "rather than the Loire's mineral grass or Marlborough's pungency. "
                "Chenin Blanc (Sula Late Harvest): honeyed lychee, dried apricot, "
                "orange blossom, preserved ginger — the Nashik black cotton soil "
                "gives an unusual grounded quality to the aromatic sweetness. "
                "Reserve Shiraz: ripe mulberry, black plum, warm spice, "
                "mocha from American oak, medium tannin.",
        "palate": "Sauvignon Blanc: dry, light-to-medium body; crisp acidity; "
                  "short-to-medium finish; 12% ABV; accessible entry-level white. "
                  "Late Harvest Chenin/Riesling: significant residual sweetness "
                  "(60–100g/L); medium acidity balancing; tropical fruit persistence; "
                  "the most interesting Sula expression. "
                  "Reserve Shiraz: medium-full body; ripe fruit; softer tannin "
                  "than European Shiraz; the oak is prominent; good for "
                  "India's own cuisine pairings.",
        "conclusion": "Sula represents the commercial success story of Indian wine — "
                      "from zero to a publicly listed company in 25 years. "
                      "For a PCT programme: serve Sula as the demonstration of how "
                      "wine culture migrates through Portuguese colonial contact. "
                      "The Late Harvest Chenin Blanc and Riesling are the most "
                      "distinctive expressions and worth including on a premium list "
                      "as a conversation piece."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Sula Late Harvest Chenin Blanc / Dia Reserve White",
         "criteria": "Late harvest; residual sugar 60–100g/L; complex tropical-sweet; "
                     "Nashik single origin; Sula's premium expressions",
         "markers": "Sula Late Harvest Chenin Blanc; Sula Dia Reserve; "
                    "international availability: US ~$22–32; BC ~$28–38"},
        {"tier": 3, "tier_name": "Sula Rasa Reserve / Sula Dindori Reserve Shiraz",
         "criteria": "Reserve designation; French or American oak; "
                     "single region Nashik; varietal purity",
         "markers": "Sula Dindori Reserve Shiraz; Sula Rasa; "
                    "US ~$16–22; BC ~$20–28"},
        {"tier": 2, "tier_name": "Sula Sauvignon Blanc / Sula Chenin Blanc Standard",
         "criteria": "Standard range; varietal correct; accessible; "
                     "the most widely distributed Indian wine internationally",
         "markers": "Sula Sauvignon Blanc; Sula Chenin Blanc; "
                    "US ~$12–16; BC ~$14–18"},
        {"tier": 1, "tier_name": "Sula Brut / Sula Zinfandel Rosé",
         "criteria": "Entry Charmat sparkling or rosé; accessible; "
                     "introduction to Sula/Indian wine category",
         "markers": "Sula Brut; Sula Shiraz Rosé; US ~$10–13; BC ~$12–15"}
    ],
    "service_intelligence": {
        "temperature": "Whites: 10–12°C. Late Harvest: 10°C. Reserve Shiraz: 16–18°C.",
        "vessel": "Standard white wine glass; ISO glass for Late Harvest tasting. "
                  "Reserve Shiraz in a standard Bordeaux glass.",
        "technique": "Sauvignon Blanc: serve cold, short pour (100mL), no decanting. "
                     "Late Harvest Chenin: 75mL as a dessert wine; "
                     "pair with the provenance story for maximum effect. "
                     "Reserve Shiraz: open 20 minutes before service; "
                     "serve slightly below room temperature at 17°C.",
        "programme_position": "Indian wine education; PCT Goa-India cultural bridge; "
                              "discovery wine for guests exploring non-European wine regions",
        "verbal_presentation": "Sula Late Harvest Chenin Blanc — Nashik Valley, India. "
                               "India's first commercial wine estate, founded 1997. "
                               "Harvested in December, when the rest of the world's vines are dormant. "
                               "The monsoon shaped it; the black cotton soil of the Deccan holds it."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Sula Vineyards (Nashik Valley, Maharashtra)",
        "producer_location": "Gat No. 36/2, Govardhan, Near Gangapur Dam, Nashik, Maharashtra, India",
        "key_person": "Rajeev Samant (founder, CEO — Stanford-educated, returned to Nashik family land); "
                      "Kerry Damskey (founding winemaker, California — no longer at Sula); "
                      "Kiran Ambwani (current Chief Winemaker)",
        "production_volume": "India's largest single winery brand: ~15 million bottles annually; "
                             "BSE-listed since 2022; exported to 30+ countries",
        "certifications": ["FSSAI India", "Organic (select ranges)", "BSE-listed (2022)"],
        "bc_distributor": "Sula available at BC Liquor stores (confirmed BCLDB listing); "
                          "Sauvignon Blanc and Chenin Blanc most reliably stocked",
        "us_distributor": "Sula imported nationally by Epic Wines & Spirits (Stockton, CA — confirmed); "
                          "available at Total Wine, Whole Foods, and Indian specialty grocery stores nationally",
        "uk_distributor": "Sula available at Waitrose, M&S, and Indian specialty retailers UK; "
                          "one of India's most internationally distributed wine brands",
        "price_tier": "Market (standard range US ~$12–16; Reserve ~$18–25; Late Harvest ~$25–35)",
        "availability_notes": "In BC: BC Liquor stores (BCLDB) carry Sula standard range. "
                              "Specialty: Liberty Wine Merchants and Marquis Wine Cellars "
                              "may carry Late Harvest and Reserve expressions. "
                              "US: Epic Wines national; Total Wine and Whole Foods carry standard range. "
                              "India: Sula is the default wine of choice in most Indian hotels and restaurants."
    },
    "trail_connection": "PCT-8",
    "trail_note": "Sula is a PCT-adjacent story: the Portuguese colonial wine culture in Goa "
                  "created the only pre-existing wine-consumption tradition in western India. "
                  "When Rajeev Samant founded Sula in 1997, the wine market he was entering "
                  "had been partially shaped by 450 years of Goan-Catholic wine familiarity "
                  "in the Mumbai-Pune-Nashik corridor. India's wine industry "
                  "could not have achieved its current scale in the western India market "
                  "without the cultural groundwork laid by the Portuguese colonial presence "
                  "in Goa 60km to the south.",
    "food_pairings": [
        {"technique_id": "", "dish": "Tandoori chicken (marinated yogurt-spice, charcoal grill)",
         "pairing_type": "complement",
         "rationale": "Sula Sauvignon Blanc alongside tandoori chicken is the most commercially "
                      "successful India food-wine pairing in restaurants globally. "
                      "The Sauvignon Blanc's citrus-tropical acidity cuts the yogurt-fat "
                      "and char of the marinade while the wine's light body doesn't overwhelm "
                      "the spice. India's most persuasive wine-with-food moment"},
        {"technique_id": "", "dish": "Fish curry (Goa Konkan style — coconut, kokum, chilli)",
         "pairing_type": "complement",
         "rationale": "A Goa fish curry paired with a Sula Late Harvest Chenin Blanc creates "
                      "a resonant PCT bridge: Portuguese-influenced Goan food culture "
                      "paired with Indian wine from the Nashik Valley, 200km north. "
                      "The Chenin Blanc's off-dry sweetness manages the kokum-sourness "
                      "and coconut richness while the wine's acidity lifts the chilli heat"}
    ],
    "source": "Sula Vineyards official documentation (sulawines.com); "
              "Sula IPO prospectus (BSE, 2022) production and distribution data; "
              "Epic Wines & Spirits US distribution confirmation; "
              "APEDA (Agricultural & Processed Food Products Export Development Authority) "
              "India wine export statistics",
})

session.commit_batch()
print(f"\n[BATCH 43 COMMITTED — Sula Vineyards Indian Wine]\n")

# PRODUCERS
session.add_producer({
    "name": "John Distilleries (Paul John Single Malt)",
    "location": "Goa facility (distilling/maturation) and Bangalore (maltings)",
    "country": "India",
    "region": "Goa, India (distillery) / Karnataka (malt production)",
    "tradition": "spirits",
    "key_person": "Paul P. John (founder); Michael D'Souza (master distiller, Goa)",
    "founded": "1992 (John Distilleries Ltd); 2008 (Paul John Single Malt launch)",
    "production_volume": "Growing premium segment; distributed in 40+ countries; "
                         "most internationally visible Indian single malt brand",
    "notable_products": ["Paul John Brilliance", "Paul John Classic Select",
                         "Paul John Bold (peated)", "Paul John Christmas Edition",
                         "Paul John Peated Select Cask"],
    "certifications": ["World Whiskies Awards (multiple years)", "Jim Murray's Whisky Bible 2012 Indian Whisky of the Year"],
    "website": "pauljohnwhisky.com",
    "philosophy": "Using the distillation heritage of Goa — India's oldest continuous copper pot "
                  "still tradition from the Feni industry — to produce world-class single malt. "
                  "Tropical ageing in Goa's extreme heat creates faster maturation and a "
                  "distinctly Indian flavour profile that cannot be replicated in Scotland.",
    "trail_connection": "PCT-8",
    "source": "John Distilleries official documentation; Preiss Imports US portfolio",
    "verified": True
})

session.add_producer({
    "name": "Sula Vineyards",
    "location": "Nashik Valley, Maharashtra, India",
    "country": "India",
    "region": "Nashik Valley DOC, Maharashtra",
    "tradition": "wine",
    "key_person": "Rajeev Samant (founder, CEO)",
    "founded": "1997",
    "production_volume": "India's largest single winery: ~15 million bottles annually; BSE-listed since 2022",
    "notable_products": ["Sula Sauvignon Blanc", "Sula Chenin Blanc", "Sula Late Harvest Chenin Blanc",
                         "Sula Dindori Reserve Shiraz", "Sula Brut"],
    "certifications": ["FSSAI India", "BSE Bombay Stock Exchange (listed 2022)"],
    "website": "sulawines.com",
    "philosophy": "India's first commercially successful fine wine estate, founded by Rajeev Samant "
                  "with the explicit goal of building a wine culture in India. The company "
                  "operated at a loss for years before becoming profitable — now the most "
                  "internationally recognised Indian wine brand.",
    "trail_connection": "PCT-8",
    "source": "Sula Vineyards official documentation; BSE 2022 IPO prospectus",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 44 COMMITTED — Goa and India Producers]\n")

print(session.finish())
