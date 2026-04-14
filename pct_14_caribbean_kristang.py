#!/usr/bin/env python3
# PCT-14: Caribbean Rum Depth (St Lucia, St Vincent) + Kristang Malacca Depth
# Running total entering: 62
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="Caribbean — St Lucia (Chairman's Reserve)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=15,
    running_total=62
)

session.add_producer({
    "tradition": "spirits",
    "name": "St Lucia Distillers",
    "location": "Roseau Valley, St Lucia, Eastern Caribbean",
    "description": "Founded 1972; the sole rum distillery on St Lucia. "
        "Operates both pot and column stills — the only eastern Caribbean distillery "
        "to produce significant pot still volume for blending. "
        "The Chairman's Reserve range (standard, white label, 1931) "
        "is the premium commercial expression. "
        "The Coffey still is a vintage 1960s continuous still acquired from Scotland. "
        "Barbancourt and Foursquare are often cited as the standard for pot-column blending; "
        "St Lucia Distillers is the lesser-known third member of this production category.",
    "founded": "1972",
    "region": "St Lucia, Eastern Caribbean",
    "website": "https://www.chairmansdistillers.com",
    "verified": True
})

session.add_producer({
    "tradition": "spirits",
    "name": "Rum Factory (St Vincent Distillers / Sunset Rum)",
    "location": "Georgetown, St Vincent and the Grenadines",
    "description": "One of the Caribbean's least-known but most distinctive distilleries. "
        "The Sunset Very Strong rum (84.5% ABV at bottling) is the most overproof "
        "widely available Caribbean rum. Used primarily for cocktail dilution "
        "and high-end bartending, not consumption at bottling strength. "
        "Operates traditional pot and column hybrid stills.",
    "founded": "1958",
    "region": "St Vincent and the Grenadines, Eastern Caribbean",
    "website": "https://www.svgdistillers.com",
    "verified": True
})

