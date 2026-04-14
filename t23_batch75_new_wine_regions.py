import psycopg2
conn = psycopg2.connect("postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable")
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
    cur.execute("""INSERT INTO beverage_regions
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
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
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, producer_type, region_id, country, production_philosophy,
         philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return (row[0], False)
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return (pid, True)

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 75 ──────────────────────────────────────────────────────────────────
# Regions: Alto Adige, Burgenland, Toro, Nahe, Pfalz

# ── Region 1: Alto Adige ──────────────────────────────────────────────────────
print("\n=== Region 1: Alto Adige ===")
r1 = R("Alto Adige", "Italy", "wine",
    designation_type="DOC",
    designation_name="Alto Adige DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Italy's northernmost and highest wine region (Südtirol in German), producing exceptional Gewürztraminer, Pinot Grigio, Lagrein, Schiava and Pinot Nero from Alpine vineyards between 200–900m altitude.",
    key_producers="Elena Walch, Tramin, Terlano, Tiefenbrunner, Abbazia di Novacella",
    historical_context="Alto Adige is culturally and linguistically German; German grape names (Lagrein, Vernatsch, Blauburgunder) coexist with Italian DOC regulation. The Alpine altitude and diurnal variation produce wines of remarkable aromatic intensity and freshness."
)
VIN(r1, 2022, "excellent", "rising", "Outstanding Alpine vintage; Gewürztraminer of extraordinary aromatic intensity and Lagrein of great depth.")
VIN(r1, 2021, "very_good", "stable", "Balanced mountain season; wines show characteristic purity and aromatic definition.")
VIN(r1, 2020, "good", "stable", "Consistent quality; reliable, expressive wines across all varieties.")
VIN(r1, 2019, "exceptional", "rising", "One of Alto Adige's greatest vintages; wines of Burgundian-level elegance and ageing potential.")
VIN(r1, 2018, "very_good", "stable", "Good overall; Pinot Nero and Lagrein both performed exceptionally well.")

p1a = P("Cantina Tramin", "winery", r1, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Termeno cooperative widely regarded as Italy's greatest Gewürztraminer producer; Nussbaumer Gewürztraminer from the Termeno cru is the world benchmark for the variety.",
    reputation_narrative="Cantina Tramin's Nussbaumer is the most acclaimed Gewürztraminer in the world; the estate defines the variety's potential for complexity, balance and ageing.",
    price_positioning="premium")
prod1a, new1a = PROD("Cantina Tramin Nussbaumer Gewürztraminer", "wine_still", p1a, r1, "Italy",
    subcategory="Gewürztraminer",
    description="The world's benchmark Gewürztraminer: lychee, rose, ginger, clove, mango and a distinctive oily, textured richness; dry, complex and capable of 10+ years of development.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Foie gras torchon with gingerbread and Sauternes jelly", "complement", "classic", "starter", "Rich foie gras and intensely aromatic Gewürztraminer is one of the great Alsace-rooted pairings.")
    PAIR(prod1a, "Massaman curry with coconut milk and roasted peanuts", "complement", "classic", "main", "Gewürztraminer's lychee and spice match the curry's aromatic complexity; sweetness in both aligns.")
    PAIR(prod1a, "Munster cheese with cumin seeds", "complement", "classic", "cheese", "The canonical Alsatian pairing — pungent washed-rind cheese and perfumed Gewürztraminer in striking balance.")
    PAIR(prod1a, "Peking duck pancakes with plum sauce", "complement", "established", "main", "Aromatic duck preparation and the wine's lychee-rose profile are natural companions.")

p1b = P("Cantina Terlano", "winery", r1, "Italy",
    production_philosophy="terroir_expression",
    philosophy_description="Alto Adige's most celebrated cooperative for Pinot Bianco and Chardonnay; the Terlano Primo Grande Cuvée is Italy's most age-worthy white wine, kept in reserve for decades.",
    reputation_narrative="Cantina Terlano regularly releases white wines 20–40 years after harvest; the Terlano Primo Grande Cuvée and Reserva are among Italy's most extraordinary and singular wine experiences.",
    price_positioning="premium")
prod1b, new1b = PROD("Cantina Terlano Pinot Bianco Vorberg Riserva", "wine_still", p1b, r1, "Italy",
    subcategory="Pinot Bianco",
    description="Italy's greatest age-worthy Pinot Bianco from the Vorberg single vineyard — lemon verbena, white peach, almond, mineral chalk and extraordinary tension; can age for decades.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "White asparagus with hollandaise and smoked trout", "complement", "classic", "starter", "South Tyrol's traditional spring pairing — the region's most beloved vegetable with its finest white wine.")
    PAIR(prod1b, "Cured speck ham with sourdough and horseradish cream", "complement", "classic", "starter", "Alto Adige's greatest cured meat with its greatest white wine; horseradish bridges the wine's mineral edge.")
    PAIR(prod1b, "Pan-roasted veal sweetbreads with capers and lemon", "complement", "established", "main", "Rich offal and mineral Pinot Bianco; capers and lemon bridge the wine's acidity and weight.")
    PAIR(prod1b, "Aged Bergkäse mountain cheese with alpine herbs", "complement", "established", "cheese", "Alpine cheese and Alpine white wine in pure terroir harmony.")

# ── Region 2: Burgenland ──────────────────────────────────────────────────────
print("\n=== Region 2: Burgenland ===")
r2 = R("Burgenland", "Austria", "wine",
    designation_type="DAC",
    designation_name="Burgenland DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Eastern Austria's warm lake-influenced wine region on the Hungarian border, famous for Blaufränkisch, Zweigelt and the world-class botrytised dessert wines (Trockenbeerenauslese) of Neusiedlersee.",
    key_producers="Ernst Triebaumer, Weingut Prieler, Moric, Feiler-Artinger, Willi Opitz",
    historical_context="Burgenland joined Austria only in 1921 (previously part of Hungary); the Neusiedlersee lake creates ideal conditions for noble rot, producing some of the world's greatest dessert wines alongside increasingly celebrated Blaufränkisch reds."
)
VIN(r2, 2022, "excellent", "rising", "Outstanding Burgenland vintage; Blaufränkisch of remarkable depth and Trockenbeerenauslese candidates of exceptional concentration.")
VIN(r2, 2021, "very_good", "stable", "Good quality; wines show the lake's warming influence with good fruit concentration.")
VIN(r2, 2020, "excellent", "rising", "Exceptional vintage for both dry reds and botrytised whites; generational TBA conditions.")
VIN(r2, 2019, "very_good", "stable", "Consistent quality; Blaufränkisch of good structure and ageing potential.")
VIN(r2, 2018, "good", "stable", "Reliable year; approachable wines with good typicity across varieties.")

p2a = P("Moric", "winery", r2, "Austria",
    production_philosophy="minimal_intervention",
    philosophy_description="Roland Velich's estate that single-handedly elevated Blaufränkisch to world-class status; Moric's Blaufränkisch from Lutzmannsburg is Austria's most critically acclaimed red wine.",
    reputation_narrative="Moric is considered Austria's greatest red wine producer; the Blaufränkisch Reserve is among Europe's most distinctive and sought-after red wines for its purity and Burgundian restraint.",
    price_positioning="ultra_premium")
prod2a, new2a = PROD("Moric Blaufränkisch Reserve", "wine_still", p2a, r2, "Austria",
    subcategory="Blaufränkisch",
    description="Austria's greatest red wine: wild cherry, blueberry, black pepper, graphite, iron and violets from limestone-clay Burgenland terroir — Burgundian in elegance, utterly Austrian in character.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Roasted Mangalica pork neck with sauerkraut and caraway", "complement", "classic", "main", "The Hungarian heritage pig of Burgenland with its greatest red wine — caraway and pepper in harmony.")
    PAIR(prod2a, "Braised veal cheeks with wild mushroom and dumplings", "complement", "established", "main", "Rich slow-cooked veal and mineral Blaufränkisch; mushroom amplifies the wine's earth and iron.")
    PAIR(prod2a, "Wild boar ragù with egg noodles and game jus", "complement", "established", "main", "Gamey boar and the wine's dark fruit and pepper create an ideal Austrian mountain pairing.")
    PAIR(prod2a, "Aged Bergkäse with mustard and dark rye", "complement", "established", "cheese", "Alpine cheese and structured Blaufränkisch; mustard bridges the wine's pepper and graphite.")

p2b = P("Feiler-Artinger", "winery", r2, "Austria",
    production_philosophy="traditional",
    philosophy_description="Rust-based estate on the Neusiedlersee famous for the world-class Ruster Ausbruch — a unique botrytised wine category between Beerenauslese and Trockenbeerenauslese that has been produced in Rust since the 17th century.",
    reputation_narrative="Feiler-Artinger Ruster Ausbruch is considered the greatest expression of Austria's unique botrytised wine tradition; the estate is Rust's most celebrated.",
    price_positioning="ultra_premium")
prod2b, new2b = PROD("Feiler-Artinger Ruster Ausbruch", "wine_dessert", p2b, r2, "Austria",
    subcategory="Ruster Ausbruch",
    description="Austria's most unique dessert wine: botrytised Welschriesling and Pinot Cuvée from Rust — dried apricot, orange marmalade, honey, saffron and extraordinary acid balance; can age for 50+ years.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Foie gras mi-cuit with brioche and fig compote", "complement", "classic", "starter", "Rich sweet wine and fatty foie gras is the ultimate Sauternes-style pairing; fig bridges the wine's dried fruit.")
    PAIR(prod2b, "Roquefort with walnut honey and pear", "contrast", "classic", "cheese", "Blue cheese's salt and tang are the perfect foil for sweet botrytised wine — a classic contrast.")
    PAIR(prod2b, "Apricot tarte Tatin with crème fraîche", "complement", "classic", "dessert", "The wine's apricot character mirrors the tart; crème fraîche's tartness bridges the sweetness.")
    PAIR(prod2b, "Saffron panna cotta with pistachio and rose", "complement", "established", "dessert", "Saffron in the dessert echoes the wine's complexity; light dairy dessert won't overwhelm its delicacy.")

# ── Region 3: Toro ────────────────────────────────────────────────────────────
print("\n=== Region 3: Toro ===")
r3 = R("Toro", "Spain", "wine",
    designation_type="DO",
    designation_name="Toro DO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Remote Castilian plateau DO on the Duero River west of Valladolid, producing Spain's most powerful and concentrated Tempranillo (Tinta de Toro) from century-old ungrafted bush vines on sandy soils.",
    key_producers="Numanthia, Pintia, Maurodos, Dominio del Bendito, Vetus",
    historical_context="Toro's sandy soils never succumbed to phylloxera, so many vines are ungrafted centenarians; the region's extreme continental climate (hot summers, cold winters) produces Spain's most powerful Tempranillo."
)
VIN(r3, 2021, "excellent", "rising", "Outstanding Toro vintage; Tinta de Toro of exceptional depth and structural balance.")
VIN(r3, 2020, "very_good", "stable", "Good quality; classic Toro profile with powerful fruit and integrated tannins.")
VIN(r3, 2019, "exceptional", "rising", "Benchmark year; old-vine Toro of extraordinary concentration and elegance.")
VIN(r3, 2018, "good", "stable", "Consistent vintage; approachable wines with broad commercial appeal.")
VIN(r3, 2017, "very_good", "stable", "Reliable quality; Tinta de Toro shows its characteristic power and dark fruit.")

p3a = P("Numanthia", "winery", r3, "Spain",
    production_philosophy="terroir_expression",
    philosophy_description="Toro's most celebrated estate (formerly LVMH-owned), producing Termanthia — Spain's highest-scored wine — from ungrafted centenarian Tinta de Toro vines.",
    reputation_narrative="Numanthia's Termanthia scored 100 points from Robert Parker; the estate is Spain's most iconic producer of powerful old-vine Tempranillo.",
    price_positioning="ultra_premium")
prod3a, new3a = PROD("Numanthia Toro", "wine_still", p3a, r3, "Spain",
    subcategory="Tinta de Toro",
    description="Benchmark Toro Tempranillo from ungrafted old vines — dark plum, black cherry, espresso, chocolate, dried herbs and formidable but well-managed tannins; requires 5–10 years of cellaring.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Cochinillo asado (suckling pig roasted in wood oven)", "complement", "classic", "main", "Castilian suckling pig and Toro Tempranillo is the region's most traditional and satisfying pairing.")
    PAIR(prod3a, "Roasted Ibérico pork secreto with black garlic aioli", "complement", "established", "main", "Ibérico pork's rich fat and dark fruit Toro; black garlic bridges the wine's espresso note.")
    PAIR(prod3a, "Braised oxtail with tomato and thyme (rabo de toro)", "complement", "classic", "main", "Classic Castilian braised beef tail with Castile's most powerful red; tomato bridges the wine's acidity.")
    PAIR(prod3a, "Aged Manchego (12 months) with quince membrillo", "complement", "established", "cheese", "Spain's most celebrated cheese with its most powerful region; quince bridges the wine's dark fruit.")

p3b = P("Dominio del Bendito", "winery", r3, "Spain",
    production_philosophy="minimal_intervention",
    philosophy_description="Small artisan estate producing Las Sabias — one of Toro's most elegant and natural Tinta de Toro wines from ancient ungrafted vines, farmed without irrigation or herbicides.",
    reputation_narrative="Dominio del Bendito is Toro's most critically acclaimed natural wine producer; Las Sabias is celebrated for achieving elegance in a region known for power.",
    price_positioning="premium")
prod3b, new3b = PROD("Dominio del Bendito Las Sabias", "wine_still", p3b, r3, "Spain",
    subcategory="Tinta de Toro",
    description="Natural Toro Tempranillo with elegance; wild dark cherry, iron, dried herbs, earth and firm but fine tannins from old ungrafted centenarian vines — power and finesse in balance.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Cordero asado (roast Castilian lamb) with garlic and herbs", "complement", "classic", "main", "Castilian lamb is this wine's natural pairing — both come from the same windswept plateau.")
    PAIR(prod3b, "Morcilla de Burgos (blood sausage) with grilled peppers", "complement", "established", "starter", "Spain's best blood sausage with Spain's most powerful Tempranillo; iron meets iron.")
    PAIR(prod3b, "Wild mushroom and garlic stew on toasted bread", "bridge", "suggested", "starter", "Earthy mushroom bridges the wine's dark fruit and iron; garlic adds aromatic depth.")
    PAIR(prod3b, "Torta del Casar (semi-liquid ewes' milk cheese)", "complement", "adventurous", "cheese", "Extremaduran soft cheese with powerful Castilian red — bold cheese and bold wine in daring balance.")

# ── Region 4: Nahe ────────────────────────────────────────────────────────────
print("\n=== Region 4: Nahe ===")
r4 = R("Nahe", "Germany", "wine",
    designation_type="Anbaugebiet",
    designation_name="Nahe Anbaugebiet",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Small German wine region between the Mosel and Rheinhessen, renowned for Riesling of extraordinary mineral diversity — from blue slate to volcanic porphyry to sandstone — producing wines of remarkable elegance and individuality.",
    key_producers="Dönnhoff, Emrich-Schönleber, Schlossgut Diel, Gut Hermannsberg, Kruger-Rumpf",
    historical_context="The Nahe was little-known until Helmut Dönnhoff's rise to global fame in the 1980s and 90s; now considered Germany's most underrated Riesling region, with Hermannshöhle producing some of Germany's greatest single-vineyard wines."
)
VIN(r4, 2021, "excellent", "rising", "Excellent Nahe vintage; Riesling of remarkable mineral complexity and perfect acid-fruit balance.")
VIN(r4, 2020, "very_good", "stable", "Good quality; elegant, precise wines with great structure for ageing.")
VIN(r4, 2019, "exceptional", "rising", "One of Nahe's greatest vintages; wines of extraordinary depth from Hermannshöhle and Dellchen.")
VIN(r4, 2018, "excellent", "rising", "Outstanding warm year; Spätlese and Auslese of exceptional concentration and balance.")
VIN(r4, 2017, "good", "stable", "Challenging spring but good harvest; wines of good structure and typicity.")

p4a = P("Dönnhoff", "winery", r4, "Germany",
    production_philosophy="terroir_expression",
    philosophy_description="Cornelius Dönnhoff's legendary estate, Germany's most acclaimed Nahe producer; the Hermannshöhle GG and the Niederhäuser Hermannshöhle Auslesen are among Germany's greatest wines.",
    reputation_narrative="Dönnhoff is widely considered one of the five greatest Riesling producers in the world; Hermannshöhle Grosses Gewächs is a global benchmark for German single-vineyard Riesling.",
    price_positioning="ultra_premium")
prod4a, new4a = PROD("Dönnhoff Niederhäuser Hermannshöhle GG Riesling", "wine_still", p4a, r4, "Germany",
    subcategory="Riesling",
    description="One of Germany's greatest Rieslings from volcanic blue slate — slate, white peach, lime zest, crushed stone, apricot and extraordinary tension; dry, profound and can age for 30+ years.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Langoustines with citrus butter and sea herbs", "complement", "classic", "starter", "Germany's greatest Riesling with the finest crustacean; citrus butter echoes the wine's stone fruit and lime.")
    PAIR(prod4a, "Seared turbot with beurre blanc and caviar", "complement", "classic", "fish_course", "Ultra-premium fish and ultra-premium German Riesling; caviar's salt amplifies slate minerality.")
    PAIR(prod4a, "Herb-crusted rack of veal with morel cream", "complement", "established", "main", "Dry GG Riesling has the structure for veal; morel's earthiness bridges wine's mineral and stone fruit.")
    PAIR(prod4a, "Aged Comté with truffle and walnut", "bridge", "established", "cheese", "Nutty aged cheese and mineral Riesling; truffle amplifies the wine's mineral depth.")

p4b = P("Emrich-Schönleber", "winery", r4, "Germany",
    production_philosophy="terroir_expression",
    philosophy_description="Monzingen-based estate producing consistently outstanding Riesling from Frühlingsplätzchen and Halenberg single vineyards — among Germany's most reliable and exciting Nahe producers.",
    reputation_narrative="Emrich-Schönleber Halenberg GG is consistently considered Germany's most underrated great Riesling; the estate produces wines of remarkable precision year after year.",
    price_positioning="premium")
prod4b, new4b = PROD("Emrich-Schönleber Monzingen Halenberg GG", "wine_still", p4b, r4, "Germany",
    subcategory="Riesling",
    description="Sandstone Nahe Riesling of distinctive character — peach, lime, slate, white flowers and a distinctive sandy-mineral finish; dry, precise and underpriced relative to quality.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Trout meunière with lemon, capers and parsley", "complement", "classic", "fish_course", "German freshwater fish and German Riesling is the country's most classic pairing; lemon echoes the wine's citrus.")
    PAIR(prod4b, "Asparagus with new potato and hollandaise (Spargel)", "complement", "classic", "main", "Germany's most beloved spring dish pairs canonically with dry Nahe Riesling.")
    PAIR(prod4b, "Smoked eel with beetroot, crème fraîche and rye", "complement", "established", "starter", "Smoky eel and mineral Riesling; beetroot earthiness bridges the wine's mineral drive.")
    PAIR(prod4b, "Mild goat's cheese with herb oil", "complement", "established", "cheese", "Tangy chèvre aligns with Riesling's acidity; herb oil bridges the wine's stone fruit character.")

# ── Region 5: Pfalz ───────────────────────────────────────────────────────────
print("\n=== Region 5: Pfalz ===")
r5 = R("Pfalz", "Germany", "wine",
    designation_type="Anbaugebiet",
    designation_name="Pfalz Anbaugebiet",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Germany's second-largest wine region and its warmest, producing powerful Riesling, Burgundy-variety reds (Spätburgunder) and unique varieties like Scheurebe and Muskateller along the Haardt mountains.",
    key_producers="Müller-Catoir, A. Christmann, Bürklin-Wolf, Knipser, Friedrich Becker",
    historical_context="The Pfalz (Palatinate) has Germany's most diverse wine production; Forst and Deidesheim produce Riesling of extraordinary richness and depth, while the Mittelhaardt is considered one of Germany's greatest Riesling terroirs."
)
VIN(r5, 2021, "excellent", "rising", "Outstanding Pfalz year; Riesling of exceptional concentration and Spätburgunder of Burgundian elegance.")
VIN(r5, 2020, "very_good", "stable", "Good quality; rich, expressive wines typical of the Pfalz's warm climate.")
VIN(r5, 2019, "exceptional", "rising", "Benchmark Pfalz vintage; wines of extraordinary concentration from the Forst vineyards.")
VIN(r5, 2018, "excellent", "rising", "Very warm year producing powerful, rich wines; Spätlese and Auslese of great intensity.")
VIN(r5, 2017, "very_good", "stable", "Good overall quality; wines show the Pfalz's characteristic warmth and generosity.")

p5a = P("Müller-Catoir", "winery", r5, "Germany",
    production_philosophy="biodynamic",
    philosophy_description="Neustadt-based biodynamic estate producing some of Germany's most distinctive Riesling, Rieslaner and Scheurebe from Haardt mountain vineyards with a unique aromatic intensity.",
    reputation_narrative="Müller-Catoir is among Germany's most celebrated estates for aromatic white variety perfection; the Haardter Bürgergarten Riesling GG is a consistent world-class benchmark.",
    price_positioning="premium")
prod5a, new5a = PROD("Müller-Catoir Haardter Herrenletten Riesling GG", "wine_still", p5a, r5, "Germany",
    subcategory="Riesling",
    description="Biodynamic Pfalz Riesling of great aromatic richness — white peach, lychee, slate, ginger and warm mineral depth; dry and opulent with Pfalz's characteristic generosity.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Saumagen (Pfalz stuffed pork stomach) with sauerkraut", "complement", "classic", "main", "The region's most beloved traditional dish with its most celebrated wine — irreducible local pairing.")
    PAIR(prod5a, "Roasted pork knuckle (Schweinshaxe) with mustard and rye", "complement", "established", "main", "Classic German pork preparation and Pfalz Riesling's richness are natural partners.")
    PAIR(prod5a, "Flammkuchen (Alsatian tarte flambée) with crème fraîche and bacon", "complement", "classic", "casual", "The Pfalz borders Alsace; flammkuchen and Riesling is a cross-border regional classic.")
    PAIR(prod5a, "Munster cheese with caraway", "complement", "established", "cheese", "Pungent washed-rind cheese and rich Riesling is the Alsatian-Pfalz canonical pairing.")

p5b = P("A. Christmann", "winery", r5, "Germany",
    production_philosophy="biodynamic",
    philosophy_description="Gimmeldingen-based estate led by Steffen Christmann (former VDP president), producing some of Germany's greatest biodynamic Riesling GGs from Idig and Reiterpfad vineyards.",
    reputation_narrative="A. Christmann Idig GG is consistently Germany's most acclaimed Pfalz Riesling; the estate's combination of biodynamic farming and Mittelhaardt terroir produces wines of extraordinary depth.",
    price_positioning="ultra_premium")
prod5b, new5b = PROD("A. Christmann Idig GG Riesling", "wine_still", p5b, r5, "Germany",
    subcategory="Riesling",
    description="Germany's most iconic Pfalz single-vineyard Riesling: Idig's ancient red sandstone and basalt produce wines of extraordinary depth — peach, apricot, ginger, mineral smoke and decades of ageing potential.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "Lobster bisque with brandy, cream and tarragon", "complement", "classic", "starter", "Ultra-premium Riesling with ultra-premium shellfish preparation; the wine's depth matches the bisque's richness.")
    PAIR(prod5b, "Roast Brittany langoustines with Riesling butter sauce", "complement", "classic", "fish_course", "A Riesling in the sauce, a Riesling in the glass — the classic French-German crossover pairing.")
    PAIR(prod5b, "Seared duck foie gras with quince and brioche toast", "complement", "established", "starter", "Rich foie and complex dry Riesling; quince bridges the wine's stone fruit and the foie's sweetness.")
    PAIR(prod5b, "Aged Comté (30 months) with truffle salt", "complement", "established", "cheese", "Germany's greatest Riesling with France's greatest mountain cheese — truffle bridges mineral depth.")

# ── Final count ───────────────────────────────────────────────────────────────
cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"\nTotal regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("Done.")
