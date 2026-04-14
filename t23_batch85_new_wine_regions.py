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
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, producer_id, region_id, origin_country, subcategory, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    # pairing_type: complement, contrast, bridge, cleanse, elevate
    # confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Languedoc ──────────────────────────────────────────────────────
print("\n=== Region 1: Languedoc ===")
r1 = R("Languedoc", "France", "wine",
    designation_type="AOC",
    designation_name="Languedoc AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's largest wine-producing region stretching from the Rhône delta to the Spanish border, encompassing the vast Hérault, Aude, and Gard departments. Historically a bulk wine sea, the Languedoc has undergone a radical quality transformation driven by international investors and a generation of terroir-focused estates. Today it produces some of France's most exciting wines from indigenous varieties and classic Mediterranean grapes in a multitude of sub-appellations.",
    key_producers="Mas de Daumas Gassac, Domaine de la Grange des Pères, Prieuré Saint-Jean de Bébian, Peyre Rose",
    historical_context="The Languedoc was France's primary wine factory through the 19th and 20th centuries — it supplied cheap bulk wine to northern France and fuelled the industrial revolution; the arrival of Aimé Guibert at Mas de Daumas Gassac in 1970 sparked the quality renaissance.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Mas de Daumas Gassac", "winery", r1, "France",
    production_philosophy="terroir_focused",
    philosophy_description="The 'Grand Cru of the Languedoc' — Aimé Guibert planted Cabernet Sauvignon on cool red glacial soils of the Aniane valley in 1972, producing a wine that challenged Bordeaux in quality. The Blanc made from multiple rare varieties is equally celebrated.",
    reputation_narrative="The founding estate of Languedoc's quality renaissance; consistently rated among France's greatest non-AOC wines.",
    price_positioning="premium")

prod1b_id = P("Domaine de la Grange des Pères", "winery", r1, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Laurent Vaillé's tiny domaine near Aniane produces microscopic quantities of exceptional red and white — Syrah, Mourvèdre, and Cabernet blend with remarkable precision and aging potential from volcanic basalt soils.",
    reputation_narrative="Among France's most cult wines; the red is considered a reference for Mediterranean Syrah-based blends.",
    price_positioning="ultra_premium")

prod1a, new1a = PROD("Mas de Daumas Gassac Rouge", "wine_still", prod1a_id, r1, "France",
    subcategory="Cabernet Sauvignon Blend",
    description="The original Languedoc grand vin — Cabernet Sauvignon-dominant with Syrah and rare Mediterranean varieties, aged in large Burgundy barrels on cool glacial soils. Powerful, complex, and age-worthy, challenging Bordeaux at its own game.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Slow-roasted saddle of lamb with olive tapenade and rosemary", "complement", "classic", "main",
         "Languedoc's signature dish — lamb with garrigues herbs meets a structured Cabernet-dominant Midi blend.")
    PAIR(prod1a, "Wild boar daube with root vegetables and orange peel", "complement", "established", "main",
         "Southern French game stew with an equally robust, complex regional red — both are built for cold evenings.")
    PAIR(prod1a, "Grilled côte de boeuf with anchovy butter and bone jus", "complement", "established", "main",
         "Cabernet's structure handles aged beef while anchovy adds umami depth echoing the wine's complexity.")
    PAIR(prod1a, "Pérail sheep's cheese with thyme honey", "complement", "established", "cheese",
         "Regional sheep's cheese from the Causses with local thyme honey bridges the wine's herbal complexity.")

