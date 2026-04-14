#!/usr/bin/env python3
"""Terminal 6 — Batch 3: Irish Whiskey — Producers + Products"""
import psycopg2, psycopg2.extras, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

MIDLETON = 241
BUSHMILLS_REGION = 242
DUBLIN = 243

def P(name, producer_type, region_id, country="Ireland",
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

def PROD(name, category, producer_id, region_id, origin_country="Ireland",
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
print("=== IRISH WHISKEY PRODUCERS ===")

irish_distillers = P("Irish Distillers — Midleton", "distillery", MIDLETON,
    production_philosophy="Triple distillation, pot still mastery, vast cask library.",
    philosophy_description=(
        "Irish Distillers, owned by Pernod Ricard, operates the world's most productively diverse "
        "distillery: Midleton in County Cork. It produces grain, malt, and pure pot still spirits "
        "(triple-distilled) across dozens of different mash bills, still types, and cask regimes. "
        "Pure pot still — from a mash of malted and unmalted barley — is the Irish signature; "
        "its creamy, spicy, distinctly Irish character is what separates Midleton from Scotland."
    ),
    key_personnel=[
        {"name": "Billy Leighton", "role": "Master Blender (Redbreast, Midleton Very Rare)"},
        {"name": "Kevin O'Gorman", "role": "Master Distiller"}
    ],
    production_details={
        "styles": "Grain whiskey, malt whiskey, pure pot still whiskey",
        "distillation": "Triple distillation in copper pot stills",
        "maturation": "Ex-bourbon American oak, ex-sherry European oak, ex-port, Mizunara",
        "brands": "Jameson, Redbreast, Green Spot, Powers, Method & Madness, Midleton Very Rare"
    },
    reputation_narrative=(
        "Irish Distillers controls over 90% of Irish whiskey production. Jameson is the "
        "world's best-selling Irish whiskey and third-best-selling whiskey globally. "
        "Redbreast 15 and 21 Year Old are the pinnacle of pure pot still Irish whiskey — "
        "critically acclaimed and highly allocated globally."
    ),
    price_positioning="premium",
    authority_tier=1)

bushmills_prod = P("Old Bushmills Distillery", "distillery", BUSHMILLS_REGION,
    country="United Kingdom",
    production_philosophy="World's oldest licensed distillery; triple-distilled single malt tradition.",
    philosophy_description=(
        "Old Bushmills holds a licence dated 1608, making it the world's oldest licensed distillery. "
        "It produces Northern Ireland's only single malt Irish whiskey series — triple-distilled "
        "from 100% malted barley, then matured in ex-bourbon and ex-sherry casks. "
        "The Bushmills philosophy: lighter and more fragrant than pot still Irish, reflecting "
        "the single malt tradition shared with Scotland but executed with Irish triple distillation."
    ),
    key_personnel=[
        {"name": "Helen Mulholland", "role": "Master Blender (until 2020)"},
        {"name": "Colum Egan", "role": "Master Distiller"}
    ],
    production_details={
        "style": "Single malt Irish whiskey (100% malted barley)",
        "distillation": "Triple distillation in copper pot stills",
        "maturation": "Ex-bourbon American oak, ex-Oloroso sherry European oak",
        "brands": "Bushmills Original, Black Bush, Bushmills Malt 10, 16, 21 Year Old"
    },
    reputation_narrative=(
        "Bushmills is Northern Ireland's only major whiskey producer and the world's oldest "
        "continuously operating licensed distillery. Black Bush — 80% single malt, ex-Oloroso "
        "sherry maturation — is the outstanding value expression. Acquired by Jose Cuervo (2014)."
    ),
    price_positioning="mid_range",
    authority_tier=1)

teeling = P("Teeling Whiskey Company", "distillery", DUBLIN,
    production_philosophy="Dublin's whiskey renaissance: wine cask innovation and pot still revival.",
    philosophy_description=(
        "Teeling (founded 2012, distilling since 2015) was the first new Dublin distillery in 125 years. "
        "Jack and Stephen Teeling's philosophy: respect the Irish pot still tradition while "
        "embracing creative wine cask finishes, single grain innovation, and transparency about "
        "the whiskey's provenance. All spirit is produced on-site in the Liberties, Dublin."
    ),
    key_personnel=[
        {"name": "Jack Teeling", "role": "Founder and CEO"},
        {"name": "Stephen Teeling", "role": "Founder and COO"},
        {"name": "Alex Chasko", "role": "Head Distiller and Blender"}
    ],
    production_details={
        "style": "Single grain, single malt, single pot still",
        "distillation": "Double distillation (malt); pot still",
        "maturation": "Ex-bourbon, ex-Cabernet Sauvignon, ex-rum, ex-Cognac",
        "brands": "Teeling Small Batch, Teeling Single Grain, Teeling Single Malt, Brabazon"
    },
    reputation_narrative=(
        "Teeling has defined the new Dublin whiskey identity: international award-winner, "
        "export-focused, and innovative. Teeling Single Grain Cabernet Sauvignon Cask won "
        "World's Best Grain Whiskey (World Whisky Awards 2020). "
        "The distillery anchors Dublin's new whiskey tourism circuit."
    ),
    price_positioning="premium",
    authority_tier=1)

# ─── PRODUCTS ──────────────────────────────────────────────────────────────────
print("\n=== IRISH WHISKEY PRODUCTS ===")

p1 = PROD("Redbreast 12 Year Old Pure Pot Still", "spirits_whiskey", irish_distillers, MIDLETON,
    subcategory="Irish Pure Pot Still Whiskey",
    description=(
        "Redbreast 12 Year Old is the benchmark expression of pure Irish pot still whiskey — "
        "a style unique to Ireland, made from a mash of both malted and unmalted barley "
        "triple-distilled in copper pot stills. The unmalted barley gives Redbreast its "
        "defining character: a rich, spicy, oily texture quite unlike Scottish single malt. "
        "Matured in a combination of ex-bourbon American oak and ex-Oloroso sherry European oak, "
        "the 12 Year Old achieves a precise balance of fresh fruit (green apple, orchard), "
        "baking spice (cinnamon, nutmeg), and creamy pot still weight. "
        "It was voted the World's Best Pot Still Whiskey at the World Whisky Awards 2018 and "
        "consistently achieves 95+ points in major competitions."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Redbreast 12 Year Old", "notes": "Benchmark entry; most available"},
        {"rank": 2, "expression": "Redbreast 15 Year Old", "notes": "Greater sherry influence"},
        {"rank": 3, "expression": "Redbreast 21 Year Old", "notes": "Pinnacle; extremely limited"},
        {"rank": 4, "expression": "Redbreast Lustau Edition", "notes": "Lustau sherry cask finish"}
    ],
    flavour_markers=["green apple", "orchard fruit", "cinnamon", "nutmeg", "vanilla", "sherry", "pot still spice"],
    flavour_weight="full",
    flavour_profile_type="pot_still_spiced",
    deductive_profile={
        "colour": "Deep gold with amber tints",
        "nose": "Rich and complex — orchard fruit (green apple, pear), baking spice, vanilla, light sherry",
        "palate": "Creamy and full — pot still weight, cinnamon and nutmeg spice, dried fruit, vanilla",
        "finish": "Long and warming — spice, dried fruit, and a characteristic pot still dryness"
    },
    service_specs={
        "serve_temp": "Neat or with a small amount of spring water",
        "glassware": "Glencairn or whiskey tumbler",
        "notes": "A few drops of water open the spice and fruit beautifully."
    },
    price_tier="premium",
    price_range_cad="$85-100",
    technical_specs={"abv": 40.0, "age": "12 years", "distillation": "Triple distillation, pot still", "mash": "Malted + unmalted barley", "maturation": "Ex-bourbon + ex-Oloroso sherry"})

p2 = PROD("Jameson Irish Whiskey", "spirits_whiskey", irish_distillers, MIDLETON,
    subcategory="Irish Blended Whiskey",
    description=(
        "Jameson is the world's best-selling Irish whiskey and the drink most responsible for "
        "the global Irish whiskey renaissance. It is a blend of triple-distilled pot still "
        "whiskey (for spice and character) and grain whiskey (for lightness and approachability), "
        "matured in ex-bourbon and ex-sherry casks for a minimum of 4 years. "
        "The Jameson style is intentionally accessible: light, smooth, slightly sweet, "
        "with none of the edge or smoke of Scotch. It is designed for mixing — the world's "
        "most consumed Irish coffee ingredient and the standard for Irish whiskey cocktails. "
        "Despite its approachable profile, it is triple-distilled with legitimate craftsmanship."
    ),
    flavour_markers=["vanilla", "honey", "light toasted wood", "sweet barley", "mild spice", "citrus"],
    flavour_weight="light",
    flavour_profile_type="smooth_accessible",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Light and sweet — vanilla, honey, sweet barley, citrus",
        "palate": "Smooth and approachable — vanilla cream, sweet cereal, mild woody spice",
        "finish": "Short, clean, sweet fade"
    },
    service_specs={
        "serve_temp": "Neat, on the rocks, or mixed",
        "glassware": "Tumbler or highball for mixing",
        "notes": "The world standard for Irish coffee. Excellent in Whiskey Sour."
    },
    price_tier="mid_range",
    price_range_cad="$45-55",
    technical_specs={"abv": 40.0, "age": "Minimum 4 years", "distillation": "Triple distillation", "style": "Blended — pot still + grain", "maturation": "Ex-bourbon + ex-sherry"})

p3 = PROD("Bushmills Black Bush", "spirits_whiskey", bushmills_prod, BUSHMILLS_REGION,
    origin_country="United Kingdom",
    subcategory="Irish Blended Whiskey — Sherry Matured",
    description=(
        "Bushmills Black Bush is Northern Ireland's most celebrated blended whiskey — "
        "approximately 80% Bushmills single malt whiskey blended with 20% grain whiskey, "
        "with the malt component matured predominantly in Oloroso sherry casks. "
        "This sherry dominance gives Black Bush a richness and dark fruit character "
        "quite different from the standard Bushmills Original (ex-bourbon). "
        "It is the outstanding value expression from the world's oldest licensed distillery: "
        "smooth, approachable, and distinctly fruit-rich from the sherry influence. "
        "Triple-distilled for Irish smoothness, with a slightly higher malt-to-grain ratio "
        "than most blended expressions."
    ),
    flavour_markers=["dried fruit", "dark cherry", "honey", "vanilla", "light tannin", "sweet malt"],
    flavour_weight="medium",
    flavour_profile_type="sherried_smooth",
    deductive_profile={
        "colour": "Deep amber-gold",
        "nose": "Dried fruit, dark cherry, honey, vanilla — the sherry influence is immediately apparent",
        "palate": "Smooth and rich — dried fruit, sweet malt, light tannin from sherry oak",
        "finish": "Medium, warming, fruit and sweet malt fade"
    },
    service_specs={
        "serve_temp": "Neat or with one large ice cube",
        "glassware": "Tumbler",
        "notes": "An excellent whiskey for those transitioning from sherried Scotch to Irish."
    },
    price_tier="mid_range",
    price_range_cad="$48-58",
    technical_specs={"abv": 40.0, "age": "NAS (approximately 5-8 years)", "distillation": "Triple distillation", "composition": "~80% single malt, 20% grain", "maturation": "Predominantly ex-Oloroso sherry"})

p4 = PROD("Teeling Single Grain Irish Whiskey", "spirits_whiskey", teeling, DUBLIN,
    subcategory="Irish Single Grain Whiskey — Wine Cask Finish",
    description=(
        "Teeling Single Grain is the expression that established Teeling's international reputation "
        "and demonstrated that Irish single grain whiskey could be as complex and acclaimed as "
        "single malt. It is made from 95% corn (maize) distilled in a column still, "
        "then finished in ex-Cabernet Sauvignon wine casks — a creative departure from "
        "the standard Irish grain whiskey style. The wine cask finish imparts red berry fruit, "
        "purple grape character, and a distinctive vinous freshness. "
        "It won 'World's Best Grain Whiskey' at the World Whisky Awards (2020) and "
        "remains the benchmark for Irish grain whiskey innovation."
    ),
    flavour_markers=["red berry", "grape", "vanilla", "honey", "sweet corn", "light tannin", "fruit cake"],
    flavour_weight="medium-light",
    flavour_profile_type="wine_influenced_grain",
    deductive_profile={
        "colour": "Light amber with ruby tints from wine cask",
        "nose": "Unusual and intriguing — red berry, grape, vanilla, sweet corn",
        "palate": "Light to medium, soft — red fruit, vanilla, sweet cereal, wine tannin",
        "finish": "Medium, fruity, vinous fade with light spice"
    },
    service_specs={
        "serve_temp": "Neat or chilled neat",
        "glassware": "Glencairn or white wine glass",
        "notes": "Can be served chilled as an aperitif. Works well with dark chocolate pairing."
    },
    price_tier="premium",
    price_range_cad="$65-78",
    technical_specs={"abv": 46.0, "age": "NAS (approximately 15-17 years at bottling)", "distillation": "Column still", "mash": "95% corn, 5% malt", "maturation": "Ex-bourbon then ex-Cabernet Sauvignon wine cask finish"})

p5 = PROD("Redbreast 15 Year Old Pure Pot Still", "spirits_whiskey", irish_distillers, MIDLETON,
    subcategory="Irish Pure Pot Still Whiskey — Premium Age Statement",
    description=(
        "Redbreast 15 Year Old represents a significant step above the 12 Year Old: "
        "three additional years of maturation amplify the sherry oak influence, "
        "deepen the dried fruit character, and develop a complexity that approaches "
        "the finest Scottish single malts in layered depth. "
        "The pure pot still character is more pronounced — the unmalted barley spice "
        "integrates with the wood to create a textbook example of premium Irish whiskey. "
        "It is one of the most critically acclaimed Irish whiskies produced: consistently "
        "95-97 points across major competitions and limited in allocation globally."
    ),
    flavour_markers=["dried fig", "raisin", "cinnamon", "dark chocolate", "pot still spice", "orange peel", "sherry"],
    flavour_weight="full",
    flavour_profile_type="pot_still_complex",
    deductive_profile={
        "colour": "Deep mahogany-amber",
        "nose": "Rich and sherried — dried fig, raisin, Christmas spice, orange peel, dark chocolate",
        "palate": "Full and creamy — pot still weight, sherry fruit, cinnamon and nutmeg, dark chocolate mid-palate",
        "finish": "Very long, warming, spice and dried fruit with lingering pot still dryness"
    },
    service_specs={
        "serve_temp": "Neat; 15 minutes in the glass before nosing",
        "glassware": "Glencairn",
        "notes": "This whiskey rewards patience. A very small water addition (5ml) opens further complexity."
    },
    price_tier="premium",
    price_range_cad="$130-160",
    technical_specs={"abv": 46.0, "age": "15 years", "distillation": "Triple distillation, pot still", "mash": "Malted + unmalted barley", "maturation": "Ex-bourbon + ex-Oloroso sherry"})

p6 = PROD("Bushmills Malt 10 Year Old", "spirits_whiskey", bushmills_prod, BUSHMILLS_REGION,
    origin_country="United Kingdom",
    subcategory="Irish Single Malt Whiskey",
    description=(
        "Bushmills Malt 10 Year Old is the pure single malt expression from the world's oldest "
        "licensed distillery — 100% malted barley, triple-distilled in copper pot stills, "
        "and matured for 10 years in ex-bourbon American oak casks. "
        "It is the most Scotch-like of Irish whiskies in character: light-bodied, fragrant, "
        "fruity, with the smoothness added by triple distillation. "
        "Where Scottish single malts might have peat smoke or robust oak tannin, "
        "Bushmills 10 Year Old offers pure, clean malt with honey and orchard fruit — "
        "the ideal Irish single malt for Scotch drinkers exploring Irish whiskey."
    ),
    flavour_markers=["honey", "apple", "vanilla", "light toffee", "floral", "fresh malt"],
    flavour_weight="light",
    flavour_profile_type="light_floral_malt",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Delicate and fragrant — honey, apple, vanilla, light floral",
        "palate": "Light and smooth — honey, fresh malt, apple, gentle vanilla oak",
        "finish": "Short-medium, clean, honey and malt fade"
    },
    service_specs={
        "serve_temp": "Neat or with a splash of spring water",
        "glassware": "Glencairn or copita",
        "notes": "An excellent aperitif whiskey. Works beautifully in a Whiskey Smash cocktail."
    },
    price_tier="mid_range",
    price_range_cad="$60-72",
    technical_specs={"abv": 40.0, "age": "10 years", "distillation": "Triple distillation, pot still", "mash": "100% malted barley", "maturation": "Ex-bourbon American oak"})

cur.close()
conn.close()
print("\n✅ T6 Batch 3 — Irish Whiskey complete.")
