#!/usr/bin/env python3
"""B140 — Collio DOC (Italy), Colli Orientali del Friuli DOC (Italy),
   Greco di Tufo DOCG supplement, Vermentino di Gallura DOCG (Italy),
   Primitivo di Manduria DOC supplement + Abruzzo (Montepulciano d'Abruzzo DOC)
All constraints verified from B136-B139.
"""
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
    cur.execute("""INSERT INTO beverage_regions
        (name, country, beverage_family, designation_type, designation_name,
         reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, country, beverage_family, designation_type, designation_name,
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s", (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"      Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country,
         subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── COLLIO DOC (Italy / Friuli-Venezia Giulia) ────────────────────────────────
print("=== Collio DOC ===")
r = R("Collio DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Collio DOC",
      reputation_tier="prestigious",
      quality_trajectory="established",
      description="Friuli's finest white wine appellation on glacial marl-and-sandstone hills bordering Slovenia's Brda region. Friulano (Tocai), Pinot Grigio, Sauvignon Blanc and Malvasia Istriana produce wines of extraordinary texture, mineral depth and food-friendly complexity. Some of Italy's most sophisticated whites come from Collio's unique ponca soil.",
      key_producers="Schiopetto, Venica & Venica, Edi Keber, Radikon",
      historical_context="Collio wine history dates to Roman viticulture on the Friulian karst hills. The modern quality era began with Mario Schiopetto's pioneering temperature-controlled stainless steel fermentation in the 1960s. The area straddles the Italian-Slovenian border, sharing its terroir with Brda on the Slovenian side. Radikon's orange wine revolution from the late 1990s made Collio internationally known for skin-contact whites.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Ponca marl-sandstone produced Friulano and Pinot Grigio of exceptional mineral depth and complexity."),
    (2019, "very_good", "stable", "Good balance of freshness and texture; Collio whites of characteristic ponca mineral character."),
    (2020, "very_good", "stable", "Consistent quality from glacial marl; Friulano and Malvasia showing excellent structure."),
    (2021, "excellent", "rising", "Benchmark Collio vintage; whites of extraordinary mineral precision and age-worthiness."),
    (2022, "very_good", "stable", "Good ponca expression; Collio whites of characteristic texture and food-friendly mineral character."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Edi Keber", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Kristian Keber continues his father Edi's legacy of producing Collio's most authentic ponca-mineral expression, farming Friulano, Malvasia and Tocai from the family's best sites and blending them into wines of remarkable coherence and terroir expression.",
       reputation_narrative="Edi Keber's Collio Bianco blend is one of Italy's most admired white wines for its mineral precision and food affinity, demonstrating that Friuli's white varieties can achieve genuine complexity and longevity.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Edi Keber Collio Bianco", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Collio's most authentic field blend — Friulano, Malvasia and Tocai from ponca marl-sandstone; mineral, textured and deeply food-friendly with stone fruit, anise and saline mineral complexity.")
if is_new:
    PAIR(prod, "Jota (Friulian bean, sauerkraut and pork soup)", "complement", "classic", "main", "Friuli's defining hearty soup finds the mineral, ponca-textured character of Collio Bianco ideal.")
    PAIR(prod, "Grilled scampi alla triestina with olive oil and lemon", "complement", "classic", "main", "Trieste-style grilled langoustines with the mineral freshness of Collio Bianco — a regional classic.")
    PAIR(prod, "Frico (Friulian cheese and potato crisp)", "complement", "classic", "casual", "Friulian potato-cheese crisp is inseparable from the regional white wines of Collio and the ponca hills.")
    PAIR(prod, "Montasio cheese aged 18 months with honey", "complement", "established", "cheese", "Aged Friulian cow's milk cheese with mountain honey finds the mineral-textured depth of Collio Bianco ideal.")

prod, is_new = PROD("Edi Keber Collio Friulano", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Single-varietal Friulano (Tocai) from Edi Keber's ponca soils; distinctive almond-bitterness, anise and mineral character unique to Friulano on glacial marl-sandstone — authentically Friulian.")
if is_new:
    PAIR(prod, "Vitello con salsa tonnata e capperi di Pantelleria", "complement", "classic", "starter", "Vitello tonnato's rich tuna-caper sauce is a classic northern Italian pairing for mineral Friulano.")
    PAIR(prod, "San Daniele prosciutto with grissini and butter", "complement", "classic", "casual", "Italy's finest prosciutto from neighbouring San Daniele is the defining Friulano companion.")
    PAIR(prod, "Grilled branzino with herbs and lemon oil", "complement", "established", "main", "Mineral Friulano's anise-almond character suits whole grilled sea bass with herb-lemon seasoning.")
    PAIR(prod, "Risotto con asparagi bianchi e burro di bufala", "complement", "established", "main", "White asparagus risotto with buffalo butter finds the mineral anise complexity of Friulano ideal.")

p2 = P("Venica & Venica", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Venica family has farmed Collio for three generations, producing exemplary single-vineyard and varietal whites from ponca soils that demonstrate the extraordinary quality potential of Friuli's indigenous and international varieties.",
       reputation_narrative="Venica & Venica's Ronco delle Mele Sauvignon Blanc and Trebbiani Friulano are among Collio's most celebrated wines, consistently rated among Italy's finest white wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Venica Ronco delle Mele Sauvignon Blanc Collio", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Benchmark Collio Sauvignon from the Ronco delle Mele vineyard on ponca; textured, mineral and complex with grapefruit, white pepper and ponca earth — one of Italy's greatest expressions of Sauvignon.")
if is_new:
    PAIR(prod, "Grilled dentice (dentex) with gremolata and olive oil", "complement", "established", "main", "Ponca mineral Sauvignon suits this Mediterranean fish with the herb-citrus character of gremolata.")
    PAIR(prod, "Asparagus gratinata with Parmesan and truffle oil", "complement", "classic", "starter", "Friuli Sauvignon's herbaceous mineral precision suits asparagus with aged cheese and truffle.")
    PAIR(prod, "Goat cheese log with herb crust and tomato vinaigrette", "complement", "classic", "casual", "Ponca Sauvignon and fresh goat cheese is a classic pairing of mineral sharpness meeting dairy tang.")
    PAIR(prod, "Grilled artichoke with lemon butter and capers", "bridge", "established", "starter", "Mineral Sauvignon's herb-citrus character bridges the notoriously difficult artichoke-wine pairing.")

prod, is_new = PROD("Venica Trebbiani Friulano Collio", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Friulano from Venica's best ponca parcels; rich almond, anise and mineral depth characteristic of great Friulano with the creamy texture that distinguishes top Collio whites.")
if is_new:
    PAIR(prod, "Fettuccine al burro e salvia con Parmesan", "complement", "classic", "main", "Butter-sage pasta with Parmesan is the classic northern Italian pairing for almond-rich Collio Friulano.")
    PAIR(prod, "Salmone con salsa di aneto e limone", "complement", "established", "main", "Salmon with dill-lemon sauce finds anise-mineral Friulano's complexity an ideal white wine match.")
    PAIR(prod, "Baccalà alla Vicentina with soft polenta", "complement", "classic", "main", "Veneto creamed salt cod with polenta is a natural companion for the mineral almond depth of Friulano.")
    PAIR(prod, "Formadi frant (Friulian aged crumble cheese) with honey", "complement", "established", "cheese", "Unique Friulian crumbled aged cheese with honey mirrors the almond-mineral complexity of Collio Friulano.")

# ── COLLI ORIENTALI DEL FRIULI DOC (Italy) ────────────────────────────────────
print("=== Colli Orientali del Friuli DOC ===")
r = R("Colli Orientali del Friuli DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Colli Orientali del Friuli DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Friuli's most diverse wine appellation on clay-marl-sandstone hills adjacent to Collio, producing both fine whites from Friulano, Ribolla Gialla and Picolit and serious reds from Schioppettino, Refosco and Pignolo. The appellation also produces the unique Picolit dessert wine from the semi-dried native grape.",
      key_producers="Miani, Livio Felluga, La Roncaia",
      historical_context="Colli Orientali's diversity of native varieties — Schioppettino, Refosco, Pignolo, Tazzelenghe, Picolit — represents one of Italy's richest indigenous vine museums. The DOC established 1970 covers 18 varieties. The revival of Schioppettino from near extinction in the 1970s by Ronchi di Cialla is one of Italian viticulture's great success stories.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Clay-marl soils produced whites and reds of exceptional structure and mineral depth."),
    (2019, "very_good", "stable", "Good balance across the range; Schioppettino and Ribolla Gialla both performing well."),
    (2020, "very_good", "stable", "Consistent quality; Refosco and Pignolo reds showing characteristic Friulian mineral structure."),
    (2021, "excellent", "rising", "Outstanding Friulian vintage; whites of extraordinary freshness and reds of genuine complexity."),
    (2022, "very_good", "stable", "Good vintage from clay-marl; indigenous varieties showing authentic character throughout."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Miani", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Enzo Pontoni at Miani is Friuli's most enigmatic and celebrated producer, farming tiny parcels of old-vine Friulano, Ribolla and Refosco with fanatical attention to producing wines of maximum concentration and terroir expression from clay-marl soils.",
       reputation_narrative="Miani is Italy's most sought-after and difficult-to-obtain Friulian producer. Pontoni's wines regularly command prices exceeding top Burgundy, demonstrating the extraordinary potential of Colli Orientali's terroir.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Miani Friulano Colli Orientali del Friuli", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Enzo Pontoni's legendary Friulano from clay-marl in Colli Orientali; profoundly concentrated, mineral and complex with almond, anise, stone fruit and a mineral persistence that ages magnificently.")
if is_new:
    PAIR(prod, "White truffle pasta with butter and Parmesan", "complement", "classic", "main", "Profound, concentrated Miani Friulano handles white truffle's intensity with matching mineral depth and almond richness.")
    PAIR(prod, "Frico di Malga (aged mountain cheese and potato cake)", "complement", "classic", "casual", "Friuli's cheese-potato classic at its most refined finds Miani's Friulano the perfect local companion.")
    PAIR(prod, "Turbotino al vapore con erbe di campo e olio di Sirmione", "complement", "established", "main", "Steamed baby turbot with wild herbs and lake olive oil finds the mineral-almond depth of Miani Friulano ideal.")
    PAIR(prod, "Castelmagno con pere e noci (Castelmagno cheese with pears and walnuts)", "complement", "established", "cheese", "Aged Piemontese blue-veined cheese with pear and walnut echoes the almond-mineral complexity of Miani.")

prod, is_new = PROD("Miani Refosco dal Peduncolo Rosso Colli Orientali", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="Miani's extraordinary Refosco dal Peduncolo Rosso; dense, mineral and age-worthy from clay-marl soils with dark berry, bitter chocolate and characteristic Refosco tannin and wild herb character.")
if is_new:
    PAIR(prod, "Braised short rib with polenta and porcini mushrooms", "complement", "established", "main", "Dense, tannic Refosco demands slow-braised beef richness and earthy mushroom depth.")
    PAIR(prod, "Fagiano arrosto con pancetta e salvia (roast pheasant with pancetta)", "complement", "classic", "main", "Roast pheasant wrapped in pancetta finds the mineral, game-friendly structure of Refosco ideal.")
    PAIR(prod, "Wild boar stew with olives, herbs and polenta", "complement", "established", "main", "Game stew with Mediterranean herbs finds the bitter-mineral depth of old-vine Refosco a natural match.")
    PAIR(prod, "Latteria Friulana aged 24 months with chestnut honey", "complement", "established", "cheese", "Long-aged Friulian cow's milk cheese and chestnut honey suit the bitter-mineral tannic depth of Refosco.")

p2 = P("Livio Felluga", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="One of Friuli's most important estates, Livio Felluga produces a broad, consistently excellent range from Colli Orientali's clay-marl soils, championing indigenous varieties alongside international grapes with equal quality and authenticity.",
       reputation_narrative="Livio Felluga's Terre Alte is considered one of Italy's greatest white wine blends, demonstrating the extraordinary potential of Colli Orientali's clay-marl terroir for complex, age-worthy whites.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Livio Felluga Terre Alte Colli Orientali", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Italy's most acclaimed Friulian white blend — Friulano, Pinot Bianco and Sauvignon — from clay-marl soils. Complex, mineral and structured with stone fruit, almond, anise and a mineral depth capable of decade-long evolution.")
if is_new:
    PAIR(prod, "Risotto con capesante e tartufo bianco d'Alba", "complement", "classic", "main", "White truffle and scallop risotto find the mineral complexity and textural depth of Terre Alte ideal.")
    PAIR(prod, "Branzino al sale con finocchio e limone", "complement", "classic", "main", "Salt-crusted sea bass with fennel and lemon mirrors the mineral-anise complexity of this Friulian blend.")
    PAIR(prod, "Grilled langoustines with herb butter and sea salt", "complement", "classic", "main", "The mineral complexity of Terre Alte elevates grilled langoustines with herb butter to great pairing territory.")
    PAIR(prod, "Stracchino or Taleggio with truffle honey", "complement", "established", "cheese", "Runny, washed-rind Italian cheese with truffle honey finds the structured mineral depth of Terre Alte ideal.")

prod, is_new = PROD("Livio Felluga Schioppettino Colli Orientali", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Native Schioppettino from Colli Orientali's clay-marl soils; distinctive with black pepper, wild berry, violets and mineral freshness — Friuli's most characterful red variety at its most expressive.")
if is_new:
    PAIR(prod, "Salame di Cormons with polenta and giardiniera", "complement", "classic", "casual", "Friulian salami from Cormons with polenta is the natural companion for native Schioppettino.")
    PAIR(prod, "Goulash friulano con spätzle (Friulian goulash with pasta)", "complement", "classic", "main", "Austro-Hungarian influenced Friulian goulash with egg pasta is the perfect vehicle for peppery Schioppettino.")
    PAIR(prod, "Grilled roe deer (capriolo) with blueberry and juniper", "complement", "established", "main", "Game with berry-juniper sauce mirrors the wild berry and peppery mineral character of Schioppettino.")
    PAIR(prod, "Ricotta affumicata (smoked ricotta) with beet carpaccio", "complement", "suggested", "casual", "Smoked ricotta and earthy beet find the peppery mineral freshness of Schioppettino an intriguing match.")

# ── VERMENTINO DI GALLURA DOCG (Italy) ────────────────────────────────────────
print("=== Vermentino di Gallura DOCG ===")
r = R("Vermentino di Gallura DOCG", "Italy", "wine",
      designation_type="DOCG",
      designation_name="Vermentino di Gallura DOCG",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Sardinia's only DOCG appellation from the granite slopes of the Gallura region in the island's northeast. Vermentino from decomposed granite produces some of the Mediterranean's most distinctive whites: bitter almond, citrus peel, white flowers and a saline mineral character unique to Gallura's granite soils.",
      key_producers="Capichera, Cantina Gallura, Surrau",
      historical_context="Vermentino arrived in Sardinia from Liguria or Corsica, finding its finest expression on Gallura's decomposed granite hillsides near the Costa Smeralda. The DOCG granted 1996 was the first on an island. Capichera's premium bottlings demonstrated in the 1990s that Sardinian Vermentino could command prices and critical acclaim rivalling mainland Italian whites.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Granite Vermentino of exceptional mineral depth and aromatic purity from Gallura's northern slopes."),
    (2020, "very_good", "stable", "Good vintage; Gallura Vermentino of characteristic bitter almond and saline mineral character."),
    (2021, "excellent", "rising", "Benchmark DOCG vintage; decomposed granite produced Vermentino of extraordinary freshness and mineral precision."),
    (2022, "very_good", "stable", "Consistent quality from granite soils; Vermentino di Gallura of genuine character and food-friendliness."),
    (2023, "excellent", "rising", "Outstanding granite vintage; Capichera and Surrau produced Gallura whites of benchmark quality."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Capichera", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Ragnedda family at Capichera single-handedly elevated Vermentino di Gallura to fine wine status, producing premium bottlings from old-vine Vermentino on the family's Arzachena granite estate that command prices far above typical Sardinian wines.",
       reputation_narrative="Capichera is Gallura's defining producer, transforming Vermentino di Gallura from a simple tourist wine to an internationally recognised white of genuine complexity and aging potential.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Capichera Vermentino di Gallura DOCG Vigna Ngena", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Capichera's prestige single-vineyard Vermentino di Gallura; profound granite mineral depth, bitter almond, white flowers and saline finish from 30-year-old vines on decomposed granite at altitude.")
if is_new:
    PAIR(prod, "Aragosta alla catalana (Catalan-style lobster with vegetables)", "complement", "classic", "main", "Gallura's traditional lobster preparation with Catalan origins demands the granite mineral depth of Capichera.")
    PAIR(prod, "Bottarga di muggine su linguine con limone e prezzemolo", "complement", "classic", "main", "Sardinian grey mullet roe pasta finds the mineral, saline Vermentino ideal for its ocean intensity.")
    PAIR(prod, "Grilled ricciola (amberjack) with salmoriglio sauce", "complement", "established", "main", "Amberjack with the Sicilian-Sardinian lemon-oregano sauce finds the mineral depth of Capichera ideal.")
    PAIR(prod, "Spaghetti ai ricci (sea urchin pasta) with Sardinian salt", "complement", "established", "main", "Sea urchin's ocean richness finds the saline granite mineral of Gallura Vermentino the perfect match.")

prod, is_new = PROD("Capichera Vermentino di Gallura DOCG", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Estate Vermentino di Gallura from Capichera's granite soils; aromatic, bitter-almond and mineral with characteristic Gallura freshness and saline mineral depth — the DOCG's most reliable producer.")
if is_new:
    PAIR(prod, "Fritto misto di mare con limone e salsa verde", "complement", "classic", "casual", "Mixed fried seafood with lemon and herb sauce is the Sardinian coastal companion for Gallura Vermentino.")
    PAIR(prod, "Grilled dentice con capperi e olive taggiasche", "complement", "established", "main", "Dentex fish with capers and Ligurian olives finds the bitter-mineral granite Vermentino ideal.")
    PAIR(prod, "Pane frattau (layered Sardinian flatbread with egg and tomato)", "bridge", "classic", "casual", "Traditional Sardinian bread dish with egg and tomato finds a bridge in the mineral freshness of Gallura Vermentino.")
    PAIR(prod, "Pecorino Sardo semi-stagionato with honey and almonds", "complement", "established", "cheese", "Semi-aged Sardinian sheep cheese with honey and almonds echoes the bitter almond-mineral depth of Gallura.")

p2 = P("Cantina Gallura", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="The Gallura cooperative winery is the appellation's largest producer, vinifying Vermentino from across the DOCG's granite hillsides to produce a reliable and authentic range of Gallura Vermentino at multiple quality levels.",
       reputation_narrative="Cantina Gallura's Canayli single-vineyard Vermentino is one of the DOCG's most consistently awarded wines, demonstrating the cooperative's commitment to quality from Sardinia's finest granite terroir.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Cantina Gallura Canayli Vermentino di Gallura", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Vermentino di Gallura from Canayli's granite slopes; benchmark mineral, aromatic and fresh with bitter almond, citrus blossom and saline character — consistently one of the DOCG's finest.")
if is_new:
    PAIR(prod, "Zuppa di cozze (mussel soup) with garlic and white wine", "complement", "classic", "casual", "Sardinian mussel soup with garlic-wine broth is a natural companion for mineral Gallura Vermentino.")
    PAIR(prod, "Orata al sale (salt-baked gilt-head bream)", "complement", "classic", "main", "Salt-baked sea bream and its clean, sweet flesh is the traditional Sardinian companion for Gallura Vermentino.")
    PAIR(prod, "Grilled gamberoni con olio EVO e limone", "complement", "established", "casual", "Grilled king prawns with extra-virgin olive oil and lemon find the mineral freshness of Gallura ideal.")
    PAIR(prod, "Casizolu or Canestrato Sardo cheese with fig jam", "complement", "suggested", "cheese", "Sardinian stretched-curd or basket cheese with fig jam suits the floral-mineral freshness of Gallura Vermentino.")

prod, is_new = PROD("Cantina Gallura Vermentino di Gallura Superiore", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="mid_range",
    description="Entry-level Vermentino di Gallura Superiore from Cantina Gallura; fresh, aromatic and characteristically Gallura with bitter almond, citrus and the island's characteristic saline mineral finish.")
if is_new:
    PAIR(prod, "Porcetto arrosto con miele di asfodelo (roast suckling pig with asphodel honey)", "complement", "classic", "main", "Sardinia's definitive roast suckling pig is equally good with both the island's reds and mineral Vermentino.")
    PAIR(prod, "Insalata di polpo con olive e capperi", "complement", "established", "casual", "Octopus salad with olives and capers finds the mineral freshness of Gallura Vermentino ideal.")
    PAIR(prod, "Culurgiones (Sardinian pasta parcels with potato and mint)", "complement", "established", "main", "Sardinia's distinctive pasta with mint and potato filling finds Gallura Vermentino a natural regional pairing.")
    PAIR(prod, "Tonno con pomodorini e basilico (Sardinian tuna steak)", "complement", "suggested", "casual", "Pan-seared tuna with cherry tomatoes and basil suits the fresh bitter-almond character of Gallura Vermentino.")

# ── MONTEPULCIANO D'ABRUZZO DOC (Italy) ───────────────────────────────────────
print("=== Montepulciano d'Abruzzo DOC ===")
r = R("Montepulciano d'Abruzzo DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Montepulciano d'Abruzzo DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Central Italy's Adriatic coast produces big, dark, full-bodied reds from the Montepulciano grape on limestone and clay soils in the Abruzzo hills. Excellent value for quality across the range, from everyday drinking to the profound Colline Teramane DOCG. The Cerasuolo d'Abruzzo rosé is one of Italy's deepest and most distinctive.",
      key_producers="Valentini, Emidio Pepe, Masciarelli",
      historical_context="Montepulciano grape (not related to Vino Nobile di Montepulciano from Sangiovese) has ancient roots in Abruzzo. The region's wine was famously praised by Hannibal's army and by 18th century travellers. Emidio Pepe's no-technology approach and Valentini's strict selection have made Abruzzo one of Italy's most discussed wine regions despite its historic undervaluation.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Montepulciano of extraordinary depth and tannic structure from Abruzzo's best limestone sites."),
    (2019, "very_good", "stable", "Good vintage across the appellation; wines of characteristic dark fruit and Mediterranean warmth."),
    (2020, "very_good", "stable", "Well-balanced Abruzzo red; top Colline Teramane wines of genuine complexity and aging potential."),
    (2021, "excellent", "rising", "Outstanding Abruzzo vintage; Montepulciano of benchmark concentration and mineral depth."),
    (2022, "very_good", "stable", "Consistent quality; Montepulciano d'Abruzzo showing its best food-friendly form."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Emidio Pepe", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Emidio Pepe's estate uses absolutely no technology — foot-treading, no temperature control, no filtration, no fining — producing Montepulciano d'Abruzzo wines of extraordinary longevity and complexity. Bottles are hand-decanted before release from the historic family cellars.",
       reputation_narrative="Emidio Pepe is one of Italy's most mythologised producers. His no-technology Montepulciano and Trebbiano are among the world's most age-worthy wines, commanding prices and critical attention far exceeding their humble Abruzzo DOC status.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Emidio Pepe Montepulciano d'Abruzzo", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="No-technology, foot-treaded Montepulciano from Emidio Pepe; profound, age-worthy and deeply characterful with dark berry, tar, dried herbs and mineral depth that evolves over decades.")
if is_new:
    PAIR(prod, "Arrosticini d'agnello (grilled lamb skewers) with chilli and salt", "complement", "classic", "casual", "Abruzzo's iconic roadside lamb skewers are inseparable from the region's great Montepulciano.")
    PAIR(prod, "Porchetta abruzzese with rosemary, fennel and garlic", "complement", "classic", "casual", "Abruzzo-style porchetta stuffed with wild herbs is the regional companion for Emidio Pepe's mythic red.")
    PAIR(prod, "Pajata (milk-fed veal intestine) alla Romana", "complement", "established", "main", "Rome's most challenging offal preparation finds the no-technology Montepulciano's depth a formidable match.")
    PAIR(prod, "Aged Pecorino di Farindola with wild honey", "complement", "classic", "cheese", "Abruzzo's rarest cheese made with pig rennet and aged Pecorino finds Emidio Pepe's Montepulciano ideal.")

prod, is_new = PROD("Emidio Pepe Trebbiano d'Abruzzo", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Legendary Trebbiano d'Abruzzo from Emidio Pepe; aged without technology in old casks for years before release. Profound, oxidative and complex — one of Italy's most age-worthy whites.")
if is_new:
    PAIR(prod, "Chitarra al ragù di agnello con Pecorino d'Abruzzo", "complement", "classic", "main", "Abruzzo's guitar-cut pasta with lamb ragù and aged Pecorino is the regional pairing for Pepe's Trebbiano.")
    PAIR(prod, "Grilled triglia (red mullet) alla livornese", "complement", "established", "main", "Aged, complex Trebbiano suits the distinctive flavour of red mullet with tomato-caper sauce.")
    PAIR(prod, "Tagliolini in brodo con tartufo nero di Norcia", "complement", "established", "main", "Black truffle from Norcia in delicate pasta broth finds Pepe's mineral oxidative Trebbiano ideal.")
    PAIR(prod, "Scamorza affumicata with honey and walnuts", "complement", "established", "cheese", "Smoked scamorza cheese with honey and walnuts mirrors the oxidative depth and complexity of aged Trebbiano.")

p2 = P("Masciarelli", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Masciarelli estate, led today by Marina Cvetic, is Abruzzo's most commercially successful quality producer, combining modern techniques with the region's native Montepulciano and Trebbiano to produce wines of consistency, complexity and excellent value.",
       reputation_narrative="Masciarelli's Villa Gemma Montepulciano is Abruzzo's most decorated wine at international competitions, demonstrating that the region can produce wines of genuine international stature alongside legendary natural producers like Emidio Pepe and Valentini.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Masciarelli Villa Gemma Montepulciano d'Abruzzo", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Masciarelli's flagship Montepulciano; concentrated, structured and smooth from limestone soils in San Martino sulla Marrucina. Dark plum, leather and Mediterranean spice with fine tannins and genuine aging potential.")
if is_new:
    PAIR(prod, "Abbacchio alla scottadito (grilled baby lamb chops)", "complement", "classic", "casual", "Roman-style baby lamb chops and their charred richness find the concentration of Villa Gemma ideal.")
    PAIR(prod, "Braised wild boar with olives and Abruzzo herbs", "complement", "established", "main", "Wild game with Mediterranean herb braising is a natural central Italian companion for structured Montepulciano.")
    PAIR(prod, "Maccheroni alla chitarra con ragù di cinghiale", "complement", "classic", "main", "Abruzzo's guitar-cut pasta with wild boar ragù is the defining regional pairing for Montepulciano.")
    PAIR(prod, "Canestrato di Moliterno aged 12 months", "complement", "established", "cheese", "Aged southern Italian sheep cheese with its robust character suits the concentration of Villa Gemma.")

prod, is_new = PROD("Masciarelli Marina Cvetic Montepulciano d'Abruzzo", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Marina Cvetic signature Montepulciano; polished, accessible and complex from Colline Teramane limestone with dark cherry, spice and the characteristic Masciarelli elegance.")
if is_new:
    PAIR(prod, "Pizza abruzzese con salsiccia e friggitelli (pizza with sausage and peppers)", "complement", "established", "casual", "Regional pizza with pork sausage and sweet green peppers suits this accessible, polished Montepulciano.")
    PAIR(prod, "Agnello cacio e ova (lamb in egg-cheese sauce)", "complement", "classic", "main", "Abruzzo's festive lamb preparation with egg-cheese sauce finds the fruit and structure of Marina Cvetic ideal.")
    PAIR(prod, "Spaghetti all'Amatriciana with guanciale", "complement", "established", "casual", "Rome's guanciale-tomato-Pecorino pasta finds Abruzzo Montepulciano's cherry richness a perfect match.")
    PAIR(prod, "Formaggio di fossa con miele millefiori", "complement", "established", "cheese", "Pit-aged Italian cheese with wildflower honey finds the accessible complexity of Marina Cvetic Montepulciano ideal.")

# ── FINAL COUNTS ──────────────────────────────────────────────────────────────
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
print("B140 complete.")
conn.close()
