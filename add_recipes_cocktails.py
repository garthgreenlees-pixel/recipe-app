#!/usr/bin/env python3
"""Add structured recipes to all 75 Provenance 500 Cocktail entries."""

import psycopg2

DB_WRITE = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

RECIPES = {
    8741: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
30ml (1oz) London dry gin — Tanqueray No. Ten or Beefeater
30ml (1oz) Campari
30ml (1oz) sweet vermouth — Carpano Antica Formula or Cocchi di Torino
---
1. Combine gin, Campari, and sweet vermouth in a mixing glass over ice
2. Stir with a bar spoon for 30 seconds (approximately 40 rotations) — dilution is the third ingredient
3. Strain over a single large ice cube into a rocks glass
4. Express an orange peel over the surface by holding it skin-side down and squeezing firmly to spray the oils
5. Run the peel around the rim, then place it in the drink
---
Garnish: Orange peel (expressed)
Temperature: Serve immediately — this drink softens as the ice dilutes it

""",

    8742: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) bourbon — Buffalo Trace, Woodford Reserve, or Maker's Mark
5ml (1 barspoon) simple syrup (1:1) or 1 sugar cube
2 dashes Angostura bitters
1 dash orange bitters — Regan's No. 6 (recommended)
---
1. If using sugar cube: muddle it with both bitters and a dash of water in the mixing glass until dissolved
2. Add bourbon and ice, stir for 20-25 seconds — dilution without water-logging
3. Strain into a rocks glass over a single large ice cube (or build directly in the glass)
4. Express an orange peel over the surface, run around the rim, garnish
---
Garnish: Orange peel (expressed) + optional Luxardo cherry on a pick
Temperature: Room-temperature ice from the stir — not over-chilled

""",

    8743: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass or chilled coupe | Ice: Cubed (rocks) or none (up)
---
60ml (2oz) blanco tequila — Tapatio, Olmeca Altos, or El Tesoro
30ml (1oz) fresh lime juice — always fresh, never bottled
22.5ml (¾oz) Cointreau
Optional: half salt rim — kosher salt on outer half only
---
1. Run a lime wedge around the outer half of the rim, dip in coarse kosher salt
2. Combine tequila, lime juice, and Cointreau in a shaker with ice
3. Shake hard for 12-15 seconds until the shaker is frosted
4. Strain over fresh ice (rocks) or double-strain into chilled coupe
5. Taste before serving — lime brightness and sweetness should be balanced
---
Garnish: Lime wheel or wedge on the rim
Temperature: Serve immediately — citrus cocktails are time-sensitive

""",

    8744: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled martini glass or coupe | Ice: None (stirred then strained)
---
75ml (2½oz) London dry gin — Tanqueray No. Ten, Beefeater, or The Botanist
15ml (½oz) dry vermouth — Noilly Prat or Dolin Dry (fresh bottle, refrigerated)
---
1. Chill the glass with ice water or in the freezer for 10 minutes
2. Combine gin and vermouth in a mixing glass packed with ice
3. Stir for 45-50 seconds — this drink does not benefit from speed
4. Strain into the chilled, dry glass
5. Express a lemon peel over the surface — the spray of oils is visible; discard or rest on rim
---
Garnish: Expressed lemon peel or three quality olives on a pick
Temperature: The glass must fog when the drink enters — ice-cold is non-negotiable
Note: The drier the martini (less vermouth), the more critical the gin quality becomes

""",

    8745: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe or nick & nora | Ice: None (stirred then strained)
---
60ml (2oz) rye whiskey — Rittenhouse, Sazerac, or Wild Turkey 101
30ml (1oz) sweet vermouth — Carpano Antica Formula, Cocchi di Torino, or Dolin Rouge
2 dashes Angostura bitters
1 dash orange bitters — Regan's No. 6 or Angostura Orange
---
1. Chill the glass with ice water while preparing
2. Combine rye, vermouth, and both bitters in a mixing glass over ice
3. Stir for 30-35 seconds — the Manhattan benefits from thorough chilling and dilution
4. Strain into the chilled, dry glass
5. Garnish with a Luxardo maraschino cherry — never red-dyed cocktail cherries
---
Garnish: Luxardo maraschino cherry (or two on a pick)
Temperature: Serve immediately — warm hands degrade this drink fast

""",

    8788: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) white Cuban-style rum — Havana Club 3, Diplomatico Planas, or Bacardi Superior
22.5ml (¾oz) fresh lime juice — pressed to order, oxidizes within 30 minutes
22.5ml (¾oz) simple syrup (1:1 white sugar to water)
---
1. Chill the coupe with ice water
2. Combine rum, lime juice, and simple syrup in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain through fine mesh into the chilled coupe — removes ice shards
5. Surface should have a faint foam — this is correct
---
Garnish: None (traditionally) or a thin lime wheel rested on the rim
Temperature: The colder the better — this drink dies at room temperature
Note: The 2:¾:¾ ratio (spirit:citrus:sweetener) is the baseline. Adjust lime or syrup in 5ml increments — limes vary in acidity and juice yield

""",

    8789: """RECIPE:
Yield: 1 cocktail | Glassware: Highball or Collins glass | Ice: Crushed
---
60ml (2oz) white Cuban rum — Havana Club 3 or Bacardi Superior
30ml (1oz) fresh lime juice
22.5ml (¾oz) simple syrup (1:1) or 2 tsp white sugar
8-10 fresh spearmint leaves (not peppermint)
60ml (2oz) chilled soda water
---
1. Gently smack mint in your palm to release oils — do not muddle aggressively or the drink turns bitter and brown
2. Place mint in glass, add lime juice and syrup, lightly press 2-3 times with muddler
3. Add rum, stir briefly, fill glass with crushed ice to the top
4. Top with soda water, gently lift from the bottom with a bar spoon once
5. Slap a mint sprig once in your palm before placing — wakes up the aromatics
---
Garnish: Fresh mint sprig (slapped) + lime wheel
Temperature: Serve immediately — this drink wilts fast

""",

    8790: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass or coupe | Ice: Cubed (rocks) or none (up)
---
60ml (2oz) bourbon — Buffalo Trace, Four Roses Small Batch, or Wild Turkey 101
30ml (1oz) fresh lemon juice
22.5ml (¾oz) simple syrup (1:1)
1 egg white (traditional — creates silky texture and foam layer)
2 dashes Angostura bitters (for foam garnish)
---
1. With egg white: dry shake all ingredients (no ice) for 15 seconds to emulsify the white
2. Add ice, shake hard for 12-15 seconds
3. Strain into rocks glass over fresh ice, or double-strain into chilled coupe
4. Float 2 dashes Angostura bitters on the foam — drag a toothpick through for a pattern
---
Garnish: Orange half-wheel + Luxardo cherry on a pick
Temperature: Cold — the egg white foam should be stiff, not runny

""",

    8791: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) vodka — Ketel One, Grey Goose, or Belvedere
30ml (1oz) fresh espresso — pulled to order, cooled 30-60 seconds
15ml (½oz) Kahlua (or Tia Maria for less sweetness)
10ml (⅓oz) simple syrup — optional, taste first (espresso sweetness varies)
---
1. Pull a single or double espresso and allow to cool briefly — hot espresso creates steam, not foam
2. Combine vodka, espresso, Kahlua, and optional syrup in a shaker with ice
3. Shake very hard for 15-20 seconds — vigorous agitation creates the signature foam
4. Double-strain into a chilled coupe
5. Three coffee beans should float on the foam — this is the test of a good shake
---
Garnish: Three whole espresso beans floated on the foam
Temperature: Serve immediately — the foam dissipates within 2-3 minutes
Note: Use freshly pulled espresso only. Cold brew is a different drink. The crema from the espresso is what creates the foam — stale espresso or concentrate produces a flat surface

""",

    8792: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled cocktail (martini) glass | Ice: None (shaken then strained)
---
45ml (1½oz) citrus vodka — Absolut Citron or Ketel One Citroen
15ml (½oz) Cointreau
30ml (1oz) fresh cranberry juice — 100% juice, not cocktail. Dilute 1:4 with water if too thick
15ml (½oz) fresh lime juice
---
1. Chill the cocktail glass with ice water
2. Combine all ingredients in a shaker with ice
3. Shake hard for 12-15 seconds — the drink should turn pale blush pink, not red
4. Strain into the chilled glass
5. Express an orange peel over the surface — the oils cut the sweetness
---
Garnish: Expressed orange peel (flaming optional for theatre)
Temperature: Ice-cold — pale pink is correct, deep red means too much cranberry

""",

    8829: """RECIPE:
Yield: 1 cocktail | Glassware: Copper mule mug or highball | Ice: Cubed
---
60ml (2oz) vodka — Ketel One or Belvedere
15ml (½oz) fresh lime juice
120ml (4oz) ginger beer — Fever-Tree or Q Mixers (not ginger ale — different product)
---
1. Fill the copper mug (or highball glass) with ice
2. Pour vodka over the ice
3. Add fresh lime juice
4. Top with ginger beer, pouring down the side to preserve carbonation
5. Stir once gently from the bottom with a long bar spoon
---
Garnish: Lime wedge squeezed and dropped in + fresh mint sprig
Temperature: The copper mug conducts cold — serve immediately and it stays cold longer
Note: Quality ginger beer is the variable that makes or breaks this drink. The copper mug is functional, not just decorative

""",

    8830: """RECIPE:
Yield: 1 cocktail | Glassware: Double rocks glass or tiki mug | Ice: Crushed
---
30ml (1oz) aged Jamaican rum — Appleton Estate Signature or Smith & Cross
30ml (1oz) aged rhum agricole — Clement VSOP or Rhum J.M V.O.
22.5ml (¾oz) fresh lime juice
15ml (½oz) orange curacao — Pierre Ferrand Dry Curacao or Cointreau
7.5ml (¼oz) orgeat — Giffard, BG Reynolds, or house-made almond syrup
---
1. Combine all ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Strain over crushed ice in a double rocks glass or tiki mug
4. Float dark rum (Gosling's or Myers's) over the top — pour slowly over a bar spoon
5. Insert a mint sprig through a spent lime shell half
---
Garnish: Spent lime shell, mint sprig, optional Luxardo cherry on a pick
Temperature: Serve immediately over crushed ice — refreshing, not boozy
Note: Do not use grenadine — that is not a Mai Tai. Orgeat is non-negotiable. Two-rum combination creates complexity a single rum cannot achieve

""",

    8831: """RECIPE:
Yield: 1 cocktail | Glassware: Poco grande glass or highball | Ice: Blended
---
60ml (2oz) white rum — Havana Club 3 or Bacardi Superior
90ml (3oz) fresh or premium pineapple juice — Dole Gold, not from concentrate
45ml (1½oz) Coco Lopez coconut cream — this brand specifically; the texture differs from alternatives
Optional: 15ml (½oz) aged rum float for complexity
---
1. Combine rum, pineapple juice, and Coco Lopez in a blender with 240ml (1 cup) crushed ice
2. Blend until smooth and frothy — no ice chunks remaining
3. Pour into a chilled poco grande glass
4. Float aged rum over the top if using
---
Garnish: Pineapple wedge + cherry on a pick + toasted coconut flakes
Temperature: Blended and slushy — serve immediately before it separates
Note: Coco Lopez is the original and is texturally superior to coconut milk or cream of coconut substitutes. The ratio of pineapple to coconut is the critical balance

""",

    8832: """RECIPE:
Yield: 1 cocktail | Glassware: Large balloon wine glass | Ice: Large cubes (2-3)
---
90ml (3oz) Prosecco — Treviso DOC, dry (not extra dry)
60ml (2oz) Aperol
30ml (1oz) soda water, chilled
---
1. Fill the balloon glass with 2-3 large ice cubes
2. Pour Prosecco first — prevents Aperol from sinking and staining the ice
3. Add Aperol
4. Top with soda water
5. Stir once gently — the layers partially merge naturally
6. Add an orange slice (not just peel — the flesh and pith are part of the flavour)
---
Garnish: Orange slice (full round slice dropped in)
Temperature: The glass should be cold — pre-chill or serve immediately with ice
Note: The 3-2-1 ratio (Prosecco:Aperol:soda) is the Venetian standard. Cheap Prosecco is detectable — the fizz dies faster and it tastes sharp. Do not use Champagne or Cava.

""",

    8833: """RECIPE:
Yield: 1 cocktail | Glassware: Collins glass | Ice: Cubed
---
60ml (2oz) London dry gin — Tanqueray or Beefeater
30ml (1oz) fresh lemon juice
22.5ml (¾oz) simple syrup (1:1)
75ml (2½oz) chilled soda water
---
1. Combine gin, lemon juice, and simple syrup in a shaker with ice
2. Shake briefly, 8-10 seconds — just to combine and chill, not to dilute heavily
3. Strain into a Collins glass over fresh ice
4. Top with soda water poured gently down the side of the glass
5. Stir once from the bottom to integrate without losing carbonation
---
Garnish: Lemon wheel + Luxardo cherry on a pick
Temperature: Cold and effervescent — the carbonation is half the drink

""",

    8839: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) London dry gin — Hendrick's, Tanqueray, or Plymouth
22.5ml (¾oz) fresh lime juice
22.5ml (¾oz) simple syrup (1:1)
---
1. Chill the coupe with ice water
2. Combine gin, lime juice, and simple syrup in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain into the chilled coupe
---
Garnish: Lime wheel or expressed lime peel
Temperature: Ice-cold — this is a bracingly cold drink
Note: Traditional Gimlet uses Rose's lime cordial (15ml) instead of fresh lime + syrup. The fresh version is more complex; the cordial version is sweeter and nostalgia-driven. Both are valid.

""",

    8840: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe, optional sugared rim | Ice: None (shaken then strained)
---
45ml (1½oz) cognac — Hennessy VS, Remy Martin VSOP, or Courvoisier VSOP
22.5ml (¾oz) Cointreau — original specification, not generic triple sec
22.5ml (¾oz) fresh lemon juice
Optional: superfine sugar for half the outer rim
---
1. If rimming: run a lemon wedge around the outer half rim, dip in superfine sugar
2. Chill the coupe with ice water
3. Combine cognac, Cointreau, and lemon juice in a shaker with ice
4. Shake hard for 12-15 seconds
5. Double-strain into the chilled coupe
---
Garnish: Expressed lemon peel
Temperature: Ice-cold — cognac opens up in cold, not at room temperature
Note: The classic ratio debate: Harry MacElhone's original was equal parts (1:1:1); most modern versions use 2:1:1. Try both — the equal-parts version is more tart and citrus-forward

""",

    8841: """RECIPE:
Yield: 1 cocktail | Glassware: Champagne flute | Ice: None (shaken then topped)
---
30ml (1oz) London dry gin — Tanqueray or Plymouth
15ml (½oz) fresh lemon juice
10ml (⅓oz) simple syrup (1:1)
75ml (2½oz) Champagne or quality Cremant — brut or extra brut
---
1. Chill the flute with ice water or keep in the freezer
2. Combine gin, lemon juice, and simple syrup in a shaker with ice
3. Shake for 10-12 seconds — don't over-dilute; the Champagne will extend the drink
4. Double-strain into the chilled flute
5. Top with Champagne, pouring slowly down the inside of the glass
6. Tilt and swirl once — do not stir
---
Garnish: Expressed lemon peel rested on the rim without touching the liquid — it kills bubbles if dropped in
Temperature: Everything must be cold — warm Champagne creates a flat drink
Note: Cognac version (substituting gin) is historically valid — the Parisian tradition. Gin is the New Orleans standard (Antoine's). Both are correct depending on context.

""",

    8842: """RECIPE:
Yield: 1 cocktail | Glassware: Highball or Collins glass | Ice: Cubed
---
60ml (2oz) blanco tequila — Tapatio, Cimarron, or Olmeca Altos
30ml (1oz) fresh grapefruit juice
15ml (½oz) fresh lime juice
15ml (½oz) agave syrup (2:1 agave nectar to water)
Pinch of salt
120ml (4oz) grapefruit soda — Jarritos or Fever-Tree Pink Grapefruit; or soda water for drier result
---
1. Rim half the glass with salt (lime wedge + kosher salt)
2. Fill the glass with ice
3. Combine tequila, both citrus juices, agave syrup, and salt over the ice
4. Top with grapefruit soda, poured gently down the side
5. Stir once from the bottom
---
Garnish: Grapefruit wedge or half-wheel on the rim
Temperature: Cold — grapefruit bitterness amplifies as it warms

""",

    8843: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Crushed
---
60ml (2oz) cachaca — Leblon, Novo Fogo Silver, or Sagatiba (not sugar cane vodka — different fermentation)
½ lime, cut into 4-6 wedges
2 tsp white sugar (or 22.5ml simple syrup)
---
1. Place lime wedges in the rocks glass, skin-side down
2. Add sugar directly onto the lime
3. Muddle firmly 8-10 times — extract juice and oil, not pulp
4. Fill the glass completely with crushed ice
5. Add cachaca, stir vigorously to dissolve sugar and integrate
6. Taste — adjust with a squeeze of fresh lime if needed
---
Garnish: Lime wedge on rim or floated lime wheel
Temperature: Serve immediately — crushed ice is integral to the drink, not incidental
Note: Cachaca is not rum — it ferments from fresh cane juice, not molasses. The grassy, funky character is the point. Do not substitute.

""",

    8857: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled rocks glass, absinthe-rinsed | Ice: None — served neat
---
60ml (2oz) rye whiskey — Sazerac Rye, Rittenhouse, or Buffalo Trace
5ml (1 barspoon) simple syrup (1:1) or 1 sugar cube
3 dashes Peychaud's bitters
1 dash Angostura bitters
5ml (1 barspoon) absinthe — Pernod, Herbsaint, or Lucid (for the rinse only)
---
1. Chill the rocks glass in the freezer or with ice water
2. Pour absinthe into the glass, swirl to coat all interior surfaces, discard the excess
3. Place sugar cube in a mixing glass, saturate with both bitters, muddle until dissolved
4. Add rye whiskey and ice, stir for 30 seconds
5. Strain into the absinthe-rinsed glass — no ice
6. Express a lemon peel skin-side down over the surface to spray oils, run around the rim, then discard — do not put it in the drink
---
Garnish: Expressed lemon peel — discarded (this is law in New Orleans)
Temperature: Served neat, no ice — the absinthe rinse is aromatic, not liquid
Note: Peychaud's bitters is not interchangeable with Angostura — the anise character is specific to this drink. The absinthe rinse is structural. Created at Merchant's Exchange Saloon, New Orleans, 1830s-1850s.

""",

    8858: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
45ml (1½oz) Campari
45ml (1½oz) sweet vermouth — Carpano Antica Formula or Cocchi di Torino
60ml (2oz) Prosecco — Treviso DOC, dry
---
1. Fill rocks glass with a large ice cube
2. Pour Campari over ice
3. Add sweet vermouth
4. Top with Prosecco — pour gently down the glass to preserve bubbles
5. Stir once with a bar spoon — just enough to briefly marry the ingredients
---
Garnish: Orange half-wheel dropped in (not expressed — the sweetness of the flesh balances the bitterness)
Temperature: Cold — the Prosecco is the backbone, not an afterthought
Note: The "Sbagliato" (Italian: "mistaken") was created at Bar Basso, Milan, when a bartender accidentally reached for Prosecco instead of gin. Do not use Champagne or Cava — Prosecco specifically.

""",

    8859: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe or rocks glass with large cube | Ice: None (coupe) or large cube (rocks)
---
45ml (1½oz) bourbon — Woodford Reserve, Buffalo Trace, or Elijah Craig Small Batch
30ml (1oz) Campari
30ml (1oz) sweet vermouth — Carpano Antica Formula
---
1. Combine bourbon, Campari, and vermouth in a mixing glass over ice
2. Stir for 30-35 seconds — bourbon needs slightly more dilution than gin
3. Strain into a chilled coupe, or over a large ice cube in a rocks glass
4. Express an orange peel over the surface
---
Garnish: Orange peel (expressed and dropped in) or Luxardo cherry
Temperature: Cold but not icy — stirred cocktails should be silky, not watery
Note: The bourbon-based sister to the Negroni. The balance between barrel sweetness and Campari bitterness is the heart. Increase bourbon to 60ml for a boozier, spirit-forward version.

""",

    8860: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
22.5ml (¾oz) bourbon — Buffalo Trace or Bulleit
22.5ml (¾oz) Aperol
22.5ml (¾oz) Amaro Nonino
22.5ml (¾oz) fresh lemon juice
---
1. Combine all four equal-parts ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
---
Garnish: None (optional: expressed lemon peel)
Temperature: Ice-cold — the balance between bitter and sour is most precise when very cold
Note: Created by Sam Ross at Milk & Honey, New York. A perfect-ratio cocktail — do not adjust the measurements. The Amaro Nonino is non-negotiable; other amaros change the flavour profile significantly.

""",

    8861: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) blended Scotch — Famous Grouse or Teacher's
22.5ml (¾oz) fresh lemon juice
22.5ml (¾oz) honey-ginger syrup (2:1 honey to water, infused with 30g fresh ginger, steeped 20 minutes, strained)
7.5ml (¼oz) Islay single malt float — Laphroaig 10 or Caol Ila 12
3 thin slices fresh ginger (for shaking)
---
1. Muddle ginger slices briefly in the shaker — bruise, don't pulverize
2. Add Scotch, lemon juice, and honey-ginger syrup with ice
3. Shake hard for 15-20 seconds
4. Double-strain over a large ice cube — the ginger filter is critical
5. Float Islay malt slowly over the back of a bar spoon — it should sit as a visible smoky layer
---
Garnish: Candied ginger on a cocktail pick
Temperature: Cold — the smoke of the Islay float is an aromatic layer inhaled before tasting
Note: Created by Sam Ross at Milk & Honey, New York. The smoke is olfactory seasoning, not a flavour bomb. Use 12-15% peated malt for the float.

""",

    8875: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
22.5ml (¾oz) London dry gin — Tanqueray or Beefeater
22.5ml (¾oz) green Chartreuse
22.5ml (¾oz) maraschino liqueur — Luxardo
22.5ml (¾oz) fresh lime juice
---
1. Combine all four equal-parts ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
---
Garnish: Expressed lime peel or lime wheel on rim
Temperature: Ice-cold — Chartreuse's aggressive herbal intensity is tempered beautifully by cold
Note: A perfect-ratio Prohibition-era cocktail. Green Chartreuse dominates without apology — this is correct. Yellow Chartreuse (sweeter, less intense) creates a softer variation worth exploring.

""",

    8876: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe (absinthe-rinsed) | Ice: None (shaken then strained)
---
22.5ml (¾oz) London dry gin
22.5ml (¾oz) Cointreau
22.5ml (¾oz) Lillet Blanc (or Cocchi Americano for closer to the original recipe)
22.5ml (¾oz) fresh lemon juice
1 rinse of absinthe or Pastis — swirled and discarded
---
1. Rinse the chilled coupe with absinthe, swirl to coat, discard
2. Combine gin, Cointreau, Lillet Blanc, and lemon juice in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain into the absinthe-rinsed coupe
---
Garnish: Expressed lemon peel (the absinthe aroma is the primary garnish)
Temperature: Ice-cold — this was designed as a morning drink (hangover cure) and should be bracingly cold
Note: Named for its role as a morning restorative. The absinthe rinse carries the anise note that ties the whole drink together.

""",

    8877: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
45ml (1½oz) London dry gin — Tanqueray, Plymouth, or Martin Miller's
15ml (½oz) maraschino liqueur — Luxardo
7.5ml (¼oz) creme de violette — Giffard or Rothman & Winter (essential for colour and floral note)
22.5ml (¾oz) fresh lemon juice
---
1. Chill the coupe with ice water
2. Combine all ingredients in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain into the chilled coupe
5. The drink should be pale lavender — not purple, not grey. Grey indicates stale creme de violette
---
Garnish: Luxardo maraschino cherry dropped in (it sinks — that's correct)
Temperature: Ice-cold — floral and citrus notes are most pronounced when cold
Note: Hugo Ensslin's 1916 recipe includes creme de violette; Harry Craddock's 1930 Savoy Cocktail Book omits it. The violet version is more visually striking and aromatically complex.

""",

    8878: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
22.5ml (¾oz) rye whiskey — Rittenhouse or Sazerac
22.5ml (¾oz) cognac — Remy Martin VSOP or Pierre Ferrand Ambre
22.5ml (¾oz) sweet vermouth — Carpano Antica Formula
7.5ml (¼oz) Benedictine
1 dash Angostura bitters
1 dash Peychaud's bitters
---
1. Combine all ingredients in a mixing glass over ice
2. Stir for 30-35 seconds — this is a stirred cocktail of deep complexity
3. Strain over a large ice cube in a rocks glass
4. Express a lemon peel over the surface
---
Garnish: Expressed lemon peel or Luxardo cherry for a sweeter profile
Temperature: Cold — this is a drink for slow sipping, not rushing
Note: Created at Hotel Monteleone, New Orleans, by Walter Bergeron, circa 1937. The Benedictine bridges the rye and cognac — it is not optional.

""",

    8884: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) London dry gin — Tanqueray, Beefeater, or Plymouth
22.5ml (¾oz) fresh lemon juice
22.5ml (¾oz) honey syrup (2:1 raw honey dissolved in warm water, cooled)
---
1. Dissolve honey in warm water to make syrup — cool completely before using
2. Combine gin, lemon juice, and honey syrup in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain into a chilled coupe
---
Garnish: Expressed lemon peel
Temperature: Ice-cold — honey sweetness is cleanest when cold
Note: A Prohibition-era cocktail designed to mask poor gin. With good gin it is revelatory. Raw honey makes a perceptibly better syrup than processed honey. The 2:1 ratio creates a pourable syrup with more honey flavour.

""",

    8885: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass or coupe | Ice: Cubed (rocks) or none (up)
---
45ml (1½oz) Disaronno Originale (or Lazzaroni for a drier, more almond-forward style)
30ml (1oz) cask-strength bourbon — Wild Turkey 101 or Evan Williams Bottled-in-Bond (offsets sweetness)
30ml (1oz) fresh lemon juice
1 egg white
2 dashes Angostura bitters (for foam pattern)
---
1. Combine amaretto, bourbon, lemon juice, and egg white in a shaker with no ice
2. Dry shake for 15-20 seconds to emulsify the egg white
3. Add ice, shake hard for 12-15 seconds
4. Strain into rocks glass over ice, or double-strain into chilled coupe
5. Allow foam to settle 10 seconds before garnishing
6. Dash Angostura over the foam, drag a toothpick for a pattern
---
Garnish: Angostura bitters pattern on foam + Luxardo cherry
Temperature: Cold — the bourbon warmth should still register through the chill
Note: The addition of bourbon (Jeffrey Morgenthaler's technique) corrects the cloying sweetness of classic versions. Without it, amaretto sours are one-dimensional. The 101-proof bourbon is specifically chosen to cut through the sweetness.

""",

    8886: """RECIPE:
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
60ml (2oz) Gosling's Black Seal rum — trademark-protected in Bermuda; no substitution
120ml (4oz) Fever-Tree Ginger Beer or Gosling's own ginger beer (not ginger ale)
15ml (½oz) fresh lime juice
---
1. Fill the highball glass with ice
2. Pour ginger beer over the ice
3. Pour Gosling's rum directly over the ginger beer — it floats as a dark cap
4. Squeeze fresh lime juice over the top
5. Do not stir — the visual of dark rum over the ginger storm is the presentation
---
Garnish: Lime wedge on the rim
Temperature: Cold — the contrast between the dark rum float and cold ginger beer is part of the experience
Note: Gosling's Black Seal is legally protected as the rum in a Dark and Stormy (trademark law, Bermuda). Using another rum makes it a "Dark and Cloudy." This is not brand preference — it is intellectual property.

""",

    8887: """RECIPE:
Yield: 1 cocktail | Glassware: Silver or pewter julep cup (or highball) | Ice: Fine crushed
---
60ml (2oz) Kentucky straight bourbon — Woodford Reserve, Maker's Mark, or Old Forester 1920
10ml (⅓oz) simple syrup (1:1)
8-10 fresh spearmint leaves
---
1. Chill the julep cup in the freezer for 30 minutes if using metal
2. Place mint in the cup, add simple syrup, gently press with muddler 3-4 times — you want oils, not shredded mint
3. Fill the cup completely with fine crushed ice, mounding it above the rim
4. Pour bourbon over the ice
5. Stir briefly with a long bar spoon until frost forms on the outside of the metal cup
6. Pack more crushed ice to create a dome above the rim
7. Insert a mint sprig through a straw (the straw brings the nose into the mint while drinking)
---
Garnish: Generous fresh mint bouquet pressed into the crushed ice — slap it first
Temperature: The frosted cup is the temperature indicator — the drink must be extremely cold
Note: The mint is primarily aromatic — you drink through it. Never over-muddle: bitter green mint juice ruins the drink. The straw placement is intentional.

""",

    8888: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) Pisco — Barsol Quebranta, Campo de Encanto, or Don Cesar (Peruvian, not Chilean, for the authentic version)
30ml (1oz) fresh lime juice
22.5ml (¾oz) simple syrup (1:1) or gomme syrup
1 egg white — essential, non-negotiable
3 dashes Angostura bitters (for garnish)
---
1. Combine pisco, lime juice, simple syrup, and egg white in a shaker without ice
2. Dry shake for 15-20 seconds until the egg white emulsifies into thick foam
3. Add ice, shake hard for 12-15 seconds
4. Double-strain into a chilled coupe
5. Wait 15 seconds for the foam to set before garnishing
6. Place 3 dashes of Angostura bitters on the foam — traditionally in a line or pattern
---
Garnish: Angostura bitters on foam (3 drops or a deliberate pattern)
Temperature: Ice-cold — the pisco's fruity grape character is most expressive when cold
Note: Chilean pisco is lighter; Peruvian pisco (Quebranta, Torontel, Albilla) has more character. Gomme syrup with gum arabic gives additional foam stability. The debate between Peru and Chile over who invented this drink is ongoing and passionate.

""",

    8905: """RECIPE:
Yield: 1 cocktail | Glassware: Highball or sling glass | Ice: Cubed
---
45ml (1½oz) London dry gin
22.5ml (¾oz) Cherry Heering
7.5ml (¼oz) Cointreau
7.5ml (¼oz) Benedictine
60ml (2oz) fresh pineapple juice — not from concentrate
15ml (½oz) fresh lime juice
10ml (⅓oz) grenadine — pomegranate-based, not commercial red syrup
1 dash Angostura bitters
60ml (2oz) soda water
---
1. Combine gin, Cherry Heering, Cointreau, Benedictine, pineapple juice, lime juice, grenadine, and bitters in a shaker with ice
2. Shake for 12-15 seconds
3. Strain into a highball glass over ice
4. Top with soda water gently
5. Optional: float additional Cherry Heering over the back of a bar spoon for colour
---
Garnish: Pineapple slice + cherry on a pick
Temperature: Cold — this is a tropical drink; refreshment is the goal

""",

    8906: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
22.5ml (¾oz) Scotch whisky — Dewar's 12 or Famous Grouse Smoky Black
22.5ml (¾oz) Cherry Heering
22.5ml (¾oz) sweet vermouth — Carpano Antica Formula
22.5ml (¾oz) fresh orange juice, strained
---
1. Chill the coupe with ice water
2. Combine all four equal-parts ingredients in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain into the chilled coupe
---
Garnish: Expressed orange peel or orange half-wheel on rim
Temperature: Ice-cold — Scotch tannins are most pleasant when chilled
Note: Named after the 1922 Rudolph Valentino film. Fresh orange juice is critical — bottled makes this flat and overly sweet. The equal-parts ratio is the complete recipe.

""",

    8907: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
45ml (1½oz) London dry gin — Tanqueray or Plymouth
22.5ml (¾oz) fresh lemon juice
15ml (½oz) raspberry syrup (Monin, Giffard, or house-made: 200g raspberries + 200g sugar + 100ml water, strained)
1 egg white
---
1. Combine gin, lemon juice, raspberry syrup, and egg white in a shaker with no ice
2. Dry shake for 15-20 seconds to emulsify
3. Add ice, shake hard for 12-15 seconds
4. Double-strain into a chilled coupe
5. The foam should be pale pink — not bright red
---
Garnish: Fresh raspberry rested on the foam
Temperature: Ice-cold — floral raspberry and gin botanicals are most elegant cold

""",

    8908: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) white rum — Havana Club 3 or Bacardi Superior
30ml (1oz) fresh grapefruit juice, strained
15ml (½oz) maraschino liqueur — Luxardo
7.5ml (¼oz) fresh lime juice
Optional: 5ml simple syrup — taste first; depends on grapefruit sweetness
---
1. Combine rum, grapefruit juice, Luxardo, and lime juice in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
4. Taste before serving — if very tart, add simple syrup and reshake briefly
---
Garnish: Grapefruit slice or lime wheel on rim
Temperature: Ice-cold — this is a bracing, complex daiquiri, not a sweet one
Note: Also called the "Papa Doble." Hemingway drank it without sugar, double the rum. The balance between grapefruit bitterness and Luxardo's almond-cherry character is the art of this drink.

""",

    8914: """RECIPE:
Yield: 1 cocktail | Glassware: Tiki mug or rocks glass | Ice: Large chunks or crushed
---
45ml (1½oz) aged Jamaican dark rum — Appleton Estate 12 or Smith & Cross
45ml (1½oz) Campari
45ml (1½oz) fresh pineapple juice
15ml (½oz) fresh lime juice
15ml (½oz) simple syrup (1:1) or Demerara syrup
---
1. Combine all ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Strain into tiki mug or rocks glass over fresh ice
---
Garnish: Pineapple frond + pineapple chunk on a pick
Temperature: Cold — Campari bitterness and Jamaican rum funk need cold to balance
Note: Created at the Hilton Kuala Lumpur in 1978 by Jeffrey Ong. The combination of Campari and rum was considered heretical — it works because Jamaican rum's funky yeast character matches Campari's bitterness perfectly.

""",

    8915: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) mezcal — Del Maguey Vida, Banhez, or Vago Espadin (espadin-based for approachability)
30ml (1oz) fresh lime juice
22.5ml (¾oz) Cointreau
Optional: 5ml agave syrup if mezcal is particularly dry
Optional: chili-salt rim (tajin + kosher salt 1:1)
---
1. Combine mezcal, lime juice, and Cointreau in a shaker with ice
2. Shake hard for 12-15 seconds
3. Strain over a large ice cube in a rocks glass
4. Taste — smoke should be present but not overwhelming
---
Garnish: Lime wheel + optional chili-salt half rim
Temperature: Cold — smoke aromatics are most controlled when cold

""",

    8916: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass or chilled coupe | Ice: Cubed (rocks) or none (up)
---
60ml (2oz) 100% agave tequila — Tapatio Reposado, El Tesoro Blanco, or Fortaleza Blanco
30ml (1oz) fresh lime juice
22.5ml (¾oz) agave syrup (2:1 agave nectar dissolved in warm water)
---
1. Combine tequila, lime juice, and agave syrup in a shaker with ice
2. Shake hard for 12-15 seconds
3. Strain over fresh ice (rocks) or into a chilled coupe
4. No salt rim required — but offer on the side if requested
---
Garnish: Lime wheel on the rim
Temperature: Cold — the agave-to-agave conversation between tequila and syrup is most nuanced cold
Note: Created by Julio Bermejo at Tommy's Mexican Restaurant, San Francisco. Replacing Cointreau with agave syrup makes the tequila the uncontested star. Must use 100% agave — mixto will be exposed.

""",

    8917: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe + shot glass of Champagne on the side | Ice: None (shaken then strained)
---
50ml (1⅔oz) vanilla vodka — Absolut Vanilla or Ketel One with house vanilla infusion
15ml (½oz) Passoa (passion fruit liqueur)
15ml (½oz) vanilla syrup (1:1)
30ml (1oz) fresh passion fruit juice (from 2-3 passion fruits, strained) — or 22.5ml Funkin passion fruit puree
15ml (½oz) fresh lime juice
One glass of Champagne or Prosecco (30-45ml) served as a side shot
---
1. Combine vanilla vodka, Passoa, vanilla syrup, passion fruit juice, and lime juice in a shaker with ice
2. Shake hard for 15-20 seconds
3. Double-strain into a chilled coupe
4. Balance a passion fruit half, flesh-side up, on the rim
5. Serve with a side shot of Champagne — they alternate (sip cocktail, sip Champagne)
---
Garnish: Passion fruit half on the rim + side shot of Champagne
Temperature: Ice-cold coupe — the passion fruit foam surface is part of the presentation
Note: Created by Douglas Ankrah at LAB bar, London. The Champagne chaser is part of the drink's design, not optional theatre. Use real passion fruits for the garnish — the seeds and flesh are visual and aromatic.

""",

    8923: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Crushed
---
50ml (1⅔oz) London dry gin — Tanqueray or Beefeater
25ml (¾oz+) fresh lemon juice
12.5ml (scant ½oz) simple syrup (1:1)
15ml (½oz) creme de mure (blackberry liqueur — Giffard or Briottet, poured over last)
---
1. Combine gin, lemon juice, and simple syrup in a shaker with ice
2. Shake hard for 12-15 seconds
3. Strain over crushed ice mounded above the rim of a rocks glass
4. Pour creme de mure over the top of the ice — it bleeds down through the ice in a visual gradient
5. Do not stir — the gradient is the visual
---
Garnish: Two blackberries + lemon slice pressed into the crushed ice
Temperature: Cold — the fruit liqueur trails through the ice as the drink is consumed
Note: Created by Dick Bradsell at Fred's Club, London, circa 1984. The creme de mure is poured last and drunk before it fully integrates — each sip changes as the liqueur bleeds through.

""",

    8924: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
22.5ml (¾oz) mezcal — Del Maguey Vida or Banhez
22.5ml (¾oz) Aperol
22.5ml (¾oz) yellow Chartreuse
22.5ml (¾oz) fresh lime juice
---
1. Combine all four equal-parts ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
---
Garnish: Expressed lime peel
Temperature: Ice-cold — mezcal smoke and Chartreuse herbs negotiate beautifully when cold
Note: Created by Phil Ward at Death & Company, New York. The mezcal-Aperol combination is the Paper Plane's smokier, more assertive cousin. Equal parts — no adjustment needed or welcome.

""",

    8925: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) bourbon — Bulleit, Buffalo Trace, or Elijah Craig Small Batch
