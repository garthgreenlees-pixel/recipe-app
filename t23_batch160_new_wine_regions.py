#!/usr/bin/env python3
"""B160 — Mosel QbA (Germany), Rheingau QbA, Pfalz QbA,
   Nahe QbA, Franken QbA — German Riesling and wine regions deep dive"""

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

# ── 1. Mosel QbA ──────────────────────────────────────────────────────────────
print("=== Mosel QbA ===")
r1 = R("Mosel QbA", "Germany", "wine",
        designation_type="QbA", designation_name="Mosel",
        reputation_tier="iconic",
        quality_trajectory="established",
        description=(
            "The world's greatest Riesling region, Mosel produces wines of incomparable "
            "delicacy and complexity from near-vertical slate slopes above the winding "
            "river. The combination of Devonian blue and red slate, extreme slate-reflected "
            "heat, and cool nights creates Riesling of gossamer lightness, electric "
            "acidity, and mineral precision that ages for decades. The great estates of "
            "the Mittelmosel — Erdener Treppchen, Wehlener Sonnenuhr, Bernkasteler "
            "Doctor — are among the world's most storied vineyard sites."
        ),
        key_producers="J.J. Prüm, Egon Müller, Karthäuserhof, Loosen, Maximin Grünhäuser",
        historical_context=(
            "The Mosel has produced wine since Roman times — Ausonius described the "
            "vineyards in the 4th century AD. The great estates were established in the "
            "18th-19th centuries, often by the Catholic church. Egon Müller's Scharzhofberger "
            "Trockenbeerenauslese regularly achieves the highest prices of any white wine "
            "at auction globally."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Classic Mosel vintage; slate minerality and electric acidity"),
    (2021, "excellent",  "stable",  "Superb freshness; the best recent vintage for Mosel Riesling"),
    (2020, "very_good",  "stable",  "Rich and ripe; excellent Spätlese and Auslese"),
    (2019, "excellent",  "rising",  "Concentrated and structured; great aging potential"),
    (2018, "very_good",  "stable",  "Warm year; riper style, powerful but balanced"),
]:
    VIN(r1, yr, qd, pt, sn)

p1a = P("J.J. Prüm Weingut", "winery", r1, "Germany",
        production_philosophy="traditional_slate_terroir",
        philosophy_description="Conservative traditional methods; wines released late; extended aging.",
        reputation_narrative="The benchmark Mosel estate; Wehlener Sonnenuhr is the world's most famous Riesling site.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod1a, new1a = PROD("J.J. Prüm Wehlener Sonnenuhr Riesling Spätlese Mosel", "wine_still", p1a, r1, "Germany",
    subcategory="white",
    description="From the Sonnenuhr sundial vineyard; off-dry Spätlese of extraordinary mineral elegance.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "smoked eel with apple and horseradish", "complement", "classic", "main",
         "classic German fish preparation and Mosel Riesling")
    PAIR(prod1a, "freshwater crayfish with dill and cream", "complement", "classic", "main",
         "river shellfish and Mosel river wine")
    PAIR(prod1a, "graved lax (cured salmon) with mustard dill sauce", "complement", "classic", "main",
         "Scandinavian preparation and German Riesling")
    PAIR(prod1a, "pork schnitzel with lemon", "complement", "classic", "main",
         "German preparation and German wine — regional tradition")

prod1b, new1b = PROD("J.J. Prüm Wehlener Sonnenuhr Riesling Auslese Mosel", "wine_still", p1a, r1, "Germany",
    subcategory="sweet_white",
    description="Auslese Sonnenuhr; honeyed, concentrated, with decades of aging potential.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "blue cheese with honey and walnuts", "complement", "classic", "cheese",
         "sweet Auslese balances blue cheese intensity")
    PAIR(prod1b, "peach Melba", "complement", "classic", "dessert",
         "peach echo to stone fruit character")
    PAIR(prod1b, "foie gras with quince jelly", "complement", "established", "starter",
         "sweet acidity and richness of foie gras")
    PAIR(prod1b, "roasted pear and almond tart", "complement", "classic", "dessert",
         "stone fruit and mineral echo")

p1b = P("Weingut Loosen (Dr. Loosen)", "winery", r1, "Germany",
        production_philosophy="old_vine_organic",
        philosophy_description="Organic farming; old ungrafted vines on blue slate; quality-focused ambassador.",
        reputation_narrative="Germany's most widely recognized Mosel producer; ambassador for Riesling globally.",
        price_positioning="premium")
prod1c, new1c = PROD("Dr. Loosen Erdener Treppchen Riesling Spätlese Mosel", "wine_still", p1c := None or p1b, r1, "Germany",
    subcategory="white",
    description="Old-vine ungrafted Spätlese from Treppchen; classic Mosel style with electric acidity.",
    price_tier="premium")
if new1c:
    PAIR(prod1c, "pan-fried trout with almonds and butter", "complement", "classic", "main",
         "Mosel river trout and Mosel Riesling — regional tradition")
    PAIR(prod1c, "Asian-spiced pork belly", "complement", "established", "main",
         "off-dry Riesling and spiced pork")
    PAIR(prod1c, "smoked salmon with cream cheese and capers", "complement", "classic", "starter",
         "slate mineral and smoked fish")
    PAIR(prod1c, "aged Gouda with caraway", "complement", "established", "cheese",
         "German-style cheese and Riesling")

prod1d, new1d = PROD("Dr. Loosen Bernkasteler Badstube Riesling Kabinett Mosel", "wine_still", p1b, r1, "Germany",
    subcategory="white",
    description="Kabinett from Badstube site; light, delicate, with mere 8% alcohol and pure Mosel character.",
    price_tier="mid_range")
if new1d:
    PAIR(prod1d, "steamed asparagus with clarified butter", "complement", "classic", "main",
         "Riesling Kabinett and German white asparagus — springtime classic")
    PAIR(prod1d, "ceviche with yuzu and herbs", "complement", "suggested", "starter",
         "delicate acidity and citrus echo")
    PAIR(prod1d, "sushi and sashimi selection", "complement", "established", "main",
         "delicate Kabinett and Japanese raw fish")
    PAIR(prod1d, "cucumber and herb salad", "complement", "classic", "starter",
         "refreshing acidity and light salad")

# ── 2. Rheingau QbA ───────────────────────────────────────────────────────────
print("=== Rheingau QbA ===")
r2 = R("Rheingau QbA", "Germany", "wine",
        designation_type="QbA", designation_name="Rheingau",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description=(
            "The Rheingau occupies a unique east-west oriented stretch of the Rhine "
            "where south-facing slopes capture maximum sunshine. Riesling dominates "
            "on quartzite and slate soils, producing wines of greater power and "
            "body than Mosel — more structured, less delicate, but capable of "
            "extraordinary complexity and longevity. Hochheim, Rüdesheim, and the "
            "famous Schloss Johannisberg give the region its prestige."
        ),
        key_producers="Weingut Robert Weil, Schloss Johannisberg, Leitz, Georg Breuer",
        historical_context=(
            "Schloss Johannisberg — reputed birthplace of Spätlese (late harvest) wine "
            "in 1775 — established the Rheingau's historical prestige. Queen Victoria's "
            "fondness for Hochheimer Riesling (Hock) made German wine fashionable in "
            "Victorian Britain. Robert Weil's Kiedrich Gräfenberg is today the region's "
            "most acclaimed estate."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Classic Rheingau year; power and minerality"),
    (2021, "very_good",  "stable",  "Fresh and precise; fine acidity structure"),
    (2020, "very_good",  "stable",  "Rich and ripe; good late harvest potential"),
    (2019, "excellent",  "rising",  "Concentrated and age-worthy; top estates excel"),
    (2018, "very_good",  "stable",  "Powerful vintage; rich and full-bodied"),
]:
    VIN(r2, yr, qd, pt, sn)

p2a = P("Weingut Robert Weil", "winery", r2, "Germany",
        production_philosophy="precision_classic_riesling",
        philosophy_description="Kiedrich specialist; precision viticulture; Gräfenberg is the great Riesling site.",
        reputation_narrative="The Rheingau's most celebrated modern estate; Kiedrich Gräfenberg is iconic.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod2a, new2a = PROD("Robert Weil Kiedrich Gräfenberg Riesling Spätlese Rheingau", "wine_still", p2a, r2, "Germany",
    subcategory="white",
    description="The Rheingau's benchmark Spätlese; off-dry, mineral, structured — great aging potential.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "grilled Rhine salmon with herbs and lemon", "complement", "classic", "main",
         "Rhine fish and Rheingau Riesling — regional tradition")
    PAIR(prod2a, "roasted goose with apple and prune stuffing", "complement", "classic", "main",
         "German Christmas goose and off-dry Riesling")
    PAIR(prod2a, "pork loin with sauerkraut and caraway", "complement", "classic", "main",
         "classic German pairing with regional Riesling")
    PAIR(prod2a, "Münster cheese with caraway seeds", "complement", "classic", "cheese",
         "German-style cheese and regional Riesling")

prod2b, new2b = PROD("Robert Weil Kiedrich Gräfenberg Riesling Auslese Rheingau", "wine_still", p2a, r2, "Germany",
    subcategory="sweet_white",
    description="Gräfenberg Auslese; concentrated, honeyed, with electric acidity and decades of aging.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Stilton with port and walnut", "complement", "established", "cheese",
         "sweet Auslese and blue cheese richness")
    PAIR(prod2b, "peach and ginger crème brûlée", "complement", "established", "dessert",
         "stone fruit and spice echo")
    PAIR(prod2b, "foie gras with Riesling Auslese poaching liquid", "complement", "classic", "starter",
         "wine used in preparation creates echo")
    PAIR(prod2b, "apricot Schmarren (Austrian dessert)", "complement", "classic", "dessert",
         "Central European apricot dessert and sweet Riesling")

p2b = P("Weingut Georg Breuer", "winery", r2, "Germany",
        production_philosophy="dry_riesling_pioneer",
        philosophy_description="Pioneer of dry Rheingau Riesling (Grosses Gewächs); Berg Schlossberg specialist.",
        reputation_narrative="Transformed Rheingau's style; Terra Montosa is the benchmark dry Riesling.",
        price_positioning="premium")
prod2c, new2c = PROD("Breuer Berg Schlossberg Riesling Grosses Gewächs Rheingau", "wine_still", p2b, r2, "Germany",
    subcategory="white",
    description="Dry Grand Cru equivalent from Rüdesheim Berg Schlossberg; mineral, structured, age-worthy.",
    price_tier="ultra_premium")
if new2c:
    PAIR(prod2c, "turbot with beurre blanc and herbs", "complement", "classic", "main",
         "dry GG Riesling and flatfish — elegant German pairing")
    PAIR(prod2c, "lobster with bisque and cream", "complement", "established", "main",
         "powerful dry Riesling and lobster")
    PAIR(prod2c, "asparagus with hollandaise (white asparagus season)", "complement", "classic", "main",
         "German white asparagus and dry Riesling — the national spring pairing")
    PAIR(prod2c, "Comté cheese with walnuts", "complement", "established", "cheese",
         "mineral dry Riesling and aged hard cheese")

prod2d, new2d = PROD("Breuer Rüdesheimer Riesling QbA Rheingau", "wine_still", p2b, r2, "Germany",
    subcategory="white",
    description="Entry Rheingau Riesling from Breuer; dry style, mineral, food-friendly.",
    price_tier="mid_range")
if new2d:
    PAIR(prod2d, "fresh asparagus with butter and herbs", "complement", "classic", "starter",
         "German asparagus and Rheingau Riesling")
    PAIR(prod2d, "grilled trout with lemon and butter", "complement", "classic", "main",
         "Rhine freshwater fish and regional Riesling")
    PAIR(prod2d, "schnitzel with potato salad", "complement", "classic", "main",
         "German classic and regional wine")
    PAIR(prod2d, "creamy scrambled eggs with chives", "complement", "established", "amuse",
         "delicate Riesling and egg preparation")

# ── 3. Pfalz QbA ──────────────────────────────────────────────────────────────
print("=== Pfalz QbA ===")
r3 = R("Pfalz QbA", "Germany", "wine",
        designation_type="QbA", designation_name="Pfalz",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Germany's warmest and most diverse wine region, the Pfalz produces "
            "Riesling of greater body and richness than Mosel or Rheingau, alongside "
            "excellent Spätburgunder (Pinot Noir), Weissburgunder (Pinot Blanc), and "
            "Grauburgunder (Pinot Gris). The Mittelhaardt — with estates like Bassermann-"
            "Jordan, Bürklin-Wolf, and von Buhl — is the prestige zone, while "
            "innovative producers in the Südpfalz are reinventing German wine style."
        ),
        key_producers="Reichsrat von Buhl, Bassermann-Jordan, Bürklin-Wolf, Knipser, Christmann",
        historical_context=(
            "The Pfalz was historically Germany's most productive wine region — German "
            "palates considered Pfalz wines too common and robust. Quality revolution "
            "in the 1980s-90s, led by Müller-Catoir and later Christmann and Knipser, "
            "transformed the region's ambitions. Spätburgunder (Pinot Noir) from the "
            "Mittelhaardt now rivals Burgundy at a fraction of the price."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Pfalz year; Riesling and Pinot Noir both excel"),
    (2021, "very_good",  "stable",  "Fresh and precise; good Spätburgunder year"),
    (2020, "excellent",  "stable",  "Rich and concentrated; great aging potential"),
    (2019, "excellent",  "rising",  "Warm and ripe; top estates made outstanding wines"),
    (2018, "very_good",  "stable",  "Very warm; powerful wines requiring time"),
]:
    VIN(r3, yr, qd, pt, sn)

p3a = P("Weingut A. Christmann", "winery", r3, "Germany",
        production_philosophy="biodynamic_grosses_gewaechs",
        philosophy_description="Biodynamic; pioneer of Grosses Gewächs; president of VDP.",
        reputation_narrative="One of Pfalz's most respected estates; Idig GG is the benchmark dry Riesling.",
        price_positioning="premium",
        authority_tier=1)
prod3a, new3a = PROD("Christmann Gimmeldinger Mandelgarten Riesling Grosses Gewächs Pfalz", "wine_still", p3a, r3, "Germany",
    subcategory="white",
    description="Dry Grand Cru Riesling from sandstone and limestone; rich, textured, mineral.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "grilled white asparagus with hollandaise", "complement", "classic", "main",
         "German white asparagus season and Pfalz Riesling")
    PAIR(prod3a, "roast pork with sauerkraut and Knödel", "complement", "classic", "main",
         "German Sunday roast and regional dry Riesling")
    PAIR(prod3a, "grilled sea bream with lemon and herbs", "complement", "established", "main",
         "textured dry Riesling and Mediterranean fish")
    PAIR(prod3a, "Bergkäse with caraway and crusty bread", "complement", "classic", "cheese",
         "mountain cheese and dry Riesling")

prod3b, new3b = PROD("Christmann Spätburgunder Haus Christmann Pfalz", "wine_still", p3b := None or p3a, r3, "Germany",
    subcategory="red",
    description="Estate Pinot Noir from the Pfalz; silky, earthy, showing Pfalz Spätburgunder character.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "roast duck with cherry and herbs", "complement", "classic", "main",
         "Pfalz Spätburgunder and duck — German take on Pinot Noir")
    PAIR(prod3b, "wild mushroom risotto", "complement", "established", "main",
         "earthy mushroom and silky Pinot")
    PAIR(prod3b, "salmon with Spätburgunder sauce", "complement", "established", "main",
         "salmon and German Pinot Noir")
    PAIR(prod3b, "aged Allgäuer Bergkäse", "complement", "established", "cheese",
         "German mountain cheese and German Pinot")

p3b_new = P("Weingut Knipser", "winery", r3, "Germany",
        production_philosophy="terroir_modern",
        philosophy_description="Quality pioneer; red wine specialist alongside exceptional Riesling.",
        reputation_narrative="Among Pfalz's most dynamic producers; Spätburgunder and Dornfelder benchmarks.",
        price_positioning="premium")
prod3c, new3c = PROD("Knipser Spätburgunder Laumersheim Pfalz", "wine_still", p3b_new, r3, "Germany",
    subcategory="red",
    description="Benchmark Pfalz Spätburgunder; dark cherry, earth, and mineral from limestone terroir.",
    price_tier="premium")
if new3c:
    PAIR(prod3c, "braised venison with juniper and herbs", "complement", "established", "main",
         "game and structured Pfalz Spätburgunder")
    PAIR(prod3c, "grilled beef rib with mushroom sauce", "complement", "established", "main",
         "earthy Pinot and grilled beef")
    PAIR(prod3c, "roast lamb with garlic and rosemary", "complement", "classic", "main",
         "German Pinot Noir and lamb")
    PAIR(prod3c, "aged Münster Géromé cheese", "complement", "established", "cheese",
         "pungent cheese and structured Pinot")

prod3d, new3d = PROD("Knipser Riesling Kallstadter Saumagen Grosses Gewächs Pfalz", "wine_still", p3b_new, r3, "Germany",
    subcategory="white",
    description="Iconic GG from Saumagen ('pig's stomach') site; limestone terroir; powerful and mineral.",
    price_tier="ultra_premium")
if new3d:
    PAIR(prod3d, "Pfalz Saumagen (stuffed pig's stomach — regional dish)", "complement", "classic", "main",
         "wine named after the site; the classic regional pairing")
    PAIR(prod3d, "grilled turbot with capers and butter", "complement", "classic", "main",
         "powerful GG Riesling and flatfish")
    PAIR(prod3d, "lobster with cream and cognac", "complement", "established", "main",
         "powerful Riesling and lobster")
    PAIR(prod3d, "soft pretzels with Obatzda cheese spread", "complement", "classic", "amuse",
         "Bavarian/Pfalz regional snack and local Riesling")

# ── 4. Nahe QbA ───────────────────────────────────────────────────────────────
print("=== Nahe QbA ===")
r4 = R("Nahe QbA", "Germany", "wine",
        designation_type="QbA", designation_name="Nahe",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "The Nahe occupies a transitional zone between the Mosel, Rheingau, and "
            "Rheinhessen, producing Riesling of distinctive character — combining "
            "Mosel delicacy with Rheingau structure and unique volcanic mineral notes "
            "from the diverse slate, quartzite, porphyry, and sandstone geology. "
            "Emrich-Schönleber and Dönnhoff are the region's most celebrated estates, "
            "producing wines that rank among Germany's finest."
        ),
        key_producers="Dönnhoff, Emrich-Schönleber, Schäfer-Fröhlich, Gut Hermannsberg",
        historical_context=(
            "The Nahe was dismissed for centuries as a minor region between the great "
            "Rhine and Mosel valleys. Helmut Dönnhoff's ascent from the 1970s demonstrated "
            "that the Nahe's diverse geology could produce wines of extraordinary complexity. "
            "The VDP Nahe classification, established in the 2000s, gave the region's "
            "best sites formal recognition."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Nahe year; volcanic mineral and electric acidity"),
    (2021, "excellent",  "stable",  "Superb freshness; the mineral character of Nahe shines"),
    (2020, "very_good",  "stable",  "Rich and ripe; excellent across all levels"),
    (2019, "excellent",  "rising",  "Complex and structured; great aging wines"),
    (2018, "very_good",  "stable",  "Warm; riper style but good balance"),
]:
    VIN(r4, yr, qd, pt, sn)

p4a = P("Weingut Dönnhoff", "winery", r4, "Germany",
        production_philosophy="traditional_precision",
        philosophy_description="Meticulous terroir expression; Hermannshöhle and Brücke are the top sites.",
        reputation_narrative="Germany's most universally admired Riesling estate; Hermannshöhle is incomparable.",
        price_positioning="ultra_premium",
        authority_tier=1)
prod4a, new4a = PROD("Dönnhoff Niederhäuser Hermannshöhle Riesling Spätlese Nahe", "wine_still", p4a, r4, "Germany",
    subcategory="white",
    description="Iconic Nahe Spätlese; volcanic slate mineral, red fruit, and extraordinary delicacy.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "pan-fried pike-perch with herb butter", "complement", "classic", "main",
         "Nahe river fish and Nahe Riesling")
    PAIR(prod4a, "cured salmon with dill and lemon", "complement", "classic", "starter",
         "delicate off-dry Riesling and cured fish")
    PAIR(prod4a, "roasted pork belly with red cabbage", "complement", "established", "main",
         "German pork preparation and Nahe Riesling")
    PAIR(prod4a, "taleggio cheese with honey", "complement", "established", "cheese",
         "semi-soft cheese and off-dry Riesling")

prod4b, new4b = PROD("Dönnhoff Kreuznacher Brückes Riesling Grosses Gewächs Nahe", "wine_still", p4a, r4, "Germany",
    subcategory="white",
    description="Dry GG from sandstone Brückes site; structured, minerally precise, age-worthy.",
    price_tier="ultra_premium")
if new4b:
    PAIR(prod4b, "white asparagus with Hollandaise and smoked salmon", "complement", "classic", "main",
         "German asparagus season and dry Nahe GG Riesling")
    PAIR(prod4b, "grilled turbot with herb beurre blanc", "complement", "classic", "main",
         "dry GG Riesling and flatfish")
    PAIR(prod4b, "chicken with Riesling cream sauce", "complement", "classic", "main",
         "wine used in sauce creates echo")
    PAIR(prod4b, "fresh Camembert with honey", "complement", "established", "cheese",
         "mineral dry Riesling and soft-ripened cheese")

p4b = P("Emrich-Schönleber Weingut", "winery", r4, "Germany",
        production_philosophy="low_yield_terroir",
        philosophy_description="Low yields; old-vine Monzingen parcels; Frühlingsplätzchen and Halenberg.",
        reputation_narrative="Nahe's most dynamic estate; Monzingen Halenberg GG is among Germany's finest dry Rieslings.",
        price_positioning="ultra_premium")
prod4c, new4c = PROD("Emrich-Schönleber Monzinger Halenberg Riesling Grosses Gewächs Nahe", "wine_still", p4b, r4, "Germany",
    subcategory="white",
    description="The Nahe's most celebrated GG; blue slate and volcanic mineral of extraordinary depth.",
    price_tier="ultra_premium")
if new4c:
    PAIR(prod4c, "oysters with Nahe Sekt mignonette", "complement", "established", "aperitif",
         "mineral GG Riesling and oyster")
    PAIR(prod4c, "grilled langoustine with citrus herbs", "complement", "established", "main",
         "mineral precision and delicate crustacean")
    PAIR(prod4c, "veal with lemon and capers", "complement", "established", "main",
         "structured dry Riesling and veal")
    PAIR(prod4c, "aged Comté with walnut", "complement", "established", "cheese",
         "mineral Riesling and aged mountain cheese")

prod4d, new4d = PROD("Emrich-Schönleber Riesling Nahe", "wine_still", p4b, r4, "Germany",
    subcategory="white",
    description="Estate Riesling; entry to the Emrich-Schönleber range; fresh, mineral, accessible.",
    price_tier="mid_range")
if new4d:
    PAIR(prod4d, "grilled white fish with lemon butter", "complement", "classic", "main",
         "mineral Riesling and simple fish preparation")
    PAIR(prod4d, "sushi and sashimi selection", "complement", "established", "main",
         "mineral delicacy and Japanese fish")
    PAIR(prod4d, "Thai green curry with coconut", "complement", "established", "main",
         "off-dry mineral and spiced curry bridge")
    PAIR(prod4d, "soft pretzels with mustard", "complement", "classic", "amuse",
         "German tradition with regional wine")

# ── 5. Franken QbA ────────────────────────────────────────────────────────────
print("=== Franken QbA ===")
r5 = R("Franken QbA", "Germany", "wine",
        designation_type="QbA", designation_name="Franken",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description=(
            "Franken (Franconia) is Germany's most distinctive wine region, known for "
            "the unique flat-bottomed Bocksbeutel bottle and Silvaner as the signature "
            "grape. The region's continental climate and diverse soils — Triassic sandstone "
            "in the east, limestone (Muschelkalk) in the west — produce wines of "
            "earthy, mineral character quite unlike any other German region. Dry Silvaner "
            "and Riesling from the Würzburger Stein and Escherndorfer Lump are benchmarks."
        ),
        key_producers="Weingut am Stein, Juliusspital, Bürgerspital, Rudolf Fürst, Horst Sauer",
        historical_context=(
            "Franken's Bocksbeutel (flask bottle) has been protected since the 18th century "
            "— its shape denotes genuinely Franconian wine. Prince Bishop Julius Echter von "
            "Mespelbrunn established Juliusspital in 1576 with winery proceeds funding the "
            "hospital still operating today. Silvaner was historically Germany's most planted "
            "variety before Riesling's dominance."
        ))

for yr, qd, pt, sn in [
    (2022, "excellent",  "rising",  "Outstanding Franken vintage; Silvaner and Riesling both excel"),
    (2021, "very_good",  "stable",  "Fresh and mineral; Silvaner at its best"),
    (2020, "excellent",  "stable",  "Rich and concentrated; earthy Franken character"),
    (2019, "very_good",  "stable",  "Consistent and reliable; good value vintage"),
    (2018, "very_good",  "stable",  "Warm year; powerful wines with good balance"),
]:
    VIN(r5, yr, qd, pt, sn)

p5a = P("Weingut am Stein Würzburg", "winery", r5, "Germany",
        production_philosophy="natural_terroir",
        philosophy_description="Natural Franken wine; old-vine Silvaner from Würzburger Stein; low intervention.",
        reputation_narrative="One of Franken's most dynamic estates; Würzburger Stein GG is the benchmark.",
        price_positioning="premium",
        authority_tier=1)
prod5a, new5a = PROD("Weingut am Stein Würzburger Stein Silvaner Grosses Gewächs Franken", "wine_still", p5a, r5, "Germany",
    subcategory="white",
    description="GG Silvaner from the Stein's limestone; earthy, mineral, dry — redefining Franken Silvaner.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "asparagus with smoked ham and Hollandaise", "complement", "classic", "main",
         "Franken Silvaner and white asparagus — the Würzburg spring tradition")
    PAIR(prod5a, "freshwater carp prepared Franconian style", "complement", "classic", "main",
         "Franken regional fish and Franken wine")
    PAIR(prod5a, "pork roast with Knödel and sauerkraut", "complement", "classic", "main",
         "Franconian Sunday roast and regional Silvaner")
    PAIR(prod5a, "Limburger cheese with caraway bread", "complement", "classic", "cheese",
         "German cheese and Franken Silvaner")

prod5b, new5b = PROD("Weingut am Stein Würzburger Stein Riesling Grosses Gewächs Franken", "wine_still", p5a, r5, "Germany",
    subcategory="white",
    description="GG Riesling from the Stein; more structured and mineral than classic Mosel; age-worthy.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "grilled pike-perch with herb cream", "complement", "classic", "main",
         "Main River fish and Franken Riesling")
    PAIR(prod5b, "steamed white asparagus with brown butter", "complement", "classic", "main",
         "German asparagus and Franken GG Riesling")
    PAIR(prod5b, "chicken with Riesling and cream", "complement", "established", "main",
         "wine used in sauce echoes wine in glass")
    PAIR(prod5b, "Allgäuer Bergkäse with rye bread", "complement", "established", "cheese",
         "mountain cheese and earthy Franken Riesling")

p5b = P("Weingut Horst Sauer", "winery", r5, "Germany",
        production_philosophy="precision_organic",
        philosophy_description="Organic farming; Escherndorfer Lump specialist; Silvaner and Riesling.",
        reputation_narrative="Escherndorfer Lump's most celebrated producer; organic pioneer in Franken.",
        price_positioning="premium")
prod5c, new5c = PROD("Horst Sauer Escherndorfer Lump Silvaner Grosses Gewächs Franken", "wine_still", p5b, r5, "Germany",
    subcategory="white",
    description="GG from the famous Lump ('rascal') site; limestone mineral, earthy, distinctive Silvaner.",
    price_tier="premium")
if new5c:
    PAIR(prod5c, "Franconian asparagus with local ham", "complement", "classic", "main",
         "regional tradition with Lump GG Silvaner")
    PAIR(prod5c, "freshwater carp prepared blue ('Karpfen blau')", "complement", "classic", "main",
         "Franken carp and Franken Silvaner — regional classic")
    PAIR(prod5c, "pumpkin soup with pumpkin seed oil", "complement", "established", "starter",
         "earthy Silvaner and pumpkin")
    PAIR(prod5c, "cold cuts Brotzeit with mustard and bread", "complement", "classic", "amuse",
         "Bavarian/Franken snack tradition")

prod5d, new5d = PROD("Horst Sauer Escherndorfer Lump Riesling Spätlese Franken", "wine_still", p5b, r5, "Germany",
    subcategory="white",
    description="Off-dry Spätlese from Lump; mineral, elegant, fresh — showing Franken Riesling at its best.",
    price_tier="mid_range")
if new5d:
    PAIR(prod5d, "smoked trout with horseradish", "complement", "classic", "starter",
         "Franken smoked fish and regional Riesling")
    PAIR(prod5d, "Thai chicken with lemongrass", "complement", "established", "main",
         "off-dry Riesling and aromatic Asian preparation")
    PAIR(prod5d, "aged Gouda with mustard seeds", "complement", "established", "cheese",
         "mineral Riesling and aged cheese")
    PAIR(prod5d, "apple strudel with vanilla cream", "complement", "classic", "dessert",
         "Central European apple dessert and off-dry Riesling")

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
print("B160 complete.")
cur.close()
conn.close()