prod1b, new1b = PROD("Grange des Pères Rouge", "wine_still", prod1b_id, r1, "France",
    subcategory="Syrah-Mourvèdre Blend",
    description="One of France's most allocated and sought-after wines — a Syrah, Mourvèdre, and Cabernet Sauvignon blend from volcanic basalt soils near Aniane, combining Northern Rhône precision with Mediterranean depth in a wine of extraordinary complexity.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Braised leg of lamb with black olive and anchovy crust", "complement", "classic", "main",
         "Mediterranean lamb preparation matches this Syrah-dominant blend's dark olive and savouriness perfectly.")
    PAIR(prod1b, "Roast beef fillet with bone marrow gratin and truffle jus", "elevate", "established", "main",
         "Vaillé's rare wine demands luxury ingredients — bone marrow and truffle bridge at the same prestige level.")
    PAIR(prod1b, "Aged Comté with black walnut bread and fig preserve", "complement", "established", "cheese",
         "The wine's dark fruit concentration and structure make it a compelling match for aged hard mountain cheese.")
    PAIR(prod1b, "Venison carpaccio with black pepper, rocket, and shaved Pecorino", "complement", "adventurous", "starter",
         "Raw game with pepper and aged sheep's cheese creates an elegant, mineral-driven contrast with this cult wine.")

# ── Region 2: Bandol ─────────────────────────────────────────────────────────
print("\n=== Region 2: Bandol ===")
r2 = R("Bandol", "France", "wine",
    designation_type="AOC",
    designation_name="Bandol AOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="A small coastal appellation west of Toulon on the Provence coast, producing France's greatest Mourvèdre-dominant red wine and celebrated rosé. The Bandol terroir — blue clay limestone soils, brilliant Mediterranean sun, and coastal wind — produces reds of extraordinary density, tannin, and longevity; minimum 18 months oak aging is required. Mourvèdre here reveals its full character: dark, meaty, and mineral.",
    key_producers="Château Pradeaux, Domaine Tempier, Domaine de Pibarnon, Château de la Rouvière",
    historical_context="Bandol's wines were traded from the port town of Bandol to the English market in the 18th century; the AOC was granted in 1941; Lulu Peyraud of Domaine Tempier was the great champion of Bandol's international reputation, attracting writers including Richard Olney to the domaine.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Domaine Tempier", "winery", r2, "France",
    production_philosophy="traditional",
    philosophy_description="The founding estate of Bandol's modern identity — the Peyraud family's Tempier produces the most celebrated Mourvèdre red wines in France, including single-vineyard La Migoua and La Tourtine alongside the classic cuvée that defined Bandol's character for 70 years.",
    reputation_narrative="The most famous Bandol estate internationally; Alice Waters, Kermit Lynch, and Richard Olney all championed Tempier's wines.",
    price_positioning="premium")

prod2b_id = P("Château Pradeaux", "winery", r2, "France",
    production_philosophy="traditional",
    philosophy_description="The most traditional and long-lived Bandol estate — Pradeaux ages its Mourvèdre in large old foudres for 4-5 years before release, producing wines of extraordinary tannic structure and 30-year aging potential that reward extreme patience.",
    reputation_narrative="The most age-worthy Bandol estate; Pradeaux wines from exceptional vintages can outlast many Bordeaux First Growths.",
    price_positioning="premium")

prod2a, new2a = PROD("Domaine Tempier Bandol Rouge Classique", "wine_still", prod2a_id, r2, "France",
    subcategory="Mourvèdre Blend",
    description="Tempier's flagship Bandol rouge — a Mourvèdre-dominant blend that defines the appellation: dark cherry, black olive, garrigue, iron, and powerful but fine tannin structure. The benchmark for Provençal red wine.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Grilled lamb chops with herbes de Provence and ratatouille", "complement", "classic", "main",
         "The definitive Provence pairing — Mourvèdre's olive and garrigue character mirrors Mediterranean ratatouille.")
    PAIR(prod2a, "Bouillabaisse with rouille and croûtons", "complement", "classic", "main",
         "Bandol's coastal terroir paired with Marseille's iconic fish stew — the two are born from the same landscape.")
    PAIR(prod2a, "Tapenade crostini with anchovies and hard-boiled egg", "complement", "classic", "aperitif",
         "Provençal aperitif food with Provençal wine — black olive tapenade mirrors Mourvèdre's olive character.")
    PAIR(prod2a, "Braised pork belly with fennel, star anise, and citrus", "complement", "established", "main",
         "Rich pork braised with anise shares Mourvèdre's meaty depth and the wine's garrigue herbal complexity.")

