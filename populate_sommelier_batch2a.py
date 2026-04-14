#!/usr/bin/env python3
"""Canon 4 Batch 2a — entries 10-12: Spain/Portugal, Germany/Austria, New World"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO technique_references
  (name,slug,category,tier_level,authority_tier,source_book,
   description,key_principles,common_mistakes,pro_tips,trigger_keywords)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

ENTRIES = [

{
"name": "MS Theory — Wine Regions of Spain & Portugal",
"slug": "ms-theory-wine-regions-spain-portugal",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Wine Scholar Guild",
"description": """Spain and Portugal together represent the most undervalued depth in the MS theory exam. Spain alone contains over 600 indigenous grape varieties and 70+ DO/DOCa designations spanning ecosystems from the Atlantic-influenced Rías Baixas to the arid meseta of Ribera del Duero to the volcanic Canary Islands. Portugal, despite its small size, produces fortified wines (Port, Madeira) that every Master Sommelier must know in encyclopaedic detail, as well as a diverse array of unfortified wines built on indigenous varieties — Touriga Nacional, Baga, Alvarinho — that appear in the MS tasting exam with increasing frequency.

The key intellectual distinction for Iberia: Spain and Portugal both operate classification systems that reward ageing time rather than site quality, unlike France's terroir-based hierarchy. Rioja crianza/reserva/gran reserva and Port ruby/tawny/vintage/colheita classifications are legal ageing designations, not quality tiers — though in practice ageing time and quality correlate. Understanding both systems fluently is an MS requirement.""",

