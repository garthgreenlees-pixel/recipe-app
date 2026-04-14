#!/usr/bin/env python3
"""B156 — Champagne AOC sub-regions: Montagne de Reims, Vallée de la Marne,
   Côte des Blancs — plus Crémant d'Alsace AOC and Cava DO"""

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

# ── 1. Montagne de Reims (Champagne sub-region) ────────────────────────────────
print("=== Montagne de Reims ===")
r1 = R("Montagne de Reims", "France", "wine",
        designation_type="AOC", designation_name="Champagne — Montagne de Reims",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The forested plateau south of Reims where Pinot Noir dominates on chalky "
            "limestone soils. The Montagne's finest villages — Ambonnay, Bouzy, Mailly, "
            "Verzenay — all hold Grand Cru status. The powerful, vinous Pinot Noir grown "
            "here provides Champagne's backbone and aging potential. The 'village' "
            "Champagne movement — small growers vinifying their own fruit — has "
            "transformed understanding of this terroir."
        ),
        key_producers="Krug, Gosset, Egly-Ouriet, Marie-Noëlle Ledru, Mailly Grand Cru",
        historical_context=(
            "The Montagne de Reims has supplied Pinot Noir to the grande maisons for "
            "centuries. The reclamation by growers (récoltants-manipulants) of bottling "
            "their own wine — rather than selling to négociants — began in earnest in the "
            "1970s with Pierre Gimonnet and accelerated dramatically post-2000."
        ))

