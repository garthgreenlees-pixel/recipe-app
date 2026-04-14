#!/usr/bin/env python3
"""Terminal 8 — Batch 1: US Bourbon + Tequila/Mezcal Depth"""
import psycopg2, psycopg2.extras, json
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, REF, PAIR

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn2 = psycopg2.connect(CONN)
conn2.autocommit = True
cur2 = conn2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

KENTUCKY = 82
TENNESSEE = 83
JALISCO   = 100
OAXACA    = 99

def P(name, producer_type, region_id, country="USA",
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur2.execute("SELECT id FROM beverage_producers WHERE name = %s", (name,))
    row = cur2.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    philo_short = (production_philosophy or "")[:100] or None
    cur2.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details,
           reputation_narrative, price_positioning, authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE) RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          reputation_narrative, price_positioning, authority_tier))
    row = cur2.fetchone()
    print(f"  ✓ {name} (id={row['id']})")
    return row['id']

def PROD(name, category, producer_id, region_id, origin_country="USA",
         subcategory=None, description=None,
         quality_hierarchy=None, deductive_profile=None, service_specs=None,
         flavour_markers=None, flavour_weight=None, flavour_profile_type=None,
         price_tier=None, price_range_cad=None, technical_specs=None):
    cur2.execute("SELECT id FROM beverage_products WHERE name = %s AND producer_id = %s",
                (name, producer_id))
    row = cur2.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    cur2.execute("""
        INSERT INTO beverage_products
          (name, category, producer_id, region_id, origin_country,
           subcategory, description, quality_hierarchy,
           deductive_profile, service_specs, flavour_markers,
           flavour_weight, flavour_profile_type,
           price_tier, price_range_cad, technical_specs, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE) RETURNING id
    """, (name, category, producer_id, region_id, origin_country,
          subcategory, description,
          json.dumps(quality_hierarchy) if quality_hierarchy else None,
          json.dumps(deductive_profile) if deductive_profile else None,
          json.dumps(service_specs) if service_specs else None,
          flavour_markers, flavour_weight, flavour_profile_type,
          price_tier, price_range_cad,
          json.dumps(technical_specs) if technical_specs else None))
    row = cur2.fetchone()
    print(f"  ✓ {name} (id={row['id']})")
    return row['id']

# ─── US BOURBON PRODUCERS ──────────────────────────────────────────────────────
print("=== US BOURBON PRODUCERS ===")

makers_mark = P("Maker's Mark Distillery", "distillery", KENTUCKY,
    production_philosophy="Smooth handcrafted bourbon: wheat instead of rye, hand-dipped red wax.",
    philosophy_description=(
        "Maker's Mark (est. 1953) pioneered the 'wheated bourbon' style — substituting wheat "
        "for the traditional rye grain in the mash bill, creating a softer, smoother, sweeter "
        "bourbon without rye's spice. The recipe: 70% corn, 16% wheat, 14% malted barley. "
        "Every bottle is hand-dipped in the iconic red wax seal — a visual signature "
        "that made bourbon accessible and premium simultaneously. "
        "The distillery uses a rotating barrel warehouse system to ensure every barrel "
        "experiences similar temperature variation."
    ),
    key_personnel=[
        {"name": "Bill Samuels Jr.", "role": "Chairman Emeritus"},
        {"name": "Mika Samuels", "role": "Current VP"}
    ],
    production_details={
        "mash_bill": "70% corn, 16% red winter wheat, 14% malted barley",
        "style": "Wheated bourbon — no rye grain",
        "maturation": "New charred American white oak barrels, rotated in warehouse",
        "brands": "Maker's Mark, Maker's 46 (seared oak stave finish), Cask Strength"
    },
    reputation_narrative=(
        "Maker's Mark created the premium bourbon category in the 1950s when bourbon sales "
        "were declining. The red wax and wheated mash bill differentiated it from every "
        "competitor. Now owned by Beam Suntory, it remains Kentucky's most recognisable brand."
    ),
    price_positioning="mid_range",
    authority_tier=1)

