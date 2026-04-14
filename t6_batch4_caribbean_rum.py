#!/usr/bin/env python3
"""Terminal 6 — Batch 4: Caribbean Rum — Producers + Products"""
import psycopg2, psycopg2.extras, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

BARBADOS = 244
JAMAICA  = 245
MARTINIQUE = 246
DEMERARA = 247

def P(name, producer_type, region_id, country,
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

def PROD(name, category, producer_id, region_id, origin_country,
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

# ─── PRODUCERS ─────────────────────────────────────────────────────────────────
print("=== CARIBBEAN RUM PRODUCERS ===")

foursquare = P("Foursquare Distillery", "distillery", BARBADOS, "Barbados",
    production_philosophy="Transparency, terroir, no added sugar: Barbados rum at its finest.",
    philosophy_description=(
        "Richard Seale's Foursquare is the world's most critically acclaimed rum distillery "
        "and the standard-bearer for rum authenticity. Seale pioneered the rum transparency "
        "movement — publishing detailed production information on every bottle — and is an "
        "outspoken opponent of added sugar, artificial colouring, and non-traditional additives. "
        "His Exceptional Cask Selection series are annual limited releases that redefine "
        "what Barbados rum can achieve in the glass."
    ),
    key_personnel=[
        {"name": "Richard Seale", "role": "Master Distiller and Owner"}
    ],
    production_details={
        "still_types": "Pot still and column still, producing different spirit characters blended post-maturation",
        "fermentation": "Moderately long, molasses-based",
        "maturation": "Ex-bourbon American oak; various finishes (Madeira, Port, sherry)",
        "philosophy": "No added sugar, no E150 caramel colouring, full transparency on production"
    },
    reputation_narrative=(
        "Foursquare is the world's most decorated rum distillery. The Exceptional Cask Selection "
        "releases (annual, limited) regularly achieve 97-99/100 across major spirits competitions. "
        "Seale's advocacy for rum transparency and GI protection for Barbadian rum has "
        "shaped the global premium rum conversation."
    ),
    price_positioning="premium",
    authority_tier=1)

mount_gay = P("Mount Gay Distilleries", "distillery", BARBADOS, "Barbados",
    production_philosophy="World's oldest rum brand: coral limestone water, coral terroir.",
    philosophy_description=(
        "Mount Gay Distilleries, established 1703, is the world's oldest continuously operating "
        "rum brand. Located in St. Lucy, Barbados, it draws water from coral limestone aquifers "
        "that impart a distinctive mineral quality to the spirit. The house style: medium-bodied, "
        "fruit-forward, vanilla-rich — the 'Barbados style' in its most accessible form."
    ),
    key_personnel=[
        {"name": "Allen Smith", "role": "Master Blender"}
    ],
    production_details={
        "still_types": "Double retort pot still and column still",
        "water": "Coral limestone aquifer",
        "maturation": "American white oak ex-bourbon barrels",
        "brands": "Eclipse, XO, Rum Bar, 1703 Master Select"
    },
    reputation_narrative=(
        "Mount Gay Eclipse is the world's best-selling Barbadian rum and the standard for "
        "the approachable Barbados style. Mount Gay XO and 1703 Master Select represent "
        "the premium tier. Mount Gay sponsors the Rolex Swan Cup — the world's largest sailing regatta."
    ),
    price_positioning="mid_range",
    authority_tier=1)

hampden = P("Hampden Estate", "distillery", JAMAICA, "Jamaica",
    production_philosophy="Pure Jamaican funk: traditional wild fermentation, highest ester production.",
    philosophy_description=(
        "Hampden Estate (established ~1750) produces the highest-ester pot still rum in the world. "
        "The traditional Jamaican production method — wild fermentation in open dunderhole pits "
        "using spent wash and cane vinegar — creates extreme bacterial activity producing "
        "hundreds of ester compounds at concentrations impossible to achieve with commercial yeast. "
        "The resulting spirit is simultaneously challenging and transcendent: overripe tropical fruit, "
        "nail polish, orange blossom, and pineapple — transformed by age into extraordinary complexity."
    ),
    key_personnel=[
        {"name": "Vivian Wisdom", "role": "Master Distiller"},
        {"name": "Luca Gargano", "role": "Global Ambassador (VELIER partnership)"}
    ],
    production_details={
        "fermentation": "Wild yeast, dunderhole pits, very long fermentation (10-14 days)",
        "still": "Pot stills only",
        "ester_marks": "HGML (>800 g/hLaa), LROK (>800), C<>H (>1600) — highest commercial ester marks",
        "maturation": "Tropical maturation at the estate; additional temperate maturation in Europe"
    },
    reputation_narrative=(
        "Hampden Estate is the most sought Jamaican rum producer globally. "
        "Its VELIER partnership releases (Great House, 60th Anniversary) are among the most "
        "celebrated rum bottlings ever made. The estate is now open for tourism and produces "
        "Rum Fire (white overproof), Rum Bar Gold, and Great House aged expressions."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

neisson = P("Neisson Distillery", "distillery", MARTINIQUE, "France",
    production_philosophy="AOC Rhum Agricole: terroir-driven cane juice distillation on Martinique.",
    philosophy_description=(
        "Neisson is Martinique's most terroir-focused rhum agricole producer — a family distillery "
        "producing rhum exclusively from fresh sugarcane juice grown on their own estate in "
        "Le Carbet. The AOC Martinique mandates the use of approved cane varieties, specific still "
        "types, and fresh-pressed juice only — Neisson takes this further by farming organically "
        "and bottling at higher strengths to preserve terroir expression."
    ),
    key_personnel=[
        {"name": "Grégoire Neisson", "role": "Director and Distiller"},
        {"name": "Virginie Neisson-Vernant", "role": "Director"}
    ],
    production_details={
        "style": "AOC Rhum Agricole (fresh cane juice only, no molasses)",
        "cane_variety": "Blue sugarcane (Canne Bleue) from own estate",
        "still": "Single creole column still per AOC specifications",
        "expressions": "Blanc 50° and 52.5°, Elevé sous Bois, Réserve Spéciale Aged, XO"
    },
    reputation_narrative=(
        "Neisson Blanc 52.5° is considered the benchmark expression of Martinique rhum agricole "
        "blanc — pure cane character, grassy and complex. The limited Parcellaire single-parcel "
        "releases command premium prices. Neisson has become the first choice for bartenders "
        "and collectors seeking authentic agricole character."
    ),
    price_positioning="premium",
    authority_tier=1)

el_dorado = P("Demerara Distillers — El Dorado", "distillery", DEMERARA, "Guyana",
    production_philosophy="Historic still marks, tropical maturation: the richest rums in the world.",
    philosophy_description=(
        "Demerara Distillers operates the Diamond Distillery complex on the Demerara coast — "
        "the world's most diverse collection of historic still types. The 'still marks' system "
        "identifies each expression by its still of origin: PM (Port Mourant wooden double retort), "
        "EHP (Enmore wooden Coffey), VSG (Versailles single wooden pot), and various others. "
        "El Dorado blends these different still characters into aged expressions of extraordinary complexity."
    ),
    key_personnel=[
        {"name": "Shaun Caleb", "role": "Master Blender"}
    ],
    production_details={
        "stills": "Port Mourant wooden double retort pot still (c.1732), Enmore wooden Coffey still, Versailles wooden pot still, and modern copper pot and column stills",
        "fermentation": "Molasses-based, variable length",
        "maturation": "Tropical maturation at the estate, American white oak",
        "brands": "El Dorado 3, 5, 8, 12, 15, 21, 25 Year Old; Single Still releases"
    },
    reputation_narrative=(
        "El Dorado 15 Year Old won 'Best Rum' at the IWSC 1992 — the first rum to win a major "
        "spirits competition. The 25 Year Old is among the most complex aged rums produced. "
        "The Single Still releases (PM, EHP, VSG) are among the most sought by collectors."
    ),
    price_positioning="premium",
    authority_tier=1)

# ─── PRODUCTS ──────────────────────────────────────────────────────────────────
print("\n=== CARIBBEAN RUM PRODUCTS ===")

p1 = PROD("Foursquare Rum Distillery — Exceptional Cask Selection Domaine de Courcelles XIV",
         "spirits_rum", foursquare, BARBADOS, "Barbados",
    subcategory="Barbados Rum — Exceptional Cask Selection",
    description=(
        "The Foursquare Exceptional Cask Selection (ECS) series is released annually by "
        "Richard Seale — each expression represents a specific cask regime aged on the island. "
        "The ECS series redefines what single blended rum can achieve: pot and column still "
        "spirit blended before maturation in ex-bourbon American oak, then finished in "
        "ex-wine or ex-sherry casks. The 14-year 2007 vintage Domaine de Courcelles finished "
        "in ex-French wine casks achieved 98/100 from critical consensus. "
        "The ECS series consistently achieves the highest scores in international rum competitions — "
        "more than any other distillery globally. No added sugar; full production transparency."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "ECS Annual Release", "notes": "New expression each year; each is its own benchmark"},
        {"rank": 2, "expression": "Foursquare 2005 Vintage", "notes": "13 years, considered a gold standard"},
        {"rank": 3, "expression": "Foursquare XO", "notes": "More widely available; excellent entry to ECS style"}
    ],
    flavour_markers=["dried tropical fruit", "vanilla", "caramel", "oak spice", "dark cherry", "cinnamon", "molasses"],
    flavour_weight="full",
    flavour_profile_type="rich_tropical_aged",
    deductive_profile={
        "colour": "Deep amber-mahogany",
        "nose": "Concentrated and layered — dried tropical fruit, vanilla, caramel, wine cask notes",
        "palate": "Full and complex — tropical fruit, dark cherry, caramel, oak spice, clean finish",
        "finish": "Very long, warming, tropical fruit and spice, no artificial sweetness"
    },
    service_specs={
        "serve_temp": "Neat at room temperature; no ice",
        "glassware": "Glencairn or copita nosing glass",
        "notes": "Treat like a fine Cognac or aged whisky. No mixer. No ice."
    },
    price_tier="ultra_premium",
    price_range_cad="$120-180",
    technical_specs={"abv": 56.0, "age": "14 years", "still_types": "Pot + column blend", "added_sugar": "None", "colouring": "None"})

p2 = PROD("Mount Gay XO", "spirits_rum", mount_gay, BARBADOS, "Barbados",
    subcategory="Barbados Aged Rum — Extra Old",
    description=(
        "Mount Gay XO is the premium aged expression from the world's oldest rum brand — "
        "a blend of pot still and column still rums aged between 8 and 15 years in "
        "American white oak ex-bourbon casks. It represents the Barbados style at its "
        "most refined: medium-bodied, fruity, and elegantly structured without the intensity "
        "of Foursquare's exceptional releases. The XO is widely distributed globally, "
        "making it the most accessible premium Barbadian rum for international markets. "
        "Won gold at the Rum & Cachaça Masters 2020."
    ),
    flavour_markers=["vanilla", "banana", "caramel", "dried fruit", "light spice", "toasted oak", "tropical fruit"],
    flavour_weight="medium",
    flavour_profile_type="smooth_tropical",
    deductive_profile={
        "colour": "Rich amber-gold",
        "nose": "Warm and inviting — vanilla, banana, caramel, light dried fruit",
        "palate": "Medium-bodied, smooth — tropical fruit, vanilla, light spice, toasted oak",
        "finish": "Medium, warming, clean tropical fruit fade"
    },
    service_specs={
        "serve_temp": "Neat or with one large ice cube",
        "glassware": "Rocks glass or Glencairn",
        "notes": "Excellent sipping rum and outstanding in an Old Fashioned."
    },
    price_tier="premium",
    price_range_cad="$80-95",
    technical_specs={"abv": 43.0, "age": "8-15 years", "still_types": "Pot + column blend", "maturation": "Ex-bourbon American oak"})

p3 = PROD("Hampden Estate Great House Distillery Edition",
         "spirits_rum", hampden, JAMAICA, "Jamaica",
    subcategory="Jamaican Rum — High Ester Pot Still",
    description=(
        "Hampden Great House is the estate's flagship aged expression — a blend of the "
        "highest ester marks (HGML and C<>H) pot-distilled at Hampden and aged for "
        "a minimum of 5 years in American white oak ex-bourbon barrels. "
        "It is the definitive expression of traditional Jamaican rum: overwhelming ester "
        "intensity on the nose (overripe banana, pineapple, mango, nail varnish), "
        "transforming in the glass to extraordinary tropical fruit complexity. "
        "At cask strength (~46%), the character is concentrated and challenging; "
        "a few drops of water make it both approachable and revelatory. "
        "No added sugar; no artificial colouring; full production transparency."
    ),
    flavour_markers=["overripe banana", "pineapple", "mango", "ester funk", "orange blossom", "vanilla", "wood spice"],
    flavour_weight="full",
    flavour_profile_type="high_ester_tropical",
    deductive_profile={
        "colour": "Golden amber",
        "nose": "Intense and complex — overripe tropical fruit, ester funk, orange blossom, banana",
        "palate": "Full and estery — pineapple, mango, vanilla, wood spice, extraordinary length",
        "finish": "Very long, tropical fruit and ester fade, clean and warming"
    },
    service_specs={
        "serve_temp": "Neat with a few drops of water, or Daiquiri",
        "glassware": "Glencairn or copita",
        "notes": "This rum polarises the uninitiated — the ester intensity requires explanation. Start with a small pour."
    },
    price_tier="ultra_premium",
    price_range_cad="$95-130",
    technical_specs={"abv": 46.0, "age": "Minimum 5 years", "still": "Pot still only", "ester_marks": "HGML + C<>H", "added_sugar": "None"})

p4 = PROD("Neisson Rhum Agricole Blanc 52.5°",
         "spirits_rum", neisson, MARTINIQUE, "France",
    subcategory="Martinique AOC Rhum Agricole Blanc",
    description=(
        "Neisson Blanc 52.5° is the benchmark unaged rhum agricole — the style that defines "
        "Martinique's AOC designation and demonstrates the terroir expression possible when "
        "rum is made from fresh sugarcane juice rather than molasses. "
        "The grassy, vegetal, almost savage freshness of unaged agricole is the defining "
        "character: green cane, fresh herbs, citrus zest, and a clean spirit structure "
        "that cannot be achieved with molasses. The 52.5% bottling strength preserves "
        "more aromatic intensity than the standard 50° version. "
        "The benchmark for rum agricole in cocktails — Daiquiri and Ti' Punch in particular."
    ),
    flavour_markers=["fresh sugarcane", "grass", "citrus zest", "fresh herbs", "tropical flowers", "light vegetal"],
    flavour_weight="medium-light",
    flavour_profile_type="fresh_agricole",
    deductive_profile={
        "colour": "Crystal clear",
        "nose": "Fresh and vegetal — green cane juice, grass, citrus zest, tropical flowers",
        "palate": "Clean and precise — fresh cane, green herb, light citrus, clean spirit heat",
        "finish": "Medium, fresh, clean sugarcane fade"
    },
    service_specs={
        "serve_temp": "Ti' Punch (neat with lime and cane syrup); Daiquiri",
        "glassware": "Short glass for Ti' Punch; coupe for Daiquiri",
        "notes": "The traditional Martinican Ti' Punch: 1.5 oz blanc, slice of lime squeezed and dropped, 0.5 tsp cane syrup."
    },
    price_tier="premium",
    price_range_cad="$72-85",
    technical_specs={"abv": 52.5, "age": "Unaged (Blanc)", "style": "AOC Rhum Agricole (fresh cane juice)", "cane": "Blue sugarcane, estate-grown"})

p5 = PROD("El Dorado 15 Year Old Special Reserve",
         "spirits_rum", el_dorado, DEMERARA, "Guyana",
    subcategory="Demerara Rum — Aged Special Reserve",
    description=(
        "El Dorado 15 Year Old is the rum that changed the world's perception of Guyanese rum "
        "and helped launch the premium rum category globally. It won 'Best Rum' at the IWSC 1992 — "
        "the first rum to win a major spirits competition. "
        "A blend of spirits from historic still marks including Port Mourant (wooden double retort pot), "
        "Enmore (wooden Coffey), and modern stills — all aged minimum 15 years in American white oak. "
        "The result is rum of extraordinary richness and complexity: dark molasses, dried tropical fruit, "
        "caramelised sugar, dark chocolate, and a thick, almost syrupy texture that no other "
        "producing country can replicate. The Demerara 'pot richness' is unmistakable."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "El Dorado 15 Year Old", "notes": "The benchmark; world-changing release"},
        {"rank": 2, "expression": "El Dorado 21 Year Old", "notes": "More wood complexity; slightly drier"},
        {"rank": 3, "expression": "El Dorado 25 Year Old", "notes": "Pinnacle; rare and allocated"}
    ],
    flavour_markers=["dark molasses", "dried tropical fruit", "caramelised sugar", "dark chocolate", "vanilla", "leather", "oak tannin"],
    flavour_weight="full",
    flavour_profile_type="rich_demerara",
    deductive_profile={
        "colour": "Deep mahogany with amber highlights",
        "nose": "Richly complex — dark molasses, dried tropical fruit, caramelised sugar, dark chocolate",
        "palate": "Thick and syrupy — molasses, caramelised fruit, dark chocolate, vanilla, wood tannin",
        "finish": "Very long, warming, dark fruit and chocolate, persistent richness"
    },
    service_specs={
        "serve_temp": "Neat; one large ice cube acceptable for long summer drinking",
        "glassware": "Rocks glass or Glencairn",
        "notes": "Excellent with chocolate desserts, cheese, and cigars. Sip slowly."
    },
    price_tier="premium",
    price_range_cad="$75-90",
    technical_specs={"abv": 43.0, "age": "15 years minimum", "still_marks": "PM, EHP, and modern stills blended", "maturation": "American white oak"})

p6 = PROD("Appleton Estate 12 Year Old Rare Casks",
         "spirits_rum", hampden, JAMAICA, "Jamaica",
    subcategory="Jamaican Rum — Aged Estate",
    description=(
        "Appleton Estate 12 Year Old Rare Casks is the medium-ester expression of Jamaican rum "
        "tradition — accessible, elegant, and far less challenging than Hampden's high-ester style. "
        "It is a blend of pot still and column still Jamaican rums aged minimum 12 years in "
        "American white oak ex-bourbon barrels at the estate in Nassau Valley. "
        "Master Blender Joy Spence is the first female master blender in the spirits industry. "
        "The Nassau Valley's combination of limestone, mineral-rich water, and tropical heat "
        "creates a 'tropical aging' environment where spirits mature 3-4x faster than in Scotland. "
        "The result: rich, fruity, and complex well beyond its 12-year age statement suggests."
    ),
    flavour_markers=["orange peel", "dried fruit", "vanilla", "molasses", "caramel", "light spice", "tropical fruit"],
    flavour_weight="medium-full",
    flavour_profile_type="tropical_aged_balanced",
    deductive_profile={
        "colour": "Rich amber",
        "nose": "Orange peel and dried tropical fruit, vanilla, light molasses, caramel",
        "palate": "Medium-full, smooth — tropical fruit, vanilla, light spice, caramel",
        "finish": "Medium-long, tropical fruit and spice"
    },
    service_specs={
        "serve_temp": "Neat, on the rocks, or in an Old Fashioned",
        "glassware": "Rocks glass or Glencairn",
        "notes": "Outstanding in a Rum Old Fashioned: 2oz rum, 0.25oz Demerara syrup, 2 dashes Angostura bitters."
    },
    price_tier="premium",
    price_range_cad="$75-85",
    technical_specs={"abv": 43.0, "age": "12 years", "still_types": "Pot + column blend", "maturation": "American white oak, Nassau Valley tropical aging"})

cur.close()
conn.close()
print("\n✅ T6 Batch 4 — Caribbean Rum complete.")
