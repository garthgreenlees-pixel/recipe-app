#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

RECIPES = {

9826: """RECIPE — Sparkling Mineral Water Infusion Service
Yield: 1 serve | Glassware: Tall crystal highball | Ice: Large clear cube
---
200ml Perrier or San Pellegrino sparkling mineral water (well chilled)
3 thin slices English cucumber (unpeeled, organic)
2 slices fresh lime, 2mm thick
1 sprig fresh mint (5–6 leaves, bruised)
Pinch fleur de sel (optional, enhances mineral perception)
---
1. Chill glass in freezer for 5 minutes or pack with ice and discard.
2. Add ice cube to glass. Layer cucumber slices against inside of glass.
3. Add lime slices and bruised mint sprig.
4. Pour sparkling water slowly down the side of the glass to preserve carbonation.
5. Rest 30 seconds before serving — allows botanicals to bloom without over-dilution.
---
Garnish: Cucumber ribbon curled around the rim; lime wheel
Temperature: 4–6°C; never room temperature — mineral expression dulls above 8°C

""",

9827: """RECIPE — Seedlip & Tonic (Classic Serve)
Yield: 1 drink | Glassware: Copa de Balon (balloon gin glass) | Ice: Oversized cube or sphere
---
50ml Seedlip Spice 94 (warm, cardamom-forward; OR Seedlip Garden 108 for herbal)
150ml Fever-Tree Mediterranean Tonic Water
3 drops Angostura bitters (optional — adds complexity without alcohol)
---
1. Fill copa de balon glass with large ice — fill to brim for maximum chill and minimum dilution.
2. Pour Seedlip over ice. Stir once gently to chill.
3. Add bitters to tonic bottle, then pour tonic water slowly down a bar spoon held against the glass side — preserve carbonation.
4. Do not stir after adding tonic.
---
Garnish: Pink grapefruit twist (expressed over surface, then placed); 2 cardamom pods (cracked, floated)
Temperature: Serve immediately; glass should feel cold to hold

""",

9828: """RECIPE — Lyre's Non-Alcoholic Negroni
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
25ml Lyre's Amaretti (non-alcoholic amaro)
25ml Lyre's Aperitif Rosso (non-alcoholic sweet vermouth)
25ml Lyre's Italian Orange (non-alcoholic Campari)
---
1. Fill mixing glass with ice. Add all three Lyre's spirits.
2. Stir 40 rotations — full dilution is essential; NA spirits need more stirring than alcoholic to integrate.
3. Strain into rocks glass over a single large ice cube.
4. The louche orange colour should appear through the ice — tilt glass to check.
---
Garnish: Wide orange peel expressed over the surface (oils spray visible), skin-side down on the rim
Temperature: Serve at 5–7°C

""",

9829: """RECIPE — Strawberry-Balsamic Drinking Shrub (Craft & Serve)
Yield: ~500ml shrub syrup (approx. 16 serves) | Glassware: Highball | Ice: Cubed
---
SHRUB SYRUP (cold-process method):
250g ripe strawberries, hulled and halved
250g white caster sugar
120ml raw apple cider vinegar (Bragg's or Forum)
10ml aged balsamic vinegar
Pinch of black pepper

SERVE (per glass):
30ml shrub syrup
150ml sparkling water
Squeeze of lemon
---
1. Macerate strawberries in sugar for 24–48 hours in a sealed jar. Shake daily.
2. Strain pulp through fine-mesh sieve without pressing — push lightly if needed.
3. Add both vinegars to strained liquid. Stir to combine. Taste for balance.
4. Bottle and refrigerate; improves over 1–2 weeks. Keeps 3 months.
5. To serve: fill highball with ice, add 30ml shrub, top with sparkling water, stir once.
---
Garnish: Strawberry half on rim; cracked black pepper
Temperature: Serve cold. Shrub stores at 4°C.

""",

9830: """RECIPE — Classic American Switchel (Haymaker's Punch)
Yield: 1 litre (approx. 4 serves) | Glassware: Mason jar or highball | Ice: Cubed
---
1 litre cold water (filtered)
60ml raw apple cider vinegar (Bragg's)
3 tbsp raw honey OR 2 tbsp molasses (for deeper flavour)
1 tsp freshly grated ginger (or 2 tsp ginger juice)
Pinch of sea salt
Squeeze of lemon (optional)
---
1. Combine all ingredients in a large jar or jug. Stir vigorously until honey/molasses fully dissolves.
2. Taste: balance is key — should be tart, sweet, and ginger-warm in equal measure.
3. Refrigerate 1–4 hours to let ginger infuse and flavours integrate.
4. Serve over ice in mason jars or highball glasses.
5. Shake or stir before each pour as ginger settles.
---
Garnish: Ginger slice and lemon wheel
Temperature: Serve cold, 4–8°C

""",

9831: """RECIPE — Artisan Ginger-Lemon Craft Soda
Yield: 1 litre soda base (8–10 serves) | Glassware: Highball or Collins | Ice: Cubed
---
GINGER SYRUP BASE:
150g fresh ginger, peeled and thinly sliced
300g white sugar
300ml water
Zest of 2 lemons
---
SERVE (per glass):
30ml ginger syrup
20ml fresh lemon juice
120ml soda water (top quality — Fever-Tree or San Pellegrino)
---
1. Combine ginger, sugar, water, and lemon zest in saucepan. Bring to boil, stir to dissolve.
2. Simmer 10 minutes. Remove from heat, steep 30 minutes covered.
3. Strain through fine sieve. Cool completely. Bottle and refrigerate (keeps 3 weeks).
4. To serve: fill highball with ice. Add ginger syrup, then lemon juice.
5. Pour soda water down a spoon — preserve bubbles. Stir once at the base.
---
Garnish: Crystallised ginger on a cocktail pick; lemon twist
Temperature: 4–6°C

""",

9832: """RECIPE — Signature Cold-Press Green Juice
Yield: 250ml (1 serve) | Glassware: Tall straight glass | Ice: None (cold-pressed is served neat)
---
150g English cucumber (unpeeled, organic)
100g celery (2 stalks, strings included)
80g green apple (Granny Smith, cored, unpeeled)
50g fresh spinach or kale
20g fresh ginger, peeled
1 lemon, peeled (white pith minimised)
Small handful flat-leaf parsley
---
1. Wash all produce thoroughly. Cut to fit juicer feed tube.
2. Process in order: cucumber → celery → apple → greens → ginger → lemon → parsley.
3. Press immediately and consume within 20 minutes for maximum enzyme activity.
4. If using a slow masticating juicer (Norwalk or Hurom): process at low rpm, no heat generated.
5. Strain through fine sieve if using centrifugal juicer — removes oxidising foam.
---
Garnish: Cucumber round floated on surface; squeeze of extra lemon to order
Temperature: Serve at 8–10°C; never warmer

""",

9833: """RECIPE — Watermelon Agua Fresca
Yield: 1 litre (4 serves) | Glassware: Tall glass or clay cup | Ice: Cubed
---
800g seedless watermelon flesh (approximately half a small melon)
500ml cold filtered water
Juice of 2 limes (approx. 60ml)
1–2 tbsp agave nectar or caster sugar (adjust to watermelon sweetness)
Pinch of sea salt (brightens flavour)
8 fresh mint leaves (optional)
---
1. Blend watermelon flesh until smooth — 30 seconds in high-speed blender.
2. Strain through fine-mesh sieve, pressing gently. Discard fibrous pulp.
3. Combine strained watermelon juice with water, lime juice, sweetener, and salt.
4. Taste and adjust — should be light, refreshing, not too sweet.
5. Refrigerate until cold. Serve over ice in tall glasses.
---
Garnish: Watermelon triangle wedge on rim; mint sprig; pinch of Tajín (chilli-lime salt) on rim for Mexican style
Temperature: 4–6°C

""",

9834: """RECIPE — Homemade Kefir (Milk Kefir Culture)
Yield: 500ml per batch | Glassware: Short wide tumbler | Ice: None
---
500ml whole milk (organic, non-homogenised preferred; goat's milk for lighter flavour)
1–2 tbsp live kefir grains (active, cauliflower-like colonies)
---
1. Place kefir grains in a clean glass jar (not metal — acids react).
2. Add milk. Cover loosely with cloth or breathable lid — kefir grains need airflow.
3. Ferment at room temperature (20–24°C) for 24–36 hours. Longer = more tart.
4. Gently shake jar every 8–12 hours to distribute cultures.
5. When kefir thickens slightly and smells pleasantly tangy, strain through plastic sieve.
6. Reserved grains go back into fresh milk immediately for next batch.
7. Refrigerate finished kefir — flavour continues to develop.
---
Garnish: For serving, top with raw honey and a pinch of cinnamon; or serve plain in a small tumbler
Temperature: Consume cold (4–6°C). Best within 1 week.

""",

9835: """RECIPE — Craft Lemonade with Rosemary Syrup
Yield: 1 serve | Glassware: Collins glass | Ice: Cubed
---
20ml fresh lemon juice (approx. 1 large lemon, strained)
15ml rosemary simple syrup (2:1 sugar:water, steeped with 3 rosemary sprigs 20 min)
150ml cold filtered water OR sparkling water for fizzy version
Pinch of sea salt
---
ROSEMARY SYRUP:
200g white sugar, 100ml water, 3 sprigs rosemary → bring to boil, simmer 5 min, steep 20 min, strain
---
1. Make rosemary syrup ahead; cool completely. (Keeps refrigerated 3 weeks.)
2. In glass filled with ice: add lemon juice, then rosemary syrup, then pinch of salt.
3. Top with water. Stir from bottom to distribute syrup.
4. Taste: adjust with extra lemon or syrup.
---
Garnish: Lemon wheel and fresh rosemary sprig; lemon twist expressed over the top
Temperature: 4–6°C; serve immediately

""",

9876: """RECIPE — The Virgin Paloma (Signature Mocktail)
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
60ml fresh pink grapefruit juice (strained)
20ml fresh lime juice
15ml agave nectar (dissolved in equal water = agave syrup)
3 drops saline solution (4:1 water:salt) OR pinch of sea salt
100ml Fever-Tree Pink Grapefruit Soda (or Jarritos Toronja)
---
1. Combine grapefruit juice, lime juice, agave syrup, and saline in a shaker with ice.
2. Shake 8–10 seconds — chill without over-diluting.
3. Strain into ice-filled highball glass.
4. Top with grapefruit soda. Do not stir — layered carbonation is part of the serve.
5. Taste: should be tart, sweet, bitter, refreshing in balance.
---
Garnish: Tajín-salted rim (half only), dehydrated grapefruit wheel, fresh mint
Temperature: Serve immediately; 5–7°C

""",

9877: """RECIPE — Ashwagandha Adaptogen Golden Tonic
Yield: 1 serve | Glassware: Small wide mug or ceramic cup | Ice: None (served warm)
---
250ml oat milk (Oatly Barista or Minor Figures)
1 tsp ashwagandha powder (KSM-66 extract preferred)
1 tsp raw honey
½ tsp ground turmeric
¼ tsp ground cinnamon
Pinch of black pepper (enhances curcumin absorption)
Pinch of cardamom
Optional: ½ tsp lion's mane powder (cognitive support)
---
1. Warm oat milk in small saucepan over medium-low heat to 65–70°C — do not boil.
2. Add all powders and honey. Whisk vigorously or use hand frother for 30 seconds.
3. Taste: adjust sweetness with honey; earthiness of ashwagandha should be present but not dominating.
4. Pour through fine sieve if powders clump.
5. Serve in warmed ceramic cup.
---
Garnish: Pinch of cinnamon dusted over froth; edible gold flake for premium service
Temperature: Serve at 65–68°C; earthenware retains heat well

""",

9878: """RECIPE — Coconut Water Electrolyte Recovery Drink
Yield: 500ml (1 serve or 2 half-serves) | Glassware: Tall glass | Ice: Cubed
---
350ml 100% pure coconut water (Harmless Harvest Pink Coconut Water or Vita Coco Pure)
100ml cold filtered water
Juice of 1 lime (approx. 25ml)
½ tsp raw honey
Pinch of sea salt (sodium electrolyte)
Pinch of ground ginger (optional, digestive)
---
1. Combine all ingredients in a glass. Stir until honey and salt dissolve.
2. Taste: slightly sweet, faintly salty, refreshing. Adjust salt if needed.
3. For post-exercise serve: add an extra pinch of salt and 1 tsp honey for glycogen.
4. Coconut water is best consumed fresh; pink coconut water is not pasteurised — keep refrigerated.
---
Garnish: Lime wedge on rim; if served in a young coconut, omit garnish and serve with a wide straw
Temperature: 4–8°C

""",

9879: """RECIPE — NA Beer Michelada-Style (Zero-Proof)
Yield: 1 serve | Glassware: Chilled pint glass or large goblet | Ice: Cubed
---
330ml Heineken 0.0 or Lucky Saint Unfiltered Lager (0.5%) — chilled hard
Juice of 1 lime (approx. 25ml)
2 dashes of hot sauce (Cholula or Valentina)
2 dashes Worcestershire sauce
Pinch of sea salt
Pinch of Tajín or celery salt for rim
---
1. Rim the glass: rub lime wedge around rim, then dip in Tajín/celery salt mix. Fill with ice.
2. In the glass: add lime juice, hot sauce, Worcestershire, and salt. Stir.
3. Pour NA beer slowly down the side of the glass — preserve carbonation.
4. Do not stir after adding beer.
5. Taste through a straw from the base to check balance.
---
Garnish: Lime wedge on rim, celery stick for stirring
Temperature: NA beer must be served at 2–4°C; the colder the better for this style

""",

9880: """RECIPE — Non-Alcoholic Wine Service & Pairing
Yield: 1 serve | Glassware: Appropriate varietal glass (Burgundy or Bordeaux) | Ice: None
---
125ml Leitz Eins Zwei Zero Riesling (NA) or Ariel Blanc (Chardonnay style)
OR Torres Natureo (Muscat style, 0.5%)
---
SERVICE PROTOCOL:
1. Serve at varietal-appropriate temperature: NA whites at 8–10°C, NA reds at 16–18°C.
2. Decant NA reds 15 minutes before service — dealcoholised reds benefit from aeration.
3. Pour against the side of the glass, tilting 45° — same as still wine service.
4. Allow 2 minutes in glass before assessing aroma — aromatics develop with slight warming.
5. PAIRING NOTE: Leitz Riesling (0.0%): oysters, sea bass, Asian spice. Ariel Blanc: soft cheeses, white fish.
---
Garnish: No garnish in wine glass. Lemon twist in presentation is acceptable.
Temperature: Whites 8–10°C, dealcoholised reds 16–18°C (not cellar cold)

""",

9881: """RECIPE — Warm Spiced Milk (Haldi Doodh / Turmeric Golden Milk)
Yield: 1 serve | Glassware: Ceramic mug or heatproof glass | Ice: None
---
250ml whole milk (or oat milk for dairy-free)
1 tsp ground turmeric
½ tsp ground ginger (or 1 tsp fresh grated)
¼ tsp ground cinnamon
Pinch of black pepper (essential for curcumin bioavailability)
1 tsp raw honey or jaggery
¼ tsp coconut oil or ghee (optional, aids fat-soluble curcumin absorption)
---
1. Combine milk and all spices in a small saucepan over medium heat.
2. Whisk constantly as milk heats — prevent scorching on the base.
3. Heat to 68–72°C (just before steaming point). Do not boil.
4. Remove from heat. Stir in honey/jaggery until dissolved.
5. Strain through fine sieve if whole spices were used. Pour into warmed mug.
---
Garnish: Pinch of cinnamon, cracked black pepper, and dried rose petals for premium service
Temperature: Serve at 68°C; allow to cool to 60°C before drinking

""",

9882: """RECIPE — Homemade Oat Milk (Barista Method)
Yield: 1 litre | Glassware: N/A (for use in coffees and recipes) | Ice: N/A
---
100g rolled oats (not instant; Quaker Old Fashioned preferred)
1 litre cold filtered water (cold is critical — warm water causes sliminess)
Pinch of sea salt
1 tsp vanilla extract (optional)
1 Medjool date (pitted, optional for sweetness)
---
1. Combine oats, cold water, salt, and date in high-speed blender. Blend 30–45 seconds ONLY.
2. Do not over-blend — oats release starch creating slimy texture.
3. Strain immediately through nut milk bag, squeezing gently once. Do not press hard.
4. Store in sealed bottle in fridge. Shake well before each use. Use within 4–5 days.
5. BARISTA TIP: heat slowly and froth at 60–65°C for latte art — higher temps break the foam.
---
Garnish: N/A — used as milk substitute in drinks
Temperature: Refrigerate at 4°C; froth at 60–65°C for coffee drinks

""",

9883: """RECIPE — Homemade Ginger Beer (Fermented or Forced-Carbonation)
Yield: 1 litre (4–6 serves) | Glassware: Highball | Ice: Cubed
---
GINGER BEER BASE:
60g fresh ginger, roughly grated (unpeeled)
150g white sugar
Juice of 2 limes (approx. 50ml)
1 litre filtered water
¼ tsp active dry yeast (for fermented version only)
---
1. Boil 250ml water with sugar until dissolved. Add grated ginger. Steep 30 minutes off heat.
2. Strain into clean bottle (or fermentation vessel). Add lime juice and remaining cold water.
3. FERMENTED: Add yeast dissolved in 2 tbsp warm water. Seal. Ferment 24–48 hrs at room temp.
   QUICK: Add ½ tsp citric acid instead of yeast. Carbonate with SodaStream or CO₂ charger.
4. Taste before sealing fermented version — should be spicy, tart, barely sweet.
5. Refrigerate to stop fermentation once carbonation is achieved.
---
Garnish: Lime wheel, crystallised ginger, mint sprig
Temperature: 4–6°C; highly carbonated versions should be opened slowly

""",

9884: """RECIPE — Focus Functional Tonic (Adaptogen & Nootropic)
Yield: 1 serve | Glassware: Rocks glass | Ice: Large cube
---
30ml lion's mane mushroom tincture (Four Sigmatic or Rainbo)
15ml fresh lemon juice
10ml raw honey syrup (1:1 honey:water)
3 dashes CBD bitters (optional, Strangely Specific or Flora CBD)
150ml Fever-Tree Elderflower Tonic Water
---
1. Combine lion's mane tincture, lemon juice, and honey syrup in shaker with ice.
2. Shake briefly (5 seconds) — just to combine and chill.
3. Strain into rocks glass over large ice cube.
4. Add bitters. Top with elderflower tonic water gently.
5. Stir once at the base — keep carbonation intact.
---
Garnish: Lemon twist, dried mushroom slice (if available), sprig of rosemary (cognitive association)
Temperature: Serve at 5–7°C; consume within 15 minutes of preparation

""",

9885: """RECIPE — Homemade Tepache (Mexican Pineapple Ferment)
Yield: 2 litres (approx. 8 serves) | Glassware: Clay cup or highball | Ice: Cubed
---
1 ripe pineapple — peel and core (fruit reserved for eating)
150g piloncillo or dark brown sugar (per litre)
2 litres filtered water (room temperature)
2 cinnamon sticks
6 whole cloves
Optional: 2 star anise, 2 dried chillies
---
1. Wash pineapple peel thoroughly. Combine peel, core, sugar, spices in large glass vessel.
2. Add water. Cover with muslin or breathable cloth — fermentation requires air exchange.
3. Leave at room temperature (22–26°C) for 24–72 hours. Taste from 36 hours.
4. Fermentation complete when pleasantly tangy, effervescent, not overly sour (vinegar = over-fermented).
5. Strain through fine sieve. Refrigerate to halt fermentation.
6. Serve over ice. Can be mixed 1:1 with sparkling water for lighter serve.
---
Garnish: Pineapple wedge, lime wedge, chilli rim (Tajín)
Temperature: Serve at 4–6°C; keeps refrigerated 1 week

""",

9921: """RECIPE — Artisan Hot Chocolate (Valrhona Method)
Yield: 1 serve (250ml) | Glassware: Wide ceramic mug | Ice: None
---
40g Valrhona Guanaja 70% dark chocolate, finely chopped (or Callebaut 811)
200ml whole milk
50ml double cream
1 tsp unrefined cane sugar (adjust to chocolate sweetness)
Pinch of fleur de sel
¼ tsp pure vanilla extract
Optional: pinch of cayenne or cinnamon (Aztec style)
---
1. Heat milk and cream in small saucepan to 70°C — just before steaming.
2. Remove from heat. Add chopped chocolate. Wait 1 minute for chocolate to melt.
3. Whisk vigorously until fully emulsified and glossy — 2 minutes.
4. Add sugar, salt, and vanilla. Taste and adjust.
5. Return to low heat if needed to reach serving temperature (65–68°C). Do not boil.
6. Pour through fine sieve if any unmelted chocolate remains.
---
Garnish: Soft whipped cream (unsweetened); Valrhona cocoa powder dusted through fine sieve; optional fleur de sel crystal
Temperature: Serve at 65–68°C in a pre-warmed mug

""",

9922: """RECIPE — Virgin Aperol Spritz (NA Aperitivo)
Yield: 1 cocktail | Glassware: Large wine glass | Ice: Cubed
---
60ml Lyre's Italian Orange (non-alcoholic Campari alternative)
OR Crodino Aperitivo (non-alcoholic, naturally bitter)
120ml Fever-Tree Sparkling Blood Orange (or Premium Soda Water)
60ml Lyre's American Malt (NA prosecco substitute) OR fresh blood orange juice
---
1. Fill large wine glass to the brim with good ice.
2. Add Lyre's Italian Orange (or Crodino) over the ice.
3. Add the NA sparkling/malt alternative.
4. Top with soda water or blood orange juice. Do not stir — let layers settle.
5. Ratio guidance: 3 parts soda : 2 parts NA spirit : 1 part accent.
---
Garnish: Full orange wheel inside the glass, green olive on a pick (traditional), mint sprig
Temperature: 5–7°C; ice must be fresh and plentiful

""",

9923: """RECIPE — Sparkling Elderflower and Pear Celebration Drink
Yield: 1 serve | Glassware: Champagne flute or coupe | Ice: None
---
20ml elderflower cordial (Belvoir Organic or St-Germain NA substitute)
20ml fresh pear juice (pressed, strained)
5ml fresh lemon juice
100ml chilled sparkling water (Perrier) or dry sparkling grape juice
1 drop rose water (optional)
---
1. Chill flute in freezer 5 minutes or rinse with ice water.
2. Combine elderflower cordial, pear juice, lemon juice, and rose water in a small jug. Stir.
3. Pour into flute. Top slowly with sparkling water — pour down the inside of the tilted glass.
4. Do not stir in flute — bubbles will carry flavours upward.
---
Garnish: Edible flower floated (violet or borage); thin pear slice draped over rim; dehydrated lemon wheel
Temperature: Serve at 4–6°C — flute should be cold to the touch

""",

9924: """RECIPE — Matcha Latte (Ceremonial Grade, Barista Method)
Yield: 1 serve | Glassware: Ceramic handleless cup or 240ml glass | Ice: None
---
3g ceremonial grade matcha powder (Ippodo Kan-iku or Marukyu Koyamaen)
30ml hot water at 75–80°C
200ml oat milk or whole milk (Oatly Barista preferred)
5ml simple syrup (optional, if sweetness desired)
---
1. Sift matcha through fine sieve into bowl or cup. (Eliminates clumping.)
2. Add 30ml water at 75–80°C. Whisk in W or M motion with chasen bamboo whisk.
3. Whisk 20–30 seconds until fully dissolved, frothy, no sediment on bowl base.
4. Steam milk to 60–65°C — stretch gently for microfoam (not stiff cappuccino foam).
5. Pour matcha concentrate into cup. Pour steamed milk over the back of a spoon to layer.
6. Finish with latte art pour if trained — classic rosette or heart.
---
Garnish: Light ceremonial matcha dusted through fine sieve; no garnish if latte art is present
Temperature: Serve at 60–65°C; matcha degrades if too hot

""",

9925: """RECIPE — Bone Broth Elixir (Umami Service)
Yield: 1 serve (200ml cup) | Glassware: Warmed bone china cup or handle-free ceramic | Ice: None
---
200ml rich beef or chicken bone broth (Kettle & Fire or homemade, 24-hour simmered)
1 tsp white miso paste (Shiro miso — lighter, sweeter)
½ tsp grated fresh ginger
2 drops toasted sesame oil
Pinch of sea salt (taste first — broth may already be seasoned)
Optional: ½ tsp apple cider vinegar (brightens)
---
1. Warm broth in small saucepan to 80°C — do not boil (destroys collagen gelatin texture).
2. Whisk miso paste with 2 tbsp warm broth first — prevents clumping.
3. Add miso mixture back to saucepan with ginger. Stir well.
4. Remove from heat. Add sesame oil. Taste and adjust salt.
5. Strain through fine sieve into pre-warmed cup.
---
Garnish: Thinly sliced green onion (scallion); sesame seeds; a sliver of nori; fresh ginger coin
Temperature: Serve at 75–80°C; bone broth cools rapidly in bone china — pre-warm cup

""",

9926: """RECIPE — Thai Iced Tea with Coconut Milk
Yield: 1 serve | Glassware: Tall glass | Ice: Crushed or cubed
---
2 tbsp Thai tea blend (Number One Brand or ChaTraMue) OR strong Ceylon black tea with 2 star anise
250ml boiling water
2 tbsp sweetened condensed milk (or 1 tbsp each condensed + evaporated)
3 tbsp full-fat coconut milk (Aroy-D or Chaokoh)
Optional: orange food colouring (traditional style) OR saffron infusion (natural)
---
1. Steep Thai tea or spiced black tea in 250ml boiling water for 5 minutes. Strain.
2. Stir condensed milk into hot tea until dissolved. Taste — should be sweet and rich.
3. Allow to cool to room temperature, then refrigerate until cold.
4. Fill glass with ice. Pour cold tea mixture over ice to 2/3 full.
5. Slowly pour coconut milk over the back of a spoon — creates the signature layered float.
---
Garnish: Do not stir before serving — the orange-and-white layered gradient is part of the presentation. Serve with a straw.
Temperature: Serve at 2–4°C; coconut float melts slowly into the drink as it's consumed

""",

9927: """RECIPE — Mulled Spiced Non-Alcoholic Cider
Yield: 1 litre (4 serves) | Glassware: Heatproof glass mug | Ice: None
---
1 litre pressed apple juice (unfiltered cloudy, Bulmers or local artisan)
1 cinnamon stick
4 whole cloves
3 star anise
1 orange, sliced into rounds
2 cardamom pods, lightly crushed
1 vanilla pod, split
1 tbsp raw honey or brown sugar (adjust to apple juice sweetness)
---
1. Combine all ingredients in a large saucepan. Heat slowly over medium-low heat.
2. Do not boil — aim for 75–80°C (steaming but not bubbling). Boiling drives off aromatics.
3. Simmer on lowest heat for 20–30 minutes. Taste every 10 minutes.
4. Strain through fine sieve. Stir in honey/sugar if desired. Taste.
5. Serve in heatproof mugs. Ladle from pot to preserve warmth.
---
Garnish: Cinnamon stick in mug, orange slice draped over rim, star anise floated
Temperature: Serve at 70–75°C; keep on lowest heat setting to maintain temperature during service

""",

9928: """RECIPE — Rose and Hibiscus Botanical Water
Yield: 1 litre (4–6 serves) | Glassware: Crystal tumbler | Ice: Large cube or sphere
---
1 litre cold filtered water
15g dried hibiscus flowers (food grade)
5g dried rose petals (organic, unsprayed)
1 strip lemon peel (no white pith)
1 strip orange peel
1 tbsp raw honey (dissolved in 2 tbsp warm water first)
---
1. Combine all ingredients in a glass jar. Cover and refrigerate.
2. Cold infuse for 8–12 hours (overnight). Longer = deeper colour and flavour.
3. Strain through fine sieve. Taste: should be floral, fruity, gently astringent from hibiscus.
4. Adjust sweetness with honey water. Add a squeeze of lemon if desired.
5. Serve over large ice in crystal tumblers. The deep crimson colour is the visual centrepiece.
---
Garnish: Dried hibiscus flower floated; dried rose petal; lemon twist
Temperature: 4–6°C; the colour is best appreciated in clear glassware

""",

9929: """RECIPE — London Fog (Earl Grey Latte)
Yield: 1 serve | Glassware: Tall heatproof glass or ceramic mug | Ice: None
---
1 bag Twinings Earl Grey (or TWG Silver Moon loose-leaf, 2g)
180ml hot water at 95°C
15ml vanilla syrup (1:1 sugar:water with 1 tsp vanilla extract, steeped)
150ml whole milk or oat milk (Oatly Barista)
---
1. Steep Earl Grey for 4–5 minutes in 180ml water at 95°C. Remove bag/leaves.
2. Stir vanilla syrup into tea concentrate.
3. Steam milk to 65°C — frothy microfoam, not stiff foam. Oat milk froths best at 60–65°C.
4. Pour tea concentrate into glass. Pour steamed milk over the back of a spoon.
5. The bergamot aroma should bloom on contact with heat — inhale before first sip.
---
Garnish: Lavender sprig (rested on the foam, not submerged); or dried cornflower; dash of vanilla powder
Temperature: Serve at 65°C; London Fogs cool quickly in tall glass — pre-warm if possible

""",

9930: """RECIPE — Raspberry-Shrub Vinegar Mocktail
Yield: 1 cocktail | Glassware: Nick & Nora or coupe | Ice: None (shaken, strained)
---
25ml raspberry-apple cider vinegar shrub (see below)
20ml fresh lemon juice
10ml simple syrup (adjust — shrub adds sweetness)
60ml cold still water or sparkling water
3 drops saline solution (4:1)
SHRUB: 200g raspberries + 200g sugar (macerate 48h) + 150ml ACV; strain and bottle
---
1. Combine shrub, lemon juice, syrup, water, and saline in shaker with ice.
2. Shake hard 12 seconds — this is a 'shaken and served up' mocktail, needs full aeration.
3. Double-strain into chilled coupe through cocktail strainer and fine sieve.
4. Taste in the glass — acid-forward with raspberry fruit and vinegar tang.
---
Garnish: Dehydrated raspberry on the rim; expressed lemon twist (discard); optional rosebud floated
Temperature: Serve at 5–7°C in a pre-chilled glass

""",

9936: """RECIPE — Ginger-Turmeric Wellness Shot
Yield: 60ml (1 shot) | Glassware: Shot glass or 60ml ceramic cup | Ice: None
---
40g fresh ginger root, peeled
20g fresh turmeric root, peeled (or 1 tsp ground)
1 lemon, peeled
1 small orange, peeled
Pinch of black pepper (essential for curcumin absorption)
Optional: ½ tsp raw honey to balance
---
1. Press ginger, turmeric, lemon, and orange through cold-press masticating juicer.
2. If using centrifugal juicer, strain through fine cloth to remove fibres.
3. Add black pepper. Shake or stir vigorously.
4. Taste: fiery, citric, earthy. Not sweet — the hit is the medicine.
5. For batch prep: double recipe, bottle, refrigerate. Consume within 3 days.
---
Garnish: No garnish (shot format); if presented in a ceramic cup, a single dried rose petal on the tray
Temperature: Room temperature or slightly cool (12–15°C); cold numbs the ginger burn

""",

9937: """RECIPE — NA Aperitivo Pairing Flight (3-Drink Format)
Yield: 3 × 90ml serves | Glassware: 3 small wine glasses or tasting glasses | Ice: Varied
---
GLASS 1 — Before Starter: 90ml Lyre's Italian Orange + 90ml Fever-Tree Refreshingly Light Tonic + ice
GLASS 2 — With Main: 90ml Seedlip Spice 94 + 90ml Fever-Tree Ginger Beer + lime squeeze + ice
GLASS 3 — After/Digestif: 80ml NA chamomile cordial + 80ml still water + 3 drops lavender bitters, no ice
---
1. Prepare each glass separately at the appropriate course transition.
2. Glass 1: pour tonic first, then Lyre's — bitterness opens appetite.
3. Glass 2: Seedlip + ginger complements roasted or spiced protein mains.
4. Glass 3: chamomile and lavender calms digestion — serve room temperature, not chilled.
5. Present flight on a small wooden board with tasting cards if available.
---
Garnish: Glass 1 — orange wheel; Glass 2 — lime wedge + crystallised ginger; Glass 3 — lavender sprig
Temperature: G1: 4°C, G2: 4°C, G3: room temperature (18–20°C)

""",

9938: """RECIPE — Passion Fruit and Mango Tropical Juice Blend
Yield: 300ml (1 large serve) | Glassware: Tall glass | Ice: Cubed
---
2 ripe passion fruits (scooped pulp and seeds)
1 ripe mango (approx. 180g flesh, or 120ml pure mango juice)
Juice of 1 lime (25ml)
50ml coconut water (optional, for tropical hydration)
1 tsp agave nectar (if mango is underripe)
---
1. Blend mango flesh with coconut water until completely smooth. Strain if fibrous.
2. Combine mango blend, lime juice, and agave in a jug.
3. Add passion fruit pulp and seeds — do not blend passion fruit (seeds add texture and visual drama).
4. Stir and taste. Adjust lime or agave.
5. Fill glass with ice. Pour blend over ice. Stir once from the base.
---
Garnish: Passion fruit shell half on the rim; dehydrated mango slice; lime wheel
Temperature: 4–6°C; use frozen mango for a slushie-style variant

""",

9939: """RECIPE — Hibiscus Craft Sparkling (Artisan Soft Drink)
Yield: 1 litre syrup (10 serves) + serve method | Glassware: Highball | Ice: Cubed
---
HIBISCUS SYRUP:
30g dried hibiscus flowers (Jamaica)
300g white sugar
500ml water
Juice of 1 lime
---
SERVE (per glass):
30ml hibiscus syrup
150ml cold sparkling water (Fever-Tree Refreshingly Light or Perrier)
---
1. Combine hibiscus, sugar, water in saucepan. Bring to boil, reduce 5 minutes.
2. Remove from heat. Steep 20 minutes. Strain through fine sieve. Add lime juice.
3. Cool and bottle. Refrigerate up to 3 weeks.
4. To serve: fill highball with ice. Add 30ml syrup. Pour sparkling water slowly.
5. Watch the deep crimson bloom through the ice — do not stir immediately.
---
Garnish: Dried hibiscus flower floated; lime wheel; mint sprig
Temperature: 4–6°C; vivid red colour is the visual signature

""",

9940: """RECIPE — Soursop (Guanabana) Agua Fresca
Yield: 1 litre (4 serves) | Glassware: Tall glass | Ice: Cubed
---
400g fresh or frozen soursop pulp (guanabana — seeds removed)
600ml cold water
Juice of 1 lime (25ml)
2–3 tbsp agave nectar or cane sugar (to taste)
Pinch of sea salt
Optional: 2 drops vanilla extract or ¼ tsp ground nutmeg
---
1. Blend soursop pulp with 200ml water until smooth (high-speed, 60 seconds).
2. Strain through fine-mesh sieve, pressing pulp gently. Remove fibres and seeds.
3. Add remaining water, lime juice, sweetener, and salt to strained juice. Stir well.
4. Taste: soursop is naturally creamy-sweet with a citric edge. Should be balanced.
5. Refrigerate until cold. Serve over ice in tall glasses.
---
Garnish: Lime wheel; fresh mint sprig; pinch of nutmeg grated over the top
Temperature: 4–6°C; soursop can be made the day before — flavour improves overnight

""",

9999: """RECIPE — Green Power Smoothie
Yield: 400ml (1 large serve) | Glassware: Wide-mouth mason jar or tall glass | Ice: None (frozen fruit used)
---
100g frozen spinach (or 2 large handfuls fresh)
1 frozen banana (cut into coins, freeze overnight)
120g frozen mango chunks
1 tbsp almond butter (or 2 tbsp hemp seeds for protein)
250ml cold unsweetened almond milk or oat milk
1 tsp spirulina or 1 scoop unflavoured greens powder (optional)
Juice of ½ lime
---
1. Add liquid to blender first — prevents blade cavitation.
2. Add all solids: frozen spinach, banana, mango, almond butter, spirulina.
3. Blend on high 60 seconds until completely smooth. Stop and scrape walls if needed.
4. Add lime juice. Blend 5 more seconds. Taste — adjust with honey or extra lime.
5. Pour immediately. Smoothies oxidise quickly — serve within 5 minutes.
---
Garnish: Hemp seeds and chia seeds scattered on top; banana slice; spirulina dust (vibrant green)
Temperature: Serve cold (5–8°C); frozen fruit maintains temperature better than adding ice

""",

10000: """RECIPE — Mango Lassi (Sweet) + Salted Lassi
Yield: 1 serve (300ml) | Glassware: Tall glass or traditional copper tumbler | Ice: Optional
---
MANGO LASSI:
200ml full-fat plain yoghurt (Yeo Valley or Chobani)
100ml whole milk
100g Alphonso mango pulp (canned Kesar or fresh ripe mango)
1 tbsp honey or white sugar
Pinch of cardamom
Pinch of saffron in 1 tbsp warm milk (optional, for premium)

SALTED LASSI:
200ml plain yoghurt, 150ml cold water, ½ tsp cumin (toasted, ground), pinch of sea salt, 5 mint leaves
---
MANGO: Blend all ingredients 30 seconds until smooth. Taste: sweet, tangy, fruity. Serve over ice or chilled.
SALTED: Blend yoghurt and water 20 seconds. Add cumin, salt, mint. Blend 10 more seconds. Serve cold.
---
Garnish: Mango Lassi — pinch of cardamom, saffron strand, pistachio sliver. Salted Lassi — fresh mint sprig, pinch of ground cumin.
Temperature: 4–6°C; copper tumblers keep lassi cold through service

""",

10001: """RECIPE — Mexican Horchata (Rice and Cinnamon)
Yield: 1 litre (4 serves) | Glassware: Tall glass | Ice: Cubed
---
200g long-grain white rice (uncooked, rinsed)
1 litre cold water, divided (500ml for soaking, 500ml for blending)
1 cinnamon stick (Mexican canela — softer than Ceylon)
100ml sweetened condensed milk OR 50g cane sugar
1 tsp pure vanilla extract
Optional: 100ml whole milk for creamier version
---
1. Soak rice and cinnamon stick in 500ml cold water for minimum 4 hours, ideally overnight.
2. Remove cinnamon. Blend rice and soaking water at high speed 2 minutes until very fine.
3. Strain through nut milk bag or layered cheesecloth. Squeeze out all liquid.
4. Add remaining 500ml water, condensed milk (or sugar), and vanilla. Stir.
5. Taste and adjust sweetness. Chill. Stir well before each pour.
---
Garnish: Cinnamon stick in glass; ground cinnamon dusted over; vanilla pod split on the rim
Temperature: 4–6°C; horchata separates naturally — always stir before serving

""",

10002: """RECIPE — Persian Sharbat-e-Sekanjabin (Vinegar-Mint Syrup Drink)
Yield: 500ml syrup (8–10 serves) | Glassware: Crystal tumbler | Ice: Cubed
---
SEKANJABIN SYRUP:
300g white sugar
200ml water
100ml white wine vinegar or apple cider vinegar
Large handful fresh mint leaves (approx. 20g)
---
SERVE (per glass):
20ml sekanjabin syrup
200ml cold still or sparkling water
---
1. Combine sugar and water in saucepan. Bring to boil, stir until dissolved.
2. Add vinegar. Simmer 10 minutes until slightly thickened.
3. Remove from heat. Add mint leaves. Steep 20 minutes.
4. Strain. Cool and bottle. Refrigerate up to 3 months.
5. To serve: add syrup to iced glass. Top with cold water. Stir gently.
---
Garnish: Fresh mint sprig; thin cucumber slices fanned in the glass (traditional pairing)
Temperature: 4–6°C; sekanjabin is also traditionally served with romaine lettuce leaves for dipping

""",

10003: """RECIPE — Turkish Ayran (Yoghurt Drink)
Yield: 1 serve (300ml) | Glassware: Tall glass or traditional copper cup | Ice: Cubed
---
150ml full-fat plain yoghurt (Turkish-style, strained — Fage 5% works well)
150ml cold filtered water (or sparkling water for effervescent version)
Pinch of sea salt (½ tsp for traditional savoury version)
Optional: dried mint (pinch for garnish)
---
1. Place yoghurt in tall glass or blender cup.
2. Add cold water gradually while whisking or blending at low speed.
3. Add salt. Blend or whisk 30 seconds until smooth and frothy.
4. For the traditional frothy top: pour from height into the serving glass.
5. The foam is a sign of quality — a flat ayran was poorly made.
---
Garnish: Pinch of dried mint floated on the foam; nothing else needed
Temperature: 2–4°C; ayran should be very cold — practically refrigerator temperature when served

""",

10019: """RECIPE — Vietnamese Sinh Tố Bơ (Avocado Smoothie)
Yield: 300ml (1 serve) | Glassware: Tall glass | Ice: Crushed
---
1 ripe Hass avocado (180g flesh)
150ml sweetened condensed milk (or 100ml coconut milk + 1 tbsp honey)
100ml cold whole milk or coconut milk
1 tsp vanilla extract
Pinch of sea salt
Crushed ice (to fill glass)
---
1. Halve and pit avocado. Scoop flesh into blender.
2. Add condensed milk, milk, vanilla, and salt.
3. Blend 45 seconds until completely smooth. Taste: rich, creamy, not too sweet.
4. Add 4–5 ice cubes. Blend 10 seconds more for a cold, slushy texture.
5. Pour into glass packed with crushed ice. Drink immediately — avocado oxidises.
---
Garnish: Drizzle of condensed milk swirled on top; single pandan leaf laid across the glass (traditional)
Temperature: 2–4°C; serve immediately to prevent browning

""",

10020: """RECIPE — Korean Sikhye (Sweet Rice Punch)
Yield: 1.5 litres (6 serves) | Glassware: Small stone bowl (dolsot) or ceramic cup | Ice: Optional
---
100g short-grain white rice (cooked, then rinsed cold — some grains should stay whole)
1 litre water
50g malt barley powder (yeotgireum — from Korean grocery)
50–80g white sugar or rice syrup (to taste)
Optional: 5 dried jujubes, 5 pine nuts for serving
---
1. Mix malt powder with 500ml warm water (55°C). Let settle 20 minutes. Strain — use liquid only.
2. Combine malt water with cooked rice in thermos or pot. Keep at 55–60°C for 4–5 hours.
3. Rice grains will float to the surface when fermentation is complete.
4. Skim floating rice grains — set aside for serving garnish.
5. Bring liquid to boil 3 minutes (stops fermentation). Add sugar/syrup. Skim foam.
6. Cool and refrigerate. Serve cold with floating rice grains and pine nuts.
---
Garnish: 3–4 cooked rice grains floated; 3 pine nuts; red jujube slice; fresh ginger coin
Temperature: 4–6°C; sikhye is naturally lightly sweet and malt-flavoured

""",

10021: """RECIPE — Butterfly Pea Flower Lemonade (Colour-Changing)
Yield: 1 serve | Glassware: Clear tall glass | Ice: Cubed
---
BUTTERFLY PEA FLOWER TEA (base):
15g dried butterfly pea flowers + 300ml boiling water → steep 5 min → strain → cool
---
PER SERVE:
150ml chilled butterfly pea flower tea (deep blue-purple)
20ml fresh lemon juice (served separately in a small jug or squeezed tableside)
10ml simple syrup (1:1 sugar:water)
---
1. Make butterfly pea flower tea and cool completely in fridge. The colour is deep indigo-blue.
2. Fill glass with ice. Pour blue tea over ice.
3. Add simple syrup. Stir to dissolve — tea remains blue.
4. TABLESIDE EFFECT: pour or squeeze lemon juice over the back of a spoon slowly.
5. Watch the drink shift from blue → purple → pink as acidity raises the pH. Do not stir — let the gradient form.
---
Garnish: Lemon wheel; edible flowers; mint sprig
Temperature: 4–6°C; perform the colour change tableside for maximum drama

""",

10022: """RECIPE — Beet-Carrot-Ginger Cold Press (Performance Juice)
Yield: 250ml (1 serve) | Glassware: Short glass or 250ml bottle | Ice: None
---
150g raw beetroot, scrubbed, unpeeled (or peeled for less earthiness)
2 medium carrots (approx. 200g)
20g fresh ginger, peeled
1 lemon, peeled
1 small apple (Granny Smith, for sweetness and body)
---
1. Wash all produce thoroughly. Beetroot stains — work on a board.
2. Cut to fit juicer chute. Process: carrot → beetroot → apple → ginger → lemon.
3. Stir the pressed juice immediately — layers separate quickly.
4. Taste: earthy, sweet, fiery from ginger, bright from lemon.
5. Consume within 20 minutes of pressing for maximum nitrate content.
---
Garnish: Thin beetroot chip on the rim of the glass; sprig of flat-leaf parsley (optional)
Temperature: 8–12°C; do not serve ice-cold — nitrate compounds work better at mild temperature. Drink before training, not after.

""",

10023: """RECIPE — Dandelion Root Latte
Yield: 1 serve (250ml) | Glassware: Ceramic mug | Ice: None
---
1 tbsp roasted dandelion root powder (Dandy Blend or homemade roasted root)
OR 1 dandelion root tea bag (Pukka or Traditional Medicinals)
200ml oat milk or whole milk
50ml hot water at 95°C
1 tsp raw honey or maple syrup
¼ tsp cinnamon
Pinch of vanilla
---
1. Steep dandelion root in 50ml hot water for 5 minutes. Strain or remove bag.
2. Steam oat milk to 65°C — light microfoam.
3. Combine dandelion concentrate and honey in mug. Stir.
4. Pour steamed milk over — add cinnamon and vanilla.
5. Froth surface lightly with milk wand if available.
---
Garnish: Cinnamon dust; dandelion flower (if seasonal and untreated); star anise floated
Temperature: Serve at 65°C; dandelion is mellow and coffee-adjacent — works well as a morning decaf alternative

""",

10044: """RECIPE — Beetroot Latte (Earth and Sweet)
Yield: 1 serve | Glassware: Ceramic handle-free cup or flat white glass | Ice: None
---
1 tsp beetroot powder (food-grade, cold-dried; Deep Purple or raw beet juice concentrate)
1 tsp maple syrup or honey
¼ tsp ground ginger
Pinch of cinnamon
200ml oat milk or coconut milk (Oatly Barista for best froth)
30ml hot water at 85°C
---
1. Combine beetroot powder, maple syrup, ginger, cinnamon in a small cup.
2. Add 30ml hot water. Whisk into a smooth paste — no lumps.
3. Steam oat milk to 60–65°C — light, glossy microfoam.
4. Pour beetroot paste into serving cup. Pour steamed milk over.
5. The vivid fuchsia-red colour should bloom through the milk — pour slowly for gradient effect.
---
Garnish: Fine beetroot powder through a sieve; edible gold flake for premium service; dried rose petal
Temperature: Serve at 60–65°C; the colour fades above 75°C — do not overheat

""",

10045: """RECIPE — NA Aperitivo Serve (Spirit-Free Pre-Dinner)
Yield: 1 serve | Glassware: Large wine glass | Ice: Cubed (generous)
---
60ml Crodino Aperitivo (non-alcoholic, ready-to-drink bitter orange aperitivo)
OR 40ml Wilderton Aperitivo (NA) + 30ml Fever-Tree Soda Water
100ml Fever-Tree Mediterranean Tonic Water
Squeeze of blood orange or regular orange (20ml)
---
1. Fill wine glass to the brim with good ice — this is non-negotiable for aperitivo service.
2. Add Crodino (or NA aperitivo spirit) over the ice.
3. Add orange juice. Do not stir yet.
4. Top slowly with tonic water — pour down the inside rim.
5. Stir once with bar spoon, lifting from bottom to integrate without losing carbonation.
---
Garnish: Large orange wheel inside the glass; rosemary sprig (lightly slapped to release oils); green olive on a pick
Temperature: 4–6°C; ice volume is critical — use at least 4–5 cubes in a large glass

""",

10046: """RECIPE — NA Digestif: Chamomile and Gentian Bitters Sipper
Yield: 1 serve | Glassware: Small Riedel spirit glass or Nick & Nora | Ice: None
---
100ml chamomile tea (Twinings Pure Camomile, 1 bag, 5 min steep, cooled)
15ml honey syrup (2:1 honey:water)
5ml apple cider vinegar (adds digestive bitterness)
3 dashes Angostura bitters (aromatic; technically 45% ABV but used in drops)
Optional: 3 drops lavender extract
---
1. Brew chamomile tea. Cool to room temperature.
2. Combine tea, honey syrup, apple cider vinegar, and bitters in mixing glass.
3. Stir gently over ice to chill. Do not dilute heavily — this is a sipping digestif.
4. Strain into a small spirit glass. No ice — served neat, room temperature to slightly cool.
5. Serve with a palate cleanser: 2 chocolate-covered mint pastilles or a lavender shortbread.
---
Garnish: Chamomile flower (fresh or dried) floated; expressed lemon peel (very fine — oils only)
Temperature: 16–18°C — slightly cool room temperature; do not serve ice cold

""",

10047: """RECIPE — Water Kefir (Probiotic Sparkling Drink)
Yield: 1 litre per batch | Glassware: Highball or jar | Ice: Cubed
---
1 litre filtered water (chlorine-free — let tap water sit 30 min to off-gas, or use bottled)
60g white sugar (cane sugar — feeds the grains, not honey which is antibacterial)
3 tbsp live water kefir grains (Cultures for Health)
2 dried figs or dates (for minerals and trace elements)
Optional 2F: 200ml juice of choice for secondary fermentation flavour
---
1. Dissolve sugar in 200ml warm water. Cool to room temperature.
2. Combine sugar water, remaining water, figs, and kefir grains in jar.
3. Cover with cloth. Ferment 24–48 hours at 20–24°C. Taste from 36 hours.
4. When pleasantly fizzy and lightly sweet, strain — reserve grains for next batch.
5. SECOND FERMENTATION (optional): Add juice, seal in swing-top bottle. Leave 12–24 hours for carbonation.
---
Garnish: Lime wedge; mint sprig; sliced fruit if second ferment flavour was used
Temperature: 4–6°C; swing-top bottles should be opened slowly over a sink

""",

10048: """RECIPE — NA Sommelier's Pairing Cocktail (Framework Drink)
Yield: 1 serve | Glassware: Wine glass | Ice: None
---
80ml Seedlip Garden 108 (herbal, pea-forward; pairs with spring/summer dishes)
30ml Verjuice (pressed unfermented grape juice — acidic, grape-like)
10ml elderflower cordial (Belvoir)
80ml sparkling water (chilled)
---
1. Combine Seedlip, verjuice, and elderflower cordial in a jug with ice. Stir 10 rotations.
2. Strain into wine glass (no ice in glass — for focused flavour perception).
3. Top with sparkling water. Do not stir.
4. This combination mimics white wine acidity and aromatics — designed to pair with white fish, light pasta, and soft goat cheese courses.
---
Garnish: Cucumber ribbon inside the glass; dill frond; thin green apple slice
Temperature: 8–10°C — same as white wine service for pairing efficacy

""",

10087: """RECIPE — Oat Milk Flat White (Barista Precision Method)
Yield: 1 serve | Glassware: 5oz/150ml ceramic tulip cup | Ice: None
---
18g finely ground espresso blend (Ozone Coffee Ritual Blend or similar; 1:2 ratio)
36ml double ristretto pull (shorter, more concentrated than espresso)
120ml Oatly Barista oat milk (dedicated barista formula — does not split under heat)
---
1. Purge group head and insert portafilter with 18g freshly ground coffee.
2. Pull ristretto: target 36ml in 25–30 seconds. Discard first and last drops.
3. Steam oat milk: texture to silky microfoam (not stiff). Target 60–65°C max.
4. Tap jug on counter, swirl to integrate. Oat milk separates faster than dairy.
5. Pour milk immediately into ristretto — draw latte art. Flat white: tulip or rosette, small and defined.
---
Garnish: Latte art is the garnish. Dust of Valrhona cocoa acceptable if requested.
Temperature: Serve at 60–65°C; flat whites cool fast in 150ml cups — deliver immediately

""",

10088: """RECIPE — Water Kefir Tepache Hybrid (Fermented Fruit Soda)
Yield: 1.5 litres | Glassware: Highball | Ice: Cubed
---
Peel and core of 1 ripe pineapple (washed)
1 litre filtered water
80g raw cane sugar or piloncillo
2 tbsp live water kefir grains (adds probiotic cultures to tepache base)
1 cinnamon stick, 3 cloves
---
1. Dissolve sugar in 200ml warm water. Cool completely.
2. Combine pineapple peel, core, spices, kefir grains, and sugar water in large glass jar.
3. Top with remaining water. Cover loosely. Ferment 24–48 hours at 22°C.
4. Taste from 30 hours — kefir grains accelerate fermentation vs. wild yeast tepache alone.
5. Strain. Bottle in swing-top bottles. Second ferment 12–18 hours for carbonation.
---
Garnish: Pineapple wedge, Tajín rim, lime squeeze
Temperature: 4°C refrigerated; second ferment bottles under pressure — open slowly over sink

""",

10089: """RECIPE — Children's Mocktail: The Sunset (Inclusive Menu)
Yield: 1 serve | Glassware: Colourful highball or novelty glass | Ice: Crushed
---
120ml fresh orange juice (Valencia, no pulp for children)
15ml grenadine (Monin or Teisseire — pomegranate syrup)
90ml lemon-lime soda (San Pellegrino Limonata or Sprite)
OPTIONAL FLOAT: 30ml cream soda on top for a cream-cloud effect
---
1. Fill glass with crushed ice — visual impression matters for children.
2. Pour orange juice over ice.
3. Pour soda gently — it should fizz and interact with the OJ.
4. Pour grenadine slowly down the inside of the glass with a bar spoon.
5. Grenadine sinks to the bottom creating the red-orange-yellow 'sunset'. Serve immediately.
---
Garnish: Paper umbrella; orange butterfly (2 half-slices wings + cherry body on a pick); rainbow sugar rim
Temperature: 2–4°C; serve with a paper or bamboo straw

""",

10090: """RECIPE — Tamarind Agua Fresca (Tamarindo)
Yield: 1 litre (4 serves) | Glassware: Tall glass | Ice: Cubed
---
100g tamarind paste (seedless block — Tamicon or similar; or fresh tamarind pods)
800ml warm water (for dissolving) + 200ml cold water
3 tbsp raw cane sugar or piloncillo
Juice of 1 lime (25ml)
Pinch of sea salt
Optional: pinch of cayenne or Tajín
---
1. Break tamarind block into chunks. Dissolve in 300ml warm water — mash with hands or spoon.
2. Strain through fine sieve, pressing solids. Discard fibrous pulp and seeds.
3. Combine tamarind liquid with remaining water, sugar, lime juice, and salt. Stir well.
4. Taste: tart, complex, faintly sweet. Adjust with sugar or lime.
5. Chill. Serve over ice.
---
Garnish: Lime wedge; Tajín rim (chilli-salt-lime); chilli-dusted tamarind candy on a stick (traditional Mexican style)
Temperature: 4–6°C

""",

10091: """RECIPE — NA Wine Service and Pairing (Dealcoholised Deep Dive)
Yield: 1 serve (125ml) | Glassware: Riedel Vinum Chardonnay glass | Ice: None
---
125ml Leitz Eins Zwei Zero Chardonnay (0.0%, Germany)
OR Torres Natureo Muscat (0.5%, Spain — stone fruit, floral)
OR Château del Ryse NA Bordeaux Rouge (0.0%, tannin-present)
---
SERVICE PROTOCOL:
1. Decant NA reds 10–15 minutes. NA whites need no decanting.
2. Serve NA whites at 8–10°C (same as still white wine). NA reds at 16°C.
3. Pour 125ml against the inside of the glass; tilt at 45° for a clean stream.
4. Allow 1–2 minutes before nosing — aromatic release is slower without alcohol.
5. PAIRING: Leitz Chardonnay → poached salmon, soft brie, mushroom risotto. Torres Natureo → apricot tart, curry-spiced dishes, soft cheese.
---
Garnish: No garnish in glass. Serve tasting notes card with each glass.
Temperature: Whites 8–10°C; NA reds 16–18°C

""",

10092: """RECIPE — House NA Cocktail (Complete Bar Signature)
Yield: 1 cocktail | Glassware: Coupe or Nick & Nora | Ice: None (stirred, served up)
---
40ml Seedlip Spice 94
20ml Seedlip Garden 108
15ml verjuice (unfermented grape juice — Maggie Beer)
10ml chamomile cordial (or chamomile syrup: 1:1 sugar:strong chamomile tea)
3 dashes Bittered Sling Kensington Bitters (aromatic; NA context acceptable)
---
1. Combine all ingredients in mixing glass. Fill with ice.
2. Stir 45–50 rotations — this drink needs full integration and chill without aeration.
3. Taste in the mixing glass: complex, herbal, slightly acidic, gently bitter.
4. Strain into chilled coupe. Serve immediately.
---
Garnish: Expressed lemon twist laid inside the coupe rim; chamomile flower floated on surface
Temperature: 5–7°C; coupe must be pre-chilled in freezer or filled with ice water

""",

10106: """RECIPE — Dashi as Beverage (Ichiban Dashi)
Yield: 1 litre (4–6 small cups) | Glassware: Small Japanese yunomi cup (handleless) | Ice: None
---
15g konbu (kombu) seaweed (clean, dried; Clearspring or Japanese market)
10g katsuobushi (dried bonito flakes) — for ichiban dashi
1 litre cold filtered water
Pinch of sea salt
Optional: 1 tsp light soy sauce (usukuchi shoyu) for seasoning
---
1. Wipe konbu gently with damp cloth — do not wash (removes glutamates). Place in cold water.
2. Heat slowly to 60°C over medium-low. Remove konbu just before boiling (approx. 60–65°C).
3. Bring to 80–90°C. Add katsuobushi. Remove from heat immediately.
4. Steep 3–4 minutes. Strain through fine cloth — do not squeeze the flakes.
5. Season lightly with salt and/or usukuchi shoyu. Taste: clean, oceanic umami.
---
Garnish: Yuzu zest (or lemon zest) floated; single mitsuba leaf; cracked sea salt crystal
Temperature: Serve at 70–75°C in pre-warmed yunomi cups

""",

10107: """RECIPE — Elderflower Cordial (from scratch)
Yield: 1.5 litres | Glassware: N/A (syrup for mixing) / Collins glass for serving
---
20 fresh elderflower heads (picked morning, August) — or 30g dried elderflowers
1kg white sugar
800ml water
2 unwaxed lemons (zest and juice)
1g citric acid (optional — extends shelf life and adds brightness)
---
1. Shake elderflower heads to remove insects. Do not wash — you'll remove the pollen.
2. Bring sugar and water to boil. Stir to dissolve. Remove from heat.
3. Add elderflowers, lemon zest, lemon juice, and citric acid. Stir.
4. Cover and steep 24–48 hours in fridge. Longer = more floral complexity.
5. Strain through cheesecloth. Bottle. Keeps refrigerated 6 weeks; frozen 1 year.
TO SERVE: 25ml cordial + 150ml sparkling water over ice. Garnish: lemon slice and elderflower sprig.
---
Garnish: Fresh or dried elderflower sprig; lemon wheel; cucumber slice
Temperature: Cordial at 4°C; serve mixed drink at 4–6°C

""",

10108: """RECIPE — 3-Juice Cleanse Protocol (Juice 1, 2, 3)
Yield: 3 × 250ml serves | Glassware: 250ml amber glass bottles or tall glasses | Ice: None
---
JUICE 1 — Morning (Alkalising):
150g cucumber + 100g celery + 80g green apple + 20g ginger + 1 lemon → cold press

JUICE 2 — Midday (Energising):
2 carrots + 1 large beetroot + 1 orange + 20g turmeric + 10g ginger → cold press

JUICE 3 — Afternoon (Calming):
200g watermelon + 1 lime + 5g fresh mint + pinch of sea salt → blend and strain
---
1. Prepare all three juices using cold-press masticating juicer for maximum enzyme preservation.
2. Bottle in amber glass to protect from UV oxidation.
3. Consume in sequence across the day: Juice 1 on empty stomach, Juice 2 at noon, Juice 3 at 3pm.
4. Keep refrigerated at 4°C. Consume within 4 hours of pressing.
---
Garnish: Label each bottle clearly. Present on a wooden board for programme service.
Temperature: 8–10°C for Juices 1 and 3; Juice 2 (beetroot) at 12°C

""",

10109: """RECIPE — Carob Hot Drink (Mediterranean Tradition)
Yield: 1 serve | Glassware: Ceramic mug | Ice: None
---
2 tbsp roasted carob powder (St. John's Bread; Organic Traditions)
200ml oat milk or whole milk
1 tsp raw honey or date syrup
¼ tsp cinnamon
Pinch of vanilla powder
Optional: pinch of ground cardamom or nutmeg
---
1. Combine carob powder and spices in mug. Add 2 tbsp cold milk — make a smooth paste.
2. Heat remaining milk to 70°C in saucepan, whisking to froth lightly.
3. Pour hot milk over carob paste, stirring vigorously as you pour.
4. Add honey. Stir until fully integrated. Taste: sweet, malty, chocolate-adjacent, naturally caffeine-free.
5. Froth with hand whisk or milk frother for 20 seconds before serving.
---
Garnish: Cinnamon dust; carob pod half on saucer; a single dried date on the side
Temperature: Serve at 65–68°C; carob is naturally sweet — avoid over-sweetening

""",

}

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    errors = 0
    for entry_id, recipe in RECIPES.items():
        try:
            cur.execute(
                "UPDATE technique_references SET pro_tips = %s || pro_tips WHERE id = %s",
                (recipe, entry_id)
            )
        except Exception as e:
            print(f"ERROR on id={entry_id}: {e}")
            errors += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"Done. {len(RECIPES) - errors} NA recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
