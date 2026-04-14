#!/usr/bin/env python3
"""Terminal 7 — Batch 2: Islay Scotch Depth — Producers + Products"""
import psycopg2, psycopg2.extras, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cur.execute("SELECT id FROM beverage_regions WHERE name = 'Islay' AND country = 'Scotland'")
row = cur.fetchone()
ISLAY = row['id']
print(f"Islay region ID: {ISLAY}")

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

# ─── ISLAY PRODUCERS ──────────────────────────────────────────────────────────
print("=== ISLAY PRODUCERS ===")

laphroaig = P("Laphroaig Distillery", "distillery", ISLAY,
    production_philosophy="The most richly flavoured of all Scotch whiskies: medicinal, iodine, peat smoke.",
    philosophy_description=(
        "Laphroaig (est. 1815) is Islay's most distinctive and provocative distillery — "
        "self-described on the label as 'the most richly flavoured of all Scotch whiskies'. "
        "Its phenol level (~45 ppm in malt) creates the characteristic medicinal, iodine, "
        "TCP antiseptic, seaweed, and smoky character that is Laphroaig's unmistakable signature. "
        "The distillery maintains its own floor malting (20% of production), worm tub condensers, "
        "and unusually small spirit stills — each preserves the heaviest possible spirit character. "
        "HRH Prince Charles (now King Charles III) is a Friend of Laphroaig — "
        "granting the distillery a Royal Warrant."
    ),
    key_personnel=[
        {"name": "Barry MacAffer", "role": "Distillery Manager"},
        {"name": "John Campbell", "role": "Former Distillery Manager (long tenure)"}
    ],
    production_details={
        "founded": 1815,
        "peat": "45-50 ppm phenol — among the highest on Islay",
        "malting": "Floor malting on-site (20% of production) — one of few remaining",
        "stills": "3 wash stills + 7 spirit stills (small, producing heavy spirit)",
        "flagship": "Laphroaig 10, Quarter Cask, Triple Wood, 18, 25, 30 Year Old; Cairdeas (annual)"
    },
    reputation_narrative=(
        "Laphroaig is the world's most polarising whisky — its medicinal, iodine character "
        "is loved or loathed, rarely tolerated. The 'Friends of Laphroaig' loyalty program "
        "(one of the world's first whisky loyalty programs) has over 740,000 members globally. "
        "HRH King Charles III holds a Friend of Laphroaig number."
    ),
    price_positioning="premium",
    authority_tier=1)

lagavulin = P("Lagavulin Distillery", "distillery", ISLAY,
    production_philosophy="The aristocrat of Islay: complex, refined peat smoke with elegance and depth.",
    philosophy_description=(
        "Lagavulin (est. 1816) is considered by many the world's finest peated Scotch whisky — "
        "combining Islay's characteristically intense peat smoke with an unusual refinement "
        "and complexity. The distillery's long fermentation (up to 60 hours) and slow, "
        "careful distillation in onion-shaped pot stills creates a heavier spirit that can "
        "absorb decades of wood aging without losing the peat character. "
        "The 16 Year Old is Islay's benchmark expression — Nick Offerman's association "
        "with the brand through Lagavulin's digital marketing has brought it mainstream recognition."
    ),
    key_personnel=[
        {"name": "Georgie Crawford", "role": "Distillery Manager"},
        {"name": "Nick Offerman", "role": "Brand ambassador (cultural)"}
    ],
    production_details={
        "founded": 1816,
        "peat": "35-40 ppm phenol",
        "fermentation": "Long fermentation (up to 60 hours) — unusual on Islay",
        "stills": "2 wash stills + 2 spirit stills — small batch, slow production",
        "flagship": "Lagavulin 16, 8, Distillers Edition (Pedro Ximénez), 12 Year Old Cask Strength"
    },
    reputation_narrative=(
        "Lagavulin 16 Year Old is the standard-bearer of Islay peated whisky — "
        "consistently 95-97 points globally and widely cited as one of the greatest "
        "whiskies produced. The Distillers Edition (Pedro Ximénez sherry cask finish) "
        "adds a layer of dark fruit sweetness that bridges Islay's savouriness."
    ),
    price_positioning="premium",
    authority_tier=1)

