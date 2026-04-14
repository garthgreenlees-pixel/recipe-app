#!/usr/bin/env python3
"""Add structured recipes to all 40 Provenance 500 Coffee entries."""

import psycopg2

DB_WRITE = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

RECIPES = {
    9466: """RECIPE:
Yield: 1 shot espresso | Glassware: Warmed demitasse cup (70ml) | Equipment: Espresso machine + portafilter
---
18g freshly ground coffee — medium-fine grind (fine as table salt; passes through 200 micron filter)
Target yield: 36g liquid espresso (1:2 ratio)
Water temperature: 93-94°C
Target time: 25-30 seconds extraction
Machine pressure: 9 bar
---
1. Flush the group head with hot water for 3 seconds — purge and temperature-stabilize
2. Grind dose: 18g into a clean, dry portafilter basket
3. Distribute grounds evenly — level with a Stockfleth's move or distribution tool
4. Tamp with 15kg (approximately 30lbs) pressure — perfectly level, single firm press
5. Lock portafilter into the group head and start immediately — do not wait
6. Begin timer; expect a 2-4 second pre-infusion then continuous flow
7. Stop at 36g yield — typically 25-30 seconds. Blond (pale) extraction past this point means over-extraction
8. Serve in the warmed demitasse immediately — espresso begins degrading at 60 seconds
---
Quality indicators: Dark amber crema with reddish-brown tiger striping; no pale blonde patches; no white foam. Aroma: caramel, dark fruit, chocolate depending on origin. Taste: high sweetness balanced with bitterness; no harshness.
Temperature: 88-93°C when extracted; serve immediately
Note: The ratio 1:2 (18g in, 36g out) is the specialty coffee standard. Ristretto (1:1.5) is shorter, more concentrated; lungo (1:3) is longer, more extracted. Every variable affects the cup — grind size is the primary dial.

""",

    9467: """RECIPE:
Yield: 300ml finished coffee | Glassware: Carafe or mug | Equipment: V60, Chemex, or flat-bed dripper + kettle
---
V60 Pour Over (primary method):
20g freshly ground coffee — medium grind (coarse as sea salt; just finer than French press)
300ml water at 93-96°C (3°C off boil; or 30 seconds after full boil)
Target brew time: 3:00-3:30 minutes
Target ratio: 1:15 (1g coffee per 15ml water)
---
V60 technique:
1. Rinse paper filter with hot water, discard rinse water — removes paper taste and preheats vessel
2. Add 20g coffee grounds, place on scale, tare to zero
3. Start timer; pour 40g water in a circular motion over all grounds (the bloom)
4. Wait 30-45 seconds for bloom — CO2 degasses from fresh coffee; this is essential
5. Continue pouring in slow, steady circles: 0:45 pour to 150g total; 1:30 pour to 250g total; 2:00 pour to 300g total
6. Allow to draw down — should finish between 3:00 and 3:30
7. Finished brew should be clear, not murky
---
Chemex variation: Use 30g coffee / 450ml water; pour rate is slower; use dedicated Chemex filters
Quality indicators: Bright, clean cup; flavour clarity (can taste individual notes); no bitterness unless intentional
Temperature: Drink at 85-90°C — too hot masks flavour; below 60°C, acidity blooms
Note: Grind fresh immediately before brewing. Pre-ground coffee from a grocery store produces a flat, cardboard cup. The bloom is non-optional — without it, the pour is uneven.

""",

    9468: """RECIPE:
Yield: Concentrate for 4-6 servings | Glassware: Glass bottle for storage; serve over ice in a rocks glass or tall glass | Equipment: Large jar or dedicated cold brew maker
---
100g coarsely ground coffee — coarser than French press (like bread crumbs)
700ml cold filtered water
Steep time: 12-24 hours at room temperature (or 24-36 hours refrigerated)
Target ratio: 1:7 for concentrate (dilute 1:1 with water or milk for serving)
---
1. Combine coarse coffee grounds with cold water in a large jar, stir to saturate all grounds
2. Cover and steep: 12-16 hours at room temperature produces a bright, acidic concentrate; 20-24 hours in the refrigerator produces a smoother, deeper concentrate
3. Strain through a fine mesh strainer, then again through a coffee filter or cheesecloth — removes all fine particles
4. Store in refrigerator — keeps up to 2 weeks
5. To serve: pour 90ml concentrate over a glass full of ice, add 90ml cold water or milk
---
Concentrate strength: Should be intensely flavoured and slightly thick — this is correct; it is a concentrate
Quality indicators: Dark brown (not black); smooth with minimal bitterness; chocolate, caramel, or fruit notes depending on origin
Temperature: Serve over ice — cold brew is designed to be cold
Note: Cold brew extracts differently than hot brew — fewer acids, more sweetness, more chocolate/caramel notes. Coarse grind is critical; fine grounds produce over-extraction and astringency even in cold water.

""",

    9469: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Traditional jebena pot or ceramic mug | Equipment: Jebena or V60 for home preparation
---
Traditional Ethiopian Coffee Ceremony (Buna):
15g Ethiopian single-origin coffee — Yirgacheffe, Sidama, or Guji preferred
250ml water at 95°C
Brewing vessel: Jebena clay pot (or V60 as substitute)
---
1. If using green beans for ceremony: lightly roast on a pan over open flame, stir constantly until dark brown and aromatic — this is done tableside in ceremony
2. Grind roasted beans coarsely in a mortar or hand grinder
3. Add grounds to jebena, pour in near-boiling water
4. Simmer gently over low heat for 5-7 minutes — do not boil vigorously
5. Pour from height through a strainer (or through the jebena's built-in grass filter) into small handleless cups
6. Traditional service: three cups (abol, tona, baraka) — increasingly diluted, each still served with ceremony

For V60 home preparation:
1. Use 15g Yirgacheffe ground medium-fine
2. Bloom with 30g water 30 seconds, then pour to 250g total over 2:30 minutes
3. The natural fruit notes of Ethiopian coffee (jasmine, bergamot, blueberry) need no sweetener

---
Accompaniment: Incense (frankincense), popcorn or kolo (roasted barley), sometimes fresh grass on the floor
Temperature: Served at room temperature — very hot drinks disrupt the ceremony's pace
Note: The buna ceremony is not about coffee — it is about community and hospitality. Three rounds are served: the first is the full-strength drink; the second is lighter; the third (baraka, meaning blessing) is the lightest. Each has ceremonial significance.

""",

    9470: """RECIPE:
Yield: 1 cup (300ml) | Glassware: Ceramic mug | Equipment: V60 pour over
---
20g Colombian single-origin coffee — Huila, Nariño, or Antioquia; medium roast preferred
300ml water at 93°C
Grind: medium (just finer than sea salt)
Target brew time: 3:00-3:30
---
1. Rinse paper filter with hot water, discard
2. Add 20g fresh-ground Colombian coffee
3. Bloom: pour 40g water at 93°C in a circle, wait 35-40 seconds — Colombian coffee blooms strongly due to high elevation freshness
4. Continue pouring slowly and steadily in three additions: to 150g at 1:00, to 250g at 2:00, to 300g at 2:30
5. Allow complete draw-down — should finish at 3:00-3:30
---
Flavour profile to expect: Caramel sweetness, mild acidity, chocolate, sometimes cherry or citrus (especially Huila and Nariño regions). One of the most balanced cups in the world.
Temperature: Drink at 85-90°C to capture the sweetness
Note: Colombian coffee was the first to achieve international recognition for quality (Juan Valdez campaign, 1958). Supreme Court certification (Denominacion de Origen) protects Huila, Nariño, Cauca, and others. Washed process is standard — expect clarity and brightness.

""",

    9471: """RECIPE:
Yield: 1 cup (300ml) | Glassware: White ceramic for colour appreciation | Equipment: V60 or Aeropress
---
20g Kenyan AA or AB coffee — washed process; light-to-medium roast
300ml water at 94-96°C (higher temperature suits the dense, high-altitude beans)
Grind: medium-fine
Target brew time: 3:00-3:30
---
V60 method:
1. Rinse filter, discard rinse
2. Add grounds, bloom with 40g water for 35 seconds — Kenyan coffee is dense and needs thorough bloom
3. Pour in steady circles, always keeping water level consistent: 150g by 1:00, 250g by 2:00, 300g by 2:30
4. Allow draw-down — should be complete by 3:30 maximum

Aeropress method (for more body):
1. 15g coffee, 200ml at 96°C
2. Inverted method: add water, stir 10 seconds, steep 1:30, flip and press over 30 seconds
3. Dilute with 50ml hot water in the cup

---
Flavour profile: Bright acidity (like biting into a ripe blackcurrant), tomato-like sweetness, complex finish. Kenyan SL-28 and SL-34 varietals are among the most distinct in the world.
Temperature: Tastes best at 80-85°C — the acidity is more complex once slightly cooled
Note: "Double washed" Kenyan processing (through two fermentation and washing phases) creates the signature brightness. SL-28 thrives in low-rainfall highlands; it is one of the few varietals recognizable by taste alone.

""",

    9472: """RECIPE:
Yield: 1 cup | Glassware: White ceramic — to appreciate the colour | Equipment: V60 or Chemex
---
12g Panama Gesha coffee (due to cost — adjust to budget) — light roast, washed process preferred
180ml water at 90-91°C (lower temperature — Gesha is delicate and burns at high heat)
Grind: medium (slightly coarser than standard to avoid over-extraction)
Target brew time: 2:30-3:00
---
1. Rinse paper filter very thoroughly — Gesha is so delicate that paper taste is detectable
2. Add 12g Gesha, bloom with 25g water at 91°C for 45 seconds — extended bloom preserves aromatic compounds
3. Pour slowly and gently in small circles: to 90g at 1:00, to 150g at 1:45, to 180g at 2:15
4. Allow draw-down — should finish at 2:30-3:00
5. Do not stir or agitate — Gesha extracts unevenly if disturbed
---
Flavour profile: Jasmine, bergamot, tropical fruit (mango, papaya), sparkling wine-like acidity. At its best, it is the most complex coffee in the world.
Temperature: Drink at 75-80°C — the aromatics are most vivid slightly cooled
Note: Panama Gesha (or Geisha) originates from Ethiopia but was transformed into a world-famous cultivar by the Peterson family at Hacienda La Esmeralda, Panama. At auction, it has sold for thousands of dollars per pound. A correct brew at 91°C reveals why.

""",

    9473: """RECIPE:
Yield: 1 flat white (150-180ml) | Glassware: Ceramic 5-6oz flat white cup | Equipment: Espresso machine + steam wand
---
Double ristretto (basis):
18g coffee ground fine
27g yield (1:1.5 ratio — shorter than espresso for a more concentrated, sweeter base)
90-92°C water temperature
20-25 second extraction
---
Steamed milk technique:
120-130ml whole milk (cold, from refrigerator — never warm)
Target milk temperature: 60-65°C (not beyond 68°C or it scalds)
Target texture: microfoam — smooth, velvety, like wet paint; not bubbly froth
---
1. Pull double ristretto into the preheated cup — pour it in, do not wait
2. Purge steam wand, submerge just below milk surface at 4 o'clock position
3. Steam: tip 1cm below surface initially; lower as milk expands to keep tip at surface (creates the whirlpool vortex)
4. Stop at 65°C — this is the maximum for flat white sweetness and texture
5. Wipe steam wand immediately, purge again
6. Swirl milk jug to integrate; tap on counter to pop any large bubbles — should look mirror-smooth
7. Pour from low height over the ristretto, using a light wrist movement for a latte art heart or rosetta
---
Garnish: Latte art (heart minimum; rosetta for skill)
Temperature: Serve immediately — flat white is 150-180ml; it cools faster than a latte
Note: The ristretto base is the Australian distinction — it creates sweetness and concentration that a standard espresso does not. The small volume means every element must be correct. Do not use low-fat or plant milk for the traditional version.

""",

    9474: """RECIPE:
Yield: 1 cup Turkish coffee (demitasse 70ml) | Glassware: Small Turkish coffee cup (fincan) | Equipment: Cezve (ibrik) — the copper or brass long-handled pot
---
7g very finely ground coffee — Turkish grind, powdery (finer than espresso; passes through 100 micron filter)
70ml cold water
1-2 tsp sugar (optional — specify unsweet/az/orta/cok seker before brewing — it cannot be added after)
Optional: 1 cardamom pod, lightly crushed
---
1. Combine cold water, ground coffee, and sugar (if using) in the cezve — do not stir yet
2. Place over very low heat
3. Stir gently once to combine, then leave undisturbed
4. Watch for a ring of foam to form around the edges (2-4 minutes) — do not walk away
5. When foam rises and reaches the rim, remove from heat immediately — this is the moment; it is about to boil
6. Spoon some foam into the cup first (this preserves the foam)
7. Return cezve to heat, allow to rise again once more
8. Pour slowly into the cup — the foam should sit on top of the grounds
9. Wait 1 minute for grounds to settle before drinking
---
Accompaniment: Glass of water (to cleanse the palate), Turkish delight or a small sweet
Temperature: Drink when slightly cooled — the grounds remain; stop before reaching them
Note: UNESCO listed Turkish coffee culture on its Intangible Cultural Heritage list in 2013. The foam (kopuk) is considered essential — no foam is considered poor craft. The grounds are not filtered — they settle and are sometimes read for fortune-telling (tasseography).

""",

    9497: """RECIPE:
Yield: 1 cappuccino (150-180ml) | Glassware: Pre-warmed ceramic cappuccino cup (150-180ml) | Equipment: Espresso machine + steam wand
---
Double espresso base:
18g coffee ground fine
36g yield (1:2 ratio, standard)
93°C water temperature
25-28 second extraction
---
Steamed milk:
100-110ml whole milk, cold from refrigerator
Target temperature: 60-65°C
Target texture: dry micro-foam — thicker than flat white; still integrated (not separated froth on top)
Traditional dry foam: 1/3 espresso, 1/3 steamed milk, 1/3 stiff foam
Modern wet cappuccino: 1/3 espresso, 2/3 velvety milk (closer to flat white in texture but smaller volume)
---
1. Pull double espresso into preheated cup
2. Steam milk: start with steam wand tip at the surface, then lower as milk heats to incorporate air
3. For a dry cappuccino (traditional): keep tip at the surface longer — more air = stiffer foam
4. Stop steaming at 65°C
5. Swirl, tap, pour from height to incorporate foam
6. Traditional Italian cappuccino: a dome of white foam sits proud of the cup rim — the foam holds its shape
---
Garnish: Optional light dusting of cocoa (Italy does not do this traditionally — this is Northern European)
Temperature: Serve immediately — cappuccino cools rapidly at this volume
Note: The cappuccino exists to be drunk in the morning. In Italy, ordering a cappuccino after 11am is culturally noted. The 150-180ml volume is the standard — anything larger is a latte by a different name.

""",

    9498: """RECIPE:
Yield: 1 glass (200-250ml) | Glassware: Tall glass | Equipment: Drip filter or Vietnamese phin dripper
---
Vietnamese Ca Phe Sua Da (Iced Coffee with Condensed Milk):
25g Vietnamese robusta-blend coffee — Trung Nguyen G7 or similar dark roast blend
35ml sweetened condensed milk (Longevity Brand or equivalent)
250ml boiling water
Large ice cubes or crushed ice
---
Phin method (traditional):
1. Add condensed milk to the bottom of the glass — this is the base layer
2. Place the phin filter on top of the glass; add ground coffee, tap to level
3. Place the filter press on top of the grounds and press gently
4. Pour 30ml boiling water over the grounds; wait 30 seconds (bloom)
5. Add remaining water to the phin (200ml total) — the drip takes 5-8 minutes
6. When finished dripping, remove the phin
7. Stir coffee and condensed milk together
8. Pour over ice in a separate glass, or add ice directly
---
Ca Phe Trung (Egg Coffee) variation:
Beat 2 egg yolks with 1 tbsp condensed milk until thick; pour over strong black coffee — do not stir

Temperature: Serve over ice immediately — Ca Phe Sua Da is always cold
Note: Vietnamese coffee uses robusta beans (higher caffeine, more bitter, less nuanced than arabica) — this is intentional. The condensed milk balances the bitterness. The phin is a gravity-fed device; it requires patience.

""",

    9499: """RECIPE:
Yield: 1 cup (200-250ml) | Glassware: Ceramic mug | Equipment: AeroPress + kettle + scale
---
Standard AeroPress recipe (James Hoffman's "The Ultimate AeroPress Technique"):
11g freshly ground coffee — medium-fine grind (slightly finer than V60)
200ml water at 100°C (full boil) — unusually, AeroPress benefits from very hot water
---
1. Place filter in the AeroPress cap; wet with hot water; clamp onto the AeroPress body
2. Stand AeroPress on the cup; add 11g grounds; tare scale
3. Start timer; pour 200ml boiling water, fully saturating grounds
4. Stir gently 10 seconds
5. Place plunger on top — but do not press yet; the seal creates a vacuum that prevents dripping
6. Wait until 2:00 on the timer
7. Swirl the AeroPress gently
8. Press slowly and steadily over 30 seconds — should finish at 2:30
9. Stop pressing when you hear the first hiss of air (don't press the "dregs" through)
---
Inverted method (for longer steep):
Flip AeroPress, brew for 1:30-2:00 steep time, then flip and press
---
Quality indicators: A clean, bright cup without grit — the paper filter catches all fines
Temperature: Can use full-boil water without over-extraction due to the short contact time
Note: AeroPress allows more experimentation than any other brewer. World AeroPress Championship recipes vary wildly — from 15-second extractions to 3-minute steeps. The pressure variable is minor; the time and grind variables are major.

""",

    9500: """RECIPE:
Yield: 1-2 cups (approximately 150ml strong espresso-style coffee) | Glassware: Moka pot to mug | Equipment: Stovetop moka pot (Bialetti Moka Express or equivalent)
---
Fine-medium grind coffee (finer than V60 but not as fine as espresso)
Fill the filter basket level with coffee — do not tamp
Fill the bottom chamber to just below the pressure valve with cold filtered water
---
1. Fill the lower chamber with cold water to just below the pressure valve — never exceed
2. Insert the filter basket, fill level with ground coffee — do not press or tamp
3. Screw the top and bottom chambers together — tight but not forced
4. Place on low-medium heat — the moka pot should never boil rapidly
5. Leave the lid open to observe extraction
6. When coffee begins to pour from the spout (golden-brown): watch carefully
7. When the stream turns pale or sputters: immediately remove from heat and run the bottom under cold water (stops extraction)
8. Pour into a small, warm cup

For espresso-style macchiato or small serving: the first pour (30-40ml) is richest — stop there
---
Temperature: Serve immediately
Note: The moka pot does not produce espresso — it produces strong, pressurized brewed coffee (1-3 bar vs espresso's 9 bar). But it produces exceptional coffee for its price point. Running cold water on the base after extraction is the Italian method to stop over-extraction.

""",

    9501: """RECIPE:
This entry covers roasting knowledge — no home brewing recipe applies. Below is a cupping guide to understand roast levels.
---
Cupping protocol (SCAA standard) to understand your roast level:
Equipment: Cupping bowls, cupping spoons, kettle, freshly roasted coffee from each roast level
---
For each roast (light/medium/dark):
8.25g ground coffee coarse per 150ml water
---
1. Grind 8.25g of each roast separately; place in separate cupping bowls
2. Note dry aroma before water — fragrance reveals roast character immediately
3. Pour 150ml water at 93°C over each; start timer
4. At 4:00, break the crust by pushing through the surface with a spoon — note the wet aroma
5. Skim foam and grounds from the surface
6. At 8:00-12:00, begin tasting with a cupping spoon (slurping is correct — it aerates the liquid)
7. Taste again at room temperature — flavour shifts significantly as it cools
---
What you should experience:
Light roast: High acidity, complex fruit/floral notes, lighter body, origin character dominant
Medium roast: Balanced acidity and sweetness, chocolate/caramel, lower fruit
Dark roast: Low acidity, bitterness, smoke/char notes, no origin character (roast dominates)

Temperature: Cup at three temperatures — this reveals the full range of the coffee's character

""",

    9502: """RECIPE:
Yield: 1 cup (300ml) | Equipment: V60 or Chemex
---
20g Guatemalan single-origin coffee — Antigua or Acatenango region; medium roast
300ml water at 93-94°C
Grind: medium
---
1. Rinse filter, discard; add grounds
2. Bloom: 40g water, wait 35 seconds — Guatemalan coffee blooms moderately
3. Pour steadily: 150g at 1:00, 250g at 2:00, 300g by 2:30
4. Draw-down complete by 3:00-3:30
---
Flavour profile: Dark chocolate, brown sugar, light citrus (especially Antigua), sometimes cherry or toffee. Body is medium-full with clean sweetness.
Temperature: Best at 80-85°C — chocolate notes are most pronounced mid-temperature
Note: Guatemalan coffee grows in eight distinct microclimates. Antigua (surrounded by three volcanoes) is the most famous — mineral-rich soil and consistent temperature create a distinctive cup. HB/SHB (Strictly Hard Bean) designation indicates high-altitude cultivation above 1,350m.

""",

    9503: """RECIPE:
Yield: 1 cup (300ml) | Equipment: French press (suits Brazilian coffee's body)
---
20g Brazilian single-origin coffee — Cerrado Mineiro, Sul de Minas, or Matas de Minas region; medium-dark roast
300ml water at 93°C
Grind: coarse (like ground pepper — notably coarser than pour over)
---
French press method:
1. Add grounds to preheated French press
2. Pour 300ml water at 93°C — fully saturate grounds; stir gently once
3. Place lid on (do not press), steep for 4:00 exactly
4. At 4:00, press plunger slowly and steadily over 20-30 seconds
5. Pour immediately after pressing — do not leave on the grounds (continues extracting)
---
Flavour profile: Milk chocolate, nuts (especially hazelnut and almond), low acidity, full body. Brazilian coffee is the world's comfort cup — sweet, non-threatening, deeply satisfying.
Temperature: French press retains heat well — serve at 85°C
Note: Brazil produces one-third of the world's coffee by volume. Most is natural process (dried in the cherry) which adds sweetness and body. Bourbon, Mundo Novo, and Catuai varietals are common. The low acidity makes it the world's most popular blend base.

""",

    9504: """RECIPE:
This is a technique entry — no brewing recipe. Below is a latte art instruction.
---
Latte art — heart (entry level):
Equipment: Steamed milk with microfoam, prepared double espresso in a wide cup
---
1. Pull a double espresso into a pre-warmed wide-mouthed cup
2. Steam 150ml whole milk to 65°C with velvety microfoam (no large bubbles)
3. Swirl the milk jug and tap it on the counter — the surface should be mirror-smooth
4. Hold the cup tilted at 45 degrees from you
5. Position the milk jug spout low (2cm above the surface) directly in the centre
6. Pour steadily at medium speed — watch the white circle of foam appear on the surface
7. When the cup is 80% full, increase pour speed and gently rock the jug back and forth
8. A white oval should form — then draw the jug forward through it in a straight line to create the heart's point
---
Rosetta: same technique but with a side-to-side oscillation as you draw back, finishing with a through-line
Temperature: Must be served immediately — latte art degrades as the foam merges with the espresso
Note: Latte art is not decoration — it is the final proof that the milk was steamed correctly. A perfect rosetta on poorly steamed milk is impossible. The art is the quality indicator.

""",

    9505: """RECIPE:
Yield: 1 cup (200ml) | Glassware: Irish coffee glass (footed heat-proof glass) | Equipment: Kettle + cream pourer
---
40ml Irish whiskey — Jameson, Redbreast 12, or Teeling Single Malt
180ml strong hot coffee — French press or drip (not espresso — too concentrated; the drink needs black coffee volume)
1-2 tsp brown sugar or demerara sugar
45ml freshly whipped heavy cream — barely whipped to a pourable but slightly thickened state (not stiff peaks)
---
1. Heat the glass by filling with boiling water; wait 30 seconds; discard the water
2. Add brown sugar to the warm glass
3. Pour hot coffee over the sugar, stir to dissolve completely
4. Add Irish whiskey
5. Pour cream over the back of a warm bar spoon, held just above the surface — the cream should float, not sink
6. Do not stir after the cream is on — it is meant to be drunk through the cream
---
The cream float: partially whipped cream (not double cream at stiff peaks, not liquid cream) sits on the surface. The correct texture is loose, pourable, barely thickened.
Temperature: Serve immediately — Irish Coffee should be piping hot beneath and cold-cream-on-top
Note: Created by Joe Sheridan at Foynes airport, Ireland, 1943, for passengers on a delayed transatlantic flight. Lightly whipped cream is essential — stiff cream sinks if poured incorrectly, and liquid cream sinks regardless.

""",

    9506: """RECIPE:
This entry covers sensory evaluation — below is a cupping protocol for home use.
---
Home cupping protocol (simplified SCAA standard):
Equipment: 2-3 cupping bowls or wide mugs, cupping or soup spoons, scale, kettle, timer
---
For each coffee (test 2-3 side by side):
8g ground coffee (coarse grind) per 120ml water
---
1. Grind 8g of each coffee coarsely; place in separate cupping bowls
2. Smell the dry grounds — record fragrance notes (floral, nutty, chocolatey, earthy)
3. Pour 120ml water at 93°C simultaneously over each bowl — start timer
4. At 4:00: "break the crust" by pushing through the foam with a spoon; smell as you break — the wet aroma is richest at this moment
5. Skim remaining foam and grounds from the surface with two spoons
6. At 8:00-10:00: begin tasting with a cupping spoon. Slurp loudly — aerates the coffee across the palate
7. Evaluate: acidity (brightness), sweetness, body (weight), aftertaste (length and quality)
8. Re-taste at room temperature — 20-25°C reveals different aspects
---
Scoring: SCAA scores on 100-point scale. 80+ is "specialty grade." 90+ is exceptional. Most commercial coffee scores 60-70.
Note: Cupping removes all brewing variables — it is the purest way to compare coffees. Slurping is the technique because the spray across the palate covers all taste zones simultaneously.

""",

    9553: """RECIPE:
Yield: 2-4 cups (400-800ml) | Glassware: Mugs | Equipment: French press (cafetiere)
---
Standard ratio: 1g coffee per 15ml water — for 400ml: 27g coffee
Water temperature: 93-94°C (just off full boil — 30 seconds rest)
Grind: coarse — noticeably chunky, like cracked pepper or coarse bread crumbs
Steep time: 4:00 exactly
---
1. Preheat French press with hot water; discard
2. Add grounds to the French press
3. Pour all 93°C water over the grounds, ensuring all grounds are saturated — stir gently once
4. Place the lid on (plunger up) but do not press — the goal is to trap heat
5. Steep exactly 4:00 minutes — set a timer
6. At 4:00: do NOT press down yet. First, skim the bloom from the top and discard it (this removes bitterness)
7. Press the plunger slowly and evenly over 20-30 seconds
8. Pour immediately into cups or a decanter — leaving coffee on the grounds continues extraction and creates bitterness
---
Troubleshooting: If plunger is hard to press — grind is too fine. If coffee tastes thin — grind finer or steep longer.
Temperature: Best enjoyed at 85-90°C — wait 1 minute after pouring before drinking
Note: The French press (cafetiere) is the world's most forgiving brewer. The coarse grind is essential — fine grounds pass through the mesh and create a gritty, over-extracted cup. The 4-minute steep is the standard; beyond 5 minutes, bitterness dominates.

""",

    9554: """RECIPE:
Yield: 1 cortado (90-120ml total) | Glassware: Small Gibraltar glass or cortado glass (90-120ml) | Equipment: Espresso machine + steam wand
---
Double espresso (the base):
18g coffee ground fine
36g yield (1:2 ratio)
93°C, 25-28 seconds
---
Equal-volume steamed milk:
36-45ml whole milk
Target temperature: 60-65°C
Target texture: silky microfoam, not stiff foam — the milk should be creamy, not foamy
---
1. Pull double espresso into the cortado glass directly
2. Steam 36-45ml milk to 65°C with minimal aeration — the cortado has very little foam
3. Pour milk gently and low over the espresso — no latte art required; just integration
4. The finished drink: equal parts coffee to milk; dark espresso visible through the glass; minimal surface foam
---
Garnish: None
Temperature: Serve immediately — at this volume, it cools in under 2 minutes
Note: "Cortado" means "cut" in Spanish — the milk cuts the acidity and strength of the espresso. The 1:1 espresso-to-milk ratio is the defining characteristic. Do not add sugar — if the espresso requires sweetening, the shot quality needs addressing.

""",

    9555: """RECIPE:
Yield: 1 dessert portion | Glassware: Deep ceramic cup, dessert bowl, or heat-proof glass | Equipment: Espresso machine
---
1 double shot espresso — pulled to order (30ml, or 36g yield from 18g dose)
1 scoop quality vanilla gelato — Fior di Latte or vanilla bean (not ice cream, not soft serve — proper gelato)
---
1. Pull the double espresso — it must be pulled to order; a saved shot becomes acidic and loses crema
2. Place the scoop of gelato in the cup
3. Pour the hot espresso directly over the gelato immediately
4. Serve within 30 seconds — the contrast between hot coffee and cold gelato is the point
5. Optional: a small biscotti or cantuccini on the side
---
The eating/drinking method: spoon gelato with espresso; drink the espresso-gelato liquid from the cup as it forms; eat remaining gelato alternating with the intensifying liquid at the bottom.
Temperature: Hot espresso over cold gelato — the temperature contrast is the experience, not an accident
Note: Affogato means "drowned" in Italian — the gelato is drowned in espresso. This is a dessert and an after-dinner digestif simultaneously. Italian law of simplicity applies: quality gelato + quality espresso = everything needed.

""",

    9556: """RECIPE:
Yield: 1 cup (150-200ml) slow-drip cold brew | Glassware: Crystal or glass cup | Equipment: Kyoto-style slow drip tower, or simulate with an inverted bottle
---
Kyoto-style cold drip (tower method):
12g coffee ground medium (between filter and French press)
200ml ice-cold water (2°C — use ice water or near-frozen water)
Drip rate: 1 drop per second — total brew time: 3-4 hours
---
Simulated home method:
1. Punch a small hole in the base of a large plastic bottle
2. Fill with ice and cold water above coarse-ground coffee in an Aeropress or French press below
3. Allow to drip through at approximately 1 drop per second
4. This creates a concentrate similar to tower-brewed coffee
---
Tower method:
1. Fill top chamber with ice and cold water
2. Set drip rate to 1 drop per second using the valve
3. Coffee sits in the middle chamber; water drips through slowly
4. Collect in the bottom carafe — 3-4 hours for 200ml
5. Serve immediately over a single ice cube, or refrigerate up to 24 hours
---
Flavour profile: Very clean, delicate, intensely aromatic — none of the bitterness of immersion cold brew. Tastes almost like tea.
Temperature: Serve at room temperature or over a single ice cube — do not dilute further
Note: Kyoto-style coffee has a completely different chemical profile from immersion cold brew — the slow, cold extraction creates clarity without the body. It is one of the most laborious coffee preparations in the world.

""",

    9557: """RECIPE:
Kissaten culture is about ritual, atmosphere, and precision — not a single recipe. Below is the kissaten master blend brew method.
---
Kissaten Master Coffee (Japanese siphon or hand drip):
Equipment: Siphon brewer (Hario, Yama Glass), or hand drip with gooseneck kettle
---
Siphon method:
20g medium-dark roast coffee (kissaten traditionally used darker roasts for the Japanese palate)
300ml filtered water
---
1. Fill bottom flask with 300ml water; heat over alcohol or halogen burner
2. Attach top flask; insert cloth filter; add coffee
3. As water heats, it rises through the siphon tube into the top flask (atmospheric pressure effect)
4. All water in the top flask: stir 3 times with a bamboo paddle, then again at the 1:00 mark
5. Remove heat source: water drops back through the filter into the bottom flask
6. Brew time is 45-60 seconds of extraction in the top flask — adjust grind to hit this window
7. Remove top flask; pour immediately from the bottom flask
---
Temperature: Serve immediately — siphon coffee cools rapidly
Note: Kissaten culture (1950s-1980s Japan) created a unique coffee aesthetic: meticulous craft, classical music, dim lighting, no hurry. The siphon brewer was a deliberate spectacle — part of the experience was watching the extraction. Many kissaten still exist in Tokyo's Shinjuku and Shibuya districts.

""",

    9558: """RECIPE:
Yield: 1 cup (300ml) | Equipment: V60 or Chemex
---
20g Costa Rican single-origin — Tarrazu region; light-medium roast; washed process
300ml water at 93-94°C
Grind: medium
---
1. Rinse filter; add grounds
2. Bloom with 40g water for 35 seconds
3. Pour steadily: 150g at 1:00, 250g at 2:00, 300g at 2:30
4. Draw-down: 3:00-3:30
---
Flavour profile: Honey sweetness, bright citric acidity (like fresh orange), malic acidity (green apple), clean finish. Tarrazu coffee grows at 1,200-1,900m in the country's most famous coffee region.
Temperature: Best at 82-88°C — the brightness is most pleasant above 80°C
Note: Costa Rica banned the cultivation of robusta by law (1989) — only arabica is grown. The "honey process" (pulped natural) originated here: the cherry is removed but some mucilage remains during drying, adding sweetness without full natural-process fruitiness. Tarrazu SHB (Strictly Hard Bean) is the highest altitude designation.

""",

    9559: """RECIPE:
Yield: 1 cup (70ml) traditional, 200ml pour over | Equipment: Traditional jebena (clay pot) or V60
---
Traditional Yemeni preparation:
12g Yemeni coffee — Haraazi or Harasi; dark roast traditional; light roast to taste origin character
70ml water per serving (strong, concentrated — the traditional cup is small)
---
Qishr (traditional spiced Yemeni coffee husk drink) variation:
15g coffee husks (qishr) — the dried outer cherry, not the bean itself
Ground ginger (1/4 tsp) and ground cinnamon (pinch)
300ml water
---
Qishr method:
1. Combine coffee husks, ginger, and cinnamon in a small pot
2. Add cold water; bring to a simmer over medium heat; simmer 10-15 minutes
3. Strain through fine mesh; add a little sugar to taste (traditional)
4. Serve in a small glass

Black coffee Yemeni method (drip):
1. 12g Yemeni coffee, medium grind, V60
2. 200ml water at 93°C
3. Standard pour over technique

---
Flavour profile: Yemeni arabica (Mocha variety — the origin of the word "mocha") is wine-like, fruity, with chocolate and spice. The terroir-driven character is unlike any other origin.
Temperature: Traditional service is very hot
Note: Yemen is the origin of commercial coffee cultivation — the first coffee houses (qahveh khaneh) opened in Aden and Mocha in the 15th century. The word "mocha" derives from the port city Al-Makha, not from chocolate.

""",

    9560: """RECIPE:
Yield: 1 serving South Indian Filter Kaapi (approximately 150ml) | Glassware: Stainless steel tumbler and dabara (saucer) | Equipment: South Indian filter coffee device
---
South Indian filter (a two-chamber metal device):
25g chicory-blend coffee (traditionally 60-80% arabica coffee + 20-40% chicory root — Narasu's, Leo, or house blend)
150ml just-boiled water
60ml warm whole milk (with 1-2 tsp sugar dissolved)
---
1. Place ground chicory-blend coffee in the upper perforated chamber of the filter
2. Press down with the small pressing disc
3. Pour just-boiled water over and replace the lid — water slowly seeps through (10-15 minutes)
4. The lower chamber collects strong, dark decoction (approximately 50ml)
5. Warm milk with sugar in a small pot
6. Combine decoction and warm milk in the tumbler (one part decoction to two parts milk)
7. "Pull" the coffee: pour back and forth between the tumbler and dabara from height 10-12 times — this aerates, mixes, and creates foam
8. Serve in the dabara (it cools faster in the shallower vessel, traditional way to drink it)
---
Temperature: Serve very hot — the pulling cools it slightly; drink immediately
Note: Filter kaapi is deeply embedded in Tamil Nadu culture. The chicory addition (a legacy of the British colonial era when coffee was expensive) is now a defining flavour, not a compromise. The pulling ritual creates a characteristic froth that is part of the identity.

""",

    9561: """RECIPE:
Yield: 1 cup (200ml) | Equipment: Chemex or V60 (both suited to Jamaican Blue Mountain's delicate character)
---
15g Jamaica Blue Mountain coffee — certified (Jamaica Agricultural Commodities Regulatory Authority seal)
225ml water at 91-92°C (slightly lower temperature — the beans are dense and delicate)
Grind: medium-fine
---
1. Rinse filter thoroughly
2. Add grounds; bloom with 30g water for 40 seconds — extended bloom for dense, high-altitude beans
3. Pour slowly: 100g at 1:00, 175g at 2:00, 225g at 2:45
4. Draw-down: 3:00-3:30
---
Flavour profile: Extremely mild — almost no bitterness; light acidity; chocolate, nuts, mild sweetness. The most approachable premium coffee in the world.
Temperature: Best at 78-85°C — the mildness and sweetness are most evident once slightly cooled
Note: Jamaica Blue Mountain must be grown above 910m in the Blue Mountain range of Jamaica — only four parishes qualify. At USD 40-100+ per pound, it is among the most expensive coffees in the world. 80% of production goes to Japan. The mildness it is famous for is often described as "elegant restraint" — it is a subtle cup, not a dramatic one.

""",

    9577: """RECIPE:
Yield: 1 cup (300ml) | Equipment: V60 or Aeropress
---
20g Peruvian single-origin — Cajamarca, Puno, or Chanchamayo region; light-medium roast; organic (Peru is a major organic coffee producer)
300ml water at 93°C
Grind: medium
---
V60:
1. Rinse filter; bloom with 40g water for 35 seconds
2. Pour steadily: 150g at 1:00, 250g at 2:00, 300g at 2:30; draw-down by 3:30
---
Flavour profile: Mild, sweet, chocolate-forward; some regions show citrus (Cajamarca); others show floral notes (Puno). Generally smooth with clean sweetness — accessible and food-friendly.
Temperature: Good at a wide range — 80-90°C
Note: Peru is one of the world's largest organic coffee producers by volume — altitude, isolation, and limited agrochemical access created organic farming by default. The coffee was historically overlooked in specialty markets; the emergence of micro-lots from Cajamarca and the Peruvian Amazon has changed this.

""",

    9578: """RECIPE:
Yield: 1 cup (200-250ml) | Glassware: Any clear glass to observe the spectacle | Equipment: Siphon brewer (Hario TCA-3 or Yama Glass)
---
20g coffee — medium-light roast (clarity of flavour suits the siphon's extraction character)
300ml filtered water
---
1. Fill the lower flask with 300ml cold or warm water; place over the burner
2. Attach the upper flask; insert the cloth or paper filter; seat it properly on the rubber grommet
3. Add 20g freshly ground coffee to the upper flask (do not add yet if water is cold — add when water approaches boiling)
4. As water heats to boiling, it rises through the siphon tube into the upper flask — this is the spectacle
5. Once all water has risen, stir the grounds-water mixture gently with a bamboo paddle
6. At 1:00 of contact time, stir once more; at 1:30, remove the heat source
7. Water draws back through the filter into the bottom flask as the temperature drops — listen for the gurgle
8. Pour from the bottom flask immediately; discard the filter puck
---
Quality indicators: A clean, clear cup with full brightness — siphon coffee is known for clarity
Temperature: Serve immediately — siphon retains heat for only a few minutes
Note: The siphon (vacuum pot) brewer was invented in Europe in the 1830s. It is the most theatrical coffee preparation in everyday use. The cloth filter (versus paper) adds very slight body. The extraction occurs at slightly below boiling — around 92-94°C in the upper flask.

""",

    9579: """RECIPE:
Yield: 1 cup cascara tea (200ml) | Glassware: Teacup or glass | Equipment: Kettle + infuser or pot
---
Cascara (dried coffee cherry husks):
8-10g dried cascara husks per 200ml water
Water temperature: 75-80°C (not boiling — like green tea)
Steep time: 4 minutes for a delicate cup; 6-7 minutes for more strength
---
1. Bring water to 75-80°C
2. Add cascara husks to an infuser or directly to the pot
3. Pour hot water over the husks
4. Steep 4 minutes for a tea-like drink; 6 minutes for more body
5. Strain and serve hot, or allow to cool and serve over ice
---
Cold cascara variation:
1. Use 15g cascara in 300ml water
2. Cold steep in refrigerator overnight (12 hours)
3. Strain and serve over ice — a light, naturally sweet, tamarind-like cold brew

Flavour profile: Hibiscus-like fruity sweetness, mild tamarind, rose hip, mild caffeine (lower than coffee). The cascara retains the fruit character of the coffee cherry with none of the coffee bitterness.
Temperature: Hot or iced — both are traditional (hot in Yemen; iced in specialty coffee culture)
Note: Cascara is the dried skin of the coffee cherry — for centuries, coffee farmers discarded it as waste. In Yemen it is qishr; in Bolivia it is sulta. The specialty coffee movement began using it circa 2010.

""",

    9580: """RECIPE:
Yield: 1 Americano or Long Black (200-250ml) | Glassware: Ceramic mug (Americano) or glass (Long Black) | Equipment: Espresso machine
---
Double espresso base: 18g coffee, 36g yield, 93°C, 25-28 seconds

Americano:
1. Pull double espresso into a mug
2. Add 150-180ml hot water to the espresso — espresso into water (not water then espresso — wrong order creates a pale, weak result)
3. Ratio: approximately 1 part espresso to 4-5 parts water; adjust to preference

Long Black (Australian/New Zealand method — the superior version):
1. Pour 150-180ml hot water into the cup first
2. Pull the double espresso over the hot water — the crema is preserved on top
3. Do not stir — the crema layer on top is the quality indicator

---
Quality indicators: Americano has minimal crema (it dissipates). Long Black has a crema layer visible on top of the water. Both should be slightly amber-tinted with full coffee flavour.
Temperature: The water should be near-boiling (90-93°C) — cold water kills the espresso
Note: The Americano was allegedly invented for American soldiers in WWII Italy who found espresso too strong. The Long Black is the Antipodean refinement — adding espresso to water (not vice versa) preserves the crema.

""",

    9581: """RECIPE:
Yield: 1 macchiato (45-60ml) | Glassware: Demitasse or small glass | Equipment: Espresso machine + steam wand
---
Double espresso: 18g coffee, 36g yield, 93°C, 25-28 seconds

Espresso macchiato:
1. Pull double espresso into a demitasse
2. Steam 15-20ml whole milk to 65°C with microfoam
3. Add one small dollop (approximately 15ml) of microfoam to the centre of the espresso — "marking" it
4. The foam sits as a small white dot in the centre of the brown espresso — this is the macchiato

Latte macchiato (layered version):
1. Steam 150ml milk to 65°C with microfoam
2. Pour the steamed milk into a tall glass first
3. Pull a single espresso through the foam — the espresso falls through and marks the milk with a brown layer in the middle
4. Three distinct layers: foam on top, espresso in the middle, milk at the bottom

---
Temperature: Serve immediately — the espresso macchiato is the smallest drink and cools fastest
Note: "Macchiato" means "stained" or "marked" in Italian. The espresso macchiato is espresso stained with milk. The latte macchiato is milk stained with espresso. They are different drinks despite the shared name.

""",

    9582: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass or coupe | Equipment: Espresso machine or cold brew

White Russian:
45ml vodka — Ketel One
22.5ml Kahlua
30ml heavy cream
---
1. Combine vodka and Kahlua in a rocks glass over ice
2. Pour cream slowly over the back of a spoon so it floats
3. Or stir all together for a richer, mixed version

Espresso Martini (reference to cocktail entry 8791)
Irish Coffee (reference to coffee entry 9505)

Coffee Old Fashioned:
60ml bourbon — Woodford Reserve
5ml coffee liqueur — Mr Black
5ml demerara syrup
2 dashes coffee bitters — Bittermens New Orleans Coffee Bitters
---
1. Combine all in mixing glass over ice; stir 25 seconds; strain over large ice cube

Black Russian:
60ml vodka
30ml Kahlua
---
Build in a rocks glass over ice; stir gently

---
Temperature: Varies by cocktail — cold for all listed
Note: Coffee cocktails benefit from quality coffee — either fresh espresso (for foam and aromatics) or premium cold brew concentrate (for smoothness and depth). Kahlua (20% ABV, 7.7% coffee) and Mr Black (25% ABV, significantly more coffee) produce markedly different results.

""",

    9583: """RECIPE:
This is a knowledge entry — below is a cupping guide to taste the difference.
---
Comparison cupping: single origin vs blend
Equipment: Two cupping bowls, scale, kettle
---
8g per 120ml for each:
Bowl 1: single-origin Ethiopian Yirgacheffe (light roast)
Bowl 2: commercial espresso blend (medium-dark roast, typically 2-4 origins)
---
1. Grind each coarsely; place in separate labeled bowls
2. Pour 93°C water simultaneously; steep 4:00
3. Break crust; skim; taste at 8:00 and again at room temperature
---
What you should experience:
Single origin: Distinct, recognizable flavour profile (floral, citrus, bright acidity). Changes noticeably as it cools — tells a story of place.
Blend: Balanced, consistent, round. Less dramatic individual notes — the whole exceeds the sum of its parts. Does not change much as it cools.
---
When each is right:
Single origin: Filter coffee, pour over, siphon — when clarity and origin character are the goal
Blend: Espresso, milk-based drinks — when consistency and harmony across a blend are required (milk mutes individual notes)

Note: Neither is superior — they serve different purposes. A single-origin Ethiopian espresso is extraordinary. The same coffee in a latte may be overwhelmed by milk. Blending was invented to solve the problem of consistency across seasons and harvests.

""",

    9584: """RECIPE:
Yield: 1 cup | Equipment: Your preferred brewer — the method is identical to regular coffee
---
Water temperature: 93°C (same as regular coffee — decaf often benefits from slightly higher temp)
Dose and ratio: Same as regular coffee (1:15 for filter; 1:2 for espresso)
Grind: Same as regular coffee for the same brewer
---
Brewing decaf coffee — standard V60:
20g decaf coffee ground medium
300ml water at 93-94°C
1. Bloom with 40g water for 30-35 seconds
2. Pour steadily: 150g at 1:00, 250g at 2:00, 300g at 2:30
3. Draw-down by 3:00-3:30

For espresso decaf:
18g decaf coffee ground fine
Target yield: 36-40g (slightly more than regular — decaf benefits from a touch more extraction)
Temperature: 92-94°C
Time: 25-30 seconds (may run slightly faster than regular coffee — adjust grind accordingly)

---
Flavour profile: With quality Swiss Water Process or CO2-process decaf: chocolate, caramel, nuts. Mountain Water Process retains origin character well.
Note: Decaf coffee retains 97% of caffeine is removed, 3% remains — this is significant for highly sensitive individuals. Swiss Water Process (no chemical solvents) and CO2 Process produce the cleanest flavour. The flavour deficit in decaf is real but smaller than most assume.

""",

    9585: """RECIPE:
This is a pairing guide entry — no brewing recipe. Below is a framework for coffee and food pairing.
---
Coffee pairing framework (Q-grader approach):

Espresso-based (high intensity, bitter-sweet):
Pairs with: Chocolate (70%+ dark), biscotti, cantucci, walnut cake, aged cheeses
Avoid: Delicate fish, light salads, fresh fruit (bitterness overwhelms)

Filter/pour over (light, bright, acidic):
Pairs with: Pastries, croissants, fresh berries, lemon tart, soft cheese
Avoid: Heavy red meat (acid clashes), very spicy food

Cold brew (sweet, low-acid, chocolate-forward):
Pairs with: Vanilla desserts, caramel, milk chocolate, soft cheeses, smoked meats
Avoid: Very acidic foods (redundant)

Specific pairings:
Ethiopian Yirgacheffe + dark chocolate: Floral coffee with 70% dark creates complexity that exceeds either alone
Kenyan AA + cheesecake: The blackcurrant acidity of Kenyan cuts through fat beautifully
Brazilian Santos + chocolate cake: Like-meets-like; the chocolate-chocolate conversation deepens both

Note: The same principles as wine pairing apply: acidity cuts fat, bitterness complements sweetness, weight should match weight.

""",

    9586: """RECIPE:
This is a movement history entry — below is a cupping protocol to experience the specialty difference.
---
Specialty vs commercial comparison:
Brew two cups side by side:
1. Commercial ground coffee (supermarket bag, no origin listed): 20g in 300ml at 93°C, V60 method
2. Specialty single-origin (transparent origin, freshly roasted within 2-4 weeks): same ratio, same method
---
What you should experience in the specialty cup:
1. Distinct flavour notes (specific fruit, floral, or nut character — not generic "coffee")
2. Sweetness in the finish without adding sugar
3. Acidity that is pleasant, not harsh (like fresh fruit, not vinegar)
4. No bitterness that doesn't belong
5. Aroma that changes as the cup cools — complexity, not flatness

What commercial coffee typically provides:
1. Generic roast character
2. Reliable but undistinctive flavour
3. Often slight rubber or cardboard notes (stale)
4. Consistent bitterness that requires milk and sugar

Note: The Specialty Coffee Association (SCA) defines specialty coffee as scoring 80+ on a 100-point cupping scale, with zero primary defects and maximum 5 secondary defects per 350g. Less than 10% of global coffee production qualifies. Freshness is the single biggest variable in your control.

""",

    9606: """RECIPE:
Yield: 1 cold foam coffee | Glassware: Tall glass (16oz) | Equipment: Milk frother or blender + espresso machine or cold brew

Cold Foam Cold Brew (primary recipe):
Cold brew concentrate 90ml (1:4 ratio, 12-hour steep — see entry 9468)
Cold water 90ml (or oat milk for a richer result)
Cold foam 60ml (see below)
Ice (full glass)
---
Cold foam:
60ml cold whole milk (or non-fat milk for more stable foam; or cold oat milk for vegan)
10ml simple syrup or vanilla syrup
---
Cold foam method:
1. Combine cold milk and syrup in a frothing pitcher
2. Use a handheld frother or blender on high speed for 30-45 seconds — the goal is thick, stable, pourable foam
3. The foam should be thick enough to spoon but pourable — not stiff peaks, not liquid
4. Refrigerate for up to 2 hours if not using immediately

Assembly:
1. Fill tall glass with ice
2. Add cold brew concentrate and cold water (or oat milk), stir briefly
3. Pour cold foam gently over the top — it should sit as a distinct white layer
4. Add flavoured syrup (vanilla, cinnamon, caramel) if desired

Nitro Cold Brew (requires nitrogen tap):
1. Load cold brew keg with nitro; dispense through a stout faucet
2. The nitrogen creates a cascading effect and creamy head — no additional ingredients needed

---
Temperature: Serve immediately — cold foam begins to integrate after 10-15 minutes
Note: Cold foam was popularized by Starbucks but originated in specialty coffee's nitrogen experimentation. The key difference from hot milk foam: cold milk does not thermally denature proteins the same way; the foam is created mechanically and is inherently less stable. Higher fat content = less stable foam; less fat = more stable but thinner foam.

""",
}


def main():
    conn = psycopg2.connect(DB_WRITE)
    cur = conn.cursor()
    success = 0
    errors = 0
    for entry_id, recipe in RECIPES.items():
        try:
            cur.execute(
                "UPDATE technique_references SET pro_tips = %s || pro_tips WHERE id = %s",
                (recipe, entry_id)
            )
            success += 1
        except Exception as e:
            print(f"ERROR on id={entry_id}: {e}")
            errors += 1
            conn.rollback()
            conn = psycopg2.connect(DB_WRITE)
            cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()
    print(f"Done. {success} coffee recipes added, {errors} errors.")


if __name__ == "__main__":
    main()