woodford = P("Woodford Reserve Distillery", "distillery", KENTUCKY,
    production_philosophy="Triple distillation, copper pot stills, five grain sources: craft bourbon.",
    philosophy_description=(
        "Woodford Reserve (est. 1996 on historic Labrot & Graham site, c.1812) is the most "
        "craft-focused of Brown-Forman's bourbon portfolio — triple-distilled in copper pot stills "
        "(unique in bourbon) rather than the standard column still method. "
        "The mash bill (72% corn, 18% rye, 10% malt) produces a higher-rye spice profile, "
        "and the triple distillation adds smoothness without lightness. "
        "Maturation in a limestone cellar creates slow, consistent aging."
    ),
    key_personnel=[
        {"name": "Chris Morris", "role": "Master Distiller"},
        {"name": "Elizabeth McCall", "role": "Assistant Master Distiller"}
    ],
    production_details={
        "mash_bill": "72% corn, 18% rye, 10% malted barley",
        "distillation": "Triple distillation in copper pot stills — unique in Kentucky bourbon",
        "maturation": "New charred American white oak, limestone cellar warehouse",
        "brands": "Woodford Reserve, Double Oaked, Batch Proof, Masters Collection"
    },
    reputation_narrative=(
        "Woodford Reserve Double Oaked is the distillery's most celebrated expression: "
        "second maturation in heavily toasted, lightly charred new barrels adds "
        "vanilla, chocolate, and caramel intensity. "
        "The Official Bourbon of the Kentucky Derby since 1999."
    ),
    price_positioning="premium",
    authority_tier=1)

four_roses = P("Four Roses Distillery", "distillery", KENTUCKY,
    production_philosophy="10 distinct bourbon recipes from 2 mash bills x 5 yeast strains.",
    philosophy_description=(
        "Four Roses (est. 1888, revived as premium brand by Japanese ownership 2002) is unique "
        "in American whiskey: it uses 2 different mash bills crossed with 5 different proprietary "
        "yeast strains, creating 10 distinct bourbon recipes blended together to achieve "
        "a nuanced, complex house style. The Low Rye mash bill (60% corn, 20% rye, 20% malt) "
        "and High Rye mash bill (75% corn, 20% rye, 5% malt) represent the two base styles; "
        "the 5 yeast strains each contribute different ester characters."
    ),
    key_personnel=[
        {"name": "Brent Elliott", "role": "Master Distiller"}
    ],
    production_details={
        "mash_bills": "Two: Low (60/20/20) and High Rye (75/20/5)",
        "yeast_strains": "5 proprietary strains — each produces different ester character",
        "recipes": "10 distinct recipes (OESO, OESK, OESV, etc.)",
        "brands": "Four Roses Yellow Label, Small Batch, Small Batch Select, Single Barrel"
    },
    reputation_narrative=(
        "Four Roses Single Barrel is widely considered the most complex everyday bourbon "
        "available — each barrel shows a different expression of the 10-recipe system. "
        "The Limited Edition Small Batch (annual) achieves 96-98 points consistently. "
        "Kirin Brewery (Japan) ownership since 2002 explains the meticulous quality focus."
    ),
    price_positioning="premium",
    authority_tier=1)

wild_turkey = P("Wild Turkey Distillery", "distillery", KENTUCKY,
    production_philosophy="High rye, high proof, traditional Kentucky bourbon — no shortcuts.",
    philosophy_description=(
        "Wild Turkey (est. 1869, Lawrenceburg KY) is the most traditional of Kentucky's "
        "major bourbon distilleries — a high-rye mash bill (13% rye vs. Maker's 16% wheat), "
        "entering the barrel at a lower proof than most competitors (110 proof vs. 125 legal max), "
        "and aged in 'alligator char' (deep char level 4) barrels. "
        "The lower entry proof preserves more congeners from the distillate; "
        "the deep char extracts maximum vanilla and caramel from the wood. "
        "Master Distiller Jimmy Russell has worked at Wild Turkey for over 60 years — "
        "the longest-tenured master distiller in the world."
    ),
    key_personnel=[
        {"name": "Jimmy Russell", "role": "Master Distiller — longest tenure in bourbon history (60+ years)"},
        {"name": "Eddie Russell", "role": "Master Distiller — Jimmy's son"}
    ],
    production_details={
        "mash_bill": "75% corn, 13% rye, 12% malted barley",
        "entry_proof": "110 proof — lower than most (preserves congeners)",
        "char_level": "Alligator char #4 — deepest char level",
        "brands": "Wild Turkey 81, 101, Rare Breed (cask strength), Longbranch, Russell's Reserve"
    },
    reputation_narrative=(
        "Wild Turkey Rare Breed (cask strength, ~56%) is consistently rated 95+ points and "
        "cited as the finest value in bourbon. Jimmy Russell's 60+ years is an unmatched record "
        "in any spirits category globally. Matthew McConaughey became Creative Director in 2016."
    ),
    price_positioning="mid_range",
    authority_tier=1)

# ─── US BOURBON PRODUCTS ───────────────────────────────────────────────────────
print("\n=== US BOURBON PRODUCTS ===")

