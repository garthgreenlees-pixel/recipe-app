#!/usr/bin/env python3
"""Terminal 5 — Batch 6: German wine refs + protocol + pairings for all T5 products"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Product IDs from batches 2-5
# Germany
EGON_AUSLESE = 473
JJ_PRUM_SPATLESE = 474
FRITZ_HAAG_AUSLESE = 475
DONNHOFF_BRUECKE = 476
BERG_SCHLOSSBERG = 477
KIRCHENSTUECK_GG = 478
MOLITOR_ZELTINGER = 479
REBHOLZ_SPB = 480
# Austria
FX_PICHLER_GV = 481
KNOLL_RIESLING = 482
BRUNDLMAYER_HEILIGENSTEIN = 483
BRUNDLMAYER_LAMM = 484
MORIC_LUTZMANNSBURG = 485
UMATHUM_HB = 486
# Portugal table wine
VALE_MEAO = 487
NIEPOORT_CHARME = 488
SOALHEIRO_ALVARINHO = 489
ESPORAO_RESERVA = 490
LUIS_PATO_BAGA = 491
CRASTO_OLD_VINES = 492
# Port + Madeira
TAYLOR_20YR = 493
NOVAL_VINTAGE = 494
GRAHAMS_30YR = 495
FONSECA_BIN27 = 496
BLANDYS_MALMSEY = 497
BLANDYS_SERCIAL = 498
BARBEITO_BOAL_30 = 499

print("=== GERMANY — REFERENCES ===")

ref_pradikat = REF(cur,
    "German Riesling — Prädikat System, VDP Classification, and Trocken vs. Feinherb vs. Süss",
    "wine_knowledge",
    description="German wine classification is the world's most sugar-centric system — the Prädikat hierarchy measures natural ripeness at harvest (in degrees Oechsle) as the primary quality indicator. This is distinct from any other classification system; understanding it is essential for confident German wine navigation and blind tasting.",
    key_principles="""GERMAN RIESLING CLASSIFICATION SYSTEMS:

PRÄDIKAT SYSTEM (natural sugar at harvest — Oechsle degrees):
Kabinett: 70-85° Oechsle; lightest; lowest alcohol (7-9% ABV); finest filigree structure; often off-dry; 10-20yr cellaring
Spätlese: 85-95° Oechsle ('late harvest'); medium body; off-dry (40-90 g/L RS typical); the sweet spot for QPR; 15-25yr
Auslese: 95-125° Oechsle ('selected harvest'); selective botrytis clusters; rich; 20-40yr cellaring; collector entry point
Beerenauslese (BA): 125-150° Oechsle; individually botrytised berries; extremely rare; sweet; 50yr+ cellaring
Eiswein: 125° Oechsle minimum; frozen-on-vine grapes; extreme acidity balances sugar; 50yr+ cellaring
Trockenbeerenauslese (TBA): 150°+ Oechsle; individually shrivelled botrytised berries; honey concentration; 100yr cellaring; most expensive German wine

DRYNESS DESIGNATIONS (within each Prädikat):
Trocken (dry): RS <9 g/L (or RS-TA ≤10 g/L formula); Grosses Gewächs must be Trocken
Halbtrocken/Feinherb: RS 9-18 g/L (or 12 g/L); off-dry; food-versatile
No designation: Default implies off-dry to sweet (the 'traditional' Mosel style)
Note: Kabinett, Spätlese, and Auslese can be Trocken or sweet depending on producer decision

VDP (VERBAND DEUTSCHER PRÄDIKATSWEINGÜTER) CLASSIFICATION:
Grosses Gewächs (GG) / Grosser Wein: VDP's top tier; single vineyard; must be Trocken; Grosse Lage designation on label; hand-harvested; low yield; only released after 1yr+ ageing
Erste Lage: VDP's Second Growth equivalent; prestigious single vineyards below Grosse Lage
Ortswein: Village level; estate's representative style
Gutswein: Estate entry level

REGIONAL STYLE DIFFERENCES:
Mosel/Saar/Ruwer: Blue Devonian slate; lightest body; highest acidity; most age-worthy Spätlese/Auslese; 7-9% ABV at Kabinett
Rheingau: Quartzite; drier style (more Trocken); more Burgundy-influenced weight; Grosses Gewächs focus
Nahe: Most geological diversity; exotic character in Brücke/Hermannshöhle; between Mosel freshness and Rheingau weight
Pfalz: Warmest; most full-bodied; basalt-over-limestone in Forst; Grosses Gewächs style most powerful

