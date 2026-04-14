#!/usr/bin/env python3
# PCT-12: Port Depth
# 40yr Tawny, Garrafeira, Colheita
# Running total entering: 54
import sys, os
sys.path.insert(0, os.path.expanduser("~/Desktop/provenance-tester-1"))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="fortified",
    region="Portugal — Douro (Port, Tawny Styles)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=13,
    running_total=54
)

session.add_producer({
    "tradition": "fortified",
    "name": "Ramos Pinto",
    "location": "Vila Nova de Gaia, Porto, Portugal",
    "description": "Founded 1880 by Adriano Ramos Pinto. Known for pioneering "
        "Quinta do Bom Retiro as a single-quinta Tawny producer. "
        "LVMH acquisition in 1990 brought investment while maintaining production autonomy. "
        "The Adriano 30yr and 40yr Tawny are among the finest in the category.",
    "founded": "1880",
    "region": "Douro DOC / Port",
    "website": "https://www.ramospinto.pt",
    "verified": True
})

session.add_producer({
    "tradition": "fortified",
    "name": "Niepoort",
    "location": "Vila Nova de Gaia, Porto, Portugal",
    "description": "Dutch family house founded 1842; now led by Dirk Niepoort. "
        "Produces the definitive Colheita range (single-harvest Tawny) and "
        "the legendary Garrafeira Port — wood ageing combined with extended bottle maturation. "
        "Holds Colheita stocks from 1934 to the present.",
    "founded": "1842",
    "region": "Douro DOC / Port",
    "website": "https://www.niepoort-vinhos.com",
    "verified": True
})