"key_principles": """SPAIN

RIOJA (DOCa — Spain's first Denominación de Origen Calificada, 1991):
Three sub-zones: Rioja Alta (west; Atlantic influence; Tempranillo dominant; elegant, age-worthy), Rioja Alavesa (Basque Country; limestone soils; concentrated, mineral Tempranillo), Rioja Oriental / Rioja Baja (east; Mediterranean influence; Garnacha dominant; richer, lower acid).
Ageing classifications: Joven (no ageing requirement — young, fruity), Crianza (minimum 2 years total ageing, 1 year in oak for reds), Reserva (minimum 3 years, 1 year in oak), Gran Reserva (minimum 5 years, 2 years in oak — only made in exceptional vintages).
Grape varieties: Tempranillo (dominant red), Garnacha, Mazuelo (Carignan), Graciano. White: Viura (Macabeo), Malvasía Riojana, Garnacha Blanca.
Traditional vs modern style: Traditional = extended American oak ageing (vanilla, coconut, dried fruit, brick colour); Modern = French oak, shorter ageing, more primary fruit, deeper colour.
Key producers: CVNE, Muga, López de Heredia (benchmark traditional), La Rioja Alta, Roda, Artadi, Remírez de Ganuza, Contino.

RIBERA DEL DUERO (DO):
High altitude plateau (800–1000m); extreme continental climate (cold nights, hot days — preserves acidity despite warmth); Tempranillo is called Tinto Fino or Tinta del País locally; more structured, darker, and less oak-vanilla than traditional Rioja.
Classification: Sin Crianza (young), Roble (brief oak), Crianza, Reserva, Gran Reserva — same framework as Rioja but applied to higher-altitude fruit.
Key producers: Vega Sicilia (Spain's most prestigious winery; Único = blend, aged 10+ years; Valbuena 5º = shorter-aged expression), Pingus (Peter Sisseck; cult wine), Abadía Retuerta, Dominio de Pingus, Pesquera.

PRIORAT (DOCa — Spain's second DOCa after Rioja):
Extreme terroir: llicorella (black slate and mica schist) soils that stress vines dramatically; yield 0.5–1 kg/vine; dramatic concentration. Old-vine Garnacha (Grenache) and Cariñena (Carignan) dominant; Syrah, Cabernet often blended.
Style: The most concentrated, mineral, complex Spanish reds; black fruit, mineral, iron, tobacco; high alcohol (14–17% natural); needs significant ageing.
Key producers: Álvaro Palacios (L'Ermita — Spain's most expensive wine), Mas d'en Gil, Cims de Porrera, Ferrer Bobet.
Nearby: Montsant DO (surrounding Priorat; similar style at lower prices).

RÍAS BAIXAS (DO):
Galicia (northwest); Atlantic Galician coast; DO since 1988; almost entirely Albariño grape; the benchmark for Spanish white wine quality. Sub-zones: Val do Salnés (most important; coastal; saline mineral), Condado do Tea (warmer, more inland), Ribeira do Ulla. Style: high acidity, citrus (lemon, grapefruit), white peach, floral, saline mineral finish; low-moderate alcohol (11–13%); limited oak contact in most expressions.
Producers: Pazo de Señorans, Fillaboa, Do Ferreiro, Terras Gauda.

JEREZ (Sherry — DO Jerez-Xérès-Sherry):
The sherry triangle: Jerez de la Frontera, Sanlúcar de Barrameda, El Puerto de Santa María (Cádiz, Andalucía).
Albariza soil (white chalk) = best quality.
Base wine: Palomino Fino (dry styles), Pedro Ximénez (PX — sweet), Moscatel (sweet).
Two ageing pathways:
  BIOLOGICAL AGEING (under flor): Fino (dry, delicate, almond, under active flor yeast — serve very cold, consume within days of opening), Manzanilla (Fino made exclusively in Sanlúcar de Barrameda; sea air produces distinctive saline, chamomile character), Amontillado (Fino that loses its flor and continues to age oxidatively; dual character: biological then oxidative; nutty + dried fruit + saline), Palo Cortado (rare, accidental pathway — starts as Fino, loses flor, develops oxidatively but with the finesse of Amontillado and the body of Oloroso).
  OXIDATIVE AGEING (without flor): Oloroso (never under flor; full oxidation; dark amber; dried fruit, walnut, fig; dry by nature but often sweetened commercially), Cream (Oloroso blended with PX to sweeten).
  Pedro Ximénez (PX): Sun-dried grapes; intense, viscous, raisin, fig, chocolate, coffee. Pour over vanilla ice cream.
Solera system: Fractional blending across multiple criaderas (scales) and final solera layer; oldest wine is at the bottom. Sherry has no vintage by definition (except Añadas — rare single vintage).
En Rama: Unfiltered sherry — released seasonally (spring Manzanilla en rama) — maximum freshness.

RUEDA (DO): Verdejo grape (distinctive herbaceous + citrus + almond); high altitude Castilla y León; fresh, crisp, aromatic whites; some barrel-aged expressions.

TORO (DO): Tinta de Toro (Tempranillo clone); extreme continental climate; very concentrated, dark, high-tannin reds; less refined than Ribera del Duero.

PENEDÈS / CAVA: Cava DO (Xarel·lo, Macabeo, Parellada traditional varieties; Chardonnay increasingly used); traditional method sparkling; minimum 9 months on lees (Reserva), 15 (Gran Reserva), 30 (Gran Añada). Penedès DO (Torres — multinational quality across styles).

PORTUGAL

PORT (DOC Douro):
Douro Valley classified into three sub-zones: Baixo Corgo (westernmost, wettest, lighter wines), Cima Corgo (quality heartland — Pinhão, Régua), Douro Superior (furthest east, hottest, most concentrated).
Grape varieties (IVDP-approved): Over 80 permitted; most important: Touriga Nacional (aromatic, floral, age-worthy), Touriga Franca (backbone, fruit), Tinta Roriz (Tempranillo), Tinta Barroca, Tinta Cão.
Port styles:
  Ruby (basic): Short wood ageing; young, fruity, simple.
  Reserve Ruby (Premium Ruby): Higher quality, more concentration, some blending.
  LBV (Late Bottled Vintage): Single vintage, bottled 4–6 years after harvest; filtered (ready to drink) or unfiltered (traditional, needs decanting).
  Vintage Port: Single exceptional year, bottled after 2 years in wood; unfiltered; requires 15–40 years of bottle ageing; the summit of Port quality. Declared by producer. Notable: 2011, 2007, 2000, 1994, 1992, 1970, 1963.
  Single Quinta Vintage: Single estate, not necessarily a declared year.
  Tawny Port: Aged in small barrels (pipes) with controlled oxidation; classified by average age: 10 Year, 20 Year, 30 Year, 40 Year Tawny (these are average ages, not specific vintages).
  Colheita: Single vintage tawny; aged minimum 7 years in barrel; the date on the label is the harvest year.
Key houses: Graham's, Taylor's, Fonseca, Quinta do Crasto, Niepoort, Ramos Pinto, Churchill's, Symington family estates (Graham's, Dow's, Warre's, Quinta do Vesúvio).

MADEIRA (DOC Madeira):
Island of Madeira; unique fortified wine; deliberately oxidised through the estufagem or canteiro process.
Estufagem: Commercial method — wine heated in tanks (45–50°C for 3+ months) to create the characteristic cooked/oxidative Madeiran character.
Canteiro: Premium method — wine aged in barrels under roof rafters in warm warehouses; slow, gentle oxidation; superior quality.
Grape varieties and style range: Sercial (driest, highest acid, most age-worthy), Verdelho (medium dry, nutty, smoky), Bual/Boal (medium sweet, rich, complex), Malmsey/Malvasia (sweetest, most voluptuous, coffee, caramel, dried fruit, raisin).
Tinta Negra: The workhorse variety used in most commercial Madeira without a varietal label.
Virtually indestructible — Madeira is one of the few wines that improve virtually indefinitely and survive extreme heat and oxidation.

VINHO VERDE (DO): Northwest Portugal; Minho region; 'green wine' = young wine (not wine made from green grapes); Alvarinho (= Albariño) is the premium variety; Loureiro, Arinto, Trajadura also used; high acid, low ABV (9–12% except premium Alvarinho at 13%+); slight effervescence in basic styles; sub-regions: Monção e Melgaço (Alvarinho), Lima (Loureiro).

DOURO UNFORTIFIED (DOC Douro): Same grapes and vineyards as Port; world-class unfortified reds; Touriga Nacional + Touriga Franca + Tinta Roriz blends; structured, mineral, age-worthy. Niepoort Redoma, Quinta do Crasto Reserva are benchmarks.

DÃO (DOC): Granite plateau; Touriga Nacional for reds; Encruzado for whites (one of Portugal's best white varieties — textured, complex, age-worthy); elegant, restrained wines.

ALENTEJO (DOC): Large southern region; hot, flat; Aragonez (Tempranillo), Trincadeira, Alicante Bouschet (rich colour, rare dark-fleshed grape); Alentejo wines tend to be riper, fuller, more international in style.""",