prod2b, new2b = PROD("Château Pradeaux Bandol Rouge", "wine_still", prod2b_id, r2, "France",
    subcategory="Mourvèdre",
    description="The most structured and age-worthy Bandol — dominated by Mourvèdre aged in large old foudres for years before release. Dense, tannic, and deeply mineral with iron, dark cherry, and black olive; requires a decade of patience.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Daube de boeuf Provençale with olives and orange zest", "complement", "classic", "main",
         "The classic Provençal braised beef with olives and orange peel — a regional soul food pairing for Bandol.")
    PAIR(prod2b, "Venison shoulder with juniper, blackberry, and root purée", "complement", "established", "main",
         "Pradeaux's powerful tannin structure handles game with authority; dark berry echoes the wine's depth.")
    PAIR(prod2b, "Aged Cantal with smoked olive oil and black pepper", "complement", "established", "cheese",
         "Hard aged French cheese from the Auvergne — the simplicity of aged Cantal meets Mourvèdre's complexity.")
    PAIR(prod2b, "Slow-roasted suckling pig with preserved lemon and thyme", "complement", "established", "main",
         "Pork's fat and Mourvèdre's tannin are natural partners — preserved lemon and thyme echo the garrigue.")

# ── Region 3: Beaumes de Venise ──────────────────────────────────────────────
print("\n=== Region 3: Gigondas ===")
r3 = R("Gigondas", "France", "wine",
    designation_type="AOC",
    designation_name="Gigondas AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="A Southern Rhône appellation of exceptional character nestled beneath the dramatic Dentelles de Montmirail mountains east of Châteauneuf-du-Pape. Gigondas produces powerful, structured Grenache-dominant reds — often considered the 'poor man's Châteauneuf' though its limestone and clay soils and altitude provide distinct freshness and mineral character. The appellation rose from Côtes du Rhône to full AOC in 1971.",
    key_producers="Château Rayas (Pignan), Domaine du Cayron, Saint-Gayan, Domaine de Font-Sane",
    historical_context="Gigondas wines were used to fortify Burgundy and Beaujolais before French appellation law prohibited the practice; once demoted, the appellation rebuilt its identity around quality Grenache blends over 50 years.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Domaine du Cayron", "winery", r3, "France",
    production_philosophy="traditional",
    philosophy_description="One of Gigondas's reference estates — Michel Faraud's old-vine Grenache from limestone and clay soils produces wines of extraordinary purity and depth, aged in large old foudres without new oak to preserve fruit expression.",
    reputation_narrative="Consistently cited as one of Gigondas's finest, most authentic expressions; wines of great aging potential.",
    price_positioning="mid_range")

prod3b_id = P("Domaine Saint-Gayan", "winery", r3, "France",
    production_philosophy="traditional",
    philosophy_description="Roger Meffre and his son Jean-Pierre produce some of Gigondas's most complete wines from very old vine Grenache parcels — their Gigondas is one of the Southern Rhône's most reliably excellent and long-lived expressions.",
    reputation_narrative="A reference for old-vine Gigondas; regular praise from major critics for consistency and value.",
    price_positioning="mid_range")

prod3a, new3a = PROD("Domaine du Cayron Gigondas", "wine_still", prod3a_id, r3, "France",
    subcategory="Grenache Blend",
    description="Old-vine Gigondas from the Cayron limestone plateau — Grenache with Syrah and Mourvèdre, aged in large old foudres. Rich, dark, and mineral with a signature freshness from the Dentelles' altitude and the appellation's cool clay and limestone soils.",
    price_tier="mid_range")