AGEING IMPERATIVE:
Off-dry Mosel Spätlese/Auslese: Do not open before 8 years. At 20 years: TDN petroleum, honey, beeswax complexity.
Trocken GG: Open at 5+ years; peak 8-15 years.
TBA/Eiswein: 30-100yr minimum.

DEDUCTIVE TASTING CLUES:
Electric acidity + steely mineral = Saar or Mosel
Exotic stone fruit + volcanic mineral = Nahe (Brücke)
Tropical fruit + full body + Trocken = Pfalz GG
Power + structure + less acid = Rheingau GG""",
    common_mistakes="Assuming RS = quality (Kabinett with low RS can outlast Auslese). Opening off-dry Riesling too young (minimum 8 years for Spätlese). Confusing Trocken GG with sweet Auslese from the same Prädikat label. Undervaluing Nahe in favour of Mosel — Dönnhoff equals or exceeds most Mosel at similar price.",
    pro_tips="The Mosel Kabinett is the world's most food-versatile wine: 7-8% ABV, 70 g/L RS, 10 g/L TA — a wine that pairs with everything from sashimi to spicy Thai to blue cheese. At the TBA/Auslese end, serve in very small quantities (30-50mL) — the intensity demands restraint.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="VDP — Verband Deutscher Prädikatsweingüter classification rules; German Wine Law (Weingesetz); Stuart Pigott — Riesling (Absolute Press); Jancis Robinson — Wine Grapes",
    authority_tier=1)

ref_germany_regions = REF(cur,
    "Germany Wine Regions — Mosel, Rheingau, Nahe, Pfalz and the Terroir Logic of Slate vs. Basalt",
    "wine_regions",
    description="Germany's wine regions produce Riesling of radically different character based primarily on geology and climate — the same grape, planted 100km apart, produces wines so different that blind tasters regularly fail to identify them as the same variety. Understanding the geological and climatic logic of the major regions enables confident navigation and pairing.",
    key_principles="""GERMANY WINE REGION FRAMEWORK:

MOSEL-SAAR-RUWER:
Geology: Blue Devonian slate (Devonschiefer) — fractures to allow deep root penetration 20m+; drains freely; retains warmth overnight
Climate: Continental with Moselle river moderating influence; steep south-facing slopes essential for ripening
Character: Lightest German Riesling; highest acidity; most mineral; TDN petroleum develops with age; 7-11% ABV range
Key sites: Scharzhofberg (Saar), Wehlener Sonnenuhr, Bernkasteler Doktor, Brauneberger Juffer, Ürzig Würzgarten

RHEINGAU:
Geology: Quartzite (quartz-dominated schist) with Rhine alluvial soils near river; Taunus granite in higher sites
Climate: Rhine flows east-west → south-facing slopes maximise sun exposure; warmer than Mosel; less extreme
Character: More body and power than Mosel; drier style (Trocken GG focus); Burgundy weight with German acid
Key sites: Berg Schlossberg, Berg Roseneck, Rüdesheimer Berg, Steinberg, Schloss Johannisberg

NAHE:
Geology: Most diverse in Germany — porphyry (volcanic), quartzite, basalt, grey-blue slate, red sandstone in close proximity
Climate: Sheltered valley; warmer than Mosel; cold Nahe river moderates summer heat
Character: Unique exotic register (stone fruit, volcanic mineral) from diverse geology; bridge between Mosel delicacy and Rheingau power
Key sites: Oberhäuser Brücke (quartzite-volcanic, Dönnhoff monopole), Niederhäuser Hermannshöhle, Schlossböckelheimer Felsenberg

