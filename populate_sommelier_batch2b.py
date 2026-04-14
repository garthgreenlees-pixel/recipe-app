#!/usr/bin/env python3
"""Canon 4 Batch 2b — entries 13-15: Spirits, Beer, Sake comprehensive"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO technique_references
  (name,slug,category,tier_level,authority_tier,source_book,
   description,key_principles,common_mistakes,pro_tips,trigger_keywords)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

ENTRIES = [

{
"name": "MS Theory — Spirits Comprehensive",
"slug": "ms-theory-spirits-comprehensive",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / WSET Spirits",
"description": """Every Master Sommelier must command spirits knowledge equal to their wine knowledge. The MS theory exam tests spirits across production, regulation, region, and flavour profile. The practical exam may require blind evaluation of a spirit flight. For most candidates, spirits represent the largest knowledge gap — the production chemistry of distillation, the regional regulations for Cognac and Scotch, the agave science of tequila and mezcal — are disciplines requiring dedicated study distinct from wine.

The central principle of spirits knowledge: flavour derives from four sources — base material (grain, grape, agave, sugarcane), fermentation character (yeast strains, fermentation time, temperature), distillation method and cut points (pot vs column, what is retained in the spirit), and maturation (barrel type, size, time, warehouse conditions). A Master Sommelier can trace any spirit's flavour profile back to these four sources.""",

