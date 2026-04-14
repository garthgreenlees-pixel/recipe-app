#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# Spirits category — cocktail/service-adjacent entries ONLY
# Pure spirit descriptions (Scotch, Bourbon, Rum, Tequila, etc.) do NOT get recipes
RECIPES = {

9357: """RECIPE — Absinthe Drip (La Louche) + Sazerac
Yield: 1 serve | Glassware: Traditional absinthe glass or wide coupe | Ice: None
---
ABSINTHE DRIP (traditional):
30ml absinthe (Pernod Absinthe Supérieure, Kübler Swiss, or La Fée Parisienne; 68%+ ABV)
90–150ml ice-cold water (dripped over a sugar cube)
1 sugar cube (placed on a slotted absinthe spoon)

SAZERAC (cocktail):
60ml Cognac or rye whiskey + 5ml absinthe (rinse only) + 2 dashes Peychaud's bitters + 10ml simple syrup
---
ABSINTHE DRIP:
1. Pour absinthe into glass. Set slotted spoon across rim with sugar cube.
2. Drip ice-cold water VERY slowly over sugar cube from a brouilleur (absinthe fountain) or pitcher.
3. Watch the louche — the green fairy turns milky-white as water emulsifies the essential oils.
4. Drip 90–150ml water total. The louche fully forms by 1:3 ratio (absinthe:water).

SAZERAC:
1. Rinse chilled rocks glass with 5ml absinthe (swirl and discard). This glass IS the garnish vessel.
2. Stir rye/Cognac, bitters, and sugar over ice 40 rotations. Strain into rinsed glass.
3. Lemon peel expressed over surface. Discard peel.
---
Garnish: Absinthe drip — no garnish (the louche is the spectacle); Sazerac — expressed lemon peel, discarded
Temperature: Absinthe drip at room temperature (the water is ice-cold); Sazerac at 5°C

""",

9358: """RECIPE — The Last Word (Chartreuse Cocktail)
Yield: 1 cocktail | Glassware: Coupe | Ice: None (served up)
---
22.5ml Green Chartreuse (110 herbs; 55% ABV — do NOT substitute Yellow)
22.5ml fresh lime juice
22.5ml Luxardo Maraschino liqueur
22.5ml dry gin (Tanqueray London Dry or Plymouth)
Equal parts — this is non-negotiable. The cocktail was designed at the Detroit Athletic Club, c.1916.
---
1. Combine all four ingredients in shaker with ice.
2. Shake hard 12 seconds — Chartreuse is thick and needs full aeration.
3. Double-strain into chilled coupe.
4. The drink should be pale green, bright, and intensely aromatic.
5. TASTE NOTE: equal parts means equal presence — gin provides structure, lime acidity, maraschino sweetness, Chartreuse complexity. None overpowers.
---
Garnish: No garnish — the vivid green colour is the visual statement
Temperature: 5–6°C in pre-chilled coupe; serve immediately

""",

9359: """RECIPE — B&B (Bénédictine and Brandy)
Yield: 1 serve | Glassware: Brandy snifter or lowball | Ice: Optional (neat is traditional)
---
30ml Bénédictine D.O.M. (27 herbs and spices; 40% ABV — made at Fécamp, Normandy)
30ml VSOP Cognac (Rémy Martin VSOP or Courvoisier VSOP — Cognac's dried fruit complements Bénédictine's honey)
---
1. TRADITIONAL (neat): pour Bénédictine first into snifter. Pour Cognac over slowly — the two liquids layer briefly before combining.
2. Swirl gently to warm in cupped hands. Nose: honey, botanical herbs, orange peel, anise, Cognac dried fruit.
3. Sip slowly — a B&B is a digestif, meant to be contemplated, not consumed quickly.
4. ON ROCKS: pour both over a large single ice cube. Stir once. The ice opens the herbs over 10 minutes.
5. COCKTAIL VARIANT (Bénédictine Sour): 45ml Bénédictine + 20ml lemon juice + 10ml simple syrup + egg white. Shake dry then wet. Double strain into coupe.
---
Garnish: Neat — no garnish; On ice — wide orange peel; Sour — lemon wheel and dried orange on foam
Temperature: Neat: room temperature (18°C); On rocks: allow to open at 10–14°C

""",

9360: """RECIPE — Paper Plane (Amaro Cocktail)
Yield: 1 cocktail | Glassware: Coupe | Ice: None (served up)
---
22.5ml Amaro Nonino Quintessentia (alpine herb amaro; 35% ABV)
22.5ml Aperol (orange aperitivo; 11% ABV)
22.5ml fresh lemon juice
22.5ml bourbon whiskey (Buffalo Trace or Wild Turkey 101)
---
1. Combine all four equal-parts ingredients in shaker with ice.
2. Shake 12 seconds. The bitterness and acidity of amaro and lemon need full integration.
3. Double-strain into chilled coupe.
4. Equal parts — created by Sam Ross at Milk & Honey, NYC, 2007. Named after the M.I.A. track.
5. AMARO SPRITZ VARIANT: 45ml Amaro Montenegro + 90ml Fever-Tree soda water + ice + orange slice in a highball.
---
Garnish: No garnish for Paper Plane; lemon twist if demanded
Temperature: 5–6°C; serve immediately — bright, tart, and slightly bitter

""",

9366: """RECIPE — Aperol Spritz (The Classic)
Yield: 1 cocktail | Glassware: Large wine glass | Ice: Cubed (generous)
---
90ml Prosecco (Mionetto Prestige Treviso Brut or La Marca — fresh, light; NOT Champagne)
60ml Aperol (aperitivo liqueur; 11% ABV)
30ml Fever-Tree Soda Water
---
1. Fill large wine glass with 4–5 ice cubes — full to the brim.
2. Add Prosecco first. Then Aperol. Then soda water.
3. Stir once gently with a bar spoon from the bottom — this is the 3-2-1 rule: 3 parts Prosecco, 2 parts Aperol, 1 part soda.
4. The vivid orange colour should show through the ice — do not muddy it with excessive stirring.
5. NEGRONI SBAGLIATO VARIATION (Campari): replace Aperol with Campari, replace soda with Prosecco. Stir. More bitter, more celebratory.
---
Garnish: Half an orange wheel inside the glass; green olive on a pick (traditional Venetian style); sprig of rosemary
Temperature: 4–6°C; ice volume is critical — at least 5 cubes in a large glass

""",

9367: """RECIPE — Americano and Campari Soda (Classic Serves)
Yield: 1 cocktail | Glassware: Highball or rocks glass | Ice: Cubed
---
CAMPARI SODA:
45ml Campari (bitter aperitivo; 25% ABV)
90ml Fever-Tree Soda Water
Large ice cube, lemon slice
---
AMERICANO (first cocktail James Bond orders in Casino Royale):
30ml Campari
30ml Martini Rosso sweet vermouth
Soda water to top (60ml)
---
CAMPARI SODA:
1. Fill highball with ice. Add Campari.
2. Pour soda water gently — stir once at the base.
3. The vivid red-orange is unmistakeable — use clear glassware always.

AMERICANO:
1. Fill rocks glass or highball with ice. Add Campari and sweet vermouth.
2. Top with soda water. Stir once from the base.
3. Serve with a wide orange peel expressed over the top.
---
Garnish: Campari Soda — lemon slice pressed against glass; Americano — orange wheel and lemon twist
Temperature: 4–6°C

""",

9368: """RECIPE — Fernet-Branca and Coke (Buenos Aires Style)
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
60ml Fernet-Branca (aromatic amaro; 39% ABV — the bartender's handshake spirit)
120ml Coca-Cola (original formula — this combination is the national drink of Argentina)
Squeeze of lime (optional — adds brightness)
---
1. Fill highball with ice. Add Fernet-Branca.
2. Pour Coca-Cola slowly down the inside of the glass — preserve carbonation.
3. Stir once from the base only. Do not agitate.
4. Squeeze of lime optional — not traditional but cuts the bitterness.
5. FERNET DIGESTIF SERVE: 30ml Fernet-Branca neat in a small glass at room temperature after a rich meal — the most traditional Italian use.
---
HANKY PANKY (bartender cocktail using Fernet): 45ml gin + 45ml sweet vermouth + 7.5ml Fernet-Branca. Stir 40 rotations. Strain into coupe. Orange twist.
Garnish: Lime wedge on rim; no garnish for Fernet neat
Temperature: Fernet and Coke: 4–6°C; Fernet neat: room temperature (18°C)

""",

9369: """RECIPE — Grand Marnier Sidecar
Yield: 1 cocktail | Glassware: Coupe | Ice: None (served up)
---
50ml Cognac VSOP (Rémy Martin VSOP or Hennessy VS)
25ml Grand Marnier Cordon Rouge (Cognac + bitter orange; 40% ABV)
20ml fresh lemon juice
Sugar rim (half — run lemon on rim, dip in caster sugar)
---
1. Half-rim the coupe with caster sugar — rub lemon wedge on half the rim only (traditional).
2. Combine Cognac, Grand Marnier, and lemon juice in shaker with ice.
3. Shake hard 12 seconds — bright, well-integrated, no sweetness imbalance.
4. Double-strain into sugar-rimmed coupe.
5. GRAND MARGARITA VARIANT: replace Cognac with tequila Blanco, add 15ml agave syrup. Same technique.
---
Garnish: Orange twist expressed and laid on the rim
Temperature: 5–7°C; the Sidecar was created at Harry's Bar, Paris, 1920s — it's a civilised drink, not a cold drink

""",

9370: """RECIPE — White Russian (Kahlúa Classic)
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
45ml vodka (Ketel One or Grey Goose — neutral, clean)
22.5ml Kahlúa coffee liqueur (16% ABV, dark, sweet — do NOT substitute generic coffee liqueur)
30ml double cream or heavy whipping cream (poured over slowly for the float)
---
1. Fill rocks glass with large cube or 2–3 regular cubes.
2. Add vodka. Add Kahlúa. Stir once.
3. Pour cream SLOWLY over the back of a bar spoon — it floats on the surface.
4. Serve unstirred — the layered dark and white is the signature visual.
5. The guest stirs it themselves as they drink — or doesn't.
6. BLACK RUSSIAN: same recipe, omit cream. Serve on ice in a rocks glass.
---
Garnish: No garnish — the layered two-tone visual IS the presentation; coffee bean floated on cream for premium service
Temperature: 6–8°C; the cream float will temper the chill slightly over drinking time

""",

9376: """RECIPE — Baileys Irish Coffee
Yield: 1 serve | Glassware: Irish coffee glass or wide heatproof mug | Ice: None
---
45ml Baileys Original Irish Cream (17% ABV — original only; refrigerate after opening)
150ml hot, strong coffee (double espresso diluted to 150ml with hot water; or dark-roast filter)
30ml soft whipped cream (lightly whipped to soft peaks — pourable consistency)
1 tsp brown sugar (optional — Baileys is already sweet)
---
1. Pre-warm glass with hot water. Discard.
2. Pour hot coffee and Baileys into the glass. Add sugar if using. Stir.
3. CREAM FLOAT: pour softly whipped cream over the back of a warm spoon held just above the surface.
4. The cream must float — if it sinks, the cream is too cold or too stiff.
5. Do NOT stir before drinking — sip through the cream layer. The temperature contrast (hot coffee below, cool cream above) is the drink's architecture.
---
Garnish: Grated nutmeg through a fine sieve over the cream; optional: Valrhona cocoa powder dusted
Temperature: Coffee at 80°C; cream layer at 12°C; the contrast is the point

""",

9377: """RECIPE — Limoncello Spritz (Southern Italian Summer Drink)
Yield: 1 cocktail | Glassware: Large wine glass or highball | Ice: Cubed
---
30ml limoncello (Pallini Limoncello or Villa Massa — Sorrentine lemon, made from sfusato lemons; 26–30% ABV)
90ml Prosecco (Mionetto Brut — dry, to balance the limoncello's sweetness)
60ml sparkling water (Fever-Tree Soda Water)
5ml fresh lemon juice
---
1. Fill large wine glass with ice. Add limoncello and lemon juice.
2. Pour Prosecco gently — tilt glass, pour down the inside.
3. Top with soda water. Stir once from the base — do not agitate bubbles.
4. LIMONCELLO SOUR: 45ml limoncello + 20ml lemon juice + 10ml simple syrup + egg white. Dry shake → wet shake → double strain into coupe. Lemon wheel.
---
Garnish: Lemon wheel; sprig of fresh thyme or basil (botanical lift); candied lemon peel spiral
Temperature: 4–6°C; limoncello must be served ice-cold (store in freezer)

""",

9378: """RECIPE — Rusty Nail (Drambuie and Scotch)
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
45ml Scotch whisky (Johnnie Walker Black Label or Chivas Regal 12yr — blended, smooth)
25ml Drambuie (Scotch + heather honey + herbs; 40% ABV)
---
1. Place large ice cube in rocks glass.
2. Pour Scotch over ice. Then add Drambuie.
3. Stir gently 10 rotations — Drambuie is viscous and settles; stir just enough to integrate.
4. Allow 2 minutes for ice to temper before drinking.
5. BALMORAL VARIANT (lighter): add 5ml fresh lemon juice. The acidity lifts the honey-richness.
6. SINGLE MALT VERSION: 45ml Glenfiddich 12yr + 20ml Drambuie. More complex and aromatic.
---
Garnish: Lemon twist expressed over the drink and dropped in; optional — thin apple slice for fruit-forward Rusty Nail
Temperature: 8–12°C; the Rusty Nail is a contemplative drink — slow sipping over 10–15 minutes

""",

9379: """RECIPE — Classic Cosmopolitan (Cointreau Version)
Yield: 1 cocktail | Glassware: Martini glass or large coupe | Ice: None (served up)
---
45ml vodka citron (Absolut Citron or Ketel One Citroen)
22.5ml Cointreau (premium triple sec; 40% ABV — do NOT use generic triple sec)
15ml fresh lime juice (key lime preferred — thinner skin, more aromatic)
30ml cranberry juice (Ocean Spray 100% — not cocktail blend; use just enough for colour, not taste)
---
1. Combine all ingredients in shaker with ice.
2. Shake hard 15 seconds — the citrus and cranberry need full integration.
3. Double-strain into chilled martini glass through fine sieve.
4. The correct colour is pale pink-rose — NOT dark cranberry red (that's too much cranberry).
5. COINTREAU SIDECAR: 50ml Cognac + 25ml Cointreau + 20ml lemon juice. Shake. Coupe. Orange twist.
---
Garnish: Flamed orange peel (hold orange peel skin-side-down over the drink, light a match between the peel and glass, squeeze — the orange oil ignites briefly, caramelising on the surface)
Temperature: 5–6°C; serve in a pre-chilled glass

""",

9380: """RECIPE — Hugo Spritz (St-Germain and Prosecco)
Yield: 1 cocktail | Glassware: Large wine glass | Ice: Cubed
---
30ml St-Germain elderflower liqueur (20% ABV — the "bartender's ketchup": use sparingly)
90ml Prosecco (dry; Lunetta Brut or La Marca)
60ml sparkling water (Fever-Tree)
8 fresh mint leaves
1 lime wedge
---
1. Fill wine glass with ice. Add lime wedge and gently bruised mint leaves.
2. Pour St-Germain over the ice.
3. Add Prosecco slowly — tilt glass, pour down the inside.
4. Top with sparkling water. Stir once at the base.
5. Do not over-use St-Germain — its floral sweetness dominates if over-poured. 20–25ml is the correct range.
---
HUGO MOCKTAIL: 25ml elderflower cordial + 90ml sparkling water + 60ml soda + mint + lime. Same method.
Garnish: Mint sprig pressed against the inside of the glass (visual presentation); lime wheel; edible flower (optional)
Temperature: 4–6°C; Hugo Spritz is a summer aperitivo — serve in warm weather, outdoors

""",

9386: """RECIPE — The Aviation (Maraschino Cocktail)
Yield: 1 cocktail | Glassware: Coupe | Ice: None (served up)
---
45ml dry gin (Plymouth Gin — the original; OR Hendrick's for floral)
15ml Luxardo Maraschino liqueur (cherry distillate; 32% ABV — NOT cherry syrup)
22.5ml fresh lemon juice
7.5ml crème de violette (Rothman & Winter — gives the cocktail its pale violet colour; OMIT for a drier Aviation)
---
1. Combine all ingredients in shaker with ice.
2. Shake 12 seconds. The cocktail needs full integration — maraschino is dense.
3. Double-strain into chilled coupe through fine sieve.
4. With crème de violette: the cocktail is a pale lavender-blue — named for the colour of the sky.
5. Without: pale yellow, slightly drier, closer to the original 1916 recipe (Hugo Ensslin, NYC).
---
Garnish: Luxardo Maraschino cherry on a cocktail pick (the real cherry in syrup, NOT a neon-red one); expressed lemon twist discarded
Temperature: 5–6°C; the Aviation is one of the great pre-Prohibition cocktails — treat it as such

""",

9387: """RECIPE — Trinidad Sour (Angostura-Forward Cocktail)
Yield: 1 cocktail | Glassware: Coupe | Ice: None (served up)
---
30ml Angostura bitters (the LARGEST ingredient — not a typo; 44.7% ABV, aromatic, spiced)
22.5ml Orgeat (almond syrup — Monin or Fee Brothers)
22.5ml fresh lemon juice
22.5ml rye whiskey (Bulleit Rye or Rittenhouse 100 Proof)
---
1. Combine all in shaker with ice.
2. Shake hard 15 seconds — Angostura has strong tannins that need aeration to soften.
3. Double-strain into chilled coupe.
4. The cocktail is a deep amber-brown with complex spice, almond, citrus balance.
5. Created by Giuseppe González at Clover Club, Brooklyn, 2009. Proof that bitters are a spirit.
---
ANGOSTURA SERVICE NOTE: the 'Angostura Sour' (standard bitters use): 3 dashes Angostura in any sour adds complexity without dominating. A rye whiskey + lemon + honey sour with 5 dashes Angostura is a bartender's benchmark drink.
Garnish: No garnish — the deep amber colour in a clean coupe is sufficient
Temperature: 5–6°C; the Trinidad Sour challenges preconceptions — present it without explanation initially

""",

9388: """RECIPE — Sloe Gin Fizz
Yield: 1 cocktail | Glassware: Collins glass | Ice: Cubed
---
45ml sloe gin (Sipsmith Sloe Gin — 29% ABV; or homemade: see below)
20ml fresh lemon juice
15ml simple syrup (or honey syrup for floral version)
60ml soda water
30ml egg white (optional — creates a thick foam top)
---
HOMEMADE SLOE GIN: 500g sloe berries (pricked) + 250g sugar + 750ml gin (Gordon's or Tanqueray). Seal and shake every 2 days. Strain after 3 months. Dark ruby, warming, plummy.
---
1. Dry shake (no ice): sloe gin, lemon, syrup, and egg white 15 seconds. Emulsify the white.
2. Add ice. Shake again 10 seconds — chill.
3. Strain into Collins glass with ice.
4. Top with soda water — pour slowly; foam will rise.
5. Without egg white: simply shake, strain, top. Simpler, equally good.
---
Garnish: Lemon wheel draped over foam; fresh or dried sloe berries on a pick; mint sprig
Temperature: 5–7°C; best made in early winter when sloe berries are freshly picked

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
    print(f"Done. {len(RECIPES) - errors} Spirits (selective) recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