for yr, qd, pt, sn in [
    (2019, "exceptional","rising",  "Widely considered one of the greatest Champagne vintages ever"),
    (2018, "excellent",  "rising",  "Outstanding; powerful Pinot Noir expression"),
    (2016, "excellent",  "stable",  "Classic vintage; elegant and age-worthy"),
    (2015, "very_good",  "stable",  "Ripe and generous; early-drinking pleasure"),
    (2013, "excellent",  "stable",  "Precise and mineral; excellent acidty"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("Egly-Ouriet Champagne", "winery", r1, "France",
        production_philosophy="grower_traditional",
        philosophy_description="Grower Champagne; old-vine Ambonnay Pinot Noir; extended lees aging.",
        reputation_narrative="Among the world's most sought-after grower Champagnes; Ambonnay specialist.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("Egly-Ouriet Grand Cru Brut Tradition", "wine_sparkling", p1a, r1, "France",
    subcategory="champagne_non_vintage",
    description="Non-vintage Ambonnay Grand Cru Champagne; powerful Pinot Noir with exceptional depth.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "oysters with lemon and mignonette", "complement", "classic", "aperitif",
         "mineral Pinot Champagne and briny oyster — the benchmark pairing")
    PAIR(prod1a, "roast quail with foie gras stuffing", "complement", "established", "main",
         "powerful Champagne and rich game bird")
    PAIR(prod1a, "aged Comté with walnut bread", "complement", "established", "cheese",
         "vinous Pinot Champagne and aged hard cheese")
    PAIR(prod1a, "smoked salmon blini with crème fraîche", "complement", "classic", "amuse",
         "classic Champagne amuse pairing")

prod1b, new1b = PROD("Egly-Ouriet VP Vieilles Vignes Brut", "wine_sparkling", p1a, r1, "France",
    subcategory="champagne_non_vintage",
    description="Old-vine prestige cuvée; extraordinary concentration and minerality from ancient parcels.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "grilled lobster with herb butter", "complement", "classic", "main",
         "prestige Champagne and lobster — classic luxury pairing")
    PAIR(prod1b, "aged Époisses with crusty bread", "complement", "established", "cheese",
         "powerful Champagne and pungent cheese")
    PAIR(prod1b, "truffle scrambled eggs", "complement", "classic", "main",
         "old-vine Champagne and truffle — luxury breakfast/brunch")
    PAIR(prod1b, "langoustine tartare with caviar", "complement", "classic", "amuse",
         "prestige Champagne and luxury canapé")

p1b = P("Mailly Grand Cru Champagne", "winery", r1, "France",
        production_philosophy="cooperative_single_village",
        philosophy_description="Single Grand Cru village cooperative; 100% Mailly Grand Cru fruit.",
        reputation_narrative="The benchmark for Mailly Grand Cru terroir expression in Champagne.",
        price_positioning="premium")
prod1c, new1c = PROD("Mailly Grand Cru Brut Réserve Champagne", "wine_sparkling", p1b, r1, "France",
    subcategory="champagne_non_vintage",
    description="Non-vintage Mailly Grand Cru; powerful Pinot Noir expression with good depth.",
    price_tier="premium")
if new1c:
    PAIR(prod1c, "oysters with caviar", "complement", "classic", "aperitif",
         "Grand Cru Champagne and luxury shellfish")
    PAIR(prod1c, "smoked duck rillettes", "complement", "established", "amuse",
         "vinous Pinot Champagne and smoked duck")
    PAIR(prod1c, "mushroom and gruyère vol-au-vent", "complement", "established", "amuse",
         "vinous Champagne and earthy pastry snack")
    PAIR(prod1c, "prawn and avocado cocktail", "complement", "classic", "starter",
         "classic Champagne starter pairing")

prod1d, new1d = PROD("Mailly Grand Cru L'Intemporelle Blanc de Noirs", "wine_sparkling", p1b, r1, "France",
    subcategory="champagne_vintage",
    description="Prestige Blanc de Noirs from 100% Pinot Noir; vinous, structured, extraordinary.",
    price_tier="ultra_premium")
if new1d:
    PAIR(prod1d, "roast partridge with bread sauce", "complement", "established", "main",
         "vinous Pinot Champagne and game bird")
    PAIR(prod1d, "pan-fried scallops with cauliflower purée", "complement", "classic", "main",
         "Blanc de Noirs power and delicate shellfish")
    PAIR(prod1d, "aged Brie de Meaux", "complement", "established", "cheese",
         "Champagne and Brie — Île-de-France tradition")
    PAIR(prod1d, "smoked salmon and caviar canapé", "complement", "classic", "amuse",
         "luxury Blanc de Noirs and luxury canapé")

# ── 2. Côte des Blancs (Champagne sub-region) ─────────────────────────────────
print("=== Côte des Blancs ===")
r2 = R("Côte des Blancs", "France", "wine",
        designation_type="AOC", designation_name="Champagne — Côte des Blancs",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The Côte des Blancs is Chardonnay country — the purest expression of "
            "this variety in Champagne, grown on east-facing chalk slopes south of "
            "Épernay. The Grand Cru villages of Avize, Cramant, Oger, and Le "
            "Mesnil-sur-Oger produce the world's finest Blanc de Blancs Champagnes: "
            "steely, mineral, precise, and extraordinarily long-lived. Krug's Clos du "
            "Mesnil and Salon both come from Le Mesnil."
        ),
        key_producers="Salon, Krug Clos du Mesnil, Pierre Peters, Jacques Selosse, Agrapart",
        historical_context=(
            "Blanc de Blancs as a distinct Champagne style was codified in the Côte des "
            "Blancs in the mid-20th century. Salon — producing only in exceptional years "
            "from Le Mesnil — became the reference. Jacques Selosse revolutionized the "
            "category from the 1980s with oxidative, low-dosage, terroir-expressive wines."
        ))

for yr, qd, pt, sn in [
    (2019, "exceptional","rising",  "Greatest Côte des Blancs vintage in decades; electrifying mineral"),
    (2018, "excellent",  "rising",  "Rich and precise; white flower and chalk"),
    (2016, "excellent",  "stable",  "Classic; razor-sharp acidity and pure Chardonnay"),
    (2015, "very_good",  "stable",  "Generous and aromatic; earlier drinking"),
    (2012, "exceptional","rising",  "Legendary vintage; wines for 30+ years of aging"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Pierre Péters Champagne", "winery", r2, "France",
        production_philosophy="grower_terroir",
        philosophy_description="Grand Cru Le Mesnil specialist; Blanc de Blancs of exceptional precision.",
        reputation_narrative="One of the Côte des Blancs' most celebrated growers; Cuvée de Réserve is benchmark.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Pierre Péters Blanc de Blancs Grand Cru Champagne", "wine_sparkling", p2a, r2, "France",
    subcategory="champagne_non_vintage",
    description="Non-vintage Blanc de Blancs from Grand Cru Le Mesnil; chalk mineral, pure Chardonnay.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "oysters with lemon and Champagne mignonette", "complement", "classic", "aperitif",
         "chalk-mineral Blanc de Blancs and oyster — the definitive pairing")
    PAIR(prod2a, "grilled langoustine with citrus butter", "complement", "classic", "main",
         "mineral Chardonnay and delicate crustacean")
    PAIR(prod2a, "seared scallops with lemon cream", "complement", "classic", "main",
         "citrus and mineral echoes scallop sweetness")
    PAIR(prod2a, "caviar service with classic garnishes", "complement", "classic", "amuse",
         "mineral Blanc de Blancs and caviar — the iconic luxury pairing")

prod2b, new2b = PROD("Pierre Péters Les Chétillons Grand Cru Champagne", "wine_sparkling", p2a, r2, "France",
    subcategory="champagne_vintage",
    description="Single-vineyard prestige cuvée from Le Mesnil; extraordinary mineral longevity.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "raw Belon oysters with no accompaniment", "complement", "classic", "aperitif",
         "pure mineral Champagne and pure oyster")
    PAIR(prod2b, "poached turbot with Champagne sauce", "complement", "classic", "main",
         "wine used in sauce creates echo; flatfish and Blanc de Blancs")
    PAIR(prod2b, "veal tenderloin with lemon and capers", "complement", "established", "main",
         "delicate veal and precise mineral Champagne")
    PAIR(prod2b, "white truffle and egg en cocotte", "complement", "established", "main",
         "mineral and earthy luxury")

p2b = P("Agrapart et Fils Champagne", "winery", r2, "France",
        production_philosophy="biodynamic_grower",
        philosophy_description="Biodynamic viticulture; multiple Grand Cru cuvées from Avize and Cramant.",
        reputation_narrative="One of the most respected Avize growers; 7 Crus is the benchmark blend.",
        price_positioning="ultra_premium")
prod2c, new2c = PROD("Agrapart 7 Crus Brut Blanc de Blancs Champagne", "wine_sparkling", p2b, r2, "France",
    subcategory="champagne_non_vintage",
    description="Multi-site Blanc de Blancs from 7 Grand Cru and Premier Cru villages; precise and creamy.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "oysters and champagne", "complement", "classic", "aperitif",
         "classic Blanc de Blancs aperitif pairing")
    PAIR(prod2c, "sea urchin on toast with lemon", "complement", "established", "amuse",
         "chalk mineral and briny sea urchin")
    PAIR(prod2c, "grilled Dover sole with lemon butter", "complement", "classic", "main",
         "mineral Chardonnay and flatfish")
    PAIR(prod2c, "lemon tart", "complement", "established", "dessert",
         "citrus and mineral echo in dessert")

prod2d, new2d = PROD("Agrapart Avizoise Blanc de Blancs Grand Cru Champagne", "wine_sparkling", p2b, r2, "France",
    subcategory="champagne_vintage",
    description="Single-vineyard Avize Grand Cru; chalky, precise, with extraordinary longevity.",
    price_tier="ultra_premium")
if new2d:
    PAIR(prod2d, "dressed Cornish crab with herb mayonnaise", "complement", "classic", "starter",
         "chalk mineral and sweet crab")
    PAIR(prod2d, "langoustine bisque with cream", "complement", "established", "starter",
         "rich texture and mineral Champagne")
    PAIR(prod2d, "beurre blanc with poached salmon", "complement", "classic", "main",
         "citrus beurre blanc echoes Chardonnay acidity")
    PAIR(prod2d, "Brie de Meaux at room temperature", "complement", "classic", "cheese",
         "Champagne and Brie — Île-de-France tradition")

# ── 3. Vallée de la Marne (Champagne sub-region) ──────────────────────────────
print("=== Vallée de la Marne ===")
r3 = R("Vallée de la Marne", "France", "wine",
        designation_type="AOC", designation_name="Champagne — Vallée de la Marne",
        reputation_tier="respected",
        quality_trajectory="established",
        description=(
            "Stretching west from Épernay along the Marne River, the Vallée de la Marne "
            "is Pinot Meunier territory — the grape that adds roundness and early-drinking "
            "pleasure to Champagne blends. The western villages around Hautvillers (where "
            "Dom Pérignon worked) produce rich, fruit-forward styles, while growers near "
            "Aÿ make more structured, Pinot Noir-dominant wines. The Marne is also known "
            "for fruitier, immediately accessible Champagnes."
        ),
        key_producers="Bollinger, Deutz, Gatinois, Vouette & Sorbée, Chartogne-Taillet",
        historical_context=(
            "Aÿ, at the eastern end of the Vallée, was historically considered the finest "
            "Champagne village — King François I and Henry VIII both claimed vineyards here. "
            "Dom Pérignon worked at Hautvillers Abbey and, while he did not 'invent' Champagne, "
            "was crucial to refining blending and bottle techniques."
        ))

for yr, qd, pt, sn in [
    (2019, "exceptional","rising",  "Outstanding; Aÿ Pinot Noir exceptional"),
    (2018, "excellent",  "rising",  "Rich and textured Marne wines"),
    (2016, "excellent",  "stable",  "Classic vintage; good balance across styles"),
    (2015, "very_good",  "stable",  "Ripe and accessible; earlier drinking"),
    (2012, "excellent",  "stable",  "Superb; age-worthy across the valley"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Gatinois Champagne", "winery", r3, "France",
        production_philosophy="grower_aÿ_grand_cru",
        philosophy_description="100% Aÿ Grand Cru Pinot Noir; traditional methods, long aging.",
        reputation_narrative="Aÿ's most celebrated small grower; benchmark for Aÿ Pinot Noir expression.",
        price_positioning="premium",
        authority_tier=1)
prod3a, new3a = PROD("Gatinois Aÿ Grand Cru Brut Réserve Champagne", "wine_sparkling", p3a, r3, "France",
    subcategory="champagne_non_vintage",
    description="100% Aÿ Grand Cru Pinot Noir; rich, structured, vinous Champagne of great character.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "charcuterie and cornichons", "complement", "classic", "amuse",
         "vinous Pinot Champagne and charcuterie — classic bistro pairing")
    PAIR(prod3a, "roast chicken with cream sauce", "complement", "established", "main",
         "structured Champagne and roast poultry")
    PAIR(prod3a, "pan-seared duck breast with cherries", "complement", "established", "main",
         "rich Pinot Champagne and duck")
    PAIR(prod3a, "grilled turbot with beurre blanc", "complement", "classic", "main",
         "vinous Champagne and flatfish")

prod3b, new3b = PROD("Gatinois Aÿ Grand Cru Millésimé Champagne", "wine_sparkling", p3a, r3, "France",
    subcategory="champagne_vintage",
    description="Vintage Aÿ Grand Cru; powerful, age-worthy Pinot Noir Champagne of great depth.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "roast grouse with bread sauce and fried breadcrumbs", "complement", "classic", "main",
         "game bird and vinous Pinot Champagne")
    PAIR(prod3b, "aged Comté and walnut bread", "complement", "established", "cheese",
         "powerful Champagne and aged hard cheese")
    PAIR(prod3b, "smoked duck breast with fig chutney", "complement", "established", "starter",
         "richness and smoke bridge to wine")
    PAIR(prod3b, "braised veal cheek with gremolata", "complement", "established", "main",
         "structured Champagne and rich braised meat")

p3b = P("Chartogne-Taillet Champagne", "winery", r3, "France",
        production_philosophy="grower_natural",
        philosophy_description="Natural Champagne from Merfy village; low dosage, single-parcel wines.",
        reputation_narrative="One of the Marne valley's most exciting growers; Orizeaux is a benchmark.",
        price_positioning="premium")
prod3c, new3c = PROD("Chartogne-Taillet Sainte Anne Brut Champagne", "wine_sparkling", p3b, r3, "France",
    subcategory="champagne_non_vintage",
    description="Non-vintage blend; accessible and vibrant with red fruit character from Pinot Meunier.",
    price_tier="premium")
if new3c:
    PAIR(prod3c, "smoked salmon and herb crème fraîche blini", "complement", "classic", "amuse",
         "classic Champagne amuse pairing")
    PAIR(prod3c, "vegetable tempura with citrus dipping sauce", "complement", "established", "amuse",
         "red fruit and citrus against crispy vegetables")
    PAIR(prod3c, "goat cheese and herb tart", "complement", "established", "starter",
         "fruity Champagne and fresh goat cheese")
    PAIR(prod3c, "fruit-forward cheese selection", "complement", "suggested", "cheese",
         "red fruit Champagne with fruit-accented cheeses")

prod3d, new3d = PROD("Chartogne-Taillet Les Orizeaux Champagne", "wine_sparkling", p3b, r3, "France",
    subcategory="champagne_non_vintage",
    description="Single-parcel Pinot Meunier from old vines; rich, distinctive, low dosage.",
    price_tier="ultra_premium")
if new3d:
    PAIR(prod3d, "pork rillettes with cornichons and bread", "complement", "classic", "amuse",
         "old-vine Meunier and pork charcuterie")
    PAIR(prod3d, "roast pork belly with apple compote", "complement", "established", "main",
         "red fruit and pork richness")
    PAIR(prod3d, "Époisses cheese at room temperature", "complement", "established", "cheese",
         "powerful Meunier and washed-rind cheese")
    PAIR(prod3d, "wild strawberry and cream mille-feuille", "complement", "suggested", "dessert",
         "red fruit echo in wine and dessert")

# ── 4. Crémant d'Alsace AOC ───────────────────────────────────────────────────
print("=== Crémant d'Alsace AOC ===")
r4 = R("Crémant d'Alsace AOC", "France", "wine",
        designation_type="AOC", designation_name="Crémant d'Alsace",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "France's second most important sparkling wine appellation after Champagne, "
            "Crémant d'Alsace is made by the traditional method from Pinot Blanc, "
            "Auxerrois, Pinot Gris, Riesling, and Pinot Noir. The wines offer excellent "
            "quality at a fraction of Champagne's price, with the characteristic "
            "Alsatian freshness, floral aromatics, and clean fruit character. Blanc de "
            "Noirs Crémant from Pinot Noir is a regional specialty."
        ),
        key_producers="Wolfberger, Kuentz-Bas, Lucien Albrecht, Dopff au Moulin, Barmes-Buecher",
        historical_context=(
            "Crémant d'Alsace received AOC status in 1976. Production has grown "
            "dramatically as consumers seek Champagne-method sparklings at accessible "
            "prices. The wines are produced throughout Alsace and must be aged on lees "
            "for at least 9 months before disgorgement."
        ))

for yr, qd, pt, sn in [
    (2022, "very_good",  "stable",  "Fresh and aromatic; classic Alsatian character"),
    (2021, "excellent",  "stable",  "Outstanding freshness and floral aromatics"),
    (2020, "very_good",  "stable",  "Good balance and clean fruit"),
    (2019, "very_good",  "stable",  "Consistent and reliable; good value"),
    (2018, "very_good",  "stable",  "Warm year; ripe and generous"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Dopff au Moulin", "winery", r4, "France",
        production_philosophy="traditional_method_specialist",
        philosophy_description="Pioneer of Crémant d'Alsace; tradition method since 1900.",
        reputation_narrative="One of Alsace's oldest and most respected Crémant producers.",
        price_positioning="mid_range",
        authority_tier=1)
prod4a, new4a = PROD("Dopff au Moulin Crémant d'Alsace Brut", "wine_sparkling", p4a, r4, "France",
    subcategory="cremant",
    description="Classic Crémant d'Alsace; fresh, floral, Pinot Blanc dominant with clean finish.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "tarte flambée (flammekueche) with crème fraîche and lardons", "complement", "classic", "main",
         "Alsatian sparkling wine and Alsatian flatbread — regional harmony")
    PAIR(prod4a, "smoked salmon blini", "complement", "classic", "amuse",
         "classic sparkling wine amuse pairing")
    PAIR(prod4a, "choucroute garnie with sausages", "complement", "established", "main",
         "Alsatian sparkling and Alsatian cuisine")
    PAIR(prod4a, "fresh goat cheese and herb crostini", "complement", "established", "amuse",
         "fresh sparkling and light cheese")

prod4b, new4b = PROD("Dopff au Moulin Cuvée Julien Crémant d'Alsace Brut", "wine_sparkling", p4a, r4, "France",
    subcategory="cremant",
    description="Prestige Crémant; extended lees aging; richer, more complex style.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "grilled scallops with lemon butter", "complement", "established", "main",
         "complex Crémant and scallop")
    PAIR(prod4b, "foie gras terrine with Gewurztraminer gelée", "complement", "established", "starter",
         "rich Crémant and foie gras — Alsatian luxury")
    PAIR(prod4b, "mushroom and Gruyère tart", "complement", "established", "main",
         "earthy and rich pairing")
    PAIR(prod4b, "munster cheese with cumin", "complement", "classic", "cheese",
         "Alsatian sparkling and Alsatian cheese tradition")

p4b = P("Lucien Albrecht Domaine", "winery", r4, "France",
        production_philosophy="traditional_alsatian",
        philosophy_description="Family estate specializing in Crémant and Alsatian still wines.",
        reputation_narrative="One of Alsace's most respected family estates for Crémant quality.",
        price_positioning="mid_range")
prod4c, new4c = PROD("Lucien Albrecht Crémant d'Alsace Blanc de Blancs Brut", "wine_sparkling", p4b, r4, "France",
    subcategory="cremant",
    description="All-Chardonnay Crémant; lighter, crisper style with citrus and mineral.",
    price_tier="mid_range")
if new4c:
    PAIR(prod4c, "oysters with shallot vinaigrette", "complement", "classic", "aperitif",
         "mineral Blanc de Blancs and oyster")
    PAIR(prod4c, "cucumber and smoked salmon canapé", "complement", "classic", "amuse",
         "delicate sparkling and fresh canapé")
    PAIR(prod4c, "ceviche of white fish", "complement", "established", "starter",
         "crisp acidity and citrus echo")
    PAIR(prod4c, "lemon sole with herb butter", "complement", "classic", "main",
         "citrus mineral and flatfish")

prod4d, new4d = PROD("Lucien Albrecht Crémant d'Alsace Rosé Brut", "wine_sparkling", p4b, r4, "France",
    subcategory="cremant",
    description="Pinot Noir rosé Crémant; salmon-pink with strawberry and red fruit character.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "strawberry and cream mille-feuille", "complement", "classic", "dessert",
         "strawberry echo in wine and dessert")
    PAIR(prod4d, "smoked duck breast with raspberry coulis", "complement", "established", "starter",
         "red fruit bridge and smoked duck")
    PAIR(prod4d, "fruit tart selection", "complement", "classic", "dessert",
         "red fruit Crémant and fruit pastry")
    PAIR(prod4d, "prosciutto and melon", "complement", "classic", "amuse",
         "red fruit and cured meat sweetness")

# ── 5. Cava DO ────────────────────────────────────────────────────────────────
print("=== Cava DO ===")
r5 = R("Cava DO", "Spain", "wine",
        designation_type="DO", designation_name="Cava",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Spain's most important traditional-method sparkling wine, produced mainly "
            "in Penedès, Catalonia, from indigenous varieties Macabeo, Parellada, and "
            "Xarel-lo, as well as Chardonnay and Pinot Noir. The wines range from "
            "entry-level non-vintage to aged Cava de Paraje Calificado — single-vineyard "
            "wines aged 36+ months rivaling fine Champagne. Codorníu and Freixenet "
            "dominate production while artisanal producers like Gramona, Raventós i Blanc, "
            "and Recaredo raise the quality ceiling."
        ),
        key_producers="Gramona, Raventós i Blanc, Recaredo, Alta Alella, Torelló",
        historical_context=(
            "José Raventós Fatjó produced Spain's first traditional-method sparkling "
            "wine in 1872, establishing the template for Cava. The name Cava ('cellar') "
            "was adopted in 1972. Quality tiers were dramatically revised in 2020 with "
            "new aged categories: Reserva (18 months), Gran Reserva (30 months), "
            "and Cava de Paraje Calificado (36+ months from single vineyards)."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Penedès conditions for premium Cava"),
    (2021, "very_good",  "stable",  "Fresh and vibrant; good quality across tiers"),
    (2020, "excellent",  "stable",  "Classic Gran Reserva potential vintage"),
    (2019, "very_good",  "stable",  "Consistent and reliable; good value"),
    (2018, "very_good",  "stable",  "Warm vintage; ripe and approachable"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Gramona Cava", "winery", r5, "Spain",
        production_philosophy="ultra_long_aging",
        philosophy_description="Specialist in extended lees aging; Argent (7 years) and III Lustros (15 years).",
        reputation_narrative="Spain's most celebrated artisanal Cava producer; benchmark for Gran Reserva.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod5a, new5a = PROD("Gramona III Lustros Gran Reserva Cava", "wine_sparkling", p5a, r5, "Spain",
    subcategory="cava",
    description="15 years on lees; one of the world's most extraordinary traditional-method sparklings.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "aged Iberico ham (Bellota 36 months)", "complement", "classic", "aperitif",
         "oxidative aged Cava and cured Iberico — the Spanish equivalent of Champagne and caviar")
    PAIR(prod5a, "pan con tomate with anchovies", "complement", "classic", "starter",
         "Catalan bread tradition with aged Cava")
    PAIR(prod5a, "aged Manchego with quince paste", "complement", "established", "cheese",
         "complex aged sparkling and aged Spanish cheese")
    PAIR(prod5a, "sea urchin on toast", "complement", "established", "amuse",
         "mineral oxidative Cava and briny sea urchin")

prod5b, new5b = PROD("Gramona Argent Gran Reserva Cava", "wine_sparkling", p5a, r5, "Spain",
    subcategory="cava",
    description="7 years on lees; rich, complex, autolytic Gran Reserva Cava of extraordinary depth.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "grilled langoustine with garlic and olive oil", "complement", "established", "main",
         "aged sparkling and Spanish crustacean")
    PAIR(prod5b, "jamón croquetas", "complement", "classic", "amuse",
         "Spanish bar tradition elevated")
    PAIR(prod5b, "salt-baked sea bass with alioli", "complement", "established", "main",
         "aged Cava and whole fish")
    PAIR(prod5b, "manchego and honey", "complement", "classic", "cheese",
         "Spanish cheese and Gran Reserva Cava")

p5b = P("Recaredo Cava", "winery", r5, "Spain",
        production_philosophy="biodynamic_natural",
        philosophy_description="Biodynamic; zero-dosage; extended aging; single-village Cava pioneer.",
        reputation_narrative="Spain's most admired natural Cava producer; Terrers and Turó d'en Mota are iconic.",
        price_positioning="ultra_premium")
prod5c, new5c = PROD("Recaredo Terrers Brut Nature Gran Reserva Cava", "wine_sparkling", p5b, r5, "Spain",
    subcategory="cava",
    description="Zero-dosage Gran Reserva; biodynamic; pure terroir expression of Penedès character.",
    price_tier="ultra_premium")
if new5c:
    PAIR(prod5c, "raw oysters with lemon only", "complement", "classic", "aperitif",
         "zero-dosage precision and pure briny oyster")
    PAIR(prod5c, "fresh burrata with tomato and basil", "complement", "established", "starter",
         "mineral sparkling and fresh cheese")
    PAIR(prod5c, "grilled prawns with romesco", "complement", "classic", "main",
         "Catalan sauce and Catalan sparkling")
    PAIR(prod5c, "aged Garrotxa goat cheese", "complement", "established", "cheese",
         "mineral Cava and Catalan goat cheese")

prod5d, new5d = PROD("Recaredo Brut Nature Reserva Cava", "wine_sparkling", p5b, r5, "Spain",
    subcategory="cava",
    description="Zero-dosage Reserva; the entry to Recaredo's range; fresh, mineral, elegant.",
    price_tier="premium")
if new5d:
    PAIR(prod5d, "pan con tomate with jamón", "complement", "classic", "amuse",
         "Catalan tradition with Catalan sparkling")
    PAIR(prod5d, "ceviche of sea bass with citrus", "complement", "established", "starter",
         "mineral zero-dosage and citrus fish")
    PAIR(prod5d, "boquerones (marinated anchovies)", "complement", "classic", "amuse",
         "zero-dosage and briny anchovies")
    PAIR(prod5d, "Catalan cream (crema catalana)", "complement", "established", "dessert",
         "regional sparkling and regional dessert")

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
print("B156 complete.")
cur.close()
conn.close()
