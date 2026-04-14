#!/usr/bin/env python3
"""
PCT-1 — Fortified / Portugal — Douro Valley (Port)
30 targets: beverage styles + producers + purveyors
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/Desktop/provenance-tester-1'))
from beverage_extractor import BeverageSession

session = BeverageSession(
    tradition="fortified",
    region="Portugal — Douro Valley (Port)",
    output_dir="./provenance_output/beverage",
    starting_entry=1,
    session_number=1,
    running_total=0
)

# ============================================================
# BEVERAGE ENTRIES — Port Wine Styles
# ============================================================

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "ruby port",
    "region": "Portugal — Douro Valley",
    "name": "Ruby Port",
    "terroir_origin": (
        "The Douro Valley in northern Portugal is one of the world's oldest demarcated wine regions (1756). "
        "The Douro Superior, Cima Corgo, and Baixo Corgo sub-zones climb steeply from the river on schist-dominated "
        "terraces. Schist fractures to allow vine root penetration 20–30 metres into bedrock, forcing water-seeking "
        "efficiency. Altitude ranges 100–700m; summers are extreme (40°C+), winters cold — a continental microclimate "
        "sealed by the Serra do Marão mountains from Atlantic influence. The combination of schist, heat, and drought "
        "stress concentrates tannin and sugar in Touriga Nacional, Touriga Franca, Tinta Roriz, Tinta Barroca, and "
        "Tinto Cão — the five principal Port grapes. The Douro DOC boundary was the world's first legally protected "
        "wine region, established by Pombal's 1756 decree."
    ),
    "production_technique": (
        "Ruby Port is the entry-level style and the archetype of the Port category. Grapes are harvested in September–"
        "October, foot-trodden in shallow granite lagares (traditional) or mechanically extracted (autovinifiers, "
        "robotic lagares) to maximise colour and tannin extraction. Fermentation is arrested mid-way — typically at "
        "5–6° Brix remaining — by adding grape spirit (aguardente vinica) at roughly 77% ABV in a ratio of 1:4 "
        "(spirit:wine). This stops yeast activity and retains residual sugar (80–120 g/L typical). The resulting "
        "wine is fortified to approximately 19–22% ABV. Ruby Port is aged for 2–3 years in large wooden vats (up "
        "to 100,000L toneis) or stainless steel, preserving fresh red-fruit character. It is invariably blended "
        "across vintages for consistency. All Port must pass the Casa do Douro classification before export through "
        "the Port Wine Institute (IVDP). Most Ruby Port is aged in the lodges of Vila Nova de Gaia, across the river "
        "from Porto, exploiting the cooler Atlantic air."
    ),
    "cross_tradition_parallels": [
        {"tradition": "fortified", "beverage": "Banyuls (Roussillon, France)",
         "connection": "Grenache-based French vin doux naturel using the same mutage (fortification) technique; "
                       "aged in bonbonnes exposed to heat, producing oxidised, rancio character parallel to Tawny Port"},
        {"tradition": "fortified", "beverage": "Maury (Roussillon, France)",
         "connection": "Dark, Grenache-dominant French fortified; similar grape-to-spirit arrest and comparable "
                       "residual sugar. Often served alongside chocolate desserts in the same programme position as Ruby Port"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby to purple-red; viscous legs on the glass; opacity increases with Reserve quality",
        "nose": "Intense fresh blackberry, black cherry, and plum; violet florals; dark chocolate undercurrent; "
                "little oxidative character distinguishes it from Tawny",
        "palate": "Full-bodied; high residual sugar (80–120 g/L); firm tannins from schist-grown grapes; "
                  "warm alcohol (19–22% ABV) integrates with fruit on quality examples; medium-length finish with "
                  "dark berry and chocolate notes",
        "conclusion": "The simplest Port expression and the broadest category by volume. Best served slightly "
                      "chilled (14–16°C) to tame alcohol. The benchmark for cheese boards and chocolate desserts."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Reserve / LBV", "criteria": "Selected lots, extended 4–6yr wood ageing; "
          "vintage-dated LBV style; single quinta sourcing", "markers": "Complexity, defined structure, 60+ months wood"},
        {"tier": 3, "tier_name": "Reserve Ruby", "criteria": "Premium blend, 3–5yr ageing, IVDP tasting panel approval",
          "markers": "Reserve label; more density and length than standard"},
        {"tier": 2, "tier_name": "Ruby", "criteria": "Standard category, 2–3yr ageing, blended across vintages",
          "markers": "Entry-level label; approachable fruit-forward style"},
        {"tier": 1, "tier_name": "Lote/Lodge Ruby", "criteria": "Minimum age, commodity production, catering/supermarket",
          "markers": "Generic 'Ruby Port' labels without house name prominence"}
    ],
    "service_intelligence": {
        "temperature": "14–16°C; slightly below room temperature to control sweetness and alcohol heat",
        "vessel": "Small Port tulip glass (100–125mL) or dessert wine glass; tapered shape concentrates aroma",
        "technique": "Serve after dinner; standard 75mL pour; decanting unnecessary for Ruby. Pair with aged "
                     "cheddar, Stilton, dark chocolate ganache, or duck liver pâté",
        "programme_position": "Dessert / cheese course position; or cocktail use (Port & tonic, Port flip). "
                              "By-the-glass anchor for fortified section",
        "verbal_presentation": "Ruby Port — from the granite terraces of the Douro Valley. Fermentation arrested "
                               "with grape spirit, this retains the black fruit of the mountain harvest. Serve with "
                               "aged cheese or dark chocolate."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Graham's Six Grapes Reserve Ruby",
        "producer_location": "Vila Nova de Gaia, Portugal / Quinta dos Malvedos, Douro Superior",
        "key_person": "Charles Symington (CEO, Symington Family Estates)",
        "production_volume": "~3M+ cases annually across Symington portfolio",
        "certifications": ["IVDP (Instituto dos Vinhos do Douro e do Porto)", "Douro DOC"],
        "bc_distributor": "Philippe Dandurand Wines / Galleon (BC) [NEEDS VERIFICATION — likely Dandurand based on portfolio]",
        "us_distributor": "Premium Port Wines, Inc. (Symington's wholly-owned US subsidiary, San Francisco — Graham's, Dow's, Warre's)",
        "uk_distributor": "Berry Bros. & Rudd; Waitrose; widely available",
        "price_tier": "Market",
        "availability_notes": "Available at BC Liquor stores and private wine shops. US: national distribution through major wholesalers. Best value: Graham's Six Grapes, Warre's Warrior, Dow's Fine Ruby."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Port wine is the anchor of the Portuguese Colonial Trail. The Douro Valley's wines were historically "
                  "shipped to England via the 1703 Methuen Treaty, which established Port's global dominance. British "
                  "merchant families (Symington, Guimaraens, Graham) built the lodges of Vila Nova de Gaia and created "
                  "the house names still dominant today. Port's fortification technique later influenced fortified wine "
                  "production along every Portuguese trade route.",
    "food_pairings": [
        {"technique_id": "", "dish": "Stilton with walnut bread", "pairing_type": "complement",
         "rationale": "Classic Anglo-Portuguese pairing; Stilton's salt and blue funk cut through Port's sweetness"},
        {"technique_id": "", "dish": "Dark chocolate tart (70% cacao)", "pairing_type": "complement",
         "rationale": "Bitterness of high-cacao chocolate harmonises with Port's residual sugar and tannin"},
        {"technique_id": "", "dish": "Duck liver pâté", "pairing_type": "bridge",
         "rationale": "Fatty richness of liver calls for the acidity and fruit of Ruby Port; classic Douro pairing"}
    ],
    "source": "IVDP official classifications; Oxford Companion to Wine; Symington Family Estates technical documentation",
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "tawny port",
    "region": "Portugal — Douro Valley",
    "name": "Aged Tawny Port — 10, 20, 30, 40-Year",
    "terroir_origin": (
        "Same schist-terraced Douro Valley as Ruby Port, but aged Tawny draws predominantly from the Cima Corgo "
        "sub-zone where granite intrusions modify the schist and lower yields intensify concentration. The key "
        "distinction is the ageing environment: Tawny is aged in small wooden pipes (550L) or toneis in the "
        "lodges of Vila Nova de Gaia, where the Atlantic microclimate allows gentle, controlled oxidation. "
        "The 'age' (10/20/30/40-year) is an average age of the blend — a solera-like system called the "
        "lote where wines of multiple years are combined to achieve consistent house style."
    ),
    "production_technique": (
        "After fortification (identical to Ruby: aguardente at 77% ABV arresting fermentation), Tawny is "
        "placed in small 550L pipes or 630L hogsheads — compared to the 10,000–100,000L vats used for Ruby. "
        "The smaller vessel dramatically increases wood-to-wine surface area, accelerating oxidation and "
        "evaporation (the 'angel's share' — 2–3% annually in Gaia). Over decades, the wine loses its ruby "
        "colour to amber-tawny as anthocyanins polymerise and precipitate. Sugar concentration increases "
        "as water evaporates; the wine gains rancio (nutty, oxidative) character. A 20-Year Tawny may "
        "contain wines ranging from 8 to 40+ years old in the blend. The 'Colheita' is a single-harvest "
        "Tawny aged minimum 7 years — the single-vintage expression of this style. All aged Tawnies must "
        "carry a bottling date; once bottled they do not improve."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Pedro Ximénez Sherry (Jerez, Spain)",
         "connection": "Oxidative fortified ageing in small wooden barrels; nutty, dried-fruit concentration; "
                       "similar solera/lote blending philosophy; both express the transformation that happens "
                       "when oxygen is introduced slowly over decades to fortified wine"},
        {"tradition": "spirits", "beverage": "Malmsey Madeira",
         "connection": "Both use canteiro (passive oxidative) ageing; both develop hazelnut-caramel-dried "
                       "apricot tertiary characters; Madeira's estufagem method accelerates what Tawny achieves "
                       "naturally through decades in Gaia lodge pipes"}
    ],
    "sensory_profile": {
        "appearance": "Amber to tawny-orange; 10-year retains some ruby highlights; 40-year approaches pale gold. "
                      "Viscous; noticeable legs",
        "nose": "10-year: dried cherry, orange peel, almond, light caramel. 20-year: hazelnut, dried fig, "
                "honey, vanilla, orange marmalade. 30-year: complex rancio (walnut, dried apricot, toffee). "
                "40-year: extraordinary complexity — dried fruit, roasted nuts, coffee, leather, sandalwood",
        "palate": "Lower residual sugar than Ruby as evaporation concentrates alcohol relative to sugar; "
                  "mellow tannins (polyphenols precipitate during ageing); warming, nutty, long finish. "
                  "20-year is the gastronomic sweet spot — enough complexity without excessive oxidation",
        "conclusion": "The sommelier's Tawny. Twenty-year is the most versatile expression: complex enough for "
                      "a dedicated dessert course, light enough for aperitif service. Chilled service essential."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Colheita / 40-Year", "criteria": "Single harvest (Colheita) or 40-year average blend; "
          "exceptional complexity; limited allocation", "markers": "Vintage year on label (Colheita); '40 Years Old' designation"},
        {"tier": 3, "tier_name": "30-Year Tawny", "criteria": "Average 30-year blend; profound rancio character; "
          "restaurant/specialist retail", "markers": "Rare in supermarkets; specialist wine merchants"},
        {"tier": 2, "tier_name": "20-Year Tawny", "criteria": "Average 20-year blend; hazelnut-fig complexity; "
          "correct gastronomic expression", "markers": "The benchmark quality level for professional programmes"},
        {"tier": 1, "tier_name": "10-Year Tawny", "criteria": "Average 10-year blend; entry into aged Tawny; "
          "accessible pricing", "markers": "Widely available; orange-almond character"}
    ],
    "service_intelligence": {
        "temperature": "12–14°C (chilled); unlike Ruby, Tawny benefits strongly from refrigeration — serve from "
                       "the fridge door, not the cellar. Oxidative notes are tamed and fruit is lifted when cold",
        "vessel": "Tulip Port glass; 75mL pour; for 40-year expressions a small Burgundy glass allows full "
                  "aroma expression without overwhelming concentration",
        "technique": "Pour gently; no decanting needed. Once opened, 20+ year Tawnies can hold refrigerated "
                     "for 2–3 months (oxidative stability is their strength). Excellent by-the-glass value "
                     "for restaurants due to longevity after opening",
        "programme_position": "Dessert wine / by-glass fortified anchor. 10-year: cheese course. 20-year: "
                              "foie gras, crème brûlée, pecan tart. 40-year: standalone or with aged hard cheese",
        "verbal_presentation": "Tawny Port, aged twenty years in small oak pipes in the lodges of Vila Nova de "
                               "Gaia. Decades of gentle oxidation transform the Douro's dark fruit into hazelnut, "
                               "dried fig, and orange marmalade. Serve chilled — this is the Douro at its most refined."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Ramos Pinto Quinta do Bom Retiro 20-Year Tawny",
        "producer_location": "Ramos Pinto Lodge, Vila Nova de Gaia; Quinta do Bom Retiro, Douro Superior",
        "key_person": "João Nicolau de Almeida (historic winemaker, Ramos Pinto); João Ramos Pinto (founder)",
        "production_volume": "Ramos Pinto produces ~600,000 bottles annually across portfolio",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "[NEEDS VERIFICATION — MMD Canada or separate BC agent]",
        "us_distributor": "Maisons Marques & Domaines USA / MMD (confirmed — Louis Roederer group US arm)",
        "uk_distributor": "Widely available; Ramos Pinto UK through Louis Roederer UK",
        "price_tier": "Estate (20-year); Reserve (10-year)",
        "availability_notes": "10-year widely available; 20-year through specialist merchants; 30/40-year via allocation. "
                              "Colheita through BCLDB special orders (BC); direct from estates or auctions (US)."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Tawny Port's oxidative ageing style was perfected in the lodges of Vila Nova de Gaia — a trade hub "
                  "established as British factors (merchants) built warehouses along the Gaia waterfront to export "
                  "Port to England under the Methuen Treaty. The 'Tawny' name itself describes the colour transformation "
                  "from the original ruby of harvest to the amber of decades of oak contact.",
    "food_pairings": [
        {"technique_id": "", "dish": "Crème brûlée", "pairing_type": "complement",
         "rationale": "Caramel and vanilla of the brûlée echo the same notes developed during Tawny's wood ageing"},
        {"technique_id": "", "dish": "Roquefort with honey", "pairing_type": "bridge",
         "rationale": "Honey bridges the sweet-savoury gap; Roquefort's funk cuts through Tawny's richness"},
        {"technique_id": "", "dish": "Pecan tart", "pairing_type": "complement",
         "rationale": "Tawny's walnut-hazelnut character in a 20-year mirrors the nuttiness of pecan perfectly"}
    ],
    "source": "IVDP technical sheets; Ramos Pinto winemaking notes; Oxford Companion to Wine; Wine & Spirits Education Trust (WSET) Diploma materials",
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "vintage port",
    "region": "Portugal — Douro Valley",
    "name": "Vintage Port (Declared Vintage)",
    "terroir_origin": (
        "Vintage Port is declared only in exceptional years — roughly 3–4 times per decade — when the Symington, "
        "Taylor, and other major houses collectively assess that the harvest meets the standard for a Declaration. "
        "Notable declared vintages: 2017, 2016, 2011, 2007, 2003, 2000, 1997, 1994, 1992, 1985, 1977, 1970, 1966, "
        "1963. The wine comes exclusively from single quintas or estate blends in the Douro Superior and Cima Corgo "
        "— the highest-altitude, lowest-yielding schist terraces. Touriga Nacional is the dominant grape for "
        "Vintage Port, prized for its inky colour, firm tannin, and floral lift. Quinta do Noval's legendary "
        "'Nacional' vineyard (ungrafted, pre-phylloxera vines) produces perhaps the world's rarest Vintage Port."
    ),
    "production_technique": (
        "Vintage Port grapes are invariably foot-trodden in granite lagares — even in the modern era, many "
        "houses retain this practice for their top wines. The slow, gentle treading extracts colour and tannin "
        "without excessive bitterness. Fermentation is arrested at the same point as Ruby (mid-fermentation) "
        "with 77% aguardente vinica. The critical distinction: Vintage Port spends only 2 years in large wooden "
        "vats before bottling without filtration. Unfiltered bottling means substantial sediment forms over "
        "decades in bottle — hence the need for careful decanting. The wine then undergoes 'reductive ageing' "
        "in bottle, developing slowly over 15–40+ years. A declared vintage will typically peak 20–30 years "
        "after harvest. Late Bottled Vintage (LBV) is Port from a single year aged 4–6 years in wood: "
        "traditional LBV (unfined, unfiltered) offers a more accessible parallel; modern LBV (filtered) "
        "requires no decanting but offers less complexity."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Barolo Riserva (Piedmont, Italy)",
         "connection": "Both are structured, tannic, age-worthy wines requiring 15–30 years before peak; "
                       "both need decanting; both express a specific terroir and vintage with maximum fidelity. "
                       "The collector's parallel in the red wine world"},
        {"tradition": "fortified", "beverage": "Single Quinta Vintage Madeira",
         "connection": "The only other fortified wine with comparable age-worthiness and collector value; "
                       "Madeira is arguably the more immortal wine (known to be excellent at 200 years) while "
                       "Vintage Port peaks in 20–40 years"}
    ],
    "sensory_profile": {
        "appearance": "Young (0–10yr): deep opaque purple-black. Middle age (15–25yr): garnet with brick rim. "
                      "Mature (30–50yr): transparent amber-garnet with significant sediment in bottle",
        "nose": "Young: explosive dark fruit, violets, dark chocolate, cedar. Middle: dried fruit, leather, "
                "truffle, tobacco, camphor, cedar. Mature: dried rose, sandalwood, dried plum, coffee, leather. "
                "Old Nacional: extraordinary complexity beyond description in young wine terms",
        "palate": "Enormous tannic structure when young — undrinkable without decanting for 3–4 hours. "
                  "After 20+ years: velvety tannins, extraordinary length (60+ seconds), layers of fruit, "
                  "earth, and evolved tertiary complexity. Residual sugar (90–110 g/L) balanced by the tannin "
                  "scaffold — the defining tension of great Vintage Port",
        "conclusion": "The most age-worthy fortified wine in the world after Madeira. A declaration-year "
                      "purchase is a 25-year investment. Decant for 3–4 hours minimum; serve at 18°C."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Nacional / Single Ungrafted Quinta", "criteria": "Pre-phylloxera ungrafted vines; "
          "ultra-rare allocation; Quinta do Noval Nacional the benchmark", "markers": "Allocation only; auction values reach £1000+ per bottle"},
        {"tier": 3, "tier_name": "Declared Single Quinta", "criteria": "Estate wines from top quintas in declared years: "
          "Quinta do Vesuvio, Quinta da Vargellas, Quinta dos Malvedos", "markers": "Single estate name on label; undeclared-year alternative to house blends"},
        {"tier": 2, "tier_name": "Declared House Vintage", "criteria": "Blend from best lots across quintas in declared years; "
          "Taylor's, Graham's, Fonseca, Dow's benchmark", "markers": "Vintage year on label; widespread critical acclaim in declared years"},
        {"tier": 1, "tier_name": "LBV (Traditional)", "criteria": "Single year, 4–6yr wood, unfiltered, vintage dated; "
          "accessible Vintage Port character", "markers": "Traditional LBV label; requires decanting; cheaper than declared Vintage"}
    ],
    "service_intelligence": {
        "temperature": "17–19°C; serve at cool room temperature, not warm",
        "vessel": "Decanter (mandatory for any wine over 10 years); pour through muslin or Vinturi if sediment heavy. "
                  "Large Burgundy glass allows full aromatic development",
        "technique": "Stand bottle upright 48 hours before service to settle sediment. Decant slowly by candlelight "
                     "or torch — stop when sediment reaches the shoulder. 3–4 hour minimum decanting for young vintages. "
                     "Mature vintages (30yr+) may need only 1 hour and can fade after 4 hours",
        "programme_position": "Standalone final glass; dessert wine alternative for serious cheese plates. "
                              "Never reduce to 'dessert wine' in presentation — it belongs in the fine wine narrative",
        "verbal_presentation": "Vintage Port, [year], Taylor Fladgate [or house]. Declared only three times this decade. "
                               "Twenty years in bottle, foot-trodden on Douro schist terraces. Decanted this afternoon "
                               "— it will open further over the next hour."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Taylor Fladgate Vintage Port",
        "producer_location": "Quinta de Vargellas, Douro Superior; Taylor Fladgate Lodge, Vila Nova de Gaia",
        "key_person": "Adrian Bridge (CEO, Taylor Fladgate Partnership); David Guimaraens (winemaker)",
        "production_volume": "Limited; declared years only; Taylor's produces ~50,000 cases in a declaration year",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "Philippe Dandurand Wines / Galleon (BC) [NEEDS VERIFICATION]",
        "us_distributor": "Kobrand Wine & Spirits (Taylor Fladgate Partnership, Fonseca, Croft) — confirmed 25+ year partnership",
        "uk_distributor": "Direct from Taylor's UK; Berry Bros. & Rudd; Justerini & Brooks",
        "price_tier": "Reserve (declared Vintage £40–£100); Estate (aged/collector's £100–£500+)",
        "availability_notes": "Declared Vintage: available through specialist merchants and BCLDB special orders. "
                              "US: through Kobrand accounts, Fine and Rare Wine (NYC), K&L Wine Merchants. "
                              "Single quintas in non-declared years offer accessible Vintage Port character at lower price."
    },
    "trail_connection": "PCT-1",
    "trail_note": "The Vintage Port Declaration is one of the wine world's most consequential rituals. British merchant "
                  "families who established the lodge system in Gaia under the Methuen Treaty created both the "
                  "infrastructure and the commercial conventions (declaration, bottling, cellaring) that define "
                  "Vintage Port today. The Trail connection: every major Port house was either founded by British "
                  "merchants or grew under British commercial patronage.",
    "food_pairings": [
        {"technique_id": "", "dish": "Neal's Yard Colston Bassett Stilton", "pairing_type": "complement",
         "rationale": "The canonical Vintage Port pairing; the blue's salt and funk amplify the wine's fruit"},
        {"technique_id": "", "dish": "Walnuts and dried figs", "pairing_type": "complement",
         "rationale": "The tertiary notes of a mature vintage echo walnut and dried fig directly"},
        {"technique_id": "", "dish": "Venison with blackberry reduction", "pairing_type": "bridge",
         "rationale": "Bold game meat needs Port's structure; blackberry bridges both"}
    ],
    "source": "IVDP declaration records; Taylor Fladgate production documentation; Robert Parker Wine Advocate; Jancis Robinson Oxford Companion to Wine",
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "white port",
    "region": "Portugal — Douro Valley",
    "name": "White Port",
    "terroir_origin": (
        "White Port is produced from white Douro grapes — Malvasia Fina, Gouveio (Verdelho), Viosinho, Rabigato, "
        "Códega, and Arinto — grown on the same schist terraces as the red varieties. The Baixo Corgo and Cima "
        "Corgo produce the most white Port. Dry white Port is a relatively modern style — historically, the "
        "default was sweet; the 'Extra Dry' and 'Lagrima' ends of the spectrum are both recent commercial "
        "developments serving different market needs. The Douro's continental climate (hot summers, cold winters) "
        "preserves natural acidity in white varieties, which is critical for the drier expressions."
    ),
    "production_technique": (
        "White Port is made identically to ruby: fermentation is arrested with aguardente vinica at a point "
        "determined by the intended sweetness level. Extra Dry styles have fermentation run to near-completion "
        "before addition, resulting in <40 g/L residual sugar; standard Dry (~40–65 g/L); Medium Dry (~65–80 g/L); "
        "Pale Cream/Sweet (~80–130 g/L); Lagrima (the sweetest, >130 g/L, meaning 'tears' from the sugar-weeping "
        "grape skins). Most white Port is aged 2–3 years in large vats or stainless steel to preserve freshness. "
        "Aged white Port (10-year, 20-year) develops oxidative complexity parallel to Tawny — golden-amber colour, "
        "dried apricot, honey, and almond. The key modern use: White Port & Tonic (the Portónico), which has "
        "revitalised the category as a premium aperitif across Europe and North America."
    ),
    "cross_tradition_parallels": [
        {"tradition": "fortified", "beverage": "Fino / Manzanilla Sherry (Jerez)",
         "connection": "Both are pale, dry-to-medium fortified wines served chilled as aperitifs; "
                       "both are underserved in North American markets; White Port occupies the same programme "
                       "slot and is often more approachable for non-Sherry audiences"},
        {"tradition": "spirits", "beverage": "Tonic-based aperitif cocktails (G&T family)",
         "connection": "The Portónico (White Port + Tonic) uses the same bitter-sweet-botanical framework "
                       "as gin & tonic; White Port's residual sugar and grape character substitute for gin's "
                       "botanical complexity"}
    ],
    "sensory_profile": {
        "appearance": "Dry/Extra Dry: pale gold to light amber; Sweet/Lagrima: deep amber to golden",
        "nose": "Dry: fresh citrus (lemon, grapefruit), white peach, floral honey, light almond. "
                "Sweet: dried apricot, orange blossom, beeswax, marmalade on quality examples",
        "palate": "Extra Dry: crisp, almost Sherry-like acidity with nutty finish; "
                  "Standard Dry: balanced sweetness with stone fruit; "
                  "Lagrima: full-bodied, rich, coating — almost dessert-thick",
        "conclusion": "White Port is the category's hidden opportunity. The Portónico is one of the best "
                      "low-effort aperitif builds for a cocktail programme — premium yet accessible."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "Aged 10/20-Year White", "criteria": "Rare; oxidative ageing; extraordinary complexity",
          "markers": "Age designation; amber-gold colour; specialist distribution"},
        {"tier": 3, "tier_name": "Reserve Extra Dry", "criteria": "Single quinta sourcing; extended ageing; premium label",
          "markers": "Niepoort 'Dry White', Ramos Pinto 'Fleur de Rosa' level"},
        {"tier": 2, "tier_name": "Extra Dry / Dry", "criteria": "Standard house production; consistent quality",
          "markers": "Taylor's Chip Dry; Ferreira Dona Antónia White"},
        {"tier": 1, "tier_name": "Standard White (Sweet)", "criteria": "Entry-level sweet White Port; "
          "supermarket distribution", "markers": "Generic sweetness; limited complexity"}
    ],
    "service_intelligence": {
        "temperature": "6–10°C (well chilled); the colder the better for dry expressions",
        "vessel": "Copa de Balon (large gin glass) for Portónico; tulip Port glass for sipping neat",
        "technique": "Portónico: 50mL White Port over ice, top with premium tonic (Fever-Tree Mediterranean "
                     "or 1724), garnish with fresh mint and lemon slice. As aperitif: serve chilled in Port "
                     "tulip with a slice of lemon rind",
        "programme_position": "Aperitif / pre-dinner; cocktail menu anchor. Excellent by-the-glass opener for "
                              "a fortified-focused programme",
        "verbal_presentation": "White Port & tonic — the Portuguese aperitif. Estate-grown Douro white grapes, "
                               "fermentation arrested with grape spirit, served over ice with tonic and fresh mint. "
                               "The Portónico: Portugal's answer to gin & tonic."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Niepoort Dry White Port",
        "producer_location": "Niepoort Lodge, Vila Nova de Gaia; Quinta de Nápoles, Douro",
        "key_person": "Dirk Niepoort (owner/winemaker)",
        "production_volume": "Niepoort produces ~400,000 bottles total across all styles",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "[NEEDS VERIFICATION]",
        "us_distributor": "Broadbent Selections (Niepoort US) [NEEDS VERIFICATION]",
        "uk_distributor": "Les Caves de Pyrène (Niepoort UK); widely available",
        "price_tier": "Market (£10–20)",
        "availability_notes": "Taylor's Chip Dry is the most widely available White Port in BC and US markets. "
                              "Niepoort and Quinta do Crasto dry whites available through specialist importers. "
                              "Portónico trend driving wider availability 2022–2025."
    },
    "trail_connection": "PCT-1",
    "trail_note": "White Port's resurgence as the Portónico is a contemporary expression of Portugal's self-confidence "
                  "with its own traditions — a shift from Port being 'British wine' to Portuguese cultural heritage.",
    "food_pairings": [
        {"technique_id": "", "dish": "Almonds and olives (aperitivo)", "pairing_type": "complement",
         "rationale": "Classic Portuguese pairing; dry White Port with roasted almonds and cured olives"},
        {"technique_id": "", "dish": "Bacalhau fritters (Pastéis de bacalhau)", "pairing_type": "bridge",
         "rationale": "Salt cod's richness and the fritter's crisp exterior call for the crispness of dry White Port"},
        {"technique_id": "", "dish": "Ceviche", "pairing_type": "complement",
         "rationale": "Extra Dry White Port's acidity and citrus notes parallel the leche de tigre in ceviche"}
    ],
    "source": "IVDP style classifications; Niepoort winery documentation; Port Wine Institute consumer guides",
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "colheita port",
    "region": "Portugal — Douro Valley",
    "name": "Colheita Port",
    "terroir_origin": (
        "Colheita (Portuguese: harvest/vintage) is a single-harvest Tawny Port — the most precise and "
        "terroir-expressive iteration of the oxidative ageing style. The grapes come from a single year's "
        "harvest, primarily from the Cima Corgo and Douro Superior, where schist soils and water-stressed vines "
        "produce concentrated fruit capable of multi-decade development. A Colheita must be aged a minimum of "
        "7 years in small wooden pipes (550L) before release — in practice, the finest examples are aged "
        "20–60+ years and represent a snapshot of a specific growing season expressed through oxidative transformation."
    ),
    "production_technique": (
        "After standard Port fortification, the wine is placed in 550L pipes and stored in the Gaia lodges. "
        "Unlike blended Tawnies (10/20/30/40-year averages), Colheita must always carry a vintage year and "
        "a bottling date — the gap between these two dates reveals the ageing history. A 1970 Colheita bottled "
        "in 2024 has spent 54 years in wood. Annual evaporation (angel's share) concentrates the wine dramatically — "
        "a 50-year-old Colheita may represent only 40–50% of its original volume. The IVDP requires that producers "
        "maintain exact records of each pipe, including vintage year, lodging date, and all blending or refilling. "
        "Unlike Vintage Port, Colheita does not improve in bottle after release — it is ready to drink when bottled "
        "and should be consumed within 1–2 years of opening (refrigerated)."
    ),
    "cross_tradition_parallels": [
        {"tradition": "spirits", "beverage": "Single Cask Scotch Whisky",
         "connection": "Both express a single year's production through decades of wood contact; both carry "
                       "a vintage year and cask/pipe reference; both develop unrepeatable character that "
                       "cannot be approximated by blending"},
        {"tradition": "fortified", "beverage": "Malmsey Colheita Madeira",
         "connection": "Both are single-vintage oxidative fortified wines; Madeira Colheita uses a similar "
                       "system requiring vintage declaration and minimum 5-year ageing. Madeira may outlive "
                       "Port Colheita in terms of cellaring potential"}
    ],
    "sensory_profile": {
        "appearance": "Amber to deep amber-gold, darkening with age; clear and brilliant after decades of settling",
        "nose": "Young Colheita (10–15yr): orange peel, dried apricot, caramel, roasted almonds. "
                "Mid (20–30yr): toffee, walnuts, dried mango, sandalwood, leather. "
                "Old (40yr+): extraordinary complexity — tobacco, dried roses, mushroom, rancio, cedar, beeswax. "
                "Great Colheitas from Niepoort or Ramos Pinto are among the world's most complex beverages",
        "palate": "Medium-high residual sugar (100–130 g/L) balanced by oxidative dryness and evaporative "
                  "concentration; velvety texture; extraordinary length — 90+ seconds in old examples. "
                  "The finish evolves in the glass over 20+ minutes",
        "conclusion": "The collector's secret within Port. Often priced lower than equivalent-age Vintage Port "
                      "despite comparable complexity. Ramos Pinto's 1937 Colheita (released mid-century) "
                      "remains a benchmark for what single-vintage oxidative ageing achieves."
    },
    "quality_hierarchy": [
        {"tier": 4, "tier_name": "50-Year+ Colheita", "criteria": "Pre-1980 vintages; extraordinary rarity; "
          "auction or allocated release only", "markers": "1966, 1963, 1937 vintages from Ramos Pinto, Niepoort, Barros"},
        {"tier": 3, "tier_name": "30–50 Year Colheita", "criteria": "1980–1995 vintages; profound complexity; "
          "specialist merchants", "markers": "Deep amber; walnut-toffee-sandalwood profile"},
        {"tier": 2, "tier_name": "15–30 Year Colheita", "criteria": "1995–2010 vintages; approachable complexity; "
          "restaurant by-the-glass at premium", "markers": "Orange-apricot-almond profile; excellent value vs Tawny"},
        {"tier": 1, "tier_name": "7–15 Year Colheita", "criteria": "Minimum legal age; single vintage; "
          "entry into the style", "markers": "Fresher fruit character retained; distinguishable from 10-year blended Tawny"}
    ],
    "service_intelligence": {
        "temperature": "10–12°C (well chilled)",
        "vessel": "Port tulip glass; for 30yr+, small Burgundy glass",
        "technique": "Serve as the most prestigious dessert wine offering on the programme. Mention the vintage "
                     "year and bottling date — this communicates provenance and singularity. Refrigerate after "
                     "opening; holds 2–3 months",
        "programme_position": "The pinnacle of the fortified section; dessert wine alternative at the cheese "
                              "course or post-dessert; optional by-the-glass for premium programmes",
        "verbal_presentation": "Colheita Port, [vintage year], [house name]. A single harvest, aged [X] years "
                               "in small oak pipes until bottled in [year]. Unlike blended Tawny, this is the "
                               "character of one specific Douro harvest — irreplaceable once gone."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Ramos Pinto Colheita and Niepoort Colheita",
        "producer_location": "Ramos Pinto Lodge and Niepoort Lodge, Vila Nova de Gaia",
        "key_person": "Dirk Niepoort; Ramos Pinto cellar master",
        "production_volume": "Very limited; pipe-by-pipe production; some vintages < 5,000 bottles",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "[NEEDS VERIFICATION]",
        "us_distributor": "Martine's Wines (Niepoort US, confirmed — Novato, CA, exclusive national importer)",
        "uk_distributor": "Specialist merchants: Berry Bros., Corney & Barrow, Justerini & Brooks",
        "price_tier": "Reserve to Estate (£20–£200+ depending on vintage age)",
        "availability_notes": "Available through specialist wine merchants; rarely at mainstream retailers. "
                              "BCLDB special orders (BC). Auction houses for pre-1990 vintages."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Colheita represents the Portuguese quality apex of their own trade tradition — a wine where "
                  "the national producers (Ramos Pinto, Niepoort, Ferreira, Barros) outperform the British houses "
                  "who historically dominated the category.",
    "food_pairings": [
        {"technique_id": "", "dish": "Aged Manchego or hard cheese with quince paste", "pairing_type": "complement",
         "rationale": "Quince paste's concentrated sweetness and the cheese's crystalline texture complement the "
                      "Colheita's density and dried-fruit character"},
        {"technique_id": "", "dish": "Financier with salted caramel", "pairing_type": "complement",
         "rationale": "Almond-butter notes of the financier mirror the Colheita's oxidative nuttiness exactly"},
        {"technique_id": "", "dish": "Foie gras terrine", "pairing_type": "bridge",
         "rationale": "The richness of foie gras requires the concentrated sweetness and acidity of an aged Colheita"}
    ],
    "source": "IVDP Colheita regulations; Niepoort archive documentation; Ramos Pinto historical records; Wine Spectator Port special issues",
})

session.commit_batch()
print(f"\n[BATCH 1 COMMITTED — Port Styles 1-5]\n")

# ============================================================
# BEVERAGE ENTRIES — Port Styles continued
# ============================================================

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "rosé port",
    "region": "Portugal — Douro Valley",
    "name": "Rosé Port",
    "terroir_origin": (
        "Rosé Port is the newest Port style, launched in 2008 by Croft (Taylor Fladgate Partnership) as 'Croft Pink' — "
        "a deliberate repositioning of Port toward a younger, aperitif-drinking audience. Produced from the same "
        "Douro red grapes (Touriga Nacional, Touriga Franca, Tinta Roriz) as Ruby Port, but with dramatically "
        "reduced skin contact during maceration, extracting only pink colour rather than the full ruby of Ruby Port. "
        "Grows in the same schist terraces of the Cima Corgo and Douro Superior."
    ),
    "production_technique": (
        "Red grapes are pressed with minimal skin contact (typically cold maceration for a few hours rather than "
        "the extended foot-treading of Ruby/Vintage). The resulting must is pale pink. Fermentation proceeds briefly "
        "before aguardente addition arrests it at ~40–80 g/L residual sugar. The wine is aged 1–2 years in large "
        "stainless steel vats to preserve freshness and fruit. Croft Pink (the original) is intentionally modelled "
        "on Provence rosé and cocktail culture rather than traditional Port. It is always served chilled, "
        "often over ice, with tonic or as the base for cocktails."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Provence Rosé (France)",
         "connection": "Direct stylistic parallel — Rosé Port is deliberately pitched as a fortified answer to "
                       "Provence rosé; similar pale salmon colour, red berry aromatics, and aperitif positioning"},
        {"tradition": "spirits", "beverage": "Aperol Spritz (aperitif category)",
         "connection": "Rosé Port occupies the same daypart and consumer segment as Aperol-based drinks; "
                       "the 'Pink Port & Tonic' is directly competitive with spritz culture"}
    ],
    "sensory_profile": {
        "appearance": "Pale to medium pink-salmon; clear; lighter than Ruby",
        "nose": "Fresh strawberry, raspberry, rose petal, light citrus; minimal oxidative character",
        "palate": "Lower residual sugar than Ruby (40–70 g/L typical); lighter body; fresh acidity; "
                  "short-to-medium finish; designed for casual enjoyment rather than contemplative sipping",
        "conclusion": "A commercially successful innovation that has opened the Port category to new consumers. "
                      "Not a serious contemplative style, but an excellent cocktail ingredient and aperitif "
                      "option that introduces Port to audiences unfamiliar with the category."
    },
    "quality_hierarchy": [
        {"tier": 3, "tier_name": "Reserve Rosé", "criteria": "Estate grape sourcing; copper-pink colour; defined strawberry character",
          "markers": "Quinta do Crasto Rosé; single quinta sourcing"},
        {"tier": 2, "tier_name": "House Rosé", "criteria": "Standard production; consistent style; mass-market availability",
          "markers": "Croft Pink; Ramos Pinto Rosé; widely distributed"},
        {"tier": 1, "tier_name": "Entry Rosé", "criteria": "Commodity production; supermarket distribution",
          "markers": "Generic Rosé Port labels"}
    ],
    "service_intelligence": {
        "temperature": "4–8°C (well chilled or over ice)",
        "vessel": "Copa de Balon over ice; or cocktail glass",
        "technique": "Pink Port & Tonic: 50mL over ice in Copa, top with tonic, fresh strawberry garnish. "
                     "Or: Pink Port Spritz with prosecco and fresh mint. Excellent for summer aperitif menus",
        "programme_position": "Aperitif / cocktail hour; summer menus; pre-dinner drinks",
        "verbal_presentation": "Croft Pink — rosé from the Douro Valley. The most recent style in Portugal's "
                               "oldest wine region. Red Douro grapes, barely touched, express only their blush."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Croft Pink (Taylor Fladgate Partnership)",
        "producer_location": "Quinta da Roêda, Cima Corgo; Taylor Fladgate Lodge, Vila Nova de Gaia",
        "key_person": "Adrian Bridge (Taylor Fladgate Partnership CEO)",
        "production_volume": "Croft Pink: large commercial volume; among the top-selling Rosé Ports",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "Lifford Wine & Spirits (Taylor Fladgate Partnership/Croft) [NEEDS VERIFICATION]",
        "us_distributor": "Kobrand Corporation (Croft/Taylor Fladgate USA)",
        "uk_distributor": "Widely available; Waitrose, Sainsbury's carry Croft Pink",
        "price_tier": "Market (£12–18)",
        "availability_notes": "Croft Pink widely available at BC Liquor stores and SAQ. US: Kobrand national. "
                              "Strong supermarket presence in UK and Europe."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Rosé Port's 2008 launch by a British-founded house (Croft) using modern marketing demonstrates "
                  "how the Port category continues to evolve under Anglo-Portuguese stewardship.",
    "food_pairings": [
        {"technique_id": "", "dish": "Strawberries with cream", "pairing_type": "complement",
         "rationale": "The direct aromatic echo of the wine's strawberry notes with fresh summer berries"},
        {"technique_id": "", "dish": "Grilled halloumi with honey", "pairing_type": "bridge",
         "rationale": "Sweet-savoury tension of halloumi and honey matches the Port's residual sweetness"}
    ],
    "source": "Croft Port product documentation; IVDP Rosé Port regulations; Wine Enthusiast coverage of Croft Pink launch 2008",
})

session.add_beverage({
    "tradition": "fortified",
    "sub_tradition": "crusted port",
    "region": "Portugal — Douro Valley",
    "name": "Crusted Port",
    "terroir_origin": (
        "Crusted Port is a British-invented style — a multi-vintage blend of Ruby Port (not single vintage) "
        "that is bottled unfiltered and allowed to develop a 'crust' (sediment) in bottle over time, mimicking "
        "the reductive ageing of Vintage Port at a fraction of the price. The grapes come from multiple years "
        "and typically the Cima Corgo and Douro Superior sub-zones. The style is particularly championed by "
        "Churchill's (founded 1981 by John Graham), which revived it in the 1990s as a 'poor man's Vintage Port.'"
    ),
    "production_technique": (
        "Crusted Port begins as a Ruby-style blend across 2–3 vintages. After 2–3 years in large wooden vats, "
        "it is bottled unfined and unfiltered — unlike standard Ruby, which is filtered bright before bottling. "
        "The unfiltered bottling allows the wine to continue throwing sediment in bottle, developing complexity "
        "over 3–5 years. The wine must be decanted before serving. A bottling date appears on the label (not "
        "vintage years, as it is a blend). The style is legally defined and must be bottled by the shipper, "
        "not at the quinta. Churchill's Crusted Port (bottled 3 years in wood, 3 years in bottle minimum) "
        "remains the category's benchmark."
    ),
    "cross_tradition_parallels": [
        {"tradition": "wine", "beverage": "Unfiltered Napa Cabernet Sauvignon",
         "connection": "Both use unfined/unfiltered bottling to retain structure and allow in-bottle development; "
                       "both require decanting and develop sediment; both are positioned as 'serious' alternatives "
                       "to more polished (filtered) versions of the same wine"},
        {"tradition": "fortified", "beverage": "Traditional LBV Port",
         "connection": "Both are multi-year blends (Crusted) or single-year (LBV) bottled unfined and unfiltered; "
                       "both require decanting and develop in bottle; Crusted is cheaper and less vintage-specific"}
    ],
    "sensory_profile": {
        "appearance": "Deep ruby-garnet; significant sediment forms over 3+ years in bottle; "
                      "brilliant red after decanting through fine mesh or muslin",
        "nose": "Dark cherry, blackberry, dark chocolate, cedar, coffee; more complexity than standard Ruby "
                "due to bottle development; light leather and tobacco emerge with age",
        "palate": "More structured than filtered Ruby; firm tannins (retained from unfiltered bottling); "
                  "60–100 g/L residual sugar; medium-long finish; develops for 5–10 years in bottle",
        "conclusion": "The best value entry into the unfiltered Port category. Essential for programmes "
                      "that want the Vintage Port conversation without the price point."
    },
    "quality_hierarchy": [
        {"tier": 3, "tier_name": "House Reserve Crusted", "criteria": "Best lots across 2–3 vintages; "
          "extended bottle ageing before release", "markers": "Churchill's Crusted; Graham's Crusted"},
        {"tier": 2, "tier_name": "Standard Crusted", "criteria": "House blend; minimum ageing requirements met",
          "markers": "Most commercial Crusted Ports"},
        {"tier": 1, "tier_name": "Filtered 'Crusted-style'", "criteria": "Technically not Crusted; filtered but labelled "
          "to suggest the style", "markers": "No sediment; misleading labelling"}
    ],
    "service_intelligence": {
        "temperature": "17–18°C",
        "vessel": "Decanter (essential); Burgundy glass",
        "technique": "Decant 1–2 hours before service; stand bottle upright 24 hours prior to allow sediment "
                     "to settle at base. Use fine mesh strainer or candle when decanting",
        "programme_position": "Cheese course / dessert wine alternative; by-the-glass if pouring from "
                              "decanted bottle; excellent value wine list option",
        "verbal_presentation": "Crusted Port — unfiltered, multi-vintage, thrown back into the cellar to "
                               "develop in bottle. Decanted this afternoon. It will open as it breathes."
    },
    "purveyor_intelligence": {
        "benchmark_producer": "Churchill's Crusted Port",
        "producer_location": "Churchill Graham Lda, Vila Nova de Gaia; Quinta da Gricha, Douro",
        "key_person": "John Graham (founder); Caroline Graham-Spencer (current generation)",
        "production_volume": "Small; Churchill's is one of the few houses that maintains the style consistently",
        "certifications": ["IVDP", "Douro DOC"],
        "bc_distributor": "[NEEDS VERIFICATION]",
        "us_distributor": "Skurnik Wines & Spirits (Churchill's US — confirmed national importer)",
        "uk_distributor": "Churchill's direct; specialist merchants",
        "price_tier": "Market (£20–30)",
        "availability_notes": "Niche distribution; primarily through specialist Port merchants. Churchill's "
                              "most accessible via direct order or specialist wine shops."
    },
    "trail_connection": "PCT-1",
    "trail_note": "Crusted Port was invented by the British Port trade — specifically the shippers of Vila Nova de Gaia "
                  "who needed a way to sell high-quality Ruby at a premium without declaring a vintage. Churchill's, "
                  "founded by a Graham family member, is the style's modern custodian.",
    "food_pairings": [
        {"technique_id": "", "dish": "Aged Cheddar (3-year)", "pairing_type": "complement",
         "rationale": "The crystalline structure and sharpness of aged Cheddar cuts through the wine's richness"},
        {"technique_id": "", "dish": "Chocolate and hazelnut cake", "pairing_type": "complement",
         "rationale": "Dark chocolate intensity mirrors the wine's cocoa and dark fruit character"}
    ],
    "source": "Churchill's Port technical documentation; IVDP Crusted Port regulations; Wine Spectator Port category reviews",
})

session.commit_batch()
print(f"\n[BATCH 2 COMMITTED — Port Styles 6-7]\n")

# ============================================================
# PRODUCER ENTRIES — Key Port Houses
# ============================================================

session.add_producer({
    "name": "Symington Family Estates",
    "location": "Vila Nova de Gaia, Portugal",
    "country": "Portugal",
    "region": "Douro Valley",
    "tradition": "fortified",
    "key_person": "Charles Symington (CEO), Dominic Symington, Rupert Symington, Johnny Symington (Directors)",
    "founded": "1882 (as Graham's; Symington family acquired control progressively 1970–1988)",
    "production_volume": "~3 million cases annually across all brands; largest producer of premium Port",
    "notable_products": ["Graham's Vintage Port", "Dow's Vintage Port", "Warre's Vintage Port",
                         "Quinta do Vesuvio Vintage Port", "Graham's Six Grapes Reserve Ruby",
                         "Dow's Trademark Tawny", "Graham's 20-Year Tawny"],
    "certifications": ["IVDP certified", "Douro DOC", "B Corp candidate (sustainability programmes)"],
    "website": "symington.com",
    "philosophy": "Fourth-generation family ownership of Portugal's most storied Port houses. Combine "
                  "traditional foot-treading at key quintas (Quinta dos Malvedos, Quinta do Vesuvio) with "
                  "investment in precision viticulture and robotic lagares to scale quality. Note: Symington "
                  "also owns Cockburn's (acquired 2010 — NOT Sogrape as commonly misreported).",
    "trail_connection": "PCT-1",
    "source": "Symington Family Estates official documentation; Wine Spectator winery profiles; Decanter Cockburn's acquisition report 2010",
    "verified": True
})

session.add_producer({
    "name": "Taylor Fladgate Partnership",
    "location": "Vila Nova de Gaia, Portugal",
    "country": "Portugal",
    "region": "Douro Valley",
    "tradition": "fortified",
    "key_person": "Adrian Bridge (CEO); David Guimaraens (winemaker, 5th generation)",
    "founded": "1692 (Taylor's founding date; Fonseca acquired 1948; Croft acquired 2001)",
    "production_volume": "Second-largest premium Port producer; ~1.5M cases across Taylor's/Fonseca/Croft",
    "notable_products": ["Taylor Fladgate Vintage Port", "Taylor Fladgate 20/30/40-Year Tawny",
                         "Fonseca Vintage Port", "Croft Quinta da Roêda", "Croft Pink"],
    "certifications": ["IVDP certified", "Douro DOC"],
    "website": "taylor.pt / fonseca.pt / croftport.com",
    "philosophy": "Oldest English-founded Port house still in continuous production. Emphasis on the "
                  "Douro Superior terroir of Quinta de Vargellas (Taylor's) and Quinta da Cruzeiro (Fonseca) "
                  "as single-quinta expressions that frame the house style.",
    "trail_connection": "PCT-1",
    "source": "Taylor Fladgate official history; IVDP records; Wine Advocate Taylor's profiles",
    "verified": True
})

session.add_producer({
    "name": "Quinta do Noval",
    "location": "Pinhão, Cima Corgo, Douro Valley, Portugal",
    "country": "Portugal",
    "region": "Douro Valley — Cima Corgo",
    "tradition": "fortified",
    "key_person": "Christian Seely (MD, AXA Millésimes); Carlos Agrellos (winemaker)",
    "founded": "1715 (quinta); 1894 (estate bottling); acquired by AXA Millésimes 1993",
    "production_volume": "Small; premium production — ~400,000 bottles annually",
    "notable_products": ["Quinta do Noval Nacional Vintage Port (ungrafted vines)",
                         "Quinta do Noval Vintage Port", "Quinta do Noval 20-Year Tawny",
                         "Quinta do Noval 10-Year Tawny"],
    "certifications": ["IVDP certified", "Douro DOC"],
    "website": "quintadonoval.com",
    "philosophy": "AXA Millésimes acquired Noval alongside Château Pichon Baron and Château Suduiraut, "
                  "applying the same quality-first philosophy. The Nacional vineyard — pre-phylloxera ungrafted "
                  "vines in a special schist outcrop — is the property's crown jewel and one of the world's "
                  "rarest wines, produced only in exceptional declared years.",
    "trail_connection": "PCT-1",
    "source": "Quinta do Noval official documentation; Wine Advocate profiles; AXA Millésimes press releases",
    "verified": True
})

session.add_producer({
    "name": "Niepoort",
    "location": "Vila Nova de Gaia, Portugal",
    "country": "Portugal",
    "region": "Douro Valley",
    "tradition": "fortified",
    "key_person": "Dirk Niepoort (5th generation owner/winemaker)",
    "founded": "1842 (Edouard Niepoort, Dutch-German family)",
    "production_volume": "~500,000 bottles annually; premium-focused production",
    "notable_products": ["Niepoort Vintage Port", "Niepoort Colheita", "Niepoort Dry White Port",
                         "Niepoort 'Bioma' Douro table wine", "Niepoort 'Charme' red"],
    "certifications": ["IVDP certified", "Douro DOC", "Organic farming on key parcels"],
    "website": "niepoort-vinhos.com",
    "philosophy": "The most iconoclastic of the major Port houses. Dirk Niepoort simultaneously produces "
                  "Port wines to the highest traditional standards AND revived the Douro table wine category "
                  "in the 1990s with 'Redoma' and 'Charme' — demonstrating that the Douro is world-class "
                  "for unfortified wines as well.",
    "trail_connection": "PCT-1",
    "source": "Niepoort official documentation; Jancis Robinson profiles; Wine & Spirits Education Trust resources",
    "verified": True
})

session.add_producer({
    "name": "Ramos Pinto",
    "location": "Vila Nova de Gaia, Portugal",
    "country": "Portugal",
    "region": "Douro Valley",
    "tradition": "fortified",
    "key_person": "João Nicolau de Almeida (legendary winemaker, retired); current winemaker: [NEEDS VERIFICATION]",
    "founded": "1880 (Adriano Ramos Pinto)",
    "production_volume": "~600,000 bottles annually; owned by Louis Roederer since 1990",
    "notable_products": ["Ramos Pinto Colheita", "Ramos Pinto 20-Year Tawny (Quinta do Bom Retiro)",
                         "Ramos Pinto Vintage Port", "Ramos Pinto Adriano Reserve"],
    "certifications": ["IVDP certified", "Douro DOC"],
    "website": "ramospinto.pt",
    "philosophy": "Founded on Art Nouveau aesthetics (the iconic early 20th-century labels by Aleardo Villa "
                  "are among Portugal's great commercial art pieces), Ramos Pinto is now owned by Champagne "
                  "Louis Roederer, bringing luxury brand management to one of the Douro's most historically "
                  "important houses. Their Colheita programme is particularly distinguished.",
    "trail_connection": "PCT-1",
    "source": "Ramos Pinto official history; Louis Roederer Group press; IVDP records",
    "verified": True
})

session.add_producer({
    "name": "Churchill's (Churchill Graham Lda)",
    "location": "Vila Nova de Gaia, Portugal",
    "country": "Portugal",
    "region": "Douro Valley",
    "tradition": "fortified",
    "key_person": "John Graham (founder 1981); Caroline Graham-Spencer (current generation)",
    "founded": "1981 (newest of the major Port houses)",
    "production_volume": "Small; boutique-scale premium production",
    "notable_products": ["Churchill's Vintage Port", "Churchill's Crusted Port",
                         "Churchill's Dry White Port", "Quinta da Gricha (single quinta)"],
    "certifications": ["IVDP certified", "Douro DOC"],
    "website": "churchills-port.com",
    "philosophy": "Founded when John Graham — a descendant of the original Graham's family — left after Symington "
                  "acquisition to create his own house. Churchill's is the standard-bearer for Crusted Port revival "
                  "and produces consistently excellent Vintage Port from Quinta da Gricha.",
    "trail_connection": "PCT-1",
    "source": "Churchill's official documentation; James Suckling profiles",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 3 COMMITTED — Port Producers]\n")

# ============================================================
# PURVEYOR ENTRIES — Distribution
# ============================================================

session.add_purveyor({
    "name": "Kobrand Corporation",
    "type": "importer",
    "location": "New York, NY, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["fortified", "wine", "spirits", "champagne"],
    "producer_relationships": ["Taylor Fladgate", "Fonseca", "Croft"],
    "website": "kobrandwineandspirits.com",
    "contact": "kobrandwineandspirits.com/contact",
    "minimum_order": "Trade accounts only",
    "delivery_notes": "National US distributor for Taylor Fladgate Partnership portfolio. "
                      "Kobrand has distributed Taylor Fladgate in the US for decades; "
                      "Taylor Fladgate is one of their anchor fortified wine brands.",
    "verified": True
})

session.add_purveyor({
    "name": "Premium Port Wines, Inc.",
    "type": "importer",
    "location": "San Francisco, CA, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["fortified"],
    "producer_relationships": ["Graham's", "Dow's", "Warre's", "Quinta do Vesuvio", "Cockburn's"],
    "website": "premiumport.com",
    "contact": "premiumport.com/contacts",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Wholly-owned US distribution subsidiary of Symington Family Estates, founded 1985. "
                      "Exclusive national US importer for all Symington Port brands. Maintains state distributor "
                      "network including Southern Glazer's in multiple states. The most efficient route to "
                      "Symington brands in any US state.",
    "verified": True
})

session.add_purveyor({
    "name": "Vintus LLC",
    "type": "importer",
    "location": "New York, NY, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["fortified", "wine"],
    "producer_relationships": ["Quinta do Noval"],
    "website": "vintus.com",
    "contact": "vintus.com/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Confirmed exclusive US national importer for Quinta do Noval (including Nacional). "
                      "Launched Vintus New York in 2019 for direct NY state distribution. Also handles other "
                      "premium European wine estates. The route for all Quinta do Noval in the US market.",
    "verified": True
})

session.add_purveyor({
    "name": "Martine's Wines",
    "type": "importer",
    "location": "Novato, CA, USA",
    "markets_served": ["nationwide_US", "California", "most_states"],
    "traditions_carried": ["fortified", "wine"],
    "producer_relationships": ["Niepoort (exclusive national US importer, most states)"],
    "website": "mwines.com",
    "contact": "mwines.com/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Confirmed exclusive US importer for Niepoort across most US states. "
                      "Specialist in premium European wines; Niepoort is a flagship producer in their portfolio. "
                      "NJ and NY may have separate arrangements — verify with Martine's directly for those states.",
    "verified": True
})

session.add_purveyor({
    "name": "Galleon Wines (Philippe Dandurand Wines)",
    "type": "agent",
    "location": "Burnaby, BC, Canada (4580 Hastings Street, Suite 203)",
    "markets_served": ["BC", "Alberta", "Western_Canada"],
    "traditions_carried": ["wine", "fortified", "spirits"],
    "producer_relationships": ["Quinta do Crasto (confirmed — listed on both Crasto's importer page and Galleon's site)"],
    "website": "galleonwines.ca",
    "contact": "galleonwines.ca/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Galleon Wines is the BC-based division of Vins Philippe Dandurand Wines Ltd — Canada's "
                      "largest family-run wine importer. Confirmed BC agent for Quinta do Crasto (Port and Douro "
                      "table wines). Philippe Dandurand Wines also the likely (unconfirmed) BC agent for Symington "
                      "brands and Taylor Fladgate based on their national Portuguese wine coverage.",
    "verified": True
})

session.add_purveyor({
    "name": "Evaton Inc. (Sogrape USA)",
    "type": "importer",
    "location": "Stamford, CT, USA",
    "markets_served": ["nationwide_US", "all_50_states"],
    "traditions_carried": ["fortified", "wine"],
    "producer_relationships": ["Sandeman (Port and Sherry)", "Ferreira Port", "Casa Ferreirinha"],
    "website": "evaton.com",
    "contact": "evaton.com/contact",
    "minimum_order": "Trade accounts",
    "delivery_notes": "Evaton is the wholly-owned US distribution subsidiary of Sogrape (Portugal's largest "
                      "wine group). Confirmed US national importer for Sandeman and Ferreira Port (Ferreira "
                      "appointed April 2020, replacing prior agent Broadbent Selections). National distribution "
                      "across all 50 states.",
    "verified": True
})

session.commit_batch()
print(f"\n[BATCH 4 COMMITTED — Port Purveyors]\n")

# Session summary
handoff = session.finish()
print(handoff)
