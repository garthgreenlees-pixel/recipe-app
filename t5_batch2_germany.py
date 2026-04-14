#!/usr/bin/env python3
"""Terminal 5 — Batch 2: Germany wine producers + products (Mosel, Saar, Nahe, Rheingau, Pfalz)"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Region IDs from batch 1
MOSEL = 221
SAAR = 222
RHEINGAU = 223
NAHE = 224
PFALZ = 225

print("=== GERMANY — PRODUCERS ===")

egon_mueller = P(cur, "Egon Müller-Scharzhof", "winery", SAAR, country="Germany",
    production_philosophy="biodynamic",
    philosophy_description="The most celebrated name in German Riesling — a 10-hectare estate centred on the legendary Scharzhofberg vineyard in the Saar, owned by the Müller family since 1797. The Scharzhofberger is the Saar's Grand Cru monopole equivalent. Their TBA (Trockenbeerenauslese) auctions at Trier command prices second only to DRC — regularly €10,000+ per half-bottle. Winemaking is non-interventionist: native yeast, very long cold fermentation in old Fuder (1,000L oval casks), no fining, no stabilisation. The wines show Saar's signature steely, almost austere profile in youth, opening into extraordinary complexity with 20–30 years.",
    key_personnel=[{"name": "Egon Müller IV", "role": "proprietor and winemaker"}],
    production_details={"vineyard_ha": 10, "flagship": "Scharzhofberger Riesling Auslese/TBA/TBA Goldkapsel",
                        "fermentation": "native yeast, old Fuder 1000L", "ageing": "extended lees, no fining"},
    quality_tier="reserve", reputation_narrative="The benchmark for Saar Riesling and among Germany's top three producers by auction price. TBA and Goldkapsel TBA require restaurant accounts; standard Kabinett and Spätlese available through German specialists (Liberty Wines, Skurnik in USA).",
    price_positioning="ultra_premium", authority_tier=1)

jj_prum = P(cur, "Weingut Joh. Jos. Prüm", "winery", MOSEL, country="Germany",
    production_philosophy="traditional",
    philosophy_description="The most celebrated Mosel estate for Auslese and above — the J.J. Prüm house style is deliberately old-fashioned: high residual sugar, very high acidity, and a sulphur-rich, reductive youth that gives way to petrol (TDN — trimethyl-1,3,5-trioxane from Riesling's degraded carotenoids), honey, and dried apricot over 20+ years. Wehlener Sonnenuhr (a carved sundial in the vineyard) is their monopole Grand Cru equivalent. Katharina Prüm runs the estate in the traditional family style — minimal cellar intervention, no temperature control, fermentation running through winter.",
    key_personnel=[{"name": "Katharina Prüm", "role": "proprietor and winemaker"}, {"name": "Dr. Manfred Prüm", "role": "founder (1911-2011)"}],
    production_details={"flagship": "Wehlener Sonnenuhr Auslese", "fermentation": "native yeast, stainless steel, cold winter fermentation",
                        "ageing": "Fuder casks then bottle 1+ year before release", "key_vineyards": ["Wehlener Sonnenuhr", "Graacher Himmelreich"]},
    quality_tier="reserve", reputation_narrative="Essential reference for any serious German wine programme. The Auslese range is the entry point for collectors; Spätlese represents extraordinary QPR. Available in BC through private import; US through Terry Theise (Skurnik Wines).",
    price_positioning="premium", authority_tier=1)

fritz_haag = P(cur, "Fritz Haag", "winery", MOSEL, country="Germany",
    production_philosophy="traditional",
    philosophy_description="Brauneberg's most celebrated estate, centred on the steep Brauneberger Juffer and Juffer Sonnenuhr vineyards. Wilhelm Haag rebuilt the estate to international prominence from the 1980s; his son Oliver continues the style — pure Devonian blue slate expression, exquisitely balanced sugar and acidity, hallmark of the 'Brauneberg style' (slightly rounder than Wehlener or Scharzhofberger, with peach and apricot generosity alongside mineral precision). Goldkapsel Auslesen are benchmark collector wines.",
    key_personnel=[{"name": "Oliver Haag", "role": "winemaker"}, {"name": "Wilhelm Haag", "role": "founder"}],
    production_details={"flagship": "Brauneberger Juffer Sonnenuhr Auslese Goldkapsel", "key_vineyards": ["Juffer Sonnenuhr", "Juffer"],
                        "fermentation": "native yeast, old Fuder", "region_note": "Brauneberg — middle Mosel"},
    quality_tier="reserve", reputation_narrative="Reference estate for Brauneberg; the Goldkapsel auctions rival Prüm. Standard Spätlese widely available through Liberty Wines (UK) and German specialists.",
    price_positioning="premium", authority_tier=1)

markus_molitor = P(cur, "Markus Molitor", "winery", MOSEL, country="Germany",
    production_philosophy="traditional",
    philosophy_description="The most prolific of the Mosel's elite — Molitor farms over 100 hectares across the Mosel, Saar, and Ruwer, producing an enormous range from entry Kabinett (White Capsule) through White Label, Green Label, Gold Label, and Goldkapsel TBA. The single-vineyard Zeltinger Sonnenuhr, Graacher Himmelreich, and Ürzig Würzgarten Auslesen are the flagship expressions. Molitor's style emphasises phenolic ripeness and textural richness alongside classic Mosel slate minerality.",
    key_personnel=[{"name": "Markus Molitor", "role": "proprietor and winemaker"}],
    production_details={"vineyard_ha": 100, "key_vineyards": ["Zeltinger Sonnenuhr", "Graacher Himmelreich", "Ürzig Würzgarten", "Wehlener Sonnenuhr"],
                        "range": "Kabinett through TBA across all single vineyards"},
    quality_tier="reserve", reputation_narrative="Greatest range depth in the Mosel — from restaurant by-the-glass Kabinett to ultra-rare TBA. Available through multiple Canadian importers and wine specialists.",
    price_positioning="premium", authority_tier=1)

donnhoff = P(cur, "Dönnhoff", "winery", NAHE, country="Germany",
    production_philosophy="biodynamic",
    philosophy_description="The Nahe's reference producer — Helmut Dönnhoff built one of Germany's greatest reputations from an overlooked region. Oberhäuser Brücke, a tiny 0.5-hectare monopole of quartzite-volcanic soil above the Nahe river, produces Riesling of breathtaking mineral precision — often compared to Mosel's greatest single vineyards but with a floral, exotic character unique to Nahe's geological diversity. Established by Helmut; now run with equal rigour by Cornelius Dönnhoff.",
    key_personnel=[{"name": "Cornelius Dönnhoff", "role": "winemaker"}, {"name": "Helmut Dönnhoff", "role": "founder"}],
    production_details={"flagship": "Oberhäuser Brücke Riesling Auslese/Spätlese", "vineyard_note": "0.5ha monopole — volcanic quartzite, 100yr vines in key parcels",
                        "key_vineyards": ["Oberhäuser Brücke", "Niederhäuser Hermannshöhle", "Schlossböckelheimer Felsenberg"]},
    quality_tier="reserve", reputation_narrative="Germany's most important under-the-radar producer — Nahe wines remain undervalued versus Mosel, creating significant QPR. Brücke Auslese is the most sought-after Nahe wine. Available through Skurnik (USA), Roberson Wine (UK).",
    price_positioning="premium", authority_tier=1)

georg_breuer = P(cur, "Georg Breuer", "winery", RHEINGAU, country="Germany",
    production_philosophy="organic",
    philosophy_description="The Rheingau's most internationally visible estate — Georg Breuer (d. 2004) pioneered the Erstes Gewächs (First Growth) classification for the Rheingau, modelling it on Burgundy. Theresa Breuer continues a programme focused on the family's Grosses Gewächs from Berg Schlossberg, Berg Roseneck, and Berg Rottland — three contiguous south-facing Rüdesheim vineyards that Breuer argues are the Rheingau's answer to the Mosel's greatest sites. The style is drier and more textural than Mosel — Rheingau weight with Alsatian breadth.",
    key_personnel=[{"name": "Theresa Breuer", "role": "CEO and winemaker"}, {"name": "Georg Breuer", "role": "founder (d. 2004)"}],
    production_details={"flagship": "Berg Schlossberg Riesling GG", "key_vineyards": ["Berg Schlossberg", "Berg Roseneck", "Berg Rottland"],
                        "classification": "Grosses Gewächs (GG) — VDP First Growth equivalent"},
    quality_tier="reserve", reputation_narrative="Reference producer for Rheingau GG — more internationally visible than most Rheingau estates. Available through specialist importers in North America.",
    price_positioning="premium", authority_tier=1)

buerklin_wolf = P(cur, "Dr. Bürklin-Wolf", "winery", PFALZ, country="Germany",
    production_philosophy="biodynamic",
    philosophy_description="The Pfalz's most internationally renowned estate — 85 hectares across Forst, Deidesheim, Ruppertsberg, and Wachenheim. Biodynamic certified since 2005. The Pfalz classification system — Grosses Gewächs from classified Lagen — is most rigorously applied at Bürklin-Wolf. Kirchenstück, a 3.5-hectare vineyard of basalt-over-limestone in the heart of Forst, produces the estate's flagship GG — dense, powerful, mineral Riesling requiring 10+ years.",
    key_personnel=[{"name": "Bettina Bürklin-von Guradze", "role": "proprietor"}, {"name": "Fritz Knorr", "role": "cellar master"}],
    production_details={"vineyard_ha": 85, "flagship": "Kirchenstück Riesling GG", "certification": "Demeter biodynamic since 2005",
                        "key_vineyards": ["Kirchenstück (Forst)", "Jesuitengarten (Forst)", "Ungeheuer (Forst)"]},
    quality_tier="reserve", reputation_narrative="Standard-bearer for biodynamic viticulture in Germany. Kirchenstück GG is the Pfalz benchmark. Available through VDP importers across North America.",
    price_positioning="premium", authority_tier=1)

rebholz = P(cur, "Weingut Rebholz", "winery", PFALZ, country="Germany",
    production_philosophy="biodynamic",
    philosophy_description="The southern Pfalz reference estate — Hansjörg Rebholz farms 20 hectares in Siebeldingen, producing both exceptional Riesling and Germany's most serious Spätburgunder (Pinot Noir). The Im Sonnenschein GG and Birkweiler Kastanienbusch GG represent the southern Pfalz's distinctive sandstone-and-slate terroir. Rebholz is also Germany's finest argument that Spätburgunder can challenge Burgundy — the Kastanienbusch Spätburgunder GG is regularly cited alongside Burgundy Premier Cru in blind tastings.",
    key_personnel=[{"name": "Hansjörg Rebholz", "role": "winemaker and proprietor"}],
    production_details={"vineyard_ha": 20, "dual_focus": "Riesling GG + Spätburgunder GG", "key_vineyards": ["Birkweiler Kastanienbusch", "Im Sonnenschein"],
                        "region_note": "Southern Pfalz — sandstone/slate terroir, different from basalt-limestone Mittelhaardt"},
    quality_tier="reserve", reputation_narrative="Germany's definitive dual-grape estate — essential for programmes covering both Riesling and serious German Pinot Noir. Limited allocation; importer Skurnik (USA).",
    price_positioning="premium", authority_tier=1)

print("\n=== GERMANY — PRODUCTS ===")

egon_auslese = PROD(cur,
    "Egon Müller Scharzhofberger Riesling Auslese",
    "wine_still", egon_mueller, SAAR, origin_country="Germany",
    subcategory="Riesling Auslese",
    description="The benchmark expression from Saar's greatest single vineyard — a bowl of blue-grey Devonian slate set above the Saar river at Wiltingen. In top vintages (2003, 2007, 2015, 2019) this is among the most complex white wines on Earth: concentrated through selective botrytis-affected berry selection (Auslese minimum 97° Oechsle), yet with Saar's signature electric acidity that prevents cloying sweetness. The wine exits fermentation at 7.5–8.5% ABV with 80–120 g/L residual sugar; after 20 years in bottle it develops petroleum, dried apricot, and orange blossom of extraordinary precision.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Goldkapsel Auslese/TBA", "criteria": "Individually selected botrytis-shrivelled berries only; <5,000 bottles; Trier auction only"},
        {"tier": 3, "tier_name": "Auslese", "criteria": "Selected overripe, partially botrytised clusters; ≥97° Oechsle; extended cold fermentation"},
        {"tier": 2, "tier_name": "Spätlese", "criteria": "Late-harvested fully ripe Riesling; ≥85° Oechsle; Scharzhofberg terroir definition"},
        {"tier": 1, "tier_name": "Kabinett", "criteria": "Earliest ripening selection; lowest sugar (70-85° Oechsle); featherlight 7% ABV"}
    ],
    deductive_profile={"appearance": "Pale gold; brilliant clarity; viscous tears with age",
                       "nose": "White peach, apricot, and lime blossom in youth; developing TDN petroleum, orange peel, and honeyed lanolin at 15+ years; slate mineral backbone throughout",
                       "palate": "High residual sugar (80-120 g/L) balanced by extreme acidity (TA 9-12 g/L); featherlight body (7.5-8.5% ABV); extraordinary length; crystalline mineral finish",
                       "conclusion": "Reserve quality; peak: 15-35 years from vintage; requires patience; benchmark Saar Auslese"},
    service_specs={"temperature_c": 8, "glass": "Riesling tulip (small bowl concentrates delicate aromatics)", "decant": "No",
                   "programme_position": "Dessert course; cheese course alternative; sommelier showcase"},
    flavour_markers=["apricot", "white peach", "slate mineral", "lime blossom", "TDN petroleum", "honey", "orange blossom"],
    flavour_weight="light", flavour_profile_type="off_dry_aromatic",
    price_tier="ultra_premium", price_range_cad="$180-400",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 7.5, "residual_sugar_gl": 90,
                     "total_acidity_gl": 10.5, "pradikat": "Auslese", "oechsle_min": 97,
                     "vineyard": "Scharzhofberg", "area_ha": 10})

jj_prum_spatlese = PROD(cur,
    "Joh. Jos. Prüm Wehlener Sonnenuhr Riesling Spätlese",
    "wine_still", jj_prum, MOSEL, origin_country="Germany",
    subcategory="Riesling Spätlese",
    description="The entry point to one of Germany's most celebrated single vineyards — the Wehlener Sonnenuhr, a carved slate sundial presiding over a south-facing amphitheatre of pure Devonian blue-grey slate above the Mosel river. Prüm's Spätlese is initially austere and reductive (sulphur is used liberally in winemaking); after 8–12 years it reveals the vineyard's signature: honeyed peach, wet slate, and developing TDN petroleum of extraordinary complexity. At ≥85° Oechsle with 60–90 g/L residual sugar balanced by 9–11 g/L acidity, this is a wine of 25-year cellaring potential from a reliable vintage.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Auslese Goldkapsel/TBA", "criteria": "Single-berry botrytised selection; Trier auction allocation only; decade-long cellaring minimum"},
        {"tier": 3, "tier_name": "Auslese", "criteria": "Overripe partially botrytised clusters from Sonnenuhr; 97+ Oechsle; benchmark collector wine"},
        {"tier": 2, "tier_name": "Spätlese", "criteria": "Late-harvested fully ripe Sonnenuhr Riesling; 85-96 Oechsle; 20yr cellaring potential"},
        {"tier": 1, "tier_name": "Kabinett", "criteria": "Earliest selection; 70-84 Oechsle; finest aperitif German wine; lightest body"}
    ],
    deductive_profile={"appearance": "Pale gold; brilliant; slight viscosity at Spätlese level",
                       "nose": "Initially closed and reductive; 5+ years: white peach, apricot, and Mosel slate minerality; 10+ years: TDN petroleum, honey, beeswax",
                       "palate": "Off-dry (60-90 g/L RS) balanced by electric acidity; medium-light body; 8% ABV; extraordinary mineral finish on blue slate",
                       "conclusion": "Reserve quality; avoid before 8 years; peak 12-25 years from vintage"},
    service_specs={"temperature_c": 9, "glass": "Riesling tulip", "decant": "No",
                   "programme_position": "Fish course (off-dry Spätlese with rich fish or shellfish); cheese course; dessert opener"},
    flavour_markers=["white peach", "apricot", "Mosel blue slate", "TDN petroleum", "honey", "lemon zest"],
    flavour_weight="light", flavour_profile_type="off_dry_aromatic",
    price_tier="premium", price_range_cad="$55-90",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 8.0, "residual_sugar_gl": 75,
                     "total_acidity_gl": 10.0, "pradikat": "Spätlese", "oechsle_min": 85,
                     "vineyard": "Wehlener Sonnenuhr", "vine_age_avg": 50})

fritz_haag_auslese = PROD(cur,
    "Fritz Haag Brauneberger Juffer Sonnenuhr Riesling Auslese",
    "wine_still", fritz_haag, MOSEL, origin_country="Germany",
    subcategory="Riesling Auslese",
    description="From the steepest section of the Brauneberger Juffer — the Sonnenuhr sub-site named for a second carved sundial — this Auslese represents the 'Brauneberg style': marginally less austere than Saar or Wehlener Sonnenuhr, with generous peach and apricot richness alongside blue slate minerality. The Juffer Sonnenuhr's extreme 75% gradient positions it among the Mosel's most labour-intensive vineyards, worked entirely by hand with winch-assisted access. Haag Auslese in magnums is among the Mosel's most age-worthy formats; the Goldkapsel Auslese is the collector's expression.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Auslese Goldkapsel", "criteria": "Individually selected botrytis berries; TBA concentration; released only in exceptional vintages"},
        {"tier": 3, "tier_name": "Auslese", "criteria": "Selected overripe clusters from Juffer Sonnenuhr; generous peach/apricot character; 97+ Oechsle"},
        {"tier": 2, "tier_name": "Spätlese", "criteria": "Fully ripe harvest from Juffer; Brauneberg generosity without Auslese concentration; 85-96 Oechsle"},
        {"tier": 1, "tier_name": "Kabinett", "criteria": "Estate entry level; 70-84 Oechsle; fresh, light, food-friendly Mosel Riesling"}
    ],
    deductive_profile={"appearance": "Pale gold with green tints in youth; deepening to amber at 15+ years",
                       "nose": "Ripe white peach, apricot, and lime blossom; less reductive than Prüm in youth; developing honey and beeswax with age",
                       "palate": "Off-dry (80-120 g/L RS); generous fruit with firm acidity; more accessible young than Wehlener; long mineral finish",
                       "conclusion": "Reserve quality; peak 10-25 years from vintage; more hedonistic profile than Saar comparators"},
    service_specs={"temperature_c": 9, "glass": "Riesling tulip",
                   "programme_position": "Fish course with cream sauces; cheese course; dessert"},
    flavour_markers=["white peach", "apricot", "lime blossom", "blue slate mineral", "honey", "beeswax"],
    flavour_weight="light", flavour_profile_type="off_dry_aromatic",
    price_tier="premium", price_range_cad="$70-130",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 8.0, "residual_sugar_gl": 100,
                     "pradikat": "Auslese", "oechsle_min": 97, "vineyard": "Brauneberger Juffer Sonnenuhr",
                     "gradient_pct": 75})

donnhoff_bruecke = PROD(cur,
    "Dönnhoff Oberhäuser Brücke Riesling Spätlese",
    "wine_still", donnhoff, NAHE, origin_country="Germany",
    subcategory="Riesling Spätlese",
    description="Germany's most sought-after Nahe wine — a 0.5-hectare monopole on quartzite-volcanic rock above the Nahe river at Oberhausen, planted with vines averaging 90+ years. The Brücke ('bridge') site was identified by Helmut Dönnhoff as the Nahe's greatest terroir expression: unlike the Mosel's pure slate mineral intensity, Brücke adds exotic stone fruit (mango, papaya alongside peach), a floral lift unique to the site's volcanic-quartzite composition, and a stony, saline finish that lengthens for 30+ seconds. At Spätlese level this is a wine of extraordinary complexity; the Auslese is one of Germany's rarest and most sought-after bottles.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Auslese/TBA", "criteria": "Selected botrytised berries from 90yr vines; sub-half-hectare monopole; extremely scarce; critical acclaim universal"},
        {"tier": 3, "tier_name": "Spätlese", "criteria": "0.5ha monopole fully ripe harvest; 85-96 Oechsle; exotic fruit + volcanic minerality; 20yr cellaring"},
        {"tier": 2, "tier_name": "Hermannshöhle Spätlese", "criteria": "Larger vineyard; less exotic character; more classical mineral-fruit balance"},
        {"tier": 1, "tier_name": "Nahe Riesling Estate", "criteria": "Multi-vineyard blend; entry Nahe Riesling; freshness and precision without single-vineyard depth"}
    ],
    deductive_profile={"appearance": "Pale gold; brilliant; slightly more viscous than Mosel at equivalent sugar level",
                       "nose": "Distinctive exotic register unusual in German Riesling — mango, papaya, white peach alongside lime blossom and volcanic stone; unique to the Brücke site's quartzite-over-volcanic rock",
                       "palate": "Off-dry (65-95 g/L RS); extraordinary tension between fruit richness and volcanic-mineral acidity; saline, stony finish lasting 30+ seconds; 8-9% ABV",
                       "conclusion": "Reserve quality; peak 10-25 years from vintage; the Nahe's greatest ambassador"},
    service_specs={"temperature_c": 9, "glass": "Riesling tulip",
                   "programme_position": "Fish course — particularly flatfish with Asian-inflected preparations; cheese course"},
    flavour_markers=["mango", "papaya", "white peach", "volcanic stone", "lime blossom", "saline mineral", "exotic florals"],
    flavour_weight="light", flavour_profile_type="off_dry_aromatic",
    price_tier="premium", price_range_cad="$80-160",
    technical_specs={"grape": "Riesling 100%", "vineyard": "Oberhäuser Brücke", "area_ha": 0.5,
                     "vine_age_avg": 90, "alcohol_abv": 8.5, "residual_sugar_gl": 80,
                     "pradikat": "Spätlese", "soil": "quartzite-over-volcanic rock"})

berg_schlossberg = PROD(cur,
    "Georg Breuer Berg Schlossberg Riesling Grosses Gewächs",
    "wine_still", georg_breuer, RHEINGAU, origin_country="Germany",
    subcategory="Riesling Grosses Gewächs",
    description="The Rheingau's most internationally recognised dry Riesling — Berg Schlossberg is a steep south-facing quartzite-and-slate slope above the Rhine at Rüdesheim, one of three contiguous 'Berg' vineyards (Schlossberg, Roseneck, Rottland) that Breuer championed for the Erstes/Grosses Gewächs classification. The GG style is fermented to dryness (< 9 g/L RS), producing a wine fundamentally different from the Mosel Auslese style: more textured, more powerful, with Alsatian breadth, but with distinctly German Riesling's electric acidity and mineral backbone. Suitable for 10-year cellaring; food-versatile in a way that off-dry Riesling is not.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Grosses Gewächs (GG)", "criteria": "VDP First Growth designation; hand-harvested; ≤50 hl/ha; dry fermented; minimum 6 months ageing before release"},
        {"tier": 3, "tier_name": "Estate Riesling (Spätlese Trocken)", "criteria": "Single-vineyard dry style; broader selection than GG; earlier accessibility"},
        {"tier": 2, "tier_name": "Rüdesheimer Riesling", "criteria": "Village-level; Rüdesheim appellation; Breuer house style without GG site specificity"},
        {"tier": 1, "tier_name": "Terra Montosa", "criteria": "Entry Rheingau Riesling; made for immediate drinking; stainless steel, no GG designation"}
    ],
    deductive_profile={"appearance": "Pale gold; brilliant; more colour than Mosel at equivalent age",
                       "nose": "Dry Riesling profile — more mineral-forward than fruit; white grapefruit, green apple, wet quartzite; developing lanolin, petrol, and toasty complexity at 8+ years",
                       "palate": "Dry (RS <9 g/L); full-bodied for German Riesling (12.5-13.5% ABV); racy acidity; textural weight from Rhine slate; long mineral finish",
                       "conclusion": "Reserve quality; excellent food versatility (fish, white meat, Asian cuisine); peak 8-15 years"},
    service_specs={"temperature_c": 11, "glass": "White Burgundy or large Riesling glass — GG needs space to breathe",
                   "decant": "Optional for GG at 5+ years", "programme_position": "Fish course; white meat; Asian cuisine"},
    flavour_markers=["white grapefruit", "green apple", "quartzite mineral", "lanolin", "white peach", "petrol"],
    flavour_weight="medium", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$65-100",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 13.0, "residual_sugar_gl": 5,
                     "style": "Grosses Gewächs (dry)", "vineyard": "Berg Schlossberg",
                     "classification": "VDP.Grosse Lage", "yield_hl_ha": 45})

kirchenstueck_gg = PROD(cur,
    "Dr. Bürklin-Wolf Kirchenstück Riesling Grosses Gewächs",
    "wine_still", buerklin_wolf, PFALZ, origin_country="Germany",
    subcategory="Riesling Grosses Gewächs",
    description="The Pfalz's most prestigious Grosses Gewächs — a 3.5-hectare parcel of basalt-over-limestone in the heart of Forst, farmed biodynamically since 2005. Kirchenstück translates as 'church parcel' — the medieval Forster church owns a strip through the vineyard. The basalt layer above the Forst limestone imparts warmth and a distinctive stony-mineral character to the fruit: denser and more powerful than Rheingau GG, with tropical fruit notes (pineapple, mango) alongside the classic Riesling mineral structure. Requires minimum 5 years to integrate; at 10 years achieves extraordinary complexity.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Kirchenstück GG", "criteria": "Flagship Grosse Lage; basalt-over-limestone; biodynamic; hand-harvested; ≤45 hl/ha yield"},
        {"tier": 3, "tier_name": "Jesuitengarten/Ungeheuer GG", "criteria": "Other Forst Grosse Lagen — excellent but without Kirchenstück's basalt distinction"},
        {"tier": 2, "tier_name": "Deidesheim/Ruppertsberg Village Riesling", "criteria": "Single village; village classification; broader selection; earlier accessibility"},
        {"tier": 1, "tier_name": "Pfalz Riesling Estate", "criteria": "Multi-village; entry commercial Pfalz Riesling; stainless steel; early drinking"}
    ],
    deductive_profile={"appearance": "Medium gold; brilliant; more colour than Mosel GG due to Pfalz warmth",
                       "nose": "More tropical than typical German Riesling — pineapple, mango, peach over quartzite-basalt mineral; developing waxy, petroleum character at 8+ years",
                       "palate": "Dry (RS <9 g/L); full-bodied (13-13.5% ABV); dense texture from basalt warmth; electric acidity; very long finish with stony-mineral persistence",
                       "conclusion": "Reserve quality; Germany's most powerful Riesling GG; peak 8-20 years"},
    service_specs={"temperature_c": 12, "glass": "Large white Burgundy glass — needs volume to express",
                   "decant": "Recommended for GG at 5+ years — 30 min exposure", "programme_position": "Rich fish, white meat, pork, Alsatian choucroute"},
    flavour_markers=["pineapple", "mango", "white peach", "basalt stone", "petrol", "waxy lanolin", "tropical mineral"],
    flavour_weight="medium-full", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$90-130",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 13.5, "residual_sugar_gl": 6,
                     "certification": "Demeter biodynamic", "vineyard": "Kirchenstück, Forst",
                     "soil": "basalt-over-limestone", "classification": "VDP.Grosse Lage"})

molitor_zeltinger = PROD(cur,
    "Markus Molitor Zeltinger Sonnenuhr Riesling Auslese",
    "wine_still", markus_molitor, MOSEL, origin_country="Germany",
    subcategory="Riesling Auslese",
    description="The flagship single-vineyard expression from Molitor's 100+ hectare Mosel operation — Zeltinger Sonnenuhr is a steep south-facing slate amphitheatre adjacent to the more famous Wehlener Sonnenuhr, producing Auslesen of extraordinary richness and complexity. Molitor's range uses colour-coded capsules: White (Kabinett) → Green (Spätlese) → Gold (Auslese) → Goldkapsel (Auslese with further botrytis selection). The Gold Auslese from Zeltinger Sonnenuhr represents the estate's most accessible collector expression — concentrated apricot and honey richness balanced by Mosel's electric acidity at 7.5-8% ABV.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Goldkapsel Auslese/TBA", "criteria": "Individual botrytised berry selection; very rare; Trier auction or mailing list allocation"},
        {"tier": 3, "tier_name": "Gold Auslese (Sonnenuhr)", "criteria": "Selected overripe/botrytised clusters; 97+ Oechsle; rich but with Mosel acidity; 20yr potential"},
        {"tier": 2, "tier_name": "Green Spätlese (Sonnenuhr)", "criteria": "Late-harvested ripe selection; 85-96 Oechsle; excellent QPR; more accessible than Auslese"},
        {"tier": 1, "tier_name": "White Kabinett (estate/village)", "criteria": "Earliest selection; 70-84 Oechsle; 7-7.5% ABV; restaurant by-the-glass standard"}
    ],
    deductive_profile={"appearance": "Deep gold; significant viscosity at Auslese level",
                       "nose": "Apricot, mango, honey, and orange marmalade richness alongside Mosel blue-slate minerality; botrytis character adds honeyed complexity without camomile off-notes",
                       "palate": "Rich (100-130 g/L RS) but balanced by electric acidity (TA 9-11 g/L); 7.5-8% ABV; extraordinary persistence on blue slate mineral finish",
                       "conclusion": "Reserve quality; peak 12-30 years from vintage; more immediately accessible than Prüm or Egon Müller"},
    service_specs={"temperature_c": 9, "glass": "Riesling tulip",
                   "programme_position": "Dessert course; cheese course (blue cheese, aged gouda); sommelier showcase"},
    flavour_markers=["apricot", "honey", "orange marmalade", "mango", "blue slate mineral", "botrytis honey"],
    flavour_weight="medium-light", flavour_profile_type="off_dry_aromatic",
    price_tier="premium", price_range_cad="$65-120",
    technical_specs={"grape": "Riesling 100%", "vineyard": "Zeltinger Sonnenuhr",
                     "pradikat": "Auslese", "oechsle_min": 97, "alcohol_abv": 7.8,
                     "residual_sugar_gl": 115, "capsule_colour": "Gold"})

rebholz_spb = PROD(cur,
    "Rebholz Birkweiler Kastanienbusch Riesling Grosses Gewächs",
    "wine_still", rebholz, PFALZ, origin_country="Germany",
    subcategory="Riesling Grosses Gewächs",
    description="The southern Pfalz's definitive GG — Birkweiler Kastanienbusch ('chestnut forest') is composed of red sandstone, quartzite, and schist — a geological cocktail that gives Rebholz Riesling its distinctive salty-mineral, red-stony character rather than the basalt-tropical notes of Forst or Kirchenstück. Rebholz farms with extreme care — composting, cover crops, minimal spraying — in a region historically prone to riper, rounder wines. The GG achieves remarkable tension: 12.5-13% ABV, RS under 8 g/L, but with acidity that balances the fruit completely. Also produces Germany's most critically acclaimed Spätburgunder (Pinot Noir) GG from the same vineyard.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"tier": 4, "tier_name": "Kastanienbusch GG (Riesling or Spätburgunder)", "criteria": "VDP Grosse Lage; hand-harvested; own-rooted vines in sandstone-quartzite; dual-variety GG from same vineyard"},
        {"tier": 3, "tier_name": "Im Sonnenschein GG", "criteria": "Second Grosse Lage; similar approach; red sandstone with different mineral signature"},
        {"tier": 2, "tier_name": "Siebeldingen Village Riesling", "criteria": "Village classification; blended from estate parcels; earlier accessibility"},
        {"tier": 1, "tier_name": "Pfalz Riesling/Weissburgunder", "criteria": "Multi-village entry range; excellent QPR for southern Pfalz freshness"}
    ],
    deductive_profile={"appearance": "Pale gold; brilliant; relatively light colour for Pfalz",
                       "nose": "Red sandstone character — more stony and saline than Forst; white peach, citrus, and distinctive earthy-mineral underlay from sandstone; less tropical than Kirchenstück",
                       "palate": "Dry; medium-full body; 12.5-13% ABV; excellent tension between fruit and acidity; salty, stony mineral finish; 10yr cellaring minimum for GG",
                       "conclusion": "Reserve quality; the Pfalz's most distinctive terroir expression; unique sandstone character sets apart from basalt-dominant Forst producers"},
    service_specs={"temperature_c": 12, "glass": "White Burgundy glass",
                   "programme_position": "Rich fish, shellfish, pork, white meat; food-versatile dry GG"},
    flavour_markers=["white peach", "citrus", "red sandstone mineral", "saline", "earthy underlay", "quartzite stone"],
    flavour_weight="medium", flavour_profile_type="dry_mineral",
    price_tier="premium", price_range_cad="$70-110",
    technical_specs={"grape": "Riesling 100%", "alcohol_abv": 12.8, "residual_sugar_gl": 7,
                     "vineyard": "Birkweiler Kastanienbusch", "soil": "red sandstone, quartzite, schist",
                     "classification": "VDP.Grosse Lage"})

print("\n✅ Terminal 5 Batch 2 — Germany complete.")
print(f"""
PRODUCER ID SUMMARY:
  egon_mueller = {egon_mueller}
  jj_prum = {jj_prum}
  fritz_haag = {fritz_haag}
  markus_molitor = {markus_molitor}
  donnhoff = {donnhoff}
  georg_breuer = {georg_breuer}
  buerklin_wolf = {buerklin_wolf}
  rebholz = {rebholz}

PRODUCT ID SUMMARY:
  egon_auslese = {egon_auslese}
  jj_prum_spatlese = {jj_prum_spatlese}
  fritz_haag_auslese = {fritz_haag_auslese}
  donnhoff_bruecke = {donnhoff_bruecke}
  berg_schlossberg = {berg_schlossberg}
  kirchenstueck_gg = {kirchenstueck_gg}
  molitor_zeltinger = {molitor_zeltinger}
  rebholz_spb = {rebholz_spb}
""")