p1 = PROD("Maker's Mark Kentucky Straight Bourbon", "spirits_whiskey", makers_mark, KENTUCKY,
    subcategory="Kentucky Straight Bourbon — Wheated",
    description=(
        "Maker's Mark is the bourbon that created the premium category — a wheated bourbon "
        "(wheat replaces rye) producing a softer, sweeter style that broadened bourbon's appeal "
        "in the 1950s when the category was in decline. The 90-proof expression (45% ABV) "
        "in the hand-dipped red wax bottle is one of the world's most recognisable spirits. "
        "The wheated mash bill delivers vanilla, caramel, and wheat bread sweetness without "
        "rye spice — making it the most approachable Kentucky bourbon and the standard "
        "recommendation for new bourbon drinkers."
    ),
    flavour_markers=["vanilla", "caramel", "wheat bread", "honey", "light oak", "sweet corn", "butterscotch"],
    flavour_weight="medium",
    flavour_profile_type="wheated_approachable_bourbon",
    deductive_profile={
        "colour": "Amber-gold",
        "nose": "Sweet and inviting — vanilla, caramel, wheat bread, honey",
        "palate": "Smooth and medium-bodied — caramel, vanilla, sweet corn, gentle oak",
        "finish": "Medium, clean, vanilla and butterscotch"
    },
    service_specs={
        "serve_temp": "Neat, rocks, or in an Old Fashioned",
        "glassware": "Rocks glass or tulip",
        "notes": "The ideal bourbon for an Old Fashioned: the wheated sweetness balances "
                 "the bitters without spice competition."
    },
    price_tier="mid_range",
    price_range_cad="$50-62",
    technical_specs={"abv": 45.0, "age": "Minimum 5-6 years (NAS)", "mash_bill": "70% corn, 16% wheat, 14% malt", "char": "Level 3"})

p2 = PROD("Woodford Reserve Double Oaked", "spirits_whiskey", woodford, KENTUCKY,
    subcategory="Kentucky Straight Bourbon — Double Oaked",
    description=(
        "Woodford Reserve Double Oaked undergoes two separate maturation periods: first in "
        "standard new charred American white oak, then a second maturation in deeply toasted, "
        "lightly charred new white oak barrels. The second barrel — toasted for longer at lower "
        "temperature — extracts maximum wood sugars (vanillin, caramel polymers) without the "
        "bitter tannin of full charring. The result is the most vanilla-rich, chocolate-intense, "
        "caramel-saturated bourbon in standard production — a dessert in a glass. "
        "Consistently 94-96 points from major competitions."
    ),
    flavour_markers=["dark chocolate", "vanilla", "caramel", "toasted oak", "dried fruit", "honey", "butterscotch"],
    flavour_weight="full",
    flavour_profile_type="double_oaked_rich_bourbon",
    deductive_profile={
        "colour": "Deep mahogany-amber",
        "nose": "Rich and sweet — dark chocolate, vanilla, caramel, toasted oak",
        "palate": "Full and luscious — chocolate, vanilla, caramel, dried fruit, honey",
        "finish": "Long, warming, vanilla and chocolate"
    },
    service_specs={
        "serve_temp": "Neat; one large ice cube acceptable",
        "glassware": "Rocks glass or Glencairn",
        "notes": "Outstanding dessert bourbon — pairs with chocolate preparations. "
                 "An excellent Old Fashioned where the vanilla does the talking."
    },
    price_tier="premium",
    price_range_cad="$80-95",
    technical_specs={"abv": 43.2, "age": "NAS (first maturation ~6 years, second additional period)", "distillation": "Triple distilled copper pot still", "maturation": "Two periods in new charred and new toasted oak"})

p3 = PROD("Four Roses Single Barrel", "spirits_whiskey", four_roses, KENTUCKY,
    subcategory="Kentucky Straight Bourbon — Single Barrel",
    description=(
        "Four Roses Single Barrel represents the pinnacle of the 10-recipe system: "
        "individual barrels from a single recipe (typically OBSV or OESV — the higher ester "
        "yeast strains) bottled at 50% ABV without reduction or blending. "
        "The result varies by barrel but consistently delivers fruit-forward, spice-rich "
        "complexity: rose petal, raspberry, vanilla, and rye spice are the characteristic notes "
        "from the high-ester yeast strains. "
        "Each bottle carries the warehouse location, barrel number, and recipe code — "
        "making it among the most transparent American whiskies produced."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Four Roses Yellow Label", "notes": "Entry: blend of all 10 recipes"},
        {"rank": 2, "expression": "Four Roses Small Batch", "notes": "4 selected recipes blended"},
        {"rank": 3, "expression": "Four Roses Single Barrel", "notes": "Single recipe, single barrel at 50%"},
        {"rank": 4, "expression": "Four Roses Limited Edition Small Batch", "notes": "Annual release; 96-98 points"}
    ],
    flavour_markers=["rose petal", "raspberry", "vanilla", "rye spice", "cinnamon", "light honey", "dried herb"],
    flavour_weight="medium-full",
    flavour_profile_type="fruit_spice_bourbon",
    deductive_profile={
        "colour": "Copper-amber",
        "nose": "Floral and fruit-forward — rose petal, raspberry, vanilla, gentle spice",
        "palate": "Medium-full — raspberry, vanilla, rye spice, cinnamon, clean oak",
        "finish": "Medium-long, fruit and spice fading"
    },
    service_specs={
        "serve_temp": "Neat or with a single ice cube",
        "glassware": "Glencairn or rocks glass",
        "notes": "The recipe code on the bottle (e.g., OBSV, OESV) tells an expert guest "
                 "exactly what to expect — V yeast = high ester, most fruit-forward."
    },
    price_tier="premium",
    price_range_cad="$75-90",
    technical_specs={"abv": 50.0, "age": "Minimum 7-9 years (single barrel)", "mash_bill": "Variable by recipe (Low or High Rye)", "yeast_strain": "Single barrel — typically high-ester V or F strain"})

