#!/usr/bin/env python3
"""Terminal 5 — Batch 5: Port wine + Madeira producers, products, refs, protocols"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Region IDs from batch 1
PORTO_DOURO = 235
MADEIRA_REGION = 236

print("=== PORT WINE — PRODUCERS ===")

taylor = P(cur, "Taylor Fladgate", "winery", PORTO_DOURO, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The oldest Port house still in single family ownership (Fladgate Partnership) — established 1692, and the most internationally recognised Port brand for quality. Quinta de Vargellas (purchased 1893) in Douro Superior is Taylor's flagship single quinta: 100+ year old vines on schist at 550m altitude producing some of Vintage Port's most ageable expressions. Taylor's Vintage Port is declared only in truly exceptional years (average 3 declarations per decade). The 20yr Tawny and the Quinta de Vargellas LBV are the entry points to serious Taylor Port.",
    key_personnel=[{"name": "Adrian Bridge", "role": "CEO, Fladgate Partnership"}, {"name": "David Guimaraens", "role": "head winemaker"}],
    production_details={"group": "Fladgate Partnership (Taylor's + Fonseca + Croft + Quinta de Roeda)",
                        "flagship_quinta": "Quinta de Vargellas, Douro Superior, 550m",
                        "range": "LBV, 20yr Tawny, 30yr Tawny, Vintage, Single Quinta Vintage"},
    quality_tier="reserve", reputation_narrative="The Port industry's most prestigious house by global recognition. Vintage Port auction prices rival Pomerol and Rhône for secondary market premium. Widely available globally including BC Liquor.",
    price_positioning="premium", authority_tier=1)

quinta_noval = P(cur, "Quinta do Noval", "winery", PORTO_DOURO, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The most storied quinta in Port — perched above Pinhão at 270-500m altitude, producing the most celebrated Vintage Port in existence: the Nacional. From a 2.5-hectare plot of pre-phylloxera, own-rooted Touriga Nacional vines that survived phylloxera in Noval's clay soils, Nacional is produced only in exceptional vintages (approximately 8-12 declarations per century). The 2011 Nacional sold for over £2,000 per bottle on release. The regular Quinta do Noval Vintage Port is among the most elegant in the category; the Nacional is in a class by itself.",
    key_personnel=[{"name": "Christian Seely", "role": "Managing Director (since 1993, AXA Millésimes)"}],
    production_details={"iconic_wine": "Nacional Vintage Port (pre-phylloxera own-rooted Touriga Nacional, 2.5ha)",
                        "declarations": "Nacional declared approximately 8-12 times per century in exceptional vintages only",
                        "ownership": "AXA Millésimes (since 1993)"},
    quality_tier="reserve", reputation_narrative="Nacional is one of the world's most sought-after wines — not just in Port but in any category. Even the standard Noval Vintage commands premium prices. Widely distributed.",
    price_positioning="ultra_premium", authority_tier=1)

grahams = P(cur, "W. & J. Graham's", "winery", PORTO_DOURO, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The Symington Family Estates' flagship house — the most celebrated name in the Symington portfolio (which also includes Dow's, Warre's, Quinta do Vesuvio, Quinta do Crasto). Graham's Vintage Port, first declared 1820, is the Symington standard: powerful, tannic, long-lived. The 30-year-old Tawny is among the finest examples of the oxidative-aged Port style. Quinta dos Malvedos, Graham's flagship quinta in Douro Superior, contributes the estate's deepest concentrations.",
    key_personnel=[{"name": "Johnny Symington", "role": "head of Graham's"}, {"name": "Charles Symington", "role": "production director"}],
    production_details={"group": "Symington Family Estates (Graham's, Dow's, Warre's, Quinta do Vesuvio)",
                        "flagship_quinta": "Quinta dos Malvedos, Douro Superior",
                        "range": "LBV, Six Grapes Reserve, 10/20/30/40yr Tawny, Vintage"},
    quality_tier="reserve", reputation_narrative="Graham's 30yr Tawny is the category benchmark. Vintage Port routinely among top 10 most critically acclaimed. Widely available.",
    price_positioning="premium", authority_tier=1)

fonseca = P(cur, "Fonseca", "winery", PORTO_DOURO, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The most consistently praised Port house for fragrant, aromatic Vintage Port — often considered more approachable younger than Taylor's, but equally age-worthy. Founded 1815; acquired by the Guimaraens family 1822; now part of the Fladgate Partnership alongside Taylor's. The Quinta do Panascal (Douro Superior) and Quinta de Cruzeiro (Cima Corgo) produce grapes with distinctive aromatic lift. Fonseca Bin 27 Reserve is one of the Port industry's most successful accessible quality offerings.",
    key_personnel=[{"name": "David Guimaraens", "role": "head winemaker (also Taylor's)"}, {"name": "Bruce Guimaraens", "role": "previous generation"}],
    production_details={"key_quintas": ["Quinta do Panascal (Douro Superior)", "Quinta de Cruzeiro (Cima Corgo)"],
                        "range": "Bin 27 Reserve Ruby, LBV, 10/20yr Tawny, Vintage",
                        "style_note": "More aromatic and approachable young than Taylor's; equally age-worthy"},
    quality_tier="reserve", reputation_narrative="Fonseca Vintage is often considered the most 'immediately enjoyable' of the great Port houses — a distinction that drives widespread recommendation. Bin 27 is Port's most successful accessible quality offering.",
    price_positioning="premium", authority_tier=1)

blandys = P(cur, "Blandy's", "winery", MADEIRA_REGION, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The benchmark Madeira shipper — established 1811 by John Blandy, still family-owned (sixth generation). Blandy's produces the widest range of Madeira styles and qualities, from entry 5yr categories through to vintage Malmsey from 1964 (still commercially available). The Blandy family's Quinta Grande provides estate-grown Bual and Malmsey grapes; other varieties are sourced from farmer relationships across the island. Blandy's is the pedagogical reference for Madeira — their four-grape, four-sweetness system (Sercial → Verdelho → Bual → Malmsey) is the standard teaching framework.",
    key_personnel=[{"name": "Chris Blandy", "role": "CEO (sixth generation)"}, {"name": "Michael Blandy", "role": "previous generation"}],
    production_details={"founded": 1811, "group": "Madeira Wine Company (majority shareholder since 1998)",
                        "range": "5yr/10yr/15yr categories in each variety + Colheita (single harvest) + Vintage",
                        "oldest_available": "1964 Malmsey (still commercially available)"},
    quality_tier="reserve", reputation_narrative="THE pedagogical reference for Madeira — Blandy's is the most widely stocked Madeira brand globally. Available in BC through multiple importers.",
    price_positioning="premium", authority_tier=1)

barbeito = P(cur, "Barbeito", "winery", MADEIRA_REGION, country="Portugal",
    production_philosophy="traditional",
    philosophy_description="The quality producer's choice for Madeira — Ricardo Diogo Freitas (fourth generation) runs a small, meticulous operation focused on canteiro-aged (natural rafters, no artificial heating) Madeira across all four noble varieties. Barbeito uses smaller barrels than most shippers (40L to 100L) for their aged Colheita and vintage expressions, arguing that greater wood surface contact accelerates complexity without compromising freshness. The 30yr Reserve in each variety are the house benchmarks — the Boal 30yr in particular is considered by specialists to rival the best Blandy's vintage examples.",
    key_personnel=[{"name": "Ricardo Diogo Freitas", "role": "director and winemaker (fourth generation)"}],
    production_details={"style": "Canteiro-aged exclusively (no estufagem/artificial heat)", "barrel_size": "40-100L (smaller than industry standard for greater complexity)",
                        "range": "10yr/30yr Reserve categories + Single Cask expressions",
                        "philosophy": "Small-scale, high-quality — the 'artisan' Madeira producer"},
    quality_tier="reserve", reputation_narrative="The specialist's choice — Barbeito's 30yr expressions are considered by many to rival or exceed Blandy's at similar price points. Growing international distribution.",
    price_positioning="premium", authority_tier=1)

print("\n=== PORT WINE — PRODUCTS ===")

taylor_20yr_tawny = PROD(cur,
    "Taylor Fladgate 20 Year Old Tawny Port",
    "wine_fortified", taylor, PORTO_DOURO, origin_country="Portugal",
    subcategory="Tawny Port 20yr",
    description="The industry benchmark for aged Tawny Port at the 20-year category — Taylor's slow-aged in small 550L pipas in the lodges of Vila Nova de Gaia, where temperature fluctuation between summer heat and winter cool drives gradual oxidation and concentration. The average age of wines in the blend is approximately 20 years (wines range from 15-30+ years). At this age, the oxidative transformation is complete: the wine shifts from purple to amber-tawny, the fruit evolves from fresh to dried (fig, date, dried apricot), the alcohol integrates, and a distinctive rancio character (nutty oxidation) emerges. Served chilled (10-12°C), this is Portugal's answer to a fine Amontillado — complex, sweet but not cloying, with exceptional length.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "40yr Old Tawny (Scion)", "criteria": "Average 40yr blend; extreme rancio and dried fruit concentration; €150+ price point; rare"},
        {"tier": 3, "tier_name": "30yr Old Tawny", "criteria": "Average 30yr blend; profound complexity; fig, walnut, coffee, dried fruit; very long rancio finish"},
        {"tier": 2, "tier_name": "20yr Old Tawny", "criteria": "Average 20yr blend; benchmark category; tawny colour fully achieved; dried fruit and rancio present; industry reference"},
        {"tier": 1, "tier_name": "10yr Old Tawny / Reserve Tawny", "criteria": "Early oxidative development; some fresh fruit remaining; transitional style; aperitif potential"}
    ],
    deductive_profile={"appearance": "Amber-tawny with pale orange rim; loss of purple colour complete at 20yr; viscous legs",
                       "nose": "Dried fig, date, dried apricot, roasted walnut, orange peel, coffee; rancio (nutty oxidative character); gentle alcohol integration at 20% ABV",
                       "palate": "Sweet (90-110 g/L RS) but balanced by oxidative acidity; medium-full body; extraordinary length; warm but integrated alcohol",
                       "conclusion": "Reserve quality; the aged Tawny benchmark; peak on release (NV); drink within 6 months of opening"},
    service_specs={"temperature_c": 11, "glass": "Small Port tulip glass (75-100mL) or white wine glass (larger bowl allows full aroma expression)",
                   "decant": "No — serve chilled, open 30 min before service", "programme_position": "Pre-dessert; cheese course (especially aged Manchego, Cheddar, Parmigiano); digestif"},
    flavour_markers=["dried fig", "date", "dried apricot", "roasted walnut", "orange peel", "rancio"],
    flavour_weight="full", flavour_profile_type="oxidative_fortified",
    price_tier="premium", price_range_cad="$55-80",
    technical_specs={"style": "Aged Tawny NV", "average_age_years": 20, "alcohol_abv": 20,
                     "residual_sugar_gl": 100, "ageing": "Small pipas (550L) in Vila Nova de Gaia lodges — natural temperature variation"})

noval_vintage = PROD(cur,
    "Quinta do Noval Vintage Port",
    "wine_fortified", quinta_noval, PORTO_DOURO, origin_country="Portugal",
    subcategory="Vintage Port",
    description="The most consistently elegant Vintage Port — Quinta do Noval's flagship expression from their Pinhão vineyards demonstrates that Port can be both powerful and aromatic, both deeply concentrated and fine-grained. Noval Vintage is declared in exceptional years only; Christian Seely's philosophy since 1993 has emphasised freshness and aromatic expression over sheer power — making Noval the 'approachable' great Vintage Port (relative to Taylor's power or Graham's structure). Still requires 20+ years to reach peak expression. The Nacional — from 2.5ha of pre-phylloxera own-rooted Touriga Nacional — is a categorically different wine in the same ecosystem.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Nacional Vintage Port", "criteria": "Pre-phylloxera own-rooted Touriga Nacional, 2.5ha; declared <10 times per century; €2,000+ per bottle; transcendent"},
        {"tier": 3, "tier_name": "Quinta do Noval Vintage Port (declared)", "criteria": "Exceptional years only; Pinhão schist; aromatic elegance; 25-30yr cellaring minimum"},
        {"tier": 2, "tier_name": "Quinta do Noval LBV (Unfiltered)", "criteria": "Late Bottled Vintage — aged 4-6yr in wood then bottled unfiltered; significant quality"},
        {"tier": 1, "tier_name": "Noval Black / Reserve", "criteria": "Entry Port; accessible fruit; immediate drinking; good introduction to the house"}
    ],
    deductive_profile={"appearance": "Very deep ruby-purple when young; developing garnet with 10+ years; opaque core in youth",
                       "nose": "Blackberry, violet, dark cherry in youth; developing cedar, tobacco, chocolate, leather at 15+ years; Nacional adds extraordinary concentration and mineral depth",
                       "palate": "Full-bodied; structured tannin (foot-trodden in lagar); 19-22% ABV integrated; 80-100 g/L RS; extraordinary length; 25+ year cellaring from declared vintages",
                       "conclusion": "Reserve quality; among the most age-worthy red wines in the world; do not open before 15 years from vintage"},
    service_specs={"temperature_c": 18, "glass": "Oversized Bordeaux glass or Vintage Port tulip",
                   "decant": "Required — decant young vintage (under 20yr) through muslin 3+ hours before service; older vintages gentle pour",
                   "programme_position": "Post-dessert or with aged hard cheese; celebration wine"},
    flavour_markers=["blackberry", "violet", "dark cherry", "cedar", "tobacco", "leather"],
    flavour_weight="full", flavour_profile_type="fortified_red",
    price_tier="ultra_premium", price_range_cad="$120-300",
    technical_specs={"style": "Vintage Port (declared years only)", "alcohol_abv": 20.5,
                     "residual_sugar_gl": 90, "ageing": "2 years in large wood before bottling, then decades in bottle",
                     "winemaking": "Foot-trodden in lagar"})

grahams_30yr = PROD(cur,
    "Graham's 30 Year Old Tawny Port",
    "wine_fortified", grahams, PORTO_DOURO, origin_country="Portugal",
    subcategory="Tawny Port 30yr",
    description="The reference point for the 30-year Tawny category — Graham's, with the longest family history in Port and the Symington's extraordinary wine library, produces the most consistently complex 30yr Tawny available commercially. At 30 years average age, the wines have undergone complete oxidative transformation: mahogany colour, intensely concentrated dried fruit (prune, fig, dried mango), rancio of extraordinary depth, and a salted caramel finish that no other beverage category can replicate. The '30yr' designation reflects the average age of wines in the blend — some components may be 40+ years.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Graham's 40yr Tawny ('The Patriarca')", "criteria": "Average 40yr blend; most complex commercial Tawny from Graham's; prune, rancio, and caramel of profound depth"},
        {"tier": 3, "tier_name": "Graham's 30yr Tawny", "criteria": "Average 30yr; mahogany colour; dried fruit intensity; rancio present and complex; 30 sec+ finish"},
        {"tier": 2, "tier_name": "Graham's 20yr Tawny", "criteria": "Average 20yr; amber; tawny character established; dried apricot and walnut; excellent at this price point"},
        {"tier": 1, "tier_name": "Six Grapes Reserve Ruby / 10yr Tawny", "criteria": "Entry Graham's quality; fresh (Six Grapes) or early oxidative (10yr); widely available and excellent QPR"}
    ],
    deductive_profile={"appearance": "Mahogany with pale amber rim; viscous legs; colour complexity reflects age",
                       "nose": "Prune, dried fig, dried mango, roasted coffee, salted caramel; profound rancio (nutty oxidative character); orange peel and walnut",
                       "palate": "Sweet (100-120 g/L RS) but balanced by oxidative complexity; medium-full body; 20% ABV integrated; extraordinary 30+ second finish of caramel and rancio",
                       "conclusion": "Reserve quality; the 30yr Tawny benchmark; NV — drink within 1 year of opening; serve chilled"},
    service_specs={"temperature_c": 10, "glass": "Port tulip or white wine glass",
                   "programme_position": "Pre-dessert; chocolate and caramel preparations; aged cheese; digestif"},
    flavour_markers=["prune", "dried fig", "roasted coffee", "salted caramel", "rancio", "orange peel"],
    flavour_weight="full", flavour_profile_type="oxidative_fortified",
    price_tier="premium", price_range_cad="$85-130",
    technical_specs={"style": "Aged Tawny NV", "average_age_years": 30, "alcohol_abv": 20,
                     "residual_sugar_gl": 110, "ageing": "Small pipas in Vila Nova de Gaia — warm summers accelerate oxidation"})

fonseca_bin27 = PROD(cur,
    "Fonseca Bin 27 Reserve Ruby Port",
    "wine_fortified", fonseca, PORTO_DOURO, origin_country="Portugal",
    subcategory="Reserve Ruby Port",
    description="Port's most successful accessible quality offering — Fonseca Bin 27 sits above standard Ruby (basic 2-3yr blend) and below Vintage (declared years only), occupying the Reserve Ruby category with approximately 4 years of ageing in large wooden vats preserving fresh fruit character. The house style of Fonseca (more aromatic, less austere than Taylor's) is fully expressed at this level: blackberry and cherry jam, with chocolate and dried herb notes from wood contact. An excellent introduction to Port for the uninitiated; a reliable by-the-glass offering for wine programmes.",
    quality_tier="estate",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Fonseca Vintage (declared)", "criteria": "Exceptional years only; 25+ yr cellaring; fragrant, aromatic Vintage style"},
        {"tier": 3, "tier_name": "Fonseca LBV (Unfiltered)", "criteria": "4-6yr wood then unfiltered; significant structure; decanting required"},
        {"tier": 2, "tier_name": "Bin 27 Reserve Ruby", "criteria": "~4yr large wood; fresh fruit preserved; accessible; restaurant standard; excellent QPR"},
        {"tier": 1, "tier_name": "Terra Prima (organic)", "criteria": "Entry organic Ruby; immediate freshness; approachable"}
    ],
    deductive_profile={"appearance": "Deep ruby-purple; full opacity; young fresh colour",
                       "nose": "Blackberry jam, cherry, dark chocolate, dried herbs; less oxidative than Tawny; straightforward fresh fruit",
                       "palate": "Sweet (90-110 g/L RS); full-bodied; fresh fruit character preserved; firm tannins from Touriga Nacional; medium-long finish",
                       "conclusion": "Estate quality; Port's best accessible by-the-glass wine; serve slightly chilled (14-16°C)"},
    service_specs={"temperature_c": 14, "glass": "Port tulip (75-100mL)",
                   "programme_position": "Cheese course (blue cheese); chocolate desserts; post-dinner port by the glass"},
    flavour_markers=["blackberry jam", "dark cherry", "dark chocolate", "dried herbs", "cassis"],
    flavour_weight="full", flavour_profile_type="fortified_red",
    price_tier="mid_range", price_range_cad="$22-30",
    technical_specs={"style": "Reserve Ruby NV", "ageing": "~4 years large wooden vats", "alcohol_abv": 20,
                     "residual_sugar_gl": 100})

print("\n=== MADEIRA — PRODUCTS ===")

blandys_malmsey_10 = PROD(cur,
    "Blandy's 10 Year Old Malmsey Madeira",
    "wine_fortified", blandys, MADEIRA_REGION, origin_country="Portugal",
    subcategory="Malmsey / Malvasia",
    description="The entry point to serious Madeira — Blandy's 10yr Malmsey (Malvasia) is the benchmark for the richest, sweetest Madeira style at the first ageable tier. Malmsey (from Malvasia Candida and Malvasia de São Jorge grapes) produces Madeira's most luscious expression: 90-120 g/L residual sugar balanced by Madeira's extreme acidity (malic acid survives the heating process). The 10yr average age represents the transition from basic Madeira (3yr estufagem category) to genuinely complex wine: dried apricot, coffee toffee, orange marmalade, and beginning rancio. The fortification to 20% ABV and subsequent heating (estufagem at 45-50°C for 90+ days, or canteiro natural ageing in rafters) makes Madeira literally indestructible — the most stable wine on Earth.",
    quality_tier="estate",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Colheita Malmsey (single vintage, 10yr+ barrel)", "criteria": "Single harvest; named vintage year; canteiro-aged; maximum complexity; rare and expensive"},
        {"tier": 3, "tier_name": "15yr Malmsey", "criteria": "Average 15yr blend; more rancio development; coffee and roasted complexity; very long finish"},
        {"tier": 2, "tier_name": "10yr Malmsey", "criteria": "Average 10yr; beginning complexity; excellent entry to serious Madeira; orange marmalade and coffee toffee"},
        {"tier": 1, "tier_name": "5yr Malmsey (Reserva)", "criteria": "Average 5yr; estufagem; basic sweetness without 10yr complexity; accessible entry point"}
    ],
    deductive_profile={"appearance": "Amber-mahogany; brilliant; viscous; colour deepens with age",
                       "nose": "Dried apricot, orange marmalade, coffee toffee; developing rancio; caramelised citrus; walnuts; extraordinary complexity for the price",
                       "palate": "Rich (90-120 g/L RS) balanced by extreme acidity; 20% ABV well-integrated; medium-long finish of coffee and caramel; essentially indestructible after opening",
                       "conclusion": "Estate quality; Madeira's most accessible entry to genuine complexity; open bottle can last months"},
    service_specs={"temperature_c": 12, "glass": "Small Madeira tulip or Port glass",
                   "programme_position": "Dessert course; cheese; digestif; chocolate preparations; Christmas pudding classic pairing"},
    flavour_markers=["dried apricot", "orange marmalade", "coffee toffee", "roasted walnut", "caramel"],
    flavour_weight="full", flavour_profile_type="oxidative_fortified",
    price_tier="mid_range", price_range_cad="$35-50",
    technical_specs={"grape": "Malvasia Candida, Malvasia de São Jorge", "style": "Malmsey NV",
                     "average_age_years": 10, "alcohol_abv": 20, "residual_sugar_gl": 105,
                     "ageing_method": "Estufagem (45-50°C, 90 days) plus wood ageing"})

blandys_sercial_colheita = PROD(cur,
    "Blandy's Sercial Colheita Madeira",
    "wine_fortified", blandys, MADEIRA_REGION, origin_country="Portugal",
    subcategory="Sercial / Colheita",
    description="Blandy's Sercial Colheita represents Madeira at its most intellectually demanding and most rewarding — the driest, most austere style (18-25 g/L RS) from a single declared harvest, canteiro-aged (natural ageing in barrels on the quinta's traditional rafters, heated by Madeira's sub-tropical sun). Sercial, related to Esgana Cão ('dog strangler'), produces Madeira of extraordinary tension: volcanic-mineral acidity, citrus zest, green almond, and walnut character without the sweetness of Bual or Malmsey. The colheita (single harvest) designation means the year is declared on the label — creating traceable provenance in a category where most wines are blended. These wines are among the world's most age-worthy.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Vintage Sercial (10yr minimum canteiro)", "criteria": "Single vintage; named year; 10+ yr canteiro; maximum mineral and oxidative complexity; transcendent; 100yr cellaring potential"},
        {"tier": 3, "tier_name": "Colheita Sercial (single harvest NV)", "criteria": "Single harvest; canteiro-aged; named year; excellent complexity at accessible price"},
        {"tier": 2, "tier_name": "15yr Sercial", "criteria": "Average 15yr blend; canteiro preferred; walnut and citrus complexity; long dry finish"},
        {"tier": 1, "tier_name": "10yr Sercial", "criteria": "Average 10yr; estufagem possible; beginning mineral complexity; dry aperitif style"}
    ],
    deductive_profile={"appearance": "Pale gold to amber (younger colheita); brilliant; lighter than Malmsey",
                       "nose": "Green almond, citrus peel, volcanic stone mineral, dry walnut; extreme acidity in youth; developing oxidative honey and caramel with age without sweetness",
                       "palate": "Dry to off-dry (18-25 g/L RS); extreme acidity; volcanic mineral finish; medium-full body; extraordinary length; no sweetness perception",
                       "conclusion": "Reserve quality; the sommelier's Madeira; pairs with food more readily than sweeter styles; 100yr cellaring potential in sealed bottle"},
    service_specs={"temperature_c": 10, "glass": "White wine glass (larger than Port tulip — needs aeration)",
                   "programme_position": "Aperitif; fish course (unusual fortified pairing); aged hard cheese"},
    flavour_markers=["green almond", "citrus peel", "volcanic stone", "dry walnut", "saline mineral"],
    flavour_weight="medium", flavour_profile_type="dry_oxidative",
    price_tier="premium", price_range_cad="$65-120",
    technical_specs={"grape": "Sercial", "style": "Colheita (single harvest)", "residual_sugar_gl": 22,
                     "alcohol_abv": 20, "ageing_method": "Canteiro (natural rafters, no artificial heat)",
                     "longevity": "100+ years in sealed bottle"})

barbeito_boal_30 = PROD(cur,
    "Barbeito 30 Year Old Reserve Boal Madeira",
    "wine_fortified", barbeito, MADEIRA_REGION, origin_country="Portugal",
    subcategory="Bual / Boal",
    description="Barbeito's flagship — the 30yr Reserve Boal from Ricardo Diogo Freitas represents the artisan approach to Madeira at its peak expression. Bual (Boal) is Madeira's medium-rich variety — 65-100 g/L residual sugar, positioned between Verdelho (medium-dry) and Malmsey (rich). At 30 years of canteiro ageing (Barbeito uses no estufagem), the wine achieves extraordinary complexity: dried fig, mocha, roasted coffee, orange peel, and a volcanic-mineral acidity that prevents the sweetness from becoming cloying. Barbeito's smaller barrel approach (40-100L) maximises complexity — many specialists regard this as superior to Blandy's equivalents at the same age tier.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Single Cask expressions", "criteria": "Individual barrel; named vintage; extreme rarity; direct allocation only"},
        {"tier": 3, "tier_name": "30yr Reserve Boal", "criteria": "30yr canteiro average; small barrel ageing; dried fig and mocha complexity; the house benchmark"},
        {"tier": 2, "tier_name": "10yr Boal", "criteria": "10yr average; canteiro method; excellent medium-rich Madeira introduction"},
        {"tier": 1, "tier_name": "Rainwater Medium Dry", "criteria": "Entry Barbeito; estufagem; commercial; accessible"}
    ],
    deductive_profile={"appearance": "Dark mahogany; opaque at the centre; brilliant amber rim; full viscosity",
                       "nose": "Dried fig, mocha, roasted coffee, orange peel, walnut; volcanic-mineral acidity lifts the aromatics; 30 years of Barbeito's small-barrel canteiro complexity",
                       "palate": "Medium-rich (75-90 g/L RS); extraordinary oxidative acidity prevents heaviness; full body; 20% ABV; 45+ second finish of coffee, caramel, and volcanic stone",
                       "conclusion": "Reserve quality; Barbeito's most acclaimed expression; specialist's benchmark for Bual quality"},
    service_specs={"temperature_c": 12, "glass": "Madeira tulip or Port glass",
                   "programme_position": "Pre-dessert; cheese course (Stilton classic match); digestif; chocolate preparations"},
    flavour_markers=["dried fig", "mocha", "roasted coffee", "orange peel", "walnut", "volcanic stone"],
    flavour_weight="full", flavour_profile_type="oxidative_fortified",
    price_tier="premium", price_range_cad="$95-150",
    technical_specs={"grape": "Bual (Boal)", "style": "Reserve NV", "average_age_years": 30,
                     "alcohol_abv": 20, "residual_sugar_gl": 82,
                     "ageing_method": "Canteiro ONLY — no estufagem; small barrels 40-100L"})

print("\n=== PORT + MADEIRA — REFERENCES ===")

ref_port_styles = REF(cur,
    "Port Wine — Complete Style Guide: Ruby, Tawny, LBV, Vintage, and Colheita",
    "wine_knowledge",
    description="Port wine encompasses two fundamentally different ageing pathways — reductive (bottle-aged: Vintage, LBV, Crusted) and oxidative (wood-aged: Ruby, Tawny, Colheita) — producing wines of completely different character despite identical winemaking foundations. Understanding this binary is the key to Port wine knowledge.",
    key_principles="""PORT STYLE MATRIX — REDUCTIVE vs. OXIDATIVE:

REDUCTIVE (BOTTLE-AGED) STYLES — fresh fruit preserved:
Vintage Port: Declared exceptional years only; 2yr wood then decades in bottle; maximum longevity (50+yr); fresh fruit → tobacco/leather/cedar with age; requires decanting
LBV (Late Bottled Vintage): Single year; 4-6yr in large wood; some unfiltered (decant) some filtered (no decant); excellent food alternative to full Vintage
Crusted Port: Blended vintage; thrown heavy sediment in bottle; decant required; premium Ruby quality without vintage declaration premium

OXIDATIVE (WOOD-AGED) STYLES — fruit transforms to dried/rancio:
Reserve Ruby: 3-5yr large wood; fresh fruit preserved; Ruby colour; entry commercial quality
10yr Tawny: Average 10yr; beginning amber; walnut and dried apricot emerging; transitional
20yr Tawny: Full amber; dried fruit dominant (fig, apricot); rancio present; category benchmark
30yr Tawny: Mahogany; profound rancio; coffee caramel; the peak NV experience
Colheita: Single-harvest Tawny; named year; canteiro or small wood; individual vintage character within oxidative style

TEMPERATURE AND SERVICE:
Vintage Port: 18°C — treat as full red wine
Aged Tawny (20yr+): 10-12°C — serve chilled
LBV: 16°C — serve below room temperature

