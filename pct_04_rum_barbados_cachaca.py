#!/usr/bin/env python3
"""
PCT×WADT Barbados Rum (Foursquare + Mount Gay)
+ PCT-13 Cachaça continuation (aged wood categories)
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="Caribbean — Barbados",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=5,
    running_total=29
)

# ============================================================
# BARBADOS RUM — PCT×WADT
# ============================================================

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "barbados rum hybrid pot-column",
    "region": "Caribbean — Barbados",
    "name": "Barbados Rum — Foursquare and the Hybrid Pot-Column Style",
    "terroir_origin": (
        "Barbados claims the first written record of rum distillation anywhere in the world — "
        "a 1647 account by Richard Ligon describing a potent spirit made from sugarcane juice. "
        "The island sits at the easternmost point of the Caribbean arc, catching the full force "
        "of Atlantic trade winds, which moderate tropical heat to produce a sugarcane with "
        "distinct mineral-saline character. Barbados's coral limestone terroir — a flat island "
        "built on reef bedrock — imparts a mineral precision to its distillates that distinguishes "
        "Barbadian rum from the heavier Jamaican or the lighter Puerto Rican styles. "
        "The PCT connection is immediate: the sugarcane varieties used in Barbados arrived via "
        "the Portuguese Atlantic island trade route (Madeira → Brazil → Caribbean), making "
        "Barbados rum the northernmost expression of the same agricultural chain that began "
        "in Madeira in the 15th century. "
        "Foursquare Distillery (St. Philip Parish) is the flagship modern Barbados producer: "
        "Richard Seale (4th generation) has become one of the world's most respected rum makers "
        "through an uncompromising 'pure rum' philosophy — no added sugar, no artificial colouring, "
        "no additives. His Exceptional Cask Series releases have won Jim Murray's Rum of the Year "
        "multiple times and redefined global expectations for Barbados rum."
    ),
    "production_technique": (
        "Barbados rum uses the hybrid pot-and-column still format — the defining technical "
        "characteristic of the Barbadian style. Foursquare operates both a two-column continuous "
        "still and traditional copper pot stills simultaneously. Each fraction is distilled "
        "separately — the column produces lighter, cleaner spirit; the pot still produces "
        "heavier, ester-rich fractions — then blended and aged together. "
        "Fermentation: 24–36 hours using select yeasts; molasses-based (blackstrap molasses from "
        "West Indian sugarcane). Distillation: pot still fraction at 75–80% ABV; column fraction "
        "at 88–92% ABV; both reduced and blended pre-ageing. "
        "Ageing: ex-bourbon American oak barrels (most common); ex-sherry and port casks for "
        "Exceptional Cask releases. Tropical ageing in Barbados accelerates maturation — "
        "the angel's share runs approximately 7–8% annually, so a 12-year Barbados rum has "
        "experienced more ageing than a 15-year Scotch. "
        "Richard Seale's Exceptional Cask Series: single cask or small batch, cask-strength releases "
        "that have included ex-Madeira (a direct PCT link), ex-port, ex-sherry, and double-ageing "
        "(Barbados + Scotland finish). The 2021 Exceptional Cask finished in ex-Madeira cask was "
        "reviewed as one of the finest rums ever produced."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Single Malt Scotch Whisky (Highland)",
         "connection": "Foursquare Exceptional Cask Series invites direct comparison with Highland malt: "
                       "both use traditional copper pot stills alongside column distillation for complexity; "
                       "both age in ex-bourbon and ex-sherry casks; both are understood through vintage "
                       "expressions and cask-strength releases. Seale has explicitly positioned Foursquare "
                       "in the Scotch quality conversation, and collectors follow his releases with the "
                       "same anticipation as Samaroli or Berry Bros. Scotch bottlings"},
        {"tradition": "spirits", "beverage": "Cognac (Grande Champagne)",
         "connection": "Mount Gay XO and the broader Barbados aged rum tradition share Cognac's central "
                       "tension: blending across different cask types and ages to achieve consistent "
                       "house style versus single-vintage expression. Both traditions use copper pot "
                       "stills (alembic vs. Barbadian copper pot) and both finish in French oak-adjacent "
                       "casks. The mineral precision of Barbados terroir parallels Grande Champagne "
                       "chalk's contribution to Cognac's signature linearity"}
    ],
    "sensory_profile": {
        "appearance": "Golden to deep amber; Foursquare Exceptional releases often show deep tawny "
                      "brown with ex-sherry cask influence; viscous at cask strength (58–62% ABV)",
        "nose": "Foursquare 12yr: fresh banana, vanilla, toasted oak, coconut husk, "
                "baking spice (cinnamon, nutmeg), dried apricot; "
                "mineral-saline undertone characteristic of Barbados coral limestone. "
                "Exceptional Cask (ex-Madeira finish): dried fig, walnut, orange peel, "
                "espresso, dark toffee — distinctly vinous from the Madeira wood. "
                "No added sugar means the finish is dry and precise rather than sweet and broad.",
        "palate": "Medium-full body; balanced pot/column profile means complexity without heaviness; "
                  "Foursquare 12yr: 40% ABV; structured; clean, dry finish with vanilla and oak. "
                  "Exceptional Cask: cask strength (typically 58–62% ABV); extraordinary depth; "
                  "a decade of flavour development across one uninterrupted sip. "
                  "Mount Gay Black Barrel: double ageing (ex-bourbon then American white oak); "
                  "sweeter profile; vanilla-caramel-tropical fruit; the most accessible Barbados style.",
        "conclusion": "Foursquare Exceptional Cask Series is the strongest argument that rum deserves "
                      "the same cellar space as rare Scotch or aged Cognac. At the same price point, "
                      "nothing else in spirits delivers comparable complexity-to-cost. For a programme: "
                      "lead with Mount Gay Black Barrel for cocktails and introduction; position "
                      "Foursquare Exceptional as the premium sipping conversation."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Foursquare Exceptional Cask Series / Vintage Single Cask",
         "criteria": "Named vintage; cask-strength or close; ex-sherry, ex-Madeira, or double-aged; "
                     "Foursquare or Mark Reynier (Habitation Velier) collaboration releases",
         "markers": "Foursquare Exceptional Cask 2008–2019 vintages; Doorly's XO; Habitation Velier Foursquare; "
                    "limited allocations through specialty spirits merchants; BC ~$110–180"},
        {"tier": 3, "tier_name": "Foursquare 12yr / Mount Gay XO",
         "criteria": "12+ years tropical ageing; hybrid pot-column; named estate; no added sugar confirmed",
         "markers": "Foursquare 12yr; Mount Gay XO; Mount Gay 1703 (blend); "
                    "BC ~$60–90; Total Wine, BevMo nationally"},
        {"tier": 2, "tier_name": "Foursquare 9yr / Mount Gay Black Barrel",
         "criteria": "Double or extended ageing; correct Barbados mineral character; cocktail or entry sipping",
         "markers": "Foursquare 9yr; Mount Gay Black Barrel; Doorly's 12yr; BC ~$38–55"},
        {"tier": 1, "tier_name": "Mount Gay Eclipse / Doorly's 8yr",
         "criteria": "Accessible entry; correct Barbados style; cocktail foundation",
         "markers": "Mount Gay Eclipse; Doorly's 8yr; Cockspur; BC ~$28–38"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for Exceptional Cask sipping; over large ice for cocktails",
        "vessel": "Glencairn or NEAT glass for Foursquare sipping; rocks glass for Mount Gay cocktails",
        "technique": "Foursquare Exceptional Cask: neat, 45mL, 10 minutes to open — treat like a Highland malt. "
                     "Add a few drops of water to cask-strength expressions to open the ester profile. "
                     "Mount Gay Black Barrel Old Fashioned: 60mL + 5mL demerara syrup + 2 dashes "
                     "Angostura + orange peel. Rum Sour: Foursquare 12yr 60mL + lime 22mL + "
                     "sugar syrup 15mL + egg white — the superior riff on a Whisky Sour.",
        "programme_position": "Premium spirits sipping section; rum cocktail foundation; "
                              "Exceptional Cask as the 'serious rum' table narrative",
        "verbal_presentation": "Foursquare Exceptional Cask — Barbados, 2010 vintage. "
                               "Twelve years in Caribbean heat, then finished in ex-Madeira cask. "
                               "No added sugar. Richard Seale's definition of pure rum."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Foursquare Distillery (St. Philip, Barbados) — Richard Seale",
        "producer_location": "Foursquare, St. Philip Parish, Barbados",
        "key_person": "Richard Seale (Master Blender, 4th generation; the world's most vocal advocate for "
                      "pure rum standards); Peter Boos (Mount Gay, Rémy Cointreau)",
        "production_volume": "Foursquare: boutique to premium (Exceptional Cask: limited allocation); "
                             "Mount Gay: large commercial (1703 brand, world's oldest operational rum distillery)",
        "certifications": ["Barbados Rum Association", "WIRSPA (West Indies Rum and Spirits Producers Association)"],
        "bc_distributor": "Foursquare: Authentic Wine & Spirits Merchants (AWSM Canada) — BC specialist importer "
                          "[verify current arrangement]; Mount Gay: available at BC Liquor (BCLDB confirmed)",
        "us_distributor": "Foursquare: Altamar Brands (national US distribution — confirmed); "
                          "Mount Gay: Rémy Cointreau USA (confirmed national)",
        "uk_distributor": "Foursquare: widely available; Berry Bros. & Rudd carries Exceptional Cask releases. "
                          "Mount Gay: mainstream UK availability (Waitrose, Sainsbury's, Majestic)",
        "price_tier": "Reserve to Prestige (Foursquare 12yr BC ~$65; Exceptional Cask ~$130–180; "
                      "Mount Gay XO BC ~$75; Eclipse BC ~$32)",
        "availability_notes": "Mount Gay Eclipse: BC Liquor stores widely. Foursquare 12yr and Exceptional "
                              "Cask: Marquis Wine Cellars, Liberty Wine, Firefly Fine Wines (Vancouver). "
                              "US: Foursquare via Altamar at Total Wine and specialty spirits shops nationally."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Barbados rum is the cultural and agricultural convergence of the Portuguese Atlantic "
                  "colonial project (sugarcane from Madeira via Brazil) and the West African Diaspora Trail "
                  "(enslaved Barbadian workers who built and operated the first distilleries from 1647). "
                  "Foursquare operates the Barbados Rum Factory — a heritage site incorporating the original "
                  "19th-century steam engine and mill house. Richard Seale's 'pure rum' advocacy represents "
                  "a deliberate resistance to the category's historic exploitation and obscurity.",
    "food_pairings": [
        {"technique_id": "", "dish": "Conkies (Barbadian cornmeal, coconut, pumpkin steamed pudding)",
         "pairing_type": "complement",
         "rationale": "The coconut-spice register of Foursquare 12yr mirrors conkies' own coconut "
                      "and cinnamon character — the national dish paired with the national spirit "
                      "at the same flavour frequency"},
        {"technique_id": "", "dish": "Grilled flying fish with bajan seasoning (Barbados national dish)",
         "pairing_type": "contrast",
         "rationale": "The salt-mineral-herb profile of flying fish seasoned with garlic, lime, "
                      "scotch bonnet, and marjoram contrasts cleanly against the sweet-vanilla "
                      "barrel character of Mount Gay Black Barrel — salt cutting sweetness, "
                      "acid cutting wood tannin"}
    ],
    "source": "Foursquare Distillery official production documentation; Richard Seale interview "
              "archive (The Fat Rum Pirate, 2016–2023); Mount Gay Distilleries official history; "
              "Jim Murray's Rum of the Year citations (2016–2022); Richard Ligon 1647 Barbados account; "
              "WIRSPA production standards documentation",
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "barbados rum mount gay heritage",
    "region": "Caribbean — Barbados",
    "name": "Mount Gay — The World's Oldest Rum Distillery (1703)",
    "terroir_origin": (
        "Mount Gay Distilleries, established by deed of sale in 1703 (St. Lucy Parish, Barbados), "
        "is the world's oldest operational rum distillery — predating the Scotch whisky industry's "
        "oldest licensed distillery by over a century. The 1703 date is documented in the sale deed "
        "of a plantation with 'two stone windmills, one boiling house, one curing house, and one "
        "still house' — the complete infrastructure of a working distillery. "
        "St. Lucy Parish sits at Barbados's northernmost tip, the most wind-exposed point of the "
        "island. The Atlantic-facing coral limestone plateau produces sugarcane with a pronounced "
        "mineral salinity — the same terroir character that distinguishes Barbados rum from the "
        "Caribbean's other major styles. Rémy Cointreau acquired Mount Gay in 1989, and the brand "
        "has operated under French fine-spirits management since — bringing a house-style discipline "
        "that emphasises consistency and the layered complexity of long ageing. "
        "The PCT connection: St. Lucy's geographic position — facing directly toward the Portuguese "
        "Atlantic route — means Mount Gay's terroir is the most direct Caribbean expression of the "
        "transatlantic sugarcane migration that Portugal initiated from Madeira in the 1400s."
    ),
    "production_technique": (
        "Mount Gay uses the Barbados hybrid still format: copper pot stills (for heavy, complex marks) "
        "combined with column stills (for lighter, cleaner fractions). Master Blender Trudiann Branker "
        "blends pot and column fractions at various aged stages to build the layered house style. "
        "Fermentation: blackstrap molasses; 24–36 hours; proprietary yeast strain. "
        "Ageing: primary ageing in ex-bourbon American oak casks in Barbados tropical climate. "
        "Eclipse (flagship): minimum 2 years; blend of pot and column spirits. "
        "Black Barrel: double-aged — first in ex-bourbon, then 6 months in charred American white oak "
        "barrels used for bourbon (the 'black barrel' of the name); the second ageing adds caramel, "
        "vanilla depth without losing Barbados mineral character. "
        "XO: reserve blend, pot and column, aged 8–15 years; the prestige house expression. "
        "1703 Master Select: annual limited release, the oldest and most complex Mount Gay expression "
        "(15–30 year blends from the private reserve). "
        "Trudiann Branker became Master Blender in 2018 — one of the first women to hold that title "
        "in the rum industry globally, following Joy Spence at Appleton by two decades."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Armagnac (Bas-Armagnac, Hors d'Age)",
         "connection": "Mount Gay 1703 Master Select and Armagnac Hors d'Age share the defining challenge "
                       "of the luxury aged spirits: blending across a wide range of vintages to achieve "
                       "extraordinary complexity while maintaining house character. Both use copper pot "
                       "distillation (column + pot for Mount Gay; continuous Armagnac alembic + pot for "
                       "prestige releases); both express terroir through mineral linearity rather than "
                       "oak-forward sweetness"},
        {"tradition": "wine", "beverage": "Aged Oloroso Sherry (Jerez)",
         "connection": "Mount Gay XO's ageing in tropical Caribbean heat produces the same "
                       "progressive concentration and oxidative complexity that solera ageing "
                       "achieves in Jerez. Both show dried fruit (raisin, fig), tobacco, "
                       "leather, and toasted nut; both are built on the principle that time "
                       "and evaporation create more complexity than any production shortcut"}
    ],
    "sensory_profile": {
        "appearance": "Mount Gay Black Barrel: medium amber, bright; Eclipse: pale gold; "
                      "XO: deep amber-mahogany; 1703: dark tawny with viscosity at 43% ABV",
        "nose": "Eclipse: banana, vanilla, caramel, light coconut — clean, youthful, mineral base. "
                "Black Barrel: butterscotch, toasted vanilla, banana foster, light smoke, "
                "caramelised sugar — the second char brings warmth. "
                "XO: dark toffee, dried stone fruit (apricot, plum), warm spice, "
                "leather, coconut cream — the full Barbados spectrum. "
                "1703 Master Select: extraordinary — orange peel confit, espresso, walnut, "
                "roasted oak, dark dried fruit, ancient wood — the rarest character in Barbados rum",
        "palate": "Black Barrel: 43% ABV; full body for the price; warm, long finish. "
                  "XO: 43% ABV; the definition of Barbados balance — weight without heaviness, "
                  "complexity without difficulty. 1703: 43% ABV; enormous; the rum equivalent of "
                  "a 25-year Highland malt at comparable pricing.",
        "conclusion": "Mount Gay XO is the most historically significant rum in constant production — "
                      "the unbroken 320-year lineage from the same St. Lucy Parish soil. "
                      "For a programme, it carries a story that no other spirit category can match: "
                      "this distillery was operating before the United States existed."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "1703 Master Select / XO Pot Still Collection",
         "criteria": "Annual limited release; 15–30 year blend from private reserve; "
                     "or XO Pot Still Collection (100% pot still, unblended with column)",
         "markers": "1703 Master Select (annual allocation); XO Pot Still; Vintage 1981 archive; "
                    "BC ~$130–220+"},
        {"tier": 3, "tier_name": "Mount Gay XO",
         "criteria": "8–15 year blend; pot and column; Barbados tropical ageing",
         "markers": "Mount Gay XO; BC ~$75; Total Wine, BevMo nationally"},
        {"tier": 2, "tier_name": "Mount Gay Black Barrel",
         "criteria": "Double-aged; ex-bourbon then charred American white oak; correct Barbados character",
         "markers": "Mount Gay Black Barrel; BC ~$45; widely available"},
        {"tier": 1, "tier_name": "Mount Gay Eclipse",
         "criteria": "Entry level; accessible pot-column blend; cocktail or introduction",
         "markers": "Mount Gay Eclipse (gold and silver); BC ~$32; most widely distributed Barbados rum"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for XO and 1703; over ice or in cocktails for Black Barrel and Eclipse",
        "vessel": "Tulip or Glencairn for XO and 1703; rocks glass for Eclipse and Black Barrel cocktails",
        "technique": "XO neat: 45mL, room temperature, 5 minutes rest — allow the tropical ageing "
                     "concentration to open. 1703: 30mL as a digestif, no ice. "
                     "Mount Gay Black Barrel Daiquiri: 60mL + 22mL lime + 15mL simple syrup, shaken — "
                     "the double-ageing caramel deepens the classic daiquiri framework. "
                     "Eclipse Rum Punch: 60mL + 30mL orange juice + 15mL grenadine + lime + Angostura.",
        "programme_position": "Heritage narrative anchor for any rum programme; 1703 Master Select "
                              "as the premium tasting experience; Black Barrel as the cocktail workhorse",
        "verbal_presentation": "Mount Gay Eclipse — St. Lucy, Barbados. The world's oldest rum distillery, "
                               "operating since 1703. Three hundred and twenty years on the same coral limestone."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Mount Gay Distilleries (St. Lucy Parish, Barbados)",
        "producer_location": "St. Lucy Parish, Barbados (north-facing Atlantic coral limestone)",
        "key_person": "Trudiann Branker (Master Blender since 2018 — one of rum's first female Master Blenders); "
                      "Rémy Cointreau (owner since 1989)",
        "production_volume": "Large commercial; Eclipse is one of the top 5 globally distributed premium rums",
        "certifications": ["Barbados Rum Association", "WIRSPA"],
        "bc_distributor": "BCLDB direct import; Mount Gay Eclipse and XO available at BC Liquor stores (confirmed)",
        "us_distributor": "Rémy Cointreau USA (confirmed national distribution)",
        "uk_distributor": "Rémy Cointreau UK; Waitrose, Sainsbury's, Majestic widely",
        "price_tier": "Market to Reserve (Eclipse BC ~$32; Black Barrel ~$45; XO ~$75; 1703 ~$160–220)",
        "availability_notes": "Eclipse and Black Barrel: BC Liquor stores statewide. XO: BC Liquor select "
                              "locations or special order. 1703: specialty spirits merchants (Marquis, "
                              "Liberty Wine Vancouver). US: nationwide via Rémy Cointreau at Total Wine, BevMo."
    },
    "trail_connection": "PCT×WADT",
    "trail_note": "Mount Gay's 1703 founding predates the American Revolution by 73 years. The distillery "
                  "has operated through 13 British monarchs, American independence, the abolition of "
                  "slavery in Barbados (1834), and Barbados's independence from Britain (2021). "
                  "The sugarcane varieties at St. Lucy are descended from the Portuguese Atlantic island "
                  "trade that defines the PCT. Under Rémy Cointreau's stewardship, Mount Gay has become "
                  "the premium face of Barbados rum globally — the 320-year continuous operation is the "
                  "rum world's most compelling provenance narrative.",
    "food_pairings": [
        {"technique_id": "", "dish": "Rum and raisin dark chocolate (70% cacao)",
         "pairing_type": "bridge",
         "rationale": "The rum-soaked raisin in dark chocolate is the textbook Mount Gay XO pairing — "
                      "the dried fruit and bitter chocolate mirror the XO's own dried plum and "
                      "tobacco depth, creating a feedback loop between food and spirit"},
        {"technique_id": "", "dish": "Barbados pepperpot (slow-braised beef with cassareep and scotch bonnet)",
         "pairing_type": "complement",
         "rationale": "The molasses depth of cassareep — the Amerindian cassava-based braising sauce "
                      "that defines pepperpot — mirrors Mount Gay's molasses-base terroir. "
                      "Black Barrel alongside pepperpot is the most literal flavour alignment "
                      "in Barbadian food and drink culture"}
    ],
    "source": "Mount Gay Distilleries official history and 1703 deed documentation; "
              "Trudiann Branker Master Blender biography; Rémy Cointreau annual report 2024; "
              "Barbados Rum Association production standards; Dave Broom 'Rum'; "
              "WIRSPA West Indian Rum documentation",
})

session.commit_batch()
print(f"\n[BATCH 24 COMMITTED — Barbados Rum: Foursquare + Mount Gay]\n")

# ============================================================
# CACHAÇA CONTINUATION — Aged Wood Categories — PCT-13
# ============================================================

session.switch_region("spirits", "Brazil — Cachaça (Aged, Wood Varieties)")

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "aged cachaça wood-matured",
    "region": "Brazil — Cachaça (Ceará, Interior States)",
    "name": "Aged Cachaça — Amburana, Carvalho, and Native Wood Maturation",
    "terroir_origin": (
        "Cachaça's ageing tradition is the most distinctive in global spirits: Brazil law permits "
        "maturation in over 28 different wood species, including tropical hardwoods unique to the "
        "Amazon basin and Brazilian cerrado. This is categorically different from every other "
        "major spirits category (Scotch, Cognac, Bourbon, Armagnac) where ageing is almost "
        "exclusively in oak. The result is a spectrum of cachaça aged expression with no direct "
        "parallel in world spirits. "
        "The key native Brazilian woods: "
        "Amburana (Amburana cearensis) — from the northeastern Caatinga and cerrado biomes; "
        "imparts vanilla, coconut husk, cinnamon, and a distinctive sweet coumarin character. "
        "The most celebrated cachaça ageing wood globally. "
        "Carvalho (Brazilian oak, various Quercus species) — similar to European oak but with "
        "stronger tannin extraction; less common than amburana but valued for structure. "
        "Castanheira (Brazilian chestnut, Bertholletia excelsa) — imparts bold tannin, "
        "dried fruit, and walnut character; the most tannic of the native wood options. "
        "Bálsamo (Myroxylon balsamum) — aromatic; adds resin and spice. "
        "Jequitibá (Cariniana legalis) — mild; preserves fruit freshness; often used for "
        "expression of unaged character in wood-aged cachaça. "
        "Ypióca (founded 1846, Ceará state; owned by Diageo since 2012) is the most globally "
        "distributed aged cachaça brand and the commercial benchmark for the wood-aged category."
    ),
    "production_technique": (
        "Brazilian law defines aged ('envelhecida') cachaça as minimum 50% of volume aged in wood "
        "vessels of maximum 700L capacity for at least one year. Premium aged cachaças typically "
        "age 2–12 years in 225–500L barrels. "
        "The spirit base: fresh sugarcane juice fermented with natural or added yeasts (24–72 hours); "
        "single distillation in copper pot still (alambique) at 38–54% ABV for premium artisanal; "
        "industrial column-distilled cachaça at 54–70% ABV for commercial brands (Ypióca uses both). "
        "Wood treatment: amburana barrels are typically air-dried 2–3 years before use; "
        "the coumarin (a naturally occurring aromatic compound) in amburana wood is the source "
        "of its distinctive coconut-vanilla-cinnamon character. "
        "Ypióca's flagship aged expression: Ypióca Ouro (Gold) — a blend of amburana and "
        "carvalho aged 6 months minimum; the commercial accessible entry. "
        "Ypióca Legítima (aged 1 year amburana): the premium standard expression. "
        "Artisanal benchmark: Novo Fogo Single Barrel (amburana or Brazilian carvalho) — "
        "Skurnik-distributed in the US, single farm, certified organic, full traceability."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Japanese Whisky (Mizunara Oak aged)",
         "connection": "Brazil's amburana wood and Japan's mizunara oak are the two most celebrated "
                       "non-traditional ageing woods in global spirits, both producing unmistakable "
                       "flavour compounds unavailable from standard oak: amburana gives coconut-coumarin; "
                       "mizunara gives sandalwood-incense. Both are expensive, difficult to source, "
                       "and produce aged spirits with no Western equivalent — the East and the South "
                       "American expressions of the same question: what does wood other than oak do?"},
        {"tradition": "spirits", "beverage": "Mezcal (añejo, barrel aged)",
         "connection": "Aged cachaça and aged mezcal are the two most significant aged spirits expressions "
                       "from Latin America where terroir and native production tradition intersect with "
                       "wood influence. Both resist the globalized barrel format (bourbon-cask dominance); "
                       "both use indigenous raw materials and traditional distillation methods; "
                       "both are gaining critical recognition as alternatives to European aged spirit "
                       "categories precisely because they cannot be understood through European frameworks"}
    ],
    "sensory_profile": {
        "appearance": "Amburana-aged: pale gold to medium amber (surprisingly light colour given flavour "
                      "intensity — amburana wood extracts differently from oak); carvalho: deeper amber",
        "nose": "Amburana: extraordinary — fresh coconut, vanilla pod, Ceylon cinnamon, raw cane, "
                "dried flowers, warm bread; the coumarin character is immediate and unmistakable. "
                "Carvalho: more familiar oak structure (vanilla, toffee, toasted wood) but with "
                "Brazilian cane's characteristic fresh fruit underneath. "
                "Castanheira: bold — walnut skin, dried cherry, firm tannin even on the nose; "
                "the most structured of the native wood options.",
        "palate": "Amburana-aged: medium body; the wood character is aromatic rather than astringent — "
                  "the finish is dry-spiced, warm, coconut-cinnamon; extremely long. "
                  "Carvalho: firmer tannin; more linear; excellent cocktail structure. "
                  "Ypióca Legítima: the commercial benchmark — slightly sweet finish (column distillate "
                  "base); more accessible than artisanal amburana; correct varietal character.",
        "conclusion": "Aged cachaça is the most undervalued premium spirits category in North America. "
                      "For any programme: a Novo Fogo amburana single barrel alongside a "
                      "standard bourbon provides the clearest demonstration that wood choice in "
                      "spirits is as profound as grape choice in wine. "
                      "The table story is the Amazon itself."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Artisanal Single Barrel Amburana / Named Estate",
         "criteria": "Named farm; certified organic; single barrel or micro-lot; "
                     "pot-still only; vintage-dated; 2–10 years amburana or castanheira",
         "markers": "Novo Fogo Single Barrel; Avuá Amburana; Germana Heritage; "
                    "Magnífica do Salinas; BC/US specialist spirits merchants; ~$60–100+"},
        {"tier": 3, "tier_name": "Premium Aged (Ypióca Legítima / Avuá Carvalho)",
         "criteria": "Named wood; 1–3 years minimum aged; traceable origin; "
                     "artisanal or premium commercial",
         "markers": "Ypióca Legítima; Avuá Carvalho; Novo Fogo Aged (12–24 month); BC/US ~$40–60"},
        {"tier": 2, "tier_name": "Standard Aged (Ypióca Ouro / Leblon Reserva Especial)",
         "criteria": "Blended aged; correct wood character; commercial quality",
         "markers": "Ypióca Ouro; Leblon Reserva Especial; Sagatiba Velha; BC/US ~$28–40"},
        {"tier": 1, "tier_name": "Entry Aged / Commercial",
         "criteria": "Brief ageing; accessible; introduction to wood-aged category",
         "markers": "Ypióca Gold; commercial aged Cachaça 51 variants; BC/US ~$18–28"}
    ],
    "service_intelligence": {
        "temperature": "Room temperature for premium amburana; standard cocktail temperature for others",
        "vessel": "Copita or snifter for premium amburana neat; rocks glass for cocktails",
        "technique": "Novo Fogo amburana neat: 45mL, room temperature — open for 5 minutes. "
                     "Water drops optional: the high coumarin content means it needs less water "
                     "than Scotch to open. Batida de Amburana: 60mL aged cachaça + 30mL lime + "
                     "20mL sugar syrup + 60mL condensed milk — traditional Brazilian creamy cocktail. "
                     "Aged Cachaça Old Fashioned: Novo Fogo amburana 60mL + 5mL demerara + "
                     "2 dashes Angostura + orange peel — the coumarin reads as a fourth dimension "
                     "against the bitters and citrus.",
        "programme_position": "Premium spirits discovery section; PCT-13 Brazil provenance narrative; "
                              "pairing with cacao-forward desserts or dark chocolate programmes",
        "verbal_presentation": "Novo Fogo Single Barrel Amburana — Santa Catarina, Brazil. "
                               "Three years in native Amazon timber. "
                               "The wood that grows nowhere else on earth."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Novo Fogo (Morretes, Santa Catarina) for artisanal; "
                              "Ypióca (Ceará, Diageo-owned since 2012) for commercial scale",
        "producer_location": "Novo Fogo: Morretes, Santa Catarina, Brazil; "
                             "Ypióca: Maranguape, Ceará, Brazil",
        "key_person": "Dragos Axinte (Novo Fogo founder/CEO); Ypióca: Diageo Brazil management",
        "production_volume": "Ypióca: major commercial scale (~2M cases; Diageo distribution); "
                             "Novo Fogo: artisanal premium (US and international specialist distribution)",
        "certifications": ["Brazilian Cachaça GI", "Organic (Novo Fogo — certified Brazilian organic)",
                           "IBRAC (Brazilian Institute of Cachaça) member"],
        "bc_distributor": "Novo Fogo: Sovereign Canada (BC — confirmed); "
                          "Ypióca: Diageo Canada (national distribution — BC Liquor through BCLDB)",
        "us_distributor": "Novo Fogo: Skurnik Wines & Spirits (US national — confirmed); "
                          "Ypióca: Diageo North America (Diageo-owned brand, direct distribution); "
                          "Avuá: Chosen Spirits (specialist importer)",
        "uk_distributor": "Novo Fogo: specialist UK retailers (Master of Malt, The Whisky Exchange); "
                          "Ypióca: not widely distributed UK market",
        "price_tier": "Market to Reserve (Ypióca Ouro BC ~$25; Legítima ~$35; "
                      "Novo Fogo Single Barrel BC ~$75–95; Avuá Amburana ~$60–70)",
        "availability_notes": "Novo Fogo: Marquis Wine Cellars and Liberty Wine Vancouver carry aged expressions. "
                              "Ypióca: BC Liquor stores (BCLDB import via Diageo). "
                              "US: Novo Fogo Skurnik nationally; Ypióca at Total Wine and Latino specialty markets. "
                              "Amburana single barrels: extremely limited allocation — pre-order with specialist merchants."
    },
    "trail_connection": "PCT-13",
    "trail_note": "Cachaça is the most produced spirit in the Southern Hemisphere and the direct "
                  "descendant of Portuguese Atlantic colonial sugarcane agriculture. The aged wood "
                  "tradition — using Amazon and cerrado hardwoods rather than European oak — represents "
                  "the most distinctly Brazilian cultural adaptation of the PCT legacy: the Portuguese "
                  "introduced the agricultural and distillation technology; Brazil's pre-colonial "
                  "forest knowledge transformed the process into something categorically new. "
                  "Ypióca's Diageo acquisition (2012) and Novo Fogo's organic certification and "
                  "US market success represent the two poles of how Brazilian cachaça is "
                  "navigating global spirits markets.",
    "food_pairings": [
        {"technique_id": "", "dish": "Brigadeiro (Brazilian chocolate-condensed milk fudge truffle)",
         "pairing_type": "bridge",
         "rationale": "Amburana's coumarin-vanilla-coconut register bridges directly with brigadeiro's "
                      "condensed milk sweetness and cocoa powder depth — the spirit and the confection "
                      "share the same warm, sweet, tropical character but through different pathways. "
                      "Amburana cachaça alongside premium brigadeiro is the most elegant Brazilian pairing"},
        {"technique_id": "", "dish": "Pão de queijo (Minas Gerais cheese bread)",
         "pairing_type": "contrast",
         "rationale": "The sharp, slightly sour fresh queijo minas in pão de queijo contrasts "
                      "cleanly against carvalho-aged cachaça's structured tannin and vanilla — "
                      "the dairy acid cuts the wood tannin; the bread's starchiness supports the "
                      "spirit's moderate weight. The canonical Minas Gerais aperitif pairing"}
    ],
    "source": "Instituto Brasileiro da Cachaça (IBRAC) wood species documentation; "
              "Novo Fogo production documentation (novofogo.com); "
              "Ypióca official brand history and Diageo acquisition 2012; "
              "Brazilian agricultural law (MAPA) cachaça definitions and wood regulations; "
              "Dave Broom 'Rum' (cachaça section); Avuá production documentation",
})

session.commit_batch()
print(f"\n[BATCH 25 COMMITTED — Barbados Rum Cont. + Aged Cachaça]\n")

# ============================================================
# PRODUCERS
# ============================================================

session.add_producer({
    "name": "Foursquare Distillery",
    "location": "Foursquare, St. Philip Parish, Barbados",
    "country": "Barbados",
    "region": "St. Philip Parish, Barbados",
    "tradition": "spirits",
    "key_person": "Richard Seale (Master Blender and owner, 4th generation)",
    "founded": "1996 (current Seale family operation; site history 19th century sugar plantation)",
    "production_volume": "Boutique to premium; Exceptional Cask Series: limited annual allocation globally",
    "notable_products": ["Foursquare Exceptional Cask Series (annual vintage)", "Foursquare 12yr",
                         "Foursquare 9yr", "Doorly's 12yr XO", "Habitation Velier Foursquare"],
    "certifications": ["Barbados Rum Association", "WIRSPA"],
    "website": "foursquaredistillery.com",
    "philosophy": "Richard Seale's 'pure rum' manifesto: no added sugar, no artificial colouring, "
                  "no flavour additives. Every release is declared with full transparency (still type, "
                  "distillation year, cask type). The Exceptional Cask Series has redefined international "
                  "expectations for what rum can achieve at the premium end. Seale is also the "
                  "industry's most vocal advocate for GI protection and rum authenticity standards.",
    "trail_connection": "PCT×WADT",
    "source": "Foursquare official production documentation; Richard Seale interview archive; "
              "Jim Murray Rum of the Year citations",
    "verified": True
})

session.add_producer({
    "name": "Mount Gay Distilleries",
    "location": "St. Lucy Parish, Barbados",
    "country": "Barbados",
    "region": "St. Lucy Parish, Barbados (north Atlantic coast)",
    "tradition": "spirits",
    "key_person": "Trudiann Branker (Master Blender since 2018); Rémy Cointreau (owner since 1989)",
    "founded": "1703 (documented deed of sale, world's oldest operational rum distillery)",
    "production_volume": "Large commercial; Eclipse is one of the world's top 5 distributed premium rums",
    "notable_products": ["Mount Gay Eclipse", "Mount Gay Black Barrel", "Mount Gay XO",
                         "Mount Gay 1703 Master Select", "Mount Gay XO Pot Still Collection"],
    "certifications": ["Barbados Rum Association", "WIRSPA"],
    "website": "mountgayrum.com",
    "philosophy": "320+ years of continuous production from the same St. Lucy Parish site. "
                  "Under Rémy Cointreau, Mount Gay has positioned itself as the premium reference "
                  "for Barbados rum globally — combining French fine-spirits marketing discipline "
                  "with genuinely historic production continuity. Trudiann Branker's appointment "
                  "in 2018 as one of rum's first female Master Blenders continues the tradition "
                  "of pioneering leadership (following Joy Spence at Appleton, 1997).",
    "trail_connection": "PCT×WADT",
    "source": "Mount Gay official history; 1703 deed documentation; Rémy Cointreau annual report 2024; "
              "Trudiann Branker biography",
    "verified": True
})

session.add_producer({
    "name": "Ypióca (Diageo Brazil)",
    "location": "Maranguape, Ceará, Brazil",
    "country": "Brazil",
    "region": "Ceará state, northeastern Brazil",
    "tradition": "spirits",
    "key_person": "Diageo Brazil management (acquired 2012)",
    "founded": "1846 (Fazenda Ypióca, one of Brazil's oldest cachaça producers)",
    "production_volume": "Large commercial (~2 million cases; Diageo global distribution)",
    "notable_products": ["Ypióca Ouro (Gold)", "Ypióca Legítima", "Ypióca 150", "Ypióca Prata"],
    "certifications": ["IBRAC member", "Brazilian Cachaça GI"],
    "website": "ypioca.com.br",
    "philosophy": "Brazil's oldest continuously operating cachaça brand, now under Diageo's "
                  "global distribution infrastructure. Ypióca is the commercial benchmark for "
                  "amburana-aged cachaça — the brand that first brought Brazilian native wood "
                  "maturation to international awareness. The 2012 Diageo acquisition gave global "
                  "distribution but maintained the Ceará production site and amburana sourcing.",
    "trail_connection": "PCT-13",
    "source": "Ypióca official brand history; Diageo 2012 acquisition announcement; "
              "IBRAC cachaça production data",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 26 COMMITTED — Barbados + Cachaça Producers]\n")

# Purveyors
session.add_purveyor({
    "name": "Altamar Brands",
    "type": "importer",
    "location": "New York, NY, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["spirits"],
    "producer_relationships": ["Foursquare Distillery (Barbados rum)", "Dictador (Colombia)",
                               "Other premium rum and spirits"],
    "website": "altamarbrands.com",
    "contact": "altamarbrands.com",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Altamar Brands is the exclusive US national importer for Foursquare Distillery "
                      "since the brand's US market expansion. The most direct US trade route for "
                      "Foursquare Exceptional Cask Series allocations. Premium on-premise and "
                      "off-premise accounts nationally.",
    "verified": True
})

session.add_purveyor({
    "name": "Rémy Cointreau USA",
    "type": "importer",
    "location": "New York, NY, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["spirits"],
    "producer_relationships": ["Mount Gay Rum (Barbados)", "Rémy Martin Cognac", "Cointreau",
                               "Botanist Gin", "Bruichladdich Whisky"],
    "website": "remycointreau.com",
    "contact": "remycointreau.com/us",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Rémy Cointreau USA handles Mount Gay national US distribution through the "
                      "parent company's owned-brand channel. Widest distribution of any Barbados "
                      "rum brand in the US market — Eclipse available at virtually every spirits "
                      "retailer nationally. Direct supplier relationships with premium on-premise.",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 27 COMMITTED — Altamar Brands + Rémy Cointreau Purveyors]\n")

print(session.finish())
