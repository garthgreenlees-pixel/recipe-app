#!/usr/bin/env python3
"""Batch 7 — Alsace (15 targets)
Producers: Trimbach, Zind-Humbrecht, Weinbach, Hugel, Deiss, Ostertag
Products: Clos Sainte Hune, Clos Windsbuhl Riesling, Schlossberg GC Riesling, Jubilee Riesling,
          Trimbach Gewurztraminer, Hengst GC Pinot Gris, Weinbach Tokay PG, Deiss Bergheim,
          Hugel VT Riesling, Ostertag Muenchberg Riesling, Trimbach Cuvee Frederic Emile
References: Alsace Grand Cru and Varietal Hierarchy; VT/SGN Guide
Pairings: choucroute, munster, foie gras, trout, tarte flambee
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

ALSACE = 155

print("\n=== ALSACE PRODUCERS ===")

trimbach = P(cur, "Trimbach",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Trimbach is the definitive address for dry, ageworthy Alsatian Riesling in the "
        "Alsace Classique tradition. Family-owned for 13 generations in Ribeauville, they "
        "reject the trend toward sweetness and produce wines of razor precision and austerity. "
        "Clos Sainte Hune — a 1.67ha monopole within Rosacker Grand Cru — is arguably "
        "France's greatest dry white wine outside of Burgundy. Cuvee Frederic Emile, from "
        "old vines in Geisberg and Osterberg Grand Crus, is the second flag wine."
    ),
    key_personnel=["Jean Trimbach", "Pierre Trimbach", "Anne Trimbach"],
    production_details={
        "founded": 1626,
        "hectares": 45,
        "flagship": "Clos Sainte Hune (1.67ha monopole within Rosacker GC)",
        "style": "dry, mineral, age-worthy — Alsace Classique"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Trimbach is the benchmark reference for serious Alsatian Riesling. Clos Sainte Hune "
        "is among the most age-worthy dry whites in the world — regularly compared to Montrachet "
        "and DRC La Tache in longevity. Available through top wine merchants and importers."
    ),
    allocation_notes="BC — Lifford Wine Agency / Charton Hobbs [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

zind_humbrecht = P(cur, "Zind-Humbrecht",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Olivier Humbrecht MW is the most influential figure in modern Alsatian viticulture. "
        "The estate pioneered biodynamic farming in Alsace and championed the expression of "
        "individual Grand Cru terroir. Their range spans all four noble varieties across "
        "seven Grand Crus including Rangen de Thann (volcanic; Alsace's steepest and most "
        "extreme vineyard), Brand, Hengst, Clos Windsbuhl, and Clos Saint Urbain. "
        "Wines range from bone-dry to TBA-level sweetness depending on vintage."
    ),
    key_personnel=["Olivier Humbrecht MW (winemaker)", "Leonard Humbrecht (founder)"],
    production_details={
        "hectares": 40,
        "grand_crus": ["Rangen de Thann", "Brand", "Hengst", "Goldert", "Herrenweg"],
        "monopoles": ["Clos Windsbuhl", "Clos Saint Urbain (within Rangen)", "Clos Jebsal"],
        "certification": "biodynamic (Biodyvin)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Zind-Humbrecht represents the pinnacle of terroir-driven Alsatian winemaking. "
        "Wines require extended aging (5-20 years) to show their full complexity. "
        "Extremely sought-after globally; key allocation through specialist importers."
    ),
    allocation_notes="BC — Select Wine Merchants / agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

weinbach = P(cur, "Domaine Weinbach",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Domaine Weinbach is the most elegant and perfumed expression of Alsatian winemaking. "
        "The estate is based in the Clos des Capucins — a historic walled vineyard in Kaysersberg — "
        "and produces wines of extraordinary aromatic intensity and finesse. "
        "The Faller family (now the Colette Faller generation) farmed biodynamically since 2010. "
        "Their Riesling Schlossberg Sainte Catherine and Gewurztraminer Altenbourg Quintessence "
        "are legendary expressions."
    ),
    key_personnel=["Colette Faller (matriarch)", "Catherine Faller", "Laurence Faller"],
    production_details={
        "hectares": 30,
        "key_wines": ["Schlossberg Sainte Catherine", "Quintessence", "Cuvee Theo"],
        "key_soils": "granite (Schlossberg), clay-limestone (Clos des Capucins)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Weinbach is the reference for pure aromatic Alsatian wines. Schlossberg Grand Cru "
        "Rieslings are benchmark granite-mineral expressions. Among Alsace's most admired estates."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

hugel = P(cur, "Hugel et Fils",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Hugel is one of Alsace's most historic estates (founded 1639) and was instrumental in "
        "codifying Vendange Tardive and Selection de Grains Nobles regulations in 1976. "
        "Based in Riquewihr, they combine a strong négociant business with estate wines. "
        "The estate Jubilee range from old-vine parcels is consistently excellent. "
        "Their VT and SGN Rieslings are benchmark sweet Alsatian wines."
    ),
    key_personnel=["Jean-Frédéric Hugel", "Marc Hugel"],
    production_details={
        "founded": 1639,
        "hectares": 26,
        "key_wines": ["Jubilee Riesling", "Schoelhammer Riesling", "VT/SGN cuvees"],
        "vt_sng_pioneer": "Hugel codified VT/SGN regulations in 1976"
    },
    quality_tier="estate",
    reputation_narrative=(
        "Among Alsace's most important historic houses. Hugel Jubilee represents "
        "excellent estate-level quality. VT and SGN wines are internationally collected."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

deiss = P(cur, "Marcel Deiss",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Marcel Deiss champions a controversial philosophy: that Alsace wines should be "
        "defined by terroir, not by grape variety. His Grand Cru and Lieux-Dits wines are "
        "field blends of multiple varieties co-planted and co-fermented in the Burgundian tradition. "
        "Bergheim (his most accessible terroir wine) blends Riesling, Gewurztraminer, and Pinot Gris "
        "from the limestone-clay soils of Bergheim. Altenberg de Bergheim Grand Cru is the flagship."
    ),
    key_personnel=["Jean-Michel Deiss", "Mathieu Deiss"],
    production_details={
        "hectares": 27,
        "philosophy": "terroir over grape variety — field blends on Grand Cru sites",
        "key_soils": "limestone-clay (Bergheim), Jurassic limestone (Altenberg)",
        "key_wines": ["Altenberg de Bergheim GC", "Schoenenbourg GC", "Burlenberg"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Deiss is a polarising but deeply thoughtful producer. The approach — blending multiple "
        "varieties per Grand Cru — is philosophically significant and produces compelling terroir wines."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

ostertag = P(cur, "Domaine Ostertag",
    producer_type="winery", region_id=ALSACE, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Andre Ostertag is one of Alsace's most intellectually driven winemakers. Biodynamic "
        "since 1997, he produces two clearly distinct ranges: the terroir-driven 'Vignobles' "
        "wines (named by appellation/soil) and the grape-driven 'Fruits d'Alsace' range. "
        "His Muenchberg Grand Cru Riesling — from volcanic sandstone — is the flagship and "
        "one of Alsace's most distinctive expressions: smoky, spicy, and deeply mineral."
    ),
    key_personnel=["Andre Ostertag", "Arthur Ostertag"],
    production_details={
        "hectares": 15,
        "key_wines": ["Muenchberg GC Riesling", "Fronholz Pinot Gris", "Heissenberg"],
        "key_soils": "volcanic sandstone (Muenchberg), clay-limestone (Fronholz)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Ostertag is highly regarded by natural wine enthusiasts and sommeliers for intellectual "
        "precision and quality. Muenchberg is a benchmark for volcanic-mineral Riesling."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== ALSACE PRODUCTS ===")

clos_sainte_hune = PROD(cur, "Trimbach Riesling Clos Sainte Hune",
    category="wine_still", producer_id=trimbach, region_id=ALSACE,
    subcategory="white",
    description=(
        "Clos Sainte Hune is widely regarded as France's greatest dry Riesling and one of the "
        "world's most age-worthy white wines. The 1.67ha monopole within Rosacker Grand Cru is "
        "planted on blue limestone and clay in Hunawihr. Bone dry (under 5g RS), with volcanic "
        "precision, extraordinary mineral depth, and a finish that lasts several minutes. "
        "Released only in the best vintages; requires 10-20 years minimum before peak."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Monopole within Grand Cru — France's greatest dry Riesling",
        "aging_potential": "20-40+ years",
        "vintage_comparison": "often compared to DRC La Tache in longevity"
    }],
    deductive_profile={
        "appearance": "pale gold, brilliant, green-tinged when young",
        "nose": "petrol (developed), lime zest, white flower, crushed stone, wet slate, beeswax",
        "palate": "bone dry, electric acidity, extraordinary mineral extract, 60+ second finish",
        "signature": "the 'kerosene' petrol note of mature Alsatian Riesling at peak — unmistakable",
        "blind_clues": "dry Riesling with petrol + slate + extreme length = Alsace; weight > Mosel"
    },
    service_specs={
        "temperature": "12-14C (warmer than most whites to show complexity)",
        "glassware": "white Burgundy glass — Riesling glass too narrow for this wine",
        "aging": "10 years minimum; ideal 15-30 years",
        "decanting": "30-45 min for young vintages"
    },
    flavour_markers=["petrol", "lime zest", "crushed stone", "wet slate", "white flower", "beeswax"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="ultra_premium",
    price_range_cad="$350-$600+",
    technical_specs={
        "grape": "Riesling 100%",
        "appellation": "Alsace Grand Cru Rosacker (monopole)",
        "soil": "blue limestone and clay",
        "rs": "under 5g/L"
    })

frederic_emile = PROD(cur, "Trimbach Riesling Cuvee Frederic Emile",
    category="wine_still", producer_id=trimbach, region_id=ALSACE,
    subcategory="white",
    description=(
        "Cuvee Frederic Emile is Trimbach's second flagship — old-vine Riesling from "
        "Geisberg and Osterberg Grand Crus in Ribeauville. Bone dry, intensely mineral, "
        "with remarkable aging capacity (15-25 years). The best available alternative "
        "to Clos Sainte Hune and dramatically more accessible in volume and price."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Grand Cru equivalent (Geisberg + Osterberg blend)",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "lime, green apple, petrol (with age), flint, white pepper, chalk mineral",
        "palate": "bone dry, linear, firm acidity, granite mineral, long finish",
        "signature": "Trimbach austerity — drier and more linear than most Alsatian Riesling"
    },
    service_specs={"temperature": "12C", "aging": "8-20 years"},
    flavour_markers=["lime", "green apple", "petrol", "flint", "white pepper", "chalk"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$85-$150",
    technical_specs={
        "grape": "Riesling",
        "appellation": "Alsace Grand Cru (Geisberg + Osterberg)",
        "rs": "under 5g/L"
    })

clos_windsbuhl = PROD(cur, "Zind-Humbrecht Riesling Clos Windsbuhl",
    category="wine_still", producer_id=zind_humbrecht, region_id=ALSACE,
    subcategory="white",
    description=(
        "Clos Windsbuhl is Zind-Humbrecht's monopole in Hunawihr, grown on muschelkalk "
        "(fossilised shell limestone) soils that produce a unique saline, oyster-mineral "
        "Riesling. The wine has extraordinary tension and mineral depth, alternating between "
        "bone dry and lightly off-dry depending on vintage conditions. "
        "A benchmark for the saline-mineral style of Alsatian Riesling."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Monopole — lieu-dit level",
        "soil_signature": "muschelkalk — saline, oyster mineral",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "oyster mineral, saline, white flower, lime, petrol (with age)",
        "palate": "electric acidity, saline mineral backbone, extraordinary length",
        "signature": "oyster-saline mineral from muschelkalk limestone — unique in Alsace"
    },
    service_specs={"temperature": "11-13C", "aging": "8-20 years"},
    flavour_markers=["oyster mineral", "saline", "white flower", "lime", "chalk"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$120-$200",
    technical_specs={
        "grape": "Riesling",
        "appellation": "Alsace (monopole Clos Windsbuhl, Hunawihr)",
        "soil": "muschelkalk (fossilised shell limestone)"
    })

hengst_pinot_gris = PROD(cur, "Zind-Humbrecht Pinot Gris Hengst Grand Cru",
    category="wine_still", producer_id=zind_humbrecht, region_id=ALSACE,
    subcategory="white",
    description=(
        "Hengst Grand Cru is Zind-Humbrecht's premier site for Pinot Gris — heavy clay-marl "
        "soils that produce enormously rich, structured Pinot Gris with extraordinary aging capacity. "
        "The wine ranges from slightly off-dry to fully luscious depending on vintage. "
        "It represents the apex of Alsatian Pinot Gris — a grape that here produces something "
        "closer to Burgundian Pinot Blanc in weight than to Italian Pinot Grigio."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Grand Cru Hengst — clay-marl richness",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "smoked bacon, truffle, brioche, golden apple, spice, hazelnut",
        "palate": "very full body, oily texture, complex spice, long finish",
        "signature": "smoked/truffle aromatic — unique to Alsatian Pinot Gris from clay soils"
    },
    service_specs={"temperature": "12-14C", "food": "foie gras, game, truffle risotto"},
    flavour_markers=["smoked bacon", "truffle", "brioche", "golden apple", "hazelnut", "spice"],
    flavour_weight="full",
    flavour_profile_type="rich aromatic",
    price_tier="premium",
    price_range_cad="$90-$160",
    technical_specs={
        "grape": "Pinot Gris",
        "appellation": "Alsace Grand Cru Hengst",
        "soil": "clay-marl"
    })

schlossberg_riesling = PROD(cur, "Domaine Weinbach Riesling Schlossberg Grand Cru Sainte Catherine",
    category="wine_still", producer_id=weinbach, region_id=ALSACE,
    subcategory="white",
    description=(
        "Schlossberg is Alsace's first classified Grand Cru and Weinbach's greatest Riesling. "
        "Grown on steep blue granite soils directly above the estate, it produces the most "
        "aristocratic and perfumed dry Riesling in Alsace. The Sainte Catherine bottling "
        "represents the top selection from old-vine parcels. Bone dry, with extraordinary "
        "finesse and a mineral purity that distinguishes granite from limestone terroirs."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Grand Cru Schlossberg — granite terroir benchmark",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "granite mineral, white peach, grapefruit flower, verbena, violet, crushed stone",
        "palate": "extremely fine, laser-focused, electric acidity, long mineral finish",
        "signature": "granite liftedness — aromatic precision distinct from limestone weight"
    },
    service_specs={"temperature": "11-12C", "aging": "8-20 years"},
    flavour_markers=["granite mineral", "white peach", "grapefruit flower", "verbena", "crushed stone"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$130-$220",
    technical_specs={
        "grape": "Riesling",
        "appellation": "Alsace Grand Cru Schlossberg",
        "soil": "blue granite"
    })

hugel_jubilee = PROD(cur, "Hugel Riesling Jubilee",
    category="wine_still", producer_id=hugel, region_id=ALSACE,
    subcategory="white",
    description=(
        "Jubilee is Hugel's estate flagship — old-vine Riesling from parcels in Schoenenbourg "
        "and Sporen Grand Crus in Riquewihr. The house style is dry and food-friendly, with "
        "a linear mineral precision that rewards 8-15 years of aging. A reference for "
        "accessible-tier Grand Cru quality in Alsatian Riesling."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "tier": "Grand Cru parcel blend (Schoenenbourg + Sporen)",
        "aging_potential": "8-15 years"
    }],
    deductive_profile={
        "nose": "lime, slate, white nectarine, hint of petrol (with age)",
        "palate": "dry, linear, firm acidity, mineral, moderate length",
        "signature": "Hugel house style — drier and more austere than many Alsatian Rieslings"
    },
    service_specs={"temperature": "10-12C", "aging": "5-15 years"},
    flavour_markers=["lime", "slate", "white nectarine", "petrol hint", "mineral"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$75-$130",
    technical_specs={
        "grape": "Riesling",
        "appellation": "Alsace (Grand Cru parcels)",
        "rs": "under 8g/L"
    })

hugel_vt_riesling = PROD(cur, "Hugel Riesling Vendange Tardive",
    category="wine_dessert", producer_id=hugel, region_id=ALSACE,
    subcategory="late_harvest",
    description=(
        "Hugel's Vendange Tardive Riesling is a benchmark for Alsatian late-harvest wines. "
        "Made from overripe, sometimes botrytised Riesling grapes, it delivers extraordinary "
        "concentration and sweetness balanced by Riesling's crystalline acidity. "
        "Hugel was instrumental in defining VT regulations in 1976; their VT remains the "
        "reference expression. Can age 20-40 years."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "classification": "Vendange Tardive — legally defined minimum ripeness",
        "aging_potential": "20-40 years",
        "botrytis": "sometimes present, not required"
    }],
    deductive_profile={
        "nose": "honey, botrytis spice, apricot jam, orange marmalade, petrol, ginger",
        "palate": "luscious but balanced acidity, long honeyed mineral finish",
        "signature": "VT sweetness balanced by Riesling's electric acidity — never cloying"
    },
    service_specs={
        "temperature": "8-10C",
        "glassware": "dessert wine glass",
        "food": "foie gras, strong cheese, fruit tarts, alone"
    },
    flavour_markers=["honey", "apricot jam", "orange marmalade", "petrol", "ginger", "botrytis spice"],
    flavour_weight="full",
    flavour_profile_type="sweet mineral",
    price_tier="ultra_premium",
    price_range_cad="$150-$350",
    technical_specs={
        "grape": "Riesling",
        "style": "Vendange Tardive (VT)",
        "rs": "typically 60-120g/L"
    })

trimbach_gewurz = PROD(cur, "Trimbach Gewurztraminer Seigneurs de Ribeaupierre",
    category="wine_still", producer_id=trimbach, region_id=ALSACE,
    subcategory="white",
    description=(
        "The Trimbach house style for Gewurztraminer follows the same philosophy as their "
        "Riesling: dry, precise, and food-driven rather than cloying and sweet. "
        "Seigneurs de Ribeaupierre represents old-vine parcels from Ribeauville and is "
        "notable for being genuinely dry (under 10g RS) — rare in Gewurztraminer. "
        "Rose petal, lychee, and spice without the heaviness typical of the variety."
    ),
    quality_tier="estate",
    quality_hierarchy=[{"tier": "Estate flagship Gewurztraminer", "aging_potential": "8-12 years"}],
    deductive_profile={
        "nose": "rose petal, lychee, ginger, allspice, smoke, white pepper",
        "palate": "dry entry, oily texture, spice complexity, firm finish",
        "signature": "Trimbach dry style — spice without sweetness; food-first Gewurz"
    },
    service_specs={"temperature": "10-12C", "food": "Munster cheese, foie gras, Alsatian choucroute"},
    flavour_markers=["rose petal", "lychee", "ginger", "allspice", "smoke", "white pepper"],
    flavour_weight="medium-full",
    flavour_profile_type="aromatic spiced",
    price_tier="premium",
    price_range_cad="$80-$130",
    technical_specs={
        "grape": "Gewurztraminer",
        "appellation": "Alsace",
        "rs": "under 10g/L"
    })

muenchberg_riesling = PROD(cur, "Domaine Ostertag Riesling Muenchberg Grand Cru",
    category="wine_still", producer_id=ostertag, region_id=ALSACE,
    subcategory="white",
    description=(
        "Muenchberg is Alsace's most distinctive Grand Cru — Triassic volcanic sandstone "
        "soil that produces Riesling unlike any other site in the region: smoky, spicy, "
        "deeply mineral, with a pronounced 'stoniness' and volcanic character. "
        "Ostertag's biodynamic Muenchberg is the benchmark for this terroir. "
        "Bones dry, with enormous aging potential and a distinctive smoky-mineral signature."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Grand Cru Muenchberg — volcanic sandstone monopoly on character",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "volcanic smoke, stone, lime pith, petrol, white flower, struck flint",
        "palate": "bone dry, angular, volcanic mineral extract, electric acidity",
        "signature": "volcanic sandstone smokiness — unique soil signature among Alsace Grand Crus"
    },
    service_specs={"temperature": "12-13C", "aging": "10-25 years"},
    flavour_markers=["volcanic smoke", "stone", "lime pith", "petrol", "struck flint"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$120-$200",
    technical_specs={
        "grape": "Riesling",
        "appellation": "Alsace Grand Cru Muenchberg",
        "soil": "Triassic volcanic sandstone"
    })

deiss_bergheim = PROD(cur, "Marcel Deiss Bergheim",
    category="wine_still", producer_id=deiss, region_id=ALSACE,
    subcategory="white",
    description=(
        "Bergheim is Deiss's most accessible terroir wine — a field blend of Riesling, "
        "Gewurztraminer, and Pinot Gris co-planted and co-fermented on limestone-clay soils. "
        "The wine expresses place over variety: the soil's warmth and richness come through "
        "regardless of which grape variety dominates in a given vintage. "
        "It represents Deiss's philosophy that Alsace wines should speak of terroir first."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "tier": "Lieu-dit field blend",
        "philosophy": "terroir over variety — field blend multiple varieties"
    }],
    deductive_profile={
        "nose": "complex, multi-varietal: rose, lychee, lime, chalk, almond, wildflowers",
        "palate": "textured, off-dry, warm limestone richness, long spice finish",
        "signature": "the complexity of a field blend — no single variety dominates"
    },
    service_specs={"temperature": "11-13C", "food": "Munster, smoked fish, mild spice"},
    flavour_markers=["rose", "lychee", "lime", "chalk", "almond", "wildflower"],
    flavour_weight="medium-full",
    flavour_profile_type="aromatic spiced",
    price_tier="premium",
    price_range_cad="$75-$130",
    technical_specs={
        "grape": "field blend — Riesling, Gewurztraminer, Pinot Gris",
        "appellation": "Alsace",
        "soil": "limestone-clay"
    })

print("\n=== ALSACE REFERENCES ===")

ref_alsace_gc = REF(cur,
    "Alsace Grand Cru — Soil Types, Variety Mapping, and Terroir Hierarchy",
    category="wine_regions", skill_level="advanced",
    description=(
        "Alsace Grand Cru covers 51 officially delimited sites, but quality is highly variable. "
        "Understanding the key soil types — granite, volcanic sandstone, limestone-marl, "
        "muschelkalk — and which varieties each favours is essential for intelligent Alsace navigation."
    ),
    key_principles=(
        "THE FOUR NOBLE VARIETIES and their soil affinities: "
        "RIESLING: The aristocrat of Alsace. Thrives on granite (Schlossberg, Brand) producing "
        "perfumed, lifted wines; limestone-marl (Rosacker, Geisberg) for more structured mineral; "
        "volcanic sandstone (Muenchberg) for smoky, spicy character. "
        "GEWURZTRAMINER: Prefers heavy clay-marl (Hengst, Goldert, Mambourg) — the warmth and "
        "richness of the soil amplifies its natural opulence. Terroir matters less than for Riesling. "
        "PINOT GRIS: Also clay-marl (Rangen de Thann, Hengst, Brand) — rich, smoky, truffle-inflected. "
        "Not Pinot Grigio; a fundamentally different wine of enormous power. "
        "MUSCAT: Goldert GC (clay-limestone) is the classic site — Muscat d'Alsace retains the "
        "extraordinary floral perfume of fresh grape. Very dry. Rare and declining. "
        "\nKEY GRAND CRUS: "
        "Schlossberg (Kaysersberg) — granite, Riesling benchmark "
        "Rosacker (Hunawihr) — limestone, Riesling — Clos Sainte Hune inside "
        "Brand (Turckheim) — granite, Riesling and Pinot Gris "
        "Hengst (Wintzenheim) — clay-marl, Gewurztraminer and Pinot Gris "
        "Rangen de Thann (Thann) — volcanic (schist/lava), steepest GC, warmest; Zind-Humbrecht monopole "
        "Muenchberg (Nothalten) — volcanic sandstone, smoky Riesling — Ostertag flagship "
        "\nVT AND SGN: "
        "Vendange Tardive (VT) — late harvest, overripe, sometimes botrytised; luscious but balanced "
        "Selection de Grains Nobles (SGN) — botrytised only; equivalent to Beerenauslese; exceptional "
        "Both legally defined by minimum ripeness levels (Hugel codified 1976). "
        "\nSERVICE NOTE: Most Alsatian whites have some residual sugar. The key is balance — "
        "Alsatian acidity keeps wines tasting dry even with 15-20g RS. "
        "Ask RS level before assuming style."
    ),
    common_mistakes=(
        "Treating all 51 Grand Crus as equal — quality ranges from excellent to mediocre. "
        "Assuming all Gewurztraminer is sweet — the best are genuinely dry. "
        "Under-estimating Alsatian Riesling aging potential (20-40 years for top wines). "
        "Confusing the 'petrol' note of aged Riesling as a fault — it is a mark of quality."
    ),
    pro_tips=(
        "For blind tasting: Alsatian Riesling = more weight and body than Mosel; "
        "more petrol/spice than German Trocken; minerally similar to Chablis but spicier. "
        "If you smell rose petal + lychee = Gewurztraminer; if smoked bacon + truffle = Pinot Gris. "
        "The 'petrol' note is TDN (trimethyl-dihydronaphthalene) — a Riesling-specific aroma "
        "compound that develops with age. It signals quality, not a fault."
    ),
    authority_tier=1,
    source_text="WSET Diploma Unit 3; CMS Advanced Sommelier; Kermit Lynch 'Adventures on the Wine Route'"
)

ref_vt_sgn = REF(cur,
    "Alsace Vendange Tardive and Selection de Grains Nobles — Style and Service Guide",
    category="wine_knowledge", skill_level="advanced",
    description=(
        "VT (Vendange Tardive) and SGN (Selection de Grains Nobles) are Alsace's legally defined "
        "late-harvest and botrytised categories. Understanding the regulatory framework, style "
        "differences, and food pairing logic is essential for confident service."
    ),
    key_principles=(
        "REGULATORY FRAMEWORK (Hugel codified 1976): "
        "VT: Minimum must weight (potential alcohol): Riesling/Muscat 95 Oechsle; Pinot Gris/Gewurz 105 Oechsle. "
        "No chaptalization permitted. Botrytis may or may not be present. "
        "SGN: Higher minimums (120/130 Oechsle). Botrytis (noble rot) is required. "
        "Equivalent to German Beerenauslese in richness. Very rare; exceptional vintages only. "
        "\nSTYLE SPECTRUM: "
        "VT Riesling: off-dry to luscious; extraordinary acidity keeps it fresh; ages 20-40 years. "
        "VT Gewurztraminer: opulent rose-lychee-ginger; rich without being cloying. "
        "VT Pinot Gris: truffle-honey richness; pairs with foie gras. "
        "SGN: all varieties produce profoundly rich, botrytised wines; serve in tiny pours. "
        "\nSERVICE: VT — 8-10C; dessert wine glass; works with foie gras, cheese, light fruit desserts. "
        "SGN — 6-8C; small pour (50ml); works alone or with Roquefort. "
        "\nAGING: VT (great vintages): 20-40 years. SGN: 30-50+ years. "
        "Both improve dramatically with 10-15 years minimum."
    ),
    common_mistakes=(
        "Serving VT too sweet — many VT Rieslings are only off-dry, not fully sweet. "
        "Pairing SGN with multi-course meal — too rich; serve alone or with cheese at end. "
        "Under-pricing VT/SGN — these are among France's rarest and most expensive wines."
    ),
    pro_tips=(
        "VT Riesling is one of the world's most under-appreciated food wines — "
        "off-dry with extraordinary acidity makes it incredibly versatile. "
        "SGN Gewurztraminer is one of the world's great sweet wines — floral intensity "
        "at botrytis concentration is extraordinary."
    ),
    authority_tier=1,
    source_text="Hugel estate literature; WSET Diploma; Cave de Ribeauville documentation"
)

print("\n=== ALSACE PAIRINGS ===")

PAIR(cur, "Choucroute garnie with pork knuckle, sausage, and juniper berries",
     "charcuterie_cured", "main",
     "classic", "complement",
     "The ultimate Alsatian terroir pairing — choucroute garnie (fermented cabbage with cured pork) "
     "is the region's emblematic dish. Clos Sainte Hune's dry mineral precision cuts through "
     "the richness; acidity matches the fermented tang; Riesling's apple-citrus freshness "
     "lifts the dish. One of France's great food-wine correspondences.",
     clos_sainte_hune, food_flavour_profile="fermented, pork fat, sour, juniper, rich", beverage_category="wine_still")

PAIR(cur, "Munster cheese with cumin seeds on pumpernickel",
     "dairy_fermented", "cheese",
     "classic", "complement",
     "Munster (the pungent washed-rind cheese of Alsace) and Gewurztraminer is one of France's "
     "most famous cheese-wine pairings. The wine's rose-lychee aromatics and off-dry richness "
     "counter the cheese's barnyard intensity; the cumin seeds mirror the spice in the wine.",
     trimbach_gewurz, food_flavour_profile="pungent, barnyard, creamy, cumin", beverage_category="wine_still")

PAIR(cur, "Foie gras terrine with Sauternes gelée and black pepper tuile",
     "charcuterie_cured", "starter",
     "classic", "complement",
     "Pinot Gris Hengst's smoked-truffle richness, residual sugar, and full body perfectly match "
     "foie gras. The Alsatian tradition of Pinot Gris with foie gras predates the Sauternes pairing "
     "and is arguably more elegant — the wine's spice cuts the fat more cleanly.",
     hengst_pinot_gris, food_flavour_profile="rich, fatty, truffle, black pepper", beverage_category="wine_still")

PAIR(cur, "Trout almondine meuniere with brown butter and capers",
     "seafood_general", "fish_course",
     "classic", "complement",
     "The classic Alsatian river fish pairing. Schlossberg Sainte Catherine's granite mineral "
     "and citrus freshness mirrors the delicacy of fresh trout; the wine's finesse matches "
     "the dish's lightness while the minerality adds dimension.",
     schlossberg_riesling, food_flavour_profile="delicate fish, brown butter, almond, caper", beverage_category="wine_still")

PAIR(cur, "Tarte flambee (Flammekueche) with creme fraiche and lardons",
     "dairy_fermented", "casual",
     "classic", "complement",
     "Alsace's version of pizza — a thin-crust tart with cream, onion, and bacon. "
     "Hugel Jubilee Riesling's dry precision and acidity cuts through the cream; "
     "the wine's mineral freshness provides counterpoint to the savoury richness.",
     hugel_jubilee, food_flavour_profile="cream, bacon, onion, char", beverage_category="wine_still")

PAIR(cur, "Foie gras mi-cuit with Hugel VT Riesling gelée and gingerbread",
     "charcuterie_cured", "starter",
     "classic", "complement",
     "The classic late-harvest Riesling and foie gras pairing. Hugel VT's luscious sweetness "
     "balanced by Riesling acidity matches foie gras perfectly — the gingerbread mirrors "
     "the wine's honey-spice notes.",
     hugel_vt_riesling, food_flavour_profile="rich, fatty, honey, gingerbread spice", beverage_category="wine_still")

PAIR(cur, "Smoked eel with potato-horseradish cream and chives",
     "seafood_general", "starter",
     "established", "complement",
     "Ostertag Muenchberg's volcanic-smoky mineral character and bone-dry precision "
     "creates a profound resonance with smoked eel — smoke meets smoke. "
     "The wine's angular acidity cuts through the potato cream; horseradish mirrors the wine's spice.",
     muenchberg_riesling, food_flavour_profile="smoky, oily fish, horseradish, cream", beverage_category="wine_still")

print("\n✅ Alsace batch complete.")
cur.close()
conn.close()