22.5ml (¾oz) fresh lemon juice
22.5ml (¾oz) honey syrup (3:1 raw honey to warm water — thicker than standard)
---
1. Make honey syrup: dissolve honey in warm (not hot) water; cool before use
2. Combine bourbon, lemon juice, and honey syrup in a shaker with ice
3. Shake hard for 12-15 seconds
4. Strain over a large ice cube in a rocks glass
---
Garnish: Expressed lemon peel
Temperature: Cold — honey opens at room temperature and becomes cloying
Note: Created by T.J. Siegal at Milk & Honey, New York. The 3:1 honey syrup is thicker than the Bee's Knees version — needed to balance 60ml of bourbon. Raw honey is meaningfully better than processed.

""",

    8926: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) aged rum — Plantation Original Dark, Appleton Estate Signature, or Ron Zacapa 23
5ml (1 barspoon) Demerara syrup (2:1 Demerara sugar to water — not simple syrup)
2 dashes Angostura bitters
1 dash Bittercube Jamaica No. 2 or Elemakule Tiki bitters (optional but excellent)
---
1. Combine rum, Demerara syrup, and bitters in a mixing glass over ice
2. Stir for 25-30 seconds — rum old fashioneds need slightly less dilution than bourbon versions
3. Strain over a large ice cube in a rocks glass
4. Express an orange peel, run around the rim, drop in
---
Garnish: Orange peel (expressed)
Temperature: Cold — Demerara syrup's molasses depth needs cold to stay restrained
Note: Demerara syrup mirrors the sugarcane heritage of rum. Jamaican rum (Smith & Cross) makes this funky and complex; Spanish-style rum (Diplomatico Reserva) makes it softer and sweeter.

""",

    8941: """RECIPE:
Yield: 1 cocktail | Glassware: Thin-walled highball (chilled in freezer 10 min) | Ice: Single large clear ice cylinder or sphere
---
45ml (1½oz) Japanese blended whisky — Suntory Toki (primary), Nikka From The Barrel (secondary)
90-120ml (3-4oz) chilled soda water — Suntory Wilkinson Tansan ideally; Fever-Tree or Q Club Soda acceptable
---
Suntory method (precise):
1. Freeze the highball glass for 10 minutes — or fill with ice water while preparing
2. Place a single large, clear ice cylinder or sphere in the glass — this is the dilution control
3. Pour whisky over the ice; stir exactly 13.5 times in one fluid, clockwise motion
4. Top with soda water poured very gently and slowly down the inside of the glass
5. Lift the bar spoon once through the drink from the bottom — one gentle lift, then stop
---
Garnish: None (traditional Suntory style) or expressed lemon peel set on the rim without touching the liquid
Temperature: Everything must be very cold — glass, ice, whisky, and soda water
Note: The 13.5 stirs before adding soda, and one lift after, is the Suntory method precisely. Each stir integrates without breaking carbonation. This ritual is taken as seriously in Japan as tea ceremony.

""",

    8942: """RECIPE:
Yield: 1 cocktail | Glassware: Small rocks glass (verre a punch) | Ice: One small ice cube, or none (tradition varies)
---
60ml (2oz) white rhum agricole — Rhum J.M Blanc, Clement Premiere Canne, or Neisson Blanc
5-10ml (1-2 tsp) cane syrup — Petit Canne or Sirop de Canne de Martinique (not simple syrup — raw cane carries terroir)
1 small disc of lime peel (2cm disc — use the zest side only, not a full squeeze)
---
1. Pour cane syrup into the glass
2. Add the lime disc; press gently to express the oils into the syrup
3. Add rhum agricole
4. Add one small ice cube — or serve sans glace (without ice) as preferred in Martinique
5. Stir once — the drinker traditionally adjusts proportions to personal taste
---
Garnish: The lime disc is the garnish
Temperature: Martiniquais often drink this at room temperature or with minimal ice — this is cultural, not a mistake
Note: "Chacun prepare son propre" — each person prepares their own Ti' Punch. In Martinique, the host provides bottles and each drinker builds their own proportions. The cane syrup carries terroir that simple syrup cannot replicate.

""",

    8943: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe or nick & nora | Ice: None (stirred then strained)
