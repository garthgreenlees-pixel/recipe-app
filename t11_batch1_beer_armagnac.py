#!/usr/bin/env python3
"""Terminal 11 — Batch 1: Belgian Beer + German Beer + Armagnac Depth"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

BELGIUM  = 101
BAVARIA  = 102
ARMAGNAC = 157

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          reputation_narrative, price_positioning, authority_tier))
    row = cur.fetchone()
    print(f"  ✓ {name} (id={row[0]})")
    return row[0]

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, producer_id, region_id, origin_country,
           subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, producer_id, region_id, origin_country,
          subcategory, description, price_tier))
    row = cur.fetchone()
    print(f"    ✓ {name} (id={row[0]})")
    return row[0]

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

def get_product(name):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Product not found: {name}")

# ═══════════════════════════════════════════════════════════════════════════
# BELGIUM — TRAPPIST & LAMBIC DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("=== BELGIUM — TRAPPIST & LAMBIC ===")

westvleteren = P("Brouwerij der Trappisten van Westvleteren", "brewery", BELGIUM, "Belgium",
    production_philosophy="The rarest Trappist beer — brewed by monks for monks, not for commerce",
    philosophy_description="Sint-Sixtus Abbey in Westvleteren is the most restricted Trappist brewery in the world — beer is sold only by advance reservation from the abbey itself, with quantities strictly limited to prevent commercial exploitation. Westvleteren 12, consistently rated the world's greatest beer, is a quadrupel of extraordinary depth brewed by monks who maintain the Trappist principle: beer is a means of sustaining the monastic community, not a commercial enterprise.",
    key_personnel=[{"name": "Brother Prior", "role": "Abbey Administrator"}],
    production_details={"availability": "abbey only by phone reservation", "rule": "Trappist Authentic certified", "production": "minimal, strictly limited"},
    reputation_narrative="Westvleteren 12 has been rated the world's greatest beer by RateBeer.com every year since 2005. The extreme scarcity — purchasable only by phoning the abbey and visiting in person — creates a mystique that the beer fully delivers on. A once-in-a-career experience for sommeliers and beer enthusiasts.",
    price_positioning="ultra_premium")

PROD("Westvleteren XII (12)", "beer_ale", westvleteren, BELGIUM, "Belgium",
    subcategory="Belgian Quadrupel — Trappist Authentic",
    description="The world's most celebrated and scarce Trappist beer — available only by advance reservation from Sint-Sixtus Abbey in Westvleteren. A quadrupel of extraordinary complexity: dark plum, dried fig, dark chocolate, brown sugar, banana, clove, and Christmas spice, with the warming alcohol (10.2% ABV) seamlessly integrated. Bottle-conditioned; improves for years. The benchmark for dark Belgian abbey beer and one of the world's great fermented beverages. Consistently rated the world's best beer since 2005.",
    price_tier="ultra_premium")

rochefort = P("Abbaye Notre-Dame de Saint-Rémy (Rochefort)", "brewery", BELGIUM, "Belgium",
    production_philosophy="Cistercian Trappist excellence — three expressions, one of Belgium's greatest breweries",
    philosophy_description="The Abbey of Notre-Dame de Saint-Rémy in Rochefort has been brewing since 1595. The modern Rochefort beers (6, 8, and 10) are among Belgium's most celebrated Trappist ales, produced under the strict Authentic Trappist Product designation. Rochefort 10 — at 11.3% ABV — is the abbey's pinnacle expression: a complex dark quadrupel of chocolate, dried fruit, and spice.",
    key_personnel=[{"name": "The Trappist Community", "role": "Brewers"}],
    production_details={"established": "brewing since 1595", "range": "Rochefort 6, 8, 10", "rule": "Authentic Trappist Product"},
    reputation_narrative="Rochefort 10 is consistently rated alongside Westvleteren 12 as one of the world's great dark ales — more accessible than Westvleteren but equally complex. The three-tier range (6, 8, 10 referring to Belgian degrees of strength) demonstrates the full Rochefort style spectrum.",
    price_positioning="premium")

PROD("Rochefort Trappistes 10", "beer_ale", rochefort, BELGIUM, "Belgium",
    subcategory="Belgian Quadrupel — Trappist Authentic",
    description="Abbaye Notre-Dame de Saint-Rémy's pinnacle expression — Rochefort 10 at 11.3% ABV. A classic Belgian dark quadrupel: dark cherry, dried raisin, chocolate, leather, earthy yeast, and warm spice. Bottle-conditioned and complex from first pour; improves significantly with cellaring. One of the world's most critically acclaimed dark beers and the most accessible of Belgium's great Trappist quadrupels. Widely available in 33cl and 75cl bottles.",
    price_tier="mid_range")

PROD("Rochefort Trappistes 8", "beer_ale", rochefort, BELGIUM, "Belgium",
    subcategory="Belgian Dubbel — Trappist Authentic",
    description="The accessible middle expression of Rochefort's range at 9.2% ABV. Dark amber; dried fruit, caramel, brown sugar, clove, and bitterness. More approachable than Rochefort 10 — the ideal introduction to Belgian Trappist dark ale complexity. Bottle-conditioned; serve at 12°C in a chalice. One of the great food-pairing beers for cheese courses and red meat.",
    price_tier="mid_range")

chimay = P("Abbaye Notre-Dame de Scourmont (Chimay)", "brewery", BELGIUM, "Belgium",
    production_philosophy="Belgium's best-known Trappist brewery — Grand Réserve is the world's most distributed Trappist ale",
    philosophy_description="Abbaye Notre-Dame de Scourmont has been brewing Chimay Trappist ales since 1862. The most commercially distributed of all Authentic Trappist Product beers, Chimay's three expressions (Red Cap, White, Blue) have introduced generations of drinkers to Belgian Trappist complexity. Chimay Grande Réserve (Blue) at 9% ABV is the abbey's flagship and the world's reference for Belgian quadrupel style.",
    key_personnel=[{"name": "Brother Boniface", "role": "Head Brewer (historical)"}],
    production_details={"established": "1862", "range": "Red Cap (Dubbel), White (Tripel), Blue/Grande Réserve (Quadrupel)", "rule": "Authentic Trappist Product"},
    reputation_narrative="Chimay is Belgium's most internationally recognised Trappist brewery — the abbey's beers are available in over 50 countries. Grande Réserve (Blue) has been the world's reference for Belgian quadrupel style since 1948 and is the benchmark against which all Belgian dark ales are judged.",
    price_positioning="mid_range")

PROD("Chimay Grande Réserve (Blue)", "beer_ale", chimay, BELGIUM, "Belgium",
    subcategory="Belgian Quadrupel — Trappist Authentic",
    description="The world's reference Belgian quadrupel — Chimay's Grande Réserve (Blue Cap) at 9% ABV, first brewed in 1948. Dark copper-mahogany; dried fruit, dark plum, chocolate, clove, yeast spice, and warming alcohol. Bottle-conditioned; complex on opening and evolving for hours in the glass. Excellent cellaring potential (5+ years develops remarkable complexity). Belgium's most internationally available Authentic Trappist Product and the benchmark for the style.",
    price_tier="mid_range")

lambic_boon = P("Brouwerij Boon", "brewery", BELGIUM, "Belgium",
    production_philosophy="Gueuze: the Champagne of Belgium — spontaneous fermentation, barrel aging, blending",
    philosophy_description="Frank Boon's Lembeek brewery has been producing and blending Lambic since 1975, after rescuing the craft from near-extinction. Boon Gueuze Mariage Parfait — 'perfect marriage' — is the pinnacle of the Boon Lambic portfolio: a blend of 3-year-old Lambics from the brewery's oldest barrels, unfiltered and refermented in bottle. One of Belgium's most complex and age-worthy beers.",
    key_personnel=[{"name": "Frank Boon", "role": "Owner/Master Blender"}],
    production_details={"style": "spontaneous fermentation, coolship, foeders", "lambic_age": "1-3 year blends for Gueuze", "flagship": "Mariage Parfait"},
    reputation_narrative="Frank Boon is credited with saving Brussels Lambic culture from extinction in the 1970s. Boon Mariage Parfait is consistently rated among the world's greatest beers — a complex, dry, effervescent Gueuze that demands food pairing and rewards collector patience (ages 10+ years).",
    price_positioning="premium")

PROD("Boon Gueuze Mariage Parfait", "beer_ale", lambic_boon, BELGIUM, "Belgium",
    subcategory="Belgian Gueuze — Spontaneous Fermentation",
    description="Frank Boon's pinnacle Gueuze — a blend of 1, 2, and 3-year-old Lambics from the brewery's oldest barrels, bottle-conditioned and aged minimum 18 months. Bone dry; complex: green apple, lemon zest, oak, barnyard, brett, vinegar whisper, and fine champagne-like effervescence. The Champagne of Belgium — unfiltered, living, complex, and cellarable for 10+ years. The benchmark for traditional unblended Gueuze and among the world's most food-friendly fermented beverages.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# BAVARIA — GERMAN BEER DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== BAVARIA — REINHEITSGEBOT ===")

paulaner = P("Paulaner Brauerei", "brewery", BAVARIA, "Germany",
    production_philosophy="Munich's oldest surviving brewery — Salvator Doppelbock and Hefeweizen tradition since 1634",
    philosophy_description="Paulaner was founded by Franciscan monks in 1634 in Munich, where they brewed Salvator — the world's first Doppelbock. The tradition of monks drinking strong Lent beer (liquid bread) is the origin of the Doppelbock style. Modern Paulaner produces Bavaria's benchmark Hefeweizen and the world's original Doppelbock, both brewed under the strict Reinheitsgebot purity law.",
    key_personnel=[{"name": "Stefan Lustig", "role": "Head Brewer"}],
    production_details={"established": "1634 by Franciscan monks", "heritage": "Salvator — world's first Doppelbock", "rule": "Reinheitsgebot purity law"},
    reputation_narrative="Paulaner Salvator is the world's original Doppelbock — the word 'Salvator' is used as the generic suffix (-ator) for all German strong lager styles. Paulaner Hefeweizen is one of Munich's benchmark Weizen expressions, exported globally as the reference for the style.",
    price_positioning="mid_range")

PROD("Paulaner Salvator Doppelbock", "beer_lager", paulaner, BAVARIA, "Germany",
    subcategory="Bavarian Doppelbock — Dark Strong Lager",
    description="The world's original Doppelbock — first brewed by Franciscan monks at the Paulaner monastery in 1634 as 'liquid bread' for Lent fasting. Dark amber; rich malt, dark bread, caramel, dried fruit, chocolate, and warming alcohol (7.9% ABV). The 'Salvator' name became the template for all German Doppelbock (-ator suffix). Brewed under Reinheitsgebot (water, hops, malt, yeast only). The benchmark for the style and one of Bavaria's most historically significant beers.",
    price_tier="mid_range")

PROD("Paulaner Hefe-Weißbier Naturtrüb", "beer_ale", paulaner, BAVARIA, "Germany",
    subcategory="Bavarian Hefeweizen — Unfiltered",
    description="One of Munich's benchmark Hefeweizen expressions — unfiltered, bottle-conditioned with live yeast. Banana, clove, vanilla, and bubblegum from the characteristic Bavarian wheat yeast strain; hazy golden appearance from suspended yeast. 5.5% ABV. Brewed under Reinheitsgebot with a minimum 50% malted wheat. The classic Bavarian table beer and the reference for the unfiltered Hefeweizen style.",
    price_tier="entry")

schneider = P("Schneider Weisse", "brewery", BAVARIA, "Germany",
    production_philosophy="Munich's oldest dedicated Weizen brewery — Tap 7 and Aventinus define the style spectrum",
    philosophy_description="Georg Schneider established Munich's first private Hefeweizen brewery in 1872 when the Wittelsbach family lifted their monopoly on wheat beer. The original Tap 7 (Mein Original) defines the darker, spicier Weizen house style; Tap 6 Unser Aventinus — a wheat Doppelbock at 8.2% — is one of Bavaria's most complex and age-worthy beers. Schneider maintains the oldest continuous Weizen tradition in Munich.",
    key_personnel=[{"name": "Georg Schneider VI", "role": "Current Owner"}],
    production_details={"established": "1872", "flagship": "Tap 7 Mein Original, Tap 6 Aventinus", "distinction": "Munich's oldest Weizen specialist"},
    reputation_narrative="Schneider Weisse Aventinus is widely considered the world's greatest Weizenbock — a wheat-based Doppelbock of extraordinary complexity that ages like wine. The brewery's Tap 7 defines the darker, spicier Munich Hefeweizen style that contrasts with the more modern banana-forward styles.",
    price_positioning="mid_range")

PROD("Schneider Weisse Tap 6 Aventinus Weizen-Doppelbock", "beer_ale", schneider, BAVARIA, "Germany",
    subcategory="Bavarian Weizenbock — Wheat Doppelbock",
    description="Germany's greatest Weizenbock — a wheat-based Doppelbock at 8.2% ABV that ages like fine wine (up to 5 years). Dark amber-brown; concentrated banana, clove, dark plum, dried fig, chocolate malt, and warming spice from Bavarian wheat yeast at full intensity. The combination of wheat yeast complexity with Doppelbock depth creates Bavaria's most complex beer. Cellared vintages develop sherry-like oxidative notes. Brewed under Reinheitsgebot since 1907.",
    price_tier="mid_range")

ayinger = P("Brauerei Aying", "brewery", BAVARIA, "Germany",
    production_philosophy="Village brewery, world-class beer — Celebrator Doppelbock and Jai Alai traditions",
    philosophy_description="The Inselkammer family has brewed in the village of Aying, 25km southeast of Munich, since 1878. Ayinger's Celebrator Doppelbock — distinguished by its miniature goat ornament — is one of Germany's most internationally awarded beers, and Aying's lagers have won more World Beer Championships than any other single German brewery.",
    key_personnel=[{"name": "Franz Inselkammer Jr.", "role": "Owner/Director"}],
    production_details={"established": "1878", "location": "Aying village, near Munich", "flagship": "Celebrator Doppelbock"},
    reputation_narrative="Ayinger Celebrator Doppelbock has won more international beer awards than almost any other German beer — the miniature goat ornament around each bottle's neck is the most recognised symbol in German craft brewing. A world-class brewery that has maintained extraordinary quality while remaining a family-owned village operation.",
    price_positioning="mid_range")

PROD("Ayinger Celebrator Doppelbock", "beer_lager", ayinger, BAVARIA, "Germany",
    subcategory="Bavarian Doppelbock — Dark Strong Lager",
    description="One of Germany's most awarded beers — Ayinger's Doppelbock with the iconic miniature goat hanging from each bottle (a nod to the Latin 'bock' = goat). Deep mahogany; rich malt, roasted chocolate, caramel, licorice, and prune with remarkable smoothness at 6.7% ABV. Cold-lagered for an extended period under Reinheitsgebot. One of the benchmark Doppelbocks alongside Paulaner Salvator — more approachable and widely distributed internationally.",
    price_tier="mid_range")

# ═══════════════════════════════════════════════════════════════════════════
# ARMAGNAC — DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== ARMAGNAC — FRANCE ===")

tariquet = P("Château du Tariquet", "distillery", ARMAGNAC, "France",
    production_philosophy="Bas-Armagnac's most innovative estate — from Gascon white wine to aged brandy",
    philosophy_description="Château du Tariquet is Gascony's largest estate, producing both Côtes de Gascogne white wines and Bas-Armagnac brandy under the Grassa family since 1912. The estate's continuous alembic still and aging cellar — with barrels ranging from 5 to 40 years — produces Armagnac of exceptional depth and accessibility. The vintage-dated expressions from exceptional years are among the most collected French brandies outside Cognac.",
    key_personnel=[{"name": "Armin Grassa", "role": "Owner/Winemaker-Distiller"}],
    production_details={"established": "1912", "location": "Eauze, Bas-Armagnac", "varieties": "Ugni Blanc, Baco, Colombard, Folle Blanche"},
    reputation_narrative="Château du Tariquet is Armagnac's most internationally recognised producer after Darroze — their vintage Bas-Armagnac expressions have won international competition gold consistently. The estate demonstrates that Bas-Armagnac, distilled in continuous alembic (unlike Cognac's pot still), produces spirits of extraordinary terroir complexity.",
    price_positioning="premium")

PROD("Tariquet Bas-Armagnac 12 Year", "spirits_brandy", tariquet, ARMAGNAC, "France",
    subcategory="Bas-Armagnac — Continuous Alembic — 12 Years",
    description="Château du Tariquet's signature aged Bas-Armagnac — 12 years minimum in Gascon black oak (chêne de Gascogne). Ugni Blanc and Baco grapes from the Eauze terroir; continuous alembic distillation (unique to Armagnac, creating more complex spirit than Cognac's pot still). Vanilla, prune, dried apricot, tobacco, and toasted oak with characteristic Armagnac 'rancio' — the oxidative, nutty depth only achieved in aged brandy. A step up in complexity and value from Cognac VSOP at comparable price.",
    price_tier="premium")

PROD("Tariquet Bas-Armagnac Folle Blanche Single Grape", "spirits_brandy", tariquet, ARMAGNAC, "France",
    subcategory="Bas-Armagnac — Single Variety — Folle Blanche",
    description="A rare single-variety expression from the historic Folle Blanche grape — once the dominant Armagnac variety before phylloxera, now accounting for less than 1% of production. More delicate and floral than Ugni Blanc-dominated Armagnac: violet, white peach, pear, fresh herbs, and a fine, lifted quality unusual for the appellation. The Folle Blanche expression demonstrates Armagnac's terroir diversity and is a collector's item for spirits-focused fine dining programs.",
    price_tier="ultra_premium")

# ─── PAIRINGS ─────────────────────────────────────────────────────────────
print("\n=== PAIRINGS ===")

WVII     = get_product("Westvleteren XII (12)")
ROCH10   = get_product("Rochefort Trappistes 10")
ROCH8    = get_product("Rochefort Trappistes 8")
CHIMAY_B = get_product("Chimay Grande Réserve (Blue)")
BOON_G   = get_product("Boon Gueuze Mariage Parfait")
PAU_SALV = get_product("Paulaner Salvator Doppelbock")
PAU_HW   = get_product("Paulaner Hefe-Weißbier Naturtrüb")
SCHN_AV  = get_product("Schneider Weisse Tap 6 Aventinus Weizen-Doppelbock")
AY_CEL   = get_product("Ayinger Celebrator Doppelbock")
TAR_12   = get_product("Tariquet Bas-Armagnac 12 Year")
TAR_FB   = get_product("Tariquet Bas-Armagnac Folle Blanche Single Grape")

# Belgian Trappist pairings
PAIR(WVII, "Dark chocolate fondant with salted caramel and gold leaf",
    "complement", "established", "dessert",
    "Westvleteren XII's extraordinary complexity — dark fruit, chocolate, spice — finds its dessert partner in chocolate fondant. The salted caramel bridges the beer's sweetness and depth; the 10.2% ABV warmth is the ideal digestif-dessert bridge experience.")

PAIR(ROCH10, "Aged Gruyère and Époisses with crusty bread and honeycomb",
    "elevate", "classic", "cheese",
    "Rochefort 10's classic Trappist-beer-and-cheese affinity: the quadrupel's dried fruit and chocolate character bridge both aged hard cheese (Gruyère's nutty savory umami) and washed-rind soft cheese (Époisses's pungency). Honeycomb amplifies the beer's natural sweetness.")

PAIR(ROCH8, "Flemish beef stew (carbonade flamande) with Belgian abbey mustard",
    "complement", "classic", "main",
    "The most classic Belgian beer pairing: Rochefort 8 and carbonade flamande, the Flemish beef stew traditionally made with Belgian dubbel. The beer's dried fruit and caramel notes integrate into the braising liquid; mustard provides the acid contrast to the beer's sweetness.")

PAIR(CHIMAY_B, "Chimay cheese and walnut bread with charcuterie",
    "bridge", "classic", "casual",
    "The most natural pairing in Belgian gastronomy: Chimay Grande Réserve and Chimay cheese — the washed-rind cheese is made by the same abbey using Chimay beer in the brine. The beer's yeast character mirrors the cheese's rind; walnut bread provides textural contrast.")

PAIR(BOON_G, "Oysters on the half-shell with lemon and shallot mignonette",
    "complement", "classic", "amuse",
    "Boon Gueuze Mariage Parfait's bone-dry, bretty, effervescent character is one of the world's greatest oyster pairings — the wine-like tartness and fine bubbles cut through the oyster's brine and creaminess while the brett funk amplifies the ocean mineral quality. A classic Belgian gastronomy pairing.")

PAIR(BOON_G, "Pan-fried foie gras with cherry reduction and brioche",
    "contrast", "established", "starter",
    "Gueuze's bone-dry tartness creates the ideal contrast to foie gras richness — the acidity cuts through the fat while the brett complexity adds dimension that dessert wine cannot. The cherry reduction bridges the beer's fruit while brioche provides the textural base.")

# Bavarian beer pairings
PAIR(PAU_SALV, "Roasted pork knuckle (Schweinshaxe) with sauerkraut and mustard",
    "complement", "classic", "main",
    "Bavaria's most iconic pairing: Doppelbock and Schweinshaxe. Paulaner Salvator's malt richness and caramel sweetness cut through the pork's fat and salt while the sauerkraut's acidity provides the contrast. The most Bavarian dining experience possible.")

PAIR(PAU_HW, "Weisswurst with sweet mustard and pretzel",
    "complement", "classic", "casual",
    "The most Bavarian pairing: Hefeweizen and Weisswurst — a Munich breakfast tradition of extraordinary consistency. The wheat beer's banana and clove amplify the veal and pork sausage's subtle sweetness; sweet mustard bridges the flavours; pretzel provides the bitterness contrast.")

PAIR(SCHN_AV, "Slow-roasted duck with red cabbage and apple sauce",
    "complement", "established", "main",
    "Schneider Aventinus Weizenbock's concentrated dark fruit and wheat yeast complexity at 8.2% ABV pairs magnificently with duck — the dark fruit mirrors the red cabbage while the wheat yeast spice amplifies the warming quality of the slow-roasted preparation. Apple sauce bridges the beer's natural apple-yeast ester.")

PAIR(AY_CEL, "Braised wild boar with mushroom and dark beer sauce",
    "complement", "established", "main",
    "Ayinger Celebrator's Doppelbock richness pairs naturally with gamey wild boar — the beer used in the braising sauce creates a natural bridge, while the mushroom amplifies the beer's earthy depth. The wine-like complexity of an aged Doppelbock serves where a Burgundy might.")

# Armagnac pairings
PAIR(TAR_12, "Crème brûlée with vanilla and armagnac-soaked prunes",
    "complement", "classic", "dessert",
    "Tariquet Bas-Armagnac 12 Year's vanilla, prune, and rancio character is perfectly mirrored in crème brûlée — the custard richness matches the Armagnac's depth while armagnac-soaked prunes create a deliberate varietal bridge that amplifies the spirit's most distinctive flavour marker.")

PAIR(TAR_12, "Selection of hard aged cheeses with dried fruits and nuts",
    "complement", "established", "cheese",
    "Aged Bas-Armagnac's oxidative rancio and dried fruit character pairs beautifully with hard aged cheeses (Comté, aged Gouda, Mimolette) — the shared nutty, oxidative quality creates complementarity. Dried fruits and nuts amplify the Armagnac's own natural markers.")

PAIR(TAR_FB, "Foie gras au torchon with Sauternes jelly and brioche",
    "complement", "established", "starter",
    "Tariquet Folle Blanche's delicate floral and white peach character — unusual for Armagnac — pairs magnificently with foie gras. The lifted floral quality adds an unexpected dimension absent in aged Cognac; Sauternes jelly provides the sweet bridge while brioche grounds the richness.")

cur.close()
conn.close()
print("\n✅ Terminal 11 Batch 1 — Belgian Beer + German Beer + Armagnac complete.")