"common_mistakes": """1. Confusing Manzanilla with Fino — both are dry, biologically-aged sherries, but Manzanilla is produced exclusively in Sanlúcar de Barrameda and carries a distinctly saline, chamomile character from the Atlantic microclimate.
2. Not knowing Palo Cortado — a rare accidental sherry style that begins as Fino (biological ageing), loses its flor before completing the biological pathway, and continues oxidatively. It has the aroma of Amontillado and the body of Oloroso. It is testable at MS level.
3. Treating 20 Year Tawny Port as a 20-year-old wine — Tawny age designations are average ages; a 20 Year Tawny is a blend of wines averaging 20 years of barrel age, not a single-vintage wine.
4. Confusing LBV filtered and unfiltered Port — filtered LBV is ready to drink (commercially convenient, no decanting needed); unfiltered LBV throws a deposit and must be decanted. This is a service exam question.
5. Missing that Touriga Nacional is Portugal's most prestigious grape — it provides the aromatic backbone and age-worthiness of both Port and Douro reds.
6. Treating Vinho Verde as purely a light, fizzy, low-ABV category — premium Alvarinho from Monção e Melgaço reaches 13%+ ABV with full body and significant complexity and can age.
7. Confusing Priorat and Ribera del Duero stylistically — Priorat = old-vine Garnacha and Cariñena on llicorella schist; Ribera = Tempranillo (Tinto Fino) on high-altitude meseta. Common palate fingerprint confusion.
8. Overlooking Madeira's indestructibility — a common exam scenario involves recommending a wine for unusual storage conditions; Madeira (already oxidised, already heat-treated) can survive heat and oxygen that would destroy any other wine.""",

"pro_tips": """1. Know the Sherry Triangle geography — Jerez, Sanlúcar, El Puerto — and know which style comes exclusively from which town. Manzanilla = Sanlúcar only. Fino can come from all three. This is a reliable MS theory question.
2. Vega Sicilia is the benchmark for Ribera del Duero but also for understanding Spanish wine philosophy: Único is not released until it is ready (10+ years after harvest); the winery makes the ageing decision, not the market.
3. For Port Vintage declarations: major houses do not always declare the same year. Know the universally acclaimed Vintage Port years: 2017, 2011, 2007, 2003, 2000, 1994, 1985, 1977, 1970, 1963, 1945. Candidates who don't know the great Port vintages fail scenarios about building a Port list.
4. The canteiro vs estufagem distinction is a reliable quality differentiator for Madeira — ask yourself whether a Madeira label specifies the method; premium producers (Blandy's, Barbeito, Justino's) increasingly use canteiro for their premium expressions.
5. Albariño (Spain, Rías Baixas) and Alvarinho (Portugal, Monção e Melgaço) are the same grape — separated by a river and a border. This genetic identity is testable.
6. For Rioja blind tasting: traditional Rioja (extended American oak) has a distinctive vanilla/coconut/dill character that is unlike almost anything else in Spain; this American oak signature is the most reliable identification marker.
7. Study the ICEX/Wines from Spain structure — Spain uses DO (Denominación de Origen) and DOCa (Denominación de Origen Calificada — only Rioja and Priorat). Know these two tiers.
8. Port service protocols for the MS practical exam: Vintage Port requires decanting (sediment forms after 5–10+ years bottle age); Tawny Port is served chilled (12–14°C) in a smaller glass; LBV filtered serves like any red table wine; Colheita is served at similar temperatures to Tawny.""",
"trigger_keywords": json.dumps(["Spain wine", "Portugal wine", "Rioja", "Ribera del Duero", "Priorat", "Sherry", "Port", "Madeira", "Rías Baixas", "MS exam Iberia"])
},