FOOD PAIRING LOGIC:
Vintage Port + aged hard cheese (Stilton, Parmigiano) — classic
20yr Tawny + pre-dessert crème brûlée, chocolate fondant, almond tarts — elevated
LBV + blue cheese or chocolate — accessible pairing

DECLARATION: The IVDP (Instituto dos Vinhos do Douro e do Porto) must approve every style designation. Vintage declarations average 3-4 per decade.""",
    common_mistakes="Serving Vintage Port at room temperature and Tawny at room temperature — both wrong in opposite directions. Not decanting unfiltered LBV (sediment makes decanting essential). Confusing Colheita (single-harvest Tawny) with Vintage Port (single-harvest bottle-aged) — completely different styles.",
    pro_tips="Colheita is Port's best-kept secret: named vintage, aged Tawny complexity, accessible price. When a guest says 'Port' without specification, ask 'fresh fruit or nutty/dried fruit?' to guide Vintage vs. Tawny selection. Opened Tawny keeps 6+ months refrigerated — Vintage must be consumed within 24-48 hours after decanting.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="IVDP — Port Wine Style Guide; Taylor Fladgate educational materials; Symington Family Estates Technical Notes",
    authority_tier=1)

ref_madeira_canteiro = REF(cur,
    "Madeira Wine — Four Noble Varieties, Canteiro vs. Estufagem, and the Indestructibility Paradox",
    "wine_knowledge",
    description="Madeira is the world's most stable wine — fortified to 20% ABV and deliberately oxidised (through heat and oxygen exposure), it is theoretically indestructible. The oldest commercially available vintage (pre-phylloxera, 1862-1880) is still drinkable — no other wine category makes this claim. Understanding Madeira requires abandoning conventional wine preservation assumptions.",
    key_principles="""MADEIRA WINE SYSTEM:

