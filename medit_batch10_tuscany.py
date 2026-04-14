#!/usr/bin/env python3
"""Batch 10 — Italian Wine: Tuscany (25 targets)
Producers: Biondi-Santi, Sassicaia (Tenuta San Guido), Ornellaia, Antinori (Tignanello),
           Montevertine, Isole e Olena, Fontodi, Castello dei Rampolla, Bibi Graetz
Products: Biondi-Santi Brunello Riserva, Sassicaia, Ornellaia, Tignanello, Montevertine Le Pergole Torte,
          Fontodi Flaccianello, Isole e Olena Cepparello, Bibi Graetz Testamatta
References: Brunello di Montalcino vs Rosso; Super Tuscans and IGT; Sangiovese deductive
Pairings: bistecca Fiorentina, ribollita, cinghiale, pappardelle, pecorino
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Tuscany region IDs from batch1:
# Tuscany=165, Brunello di Montalcino=166, Chianti Classico=167,
# Bolgheri=168, Montalcino=169 (same as Brunello), Vernaccia=170

TUSCANY = 165
BRUNELLO = 166
CHIANTI = 167
BOLGHERI = 168
MONTALCINO = 169

print("\n=== TUSCANY PRODUCERS ===")

biondi_santi = P(cur, "Biondi-Santi",
    producer_type="winery", region_id=BRUNELLO, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Biondi-Santi invented Brunello di Montalcino. Ferruccio Biondi-Santi isolated a "
        "superior Sangiovese clone ('Brunello') in 1870 and created the first modern Brunello. "
        "The estate is in Il Greppo in the northern sector of Montalcino — the coolest "
        "sub-zone, producing wines of the most delicate and age-worthy character. "
        "The riserva, made only in exceptional years, is among Italy's most age-worthy wines "
        "(the 1955 and 1964 riserve are legendary). Now owned by EPI Group (France) since 2016; "
        "Giampiero Bertolini manages quality."
    ),
    key_personnel=["Ferruccio Biondi-Santi (founder, d.1917)", "Franco Biondi-Santi (d.2013)", "Jacopo Biondi-Santi (last family member)", "Giampiero Bertolini (CEO)"],
    production_details={
        "estate": "Il Greppo, northern Montalcino",
        "clone": "Brunello clone — selected by Ferruccio Biondi-Santi 1870",
        "key_wines": ["Brunello Riserva (exceptional years only)", "Brunello Annata", "Rosso di Montalcino"],
        "style": "traditional — large Slavonian oak"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Biondi-Santi is the most historic Brunello estate — the original. Riserva is among "
        "Italy's most collectible wines. Even annata requires 15-20 years to peak. "
        "The 1888 and 1891 Riserve were still alive in the 1990s tastings."
    ),
    allocation_notes="BC — Select Wine Merchants [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

tenuta_san_guido = P(cur, "Tenuta San Guido",
    producer_type="winery", region_id=BOLGHERI, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Tenuta San Guido created the 'Super Tuscan' category with Sassicaia — a Cabernet "
        "Sauvignon-based wine made outside DOC rules on the Tyrrhenian coast of Tuscany. "
        "Marchese Mario Incisa della Rocchetta planted Cabernet Sauvignon in 1944 on gravel "
        "soils similar to Pauillac. Sassicaia went commercial in 1968 and in 1994 became the "
        "only single-estate DOC in Italy (Bolgheri Sassicaia DOC). "
        "Giacomo Tachis was the legendary consultant winemaker."
    ),
    key_personnel=["Marchese Mario Incisa della Rocchetta (founder)", "Priscilla Incisa della Rocchetta (current)"],
    production_details={
        "hectares": 90,
        "key_wine": "Sassicaia — Italy's most celebrated Cabernet Sauvignon-based wine",
        "appellation": "Bolgheri Sassicaia DOC (own DOC since 1994)",
        "grapes": "Cabernet Sauvignon 85%, Cabernet Franc 15%"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Sassicaia is Italy's most internationally recognised wine outside Brunello. "
        "Created the Super Tuscan movement. 1985 vintage rated 100pts by Wine Spectator — "
        "the first Italian wine to achieve this. Strong global distribution."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

ornellaia_estate = P(cur, "Ornellaia",
    producer_type="winery", region_id=BOLGHERI, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Ornellaia was founded in 1981 by Lodovico Antinori (nephew of Piero Antinori) "
        "on the Bolgheri coast. Now owned by Frescobaldi, it produces Ornellaia "
        "(Cabernet Sauvignon-Merlot blend) and the 'Masseto' — Italy's greatest Merlot, "
        "grown on a clay-rich hill that Lodovico recognized as extraordinary Merlot terroir. "
        "Masseto was separated into its own company in 2017."
    ),
    key_personnel=["Axel Heinz (winemaker since 2005)"],
    production_details={
        "hectares": 99,
        "key_wines": ["Ornellaia (Cabernet blend)", "Le Serre Nuove (second wine)", "Le Volte"],
        "ownership": "Frescobaldi (since 2005)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Ornellaia is a benchmark Bolgheri wine — Bordeaux-style blend on Tuscan coast. "
        "Consistently in Italy's top tier. Strong BC distribution."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

antinori = P(cur, "Marchesi Antinori",
    producer_type="winery", region_id=CHIANTI, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Antinori is Italy's most historically significant wine family — 26 generations of "
        "continuous wine production since 1385 in Florence. Piero Antinori created Tignanello "
        "in 1971 — the wine that launched the Super Tuscan movement by blending Sangiovese "
        "with Cabernet Sauvignon and aging in barrique rather than large oak. "
        "Today the estate includes Tignanello, Guado al Tasso (Bolgheri), "
        "Cervaro della Sala (Umbria), and many others."
    ),
    key_personnel=["Piero Antinori", "Albiera Antinori", "Allegra Antinori", "Alessia Antinori"],
    production_details={
        "founded": 1385,
        "key_wines": ["Tignanello", "Solaia", "Guado al Tasso"],
        "tignanello_history": "first Super Tuscan — Sangiovese + Cabernet blend in barrique (1971)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Antinori is Italy's most historically important wine family. Tignanello is a "
        "benchmark Super Tuscan — widely distributed and consistently excellent. "
        "Good BC availability."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

montevertine = P(cur, "Montevertine",
    producer_type="winery", region_id=CHIANTI, country="Italy",
    production_philosophy="natural",
    philosophy_description=(
        "Montevertine was founded by Sergio Manetti in 1971 in Radda in Chianti. Manetti "
        "grew disillusioned with Chianti Classico DOCG regulations (which required white grapes "
        "in the blend) and withdrew from the appellation. Le Pergole Torte — 100% Sangiovese "
        "from a single vineyard — is classified as mere IGT Toscana but is widely considered "
        "Italy's greatest Sangiovese. His son Martino continues the estate."
    ),
    key_personnel=["Sergio Manetti (founder, d.2000)", "Martino Manetti (current)"],
    production_details={
        "hectares": 22,
        "key_wines": ["Le Pergole Torte (IGT Toscana, 100% Sangiovese)", "Montevertine (Sangiovese blend)", "Pian del Ciampolo"],
        "philosophy": "withdrew from Chianti Classico DOCG to make pure Sangiovese"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Montevertine Le Pergole Torte is considered Italy's greatest Sangiovese expression. "
        "Despite IGT classification, it commands prices comparable to Brunello Riserva."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

fontodi = P(cur, "Fontodi",
    producer_type="winery", region_id=CHIANTI, country="Italy",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Fontodi is the great estate of the Conca d'Oro — the golden amphitheater in "
        "Panzano in Chianti that Giovanni Manetti (no relation to Montevertine Manetti) "
        "has converted to biodynamic farming. Flaccianello della Pieve (100% Sangiovese, IGT) "
        "is the flagship — a wine of extraordinary concentration and elegance from the "
        "galestro and alberese soils of the Conca d'Oro."
    ),
    key_personnel=["Giovanni Manetti"],
    production_details={
        "hectares": 70,
        "key_wines": ["Flaccianello della Pieve (IGT, 100% Sangiovese)", "Chianti Classico Gran Selezione Vigna del Sorbo"],
        "certification": "biodynamic"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Fontodi Flaccianello is one of Tuscany's great single-vineyard Sangiovese expressions. "
        "The biodynamic conversion of the Conca d'Oro is considered a model for the region."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

isole_olena = P(cur, "Isole e Olena",
    producer_type="winery", region_id=CHIANTI, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Isole e Olena is the estate of Paolo de Marchi — one of Chianti Classico's most "
        "thoughtful producers. His Cepparello (100% Sangiovese, IGT) is a benchmark for "
        "elegant, pure Sangiovese. De Marchi has also produced extraordinary Syrah "
        "(unusual for Tuscany) and Chardonnay from his high-altitude vineyards. "
        "The estate is now owned by the D'Urso family but de Marchi has remained."
    ),
    key_personnel=["Paolo de Marchi"],
    production_details={
        "hectares": 50,
        "key_wines": ["Cepparello (IGT, 100% Sangiovese)", "Chianti Classico", "Syrah"],
        "cepparello": "IGT — withdrew from Chianti Classico for pure Sangiovese expression"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Isole e Olena is a benchmark Chianti estate with consistent quality. "
        "Cepparello is one of Tuscany's finest Sangiovese expressions."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

bibi_graetz = P(cur, "Bibi Graetz",
    producer_type="winery", region_id=TUSCANY, country="Italy",
    production_philosophy="natural",
    philosophy_description=(
        "Bibi Graetz is a Florentine artist who discovered old, abandoned Sangiovese vineyards "
        "on Fiesole hill above Florence and decided to make wine from them. Testamatta "
        "('crazy head') — from 80-100 year old Sangiovese vines on clay-limestone soils — "
        "has become one of Italy's most exciting Sangiovese wines. "
        "His approach is deliberately artisanal and philosophical: no certification, "
        "farming guided by instinct, winemaking minimal."
    ),
    key_personnel=["Bibi Graetz"],
    production_details={
        "location": "Fiesole hill above Florence",
        "key_wines": ["Testamatta (100% Sangiovese)", "Colore", "Bugia"],
        "vine_age": "80-100+ years old Sangiovese vines"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Bibi Graetz has become a cult figure in Italian natural wine. Testamatta "
        "from century-old vines is extraordinary — complex, wild, deeply mineral."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

print("\n=== TUSCANY PRODUCTS ===")

brunello_riserva = PROD(cur, "Biondi-Santi Brunello di Montalcino Riserva",
    category="wine_still", producer_id=biondi_santi, region_id=BRUNELLO,
    subcategory="red",
    description=(
        "Biondi-Santi Brunello Riserva is made only in exceptional years from old-vine "
        "Brunello Sangiovese at Il Greppo. Released after 6+ years aging (including "
        "minimum 3.5 years in large Slavonian oak). The wine is famously austere in youth — "
        "tight, tannic, demanding — but opens into something extraordinary after 20-30 years. "
        "Great vintages: 1955, 1964, 1975, 1985, 1990, 1995, 2012, 2016."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Brunello Riserva — Italy's founding great red wine",
        "aging_potential": "40-60 years in great vintages",
        "release": "minimum 6 years after harvest"
    }],
    deductive_profile={
        "appearance": "garnet, browning rim, brick-orange at maturity",
        "nose": "dried cherry, dried rose, tar, tobacco, leather, forest floor, camphor",
        "palate": "high acidity, firm tannin, great length, austere in youth",
        "signature": "Montalcino finesse — more elegant and floral than Barolo's earthiness",
        "blind_clues": "Sangiovese: cherry + dried flower + tobacco; more acid-driven than Nebbiolo"
    },
    service_specs={
        "temperature": "17-18C",
        "decanting": "young: 3-4 hours; mature: 1-2 hours carefully",
        "aging": "minimum 15 years; ideal 25-40 years"
    },
    flavour_markers=["dried cherry", "dried rose", "tar", "tobacco", "leather", "camphor"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$600-$1200+",
    technical_specs={
        "grape": "Brunello (Sangiovese Grosso) 100%",
        "appellation": "Brunello di Montalcino DOCG Riserva",
        "oak": "large Slavonian oak 3.5 years minimum"
    })

sassicaia = PROD(cur, "Tenuta San Guido Sassicaia",
    category="wine_still", producer_id=tenuta_san_guido, region_id=BOLGHERI,
    subcategory="red",
    description=(
        "Sassicaia is Italy's most internationally recognised non-Barolo red wine. "
        "A Cabernet Sauvignon-Cabernet Franc blend grown on the Bolgheri coast — "
        "gravel soils similar to Pauillac, with the warm Mediterranean influence "
        "creating richer, more opulent fruit than Bordeaux. "
        "First Super Tuscan; now has its own DOC (Bolgheri Sassicaia). "
        "Aged 24 months in barriques (25% new)."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Italy's founding Super Tuscan — own DOC",
        "aging_potential": "20-35 years"
    }],
    deductive_profile={
        "appearance": "deep ruby-garnet",
        "nose": "blackcurrant, cedar, tobacco, graphite, olive, Mediterranean herbs",
        "palate": "full body, firm tannin, Mediterranean warmth, very long mineral finish",
        "signature": "Italian Cabernet — more herbal and Mediterranean than Napa; more opulent than Bordeaux",
        "blind_clues": "If it tastes like Bordeaux with more warmth and olive/herb = Super Tuscan Cabernet"
    },
    service_specs={
        "temperature": "17-18C",
        "decanting": "2-3 hours for young vintages",
        "aging": "8-25 years from vintage"
    },
    flavour_markers=["blackcurrant", "cedar", "tobacco", "graphite", "olive", "Mediterranean herb"],
    flavour_weight="full",
    flavour_profile_type="structured Cabernet",
    price_tier="ultra_premium",
    price_range_cad="$350-$550",
    technical_specs={
        "grape": "Cabernet Sauvignon 85%, Cabernet Franc 15%",
        "appellation": "Bolgheri Sassicaia DOC",
        "oak": "barrique 24 months (25% new)"
    })

ornellaia_wine = PROD(cur, "Ornellaia Bolgheri Superiore",
    category="wine_still", producer_id=ornellaia_estate, region_id=BOLGHERI,
    subcategory="red",
    description=(
        "Ornellaia is a Bordeaux-style blend from Bolgheri — Cabernet Sauvignon, Merlot, "
        "Cabernet Franc, and Petit Verdot from the coastal estate. Each vintage is given "
        "an artistic theme ('the exuberance of 2011', 'the harmony of 2013') and a unique "
        "label by a different artist. Lush, Mediterranean-influenced, and consistently "
        "among Italy's most polished international-style reds."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Bolgheri Superiore — iconic Super Tuscan Bordeaux blend",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "blackcurrant, dark cherry, cedar, mocha, chocolate, Mediterranean herbs",
        "palate": "full body, polished tannin, rich and lush, very long finish",
        "signature": "the most polished and international of the Bolgheri wines — opulence and precision"
    },
    service_specs={"temperature": "17-18C", "decanting": "1-2 hours", "aging": "8-25 years"},
    flavour_markers=["blackcurrant", "dark cherry", "cedar", "mocha", "chocolate", "herb"],
    flavour_weight="full",
    flavour_profile_type="structured Cabernet",
    price_tier="ultra_premium",
    price_range_cad="$280-$450",
    technical_specs={
        "grape": "Cabernet Sauvignon, Merlot, Cabernet Franc, Petit Verdot blend",
        "appellation": "Bolgheri Superiore DOC"
    })

tignanello = PROD(cur, "Antinori Tignanello",
    category="wine_still", producer_id=antinori, region_id=CHIANTI,
    subcategory="red",
    description=(
        "Tignanello created the Super Tuscan category in 1971 — the first time Sangiovese "
        "was blended with Cabernet Sauvignon (20%) and aged in barrique rather than large oak. "
        "It was also the first commercial Chianti to eliminate white grapes. "
        "Today it remains the benchmark Super Tuscan: 80% Sangiovese, 15% Cabernet Sauvignon, "
        "5% Cabernet Franc, from the Tignanello vineyard in Sant'Andrea in Percussina."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "historical_significance": "the first Super Tuscan — created the category (1971)",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "cherry, blackcurrant, cedar, spice, tobacco, subtle olive",
        "palate": "Sangiovese freshness + Cabernet structure; medium-full body; long finish",
        "signature": "the Super Tuscan blueprint — Sangiovese brightness + Cabernet structure"
    },
    service_specs={"temperature": "17C", "decanting": "1-2 hours", "aging": "8-20 years"},
    flavour_markers=["cherry", "blackcurrant", "cedar", "spice", "tobacco"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$200-$320",
    technical_specs={
        "grape": "Sangiovese 80%, Cabernet Sauvignon 15%, Cabernet Franc 5%",
        "appellation": "IGT Toscana"
    })

le_pergole_torte = PROD(cur, "Montevertine Le Pergole Torte",
    category="wine_still", producer_id=montevertine, region_id=CHIANTI,
    subcategory="red",
    description=(
        "Le Pergole Torte is Italy's greatest 100% Sangiovese — grown on the alberese "
        "and galestro soils of a single vineyard in Radda in Chianti. "
        "Classified as IGT Toscana (because Sergio Manetti refused DOCG rules), "
        "it nonetheless commands prices above most Brunello Riserva. "
        "Each label features an original artwork by sculptor Lorenzo Casini. "
        "Made since 1977; aged in small French oak since 1994."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Italy's greatest Sangiovese — IGT despite Grand Cru quality",
        "aging_potential": "25-40 years"
    }],
    deductive_profile={
        "appearance": "ruby-garnet; evolves to brick-orange",
        "nose": "cherry, dried flower, leather, mineral clay, iron, tobacco",
        "palate": "extreme purity of Sangiovese fruit, electric acidity, fine mineral tannin",
        "signature": "the purest Sangiovese expression — no Cabernet, no additions, full terroir"
    },
    service_specs={
        "temperature": "16-17C",
        "decanting": "2-3 hours young; 1 hour for mature",
        "aging": "optimal 10-25 years"
    },
    flavour_markers=["cherry", "dried flower", "leather", "mineral clay", "iron", "tobacco"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$350-$600",
    technical_specs={
        "grape": "Sangiovese 100%",
        "appellation": "IGT Toscana",
        "vineyard": "Le Pergole Torte, Radda in Chianti"
    })

flaccianello = PROD(cur, "Fontodi Flaccianello della Pieve",
    category="wine_still", producer_id=fontodi, region_id=CHIANTI,
    subcategory="red",
    description=(
        "Flaccianello della Pieve is the flagship of the Conca d'Oro — 100% Sangiovese "
        "from the biodynamically farmed estate in Panzano in Chianti. "
        "The galestro and alberese soils of the Conca d'Oro amphitheater are some of "
        "Chianti's most celebrated terroir. The wine has extraordinary concentration "
        "and elegance — the biodynamic farming is evident in the mineral tension."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Conca d'Oro amphitheater, Panzano",
        "farming": "biodynamic",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "dark cherry, dried rose, iron mineral, tobacco, dried herbs",
        "palate": "concentrated but precise, firm tannin, mineral acid backbone",
        "signature": "biodynamic mineral tension — Conca d'Oro galestro-iron precision"
    },
    service_specs={"temperature": "17C", "decanting": "2 hours", "aging": "8-25 years"},
    flavour_markers=["dark cherry", "dried rose", "iron mineral", "tobacco", "dried herb"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="premium",
    price_range_cad="$160-$280",
    technical_specs={
        "grape": "Sangiovese 100%",
        "appellation": "IGT Toscana",
        "soil": "galestro and alberese (Conca d'Oro)"
    })

cepparello = PROD(cur, "Isole e Olena Cepparello",
    category="wine_still", producer_id=isole_olena, region_id=CHIANTI,
    subcategory="red",
    description=(
        "Cepparello is Isole e Olena's 100% Sangiovese from old vines — a wine of remarkable "
        "elegance and consistency. Paolo de Marchi withdrew from Chianti Classico DOCG to "
        "make pure Sangiovese without required blending rules. The result is a wine that "
        "shows Sangiovese's capacity for both power and finesse."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Single-vineyard IGT — pure Sangiovese",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "nose": "cherry, dried rose, tobacco, mineral, subtle spice from French oak",
        "palate": "elegant structure, bright acidity, refined tannin, long finish",
        "signature": "the most consistently elegant pure Sangiovese in Chianti"
    },
    service_specs={"temperature": "17C", "decanting": "1-2 hours", "aging": "8-20 years"},
    flavour_markers=["cherry", "dried rose", "tobacco", "mineral", "spice"],
    flavour_weight="medium-full",
    flavour_profile_type="tannic structured",
    price_tier="premium",
    price_range_cad="$140-$220",
    technical_specs={
        "grape": "Sangiovese 100%",
        "appellation": "IGT Toscana"
    })

testamatta = PROD(cur, "Bibi Graetz Testamatta",
    category="wine_still", producer_id=bibi_graetz, region_id=TUSCANY,
    subcategory="red",
    description=(
        "Testamatta ('crazy head') is made from 80-100 year old Sangiovese vines on "
        "Fiesole hill above Florence — an area no one else was farming seriously. "
        "The old vines produce extraordinary concentrated, wild Sangiovese unlike anything "
        "in Chianti or Montalcino. Minimal intervention, extended maceration, aged in large "
        "and small French oak. A genuinely wild and unique wine."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vine_age": "80-100+ years old Sangiovese on Fiesole",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "dark cherry, dried flower, clay mineral, leather, dried herbs, earthy",
        "palate": "concentrated, wild, complex, very long finish",
        "signature": "old-vine wildness — the most artisanal of Tuscany's great Sangiovese wines"
    },
    service_specs={"temperature": "17C", "decanting": "2-3 hours", "aging": "8-20 years"},
    flavour_markers=["dark cherry", "dried flower", "clay mineral", "leather", "dried herb"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$200-$350",
    technical_specs={
        "grape": "Sangiovese 100%",
        "appellation": "IGT Toscana",
        "vineyard": "Fiesole, above Florence"
    })

print("\n=== TUSCANY REFERENCES ===")

ref_brunello = REF(cur,
    "Brunello di Montalcino — DOCG Regulations, Style Spectrum, and Sub-Zone Logic",
    category="wine_regions", skill_level="advanced",
    description=(
        "Brunello di Montalcino is Italy's most prestigious red wine DOCG. "
        "Understanding its regulations, sub-zone terroir differences, and the "
        "Brunello vs Rosso hierarchy is essential for service and recommendation."
    ),
    key_principles=(
        "GRAPE: Brunello = Sangiovese Grosso (a clone of Sangiovese selected by Biondi-Santi). "
        "100% Sangiovese required. "
        "\nREGULATIONS: "
        "Brunello di Montalcino DOCG: minimum 5 years aging (2 in oak); "
        "released no earlier than Jan 1 of 5th year after harvest. "
        "Riserva: 6 years minimum; 2.5 years in oak. "
        "Rosso di Montalcino DOC: 1 year minimum; released same year as harvest. "
        "\nSUB-ZONE TERROIR: "
        "NORTH (Biondi-Santi, Lisini): coolest; volcanic tufa and clay; most elegant and structured. "
        "SOUTH (Banfi, Caparzo, Casanova di Neri): warmer; more Mediterranean; richer, rounder. "
        "EAST (Cerbaiona, Altesino, Poggio di Sotto): galestro-limestone; most mineral and austere. "
        "\nBRUNELLO vs ROSSO DI MONTALCINO: "
        "Rosso is not a failed Brunello — it is the second wine. "
        "Best producers (Poggio di Sotto, Cerbaia) make Rosso deliberately excellent — "
        "approachable at 2-3 years but from same vineyards as Brunello. "
        "At the table, Rosso is often the better recommendation (food-friendlier, ready now). "
        "\nSTYLE EVOLUTION: "
        "Traditional: large Slavonian oak, austere, 20+ year ageability. "
        "Modern: barrique, richer, approachable earlier. "
        "Today: most producers balance both. The BBES scandal (2008) led to re-regulation."
    ),
    common_mistakes=(
        "Assuming all Brunello is the same regardless of sub-zone. "
        "Treating Rosso di Montalcino as inferior — at top estates it is excellent. "
        "Not knowing the aging requirements (confusing Brunello annata with Riserva). "
        "Under-estimating the north-south terroir divide in Montalcino."
    ),
    pro_tips=(
        "If a guest wants Brunello but needs it ready now, recommend Rosso di Montalcino "
        "from a great producer (Poggio di Sotto, Cerbaia). "
        "The 2016 Brunello is universally hailed as the vintage of the decade — "
        "recommend for serious cellaring."
    ),
    authority_tier=1,
    source_text="Consorzio del Vino Brunello di Montalcino; DOCG regulations; Jancis Robinson Oxford Companion"
)

ref_super_tuscans = REF(cur,
    "Super Tuscans and the IGT Revolution — Sangiovese, Cabernet, and Merlot in Tuscany",
    category="wine_regions", skill_level="advanced",
    description=(
        "Super Tuscans' — wines made outside traditional DOC/DOCG rules — transformed Italian "
        "wine in the 1970s-90s and created a new category of prestige. "
        "Understanding the movement's history, the key wines, and the IGT framework "
        "is essential for intelligent Tuscan navigation."
    ),
    key_principles=(
        "HISTORY: "
        "1968: Sassicaia first commercial release (Cabernet Sauvignon — not an Italian variety; "
        "sold as 'Vino da Tavola' — table wine, the lowest category). "
        "1971: Tignanello — first Super Tuscan blending Sangiovese with Cabernet in barrique. "
        "1975: Solaia introduced. "
        "1978: Ornellaia planted. "
        "By the 1980s, Italy's best wines were classified as mere table wine. "
        "1992: IGT category created — allowing wines like Sassicaia to have a regional label. "
        "1994: Sassicaia becomes the only single-estate DOC in Italy. "
        "\nKEY CATEGORIES: "
        "BOLGHERI: Cabernet-based (Sassicaia, Ornellaia) or Merlot-based (Masseto). "
        "Mediterranean influence; gravel soils. "
        "CHIANTI CLASSICO IGT: Pure Sangiovese (Tignanello, Le Pergole Torte, Cepparello). "
        "The wine that left DOC because DOCG rules were too restrictive. "
        "\nWHY 'SUPER TUSCAN' MATTERS COMMERCIALLY: "
        "These wines bypassed bureaucracy and proved terroir-driven quality could come from "
        "rules-defying production. The lesson: quality matters more than classification. "
        "Today many are back within DOC/DOCG (Sassicaia has its own DOC). "
        "\nSANGIOVESE DEDUCTIVE BASICS: "
        "Cherry + dried flower + tobacco + high acidity + firm tannin = Sangiovese. "
        "Brunello: 5+ years aging, very long life. "
        "Chianti Classico Gran Selezione: food-friendly, ready at 5-10 years. "
        "Pure Sangiovese IGT (Pergole Torte, Cepparello): most intellectually pure expression."
    ),
    common_mistakes=(
        "Assuming 'IGT' means lower quality — Pergole Torte is classified IGT but rivals "
        "the world's greatest reds. "
        "Treating all Bolgheri wines as 'Italian Bordeaux' — the terroir is fundamentally different. "
        "Not knowing that Tignanello was the first Super Tuscan blend (not Sassicaia, which is "
        "Cabernet only, no Sangiovese)."
    ),
    pro_tips=(
        "The hierarchy paradox is a useful teaching tool: Le Pergole Torte (classified 'IGT Toscana') "
        "sells for more than most Brunello Riserva (classified as Italy's highest DOCG). "
        "Quality transcends classification in Italian wine."
    ),
    authority_tier=1,
    source_text="Hugh Johnson and Jancis Robinson 'World Atlas of Wine'; Antinori estate documentation"
)

print("\n=== TUSCANY PAIRINGS ===")

PAIR(cur, "Bistecca alla Fiorentina — T-bone grilled over chestnut charcoal",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "The definitive Tuscan pairing — Chianina beef T-bone, 1kg minimum, grilled very rare over "
     "chestnut charcoal, with just olive oil, salt, and lemon. Brunello Riserva's tannin "
     "structure precisely matches the protein and fat of aged Chianina beef; "
     "the wine's acidity cuts through the charred fat. One of Italy's great terroir pairings.",
     brunello_riserva, food_flavour_profile="aged beef, charcoal, fat, olive oil", beverage_category="wine_still")

PAIR(cur, "Cinghiale in dolceforte — wild boar in sweet-sour sauce",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Wild boar braised in Chianti with pine nuts, chocolate, and vinegar (dolceforte sauce) "
     "is a medieval Tuscan recipe. Le Pergole Torte's complex, iron-mineral Sangiovese "
     "meets the gamey richness and sweet-sour complexity of the dish.",
     le_pergole_torte, food_flavour_profile="wild boar, chocolate, vinegar, pine nut, gamey", beverage_category="wine_still")

PAIR(cur, "Tagliata di manzo with rucola and Parmigiano",
     "wagyu_premium_protein", "main",
     "established", "complement",
     "Sliced grilled beef with bitter rocket and Parmigiano — a Florentine trattoria classic. "
     "Tignanello's Sangiovese freshness and Cabernet structure provides the ideal frame: "
     "acidity for the rocket, tannin for the beef.",
     tignanello, food_flavour_profile="grilled beef, bitter rocket, Parmigiano, olive oil", beverage_category="wine_still")

PAIR(cur, "Ribollita — Tuscan bread and bean soup with cavolo nero",
     "produce_specialty", "main",
     "established", "complement",
     "Ribollita (twice-cooked Tuscan soup with bread, cannellini beans, and black kale) "
     "is humble food requiring a humble-ambitious wine. Flaccianello's biodynamic mineral "
     "energy lifts the earthy bean soup; the wine's tannin provides structure against "
     "the starchy bread thickening.",
     flaccianello, food_flavour_profile="bean, kale, bread, tomato, sage, earthy", beverage_category="wine_still")

PAIR(cur, "Pappardelle al cinghiale — pappardelle with wild boar ragu",
     "rice_grains", "main",
     "classic", "complement",
     "Pappardelle al cinghiale is the canonical Tuscan pasta dish. Cepparello's elegant, "
     "pure Sangiovese structure complements the gamey, herb-rich boar ragu without overwhelming "
     "the pasta's egg richness.",
     cepparello, food_flavour_profile="wild boar, herb ragu, egg pasta, rosemary", beverage_category="wine_still")

PAIR(cur, "Pecorino di Pienza with honey, walnuts, and fresh figs",
     "dairy_fermented", "cheese",
     "classic", "complement",
     "Pecorino di Pienza (aged sheep milk cheese from the Crete Senesi) and Brunello is "
     "a regional pairing of profound simplicity. The wine's tannin cuts the sheep fat; "
     "the honey bridges the dried cherry in the wine; the walnut echoes the tobacco notes.",
     brunello_riserva, food_flavour_profile="aged sheep cheese, honey, walnut, fresh fig", beverage_category="wine_still")

PAIR(cur, "Crostini neri — chicken liver pate on grilled bread",
     "charcuterie_cured", "starter",
     "classic", "complement",
     "Crostini neri (chicken liver crostini with capers and anchovies) is the quintessential "
     "Florentine antipasto. Sassicaia's cedar-blackcurrant Mediterranean character provides "
     "a counterpoint to the ferrous richness of liver — the Cabernet's freshness "
     "cuts through the intensity.",
     sassicaia, food_flavour_profile="chicken liver, caper, anchovy, grilled bread", beverage_category="wine_still")

PAIR(cur, "Ribollita with old-vine Fiesole Sangiovese",
     "produce_specialty", "casual",
     "suggested", "complement",
     "Testamatta from century-old Fiesole vines with the simple Tuscan peasant food "
     "that would have fed the vineyard workers. The wine's wild complexity and old-vine "
     "concentration creates an unexpected dialogue with humble ribollita.",
     testamatta, food_flavour_profile="bean, kale, bread, olive oil, garlic", beverage_category="wine_still")

print("\n✅ Tuscany batch complete.")
cur.close()
conn.close()
