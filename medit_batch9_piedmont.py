#!/usr/bin/env python3
"""Batch 9 — Italian Wine: Piedmont (30 targets)
Producers: Gaja, Bruno Giacosa, Bartolo Mascarello, Giuseppe Quintarelli-style (Giacomo Conterno),
           Roagna, Cogno, Ceretto, G.D. Vajra, Vietti, Marchesi di Barolo
Products: Gaja Barbaresco, Gaja Sori Tildin, Giacosa Barolo Falletto, Barolo Mascarello,
          Conterno Monfortino, Cogno Ravera, Roagna Crichet Paje, Vietti Castiglione,
          Ceretto Bricco Rocche, Vajra Bricco delle Viole, Gaja Ca Marcanda
References: Barolo DOCG Crus and Nebbiolo; Barbaresco vs Barolo; Barolo Wars
Pairings: truffle, tajarin, brasato, finanziera, vitello tonnato
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Piedmont region IDs from batch1
# Piedmont=160, Barolo=161, Barbaresco=162, Langhe=163, Gavi=164
PIEDMONT = 160
BAROLO = 161
BARBARESCO = 162
LANGHE = 163

print("\n=== PIEDMONT PRODUCERS ===")

gaja = P(cur, "Gaja",
    producer_type="winery", region_id=BARBARESCO, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Angelo Gaja single-handedly transformed Piedmont's international reputation. "
        "He introduced Barrique aging (controversial at the time), introduced French varieties "
        "to Piedmont, and relentlessly promoted the region to international markets. "
        "His Barbaresco crus — Sori Tildin, Costa Russi, Sori San Lorenzo — are among Italy's "
        "most iconic wines. He also created Sito Moresco and Promis (Langhe) and expanded to "
        "Bolgheri (Ca Marcanda) and Montalcino (Pieve Santa Restituta)."
    ),
    key_personnel=["Angelo Gaja", "Gaia Gaja", "Giovanni Gaja"],
    production_details={
        "hectares": 100,
        "key_wines": ["Barbaresco (single-vineyard crus)", "Barolo (Sperss, Conteisa)", "Ca Marcanda (Bolgheri)"],
        "style": "modern — barrique aging, single-vineyard focus",
        "crus": ["Sori Tildin", "Costa Russi", "Sori San Lorenzo"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Gaja is the most globally recognised Italian wine producer. His wines command prices "
        "comparable to First Growth Bordeaux. Strong BC agent network."
    ),
    allocation_notes="BC — Select Wine Merchants [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

giacosa = P(cur, "Bruno Giacosa",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Bruno Giacosa was the 'great traditionalist' of Piedmont — producing wines of "
        "extraordinary structure and longevity from owned and purchased vineyards. "
        "His Barolo Falletto (from his own Serralunga vineyard) and Barbaresco Santo Stefano "
        "(from Neive) are benchmarks for the traditional style: large Slavonian oak, extended "
        "maceration, no barrique. Giacosa was also a brilliant négoce buyer — his vintage "
        "purchases from top growers are legendary. He passed away in 2018; the estate continues."
    ),
    key_personnel=["Bruno Giacosa (founder, d.2018)", "Bruna Giacosa (current)"],
    production_details={
        "model": "estate + négociant",
        "key_wines": ["Barolo Falletto (Serralunga)", "Barbaresco Santo Stefano (Neive)"],
        "style": "traditional — large Slavonian oak, extended maceration",
        "label": "red label = riserva; white label = standard"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Giacosa Barolo Falletto Riserva (red label) is among the most coveted Italian wines. "
        "His négoce bottlings from the 1960s-80s are legendary collector items."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

mascarello = P(cur, "Bartolo Mascarello",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="natural",
    philosophy_description=(
        "Bartolo Mascarello was the philosophical leader of the Barolo 'traditionalist' camp "
        "in the Barolo Wars of the 1980s-90s. He was also a passionate political activist — "
        "his hand-painted labels feature anti-war and political slogans. "
        "His single Barolo is a blend from four historic crus in La Morra and Barolo villages — "
        "deliberately NOT single-vineyard, to express the totality of Barolo terroir. "
        "Large Slavonian oak, zero barrique, very long maceration. "
        "Daughter Maria Teresa continues the estate."
    ),
    key_personnel=["Bartolo Mascarello (founder, d.2005)", "Maria Teresa Mascarello (current)"],
    production_details={
        "hectares": 5,
        "style": "ultra-traditional — single Barolo from four cru blend, Slavonian oak",
        "production": "very small — around 25,000 bottles/year total",
        "labels": "hand-painted by Bartolo Mascarello; political art"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Mascarello Barolo is one of Italy's most sought-after wines. Production is tiny "
        "and allocation is fiercely competitive. A philosophical and qualitative benchmark."
    ),
    allocation_notes="Ultra-limited; BC allocation [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

conterno = P(cur, "Giacomo Conterno",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Giacomo Conterno is the producer of Barolo Monfortino — Italy's most celebrated "
        "and age-worthy single wine. Monfortino is made only in exceptional vintages from "
        "the Cascina Francia vineyard in Serralunga d'Alba, aged a minimum 7 years in large "
        "Slavonian oak casks. The result is a wine of extraordinary structure and 50+ year "
        "aging potential. Roberto Conterno (Giacomo's son) now runs the estate."
    ),
    key_personnel=["Giacomo Conterno (founder)", "Roberto Conterno (current)"],
    production_details={
        "hectares": 14,
        "key_wines": ["Barolo Monfortino Riserva", "Barolo Cascina Francia", "Barbera d'Alba Francia"],
        "style": "ultra-traditional — 7+ years Slavonian oak for Monfortino",
        "monfortino": "made only in exceptional vintages from Cascina Francia, Serralunga"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Monfortino Barolo Riserva is Italy's most age-worthy wine — regularly assessed "
        "at 50+ year potential. Roberto Conterno also acquired Cerequio, one of Barolo's "
        "greatest crus, in 2015. Among Italy's most important estates."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

roagna = P(cur, "Roagna",
    producer_type="winery", region_id=BARBARESCO, country="Italy",
    production_philosophy="natural",
    philosophy_description=(
        "Roagna in Paje (Barbaresco) is the most philosophically rigorous of Piedmont's "
        "natural producers. Luca Roagna produces wines from extremely old vines (Paje, "
        "Asili, Gallina, Rabaja — all Barbaresco crus) with extended maceration (90+ days), "
        "aging in large Slavonian oak, and absolute minimal intervention. "
        "The Crichet Paje is a single-vineyard selection from the oldest Paje vines — "
        "one of Italy's greatest wines."
    ),
    key_personnel=["Luca Roagna", "Alfredo Roagna"],
    production_details={
        "hectares": 12,
        "key_wines": ["Barbaresco Crichet Paje", "Barbaresco Paje", "Barolo La Pira"],
        "style": "natural-traditional — extended maceration, large Slavonian oak",
        "maceration": "90+ days for Crichet Paje"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Roagna Crichet Paje is among Italy's most exciting and age-worthy Nebbiolo expressions. "
        "Production is tiny; allocation strictly controlled."
    ),
    allocation_notes="Ultra-limited; BC allocation [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

vietti = P(cur, "Vietti",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Vietti in Castiglione Falletto is one of Piedmont's most historically significant "
        "estates — Alfredo Currado began labeling single-vineyard Barolo in the 1960s, "
        "predating the modern single-vineyard movement. The estate produces Barolo from "
        "five crus (Lazzarito, Brunate, Rocche, Castiglione, Villero) and Barbaresco "
        "from Masseria. Luca Currado (son-in-law) is the current winemaker. "
        "Now owned by the Krause family (US); quality has remained very high."
    ),
    key_personnel=["Luca Currado", "Elena Penna"],
    production_details={
        "hectares": 45,
        "key_wines": ["Barolo Lazzarito", "Barolo Brunate", "Barolo Castiglione", "Barbera d'Asti Scarrone"],
        "crus": ["Lazzarito (Serralunga)", "Brunate (La Morra)", "Castiglione Falletto"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Vietti is a historically important estate and produces some of Barolo's finest "
        "single-vineyard expressions. Broad distribution including BC."
    ),
    allocation_notes="BC — agents / specialty retailers",
    price_positioning="ultra_premium", authority_tier=1)

vajra = P(cur, "G.D. Vajra",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="biodynamic",
    philosophy_description=(
        "G.D. Vajra in Vergne (Barolo) represents a balanced approach to Piedmontese "
        "winemaking — respectful of tradition but without dogma. Their Bricco delle Viole "
        "Barolo (from the highest elevation cru in Barolo DOCG, on volcanic soils) is "
        "among Barolo's most distinctive and ethereal expressions. Also outstanding: "
        "their Dolcetto d'Alba, Freisa, and Langhe Riesling (unusual for the region)."
    ),
    key_personnel=["Aldo Vaira", "Milena Vaira", "Isidoro Vaira"],
    production_details={
        "hectares": 60,
        "key_wines": ["Barolo Bricco delle Viole", "Barolo Luigi Baudana", "Langhe Riesling"],
        "bricco_delle_viole": "highest elevation Barolo cru — volcanic soil, ethereal style"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Vajra is a beloved estate among sommeliers for intellectual depth and excellent value "
        "relative to some other Barolo estates. Bricco delle Viole is extraordinary."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

ceretto = P(cur, "Ceretto",
    producer_type="winery", region_id=BAROLO, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Ceretto is one of the most business-minded and quality-focused families in Piedmont, "
        "owning multiple estates across Barolo, Barbaresco, and the Langhe. Their Bricco Rocche "
        "estate in Castiglione Falletto produces single-vineyard Barolo from some of the "
        "appellation's finest south-facing slopes. The Zonchetta Barolo from Bricco Rocche "
        "is their apex expression. Also known for their Barbaresco at Bricco Asili."
    ),
    key_personnel=["Bruno Ceretto", "Marcello Ceretto"],
    production_details={
        "hectares": 160,
        "key_estates": ["Bricco Rocche (Barolo)", "Bricco Asili (Barbaresco)", "Blange (Moscato)"],
        "style": "modern — barrique aging for single-vineyard expressions"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Ceretto is one of Piedmont's most consistent quality estates with broad distribution. "
        "Good BC availability across price points."
    ),
    allocation_notes="BC — Lifford Wine Agency / agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== PIEDMONT PRODUCTS ===")

gaja_barbaresco = PROD(cur, "Gaja Barbaresco",
    category="wine_still", producer_id=gaja, region_id=BARBARESCO,
    subcategory="red",
    description=(
        "Gaja's estate Barbaresco DOCG is the entry point to the Gaja hierarchy — a blend "
        "from multiple village parcels including Brich Ronchi, Roncaglie, and others. "
        "Modern in style (barrique-aged), it offers approachability at 5-8 years but rewards "
        "patience to 15-20 years. A benchmark for the appellation at the entry-estate level."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Barbaresco DOCG estate blend",
        "hierarchy": "below Sori Tildin, Costa Russi, Sori San Lorenzo",
        "aging_potential": "15-25 years"
    }],
    deductive_profile={
        "appearance": "garnet-ruby, browning rim with age",
        "nose": "tar, roses, cherry, leather, tobacco, subtle barrique oak",
        "palate": "full tannin, bright acidity, cherry-tar complex, long finish",
        "signature": "tar and roses — Nebbiolo's essential blind tasting fingerprint",
        "blind_clues": "Nebbiolo: tar + roses + high tannin + high acidity = Piedmont"
    },
    service_specs={
        "temperature": "16-18C",
        "decanting": "2-3 hours for young vintages; older vintages may need less",
        "glassware": "large Burgundy bowl",
        "aging": "optimal 8-20 years from vintage"
    },
    flavour_markers=["tar", "rose", "cherry", "leather", "tobacco", "liquorice"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$250-$400",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barbaresco DOCG",
        "aging": "barrique and large oak combination"
    })

gaja_sori_tildin = PROD(cur, "Gaja Sori Tildin",
    category="wine_still", producer_id=gaja, region_id=BARBARESCO,
    subcategory="red",
    description=(
        "Sori Tildin is one of Barbaresco's three legendary Gaja single-vineyard crus. "
        "The name combines 'sori' (the best sun-exposed slope in Piedmontese dialect) and "
        "'Tildin' (the nickname of Gaja's grandmother Clotilde). The vineyard in Treiso "
        "produces a more opulent, floral-forward Nebbiolo than the more austere Sori San Lorenzo. "
        "Note: technically sold as 'Langhe DOC' (Nebbiolo) as Gaja withdrew from the DOCG "
        "in protest of multi-variety blending rules — but qualitatively it is pure Barbaresco."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Single vineyard Grand Cru equivalent",
        "sold_as": "Langhe DOC Nebbiolo (withdrawn from Barbaresco DOCG)",
        "aging_potential": "25-40 years"
    }],
    deductive_profile={
        "nose": "rose, violet, tar, cherry liqueur, licorice, tobacco, subtle oak",
        "palate": "more opulent than Barbaresco DOCG; structured tannin; very long finish",
        "signature": "Treiso opulence — floral-forward Nebbiolo from south-facing slope"
    },
    service_specs={
        "temperature": "17-18C",
        "decanting": "3-4 hours for young vintages; 1-2 hours for aged",
        "aging": "optimal 10-30 years from vintage"
    },
    flavour_markers=["rose", "violet", "tar", "cherry liqueur", "licorice", "tobacco"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$600-$900+",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Langhe DOC (formerly Barbaresco DOCG)",
        "vineyard": "Sori Tildin, Treiso"
    })

giacosa_falletto = PROD(cur, "Bruno Giacosa Barolo Falletto di Serralunga",
    category="wine_still", producer_id=giacosa, region_id=BAROLO,
    subcategory="red",
    description=(
        "Giacosa Barolo Falletto is the estate's flagship wine from the 9ha Falletto vineyard "
        "in Serralunga d'Alba — Barolo's most austere and structured commune, with compact "
        "Helvetian limestone soils. The standard (white label) Falletto requires 8-10 years; "
        "the Riserva (red label, made only in exceptional years) needs 15-20+ years before peak. "
        "Large Slavonian oak aging; no barrique. Pure traditional style."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Falletto, Serralunga d'Alba",
        "commune": "Serralunga — most austere, longest aging",
        "riserva": "red label — exceptional years only; 7 years minimum aging"
    }],
    deductive_profile={
        "appearance": "garnet with ruby core; browning rim in older vintages",
        "nose": "dried rose, tar, tobacco leaf, forest floor, anise, leather",
        "palate": "extraordinary tannin structure, bright acidity, dry, very long mineral finish",
        "signature": "Serralunga austerity — angular tannin, less fruit than La Morra communes"
    },
    service_specs={
        "temperature": "16-18C",
        "decanting": "3-4 hours for young vintages; older (15+ years) pour direct",
        "aging": "10-15 years minimum; Riserva: 20-30+ years"
    },
    flavour_markers=["dried rose", "tar", "tobacco leaf", "forest floor", "anise", "leather"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$350-$600",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG",
        "vineyard": "Falletto, Serralunga d'Alba",
        "oak": "large Slavonian oak, no barrique"
    })

conterno_monfortino = PROD(cur, "Giacomo Conterno Barolo Monfortino Riserva",
    category="wine_still", producer_id=conterno, region_id=BAROLO,
    subcategory="red",
    description=(
        "Barolo Monfortino Riserva is Italy's most age-worthy wine. Made only in exceptional "
        "vintages from the Cascina Francia vineyard in Serralunga, aged a minimum 7 years in "
        "large Slavonian oak — and sometimes released 10+ years after harvest. "
        "Monfortino represents Nebbiolo at its most extreme and profound: "
        "extraordinary tannin, almost infinite acidity, 50+ year potential in great years. "
        "Great vintages: 1958, 1964, 1971, 1978, 1985, 1990, 2010, 2016."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Italy's most age-worthy wine",
        "aging_potential": "50+ years in great vintages",
        "minimum_oak_aging": "7 years in large Slavonian casks"
    }],
    deductive_profile={
        "appearance": "garnet; orange-brick rim in mature wines",
        "nose": "dried rose petals, tar, clay, camphor, tobacco, spiced leather, truffle",
        "palate": "extraordinary structure, massive yet refined tannin, 90+ second finish",
        "signature": "the most demanding and age-worthy Italian wine — requires patience of decades"
    },
    service_specs={
        "temperature": "16-17C",
        "decanting": "young: 4+ hours; older: 1 hour; very old: pour direct carefully",
        "aging": "optimal: 20-40 years from vintage; great years: 50+"
    },
    flavour_markers=["dried rose", "tar", "clay", "camphor", "tobacco", "truffle", "spiced leather"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$800-$1500+",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG Riserva",
        "vineyard": "Cascina Francia, Serralunga d'Alba",
        "oak": "minimum 7 years large Slavonian casks"
    })

mascarello_barolo = PROD(cur, "Bartolo Mascarello Barolo",
    category="wine_still", producer_id=mascarello, region_id=BAROLO,
    subcategory="red",
    description=(
        "Bartolo Mascarello's single Barolo is a deliberate cru blend from four historically "
        "significant parcels in La Morra (Ruè, San Lorenzo) and Barolo village (Cannubi, "
        "Rocche dell'Annunziata). The philosophy: Barolo is greater than any single vineyard. "
        "Ultra-traditional: extended maceration, large Slavonian oak, no barrique, no additions. "
        "Each label is a hand-painted artwork by Bartolo (and now Maria Teresa). "
        "Among Italy's most philosophically significant wines."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "philosophy": "cru blend — Barolo as appellation, not single vineyard",
        "crus": ["Rue", "San Lorenzo", "Cannubi", "Rocche dell'Annunziata"],
        "aging_potential": "30-50 years"
    }],
    deductive_profile={
        "nose": "rose petals, tar, cherry, clay mineral, tobacco, dried herbs",
        "palate": "traditional structure, tannic but refined, bright acidity, long earthy finish",
        "signature": "La Morra softness in a traditional frame — roses more than tar initially"
    },
    service_specs={
        "temperature": "16-18C",
        "decanting": "2-3 hours for young; older: 1 hour",
        "aging": "optimal 10-25 years"
    },
    flavour_markers=["rose petals", "tar", "cherry", "clay mineral", "tobacco", "dried herb"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$400-$700",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG",
        "style": "traditional — large Slavonian oak blend"
    })

vietti_castiglione = PROD(cur, "Vietti Barolo Castiglione",
    category="wine_still", producer_id=vietti, region_id=BAROLO,
    subcategory="red",
    description=(
        "Vietti Barolo Castiglione is the estate's village-level blend — a cru blend "
        "from Castiglione Falletto village parcels that serves as an accessible introduction "
        "to the Vietti style. It is the 'Bourgogne Rouge' of the Vietti range — "
        "entry-level but with genuine depth and structure. Ready in 5-8 years; "
        "rewards 10-15 years. An essential reference for teaching Nebbiolo fundamentals."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "tier": "village-level Barolo — Castiglione Falletto blend",
        "vs_single_vineyard": "approachable earlier, accessible price"
    }],
    deductive_profile={
        "nose": "cherry, rose, tar, anise, light leather",
        "palate": "medium-full body, firm tannin, bright acidity",
        "signature": "accessible Barolo structure — tar-rose without extremes"
    },
    service_specs={"temperature": "17C", "decanting": "1-2 hours", "aging": "5-15 years"},
    flavour_markers=["cherry", "rose", "tar", "anise", "light leather"],
    flavour_weight="medium-full",
    flavour_profile_type="tannic structured",
    price_tier="premium",
    price_range_cad="$120-$180",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG",
        "commune": "Castiglione Falletto blend"
    })

vajra_bricco = PROD(cur, "G.D. Vajra Barolo Bricco delle Viole",
    category="wine_still", producer_id=vajra, region_id=BAROLO,
    subcategory="red",
    description=(
        "Bricco delle Viole is the highest-elevation Grand Cru in the Barolo DOCG — "
        "at 400m+ altitude on volcanic (basalt and tufa) soils above Vergne. "
        "The combination of altitude and volcanic soils produces a Barolo of extraordinary "
        "elegance and perfume — more floral than structured, with a violet-lifted quality "
        "unlike any other Barolo cru. Vajra's biodynamic farming amplifies the terroir expression."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Bricco delle Viole — highest elevation in Barolo DOCG",
        "soil": "volcanic (basalt + tufa)",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "violet, rose, eucalyptus, mountain herbs, cherry, floral earthiness",
        "palate": "elegant, lighter tannin than La Morra, electric acidity, floral finish",
        "signature": "altitude + volcanic soil = the most ethereal Barolo — violet-dominant"
    },
    service_specs={"temperature": "16C", "decanting": "1-2 hours", "aging": "8-25 years"},
    flavour_markers=["violet", "rose", "eucalyptus", "mountain herb", "cherry", "floral earth"],
    flavour_weight="medium-full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$200-$320",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG",
        "vineyard": "Bricco delle Viole — volcanic soils at 400m+"
    })

roagna_crichet = PROD(cur, "Roagna Barbaresco Crichet Paje",
    category="wine_still", producer_id=roagna, region_id=BARBARESCO,
    subcategory="red",
    description=(
        "Crichet Paje is Roagna's flagship — a selection from the oldest (60-100 year old) "
        "Paje vineyard vines, made only in exceptional vintages. Extended maceration (90+ days), "
        "aging in large Slavonian oak for 4+ years. The wine has extraordinary concentration "
        "and tannin, with 30-50 year aging potential. One of Italy's most technically "
        "demanding and rewarding wines to assess."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Paje (Barbaresco) — oldest vine selection",
        "vine_age": "60-100 years old",
        "made_in": "exceptional vintages only"
    }],
    deductive_profile={
        "nose": "dried rose, tar, liquorice, truffle, clay, old leather, camphor",
        "palate": "enormous tannin structure, concentrated, very long mineral finish",
        "signature": "extreme old-vine Nebbiolo concentration with traditional restraint"
    },
    service_specs={
        "temperature": "16-17C",
        "decanting": "4+ hours for young; allow 48h open in decanter",
        "aging": "optimal 15-40 years"
    },
    flavour_markers=["dried rose", "tar", "liquorice", "truffle", "clay", "camphor"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$500-$900",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barbaresco DOCG",
        "vineyard": "Crichet Paje — oldest vines in Paje"
    })

ceretto_bricco_rocche = PROD(cur, "Ceretto Barolo Bricco Rocche",
    category="wine_still", producer_id=ceretto, region_id=BAROLO,
    subcategory="red",
    description=(
        "Bricco Rocche is Ceretto's flagship Barolo from their own estate in Castiglione "
        "Falletto. The south-facing slope of Bricco Rocche is one of Barolo's most celebrated "
        "sites, producing a Barolo of exceptional density and balance. "
        "The modern Ceretto style uses barrique alongside large oak — richer and more "
        "immediately approachable than pure traditional wines but with genuine aging potential."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Bricco Rocche, Castiglione Falletto",
        "style": "modern-traditional balance",
        "aging_potential": "20-30 years"
    }],
    deductive_profile={
        "nose": "dark cherry, rose, vanilla (from barrique), tar, tobacco",
        "palate": "rich, modern, dense tannin, balanced acidity",
        "signature": "Castiglione Falletto density with modern oak integration"
    },
    service_specs={"temperature": "17C", "decanting": "2-3 hours", "aging": "8-25 years"},
    flavour_markers=["dark cherry", "rose", "vanilla", "tar", "tobacco"],
    flavour_weight="full",
    flavour_profile_type="tannic structured",
    price_tier="ultra_premium",
    price_range_cad="$280-$450",
    technical_specs={
        "grape": "Nebbiolo 100%",
        "appellation": "Barolo DOCG",
        "vineyard": "Bricco Rocche, Castiglione Falletto"
    })

print("\n=== PIEDMONT REFERENCES ===")

ref_barolo_crus = REF(cur,
    "Barolo DOCG — Commune Terroir and MGA (Menzione Geografica Aggiuntiva) System",
    category="wine_regions", skill_level="master",
    description=(
        "The 2010 Barolo regulations introduced the MGA system — 181 officially delimited "
        "single-vineyard classifications across 11 communes. Understanding the commune-level "
        "terroir differences is the foundation of serious Barolo navigation."
    ),
    key_principles=(
        "COMMUNE TERROIR MAP: "
        "SERRALUNGA D'ALBA: Helvetian limestone (compact, high Mg), poor drainage. "
        "Wines: extremely structured, austere, longest aging. Key crus: Falletto, Francia, Vigna Rionda. "
        "LA MORRA: Tortonian limestone-marl (loose, high Ca). "
        "Wines: floral, perfumed, more approachable. Key crus: Brunate, Cerequio, Rocche dell'Annunziata. "
        "BAROLO (commune): Tortonian + Helvetian mix. "
        "Wines: balanced between La Morra and Serralunga. Key crus: Cannubi, Sarmassa, Le Coste. "
        "CASTIGLIONE FALLETTO: Helvetian limestone, moderate altitude. "
        "Wines: structured but with aromatic lift. Key crus: Bricco Rocche, Monprivato, Villero. "
        "MONFORTE D'ALBA: Helvetian limestone, higher altitude. "
        "Wines: intense, structured, mineral. Key crus: Bussia, Ginestra, Mosconi. "
        "\nMGA HIERARCHY: "
        "MGA = officially classified single-vineyard (like Burgundy Premier Cru). "
        "An MGA label must include the vineyard name prominently. "
        "The MGA system distinguishes single-vineyard expressions from village blends. "
        "\nTHE BAROLO WARS (1980s-90s): "
        "Modernists (Elio Altare, Ceretto, Gaja): barrique, shorter maceration, approachable "
        "Traditionalists (Giacomo Conterno, Mascarello, Giacosa): Slavonian oak, long maceration "
        "Today the war has largely resolved — most producers use a combination; "
        "the real distinction is now about terroir expression, not oak."
    ),
    common_mistakes=(
        "Assuming Barolo from La Morra will age as long as Serralunga — it won't. "
        "Confusing Barolo Wars with quality — some traditionalists make mediocre wines; "
        "some modernists make extraordinary ones. "
        "Forgetting that Barbaresco (on Tortonian marl) is structurally closer to La Morra Barolo "
        "than to Serralunga."
    ),
    pro_tips=(
        "For blind tasting Nebbiolo: the tar-roses combination is unmistakable. "
        "Then ask: is it Barolo or Barbaresco? Barolo = more tannin, longer aging; "
        "Barbaresco = slightly more immediately expressive (Tortonian marl = faster development). "
        "Commune clue: if extremely austere and angular = likely Serralunga; "
        "if perfumed and floral = likely La Morra."
    ),
    authority_tier=1,
    source_text="Barolo MGA regulations (2010); Kerin O'Keefe 'Barolo and Barbaresco'; "
                "Ian d'Agata 'Native Wine Grapes of Italy'"
)

ref_nebbiolo_deductive = REF(cur,
    "Nebbiolo — Deductive Tasting Framework for Barolo and Barbaresco",
    category="deductive_method", skill_level="master",
    description=(
        "Nebbiolo is Italy's most structurally demanding grape and the source of Barolo and "
        "Barbaresco — Italy's greatest red wines. This reference provides the complete deductive "
        "framework for identifying and contextualising Nebbiolo in a blind tasting."
    ),
    key_principles=(
        "GRAPE FUNDAMENTALS: Nebbiolo ripens very late (late October), producing high acidity, "
        "high tannin, and relatively moderate colour (paler than Cabernet or Merlot). "
        "The paradox: pale colour but enormous structure. This is Nebbiolo's blind clue. "
        "\nAPPEARANCE: "
        "Pale garnet to ruby; browning rim develops quickly (5-8 years); by 15 years, "
        "significant orange-brick development. The pale colour misleads — this is not a light wine. "
        "\nNOSE: "
        "Young (1-8 years): rose, cherry, violets, tar, anise, subtle leather "
        "Developing (8-15 years): dried rose, tobacco, forest floor, truffle, camphor "
        "Mature (15+ years): dried flowers, balsam, orange peel, leather, camphor, tar "
        "THE TWO SIGNATURES: tar (from secondary fermentation compounds) + roses (from geraniol) "
        "\nPALATE: "
        "High acidity (above 5.5-6.5g/L in great years) "
        "High tannin (assertive but not coarse in quality examples) "
        "Medium-low concentration (paler than expected given tannin) "
        "Very long finish — the length is a key quality indicator "
        "\nBARRIQUE vs LARGE OAK: "
        "Barrique: toast, vanilla overlay; rounder tannin; more accessible young "
        "Large Slavonian: dried fruit, earth; more angular; demands longer aging "
        "\nBARBARESCO vs BAROLO: "
        "Barbaresco (Tortonian marl): slightly more approachable, floral, develops faster "
        "Barolo (Helvetian limestone, Tortonian marl mixture): more structured, longer lived "
        "\nWHEN STUCK IN A BLIND: Pale colour + high tannin + tar-rose = Nebbiolo. "
        "Then: is it young or old? Commune?"
    ),
    common_mistakes=(
        "Confusing Nebbiolo's pale colour with light-bodied wines — it is always full-bodied. "
        "Missing the orange-brick rim in older wines as a development clue. "
        "Calling tannin 'coarse' in a traditional wine — assertive tannin is intentional. "
        "Not giving enough time for the nose to open — Nebbiolo often needs 15-30 min in glass."
    ),
    pro_tips=(
        "The pale colour + massive structure paradox is Nebbiolo's greatest training tool. "
        "Great Barolo at 20 years smells like a library — tobacco, camphor, dried flowers, leather. "
        "Monfortino is the extreme of this aging curve: needs 20+ years to reveal its greatness."
    ),
    authority_tier=1,
    source_text="CMS Advanced Sommelier deductive method; WSET Diploma Unit 3; Barolo MGA reference materials"
)

print("\n=== PIEDMONT PAIRINGS ===")

PAIR(cur, "Tajarin al tartufo bianco — hand-cut egg pasta with white truffle",
     "rice_grains", "main",
     "classic", "complement",
     "The quintessential Piedmontese pairing. White truffle's earthy, garlic-honey intensity "
     "is a molecular mirror of aged Nebbiolo's tar-truffle-forest floor aromatics. "
     "Gaja Barbaresco's bright acidity and cherry freshness lifts the dish; "
     "the wine's structured tannin provides the frame.",
     gaja_barbaresco, food_flavour_profile="white truffle, egg pasta, butter, garlic", beverage_category="wine_still")

PAIR(cur, "Brasato al Barolo — beef braised in Barolo with root vegetables",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Brasato al Barolo is Piedmont's canonical meat dish. The braising wine should be Barolo; "
     "the drinking wine should be Barolo. Monfortino's extreme structure and tannin is softened "
     "by the collagen-rich braise; the dish's richness requires the wine's structural assertiveness.",
     conterno_monfortino, food_flavour_profile="braised beef, root vegetables, rich sauce, Barolo reduction", beverage_category="wine_still")

PAIR(cur, "Finanziera — offal and sweetbreads in Marsala with mushrooms",
     "wagyu_premium_protein", "starter",
     "established", "complement",
     "Finanziera (Turin's classic offal dish) has assertive flavours requiring an equally assertive wine. "
     "Bartolo Mascarello's traditional structure matches the dish's complexity; "
     "Nebbiolo's acid cuts through the richness.",
     mascarello_barolo, food_flavour_profile="organ meat, sweetbread, Marsala, mushroom", beverage_category="wine_still")

PAIR(cur, "Vitello tonnato — veal with tuna-caper sauce",
     "wagyu_premium_protein", "starter",
     "classic", "complement",
     "Vitello tonnato is a Piedmontese classic — the contrast pairing of delicate veal "
     "with punchy tuna mayo. Gaja Sori Tildin's aromatic complexity and balanced tannin "
     "works with both elements: the wine's fruit mirrors the veal; acidity cuts the tuna mayo.",
     gaja_sori_tildin, food_flavour_profile="delicate veal, tuna-caper mayo, capers, lemon", beverage_category="wine_still")

PAIR(cur, "Agnolotti del plin with meat broth and butter",
     "rice_grains", "main",
     "classic", "complement",
     "Agnolotti del plin (Piedmont's pinched-pasta dumplings filled with meat) in classic "
     "service — in broth (en brodo) or with just butter and sage. Vietti Castiglione's "
     "accessible structure and cherry-tar freshness is the everyday Barolo companion "
     "for this Piedmontese comfort dish.",
     vietti_castiglione, food_flavour_profile="meat-filled pasta, beef broth, butter", beverage_category="wine_still")

PAIR(cur, "Roast guinea fowl with Barolo reduction and porcini",
     "wagyu_premium_protein", "main",
     "established", "complement",
     "Guinea fowl's delicate, slightly gamy flavour is an ideal match for Vajra Bricco delle "
     "Viole's ethereal, violet-lifted Nebbiolo. The altitude and volcanic mineral of the vineyard "
     "creates a wine with elegant structure — not the brute force of Serralunga, "
     "but enough to support the roasted game.",
     vajra_bricco, food_flavour_profile="roasted guinea fowl, porcini, Barolo reduction", beverage_category="wine_still")

PAIR(cur, "Castelmagno cheese with chestnut honey and walnuts",
     "dairy_fermented", "cheese",
     "classic", "complement",
     "Castelmagno (a Piedmontese PDO hard cheese with blue veining) and Barolo is a canonical "
     "Piedmontese cheese pairing. The cheese's complex, crumbly richness and mild blue pungency "
     "is met by Giacosa Falletto's structured tannin and dried fruit character.",
     giacosa_falletto, food_flavour_profile="hard aged cheese, mild blue, chestnut honey, walnut", beverage_category="wine_still")

PAIR(cur, "Pasta al Barbaresco — pappardelle with Barbaresco and sausage ragu",
     "rice_grains", "main",
     "established", "complement",
     "Roagna Crichet Paje with wild boar or sausage ragu — the old-vine concentration "
     "and earthy complexity of the wine meets the gamey richness of Barbaresco-braised ragù. "
     "Regional cooking with regional wine: the perfection of terroir coherence.",
     roagna_crichet, food_flavour_profile="wild boar ragu, pappardelle, Barbaresco reduction", beverage_category="wine_still")

print("\n✅ Piedmont batch complete.")
cur.close()
conn.close()