---
45ml (1½oz) London dry gin — Tanqueray or Beefeater
45ml (1½oz) sweet vermouth — Carpano Antica Formula or Punt e Mes
7.5ml (¼oz) Fernet-Branca
---
1. Combine gin, sweet vermouth, and Fernet-Branca in a mixing glass over ice
2. Stir for 30 seconds — Fernet is powerful and needs full dilution to integrate
3. Strain into a chilled coupe or nick & nora
4. Express an orange peel over the surface
---
Garnish: Expressed orange peel
Temperature: Cold — Fernet-Branca's menthol and herbal intensity is most manageable cold
Note: Created by Ada Coleman at the American Bar, The Savoy, London, circa 1920. One of the few classic cocktails created by a woman, still celebrated under her name. Fernet-Branca is non-negotiable — it is the ingredient that defines the Hanky Panky.

""",

    8944: """RECIPE:
Yield: 1 cocktail | Glassware: Highball | Ice: None in the finished drink
---
60ml (2oz) London dry gin — Plymouth or Tanqueray
22.5ml (¾oz) fresh lemon juice
22.5ml (¾oz) fresh lime juice
30ml (1oz) heavy cream (not whipping cream)
15ml (½oz) simple syrup (1:1)
1 egg white
3 drops orange flower water — the concentrated water, not blossom syrup
30ml (1oz) chilled soda water
---
1. Combine gin, both citrus juices, cream, simple syrup, egg white, and orange flower water in a shaker WITHOUT ice
2. Dry shake for 2 full minutes — this step creates the texture; do not shortchange it
3. Add ice and shake hard for another 2 minutes — the prolonged shake is the recipe
4. Strain into a highball with no ice
5. Add chilled soda water slowly down the inside of the glass as the foam rises
6. The finished drink: tall, white, frothy
---
Garnish: None
Temperature: All ingredients should be refrigerator-cold before starting
Note: Henry C. Ramos invented this in New Orleans, 1888. He employed "shaker boys" who passed the shaker down a line for 12 minutes total. Modern target is 4-5 minutes minimum. Orange flower water is measured in drops — overpouring creates a perfume-counter drink.

