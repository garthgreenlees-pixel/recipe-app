#!/usr/bin/env python3
"""Batch 6 — Loire Valley (20 targets)"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

SANCERRE = 153
VOUVRAY = 151
MUSCADET = 148
SAVENNIERES = 154
ANJOU = 149

print("\n=== LOIRE VALLEY PRODUCERS ===")

dagueneau = P(cur, "Didier Dagueneau",
    producer_type="winery", region_id=SANCERRE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "The 'bad boy of Pouilly' revolutionised Sauvignon Blanc through ultra-low yields, "
        "barrel fermentation, and uncompromising selection. Dagueneau pioneered the idea that "
        "Pouilly-Fumé could age as long as premier cru Burgundy. His son Louis-Benjamin continues the domaine."
    ),
    key_personnel=["Didier Dagueneau (founder, d.2008)", "Louis-Benjamin Dagueneau (current)"],
    production_details={
        "hectares": 13,
        "yields": "very low, 15-25 hl/ha",
        "vinification": "barrel fermented in Allier oak, extended lees aging",
        "key_soils": "silex (flint), kimmeridgian limestone, oolitic limestone"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Universally regarded as the reference-standard producer for Pouilly-Fumé and Loire "
        "Sauvignon Blanc. Silex and Pur Sang command Burgundy Grand Cru-level prices."
    ),
    allocation_notes="Ultra-allocation; BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

huet = P(cur, "Domaine Huet",
    producer_type="winery", region_id=VOUVRAY, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "The undisputed reference for Vouvray and arguably the finest Chenin Blanc on earth. "
        "Biodynamic since 1990. Three single-vineyard Chenin Blancs in multiple styles (Sec, Demi-Sec, "
        "Moelleux, Petillant) depending on vintage. The wines age 30-50+ years."
    ),
    key_personnel=["Gaston Huet (founder)", "Noel Pinguet (longtime winemaker)", "Anthony Hwang (owner since 2002)"],
    production_details={
        "hectares": 35,
        "vineyards": ["Le Mont", "Clos du Bourg", "Le Haut-Lieu"],
        "styles": "sec, demi-sec, moelleux, petillant naturel",
        "key_soils": "tuffeau (volcanic chalk), clay-limestone"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Huet Vouvray wines are benchmarks for Chenin Blanc longevity. "
        "Highly sought; allocation through specialist importers."
    ),
    allocation_notes="Specialist allocation; BC — Classic Wine Imports [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

joly = P(cur, "Nicolas Joly — Coulee de Serrant",
    producer_type="winery", region_id=SAVENNIERES, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Nicolas Joly is the spiritual godfather of biodynamic viticulture. Coulee de Serrant "
        "is one of France's seven single-vineyard AOCs. The wines are grown on south-facing schist "
        "terraces above the Loire from old vines. Joly's book became the biodynamic manifesto."
    ),
    key_personnel=["Nicolas Joly (founder/philosopher)", "Virginie Joly (current)"],
    production_details={
        "hectares": 7,
        "monopole_aoc": "Coulee de Serrant — 7ha",
        "grape": "Chenin Blanc 100%",
        "key_soils": "dark volcanic schist, clay-sand"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Coulee de Serrant is among France's most historically significant white wines. "
        "Controversial but a fundamental reference for Savenni\u00e8res and Loire Chenin philosophy."
    ),
    allocation_notes="Ultra-limited; BC importer [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

cotat = P(cur, "Domaine Cotat",
    producer_type="winery", region_id=SANCERRE, country="France",
    production_philosophy="natural",
    philosophy_description=(
        "Francois and Pascal Cotat represent the old-guard Sancerre style: tiny yields, old vines, "
        "barrel fermentation, zero additions. Their Sancerres age 10-20 years easily."
    ),
    key_personnel=["Francois Cotat", "Pascal Cotat"],
    production_details={
        "hectares": 4,
        "key_wines": ["Les Monts Damnes", "La Grande Cote"],
        "vinification": "barrel fermented, aged 12-18 months on lees",
        "key_soils": "kimmeridgian limestone, silex"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Cotat Sancerres are among the most collectible Loire whites. "
        "A benchmark for serious Sauvignon Blanc aging potential."
    ),
    allocation_notes="Extremely limited; BC allocation [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

vacheron = P(cur, "Domaine Vacheron",
    producer_type="winery", region_id=SANCERRE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Biodynamic certified since 2011, Vacheron is the estate most associated with Sancerre's "
        "terroir diversity — both white (Sauvignon Blanc) and red (Pinot Noir) from single-vineyard "
        "parcels including Les Romains and Belle Dame."
    ),
    key_personnel=["Jean-Laurent Vacheron", "Jean-Dominique Vacheron"],
    production_details={
        "hectares": 49,
        "key_wines": ["Les Romains", "Belle Dame", "La Belle Dame Rouge"],
        "certification": "biodynamic (Demeter)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Top-tier Sancerre producer with broad range. Vacheron reds are among the best "
        "expressions of Sancerre Rouge."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

bourgeois = P(cur, "Henri Bourgeois",
    producer_type="winery", region_id=SANCERRE, country="France",
    production_philosophy="sustainable",
    philosophy_description=(
        "One of the most important names in Sancerre, with vineyards across the appellation's "
        "three soil types. Their flagship La Md d'Henry is one of Sancerre's great single-vineyard expressions."
    ),
    key_personnel=["Jean-Marie Bourgeois", "Arnaud Bourgeois"],
    production_details={
        "hectares": 70,
        "key_wines": ["La Md d'Henry", "Les Baronnes", "D'Antan"],
        "appellations": ["Sancerre", "Pouilly-Fume", "Marlborough NZ"]
    },
    quality_tier="estate",
    reputation_narrative=(
        "Highly reliable, broad portfolio across Sancerre price points. Good BC availability."
    ),
    allocation_notes="BC — Mark Anthony Group / agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

pepiere = P(cur, "Domaine de l'Ecu / Marc Ollivier (Pepiere)",
    producer_type="winery", region_id=MUSCADET, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Marc Ollivier's Domaine Pepiere is the definitive address for serious Muscadet, "
        "proving that Melon de Bourgogne can produce wines of genuine depth. His Cru Communaux "
        "spend years on lees before release, reframing Muscadet as a grand terroir wine."
    ),
    key_personnel=["Marc Ollivier", "Remi Branger (current winemaker)"],
    production_details={
        "hectares": 30,
        "key_wines": ["Clos des Briords", "Clisson", "Gras Moutons"],
        "sur_lie": "extended — Clisson 3+ years",
        "key_soils": "gabbro, orthogneiss, granite"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Pepiere has transformed the perception of Muscadet internationally. "
        "Clisson is a benchmark for extended sur-lie aging."
    ),
    allocation_notes="BC importer [NEEDS VERIFICATION]",
    price_positioning="mid_range", authority_tier=1)

villeneuve = P(cur, "Chateau de Villeneuve",
    producer_type="winery", region_id=ANJOU, country="France",
    production_philosophy="sustainable",
    philosophy_description=(
        "One of the top estates in Saumur-Champigny, producing serious Cabernet Franc "
        "from old vines on tuffeau soils — benchmarks for the appellation's aging capacity."
    ),
    key_personnel=["Jean-Pierre Chevallier"],
    production_details={
        "hectares": 30,
        "key_wines": ["Saumur-Champigny Les Cormiers", "Saumur Blanc"],
        "key_soils": "tuffeau"
    },
    quality_tier="estate",
    reputation_narrative="Top Saumur-Champigny estate; reference for Loire Cabernet Franc from tuffeau.",
    allocation_notes="BC importer [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== LOIRE VALLEY PRODUCTS ===")

dagueneau_silex = PROD(cur, "Didier Dagueneau Pouilly-Fume Silex",
    category="wine_still", producer_id=dagueneau, region_id=SANCERRE,
    subcategory="white",
    description=(
        "Silex is Dagueneau's most celebrated wine, grown on flint (silex) soils that impart "
        "a strikingly smoky, gunflint character unique in the Loire. Barrel fermented with "
        "extended lees aging, it combines the herbal energy of Sauvignon Blanc with a "
        "mineral precision that demands 5-15 years of cellaring."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Grand Cru equivalent", "aging_potential": "15-25 years"}],
    deductive_profile={
        "appearance": "gold with green tinge, brilliant",
        "nose": "struck flint, gunsmoke, white currant, grapefruit zest, white flower, lanolin",
        "palate": "intense, racy acidity, dense mineral extract, citrus oil, long saline finish",
        "signature": "the silex smoke — unmistakable gunflint note from flint soil",
        "blind_clues": "Sauvignon Blanc but more weight than Sancerre; smoke + mineral = Dagueneau"
    },
    service_specs={
        "temperature": "10-12C",
        "glassware": "white Burgundy glass",
        "decanting": "20 min for young vintages",
        "aging": "best 5-15 years from vintage"
    },
    flavour_markers=["gunflint", "white currant", "grapefruit zest", "lanolin", "white flower", "chalk mineral"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="ultra_premium",
    price_range_cad="$350-$600+",
    technical_specs={"grape": "Sauvignon Blanc 100%", "appellation": "Pouilly-Fume", "soil": "silex (flint)"})

dagueneau_pur_sang = PROD(cur, "Didier Dagueneau Pouilly-Fume Pur Sang",
    category="wine_still", producer_id=dagueneau, region_id=SANCERRE,
    subcategory="white",
    description=(
        "Pur Sang ('thoroughbred') grows on oolitic limestone, producing a wine that contrasts "
        "with Silex: creamier, more floral, with chalk-driven mineral structure rather than flint smoke. "
        "More approachable younger than Silex."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Grand Cru equivalent", "vs_silex": "more floral, chalky; less smoky"}],
    deductive_profile={
        "nose": "white flower, chalk, lemon curd, guava, fennel frond",
        "palate": "round entry, intense acidity, limestone mineral, long finish",
        "signature": "chalk-cream texture distinct from silex's angularity"
    },
    service_specs={"temperature": "10-12C", "glassware": "white Burgundy bowl"},
    flavour_markers=["chalk mineral", "white flower", "lemon curd", "guava", "fennel"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="ultra_premium",
    price_range_cad="$280-$480",
    technical_specs={"grape": "Sauvignon Blanc 100%", "soil": "oolitic limestone"})

huet_le_mont_sec = PROD(cur, "Domaine Huet Vouvray Le Mont Sec",
    category="wine_still", producer_id=huet, region_id=VOUVRAY,
    subcategory="white",
    description=(
        "Le Mont Sec is Huet's bone-dry expression from the Le Mont vineyard on tuffeau soils. "
        "In great years it rivals the finest dry whites in France — laser-focused, electric acidity, "
        "profound mineral depth. Chenin Blanc in this style lasts 20-40 years."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"vineyard": "Le Mont — tuffeau clay, south-facing", "aging_potential": "20-40+ years"}],
    deductive_profile={
        "appearance": "pale gold, brilliant",
        "nose": "quince, beeswax, hay, tuffeau chalk, dried apricot",
        "palate": "bone dry, nerve-shaking acidity, medium-full body, incredible length",
        "signature": "tuffeau mineral plus Chenin quince-beeswax complexity",
        "blind_clues": "Loire Chenin — waxy, quince, electric acidity"
    },
    service_specs={
        "temperature": "10-12C",
        "glassware": "white Burgundy glass",
        "aging": "optimal 10-30 years from vintage"
    },
    flavour_markers=["quince", "beeswax", "tuffeau chalk", "dried apricot", "hay", "white flower"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$80-$140",
    technical_specs={"grape": "Chenin Blanc 100%", "appellation": "Vouvray", "soil": "tuffeau"})

huet_cb_demi_sec = PROD(cur, "Domaine Huet Vouvray Clos du Bourg Demi-Sec",
    category="wine_still", producer_id=huet, region_id=VOUVRAY,
    subcategory="white",
    description=(
        "Clos du Bourg is Huet's walled monopole — 5.5ha of finest tuffeau. The Demi-Sec "
        "(off-dry, 15-40g/L RS) is perfectly balanced by Chenin's electric acidity, making it "
        "simultaneously a food wine and a meditation wine. Great vintages age 30-50 years."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"vineyard": "Clos du Bourg monopole — finest tuffeau in Vouvray", "aging_potential": "30-50 years"}],
    deductive_profile={
        "nose": "honeysuckle, preserved quince, beeswax, golden apple, tuffeau mineral",
        "palate": "off-dry entry, then crystalline acidity takes over, long saline finish",
        "signature": "off-dry tension — sweetness and acidity in perfect equilibrium"
    },
    service_specs={
        "temperature": "10-12C",
        "food_pairing": "foie gras, Comte, roasted pork, spiced poultry",
        "aging": "drink at 10-30 years; great vintages 30-50"
    },
    flavour_markers=["honeysuckle", "quince preserve", "beeswax", "golden apple", "tuffeau mineral"],
    flavour_weight="medium-full",
    flavour_profile_type="off-dry mineral",
    price_tier="premium",
    price_range_cad="$90-$160",
    technical_specs={"grape": "Chenin Blanc", "appellation": "Vouvray", "style": "demi-sec", "rs": "15-40g/L"})

coulee_de_serrant = PROD(cur, "Coulee de Serrant — Nicolas Joly",
    category="wine_still", producer_id=joly, region_id=SAVENNIERES,
    subcategory="white",
    description=(
        "Coulee de Serrant is one of France's most historically significant wines and one of only "
        "seven single-vineyard AOCs. The 7ha monopole sits on south-facing schist terraces above "
        "the Loire. Grown biodynamically from old-vine Chenin Blanc, the wine requires 5-10 years "
        "minimum before the austere structure resolves."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Monopole AOC — Grand Cru equivalent", "aging_potential": "20-40 years"}],
    deductive_profile={
        "appearance": "deep gold, sometimes amber with age",
        "nose": "schist mineral, quince, dried flowers, beeswax, wood resin",
        "palate": "austere, firm phenolics from Chenin, electric acidity, mineral length",
        "signature": "the Loire's most austere and demanding Chenin — requires patience",
        "blind_clues": "Loire Chenin with schist grip; darker and more resinous than Vouvray"
    },
    service_specs={
        "temperature": "12-14C",
        "decanting": "1-2 hours recommended",
        "aging": "5-10 years minimum; ideal 15-25 years"
    },
    flavour_markers=["schist mineral", "quince", "dried flowers", "beeswax", "wood resin", "graphite"],
    flavour_weight="full",
    flavour_profile_type="mineral-driven",
    price_tier="ultra_premium",
    price_range_cad="$180-$350",
    technical_specs={"grape": "Chenin Blanc 100%", "appellation": "Coulee de Serrant AOC", "soil": "volcanic schist"})

cotat_monts_damnes = PROD(cur, "Domaine Cotat Sancerre Les Monts Damnes",
    category="wine_still", producer_id=cotat, region_id=SANCERRE,
    subcategory="white",
    description=(
        "Les Monts Damnes is Cotat's flagship from the steepest vineyard in Sancerre — pure "
        "kimmeridgian limestone slopes. Old vines, barrel fermented, aged 18 months on lees. "
        "The wine defies Sauvignon Blanc convention: iodine, oyster shell, white flower, "
        "and a saline finish that lasts 60 seconds."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"vineyard": "Les Monts Damnes — steep kimmeridgian, 50+ year old vines", "aging_potential": "15-25 years"}],
    deductive_profile={
        "nose": "oyster shell, iodine, white flower, preserved lemon, chalk",
        "palate": "lean, electric, saline mineral, long oyster-iodine finish",
        "signature": "closest to Chablis Premier Cru of any Loire Sauvignon — terroir dominant"
    },
    service_specs={"temperature": "10C", "glassware": "narrow white glass preserving mineral tension"},
    flavour_markers=["oyster shell", "iodine", "chalk mineral", "white flower", "preserved lemon"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="ultra_premium",
    price_range_cad="$150-$280",
    technical_specs={"grape": "Sauvignon Blanc", "soil": "kimmeridgian limestone", "appellation": "Sancerre"})

vacheron_sancerre = PROD(cur, "Domaine Vacheron Sancerre Les Romains",
    category="wine_still", producer_id=vacheron, region_id=SANCERRE,
    subcategory="white",
    description=(
        "Les Romains is Vacheron's single-vineyard flagship from silex soils. Biodynamically farmed, "
        "barrel fermented with extended lees contact — the house style leaning toward Burgundian "
        "weight and texture while retaining Sauvignon Blanc's citrus-herbal notes."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"vineyard": "Les Romains — silex soils, old vines", "aging_potential": "8-15 years"}],
    deductive_profile={
        "nose": "silex smoke, pink grapefruit, elderflower, chalk, fennel frond",
        "palate": "medium-full body, creamy lees texture, long mineral finish",
        "signature": "rounder and more Burgundian than Cotat; silex smoke without Dagueneau's weight"
    },
    service_specs={"temperature": "10-12C"},
    flavour_markers=["silex smoke", "grapefruit", "elderflower", "chalk", "lees cream"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$85-$140",
    technical_specs={"grape": "Sauvignon Blanc", "soil": "silex", "appellation": "Sancerre"})

muscadet_pepiere = PROD(cur, "Domaine Pepiere Muscadet Sevre et Maine Clisson",
    category="wine_still", producer_id=pepiere, region_id=MUSCADET,
    subcategory="white",
    description=(
        "Clisson is the apex of Pepiere's Muscadet — a Cru Communal on ancient gabbro and granite "
        "soils, aged 3+ years on lees before release. Full-bodied, texturally dense, saline-mineral, "
        "with 10-20 years aging potential. It reframes Melon de Bourgogne as a serious terroir grape."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"classification": "Cru Communal Clisson", "sur_lie_aging": "3+ years", "aging_potential": "10-20 years"}],
    deductive_profile={
        "nose": "saline, oyster shell, green apple, lemon curd, granite mineral, fresh herbs",
        "palate": "medium-full body from lees contact, bright acidity, long saline finish",
        "signature": "Muscadet weight — challenges expectation; old-vine Melon depth"
    },
    service_specs={"temperature": "8-10C", "pairing": "Atlantic shellfish — oysters, clams, langoustines"},
    flavour_markers=["saline", "oyster shell", "lemon curd", "green apple", "granite mineral"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="mid_range",
    price_range_cad="$45-$80",
    technical_specs={"grape": "Melon de Bourgogne", "appellation": "Muscadet Sevre et Maine sur Lie", "soil": "gabbro"})

print("\n=== LOIRE REFERENCES ===")

ref_loire_diversity = REF(cur,
    "Loire Valley — Appellation Hierarchy and Grape Diversity",
    category="wine_regions", skill_level="advanced",
    description=(
        "The Loire Valley is France's most diverse wine region — 1,000km of river, 50+ AOCs, "
        "and 4 key grape varieties that produce completely different styles by sub-region. "
        "Essential geography, grape-appellation mapping, and style hierarchy for Loire navigation."
    ),
    key_principles=(
        "1. SAUVIGNON BLANC: Upper Loire — Sancerre and Pouilly-Fume are benchmark AOCs. "
        "Sancerre: three soil types (kimmeridgian, silex, limestone); styles vary accordingly. "
        "Pouilly-Fume: flint and limestone soils; Dagueneau defines the upper tier. "
        "Also: Menetou-Salon (value alternative), Quincy, Reuilly. "
        "2. CHENIN BLANC: Middle Loire — Vouvray, Savennieres, Anjou, Saumur. "
        "Vouvray: range from bone-dry (Sec) through Demi-Sec, Moelleux to Petillant. "
        "Savennieres: dry, austere, structured — Coulee de Serrant is the monopole AOC. "
        "3. CABERNET FRANC: Touraine reds — Chinon, Bourgueil, Saumur-Champigny. "
        "Produces vivid, herbal, violet-scented reds from tuffeau. Age well 10-20 years. "
        "4. MELON DE BOURGOGNE: Pays Nantais — Muscadet Sevre-et-Maine, Cru Communaux. "
        "Sur-lie aging (months to years) is the defining technique. "
        "Cru Communaux (Clisson, Gorges, Le Pallet) are the quality apex. "
        "5. SWEET WINES: Coteaux du Layon, Quarts de Chaume (Grand Cru), Bonnezeaux — "
        "all Chenin Blanc botrytis from the Layon river valley."
    ),
    common_mistakes=(
        "Assuming all Sancerre is the same regardless of soil type. "
        "Treating Muscadet as a simple service wine without recognising Cru Communaux. "
        "Serving Vouvray Demi-Sec as a dessert wine (it pairs with savoury food). "
        "Confusing Sancerre Rouge (Pinot Noir) with Loire Cabernet Franc reds."
    ),
    pro_tips=(
        "The three Sancerre soil types produce distinctly different wines: kimmeridgian = mineral/taut; "
        "silex = smoky/angular; limestone/clay = rounder/more aromatic. "
        "Vouvray Sec from Huet lasts longer than most red Burgundies. "
        "Clisson Cru Communal Muscadet at 8-10 years is one of the best-value aged whites in France."
    ),
    authority_tier=1,
    source_text="WSET Diploma / CMS Advanced Sommelier curriculum; Oxford Companion to Wine"
)

ref_chenin_vouvray = REF(cur,
    "Chenin Blanc — Vouvray and Loire Style Spectrum",
    category="wine_knowledge", skill_level="master",
    description=(
        "Chenin Blanc's defining attributes — electric acidity, extraordinary longevity, "
        "and chameleonic ability to express terroir and botrytis — are best understood through "
        "Vouvray. Style spectrum, vintage variation, and deductive framework for Loire Chenin."
    ),
    key_principles=(
        "GRAPE FUNDAMENTALS: Chenin Blanc has naturally high acidity (pH 3.0-3.2 even in ripe "
        "years), thin skins, and very high sugar potential. These properties mean: "
        "(a) it can produce bone-dry wines with extraordinary tension; "
        "(b) residual sugar is balanced naturally by acidity; "
        "(c) botrytis concentrates sugars without losing freshness. "
        "VOUVRAY STYLE SPECTRUM (vintage dependent): "
        "Sec: under 4g RS, bone-dry, electric; great years: 1989, 1990, 2002, 2018, 2022. "
        "Demi-Sec: 15-40g RS, off-dry; quintessential style for most vintages. "
        "Moelleux: 40-100g RS, luscious; requires botrytis influence. "
        "THE KEY INSIGHT: Style is vintage-determined, not pre-planned. "
        "DEDUCTIVE FRAMEWORK: "
        "Nose clues: quince, beeswax, hay, tuffeau chalk, preserved lemon (young); "
        "honey, lanolin, dried apricot, saffron (aged). "
        "Palate clues: electric acidity always present; "
        "phenolic grip ('bitter almond' finish) — unique to Chenin. "
        "AGING: Huet Clos du Bourg Moelleux 1947 is still alive. "
        "Even Sec needs 5-10 years. The rule: if in doubt, wait."
    ),
    common_mistakes=(
        "Confusing Vouvray Demi-Sec with dessert wine (it is a food wine). "
        "Under-estimating Vouvray Sec aging potential (rivals Meursault). "
        "Neglecting the bitter-almond finish as a Chenin blind tasting clue."
    ),
    pro_tips=(
        "The beeswax + quince combination is Chenin Blanc's fingerprint. "
        "Aged Vouvray (10+ years) is one of the most underpriced great whites in France. "
        "Cotat's mineral-dominant Sancerre style mimics Chenin's depth from Sauvignon Blanc — "
        "useful comparison to show how soil overrides grape expectations."
    ),
    authority_tier=1,
    source_text="Huet domaine literature; WSET Diploma Unit 3; Jacqueline Friedrich 'A Wine and Food Guide to the Loire'"
)

print("\n=== LOIRE PAIRINGS ===")

PAIR(cur, "Crottin de Chavignol warm goat cheese with chervil and chive",
     "dairy_fermented", "starter",
     "classic", "complement",
     "The Loire Valley's most iconic pairing: Crottin de Chavignol made 5km from Sancerre vineyards. "
     "Sauvignon Blanc's herbaceous and mineral character cuts the lactic cream; Cotat's iodine "
     "mineral mirrors the goat's tang.",
     cotat_monts_damnes, food_flavour_profile="tangy, lactic, fresh herb", beverage_category="wine_still")

PAIR(cur, "Fine de Claire oysters with mignonette granita",
     "seafood_sashimi", "aperitif",
     "classic", "complement",
     "Atlantic oysters and Muscadet is the great French terroir pairing. Clisson's saline mineral "
     "and oyster shell character literally reflects the shellfish it pairs with. "
     "Iodine meets iodine; acidity cleanses the brine.",
     muscadet_pepiere, food_flavour_profile="briny, iodine, cold mineral", beverage_category="wine_still")

PAIR(cur, "Pike perch quenelles with Nantua sauce and crayfish butter",
     "seafood_general", "main",
     "classic", "complement",
     "The Loire's classic white-wine-and-river-fish pairing. Huet Le Mont Sec's electric acidity "
     "and tuffeau mineral cuts through the rich butter sauce while matching the dish's substance.",
     huet_le_mont_sec, food_flavour_profile="rich butter, crayfish, cream, herbal", beverage_category="wine_still")

PAIR(cur, "Foie gras terrine with quince gelee and brioche toast",
     "charcuterie_cured", "starter",
     "classic", "complement",
     "Huet Clos du Bourg Demi-Sec is one of the world's great foie gras pairings. "
     "Off-dry sweetness meets the richness of foie gras, while Chenin's electric acidity "
     "prevents cloying. The quince gelee mirrors the wine's flavour directly.",
     huet_cb_demi_sec, food_flavour_profile="rich, fatty, sweet, quince", beverage_category="wine_still")

PAIR(cur, "Pork rillons with grain mustard and cornichons",
     "charcuterie_cured", "casual",
     "established", "contrast",
     "A Loire terroir pairing: pork rillons (crisp confit pork belly) from Touraine with "
     "Savennieres Chenin. The wine's phenolic grip and austerity cuts through rendered pork fat; "
     "mustard's acidity mirrors Chenin's electric structure.",
     coulee_de_serrant, food_flavour_profile="rendered pork fat, smoky, mustard, acidity", beverage_category="wine_still")

PAIR(cur, "River crayfish bisque with tarragon cream",
     "seafood_general", "starter",
     "established", "complement",
     "Dagueneau Silex's gunflint mineral and lees richness stands up to cream-based bisque. "
     "Sauvignon Blanc's herbal energy connects with tarragon; the flint smokiness adds complexity.",
     dagueneau_silex, food_flavour_profile="sweet crayfish, tarragon cream, herbal", beverage_category="wine_still")

PAIR(cur, "Loire salmon en papillote with beurre blanc",
     "seafood_general", "fish_course",
     "classic", "complement",
     "Beurre blanc was invented in the Loire Valley — a sauce of shallots reduced in Muscadet "
     "or Vouvray. Vacheron Sancerre with salmon in Loire beurre blanc closes the terroir loop; "
     "Sauvignon Blanc's acidity mirrors the wine in the sauce.",
     vacheron_sancerre, food_flavour_profile="salmon, herb, butter-vinegar sauce", beverage_category="wine_still")

print("\n=== LOIRE SERVICE PROTOCOL ===")

PROTOCOL(cur,
    "Loire Chenin Blanc Service — Vouvray and Savennieres",
    category="wine_presentation", beverage_family="wine",
    procedure=(
        "1. PRE-SERVICE: Confirm vintage age. Young Vouvray Sec (under 5 years): serve at 10C. "
        "Aged Vouvray (5-15 years): allow to open at 12C — serve warmer to unlock complexity. "
        "Very old Vouvray/Savennieres (15+ years): decant briefly (15-20 min) to remove bottle reduction. "
        "2. GLASSWARE: White Burgundy glass — wider bowl than Sauvignon Blanc glasses allows "
        "Chenin's waxy aromatic complex to develop fully. "
        "3. PRESENTATION: State vintage, vineyard, and style (Sec/Demi-Sec/Moelleux) clearly. "
        "For Demi-Sec: alert the guest to the off-dry style — many mistake it for Sec. "
        "4. POUR: Small initial pour (30ml) to check for premature oxidation or reduction. "
        "Older wines may show initial reduction (struck match, struck stone) — this will blow off. "
        "5. GUEST COMMUNICATION: For unfamiliar guests, position Loire Chenin against "
        "other whites they know: 'More electric acidity than Chablis; more waxy complexity than Sancerre; "
        "longer aging potential than almost any dry white in France.' "
        "6. FOOD GUIDANCE: Sec — grilled fish, goat cheese, light poultry; "
        "Demi-Sec — foie gras, pork rillettes, Comte, mild Asian spice; "
        "Moelleux — alone or with Roquefort, blue cheese, fruit desserts."
    ),
    description=(
        "Service protocol for Loire Valley Chenin Blanc, covering Vouvray across styles "
        "and Savennieres (including Coulee de Serrant). Focus on vintage assessment, style "
        "communication to guests, and appropriate glassware and temperature."
    ),
    rationale=(
        "Chenin Blanc is the most misunderstood of France's great white grapes — often "
        "underestimated because of basic Vouvray. The service protocol must bridge the gap "
        "between guest expectation and the wine's actual quality level and complexity."
    ),
    common_errors=(
        "Serving Demi-Sec without alerting guests to off-dry style. "
        "Dismissing initial reduction in old Vouvray as a fault — it will resolve. "
        "Using narrow Sauvignon Blanc-style glass which inhibits aromatic development. "
        "Serving aged Vouvray too cold — needs 12C minimum to show."
    ),
    service_context="fine_dining, sommelier_recommendation",
    equipment_required=["white Burgundy wine glass", "decanter (for aged wines)"],
    guest_communication=(
        "For unfamiliar guests: 'Vouvray from Huet is one of France's longest-lived white wines — "
        "this style has been made here for centuries. The wine has extraordinary precision and will "
        "continue developing for another 20 years.' "
        "For Demi-Sec: 'This style is off-dry — the sweetness is perfectly balanced by Chenin's "
        "electric acidity. It pairs beautifully with the foie gras or the pork.'"
    ),
    skill_level="advanced", authority_tier=1,
    source_text="CMS Advanced Sommelier curriculum; Guild of Sommeliers Loire Valley module"
)

print("\n✅ Loire Valley batch complete.")
cur.close()
conn.close()
