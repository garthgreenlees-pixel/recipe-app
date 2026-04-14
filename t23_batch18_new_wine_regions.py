#!/usr/bin/env python3
"""T23 Batch 18 — New wine regions: Pfalz (Germany), Pantelleria DOC (Italy), Madeira DO (Portugal), Maremma Toscana DOC (Italy), Paso Robles AVA (USA)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
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

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
      (name, country, region_id, producer_type, reputation_narrative, authority_tier)
      VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
      (name, country, region_id, producer_type, description))
    pid = cur.fetchone()[0]
    print(f"  Producer: {name} ({pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── PFALZ (GERMANY) ───────────────────────────────────────────────
print("\n=== Pfalz (Germany) ===")
r_pfa = R("Pfalz", "Germany", "wine",
           designation_type="Qualitätswein",
           designation_name="Pfalz Qualitätswein",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Germany's largest and warmest quality wine region, stretching along the eastern foothills of the Haardt mountains (the northward extension of Alsace's Vosges) in Rhineland-Palatinate. The Pfalz produces exceptional Riesling in both dry and off-dry styles, alongside Germany's finest Spätburgunder (Pinot Noir), Weissburgunder, and Grauburgunder. The Middle Haardt — Deidesheim, Forst, and Ruppertsberg — produces the region's finest Riesling from volcanic basalt and sandstone.",
           key_producers="Müller-Catoir, A. Christmann, Bürklin-Wolf, Friedrich Becker, Knipser",
           historical_context="The Pfalz's wine history began with the Romans who established Neustadt an der Weinstrasse. The region's warm, sheltered climate — the warmest in Germany — allowed full grape ripeness centuries before global warming. Müller-Catoir's revolution in the 1980s under winemaker Hans-Günter Schwarz established that Pfalz Riesling could rival Mosel in aromatic complexity while offering more weight and structure. Friedrich Becker's Pinot Noir from Schweigen on the French border demonstrated Germany's potential for world-class red wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Pfalz vintage; Riesling from Mittelhaardt basalt showed extraordinary aromatic complexity; Spätburgunder of Burgundian elegance."),
    (2021, "very_good", "stable", "Classic vintage; the Haardt foothills produced Riesling of excellent structure and Pinot Noir of fine aromatic character."),
    (2020, "excellent", "stable", "Benchmark year; Bürklin-Wolf and Christmann produced Riesling GG wines of exceptional mineral precision."),
    (2019, "exceptional", "rising", "Greatest Pfalz vintage of the modern era; Spätburgunder from the French border reached international recognition."),
    (2018, "excellent", "stable", "Excellent vintage; the warmth produced Pfalz Riesling of unusual richness; Auslese wines of extraordinary concentration."),
]:
    VIN(r_pfa, yr, qd, pt, sn)

p_mcg = P("Müller-Catoir", "Germany", r_pfa,
           description="The Catoir family's Neustadt estate, transformed by legendary winemaker Hans-Günter Schwarz (1979-2002), is considered the Pfalz's most innovative and internationally influential producer. The Muskateller, Scheurebe, and Riesling wines at every quality level are benchmarks for the region's expressive, aromatic style.")
prod_mcg, new = PROD("Müller-Catoir Haardter Bürgergarten Riesling Spätlese", "wine_still", p_mcg, r_pfa, "Germany",
                     subcategory="Riesling",
                     description="Pfalz Riesling Spätlese at its most expressive — off-dry, aromatic, and complex from volcanic Haardt soils. Peach, apricot, jasmine, ginger, and a mineral finesse that sets this apart from the Mosel's steely style. More weight and generosity than Mosel Spätlese; exceptional food wine and pleasure wine.",
                     price_tier="premium")
if new:
    PAIR(prod_mcg, "Saumagen (stuffed pig stomach with potatoes and spices) — Pfalz speciality", "complement", "classic", "main", "The Pfalz's most traditional dish and its regional Riesling — Spätlese's off-dry richness handles the hearty preparation; peach and apricot notes bridge the pork's richness")
    PAIR(prod_mcg, "Spicy Thai green curry with chicken, coconut milk, and Thai basil", "complement", "established", "main", "German Spätlese's residual sugar and bright acidity is one of the world's great matches for Thai spice; the wine's fruit mirrors the lemongrass; sweetness tempers the chilli")

p_chm = P("A. Christmann", "Germany", r_pfa,
           description="Steffen Christmann's biodynamic Gimmeldingen estate and former president of the VDP association producing benchmark Pfalz Riesling GG from Forster Ungeheuer and Ruppertsberger Reiterpfad. Christmann's dry Grosses Gewächs Rieslings are among Germany's finest and most internationally sought-after.")
prod_chm, new = PROD("Christmann Idig Grosses Gewächs Riesling", "wine_still", p_chm, r_pfa, "Germany",
                     subcategory="Riesling",
                     description="The Pfalz's most acclaimed single-vineyard GG Riesling from the Idig — a grand cru-equivalent volcanic basalt site in Ruppertsberg. Bone dry, intensely mineral, with peach, citrus, white pepper, and the rich textural weight that distinguishes Pfalz from Mosel Riesling. Exceptional aging potential.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_chm, "Grilled Dover sole with caper butter, boiled potatoes, and dill", "complement", "classic", "main", "Pfalz's finest dry Riesling and European flatfish — the wine's mineral precision and citrus character mirrors the delicate sole; caper's brine finds resonance; dill bridges the herbal notes")
    PAIR(prod_chm, "Roasted suckling pig (Spanferkel) with Sauerkraut, bread dumplings, and caraway", "complement", "classic", "main", "Germany's festive dish and Germany's finest dry white — the Riesling's mineral acid cuts through the pork fat; caraway's spice bridges the wine's pepper character")

# ── PANTELLERIA DOC (ITALY) ───────────────────────────────────────
print("\n=== Pantelleria DOC (Italy) ===")
r_pan = R("Pantelleria", "Italy", "wine",
           designation_type="DOC",
           designation_name="Pantelleria DOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Italy's most remote and dramatically volcanic wine island between Sicily and Tunisia, producing the legendary Passito di Pantelleria from sun-dried Zibibbo (Muscat of Alexandria) grapes on ancient basalt volcanic soils. The island's extreme wind requires the alberello pantesco training system where vines are trained into small bushes almost on the ground. Passito di Pantelleria — golden, intensely aromatic, and beautifully balanced between sweetness and acidity — is one of Italy's greatest dessert wines.",
           key_producers="Donnafugata, Pellegrino, Salvatore Murana, De Bartoli, Hibiscus",
           historical_context="Pantelleria's wine tradition dates to the Phoenicians who first planted Zibibbo on the volcanic island. The alberello pantesco training system was developed to protect vines from the fierce Scirocco winds blowing from North Africa. Passito di Pantelleria received DOC status in 1971. The island itself became a UNESCO World Heritage Site in 2014 specifically for its traditional vine cultivation technique. Giorgio Armani maintains a villa on the island, making it a destination for fashion and culture as well as wine.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Pantelleria vintage; Zibibbo grapes achieved perfect concentration for Passito; dry Muscat showed extraordinary aromatic intensity."),
    (2021, "very_good", "stable", "Classic vintage; island conditions were ideal for the sun-drying (appassimento) of Zibibbo grapes."),
    (2020, "excellent", "stable", "Benchmark year; Donnafugata Ben Ryé and Murana Martingana received the highest critical scores of the decade."),
    (2019, "excellent", "rising", "Outstanding vintage; Passito di Pantelleria of extraordinary complexity and balance from all producers."),
    (2018, "very_good", "stable", "Solid vintage; dry Muscat and Passito both showed excellent varietal character from the volcanic basalt."),
]:
    VIN(r_pan, yr, qd, pt, sn)

p_don = P("Donnafugata", "Italy", r_pan,
           description="The Rallo family's Sicilian and Pantelleria estate producing Ben Ryé — one of Italy's most internationally acclaimed and collected dessert wines. Ben Ryé's name means 'son of the wind' in Arabic, referencing the Scirocco that shapes the island's viticulture. The wine consistently receives Italy's highest scores from every major guide.")
prod_don, new = PROD("Donnafugata Ben Ryé Passito di Pantelleria", "wine_still", p_don, r_pan, "Italy",
                     subcategory="Muscat of Alexandria",
                     description="Italy's most celebrated Passito di Pantelleria — sun-dried Zibibbo grapes on volcanic basalt producing extraordinary golden sweetness: apricot jam, orange peel, honey, dried figs, caramelized almonds, and volcanic mineral complexity. Rich but balanced by natural acidity and volcanic freshness. One of Italy's great dessert wines.",
                     price_tier="premium")
if new:
    PAIR(prod_don, "Sicilian cannoli with ricotta, candied orange peel, and pistachio", "complement", "classic", "dessert", "Pantellerian wine and Sicilian pastry — Ben Ryé's orange peel and almond character mirrors the cannoli filling; the wine's sweetness and acidity provide the perfect counterpoint to the crispy shell")
    PAIR(prod_don, "Gorgonzola dolce with acacia honey, toasted walnuts, and pear", "complement", "classic", "cheese", "The wine's apricot and honey sweetness is the ideal partner for blue cheese; walnuts echo the wine's almond character; pear bridges the wine's fruit intensity")

p_mur = P("Salvatore Murana", "Italy", r_pan,
           description="The island's most authentic and passionate Zibibbo producer — Salvatore Murana's single-parcel Passito wines (Martingana, Khamma) are considered Pantelleria's finest and most individual expressions. Murana's wines are more mineral and less opulent than the commercial productions, revealing the volcanic basalt's terroir with startling clarity.")
prod_mur, new = PROD("Murana Martingana Passito di Pantelleria", "wine_still", p_mur, r_pan, "Italy",
                     subcategory="Muscat of Alexandria",
                     description="The most terroir-expressive Passito di Pantelleria from the high-altitude Martingana contrada — more restrained and mineral than Ben Ryé, with greater freshness and volcanic mineral intensity. Dried apricot, fig, volcanic ash, orange blossom, and a long, saline finish unique to this remarkable site.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mur, "Almond semifreddo with Pantellerian capers and sea salt", "complement", "established", "dessert", "Island wine and island almond — the wine's volcanic mineral and apricot character bridges the almond's sweetness; capers add a briny complexity that mirrors the wine's saline finish")
    PAIR(prod_mur, "Foie gras torchon with Sauternes jelly, brioche toast, and fleur de sel", "complement", "established", "starter", "Great sweet wine and foie gras is gastronomy's most celebrated pairing; Murana's mineral version adds volcanic complexity alongside the sweetness that cuts through the fat")

# ── MADEIRA DO (PORTUGAL) ─────────────────────────────────────────
print("\n=== Madeira DO (Portugal) ===")
r_mad = R("Madeira", "Portugal", "wine",
           designation_type="DO",
           designation_name="Madeira DO",
           reputation_tier="iconic",
           quality_trajectory="rediscovering",
           description="Portugal's Atlantic volcanic island producing the world's most long-lived and unique fortified wine — Madeira. The estufagem process (deliberate controlled heating) and the island's perpetual humidity create wines with natural oxidative stability capable of lasting centuries in bottle. Four noble varieties — Sercial (dry), Verdelho (off-dry), Bual (medium sweet), and Malmsey/Malvasia (sweet) — each produce distinctly different styles. A bottle of pre-phylloxera 19th-century Madeira, still alive and complex, is among wine's greatest wonders.",
           key_producers="Barbeito, Blandy's, Henriques & Henriques, Justino's, D'Oliveiras",
           historical_context="Madeira's wine became essential for long sea voyages in the Age of Exploration — the controlled heating mimicked the wine's journey through the tropics in ships' holds, accidentally creating its unique stability. Thomas Jefferson and George Washington were devoted Madeira drinkers; the Declaration of Independence was toasted with Madeira. The phylloxera crisis of the 1850s-1890s devastated the island, replacing noble varieties with the inferior Tinta Negra. The 21st century has seen a renaissance with replanting of noble varieties.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Madeira vintage; single-varietal Sercial and Verdelho from high-altitude volcanic soils showed exceptional aromatic precision."),
    (2021, "very_good", "stable", "Classic vintage; the island's perpetual humidity and volcanic terroir produced wines of excellent natural acidity."),
    (2020, "excellent", "stable", "Benchmark year; Barbeito and Blandy's Colheita bottlings from this year showed extraordinary potential."),
    (2019, "excellent", "rising", "Outstanding vintage; Sercial reached its highest critical recognition in a generation; the dry style's complexity gained major attention."),
    (2018, "very_good", "stable", "Solid vintage; Verdelho and Bual both showed excellent balance between sweetness and the island's natural volcanic acidity."),
]:
    VIN(r_mad, yr, qd, pt, sn)

p_bar = P("Barbeito", "Portugal", r_mad,
           description="The Barbeito family's Funchal lodge producing Madeira of extraordinary mineral precision and freshness — often considered the island's most exciting modern producer. Ricardo Freitas's single-year Colheita wines and old vintage releases demonstrate that Madeira, properly made, is among the world's most distinctive and age-worthy wines.")
prod_bar, new = PROD("Barbeito 10 Year Old Sercial Madeira", "wine_fortified", p_bar, r_mad, "Portugal",
                     subcategory="Sercial",
                     description="Barbeito's benchmark dry Sercial — Madeira's driest style from the island's highest altitude volcanic vineyards. Intense oxidative complexity: hazelnuts, dried citrus, caramelized almonds, tangerine peel, and the piercing volcanic acidity that makes Sercial one of the world's most unique and food-compatible wines.",
                     price_tier="premium")
if new:
    PAIR(prod_bar, "Caldo verde (kale and potato soup with chorizo) as an aperitif pairing", "complement", "classic", "aperitif", "Dry Madeira Sercial has long been served as an aperitif throughout the Lusophone world; the wine's hazelnut and citrus complexity bridges the soup's smoky chorizo")
    PAIR(prod_bar, "Turtle soup (traditional Madeiran) or mushroom consommé with sherry", "complement", "classic", "starter", "Dry Madeira has historically been the classic partner for rich consommés; the wine's nutty oxidative character bridges the concentrated stock's depth")

p_bla = P("Blandy's", "Portugal", r_mad,
           description="The Blandy family's Funchal lodge — the oldest Madeira wine company (1811) — producing the island's most commercially successful and consistently acclaimed range from 5-Year to vintage Single Harvest wines. Blandy's 1920 and other old vintage releases demonstrate Madeira's extraordinary immortality.")
prod_bla, new = PROD("Blandy's 10 Year Old Malmsey Madeira", "wine_fortified", p_bla, r_mad, "Portugal",
                     subcategory="Malmsey",
                     description="Blandy's benchmark sweet Malmsey (Malvasia) — the richest and most approachable of the four noble Madeira styles. Caramel, toffee, dried fig, orange marmalade, and roasted almonds with the volcanic acidity that prevents cloying sweetness. One of the world's great sweet wines for immediate enjoyment.",
                     price_tier="mid_range")
if new:
    PAIR(prod_bla, "Christmas pudding with brandy butter, candied fruit, and toasted almonds", "complement", "classic", "dessert", "Sweet Madeira and rich dried fruit desserts is a centuries-old British tradition; the wine's caramel and almond character mirrors the pudding; volcanic acidity prevents cloyingness")
    PAIR(prod_bla, "Chocolate fondant with salted caramel, vanilla ice cream, and cocoa powder", "complement", "established", "dessert", "The wine's caramelized almond and toffee character bridges the chocolate's bitterness; salted caramel echoes the wine's saline volcanic note; acidity prevents the pairing from being overwhelmingly sweet")

# ── MAREMMA TOSCANA DOC (ITALY) ───────────────────────────────────
print("\n=== Maremma Toscana DOC (Italy) ===")
r_mar = R("Maremma Toscana", "Italy", "wine",
           designation_type="DOC",
           designation_name="Maremma Toscana DOC",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Tuscany's coastal wild frontier extending from Piombino to the Lazio border — once malaria-ridden marshland drained by Mussolini, now one of Italy's most dynamic and exciting wine territories. Bolgheri DOC (home of Sassicaia and Ornellaia) sits within the Maremma and spawned the Super Tuscan revolution. The broader Maremma produces Sangiovese, Cabernet Sauvignon, Merlot, and Syrah from diverse volcanic, clay, and alluvial terroirs in a warmer coastal climate that creates wines of generosity and Mediterranean character.",
           key_producers="Sassicaia (Tenuta San Guido), Ornellaia, Morellino di Scansano, Erik Banti, Poggio Argentiera",
           historical_context="The Maremma was Italy's wildest and least hospitable coastal territory until land reclamation in the 1930s. Mario Incisa della Rocchetta planted Cabernet Sauvignon at Sassicaia in 1944 — initially for personal consumption — based on his love of Bordeaux. When Antinori's Sassicaia was first released commercially in 1968, it created the 'Super Tuscan' category and proved that Italy could produce world-class Cabernet Sauvignon. Bolgheri received its own DOC in 1983 and Sassicaia its own DOCG in 1994.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Maremma vintage; Bolgheri Cabernet Sauvignon showed extraordinary depth; Morellino Sangiovese of excellent Mediterranean richness."),
    (2021, "very_good", "stable", "Classic vintage; the coastal breezes produced wines of excellent freshness; Sassicaia and Ornellaia both excellent."),
    (2020, "excellent", "stable", "Benchmark year; Sassicaia 2020 received the highest scores in a decade from multiple major international critics."),
    (2019, "exceptional", "rising", "Greatest Maremma vintage of the modern era; Super Tuscans of legendary quality from all top estates."),
    (2018, "excellent", "stable", "Excellent vintage; Ornellaia and Le Macchiole produced wines of exceptional balance and age-worthiness."),
]:
    VIN(r_mar, yr, qd, pt, sn)

p_sas = P("Tenuta San Guido", "Italy", r_mar,
           description="Mario Incisa della Rocchetta's legendary Bolgheri estate producing Sassicaia — Italy's most internationally celebrated wine and the progenitor of the Super Tuscan category. The estate's Cabernet Sauvignon-dominated blend, conceived in 1944, revolutionized Italian wine's international standing and proved Italy could produce wines competitive with the finest Bordeaux.")
prod_sas, new = PROD("Sassicaia Bolgheri DOC", "wine_still", p_sas, r_mar, "Italy",
                     subcategory="Cabernet Sauvignon Blend",
                     description="Italy's most iconic and internationally collected wine — Cabernet Sauvignon and Cabernet Franc from the Bolgheri coastal plateaux. Blackcurrant, cedar, tobacco, dark chocolate, Mediterranean garrigue, and the distinctive Bolgheri mineral character. Requires minimum 10 years of aging; develops extraordinary complexity over 30-40 years in bottle.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_sas, "Bistecca alla Fiorentina (T-bone, minimum 1.5kg) with fleur de sel and Tuscan olive oil", "complement", "classic", "main", "Italy's greatest steak and Italy's greatest wine — the bistecca's char and mineral salt finds perfect resonance in Sassicaia's cedar and mineral character; a pairing of national pride")
    PAIR(prod_sas, "Cinghiale (wild boar) slow-braised in Bolgheri wine with juniper and winter vegetables", "complement", "classic", "main", "The Maremma's wild boar and its greatest wine — the wine appears in the braising liquid; juniper mirrors Sassicaia's herbal complexity; the wine's tannins handle the game")

p_poa = P("Poggio Argentiera", "Italy", r_mar,
           description="Gianpaolo Paglia's organic Maremma estate in Capalbio producing benchmark Morellino di Scansano — Sangiovese from the Maremma hills with a coastal, Mediterranean character distinct from Chianti. Finisterre and Bellamarsilia are among the Maremma's finest value-quality ratio wines.")
prod_poa, new = PROD("Poggio Argentiera Morellino di Scansano Riserva", "wine_still", p_poa, r_mar, "Italy",
                     subcategory="Sangiovese",
                     description="Maremma coastal Sangiovese at its most expressive — warm Mediterranean plum, sour cherry, dried herbs, Mediterranean scrub, and a gentle coastal salinity that distinguishes Morellino from inland Chianti. More generous and sunnier in character; excellent food wine of Tuscan warmth.",
                     price_tier="mid_range")
if new:
    PAIR(prod_poa, "Cacciucco alla Livornese (Livorno fish stew) with spiced tomato broth and croutons", "complement", "established", "main", "The Maremma's coastal fish stew tradition and its coastal Sangiovese — the wine's Mediterranean herb and cherry character mirrors the spiced broth; the wine's freshness bridges the seafood richness")
    PAIR(prod_poa, "Porchetta di Ariccia (Roman herb-roasted pork) with rosemary bread and fennel salad", "complement", "classic", "main", "Tuscan coastal Sangiovese and center-Italian herb-roasted pork — the wine's cherry and herb character bridges the fennel and rosemary; the wine's structure handles the rich pork belly")

# ── PASO ROBLES AVA (USA) ─────────────────────────────────────────
print("\n=== Paso Robles AVA (USA) ===")
r_pas = R("Paso Robles", "USA", "wine",
           designation_type="AVA",
           designation_name="Paso Robles AVA",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="California's most dynamic and rapidly evolving wine region in the Central Coast of San Luis Obispo County, producing outstanding Rhône-style wines (Grenache, Syrah, Mourvèdre, Roussanne, Viognier), powerful Zinfandel, and Cabernet Sauvignon from diverse calcareous limestone, clay, and sandy soils. The region's extreme diurnal temperature variation (40°F swings between day and night) creates wines of remarkable freshness despite the warm growing season. The 11 sub-AVAs include the cooler Templeton Gap and the calcareous limestone Willow Creek District.",
           key_producers="Tablas Creek, L'Aventure, Saxum, Booker, Justin",
           historical_context="The Haas family's Tablas Creek (founded 1989 with Château Beaucastel of Châteauneuf-du-Pape) planted Rhône varieties from imported Beaucastel cuttings and established Paso Robles as California's Rhône Ranger capital. Justin Winery's ISOSCELES blend pioneered Bordeaux varietals in the region in the 1980s. Saxum's James Berry Vineyard Grenache blend became Paso's first perfect 100-point wine, establishing the region's world-class credentials.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Paso Robles vintage; Grenache from calcareous limestone showed extraordinary purity; Syrah of Rhône-comparable depth."),
    (2021, "very_good", "stable", "Classic vintage; the extreme diurnal variation produced wines of excellent freshness despite the warm growing conditions."),
    (2020, "excellent", "stable", "Benchmark year; Saxum and Tablas Creek produced the finest Grenache and Roussanne blends of the decade."),
    (2019, "excellent", "rising", "Outstanding vintage; Paso Robles Rhône blends reached their highest critical recognition yet; Zinfandel also excellent."),
    (2018, "very_good", "stable", "Solid vintage; Mourvèdre and Grenache showed excellent varietal character from calcareous limestone sub-AVAs."),
]:
    VIN(r_pas, yr, qd, pt, sn)

p_tab = P("Tablas Creek Vineyard", "USA", r_pas,
           description="The Haas family and Château Beaucastel's joint venture that introduced Rhône varieties from certified Beaucastel cuttings to California. Tablas Creek's Esprit de Tablas — a Mourvèdre, Grenache, Syrah, and Counoise blend in the Châteauneuf-du-Pape tradition — is the American Rhône movement's most important and consistently acclaimed wine.")
prod_tab, new = PROD("Tablas Creek Esprit de Tablas Rouge", "wine_still", p_tab, r_pas, "USA",
                     subcategory="GSM Blend",
                     description="The definitive California Rhône blend — Mourvèdre, Grenache, Syrah, and Counoise from Beaucastel cuttings on Paso's calcareous limestone. Dark cherry, Provençal garrigue, lavender, black olive, and the warm Mediterranean generosity of Châteauneuf-du-Pape translated into Californian terroir. One of the American Rhône movement's finest achievements.",
                     price_tier="premium")
if new:
    PAIR(prod_tab, "Grilled rack of California lamb with herbes de Provence, aioli, and ratatouille", "complement", "classic", "main", "California's Rhône blend and California lamb — the wine's garrigue and lavender character mirrors the Provençal herbs; ratatouille's Mediterranean vegetables bridge both wine and meat")
    PAIR(prod_tab, "Wild mushroom and chorizo paella with saffron and roasted peppers", "complement", "established", "main", "The Mourvèdre and Grenache blend's Mediterranean spice and dark fruit finds perfect resonance in the paella's saffron and chorizo; mushroom adds earthy depth")

p_sax = P("Saxum Vineyards", "USA", r_pas,
           description="Justin Smith's family estate producing Paso Robles' most critically acclaimed and allocated Grenache-based blends from the James Berry Vineyard's ancient calcareous limestone soils. Saxum has received multiple 100-point scores and is considered Paso Robles' reference producer for world-class GSM blends.")
prod_sax, new = PROD("Saxum James Berry Vineyard", "wine_still", p_sax, r_pas, "USA",
                     subcategory="Grenache Blend",
                     description="Paso Robles' most celebrated wine — Grenache, Syrah, and Mourvèdre from the ancient James Berry calcareous limestone vineyard. Dark cherry, blackberry, lavender, mineral limestone, and the Rhône-like complexity that earned Paso Robles its world-class reputation. Received California's first 100-point Paso Robles score. Highly allocated.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_sax, "Slow-roasted prime rib with au jus, horseradish cream, and Yorkshire pudding", "complement", "established", "main", "California's most powerful and complex Grenache blend demands the richest beef preparation; the wine's dark cherry and mineral limestone character handles the richness")
    PAIR(prod_sax, "Lamb merguez with harissa, couscous, and preserved lemon yogurt", "complement", "classic", "main", "The Rhône influence in the wine finds direct resonance with North African spiced lamb; harissa's chilli is tempered by the wine's generous fruit; preserved lemon bridges the mineral note")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
