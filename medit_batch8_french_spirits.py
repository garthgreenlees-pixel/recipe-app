#!/usr/bin/env python3
"""Batch 8 — French Spirits: Cognac, Armagnac, Calvados, Pastis (25 targets)
Producers: Remy Martin, Hennessy, Delamain, Hine, Darroze, Castarede, Domaine du Tariquet,
           Domaine Dupont, Calvados Lemorton, Ricard, Henri Bardouin
Products: Remy Martin XO, Louis XIII, Hennessy Paradis, Delamain Pale & Dry, Hine Antique,
          Darroze 10yr Armagnac, Castarede 1989 Armagnac, Dupont Calvados VSOP,
          Lemorton Domfrontais, Ricard Pastis, Henri Bardouin Pastis, Noilly Prat
References: Cognac Crus and Aging; Armagnac vs Cognac; Calvados Appellations; Pastis anethole
Protocols: Spirit service at table
"""
import sys
sys.path.insert(0, "/Users/garthgreenlees/Desktop/provenance-tester-1")
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

COGNAC = 156
ARMAGNAC = 157
NORMANDY = 158
ALSACE = 155  # for Ricard/Pastis (no Provence region in our regions, use Alsace)
# Provence not in our region set — use COGNAC as a placeholder and set country correctly
# Actually let's check: we inserted Morocco=183, Turkey=184, Cognac=156, Armagnac=157, Normandy=158, Provence=159
PROVENCE = 159

print("\n=== COGNAC PRODUCERS ===")

