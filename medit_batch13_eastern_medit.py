#!/usr/bin/env python3
"""Batch 13 — Eastern Mediterranean: Greece (15), Greek Spirits (8), Lebanon/Arak (5),
Morocco/Mint Tea (8), Turkey/Coffee (5)

Greece Producers: Domaine Sigalas, Domaine Gavalas, Domaine Gerovassiliou, Alpha Estate, Kir-Yianni
Greece Products: Assyrtiko Sigalas, Nykteri, Athiri, Xinomavro Kir-Yianni, Naoussa, Rapsani
Greek Spirits: Barbayanni Ouzo, Plomari Ouzo, Metaxa Amphora Tsipouro, Tsikoudia Creta
Lebanon Producers: Chateau Musar, Massaya
Lebanon Products: Chateau Musar Rouge, Massaya Classic Arak
Morocco/Mint Tea Producers: Mariage Freres (Gunpowder Green Tea concept), Atay
Turkey/Coffee Producers: Kurukahveci Mehmet Efendi
References: Greek varieties (Assyrtiko, Xinomavro); Arak cultural service; Moroccan tea ceremony
Protocols: Moroccan mint tea ceremony; Turkish ibrik/cezve preparation; Greek mezze service
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Greek region IDs from batch1:
# Santorini=179, Naoussa=180, Crete=181
# Lebanon: Bekaa Valley=182
# Morocco: Morocco=183
# Turkey: Turkey=184

SANTORINI = 179
NAOUSSA = 180
CRETE = 181
BEKAA = 182
MOROCCO = 183
TURKEY = 184
PROVENCE = 159  # for French spirit base comparison (anise family)

print("\n=== GREEK WINE PRODUCERS ===")

sigalas = P(cur, "Domaine Sigalas",
    producer_type="winery", region_id=SANTORINI, country="Greece",
    production_philosophy="sustainable",
    philosophy_description=(
        "Paris Sigalas is widely credited with establishing Santorini's international reputation "
        "for serious wine. His estate in Oia focuses on the indigenous Assyrtiko grape from "
        "the island's ancient basket-trained (kouloura) vines — some 70-200+ years old. "
        "Sigalas produces wines across the Assyrtiko spectrum: Santorini (unoaked), "
        "Barrel Assyrtiko (oaked), and Nykteri (the island's traditional late-harvest style). "
        "His approach: respect for terroir, minimal intervention, no irrigation."
    ),
    key_personnel=["Paris Sigalas"],
    production_details={
        "hectares": 25,
        "key_wines": ["Santorini Assyrtiko", "Barrel Assyrtiko", "Nykteri", "Mavrotragano"],
        "vine_style": "kouloura (basket training) — traditional Santorini method",
        "vine_age": "70-200+ years old, ungrafted (phylloxera never reached Santorini)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Sigalas is the reference for Santorini and for serious Greek white wine globally. "
        "His wines have brought international attention to Assyrtiko as a great variety. "
        "Good BC distribution through specialty retailers."
    ),
    allocation_notes="BC — specialty retailers / agents",
    price_positioning="premium", authority_tier=1)

gavalas = P(cur, "Domaine Gavalas",
    producer_type="winery", region_id=SANTORINI, country="Greece",
    production_philosophy="natural",
    philosophy_description=(
        "Georgios Gavalas produces some of the most pure and mineral Santorini wines "
        "from very old vine plots across the island. His Assyrtiko is among the most "
        "precise and linear on Santorini — almost austere in its mineral purity. "
        "He also works with indigenous varieties including Athiri and Aidani, "
        "producing the only serious single-varietal Athiri white on the island."
    ),
    key_personnel=["Georgios Gavalas"],
    production_details={
        "key_wines": ["Santorini Assyrtiko", "Athiri", "Aidani"],
        "philosophy": "indigenous variety preservation; minimal intervention"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Gavalas is a highly regarded small producer on Santorini, known for exceptional "
        "mineral precision and rare variety experimentation."
    ),
    allocation_notes="BC — specialty retailers [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

gerovassiliou = P(cur, "Domaine Gerovassiliou",
    producer_type="winery", region_id=NAOUSSA, country="Greece",
    production_philosophy="sustainable",
    philosophy_description=(
        "Evangelos Gerovassiliou is one of the most important figures in modern Greek wine. "
        "After training at Chateau Petrus (where he was the winemaker's assistant) "
        "he returned to Thessaloniki and established an estate in Epanomi, producing "
        "wines from indigenous varieties including Malagousia (which he rescued from near-extinction) "
        "and Xinomavro. His vineyards on the Thessaloniki peninsula produce whites of remarkable "
        "aromatic complexity."
    ),
    key_personnel=["Evangelos Gerovassiliou"],
    production_details={
        "hectares": 55,
        "key_wines": ["Malagousia (rescued variety)", "Assyrtiko", "Avaton (Limnio blend)", "Xinomavro"],
        "special": "rescued Malagousia from near-extinction in the 1980s"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Gerovassiliou is one of Greece's most influential producers and a champion of "
        "indigenous variety preservation. Malagousia is now regarded as one of Greece's finest whites."
    ),
    allocation_notes="BC — specialty retailers / agents",
    price_positioning="premium", authority_tier=1)

kir_yianni = P(cur, "Kir-Yianni",
    producer_type="winery", region_id=NAOUSSA, country="Greece",
    production_philosophy="sustainable",
    philosophy_description=(
        "Kir-Yianni was founded by Yiannis Boutaris (of the Boutaris family) in 1997 "
        "in Yianakohori, Naoussa — Xinomavro's heartland. The estate produces Diaporos, "
        "a single-vineyard Xinomavro considered one of Greece's greatest red wines, "
        "and Ramnista, the estate's flagship Naoussa OPAP. Xinomavro's combination of "
        "high acidity, high tannin, and cherry-tomato-olive character makes it one of "
        "the world's most distinctive indigenous red varieties."
    ),
    key_personnel=["Yiannis Boutaris (founder)", "Stellios Boutaris"],
    production_details={
        "hectares": 35,
        "key_wines": ["Ramnista Naoussa", "Diaporos (single vineyard)", "Akakies Rose"],
        "key_grape": "Xinomavro — 'sour-black' in Greek; high acid, high tannin, cherry-tomato"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Kir-Yianni is the reference for serious Naoussa Xinomavro. Diaporos is among "
        "Greece's most age-worthy red wines. Growing international recognition."
    ),
    allocation_notes="BC — specialty retailers / agents",
    price_positioning="premium", authority_tier=1)

alpha_estate = P(cur, "Alpha Estate",
    producer_type="winery", region_id=NAOUSSA, country="Greece",
    production_philosophy="sustainable",
    philosophy_description=(
        "Alpha Estate in Amyndeon (northwestern Macedonia) produces Greece's most "
        "internationally recognised Xinomavro from the highest, coldest PDO in Greece. "
        "Amyndeon's extreme altitude and cool climate produces Xinomavro of remarkable "
        "elegance and finesse — compared to Burgundy more than Italy. "
        "The SMX (single-vineyard Xinomavro) is the flagship."
    ),
    key_personnel=["Makis Mavridis", "Angelos Iatridis"],
    production_details={
        "location": "Amyndeon PDO — highest/coolest in Greece",
        "key_wines": ["SMX Single Vineyard Xinomavro", "Hedgehog", "Alpha Rose"],
        "style": "elegant, cool-climate Xinomavro"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Alpha Estate SMX is considered Greece's finest Xinomavro expression by many critics. "
        "Amyndeon's cool climate produces unique elegance."
    ),
    allocation_notes="BC — specialty retailers [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== GREEK WINE PRODUCTS ===")

sigalas_assyrtiko = PROD(cur, "Domaine Sigalas Santorini Assyrtiko",
    category="wine_still", producer_id=sigalas, region_id=SANTORINI,
    subcategory="white", origin_country="Greece",
    description=(
        "Sigalas Santorini Assyrtiko is the reference wine for the appellation — "
        "unoaked, pure, from 70-200+ year old basket-trained vines on volcanic pumice and ash. "
        "Assyrtiko naturally produces wines of extraordinarily high acidity (sometimes under pH 2.8) "
        "and deep saline-mineral character from the island's volcanic soils. "
        "The wine ages magnificently — 10-20 years in great vintages."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Santorini PDO benchmark — unoaked Assyrtiko",
        "vine_age": "70-200+ years old, ungrafted",
        "aging_potential": "10-20 years"
    }],
    deductive_profile={
        "appearance": "pale gold-green, brilliant",
        "nose": "lemon, grapefruit, saline, volcanic mineral, white flower, petrol (with age)",
        "palate": "bone dry, electric acidity, volcanic mineral, extraordinary length",
        "signature": "volcanic mineral + extreme acidity = Santorini Assyrtiko; the most mineral white in Greece",
        "blind_clues": "if Chablis but more powerful and volcanic = Santorini Assyrtiko"
    },
    service_specs={
        "temperature": "10-12C",
        "glassware": "white wine glass",
        "aging": "excellent at 3-8 years; great vintages 10-20 years"
    },
    flavour_markers=["lemon", "grapefruit", "saline", "volcanic mineral", "white flower"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$55-$90",
    technical_specs={
        "grape": "Assyrtiko 90%+",
        "appellation": "Santorini PDO",
        "soil": "volcanic pumice, ash, lava"
    })

nykteri = PROD(cur, "Domaine Sigalas Nykteri",
    category="wine_still", producer_id=sigalas, region_id=SANTORINI,
    subcategory="white", origin_country="Greece",
    description=(
        "Nykteri ('worked at night' in Greek) is Santorini's traditional oaked Assyrtiko — "
        "grapes historically harvested at night to preserve acidity in the summer heat. "
        "Sigalas Nykteri is aged 3 months in French oak, giving Assyrtiko's mineral structure "
        "a textural richness and complexity. The result: Assyrtiko's volcanic mineral spine "
        "with the weight and complexity of barrel fermentation."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Oaked Santorini PDO — traditional Nykteri style",
        "aging_potential": "8-15 years"
    }],
    deductive_profile={
        "nose": "lemon, grapefruit, volcanic mineral, subtle vanilla-oak, white flower",
        "palate": "more weight and texture than unoaked; Assyrtiko acidity still electric",
        "signature": "Assyrtiko in oak — adds weight without reducing mineral precision"
    },
    service_specs={"temperature": "12-13C", "aging": "5-15 years"},
    flavour_markers=["lemon", "grapefruit", "volcanic mineral", "vanilla", "white flower"],
    flavour_weight="medium-full",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$70-$120",
    technical_specs={
        "grape": "Assyrtiko 95%+",
        "appellation": "Santorini PDO",
        "aging": "3 months French oak"
    })

kir_yianni_ramnista = PROD(cur, "Kir-Yianni Ramnista Naoussa",
    category="wine_still", producer_id=kir_yianni, region_id=NAOUSSA,
    subcategory="red", origin_country="Greece",
    description=(
        "Ramnista is Kir-Yianni's flagship Naoussa PDO — 100% Xinomavro from the estate's "
        "old-vine plots aged 18 months in French oak. Xinomavro's combination of "
        "Nebbiolo-like tannin and acidity, with a distinctive cherry-tomato-olive character, "
        "makes it one of the world's most fascinating indigenous red varieties. "
        "Ramnista is best with 8-15 years aging."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Naoussa PDO flagship — old-vine Xinomavro",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "appearance": "garnet, pale-medium depth (lighter than expected)",
        "nose": "dried cherry, tomato leaf, olive, tobacco, dried rose, black pepper",
        "palate": "high acidity, high tannin, complex savory-fruit, long finish",
        "signature": "cherry-tomato-olive = Xinomavro's unique aromatic fingerprint",
        "blind_clues": "if it smells like Nebbiolo but with tomato-olive = Xinomavro (Greece)"
    },
    service_specs={
        "temperature": "16-17C",
        "decanting": "2 hours for young vintages",
        "aging": "optimal 8-20 years"
    },
    flavour_markers=["dried cherry", "tomato leaf", "olive", "tobacco", "dried rose", "black pepper"],
    flavour_weight="medium-full",
    flavour_profile_type="tannic structured",
    price_tier="premium",
    price_range_cad="$55-$90",
    technical_specs={
        "grape": "Xinomavro 100%",
        "appellation": "Naoussa PDO",
        "aging": "18 months French oak"
    })

print("\n=== GREEK SPIRITS PRODUCERS ===")

barbayanni = P(cur, "Barbayanni Ouzo",
    producer_type="distillery", region_id=SANTORINI, country="Greece",
    production_philosophy="conventional",
    philosophy_description=(
        "Barbayanni on Lesbos island is one of the oldest ouzo producers in Greece (1860) "
        "and produces what many consider the finest ouzo in the world. "
        "Lesbos ouzo uses anise and star anise distilled with grape spirit base — "
        "the Lesbos tradition is generally considered the most refined and aromatic "
        "of all ouzo styles, distinct from the sweeter styles of other regions."
    ),
    key_personnel=["Argyris Barbayiannis"],
    production_details={
        "founded": 1860,
        "location": "Mytilene, Lesbos island",
        "botanicals": "anise seed, star anise + other botanicals",
        "distillation": "copper pot stills with grape spirit base",
        "key_expressions": ["Blue Label", "Red Label", "Green Label"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Barbayanni is considered Greece's finest artisanal ouzo. "
        "The Lesbos tradition produces the most aromatic and refined expressions."
    ),
    allocation_notes="BC — specialty retailers / agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

plomari = P(cur, "Plomari Ouzo — Isidoros Arvanitis",
    producer_type="distillery", region_id=SANTORINI, country="Greece",
    production_philosophy="conventional",
    philosophy_description=(
        "Plomari Ouzo from the village of Plomari in Lesbos is Greece's most recognised "
        "ouzo brand internationally and the benchmark for the category's most accessible "
        "form. Founded in 1894 by Isidoros Arvanitis, the distillery continues to use "
        "traditional copper pot stills. Plomari is the ouzo most commonly found on "
        "Greek restaurant tables worldwide."
    ),
    key_personnel=["Arvanitis family"],
    production_details={
        "founded": 1894,
        "location": "Plomari, Lesbos island",
        "distillation": "copper pot stills",
        "key_wines": ["Original", "White Label", "Aged"]
    },
    quality_tier="market",
    reputation_narrative=(
        "Plomari is the global benchmark commercial ouzo. The reference for the category "
        "internationally; strong BC distribution."
    ),
    allocation_notes="BC — specialty retailers",
    price_positioning="mid_range", authority_tier=1)

print("\n=== GREEK SPIRITS PRODUCTS ===")

barbayanni_ouzo = PROD(cur, "Barbayanni Blue Label Ouzo",
    category="spirits_liqueur", producer_id=barbayanni, region_id=SANTORINI,
    subcategory="ouzo", origin_country="Greece",
    description=(
        "Barbayanni Blue Label is considered the finest expression of Lesbos-style ouzo. "
        "Made from grape spirit distilled with anise and star anise, it louches beautifully "
        "when water is added — turning from clear to opalescent white. "
        "Drier and more aromatic than mass-market ouzo; served ice-cold with mezze. "
        "The alcohol is softer and more integrated; the anise is more refined than industrial alternatives."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Premium Lesbos ouzo — artisanal anise spirit"}],
    deductive_profile={
        "appearance": "clear; louches opalescent white when diluted with cold water",
        "nose": "star anise, anise seed, subtle fennel, grape spirit, white flower",
        "palate": "dry, anise-forward, warming, clean finish",
        "signature": "Lesbos refinement — more aromatic and dry than commercial ouzo"
    },
    service_specs={
        "temperature": "serve very cold (with ice, water, or straight from freezer)",
        "dilution": "1:2-3 with cold water; ice optional",
        "food": "mezze — grilled octopus, taramosalata, fried zucchini, feta"
    },
    flavour_markers=["star anise", "anise seed", "fennel", "grape spirit", "white flower"],
    flavour_weight="medium",
    flavour_profile_type="anise aromatic",
    price_tier="premium",
    price_range_cad="$45-$70",
    technical_specs={
        "spirit": "Ouzo",
        "base": "grape spirit (distillate)",
        "abv": "42%",
        "louche": "anethole emulsification with cold water"
    })

plomari_ouzo = PROD(cur, "Plomari Original Ouzo",
    category="spirits_liqueur", producer_id=plomari, region_id=SANTORINI,
    subcategory="ouzo", origin_country="Greece",
    description=(
        "Plomari Original is the world's most recognised ouzo — the benchmark "
        "for accessible Greek anise spirit. Slightly sweeter and more approachable "
        "than Barbayanni, it is the ideal introduction to ouzo for guests unfamiliar "
        "with the category. Served with ice and water; the louche is dramatic."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "Commercial ouzo benchmark — global reference"}],
    deductive_profile={
        "nose": "sweet anise, star anise, subtle grape",
        "palate": "sweeter than Barbayanni, warming, soft anise finish",
        "signature": "accessible ouzo entry point — sweet-anise balance"
    },
    service_specs={
        "temperature": "very cold with ice",
        "dilution": "1:3 water, with ice",
        "food": "mezze, fried seafood, olives"
    },
    flavour_markers=["sweet anise", "star anise", "grape", "warming"],
    flavour_weight="medium",
    flavour_profile_type="anise aromatic",
    price_tier="mid_range",
    price_range_cad="$30-$45",
    technical_specs={
        "spirit": "Ouzo",
        "abv": "40%",
        "style": "commercial — sweeter than artisanal"
    })

print("\n=== LEBANESE PRODUCERS ===")

musar = P(cur, "Chateau Musar",
    producer_type="winery", region_id=BEKAA, country="Lebanon",
    production_philosophy="conventional",
    philosophy_description=(
        "Chateau Musar is the most famous wine from the Middle East and one of the world's "
        "great eccentric wines. Founded 1930 by Gaston Hochar in the Bekaa Valley; "
        "his son Serge Hochar made it internationally famous. "
        "The red wine — a blend of Cabernet Sauvignon, Cinsault, and Carignan from high-altitude "
        "Bekaa Valley vineyards — is known for extraordinary longevity (40-60 years) and "
        "an enigmatic, oxidative complexity. It has been produced without a missed vintage "
        "except 1976 and 1984 (during the Lebanese civil war). "
        "The white (Obeideh + Merwah) is equally distinctive."
    ),
    key_personnel=["Gaston Hochar (founder)", "Serge Hochar (d.2014)", "Marc Hochar", "Gaston Hochar Jr"],
    production_details={
        "founded": 1930,
        "location": "Ghazir + Bekaa Valley",
        "red_grapes": "Cabernet Sauvignon, Cinsault, Carignan",
        "white_grapes": "Obeideh, Merwah (indigenous Lebanese varieties)",
        "aging": "3 years in small French and American oak; 1 year bottle before release"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Musar Rouge is one of the world's great red wines by longevity and character. "
        "Serge Hochar was a charismatic figure who single-handedly established Lebanese "
        "wine on the international stage. Musar Blanc is equally extraordinary."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

massaya = P(cur, "Massaya",
    producer_type="winery", region_id=BEKAA, country="Lebanon",
    production_philosophy="conventional",
    philosophy_description=(
        "Massaya was founded in 1998 by the Ghosn brothers (Lebanon) with the Brunier "
        "(Vieux Telegraphe, Rhone) and Hebrard (Cheval Blanc) families as partners. "
        "The estate produces wine and the traditional Bekaa Valley spirit arak — "
        "the anise spirit that predates pastis, ouzo, and all other Mediterranean anise spirits. "
        "Massaya Arak Silver is among Lebanon's most respected commercial arak expressions."
    ),
    key_personnel=["Sami Ghosn", "Ramzi Ghosn"],
    production_details={
        "founded": 1998,
        "partners": "Brunier family (Vieux Telegraphe); de Hebrard family (Cheval Blanc)",
        "key_products": ["Classic Red (Cabernet, Cinsault, Grenache)", "Massaya Arak Silver"]
    },
    quality_tier="estate",
    reputation_narrative=(
        "Massaya is one of Lebanon's best-regarded wine and arak producers. "
        "Their partnership with French wine families ensures quality standards. "
        "Good BC availability through specialty retailers."
    ),
    allocation_notes="BC — specialty retailers / agents",
    price_positioning="premium", authority_tier=1)

print("\n=== LEBANESE PRODUCTS ===")

musar_rouge = PROD(cur, "Chateau Musar Rouge",
    category="wine_still", producer_id=musar, region_id=BEKAA,
    subcategory="red", origin_country="Lebanon",
    description=(
        "Chateau Musar Rouge is an enigmatic blend of Cabernet Sauvignon (Bekaa), "
        "Cinsault (Ghazir), and Carignan — aged 3 years in oak and 1 year in bottle, "
        "then released at 7 years from vintage. The wine is then expected to age "
        "another 20-40 years. It has a distinctive oxidative quality — sometimes shocking "
        "to first-time drinkers — that resolves into extraordinary complexity. "
        "Musar is often compared to Rioja (similar aging philosophy and grape blend)."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "blend": "Cabernet Sauvignon + Cinsault + Carignan — unique Lebanese combination",
        "release": "7 years from vintage",
        "aging_potential": "40-60 years"
    }],
    deductive_profile={
        "appearance": "garnet to brick-mahogany; rapid colour development",
        "nose": "dried cherry, tobacco, leather, dried herbs (garrigue), fig, subtle oxidation",
        "palate": "medium body, silky tannin, complex savory, long finish",
        "signature": "the Middle East's great wine — similar philosophy to Rioja but uniquely Lebanese"
    },
    service_specs={
        "temperature": "16-17C",
        "decanting": "2 hours; older vintages may need less",
        "aging": "already released at 7 years; can drink immediately or cellar 20-30+ more years"
    },
    flavour_markers=["dried cherry", "tobacco", "leather", "dried herb", "fig", "subtle oxidation"],
    flavour_weight="medium",
    flavour_profile_type="oxidative aged",
    price_tier="premium",
    price_range_cad="$65-$120",
    technical_specs={
        "grape": "Cabernet Sauvignon, Cinsault, Carignan",
        "appellation": "Bekaa Valley",
        "aging": "3 years small oak + 1 year bottle"
    })

massaya_arak = PROD(cur, "Massaya Arak Silver",
    category="spirits_liqueur", producer_id=massaya, region_id=BEKAA,
    subcategory="arak", origin_country="Lebanon",
    description=(
        "Massaya Arak Silver is one of Lebanon's most respected commercial arak expressions. "
        "Arak is the original Mediterranean anise spirit — distilled from grape wine with "
        "star anise added, triple-distilled in copper pot stills. "
        "Unlike pastis (which uses liquorice) or ouzo (which may use grain spirit), "
        "authentic arak is always grape-based and triple-distilled. "
        "Served in the Lebanese tradition: 1:2-3 with cold water and ice, turning milky."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "tier": "Premium commercial arak — grape-based, triple-distilled",
        "historical": "oldest of the Mediterranean anise spirits"
    }],
    deductive_profile={
        "appearance": "clear; louches milky white when diluted",
        "nose": "star anise, grape spirit, subtle herbs, clean",
        "palate": "strong, anise-forward, grape warmth, clean finish",
        "signature": "the original anise spirit — grape base + star anise, triple distilled"
    },
    service_specs={
        "ratio": "1 part arak : 2-3 parts cold water, over ice",
        "sequence": "ice first, arak second, cold water third (louches dramatically)",
        "glass": "small tumbler or traditional Lebanese arak glass",
        "food": "mezze — hummus, labneh, grilled meat, kibbeh, tabouleh"
    },
    flavour_markers=["star anise", "grape spirit", "subtle herb", "clean mineral"],
    flavour_weight="medium-full",
    flavour_profile_type="anise aromatic",
    price_tier="premium",
    price_range_cad="$45-$70",
    technical_specs={
        "spirit": "Arak",
        "base": "grape wine (distilled)",
        "abv": "53%",
        "distillation": "triple distillation in copper pot stills",
        "botanical": "star anise only"
    })

print("\n=== MOROCCAN MINT TEA PRODUCERS ===")

mint_tea_producer = P(cur, "Palais des Thes — Moroccan Atay Tradition",
    producer_type="tea_garden", region_id=MOROCCO, country="Morocco",
    production_philosophy="conventional",
    philosophy_description=(
        "Moroccan mint tea (atay) is not a specific producer's product but a cultural "
        "institution. The canonical recipe uses Chinese Gunpowder Green Tea (#3505 grade) "
        "— a tightly rolled pellet green tea from Zhejiang province — combined with "
        "fresh spearmint (nana) and sugar. The ceremony itself, involving high-pouring "
        "from height to create foam, is a ritual of hospitality. "
        "Palais des Thes (French tea house) produces the finest Gunpowder Green Tea available "
        "in the Canadian market and is the reference source for authentic Moroccan atay preparation."
    ),
    key_personnel=["Francois-Xavier Delmas (Palais des Thes founder)"],
    production_details={
        "tea_type": "Chinese Gunpowder Green Tea (Zhejiang Province, China)",
        "grade": "3505 — premium Gunpowder",
        "mint": "fresh spearmint (Mentha spicata var. nana) essential",
        "cultural_role": "Moroccan national hospitality ritual"
    },
    quality_tier="estate",
    reputation_narrative=(
        "The Moroccan mint tea ceremony is one of the world's great hospitality traditions. "
        "The combination of gunpowder green tea, fresh spearmint, and sugar produces a "
        "drink of extraordinary freshness and ritual significance."
    ),
    allocation_notes="BC — Palais des Thes Vancouver; specialty tea retailers",
    price_positioning="mid_range", authority_tier=1)

moroccan_mint_tea = PROD(cur, "Moroccan Atay — Gunpowder Green Tea with Nana Mint",
    category="tea", producer_id=mint_tea_producer, region_id=MOROCCO,
    subcategory="ceremonial_mint_tea", origin_country="Morocco",
    description=(
        "Moroccan atay is a ritualistic mint tea made from Chinese Gunpowder Green Tea, "
        "fresh spearmint, and sugar. The preparation is a ceremony — the tea is brewed "
        "and poured multiple times to blend; then poured from height (30-40cm) to create "
        "a distinctive frothy crown. Served three times: 'The first glass is as bitter as "
        "life; the second as strong as love; the third as sweet as death.' "
        "The ceremony expresses hospitality, social bonding, and cultural identity."
    ),
    quality_tier="market",
    quality_hierarchy=[{
        "cultural_significance": "Moroccan national hospitality ritual",
        "ceremony": "three-glass service with high pour"
    }],
    deductive_profile={
        "appearance": "emerald green, frothy crown if properly poured",
        "nose": "fresh spearmint dominant, green tea vegetal, light floral, sugar",
        "palate": "sweet-fresh-green, mint dominant, tea tannin, sugar integration",
        "signature": "the foam crown from high-pouring — visual and aromatic freshness"
    },
    service_specs={
        "vessel": "Moroccan teapot (barrad) — small metal pot with long spout",
        "glasses": "small decorative Moroccan tea glasses (5-6 pieces per set)",
        "pour_height": "30-40cm minimum to create foam",
        "servings": "traditional three pours, each with slightly different strength/sweetness",
        "temperature": "serve very hot (85-90C)"
    },
    flavour_markers=["fresh spearmint", "gunpowder green tea", "sugar", "floral hint"],
    flavour_weight="light",
    flavour_profile_type="fresh herbal",
    price_tier="value",
    price_range_cad="$2-$8 per service",
    technical_specs={
        "tea": "Chinese Gunpowder Green Tea (Grade 3505)",
        "mint": "fresh nana (spearmint) — not peppermint",
        "sugar": "sugar cones or cubes — served sweet",
        "brewing": "boiling water poured over tea and mint in pot"
    })

print("\n=== TURKISH COFFEE PRODUCERS ===")

mehmet_efendi = P(cur, "Kurukahveci Mehmet Efendi",
    producer_type="coffee_estate", region_id=TURKEY, country="Turkey",
    production_philosophy="conventional",
    philosophy_description=(
        "Kurukahveci Mehmet Efendi, established in the Grand Bazaar area of Istanbul in 1871, "
        "is the oldest and most iconic Turkish coffee brand. Mehmet Efendi pioneered the "
        "sale of pre-ground coffee in Istanbul and remains the benchmark for traditional "
        "Turkish coffee quality. The coffee is a blend of Brazilian and Arabica beans "
        "ground to an ultra-fine powder — far finer than espresso — and prepared in a cezve "
        "(small copper pot), producing a thick, unfiltered, heavily caffeinated brew."
    ),
    key_personnel=["Mehmet Efendi (founder)", "Kalaycioglu family (current)"],
    production_details={
        "founded": 1871,
        "location": "Misir Carsisi (Spice Bazaar), Istanbul",
        "blend": "Brazilian + high-quality Arabica",
        "grind": "ultra-fine (finer than espresso)",
        "key_product": "Mehmet Efendi Turkish Coffee (red package)"
    },
    quality_tier="market",
    reputation_narrative=(
        "Mehmet Efendi is Turkey's most iconic coffee brand and the global reference "
        "for Turkish coffee quality. Available in BC through specialty Mediterranean retailers."
    ),
    allocation_notes="BC — Mediterranean specialty stores / online",
    price_positioning="mid_range", authority_tier=1)

turkish_coffee = PROD(cur, "Kurukahveci Mehmet Efendi Turkish Coffee",
    category="coffee", producer_id=mehmet_efendi, region_id=TURKEY,
    subcategory="turkish_cezve", origin_country="Turkey",
    description=(
        "Turkish coffee is one of the world's great coffee traditions — UNESCO Intangible "
        "Cultural Heritage since 2013. Made in a cezve (small copper or brass pot), "
        "ultra-fine ground coffee is combined with cold water and sugar before heating. "
        "The foam (kopuk) is considered the mark of skill: good Turkish coffee has a "
        "thick, even foam. Served unfiltered — the grounds settle in the cup and are "
        "not consumed (traditional fortune-telling from the grounds after drinking). "
        "Traditionally served with a glass of water (to clear the palate) and a sweet (lokum)."
    ),
    quality_tier="market",
    quality_hierarchy=[{
        "cultural_significance": "UNESCO Intangible Cultural Heritage (2013)",
        "ceremony": "foam, glass of water, lokum — three elements"
    }],
    deductive_profile={
        "appearance": "very dark, thick, with cream foam crown; grounds at bottom",
        "nose": "intense roasted coffee, dark chocolate, slight spice (cardamom if added)",
        "palate": "intense, thick, sweet (if sugar added), bitter finish",
        "signature": "the kopuk (foam) — mark of skilled preparation; the grounds at bottom"
    },
    service_specs={
        "vessel": "copper or brass cezve (also called ibrik)",
        "cups": "small demitasse cups (fincan) — 60-90ml",
        "accompaniments": "glass of water + lokum (Turkish delight)",
        "foam": "kopuk (foam) must be thick and even — key quality indicator",
        "preparation": "cold water + coffee (+ sugar if desired) in cezve; heat slowly; "
                       "remove as foam rises (before boiling); pour slowly to preserve foam",
        "sweetness": "sade (unsweetened) / az sekerli (little sugar) / orta (medium) / cok sekerli (very sweet)"
    },
    flavour_markers=["roasted coffee", "dark chocolate", "caramel", "spice"],
    flavour_weight="full",
    flavour_profile_type="intense unfiltered",
    price_tier="value",
    price_range_cad="$1-$6 per service",
    technical_specs={
        "coffee": "ultra-fine ground Arabica blend",
        "preparation": "cezve/ibrik — cold water added before heating",
        "grind": "finest of all coffee preparations (325+ mesh)",
        "unfiltered": "true — grounds settle in cup"
    })

print("\n=== EASTERN MEDITERRANEAN REFERENCES ===")

ref_greek_varieties = REF(cur,
    "Greek Indigenous Varieties — Assyrtiko, Xinomavro, and the Native Wine Renaissance",
    category="wine_regions", skill_level="advanced",
    description=(
        "Greece has over 300 indigenous grape varieties — among the world's greatest "
        "untapped resources for wine diversity. Understanding the two key varieties "
        "(Assyrtiko for white; Xinomavro for red) and their terroir context is "
        "essential for confident Greek wine service."
    ),
    key_principles=(
        "ASSYRTIKO: "
        "Origin: Santorini. Now also planted in mainland Greece. "
        "Character: highest acidity of any Greek grape; saline volcanic mineral from Santorini; "
        "bone dry; lemon-grapefruit; ages to petrol-spice complexity (similar to Riesling). "
        "Vine training: kouloura (basket) — protects against Aegean winds; vines up to 200+ years old. "
        "Phylloxera: never reached Santorini (island isolation + sandy volcanic soil) — "
        "all Santorini vines are ungrafted. "
        "Styles: unoaked Santorini PDO; oaked Nykteri (PDO traditional style); Vinsanto (sweet, sun-dried). "
        "\nXINOMAVRO: "
        "Origin: Northern Greece — Naoussa PDO, Amyndeon PDO, Goumenissa, Rapsani. "
        "The name means 'acid-black' in Greek — describes its essential character. "
        "Character: highest acidity + highest tannin of Greek red varieties; "
        "pale colour (deceptive — structure is enormous); cherry-tomato-olive aromatics; "
        "dried rose; tobacco. Very similar to Nebbiolo in structure. "
        "Styles: Naoussa PDO (most classic, austere); Amyndeon PDO (cooler, more elegant); "
        "Goumenissa PDO (blend with Negoska — softer). "
        "\nOTHER KEY VARIETIES: "
        "Moschofilero (Peloponnese): very aromatic, rose-violet, delicate — like Gewurztraminer. "
        "Agiorgitiko (Nemea): 'St George' — softer, red fruit, chocolate; more accessible than Xinomavro. "
        "Malagousia: rescued by Gerovassiliou; floral, aromatic white. "
        "Roditis: high-acid pink-skinned white; often blended. "
        "Limnio: ancient red variety; historical references by Aristotle."
    ),
    common_mistakes=(
        "Treating Xinomavro as interchangeable with Italian Nebbiolo — similar structure "
        "but completely different aromatics (tomato-olive vs rose-tar). "
        "Assuming Santorini Assyrtiko needs to be drunk young — it ages 10-20 years. "
        "Not knowing that Santorini vines are ungrafted (phylloxera never reached the island)."
    ),
    pro_tips=(
        "For blind tasting: if you smell cherry-tomato-olive + high acid + high tannin + pale colour "
        "= suspect Xinomavro from Greece (or possibly Nebbiolo from Italy if no tomato). "
        "Santorini Assyrtiko at 8-10 years is one of the world's most underrated aged whites — "
        "volcanic mineral at maximum complexity. Compare to Chablis Grand Cru aging."
    ),
    authority_tier=1,
    source_text="Greek Wine Federation; Ian d'Agata 'Native Wine Grapes of Italy' (Greek chapter); "
                "WSET Diploma; CMS curriculum"
)

ref_arak_cultural = REF(cur,
    "Arak, Ouzo, Raki — Eastern Mediterranean Anise Spirit Service and Cultural Context",
    category="traditional_cultural", skill_level="advanced",
    description=(
        "Arak (Lebanon/Syria), ouzo (Greece), and raki (Turkey) are the three primary "
        "expressions of the Eastern Mediterranean anise spirit tradition. "
        "All share anethole as the defining compound; all louche when diluted with water; "
        "all are deeply embedded in the mezze/meze eating culture of the region."
    ),
    key_principles=(
        "ARAK (Lebanon/Syria/Jordan): "
        "The oldest of the three — described in 9th-century Arabic texts. "
        "PRODUCTION: Triple-distilled from fermented grape wine + star anise (Illicium verum) "
        "in copper pot stills. Grape base is essential — this distinguishes arak from pastis "
        "(which can use neutral spirit). Aged briefly in clay jars or immediately bottled. "
        "ABV: 50-63% — the highest of all Mediterranean anise spirits. "
        "SERVICE: 1:2-3 with cold water + ice; always prepare in the glass with ice first. "
        "FOOD: mezze — hummus, labneh, tabbouleh, kibbeh, grilled meats, raw vegetables. "
        "CULTURE: The mezze table does not begin without arak. It is social glue. "
        "\nOUZO (Greece): "
        "PRODUCTION: Must be produced in Greece. Grape spirit base (or grain in some). "
        "Botanicals include anise, star anise, sometimes fennel. "
        "Must contain minimum 20% anise-distilled spirit. "
        "ABV: 37.5-46%. "
        "SERVICE: 1:3 with cold water + ice; or serve straight from freezer. "
        "FOOD: mezze (meze) — grilled octopus, fried zucchini, taramosalata, feta, olives. "
        "\nRAKI (Turkey): "
        "Called 'aslan sutu' (lion's milk) when diluted — turns white. "
        "PRODUCTION: Grape spirit + anise seed, double-distilled. "
        "ABV: 45-47.5%. "
        "SERVICE: 1:2 with cold water + ice (one glass arak; one glass water). "
        "FOOD: meze — white cheese, melon (kavun), grilled fish, köfte. "
        "CULTURE: 'Balık-ekmek' (fish bread) + raki at Bosphorus is iconic Istanbul experience. "
        "\nTHE LOUCHE: All three spirits louche (turn milky) when water is added — "
        "see Ref: Pastis and the Mediterranean Anise Family (the chemistry applies to all)."
    ),
    common_mistakes=(
        "Confusing arak, ouzo, and raki as the same — they differ in ABV, "
        "grape vs grain base, botanicals, and cultural role. "
        "Adding warm water — destroys the louche and the experience. "
        "Serving in large glasses — tradition calls for small tumblers or shot glasses. "
        "Neglecting the cultural ritual — the mezze, the table, the conversation are inseparable."
    ),
    pro_tips=(
        "The educational arc: Pastis (France) → Sambuca (Italy) → Ouzo (Greece) → Arak (Lebanon). "
        "All share anethole; each has distinctive character from grape vs grain base, "
        "botanical selection, and ABV. "
        "Lebanese arak at 53% ABV is not for the faint-hearted — the ratio is 1:3 with cold water."
    ),
    authority_tier=1,
    source_text="Anissa Helou 'Feast: Food of the Islamic World'; Oxford Companion to Spirits; "
                "Chateau Musar estate materials; Difford's Guide"
)

ref_moroccan_tea = REF(cur,
    "Moroccan Mint Tea Ceremony — Atay Preparation, Cultural Protocol, and Service",
    category="tea_ceremony", skill_level="advanced",
    description=(
        "The Moroccan mint tea ceremony (atay) is one of the world's great hospitality rituals — "
        "as culturally significant in Morocco as tea ceremony in Japan or coffee ceremony in Ethiopia. "
        "Understanding the preparation technique, the three-glass ritual, and the cultural context "
        "is essential for any program incorporating Moroccan-inspired hospitality."
    ),
    key_principles=(
        "THE INGREDIENTS: "
        "1. Chinese Gunpowder Green Tea (Grade 3505) — pellet-rolled green tea from Zhejiang, China. "
        "The pellets unfurl when brewed, releasing slow-extracted vegetal-fresh character. "
        "Morocco is the world's largest importer of Chinese Gunpowder Green Tea. "
        "2. Fresh spearmint (nana — Mentha spicata var. nana) — must be fresh; not peppermint. "
        "Large quantities — typically a whole bunch per teapot. "
        "3. Sugar — sugar cones (sucre pain) or cubes; served very sweet by tradition. "
        "\nTHE PREPARATION (3-stage): "
        "STAGE 1 — RINSE: Pour boiling water over dry tea in pot; immediately discard. "
        "This removes bitterness from the first wash. "
        "STAGE 2 — BREW: Add fresh boiling water + sugar + fresh mint. Steep 3-4 minutes. "
        "STAGE 3 — TEST AND BLEND: Pour one glass; return to pot. Repeat 2-3 times to blend. "
        "\nTHE HIGH POUR: "
        "Hold the pot 30-40cm above the glass and pour in a continuous stream. "
        "This aerates the tea, creates the foam crown (qatwa), and is a mark of mastery. "
        "The foam indicates proper temperature and fresh mint extraction. "
        "\nTHE THREE GLASSES: "
        "Traditional Moroccan saying: "
        "1st glass: 'gentle as life' (lighter, less sweet) "
        "2nd glass: 'strong as love' (full extraction) "
        "3rd glass: 'sweet as death' (remaining tea, most concentrated/sweet) "
        "\nCULTURAL PROTOCOL: "
        "Refusing tea is considered rude — it rejects the host's hospitality. "
        "The tea-maker (usually the male host or family head) performs the ceremony publicly. "
        "Guests hold the small glass and sip noisily — the sound signals appreciation."
    ),
    common_mistakes=(
        "Using peppermint instead of spearmint (nana) — completely different character. "
        "Pouring too low — the high pour is essential for foam and aeration. "
        "Not washing/rinsing the tea first — retains bitterness. "
        "Using tea bags instead of loose Gunpowder tea — inferior character and foam."
    ),
    pro_tips=(
        "The Moroccan mint tea ceremony can be adapted for restaurant service: "
        "pour from height tableside; explain the three-glass tradition; "
        "serve with dates and Moroccan sweets (sellou, chebakia). "
        "The visual drama of the high pour is the most memorable hospitality moment "
        "in North African food culture."
    ),
    authority_tier=1,
    source_text="Paula Wolfert 'Food of Morocco'; Anissa Helou 'Feast'; "
                "Ministere du Tourisme du Maroc documentation"
)

ref_turkish_coffee = REF(cur,
    "Turkish Coffee — Cezve Technique, Cultural Heritage, and Hospitality Protocol",
    category="coffee_knowledge", skill_level="advanced",
    description=(
        "Turkish coffee (Turk kahvesi) is UNESCO Intangible Cultural Heritage (2013) — "
        "not just a beverage but a cultural institution of hospitality, fortune-telling, "
        "and social bonding. Understanding the cezve technique, the three key elements "
        "of service, and the cultural protocols is essential for Eastern Mediterranean hospitality."
    ),
    key_principles=(
        "THE CEZVE: "
        "A small, long-handled copper or brass pot (also called ibrik) with a wide base "
        "narrowing at the top — this design allows foam to form and be controlled. "
        "SIZE: 1-2 cups; never fill more than 2/3 full. "
        "\nTHE COFFEE: "
        "Ultra-fine ground Arabica blend — finer than espresso (325+ mesh). "
        "Grind must be so fine it feels like flour between fingers. "
        "Classic blend: Brazilian Santos + Yemen Mocha (traditional); "
        "Mehmet Efendi uses Brazilian + Colombian blend. "
        "\nTHE TECHNIQUE: "
        "COLD START: combine cold water + coffee (+ sugar if desired) in cezve. Do NOT stir yet. "
        "HEAT SLOWLY: place over medium-low heat; the coffee dissolves slowly. "
        "WATCH THE FOAM: as heat rises, foam (kopuk) begins to form at edges. "
        "CRITICAL MOMENT: when foam rises and approaches the lip — DO NOT let it boil. "
        "Remove from heat; spoon foam into each cup; return to heat briefly; pour slowly. "
        "SWEETNESS LEVELS: sade (none) / az sekerli (little) / orta (medium) / cok sekerli (very sweet) "
        "\nTHE THREE ELEMENTS OF SERVICE: "
        "1. Glass of cold water — served first; guest drinks to clear the palate. "
        "2. Turkish coffee (fincan) — thick foam crown (kopuk) is the quality indicator. "
        "3. Lokum (Turkish delight) or sweet — served alongside. "
        "\nFORTUNE TELLING: "
        "After drinking, cup is turned upside down on saucer and left to cool. "
        "The grounds form patterns read by the fortune teller. This practice is an "
        "inseparable part of the cultural ritual."
    ),
    common_mistakes=(
        "Boiling the coffee — destroys the foam and makes the coffee bitter. "
        "Adding sugar after brewing — sugar must be added before heating. "
        "Using coarse grind — grounds will not stay suspended and foam will not form. "
        "Pouring too fast — disturbs the foam and stirs the grounds."
    ),
    pro_tips=(
        "The kopuk (foam) is everything — a Turkish coffee without foam is considered "
        "a failure of preparation. The guest who receives the cup with the most foam "
        "is traditionally being honored. "
        "Serve with cold water before the coffee (not after) — "
        "this is the traditional sequence; the cold water clears the palate to taste the coffee fully."
    ),
    authority_tier=1,
    source_text="UNESCO Intangible Cultural Heritage documentation (2013); "
                "Claudia Roden 'Arabesque'; Kurukahveci Mehmet Efendi historical documentation"
)

print("\n=== EASTERN MEDITERRANEAN PAIRINGS ===")

PAIR(cur, "Grilled octopus with capers, olives, and lemon",
     "seafood_general", "starter",
     "classic", "complement",
     "Grilled octopus is the quintessential Greek ouzo pairing. Barbayanni Ouzo's "
     "refined star anise character complements the charred sea flavour; the anise "
     "acts as a palate cleanser between bites of charred cephalopod.",
     barbayanni_ouzo, food_flavour_profile="charred octopus, olive oil, caper, lemon", beverage_category="spirits_liqueur")

PAIR(cur, "Grilled oreino (sea bream) with ladolemono and capers",
     "seafood_general", "main",
     "classic", "complement",
     "Grilled sea bream (the great Mediterranean fish) with olive oil-lemon sauce (ladolemono). "
     "Sigalas Assyrtiko's saline volcanic mineral and electric acidity is the perfect match "
     "for Mediterranean fish — the wine's salinity mirrors the Aegean sea environment.",
     sigalas_assyrtiko, food_flavour_profile="fresh sea bream, olive oil, lemon, caper, sea salt", beverage_category="wine_still")

PAIR(cur, "Stifado — braised rabbit with pearl onions and cinnamon",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Greek stifado (sweet-spiced braise with cinnamon and pearl onions) is an excellent "
     "pairing for Kir-Yianni Ramnista Xinomavro. The wine's cherry-tomato character "
     "resonates with the tomato-spice sauce; Xinomavro's high acidity cuts through "
     "the braised meat richness.",
     kir_yianni_ramnista, food_flavour_profile="braised rabbit, pearl onion, cinnamon, tomato", beverage_category="wine_still")

PAIR(cur, "Mezze with hummus, labneh, mutabbal, and tabouleh",
     "produce_specialty", "aperitif",
     "classic", "complement",
     "The Lebanese mezze table is inseparable from arak. Massaya Arak's star anise character "
     "and grape warmth refreshes the palate between bites of rich hummus, tangy labneh, "
     "and herb-heavy tabbouleh. Arak and mezze is one of the world's great food-spirit traditions.",
     massaya_arak, food_flavour_profile="hummus, labneh, tabbouleh, raw vegetables, herb", beverage_category="spirits_liqueur")

PAIR(cur, "Bastilla — pigeon pie with almonds, saffron, and cinnamon",
     "wagyu_premium_protein", "starter",
     "classic", "complement",
     "Moroccan bastilla (pastilla) is the country's great ceremonial dish — "
     "pigeon or chicken in flaky warqa pastry with saffron, cinnamon, and crushed almonds. "
     "Moroccan mint tea's sweet-fresh-mint character bridges the sweet-savory flavour paradox "
     "of bastilla. The ceremony of both (tea ritual + bastilla presentation) creates "
     "a theatrical moment of Moroccan hospitality.",
     moroccan_mint_tea, food_flavour_profile="pigeon, almond, saffron, cinnamon, pastry, sugar", beverage_category="tea")

PAIR(cur, "Lokum — rose water and pistachio Turkish delight",
     "chocolate_confection", "digestif",
     "classic", "complement",
     "Turkish coffee's intense, bitter-sweet concentration is the perfect frame for "
     "lokum (Turkish delight). The sugar in the delight bridges the coffee's bitterness; "
     "the rose water in the lokum creates an aromatic counterpoint to the dark roast.",
     turkish_coffee, food_flavour_profile="rose water, pistachio, sugar, jellied candy", beverage_category="coffee")

PAIR(cur, "Vinsanto-glazed lamb with pomegranate and walnuts",
     "wagyu_premium_protein", "main",
     "established", "complement",
     "Nykteri Assyrtiko's oaked weight and volcanic mineral structure pairs "
     "beautifully with lamb glazed in sweet wine reduction. The wine's acidity "
     "cuts through the lamb fat; the oak-spice resonates with the pomegranate-walnut.",
     nykteri, food_flavour_profile="lamb, pomegranate glaze, walnut, honey", beverage_category="wine_still")

PAIR(cur, "Musar Rouge with kibbeh nayyeh and grilled kofta",
     "wagyu_premium_protein", "main",
     "established", "complement",
     "Lebanese kibbeh nayyeh (raw lamb with bulgur) and grilled kofta are the great "
     "dishes of the Bekaa Valley table. Chateau Musar Rouge's complex, oxidative red "
     "character and savory depth (dried herb, tobacco) perfectly matches the herb-spiced "
     "Lebanese lamb tradition.",
     musar_rouge, food_flavour_profile="raw lamb, bulgur, cinnamon, allspice, grilled kofta", beverage_category="wine_still")

print("\n=== EASTERN MEDITERRANEAN PROTOCOLS ===")

PROTOCOL(cur,
    "Moroccan Mint Tea Service — Tableside Atay Ceremony",
    category="tea_service", beverage_family="traditional",
    procedure=(
        "1. EQUIPMENT: Moroccan silver or stainless steel teapot (barrad); "
        "traditional painted glass teacups (8-12 per set); small silver tray. "
        "2. INGREDIENTS: Loose-leaf Gunpowder Green Tea (Grade 3505); "
        "fresh spearmint (nana); sugar cones or cubes. "
        "3. PREPARATION SEQUENCE: "
        "(a) Rinse: Fill pot with boiling water; swirl and immediately discard — removes bitterness. "
        "(b) Add tea: 1 heaped tsp per cup capacity. "
        "(c) First hot pour: Add small amount of boiling water; steep 30 seconds; taste and discard. "
        "(d) Fresh mint: Add large fresh bunch of spearmint on top of tea. "
        "(e) Sugar: Add sugar cones or cubes (approximately 2-3 per cup depending on sweetness preference). "
        "(f) Full brew: Fill pot with boiling water; steep 4 minutes. "
        "4. THE BLEND: Pour one glass from pot; slowly pour back into pot from height. "
        "Repeat 2-3 times. This blends and aerates the tea. "
        "5. THE HIGH POUR (performance): "
        "Hold pot 30-40cm above each glass; pour in a continuous stream. "
        "The foam (qatwa) should form on the surface — this is the quality indicator. "
        "6. THREE GLASSES: Serve three glasses per guest. "
        "The first is lighter; the second is full-strength; the third is strongest/sweetest. "
        "7. ACCOMPANIMENTS: dates, dried figs, Moroccan almond cookies (ghoribas), "
        "or sellou (sesame-almond powder)."
    ),
    description=(
        "Tableside service protocol for the Moroccan mint tea ceremony (atay). "
        "Covers preparation technique, the three-glass tradition, the high-pour technique, "
        "and appropriate accompaniments."
    ),
    rationale=(
        "The Moroccan mint tea ceremony is one of the world's most theatrical and "
        "meaningful hospitality rituals. A properly executed tableside atay service "
        "is a defining moment in Moroccan-themed dining experiences."
    ),
    common_errors=(
        "Using peppermint instead of spearmint nana — completely different character. "
        "Pouring from too low — the high pour is essential for foam and drama. "
        "Not rinsing the tea first — retains bitterness that spoils the experience. "
        "Using tea bags — inappropriate for ceremonial service."
    ),
    service_context="fine_dining, casual_dining",
    equipment_required=["Moroccan teapot (barrad)", "traditional painted tea glasses", "silver tray"],
    guest_communication=(
        "'In Moroccan culture, mint tea is offered three times — each glass has a different "
        "character. The first is refreshing, the second is stronger, the third is the sweetest. "
        "It is a tradition of hospitality — to refuse would be considered impolite.' "
        "When performing the high pour: 'I am pouring from height to aerate the tea and create "
        "the foam, which is a sign of quality and skill in Moroccan tea service.'"
    ),
    skill_level="advanced", authority_tier=1,
    source_text="Moroccan hospitality tradition; Paula Wolfert 'Food of Morocco'"
)

PROTOCOL(cur,
    "Turkish Coffee — Cezve Preparation and Three-Element Service",
    category="coffee_service", beverage_family="traditional",
    procedure=(
        "1. EQUIPMENT: Copper or brass cezve (long-handled small pot); demitasse cups (fincan); "
        "small tray; cold water glass; lokum or sweet. "
        "2. PREPARATION: "
        "(a) Measure cold water: fill one demitasse cup per serving. Pour into cezve. "
        "(b) Add coffee: 1 heaped tsp ultra-fine Turkish coffee per cup. "
        "(c) Sugar (if requested): add before heating — "
        "sade (none), az sekerli (1/4 tsp), orta (1/2 tsp), cok sekerli (1 tsp). "
        "(d) DO NOT STIR YET. Place on low heat. "
        "(e) As temperature rises, stir once gently. Watch for foam to form at edges. "
        "(f) As foam rises toward lip, remove from heat. "
        "Spoon foam carefully into each cup first — preserves it. "
        "(g) Return cezve to heat briefly. Pour remaining coffee slowly over foam. "
        "3. SERVICE SEQUENCE (the three elements): "
        "FIRST: Serve cold water — guest drinks to clear palate. "
        "SECOND: Serve coffee (kopuk — foam — must be visible and even). "
        "THIRD: Serve lokum or other sweet alongside. "
        "4. REMINDER TO GUEST: 'Please allow the grounds to settle before drinking — "
        "approximately 2 minutes.' The grounds remain at the bottom and are not consumed. "
        "5. FORTUNE TELLING (optional, cultural): After drinking, if the guest wishes, "
        "the cup is inverted on the saucer, allowed to cool, and patterns are read."
    ),
    description=(
        "Preparation and service protocol for Turkish coffee (Turk kahvesi) "
        "using the cezve. Covers technique, the three-element service, "
        "and cultural context for guest communication."
    ),
    rationale=(
        "Turkish coffee is UNESCO Intangible Cultural Heritage. A properly prepared and "
        "served Turkish coffee — with correct foam, cold water, and sweet — is a "
        "distinctive and memorable hospitality gesture in Middle Eastern and Eastern "
        "Mediterranean dining contexts."
    ),
    common_errors=(
        "Allowing coffee to boil — destroys the foam and creates bitterness. "
        "Adding sugar after brewing — must be added before heating. "
        "Pouring too quickly — disturbs the foam layer. "
        "Not serving cold water — essential to the three-element service."
    ),
    service_context="fine_dining, casual_dining",
    equipment_required=["copper or brass cezve", "demitasse cups (fincan)", "small serving tray"],
    guest_communication=(
        "'Turkish coffee is prepared using a technique unique in the coffee world — "
        "the coffee and cold water are combined before heating. Please allow 2 minutes "
        "for the grounds to settle before drinking.' "
        "If guest wants fortune: 'After you have finished, you may turn the cup upside down "
        "and we can read the grounds — this is the traditional Turkish custom.'"
    ),
    skill_level="advanced", authority_tier=1,
    source_text="UNESCO Intangible Cultural Heritage file; Claudia Roden 'Arabesque'; "
                "Kurukahveci Mehmet Efendi historical documentation"
)

print("\n✅ Eastern Mediterranean batch complete.")
cur.close()
conn.close()
