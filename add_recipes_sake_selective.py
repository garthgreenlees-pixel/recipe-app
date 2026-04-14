#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# Sake & East Asian — service/cocktail entries only; production entries do NOT get recipes
RECIPES = {

9411: """RECIPE — Sake Service Protocol (Temperature Guide)
Yield: 1 serve | Glassware: Ochoko (cold) or tokkuri + ochoko (warm) | Ice: None
---
100ml sake (varietal per occasion):
- JUNMAI DAIGINJO: 8–12°C (refrigerator cold)
- GINJO: 10–15°C (light chill)
- JUNMAI: 15–20°C (room temp or warm)
- HONJOZO: can serve warm (nurukan 40–45°C)
- FUTSUSHU (table sake): warm (atsukan 55°C)
---
COLD SERVICE (reishu):
1. Store sake refrigerated. Pour into chilled ochoko or wine glass.
2. Use a Burgundy glass for premium ginjo — aromatics lift with warming.
3. 60ml is the standard serve in a restaurant context; 100ml for izakaya.

WARM SERVICE (nurukan):
1. Pour sake into tokkuri ceramic flask. Set flask in 50°C water bath for 5 minutes.
2. Target temperature: 40–45°C for nurukan (hand-warm). Never microwave — creates harsh notes.
3. Pour into pre-warmed ochoko. Serve immediately; tokkuri cools rapidly.

---
Garnish: No garnish; the vessel IS the presentation — use quality ceramics for premium sake
Temperature: Match serving temperature to sake type and season — cold in summer, warm in winter

""",

9412: """RECIPE — Junmai Daiginjo Premium Service (Fine Dining)
Yield: 1 serve | Glassware: White wine Burgundy glass (Riedel) or traditional kikichoko | Ice: None
---
80ml Junmai Daiginjo (Dassai 39 Polished, Kubota Manju, or Hakkaisan Junmai Daiginjo)
---
TASTING PROTOCOL:
1. Serve at 8–12°C — slightly below refrigerator temperature is ideal.
2. Use a Burgundy-shaped wine glass: the bowl shape traps the delicate ginjo-ka (fruity floral aroma).
3. Pour to 1/3 of the glass — allow ample space for swirling and nosing.
4. Swirl gently (never aggressively). Junmai Daiginjo: look for rice polish-thin viscosity.
5. Nose: ginjo-ka = fresh melon, pear, lychee, and white flower notes from highly polished rice.
6. Sip: clean, pure, mineral. The finish should be long and rice-elegant, not sweet.
FOOD PAIRING: delicate white fish sashimi, lightly marinated scallop, oyster on the half shell, chilled tofu.
---
Garnish: No garnish; a small dish of wasabi-pickled cucumber on the side for pairing
Temperature: 8–12°C; never warm Junmai Daiginjo — high polish aromatics volatilise at heat

""",

9413: """RECIPE — Nigori Sake Cocktail (Unfiltered, Cloudy)
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Large cube
---
60ml nigori sake (Kiku-Masamune Nigori or Mio Sparkling Nigori; cloudy white, unfiltered)
20ml yuzu juice (or 15ml fresh lime + 5ml fresh orange juice)
10ml simple syrup (1:1)
Shake of kosher salt (optional — enhances the rice umami)
---
1. IMPORTANT: shake nigori sake bottle gently before opening — the rice solids settle.
2. Combine nigori, yuzu (or lime/orange), syrup, and salt in shaker with ice.
3. Shake hard 10 seconds — the rice solids froth with aeration.
4. Strain over large ice cube in rocks glass. The drink will be white and creamy.
5. TRADITIONAL SERVE: simply pour chilled nigori into rocks glass with ice. Let the cloudiness speak.
---
Garnish: Thin yuzu wheel (or thin lime wheel); toasted sesame seeds floated
Temperature: 5–7°C; nigori should be served very cold — the cold emphasises the creamy texture

""",

9414: """RECIPE — Chilled Summer Amazake (Ginger and Citrus)
Yield: 2 serves (400ml) | Glassware: Tall glass | Ice: Cubed
---
200ml cold amazake (Marukome Koji Amazake — rice and koji only, no added sugar; or homemade)
150ml cold sparkling water or cold yuzu soda
1 tsp freshly grated ginger (or ½ tsp ginger juice)
5ml fresh yuzu juice (or lemon juice)
Pinch of sea salt
---
1. Stir amazake well before measuring — rice sediment settles.
2. Combine amazake, ginger, and yuzu juice in a glass. Stir.
3. Add ice. Top with sparkling water — pour slowly to maintain bubbles.
4. Pinch of salt enhances the natural sweetness of the koji fermentation.
5. Drink immediately — amazake oxidises quickly once opened.
---
Garnish: Slice of fresh ginger; yuzu peel curl; black sesame seeds scattered on top
Temperature: 4–6°C; summer amazake is a traditional post-festival drink in Japan — served ice-cold from street stalls

""",

9415: """RECIPE — Mirin-Based Cocktail (Tama Mirin Service)
Yield: 1 cocktail | Glassware: Nick & Nora or small coupe | Ice: None
---
30ml hon-mirin (true mirin — Mikawa Mirin or Hinode Hon Mirin; 14% ABV, sweet, complex)
20ml Junmai sake
15ml fresh yuzu juice
5ml lemon juice
Pinch of sea salt
Thyme sprig (steeped in mirin 5 minutes for herbaceous note — optional)
---
1. Combine mirin, sake, yuzu, lemon, and salt in mixing glass with ice.
2. Stir 30 rotations — mirin is viscous and needs stirring rather than shaking to prevent over-dilution.
3. Strain into chilled coupe.
4. NOTE: only use hon-mirin (true mirin). Mirin-fu choumiryo (mirin-style condiment) is not a beverage — it contains salt.
5. TASTING NOTE: hon-mirin has natural sweetness, umami, and subtle rice character. This cocktail balances its sweetness with yuzu acidity.
---
Garnish: Yuzu twist expressed over the glass and draped on rim; single gold leaf for premium service
Temperature: 4–6°C; serve in a pre-chilled glass

""",

9416: """RECIPE — Makgeolli Makgeopong (Makgeolli Soju Bomb)
Yield: 1 serve | Glassware: Makgeolli bowl (daepo) | Ice: None
---
180ml fresh makgeolli (Wolhwa, Jipyong, or Nongmin — chilled; unpasteurised preferred)
30ml soju (Chamisul Fresh or Jinro — 16–25% ABV)
CLASSIC SERVE: 200ml makgeolli neat in bowl, shaken gently to mix cloudiness
---
TRADITIONAL SERVE (preferred):
1. Shake makgeolli container gently — rice sediment settles continuously.
2. Pour 200ml into a wide, shallow ceramic bowl (daepo).
3. The cloudiness, faint effervescence, and milky white colour are the quality indicators.
4. Serve alongside jeon (Korean pancakes) — makgeolli is inseparable from anju food pairing.

MAKGEOPONG BOMB:
1. Pour makgeolli into bowl. Drop a small glass of soju into the bowl.
2. The mix clouds further and becomes slightly more alcoholic and carbonated.
3. Drink in one continuous pour.
---
Garnish: No garnish; small dish of kimchi jeon (kimchi pancake) or haemul pajeon is the required accompaniment
Temperature: 4–6°C; makgeolli is always served cold — fresh bottles from the fridge

""",

9417: """RECIPE — Shaoxing Rice Wine Sour (Cocktail)
Yield: 1 cocktail | Glassware: Coupe or Nick & Nora | Ice: None (served up)
---
50ml aged Shaoxing rice wine (Pagoda brand Yellow Rice Wine — 8 year; 15–18% ABV)
20ml fresh lemon juice
10ml rock candy syrup (bing tang; or simple syrup)
15ml fresh egg white (for foam — optional but traditional foam texture)
3 drops black sesame bitters (or Angostura)
---
1. Dry shake all ingredients (no ice): shake hard 15 seconds. Egg white emulsification is critical.
2. Add ice to shaker. Shake 10 more seconds — chill without over-dilution.
3. Double-strain into chilled coupe through cocktail strainer and fine sieve.
4. Allow foam to settle 10 seconds into a white, smooth head.
5. Drop 3 bitters dots onto foam. No need to draw a pattern — minimalist Chinese aesthetic.
---
Garnish: Single sesame seed cluster on the foam; thinly sliced pickled lotus root on the rim (optional)
Temperature: 5–7°C; Shaoxing wine is nutty, sherry-like, and pairs with egg white beautifully

""",

9418: """RECIPE — Plum Wine Spritz (Umeshu Soda)
Yield: 1 serve | Glassware: Highball | Ice: Cubed
---
45ml umeshu (Choya Extra Years, or Clearspring Japanese Plum Wine; 10–13% ABV)
120ml cold sparkling water (Fever-Tree Soda Water or Perrier)
10ml fresh lemon juice
---
CLASSIC HIGHBALL:
1. Fill highball with ice. Add umeshu.
2. Squeeze lemon. Pour sparkling water slowly down the inside of the glass.
3. Do not stir — the sweet plum floats and mingles naturally.
4. A pickled ume plum from the jar placed in the glass is the traditional service touch.

UMESHU ROCKS:
60ml umeshu over a large ice cube in a rocks glass. Nothing else. This is the formal way.
---
Garnish: Pickled ume plum in the glass (direct from the jar used in production); shiso leaf; lemon twist
Temperature: 4–6°C; umeshu is sweet — cold temperature and sparkling water provide balance

""",

9433: """RECIPE — Suntory Toki Japanese Whisky Highball (Haibōru)
Yield: 1 cocktail | Glassware: Tall thin highball (frozen) | Ice: Large clear cubed or hand-carved sphere
---
45ml Suntory Toki blended malt whisky (OR Nikka From the Barrel for richer version)
135ml Suntory The Premium Malt's soda water (or Fever-Tree Soda Water)
Ratio: 1:3 whisky to soda water (strict at leading Japanese bars)
---
1. GLASS PREPARATION: fill highball glass with ice water. Leave 1 minute. Discard. Add clear ice cubes.
2. WHISKY: pour 45ml over ice. Stir 13 times (the traditional Suntory bar number — clockwise).
3. CARBONATION: pour soda water slowly down a bar spoon held against the inside of the glass.
4. Final stir: 3 rotations only. Stop — do not agitate carbonation further.
5. The haibōru should be crystal-clear, highly carbonated, and precisely balanced.
---
Garnish: No garnish at traditional Japanese bars; a lemon twist is acceptable in a Western context
Temperature: 3–5°C; the colder the better — Japanese bars shave ice to exact dimensions for heat management

""",

9435: """RECIPE — Saketini (Sake Cocktail)
Yield: 1 cocktail | Glassware: Martini glass or Nick & Nora | Ice: None
---
45ml Junmai or Ginjo sake (Ozeki Dry Sake or Gekkeikan Organic; clean, dry)
20ml dry vermouth (Dolin Dry; can reduce to 10ml for drier serve)
Optional: 5ml yuzu liqueur (Yuzuri or Roku Yuzu for citrus lift)
---
DRY METHOD (stirred):
1. Chill mixing glass with ice water. Discard.
2. Fill mixing glass with ice. Add sake, vermouth, and yuzu liqueur.
3. Stir 40 rotations — cold, clear, diluted correctly.
4. Strain into chilled martini glass.
5. The sake martini should be translucent, not cloudy — use filtered (clear) sake, not nigori.

WET SHAKE METHOD (for more dilution and air):
- Shake all ingredients with ice. Double-strain into chilled coupe.
---
Garnish: Cucumber ribbon instead of olive (Japanese aesthetic — cleaner, more appropriate to sake's delicacy); lemon twist for citrus saketini
Temperature: 5–6°C in pre-chilled glass

""",

9437: """RECIPE — Shochu Sour (Izakaya Style)
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Cubed
---
60ml mugi (barley) shochu (Iichiko Silhouette or Towari — 25% ABV; clean, light)
25ml fresh lemon juice (or yuzu if available)
15ml honey syrup (2:1 honey:hot water, cooled)
Soda water to top (approx. 60ml)
---
1. Fill rocks glass with ice. Add shochu, lemon juice, and honey syrup.
2. Stir briefly from the base — 10 rotations.
3. Top with soda water. One more stir at the base.
4. CHUHAI VARIANT (izakaya classic): shochu + canned lemon soda (Mitsuya Cider) — no mixing needed. Equal parts.
5. SHOCHU MOJITO: 60ml imo (sweet potato) shochu + 15ml lime + 10ml sugar + 8 mint leaves + soda water. Muddle mint with lime and sugar first, then add shochu and ice.
---
Garnish: Lemon wheel; fresh mint; thin cucumber slice for yuzu variant
Temperature: 4–6°C; shochu sour is the everyday bar drink of Japan — made quickly, drunk fresh

""",

9452: """RECIPE — Sparkling Sake (Awa Sake) Service
Yield: 1 serve | Glassware: Champagne flute or coupe | Ice: None
---
100ml awa sake (certified: Dassai Sparkling Junmai Daiginjo, Mio Sparkling Sake by Takara, or Sequoia Sake Co. Sparkling)
OR: Sparkling Nigori (Gekkeikan Zipang or Kikusui Junmai Ginjo Sparkling)
---
SERVICE PROTOCOL:
1. Store awa sake cold (4–6°C) and upright. NEVER shake — CO₂ is secondary-ferment produced.
2. Open by removing the foil cap, then gently lift the crown cap while holding the bottle at an angle over a sink.
3. Let the initial foam settle. Pour slowly into a tilted flute — same as Champagne service.
4. The mousse (foam) should be fine and persistent — a sign of quality in-bottle fermentation.
5. PAIRING: sparkling sake pairs with oysters, light sashimi, edamame, tempura, and soft goat cheese.
---
Garnish: No garnish in flute; for a celebration serve, a sakura (cherry blossom) petal floated if seasonal
Temperature: 4–6°C; serve immediately — sparkling sake loses carbonation faster than Champagne

""",

9453: """RECIPE — Ruou De Cocktail (Vietnamese Rice Spirit)
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Cubed
---
45ml Vietnamese ruou de (rice liquor; 29.5% ABV — Halico brand) OR substitute Thai rice whisky (Mekhong 35% ABV) if unavailable
20ml fresh lime juice
15ml simple syrup
8 fresh mint leaves
Soda water (60ml)
---
1. Muddle mint and syrup gently in shaker base — bruise, do not shred.
2. Add ice, ruou de, and lime juice. Shake 8 seconds.
3. Pour (don't strain — keep mint) into ice-filled rocks glass.
4. Top with soda water. Stir once from the base.
5. This is a Vietnamese-style mojito — the rice spirit's subtle funk and clean heat are ideal with citrus-mint.
---
TRADITIONAL SERVE: shot of ruou de at room temperature in a small ceramic cup alongside a pho or rice dish.
Garnish: Lime wedge; fresh mint sprig; lemongrass stalk as a stirrer (traditional Vietnamese presentation)
Temperature: 4–6°C for cocktail; room temperature for traditional straight serve

""",

9454: """RECIPE — Bokbunja Royale (Korean Black Raspberry Wine Cocktail)
Yield: 1 cocktail | Glassware: Champagne flute or coupe | Ice: None
---
30ml Bokbunja-ju (Korean wild black raspberry wine — Bohae or Munbae brand; 15–19% ABV)
10ml crème de cassis (optional — amplifies the blackberry note)
80ml Brut sparkling wine (Cava or Prosecco; or Champagne for premium)
---
1. Chill flute. Add bokbunja-ju to the base of the flute.
2. Add crème de cassis if using.
3. Pour sparkling wine slowly down the inside of the tilted flute.
4. The bokbunja sinks and creates a deep magenta-to-pink gradient.
5. Do not stir — let the gradient form naturally.
---
TRADITIONAL SERVE: 60ml bokbunja-ju served chilled in a small wine glass, neat, with a cheese plate or dark chocolate.
Garnish: 3 fresh blackberries or blueberries dropped in; dried rose petal floated; no garnish for traditional serve
Temperature: 6–8°C; bokbunja-ju is highly aromatic — do not serve too cold

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
    print(f"Done. {len(RECIPES) - errors} Sake (selective) recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