"key_principles": """SCOTCH WHISKY (Scotch Whisky Regulations 2009)
Definition: Must be made in Scotland, from cereal grains, water, and yeast; aged minimum 3 years in oak casks (max 700L); min 40% ABV at bottling; no added substances except water and caramel (E150a) for colour; must express the aroma, taste, and character of Scotch whisky.
Five categories: Single Malt Scotch (from one distillery, malted barley only, pot stills), Single Grain Scotch (from one distillery, other cereal grains, usually column stills), Blended Malt (blend of single malts from multiple distilleries — formerly Vatted Malt), Blended Grain, Blended Scotch (blend of malt and grain whiskies — the commercial mainstream: Johnnie Walker, Chivas Regal, Dewar's).

Regions (flavour profiles):
  Speyside (70+ distilleries — the most concentrated): Fruit-forward, malty, often sherry-influenced; restrained peat; range from light and floral (Glenfiddich, The Glenlivet) to rich and complex (Macallan, Glenfarclas, GlenDronach). Benchmark expressions: The Macallan 18yr Sherry Oak, Glenfarclas 105.
  Highlands (most geographically diverse): Hard to generalise; includes everything from maritime (Clynelish — waxy, coastal) to heather honey (Dalmore) to robust (Glenmorangie — lightest highland distillate, multiple wood finishes). Sub-region Orkney: Highland Park (balanced — heather, smoke, maritime, honey) and Scapa.
  Islay (the peat island): Medicinal, smoky, maritime. Phenol levels (PPM) key: Caol Ila (35 ppm), Lagavulin (35 ppm), Ardbeg (25 ppm unpeated through to very peated); Laphroaig (40–45 ppm; iodine, seaweed, hospital); Bruichladdich (Octomore — world's most heavily peated at 167–258 ppm depending on edition; paradoxically the smoke is balanced by sweetness). Kilchoman (farm distillery; intensely peated but with sweetness). Bunnahabhain (lightest Islay — unpeated, nutty, maritime without heavy smoke).
  Campbeltown: Only 3 distilleries; Springbank (also Longrow = heavily peated; Hazelburn = triple distilled, unpeated; and Springbank = lightly peated); briny, oily, complex.
  Lowlands: Light, gentle, grassier, floral; triple distillation was traditional (Auchentoshan); Glenkinchie (delicate, light).
  Islands (not a formal SWR region): Talisker (Skye — peppery, marine, peated, distinctive); Jura, Arran, Tobermory.

Key production variables: Pot stills (size, shape — tall narrow still = lighter spirit; short squat = heavier, more oily/fruity), copper contact (removes sulfur), worm tubs vs condensers (worm tubs = heavier spirit — Mortlach, Springbank), percentage of new vs refill oak, sherry vs bourbon cask (sherry = dried fruit, chocolate, spice; bourbon = vanilla, caramel, coconut), cask size (first-fill barrel vs hogshead vs butt).

BOURBON AND AMERICAN WHISKEY (US Federal Standards of Identity)
Bourbon must: Be made in the USA (not just Kentucky); from a grain mash of minimum 51% corn; distilled to no higher than 160 proof (80% ABV); entered into barrel at no more than 125 proof (62.5% ABV); aged in new, charred oak containers (no minimum age requirement for Bourbon, except Straight Bourbon = 2+ years; if under 4 years, age must be stated on label).
Tennessee Whiskey (Jack Daniel's, George Dickel): Meets all bourbon requirements PLUS Lincoln County Process (charcoal mellowing — spirit dripped through 10 feet of sugar maple charcoal before barrelling). Some consider it a sub-category of Bourbon; Tennessee producers disagree.
Key Mash Bills: High corn (79–86%+ corn): Buffalo Trace, Wild Turkey, Jim Beam — sweet, caramel, vanilla. Rye-forward (high rye — 18–35% rye): Four Roses (10 recipes including OBSV = high rye, fruity yeast), Bulleit, Knob Creek — spice, dill, pepper. Wheated (wheat replaces rye): Maker's Mark, W.L. Weller, Pappy Van Winkle — soft, approachable, bread, vanilla, gentle spice.
Small batch vs single barrel vs cask strength: Small batch = limited number of barrels blended; Single barrel = one barrel, naturally more variation; Cask strength / Barrel proof = uncut and unfiltered.
Rye Whiskey (Federal): Minimum 51% rye grain; new charred oak; more spicy, herbal, dry than bourbon. Rittenhouse, Sazerac Rye, WhistlePig.

IRISH WHISKEY
Regulations: Made in Ireland; minimum 3 years aged in wooden casks (any wood); min 40% ABV; must retain character of aroma, taste from raw materials.
Four categories: Single Malt (pot still, malted barley, one distillery), Single Pot Still (mixture of malted and UNMALTED barley in pot still — the defining Irish style, producing a distinctive creamy, spicy, oily texture; Redbreast, Green Spot, Yellow Spot, Midleton Very Rare), Single Grain (column still, mixed grains), Blended (most commercial Irish: Jameson, Bushmills, Tullamore D.E.W.).
Triple distillation: Jameson and most commercial Irish are triple-distilled (pot still or column); produces a lighter, smoother spirit.

JAPANESE WHISKY
No legal standard until 2024 (Japan Spirits and Liqueurs Makers Association established rules 2024 — must be made in Japan from Japanese water, aged minimum 3 years). Previously some 'Japanese' whiskies contained Scottish or Canadian whisky.
House styles: Suntory (The Yamazaki — Japan's first distillery 1923; stone fruit, Japanese oak/Mizunara gives distinctive sandalwood/incense note; Hibiki = blended); Nikka (Yoichi — peated, maritime, more robust; Miyagikyo — lighter, floral, fruity; Taketsuru = blended).
Key innovation: Mizunara (Japanese oak) barrels impart unique sandalwood, coconut, incense, oriental spice character unlike any European or American oak. Extremely rare and expensive.

COGNAC (AOC Cognac)
Grapes: Ugni Blanc (Trebbiano) dominant (90%+ of plantings); also Folle Blanche, Colombard.
Production: Double distillation in copper pot stills (Charentais alembic); distilled off the lees; aged in Limousin or Tronçais oak barrels in the Charente region.
Six crus (ranked quality): Grande Champagne (chalk — finest; most age-worthy, longest to develop: Rémy Martin XO, Frapin, Ragnaud-Sabourin) · Petite Champagne (slightly less chalk) · Borderies (clay-chalk, develops fastest, violets aroma, round and supple — Rémy Martin uses a high proportion) · Fins Bois · Bons Bois · Bois Ordinaires.
Age designations (time in oak): VS (Very Special — min 2 years) · VSOP (Very Superior Old Pale — min 4 years) · XO (Extra Old — min 10 years since 2018; previously 6 years) · XXO (Extra Extra Old — min 14 years).
Fine Champagne = blend of Grande and Petite Champagne with minimum 50% Grande.
Key producers: Hennessy (largest; bold, robust house style), Rémy Martin (Grande Champagne and Borderies blend; floral, elegant), Martell (Borderies specialist; lighter, fruitier), Courvoisier, Delamain (pale, dry, Grande Champagne specialist), Prunier, Pierre Ferrand.

ARMAGNAC (AOC Armagnac):
Gascony (southwest France); primary difference from Cognac: single continuous distillation in an Armagnac alembic (column still at low proof ~55% ABV) vs double pot-still distillation → more congeners → more rustic, characterful, complex spirit.
Three crus: Bas-Armagnac (sandy soils, finest; most delicate and fruity), Ténarèze (clay-limestone, middle quality), Haut-Armagnac (chalk, declining). Grape varieties: Ugni Blanc, Colombard, Folle Blanche, Baco Blanc (hybrid, most planted in Bas-Armagnac — rich, prune-like).
Single vintage Armagnac is common (unlike Cognac); great vintages (1893, 1914, 1928, 1982, 1988) survive for 80–100 years.

CALVADOS (AOC):
Apple and pear brandy from Normandy, France. Three AOC sub-regions: Calvados (largest; column distilled), Calvados Pays d'Auge (pot still double distilled; finest; Boulard, Roger Groult), Calvados Domfrontais (minimum 30% pear; column distilled). Aged in Limousin oak. Age designations: Fine/VS (2 years), VSOP/Vieux (3 years), XO/Hors d'Age (6+ years).

TEQUILA AND MEZCAL (NOM — Norma Oficial Mexicana)
Tequila: Blue Weber agave (Agave tequilana) only; five states (Jalisco dominant; also Guanajuato, Michoacán, Nayarit, Tamaulipas); minimum 51% agave sugars (mixto); 100% agave Tequila is higher quality; NOM number on each bottle identifies the producer facility.
  Regions: Highlands (Los Altos — red clay soil; richer, sweeter, floral agave; Patrón, El Tesoro) vs Valley/Lowlands (volcanic soil; more herbal, earthy, pepper agave character; Don Julio, Olmeca Altos).
  Age categories: Blanco/Silver (unaged or max 2 months in steel); Reposado (2 months–1 year in oak); Añejo (1–3 years); Extra Añejo (3+ years — the most expensive).
Mezcal: Any agave species (30+ varieties used); any state with the DO (Oaxaca dominant; also Guerrero, San Luis Potosí, Durango, Zacatecas, Tamaulipas, Michoacán, Puebla, Guanajuato); primarily Espadín (Agave angustifolia — 80% of mezcal production); also Tobalá, Tepeztate, Arroqueño, Mexicano and more.
  Production: Agave piñas roasted in earthen pit ovens over mesquite or other woods → crushed by tahona stone wheel or mechanically → fermented → distilled in clay or copper pot stills. Smoke from roasting is primary mezcal character.
  Categories: Joven (unaged), Reposado (2–12 months), Añejo (1–3 years); Ancestral (most traditional — clay pot still), Artisanal (wood or copper still), Mezcal (larger scale).

RUM (no single international definition — production varies enormously)
Key production methods: Column still (lighter rum; Bacardí style — most Cuban/PR-influenced), Pot still (heavier, more flavourful — Jamaican), or blended (both stills; Barbados — Cockspur, Mount Gay).
Major categories: Spanish-style (Cuba, Puerto Rico, Dominican Republic — column still, lighter, clean); English-style (Barbados, Trinidad, Guyana, Jamaica — heavier, pot still influence); French-style (Martinique, Guadeloupe — Rhum Agricole: from fresh sugarcane juice, not molasses; AOC Martinique is the only French AOC outside of France; must use specific agave varieties — wait, agave is for tequila; must use specific cane varieties and production methods).
Demerara Rum (Guyana — El Dorado Distillery, formerly Enmore and others): made from the sugar cane grown in the alluvial Demerara River delta; rich, dark, treacle, dried fruit; uses historic wooden pot stills including the Port Mourant double pot still and the Coffey still.
Jamaican high-ester rum: Measured in grams of esters per hectolitre of pure alcohol; Hampden Estate (most famous for high ester — HLCF mark = extremely funky, 800+ g/hlpa); Worthy Park; Appleton Estate. The funky, overripe fruit character comes from ester concentration.

GIN (no age requirement; minimum 37.5% ABV in EU)
London Dry: Neutral grain spirit redistilled with botanicals; no flavouring added after redistillation except water; juniper dominant. Major brands: Beefeater, Tanqueray, Gordon's, Sipsmith.
Plymouth Gin: Geographic designation (Plymouth, Devon); earthier, slightly sweeter than London Dry; less juniper-forward; Black Friars Distillery.
Old Tom: Slightly sweetened (traditionally); the 'missing link' between Genever and London Dry; used in classic cocktails (Tom Collins, Martinez).
Genever (Dutch gin — GI): Holland/Belgium; malt wine base (distilled from malt grain wine = whisky-like base); distilled with juniper; Jonge (young, lighter) vs Oude (old style — more malt character, traditional).
New Western / Contemporary: Reduced juniper; other botanicals dominant — Hendrick's (cucumber, rose), Monkey 47 (47 botanicals), Roku (Japanese botanicals: sakura, yuzu, sencha, sansho pepper), The Botanist (22 wild Islay botanicals), Malfy (Italian citrus).

VODKA: Neutral grain or potato spirit; minimum 40% ABV; filtered; virtually flavourless by legal definition in the EU. Grain vodka (wheat, rye, corn) tends slightly drier; potato vodka (Belvedere — technically wheat; Chopin, Luksusowa — potato) often perceived as creamier. Ultra-premium: Stolichnaya, Grey Goose, Belvedere, Crystal Head. Flavoured vodkas are a separate commercial category.

ABSINTHE: Distilled spirit with grand wormwood (Artemisia absinthium), green anise, and Florence fennel as the 'holy trinity' of botanicals; banned in much of the world 1905–2007 (myth: thujone in wormwood causes hallucinations — disproven; it was simply a convenient Temperance Movement target); revived since 2007. Blanche/Argentée (uncoloured), Verte (green, coloured by chlorophyll from herbs added post-distillation). Traditional service: water dripped over a sugar cube through an absinthe spoon. Thujone content in modern absinthe is regulated (max 10mg/kg in EU, 10ppm in USA).

BITTERS: Concentrated aromatic preparations of botanicals in alcohol; not typically drunk neat (with exceptions: Fernet-Branca, Amaro); used as modifiers in cocktails. Angostura (Trinidad — the most used cocktail bitter in the world; gentian, bark, spice); Peychaud's (New Orleans — fennel, anise — essential in the Sazerac); Orange bitters (Regans', Fee Brothers, Regan's No. 6). Amaro (Italian bitter liqueur — Campari, Aperol, Cynar, Averna, Fernet; herbal, bitter, digestive).""",