{
"name": "MS Theory — Wine Regions of Germany & Austria",
"slug": "ms-theory-wine-regions-germany-austria",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Wine Scholar Guild — German Wine Scholar",
"description": """Germany and Austria together represent the most intellectually demanding section of the MS theory exam because of the complexity of their classification systems and the counter-intuitive fact that their finest wines (Spätlese, Auslese, TBA in Germany; Smaragd in Austria) can be produced from a single grape variety (Riesling) across a dramatic quality and sweetness spectrum in what are nominally cool climates. Understanding these wines requires separating residual sugar from quality — a Mosel Trockenbeerenauslese and a bone-dry Wachau Smaragd both represent pinnacle quality despite opposite ends of the sweetness spectrum.

Germany is home to the world's greatest Riesling. The Mosel's slate soils, steep river-facing terraces, and slate terroir produce wines of extraordinary mineral precision and longevity at low alcohol levels (7–11%) that have no direct parallel anywhere in the wine world. Austria's Grüner Veltliner is arguably the world's finest food-pairing white wine — high acidity, white pepper, mineral, and clean finish that works with notoriously difficult pairings (asparagus, artichoke). Both countries' quality systems reward site and vintage rather than producer reputation.""",

"key_principles": """GERMANY

PRÄDIKAT SYSTEM (Qualitätswein mit Prädikat — QmP)
Six Prädikat levels defined by must weight (Oechsle — measure of sugar in the must at harvest):
  Kabinett: Lightest; lowest must weight; often semi-dry or dry; 67–82 Oechsle; delicate, low ABV (7–10%), great acid-RS balance.
  Spätlese (late harvest): Richer; minimum 76–90 Oechsle depending on region; can be dry or off-dry; fuller flavoured than Kabinett.
  Auslese (select harvest): Selected bunches of fully ripe grapes; some botrytis possible; noticeably sweet in most expressions; complex, layered.
  Beerenauslese (BA): Individual berries selected for botrytis/overripeness; rare; luscious sweetness; extraordinary complexity and longevity.
  Eiswein (Ice Wine): Grapes frozen naturally on the vine (harvested at -8°C or colder); concentrated acid AND sugar; tart, intense, mineral sweetness.
  Trockenbeerenauslese (TBA): Individually selected dried/botrytised berries; the rarest and most expensive German wine; syrupy, extraordinarily concentrated; must weight 150+ Oechsle; can age for 50–100 years.

Note: Prädikat levels indicate must weight at harvest, NOT final sweetness level. A Spätlese can be fermented dry (Spätlese Trocken) or left with residual sugar. At higher levels (BA, TBA), the sugar concentration almost always prevents complete fermentation, producing naturally sweet wines.

TROCKEN / HALBTROCKEN / FEINHERB
Trocken (dry): Under 9 g/L RS (or up to 4 g/L above total acidity).
Halbtrocken (half-dry / off-dry): 9–18 g/L RS.
Feinherb: Informal term, similar to halbtrocken but with slightly more flexibility; used in Mosel.

VDP CLASSIFICATION (Verband Deutscher Prädikatsweingüter — Association of German Predicate Wine Estates)
VDP.Grosse Lage (GL): The top tier; single vineyard; Germany's equivalent of Grand Cru. Red wines = VDP.Grosses Gewächs (GG) — always dry. White wines = VDP.Grosses Gewächs (dry) or traditional Prädikat (sweet).
VDP.Erste Lage (EL): Premier Cru equivalent; single vineyard, second tier.
VDP.Ortswein: Village wine.
VDP.Gutswein: Estate wine.
The VDP classification is voluntary and producer-led but is the most reliable quality indicator in Germany.

GERMAN WINE REGIONS (13 Anbaugebiete)
Mosel (the most important region for MS study): Steep (up to 70° gradient) blue and red Devonian slate terraces on the Mosel, Saar, and Ruwer rivers; slate absorbs heat, stores it, and releases it at night — essential for ripening at this latitude (51°N). Riesling dominant. Style: the finest Mosel Riesling (GK Apotheke, Erdener Prälat, Brauneberger Juffer-Sonnenuhr) has extraordinary precision: citrus blossom, slate, white peach; low alcohol; crystalline acidity balanced by natural RS (in non-Trocken styles); the most ethereal white wine in the world. Can age 30–50+ years.
  Key villages: Trittenheim, Neumagen-Dhron, Piesport (Goldtröpfchen — famous cru), Bernkastel (Bernkasteler Doctor — the most famous individual vineyard in Germany), Graach, Wehlen (Wehlener Sonnenuhr — the benchmark for Mosel GG), Zeltingen, Ürzig (Ürziger Würzgarten — spicy, volcanic soil), Erden, Traben-Trarbach.
  Key producers: Egon Müller (Scharzhofberg — the most expensive Riesling), J.J. Prüm (Wehlener Sonnenuhr), Molitor, Loosen, Selbach-Oster, Schloss Lieser.

Rheingau: Rhine river facing south (unique — the Rhine flows east-west here); steep hillside sites; Riesling dominant; fuller, more powerful than Mosel; higher alcohol. Classified estates (Kloster Eberbach history). Johannisberg (the historic Schloss Johannisberg estate). Rüdesheim Berg Schlossberg (the great GG site). Assmannshausen (Spätburgunder/Pinot Noir specialist).

Pfalz: Germany's second largest region; warmer, drier (rain shadow of Hardt mountains); Mediterranean influence; broad range of varieties (Riesling, Grauburgunder, Dornfelder, Spätburgunder); richer, more flamboyant Riesling than Mosel or Rheingau.
  Great Grosses Gewächs sites: Forster Kirchenstück, Deidesheimer Hohenmorgen.

Nahe: Small region of extraordinary geological diversity (porphyry, slate, sandstone, quartzite); this diversity produces Rieslings of unusual mineral complexity. Dönnhoff is the benchmark estate.

Franken (Franconia): Silvaner dominant (unusual in Germany — most regions are Riesling); bottled in the distinctive squat Bocksbeutel flask; earthy, mineral, high acid, smoky; Würzburg is the centre.

Baden: Southernmost; warmest; Spätburgunder (Pinot Noir) of note; Kaiserstuhl (volcanic basalt soils).

Other regions: Rheinhessen (Germany's largest; Liebfraumilch origin; Flörsheim-Dalsheim, Westhofener Kirchspiel GG), Württemberg, Mittelrhein, Ahr (cool, north; Spätburgunder specialist — Germany's best Pinot Noir), Saale-Unstrut and Sachsen (easternmost, former East Germany).

AUSTRIA

WACHAU (DAC — Districtus Austriae Controllatus):
Steep (up to 70°) granite and gneiss terraces on the Danube; Grüner Veltliner and Riesling; the most prestigious Austrian wine region. The Wachau has its own classification (not the official Prädikat system):
  Steinfeder: Lightest; max 11.5% ABV; delicate, for early drinking (named after the stipa grass that grows in the vineyards).
  Federspiel: Medium weight; 11.5–12.5% ABV; elegant, accessible (named after the falconer's lure — the falcon that hunts along the Danube).
  Smaragd: Richest; min 12.5% ABV (often 13.5–15%); from fully ripe, late-harvested grapes; concentrated, age-worthy; the summit of Wachau quality (named after the emerald lizard found on the terraces).
Key villages: Spitz, Weißenkirchen, Dürnstein, Loiben, Unterloiben (F.X. Pichler's home village).
Key producers: F.X. Pichler (the most coveted), Domäne Wachau, Knoll, Alzinger, Hirtzberger, Prager.

KREMSTAL and KAMPTAL (both DAC):
Adjacent to Wachau; similar varieties; slightly cooler due to wind from the north (Kamptal especially — the famous Kamp valley wind); Loess and loam soils replace Wachau's granite; slightly richer, rounder Grüner Veltliner.
Key producers: Kamptal — Bründlmayer (benchmark for Kamptal GV and Riesling), Hirsch, Loimer, Schloss Gobelsburg. Kremstal — Salomon-Undhof, Stadt Krems.

BURGENLAND (Neusiedlersee area):
Pannonian plain; the Neusiedlersee lake creates autumn fog = ideal conditions for Botrytis cinerea; home of Austria's finest sweet wines. Ruster Ausbruch (historic classification from the town of Rust — one of Austria's oldest wine designations; semi-dried/botrytised grapes). Trockenbeerenauslese and Beerenauslese production.
Also: Blaufränkisch (Austria's most important red variety) — from Mittelburgenland and Eisenberg DAC; dark, spicy, iron, black pepper, cherry; excellent structure.
Key producers: Kracher (TBA and BA benchmark; 'Nouvelle Vague' — barrel-fermented; 'Zwischen den Seen' — steel tank), Feiler-Artinger, Ernst Triebaumer.

DAC SYSTEM: Austria's quality classification system. When a wine qualifies as DAC (meets variety and style requirements for that region), it uses the regional name. If it doesn't qualify, it falls to 'Niederösterreich' or 'Wien' regional designation. Not all Austrian regions are DAC yet — the system is still being implemented.

WIEN (Vienna): The world's largest wine-producing capital city; Gemischter Satz (field blend — multiple varieties planted, harvested, and fermented together, a pre-modern practice preserved in Vienna); Riesling from Nussberg and Bisamberg.""",

"common_mistakes": """1. Treating Prädikat level as a sweetness level rather than a must weight at harvest — a Spätlese Trocken is dry; a Kabinett with high residual sugar is sweeter than a Spätlese Trocken. The Prädikat indicates harvest intensity, not the wine's sweetness.
2. Not knowing the VDP classification system — German wines labelled with the VDP eagle are classified by site quality (Grosse Lage, Erste Lage), not by Prädikat. A VDP.Grosses Gewächs is always dry; this distinguishes it from a Spätlese with Prädikat designation.
3. Confusing Mosel with Rheingau structurally — Mosel Riesling: lighter, more delicate, higher acid, lower alcohol (slate soils, steep terraces); Rheingau Riesling: fuller, broader, slightly more powerful (fuller sun exposure, loam soils).
4. Missing the Wachau classification — Steinfeder/Federspiel/Smaragd is a voluntary classification used only in the Wachau; it does NOT use the Austrian Prädikat system. A Smaragd is not equivalent to a Spätlese; it is a dry wine of maximum ripeness.
5. Assuming all Austrian wine is Grüner Veltliner — Austria also produces world-class Riesling (particularly Wachau and Kamptal), excellent Blaufränkisch (red), and some of the world's greatest botrytised wines from Burgenland.
6. Not knowing Egon Müller as the benchmark for Mosel — the Scharzhofberg TBA from Egon Müller regularly achieves the highest per-bottle auction prices of any white wine globally. The estate (Weingut Egon Müller-Scharzhof, in the Saar) is the definitive benchmark.
7. Forgetting that Eiswein requires natural freezing on the vine — Ice Wine from Canada (Inniskillin) uses the same concept but different production scale and climate. German Eiswein is rare; Canadian Ice Wine is more commercially available. Never confuse them.
8. Overlooking Ahr for Spätburgunder — Germany's northernmost region (Ahr Valley, red wine specialist) produces some of Germany's finest Pinot Noir. It is obscure but testable at MS level.""",

"pro_tips": """1. Build a mental map of Germany's 13 regions ordered by latitude and climate: Ahr (northernmost, coolest) → Mosel → Nahe → Rheingau → Rheinhessen → Pfalz (southernmost warm major region) → Baden (southernmost). Temperature increases south; this maps to wine style.
2. The Oechsle scale is the German sugar measurement: 1 Oechsle = 1g per litre of must above water weight. At TBA levels (150+ Oechsle), the must is thick as syrup. Know that 72 Oechsle = approximately 9.5% potential alcohol.
3. F.X. Pichler is the most consistently testable Austrian producer — know that his Riesling and Grüner Veltliner from Loiben (Wachau Smaragd) are reference wines, and that his 'M' designation (the top cuvée above Smaragd in his classification) represents the pinnacle of Wachau white wine.
4. For blind tasting: Mosel Riesling fingerprint — pale lemon-green colour, delicate nose (white flower, citrus blossom, slate), high acid, light body, off-dry balance (RS typically 15–30 g/L in QmP styles), slate/mineral finish, low alcohol (8–10%). Almost nothing else shares this profile.
5. Austrian Grüner Veltliner fingerprint: medium gold, white pepper (the defining aromatic marker — peppery/vegetal note from rotundone compound), citrus, green herb, high acid, mineral finish, dry. If you smell white pepper on a white wine, Grüner Veltliner is the primary hypothesis.
6. Know Germany's great vintages: 2019 (extraordinary across all regions), 2015 (Riesling excellence), 2001, 1971, 1959 (historic). Great vintages in Germany often produce Auslese, BA, or TBA in regions that may not achieve this in lesser years.
7. The Mosel's great village ladder: Trittenheim → Piesport → Brauneberg → Bernkastel → Graach → Wehlen → Zeltingen → Ürzig → Erden. Know the flow of the river and that the best sites are always on the south-facing river-bend terraces.
8. Study the DAC system for Austria: as of 2026, fully operational DAC regions include Wachau (uses its own Steinfeder/Federspiel/Smaragd system, not DAC formally), Kamptal DAC, Kremstal DAC, Weinviertel DAC (Grüner Veltliner focus), Traisental DAC, Mittelburgenland DAC (Blaufränkisch), Leithaberg DAC, Neusiedlersee DAC, Eisenberg DAC, Rosalia DAC, Carnuntum DAC, Wien DAC, Vulkanland Steiermark DAC, Weststeiermark DAC, Südsteiermark DAC.""",
"trigger_keywords": json.dumps(["Germany wine", "Austria wine", "Mosel", "Riesling", "Wachau", "Grüner Veltliner", "Prädikat", "VDP", "TBA", "MS exam Germany Austria"])
},