if new3a:
    PAIR(prod3a, "Lamb gigot with garlic, anchovy, and wild rosemary", "complement", "classic", "main",
         "The Southern Rhône's definitive pairing — slow-roasted lamb with Mediterranean herbs and Grenache-dominant red.")
    PAIR(prod3a, "Wild mushroom tart with Pélardon goat's cheese", "complement", "established", "starter",
         "Earthy, fungal notes echo the wine's depth while goat's cheese adds the regional Provençal dimension.")
    PAIR(prod3a, "Grilled beef entrecôte with thyme butter and aioli", "complement", "established", "main",
         "Classic Southern French grill pairing — Grenache's red fruit and the beef's char in easy harmony.")
    PAIR(prod3a, "Banon leaf-wrapped cheese at room temperature", "complement", "established", "cheese",
         "Aged Provençal goat's cheese wrapped in chestnut leaves — a regional cheese board classic with Gigondas.")

prod3b, new3b = PROD("Domaine Saint-Gayan Gigondas", "wine_still", prod3b_id, r3, "France",
    subcategory="Grenache Blend",
    description="Saint-Gayan's benchmark Gigondas — a traditional Grenache-dominant blend showing the Southern Rhône's characteristic warmth with Dentelles mineral freshness. Reliable, structured, and genuine with dark cherry, olive, and spice.",
    price_tier="mid_range")
if new3b:
    PAIR(prod3b, "Slow-cooked lamb tagine with apricot and preserved lemon", "complement", "established", "main",
         "North African-inflected lamb preparation shares the warm spice and dried-fruit character of Southern Rhône.")
    PAIR(prod3b, "Roasted aubergine with tomato, olives, and feta", "complement", "established", "main",
         "Mediterranean vegetable preparation mirrors the garrigue-herb character of this Grenache blend.")
    PAIR(prod3b, "Grilled merguez sausage with harissa and flatbread", "complement", "established", "casual",
         "Provençal-North African crossover — spiced lamb sausage with a rustic Southern Rhône red is a natural fit.")
    PAIR(prod3b, "Roquefort with honeycomb and walnut pain de campagne", "contrast", "established", "cheese",
         "Roquefort's bold salt and the honeycomb's sweetness contrast beautifully with Grenache's dark fruit warmth.")

# ── Region 4: Xinomavro / Naoussa ───────────────────────────────────────────
print("\n=== Region 4: Naoussa ===")
r4 = R("Naoussa", "Greece", "wine",
    designation_type="PDO",
    designation_name="Naoussa PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Northern Greece's most prestigious red wine PDO, located in Macedonia south of Thessaloniki beneath Mount Vermio. Naoussa produces exclusively Xinomavro — Greece's greatest indigenous red variety, often compared to Nebbiolo for its high acid, high tannin structure and ability to age magnificently. The variety's name means 'acid black' in Greek. The terraced vineyards of Naoussa's sandy clay produce reds of extraordinary complexity and longevity.",
    key_producers="Kir-Yianni, Boutari, Thymiopoulos, Alpha Estate",
    historical_context="Naoussa was one of Greece's first AOC-equivalent designations, granted in 1971; the region's wines were exported to the Ottoman Empire and Russia in the 18th century; Naoussa's sandy soils protected its pre-phylloxera vine heritage.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "rising"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Kir-Yianni Estate", "winery", r4, "Greece",
    production_philosophy="terroir_focused",
    philosophy_description="Founded by Yiannis Boutaris, Kir-Yianni produces single-vineyard Naoussa Xinomavro of international acclaim — Ramnista and Diaporos are the benchmark bottlings, aged in French oak barrels to preserve Xinomavro's characteristic acidity and tannin.",
    reputation_narrative="The reference estate for quality Naoussa; Kir-Yianni pioneered international interest in Greek fine wine.",
    price_positioning="premium")