"common_mistakes": """1. Not knowing that Bourbon does NOT need to be made in Kentucky — it must be made in the USA, but no specific state is required. The 'Kentucky Bourbon' label is a legitimate geographic specification, not a requirement for the category.
2. Confusing Blended Scotch with Blended Malt — Blended Scotch (most common category: Johnnie Walker, Chivas) = Single Malts blended with Grain Whiskies. Blended Malt (formerly Vatted Malt: Compass Box, Monkey Shoulder) = multiple Single Malts, no grain whisky.
3. Thinking all Japanese whisky is now subject to Japanese regulations — the 2024 JSLMA rules only apply to member distilleries; non-member producers may still import and blend foreign whisky for Japanese-labelled products. Verification requires checking distillery membership.
4. Misidentifying Armagnac as Cognac — Armagnac is single-distilled in a continuous alembic (producing more congeners, more flavour), while Cognac is double pot-still distilled (lighter, more refined). The flavour difference is significant and detectable.
5. Treating mezcal as a flavoured or inferior tequila — mezcal is a separate category with distinct production (any agave species, earthen pit roasting, clay pot distillation for artisanal mezcal) that preceded the industrialisation of tequila production.
6. Forgetting the AOC Martinique Rhum Agricole designation — it is the only French AOC outside France's geographic borders; it specifies cane varieties, harvest dates, distillation proof, and ageing requirements. This is a testable MS fact.
7. Confusing the Cognac age designations with barrel age — VS means the youngest component is at least 2 years old in oak; it does not mean all components are 2 years old. A VSOP may contain components much older than 4 years.
8. Missing thujone reality on absinthe — the hallucination narrative is a myth. Modern scientific analysis of pre-ban absinthe shows thujone levels were never high enough to cause psychoactive effects. The ban was politically motivated (Temperance Movement). This is testable MS theory.""",

"pro_tips": """1. For Scotch blind evaluation: phenol PPM is the best proxy for smoke intensity. Build a mental scale: Glenfiddich ~0 ppm → Glenmorangie 0 → Auchentoshan 0 → Highland Park ~20 → Caol Ila 35 → Laphroaig 40–45 → Ardbeg 23 (unpeated versions) → Octomore 167+. Smoke intensity correlates with peating level, detectable on nose.
2. Know the Sazerac cocktail for the MS practical — it is one of the oldest cocktails in America (New Orleans, 1800s) and requires: Rye Whiskey (or Cognac in the original formula), Peychaud's Bitters, absinthe rinse, sugar. This tests knowledge of spirits categories simultaneously.
3. The Lincoln County Process (Tennessee whiskey) removes congeners that would otherwise produce a heavier, more rustic spirit — the charcoal mellowing (about 10 days of gravity filtration through maple charcoal) creates the mellower character that distinguishes Jack Daniel's from similar-mash-bill bourbon.
4. For the MS theory exam: memorise the six Cognac crus in order of quality (Grande Champagne → Petite Champagne → Borderies → Fins Bois → Bons Bois → Bois Ordinaires) and which major houses source primarily from which cru (Rémy Martin = Grande + Borderies blend; Delamain = Grande Champagne only).
5. Rancio — the walnut-like, oxidative, complex note in aged Armagnac and Cognac — is produced by esterification and oxidation reactions in extended barrel contact. It is the definitive quality indicator for fine brandy and should be specifically identified in any MS spirits evaluation.
6. The NOM system for Tequila (and Mezcal's CRM certification) are legal traceability systems — the NOM number on the bottle identifies the distillery, not the brand. Multiple brands may share a NOM (contract distilling). Knowing key NOM numbers (1122 = Herradura, 1079 = Patrón) demonstrates depth.
7. For Japanese whisky: Mizunara oak (Quercus mongolica) is extremely porous, difficult to work, and takes 200 years to grow to the right size — these properties make it expensive and rare. The sandalwood/incense/coconut character it imparts is unique and identifiable on the nose.
8. Genever is the ancestor of gin — Dutch merchants introduced it to England in the 17th century during the Thirty Years War ('Dutch courage' as British soldiers drank it before battle). London Dry gin developed later as a distinctly English style. This historical lineage is testable MS knowledge.""",
"trigger_keywords": json.dumps(["Scotch whisky", "Bourbon", "Cognac", "Armagnac", "Tequila", "Mezcal", "Rum", "Gin", "spirits knowledge", "MS exam spirits"])
},

