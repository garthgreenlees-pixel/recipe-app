#!/usr/bin/env python3
# PCT-19: Goa Feni Depth (Cashew + Coconut) + Sula/Grover Indian Wine + Quinta das Carvalhas
# Running total entering: 72
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="spirits",
    region="India — Goa (Feni, Cashew and Coconut Traditional Spirits)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=20,
    running_total=72
)

session.add_producer({
    "tradition": "spirits",
    "name": "Cazulo Premium Feni",
    "location": "Siolim, North Goa, India",
    "description": "The leading artisan Cashew Feni producer in Goa. "
        "Cazulo (founded 2017) was the first Goa Feni producer to pursue "
        "GI-quality standards, single-village sourcing, and premium positioning. "
        "The production: traditional bhaati still (clay pot) from Siolim village, "
        "with 40-year-old cashew orchards in laterite-soil North Goa. "
        "Cazulo markets internationally as the 'Champagne of India' — "
        "a claim based on the GI status awarded to Goa Feni in 2009.",
    "founded": "2017",
    "region": "North Goa, India",
    "website": "https://www.cazulo.com",
    "verified": True
})

session.add_producer({
    "tradition": "wine",
    "name": "Sula Vineyards",
    "location": "Nashik Valley, Maharashtra, India",
    "description": "Founded 1999 by Rajeev Samant (Stanford MBA, ex-Oracle). "
        "The largest and most internationally recognised Indian wine producer. "
        "The Nashik Valley winery is the destination wine tourism site in India. "
        "Sula produces Chenin Blanc (the dominant variety), Shiraz, Riesling, "
        "Sauvignon Blanc, and sparkling wine. "
        "The 2023 IPO makes Sula the first publicly traded Indian wine company.",
    "founded": "1999",
    "region": "Nashik Valley, Maharashtra, India",
    "website": "https://www.sulawines.com",
    "verified": True
})

session.add_purveyor({
    "name": "Santra Beverages (US) / Feni Imports India",
    "type": "importer",
    "description": "US importer of Goa Feni and Indian spirits. "
        "Cazulo Feni is available through a small number of specialty importers "
        "in the US as GI-protected Indian spirits gain international market access.",
    "markets_served": ["US", "UK"],
    "traditions_carried": ["spirits"],
    "website": "https://www.cazulo.com",
    "verified": True
})

