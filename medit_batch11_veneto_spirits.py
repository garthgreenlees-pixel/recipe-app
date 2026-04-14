#!/usr/bin/env python3
"""Batch 11+12 — Italian: Veneto (15 targets) + Italian Spirits: Grappa, Amaro, Limoncello (15 targets)
Veneto Producers: Dal Forno Romano, Quintarelli, Maculan, Pieropan, Allegrini
Veneto Products: Amarone Dal Forno, Amarone Quintarelli, Soave Classico Pieropan, Soave Calvarino,
                 Recioto Romeo, Valpolicella Allegrini
Italian Spirits Producers: Nonino, Nardini, Fernet-Branca, Limoncello di Capri, Montenegro
Italian Spirits Products: Nonino Monovitigno Grappa, Nardini Acquavite, Fernet-Branca,
                          Limoncello di Capri, Amaro Montenegro
References: Amarone and Appassimento; Grappa and Italian digestif culture
Pairings: risotto al Amarone, ossobuco, grana padano, tiramisu
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Veneto region IDs from batch1:
# Veneto=171, Amarone=172, Soave=173, Prosecco=174
VENETO = 171
AMARONE = 172
SOAVE = 173

# For Italian spirits — use Veneto (Grappa), Tuscany (Fernet), Campania (Limoncello)
# Tuscany=165 exists; need to use Veneto for Grappa producers
TUSCANY = 165

print("\n=== VENETO PRODUCERS ===")

dal_forno = P(cur, "Dal Forno Romano",
    producer_type="winery", region_id=AMARONE, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Dal Forno Romano in Illasi produces what many consider the most powerful and "
        "concentrated Amarone on earth. Romano Dal Forno is obsessive about quality: "
        "yields under 10 hl/ha, appassimento (drying) lasting 90+ days, aging in "
        "new French barriques for 4+ years. The wine is virtually impenetrable in youth — "
        "requiring 15-20 years minimum — but achieves extraordinary complexity at peak. "
        "Production is tiny; prices rival First Growth Bordeaux."
    ),
    key_personnel=["Romano Dal Forno", "Marco Dal Forno", "Luca Dal Forno"],
    production_details={
        "hectares": 25,
        "yields": "extremely low — under 10 hl/ha",
        "appassimento": "90+ days drying on bamboo racks",
        "oak": "new French barrique — 4+ years",
        "key_wines": ["Amarone della Valpolicella", "Valpolicella Superiore", "Monte Lodoletta"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Dal Forno Amarone is among the world's most powerful and expensive red wines. "
        "Extremely limited production; allocation through specialist importers only. "
        "The 1983 and 1990 vintages are legendary."
    ),
    allocation_notes="Ultra-allocation; BC importer [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

quintarelli = P(cur, "Giuseppe Quintarelli",
    producer_type="winery", region_id=AMARONE, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Giuseppe Quintarelli (1927-2012) was the most legendary figure in Valpolicella — "
        "the patriarch of Amarone. His estate in Cerè di Negrar produced wines of "
        "extraordinary complexity through the most traditional methods: the longest "
        "appassimento (3-5 months), aging in old Slavonian oak for up to 7 years, "
        "and no compromise. His Amarone Classico labels (some hand-dated by Quintarelli) "
        "are Italian wine legends. Son-in-law Francesco Dall'Omo and family continue."
    ),
    key_personnel=["Giuseppe Quintarelli (founder, d.2012)", "Francesco Dall'Omo (current)"],
    production_details={
        "hectares": 15,
        "appassimento": "3-5 months — longest in Valpolicella",
        "oak": "large Slavonian oak, 7 years for Amarone",
        "key_wines": ["Amarone Classico", "Recioto della Valpolicella Classico", "Primofiore"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Quintarelli Amarone is Italy's most mythologised wine — his hand-dated labels "
        "are collector items. The wines require 20+ years before peak."
    ),
    allocation_notes="Ultra-limited; BC importer [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

pieropan = P(cur, "Pieropan",
    producer_type="winery", region_id=SOAVE, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Leonildo Pieropan was the person most responsible for rescuing Soave Classico from "
        "mediocrity. In the 1970s, Soave had become a byword for cheap, industrial white wine. "
        "Pieropan demonstrated that old-vine Garganega from the volcanic basalt-limestone "
        "soils of the Classico zone could produce wines of genuine complexity and longevity. "
        "Their single-vineyard Calvarino (from 30+ year old vines) and La Rocca are benchmarks."
    ),
    key_personnel=["Leonildo Pieropan (founder)", "Teresita Pieropan", "Dario Pieropan", "Andrea Pieropan"],
    production_details={
        "hectares": 35,
        "key_wines": ["Soave Classico", "Calvarino (Garganega + Trebbiano di Soave)", "La Rocca"],
        "key_soils": "volcanic basalt-limestone (Classico zone)"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Pieropan is the reference producer for serious Soave Classico — the estate that "
        "proved the appellation could produce great white wine. Strong BC distribution."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

allegrini = P(cur, "Allegrini",
    producer_type="winery", region_id=AMARONE, country="Italy",
    production_philosophy="sustainable",
    philosophy_description=(
        "Allegrini is one of the most important estates in Valpolicella — bridging traditional "
        "quality (their Amarone is excellent) with modern single-vineyard focus. "
        "Their La Grola and La Poja (100% Corvina, unusual) IGT wines broke ground in the 1980s "
        "by proving Valpolicella grapes could make serious fresh wines without appassimento. "
        "Marilisa Allegrini has been instrumental in promoting Valpolicella globally."
    ),
    key_personnel=["Marilisa Allegrini", "Francesco Allegrini", "Corrado Allegrini"],
    production_details={
        "hectares": 75,
        "key_wines": ["Amarone della Valpolicella Classico", "La Poja (100% Corvina IGT)", "Soave La Grola"],
        "innovation": "La Poja — 100% Corvina without appassimento — ground-breaking"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Allegrini is one of Valpolicella's most internationally successful estates. "
        "Their Amarone is consistently excellent. Good BC availability."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== VENETO PRODUCTS ===")

dal_forno_amarone = PROD(cur, "Dal Forno Romano Amarone della Valpolicella",
    category="wine_still", producer_id=dal_forno, region_id=AMARONE,
    subcategory="red",
    description=(
        "Dal Forno Amarone is the most powerful Amarone produced — the apex of the "
        "appassimento technique. Made from Corvina, Corvinone, and Rondinella grapes "
        "dried for 90+ days, losing 40-50% of their weight and concentrating sugars "
        "to extraordinary levels. The resulting wine has 15-17% alcohol, massive tannin, "
        "and 50+ year aging potential. Impenetrable in youth — a 20-year project."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Amarone apex — most concentrated expression",
        "aging_potential": "40-60 years",
        "appassimento": "90+ days"
    }],
    deductive_profile={
        "appearance": "deep ruby-garnet, almost opaque",
        "nose": "dried cherry, fig, dark chocolate, tobacco, tar, leather, dried violets",
        "palate": "15-17% ABV; massive tannin; extraordinarily dense fruit concentration",
        "signature": "the most extreme and powerful Italian red — Amarone concentrated to maximum",
        "blind_clues": "very high ABV + dried fruit + massive tannin = Amarone; Dal Forno is the extreme"
    },
    service_specs={
        "temperature": "17-18C",
        "decanting": "4+ hours; or open 24 hours before serving",
        "aging": "minimum 15-20 years; optimal 30-40 years"
    },
    flavour_markers=["dried cherry", "fig", "dark chocolate", "tobacco", "tar", "dried violet"],
    flavour_weight="full",
    flavour_profile_type="rich dried fruit",
    price_tier="ultra_premium",
    price_range_cad="$600-$1000+",
    technical_specs={
        "grape": "Corvina 70%, Corvinone 20%, Rondinella 10%",
        "appellation": "Amarone della Valpolicella DOC",
        "appassimento": "90+ days",
        "abv": "15-17%"
    })

quintarelli_amarone = PROD(cur, "Giuseppe Quintarelli Amarone Classico",
    category="wine_still", producer_id=quintarelli, region_id=AMARONE,
    subcategory="red",
    description=(
        "Quintarelli Amarone Classico is among Italy's most mythologised wines. "
        "The legendary 3-5 month appassimento, followed by 7 years in large Slavonian oak, "
        "produces an Amarone of extraordinary complexity and longevity. "
        "Hand-dated bottles by Quintarelli himself are collector items. "
        "Unlike Dal Forno's power, Quintarelli's Amarone has more elegance and length — "
        "the traditional style at its highest expression."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "tier": "Traditional Amarone benchmark",
        "aging_potential": "40-60 years",
        "appassimento": "3-5 months"
    }],
    deductive_profile={
        "nose": "dried cherry, prune, tobacco, leather, cedar, forest floor, potpourri",
        "palate": "profound complexity, traditional structure, more elegant than Dal Forno",
        "signature": "Quintarelli subtlety — complexity over power; traditional at its pinnacle"
    },
    service_specs={
        "temperature": "17C",
        "decanting": "3-4 hours; old vintages pour direct carefully",
        "aging": "optimal 20-40 years"
    },
    flavour_markers=["dried cherry", "prune", "tobacco", "leather", "cedar", "forest floor"],
    flavour_weight="full",
    flavour_profile_type="rich dried fruit",
    price_tier="ultra_premium",
    price_range_cad="$500-$900",
    technical_specs={
        "grape": "Corvina, Corvinone, Rondinella, Molinara blend",
        "appellation": "Amarone della Valpolicella Classico DOC",
        "oak": "7 years large Slavonian oak"
    })

pieropan_calvarino = PROD(cur, "Pieropan Soave Classico Calvarino",
    category="wine_still", producer_id=pieropan, region_id=SOAVE,
    subcategory="white",
    description=(
        "Calvarino is Pieropan's landmark single-vineyard Soave — from 30+ year old Garganega "
        "and Trebbiano di Soave vines on the volcanic basalt soils of the Classico zone. "
        "It is the wine that proved Soave Classico could produce whites of genuine depth "
        "and 5-10 year aging potential. Almond-mineral, textured, with a bitter almond finish "
        "that is Garganega's signature."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "vineyard": "Calvarino — volcanic basalt, 30+ year old vines",
        "aging_potential": "8-12 years"
    }],
    deductive_profile={
        "nose": "almond, white peach, citrus blossom, chalk mineral, subtle volcanic stone",
        "palate": "medium body, textured, bitter almond finish, mineral length",
        "signature": "bitter almond + chalk mineral = Garganega from volcanic Soave Classico"
    },
    service_specs={"temperature": "10-12C", "aging": "5-10 years"},
    flavour_markers=["almond", "white peach", "citrus blossom", "chalk mineral", "volcanic stone"],
    flavour_weight="medium",
    flavour_profile_type="mineral-driven",
    price_tier="premium",
    price_range_cad="$65-$100",
    technical_specs={
        "grape": "Garganega 70%, Trebbiano di Soave 30%",
        "appellation": "Soave Classico DOC",
        "soil": "volcanic basalt-limestone"
    })

allegrini_amarone = PROD(cur, "Allegrini Amarone della Valpolicella Classico",
    category="wine_still", producer_id=allegrini, region_id=AMARONE,
    subcategory="red",
    description=(
        "Allegrini's Amarone Classico is one of the appellation's most consistent and "
        "food-friendly expressions. More approachable than Dal Forno or Quintarelli, "
        "it shows Amarone's essential dried fruit and chocolate character with slightly "
        "less austerity — an excellent introduction to the category."
    ),
    quality_tier="estate",
    quality_hierarchy=[{"tier": "Amarone Classico — accessible quality benchmark", "aging_potential": "15-25 years"}],
    deductive_profile={
        "nose": "dried cherry, chocolate, tobacco, leather, spice",
        "palate": "full body, rich dried fruit, firm tannin, long finish",
        "signature": "accessible Amarone — classic dried fruit character without extreme concentration"
    },
    service_specs={"temperature": "17C", "decanting": "2-3 hours", "aging": "8-20 years"},
    flavour_markers=["dried cherry", "chocolate", "tobacco", "leather", "spice"],
    flavour_weight="full",
    flavour_profile_type="rich dried fruit",
    price_tier="premium",
    price_range_cad="$120-$200",
    technical_specs={
        "grape": "Corvina 70%, Rondinella 30%",
        "appellation": "Amarone della Valpolicella Classico DOC"
    })

print("\n=== ITALIAN SPIRITS PRODUCERS ===")

nonino = P(cur, "Distillerie Nonino",
    producer_type="distillery", region_id=VENETO, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Nonino in Percoto (Friuli) transformed Italian grappa from a rough farm spirit "
        "into an elegant, respected digestif category. Giannola Nonino created the first "
        "single-varietal grappa in 1973 (ÙE — from Picolit grapes) and pioneered distilling "
        "fresh, moist pomace rather than dry pomace. Nonino Monovitigno grappas showcase "
        "the aromatic character of individual grape varieties — Moscato, Picolit, Merlot."
    ),
    key_personnel=["Giannola Nonino", "Antonella, Cristina, Elisabetta Nonino"],
    production_details={
        "location": "Percoto, Friuli-Venezia Giulia",
        "innovation": "first single-varietal grappa (1973 Picolit UE); fresh moist pomace distillation",
        "distillation": "bain-marie alembic stills (pot still, gentle heat)",
        "key_expressions": ["ÙE Monovitigno", "Grappa Il Prosecco", "Amaro Nonino Quintessentia"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Nonino is the reference producer for premium Italian grappa. Amaro Nonino "
        "Quintessentia is among Italy's most complex and celebrated amari. "
        "Strong BC distribution through specialty retailers."
    ),
    allocation_notes="BC — specialty retailers / agents",
    price_positioning="premium", authority_tier=1)

nardini = P(cur, "Bortolo Nardini",
    producer_type="distillery", region_id=VENETO, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Bortolo Nardini is Italy's oldest grappa house (founded 1779) — based in Bassano "
        "del Grappa, the Venetian town from which grappa takes its modern name. "
        "Their iconic Acquavite is a blend of multiple grape pomaces — a traditional, "
        "robust, and intensely aromatic grappa. The Nardini osteria at Ponte degli Alpini "
        "has served grappa to travellers since 1779."
    ),
    key_personnel=["Bortolo Nardini (founder)", "Primo Lorenzoni (current)"],
    production_details={
        "founded": 1779,
        "location": "Bassano del Grappa, Veneto",
        "style": "traditional Italian grappa — robust and aromatic",
        "key_expressions": ["Acquavite", "Riserva", "Mandorla (almond)"]
    },
    quality_tier="estate",
    reputation_narrative=(
        "Nardini is Italy's oldest and most historically significant grappa producer. "
        "The Acquavite is the benchmark for traditional Italian grappa style."
    ),
    allocation_notes="BC — specialty retailers",
    price_positioning="mid_range", authority_tier=1)

fernet_branca_producer = P(cur, "Fratelli Branca Distillerie",
    producer_type="distillery", region_id=TUSCANY, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Fernet-Branca was created by Bernardino Branca in Milan in 1845 as a medicinal "
        "bitters. The formula contains 27 botanicals including aloe, myrrh, rhubarb, "
        "gentian, chamomile, cardamom, saffron, and mint — macerated in neutral spirit "
        "for over 12 months and aged in oak for one year. "
        "The most bitter and complex of the major Italian amari; an acquired taste that "
        "has become globally ubiquitous in bartender culture."
    ),
    key_personnel=["Branca family"],
    production_details={
        "founded": 1845,
        "location": "Milan, Lombardy",
        "botanicals": "27 including aloe, myrrh, gentian, rhubarb, saffron, mint",
        "aging": "12 months maceration + oak aging"
    },
    quality_tier="market",
    reputation_narrative=(
        "Fernet-Branca is the most globally recognised Italian amaro. Essential knowledge "
        "for any bar program. Very strong BC distribution."
    ),
    allocation_notes="BC — wide distribution",
    price_positioning="mid_range", authority_tier=1)

amaro_montenegro_producer = P(cur, "Amaro Montenegro",
    producer_type="distillery", region_id=TUSCANY, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Amaro Montenegro was created in 1885 by Stanislao Cobianchi in Bologna, "
        "and named for Princess Elena of Montenegro (who married the King of Italy in 1896). "
        "It contains 40 botanicals including sweet orange peel, coriander, and vanilla, "
        "producing the sweetest and most accessible of Italy's major amari. "
        "The preferred amaro of bartenders seeking balance over extreme bitterness."
    ),
    key_personnel=["Stanislao Cobianchi (founder)"],
    production_details={
        "founded": 1885,
        "location": "Bologna, Emilia-Romagna",
        "botanicals": "40 including sweet orange, coriander, vanilla, dried herbs",
        "style": "sweeter, more approachable than Fernet"
    },
    quality_tier="market",
    reputation_narrative=(
        "Amaro Montenegro is the most food-friendly and accessible of Italy's major amari. "
        "Essential for classic cocktail and digestif service. Strong BC distribution."
    ),
    allocation_notes="BC — wide distribution",
    price_positioning="mid_range", authority_tier=1)

limoncello_producer = P(cur, "Limoncello di Capri",
    producer_type="distillery", region_id=TUSCANY, country="Italy",
    production_philosophy="conventional",
    philosophy_description=(
        "Limoncello di Capri is one of the most recognised producers of the Campanian "
        "lemon liqueur. True limoncello is made from the zest of Sfusato Amalfitano "
        "or Femminello lemons (large, intensely aromatic, grown on the Amalfi coast and "
        "Capri island) macerated in neutral spirit. The resulting liqueur is vivid yellow, "
        "intensely lemony, and served very cold as a digestif."
    ),
    key_personnel=["Capri family producers"],
    production_details={
        "location": "Capri, Campania",
        "lemon_variety": "Sfusato di Amalfi — large, aromatic Amalfi lemons",
        "method": "lemon zest maceration in neutral spirit",
        "style": "intensely lemony, sweet, served frozen"
    },
    quality_tier="market",
    reputation_narrative=(
        "Limoncello di Capri is the reference quality limoncello for restaurant service. "
        "Widely available in BC through specialty retailers."
    ),
    allocation_notes="BC — specialty retailers",
    price_positioning="mid_range", authority_tier=1)

print("\n=== ITALIAN SPIRITS PRODUCTS ===")

nonino_grappa = PROD(cur, "Nonino UE Grappa Monovitigno Moscato",
    category="spirits_liqueur", producer_id=nonino, region_id=VENETO,
    subcategory="grappa",
    description=(
        "Nonino ÙE Monovitigno Moscato is the definitive single-varietal grappa — distilled "
        "from fresh Moscato Giallo grape pomace using bain-marie pot stills. The aromatic "
        "intensity of Moscato is preserved in the grappa: rose, peach, orange blossom. "
        "This wine demonstrates that grappa can be as aromatic and refined as the finest "
        "eau-de-vie. Served chilled as a digestif."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{"tier": "Single-varietal grappa — Nonino pioneer expression"}],
    deductive_profile={
        "nose": "rose, peach, orange blossom, grape must, delicate spice",
        "palate": "smooth, aromatic, warming, dry finish with floral persistence",
        "signature": "Moscato florality preserved through distillation — grappa as perfume"
    },
    service_specs={
        "temperature": "10-14C (slightly chilled)",
        "glass": "tulip grappa glass or small white wine glass",
        "serving": "digestif after dinner; 30ml pour"
    },
    flavour_markers=["rose", "peach", "orange blossom", "grape must", "floral spice"],
    flavour_weight="medium",
    flavour_profile_type="floral aromatic spirit",
    price_tier="premium",
    price_range_cad="$80-$120",
    technical_specs={
        "spirit": "Grappa Monovitigno (single varietal)",
        "grape": "Moscato Giallo pomace",
        "abv": "41%",
        "distillation": "bain-marie pot still"
    })

fernet_branca = PROD(cur, "Fernet-Branca",
    category="spirits_liqueur", producer_id=fernet_branca_producer, region_id=TUSCANY,
    subcategory="amaro",
    description=(
        "Fernet-Branca is the world's most bitter and complex Italian amaro — 27 botanicals "
        "including aloe, myrrh, rhubarb, gentian, and mint. Intensely menthol on the nose; "
        "searing bitterness on the palate that transitions to a warm, digestive finish. "
        "An acquired taste that has become ubiquitous in global bartender culture "
        "(Calgary alone is one of the largest Fernet markets outside Italy). "
        "Traditionally served neat at room temperature, or with ginger ale (San Francisco style)."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "Most bitter of Italian amari — the bartender's benchmark"}],
    deductive_profile={
        "nose": "intense mint, menthol, bitter herbs, anise, dark spice",
        "palate": "extreme bitterness, then warming saffron-herb-tobacco complexity",
        "signature": "the most bitter legally sold amaro — the 'Marmite' of Italian spirits"
    },
    service_specs={
        "temperature": "room temperature or over ice",
        "uses": "digestif; bartender shot; cocktail modifier; Fernet and ginger ale",
        "pairing": "espresso coffee; dark chocolate"
    },
    flavour_markers=["mint", "menthol", "gentian", "saffron", "dark spice", "anise"],
    flavour_weight="full",
    flavour_profile_type="bitter herbal",
    price_tier="mid_range",
    price_range_cad="$45-$65",
    technical_specs={
        "spirit": "Amaro (bitters-based)",
        "botanicals": "27 including aloe, myrrh, rhubarb, gentian",
        "abv": "39%",
        "aging": "12 months oak"
    })

amaro_montenegro = PROD(cur, "Amaro Montenegro",
    category="spirits_liqueur", producer_id=amaro_montenegro_producer, region_id=TUSCANY,
    subcategory="amaro",
    description=(
        "Amaro Montenegro is the most balanced and food-friendly of Italy's major amari — "
        "40 botanicals with a sweet orange backbone, coriander, and vanilla that make it "
        "far more approachable than Fernet-Branca. The sweetness is well-balanced by gentle "
        "bitterness. An ideal introduction to Italian amaro culture and an excellent "
        "digestif recommmendation for guests who find Fernet too extreme."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "Most accessible of major Italian amari — sweet-bitter balance"}],
    deductive_profile={
        "nose": "sweet orange, vanilla, coriander, dried herbs, mild bitterness",
        "palate": "sweet entry, gentle bitterness, warm spice, clean finish",
        "signature": "the gateway amaro — sweet-bitter balance without Fernet's extremism"
    },
    service_specs={
        "temperature": "slightly chilled (12-14C)",
        "glass": "rocks glass with one large ice cube",
        "uses": "digestif; cocktail modifier (particularly in classics like Paper Plane)"
    },
    flavour_markers=["sweet orange", "vanilla", "coriander", "dried herb", "gentle bitter"],
    flavour_weight="medium",
    flavour_profile_type="sweet bitter herbal",
    price_tier="mid_range",
    price_range_cad="$45-$60",
    technical_specs={
        "spirit": "Amaro",
        "botanicals": "40 including sweet orange, coriander, vanilla",
        "abv": "23%"
    })

limoncello = PROD(cur, "Limoncello di Capri",
    category="spirits_liqueur", producer_id=limoncello_producer, region_id=TUSCANY,
    subcategory="limoncello",
    description=(
        "Limoncello di Capri is made from the zest of Sfusato di Amalfi lemons — "
        "large, intensely aromatic lemons grown on the Amalfi coast and Capri island. "
        "The zest is macerated in pure neutral spirit, then sweetened with simple syrup. "
        "Served frozen (from the freezer): the cold temperature preserves the aromatic "
        "intensity and creates the viscous, almost syrupy texture of proper limoncello."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "Reference quality limoncello from Amalfi lemon zest"}],
    deductive_profile={
        "nose": "intensely fresh lemon zest, candied peel, orange blossom, lemon flower",
        "palate": "sweet-tart, lemon oil intensity, viscous, clean finish",
        "signature": "Sfusato Amalfi lemon intensity — impossible to replicate without this variety"
    },
    service_specs={
        "temperature": "frozen (directly from freezer — -18 to -20C)",
        "glass": "frozen ceramic shot glass or chilled narrow glass",
        "serving": "50ml pour; digestif after seafood meals"
    },
    flavour_markers=["lemon zest", "candied peel", "lemon flower", "orange blossom"],
    flavour_weight="medium",
    flavour_profile_type="sweet citrus spirit",
    price_tier="mid_range",
    price_range_cad="$35-$55",
    technical_specs={
        "spirit": "Limoncello",
        "lemon": "Sfusato di Amalfi (Amalfi coast IGP)",
        "abv": "30%",
        "method": "zest maceration, not juice"
    })

nardini_acquavite = PROD(cur, "Nardini Acquavite di Vinaccia",
    category="spirits_liqueur", producer_id=nardini, region_id=VENETO,
    subcategory="grappa",
    description=(
        "Nardini Acquavite is the traditional Italian grappa — robust, intensely aromatic, "
        "and uncompromising. Made from a blend of grape pomace (primarily from Prosecco "
        "and Veneto varieties), it represents the historic style of Italian grappa before "
        "Nonino's refinement: powerful, rough-edged, and deeply flavourful. "
        "Served at room temperature in the traditional Venetian manner."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "Traditional Italian grappa benchmark — Italy's oldest producer"}],
    deductive_profile={
        "nose": "grape must, spice, earthy, robust floral, slight astringency",
        "palate": "warming, robust, grape character, long bitter finish",
        "signature": "traditional Italian grappa — less refined than Nonino but authentic"
    },
    service_specs={
        "temperature": "room temperature or slightly warm",
        "glass": "traditional Venetian grappa glass (small, narrow)",
        "uses": "caffe corretto (grappa in espresso); digestif"
    },
    flavour_markers=["grape must", "spice", "earthy", "robust floral"],
    flavour_weight="full",
    flavour_profile_type="robust spirit",
    price_tier="mid_range",
    price_range_cad="$40-$65",
    technical_specs={
        "spirit": "Grappa (acquavite di vinaccia)",
        "grape": "Veneto pomace blend",
        "abv": "40%",
        "style": "traditional — not single-varietal"
    })

print("\n=== VENETO & ITALIAN SPIRITS REFERENCES ===")

ref_amarone = REF(cur,
    "Amarone della Valpolicella — Appassimento Technique and Style Spectrum",
    category="wine_knowledge", skill_level="advanced",
    description=(
        "Amarone is Italy's most unusual great red wine — made from dried grapes. "
        "Understanding the appassimento (drying) technique, the DOCG regulations, "
        "and the style spectrum from traditional to modern is essential for confident service."
    ),
    key_principles=(
        "APPASSIMENTO TECHNIQUE: "
        "Corvina, Corvinone, Rondinella, and Molinara grapes are harvested in October "
        "and dried on bamboo racks (arele) or in special drying lofts (fruttai) for 90-120 days. "
        "During drying, grapes lose 30-40% of their weight, concentrating sugars, acids, and flavours. "
        "The dried grapes are pressed in January-February; fermentation is slow and difficult. "
        "\nSTYLE SPECTRUM: "
        "TRADITIONAL (Quintarelli, Allegrini): large Slavonian oak, 6-8 years aging; "
        "more complex, savory, requires 15-25 years. "
        "MODERN (Dal Forno, some Bertani): new French barriques, more opulent fruit; "
        "earlier approachability but similar longevity. "
        "\nAMARONE vs RECIOTO vs VALPOLICELLA: "
        "All use appassimento but differ in fermentation completion: "
        "AMARONE: fermented fully dry (15-17% ABV); the 'bitter' wine (amaro = bitter) "
        "RECIOTO: fermented partially; residual sugar remaining; the 'sweet' Amarone "
        "VALPOLICELLA RIPASSO: fresh Valpolicella wine re-fermented on Amarone pomace — "
        "middle ground: more richness than fresh Valpolicella, less than Amarone "
        "\nSERVICE: Amarone's power (15-17% ABV) makes portion control important. "
        "60-90ml pours rather than 150ml. Decant 2-4 hours. "
        "Avoid pairing with delicate foods — requires substantial, rich dishes."
    ),
    common_mistakes=(
        "Serving Amarone too young — Dal Forno requires 15 years minimum. "
        "Recommending Ripasso as a substitute for Amarone (explain the difference). "
        "Over-pouring (standard 150ml pour of 16% ABV wine is too much). "
        "Confusing Recioto (sweet) with Amarone (dry)."
    ),
    pro_tips=(
        "The key appassimento clue in the glass: dried fruit aromatics (raisin, prune, fig) "
        "combined with very high ABV. No other Italian wine has this combination. "
        "Allegrini's Amarone is the ideal introduction — slightly less extreme than Dal Forno "
        "but showing the essential dried-fruit character of the category."
    ),
    authority_tier=1,
    source_text="Consorzio Vini Valpolicella; WSET Diploma Unit 3; Ian d'Agata 'Native Wine Grapes of Italy'"
)

ref_grappa_amaro = REF(cur,
    "Grappa, Amaro, and Italian Digestif Culture — Service Guide",
    category="spirits_knowledge", skill_level="advanced",
    description=(
        "The Italian digestif culture spans grappa (pomace brandy), amaro (bitter herbal liqueur), "
        "limoncello (lemon zest liqueur), and sambuca (anise). Understanding the category "
        "distinctions, key producers, and service logic is essential for any program "
        "with Italian wine or food focus."
    ),
    key_principles=(
        "GRAPPA: "
        "Distilled from grape pomace (solid remains after pressing — skins, seeds, stems). "
        "Must be produced in Italy from Italian grapes. "
        "Traditional style: robust, rough-edged, earthy (Nardini). "
        "Modern style: single-varietal, aromatic, refined (Nonino Monovitigno). "
        "Best grappas: Nonino (Monovitigno range), Romano Levi (hand-labeled, artisanal), "
        "Poli, Maschio. "
        "Service: traditional = room temperature; refined = slightly chilled (12-14C). "
        "\nAMARO: "
        "Bitter herbal liqueur with varying levels of sweetness. Made from herbs, roots, "
        "bark, citrus peel, and spices macerated in spirit. Served as digestif. "
        "Category spectrum by bitterness: "
        "Sweet/mild: Montenegro (23%), Aperol (11%), Averna. "
        "Moderate: Campari (25%), Ramazzotti, Cynar (artichoke). "
        "Intense: Fernet-Branca (39%), Braulio (21%), Sfumato Rabarbaro. "
        "Classic cocktail use: Negroni (Campari), Paper Plane (Montenegro/Aperol), "
        "Boulevardier, Black Manhattan. "
        "\nLIMONCELLO: "
        "Made from lemon zest (not juice) macerated in neutral spirit. "
        "Must use Sorrento/Amalfi IGP lemons for quality expression. "
        "Serve frozen — from the freezer — to achieve proper viscosity and cold service. "
        "\nCAFFE CORRETTO: "
        "Traditional Italian tradition — espresso 'corrected' with a small pour of grappa. "
        "A sommelier opportunity: suggest the correcto with the post-meal coffee."
    ),
    common_mistakes=(
        "Serving limoncello warm — must be frozen. "
        "Recommending Fernet-Branca to a guest who has never had amaro — too extreme as intro. "
        "Not knowing that Aperol is an amaro (liqueur), not a wine. "
        "Confusing grappa (pomace) with brandy (wine)."
    ),
    pro_tips=(
        "The progression for introducing amaro to a new guest: "
        "Aperol Spritz → Amaro Montenegro neat → Averna → Fernet-Branca. "
        "Build up to the most intense over multiple visits. "
        "Nonino Amaro Quintessentia is the ideal gateway for wine-focused guests — "
        "more complex than Montenegro but made from wine spirit rather than grain."
    ),
    authority_tier=1,
    source_text="CMS spirits curriculum; Difford's Guide to Cocktails; Nonino distillery documentation"
)

print("\n=== VENETO & SPIRITS PAIRINGS ===")

PAIR(cur, "Risotto al Amarone with Parmigiano and black truffle",
     "rice_grains", "main",
     "classic", "complement",
     "The quintessential Amarone pairing — risotto made with Amarone wine, finished with "
     "Parmigiano. Dal Forno's concentration matches the intensity of the Amarone reduction "
     "in the risotto; the truffle echoes the wine's earthy dried fruit notes.",
     dal_forno_amarone, food_flavour_profile="Amarone reduction, risotto, truffle, Parmigiano", beverage_category="wine_still")

PAIR(cur, "Ossobuco alla Milanese with gremolata and saffron risotto",
     "wagyu_premium_protein", "main",
     "classic", "complement",
     "Ossobuco (braised veal shank) with saffron risotto is one of Italy's great ragout dishes. "
     "Quintarelli Amarone's complex dried fruit and tobacco character provides the necessary "
     "weight and depth to match the collagen richness of braised veal shanks.",
     quintarelli_amarone, food_flavour_profile="braised veal shank, saffron risotto, gremolata", beverage_category="wine_still")

PAIR(cur, "Baccala mantecato on polenta crostini",
     "seafood_general", "starter",
     "established", "complement",
     "Salt cod whipped with olive oil and garlic (baccala mantecato) is a Venetian classic. "
     "Pieropan Calvarino's almond-mineral character and medium body works with the "
     "salt-olive oil richness of baccala without overpowering the delicate cod.",
     pieropan_calvarino, food_flavour_profile="salt cod, olive oil, garlic, polenta", beverage_category="wine_still")

PAIR(cur, "Tiramisu — espresso, mascarpone, Marsala, savoiardi",
     "chocolate_confection", "dessert",
     "classic", "complement",
     "Tiramisu with a grappa digestif is the canonical Venetian ending. "
     "Nonino Moscato grappa's rose-peach florality complements the mascarpone cream "
     "and espresso bitterness; the grappa cuts through the sweetness.",
     nonino_grappa, food_flavour_profile="mascarpone, espresso, chocolate, savoiardi", beverage_category="spirits_liqueur")

PAIR(cur, "Spaghetti alle vongole with bottarga and olive oil",
     "seafood_general", "main",
     "classic", "complement",
     "Vongole (clam pasta) with bottarga (cured mullet roe) is the great Italian seafood pasta. "
     "Pieropan Soave Calvarino's almond-mineral character and saline minerality "
     "mirrors the seafood's brine while the almond note echoes the bottarga.",
     allegrini_amarone, food_flavour_profile="clams, bottarga, olive oil, white wine, parsley", beverage_category="wine_still")

PAIR(cur, "Grana Padano 36 months with mostarda di frutta",
     "dairy_fermented", "cheese",
     "established", "complement",
     "Grana Padano at 36 months (salty-crystalline-nutty) with mostarda di frutta "
     "(fruit in mustard syrup) is a Northern Italian classic. Amaro Montenegro's "
     "sweet-bitter balance and orange peel character harmonises with both elements.",
     amaro_montenegro, food_flavour_profile="aged hard cheese, crystalline salt, sweet-spicy fruit mustard", beverage_category="spirits_liqueur")

PAIR(cur, "Panna cotta with Amalfi lemon curd and limoncello drizzle",
     "dairy_fermented", "dessert",
     "classic", "complement",
     "Limoncello di Capri over panna cotta — the perfect Southern Italian dessert ending. "
     "The frozen limoncello drizzled over the cold cream creates temperature contrast "
     "while the lemon intensity cuts through the cream's richness.",
     limoncello, food_flavour_profile="panna cotta cream, lemon curd, sugar", beverage_category="spirits_liqueur")

PAIR(cur, "Caffe corretto — espresso with grappa",
     "chocolate_confection", "digestif",
     "classic", "complement",
     "The traditional Venetian caffe corretto — espresso 'corrected' with a small pour "
     "of Nardini Acquavite. The bitter espresso and the robust grape character of traditional "
     "grappa create a Northern Italian morning or evening ritual.",
     nardini_acquavite, food_flavour_profile="espresso, bitter, dark roast", beverage_category="spirits_liqueur")

print("\n✅ Veneto + Italian Spirits batch complete.")
cur.close()
conn.close()