""",

    8950: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) blanco tequila — Tapatio, Olmeca Altos, or Cimarron
30ml (1oz) fresh lime juice
22.5ml (¾oz) Cointreau
15ml (½oz) fresh jalapeno juice (or 3-5 jalapeno slices, muddled then strained)
Chili-salt rim: 1:1 kosher salt to tajin
---
1. Prepare jalapeno juice: muddle 3-5 jalapeno slices in the shaker, shake with ice, double-strain — keep liquid
2. Alternatively, juice whole jalapenos through a juicer
3. Rim half the glass with lime wedge + chili-salt mixture
4. Combine tequila, lime juice, Cointreau, and jalapeno juice in shaker with ice
5. Shake hard for 15 seconds
6. Strain over a large ice cube
---
Garnish: Jalapeno slice on rim + lime wheel
Temperature: Cold — jalapeno heat increases as the drink warms; keep it cold
Note: Control heat by adjusting jalapeno quantity. Habanero for extreme heat; serrano for medium. Seeds carry most heat — removing them before muddling creates a milder drink.

""",

    8951: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled martini glass or coupe | Ice: None (stirred then strained)
---
75ml (2½oz) London dry gin (more interesting) or vodka (more traditional for dirty)
15ml (½oz) dry vermouth — Noilly Prat (fresh bottle, refrigerated)
15-22.5ml (½-¾oz) olive brine — from quality green olives in brine, not sweet cocktail olives
---
1. Chill the martini glass in the freezer or with ice water
2. Combine spirit, vermouth, and olive brine in a mixing glass over ice
3. Stir for 40-45 seconds — the brine needs thorough chilling
4. Strain into the chilled, dry glass
5. Garnish with 2-3 quality olives on a cocktail pick, submerged in the drink
---
Garnish: 2-3 Castelvetrano or Cerignola olives on a pick
Temperature: Ice-cold — warm dirty martinis are deeply unpleasant
Note: "Extra dirty" means more brine. Use quality olives — cheap olive brine smells of vinegar. Castelvetrano olives are mild and buttery; Cerignola are meatier. Never use pimento-stuffed cocktail olives.

