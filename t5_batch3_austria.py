#!/usr/bin/env python3
"""Terminal 5 — Batch 3: Austria wine producers + products (Wachau, Kamptal, Kremstal, Burgenland)"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PAIR

conn, cur = get_conn()

# Region IDs from batch 1
WACHAU = 226
KAMPTAL = 227
KREMSTAL = 228
BURGENLAND = 229

print("=== AUSTRIA — PRODUCERS ===")

fx_pichler = P(cur, "F.X. Pichler", "winery", WACHAU, country="Austria",
    production_philosophy="traditional",
    philosophy_description="The most celebrated name in Austrian wine — Franz Xaver Pichler established the Wachau's global reputation through extreme quality thresholds and iconic wines. Lucas Pichler (son) maintains the rigorous standard. The Smaragd tier ('M' designation on the label) represents perfection — only declassified in years when quality falls below the Pichler threshold. The Loibner Berg Riesling and the Dürnsteiner Kellerberg Grüner Veltliner are the estate's twin peaks. Pichler wines are difficult to source without a restaurant account — allocation is heavily oversubscribed.",
    key_personnel=[{"name": "Lucas Pichler", "role": "winemaker (son of F.X.)"}, {"name": "F.X. Pichler", "role": "founder"}],
    production_details={"region": "Loiben — Dürnstein, central Wachau", "key_wines": ["Unendlich Grüner Veltliner Smaragd", "Loibner Berg Riesling Smaragd M"],
                        "classification": "Vinea Wachau Smaragd", "style": "Maximum concentration, minimum intervention, extended lees ageing"},
    quality_tier="reserve", reputation_narrative="THE reference producer for Wachau — commands Burgundy Grand Cru pricing for Smaragd M. Allocation-based; restaurant direct or through premium importers (Skurnik USA, Liberty Wines UK).",
    price_positioning="ultra_premium", authority_tier=1)

emmerich_knoll = P(cur, "Emmerich Knoll", "winery", WACHAU, country="Austria",
    production_philosophy="traditional",
    philosophy_description="The Knoll estate in Unterloiben, founded 1872, is among the Wachau's most traditional and least-known internationally — despite producing wines that regularly exceed Pichler in blind tastings. Knoll's approach is distinctly old-fashioned: foot-treading for sorting, extended maceration, old oak for some cuvées, minimal intervention. The Loibner Schütt and Loibner Ried Loibenberg single-vineyard Smaragden are the benchmarks. Emmerich Knoll (fourth generation) is quietly considered by insiders to equal or exceed F.X. Pichler in certain vintages.",
    key_personnel=[{"name": "Emmerich Knoll III", "role": "winemaker"}, {"name": "Emmerich Knoll II", "role": "previous generation"}],
    production_details={"region": "Unterloiben, central Wachau", "key_wines": ["Loibner Schütt GV Smaragd", "Loibner Ried Loibenberg Riesling Smaragd"],
                        "style": "Traditional — old oak for premium cuvées, minimal intervention, exceptional terroir transparency"},
    quality_tier="reserve", reputation_narrative="The insider's choice — regularly rivals Pichler at significantly lower prices. Allocation scarce but more accessible than F.X. Pichler. Available through Austrian wine specialists.",
    price_positioning="premium", authority_tier=1)

brundlmayer = P(cur, "Weingut Bründlmayer", "winery", KAMPTAL, country="Austria",
    production_philosophy="biodynamic",
    philosophy_description="Willi Bründlmayer is Kamptal's most internationally visible producer — 80 hectares across Zöbing, Langenlois, Kammern, and the iconic Zöbinger Heiligenstein. The Heiligenstein is a 350-million-year-old rhyolite volcanic outcrop — one of Austria's most distinctive geological features — producing Riesling of extraordinary mineral depth. Bründlmayer was an early advocate for dry Grüner Veltliner as a serious ageing wine; his Lamm GV (from Loess and primary rock soils above Langenlois) is the Kamptal GV benchmark. Biodynamic principles applied estate-wide since 2010.",
    key_personnel=[{"name": "Willi Bründlmayer", "role": "proprietor and winemaker"}, {"name": "Michael Bründlmayer", "role": "son, next generation"}],
    production_details={"vineyard_ha": 80, "key_sites": ["Zöbinger Heiligenstein (rhyolite)", "Lamm (loess-primary rock)", "Steinmassel", "Dechant"],
                        "key_wines": ["Heiligenstein Riesling", "Lamm Grüner Veltliner", "Spiegel GV Smaragd equivalent"],
                        "certification": "Biodynamic since 2010"},
    quality_tier="reserve", reputation_narrative="Kamptal's reference estate — Heiligenstein Riesling is one of Austria's three or four greatest wines. Widely available through Austrian/European importers in North America.",
    price_positioning="premium", authority_tier=1)

nigl = P(cur, "Weingut Nigl", "winery", KREMSTAL, country="Austria",
    production_philosophy="traditional",
    philosophy_description="Martin Nigl produces Kremstal's most compelling wines from volcanic Senftenberg parcels — a combination of primary rock (gneiss, granite) and loess that produces Riesling of unusual mineral intensity for the region. The Privat Riesling (from oldest Senftenberg vines) and the Riesling vom Stein are the estate's flagship expressions — regularly achieving scores that exceed their Kamptal and Wachau counterparts at lower prices. Nigl is Kremstal's strongest argument for the DAC's quality potential.",
    key_personnel=[{"name": "Martin Nigl", "role": "winemaker and proprietor"}],
    production_details={"region": "Senftenberg, Kremstal", "soil": "volcanic gneiss-granite plus loess",
                        "key_wines": ["Privat Riesling (oldest Senftenberg vines)", "Riesling vom Stein", "Grüner Veltliner Privat"]},
    quality_tier="reserve", reputation_narrative="Kremstal's best QPR producer. Privat Riesling rivals Wachau Smaragd at fraction of Pichler prices. Available through Austrian specialists.",
    price_positioning="mid_range", authority_tier=1)

umathum = P(cur, "Weingut Umathum", "winery", BURGENLAND, country="Austria",
    production_philosophy="biodynamic",
    philosophy_description="Josef Umathum is Burgenland's reference producer for single-vineyard Blaufränkisch — the estate in Frauenkirchen was biodynamic from 1997, long before it was fashionable in Austria. The Hallebühl and Unter den Terrassen single-vineyard Blaufränkisch are the benchmarks: deeply coloured, iron-spiced, graphite-mineral Blaufränkisch with the tannin structure to age 15+ years. Umathum was one of the first Austrian producers to prove that Burgenland reds could rival Burgundy for age-worthy precision.",
    key_personnel=[{"name": "Josef Umathum", "role": "founder and winemaker"}, {"name": "Thomas Umathum", "role": "next generation"}],
    production_details={"region": "Frauenkirchen, Neusiedlersee-Hügelland, Burgenland", "certification": "Biodynamic (Demeter) since 1997",
                        "key_wines": ["Hallebühl Blaufränkisch", "Unter den Terrassen Blaufränkisch", "Sankt Laurent"],
                        "key_grape": "Blaufränkisch — iron-rich schist soils, Neusiedlersee influence"},
    quality_tier="reserve", reputation_narrative="Austria's biodynamic Blaufränkisch pioneer. Wines age gracefully 15-25 years. Limited North American availability — Austrian specialist import.",
    price_positioning="premium", authority_tier=1)

moric = P(cur, "Moric", "winery", BURGENLAND, country="Austria",
    production_philosophy="organic",
    philosophy_description="Roland Velich (of Velich — Tiglat TBA fame) founded Moric in 2001 as a project exclusively focused on old-vine Blaufränkisch from Lutzmannsburg, Mittelburgenland. 'Moric' is Burgenland's old Germanic spelling. The philosophy: only pre-1960 planted vines, no new oak (used 500L Burgundy barriques), no filtration, no fining. The result is Blaufränkisch at its most mineral and precise — the antithesis of the New World-influenced Burgenland reds of the 1990s. Lutzmannsburg alte Reben (old vines) is Austria's most internationally acclaimed Blaufränkisch.",
    key_personnel=[{"name": "Roland Velich", "role": "founder and winemaker"}],
    production_details={"region": "Lutzmannsburg, Mittelburgenland", "vine_age_policy": "Only pre-1960 planted vines",
                        "key_wines": ["Lutzmannsburg Alte Reben Blaufränkisch", "Neckenmarkt Alte Reben Blaufränkisch"],
                        "oak_policy": "Used 500L Burgundy barriques only — no new oak"},
    quality_tier="reserve", reputation_narrative="Austria's most internationally acclaimed Blaufränkisch — regularly compared to Chambolle-Musigny for elegance and mineral precision. Sought-after allocation.",
    price_positioning="premium", authority_tier=1)

print("\n=== AUSTRIA — PRODUCTS ===")

fx_pichler_unendlich = PROD(cur,
    "F.X. Pichler Dürnsteiner Kellerberg Grüner Veltliner Smaragd",
    "wine_still", fx_pichler, WACHAU, origin_country="Austria",
    subcategory="Grüner Veltliner Smaragd",
    description="Pichler's signature Grüner Veltliner — from the steep Kellerberg slope above Dürnstein, where the granite and gneiss bedrock beneath a thin loess layer concentrates Grüner Veltliner into a wine of extraordinary mineral intensity and longevity. The Smaragd classification requires minimum 12.5% ABV and hand-harvesting at full phenolic maturity. The Kellerberg GV achieves 13.5–14% ABV in top vintages — for many decades considered 'too big' for a white wine by conventional critics, it is now recognised as one of Austria's greatest expressions of terroir. The white pepper, green herb, and mineral character of Grüner Veltliner is amplified to extraordinary concentration by the Kellerberg's steep gradient and granite-gneiss substrate.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Smaragd M (Kellerberg / Loibner Berg)", "criteria": "M-designation: only released when quality is absolute; 13.5-14% ABV; granite-gneiss Wachau precision; 15-25yr cellaring"},
        {"tier": 3, "tier_name": "Smaragd (single vineyard)", "criteria": "Minimum 12.5% ABV; Vinea Wachau Smaragd classification; hand-harvested fully mature clusters; 10yr+ cellaring"},
        {"tier": 2, "tier_name": "Federspiel (estate)", "criteria": "11.5-12.5% ABV; lighter Wachau style — fresher, earlier drinking; still single-vineyard precision"},
        {"tier": 1, "tier_name": "Steinfeder", "criteria": "Max 11.5% ABV; lightest Wachau tier — for immediate drinking; floral and fresh"}
    ],
    deductive_profile={"appearance": "Deep gold with green tints; full viscosity at Smaragd level",
                       "nose": "Grüner Veltliner signature: white pepper (rotundone compound), green herbs (tarragon, fennel), citrus zest, stone fruit; Kellerberg granite adds mineral-smoky depth",
                       "palate": "Full-bodied (13.5% ABV); dry; Wachau-characteristic power combined with laser acidity; white pepper finish of extraordinary persistence; 15yr cellaring minimum",
                       "conclusion": "Reserve quality; the Wachau's most powerful Grüner Veltliner; peak 10-25 years from vintage"},
    service_specs={"temperature_c": 13, "glass": "White Burgundy large format — needs aeration",
                   "decant": "Recommended for 5+ year examples — 45 min", "programme_position": "Rich fish, veal, pork, white truffle preparations"},
    flavour_markers=["white pepper", "green herbs", "citrus zest", "stone fruit", "granite mineral", "fennel"],
    flavour_weight="full", flavour_profile_type="dry_mineral",
    price_tier="ultra_premium", price_range_cad="$120-200",
    technical_specs={"grape": "Grüner Veltliner 100%", "alcohol_abv": 13.8, "residual_sugar_gl": 3,
                     "classification": "Vinea Wachau Smaragd", "vineyard": "Dürnsteiner Kellerberg",
                     "soil": "granite-gneiss with thin loess", "gradient_pct": 60})

emmerich_knoll_riesling = PROD(cur,
    "Emmerich Knoll Loibner Ried Loibenberg Riesling Smaragd",
    "wine_still", emmerich_knoll, WACHAU, origin_country="Austria",
    subcategory="Riesling Smaragd",
    description="The Loibenberg — 'Loiben hill' — is the benchmark Wachau Riesling site for Knoll: a south-facing gneiss-primary rock slope above the Danube at Unterloiben, producing Riesling of extraordinary mineral precision and longevity. Unlike Pichler's powerful concentration, Knoll's Loibenberg has a distinctive tension — the gneiss mineral backbone stretches the wine's acidity through a long, slow finish of crushed stone and citrus peel. In top vintages (2007, 2015, 2017, 2019) this rivals the Mosel's greatest Auslesen for mineral depth, but in a dry (Smaragd) format that makes it more food-versatile. Minimum 12.5% ABV; exceptional structure to age 20+ years.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Loibenberg Riesling Smaragd (top vintages)", "criteria": "Single vineyard, gneiss primary rock, Smaragd classification; exceptional vintages only achieve full mineral expression; 20yr cellaring"},
        {"tier": 3, "tier_name": "Riesling Smaragd (Schütt / Pfaffenberg)", "criteria": "Alternative single-vineyard Smaragd Rieslings — slightly more accessible than Loibenberg"},
        {"tier": 2, "tier_name": "Riesling Federspiel", "criteria": "11.5-12.5% ABV; lighter, fresher style; earlier drinking; good food wine"},
        {"tier": 1, "tier_name": "Riesling Steinfeder", "criteria": "Lightest tier; immediate freshness; aperitif register"}
    ],
    deductive_profile={"appearance": "Pale gold with green highlights; brilliant clarity",
                       "nose": "Crushed stone and citrus peel dominance unusual in Austria — more mineral than fruit-forward; lime, yellow peach, and gneiss rock over grapefruit acidity",
                       "palate": "Dry; full-bodied Smaragd (12.5-13% ABV); extended mineral finish; lime zest and wet stone persistence 25+ seconds; extraordinary tension",
                       "conclusion": "Reserve quality; the Wachau insider's benchmark; peak 8-20 years from vintage"},
    service_specs={"temperature_c": 12, "glass": "White Burgundy or large Riesling glass",
                   "decant": "Optional at 5+ years", "programme_position": "Rich fish, shellfish, Viennese cuisine"},
    flavour_markers=["crushed stone", "lime zest", "yellow peach", "gneiss mineral", "white grapefruit", "citrus peel"],
    flavour_weight="medium-full", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$85-140",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 13.0, "residual_sugar_gl": 4,
                     "classification": "Vinea Wachau Smaragd", "vineyard": "Ried Loibenberg",
                     "soil": "gneiss primary rock"})

brundlmayer_heiligenstein = PROD(cur,
    "Bründlmayer Zöbinger Heiligenstein Riesling",
    "wine_still", brundlmayer, KAMPTAL, origin_country="Austria",
    subcategory="Riesling Reserve",
    description="Austria's most geologically distinctive single-vineyard wine — the Heiligenstein is a 350-million-year-old volcanic rhyolite outcrop above Zöbing, separated from the surrounding loess landscape by geological faulting. The rhyolite imparts a unique flavour signature: intense stone fruit (peach, yellow plum), floral lift (rose water, elderflower), and a smoky-volcanic mineral finish that no other Austrian vineyard replicates. Bründlmayer's interpretation — biodynamic since 2010, native yeast fermentation, minimal sulphur — is the benchmark expression of this unique terroir. The wine achieves extraordinary longevity: 20+ years from exceptional vintages.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Heiligenstein Reserve (Alte Reben)", "criteria": "Oldest vines on the rhyolite; even more concentrated volcanic mineral character; rarely produced"},
        {"tier": 3, "tier_name": "Heiligenstein Riesling (standard)", "criteria": "Full rhyolite vineyard expression; 13-13.5% ABV; biodynamic; 15-20yr cellaring potential"},
        {"tier": 2, "tier_name": "Kamptal DAC Reserve Riesling", "criteria": "Multi-vineyard blend including Heiligenstein parcels; more accessible; 8-12yr cellaring"},
        {"tier": 1, "tier_name": "Kamptal DAC Riesling", "criteria": "Village-level; fresher, immediate drinking style; Kamptal DAC appellation"}
    ],
    deductive_profile={"appearance": "Medium-full gold; brilliant; slightly more colour than Wachau Riesling",
                       "nose": "Distinctive volcanic character — rose water, elderflower, yellow peach, and stone fruit over a smoky-volcanic mineral underlay; unique to rhyolite",
                       "palate": "Full-bodied (13-13.5% ABV); dry; extraordinary volcanic-mineral length; floral persistence unusual in dry Riesling; 20yr potential",
                       "conclusion": "Reserve quality; Austria's most geologically unique terroir expression; peak 8-20 years"},
    service_specs={"temperature_c": 12, "glass": "White Burgundy glass",
                   "decant": "Recommended at 5+ years", "programme_position": "Veal, white asparagus, Viennese Wiener Schnitzel, white truffle"},
    flavour_markers=["rose water", "elderflower", "yellow peach", "volcanic stone", "stone fruit", "smoky mineral"],
    flavour_weight="medium-full", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$70-120",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 13.2, "residual_sugar_gl": 5,
                     "vineyard": "Zöbinger Heiligenstein", "soil": "350M-year-old rhyolite volcanic rock",
                     "certification": "Biodynamic (Demeter)"})

brundlmayer_lamm_gv = PROD(cur,
    "Bründlmayer Langenlois Lamm Grüner Veltliner Reserve",
    "wine_still", brundlmayer, KAMPTAL, origin_country="Austria",
    subcategory="Grüner Veltliner Reserve",
    description="The Kamptal's reference Grüner Veltliner — Lamm ('lamb') is a south-facing slope above Langenlois on loess-over-primary rock soils, producing GV of white pepper intensity and mineral precision. Bründlmayer's Lamm is the wine that moved Grüner Veltliner from wine-list curiosity to sommelier staple: at 13+ % ABV, fully dry, with the distinctive rotundone-driven white pepper signature amplified by loess minerality, it demonstrates what GV achieves at the apex of quality. An essential reference wine for Austrian wine education.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Lamm Reserve (top vintages)", "criteria": "Full Lamm vineyard expression; loess-primary rock; 13-13.5% ABV; white pepper concentration; 15yr cellaring"},
        {"tier": 3, "tier_name": "Spiegel GV Reserve", "criteria": "Alternative single-vineyard — loess-dominant; more generous texture than Lamm; 10yr cellaring"},
        {"tier": 2, "tier_name": "Kamptal DAC Reserve GV", "criteria": "Multi-vineyard reserve; accessible white pepper and fruit; 5-8yr cellaring"},
        {"tier": 1, "tier_name": "Kamptal DAC Grüner Veltliner", "criteria": "Village-level GV; immediate drinking; aperitif and fish course standard"}
    ],
    deductive_profile={"appearance": "Medium gold; brilliant; slight green tint in youth",
                       "nose": "White pepper (rotundone) — the defining Grüner Veltliner marker; citrus zest, stone fruit, green herb (tarragon, fennel); loess adds a flinty, smoky mineral layer",
                       "palate": "Full-bodied (13-13.5% ABV); dry; electric acidity from Kamptal; persistent white pepper and mineral finish; 15yr cellaring potential",
                       "conclusion": "Reserve quality; Kamptal GV benchmark; peak 6-15 years from vintage"},
    service_specs={"temperature_c": 12, "glass": "White Burgundy glass",
                   "programme_position": "Classic Austrian pairing: Wiener Schnitzel, pike-perch (zander) Müllerin, Viennese asparagus"},
    flavour_markers=["white pepper", "citrus zest", "stone fruit", "tarragon", "fennel", "loess mineral"],
    flavour_weight="full", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$60-90",
    technical_specs={"grape": "Grüner Veltliner 100%", "alcohol_abv": 13.2, "residual_sugar_gl": 4,
                     "vineyard": "Langenlois Lamm", "soil": "loess over primary rock",
                     "certification": "Biodynamic (Demeter)"})

moric_lutzmannsburg = PROD(cur,
    "Moric Lutzmannsburg Alte Reben Blaufränkisch",
    "wine_still", moric, BURGENLAND, origin_country="Austria",
    subcategory="Blaufränkisch Alte Reben",
    description="Austria's most internationally acclaimed red wine — Blaufränkisch from pre-1960 planted vines in Lutzmannsburg, Mittelburgenland, on iron-rich clay-limestone soils. Roland Velich's approach is deliberately Burgundian: only old-vine parcels, used 500L barriques (no new oak), no fining, no filtration. The result is Blaufränkisch at its most mineral and precise — the iron character of the Mittelburgenland soils expresses as graphite, dark cherry, and a violet-spiced finish that lengthens for 30+ seconds. In top vintages (2013, 2015, 2017) this challenges Premier Cru Burgundy in blind tastings.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Alte Reben (Old Vines)", "criteria": "Pre-1960 planted vines only; Lutzmannsburg iron-clay-limestone; old Burgundy barriques; no fining/filtration; 15-25yr cellaring"},
        {"tier": 3, "tier_name": "Blaufränkisch Neckenmarkt", "criteria": "Second vineyard — adjacent Neckenmarkt; schist soils; similar precision, marginally less concentration"},
        {"tier": 2, "tier_name": "Classic Blaufränkisch", "criteria": "Multi-vineyard; early accessibility; iron and dark cherry character without old-vine concentration"},
        {"tier": 1, "tier_name": "Burgenland Blaufränkisch (entry)", "criteria": "Entry level; iron-mineral character of Burgenland; drinking window 2-5 years"}
    ],
    deductive_profile={"appearance": "Deep ruby-purple; brilliant; high colour density",
                       "nose": "Graphite, dark cherry, violet, and iron mineral — the Mittelburgenland signature; black pepper, dark spice; developing cigar box and truffle with age",
                       "palate": "Full-bodied; dry; iron-mineral backbone with silky tannins from old vines; 13-13.5% ABV; 30+ second mineral finish with graphite persistence",
                       "conclusion": "Reserve quality; Austria's Burgundy equivalent; peak 8-25 years from vintage"},
    service_specs={"temperature_c": 16, "glass": "Red Burgundy large bowl",
                   "decant": "Required — 2-3 hours for young vintages", "programme_position": "Main course: game, beef, venison, aged hard cheese"},
    flavour_markers=["graphite", "dark cherry", "violet", "iron mineral", "black pepper", "cigar box"],
    flavour_weight="full", flavour_profile_type="red_mineral",
    price_tier="premium", price_range_cad="$75-120",
    technical_specs={"grape": "Blaufränkisch 100%", "vine_age": "pre-1960 planted", "alcohol_abv": 13.5,
                     "residual_sugar_gl": 2, "oak": "used 500L Burgundy barriques (no new oak)",
                     "fining_filtration": "None", "soil": "iron-rich clay-limestone"})

umathum_hb = PROD(cur,
    "Umathum Hallebühl Blaufränkisch",
    "wine_still", umathum, BURGENLAND, origin_country="Austria",
    subcategory="Blaufränkisch Hallebühl",
    description="Umathum's flagship single-vineyard Blaufränkisch — the Hallebühl ('slope of the cock') in Frauenkirchen, Neusiedlersee-Hügelland, on iron-rich schist soils with Pannonian climate influence (hot summers, cold winters, very low rainfall). Biodynamic since 1997, the Hallebühl demonstrates what commitment to terroir and organic viticulture can achieve in Burgenland: deep colour, spiced dark fruit, and a mineral-graphite backbone that ages gracefully over 15+ years. Umathum was Austria's biodynamic pioneer — certified by Demeter before any other leading Burgenland estate.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Hallebühl Blaufränkisch", "criteria": "Single-vineyard Frauenkirchen; iron schist; biodynamic; 13.5% ABV; Pannonian concentration; 15-20yr cellaring"},
        {"tier": 3, "tier_name": "Unter den Terrassen Blaufränkisch", "criteria": "Second single-vineyard; similar approach; slightly more accessible tannin structure"},
        {"tier": 2, "tier_name": "Blaufränkisch Alte Reben", "criteria": "Multi-vineyard old vines; excellent QPR; 8-12yr cellaring"},
        {"tier": 1, "tier_name": "Burgenland Blaufränkisch Classique", "criteria": "Entry; Neusiedlersee fruit character; fresh dark cherry; drink 2-5 years"}
    ],
    deductive_profile={"appearance": "Very deep ruby-purple; near-opaque; significant colour from hot Pannonian summers",
                       "nose": "Dark cherry, blackberry, iron-graphite, and dark spice; biodynamic character adds earthy complexity and vitality; violet florals in youth",
                       "palate": "Full-bodied; concentrated (13.5% ABV); iron-mineral backbone; firm tannins needing 5+ years; long spiced mineral finish",
                       "conclusion": "Reserve quality; Burgenland's biodynamic pioneer benchmark; peak 8-20 years"},
    service_specs={"temperature_c": 16, "glass": "Red Burgundy glass",
                   "decant": "Required — 2+ hours for young vintages", "programme_position": "Game, beef, venison; Austrian Tafelspitz alternative"},
    flavour_markers=["dark cherry", "blackberry", "iron mineral", "graphite", "dark spice", "violet"],
    flavour_weight="full", flavour_profile_type="red_mineral",
    price_tier="premium", price_range_cad="$65-100",
    technical_specs={"grape": "Blaufränkisch 100%", "alcohol_abv": 13.5, "residual_sugar_gl": 2,
                     "certification": "Demeter biodynamic since 1997", "vineyard": "Hallebühl, Frauenkirchen",
                     "soil": "iron-rich schist"})

print("\n=== AUSTRIA — REFERENCES ===")

ref_gv = REF(cur,
    "Grüner Veltliner — Austria's Native White and the VDP Equivalent Classification",
    "wine_knowledge",
    description="Grüner Veltliner (GV) is Austria's signature white grape — covering 28% of planted area, found in Wachau, Kamptal, Kremstal, Traisental, and Wien (Vienna). The defining aromatic compound is rotundone — the same pepper compound found in Syrah/Shiraz — which expresses as white pepper in dry GV and combines with green herb (tarragon, fennel, celery), citrus zest, and stone fruit character. Austria's unique classification: Vinea Wachau (Wachau-specific) with Steinfeder → Federspiel → Smaragd tiers; and DAC (Districtus Austriae Controllatus) for other regions. The GG (Grosses Gewächs) equivalent in Austria is effectively the Smaragd designation for Wachau and the Reserve tier for DAC regions.",
    key_principles="""GRÜNER VELTLINER DEDUCTIVE FRAMEWORK:

PRIMARY AROMATIC MARKER — ROTUNDONE:
White pepper character is the defining GV marker — caused by rotundone (a sesquiterpene ketone also found in black pepper and Syrah). Higher concentrations in cooler vintages and clay-heavy soils. Absence of pepper = less typical GV expression.

REGIONAL STYLE DIFFERENCES:
Wachau Smaragd: Maximum concentration; granite-gneiss backbone; 12.5-14% ABV; food-requiring power; 15-25yr cellaring
Kamptal Reserve: Loess mineral backbone; generous fruit with white pepper; 13-13.5% ABV; versatile pairing; 10-15yr
Kremstal: Between Wachau and Kamptal — intermediate mineral and weight
Wien (Vienna): Gemischter Satz (field blend) tradition; fresh, immediate, urban vineyard character

QUALITY HIERARCHY:
Smaragd (Wachau) / Reserve DAC: Full ripeness, maximum complexity, cellaring potential
Federspiel (Wachau) / DAC Klassik: Medium weight; excellent food wine; accessible
Steinfeder (Wachau): Lightest; max 11.5% ABV; aperitif; immediate drinking

FOOD PAIRING FRAMEWORK (GV versatility):
White pepper → white meat, veal, schnitzel, chicken
Citrus-mineral → fish, shellfish, sashimi
Full Smaragd → white truffle, rich fish sauces, asparagus
Green herb → herb-crusted preparations, green asparagus