prod4b_id = P("Thymiopoulos Vineyards", "winery", r4, "Greece",
    production_philosophy="natural",
    philosophy_description="Apostolos Thymiopoulos is Naoussa's most exciting natural winemaker — his Earth and Sky and Uranos Xinomavro cuvées use minimal sulphur, whole-bunch fermentation, and old foudres to produce wines of unprecedented freshness and purity for the appellation.",
    reputation_narrative="The most internationally acclaimed younger producer in Naoussa; Earth and Sky Xinomavro is a reference for natural Greek wine.",
    price_positioning="mid_range")

prod4a, new4a = PROD("Kir-Yianni Ramnista Naoussa", "wine_still", prod4a_id, r4, "Greece",
    subcategory="Xinomavro",
    description="From the Ramnista single vineyard — old-vine Xinomavro on red sandy clay soils at high altitude, aged in French oak. The benchmark Naoussa: tomato, sour cherry, dried flowers, and firm Nebbiolo-like tannin structure with extraordinary aging potential.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Slow-braised lamb kleftiko with lemon, garlic, and oregano", "complement", "classic", "main",
         "Greece's most beloved slow-cooked lamb with the country's most structured red — a regional archetype.")
    PAIR(prod4a, "Grilled octopus with olive oil, lemon, and dried oregano", "complement", "classic", "main",
         "Greek taverna staple with Xinomavro — the variety's acidity and tannin cut through charred octopus.")
    PAIR(prod4a, "Moussaka with béchamel and aged Kefalotyri", "complement", "established", "main",
         "Greece's defining baked dish with its defining red wine — Xinomavro's acidity balances the béchamel richness.")
    PAIR(prod4a, "Aged Graviera cheese with thyme honey and dried figs", "complement", "established", "cheese",
         "Hard Greek sheep's milk cheese with Xinomavro — a regional cheese board that showcases Greek terroir.")

prod4b, new4b = PROD("Thymiopoulos Earth and Sky Xinomavro", "wine_still", prod4b_id, r4, "Greece",
    subcategory="Xinomavro",
    description="A minimal-intervention Xinomavro of extraordinary freshness — whole-bunch fermented with natural yeasts, aged in large foudres. Lighter and more aromatic than traditional Naoussa expressions, revealing Xinomavro's floral, red-cherry, and savoury dimension.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Grilled lamb cutlets with tzatziki and charred pita", "complement", "classic", "main",
         "The simplest Greek expression — grilled lamb cutlets with refreshing tzatziki and a natural Xinomavro.")
    PAIR(prod4b, "Spanakopita with feta and wild greens", "complement", "established", "starter",
         "The freshness of this Xinomavro mirrors the bright, herbal character of Greek spinach and feta pie.")
    PAIR(prod4b, "Beef stifado with pearl onions and cinnamon", "bridge", "established", "main",
         "The sweet cinnamon and sour cherry in stifado mirror Xinomavro's characteristic flavour profile exactly.")
    PAIR(prod4b, "Feta marinated in olive oil and herbs with olives", "complement", "classic", "aperitif",
         "The quintessential Greek aperitif pairing — marinated feta and natural Xinomavro, both vivid and aromatic.")