""",

    8952: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe or martini glass | Ice: None (shaken then strained)
---
50ml (1⅔oz) vodka — Ketel One or Belvedere
20ml (⅔oz) lychee liqueur — Kwai Feh or Giffard Lychee
15ml (½oz) dry vermouth — Noilly Prat
30ml (1oz) fresh lychee juice (4-5 fresh lychees pressed; or canned lychee syrup if unavailable)
10ml (⅓oz) fresh lime juice
---
1. Chill the glass with ice water
2. Combine all ingredients in a shaker with ice
3. Shake hard for 12-15 seconds
4. Double-strain through fine mesh into chilled glass — remove any pulp
---
Garnish: Fresh lychee on a pick or dropped in
Temperature: Ice-cold — the perfumed, floral quality of lychee is most elegant cold

""",

    8953: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
50ml (1⅔oz) vodka — Ketel One or Grey Goose
30ml (1oz) fresh passion fruit juice (2-3 passion fruits pressed through strainer)
15ml (½oz) Passoa (passion fruit liqueur)
10ml (⅓oz) fresh lime juice
10ml (⅓oz) vanilla syrup (1:1 with vanilla extract, or infused vanilla bean)
---
1. Combine all ingredients in a shaker with ice
2. Shake very hard for 15-20 seconds — passion fruit pulp creates natural foam
3. Double-strain through fine mesh into chilled coupe — removes seeds
---
Garnish: Passion fruit half on rim, flesh-side up, seeds visible
Temperature: Ice-cold — fresh passion fruit oxidizes quickly; serve immediately