remy_martin = P(cur, "Remy Martin",
    producer_type="distillery", region_id=COGNAC, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Remy Martin is unique among the major Cognac houses in using exclusively Grande Champagne "
        "and Petite Champagne grapes (their 'Fine Champagne' designation). This focus on the "
        "two best crus gives their Cognacs the chalky mineral complexity and exceptional "
        "aging potential that distinguishes them from house blends using lesser crus. "
        "Founded 1724; the house is the reference for 'Fine Champagne' style Cognac."
    ),
    key_personnel=["Baptiste Loiseau (cellar master)"],
    production_details={
        "founded": 1724,
        "crus": "exclusively Grande Champagne and Petite Champagne (Fine Champagne blend)",
        "grape": "Ugni Blanc (primary), Colombard, Folle Blanche",
        "distillation": "Charentais alembic pot still, double distillation",
        "key_expressions": ["VSOP", "XO", "Louis XIII"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "One of the four major Cognac houses (with Hennessy, Courvoisier, Martell). "
        "Distinguished by Fine Champagne quality focus. Louis XIII is the apex — a blend "
        "of up to 1,200 eaux-de-vie aged 40-100+ years."
    ),
    allocation_notes="BC — Mark Anthony Group [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

hennessy = P(cur, "Hennessy",
    producer_type="distillery", region_id=COGNAC, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Hennessy is the world's largest Cognac house (founded 1765 by Richard Hennessy, "
        "an Irish officer in the French army) and is responsible for approximately 40% of "
        "global Cognac sales. Part of LVMH since 1987. The house uses all Cognac crus and "
        "maintains enormous stocks — the Paradis cellar holds an estimated 350,000 eaux-de-vie. "
        "Their master blender tradition is the foundation of house consistency."
    ),
    key_personnel=["Renaud Fillioux de Gironde (cellar master — 8th generation)"],
    production_details={
        "founded": 1765,
        "ownership": "LVMH",
        "production": "largest Cognac producer — approx 40% global share",
        "cellar": "Paradis — 350,000+ eaux-de-vie",
        "key_expressions": ["VS", "VSOP", "XO", "Paradis", "Richard Hennessy"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "The reference point for Cognac globally. Paradis is extraordinary; XO is the benchmark "
        "for the category. Strong BC distribution."
    ),
    allocation_notes="BC — Mark Anthony Group / broad distribution",
    price_positioning="ultra_premium", authority_tier=1)

delamain = P(cur, "Delamain",
    producer_type="distillery", region_id=COGNAC, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Delamain is the antithesis of the large Cognac houses: a small, specialist négociant "
        "that focuses exclusively on Grande Champagne, aged to a minimum 20 years before release, "
        "and never coloured or sweetened. Their Pale & Dry XO is the benchmark for the "
        "'Grand Champagne' house style — delicate, floral, aristocratic. "
        "Founded 1824; family-owned; extraordinarily consistent quality."
    ),
    key_personnel=["Charles Braastad-Delamain"],
    production_details={
        "founded": 1824,
        "cru": "exclusively Grande Champagne",
        "minimum_age": "20 years before release",
        "additions": "no colouring, no sweetening (boisé)",
        "key_expressions": ["Pale & Dry XO", "Vesper", "Tres Venerable"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Delamain is the sommelier's Cognac — elegant, dry, unadorned. Pale & Dry is the "
        "reference for Grande Champagne style. Boutique allocation through specialist importers."
    ),
    allocation_notes="BC — Select Wine Merchants / agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

hine = P(cur, "Hine Cognac",
    producer_type="distillery", region_id=COGNAC, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Hine is a specialist Grande Champagne house founded by Thomas Hine (an English merchant) "
        "in 1817 in Jarnac. The house is known for early-landing Cognacs — spirits shipped in "
        "cask to Bristol for aging in the cooler, damp English climate, which imparts unique "
        "delicacy and restraint. Hine Antique XO is the benchmark for this style. "
        "Now owned by CL Financial; quality has remained high."
    ),
    key_personnel=["Eric Forget (cellar master)"],
    production_details={
        "founded": 1817,
        "specialty": "early-landing Cognacs — aged in Bristol, England",
        "cru": "primarily Grande Champagne",
        "key_expressions": ["Antique XO", "Homage", "Triomphe"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Hine's early-landing specialty produces uniquely delicate, English-style Cognacs "
        "with more restraint than French-aged equivalents. Antique XO is a sommelier favourite."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

print("\n=== ARMAGNAC PRODUCERS ===")

darroze = P(cur, "Francis Darroze",
    producer_type="distillery", region_id=ARMAGNAC, country="France",
    production_philosophy="natural",
    philosophy_description=(
        "Francis Darroze is the premier single-estate Armagnac négoce — selecting, aging, "
        "and bottling Armagnacs from individual farmhouse distillers across Bas-Armagnac. "
        "Rather than blending, each bottling is labeled with the producer's name, vintage, "
        "and appellation. Darroze single-estate Armagnacs — often from obscure family farms "
        "— represent Armagnac at its most terroir-expressive and authentic."
    ),
    key_personnel=["Francis Darroze", "Marc Darroze"],
    production_details={
        "model": "single-estate négociant — buys and ages from individual farms",
        "appellation": "Bas-Armagnac (primary)",
        "distillation": "continuous Armagnac alembic (Armagnacais)",
        "key_grapes": ["Baco Blanc", "Ugni Blanc", "Colombard", "Folle Blanche"],
        "bottling": "vintage-dated, single-estate, no additions"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Darroze is the reference for serious Armagnac connoisseurship. Single-estate, "
        "vintage-dated bottlings from farms like Domaine de Millet and Domaine de Rimaison "
        "are extraordinary. Strong reputation among sommeliers globally."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="ultra_premium", authority_tier=1)

castarede = P(cur, "Castarede Armagnac",
    producer_type="distillery", region_id=ARMAGNAC, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Castarede is one of Armagnac's oldest houses (founded 1832) and the oldest family-owned "
        "Armagnac négociant still in operation. Based in Lavardac in Bas-Armagnac, they specialise "
        "in aged, vintage-dated Armagnacs. Their vintage-specific releases dating back to the 1950s "
        "are legendary — a direct connection to Armagnac's history as France's oldest distilled spirit."
    ),
    key_personnel=["Florence Castarede"],
    production_details={
        "founded": 1832,
        "appellation": "Bas-Armagnac",
        "specialty": "vintage-dated single-year releases — back to 1950s",
        "key_expressions": ["VSOP", "vintage releases (1960, 1970, 1980, 1990, 2000)"]
    },
    quality_tier="estate",
    reputation_narrative=(
        "Castarede is a historic Armagnac house with strong vintage collections. "
        "Good value relative to Cognac at equivalent age. Good BC agent availability."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== CALVADOS PRODUCERS ===")

dupont = P(cur, "Domaine Dupont",
    producer_type="distillery", region_id=NORMANDY, country="France",
    production_philosophy="biodynamic",
    philosophy_description=(
        "Domaine Dupont in Victot-Pontfol is the reference producer for Pays d'Auge Calvados — "
        "Normandy's premier appellation requiring double distillation in pot stills (as opposed "
        "to continuous column stills). Jérôme Dupont farms the orchards organically and uses "
        "over 60 apple varieties in the blend. Their VSOP and Hors d'Age expressions are "
        "benchmarks for complex, food-friendly Calvados."
    ),
    key_personnel=["Jerome Dupont"],
    production_details={
        "appellation": "Calvados Pays d'Auge (POD requiring pot still double distillation)",
        "apple_varieties": "60+ traditional Norman varieties",
        "farming": "organic, biodynamic approach",
        "key_expressions": ["VSOP", "Hors d'Age", "Selection", "Réserve"]
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Domaine Dupont is the sommelier's Calvados of choice — complex, terroir-expressive, "
        "and genuinely food-friendly. Hors d'Age (10+ years) rivals fine Cognac in complexity."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

lemorton = P(cur, "Distillerie Lemorton",
    producer_type="distillery", region_id=NORMANDY, country="France",
    production_philosophy="natural",
    philosophy_description=(
        "Domaine Lemorton in Domfront produces Calvados Domfrontais — the only Calvados "
        "appellation that requires a minimum of 30% pear spirit (made from Perry pears). "
        "This pear-dominant style produces a lighter, more floral Calvados than Pays d'Auge. "
        "Lemorton is the benchmark for this style — their 15-year expression is extraordinary."
    ),
    key_personnel=["Remi Lemorton"],
    production_details={
        "appellation": "Calvados Domfrontais (min 30% pear)",
        "distillation": "continuous column still (permitted in this appellation)",
        "key_expressions": ["15 Years", "1989", "1978"],
        "pear_varieties": "local perry pears"
    },
    quality_tier="reserve",
    reputation_narrative=(
        "Lemorton is the reference for pear-forward Calvados Domfrontais. "
        "Their aged expressions are sought by collectors and bartenders alike."
    ),
    allocation_notes="BC — agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

ricard_producer = P(cur, "Ricard — Pernod Ricard",
    producer_type="distillery", region_id=PROVENCE, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Ricard was invented by Paul Ricard in 1932 after the French government legalised "
        "anise spirits (absinthe had been banned since 1915). His formula — star anise, "
        "liquorice root, Provencal herbs — became the best-selling pastis in France and "
        "one of the best-selling spirits in the world. The brand merged with Pernod in 1975 "
        "to form Pernod Ricard. Ricard is the archetype of the pastis category."
    ),
    key_personnel=["Paul Ricard (founder)"],
    production_details={
        "founded": 1932,
        "key_botanicals": "star anise, liquorice root, Provencal herbs",
        "alcohol": "45% ABV",
        "style": "louche spirit — turns milky when diluted with water"
    },
    quality_tier="market",
    reputation_narrative=(
        "Ricard is the benchmark pastis — the standard against which all others are judged. "
        "Essential knowledge for any sommelier working with aperitif service. "
        "Very wide BC distribution."
    ),
    allocation_notes="BC — wide distribution; Pernod Ricard Canada",
    price_positioning="mid_range", authority_tier=1)

bardouin_producer = P(cur, "Henri Bardouin",
    producer_type="distillery", region_id=PROVENCE, country="France",
    production_philosophy="conventional",
    philosophy_description=(
        "Henri Bardouin is the artisanal counterpart to Ricard — a small-production pastis "
        "from Forcalquier in the Haute-Provence using 65 botanicals from the surrounding "
        "landscape (wild herbs, flowers, spices). More complex, less sweet, and more "
        "herbaceous than Ricard. The preferred pastis of sommeliers and serious cocktail bars."
    ),
    key_personnel=["Henri Bardouin (founder)"],
    production_details={
        "location": "Forcalquier, Haute-Provence",
        "botanicals": "65+ wild Provencal herbs including thyme, rosemary, savory, lavender",
        "alcohol": "45% ABV",
        "style": "artisanal — more herbal complexity than industrial pastis"
    },
    quality_tier="estate",
    reputation_narrative=(
        "Henri Bardouin is the sommelier's pastis — more complex, less sweet, and more "
        "authentically Provencal than Ricard. Available through specialty liquor retailers."
    ),
    allocation_notes="BC — specialty retailers / agents [NEEDS VERIFICATION]",
    price_positioning="premium", authority_tier=1)

print("\n=== SPIRITS PRODUCTS ===")

remy_xo = PROD(cur, "Remy Martin XO Excellence",
    category="spirits_brandy", producer_id=remy_martin, region_id=COGNAC,
    subcategory="cognac",
    description=(
        "Remy Martin XO Excellence is a blend of over 400 Grande Champagne and Petite Champagne "
        "eaux-de-vie aged 10-37 years. The Fine Champagne designation guarantees chalky mineral "
        "complexity from the Grande Champagne cru. Luscious on the palate with rancio (oxidative "
        "nutty) complexity, dried fruit concentration, and remarkably long finish."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "age": "10-37 years (blend)",
        "cru": "Fine Champagne (Grande + Petite Champagne)",
        "designation": "XO"
    }],
    deductive_profile={
        "nose": "dried fig, prune, orange peel, vanilla, cinnamon, rancio nut, subtle floral",
        "palate": "luscious, full body, oak spice, dried fruit, very long chalk-mineral finish",
        "signature": "Fine Champagne chalk mineral — distinctive from other crus"
    },
    service_specs={
        "glass": "tulip-shaped Cognac glass (NOT snifter)",
        "temperature": "room temperature or slightly cooler (18-20C)",
        "service": "no ice; serve neat; no water addition"
    },
    flavour_markers=["dried fig", "prune", "orange peel", "vanilla", "rancio", "chalk mineral"],
    flavour_weight="full",
    flavour_profile_type="rich aged spirit",
    price_tier="ultra_premium",
    price_range_cad="$280-$380",
    technical_specs={
        "spirit": "Cognac Fine Champagne XO",
        "abv": "40%",
        "age": "10-37 years",
        "crus": "Grande Champagne + Petite Champagne"
    })

delamain_pale_dry = PROD(cur, "Delamain Pale and Dry XO Grande Champagne",
    category="spirits_brandy", producer_id=delamain, region_id=COGNAC,
    subcategory="cognac",
    description=(
        "Delamain Pale & Dry is the benchmark for Grande Champagne Cognac in its purest expression. "
        "Minimum 20 years in Limousin oak; no caramel colour; no boisé (oak extract) addition. "
        "The pale gold colour is natural — from the spirit itself, not addition. "
        "Lighter, more floral, and more delicate than most XOs; extraordinary finesse and length."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "age": "minimum 20 years",
        "cru": "Grande Champagne exclusively",
        "additions": "none — no colour, no sweetening"
    }],
    deductive_profile={
        "appearance": "pale gold — natural colour from aging alone",
        "nose": "jasmine, rose, dried apricot, chalk mineral, light vanilla, very subtle rancio",
        "palate": "extremely elegant, dry finish, long floral-mineral length",
        "signature": "the driest and most elegant XO — the sommelier's choice"
    },
    service_specs={
        "glass": "tulip cognac glass",
        "temperature": "18-20C",
        "serving": "neat; 30-40ml pour; allow to open 2-3 minutes"
    },
    flavour_markers=["jasmine", "rose", "dried apricot", "chalk mineral", "vanilla", "floral"],
    flavour_weight="medium-full",
    flavour_profile_type="elegant aged spirit",
    price_tier="ultra_premium",
    price_range_cad="$300-$450",
    technical_specs={
        "spirit": "Cognac Grande Champagne XO",
        "abv": "40%",
        "age": "minimum 20 years",
        "additions": "none"
    })

hine_antique = PROD(cur, "Hine Antique XO Premier Cru",
    category="spirits_brandy", producer_id=hine, region_id=COGNAC,
    subcategory="cognac",
    description=(
        "Hine Antique XO is a Grande Champagne Cognac aged partly in the early-landing tradition "
        "— shipped in cask to Bristol for aging in England's cooler, more humid climate. "
        "This produces a uniquely delicate, flower-forward Cognac with less oak influence "
        "than French-aged equivalents. The result is refined, light, and extraordinarily aromatic."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "specialty": "early-landing — partly aged in Bristol, England",
        "cru": "Grande Champagne",
        "aging": "minimum 10 years"
    }],
    deductive_profile={
        "nose": "jasmine, white rose, dried peach, light rancio, chalk, very subtle oak",
        "palate": "light body, delicate, floral, long mineral finish",
        "signature": "the most English of Cognacs — delicate and flower-forward"
    },
    service_specs={"glass": "tulip cognac glass", "temperature": "room temperature"},
    flavour_markers=["jasmine", "white rose", "dried peach", "chalk", "light rancio"],
    flavour_weight="medium",
    flavour_profile_type="elegant aged spirit",
    price_tier="ultra_premium",
    price_range_cad="$250-$380",
    technical_specs={
        "spirit": "Cognac Grande Champagne XO",
        "abv": "40%",
        "specialty": "early-landing aged in Bristol"
    })

darroze_10yr = PROD(cur, "Francis Darroze Bas-Armagnac 10 Year",
    category="spirits_brandy", producer_id=darroze, region_id=ARMAGNAC,
    subcategory="armagnac",
    description=(
        "Darroze's entry-level single-estate expression showcases the house's philosophy: "
        "single-estate, unblended Armagnac from Bas-Armagnac, distilled in the traditional "
        "continuous Armagnacais alembic. The 10-year version shows Armagnac's essential "
        "character — more rustic and powerful than Cognac, with distinctive prune-black pepper "
        "and earthy notes. Often sourced from a single named farmhouse estate."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "model": "single-estate Bas-Armagnac",
        "age": "10 years",
        "appellation": "Bas-Armagnac"
    }],
    deductive_profile={
        "nose": "prune, dried plum, black pepper, earthy, tobacco, dark chocolate",
        "palate": "more structured and rustic than Cognac, rich dark fruit, long peppery finish",
        "signature": "Armagnac earthiness — prune + black pepper is the telltale blind cue"
    },
    service_specs={"glass": "tulip spirit glass", "temperature": "room temperature"},
    flavour_markers=["prune", "dried plum", "black pepper", "earthy", "tobacco", "dark chocolate"],
    flavour_weight="full",
    flavour_profile_type="robust aged spirit",
    price_tier="premium",
    price_range_cad="$120-$180",
    technical_specs={
        "spirit": "Armagnac Bas-Armagnac",
        "distillation": "Armagnacais continuous alembic",
        "abv": "43-48%",
        "age": "10 years"
    })

dupont_vsop = PROD(cur, "Domaine Dupont Calvados Pays d'Auge VSOP",
    category="spirits_brandy", producer_id=dupont, region_id=NORMANDY,
    subcategory="calvados",
    description=(
        "Dupont VSOP is a minimum 4-year Calvados Pays d'Auge — France's premier Calvados "
        "appellation requiring double distillation in pot stills from 100% Norman apples. "
        "The VSOP shows the essential Calvados character: fresh apple and baked apple, "
        "warming wood spice from Limousin oak, and the characteristic cream-butter texture "
        "of Pays d'Auge. A reference for the category."
    ),
    quality_tier="estate",
    quality_hierarchy=[{
        "appellation": "Calvados Pays d'Auge — premier appellation",
        "distillation": "double distillation in pot stills",
        "age": "minimum 4 years (VSOP)"
    }],
    deductive_profile={
        "nose": "fresh apple, baked apple, cider vinegar, cinnamon, cream, oak spice",
        "palate": "medium-full body, creamy texture, apple-spice, warming finish",
        "signature": "apple-cream combination — Norman terroir in a glass"
    },
    service_specs={
        "glass": "tulip spirit glass",
        "uses": "digestif, trou normand (mid-meal palate reset), cooking, cocktails"
    },
    flavour_markers=["fresh apple", "baked apple", "cinnamon", "cream", "oak spice", "cider"],
    flavour_weight="medium-full",
    flavour_profile_type="fruity aged spirit",
    price_tier="premium",
    price_range_cad="$80-$130",
    technical_specs={
        "spirit": "Calvados Pays d'Auge",
        "abv": "42%",
        "distillation": "pot still double distillation",
        "age": "minimum 4 years"
    })

ricard_pastis = PROD(cur, "Ricard Pastis de Marseille",
    category="spirits_liqueur", producer_id=ricard_producer, region_id=PROVENCE,
    subcategory="pastis",
    description=(
        "Ricard Pastis de Marseille is the world's best-selling pastis and the archetype "
        "of the anise-liquorice spirit category. When diluted with cold water (typically "
        "1:5 ratio), the anethole compounds louche — turning the liquid opaque and milky. "
        "This louche effect is caused by the emulsification of essential oils that are "
        "soluble in alcohol but not in water. The ritual: ice first, pastis second, cold water third."
    ),
    quality_tier="market",
    quality_hierarchy=[{"tier": "benchmark commercial pastis", "category_archetype": True}],
    deductive_profile={
        "appearance": "clear amber neat; milky/louche when diluted",
        "nose": "intense star anise, liquorice, Provencal herbs, subtle spice",
        "palate": "sweet, anise-forward, herbaceous, warming",
        "signature": "the louche — pastis turns milky white when cold water is added"
    },
    service_specs={
        "ratio": "1 part pastis : 5 parts cold water (traditional Marseille ratio)",
        "sequence": "ice first, then pastis, then cold water — never reverse",
        "temperature": "serve very cold",
        "glass": "tall straight glass (Ricard glass)"
    },
    flavour_markers=["star anise", "liquorice", "Provencal herbs", "sweet spice"],
    flavour_weight="medium",
    flavour_profile_type="anise aromatic",
    price_tier="mid_range",
    price_range_cad="$35-$50",
    technical_specs={
        "spirit": "pastis",
        "abv": "45%",
        "key_botanicals": "star anise, liquorice root, Provencal herbs",
        "louche": "anethole emulsification when diluted with cold water"
    })

bardouin_pastis = PROD(cur, "Henri Bardouin Pastis",
    category="spirits_liqueur", producer_id=bardouin_producer, region_id=PROVENCE,
    subcategory="pastis",
    description=(
        "Henri Bardouin Pastis from Forcalquier uses 65 botanicals — including wild thyme, "
        "rosemary, savory, lavender, and vanilla — creating a far more complex aromatic profile "
        "than industrial pastis. Less sweet, more herbaceous, and more authentically Provencal. "
        "The preferred pastis of sommeliers and serious cocktail programs. Also louches beautifully."
    ),
    quality_tier="estate",
    quality_hierarchy=[{"tier": "artisanal pastis — 65 botanicals", "vs_commercial": "more complex, less sweet"}],
    deductive_profile={
        "nose": "star anise, wild thyme, lavender, rosemary, subtle vanilla, gentian",
        "palate": "drier than Ricard, more herbaceous, complex, long finish",
        "signature": "wild herb complexity — Haute-Provence landscape in a glass"
    },
    service_specs={
        "ratio": "1:5 with cold water (same as Ricard)",
        "glass": "tall straight glass",
        "temperature": "serve very cold"
    },
    flavour_markers=["star anise", "wild thyme", "lavender", "rosemary", "vanilla", "gentian"],
    flavour_weight="medium",
    flavour_profile_type="anise aromatic",
    price_tier="premium",
    price_range_cad="$55-$80",
    technical_specs={
        "spirit": "pastis",
        "abv": "45%",
        "botanicals": "65 wild Provencal herbs",
        "location": "Forcalquier, Haute-Provence"
    })

lemorton_domfrontais = PROD(cur, "Lemorton Calvados Domfrontais 15 Year",
    category="spirits_brandy", producer_id=lemorton, region_id=NORMANDY,
    subcategory="calvados",
    description=(
        "Lemorton Domfrontais 15 Year is the benchmark for Calvados Domfrontais — the appellation "
        "that requires a minimum 30% pear spirit. The pear character makes this Calvados lighter, "
        "more floral, and more ethereal than Pays d'Auge. At 15 years, the pear becomes more "
        "preserved and complex; the spirit has remarkable delicacy and length."
    ),
    quality_tier="reserve",
    quality_hierarchy=[{
        "appellation": "Calvados Domfrontais — min 30% pear",
        "age": "15 years",
        "pear_character": "distinctive floral pear distinguishes from Pays d'Auge"
    }],
    deductive_profile={
        "nose": "pear eau-de-vie, apple, blossom, preserved pear, subtle oak, cream",
        "palate": "lighter and more delicate than Pays d'Auge, floral, long finish",
        "signature": "pear florality — distinguishes Domfrontais from apple-forward Pays d'Auge"
    },
    service_specs={"glass": "tulip spirit glass", "temperature": "room temperature"},
    flavour_markers=["pear blossom", "preserved pear", "apple", "cream", "subtle oak"],
    flavour_weight="medium",
    flavour_profile_type="floral aged spirit",
    price_tier="premium",
    price_range_cad="$130-$200",
    technical_specs={
        "spirit": "Calvados Domfrontais",
        "abv": "42%",
        "pear_minimum": "30% perry pear required by law",
        "age": "15 years"
    })

print("\n=== FRENCH SPIRITS REFERENCES ===")

ref_cognac_crus = REF(cur,
    "Cognac — Cru Hierarchy, Aging, and Style Spectrum",
    category="spirits_knowledge", skill_level="advanced",
    description=(
        "Cognac is France's most regulated brandy — six defined crus, aging designations, "
        "and strict production rules including Charentais pot still distillation. "
        "Understanding the cru hierarchy, aging classifications, and regional style differences "
        "is essential for intelligent Cognac service and recommendation."
    ),
    key_principles=(
        "CRU HIERARCHY (chalk content = quality/aging potential): "
        "1. Grande Champagne (outermost — most chalk; most finesse; ages longest) "
        "2. Petite Champagne (slightly less chalk; still excellent) "
        "3. Fine Champagne = blend of Grande + Petite Champagne (at least 50% Grande) "
        "4. Borderies (smallest; distinctive violet-walnut character; ages faster) "
        "5. Fins Bois (larger area; fruity, rounder; used in VSOP blends) "
        "6. Bons Bois, Bois Ordinaires (larger area; used in VS blends or distilled for other uses) "
        "\nAGING CLASSIFICATIONS (minimum age in Limousin or Tronçais oak): "
        "VS (Very Special): 2 years minimum "
        "VSOP (Very Superior Old Pale): 4 years minimum "
        "XO (Extra Old): 10 years minimum (changed from 6 years in 2018) "
        "Napoleon: 6 years minimum (between VSOP and XO) "
        "XXO (Extra Extra Old): 14 years minimum (newest classification) "
        "\nHOUSE STYLES: "
        "Hennessy: full-bodied, rich, uses all crus — consistent, mainstream quality "
        "Remy Martin: Fine Champagne focus — mineral, elegant "
        "Delamain: Grande Champagne only — the most delicate and floral "
        "Hine: Grande Champagne with early-landing English aging — unique restraint "
        "Martell: Borderies focus — distinctive violet-nut character "
        "\nSERVICE: Tulip glass (not balloon snifter) — wide snifter overheats the spirit. "
        "Room temperature or slightly cooler. Never add ice. Never water."
    ),
    common_mistakes=(
        "Using a large balloon snifter — this overheats the spirit and drives off delicate aromatics. "
        "Treating all Cognac as the same regardless of cru or age. "
        "Assuming VS Cognac is suitable for premium cocktails — use minimum VSOP. "
        "Not knowing that XO minimum age increased from 6 to 10 years in 2018."
    ),
    pro_tips=(
        "Grande Champagne is to Cognac what Grand Cru Burgundy is to Pinot Noir. "
        "The 'rancio' note (nutty-oxidative) in aged Cognac is a mark of quality, not a fault. "
        "Hine Antique is the best introduction for guests who find Cognac too heavy — "
        "the English-aged style has remarkable delicacy."
    ),
    authority_tier=1,
    source_text="BNIC (Bureau National Interprofessionnel du Cognac) regulations; CMS spirits curriculum"
)

ref_armagnac_vs_cognac = REF(cur,
    "Armagnac versus Cognac — Key Distinctions for Sommelier Service",
    category="spirits_knowledge", skill_level="advanced",
    description=(
        "Armagnac is France's oldest distilled spirit (1411) and fundamentally different "
        "from Cognac in production method, style, and culture. Understanding the key "
        "distinctions allows confident comparison and service."
    ),
    key_principles=(
        "KEY DIFFERENCES: "
        "GEOGRAPHY: Armagnac = Gascony, Gers department (Bas-Armagnac, Tenareze, Haut-Armagnac). "
        "Cognac = Charente, near La Rochelle coast. "
        "\nDISTILLATION: Armagnac uses the Armagnacais continuous alembic (lower ABV off the still = "
        "more congeners = more character); Cognac uses Charentais pot still with double distillation "
        "(higher initial ABV = cleaner, more neutral spirit). "
        "\nSTYLE RESULT: Armagnac is more rustic, powerful, and earthy; Cognac is more refined, "
        "floral, and approachable. Armagnac's character: prune, black pepper, tobacco, earth. "
        "Cognac's character: dried fruit, flower, chalk mineral. "
        "\nVINTAGE DATING: Armagnac is much more commonly vintage-dated (single year) than Cognac. "
        "Vintage Armagnac from great years (1967, 1975, 1980) is the category's equivalent of "
        "vintage Champagne — sought by collectors and valued for aging. "
        "\nGRAPES: Both use Ugni Blanc primarily. Armagnac also uses Baco Blanc (a hybrid unique "
        "to Armagnac — not permitted in Cognac), Colombard, Folle Blanche. "
        "Baco Blanc gives Armagnac distinctive dark, earthy, rustic character. "
        "\nAGING: Both use oak. Armagnac typically uses dark, old Gascony oak; "
        "Cognac uses Limousin or Tronçais. Armagnac's dark oak integration adds to its earthiness."
    ),
    common_mistakes=(
        "Recommending Armagnac as a substitute for Cognac to a guest who wants elegance — "
        "Armagnac is deliberately rougher and more powerful. "
        "Not knowing that Baco Blanc is unique to Armagnac and gives the earthy dark character. "
        "Assuming vintage Armagnac means the spirit is better — quality of the base spirit matters."
    ),
    pro_tips=(
        "When introducing Armagnac to a Cognac drinker: 'Armagnac is France's wild, rustic cousin — "
        "more powerful, more earthy, more individual. Cognac is the trained sommelier; "
        "Armagnac is the passionate peasant farmer.' "
        "Darroze single-estate bottlings are the best introduction to serious Armagnac."
    ),
    authority_tier=1,
    source_text="BNIA (Bureau National Interprofessionnel de l'Armagnac); Oxford Companion to Spirits"
)

ref_pastis_anethole = REF(cur,
    "Pastis and the Mediterranean Anise Family — Anethole and the Louche Effect",
    category="spirits_knowledge", skill_level="advanced",
    description=(
        "Pastis belongs to a family of anise spirits found across the Mediterranean: "
        "pastis (France), ouzo (Greece), arak (Lebanon/Syria), raki (Turkey), sambuca (Italy), "
        "and Pernod (absinthe heritage, France). All share one defining molecule: trans-anethole. "
        "This reference covers the chemistry, production distinctions, and service logic "
        "shared across the entire Mediterranean anise family."
    ),
    key_principles=(
        "THE DEFINING MOLECULE: trans-Anethole (C10H12O) is the essential oil extracted from "
        "star anise (Illicium verum), green anise (Pimpinella anisum), and liquorice root. "
        "It is responsible for: (1) the characteristic sweet anise flavour; (2) the louche effect. "
        "\nTHE LOUCHE EFFECT: Anethole is soluble in alcohol but NOT in water. When cold water "
        "is added to a high-proof anise spirit, the alcohol concentration drops, causing anethole "
        "to come out of solution as an emulsion — creating the characteristic milky-white opacity. "
        "The louche is a quality indicator: the more dramatic and smooth the louche, the higher "
        "the quality of the essential oils. "
        "\nMEDITERRANEAN ANISE FAMILY: "
        "PASTIS (France, Provence): star anise + liquorice + herbs; 45% ABV; dilute 1:5; Ricard/Bardouin "
        "OUZO (Greece): grape spirit base + anise; 38-46% ABV; dilute 1:3; served with food (mezze) "
        "ARAK (Lebanon/Syria): grape spirit base + anise (star anise); 50-63% ABV; dilute 1:2-3 with ice; "
        "the oldest of the family — described in texts from 9th century "
        "RAKI (Turkey): grape spirit base + anise; 45% ABV; known as 'lion's milk'; dilute 1:2 with water "
        "SAMBUCA (Italy): neutral spirit + star anise + elderflower; sweeter; served neat or with coffee beans "
        "\nCOMMON THREAD: All are aperitif spirits associated with socialising and food in their "
        "respective cultures. The Mediterranean tradition of the long, slow aperitif — pastis in "
        "Marseille, ouzo in Athens, arak in Beirut — reflects a shared cultural relationship "
        "between anise spirit, water, conversation, and anticipation before eating."
    ),
    common_mistakes=(
        "Confusing pastis (post-1932, liquorice root present) with absinthe (pre-ban; bitter wormwood). "
        "Adding hot water to anise spirits — destroys the louche effect. "
        "Adding water before ice — the correct sequence is ice first, spirit second, cold water third. "
        "Treating arak, ouzo, raki as interchangeable — each has distinct character from grape base, "
        "botanical selection, and dilution ratio."
    ),
    pro_tips=(
        "The louche is a theatrical and educational moment — use it with guests to explain "
        "the chemistry of anethole emulsification. It is one of the most visually compelling "
        "demonstrations in spirit service. "
        "Henri Bardouin Pastis is the best choice for guests who want to understand the category "
        "at a more complex level — 65 botanicals versus Ricard's simpler formula."
    ),
    authority_tier=1,
    source_text="Oxford Companion to Spirits and Cocktails; McGee 'On Food and Cooking' (anethole); "
                "Difford's Guide to Spirits; Raki/Arak cultural research"
)

print("\n=== FRENCH SPIRITS PROTOCOL ===")

PROTOCOL(cur,
    "Cognac and Armagnac Service — Fine Dining Tableside Protocol",
    category="spirit_service", beverage_family="spirits",
    procedure=(
        "1. ARRIVAL: Present the bottle label-forward to the guest. State producer, designation "
        "(VS/VSOP/XO), and cru if applicable (Grande Champagne, Bas-Armagnac, etc.). "
        "2. GLASSWARE: Use tulip-shaped spirit glass — NOT a large balloon snifter. "
        "The tulip concentrates aromatics at the aperture without overheating from palm warmth. "
        "3. POUR: Standard 45ml (1.5 oz) pour. For premium aged expressions (XO+, vintage), "
        "allow 30 seconds after pouring for the glass to open before presenting. "
        "4. TEMPERATURE: Serve at room temperature (18-20C). Do not warm the glass in hands. "
        "Do not add ice. Do not add water (unlike whisky, Cognac is not improved by dilution). "
        "Exception: very young VS Cognac in a cocktail context — ice/water permitted. "
        "5. GUEST COMMUNICATION: "
        "For unfamiliar guests: 'This is [Producer] XO — aged a minimum 10 years in French oak. "
        "The chalk soils of Grande Champagne give it that remarkable mineral freshness underneath "
        "the rich fruit character.' "
        "6. POST-POUR: Leave the bottle within guest's sight. Offer second pour proactively "
        "for premium selections. Note food pairing opportunities (Cognac pairs with: dark chocolate, "
        "blue cheese, cigar, dry fruit tart; Armagnac with: prunes, cassoulet, duck confit)."
    ),
    description=(
        "Tableside service protocol for Cognac, Armagnac, and other French brandy "
        "in a fine dining context. Covers glassware, temperature, pour size, and "
        "guest communication for a premium service experience."
    ),
    rationale=(
        "French brandy service is often reduced to afterthought in restaurant settings. "
        "A properly executed Cognac/Armagnac service — correct glass, room temperature, "
        "confident cru explanation — elevates the experience and drives premium selection."
    ),
    common_errors=(
        "Using large balloon snifter — overheats the spirit, drives off aromatics. "
        "Serving chilled or on ice without guest request. "
        "Not explaining the cru distinction (Grande Champagne vs Borderies, etc.). "
        "Pouring more than 45ml — overwhelming the guest and diluting the experience."
    ),
    service_context="fine_dining, sommelier_recommendation",
    equipment_required=["tulip spirit glass", "spirit decanter (optional for Armagnac)"],
    guest_communication=(
        "For Cognac: 'This is one of France's great aged spirits — the chalk soils of "
        "Grande Champagne create a minerality you won't find in other brandies.' "
        "For Armagnac: 'Armagnac is France's oldest distilled spirit and made in the "
        "Gascon tradition — more rustic and earthy than Cognac, often vintage-dated.' "
        "For Calvados: 'This is apple brandy from Normandy — distilled from cider apples "
        "and aged in oak. It is an extraordinary digestif and one of France's best-kept secrets.'"
    ),
    skill_level="advanced", authority_tier=1,
    source_text="BNIC service standards; CMS Advanced Sommelier curriculum"
)

print("\n=== FRENCH SPIRITS PAIRINGS ===")

PAIR(cur, "Valrhona dark chocolate (72%) with fleur de sel",
     "chocolate_confection", "digestif",
     "classic", "complement",
     "The quintessential post-dinner Cognac pairing. Remy Martin XO's dried fruit, rancio, "
     "and chalk mineral interplays with dark chocolate's bitter-sweet depth. "
     "Fleur de sel bridges the mineral tension between wine and chocolate.",
     remy_xo, food_flavour_profile="bitter dark chocolate, salt, rich", beverage_category="spirits_brandy")

PAIR(cur, "Pruneaux d'Agen (prunes) with Armagnac and cream",
     "preserved_pickled", "digestif",
     "classic", "complement",
     "Prunes marinated in Armagnac is the Gascon classic — Armagnac prunes served with cream "
     "are the definitive regional pairing. The dark fruit and earthy prune quality mirrors "
     "Armagnac's own prune-black pepper character.",
     darroze_10yr, food_flavour_profile="prune, caramel, cream, dried fruit", beverage_category="spirits_brandy")

PAIR(cur, "Trou normand — apple sorbet with Calvados poured over",
     "preserved_pickled", "pre_dessert",
     "classic", "complement",
     "The trou normand is a Norman tradition — a small apple sorbet doused with Calvados "
     "served mid-meal to cleanse the palate and stimulate appetite. "
     "Dupont VSOP provides the apple-cream warmth that melts into the sorbet perfectly.",
     dupont_vsop, food_flavour_profile="apple sorbet, cold, refreshing", beverage_category="spirits_brandy")

PAIR(cur, "Pissaladiere (Nicoise onion tart) with anchovies and olives",
     "preserved_pickled", "aperitif",
     "classic", "complement",
     "The Provencal aperitif pairing — pastis and Nicoise snacks. Henri Bardouin's "
     "complex herbal pastis complements the salty-savoury intensity of pissaladiere; "
     "the herb complexity mirrors the olives and anchovy brine.",
     bardouin_pastis, food_flavour_profile="caramelised onion, anchovy salt, olive, herb", beverage_category="spirits_liqueur")

PAIR(cur, "Roquefort with walnut bread and pear",
     "dairy_fermented", "cheese",
     "established", "contrast",
     "Delamain Pale & Dry's floral elegance and chalk mineral create a refined counterpoint "
     "to Roquefort's barnyard intensity. The cheese's saline blue character meets the spirit's "
     "mineral precision; the pear provides a fruity bridge.",
     delamain_pale_dry, food_flavour_profile="salty blue cheese, barnyard, walnut, pear", beverage_category="spirits_brandy")

print("\n✅ French Spirits batch complete.")
cur.close()
conn.close()
