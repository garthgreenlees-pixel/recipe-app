#!/usr/bin/env python3
"""
Flor de Caña (Nicaragua rum),
Rhum Barbancourt (Haiti — fresh cane juice, Cognac method),
Dão white wine (Encruzado — Portugal's finest white wine variety)
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="Central America — Nicaragua (Flor de Caña)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=11,
    running_total=48
)

# ============================================================
# FLOR DE CAÑA — NICARAGUA — PCT EXTENSION
# ============================================================

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "nicaraguan rum slow aged column",
    "region": "Central America — Nicaragua (Chichigalpa, Chinandega)",
    "name": "Flor de Caña — Nicaragua Slow Aged, Carbon Neutral",
    "terroir_origin": (
        "Flor de Caña ('Flower of the Sugarcane') is produced at the Compañía Licorera "
        "de Nicaragua (CLN) in Chichigalpa, Chinandega — Nicaragua's Pacific coast "
        "agricultural lowland on the volcanic plain at the base of the San Cristóbal "
        "and Casita volcanoes. The region is one of Central America's most fertile "
        "agricultural zones: the volcanic soils (basalt and andisols from recent "
        "eruptions) and Pacific-influenced climate (distinct wet-dry seasons; "
        "hot, humid growing conditions) produce dense, high-yield sugarcane. "
        "The PCT connection: the same Portuguese-initiated Atlantic sugarcane chain "
        "(Madeira → Caribbean → mainland Central America) reaches Nicaragua through "
        "the Spanish colonial trade network. The Pellas family, who have operated "
        "CLN since 1937, built a vertically integrated sugarcane estate from "
        "field to bottle on the same volcanic Pacific plain. "
        "The volcano proximity: both San Cristóbal (Nicaragua's highest active volcano, "
        "1,745m) and Casita are within sight of the distillery. "
        "The volcanic terroir is the Central American equivalent of Martinique's "
        "Mont Pelée influence — an active volcanic environment shaping the agricultural "
        "raw material. "
        "Flor de Caña achieved: Carbon Neutral certification (2018), Fair Trade "
        "certification (2018) — the first rum to achieve both simultaneously. "
        "The Fair Trade certification is significant: it covers not just environmental "
        "practices but the social infrastructure for CLN's 1,400+ employees, "
        "including healthcare, education, and housing."
    ),
    "production_technique": (
        "Flor de Caña production: "
        "Sugarcane: estate-grown on the Chichigalpa estate; hand-harvested during "
        "the dry season (November–April); immediately crushed and clarified. "
        "Molasses: from CLN's own sugar mill — not purchased commodity molasses "
        "but directly produced from their own cane. This vertical integration "
        "controls the fermentation substrate from the field. "
        "Fermentation: 3–4 days in stainless steel; specific yeast strain maintained "
        "by CLN; the volcanic mineral character of the Pacific plain is argued to "
        "influence the fermentation environment (mineral-rich water from the volcano watershed). "
        "Distillation: multiple column stills; the final distillate is clean, "
        "lighter-bodied than pot-still Caribbean rum — the Central American style. "
        "Natural ageing: CLN ages exclusively in ex-American bourbon casks in "
        "the Nicaraguan warehouse without temperature control or artificial aging — "
        "the tropical heat and humidity work on the rum naturally. "
        "'Slow aged' marketing claim: CLN emphasises that no additives or "
        "artificial ageing acceleration is used — the same claim Richard Seale "
        "makes for Foursquare, but framed as a Central American sustainability narrative. "
        "12yr: 12 years minimum; the accessible premium benchmark. "
        "18yr: 18 years minimum; extraordinary by column still standards; "
        "one of the most complex light-rum expressions available. "
        "25yr: the prestige expression; limited allocation."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Diplomatico Reserva Exclusiva (Venezuela)",
         "connection": "Flor de Caña 18yr and Diplomatico Reserva Exclusiva represent the "
                       "two benchmark premium Central/South American column-still aged rums "
                       "at comparable price points. Both are lighter-bodied than Caribbean "
                       "pot-still expressions; both achieve richness through extended wood ageing "
                       "rather than post-production sugar addition (a key marketing distinction). "
                       "Flor de Caña's volcanic Pacific terroir vs. Diplomatico's Venezuelan "
                       "Andean foothills is the primary terroir contrast between the two"},
        {"tradition": "spirits", "beverage": "Flor de Caña alongside Angostura 1824 (comparative)",
         "connection": "The side-by-side of Flor de Caña 18yr (column-still, Central American) "
                       "and Angostura 1824 12yr (pot-column blend, Trinidad) demonstrates "
                       "the fundamental style division in aged rum: column-still elegance "
                       "and precision (Flor de Caña) vs. pot-still weight and funk (Angostura). "
                       "Both achieve comparable complexity through different means; "
                       "both represent regional terroir through their distillation tradition"}
    ],
    "sensory_profile": {
        "appearance": "Flor de Caña 12yr: medium amber, clear, golden highlights. "
                      "18yr: deeper amber, more red-orange tones from extended barrel time. "
                      "25yr: deep mahogany, very viscous.",
        "nose": "12yr: clean, precise, accessible — vanilla, caramel, dried peach, "
                "light tropical fruit (mango, papaya), gentle oak, "
                "the characteristic Nicaraguan column-still lightness. "
                "No heaviness, no molasses-rawness — the cleanest major rum style. "
                "18yr: much more complex — dark caramel, dried stone fruit, "
                "leather, tobacco, cinnamon, light coffee; "
                "the Pacific volcanic terroir adds a faint mineral dryness. "
                "25yr: extraordinary — dark chocolate, prune, espresso, "
                "warm wood, vanilla cream; the finest Flor de Caña expression.",
        "palate": "12yr (40% ABV): light-to-medium body; smooth, clean; "
                  "sweet caramel-vanilla forward; short-to-medium finish; "
                  "the easiest-drinking premium aged rum in the category. "
                  "18yr (40% ABV): medium-full body; dried fruit and oak persistence; "
                  "a subtle dryness on the finish from the volcanic-mineral water influence. "
                  "25yr (40% ABV): the most complete Flor de Caña expression; "
                  "long, complex finish; extraordinary by column-still standards.",
        "conclusion": "Flor de Caña 18yr is the column-still rum's best argument: "
                      "18 years in natural tropical ageing achieves a complexity "
                      "that respects the clean-elegant column-still tradition "
                      "while delivering genuine premium spirit depth. "
                      "The Carbon Neutral + Fair Trade credentials make it the "
                      "most sustainability-positioned premium rum in the category."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Flor de Caña 25yr / 20yr Reserve",
         "criteria": "25 years natural ageing; No Sugar Added certified; "
                     "single estate estate-vertically integrated production",
         "markers": "Flor de Caña 25yr; 20yr Reserve; BC ~$95–120; US ~$80–100"},
        {"tier": 3, "tier_name": "Flor de Caña 18yr",
         "criteria": "18 years minimum; complex extended ageing; "
                     "the benchmark expression; Carbon Neutral + Fair Trade",
         "markers": "Flor de Caña 18yr; BC ~$65–80; US ~$55–70"},
        {"tier": 2, "tier_name": "Flor de Caña 12yr",
         "criteria": "12 years; accessible premium; correct Nicaraguan character; "
                     "Carbon Neutral certified",
         "markers": "Flor de Caña 12yr; BC ~$40–50; US ~$30–40"},
        {"tier": 1, "tier_name": "Flor de Caña 7yr / 4yr",
         "criteria": "Younger age; entry to the brand character; cocktail grade",
         "markers": "Flor de Caña 7yr; 4yr Extra Seco; BC ~$25–35; US ~$18–25"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for 18yr and 25yr; over ice or in cocktails for 12yr",
        "vessel": "Glencairn or tulip for 18yr and 25yr neat; rocks glass for cocktails",
        "technique": "Flor de Caña 18yr neat: 45mL, room temperature — the clean column-still "
                     "character needs no water addition to open. "
                     "Nicaraguan Sour: Flor de Caña 12yr 60mL + lime 20mL + sugar 15mL + egg white. "
                     "Rum Old Fashioned: 18yr 60mL + 5mL agave syrup + Angostura + orange peel — "
                     "the 18yr's dried fruit and oak depth makes an unusually clean-elegant cocktail. "
                     "Sustainability narrative: the Carbon Neutral + Fair Trade combination "
                     "is the most compelling ethical story in the rum category.",
        "programme_position": "Sustainability-focused premium rum; comparative tasting with Caribbean rums; "
                              "cocktail programme base for tropical/rum menus",
        "verbal_presentation": "Flor de Caña 18 Years — Chichigalpa, Nicaragua. "
                               "Eighteen years in volcanic Pacific heat. "
                               "Carbon neutral, Fair Trade certified. "
                               "The rum at the base of the San Cristóbal volcano."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Compañía Licorera de Nicaragua (CLN) — Pellas Family",
        "producer_location": "Chichigalpa, Chinandega, Nicaragua (Pacific coast lowland)",
        "key_person": "Alfredo Pellas family (CLN ownership since 1937; "
                      "also control Grupo Pellas, Nicaragua's largest private company)",
        "production_volume": "Large commercial; distributed in 50+ countries; "
                             "one of Central America's largest beverage companies",
        "certifications": ["Carbon Neutral (2018 — first rum)", "Fair Trade (2018 — first rum)",
                           "No Sugar Added certified"],
        "bc_distributor": "BCLDB / Diageo Canada (Diageo distributes in Canada); "
                          "Flor de Caña 12yr and 18yr available at BC Liquor stores",
        "us_distributor": "DropCo Beverages (formerly Gemini Spirits) — US national; "
                          "widely available Total Wine, BevMo, premium spirits retailers",
        "uk_distributor": "Widely available UK: Master of Malt, The Whisky Exchange; "
                          "mainstream UK supermarket distribution",
        "price_tier": "Market to Reserve (12yr BC ~$45; 18yr BC ~$70; 25yr BC ~$105)",
        "availability_notes": "In BC: BC Liquor stores carry Flor de Caña 12yr and 18yr nationally. "
                              "US: DropCo national distribution; Total Wine carries 7yr through 18yr. "
                              "One of the most widely available premium aged rums in North America."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Nicaragua's rum industry follows the same Portuguese-Atlantic sugarcane trade "
                  "chain that underlies all Caribbean and Central American rum: "
                  "Madeira → Caribbean → mainland via Spanish colonial networks. "
                  "Flor de Caña's Carbon Neutral and Fair Trade certifications represent "
                  "the most significant corporate sustainability achievement in rum production — "
                  "a direct response to the category's historical associations with "
                  "the Atlantic plantation economy (WADT). "
                  "The Pellas family's vertical integration (field to bottle) on "
                  "the volcanic Pacific plain is the contemporary answer to the "
                  "plantation model that the PCT and WADT built.",
    "food_pairings": [
        {"technique_id": "", "dish": "Vigorón (Nicaraguan pork rinds with yuca and cabbage slaw)",
         "pairing_type": "complement",
         "rationale": "Nicaragua's most celebrated street food — crispy pork rinds (chicharrón), "
                      "boiled yuca, and pickled cabbage slaw — pairs with Flor de Caña 12yr "
                      "as the canonical Nicaraguan food-spirit combination. "
                      "The rum's caramel-vanilla sweetness complements the pork fat richness "
                      "while the lactic slaw acidity mirrors the rum's clean column-still finish"},
        {"technique_id": "", "dish": "Tres leches cake (Latin American cream-soaked sponge)",
         "pairing_type": "complement",
         "rationale": "Tres leches — sponge cake soaked in three milks (condensed, evaporated, cream) "
                      "— is the regional dessert most calibrated to Flor de Caña 18yr's "
                      "vanilla-caramel-dried stone fruit profile. "
                      "The rum's extended wood-ageing sweetness finds its exact "
                      "register in the condensed milk sweetness of the dessert"}
    ],
    "source": "Compañía Licorera de Nicaragua official production documentation; "
              "Carbon Neutral certification documentation (Bureau Veritas, 2018); "
              "Fair Trade certification documentation (Fair Trade USA, 2018); "
              "DropCo Beverages US distribution portfolio",
})

session.commit_batch()
print(f"\n[BATCH 49 COMMITTED — Flor de Caña Nicaragua]\n")

# ============================================================
# RHUM BARBANCOURT — HAITI — PCT×WADT
# ============================================================

session.switch_region("spirits", "Caribbean — Haiti (Rhum Barbancourt)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "haitian rhum agricole cognac method",
    "region": "Caribbean — Haiti (Port-au-Prince; sugarcane from Plaine du Cul-de-Sac)",
    "name": "Rhum Barbancourt — Haiti, Double-Distilled Sugarcane Juice, Cognac Method",
    "terroir_origin": (
        "Haiti occupies the western third of the island of Hispaniola — "
        "the first Caribbean island colonised by Columbus (1492) and, for a century and a half, "
        "the most economically significant colonial territory in the Western Hemisphere. "
        "The French colony of Saint-Domingue (Haiti) produced approximately 40% of "
        "Europe's sugar and 60% of its coffee by 1789 — making it the most profitable "
        "colonial territory on earth. This agricultural wealth was built entirely on "
        "enslaved West African labour: the WADT's most extreme example. "
        "The Haitian Revolution (1791–1804) — led by Toussaint Louverture, "
        "Jean-Jacques Dessalines, and Henri Christophe — was the only successful "
        "slave revolution in history and created the first Black republic. "
        "The sugarcane varieties that produced this colonial wealth arrived via the same "
        "Portuguese Atlantic chain that defines the PCT. "
        "Rhum Barbancourt: founded 1862 by Dupré Barbancourt, "
        "a French immigrant from the Charente — the same region that produces Cognac. "
        "Barbancourt brought the Cognac double-distillation method to Haiti, "
        "combined with the rhum agricole tradition (fresh sugarcane juice, not molasses). "
        "The result: a rum that is technically a hybrid of "
        "rhum agricole (Martinique) and Cognac (France) production philosophy, "
        "produced in the most historically charged rum territory in the Caribbean."
    ),
    "production_technique": (
        "Rhum Barbancourt production is a deliberate transplant of Cognac methodology "
        "to the Caribbean: "
        "Raw material: fresh sugarcane juice (vesou) from the Plaine du Cul-de-Sac, "
        "a flat agricultural plain east of Port-au-Prince. "
        "Fermentation: 72 hours using Barbancourt's own yeast strain; "
        "the tropical heat drives fast, complete fermentation. "
        "First distillation: low-wine distillation in copper column still to approximately "
        "50% ABV — similar to the first distillation ('première chauffe') in Cognac. "
        "Second distillation: pot still (alembic) to final spirit at 85–90% ABV — "
        "the 'bonne chauffe' in Cognac terminology. "
        "This double distillation using both column and pot still is unique in Caribbean rum "
        "and was brought directly from Charente by Dupré Barbancourt. "
        "Reduction: reduced to 45% ABV with demineralised water. "
        "Ageing: in Limousin French oak barrels (the same oak used for Cognac ageing). "
        "Reserve du Domaine: 15 years in Limousin oak; the prestige expression. "
        "Estate Reserve 8yr: 8 years; the standard premium expression. "
        "The Thierry Gardère family has managed Barbancourt since 1946 — "
        "the same family continuity through the Duvalier dictatorship, "
        "the 1994 UN sanctions, and the 2010 earthquake."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Armagnac (Bas-Armagnac, column + pot still)",
         "connection": "Rhum Barbancourt's double-distillation combining column and pot still "
                       "is structurally identical to Bas-Armagnac's single-distillation in the "
                       "Armagnac alembic (a continuous still that operates similarly to a "
                       "combined column + pot process). Both achieve complexity through "
                       "the preservation of secondary congeners from the raw material; "
                       "both age in French oak (Limousin for Barbancourt, Gascon oak for Armagnac). "
                       "Barbancourt Reserve du Domaine and a 15-year Armagnac "
                       "side by side demonstrates the Cognac winemaker's philosophy "
                       "applied to two different agricultural raw materials"},
        {"tradition": "spirits", "beverage": "Rhum Agricole AOC Martinique (Clément)",
         "connection": "Both Barbancourt and Martinique agricole use fresh sugarcane juice "
                       "rather than molasses. The difference: Martinique AOC uses column stills "
                       "exclusively; Barbancourt adds the pot-still second distillation "
                       "from the Cognac method. Martinique's AOC framework is rigorous and "
                       "French-controlled; Haiti has no equivalent appellation structure — "
                       "Barbancourt's quality depends entirely on the Gardère family's "
                       "maintained production standard rather than external regulation"}
    ],
    "sensory_profile": {
        "appearance": "Barbancourt Estate Reserve 8yr: bright amber-gold; clear; "
                      "medium legs from the 43% ABV. "
                      "Reserve du Domaine 15yr: deeper amber, more gold in the centre; "
                      "the Limousin oak shows in the colour.",
        "nose": "Estate Reserve 8yr: fresh cane juice character (the agricole base) "
                "combined with Cognac-wood complexity — vanilla, dried stone fruit, "
                "light floral, fresh tropical fruit (guava, mango), warm spice. "
                "The double distillation creates a cleaner, more refined character "
                "than single-distilled agricole; the Limousin oak adds a "
                "distinctly French register absent in American-oak-aged Caribbean rum. "
                "Reserve du Domaine 15yr: extraordinary depth — walnut, dried apricot, "
                "orange peel, espresso, vanilla cream, the subtle Haitian terroir "
                "of the Plaine du Cul-de-Sac minerality.",
        "palate": "8yr (43% ABV): medium body; balanced fresh cane / wood complexity; "
                  "the Limousin oak gives a different tannin character from American oak — "
                  "finer, less vanilla-dominant, more tannic. "
                  "15yr (43% ABV): full body; extraordinary complexity; "
                  "the French double-distillation method and the 15yr Limousin oak "
                  "create a spirit that crosses the sensory boundary between rum and Cognac. "
                  "The most historically layered rum: the Haitian Revolution "
                  "in a glass with a French winemaker's method.",
        "conclusion": "Rhum Barbancourt Reserve du Domaine is the most historically freighted "
                      "spirit in the PCT×WADT intersection. The Cognac method applied to "
                      "Haitian sugarcane on the plantation land of the "
                      "world's most significant slave revolution creates a beverage "
                      "with narrative weight that no other spirit in the world carries. "
                      "For a programme: serve alongside the history. "
                      "The rum stands alone; the story is extraordinary."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Barbancourt Reserve du Domaine (15yr)",
         "criteria": "15 years Limousin oak; double-distillation method; "
                     "Gardère family estate production; the pinnacle of Barbancourt",
         "markers": "Barbancourt Reserve du Domaine 15yr; BC ~$65–80; US ~$55–70"},
        {"tier": 3, "tier_name": "Barbancourt Estate Reserve 8yr",
         "criteria": "8 years Limousin French oak; double-distillation; "
                     "the accessible premium expression; Cognac-method quality",
         "markers": "Barbancourt Estate Reserve 8yr (the blue label); BC ~$35–45; US ~$28–38"},
        {"tier": 2, "tier_name": "Barbancourt 5 Stars Rum",
         "criteria": "5 years Limousin oak; the standard range; accessible; "
                     "correct Haitian agricole-Cognac character",
         "markers": "Barbancourt 5 Stars; BC ~$25–32; US ~$20–28"},
        {"tier": 1, "tier_name": "Barbancourt 3 Stars / White",
         "criteria": "Young rum; 3 stars designation; cocktail grade; "
                     "introduction to Barbancourt character",
         "markers": "Barbancourt 3 Stars; 2yr; BC ~$18–22; US ~$15–18"}
    ],
    "service_intelligence": {
        "temperature": "15yr: room temperature neat. 8yr: room temperature or single ice cube.",
        "vessel": "Cognac-style snifter or Glencairn for 15yr; rocks glass for 8yr cocktail use",
        "technique": "Reserve du Domaine 15yr: 45mL, room temperature, 5 minutes — "
                     "treat identically to a 15-year Armagnac. "
                     "Haitian Punch: 8yr 60mL + lime juice 20mL + cane sugar 15mL + "
                     "Angostura 2 dashes + nutmeg grated — the traditional Caribbean punch "
                     "with Haitian rhum and Grenadian nutmeg. "
                     "Side-by-side education: Barbancourt 8yr alongside Clément VSOP — "
                     "both fresh cane juice; column + pot vs. column only; "
                     "Limousin oak vs. American oak.",
        "programme_position": "Most historically significant rum in the programme narrative; "
                              "PCT×WADT intersection at its most concentrated; "
                              "premium spirits discovery experience",
        "verbal_presentation": "Barbancourt Reserve du Domaine — Port-au-Prince, Haiti. "
                               "Fifteen years in Limousin oak. Double-distilled like Cognac. "
                               "Dupré Barbancourt came from the Charente in 1862. "
                               "He brought the only method he knew "
                               "to the site of the only successful slave revolution in history."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Distillerie Rhum Barbancourt (Port-au-Prince, Haiti) — Thierry Gardère family",
        "producer_location": "Portail Léogâne, Port-au-Prince, Haiti (distillery); "
                             "Plaine du Cul-de-Sac (sugarcane cultivation)",
        "key_person": "Thierry Gardère (current managing director; family ownership since 1946)",
        "production_volume": "Haiti's only internationally distributed rum brand; "
                             "medium commercial scale; distributed in 30+ countries",
        "certifications": ["Rhum Barbancourt has no current AOC or GI but maintains "
                           "consistent family-quality standard since 1862"],
        "bc_distributor": "Barbancourt available at BC Liquor stores (BCLDB — confirmed); "
                          "5 Stars and Estate Reserve 8yr most consistently stocked",
        "us_distributor": "Heavenly Rum (national US distribution for Barbancourt — confirmed); "
                          "widely available at Total Wine, BevMo, specialty spirits retailers",
        "uk_distributor": "Widely available UK: The Whisky Exchange; Master of Malt; "
                          "Berry Bros. & Rudd (carries 15yr); specialist Caribbean rum merchants",
        "price_tier": "Market to Reserve (5 Stars US ~$22; Estate Reserve 8yr US ~$32; "
                      "Reserve du Domaine 15yr US ~$60)",
        "availability_notes": "In BC: BC Liquor stores carry 5 Stars and 8yr reliably. "
                              "15yr: BC Liquor select locations or special order. "
                              "US: Heavenly Rum national; Total Wine carries 5 Stars through 8yr; "
                              "15yr at specialty spirits retailers and online (Total Wine, ReserveBar). "
                              "UK: very accessible — The Whisky Exchange and Berry Bros. both carry all tiers."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Haiti is the PCT×WADT's most historically dense point of convergence: "
                  "the island where Columbus arrived in 1492 built the Atlantic colonial economy "
                  "using Portuguese-chain sugarcane; the wealth extracted through enslaved "
                  "West African labour (WADT) funded European empire for 300 years; "
                  "the Haitian Revolution (1791–1804) destroyed that economy and created "
                  "the first free Black republic. "
                  "Dupré Barbancourt arrived 58 years after the Revolution and built "
                  "a rum distillery on the same plantation-economy infrastructure using "
                  "a French technique — the post-colonial appropriation of colonial tools "
                  "for independent national production. "
                  "The Gardère family's 1946 continuity through the Duvalier years, "
                  "the 1994 sanctions, and the 2010 earthquake is the most resilient "
                  "production story in Caribbean rum.",
    "food_pairings": [
        {"technique_id": "", "dish": "Griot (Haitian slow-braised then fried pork shoulder)",
         "pairing_type": "complement",
         "rationale": "Griot — pork shoulder marinated in sour orange, herbs, and Scotch bonnet, "
                      "slow-braised then deep-fried to a crispy-tender result — "
                      "is Haiti's most celebrated national dish. "
                      "Barbancourt Estate Reserve 8yr alongside griot is the canonical "
                      "Haitian food-spirit pairing: the rum's fresh cane acidity cuts "
                      "the pork fat while the Limousin oak's tannin "
                      "manages the crispy-rendered texture"},
        {"technique_id": "", "dish": "Pain patate (Haitian sweet potato pudding cake)",
         "pairing_type": "complement",
         "rationale": "Pain patate — steamed sweet potato, coconut, cinnamon, rum, "
                      "banana pudding — is baked with Barbancourt in the recipe and served "
                      "alongside it as a digestif pairing. "
                      "The rum in the pudding and the rum in the glass is the "
                      "most direct example of spirit-and-food unity in the PCT: "
                      "the same bottle flavours both"}
    ],
    "source": "Distillerie Rhum Barbancourt official history and production documentation; "
              "Thierry Gardère interview archives; "
              "C.L.R. James 'The Black Jacobins' (Haitian Revolution history); "
              "Heavenly Rum US distribution confirmation; "
              "Dave Broom 'Rum' (Haiti section)",
})

session.commit_batch()
print(f"\n[BATCH 50 COMMITTED — Rhum Barbancourt Haiti]\n")

# ============================================================
# DÃO WHITE WINE — ENCRUZADO — PCT-1
# ============================================================

session.switch_region("wine", "Portugal — Dão DOC (White Wines)")

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "dao white wine encruzado",
    "region": "Portugal — Dão DOC (Beira Interior, granite highlands)",
    "name": "Dão White — Encruzado, Portugal's Most Distinctive White Wine Variety",
    "terroir_origin": (
        "The Dão region (central Portugal, Beira Interior) is better known internationally "
        "for red Touriga Nacional than for white wine, but Encruzado — the Dão's signature "
        "white variety — is increasingly recognised as one of the most distinctive "
        "white wine grapes in Europe. "
        "Encruzado means 'crossroads' in Portuguese — the vine is at the crossroads "
        "of the Dão's two defining characteristics: the granite-schist highland soils "
        "(500–800m altitude) and the extreme continental climate "
        "(cold winters, hot dry summers). "
        "The terroir: the Dão Valley is enclosed by mountain ranges on three sides "
        "(Serra da Estrela, Serra da Lapa, Serra do Caramulo) that block maritime influence "
        "from both the Atlantic and the Mediterranean. "
        "This creates one of the most extreme continental microclimates in Portugal: "
        "temperatures range from -5°C in winter to 40°C in summer; "
        "the granite and schist soils retain heat and drain well; "
        "the altitude moderates summer extremes to preserve acid in the grapes. "
        "Encruzado is only found in the Dão — it is a true place-variety, "
        "not transplanted elsewhere in commercial quantity. "
        "Benchmark producers: Quinta dos Roques (Toninha Mesquita, the 'queen of Dão white'); "
        "Alvaro Castro (Casa de Saima, the most internationally visible Dão producer); "
        "Rui Reguinga (independent winemaker consulting at multiple Dão estates)."
    ),
    "production_technique": (
        "Encruzado's extraordinary complexity comes from its natural chemistry: "
        "very high natural acidity; moderate sugar accumulation (controlled by the altitude); "
        "rich precursor compounds that develop into complex aromas through winemaking. "
        "Harvest: late September to mid-October (one of Portugal's latest white wine harvests); "
        "the extended ripening season on granite soils builds complexity without sacrificing acid. "
        "Traditional whole-cluster pressing (the standard for premium Encruzado): "
        "maintains freshness and avoids extracting bitter grape skin phenolics. "
        "Fermentation: skin contact (maceration pelliculaire) practiced by some producers "
        "for 8–24 hours pre-fermentation — the granite terroir's phenolic character "
        "is extracted without over-extraction in the brief contact. "
        "Oak fermentation and ageing: premium Encruzado is fermented and aged in "
        "French oak barrels (225L, mostly 2nd and 3rd fill to minimise new-oak dominance); "
        "lees stirring (bâtonnage) for 6–12 months adds creaminess and texture. "
        "The result: a white wine with the complexity of a grand cru white Burgundy, "
        "the mineral freshness of Chablis, and an aromatic profile entirely its own. "
        "Quinta dos Roques Encruzado: consistently rated among Portugal's finest white wines; "
        "US importer Golden Ram Imports (confirmed from previous research)."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "White Burgundy Grand Cru (Meursault, Puligny-Montrachet)",
         "connection": "Encruzado is Portugal's answer to Meursault: both are the defining "
                       "white wine variety of a red wine-dominated region; both achieve "
                       "the counterintuitive result of white wine supremacy in a "
                       "landscape planted primarily to red varieties. "
                       "Encruzado's granite-schist mineral precision compares to Meursault's "
                       "Kimmeridgian chalk precision; both wines develop extraordinary complexity "
                       "through lees ageing; both are best at 5–10 years. "
                       "Encruzado is currently priced at 30–40% of equivalent quality Meursault "
                       "— this gap will likely close as the variety gains international recognition"},
        {"tradition": "wine", "beverage": "Grüner Veltliner Smaragd (Wachau, Austria)",
         "connection": "Both Encruzado and Grüner Veltliner Smaragd are continental-climate "
                       "white wines with electric acidity, distinctive mineral identities, "
                       "and medium-to-full body from the warm, dry growing seasons. "
                       "Both age beautifully: 10+ years in each case produces wines of "
                       "extraordinary complexity. Both are found almost exclusively in their "
                       "home region; both are the 'insider secret' of their respective "
                       "national wine cultures"}
    ],
    "sensory_profile": {
        "appearance": "Pale gold to medium gold; greenish rim in youth; "
                      "bright and clear with slow legs from medium alcohol (13–13.5%); "
                      "aged examples develop a deeper gold with a honey tint",
        "nose": "Young Encruzado (1–3 years): white peach, nectarine, citrus zest, "
                "white flower (jasmine, acacia), fresh almond, "
                "the distinctive granite mineral note — a dry, crushed-stone precision "
                "on the back of the nose absent from any limestone or chalk terroir. "
                "Oak-aged: additional creaminess, light toast, vanilla undertone; "
                "the oak should integrate completely — the fruit and mineral are primary. "
                "Aged (5–8 years): white truffle, roasted nuts, dried apricot, "
                "honeycomb, complex mineral evolution — the most complex expression.",
        "palate": "Full body (unusual for a white wine of this acidity level — "
                  "the granite soil and lees ageing create texture); "
                  "electric acidity drives linear freshness; "
                  "long, mineral finish; the oak-aged expressions develop a "
                  "Meursault-like creaminess that bridges the body and the acid. "
                  "Quinta dos Roques Encruzado at 8 years: one of Portugal's "
                  "greatest white wine moments.",
        "conclusion": "Encruzado is Portugal's most undervalued white grape variety. "
                      "For a programme: serve alongside Meursault at the same price point "
                      "and let the comparison make the case. "
                      "The PCT narrative: the granite-schist terroir of the Dão "
                      "has produced this variety for centuries; "
                      "the world outside Portugal is only just discovering it."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Quinta dos Roques Encruzado Reserve / Alvaro Castro Claro",
         "criteria": "Named single vineyard; 100% Encruzado; French oak fermented and aged 12+ months; "
                     "minimum 5 years for peak expression",
         "markers": "Quinta dos Roques Encruzado Reserve; Alvaro Castro Claro; "
                    "Caves São João Encruzado; BC ~$35–50; US ~$28–40"},
        {"tier": 3, "tier_name": "Quinta dos Roques Encruzado Standard / Dão DOC White",
         "criteria": "Dão DOC white; 100% or majority Encruzado; "
                     "partial barrel fermentation or full stainless",
         "markers": "Quinta dos Roques Encruzado; Sogrape Dão White; BC ~$22–35; US ~$18–28"},
        {"tier": 2, "tier_name": "Dão DOC White Blend",
         "criteria": "Dão DOC; Encruzado-dominant blend with Bical, Malvasia Fina; "
                     "correct granite mineral character",
         "markers": "Standard Dão white blends; Duque de Viseu Branco; BC ~$14–22; US ~$12–18"},
        {"tier": 1, "tier_name": "Beiras IGP White",
         "criteria": "Regional white; Encruzado component; accessible entry",
         "markers": "Beiras IGP; commercial Portuguese white blends; BC ~$10–14; US ~$8–12"}
    ],
    "service_intelligence": {
        "temperature": "10–12°C (young); 12–14°C (5+ year aged) — barrel-aged "
                       "Encruzado benefits from slightly warmer serving to open the texture",
        "vessel": "White Burgundy glass (the wider bowl opens the creaminess and mineral); "
                  "standard white glass for unoaked versions",
        "technique": "Oak-aged Encruzado: open 15 minutes before service; "
                     "the Meursault-style creaminess opens slowly. "
                     "Aged Encruzado (5+ years): decant briefly (15 minutes) — "
                     "it is one of the few white wines that benefits from brief decanting. "
                     "Comparative: Encruzado alongside Meursault Village and Grüner Veltliner "
                     "Smaragd for a European continental white wine flight.",
        "programme_position": "Premium white wine discovery experience; "
                              "Portuguese white wine anchor for PCT programme; "
                              "Meursault comparison centrepiece for wine education",
        "verbal_presentation": "Quinta dos Roques Encruzado — Dão Valley, Portugal. "
                               "The 'crossroads' variety. Granite and schist at 600 metres. "
                               "Portugal's answer to Meursault. The white wine the region "
                               "kept for itself until the 1990s."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Quinta dos Roques (Toninha Mesquita, Dão — the reference Encruzado producer)",
        "producer_location": "Abrunhosa do Ladário, Mangualde, Dão DOC, Portugal",
        "key_person": "Toninha Mesquita (owner and winemaker; known internationally as 'the queen of Dão white'); "
                      "Alvaro Castro (Quinta da Pellada; the other key Dão white reference)",
        "production_volume": "Small family estate; Quinta dos Roques: medium production for the region; "
                             "international distribution via Golden Ram Imports (US)",
        "certifications": ["Dão DOC"],
        "bc_distributor": "Quinta dos Roques: no confirmed dedicated BC distributor; "
                          "Liberty Wine Merchants and Marquis Wine Cellars (Vancouver) "
                          "carry on occasion; BCLDB special order available; "
                          "Sogrape Dão whites more reliably available through regular BCLDB listings",
        "us_distributor": "Quinta dos Roques: Golden Ram Imports (national US — confirmed from "
                          "earlier research); "
                          "Alvaro Castro: Skurnik Wines & Spirits (national — confirmed)",
        "uk_distributor": "Quinta dos Roques: Yapp Brothers (Wiltshire — specialist Portuguese); "
                          "Armit Wines (London); Wines of Portugal (UK)",
        "price_tier": "Market to Reserve (Quinta dos Roques standard US ~$22; Reserve US ~$35–45; "
                      "Alvaro Castro Claro US ~$35–50)",
        "availability_notes": "In BC: Sogrape Dão wines available at BC Liquor; "
                              "Quinta dos Roques available through Liberty Wine or private import. "
                              "US: Golden Ram Imports for Quinta dos Roques nationally; "
                              "Skurnik for Alvaro Castro nationally. "
                              "UK: Yapp Brothers is the most established UK Dão source."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Dão region sits at the geographical centre of Portugal, "
                  "at the crossroads of the Roman road network that connected Lisbon "
                  "to the northern ports. The granite-enclosed valley's isolation "
                  "preserved both indigenous varieties (Encruzado, Touriga Nacional, Jaen) "
                  "and traditional winemaking practices longer than any other Portuguese region. "
                  "The 1989 reversal of the cooperativa monopoly (until that date, "
                  "all Dão wine was required to pass through cooperatives, destroying quality) "
                  "allowed estates like Quinta dos Roques to bottle their own production — "
                  "the modern Dão quality revolution is just 35 years old.",
    "food_pairings": [
        {"technique_id": "", "dish": "Chanterelle mushroom and Dão olive oil bruschetta",
         "pairing_type": "complement",
         "rationale": "The aged Encruzado's white truffle and toasted almond character "
                      "bridges directly with chanterelle mushrooms' own earthy-nutty-floral "
                      "aromatic. The granite mineral in the wine and the woodland floor "
                      "character of the mushroom create a feedback loop. "
                      "Dão olive oil on the bruschetta adds the regional identity — "
                      "the same valley's produce on the same palate"},
        {"technique_id": "", "dish": "Bacalhau com natas (salt cod with cream sauce and potato gratin)",
         "pairing_type": "bridge",
         "rationale": "Bacalhau com natas — salt cod baked with cream sauce, "
                      "caramelised onions, and potato — is the richest Portuguese bacalhau preparation. "
                      "The oak-aged Encruzado's full body and acid structure manages the cream richness "
                      "while the granite mineral character bridges with the salt cod's cured-sea depth. "
                      "Portugal's finest white wine meets its most beloved national ingredient"}
    ],
    "source": "CVR Dão (Comissão Vitivinícola da Região Dão) DOC regulations; "
              "Quinta dos Roques official estate documentation; "
              "Golden Ram Imports US portfolio; "
              "Wines of Portugal Dão regional guide; "
              "Jancis Robinson 'Wine Grapes' (Encruzado entry)",
})

session.commit_batch()
print(f"\n[BATCH 51 COMMITTED — Dão White Encruzado]\n")

# PRODUCERS
session.add_producer({
    "name": "Compañía Licorera de Nicaragua (CLN) — Flor de Caña",
    "location": "Chichigalpa, Chinandega, Nicaragua",
    "country": "Nicaragua",
    "region": "Pacific coast lowland, Nicaragua",
    "tradition": "spirits",
    "key_person": "Alfredo Pellas Jr. (Grupo Pellas; family ownership since 1937)",
    "founded": "1890 (CLN estate); Flor de Caña brand since 1937",
    "production_volume": "Large commercial; distributed in 50+ countries; "
                         "Carbon Neutral + Fair Trade certified since 2018",
    "notable_products": ["Flor de Caña 12yr", "Flor de Caña 18yr",
                         "Flor de Caña 25yr", "Flor de Caña 7yr Extra Seco"],
    "certifications": ["Carbon Neutral (Bureau Veritas, 2018)", "Fair Trade (Fair Trade USA, 2018)",
                       "No Sugar Added certified"],
    "website": "flordecana.com",
    "philosophy": "Vertical integration from field to bottle on the volcanic Pacific plain: "
                  "own sugarcane estate, own sugar mill, own distillery, own ageing warehouse. "
                  "Natural slow ageing without temperature control or additives. "
                  "The Carbon Neutral + Fair Trade dual certification is the most significant "
                  "sustainability achievement in the rum category.",
    "trail_connection": "PCT×WADT",
    "source": "CLN official documentation; Carbon Neutral and Fair Trade certification records; "
              "DropCo Beverages US distribution portfolio",
    "verified": True
})

session.add_producer({
    "name": "Distillerie Rhum Barbancourt",
    "location": "Portail Léogâne, Port-au-Prince, Haiti",
    "country": "Haiti",
    "region": "Port-au-Prince / Plaine du Cul-de-Sac, Haiti",
    "tradition": "spirits",
    "key_person": "Thierry Gardère (managing director; Gardère family ownership since 1946)",
    "founded": "1862 (Dupré Barbancourt, immigrant from the Charente, France)",
    "production_volume": "Haiti's only internationally distributed rum brand; medium commercial scale",
    "notable_products": ["Barbancourt Reserve du Domaine 15yr",
                         "Barbancourt Estate Reserve 8yr",
                         "Barbancourt 5 Stars", "Barbancourt 3 Stars"],
    "certifications": ["Haitian Rum Producers Association member"],
    "website": "rhumbarbancourtinc.com",
    "philosophy": "The only Caribbean rum distillery using the Cognac double-distillation method "
                  "(column + pot still in sequence) with fresh sugarcane juice and Limousin "
                  "French oak barrels. Dupré Barbancourt's 1862 founding decision to bring "
                  "the Charente method to Haiti has been maintained without interruption "
                  "through 163 years of ownership changes, dictatorship, sanctions, and earthquake.",
    "trail_connection": "PCT×WADT",
    "source": "Distillerie Rhum Barbancourt official history; Heavenly Rum US distribution confirmation",
    "verified": True
})

session.add_producer({
    "name": "Quinta dos Roques",
    "location": "Abrunhosa do Ladário, Mangualde, Dão DOC, Portugal",
    "country": "Portugal",
    "region": "Dão DOC, Beira Interior, Portugal",
    "tradition": "wine",
    "key_person": "Toninha Mesquita (owner and winemaker; known internationally as the reference "
                  "Encruzado producer, 'the queen of Dão white')",
    "founded": "1989 (estate bottling commenced; family ownership longer)",
    "production_volume": "Small family estate; primarily exported via Golden Ram Imports (US)",
    "notable_products": ["Quinta dos Roques Encruzado", "Quinta dos Roques Reserve Encruzado",
                         "Quinta dos Roques Touriga Nacional"],
    "certifications": ["Dão DOC"],
    "website": "quintadosroques.pt",
    "philosophy": "The reference producer for Encruzado — Portugal's most distinctive native "
                  "white wine variety. Toninha Mesquita's commitment to native Dão varieties "
                  "at the expense of international varieties has defined the modern Dão "
                  "white wine conversation.",
    "trail_connection": "PCT-1",
    "source": "Quinta dos Roques official documentation; Golden Ram Imports US portfolio",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 52 COMMITTED — Nicaragua, Haiti, Dão Producers]\n")

print(session.finish())
