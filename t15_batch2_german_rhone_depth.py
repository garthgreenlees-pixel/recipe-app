#!/usr/bin/env python3
"""Terminal 15 — Batch 2: German Riesling depth (Rheingau + Saar + Nahe) + Rhône depth (Rayas)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs (existing)
RHEINGAU       = 165  # Need to verify
NAHE           = 164
SAAR           = 163
CHATEAUNEUF    = 139

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def get_region_id(name):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Region not found: {name}")

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
    print(f"  ✓ NEW producer: {name} (id={pid})")
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
    print(f"  ✓ NEW product: {name} (id={pid})")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# Get actual region IDs
RHEINGAU = get_region_id("Rheingau")
NAHE     = get_region_id("Nahe")
SAAR     = get_region_id("Saar")
CHATEAUNEUF = get_region_id("Châteauneuf-du-Pape")
print(f"Regions: Rheingau={RHEINGAU}, Nahe={NAHE}, Saar={SAAR}, ChNdP={CHATEAUNEUF}")

# ─── RHEINGAU ────────────────────────────────────────────────────────────────
print("\n=== RHEINGAU DEPTH ===")

ROBERT_WEIL = P(
    "Weingut Robert Weil", "winery", RHEINGAU, "Germany",
    production_philosophy="The reference estate for Rheingau Riesling — from dry GG to legendary Trockenbeerenauslese",
    philosophy_description=(
        "Weingut Robert Weil under Wilhelm Weil is the prestige address of the Rheingau — "
        "consistently producing the finest dry Riesling Grosses Gewächs (particularly from the "
        "Gräfenberg vineyard) and among the world's greatest Trockenbeerenauslese and Eiswein. "
        "The estate's 80-hectare holdings in Kiedrich on deep phyllite and loess soils produce "
        "Riesling of extraordinary aromatic complexity, precise acidity, and aging potential. "
        "Wilhelm Weil's commitment to quality across the full range — from the Kiedrich village "
        "Riesling to the legendary TBA — makes this the benchmark for Rhine Riesling at every "
        "price point."
    ),
    reputation_narrative=(
        "Robert Weil is the most prestigious estate in the Rheingau — producing the finest dry "
        "Riesling and the most collectible late-harvest wines in the entire Rhine. The Gräfenberg "
        "Riesling Grosses Gewächs is considered among Germany's greatest dry Rieslings."
    ),
    price_positioning="ultra_premium"
)

SCHLOSS_JB = P(
    "Schloss Johannisberg", "winery", RHEINGAU, "Germany",
    production_philosophy="The oldest Riesling estate in the world — 1,000 years of Rheingau tradition",
    philosophy_description=(
        "Schloss Johannisberg is the most historically important Riesling estate in the world — "
        "continuously producing wine since 817 AD and the estate credited with discovering "
        "Spätlese (late harvest) winemaking in 1775. The estate's steep south-facing slope above "
        "the Rhine, with its unique loess and slate terroir, produces Riesling of distinctive "
        "floral elegance, mineral clarity, and the characteristic Johannisberg style: creamy, "
        "honeyed, and age-worthy. The Gelblack (yellow capsule) Riesling Spätlese and Rotlack "
        "Auslese are the estate's historic benchmarks."
    ),
    reputation_narrative=(
        "Schloss Johannisberg is the most historically significant wine estate in Germany — "
        "1,200 years of continuous wine production and the birthplace of Spätlese. A "
        "pilgrimage destination for Riesling lovers worldwide."
    ),
    price_positioning="premium"
)

WEIL_GRAEF = PROD(
    "Robert Weil Kiedrich Gräfenberg Riesling Grosses Gewächs",
    "wine_still", ROBERT_WEIL, RHEINGAU, "Germany",
    subcategory="white",
    description=(
        "The definitive Rheingau Grosses Gewächs — Robert Weil's Gräfenberg GG is considered "
        "the finest dry Riesling in the entire Rhine Gorge. From the Gräfenberg vineyard's steep "
        "phyllite-and-loess soils: extraordinary mineral precision, grapefruit, white peach, "
        "apricot, and a stony mineral spine of exceptional depth. Bone dry (GG standard), "
        "high natural acidity (typically 8-9 g/L), and an aging potential of 15-25 years. "
        "In great vintages (2015, 2017, 2019, 2021) this rivals the finest Mosel Riesling "
        "for complexity and longevity."
    ),
    price_tier="ultra_premium"
)

WEIL_TBA = PROD(
    "Robert Weil Kiedrich Gräfenberg Riesling Trockenbeerenauslese",
    "wine_dessert", ROBERT_WEIL, RHEINGAU, "Germany",
    subcategory="sweet",
    description=(
        "Among the world's greatest sweet wines — Weil's Trockenbeerenauslese from the "
        "Gräfenberg vineyard is produced only in exceptional vintages from individually selected "
        "botrytised grapes. Production is minuscule (often fewer than 100 cases); the wine's "
        "concentrated apricot jam, honey, saffron, and mineral complexity ages virtually "
        "indefinitely. The 1999, 2005, and 2015 TBAs from Weil are considered among the "
        "greatest German sweet wines ever produced. Secondary market prices are extraordinary."
    ),
    price_tier="ultra_premium"
)

JOHANNISBERG_SP = PROD(
    "Schloss Johannisberg Riesling Spätlese Gelblack",
    "wine_still", SCHLOSS_JB, RHEINGAU, "Germany",
    subcategory="white",
    description=(
        "The most historically significant German wine still in production — Schloss Johannisberg "
        "Spätlese 'Gelblack' (Yellow Capsule) is produced from the estate that discovered "
        "Spätlese in 1775. From the historic south-facing slope above the Rhine: off-dry, "
        "with 30-40g/L residual sugar balanced by high Riesling acidity. Honeyed peach, "
        "apricot, slate mineral, and a floral elegance that speaks of 1,200 years of "
        "winemaking tradition. The wine ages magnificently for 20-30 years."
    ),
    price_tier="premium"
)

# ─── SAAR DEPTH ──────────────────────────────────────────────────────────────
print("\n=== SAAR DEPTH ===")

VAN_VOLXEM = P(
    "Van Volxem", "winery", SAAR, "Germany",
    production_philosophy="Bone-dry Grosses Gewächs Riesling from Saar — the modern dry Saar revolution",
    philosophy_description=(
        "Roman Niewodniczanski purchased the historic Van Volxem estate in 1999 and transformed "
        "it into the most ambitious producer in the Saar. While Egon Müller defines the "
        "traditional late-harvest style, Van Volxem defines the modern dry Saar — bone-dry "
        "Grosses Gewächs Riesling of extraordinary mineral intensity, high acidity, and 20+ "
        "year aging potential. The Scharzhofberg, Kanzem Altenberg, and Wawerner Herrenberg GGs "
        "are among Germany's most mineral and age-worthy dry Rieslings. The wines are fiercely "
        "individual — initially austere, revelatory with 5-10 years of cellaring."
    ),
    reputation_narrative=(
        "Van Volxem is the standard-bearer for dry Saar Riesling — the modern estate that "
        "proved the Saar could produce Grosses Gewächs of world-class stature. A must-follow "
        "estate for Riesling enthusiasts seeking dry German wine."
    ),
    price_positioning="ultra_premium"
)

ZILLIKEN = P(
    "Forstmeister Geltz Zilliken", "winery", SAAR, "Germany",
    production_philosophy="Traditional Saar Riesling — Saarburger Rausch single vineyard specialist",
    philosophy_description=(
        "The Zilliken family estate in Saarburg specialises exclusively in the Saarburger Rausch "
        "vineyard — one of the Saar's finest sites, with steep blue slate soils that produce "
        "Riesling of extraordinary mineral precision and elegance. Hanno Zilliken produces the "
        "full Prädikat range (Kabinett through TBA) from this single vineyard, with the "
        "Saarburger Rausch Riesling Auslese considered one of the finest expressions of "
        "off-dry Saar style: delicate, mineral, with apricot fruit and a steel-like precision. "
        "The estate's approach is traditional and uncompromising — Riesling and nothing else."
    ),
    reputation_narrative=(
        "Forstmeister Geltz Zilliken is one of the Saar's most admired traditional estates — "
        "the Saarburger Rausch single vineyard produces some of Germany's most precise and "
        "mineral off-dry Rieslings."
    ),
    price_positioning="premium"
)

VAN_VOLXEM_SCHAR = PROD(
    "Van Volxem Scharzhofberg Riesling Grosses Gewächs",
    "wine_still", VAN_VOLXEM, SAAR, "Germany",
    subcategory="white",
    description=(
        "Van Volxem's bone-dry Grosses Gewächs from the legendary Scharzhofberg vineyard — "
        "the most famous single vineyard in Germany (Egon Müller's estate takes precedence for "
        "TBA, Van Volxem for dry GG). Bone dry, extraordinarily mineral: slate, flint, white "
        "peach, lime zest, and a laser-focused acidity that initially seems austere before "
        "revealing extraordinary complexity at 8-15 years. One of Germany's greatest dry "
        "Rieslings — the antithesis of Mosel's fruit-forward style."
    ),
    price_tier="ultra_premium"
)

ZILLIKEN_RAUSCH = PROD(
    "Forstmeister Geltz Zilliken Saarburger Rausch Riesling Auslese",
    "wine_still", ZILLIKEN, SAAR, "Germany",
    subcategory="white",
    description=(
        "Forstmeister Geltz Zilliken's Saarburger Rausch Auslese is one of the finest "
        "expressions of traditional Saar off-dry Riesling: delicate residual sugar (80-100g/L) "
        "balanced by the Saar's piercing acidity, producing a wine of extraordinary tension. "
        "Apricot, white peach, slate mineral, white flower, and a rapier-like precision from "
        "the blue slate soils of the Rausch vineyard. Drink between 10-25 years for full "
        "expression of this classical German Riesling style."
    ),
    price_tier="premium"
)

# ─── NAHE DEPTH ──────────────────────────────────────────────────────────────
print("\n=== NAHE DEPTH ===")

SCHAFER_FROHLICH = P(
    "Schäfer-Fröhlich", "winery", NAHE, "Germany",
    production_philosophy="Biodynamic Nahe Riesling — Tim Fröhlich's multiple GG single vineyards",
    philosophy_description=(
        "Tim Fröhlich's Schäfer-Fröhlich estate in Bockenau is among the most exciting German "
        "Riesling producers — converting to biodynamics in the 2000s and producing multiple "
        "Grosses Gewächs from distinct Nahe terroirs: Bockenauer Felseneck (porphyry), "
        "Schlossberg, and Kupfergrube (blue slate from the Nahe's volcanic deposits). "
        "The wines show extraordinary mineral diversity — the porphyry-driven Felseneck is "
        "the most complex and structured; all the GGs share Fröhlich's signature: dry, "
        "mineral, with the Nahe's characteristic floral elegance and 15-20 year potential. "
        "Critically acclaimed and increasingly difficult to obtain."
    ),
    reputation_narrative=(
        "Schäfer-Fröhlich is the most exciting current estate in the Nahe — Tim Fröhlich's "
        "biodynamic Grosses Gewächs wines are among the most critically acclaimed German "
        "Rieslings of the past decade."
    ),
    price_positioning="ultra_premium"
)

SF_FELSENECK = PROD(
    "Schäfer-Fröhlich Bockenauer Felseneck Riesling Grosses Gewächs",
    "wine_still", SCHAFER_FROHLICH, NAHE, "Germany",
    subcategory="white",
    description=(
        "The most critically acclaimed wine from Schäfer-Fröhlich — the Bockenauer Felseneck GG "
        "from porphyry (ancient volcanic) soils is unique among German Riesling for its "
        "red fruit character alongside the classic mineral precision. Red apple, blood orange, "
        "flint, smoke, and volcanic mineral from the porphyry subsoil — utterly distinctive "
        "and unlike any other German white wine. The biodynamic farming amplifies the terroir "
        "expression to extraordinary levels. Age 8-20 years for full complexity."
    ),
    price_tier="ultra_premium"
)

# ─── CHÂTEAUNEUF-DU-PAPE DEPTH (Rayas) ───────────────────────────────────────
print("\n=== CHÂTEAUNEUF-DU-PAPE DEPTH ===")

RAYAS = P(
    "Château Rayas", "winery", CHATEAUNEUF, "France",
    production_philosophy="100% Grenache Châteauneuf-du-Pape — the world's greatest Grenache producer",
    philosophy_description=(
        "Château Rayas is the most sought-after wine in Châteauneuf-du-Pape — arguably the "
        "world's greatest expression of pure Grenache from 60-80 year old vines in the "
        "appellation's northernmost, most forest-protected site. The late Emmanuel Reynaud's "
        "idiosyncratic approach (very late harvest, high natural alcohol, no new oak, minimal "
        "intervention) produces wines of extraordinary complexity: raspberry, pomegranate, "
        "kirsch, iron, white pepper, and an ethereal quality that defies the grape's usual "
        "alcohol-driven richness. The wine's trademark is levity — extraordinary concentration "
        "without weight. Pignan (the second wine) is barely less magnificent. Production is "
        "limited; secondary market prices are extraordinary."
    ),
    reputation_narrative=(
        "Château Rayas is the most sought-after wine in Châteauneuf-du-Pape and one of the "
        "most collectible wines in the world. The standard against which all Grenache is measured. "
        "Rayas is to Châteauneuf what DRC is to Burgundy."
    ),
    price_positioning="ultra_premium"
)

RAYAS_WINE = PROD(
    "Château Rayas Châteauneuf-du-Pape Rouge",
    "wine_still", RAYAS, CHATEAUNEUF, "France",
    subcategory="red",
    description=(
        "The world's greatest Grenache — Château Rayas from 60-80 year old vines in the "
        "sand and clay soils of the appellation's northernmost, most shaded site. Unlike "
        "any other Châteauneuf: no massive extraction, no new oak, extraordinarily fresh "
        "for its alcohol (15%+). Raspberry, kirsch, pomegranate, iron mineral, white pepper, "
        "and an ethereal translucency more reminiscent of great Pinot Noir than of powerful "
        "Grenache. The wine opens at 8-10 years and ages magnificently for 30-40 years. "
        "Production: fewer than 2,000 cases; secondary market exceeds $400/bottle."
    ),
    price_tier="ultra_premium"
)

RAYAS_BLANC = PROD(
    "Château Rayas Châteauneuf-du-Pape Blanc",
    "wine_still", RAYAS, CHATEAUNEUF, "France",
    subcategory="white",
    description=(
        "The rarest white Châteauneuf-du-Pape — Rayas Blanc from old-vine Clairette and "
        "Grenache Blanc in the same forest-protected northern site. The wine shows an "
        "extraordinary character: oxidative depth, lanolin, white truffle, quince, and "
        "a mineral concentration unlike any other Southern Rhône white. Ages magnificently "
        "for 20-30 years, developing extraordinary complexity reminiscent of aged white "
        "Burgundy. One of the world's rarest and most sought-after white wines. "
        "Production is minuscule — often fewer than 300 cases per vintage."
    ),
    price_tier="ultra_premium"
)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Rheingau pairings
PAIR(WEIL_GRAEF, "Roasted sea bass with lemon butter sauce and grilled leek",
    "elevate", "classic", "fish_course",
    "Robert Weil Gräfenberg GG — the finest dry Riesling in the Rheingau — elevates "
    "sea bass with lemon butter to grand cru level. The wine's extraordinary mineral "
    "precision and grapefruit character amplifies the fish's delicacy; the leek's "
    "sweetness bridges the wine's floral aromatics; lemon butter mirrors the Riesling's "
    "citrus precision. A Rheingau pairing of the highest distinction.")

PAIR(WEIL_GRAEF, "Sautéed sweetbreads with caper brown butter and lemon",
    "complement", "established", "main",
    "Weil Gräfenberg GG's mineral weight and dry precision achieves a sophisticated "
    "pairing with veal sweetbreads — the offal's rich, mineral texture is complemented "
    "by the wine's slate mineral backbone; caper beurre noisette bridges the wine's "
    "acidity; lemon amplifies the Riesling's citrus character. One of the most "
    "technically sophisticated Riesling food pairings.")

PAIR(WEIL_TBA, "Foie gras terrine with Riesling Auslese jelly and brioche",
    "complement", "classic", "amuse",
    "Robert Weil TBA and foie gras: one of the world's transcendent luxury pairings. "
    "The wine's concentrated apricot, honey, and saffron amplifies the foie gras's "
    "natural sweetness while the extraordinary acidity cuts through the fat with "
    "precision. Auslese jelly bridges wine and foie; brioche echoes the TBA's "
    "honeyed complexity. A pairing for the world's most celebrated tasting menus.")

PAIR(WEIL_TBA, "Époisses de Bourgogne with sourdough",
    "contrast", "established", "cheese",
    "Robert Weil TBA and washed-rind Époisses: the classic contrast of sweet Riesling "
    "with powerfully aromatic cheese. The wine's honey and apricot sweetness contrasts "
    "magnificently with the cheese's pungent, barnyard character; the extraordinary "
    "acidity cuts through the fat; the sourdough provides a neutral bridge between "
    "two of France and Germany's most extreme food-wine expressions.")

PAIR(JOHANNISBERG_SP, "Poached salmon with mustard cream sauce",
    "complement", "classic", "fish_course",
    "Schloss Johannisberg Spätlese's off-dry elegance and historic honeyed character "
    "is the definitive German Riesling pairing for poached salmon — the wine's residual "
    "sugar amplifies the fish's natural oils while the mustard cream provides the "
    "acidic bridge. The most historically appropriate German wine and fish combination: "
    "1,200 years of Rheingau tradition meets classic European fish cookery.")

PAIR(JOHANNISBERG_SP, "Roasted pork belly with apple, sage, and crackling",
    "complement", "classic", "main",
    "Schloss Johannisberg Spätlese's off-dry character is the traditional German "
    "pairing for roasted pork — the wine's gentle sweetness bridges the pork's "
    "fat while the apple amplifies the Riesling's fruit character. Sage echoes "
    "the wine's herbaceous complexity; the crackling provides textural contrast "
    "to the wine's silky off-dry finish. Classic German wine and food tradition.")

# Saar pairings
PAIR(VAN_VOLXEM_SCHAR, "Grilled sole with capers, lemon, and brown butter",
    "complement", "classic", "fish_course",
    "Van Volxem Scharzhofberg GG's bone-dry mineral precision is the ideal partner "
    "for sole meunière — the wine's slate and flint mineral character amplifies the "
    "sole's delicate white flesh; caper's acidity bridges the wine's steely precision; "
    "brown butter echoes the wine's mineral complexity without softening its essential "
    "austerity. A pairing of German dry Riesling's greatest food affinity.")

PAIR(VAN_VOLXEM_SCHAR, "Raw oysters with apple mignonette",
    "complement", "classic", "amuse",
    "Van Volxem Scharzhofberg GG's extraordinary mineral tension — almost more Chablis "
    "than Rhine — achieves the classic mineral wine and raw oyster combination. The "
    "wine's flint and slate character mirrors the oyster's brine; apple mignonette "
    "bridges the Riesling's fruit; the wine's bone-dry structure provides the acidic "
    "clarity that cuts through the oyster's texture with precision.")

PAIR(ZILLIKEN_RAUSCH, "Seared duck liver (foie gras) with peach and ginger",
    "complement", "established", "amuse",
    "Zilliken Saarburger Rausch Auslese's delicate off-dry style — with its apricot "
    "precision and piercing acidity — achieves an elegant pairing with seared foie gras "
    "and peach. The wine's residual sugar amplifies the peach's sweetness while the "
    "Saar acidity cuts the foie's fat; ginger bridges the wine's spice note. A refined, "
    "traditional German Prädikat pairing of considerable elegance.")

PAIR(ZILLIKEN_RAUSCH, "Thai prawn curry with lemongrass and jasmine rice",
    "complement", "established", "main",
    "Zilliken Rausch Auslese's off-dry character and piercing acidity is a classic "
    "match for Thai prawn curry — the residual sugar tames the chilli heat; the "
    "lemongrass amplifies the Riesling's floral aromatics; the prawn's sweetness "
    "bridges wine and sauce. Traditional German off-dry Riesling wisdom applied "
    "to contemporary Southeast Asian cuisine.")

# Nahe pairings
PAIR(SF_FELSENECK, "Cured salmon with beet, dill cream, and lemon caviar",
    "complement", "established", "starter",
    "Schäfer-Fröhlich Felseneck GG's distinctive red-fruit and volcanic mineral "
    "character creates an unusual pairing with cured salmon — the wine's blood orange "
    "and red apple notes bridge the salmon's cured sweetness; beet amplifies the "
    "wine's earthy mineral character; dill cream echoes the Riesling's herbal precision. "
    "A pairing that reveals the porphyry's distinctive flavour profile.")

PAIR(SF_FELSENECK, "Roasted guinea fowl with wild mushroom and thyme jus",
    "complement", "adventurous", "main",
    "Schäfer-Fröhlich Felseneck GG's complexity and mineral depth achieves a "
    "sophisticated pairing with guinea fowl — the wine's red fruit and flint character "
    "bridges the bird's delicate game flavour; wild mushroom amplifies the volcanic "
    "mineral; thyme echoes the wine's herbaceous mineral note. An advanced Riesling "
    "food pairing that demonstrates dry German Riesling's versatility beyond fish.")

# Château Rayas pairings
PAIR(RAYAS_WINE, "Roasted leg of Sisteron lamb with herbes de Provence and garlic",
    "complement", "classic", "main",
    "Château Rayas Grenache and Provençal herb-roasted lamb: the defining Rhône pairing. "
    "The wine's extraordinary raspberry and kirsch purity meets the garrigue herb character "
    "of Provençal lamb — herbes de Provence amplify Rayas's wild herb note; the lamb's "
    "fat softens the wine's ethereal quality; garlic bridges the wine's aromatic depth. "
    "A pairing of southern France's greatest wine and its most cherished meat tradition.")

PAIR(RAYAS_WINE, "Spit-roasted pigeon with cherry sauce and pommes sarladaise",
    "elevate", "established", "main",
    "Château Rayas's ethereal Grenache — more Pinot Noir-like than typical Châteauneuf — "
    "achieves its most complete food expression with pigeon: the game bird's delicate "
    "gamey richness is amplified by the wine's raspberry and pomegranate character; "
    "cherry sauce bridges wine and bird; pommes sarladaise provide the Périgord richness "
    "that the wine's translucent quality demands. A pairing of Rhône and Périgord elegance.")

PAIR(RAYAS_BLANC, "Roasted Jerusalem artichoke with truffle and aged Comté",
    "elevate", "established", "starter",
    "Château Rayas Blanc — the most complex white Châteauneuf ever made — achieves its "
    "highest expression with Jerusalem artichoke and truffle: the wine's oxidative depth, "
    "lanolin, and white truffle character amplifies the artichoke's earthy sweetness; "
    "truffle amplifies the wine's signature aromatic; aged Comté bridges the oxidative "
    "richness with savoury umami depth. An extraordinary pairing for this extraordinary wine.")

PAIR(RAYAS_BLANC, "Poached turbot with saffron beurre blanc and fennel fronds",
    "elevate", "established", "fish_course",
    "Rayas Blanc's extraordinary mineral depth and oxidative complexity at its finest with "
    "turbot: the wine's white truffle and quince character amplifies the turbot's complexity; "
    "saffron beurre blanc bridges the wine's Mediterranean aromatic heritage; fennel "
    "echoes the wine's anise-mineral character. A pairing for the world's rarest white "
    "Southern Rhône with the finest flatfish.")

cur.close()
conn.close()
print("\n✅ Terminal 15 Batch 2 — German Riesling depth + Rhône depth complete.")