DEDUCTIVE CLUES FOR BLIND TASTING:
White pepper: rotundone — highly diagnostic; consider Austria, Northern Rhône (Syrah has same compound)
Citrus-mineral acidity: Austrian or cool-climate characteristic
Low colour with high weight: Austrian Smaragd
Absence of oak character: Most GV aged in stainless steel or old oak — no vanilla""",
    common_mistakes="Confusing GV's white pepper with Gewürztraminer spice — entirely different mechanisms and aromatic profiles. Assuming GV cannot age — Smaragd GV from Wachau ages 20+ years. Over-chilling GV (serve at 12-13°C, not 8°C).",
    pro_tips="Always ask the vintage — GV is more vintage-sensitive than most Austrian reds. 2015, 2017, 2019 are exceptional for Smaragd; 2018 for fresh Federspiel. The Wachau, Kamptal, Kremstal DAC regulations mandate GV as the primary white variety — this regional specificity is Austria's version of Burgundy's Chardonnay monopoly.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="Austrian Wine Marketing Board; Vinea Wachau Nobilis Districtus; Kamptal DAC regulations; Willi Bründlmayer — In the spirit of Grüner Veltliner",
    authority_tier=1)

ref_blaufrankisch = REF(cur,
    "Blaufränkisch — Burgenland's Age-Worthy Red and Its Pannonian Terroir Logic",
    "wine_knowledge",
    description="Blaufränkisch (Lemberger in Germany, Kékfrankos in Hungary) is Burgenland's defining red grape — producing wines that range from fresh, iron-mineral aperitif reds to profound, graphite-structured age-worthy wines rivalling Burgundy for mineral complexity. The grape's defining characteristics: high natural acidity, iron-mineral expression from schist and clay-limestone soils, dark cherry and violet fruit, and a white pepper character that parallels (but does not equal) Grüner Veltliner's rotundone. The Mittelburgenland (Moric, Weninger) and Neusiedlersee-Hügelland (Umathum, Triebaumer) are the quality heartlands.",
    key_principles="""BLAUFRÄNKISCH REGIONAL EXPRESSION:

MITTELBURGENLAND (Moric, Weninger):
Soil: Iron-rich clay-limestone; Pannonian continental climate
Style: Most structured; graphite-iron mineral backbone; dark cherry; 15-25yr cellaring
Reference: Moric Lutzmannsburg Alte Reben — Austria's most praised red

NEUSIEDLERSEE-HÜGELLAND (Umathum, Triebaumer):
Soil: Iron-rich schist; Neusiedlersee moisture influence
Style: Deep colour; dark fruit concentration; more immediately accessible than Mittelburgenland
Reference: Umathum Hallebühl — biodynamic pioneer

RUST / RUSTER AUSBRUCH (sweet wine):
Neusiedlersee lake fog generates consistent autumn botrytis
Ausbruch style: 250-500 g/L RS; 100+ year cellaring potential
Rare varieties: Weissburgunder, Welschriesling, Furmint

DEDUCTIVE FRAMEWORK:
Iron-mineral: Highly characteristic of Burgenland — graphite, dark cherry, iron
Tannin: Finer than expected for deep colour — similar to Sangiovese structure
Acidity: High — enables longevity
Comparison: Blaufränkisch — dark cherry + iron/graphite = Barolo's tar + rose, but mineral-driven rather than volatile""",
    common_mistakes="Underestimating Blaufränkisch's ageing potential — quality examples need 5+ years and reward 20. Confusing with Zweigelt (more immediate, lower acid, red cherry character — different variety). Over-serving temperature (max 16°C).",
    pro_tips="Biodynamic certification (Umathum Demeter 1997, Moric organic) correlates strongly with quality in Burgenland — use as selection shortcut. Mittelburgenland Blaufränkisch improves dramatically with 2+ hours decanting.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="Austrian Wine Marketing Board; Roland Velich (Moric) — personal notes; Jancis Robinson — Wine Grapes (Blaufränkisch entry)",
    authority_tier=1)

print("\n✅ Terminal 5 Batch 3 — Austria complete.")
print(f"""
PRODUCER IDs:
  fx_pichler = {fx_pichler}
  emmerich_knoll = {emmerich_knoll}
  brundlmayer = {brundlmayer}
  nigl = {nigl}
  umathum = {umathum}
  moric = {moric}

PRODUCT IDs:
  fx_pichler_unendlich = {fx_pichler_unendlich}
  emmerich_knoll_riesling = {emmerich_knoll_riesling}
  brundlmayer_heiligenstein = {brundlmayer_heiligenstein}
  brundlmayer_lamm_gv = {brundlmayer_lamm_gv}
  moric_lutzmannsburg = {moric_lutzmannsburg}
  umathum_hb = {umathum_hb}

REF IDs:
  ref_gv = {ref_gv}
  ref_blaufrankisch = {ref_blaufrankisch}
""")