session.add_beverage({
    "tradition": "spirits",
    "sub_tradition": "goa feni cashew pot still clay bhaati single distillation gi",
    "region": "India — Goa (Cashew Feni, North Goa Laterite Orchards)",
    "name": "Cashew Feni GI — Goa's Portuguese-Origin Clay Pot Still Spirit, GI Protected",
    "terroir_origin": (
        "Cashew Feni (from the Hindi feni, meaning 'froth') is the most direct "
        "Portuguese colonial beverage legacy in India. "
        "The Portuguese introduced the cashew tree (Anacardium occidentale) "
        "to Goa from Brazil in the 16th century — the cashew is native to coastal Brazil "
        "and was brought to Goa as part of the Portuguese global botanical exchange. "
        "This is the PCT loop: "
        "Brazil (cashew native) → Portugal (colonial botanical transfer) → Goa (cashew planted) "
        "→ Feni (distillation of cashew apple juice using Portuguese alembic methods) "
        "→ GI-protected Indian spirit. "
        "The cashew apple: the fruit surrounds the cashew nut; in Goa, "
        "the apple (not the nut) is the raw material for Feni. "
        "The cashew apple juice ferments rapidly in the Goa monsoon heat "
        "and is then distilled. "
        "North Goa terroir: laterite (ferricrete) soil — the iron-rich red soils "
        "that underlie most of Goa's coastal terrain. "
        "Laterite is extremely well-drained; cashew trees thrive in these "
        "mineral-rich, low-fertility conditions that other crops cannot tolerate. "
        "The 40-year-old cashew orchards at Cazulo's Siolim source: "
        "older trees produce less yield but more concentrated juice. "
        "GI Protection (2009): Feni was the first Indian alcoholic beverage "
        "to receive Geographical Indication protection — the Indian legal equivalent "
        "of the Portuguese DOP or French AOC."
    ),
    "production_technique": (
        "Traditional Cashew Feni production: "
        "Harvest: manual picking of ripe cashew apples in March-May "
        "(the hot, dry pre-monsoon season); the cashew nut is removed; "
        "only the apple is used for Feni. "
        "Pressing: traditional foot-treading in stone troughs (identical to "
        "Port wine lagare foot-treading — the Portuguese production method "
        "transplanted directly to Goa). "
        "Fermentation: 2-3 days at ambient temperature (30-35 degrees C); "
        "wild yeast from the laterite orchard soil. "
        "The first distillation (Urrac): cashew apple wash distilled in a "
        "clay pot still (bhaati) on a wood fire; produces a spirit at "
        "approximately 15% ABV. "
        "The second distillation (Feni): the Urrac is redistilled for "
        "the final Cashew Feni at 40-45% ABV; "
        "the clay pot still adds a distinctive clay-mineral character. "
        "Cazulo production: the traditional bhaati still from Siolim village, "
        "60+ year old clay pot still in continuous use; "
        "single-village sourcing; no additives; vintage-dated bottles. "
        "Coconut Feni (separate tradition): derived from the toddy of the "
        "coconut palm flower — an entirely different raw material and process."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "spirits",
            "beverage": "Mezcal Espadin (Oaxaca, Mexico — agave clay pot distillation)",
            "connection": (
                "Both are clay pot still spirits from pre-industrial traditions. "
                "Both use the clay vessel as an active participant in the distillation — "
                "the clay imparts mineral character to the spirit. "
                "Both have GI or DO protection as indigenous regional spirits. "
                "The comparison teaches that clay pot distillation is a "
                "global pre-industrial technology, not an exoticism."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Grogue Fogo (Cape Verde, fresh cane juice copper pot still)",
            "connection": (
                "Both are Portuguese colonial pot still spirits from tropical territories "
                "where the Portuguese alembic tradition was transplanted. "
                "Grogue uses copper; Feni uses clay. "
                "Both produce fresh-agricultural spirits from local raw materials "
                "using the same inherited pot still logic."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Calvados Pays d'Auge AOC (apple brandy, Normandy)",
            "connection": (
                "Both are fruit distillates — Calvados from apple, Feni from cashew apple. "
                "Both are GI-protected regional spirit traditions whose raw material "
                "is an agricultural fruit that requires no added sugar for fermentation. "
                "The apple-cashew apple comparison opens the 'fruit spirit' category "
                "to tropical and non-European raw materials."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Soju (Korean rice spirit, modern column distillation)",
            "connection": (
                "Both are the dominant traditional spirit of their respective countries "
                "(Feni in Goa; Soju in Korea) consumed in a culture-specific social context. "
                "The comparison shows how two completely different raw materials "
                "(cashew apple vs rice/sweet potato) fill the same cultural role "
                "of the 'national spirit' in two different Asian drinking cultures."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Crystal clear at bottling; faint ivory tinge in older expressions; some unfiltered examples show a slight haze from the clay still contact",
        "nose": "Fresh cashew apple (tropical, lightly fermenty, faint funk), clay mineral from the bhaati still, citrus-skin dryness, faint cooked apple, earthy-tropical ferment",
        "palate": "Entry: dry, light to medium body; the cashew character is distinct from any other fruit spirit — tropical without sweetness. Mid-palate: the clay mineral character from the bhaati still adds a dry stone note. Finish: clean and short, with a light cashew-nut oil aftertaste",
        "texture": "Light body; the cashew apple juice produces a lighter spirit than molasses or grain bases; the clay still adds a dry mineral mid-palate instead of oiliness",
        "finish": "25-40 seconds; clean and mineral; the cashew apple dryness is the defining final note; no sweetness residual",
        "conclusion": "The PCT's most explicit agricultural circuit: cashew from Brazil, planted in Goa by Portugal, distilled in a clay pot — 500 years of colonial botany in one glass"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Cazulo Cashew Feni Reserve (vintage dated, 40yr orchard)",
            "criteria": "Single village (Siolim); vintage dated; 40-year cashew orchard; "
                "bhaati clay pot still in continuous use; GI certified; "
                "the reference expression for export-quality Feni",
            "markers": "Cazulo Reserve; US ~$45-65; UK ~$40-60; India ~$15-20 equivalent; limited export"
        },
        {
            "tier": 3,
            "tier_name": "Cazulo Standard Cashew Feni (GI certified)",
            "criteria": "GI certified; Siolim village sourcing; traditional bhaati; "
                "the accessible premium expression of the tradition",
            "markers": "Cazulo Standard; US ~$35-50; India ~$8-12 equivalent"
        },
        {
            "tier": 2,
            "tier_name": "XL Velho Feni or Old Goa Cashew Feni (local brand, GI certified)",
            "criteria": "GI certified local brands; traditional production; "
                "widely available in Goa; standard quality benchmark",
            "markers": "XL Velho; Goa only ~$5-8 equivalent; not exported"
        },
        {
            "tier": 1,
            "tier_name": "Coconut Feni (separate tradition, lower price tier)",
            "criteria": "Coconut palm flower toddy distillate; different raw material; "
                "lower status than Cashew Feni traditionally; "
                "introduction to the Feni category at lowest accessible price",
            "markers": "Coconut Feni; Goa only; not exported; educational substitute only outside India"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at room temperature or with a single ice sphere; the cashew character is most distinct at 20-22 degrees C",
        "vessel": "Short tumbler or shot glass for traditional Goa service; tulip for professional tasting; clay cup if available",
        "technique": "Cazulo Feni as a cocktail base: "
            "Feni Caipirinha — 50mL Cazulo + 15mL lime juice + 10mL sugar + muddled lime. "
            "The Caipirinha format works because the cashew-apple and lime "
            "share tropical-dry citrus character that the Brazilian original uses cachaca for. "
            "The PCT circuit demonstration: Caipirinha made with Feni instead of cachaca "
            "is the PCT beverage metaphor in a glass — "
            "a Brazilian cocktail format using a Goan spirit made from a Brazilian fruit. "
            "The education narrative: 'The cashew is native to Brazil. "
            "The Portuguese brought it to Goa in 1560. "
            "In Goa, they distilled it using their own alembic technology. "
            "This spirit has been made in this village since the 16th century.'",
        "programme_position": "PCT education flagship; India origin spirits; international cocktail menu using non-standard bases",
        "verbal_presentation": "Cazulo Cashew Feni — Siolim, North Goa. "
            "The cashew tree arrived here from Brazil in 1560, brought by the Portuguese. "
            "It has been distilled in this clay pot ever since. "
            "GI-protected. The first Indian spirit with geographic protection."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Cazulo Premium Feni — the internationally recognised quality benchmark",
        "producer_location": "Siolim, North Goa, India",
        "key_person": "Nikhil Sikchi (founder, Cazulo; pioneer of premium Feni export)",
        "bc_distributor": "Not available in BC. No BCLDB listing.",
        "us_distributor": "Santra Beverages and specialty Indian spirits importers; "
            "limited distribution in Indian restaurant markets (New York, New Jersey)",
        "uk_distributor": "Cazulo has UK distribution through Indian specialty drinks importers",
        "price_tier": "Entry: $35-50 (Cazulo standard). Premium: $45-65 (Cazulo Reserve). Ultra: N/A — the category ceiling is still developing.",
        "availability_notes": "Cazulo Feni is available in the US and UK through specialty Indian spirits importers. "
            "Not available in BC at time of writing. India price is significantly lower ($8-20 equivalent)."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Prawn Balchao (Goa fermented prawn pickle with vinegar and dried chillies)",
            "pairing_type": "complement",
            "rationale": "Balchao is Goa's most distinctively Portuguese-Indian dish — "
                "a fermented prawn pickle with vinegar that reflects the Portuguese "
                "use of wine vinegar in tropical preservation. "
                "The cashew mineral dryness of Feni cuts through the "
                "fermented shrimp funk and vinegar acidity — "
                "the canonical Goa table where both are present simultaneously."
        },
        {
            "technique_id": "",
            "dish": "Bebinca (Goan layered coconut-egg custard cake)",
            "pairing_type": "bridge",
            "rationale": "Bebinca is Goa's most celebrated dessert — "
                "a layered coconut milk and egg yolk cake baked layer by layer. "
                "The coconut richness bridges the cashew-tropical character of the Feni "
                "through the shared tropical-fruit register. "
                "Both are Goan products; both carry the Portuguese-Indian synthesis."
        }
    ],
    "source": "Cazulo Premium Feni production documentation; "
        "GI certificate for Goa Feni (GI Application No. 155, 2009); "
        "BEVQ (Goa Beverages Corporation) technical specifications; "
        "Santra Beverages US distribution portfolio",
    "trail_connection": "PCT-8",
    "trail_note": "PCT Region 8: Goa — the most intact Portuguese colonial cultural territory "
        "outside Portugal itself. "
        "Cashew Feni is the PCT's most explicit agricultural loop: "
        "cashew native to Brazil (PCT-12/13) → transplanted to Goa by Portugal "
        "(PCT-8) → distilled using Portuguese alembic technology → "
        "GI-protected in 2009 by the Indian government. "
        "The entire Portuguese colonial botanical exchange in one spirit."
})

session.commit_batch()

session.switch_region("wine", "India — Nashik Valley (Sula Vineyards, Chenin Blanc)")

session.add_beverage({
    "tradition": "wine",
    "sub_tradition": "india nashik valley chenin blanc tropical continental",
    "region": "India — Nashik Valley (Maharashtra, 600m altitude)",
    "name": "Sula Chenin Blanc — Nashik Valley, India's First World-Class White Wine Origin",
    "terroir_origin": (
        "The Nashik Valley is the centre of India's wine revolution — "
        "located in Maharashtra state, approximately 180km northeast of Mumbai, "
        "at 600m altitude on basalt-derived soils. "
        "The PCT connection: Nashik's wine production was not historically Portuguese, "
        "but the Portuguese colonial presence in nearby Goa (PCT-8) created "
        "a wine-drinking culture in western India that provided the market context "
        "for the modern Indian wine industry. "
        "The Nashik terroir: the Deccan Plateau's basalt geology creates a distinctive "
        "growing environment — well-drained basalt soils with high mineral content, "
        "altitude-moderated temperature (30-35 degrees C summer peak vs. "
        "Mumbai's coastal 35-38 degrees C), and a continental monsoon pattern "
        "that provides 700mm rainfall concentrated in June-September "
        "(the growing season is October-March, the dry, cool winter). "
        "Chenin Blanc as the dominant variety: Sula founder Rajeev Samant chose "
        "Chenin Blanc as the signature white variety based on its proven "
        "performance in warm climates (Loire Valley, South Africa, Argentina). "
        "The Nashik Chenin is dramatically different from Loire Valley Chenin: "
        "lower acidity (the monsoon break creates warmer winters than Vouvray), "
        "higher tropical fruit concentration, and a richer mouthfeel "
        "from the basalt mineral content and warm harvest conditions."
    ),
    "production_technique": (
        "Sula Nashik production: "
        "Harvest: manual, January-February — the cool dry winter is the Nashik harvest window. "
        "Vine training: double cordon Royat on trellises at 600m altitude; "
        "average vine age at Sula's estate: 15-25 years. "
        "Varieties: Chenin Blanc (dominant for premium white); "
        "also Sauvignon Blanc, Riesling (atypical for this latitude). "
        "Fermentation: temperature-controlled stainless steel; "
        "whole-cluster pressing; Sula's winemakers use Burgundy-trained techniques. "
        "Lees ageing: the Sula Dindori Reserve Chenin Blanc is "
        "aged 6 months on gross lees in a combination of stainless steel "
        "and neutral French oak (10-20% new oak) — the lees ageing adds "
        "texture that compensates for the lower natural acidity. "
        "The harvest timing challenge: the Nashik growing season ends when "
        "temperatures begin rising in March-April; delayed harvest produces "
        "overripe fruit; early harvest produces underripe acid. "
        "Vintage variation in Nashik: significant — good vintages have "
        "a cool, dry March (slow phenolic maturation); "
        "difficult vintages arrive with early heat (rapid sugar accumulation "
        "before acid develops). "
        "Wine tourism: Sula's winery at Gangapur Village is the largest "
        "wine tourism destination in India — approximately 300,000 visitors per year."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "wine",
            "beverage": "Chenin Blanc Vouvray Sec (Loire Valley, France)",
            "connection": (
                "The same variety from the cooler origin. "
                "Vouvray Sec: higher acidity, mineral, apple-quince, "
                "beeswax texture, capable of 20-30 year ageing. "
                "Nashik Chenin: lower acidity, more tropical (mango-papaya), "
                "richer texture, drink within 3-5 years. "
                "The comparison demonstrates that Chenin Blanc is a variety "
                "whose character is determined almost entirely by climate latitude."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Stellenbosch Chenin Blanc (South Africa, Swartland)",
            "connection": (
                "Both are warm-climate Chenin Blancs from former British-influenced wine regions. "
                "South African Chenin (Ken Forrester, Mullineux) is the closest "
                "established reference for warm-climate Chenin quality. "
                "The comparison contextualises Nashik's quality level within "
                "the global Chenin Blanc conversation."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Grover Zampa La Reserve Blanc (Nandi Hills, Karnataka, India)",
            "connection": (
                "The internal India comparison: Nashik (Maharashtra, Chenin dominant) "
                "vs Nandi Hills (Karnataka, cooler altitude, Sauvignon Blanc and Chardonnay). "
                "The two regions show the range of Indian terroir — "
                "both are 20-30 year old industries; both are developing regional identity."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Torrontes Cafayate (Argentina, high altitude tropical white)",
            "connection": (
                "Both are tropical-latitude, high-altitude white wines "
                "from formerly non-traditional wine regions that have achieved "
                "international recognition in the last 25 years. "
                "Argentina's Torrontes and India's Chenin Blanc both demonstrate "
                "that altitude can compensate for latitude in tropical wine production."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Pale gold with green-gold highlights; medium viscosity; faint spritz at 1-2 years from partial CO2 retention",
        "nose": "Ripe white peach, green mango, guava, fresh lychee, lemon blossom; the tropical fruit character is more pronounced than Loire Valley Chenin at equivalent price",
        "palate": "Entry: off-dry with perceptible residual sugar (3-8g/L in standard; up to 15g/L in late-harvest expressions). Mid-palate: tropical fruit concentration balanced by medium-plus acidity. Finish: the Nashik basalt mineral provides a dry stone note under the fruit",
        "texture": "Medium body; the lees ageing on Dindori Reserve creates a textured mid-palate; rounder than Loire Chenin but with more tension than many tropical whites",
        "finish": "40-55 seconds; tropical fruit yielding to mineral and light acidity; the finish is clean and dry despite the residual sugar impression on entry",
        "conclusion": "The proof that India has a wine identity — not a European imitation but a tropical-basalt-altitude expression of a globally adaptable variety"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Sula Dindori Reserve Chenin Blanc (lees aged, neutral oak)",
            "criteria": "Estate vineyard; 6 months lees contact; 10-20% neutral French oak; "
                "the most textured and age-worthy Sula Chenin expression",
            "markers": "Sula Dindori Reserve; India ~$18-22 equivalent; UK ~$22-28; limited US distribution"
        },
        {
            "tier": 3,
            "tier_name": "Sula Chenin Blanc Vineyards (vintage single estate)",
            "criteria": "Gangapur estate; stainless steel; no oak; "
                "the definitive expression of Nashik Chenin terroir at standard commercial price",
            "markers": "Sula Chenin Blanc; India ~$10-14 equivalent; UK ~$14-18; US specialty wine shops ~$18-24"
        },
        {
            "tier": 2,
            "tier_name": "Grover Zampa Sauvignon Blanc (Nandi Hills, alternative Indian white)",
            "connection": "Alternative premium Indian white for programme depth",
            "criteria": "Nandi Hills terroir; 4-6 months lees contact; "
                "reference for the Karnataka wine region as alternative to Nashik",
            "markers": "Grover Zampa SB; India ~$12-16; UK ~$16-20"
        },
        {
            "tier": 1,
            "tier_name": "Sula Sauvignon Blanc or Sula Riesling (entry Indian white)",
            "criteria": "Nashik estate; stainless steel; accessible pricing; "
                "introduction to Indian wine for guests new to the category",
            "markers": "Sula SB; India ~$7-10 equivalent; US ~$15-18; UK ~$12-16"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 10-12 degrees C — the tropical fruit character needs some chill to stay fresh; too warm makes it cloying",
        "vessel": "Narrow white wine glass (Riesling or Loire style) to preserve the floral and tropical aromatics without dissipating them too rapidly",
        "technique": "Sula Dindori Reserve Chenin as a white Burgundy substitute: "
            "the lees texture and mineral finish position this wine in the same service context "
            "as a mid-range Macon-Villages or Chablis at a fraction of the price. "
            "The India origin narrative: 'Indian wine has existed for 25 years at quality level. "
            "Nashik is 600m altitude; basalt soils; cool winters for growing. "
            "This wine contains 0% compromise and 100% Indian wine history.'",
        "programme_position": "Indian cuisine pairing; PCT education wine; affordable white for by-the-glass program",
        "verbal_presentation": "Sula Dindori Reserve Chenin Blanc — Nashik Valley, Maharashtra. "
            "600 metres altitude on the Deccan Plateau. "
            "Indian wine on its own terms."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Sula Vineyards (Rajeev Samant) — the first and most internationally recognised Indian wine producer",
        "producer_location": "Gangapur Village, Nashik, Maharashtra, India",
        "key_person": "Rajeev Samant (founder/CEO); Kerry Damskey (consulting winemaker, US)",
        "bc_distributor": "Not available through BCLDB. Private import only.",
        "us_distributor": "ASV Wines (US); limited distribution in Indian restaurant markets (New York, Bay Area)",
        "uk_distributor": "Widely available in UK: Waitrose, Marks and Spencer, Oddbins, The Wine Society",
        "price_tier": "Entry: $15-18 (Sula SB). Mid: $18-24 (Sula Chenin Blanc). Premium: $22-28 (Dindori Reserve).",
        "availability_notes": "Sula is widely available in the UK (Waitrose, M&S). "
            "US availability is limited to Indian-focused specialty wine retailers. "
            "BC: private order required."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Grilled tandoori prawn with mint chutney and fresh lime",
            "pairing_type": "complement",
            "rationale": "The tropical-citrus character of Nashik Chenin Blanc "
                "is the natural Indian wine pairing for tandoori seafood. "
                "The lime in the chutney and the citrus in the wine create "
                "a mutual citrus bridge; the tandoor smoke and the mineral basalt "
                "character of the Chenin create a second-layer dialogue."
        },
        {
            "technique_id": "",
            "dish": "Goa prawn curry (coconut milk base, green chilli, tamarind)",
            "pairing_type": "bridge",
            "rationale": "The PCT bridge pairing: a Goa prawn curry (PCT-8) "
                "paired with a Nashik Valley Chenin Blanc (adjacent Maharashtra) "
                "is the most natural Indian wine-and-food pairing in the context "
                "of a PCT beverage programme. "
                "The coconut and tamarind sweetness bridges the tropical fruit "
                "in the wine and the spiced coconut in the dish."
        }
    ],
    "source": "Sula Vineyards production documentation; "
        "FSSAI (Food Safety and Standards Authority of India) wine classification; "
        "ASV Wines US distribution portfolio; "
        "UK Wine & Spirit Trade Association India wine import data 2024",
    "trail_connection": "PCT-8",
    "trail_note": "PCT Region 8: Goa → Nashik extension. "
        "The Portuguese wine-drinking culture in Goa (PCT-8) and the "
        "historical British colonial wine import market in Mumbai and Bangalore "
        "together created the consumer demand that Sula's 1999 launch capitalised on. "
        "The Nashik wine industry is the commercial offspring of "
        "the Portuguese-British wine culture layered on the Indian subcontinent."
})

session.commit_batch()

session.finish()