{
"name": "MS Theory — Beer Comprehensive",
"slug": "ms-theory-beer-comprehensive",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Cicerone Certification Program",
"description": """Beer knowledge for the Master Sommelier exam is tested at a level comparable to the Certified Cicerone certification: understanding of brewing science, style history, ingredient function, flavour development, off-flavour identification, and service. The MS theory exam may ask candidates to recommend beer pairings, explain production differences between style families, or identify quality indicators for specific categories. The practical exam may include evaluation of a beer or beer-based beverage.

Beer is the world's most consumed alcoholic beverage and is increasing in prestige — the Cicerone certification programme (Certified Cicerone, Advanced Cicerone, Master Cicerone) mirrors the sommelier track in rigour and depth. Master Cicerone candidates undergo practical exams comparable in length and intensity to the MS examination. For the MS candidate who approaches beer as a secondary subject, the minimum competency required is: the major style families, production differences between them, off-flavour identification, and beer-food pairing logic.""",

"key_principles": """BREWING PRODUCTION FUNDAMENTALS

Ingredients:
  Water: The most important ingredient by volume. Water chemistry affects style fundamentally: high sulfate (Burton-on-Trent) accentuates hop bitterness and dryness — ideal for pale ale/IPA. Soft water (Pilsen) produces the delicate, rounded character of Czech Pilsner. High carbonate (Dublin) suits dark, roasted beers. Brewers 'Burtonise' (add gypsum = calcium sulfate) for hop-forward styles.
  Malt: Barley is malted (germinated, then kilned) to produce enzymes that convert starch to fermentable sugars. Kilning temperature and duration determine colour (SRM) and flavour: pale malt (lightest, most enzymes, base of most beers) → Munich malt (toasty, bready, golden colour) → crystal/caramel malts (residual sweetness, red-amber colour — added sweetness because starches are converted to unfermentable dextrins in the production process) → chocolate malt (dark brown, chocolate, coffee notes) → black patent malt/roasted barley (black, bitter, coffee/espresso; roasted barley is unmalted, gives distinctive dry, harsh roast of Irish Stout).
  Hops: Female flowers of Humulus lupulus. Used for bitterness (isohumulones from alpha acids), aroma (essential oils from hop cones), and as a preservative. Key varieties: Noble hops (Saaz — Pilsen, Czech; Hallertau Mittelfrüh — German; Tettnang — German; Spalt — German; characterised by low alpha acid, high aroma, spicy/floral/herbal). American hops (Cascade — grapefruit, floral; Centennial — citrus, floral 'Super Cascade'; Citra — tropical, citrus, passion fruit; Mosaic — complex tropical and earthy; Simcoe — pine, passion fruit; Amarillo — orange). British hops (Fuggles — earthy, tobacco; East Kent Goldings — gentle, floral, honey).
  Yeast: Saccharomyces cerevisiae (ale yeast — top fermenting, 15–25°C, produces esters and phenols) vs Saccharomyces pastorianus (lager yeast — bottom fermenting, 5–15°C, produces clean, neutral profile). Wild yeast: Brettanomyces (funk, barnyard, leather — intentional in Belgian sour, Lambic; fault in most other styles).

Brewing Process:
  Mashing: Crushed malted grain mixed with hot water (67–70°C for most beers). Enzymes (alpha and beta amylase) convert starch to fermentable sugars. Temperature affects fermentability: lower mash temp (64°C) = more fermentable (drier, lighter body); higher mash temp (70°C) = less fermentable (more residual sugar = fuller body, sweeter).
  Lautering: Separation of liquid wort from spent grain; the grain bed acts as a filter.
  Boiling: Wort boiled 60–90 minutes. Hop additions: bittering hops at 60+ minutes (maximum isohumulone isomerisation); flavour hops at 15–30 minutes; aroma hops at 0–5 minutes or whirlpool/hop stand; dry hopping (cold, post-fermentation) = maximum aroma, zero additional bitterness.
  Fermentation: Yeast pitched into cooled wort (18–22°C for most ales; 8–12°C for lagers). Primary fermentation 1–2 weeks (ales), 3–4 weeks (lagers). Secondary/conditioning: Ales at 10–14°C; lager conditioning (lagering) at 0–4°C for weeks/months.
  Packaging: Draught (cask conditioned = 'real ale' — live fermentation, lower CO₂, served at cellar temperature 12–14°C; or keg conditioned = filtered/pasteurised, CO₂/N₂ dispense), bottle (bottle-conditioned = with live yeast, secondary fermentation adds carbonation; filtered and force-carbonated = most commercial bottles), can.

BEER STYLE FAMILIES AND MS KNOWLEDGE REQUIREMENTS

LAGER FAMILY (bottom-fermented, cold-conditioned):
  German Pilsner: Pale straw, brilliant; Saaz or Hallertau hop (spicy, floral); crisp bitterness (IBU 25–45); clean, dry finish; low ABV (4.5–5.5%). Warsteiner, Bitburger, Jever (most bitter German Pils), König Pilsener.
  Czech Pilsner (Bohemian): Soft water (Pilsen); Saaz hops; noticeably fuller body and softer mouthfeel than German Pils; characteristic herbal/spicy hop aroma; slight residual sweetness; Pilsner Urquell (the original; unfiltered version = Pilsner Urquell unpasteurised/tankové pivo — exceptional).
  Munich Helles: Pale gold; malty and soft; less hop bitterness than Pilsner; Spaten, Augustiner, Hacker-Pschorr.
  Märzen / Oktoberfest: Amber; toasted malt; moderate bitterness; 5.5–6.5% ABV; lagered from March (Märzen = March beer) until the September Oktoberfest.
  Bock: Dark amber to mahogany; rich malt; low bitterness; 6.5–7.5% ABV; Einbecker, Paulaner Salvator.
  Doppelbock: Very dark; intensely malty (bread, toast, caramel, chocolate); 7–12% ABV; names traditionally ending in -ator (Salvator, Celebrator, Optimator); Paulaner, Ayinger, Andechs.
  Schwarzbier: 'Black beer' — dark brown/black; roasted character lighter than stout (no harsh roast); Köstritzer (Germany's most famous Schwarzbier).

ALE FAMILY (top-fermented, warmer fermentation):
  Pale Ale (British): Amber-gold; balanced malt and hop; 4–5.5% ABV; earthy, marmalade-ester character from British yeast; Fuller's London Pride, Timothy Taylor Landlord.
  IPA (India Pale Ale): Historically high-hopped British ales for India trade (hops preserved beer on the voyage). American IPA: citrus/pine/tropical; high bitterness (IBU 40–70+); dry; 6–7.5% ABV; Sierra Nevada Torpedo, Stone IPA. New England / Hazy IPA: Hazy/opaque from biotransformation (dry-hopping with specific yeast strains transforms hop compounds, creating thiol-driven tropical aroma); lower perceived bitterness; juicy, soft; Treehouse, Alchemist Heady Topper, Trillium.
  British Mild: Dark brown; low ABV (3–4%); caramel, toast, minimal bitterness; pub session beer; nearly extinct outside England.
  Porter: Dark brown; chocolate, coffee, caramel; 5–7% ABV; originally a London style (18th century blend of different aged beers → 'entire butt'); Fuller's London Porter, Anchor Porter.
  Stout — Dry Irish: Black, opaque; roasted barley (dry, espresso, bitter); NO residual sweetness (unlike Milk/Sweet Stout); low ABV (4–5%); Guinness Draught (nitrogen-dispensed, signature creamy head).
  Imperial Stout (Russian Imperial Stout): Black; extremely complex (coffee, chocolate, dark fruit, vanilla, liquorice, oak if barrel-aged); 9–14% ABV; aged in bourbon barrels dramatically for more complexity; Goose Island Bourbon County, North Coast Old Rasputin.
  Wheat Beer — Hefeweizen (Bavarian): Hazy gold; banana (isoamyl acetate), clove (4-vinyl guaiacol) from the Weihenstephan wheat yeast strain; low bitterness; high carbonation; soft mouthfeel; 5–5.5% ABV; Weihenstephaner, Paulaner, Schneider Weisse (spicier, darker). Clove character = 4VG from ferulic acid rest during mashing (50–55°C rest increases ferulic acid).
  Witbier (Belgian White): Hazy, pale; coriander, bitter orange peel (Belgian tradition); wheat and unmalted wheat; gentle spice and citrus; Hoegaarden (Pierre Celis's creation — revived the style), Blanche de Bruxelles.
  Saison (Belgian Farmhouse Ale): Golden to amber; fruity, spicy, earthy; highly carbonated; bone dry finish; high attenuation (very little residual sugar); originally brewed in winter for summer farmworker consumption; 5–8% ABV; Dupont Saison (the benchmark), Fantôme, Boulevard Tank 7.
  Belgian Single/Dubbel/Tripel/Quadrupel: Single = light, golden, for monks only (rarely commercialised). Dubbel = dark amber, dried fruit, caramel, moderate strength (6–8%). Tripel = pale gold, deceptively strong (8–10%), spicy, fruity, very dry despite strength; Westmalle Tripel (the defining example). Quadrupel/Abt = darkest, richest, most complex (10–14%); St. Bernardus Abt 12, Westvleteren 12 (often called 'the best beer in the world' — extremely limited distribution).
  Trappist Beers: 13 authorised Authentic Trappist Product (ATP) breweries worldwide. Belgian: Westvleteren, Chimay, Rochefort, Westmalle, Orval (unique — uses Brettanomyces for dryness; the only Trappist beer with deliberate Brett character), Achel, La Trappe (Netherlands), Spencer (USA), Engelszell (Austria), Cardeña (Spain), Tre Fontane (Italy), Tynt Meadow (UK), Sept (France). The 'Big Six': Westvleteren, Chimay, Rochefort, Westmalle, Orval, La Trappe.
  Lambic/Gueuze: Wild-fermented; no commercial yeast — open fermentation tanks (coolships) inoculated by wild Brettanomyces and Pediococcus bacteria; aged in oak wine barrels (often used Burgundy barrels) for 1–3 years; Gueuze = blend of 1, 2, and 3-year lambics (produces carbonation from residual fermentable sugars); Cantillon (Brussels — the benchmark), 3 Fonteinen, Tilquin, Boon. Lambic: sour, acidic, funky, complex; the world's only major beer style with no added commercial yeast.
  Berliner Weisse: Very low ABV (2.5–4%); tart, acidic (lactic fermentation); very pale; served with raspberry (Himbeersirup) or woodruff (Waldmeister) syrup in Berlin tradition; currently revived by craft brewers globally.
  Gose: Leipzig tradition; wheat beer + lactic fermentation + salt + coriander; unusual combination of sourness, salinity, and herb; nearly extinct, revived in the 2010s craft beer movement; pairs well with oysters.""",

"common_mistakes": """1. Not knowing the three Trappist beer tiers — Single, Dubbel, Tripel, Quad — and their flavour profiles. Westmalle Tripel and Westvleteren 12 are reference-level exam answers for Tripel and Quadrupel respectively.
2. Confusing IBU with perceived bitterness — IBU measures isoalpha acid concentration; perceived bitterness is modulated by malt sweetness, carbonation, body, and serving temperature. A Doppelbock with 25 IBU can taste less bitter than an IPA with 60 IBU due to malt sweetness balance.
3. Treating all Belgian ales as interchangeable — Saison (dry, spicy, farmhouse character), Tripel (golden, spicy, strong, dry), Dubbel (dark, dried fruit, moderate), Quad (darkest, richest, strongest) have fundamentally different flavour profiles despite shared Belgian heritage.
4. Missing the water chemistry knowledge — Burton water (high sulfate) vs Pilsen water (extremely soft) produce fundamentally different beers from the same grain and hops. This is a production question, not a flavour question; the science behind it is testable.
5. Confusing Porter and Stout stylistically — historically, Stout was a 'stouter' (stronger) Porter; today they are separate styles. The key difference: dry Irish Stout uses unmalted roasted barley (harsh, dry roast); Porter uses malted chocolate malt (smoother, sweeter roast).
6. Not knowing Orval as a unique Trappist style — Orval is the only Trappist beer to use Brettanomyces intentionally in the bottle; it evolves from a clean, hoppy amber at 6 months to a complex, funky, dry amber at 2–5 years. This is testable.
7. Treating Pilsner Urquell as just another lager — it is the original Pilsner (1842), the template for the world's most widely produced beer style, and still produced with traditional triple decoction mashing and open fermentation fermenters. The tankové (tank beer) version served unfiltered and unpasteurised is among the finest lager experiences available.
8. Missing the ferulic acid rest for clove character in Hefeweizen — the clove (4-vinyl guaiacol) characteristic is produced by the yeast converting ferulic acid (produced during a specific mashing rest at 45–50°C) into 4VG. Without the ferulic acid rest, minimal clove character. This enzymatic control is testable production knowledge.""",

"pro_tips": """1. The ABV/IBU relationship is the key to style identification: low ABV + low IBU = lager family session beers; high IBU + high ABV = IPA; high ABV + low IBU = Belgian strong ales (Tripel, Quad). Use this matrix as a deductive starting point.
2. Study the Reinheitsgebot (German Beer Purity Law, 1516) — it originally restricted German beer to water, barley, and hops only (yeast was unknown; it was added to the law later). Modern Reinheitsgebot still applies in Germany; this is why German beers cannot legally contain coriander or orange peel that make Witbier/Gose Belgian styles impossible to produce under German beer law.
3. For Master Sommelier beer pairing questions: bitterness cuts fat (IPA with fried food, unctuous dishes); acidity (Saison, Berliner Weisse, Gose) cuts richness; malt sweetness bridges spice (Märzen with spiced sausage); roasted character pairs with smoked/grilled flavours (Stout with oyster). These are logical, testable.
4. Understand cask vs keg dispense at the MS level: cask-conditioned 'real ale' is alive, low CO₂, served at 12–14°C, has a short shelf life (3–5 days after tapping), and has complex microbial character. Keg beer is filtered/pasteurised, force-carbonated, served colder (4–8°C), and is more commercially stable. A guest requesting a 'real ale' requires this knowledge.
5. Know that Cantillon (Brussels) and 3 Fonteinen (Beersel) are the two benchmark Lambic/Gueuze producers — visiting either is required for serious beer study. Cantillon's BKBK and Bruocsella (the plain lambic) are the entry points to understanding the style.
6. For the Cicerone exam (beer parallel of sommelier): the beer service section requires knowledge of draught line cleaning protocols (minimum every 2 weeks, ideally weekly), serving temperature by style (lager 3–6°C, Belgian strong 10–12°C, Imperial Stout 14–18°C), and glassware (Pilsner flute, tulip for Belgian, shaker pint for American Ale).
7. Build a paired tasting: standard Pilsner Urquell (filtered, pasteurised) alongside a Pilsner Urquell tankové (unfiltered, unpasteurised). The difference demonstrates the impact of filtration and pasteurisation on flavour — relevant to natural vs conventional production discussions in wine and beer.
8. Dry-hopping biotransformation is the science behind NEIPA haze and tropical flavour: during active fermentation, yeast enzymes interact with hop precursors (thiols — sulphur-containing flavour compounds) and convert them into intensely tropical, aromatic compounds (3-mercaptohexanol = passion fruit). This is why NEIPA has its distinctive tropical character even when made with hops that smell primarily of citrus/pine.""",
"trigger_keywords": json.dumps(["beer styles", "brewing", "IPA", "lager", "Trappist", "Lambic", "hefeweizen", "MS exam beer", "Cicerone", "beer knowledge"])
},

