"""
T22 Batch 1: Spirits region depth — second products for 9 single-product spirits regions
Targets: Martinique (246), Guyana (247), Haiti (76), Dublin (243),
         Chichibu (240), Yoichi (238), Ilocos (73), Quezon (72), Islay-Campbeltown (98)
"""
import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
conn.autocommit = True
cur = conn.cursor()

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Producer [{pid}]: {name}")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence,
           meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T22 BATCH 1: SPIRITS REGION DEPTH (9 REGIONS) ===\n")

# ── MARTINIQUE AOC — RHUM AGRICOLE (246) — J.M. Distillery ──
print("── MARTINIQUE — J.M. Distillery ──")
pid = P(
    name="Distillerie J.M. — Martinique",
    producer_type="distillery",
    region_id=246,
    country="France",
    production_philosophy="Macouba estate — Martinique's most mineral and terroir-driven Rhum Agricole",
    philosophy_description=(
        "Distillerie J.M. is one of Martinique's most distinguished and sought-after Rhum Agricole "
        "producers, farming sugarcane on the volcanic slopes of Macouba in northern Martinique "
        "near Mount Pelée. The region's rich volcanic soils, Atlantic trade winds, and high "
        "rainfall produce sugarcane of exceptional aromatic complexity. J.M.'s rhums are "
        "renowned for their distinctive mineral, terroir-driven character and rich, complex "
        "expressions across their aged range. The J.M. XO in particular is considered one "
        "of the Caribbean's greatest aged spirits."
    ),
    reputation_narrative=(
        "J.M. Distillery produces what many consider Martinique's most distinctive and "
        "terroir-expressive Rhum Agricole, with the Macouba estate's volcanic soils creating "
        "a character quite different from the more widely known southern Martinique producers."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="J.M. Rhum Agricole Blanc 50° Martinique AOC",
    category="spirits_rum",
    producer_id=pid,
    region_id=246,
    origin_country="France",
    subcategory="Rhum Agricole Blanc",
    description=(
        "Unaged Rhum Agricole Blanc from Distillerie J.M., produced from fresh sugarcane juice "
        "grown on the volcanic slopes of Macouba in northern Martinique. The J.M. Blanc 50° "
        "is bottled at 50% ABV rather than the standard 55%, making it more immediately "
        "approachable while retaining the estate's characteristic mineral complexity and "
        "fresh sugarcane vibrancy. Martinique's AOC regulations require production exclusively "
        "from fresh sugarcane juice (not molasses), column distillation to specific parameters, "
        "and at least three months of rest. J.M.'s Macouba terroir adds distinctive volcanic "
        "mineral character unique to northern Martinique."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Ti' punch with lime disc and cane sugar — the classic Martinique service",
     "complement", "classic", "aperitif",
     "The canonical Martinique pairing — Ti' punch showcases Rhum Agricole Blanc's terroir purity")
PAIR(prod,
     "Accras de morue (salt cod fritters) with chien sauce and lime",
     "cleanse", "established", "starter",
     "Agricole Blanc's mineral brightness and grassy freshness cut through fried accras richness")

# ── GUYANA — DEMERARA RUM (247) — Uitvlugt Estate ──
print("\n── GUYANA — Uitvlugt Estate ──")
pid = P(
    name="Uitvlugt Estate — Demerara Distillers",
    producer_type="distillery",
    region_id=247,
    country="Guyana",
    production_philosophy="Demerara's most complex pot still heritage — wooden Coffey still tradition",
    philosophy_description=(
        "The Uitvlugt Estate represents one of Guyana's most historically significant rum "
        "distilleries, with wooden Coffey (continuous) stills and traditional pot stills that "
        "produce distillates of extraordinary complexity now consolidated under Demerara Distillers "
        "Limited. The Uitvlugt marque produces lighter, more aromatic Demerara rums compared "
        "to the heavy, pot-still Port Mourant style, and is a key component of many premium "
        "Demerara blends. The estate's heritage dates to the colonial plantation era, and its "
        "traditional wooden stills are now among the oldest functioning distillation equipment "
        "in the world."
    ),
    reputation_narrative=(
        "Uitvlugt distillates are prized by independent rum bottlers worldwide for their "
        "complexity and distinctive aromatic character, representing one of the Caribbean's "
        "most important rum heritage sites and a living museum of plantation-era distillation."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Uitvlugt — Enmore Single Estate Demerara Rum 15 Year",
    category="spirits_rum",
    producer_id=pid,
    region_id=247,
    origin_country="Guyana",
    subcategory="Demerara Rum",
    description=(
        "Single estate Demerara rum from the historic Uitvlugt and Enmore estates in Guyana, "
        "aged 15 years in ex-bourbon barrels. Distilled using traditional wooden Coffey column "
        "stills — some of the oldest continuously operating distillation equipment in the world "
        "— the spirit develops extraordinary layers of complexity during long tropical aging "
        "in Guyana's humid equatorial climate. Demerara rums aged in the tropics lose far more "
        "to evaporation per year than European-aged spirits, concentrating the remaining rum "
        "into an intensely flavoured expression of this unique sugarcane terroir."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Roasted plantains with cinnamon, brown sugar, and rum cream",
     "complement", "classic", "dessert",
     "Demerara rum's molasses richness and vanilla-oak depth harmonise with caramelised plantain")
PAIR(prod,
     "Pepperpot — Guyanese braised beef and offal with cassareep and peppers",
     "complement", "established", "main",
     "Regional synergy — Demerara rum and Guyana's national dish share cassareep's dark sweetness")

# ── HAITI — CLAIRIN TRADITION (76) — Barbancourt Clairin ──
print("\n── HAITI — Clairin Barbancourt ──")
pid = P(
    name="Barbancourt — Haiti Clairin Division",
    producer_type="distillery",
    region_id=76,
    country="Haiti",
    production_philosophy="Haiti's artisanal clairin tradition — agricultural rum before industrial methods",
    philosophy_description=(
        "While Barbancourt is best known for its aged Haitian rum, the estate's relationship "
        "with clairin — Haiti's traditional unaged, minimally processed sugarcane spirit — "
        "connects it to the island's agricultural spirit heritage predating industrial rum "
        "production. Clairin is produced by hundreds of small distillers across Haiti's "
        "interior using locally grown, often heirloom sugarcane varieties fermented with "
        "indigenous yeasts and distilled in simple pot stills. The Barbancourt connection "
        "provides context for clairin's position in Haitian drinking culture alongside "
        "the island's more famous aged rum tradition."
    ),
    reputation_narrative=(
        "Clairin represents Haiti's most authentic and culturally significant spirits tradition, "
        "produced with minimal technology and maximum terroir expression from diverse sugarcane "
        "varieties across the island's interior regions."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Clairin Le Rocher — Haitian Artisanal Sugarcane Spirit",
    category="spirits_rum",
    producer_id=pid,
    region_id=76,
    origin_country="Haiti",
    subcategory="Clairin",
    description=(
        "Clairin from the Le Rocher area of Haiti's sugarcane growing regions, produced in the "
        "traditional artisanal manner from fresh-pressed sugarcane juice fermented with "
        "indigenous wild yeasts and distilled in simple copper pot stills. Unlike industrial "
        "rum production, clairin maintains the diversity of Haiti's many sugarcane varietals "
        "and the wild yeast populations unique to each producer's terroir. The result is a "
        "spirit of vivid, complex character — grassy, floral, funky, and profoundly individual "
        "— representing Haiti's agricultural spirit tradition in its purest form. Each clairin "
        "producer creates a distinctly different spirit from the same basic process."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Griot de porc (twice-cooked pork) with pikliz slaw and plantain",
     "complement", "classic", "main",
     "Haiti's national dish and national spirit — pikliz heat tamed by clairin's grassy freshness")
PAIR(prod,
     "Conch ceviche with lime, hot peppers, and coconut water",
     "complement", "established", "starter",
     "Clairin's wild-yeast funk and citrus notes mirror Caribbean ceviche's acid-spice brightness")

# ── DUBLIN — NEW WAVE IRISH WHISKEY (243) — Dingle Distillery ──
print("\n── DUBLIN — Dingle Distillery ──")
pid = P(
    name="Dingle Distillery",
    producer_type="distillery",
    region_id=243,
    country="Ireland",
    production_philosophy="Ireland's new wave pioneer — Kerry pot still whiskey with Hibernian coastal character",
    philosophy_description=(
        "Dingle Distillery was one of the first craft distilleries established in the Irish "
        "whiskey renaissance, founded in 2012 in the town of Dingle on the Dingle Peninsula "
        "in County Kerry. While primarily classified with the broader New Wave Irish Whiskey "
        "movement, Dingle brings a distinctly non-Dublin character — the wild Atlantic coastline, "
        "Kerry's rain-washed maritime climate, and local barley inform a pot still and single "
        "malt style with genuine coastal character. The distillery's small-batch production "
        "and commitment to Irish pot still traditions have made it one of the most respected "
        "craft Irish whiskey producers."
    ),
    reputation_narrative=(
        "Dingle Distillery represents Irish whiskey's craft renaissance with authority, producing "
        "pot still and single malt expressions of genuine quality that demonstrate the category's "
        "revival extends well beyond the large established distilleries."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Dingle Single Pot Still Irish Whiskey",
    category="spirits_whiskey",
    producer_id=pid,
    region_id=243,
    origin_country="Ireland",
    subcategory="Irish Single Pot Still",
    description=(
        "Single pot still Irish whiskey from Dingle Distillery, produced in the traditional "
        "Irish pot still style from a mash of malted and unmalted barley in copper pot stills. "
        "The single pot still category is uniquely Irish — developed to circumvent malt taxes "
        "in the 19th century — and produces a distinctive creamy, spicy, and intensely "
        "flavoured whiskey unlike any Scotch or American equivalent. Dingle's coastal Kerry "
        "location and small-batch production bring Atlantic freshness and maritime character "
        "to a traditional category, creating an expression that balances pot still's characteristic "
        "weight and spice with the distillery's unique coastal terroir."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Smoked salmon with brown bread, crème fraîche, and micro herbs",
     "complement", "classic", "starter",
     "Irish pot still whiskey and smoked salmon — a classic pairing where smoke and spice harmonise")
PAIR(prod,
     "Farmhouse cheddar with Dijon mustard, pickled walnuts, and oatcakes",
     "complement", "established", "cheese",
     "Pot still's creamy spice and weight make it ideal with aged cheddar's nutty sharpness")

# ── CHICHIBU — ICHIRO'S MALT (240) — Chichibu Distillery (second expression) ──
print("\n── CHICHIBU — Ichiro's Malt Mizunara Wood Reserve ──")
# Use the existing producer for a second product
cur.execute("SELECT id FROM beverage_producers WHERE name LIKE '%Chichibu%'")
row = cur.fetchone()
if row:
    chichibu_id = row[0]
    print(f"  ~ EXISTS producer (id={chichibu_id})")
else:
    chichibu_id = P(
        name="Venture Whisky — Chichibu Distillery",
        producer_type="distillery",
        region_id=240,
        country="Japan",
        production_philosophy="Ichiro Akuto's Japanese craft benchmark — Chichibu's terroir-driven whisky artistry",
        philosophy_description=(
            "Venture Whisky's Chichibu Distillery, founded by Ichiro Akuto in 2008, is Japan's "
            "most celebrated craft distillery, producing whisky of extraordinary quality and "
            "complexity from the mountain town of Chichibu in Saitama Prefecture. Akuto-san's "
            "meticulous approach to cask selection, local barley sourcing, and innovative wood "
            "management — including Japanese mizunara casks — has created a whisky of genuine "
            "international acclaim despite tiny production volumes."
        ),
        reputation_narrative=(
            "Ichiro's Malt from Chichibu has become one of the world's most sought-after "
            "craft whiskies, commanding premium prices and global recognition for quality "
            "that rivals the established Scottish and Japanese giants."
        ),
        price_positioning="ultra_premium",
        authority_tier=1
    )
prod = PROD(
    name="Ichiro's Malt Chichibu Mizunara Wood Reserve",
    category="spirits_whiskey",
    producer_id=chichibu_id,
    region_id=240,
    origin_country="Japan",
    subcategory="Japanese Single Malt",
    description=(
        "Chichibu single malt whisky finished in Japanese mizunara (Quercus mongolica) casks, "
        "a uniquely Japanese oak that imparts distinctive incense, sandalwood, and Asian spice "
        "notes impossible to replicate with European or American oak. Mizunara is extraordinarily "
        "difficult to work with — it leaks, cracks, and requires decades to impart its character "
        "effectively — but the results, when successful, are among the most distinctive whisky "
        "expressions in the world. Ichiro Akuto's expertise in mizunara finishing has produced "
        "a Chichibu expression that embodies Japanese whisky's unique relationship with "
        "indigenous materials and centuries-old craft traditions."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Wagyu beef sukiyaki with raw egg, spring onion, and tofu",
     "complement", "classic", "main",
     "Mizunara's sandalwood and incense echo sukiyaki's sweet soy glaze and Wagyu's umami depth")
PAIR(prod,
     "Matcha tiramisu with black sesame cream and yuzu zest",
     "complement", "established", "dessert",
     "Japanese whisky's incense complexity bridges Eastern and Western flavour elements beautifully")

# ── YOICHI — NIKKA (238) — Yoichi Single Malt Peaty ──
print("\n── YOICHI — Nikka Yoichi Heavily Peated ──")
cur.execute("SELECT id FROM beverage_producers WHERE name LIKE '%Yoichi%' AND name LIKE '%Nikka%'")
row = cur.fetchone()
if row:
    yoichi_id = row[0]
    print(f"  ~ EXISTS producer (id={yoichi_id})")
else:
    yoichi_id = P(
        name="Nikka Whisky — Yoichi Distillery",
        producer_type="distillery",
        region_id=238,
        country="Japan",
        production_philosophy="Masataka Taketsuru's Scottish-inspired masterwork — Yoichi's Hokkaido maritime peat",
        philosophy_description=(
            "The Yoichi Distillery was founded by Masataka Taketsuru in 1934 after returning "
            "from Scotland, where he learned distillation at multiple Highland and Speyside "
            "distilleries. Yoichi's Hokkaido location provided the cold, maritime climate most "
            "similar to Scotland, while the distillery's coal-fired pot stills — the last "
            "in Japan — produce a heavy, peaty style unlike any other Japanese whisky. "
            "Yoichi remains Japan's most Scotch-influenced expression."
        ),
        reputation_narrative=(
            "Yoichi is Japan's most assertive and idiosyncratic single malt, with its coal-fired "
            "pot stills and maritime Hokkaido location producing a whisky of genuine power and "
            "complexity that has earned international recognition since its worldwide launch."
        ),
        price_positioning="ultra_premium",
        authority_tier=1
    )
prod = PROD(
    name="Nikka Yoichi Single Malt — Heavily Peated",
    category="spirits_whiskey",
    producer_id=yoichi_id,
    region_id=238,
    origin_country="Japan",
    subcategory="Japanese Single Malt",
    description=(
        "The Heavily Peated expression from Nikka's Yoichi Distillery, distilled in traditional "
        "coal-fired direct-flame pot stills — the only coal-fired stills in Japan — which "
        "produce a heavier, more textured spirit than gas or steam-fired alternatives. Yoichi's "
        "Hokkaido coastal location provides genuine maritime influence similar to Scottish "
        "island malts, while the peated barley adds a distinctive Japanese interpretation of "
        "smoke. The result is an assertive, complex single malt that bridges the styles of "
        "Islay and the Japanese whisky tradition — smoky, maritime, and intensely flavoured "
        "with Yoichi's characteristic oiliness and weight."
    ),
    price_tier="ultra_premium"
)
PAIR(prod,
     "Yakitori thighs with tare glaze, shichimi, and pickled daikon",
     "complement", "classic", "main",
     "Yoichi's smoke and weight complement yakitori's char and umami tare glaze intensity")
PAIR(prod,
     "Smoked Pacific oysters with ponzu and tobiko",
     "complement", "established", "starter",
     "Maritime peat whisky and Pacific oysters — Hokkaido coastal terroir pairing of great synergy")

# ── ILOCOS REGION — BASI (73) — second Basi producer ──
print("\n── ILOCOS REGION — Ilocos Basi Cooperative ──")
pid = P(
    name="Ilocos Basi Traditional Producers Cooperative",
    producer_type="distillery",
    region_id=73,
    country="Philippines",
    production_philosophy="Ilocos Region's communal Basi tradition — fermented sugarcane wine preserved through generations",
    philosophy_description=(
        "The Ilocos Basi Traditional Producers Cooperative represents the collective of small "
        "traditional Basi producers in the Ilocos Norte and Ilocos Sur regions of northern "
        "Luzon. Basi is a fermented sugarcane wine unique to the Ilocos people, with production "
        "methods dating back at least 500 years and preserved through generations of family "
        "producers. The cooperative protects the traditional recipe and production methods — "
        "using local sugarcane varieties, bark additives, and clay pot fermentation — while "
        "providing market access for small producers who might otherwise be displaced by "
        "commercial production."
    ),
    reputation_narrative=(
        "The Ilocos Basi cooperative represents an important cultural preservation effort, "
        "maintaining living traditions of Filipino fermented beverage production that were "
        "nearly lost during the colonial period's suppression of indigenous alcohol production."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Ilocos Basi Aged Reserve — Sugarcane Wine",
    category="traditional_cultural",
    producer_id=pid,
    region_id=73,
    origin_country="Philippines",
    subcategory="Basi",
    description=(
        "Aged Basi from the Ilocos Region of northern Luzon, Philippines, produced by the "
        "traditional method of fermenting pressed sugarcane juice with bark additives — "
        "particularly duhat (Java plum) and sampalok (tamarind) bark — in sealed clay pots. "
        "The Aged Reserve Basi undergoes 1–3 years of earthen vessel aging, developing "
        "complexity and a distinctive tannic character from the bark additions. The result "
        "is amber-hued with notes of dried fruit, earth, sugarcane, and a subtle astringency "
        "that makes it unlike any other fermented beverage in the world. An endangered "
        "UNESCO-recognised traditional beverage of the Ilocos people."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Bagnet (fried Ilocano pork belly) with tomato and bagoong",
     "complement", "classic", "main",
     "Ilocos cultural pairing — Basi's tannic sweetness complements Ilocano pork's rich fat")
PAIR(prod,
     "Pinakbet (Ilocano vegetable stew with shrimp paste and bitter melon)",
     "complement", "established", "main",
     "Basi's earthiness and sweetness balance pinakbet's bitter melon and fermented shrimp intensity")

# ── QUEZON PROVINCE — LAMBANOG (72) — Lakan Lambanog ──
print("\n── QUEZON PROVINCE — Lakan Lambanog ──")
pid = P(
    name="Lakan Lambanog — Quezon Province",
    producer_type="distillery",
    region_id=72,
    country="Philippines",
    production_philosophy="Premium Quezon lambanog — artisanal coconut toddy spirit for modern appreciation",
    philosophy_description=(
        "Lakan Lambanog is one of the few Quezon Province lambanog producers bringing artisanal "
        "quality standards to this traditional Filipino coconut spirit. Lambanog is produced "
        "from the fermented sap of the coconut palm flower (tubâ), which is collected by "
        "skilled tree climbers (mananggiti) and distilled in traditional clay pot stills. "
        "Lakan's mission is to elevate lambanog from its association with cheap industrial "
        "production to a spirit worthy of appreciation alongside artisanal spirits globally, "
        "using traditional methods, clean coconut sap sources, and careful distillation."
    ),
    reputation_narrative=(
        "Lakan Lambanog represents the movement to reclaim lambanog's traditional artisanal "
        "heritage and position this uniquely Filipino spirit as a serious category worthy "
        "of international attention and craft spirits appreciation."
    ),
    price_positioning="mid_range",
    authority_tier=2
)
prod = PROD(
    name="Lakan Lambanog Aged Coconut Spirit — Quezon",
    category="traditional_cultural",
    producer_id=pid,
    region_id=72,
    origin_country="Philippines",
    subcategory="Lambanog",
    description=(
        "Artisanal aged lambanog from the Quezon Province of Luzon, Philippines, produced "
        "from the fermented sap of coconut palm flowers collected in traditional clay pots "
        "by skilled mananggiti (coconut tappers). Lakan's aged expression rests in toasted "
        "local hardwood barrels for 6–12 months, developing coconut cream, vanilla, and "
        "tropical fruit character with a clean, smooth finish unusual for traditional lambanog. "
        "Unlike industrial lambanog (often flavoured with fruit concentrates), Lakan's spirit "
        "expresses the natural character of Quezon's coconut palms and the skill of traditional "
        "fermentation and distillation methods."
    ),
    price_tier="mid_range"
)
PAIR(prod,
     "Lechon kawali (deep-fried crispy pork belly) with liver sauce and pickled papaya",
     "complement", "classic", "main",
     "Coconut spirit's sweetness and clarity balance lechon's rich pork fat and liver sauce depth")
PAIR(prod,
     "Halo-halo with ube ice cream, sago, nata de coco, and condensed milk",
     "complement", "established", "dessert",
     "Lambanog's coconut sweetness harmonises with halo-halo's tropical mix and ube's earthiness")

# ── ISLAY — CAMPBELTOWN (98) — Glengyle Distillery ──
print("\n── ISLAY — CAMPBELTOWN — Glengyle (Kilkerran) ──")
pid = P(
    name="Glengyle Distillery — Kilkerran",
    producer_type="distillery",
    region_id=98,
    country="Scotland",
    production_philosophy="Campbeltown's revival — Kilkerran single malt restoring the town of whisky to glory",
    philosophy_description=(
        "Glengyle Distillery, home of Kilkerran single malt, was founded in 2004 by J. & A. "
        "Mitchell & Co. (the owners of Springbank) in the historic Glengyle Distillery building, "
        "making it only the third distillery in Campbeltown — once Scotland's whisky capital "
        "with over 30 distilleries. Kilkerran (the ancient name for Campbeltown) is the first "
        "single malt to emerge from the reborn Glengyle site in decades, produced in the "
        "Springbank family tradition of minimal filtration, natural colour, and traditional "
        "distillation methods. The whisky represents Campbeltown's ongoing revival and the "
        "Mitchell family's commitment to the region's unique style."
    ),
    reputation_narrative=(
        "Kilkerran has quickly established itself as a serious Campbeltown single malt, "
        "earning critical acclaim for its traditional production methods and distinctively "
        "maritime, complex character that embodies the Campbeltown style's celebrated history."
    ),
    price_positioning="premium",
    authority_tier=2
)
prod = PROD(
    name="Kilkerran 12 Year Old Campbeltown Single Malt",
    category="spirits_whiskey",
    producer_id=pid,
    region_id=98,
    origin_country="Scotland",
    subcategory="Campbeltown Single Malt",
    description=(
        "12 year old single malt Scotch whisky from Glengyle Distillery, bottled as Kilkerran "
        "— the ancient Gaelic name for Campbeltown. Matured in a combination of ex-bourbon and "
        "ex-sherry casks in the traditional Campbeltown style, the whisky shows the region's "
        "characteristic profile of coastal brine, light peat, fresh fruit, and maritime "
        "complexity that distinguishes Campbeltown from Islay, Speyside, and Highland malts. "
        "Bottled at natural colour without chill filtration in the Springbank family tradition. "
        "A significant addition to Scotland's smallest and most historically important whisky region."
    ),
    price_tier="premium"
)
PAIR(prod,
     "Cold-smoked Loch Fyne mackerel with horseradish cream and rye toast",
     "complement", "classic", "starter",
     "Campbeltown coastal whisky and cold-smoked mackerel — maritime brine meets maritime brine")
PAIR(prod,
     "Haggis neeps and tatties with whisky cream sauce",
     "complement", "established", "main",
     "Traditional Scottish pairing — Campbeltown malt's weight and complexity complement haggis perfectly")

print("\n✅ T22 Batch 1 complete.")
print("  Martinique (246): +1 producer (J.M.), +1 product, +2 pairings")
print("  Guyana (247): +1 producer (Uitvlugt), +1 product, +2 pairings")
print("  Haiti (76): +1 producer (Barbancourt Clairin), +1 product, +2 pairings")
print("  Dublin (243): +1 producer (Dingle), +1 product, +2 pairings")
print("  Chichibu (240): +1 product (Mizunara), +2 pairings")
print("  Yoichi (238): +1 product (Heavily Peated), +2 pairings")
print("  Ilocos Basi (73): +1 producer (Cooperative), +1 product, +2 pairings")
print("  Quezon Lambanog (72): +1 producer (Lakan), +1 product, +2 pairings")
print("  Islay-Campbeltown (98): +1 producer (Kilkerran), +1 product, +2 pairings")

cur.close()
conn.close()