""",

    8954: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube or cubed
---
60ml (2oz) blanco tequila — Tapatio or Olmeca Altos
60ml (2oz) fresh watermelon juice (blend and strain — 2 cups cubed watermelon yields roughly 150ml)
22.5ml (¾oz) Cointreau
15ml (½oz) fresh lime juice
5ml (1 tsp) agave syrup — optional; taste first, ripe watermelon may not need it
---
1. Blend watermelon chunks, strain through fine mesh — should be a clear, deep pink juice
2. Combine tequila, watermelon juice, Cointreau, and lime juice in a shaker with ice
3. Shake hard for 15 seconds
4. Strain over ice in a rocks glass
---
Garnish: Watermelon wedge + lime wheel on rim
Temperature: Very cold — watermelon flavour blooms then dies quickly as it warms
Note: Use only peak-season watermelon — under-ripe melon gives watery, flat juice. Taste the juice before adding lime; natural sweetness varies dramatically.

""",

    8975: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml (2oz) bourbon — Buffalo Trace or Woodford Reserve Double Oaked
7.5ml (¼oz) hot honey syrup (2:1 raw honey to water, infused with 1-2 sliced fresno or calabrian chilis, steeped 20 min, strained)
2 dashes Angostura bitters
1 dash mole bitters — Bittermens Xocolatl Mole (optional, adds depth)
---
1. Make hot honey syrup: heat honey and water to 60°C, add sliced chilis, steep 20 minutes, strain and cool
2. Combine bourbon, hot honey syrup, and bitters in a mixing glass over ice
3. Stir for 25-30 seconds
4. Strain over a large ice cube
5. Express an orange peel
---
Garnish: Orange peel (expressed) + optional thin chili ring on the rim
Temperature: Cold — chili heat is most controlled when the drink is cold

""",

    8976: """RECIPE:
Yield: 1 cocktail | Glassware: Coupe (smoked interior) | Ice: None (shaken then strained)
---
60ml (2oz) mezcal — Del Maguey San Luis del Rio or Vago Espadin en Barro
15ml (½oz) Cointreau
15ml (½oz) fresh lime juice
10ml (⅓oz) agave syrup (2:1)
To smoke the glass: fresh rosemary sprig or applewood chip
---
1. Smoke the coupe: burn the rosemary or wood chip, invert the glass over it, allow smoke to fill interior for 30 seconds
2. Combine mezcal, Cointreau, lime juice, and agave syrup in a shaker with ice
3. Shake hard for 12-15 seconds
4. Strain into the smoked coupe — pour directly into the smoke without inverting the glass first
5. Rest the scorched rosemary sprig on the rim
---
Garnish: Scorched rosemary sprig + lime wheel
Temperature: Ice-cold — the smoke is aromatic, the drink should contrast it with sharp coldness

""",

    8977: """RECIPE:
Yield: 1 cocktail | Glassware: Longneck bottle or highball | Ice: None (traditional) or cubed
---
60ml (2oz) blanco tequila — Casamigos Blanco, Tapatio, or El Jimador
30ml (1oz) fresh lime juice
120ml (4oz) Topo Chico sparkling mineral water — the canonical brand; the Texas standard
---
1. Pour tequila and lime juice directly into a cold Topo Chico bottle, or a highball with ice
2. Top with Topo Chico — pour slowly to maintain bubbles
3. Squeeze a lime wedge over and drop in
4. Stir once (or don't — traditionalists don't)
---
Garnish: Lime wedge
Temperature: Near-frozen — Topo Chico must be very cold; its mineral profile is better near-frozen
Note: This is West Texas ranch country in a glass. No sweetener. No triple sec. Tequila, lime, sparkling mineral water. The Topo Chico mineral character is part of the drink — substitute Perrier or San Pellegrino if unavailable.

""",

    8978: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Cubed
---
60ml (2oz) London dry gin — Tanqueray or Beefeater (avoid heavily floral gins — they clash with basil)
30ml (1oz) fresh lemon juice
22.5ml (¾oz) simple syrup (1:1)
10-12 large fresh Italian basil leaves (not Thai basil)
---
1. Combine basil and simple syrup in the shaker — muddle lightly (5-6 presses) to release oils without shredding
2. Add gin and lemon juice
3. Shake hard with ice for 15-20 seconds — further basil extraction occurs during the shake
4. Double-strain through fine mesh into rocks glass over fresh ice — basil fragments turn bitter if left in
5. The drink should be pale green — vivid green means over-muddled; brown means oxidized basil
---
Garnish: Basil sprig placed immediately before serving — wilts fast
Temperature: Cold — basil oxidizes within minutes; serve and drink immediately
Note: Created by Jorg Meyer at Le Lion, Hamburg. Double-straining is essential. Tender basil leaves are best — woody stems give bitter flavour.

""",

    8979: """RECIPE:
Yield: 1 cocktail | Glassware: Large wine glass | Ice: Large cubes (2-3)
---
60ml (2oz) Campari
60ml (2oz) sweet vermouth — Carpano Antica Formula
60ml (2oz) Prosecco — Treviso DOC
30ml (1oz) soda water
---
1. Fill wine glass with 2-3 large ice cubes
2. Pour Campari over ice
3. Add sweet vermouth
4. Top with Prosecco, pouring down the side
5. Add soda water
6. Stir once gently
---
Garnish: Orange half-wheel
Temperature: Cold — the Prosecco is the lightener and its temperature matters

""",

    8993: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) Earl Grey-infused gin — cold-infuse 2 Earl Grey bags per 700ml London dry gin for 2 hours; strain
(Alternative: 50ml London dry gin + 15ml Earl Grey syrup: steep 3 bags in 200ml hot water 4 min, add 200g sugar, cool)
15ml (½oz) fresh lemon juice
10ml (⅓oz) simple syrup (1:1)
1 egg white (optional — creates silkiness and foam)
---
1. With egg white: combine all in shaker without ice, dry shake 15 seconds
2. Add ice, shake hard 12-15 seconds
3. Double-strain into chilled coupe
---
Garnish: Expressed lemon peel
Temperature: Ice-cold — bergamot oils are most aromatic when cold
Note: The bergamot oil in Earl Grey is the perfume of this drink — too much and it becomes medicinal. Infusion time is critical: over 2 hours and the tea turns tannic and bitter.

""",

    8994: """RECIPE:
Yield: 1 cocktail | Glassware: Collins or highball | Ice: Cubed
---
60ml (2oz) London dry gin — Hendrick's or The Botanist (floral gins complement lavender)
30ml (1oz) fresh lemon juice
22.5ml (¾oz) lavender syrup (steep 2 tbsp dried food-grade lavender in 200ml hot water 5 min, strain, add 200g sugar, cool)
90ml (3oz) chilled soda water
---
1. Combine gin, lemon juice, and lavender syrup in a shaker with ice
2. Shake briefly, 10-12 seconds
3. Strain into Collins glass over fresh ice
4. Top with soda water, poured gently down the side
5. Stir once from the bottom
---
Garnish: Dried lavender sprig + lemon wheel
Temperature: Cold and effervescent
Note: Lavender syrup concentration varies widely. Taste before using — dried lavender turns soapy if over-steeped. 5 minutes maximum. Food-grade lavender only — some ornamental lavender is treated with pesticides.

""",

    8995: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
60ml (2oz) Japanese gin — Roku, Ki No Bi, or Nikka Coffey Gin
22.5ml (¾oz) yuzu juice — fresh-pressed in season; bottled Kikkoman or Mitsukan year-round
15ml (½oz) simple syrup (1:1)
5ml (1 tsp) yuzu liqueur — Choya or Suntory (optional — deepens the citrus profile)
---
1. Combine gin, yuzu juice, simple syrup, and yuzu liqueur in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
---
Garnish: Thin yuzu wheel rested on rim, or expressed yuzu peel
Temperature: Ice-cold — yuzu's aromatic citrus oils are most vivid at low temperature
Note: Yuzu juice is significantly more acidic and aromatic than lime or lemon. Adjust simple syrup upward by 5-7ml if the yuzu is particularly tart. Bottled yuzu juice varies — Kikkoman and Mitsukan are reliable.

""",

    8996: """RECIPE:
Yield: 1 cocktail | Glassware: Large copa de balon (balloon gin glass) or highball | Ice: Large ice ball or large cubes
---
50ml (1⅔oz) London dry gin — Tanqueray or Beefeater
150ml (5oz) premium tonic water — Fever-Tree Indian Tonic or East Imperial Old World Tonic
1 tsp ceremonial-grade matcha powder
15ml (½oz) hot water (80°C — not boiling)
5ml (1 tsp) honey syrup (2:1 honey to water)
---
1. Whisk matcha with 80°C water and honey syrup until fully dissolved and lump-free — a chasen (bamboo whisk) gives best results
2. Allow the matcha mixture to cool completely to room temperature — hot liquid kills carbonation
3. Place ice in the balloon glass
4. Pour gin over the ice
5. Add the cooled matcha mixture
6. Top with tonic water, pouring slowly down the side
7. Stir once very gently from the bottom
---
Garnish: Thin cucumber slice + dried lime wheel
Temperature: Cold — matcha and gin botanicals are both floral; cold tempers potential bitterness

""",

    8997: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
30ml (1oz) mezcal — Del Maguey Vida or Vago Espadin
30ml (1oz) Campari
30ml (1oz) sweet vermouth — Carpano Antica Formula or Cocchi di Torino
---
1. Combine mezcal, Campari, and vermouth in a mixing glass over ice
2. Stir for 30 seconds
3. Strain over a large ice cube in a rocks glass
4. Express an orange peel over the surface
---
Garnish: Orange peel (expressed) + optional grapefruit peel for smoke contrast
Temperature: Cold — mezcal smoke is most balanced against cold Campari bitterness
Note: The gin-to-mezcal swap is structurally seamless — mezcal's agave sweetness and smoke replace gin's botanical dryness. Use espadin mezcal (most approachable smoke level) before experimenting with tobala or madrecuixe.

