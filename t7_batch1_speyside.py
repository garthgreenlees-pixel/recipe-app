#!/usr/bin/env python3
"""Terminal 7 — Batch 1: Speyside Scotch Depth — Producers + Products"""
import psycopg2, psycopg2.extras, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Existing Speyside region ID — look it up
cur.execute("SELECT id FROM beverage_regions WHERE name = 'Speyside' AND country = 'Scotland'")
row = cur.fetchone()
SPEYSIDE = row['id']
print(f"Speyside region ID: {SPEYSIDE}")

def P(name, producer_type, region_id, country="Scotland",
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
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
    row = cur.fetchone()
    print(f"  ✓ {name} (id={row['id']})")
    return row['id']

def PROD(name, category, producer_id, region_id, origin_country="Scotland",
         subcategory=None, description=None,
         quality_hierarchy=None, deductive_profile=None, service_specs=None,
         flavour_markers=None, flavour_weight=None, flavour_profile_type=None,
         price_tier=None, price_range_cad=None, technical_specs=None):
    cur.execute("SELECT id FROM beverage_products WHERE name = %s AND producer_id = %s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    cur.execute("""
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
    row = cur.fetchone()
    print(f"  ✓ {name} (id={row['id']})")
    return row['id']

# ─── SPEYSIDE PRODUCERS ────────────────────────────────────────────────────────
print("=== SPEYSIDE PRODUCERS ===")

glenfiddich = P("Glenfiddich Distillery", "distillery", SPEYSIDE,
    production_philosophy="World's most awarded single malt: approachable innovation at scale.",
    philosophy_description=(
        "Glenfiddich, founded 1887 by William Grant with his own hands and seven children, "
        "is the world's most awarded single malt whisky and the expression that introduced "
        "single malt to the global market (the first distillery to seriously promote "
        "single malt in the 1960s, when blended Scotch dominated globally). "
        "The Robbie Dhu springs provide soft, pure water; stainless steel washbacks and "
        "relatively small pot stills produce a light, fruity spirit that responds well to "
        "wood management. The experimental Solera vat system for the 15 Year Old is unique in Scotch."
    ),
    key_personnel=[
        {"name": "Brian Kinsman", "role": "Malt Master"},
        {"name": "Kelsey McKechnie", "role": "Brand Ambassador"}
    ],
    production_details={
        "founded": 1887,
        "stills": "28 small pot stills — one of the largest still populations in Speyside",
        "water": "Robbie Dhu springs",
        "fermentation": "Stainless steel washbacks, standard fermentation",
        "flagship": "Glenfiddich 12, 15 (Solera), 18, 21 Year Old; Gran Reserva 21 (rum cask)"
    },
    reputation_narrative=(
        "Glenfiddich is the world's best-selling single malt whisky — over 12 million bottles "
        "annually. Its influence in establishing the single malt category globally cannot be "
        "overstated: in the 1960s, it was one of the first distilleries to bottle and market "
        "single malt to an international audience. William Grant & Sons remains family-owned."
    ),
    price_positioning="premium",
    authority_tier=1)

balvenie = P("The Balvenie Distillery", "distillery", SPEYSIDE,
    production_philosophy="Five traditional skills: floor malting, coopering, coppersmiths, cooperage.",
    philosophy_description=(
        "The Balvenie, William Grant's second distillery (established 1892), is defined by its "
        "commitment to traditional craftsmanship: it is one of very few Scottish distilleries "
        "that still maintains all five traditional skills — growing its own barley, floor malting, "
        "coopering, coppersmiths (in-house still repair), and its own cooperage. "
        "The distillery's signature is the DoubleWood process: maturation in ex-bourbon American "
        "oak followed by finishing in ex-Oloroso sherry European oak — a process now widely copied."
    ),
    key_personnel=[
        {"name": "David Stewart MBE", "role": "Malt Master — longest-serving in the industry (since 1962)"}
    ],
    production_details={
        "malting": "Floor malting on-site — one of very few Scottish distilleries still doing this",
        "cooperage": "In-house cooperage — controls all cask quality",
        "stills": "5 wash stills, 6 spirit stills — slightly larger than Glenfiddich",
        "flagship": "DoubleWood 12, Caribbean Cask 14, Single Barrel 12 & 15, PortWood 21, 30 Year Old"
    },
    reputation_narrative=(
        "The Balvenie DoubleWood is one of the world's most recognisable Scotch expressions. "
        "The PortWood 21 Year Old and Thirty consistently achieve 95+ points. "
        "David Stewart MBE is the longest-serving malt master in Scotch whisky history."
    ),
    price_positioning="premium",
    authority_tier=1)

glenlivet = P("The Glenlivet Distillery", "distillery", SPEYSIDE,
    production_philosophy="The original: first licensed Scotch distillery, defining the lighter Speyside style.",
    philosophy_description=(
        "The Glenlivet, licensed in 1824 as the first legal Highland distillery under the Excise Act "
        "(which George Smith was instrumental in drafting), is the most historically significant "
        "Speyside distillery. The lighter, floral Speyside style that The Glenlivet pioneered "
        "became the template for what most of the world understands as 'Scotch whisky'. "
        "Owned by Pernod Ricard, it is the best-selling Scotch in the United States."
    ),
    key_personnel=[
        {"name": "Alan Winchester", "role": "Master Distiller"}
    ],
    production_details={
        "founded": 1824,
        "water": "Josie's Well spring on the estate",
        "stills": "14 pot stills across two still houses",
        "style": "Light, floral, fruity — the benchmark Speyside new make character",
        "flagship": "Glenlivet 12, 15 (French Oak Reserve), 18, 21 (Archive), 25 Year Old"
    },
    reputation_narrative=(
        "The Glenlivet 18 Year Old is one of the benchmark Speyside age statements globally. "
        "George Smith's 1824 legal licence was so coveted that 27 other distilleries "
        "temporarily added 'the Glenlivet' to their names — a legal battle that lasted until 1884."
    ),
    price_positioning="premium",
    authority_tier=1)

glenfarclas = P("Glenfarclas Distillery", "distillery", SPEYSIDE,
    production_philosophy="Family independence: the most sherried Speyside, direct-fired stills, no compromise.",
    philosophy_description=(
        "Glenfarclas (est. 1836) is one of the few remaining family-owned and family-managed "
        "Scottish distilleries — the Grant family (no relation to William Grant of Glenfiddich) "
        "has operated it since 1865. The philosophy is absolute independence: no corporate "
        "ownership, no compromise on production methods. Direct-fired stills (one of very few "
        "remaining in Scotland), 100% Oloroso sherry cask maturation policy, and aging "
        "in large 500-litre butts rather than small barrels — the result is the most richly "
        "sherried, full-bodied single malt in Speyside."
    ),
    key_personnel=[
        {"name": "John L.S. Grant", "role": "Chairman (6th generation family ownership)"},
        {"name": "George Grant", "role": "Sales Director and family sixth generation"}
    ],
    production_details={
        "founded": 1836,
        "ownership": "Grant family since 1865 — fully independent",
        "stills": "6 pot stills, direct-fired (gas flame) — very rare in Scotland",
        "casks": "100% ex-Oloroso sherry butts (500L)",
        "flagship": "Glenfarclas 10, 12, 15, 17, 21, 25, 30, 40, 50, 60 Year Old; 105 Cask Strength"
    },
    reputation_narrative=(
        "Glenfarclas 105 Cask Strength is one of Scotland's most celebrated value expressions — "
        "60% ABV, fully sherried, under $100 CAD. The 25 and 30 Year Old are among the most "
        "critically acclaimed Speyside expressions at any price point. "
        "Family independence and transparent production make Glenfarclas a connoisseur's choice."
    ),
    price_positioning="mid_range",
    authority_tier=1)

aberlour = P("Aberlour Distillery", "distillery", SPEYSIDE,
    production_philosophy="A'Bunadh: the original cask strength sherry bomb; Speyside's most intense.",
    philosophy_description=(
        "Aberlour (est. 1879) sits where the Lour Burn meets the Spey in the heart of Speyside. "
        "It is most celebrated for A'Bunadh — a cask strength, unfiltered, non-chill-filtered "
        "expression matured exclusively in ex-Oloroso sherry butts with no age statement. "
        "Released in batches, each A'Bunadh batch achieves a different character. "
        "Owned by Pernod Ricard but operated with autonomy."
    ),
    key_personnel=[
        {"name": "Sandy Hyslop", "role": "Master Distiller (Chivas Brothers)"}
    ],
    production_details={
        "founded": 1879,
        "water": "Ben Rinnes spring",
        "stills": "2 wash stills, 2 spirit stills",
        "casks": "A'Bunadh: 100% ex-Oloroso sherry; 12 Year Old: combination",
        "flagship": "Aberlour 12 Double Cask, 16 Double Cask, A'Bunadh (NAS cask strength)"
    },
    reputation_narrative=(
        "A'Bunadh ('origin' in Scottish Gaelic) is consistently rated 95-97 points globally — "
        "one of the best-value cask strength expressions in Scotch whisky. "
        "Each batch (150+ released) achieves a slightly different ABV and character, "
        "making it a collector's staple. The Batch 60+ releases are particularly sought."
    ),
    price_positioning="mid_range",
    authority_tier=1)

mortlach = P("Mortlach Distillery", "distillery", SPEYSIDE,
    production_philosophy="The 'Beast of Dufftown': heavy, meaty Speyside from unique 2.81x distillation.",
    philosophy_description=(
        "Mortlach (est. 1823, Dufftown's first legal distillery) produces the heaviest, most "
        "complex spirit in Speyside through its unique 2.81x distillation ratio — a combination "
        "of six stills operating in a non-standard configuration that creates an unusually "
        "heavy, meaty spirit character called 'the worm' by distillery workers. "
        "This spirit requires longer aging than conventional Speyside; aged expressions "
        "develop a savoury, beef-fat, truffle complexity unlike any other whisky. "
        "Owned by Diageo; historically used heavily in Johnnie Walker blends."
    ),
    key_personnel=[
        {"name": "Dr. Jim Beveridge", "role": "Master Blender (Diageo Scotch)"}
    ],
    production_details={
        "founded": 1823,
        "distillation": "2.81x distillation ratio — 3 small spirit stills and 3 wash stills in non-standard configuration",
        "character": "Heavy, meaty, waxy — nicknamed 'the Beast of Dufftown'",
        "flagship": "Mortlach 12 Year Old 'The Wee Witchie', Mortlach 16 Year Old 'The Distiller's Dram', Mortlach 20 Year Old"
    },
    reputation_narrative=(
        "Mortlach was largely unknown until Diageo launched a standalone range in 2014. "
        "The 16 Year Old in particular achieved 97-98 points from multiple critics — "
        "widely considered the finest Diageo single malt expression. "
        "The meaty, savoury character is polarising but deeply beloved by enthusiasts."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

# ─── SPEYSIDE PRODUCTS ─────────────────────────────────────────────────────────
print("\n=== SPEYSIDE PRODUCTS ===")

p1 = PROD("Glenfiddich 18 Year Old Single Malt", "spirits_whiskey", glenfiddich, SPEYSIDE,
    subcategory="Speyside Single Malt — Premium Age Statement",
    description=(
        "Glenfiddich 18 Year Old is the hinge expression of the range — where the distillery's "
        "characteristic fruity, approachable style gains genuine complexity from 18 years of "
        "maturation in American oak (ex-bourbon) and European oak (ex-sherry) casks. "
        "Unlike the lighter 12 Year Old, the 18 shows significant dried fruit from the sherry "
        "wood alongside the orchard fruit core. It is the expression most likely to convert "
        "a sceptic of Glenfiddich's lighter style. Won multiple gold medals at IWSC."
    ),
    flavour_markers=["dried apple", "pear", "dried apricot", "cinnamon", "vanilla", "light sherry", "oak spice"],
    flavour_weight="medium-full",
    flavour_profile_type="fruit_driven_speyside",
    deductive_profile={
        "colour": "Deep gold with amber tints",
        "nose": "Rich orchard fruit, dried apricot, vanilla, gentle sherry, cinnamon",
        "palate": "Rounded and complex — dried fruit, cinnamon, vanilla, mellow oak tannin",
        "finish": "Long, warm, spice and fruit fade"
    },
    service_specs={
        "serve_temp": "Neat or with a few drops of spring water",
        "glassware": "Glencairn",
        "notes": "Works very well with the addition of a splash of water — opens the dried fruit."
    },
    price_tier="premium",
    price_range_cad="$115-135",
    technical_specs={"abv": 40.0, "age": "18 years", "distillation": "Pot still", "maturation": "American oak + European oak (small sherry proportion)"})

p2 = PROD("The Balvenie DoubleWood 17 Year Old", "spirits_whiskey", balvenie, SPEYSIDE,
    subcategory="Speyside Single Malt — DoubleWood Maturation",
    description=(
        "The Balvenie DoubleWood 17 Year Old is the premium expression of the iconic DoubleWood "
        "process — matured first in ex-bourbon American oak for 15 years, then transferred to "
        "ex-Oloroso sherry European oak butts for a further 2 years of finishing. "
        "The result is the benchmark expression of Balvenie's house philosophy: the vanilla and "
        "fruit of bourbon oak layered with the dried fruit and spice of sherry. "
        "More complex than the 12 Year Old DoubleWood, with the sherry integration deeper "
        "and the oak structure more evident. Consistently achieves 94-96 points."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "DoubleWood 12 Year Old", "notes": "Entry to the DoubleWood style"},
        {"rank": 2, "expression": "DoubleWood 17 Year Old", "notes": "Premium — more complex, deeper sherry"},
        {"rank": 3, "expression": "PortWood 21 Year Old", "notes": "Port pipe finish; exceptional complexity"}
    ],
    flavour_markers=["dried fruit", "honey", "vanilla", "cinnamon", "sherry", "Christmas cake", "orange peel"],
    flavour_weight="medium-full",
    flavour_profile_type="doublewood_speyside",
    deductive_profile={
        "colour": "Deep amber-gold",
        "nose": "Warm and inviting — honey, dried fruit, vanilla, gentle sherry, cinnamon",
        "palate": "Smooth and rich — Christmas cake, orange peel, vanilla, spice, integrated tannin",
        "finish": "Long, warming, spice and dried fruit"
    },
    service_specs={
        "serve_temp": "Neat",
        "glassware": "Glencairn",
        "notes": "An ideal after-dinner whisky. Pairs extremely well with Christmas cake or dark chocolate."
    },
    price_tier="premium",
    price_range_cad="$160-195",
    technical_specs={"abv": 43.0, "age": "17 years (15 bourbon + 2 sherry)", "distillation": "Pot still", "maturation": "Ex-bourbon American oak then ex-Oloroso sherry European oak"})

p3 = PROD("The Glenlivet 18 Year Old Single Malt", "spirits_whiskey", glenlivet, SPEYSIDE,
    subcategory="Speyside Single Malt — Classic Age Statement",
    description=(
        "The Glenlivet 18 Year Old is the benchmark expression for what classical Speyside "
        "single malt whisky can achieve: the light, floral, fruit-forward style of the "
        "distillery gains depth, oak complexity, and a dried fruit richness from 18 years "
        "of maturation in a combination of American and European oak. "
        "It is one of the world's best-selling premium Scotch expressions, particularly "
        "dominant in the US market where it is the best-selling single malt. "
        "The 18 Year Old achieves the critical balance of accessibility and complexity "
        "that defines Glenlivet's commercial success."
    ),
    flavour_markers=["pineapple", "citrus", "honey", "vanilla", "dried fruit", "spice", "floral"],
    flavour_weight="medium",
    flavour_profile_type="light_floral_speyside",
    deductive_profile={
        "colour": "Rich gold",
        "nose": "Fruit-forward and floral — pineapple, citrus, honey, vanilla, light dried fruit",
        "palate": "Smooth and elegant — tropical fruit, honey, gentle spice, vanilla oak",
        "finish": "Medium-long, clean, fruity and sweet"
    },
    service_specs={
        "serve_temp": "Neat or on the rocks",
        "glassware": "Glencairn or tumbler",
        "notes": "One of the most versatile Scotch expressions — works equally well neat and mixed."
    },
    price_tier="premium",
    price_range_cad="$110-130",
    technical_specs={"abv": 43.0, "age": "18 years", "distillation": "Pot still", "maturation": "American oak + European oak"})

p4 = PROD("Glenfarclas 21 Year Old Single Malt", "spirits_whiskey", glenfarclas, SPEYSIDE,
    subcategory="Speyside Single Malt — Sherried, Family-Owned",
    description=(
        "Glenfarclas 21 Year Old is the pinnacle of everyday Glenfarclas — rich, sherried, and "
        "deeply complex at an age when most Speyside distilleries have lost family independence. "
        "Matured entirely in ex-Oloroso sherry butts in the family's direct-fired still tradition, "
        "it achieves a depth of dried fruit, Christmas cake, and spice complexity that benchmarks "
        "the sherried Speyside style. At under $200 CAD, it represents exceptional value compared "
        "to contemporaries from larger corporate-owned distilleries. "
        "Consistently 94-96 points from specialist critics."
    ),
    flavour_markers=["Christmas cake", "raisin", "dark fruit", "coffee", "dark chocolate", "cinnamon", "leather"],
    flavour_weight="full",
    flavour_profile_type="sherried_full_speyside",
    deductive_profile={
        "colour": "Deep mahogany-amber",
        "nose": "Rich and sherried — Christmas cake, dark fruit, coffee, cinnamon, light leather",
        "palate": "Full and complex — raisin, dark fruit, coffee, dark chocolate, warming spice",
        "finish": "Long, warming, sherried fruit and coffee fading to wood spice"
    },
    service_specs={
        "serve_temp": "Neat; allow 10 minutes to open",
        "glassware": "Glencairn",
        "notes": "One of Speyside's best pairings with dark chocolate and blue cheese."
    },
    price_tier="premium",
    price_range_cad="$155-195",
    technical_specs={"abv": 43.0, "age": "21 years", "distillation": "Pot still, direct-fired", "maturation": "100% ex-Oloroso sherry butts (500L)", "ownership": "Family-owned — Grant family"})

p5 = PROD("Aberlour A'Bunadh Batch Cask Strength", "spirits_whiskey", aberlour, SPEYSIDE,
    subcategory="Speyside Single Malt — NAS Cask Strength Sherried",
    description=(
        "A'Bunadh ('origin' in Scottish Gaelic) is Aberlour's cask strength, non-chill-filtered, "
        "uncoloured expression matured exclusively in ex-Oloroso sherry butts — released in "
        "numbered batches (150+ batches as of 2024). Each batch achieves a slightly different "
        "ABV (typically 59-61%) and a subtly different character depending on cask selection. "
        "At full strength, A'Bunadh is a sherry bomb: dark fruit, chocolate, Christmas cake, "
        "and warming alcohol — essentially liquid Christmas pudding at cask strength. "
        "The lack of chill-filtering preserves all natural fat and ester compounds. "
        "It is widely considered the best-value cask strength expression in Scotch whisky."
    ),
    flavour_markers=["Christmas pudding", "dark cherry", "dark chocolate", "coffee", "dried fruit", "cinnamon", "ginger"],
    flavour_weight="full",
    flavour_profile_type="cask_strength_sherried",
    deductive_profile={
        "colour": "Deep mahogany",
        "nose": "Intense and sherried — Christmas pudding, dark cherry, dark chocolate, dried fruit",
        "palate": "Full and warming at high strength — chocolate, coffee, Christmas cake, spice",
        "finish": "Very long, warming, dark fruit and spice, extraordinary persistence"
    },
    service_specs={
        "serve_temp": "Neat with water available; never ice",
        "glassware": "Glencairn",
        "notes": "Always add a small amount of water to open the dark fruit complexity. "
                 "At 60%, neat is very challenging — a few drops of water is not compromise, it's correct."
    },
    price_tier="mid_range",
    price_range_cad="$90-115",
    technical_specs={"abv": "59-61% batch-variable", "age": "NAS (approximately 10-14 years)", "distillation": "Pot still", "maturation": "100% ex-Oloroso sherry butts", "chill_filtered": False})

p6 = PROD("Mortlach 16 Year Old — The Distiller's Dram", "spirits_whiskey", mortlach, SPEYSIDE,
    subcategory="Speyside Single Malt — Heavy, Meaty, Unusual",
    description=(
        "Mortlach 16 Year Old 'The Distiller's Dram' is the expression that convinced the "
        "whisky world that Mortlach deserved its own spotlight. Released in 2014 as part of "
        "Diageo's Mortlach relaunch, it is the most complex and ambitious expression from "
        "the 'Beast of Dufftown' — the 2.81x distillation ratio creates an extraordinarily "
        "heavy, meaty spirit that gains wax, leather, truffle, and savouriness with 16 years "
        "of sherry cask maturation. It is completely unlike anything else in Speyside — "
        "the polar opposite of Glenlivet's fruity lightness. Consistently 96-98 points."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Mortlach 12 Year Old 'The Wee Witchie'", "notes": "Entry to the Mortlach character"},
        {"rank": 2, "expression": "Mortlach 16 Year Old 'The Distiller's Dram'", "notes": "Pinnacle of standard range"},
        {"rank": 3, "expression": "Mortlach 20 Year Old", "notes": "Most complex; extremely limited"}
    ],
    flavour_markers=["beef stock", "truffle", "dark fruit", "leather", "wax", "dried fig", "oak tannin"],
    flavour_weight="full",
    flavour_profile_type="heavy_meaty_speyside",
    deductive_profile={
        "colour": "Rich copper-mahogany",
        "nose": "Uniquely savoury and rich — beef stock, leather, truffle, dark fruit, wax",
        "palate": "Heavy and meaty — extraordinary texture, truffle, dried fig, dark fruit, big tannin",
        "finish": "Very long, savoury and drying, beef fat and leather persist"
    },
    service_specs={
        "serve_temp": "Neat; never diluted with more than 5ml water",
        "glassware": "Glencairn",
        "notes": "Pair with aged beef, truffle preparations, or dark chocolate. "
                 "Warn guests unfamiliar with the style — the savouriness is striking."
    },
    price_tier="ultra_premium",
    price_range_cad="$220-270",
    technical_specs={"abv": 43.4, "age": "16 years", "distillation": "2.81x ratio pot still distillation — unique system", "maturation": "Combination of Oloroso sherry and American oak"})

cur.close()
conn.close()
print("\n✅ T7 Batch 1 — Speyside complete.")
