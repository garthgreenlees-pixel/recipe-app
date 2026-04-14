#!/usr/bin/env python3
"""Terminal 6 — Batch 2: Japanese Whisky — Producers + Products"""
import psycopg2, psycopg2.extras, re, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Region IDs from T6 Batch 1
YAMAZAKI = 237
YOICHI   = 238
MIYAGIKYO = 239
CHICHIBU = 240

def P(name, producer_type, region_id, country="Japan",
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name = %s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    # Truncate production_philosophy to 100 chars if needed
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

def PROD(name, category, producer_id, region_id, origin_country="Japan",
         subcategory=None, description=None, quality_tier=None,
         quality_hierarchy=None, deductive_profile=None, service_specs=None,
         flavour_markers=None, flavour_weight=None, flavour_profile_type=None,
         price_tier=None, price_range_cad=None, technical_specs=None):
    cur.execute("SELECT id FROM beverage_products WHERE name = %s AND producer_id = %s",
                (name, producer_id))
    if cur.fetchone():
        cur.execute("SELECT id FROM beverage_products WHERE name = %s AND producer_id = %s",
                    (name, producer_id))
        row = cur.fetchone()
        print(f"  ~ EXISTS: {name} (id={row['id']})")
        return row['id']
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, producer_id, region_id, origin_country,
           subcategory, description, quality_tier, quality_hierarchy,
           deductive_profile, service_specs, flavour_markers,
           flavour_weight, flavour_profile_type,
           price_tier, price_range_cad, technical_specs, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE) RETURNING id
    """, (name, category, producer_id, region_id, origin_country,
          subcategory, description, quality_tier,
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
print("=== JAPANESE WHISKY PRODUCERS ===")

suntory = P("Suntory Spirits — Yamazaki Distillery", "distillery", YAMAZAKI,
    production_philosophy="Monozukuri: Japanese craftsmanship applied to whisky at every production step.",
    philosophy_description=(
        "Monozukuri — the Japanese art of craftsmanship applied to whisky: every detail of production "
        "is treated as an art form. Suntory operates multiple still shapes, fermentation vessels, "
        "yeast strains, and cask types simultaneously, creating a vast spirit library from which "
        "master blenders construct the house styles."
    ),
    key_personnel=[
        {"name": "Shinji Fukuyo", "role": "Chief Blender, Suntory"},
        {"name": "Shingo Torii", "role": "Founder (historical)"}
    ],
    production_details={
        "still_types": "Multiple pot still shapes (straight, bulge neck, lantern)",
        "fermenters": "Stainless steel and wooden (Douglas fir)",
        "maturation": "American white oak (ex-bourbon), European oak (ex-sherry), Mizunara",
        "flagship": "Yamazaki 12, 18, 25 Year Old; Hibiki 21 Year Old"
    },
    reputation_narrative=(
        "Yamazaki is Japan's most recognised whisky brand and among the top 5 most collectible "
        "whiskies in the world. The 2013 Sherry Cask bottling triggered a global Japanese whisky "
        "shortage that lasted a decade. Current allocations are controlled by lottery in Japan."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

nikka_yoichi = P("Nikka Whisky — Yoichi Distillery", "distillery", YOICHI,
    production_philosophy="Scottish methods in Hokkaido: coal-fired stills, worm tubs, maritime conditions.",
    philosophy_description=(
        "Masataka Taketsuru's founding philosophy: make whisky worthy of Scotland's best, using "
        "Scottish methods adapted to Hokkaido's conditions. Direct coal-fired stills are maintained "
        "as a deliberate choice — not tradition for its own sake but because the heat transfer "
        "creates the waxiness and weight that defines Yoichi's character."
    ),
    key_personnel=[
        {"name": "Masataka Taketsuru", "role": "Founder (1934-1979)"},
        {"name": "Nikka master blending team", "role": "Current production (Asahi Breweries)"}
    ],
    production_details={
        "stills": "Coal-fired direct-heated pot stills; worm tub condensers",
        "fermentation": "Long fermentation up to 7 days, house yeast",
        "maturation": "Ex-bourbon, ex-sherry, remade Japanese oak; damp Hokkaido warehouses",
        "flagship": "Yoichi Single Malt NAS; Yoichi 10/12/15/20 (discontinued)"
    },
    reputation_narrative=(
        "Yoichi Single Malt is Japan's most powerful and smoky whisky. Jim Murray awarded "
        "Yoichi 1987 the title 'World's Best Single Malt' (Whisky Bible 2008). "
        "The discontinued age statement range (10, 12, 15, 20 Year Old) is now "
        "among the most sought on secondary markets globally."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

nikka_miyagikyo = P("Nikka Whisky — Miyagikyo Distillery", "distillery", MIYAGIKYO,
    production_philosophy="Yoichi's complement: lighter, floral Coffey still spirit for versatile blending.",
    philosophy_description=(
        "Miyagikyo was designed as Yoichi's complement: lighter, more floral and fruity, "
        "for the blending versatility that creates Nikka's house styles. "
        "Coffey stills (continuous column) for grain and malt spirit at Miyagikyo are "
        "the soul of Nikka From The Barrel — Japan's most acclaimed blended whisky."
    ),
    key_personnel=[
        {"name": "Masataka Taketsuru", "role": "Founder (1969)"},
        {"name": "Nikka master blending team", "role": "Current production (Asahi Breweries)"}
    ],
    production_details={
        "stills": "Pot stills and Coffey stills (continuous column) at same site",
        "coffey_malt": "Malt wash through column stills — unique globally",
        "maturation": "Ex-bourbon and ex-sherry",
        "water": "Nikkagawa river, sourced on-site",
        "flagship": "Nikka From The Barrel, Miyagikyo Single Malt, Coffey Malt"
    },
    reputation_narrative=(
        "Nikka From The Barrel — a blend of Yoichi, Miyagikyo pot, and Miyagikyo Coffey "
        "spirits at 51.4% — is consistently rated the world's best value whisky per point. "
        "Miyagikyo 10 Year Old is the benchmark lighter Japanese single malt."
    ),
    price_positioning="premium",
    authority_tier=1)

venture = P("Venture Whisky — Chichibu Distillery", "distillery", CHICHIBU,
    production_philosophy="Artisanal, uncompromising: floor malting, 15+ cask types, hand-operated stills.",
    philosophy_description=(
        "Artisanal, uncompromising, obsessive: Ichiro Akuto's philosophy is that great whisky "
        "begins with the grain (floor-malted on-site), the fermentation (long, with house yeast), "
        "and the wood (more than 15 cask types including virgin Mizunara). "
        "Every step is done by hand by a small team. No blending in of neutral spirit. "
        "Every release is a limited edition; no permanent expressions exist."
    ),
    key_personnel=[
        {"name": "Ichiro Akuto", "role": "Founder and Master Distiller"}
    ],
    production_details={
        "malting": "Floor malting on-site — Japanese barley and small percentage peated",
        "fermenters": "Open-top wooden washbacks",
        "stills": "Direct-fired pot stills, small batch, hand-operated",
        "casks": "15+ types: virgin American oak, ex-bourbon, ex-sherry, ex-wine, Mizunara, Japanese cedar",
        "annual_production_litres": 100000
    },
    reputation_narrative=(
        "Chichibu is the world's most celebrated craft whisky distillery. "
        "Its limited releases (100-500 bottles per expression) sell out within minutes globally. "
        "The Hanyu Card Series (completed 2014) is among the most valuable whisky collections ever made. "
        "Ichiro's Malt Mizunara Wood Reserve, Double Distilleries, and The Floor Malted are "
        "among the most sought Japanese whiskies in secondary markets."
    ),
    price_positioning="ultra_premium",
    authority_tier=1)

# ─── PRODUCTS ──────────────────────────────────────────────────────────────────
print("\n=== JAPANESE WHISKY PRODUCTS ===")

p1 = PROD("The Yamazaki 12 Year Old Single Malt", "spirits_whiskey", suntory, YAMAZAKI,
    subcategory="Japanese Single Malt Whisky",
    description=(
        "The entry-level age statement expression of Suntory's Yamazaki Distillery — and the "
        "world's most recognised Japanese whisky outside Japan. Distilled from 100% malted barley "
        "and matured for a minimum of 12 years in a combination of American white oak (ex-bourbon), "
        "European oak (ex-sherry), and a small percentage of Mizunara Japanese oak. "
        "The resulting whisky is the textbook expression of the Japanese single malt style: "
        "silky texture, restrained sweetness, layered complexity, and exceptional integration. "
        "It represents the gateway expression to Japanese whisky appreciation for most international drinkers."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Yamazaki 12 Year Old", "notes": "Entry point to Japanese single malt"},
        {"rank": 2, "expression": "Yamazaki 18 Year Old", "notes": "Greater wood complexity"},
        {"rank": 3, "expression": "Yamazaki 25 Year Old", "notes": "Pinnacle; extremely limited"},
        {"rank": 4, "expression": "Yamazaki Limited Edition", "notes": "Annual release; lottery allocation"}
    ],
    flavour_markers=["peach", "pineapple", "coconut", "vanilla", "clove", "Japanese oak sandalwood", "honey"],
    flavour_weight="medium",
    flavour_profile_type="complex_layered",
    deductive_profile={
        "colour": "deep amber-gold",
        "nose": "Ripe peach and plum, honeyed sweetness, coconut and vanilla from American oak, subtle spice",
        "palate": "Silky entry, peach and apricot, vanilla cream, mild tannin from oak, clove and cinnamon finish",
        "finish": "Medium-long, sweet fruit and spice fade into sandalwood (Mizunara influence)"
    },
    service_specs={
        "serve_temp": "Neat at room temperature or with a single large ice ball",
        "glassware": "Glencairn or wide-bowl nosing glass",
        "notes": "A splash of spring water (not tap) opens the nose significantly. Japanese style: Mizuwari (1:2.5 whisky to chilled water) is traditional."
    },
    price_tier="ultra_premium",
    price_range_cad="$110-130",
    technical_specs={"abv": 43.0, "age": "12 years minimum", "distillation": "Pot still", "maturation": "American oak, European oak, Mizunara oak"})

p2 = PROD("The Yamazaki 18 Year Old Single Malt", "spirits_whiskey", suntory, YAMAZAKI,
    subcategory="Japanese Single Malt Whisky — Premium Age Statement",
    description=(
        "The 18 Year Old is Suntory's most commercially available premium expression and consistently "
        "appears on lists of the world's greatest whiskies. Six more years of maturation add significant "
        "sherry cask influence, Mizunara oak character (sandalwood, coconut), and a depth of dried fruit "
        "complexity that the 12 Year Old hints at but cannot fully achieve. "
        "It won 'Best Single Malt' at the San Francisco World Spirits Competition multiple times. "
        "The production quantity is severely limited — most bottles are allocated to Japan and "
        "select global markets through restricted distribution."
    ),
    flavour_markers=["dried fig", "raisin", "sandalwood", "dark chocolate", "orange peel", "cinnamon", "coconut cream"],
    flavour_weight="full",
    flavour_profile_type="sherried_complex",
    deductive_profile={
        "colour": "Deep mahogany with amber highlights",
        "nose": "Dried fruit (fig, raisin), dark chocolate, incense, sandalwood, dried orange peel",
        "palate": "Rich and structured — dark fruit, sherry tannin, baking spice, coconut and sandalwood from Mizunara",
        "finish": "Very long, warming, dried fruit and spice with a persistent sandalwood signature"
    },
    service_specs={
        "serve_temp": "Neat; never chilled",
        "glassware": "Glencairn or tulip",
        "notes": "This whisky benefits from 10-15 minutes in the glass before nosing. A few drops of water reveal further complexity."
    },
    price_tier="ultra_premium",
    price_range_cad="$280-350",
    technical_specs={"abv": 43.0, "age": "18 years minimum", "distillation": "Pot still", "maturation": "American oak, European oak (sherry), Mizunara"})

p3 = PROD("Nikka From The Barrel", "spirits_whiskey", nikka_miyagikyo, MIYAGIKYO,
    subcategory="Japanese Blended Whisky",
    description=(
        "Nikka From The Barrel is Japan's most critically acclaimed blended whisky and arguably "
        "the world's best value whisky per point of quality. It is a blend of Miyagikyo pot still malt, "
        "Miyagikyo Coffey malt, Miyagikyo Coffey grain, and Yoichi malt — re-blended and re-casked "
        "for a period ('marriage') before bottling at a cask-strength-adjacent 51.4% ABV. "
        "The high bottling strength is the key: it preserves aromatic intensity and a texture "
        "(mouth-coating, almost oily) that 40-43% whiskies cannot achieve. "
        "Rated 97/100 by Whisky Advocate and regularly appears on 'Best Whisky Under $70' lists globally."
    ),
    flavour_markers=["raisin", "honey", "dark toffee", "orange marmalade", "vanilla", "clove", "dried cherry"],
    flavour_weight="full",
    flavour_profile_type="rich_blended",
    deductive_profile={
        "colour": "Deep amber-mahogany",
        "nose": "Concentrated honey and toffee, orange marmalade, raisin, vanilla, subtle peat smoke from Yoichi component",
        "palate": "Huge and mouth-coating at 51.4% — toffee, dried fruit, clove, cinnamon, dark chocolate mid-palate",
        "finish": "Long, warming, drying spice fading to vanilla and dried fruit"
    },
    service_specs={
        "serve_temp": "Neat or with a very small amount of spring water",
        "glassware": "Glencairn",
        "notes": "Sip slowly. The 51.4% ABV requires water or patience to open. One small ice cube is acceptable."
    },
    price_tier="premium",
    price_range_cad="$65-80",
    technical_specs={"abv": 51.4, "age": "NAS (No Age Statement)", "distillation": "Pot still + Coffey still blend", "maturation": "Multiple cask types, re-casked marriage"})

p4 = PROD("Yoichi Single Malt — NAS", "spirits_whiskey", nikka_yoichi, YOICHI,
    subcategory="Japanese Single Malt Whisky — Peated",
    description=(
        "The current No Age Statement Yoichi expression replaced the celebrated age statement range "
        "(10, 12, 15, 20 Year Old) in 2015. It draws on the same coal-fired, worm tub-condensed spirit "
        "that made the original range famous: heavy, oily, maritime, and lightly peated — "
        "the most Scotch-like of Japanese single malts in structure but uniquely Japanese in execution. "
        "The NAS release blends different aged stocks to maintain house character. "
        "Critical consensus: comparable to the discontinued 12 Year Old in quality if "
        "slightly less complex. Secondary market for the discontinued 10 Year Old "
        "runs 3-5x original retail."
    ),
    flavour_markers=["sea salt", "peat smoke", "dried fruit", "malt", "wax", "leather", "dark toffee"],
    flavour_weight="full",
    flavour_profile_type="maritime_peated",
    deductive_profile={
        "colour": "Amber-gold",
        "nose": "Coastal and slightly peaty — sea salt, smoked malt, dried fruit, wax, leather",
        "palate": "Heavy and oily texture, peat smoke on mid-palate, dried fruit, dark toffee, maritime salinity",
        "finish": "Long, warming, maritime smoke persisting with dried fruit and wax"
    },
    service_specs={
        "serve_temp": "Neat or with a few drops of spring water",
        "glassware": "Glencairn",
        "notes": "The peated character responds well to a small amount of water — opens the fruit notes."
    },
    price_tier="ultra_premium",
    price_range_cad="$110-140",
    technical_specs={"abv": 45.0, "age": "NAS", "distillation": "Coal-fired pot still, worm tub condenser", "maturation": "Ex-bourbon and ex-sherry"})

p5 = PROD("Ichiro's Malt — The Floor Malted", "spirits_whiskey", venture, CHICHIBU,
    subcategory="Japanese Single Malt Whisky — Artisanal",
    description=(
        "The Floor Malted is Chichibu's statement of origin: a single malt made entirely from "
        "barley floor-malted on-site at Chichibu — one of only a handful of distilleries globally "
        "that still perform this labour-intensive traditional technique. "
        "Floor malting (spreading wet grain on warehouse floors, turning by hand every 8 hours for "
        "5-7 days) produces a malt with more complexity and site-specific character than industrial "
        "maltings. The barley is Japanese-grown, adding another layer of terroir. "
        "The resulting spirit is fruity, complex, and distinctively estery — a Japanese equivalent "
        "of Springbank's commitment to traditional methods. Limited to a few thousand bottles per year."
    ),
    flavour_markers=["green apple", "peach", "barley", "fresh bread", "vanilla", "light oak", "tropical fruit"],
    flavour_weight="medium",
    flavour_profile_type="fruity_artisanal",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Vibrant and fresh — green apple, peach, fresh bread, barley, light vanilla",
        "palate": "Fruity and estery — tropical fruit, green apple, developing sweetness, clean oak",
        "finish": "Medium-long, clean, fruity with lingering barley and sweet malt"
    },
    service_specs={
        "serve_temp": "Neat at room temperature",
        "glassware": "Glencairn or copita",
        "notes": "Serve without ice to appreciate the delicate ester profile."
    },
    price_tier="ultra_premium",
    price_range_cad="$180-250",
    technical_specs={"abv": 50.5, "age": "NAS (approximately 3-5 years)", "distillation": "Direct-fired pot still", "maturation": "Various cask types", "malt_source": "Japanese barley, floor-malted on-site"})

p6 = PROD("Miyagikyo Single Malt — NAS", "spirits_whiskey", nikka_miyagikyo, MIYAGIKYO,
    subcategory="Japanese Single Malt Whisky — Light and Floral",
    description=(
        "The Miyagikyo NAS expression represents the opposite end of Nikka's Japanese single malt "
        "spectrum from Yoichi: light, floral, fruity, and elegant rather than heavy and maritime. "
        "It is the ideal introductory Japanese single malt for drinkers accustomed to Lowland Scotch "
        "or Irish whiskey — approachable, perfumed, and versatile. "
        "Pot-distilled at Miyagikyo using the distillery's natural spring water, "
        "matured primarily in ex-bourbon American oak to emphasise fruit and vanilla. "
        "The NAS replaced the 10 Year Old expression in 2015; it is widely available and "
        "represents excellent value in the Japanese single malt category."
    ),
    flavour_markers=["apple blossom", "pear", "apricot", "vanilla", "honey", "light toffee", "fresh floral"],
    flavour_weight="light",
    flavour_profile_type="floral_delicate",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Floral and fruit-forward — apple blossom, pear, apricot, gentle honey",
        "palate": "Light and elegant — fresh fruit, vanilla, honey, subtle oak spice",
        "finish": "Short-medium, clean, fruit and vanilla fade gently"
    },
    service_specs={
        "serve_temp": "Neat or Highball (Japanese whisky soda)",
        "glassware": "Glencairn neat; tall glass for Highball",
        "notes": "Exceptional as a Highball: 1 part Miyagikyo to 3 parts chilled soda water, garnished with lemon peel."
    },
    price_tier="premium",
    price_range_cad="$85-100",
    technical_specs={"abv": 45.0, "age": "NAS", "distillation": "Pot still", "maturation": "Ex-bourbon American oak"})

cur.close()
conn.close()
print("\n✅ T6 Batch 2 — Japanese Whisky complete.")