bruichladdich = P("Bruichladdich Distillery", "distillery", ISLAY,
    production_philosophy="Progressive Hebridean distillers: terroir-obsessed, experimental, independent.",
    philosophy_description=(
        "Bruichladdich (est. 1881, revived 2001) is Islay's most progressive and experimental "
        "distillery. Re-established as an independent by Mark Reynier and master distiller "
        "Jim McEwan, it pioneered the concept of whisky terroir: single farm barley, "
        "different Scottish regions, and even different Islay farms producing distinct expressions. "
        "Three distinct styles: Bruichladdich (unpeated), Port Charlotte (heavily peated, ~40 ppm), "
        "and Octomore (super-heavily peated, up to 309 ppm — the world's most peated whisky). "
        "Acquired by Rémy Cointreau in 2012 but maintains strong independent philosophy."
    ),
    key_personnel=[
        {"name": "Adam Hannett", "role": "Head Distiller"},
        {"name": "Jim McEwan", "role": "Master Distiller (2001-2015, now retired)"}
    ],
    production_details={
        "founded": 1881,
        "revived": 2001,
        "styles": "Bruichladdich (unpeated), Port Charlotte (heavily peated ~40 ppm), Octomore (super-peated ~200+ ppm)",
        "terroir": "Single farm Scottish barley, Islay barley, and own farm barley for provenance expressions",
        "flagship": "Classic Laddie, Port Charlotte 10, Octomore (annual), Islay Barley, Bere Barley"
    },
    reputation_narrative=(
        "Bruichladdich's Octomore series holds the record for the world's most heavily peated "
        "whisky (up to 309 ppm phenol). The Classic Laddie (unpeated) is among Islay's "
        "most approachable expressions. Bruichladdich's terroir philosophy has influenced "
        "craft whisky producers globally."
    ),
    price_positioning="premium",
    authority_tier=1)

bowmore = P("Bowmore Distillery", "distillery", ISLAY,
    production_philosophy="The heart of Islay: balanced peat smoke, sea-salt, and aged elegance.",
    philosophy_description=(
        "Bowmore (est. 1779) is Islay's oldest distillery and sits at the heart of the island "
        "— literally, in the middle of Bowmore village, on the shores of Loch Indaal. "
        "It balances Islay's characteristic peat smoke with greater elegance and refinement "
        "than Laphroaig or Lagavulin — the peat level (~25 ppm) creates smoke without "
        "medicinal extremes. The distillery's sea-level warehouses (No. 1 Vaults) allow "
        "salt air to permeate maturing casks, adding a maritime brine note unique to Bowmore."
    ),
    key_personnel=[
        {"name": "David Turner", "role": "Distillery Manager"}
    ],
    production_details={
        "founded": 1779,
        "peat": "25 ppm phenol — balanced Islay level",
        "warehouses": "No. 1 Vaults: sea-level warehouses allow maritime brine influence",
        "malting": "Floor malting on-site (40% of production)",
        "flagship": "Bowmore 12, 15, 18, 25 Year Old; No. 1 Vaults Edition (annual)"
    },
    reputation_narrative=(
        "Bowmore 18 Year Old is one of Islay's most sought aged expressions — "
        "balanced, complex, with the maritime brine and gentle peat smoke of the "
        "sea-level vault maturation. "
        "The No. 1 Vaults annual release achieves 95-97 points from specialist critics."
    ),
    price_positioning="premium",
    authority_tier=1)