PFALZ:
Geology: Basalt over limestone in Forst/Deidesheim (warmest; most distinctive); sandstone/quartzite in southern Pfalz (Rebholz)
Climate: Warmest of the Riesling regions; sheltered by Haardt Mountains; Mediterranean-influenced microclimate in Mittelhaardt
Character: Most full-bodied German Riesling; tropical fruit in Forst basalt sites; Pinot Noir also serious; 12.5-13.5% ABV GG typical
Key sites: Forst Kirchenstück (basalt), Forst Jesuitengarten, Deidesheim Herrgottsacker, Birkweiler Kastanienbusch (sandstone)""",
    common_mistakes="Assuming 'Mosel' means light and simple — TBA from Mosel is among the most concentrated wines on Earth. Ignoring the Nahe — Dönnhoff equals Egon Müller in quality at considerably lower prices. Treating all German Riesling as sweet.",
    pro_tips="When building a German Riesling flight for a tasting: Mosel Kabinett (steely slate) → Nahe Spätlese (exotic volcanic) → Rheingau GG (structured quartzite) → Pfalz GG (tropical basalt) — 4 vineyards, 4 completely different characters from 1 grape variety. No other country demonstrates terroir as clearly.",
    service_context="fine_dining, sommelier_recommendation",
    source_text="VDP regional documentation; Hugh Johnson & Jancis Robinson — World Atlas of Wine; Mosel Wine Growers Association (Moselwein e.V.)",
    authority_tier=1)

print("\n=== GERMAN RIESLING PROTOCOL ===")

prot_riesling_service = PROTOCOL(cur,
    "German Riesling Service — Off-Dry Spätlese and Dry GG Protocols",
    "wine_presentation",
    "wine",
    procedure="""GERMAN RIESLING SERVICE — TWO DISTINCT PROTOCOLS:

PROTOCOL A — OFF-DRY RIESLING (Kabinett / Spätlese / Auslese):
1. TEMPERATURE: 8-10°C; German off-dry Riesling served colder than dry whites — the temperature suppresses residual sugar sensation while preserving acidity.
2. GLASS: Riesling tulip (small bowl, tapered — concentrates aromatics); Riedel Riesling Grand Cru or equivalent.
3. VINTAGE COMMUNICATION: Mandatory. Communicate vintage, producer, and Prädikat. 'This is the 2019 Joh. Jos. Prüm Wehlener Sonnenuhr Spätlese — the Prädikat tells us the grapes were harvested late, at full phenolic maturity, giving around 70 grams of residual sugar balanced by elevated acidity. The wine needs 8-10 years to reveal its full potential — today we're catching it in early development.'
4. POUR VOLUME: 90-100mL for standard service; 60-75mL for dessert/cheese course service.
5. POSITIONING ON MENU: Fish course (with Asian preparations, Thai spice, sashimi); cheese course (blue cheese — the classic); or as the main fish wine for oily fish (salmon, trout).

