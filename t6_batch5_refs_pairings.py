#!/usr/bin/env python3
"""Terminal 6 — Batch 5: Refs, Protocols, and Pairings"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, REF, PROTOCOL, PAIR

conn, cur = get_conn()

# Product IDs from T6 batches 2–4
YAMAZAKI_12 = 501
YAMAZAKI_18 = 502
NIKKA_FTB   = 503
YOICHI      = 504
ICHIRO      = 505
MIYAGIKYO   = 506

REDBREAST_12 = 507
JAMESON     = 508
BLACKBUSH   = 509
TEELING_GRAIN = 510
REDBREAST_15 = 511
BUSHMILLS_10 = 512

FOURSQUARE  = 513
MOUNTGAY_XO = 514
HAMPDEN     = 515
NEISSON     = 516
ELDORADO_15 = 517
APPLETON_12 = 518

# ─── REFERENCES ────────────────────────────────────────────────────────────────
print("=== BEVERAGE REFERENCES ===")

REF(cur,
    name="Japanese whisky: style overview and production philosophy",
    category="spirits_knowledge",
    description=(
        "Japanese whisky is the world's most celebrated and sought spirit category of the 21st century. "
        "It emerged from Masataka Taketsuru's training in Scotland (1918-1920) and Suntory's founding of "
        "Yamazaki Distillery in 1923. The Japanese style synthesises Scottish technique with Japanese "
        "precision aesthetics (monozukuri): multiple still shapes, fermentation vessel types, yeast "
        "strains, and cask types operated simultaneously create a vast blending inventory. "
        "The defining wood policy includes Mizunara Japanese oak — sandalwood and coconut aromatics "
        "requiring decades to develop — alongside ex-bourbon and ex-sherry casks. "
        "The Japanese Whisky crisis (2015-present): global demand triggered by Yamazaki Sherry Cask 2013 "
        "winning 'World's Best' caused severe stock shortages. Age statement expressions were discontinued "
        "at Yoichi, Miyagikyo, and Hakushu; NAS (No Age Statement) expressions replaced them. "
        "Secondary market premiums: Yoichi 10yo, Yamazaki 25yo, Hibiki 17yo achieve 5-20x retail."
    ),
    key_principles=(
        "Japanese whisky is NOT legally regulated like Scotch — until 2021 there were no minimum age "
        "or Japan-origin requirements. The Japanese Spirits & Liqueurs Makers Association (JSLMA) "
        "introduced voluntary standards in 2021: minimum 3 years, Japan-distilled, Japan-bottled. "
        "Verify any bottle claims against production date. "
        "The Mizunara signature — sandalwood, incense, coconut — is the most distinctively Japanese "
        "element; it only appears after many years of maturation. "
        "Japanese whisky is served as: Mizuwari (1:2.5 with chilled still water), Highball "
        "(1:3 with chilled sparkling water), or neat. All three are legitimate."
    ),
    common_mistakes=(
        "Assuming all 'Japanese' whisky is actually distilled in Japan — some brands blend "
        "imported Scottish or Canadian whisky and bottle in Japan. "
        "Over-chilling: serving Japanese whisky at temperatures below 15°C suppresses aromatics. "
        "Adding too much water to a NAS expression: concentration is already lower."
    ),
    pro_tips=(
        "The Highball is not a compromise — it is the traditional Japanese presentation. "
        "Prepare it correctly: 1 measure whisky, fill with very cold soda, stir once gently, "
        "garnish with lemon peel. The Yamazaki 12 Highball is one of the world's great food cocktails."
    ),
    skill_level="advanced",
    service_context="spirits bar, premium restaurant, whisky tasting",
    authority_tier=1)

REF(cur,
    name="Irish whiskey: production styles and Midleton mastery",
    category="spirits_knowledge",
    description=(
        "Irish whiskey is defined by three production styles: pure pot still (malted + unmalted barley, "
        "triple-distilled), single malt (malted barley only, triple-distilled), and grain (corn + malt, "
        "column still). Pure pot still is uniquely Irish — the unmalted barley creates a creamy, "
        "oily, spiced character unlike any other whisky style. "
        "Triple distillation is the Irish standard (vs. Scottish double distillation): "
        "produces a lighter, smoother spirit — more approachable but less complex at entry level. "
        "The Irish whiskey industry was devastated by Prohibition (loss of US market), Irish independence "
        "(loss of British Empire markets), and the rise of Scotch in the 1950s-60s. By the 1980s, "
        "only three distilleries remained. The renaissance: 40+ distilleries now operate, "
        "with world production expected to double by 2030."
    ),
    key_principles=(
        "Know the style distinction: pot still (spiced, oily, uniquely Irish), "
        "single malt (lighter than Scotch due to triple distillation), grain (for blending). "
        "Redbreast = pure pot still pinnacle. Bushmills = Northern Ireland single malt. "
        "Jameson = global blend, pot still + grain, triple-distilled. "
        "The unmalted barley percentage in pot still: Midleton pot still is approximately "
        "30% unmalted barley — this creates the 'green', spicy, almost oily character. "
        "Irish whiskey must: be triple pot-distilled or column-still distilled in Ireland, "
        "aged minimum 3 years in wood casks, bottled at minimum 40% ABV."
    ),
    common_mistakes=(
        "Treating all Irish whiskey as light and uninteresting — Redbreast 21 Year Old matches "
        "or exceeds Scottish single malts of equivalent age and price. "
        "Confusing Northern Ireland (Bushmills, UK) with Republic of Ireland (Midleton, Teeling) — "
        "both produce Irish whiskey under the same GI but from separate jurisdictions."
    ),
    pro_tips=(
        "Redbreast 12 Cask Strength is the most impressive value in Irish whiskey — at ~60% ABV "
        "it shows what pot still can achieve with full concentration. "
        "Irish coffee: Jameson, hot coffee, brown sugar, lightly whipped cream — the classic."
    ),
    skill_level="advanced",
    service_context="spirits bar, Irish pub, whiskey dinner",
    authority_tier=1)

REF(cur,
    name="Caribbean rum: styles, ester marks, and terroir",
    category="spirits_knowledge",
    description=(
        "Caribbean rum is the world's most stylistically diverse spirits category — "
        "the production geography (from Barbados to Martinique to Jamaica to Guyana) "
        "creates radically different spirit characters that outpace the regional diversity of Scotch. "
        "The key production variables: "
        "Fermentation: commercial yeast (lighter, shorter) vs. wild yeast / dunderhole pits (heavy, estery, funky). "
        "Distillation: pot still (heavy, rich, estery) vs. column still (light, clean). "
        "Base material: molasses (most rums, dark fruit/caramel) vs. fresh cane juice (agricole, grassy/fresh). "
        "Style geography: Barbados (medium, elegant), Jamaica (high ester, funky), "
        "Martinique (agricole, fresh vegetal), Guyana/Demerara (thick, dark, rich), "
        "Cuba (light, column still), Rhum Vieux Agricole (aged agricole, complex)."
    ),
    key_principles=(
        "Ester measurement (g/hLaa) is the key quality marker for Jamaican rum: "
        "Low ester <100; Medium 100-300; High 300-700; Very High 700-1600+. "
        "Foursquare's transparency standard: demand age statement, no added sugar declaration, "
        "no artificial colouring, still type disclosed. "
        "AOC Martinique is the only GI for rum worldwide — mandates fresh cane juice only. "
        "Demerara still marks: PM (Port Mourant wooden pot, c.1732), EHP (Enmore wooden Coffey), "
        "VSG (Versailles wooden pot) — each produces a different character."
    ),
    common_mistakes=(
        "Assuming all Caribbean rum is sweet: high-quality rums (Foursquare, Hampden, El Dorado 15) "
        "have no added sugar — the sweetness is natural from aging. "
        "Conflating agricole and traditional molasses rum — fundamentally different products."
    ),
    pro_tips=(
        "The Ti' Punch (Martinique): Neisson Blanc, fresh lime slice squeezed in, cane syrup. "
        "Simple, perfect, and the correct presentation for rhum agricole blanc. "
        "For food pairing: Demerara rum with dark chocolate is as successful as Port."
    ),
    skill_level="intermediate",
    service_context="spirits bar, rum tasting, cocktail program",
    authority_tier=1)

# ─── PROTOCOLS ─────────────────────────────────────────────────────────────────
print("\n=== SERVICE PROTOCOLS ===")

PROTOCOL(cur,
    name="Japanese Whisky Service — Neat, Mizuwari, and Highball Protocols",
    category="spirit_service",
    beverage_family="spirits",
    procedure=(
        "NEAT: Pour 30-45ml at room temperature into a clean Glencairn or wide-bowl nosing glass. "
        "Allow 5-10 minutes before serving to allow aromatics to open. "
        "Present the bottle to the guest, name the expression, note any Mizunara oak influence. "
        "Offer a small glass of still spring water on the side. "
        "\n\nMIZUWARI (traditional diluted): Chill a tall glass. Add 2-3 large ice cubes. "
        "Add 45ml whisky. Stir 13.5 times clockwise (Japanese precision standard). "
        "Slowly pour 120ml chilled still spring water. Stir 3.5 times. Do not garnish. "
        "\n\nHIGHBALL: Chill a tall glass to below 0°C. Add one very large ice block. "
        "Add 45ml whisky. Fill slowly with 135ml chilled carbonated water (ideally from soda gun). "
        "Stir once very gently (preserve carbonation). Garnish with a strip of yuzu or lemon peel."
    ),
    description="Three legitimate Japanese whisky service presentations — neat, Mizuwari, and Highball.",
    rationale=(
        "Japanese whisky culture treats all three presentations as legitimate and food-worthy. "
        "The Highball is not a 'lesser' presentation — the Japanese have elevated it to a culinary art. "
        "Mizuwari is the traditional tableside presentation at Japanese whisky bars. "
        "Neat service is for tasting and appreciation contexts."
    ),
    common_errors=[
        "Adding too much water to neat service — water is offered, not added by default",
        "Using tap water — Japanese spring water is the standard",
        "Not chilling the Highball glass adequately — temperature is critical to carbonation",
        "Stirring a Highball vigorously — kills carbonation"
    ],
    equipment_required=["Glencairn glasses", "tall Highball glasses", "large ice block", "still spring water", "carbonated water", "bar spoon", "yuzu or lemon peel"],
    guest_communication=(
        "For a guest unfamiliar with Japanese whisky: 'Would you like to try it neat first? "
        "I can also prepare it as a Highball — the traditional Japanese presentation with "
        "sparkling water, which is excellent with food.'"
    ),
    service_context="premium bar, Japanese restaurant, whisky tasting",
    skill_level="intermediate",
    authority_tier=1)

PROTOCOL(cur,
    name="Rum Tasting Service — Deductive Style Presentation",
    category="spirit_service",
    beverage_family="spirits",
    procedure=(
        "1. Present the bottle to the guest; name the distillery, country, and style (e.g., "
        "'This is Foursquare Exceptional Cask — a Barbados aged rum, pot and column blend, 14 years'). "
        "2. Pour 30ml into a Glencairn or copita nosing glass. "
        "3. Allow 3-5 minutes for aromatics to open (spirits evaporate faster than wine). "
        "4. Guide the guest through: colour → nose → palate → finish. "
        "5. Offer still spring water — demonstrate with a 5ml addition to a second glass. "
        "6. For Jamaican high-ester rum: warn the guest before nosing ('The nose is intense — "
        "please nose at 5cm distance first'). "
        "7. If offering a Ti' Punch for agricole: prepare tableside: "
        "squeeze a lime slice into a short glass, add 45ml blanc agricole, 1 tsp cane syrup."
    ),
    description="Structured rum tasting service with deductive approach and style-specific guidance.",
    rationale=(
        "Premium rum deserves the same structured service as fine whisky or Cognac. "
        "The diversity of rum styles (high-ester Jamaican, agricole, Demerara) requires "
        "guest orientation before tasting to avoid confusion or unpleasant first impressions."
    ),
    common_errors=[
        "Pouring over ice before the guest has nosed the rum neat",
        "Not warning guests about high-ester Jamaican rum intensity",
        "Serving agricole blanc without explanation — the vegetal nose surprises unprepared guests",
        "Using mugs or inappropriate glassware"
    ],
    equipment_required=["Glencairn or copita nosing glasses", "short glasses for Ti' Punch", "spring water", "bar spoon", "fresh lime", "cane syrup"],
    guest_communication=(
        "Frame rum diversity as a strength: 'The world of rum is as diverse as wine — "
        "Barbados is elegant like Burgundy, Jamaica is intense like Barolo, "
        "and Martinique agricole is fresh like Chablis.'"
    ),
    service_context="spirits bar, rum dinner, cocktail consultation",
    skill_level="advanced",
    authority_tier=1)

# ─── PAIRINGS ──────────────────────────────────────────────────────────────────
print("\n=== PAIRINGS ===")

# Japanese Whisky pairings
PAIR(cur,
    food_description="Aged Comté or Gruyère cheese — savoury umami complement to Yamazaki's sweet oak",
    food_category="dairy_cheese", meal_context="cheese",
    confidence="classic", pairing_type="complement",
    flavour_logic="The nutty, crystalline umami of aged hard cheese echoes the vanilla and caramel "
                  "oak notes of Yamazaki 12, while the milk fat coats the palate between sips.",
    product_id=YAMAZAKI_12,
    food_flavour_profile="savoury, nutty, umami, crystalline",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Dark chocolate 70%+ — dried fruit and spice complement to Yamazaki 18's sherry notes",
    food_category="chocolate_confection", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="The bitter cacao and dried fruit of 70% dark chocolate mirrors and amplifies "
                  "the dried fig, raisin, and dark chocolate notes of the sherried Yamazaki 18.",
    product_id=YAMAZAKI_18,
    food_flavour_profile="bitter, dark fruit, roasted cacao",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Smoked salmon blinis with crème fraîche — smoke and fat against Nikka From The Barrel",
    food_category="seafood_general", meal_context="amuse",
    confidence="established", pairing_type="bridge",
    flavour_logic="The smoke from cured salmon bridges to the subtle Yoichi peat note in Nikka FTB, "
                  "while the crème fraîche fat and acidity refreshes between sips.",
    product_id=NIKKA_FTB,
    food_flavour_profile="smoky, fatty, acidic, saline",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Grilled Hokkaido lamb chops with rosemary — maritime and herb complement to Yoichi",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="established", pairing_type="complement",
    flavour_logic="The maritime salinity and subtle peat of Yoichi NAS cuts through lamb fat, "
                  "while the rosemary echoes the dried herb and smoke in the whisky.",
    product_id=YOICHI,
    food_flavour_profile="rich, gamey, herbal, fatty",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Fresh fruit mochi — estery fruit echoes in Ichiro's Floor Malted",
    food_category="produce_specialty", meal_context="dessert",
    confidence="suggested", pairing_type="complement",
    flavour_logic="The clean ester and fresh fruit character of Ichiro's Floor Malted (green apple, "
                  "peach) finds complementary sweetness in fresh fruit mochi without overwhelming it.",
    product_id=ICHIRO,
    food_flavour_profile="sweet, fresh, mochi-textured",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Grilled Japanese chicken skewers (yakitori) — delicate protein matches Miyagikyo lightness",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="classic", pairing_type="complement",
    flavour_logic="Miyagikyo's light, floral, apple-blossom profile matches the clean grilled flavour "
                  "of yakitori without overwhelming the delicate poultry — a natural Japanese pairing.",
    product_id=MIYAGIKYO,
    food_flavour_profile="savoury, clean, lightly smoky, delicate",
    beverage_category="spirits_whiskey")

# Irish Whiskey pairings
PAIR(cur,
    food_description="Smoked duck breast with wild mushroom — pot still spice meets rich game",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="established", pairing_type="complement",
    flavour_logic="Redbreast 12's cinnamon and nutmeg pot still spice cuts through smoked duck fat, "
                  "while the orchard fruit notes lift the earthiness of wild mushroom.",
    product_id=REDBREAST_12,
    food_flavour_profile="smoky, rich, gamey, earthy",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Irish soda bread with Kerrygold butter — the classic Irish breakfast complement",
    food_category="flour_baking", meal_context="casual",
    confidence="classic", pairing_type="complement",
    flavour_logic="Jameson's light vanilla and sweet barley notes find complementary simplicity "
                  "in good soda bread and salted butter — a traditional Irish morning pairing.",
    product_id=JAMESON,
    food_flavour_profile="buttery, wheaten, slightly sour, comforting",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Sticky toffee pudding — sherry fruit of Black Bush mirrors caramelised sugar",
    food_category="produce_specialty", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="The dried fruit and Oloroso sherry influence of Bushmills Black Bush mirrors "
                  "the caramelised date and toffee of sticky toffee pudding — Ireland's best dessert pairing.",
    product_id=BLACKBUSH,
    food_flavour_profile="caramelised, sticky, dark fruit, butterscotch",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Roquefort with honeycomb — wine cask grain bridges blue cheese and sweet",
    food_category="dairy_cheese", meal_context="cheese",
    confidence="adventurous", pairing_type="bridge",
    flavour_logic="Teeling's Cabernet Sauvignon cask finish bridges the gap between the blue cheese's "
                  "funk and the honeycomb's sweetness — the wine cask note creates a wine-like context.",
    product_id=TEELING_GRAIN,
    food_flavour_profile="funky, salty, sweet, complex",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Chocolate fondant with orange — dark fruit and spice complexity of Redbreast 15",
    food_category="chocolate_confection", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Redbreast 15's dried fig, dark chocolate, and orange peel notes find direct "
                  "reflection in a chocolate fondant with orange — the whisky effectively functions "
                  "as a sauce note.",
    product_id=REDBREAST_15,
    food_flavour_profile="dark chocolate, citrus, warm, molten",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Oysters with lemon — clean single malt cuts through briny shellfish",
    food_category="seafood_sashimi", meal_context="amuse",
    confidence="established", pairing_type="cleanse",
    flavour_logic="Bushmills 10's clean, light honey and apple character refreshes between oysters "
                  "without competing — the triple distillation removes any harsh edge.",
    product_id=BUSHMILLS_10,
    food_flavour_profile="briny, oceanic, citrus, clean",
    beverage_category="spirits_whiskey")

# Caribbean Rum pairings
PAIR(cur,
    food_description="70% dark chocolate bonbons with dried tropical fruit — mirror Foursquare's profile",
    food_category="chocolate_confection", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Foursquare ECS's concentrated tropical fruit, caramel, and dark chocolate notes "
                  "find direct mirrors in dark chocolate bonbons — one of rum's greatest pairings.",
    product_id=FOURSQUARE,
    food_flavour_profile="dark, bitter, tropical, complex",
    beverage_category="spirits_rum")

PAIR(cur,
    food_description="Grilled pineapple with brown sugar — tropical sweetness complements Mount Gay XO",
    food_category="produce_specialty", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Mount Gay XO's tropical fruit and vanilla notes find natural complementarity "
                  "in caramelised grilled pineapple — the rum amplifies the tropical fruit register.",
    product_id=MOUNTGAY_XO,
    food_flavour_profile="tropical, caramelised, sweet, bright",
    beverage_category="spirits_rum")

PAIR(cur,
    food_description="Jerk-spiced pork belly — Jamaican ester funk and spice meets island flavours",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="classic", pairing_type="complement",
    flavour_logic="Hampden's high-ester tropical character and the pineapple/mango notes find "
                  "natural resonance with Jamaican jerk spice — this is the rum equivalent of "
                  "terroir pairing: same island, same spices.",
    product_id=HAMPDEN,
    food_flavour_profile="spicy, smoky, tropical, rich",
    beverage_category="spirits_rum")

PAIR(cur,
    food_description="Chilled ceviche with lime and plantain — agricole blanc as a Ti' Punch companion",
    food_category="seafood_sashimi", meal_context="starter",
    confidence="classic", pairing_type="complement",
    flavour_logic="Neisson Blanc 52.5° functions as the ideal Ti' Punch aperitif — the fresh cane "
                  "and citrus character of the rum mirrors the lime acid and ocean freshness of ceviche.",
    product_id=NEISSON,
    food_flavour_profile="acidic, fresh, tropical, citrus",
    beverage_category="spirits_rum")

PAIR(cur,
    food_description="Aged cheddar and Demerara dark fruitcake — rum Christmas pairing",
    food_category="dairy_cheese", meal_context="cheese",
    confidence="classic", pairing_type="complement",
    flavour_logic="El Dorado 15's dark molasses, dried fruit, and caramelised sugar character "
                  "mirrors the dense fruit and crystallised sugar of dark fruitcake — "
                  "and the aged cheddar sharpness provides contrast.",
    product_id=ELDORADO_15,
    food_flavour_profile="rich, fruity, crystallised, pungent cheese",
    beverage_category="spirits_rum")

PAIR(cur,
    food_description="Vanilla ice cream with rum-soaked raisins — tropical aging character amplified",
    food_category="produce_specialty", meal_context="dessert",
    confidence="established", pairing_type="complement",
    flavour_logic="Appleton 12's orange peel, vanilla, and tropical fruit notes elevate vanilla ice cream — "
                  "especially when the dessert includes rum-soaked raisins (a direct flavour echo).",
    product_id=APPLETON_12,
    food_flavour_profile="sweet, vanilla, cold, fruity",
    beverage_category="spirits_rum")

conn.commit()
cur.close()
conn.close()
print("\n✅ T6 Batch 5 — Refs, Protocols, Pairings complete.")