""",

    8998: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
30ml (1oz) London dry gin — Tanqueray or Beefeater
30ml (1oz) Campari (or Mr Black coffee amaro for a softer approach)
30ml (1oz) cold brew coffee concentrate (1:4 ratio, 12-hour cold steep)
Optional: 7.5ml (¼oz) Benedictine for sweetness bridge
---
1. Combine gin, Campari, and cold brew coffee concentrate in a mixing glass over ice
2. Stir for 30-35 seconds
3. Strain over a large ice cube in a rocks glass
4. Express an orange peel — the citrus oils bridge the coffee and bitterness
---
Garnish: Orange peel (expressed) + 3 coffee beans floated on top
Temperature: Cold — coffee bitterness amplifies at room temperature
Note: The cold brew replaces sweet vermouth. The coffee adds bitterness and roasted sweetness that bridges Campari and gin. Cold brew must be concentrate (not ready-to-drink) for the right body and flavour intensity.

""",

    8999: """RECIPE:
Yield: approximately 10 servings (batch cocktail) — individual serving 90ml | Glassware: Nick & nora or coupe | Ice: None
---
Batch:
300ml (10oz) base spirit — cognac, rum, bourbon, or gin (or combination)
150ml (5oz) fresh citrus juice — lemon or lime
150ml (5oz) simple syrup or flavoured syrup
150ml (5oz) fortified wine or liqueur — port, Lillet, Cointreau (optional)
600ml (20oz) whole milk
---
Clarification process:
1. Combine all non-milk ingredients (add citrus last) — this is the punch base
2. Heat milk to 70°C (just below simmering) — do not boil
3. Pour the punch into the hot milk (not milk into punch) — acid curdles milk proteins
4. Stand for 5 minutes while curds form
5. Strain through a coffee filter or fine cheesecloth — takes 2-4 hours; do not press or squeeze
6. The result: crystal-clear, pale amber liquid with remarkable silk texture
7. Refrigerate for service — keeps up to 2 weeks
---
Garnish: Expressed citrus peel, grated nutmeg, or small edible flower — match to the flavour profile
Temperature: Serve at cellar temperature (12-14°C) or lightly chilled — not ice-cold
Note: This technique dates to 17th-century Britain. Casein proteins strip tannins and particulates, clarifying the liquid completely. The result tastes nothing like milk — silky, complex, and remarkably refined.

""",

    9000: """RECIPE:
Yield: 1 cocktail | Glassware: Thin-walled highball (frosted) | Ice: Crystal-clear large cylinder or sphere
---
45ml (1½oz) Japanese blended whisky — Suntory Toki (engineered for highball dilution)
90-120ml (3-4oz) soda water — Suntory Wilkinson Tansan ideal; Fever-Tree or Q Club Soda acceptable
---
Suntory method (exact):
1. Fill highball with ice, stir to chill, pour out melt water — glass must be very cold
2. Pour whisky over ice — stir exactly 3 times
3. Add soda water down the back of a bar spoon to preserve bubbles until glass is full
4. Lift the bar spoon once from the bottom in one upward motion — stop immediately
---
Garnish: Expressed lemon peel placed on the rim without touching the liquid
Temperature: Everything cold — glass, ice, whisky, and soda
Note: The Suntory Toki whisky is specifically engineered for highball dilution — its flavour profile opens up with the addition of carbonated water. The 2:1 soda-to-whisky ratio with maximum carbonation preservation is the goal.

""",

    9008: """RECIPE:
Yield: 1 cocktail | Glassware: Collins glass | Ice: Cubed
---
60ml (2oz) London dry gin — Hendrick's (cucumber-forward) or Tanqueray
15ml (½oz) St-Germain elderflower liqueur
30ml (1oz) fresh lemon juice
15ml (½oz) simple syrup (1:1) — taste first; St-Germain adds sweetness
4-5 thin cucumber slices (English or Persian)
90ml (3oz) chilled soda water
---
1. Muddle cucumber slices with simple syrup in the shaker — 5-6 gentle presses
2. Add gin, St-Germain, and lemon juice with ice
3. Shake hard for 12-15 seconds
4. Double-strain through fine mesh into Collins glass over ice — removes cucumber
5. Top with soda water
---
Garnish: Cucumber ribbon (vegetable peeler, looped inside the glass) + lemon wheel
Temperature: Cold — cucumber becomes vegetal if warm

""",

    9009: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Crushed
---
60ml (2oz) bourbon — Bulleit, Four Roses Single Barrel, or Maker's Mark
22.5ml (¾oz) fresh lemon juice
15ml (½oz) simple syrup (1:1)
6-8 fresh blackberries (or 30ml blackberry puree)
4-5 fresh mint leaves
---
1. Muddle blackberries and mint in the shaker with simple syrup — press firmly to release juice
2. Add bourbon and lemon juice with ice
3. Shake hard for 15 seconds
4. Double-strain through fine mesh into rocks glass over crushed ice — blackberry seeds are bitter and must be removed
---
Garnish: Fresh blackberries on a pick + mint sprig (slapped once)
Temperature: Cold — blackberry oxidizes quickly; serve and drink immediately

""",

    9010: """RECIPE:
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
45ml (1½oz) reposado tequila — Tapatio Reposado or Olmeca Altos Reposado
15ml (½oz) mezcal — Del Maguey Vida
5ml (1 barspoon) agave syrup (2:1)
2 dashes Angostura bitters
1 dash mole bitters — Bittermens Xocolatl Mole (optional but excellent)
---
1. Combine tequila, mezcal, agave syrup, and bitters in a mixing glass over ice
2. Stir for 25-30 seconds
3. Strain over a large ice cube in a rocks glass
4. Express an orange peel over the surface — optional: flame the peel for theatre
---
Garnish: Orange peel (expressed, optionally flamed)
Temperature: Cold — agave dimension of both spirits reads most clearly cold
Note: Created by Phil Ward at Death & Company, New York. The 3:1 tequila-to-mezcal ratio lets the tequila's fruit character lead with mezcal as a smoke finish. Equal parts creates a smokier, mezcal-forward version.

""",

    9024: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
45ml (1½oz) vodka — Ketel One or Belvedere
45ml (1½oz) Mr Black Cold Brew Coffee Liqueur
30ml (1oz) cold brew coffee concentrate (1:4 ratio, 12-hour cold steep — not instant)
Optional: 7.5ml (¼oz) simple syrup — Mr Black carries sweetness; taste first
---
1. Combine vodka, Mr Black, and cold brew concentrate in a shaker with ice
2. Shake extremely hard for 20 seconds — cold brew creates foam through vigorous agitation
3. Double-strain into a chilled coupe
4. Three coffee beans should float on the foam — if they sink, the shake was insufficient
---
Garnish: Three whole coffee beans floated on the foam
Temperature: Serve immediately — cold brew foam is stable but time-limited
Note: The Mr Black method replaces fresh espresso with cold brew concentrate + coffee liqueur for a smoother, less acidic result. The alcohol in Mr Black (25% ABV) assists foam stability. Cold brew must be concentrate, not ready-to-drink.

""",

    9025: """RECIPE:
Yield: 2-4 servings | Glassware: Chilled coupe or wine glass | Ice: Blended
---
750ml (1 bottle) dry rose wine — Provence-style, pale and dry (Whispering Angel, Miraval)
60ml (2oz) vodka or rose brandy — prevents the mixture from freezing solid
30ml (1oz) simple syrup (1:1) or strawberry syrup
30ml (1oz) fresh lemon juice
Optional: 150g fresh or frozen strawberries for colour and flavour
---
1. Freeze the rose wine in a shallow dish for 4-6 hours until partially frozen — it won't fully freeze due to alcohol content
2. Blend the partially frozen rose with vodka, syrup, lemon juice, and strawberries until smooth
3. Taste — adjust sweetness and acidity before serving
4. Pour into chilled coupes or wine glasses immediately
---
Garnish: Fresh strawberry on the rim + thin lemon wheel
Temperature: Slushy — between liquid and frozen; if too liquid, re-freeze 30 minutes
Note: The vodka or high-alcohol addition lowers the freezing point, keeping the mixture slushy rather than solid. Serve immediately after blending — it melts fast.

""",

    9026: """RECIPE:
Yield: 1 cocktail | Glassware: Chilled coupe | Ice: None (shaken then strained)
---
22.5ml (¾oz) London dry gin — Tanqueray or Plymouth
22.5ml (¾oz) green Chartreuse (VEP for special occasions)
22.5ml (¾oz) yellow Chartreuse (replaces maraschino in this variation — honey-herbal, softer)
22.5ml (¾oz) fresh lime juice
---
1. Combine all four equal-parts ingredients in a shaker with ice
2. Shake hard for 12-15 seconds
3. Double-strain into a chilled coupe
---
Garnish: Expressed lime peel
Temperature: Ice-cold — two Chartreuses is intense; cold is the restraint
Note: This variation substitutes yellow Chartreuse for Luxardo maraschino — the result is honey-herbal-lime with green Chartreuse intensity. More complex than the original Last Word, arguably more balanced. Some argue this is the superior version.

""",

    9027: """RECIPE:
Yield: 1 cocktail | Glassware: Highball or copa de balon | Ice: Large cube or cubed
---
45ml (1½oz) gin — The Botanist, Monkey 47, or a gin with spice notes
15ml (½oz) turmeric syrup (steep 30g fresh grated turmeric in 200ml hot water 10 min, strain, add 200g sugar, cool)
15ml (½oz) fresh lemon juice
5ml (1 tsp) fresh ginger juice (grate ginger, press through cloth)
120ml (4oz) tonic water — Fever-Tree Mediterranean Tonic
Pinch of freshly ground black pepper (increases turmeric bioavailability and adds aroma)
---
1. Combine gin, turmeric syrup, lemon juice, and ginger juice in a shaker with ice
2. Shake for 10-12 seconds
3. Strain into glass over ice
4. Top with tonic water
5. Grind black pepper over the surface
---
Garnish: Thin turmeric root slice or turmeric powder dusted on surface + lemon wheel
Temperature: Cold — turmeric can taste medicinal at room temperature; cold tempers it
Note: Turmeric syrup oxidizes rapidly — use within 48 hours. The turmeric-ginger-black pepper combination mirrors golden milk; the drink is genuinely functional as well as flavourful.

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
    print(f"Done. {success} recipes added, {errors} errors.")


if __name__ == "__main__":
    main()
