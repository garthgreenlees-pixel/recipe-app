#!/usr/bin/env python3
"""Terminal 5 — Batch 4: Portugal table wine producers + products (Douro, Vinho Verde, Alentejo, Bairrada, Dão)"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PAIR

conn, cur = get_conn()

# Region IDs from batch 1
DOURO_TABLE = 230
VINHO_VERDE = 231
ALENTEJO = 232
BAIRRADA = 233
DAO = 234

print("=== PORTUGAL TABLE WINE — PRODUCERS ===")

vale_meao = P(cur, "Quinta do Vale Meão", "winery", DOURO_TABLE, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The spiritual successor to Barca Velha — Quinta do Vale Meão in Douro Superior was the original estate where Fernando Nicolau de Almeida made Portugal's greatest wine. When Ferreira sold the quinta in 1999 to the Olazabal family, Francisco Olazabal (Fernando's grandson) began making Vale Meão from the same Touriga Nacional-dominant schist terraces at 400-550m altitude. The Douro Superior's extreme continental climate (hottest, driest sub-zone) concentrates fruit to extraordinary intensity. The wine: dark, intense, mineral, structured Douro capable of 20-year evolution.",
    key_personnel=[{"name": "Francisco Olazabal", "role": "winemaker (Fernando Nicolau de Almeida's grandson)"}, {"name": "Francisco Javier Olazabal", "role": "CEO"}],
    production_details={"region": "Douro Superior — altitude 400-550m", "flagship": "Vale Meão (Touriga Nacional dominant blend)",
                        "history": "Original estate where Barca Velha was produced 1952-1999", "key_grape": "Touriga Nacional, Touriga Franca, Tinta Roriz"},
    quality_tier="reserve", reputation_narrative="The Douro's most historically important estate — connection to Barca Velha makes it Portugal's most storied quinta. Vale Meão the wine regularly ranks among Portugal's top 5 reds. Available through Portuguese specialists.",
    price_positioning="premium", authority_tier=1)

niepoort = P(cur, "Niepoort", "winery", DOURO_TABLE, country="Portugal",
    production_philosophy="biodynamic",
    philosophy_description="Dirk Niepoort is the Douro's most influential winemaker — simultaneously a Port shipper (fifth generation Dutch family since 1842) and the pioneer of fine Douro table wines. Charme (Tinta Amarela/Trincadeira dominant) and Redoma Tinto (traditional field blend) changed how the world perceived Portuguese table wine in the 1990s. Niepoort's biodynamic viticulture and commitment to old-vine field blends mirrors his philosophical opposition to international varieties and new oak. The estate works with terraced, pre-phylloxera field blends of 20+ indigenous varieties.",
    key_personnel=[{"name": "Dirk Niepoort", "role": "proprietor and winemaker"}],
    production_details={"tradition": "Port shipper (1842) + table wine pioneer (1991 first Redoma)",
                        "key_wines": ["Charme (Tinta Amarela dominant)", "Redoma Tinto (field blend)", "Redoma Branco"],
                        "philosophy": "Indigenous varieties only; old vines; field blends; no new oak; biodynamic"},
    quality_tier="reserve", reputation_narrative="The Douro's most important wine thinker — Dirk Niepoort's influence on Portuguese wine has been transformative. Redoma and Charme are reference wines for understanding Douro terroir. Available through Portuguese/European specialists.",
    price_positioning="premium", authority_tier=1)

crasto = P(cur, "Quinta do Crasto", "winery", DOURO_TABLE, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The Roquette and Loendorf families run one of the Cima Corgo's most ambitious estates — iconic terraced vineyards above Pinhão (the Douro's most photographed stretch) planted with old schist terraces and pre-phylloxera field blends. The Reserva Old Vines and Maria Teresa (oldest vines, single vineyard) are the estate benchmarks. Crasto is also one of the Douro's most commercially accessible quality estates — the regular Reserva offering extraordinary QPR for its quality level.",
    key_personnel=[{"name": "Tomás Roquette", "role": "managing partner"}, {"name": "Miguel Roquette", "role": "viticulture director"}],
    production_details={"region": "Cima Corgo — above Pinhão; the Douro's premium sub-zone",
                        "key_wines": ["Reserva Old Vines", "Maria Teresa (oldest pre-phylloxera vines)", "Vinha Maria Teresa"],
                        "terraces": "Traditional schist terraces above the Douro river"},
    quality_tier="reserve", reputation_narrative="Crasto Reserva Old Vines is the Douro's best-value serious red. Maria Teresa (pre-phylloxera vines) is a collector wine. Wide distribution makes Crasto the accessible gateway to quality Douro.",
    price_positioning="mid_range", authority_tier=1)

soalheiro = P(cur, "Soalheiro", "winery", VINHO_VERDE, country="Portugal",
    production_philosophy="organic",
    philosophy_description="The Cerdeira family pioneered single-variety Alvarinho in the Moncão e Melgaço sub-zone — the northernmost and coolest part of Vinho Verde, bordering Galicia where Albariño grows across the border. João António Cerdeira planted the first Alvarinho vines in Alvarinho at Soalheiro in 1974; before that the grape was used in blends. The Soalheiro Alvarinho is Portugal's benchmark expression — restrained stone fruit, lemon blossom, and saline mineral character unique to the granite-over-schist terroir at 200-250m altitude.",
    key_personnel=[{"name": "João Cerdeira", "role": "CEO"}, {"name": "António Luís Cerdeira", "role": "founder (1974)"}],
    production_details={"region": "Monção e Melgaço — northernmost Vinho Verde; altitude 200-250m",
                        "flagship": "Soalheiro Alvarinho (single variety)", "soil": "granite over schist",
                        "key_note": "First producer to bottle single-variety Alvarinho in Portugal (1974)"},
    quality_tier="reserve", reputation_narrative="The pioneer and benchmark for Portuguese Alvarinho. Soalheiro Alvarinho is the reference for understanding why Monção e Melgaço produces Portugal's finest Vinho Verde. Available through Portuguese wine specialists.",
    price_positioning="mid_range", authority_tier=1)

esporao = P(cur, "Herdade do Esporão", "winery", ALENTEJO, country="Portugal",
    production_philosophy="organic",
    philosophy_description="Esporão is the Alentejo's most internationally recognised estate — 750 hectares of cork oak, olive groves, and vineyards in Reguengos de Monsaraz, near the Spanish border. João Roquette (co-owner) commissioned the iconic 1993 cellar from architect Álvaro Siza Vieira. The Reserva (Monte Velho) and Private Selection ranges establish Esporão as Portugal's most commercially significant quality estate. Organic certification since 2010; extensive water-conservation programme in Portugal's driest wine region.",
    key_personnel=[{"name": "David Baverstock", "role": "chief winemaker (Australian-born; 30yr tenure)"}, {"name": "João Roquette", "role": "president"}],
    production_details={"vineyard_ha": 750, "region": "Reguengos de Monsaraz, Alentejo",
                        "key_wines": ["Esporão Reserva Tinto", "Monte Velho (entry range)", "Private Selection"],
                        "cellar": "Álvaro Siza Vieira design, 1993", "certification": "Organic since 2010"},
    quality_tier="reserve", reputation_narrative="The Alentejo's flagship estate — Esporão Reserva is Portugal's most widely available quality red under €15-20. Available through most wine importers globally including BC.",
    price_positioning="mid_range", authority_tier=1)

luis_pato = P(cur, "Luis Pato", "winery", BAIRRADA, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="Luis Pato is the Bairrada's most important figure — both its greatest winemaker and its most tireless advocate in the face of regulatory obstruction. In 1991 he was excluded from the Bairrada DOC after choosing not to add Touriga Nacional (a non-local variety required by DOC rules). He continued producing under Vinho Regional designation for a decade — a principled stand that ultimately forced the DOC to revise its rules. Pato's single-vineyard Baga wines (Quinta do Ribeirinho Pé Franco — own-rooted, pre-phylloxera; Vinha Pan; Vinha Formal) demonstrate Bairrada's capacity to produce age-worthy reds of 30-50 year cellaring potential.",
    key_personnel=[{"name": "Luis Pato", "role": "founder and winemaker"}, {"name": "Filipa Pato", "role": "daughter; separate winery, parallel reputation"}],
    production_details={"key_grape": "Baga — extreme tannin and acidity; clay-limestone Bairrada soils",
                        "key_wines": ["Pé Franco (own-rooted pre-phylloxera vines)", "Vinha Pan", "Vinha Formal"],
                        "style": "Traditional Baga — no commercial concessions; 20-50yr cellaring potential"},
    quality_tier="reserve", reputation_narrative="Bairrada's most important producer — Pé Franco (own-rooted) is one of Portugal's great age-worthy reds. Essential reference for any serious Portuguese wine programme. Specialist import.",
    price_positioning="premium", authority_tier=1)

print("\n=== PORTUGAL TABLE WINE — PRODUCTS ===")

vale_meao_wine = PROD(cur,
    "Quinta do Vale Meão",
    "wine_still", vale_meao, DOURO_TABLE, origin_country="Portugal",
    subcategory="Douro DOC Tinto",
    description="Portugal's most historically loaded wine — from the original Barca Velha quinta, now making its own benchmark Douro DOC tinto under the Olazabal family. Touriga Nacional-dominant (40-60%) with Touriga Franca, Tinta Roriz, and old field-blend varieties from terraced schist at 400-550m altitude in Douro Superior. The wine: concentrated dark fruit (blackberry, black cherry), graphite mineral, violet florals, and a structured tannin backbone requiring 8-10 years minimum. At peak (15-25 years) it reveals tobacco, leather, dried herbs, and cedar complexity that justifies its position as one of Portugal's finest.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Vale Meão (flagship)", "criteria": "Touriga Nacional dominant; Douro Superior schist terraces 400-550m; hand-harvested foot-trodden; 15-25yr cellaring"},
        {"tier": 3, "tier_name": "Meandro do Vale Meão", "criteria": "Second wine; earlier accessibility; same vineyard sources; 8-15yr cellaring"},
        {"tier": 2, "tier_name": "Vale Meão Branco", "criteria": "White Douro DOC — Rabigato dominant; alternative to red programme"},
        {"tier": 1, "tier_name": "Vinho Novo", "criteria": "Entry level; fresh fruit-forward; early drinking; no oak"}
    ],
    deductive_profile={"appearance": "Deep ruby-purple; near-opaque; Douro Superior concentration",
                       "nose": "Blackberry, black cherry, graphite, violet florals; cedar and tobacco with age; schist mineral backbone throughout",
                       "palate": "Full-bodied; structured tannins from Touriga Nacional; high natural acidity; 14-14.5% ABV; 15-25yr cellaring potential from top vintages",
                       "conclusion": "Reserve quality; Portugal's most historically significant estate; peak 12-25 years from vintage"},
    service_specs={"temperature_c": 17, "glass": "Red Bordeaux glass",
                   "decant": "Required — 3+ hours for young vintages", "programme_position": "Main course: lamb, beef, game, aged cheese"},
    flavour_markers=["blackberry", "black cherry", "graphite", "violet", "cedar", "schist mineral"],
    flavour_weight="full", flavour_profile_type="red_mineral",
    price_tier="premium", price_range_cad="$65-100",
    technical_specs={"grapes": "Touriga Nacional 40-60%, Touriga Franca, Tinta Roriz, field blend",
                     "alcohol_abv": 14.2, "region": "Douro Superior, altitude 400-550m",
                     "soil": "schist terraces", "ageing": "18-20 months French oak"})

niepoort_charme = PROD(cur,
    "Niepoort Charme Tinto",
    "wine_still", niepoort, DOURO_TABLE, origin_country="Portugal",
    subcategory="Douro DOC Tinto",
    description="Niepoort's most elegant red — Charme is Tinta Amarela (Trincadeira) dominant, from old terraced vines in the Cima Corgo's schist amphitheatres. Where most Douro reds pursue concentration and power, Charme is deliberately refined — lower alcohol (13-13.5% ABV), lighter colour than Touriga Nacional-dominant wines, but extraordinary perfume and mineral complexity. Dirk Niepoort specifically chose Tinta Amarela for its aromatic character: dried herbs, wild strawberry, iron mineral, and a silkiness that other Douro grapes rarely achieve. No new oak — aged in old 500L toneis (traditional Douro barrels). A wine that challenges the idea that Douro = power.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Charme (Tinta Amarela dominant)", "criteria": "Old terraced vines; Cima Corgo schist; minimal intervention; no new oak; 15-20yr cellaring"},
        {"tier": 3, "tier_name": "Redoma Tinto (field blend)", "criteria": "Field blend of 20+ indigenous varieties; more complex assembly; similar philosophy"},
        {"tier": 2, "tier_name": "Diálogo Tinto", "criteria": "Entry Niepoort red; indigenous varieties; accessible and food-friendly"},
        {"tier": 1, "tier_name": "Twisted Tinto", "criteria": "Commercial range; stainless steel; immediate drinking; accessible pricing"}
    ],
    deductive_profile={"appearance": "Medium ruby with garnet rim; relatively light for Douro — Tinta Amarela characteristic",
                       "nose": "Dried wild herbs, strawberry, iron mineral, and violet — unlike most Douro reds; perfumed rather than powerful; a quiet wine that rewards attention",
                       "palate": "Medium to medium-full body; silky tannins; 13-13.5% ABV; iron-mineral finish of extraordinary length; no new oak influence",
                       "conclusion": "Reserve quality; the Douro's most elegant red; contrasts with the region's typical power style; peak 8-20 years"},
    service_specs={"temperature_c": 16, "glass": "Red Burgundy glass — benefits from the same delicacy focus",
                   "decant": "1-2 hours recommended", "programme_position": "Main course: lamb, duck, mushroom-based preparations; cheese"},
    flavour_markers=["dried wild herbs", "strawberry", "iron mineral", "violet", "dark cherry", "silky tannin"],
    flavour_weight="medium-full", flavour_profile_type="red_mineral",
    price_tier="premium", price_range_cad="$70-110",
    technical_specs={"grape": "Tinta Amarela (Trincadeira) dominant, plus field blend indigenes",
                     "alcohol_abv": 13.2, "oak": "old toneis 500L — no new oak",
                     "vineyard": "Cima Corgo schist terraces"})

soalheiro_alvarinho = PROD(cur,
    "Soalheiro Alvarinho Monção e Melgaço",
    "wine_still", soalheiro, VINHO_VERDE, origin_country="Portugal",
    subcategory="Alvarinho single variety",
    description="The benchmark for Portuguese Alvarinho — from the Monção e Melgaço sub-zone at 200-250m altitude on granite-over-schist soils, where Atlantic rainfall (1,600mm annually) and cool temperatures preserve freshness while extended sun exposure (the south-facing solar hill of 'Soalheiro' — 'sunny place') achieves full phenolic maturity. João Cerdeira's father planted the first Alvarinho here in 1974; the wine has set the stylistic template for single-variety Alvarinho ever since. The profile is distinctive: white peach and lemon blossom aromatics, saline minerality from schist, and a refreshing acidity that places it between Galician Albariño and premier Burgundy Chablis on the mineral white wine spectrum.",
    quality_tier="estate",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Primeiras Vinhas (Oldest Vines)", "criteria": "Pre-1974 planted Alvarinho; maximum concentration; rare release"},
        {"tier": 3, "tier_name": "Soalheiro Alvarinho (standard)", "criteria": "Single-variety; Monção e Melgaço granite-schist; 12.5-13% ABV; 3-8yr ageing"},
        {"tier": 2, "tier_name": "Soalheiro Evolução", "criteria": "Aged Alvarinho (2 yrs); nutty complexity added; more food-versatile"},
        {"tier": 1, "tier_name": "Soalheiro Vinho Verde (blend)", "criteria": "Multi-variety; standard Vinho Verde freshness; early drinking"}
    ],
    deductive_profile={"appearance": "Pale gold with green highlights; brilliant",
                       "nose": "White peach, lemon blossom, and saline-schist mineral; citrus blossom; less floral than Galician Albariño; more mineral-focused",
                       "palate": "Medium body; high natural acidity; dry; saline mineral finish; 12.5-13% ABV; refreshing and focused",
                       "conclusion": "Estate quality; Portugal's Alvarinho benchmark; peak 2-6 years from vintage"},
    service_specs={"temperature_c": 10, "glass": "White Burgundy or large white wine glass",
                   "programme_position": "Aperitif; fish course; shellfish; grilled sea bream or sardines"},
    flavour_markers=["white peach", "lemon blossom", "saline mineral", "citrus blossom", "schist stone"],
    flavour_weight="medium-light", flavour_profile_type="dry_mineral",
    price_tier="mid_range", price_range_cad="$28-45",
    technical_specs={"grape": "Alvarinho 100%", "alcohol_abv": 12.8, "residual_sugar_gl": 3,
                     "sub_zone": "Monção e Melgaço", "altitude_m": 220,
                     "soil": "granite over schist"})

esporao_reserva = PROD(cur,
    "Esporão Reserva Tinto",
    "wine_still", esporao, ALENTEJO, origin_country="Portugal",
    subcategory="Alentejo DOC Tinto",
    description="Portugal's best-value quality red — Esporão Reserva Tinto from Reguengos de Monsaraz is the reference for understanding Alentejo at its quality threshold. A blend of Trincadeira, Aragonez (Tempranillo), Alicante Bouschet, and Touriga Nacional from 750-hectare organic estate vineyards on schist and granite soils under Alentejo's hot, dry Pannonian-influenced climate. Organic since 2010; David Baverstock's 30-year tenure has refined the style toward elegance rather than the extracted heaviness that characterised many Alentejo reds of the 1990s. The benchmark expression: ripe dark plum, dark cherry, dried herbs, and mineral texture — full-bodied but not heavy.",
    quality_tier="estate",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Private Selection", "criteria": "Single-vineyard selection; 18 months French oak; 10-15yr cellaring; competition benchmark"},
        {"tier": 3, "tier_name": "Reserva Tinto", "criteria": "Premium blend; best lots; 14 months French oak; 5-10yr cellaring potential; quality/price benchmark"},
        {"tier": 2, "tier_name": "Esporão Colheita Tinto", "criteria": "Standard blend; 6 months oak; earlier drinking; excellent QPR"},
        {"tier": 1, "tier_name": "Monte Velho Tinto", "criteria": "Entry level; 3-4 months oak; fresh fruit; immediate drinking; widely available"}
    ],
    deductive_profile={"appearance": "Deep ruby; full opacity; Alentejo concentration",
                       "nose": "Ripe dark plum, dark cherry, dried herbs (garrigue); medium oak influence; mineral schist undertone",
                       "palate": "Full-bodied; round tannins from warm Alentejo climate; 14-14.5% ABV; medium-long finish; herb and spice complexity",
                       "conclusion": "Estate quality; Portugal's most accessible quality red; peak 5-10 years from vintage"},
    service_specs={"temperature_c": 17, "glass": "Red Bordeaux glass",
                   "decant": "45 min recommended for Reserva", "programme_position": "Main course: grilled lamb, beef, cured meats, aged sheep cheese (Serpa)"},
    flavour_markers=["dark plum", "dark cherry", "dried herbs", "garrigue", "schist mineral", "cedar"],
    flavour_weight="full", flavour_profile_type="red_fruit_driven",
    price_tier="mid_range", price_range_cad="$20-35",
    technical_specs={"grapes": "Trincadeira, Aragonez, Alicante Bouschet, Touriga Nacional",
                     "alcohol_abv": 14.2, "ageing": "14 months French oak (30% new)",
                     "certification": "Organic (since 2010)"})

luis_pato_baga = PROD(cur,
    "Luis Pato Quinta do Ribeirinho Pé Franco Bairrada",
    "wine_still", luis_pato, BAIRRADA, origin_country="Portugal",
    subcategory="Bairrada DOC Baga",
    description="Portugal's most important age-worthy red — Pé Franco ('unrooted foot') designates own-rooted, pre-phylloxera vines that survived because Bairrada's clay soils prevented phylloxera from penetrating to root depth. The vine age: over 100 years. The grape: Baga at its most extreme — the tannin and acidity levels that discourage casual drinkers but enable 50-year cellaring in exceptional vintages. Luis Pato has spent four decades insisting that Baga is Portugal's Nebbiolo — requiring patience and specific food pairing but ultimately producing wines of extraordinary mineral complexity. The Pé Franco is his masterwork: pure Baga from ungrafted vines on Bairrada's distinctive blue clay-limestone.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Pé Franco (own-rooted pre-phylloxera)", "criteria": "100yr+ ungrafted vines; blue clay-limestone; extreme Baga; 30-50yr cellaring potential in top vintages; the estate's singular masterwork"},
        {"tier": 3, "tier_name": "Vinha Pan / Vinha Formal", "criteria": "Other single-vineyard Baga; younger vines; similar discipline; 15-25yr cellaring"},
        {"tier": 2, "tier_name": "Bairrada Tinto Clássico", "criteria": "Multi-vineyard Baga; earlier accessibility; classic Bairrada profile; 8-12yr cellaring"},
        {"tier": 1, "tier_name": "Vinho Regional Beiras Baga", "criteria": "Entry level; lighter extraction; earlier drinking; demonstrates fresh Baga character"}
    ],
    deductive_profile={"appearance": "Deep ruby with brick rim (age); lighter than Douro despite high tannin",
                       "nose": "Remarkable aromatic complexity: dried cherry, iron mineral, leather, dried herbs (bay leaf, thyme), tobacco; no fruit sweetness in youth; reveals florals and forest floor with 10+ years",
                       "palate": "Extreme acidity and tannin in youth — Baga's defining challenge; with 15+ years: silky resolution; extraordinary savoury mineral complexity; 12.5-13% ABV",
                       "conclusion": "Reserve quality; Portugal's most demanding and most rewarding red; do not open before 10 years; peak 20-40 years from vintage"},
    service_specs={"temperature_c": 16, "glass": "Red Burgundy glass — the Baga-Pinot Noir structural parallel",
                   "decant": "Required — 3+ hours for any vintage under 10 years",
                   "programme_position": "Game birds (partridge, quail), suckling pig (leitão), aged sheep cheese (Serpa, Azeitão)"},
    flavour_markers=["dried cherry", "iron mineral", "leather", "dried herbs", "tobacco", "forest floor"],
    flavour_weight="full", flavour_profile_type="red_mineral",
    price_tier="premium", price_range_cad="$60-95",
    technical_specs={"grape": "Baga 100%", "vine_age": "100yr+ own-rooted (pre-phylloxera)",
                     "alcohol_abv": 12.8, "soil": "blue clay-limestone (Bairrada argillaceous limestone)",
                     "ageing": "18-24 months old oak"})

crasto_old_vines = PROD(cur,
    "Quinta do Crasto Reserva Old Vines",
    "wine_still", crasto, DOURO_TABLE, origin_country="Portugal",
    subcategory="Douro DOC Tinto",
    description="Crasto's benchmark red — from old terraced schist vines above Pinhão in the Cima Corgo, produced by the Roquette family from traditional field-blend plots alongside single-variety Touriga Nacional and Touriga Franca parcels. The Reserva Old Vines represents the estate's quality-price apex: deeply concentrated Douro fruit (blackberry, cassis, graphite) with the structure to age 15+ years, at a price accessible enough to feature by the bottle on quality wine lists. Foot-trodden in traditional lagares during harvest; aged 18 months in French oak (30% new).",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Maria Teresa (single vineyard)", "criteria": "Oldest pre-phylloxera parcels; single vineyard; maximum concentration; ultra-limited allocation; 20-30yr cellaring"},
        {"tier": 3, "tier_name": "Reserva Old Vines", "criteria": "Old vine selection; Cima Corgo schist; foot-trodden; 18 months oak; 10-20yr cellaring; estate's quality-price benchmark"},
        {"tier": 2, "tier_name": "Crasto Tinto DOC", "criteria": "Standard Douro red; good varietal expression; 8-12 months oak; 5-10yr cellaring"},
        {"tier": 1, "tier_name": "Flôr de Crasto", "criteria": "Entry level; accessible Douro character; fresh fruit; early drinking"}
    ],
    deductive_profile={"appearance": "Very deep ruby-purple; opaque; classic Douro concentration",
                       "nose": "Blackberry, cassis, graphite, violet; schist mineral backbone; cedar oak integration at 5+ years",
                       "palate": "Full-bodied; structured tannins from schist-grown Touriga Nacional; 14-14.5% ABV; long graphite-mineral finish; 15yr+ cellaring potential",
                       "conclusion": "Reserve quality; the Douro's best-value serious red; exceptional QPR; peak 8-20 years from vintage"},
    service_specs={"temperature_c": 17, "glass": "Red Bordeaux glass",
                   "decant": "Required — 2 hours for vintages under 8 years", "programme_position": "Main course: lamb, beef, game; Portuguese bacalhau à Brás"},
    flavour_markers=["blackberry", "cassis", "graphite", "violet", "cedar", "schist mineral"],
    flavour_weight="full", flavour_profile_type="red_mineral",
    price_tier="mid_range", price_range_cad="$35-55",
    technical_specs={"grapes": "Touriga Nacional, Touriga Franca, old field-blend indigenes",
                     "alcohol_abv": 14.2, "ageing": "18 months French oak (30% new)",
                     "region": "Cima Corgo, Pinhão; altitude 150-350m"})

print("\n=== PORTUGAL TABLE WINE — REFERENCES ===")

ref_douro_table = REF(cur,
    "Douro DOC Table Wine — From Port Country to Fine Red Wine",
    "wine_regions",
    description="The Douro DOC table wine category covers the same schist-terraced valley as Port wine, but the same grapes fermented to dryness produce some of Portugal's — and Iberia's — most compelling red wines. The Douro Superior (furthest inland, most extreme heat/drought, highest altitude) produces the most concentrated table wines; Cima Corgo (centred on Pinhão) is the quality heartland; Baixo Corgo (closest to coast) is the most Atlantic-influenced and produces lighter, fresher styles.",
    key_principles="""DOURO TABLE WINE FRAMEWORK:

THREE SUB-ZONES:
Douro Superior: Hottest, driest; 400-700m altitude; most concentrated wines; Vale Meão, Ramos Pinto Quinta da Ervamoira
Cima Corgo: Quality heartland; Pinhão epicentre; 150-450m; Crasto, Niepoort, Ramos Pinto, Regueiro
Baixo Corgo: Most Atlantic influence; lighter styles; cooperative-dominated; less internationally visible

INDIGENOUS GRAPE VARIETIES:
Touriga Nacional: Primary red variety; high natural acidity; fine tannins; violet florals and dark fruit; ageing backbone
Touriga Franca: Perfume and elegance; historically undervalued; increasingly respected as principal
Tinta Roriz (Tempranillo): Structure and colour; the workhouse variety
Tinta Barroca: Softness and colour; ripens early; often blended
Tinta Amarela (Trincadeira): Niepoort's preferred variety for elegance and aromatics; underused by most producers

TERROIR LOGIC:
Schist soil: Fractures easily; allows deep root penetration (20-30m); forces vine water stress; concentration mechanism
Altitude: Every 100m elevation = approximately 0.6°C cooler; altitude determines freshness vs. concentration
Aspect: South-facing slopes = maximum sun; north-facing = higher acidity, lower alcohol

PORT PRODUCERS' TABLE WINE PROGRAMMES:
Niepoort (Redoma, Charme), Ramos Pinto (Duas Quintas), Quinta do Crasto — all Port families making fine table wine
Barca Velha (Ferreira) was the prototype in 1952; Vale Meão is the spiritual successor""",
    common_mistakes="Assuming Port wine knowledge transfers to Douro table wine — different extraction, different ageing, different balance point. Over-serving temperature (max 17°C). Opening too young — quality Douro reds need minimum 5 years.",
    pro_tips="The Douro Superior's altitude wines (Vale Meão, Ramos Pinto Ervamoira) are more structured and age-worthy than Baixo Corgo; pay attention to sub-zone on label when available. Niepoort's approach (field blends, no new oak) produces distinctly different wines than Touriga Nacional-dominant producers.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="João Ramos Pinto — The Douro Wine Guide; Dirk Niepoort personal notes; Wine Spectator Douro reports",
    authority_tier=1)

ref_vinho_verde_alvarinho = REF(cur,
    "Vinho Verde and Alvarinho — Portugal's Aromatic White from the Minho",
    "wine_regions",
    description="Vinho Verde covers Portugal's far northwest — the Minho/Green Wine country bordering Galicia. The name refers to youth and freshness, not colour. Standard Vinho Verde is a multi-variety blend of Loureiro, Trajadura, Arinto, and other local grapes — light, high-acid, often with slight effervescence from early bottling. The Monção e Melgaço sub-zone, growing exclusively Alvarinho (Albariño across the Galician border), produces Portugal's most elegant and age-worthy white wines — serious single-variety expressions demanding premium positioning.",
    key_principles="""VINHO VERDE HIERARCHY:

