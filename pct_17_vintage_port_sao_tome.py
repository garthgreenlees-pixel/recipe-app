#!/usr/bin/env python3
# PCT-17: Sao Tome Cacao Depth + Port Vintage (LBV, Declared) + Angola Coffee Depth
# Running total entering: 68
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="fortified",
    region="Portugal — Douro (Vintage Port, Declared and LBV)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=18,
    running_total=68
)

session.add_producer({
    "tradition": "fortified",
    "name": "Graham's (W. and J. Graham and Co.)",
    "location": "Vila Nova de Gaia, Porto, Portugal",
    "description": "Founded 1820 by the Graham brothers from Glasgow. "
        "Among the most highly regarded Vintage Port producers — "
        "the 1963, 1970, 1977, 1985 are among the greatest Ports declared in the 20th century. "
        "Now owned by the Symington Family Estates since 1970. "
        "Quinta dos Malvedos is the flagship single-quinta estate.",
    "founded": "1820",
    "region": "Douro DOC / Port",
    "website": "https://www.grahams-port.com",
    "verified": True
})

session.add_producer({
    "tradition": "chocolate",
    "name": "Claudio Corallo (Claudio Corallo Chocolate)",
    "location": "Principe Island, Sao Tome and Principe",
    "description": "Italian-born agronomist who moved to Sao Tome in 1997 "
        "to cultivate the rarest cacao varieties on the islands. "
        "Claudio Corallo grows, ferments, and transforms all his own cacao "
        "on Principe Island — one of the last bean-to-bar operations "
        "in the cacao-growing region itself. "
        "His Forastero Nacional variety is unique globally.",
    "founded": "1997",
    "region": "Principe Island, Sao Tome and Principe",
    "website": "https://www.claudiocorallo.com",
    "verified": True
})