p4 = PROD("Wild Turkey Rare Breed Cask Strength", "spirits_whiskey", wild_turkey, KENTUCKY,
    subcategory="Kentucky Straight Bourbon — Cask Strength",
    description=(
        "Wild Turkey Rare Breed is the distillery's cask strength expression — bottled without "
        "water reduction at approximately 56-58.4% ABV (the proportion varies by batch). "
        "The combination of Wild Turkey's high-rye mash bill, low entry proof (110), "
        "and alligator char at full strength creates one of the most complex and powerful "
        "everyday American whiskies: vanilla and caramel from deep char are amplified by "
        "full ABV concentration, while the rye spice provides structure. "
        "Consistently cited as the best value in cask-strength bourbon — under $80 CAD. "
        "Consistently 95+ points from all major competitions."
    ),
    flavour_markers=["vanilla", "caramel", "rye spice", "dark fruit", "alligator char", "honey", "cinnamon"],
    flavour_weight="full",
    flavour_profile_type="cask_strength_high_rye_bourbon",
    deductive_profile={
        "colour": "Deep amber",
        "nose": "Powerful and rich — vanilla, caramel, rye spice, dark fruit, honey",
        "palate": "Full and warming — vanilla, rye spice, dark fruit, alligator char sweetness",
        "finish": "Very long, warming, spice and vanilla, persistent"
    },
    service_specs={
        "serve_temp": "Neat with water available; never on ice",
        "glassware": "Glencairn",
        "notes": "At 56%+, water addition (10-15ml) is not a compromise — "
                 "it opens the vanilla and caramel significantly."
    },
    price_tier="mid_range",
    price_range_cad="$65-78",
    technical_specs={"abv": "56-58.4% batch variable", "age": "Blend of 6, 8, and 12 year stocks", "mash_bill": "75% corn, 13% rye, 12% malt", "char": "Alligator char #4", "entry_proof": 110})

# ─── TEQUILA PRODUCERS ─────────────────────────────────────────────────────────
print("\n=== TEQUILA/MEZCAL PRODUCERS ===")

don_julio = P("Tequila Don Julio", "distillery", JALISCO, "Mexico",
    production_philosophy="Estate-grown blue Weber agave: the luxury tequila standard.",
    philosophy_description=(
        "Tequila Don Julio (est. 1942 by Don Julio González) was the first luxury tequila — "
        "created in a shorter, wider bottle so the dinner table conversation could continue "
        "over the label. Don Julio González pioneered the concept of highland Jalisco agave "
        "(Los Altos region, 2,000m elevation) producing smaller, denser, fruitier piñas "
        "than lowland agave — the defining characteristic of the Don Julio style. "
        "Now owned by Diageo; remains the world's top-selling premium tequila."
    ),
    key_personnel=[
        {"name": "Don Julio González", "role": "Founder (1942-2012)"},
        {"name": "Diageo production team", "role": "Current ownership/production"}
    ],
    production_details={
        "agave": "Blue Weber agave, highland Jalisco (Los Altos), 7-10 years maturation",
        "cooking": "Autoclave steam cooking",
        "distillation": "Double distillation, column still",
        "brands": "Don Julio Blanco, Reposado, Añejo, 1942, Real (ultra-premium)"
    },
    reputation_narrative=(
        "Don Julio 1942 is the world's most recognisable premium tequila — the bottle shape "
        "(commemorating the founding year) appears at celebrity events globally. "
        "Don Julio Blanco is the benchmark for highland Jalisco tequila."
    ),
    price_positioning="premium",
    authority_tier=1)