FOUR NOBLE VARIETIES (driest to richest):
Sercial: Driest (18-25 g/L RS); most austere; volcanic-mineral; green almond and citrus; aperitif style; 100yr cellaring potential
Verdelho: Medium-dry (25-65 g/L RS); smoke and honey; balances fruit and acidity; most food-versatile Madeira
Bual (Boal): Medium-rich (65-100 g/L RS); dried fig and coffee; elegant sweetness; pre-dessert or dessert
Malmsey (Malvasia): Richest (90-120 g/L RS); most immediate; orange marmalade and toffee; most widely produced

AGEING METHODS:
Canteiro: Natural ageing in barrels stacked on rafters (estufas/lodges); heated by Madeira's sub-tropical sun; superior method; used for premium expressions
Estufagem: Artificial heating in stainless steel tanks to 45-50°C for minimum 90 days; cheaper; faster; used for entry 3yr and basic 5yr categories

AGE DESIGNATIONS:
3yr: Entry commercial; estufagem; basic; not food-appropriate
5yr (Reserva): Estufagem; recognisable Madeira character beginning
10yr (Reserva Velha): Average 10yr; beginning complexity; first serious tier
15yr (Extra Reserva): Deep complexity; rancio developing
20yr+: Profound rancio; exceptional longevity
Colheita: Single harvest, named year; 5yr minimum wood
Vintage: Single year, minimum 20yr canteiro; peak expression

