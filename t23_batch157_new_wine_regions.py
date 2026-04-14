#!/usr/bin/env python3
"""B157 — Alsace Grand Cru AOC, Sancerre AOC, Pouilly-Fumé AOC,
   Muscadet Sèvre et Maine AOC, Savennières AOC — Loire and Alsace"""

import psycopg2

WRITE_DSN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(WRITE_DSN)
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, designation_type=None, designation_name=None,
      reputation_tier=None, quality_trajectory=None, description=None,
      key_producers=None, historical_context=None):
    cur.execute("SELECT id FROM beverage_regions WHERE name=%s AND country=%s", (name, country))
    row = cur.fetchone()
    if row:
        print(f"  Region exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_regions
            (name, country, beverage_family, designation_type, designation_name,
             reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region inserted: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
        (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
        VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
        (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, producer_type, region_id, country, production_philosophy=None,
      philosophy_description=None, reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"    Producer inserted: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── 1. Alsace Grand Cru AOC ───────────────────────────────────────────────────
print("=== Alsace Grand Cru AOC ===")
r1 = R("Alsace Grand Cru AOC", "France", "wine",
        designation_type="AOC", designation_name="Alsace Grand Cru",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "51 named Grand Cru vineyards in Alsace producing the region's finest "
            "Riesling, Gewurztraminer, Pinot Gris, and Muscat. Each Grand Cru has "
            "distinct terroir — limestone at Altenberg de Bergheim, granite at Schlossberg, "
            "sandstone at Kirchberg de Barr — creating remarkable wine diversity. "
            "Riesling Grand Crus can age for decades; Gewurztraminer Grand Cru produces "
            "some of the world's most intense aromatic whites. Vendanges Tardives (VT) "
            "and Sélection de Grains Nobles (SGN) from Grand Crus are world-class dessert wines."
        ),
        key_producers="Weinbach, Zind-Humbrecht, Trimbach, Hugel, Ostertag",
        historical_context=(
            "Alsace's Grand Cru system was established in 1983, though individual vineyards "
            "had been recognized as superior for centuries. Trimbach notably refuses to "
            "label its Clos Sainte Hune (from Rosacker Grand Cru) as Grand Cru, arguing "
            "the system is flawed. Despite this, Grand Cru wines represent Alsace at its "
            "most profound."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Superb vintage; classic Grand Cru aromatic richness"),
    (2021, "very_good",  "stable",  "Fresh, precise wines; excellent acidity"),
    (2020, "excellent",  "rising",  "Outstanding concentration from warm dry season"),
    (2019, "excellent",  "stable",  "Classic Alsace vintage; concentrated and aromatic"),
    (2017, "very_good",  "stable",  "Good; accessible style; drinking beautifully"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Domaine Zind-Humbrecht", "winery", r1, "France",
        production_philosophy="biodynamic_terroir",
        philosophy_description="Biodynamic; single-vineyard expression; low yields and minimal intervention.",
        reputation_narrative="Alsace's most celebrated estate; benchmark for Grand Cru terroir expression.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Zind-Humbrecht Riesling Rangen de Thann Clos Saint Urbain Grand Cru", "wine_still", p1a, r1, "France",
    subcategory="white",
    description="From the volcanic Rangen Grand Cru; one of France's greatest Rieslings — mineral, complex, ages decades.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "grilled langoustine with citrus and herbs", "complement", "classic", "main",
         "volcanic mineral Riesling and delicate crustacean")
    PAIR(prod1a, "aged Munster cheese with cumin", "complement", "classic", "cheese",
         "Grand Cru Riesling and Alsatian Munster — the regional classic")
    PAIR(prod1a, "wild mushroom and truffle tart", "complement", "established", "main",
         "volcanic mineral and earthy mushroom")
    PAIR(prod1a, "seared scallops with Riesling sauce", "complement", "classic", "main",
         "wine used in sauce creates echo; classic preparation")

prod1b, new1b = PROD("Zind-Humbrecht Gewurztraminer Hengst Grand Cru", "wine_still", p1a, r1, "France",
    subcategory="white",
    description="Hengst Grand Cru Gewurztraminer; explosive rose, lychee, spice aromatics with grand scale.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "roasted Alsatian duck with fruit sauce", "complement", "established", "main",
         "spiced aromatic wine and duck richness")
    PAIR(prod1b, "foie gras with lychee and ginger", "complement", "classic", "starter",
         "lychee echo in wine and foie gras preparation")
    PAIR(prod1b, "Thai green curry with coconut", "contrast", "established", "main",
         "aromatic spice and tropical fruit bridge")
    PAIR(prod1b, "Munster à point with cumin seeds", "complement", "classic", "cheese",
         "the definitive Alsatian cheese and Gewurztraminer pairing")

p1b = P("Domaine Weinbach", "winery", r1, "France",
        production_philosophy="organic_terroir",
        philosophy_description="Organic farming; Clos des Capucins monopole; meticulous single-vineyard wines.",
        reputation_narrative="One of Alsace's most beloved estates; Clos des Capucins is a landmark monopole.",
        price_positioning="premium")
prod1c, new1c = PROD("Weinbach Riesling Schlossberg Grand Cru Alsace", "wine_still", p1b, r1, "France",
    subcategory="white",
    description="Granite Schlossberg Grand Cru Riesling; the benchmark for granite-terroir Alsatian Riesling.",
    price_tier="premium")
if new1c:
    PAIR(prod1c, "freshwater crayfish with Riesling cream sauce", "complement", "classic", "main",
         "classic Alsatian preparation echoes the wine")
    PAIR(prod1c, "choucroute garnie with Riesling", "complement", "classic", "main",
         "Alsatian sauerkraut dish and regional Riesling")
    PAIR(prod1c, "grilled trout with almonds", "complement", "classic", "main",
         "freshwater fish and Alsatian Riesling")
    PAIR(prod1c, "smoked trout with horseradish cream", "complement", "established", "starter",
         "smoke and mineral bridge")

prod1d, new1d = PROD("Weinbach Gewurztraminer Furstentum Grand Cru Alsace", "wine_still", p1b, r1, "France",
    subcategory="white",
    description="Furstentum Grand Cru Gewurztraminer; rich, aromatic, powerful — built for food and aging.",
    price_tier="premium")
if new1d:
    PAIR(prod1d, "baeckeoffe (Alsatian meat and potato casserole)", "complement", "classic", "main",
         "rich Gewurztraminer and Alsatian comfort food")
    PAIR(prod1d, "blue cheese and walnut", "complement", "established", "cheese",
         "aromatic intensity cuts through blue cheese")
    PAIR(prod1d, "roast pork with spiced apple sauce", "complement", "established", "main",
         "spice echo and apple bridge")
    PAIR(prod1d, "lychee and rose water dessert", "bridge", "classic", "dessert",
         "lychee echo in wine and dessert")

# ── 2. Sancerre AOC ───────────────────────────────────────────────────────────
print("=== Sancerre AOC ===")
r2 = R("Sancerre AOC", "France", "wine",
        designation_type="AOC", designation_name="Sancerre",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "The Loire Valley's most celebrated appellation, Sancerre produces "
            "benchmark Sauvignon Blanc from chalk, flint (silex), and limestone "
            "soils on the right bank of the Loire. The wines are crisp, mineral, "
            "and intensely aromatic with green herbs, citrus, and distinctive "
            "smoky flint character from silex soils. Sancerre also produces a "
            "small amount of Pinot Noir red and rosé of remarkable elegance."
        ),
        key_producers="Henri Bourgeois, Lucien Crochet, Henri Pellé, Château de Sancerre, Vacheron",
        historical_context=(
            "Sancerre's wine reputation was largely post-WWII — its wines were mostly "
            "sold locally. The 1970s and 1980s saw global recognition of Sauvignon Blanc "
            "as a variety, and Sancerre became its benchmark expression. The silex soils "
            "of Sancerre — fossilized oyster shell — uniquely flavour the region's finest wines."
        ))

for yr, qd, pt, sn in [
    (2023, "excellent",  "rising",  "Fresh, pure Sancerre with outstanding aromatics"),
    (2022, "very_good",  "stable",  "Balanced vintage; classic Sancerre character"),
    (2021, "excellent",  "stable",  "Superb freshness; one of Sancerre's best recent years"),
    (2020, "very_good",  "stable",  "Good; rich style with moderate acidity"),
    (2019, "very_good",  "stable",  "Classic Sancerre vintage; textbook aromatics"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Henri Bourgeois Sancerre", "winery", r2, "France",
        production_philosophy="terroir_multiple_sites",
        philosophy_description="Multi-terroir approach; La Bourgeoise and d'Antan are top cuvées.",
        reputation_narrative="One of Sancerre's most consistent and reputed family estates.",
        price_positioning="premium",
        authority_tier=1)
prod2a, new2a = PROD("Henri Bourgeois Sancerre La Bourgeoise Blanc", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Prestige Sancerre blanc; silex and chalk blend of concentrated, mineral Sauvignon Blanc.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "chèvre frais with herbs on toast", "complement", "classic", "amuse",
         "Sancerre and goat cheese — the definitive pairing")
    PAIR(prod2a, "oysters with lemon", "complement", "classic", "aperitif",
         "flint mineral and briny oyster")
    PAIR(prod2a, "asparagus with goat cheese and lemon vinaigrette", "complement", "classic", "starter",
         "grassy Sauvignon and asparagus")
    PAIR(prod2a, "grilled sole with herb butter", "complement", "established", "main",
         "mineral acidity and flatfish")

prod2b, new2b = PROD("Henri Bourgeois Sancerre Les Baronnes Blanc", "wine_still", p2a, r2, "France",
    subcategory="white",
    description="Village Sancerre from limestone soils; crisp, aromatic, classic style.",
    price_tier="mid_range")
if new2b:
    PAIR(prod2b, "Crottin de Chavignol (local goat cheese)", "complement", "classic", "cheese",
         "Sancerre and local Chavignol goat cheese — the regional tradition")
    PAIR(prod2b, "cucumber and dill canapé", "complement", "established", "amuse",
         "herbal freshness bridge")
    PAIR(prod2b, "smoked salmon and capers", "complement", "classic", "starter",
         "mineral acidity and smoked fish")
    PAIR(prod2b, "green salad with goat cheese dressing", "complement", "classic", "starter",
         "classic Loire Valley salad pairing")

p2b = P("Domaine Vacheron", "winery", r2, "France",
        production_philosophy="biodynamic_old_vine",
        philosophy_description="Biodynamic Sancerre; old vines on diverse terroirs; reds and whites.",
        reputation_narrative="Among Sancerre's most celebrated producers; reds are benchmark Pinot Noir.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("Vacheron Sancerre Blanc Les Romains", "wine_still", p2b, r2, "France",
    subcategory="white",
    description="Old-vine silex Sancerre; mineral, intense, long-lived with gunflint character.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "grilled langoustine with citrus", "complement", "classic", "main",
         "flint mineral and delicate crustacean")
    PAIR(prod2c, "salt cod brandade with olive oil", "complement", "established", "main",
         "mineral acidity and preserved fish")
    PAIR(prod2c, "Épineuil goat cheese aged 8 weeks", "complement", "classic", "cheese",
         "aged goat cheese and mineral Sancerre")
    PAIR(prod2c, "fresh oysters Gillardeau", "complement", "classic", "aperitif",
         "flint and oyster — profound mineral pairing")

prod2d, new2d = PROD("Vacheron Sancerre Rouge Les Guignes", "wine_still", p2b, r2, "France",
    subcategory="red",
    description="Old-vine Pinot Noir from Sancerre; silk, red fruit, chalk mineral — elegant Loire red.",
    price_tier="ultra_premium")
if new2d:
    PAIR(prod2d, "roast quail with cherry sauce", "complement", "classic", "main",
         "delicate Loire Pinot and game bird")
    PAIR(prod2d, "wild mushroom and lentil salad", "complement", "established", "starter",
         "earthy Pinot and earthy ingredients")
    PAIR(prod2d, "seared duck breast with raspberry jus", "complement", "established", "main",
         "silky red fruit and duck")
    PAIR(prod2d, "aged Crottin de Chavignol", "complement", "classic", "cheese",
         "aged local cheese and local Pinot Noir")

# ── 3. Pouilly-Fumé AOC ───────────────────────────────────────────────────────
print("=== Pouilly-Fumé AOC ===")
r3 = R("Pouilly-Fumé AOC", "France", "wine",
        designation_type="AOC", designation_name="Pouilly-Fumé",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "Across the Loire River from Sancerre, Pouilly-Fumé produces Sauvignon Blanc "
            "of a different character — fuller, richer, and less herbaceous, often with "
            "a distinctive smoky note (fumé) from the silex soils. The best Pouilly-Fumé "
            "rivals Sancerre in complexity and longevity. Didier Dagueneau's ultra-precise "
            "single-vineyard wines — Silex, Pur Sang — transformed understanding of "
            "what Sauvignon Blanc could achieve."
        ),
        key_producers="Didier Dagueneau, Château de Tracy, Michel Redde, Jean-Claude Chatelain",
        historical_context=(
            "Pouilly-Fumé's 'fumé' character — reminiscent of gunsmoke — was long thought "
            "to derive from the silex soils; modern research suggests it comes from certain "
            "thiols in Sauvignon Blanc. Didier Dagueneau, the 'enfant terrible' of the Loire "
            "who died in 2008, left behind wines that transformed the region's ambitions."
        ))

for yr, qd, pt, sn in [
    (2023, "very_good",  "stable",  "Classic Pouilly-Fumé; good aromatic intensity"),
    (2022, "excellent",  "rising",  "Outstanding concentration and freshness"),
    (2021, "excellent",  "stable",  "Superb freshness; silex soils shine"),
    (2020, "very_good",  "stable",  "Rich and textured; excellent quality"),
    (2019, "very_good",  "stable",  "Classic vintage; good aromatics and structure"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Domaine Didier Dagueneau", "winery", r3, "France",
        production_philosophy="low_yield_precision",
        philosophy_description="Ultra-low yields; fermentation in barrel; single-vineyard precision.",
        reputation_narrative="The most celebrated and controversial Pouilly-Fumé producer; Silex is legendary.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod3a, new3a = PROD("Dagueneau Pouilly-Fumé Silex", "wine_still", p3a, r3, "France",
    subcategory="white",
    description="Benchmark Pouilly-Fumé from flint soils; smoky, intense, mineral — one of France's greatest Sauvignon Blancs.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "oysters with lemon and Oscietra caviar", "complement", "classic", "aperitif",
         "flint mineral and luxury seafood — iconic pairing")
    PAIR(prod3a, "grilled langoustine with Dagueneau butter", "complement", "classic", "main",
         "precise mineral Sauvignon and crustacean")
    PAIR(prod3a, "goat cheese soufflé with herbs", "complement", "classic", "starter",
         "goat cheese and Loire Sauvignon — the classic combination")
    PAIR(prod3a, "raw oysters on ice", "complement", "classic", "aperitif",
         "gunsmoke mineral and briny oyster")

prod3b, new3b = PROD("Dagueneau Pouilly-Fumé Pur Sang", "wine_still", p3a, r3, "France",
    subcategory="white",
    description="Second flagship cuvée; from young vines on silex; precise, smoky, age-worthy.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "chèvre frais with herbs", "complement", "classic", "amuse",
         "Loire Sauvignon and fresh goat cheese")
    PAIR(prod3b, "smoked eel with horseradish and apple", "complement", "established", "starter",
         "smoke in wine and smoked eel bridge")
    PAIR(prod3b, "seared scallops with asparagus", "complement", "classic", "main",
         "mineral Sauvignon and delicate shellfish")
    PAIR(prod3b, "grilled turbot with caper sauce", "complement", "established", "main",
         "mineral precision and flatfish")

p3b = P("Château de Tracy", "winery", r3, "France",
        production_philosophy="traditional_estate",
        philosophy_description="Historic estate on the Loire river; traditional Pouilly-Fumé style.",
        reputation_narrative="One of Pouilly-Fumé's oldest and most reliable estates.",
        price_positioning="premium")
prod3c, new3c = PROD("Château de Tracy Pouilly-Fumé", "wine_still", p3b, r3, "France",
    subcategory="white",
    description="Classic Pouilly-Fumé; fresh, aromatic, Loire Sauvignon with mineral character.",
    price_tier="mid_range")
if new3c:
    PAIR(prod3c, "grilled white asparagus with sauce Maltaise", "complement", "classic", "starter",
         "Loire Sauvignon and asparagus — spring tradition")
    PAIR(prod3c, "fresh goat cheese and herb salad", "complement", "classic", "starter",
         "classic Loire Valley pairing")
    PAIR(prod3c, "ceviche of sea bass with citrus", "complement", "established", "starter",
         "citrus and mineral echo")
    PAIR(prod3c, "salmon rillettes with capers and lemon", "complement", "established", "amuse",
         "Loire tradition with river fish")

prod3d, new3d = PROD("Château de Tracy 101 Rangs Pouilly-Fumé", "wine_still", p3b, r3, "France",
    subcategory="white",
    description="Prestige selection from 101-row old vine parcels; more concentrated and complex.",
    price_tier="premium")
if new3d:
    PAIR(prod3d, "grilled lobster with herb butter", "complement", "established", "main",
         "rich Pouilly-Fumé and lobster")
    PAIR(prod3d, "pike quenelles with Nantua sauce", "complement", "classic", "main",
         "Loire river fish and Loire white wine")
    PAIR(prod3d, "sea urchin on brioche", "complement", "established", "amuse",
         "mineral and briny sea urchin")
    PAIR(prod3d, "leek and goat cheese tart", "complement", "established", "main",
         "Loire Sauvignon and goat cheese")

# ── 4. Muscadet Sèvre et Maine AOC ────────────────────────────────────────────
print("=== Muscadet Sèvre et Maine AOC ===")
r4 = R("Muscadet Sèvre et Maine AOC", "France", "wine",
        designation_type="AOC", designation_name="Muscadet Sèvre et Maine",
        reputation_tier="respected",
        quality_trajectory="rediscovering",
        description=(
            "The archetypal seafood wine of the Loire estuary, Muscadet is made from "
            "Melon de Bourgogne on granite and gneiss soils at the mouth of the Loire. "
            "Wines aged sur lie (on the lees) develop additional complexity, texture, "
            "and a distinctive yeasty minerality. The finest Muscadet — from the Crus "
            "Communaux de Gorges, Le Pallet, Clisson — can age for a decade or more "
            "and rival far more expensive white wines."
        ),
        key_producers="Luneau-Papin, Marc Olivier, Bonnet-Huteau, Pepière, Brégeon",
        historical_context=(
            "Muscadet was devastated by overproduction and quality decline in the 1980s-90s. "
            "The Crus Communaux system (2011) recognized six superior terroir zones with "
            "minimum 18 months lees aging, transforming the category. A new generation "
            "of producers is reclaiming Muscadet's reputation as a serious wine."
        ))

for yr, qd, pt, sn in [
    (2023, "very_good",  "stable",  "Fresh and mineral; classic Muscadet style"),
    (2022, "excellent",  "rising",  "Outstanding sur lie complexity and depth"),
    (2021, "excellent",  "stable",  "Superb freshness and mineral character"),
    (2020, "very_good",  "stable",  "Good quality; accessible and food-friendly"),
    (2019, "very_good",  "stable",  "Excellent year; minerality and lees integration"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Domaine Luneau-Papin", "winery", r4, "France",
        production_philosophy="sur_lie_terroir",
        philosophy_description="Multiple single-terroir Muscadets; long lees aging and minimal sulfur.",
        reputation_narrative="Muscadet's most celebrated producer; Muscadet Classique is the benchmark.",
        price_positioning="mid_range",
        authority_tier=1)
prod4a, new4a = PROD("Luneau-Papin Muscadet Sèvre et Maine sur Lie L d'Or", "wine_still", p4a, r4, "France",
    subcategory="white",
    description="Prestige Muscadet sur lie; granite terroir with long lees aging — mineral, textured, age-worthy.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Breton oysters with lemon mignonette", "complement", "classic", "aperitif",
         "Muscadet and Atlantic oysters — the definitive Atlantic France pairing")
    PAIR(prod4a, "mussels marinière with white wine", "complement", "classic", "main",
         "Muscadet and mussels from the Loire estuary")
    PAIR(prod4a, "clam chowder with crusty bread", "complement", "established", "main",
         "bivalve and sur lie Muscadet")
    PAIR(prod4a, "grilled sardines with lemon", "complement", "classic", "main",
         "Atlantic fish and Atlantic wine")

prod4b, new4b = PROD("Luneau-Papin Muscadet Gorges Cru Communal", "wine_still", p4a, r4, "France",
    subcategory="white",
    description="Cru Communal from Gorges terroir; minimum 18 months sur lie; remarkable aging potential.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "fresh lobster with herb mayonnaise", "complement", "established", "main",
         "Cru Muscadet and crustacean — elevated pairing")
    PAIR(prod4b, "grilled turbot with sea vegetables", "complement", "classic", "main",
         "mineral Muscadet and flatfish")
    PAIR(prod4b, "sea urchin pasta with lemon and herbs", "complement", "established", "main",
         "brine and mineral bridge")
    PAIR(prod4b, "oysters and brown bread butter", "complement", "classic", "aperitif",
         "pure Cru Muscadet and pure oyster")

p4b = P("Domaine de la Pépière", "winery", r4, "France",
        production_philosophy="natural_minimal_intervention",
        philosophy_description="Natural Muscadet; low sulfur; long sur lie; gneiss terroir specialist.",
        reputation_narrative="Among the Loire's most respected natural wine producers; Clos des Briords is iconic.",
        price_positioning="mid_range")
prod4c, new4c = PROD("Pépière Muscadet Sèvre et Maine sur Lie", "wine_still", p4c := None or p4b, r4, "France",
    subcategory="white",
    description="Classic natural Muscadet sur lie; gneiss mineral, lees texture, long finish.",
    price_tier="entry")
if new4c:
    PAIR(prod4c, "oysters with shallot vinaigrette", "complement", "classic", "aperitif",
         "mineral Muscadet and Atlantic oyster")
    PAIR(prod4c, "fried calamari with lemon and aioli", "complement", "established", "main",
         "crisp acidity cuts through fried calamari")
    PAIR(prod4c, "fresh shrimp with herb dip", "complement", "classic", "amuse",
         "Atlantic seafood and Atlantic wine")
    PAIR(prod4c, "smoked mackerel and cucumber canapé", "complement", "established", "amuse",
         "lees texture and smoked fish")

prod4d, new4d = PROD("Pépière Clos des Briords Muscadet Sèvre et Maine Vieilles Vignes", "wine_still", p4b, r4, "France",
    subcategory="white",
    description="Old-vine monopole; exceptional concentration and mineral depth for long aging.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "sea bass en croûte with beurre blanc", "complement", "classic", "main",
         "fine Muscadet and classic French fish preparation")
    PAIR(prod4d, "scallops in their shell with herbs", "complement", "classic", "main",
         "mineral Muscadet and scallop")
    PAIR(prod4d, "langoustine bisque with cream", "complement", "established", "starter",
         "lees richness and crustacean bisque")
    PAIR(prod4d, "fresh oyster and cucumber amuse", "complement", "classic", "amuse",
         "mineral and brine echo")

# ── 5. Savennières AOC ────────────────────────────────────────────────────────
print("=== Savennières AOC ===")
r5 = R("Savennières AOC", "France", "wine",
        designation_type="AOC", designation_name="Savennières",
        reputation_tier="prestigious",
        quality_trajectory="rediscovering",
        description=(
            "One of France's most distinctive and age-worthy white wines, Savennières "
            "produces dry Chenin Blanc from schist and volcanic soils on south-facing "
            "slopes above the Loire. The wines are fiercely mineral, intensely concentrated, "
            "and require years of aging to reveal their extraordinary complexity. The "
            "monopole vineyards Coulée de Serrant and Roche aux Moines are among France's "
            "most celebrated terroirs."
        ),
        key_producers="Nicolas Joly, Domaine des Baumard, Closel, Château d'Épiré",
        historical_context=(
            "Nicolas Joly at Clos de la Coulée de Serrant is not only Savennières's most "
            "famous producer but the father of biodynamic viticulture in France. His writings "
            "and evangelism for biodynamics in the 1980s influenced a generation of winemakers "
            "worldwide. Savennières's austere style fell from fashion; it is now rediscovered "
            "as a benchmark for age-worthy dry Chenin Blanc."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Savennières vintage; concentration and mineral depth"),
    (2021, "very_good",  "stable",  "Fresh and precise; mineral backbone excellent"),
    (2020, "excellent",  "stable",  "Classic Savennières character; age-worthy"),
    (2019, "very_good",  "stable",  "Consistent quality; good mineral expression"),
    (2018, "excellent",  "rising",  "Rich and concentrated; excellent aging potential"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Nicolas Joly Clos de la Coulée de Serrant", "winery", r5, "France",
        production_philosophy="biodynamic_pioneer",
        philosophy_description="Biodynamic pioneer; Coulée de Serrant monopole; minimal intervention.",
        reputation_narrative="France's most famous biodynamic estate; Coulée de Serrant is a national monument.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Joly Savennières Coulée de Serrant", "wine_still", p5a, r5, "France",
    subcategory="white",
    description="The most celebrated Savennières; biodynamic Chenin Blanc of extraordinary minerality and longevity.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "poached Loire salmon with beurre blanc", "complement", "classic", "main",
         "Loire river fish and Loire white wine — the regional classic pairing")
    PAIR(prod5a, "roast veal with cream and mushrooms", "complement", "established", "main",
         "textured Chenin Blanc and rich veal")
    PAIR(prod5a, "pike perch with butter and herbs", "complement", "classic", "main",
         "freshwater fish and structured Loire white")
    PAIR(prod5a, "scallops with Savennières beurre blanc", "complement", "classic", "main",
         "wine used in sauce creates echo; classic preparation")

prod5b, new5b = PROD("Joly Savennières Clos de la Bergerie", "wine_still", p5a, r5, "France",
    subcategory="white",
    description="Second wine of La Coulée de Serrant; more accessible but same biodynamic philosophy.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "grilled turbot with lemon butter and capers", "complement", "classic", "main",
         "mineral Chenin Blanc and flatfish")
    PAIR(prod5b, "chicken with morel cream sauce", "complement", "established", "main",
         "rich texture and structured Chenin Blanc")
    PAIR(prod5b, "asparagus with hollandaise", "complement", "established", "starter",
         "mineral and spring vegetable")
    PAIR(prod5b, "Brillat-Savarin cheese", "complement", "established", "cheese",
         "rich triple cream and textured Chenin Blanc")

p5b = P("Domaine des Baumard", "winery", r5, "France",
        production_philosophy="traditional_estate",
        philosophy_description="Loire specialist across multiple appellations; Savennières and Coteaux du Layon.",
        reputation_narrative="One of the Loire's most respected estates; Clos du Papillon is the benchmark.",
        price_positioning="premium")
prod5c, new5c = PROD("Baumard Savennières Clos du Papillon", "wine_still", p5b, r5, "France",
    subcategory="white",
    description="Benchmark Savennières; structured, mineral Chenin Blanc with excellent aging potential.",
    price_tier="premium")
if new5c:
    PAIR(prod5c, "grilled langoustine with herb butter", "complement", "established", "main",
         "rich mineral Savennières and crustacean")
    PAIR(prod5c, "pike quenelles with Nantua sauce", "complement", "classic", "main",
         "classic Loire valley preparation")
    PAIR(prod5c, "veal sweetbreads with lemon caper sauce", "complement", "established", "main",
         "mineral acidity and rich sweetbreads")
    PAIR(prod5c, "aged Comté with walnuts", "complement", "established", "cheese",
         "structured Chenin Blanc and aged hard cheese")

prod5d, new5d = PROD("Baumard Savennières Clos de Saint Yves", "wine_still", p5b, r5, "France",
    subcategory="white",
    description="Entry Savennières from Baumard; approachable mineral Chenin Blanc with excellent freshness.",
    price_tier="mid_range")
if new5d:
    PAIR(prod5d, "fried whitebait with lemon", "complement", "classic", "amuse",
         "mineral Loire white and simple fried fish")
    PAIR(prod5d, "mussels marinière with white wine", "complement", "established", "main",
         "mineral Chenin Blanc and bivalves")
    PAIR(prod5d, "smoked salmon and cream cheese tartine", "complement", "established", "starter",
         "mineral acidity and smoked fish")
    PAIR(prod5d, "goat cheese and herb omelette", "complement", "established", "main",
         "Loire white and goat cheese")

# ── Final counts ──────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nDB — regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"DB — producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"DB — products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"DB — pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"DB — vintages: {cur.fetchone()[0]}")
print("B157 complete.")
cur.close()
conn.close()