{
"name": "MS Theory — Sake Comprehensive",
"slug": "ms-theory-sake-comprehensive",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Sake Service Institute / Sake & Shochu Makers Association of Japan",
"description": """Sake occupies a unique position in the MS examination: it is a separate study domain from wine but shares enough conceptual vocabulary (terroir, vintage, appellation-equivalent) to be approachable through existing wine knowledge. The challenge is that sake has its own technical framework — rice polishing ratios, koji science, yeast association numbers, brewing water chemistry, and a temperature service protocol unique in the beverage world — that requires dedicated study.

At the Master Sommelier level, sake knowledge is not merely identifying junmai from honjozo but understanding why the Yamada Nishiki rice variety produces the finest daiginjo, why miyamizu (the hard mineral water of Nada) produces masculine, structured sake while the soft water of Fushimi produces smooth, light sake, and why the kimoto method produces more complex, high-acid sake than the modern sokujo starter. This is craft knowledge, not just classification knowledge.""",

"key_principles": """RICE VARIETIES (Sakamai — sake rice)
Premium sake rice differs from table rice: larger grain, lower protein and fat content (which would cause off-flavours), distinctive starchy core (shinpaku) that develops the koji fungus. Principal varieties:
  Yamada Nishiki (山田錦): Called the 'Cabernet Sauvignon of sake rice.' Grown primarily in Hyogo Prefecture (Mita, Yoshikawa districts — the Grands Crus of sake rice). Largest, most consistent grain; ideal shinpaku size. Used for the finest daiginjo globally. More expensive than other varieties. Produces: complex, multi-layered, fragrant, elegant sake.
  Gohyakumangoku (五百万石): Niigata's primary variety; slightly smaller grain; clean, light character; perfectly suited to Niigata's tanrei (clean, crisp) style. The rice for producing light, dry ginjo.
  Miyama Nishiki (美山錦): Nagano and northern Tohoku; cold-climate adapted; smaller grain but good shinpaku; produces clean, fruity sake; suited to cold-climate ginjo production.
  Omachi (雄町): Historic variety (oldest cultivated sake rice still in use, from Okayama); irregular grain, difficult to polish and koji; produces earthy, complex, rich, full-bodied sake with distinctive mineral depth; favoured by specialists.
  Dewasansan (出羽燦々): Yamagata; developed from Miyama Nishiki; smooth, elegant, fruity; preferred in Yamagata ginjo production (Juyondai, Yukitsubaki).
  Hattan Nishiki, Kame-no-O, Ipponjime, Senbonishiki: Regional varieties producing distinctive regional styles.

RICE POLISHING (Seimai)
The seimai buai (polishing ratio) indicates what percentage of the grain REMAINS after polishing. Lower number = more polished = more expensive.
  90% remaining (10% polished): Futsushu (table sake); barely polished; more protein and fat remain; heavier, earthier, less aromatic.
  70% remaining (30% polished): Honjozo minimum; standard junmai.
  60% remaining (40% polished): Ginjo minimum. A 60% polish takes 30+ hours for Yamada Nishiki.
  50% remaining (50% polished): Daiginjo minimum. Extraordinary expense — half the grain is discarded.
  35% remaining (65% polished): Dassai 39 (35% was the previous signature expression; now Dassai 23 at 23% remaining). At this level, the grain is nearly spherical; tiny, fragile.
  23% remaining (77% polished): Dassai 23. Currently one of the most polished sake commercially produced. Near the technical limit.

KOJI (麹 — Aspergillus oryzae)
Koji is the mould that converts rice starch into fermentable sugars — the essential biological transformation that defines sake production. Without koji, rice starch cannot be fermented by yeast. This simultaneous saccharification and fermentation ('multiple parallel fermentation') distinguishes sake from beer (which saccharifies first in mashing, then ferments separately) and from wine (which requires no saccharification).
Production: Koji is grown on steamed rice by spraying or spreading A. oryzae spores and incubating at 30–40°C for 40–48 hours. Koji mould sends hyphae into the rice grain, producing amylases (starch → sugar) and proteases (protein → amino acids). The protease activity is critical: excess amino acid production creates a nigami (bitterness) or sharp flavour; precise koji management controls the amino acid level.
Three koji production methods: Hako koji (box method — most common, standard); Futa koji (lid method — slightly more variation); Mori koji (traditional, most labour-intensive — most control, used in premium production).

YEAST STRAINS (Association Yeasts — Kyokai Kobo)
The Japan Brewing Association maintains a library of yeast strains. The most important:
  #7 (Kyokai 7): The most widely used sake yeast; moderate ester production; floral, gentle, reliable; lower ginjo-ka than #9; used in many standard ginjo.
  #9 (Kyokai 9): The classic ginjo yeast; very high isoamyl acetate production (banana/melon aroma); the defining ginjo-ka yeast; widely used in premium ginjo and daiginjo; produces the characteristic fruity-sweet nose of modern premium sake.
  #14 (Kyokai 14): High ethyl caproate (apple, anise aroma); used in Niigata-style clean ginjo; produces a more apple-forward character than #9.
  #18: Very high aromatic; used in premium ginjo to achieve maximum fragrance; not as widely used due to difficulty in management.
  ADD (Association Distilled Drink — Awa yeast): Developed for sparkling sake production; produces CO₂ as a byproduct; used in bottle-fermented sparkling sake.

WATER (Mizu)
Water chemistry is as important in sake as in brewing. Mineral content affects fermentation speed, yeast activity, and final flavour profile.
  Miyamizu (宮水 — 'Shrine Water'): Hard water from Nada, Hyogo; high mineral content (potassium, phosphorus, magnesium); promotes vigorous fermentation; produces bold, structured, 'masculine' sake (referred to in sake as otokozake — 'man's sake'). Nada is the world's largest sake-producing district; producers include Kenbishi, Hakutsuru, Kikumasamune.
  Fushimi water (Kyoto): Extremely soft; gentle fermentation; produces smooth, light, refined sake (referred to as onnazake — 'woman's sake'). Producers: Gekkeikan, Takashimaya.
  Hiroshima water: Soft; was problematic historically (soft water made fermentation control difficult); the toji (head brewer) Senzaburo Miura developed the Hiroshima brewing method (softer koji, cooler temperatures) to compensate. Produces smooth, fruity sake.
  Niigata water: Very soft, pure snowmelt; combined with the cold climate → produces the clean, crisp tanrei style; Kubota, Koshi no Kanbai.

BREWING WATER STARTER METHODS (Shubo / Moto)
The shubo (mother of sake / yeast starter) establishes the yeast culture before the main fermentation. Method determines style:
  Kimoto (生酛): The most traditional method (Edo period, 400+ years old). Requires yamaoroshi — paddle-mixing of the rice, water, and koji in a cold room to create a lactic acid environment naturally (through Lactobacillus development). Takes 30 days vs 10–15 for modern methods. Results: high lactic acidity, complex umami, earthy-savoury character, full body, longer finish. Signature style for producers: Sudo Honke (Tentaka Ku — 'Hawk in the Heavens' — Tokyo's premier kimoto producer), Tamanohikari, Yaegaki Ki-ippon.
  Yamahai (山廃酛): Simplified kimoto — the yamaoroshi paddle-mixing step is omitted (yamahai = 'yamaoroshi haishi' = abandonment of yamaoroshi). Natural lactic acid development still occurs (without mechanical mixing); takes about the same time. Produces: similar to kimoto but often slightly less complex; earthy, wild, acidic, full-bodied. Producers known for yamahai: Kikuhime, Tedorigawa (Ishikawa Prefecture).
  Sokujo (速醸酛): Modern starter method (early 20th century); commercial lactic acid added directly to the must instead of developing naturally; reduces starter development from 30 days to 10–15 days; produces cleaner, lighter, more consistent sake. The dominant production method for most sake (90%+ of production). Not inferior — just different: clean, accessible, less earthy complexity than kimoto/yamahai.

REGIONAL STYLES AND TERROIR
  Niigata (tanrei karakuchi — clean and dry): Cold winters; soft snowmelt water; Gohyakumangoku rice; long, cold fermentation; light, clean, dry sake; low acidity, subtle aroma. Benchmark producers: Hakkaisan, Kubota (Asahi Shuzo), Koshi no Kanbai, Juyondai (Yamagata, adjacent; similar clean style).
  Nada (Hyogo): Miyamizu hard water; bold, structured, 'masculine'; full body, high acidity; table sake traditionally; now also premium. Kenbishi (historic — 500 years), Hakutsuru, Kikumasamune.
  Fushimi (Kyoto): Soft water; smooth, light, elegant, refined. Gekkeikan (the world's largest sake producer), Tamanohikari.
  Hiroshima: Soft water + developed Hiroshima method; fruity, smooth; Saijo (the 'sake capital' of Hiroshima): Kamotsuru, Sempuku, Zohokoku.
  Akita (northeast — Tohoku region): Cold; Miyama Nishiki rice; earthy, full-bodied sake; yamahai production common; Dewatsuru, Kariho.
  Yamagata: Dewasansan rice; clean, fruity, elegant; Juyondai (the most sought-after premium sake in Japan, extremely limited), Yukitsubaki.

MODERN TRENDS AND SPECIALIST CATEGORIES
  Sparkling Sake (Awa Sake): Bottle-fermented (secondary fermentation in bottle, like Champagne) vs tank-carbonated. The Japan Awa Sake Association (founded 2016) certifies bottle-fermented sparkling sake. Requirements: minimum 5g/L CO₂; in-bottle secondary fermentation; minimum 5% ABV.
  Aged Sake (Koshu): Deliberately aged for 3–10+ years; amber colour; Maillard reaction produces caramel, soy, walnut, dried fruit; the umami deepens dramatically with age; a distinct category requiring specific evaluation approach. Producers: Mikotsuru (Tochigi), Jikon-ko Koshu.
  Natural Sake / Kimoto Revival: Growing movement toward traditional production methods; kimoto and yamahai experiencing a premium revival; natural fermentation without added lactic acid; parallels to natural wine movement.
  Single Variety / Terroir Sake: Producers increasingly emphasising specific rice variety, specific rice-growing village, or even specific paddock (tanada) origin — parallel to single-vineyard wine. Aramasa (Akita) is the leader — uses only Akita-grown Omachi rice, kimoto method, wood barrels; completely distinctive style.
  Export and International Market: US, UK, Europe, Australia are the fastest-growing sake export markets. Sake from the US (Sequoia Sake Co., Brooklyn Kura), UK, and Australia is now commercially available.""",

"common_mistakes": """1. Treating polishing ratio as a direct quality indicator — a highly polished sake is not automatically better than a less-polished one; a kimoto junmai (no polishing requirement) from a great producer can be more complex than a mediocre 35% polish daiginjo.
2. Not distinguishing kimoto from yamahai — both produce complex, earthy, high-acid sake through natural lactic acid development; kimoto requires the yamaoroshi paddle-mixing step; yamahai abandons it. They produce similar but distinct styles.
3. Applying sweetness assessments from wine — sake SMV (Sake Meter Value) is a density measurement, not a sweetness scale. A sake with SMV +5 (technically 'dry') can taste sweeter than SMV 0 if amino acid content is high. Taste without preconceptions.
4. Treating nigori as inferior — cloudy sake (nigori) is a stylistic choice involving coarse filtration that retains rice solids; it is not unfinished or poorly made. Premium nigori (Joto Umeshu, some Dassai expressions) is intentional artisanship.
5. Missing that namazake must be kept cold throughout the supply chain — unpasteurised sake (namazake) contains active enzymes that continue to develop if not refrigerated; warm storage causes 'nama deterioration' (namaochi). Its fresh, lively character depends on unbroken cold chain.
6. Not knowing that yeast selection is the primary tool for aromatic profile in sake — the ginjo-ka (fruity, floral aroma) of premium sake comes from yeast ester production (isoamyl acetate for banana/melon, ethyl caproate for apple), not from the rice variety. Yeast #9 vs yeast #14 produce fundamentally different aromas.
7. Confusing the SMV (Sake Meter Value) scale direction — positive SMV = drier; negative SMV = sweeter. Many candidates reverse this. A sake labelled +10 is very dry; -10 is very sweet.
8. Overlooking the service temperature matrix — temperature completely transforms sake. Evaluating a junmai only at refrigerator temperature misses half the wine's character. The professional evaluator must know which style performs best at which temperature and explain why (cold suppresses sweetness and acidity; warm enhances umami and softens acidity).""",

"pro_tips": """1. Develop a 'sake fingerprint' tasting protocol: taste any sake at three temperatures — 8°C (chilled), 20°C (room temperature), 40°C (nurukan warm). The character changes dramatically. Ginjo reveals aromatics best cold; junmai reveals body and umami best at room temperature; honjozo and futsushu often show best warm. This practical understanding separates professional sake service from casual knowledge.
2. The Aramasa brewery (Akita Prefecture) represents the most radical departure in modern sake philosophy — all kimoto production, no added yeast (using naturally occurring ambient yeast from the brewery), Akita-grown Omachi rice only, all ageing in wooden barrels (a revival of pre-modern production). Their sake is almost impossible to source outside Japan. Knowing Aramasa demonstrates depth.
3. For the MS exam: know the three historic brewing districts of Japan: Nada (Hyogo — the largest; Kenbishi, Hakutsuru; hard miyamizu water), Fushimi (Kyoto — soft water, elegant; Gekkeikan), Itami (historically the first major brewing district; now largely commercial). These three are the 'Champagne, Bordeaux, Burgundy' of Japanese sake.
4. The Juyondai sake (Yamagata — Takagi Sake Brewery) demonstrates how scarcity creates prestige in sake: production is intentionally tiny; the sake is almost never available in retail; it is 'found' on specialist sake bar menus in Japan. Knowing Juyondai and its reputation demonstrates deep market knowledge.
5. Study the sake rice polishing cost structure: as polishing ratio decreases from 70% to 35%, cost increases exponentially — the time required, the grain loss (you discard 35–65% of expensive rice), and the equipment requirements all compound. Understanding the economics of premium sake production places it correctly as a prestige product requiring equivalent respect to Grand Cru wine.
6. For food pairing: sake's primary advantage over wine is the absence of tannin and low fruit acidity — this makes it extraordinarily food-versatile. The secondary advantage: umami compounds in sake harmonise with umami in food, creating 'umami synergy.' Fish, shellfish, aged cheese, eggs, and fermented foods all benefit from this harmonisation.
7. The kikichoko (blue and white tasting cup with snake-eye circles) is not merely traditional aesthetic — the concentric blue circles against the white interior allow the evaluator to assess colour and clarity under standardised conditions. Know why it exists and what it measures.
8. Build regional sake vocabulary: tanrei (Niigata — clean, light, crisp, dry); junsui (Hiroshima — pure, smooth, delicate); gojo (Akita — full-bodied, earthy, complex); otokozake / onnazake (masculine/feminine sake — a historical flavour register term, not a gender designation). These terms appear in sake literature and are testable.""",
"trigger_keywords": json.dumps(["sake", "junmai", "daiginjo", "koji", "kimoto", "yamahai", "Yamada Nishiki", "sake regions", "MS exam sake", "sake production"])
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
