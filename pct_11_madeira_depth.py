#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="fortified",
    region="Portugal — Madeira (Rare Varieties)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=12,
    running_total=51
)

session.add_producer({
    "tradition": "fortified",
    "name": "Vinhos Barbeito",
    "location": "Camara de Lobos, Madeira, Portugal",
    "description": "Founded 1946 by Mario Barbeito; now led by Ricardo Freitas. "
        "The only house still fermenting in open wooden vats and the last to maintain "
        "significant stocks of pre-phylloxera Terrantez and Bastardo.",
    "founded": "1946",
    "region": "Madeira DOC",
    "website": "https://www.vinhosbarbeito.com",
    "verified": True
})

session.add_producer({
    "tradition": "fortified",
    "name": "Henriques and Henriques",
    "location": "Camara de Lobos, Madeira, Portugal",
    "description": "Founded 1850; one of the few Madeira houses to own significant "
        "vineyard land (60 ha). The H&H 15-year Verdelho is the benchmark expression — "
        "medium-dry, smoked citrus peel, mineral salinity, extraordinary length.",
    "founded": "1850",
    "region": "Madeira DOC",
    "website": "https://www.henriquesehenriques.pt",
    "verified": True
})

session.add_purveyor({
    "name": "The Rare Wine Co.",
    "type": "importer",
    "description": "Napa-based dedicated importer of Madeira. "
        "The dominant US importer for premium Madeira, representing Barbeito and d\'Oliveira.",
    "markets_served": ["US", "nationwide_US"],
    "traditions_carried": ["fortified"],
    "website": "https://www.rarewineco.com",
    "verified": True
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "madeira canteiro terrantez",
    "region": "Portugal — Madeira (Terrantez Variety)",
    "name": "Madeira Terrantez — Rarest Native Variety, High-Acid Medium-Rich Style",
    "terroir_origin": (
        "Terrantez is Madeira\'s most prized and rarest native white variety — "
        "nearly wiped out by the dual phylloxera and oidium epidemics of the 1870s-1880s. "
        "Fewer than 5 hectares exist today, concentrated in Sao Jorge and Camara de Lobos. "
        "In the pre-phylloxera era Terrantez ranked above Sercial and Verdelho as the wine "
        "of choice for the English merchant class in Funchal. The variety demands "
        "exceptional cultivation discipline — low yields, disease susceptibility, irregular "
        "ripening — so only Barbeito and one or two independent farmers have maintained "
        "production. Terrantez sits medium in the Madeira sweetness scale: drier than Bual, "
        "richer than Verdelho. Its defining characteristic is the tension between residual "
        "sugar and devastating acid — a paradox of texture that no other Madeira variety replicates. "
        "Sao Jorge parish: north-facing volcanic basalt slopes, 400-550m elevation, Atlantic wind "
        "exposure full. Volcanic basalt and tuff parent material: mineral salinity, high phosphorus, "
        "low potassium. Pergola system (latada): overhead vine training allows airflow, critical "
        "for humidity control on this Atlantic island."
    ),
    "production_technique": (
        "Harvest: manual, late October — Terrantez ripens 2-3 weeks after Verdelho and Sercial. "
        "Fortification: neutral grape spirit (96% abv) added at approx 9% residual sugar (medium style). "
        "Canteiro method only — NO estufagem heat tanks; 20yr+ in attic lodges at Funchal waterfront. "
        "Canteiro ageing: barrels stacked in tiers near roof; summer temperatures reach 35-40C naturally. "
        "Barrel regime: 500L chestnut then 300L American oak; solera-style topping from younger vintages. "
        "Barbeito vintage releases: single barrel, single year — minimum 20yr age; Ricardo Freitas "
        "selects by sensory evaluation only. Oxidative ageing: no topping up; ullage intentional — "
        "controlled micro-oxygenation creates rancio character over decades. "
        "Bottling: no filtration; some batches unfined — haze possible in cold storage."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "fortified",
            "beverage": "Tokaji Aszu 5-6 Puttonyos (Hungary)",
            "connection": (
                "Same tension between botrytis sweetness and volcanic acid — "
                "different climate, identical paradox of structure. "
                "Both demand decades of ageing for full resolution."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Chateau Chalon Vin Jaune (Jura)",
            "connection": (
                "Solera-influenced oxidative ageing in French Jura parallels Madeira\'s "
                "canteiro philosophy — both demand patience measured in decades, "
                "both produce rancio and volatile complexity from controlled oxidation."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Bual Madeira",
            "connection": (
                "Bual has more stone-fruit density; Terrantez has more citrus-mineral "
                "definition — the distinction reveals the internal range within the Madeira DOC."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Pedro Ximenez Sherry (aged)",
            "connection": (
                "Both use extreme concentration, but Terrantez maintains acid architecture "
                "that PX dissolves — two opposite philosophies of fortified sweetness."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Deep amber-mahogany, slow-rolling viscous legs; green-gold rim in young examples fading to tawny at 20yr",
        "nose": "Dried orange peel, quince paste, rancio walnut oil, volcanic mineral, old varnish, iodine-sea air",
        "palate": "Entry: medium-rich sweetness. Mid-palate: volcanic acid cuts through density with precision. Finish: 90+ seconds of citrus mineral and walnut oxidation",
        "texture": "Oily-glycerous weight paradoxically light on the palate — the high acid provides lift that Bual cannot match",
        "finish": "Extremely persistent — volatile acidity provides sharp definition; dried citrus peel and rancio last minutes not seconds",
        "conclusion": "The most intellectually demanding Madeira style — requires context to be understood, rewards patience"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Pre-1970 Vintage Terrantez",
            "criteria": "Single vintage, pre-phylloxera stock lineage; 50+ years canteiro; museum-quality; authenticated provenance required",
            "markers": "Barbeito Terrantez 1977 or earlier; auction or direct allocation only; BC and US price on request"
        },
        {
            "tier": 3,
            "tier_name": "Barbeito Terrantez 20yr Single Cask",
            "criteria": "Full canteiro 20yr minimum; no estufagem; single barrel selection by Ricardo Freitas; unfined",
            "markers": "Barbeito Terrantez 20yr; US ~$120-200 via Rare Wine Co.; limited annual production"
        },
        {
            "tier": 2,
            "tier_name": "H&H Colheita Terrantez 15yr",
            "criteria": "Single-vintage aged 15yr; more focus than blended versions; better terroir expression",
            "markers": "H&H 15yr Colheita; BC ~$75-100; US ~$65-85; BCLDB special order"
        },
        {
            "tier": 1,
            "tier_name": "Blandy\'s Terrantez 10yr",
            "criteria": "Blended across years for consistency; estufagem-hybrid ageing; gentler fruit-forward profile",
            "markers": "Blandy\'s Terrantez 10yr; BC ~$45-60; US ~$40-55; BCLDB listed"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 14-16 degrees C — too cold suppresses the volatile character; too warm collapses the acid tension",
        "vessel": "Medium-sized white wine glass or tulip — wide enough to allow the volatile nose to develop; not a Port glass",
        "technique": "The correct Terrantez sequence at table: serve after Sercial and Verdelho, before Bual and Malmsey. "
            "The acid provides a mid-meal reset. At the bar: 20yr Terrantez in a Nick & Nora, "
            "single orange peel expression, neat — converts Madeira skeptics on the first pour. "
            "Never use Terrantez in cooked applications — the volatile acid dissipates on heat; "
            "use Bual or Malmsey for cooking instead.",
        "programme_position": "Madeira vertical tasting anchor; cheese course partner; by-the-glass premium fortified program",
        "verbal_presentation": "Madeira Terrantez — fewer than five hectares on the island. "
            "Pre-phylloxera variety, canteiro aged twenty years. "
            "More acid than sugar. The paradox of Madeira in a glass."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Vinhos Barbeito (Ricardo Freitas) — Camara de Lobos, Madeira",
        "producer_location": "Camara de Lobos, Madeira, Portugal",
        "key_person": "Ricardo Freitas (winemaker/owner since 2000s)",
        "bc_distributor": "BCLDB stocks Blandy\'s but not Barbeito. Private order required for Barbeito expressions.",
        "us_distributor": "The Rare Wine Co. (Napa) — dominant Madeira dedicated importer; primary Barbeito allocation holder",
        "uk_distributor": "Berry Bros. and Rudd (London) — stocks Barbeito 20yr expressions; primary UK fine Madeira source",
        "price_tier": "Entry: $45-60 (Blandy\'s 10yr). Premium: $120-200 (Barbeito 20yr). Ultra: market price",
        "availability_notes": "Supply extremely limited. Barbeito 20yr allocations sell out annually. Pre-order recommended."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Aged Queijo da Serra (Portuguese mountain sheep cheese, 18+ months)",
            "pairing_type": "complement",
            "rationale": "The crystalline texture and lactic sharpness of aged Queijo da Serra "
                "finds the exact counterpart in Terrantez\'s rancio walnut oil and citrus acid — "
                "two aged Portuguese products at the peak of their respective traditions."
        },
        {
            "technique_id": "",
            "dish": "Foie gras torchon with citrus gel",
            "pairing_type": "contrast",
            "rationale": "Terrantez\'s volcanic acid and medium-rich sweetness is the only Madeira "
                "style that both cuts the fat richness of foie gras and matches its luxury register — "
                "the contrast pairing that reveals both products at their most expressive."
        }
    ],
    "source": "IVBAM (Instituto do Vinho, do Bordado e do Artesanato da Madeira) technical documentation; "
        "Vinhos Barbeito vintage release notes; The Rare Wine Co. Madeira catalogue 2024",
    "trail_connection": "PCT-2",
    "trail_note": "PCT Region 2: Madeira — the island that launched the Portuguese Atlantic trade network. "
        "Terrantez is the pre-phylloxera survivor from the era when Madeira was the most traded "
        "wine on the Atlantic — carried on every Portuguese and British trade vessel crossing "
        "to the Americas, Africa, and the Indian Ocean."
})

session.commit_batch()

session.switch_region("fortified", "Portugal — Madeira (Bastardo Variety)")

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "madeira canteiro bastardo",
    "region": "Portugal — Madeira (Bastardo Variety)",
    "name": "Madeira Bastardo — Ghost Variety, Pre-Phylloxera Red-Berried Fortified",
    "terroir_origin": (
        "Bastardo (identical to Trousseau in Jura, grown across borders under the same name) "
        "was once Madeira\'s second most-planted variety after Malvasia. "
        "The 1872 oidium epidemic followed by phylloxera devastated plantings to near-extinction. "
        "The variety is red-berried — rare for Madeira where white varieties dominate — "
        "producing wines with a distinctive copper-amber colour rather than typical mahogany. "
        "Fewer than 2 hectares remain, primarily in Barbeito\'s supplier network in Sao Vicente "
        "and Santana. A 2019 IVBAM-backed replanting programme has added 0.8ha of new Bastardo. "
        "Sao Vicente north coast: basalt sea cliffs, maximum Atlantic salinity exposure, "
        "highest rainfall zone on island. Santana parish: coolest growing zone, "
        "highest acid retention in red-berried varieties. Volcanic tuff soil: darker, "
        "more heat-retentive than basalt; encourages phenolic development in red skin varieties."
    ),
    "production_technique": (
        "Harvest: mid-October — slightly earlier than Terrantez due to thinner skins and rot risk. "
        "Vinification: whole-cluster pressing; brief skin contact (4-8 hrs) extracts colour and tannin — "
        "no extended maceration. "
        "Fortification: at 4-6% residual sugar — drier than Bual, richer than Verdelho; medium-dry classification. "
        "Canteiro ageing: all remaining Bastardo uses canteiro only — no estufagem applied. "
        "Barrel: 300L American oak, then 500L chestnut; transfers every 5-7 years to fresh wood. "
        "Colour evolution: copper-pink in youth to amber-garnet at 10yr to tawny-copper at 20yr+. "
        "Oxidative development: faster than white-variety Madeiras — tannins soften within 10yr canteiro. "
        "Barbeito releases: 10yr blended and occasional single-vintage (2015 vintage released 2025, "
        "limited to approximately 400 bottles)."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "wine",
            "beverage": "Jura Trousseau (Domaine de la Tournelle)",
            "connection": (
                "Same variety; Jura\'s version is lighter red table wine — "
                "Madeira\'s canteiro transforms it to oxidative amber. "
                "The tannin lineage is recognisable across both styles; "
                "Bastardo 20yr shows where Trousseau goes with five decades of oxidation."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Colheita Tawny Port (20yr)",
            "connection": (
                "Tawny copper colour, dried fruit and rancio similarities — "
                "but Port lacks Madeira\'s volcanic acidity that defines Bastardo\'s finish. "
                "Port is sweeter and heavier; Bastardo is more mineral and tense."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Oloroso Sherry (medium, Lustau)",
            "connection": (
                "Oxidative amber, dried fruit and walnut are shared — "
                "but higher sweetness and lower acid definition in Oloroso "
                "vs Bastardo\'s Atlantic tension shows the Andalusian-Atlantic climate divide."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Sagrantino Passito (Umbria, Arnaldo Caprai)",
            "connection": (
                "Red-grape fortified/passito style with tannin and dried cherry — "
                "tannin structure comparison reveals Bastardo\'s moderate grip "
                "vs Sagrantino\'s formidable power."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Translucent copper-amber with tawny rim; distinctly lighter in colour than Bual or Malmsey at equivalent age",
        "nose": "Dried strawberry, Morello cherry compote, roasted hazelnut, volatile acetone edge, sea salt mineral",
        "palate": "Red-fruit sweetness with grippy fine tannin — unlike any white-variety Madeira; medium-dry with acid lift on finish",
        "texture": "Less viscous than Bual; fine tannin creates slight astringency that white Madeiras lack entirely; unusually refreshing mouthfeel for a fortified wine",
        "finish": "Shorter than Terrantez; red-fruit-and-mineral; tannin provides structural grip through the finish and into the aftertaste",
        "conclusion": "The only Madeira with tannin structure — bridges the aperitif-and-red-wine roles simultaneously"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Pre-phylloxera Bastardo casks (if authenticated)",
            "criteria": "Museum auction only; authentication through IVBAM or independent MW assessment required; "
                "Barbeito has confirmed pre-1870 stocks in deep cellar; extraordinary rarity",
            "markers": "Auction only; price on request; no regular market availability"
        },
        {
            "tier": 3,
            "tier_name": "Barbeito Bastardo 20yr Single Cask",
            "criteria": "Full canteiro 20yr; no estufagem; tannin-softened rancio complexity; "
                "limited to single barrel per release; unfined and unfiltered",
            "markers": "Check vintage availability with The Rare Wine Co.; US ~$150-220; extremely limited"
        },
        {
            "tier": 2,
            "tier_name": "Barbeito Bastardo 10yr Blended",
            "criteria": "Best current-availability example; approximately 500 cases per year; "
                "10yr canteiro minimum; the most achievable Bastardo for program use",
            "markers": "Barbeito Bastardo 10yr; US ~$80-120 via Rare Wine Co.; Canada: private order only"
        },
        {
            "tier": 1,
            "tier_name": "No entry-level Bastardo",
            "criteria": "Supply constraints prevent volume commercial production; "
                "no producer currently offers a sub-10yr or blended entry-tier Bastardo",
            "markers": "Category gap — recommend Blandy\'s Bual 5yr as substitute for entry introduction"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 13-15 degrees C — tannin structure responds to cooler service than white Madeira styles",
        "vessel": "Medium bordeaux-style glass (wider bowl than Port glass) to give the tannin structure room to breathe",
        "technique": "Bastardo in a Madeira Cobbler (crushed ice, seasonal berries, mint) is the most visually "
            "distinctive serve in the fortified category — the copper colour in a crystal glass "
            "creates immediate conversation. At table: with charcuterie boards, aged Gouda, "
            "or dark chocolate at 70%+ cacao. Never serve warm — warmth collapses the tannin freshness.",
        "programme_position": "Fortified wine education sessions; rare variety showcase; charcuterie pairing program",
        "verbal_presentation": "Madeira Bastardo — fewer than two hectares surviving on the island. "
            "Red-berried, canteiro aged, pre-phylloxera lineage. "
            "The copper wine of the Atlantic."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Vinhos Barbeito (Ricardo Freitas) — the last house to maintain regular Bastardo production",
        "producer_location": "Camara de Lobos, Madeira, Portugal",
        "key_person": "Ricardo Freitas (winemaker; has championed pre-phylloxera variety preservation)",
        "bc_distributor": "Not available through BCLDB. Private order through a licensed BC agent required.",
        "us_distributor": "The Rare Wine Co. (Napa) — primary and often sole US source for Barbeito Bastardo",
        "uk_distributor": "Berry Bros. and Rudd or Handford Wines (London) — occasional allocations only",
        "price_tier": "No entry tier. Mid: $80-120 (Barbeito 10yr). Premium: $150-220 (Barbeito 20yr).",
        "availability_notes": "Supply extremely constrained. Barbeito 10yr is the standard commercial release. "
            "Pre-ordering via Rare Wine Co. recommended for any allocation."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Jamon Iberico de Bellota (acorn-fed Iberian ham, 36+ months cure)",
            "pairing_type": "complement",
            "rationale": "Bastardo\'s fine red-fruit tannin cuts through the fat of aged Jamon Iberico "
                "while the dried cherry and hazelnut mineral dialogue runs through both products — "
                "two Iberian Peninsula traditions at peak expression."
        },
        {
            "technique_id": "",
            "dish": "70% Valrhona dark chocolate (Guanaja)",
            "pairing_type": "bridge",
            "rationale": "Bastardo\'s tannin dialogue with high-cacao chocolate works "
                "where Malmsey would be overwhelmed by sweetness — "
                "the medium-dry mineral tension of Bastardo bridges the bitter cacao and the dried fruit "
                "in a way no white Madeira can achieve."
        }
    ],
    "source": "IVBAM Madeira technical classification documentation; "
        "Barbeito vintage release notes and Ricardo Freitas interview documentation; "
        "The Rare Wine Co. Madeira allocation catalogue 2024",
    "trail_connection": "PCT-2",
    "trail_note": "PCT Region 2: Madeira — Bastardo\'s near-extinction and slow recovery "
        "mirrors the colonial disruption of Madeira\'s agricultural landscape. "
        "The preservation of Bastardo by Barbeito is the clearest example of "
        "viticultural archaeology in the Portuguese Atlantic tradition."
})

session.commit_batch()

session.switch_region("fortified", "Portugal — Madeira (Verdelho Variety)")

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "madeira canteiro verdelho",
    "region": "Portugal — Madeira (Verdelho Variety)",
    "name": "Madeira Verdelho 10yr — Medium-Dry Smoky Atlantic Style",
    "terroir_origin": (
        "Verdelho is Madeira\'s most food-flexible variety — medium-dry, with a "
        "signature smoked citrus peel and volcanic mineral character that no other "
        "fortified wine replicates. Historically, Verdelho was the dominant export "
        "style to Brazil and the Baltic states — the wine of choice for Portuguese "
        "colonial trade vessels making the Atlantic crossing. The variety thrives at "
        "mid-elevation (300-500m) on the island\'s south-facing slopes, producing wines "
        "with more body than Sercial and more freshness than Bual. The 10-year category "
        "represents the minimum age at which Verdelho fully expresses its canteiro-derived "
        "depth. Under 10 years the smoky mineral character is underdeveloped. "
        "Verdelho: native Madeira variety (distinct from mainland Verdellho/Gouveio); "
        "mid-elevation cultivar thriving at 300-500m. South coast mid-elevation belt: "
        "warmer than north-face plots; phenolic development vs acid retention balance. "
        "Palheiro and Campanario parcels: volcanic clay-basalt, moderate water retention — "
        "key for the oily texture. Ocean influence: prevailing SW Atlantic winds carry salinity "
        "embedded in every Madeira grown within 5km of coast."
    ),
    "production_technique": (
        "Harvest: mid-September — earlier than Sercial, later than Malvasia; balanced sugar-acid window. "
        "Crushing and pressing: whole-cluster pneumatic press; no skin maceration for white grape varieties. "
        "Fermentation: stainless steel, temperature-controlled; ferments to 6-8% natural alcohol before fortification. "
        "Fortification: neutral 96% grape spirit; target 4-6% residual sugar (medium-dry classification). "
        "Estufagem vs canteiro: commercial 10yr uses hybrid — 6 months estufagem + 9.5yr canteiro; "
        "H&H 15yr uses full canteiro for the complete style expression. "
        "Canteiro: 600L American oak barrels stacked in Funchal waterfront lodges; summer peak 35-40C. "
        "Blending: H&H 15yr blended across multiple years to maintain consistent house style; "
        "single-vintage for Colheita releases. "
        "Oxidative ageing: ullage maintained intentionally — maderisation is the desired outcome, not a defect."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "fortified",
            "beverage": "Manzanilla Pasada Sherry (Barbadillo)",
            "connection": (
                "Closest saline-mineral parallel in the fortified world; both sea-air aged, "
                "both mineral-driven — but Verdelho adds canteiro rancio and Atlantic acid "
                "that aged Manzanilla at the solera level cannot match."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Palo Cortado Sherry (Gonzalez Byass Apostoles)",
            "connection": (
                "Rare, positioned between Amontillado and Oloroso — closest Sherry parallel "
                "to Verdelho\'s tension between fresh and oxidative character. "
                "But Verdelho\'s Atlantic volcanic acid is more pronounced than Jerez\'s warm flatland."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Sercial Madeira",
            "connection": (
                "Sercial is drier, higher acid, more lemon-mineral; Verdelho adds body and "
                "stone-fruit mid-palate that Sercial lacks — the definitive internal Madeira style comparison."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Dry Tokaji Furmint (Disznoko or Royal Tokaji)",
            "connection": (
                "Volcanic mineral character and oxidative ageing parallels — "
                "Hungary\'s volcanic Furmint and Madeira\'s volcanic Verdelho "
                "both carry the mountain-sea mineral axis through to their finish."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Clear amber-gold, lighter than Bual; olive-green rim highlights in 10yr expressions; darker caramel at 15yr+",
        "nose": "Smoked lemon peel, dried apricot kernel, salted caramel, iodine mineral, burnt orange zest; more saline than any other fortified wine from this latitude",
        "palate": "Entry: off-dry, perceptible sweetness. Rapid acid shift mid-palate. Finish: volcanic mineral-saline persistence; the salt stays after the fruit resolves",
        "texture": "Medium-bodied; slight oiliness at 10yr; more glycerous at 15yr+; clean and defined — no softness or flab",
        "finish": "60-75 seconds; smoked citrus and saline mineral; acid provides freshness unusual for a 10yr fortified wine of any tradition",
        "conclusion": "The sommelier\'s Madeira — bridges aperitif, cheese, and dessert roles simultaneously without losing identity"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Barbeito Ricardo Freitas Verdelho Colheita (single vintage) or pre-1950",
            "criteria": "Single vintage release; full canteiro; minimum 30yr; "
                "unfined and unfiltered; maximum individual year expression",
            "markers": "The Rare Wine Co. (when available); US $200+; extremely limited allocation"
        },
        {
            "tier": 3,
            "tier_name": "Barbeito Verdelho 20yr Single-Cask",
            "criteria": "Full canteiro 20yr minimum; single cask selection; more rancio and volatile depth than H&H; "
                "unfined; the reference for what Verdelho becomes at maximum expression",
            "markers": "Barbeito 20yr; US ~$100-150 via Rare Wine Co.; BC: private order only"
        },
        {
            "tier": 2,
            "tier_name": "H&H 15yr Verdelho (Henriques and Henriques)",
            "criteria": "The benchmark 15yr expression; full canteiro; "
                "smoked citrus-mineral at most expressive form; consistent house style",
            "markers": "H&H 15yr Verdelho; BC ~$65-80; US ~$55-70; BCLDB special order"
        },
        {
            "tier": 1,
            "tier_name": "Blandy\'s Verdelho 5yr",
            "criteria": "Estufagem-dominant; simpler caramel-citrus profile; introduction to the variety style",
            "markers": "Blandy\'s Verdelho 5yr; BC ~$28-35; US ~$22-30; BCLDB listed"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 12-14 degrees C for maximum mineral and acid expression — the most food-flexible serving temperature in the fortified category",
        "vessel": "Medium white wine glass (not a Port Dock glass) — the wider bowl opens the smoked citrus and saline mineral nose",
        "technique": "At table: with ceviche or crudo (acid and saline mineral work against seafood acidity), "
            "with aged Manchego or Comte, with ham-based preparations (Jamon Iberico, prosciutto), "
            "and with light tarte tatin or citrus pastries. "
            "Offer a 1.5 oz pour at 13 degrees C with three cheeses "
            "and watch the table\'s perception of Madeira transform in a single service.",
        "programme_position": "By-the-glass premium fortified; Madeira introduction tasting; "
            "cheese course anchor; aperitif program for guests resistant to sweet fortified wine",
        "verbal_presentation": "Madeira Verdelho 15 Years — Henriques and Henriques. "
            "Medium-dry. Atlantic volcanic. Smoked citrus and sea salt. "
            "The wine Portuguese trade ships carried to every continent."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Henriques and Henriques — H&H 15yr Verdelho is the definitive commercial benchmark",
        "producer_location": "Camara de Lobos, Madeira, Portugal",
        "key_person": "H&H family management; one of the few houses with significant vineyard ownership (60 ha)",
        "bc_distributor": "BCLDB stocks Blandy\'s Verdelho 5yr and 10yr; H&H 15yr requires private order through agent",
        "us_distributor": "The Rare Wine Co. (Napa) — H&H 15yr and Barbeito 20yr; National Wine and Spirits (wider distribution)",
        "uk_distributor": "Waitrose (Blandy\'s), Berry Bros. and Rudd (premium stocks), The Wine Society",
        "price_tier": "Entry: $28-35 (Blandy\'s 5yr). Mid: $65-80 (H&H 15yr). Premium: $100-150 (Barbeito 20yr).",
        "availability_notes": "H&H 15yr is the most accessible premium Verdelho in North America. "
            "Blandy\'s widely available across BCLDB, LCBO, and US national distribution."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Cured salmon gravlax with dill and citrus",
            "pairing_type": "complement",
            "rationale": "Verdelho\'s smoked citrus peel and saline mineral profile finds its exact "
                "food counterpart in cured salmon — the salt cure of the fish mirrors the sea-air "
                "salt in the wine, while the citrus and dill of the gravlax extend the lemon-mineral finish."
        },
        {
            "technique_id": "",
            "dish": "Jamon Iberico de Bellota with Manchego Curado",
            "pairing_type": "bridge",
            "rationale": "The bridge pairing: Verdelho\'s medium-dry mineral character sits between "
                "the fat richness of Jamon and the crystalline lactic sharpness of aged Manchego — "
                "a three-way bridge that demonstrates why Verdelho is the most food-flexible "
                "Madeira style in a professional service context."
        }
    ],
    "source": "Henriques and Henriques production documentation; IVBAM technical specifications; "
        "The Rare Wine Co. Madeira catalogue 2024; BCLDB product listings verified April 2026",
    "trail_connection": "PCT-2",
    "trail_note": "PCT Region 2: Madeira — Verdelho was the primary wine of Portuguese Atlantic trade, "
        "carried to Brazil (PCT-12/13), the Cape Verde islands (PCT-4), "
        "Mozambique (PCT-7), and Goa (PCT-8) on every major Portuguese vessel from the 16th century. "
        "The medium-dry mineral style was deliberately suited to the Atlantic crossing — "
        "acid and oxidative resistance made it the only wine that improved during the voyage."
})

session.commit_batch()

session.finish()