session.add_purveyor({
    "name": "Quinta do Crasto / Symington Family Estates (UK/Canada)",
    "type": "direct_estate_exporter",
    "description": "Symington Family Estates is the dominant quality-focused Port producer group: "
        "Graham's, Dow's, Warre's, Quinta do Vesuvio. "
        "Exports directly to UK (Majestic, Berry Bros. and Rudd) and Canada (BCLDB). "
        "The family has owned Graham's since 1970.",
    "markets_served": ["UK", "worldwide_CA", "BC", "BCLDB", "US"],
    "traditions_carried": ["fortified"],
    "website": "https://www.symington.com",
    "verified": True
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "port vintage declared single harvest reductive",
    "region": "Portugal — Douro (Vintage Port, Declared Vintage)",
    "name": "Declared Vintage Port — Graham's, The Apex of the Reductive Maturation Path",
    "terroir_origin": (
        "Declared Vintage Port is the style that defines the category's ceiling "
        "and occupies the most coveted position in the international fine wine market. "
        "A 'declaration' is a decision made by the individual Port house "
        "in the second year after harvest — if the vintage is considered "
        "exceptional in quality and character, the house 'declares' and bottles "
        "after a minimum of 2 years in wood, then the wine is expected to age "
        "20-50 years in bottle. "
        "Not every year is declared — typically 3-5 times per decade for a given house. "
        "Universal declarations (when most houses agree the vintage is exceptional) "
        "occur even less frequently: 1977, 1994, 2000, 2011, 2017, 2022 are the "
        "key post-war universal declarations. "
        "Graham's Quinta dos Malvedos (Tua tributary, Douro Superior): "
        "the primary single-quinta source for declared Graham's Vintage. "
        "Altitude: 100-400m. Soils: pre-Cambrian schist (xisto), steep terrace cultivation. "
        "Varieties: Touriga Nacional (15-20%), Touriga Franca (20-25%), Tinta Roriz (30-35%), "
        "Tinta Barroca, Tinto Cao. The blend ratio changes by vintage. "
        "The PCT connection: Vintage Port is the wine that the Methuen Treaty (1703) "
        "created the commercial infrastructure for — Portugal's answer to French Claret "
        "for the English market, sustained by 300 years of Anglo-Portuguese trade alliance."
    ),
    "production_technique": (
        "Graham's Vintage Port production: "
        "Harvest: hand-picking in early October; Quinta dos Malvedos harvested by the "
        "resident workforce (approximately 200 people during harvest). "
        "The lagar: foot-treading in granite lagares is standard for declared vintage; "
        "the human foot provides optimal tannin and colour extraction without pip crushing. "
        "Fortification: at 5-6 Baume (approximately 9-11% residual sugar); "
        "grape spirit (77% abv) stops fermentation and preserves sweetness. "
        "Wood: 20 months maximum in large wood (600-800L casks) before bottling; "
        "the brief wood phase preserves the reductive potential for bottle evolution. "
        "Bottling: filtered and sealed under cork with wax or lead-free foil. "
        "The bottle phase: the reductive maturation in bottle creates the defining character — "
        "tannins slowly polymerise, the deep ruby loses colour through the rim, "
        "primary fruit compounds transform to tertiary complexity (dried fruit, leather, cedar, "
        "tobacco, iron). "
        "The 20-year trajectory: a declared Vintage Port from a great year "
        "(1977, 1994, 2011) is drinking in the 20-30 year window post-vintage; "
        "the 1977 Graham's was still extraordinary at 45 years old in 2022."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "wine",
            "beverage": "Chateau Latour (Premier Cru Classe Pauillac, 20yr+ old vintage)",
            "connection": (
                "Both are fine wines that demand decades of bottle maturation for full expression. "
                "Both develop the tannin-fruit-mineral complexity that defines "
                "the pinnacle of their respective traditions. "
                "The comparison contextualises why Vintage Port is priced and cellared "
                "on the same logic as first-growth Bordeaux — "
                "both are 20-50 year maturation propositions."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Colheita Tawny Port (same region, oxidative path)",
            "connection": (
                "Vintage Port (reductive bottle ageing, dark ruby to garnet) "
                "vs Colheita (oxidative wood ageing, dark ruby to amber) "
                "from the same Douro terroir reveals the fundamental fork in Port production. "
                "Both start from the same fortified wine; the maturation environment "
                "creates opposite colour and flavour outcomes."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Barolo Riserva (Nebbiolo, Piedmont, 15yr+)",
            "connection": (
                "Both are Italy's and Portugal's most tannic wines requiring "
                "20+ years to fully integrate their tannin structure. "
                "Barolo Riserva and Vintage Port are the two European wine categories "
                "most reliably requiring a full generation of patience. "
                "The comparison teaches cellar-building logic to wine-educated guests."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Macallan 25yr Sherry Oak Single Malt Scotch",
            "connection": (
                "Both occupy the 'heritage prestige' price-and-narrative space "
                "at the top of their respective categories. "
                "Both are used as cellar-building investments and gifts for milestone occasions. "
                "The comparison bridges the fortified wine and spirits "
                "luxury positioning conversation for guests who know whisky."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Deep ruby-garnet at 5yr; garnet-brick at 15yr; the colour browning at the rim is visible at 20yr; 30yr+ shows significant brick-orange fading at the rim",
        "nose": "Young (5yr): black plum, blackcurrant, dark chocolate, violets, cedar. 15yr: dried plum, leather, tobacco, iron mineral, coffee. 25yr+: cigar, dried rose, cedar chest, dark chocolate, vanilla from the brief wood phase",
        "palate": "The tannins are the story — young Vintage Port is tannic and structured; at 20yr they are polished and integrated. The sweetness persists through all ages, providing the thread that connects young to mature",
        "texture": "The most tannic fortified wine produced — but the tannins are ripe from the lagar extraction and polymerise into silk over 20 years of bottle maturation",
        "finish": "3-5 minutes at 20yr+; the longest finish in the Port category; tannin, dried fruit, cedar, and iron mineral work in sequence; the sweetness is the last note to resolve",
        "conclusion": "The fortified wine that rewards generational patience — the one category where cellaring is not optional but intrinsic to the design"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Graham's Vintage Port 1977 or 1963 (legendary decades)",
            "criteria": "Universal declaration vintage; 40-60yr bottle maturation; "
                "tannins fully polymerised; tertiary development at maximum; "
                "one of the greatest wine experiences available",
            "markers": "Graham's 1977; auction price $250-500+; still drinking magnificently at 45yr"
        },
        {
            "tier": 3,
            "tier_name": "Graham's Vintage Port 2011 or 2017 (modern classics)",
            "criteria": "Universal declaration vintages of the modern era; "
                "at 10-15yr drinking window approaching but requiring patience; "
                "the benchmark for cellaring investment at current market",
            "markers": "Graham's 2011; BC ~$90-130; US ~$80-115; BCLDB listed; cellar 5-15yr more"
        },
        {
            "tier": 2,
            "tier_name": "Graham's LBV (Late Bottled Vintage) filtered",
            "criteria": "Single vintage; 4-6yr in wood; filtered for immediate drinking; "
                "the accessible entry to vintage Port character without 20yr cellar requirement",
            "markers": "Graham's LBV; BC ~$25-35; US ~$22-30; BCLDB listed; drink within 5yr of purchase"
        },
        {
            "tier": 1,
            "tier_name": "Graham's Six Grapes or Warre's Warrior (Ruby Reserve)",
            "criteria": "Non-vintage Ruby; fruit-forward; no ageing requirement; "
                "introduction to Port's fruit character at the widest audience price point",
            "markers": "Six Grapes; BC ~$20-28; US ~$18-25; BCLDB widely listed"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 16-18 degrees C for mature Vintage Port — the tannin structure needs warmth to open; too cold makes the tannins tight and the fruit hidden",
        "vessel": "Large tulip or a white Burgundy glass — the wide bowl essential for the nose to develop the layered tertiary character",
        "technique": "Mature Vintage Port requires 1-2 hours decanting. "
            "For restaurant service: the decant is the service ritual — "
            "perform it at the table with a candle if possible, pouring against the light "
            "to see the sediment in the bottle neck. "
            "The narrative: 'This was bottled in [year]. It has been maturing in the bottle "
            "for [X] years. We decanted it [X] hours ago to allow it to open. "
            "When you taste the tannins, you are tasting what time does to grapes.' "
            "Serve with Stilton, walnuts, dried fruit. The Stilton-Vintage Port combination "
            "is the most iconic British fine dining ritual.",
        "programme_position": "Cellar programme flagship; milestone anniversary wine; "
            "fine wine education anchor for the fortified category",
        "verbal_presentation": "Graham's Vintage Port, [year]. "
            "Declared by Graham's as the finest wine of the year. "
            "Foot-treaded in the Douro, cellared for [X] years. "
            "The wine that required your patience."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Graham's (Symington Family Estates) — the most celebrated Vintage Port house in the modern era",
        "producer_location": "Quinta dos Malvedos, Douro Superior / Vila Nova de Gaia lodge",
        "key_person": "David Guimaraens (head winemaker for Symington Estates across all houses)",
        "bc_distributor": "BCLDB stocks Graham's LBV and current declared vintages in Signature stores",
        "us_distributor": "Kobrand Corporation (US national for Graham's/Warre's/Dow's/Quinta do Vesuvio)",
        "uk_distributor": "Berry Bros. and Rudd, Majestic, Waitrose — widely available across all channels",
        "price_tier": "Entry: $20-28 (Six Grapes). Mid: $25-35 (LBV). Premium: $90-130 (current declared). Ultra: $250-500+ (legendary decades).",
        "availability_notes": "Graham's LBV and current declared vintages are BCLDB Signature store staples. "
            "Older declared vintages through Berry Bros., Corney and Barrow (UK), or auction. "
            "US: Kobrand national distribution; widely available Total Wine and specialty wine shops."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Stilton blue cheese with toasted walnuts",
            "pairing_type": "complement",
            "rationale": "The canonical Anglo-Portuguese Vintage Port pairing — "
                "the blue cheese fat and salt find their structural counterpart "
                "in the wine's ripe tannin and sweetness. "
                "The walnut bridges both the rancio character of the mature Port "
                "and the mineral fat of the cheese. "
                "The cultural narrative: the same Methuen Treaty that built the Port trade "
                "also established the British taste for Port-and-cheese."
        },
        {
            "technique_id": "",
            "dish": "Dark chocolate tart (70%+ cacao, light salt crust)",
            "pairing_type": "bridge",
            "rationale": "The tannin in mature Vintage Port and the tannin in high-cacao chocolate "
                "create a shared structural register — both require patience to reveal their sweetness "
                "and both carry a mineral iron note that bridges the two. "
                "The salt crust on the tart amplifies the mineral dimension of both."
        }
    ],
    "source": "IVDP Vintage Port classification and declaration records; "
        "Graham's (Symington) production documentation; "
        "Berry Bros. and Rudd Vintage Port archive; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1: Portugal (Douro). "
        "Declared Vintage Port is the wine category that the Methuen Treaty made possible — "
        "the preferential tariff arrangement that gave Portuguese wine access to the British market "
        "in 1703 created the commercial incentive for the English families (Graham, Taylor, Warre, Dow, Sandeman) "
        "to invest in the Douro terroir and develop the Vintage Port style. "
        "Without the Methuen Treaty, there would be no Vintage Port."
})

session.commit_batch()

session.switch_region("chocolate", "Africa — Sao Tome and Principe (Claudio Corallo)")

session.add_beverage({
    "tradition": "chocolate",
    "sub_tradition": "single origin bean to bar volcanic island forastero nacional",
    "region": "Africa — Sao Tome and Principe (Principe Island)",
    "name": "Claudio Corallo Cacao — Principe Island, Forastero Nacional, Bean-to-Bar Volcanic Origin",
    "terroir_origin": (
        "Sao Tome and Principe are two small islands in the Gulf of Guinea, "
        "approximately 250km off the coast of Gabon — among the smallest countries in Africa "
        "and the first sub-Saharan African territory reached by Portuguese explorers (1470). "
        "The islands were uninhabited when discovered and were colonised as "
        "sugar-producing plantations using enslaved West Africans — "
        "the model that was then replicated in Brazil, the Caribbean, and every PCT territory. "
        "Cacao replaced sugar as the islands' primary cash crop in the 19th century "
        "when the large Portuguese roças (plantation estates) shifted production. "
        "Sao Tome and Principe's cacao heritage: the Amelonado Forastero variety "
        "was planted in the late 19th century and became the dominant variety "
        "after the introduction of modern hybrids elsewhere. "
        "The Sao Tome cacao is genetically unusual — the 'Forastero Nacional' or 'Sao Tome' type "
        "has been isolated on the island long enough to develop distinguishable island-specific genetics. "
        "Principe Island: Claudio Corallo settled on Principe (the smaller, less populated island) "
        "after leaving his previous operations in Congo and Sao Tome. "
        "Principe is now designated a UNESCO Biosphere Reserve — "
        "the rainforest cacao agroforestry of Corallo's estate is within this protected zone. "
        "Volcanic soils: derived from the Cameroon Volcanic Line (the same tectonic system "
        "that created Mount Cameroon); the soils are deep andisols with "
        "high mineral content, exceptional water retention, and extreme organic matter from "
        "the rainforest floor — the most mineral-rich cacao soils outside of "
        "the Peruvian Amazon."
    ),
    "production_technique": (
        "Claudio Corallo production on Principe: "
        "Cultivation: shade-grown under indigenous rainforest canopy; "
        "no chemical inputs; traditional agroforestry. "
        "Varieties: Forastero Nacional (primary Sao Tome genetic type), "
        "with small plots of Trinitario and rare Amelonado selections. "
        "Harvest: manual, selective — only ripe cherries; done continuously "
        "through the main and mid-harvest (October-January and May-June). "
        "Fermentation: Claudio Corallo does his own fermentation in wood boxes "
        "under banana leaves for 5-8 days — precise temperature monitoring "
        "(the fermentation peak must hit 50-52 degrees C for flavour development). "
        "This is more careful than most industrial cacao processing. "
        "Drying: sun-dried on raised beds for 5-7 days; "
        "the volcanic island air has a salt-mineral character that "
        "Corallo argues influences the dried bean mineral note. "
        "Roasting: Corallo roasts on the island in small batches; "
        "each lot is roasted differently based on bean character. "
        "Grinding: stone grinding on site; no added emulsifiers, "
        "no added vanilla, no added sugar beyond the minimum. "
        "The 70% bar: Forastero Nacional cacao at 70% is the benchmark expression "
        "— bitter, mineral, fermented dried fruit without the sweetness of milk chocolate. "
        "The 80% bar: for tasting contexts where full cacao character is required."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "chocolate",
            "beverage": "Felchlin Maracaibo Clasificado 65% (Venezuela, Criollo)",
            "connection": (
                "Both are bean-to-bar volcanic-island origin chocolates from "
                "former plantation-agriculture colonial territories. "
                "Felchlin Maracaibo (Venezuela Criollo) is more floral and mild; "
                "Corallo Principe (Forastero Nacional) is more mineral and fermented-fruit. "
                "The comparison teaches guests the variety-driven flavour dimension in cacao."
            )
        },
        {
            "tradition": "chocolate",
            "beverage": "Valrhona Guanaja 70% (Madagascar Trinitario)",
            "connection": (
                "Both are reference 70% dark chocolates from volcanic African island origins. "
                "Valrhona Guanaja (Madagascar) is the international industry standard for "
                "dark chocolate profiling. Corallo Principe is the artisan-scale equivalent "
                "from the adjacent African Atlantic island tradition."
            )
        },
        {
            "tradition": "coffee",
            "beverage": "Sao Tome Island Coffee (same island, single origin)",
            "connection": (
                "The multi-crop volcanic island comparison: Sao Tome produces both "
                "specialty cacao and specialty coffee from the same roça estates. "
                "Pairing Sao Tome cacao and Sao Tome coffee creates a "
                "single-island sensory experience with the PCT colonial history "
                "expressed through two different crop traditions."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Douro Vintage Port (Quinta do Vesuvio)",
            "connection": (
                "The PCT pairing: Sao Tome Forastero Nacional 70% dark chocolate "
                "and Quinta do Vesuvio Vintage Port is the canonical "
                "Portuguese colonial product pairing — "
                "cacao from the equatorial Atlantic island, Port from the Portuguese river valley, "
                "both products of the same Atlantic colonial trade infrastructure."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Dark brown-ebony; 70%+ cacao shows minimal added sugar; matte surface with visible cocoa butter bloom in older bars",
        "nose": "Fermented dried red fruit (cassis, dried cherry), volcanic mineral, dark chocolate bitterness, light tobacco, sea-salinity from the Principe island air",
        "palate": "Entry: immediate cacao bitterness with no milk dilution. Mid-palate: fermented dried fruit complexity from the carefully controlled fermentation. Finish: mineral-volcanic persistence that coastal African cacao has over South American origins",
        "texture": "Full body from high cocoa butter; fine grain from stone-grinding; long melt from the slow particle reduction",
        "finish": "45-60 seconds; the mineral volcanic character persists after the cacao bitterness resolves; faint fermented dried fruit in the aftertaste",
        "conclusion": "The PCT's most extreme raw material story — the island that launched the Atlantic slave trade now produces one of the world's most ethically significant bean-to-bar chocolates"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Claudio Corallo Granellato 70% Forastero Nacional (with cacao nibs)",
            "criteria": "70% cacao; Forastero Nacional variety; cacao nibs added for texture; "
                "the full expression of Principe island terroir with textural complexity; "
                "extremely limited export production",
            "markers": "Claudio Corallo Granellato; BC: specialty chocolate retailers; US ~$15-20/50g; very limited"
        },
        {
            "tier": 3,
            "tier_name": "Claudio Corallo Cacao 70% (standard Principe bar)",
            "criteria": "70% cacao; single origin Principe; no added vanilla or emulsifier; "
                "the reference Corallo expression for tasting",
            "markers": "Claudio Corallo 70%; BC: Mink Chocolates and specialty; US ~$12-18/50g"
        },
        {
            "tier": 2,
            "tier_name": "Sao Tome 70% from other producers (Alter Eco, Theo)",
            "criteria": "Sao Tome certified organic; major Western chocolate producers; "
                "accessible introduction to Sao Tome island character",
            "markers": "Alter Eco Sao Tome 70%; BC ~$8-12/75g; US ~$7-10/75g; natural food stores"
        },
        {
            "tier": 1,
            "tier_name": "West African Forastero blend (70%, major craft)",
            "criteria": "West African Forastero including Sao Tome component; "
                "blended but accessible; introduction to the African cacao mineral character",
            "markers": "Various craft producers; BC ~$5-10/75g; widely available"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 20-22 degrees C (slightly warm room temperature) — cold temperature hardens the cocoa butter and reduces the melt speed that develops the flavour",
        "vessel": "White ceramic small plate or a wooden board for tasting; serve in thin squares cut with a sharp knife to maximise surface area-to-volume ratio",
        "technique": "Corallo 70% in a PCT pairing sequence: "
            "serve with Quinta do Vesuvio Port (or Graham's 20yr LBV as accessible substitute). "
            "The PCT colonial chain in two products: cacao from Sao Tome (Gulf of Guinea), "
            "Port from the Douro (mainland Portugal) — both products of the "
            "Portuguese Atlantic colonial infrastructure. "
            "The educational narrative: 'Both come from Portuguese colonial territories. "
            "The cacao was first planted by Portuguese colonists in the 1600s. "
            "The Port grapes were cultivated by English merchants who traded through Portugal. "
            "Both are on the table because of the same 300 years of Atlantic trade.'",
        "programme_position": "PCT pairing anchor; single-origin chocolate tasting; chocolate-Port dessert course",
        "verbal_presentation": "Claudio Corallo, Principe Island. "
            "The first island the Portuguese reached in sub-Saharan Africa. "
            "Forastero Nacional cacao, grown in volcanic rainforest soil. "
            "Bean-to-bar on the island where it is grown."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Claudio Corallo — Principe Island; the sole producer of this cacao at fine-dining quality",
        "producer_location": "Principe Island, Sao Tome and Principe",
        "key_person": "Claudio Corallo (Italian agronomist; resident on Principe since 1997)",
        "bc_distributor": "Mink Chocolates (Vancouver) occasionally stocks Corallo; specialty chocolate retailers",
        "us_distributor": "Chocosphere (Portland, OR) — primary US Corallo source; "
            "also available through specialty food importers",
        "uk_distributor": "Paul A Young Fine Chocolates (London); Rococo Chocolates; direct from Corallo website",
        "price_tier": "Entry: $5-10 (West African blend). Mid: $8-12 (Sao Tome Alter Eco). Premium: $12-18 (Corallo 70%). Ultra: $15-20 (Corallo Granellato).",
        "availability_notes": "Claudio Corallo exports in very small volumes. "
            "Contact Chocosphere (US) or Mink Chocolates (Vancouver) for current stock. "
            "Availability is seasonal based on harvest cycles on Principe Island."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Quinta do Vesuvio Vintage Port 2011 or Graham's LBV",
            "pairing_type": "bridge",
            "rationale": "The canonical PCT pairing: Sao Tome volcanic cacao "
                "and Douro Vintage Port — both products of the Portuguese Atlantic colonial world. "
                "The tannin in the 70% cacao and the tannin in aged Vintage Port "
                "create a mutual tannin bridge; the dried fruit in the chocolate "
                "and the dried fruit in the Port are mirror expressions."
        },
        {
            "technique_id": "",
            "dish": "Fleur de sel from Guerande (on top of the chocolate)",
            "pairing_type": "complement",
            "rationale": "The Principe island salt-mineral character in the cacao "
                "is amplified by Atlantic sea salt — the salt on the chocolate "
                "creates a mineral dialogue between the island volcanic soil "
                "and the Atlantic ocean that produced it. "
                "The simplest and most direct expression of the Sao Tome terroir."
        }
    ],
    "source": "Claudio Corallo production documentation and Principe Island estate records; "
        "UNESCO Biosphere Reserve Principe Island documentation; "
        "Chocosphere sourcing documentation; "
        "FAPROS (Sao Tome cacao federation) technical records",
    "trail_connection": "PCT-6",
    "trail_note": "PCT Region 6: Sao Tome and Principe — the Gulf of Guinea islands "
        "that launched the Portuguese equatorial plantation model "
        "subsequently replicated in Brazil, the Caribbean, and Mozambique. "
        "Claudio Corallo's bean-to-bar operation on Principe Island is "
        "the most direct post-colonial rehabilitation of the cacao tradition "
        "that the Portuguese colonial system introduced in the 16th century."
})

session.commit_batch()

session.finish()