# ── Region 5: Santorini ──────────────────────────────────────────────────────
print("\n=== Region 5: Santorini ===")
r5 = R("Santorini", "Greece", "wine",
    designation_type="PDO",
    designation_name="Santorini PDO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="One of the world's most extraordinary wine-growing environments — volcanic island in the Aegean Sea, using a unique training system (kouloura) where ancient, ungrafted Assyrtiko vines coil in baskets close to the ground to resist the fierce Meltemi winds. Santorini Assyrtiko is Greece's greatest white wine: volcanic mineral, lime-accented, high-acid, and capable of extraordinary aging. A wine of global significance.",
    key_producers="Domaine Sigalas, Gaia Wines, Hatzidakis, Santo Wines, Argyros",
    historical_context="Santorini's vines survived phylloxera because the volcanic pumice soil is hostile to the louse — the island maintains some of the world's oldest ungrafted vines, possibly dating back over 500 years of continuous cultivation on the same root stock.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "exceptional", "rising"),
    (2021, "very_good", "stable"), (2020, "excellent", "stable"), (2019, "very_good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Domaine Sigalas", "winery", r5, "Greece",
    production_philosophy="terroir_focused",
    philosophy_description="Paris Sigalas produces Santorini's most internationally acclaimed Assyrtiko — his barrel-fermented Kavalieros and crisp unoaked Assyrtiko have defined the modern benchmark for the variety, combining volcanic minerality with precise winemaking.",
    reputation_narrative="The reference Santorini estate internationally; Kavalieros single-vineyard Assyrtiko is the island's most prestigious wine.",
    price_positioning="premium")

prod5b_id = P("Gaia Wines", "winery", r5, "Greece",
    production_philosophy="terroir_focused",
    philosophy_description="Leon Karatsalos and Yiannis Paraskevopoulos co-founded Gaia to explore Greece's most interesting indigenous varieties — Thalassitis Assyrtiko from Santorini and the Wild Ferment version are defining expressions of the island's terroir.",
    reputation_narrative="One of Greece's most important fine wine estates; Thalassitis is a benchmark for Santorini Assyrtiko globally.",
    price_positioning="premium")

prod5a, new5a = PROD("Domaine Sigalas Assyrtiko Kavalieros", "wine_still", prod5a_id, r5, "Greece",
    subcategory="Assyrtiko",
    description="Single-vineyard Assyrtiko from the Kavalieros plot — barrel-fermented with extended lees contact, producing a textural, mineral, and complex expression of Santorini's volcanic terroir with extraordinary aging potential.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Grilled whole sea bream with lemon, olive oil, and capers", "complement", "classic", "main",
         "Aegean whole fish with volcanic island white — the wine's citrus and mineral mirror the sea bream's freshness.")
    PAIR(prod5a, "White bean soup (fasolada) with extra-virgin olive oil and oregano", "complement", "established", "starter",
         "Greece's national soup with Santorini Assyrtiko — the olive oil bridges both while the acidity lifts the beans.")
    PAIR(prod5a, "Grilled lobster with lemon butter and wild herbs", "complement", "established", "main",
         "Aegean luxury — barrel-fermented Assyrtiko's texture and mineral match lobster's oceanic richness.")
    PAIR(prod5a, "Fava Santorini with capers and spring onion", "complement", "classic", "starter",
         "Santorini's own yellow split pea purée is the classic regional pairing for island Assyrtiko.")

prod5b, new5b = PROD("Gaia Thalassitis Assyrtiko", "wine_still", prod5b_id, r5, "Greece",
    subcategory="Assyrtiko",
    description="Unoaked Santorini Assyrtiko of great precision — volcanic mineral, lime zest, saline, and bone-dry with electrifying acidity. Thalassitis ('of the sea') captures the island's maritime character in its purest form.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Freshly shucked oysters with Santorini tomato water", "cleanse", "classic", "aperitif",
         "Volcanic island wine with Aegean shellfish — the saline minerality mirrors the oyster's brine exactly.")
    PAIR(prod5b, "Grilled octopus with capers, sun-dried tomato, and ouzo vinaigrette", "complement", "classic", "main",
         "The quintessential Santorini taverna experience — charred octopus with the island's crisp white wine.")
    PAIR(prod5b, "Fried whitebait with lemon and sea salt", "complement", "classic", "starter",
         "Crispy small fish with a crisp volcanic white — the simplest and most perfect Aegean pairing.")
    PAIR(prod5b, "Chlorotyri fresh cheese with Santorini cherry tomatoes", "complement", "classic", "cheese",
         "Santorini's own fresh cheese with the island's famous tiny tomatoes and its native white wine — pure island harmony.")

# ── Counts ────────────────────────────────────────────────────────────────────
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
cur.close()
conn.close()