MONÇÃO E MELGAÇO (Alvarinho):
Climate: Sub-alpine influence; highest annual rainfall + longest dry season in Vinho Verde
Variety: Alvarinho 100% (permitted under Minho sub-regional rules)
Style: Full-bodied for Vinho Verde; 12.5-13% ABV; saline mineral; stone fruit; 3-8yr cellaring
Price positioning: Premium white — above standard Vinho Verde
References: Soalheiro, Anselmo Mendes, Quinta de Soalheiro, Quinta do Ameal

LIMA / BASTO / CÁVADO (Loureiro/multi-variety):
Style: Fresh, light (10.5-11.5% ABV), slight petillance; citrus and floral
Price: Entry white wine category; restaurant carafe potential; excellent aperitif

LIMA ALVARINHO (emerging):
Producing single-variety Alvarinho outside Monção e Melgaço; less recognised but rising quality

ALVARINHO vs. ALBARIÑO:
Same grape; different expression
Portuguese Alvarinho: More saline; more mineral; less floral than Spanish counterpart
Spanish Albariño (Rías Baixas): More aromatic floral lift; peachier fruit; often slightly lower acid
Shared characteristics: Stone fruit, citrus, saline mineral, medium body""",
    common_mistakes="Treating all Vinho Verde as light, simple party wine — Monção e Melgaço Alvarinho is a serious ageing wine. Confusing Alvarinho (Portuguese) with Albariño (Spanish) as identical — they share DNA but express differently. Over-chilling (serve at 10°C, not 6°C).",
    pro_tips="Aged Soalheiro Alvarinho (Evolução range — 2 years) demonstrates the variety's ageing capacity. When listing Vinho Verde, specify the sub-zone and variety on the list — 'Vinho Verde Alvarinho Monção e Melgaço' positions premium product correctly.",
    service_context="fine_dining, casual_dining",
    source_text="CVRVV — Comissão de Viticultura da Região dos Vinhos Verdes; Soalheiro estate documentation",
    authority_tier=1)

print("\n✅ Terminal 5 Batch 4 — Portugal table wine complete.")
print(f"""
PRODUCER IDs:
  vale_meao = {vale_meao}
  niepoort = {niepoort}
  crasto = {crasto}
  soalheiro = {soalheiro}
  esporao = {esporao}
  luis_pato = {luis_pato}

PRODUCT IDs:
  vale_meao_wine = {vale_meao_wine}
  niepoort_charme = {niepoort_charme}
  soalheiro_alvarinho = {soalheiro_alvarinho}
  esporao_reserva = {esporao_reserva}
  luis_pato_baga = {luis_pato_baga}
  crasto_old_vines = {crasto_old_vines}

REF IDs:
  ref_douro_table = {ref_douro_table}
  ref_vinho_verde_alvarinho = {ref_vinho_verde_alvarinho}
""")
