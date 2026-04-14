#!/usr/bin/env python3
"""Terminal 14 — Batch 2: Champagne depth + Burgundy whites depth + Corton-Charlemagne"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs (existing)
CHAMPAGNE     = 143
MONTAGNE_REIMS = 144
COTE_BLANCS   = 145
VALLEE_MARNE  = 146
PULIGNY       = 118
CHASSAGNE     = 119
ALOXE_CORTON  = 113
NSG           = 111

# ─── HELPERS ─────────────────────────────────────────────────────────────────

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

# ─── CHAMPAGNE DEPTH ─────────────────────────────────────────────────────────
print("=== CHAMPAGNE DEPTH ===")

TAITTINGER = P(
    "Taittinger", "winery", CHAMPAGNE, "France",
    production_philosophy="Chardonnay-dominant prestige Champagne, elegance and freshness over power",
    philosophy_description=(
        "Taittinger is one of Champagne's most respected maisons, distinguished by its Chardonnay-"
        "heavy philosophy — the Comtes de Champagne Blanc de Blancs is considered among the finest "
        "prestige cuvées ever produced. The Brut Réserve (35% Chardonnay) showcases Taittinger's "
        "house style: delicate, creamy, and fresh. The Comtes de Champagne is produced only in "
        "exceptional vintages from 100% Grand Cru Côte des Blancs Chardonnay, aged for 10 years "
        "on the lees — a wine of extraordinary floral elegance, mineral depth, and 20+ year aging "
        "potential. Pierre-Emmanuel Taittinger's stewardship has maintained the family independence "
        "that makes this maison unique among Champagne's grandes marques."
    ),
    reputation_narrative=(
        "Taittinger is one of the few remaining family-owned grandes maisons in Champagne. "
        "Comtes de Champagne is consistently ranked among the 5 greatest prestige cuvées ever produced."
    ),
    price_positioning="ultra_premium"
)

ROEDERER = P(
    "Louis Roederer", "winery", MONTAGNE_REIMS, "France",
    production_philosophy="Estate Champagne with biodynamic viticulture, Cristal prestige cuvée",
    philosophy_description=(
        "Louis Roederer is the standard of excellence for estate Champagne — the maison owns the "
        "majority of the grapes it uses (exceptional in Champagne) and has converted much of its "
        "estate to biodynamic viticulture under Frédéric Rouzaud. The non-vintage Brut Premier "
        "is arguably the finest NV Champagne at its price; Cristal (created in 1876 for Tsar "
        "Alexander II) is among the most collectible luxury wines in the world. Recent Cristal "
        "vintages have achieved new heights of purity, complexity, and aging potential — the "
        "2012 and 2014 are considered among the finest ever produced."
    ),
    reputation_narrative=(
        "Louis Roederer is considered the greatest general Champagne house for consistent quality "
        "across all price points. Cristal is one of the world's most famous and collectible wines."
    ),
    price_positioning="ultra_premium"
)

BILLECART = P(
    "Billecart-Salmon", "winery", MONTAGNE_REIMS, "France",
    production_philosophy="Family-owned Champagne, the benchmark Blanc de Blancs and Rosé specialist",
    philosophy_description=(
        "Billecart-Salmon is the most respected family-owned Champagne house among sommeliers "
        "and fine dining professionals — the estate's wines represent the highest quality-to-"
        "value ratio among prestige Champagne. The Blanc de Blancs (100% Chardonnay) is one of "
        "the finest expressions of the style; the Nicolas François Billecart prestige cuvée "
        "achieves extraordinary depth. The rosé is considered the finest in all of Champagne: "
        "pure salmon, delicate, mineral, and capable of aging 15-20 years. Owned by the same "
        "family since 1818 — six generations of uncompromising quality."
    ),
    reputation_narrative=(
        "Billecart-Salmon is the sommelier's Champagne house — consistently voted the finest "
        "family-owned maison by professionals. The rosé is considered the benchmark of all "
        "Champagne rosé. A must-have on any serious fine dining Champagne list."
    ),
    price_positioning="premium"
)

SELOSSE = P(
    "Jacques Selosse", "winery", COTE_BLANCS, "France",
    production_philosophy="Oxidative, terroir-driven grower Champagne — the father of the natural Champagne movement",
    philosophy_description=(
        "Anselme Selosse is the most influential winemaker in the history of grower Champagne — "
        "his introduction of biodynamic viticulture, oxidative winemaking (solera-based), and "
        "terroir-focused thinking to Champagne transformed the entire appellation from the 1980s. "
        "Selosse's 'Initial' (the NV entry wine) and 'Substance' (the perpetual solera) challenge "
        "all preconceptions of what Champagne should taste like: oxidative, nutty, complex, "
        "mineral, and with a depth more reminiscent of Burgundy than conventional Champagne. "
        "He is the intellectual godfather of the récoltant-manipulant movement."
    ),
    reputation_narrative=(
        "Jacques Selosse is the most intellectually important Champagne producer in history — "
        "his influence on grower Champagne and natural winemaking is impossible to overstate. "
        "Initial and Substance are among the most sought-after Champagnes worldwide."
    ),
    price_positioning="ultra_premium"
)

POL_ROGER = P(
    "Pol Roger", "winery", CHAMPAGNE, "France",
    production_philosophy="Classic Champagne house — Sir Winston Churchill's favourite, traditional style",
    philosophy_description=(
        "Pol Roger is one of Champagne's most beloved traditional houses — the favourite Champagne "
        "of Winston Churchill (who consumed an estimated 42,000 bottles in his lifetime). The "
        "Churchill family relationship led to the creation of the prestige cuvée 'Cuvée Sir "
        "Winston Churchill' — a Pinot Noir-dominant vintage Champagne of extraordinary structure "
        "and aging potential. The house's White Foil Brut is considered among the finest non-"
        "vintage Champagnes at any price. Family-owned since 1849, Pol Roger maintains the "
        "most traditional approach among Champagne's grandes maisons."
    ),
    reputation_narrative=(
        "Pol Roger is Winston Churchill's Champagne — a house of impeccable tradition, "
        "quality, and historical resonance. Cuvée Sir Winston Churchill is among the most "
        "collectible prestige cuvées ever produced."
    ),
    price_positioning="ultra_premium"
)

# Champagne products
COMTES = PROD(
    "Taittinger Comtes de Champagne Blanc de Blancs",
    "wine_sparkling", TAITTINGER, CHAMPAGNE, "France",
    subcategory="blanc_de_blancs",
    description=(
        "Among the five greatest prestige Champagnes ever produced — Taittinger Comtes de Champagne "
        "is 100% Grand Cru Chardonnay from the Côte des Blancs, aged 10 years on the lees, "
        "released only in exceptional vintages. The wine shows extraordinary floral elegance: "
        "white blossom, lemon curd, white peach, almond, and a chalky mineral precision from "
        "the purest Champagne terroir. At 15-20 years, the wine develops extraordinary honey, "
        "brioche, and mineral complexity. A benchmark for Blanc de Blancs at the highest level."
    ),
    price_tier="ultra_premium"
)

CRISTAL = PROD(
    "Louis Roederer Cristal Vintage Champagne",
    "wine_sparkling", ROEDERER, MONTAGNE_REIMS, "France",
    subcategory="vintage",
    description=(
        "Created in 1876 for Tsar Alexander II of Russia, Louis Roederer Cristal is one of the "
        "world's most famous luxury wines. Equal Chardonnay and Pinot Noir from estate-farmed "
        "Grand Cru vineyards (biodynamic from 2021), aged 6 years on lees in the Roederer cellar. "
        "The wine shows extraordinary balance: brioche, lemon zest, white peach, red berry, and "
        "the pure mineral transparency of estate viticulture. Recent vintages (2012, 2014, 2016) "
        "achieve new heights of complexity. The iconic clear bottle with gold foil remains "
        "one of the most recognisable luxury wine images in the world."
    ),
    price_tier="ultra_premium"
)

BILLECART_BDB = PROD(
    "Billecart-Salmon Blanc de Blancs Champagne",
    "wine_sparkling", BILLECART, MONTAGNE_REIMS, "France",
    subcategory="blanc_de_blancs",
    description=(
        "Billecart-Salmon's Blanc de Blancs is one of the finest expressions of 100% Chardonnay "
        "Champagne from the maison's estate parcels on the Côte des Blancs. Pure, mineral, and "
        "precise: white flower, lemon, green apple, chalk, and the characteristic Billecart "
        "freshness. The extended lees aging gives brioche complexity without compromising the "
        "wine's essential citrus precision. A benchmark for sommelier-chosen Champagne."
    ),
    price_tier="premium"
)

BILLECART_NF = PROD(
    "Billecart-Salmon Nicolas François Billecart Vintage",
    "wine_sparkling", BILLECART, MONTAGNE_REIMS, "France",
    subcategory="vintage",
    description=(
        "Billecart-Salmon's prestige cuvée — the Nicolas François Billecart — is a vintage-dated "
        "equal blend of Chardonnay and Pinot Noir from Grand Cru villages, aged 8+ years on lees. "
        "The wine achieves extraordinary complexity: brioche, lemon curd, red currant, ginger, "
        "and the Billecart house's trademark mineral precision. One of the finest prestige cuvées "
        "in terms of quality-to-price ratio."
    ),
    price_tier="ultra_premium"
)

SELOSSE_INITIAL = PROD(
    "Jacques Selosse Initial Blanc de Blancs",
    "wine_sparkling", SELOSSE, COTE_BLANCS, "France",
    subcategory="blanc_de_blancs",
    description=(
        "Jacques Selosse's 'Initial' is the entry to the most intellectually radical wine in "
        "Champagne — a perpetual-reserve solera-based Blanc de Blancs of oxidative complexity, "
        "mineral depth, and Burgundian richness that challenges every preconception of what "
        "Champagne should be. Toasted hazelnut, dried apricot, oxidative Chardonnay, chalk "
        "mineral, and a nutty, complex finish unlike any conventional Champagne. More aged Sherry "
        "meets Puligny-Montrachet than standard Champagne — a reference for natural wine lovers. "
        "Virtually impossible to find; secondary market prices exceed $400+ per bottle."
    ),
    price_tier="ultra_premium"
)

CHURCHILL = PROD(
    "Pol Roger Cuvée Sir Winston Churchill Vintage",
    "wine_sparkling", POL_ROGER, CHAMPAGNE, "France",
    subcategory="vintage",
    description=(
        "Created in 1984 to honour Winston Churchill's legendary relationship with Pol Roger, "
        "Cuvée Sir Winston Churchill is the most Pinot Noir-dominant of all prestige cuvées — "
        "matching the great man's preference for full-bodied, structured Champagne. Aged 8 years "
        "minimum on lees before disgorgement, then held for further bottle age before release. "
        "The wine shows extraordinary richness: dark apple, brioche, biscuit, ginger, and a "
        "powerful Pinot structure that needs 10-15 years to fully integrate. A collector's "
        "Champagne of significant historical resonance and exceptional quality."
    ),
    price_tier="ultra_premium"
)

# ─── BURGUNDY WHITES DEPTH ───────────────────────────────────────────────────
print("\n=== BURGUNDY WHITES DEPTH ===")

SAUZET = P(
    "Etienne Sauzet", "winery", PULIGNY, "France",
    production_philosophy="Reference Puligny-Montrachet from estate and négociant parcels",
    philosophy_description=(
        "Domaine Etienne Sauzet is one of the two or three most important producers in Puligny-"
        "Montrachet — alongside Domaine Leflaive, the reference for white Burgundy at the village, "
        "premier cru, and grand cru level. Benoît Riffault (grandson of Etienne Sauzet) produces "
        "wines of extraordinary mineral precision and elegance from the appellation's finest sites: "
        "Montrachet, Bâtard-Montrachet, Bienvenues-Bâtard-Montrachet, and the superb premier crus "
        "Les Combettes and La Garenne. Sauzet's Puligny village wines are benchmarks of the style: "
        "mineral, citrus, and almost impossibly pure."
    ),
    reputation_narrative=(
        "Etienne Sauzet is considered equal with Leflaive as the reference for Puligny-Montrachet. "
        "The Montrachet and Bâtard-Montrachet grand crus from Sauzet are among the most collected "
        "white Burgundies in the world."
    ),
    price_positioning="ultra_premium"
)

RAMONET = P(
    "Domaine Ramonet", "winery", CHASSAGNE, "France",
    production_philosophy="Old-vine Chassagne-Montrachet whites and reds, the reference domaine",
    philosophy_description=(
        "Domaine Ramonet is the most important producer in Chassagne-Montrachet — the domaine "
        "that established the village's reputation as the peer of Puligny and Meursault. Pierre "
        "and Noël Ramonet began the domaine's ascent in the 1920s; their descendants continue "
        "the tradition of producing Chardonnay of extraordinary depth from the village's finest "
        "sites: Montrachet, Bâtard-Montrachet, Bienvenues-Bâtard-Montrachet, and the premier crus "
        "Les Caillerets and Morgeot. The Ramonet style emphasises weight and mineral complexity "
        "over pure delicacy — wines of Burgundy's greatest depth and aging potential."
    ),
    reputation_narrative=(
        "Domaine Ramonet is the benchmark for Chassagne-Montrachet and among the most collected "
        "domaines in all of Burgundy. Ramonet Montrachet is one of the world's most sought-after "
        "white wines."
    ),
    price_positioning="ultra_premium"
)

BONNEAU = P(
    "Bonneau du Martray", "winery", ALOXE_CORTON, "France",
    production_philosophy="The reference monopole for Corton-Charlemagne Grand Cru",
    philosophy_description=(
        "Bonneau du Martray holds the most significant portion of Corton-Charlemagne Grand Cru — "
        "a near-monopole that makes it the definitive producer of this magnificent Chardonnay "
        "appellation. The estate (acquired by Stanley Kroenke in 2017) farms biodynamically on "
        "the steep south-facing Corton hill, producing wines of extraordinary mineral depth, "
        "power, and longevity. Corton-Charlemagne Grand Cru from Bonneau du Martray is the "
        "definitive expression of the variety: citrus, white peach, mineral, and the distinctive "
        "iron and quartz character from the Corton hill's unique soils. Ages magnificently for "
        "20-30 years."
    ),
    reputation_narrative=(
        "Bonneau du Martray is THE reference for Corton-Charlemagne Grand Cru — the monopole "
        "that defines this great Burgundy appellation. One of the most sought-after white "
        "Burgundies outside the Côte de Beaune's most famous villages."
    ),
    price_positioning="ultra_premium"
)

LEROY_NSG = P(
    "Domaine Leroy", "winery", NSG, "France",
    production_philosophy="Biodynamic Burgundy at the highest level — Lalou Bize-Leroy's legendary estate",
    philosophy_description=(
        "Domaine Leroy under Lalou Bize-Leroy is considered by many critics as the greatest "
        "domaine in Burgundy — and among the greatest wine estates in the world. Strict biodynamic "
        "farming with minuscule yields (often just 10-15hl/ha vs the appellation average of 40+) "
        "produces wines of extraordinary concentration, mineral precision, and longevity. Every "
        "wine Leroy produces — from village level to grand cru — is made to the standard of its "
        "most prestigious neighbours. The Nuits-Saint-Georges premiers crus, Gevrey-Chambertin, "
        "and Vosne-Romanée from Leroy are among the world's most collectible wines. Production is "
        "minuscule; prices on the secondary market rival DRC."
    ),
    reputation_narrative=(
        "Domaine Leroy is considered by many to be Burgundy's greatest domaine — a wine estate "
        "of legendary biodynamic precision, minuscule yields, and uncompromising quality. Lalou "
        "Bize-Leroy's wines are among the world's most sought-after and age for 30-50 years."
    ),
    price_positioning="ultra_premium"
)

# Burgundy white products
SAUZET_PMC = PROD(
    "Sauzet Puligny-Montrachet Les Combettes 1er Cru",
    "wine_still", SAUZET, PULIGNY, "France",
    subcategory="white",
    description=(
        "Etienne Sauzet's Les Combettes premier cru is one of Puligny-Montrachet's greatest "
        "expressions at the 1er Cru level — the site's exceptional situation adjacent to "
        "Meursault delivers wines of unusual body and mineral richness for Puligny. Lemon curd, "
        "white peach, almond, and a deep chalk-mineral spine that ages beautifully for 10-15 "
        "years. One of Sauzet's benchmark wines and a reference for Puligny premier cru complexity."
    ),
    price_tier="ultra_premium"
)

SAUZET_BTD = PROD(
    "Sauzet Bâtard-Montrachet Grand Cru",
    "wine_still", SAUZET, PULIGNY, "France",
    subcategory="white",
    description=(
        "Sauzet Bâtard-Montrachet Grand Cru from one of Burgundy's four greatest white wine "
        "appellations: extraordinary mineral density, lemon oil, white peach, almond, and a "
        "profound limestone mineral backbone that demands 8-15 years. The wine shows the "
        "Bâtard's characteristic additional weight compared to Montrachet while retaining "
        "Puligny's essential mineral precision and tension."
    ),
    price_tier="ultra_premium"
)

RAMONET_MONTRACHET = PROD(
    "Ramonet Le Montrachet Grand Cru",
    "wine_still", RAMONET, CHASSAGNE, "France",
    subcategory="white",
    description=(
        "Among the world's greatest white wines — Domaine Ramonet's Le Montrachet from the "
        "Chassagne side of the monopole. The wine's extraordinary depth of mineral concentration, "
        "weight, and longevity sets the standard for all white Burgundy: hazelnut, white truffle, "
        "lemon oil, honey, and a profound chalk-limestone mineral structure that demands 15-20 "
        "years to reveal its full complexity. Production is minuscule; one of Burgundy's most "
        "sought-after wines. In great vintages (1978, 1986, 2002, 2014) Ramonet Montrachet is "
        "one of the 10 greatest wines ever produced."
    ),
    price_tier="ultra_premium"
)

RAMONET_BTD = PROD(
    "Ramonet Bâtard-Montrachet Grand Cru",
    "wine_still", RAMONET, CHASSAGNE, "France",
    subcategory="white",
    description=(
        "Ramonet's Bâtard-Montrachet is among the most powerful and mineral of all Grand Cru "
        "Chardonnay — from old vines on the Chassagne side of this exceptional appellation. "
        "Extraordinary density of fruit (lemon butter, almond, white truffle, toasted hazelnut) "
        "backed by a profound limestone mineral structure. Ramonet's age-worthy style means this "
        "wine needs 10-12 years before revealing its full complexity and lasts 25-30 years in "
        "great vintages."
    ),
    price_tier="ultra_premium"
)

BONNEAU_CC = PROD(
    "Bonneau du Martray Corton-Charlemagne Grand Cru",
    "wine_still", BONNEAU, ALOXE_CORTON, "France",
    subcategory="white",
    description=(
        "The definitive Corton-Charlemagne — from Bonneau du Martray's near-monopole on the "
        "Corton hill's finest south-facing vineyards. The most powerful and mineral of all "
        "Burgundy Grand Cru whites: intense lemon, white peach, almond, and the distinctive "
        "iron-and-quartz mineral character unique to the Corton hill's Permian limestone and "
        "iron-rich soils. The wine demands 8-15 years to reveal its character and ages for "
        "25-35 years. A rival to the finest Montrachet in weight and longevity — and at a "
        "fraction of the price."
    ),
    price_tier="ultra_premium"
)

LEROY_NSG_WINE = PROD(
    "Domaine Leroy Nuits-Saint-Georges Les Allots 1er Cru",
    "wine_still", LEROY_NSG, NSG, "France",
    subcategory="red",
    description=(
        "One of the rarest wines in Burgundy — Domaine Leroy's Nuits-Saint-Georges from "
        "Lalou Bize-Leroy's biodynamically-farmed estate. The minuscule yields (10-15hl/ha) "
        "produce a Pinot Noir of extraordinary concentration and mineral precision: dark cherry, "
        "blackberry, iron, graphite, and truffle with a structured tannin backbone that unfolds "
        "over 20-30 years. Every Leroy wine is produced to grand cru standards regardless of "
        "classification — this Nuits 1er Cru rivals the finest grand crus in quality. "
        "Virtually unobtainable; secondary market prices exceed many Burgundy grand crus."
    ),
    price_tier="ultra_premium"
)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Champagne pairings
PAIR(COMTES, "Roasted white asparagus with lemon butter and Oscietra caviar",
    "elevate", "established", "amuse",
    "Taittinger Comtes de Champagne and caviar with white asparagus: one of fine dining's "
    "transcendent luxury pairings. The wine's Blanc de Blancs purity and chalky mineral "
    "depth amplifies the caviar's brine; the white asparagus bridges the wine's delicate "
    "floral character; the lemon butter amplifies Chardonnay's citrus precision. A pairing "
    "that justifies the prestige cuvée's extraordinary price.")

PAIR(COMTES, "Steamed langoustines with seaweed butter",
    "elevate", "classic", "amuse",
    "Comtes de Champagne's Blanc de Blancs mineral precision is the supreme partner for "
    "raw or simply cooked crustaceans — the wine's chalk mineral character mirrors the "
    "langoustine's oceanic sweetness; seaweed butter amplifies the marine mineral connection. "
    "The wine's 10+ years of lees aging provides the depth to match luxury shellfish.")

PAIR(CRISTAL, "Beluga caviar service with blinis and crème fraîche",
    "complement", "classic", "amuse",
    "Louis Roederer Cristal was created for the Russian royal family — and caviar is the "
    "imperial pairing. The wine's estate Chardonnay purity and fine Pinot structure amplifies "
    "the beluga's clean brine while the crème fraîche bridges the wine's creamy texture. "
    "Blinis provide the neutral starch base. The most historically appropriate luxury pairing "
    "in the Champagne canon.")

PAIR(CRISTAL, "Poached turbot with Champagne beurre blanc",
    "complement", "classic", "fish_course",
    "Roederer Cristal's balance of Chardonnay freshness and Pinot Noir structure makes it "
    "uniquely versatile for the main fish course — the traditional Champagne beurre blanc "
    "creates perfect harmony between the wine and sauce. The turbot's firm, delicate flesh "
    "is elevated by the wine's mineral depth and the sauce's butter-Champagne richness.")

PAIR(BILLECART_BDB, "Oysters with finger lime and shiso",
    "complement", "classic", "amuse",
    "Billecart-Salmon Blanc de Blancs' pristine Chardonnay precision and mineral freshness "
    "is the classic oyster wine — the wine's chalk mineral mirrors the oyster's brine while "
    "finger lime citrus amplifies the Chardonnay's acidity. Shiso adds an aromatic dimension "
    "that bridges the wine's floral character with the oyster's oceanic quality.")

PAIR(BILLECART_NF, "Roasted duck breast with cherries and brown butter",
    "complement", "established", "main",
    "Nicolas François Billecart's prestige cuvée — with Pinot Noir richness and Chardonnay "
    "precision — achieves the rare combination of Champagne with a main course. The duck's "
    "richness softens the wine's acidity; the cherry sauce amplifies the Pinot component; "
    "brown butter bridges the wine's toasty complexity. An advanced pairing that demonstrates "
    "vintage prestige Champagne's versatility beyond the aperitif.")

PAIR(SELOSSE_INITIAL, "Sautéed foie gras with Sauternes reduction and brioche",
    "contrast", "adventurous", "amuse",
    "Jacques Selosse Initial's oxidative complexity and nutty mineral depth creates an "
    "extraordinary contrast with foie gras — the wine's savoury, almost Sherry-like character "
    "cuts through the fat with precision that conventional Champagne cannot achieve. Sauternes "
    "reduction bridges the wine's oxidative richness; brioche echoes its toasted hazelnut notes. "
    "An avant-garde pairing for guests who know Selosse — intellectually challenging.")

PAIR(SELOSSE_INITIAL, "Aged Comté with honey and walnut",
    "complement", "established", "cheese",
    "Selosse Initial's oxidative, nutty Chardonnay character finds its mirror in aged Comté — "
    "the cheese's caramelised, toasted hazelnut depth amplifies the wine's solera complexity. "
    "Honey bridges the wine's sweetness while walnut echoes the Initial's distinctive "
    "walnut-skin mineral character. The most intellectually satisfying Champagne-cheese pairing.")

PAIR(CHURCHILL, "Braised beef short rib with horseradish and Yorkshire pudding",
    "complement", "classic", "main",
    "Pol Roger Cuvée Sir Winston Churchill — the most Pinot Noir-dominant prestige cuvée — "
    "achieves Winston Churchill's own preference: serious wine with serious food. The rich, "
    "slow-braised beef meets its match in the wine's structured Pinot power; horseradish "
    "bridges the wine's mineral character; Yorkshire pudding provides the classic British "
    "roast context that Churchill would have approved. A pairing of historical resonance.")

PAIR(CHURCHILL, "Grouse with game chips, bread sauce, and watercress",
    "complement", "established", "main",
    "The most Churchill-appropriate game pairing: roasted grouse (Britain's finest game bird) "
    "with the wine's powerful Pinot Noir-dominant structure. The grouse's intense gamey "
    "flavour matches the Churchill's concentrated Champagne weight; bread sauce provides "
    "a traditional English foil; watercress echoes the wine's mineral freshness. "
    "A pairing of British culinary heritage and Champagne prestige.")

# Burgundy white pairings
PAIR(SAUZET_PMC, "Pan-roasted sea bass with lemon beurre blanc and chervil",
    "elevate", "classic", "fish_course",
    "Sauzet Les Combettes premier cru — among Puligny's most versatile 1er Cru — achieves "
    "its greatest expression with pan-roasted sea bass. The wine's lemon curd and almond "
    "character amplifies the bass's delicate flesh; the beurre blanc bridges the wine's "
    "acidity and texture; chervil echoes the Chardonnay's herbal mineral note. A pairing "
    "of complete Burgundy-fish harmony.")

PAIR(SAUZET_BTD, "Roasted lobster with tarragon butter and sautéed brioche",
    "elevate", "established", "main",
    "Sauzet Bâtard-Montrachet Grand Cru's extraordinary mineral density and weight achieves "
    "its ultimate expression with roasted whole lobster — the crustacean's natural sweetness "
    "and richness demands the full mineral depth of Grand Cru Chardonnay. The tarragon butter "
    "amplifies the wine's herbal character; toasted brioche echoes the wine's barrel-influenced "
    "complexity. A luxury pairing of equal grandeur.")

PAIR(RAMONET_MONTRACHET, "Whole turbot roasted on the bone with black truffle",
    "elevate", "established", "main",
    "Ramonet Le Montrachet — among the world's greatest white wines — achieves its fullest "
    "expression with whole turbot roasted on the bone, adorned with black truffle. The wine's "
    "extraordinary mineral depth amplifies the turbot's firm, complex flavour; black truffle "
    "echoes the Montrachet's signature white truffle and hazelnut notes. A pairing of "
    "transcendent luxury that belongs on a tasting menu of the highest ambition.")

PAIR(RAMONET_BTD, "Roasted veal sweetbreads with morel cream and asparagus",
    "elevate", "established", "main",
    "Ramonet Bâtard-Montrachet's extraordinary power and mineral density achieves the rare "
    "feat of pairing white Burgundy with offal of the highest quality. Veal sweetbreads' "
    "rich, mineral texture and delicate flavour is amplified by the Bâtard's weight and "
    "complexity; morel cream bridges the wine's earthy character; asparagus provides a "
    "green freshness that the wine's acidity supports.")

PAIR(BONNEAU_CC, "Roasted chicken with Comté and truffle under the skin",
    "complement", "classic", "main",
    "Bonneau du Martray Corton-Charlemagne's mineral power and iron-inflected character "
    "achieves its finest food expression with chicken cooked with Comté and truffle. The "
    "Corton's iron mineral amplifies the cheese's caramel depth; truffle bridges the wine's "
    "iron-quartz mineral to the aromatic fungi; the chicken's fat provides the textural "
    "richness that the wine's structure can penetrate. A Burgundian classic.")

PAIR(BONNEAU_CC, "Sautéed king scallop with celeriac purée and hazelnut brown butter",
    "elevate", "established", "starter",
    "Corton-Charlemagne's mineral weight and toasted hazelnut character creates an outstanding "
    "pairing with seared scallops — the wine's almond and hazelnut notes mirror the brown "
    "butter; the celeriac purée bridges the wine's earthy mineral; the scallop's natural "
    "sweetness amplifies the Chardonnay's fruit. A luxury starter pairing of complete logic.")

PAIR(LEROY_NSG_WINE, "Roasted pheasant with chestnut, Agen prune, and game jus",
    "complement", "established", "main",
    "Domaine Leroy's extraordinary Nuits-Saint-Georges — concentrated beyond its classification "
    "through biodynamic precision — achieves its finest expression with roasted pheasant and "
    "autumn accompaniments. The wine's dark cherry, iron, and truffle character amplifies the "
    "pheasant's gamey richness; chestnut provides earthy sweetness; prune bridges the wine's "
    "dark fruit; game jus deepens the mineral character. A pairing for Burgundy's most "
    "concentrated red wines.")

cur.close()
conn.close()
print("\n✅ Terminal 14 Batch 2 — Champagne depth + Burgundy whites complete.")
