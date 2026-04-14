#!/usr/bin/env python3
"""
Canon 4 — Sommelier Training Frameworks, Batch 1 (entries 1–9)
Deductive Frameworks (7) + MS Exam Prep France & Italy (2)
"""
import psycopg2
import json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

ENTRIES = [

# ─── PART 1: DEDUCTIVE TASTING FRAMEWORKS ────────────────────────────────────

{
"name": "CMS Deductive Wine Tasting Grid",
"slug": "cms-deductive-wine-tasting-grid",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers Americas",
"description": """The Court of Master Sommeliers (CMS) Deductive Tasting Grid is the most rigorous blind tasting methodology in professional wine education. It requires the candidate to move systematically from observation through analysis to a specific, defensible conclusion: one grape variety, one country, one region, one quality level, one vintage. At the Master Sommelier level, candidates have approximately 25 minutes to taste six wines and deliver spoken deductions with reasoning at every step.

The method is deductive, not inductive. Every conclusion must be reached by arguing from structural evidence — acid levels, tannin quality, colour depth, aromatic development — not from familiarity or guessing. A candidate who identifies a wine correctly without the correct structural argument scores no points. The discipline of the grid forces intellectual rigour: you must be wrong in specific, defensible ways rather than vaguely right.

The grid has five sections: Appearance, Nose, Palate, Initial Conclusion, and Final Conclusion. Each section narrows the logical field. By the time you reach Final Conclusion, you should have eliminated 90% of possibilities on structural grounds alone. The final answer is not a guess — it is the only surviving hypothesis.""",

"key_principles": """APPEARANCE
Clarity: Brilliant (sparkling, like a diamond) · Star bright (exceptional) · Clear (normal, no haziness) · Hazy (suspect — unfiltered, OR a fault). Haze in a commercial wine is a flaw; haze in an unfiltered natural wine is expected.
Brightness: Bright (lively, primary) · Moderate · Dull (suggesting age, heat damage, or oxidation).
Colour — White wines: Water white (neutral, low phenolics — Pinot Grigio, Muscadet) · Straw (young, unoaked) · Yellow (medium age or oak contact) · Gold (oak, age, late harvest, or botrytis) · Amber/Brown (extended skin contact, oxidative ageing, or fault).
Colour — Red wines: Purple (young, primary — Malbec, young Syrah, Gamay) · Ruby (young to medium, fresh fruit dominant — Sangiovese, young Cab) · Red (medium age) · Garnet (age beginning — the brick is moving in from the rim) · Brick (significant age — the centre is now brick-red) · Brown (advanced age or heat damage).
Colour — Rosé: Pink (fresh, primary, Grenache or Pinot Noir base) · Salmon (Provence style, deliberate pale extraction) · Copper (skin-contact, extended maceration, or oxidative).
Concentration: Pale / Medium / Deep. Critical diagnostic: depth indicates grape variety (Nebbiolo is pale; Syrah is deep), climate (cool = less pigment), and vinification.
Viscosity/Legs: Low (thin, watery, low alcohol or low sugar) · Medium · High (elevated alcohol and/or residual sugar). Legs indicate potential structure; they do NOT indicate quality.
Gas evidence: None · Slight (malolactic gas, some Vinho Verde) · Moderate · Heavy (sparkling).

NOSE
Step 1 — Condition. Is the wine clean? Faults: TCA (musty, wet cardboard — corked wine, 0 or more faults); VA (volatile acidity — vinegar, nail polish remover: ethyl acetate); oxidation (sherry-like, flat, nutty — but at wrong wine type); reduction (struck flint, gunmetal, rotten egg — reductive winemaking, often blows off with air); Brettanomyces (barnyard, leather, Band-Aid, horse — spoilage yeast, acceptable at low levels in Burgundy, disqualifying at high levels).
Step 2 — Intensity: Delicate (low, searching) · Moderate · Powerful (Viognier, New World Chardonnay, Gewurztraminer).
Step 3 — Development: Youthful (primary fruit dominant, no tertiary) · Developing (fruit beginning to evolve, secondary notes present) · Vinous/Developed (tertiary dominant: savoury, earthy, secondary complexity).
Fruit categories:
  White fruit: Citrus (lemon, lime, grapefruit, yuzu) · Tree fruit (apple, pear, peach, apricot) · Tropical (pineapple, mango, passion fruit, lychee) · Melon (honeydew, watermelon, cantaloupe).
  Red fruit: Red berry (strawberry, raspberry, red cherry, cranberry) · Black berry (blackcurrant, blackberry, black cherry, blueberry) · Dried fruit (fig, date, raisin, prune, dried cherry).
Earth: Potting soil, mushroom, forest floor (Burgundy) · Chalk, limestone, slate (mineral — Loire, Chablis) · Volcanic (Etna, Santorini) · Petroleum/kerosene (aged Riesling — TDN compound) · Barnyard (Brett-influenced).
Wood: Vanilla, coconut (new American oak — Rioja, new-world Chardonnay) · Cedar, cigar box (French oak — Bordeaux) · Smoke, toast, char (heavily toasted barrels) · Dill (American oak character, volatile compound).
Other aromatics: Floral (rose = Gewurztraminer, Nebbiolo; violet = Malbec; white flower = Viognier, Grüner Veltliner; chamomile = aged Riesling) · Herbal (pyrazines = green bell pepper, Sauvignon Blanc, cool-climate Cab Franc; eucalyptus = Barossa Shiraz, Napa Cab; herbes de Provence = southern Rhône Grenache) · Spice (black pepper = Syrah/Shiraz, Grüner Veltliner; white pepper = Grüner Veltliner; cinnamon, clove = oak-aged reds) · Oxidative (Sherry-like, nutty — indicates deliberate or incidental oxidation).

PALATE
Sweetness: Bone dry (0 g/L RS — most table wine) · Dry (under 4 g/L) · Off-dry (4–12 g/L — feel it but not obviously sweet) · Sweet (12–45 g/L — German Auslese territory) · Luscious (45+ g/L — Sauternes, TBA).
Acidity: Use the salivation test. Low (flat, no salivation) · Medium-minus · Medium · Medium-plus · High (mouth-watering, persistent salivation). High acidity = youth signal, cool climate, or variety (Riesling, Chenin Blanc, Chablis). Low acidity = warm climate, over-cropping, or malolactic.
Tannin (reds/rosé): Quantity (low–high) AND quality (fine/silky = Pinot Noir, aged wines; grippy/angular = young Nebbiolo, Cab Sauv; chalky/dusty = Malbec, young Merlot; coarse/astringent = underripe grapes, heavy extraction). Tannin quality is the single most reliable variety marker for reds.
Alcohol: Low (under 11%) · Medium-minus (11–12.5%) · Medium (12.5–13.5%) · Medium-plus (13.5–14.5%) · High (14.5%+). Warmth in throat; not just heat but length of warmth.
Body: Correlation of alcohol + glycerol + RS. Light/Medium-minus/Medium/Medium-plus/Full.
Texture: Critical tertiary descriptor. Creamy (malolactic, barrel ferment) · Round (low tannin, elevated glycerol) · Velvety (fine tannin + elevated glycerol — aged Pinot, Barolo riserva) · Chalky (natural chalk, high acid + mineral — Champagne, Chablis) · Grippy (moderate-high tannin, present but not coarse) · Angular/sharp (high acid + lean body — young Grüner, cold-climate Riesling) · Waxy (skin contact, some Viognier, aged Chenin).
Mousse (sparkling only): Delicate (Champagne, fine perlage) · Creamy (traditional method, quality cuvées) · Aggressive (tank method, Prosecco, Asti).
Flavour intensity and characteristics: Mirror nose categories. Confirm or contradict nose findings.
Finish: Short (under 4 seconds) · Medium-minus · Medium (6–9 seconds) · Medium-plus (9–12 seconds) · Long (12+ seconds — Grand Cru Burgundy, Premier Cru Champagne, Sauternes).
Complexity: Low · Moderate · High (multiple layers that evolve over time in the glass and on the palate).

INITIAL CONCLUSION
Synthesise the structural data to narrow down: Old World or New World? Cool, moderate, or warm climate? Age range (under 3 years, 3–7, 7–15, 15+)? Which grape families are consistent with the structure? Name 2–4 possible grape varieties and 3–5 possible countries.

FINAL CONCLUSION
Commit to: Grape variety (one, with reasoning) · Country (one) · Region/appellation (one) · Quality level (AOC, Premier Cru, Grand Cru, etc.) · Vintage (within a 3-year range minimum; exact year if possible). Reason aloud. Every structural element should support your conclusion. If one element contradicts, explain why (unusual vintage, winemaker style).

LEVEL DISTINCTIONS
Certified (passed): Identifies the structural grid correctly; reasonable conclusion. Advanced: Identifies structural markers precisely and narrows to the correct country and variety with high frequency. Master: Identifies the specific appellation, producer style, and vintage range with defensible structural reasoning — and is right more than 75% of the time across 6 wines in 25 minutes.""",

"common_mistakes": """1. Skipping the condition check — failing to note a fault (reduction, VA) that dramatically changes the interpretation.
2. Confusing Pinot Noir with Nebbiolo on nose — both can show red cherry and floral notes; tannin quality (Pinot: silky; Nebbiolo: grippy/chalky) and acidity level distinguish them on palate.
3. Calling New World wines 'Old World' due to restraint — cool-climate New Zealand Pinot Noir, Willamette Pinot, and Central Otago regularly fool candidates. Look for fruit purity and ripeness level.
4. Over-weighting colour — deep colour does not mean Syrah; pale colour does not mean Pinot Noir. Always confirm with tannin quality and aromatic markers.
5. Using hedged language at Master level — 'This might be Burgundy' is a failing answer. Commit: 'This is Pinot Noir from Burgundy, likely Côte de Nuits, 7–12 years old.'
6. Ignoring negative evidence — the absence of green bell pepper rules out Sauvignon Blanc; the absence of petroleum rules out aged Riesling. Use what's NOT there.
7. Confusing Grenache with Pinot Noir — both can be pale, high-acid, red-fruited; Grenache has glycerol richness, lower tannin, and often a spiced/herbal character (garrigue).
8. Mistaking Viognier for Chardonnay — Viognier has an aromatic intensity, peach/apricot character, and lower acidity that should distinguish it clearly from even a rich Chardonnay.""",

"pro_tips": """1. Practise the 25-minute format from day one — most Advanced and Master failures are time-management failures. Use a timer; deliver all 6 wines with reasoning in 25 minutes.
2. The 'lighthouse' approach for identification: identify the single most distinctive structural characteristic of the wine first, then build outward. A wine with high acidity + kerosene on the nose IS Riesling until proven otherwise.
3. For red wines, evaluate tannin quality before tannin quantity — the texture of tannin (silky vs chalky vs grippy) is the most reliable variety differentiator.
4. Build a 'structural fingerprint' for the 12–15 most commonly served varietals: Chardonnay, Sauvignon Blanc, Riesling, Pinot Gris/Grigio, Viognier, Chenin Blanc; Pinot Noir, Syrah/Shiraz, Cabernet Sauvignon, Merlot, Nebbiolo, Grenache, Sangiovese, Malbec, Tempranillo.
5. Vintage matters structurally — great vintages produce wines with better balance and longer finishes; poor vintages produce dilute or over-extracted wines with shorter finishes. Know the great/poor vintages for the major regions.
6. At Master level, the examiner expects you to commit to a specific producer style occasionally — 'This has the precision and clarity of the Côte de Nuits rather than the power of Gevrey — possibly Vosne-Romanée.' This level of specificity distinguishes Master candidates from Advanced.
7. Never contradict yourself between Initial and Final Conclusion. If you said 'cool climate' in Initial, your Final must be a cool-climate region.
8. Practice decanting without contamination — the practical exam at MS level tests service as well as tasting. A candidate who spills, leaves sediment in the wine, or fails to present the bottle correctly loses marks before they open their mouth.""",
"trigger_keywords": json.dumps(["CMS", "Court of Master Sommeliers", "deductive tasting", "blind tasting", "tasting grid", "wine tasting methodology", "appearance nose palate", "sommelier exam", "WSET", "tasting framework"])
},

# ─── ENTRY 2 ─────────────────────────────────────────────────────────────────
{
"name": "WSET Systematic Approach to Tasting (SAT)",
"slug": "wset-systematic-approach-to-tasting-sat",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Wine & Spirit Education Trust",
"description": """The WSET Systematic Approach to Tasting (SAT) is the Wine & Spirit Education Trust's structured methodology for evaluating wine quality, production characteristics, and commercial potential. Where the CMS grid focuses primarily on identification (what is this wine?), the WSET SAT emphasises quality assessment (how good is this wine and why?) and production inference (how was this wine made?). It is the global standard for wine education at Levels 2, 3, and Diploma (Level 4).

At Level 3, the SAT introduces the quality conclusion — a formal assessment of whether a wine is faulty, poor, acceptable, good, very good, or outstanding, with specific structural reasoning for each rating. At Diploma level, the candidate adds production analysis: was the wine fermented in barrel? Did it undergo malolactic? What oak regime was used? What was the approximate age? The Diploma candidate is expected to assess commercial viability and food pairing suitability, not just describe structure.

The SAT shares its sensory categories with the CMS grid but differs fundamentally in purpose, vocabulary, and grading emphasis. Understanding both systems is essential for professionals who may encounter graduates of either programme and who need to communicate across institutional vocabularies.""",

"key_principles": """WSET SAT STRUCTURE
The SAT has four phases: Appearance, Nose, Palate, Conclusions.

APPEARANCE
Clarity: Clear or hazy (hazy = possible fault, unfiltered intention, or secondary fermentation in bottle).
Intensity: Pale, medium, deep.
Colour (white): Lemon-green (young, unoaked, or high acid) · Lemon (young to medium) · Gold (age, oak, botrytis, or skin contact) · Amber/Brown (extended skin contact, or oxidative fault).
Colour (red): Purple (young) · Ruby (primary to medium age) · Garnet (medium to aged) · Tawny (significantly aged or oxidative).
Other observations: Effervescence (if sparkling — bubbles persistent/not).

NOSE
Condition: Clean or faulty. WSET lists: cork taint (TCA), oxidation, reduction (sulfide), volatile acidity, Brettanomyces.
Intensity: Delicate, medium, pronounced.
Aroma characteristics by category:
  Floral: blossom, rose, violet, acacia, elderflower, jasmine.
  Green/Herbal: cut grass, tomato leaf, asparagus, eucalyptus, mint, dried herbs.
  Fruit — citrus: lemon, lime, grapefruit, orange zest.
  Fruit — green/yellow: apple, pear, peach, apricot, melon.
  Fruit — red: strawberry, raspberry, redcurrant, red cherry.
  Fruit — black: blackcurrant, blueberry, blackberry, plum, black cherry.
  Fruit — tropical: pineapple, mango, passion fruit, lychee, banana.
  Fruit — dried: fig, prune, raisin, dried apricot, candied peel.
  Spice: black pepper, white pepper, cinnamon, clove, nutmeg, ginger, anise.
  Savoury: meat, game, leather, tobacco, earth, forest floor, mushroom, truffle.
  Oxidative: almond, marzipan, hazelnut, caramel, toffee, coffee, chocolate.
  Oak-derived: vanilla, coconut, cedar, char, smoke, toast, clove, dill.
Development: Youthful (primary fruit dominant) · Developing (fruit + emerging secondary) · Developed/Mature (secondary and tertiary dominate; primary fruit recedes).

PALATE
Sweetness: Dry (no perceptible sweetness) · Off-dry · Medium-dry · Medium-sweet · Sweet · Luscious.
Acidity: Low / Medium / High. (WSET uses 3-point scale at Level 3; Diploma adds medium-minus/plus.)
Tannin (red wines): Low / Medium / High. WSET Diploma adds tannin nature: soft, rounded, grippy, harsh.
Alcohol: Low (under 11%) · Medium (11–13.9%) · High (14%+). Diploma adds medium-minus/plus.
Body: Light / Medium / Full.
Mousse (sparkling): Delicate / Creamy / Aggressive.
Flavour intensity: Low / Medium / Pronounced.
Flavour characteristics: Same categories as nose — confirm or correct nose findings.
Finish: Short (under 3 sec) · Medium / Long (over 7 sec at Diploma level).
Other observations (Diploma): Texture (creamy, round, angular) · Balance (is acidity/tannin/alcohol/residual sugar in proportion?).

CONCLUSIONS — WSET UNIQUE SECTION
Quality Assessment (the key WSET differentiator):
  Faulty: Flaw that renders the wine unpleasant (TCA, severe VA, severe oxidation).
  Poor: No fault, but lacks balance, complexity, or typicality.
  Acceptable: Technically correct, shows typicality, but limited complexity or finish.
  Good: Clear typicality, good balance, good finish.
  Very Good: Complexity, typicality, good balance, notable finish.
  Outstanding: All elements in exceptional harmony; memorable, complex, long finish.
Quality reasoning must cite specific structural evidence — 'outstanding because of the exceptional length (15+ seconds), multi-layered complexity, and perfect balance between fruit, oak, and acidity.'

Production Inference (Diploma level):
Identify: Was the wine barrel-fermented? (Creamy texture, vanilla, toast, dough) Malolactic? (Lower acidity, creamy/buttery, diacetyl if heavy) What oak regime? (Age of barrel: new = strong oak; old = minimal oak) Ageing on lees? (Biscuity, autolytic, increased texture and weight).

Readiness Assessment (Diploma):
Is the wine ready to drink now, or does it need ageing? Cite structural evidence: tannin still grippy → needs time; primary fruit still dominant → drink within 3–5 years; tertiary development at 40% → peak or near-peak.

LEVEL DIFFERENCES
Level 2: Name the structural components using basic vocabulary. Identify clear faults. No quality conclusion required.
Level 3: Use full SAT vocabulary. Provide a quality conclusion with reasoning. Identify 2–3 aroma characteristics per category.
Diploma: Full production inference. Specific quality conclusion with evidence. Commercial assessment. Vintage and regional identification expected (not blind tasting, but theoretical knowledge application).""",

"common_mistakes": """1. Treating SAT and CMS as interchangeable — the SAT quality conclusion language is specific and must be used precisely at WSET level; 'good' has a technical meaning.
2. Skipping the quality conclusion at Level 3 — the most common reason for failing WSET Unit 3 assessments is describing the wine fully but omitting the quality statement and reasoning.
3. Using CMS vocabulary in a WSET assessment (or vice versa) — 'bone dry' is CMS language; WSET uses 'dry.' 'Pronounced' intensity is WSET; 'powerful' is CMS.
4. Confusing 'medium-dry' with 'off-dry' — WSET uses a 6-point sweetness scale; Level 3 candidates often conflate these. Medium-dry is more perceptibly sweet than off-dry.
5. Failing to provide production inference at Diploma level — stating 'vanilla and toast on nose' without concluding 'fermented and/or aged in new or nearly new oak' fails the production analysis requirement.
6. Assessing wine as 'very good' or 'outstanding' without citing complexity and finish length — quality levels above 'good' require demonstrated complexity (multiple layers, evolving aromatics) and a measurable long finish.
7. Confusing 'balance' with 'completeness' — at Diploma level, a wine can be complete in all components but still unbalanced if one element dominates distractingly.
8. Not calibrating readiness conclusions to structure — saying 'ready to drink' without citing evidence (primary fruit still fresh, tannin integrated, acidity in balance) is an incomplete Diploma answer.""",

"pro_tips": """1. Memorise the WSET quality scale and practise applying it with precise reasoning for every tasting — even casual tastings. The habit of concluding with a quality statement is the most differentiating Diploma skill.
2. The Diploma theory papers test knowledge of production methods extensively — know malolactic fermentation, its triggers, its markers, and its effect on wine structure; it appears in nearly every Diploma unit.
3. For the blind tasting component at Diploma: use the SAT structure even under exam pressure. Markers will not credit a disorganised answer even if the identification is correct.
4. Build vocabulary cards: one card per aroma descriptor, with the grape variety or wine style most commonly associated with it. Review 10 cards per day for 90 days before the exam.
5. Practise the readiness assessment with every tasting: 'drink now, or cellar 3–5 years, or cellar 10+ years?' and give the structural evidence every time.
6. At Level 3, the quality conclusion is worth a significant proportion of marks in assessed tastings. Never omit it, even if you are uncertain. 'Acceptable because it shows regional typicality but lacks complexity and finish length' is a valid, specific Level 3 answer.
7. The WSET Diploma Unit D (wines of the world) and Unit E (tasting) are the highest failure rates. Unit D requires knowing specific production regulations for all major wine regions — treat it as legal study, not wine tasting.
8. Use WSET resources: the WSET study guides are the canonical reference for exam vocabulary. Do not paraphrase — use the precise terms, as markers are trained to the vocabulary.""",
"trigger_keywords": json.dumps(["WSET", "SAT", "systematic approach to tasting", "wine education", "quality assessment", "Diploma", "Level 3", "WSET tasting", "blind assessment", "production inference"])
},

# ─── ENTRY 3 ─────────────────────────────────────────────────────────────────
{
"name": "BAR Spirits Tasting Methodology",
"slug": "bar-spirits-tasting-methodology",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Beverage Alcohol Resource (BAR)",
"description": """The Beverage Alcohol Resource (BAR) programme, co-developed by leaders including Dale DeGroff, Steve Olson, and F. Paul Pacult, established the most rigorous professional framework for evaluating distilled spirits. Where wine tasting grids were designed for a single product category, the BAR methodology must serve fundamentally different spirit families — from the grain-forward complexity of Scotch single malt to the agave terroir of mezcal to the molasses depth of pot-still rum. The framework adapts while maintaining structural consistency.

The BAR spirit evaluation proceeds through four phases: Appearance, Nose, Palate, and Finish. Each phase has category-specific subsets depending on the spirit family being evaluated. The methodology also incorporates production knowledge — a trained evaluator knows that the vanilla and coconut notes in a bourbon come from new American oak, that the smoky phenols in Islay Scotch come from peat kilning, and that the floral tropical notes in rhum agricole come from fresh sugarcane juice fermentation. Knowledge of production is inseparable from sensory evaluation in spirits assessment.""",

"key_principles": """APPEARANCE
Colour range: Crystal/water-white (unaged or filtered — vodka, gin, blanco tequila, white rum) · Pale gold/straw (light ageing — bourbon under 4 years, reposado tequila) · Gold (moderate ageing — bourbon 4–8 years, VS Cognac) · Deep amber/mahogany (extended ageing — 12+ year Scotch, XO Cognac, añejo tequila) · Red-brown (solera-aged rum, PX sherry-finished expressions).
Clarity: Crystal clear (expected for most commercial spirits) · Slightly hazy (chill-filtered vs non-chill-filtered — non-chill-filtered Scotch may haze when cold; this is NOT a fault).
Viscosity legs: More pronounced in higher-ABV and higher-congener spirits. Brandy and aged rum often show prominent legs.

NOSE (allow 30–60 seconds for the spirit to open)
Protocol: Never nose at barrel strength undiluted. Add a few drops of still water to open aromatics. Approach from 6 inches, then closer as the spirit adjusts.

SCOTCH WHISKY — Nose markers by category:
  Speyside: Fruity, malty, sherry (dried fruit, Christmas cake, vanilla, clean grain).
  Islay: Peat smoke (medicinal, TCP, bonfire, ash), brine (seaweed, kelp, oyster shell), maritime.
  Highlands: Heather, honey, light peat, dried fruit, floral.
  Lowlands: Light, grain-forward, floral, grassy, delicate.
  Campbeltown: Briny, earthy, malty, peaty, slightly funky.
  Orkney: Heather, smoke, maritime, honeyed.
Whisky production markers: Peat level (phenol PPM — Caol Ila: 35ppm, Lagavulin: 35ppm, Octomore: 167ppm+); Sherry maturation (dried fruit, spice, chocolate); Bourbon barrel maturation (vanilla, caramel, baking spice); first-fill vs refill (intensity of wood influence).

BOURBON/AMERICAN WHISKEY — Nose markers:
  Mash bill high corn (75%+): Sweet corn, caramel, vanilla, butterscotch.
  Rye-forward mash bill (18%+ rye: Bulleit, Four Roses OBSV): Spice, dill, black pepper, herbs.
  Wheated bourbon (Maker's Mark, Pappy): Soft wheat, baked bread, gentle vanilla.
  Tennessee whiskey (Lincoln County Process — charcoal mellowing): Slightly sweeter, maple, less spice than bourbon.

GIN — Nose markers by style:
  London Dry: Juniper-forward (pine, resinous), citrus peel, coriander seed, angelica root. Clean spirit base.
  Plymouth: Earthy, slightly softer, damp soil, citrus less dominant than juniper.
  Old Tom: Slightly sweet (historically sugar-added), floral, less austere than London Dry.
  New Western/Contemporary: Reduced juniper, elevated floral or citrus botanicals (Hendrick's: cucumber/rose; Monkey 47: complex botanical medley; Roku: sakura, yuzu, sencha).

COGNAC/ARMAGNAC — Nose markers:
  VS/VSOP: Fresh fruit (apple, pear, plum), light floral, minimal wood.
  XO: Dried fruit, spice (cinnamon, nutmeg), tobacco, leather, rancio (the distinctive walnut-like oxidative quality of extended barrel age in French brandy).
  Grande Champagne vs Petite Champagne vs Borderies: Grande = floral, long ageing potential; Borderies = violets, softer faster development; Bons Bois = shorter life, more grain notes.
  Armagnac distinction: Column distilled at lower proof → more congeners → more flavour intensity; Gascony terroir → more rustic than Cognac; Bas-Armagnac (best) = sandy soils, lighter spirit.

TEQUILA/MEZCAL — Nose markers:
  Blanco tequila (high-quality, Highlands): Bright citrus, white pepper, agave sweetness (cooked agave, vegetal, earthy).
  Reposado: Caramel, vanilla beginning, still primary agave character.
  Añejo: Deep vanilla, chocolate, spice from oak; agave becomes background note.
  Mezcal (Oaxacan Espadín): Smoke (roasted agave piña, not peat), tropical fruit, minerality. Intensity of smoke varies by producer technique (earthen pit vs above-ground roasting).
  Tobalá, Tepeztate, other wild agave mezcals: Floral, complex, less smoke-dominant, terroir-expressive.

RUM — Nose markers by type:
  Light column-still (Bacardí, Don Q): Clean, light molasses, vanilla, subtle tropical fruit.
  Spanish-style aged (Diplomatico, Ron Zacapa): Caramel, vanilla, dried tropical fruit, molasses, minimal vegetal note.
  English-style pot-still (Barbados — Mount Gay XO, Doorly's): Heavy body, overripe banana, funk, leather.
  Jamaican high-ester (Appleton Estate, Hampden Estate): Overripe fruit, acetone/nail polish (at high ester levels), banana, tropical funk.
  Rhum Agricole (Martinique, AOC — Rhum J.M., Clément): Fresh sugarcane juice, vegetal, grassy, agricultural character — fundamentally different from molasses-based rum. Cachaça: similar; fermented sugarcane; earthy, grassy, funky.
  Demerara rum (El Dorado — Guyana): Rich, treacly molasses, dark sugar, coffee, chocolate.

PALATE — Structured assessment
Sweetness: Spirit sweetness from RS, glycerol, or caramel addition (caramel added for colour in Scotch up to 2.5%); note if sweetness is structural or additive.
Heat: Alcohol presentation — burn location (tip of tongue = hot; back throat = high ABV; even warmth = integrated). Harsh burn indicates young spirit or poor distillation.
Mouthfeel/Texture: Oily (high congener, pot-still rums, peated Scotch) · Silky (aged, redistilled, good filtration) · Thin/watery (column-still, neutral spirit base).
Flavour depth: Primary, Secondary (barrel-derived), Tertiary (age complexity).
Balance: Alcohol does not dominate; flavour and finish are in proportion to the ABV.

FINISH
Length: Short (under 10 sec) · Medium · Long (30+ sec — indicator of quality in aged spirits).
Character: What lingers? Spice (rye whiskey, Cognac) · Smoke (Islay Scotch) · Oak tannin (over-aged spirits can be drying) · Fruit (pot-still rum, XO brandy) · Mineral (mezcal).
Heat vs warmth: Warmth is positive — lingers pleasantly. Heat is negative — burns without flavour.""",

"common_mistakes": """1. Nosing at full cask strength without water — high ABV spirits (58%+) numb the olfactory receptors. Always add a few drops of still water before nosing.
2. Mistaking peat smoke for 'burnt' or 'faulty' — peat smoke on Islay Scotch is intentional and desirable; evaluators unfamiliar with the style mark it as a fault.
3. Confusing rhum agricole with molasses rum — agricole has a distinctly grassy, vegetal, fresh character; evaluators expecting molasses sweetness will miss the category entirely.
4. Calling all mezcal 'smoky' — only some mezcals are heavily smoked (earthen pit roasting). Wild agave mezcals (Tobalá, Arroqueño) can be floral and smoke-minimal.
5. Overlooking mash bill differences in bourbon — a rye-forward mash bill (Bulleit, Four Roses) and a wheated mash bill (Maker's Mark) produce fundamentally different spirits; treating all bourbon as identical is a novice error.
6. Ignoring finish character — finish length and character are primary quality indicators in spirits; a 10-second spice finish in bourbon vs a 45-second dried fruit and rancio finish in XO Cognac represents a fundamental quality difference.
7. Evaluating vodka for absence of flavour only — quality vodka assessment involves texture (silky vs rough), warmth vs heat, and subtle grain character.
8. Confusing Cognac with Armagnac — Cognac is double-distilled in pot stills (lighter); Armagnac is continuous-distilled in column at lower proof (heavier, more characterful). Cognac is dominated by Ugni Blanc; Armagnac uses multiple varieties including Baco Blanc.""",

"pro_tips": """1. Build separate sensory reference files for each spirit family — the descriptors for Islay Scotch and blanco tequila share almost nothing; treating them with the same vocabulary set is a diagnostic failure.
2. Always assess spirits at a minimum of two ABV presentations: neat, and with 5–10ml still water. Many spirits reveal their character only after dilution; cask strength samples rarely show their best nose undiluted.
3. For the MS practical exam, spirits may be served in the theory component — know the production regulations for all major spirits: age requirements for cognac VS/VSOP/XO, bourbon minimum ageing, Scotch 3-year minimum, tequila appellation and agave requirements.
4. Rancio — the walnut-like, oxidative, waxy quality in aged Cognac and Armagnac — is the most reliable quality indicator for premium brandy. If you cannot identify rancio, you cannot reliably distinguish VS from XO in a blind context.
5. Ester levels in rum (measured in grams per hectolitre of pure alcohol) are the critical technical differentiator: light rum = low ester; Jamaican high-ester rum = 200–1600g/hlpa. The funk and overripe fruit character scale directly with ester levels.
6. Study production alongside sensory — knowing that new American oak barrels contribute vanillin, lactones (coconut/vanilla), and caramel from charring, while used French oak contributes more spice and less primary sweetness, allows you to read a spirit's production from its nose alone.
7. For gin: the dominance of juniper is the legal and stylistic baseline for London Dry. If juniper is not the most prominent botanical, the gin is Contemporary/New Western, not London Dry — this affects service, cocktail pairings, and legal classification.
8. Know the major blending houses and their house styles: Hennessy (full-bodied, robust), Rémy Martin (floral, refined Grande Champagne), Martell (lighter, more delicate Borderies influence). These styles are predictable and testable.""",
"trigger_keywords": json.dumps(["BAR", "spirits tasting", "whisky evaluation", "gin assessment", "rum tasting", "tequila mezcal", "Cognac Armagnac", "distilled spirits", "spirit evaluation", "blind spirits"])
},

# ─── ENTRY 4 ─────────────────────────────────────────────────────────────────
{
"name": "BJCP Beer Evaluation Framework",
"slug": "bjcp-beer-evaluation-framework",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Beer Judge Certification Program",
"description": """The Beer Judge Certification Program (BJCP) provides the most widely used structured beer evaluation framework in the world, deployed at homebrew competitions, professional assessments, and educational programmes including the Cicerone Certification Program. The BJCP scoresheet evaluates beer across five categories: Aroma, Appearance, Flavour, Mouthfeel, and Overall Impression, totalling 50 points. A score of 45–50 indicates an extraordinary beer; 38–44 outstanding; 30–37 very good; 21–29 good; 14–20 fair; 7–13 problematic; under 7 not a beer.

The fundamental principle of BJCP evaluation is style-appropriateness. A beer is not evaluated against an abstract ideal but against the BJCP Style Guidelines — the comprehensive document defining over 100 beer styles with their acceptable ranges for colour (SRM), bitterness (IBU), original gravity (OG), final gravity (FG), and ABV. An evaluator must know the style guidelines before they can evaluate a beer: a hazy New England IPA is correct; the same haziness in a German Pilsner is a flaw. Context is everything.

The Cicerone Certification Program — the beer equivalent of sommelier certification — uses BJCP evaluation principles at its Certified Cicerone and Master Cicerone levels. Candidates must not only identify styles but demonstrate knowledge of draft systems, off-flavour identification, and pairing logic.""",

"key_principles": """BJCP EVALUATION SCORESHEET

AROMA (12 points)
Evaluate malt, hops, fermentation character, and style-specific aromatics. Note intensity and balance.
  Malt aromatics: Grainy, cereal, bready, biscuity (Maillard reactions in kilning) · Caramel, toffee (crystal malts) · Roasted (black malt, chocolate malt, roasted barley) · Dark fruit (Munich malt, dark caramel).
  Hop aromatics: Floral, citrus, tropical, piney, resinous, herbal, earthy, spicy (variety-dependent). Noble hops (Hallertau, Tettnang, Saaz): floral, spicy, herbal, restrained. American hops (Cascade, Centennial, Citra, Mosaic): citrus, tropical, resinous. UK hops (Fuggles, EKG): earthy, herbal.
  Fermentation character: Fruity esters (isoamyl acetate — banana in hefeweizen; ethyl acetate — pear), phenols (4-vinyl guaiacol — clove in hefeweizen; 4-ethyl phenol — Band-Aid/barnyard in Brett), diacetyl (butter/butterscotch — see off-flavours), DMS (cooked corn — see off-flavours), sulfur (reduction).
  Yeast strain marker: English ale yeast = marmalade, stone fruit esters; Belgian ale yeast = phenolic spice, fruity complexity; hefeweizen yeast = banana + clove; lager yeast = clean, neutral.

APPEARANCE (3 points)
Colour (SRM scale — Standard Reference Method):
  2–3 SRM: Pale straw (light lager, Berliner Weisse)
  4–6 SRM: Gold (Pilsner, pale ale, blonde)
  7–14 SRM: Amber to copper (amber ale, Märzen, Vienna lager)
  15–22 SRM: Deep amber to brown (brown ale, bock)
  23–35 SRM: Dark brown to black (porter, stout)
Clarity: Brilliant, clear, slight haze, hazy (unfiltered), opaque. Assess appropriateness to style: German Pilsner should be brilliant; New England IPA is expected hazy; hefeweizen may be hazy.
Head: Colour (white, off-white, tan, brown), retention (persistent, moderate, fleeting), texture (fine bubbles = quality carbonation; large bubbles = over-carbonated or contaminated lines).

FLAVOUR (20 points)
The largest weighted category. Evaluate: malt character, hop character, fermentation character, balance, finish, aftertaste.
  Bitterness (IBU): Pilsner: 25–45 IBU · Pale ale: 30–50 · IPA: 40–70+ · Stout: 25–40 · Hefeweizen: 8–15. Over-bitterness (harsh, astringent) vs appropriate bitterness (clean, balancing).
  Hop flavour: Timing of hop addition determines character. Bittering hops (60+ min): bitterness, minimal aroma. Flavour hops (15–30 min): flavour, some aroma. Aroma/dry-hop additions (0 min, post-fermentation): intense aroma, minimal bitterness.
  Malt-hop balance: English ale = malt-forward balance; American IPA = hop-forward; German lager = balanced with hop bitterness providing crispness; Belgian = complex fermentation character over both.
  Finish: Dry (low FG, highly attenuated — saison, Berliner Weisse) · Sweet (higher FG, less attenuated — milk stout, doppelbock) · Bitter (lingering hop bitterness — West Coast IPA).

MOUTHFEEL (5 points)
Body: Light/Medium/Full — determined by FG and protein content.
Carbonation: Low (cask ale, imperial stout) · Medium · High (hefeweizen, Berliner Weisse, witbier).
Warmth: Appropriate for ABV — imperceptible in session beers; warming (not burning) in Imperial Stout (9–12%).
Creaminess: Oats in oatmeal stout/NEIPA; nitrogen dispense (Guinness widget) creates silky mouthfeel.
Astringency: Tannin extraction from grain husk (mashing at too high temperature), dry-hopping haze-positive yeast interactions. Generally a fault.

OVERALL IMPRESSION (10 points)
Is the beer an outstanding, accurate example of its style? Does it merit the style designation? Would you seek another? Holistic evaluation: all five sensory categories working together.

STYLE-BY-STYLE DIAGNOSTIC MARKERS
IPA (West Coast): Clear, gold to amber; citrus/pine/tropical hop aroma dominant; high bitterness (40–70 IBU); dry finish. New England IPA: Hazy/opaque; intense tropical/citrus aroma from biotransformation; low bitterness perceived (despite moderate IBU) due to softness.
Pilsner (Czech/German): Brilliant pale gold; Saaz hop (spicy/floral); crisp bitterness; clean lager yeast; dry finish; brilliant clarity essential.
Stout (Dry Irish): Black, opaque; roasted barley (coffee, dark chocolate) dominant; minimal residual sweetness; moderate bitterness; low ABV (4–5%).
Imperial Stout: Black; complex (chocolate, coffee, roast, dark fruit, oak if barrel-aged); high ABV (8–14%); full body; warming.
Hefeweizen: Hazy gold/amber; banana (isoamyl acetate) and clove (4VG) in balance; low bitterness; soft mouthfeel; persistent head.
Belgian Tripel: Golden; complex fruity esters (orange, banana) and phenols (pepper, spice); high ABV (8–10%); deceptively dry finish despite strength; effervescent.
Saison: Golden to amber; fruity, spicy, earthy; often with herbal or citrus hop character; high carbonation; dry, refreshing finish.
Lambic/Gueuze: Sour, acidic; funky barnyard (Brett), must, hay; wild fermentation character essential; Gueuze = blend of aged lambics, highly carbonated.

OFF-FLAVOUR IDENTIFICATION (critical for Cicerone level)
Diacetyl: Butter, butterscotch. Cause: incomplete fermentation (yeast flocculation too early), bacterial contamination. Fix: diacetyl rest, warm conditioning.
DMS (Dimethyl Sulfide): Cooked corn, creamed corn. Cause: inadequate boil vigour (SMM not volatilised), contamination. Acceptable at very low levels in some lagers.
Acetaldehyde: Green apple, cut grass, latex. Cause: young beer (yeast has not fully reduced acetaldehyde to ethanol). Fix: additional conditioning time.
Oxidation: Cardboard, wet paper, sherry-like. Cause: oxygen exposure post-fermentation. Irreversible. Draft line contamination or poorly cleaned equipment.
Light-strike (skunking): Mercaptan (skunk). Cause: isohumulones in hops react with UV light. Prevent with brown/opaque glass or light-stable hop extracts. Green or clear glass = high risk.
Chlorophenol (Band-Aid, plastic): Chlorine in water reacting with phenolic compounds. Use carbon filters.
Acetic acid: Vinegar. Cause: Acetobacter contamination (oxygen + alcohol = acetic acid). A fault in most styles; intentional in some sours.""",

"common_mistakes": """1. Evaluating against a personal ideal rather than the BJCP style guidelines — marking down a hefeweizen for haziness, or an IPA for bitterness, when both are style-correct.
2. Failing to identify diacetyl at low concentrations — diacetyl threshold is approximately 0.1 mg/L; trained evaluators must detect it at this level, which requires repeated calibration tasting.
3. Confusing light-strike (skunking) with oxidation — both produce off-putting aromas, but skunking (mercaptan) is distinctly skunk-like, while oxidation is cardboard/wet paper. Treatment differs.
4. Missing fermentation character in Belgian ales — the phenolic and ester complexity of Belgian yeast is often confused with hop character or oxidation by evaluators unfamiliar with the style.
5. Assessing head retention as a quality metric universally — low head retention is a fault in Pilsner; it is acceptable in some high-alcohol imperial stouts. Context matters.
6. Conflating bitterness with astringency — bitterness (IBU, clean) is from iso-alpha acids from hops; astringency (rough, drying, tannin) is from polyphenol extraction from grain husks or excessive dry-hopping. They are different sensory experiences.
7. Scoring too low for style-appropriate characteristics — evaluators sometimes dock points for strong roast in a stout or high carbonation in a Berliner Weisse, both of which are required style elements.
8. Ignoring temperature when evaluating — serving temperature dramatically affects apparent bitterness, carbonation, and aroma intensity. All evaluation should note whether temperature was appropriate for the style.""",

"pro_tips": """1. Study the BJCP Style Guidelines (free PDF) as a primary reference — know the SRM, IBU, OG, FG, and ABV ranges for the 20 most common styles. These are testable at Cicerone Certified level.
2. For Cicerone exam preparation: the off-flavour identification component is the highest failure point. Build a set of calibrated off-flavour solutions (diacetyl, DMS, acetaldehyde, isovaleric, acetic) and taste them weekly until identification is automatic.
3. The BJCP written judging component requires written feedback at an intermediate level — practise writing evaluation notes that are specific (cite exact aroma, flavour, and mouthfeel findings) and constructive (suggest what caused the issue, how to fix it).
4. For MS theory: know the role of water chemistry in beer production — Burton-on-Trent's high sulfate water accentuates hop bitterness (Burton ales); Pilsen's extremely soft water produces the delicate Pilsner character. Brewers 'Burtonise' water (add sulfates) for IPAs.
5. Noble hops (Hallertau Mittelfrüh, Tettnang, Saaz, Spalt) are used in traditional European lagers and produce restrained, spicy, herbal aromatics. American C-hops (Cascade, Centennial, Chinook) produce the citrus/pine/resinous character associated with American IPAs. Know them on the nose.
6. Practise evaluating beers at style-correct temperatures: lager at 4–7°C, session ale at 10°C, Belgian strong at 12–14°C, imperial stout at 14–18°C. The temperature changes every sensory characteristic.
7. For MS-level beer knowledge: understand fermentation temperature's impact on ester and phenol production — higher fermentation temperature increases ester and phenol production in ale yeasts, which is why Belgian abbey ales (fermented warm) are more complex and estery than their American counterparts.
8. The Trappist designation — 'Authentic Trappist Product' (ATP) — is legally protected. Only breweries physically within Trappist monasteries may use it: Westvleteren, Rochefort, Chimay, Westmalle, Orval, Achel (Belgium), La Trappe (Netherlands), Spencer (USA), Engelszell (Austria), Cardeña (Spain), Tre Fontane (Italy), Tynt Meadow (UK), Sept (France). Know all 13.""",
"trigger_keywords": json.dumps(["BJCP", "beer evaluation", "beer judge", "Cicerone", "off-flavour identification", "beer styles", "diacetyl", "DMS", "beer tasting", "beer assessment"])
},

# ─── ENTRY 5 ─────────────────────────────────────────────────────────────────
{
"name": "SCA Coffee Cupping Protocol",
"slug": "sca-coffee-cupping-protocol",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Specialty Coffee Association",
"description": """The Specialty Coffee Association (SCA) cupping protocol is the global standard for evaluating coffee quality, used by green coffee buyers, roasters, Q-graders, and barista competition judges worldwide. It establishes the conditions, methodology, and scoring rubric for coffee assessment in a format that is reproducible, calibrated, and internationally recognised. The SCA cupping form scores 10 attributes on a 6-point scale (each attribute scored 6–10, with 6 being the floor of 'good'), producing a total quality score out of 100 points. Coffees scoring 80+ are classified as specialty grade.

The Q-grader certification — administered by the Coffee Quality Institute (CQI) — is the professional credential for coffee evaluators and requires passing 22 separate exams covering cupping, grading, sensory triangulation, and green coffee assessment. Q-graders must be recertified every three years through calibration cupping. The Q-grader is to coffee what the Master of Wine is to wine: the highest professional evaluation credential.

Cupping is distinct from brewing: the protocol strips away brewing variables (grind consistency, extraction pressure, brew ratio variation) to evaluate the coffee as a commodity. Ground coffee is steeped in hot water in an open bowl; crust is broken at a specific moment; the liquid is tasted with a cupping spoon, slurped loudly to aerate the coffee across all taste receptors simultaneously.""",

"key_principles": """SCA CUPPING PROTOCOL — PROCEDURE
Preparation:
  Grind size: Medium-coarse (similar to drip; not espresso). Grind immediately before cupping (within 15 minutes).
  Water temperature: 93°C ± 1°C (off the boil — boiling water over-extracts and scalds).
  Ratio: 8.25g coffee per 150ml water (approximately 1:18 ratio).
  Cups: Minimum 5 cups per sample (for consistency assessment — uniformity is one of the ten scored attributes).
  Minimum 2 cups at 15 minutes before evaluation begins. Coffees should be evaluated at the same stage of rest post-roast (8–24 hours; avoid evaluating within 8 hours or after 3 weeks from roast).

Evaluation sequence:
  Step 1 — Dry fragrance (3–5 minutes after grinding): Nose the ground coffee dry. This captures the most volatile aromatics.
  Step 2 — Wet aroma (immediately after pouring water): Pour water at 93°C. Do not stir. Nose the wet crust forming on the surface. The crust concentrates aromatics.
  Step 3 — Break (4 minutes after pouring): Break the crust with the cupping spoon, pushing grounds to the back. Deeply inhale the escaping steam. This is the peak aromatic moment.
  Step 4 — Evaluate at multiple temperatures: Begin tasting once the coffee reaches approximately 70°C (warm, not scalding). Re-evaluate at 60°C (mid-temperature reveals different attributes — acidity becomes more apparent). Re-evaluate at room temperature (cool coffee reveals sweetness and balance most accurately). Quality coffees improve or maintain as they cool; poor coffees deteriorate.

SCA CUPPING FORM — 10 SCORED ATTRIBUTES

1. FRAGRANCE/AROMA (6–10 points)
Evaluate dry fragrance and wet aroma together. The SCA Flavour Wheel provides vocabulary:
  Floral: Jasmine, rose, chamomile, elderflower, orange blossom (high-grown Ethiopian, some Panamanian Gesha).
  Fruity: Berry (strawberry, blueberry, raspberry — natural process), stone fruit (peach, apricot — washed Ethiopian), citrus (lemon, lime, grapefruit — high-altitude washed), tropical (mango, passion fruit, pineapple — anaerobic process).
  Nutty/Cocoa: Hazelnut, almond, dark chocolate, milk chocolate (Brazilian naturals, some Colombians).
  Sweet: Caramel, brown sugar, maple, honey, vanilla.
  Vegetal/Herbal: Green tea, herbs, tomato — often indicates under-development or specific processing.
  Spice: Black pepper, cinnamon, cardamom.
  Earthy/Musty: Potato defect, earthy, mushroom — often indicates defect or robusta contamination.

2. FLAVOUR (6–10 points)
What is experienced from first sip through the mid-palate? The interaction of all taste, aroma, and mouthfeel elements. Primary taste dimensions: sweetness, acidity, bitterness. Note complexity, intensity, and desirability of flavour.

3. AFTERTASTE (6–10 points)
Length and quality of flavour after swallowing. Long, positive aftertaste (chocolate, fruit, floral residual) = high score. Short or negative (astringent, bitter, sour) = low score.

4. ACIDITY (6–10 points)
Quality AND intensity. Evaluate desirability: is the acidity bright and pleasant (malic, citric) or unpleasant (acetic, ferment-derived)? Rate both intensity (low/medium/high) and quality. High-altitude washed coffees = bright, clean acidity. Natural process = lower acidity, sweeter. Robusta = flat, harsh.
SCA pH range for specialty: approximately 4.8–5.5.

5. BODY (6–10 points)
Mouthfeel — weight, viscosity, texture. Full body (Indonesia Sumatra Mandheling — heavy, syrupy, low-acid) vs light body (Ethiopian washed — delicate, tea-like). Note: body is independent of strength; it relates to soluble solid content and oil levels.

6. BALANCE (6–10 points)
Do flavour, aftertaste, acidity, and body complement each other, or does one element dominate distractingly? A perfectly balanced specialty coffee shows all elements in harmony with no single dimension overshadowing another.

7. SWEETNESS (6–10 points)
Each of the 5 cups evaluated independently (max 2 points per cup = 10 points across 5 cups). Any cup without sweetness = 0 for that cup. Sweetness is a mark of ripe cherry, proper processing, and correct roast. Underripe or over-roasted coffee lacks sweetness.

8. CLEAN CUP (6–10 points)
Each of 5 cups evaluated independently (max 2 per cup). Any tainting aroma or flavour that is not part of the coffee's intrinsic character = mark down. Ferment, mould, phenol, rubber, or any foreign taste.

9. UNIFORMITY (6–10 points)
Each of 5 cups. Are all cups consistent? Variation between cups indicates inconsistent processing (drying, picking) or grading failure.

10. OVERALL (6–10 points)
Holistic assessment. Does this coffee exceed the sum of its parts? Is it memorable? Would you pay a premium price for this lot?

TOTAL SCORE CALCULATION
Sum all 10 attributes. Subtract defects (Category 1 defects: 2 points each; Category 2: 4 points each).
Scoring scale: 90–100 = outstanding; 85–89.99 = excellent; 80–84.99 = very good (specialty threshold) · Under 80 = not specialty.

DEFECT IDENTIFICATION
Quakers: Unripe, undeveloped beans — pale, chalky, peanut/cereal flavour. Indicate improper picking or sorting.
Past crop: Woody, cardboard, paper bag — stale green coffee (beyond 1 crop year).
Ferment/Sour: Vinegary, yoghurt, onion — over-fermented in processing.
Phenol: Plastic, rubber, medicinal — contamination during processing or transport.
Potato defect (East African): Raw potato aroma — caused by Antestia bug damage, lactic acid bacterial infection of the cherry.

ROAST ASSESSMENT
Roast level (Agtron scale, 0=black to 100=green): Light (70–95): Maximum origin character, high acidity, light body. Medium (55–70): Balance of origin and roast character. Dark (25–45): Roast character dominates; bitter, low acidity, heavy body. The SCA recommends cupping at Medium roast (Agtron 55–65) to evaluate origin character without roast interference.""",

"common_mistakes": """1. Evaluating fragrance immediately after pouring (not allowing the 4-minute crust to form) — the crust concentrates aromatics; breaking it too early misses the peak aromatic moment.
2. Tasting too hot — coffee above 75°C presents primarily bitterness and suppresses sweetness and fruity acidity. Sip at 65–70°C for a balanced initial read; re-evaluate at room temperature.
3. Marking down natural-process coffee for 'ferment' character — ripe, clean, intentional fruit notes from natural processing are not defects; off-putting, vinegary, or yoghurt notes are.
4. Confusing body with strength — strength (TDS, total dissolved solids) is a brew ratio variable; body is a sensory characteristic of the coffee itself. High body can occur at any brew strength.
5. Failing to evaluate uniformity consistently across all 5 cups — evaluators often taste 2–3 cups and assume consistency. Variation in the remaining cups is a real processing flaw.
6. Using the flavour wheel superficially without calibration — 'fruity' is not specific enough for SCA cupping. 'Strawberry, raspberry, fermented stone fruit' requires calibration with reference samples.
7. Evaluating dark-roasted coffee and attributing all flavour to origin — at roast levels above Agtron 45, origin character is largely destroyed by Maillard reaction and caramelisation products. Describe what is there, not what the origin 'should' taste like.
8. Not allowing the recommended post-roast rest (8–24 hours) — coffee roasted within 8 hours degasses CO₂ which disrupts extraction and evaluation accuracy; CO₂ creates a false perception of freshness and can cause inconsistent results.""",

"pro_tips": """1. Build your sensory reference library: taste reference standards for each primary flavour category on the SCA Flavour Wheel. Strawberry jam (red berry natural process), citrus peel (washed Ethiopian), caramel (medium roast Colombian) — taste them before cupping to calibrate your descriptors.
2. Slurp loudly — aeration sprays the coffee across all taste receptors simultaneously and volatilises aromatics retronasally. The loud slurp is not poor manners; it is mandatory technique for accurate evaluation.
3. For Q-grader preparation: the SCA triangle test (identifying the odd sample in a set of three) requires a difference threshold of p<0.05 across 8 sets. Practise sensory discrimination tests weekly.
4. Evaluate coffees at multiple temperatures systematically — build the habit of noting separate scores at warm, mid, and cool. High-quality coffees reveal new positive dimensions as they cool; poor coffees deteriorate.
5. Calibration is everything at the professional level — cup alongside Q-graders and compare scores for the same lot. Disagreements reveal calibration errors. Industry-wide calibration sessions (competitions, trade events) are how professionals maintain accuracy.
6. For MS exam coffee knowledge: know the major growing regions and their characteristic profiles. Ethiopia (washed): floral, citrus, bright acidity. Ethiopia (natural): berry, fruit, heavy body. Kenya (washed): blackcurrant, tomato, bright acid. Colombia: balanced, caramel, fruit. Indonesia (Sumatra): earthy, full body, low acid. Guatemala: dark chocolate, balanced, mild.
7. Understand process impact on flavour: Washed (wet) = clean, bright, terroir-expressive. Natural (dry) = fruity, heavy body, lower acidity. Honey process = between washed and natural; fruit notes with more clarity than natural. Anaerobic = intense, complex, fermented notes.
8. The SCA Flavour Wheel (developed with World Coffee Research) is the standard vocabulary reference — know the three tiers: main categories (fruity, floral, nutty, cocoa, spicy, etc.), subcategories, and specific descriptors. This is the controlled vocabulary for all professional cupping documentation.""",
"trigger_keywords": json.dumps(["SCA", "coffee cupping", "Q-grader", "specialty coffee", "cupping protocol", "fragrance aroma", "coffee evaluation", "coffee tasting", "flavour wheel", "coffee defects"])
},

# ─── ENTRY 6 ─────────────────────────────────────────────────────────────────
{
"name": "SSI/JSA Sake Tasting Framework",
"slug": "ssi-jsa-sake-tasting-framework",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Sake Service Institute / Japan Sake and Shochu Makers Association",
"description": """The Sake Service Institute (SSI) and the Japan Sake and Shochu Makers Association (JSA) provide the two primary structured tasting frameworks for professional sake evaluation. The SSI International certification (Sake Expert Advisor, International Kikisake-shi) and the JSA Sake Sommelier certification are the recognised professional credentials globally. Both frameworks share core structure — appearance, aroma, palate, finish — but differ in vocabulary and emphasis.

Japanese sake tasting employs two distinct aroma evaluation moments, each with specific Japanese terminology: uwadachika (立ち香) refers to the initial nose sensed from outside the glass — the top note, often the most volatile aromatics; fukumika (含み香) refers to the aroma experienced retronasally in the mouth (in-mouth aroma), which may differ significantly from the initial nose. This distinction is fundamental to sake evaluation and has no direct parallel in wine or spirits tasting frameworks.

The SSI classification system ('flavour map') categorises sake into four broad style quadrants based on aroma intensity (aromatic vs subtle) and body (light vs rich), allowing for rapid categorisation useful in food pairing and service temperature decisions: Kunshu (aromatic and light — ginjo styles), Soshu (light and subtle — filtered table sake), Jukushu (rich and aged — aged koshu), Junshu (rich and less aromatic — junmai styles).""",

"key_principles": """SAKE CLASSIFICATION SYSTEM (prerequisite knowledge)

Rice polishing ratio (seimai buai): The percentage of the grain REMAINING after polishing. Lower = more polished = higher quality premium tier.
  Daiginjo: 50% or less remaining (50%+ polished away) — the top category.
  Ginjo: 60% or less remaining.
  Tokubetsu (special): 60% or less (honjozo or junmai with special designation).
  Honjozo: 70% or less remaining; small amount of distilled alcohol added.
  Junmai: No minimum polishing ratio; no added alcohol — pure rice, water, koji, yeast.
  Futsushu (table sake): No polishing requirements; most commercially produced sake.

Junmai prefix: Added when no distilled alcohol is used. Junmai Daiginjo = daiginjo with no added alcohol. Honjozo without the Junmai prefix = small amount of distilled alcohol added to lighten texture and increase aroma.

Production process designations:
  Kimoto: Traditional starter method (yamaoroshi) — lactic acid bacteria develop naturally over weeks. Produces more complex, full-bodied, savoury sake; higher acidity.
  Yamahai: Simplified kimoto without the laborious yamaoroshi (paddle mixing) — still naturally lactic. Similar characteristics to kimoto; rich, complex, high acidity.
  Sokujo: Modern starter method (most sake). Adding lactic acid directly — faster, cleaner, consistent.
  Namazake: Unpasteurised sake — must be kept cold, has a fresh, lively, slightly raw character.
  Muroka: Uncharcoal-filtered — retains more colour and flavour; often slightly golden rather than clear.
  Nigori: Coarsely filtered (cloudy) — rice sediment remains; sweet, creamy, lower ABV typical.
  Sparkling: Either bottle-fermented (awa sake — Dassai Sparkling, Aramasa) or tank-carbonated (Mio by Takara).
  Koshu: Aged sake — rare, amber, oxidative, umami-rich. Unlike most sake which is consumed young.

SSI TASTING FRAMEWORK

APPEARANCE
Colour: Water-white (most filtered ginjo) · Very pale gold · Pale gold (some junmai) · Pale amber/yellow-green (muroka, yamahai) · Amber (aged sake, koshu).
Clarity: Brilliant, clear, slight haze (unfiltered/muroka), cloudy/opaque (nigori).
Viscosity: Note viscosity legs — high-alcohol sake (above 16%) or high-RS nigori shows legs.
Effervescence (sparkling): Fine persistent bubbles (bottle-ferment) vs larger coarser bubbles (tank-carbonation) — the same distinction as Champagne vs Cava.

UWADACHIKA (initial/top nose) — from outside the glass
Evaluate at room temperature; then again at service temperature.
Fruity-aromatic (ginjo-ka): Typical of ginjo/daiginjo fermented with low-temperature fermentation and selected yeast.
  Isoamyl acetate (banana, melon): High in ginjo fermented with Association Yeast #9 (the classic ginjo yeast).
  Ethyl caproate (apple, anise): Typical of Dassai and precision ginjo fermentation.
  Ethyl acetate (at low levels: floral; at high levels: nail polish = fault).
Clean/neutral: Typical of sokujo-method futsushu and some honjozo.
Savoury/earthy: Typical of kimoto, yamahai — lactic, aged rice, mushroom.
Oxidative/aged: Typical of koshu — caramel, dried fruit, soy, walnut.
Rice/cereal: Clean grain, steamed rice character — subtle in well-made sake.

FUKUMIKA (in-mouth aroma, retronasally experienced)
This may confirm, contradict, or add to the uwadachika.
Ginjo styles: In-mouth aroma may be richer and more complex than initial nose — the warmth of the mouth volatilises heavier aromatic compounds.
Kimoto/yamahai: Savoury complexity and lactic notes often emerge more fully in the mouth.
Nigori: The in-mouth aroma is significantly richer — the rice solids deliver sweetness and rice character retronasally.

PALATE
Sweetness: Scale from bone dry (nihonshu-do [Sake Meter Value] +10 or higher) to sweet (-10 or lower). SMV: + = dry, - = sweet, 0 = neutral. Most ginjo: +2 to +5. Nigori: -10 or lower.
Acidity: Sake acidity is measured in grams/litre titratable acidity. Higher acidity (1.8+): junmai, kimoto, yamahai. Lower acidity (1.0–1.4): ginjo, daiginjo, modern sokujo.
Umami: A key dimension that wine tasting frameworks largely ignore. Sake — particularly junmai, kimoto, yamahai — can have significant glutamate-driven umami from rice protein breakdown during fermentation and ageing.
Texture: Clean and crisp (daiginjo, sokujo) · Creamy/rounded (junmai, nigori) · Rich and full (kimoto, yamahai) · Light and delicate (ginjo).
Alcohol: Sake is typically 14–17% ABV. Some genshu (undiluted sake) reaches 18–20%. Some lower ABV styles (Mio, sparkling): 5%.

FINISH
Length: Short (futsushu, tank-carbonated sparkling) · Medium (standard honjozo) · Long (premium daiginjo, kimoto aged expressions).
Character: Clean and fading (ginjo) · Savoury and lingering (kimoto/yamahai) · Sweet and persistent (nigori) · Complex and evolving (koshu).

TEMPERATURE SERVICE CHART (temperature determines flavour profile)
Tobi-kirikan (50°C+): Very hot — rarely used; only low-grade futsushu.
Atsukan (50°C): Hot — traditional bar service; honjozo, futsushu.
Jyoukan (45°C): Warm — earthy, savoury notes amplified.
Nurukan (40°C): Body temperature — mellows acidity; common for junmai.
Hitohadakan (35°C): Skin temperature — softer, rounder.
Jouon (room temp, 20°C): Clean expression; suits junmai and honjozo.
Suzuhie (15°C): Slightly chilled — good for ginjo and junmai ginjo.
Hanatsuka (10°C): Chilled — optimal for ginjo, daiginjo.
Yukihie (5°C): Well chilled — optimal for premium daiginjo; maximises ginjo-ka.""",

"common_mistakes": """1. Evaluating sake only at refrigerator temperature — many junmai and honjozo styles reveal significantly more complexity at room temperature or warm (nurukan); restricting evaluation to cold suppresses their best qualities.
2. Confusing ginjo-ka (fruity aromatic character from ester production) with actual fruit addition — sake contains no fruit; the banana and melon notes are produced by yeast fermentation of polished rice at low temperatures.
3. Applying wine tasting vocabulary uncritically — sake lacks tannin, has a different acidity profile, and its umami dimension is not present in most wine. The evaluator must adapt vocabulary.
4. Ignoring the SMV (Sake Meter Value) for sweetness assessment — a sake marked +5 (dry) can taste sweeter than a sake marked 0 if it has a higher amino acid content (umami/savoury perception); SMV is a guide, not an absolute.
5. Treating nigori as a lower-quality product — cloudy sake is a stylistic choice involving coarse filtration to retain rice solids; it is not an unfinished sake. High-quality nigori (Joto, Dewazakura) commands premium pricing.
6. Failing to assess fukumika separately from uwadachika — the in-mouth aroma can be dramatically different from the initial nose, especially in kimoto sake; treating them as one evaluation misses critical complexity.
7. Ignoring production method as a tasting clue — the difference between sokujo and kimoto/yamahai is reliably detectable on the nose and palate (savoury, lactic, complex vs clean, linear) and should be named in professional evaluation.
8. Over-applying food pairing rules from wine — sake's lower acidity, lack of tannin, and umami content make it more food-friendly than most wine, but some traditional pairing principles (tannic red wine with red meat) do not translate.""",

"pro_tips": """1. Study the nine JSA-designated Association Yeasts — especially Yeast #7 (gentle, floral, low-aromatic), #9 (high isoamyl acetate — banana, the most common ginjo yeast), #14 (apple, more fruity ester profile), and #18 (apple, highly aromatic, used in Niigata ginjo). Yeast strain is often detectable on the nose.
2. The kikisake-shi (sake sommelier) practise tasting uses a standardised blue ceramic cup (kikichoko) with a snake-eye blue circle on the inside — the contrast helps assess clarity and colour more accurately than clear glass. Know why.
3. For MS exam: know the five major rice varieties: Yamada Nishiki (the 'Cabernet Sauvignon of sake rice' — most prestigious, grown in Hyogo); Gohyakumangoku (Niigata's main variety — clean, light, ginjo-suited); Miyama Nishiki (Nagano, northern cold climate); Omachi (historical, complex, earthy, from Okayama); Dewasansan (Yamagata, floral, smooth).
4. Build regional knowledge: Niigata = tanrei (light, dry, clean, no prominent ginjo-ka); Hiroshima = soft water, light, smooth; Nada (Hyogo) = hard water (miyamizu), full-bodied, 'masculine'; Akita (Dewa = earthy, rich, yamahai common).
5. When evaluating sparkling sake: look for fine, persistent bubbles (in-bottle secondary fermentation) vs larger, dissipating bubbles (tank-injected CO₂) — the same quality indicator as Champagne vs industrial sparkling.
6. Koshu (aged sake) is a separate evaluation category — expect Maillard reaction products (caramel, soy, walnut, mushroom), amber colour, and complex savoury-sweet palate. Standard ginjo descriptors do not apply.
7. For food pairing: the universal rule of sake pairing is 'washoku no tomo' — sake does not clash with food the way tannic red wine can. Its lack of tannin and moderate acidity make it extraordinarily food-versatile. The primary pairing principle: match body and intensity (light ginjo with delicate seafood; rich kimoto with aged cheese, cured meat).
8. Temperature service is the most underrated variable in sake evaluation — practise evaluating the same sake (a good junmai) at 5°C, 20°C, 40°C, and 50°C. The transformation in sweetness, acidity, and aromatic character is dramatic and demonstrates why temperature is a pairing and service decision, not merely preference.""",
"trigger_keywords": json.dumps(["sake tasting", "SSI", "JSA", "kikisake-shi", "uwadachika", "fukumika", "ginjo", "daiginjo", "junmai", "sake evaluation", "sake sommelier"])
},

# ─── ENTRY 7 ─────────────────────────────────────────────────────────────────
{
"name": "Non-Alcoholic Tasting Framework",
"slug": "non-alcoholic-tasting-framework",
"category": "Sommelier Training — Deductive Frameworks",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Provenance Beverage Intelligence",
"description": """Non-alcoholic beverage evaluation requires a distinct tasting framework because NA products must be assessed on their own merits, not measured against their alcoholic counterparts. Evaluating Seedlip as 'a poor substitute for gin' is a category error — the same as evaluating a sorbet as 'a bad ice cream.' The professional evaluator's task is to understand what the product is trying to achieve, assess how successfully it does so, and recommend it to appropriate contexts without the loaded vocabulary of deficit.

The NA beverage landscape includes: non-alcoholic spirits (botanical distillates or preparations — Seedlip, Lyre's, Monday Gin, Ritual Zero-Proof), dealcoholised wine (vacuum-distilled or reverse osmosis — Leitz Eins Zwei Zero, Ariel), NA beer (craft and commercial), fermented NA beverages (kombucha, kefir, jun, water kefir/tibicos), shrubs and drinking vinegars, functional beverages (adaptogens, nootropics, CBD-infused, ceremonial cacao), and premium mixers elevated to standalone status (Fever-Tree, Luscombe, Belvoir).

The gold standard for NA programme design at the time of writing is Kann restaurant (Portland, Oregon, Chef Gregory Gourdet) — a James Beard Award-winning restaurant with one of the most sophisticated dedicated NA pairing menus in the world, treating non-alcoholic beverages with the same seriousness, sourcing depth, and technical precision as any wine programme. The Kann model demonstrates that NA is not an afterthought but a primary hospitality programme.""",

"key_principles": """EVALUATION FRAMEWORK FOR NA BEVERAGES

APPEARANCE
Clarity: Crystal clear (most distillates, filtered kombucha) · Slightly hazy (unfiltered kombucha, shrubs) · Cloudy (kefir, some functional drinks) · Note if appropriate to product category.
Colour: Natural (ingredient-derived — turmeric gold, hibiscus crimson, black elderflower) · Enhanced (added colouring — note if present) · The colour should be authentic to the stated botanical or base.
Carbonation (where applicable): Fine persistent (quality kombucha, Champagne-method NA wine) · Moderate (standard sparkling water NA cocktail) · Large and coarse (over-carbonated, dissipating rapidly).

NOSE (or Fragrance)
Condition: Clean (no off-aromas — vinegar spike, TCA-like mustiness, rancid fat) · Note any off-aromas as faults.
Intensity: Delicate (requires close nosing) · Moderate · Pronounced (strong aromatics — Seedlip Spice 94 opening).
Botanical integrity: Does the nose reflect the stated botanicals? Hedgerow botanical drinks (Seedlip Garden 108: peas, hay, mint, spearmint, rosemary, thyme, hops) — can you identify the botanical profile?
Complexity: Single-note (one-dimensional, lacks development) · Moderate (two or three distinct aroma families) · Complex (multiple distinct aromatic layers that evolve with time in the glass or with temperature).
Development: Does the aroma change as the product warms or breathes? High-quality botanical preparations (especially kombucha) often reveal secondary aromas on warming.

PALATE
Sweetness: Assess residual sugar, natural sweetness (fruit-derived), or sugar alcohols. Scale: Bone dry (0 g/L RS, dry kombucha) · Dry · Off-dry · Sweet. Note if sweetness is natural (cane, fruit) or artificial (stevia, sucralose — often has a delayed sweetness and metallic aftertaste).
Acidity: Critical evaluative dimension for kombucha and shrubs. Evaluate both quantity (low/medium/high) and quality (bright/clean malic or citric vs sharp/harsh acetic). Kombucha acidity at premium level: 0.5–0.8% titratable acidity; over 0.8% is often perceived as too sharp.
Bitterness: Evaluate separately from acidity. Hop bitterness (NA beer), tonic quinine, gentian (some botanical spirits), caffeine (coffee-based beverages), cacao (chocolate functional drinks). Bitterness quality: clean and integrated vs harsh and dissonant.
Carbonation mouthfeel: Fine and persistent (quality) vs large and aggressive (over-carbonated). Carbonation should enhance, not dominate. Flat (CO₂ escaped) = fault.
Texture/Body: Weight — thin/light (most NA spirits) vs medium/full (oat-based kefir, thick functional drinks). Silky, round, watery, or mouth-drying.
Flavour integration: Are the components (botanical, acidity, sweetness, carbonation) working together, or does one element feel bolted on? The key quality marker for NA beverages.
Alcohol warmth absence: This is a genuine structural gap in many NA spirits. Quality NA products fill this space with texture (viscosity from glycerol, gum arabic, or inulin), capsaicin (gentle heat), or piperin (pepper). Note whether the mouthfeel feels complete or hollow.

FINISH
Length: Short · Medium · Long. Most NA beverages have shorter finishes than their alcoholic equivalents because alcohol provides weight and persistence that is difficult to replicate.
Character: Botanical (herbal, spice) · Fruity · Bitter · Clean and fading · Sweet residual.
Completeness: Does the finish feel satisfying, or does it feel truncated? The most common NA failure is a finish that disappears in 2–3 seconds without resolution.

CATEGORY-SPECIFIC EVALUATION

Non-Alcoholic Spirits (Seedlip, Lyre's, Monday, Ritual, CleanCo):
Evaluate: Botanical authenticity, textural fullness, finish length. Seedlip (distilled) has genuine botanical complexity; most Lyre's products are flavour constructs with less complexity. The honest evaluation distinguishes between distilled NA spirits (genuine botanical complexity) and flavoured water with thickeners (less sophisticated).

Dealcoholised Wine (Leitz Eins Zwei Zero, Ariel, Torres Natureo):
Evaluate: Varietal character retention, acidity, texture, balance. The vacuum dealcoholisation or reverse osmosis process removes alcohol and often strips texture and finish. High-quality producers compensate with post-dealcoholisation adjustments. Evaluate: does the wine retain varietal character (Riesling should still show petrol notes and high acidity)?

Premium Kombucha (Health-Ade, Wild Tonic, June Shine, Equinox):
Evaluate on: SCOBY (Symbiotic Culture of Bacteria and Yeast) quality, acidity (clean vs vinegary), carbonation, flavour clarity, secondary fermentation consistency.

Shrubs and Drinking Vinegars:
Evaluate: Fruit quality, vinegar type (apple cider vinegar = complex; white distilled = harsh), balance (sweetness must balance acidity), whether designed for dilution or straight service.

SERVICE STANDARD
The professional standard for NA beverages: same glassware as alcoholic equivalents, same provenance conversation, same pairing language, same service temperature attention. A guest who orders an NA drink deserves a sommelier's full engagement — including recommendation of pairings, explanation of production, and a beverage experience of equal seriousness to the wine or cocktail menu.""",

"common_mistakes": """1. Evaluating NA spirits against alcoholic spirits as the baseline — 'this is a poor substitute for gin' is an invalid evaluation. The correct question is 'does this NA spirit succeed on its own terms?'
2. Accepting low finish length in NA beverages as inevitable — the best NA products (high-quality kombucha, some distilled botanical spirits) achieve genuine finish length through complexity, not alcohol. Accepting short finish as inherent to the category misses this distinction.
3. Ignoring the textural gap — many NA spirits feel watery compared to their alcoholic counterparts. A professional evaluator notes this explicitly and assesses whether the producer has compensated (glycerol, inulin, capsaicin).
4. Confusing 'natural' with 'high quality' in functional beverages — the functional beverage category is heavily marketed with 'natural' and 'organic' claims that do not correlate with sensory quality. Evaluate sensorially, not label-first.
5. Dismissing kombucha acidity as a fault — acidity in kombucha (lactic and acetic acid from SCOBY fermentation) is a stylistic marker, not a defect, within appropriate ranges. Over-acidic kombucha (sharply vinegary) IS a fault.
6. Ignoring carbonation quality — for NA beverages, carbonation texture is even more important than in alcoholic drinks because it contributes significantly to mouthfeel and finish. Large, dissipating bubbles reduce quality; fine, persistent carbonation elevates the product.
7. Applying the same service temperature to all NA beverages — kombucha and NA beer are served cold; functional beverages may be served at room temperature or warm (ceremonial cacao, adaptogen tonics); some botanical preparations are best at slightly above refrigerator temperature.
8. Treating the NA programme as secondary to the alcoholic list — in modern fine dining, a dedicated NA pairing menu is a marker of programme sophistication, not an accommodation. Guests who request NA deserve the full sommelier experience.""",

"pro_tips": """1. Visit Kann (Portland, OR) virtually — study the menu online, read the press coverage on Gregory Gourdet's NA programme. This is the benchmark: NA pairings selected with the same rigour as wine pairings, each beverage explained in terms of production, origin, and sensory rationale.
2. Build a NA tasting flight for your restaurant team: one NA spirit (Seedlip Spice 94), one quality kombucha (Health-Ade Ginger Lemon), one dealcoholised wine (Leitz Eins Zwei Zero Riesling), one premium shrub. Evaluate on the same dimensions as alcoholic equivalents. The discipline of using identical evaluation language breaks the 'lesser than' mental model.
3. The financial case for the NA programme: premium NA beverages (a 200ml serve of high-quality kombucha or Seedlip cocktail) can be priced at $8–16 with a similar margin to cocktails, while serving the fastest-growing guest demographic (sober-curious, Dry January, health-conscious, pregnant, designated driver).
4. Glycerol (vegetable glycerin) addition at 0.5–1% is the most common textural enhancer in NA spirits — it is legal, calorie-minor, and significantly improves mouthfeel without flavour impact. Know it exists and be able to evaluate when it is used successfully vs when it makes a product feel artificially thick.
5. For professional NA spirit evaluation: Seedlip's three expressions (Spice 94, Garden 108, Grove 42) are distilled — this is genuine distillation of botanicals, producing complexity that flavour-construction products cannot match. The distinction matters for menu positioning and staff training.
6. The fastest-growing NA category (2026) is the ready-to-drink functional beverage — adaptogens (ashwagandha, lion's mane, reishi), nootropics (L-theanine, GABA), and CBD-infused beverages. Evaluate these as functional food products as well as beverages: does the stated functional ingredient appear in a clinically meaningful dose?
7. For MS exam: the non-alcoholic beverage category is increasingly represented in advanced programme theory. Know the market leaders, their production methods, and how they should be served. NA beer knowledge (craft NA beer, non-alcoholic craft category growth) is testable.
8. Always pair NA beverages with the same intentionality as alcoholic pairings. A dish with high acidity → pair with lower-acidity NA beverage (NA wine, lightly acidic kombucha) rather than a high-acid shrub that will clash. The same pairing logic applies: weight with weight, acidity with acidity, bridge shared flavour compounds.""",
"trigger_keywords": json.dumps(["non-alcoholic", "NA beverage", "Seedlip", "dealcoholised wine", "kombucha tasting", "NA spirits", "zero proof", "NA framework", "Kann restaurant", "Gregory Gourdet"])
},

# ─── PART 2: MS EXAM PREPARATION MODULES ─────────────────────────────────────

{
"name": "MS Theory — Wine Regions of France",
"slug": "ms-theory-wine-regions-france",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Wine Scholar Guild — French Wine Scholar",
"description": """France remains the primary reference point for global wine study. Every Master Sommelier candidate must have encyclopaedic knowledge of French appellations — not just the major regions but the village-level distinctions within Burgundy, the classified estates of Bordeaux, the house styles of Champagne, and the obscure but testable appellations of Jura and Savoie. France established the AOC (Appellation d'Origine Contrôlée) system that became the template for wine regulation globally; understanding it structurally is as important as knowing individual wines.

The MS theory exam tests this knowledge through scenario-based wine list questions, food-pairing questions, and wine identification. The practical tasting exam regularly features French wines: Burgundy Pinot Noir, Chardonnay, Chablis, Northern Rhône Syrah, Southern Rhône Grenache blends, Loire Chenin Blanc, and Champagne. A candidate who cannot distinguish a Côte de Nuits Pinot Noir from a Côte de Beaune Pinot Noir on structural grounds alone is not ready for the Master Sommelier exam.""",

"key_principles": """BORDEAUX
Left Bank (Médoc peninsula, dominated by Cabernet Sauvignon): Médoc AOC (northern, simpler) · Haut-Médoc AOC · Six Communal AOCs: Pauillac (Lafite, Latour, Mouton — power + cassis), St-Estèphe (iron, tannic, least glamorous Left Bank style), St-Julien (most consistent commune — harmony, cedar, elegance), Margaux (the most perfumed, feminine Left Bank — violet, cassis), Listrac-Médoc, Moulis.
1855 Classification: 5 tiers. Premiers Crus: Lafite-Rothschild (Pauillac), Latour (Pauillac), Margaux (Margaux), Haut-Brion (Pessac-Léognan — not Médoc), Mouton-Rothschild (Pauillac, elevated 1973). Only change since 1855.
Right Bank (Merlot-dominant; Saint-Émilion, Pomerol): Pomerol (no classification; Petrus is the benchmark — one hectare, 100% Merlot, Bousscaut clay, 5,000 bottles/year). Saint-Émilion (revised classification 2022 — 4 tiers: Saint-Émilion Grand Cru, Grand Cru Classé, Premier Grand Cru Classé B, Premier Grand Cru Classé A — currently: Angélus, Cheval Blanc, Figeac, Pavie).
Entre-Deux-Mers: Dry whites from Sauvignon Blanc, Sémillon, Muscadelle.
Sauternes/Barsac: Noble rot (Botrytis cinerea) dessert wine. 1855 classification with one Premier Cru Supérieur: Château d'Yquem. Grape varieties: Sémillon (dominant), Sauvignon Blanc, Muscadelle.

BURGUNDY
The principle: terroir (lieu-dit, specific vineyard) is paramount. Same grape varieties across the Côte d'Or — Pinot Noir for reds, Chardonnay for whites — but quality and style vary dramatically by vineyard, not producer.
Classification (top to bottom): Grand Cru AOC (the vineyard name alone: Chambertin, Montrachet, Corton) · Premier Cru AOC (village + vineyard: Gevrey-Chambertin 1er Cru Les Cazetiers) · Village AOC (Gevrey-Chambertin, Meursault) · Regional AOC (Bourgogne Rouge, Bourgogne Blanc).
Côte de Nuits (primarily red Pinot Noir, the world's greatest): Gevrey-Chambertin (9 Grand Crus including Chambertin, Clos de Bèze) · Morey-Saint-Denis · Chambolle-Musigny (Les Amoureuses is a benchmark Premier Cru — silky, ethereal) · Vougeot (Clos de Vougeot Grand Cru — 50 hectares, 80 producers) · Vosne-Romanée (Romanée-Conti, Richebourg, La Tâche — the most expensive red wine land on earth) · Nuits-Saint-Georges (no Grand Crus; noted Premier Crus).
Côte de Beaune (white dominance; some very fine reds): Corton (only red Grand Cru in Côte de Beaune) · Aloxe-Corton · Pernand-Vergelesses · Savigny-lès-Beaune · Beaune · Pommard (robust, tannic, structured Pinot Noir) · Volnay (more elegant, red-fruited Pinot Noir) · Meursault (no Grand Crus; Premier Crus Perrières, Charmes; Burgundy's most famous dry white village) · Puligny-Montrachet (Montrachet Grand Cru, Chevalier-Montrachet, Bâtard-Montrachet) · Chassagne-Montrachet (Bâtard-Montrachet, Criots-Bâtard-Montrachet — also fine Pinot Noir) · Santenay · Maranges.
Chablis: Northernmost Burgundy; Kimmeridgian limestone; Chardonnay. Grand Crus (7): Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Valmur, Vaudésir. Petit Chablis (entry level) · Chablis · Chablis Premier Cru · Chablis Grand Cru.
Mâconnais: Pouilly-Fuissé (elevated in 2020 with Premier Crus), Saint-Véran, Mâcon-Villages — approachable Chardonnay, no oak as default.
Beaujolais: Gamay grape. 10 Crus (most serious): Moulin-à-Vent (most structured, can age), Morgon (second most age-worthy), Fleurie (most elegant), Brouilly, Côte de Brouilly, Régnié, Juliénas, Saint-Amour, Chiroubles, Chénas. Beaujolais Nouveau (third Thursday of November) — not the quality benchmark.

CHAMPAGNE
Three grape varieties: Chardonnay (50% in Blanc de Blancs), Pinot Noir (structure, power, red fruit), Pinot Meunier (fruit, accessibility, rounds blends).
Five sub-regions: Montagne de Reims (Pinot Noir dominant; Grand Crus: Ambonnay, Bouzy, Mailly, Verzenay, Louvois) · Vallée de la Marne (Pinot Meunier dominant) · Côte des Blancs (Chardonnay dominant; Grand Crus: Avize, Cramant, Oger, Mesnil-sur-Oger) · Côte de Sézanne · Aube (Côte des Bar — Pinot Noir, southernmost).
Styles: NV (Non-Vintage — blend of multiple years, house style consistency) · Vintage (single year, only exceptional years) · Blanc de Blancs (100% Chardonnay — precise, linear, ageable) · Blanc de Noirs (100% Pinot Noir and/or Meunier — fuller, richer) · Rosé (saignée or blend method) · Prestige Cuvée (Dom Pérignon, Krug Grande Cuvée, Salon, Cristal, Belle Époque).
Major houses: Moët & Chandon, Veuve Clicquot, Bollinger, Pol Roger, Billecart-Salmon, Gosset, Krug, Taittinger, Louis Roederer, Jacquesson. Grower Champagne movement: Egly-Ouriet, Pierre Péters, Ulysse Collin, Benoit Lahaye.
Disgorgement and dosage: NV typically 2–4 years on lees before disgorgement; Vintage 6–10 years. Dosage levels: Brut Nature (0 g/L RS) · Extra Brut (0–6) · Brut (0–12) · Extra Dry (12–17) · Sec (17–32) · Demi-Sec (32–50) · Doux (50+).

RHÔNE VALLEY
Northern Rhône (Syrah for reds; Marsanne/Roussanne/Viognier for whites):
  Côte-Rôtie: Up to 20% Viognier co-fermented with Syrah (adds floral lift, fixation of colour). Steep granite terraces. Two slopes: Côte Blonde (lighter, floral) and Côte Brune (darker, structured).
  Condrieu: 100% Viognier; the definitive Viognier appellation. Floral, apricot, rich, low acid.
  Château-Grillet: 3.8 hectares, Viognier; single estate monopole, its own AOC within Condrieu.
  Saint-Joseph: Both red (Syrah) and white (Marsanne/Roussanne). Broad appellation.
  Crozes-Hermitage: Largest Northern Rhône appellation; surrounds the Hermitage hill; accessible Syrah and white blends.
  Hermitage: The grand cru of Northern Rhône — concentrated, long-lived Syrah. White Hermitage (Marsanne/Roussanne) is among France's finest white wines and one of the most age-worthy.
  Cornas: 100% Syrah; no blending allowed; powerful, dark, tannic, slow-developing; no white wine.
  Saint-Péray: Still and sparkling wine from Marsanne; lesser known.
Southern Rhône (Grenache-dominant blends):
  Châteauneuf-du-Pape: 13 permitted varieties (Grenache, Mourvèdre, Syrah the trinity; also Cinsault, Clairette, etc.); large rounded galets (pebbles); the classic garrigue-scented, full-bodied Southern Rhône style. Notable: Château Rayas (old-vine Grenache, elegant, cool for the appellation).
  Gigondas, Vacqueyras: More structured, less expensive CDPs. Gigondas is the more serious.
  Ventoux, Luberon: Lighter, approachable regional designations.
  Muscat de Beaumes-de-Venise: Sweet fortified Muscat.

LOIRE VALLEY
Muscadet (Melon de Bourgogne): Westernmost Loire; Atlantic climate; sur lie ageing (lees contact adds texture and bready character); Sèvre-et-Maine is the best sub-appellation; Muscadet Crus (Clisson, Gorges, Le Pallet) established 2011 — age-worthy.
Anjou-Saumur: Chenin Blanc heartland. Savennières (bone dry, mineral, volcanic and schist soils, age 10–20 years). Coteaux du Layon (sweet Chenin: Quarts de Chaume Grand Cru, Bonnezeaux). Saumur-Champigny (Cabernet Franc red).
Touraine: Vouvray (dry through sweetluscious Chenin Blanc; Mousseux sparkling), Montlouis-sur-Loire (opposite bank, similar), Chinon (Cabernet Franc red — iron, pepper, redcurrant), Bourgueil, Saint-Nicolas-de-Bourgueil.
Central Loire: Sancerre and Pouilly-Fumé (Sauvignon Blanc; Kimmeridgian limestone; flint mineral character); Menetou-Salon, Quincy, Reuilly (less expensive alternatives to Sancerre).

ALSACE
Almost exclusively varietal wines (unusual for France). Grand Cru designation: 51 Grand Crus.
Varieties: Riesling (greatest potential; most age-worthy; mineral, high acid), Gewurztraminer (intensely aromatic; rose, lychee, spice; low acid), Pinot Gris (rich, textured, off-dry), Muscat (dry or sweet; aromatic), Pinot Blanc (lighter, everyday), Sylvaner (diminishing), Pinot Noir (only red allowed).
Special classifications: Vendange Tardive (VT — late harvest; concentrated; often off-dry to sweet) · Sélection de Grains Nobles (SGN — botrytis-affected; sweetluscious; highest quality; very rare).
Crémant d'Alsace: Sparkling; Pinot Blanc dominant.

ADDITIONAL REGIONS (testable at MS level)
Languedoc-Roussillon: France's largest wine region; IGP Pays d'Oc (Languedoc) produces excellent varietal wines at competitive prices; Corbières, Faugères, Saint-Chinian, Minervois are notable AOCs; Roussillon: Grenache-dominant, Banyuls (fortified, oxidative) and Maury (Grenache-based VDN).
Provence: Pale rosé (Grenache, Cinsault, Mourvèdre, Rolle); Bandol (serious Mourvèdre reds that age 20+ years — Domaine Tempier); Bellet (near Nice, local varieties).
Jura: Chardonnay and Savagnin (Ouillé = reductive style; Sous Voile = oxidative — vin jaune, the great aged oxidative wine of France, aged minimum 6 years 3 months under flor yeast). Vin de Paille (straw wine, sweet). Poulsard, Trousseau (indigenous reds).
Savoie: Alpine wines; Jacquère (white) and Altesse/Roussette; Mondeuse (red); Seyssel (sparkling). Crisp, mountain character.""",

"common_mistakes": """1. Confusing Left Bank and Right Bank Bordeaux structure — Left Bank = Cabernet Sauvignon dominant, firmer tannin, cassis-driven; Right Bank = Merlot dominant, rounder, plum, chocolate. Tannin quality distinguishes them on palate.
2. Treating all Chablis as interchangeable — Petit Chablis, Chablis, Premier Cru, and Grand Cru represent dramatically different intensity, mineral depth, and ageing potential. On the MS exam, they must be distinguished.
3. Claiming Dom Pérignon is a house — it is a prestige cuvée of Moët & Chandon (LVMH). Know which prestige cuvée belongs to which house.
4. Not knowing the 2022 Saint-Émilion classification changes — Cheval Blanc, Angélus, Figeac, Pavie are the four Premier Grand Cru Classé A. This classification has been legally contested.
5. Overlooking Jura and Savoie — both are testable at MS level; vin jaune from Jura (oxidative, aged under flor, served in the 62cl clavelin bottle) is a reliable MS exam topic.
6. Confusing Condrieu and Château-Grillet — both are Viognier AOCs; Château-Grillet is a monopole within Condrieu's geographical boundary, with its own separate AOC, far smaller production, and higher price.
7. Misidentifying Muscat in Alsace — Alsace Muscat is typically dry (unlike most Muscat-based wines elsewhere); in blind tasting, the intensely grapey aroma with low acidity and dry finish can confuse candidates.
8. Missing the distinction between Pinot Noir from Côte de Nuits vs Côte de Beaune — Côte de Nuits: darker fruit, more tannic, longer-ageing (Gevrey, Vosne); Côte de Beaune: lighter, red-fruited, more accessible earlier (Volnay, Pommard).""",

"pro_tips": """1. Memorise the 1855 Bordeaux Classification by commune: all 5 Premiers Crus and their communes, all Second Growths, at minimum; know that Mouton was elevated in 1973. At MS level, knowing at least through Third Growth is expected.
2. For Burgundy: build a grid — rows are villages (Gevrey, Chambolle, Vosne, Nuits, Pommard, Volnay, Meursault, Puligny, Chassagne), columns are Grand Crus and notable Premier Crus. Fill in. This is the core testable matrix.
3. The Côte de Nuits is structured north-to-south: Marsannay, Fixin, Gevrey-Chambertin, Morey-Saint-Denis, Chambolle-Musigny, Vougeot, Vosne-Romanée, Nuits-Saint-Georges. Know this geographic order.
4. For Champagne: know the difference between Blanc de Blancs (Chardonnay; precise, linear, green apple, chalk) and Blanc de Noirs (Pinot Noir/Meunier; fuller, red fruit, toasty) as a blind tasting tool. Also know: Champagne Grand Cru villages (17 villages rated 100% on the échelle des crus).
5. Northern Rhône structural fingerprints: Côte-Rôtie = Syrah with Viognier coferment (floral lift, bacon fat) · Hermitage = concentrated, iron, liquorice, smoky Syrah · Cornas = most untamed, pure Syrah, dense, structured.
6. For the Loire: Chenin Blanc is the diagnostic variety — in Vouvray it ranges from bone dry to richly sweet within the same appellation depending on vintage; in Savennières it is always dry and mineral. The context changes the wine completely.
7. Alsace Grand Cru study: know Schlossberg (Riesling, granite, Kaysersberg), Rangen de Thann (Riesling and Pinot Gris, volcanic), Hengst (Gewurztraminer, limestone), Brand (Riesling, granite). These are MS-level testable.
8. Provence rosé: pale colour is a deliberate winemaking choice (short cold maceration), not a function of poor extraction. The colour should be the palest pink possible — 'oeil de perdrix' (partridge eye) — in premium expressions. Château Miraval and Whispering Angel set the commercial benchmark.""",
"trigger_keywords": json.dumps(["France wine regions", "Bordeaux", "Burgundy", "Champagne", "Rhône", "Loire", "Alsace", "Master Sommelier", "MS exam", "French appellations"])
},

# ─── ENTRY 9 ─────────────────────────────────────────────────────────────────
{
"name": "MS Theory — Wine Regions of Italy",
"slug": "ms-theory-wine-regions-italy",
"category": "Sommelier Training — MS Exam Preparation",
"tier_level": "master",
"authority_tier": 1,
"source_book": "Court of Master Sommeliers / Vinitaly International Academy",
"description": """Italy presents the most complex wine landscape on earth: over 500 officially recognised grape varieties, 78 DOCG designations, 341 DOC designations, and a geographic range from the alpine north (Valle d'Aosta, Trentino-Alto Adige) to the volcanic south (Etna, Pantelleria). For the Master Sommelier candidate, Italy requires a structured approach — learning by region (north, central, south, islands) rather than by variety, because the same grape (Sangiovese) produces fundamentally different wines in Tuscany, Emilia-Romagna, and Umbria.

The classification system (DOCG → DOC → IGT → Vino) provides a legal framework but is not a reliable quality indicator: some of Italy's most prestigious wines (Sassicaia, until it gained its own DOC; Super Tuscans originally as IGT) began as humble table wine classifications because they didn't meet DOC requirements for permitted grape varieties. Understanding where the classification system fails quality assessment is as important as knowing the classification itself.""",

"key_principles": """ITALIAN CLASSIFICATION SYSTEM
DOCG (Denominazione di Origine Controllata e Garantita): Highest tier; 78 designations; production rules strictly defined. Examples: Barolo, Barbaresco, Brunello di Montalcino, Chianti Classico, Amarone.
DOC (Denominazione di Origine Controllata): 341 designations; the working tier of Italian wine.
IGT (Indicazione Geografica Tipica): Geographic designation without strict production rules — allows innovation. Super Tuscans (Sassicaia, Ornellaia, Masseto) were IGT.
Vino: Basic table wine designation.

NORTHWEST ITALY
Piedmont (the most important region for MS study):
  Barolo (DOCG): 'The King of Italian Wines' — 100% Nebbiolo; minimum 38 months ageing (62 in riserva); MOGA system (Menzioni Geografiche Aggiuntive) — individual vineyard (MGA) designation system established 2010; there are 155+ MGAs.
  Key MGAs: Brunate, Cannubi (Barolo village, the most historic), Serralunga d'Alba (largest, most austere, tannic, powerful — full limestone soil), Castiglione Falletto (intermediate), La Morra (most accessible, floral, earliest maturing), Verduno, Novello.
  Barolo structural profile: High tannin, high acidity, high alcohol; pomegranate, tar, roses, leather, liquorice; pale garnet colour (Nebbiolo is pale — do not confuse with Pinot Noir in blind tasting; key difference: Barolo tannin is significantly more grippy/chalky than Pinot Noir's silky tannin).
  Barbaresco (DOCG): 100% Nebbiolo; minimum 26 months ageing (50 riserva); considered more elegant and earlier-maturing than Barolo; communes: Barbaresco, Treiso, Neive, San Rocco Seno d'Elvio. Key producer: Gaja (Bruno Giacosa, Produttori del Barbaresco).
  Barbera d'Asti / Barbera d'Alba (DOCG/DOC): High acidity, low tannin, dark fruit, plum; everyday and premium ranges.
  Dolcetto: Low acidity, soft, bitter finish, dark fruit; early drinking.
  Moscato d'Asti (DOCG): Lightly sparkling (frizzante), low ABV (5–6%), intensely floral-peachy-honeyed; not dessert wine despite sweetness — serve cold as aperitivo.
  Gavi (DOCG): Cortese grape; Gavi di Gavi (from the town of Gavi); clean, mineral, citrus, light body; the definitive Piedmont white.
  Arneis: White grape; Roero DOC (opposite bank of Tanaro from Barolo); floral, light, pear.

Lombardy:
  Franciacorta (DOCG): Traditional method sparkling; Chardonnay-dominant; 18 months non-vintage, 30 months vintage on lees; Italy's answer to Champagne.
  Valtellina (DOC/DOCG): Nebbiolo (locally called Chiavennasca) on steep alpine terraces; Sforzato di Valtellina (passito method — dried grapes; concentrated, high alcohol).
  Oltrepò Pavese: Pinot Nero (Pinot Noir) — significant but understated.

NORTHEAST ITALY
Veneto:
  Prosecco DOC/DOCG: Glera grape; tank method (Charmat); primary floral, apple, pear aromas; no autolytic complexity. Conegliano Valdobbiadene Prosecco Superiore DOCG; single vineyard Rive; Cartizze (107ha, highest quality cru).
  Amarone della Valpolicella (DOCG): Dried grape (appassimento) wine; Corvina dominant; minimum 2 years ageing; 14–17% ABV; concentrated, raisined fruit, dark chocolate, tar, spice; one of Italy's most prestigious reds.
  Recioto della Valpolicella: Sweet version of Amarone (the wine that 'escaped' full fermentation to become Amarone — legend).
  Soave (DOC/DOCG): Garganega grape; Soave Classico (historic zone); Soave Superiore DOCG; volcanic basalt soil; white peach, almond, floral; can age in premium expressions.
  Bardolino: Light Corvina-based red; Lake Garda.
Trentino-Alto Adige: Alpine character; crisp whites (Pinot Grigio, Gewurztraminer, Riesling), Lagrein (indigenous dark red), Teroldego Rotaliano (powerful, dark, structured).
Friuli-Venezia Giulia: White wine excellence; Friulano (Sauvignonasse — not Sauvignon Blanc), Ribolla Gialla, Malvasia Istriana; Collio DOC and Colli Orientali del Friuli DOC (the top quality zones).

CENTRAL ITALY — TUSCANY (most critical for MS)
Chianti Classico (DOCG): Sangiovese-dominant (minimum 80%); the historic zone between Florence and Siena; Gran Selezione (top tier, single vineyard or best selection, minimum 30 months ageing including 3 months bottle); Riserva (24 months minimum); Annata (standard). Key villages: Gaiole, Radda, Castelnuovo Berardenga, Greve, Panzano, San Casciano.
Brunello di Montalcino (DOCG): 100% Sangiovese Grosso (Brunello clone); minimum 5 years ageing for standard (6 for riserva); the longest-ageing Sangiovese; structured, austere when young, developing profound complexity with 15–30 years. Key producers: Biondi-Santi (created Brunello as we know it), Soldera, Cerbaiona, Poggio di Sotto, Altesino.
Vino Nobile di Montepulciano (DOCG): Prugnolo Gentile (Sangiovese clone); elegant, earthy, red cherry, spice; Montepulciano is the town (not the grape variety Montepulciano d'Abruzzo).
Morellino di Scansano (DOCG): Coastal Maremma; Sangiovese in a warmer climate; richer, riper, approachable.
Bolgheri DOC: The Super Tuscan birthplace. Sassicaia (its own DOC — Bolgheri Sassicaia DOC), Ornellaia, Masseto (Merlot), Guado al Tasso. Cabernet Sauvignon and Merlot dominant; international varieties succeed here because the coastal microclimate suits them. Coastal Maremma soils.
Super Tuscans (historical context): Antinori's Tignanello (1971 — first Sangiovese blended with Cabernet, aged in small barriques, an illegal wine under Chianti rules at the time). Sassicaia (Cabernet-dominated, considered Italy's best Cabernet). These wines broke DOC rules intentionally and created the IGT movement.
Vernaccia di San Gimignano (DOCG): Italy's first DOCG (1993); white wine; Vernaccia grape; nutty, almond, citrus; the wines of the towers.

OTHER CENTRAL ITALY
Umbria: Sagrantino di Montefalco (DOCG) — Sagrantino grape; Italy's highest tannin level; deep colour, dried fig, mulberry, powerful, needs 10+ years. Orvieto (DOC) — Trebbiano and Grechetto white blend.
Marche: Verdicchio dei Castelli di Jesi (DOC) — one of Italy's most underrated whites; citrus, almond, mineral, age-worthy.
Abruzzo: Montepulciano d'Abruzzo (DOC) — the grape Montepulciano (not related to the Tuscany town); dark, robust, black cherry, bitter chocolate; Cerasuolo d'Abruzzo (rosé).

SOUTHERN ITALY AND ISLANDS
Campania: Taurasi (DOCG) — Aglianico grape; the 'Barolo of the South'; high tannin, high acidity, volcanic soil; structured, dark, tar and roses. Greco di Tufo (DOCG) and Fiano di Avellino (DOCG) — two of Italy's finest indigenous whites.
Basilicata: Aglianico del Vulture (DOC/DOCG) — Monte Vulture volcano; Aglianico on volcanic ash; structured, mineral, dark fruit, long ageing.
Puglia: Primitivo (= Zinfandel genetically — confirmed by DNA analysis); Primitivo di Manduria. Negroamaro — dark, tannic, southern depth; Salice Salentino.
Sicily: Nero d'Avola — the flagship variety; dark, concentrated, Mediterranean warmth. Etna DOC — Nerello Mascalese (red, on volcanic basalt, often compared to Burgundy Pinot Noir for elegance and terroir expressiveness); Carricante (white, mineral, high acid); Etna is the most discussed Italian wine appellation of the 21st century for quality and terroir specificity. Marsala (DOC) — fortified wine; Florio, Pellegrino the key producers.
Sardinia: Cannonau (= Grenache genetically — introduced by Aragon); Vermentino di Gallura (DOCG).""",

"common_mistakes": """1. Confusing Vino Nobile di Montepulciano (Sangiovese-based wine from Montepulciano the town) with Montepulciano d'Abruzzo (the Montepulciano grape variety grown in Abruzzo) — these are unrelated beyond the shared name.
2. Treating Prosecco as equivalent to Champagne — fundamentally different production (tank method vs traditional method); fundamentally different aromatics (fresh fruit vs autolytic complexity). Never confuse them in service or theory.
3. Missing that Amarone is NOT a fortified wine — the concentration comes from appassimento (drying the grapes) not from added alcohol. It is a naturally high-ABV wine from concentrated grape sugars.
4. Conflating Barolo communes without understanding their structural differences — La Morra Barolo (sandstone/tufa, more perfumed, earlier-maturing) vs Serralunga d'Alba (limestone, austere, long-lived) is a fundamental distinction.
5. Describing Nebbiolo as similar to Pinot Noir based on colour alone — both can be pale; Nebbiolo's tannin is far more grippy, acidity higher, finish more structured; they should never be confused at MS level.
6. Not knowing the Super Tuscan history and legal context — Tignanello, Sassicaia, and Ornellaia violated DOC rules intentionally and were initially labelled Vino da Tavola. This context is MS exam standard knowledge.
7. Ignoring the south and islands — Campania (Taurasi), Etna (Nerello Mascalese), Aglianico del Vulture — these are tested at MS level and represent some of Italy's most exciting quality development.
8. Treating Franciacorta as Italian Prosecco — Franciacorta is traditional method (méthode champenoise), minimum 18 months on lees, and stylistically much closer to Champagne than to Prosecco.""",

"pro_tips": """1. Italy study requires regional anchoring: Northwest (Barolo, Barbaresco, Gavi, Franciacorta), Northeast (Amarone, Soave, Prosecco, Friuli whites), Central (Chianti Classico, Brunello, Bolgheri, Sagrantino), South and Islands (Taurasi, Etna, Aglianico del Vulture, Primitivo). Build your study map geographically.
2. The three great aged Italian reds — Barolo, Barbaresco, Brunello — all require significant bottle age to show their best. Know their ageing trajectories: Brunello is typically unapproachable for 8–12 years; Barolo Riserva from Serralunga for 10–15 years.
3. For blind tasting Italian reds: Nebbiolo fingerprint: pale garnet/ruby colour, high acid, grippy chalky tannin, pomegranate/dried rose/tar nose. If you see these together, Barolo/Barbaresco is the hypothesis.
4. Etna is the most fashion-forward Italian appellation in 2026 — know the key producers (Cornelissen, Passopisciaro, Terre Nere, Benanti), the geology (basalt volcanic soils, 300–1000m elevation), and the wines (Nerello Mascalese for reds — delicate, pinot-like; Carricante for whites — mineral, saline).
5. Amarone and Valpolicella are the same grapes (Corvina dominant) and same region; Amarone is the passito (dried) version. Ripasso adds the Valpolicella pressing back to basic Valpolicella must — 'little Amarone' technique.
6. For whites: Soave Classico (volcanic basalt, Garganega) is one of Italy's most underrated ageable whites. Fiano di Avellino and Greco di Tufo are the benchmarks for southern Italy indigenous whites. Verdicchio from the Marche is almost unknown internationally but reaches Premier Cru quality.
7. Know that Cannonau (Sardinia) = Grenache (Spain) = Garnacha (Spain) — all the same grape, confirmed by genetic analysis. Similarly, Primitivo (Puglia) = Zinfandel (California) = Crljenak Kaštelanski (Croatia).
8. The VIA (Vinitaly International Academy) Italian Wine Ambassador and Italian Wine Expert certifications are the specialist credentials for Italy — they are comprehensive and testable; their study materials map directly onto MS exam knowledge requirements for Italy.""",
"trigger_keywords": json.dumps(["Italy wine regions", "Barolo", "Barbaresco", "Brunello", "Chianti Classico", "Amarone", "Etna", "Super Tuscan", "Nebbiolo", "Italian wine", "MS exam Italy"])
},

]

SQL = """
INSERT INTO technique_references
  (name, slug, category, tier_level, authority_tier, source_book,
   description, key_principles, common_mistakes, pro_tips, trigger_keywords)
VALUES
  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING id
"""

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