{
"name": "MS Theory — New World Wine Regions",
"slug": "ms-theory-new-world-wine-regions",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Society of Wine Educators",
"description": """New World wine regions — defined broadly as wine-producing countries outside Europe and the Middle East — present the MS candidate with the challenge of studying developing classification systems, diverse climates, and young wine cultures that have evolved rapidly since the 1960s and 1970s. The key insight for New World study: quality is increasingly site-specific rather than producer-driven, and the best producers in each region have identified their great terroirs through 30–50 years of observation. The MS exam expects this terroir-level knowledge for California, Oregon, and Washington at minimum, with less granular but still substantive knowledge of Australia, New Zealand, South Africa, Argentina, and Chile.

New World wines in the MS practical tasting exam are characterised by: higher alcohol levels (typically 13.5–15.5%), riper fruit (black and tropical rather than red and green), less earth and mineral, and more prominent new oak in premium expressions. At Master level, the candidate must identify not just 'New World Cabernet Sauvignon' but distinguish Napa Valley Cabernet from Margaret River Cabernet from Coonawarra Cabernet — each has a structural and aromatic fingerprint.""",

"key_principles": """CALIFORNIA

NAPA VALLEY (AVA — American Viticultural Area):
The most prestigious single wine valley in the New World. Cabernet Sauvignon dominant for reds; Chardonnay for whites. Classified in 2021 with the introduction of named sub-AVAs with measurable specificity.
Key Sub-AVAs and their profiles:
  Rutherford (benchmark Cabernet; 'Rutherford Dust' — earthy, mineral, graphite character claimed by locals; valley floor gravelly loam): Beaulieu Vineyard, Inglenook (Francis Ford Coppola), Rubicon Estate.
  Oakville (the most concentrated, powerful Napa Cabernet; deep alluvial, well-drained soils; Opus One's home): Harlan Estate, Screaming Eagle, Opus One, Far Niente, Robert Mondavi To Kalon.
  Stags Leap District (more elegant, silky-textured Cabernet; famous for the 1976 Paris Tasting victory; volcanic Palisades soils): Stag's Leap Wine Cellars (S.L.V. and Cask 23), Shafer, Silverado.
  Howell Mountain (mountain AVA; elevation 400–700m; volcanic ash soils; high tannin, concentrated, needs long ageing): Dunn Vineyards.
  Mount Veeder (volcanic, poor soils; garrigue/herbaceous Cabernet character): Hess Collection.
  Spring Mountain (steep slopes; mineral, structured): Smith-Madrone, Spring Mountain Vineyard.
  St. Helena (transition between Rutherford and Calistoga; classic valley floor structure).
  Calistoga (northernmost, hottest; powerful, structured Cabernet; Saralee's Vineyard area).
  Carneros (southernmost, coolest — San Pablo Bay influence; Pinot Noir and Chardonnay specialist; Domaine Carneros, Etude).
  Coombsville: Newest major Napa sub-AVA; volcanic soils; cool; emerging quality for Cabernet and Chardonnay.

SONOMA COUNTY:
Larger and more diverse than Napa; many AVAs with distinct characters.
  Russian River Valley (RRV): Cool, foggy; Pinot Noir benchmark in California; Williams Selyem, Rochioli, Dutton-Goldfield, Littorai; also exceptional Chardonnay.
  Sonoma Coast: Broader AVA including RRV; the 'true' Sonoma Coast (ocean-visible vineyards) is extremely cool; Hirsch Vineyards, Peay, Ceritas.
  Dry Creek Valley: Zinfandel heartland; old-vine Zin on benchland terraces; Ridge Lytton Springs, Seghesio.
  Alexander Valley: Warmer; Cabernet, Merlot; Clos du Bois, Stonestreet.
  Sonoma Valley: Warm; Cabernet, Zinfandel, Syrah; Ravenswood, Benziger.

CENTRAL COAST:
  Santa Cruz Mountains: Cool hillside vineyards; Ridge Monte Bello (one of California's finest Cabernets — limestone, mineral, restrained); Mount Eden.
  Monterey: Cool; Chardonnay, Pinot Noir in Santa Lucia Highlands AVA (Pisoni Vineyard, Paraiso).
  Paso Robles: Hot, inland; increasingly important; Rhône varieties (Grenache, Syrah, Mourvèdre) and Cabernet; Saxum, Justin, Halter Ranch; Adelaide District sub-AVA (limestone).
  Santa Barbara County: Cool; Santa Maria Valley (Bien Nacido Vineyard), Santa Ynez Valley, Sta. Rita Hills AVA (Pinot Noir specialist; Sanguis, Brewer-Clifton, Sea Smoke, Melville).

OREGON
Willamette Valley: The defining Oregon AVA; cool climate (similar latitude to Burgundy); Pinot Noir dominant; Chardonnay gaining significance.
  Nested AVAs: Dundee Hills (red volcanic Jory soil — iron-rich, excellent drainage; Domaine Drouhin Oregon, Adelsheim, Archery Summit) · Chehalem Mountains · Ribbon Ridge (Bergström, Trisaetum) · Eola-Amity Hills (ancient sea bed, marine sedimentary; WillaKenzie Estate; the coolest of the named AVAs, Pinot Noir of great precision) · McMinnville AVA · Van Duzer Corridor (unique ocean wind gap — very cool; Benton-Lane).
Style: Oregon Pinot Noir sits between Burgundy (more elegant, lower alcohol) and California (riper fruit); at its best, achieves a Burgundy-like precision at lower cost; at its worst, is thin and underripe (cool vintages) or over-extracted (warm vintages trying to replicate California).
Key producers: Domaine Drouhin Oregon (Veronique Drouhin trained), Eyrie (the pioneer — David Lett planted Pinot in Willamette in 1965), A to Z Wineworks (value), Beaux Frères (Robert Parker's brother-in-law), Ponzi, Chehalem.

WASHINGTON STATE
Columbia Valley: Vast AVA covering most of eastern Washington; dry, desert-like; Cascade Mountains block Pacific rain; irrigation essential; diurnal temperature variation (hot days/cold nights at 46°N latitude) preserves acidity.
  Walla Walla Valley: Bisected by WA/OR border; benchmark for Washington Cabernet, Merlot, Syrah; alluvial/loess soils; Leonetti (the founding estate), L'Ecole No. 41, Cayuse (volcanic basalt at Rocks District — a sub-appellation within Walla Walla that is among the most exciting American terroir discoveries of the 21st century; cobblestone river deposits, Syrah of extraordinary mineral depth).
  Red Mountain AVA: The hottest, driest sub-AVA; highest Brix at harvest; Cabernet Sauvignon of extreme concentration; Kiona, Col Solare, Hedges.
  Yakima Valley: Diverse soils; Riesling and Chenin Blanc succeed as well as reds; Chinook.
  Horse Heaven Hills: South-facing slopes above Columbia River; Champoux Vineyard (one of WA's most prized).
Washington vs Oregon: Washington reds tend to be riper, higher alcohol, more structured and tannic than Oregon; Washington's best Cabernet and Merlot are competitive with Napa.

AUSTRALIA
Barossa Valley: South Australia; the spiritual home of Australian Shiraz; old-vine (100–150 years) Shiraz of enormous depth and concentration; Penfolds Grange (Australia's most famous wine — national treasure, aged in American oak), Two Hands, Torbreck, Henschke (Hill of Grace — single vineyard 150-year-old vine Shiraz; the benchmark of Australian wine).
McLaren Vale: South Australia; 30km south of Adelaide; warmer, Mediterranean; Grenache and Shiraz; chocolate/coffee notes alongside fruit.
Coonawarra: South Australia; famous terra rossa (red iron-rich clay over limestone); Cabernet Sauvignon specialist; pencil cedar, eucalyptus, restrained; Wynns, Hollick, Bowen Estate.
Margaret River: Western Australia; isolated; maritime climate (cool, consistent); Cabernet Sauvignon and Chardonnay benchmarks; Cape Mentelle, Leeuwin Estate (Art Series Chardonnay — Australia's most prestigious Chardonnay), Moss Wood, Cullen.
Yarra Valley: Victoria; cool; Pinot Noir and Chardonnay; Yering Station, De Bortoli Noble One (Semillon botrytis), Coldstream Hills.
Hunter Valley: New South Wales; hot, humid, controversial; Semillon (at low alcohol, with age develops extraordinary honeyed, toast complexity) and Shiraz; McWilliams Mount Pleasant, Tyrrells.
Clare Valley and Eden Valley: South Australia; cool high-altitude; Riesling specialists (lime, toast, mineral, petrol with age); Jim Barry (The Armagh Shiraz), Grosset (Poland Hill — Clare benchmark), Pewsey Vale (Eden Valley).
Tasmania: Island; coolest Australian wine region; sparkling wine; Pinot Noir; Pipers River, Jansz, Josef Chromy.

NEW ZEALAND
Marlborough: South Island; Sauvignon Blanc capital of the world; characteristic pyrazine (capsicum, asparagus), passion fruit, citrus character; 'cat's pee on a gooseberry bush' historical descriptor; Cloudy Bay (put NZ SB on the world map), Seresin, Dog Point, Greywacke.
Central Otago: Southernmost major wine region on earth; 45°S latitude; extreme continental climate; Pinot Noir specialist; schist soils; Felton Road (benchmark), Ata Rangi, Rippon, Two Paddocks. Style: richer, darker Pinot than Burgundy, with concentration and spice.
Hawke's Bay: North Island; warmer; Syrah and Bordeaux-style blends (Gimblett Gravels sub-region — free-draining shingle; Craggy Range, Trinity Hill).
Martinborough: Transition climate; Pinot Noir; Ata Rangi (original location), Martinborough Vineyard.

SOUTH AFRICA
Stellenbosch: The Napa Valley of South Africa; diverse soils (granite, Table Mountain Sandstone, schist); Cabernet Sauvignon, Pinotage, Chenin Blanc (the dominant white variety nationally — called Steen historically), Chardonnay; Kanonkop (benchmark for Pinotage and Cabernet), Rustenberg, Warwick.
Swartland: The new quality frontier; dry-farmed old vines (bush vines); Chenin Blanc, Cinsault, Grenache, Syrah; Eben Sadie (Sadie Family Wines — the most talked-about producer in SA); the 'Swartland Revolution' (2010 onwards) completely changed perceptions of South African wine.
Constantia: Cape Town; historical importance (the 18th-century sweet Vin de Constance was the most famous wine in the world — sent to Napoleon in exile on St Helena); Klein Constantia and Groot Constantia.
Walker Bay: Cool (Atlantic); Pinot Noir and Chardonnay; Bouchard Finlayson, Hamilton Russell (benchmark for SA Pinot Noir and Chardonnay).

ARGENTINA
Mendoza: 70% of Argentine wine production; high altitude (800–1800m) with Andes range providing irrigation; Malbec specialist; Luján de Cuyo and Maipú (lower altitude, established Malbec); Uco Valley (high altitude, 1000–1400m+ elevation; cooler, more precise; the emerging quality frontier of Argentine Malbec; Zuccardi Valle de Uco, Catena Zapata Adrianna Vineyard — ranked world's best vineyard by multiple publications).
Torrontés: Argentina's signature aromatic white — Salta province (highest vineyards in the world, 2500m); intensely floral (Gewurztraminer-like), low acid, dry.

CHILE
Maipo Valley: Just south of Santiago; Cabernet Sauvignon benchmark (Concha y Toro Almaviva, Don Melchor); Alto Maipo (high altitude within valley, more precise).
Casablanca and San Antonio/Leyda (the latter at sea level, very cold): White wine specialists — Sauvignon Blanc and Chardonnay.
Colchagua Valley: Warmer; Carménère (Chile's signature red variety; genetically the 'lost' Bordeaux variety identified in Chile in 1994 — previously thought extinct); also Syrah; Casa Lapostolle.
Bío-Bío and Malleco: Southernmost Chilean wine regions; cool; Pinot Noir and Riesling; País (the historic mission grape) used by natural wine producers.""",

"common_mistakes": """1. Treating all Napa Cabernet as identical — sub-AVA variation is significant and testable: Rutherford (graphite, earthier), Oakville (concentrated, powerful), Stags Leap (silky, elegant), Howell Mountain (austere, tannic), Carneros (cool, lighter).
2. Confusing Oregon and Washington style profiles — Oregon Pinot Noir is cool, elegant, Burgundy-adjacent; Washington Cabernet and Merlot are warm, concentrated, and structured. They are fundamentally different.
3. Not knowing that Carménère was 'discovered' in Chile in 1994 — until DNA analysis, it was grown and sold as Merlot. It is now Chile's signature variety with its own identity.
4. Missing that New Zealand makes world-class Pinot Noir in Central Otago alongside its famous Marlborough Sauvignon Blanc — the SB dominance overshadows the Otago Pinot quality in exam preparation.
5. Treating all Australian Shiraz as Barossa in style — Barossa (warm, concentrated, American oak); McLaren Vale (chocolate/coffee); Margaret River (no Shiraz benchmark); Clare/Eden Valley (cooler, more elegant). Each region has a distinct profile.
6. Conflating South African Chenin Blanc (crisp, high-acid, versatile) with Loire Chenin Blanc — South African Chenin (called Steen historically) tends to be drier, less prone to botrytis sweet wine production, and more neutral in style.
7. Overlooking the Swartland — for MS theory, the Swartland Revolution (Eben Sadie, Andrea and Chris Mullineux, Donovan Rall) is required knowledge; this movement established South Africa as a fine wine nation.
8. Treating the Uco Valley as the same as lower-altitude Mendoza — Uco Valley (1000–1400m+) Malbec is structurally different: higher acidity, more aromatic precision, less jammy than valley-floor Mendoza.""",

"pro_tips": """1. For the MS tasting exam on New World reds: New World Cabernet Sauvignon fingerprint vs Old World: New World = black fruit dominant, mint/eucalyptus sometimes (Napa, SA), prominent new oak, higher alcohol (14–15%), less earth/mineral, riper tannin.
2. Build a mental grid for California: Napa vs Sonoma for reds (Napa = Cabernet power; Sonoma/RRV = Pinot elegance), then within Napa, the sub-AVA temperature map (Carneros cool, Calistoga hot).
3. For Australia: learn the Penfolds range as a quality ladder. Grange = Barossa Shiraz pinnacle; Bin 707 = Cabernet; RWT = Barossa Shiraz French-oaked (contrast with Grange's American oak); Yattarna = 'White Grange' (Chardonnay).
4. Hill of Grace (Henschke, Eden Valley, 150-year-old Shiraz) is Australia's other iconic wine alongside Grange — know it, know the vineyard history (planted 1860 by Silesian immigrants), and know it is single-vineyard (unlike Grange, which is a multi-region blend).
5. Washington State's 'Rocks District of Milton-Freewater' within Walla Walla is the most exciting American terroir discovery of the last decade — cobblestone glacial flood deposits, Syrah of mineral, iron, and dark fruit depth. Study Cayuse Vineyards as the benchmark.
6. For Chile: the 2006 Casa Marín and the rise of coastal Chilean wine (Leyda, San Antonio) established that Chile can produce elegant, precise Sauvignon Blanc and Chardonnay, not just warm-climate Carménère.
7. For Argentina: the Adrianna Vineyard (Catena Zapata, Gualtallary, Uco Valley, 1450m) is arguably the most discussed single vineyard in the New World. The Amy Egret and White Bones Chardonnays from this vineyard consistently rank among the world's finest whites.
8. Know the 1976 Paris Tasting (Judgment of Paris — Steven Spurrier's blind tasting): Stag's Leap Wine Cellars SLV 1973 beat all French reds; Chateau Montelena Chardonnay 1973 beat all French whites. This event is foundational to New World wine legitimacy and is testable at MS level.""",
"trigger_keywords": json.dumps(["New World wine", "California wine", "Napa Valley", "Oregon Pinot Noir", "Washington State", "Australia wine", "New Zealand", "South Africa", "Argentina Malbec", "MS exam New World"])
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    errors = 0
    for e in ENTRIES:
        try:
            cur.execute(SQL, (
                e["name"], e["slug"], e["category"], e["tier_level"],
                e["authority_tier"], e["source_book"],
                e["description"], e["key_principles"],
                e["common_mistakes"], e["pro_tips"],
                e["trigger_keywords"]
            ))
            inserted += 1
        except Exception as ex:
            print(f"ERROR on {e['slug']}: {ex}")
            conn.rollback()
            errors += 1
            continue
        conn.commit()
    cur.close()
    conn.close()
    print(f"Done. {inserted} inserted, {errors} errors.")

if __name__ == "__main__":
    main()