clase_azul = P("Clase Azul Spirits", "distillery", JALISCO, "Mexico",
    production_philosophy="Ultra-premium: handcrafted Talavera ceramic decanters, slow-cooked agave.",
    philosophy_description=(
        "Clase Azul (est. 1997) produces ultra-premium tequila in handmade Talavera ceramic "
        "decanters — each bottle is a collector's item with painted artisan decoration. "
        "The tequila itself matches the vessel: highland Blue Weber agave, slow-cooked in "
        "traditional brick ovens (rather than industrial autoclaves), fermented with proprietary "
        "yeast, and double-distilled. The result is among the fruitiest and most complex "
        "añejo tequilas produced — highly sought by collectors and luxury buyers."
    ),
    key_personnel=[
        {"name": "Arturo Lomeli", "role": "Founder and CEO"}
    ],
    production_details={
        "agave": "Highland Blue Weber agave (Jalisco highlands)",
        "cooking": "Brick oven slow-cooking (traditional) — not autoclaved",
        "vessel": "Handpainted Talavera ceramic decanters — each hand-decorated",
        "brands": "Clase Azul Plata, Reposado, Añejo, Ultra (25-year añejo)"
    },
    reputation_narrative=(
        "Clase Azul Reposado is the world's best-selling ultra-premium tequila by value. "
        "The Ultra ($1,500+ per bottle) is one of the world's most expensive tequilas. "
        "The ceramic bottles are often collected and repurposed as decanters independently."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

el_silencio = P("El Silencio Mezcal", "distillery", OAXACA, "Mexico",
    production_philosophy="Accessible craft mezcal: espadin agave, Oaxacan tradition made approachable.",
    philosophy_description=(
        "El Silencio (est. 2012) represents the accessible end of the artisanal mezcal movement — "
        "produced in Oaxaca using traditional espadin agave (the most common mezcal variety), "
        "earth-pit roasting, and copper still distillation. While not as artisanal as Del Maguey's "
        "village-specific productions, El Silencio made quality mezcal accessible to the US market "
        "at a price point that enabled mainstream cocktail programs to serve it. "
        "The smoke character is present but more integrated than wild-caught agave mezcal."
    ),
    key_personnel=[
        {"name": "Ignacio Alvarado", "role": "Co-founder"}
    ],
    production_details={
        "agave": "Espadin (Agave angustifolia) — most common mezcal variety",
        "roasting": "Underground earth pit, firewood — traditional method",
        "distillation": "Double distillation, copper stills",
        "brands": "El Silencio Espadin, Joven, Madre Cuishe"
    },
    reputation_narrative=(
        "El Silencio is the gateway mezcal for bartenders entering the category — "
        "approachable smoke, affordable pricing, and consistent quality. "
        "Its growth helped establish mezcal as a mainstream cocktail spirit in North America."
    ),
    price_positioning="mid_range",
    authority_tier=1)

# ─── TEQUILA/MEZCAL PRODUCTS ───────────────────────────────────────────────────
print("\n=== TEQUILA/MEZCAL PRODUCTS ===")

p5 = PROD("Don Julio 1942 Añejo", "spirits_agave", don_julio, JALISCO, "Mexico",
    subcategory="Highland Jalisco Añejo Tequila",
    description=(
        "Don Julio 1942 is the most recognisable premium tequila in the world — named for "
        "the year Don Julio González began distilling. It is an añejo tequila aged for "
        "a minimum of 2.5 years in American white oak barrels, at the Highland Jalisco "
        "altitude where the cooler temperature creates slower, more complex aging. "
        "The result is tequila of extraordinary richness: vanilla, caramel, dark chocolate, "
        "and the residual agave sweetness that highland piñas develop — all integrated "
        "through 30 months of American oak aging. "
        "The tall, distinctive bottle with the hand-numbered tag is the "
        "VIP table's tequila of choice globally."
    ),
    flavour_markers=["vanilla", "caramel", "dark chocolate", "roasted agave", "dried fruit", "honey", "oak spice"],
    flavour_weight="full",
    flavour_profile_type="rich_anejo_highland",
    deductive_profile={
        "colour": "Dark amber",
        "nose": "Rich and complex — vanilla, caramel, roasted agave, dried fruit, dark chocolate",
        "palate": "Full and silky — caramel, vanilla, agave, chocolate, warm oak spice",
        "finish": "Very long, warm, vanilla and agave fade"
    },
    service_specs={
        "serve_temp": "Neat or with one large ice cube",
        "glassware": "Snifter or rocks glass",
        "notes": "This tequila should be sipped, not shot. "
                 "Serve neat at room temperature to appreciate full complexity."
    },
    price_tier="ultra_premium",
    price_range_cad="$175-210",
    technical_specs={"abv": 40.0, "age": "Minimum 30 months añejo", "agave": "Highland Blue Weber, Los Altos Jalisco", "maturation": "American white oak barrels"})

p6 = PROD("Clase Azul Reposado", "spirits_agave", clase_azul, JALISCO, "Mexico",
    subcategory="Highland Jalisco Reposado Tequila — Luxury",
    description=(
        "Clase Azul Reposado is the world's best-selling ultra-premium tequila by value — "
        "aged 8 months in American whiskey barrels and presented in a handpainted Talavera "
        "ceramic decanter. The slow-cooked (brick oven) highland agave produces a fruitier, "
        "more complex spirit than industrially processed competitors; the whiskey cask "
        "aging adds vanilla and caramel without obscuring the agave character. "
        "The ceramic bottle is a collector's item — often retained and repurposed after the "
        "tequila is consumed. Each decanter is individually hand-decorated by Oaxacan artisans."
    ),
    flavour_markers=["fresh agave", "vanilla", "caramel", "pear", "honey", "light oak", "cinnamon"],
    flavour_weight="medium-full",
    flavour_profile_type="reposado_luxury_highland",
    deductive_profile={
        "colour": "Light amber-gold",
        "nose": "Fresh and fruity — agave, pear, vanilla, honey, cinnamon",
        "palate": "Medium-full and smooth — agave sweetness, vanilla, caramel, light oak",
        "finish": "Medium-long, clean, agave and vanilla"
    },
    service_specs={
        "serve_temp": "Neat; occasional rocks for cocktail service",
        "glassware": "Snifter or Glencairn",
        "notes": "The bottle itself is a conversation piece — often displayed on the table during service."
    },
    price_tier="ultra_premium",
    price_range_cad="$140-170",
    technical_specs={"abv": 40.0, "age": "8 months reposado", "agave": "Highland Blue Weber, slow brick oven cooked", "vessel": "Handpainted Talavera ceramic decanter"})

p7 = PROD("El Silencio Espadin Mezcal", "spirits_agave", el_silencio, OAXACA, "Mexico",
    subcategory="Oaxacan Mezcal — Espadin — Approachable Craft",
    description=(
        "El Silencio Espadin is the gateway expression of artisanal Oaxacan mezcal — "
        "made from espadin agave (Agave angustifolia), earth-pit roasted for 3-5 days over "
        "wood fire (creating the characteristic smoke), fermented naturally, and double-distilled "
        "in copper stills. The smoke character is integrated rather than dominant — "
        "softer than Del Maguey's wild-caught agave expressions, making it accessible "
        "for cocktail use and introducing guests to mezcal's defining character. "
        "The worm at the bottom of cheaper mezcal bottles is a marketing gimmick — "
        "not present in quality mezcal like El Silencio."
    ),
    flavour_markers=["smoke", "roasted agave", "citrus", "green herbs", "light floral", "mineral", "cooked vegetable"],
    flavour_weight="medium",
    flavour_profile_type="smoked_espadin_mezcal",
    deductive_profile={
        "colour": "Crystal clear (blanco/joven)",
        "nose": "Smoke and roasted agave, citrus, fresh herbs, mineral",
        "palate": "Medium — smoke, roasted agave, citrus, cooked vegetable sweetness",
        "finish": "Medium, smoke and agave fade with mineral persistence"
    },
    service_specs={
        "serve_temp": "Neat or in a Mezcal Margarita",
        "glassware": "Veladora glass (traditional) or copita",
        "notes": "Serve with an orange slice dusted with sal de gusano (worm salt) — "
                 "the traditional Oaxacan accompaniment to mezcal."
    },
    price_tier="mid_range",
    price_range_cad="$55-68",
    technical_specs={"abv": 40.0, "agave": "Espadin (Agave angustifolia)", "roasting": "Earth pit, 3-5 days over firewood", "distillation": "Double distillation, copper stills"})

conn2.close()
print("\n✅ T8 Batch 1 — US Bourbon + Tequila/Mezcal complete.")

# ─── REFS AND PAIRINGS via medit_helpers ──────────────────────────────────────
print("\n=== REFS AND PAIRINGS ===")
conn3, cur3 = get_conn()

REF(cur3,
    name="American bourbon: mash bills, regions, and style spectrum",
    category="spirits_knowledge",
    description=(
        "American bourbon must be: produced in the USA, mash bill minimum 51% corn, "
        "distilled to no more than 160 proof (80% ABV), matured in new charred American "
        "white oak containers, entered at no more than 125 proof (62.5% ABV). "
        "Kentucky Straight Bourbon additionally requires: minimum 2 years aging in Kentucky. "
        "The mash bill variations create distinct style families: "
        "Wheated (wheat replaces rye): Maker's Mark, Pappy Van Winkle — sweeter, softer "
        "High Rye (18%+ rye): Woodford Reserve, Bulleit — spicier, drier "
        "Standard Rye (10-15%): Four Roses, Wild Turkey, Buffalo Trace — the classic balance "
        "The 'Big Four' distilleries: Buffalo Trace (Sazerac), Brown-Forman (Woodford), "
        "Beam Suntory (Maker's, Knob Creek), Heaven Hill (Elijah Craig, Evan Williams)."
    ),
    key_principles=(
        "The char level (1-4) is critical: Level 3 = sweet/vanilla, Level 4 ('alligator char') = "
        "deep caramel/complex. "
        "Entry proof affects congener retention: lower entry proof = more flavour character. "
        "Wheated vs. ryed: know which your guest prefers — it predicts the style. "
        "The age statement paradox: Kentucky's heat accelerates aging — "
        "a 6-year Kentucky bourbon can match a 12-year Scotch in wood influence. "
        "Angel's share: 3-5% annually in Kentucky's climate (vs. 1-2% in Scotland)."
    ),
    common_mistakes=(
        "Treating Tennessee whiskey as bourbon: Jack Daniel's is charcoal-mellowed (Lincoln County Process) "
        "and self-classifies as 'Tennessee Whiskey' — technically bourbon but chooses not to claim it. "
        "Assuming older = better: beyond 12-15 years, Kentucky's heat can over-oak a bourbon. "
        "Not distinguishing single barrel from small batch: single barrel = one cask, "
        "small batch = selected barrels blended (typically 20-50)."
    ),
    pro_tips=(
        "For a bourbon flight: Maker's Mark (wheated, accessible) → Four Roses Single Barrel "
        "(fruit-forward, medium rye) → Wild Turkey Rare Breed (cask strength, traditional). "
        "Buffalo Trace and Blanton's both come from the same distillery — different mash bills "
        "and barrel locations in the same warehouse produce the style differences."
    ),
    skill_level="intermediate",
    service_context="spirits bar, American restaurant, bourbon dinner",
    authority_tier=1)

REF(cur3,
    name="Tequila and mezcal: agave, production, and the NOM system",
    category="spirits_knowledge",
    description=(
        "Tequila and mezcal are both agave spirits but with critical legal distinctions: "
        "TEQUILA: Must be produced in Jalisco (+ 4 other states), made exclusively from "
        "Blue Weber agave (Agave tequilana), CRT-regulated with NOM (Norma Oficial Mexicana) number. "
        "MEZCAL: Can be produced in 9 designated states (primarily Oaxaca), can use 30+ agave "
        "varieties, CRMO-regulated. 'The worm' is not traditional — it's a marketing gimmick "
        "from the 1950s added to cheaper mezcal. Quality mezcal never contains a worm. "
        "Both are classified by age: Blanco/Joven (unaged), Reposado (2-12 months), "
        "Añejo (1-3 years), Extra Añejo (3+ years). "
        "The NOM number on every tequila bottle identifies the specific distillery — "
        "multiple brands can be produced at the same distillery."
    ),
    key_principles=(
        "Agave takes 7-12 years to mature before harvesting — unlike grain, it is a finite resource. "
        "Cooking method: autoclave (industrial, lighter character) vs. brick oven (traditional, fruitier) "
        "vs. earth pit (mezcal, smoky). "
        "Highland vs. Lowland Jalisco: highland (Los Altos, 2,000m+) = smaller, sweeter, "
        "more fruit-forward agave; lowland (Tequila Valley) = larger, more vegetal, earthier. "
        "Mezcal's smoke: from earth-pit roasting, not from the agave itself — "
        "different from Islay peat smoke in that it is intentional and consistent."
    ),
    common_mistakes=(
        "Assuming all tequila is the same: Don Julio (highland, sweeter) vs. Herradura (lowland, earthier). "
        "Conflating mezcal's smoke with peat smoke — they are different compounds. "
        "Not knowing that Clase Azul's ceramic bottle is handmade — worth explaining to guests."
    ),
    pro_tips=(
        "For a tequila flight: Blanco → Reposado → Añejo from the same producer (Don Julio) "
        "shows how oak transforms the base agave character cleanly. "
        "Mezcal negroni: Del Maguey Vida + Campari + sweet vermouth — the smoke bridges "
        "the bitter and sweet beautifully."
    ),
    skill_level="intermediate",
    service_context="spirits bar, Mexican restaurant, agave tasting",
    authority_tier=1)

# Product IDs (T8 products)
MAKERS    = p1['id'] if isinstance(p1, dict) else None
WOODFORD_DO = p2['id'] if isinstance(p2, dict) else None

# Re-query since p1-p7 are IDs from the cur2 RealDictCursor
conn_q = psycopg2.connect(CONN)
conn_q.autocommit = True
cur_q = conn_q.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Maker''s Mark Kentucky Straight Bourbon'")
MAKERS = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Woodford Reserve Double Oaked'")
WOODFORD_DO = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Four Roses Single Barrel'")
FOUR_ROSES_SB = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Wild Turkey Rare Breed Cask Strength'")
RARE_BREED = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Don Julio 1942 Añejo'")
DON_JULIO_1942 = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'Clase Azul Reposado'")
CLASE_AZUL_REP = cur_q.fetchone()['id']
cur_q.execute("SELECT id FROM beverage_products WHERE name = 'El Silencio Espadin Mezcal'")
EL_SILENCIO = cur_q.fetchone()['id']
cur_q.close()
conn_q.close()

print(f"Product IDs confirmed: Maker's={MAKERS}, Woodford DO={WOODFORD_DO}, 4Roses={FOUR_ROSES_SB}, Rare Breed={RARE_BREED}, DJ1942={DON_JULIO_1942}, ClaseAzul={CLASE_AZUL_REP}, Silencio={EL_SILENCIO}")

# Bourbon pairings
PAIR(cur3,
    food_description="Pecan pie — wheated bourbon's vanilla and caramelised nut mirror",
    food_category="flour_baking", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Maker's Mark's wheated sweetness (vanilla, caramel, butterscotch) finds "
                  "its perfect culinary mirror in pecan pie — the roasted nut echoes the oak, "
                  "the caramel filling mirrors the bourbon's sweetness.",
    product_id=MAKERS,
    food_flavour_profile="caramelised, nutty, sweet, buttery",
    beverage_category="spirits_whiskey")

PAIR(cur3,
    food_description="Dark chocolate brownie with sea salt — Double Oaked's intensity",
    food_category="chocolate_confection", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Woodford Reserve Double Oaked's dark chocolate and caramel notes find "
                  "direct complementarity in a rich brownie — the sea salt accent provides "
                  "the same contrast the oak tannin provides in the whiskey.",
    product_id=WOODFORD_DO,
    food_flavour_profile="dark, bitter, sweet, salty",
    beverage_category="spirits_whiskey")

PAIR(cur3,
    food_description="Cornbread with honey butter — fruit-forward bourbon meets American grain",
    food_category="flour_baking", meal_context="casual",
    confidence="established", pairing_type="complement",
    flavour_logic="Four Roses Single Barrel's rose petal and fruit character finds "
                  "complementarity in the natural corn sweetness of cornbread with honey butter — "
                  "a quintessentially American grain pairing.",
    product_id=FOUR_ROSES_SB,
    food_flavour_profile="sweet, corny, buttery, honey",
    beverage_category="spirits_whiskey")

PAIR(cur3,
    food_description="Aged Cheddar with hot sauce — cask strength bourbon cuts through fat and heat",
    food_category="dairy_cheese", meal_context="cheese",
    confidence="established", pairing_type="cleanse",
    flavour_logic="Wild Turkey Rare Breed's cask strength (56%+) and deep char cut through "
                  "the fat of aged cheddar — the spice mirrors the hot sauce, and the bourbon "
                  "structure provides a counterpoint to both fat and heat.",
    product_id=RARE_BREED,
    food_flavour_profile="sharp, fatty, spicy, crystalline",
    beverage_category="spirits_whiskey")

# Tequila pairings
PAIR(cur3,
    food_description="Duck carnitas tacos with pickled red onion — añejo richness and confit richness",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="established", pairing_type="complement",
    flavour_logic="Don Julio 1942's vanilla, caramel, and aged agave character complements "
                  "the rich, slow-rendered duck fat of carnitas — the pickled onion bridges "
                  "acidity that refreshes between sips.",
    product_id=DON_JULIO_1942,
    food_flavour_profile="rich, fatty, acidic, spiced",
    beverage_category="spirits_agave")

PAIR(cur3,
    food_description="Ceviche with fresh lime and jalapeño — fresh agave matches ocean and citrus",
    food_category="seafood_sashimi", meal_context="starter",
    confidence="classic", pairing_type="complement",
    flavour_logic="Clase Azul Reposado's fresh agave and gentle vanilla character complements "
                  "the citrus acid and oceanic freshness of ceviche — the mild wood aging "
                  "adds structure without overwhelming the delicate seafood.",
    product_id=CLASE_AZUL_REP,
    food_flavour_profile="acidic, fresh, spicy, oceanic",
    beverage_category="spirits_agave")

PAIR(cur3,
    food_description="Grilled poblano peppers with queso fresco — mezcal smoke and roasted pepper",
    food_category="produce_specialty", meal_context="starter",
    confidence="classic", pairing_type="complement",
    flavour_logic="El Silencio Espadin's earth-pit smoke directly mirrors the roasted char "
                  "of grilled poblano peppers — the queso fresco provides a dairy bridge "
                  "that softens both.",
    product_id=EL_SILENCIO,
    food_flavour_profile="smoky, roasted, mild heat, creamy",
    beverage_category="spirits_agave")

conn3.commit()
cur3.close()
conn3.close()
print("\n✅ T8 Batch 1 — All complete.")