session.add_purveyor({
    "name": "Broadbent Selections",
    "type": "importer",
    "description": "New York-based importer of Port and fortified wines. "
        "Holds primary US allocation for Niepoort and Ramos Pinto.",
    "markets_served": ["US", "nationwide_US"],
    "traditions_carried": ["fortified"],
    "website": "https://www.broadbent.com",
    "verified": True
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "port tawny 40yr wood aged",
    "region": "Portugal — Douro (Tawny Port, 40yr Category)",
    "name": "40-Year-Old Tawny Port — Four Decades of Canteiro Oxidative Ageing",
    "terroir_origin": (
        "40-Year-Old Tawny Port is the category that most challenges wine's usual "
        "concept of vintage — the label designates average age of the blend, "
        "not the harvest year. The IVDP (Instituto dos Vinhos do Douro e Porto) "
        "certifies that the blend's average age is minimum 40 years. "
        "In practice, the finest 40yr blends contain components from 50, 60, or 70+ year barrels. "
        "The Douro terroir: schist (xisto) dominated hillsides at 50-200m altitude, "
        "Cima Corgo sub-region for premium production. "
        "Soils: decomposed schist, low water retention, forcing deep vine root systems "
        "that access subterranean moisture during the dry Douro summer (200mm annual rainfall). "
        "The Douro summer: 40-45 degrees C peak temperatures; the same conditions that drive "
        "the canteiro ageing also concentrate sugar in the grapes. "
        "Principal varieties: Touriga Nacional (aromatics, structure), Touriga Franca "
        "(volume, colour), Tinta Roriz/Tempranillo (body), Tinto Cao (acidity). "
        "For Tawny: blended vineyards across multiple quintas; focus is on average vine age "
        "(older vines produce more concentrated must), not single-site identity."
    ),
    "production_technique": (
        "Harvest: manual picking into 20kg baskets maximum; foot-treading in granite lagares "
        "for premium lots, robotic treaders for volume. "
        "Fortification: grape spirit (77% abv) added at approximately 5-8 Baume — "
        "higher sugar residual than Vintage Port; the sweetness essential for the "
        "40yr Tawny texture after four decades of oxidative reduction. "
        "Wood ageing: 550L oak pipes (seasoned American or French oak) in Gaia waterfront lodges; "
        "summer heat drives evaporation and oxidation (angel's share = 3% per year). "
        "Four decades of wood ageing creates: rancio character (oxidative esters from "
        "glycerol breakdown), dried fruit concentration (apricot, fig, walnut), "
        "amber-tawny colour from phenolic browning (colour shift from deep ruby to "
        "tawny amber takes 10+ years), and acid structure that becomes almost saline. "
        "The blending: the cellarmaster tastes hundreds of barrels to assemble the 40yr "
        "designation; age is not uniform but averaged. "
        "Niepoort Quinta do Bom Retiro 40yr: single-quinta sourcing; old vine Touriga "
        "Nacional dominant; the benchmark for house-expression Tawny."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "fortified",
            "beverage": "Madeira Malmsey 20yr",
            "connection": (
                "Both are oxidative fortified wines aged in wood with residual sweetness. "
                "40yr Tawny: nutty rancio, dried apricot, amber-tawny. "
                "Malmsey 20yr: caramel, raisined fruit, mahogany. "
                "The comparison reveals how grape variety and island vs. continent ageing "
                "environments create divergent outcomes from identical oxidative logic."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Oloroso VORS (30yr) Sherry",
            "connection": (
                "Both are wood-aged oxidative fortified wines in the 30-40yr range. "
                "VORS Oloroso: drier, more intense, walnut oil and dark fig. "
                "40yr Tawny: sweeter, more apricot and rancio, higher acid backbone. "
                "The sweetness vs dryness divide is the primary structural contrast."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Armagnac Bas-Armagnac 30yr (Darroze)",
            "connection": (
                "Both require four decades of patient barrel evolution for full expression. "
                "Both develop rancio as the primary oxidative complexity marker. "
                "The brandy-Port comparison in fine dining teaches guests that "
                "rancio is a sign of quality, not defect."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Colheita Tawny Port (same house)",
            "connection": (
                "40yr Tawny (blended, averaged) vs Colheita (single vintage, same wood method) — "
                "the internal Port category comparison that demonstrates how "
                "blending consistency and vintage individuality create different outcomes "
                "from identical production methods."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Warm amber-tawny with orange-mahogany rim; the colour is amber-copper not ruby at 40yr — the oxidative browning is complete",
        "nose": "Concentrated dried apricot, fig, rancio walnut oil, orange peel, caramel, toasted almond, volatile aldehydes; the nose at 40yr is more nuanced than most spirits at equivalent age",
        "palate": "Sweet but not cloying — the 40yr acid backbone prevents the sweetness from becoming one-dimensional; dried fruit, rancio, and saline mineral work in sequence",
        "texture": "Dense and glycerous; four decades of evaporation concentrate the original wine to a fraction of its volume; mouthcoating without heaviness",
        "finish": "90+ seconds; alternating rancio walnut oil and dried apricot; faint volatile acidity on the last breath adds length; the most persistent finish in the Portuguese fortified category",
        "conclusion": "The highest expression of oxidative patience — proof that time transforms rather than diminishes"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Quinta do Noval 40yr (Nacional vineyard blend)",
            "criteria": "Nacional vineyard pre-phylloxera old vine contribution; 40yr aged in smallest pipe format; "
                "exceptional concentration from low-yield schist; the most priced 40yr Tawny in production",
            "markers": "Quinta do Noval 40yr; BC ~$150-200; US ~$130-180; extremely limited allocation"
        },
        {
            "tier": 3,
            "tier_name": "Graham's 40yr or Ramos Pinto 40yr",
            "criteria": "Definitive commercial benchmark 40yr expressions; consistent house style; "
                "full rancio development; widely available at premium price point",
            "markers": "Graham's 40yr; Ramos Pinto 40yr; BC ~$90-130; US ~$80-120; BCLDB listed"
        },
        {
            "tier": 2,
            "tier_name": "Taylor Fladgate 30yr or Fonseca 30yr",
            "criteria": "30yr designation; full oxidative development with slightly less rancio intensity than 40yr; "
                "strong value relative to 40yr; better entry point for programme introduction",
            "markers": "Taylor 30yr; BC ~$70-90; US ~$60-80; BCLDB listed"
        },
        {
            "tier": 1,
            "tier_name": "Calem 20yr or Ferreira 20yr",
            "criteria": "20yr designation; rancio character emerging but not dominant; "
                "dried apricot and walnut developing; introduction to the oxidative Tawny style",
            "markers": "Calem 20yr; BC ~$45-60; US ~$40-55; BCLDB widely available"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 14-16 degrees C lightly chilled — 40yr paradoxically shows better at moderate cool than room temperature; warmth collapses the rancio into sweetness",
        "vessel": "Small 90-100mL pour in a white wine glass (not a Port glass); the wider bowl opens the volatile aldehydes and rancio nose",
        "technique": "40yr Tawny at dessert: serve with walnut and dried apricot components of the cheese course, "
            "or after dessert service as a meditation wine. "
            "The Portuguese serve it chilled as an aperitif in the Douro — the cold sharpens the acid "
            "and makes the wine feel lighter and more refreshing than expected. "
            "The 40yr is the Port that converts whisky drinkers — the rancio bridge to single malt is direct.",
        "programme_position": "End-of-meal meditation pour; premium dessert course pairing; fine Tawny vertical education session",
        "verbal_presentation": "Forty-Year-Old Tawny — an average age, not a vintage. "
            "Built from four decades of barrels, each contributing its own decade. "
            "Apricot and walnut from forty years in the Douro sun."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Graham's, Ramos Pinto, Quinta do Noval",
        "producer_location": "Vila Nova de Gaia, Porto, Portugal (Gaia lodges on the Douro south bank)",
        "key_person": "David Guimaraens (Graham's winemaker); Joao Ramos (Ramos Pinto); Christian Seely (Noval/AXA)",
        "bc_distributor": "BCLDB stocks Graham's 40yr, Taylor 30yr, Ramos Pinto 30yr and 40yr at Signature stores",
        "us_distributor": "Broadbent Selections (premium allocation); Kobrand Corp (Taylor Fladgate / Fonseca); Haus Alpenz (Noval)",
        "uk_distributor": "Berry Bros. and Rudd, Waitrose, direct from Gaia lodges",
        "price_tier": "Entry: $45-60 (20yr). Mid: $70-90 (30yr). Premium: $90-130 (40yr). Ultra: $150-200 (Noval 40yr).",
        "availability_notes": "40yr Tawny is the most widely available ultra-premium fortified wine in BC. "
            "Graham's 40yr and Taylor 30yr are BCLDB Signature store staples in Vancouver."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Creme brulee with caramelised sugar and Madagascar vanilla",
            "pairing_type": "complement",
            "rationale": "The caramelised sugar crust and vanilla cream of creme brulee find "
                "their exact flavour register in 40yr Tawny's oxidative caramel and dried apricot — "
                "demonstrating why Tawny Port is the canonical dessert wine of French bistro "
                "and Portuguese fine dining simultaneously."
        },
        {
            "technique_id": "",
            "dish": "Stilton and walnut, or Roquefort with dried fig",
            "pairing_type": "bridge",
            "rationale": "The rancio walnut oil in 40yr Tawny bridges the blue cheese fat and salt "
                "with the dried fruit sweetness — a textbook bridge pairing where the wine's "
                "rancio marker reflects both the nutty crust and oxidative fat of the cheese."
        }
    ],
    "source": "IVDP technical specifications for Tawny Port designations; "
        "Graham's, Ramos Pinto, and Taylor Fladgate production documentation; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1: Portugal (Douro). 40yr Tawny is the apex expression of the Port category "
        "that the English-Portuguese trade alliance (Methuen Treaty 1703) created and sustained. "
        "The 18th-century English merchant houses (Graham's, Taylor, Sandeman, Fonseca) "
        "established the Gaia lodge system that still houses every 40yr Tawny in production today."
})

session.commit_batch()

session.switch_region("fortified", "Portugal — Douro (Garrafeira Port, Niepoort)")

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "port garrafeira wood then bottle aged",
    "region": "Portugal — Douro (Garrafeira Port Category)",
    "name": "Garrafeira Port — Niepoort, Wood Ageing Then Extended Glass Maturation",
    "terroir_origin": (
        "Garrafeira Port is a category so rare that only Niepoort produces it commercially. "
        "The category was defined in the 1937 Port regulations but abandoned by all other houses. "
        "A Garrafeira must age a minimum of 3.5 years in small wood (20-600L barrels), "
        "then transfer to large glass demijohns (10-15 litres) for extended bottle maturation — "
        "minimum 8 years in glass, but Niepoort ages for decades. "
        "The result: a wine that combines the oxidative rancio of wood ageing with the reductive "
        "evolution of bottle maturation — a combination found nowhere else in the fortified world. "
        "Douro terroir: Quinta de Santa Clara and Quinta de Roriz grapes (Cima Corgo, 100-150m); "
        "decomposed schist soils; hand harvested; foot treaded in stone lagares. "
        "Dirk Niepoort revived the Garrafeira programme in the 1980s having found pre-war stocks "
        "in the Gaia lodge. He has continued single-vintage releases, now typically "
        "20-30 years old at release."
    ),
    "production_technique": (
        "Garrafeira production at Niepoort: "
        "Harvest and fermentation: identical to Vintage Port — foot-treaded granite lagares, "
        "fortified at 5-6 Baume (higher sugar than Tawny), full colour and tannin extraction. "
        "Wood phase: 3.5-7 years in 550L pipes; the wine oxidises slowly, developing rancio and "
        "amber colour — but the wood phase is deliberately shorter than Tawny to preserve primary fruit. "
        "Transfer to glass demijohns: the wine moves from wood to sealed glass, cutting off "
        "all further oxidation and beginning a long reductive maturation. "
        "The glass phase: 10-30+ years in demijohn. "
        "Niepoort's 1985 Garrafeira was only released in 2015 after 30 years total maturation. "
        "During the glass phase: tannins polymerise and soften; primary fruit re-emerges "
        "through the rancio layer; tertiary volatile-floral develops that resembles "
        "old Vintage Port but with rancio depth that pure bottle maturation never achieves. "
        "Bottling: into 750mL bottles under cork; significant sediment; decanting essential. "
        "Annual production: fewer than 3,000 bottles per vintage release."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "fortified",
            "beverage": "Vintage Port (Declared Vintage, same house)",
            "connection": (
                "Garrafeira starts identically to Vintage Port — same lagare treading, "
                "same fortification level. The divergence is in the subsequent maturation path: "
                "Vintage goes straight to bottle; Garrafeira goes to wood then glass. "
                "The comparison of Niepoort 2000 Vintage vs 1985 Garrafeira "
                "demonstrates how the wood phase permanently redirects the wine's evolution."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "40yr Tawny Port",
            "connection": (
                "Both undergo wood ageing in Gaia lodges and develop rancio. "
                "But Tawny goes from wood to bottle for immediate consumption; "
                "Garrafeira goes from wood to glass for decades of reductive evolution. "
                "Tawny is the oxidative endpoint; Garrafeira is an oxidative-reductive hybrid."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Cognac Grande Champagne 40yr+ (Tres Vieux Reserve)",
            "connection": (
                "The closest structural parallel: both develop in wood for a defined period "
                "then continue evolving after transfer. Cognac's extended barrel phase creates "
                "rancio that resembles Garrafeira's wood-then-glass trajectory. "
                "The Cognac comparison contextualises rancio for guests who know spirits."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Penfolds Grange (Australian Shiraz, 30yr+ old vintages)",
            "connection": (
                "Both demand extraordinary patience for full expression — "
                "Garrafeira 15-30 years from bottling; old Grange 20-40 years from vintage. "
                "Both develop tertiary complexity that transforms the original production. "
                "The category bridge teaches guests about wine's time dimension."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Dark amber-garnet; bricking at the rim indicates 20+ year bottle age; less tawny than a 40yr but less deep ruby than a 15yr Vintage Port",
        "nose": "Layer one: rancio walnut and dried fig from the wood phase. Layer two: dark berry and roasted coffee from the glass phase reduction. Layer three: volatile dried floral (rose petal, dried violet) that signals extreme bottle age. The three layers are distinct and sequential.",
        "palate": "Medium-full body; tannins fine-grained from double maturation; sweetness lower than 40yr Tawny; the rancio and primary fruit coexist rather than one replacing the other",
        "texture": "The glass phase produces a silkiness that wood ageing alone never achieves — tannins polymerised under reductive conditions into the smoothest texture in the Port category",
        "finish": "2 minutes+; rancio yields to primary fruit yields to volatile floral in a sequence that continues evolving in the glass for several minutes after the last sip",
        "conclusion": "The intellectual achievement of Port — the only category that deliberately combines both major maturation philosophies in sequence"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Niepoort Garrafeira 1985 or pre-1990",
            "criteria": "30+ years of glass maturation on top of 3.5+ years wood; "
                "tertiary volatile-floral at maximum development; extreme rarity — fewer than 3,000 bottles per vintage",
            "markers": "Niepoort 1985 Garrafeira; BC: private import required; US: Broadbent or direct; $200-400+"
        },
        {
            "tier": 3,
            "tier_name": "Niepoort Garrafeira 1995-2005",
            "criteria": "20-30 years combined maturation; full glass-phase evolution achieved; "
                "at drinking peak; the mid-career expression at its most dimensional",
            "markers": "Niepoort Garrafeira 1990s-2000s vintage; US ~$150-250 via Broadbent Selections"
        },
        {
            "tier": 2,
            "tier_name": "Niepoort Garrafeira 2005-2010",
            "criteria": "15-20 years combined maturation; still developing glass phase; "
                "rancio and primary fruit tension at its most dynamic and teachable",
            "markers": "Niepoort Garrafeira; US ~$100-180 via Broadbent; Canada: private import"
        },
        {
            "tier": 1,
            "tier_name": "No entry-level Garrafeira",
            "criteria": "Category produced by Niepoort only; no entry-level version exists; "
                "the closest substitute is Niepoort Colheita 10yr at a lower price point",
            "markers": "Recommend Niepoort Colheita as entry to the house style; BC ~$65-80"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 16-18 degrees C (just below room temperature) — warmth is essential for the three-layer nose to open sequentially",
        "vessel": "Tulip glass or white Burgundy glass — large enough to hold the nose but narrow enough to concentrate it",
        "technique": "Garrafeira requires a 20-minute decanting before service — "
            "the sediment from glass maturation is significant and the wine needs air to open. "
            "Service: as a meditation wine after dessert, or as centrepiece of a Port vertical "
            "showing Tawny (oxidative) vs Garrafeira (oxidative-reductive) vs Vintage (reductive). "
            "The three-category comparison is the most educational Port tasting in "
            "a professional service context.",
        "programme_position": "Rare Port vertical anchor; cellar programme signature; sommelier education centrepiece",
        "verbal_presentation": "Niepoort Garrafeira — three and a half years in oak, then thirty in glass. "
            "The only Port that goes through both maturation philosophies in sequence. "
            "One producer. One category. Fewer than three thousand bottles per vintage."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Niepoort — the sole producer of Garrafeira Port commercially",
        "producer_location": "Vila Nova de Gaia, Porto, Portugal",
        "key_person": "Dirk Niepoort (5th generation; revived the Garrafeira category from pre-war stocks)",
        "bc_distributor": "No BCLDB listing; private import required through a licensed BC agent",
        "us_distributor": "Broadbent Selections (New York) — primary US Niepoort allocation holder",
        "uk_distributor": "Les Caves de Pyrene (UK), Fine and Rare (London)",
        "price_tier": "No entry tier. Minimum $100. Premium: $150-250. Ultra: $200-400+.",
        "availability_notes": "Production limited to fewer than 3,000 bottles per vintage release. "
            "Allocation required in advance through Broadbent Selections (US) or Niepoort direct (Europe)."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Queijo da Serra aged 24 months with walnut bread",
            "pairing_type": "complement",
            "rationale": "The rancio walnut oil in Garrafeira and the crystalline sheep fat of "
                "aged Queijo da Serra are in direct flavour dialogue — "
                "two Portuguese products from opposite sides of the country "
                "that reach maximum expression in the same tasting moment."
        },
        {
            "technique_id": "",
            "dish": "Chestnut honey and aged almond pastry (Queijadas de Sintra)",
            "pairing_type": "bridge",
            "rationale": "The chestnut and almond of traditional Portuguese pastry "
                "bridges the rancio almond-walnut character of the wine with the sweetness register "
                "of the glass-matured fruit — a bridge pairing requiring no explanation; "
                "the mutual recognition is immediate."
        }
    ],
    "source": "Niepoort production documentation; IVDP Garrafeira category technical specifications; "
        "Broadbent Selections US allocation catalogue 2024",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1: Portugal (Douro). Niepoort Garrafeira represents the most extreme "
        "expression of Port's willingness to invest time as a production input. "
        "The Dutch family (Niepoort) producing this most Portuguese of wines "
        "reflects the Anglo-Dutch-Portuguese trade triangle that built the Douro wine industry."
})

session.commit_batch()

session.switch_region("fortified", "Portugal — Douro (Colheita Port, Single Vintage Tawny)")

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "port colheita single vintage tawny",
    "region": "Portugal — Douro (Colheita Port Category)",
    "name": "Colheita Port — Niepoort, Single-Harvest Tawny Wood-Aged to Order",
    "terroir_origin": (
        "Colheita (Portuguese: harvest) Port is the single-vintage version of Tawny Port — "
        "the same production method (wood ageing in Gaia lodges, oxidative evolution) "
        "but from a single harvest year rather than a blend averaged across decades. "
        "The IVDP requires minimum 7 years wood ageing for Colheita designation; "
        "the finest examples are aged 20-40+ years before bottling. "
        "Niepoort's Colheita programme is the most outstanding in the category — "
        "the house holds vintage stocks from 1934 onward in the Gaia lodge. "
        "Douro terroir for Colheita: Cima Corgo sub-region; Quinta da Napoles and Quinta do Passadouro "
        "provide the primary vineyard source. Old vine Touriga Nacional and Tinta Roriz "
        "(average age 40-60 years) are preferred — the concentration from low-yield old vines "
        "creates the residual sugar needed to support four decades of wood ageing. "
        "The vintage year on a Colheita label has emotional resonance for guests in ways "
        "that blended Tawny cannot — guests connect personal dates "
        "(birth year, wedding year) to a wine with genuine provenance from that year."
    ),
    "production_technique": (
        "Colheita production: "
        "Harvest: same as Tawny — manual harvest, foot treading in granite lagares "
        "for premium lots; fortification at 5-6 Baume. "
        "Single-harvest segregation: all Colheita barrels are maintained under vintage tracking "
        "from first year of wood to bottling — the provenance chain is unbroken. "
        "Wood ageing: 550L pipes; the same Gaia lodge system as blended Tawny. "
        "At Niepoort: 7 to 30+ years in wood before bottling on demand. "
        "Bottling to order: unlike blended Tawny (bottled in advance), "
        "Colheita is bottled to order — a bottle from the 1967 vintage "
        "may have been resting in wood until 2026. "
        "The final wood age is on the back label. "
        "This means two bottles of the same Colheita vintage can have different flavour profiles "
        "depending on when they were bottled — younger bottlings are more primary; "
        "older bottlings are more rancio and concentrated. "
        "The legal requirement: bottling date must appear on the Colheita label alongside the vintage."
    ),
    "cross_tradition_parallels": [
        {
            "tradition": "fortified",
            "beverage": "40yr Tawny Port (same category, blended version)",
            "connection": (
                "Colheita vs 40yr Tawny is the internal Port comparison revealing the tension "
                "between consistency (blended Tawny) and individuality (Colheita). "
                "The 40yr Tawny is always consistent across years; "
                "the Colheita 1985 and Colheita 1994 taste distinctly different "
                "based on the growing season of each year."
            )
        },
        {
            "tradition": "spirits",
            "beverage": "Vintage Armagnac (single year, Armagnac AOC)",
            "connection": (
                "Both are single-year expressions of traditions typically sold as age-averaged blends. "
                "The vintage Armagnac and Colheita Port communicate the same message: "
                "that the individual year carries provenance, weather, and terroir "
                "that no blend can replicate."
            )
        },
        {
            "tradition": "fortified",
            "beverage": "Garrafeira Port (same house)",
            "connection": (
                "Colheita (wood only, bottled when ready) vs Garrafeira (wood then glass) — "
                "the Niepoort house comparison illuminating how the maturation path "
                "after the wood phase defines the final character. "
                "Colheita is fully oxidative; Garrafeira is oxidative-then-reductive."
            )
        },
        {
            "tradition": "wine",
            "beverage": "Vintage Champagne (Dom Perignon, late disgorgement 20yr+)",
            "connection": (
                "Both communicate a single year held in the cellar as a deliberate act of patience. "
                "The luxury positioning is identical; the production logic (single harvest, "
                "extended maturation, release when ready) is the same premium philosophy "
                "applied to different traditions."
            )
        }
    ],
    "sensory_profile": {
        "appearance": "Warm amber-tawny at 20yr; deeper mahogany-amber at 40yr; colour shifts with each additional decade of wood maturation",
        "nose": "Vintage-specific: 1985 Colheita shows more tobacco and dried fig; 1967 shows more rancio and volatile dried citrus. The year is in the nose.",
        "palate": "Higher acid backbone than blended Tawny — the vintage year preserves year-specific structural character that blending averages out; sweetness calibrated to the vintage",
        "texture": "Comparable to blended 40yr Tawny in glycerous structure, but vintage character creates individual inflection points in the flavour development",
        "finish": "90-120 seconds; the finish carries the vintage year's character — mineral-driven years produce saline finishes; riper years produce more caramel and dried fruit",
        "conclusion": "The Tawny Port category's most communicable wine — the vintage date is the most powerful service conversation starter in the fortified category"
    },
    "quality_hierarchy": [
        {
            "tier": 4,
            "tier_name": "Niepoort Colheita 1967 or pre-1970",
            "criteria": "50+ year wood age; rancio at maximum development; volatile dried-floral at full expression; "
                "most profound Colheita expression; bottled to order from surviving barrels",
            "markers": "Niepoort Colheita 1967; US ~$200-300+ via Broadbent; BC: private import required"
        },
        {
            "tier": 3,
            "tier_name": "Niepoort Colheita 1985-1995 (30yr+ wood)",
            "criteria": "30+ year wood; rancio well established; vintage character fully integrated; "
                "the practical premium expression for fine dining programme use",
            "markers": "Niepoort Colheita 1985-1995 vintage; US ~$120-180; BC: private order"
        },
        {
            "tier": 2,
            "tier_name": "Niepoort Colheita 2000-2010 (15-25yr wood)",
            "criteria": "15-25 year wood; rancio developing; primary fruit still visible; "
                "the expression that teaches guests how the style evolves over time",
            "markers": "Niepoort Colheita 2000s vintage; US ~$80-120 via Broadbent; BC: private order"
        },
        {
            "tier": 1,
            "tier_name": "Ramos Pinto Quinta do Bom Retiro Colheita (7-10yr)",
            "criteria": "Minimum designation age (7yr); rancio beginning; fresh fruit still dominant; "
                "introduction to Colheita category at accessible price",
            "markers": "Ramos Pinto Colheita (recent vintage); BC ~$45-65; US ~$40-55; BCLDB listed"
        }
    ],
    "service_intelligence": {
        "temperature": "Serve at 14-16 degrees C — slightly warmer than blended Tawny to open the vintage-specific volatile character",
        "vessel": "White wine glass (not Port glass) — the wider bowl essential for the vintage-specific nose to develop fully",
        "technique": "The Colheita service script: 'This is the harvest of [year]. "
            "The wine has been in barrel in the Niepoort lodge since that year. "
            "This bottle was filled [X months] ago — it has spent [X] years in wood.' "
            "The year as guest hook: offer to serve a vintage from the guest's birth year, "
            "graduation, or anniversary year when available — "
            "the personalisation is the most powerful service moment in the fortified category.",
        "programme_position": "Birth year gift programme; milestone anniversary pairing; fine Port vertical anchor; cellar programme signature",
        "verbal_presentation": "Niepoort Colheita [year] — bottled from single harvest. "
            "The wood has been adding its work since [year]. "
            "This is what that year tastes like now."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Niepoort — the definitive Colheita house; holds stocks from 1934 onward",
        "producer_location": "Vila Nova de Gaia, Porto, Portugal",
        "key_person": "Dirk Niepoort; cellarmaster maintains vintage inventory from pre-war stocks",
        "bc_distributor": "No current BCLDB listing for Niepoort Colheita; private import required",
        "us_distributor": "Broadbent Selections (New York) — primary US importer for Niepoort portfolio",
        "uk_distributor": "Les Caves de Pyrene, Fine and Rare (London), Berry Bros. and Rudd",
        "price_tier": "Entry: $45-65 (Ramos Pinto Colheita recent). Mid: $80-120 (Niepoort 2000s). Premium: $120-180 (Niepoort 1985-95). Ultra: $200-300+ (Niepoort pre-1970).",
        "availability_notes": "Niepoort Colheita availability shifts annually as stocks are bottled to order. "
            "Contact Broadbent Selections for current vintage availability. "
            "Some vintages permanently sold out — 1934 stock confirmed exhausted."
    },
    "food_pairings": [
        {
            "technique_id": "",
            "dish": "Pasteis de nata (Portuguese custard tart, fresh from oven)",
            "pairing_type": "complement",
            "rationale": "The caramelised custard of a fresh pasteis de nata "
                "mirrors the dried apricot and caramel character of 20yr Colheita — "
                "the canonical Portuguese bakery-and-fortified pairing "
                "that communicates PCT heritage directly through flavour."
        },
        {
            "technique_id": "",
            "dish": "Roquefort with quince paste (marmelo)",
            "pairing_type": "contrast",
            "rationale": "The salt and fat of Roquefort find contrast in Colheita's acid and sweetness — "
                "the quince paste bridges the two by sharing the dried fruit register "
                "with the wine while amplifying the blue cheese salt intensity."
        }
    ],
    "source": "IVDP Colheita category technical specifications; "
        "Niepoort vintage inventory documentation; "
        "Broadbent Selections US allocation catalogue 2024; "
        "BCLDB product listings verified April 2026",
    "trail_connection": "PCT-1",
    "trail_note": "PCT Region 1: Portugal (Douro). Colheita Port is the individual vintage expression "
        "of the Portuguese fortified tradition that British-Portuguese trade created. "
        "The oldest surviving Niepoort Colheita stocks (1934) pre-date WWII — "
        "evidence that even the catastrophes of the 20th century could not interrupt "
        "the four-century continuity of Port wine production."
})

session.commit_batch()

session.finish()