caol_ila = P("Caol Ila Distillery", "distillery", ISLAY,
    production_philosophy="Islay's most productive distillery: lighter peat, transparency, value.",
    philosophy_description=(
        "Caol Ila (est. 1846, 'Sound of Islay') is the largest distillery on the island and "
        "historically the most important contributor to Johnnie Walker Black Label — "
        "80% of its production goes to Diageo's blending program. Its standalone single malt "
        "range was limited until the specialist bottling movement brought it into focus. "
        "The peat character (~35 ppm) is more maritime and smoke-focused than medicinal — "
        "the closest to a 'lighter peated Islay' style. Increasingly sought by specialists "
        "as an excellent-value alternative to Lagavulin."
    ),
    key_personnel=[
        {"name": "Billy Stitchell", "role": "Distillery Manager"}
    ],
    production_details={
        "founded": 1846,
        "peat": "35 ppm phenol — maritime smoke focus",
        "production": "Largest distillery on Islay; majority goes to Johnnie Walker blends",
        "stills": "3 wash stills + 3 spirit stills — highest capacity on Islay",
        "flagship": "Caol Ila 12 Year Old, Caol Ila Distillers Edition (Moscatel finish), Caol Ila Moch (NAS)"
    },
    reputation_narrative=(
        "Caol Ila 12 Year Old is considered among the best-value peated Scotch expressions: "
        "classic Islay smoke without the premium commanded by Lagavulin or Laphroaig. "
        "The independent bottling community has produced exceptional single cask expressions "
        "showing Caol Ila's hidden complexity."
    ),
    price_positioning="mid_range",
    authority_tier=1)

# ─── ISLAY PRODUCTS ────────────────────────────────────────────────────────────
print("\n=== ISLAY PRODUCTS ===")

p1 = PROD("Laphroaig 10 Year Old Single Malt", "spirits_whiskey", laphroaig, ISLAY,
    subcategory="Islay Single Malt — Medicinal Peated",
    description=(
        "Laphroaig 10 Year Old is the standard expression that defines the Laphroaig style "
        "and represents the most polarising whisky in Scotland's canon: intensely medicinal, "
        "iodine-rich, seaweed, antiseptic, and smoky — characteristics that its devoted following "
        "considers unparalleled and that newcomers may find challenging. "
        "At the 10-year mark, the spirit's raw power is still evident — wood softening "
        "is present but the phenolic character (45+ ppm) dominates. "
        "It is the essential reference for understanding peated Islay whisky at its most extreme. "
        "Royal Warrant holder — the label features the HRH mark."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Laphroaig 10 Year Old", "notes": "The entry reference; most available"},
        {"rank": 2, "expression": "Laphroaig Quarter Cask", "notes": "Smaller casks = faster maturation; sweeter"},
        {"rank": 3, "expression": "Laphroaig 18 Year Old", "notes": "More integrated; oak softens medicinal edge"},
        {"rank": 4, "expression": "Cairdeas Annual Release", "notes": "Cask strength; each batch different"}
    ],
    flavour_markers=["iodine", "TCP antiseptic", "seaweed", "peat smoke", "sea salt", "vanilla oak", "brine"],
    flavour_weight="full",
    flavour_profile_type="medicinal_peated_islay",
    deductive_profile={
        "colour": "Pale gold (no added caramel)",
        "nose": "Immediately striking — iodine, antiseptic, seaweed, damp peat, sea spray",
        "palate": "Smoky and medicinal — phenolic intensity, sea salt, peat, light vanilla from oak",
        "finish": "Very long, smoky, medicinal, sea salt — the most persistent finish in Scotch"
    },
    service_specs={
        "serve_temp": "Neat; water available separately",
        "glassware": "Glencairn",
        "notes": "Frame this for unfamiliar guests: 'This is the most challenging and most beloved Scotch. "
                 "Expect iodine and antiseptic — that is its character, not a flaw.'"
    },
    price_tier="mid_range",
    price_range_cad="$75-90",
    technical_specs={"abv": 43.0, "age": "10 years", "ppm": "45-50 phenol", "distillation": "Pot still, worm tub condensers", "maturation": "American white oak ex-bourbon"})