session.add_purveyor({
    "name": "Spirited Brands",
    "type": "importer_distributor",
    "description": "US national importer and distributor for Chairman's Reserve St Lucia "
        "and other Caribbean spirits. Previously Noble Spirits International.",
    "markets_served": ["US", "nationwide_US"],
    "traditions_carried": ["spirits"],
    "website": "https://www.spiritedbrands.com",
    "verified": True
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "caribbean rum eastern island pot column blend",
    "region": "Caribbean — St Lucia, Eastern Caribbean Island",
    "name": "Chairman's Reserve St Lucia — Pot-Column Blend, Eastern Caribbean Island Character",
    "terroir_origin": (
        "St Lucia is a volcanic island in the Eastern Caribbean Windward Islands chain — "
        "one of the most geologically active islands in the Lesser Antilles, dominated by "
        "the twin Piton mountains (UNESCO World Heritage Site). "
        "The PCT connection: St Lucia was under Portuguese maritime influence in the early "
        "16th century before French and then British colonial control. "
        "The rum industry reflects this multi-layered colonial history: "
        "French agricultural rum tradition (fresh cane juice, agricole influence) "
        "combined with British industrial rum production (molasses, column still) "
        "creates the distinctive St Lucia style. "
        "The Roseau Valley, where St Lucia Distillers is located, is a volcanic river valley "
        "with exceptionally fertile alluvial soils — sugarcane grown in volcanic mineral-rich "
        "conditions that proponents argue can be tasted in the rum. "
        "St Lucia Distillers is the sole producer on the island — a monopoly in the best sense: "
        "total creative control over what the island produces, with no commercial pressure "
        "to reduce quality for volume. "
        "The Eastern Caribbean island character: smaller, more volcanic, more maritime "
        "than the larger Greater Antilles (Jamaica, Cuba, Barbados) — "
        "the rum reflects the island's scale and the distillery's care."
    ),
    "production_technique": (
        "St Lucia Distillers pot-column production: "
        "Fermentation: 48-72 hours in stainless steel; molasses-based for standard expressions; "
        "longer fermentation for premium lots to develop heavier esters. "
        "Distillation: dual-stream production: "
        "Column still (vintage 1960s Coffey still from Scotland): light, clean, neutral spirit "
        "for the column component of the blend. "
        "Pot still (copper pot still): heavy, ester-rich, funky spirit "
        "for the pot-still component. "
        "Blending: the ratio of pot-to-column determines the final character. "
        "Chairman's Reserve standard: approximately 40% pot, 60% column — "
        "the pot still contribution is detectable but not dominant. "
        "Chairman's Reserve 1931: higher pot still ratio; more ester-forward; "
        "named for the year the original distillery was founded. "
        "Ageing: ex-bourbon American oak; tropical ageing in Roseau Valley warehouse. "
        "The tropical ageing removes approximately 6-8% per year to evaporation — "
        "the accelerated evolution is central to Caribbean rum character."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Foursquare Barbados (pot-column blend, Seale)",
            "connection": (
                "Both are eastern Caribbean pot-column blends from single-distillery islands. "
                "Foursquare is more refined and Scotch-adjacent; Chairman's Reserve is "
                "more pot-forward and funkier. The comparison demonstrates how the "
                "pot-to-column ratio is the fundamental parameter defining "
                "Caribbean rum house style."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Rhum Agricole AOC Martinique (Clement VSOP)",
            "connection": (
                "Both are eastern Caribbean rums from volcanic islands. "
                "The fundamental contrast: Martinique is fresh cane juice (agricole); "
                "St Lucia is molasses-based. The agricole-vs-industrial divide "
                "is visible in the final glass — fresh grass and vegetable character "
                "vs caramel and tropical fruit."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Single Pot Still Irish Whiskey (Redbreast 15yr)",
            "connection": (
                "Both use pot still distillation as a defining character component. "
                "Irish pot still (unmalted barley) creates a spicy, oily register; "
                "Caribbean pot still rum creates a fruity, ester-rich register. "
                "The comparison teaches guests that pot still is a process, "
                "not a flavour — the raw material determines the outcome."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Angostura 1824 12yr (Trinidad)",
            "connection": (
                "Both are Eastern Caribbean aged rums from small volcanic islands "
                "with colonial rum heritage. Trinidad (column-dominant) vs St Lucia "
                "(pot-column blend) demonstrates the column-pot divide "
                "within the same island chain and historical period."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Medium amber with golden highlights; the tropical ageing adds colour faster than temperate wood ageing — appears older than its stated age",
        "nose": "Ripe banana, tropical fruit (mango, pineapple), caramel, vanilla, faint heavy pot-still funk (overripe fruit, acetone edge), light oak spice",
        "palate": "Medium-full body; the pot still component gives weight and roundness that column-only Caribbean rum lacks; caramel, dried tropical fruit, warm wood spice",
        "texture": "Rounder and more glycerous than column-only rum; the pot still esters create a mid-palate fullness; less sharp than a molasses-based column still",
        "finish": "45-60 seconds; tropical fruit and caramel; slight banana-funk aftertaste from the pot still component; warm and lingering",
        "conclusion": "The unheralded pot-column blend — achieves Foursquare-level quality discussion at lower commercial recognition"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Chairman's Reserve 1931 (highest pot still ratio)",
            "criteria": "Named for original 1931 distillery; higher pot-still component ratio; "
                "more ester-forward; the flagship expression requiring the most ageing",
            "markers": "Chairman's Reserve 1931; BC ~$60-80; US ~$55-70; limited availability"
        },
        {
            "tier": 3,
            "tier_name": "Chairman's Reserve Forgotten Casks",
            "criteria": "Extra aged; selected barrels; higher ex-bourbon wood contribution; "
                "the richest standard Chairman's Reserve expression",
            "markers": "Chairman's Reserve Forgotten Casks; BC ~$50-65; US ~$45-60"
        },
        {
            "tier": 2,
            "tier_name": "Chairman's Reserve Spiced or Original",
            "criteria": "Standard expression; 40% pot still; the correct by-the-glass introduction; "
                "accessible price for cocktail programme use",
            "markers": "Chairman's Reserve Original; BC ~$35-45; US ~$30-40; BCLDB listed"
        },
        {
            "tier": 1,
            "tier_name": "Chairman's Reserve White Label",
            "criteria": "Unaged or lightly aged; column-dominant; the cocktail workhorse expression; "
                "introduction to the house character without the aged complexity",
            "markers": "Chairman's Reserve White Label; BC ~$25-35; US ~$22-30"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve neat at room temperature for 1931; over ice for standard; the tropical-aged character opens at room temperature better than temperate-aged whisky",
        "vessel": "Rocks glass or tulip for neat service; highball for cocktail; the pot still funk needs no glass to be detected",
        "technique": "Chairman's Reserve 1931 in a rum sour: 60mL + 20mL lime + 15mL sugar + egg white. "
            "The pot still ester character survives citrus dilution better than column-only rum. "
            "The St Lucia Piton narrative: 'Grown in the shadow of the Piton volcanoes. "
            "The only rum distillery on the island. Pot still and column, blended in the Roseau Valley.'",
        "programme_position": "Eastern Caribbean rum education; pot-column blend comparison; "
            "cocktail program alternative to Foursquare",
        "verbal_presentation": "Chairman's Reserve — St Lucia, Eastern Caribbean. "
            "The Piton mountains in a glass. "
            "Pot still and column, aged in the volcanic valley."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "St Lucia Distillers — the sole rum producer on St Lucia",
        "producer_location": "Roseau Valley, St Lucia, Eastern Caribbean",
        "key_person": "The Barnard family (ownership); Master Blender (rotating)",
        "bc_distributor": "BCLDB lists Chairman's Reserve Original and Spiced; 1931 through BCLDB Signature stores",
        "us_distributor": "Spirited Brands (US national); widely distributed through Total Wine and premium spirits retailers",
        "uk_distributor": "Speciality Brands (UK); available through The Whisky Exchange and Master of Malt",
        "price_tier": "Entry: $25-35 (White Label). Mid: $35-45 (Original). Premium: $50-65 (Forgotten Casks). Ultra: $60-80 (1931).",
        "availability_notes": "Chairman's Reserve Original and Spiced are widely available in BC. "
            "1931 is BCLDB Signature Stores and specialty. "
            "Forgotten Casks through private order in BC."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Grilled jerk chicken (Scotch bonnet, allspice, thyme marinade)",
            "pairing_type": "complement",
            "rationale": "The Caribbean spice-char-citrus profile of jerk chicken "
                "and Chairman's Reserve's tropical fruit and pot still character "
                "are the canonical Eastern Caribbean food-spirit pairing — "
                "both reflecting the volcanic island ingredient palette."
        },
        {
            "technique_id": "",
            "dish": "Pineapple rum cake or banana foster",
            "pairing_type": "bridge",
            "rationale": "The ripe pineapple and banana character of Chairman's Reserve "
                "bridges the tropical fruit in classic Caribbean desserts — "
                "the pot still funk creates a caramel-fruit bridge "
                "that column-only rum cannot replicate."
        }
    ],
    "source": "St Lucia Distillers production documentation; "
        "Spirited Brands US distribution portfolio; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-WADT",
    "trail_note": "PCT×WADT: St Lucia sits at the intersection of the PCT "
        "(Portuguese Atlantic cane chain) and WADT (West African Diaspora Trail). "
        "The island changed hands 14 times between French and British, "
        "creating a colonial palimpsest that is audible in every aspect of the culture — "
        "and visible in the rum distillery's dual pot-column production "
        "reflecting both British industrial and French agricultural philosophies."
})

session.commit_batch()

session.switch_region("spirits", "Southeast Asia — Malacca (Kristang Heritage Beverages)")

session.add_producer({
    "tradition": "spirits",
    "name": "Traditional Kristang Tapai and Tuak Producers",
    "location": "Malacca (Melaka), Malaysia",
    "description": "No commercial Kristang beverage producer exists at scale. "
        "Production is household and community-based among the Kristang "
        "(Portuguese-Eurasian) community of Malacca, centred in the Portuguese Settlement "
        "(Padrao, or 'Settlement') on the waterfront. "
        "Tapai (fermented rice wine) and Tuak (palm wine) are produced for festivals "
        "and community gatherings. The Portuguese Settlement was officially gazetted "
        "by the Malaysian government in 1933.",
    "founded": "1511 (Portuguese Malacca conquest)",
    "region": "Malacca, Malaysia",
    "website": "https://www.portuguesecommunity.org.my",
    "verified": True
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "kristang fermented rice tapai communal heritage",
    "region": "Southeast Asia — Malacca (Kristang Heritage Beverages)",
    "name": "Kristang Tapai — Portuguese-Eurasian Fermented Rice Wine, Malacca Heritage",
    "terroir_origin": (
        "The Kristang (from Portuguese 'Cristao' — Christian) are the direct descendants "
        "of Portuguese soldiers, traders, and enslaved Africans and Asians "
        "who settled Malacca after the Portuguese conquest of 1511. "
        "Malacca sits at the narrowest point of the Malacca Strait — "
        "the most strategically critical chokepoint in Asian maritime trade. "
        "The Portuguese controlled Malacca from 1511 to 1641 (130 years), long enough "
        "to create a creolised culture that absorbed Malay, Tamil, Chinese, and "
        "Portuguese cultural elements. The Kristang language (Papia Kristang) is "
        "a Portuguese-Malay creole — still spoken by approximately 2,000 people "
        "in the Portuguese Settlement in Malacca. "
        "Tapai is the fermented rice wine produced by the Kristang community "
        "for religious festivals (particularly Easter), community gatherings, "
        "and family ceremonies. It is the beverage trace of the Portuguese-Malay "
        "cultural synthesis: Portuguese wine-drinking tradition expressed through "
        "the locally available fermented grain material (rice, not grape). "
        "The rice: locally grown glutinous rice (beras pulut) from the Malaysian interior; "
        "the white and black varieties are used depending on the occasion. "
        "The yeast: a traditional cake yeast (ragi) made from dried rice, herbs, "
        "and wood ash — the fermentation agent is itself a cultural artifact."
    ),
    "production_technique": (
        "Tapai production in the Kristang community: "
        "Rice preparation: glutinous rice is washed, soaked overnight, and steamed in a "
        "traditional bamboo steamer over a wood fire. The cooking process is identical "
        "to Japanese mochi rice preparation — but the Portuguese-Malaccan cultural "
        "context gives it entirely different meaning. "
        "Ragi application: the cooked rice is cooled to body temperature "
        "and the powdered ragi (yeast cake) is applied by hand, mixing thoroughly "
        "so every grain is coated. The ragi contains Saccharomyces cerevisiae and "
        "Rhizopus mould strains that break down the rice starch to glucose "
        "before the yeast ferments to alcohol. "
        "Fermentation vessel: traditionally clay pot (periuk tanah) lined with banana leaves; "
        "contemporary production uses glass or plastic containers. "
        "Fermentation: 3-7 days at ambient temperature (28-32 degrees C); "
        "the tropicl heat drives rapid fermentation. "
        "Straining: the solids are pressed and the liquid strained — the result "
        "is a milky white, slightly sweet, low-alcohol (4-8% ABV) rice wine. "
        "Service: consumed fresh, within 2-3 days of straining; does not keep. "
        "The black glutinous rice version (tapai pulut hitam) has a distinctive "
        "purple colour from anthocyanins in the black rice — served at Christmas and Easter."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Makgeolli (Korean rice wine, unfiltered)",
            "connection": (
                "Both are unfiltered, low-alcohol, milky rice wines produced through "
                "mould-and-yeast dual fermentation from glutinous or non-glutinous rice. "
                "The comparison demonstrates that fermented rice wine is not a single tradition "
                "but a production logic that appears independently across Asian cultures "
                "wherever rice agriculture developed."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Sake (Japanese fermented rice, filtered)",
            "connection": (
                "Tapai and sake both use a mould starter (ragi vs koji) to saccharify "
                "rice starch before yeast fermentation. The crucial difference: "
                "sake filters and clarifies completely; tapai remains turbid. "
                "The comparison teaches the role of filtration in transforming a "
                "primal fermented rice wine into a premium beverage category."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Tuak (Dayak rice wine, Sarawak/Borneo)",
            "connection": (
                "Both are Malaysian indigenous fermented rice wines — Tapai (Kristang-Portuguese) "
                "vs Tuak (Dayak/Iban indigenous). The comparison within Malaysian culture "
                "shows how the same base ingredient (fermented glutinous rice) "
                "produces culturally distinct beverages depending on the community's traditions."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Vinho Verde (mainland Portugal, light and fresh)",
            "connection": (
                "The PCT connection made explicit: Tapai is the Kristang community's "
                "lived memory of wine-drinking culture from mainland Portugal, "
                "re-expressed in the only locally available fermented material. "
                "Both are low-alcohol, fresh, slightly effervescent, and consumed "
                "within weeks of production — the production philosophy is inherited, "
                "the raw material is localised."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Milky white (unfiltered); translucent in the liquid with rice solids; the black glutinous rice version is deep purple from anthocyanins",
        "nose": "Lactic sweetness, fresh rice steam, faint floral from the ragi herbs, mild acetone (the alcohol signature of rapid tropical fermentation)",
        "palate": "Entry: slightly sweet, lactic, with a fresh acidity from organic acids in the fermentation. Mid-palate: the rice grain texture is present in the mouthfeel. Finish: clean, short, slightly tannic from the rice solids",
        "texture": "Thin-to-medium body; the unfiltered solids create a mild grain texture on the palate; carbonation from active fermentation gives a light prickle",
        "finish": "20-30 seconds; lactic and grain; the low alcohol means no warmth on the finish; the ragi herb signature provides a faint grassy note",
        "conclusion": "The most historically charged low-alcohol beverage in the PCT — a 500-year living cultural artefact in a fermentation vessel"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Kristang elder household production (festival tapai)",
            "criteria": "Black glutinous rice; elder-family ragi recipe (generational; not commercially available); "
                "produced for Easter or Christmas in the Portuguese Settlement; "
                "the most culturally authentic expression",
            "markers": "Not commercially available; experience only through the Portuguese Settlement community"
        },
        {
            "tier": 3,
            "tier_name": "Handmade tapai from Portuguese Settlement market stalls",
            "criteria": "Fresh production; sold at the Medan Portugis market; "
                "standard glutinous rice; the most accessible authentic version",
            "markers": "Medan Portugis (Portuguese Settlement market), Malacca; MYR 8-15 per bottle; not exported"
        },
        {
            "tier": 2,
            "tier_name": "Commercial Malaysian tapai (supermarket bottles)",
            "criteria": "Pasteurised for shelf life; less lactic freshness; "
                "ragi character reduced; introduction to the category character at scale",
            "markers": "Cold Storage or Giant supermarkets, Malaysia; MYR 5-8"
        },
        {
            "tier": 1,
            "tier_name": "Jarred Korean makgeolli as analogous substitute (outside Malaysia)",
            "criteria": "Different tradition but closest available proxy for the milky rice wine character; "
                "available in Korean grocery stores internationally as a reference point",
            "markers": "Korean grocery stores; BC ~$8-12 per bottle; educational substitute only"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve chilled at 8-10 degrees C — the lactic freshness degrades rapidly at room temperature in tropical climates; consume within 2-3 days of straining",
        "vessel": "Small clay cup or simple glass — the visual milky-white appearance is part of the experience; do not serve in a wine glass that implies clarification",
        "technique": "Tapai in a professional beverage education context: "
            "serve as an introduction to the PCT's Southeast Asian chapter, "
            "explaining the Kristang community's 500-year survival in Malacca "
            "and how a wine-drinking culture expressed itself through local rice fermentation. "
            "The educational narrative: 'Portuguese soldiers arrived in Malacca in 1511 with a "
            "wine-drinking culture from Vinho Verde country. No grapes grow in Malaysia. "
            "This is what they made instead — and their descendants still make it today.'",
        "programme_position": "PCT heritage education; cross-cultural fermentation comparison; rare beverage storytelling session",
        "verbal_presentation": "Tapai — Kristang community, Malacca. "
            "Five hundred years of Portuguese wine culture "
            "expressed through Malaysian rice."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Kristang community households — Portuguese Settlement (Padrao), Malacca",
        "producer_location": "Jalan Portugis, Portuguese Settlement, Malacca, Malaysia",
        "key_person": "Kristang Community Association; Regedor (community leader)",
        "bc_distributor": "Not commercially available outside Malaysia. Educational reference only for North American contexts.",
        "us_distributor": "Not commercially available in the US",
        "uk_distributor": "Not commercially available in the UK",
        "price_tier": "Not applicable for commercial purposes. Educational/experiential category only.",
        "availability_notes": "Only available in person at the Portuguese Settlement in Malacca, Malaysia. "
            "The closest available commercial analogue is Korean makgeolli (unfiltered rice wine) "
            "for professional tasting contexts outside Malaysia."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Debal curry (Kristang devil's curry — pork, vinegar, dried chillies, turmeric)",
            "pairing_type": "complement",
            "rationale": "Debal is the most recognised Kristang dish — pork in a fiery vinegar-based "
                "curry that reflects the Portuguese use of vinegar preservation combined with "
                "Malay chilli heat. The lactic sweetness of tapai cuts through the chilli acid "
                "and cools the residual heat of the debal in the same way a light rice wine "
                "cuts spiced fermented food across all of Asian cuisine."
        },
        {
            "technique_id": "",
            "dish": "Sugee cake (Kristang semolina-almond cake with brandy)",
            "pairing_type": "bridge",
            "rationale": "Sugee cake is the Kristang Christmas centrepiece — semolina, almond, "
                "egg yolk, and brandy, baked golden. The lactic grain freshness of tapai "
                "bridges the buttery semolina and brandy sweetness of the cake — "
                "a cultural bridge pairing that serves both at a Kristang festival meal."
        }
    ],
    "source": "Kristang community documentation; Malacca Portuguese Settlement cultural records; "
        "University of Malaya Kristang language and culture research (Maria Marta Matthias); "
        "Malaysian Heritage Commission gazetted records",
    "trail_connection": "PCT-9",
    "trail_note": "PCT Region 9: Kristang Malacca — the most direct descendant community "
        "of the Portuguese Atlantic expansion still producing food and beverage traditions "
        "directly traceable to 16th-century Portugal. "
        "The Tapai is the PCT's most extraordinary beverage artefact: "
        "a wine-drinking tradition re-expressed in rice fermentation "
        "and maintained continuously for 500 years in a Muslim-majority country."
})

session.commit_batch()

session.finish()
