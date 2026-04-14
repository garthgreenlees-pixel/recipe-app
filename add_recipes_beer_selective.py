#!/usr/bin/env python3
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

# Beer category — only homebrew-relevant entries and beer cocktails
# Style descriptions (IPA, Stout, Pilsner, etc.) do NOT get recipes
RECIPES = {

9241: """RECIPE — Quick Kettle Sour (Berliner Weisse Method)
Yield: 20 litres | Glassware: Tall Weizen glass | Ice: None
---
4.5kg Pilsner malt (80%) + 1.1kg raw wheat malt (20%)
Water to 20 litre final volume
Lactobacillus plantarum culture (or Wildbrew Sour Pitch by Lallemand)
US-05 or WY1056 yeast for primary fermentation
Target OG: 1.034 | Target pH: 3.3–3.5 | Target ABV: approx. 3.2%
---
1. Mash at 65°C for 60 minutes. Lauter and collect wort in kettle.
2. Boil 10 minutes — pasteurise. Cool wort to 38–40°C. Do NOT hop yet.
3. Pitch Lactobacillus. Purge kettle headspace with CO₂ (prevents acetic acid production).
4. Sour 16–24 hours at 38–40°C. Target pH 3.3–3.5 (check with pH meter, not strips).
5. Boil full 60 min with 20g Hallertau Mittelfrüh hops (bittering only — 10 IBU). Cool to 20°C.
6. Pitch primary yeast. Ferment 7–10 days. Bottle or keg.
---
Garnish: Lemon wheel on the rim; dash of raspberry syrup (Schuss) is traditional
Temperature: Serve at 5–7°C; Berliner Weisse is always served very cold and very pale

""",

9248: """RECIPE — Bourbon Barrel-Aged Imperial Stout (Homebrew)
Yield: 20 litres | Glassware: Snifter | Ice: None
---
GRAIN BILL: 5kg Golden Promise (59%) + 1kg Chocolate Malt + 500g Black Patent + 500g Crystal 120L + 500g Roasted Barley + 200g Cara-Munich
HOPS: 80g Magnum (bittering, 60 min) — target 60 IBU
YEAST: Wyeast 1056 American Ale or US-05
OG: 1.110 | FG: 1.022 | ABV: 11.5%
---
1. Mash at 68°C for 75 minutes (higher temp for full body in imperial stout).
2. Collect wort. Boil 90 minutes — first wort hop with Magnum at 60 minutes.
3. Cool to 20°C. Pitch large yeast starter (150 billion cells for high gravity).
4. Primary ferment 14–21 days at 20°C. Ramp to 22°C in final 3 days for attenuation.
5. BARREL AGING: rack into sanitised bourbon barrel (or secondary with oak spiral + 60ml bourbon).
6. Age 4–12 weeks. Taste every 2 weeks — oak integrates quickly. Bottle at desired wood character.
---
Garnish: No garnish — served neat in a snifter, 8°C, in 330ml bottles aged minimum 3 months
Temperature: 10–14°C; barrel-aged stouts open up beautifully at cellar temperature

""",

9273: """RECIPE — Raspberry-Dry-Hopped IPA (Fruit Adjunct Addition)
Yield: 20 litres | Glassware: IPA glass or tulip | Ice: None
---
BASE PALE ALE (19 litres, fermented): target OG 1.055, ABV 5.5%, light bitterness (35 IBU)
FRUIT ADDITION: 1.5kg fresh or frozen raspberries (per 20L batch)
DRY HOP: 30g Citra + 20g Galaxy (added during dry hop stage)
---
1. Brew a clean pale ale base: 4.5kg Pale Malt + 500g Munich. Mash 65°C/60 min.
2. Primary fermentation complete (7–10 days at 19°C). FG reached.
3. FRUIT ADDITION: freeze raspberries (kills wild yeast). Thaw. Add to secondary vessel.
4. Rack beer onto raspberries. Ferment 5–7 days — raspberry sugars re-ferment (gravity drops 4–6 pts).
5. DRY HOP: add Citra and Galaxy. Wait 4–5 days at 18°C. Do not remove hops until final gravity stable.
6. Cold crash 48 hours at 2°C. Package carefully — significant CO₂ from fruit sugar fermentation.
---
Garnish: Raspberry on the rim; foam should be light pink-tinged
Temperature: 4–6°C; serve fresh — fruit IPAs do not age well (drink within 6–8 weeks)

""",

9278: """RECIPE — Spontaneous Farmhouse Ale (Coolship-Style)
Yield: 10 litres | Glassware: Wide-mouthed tumbler or lambic tulip | Ice: None
---
2.5kg Pilsner malt (60%) + 1.5kg unmalted raw wheat (40%)
10g aged, low-alpha hops (Goldings or Hallertau, 3+ years old — for preservation only)
Wild yeast and bacteria from the environment (NO commercial yeast pitched)
---
1. Turbid mash method: mash at 45°C/15 min, then 62°C/15 min, then 72°C/30 min. Collect turbid, starchy wort.
2. Boil 3 hours (reducing volume concentrates wort). Add aged hops at 60 minutes.
3. COOLSHIP: pour hot wort into a shallow open vessel (coolship or large enamel roasting pan). Leave uncovered overnight — ideally October through March, outdoor temp 3–8°C.
4. Wild Brettanomyces, Pediococcus, and Acetobacter inoculate the wort overnight.
5. Transfer to a 20-litre oak barrel or demijohn. Age 12–36 months without disturbance.
6. Blend batches of different ages (3:2:1 ratio old:medium:young) for final gueuze-style balance.
---
Garnish: No garnish; fruit (kriek: 200g cherries per litre) can be added at 6 months for a kriek variant
Temperature: 10–14°C; wild ales need bottle conditioning — 3–6 months minimum after bottling

""",

9279: """RECIPE — Millet and Buckwheat Gluten-Free Pale Ale
Yield: 20 litres | Glassware: Pint glass | Ice: None
---
3.5kg millet malt (Grouse Malt or Eckert Malting; 70%) + 1kg buckwheat malt (20%) + 500g rice hulls (lautering aid, 10%)
HOPS: 30g Cascade (60 min) + 30g Mosaic (0 min) + 30g Citra (dry hop)
YEAST: Lallemand Nottingham or SafAle US-05
ENZYMES: Beano or White Labs Clarity Ferm (aids millet fermentability)
---
1. Add Beano tablets (2–3 crushed) to mash water at dough-in — millet starches need exogenous enzymes.
2. Mash at 64°C for 90 minutes (longer than barley to fully convert millet starch).
3. Add rice hulls — improves lauter flow through glutinous millet grain bed.
4. Collect wort (clear, golden). Boil 60 min. Add Cascade at 60 min; Mosaic at 0 min.
5. Ferment 14 days at 18–20°C. Dry hop with Citra for 4–5 days.
6. Cold crash. Package. Confirm gluten-free status with ELISA test strip (<10ppm for certified GF).
---
Garnish: Lemon wedge (traditional pub pale ale style)
Temperature: 4–6°C; gluten-free beers often best slightly cooler than barley equivalents

""",

9288: """RECIPE — Sahti (Finnish Farmhouse Rye Beer with Juniper)
Yield: 15 litres | Glassware: Wooden keg-cup (haapakiulu) or large mug | Ice: None
---
3.5kg malted barley (basic pale malt) + 1kg rye malt + 500g rye bread crust (traditional starch source)
50g juniper branches (fresh — needles and branches; not juniper berries)
1 tsp bakers yeast (traditional: dry Fleischmann's; commercial: Wyeast 3638 Bavarian Wheat)
Sauna birch whisk or juniper filter (kuurna) for traditional lautering
---
1. JUNIPER INFUSION: boil 2 litres water with juniper branches 20 minutes. Strain. Reserve spiced water.
2. Mash all grain at 68°C using the juniper water + additional hot water. Mash 60–90 minutes.
3. LAUTERING: Sahti traditionally uses a kuurna (trough) lined with juniper branches as a filter bed. Modern: voile bag in a bucket with holes.
4. Collect wort. Sahti is NOT boiled — this preserves raw grain character and yeast viability.
5. Cool to 35°C. Pitch baker's yeast dissolved in warm water. Ferment 1–3 days at 20–25°C.
6. Sahti is ready quickly — extremely perishable. Drink within 1 week. Traditional competitions are same-day.
---
Garnish: No garnish; served with smoked sausage (makkara) and dark bread at Midsummer festivals
Temperature: 12–15°C; never cold — Sahti is a warm farmhouse drink

""",

9299: """RECIPE — Habanero-Honey Beer (Chili and Spice Craft Beer)
Yield: 20 litres | Glassware: Pint glass | Ice: None
---
4.5kg Maris Otter pale malt + 500g Munich
HOPS: 25g Centennial (60 min) — 30 IBU base
ADJUNCTS: 500g wildflower honey (added to kettle at flameout)
SPICE: 2–4 fresh habanero peppers, halved (added at cold crash or secondary — start with 2, taste and add)
YEAST: WY1056 or US-05 — clean, neutral to let the chili and honey shine
---
1. Mash at 65°C/60 min. Collect wort. Boil 60 minutes with Centennial.
2. At flameout (0 min): add honey. Stir to dissolve. Chill quickly.
3. Primary ferment 10–14 days at 18°C.
4. CHILI ADDITION: at cold crash, add halved habaneros (seeds in = more heat, seeds removed = fruity heat).
5. Taste every 12 hours. Remove chilies when heat is present but not overwhelming — 24–48 hours usually.
6. Package. The heat intensifies slightly with carbonation — err on the side of mild.
---
Garnish: No garnish for chili beer; serve with aged cheddar or smoked charcuterie
Temperature: 4–6°C; cold serving reduces perceived heat slightly — important calibration

""",

9300: """RECIPE — Cyser (Apple Honey Mead)
Yield: 5 litres | Glassware: Wine glass or goblet | Ice: None
---
1.5kg raw local honey (wildflower; monofloral creates more varietal character)
2 litres fresh-pressed apple juice (unfiltered — cloudy, local orchard; NOT pasteurised concentrate)
2 litres cold filtered water
1 packet Lalvin 71B yeast (fruit-forward; softens malic acid in apple)
1 tsp yeast nutrient (Fermaid-O; staggered nutrient additions recommended)
---
1. Sanitise all equipment with Star San (no-rinse). Mix honey, apple juice, and water.
2. Target starting gravity: 1.080–1.085 (medium cyser, finishes at approx. 10–11% ABV).
3. Add yeast nutrient (½ dose now). Pitch rehydrated yeast.
4. Staggered nutrients (TOSNA method): add remaining nutrient at 24h, 48h, and 72h.
5. Primary ferment 21–28 days at 18–20°C. Rack to secondary when gravity stable.
6. Age 2–6 months. Cyser benefits from ageing — apple mellows and honey integrates.
---
Garnish: Cinnamon stick in glass; apple slice on rim; serve as a light semi-sweet dessert wine
Temperature: 8–12°C; dry versions at 10°C, sweet versions at 12°C

""",

9306: """RECIPE — Traditional Hard Cider (Semi-Dry English Style)
Yield: 5 litres | Glassware: Pint glass or dimpled mug | Ice: None
---
5 litres fresh apple juice (freshly pressed, unfiltered — Bulmers or local orchard; mix of bitter-sharp and sweet varieties for complexity)
Campden tablet (potassium metabisulphite, 1 crushed per 5L — inhibits wild yeast and bacteria)
1 packet cider yeast (Lallemand Belle Saison or Red Star Cote des Blancs for fruity; EC-1118 for dry)
Optional: 100g brown sugar at fermentation for elevated ABV
---
1. 24 HOURS BEFORE: Crush Campden tablet into fresh-pressed juice. Stir. Cover loosely. Allow 24h for sulphur to off-gas.
2. Pitch cider yeast (rehydrated per packet instructions). For wild cider: omit Campden and yeast — rely on native apple yeast.
3. Ferment at 15–18°C (cooler = more aromatic, slower). Primary: 14–21 days.
4. Taste from day 10. Dry cider: ferment to terminal gravity (approx. 1.005–1.000). Semi-dry: stop at 1.010.
5. Rack to secondary. Cold crash 48 hours. Fine with isinglass if clarity needed.
6. Bottle condition (1 tsp sugar per 500ml for moderate carbonation) or keg.
---
Garnish: No garnish for traditional cider; cinnamon stick for mulled cider
Temperature: 8–12°C for still cider; 6–8°C for sparkling cider

""",

9307: """RECIPE — Birch Kvass (Baltic Spring Variant)
Yield: 1.5 litres | Glassware: Tall glass or mug | Ice: None
---
250g rye bread (dark Borodinsky or pumpernickel), sliced and toasted very dark
300ml fresh birch sap (collected in early spring, or substitute clear apple juice for year-round)
1 litre boiling water
80g sugar or raw honey
5g active dry yeast
Optional: 10g fresh or dried mint; strip of lemon peel
---
1. Toast bread until very dark (near charred). This is the colour and caramel source.
2. Pour boiling water over toasted bread. Steep until cooled (room temperature).
3. Strain. Add birch sap (or apple juice substitute), sugar/honey, mint, and lemon.
4. Cool to 25°C. Add yeast dissolved in 2 tbsp warm water. Stir.
5. Ferment loosely covered 8–12 hours at room temperature. Taste from 8 hours.
6. Strain and bottle. Refrigerate — drink within 5 days. Birch kvass is naturally fresh and delicate.
---
Garnish: Sprig of fresh birch leaf (seasonal); lemon slice; mint sprig
Temperature: 4–6°C; serve very cold for maximum freshness

""",

9308: """RECIPE — Chicha de Jora (Traditional Fermented Corn Beer)
Yield: 2 litres | Glassware: Ceramic cup or wooden bowl | Ice: None
---
500g jora corn (germinated, dried, and toasted Andean corn; from Latin grocery) OR substitute malted corn/maize
2 litres water
100g piloncillo or brown sugar (optional — native versions are unsweetened)
1 cinnamon stick + 5 cloves + 3 star anise (optional spice additions)
Wild yeast (native; no commercial yeast added in traditional method)
---
1. Grind jora corn coarsely — not to flour. Combine with water in a large clay pot.
2. Simmer 2–3 hours, stirring frequently. The liquid becomes opaque and starchy.
3. Add spices if using. Simmer 30 more minutes.
4. Remove from heat. Cool to room temperature. Sweeten with piloncillo if desired.
5. Transfer to ceramic vessel. Cover loosely. Leave at room temperature 48–72 hours.
6. Wild fermentation begins — taste from 48 hours. Ready when pleasantly sour, mildly fizzy, and sweet-starchy (2–4% ABV).
---
Garnish: Served in clay cups; no garnish — the earthenware IS the presentation
Temperature: Room temperature or slightly cool (18–20°C); always consumed fresh

""",

9309: """RECIPE — Water Kefir Beer (Probiotic Fermented Beverage)
Yield: 1 litre | Glassware: Highball or mason jar | Ice: Cubed
---
1 litre filtered water (chlorine-free; use bottled or let tap water rest 30 min)
60g cane sugar (feeds the grains)
3 tbsp water kefir grains (live; Cultures for Health)
2 dried figs (adds minerals and natural yeast)
SECONDARY FERMENT FLAVOURING (choose one):
- 200ml fresh ginger juice + 50ml lemon (Ginger Beer style)
- 200ml grape juice (wine-adjacent profile)
- 200ml blueberry juice (anthocyanin-rich)
---
1. Dissolve sugar in 200ml warm water. Cool. Combine with remaining cold water.
2. Add kefir grains and figs. Cover loosely with breathable cloth.
3. Ferment 24–48 hours at 22°C. Taste from 36 hours — should be tangy, lightly sweet, faintly fizzy.
4. Strain. Reserve grains for next batch.
5. SECOND FERMENT: add chosen flavouring. Seal tightly in swing-top bottle. 12–24 hours at room temp.
6. Refrigerate. Open slowly over a sink — significant natural carbonation.
---
Garnish: Per flavour: ginger version → lime wedge + crystallised ginger; grape → frozen grapes
Temperature: 4–6°C; consume within 1 week (probiotics most active when fresh)

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
    print(f"Done. {len(RECIPES) - errors} Beer (selective) recipes added, {errors} errors.")

if __name__ == "__main__":
    main()