p2 = PROD("Lagavulin 16 Year Old Single Malt", "spirits_whiskey", lagavulin, ISLAY,
    subcategory="Islay Single Malt — Aristocrat of Peat",
    description=(
        "Lagavulin 16 Year Old is the benchmark peated Scotch whisky and arguably the finest "
        "standard-range expression produced in Scotland. It balances Islay's peat smoke "
        "with 16 years of exceptional cask development — the wood tames the raw phenolic edge "
        "and develops dried fruit, dark chocolate, and a rich oak sweetness that complements "
        "rather than competes with the smoke. The result is a whisky of extraordinary complexity "
        "and elegance: smoky but refined, powerful but balanced. "
        "Consistently 95-98 points globally; regularly named in 'Best Scotch Whisky' lists. "
        "Featured in the Diageo Special Releases as a 12 Year Old Cask Strength annually."
    ),
    quality_hierarchy=[
        {"rank": 1, "expression": "Lagavulin 8 Year Old", "notes": "Lighter, rawer; entry to Lagavulin style"},
        {"rank": 2, "expression": "Lagavulin 16 Year Old", "notes": "The benchmark; pinnacle of everyday range"},
        {"rank": 3, "expression": "Lagavulin Distillers Edition", "notes": "Pedro Ximénez finish; adds dark fruit sweetness"},
        {"rank": 4, "expression": "Lagavulin 12 Year Old Cask Strength", "notes": "Annual release; specialist collectors"}
    ],
    flavour_markers=["peat smoke", "dark dried fruit", "dark chocolate", "sea salt", "leather", "oak tannin", "iodine"],
    flavour_weight="full",
    flavour_profile_type="aristocratic_peated_islay",
    deductive_profile={
        "colour": "Deep amber-mahogany",
        "nose": "Complex and refined — peat smoke, dried fruit, dark chocolate, leather, sea salt",
        "palate": "Full and elegant — smoke, dark fruit, chocolate, sea salt, long and complex",
        "finish": "Extraordinary length — smoke, dried fruit, and leather persist for minutes"
    },
    service_specs={
        "serve_temp": "Neat",
        "glassware": "Glencairn",
        "notes": "The definitive after-dinner Islay whisky. Pairs exceptionally with smoked meat, "
                 "oysters, and dark chocolate. Allow 10+ minutes in the glass."
    },
    price_tier="premium",
    price_range_cad="$110-130",
    technical_specs={"abv": 43.0, "age": "16 years", "ppm": "35-40 phenol", "distillation": "Pot still", "maturation": "American oak ex-bourbon"})

p3 = PROD("Port Charlotte 10 Year Old Single Malt", "spirits_whiskey", bruichladdich, ISLAY,
    subcategory="Islay Single Malt — Heavily Peated, Progressive",
    description=(
        "Port Charlotte 10 Year Old is Bruichladdich's heavily peated expression — named for "
        "a village on the western shore of Islay. At ~40 ppm phenol, it sits between Lagavulin "
        "and Laphroaig in peat intensity but with Bruichladdich's characteristic fresh, "
        "clean spirit style underpinning the smoke. The 10 Year Old balances peat smoke, "
        "salt spray, and vanilla from American oak in a way that Bruichladdich describes as "
        "'complex peating' rather than phenolic dominance. It is consistently the best-value "
        "heavily peated Islay single malt and has achieved 95+ points from multiple critics. "
        "Non-chill-filtered and natural colour."
    ),
    flavour_markers=["peat smoke", "salt spray", "vanilla", "citrus", "barley", "charcoal", "dried herb"],
    flavour_weight="full",
    flavour_profile_type="clean_peated_islay",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Peat smoke up front, then citrus and vanilla, salt spray, clean barley",
        "palate": "Complex and fresh — smoke, vanilla, citrus zest, salt, clean spirit structure",
        "finish": "Long, smoky but clean, citrus and salt fade"
    },
    service_specs={
        "serve_temp": "Neat or with a few drops of water",
        "glassware": "Glencairn",
        "notes": "Water opens the citrus notes significantly — recommended for first-time tasting."
    },
    price_tier="premium",
    price_range_cad="$90-110",
    technical_specs={"abv": 50.0, "age": "10 years", "ppm": "40 phenol", "distillation": "Pot still", "maturation": "American oak ex-bourbon", "chill_filtered": False})

