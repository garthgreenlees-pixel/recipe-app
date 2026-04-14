#!/usr/bin/env python3
"""Add structured recipes to all 40 Provenance 500 Tea entries."""

import psycopg2

DB_WRITE = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

RECIPES = {
    9636: """RECIPE:
Yield: 1 cup (200ml) | Glassware: Thin-walled glass or white ceramic | Equipment: Gaiwan, kyusu teapot, or Western teapot
---
3g green tea leaves — Dragon Well (Longjing), Bi Luo Chun, or Sencha
200ml water at 70-75°C (heat to 85°C then cool 2-3 minutes, or use a temperature-controlled kettle)
Steep time: 1:30-2:00 minutes for first infusion
---
Gaiwan method (Chinese tradition):
1. Heat the gaiwan with boiling water; discard — preheating stabilizes temperature
2. Add 3g tea leaves; pour 70°C water to fill approximately two-thirds
3. Steep 1:30-2:00 minutes
4. Tilt the gaiwan lid to hold back leaves; pour into cup
5. Second infusion: 70°C water, 1:30-2:00 minutes (often the best cup)
6. Third infusion: 75°C water, 2:30 minutes
7. Most green teas yield 3-5 quality infusions

Western teapot method:
1. Add 3g leaves per 200ml water at 70-75°C
2. Steep 2:00 minutes
3. Strain immediately — do not leave leaves in contact with water

---
Quality indicators: Pale yellow-green liquor; fresh, vegetal, oceanic, or sweet aroma; no bitterness (bitterness means over-temperature or over-steep)
Temperature: Drink at serving temperature — wait for it to cool to below 70°C for best flavour
Note: Green tea is the most temperature-sensitive tea category. Boiling water destroys catechins, creates harsh bitterness, and strips delicate aromatic compounds. The 70°C rule applies to Japanese and Chinese green tea alike.

""",

    9637: """RECIPE:
Yield: 1 bowl (120-150ml) | Glassware: Traditional chawan (tea bowl) | Equipment: Chasen (bamboo whisk) + chashaku (bamboo scoop) + chawan
---
2g ceremonial-grade matcha powder — Uji (Kyoto prefecture) origin preferred; vibrant green colour
70ml water at 75-80°C (not boiling — boiling destroys flavour and creates bitterness)
---
Thin matcha (usucha — standard serving):
1. Warm the chawan by filling with hot water; discard and wipe dry
2. Sift 2g matcha into the chawan through a fine mesh strainer — eliminates clumps
3. Pour 70ml water at 75-80°C into the chawan
4. Whisk with the chasen in a rapid back-and-forth "W" or "M" motion — not circular — for 20-30 seconds until a thick, uniform foam forms with no large bubbles
5. The finished matcha should be completely smooth with a fine, stable foam surface

Thick matcha (koicha — ceremonial serving, requires premium matcha):
1. Use 4g premium matcha in 40ml water at 75°C
2. Fold slowly with the chasen in a gentle circular motion until smooth and thick — this is not frothed
3. The result is thick like melted chocolate — served silently in formal ceremony

---
Accompaniment: A small Japanese sweet (wagashi) — eaten before drinking
Temperature: Drink immediately — matcha begins to separate within 2-3 minutes
Note: Ceremonial-grade matcha (shade-grown for 3-4 weeks before harvest to boost L-theanine and chlorophyll, then stone-ground) is categorically different from culinary-grade. Culinary-grade matcha turns brown and bitter when whisked alone. Invest in the correct grade for drinking.

""",

    9638: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Large ceramic mug or teacup with saucer | Equipment: Teapot or infuser
---
3g black tea — Assam (malty, robust), Darjeeling first flush (floral, muscatel), or Ceylon (bright, citrus)
250ml water at 95-100°C (full boil or just below)
Steep time: Assam: 3-4 minutes | Darjeeling: 3 minutes | Ceylon: 3-4 minutes
---
1. Bring water to a full boil (95-100°C)
2. Warm the teapot by filling with boiling water; discard
3. Add 3g loose leaf tea (or 1 high-quality teabag) to the warmed teapot
4. Pour boiling water over the leaves
5. Steep: Assam 3-4 minutes (longer = more tannin, less pleasant); Darjeeling 3 minutes maximum; Ceylon 3-4 minutes
6. Strain immediately when steep time is reached — do not guess at time
7. Serve with milk poured in first (if using milk) — the classic British argument, never resolved

With milk (English tradition):
A small pour of cold whole milk added to the cup — milk first or after, both are valid depending on whom you ask

---
Quality indicators: Assam: deep amber, malty; Darjeeling: pale amber-gold, muscatel grape and floral; Ceylon: bright, orange-red
Temperature: Drink at 70-75°C — black tea is best just off full heat
Note: Black tea refers to oxidation level (100% oxidized), not the serving colour. Darjeeling first flush (spring harvest) is the most delicate and sought-after black tea globally — steep time is critical; 3:30 is the maximum before bitterness overtakes the muscatel note.

""",

    9639: """RECIPE:
Yield: 1 cup (150ml for gongfu; 250ml for Western) | Glassware: Gaiwan or small teacups | Equipment: Gaiwan + fairness pitcher (cha hai)
---
5g oolong tea — Tie Guan Yin (lightly oxidized, floral), Da Hong Pao (heavily oxidized, roasted), or High Mountain Ali Shan (fruity, creamy)
---
Gongfu cha method (recommended for oolong):
Water temperature: 85-95°C depending on oxidation level — lighter oolongs (20-40% oxidized) at 85-90°C; darker oolongs (60-80% oxidized) at 90-95°C
First infusion: 30 seconds; second: 45 seconds; third: 1:00; fourth: 1:30 (add 30 seconds each round)
---
1. Heat gaiwan and cups with boiling water; discard
2. Add 5g oolong to the gaiwan (about one-third full for tightly rolled oolongs — they expand dramatically)
3. Rinse: pour 85-90°C water over leaves, fill gaiwan, pour off immediately (5 seconds) — this "opens" the leaves and rinses impurities
4. First infusion: pour 85-90°C water; steep 30-40 seconds; pour into fairness pitcher, then into individual cups
5. Continue through 6-10 infusions — oolong is designed for multiple steeps; the character evolves dramatically

Western method:
3g oolong in 250ml water at 85-90°C; steep 3-5 minutes; strain

---
Temperature: Serve immediately after each pour — the small cups cool rapidly
Note: Oolong is the most complex tea category — ranging from 15% to 85% oxidation. The gongfu method is designed for oolong specifically; the short, repeated steeps reveal the evolution of the leaf across many infusions. Taiwanese high-mountain oolongs (Ali Shan, Li Shan) are among the most prized teas in the world.

""",

    9640: """RECIPE:
Yield: 1 cup (200ml) | Glassware: White ceramic or glass to appreciate the colour | Equipment: Infuser or gaiwan
---
3g white tea — Silver Needle (Bai Hao Yin Zhen) or White Peony (Bai Mu Dan)
200ml water at 75-80°C (white tea is the most delicate; boiling water obliterates the character)
Steep time: Silver Needle: 4-5 minutes | White Peony: 3-4 minutes
Multiple infusions: Silver Needle yields 5-7 infusions; White Peony 3-5
---
1. Do not preheat the vessel dramatically — white tea is delicate; extreme temperature changes harm the leaves
2. Add 3g white tea leaves or buds to the gaiwan or infuser
3. Pour 75-80°C water gently over the leaves — do not pour forcefully onto the leaves
4. Steep Silver Needle 4-5 minutes; White Peony 3-4 minutes
5. For Silver Needle: the buds are very dense; they may be steeped longer on subsequent infusions (each adding 60 seconds)
6. Pour and serve — the liquor should be very pale gold to light amber

---
Flavour profile: Silver Needle — cucumber, honeydew, light sweetness, almost no bitterness; White Peony — more body, slight floral, gentle sweetness
Temperature: Drink at 60-65°C — white tea's sweetness is most apparent at lower temperatures
Note: White tea undergoes no oxidation and no rolling — the leaves are simply withered and dried. This minimal processing preserves the highest levels of antioxidants of any tea type. The name refers to the silver-white hairs (pekoe) on the unopened buds of Camellia sinensis. Fuding and Zhenghe in Fujian province are the canonical origins.

""",

    9641: """RECIPE:
Yield: 1 cup (150-200ml) | Glassware: Ceramic or yixing clay cup | Equipment: Gaiwan or yixing teapot (dedicated to pu-erh)
---
Sheng (raw, aged) pu-erh:
4-5g sheng pu-erh from a compressed cake — break off with a pu-erh pick; use older material from the edges
Water temperature: 95-100°C
First infusion: 30 seconds; subsequent: add 15-20 seconds each

Shou (ripe, fermented) pu-erh:
4-5g shou pu-erh
Water temperature: 95-100°C
First infusion: 20 seconds; subsequent: add 15 seconds each

---
Gongfu method (for both types):
1. Rinse the yixing or gaiwan with boiling water
2. Add 4-5g tea; rinse the leaves with boiling water, pour off in 5 seconds — removes any earthy notes and opens compressed leaves
3. Pour boiling water; steep according to type
4. Pour all liquid into a fairness pitcher immediately at the end of each steep
5. Sheng: yields 10-15 quality infusions; Shou: 8-12 infusions

---
Flavour profile: Sheng (aged 10+ years): camphor, forest floor, dried fruit, complex sweetness, evolving from vegetal to aged character; Shou: earth, dark chocolate, compost, wet wood, smooth and full
Temperature: Serve at drinking temperature from small cups — both types benefit from heat
Note: Pu-erh is the only tea that improves with age — like wine or cheese, old sheng pu-erh cakes from Yunnan can be worth thousands of dollars and decades old. Yixing clay teapots, with their unglazed porous walls, absorb the tea's character over time — a seasoned yixing pot is part of the flavour.

""",

    9642: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Teacup with saucer | Equipment: Teapot or infuser
---
3g Earl Grey loose leaf tea — Twinings Original, Fortnum & Mason Earl Grey, or specialty bergamot-forward blends
250ml water at 90-95°C (just below full boil — black tea base with bergamot oil)
Steep time: 3-4 minutes — 4 minutes maximum before bergamot becomes bitter
---
1. Warm the teapot or cup with hot water; discard
2. Add 3g Earl Grey (or 1 quality teabag)
3. Pour 90-95°C water over the leaves
4. Steep exactly 3 minutes — the bergamot oil extracts very quickly
5. Strain immediately
6. Optional: add a thin slice of fresh lemon (amplifies the bergamot) or a dash of cold milk (masks the bergamot — purists prefer without)

London Fog (Earl Grey latte):
1. Brew Earl Grey double-strength: 6g in 100ml water, 3 minutes
2. Steam 150ml oat milk or whole milk to 65°C with microfoam
3. Combine and optionally add 10ml vanilla syrup
4. Pour steamed milk over concentrated tea

---
Flavour profile: Bergamot citrus aroma (from Citrus bergamia — a bitter orange hybrid from Calabria, Italy) over black tea; floral, citrus-forward, aromatic
Temperature: Drink at 65-70°C — bergamot oils are most aromatic just above body temperature
Note: Bergamot oil is what creates the distinctive flavour — real bergamot rind oil (not synthetic flavouring) makes an entirely different Earl Grey. The best Earl Greys are scented with natural bergamot extract applied to the tea leaves.

""",

    9643: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Any mug | Equipment: Kettle + infuser or teapot

Chamomile tisane:
4g dried chamomile flowers (loose) or 2 quality chamomile teabags
250ml water at 95°C (just below boiling — chamomile chamomile is hardy and welcomes near-boiling water)
Steep time: 5-7 minutes (longer than most — the oils need time to extract)
1. Pour near-boiling water over chamomile
2. Cover the cup while steeping — the aromatic oils evaporate with steam
3. Steep 5-7 minutes (not less — chamomile is surprisingly resistant to over-extraction)
4. Strain; add a drizzle of raw honey if desired

Peppermint tisane:
3g dried peppermint leaves or 4g fresh (bruise fresh leaves gently before using)
250ml water at 90-95°C
Steep time: 5-7 minutes
1. Pour water over peppermint
2. Cover while steeping
3. Strain; drink without milk or sweetener typically

Rooibos (see also entry 9782 for deep dive):
5g rooibos needle or coarse cut
250ml water at 100°C (full boil — rooibos is fully caffeine-free and tolerates boiling)
Steep time: 5-10 minutes (longer steeping only increases body, not bitterness)
---
General rule for herbal tisanes: No caffeine = no bitterness from over-steeping. Boiling or near-boiling water is almost always correct. Cover while steeping to retain volatile aromatic compounds.
Temperature: Drink at 65-70°C for most herbs
Note: Herbal tisanes are technically not tea (Camellia sinensis) — they are infusions of herbs, flowers, roots, and spices. The word "tisane" (French) is more accurate. None contain caffeine unless blended with actual tea.

""",

    9644: """RECIPE:
Yield: 2 cups (400ml) | Glassware: Handle-less chai glass or mug | Equipment: Saucepan
---
Masala chai spice blend (for 1 batch):
4 green cardamom pods (lightly crushed)
1 cinnamon stick (5cm)
4 whole cloves
1 tsp fresh ginger, grated (or ½ tsp dried ginger powder)
4 black peppercorns (cracked)
Optional: 1 star anise, pinch of nutmeg
---
Main recipe:
400ml water
2 tsp loose black tea — Assam CTC (Cut Tear Curl — traditional) or strong Assam loose leaf
200ml whole milk
2 tsp sugar (or to taste)
---
1. Combine water with all spices in a saucepan; bring to a full boil
2. Add tea; reduce to a simmer; simmer 2-3 minutes (the tea blooms in the boiling water)
3. Add milk; bring back to a boil while watching — it can overflow suddenly
4. Allow to rise (the foam reaching the top) twice — the "double boil" creates the right extraction
5. Strain through a fine mesh strainer into cups, pouring from height for slight froth
6. Taste and adjust sweetness
---
Accompaniment: Biscuits, samosa, or nothing — chai stands alone
Temperature: Serve very hot — should be drunk slowly as it cools
Note: Chai (simply means "tea" in Hindi) is built around Assam CTC tea — its high surface area allows quick extraction during boiling. Each household in India has its own spice ratio and sugar level. This recipe is a Punjabi-style masala chai — cardamom-forward with all the warming spices. The double-boil creates depth that a simple steep cannot.

""",

    9645: """RECIPE:
Yield: 4-6 small cups (15-25ml each) | Glassware: Zhong (gaiwan) with small tasting cups + cha hai (fairness pitcher) | Equipment: Gaiwan or yixing teapot + cha hai (fairness pitcher)
---
Gongfu cha ("kung fu tea" — the art of making tea with skill):
7g high-quality oolong or pu-erh — Da Hong Pao, Tie Guan Yin, or aged sheng pu-erh
Water: freshly drawn spring water at 95°C for oolongs; 100°C for pu-erh
Vessel: 120ml gaiwan (standard size)
---
The gongfu cha sequence:
1. Heat all utensils — pour boiling water over the gaiwan, fairness pitcher, and all cups
2. Add tea leaves to the warmed gaiwan (approximately one-third full for oolongs)
3. Rinse: pour water over the leaves, steep 5 seconds, pour off through the fairness pitcher — discard this rinse; it cleans the leaves and wakes them
4. First proper infusion: pour water in a circular motion; steep 30-45 seconds
5. Pour all liquid from the gaiwan into the fairness pitcher (pour everything out — do not leave drops)
6. From the fairness pitcher, pour evenly into the small tasting cups — the fairness pitcher equalizes concentration
7. Successive infusions: add 15-20 seconds to each steep time; continue through 8-15 infusions
8. Pay attention to how the character evolves — early infusions are bright; middle infusions are most complex; late infusions are sweeter and gentler
---
Temperature: Serve immediately in small cups — they cool fast and should be drunk quickly, then refilled
Note: Gongfu cha is not about ceremony for ceremony's sake — it is a system designed to maximize flavour extraction from premium tea across many infusions. The small cup size forces attention: you must drink immediately and taste completely before the cup is refilled.

""",

    9670: """RECIPE:
Yield: 1 cup (200ml) | Equipment: Kyusu (Japanese side-handle teapot) preferred; Western teapot or infuser acceptable

Sencha:
4g sencha leaves — Shizuoka, Uji, or Kagoshima origin; vibrant green colour
150-200ml water at 70-75°C
Steep time: 1:30-2:00 minutes
1. Warm the kyusu with hot water; discard
2. Add sencha
3. Pour 70-75°C water (cooled from boiling — add 20% cold water to boiling water to reach this)
4. Steep 1:30 (light brew) to 2:00 (fuller brew)
5. Pour every drop out — leaving tea in contact with water over-steeps
6. Second steep: 70°C water, 1:00 minute; third: 75°C, 1:30

Gyokuro (shade-grown — premium):
5g gyokuro per 60ml water (concentrated — it is drunk in small amounts)
Water at 50-60°C (very cool — gyokuro is extremely delicate and umami-rich)
Steep time: 2:30-3:00 minutes
Yield 3-4 infusions

Hojicha (roasted):
5g hojicha leaves or twigs
200ml water at 95°C (hojicha is roasted and can withstand higher temperature)
Steep time: 1:00-2:00 minutes; can be steeped multiple times

---
Note: Gyokuro is the most premium Japanese green tea — shade-grown to maximize L-theanine (umami amino acid) and minimize catechins (bitterness). The result is rich, savoury, sweet, and almost vegetable-like in depth. It requires the lowest water temperature of any tea.

""",

    9671: """RECIPE:
Yield: 1 cup high mountain oolong; 1 serving bubble tea (700ml)

High Mountain Oolong (Ali Shan, Li Shan):
4g high mountain oolong — tightly rolled balls; green to gold colour
100ml water at 90°C
---
Gongfu method:
1. Warm gaiwan; add tea
2. Rinse: 90°C water, 5 seconds, discard
3. First steep: 45 seconds at 90°C; second: 60 seconds; third: 80 seconds
4. High mountain oolongs yield 6-10 infusions with increasing floral sweetness

Taiwanese Bubble Tea (Pearl Milk Tea):
Tapioca pearls (boba): 50g dry
Strong tea base: 10g Assam CTC in 200ml water, 4 minutes, strained; or 10g Taiwanese red tea (Ruby Red 18)
150ml whole milk or oat milk
30ml sugar syrup (brown sugar preferred: caramelize 50g brown sugar in 50ml water)
Ice

Boba preparation:
1. Boil tapioca pearls in abundant water per package instructions (typically 20-30 minutes); they should be chewy all the way through
2. Drain and toss with a tablespoon of brown sugar syrup while hot

Assembly:
1. Brew strong tea; cool to room temperature
2. Combine tea, milk, and sugar syrup in a cocktail shaker with ice; shake hard 10 seconds
3. Pour into a tall glass with boba at the bottom
4. Insert a wide straw

---
Note: Bubble tea was invented in Taiwan in the 1980s (credited to Liu Han-Chieh at Chun Shui Tang, Taichung). The boba must be freshly cooked — they harden after 4-6 hours and become unpleasant. Properly cooked boba should be like a chewy gummy — not hard, not mushy.

""",

    9672: """RECIPE:
Yield: 2 cups (teapot) or 1 glass per person | Glassware: Small Moroccan tea glass (ornate, handle-free) | Equipment: Moroccan silver or metal teapot (berrad)

Moroccan Atay (Mint Tea):
4g Chinese Gunpowder green tea (this specific type is traditional — not loose leaf or other greens)
Large bunch of fresh spearmint (na'na') — approximately 20g
3-4 tsp white sugar (or to taste; Moroccan tea is very sweet)
500ml boiling water
---
1. Warm the teapot with a small amount of boiling water; discard
2. Add gunpowder tea to the pot; pour a small amount of boiling water; swirl and discard — this rinses the tea
3. Add fresh mint, packing it firmly into the pot
4. Add sugar
5. Pour boiling water into the pot to fill
6. Steep 3-4 minutes
7. Pour one glass out and return it to the pot (the tasting glass) — taste and adjust sweetness
8. Pour from height — 30-45cm above the glass — to create the characteristic froth on the surface
---
Service: Three glasses are traditionally served, each slightly different. The host pours; guests do not pour for themselves.
Temperature: Serve very hot — the glass is handled with care
Note: The Moroccan mint tea ritual is central to hospitality — refusing tea is refusing the host. The three-glass tradition has a proverb: "The first glass is as gentle as life, the second is as strong as love, the third is as bitter as death." Gunpowder tea is essential — its tightly rolled pellets and slightly smoky, robust character hold up to the mint and sugar.

""",

    9673: """RECIPE:
Yield: 1 pot (3-4 cups) | Glassware: Bone china teacup with saucer | Equipment: Warmed teapot, hot water jug, milk jug, tea strainer

English Afternoon Tea:
8g high-quality blended black tea — Fortnum & Mason Royal Blend, Twinings Afternoon, or Darjeeling second flush
600ml freshly boiled water (95-100°C — re-boiled water loses oxygen and tastes flat)
Cold whole milk (separate jug)
---
1. Warm the teapot: fill with boiling water, leave 30 seconds, discard — this prevents the first cup being cold
2. Add 8g loose leaf tea to the warmed pot
3. Pour freshly boiled water (the water must be actively boiling when poured — not water that has been sitting)
4. Steep 3-5 minutes (Darjeeling: 3 minutes; blended Assam/Ceylon: 4-5 minutes)
5. Bring the teapot to the table with a hot water jug for dilution
6. Use a silver tea strainer over each cup when pouring
7. Milk goes in after the tea (or before — the great unanswered question of British culture)

The scone order: cream first, then jam (Cornish method) OR jam first, then cream (Devon method)
Sandwiches: egg and cress, smoked salmon and cream cheese, cucumber — crusts removed, cut into fingers

---
Temperature: The pot should be served as soon as it has steeped — afternoon tea moves at a civilised pace but not a slow one
Note: Afternoon tea was introduced by Anna Russell, Duchess of Bedford, circa 1840, as a remedy for the "sinking feeling" between lunch and a late dinner. The distinction from "high tea" (a working-class supper) is often confused — afternoon tea is the refined version served between 3-5pm with delicacies.

""",

    9674: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Ceramic mug — do not use glass unless necessary; the aroma is part of the character | Equipment: Teapot or infuser
---
3g Lapsang Souchong loose leaf — Da Zhangshan origin (traditional pine smoke from Fujian) or Zheng Shan Xiao Zhong (more delicate, not smoked artificially)
250ml water at 95-98°C (just below full boil — high temperature needed for the dense, roasted leaf)
Steep time: 3-4 minutes maximum; Lapsang turns astringent quickly with over-steeping
---
1. Warm the teapot or mug with hot water; discard
2. Add 3g Lapsang Souchong
3. Pour 95-98°C water over the leaves
4. Steep 3 minutes (first timer set); taste at 3:00 — if sufficient smoke and body, strain immediately
5. Do not steep beyond 4 minutes
6. Serve without milk (traditional) or with a small amount of whole milk (the milk tempers the smoke)
---
Food pairing: Smoked salmon, aged cheese (especially smoked cheddar or Gruyere), duck, game — the smoke of the tea matches the smoke of the food
Cocktail application: 1-2 tsp Lapsang cold-brewed in spirits for 4 hours creates a smoked cocktail base
Temperature: Drink at 65-70°C — the smoke aroma is most complex above body temperature
Note: Lapsang Souchong is the world's first black tea — discovered in Fujian, China, when soldiers occupied a tea factory. To save the harvest, the farmers dried the leaves rapidly over pine fires. The pine smoke became the defining character. Da Zhangshan uses actual pine smoke; cheaper versions use flavouring — the difference is immediately apparent.

""",

    9675: """RECIPE:
Yield: 1 cup (200ml) | Glassware: Fine bone china to appreciate the pale gold colour | Equipment: Teapot or infuser
---
3g Darjeeling first flush — Thurbo Estate, Margaret's Hope, or Makaibari; recent harvest (look for year on packaging)
200ml water at 85-90°C (lower than standard black tea — first flush is more delicate)
Steep time: 2:30-3:00 minutes maximum
---
1. Use spring water if possible — Darjeeling's clarity is water-dependent
2. Warm the teapot with hot water; discard
3. Add first flush leaves
4. Pour 85-90°C water (not boiling — the muscatel character burns off above 90°C)
5. Steep 2:30 minutes; taste; strain immediately when ready
6. Do not add milk — it masks the muscatel character that defines this tea
7. Drink plain in a fine cup
---
Flavour profile: Muscatel grape and apricot notes, light body, hint of green tea character, complex floral finish — the finest first flushes taste like a dry white wine in tea form
Temperature: Drink at 70-75°C — the aromatics bloom just above body temperature
Note: Darjeeling first flush (March-April harvest, after the dormant winter) is called the "Champagne of teas" — not just metaphor, but because the muscatel character is actually caused by the same green leafhopper insect that creates Oriental Beauty oolong. The insect bite triggers a chemical response in the plant that creates the muscatel aroma. The second flush (May-June) has more body and stronger muscatel; the autumnal flush has earthy depth.

""",

    9676: """RECIPE:
Yield: 1 cup hot (250ml) or 1 jug cold (1 litre) | Equipment: Teapot or saucepan

Hot hibiscus:
15g dried hibiscus flowers (Hibiscus sabdariffa — the roselle variety, not ornamental)
500ml water at 95°C (near-boiling)
Steep time: 5-8 minutes
1 tsp sugar or agave (optional)
---
1. Pour near-boiling water over hibiscus flowers
2. Steep 5-8 minutes (longer = deeper colour and more tartness)
3. Strain; add sweetener if desired; serve hot

Agua de Jamaica (Mexican cold version):
50g dried hibiscus flowers
1.5 litres water (1 litre boiling + 500ml cold)
3-4 tbsp sugar (to taste; hibiscus is very tart)
Juice of 1 lime
---
1. Pour 1 litre boiling water over hibiscus; steep 10-15 minutes
2. Strain through fine mesh; add sugar while hot; stir to dissolve
3. Add 500ml cold water; add lime juice
4. Refrigerate; serve over ice with lime wheel

---
Flavour profile: Intensely tart (like cranberry + pomegranate), deep crimson colour, floral background
Cocktail application: Use as a mixer in margaritas or gin sours — replaces citrus beautifully
Temperature: Hot or cold — hibiscus is one of the few beverages equally good in both forms
Note: Hibiscus tea (agua de Jamaica in Mexico, zobo in West Africa, bissap in Senegal) spans global cultures. The tartness comes from citric and malic acid in the sepals. One cup provides more vitamin C than an orange. The colour is pH-sensitive — add lime and it turns bright pink; add baking soda and it turns dark purple.

""",

    9677: """RECIPE:
Yield: 1 serving (a gourd of mate) | Glassware: Traditional gourd (mate) | Equipment: Metal bombilla straw + mate gourd
---
Yerba mate: 25-30g dried yerba mate herb — Nobleza Gaucha, Cruz de Malta, or Taragui brands; Argentine-style cut (coarse)
250ml water at 70-75°C (never boiling — "mate killer" temperature; boiling water burns the herb and creates harshness)
---
1. Fill the gourd two-thirds with dry mate
2. Cover the top with your palm; turn the gourd upside down and shake — this moves fine dust to the palm and away from the stem; discard the dust
3. Return the gourd upright with the herb in a mound on one side (not flat) — this creates the space for the water
4. Insert the bombilla straw into the bare side of the gourd, buried in the herb
5. Pour a small amount of cool water (50°C) into the side where the bombilla sits — do not wet the herb yet; this pre-hydrates slowly
6. Wait 30 seconds; then pour 70-75°C water to fill the gourd (water on the bare side, not over the herb)
7. Drink through the bombilla (the metal filter at the bottom stops herb from entering)
8. Refill with 70-75°C water when empty — the same gourd yields 10-20 refills
---
Social protocol: The cebador (server) prepares and passes the gourd; the drinker finishes completely and returns it without saying "thank you" (gracias means "no more" in mate culture); the cebador refills and passes to the next person
Temperature: 70-75°C is non-negotiable — this is the functional requirement, not a preference
Note: Yerba mate contains caffeine (theophylline and theobromine) plus high levels of antioxidants. It is one of the only beverages that is both a social ritual and considered a meal substitute in Argentina and Uruguay. The bombilla filter is precision-engineered — inserting it straight in (not at an angle) blocks it.

""",

    9678: """RECIPE:
Yield: 2 cups (400ml) | Equipment: Saucepan
---
Base chai blend (house masala — enough for 4-6 servings):
10 green cardamom pods (crushed)
2 cinnamon sticks (5cm each)
10 whole cloves
1 tsp black peppercorns (cracked)
2 tsp dried ginger (or 2 tbsp fresh grated)
2 star anise (optional)
1 small piece of mace
---
Chai preparation (per 2 cups):
400ml water
2 heaped tsp Assam CTC black tea
200ml whole milk
2-3 tsp sugar (to taste)
2 tsp chai masala blend (from above)
---
1. Combine water with chai masala in a saucepan; bring to boil; reduce and simmer 3 minutes
2. Add tea; stir; simmer 2 more minutes
3. Add milk; turn heat to medium-high; bring to a vigorous boil while watching (will overflow)
4. As foam rises, remove from heat; allow to settle; return to heat twice more (traditional triple rise)
5. Strain through fine mesh; add sugar; adjust to taste
6. Pour into glasses from height for froth
---
Iced chai:
Brew double-strength as above; cool; pour over ice; add cold milk 1:1
---
Note: Every chai masala is a regional signature — Gujarati chai leans on cinnamon and cloves; Punjabi on black pepper and ginger; Kashmiri on saffron and almonds (kahwa). The principle is universal: boil spices first, then add tea and milk together. The double or triple boil creates a depth that a simple steep cannot.

""",

    9714: """RECIPE:
Yield: 1-2 litres kombucha (first fermentation) | Glassware: Glass jar for fermentation; tall glass for serving | Equipment: 2-4 litre glass jar + SCOBY (Symbiotic Culture of Bacteria and Yeast)
---
First fermentation:
1 SCOBY + 200ml starter liquid (from a previous batch or store-bought unflavoured raw kombucha)
1 litre strong black or green tea (6g tea in 1 litre boiling water, steeped 10 minutes, strained)
100g white sugar (dissolved in the hot tea)
---
1. Brew tea; dissolve sugar while hot; cool completely to below 25°C (warm tea kills SCOBY)
2. Pour cooled tea into clean glass jar; add starter liquid; lower SCOBY in gently
3. Cover with a breathable cloth (cheesecloth, coffee filter) secured with a rubber band — not an airtight lid
4. Ferment at room temperature (20-24°C ideal) for 7-14 days
5. Taste daily from day 7 — ready when pleasantly tart with residual sweetness; typically day 9-12
6. Remove SCOBY + 200ml liquid (save for next batch); bottle the kombucha

Second fermentation (for carbonation):
1. Add fruit juice (50ml per 500ml), ginger, or flavouring to the bottled kombucha
2. Seal in flip-top bottles; ferment at room temperature 2-4 days
3. Burp bottles daily — pressure can build significantly
4. Refrigerate when desired carbonation level is reached
---
Temperature: Serve chilled — kombucha is always cold
Note: The SCOBY is the living culture — it must be handled carefully. Do not use antibacterial soap when cleaning equipment. The starter liquid (acidic) prevents contamination during early fermentation. Room temperature matters: below 18°C, fermentation slows dramatically; above 28°C, off-flavours develop.

""",

    9715: """RECIPE:
Yield: 1 mug (300ml) | Equipment: Small saucepan or milk frother | Glassware: Large mug

Golden Milk (Turmeric Latte):
300ml whole milk or oat milk (both work well; oat milk creates a naturally sweet version)
1 tsp ground turmeric (or 1 tbsp fresh turmeric, grated)
½ tsp ground cinnamon
¼ tsp ground ginger (or 1 tsp fresh grated)
Pinch of freshly ground black pepper (increases turmeric absorption by 2000%)
1 tsp raw honey or maple syrup (add after heating — honey loses beneficial enzymes above 60°C)
Pinch of ground cardamom
Optional: ¼ tsp vanilla extract
---
1. Combine milk with all spices (not honey) in a small saucepan
2. Heat over medium heat, whisking constantly — do not allow to boil; target 60-65°C
3. Continue whisking until hot and slightly frothy (or use a milk frother)
4. Remove from heat; add honey and vanilla if using
5. Strain through a fine mesh if texture is important (the turmeric won't fully dissolve)
6. Pour into a warmed mug; grate a pinch of additional cinnamon on top
---
Iced version: Double the concentration; cool completely; pour over ice; add cold milk
Temperature: Serve at 60-65°C — just below scalding; sip immediately
Note: The black pepper addition is not incidental — piperine in black pepper increases curcumin (turmeric's active compound) bioavailability by 2000% according to multiple studies. Without black pepper, most of the turmeric's anti-inflammatory properties pass through unabsorbed. This is Ayurvedic knowledge confirmed by modern nutritional science.

""",

    9716: """RECIPE:
Yield: 1 cup (200ml) | Glassware: Small ceramic cup or sencha cup | Equipment: Kyusu or infuser

Genmaicha:
4g genmaicha tea (green tea mixed with toasted brown rice — the ratio varies by brand; more rice = nuttier)
200ml water at 75-80°C (similar to regular green tea — the rice content does not change the temperature requirement)
Steep time: 1:30-2:00 minutes
---
1. Warm the kyusu with hot water; discard
2. Add genmaicha leaves
3. Pour 75-80°C water
4. Steep 1:30-2:00 minutes
5. Pour out completely into cups — do not leave in contact with leaves
6. Second infusion: 80°C water, 1:30 minutes; third: 85°C, 2:00 minutes

Matcha-iri genmaicha (with added matcha):
Some genmaicha varieties include matcha powder added at the end of production
These require: steep as above, then whisk briefly with a chasen for the matcha component

---
Flavour profile: Nutty, popcorn-like (from the toasted rice — some rice "pops" like popcorn during roasting), fresh green tea character, light sweetness, umami background
Temperature: Drink at 65-70°C — the nutty notes are most pleasant at moderate heat
Note: Genmaicha was historically known as "peasant tea" or "poor man's tea" — the rice was added to extend the expensive tea with cheap filler. The pairing became celebrated for its own character. The roasted rice creates the same Maillard reaction compounds as popcorn.

""",

    9717: """RECIPE:
Yield: 1 cup (200ml) | Glassware: White ceramic cup | Equipment: Teapot or gaiwan

Jasmine tea (loose leaf or pearls):
4g jasmine tea — jasmine pearls (Dragon Phoenix Pearls) or jasmine sencha (loose leaf)
200ml water at 75-80°C (jasmine tea has a green or white tea base — never use boiling water)
Steep time: 2:00-3:00 minutes for pearls (they unfurl slowly); 1:30-2:00 for loose leaf
---
1. Warm the teapot or cup
2. Add jasmine tea — pearls are visually spectacular as they unfurl in a glass
3. Pour 75-80°C water
4. Steep: pearls 2:00-3:00 minutes (they expand significantly); loose leaf 1:30-2:00
5. Do not strain if using pearls in a glass — they are part of the visual
6. Pour off into a cup if using a teapot

Second infusion: 80°C water, 2:00 minutes — jasmine yields 3-5 infusions
---
Flavour profile: Jasmine flowers, fresh floral sweetness, green tea base (grassy, slightly oceanic), light body
Temperature: Drink at 65-70°C — jasmine aromatics are volatile and diminish if too hot
Note: Jasmine tea is produced by layering fresh jasmine flowers over green (or sometimes white or oolong) tea leaves at night, when the flowers are most fragrant, then removing them before dawn. This process (called scenting or chaxuning) may be repeated 3-7 times for premium jasmine teas. The tea absorbs the fragrance; the flowers are removed before packaging.

""",

    9718: """RECIPE:
Yield: 1 cup | Equipment: Standard teapot or saucepan for boricha

Boricha (Korean roasted barley tea):
30g roasted barley — pre-roasted packages available (Ottogi, Damtuh brands) or roast raw barley yourself in a dry pan until golden
1 litre water
---
1. If roasting raw barley: toast in a dry pan over medium heat 10-15 minutes, stirring constantly, until golden and aromatic
2. Boil water in a saucepan; add roasted barley
3. Reduce heat; simmer 15-20 minutes
4. Strain; serve hot or cold
5. Boricha is always made in large batches — it is the everyday Korean drink, served as water would be

Nokcha (Korean green tea):
3g Korean green tea — Jeju Woojeon (first harvest, most premium) or Sejak
150ml water at 65-70°C (Korean green tea is delicate; lower temperature than Chinese greens)
Steep time: 1:00-1:30 minutes; multiple infusions
---
Yuja-cha (citron honey tea):
2 tbsp yuja-cha paste (Korean citron marmalade — Chung Jung One brand)
200ml hot water (85°C)
1. Spoon paste into cup; pour hot water; stir; drink with the peel pieces

---
Note: Boricha is consumed as a daily hydration beverage in Korean households — always kept in the refrigerator in summer, served hot in winter. It is caffeine-free and considered digestive and cooling. The everyday Korean table has boricha where Western tables have water.

""",

    9719: """RECIPE:
Yield: 1 cup (200ml) | Equipment: Teapot or gaiwan

Dianhong (Yunnan Black Tea / Golden Tips):
4g Yunnan black tea — Golden Monkey (Jin Hou), Yunnan Gold (Dian Hong Jin Ya) — look for the golden tips
200ml water at 90-95°C (slightly below boiling — Yunnan black is less tannic and more delicate than Assam)
Steep time: 2:30-3:00 minutes (shorter than Assam — Yunnan burns faster)
---
1. Warm the teapot; add tea
2. Pour 90-95°C water
3. Steep 2:30-3:00 minutes — no longer
4. Pour completely; serve without milk (milk masks the characteristic malt-honey-cocoa notes)
---
Flavour profile: Honey sweetness, cocoa, malt, rich and smooth. The golden tips (the unopened buds) contribute sweetness and aroma. One of the sweetest, most approachable black teas.
Temperature: Drink at 70-75°C
Note: Yunnan is the botanical birthplace of Camellia sinensis — the tea plant originated here. Dianhong refers to black (hong) tea from Dian (Yunnan). The golden tips (buds) are the highest-quality part of the plant — leaves with the most golden tips command the highest prices. Unlike Assam, Yunnan black tea is low in tannins and very high in natural sweetness.

""",

    9720: """RECIPE:
Yield: 1 litre iced tea | Glassware: Tall glass | Equipment: Teapot or saucepan

Sweet Tea (Southern American style):
6g black tea (Luzianne brand is traditional for Southern sweet tea, or Lipton Family-Size bags)
500ml boiling water for the tea concentrate
500ml cold water
100g sugar (dissolved while tea is hot)
---
1. Brew tea: steep 5 minutes in 500ml boiling water
2. Remove tea bags/leaves; add sugar immediately to the hot concentrate; stir until dissolved
3. Add 500ml cold water; stir; refrigerate
4. Serve over ice in a tall glass with a lemon wedge
---
Sun Tea (no-heat method, 6-8 hours):
8g tea, 2 litres cold water; steep in a jar in direct sunlight 6-8 hours; strain; add sugar to taste

Cold-Brew Iced Tea:
8g tea per 1 litre cold water; refrigerate 8-12 hours; strain; serve over ice (no sugar needed — cold brew is naturally sweeter)

Japanese Iced Matcha:
2g ceremonial matcha; whisk with 30ml hot water (80°C) until smooth; pour over a full glass of ice; add 200ml cold water

---
Temperature: Always served over ice — Southern sweet tea is always cold, very sweet, and usually very strong
Note: Southern US sweet tea is made by dissolving the sugar in the hot concentrate — this creates a supersaturated solution that holds more sugar than cold water can. Adding sugar after cooling results in undissolved crystals at the bottom. It is technically a sugar-tea syrup diluted with cold water.

""",

    9721: """RECIPE:
Yield: 1 large glass (700ml) | Glassware: Tall glass | Equipment: Saucepan

Thai Tea (Cha Yen):
30g Thai tea mix — Cha Tra Mue brand (the classic orange-coloured blend of black tea, vanilla, spices, and food colouring) or use strong Assam + half a star anise + 1 cardamom pod
300ml boiling water
3 tbsp sweetened condensed milk (Longevity brand)
2 tbsp evaporated milk (poured over ice, not mixed in)
Crushed ice or large ice cubes
---
1. Brew Thai tea: steep 30g mix in 300ml boiling water for 5-7 minutes; strain through a fine-mesh or cheesecloth (the mix is fine-ground and requires thorough straining)
2. While hot, stir in sweetened condensed milk until dissolved
3. Allow to cool; can refrigerate at this point
4. Fill glass with crushed or cubed ice
5. Pour the tea-condensed milk mixture over the ice (fills about two-thirds of the glass)
6. Pour evaporated milk gently over the top — it should float as a pale cream layer over the orange tea
7. Serve with a straw and stir before drinking
---
Temperature: Always cold and iced — Thai tea is a street-food drink, always cold
Note: Thai tea's orange colour comes from food colouring added to the tea mix — not from the tea itself. Cha Tra Mue is the most iconic brand (the elephant label) available throughout Southeast Asia and globally online. The layered presentation (orange tea + white evaporated milk) is part of the identity — stir it together when drinking.

""",

    9722: """RECIPE:
Yield: 1 serving (approximately 250ml) | Glassware: Traditional wooden bowl or ceramic bowl | Equipment: Saucepan

Tibetan Butter Tea (Po Cha / Bhoe Ja):
500ml water
5g Pu-erh or strong black tea (brickle tea, if available; or Yunnan or Assam as substitute)
30ml yak butter or unsalted European-style cultured butter (closest available substitute)
1 tsp Himalayan rock salt (essential — this is a savoury drink, not sweet)
60ml milk (traditionally yak milk; whole cow's milk acceptable)
---
1. Boil water; add tea; simmer 10-15 minutes (very strong extraction is correct)
2. Strain tea into a traditional wooden churn (dong mo) or blender
3. Add butter and salt to the hot tea
4. Churn vigorously for 2-3 minutes (in the dong mo) or blend 30-45 seconds (modern method) until emulsified and slightly frothy
5. Add milk; churn/blend briefly again
6. Serve in a wooden bowl or pre-warmed ceramic bowl — refilled constantly throughout the day
---
Temperature: Very hot — this is a warming, high-calorie drink for extreme altitude living
Note: Po Cha provides around 240 calories per cup from the butter — functional high-altitude nutrition. Tibetans may drink 40+ cups per day. The salt and butter combination sounds unusual to Western palates but is deeply warming and sustaining. The fat in the butter prevents the high-altitude dehydration that water alone cannot address at 4,000m+ elevation.

""",

    9723: """RECIPE:
Yield: 1 each (see individual recipes below) | Equipment: Various

London Fog (Earl Grey latte):
Strong Earl Grey concentrate: 10g tea in 100ml water at 90°C, 5 minutes; strain
150ml oat milk or whole milk; steam to 65°C with microfoam
15ml vanilla syrup (1:1)
---
1. Combine concentrate, syrup, and steamed milk; top with foam

Arnold Palmer (half and half):
500ml brewed black tea (Lipton or Tetley; sweetened or not)
500ml fresh lemonade (200g sugar + 200ml lemon juice + 600ml cold water)
---
Combine; pour over ice; adjust ratio to preference

Tea-infused gin cocktail:
2 Earl Grey bags cold-steeped in 700ml London dry gin for 2 hours; strain
Use as a base in a Martini (see cocktail entry 8993) or serve with tonic

Hojicha Latte:
10g hojicha (roasted Japanese green tea) steeped in 100ml hot water (90°C) for 2 minutes; strain
150ml oat milk; steam to 65°C
Combine; optional: a pinch of cinnamon

Matcha latte (see Non-Alcoholic entry 9924 for detailed recipe)

---
Note: Tea's role in the bar is expanding — tea-infused spirits, tea syrups, tea-based cocktails, and tea-forward mocktails are now menu staples at serious cocktail bars. Cold-infusing tea into spirits avoids bitterness and creates clean, aromatic results. The rule: 2 teabags per 700ml, 2-4 hours maximum cold infusion.

""",

    9782: """RECIPE:
Yield: 1 cup (300ml) | Glassware: Mug | Equipment: Teapot, saucepan, or infuser

Rooibos (plain):
5g rooibos (needles, loose leaf, or teabag — Two Oceans, Carmien, or Numi brands)
300ml water at 100°C (full boil — rooibos is caffeine-free and cannot be over-steeped)
Steep time: 5-10 minutes (longer only increases body and depth, never bitterness)
Optional: Honey, milk, or lemon
---
1. Pour boiling water over rooibos
2. Steep 5-10 minutes (steep time is flexible — rooibos is forgiving)
3. Strain; add honey or milk if desired
4. Serve hot or allow to cool completely and serve over ice

Rooibos latte:
5g rooibos in 150ml boiling water; steep 8 minutes; strain strong
150ml steamed oat milk or whole milk at 65°C
Combine; optional: 1 tsp vanilla syrup and a pinch of cinnamon

Rooibos iced tea:
15g rooibos in 1 litre boiling water; steep 10 minutes; strain; cool; refrigerate; serve over ice

---
Flavour profile: Naturally sweet (contains aspalathin, a unique flavonoid), vanilla-like, slightly earthy, mild tannins, red-amber colour
Temperature: Excellent both hot and cold — one of the most versatile tisanes
Note: Rooibos (Aspalathus linearis) grows only in the Cederberg mountains of South Africa's Western Cape — an area of approximately 200km x 30km. It cannot be cultivated elsewhere due to specific soil and climate requirements. Rooibos contains zero caffeine, zero oxalic acid (kidney stone-safe), and exceptionally high antioxidants (polyphenols).

""",

    9783: """RECIPE:
Yield: 1 cup (250ml) | Glassware: Glass or ceramic — the pale gold colour is part of the identity | Equipment: Infuser or teapot

Chrysanthemum tea (Ju Hua Cha):
8-10 dried chrysanthemum flowers (Bai Ju — white chrysanthemum is preferred; Hangzhou origin is most prized)
250ml water at 90-95°C (just below boiling — chrysanthemum is delicate)
Steep time: 3-5 minutes
Optional: rock sugar (bing tang) or honey; wolfberries (goji berries)
---
1. Rinse flowers briefly with a small amount of hot water; discard rinse — removes any dust
2. Pour 90-95°C water over flowers
3. Steep 3-5 minutes; the water will turn pale gold and the flowers will expand
4. Add rock sugar or wolfberries during steeping if using
5. Strain or drink with the flowers left in (they sink and are not consumed)
---
Flavour profile: Floral (chrysanthemum), lightly sweet, slightly bitter finish, very light body
Traditional use: Cooling (in Traditional Chinese Medicine, chrysanthemum is classified as a "cooling" herb — taken for fever, headaches, eye strain, and inflammation)
Temperature: Drink at 65-70°C; also consumed cold and refrigerated in summer
Note: Chrysanthemum tea is one of China's most consumed beverages after water and green tea. The white chrysanthemum variety (Bai Ju Hua from Hangzhou or Huizhou) is preferred for tea — the yellow variety (Huang Ju) is stronger and more medicinal in character. Traditionally combined with pu-erh tea for a "dual function" cup.

""",

    9784: """RECIPE:
Yield: 1 samovar service (many cups) | Glassware: Traditional podstakannik (metal cup holder with glass) | Equipment: Samovar (or large urn as substitute)
---
Russian samovar tea:
Zavarka (concentrated tea):
15g strong black tea — Georgian tea, Indian Assam, or Ceylon
300ml boiling water
---
1. Brew zavarka: steep tea very strongly in 300ml boiling water for 7-10 minutes; this concentrate sits on top of the samovar
2. Fill the samovar with boiling water and keep at near-boiling throughout service

Serving each cup:
1. Pour a small amount of zavarka (30-50ml) into the glass inside the podstakannik
2. Fill with hot water from the samovar tap — dilute to preference (each person adjusts their own)
3. Add lemon slice and/or sugar (lump sugar held between teeth is the old Russian method — drinking tea through the sugar)

Russian additions: Raspberry jam (varenye) stirred in as a sweetener; a tablespoon of honey; milk is uncommon
---
Temperature: Very hot — the podstakannik (metal holder) protects the fingers while holding glass
Note: The samovar is not just a kettle — it is the symbol of Russian hospitality. A copper samovar burning charcoal (rather than electric) produces a distinctly different heat that samovar traditionalists insist affects the taste of the water. The ritual of gathering around the samovar is called "tea drinking" (chaepitie) — it is a social event lasting hours.

""",

    9785: """RECIPE:
Yield: 2 litres (Southern style) | Glassware: Mason jar or tall glass | Equipment: Teapot or saucepan

Southern Sweet Tea (canonical recipe):
4 family-size black tea bags (Luzianne or Lipton) or 12 regular bags
1 litre boiling water (for concentrate)
1 litre cold water (for dilution)
200g white sugar (dissolved in the hot concentrate — very sweet; adjust to taste)
---
1. Bring 1 litre water to a full boil
2. Pour over tea bags in a heat-proof pitcher; steep 5 minutes exactly (not more — will turn bitter)
3. Remove bags; add sugar immediately to the hot tea; stir vigorously until fully dissolved
4. Add 1 litre cold water; stir; refrigerate
5. Serve over ice in a mason jar or tall glass with a lemon wedge and a long straw
---
Variations:
Arnold Palmer: half sweet tea, half lemonade
Peach sweet tea: add 60ml peach nectar per litre; garnish with a fresh peach slice
Mint sweet tea: steep 8 fresh mint leaves in the hot concentrate with the tea; remove with the bags

Temperature: Always served ice-cold; never at room temperature
Note: Sweet tea is a regional identity in the American South — a non-sweet option is often unavailable. The sugar is dissolved while hot (creating a supersaturated solution), which is why Southern sweet tea can hold far more sugar than regular iced tea with sugar stirred in cold. Ordering "iced tea" in the South typically means you receive sweet tea automatically.

""",

    9786: """RECIPE:
Tasting framework to understand the specialty tea movement:
---
Comparison protocol — specialty vs. commodity tea:
Brew two cups simultaneously:
Cup 1: commodity tea — a standard supermarket tea bag (Lipton, Tetley, store-brand)
Cup 2: specialty single-estate tea — a named estate (e.g., Makaibari Darjeeling, Glenburn Second Flush, Thurbo First Flush)

Both: 3g per 200ml, water at 90°C, 3 minutes steep

---
Compare:
1. Dry leaf aroma — commodity: generic, musty; specialty: specific, complex, aromatic
2. Colour — commodity: deep red-brown (small-particle CTC extract); specialty: varies by type (pale gold to amber to deep red)
3. First taste — commodity: bold bitterness, flat; specialty: specific flavour notes (fruit, flowers, mineral, malt)
4. Finish — commodity: astringent, short; specialty: evolving, sweet, long-lasting
5. At room temperature — commodity: more flat; specialty: develops new flavours as it cools
---
Specialty tea markers: named estate, harvest date (first flush, second flush, autumnal), elevation, cultivar, process (orthodox vs CTC), and country of origin all appear on the label. Commodity tea has none of this information.
Note: Tea is the world's most consumed beverage after water. Approximately 80% of global production is commodity-grade CTC (Cut-Tear-Curl machine processing), blended and sold anonymously. Specialty tea represents the top 5-10% of production — traceable, specific, and worth drinking without milk.

""",

    9787: """RECIPE:
Tea and food pairing framework — systematic approach:
---
For each pairing below: brew 200ml of the listed tea at the correct temperature and steep time

Principle 1 — Weight matching:
Delicate teas (white, light green) + delicate foods (sushi, mild fish, fresh cheese)
Full-bodied teas (Assam, Yunnan black, pu-erh) + rich foods (steak, aged cheese, roasted meat)

Specific pairings:
Darjeeling first flush (muscatel) + almond tart or croissant: The muscatel and almond mirror each other
Lapsang Souchong + smoked salmon: Smoke meets smoke; amplification, not clash
Japanese Gyokuro + delicate sashimi: The umami (L-theanine) of gyokuro matches the umami of fish
Pu-erh (aged sheng) + aged hard cheese: Both have fungal complexity; they find common ground
Moroccan mint tea + lamb tagine: The mint cuts through the richness of the braised lamb
Masala chai + sticky toffee pudding: Spice-meets-caramel in harmonic sweetness
Camomile + honey cake or madeleines: Floral meets floral

Principle 2 — Acidity and fat:
High-acidity teas (Kenyan, Ceylon) cut through dairy fat (like wine acidity)
Low-acidity teas (pu-erh, rooibos) work with sweet and fatty desserts

Principle 3 — Temperature:
Hot tea with food (traditional); cold-brew iced tea for summer fare (salads, light fish)

---
Note: Tea and food pairing is an emerging discipline — established in Asia for millennia but now entering Western fine dining. The key advantage over wine: zero alcohol, high flexibility with all courses, and the ability to pair with dessert without clashing sweetness.

""",

    9788: """RECIPE:
Yield: 1 cup (200ml) | Equipment: Teapot or gaiwan

Sun Moon Lake Black Tea (Ruby Red 18 / Hongyucha):
4g Sun Moon Lake black tea — Ruby Red (TRES No. 18), Assam (TRES No. 8), or Ruby hybrid
200ml water at 90-95°C (slightly below boiling — this tea is more delicate than Assam)
Steep time: 2:00-3:00 minutes (short steep — this tea extracts quickly)
---
1. Warm the teapot; add leaves
2. Pour 90-95°C water
3. Steep 2:00-3:00 minutes; strain immediately
4. Serve without milk — the cinnamon-mint character of Ruby Red (No. 18) needs no addition
---
Flavour profile: Ruby Red (No. 18) — distinctive cinnamon, mint, and caramel notes unlike any other black tea; low astringency; medium-light body
Temperature: Drink at 70-75°C; also excellent cold over ice without any additional sweetener
Note: Taiwan's Sun Moon Lake tea region produces a unique black tea using the Assam cultivar (TRES No. 8, brought from India in 1925) and a hybrid with a wild Burmese variety (creating TRES No. 18, Ruby Red). The cinnamon-mint note of Ruby Red is a natural characteristic of the hybrid — not an added flavouring. It is one of the most unusual and beloved teas in Taiwan.

""",

    9789: """RECIPE:
Yield: 1 cup (250ml) | Equipment: Infuser or pot

Lavender tisane:
5g dried food-grade lavender flowers (not ornamental — ornamental lavender may be treated)
250ml water at 90°C
Steep time: 5 minutes (maximum — longer creates a soapy, perfume-counter character)
Optional: honey and lemon
---
1. Pour 90°C water over lavender
2. Cover while steeping — the volatile oils escape with steam
3. Steep exactly 5 minutes; strain immediately
4. Sweeten with a drizzle of honey if desired

Floral tisane blend:
3g rose petals + 2g hibiscus + 2g chamomile
250ml water at 90°C
5 minutes; strain; add honey
---
This creates a "garden blend" with rose floral, hibiscus tartness, and chamomile calm

Rose petal tea:
5g dried rose petals (food grade — from an unsprayed source; Damask rose is the most aromatic)
250ml water at 85°C (lower — rose petals are delicate)
4 minutes; strain; add rock sugar or honey

Elderflower:
Use elderflower cordial (St-Germain or Belvoir) diluted 1:8 with hot water — or brew fresh elderflowers (10g in 300ml at 75°C, 5 minutes) for a fresh floral tisane
---
Temperature: 65-70°C for all floral tisanes — serve and drink promptly; they cool fast
Note: Lavender must be food-grade (culinary lavender) — not garden lavender, which may have been treated with pesticides. The most common mistake is over-steeping: beyond 5 minutes, lavender goes from pleasant-floral to overwhelming-soapy. 5 minutes is not a guideline — it is the maximum.

""",

    9790: """RECIPE:
Yield: 1 cup (250ml) | Equipment: Teapot or saucepan

Licorice root tea:
8g dried licorice root (Glycyrrhiza glabra) — cut and sifted
250ml water
Bring water and licorice root to a simmer; simmer 10-15 minutes (not just steep — roots require decoction)
Strain; sweeten if desired (it is naturally very sweet — glycyrrhizin is 50x sweeter than sugar)

Dandelion root "coffee":
10g roasted dandelion root (available in health food stores; Teeccino brand)
250ml water
Simmer 10-15 minutes; strain; add milk and sweetener if desired
---
Flavour profile: Rich, dark, coffee-like (not identical — slightly earthier and more herbal), naturally caffeine-free

Chicory root "coffee":
10g roasted chicory root granules
250ml water at 95°C
Steep 5-7 minutes (unlike dandelion, chicory can be steeped rather than simmered)
Add milk — chicory is always better with milk (as in New Orleans-style cafe du monde blend)

Burdock root tea:
8g burdock root (gobo)
500ml water
Simmer 20 minutes; strain; earthy, slightly sweet, mineral

---
Temperature: Hot; root teas are always served hot
Note: Root tisanes require decoction (simmering), not infusion (steeping) — the tough plant material releases its compounds only under prolonged heat. Licorice root should not be consumed in large quantities daily — glycyrrhizin affects aldosterone and can elevate blood pressure with excessive consumption.

""",

    9791: """RECIPE:
Yield: 1 cocktail or mocktail | Glassware: Coupe or rocks glass | Equipment: Chasen + shaker

Matcha Gin and Tonic (alcoholic):
See cocktail entry 8996 for full recipe

Matcha Sour (non-alcoholic):
2g ceremonial matcha whisked with 30ml water at 80°C until smooth
30ml fresh lemon juice
15ml agave syrup (2:1)
1 egg white or 30ml aquafaba (chickpea liquid)
---
1. Whisk matcha with hot water; cool completely (important — hot matcha in a shaker creates steam)
2. Combine cooled matcha, lemon juice, agave syrup, and egg white in a shaker; dry shake 15 seconds
3. Add ice; shake hard 15 seconds
4. Double-strain into a chilled coupe

Matcha Highball (non-alcoholic):
2g matcha whisked with 30ml water at 80°C
10ml honey syrup (2:1)
200ml sparkling water, poured gently over ice and matcha; stir once

Matcha Cold Brew Latte:
2g culinary matcha (cold-brew grade) whisked into 100ml cold water; stir vigorously (not whisk — whisking cold is less effective)
150ml cold oat milk; pour over ice

---
Note: Matcha in cocktails follows the same temperature rule as matcha tea: never above 80°C. Hot matcha in a shaker with ice creates condensation and steam that floods the shaker and changes the dilution. Always cool the matcha mixture before combining with other cold cocktail ingredients.

""",

    9792: """RECIPE:
Yield: 1 litre | Glassware: Tall glass or pitcher | Equipment: Large jar + refrigerator (no heat required)

Cold brew green tea:
8g Japanese green tea — Sencha or Gyokuro for cold brew (cold brew is ideal for delicate greens — no bitterness risk)
1 litre cold filtered water
---
1. Combine tea and cold water in a jar; do not use any warm water
2. Refrigerate for 6-8 hours (Sencha) or 4-6 hours (Gyokuro — more concentrated and delicate)
3. Strain through a fine mesh; refrigerate for up to 3 days
4. Serve in a tall glass over ice; no milk or sweetener typically needed — cold brew green tea is naturally sweet

Cold brew black tea:
8g Darjeeling or Ceylon black tea
1 litre cold water
Refrigerate 12-14 hours; strain; serve over ice (excellent without sweetener — cold brew is gentler than hot-brewed)

Cold brew chamomile:
10g dried chamomile flowers
1 litre cold water
Refrigerate 8-12 hours; strain; add honey at serving if desired

---
The science of cold brew tea: Cold water extracts tea's sweet compounds (amino acids, theanine, sugars) while leaving behind most bitter tannins and catechins (which require heat for extraction). The result is a naturally sweet, smooth, low-bitterness beverage. This is the same principle as cold brew coffee — cold extraction changes the chemical profile significantly.
Temperature: Serve ice-cold — cold brew tea is designed for cold service; heating it defeats the purpose
Note: Cold brew green tea is exceptionally high in L-theanine (the calming amino acid) because L-theanine is water-soluble at all temperatures, while catechins (bitter) require heat. The cold brew method creates a maximally calming, minimally bitter cup.

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
    print(f"Done. {success} tea recipes added, {errors} errors.")


if __name__ == "__main__":
    main()
