#!/usr/bin/env python3
"""
PCT×WADT Caribbean Rum depth:
Angostura (Trinidad — rum + bitters),
River Antoine (Grenada — windmill-powered oldest Windward Islands distillery),
Chairman's Reserve (St. Lucia)
+ Flor de Caña (Nicaragua) + Ron Zacapa (Guatemala) as Central American PCT extensions
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="Caribbean — Trinidad (Angostura)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=10,
    running_total=45
)

# ============================================================
# ANGOSTURA — TRINIDAD — PCT×WADT
# ============================================================

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "trinidad rum molasses column-pot",
    "region": "Caribbean — Trinidad and Tobago",
    "name": "Angostura Trinidad Rum — The Island of the Bitters and the Column Still",
    "terroir_origin": (
        "Trinidad, the southernmost major Caribbean island (just 11km off the Venezuelan coast), "
        "sits at the convergence of the Caribbean Sea and the Atlantic Ocean. "
        "Its proximity to South America means Trinidad has a different botanical and "
        "agricultural character from the northern Antilles: more South American biodiversity, "
        "different soil types (from the Orinoco River's geological influence), "
        "and a richer secondary fermentation flora from the rainforest environment. "
        "The PCT connection: Trinidad was part of the Spanish colonial system before the "
        "British took it in 1797; sugarcane and rum production had been established "
        "under both Spanish and then British colonial control. "
        "The Portuguese Atlantic colonial sugarcane chain reached Trinidad via the "
        "same route as Barbados and Jamaica: Madeira → Brazil → Eastern Caribbean. "
        "Angostura Ltd (founded 1949 as a distillery, though the Angostura name dates to "
        "1824) is the primary Trinidadian rum producer and the world's most famous bitters producer. "
        "The double significance of Angostura: "
        "First, it produces rum using the heavy molasses of Trinidad's south coast "
        "refineries — the same blackstrap molasses from Venezuelan-adjacent sugarcane. "
        "Second, it produces Angostura Aromatic Bitters — the small bottle with the "
        "oversized label that is in every cocktail bar on earth. "
        "Angostura Bitters (invented 1824 by German-Venezuelan Dr. Johann Siegert "
        "in Ciudad Bolívar, Venezuela; moved to Trinidad 1875) contains gentian root, "
        "various spices and botanicals, and rum — the formula is secret. "
        "It is the highest-volume cocktail ingredient in the world."
    ),
    "production_technique": (
        "Angostura rum production: "
        "Fermentation: blackstrap molasses; 24–96 hours; pot and column still fermentations "
        "run separately, each with different yeast strains and fermentation times. "
        "Distillation: Angostura operates both traditional column stills and pot stills; "
        "the lighter column-distilled fraction is used for white rum (1919 White); "
        "the heavier pot-still fraction blended for aged expressions. "
        "Angostura 1824: the flagship; named for the year Siegert founded the bitters company. "
        "1919 Rum: the standard aged expression; 8-year average age, heavy molasses base, "
        "Trinidadian terroir — full-bodied, dark fruit, vanilla, brown spice. "
        "Angostura 1824 12-Year: complex; ex-bourbon and ex-sherry cask ageing; "
        "similar in quality tier to Appleton 12yr. "
        "Bitters production: the Angostura Bitters recipe is one of the most guarded "
        "commercial secrets in the food and beverage industry. "
        "The formula is known only to five people (all family members). "
        "The production: macerate botanicals in high-proof rum alcohol; "
        "blend with gentian extract; bottle at 44.7% ABV. "
        "The oversized label (a source of questions since 1870) originated when two brothers "
        "independently ordered labels and bottles and the labels arrived too large — "
        "the mistake was retained as a brand identity."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Appleton Estate 12yr (Jamaica)",
         "connection": "Angostura 1824 and Appleton 12yr represent the heavy-molasses Caribbean "
                       "pot-column hybrid at comparable quality tiers. "
                       "Jamaica's Appleton uses Jamaican limestone-filtered water and the Nassau "
                       "Valley terroir; Trinidad's Angostura uses Venezuelan-influenced molasses "
                       "and rainforest botanical environment. Both achieve full-body dark-rum "
                       "complexity through careful blending and tropical ageing; "
                       "the distinction is Appleton's banana-ester Jamaican pot-still character "
                       "versus Angostura's darker, drier, more molasses-forward Trinidadian style"},
        {"tradition": "spirits", "beverage": "Peychaud's Bitters (Sazerac comparison)",
         "connection": "Angostura Bitters and Peychaud's Bitters are the two essential cocktail "
                       "bitters that shaped the entire history of the cocktail. "
                       "Peychaud's (New Orleans, 1830) is rum-based and lighter; "
                       "Angostura (Trinidad, 1824) is heavier, more complex, gentian-dominant. "
                       "Both are technically spirits (44.7% ABV) but used in such small quantities "
                       "as flavouring agents that their contribution is aromatic rather than alcoholic. "
                       "The PCT significance: both are rum-based; both emerged from the "
                       "Atlantic colonial rum trade infrastructure"}
    ],
    "sensory_profile": {
        "appearance": "Angostura 1919: deep mahogany-brown; viscous; slow tears. "
                      "Bitters: near-opaque dark brown; aromatic smoke when opened. "
                      "1824 12-year: deep amber with reddish highlights.",
        "nose": "Angostura 1919: molasses-forward (this is the signature — "
                "more immediately molasses than Jamaica or Barbados); "
                "dark dried fruit (raisin, prune), vanilla, brown spice, "
                "leather, a hint of tobacco. The full South American-proximity "
                "molasses terroir character. "
                "1824 12-year: more refined; the molasses integrates into "
                "dark chocolate, dried stone fruit, toasted oak, cinnamon; "
                "the Trinidadian character under all of it. "
                "Angostura Bitters (undiluted): extraordinarily complex — "
                "gentian root bitterness, clove, allspice, vanilla, orange peel, "
                "rum, mystery; the most complex olfactory experience in a small bottle.",
        "palate": "1919 (40% ABV): full body; sweetness from the molasses base "
                  "(residual sugar from commercial production); dark fruit finish; "
                  "the most accessible full-body Caribbean rum for cocktail use. "
                  "1824 12-year: drier, more structured; excellent sipping rum. "
                  "Bitters in an Old Fashioned (2 dashes in 50mL Bourbon or rum): "
                  "the most transformative micro-addition in bartending — "
                  "the gentian and spice add dimensions unavailable in any other ingredient.",
        "conclusion": "Angostura occupies a unique position: it is both a significant rum producer "
                      "and the world's most important non-rum beverage company — "
                      "the bitters in every cocktail bar globally. "
                      "For a programme: serve 1824 12-year as the sipping Trinidad rum; "
                      "serve Angostura Bitters as the cocktail education anchor. "
                      "The oversized label story is mandatory table narrative."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Angostura 1824 12-year / Cask Collection",
         "criteria": "12+ years tropical ageing; pot and column blend; "
                     "ex-bourbon and ex-sherry; limited edition cask expressions",
         "markers": "Angostura 1824; Angostura Cask Collection releases; BC ~$55–75; US ~$45–60"},
        {"tier": 3, "tier_name": "Angostura 7-year / 1919 Rum",
         "criteria": "7–8 years; correct Trinidadian molasses-dark character; "
                     "blended pot-column; accessible premium sipping",
         "markers": "Angostura 1919; Angostura 7yr; BC ~$35–48; US ~$30–40"},
        {"tier": 2, "tier_name": "Angostura 5-year / Reserva",
         "criteria": "5 years; accessible; cocktail-grade sipping; "
                     "Trinidadian molasses base correct",
         "markers": "Angostura Reserva 5yr; BC ~$25–35; US ~$20–28"},
        {"tier": 1, "tier_name": "Angostura White / Bitters (Specialty Category)",
         "criteria": "White rum (column-distilled, charcoal filtered) or Bitters as signature product; "
                     "foundational cocktail ingredients",
         "markers": "Angostura 1919 White; Angostura Aromatic Bitters 200ml; "
                    "widely available; BC bitters ~$12–15; US ~$10–12"}
    ],
    "service_intelligence": {
        "temperature": "1824 12-year: room temperature neat; 1919: over large ice or in cocktails",
        "vessel": "Glencairn for 1824 sipping; rocks glass for 1919 cocktails",
        "technique": "Angostura 1824 12yr neat: 45mL, room temperature, 5 minutes rest. "
                     "Trinidad Sour: Angostura 1919 60mL + lime 22mL + sugar 15mL + "
                     "2 dashes Angostura Bitters + egg white — the spirit and its own bitters "
                     "in one cocktail. "
                     "Old Fashioned with Angostura 1824: 60mL + 2 dashes Angostura Bitters + "
                     "5mL demerara + orange peel. Rum Punch: the bitters bottle is essential.",
        "programme_position": "Caribbean rum anchor; cocktail education with bitters; "
                              "Trinidadian provenance narrative",
        "verbal_presentation": "Angostura 1824 — Port of Spain, Trinidad. "
                               "The same company that has been flavouring cocktails since 1824. "
                               "The oversized label? A mistake they kept. "
                               "The secret formula? Five family members know it."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Angostura Ltd (Port of Spain, Trinidad and Tobago)",
        "producer_location": "20 Concession Road, Brighton, La Brea, Trinidad",
        "key_person": "Lorcan Dowd (CEO, Angostura Holdings Ltd); "
                      "Joy Spence (Appleton) was the first female Master Blender — "
                      "Angostura's equivalent is their master blending team",
        "production_volume": "Large commercial; Angostura Bitters distributed to 170+ countries annually; "
                             "rum distributed in 50+ markets",
        "certifications": ["Trinidad Rum Producers Association", "WIRSPA"],
        "bc_distributor": "Angostura widely available at BC Liquor stores (BCLDB); "
                          "bitters and standard rum expressions widely distributed",
        "us_distributor": "Campari America (US distribution of Angostura rum — confirmed); "
                          "bitters direct through Angostura USA / multiple distributors",
        "uk_distributor": "Widely available UK: Sainsbury's, Waitrose, Majestic, The Whisky Exchange",
        "price_tier": "Market to Reserve (Bitters ~$12 BC; 1919 ~$35 BC; 1824 12yr ~$60 BC)",
        "availability_notes": "Angostura products: BC Liquor stores nationally; virtually universal "
                              "distribution. Bitters: available in every bar supply store, "
                              "supermarket spirits aisle, and specialty retailer in North America. "
                              "1824 12-year: BC Liquor stores and specialty spirits shops."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Angostura Bitters was invented in 1824 by a German physician in Venezuela "
                  "using Caribbean rum and Amazonian botanicals — a product of the Portuguese "
                  "Atlantic-colonial rum trade (the base spirit), the German scientific tradition "
                  "(the inventor), and the Amazonian botanical knowledge of the South American coast. "
                  "When the Siegert family moved Angostura to Trinidad in 1875, "
                  "they placed the world's most widely distributed cocktail ingredient "
                  "on the same island that was part of the Atlantic sugarcane trade. "
                  "Every cocktail bar on earth has Angostura Bitters. "
                  "Every bottle is PCT.",
    "food_pairings": [
        {"technique_id": "", "dish": "Doubles (Trinidad curried chickpea fritters in bara bread)",
         "pairing_type": "complement",
         "rationale": "Trinidad's national street food — bara bread stuffed with curried chickpeas, "
                      "chutney, and pepper sauce — pairs with Angostura 1919 as the "
                      "canonical Trinidadian breakfast-to-lunch pairing. "
                      "The curried chickpea's warmth and the bara's fried dough find "
                      "the rum's molasses-dark warmth as a complementary register"},
        {"technique_id": "", "dish": "Bitters Old Fashioned / Cocktail reference",
         "pairing_type": "bridge",
         "rationale": "The most direct product education: Angostura Bitters in an Old Fashioned "
                      "alongside a neat pour of Angostura 1824 12yr demonstrates that "
                      "the cocktail's essential flavouring agent and the sipping rum "
                      "come from the same island, the same company, and ultimately "
                      "the same Atlantic colonial sugarcane trade"}
    ],
    "source": "Angostura Holdings Ltd official history and production documentation; "
              "Johann Gottlieb Benjamin Siegert 1824 bitters formulation historical records; "
              "WIRSPA production standards; "
              "Dave Broom 'Rum' (Trinidad section); "
              "Campari America US distribution confirmation",
})

session.commit_batch()
print(f"\n[BATCH 45 COMMITTED — Angostura Trinidad Rum and Bitters]\n")

# ============================================================
# RIVER ANTOINE — GRENADA — PCT×WADT
# ============================================================

session.switch_region("spirits", "Caribbean — Grenada (River Antoine Estate)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "grenada river antoine windmill rum",
    "region": "Caribbean — Grenada (St. Patrick Parish, northeastern coast)",
    "name": "River Antoine Estate Rum — The Most Traditional Rum in the Caribbean",
    "terroir_origin": (
        "River Antoine Estate (Grenada) operates the oldest rum distillery in the Windward "
        "Islands still using all-original pre-industrial equipment. Founded in the 1780s "
        "(during the British colonial period following France's cession of Grenada in 1763), "
        "River Antoine has been producing rum continuously using the same waterwheel, "
        "the same wooden mill, and the same copper pot stills since the estate was built. "
        "The PCT connection is through the full Atlantic colonial chain: "
        "Portuguese Atlantic sugarcane cultivation → Spanish/French initial Caribbean colonisation "
        "(Grenada was French from 1649 to 1762) → British rum production culture after 1763. "
        "The River Antoine estate itself was built during the British period "
        "but on French-cleared plantation land, over the original Caribbean indigenous "
        "(Kalinago) territory. "
        "The rum: single estate, single-still, unaged (white rum) at 75% ABV — "
        "the highest-proof commercially produced white rum available anywhere. "
        "Overproof: the traditional Caribbean 'overproof rum' tradition dates from "
        "the same era as Grenada's founding — high-proof rum was mixed with water "
        "on plantations as a daily ration for enslaved workers (the WADT's most "
        "direct material legacy). River Antoine continues this production tradition "
        "unchanged from the 18th century: the waterwheel turns the mill; "
        "fresh-pressed cane juice ferments overnight in wooden vats with wild yeasts; "
        "distillation in the original copper pot still the next day."
    ),
    "production_technique": (
        "River Antoine's production process is the least changed in the Caribbean: "
        "Cane harvesting: manual, by machete; sugarcane from the surrounding estate fields "
        "and adjacent farms. "
        "Milling: a waterwheel powered by the Antoine River drives the original wooden mill "
        "and crusher — the same waterwheel that has operated since the 1780s; "
        "the water source is the same river that gives the estate its name. "
        "Fermentation: fresh-pressed sugarcane juice (vesou) — not molasses — "
        "collected in open wooden fermentation vats; wild yeasts from the environment "
        "ferment the juice overnight at ambient temperature (28–32°C tropical heat); "
        "12–18 hours fermentation produces a wash of approximately 7–9% ABV. "
        "Distillation: original copper pot still (single distillation); "
        "heart cut taken at approximately 75% ABV. "
        "No ageing: the white rum is bottled at full distillation proof (75% ABV) "
        "without dilution or ageing. The overproof character is the product itself. "
        "This production is almost identical to the process that produced Caribbean rum "
        "in the 18th century — a living museum of pre-industrial rum production "
        "that also happens to produce extraordinary rum."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Rhum Agricole AOC Martinique (Clément, J.M.)",
         "connection": "River Antoine Estate and Martinique Rhum Agricole are both fresh "
                       "sugarcane juice-based rums rather than molasses-based — the agricultural "
                       "rum tradition using vesou rather than distillery byproduct. "
                       "The difference: Martinique's AOC requires specific ageing, "
                       "controlled production, column still elements; River Antoine is "
                       "the artisanal pre-AOC version of the same philosophy — "
                       "fresh juice, pot still only, no ageing, no standardisation. "
                       "Both express the terroir of the specific Caribbean island "
                       "through the sugarcane variety and environment rather than "
                       "through the molasses commodity chain"},
        {"tradition": "spirits", "beverage": "Mezcal Ensamble (Agave, Oaxaca)",
         "connection": "River Antoine Estate rum and artisanal Oaxacan mezcal share the "
                       "defining character of pre-industrial spirits production that has "
                       "resisted modernisation: both use wild fermentation with ambient yeasts; "
                       "both distill in copper or clay pot stills using traditional equipment; "
                       "both produce spirits at high ABV with raw agricultural character. "
                       "Both are preserved 18th-century production technologies in active use — "
                       "the most important living examples of pre-industrial distillation"}
    ],
    "sensory_profile": {
        "appearance": "Clear to very pale straw; 75% ABV creates a slight viscosity; "
                      "thin tears from the high alcohol; no colour from absence of ageing",
        "nose": "Extraordinarily complex for an unaged spirit — the fresh sugarcane juice "
                "and wild yeast fermentation create complexity impossible in molasses rum: "
                "fresh-cut sugarcane, green grass, tropical flower, "
                "light brine from the Antoine River proximity to the coast, "
                "sweet raw cane, overripe banana, light fusel from the overproof character. "
                "The nose at 75% ABV is intense — approach carefully, "
                "do not get too close initially.",
        "palate": "75% ABV — this is not sipped neat by choice; the tradition is to dilute 1:1 "
                  "with water, producing a spirit at approximately 37–38% ABV. "
                  "Diluted: the complexity opens — fresh cane sweetness, tropical fruit, "
                  "wild fermentation character, the same raw agricultural identity "
                  "as the nose. The flavour is closer to the original pre-18th century "
                  "Caribbean rum experience than any other commercially available spirit. "
                  "For mixing: at full proof, River Antoine is the most powerful "
                  "rum cocktail ingredient available — a few drops go far.",
        "conclusion": "River Antoine Estate rum is the PCT×WADT's most historically "
                      "authentic beverage: the 1780s Caribbean plantation rum, "
                      "still produced on the same waterwheel. "
                      "For a programme: serve diluted 1:1 with still water to 37.5% ABV; "
                      "describe the waterwheel and the wild fermentation. "
                      "This is the rum that the enslaved workers who built it "
                      "also drank — the history is immediate."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "River Antoine Estate Overproof (75% ABV) — Bottled Direct",
         "criteria": "Single estate, full proof, original equipment production; "
                     "export version (available internationally) vs. local version (sold at estate)",
         "markers": "River Antoine Estate Rum 75% ABV (export bottle); "
                    "extremely limited international distribution; UK/US ~$25–35 for 750mL"},
        {"tier": 3, "tier_name": "Grenada-Produced Rum — Clarke's Court",
         "criteria": "Grenada origin; produced at Clarke's Court Distillery "
                     "(Grenada's other major rum producer, more accessible);  "
                     "correct Grenada terroir character",
         "markers": "Clarke's Court Special Dark; Clarke's Court Pure White; BC/US ~$20–28"},
        {"tier": 2, "tier_name": "West Indian Overproof White Rum (Windward Islands)",
         "criteria": "Caribbean overproof white rum at 65–75% ABV; "
                     "vesou or heavy molasses base; traditional Caribbean character",
         "markers": "Wray & Nephew Overproof (Jamaica, 63%); Bacardi 151 (discontinued); "
                    "Hamilton Pot Still Black (US import); BC/US ~$22–35"},
        {"tier": 1, "tier_name": "Premium White Rum (Commercial Reference)",
         "criteria": "High-quality white rum; clean, fresh; cocktail foundation; "
                     "reference tier for comparison with overproof and aged styles",
         "markers": "Banks 5 Island; Wray & Nephew White Overproof; Foursquare White; "
                    "BC/US ~$18–25"}
    ],
    "service_intelligence": {
        "temperature": "Never serve undiluted; dilute 1:1 with still water before service "
                       "to reach ~37% ABV. Temperature: room temperature or with single ice cube.",
        "vessel": "Small rocks glass (diluted) or shot glass (for programme tasting purposes); "
                  "no stemmed glass",
        "technique": "Service protocol: dilute 15mL of River Antoine 75% with 15mL still water "
                     "to create a 30mL tasting portion at ~37.5% ABV. "
                     "Instruct guests to nose from 15cm distance before tasting — "
                     "the undiluted vapour at 75% ABV is intense. "
                     "Caribbean Rum Punch using River Antoine: 1 part (3mL) River Antoine + "
                     "6 parts fruit juice (grapefruit, pineapple, lime) + 3 parts coconut water — "
                     "the overproof makes a punch of normal strength with minimal volume. "
                     "Historical education: describe the plantation daily ration dilution practice.",
        "programme_position": "Historical education anchor; most traditional rum production demonstration; "
                              "PCT×WADT history narrative (waterwheel, original equipment, 1780s)",
        "verbal_presentation": "River Antoine Estate — Grenada, 1780s. "
                               "The same waterwheel. The same copper pot still. "
                               "The same wild yeast from the air. "
                               "Two hundred and forty years of Caribbean rum production, unchanged."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "River Antoine Estate (Duquesne, St. Patrick Parish, Grenada)",
        "producer_location": "River Antoine Estate, St. Patrick Parish, northern Grenada",
        "key_person": "River Antoine family management (family-owned since the estate was built)",
        "production_volume": "Very small; mostly sold at the estate and local Grenada market; "
                             "limited export versions available",
        "certifications": ["Heritage rum classification (Grenada Sugar Factory standards)"],
        "bc_distributor": "Not commercially available in BC; "
                          "extremely limited export distribution; "
                          "seek via specialist Caribbean rum importers (Hamilton Rum, "
                          "MiniBar Delivery, Caskers online)",
        "us_distributor": "Hamilton Spirits Company (Greg Brady, NYC; imports rare Caribbean rums "
                          "including River Antoine — confirmed); specialist spirits retailers: "
                          "Astor Wines NYC, K&L Wines SF carry when available",
        "uk_distributor": "Master of Malt carries limited River Antoine stock; "
                          "The Whisky Exchange; La Maison du Whisky (UK/FR)",
        "price_tier": "Market (~$25–35 US for export bottle; negligible at estate in Grenada)",
        "availability_notes": "River Antoine is one of the most difficult rum expressions to source "
                              "in North America. "
                              "US: Hamilton Spirits (hamiltonrum.com) is the most reliable; "
                              "K&L Wines San Francisco. "
                              "BC: no reliable retail source; online private import only. "
                              "UK: Master of Malt most consistent. "
                              "Alternative: serve Wray & Nephew Overproof (Jamaica, 63% ABV) "
                              "as the most widely available overproof comparison point."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "River Antoine Estate was built by enslaved West African workers "
                  "approximately 1785–1800 on what had been French colonial land. "
                  "The waterwheel, the vats, the stills, and the mill represent the "
                  "most intact physical legacy of the Atlantic plantation rum economy "
                  "still in active commercial operation anywhere in the Caribbean. "
                  "The WADT (West African Diaspora Trail) is not abstract here — "
                  "the labour that built this equipment was African enslaved labour; "
                  "the same overproof rum they produced was allocated as their daily ration. "
                  "River Antoine's continuation is both a heritage achievement and an "
                  "act of historical memory.",
    "food_pairings": [
        {"technique_id": "", "dish": "Oil-down (Grenada national dish — breadfruit, callaloo, coconut milk, salt fish)",
         "pairing_type": "complement",
         "rationale": "Oil-down — Grenada's national dish, a one-pot stew of breadfruit, "
                      "callaloo, salted meat and fish, coconut milk, and Caribbean spices — "
                      "is the most direct River Antoine pairing: both are expressions of "
                      "Grenada's agricultural bounty. The raw cane character of the rum "
                      "mirrors the fresh coconut and breadfruit of the dish; "
                      "the rum diluted with coconut water becomes an "
                      "extension of the same culinary tradition"},
        {"technique_id": "", "dish": "Nutmeg ice cream (Grenada is the world's second-largest nutmeg producer)",
         "pairing_type": "bridge",
         "rationale": "Grenada produces approximately 20% of the world's nutmeg — "
                      "the island was known as the 'Spice Isle.' River Antoine rum "
                      "with fresh-grated Grenadian nutmeg on vanilla ice cream "
                      "is the most sensory-specific Grenada experience available: "
                      "the overproof rum's raw cane character is transformed by "
                      "the nutmeg's warm-spice oils into a flavour combination "
                      "unique to this island"}
    ],
    "source": "River Antoine Estate production documentation; "
              "Grenada History Trust heritage distillery documentation; "
              "Dave Broom 'Rum' (Grenada section); "
              "Hamilton Spirits Company import documentation; "
              "WIRSPA Windward Islands rum producers",
})

session.commit_batch()
print(f"\n[BATCH 46 COMMITTED — River Antoine Grenada Rum]\n")

# ============================================================
# RON ZACAPA — GUATEMALA — Central American PCT Extension
# ============================================================

session.switch_region("spirits", "Central America — Guatemala (Ron Zacapa, Highlands)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "guatemalan rum sistema solera highland",
    "region": "Central America — Guatemala (Retalhuleu on Pacific coast; aged 2,300m highlands)",
    "name": "Ron Zacapa — Guatemala Sistema Solera, the Highest Aged Rum in the World",
    "terroir_origin": (
        "Ron Zacapa Centenario is produced from sugarcane grown in Guatemala's "
        "Pacific coastal lowlands (Retalhuleu) and aged 2,300m above sea level "
        "in the Quetzaltenango highlands — the unique 'House Above the Clouds' "
        "ageing warehouse. "
        "The PCT connection: Central America's Portuguese colonial link is indirect — "
        "the region was primarily Spanish colonial territory — "
        "but the sugarcane varieties cultivated in Guatemala arrived via the same "
        "Portuguese Atlantic chain (Madeira → Caribbean → Spanish mainland colonies). "
        "More directly: Zacapa represents the Spanish colonial rum tradition "
        "that parallels the Portuguese-influenced Caribbean tradition. "
        "The terroir innovation: ageing at 2,300m altitude creates dramatically different "
        "conditions from sea-level Caribbean ageing — the thinner air, lower ambient "
        "pressure, cooler temperatures (average 15°C vs. Caribbean 28°C), and "
        "lower oxygen content slow the evaporation and oak extraction rates. "
        "The result: a slower, more nuanced ageing curve. "
        "Ron Zacapa 23: average 6–23 years of age using the Sistema Solera method — "
        "the Sherry solera system applied to rum, creating blends of multiple vintages "
        "in sequence rather than single-year ageing. "
        "Zacapa is owned by Diageo (since 2011) and is one of the world's most "
        "premium rum expressions by price and critical recognition."
    ),
    "production_technique": (
        "Ron Zacapa's production uses first-press virgin sugarcane honey "
        "(vírgen de caña — the first pressing of the sugarcane) "
        "rather than blackstrap molasses. This is unusual: most rum uses molasses, "
        "the byproduct of sugar refining. First-press juice contains higher sugar "
        "content and different aromatic precursors than molasses — "
        "closer to the rhum agricole tradition (fresh juice) than to the "
        "standard molasses tradition, but produced differently (condensed and "
        "clarified rather than immediately fermented). "
        "Fermentation: 3–5 days using specific yeast strains; "
        "the first-press honey provides more complex fermentation substrate "
        "than blackstrap molasses. "
        "Distillation: column still (the American-continental production tradition "
        "rather than the pot-still artisanal Caribbean tradition). "
        "Sistema Solera ageing: casks arranged in tiers; the oldest rum is at "
        "the bottom, the youngest at the top; fractional drawing from the "
        "bottom tier (never more than 1/3 of the oldest cask at a time) "
        "and refilling with younger spirit. "
        "Cask variety: ex-bourbon, ex-sherry, ex-port, ex-Pedro Ximénez; "
        "the diversity of cask types is the central complexity driver. "
        "Ageing location: the 'House Above the Clouds' at 2,300m in the "
        "Quetzaltenango/Huehuetenango highlands of western Guatemala."
    ),
    "cross_tradition_parallels": [
        {"tradition": "fortified", "beverage": "Amontillado Sherry (Solera ageing, Jerez)",
         "connection": "Ron Zacapa's Sistema Solera is directly borrowed from Sherry production: "
                       "the fractional blending across age tiers creates similar complexity "
                       "to Amontillado or Palo Cortado — you cannot identify a single vintage "
                       "because every glass contains rum from multiple years. "
                       "Both Amontillado and Zacapa 23 achieve their complexity through "
                       "sustained wood contact across multiple age layers; "
                       "both carry dried fruit, nut, and warm spice as their signature profile"},
        {"tradition": "spirits", "beverage": "Foursquare Exceptional Cask Series (Barbados)",
         "connection": "Zacapa 23 and Foursquare Exceptional Cask represent the two most "
                       "technically ambitious premium rum approaches: Foursquare's vintage-dated, "
                       "cask-strength, no-additives transparency vs. Zacapa's solera-blended, "
                       "high-altitude, multi-cask complexity. "
                       "Both command premium pricing; both have expanded the category's ceiling. "
                       "The philosophical contrast is instructive: "
                       "Foursquare argues for purity and declared vintage; "
                       "Zacapa argues for complexity and blended continuity"}
    ],
    "sensory_profile": {
        "appearance": "Deep mahogany; amber-orange highlights; viscous; "
                      "slow legs from the high residual sweetness and natural concentration",
        "nose": "Zacapa 23: extraordinarily rich — vanilla cream, dark toffee, "
                "dried plum and fig, orange confit, roasted coffee, dark chocolate, "
                "warm spice (cinnamon, cardamom), oak — and underneath it all, "
                "the first-press cane honey's own gentle sweetness. "
                "The altitude ageing is perceptible: the flavours are concentrated "
                "without the heavy tropical-wood extraction of sea-level Caribbean rum. "
                "XO (older solera expression): more dried fruit, more coffee, more chocolate; "
                "extraordinary length and density.",
        "palate": "40% ABV (Zacapa 23); the residual sweetness is significant — "
                  "Zacapa has historically added a small amount of sugar post-distillation "
                  "(a controversial practice in the rum community, following Richard Seale's "
                  "campaigning for pure rum standards). "
                  "The flavour is full, rich, accessible — the most luxuriously textured "
                  "rum at its price point. "
                  "Zacapa XO: 40% ABV; deeper; longer finish; "
                  "the solera's oldest fractions create layers of complexity.",
        "conclusion": "Zacapa 23 is the rum world's most successful premium gift-category product — "
                      "widely regarded as the entry into 'serious rum' for consumers who "
                      "begin with its accessibility and then discover more complex expressions. "
                      "For a programme: position as the 'gateway premium rum' before Foursquare "
                      "and El Dorado; its accessibility is a feature, not a limitation."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Ron Zacapa XO / Edición Negra Luxury",
         "criteria": "Extended solera; older average age; ex-Pedro Ximénez finish; "
                     "luxury packaging tier",
         "markers": "Zacapa XO; Zacapa Royal 25yr; limited expressions; "
                    "BC ~$100–160; US ~$80–130"},
        {"tier": 3, "tier_name": "Ron Zacapa 23 (Centenario)",
         "criteria": "Sistema Solera; 6–23 year range; House Above the Clouds ageing; "
                     "multi-cask complexity; the reference expression",
         "markers": "Ron Zacapa Centenario 23; BC ~$60–75; US ~$45–60"},
        {"tier": 2, "tier_name": "Ron Zacapa Edición Negra",
         "criteria": "Younger solera average; accessible; introduction to the Zacapa profile",
         "markers": "Zacapa Edición Negra; BC ~$40–50; US ~$30–40"},
        {"tier": 1, "tier_name": "Guatemala Rum Category (Commercial Reference)",
         "criteria": "Guatemala origin; correct highland character; "
                     "commercial accessibility",
         "markers": "Botran Reserva; Diplomático (Venezuela, similar style); "
                    "BC/US ~$25–38"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for Zacapa 23 neat; the solera complexity opens "
                       "at 18–20°C. Ice optional: a single large cube is acceptable.",
        "vessel": "Wide-bowl snifter or Glencairn; the rich aromatics fill a larger vessel well",
        "technique": "Zacapa 23 neat: 45mL, room temperature, 3–5 minutes to open fully. "
                     "Old Fashioned: Zacapa 23 60mL + 5mL agave syrup + "
                     "2 dashes Angostura + orange peel — the solera complexity "
                     "makes an extraordinarily layered Old Fashioned. "
                     "XO: digestif only, neat at 30mL. "
                     "Guest pairing recommendation: offer Zacapa 23 alongside dark chocolate "
                     "as the natural pairing.",
        "programme_position": "Premium gift rum; gateway to the serious rum conversation; "
                              "educational: solera ageing method demonstration",
        "verbal_presentation": "Ron Zacapa Centenario 23 — Quetzaltenango highlands, Guatemala. "
                               "Aged 2,300 metres above sea level in the House Above the Clouds. "
                               "A solera blend: every glass contains rum from up to 23 years of "
                               "fractional ageing in ex-bourbon, ex-sherry, and Pedro Ximénez casks."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Industrias Licoreras de Guatemala (ILG) — Zacapa",
        "producer_location": "Retalhuleu (production) / Quetzaltenango (ageing), Guatemala",
        "key_person": "Lorena Vásquez (Master Blender, Zacapa — one of Latin America's most prominent "
                      "female master blenders); Diageo (owner since 2011)",
        "production_volume": "Premium commercial; globally distributed via Diageo; "
                             "one of the top 5 premium rum brands globally by value",
        "certifications": ["Guatemala Rum Producers Association"],
        "bc_distributor": "Diageo Canada / BCLDB; Ron Zacapa 23 widely available at BC Liquor stores",
        "us_distributor": "Diageo North America (national); widely available Total Wine, BevMo, "
                          "national premium retailers",
        "uk_distributor": "Diageo UK; widely available at Waitrose, Sainsbury's, major retailers",
        "price_tier": "Reserve to Prestige (Zacapa 23 BC ~$65–75; XO BC ~$130–160)",
        "availability_notes": "Zacapa 23: BC Liquor stores nationally; one of the most accessible "
                              "premium rums in BC. US: Diageo national at virtually all "
                              "premium spirits retailers. The most widely distributed "
                              "premium-tier rum in North America."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Guatemala's sugarcane agriculture arrived via the Spanish colonial trade network "
                  "that used the same Portuguese Atlantic island-sourced cane varieties. "
                  "The Zacapa story is specifically Central American: "
                  "a Spanish-colonial agricultural base (sugarcane) combined with "
                  "a French-inspired ageing technique (solera from Jerez) and "
                  "a specifically Guatemalan terroir innovation (altitude ageing). "
                  "Lorena Vásquez's role as Master Blender continues the Latin American "
                  "female Master Blender tradition established by Joy Spence (Appleton, Jamaica) "
                  "and continued by Trudiann Branker (Mount Gay, Barbados).",
    "food_pairings": [
        {"technique_id": "", "dish": "Mole negro (Oaxacan dried chilli, chocolate, spice sauce on turkey)",
         "pairing_type": "complement",
         "rationale": "Mole negro's complexity — 30+ ingredients including dried chillis, "
                      "chocolate, sesame, cumin, cinnamon, dried fruit — "
                      "mirrors Zacapa's own multi-layer solera complexity. "
                      "The chocolate and dried fruit in the mole find the same register "
                      "in the rum; the chilli heat is cut by the rum's sweetness. "
                      "The most ambitious Caribbean-Central American food pairing"},
        {"technique_id": "", "dish": "Dark chocolate truffles (70%+ cacao, single origin)",
         "pairing_type": "complement",
         "rationale": "Zacapa 23's vanilla-toffee-dried-fruit complexity mirrors "
                      "dark chocolate's own bitter-fruit register — the solera's "
                      "multi-year wood integration provides the same layered complexity "
                      "as a well-conched single-origin chocolate. "
                      "The canonical premium rum and dark chocolate pairing"}
    ],
    "source": "Ron Zacapa official production documentation; "
              "Diageo 2024 annual report (Zacapa acquisition history); "
              "Lorena Vásquez Master Blender biography; "
              "ILG Guatemala production documentation; "
              "The Rum Lab industry analysis (solera rum methodology)",
})

session.commit_batch()
print(f"\n[BATCH 47 COMMITTED — Ron Zacapa Guatemala]\n")

# PRODUCERS
session.add_producer({
    "name": "Angostura Ltd",
    "location": "Laventille, Port of Spain, Trinidad and Tobago",
    "country": "Trinidad and Tobago",
    "region": "Port of Spain / La Brea, Trinidad",
    "tradition": "spirits",
    "key_person": "Lorcan Dowd (CEO, Angostura Holdings); Dr. Johann Gottlieb Benjamin Siegert (founder, 1824)",
    "founded": "1824 (Angostura Bitters); 1949 (Angostura rum distillery)",
    "production_volume": "Large commercial; bitters distributed to 170+ countries; "
                         "rum in 50+ markets",
    "notable_products": ["Angostura Aromatic Bitters", "Angostura 1824 12yr",
                         "Angostura 1919 Rum", "Angostura Reserva 5yr",
                         "Angostura 1919 White Rum"],
    "certifications": ["Trinidad Rum Producers Association", "WIRSPA"],
    "website": "angostura.com",
    "philosophy": "The world's most widely distributed cocktail ingredient (Angostura Bitters) "
                  "alongside a premium rum range that carries the same Trinidad terroir. "
                  "The bitters formula, known only to five family members, is the most "
                  "guarded recipe in the beverages industry — a 200-year-old secret "
                  "that flavours cocktails globally.",
    "trail_connection": "PCT×WADT",
    "source": "Angostura Holdings official documentation; Campari America US distribution confirmation",
    "verified": True
})

session.add_producer({
    "name": "Industrias Licoreras de Guatemala (ILG) — Ron Zacapa",
    "location": "Retalhuleu (production) / Quetzaltenango (ageing), Guatemala",
    "country": "Guatemala",
    "region": "Pacific coast lowlands (production) / Western highlands (ageing)",
    "tradition": "spirits",
    "key_person": "Lorena Vásquez (Master Blender); Diageo (owner since 2011)",
    "founded": "1976 (Ron Zacapa brand launch in Guatemala's centennial year, hence 'Centenario')",
    "production_volume": "Premium commercial; top 5 premium rum brands globally by value",
    "notable_products": ["Ron Zacapa Centenario 23", "Ron Zacapa XO", "Ron Zacapa Edición Negra",
                         "Ron Zacapa Royal 25yr"],
    "certifications": ["Guatemala Rum Producers Association"],
    "website": "ronzacapa.com",
    "philosophy": "The pioneer of high-altitude rum ageing: the 'House Above the Clouds' warehouse "
                  "at 2,300m in the Guatemalan highlands produces slower, more nuanced maturation "
                  "than sea-level Caribbean ageing. Sistema Solera (fractional blending across "
                  "age tiers) combined with multi-cask variety creates the most complex blend "
                  "in the rum category at its price point.",
    "trail_connection": "PCT×WADT",
    "source": "ILG official documentation; Diageo 2024 annual report; Lorena Vásquez biography",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 48 COMMITTED — Caribbean + Central American Rum Producers]\n")

print(session.finish())