PROTOCOL B — GROSSES GEWÄCHS (Dry German Riesling):
1. TEMPERATURE: 11-12°C; slightly warmer than off-dry to open aromatic complexity.
2. GLASS: White Burgundy glass (larger bowl) — GG has enough weight to fill a bigger glass; the aeration benefits dry Riesling.
3. DECANTING: Optional for GG at 5+ years — 20-30 minutes in a carafe to open the wine.
4. VERBAL PRESENTATION: 'This is the 2017 Georg Breuer Berg Schlossberg Grosses Gewächs from the Rheingau — a dry Riesling, less than 9 grams of residual sugar, so it will pair with the same preparations as white Burgundy. The Grosses Gewächs is Germany's VDP First Growth designation — from a classified Grand Cru-equivalent vineyard.'
5. POSITIONING: Food-first — rich fish, white meat, Asian cuisine, pork. GG is the Riesling that challenges Burgundy for food versatility.""",
    description="Service protocol distinguishing off-dry Prädikat Riesling (Kabinett, Spätlese, Auslese) from dry Grosses Gewächs — fundamentally different service requirements.",
    rationale="German Riesling's dual nature (sweet vs. dry) creates guest confusion — the sommelier must actively clarify the distinction and pair appropriately.",
    common_errors="Serving off-dry Riesling warm (must be 8-10°C). Using Bordeaux glass for delicate Kabinett. Failing to communicate the Prädikat (guests assume all German Riesling is sweet). Serving young off-dry Riesling (Spätlese under 8 years) without mentioning its cellaring potential.",
    service_context="fine_dining, sommelier_recommendation",
    equipment_required=["Riesling tulip glasses", "White Burgundy glasses", "wine carafe for GG"],
    guest_communication="The essential script: 'German Riesling exists on a spectrum — this [Kabinett/Spätlese/Auslese] has residual sugar balanced by intense acidity, while the [GG/Trocken] is completely dry. Which style suits your preference today?'",
    skill_level="advanced", authority_tier=1,
    source_text="Court of Master Sommeliers German wine modules; VDP educational materials")

print("\n=== PAIRINGS — GERMANY (Riesling) ===")

# Germany off-dry Riesling pairings
PAIR(cur, "Aged Mimolette, walnuts, and honey — Prädikat Riesling cheese course pairing: sugar/acid balance cuts fat, honey bridges sweetness", "cheese", "cheese", "classic", "complement",
     "The residual sugar (70-120 g/L) of Spätlese/Auslese acts as the honey component; aged Mimolette's caramelised milk fat bridges to the wine's dried apricot and citrus character; walnuts add textural parallel to the slate mineral", EGON_AUSLESE, beverage_category="wine_still")

PAIR(cur, "Sashimi-grade halibut with yuzu kosho and shiso — Mosel Kabinett as the canonical sashimi-wine pairing", "seafood", "fish_course", "established", "complement",
     "Mosel Kabinett at 7-8% ABV does not overwhelm delicate white fish; yuzu's citrus parallels the Riesling's lime character; shiso's herbal anise echoes the wine's floral-herb register; slate minerality provides the same clean mineral finish as fresh halibut", JJ_PRUM_SPATLESE, beverage_category="wine_still")

PAIR(cur, "Foie gras torchon with Sauternes gel and brioche — Auslese Riesling as an alternative to Sauternes for foie gras service", "charcuterie", "starter", "established", "bridge",
     "Auslese's botrytis character (honey, dried apricot) parallels Sauternes directly; the higher acidity of Riesling (TA 9-11 g/L vs. Sauternes 5-7 g/L) cuts the fat more effectively; no sulphur clash with delicate foie gras", FRITZ_HAAG_AUSLESE, beverage_category="wine_still")

PAIR(cur, "Thai green curry with lemongrass, galangal, kaffir lime — Nahe Brücke Spätlese as spice-cuisine Riesling", "meat_poultry", "main", "classic", "complement",
     "Brücke's exotic tropical profile (mango, papaya) mirrors Thai curry's citrus-tropical base; residual sugar tames capsaicin heat; saline volcanic mineral finish cleanses coconut fat; this pairing demonstrates Riesling's spice-wine superiority over all other varieties", DONNHOFF_BRUECKE, beverage_category="wine_still")

PAIR(cur, "Wiener Schnitzel with lingonberry and cucumber salad — the canonical Austrian-German Riesling pairing", "meat_poultry", "main", "classic", "complement",
     "GG Trocken's body (13% ABV) and mineral acidity cut veal schnitzel fat; the lemon squeeze at service parallels the wine's citrus character; lingonberry's tartness resonates with GG acidity", BERG_SCHLOSSBERG, beverage_category="wine_still")

PAIR(cur, "Pfalz-style black truffle risotto with Parmigiano — Kirchenstück GG as the Alsatian-power pairing", "grains_pasta", "main", "suggested", "elevate",
     "Kirchenstück GG's tropical density and basalt-driven power can stand up to truffle's umami intensity — one of the rare white wines with this capability; Parmigiano's fat provides textural counterweight", KIRCHENSTUECK_GG, beverage_category="wine_still")

PAIR(cur, "Blue Stilton with Medjool dates and toasted almonds — aged Tawny Auslese cheese course", "cheese", "cheese", "classic", "bridge",
     "Mosel Auslese's honey and dried apricot character bridges directly to Stilton's own sweet-salt character; the extreme acidity cuts the blue's creaminess; dates parallel the wine's fruit character", MOLITOR_ZELTINGER, beverage_category="wine_still")

PAIR(cur, "Pork tenderloin with apple and black forest mushroom jus — Pfalz GG red-meat equivalent", "meat_pork", "main", "established", "complement",
     "Rebholz sandstone-quartzite GG has sufficient saline mineral acidity to cut through pork fat; apple in the preparation parallels the wine's stone fruit; mushroom umami bridges to the wine's earthy-mineral character", REBHOLZ_SPB, beverage_category="wine_still")

print("\n=== PAIRINGS — AUSTRIA ===")

PAIR(cur, "White asparagus with Hollandaise and morel mushrooms — the quintessential Austrian Smaragd pairing", "vegetable", "main", "classic", "complement",
     "Asparagus's vegetal bitterness requires a full-bodied white (Smaragd) with sufficient weight; Hollandaise butter fat balanced by GV's white pepper and citrus acidity; morel umami bridges to the wine's granite mineral", FX_PICHLER_GV, beverage_category="wine_still")

PAIR(cur, "Grilled Dover sole Meunière with capers and browned butter — Wachau Riesling Smaragd as the sole's companion", "seafood", "fish_course", "classic", "complement",
     "Wachau Riesling's mineral precision and citrus-stone acidity cuts browned butter fat without overwhelming sole's delicacy; capers' saline tang echoes the gneiss mineral character of the Loibenberg site", KNOLL_RIESLING, beverage_category="wine_still")

PAIR(cur, "Wiener Rostbraten (roast sirloin with anchovy and fried onion) — Heiligenstein Riesling as the Austrian roast meat pairing", "meat_beef", "main", "established", "complement",
     "Heiligenstein's volcanic-mineral weight and floral aromatics provide aromatic contrast to the savoury anchovy-onion preparation; the wine's full body (13-13.5% ABV) handles the richness", BRUNDLMAYER_HEILIGENSTEIN, beverage_category="wine_still")

PAIR(cur, "Tafelspitz (boiled beef with chive cream and rösti) — Kamptal Grüner Veltliner as Austria's national beef pairing", "meat_beef", "main", "classic", "complement",
     "Austria's most classic pairing: boiled beef's clean, saline flavour + Grüner Veltliner's white pepper and mineral acidity = the textbook Austrian food-wine marriage. Grüner's herbal character (tarragon) parallels the chive cream", BRUNDLMAYER_LAMM, beverage_category="wine_still")

PAIR(cur, "Venison saddle with juniper, chocolate jus, and salsify — Burgenland Blaufränkisch as the Austrian game wine", "meat_game", "main", "classic", "complement",
     "Moric Alte Reben's graphite-iron backbone pairs with venison's iron-rich dark meat; juniper's piney-resinous character bridges to the wine's spice; chocolate jus provides sweet contrast to the wine's dry structure", MORIC_LUTZMANNSBURG, beverage_category="wine_still")

PAIR(cur, "Wild boar terrine with cornichons and Dijon — Burgenland Blaufränkisch as charcuterie wine", "charcuterie", "starter", "established", "complement",
     "Umathum Hallebühl's dark cherry and iron mineral character cuts through the richness of boar terrine; the wine's firm tannin structure handles the fat; cornichon acidity parallels the wine's acidity", UMATHUM_HB, beverage_category="wine_still")

print("\n=== PAIRINGS — PORTUGAL TABLE WINE ===")

PAIR(cur, "Slow-roasted lamb shoulder with dried herbs and preserved lemon — Douro DOC Vale Meão as the canonical lamb pairing", "meat_lamb", "main", "classic", "complement",
     "Vale Meão's Touriga Nacional-dominant structure (graphite, violet, cedar tannin) is the Douro's answer to Bordeaux with lamb; dried herbs in the preparation parallel the wine's tobacco and cedar development; preserved lemon cuts the fat", VALE_MEAO, beverage_category="wine_still")

PAIR(cur, "Duck breast with cherry and mushroom sauce — Niepoort Charme as the elegant Douro pairing", "meat_poultry", "main", "established", "complement",
     "Charme's Tinta Amarela elegance (wild strawberry, dried herbs, iron mineral) pairs with duck's richness without overpowering; cherry sauce parallels the wine's own fruit character; mushroom umami bridges to the iron-mineral finish", NIEPOORT_CHARME, beverage_category="wine_still")

PAIR(cur, "Grilled sea bream (dourada) with olive oil and Maldon salt — Soalheiro Alvarinho as the coastal fish pairing", "seafood", "fish_course", "classic", "complement",
     "Alvarinho's saline mineral-schist character mirrors the sea; white peach and lemon blossom aromatics complement the sea bream's clean, sweet flesh; the wine's refreshing acidity acts as the ideal accompaniment to olive oil drizzle", SOALHEIRO_ALVARINHO, beverage_category="wine_still")

PAIR(cur, "Grilled Iberian pork secreto with Piri Piri and charred peppers — Esporão Reserva as the Alentejo grill pairing", "meat_pork", "main", "classic", "complement",
     "Esporão Reserva's full-bodied, warm (14% ABV) profile handles the charred fat of Iberian pork; Piri Piri's mild heat is complemented by the wine's dark fruit concentration; garrigue herbs in the wine parallel the charred pepper preparation", ESPORAO_RESERVA, beverage_category="wine_still")

PAIR(cur, "Suckling pig (leitão à Bairrada) — Luis Pato Baga as the canonical Bairrada regional pairing", "meat_pork", "main", "classic", "complement",
     "THE classic Bairrada pairing — leitão (suckling pig roasted whole, skin crackling) with young Baga is Bairrada's version of Barolo with tajarin; the wine's extreme acidity cuts the pig fat with precision; crackling's salt amplifies the fruit; absolutely inseparable regionally", LUIS_PATO_BAGA, beverage_category="wine_still")

PAIR(cur, "Bacalhau à Brás (salt cod with potato straws and eggs) — Quinta do Crasto Reserva as the bacalhau Douro pairing", "seafood", "main", "established", "complement",
     "Portugal's national dish demands a Douro red: the salt cod's powerful umami and salt contrast with Crasto's graphite-blackberry density creates a bridge pairing; the potato and egg soften the wine's tannin", CRASTO_OLD_VINES, beverage_category="wine_still")

print("\n=== PAIRINGS — PORT + MADEIRA ===")

PAIR(cur, "Stilton with Medjool dates and walnut bread — Taylor 20yr Tawny as the aged cheese pairing", "cheese", "cheese", "classic", "bridge",
     "The canonical Port-Stilton pairing with Tawny: the dried fruit character (fig, apricot) of 20yr Tawny bridges to Stilton's own sweet-salt character; the wine's high acid cuts the blue's creaminess; Medjool dates parallel the wine's fruit concentration", TAYLOR_20YR, beverage_category="wine_fortified")

PAIR(cur, "Chocolate fondant with vanilla ice cream — Quinta do Noval Vintage Port as the chocolate dessert pairing", "dessert", "dessert", "classic", "complement",
     "Vintage Port's fresh fruit character (blackberry, dark cherry) complements rather than competes with dark chocolate; the wine's tannin structure provides bitter counterpoint to the fondant's richness; vanilla ice cream adds sweet contrast", NOVAL_VINTAGE, beverage_category="wine_fortified")

PAIR(cur, "Crème brûlée with orange and cardamom — Graham's 30yr Tawny as the pre-dessert fortified", "dessert", "pre_dessert", "classic", "complement",
     "30yr Tawny's caramelised character (salted caramel, coffee toffee) mirrors crème brûlée's caramelised sugar directly; orange in the preparation parallels the wine's orange peel; cardamom's spice echoes the wine's rancio complexity", GRAHAMS_30YR, beverage_category="wine_fortified")

PAIR(cur, "Warm gorgonzola with honey and toasted pine nuts — Fonseca Bin 27 Ruby Port as the blue cheese pairing", "cheese", "cheese", "classic", "bridge",
     "Reserve Ruby Port's fresh blackberry and dark chocolate character bridges to gorgonzola's sweet-saline character; honey is the sweet link between wine and cheese; pine nuts add textural complexity", FONSECA_BIN27, beverage_category="wine_fortified")

PAIR(cur, "Christmas pudding with brandy butter — Blandy's 10yr Malmsey as the festive dessert pairing", "dessert", "dessert", "classic", "complement",
     "Malmsey's dried fruit (fig, apricot) and orange marmalade character is an exact mirror of Christmas pudding's flavour profile; the wine's extreme acidity prevents the richness from becoming cloying; the indestructibility of Madeira makes it ideal for festive cellaring", BLANDYS_MALMSEY, beverage_category="wine_fortified")

PAIR(cur, "Seared scallop with cauliflower purée and hazelnuts — Blandy's Sercial as the dry fortified aperitif pairing", "seafood", "starter", "suggested", "contrast",
     "Dry Sercial is Madeira's aperitif expression — the contrast pairing with scallop: the wine's extreme acidity (volcanic mineral, green almond) shocks against the scallop's sweet richness, then resolves through the cauliflower's earthiness; an unusual but compelling pairing for sommelier showcasing", BLANDYS_SERCIAL, beverage_category="wine_fortified")

PAIR(cur, "Tawny port-poached pear with roquefort and candied walnuts — Barbeito Boal 30yr as the dessert cheese pairing", "cheese", "pre_dessert", "established", "elevate",
     "Barbeito's medium-rich 30yr Boal (dried fig, mocha, volcanic mineral) elevates the Roquefort-pear combination: the wine's dried fruit parallels the poached pear's sweetness while its acidity cuts the Roquefort's richness; walnuts echo the wine's own walnut-rancio character", BARBEITO_BOAL_30, beverage_category="wine_fortified")

print("\n✅ Terminal 5 Batch 6 — Refs + Protocol + Pairings complete.")
print(f"""
REF IDs:
  ref_pradikat = {ref_pradikat}
  ref_germany_regions = {ref_germany_regions}

PROTOCOL ID:
  prot_riesling_service = {prot_riesling_service}
""")