THE INDESTRUCTIBILITY PARADOX:
Once bottled, Madeira's oxidative stability means:
- Opened bottles keep 6 months+ refrigerated
- Sealed bottles last centuries
- This makes Madeira ideal for by-the-glass programmes — no wastage concern""",
    common_mistakes="Treating Madeira as a sweet dessert wine — Sercial and Verdelho are aperitif wines. Over-chilling Malmsey (serve at 12°C). Confusing estufagem quality with canteiro quality — premium expressions always canteiro.",
    pro_tips="The best sommelier education tool: serve a flight of Sercial → Verdelho → Bual → Malmsey to illustrate sweetness spectrum from completely dry to rich. Madeira is the ultimate by-the-glass fortified — opened bottles require no special treatment.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="IVBAM — Madeira Wine Institute documentation; Blandy's educational materials; Richard Mayson — Madeira (Infinite Ideas, 2019)",
    authority_tier=1)

print("\n=== PORT PROTOCOLS ===")

prot_port = PROTOCOL(cur,
    "Port Wine Service — Vintage Decanting and Tawny Tableside",
    "wine_presentation",
    "fortified",
    procedure="""PORT SERVICE PROTOCOL — TWO STYLES:

VINTAGE PORT / UNFILTERED LBV — DECANTING SEQUENCE:
1. PREPARATION: Stand the bottle upright 24-48 hours before service to allow sediment to settle to the bottle base.
2. OPENING: Cut capsule completely. Extract cork with the cork-puller's corkscrew — old corks require gentle extraction. Wipe bottle neck with clean linen.
3. POUR PREPARATION: Place lit candle or wine light below the bottle neck during pouring to backlight the wine and identify when sediment approaches.
4. SINGLE SLOW POUR: Decant in one continuous, steady pour — do not stop and start (this disturbs sediment). Pour until the first wisps of sediment are visible through the candlelight. Stop.
5. SERVICE: Decant should be placed at the table. Port is NOT passed clockwise — in British tradition, the decanter is passed to the left (to the host's right hand neighbour first, then around the table, always to the left). This is the 'bishop's rule' — origins traced to 17th century English dining.
6. POUR VOLUME: 75-100mL per glass. Small Port tulip glass or small Bordeaux glass.

AGED TAWNY (20yr+) — CHILLED TABLESIDE SERVICE:
1. Retrieve from refrigerator (10-12°C service temperature).
2. Open 30 minutes before service to allow aromas to open.
3. Serve in small white wine glass or Port tulip — 75mL pour.
4. Verbal presentation: '[Name], Graham's/Taylor's 30-year-old Tawny — the average age of wines in the blend. Aged in small barrels in Vila Nova de Gaia, allowing gentle oxidation over decades. The colour has shifted completely from purple to mahogany, and the fruit has transformed from fresh blackberry to dried fig and roasted walnut.'""",
    description="Complete service protocol for both reductive (Vintage/LBV) and oxidative (Tawny) Port styles — including the 'passing to the left' tradition.",
    rationale="Port service has two fundamentally different requirements: Vintage Port requires temperature (18°C), decanting, and sediment management; Tawny requires chilling (10-12°C) and no decanting.",
    common_errors="Serving Vintage Port at room temperature (too warm — 18°C maximum). Not decanting unfiltered LBV. Serving Tawny warm. Passing the decanter to the right (breaks the historical tradition).",
    service_context="fine_dining, sommelier_recommendation",
    equipment_required=["decanter", "candle or port light", "muslin cloth", "Port tulips", "white wine glasses", "refrigerator"],
    guest_communication="The key communication: distinguish Vintage (rich, fresh fruit, structured) from Tawny (dried fruit, nutty, chilled). 'Port' ordered without specification requires a clarifying question.",
    skill_level="advanced", authority_tier=1,
    source_text="Court of Master Sommeliers Port service protocols; Taylor Fladgate service notes")

print("\n✅ Terminal 5 Batch 5 — Port + Madeira complete.")
print(f"""
PRODUCER IDs:
  taylor = {taylor}
  quinta_noval = {quinta_noval}
  grahams = {grahams}
  fonseca = {fonseca}
  blandys = {blandys}
  barbeito = {barbeito}

PRODUCT IDs:
  taylor_20yr_tawny = {taylor_20yr_tawny}
  noval_vintage = {noval_vintage}
  grahams_30yr = {grahams_30yr}
  fonseca_bin27 = {fonseca_bin27}
  blandys_malmsey_10 = {blandys_malmsey_10}
  blandys_sercial_colheita = {blandys_sercial_colheita}
  barbeito_boal_30 = {barbeito_boal_30}

REF IDs:
  ref_port_styles = {ref_port_styles}
  ref_madeira_canteiro = {ref_madeira_canteiro}

PROTOCOL IDs:
  prot_port = {prot_port}
""")