p4 = PROD("Bowmore 18 Year Old Single Malt", "spirits_whiskey", bowmore, ISLAY,
    subcategory="Islay Single Malt — Balanced, Maritime, Aged",
    description=(
        "Bowmore 18 Year Old is widely considered the most elegant and balanced Islay whisky "
        "at the 18-year age statement: the maritime brine from No. 1 Vaults' sea-level maturation, "
        "the gentle 25 ppm peat smoke, and 18 years of American and European oak development "
        "create a complexity that is refined rather than extreme. "
        "The salt air penetrating the old stone vaults is the defining influence: "
        "an iodine-and-brine note that is maritime rather than medicinal. "
        "Often recommended as the ideal entry to aged Islay whisky for those put off by "
        "Laphroaig's medicinal intensity."
    ),
    flavour_markers=["sea salt", "gentle peat", "dark fruit", "vanilla", "brine", "dark chocolate", "smoke"],
    flavour_weight="full",
    flavour_profile_type="maritime_balanced_islay",
    deductive_profile={
        "colour": "Deep amber",
        "nose": "Maritime and complex — sea salt, gentle peat smoke, dark fruit, vanilla, brine",
        "palate": "Balanced and elegant — salt, peat, dark fruit, chocolate, long complex finish",
        "finish": "Very long, maritime brine, smoke, and dried fruit — all integrated"
    },
    service_specs={
        "serve_temp": "Neat",
        "glassware": "Glencairn",
        "notes": "The ideal Islay whisky for guests who find Laphroaig or Lagavulin too extreme. "
                 "Frame as 'maritime elegance rather than medicinal intensity'."
    },
    price_tier="ultra_premium",
    price_range_cad="$200-240",
    technical_specs={"abv": 43.0, "age": "18 years", "ppm": "25 phenol", "maturation": "No. 1 Vaults sea-level warehouses, American + European oak"})

p5 = PROD("Caol Ila 12 Year Old Single Malt", "spirits_whiskey", caol_ila, ISLAY,
    subcategory="Islay Single Malt — Value Peated",
    description=(
        "Caol Ila 12 Year Old is Islay's best-kept secret and consistently rated among "
        "the world's best-value peated Scotch expressions. The distillery's maritime location "
        "overlooking the Sound of Islay (between Islay and Jura) creates a whisky that is "
        "smoke-forward but cleaner and more citrus-influenced than Laphroaig or Lagavulin. "
        "The 12 Year Old is the lightest and most approachable of Islay's heavily peated range — "
        "the ideal gateway to the style. At well under half the price of Lagavulin 16, "
        "it is the smart choice for cocktail programs and by-the-glass service."
    ),
    flavour_markers=["smoke", "citrus", "sea breeze", "light peat", "vanilla", "green apple", "brine"],
    flavour_weight="medium-full",
    flavour_profile_type="lighter_peated_islay",
    deductive_profile={
        "colour": "Pale gold",
        "nose": "Fresh and smoky — citrus, sea breeze, light peat, vanilla",
        "palate": "Medium-full, approachable — citrus, smoke, light brine, vanilla",
        "finish": "Medium-long, smoke and citrus fade cleanly"
    },
    service_specs={
        "serve_temp": "Neat, on the rocks, or in a Penicillin cocktail",
        "glassware": "Glencairn neat; Highball for cocktails",
        "notes": "Excellent in the Penicillin cocktail (Caol Ila, lemon, honey ginger syrup, Islay float). "
                 "Good for guests approaching peated whisky for the first time."
    },
    price_tier="mid_range",
    price_range_cad="$75-90",
    technical_specs={"abv": 43.0, "age": "12 years", "ppm": "35 phenol", "distillation": "Pot still", "maturation": "American oak ex-bourbon"})

cur.close()
conn.close()
print("\n✅ T7 Batch 2 — Islay complete.")
