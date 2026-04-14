#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# Wine category — ONLY sangria, mulled wine, and spritz-adjacent entries get recipes
# Grape variety and regional descriptions do NOT get recipes
RECIPES = {

9044: """RECIPE — Red Wine Sangria (Malbec Base)
Yield: 1.5 litres (6 serves) | Glassware: Large wine glass | Ice: Cubed
---
750ml Malbec (Clos de los Siete or Trivento Reserve — robust, fruity; good for sangria)
150ml brandy (Torres 10yr or Cardenal Mendoza — Spanish brandy; or Cognac VS)
100ml orange juice (fresh-squeezed)
50ml Cointreau or triple sec
2 tbsp raw cane sugar or agave nectar
1 orange, thinly sliced
1 lemon, thinly sliced
1 green apple, cored and sliced thinly
1 cinnamon stick
Soda water to top (150–200ml per jug)
---
1. Combine sliced fruit, cinnamon, sugar, orange juice, and brandy in a large jug. Stir to dissolve sugar.
2. Add Malbec and Cointreau. Stir gently — don't crush the fruit.
3. Refrigerate minimum 2 hours, ideally overnight. The longer the maceration, the better the integration.
4. To serve: add ice to glass. Pour sangria, including some fruit.
5. Top each glass with a splash of soda water (25ml). Stir once.
---
Garnish: Orange and lemon slices in the glass; cinnamon stick in the jug; mint sprig for service
Temperature: 4–6°C; sangria must be made ahead — serving immediately produces a flat, disconnected drink

""",

9155: """RECIPE — Classic Champagne Cocktail (Belle Époque)
Yield: 1 cocktail | Glassware: Champagne flute or coupe | Ice: None
---
100ml Champagne (Billecart-Salmon Brut NV or Pol Roger Brut NV — top-quality matters; the sugar cube amplifies impurities in cheap wine)
1 white sugar cube
2 dashes Angostura bitters
15ml Cognac (VSOP — Rémy Martin or Courvoisier; optional but traditional)
---
1. Chill flute in freezer 5 minutes. Dry with lint-free cloth.
2. Place sugar cube in the base of the flute.
3. Dash 2 drops Angostura bitters directly onto the sugar cube — it will absorb and turn brown-red.
4. Add Cognac (if using) over the cube.
5. Pour Champagne slowly down the inside of the tilted flute.
6. Watch: the sugar cube dissolves slowly over 5–10 minutes, releasing continuous streams of bubbles (bead streams). The bitters bloom through the wine as it dissolves.
---
Garnish: Orange twist expressed over the surface and laid across the rim; brandied cherry (optional)
Temperature: 8°C; the Champagne Cocktail dates to 1862 — it is a slow, contemplative drink, not a fast pour

""",

9156: """RECIPE — Aperol Spritz (with Prosecco)
Yield: 1 cocktail | Glassware: Large wine glass (stemmed) | Ice: Cubed (generous)
---
90ml Prosecco (Mionetto Prestige Treviso Brut, Bisol Crede Valdobbiadene, or Ruffino — dry is essential)
60ml Aperol (11% ABV; orange, rhubarb, and gentian bitter aperitivo)
30ml Fever-Tree Soda Water
---
GOLDEN RATIO: 3 parts Prosecco : 2 parts Aperol : 1 part soda water (the canonical Venetian recipe)
---
1. Fill wine glass generously with ice — this is non-negotiable; the glass must be cold.
2. Add Prosecco first. Then Aperol. Then soda water.
3. Stir gently once from the bottom using a long spoon — just enough to combine, not enough to dissipate bubbles.
4. The vivid orange-gold should be clear and sparkling — not cloudy or over-mixed.
5. TEMPERATURE CRITICAL: Prosecco must be ice-cold. Warm Prosecco makes a flat, sweet spritz.
---
Garnish: Half an orange wheel pressed inside the glass; green olive on a metal pick (traditional Veneto aperitivo style)
Temperature: 4–6°C; ice volume keeps the drink cold for 15–20 minutes of drinking time

""",

9158: """RECIPE — Provence Rosé Sangria (Summer Pitcher)
Yield: 1.5 litres (6 serves) | Glassware: Large wine glass | Ice: Cubed
---
750ml Provence rosé (Château Miraval, Whispering Angel, or Miraval — pale, dry, crisp)
100ml elderflower liqueur (St-Germain) OR elderflower cordial (Belvoir, 50ml)
60ml dry white vermouth (Dolin Blanc)
Juice of 1 lemon (25ml)
1 white peach, pitted and thinly sliced
200g strawberries, hulled and halved
½ cucumber, thinly sliced
200ml sparkling water (to top, per serve)
---
1. Combine rosé, elderflower liqueur, vermouth, lemon juice, and all fruit in a large glass jug.
2. Stir gently. Do not crush the fruit — bruising oxidises the white peach quickly.
3. Refrigerate minimum 1 hour (2 hours ideal). Rosé sangria macerates faster than red.
4. To serve: fill glass with ice. Ladle sangria and fruit into glass. Top with 25–30ml sparkling water.
---
Garnish: Cucumber ribbon draped over the glass rim; strawberry on rim; fresh mint sprig; edible rose petal floated
Temperature: 4–6°C; serve in clear glass to show the blush-pink colour

""",

9173: """RECIPE — Porto Tónico (Port and Tonic Spritz)
Yield: 1 cocktail | Glassware: Copa de Balon or large wine glass | Ice: Cubed
---
60ml white port (Niepoort White, Ramos Pinto White, or Churchill's White — dry style preferred)
OR: 45ml tawny port (10yr Ramos Pinto) for richer version
150ml Fever-Tree Tonic Water (or Fever-Tree Elderflower Tonic for floral complexity)
5ml fresh lemon juice
---
1. Fill copa de balon or large wine glass with generous ice.
2. Add white port. Add lemon juice.
3. Pour tonic water slowly down a bar spoon against the glass interior.
4. Stir once at the base — do not over-mix.
5. PORTO COLADO VARIANT: 45ml white port + 30ml coconut water + 60ml pineapple juice + tonic. Tropical.
---
Garnish: Lemon wheel in the glass; mint sprig; dried orange slice; for tawny version — cinnamon stick
Temperature: 4–6°C; Port and Tonic is Portugal's national outdoor drink; serve in summer at outdoor bars

""",

9174: """RECIPE — Sherry Cobbler (1830s Classic)
Yield: 1 cocktail | Glassware: Tall goblet or Collins glass | Ice: Crushed (essential)
---
90ml Oloroso or Amontillado sherry (Lustau Los Arcos Amontillado or Toro Albalá Oloroso — dry, nutty, complex; 17–18% ABV)
10ml simple syrup (1:1)
2 orange slices
1 slice pineapple (optional — historical recipe)
---
1. In a shaker: muddle orange slices with simple syrup. Add pineapple if using.
2. Add sherry and a scoop of crushed ice. Shake briefly (5–8 seconds) — just to chill, not over-dilute.
3. Pour directly into goblet or Collins glass packed with crushed ice.
4. The crushed ice creates the 'snow cone' visual that was revolutionary when introduced in 1830s America.
5. REBUJITO VARIANT (Feria de Abril, Seville): 60ml Manzanilla sherry + 120ml Sprite or 7-Up + ice in highball. Stir. Mint sprig. No muddling.
---
Garnish: Fresh orange and lemon slice; seasonal berries; sprig of fresh mint pressed into the crushed ice; paper or bamboo straw (the Cobbler popularised the drinking straw in the 1800s)
Temperature: 2–4°C; crushed ice is essential — it's the defining texture of the Cobbler

""",

9176: """RECIPE — Peach Bellini (Prosecco and White Peach)
Yield: 1 cocktail | Glassware: Champagne flute | Ice: None
---
50ml white peach purée (fresh: blend 2 white peaches, strain; or Boiron frozen peach purée)
100ml Prosecco (Cipriani Bellini Prosecco or Ruggeri Q Valdobbiadene Brut — dry, fine bubbles)
Optional: 5ml peach liqueur (Belle de Brillet or Mathilde Peach) for intensified peach flavour
---
HARRY'S BAR, VENICE — original Bellini method (Giuseppe Cipriani, 1948):
1. Chill flute in freezer. Dry.
2. Add white peach purée to base of flute — 50ml exactly.
3. Pour Prosecco VERY slowly down the inside of the tilted flute.
4. The purée and Prosecco create a pink-peach gradient that rises naturally.
5. Do NOT stir — the bubbles carry the purée upward over the next 2–3 minutes.
---
NOTE: Yellow peach = inferior; only white peach (pesca bianca) is correct for a Bellini.
NOTE: Champagne is NOT traditional — Harry's Bar used Prosecco. Champagne makes a 'Champagne Bellini', a different drink.
Garnish: No garnish — the gentle peach-pink colour in a clean flute is the aesthetic
Temperature: 6–8°C; Prosecco must be cold; purée should be room temperature for proper mixing gradient

""",

9220: """RECIPE — Negroni Sbagliato (Lambrusco or Sparkling Wine)
Yield: 1 cocktail | Glassware: Large wine glass or rocks glass | Ice: Cubed
---
45ml Campari (25% ABV)
45ml Martini Rosso sweet vermouth
45ml sparkling red wine — traditionally Lambrusco Grasparossa (Villa di Corlo, or Lini 910 Labrusca)
OR: Prosecco (Brut) for a lighter, cleaner version
---
1. Fill rocks glass or wine glass with ice.
2. Add Campari. Add Martini Rosso.
3. Stir 5 rotations to integrate.
4. Pour sparkling wine slowly — use Lambrusco for the traditional version (darker, fruitier) or Prosecco for a lighter contemporary sbagliato.
5. One final stir at the base only.
6. "Sbagliato" means "mistaken" in Italian — legend has it a bartender reached for Prosecco instead of gin while making a Negroni. The happy accident became iconic.
---
Garnish: Large orange slice or orange wheel in the glass (the Negroni family always takes orange); sprig of rosemary
Temperature: 4–6°C; Lambrusco should be well-chilled — it is naturally low-tannin and loses fruit character if warm

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
    print(f"Done. {len(RECIPES) - errors} Wine (selective) recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
