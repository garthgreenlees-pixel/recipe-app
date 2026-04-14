#!/usr/bin/env python3
"""
PCT-3 Azores (volcanic wines + Gorreana tea)
+ PCT-11 Timor-Leste coffee (Timor Hybrid origin)
+ PCT-6 São Tomé & Príncipe (fine cacao / ceremonial)
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="wine",
    region="Portugal — Azores (Pico Island, DOC)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=6,
    running_total=32
)

# ============================================================
# AZORES WINES — PCT-3
# ============================================================

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "volcanic island white wine",
    "region": "Portugal — Azores (Pico Island DOC)",
    "name": "Azores Wine — Pico Island Volcanic White (Verdelho, Arinto dos Açores)",
    "terroir_origin": (
        "The Azores archipelago sits at the mid-Atlantic ridge, 1,400km west of Lisbon — "
        "nine volcanic islands that were uninhabited when the Portuguese arrived in 1427. "
        "Pico Island's viticultural landscape is a UNESCO World Heritage Site (2004): "
        "generations of farmers built a dense network of low black basalt walls "
        "(currais) directly on the dark volcanic rock to create thousands of tiny "
        "vine enclosures that protect vines from Atlantic winds. The landscape — "
        "black basalt, green vine, deep ocean — is one of the most visually "
        "distinctive wine regions on earth. "
        "The primary varieties: Verdelho (the same grape used in Madeira's semi-sweet "
        "style — a direct PCT-1 to PCT-3 connection across 1,000km of Atlantic ocean); "
        "Arinto dos Açores (locally adapted mutation of Arinto from the mainland, "
        "producing higher natural acidity in the Atlantic climate). "
        "The terroir is extreme: Pico rises to 2,351m (Portugal's highest peak); "
        "the sea surrounds every vine; the basalt retains daytime heat and releases "
        "it slowly at night; the Atlantic humidity means no irrigation is needed "
        "and botrytis management is the central challenge. "
        "The result is wine with no direct parallel anywhere in Europe: mineral-volcanic, "
        "high acid, oceanic salinity, moderate alcohol — the Atlantic encoded in grape form."
    ),
    "production_technique": (
        "Harvesting: September–October; entirely manual due to the terrain (no machinery "
        "can navigate the currais walls); often harvested across weeks as each micro-enclosure "
        "ripens at a different rate based on orientation and wind exposure. "
        "Vinification: minimal intervention is the norm — the terroir is so dominant that "
        "winemakers work to preserve rather than transform. Stainless steel fermentation "
        "at low temperature (13–16°C) to retain aromatics. "
        "Lagar (stone trough) fermentation still practiced by some traditional producers "
        "for limited batches. "
        "Key producers: Adega Cooperativa do Pico (largest, founded 1954; the main commercial "
        "face of Pico wine); Terras de Lava (premium artisanal, founded 2002); "
        "Cabeço do Monte (acclaimed small producer); "
        "Curral Atlântis (cooperativa premium tier). "
        "DOC regulations: Pico DOC (2002); also Biscoitos DOC (Terceira island) and "
        "Graciosa DOC. IGP Açores covers the broader category. "
        "Ageing: premium Verdelho can age 5–15 years — the natural high acidity and "
        "mineral structure create extraordinary ageing potential, particularly in bottles "
        "sealed with quality cork or screwcap."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Chablis Grand Cru (Kimmeridgian limestone)",
         "connection": "Both Azores volcanic basalt and Chablis Kimmeridgian limestone are mineral-dominant "
                       "terroirs that impose their geological identity on the wine more forcefully than "
                       "the grape variety itself. Azores Verdelho and Chablis Chardonnay both produce "
                       "high-acid, mineral-linear whites where the soil conversation is primary. "
                       "The distinction: Chablis is ancient seabed; Pico is active volcanic Atlantic — "
                       "different mineral registers (chalk vs. basalt) but the same principle that "
                       "geology trumps everything else"},
        {"tradition": "wine", "beverage": "Rias Baixas Albariño (Galicia, Spain)",
         "connection": "The Atlantic wine triangle: Vinho Verde, Rias Baixas, and Azores all express "
                       "the Portuguese-Galician Atlantic climate through high-acid, mineral, lower-alcohol "
                       "whites. Azores adds the volcanic-saline dimension absent in both Vinho Verde and "
                       "Albariño. For a programme: all three represent the northern Atlantic coast "
                       "expression of white wine; the Azores is the most extreme — the open ocean "
                       "version of the same story"}
    ],
    "sensory_profile": {
        "appearance": "Pale gold to medium gold; crystalline clarity; some age-worthy examples "
                      "develop a distinctive greenish tint at youth; slow legs in the glass "
                      "from the relatively low alcohol (12–13% for Arinto; 12.5–13.5% for Verdelho)",
        "nose": "Arinto dos Açores: extraordinary mineral-saline opening (crushed basalt, sea air, "
                "iodine undertone); white flower, lemon zest, fresh lime, nectarine, "
                "green apple; Atlantic oceanic salinity persisting throughout. "
                "Verdelho: fuller — honey, melon, apricot — but always with the volcanic "
                "mineral base. Both: a quality that wine professionals describe as 'smelling "
                "wet basalt in sunshine at the ocean edge'.",
        "palate": "Arinto: electric acidity (malic-tartaric balance distinctive from mainland Arinto); "
                  "medium body; laser-precise mineral finish of extraordinary length; "
                  "flavour development: first citrus, then stone fruit, then sustained mineral-salinity. "
                  "Verdelho: more roundness; stone fruit more prominent; still high acidity and "
                  "basalt minerality; ages to develop a golden, nutty complexity with retained "
                  "freshness. Terras de Lava Arinto: one of the most distinctive white wines produced "
                  "anywhere in the Portuguese-speaking world.",
        "conclusion": "Azores wine is the PCT's most compelling argument for geographic specificity "
                      "in wine: no winemaking technique produces this mineral-volcanic-oceanic character. "
                      "For a serious wine programme, a Pico Arinto or Verdelho represents a "
                      "conversation no other wine region on earth can provide."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Terras de Lava / Cabeço do Monte — Premium Single Vineyard",
         "criteria": "Named estate; 100% basalt terroir; single variety Arinto or Verdelho; "
                     "aged 12–18 months on fine lees; DOC Pico or equivalent top classification",
         "markers": "Terras de Lava Arinto; Cabeço do Monte Reserve; Curral Atlântis Grande Escolha; "
                    "BC/US ~$35–55 (specialist Portuguese importers)"},
        {"tier": 3, "tier_name": "Adega do Pico — Estate Range",
         "criteria": "DOC Pico; estate Verdelho or Arinto; basalt terroir confirmed; clean winemaking",
         "markers": "Adega do Pico Escolha; Curral Atlântis; Lajido; BC/US ~$22–35"},
        {"tier": 2, "tier_name": "Cooperativa Standard DOC",
         "criteria": "DOC Pico or IGP Açores; cooperativa production; correct varietal character",
         "markers": "Adega Cooperativa do Pico standard range; Basalto; BC/US ~$16–22"},
        {"tier": 1, "tier_name": "IGP Açores / Commercial",
         "criteria": "Island origin; multi-island blend; entry to Azores character",
         "markers": "IGP Açores blends; Pico Branco standard; BC/US ~$12–16"}
    ],
    "service_intelligence": {
        "temperature": "10–12°C; young Arinto benefits from cold serving; aged Verdelho at 13–14°C",
        "vessel": "White wine glass (standard; Riedel Veritas or similar); "
                  "wider bowl for aged Verdelho to capture the honey-floral development",
        "technique": "Young Arinto: pour cold; allow 5 minutes to open in glass — the aromatic precision "
                     "unfolds in stages. Aged Verdelho (10+ years): open 30 minutes before serving. "
                     "Food pairing primary: the wine is built for the table, not solo sipping. "
                     "Serve alongside cold seafood for the basalt-meets-ocean effect.",
        "programme_position": "By-the-glass conversation wine: the story drives as much as the flavour. "
                              "Sommelier pairing feature for Atlantic seafood courses. "
                              "PCT geographical anchor: the same volcanic island chain that "
                              "launched Portuguese exploration.",
        "verbal_presentation": "Terras de Lava Arinto — Pico Island, Azores. UNESCO World Heritage viticulture. "
                               "Hand-harvested from basalt enclosures in the mid-Atlantic. "
                               "The most volcanic white wine in Europe."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Terras de Lava (Pico Island, founded 2002) and Adega Cooperativa do Pico",
        "producer_location": "Pico Island, Azores, Portugal",
        "key_person": "João Brum (Terras de Lava, winemaker); Luís Melo (Adega do Pico)",
        "production_volume": "Small: Azores produces fewer than 2,000 hectolitres annually — "
                             "the smallest DO region in Portugal by volume",
        "certifications": ["DOC Pico", "IGP Açores", "UNESCO World Heritage viticulture landscape (2004)"],
        "bc_distributor": "Private import only; no current BC commercial distributor confirmed; "
                          "BCLDB special order possible for cooperativa range (IGP Açores)",
        "us_distributor": "Ferreira Imports (Portuguese specialist, New York — carries Pico wines); "
                          "Premium Port Wines Inc. (San Francisco) occasionally lists Azores; "
                          "extremely limited US distribution overall",
        "uk_distributor": "Lea & Sandeman (London — UK importer for Terras de Lava); "
                          "The Wine Society; Bat & Bottle",
        "price_tier": "Market to Reserve (cooperativa standard: ~$18 US; Terras de Lava: ~$35–45 US)",
        "availability_notes": "Azores wine is among the most difficult Portuguese wines to source in "
                              "North America. US: Ferreira Imports, NY; Crush Wine & Spirits NY. "
                              "In BC: private import only through specialist order. "
                              "UK is the best-served non-European market for Azores wine."
    },
    "trail_connection": "PCT-3",
    "trail_note": "The Azores were the first mid-Atlantic Portuguese colonial settlement (1427) and "
                  "served as the primary restocking point for all Portuguese Atlantic voyages — "
                  "Columbus stopped in the Azores on his return from the Americas in 1493. "
                  "The Verdelho grape variety was cultivated in the Azores before it became the "
                  "primary Madeira variety — the PCT flows from Azores to Madeira, not the reverse. "
                  "The UNESCO heritage status (2004) protects the basalt currais wall viticultural "
                  "landscape that has remained essentially unchanged since the 15th century.",
    "food_pairings": [
        {"technique_id": "", "dish": "Percebes (goose barnacles) — North Atlantic",
         "pairing_type": "complement",
         "rationale": "Percebes from the Atlantic coast carry intense oceanic-mineral iodine character "
                      "that mirrors the Arinto dos Açores directly — the same ocean in two forms. "
                      "This is one of the few wine-and-food pairings where the mineral match "
                      "is so precise it reads as a single flavour system rather than a pairing"},
        {"technique_id": "", "dish": "Alcatra (Terceira Island slow-braised beef with red wine and allspice)",
         "pairing_type": "contrast",
         "rationale": "Azores' most iconic dish — braised beef in terracotta with Açores red wine, "
                      "allspice, bay, and cloves — pairs as contrast with the white: "
                      "the Arinto's electric acidity cuts the braised fat while the allspice "
                      "and clove find the wine's own spice-mineral undertone"}
    ],
    "source": "DOC Pico official production documentation; UNESCO World Heritage evaluation report 2004; "
              "Terras de Lava producer documentation; Adega Cooperativa do Pico official history; "
              "Wines of Portugal (viniportugal.pt) Azores regional guide",
})

session.commit_batch()
print(f"\n[BATCH 28 COMMITTED — Azores Pico Island Wine]\n")

# ============================================================
# AZORES TEA — PCT-3 (Gorreana)
# ============================================================

session.switch_region("tea", "Portugal — Azores (São Miguel Island)")

session.add_beverage({
    "tradition": "tea",
    "sub_tradition": "atlantic volcanic island tea",
    "region": "Portugal — Azores (São Miguel Island, Gorreana Estate)",
    "name": "Gorreana Estate Tea — Europe's Only Remaining Tea Plantation",
    "terroir_origin": (
        "Gorreana Tea Estate (Maia, São Miguel Island, Azores) is the only remaining tea "
        "plantation in Europe and one of the most historically significant agricultural "
        "curiosities in the Portuguese colonial world. Tea cultivation in the Azores began "
        "in 1874, introduced by Portuguese entrepreneur Jacinto Leite who imported tea "
        "plants from the Brazilian state of Rio de Janeiro — themselves descended from seeds "
        "obtained via Chinese trade contacts through the Portuguese colonial network in Macau "
        "and the Far East. The PCT connection is explicit: Azores tea exists because Portugal's "
        "commercial network connected Chinese tea cultivation (via Macau, PCT-10) to Atlantic "
        "island agriculture. At its peak in the early 20th century, São Miguel had seven tea "
        "estates. Gorreana (founded 1883) is the only survivor. "
        "The estate occupies 35 hectares on São Miguel's north coast at 300–450m elevation. "
        "The North Atlantic climate — consistent moisture, moderate temperatures (12–20°C), "
        "high humidity — is structurally similar to Darjeeling and Assam in the Himalayan "
        "foothills: the Atlantic and the monsoon create comparable tea-growing conditions "
        "through different mechanisms. The basalt volcanic soil of São Miguel adds a mineral "
        "character not found in Himalayan or Chinese tea terroirs."
    ),
    "production_technique": (
        "Gorreana produces both black and green teas entirely by hand and using Victorian-era "
        "machinery that has not been substantially modernised since the early 20th century. "
        "This is a deliberate heritage preservation: the estate uses rolling machines, "
        "drying ovens, and sorting trays from the 1900–1920 period, creating a production "
        "continuity that is unique in European food and beverage culture. "
        "Black tea production: withering (24 hours in Atlantic ocean air), rolling (copper "
        "drum rollers), fermentation/oxidation (3–4 hours), drying (hot air ovens, 90–95°C), "
        "sifting and grading. Grades: Broken Leaf, Orange Pekoe, Pekoe, Hysson (green). "
        "Green tea: withering, minimal rolling, steam-fixing to halt oxidation, drying. "
        "Harvest: mechanical hand-picking of the two-leaves-and-a-bud standard; "
        "three flushes annually (April–September). "
        "The Azores maritime climate means Gorreana tea does not produce the sharp seasonal "
        "first-flush variation of Darjeeling — instead, consistency across flushes is the "
        "hallmark of the Atlantic terroir. No pesticides have ever been used on the estate "
        "(certified organic 2001). The hand-sorting process removes stems and yellow leaves "
        "at multiple stages."
    ),
    "cross_tradition_parallels": [
        {"tradition": "tea", "beverage": "Darjeeling Second Flush (Himalayan black tea)",
         "connection": "Both Gorreana and Darjeeling Second Flush achieve complexity through cool-climate "
                       "slow maturation — Atlantic moisture versus Himalayan monsoon. Darjeeling's "
                       "muscatel (2-methylbutyraldehyde ester) character versus Gorreana's mineral-"
                       "Atlantic character represents the terroir contrast: altitude-mineral Himalayan "
                       "versus sea-level volcanic Atlantic. Neither has a direct parallel elsewhere. "
                       "Gorreana is the quieter wine; Darjeeling is the opera"},
        {"tradition": "wine", "beverage": "Azores Pico Island White (Arinto dos Açores)",
         "connection": "Gorreana tea and Pico wine are the two most singular expressions of Azores "
                       "agricultural terroir: both are made on basalt volcanic islands with extreme "
                       "Atlantic exposure; both carry the island's distinctive mineral-oceanic "
                       "signature. A Gorreana tea service alongside Pico Island wine creates the "
                       "complete Azores sensory narrative for a PCT programme — "
                       "one cold, one hot; both unmistakably of the same volcanic archipelago"}
    ],
    "sensory_profile": {
        "appearance": "Black tea brew: deep amber to copper-red; clear; no visible tannin clouding. "
                      "Green tea (Hysson): pale yellow-green; delicate; lighter than Chinese green teas. "
                      "Both: distinctly brighter colour than Darjeeling equivalents",
        "nose": "Black (Orange Pekoe): warm bread, light smoke, dried stone fruit, marine minerality "
                "(subtle — not present in inland teas), gentle tannin. "
                "Broken Leaf: stronger, earthier, more tannic. "
                "Green (Hysson): fresh grass, steamed artichoke, Atlantic sea air, lime leaf — "
                "the European jade: lighter than Chinese green tea with a distinctive marine note "
                "absent in all other tea traditions.",
        "palate": "Black: medium body; moderate tannin (lower than Assam or Ceylon); clean finish "
                  "with sustained mineral length. No added milk needed for balance — the Atlantic "
                  "terroir moderates tannin naturally. "
                  "Green: delicate; low astringency; the mineral-marine note most pronounced "
                  "on the mid-palate; clean dry finish. "
                  "The defining character of Gorreana: a mineral-saline depth that locates the "
                  "tea geographically — you can taste the ocean surrounding São Miguel.",
        "conclusion": "Gorreana is the most historically significant tea produced outside Asia. "
                      "For a serious beverage programme: serve Gorreana as the opening of a tea flight "
                      "with the provenance story (Portuguese Atlantic colonial trade, Victorian machinery, "
                      "only European tea estate). The sensory experience is distinctive; "
                      "the historical context is extraordinary."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Gorreana Orange Pekoe / Hysson Green (Estate Direct)",
         "criteria": "Certified organic; estate-direct sourcing; current vintage; hand-sorted; "
                     "Orange Pekoe grade or Hysson green",
         "markers": "Gorreana Orange Pekoe; Gorreana Hysson Green; estate-direct or European specialty "
                    "tea merchants; ~€8–15 per 100g"},
        {"tier": 3, "tier_name": "Gorreana Broken Leaf / Pekoe (Standard Grade)",
         "criteria": "Certified organic; Gorreana estate; Broken Leaf or standard Pekoe grade",
         "markers": "Gorreana Broken Leaf; Gorreana Pekoe; specialty tea retailers; ~€6–10 per 100g"},
        {"tier": 2, "tier_name": "Porto Formoso Estate (the other Azores tea estate)",
         "criteria": "The second surviving Azores tea operation (less recognised than Gorreana); "
                     "certified organic; São Miguel terroir",
         "markers": "Porto Formoso teas; also available direct from São Miguel; ~€8–12 per 100g"},
        {"tier": 1, "tier_name": "Azores Tea (blended/commercial)",
         "criteria": "Azores-origin tea in commercial packaging; correct Atlantic character but "
                     "less provenance specificity",
         "markers": "Commercial Azores tea gift packs; sold widely in the Azores; ~€4–8 per 100g"}
    ],
    "service_intelligence": {
        "temperature": "Black tea: 95°C water; 3–4 minutes steep. "
                       "Green (Hysson): 75–80°C water (do NOT use boiling — Atlantic green tea is "
                       "delicate and will turn bitter); 2–3 minutes steep.",
        "vessel": "White porcelain cup (essential for observing colour); "
                  "traditional Gorreana service uses the estate's own ceramic cups (available from estate). "
                  "Teapot: ceramic or earthenware; avoid metal which affects the mineral character.",
        "technique": "Black: steep 3.5 minutes, remove leaves — do not over-steep or tannin becomes dominant. "
                     "Serve plain first to identify the mineral-saline character before adding milk/sugar. "
                     "Green (Hysson): 2.5 minutes maximum; serve plain; the maritime note is most evident "
                     "in the first sip without additions. "
                     "Programme service: offer a Gorreana Orange Pekoe alongside Azores Pico wine as "
                     "the PCT Atlantic island flight — hot tea, cold wine, same volcanic terroir.",
        "programme_position": "Tea service anchor for PCT programme; historical narrative beverage; "
                              "afternoon service or paired with pastel de nata (Portuguese custard tart)",
        "verbal_presentation": "Gorreana Orange Pekoe — São Miguel, Azores. 1883. "
                               "The only tea estate in Europe. The Atlantic volcanic version of Darjeeling. "
                               "From the same Portuguese colonial trade network that brought tea "
                               "from Macau to the mid-Atlantic."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Gorreana Tea Estate (Maia, São Miguel Island, Azores, Portugal)",
        "producer_location": "Maia, São Miguel Island, Azores, Portugal",
        "key_person": "Ernesto Melo e Azevedo (current estate owner/manager, 5th generation family estate)",
        "production_volume": "Small — approximately 40,000kg annually from 35 hectares; "
                             "significantly constrained by hand production and Victorian machinery",
        "certifications": ["Certified Organic (2001)", "Protected Designation of Origin (European DOP)"],
        "bc_distributor": "No confirmed BC commercial distributor; specialty tea shops carry "
                          "(Lupicia, Silk Road Tea) via European import routes; also available direct "
                          "shipping from gorreana.pt to Canada",
        "us_distributor": "Arbor Teas (Ann Arbor, MI — confirmed organic specialty importer); "
                          "Simpson & Vail (Brookfield, CT — Portuguese specialty teas); "
                          "available direct from gorreana.pt to US",
        "uk_distributor": "Fortnum & Mason (London — stocks Gorreana as specialty provenance tea); "
                          "The Tea Makers of London; widely available via UK online specialty retailers",
        "price_tier": "Market (~€8–15 / 100g; specialty retail ~$14–22 CAD / 100g)",
        "availability_notes": "Most accessible via direct order from gorreana.pt (ships internationally). "
                              "In Vancouver: Murchie's Tea & Coffee (check availability); "
                              "Lupicia (Pacific Centre, Vancouver) — occasional Azores listing. "
                              "US: Arbor Teas national delivery. UK: Fortnum & Mason flagship."
    },
    "trail_connection": "PCT-3",
    "trail_note": "Gorreana tea exists because of the Portuguese colonial trade network: "
                  "Chinese tea cultivation (Macau, PCT-10) → Macanese botanical knowledge → "
                  "Brazilian colonial agricultural experiments → Azores island introduction (1874). "
                  "The Victorian-era machinery, hand-sorting processes, and organic certification "
                  "create a beverage with an unusually complete provenance narrative — from "
                  "15th-century Portuguese exploration to the 2001 organic standard, "
                  "all on the same 35-hectare basalt hillside.",
    "food_pairings": [
        {"technique_id": "", "dish": "Pastel de nata (Portuguese custard tart)",
         "pairing_type": "complement",
         "rationale": "The pastéis de nata + tea pairing is as canonical in Lisbon cafés as "
                      "croissant + coffee in Paris. Gorreana black tea's moderate tannin cuts the "
                      "egg-custard richness of the tart while the mineral undertone bridges "
                      "with the caramelised sugar crust — the PCT's most culturally embedded "
                      "food-beverage pairing, transported from Lisbon to the Azores and back"},
        {"technique_id": "", "dish": "Queijo São Jorge (Azores aged cow's milk cheese)",
         "pairing_type": "bridge",
         "rationale": "São Jorge DOP cheese (Azores — sharp, nutty, aged 7+ months) "
                      "and Gorreana black tea share the mineral-dairy register: "
                      "the tea's Atlantic minerality bridges with the cheese's "
                      "Azores pasture character. Both are from São Miguel-adjacent islands; "
                      "both carry the volcanic archipelago in their flavour structure"}
    ],
    "source": "Gorreana Tea Estate official history and production documentation (gorreana.pt); "
              "Azores DOP certification documentation; organic certification records (2001); "
              "UNESCO botanical heritage documentation (Azores colonial agriculture); "
              "Ernesto Melo e Azevedo estate interviews (multiple sources, 2015–2022)",
})

session.commit_batch()
print(f"\n[BATCH 29 COMMITTED — Azores Tea: Gorreana]\n")

# ============================================================
# TIMOR-LESTE COFFEE — PCT-11
# ============================================================

session.switch_region("coffee", "Timor-Leste — Ermera, Aileu, Ainaro")

session.add_beverage({
    "tradition": "coffee",
    "sub_tradition": "timor hybrid specialty coffee",
    "region": "Timor-Leste — Ermera District (Central Highlands)",
    "name": "Timor-Leste Coffee — Origin of the Timor Hybrid, Ermera Highlands",
    "terroir_origin": (
        "Timor-Leste (East Timor) is one of the most globally significant coffee origins "
        "in botanical history while remaining among the least-known in specialty markets. "
        "The reason: in approximately 1927, a spontaneous natural cross-pollination occurred "
        "on Timor between Coffea arabica and Coffea canephora (robusta) — the only documented "
        "natural arabica-robusta hybrid in coffee history. This plant, known as the "
        "'Timor Hybrid' (HdT — Híbrido de Timor), has resistance to coffee leaf rust "
        "(Hemileia vastatrix) that its arabica parent completely lacks. "
        "Beginning in the 1950s, Portuguese colonial botanical researchers identified and "
        "propagated the Timor Hybrid. It has since been used to breed virtually every "
        "major rust-resistant arabica variety now grown globally: Catimor, Sarchimor, "
        "Castillo (Colombia), Ruiru 11 (Kenya), Lempira (Honduras). "
        "The majority of coffee grown at altitude today contains Timor Hybrid genetics. "
        "Timor-Leste's Ermera district (central highlands, 1,000–1,800m altitude) produces "
        "washed, natural, and honey-process coffees from the original Timor Hybrid and its "
        "descendants. The PCT connection: Portugal colonised Timor-Leste in 1515 and maintained "
        "colonial control until 1975 — one of the longest continuous colonial relationships "
        "in history. Portuguese missionaries and colonial farmers introduced coffee cultivation "
        "to Ermera in the 19th century, initially growing Typica arabica before the spontaneous "
        "Timor Hybrid appeared. After Indonesian occupation (1975–1999) and independence (2002), "
        "Timor-Leste's coffee industry was rebuilt with NGO and international specialty "
        "buyer support as the country's primary export commodity."
    ),
    "production_technique": (
        "Timor-Leste coffee is produced primarily by smallholder farmers on plots of "
        "0.5–3 hectares in the central mountain highlands. "
        "Varieties: Timor Hybrid (HdT) and its Timorese selections; Typica (remaining "
        "original Portuguese introduction); some Catimor (a Timor Hybrid × Caturra cross). "
        "Processing: both washed (wet) and natural (dry) processing are practiced, "
        "with washed dominant for quality-focused production. Cooperativa Café Timor (CCT), "
        "founded 1994, is the primary organised producer group — a farmer cooperative "
        "with 24,000+ member households. CCT certifications: USDA Organic, Fairtrade. "
        "Wet-process stations: CCT operates centralised washing stations in Ermera, Aileu, "
        "and Ainaro districts; cherries pulped same day as harvest; fermented 24–48 hours in "
        "water; washed; dried on raised beds 12–20 days. "
        "Natural process: small-scale, farm-level; whole cherries dried on patios; "
        "producing fruit-forward, wine-like cup character. "
        "Harvest: May–August (dry season). Single-origin specialty lots from CCT "
        "are sourced by Intelligentsia Coffee (US), Specialty Coffee (UK), "
        "and multiple specialty roasters globally."
    ),
    "cross_tradition_parallels": [
        {"tradition": "coffee", "beverage": "Ethiopian Heirloom Varieties (Yirgacheffe, Sidama)",
         "connection": "Ethiopia is the birthplace of arabica coffee; Timor-Leste is the birthplace "
                       "of the rust-resistant hybrid that preserved arabica globally. Both are origin "
                       "stories without which modern coffee could not exist: Ethiopia provides the "
                       "genetic foundation; Timor provides the disease resistance that kept that "
                       "foundation from being destroyed by leaf rust. A flight including both origins "
                       "tells the complete story of arabica coffee's botanical survival"},
        {"tradition": "coffee", "beverage": "Colombian Castillo (Cenicafé cultivar)",
         "connection": "Colombia's Castillo variety — the commercial standard for most of Colombia's "
                       "6 million coffee-growing households — contains Timor Hybrid genetics in its "
                       "parentage (Timor Hybrid × Caturra → Catimor × Colombia → Castillo). "
                       "Every cup of Colombian Castillo is genetically linked to a spontaneous "
                       "cross on a Timorese hillside in 1927. "
                       "Tasting Timor-Leste alongside Castillo is tasting botanical ancestry"}
    ],
    "sensory_profile": {
        "appearance": "Medium brown; clarity varies by processing; washed: cleaner, brighter; "
                      "natural: slightly deeper with dried-fruit oils; crema moderate in espresso",
        "nose": "Washed Timor-Leste (CCT): earthy baseline characteristic of Timor Hybrid genetics — "
                "brown spice, cedar, dried herbs, mild tobacco; moderate brightness; "
                "dark chocolate; some brown sugar. "
                "Natural process: additional dried cherry, fig, winey complexity layered over the "
                "earthy base. The Timor Hybrid character is identifiable: "
                "heavier, earthier, more structured than pure Typica but less aggressive than robusta.",
        "palate": "Medium-to-full body (heavier than Ethiopian or Colombian heirloom arabica — "
                  "the robusta genetics give weight); moderate acidity; long, earthy finish; "
                  "dark chocolate and brown spice persistence; "
                  "washed: cleaner fruit definition; natural: winey and dried-fruit layering. "
                  "Best as espresso or Moka pot — the body structure responds well to pressure extraction. "
                  "Filter brewing reveals the cedar-herbal complexity characteristic of HdT parentage.",
        "conclusion": "Timor-Leste coffee will never be the most delicate or florally complex cup "
                      "in a flight — that is not what it is. It is the most historically important "
                      "coffee in a flight, and a skilled presentation makes that value tangible. "
                      "Pair it with Colombia's Castillo in a cupping: origins 13,000km apart, "
                      "botanically inseparable."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "CCT Single Origin Micro-Lot / Natural Process",
         "criteria": "Cooperativa Café Timor named-district micro-lot; natural or honey process; "
                     "current crop; specialty roaster sourced; SCA score 84+",
         "markers": "CCT Ermera Single District Natural; Intelligentsia Direct Trade lots; "
                    "specialty roasters with direct CCT sourcing; BC/US ~$20–32 per 250g"},
        {"tier": 3, "tier_name": "CCT Organic Fairtrade Standard",
         "criteria": "CCT Fairtrade + USDA Organic certified; washed process; Ermera or Aileu origin",
         "markers": "Cooperativa Café Timor standard certified bags; available at organic retailers; "
                    "BC/US ~$14–20 per 250g"},
        {"tier": 2, "tier_name": "Timor Coffee Company / Blended Timor",
         "criteria": "Commercial scale; Timor-Leste origin; correct Timor Hybrid character; "
                     "accessible pricing",
         "markers": "Timor Coffee Company blends; commercial Timor-origin bags; BC/US ~$10–14 per 250g"},
        {"tier": 1, "tier_name": "Timor-Leste Commodity Grade",
         "criteria": "Origin certified; commercial grade; espresso blend component",
         "markers": "Commodity Timor in commercial blends; not typically single-origin at this tier"}
    ],
    "service_intelligence": {
        "temperature": "93–96°C; slightly higher than Ethiopian for filter (the Timor Hybrid "
                       "body benefits from higher extraction temperature)",
        "vessel": "Cupping bowls for comparative tasting; V60 or Chemex for filter; "
                  "Moka pot or espresso for pressure extraction",
        "technique": "Espresso: 18g in, 36g out, 28–32 second extraction at 93°C — "
                     "the body structure of Timor Hybrid produces excellent espresso crema. "
                     "Cupping/comparison: brew Timor-Leste alongside Ethiopian Yirgacheffe and "
                     "Colombian Castillo — three origins representing the botanical triangle "
                     "of arabica coffee. The provenance story drives the experience. "
                     "Natural process: brew at slightly lower temperature (91°C) to "
                     "preserve the fruit character without amplifying the earthy base.",
        "programme_position": "Coffee education anchor; PCT provenance narrative; "
                              "most powerful in a comparative flight with CCT Organic direct trade story",
        "verbal_presentation": "Cooperativa Café Timor — Ermera, Timor-Leste. "
                               "Origin of the Timor Hybrid. The cross-pollination in 1927 that gave "
                               "resistance to every rust-susceptible coffee farm in the world. "
                               "500 years of Portuguese colonial history in a cup."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Cooperativa Café Timor (CCT) — 24,000 smallholder member households",
        "producer_location": "Ermera, Aileu, and Ainaro districts, Timor-Leste",
        "key_person": "CCT management (cooperative structure); Intelligentsia Coffee (key US specialty buyer)",
        "production_volume": "~10,000–15,000 metric tonnes annually (Timor-Leste national total); "
                             "specialty micro-lot: small allocation through Intelligentsia and specialty buyers",
        "certifications": ["USDA Organic (CCT)", "Fairtrade International (CCT)", "Rainforest Alliance (partial)"],
        "bc_distributor": "No dedicated BC commercial importer; "
                          "Kicking Horse Coffee (Invermere, BC) sources Timor-Leste for blends; "
                          "Salt Spring Coffee (BC) has sourced directly from CCT; "
                          "specialty roasters via Royal Coffee (Vancouver warehouse, Pacific importer)",
        "us_distributor": "Intelligentsia Coffee (Chicago — confirmed direct trade CCT partnership); "
                          "Royal Coffee (Oakland + Vancouver warehouse — confirmed Pacific importer); "
                          "Sustainable Harvest (Portland, OR — Fair Trade specialty importer)",
        "uk_distributor": "Union Hand-Roasted Coffee (London); Hasbean (Staffordshire); "
                          "Extract Coffee (Bristol); multiple specialty UK roasters source CCT directly",
        "price_tier": "Market (CCT standard ~$10–14/250g; micro-lot specialty ~$22–32/250g)",
        "availability_notes": "In BC: Salt Spring Coffee and Kicking Horse both carry or have carried "
                              "Timor-Leste. Royal Coffee's Vancouver warehouse is the most practical "
                              "BC access route for green bean purchasing. "
                              "US: Intelligentsia Café locations carry Timor-Leste single origin seasonally."
    },
    "trail_connection": "PCT-11",
    "trail_note": "Timor-Leste's coffee history spans the full Portuguese colonial arc: "
                  "Portuguese missionaries introduced Typica coffee cultivation to Ermera in the 1800s; "
                  "Portuguese colonial botanists documented and began propagating the spontaneous "
                  "Timor Hybrid in the 1950s; Indonesian occupation (1975–1999) disrupted but "
                  "did not destroy the coffee infrastructure. Post-independence, coffee is "
                  "Timor-Leste's largest export earner and the CCT cooperative — supported by "
                  "USAID and Fair Trade networks — has rebuilt the industry from the ground up. "
                  "The Timor Hybrid's global importance was not fully understood until the "
                  "1970s–1980s: the genetics that protect most of the world's coffee from "
                  "leaf rust are on every farm in Timor-Leste, waiting to be understood.",
    "food_pairings": [
        {"technique_id": "", "dish": "Batar daan (Timorese corn and bean stew with coconut milk)",
         "pairing_type": "complement",
         "rationale": "Timor-Leste's staple dish — dried corn, pumpkin, black-eyed peas, coconut — "
                      "shares the earthy, warm, starchy register of Timor Hybrid coffee. "
                      "The coffee's brown-spice and cedar character bridges with the coconut "
                      "and corn sweetness; the moderate acidity lifts the dish's starchy weight"},
        {"technique_id": "", "dish": "Dark chocolate (70–80% cacao, Santo Tomé or Peruvian origin)",
         "pairing_type": "complement",
         "rationale": "The Timor Hybrid's body-and-dark-chocolate character mirrors high-cacao "
                      "dark chocolate directly — the same earthy-bitter-dried-fruit register. "
                      "CCT espresso and 75% dark chocolate is a flavour doubling, not a contrast; "
                      "both are expressing the same tropical-origin weight through different forms"}
    ],
    "source": "Cooperativa Café Timor official documentation (ccttimor.com); "
              "World Coffee Research Timor Hybrid botanical documentation; "
              "Cenicafé (Colombia) Timor Hybrid genetics research; "
              "Intelligentsia Coffee direct trade documentation; "
              "Timor-Leste coffee industry reports (ITC Geneva 2019–2022); "
              "UNESCO Portuguese colonial Timor documentation",
})

session.commit_batch()
print(f"\n[BATCH 30 COMMITTED — Timor-Leste Coffee]\n")

# ============================================================
# SÃO TOMÉ & PRÍNCIPE — Fine Cacao/Ceremonial — PCT-6
# ============================================================

session.switch_region("ceremonial", "São Tomé & Príncipe — Cacao and Colonial Beverages")

session.add_beverage({
    "tradition": "ceremonial",
    "sub_tradition": "sao tome fine cacao drinking chocolate",
    "region": "São Tomé & Príncipe (Gulf of Guinea, Atlantic)",
    "name": "São Tomé Fine Cacao — Drinking Chocolate and the Colonial Sugar-Cacao Trade",
    "terroir_origin": (
        "São Tomé and Príncipe, two volcanic islands in the Gulf of Guinea off West Africa's coast, "
        "were uninhabited when Portuguese navigators arrived in 1470. The islands became the first "
        "Portuguese plantation economy — the template for the colonial agricultural model "
        "subsequently applied across Brazil, Angola, and the Indian Ocean colonies. "
        "Sugarcane was the first crop; enslaved West African workers were the first labour force. "
        "By 1550, São Tomé was the world's largest sugar producer. When Brazilian sugar overtook "
        "São Tomé production by 1600, the islands transitioned to a new cash crop: cacao. "
        "Cacao was introduced to São Tomé in the 1820s (seeds from Brazil — the same Portuguese "
        "colonial agricultural network operating in reverse: plant material moving from the "
        "Americas back to Africa via the PCT corridor). "
        "São Tomé's volcanic basalt terroir — equatorial heat (average 27°C), 1,500–3,000mm "
        "annual rainfall, Obô natural reserve forest cover — creates ideal cacao growing conditions. "
        "The primary cacao variety: Amelonado (Forastero subtype), old planted stock from "
        "19th-century introduction. Claudio Corallo, an Italian-Portuguese chocolatier who moved "
        "to São Tomé in the 1990s, grows and produces direct-from-plantation chocolate on the "
        "island at his Terreiro Velho estate — considered among the finest chocolate production "
        "in the world and the reference for São Tomé cacao character."
    ),
    "production_technique": (
        "São Tomé fine cacao production follows traditional Amelonado processing: "
        "Harvest: manual, year-round with peaks February–April and October–December. "
        "Fermentation: 5–7 days in wooden fermentation boxes; indigenous yeasts and bacteria "
        "from the forest environment. The Gulf of Guinea humidity and heat create active, "
        "complex fermentations that produce the fruity-acidic-floral character of premium "
        "São Tomé cacao. "
        "Drying: sun-drying on raised beds 7–14 days. The equatorial sun produces "
        "rapid drying without the extended time required in cooler origins. "
        "Claudio Corallo's method (Terreiro Velho estate): fermentation on the tree "
        "(selective harvest at precise ripeness); minimum-intervention fermentation; "
        "controlled drying; stone-ground on the island — no conching, no added lecithin. "
        "The resulting chocolate is intentionally 'rustic' with maximum terroir expression. "
        "Drinking chocolate tradition: São Tomé's Creole food culture (roça / plantation culture) "
        "includes a traditional hot cacao drink made from roasted, ground cacao beans, "
        "hot water, and palm sugar — the same preparation found in Aztec and Mayan traditions, "
        "introduced to West Africa via the Portuguese Atlantic trade."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Vintage Port (Douro Valley)",
         "connection": "São Tomé fine cacao and Vintage Port occupy the same position in their "
                       "respective categories: both are products of extreme terroir (volcanic island "
                       "vs. Douro schist), both carry the historical weight of the Portuguese colonial "
                       "trade system that created them, and both achieve complexity through "
                       "terroir-primary production philosophy. A tasting of Claudio Corallo "
                       "São Tomé chocolate with Vintage Port creates the PCT's most condensed "
                       "historical narrative: 500 years of Portuguese agriculture, two products, "
                       "one pairing"},
        {"tradition": "coffee", "beverage": "Ethiopia Heirloom Natural (Yirgacheffe/Guji)",
         "connection": "Ethiopian natural coffee and São Tomé fine cacao drinking chocolate share "
                       "the fermented-fruit-complexity register: both are beverages where controlled "
                       "fermentation of tropical agricultural raw material produces extraordinary "
                       "complexity. Both origins are African; both use indigenous microbial "
                       "fermentation; both resist standardisation and industrial processing "
                       "by the strength of their terroir character"}
    ],
    "sensory_profile": {
        "appearance": "São Tomé cacao drinking chocolate: deep brown-black; viscous; "
                      "no sheen (natural cacao fat without added lecithin); "
                      "served warm at 70–75°C in traditional ceramic or metal cups",
        "nose": "Claudio Corallo São Tomé: intensely fruity (dried cherry, blackcurrant, "
                "red wine); notable acidity on the nose (the Amelonado fermentation character); "
                "tobacco, dried mushroom, sea air, prune. "
                "Traditional Creole cacao drink: more roasted, less fermented complexity — "
                "deep toasted dark chocolate, slight bitterness, palm sugar sweetness, "
                "warm and earthy. Both express the same volcanic terroir through different "
                "preparation intensities.",
        "palate": "Claudio Corallo 75% drinking chocolate: extraordinary — the most complex "
                  "West African single-origin cacao. Bitter-fruity opening, then dried cherry "
                  "and red wine, then sustained tobacco-mineral finish. Acidic by chocolate "
                  "standards — the fermentation defines the flavour more than roasting. "
                  "Traditional cacao drink (light-roast ground cacao + water): thick, warming, "
                  "bitter-sweet; the agricultural version of the Aztec preparation that predates "
                  "all modern chocolate. Both: long finish, volcanic mineral depth.",
        "conclusion": "São Tomé fine cacao is the PCT's most emotionally complex beverage: "
                      "the same islands where the Portuguese first deployed the plantation-and-slavery "
                      "model now produce some of the world's finest chocolate. "
                      "The Claudio Corallo story — an Italian who chose to grow and make chocolate "
                      "on São Tomé rather than import the cacao elsewhere — is a modern counternarrative "
                      "to the plantation extraction history. "
                      "For a programme: serve as a flight-closing ceremonial element."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Claudio Corallo Estate São Tomé (Terreiro Velho)",
         "criteria": "Single estate; estate-processed; stone-ground; no additives; "
                     "Claudio Corallo label; 70–100% cacao content",
         "markers": "Claudio Corallo 75%, 80%, 100%; Terreiro Velho estate; limited international distribution; "
                    "~$15–25 per 50g bar; drinking chocolate preparation from bars"},
        {"tier": 3, "tier_name": "São Tomé Fine Cacao — Certified Single Origin",
         "criteria": "Certified single origin São Tomé; named producer or cooperative; "
                     "72%+ cacao content; bean-to-bar by quality chocolatier",
         "markers": "Valrhona Manjari (STP origin); Vintage Plantations São Tomé; "
                    "Pralus São Tomé; ~$8–14 per 50g bar"},
        {"tier": 2, "tier_name": "São Tomé Commercial Origin",
         "criteria": "São Tomé origin certified; commercial chocolatier processing; "
                     "correct terroir character but less complexity",
         "markers": "Barry-Callebaut São Tomé origin; commercial specialty chocolate bars; ~$5–8 per 50g"},
        {"tier": 1, "tier_name": "Gulf of Guinea Blend",
         "criteria": "West African origin (may include STP); commercial grade; "
                     "accessible introduction to the flavour profile",
         "markers": "Commercial West African chocolate; flavour profile accessible; ~$2–4 per 50g"}
    ],
    "service_intelligence": {
        "temperature": "Drinking chocolate (traditional cacao preparation): 70–75°C; "
                       "serve in warmed ceramic cup. Do NOT use milk — the traditional "
                       "preparation is water-based to allow the cacao terroir to express directly.",
        "vessel": "Small ceramic or earthenware cup (125–150mL); heavy base to retain heat",
        "technique": "Traditional cacao drink preparation: roast whole dried cacao beans 10 minutes "
                     "at 170°C; cool; peel shells; grind in mortar or food processor to coarse paste; "
                     "dissolve 2 tbsp paste in 150mL near-boiling water; add pinch of sea salt and "
                     "small amount of palm sugar or muscovado sugar; whisk until uniform. "
                     "Modern Corallo bar drinking chocolate: melt 15g Corallo 75% in 100mL warm "
                     "water at 70°C; no milk; no sugar; whisk smooth. "
                     "Programme service: offer as a closing ceremonial drink after a PCT tasting flight; "
                     "pair with a small piece of Claudio Corallo bar alongside.",
        "programme_position": "Ceremonial closing element for PCT beverage programme; "
                              "historical narrative anchor for the colonial Atlantic plantation system; "
                              "dessert pairing or standalone tasting experience",
        "verbal_presentation": "Claudio Corallo São Tomé — Terreiro Velho estate, Gulf of Guinea. "
                               "The islands where Portugal built the first plantation economy in history. "
                               "Cacao grown on the same volcanic soil, five centuries later."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Claudio Corallo (Terreiro Velho estate, São Tomé)",
        "producer_location": "Terreiro Velho, São Tomé Island, Democratic Republic of São Tomé & Príncipe",
        "key_person": "Claudio Corallo (founder; Italian chocolatier who relocated permanently to STP "
                      "in the 1990s; considered one of the world's finest fine chocolate producers)",
        "production_volume": "Very small — estate-scale; Claudio Corallo produces "
                             "fewer than 20 tonnes of finished chocolate annually",
        "certifications": ["São Tomé DOP cacao (partial)", "Artisanal production (estate-direct)"],
        "bc_distributor": "No dedicated BC distributor for Claudio Corallo; "
                          "Meinhardt Fine Foods (Vancouver) has carried Corallo bars; "
                          "specialty chocolate shops (Beta5 Chocolates Vancouver) sourced via European import; "
                          "Valrhona and Vintage Plantations STP origins more reliably available at "
                          "Thierry Chocolatier (Vancouver), Daniel Le Chocolat Belge",
        "us_distributor": "Corallo: select specialty retailers (Dean & DeLuca; Zingerman's Ann Arbor; "
                          "Formaggio Kitchen Boston); no national distributor confirmed. "
                          "Vintage Plantations São Tomé: Americas specialty chocolate distributors; "
                          "Valrhona USA (Manjari and similar STP origins)",
        "uk_distributor": "Claudio Corallo: Rococo Chocolates (London); Fortnum & Mason (occasional); "
                          "specialist fine chocolate merchants. Valrhona STP widely available UK.",
        "price_tier": "Reserve to Prestige (Corallo bars ~$20–28 CAD per 50g; "
                      "Valrhona/Vintage Plantations ~$8–12 per 50g; drinking chocolate preparation ~$5–10 per service)",
        "availability_notes": "Claudio Corallo is the most difficult PCT beverage to source in North America. "
                              "Most reliable: order direct from claudiocorallo.com (ships internationally). "
                              "In Vancouver: Meinhardt Fine Foods has carried; call ahead to confirm stock. "
                              "US: Zingerman's (zingermans.com) reliably carries Corallo; "
                              "Formaggio Kitchen (Boston, Cambridge MA) carries when available."
    },
    "trail_connection": "PCT-6",
    "trail_note": "São Tomé & Príncipe is the starting point for the entire PCT plantation model: "
                  "the Portuguese colonial agricultural template first deployed here in the 1480s — "
                  "forced labour, monoculture cash crops, offshore island plantation — "
                  "was subsequently replicated in Brazil (1500s), Angola (1600s), and Mozambique (1700s). "
                  "The cacao that Claudio Corallo grows on Terreiro Velho estate is the direct "
                  "descendant of seeds brought from Brazil in the 1820s by the same colonial "
                  "trade network that the 1480s plantation model made possible. "
                  "São Tomé fine cacao is the PCT's most compressed historical object.",
    "food_pairings": [
        {"technique_id": "", "dish": "Roasted coconut and cashew (São Tomé Creole tradition)",
         "pairing_type": "complement",
         "rationale": "São Tomé's Creole kitchen uses coconut and cashew from the same plantation-era "
                      "agricultural introduction that brought cacao. Roasted cashews with dark "
                      "cacao drinking chocolate mirrors the island's own flavour palette: "
                      "the cashew's sweet-roasted-nut character bridges with cacao's "
                      "bitter-fruity depth while the coconut fat on the palate "
                      "softens the cacao's pronounced acidity"},
        {"technique_id": "", "dish": "Vintage Port (Taylor Fladgate or Quinta do Noval)",
         "pairing_type": "bridge",
         "rationale": "The PCT's most historically resonant pairing: "
                      "São Tomé cacao drinking chocolate alongside Vintage Port "
                      "unites the Portuguese colonial trade system's two most important "
                      "agricultural products — cacao from the Gulf of Guinea and wine from the Douro — "
                      "both shaped by 500 years of Portuguese agricultural and commercial history. "
                      "The bridge is the shared dried-fruit and mineral character in both"}
    ],
    "source": "Claudio Corallo official production documentation (claudiocorallo.com); "
              "São Tomé colonial history (UNESCO; João de Barros, Décadas da Ásia, 1552); "
              "ICCO (International Cacao Organisation) São Tomé DOP documentation; "
              "Vintage Plantations origin documentation; "
              "William Gervase Clarence-Smith 'Cocoa and Chocolate 1765–1914'",
})

session.commit_batch()
print(f"\n[BATCH 31 COMMITTED — São Tomé & Príncipe Cacao]\n")

# ============================================================
# PRODUCERS
# ============================================================

session.add_producer({
    "name": "Terras de Lava (Pico Island Wines)",
    "location": "Pico Island, Azores, Portugal",
    "country": "Portugal",
    "region": "Pico Island DOC, Azores",
    "tradition": "wine",
    "key_person": "João Brum (winemaker and founder)",
    "founded": "2002",
    "production_volume": "Small artisanal — very limited international allocation",
    "notable_products": ["Terras de Lava Arinto dos Açores", "Terras de Lava Verdelho",
                         "Terras de Lava Reserve"],
    "certifications": ["DOC Pico", "UNESCO World Heritage viticulture landscape (site)"],
    "website": "terrasdelava.com",
    "philosophy": "Maximum expression of Pico Island volcanic basalt terroir through minimal-intervention "
                  "winemaking. João Brum works exclusively with native Azores varieties on basalt currais "
                  "vineyards at 50–200m altitude. Considered the benchmark for Azores wine globally.",
    "trail_connection": "PCT-3",
    "source": "Terras de Lava official documentation; Wines of Portugal Azores evaluation",
    "verified": True
})

session.add_producer({
    "name": "Gorreana Tea Estate",
    "location": "Maia, São Miguel Island, Azores, Portugal",
    "country": "Portugal",
    "region": "São Miguel Island, Azores",
    "tradition": "tea",
    "key_person": "Ernesto Melo e Azevedo (5th generation estate owner)",
    "founded": "1883",
    "production_volume": "~40,000kg annually from 35 hectares; smallest commercially significant "
                         "tea production in Europe",
    "notable_products": ["Gorreana Orange Pekoe", "Gorreana Broken Leaf", "Gorreana Hysson Green",
                         "Gorreana Pekoe"],
    "certifications": ["Certified Organic (2001)", "DOP Açores"],
    "website": "gorreana.pt",
    "philosophy": "The only remaining working tea estate in Europe. Victorian-era machinery "
                  "preserved in complete operational condition — the estate is simultaneously a "
                  "production facility and a living heritage museum. Organic certification "
                  "since 2001; no pesticides ever used. The PCT connection: Gorreana exists "
                  "because of Portugal's Macau-Brazil-Azores botanical trade network.",
    "trail_connection": "PCT-3",
    "source": "Gorreana Estate official documentation (gorreana.pt); Azores agricultural registry",
    "verified": True
})

session.add_producer({
    "name": "Claudio Corallo (Terreiro Velho, São Tomé)",
    "location": "Terreiro Velho estate, São Tomé Island, São Tomé & Príncipe",
    "country": "São Tomé & Príncipe",
    "region": "São Tomé Island, Gulf of Guinea",
    "tradition": "ceremonial",
    "key_person": "Claudio Corallo (Italian founder; relocated permanently to STP from Italy)",
    "founded": "1990s (Terreiro Velho cacao estate)",
    "production_volume": "Fewer than 20 tonnes of finished chocolate annually — very small estate",
    "notable_products": ["Corallo Cacao 75% São Tomé", "Corallo Cacao 80%", "Corallo Cacao 100%",
                         "Corallo Nibs São Tomé"],
    "certifications": ["Artisanal estate-direct production"],
    "website": "claudiocorallo.com",
    "philosophy": "Farm-to-bar in the most literal sense: Corallo grows, ferments, dries, roasts, "
                  "and stone-grinds on the same São Tomé estate. No conching, no added lecithin, "
                  "no vanilla. The Amelonado cacao from Terreiro Velho expresses volcanic Gulf of "
                  "Guinea terroir at its most unmediated. Considered by many fine chocolate experts "
                  "as producing the finest single-terroir chocolate in the world.",
    "trail_connection": "PCT-6",
    "source": "Claudio Corallo official documentation (claudiocorallo.com); "
              "multiple fine chocolate review sources",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 32 COMMITTED — Azores + STP Producers]\n")

print(session.finish())
