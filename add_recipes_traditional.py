#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

RECIPES = {

10128: """RECIPE — Pulque Curado de Tamarindo (Flavoured Pulque)
Yield: 1 litre (4 serves) | Glassware: Clay cup (jarro de barro) or lowball | Ice: Cubed
---
1 litre fresh pulque (from pulquería or fermented agave sap, 3–8% ABV naturally)
100g tamarind paste, dissolved in 150ml warm water and strained
50g sugar or piloncillo (adjust to taste — pulque is naturally sour)
Pinch of sea salt
Optional: 1 tsp ground cinnamon, 2 tbsp chilli powder (for spiced curado)
---
1. Combine fresh pulque with tamarind liquid, sugar, and salt in a large clay jug.
2. Stir vigorously with a wooden spoon — pulque foams naturally and must be incorporated.
3. Taste: tart, funky, slightly thick. The curado should balance pulque sourness with tamarind sweet-sour.
4. Refrigerate 1 hour minimum before serving — improves integration.
5. Pour into clay cups over ice. Stir before each pour as pulque separates.
---
Garnish: Tajín rim; chilli-dusted tamarind ball on rim; lime wedge
Temperature: 4–6°C; pulque is always served cold and consumed same-day — it continues to ferment

""",

10129: """RECIPE — Chicha Morada (Purple Corn Punch, Non-Fermented)
Yield: 1.5 litres (6 serves) | Glassware: Tall glass | Ice: Cubed
---
500g purple Peruvian corn (maíz morado — whole cobs or dried kernels)
2 litres water
1 cinnamon stick
5 whole cloves
1 quince, chopped (or 1 green apple)
100g caster sugar (or to taste)
Juice of 3 limes (approx. 75ml)
---
1. Combine purple corn, water, quince, cinnamon, and cloves in large pot.
2. Bring to boil, reduce heat, and simmer 45 minutes. The liquid turns deep burgundy-purple.
3. Strain through fine sieve. Add sugar while hot — stir to dissolve.
4. Cool completely. Add lime juice only when cold (hot lime goes bitter).
5. Serve over ice in tall glasses. Stir before pouring — sugar settles.
---
Garnish: Dried purple corn kernel on rim; lime wheel; cinnamon stick in glass
Temperature: 4–6°C; chicha morada is always served cold

""",

10130: """RECIPE — Traditional Kava Preparation (Waka Grade)
Yield: 1 litre (4–6 shells) | Glassware: Half-coconut shell (tanoa) | Ice: None
---
60g waka-grade kava powder (lateral root, Fiji; Wakacon or Kalm with Kava brand)
1 litre cold water (cold water = smoother extraction; hot water increases bitterness)
Muslin straining bag or cheesecloth
---
1. Place kava powder in straining bag. Submerge in cold water in a large bowl.
2. Knead, squeeze, and work the bag for 10–15 minutes continuously — this extracts kavalactones.
3. Lift and squeeze the bag repeatedly. The water should turn light tan-brown.
4. Remove bag. The kava is ready — drink within 2 hours for best potency.
5. Serve in half-coconut shells. Guests clap once before receiving, once after emptying (traditional protocol).
---
Garnish: No garnish — kava ceremony is stripped back; the shell IS the vessel
Temperature: Room temperature or slightly cool (18–22°C); cold kava loses some ritual character

""",

10131: """RECIPE — Yerba Maté (Traditional Gourd Ceremony)
Yield: Continuous serve from gourd | Glassware: Calabaza gourd with bombilla metal straw | Ice: None
---
3–4 tablespoons loose yerba maté (Cruz de Malta or Taragüi — Argentine; with stems for milder flavour)
Hot water at 70–80°C (NOT boiling — boiling water scalds the herb and turns it bitter)
Optional: small orange rind for flavour; 1 tsp honey for sweeter serve
---
1. Fill the gourd 2/3 full with dry yerba maté. Cover the opening with palm, invert, and shake — brings fine dust to the top.
2. Tilt the gourd to one side, creating a mound of maté on one half.
3. Pour a small amount of cold water into the empty space at the bottom — this protects the herb from heat-shock.
4. Insert the bombilla into the wetted area. Do not move it again.
5. Pour hot water (70–80°C) into the empty space. The maté mound stays dry at the top.
6. The server (cebador) drinks the first bitter preparation, then refills and passes clockwise.
---
Garnish: Gourd may be decorated traditionally; orange peel or mint added to the dry herb layer for chimarro or tereré style
Temperature: 70–80°C; never boiling — this is the cardinal rule of maté preparation

""",

10132: """RECIPE — Ethiopian Coffee Ceremony (Buna)
Yield: 3 rounds (3 small cups per person) | Glassware: Small ceramic handleless cups (jebena buna cups) | Ice: None
---
3 tbsp green unroasted Ethiopian coffee beans (Yirgacheffe or Sidama variety)
500ml cold water
1–2 tsp sugar per cup (caster or traditional nib-ib sugar cane)
Optional: cardamom pods, rue herb (tena adam) for incense/blessing
---
1. Wash green beans in cold water. Dry-roast in a pan over medium-high heat, stirring constantly.
2. Roast until dark brown (not black) and aromatic — 10–15 minutes. Grind to fine-medium powder.
3. Add ground coffee to jebena (clay pot) with cold water. Place on charcoal fire or low gas flame.
4. Bring to boil slowly. Once boiling, reduce heat and let froth settle. Repeat twice.
5. Pour through strainer into cups in one continuous stream from height — creates the head of foam.
6. FIRST ROUND (Abol): strongest, most sacred. SECOND (Tona): lighter. THIRD (Baraka): lightest, a blessing.
---
Garnish: Frankincense burned on charcoal nearby; popcorn or kolo (roasted barley) served alongside; rue sprig in the ceremony space
Temperature: Serve very hot (80–85°C) in small cups; ceremony is unhurried — 30–45 minutes

""",

10158: """RECIPE — Tibetan Butter Tea (Po Cha)
Yield: 1 serve (250ml) | Glassware: Wooden or ceramic bowl-style cup | Ice: None
---
500ml water
1 tbsp pu-erh tea leaves (or 2 strong pu-erh tea bags) — brewed strong
1–2 tbsp yak butter (or high-quality unsalted cultured butter — Kerrygold works)
¼ tsp sea salt
50ml fresh milk (or 2 tbsp full-fat milk powder)
---
1. Steep pu-erh leaves in 200ml boiling water for 5–7 minutes to make a very strong dark tea.
2. Strain tea into a traditional churn (dongmo) or blender. The churn is essential to the original method.
3. Add butter, salt, and milk. Churn or blend vigorously 1 minute — emulsification is key.
4. The result should be creamy, pale tan, and frothy — like a savoury latte.
5. Serve immediately in pre-warmed bowl-cups. Refill continuously throughout the meal.
---
Garnish: No garnish — po cha is a sustenance drink, not decorative
Temperature: Serve at 70–75°C; high altitude demands warming drinks that hold heat

""",

10159: """RECIPE — Moroccan Atay (Mint Tea)
Yield: 1 pot (3–4 small glasses) | Glassware: Small Moroccan decorative glass (tea glass) | Ice: None
---
1 tbsp loose Chinese gunpowder green tea (Nana Tea — do not substitute with other green teas)
Large bunch fresh spearmint (about 30g — Moroccan nana mint, not peppermint)
3–4 tbsp caster sugar (tea is traditionally very sweet — adjust to guest preference)
500ml boiling water
---
1. Warm the teapot with boiling water. Discard.
2. Add gunpowder tea. Pour 100ml boiling water. Swirl for 10 seconds. Pour off — this is the "washing" step (removes bitterness and dusty notes).
3. Add fresh mint to the pot. Add sugar. Pour remaining boiling water over everything.
4. Steep 3–5 minutes. Taste: strong, sweet, mintfresh. Adjust sugar if needed.
5. POUR FROM HEIGHT: hold pot 30cm above the glasses. This aerates the tea, creates foam, and cools slightly. Pour, then pour back into pot once. Serve from height again for final pour.
---
Garnish: Fresh mint sprig stood in each glass; a date or msemen (flatbread) on the side
Temperature: Serve hot (75–80°C); the ritual of pouring from height is non-negotiable

""",

10160: """RECIPE — Russian Bread Kvass (Khlébny Kvas)
Yield: 2 litres | Glassware: Tall mug or glass | Ice: None (served cool)
---
300g dark rye bread (Borodinsky or dark sourdough), sliced and toasted until dark-crusted
2 litres boiling water
100g sugar
10g active dry yeast (dissolved in 2 tbsp warm water)
Handful raisins (optional — for natural carbonation)
2 tbsp fresh mint (optional)
---
1. Toast bread until very dark (near burnt) — this is the source of kvass's colour and caramel flavour.
2. Pour boiling water over toasted bread in a large jar. Cool to room temperature.
3. Strain bread. Add sugar to liquid — stir to dissolve.
4. When liquid is at 25°C, add yeast. Stir. Add raisins and mint.
5. Ferment loosely covered at room temperature 8–12 hours. Taste from 8 hours.
6. When pleasantly tangy and slightly fizzy, strain and refrigerate. Stops fermentation.
---
Garnish: Sprig of fresh dill or mint; lemon slice
Temperature: 4–8°C; kvass is served cold, never warm

""",

10161: """RECIPE — Palm Wine Service (West African)
Yield: 1 serve | Glassware: Carved wooden cup or lowball | Ice: None
---
200ml fresh palm wine (raphia palm or oil palm — from local tapper; consumed same-day)
---
SERVICE PROTOCOL — Palm wine is extremely time-sensitive:
1. Fresh (tapped that morning): 1–3% ABV, sweet, yeasty, slightly effervescent. Serve immediately.
2. 6–12 hours: 4–7% ABV, more sour, more carbonated. Still excellent.
3. 24 hours: 8%+ and very sour — approaching palm wine vinegar. Still consumed but acquired taste.
4. Pour carefully — palm wine has natural sediment. Tilt the vessel gently, do not shake.
5. The first pour (palm wine head/foam) is considered the best — serve this to guests of honour.
---
Garnish: No garnish; presented in natural vessel — the drink speaks for itself
Temperature: Cellar cool (14–18°C) for fresh wine; never refrigerate — cold halts fermentation abruptly

""",

10162: """RECIPE — Amazake (Japanese Sweet Fermented Rice)
Yield: 1 litre (4 serves) | Glassware: Small ceramic cup | Ice: None (or iced version)
---
200g short-grain Japanese white rice (cooked)
100g dried rice koji (Aspergillus oryzae cultured rice; available at Japanese grocery)
500ml warm water
Pinch of salt
Optional: 1 tsp grated fresh ginger (traditional garnish/digestive)
---
1. Cook rice, allow to cool to 55–60°C — warm, not hot.
2. Combine warm rice with rice koji and warm water in a clean vessel.
3. Maintain at 55–60°C for 8–12 hours (rice cooker on 'keep warm' setting is ideal).
4. Stir every 2 hours. The mixture will become sweet, creamy, and porridge-like.
5. Blend to smooth consistency if desired, or leave chunky for traditional style.
6. Heat to 85°C to stop fermentation. Cool and refrigerate.
---
Garnish: Grated fresh ginger on top; yuzu zest; pinch of pink salt
Temperature: Serve warm (60°C) in winter; chilled (4°C) in summer — both are traditional

""",

10178: """RECIPE — Tuak (Indonesian Rice Wine) Service
Yield: 1 serve | Glassware: Small bamboo cup or ceramic shot glass | Ice: None
---
100ml fresh tuak (palm or rice wine from local production; 4–14% ABV depending on fermentation stage)
---
CEREMONIAL SERVICE PROTOCOL:
1. Tuak is served at room temperature in the Batak/Dayak tradition — never chilled.
2. Pour gently to avoid disturbing the natural sediment (cloudy lees).
3. The cloudiness indicates active live culture — this is not a flaw but a sign of freshness.
4. First portion poured onto the ground as offering to ancestors before drinking begins.
5. For flavoured serving: dissolve 1 tsp palm sugar and ¼ tsp ground cinnamon into a fresh pour.
---
SIMPLE PALM SUGAR VARIANT: 100ml tuak + ½ tsp palm sugar + pinch of cinnamon. Stir gently.
---
Garnish: No garnish in traditional context; dried clove floated for premium service presentation
Temperature: Room temperature (22–28°C) — traditional Borneo and Sumatra serve

""",

10179: """RECIPE — Jamaican Ginger Beer (The Real Thing)
Yield: 1.5 litres (6 serves) | Glassware: Highball | Ice: Cubed
---
150g fresh ginger root, grated (unpeeled for maximum flavour)
250g granulated cane sugar
1.2 litres water (400ml boiling + 800ml cold)
Juice of 3 limes (approx. 75ml)
½ tsp active dry yeast (for fermentation)
2 whole cloves
1 stick cinnamon
---
1. Boil 400ml water with sugar, cloves, and cinnamon. Stir until dissolved. Remove from heat.
2. Add grated ginger. Steep 30 minutes covered. Strain through fine sieve — press ginger hard.
3. Combine strained liquid with remaining cold water and lime juice. Cool to 25°C.
4. Dissolve yeast in 2 tbsp warm water. Add to ginger liquid. Stir well.
5. Bottle in swing-top or plastic bottles (allows pressure check). Ferment 24–48 hours at room temp.
6. Refrigerate when carbonated. Open carefully.
---
Garnish: Lime wedge; crystallised ginger; Angostura bitters float (the Jamaica tradition)
Temperature: 4°C; Jamaican ginger beer is serious — fiery, sweet-tart, potently gingery

""",

10180: """RECIPE — O-Miki Sake Ceremony (Kanpai Service)
Yield: 1 serve | Glassware: Ochoko (ceramic sake cup) or masu (wooden box) | Ice: None
---
100ml premium junmai sake (Dassai 39 or Hakutsuru Junmai) for cold service
OR for warm service (nurukan):
100ml junmai sake, heated tokkuri flask in 50°C water bath for 5 minutes → target 40–45°C
---
CEREMONIAL PROTOCOL:
1. Never pour sake for yourself — always pour for the person next to you, and receive with both hands.
2. For cold serve (reishu): chill sake to 8–12°C. Pour into ochoko with two hands.
3. For warm serve (nurukan): heat in tokkuri flask (ceramic flask) set in 50°C water. Never microwave.
4. The kanpai toast: raise ochoko at chest height, make eye contact, say "kanpai," then sip.
5. Do not set down an empty ochoko — the host will refill it before it's empty.
---
Garnish: No garnish in ochoko; masu sometimes sprinkled with pinch of coarse salt on the corner
Temperature: Cold (reishu): 8–12°C; Warm (nurukan): 40–45°C; Hot (atsukan): 55°C

""",

10181: """RECIPE — Basque Cider Sangria (Sidra-Style Punch)
Yield: 1 litre (4–6 serves) | Glassware: Wide wine glass or jug | Ice: Cubed
---
750ml dry traditional cider (Basque Txakoli-style sidra, or Aspall English dry cider)
1 green apple and 1 pear, cored, thinly sliced
1 orange, thinly sliced into rounds
50ml Cointreau or triple sec (optional for alcoholic version; omit for NA — add extra OJ)
150ml fresh orange juice
3 tbsp raw honey
2 cinnamon sticks
Handful of mint leaves
---
1. Combine orange juice, honey, cinnamon, and Cointreau in a jug. Stir to dissolve honey.
2. Add fruit slices. Pour cider gently down the side of the jug — preserve carbonation.
3. Stir once from the base. Do not crush the fruit.
4. Refrigerate 30–60 minutes — fruit infuses the cider.
5. Serve over ice; ladle fruit into each glass.
---
Garnish: Apple and pear slices in the glass; mint sprig; cinnamon stick
Temperature: 4–6°C; traditional Basque sidra is poured from height (escanciado) to aerate

""",

10182: """RECIPE — Umeshu Highball (Japanese Plum Wine Serve)
Yield: 1 serve | Glassware: Highball | Ice: Cubed
---
45ml umeshu (Choya Extra Years plum wine, or homemade — see below)
90ml sparkling water (Fever-Tree Soda Water or Mitsuya Cider)
Squeeze of lime (5ml)
HOMEMADE UMESHU BASE: 1kg green ume plums + 500g rock sugar + 1.8L shochu or vodka → seal, rest 6 months
---
1. Fill highball with ice. Add umeshu over ice.
2. Pour sparkling water slowly down the back of a bar spoon.
3. Squeeze lime. Do not stir — the sweet plum layers naturally with the sparkling water.
4. For a classic serve (not highball): 60ml umeshu over ice in rocks glass, 1 ume plum fruit from the jar placed in glass.
---
Garnish: Pickled ume plum in the glass (from the jar used to make umeshu); shiso leaf; lime twist
Temperature: 4–6°C; umeshu is sweet — the sparkling water and lime balance it

""",

10203: """RECIPE — Georgian Amber Wine Service (Qvevri Style)
Yield: 1 serve | Glassware: Traditional ceramic or terracotta cup, or wide-bowled red wine glass | Ice: None
---
125ml Georgian amber wine — Rkatsiteli or Mtsvane variety, skin-contact (Pheasant's Tears, Lagvinari, or Ramaz Nikoladze)
---
SERVICE PROTOCOL:
1. Amber wine is served at 14–16°C — slightly cooler than red wine, slightly warmer than white.
2. No decanting required — skin-contact whites are stable and aromatic from pour.
3. Pour slowly. Colour ranges from pale gold to deep amber-orange — always show in natural light.
4. Swirl and nose: expect dried apricot, beeswax, tannic grip, walnut, and oxidative notes (not a flaw — intentional).
5. TRADITIONAL TOAST (mravalamziani): say "gaumarjos" (to victory) before drinking. The host always toasts first.
6. FOOD PAIRING: Georgian churchkhela (walnut-grape), sulguni cheese, lobiani (bean bread), badrijani nigvzit (walnut-stuffed aubergine).
---
Garnish: No garnish in glass; serve with walnuts and a piece of guda or sulguni cheese on the side
Temperature: 14–16°C; never serve cold like a white wine or warm like a red

""",

10204: """RECIPE — Turkish Raki Service (Lion's Milk)
Yield: 1 serve | Glassware: Tall, narrow Raki glass (bardak) + small water glass | Ice: Served separately
---
45ml Turkish raki (Yeni Raki, Tekirdag, or Bursa — anise-flavoured double-distilled grape spirit; 45% ABV)
45ml cold still water (added tableside)
2–3 ice cubes (added last, if desired)
---
1. Pour raki into tall glass. This is the "lion" — golden-clear.
2. Pour cold water slowly into the raki glass. Watch the louche (milky white cloud form) — this is "lion's milk" (aslan sütü).
3. Add ice last — do NOT put ice in first (ruins the louche sequence).
4. Swirl gently. Aroma of anise blooms immediately — this is the moment.
5. Serve alongside: beyaz peynir (white cheese), melon, zeytun (olives), midye (mussels), cacık (yoghurt-cucumber).
---
Garnish: No garnish in the glass; the meze table IS the garnish
Temperature: Raki chilled to 8°C before pouring; water at 4°C; ice added to personal preference

""",

10205: """RECIPE — Makgeolli Service (Korean Rice Wine)
Yield: 1 serve | Glassware: Ceramic bowl (daepo) or traditional makgeolli bowl | Ice: None
---
200ml makgeolli (Wolhwa or Jipyong brand — fresh, refrigerated; white, milky, 6–8% ABV)
---
SERVICE PROTOCOL:
1. Makgeolli separates naturally — shake the bottle gently (or stir the jug) before pouring.
2. Serve in a wide, shallow bowl (daepo) or a traditional earthen cup — not tall glasses.
3. The cloudiness and slight effervescence are essential qualities; clear makgeolli = pasteurised, inferior.
4. Serve at 4–6°C — very cold cuts through the natural sweetness.
5. PAIRING (anju): haemul pajeon (seafood pancake), kimchi pancake, dubu kimchi (tofu and kimchi), gamja-jeon (potato pancake). Food is non-negotiable with makgeolli.
---
SIMPLE VARIANT — Makgeolli Soju Mix (Somaek-style): 150ml makgeolli + 30ml soju. Stir once.
Garnish: No garnish; doily or bamboo mat under the bowl is traditional
Temperature: 4–6°C; fresh unpasteurised makgeolli keeps only 1–2 weeks refrigerated

""",

10206: """RECIPE — Lebanese Arak Serve (The Milky White)
Yield: 1 serve | Glassware: Short tumbler (ka'as) | Ice: Added last
---
30–45ml arak (Kasr El Helou, Ksarak, or Brun — anise and grape double-distilled; 50–60% ABV)
60ml very cold water (equal to or slightly more than arak — ratio is personal)
3 ice cubes
---
1. Pour arak into glass first. It is clear.
2. Add cold water — watch the louche (white cloud). This is the hallmark of the serve.
3. Add ice cubes LAST — ice after water is the correct sequence.
4. Never mix water into ice first — this prevents the louche from forming properly.
5. Do NOT dilute heavily — arak at 50%+ needs the ritual proportion: 1:2 to 1:1 arak:water max.
6. Always eat with arak — the meze table (hummus, tabbouleh, kibbeh, fattoush) accompanies every session.
---
Garnish: No garnish in glass; the louche is the spectacle
Temperature: Arak stored at room temperature; water at 4°C; serve the final drink at 8–12°C

""",

10207: """RECIPE — Mezcal Oaxacan Service (Palenque Style)
Yield: 1 serve | Glassware: Copita (small terracotta cup) | Ice: None
---
50ml single-origin mezcal (Del Maguey San Luis del Rio, Vago Espadin en Barro, or Alipús)
---
PALENQUE SERVICE PROTOCOL:
1. Pour mezcal into copita — a small clay cup that adds earthy mineral quality to the nose.
2. Do NOT add ice to quality mezcal. Cold suppresses the smoke and agave character.
3. Let the mezcal rest in the copita 2 minutes — the clay warms slightly and releases aromatics.
4. Take a small sip. Let it rest on the tongue. The smoke comes second, after the agave fruit.
5. Eat sal de gusano (worm salt — salt, chilli, ground agave worm) on an orange slice between sips.
6. The orange-sal de gusano combination is the traditional Oaxacan accompaniment.
---
Garnish: Orange slice dusted with sal de gusano; fresh cucumber slice (cooling contrast to smoke)
Temperature: Room temperature (18–22°C); mezcal is never chilled

""",

10238: """RECIPE — Baijiu Moutai Ceremony (Ganbei Toast)
Yield: 1 serve | Glassware: Small shot glass (baijiu cup) or thimble | Ice: None
---
30ml Kweichow Moutai sauce-aroma baijiu (53% ABV) OR Wuliangye strong-aroma (52% ABV)
---
GANBEI CEREMONY PROTOCOL:
1. Pour baijiu for others — never for yourself. The host pours for all guests first.
2. Hold the glass in your right hand, supported by left hand. Lower your glass slightly below the host's — a sign of respect.
3. Make eye contact. Say "ganbei" (干杯 — literally "dry cup"). It means to finish the glass completely.
4. Drink in one motion — no sipping for ganbei toasts. Turn glass upside down to prove it's empty.
5. The host drinks first at each toast. A designated drinker (代喝, dài hē) can drink on behalf of non-drinkers.
---
TASTING NOTE (non-ceremony): For appreciation, sip slowly from a narrow wine glass at 20°C. Nose: soy, dark fruit, earthy. Palate: complex, warming, lingering.
Garnish: No garnish; serve alongside cold dishes (凉菜, liángcài) — century egg, cold tofu, braised pork
Temperature: Room temperature (20°C); never chilled, never warmed

""",

10239: """RECIPE — Peruvian Pisco Sour (El Original)
Yield: 1 cocktail | Glassware: Coupe or Old Fashioned glass | Ice: None (served straight up or rocks)
---
60ml Peruvian pisco (QuebrAnta grape — Macchu Pisco or Campo de Encanto Acholado; 40% ABV)
30ml fresh lime juice (key lime, limón de Pica preferred)
22ml simple syrup (1:1, caster sugar)
30ml fresh egg white (one medium egg white — approx. 30ml)
3 dashes Amargo Chuncho bitters (Peruvian aromatic bitters; or Angostura if unavailable)
---
1. Dry shake (no ice): combine pisco, lime, syrup, and egg white. Shake hard 15 seconds — emulsifies the white.
2. Add ice to shaker. Shake again 10 seconds — chill and dilute.
3. Double-strain into chilled coupe through cocktail strainer and fine sieve.
4. Allow foam to settle 10 seconds — it rises to a thick, stable white head.
5. Dash 3 drops Chuncho bitters onto the foam in a triangle pattern. Do not stir.
---
Garnish: The bitters pattern on the foam IS the garnish — the Peruvian tradition
Temperature: Serve at 5–7°C; the egg white foam is temperature-sensitive — deliver immediately

""",

10240: """RECIPE — Aquavit Skål (Nordic Service with Herring)
Yield: 1 serve | Glassware: Tulip-shaped aquavit glass (snaps glass) | Ice: None
---
40ml aquavit (Linie Aquavit — barrel-aged, caraway and dill; or Aalborg Taffel — unaged, purer)
Cold beer chaser (Carlsberg or Tuborg Export — traditional accompaniment)
---
NORDIC DRINKING RITUAL (Skål):
1. Chill aquavit to 2–4°C in freezer — it should be ice-cold, almost syrupy.
2. Pour 40ml into tulip glass. It should show faint oiliness when tilted.
3. Hold glass at chest height. Make eye contact with each person at the table.
4. Say "skål" — look each person in the eye individually (essential — avoiding eye contact is impolite).
5. Drink in one motion at the table's agreed moment. Chase immediately with a sip of cold beer.
6. FOOD: always paired with gravlax, pickled herring, open-faced rye bread (smørrebrød), or cold potato.
---
Garnish: No garnish in snaps glass; lemon-dill gravlax slice served alongside on dark rye
Temperature: 2–4°C; aquavit must be served ice-cold — it becomes almost viscous at serving temp

""",

10241: """RECIPE — Traditional Mead (Honey Wine, First Fermentation)
Yield: 4.5 litres | Glassware: Wine glass or goblet | Ice: None
---
1.35kg raw honey (wildflower or orange blossom; local, unfiltered preferred)
3.6 litres filtered water (room temperature — chlorine inhibits fermentation)
1 packet wine yeast (Lalvin 71B — fruit-forward; or EC-1118 for drier, crisper)
1 tsp yeast nutrient (Fermaid-O or DAP)
---
1. Sanitise all equipment with Star San solution.
2. Heat 1 litre water to 40°C. Dissolve honey gently — do not boil (destroys honey aromatics).
3. Combine honey water with remaining 2.6 litres room-temperature water in fermenter.
4. Target must temperature: 22–24°C. Add yeast nutrient.
5. Sprinkle or pitch yeast. Seal with airlock.
6. Ferment 14–28 days at 18–22°C. Rack into secondary vessel when bubbling slows.
7. Age 2–6 months minimum before bottling. Mead improves dramatically with age.
---
Garnish: In glass: honey drizzle on the rim; sprig of fresh thyme or rosemary (herbal mead style)
Temperature: Serve at 10–14°C for young mead; 14–16°C for aged traditional mead

""",

10242: """RECIPE — Lambic Gueuze Service (Spontaneous Fermentation)
Yield: 1 serve | Glassware: Wide-mouthed wine glass or lambic tulip | Ice: None
---
250ml gueuze (Cantillon Gueuze, 3 Fonteinen Oude Gueuze, or Tilquin Queuze — all 5–8% ABV)
---
SERVICE PROTOCOL:
1. Gueuze is served at 10–14°C — cellar temperature. Not ice-cold.
2. Open slowly: gueuze is highly carbonated (Champagne-like CO₂ pressure). Pour carefully.
3. Tilt the glass and pour gently against the side — head will form naturally, allow it.
4. Serve with the opened bottle so the guest can assess the label (blending year, brewery details).
5. KRIEK VARIANT: pour 200ml gueuze + 50ml kriek (cherry lambic) for a mixed serve.
6. FOOD PAIRING: aged Belgian cheese (Chimay, Orval), mussels, strong washed-rind cheese, charcuterie.
---
Garnish: No garnish in glass; serve with a fresh raw oyster alongside for the classic pairing
Temperature: 10–14°C; do not serve cold — cold suppresses the wild yeast complexity

""",

10287: """RECIPE — Umqombothi (South African Sorghum Beer)
Yield: 2 litres | Glassware: Traditional wooden cup or large enamel mug | Ice: None
---
500g sorghum meal (ground sorghum; from African grocery)
250g maize meal (mealie pap meal)
2 litres water (divided)
Optional: 2 tbsp sorghum malt (sprouted sorghum, dried and ground) for extra fermentation activity
---
1. Mix sorghum and maize meal with 500ml lukewarm water to form smooth paste.
2. Bring remaining 1.5 litres water to boil. Add meal paste gradually, stirring constantly.
3. Simmer 30 minutes, stirring — the porridge thickens and darkens.
4. Remove from heat. Cool to 30°C. Pour into clay or plastic fermentation vessel.
5. The natural wild yeasts in the sorghum begin fermentation. Loosely cover.
6. Ferment 24–48 hours at 25–30°C. Taste from 24 hours — sour, earthy, slightly fizzy.
7. Strain through large-holed sieve (umqombothi retains some texture — it is semi-thick).
---
Garnish: Served in community — passed from person to person in a shared container (ubuntu spirit)
Temperature: Room temperature (18–24°C); some prefer it cool from the shade. Never refrigerate.

""",

10288: """RECIPE — Mongolian Airag Service (Fermented Mare's Milk)
Yield: 1 serve | Glassware: Wooden bowl (airag bowl) or wide ceramic cup | Ice: None
---
200ml airag (fermented mare's milk; 0.5–2.5% ABV; sourced from Mongolian producers — extremely seasonal and regional)
---
NOTE: Airag cannot be easily replicated outside Central Asia, but kefir comes closest.
---
AIRAG APPROXIMATION (for non-steppe service):
200ml goat's milk kefir (Bionade Goat Kefir or homemade)
Small pinch of salt
Optional: drop of natural vanilla
---
AIRAG CEREMONIAL SERVICE:
1. Airag is offered to guests with two hands — both hands on the bowl, elbows slightly bent.
2. Receive with both hands or right hand supported by left — never one hand.
3. Take a small sip, or at minimum touch lips to bowl, even if you choose not to drink more.
4. Return bowl with both hands. Host refills continuously.
5. The host whips airag 3–5 times with a ladle before serving each round — essential to maintain carbonation.
---
Garnish: No garnish; serve alongside suutei tsai (Mongolian butter tea) and dried meat (borts)
Temperature: Slightly cool (12–16°C) — typically kept in shaded part of the ger

""",

10289: """RECIPE — Greek Ouzo Serve (The Proper Way)
Yield: 1 serve | Glassware: Small ouzo glass (narrow tumbler) | Ice: Separate dish
---
40ml ouzo (Plomari, Barbayanni, or Metaxa Ouzo 12 — anise and fennel, 37–46% ABV)
80ml very cold water (separate small jug)
Ice cubes (separate dish — guest adds own)
---
1. Pour ouzo into glass at room temperature — it is clear.
2. Add cold water slowly — the louche (white cloud) forms. This is non-negotiable.
3. Ratio: 1 part ouzo to 2 parts water is classical. More water = less intense, more food-friendly.
4. Add ice after water — the louche will be stable before chilling.
5. Always serve with meze: grilled octopus, tzatziki, spanakopita, feta, dolmades. Ouzo without food is tourist behaviour.
---
OUZO-BASED COCKTAIL (modern): 25ml ouzo + 15ml fresh lemon + 90ml sparkling water + ice → ouzo spritz.
Garnish: No garnish in the glass; thin slice of salted cucumber on the side (digestive pairing)
Temperature: Ouzo at room temp, water at 4°C; drink temperature 10–14°C

""",

10290: """RECIPE — Hungarian Pálinka Service (Fruit Brandy Tradition)
Yield: 1 serve | Glassware: Tulip-shaped spirit glass (100ml) | Ice: None
---
30–40ml aged pálinka (minimum 2-year barrel; Zwack Fütyülős Barack apricot pálinka, or Villány Sóly plum pálinka; 40–52% ABV)
---
TRADITIONAL SERVICE PROTOCOL:
1. Pálinka is served at room temperature — approximately 20°C.
2. Never add ice, water, or mixers — pálinka is appreciated neat, pure.
3. Pour into a tulip glass that traps aromatics. Do not use a shot glass.
4. Allow 1–2 minutes for the glass to warm slightly in your hands.
5. Nose before drinking: fresh fruit, dried fruit, subtle brandy heat. No burn.
6. Sip slowly. Pálinka should feel warm, not burning — quality is judged by smoothness.
7. TOAST: "Egészségünkre!" (To our health!) — eye contact required, never look away when toasting.
---
FOOD PAIRING: Lecsó (pepper-tomato stew), kolbász (paprika sausage), kürtőskalács (chimney cake) with apricot pálinka.
Garnish: Dried apricot on the side for apricot pálinka; dried plum for szilva; no garnish in the glass
Temperature: 18–22°C; never cold

""",

10291: """RECIPE — Calvados Trou Normand (Palate Cleanser)
Yield: 1 serve | Glassware: Small sorbet coupe or shot glass + dessert spoon | Ice: Sorbet
---
35ml Calvados (Pays d'Auge AOC — Boulard VSOP or Château du Breuil Fine; 40% ABV)
1 small scoop apple sorbet (or pear sorbet — approx. 50g)
---
1. Place a small scoop of apple sorbet in a chilled coupe or shallow bowl.
2. Pour Calvados slowly over the sorbet at the table — it should pool and begin melting the edges.
3. Serve immediately — the sorbet melts into the Calvados creating a semi-frozen palate cleanser.
4. Consumed between the fish and meat courses in Norman tradition.
5. CALVADOS NEAT (after-dinner): 40ml in brandy snifter at 18–20°C; swirl gently; note apple, pear, oak, honey.
---
Garnish: Thin dehydrated apple chip draped on sorbet; a few grains of fleur de sel (salt enhances apple)
Temperature: Sorbet at -4°C; Calvados at room temperature (18–20°C)

""",

10312: """RECIPE — Classic Caribbean Rum Punch (1-2-3-4 Ratio)
Yield: 1 serve | Glassware: Highball or rum punch glass | Ice: Cubed
---
30ml fresh lime juice (1 SOUR)
60ml simple syrup or grenadine (2 SWEET — 1 sugar: 2 fruit ratio)
90ml dark rum (Mount Gay Eclipse, Appleton Estate 8yr, or local island rum) (3 STRONG)
120ml cold water or pineapple juice (4 WEAK)
2 dashes Angostura bitters (a fifth: dash of bitters, traditional)
Pinch of grated nutmeg
---
1. Fill glass with ice. Add lime juice, then syrup or grenadine.
2. Add rum. Add cold water or pineapple juice.
3. Stir well from the bottom — integrate all components.
4. Add 2 dashes Angostura. Stir once more.
5. Grate fresh nutmeg over the top — this is the signature finishing touch across the Caribbean.
---
Garnish: Lime wheel; maraschino cherry; pineapple chunk on a pick; nutmeg — all traditional
Temperature: 4–6°C; punch is best cold and slightly diluted — ice volume matters

""",

10313: """RECIPE — The Scotch Dram (Traditional Service)
Yield: 1 serve | Glassware: Copita-style nosing glass or traditional tumbler | Ice: Optional (purist: none)
---
45ml single malt Scotch whisky (Glenfiddich 12yr for Highland; Laphroaig Quarter Cask for Islay smoke; Dalwhinnie for gentle approachability)
5–10ml still water (still, not sparkling; soft water preferred — Speyside: use local water)
---
1. Pour whisky into copita nosing glass. Observe colour — holds to the glass as 'legs' run down.
2. Add a few drops of water (not a full splash). Water opens up the whisky by lowering surface tension.
3. Nose in 3 stages: from 20cm, then 10cm, then at the rim. Never press nose into the glass.
4. Sip a small amount. Let it coat the full palate before swallowing.
5. Breathe out through the nose after swallowing — the retro-nasal finish is where the complexity lives.
---
ROB ROY VARIATION: 50ml Scotch + 25ml Martini Rosso + 2 dashes Angostura, stirred 40 rotations, coupe, Luxardo cherry.
Garnish: No garnish for a dram; maraschino cherry and orange twist for a Rob Roy
Temperature: Room temperature (18–20°C) for single malt; Rob Roy served at 5°C

""",

10314: """RECIPE — Goa Feni (Cashew) Service and Feni Sour
Yield: 1 cocktail | Glassware: Rocks glass | Ice: Cubed
---
FENI SOUR:
45ml cashew feni (first or double-distilled; Cazulo Premium Feni; 40–45% ABV)
20ml fresh lime juice
15ml palm jaggery syrup (or raw cane sugar syrup)
10ml fresh pineapple juice (optional — tropical bridge)
---
1. Combine all ingredients in shaker with ice.
2. Shake hard 10 seconds — feni needs aeration to reduce the raw spirit heat.
3. Strain into ice-filled rocks glass.
4. STRAIGHT FENI SERVE: 30ml feni neat in small ceramic cup at room temperature — traditional Goan style.
5. CLASSIC FENI COCKTAIL: feni + warm water + lime + jaggery — served post-meal as digestif.
---
Garnish: Lime wheel; cashew nut on a pick; pinch of red Goa pepper on the surface
Temperature: Feni neat at 20°C; Feni Sour at 5–7°C

""",

10315: """RECIPE — Irish Poitin Hot Toddy
Yield: 1 serve | Glassware: Heatproof glass mug or Irish coffee glass | Ice: None
---
40ml poitin (Glendalough Poitin Raw Spirit, Knockeen Hills, or Bán Poitin; 40–60% ABV)
20ml raw honey (or 1 tbsp)
15ml fresh lemon juice
200ml near-boiling water (90°C — just off boil)
2 whole cloves
1 cinnamon stick
1 slice fresh ginger
---
1. Pre-warm the glass with boiling water. Discard.
2. Add honey and lemon juice to warm glass. Add cloves, cinnamon, and ginger.
3. Pour poitin over the spices.
4. Top with hot water. Stir until honey dissolves.
5. Rest 1 minute — let the spices bloom and the poitin integrate with the heat.
---
Garnish: Lemon wheel with 2–3 cloves pushed into the skin floated on top; cinnamon stick stirrer; star anise
Temperature: Serve at 65–70°C; drink slowly — poitin is potent

""",

10316: """RECIPE — Russian Vodka Toast Service with Zakuski
Yield: 1 serve | Glassware: Small shot glass (ryumka) or flat-bottomed Russian shot | Ice: None
---
50ml vodka (Beluga Noble, Kauffman Private Collection, or Stolichnaya Elit — high-quality, clean; 40% ABV)
---
TOAST SERVICE PROTOCOL:
1. Chill vodka to -18°C in freezer — it becomes slightly viscous and silky.
2. Pour into small glass. Full pour — Russian tradition is to fill completely.
3. TOAST: "Za zdorovye!" (To health!). Everyone clinks glasses. Eye contact. Drink together in one motion.
4. After each shot, eat immediately — this is the zakuski culture:
   - Slice of rye bread with caviar (or butter + dill)
   - A thin slice of smoked salmon or sprat
   - A bite of gherkin (soleniy oguretz) — the most important zakuska
   - Pickled mushrooms (griby) or cold beet salad
5. Breathing on exhale after drinking, then biting the bread, was the traditional folk method to neutralise the burn.
---
Garnish: Gherkin on a small fork served alongside every glass; rye bread slice with dill butter on the side
Temperature: Frozen vodka at -18°C; serve immediately before it warms

""",

10342: """RECIPE — Swedish Glögg (Nordic Mulled Wine)
Yield: 1.5 litres (8–10 serves) | Glassware: Small heatproof mug with handle | Ice: None
---
750ml red wine (Shiraz or Merlot — don't use quality wine; use robust house red)
200ml aquavit or vodka (aquavit adds caraway; vodka adds strength without flavour)
100ml port (Ruby — adds sweetness and depth)
150g white sugar
1 cinnamon stick
10 cardamom pods, lightly cracked
8 whole cloves
Peel of 1 orange (remove white pith)
5cm piece fresh ginger, sliced
Optional: 10 whole almonds, 50g raisins (for serving in the glass)
---
1. Combine spices and orange peel in 100ml of the wine. Bring to simmer. Steep 30 minutes.
2. Add remaining wine and port. Warm to 75°C — do not boil.
3. Add sugar. Stir to dissolve. Taste and adjust.
4. Add aquavit or vodka off the heat — this preserves the spirit character.
5. Strain. Keep warm in a slow cooker or pot on lowest heat.
6. To serve: ladle into mugs. Drop 4–5 almonds and a few raisins into each mug.
---
Garnish: Cinnamon stick in mug; orange slice; blanched almonds floated
Temperature: Serve at 70–75°C; traditionally served outdoors in winter

""",

10343: """RECIPE — Caribbean Christmas Sorrel Punch (Hibiscus Rum Punch)
Yield: 2 litres (8–10 serves) | Glassware: Tall glass or punch cup | Ice: Cubed
---
100g dried sorrel (dried hibiscus flowers — same botanical; Caribbean term is sorrel)
1.5 litres boiling water
200g white sugar or brown sugar (adjust to taste)
5 whole cloves
3cm piece fresh ginger, sliced
250ml dark rum (Appleton Estate 12yr or Mount Gay Black Barrel) — optional or omit for NA version
Juice of 2 limes
---
1. Combine sorrel, cloves, and ginger in large heatproof jug. Pour boiling water over.
2. Steep 24–48 hours refrigerated for maximum colour and flavour (overnight minimum).
3. Strain through fine sieve. Add sugar — stir to dissolve in the cold liquid.
4. Add rum (if using) and lime juice. Taste: should be tart, spiced, floral.
5. Serve over ice in tall glasses.
---
Garnish: Lime wheel; fresh ginger slice; dried hibiscus flower floated; Christmas sprig of herbs
Temperature: 4–6°C; sorrel punch is a celebration drink — make in large batch, serve generously

""",

10344: """RECIPE — Kava Ceremony Cocktail (Hawaiian Interpretation)
Yield: 1 serve | Glassware: Half-coconut shell or lowball | Ice: None
---
40ml kava concentrate (Kalm with Kava Instant Kava — noble variety; 1 tbsp dissolved in 100ml water)
20ml coconut water
10ml fresh lime juice
10ml mango nectar or fresh mango juice
1 drop pandan extract (optional — Hawaiian floral note)
---
1. Prepare kava concentrate: dissolve instant kava in cold water, stir vigorously 2 minutes.
2. Combine kava concentrate, coconut water, lime juice, and mango. Stir.
3. Do not shake — kava should not be aerated.
4. Pour into shell or glass.
5. Perform the ceremonial clap: one clap before receiving, say "Bula!" (Fijian), one clap before drinking.
---
Garnish: Plumeria (frangipani) flower on rim; lime leaf floated; fresh mint sprig
Temperature: Room temperature or slightly cool (18–22°C)

""",

10345: """RECIPE — Kiddush Wine Service (Shabbat and Holiday)
Yield: 1 serve | Glassware: Silver kiddush cup (kos shel kiddush) or large wine glass | Ice: None
---
125ml kosher red wine (Herzog Cabernet Sauvignon, Carmel Selected, or Bartenura Moscato)
OR: 125ml kosher grape juice (Kedem) for children and abstainers
---
KIDDUSH PROTOCOL (Shabbat):
1. Pour wine to the brim — an overfull cup symbolises abundance and blessing.
2. Hold the cup in both hands cupped together (traditional) or in the dominant hand at chest height.
3. Recite the Kiddush prayer (the sanctification of wine and Shabbat).
4. After the blessing, drink at least a revi'it (approx. 86ml) of the wine — a meaningful amount, not a sip.
5. Share the wine with others at the table — pass the cup or pour from the bottle for each guest.
6. FOLLOW WITH: Motzi (bread blessing over two challah loaves, lightly salted). Wine and bread are always paired.
---
Garnish: No garnish — this is a holy vessel and ceremony; presentation of the silver cup itself is the ceremony
Temperature: Red wine at 16–18°C; grape juice at 6–8°C

""",

10346: """RECIPE — Cultural Beverage Pairing Flight (Master Framework)
Yield: 3 × 80ml serves | Glassware: 3 small tasting glasses | Ice: Per tradition
---
GLASS 1 — Bitter and Aperitivo (Pre-Meal): 80ml Crodino aperitivo + orange twist
GLASS 2 — Fermented and Sour (Mid-Meal): 80ml cloudy kefir OR kombucha, room temperature, no ice
GLASS 3 — Sweet and Settling (Post-Meal): 80ml chamomile honey cordial (2 tbsp honey syrup + 60ml chamomile tea), no ice
---
1. Prepare all three glasses in advance. Present on a wooden board with tasting cards.
2. Serve Glass 1 on the guest's arrival — bitter compounds prime the stomach for eating.
3. Serve Glass 2 mid-meal, alongside the main dish — fermented drinks aid digestion and complement savoury foods.
4. Serve Glass 3 after dessert — chamomile and honey calm digestion and close the meal.
5. Brief explanation of the cultural tradition each drink represents enhances the experience.
---
Garnish: Glass 1 — orange wheel; Glass 2 — lemon slice; Glass 3 — chamomile flower
Temperature: G1: 4°C; G2: room temperature; G3: 60°C (warm)

""",

10377: """RECIPE — Philippine Lambanog Cocktail (Coconut Sap Spirit Serve)
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
45ml lambanog (coconut sap spirit; 40–65% ABV — Vino Kulafu for commercial, or artisan from Quezon Province)
20ml fresh calamansi juice (or 15ml lime juice + 5ml orange juice as substitute)
15ml simple syrup
60ml fresh buko (young coconut) water
Splash of soda water
---
1. Combine lambanog, calamansi/lime, and syrup in shaker with ice.
2. Shake 8 seconds. Strain into ice-filled highball.
3. Add coconut water. Top with soda.
4. STRAIGHT SERVE: 30ml lambanog in small glass at room temperature — the tradition at fiestas.
---
Garnish: Calamansi half on rim; toasted coconut shavings; pandan leaf draped across the glass
Temperature: 5–7°C for cocktail; room temperature for traditional straight serve

""",

10378: """RECIPE — Lion's Paw (Sri Lankan Coconut Arrack & Ginger Beer)
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
45ml Rockland Ceylon Arrack (or Old Arrack; 40% ABV — coconut flower sap distillate, double-pot-still)
15ml fresh lime juice
10ml demerara syrup (2:1 sugar:water)
2 dashes Angostura bitters
120ml Bundaberg Ginger Beer (or spicy equivalent)
---
1. Fill highball with ice. Add arrack, lime juice, and demerara syrup.
2. Stir once from the base to integrate.
3. Pour ginger beer gently down the inside of the glass.
4. Add bitters. Do not stir — let the bitters float and aroma develop from the top.
5. The arrack's coconut-toffee character should meld with the ginger heat on the palate.
---
Garnish: Lime wedge; crystallised ginger on a pick; pandan leaf pressed against inside of glass (traditional Sri Lankan presentation)
Temperature: 4–6°C; arrack is tropical in character — serve cold

""",

10379: """RECIPE — Kir Royale (Champagne Ceremony Cocktail)
Yield: 1 cocktail | Glassware: Champagne flute | Ice: None
---
15ml crème de cassis (blackcurrant liqueur — Lejay or Gabriel Boudier; 15–20% ABV)
100ml Champagne (Billecart-Salmon Brut, Taittinger Brut Reserve, or Ruinart Blanc de Blancs)
OR: Crémant d'Alsace or Cava for a more casual serve
---
1. Chill flute in freezer 5 minutes or rinse with ice water. Dry with lint-free cloth.
2. Add crème de cassis to the cold dry flute — it sinks to the bottom.
3. Tilt flute at 45°. Pour Champagne slowly down the inside of the glass.
4. As Champagne mixes with cassis, it creates a rose-to-red gradient that rises to the surface.
5. Do not stir — let the carbonation carry the cassis upward naturally.
---
CHAMPAGNE SERVICE: 8–10°C; open by removing foil, twisting the cage 6 turns counterclockwise, holding the cork firm and rotating the bottle — not the cork. The cork should exhale with a quiet sigh, not a pop.
Garnish: 3 fresh or frozen blackcurrants dropped in; edible gold leaf for celebration
Temperature: 8–10°C; Champagne loses its magic above 12°C

""",

10380: """RECIPE — Chuflay (Bolivian Singani Highball)
Yield: 1 cocktail | Glassware: Highball | Ice: Cubed
---
60ml singani (Casa Real, Rujero, or Los Papayas — altitude-grown Muscat of Alexandria distillate; 40% ABV)
Juice of ½ lime (approx. 15ml)
120ml ginger ale (Schweppes Dry Ginger Ale; NOT ginger beer — the distinction matters)
2 drops Angostura bitters (optional)
---
1. Fill highball with ice. Add singani and lime juice.
2. Stir once to chill the base.
3. Pour ginger ale gently — do not stir again.
4. Add bitters. The aromatic top layer is part of the experience.
5. VARIANT — Singani Sour: 50ml singani + 25ml lemon + 15ml simple syrup + egg white, dry shake then shake with ice, double strain.
---
Garnish: Lime wheel; cocktail cherry; sprig of muña (Bolivian mountain mint — substitute regular mint)
Temperature: 4–6°C; singani is floral and elegant — do not mask with too much ginger ale

""",

10381: """RECIPE — Shochu Mizuwari (Water Serve)
Yield: 1 serve | Glassware: Tall glass (mizuwari glass) | Ice: Cubed (first the ice)
---
60ml shochu (Satsuma Honkoshi iimo shochu — sweet potato; or Iichiko Silhouette mugi barley shochu; 25% ABV)
90ml cold still water (soft water is preferred — Volvic or local soft mineral water)
---
MIZUWARI PROTOCOL:
1. Fill glass with ice. Add shochu. Stir 13 rotations (this is traditional — specific number).
2. Add one ice cube. Add water.
3. Stir 3 more rotations — do not over-stir.
4. OCHAWARI (tea-serve variant): replace water with warm bancha or mugicha (barley tea) — 80°C.
5. OYUWARI (hot water variant): pour shochu into warmed cup first, then add hot water at 70°C.
6. FOOD PAIRING: imo shochu with yakitori and grilled meats; mugi shochu with sashimi and light dishes.
---
Garnish: No garnish for mizuwari — purity is the aesthetic; lemon twist for modern bar context
Temperature: Mizuwari: 4–6°C; oyuwari: 60–65°C; ochawari: 55–60°C

""",

10407: """RECIPE — Grappa Tasting Service (Italian Pomace Spirit)
Yield: 1 serve | Glassware: Tulip-shaped grappa glass (chiaro) | Ice: None
---
30ml grappa (Nonino Cru Monovitigno Picolit — aged; or Nardini Bianca — unaged, floral; 37–50% ABV)
---
GRAPPA SERVICE PROTOCOL:
1. Unaged (bianca) grappa: serve at 8–10°C — slightly chilled to tame the raw alcohol.
2. Aged (riserva) grappa: serve at 14–18°C — room temperature to open oak and dried fruit.
3. Tulip glass is essential — traps aromatics. Never a shot glass.
4. Swirl gently. Nose from 15cm: pomace should express grape variety character (moscato: floral; nebbiolo: rose, tar).
5. Sip slowly. Grappa finishes long and warm — quality is judged by the length of the finish.
6. TRADITIONAL PAIRING: resentin (coffee cup rinsed with grappa — finished last after espresso); tiramisu; panna cotta.
---
Garnish: No garnish for classic service; a single dark chocolate square on the saucer is acceptable
Temperature: Bianca: 8–10°C; Riserva: 14–18°C — never ice, never room temperature for bianca

""",

10408: """RECIPE — Vietnamese Ruou Can (Communal Jar Rice Wine)
Yield: 2 litre jar (serves 6–10) | Glassware: Drinking bamboo straws in shared ceramic jar | Ice: None
---
1kg glutinous rice, soaked overnight and steamed until cooked
50g banh men (traditional Vietnamese yeast cake — dried and ground; from Vietnamese market)
2 litres water (added after initial fermentation)
---
1. Spread cooked glutinous rice in a thin layer on clean surface. Cool to 35–40°C.
2. Sprinkle ground banh men evenly over rice. Fold in gently to distribute.
3. Pack into a large clean jar. Seal and ferment at 28–30°C for 3–5 days.
4. Add 2 litres cold water to the fermented rice. Do not stir.
5. Ruou can is ready when the liquid is cloudy, slightly sweet, and mildly fizzy (3–7% ABV typically).
---
COMMUNAL SERVE: Gather around the jar. Insert bamboo straws — one per person. The ritual is to drink simultaneously. The host refills the jar with water as it empties; this cycle continues until the rice is exhausted.
Garnish: Jar decorated with red cloth or flowers for ceremony
Temperature: Room temperature (22–28°C); ruou can is a warm-climate ceremonial drink

""",

10409: """RECIPE — Natural Wine Pét-Nat Service (Pétillant Naturel)
Yield: 1 serve | Glassware: Burgundy wine glass or natural wine tumbler | Ice: None
---
125ml pétillant naturel (Frank Cornelissen Munjebel Bianco, Le Temps des Cerises Brut d'Alsace, or Domaine La Bohème Effervescence; 10–12% ABV)
---
SERVICE PROTOCOL:
1. Serve at 10–12°C — pét-nat is best cooler than still natural wines.
2. OPEN CAREFULLY: pét-nat bottles have crown caps (beer caps), not corks. Release slowly — significant CO₂ pressure.
3. Pét-nat is naturally cloudy from yeast sediment — do not decant. The cloudiness is integral.
4. Let the wine rest 2 minutes in the glass. The natural carbonation settles into fine bubbles.
5. Nose: wild yeast, apple, brioche, often a hint of cidery oxidation — these are qualities, not faults.
6. NATURAL WINE ETIQUETTE: if the wine smells like a barnyard or wet dog, it may be mousiness — this is a fault. A horse blanket note is acceptable; mousiness is not.
---
Garnish: No garnish; serve with a card noting the producer, vintage, and brief tasting note
Temperature: 10–12°C; keep bottle cold throughout service — pét-nat warms quickly

""",

10410: """RECIPE — Pomace Spirit Flight (Grappa / Marc / Orujo Comparison)
Yield: 3 × 20ml tasting pours | Glassware: 3 grappa tulip glasses | Ice: None
---
GLASS 1 — Italian: 20ml Poli Cleopatra Moscato Oro Grappa (aged, floral, delicate; 40% ABV)
GLASS 2 — French: 20ml Marc de Bourgogne (earthy, robust, rustic; 40–45% ABV)
GLASS 3 — Spanish/Portuguese: 20ml Orujo de Galicia (spicy, robust; or Portuguese aguardente bagaceira; 40%)
---
1. Serve in order of increasing intensity: grappa (lightest) → marc (middle) → orujo (most robust).
2. Use clean glasses for each — cross-contamination ruins the comparative exercise.
3. GRAPPA: serve at 10°C (slightly chilled). MARC: 14°C. ORUJO: 16°C.
4. Between each taste, cleanse the palate with still water and a small piece of plain bread.
5. Guide guests: note the grape variety in grappa vs. the regional terroir in marc vs. the wildness of orujo.
---
Garnish: Small card in front of each glass identifying the region and producer
Temperature: Ascending: 10°C → 14°C → 16°C

""",

10411: """RECIPE — Cedar Bark and Pine Needle Tea (Indigenous North American)
Yield: 500ml | Glassware: Ceramic or earthenware cup | Ice: None
---
1 handful young cedar branch tips (Western Red Cedar or Eastern White Cedar — fresh, green; NOT ornamental or toxic species; verify before foraging)
OR: 2 tbsp dried cedar leaf tea (from Indigenous-owned supplier — Raven Reads or similar)
500ml cold water
1 tsp raw honey or maple syrup (optional)
---
IMPORTANT: Only use Western Red Cedar (Thuja plicata) or Eastern White Cedar (Thuja occidentalis). Never use Yellow Cedar or Ornamental Cedars — toxic.
---
1. If using fresh cedar: rinse branch tips thoroughly with cold water.
2. Cold-infuse method (preferred for delicate cedar): combine cedar and cold water in jar. Refrigerate 6–12 hours.
3. Hot-brew method: bring water to simmer (not boil — preserves volatile aromatics). Add cedar. Steep 10 minutes off heat.
4. Strain through fine sieve. Add honey or maple syrup if desired.
5. Taste: piney, clean, slightly citrus and evergreen. High in Vitamin C — a traditional medicine.
---
Garnish: Cedar sprig in the cup; thin slice of dried apple floated (Indigenous winter tea tradition)
Temperature: Serve warm (65–70°C) in cooler months; cold-infused served at 8°C in summer

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
    print(f"Done. {len(RECIPES) - errors} Traditional recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
