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

# ── Region 1: Kamptal ────────────────────────────────────────────────────────
print("\n=== Region 1: Kamptal ===")
r1 = R("Kamptal", "Austria", "wine",
    designation_type="DAC",
    designation_name="Kamptal DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Austria's most exciting white wine region after Wachau — the Kamp River valley north of Langenlois produces extraordinary Riesling and Grüner Veltliner from volcanic basalt, crystalline gneiss, and loess soils. The diversity of Kamptal's soils allows multiple expressions of both varieties across numerous single-vineyard sites. The Heiligenstein volcanic basalt vineyard — shared by Bründlmayer and Schloss Gobelsburg — is Austria's most famous Riesling site outside Wachau.",
    key_producers="Bründlmayer, Schloss Gobelsburg, Loimer, Hirsch, Jurtschitsch",
    historical_context="The Cistercian monks of Stift Zwettl cultivated the Kamp Valley vineyards for 800 years; the DAC system was introduced in 2008 to protect and promote Kamptal's Grüner Veltliner and Riesling identity against the generic Austrian blending tradition.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "excellent", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Weingut Bründlmayer", "winery", r1, "Austria",
    production_philosophy="biodynamic",
    philosophy_description="Willi Bründlmayer is the patriarch of Kamptal — his biodynamically farmed estate produces the benchmark Kamptal Rieslings from Heiligenstein volcanic basalt and the finest Grüner Veltliner from Lamm loess. The Sekt Brut and various white wines span Austria's most complete quality range from a single estate.",
    reputation_narrative="Austria's most complete white wine estate; Heiligenstein Riesling Lyra is among Austria's most prestigious bottles.",
    price_positioning="premium")

prod1b_id = P("Schloss Gobelsburg", "winery", r1, "Austria",
    production_philosophy="traditional",
    philosophy_description="Under Michael Moosbrugger's stewardship since 1996, this Cistercian monastery winery produces Kamptal's finest Riesling and Grüner Veltliner alongside historic Heuriger wines. The Tradition Riesling and Grüner Veltliner represent Austria's most intellectually ambitious single-variety expressions.",
    reputation_narrative="One of Austria's most historically significant estates; Schloss Gobelsburg Riesling Heiligenstein is a regional treasure.",
    price_positioning="premium")

prod1a, new1a = PROD("Bründlmayer Riesling Heiligenstein Lyra", "wine_still", prod1a_id, r1, "Austria",
    subcategory="Riesling",
    description="From the Heiligenstein volcanic basalt site — Austria's most celebrated Riesling outside Wachau. The Lyra vine training produces extreme concentration from the ancient basalt soils: citrus, peach, flint, and mineral precision with 20-year aging potential.",
    price_tier="premium")
if new1a:
    PAIR(prod1a, "Wiener Schnitzel with warm potato salad and cucumber", "complement", "classic", "main",
         "Austria's definitive dish with Austria's finest Riesling — the wine's acidity cuts through the breaded veal.")
    PAIR(prod1a, "Zander (pike-perch) with brown butter, capers, and lemon", "complement", "classic", "fish_course",
         "Austrian freshwater fish with Austrian mineral Riesling — a Danube Valley pairing of great regional authenticity.")
    PAIR(prod1a, "White asparagus with hollandaise and air-dried ham", "complement", "classic", "starter",
         "Austria's spring asparagus season demands Kamptal Riesling — the wine's acid and mineral bridge through the rich sauce.")
    PAIR(prod1a, "Graukäse (grey cheese) with rye bread and radish", "complement", "adventurous", "cheese",
         "Austria's most challenging soured whey cheese with the Heiligenstein's mineral precision — a provocative pairing.")

prod1b, new1b = PROD("Schloss Gobelsburg Grüner Veltliner Lamm", "wine_still", prod1b_id, r1, "Austria",
    subcategory="Grüner Veltliner",
    description="From the loess-over-gneiss Lamm vineyard in the Kamptal — Austria's reference single-vineyard Grüner Veltliner, combining the variety's signature white pepper, grapefruit, and mineral character with extraordinary texture from old vines and a long winemaking tradition.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled Wachau asparagus with truffle butter and shaved Parmigiano", "complement", "classic", "starter",
         "Grüner Veltliner is spring asparagus's perfect partner — white pepper note echoes through the vegetable.")
    PAIR(prod1b, "Tafelspitz (boiled prime beef) with creamed spinach and apple-horseradish", "complement", "classic", "main",
         "Austria's imperial dish with its signature grape variety — the wine's pepper and mineral frame the boiled beef.")
    PAIR(prod1b, "Cured Lachsschinken (loin ham) with Dijon and cornichons", "complement", "established", "starter",
         "Austrian air-cured pork loin with Kamptal GV — mustard bridges the wine's pepper and the ham's cured saline.")
    PAIR(prod1b, "Emmental with apple and walnut on bread", "complement", "established", "cheese",
         "Hard Alpine cheese with apple and walnut echoes Grüner Veltliner's white pepper and mineral freshness.")

# ── Region 2: Styria (Südsteiermark) ─────────────────────────────────────────
print("\n=== Region 2: Styria ===")
r2 = R("Styria", "Austria", "wine",
    designation_type="DAC",
    designation_name="Südsteiermark DAC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Austria's southernmost wine region bordering Slovenia, producing the country's finest Sauvignon Blanc and some of its most elegant Welschriesling and Muskateller from dramatic steep hillside vineyards in the Südsteiermark (South Styria), Weststeiermark, and Vulkanland sub-regions. The Mediterranean climate moderated by Alpine winds produces wines of remarkable freshness and aromatic precision — Styrian Sauvignon Blanc rivals Sancerre in quality and has its own distinct mineral character.",
    key_producers="Tement, E. & M. Tscheppe, Gross, Lackner-Tinnacher, Muster",
    historical_context="South Styria's identity as Austria's finest Sauvignon Blanc producer was established by Manfred Tement in the 1980s; the region's proximity to Slovenia reflects centuries of Austro-Hungarian cross-cultural viticulture that created one of Europe's most distinctive wine identities.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "exceptional", "rising"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Weingut Tement", "winery", r2, "Austria",
    production_philosophy="biodynamic",
    philosophy_description="Manfred and Armin Tement produce South Styria's most iconic Sauvignon Blanc from the Zieregg vineyard — Austria's most celebrated single-vineyard white wine site, combining volcanic and clay-rich soils at high altitude to produce a wine that rivals Burgundy Grand Cru in complexity.",
    reputation_narrative="South Styria's reference estate; Zieregg Sauvignon Blanc is Austria's most internationally celebrated non-Wachau white.",
    price_positioning="ultra_premium")

prod2b_id = P("Weingut Gross", "winery", r2, "Austria",
    production_philosophy="terroir_focused",
    philosophy_description="Alois Gross's estate in Ratsch produces benchmark Styrian Sauvignon Blanc and Welschriesling from steep slate and clay vineyards — the Nussberg and Sulz cuvées are among South Styria's finest terroir expressions.",
    reputation_narrative="One of South Styria's most respected family estates; internationally recognised for Sauvignon Blanc precision.",
    price_positioning="premium")

prod2a, new2a = PROD("Tement Zieregg Sauvignon Blanc", "wine_still", prod2a_id, r2, "Austria",
    subcategory="Sauvignon Blanc",
    description="From the Zieregg volcanic and clay hillside vineyard — Austria's most famous single-vineyard Sauvignon Blanc. Combining cool-climate freshness with texture and mineral depth, Zieregg is more complex than most Loire or New Zealand Sauvignon, aging beautifully over 10+ years.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Styrian Backhendl (fried chicken) with cucumber salad", "complement", "classic", "main",
         "Styria's beloved fried chicken dish with Styria's most famous white wine — a crisp regional pairing.")
    PAIR(prod2a, "Steamed asparagus from Graz with Sauce Béarnaise", "complement", "classic", "starter",
         "Styrian asparagus and Sauvignon Blanc — the wine's citrus and green herb character mirror béarnaise's tarragon.")
    PAIR(prod2a, "Seared scallop with pea purée and lime butter", "complement", "established", "starter",
         "Sauvignon's citrus and green character complement scallop's sweetness and the pea's vegetal freshness.")
    PAIR(prod2a, "Steirischer Ziegenfrischkäse (Styrian fresh goat's cheese) with herbs", "complement", "classic", "cheese",
         "Regional young goat's cheese with the region's greatest white wine — a natural Styrian terroir pairing.")

prod2b, new2b = PROD("Gross Sauvignon Blanc Nussberg", "wine_still", prod2b_id, r2, "Austria",
    subcategory="Sauvignon Blanc",
    description="From the Nussberg hillside in Ratsch — Gross's signature Sauvignon Blanc showing South Styria's characteristic mineral precision, grapefruit, elderflower, and a chalky mineral finish that distinguishes it from the Loire's flintier style.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Grilled sea bass with fennel salad and lemon dressing", "complement", "established", "fish_course",
         "Crisp Austrian Sauvignon Blanc's mineral freshness and citrus frame sea bass with precision.")
    PAIR(prod2b, "Styrian pumpkin soup with pumpkin seed oil and crème fraîche", "complement", "classic", "starter",
         "The Styrian pumpkin and its seed oil are regional icons — the wine's crisp acidity balances the soup's richness.")
    PAIR(prod2b, "Thai-style glass noodle salad with prawns and lemongrass", "complement", "established", "main",
         "Sauvignon Blanc's aromatic freshness is the perfect foil for lemongrass, lime, and chilli in the dressing.")
    PAIR(prod2b, "Young Austrian goat's cheese with wildflower honey and walnuts", "complement", "established", "cheese",
         "Fresh regional goat's cheese with Styrian Sauvignon — one of wine's timeless grape-and-cheese harmonies.")

# ── Region 3: Beaujolais — Morgon ─────────────────────────────────────────────
print("\n=== Region 3: Morgon ===")
r3 = R("Morgon", "France", "wine",
    designation_type="AOC",
    designation_name="Morgon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of the ten Beaujolais Crus, Morgon is the most structured and age-worthy after Moulin-à-Vent, known for its distinctive volcanic decomposed schist (roche pourrie — 'rotten rock') of the Côte du Py hill that gives Gamay wines a density and iron-mineral character unique among Beaujolais. In great years, Morgon from Côte du Py evolves into a wine that uncannily resembles mature Pinot Noir from Burgundy — a phenomenon that Beaujolais lovers call 'Morgonner'.",
    key_producers="Jean-Paul Thévenet, Marcel Lapierre, Jean Foillard, Mathieu Lapierre, Louis-Claude Desvignes",
    historical_context="The 'Gang of Four' (Lapierre, Foillard, Breton, Métras) pioneered natural Beaujolais in Morgon in the 1980s under Jules Chauvet's guidance — establishing Beaujolais's quality revival and inspiring the global natural wine movement.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Marcel Lapierre", "winery", r3, "France",
    production_philosophy="natural",
    philosophy_description="Marcel Lapierre was the father of natural Beaujolais — his no-sulphur, whole-bunch fermented Morgon transformed perceptions of the cru and launched the global natural wine movement. Now run by son Mathieu and daughter Camille with the same philosophy.",
    reputation_narrative="The founding estate of the natural wine movement; Lapierre Morgon is among the most beloved wines in natural wine culture.",
    price_positioning="premium")

prod3b_id = P("Jean Foillard", "winery", r3, "France",
    production_philosophy="natural",
    philosophy_description="One of the natural Beaujolais pioneers alongside Lapierre — Jean Foillard's Côte du Py Morgon from old-vine Gamay on volcanic schist is one of the cru's most concentrated and complex expressions, fermented without added sulphur and aged in large old barrels.",
    reputation_narrative="A founding member of natural Beaujolais; Côte du Py is among Morgon's most sought-after single-vineyard wines.",
    price_positioning="premium")

prod3a, new3a = PROD("Marcel Lapierre Morgon", "wine_still", prod3a_id, r3, "France",
    subcategory="Gamay",
    description="The natural wine movement's most iconic bottle — whole-bunch fermented Morgon with no added sulphur, expressing the Côte du Py's volcanic roche pourrie character with extraordinary purity: dark cherry, iron mineral, and a silk that develops with 5-10 years of aging.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Rosette de Lyon charcuterie with cornichons and Dijon", "complement", "classic", "casual",
         "The Lyon bouchon archetype — charcuterie with natural Beaujolais is both a cultural and gastronomic institution.")
    PAIR(prod3a, "Boudin noir (black pudding) with apple compote and mashed potato", "complement", "classic", "main",
         "Classic French bistro pairing — iron-rich blood sausage echoes Morgon's iron and dark-fruit mineral character.")
    PAIR(prod3a, "Duck terrine en croûte with green peppercorn and cornichon", "complement", "established", "starter",
         "Rustic game terrine with natural Morgon — both share a wild, unfiltered character that's deeply satisfying.")
    PAIR(prod3a, "Grilled bone-in pork chop with mustard sauce and sautéed mushrooms", "complement", "classic", "main",
         "Morgon's structure and dark fruit handle the pork chop's fat — mustard's acidity mirrors the wine's character.")

prod3b, new3b = PROD("Jean Foillard Morgon Côte du Py", "wine_still", prod3b_id, r3, "France",
    subcategory="Gamay",
    description="From the Côte du Py's volcanic decomposed schist — Foillard's Morgon is among the cru's most structured and concentrated expressions: dark cherry, iron, volcanic mineral, and a tannin structure that confirms Morgon's claim as Beaujolais's most Burgundian cru.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Chicken liver parfait with Cognac and brioche toast", "complement", "established", "starter",
         "Rich liver preparation with a structured Beaujolais cru — the wine's iron mineral echoes the liver's depth.")
    PAIR(prod3b, "Pot-au-feu with bone marrow toast and gros sel", "complement", "classic", "main",
         "France's defining winter broth with Morgon — the wine's mineral depth and structure bridge the marrow richness.")
    PAIR(prod3b, "Roasted duck breast with cherry gastrique and celeriac", "complement", "classic", "main",
         "Dark cherry and iron in Côte du Py Gamay mirror the duck preparation's fruit and richness.")
    PAIR(prod3b, "Saint-Marcellin at peak ripeness, just running", "complement", "classic", "cheese",
         "Rhône Valley's tiny runny cheese at peak ripeness with a structured natural Morgon — regional French harmony.")

# ── Region 4: Fleurie ─────────────────────────────────────────────────────────
print("\n=== Region 4: Fleurie ===")
r4 = R("Fleurie", "France", "wine",
    designation_type="AOC",
    designation_name="Fleurie AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The most feminine and floral of the Beaujolais Crus — Fleurie's pink granite hillsides and clay-sand soils produce Gamay wines of extraordinary delicacy, violets, and red fruit. The Clos de la Roilette, La Madone, and Grille-Midi are the most celebrated single-vineyard sites. Fleurie's approachable elegance makes it the gateway Beaujolais cru for many wine lovers discovering the region's serious side.",
    key_producers="Michel Chignard, Clos de la Roilette, Château de Fleurie, Jean-Marc Despres",
    historical_context="Fleurie's distinctive pink granite was formed through volcanic intrusion 300 million years ago; the name 'Fleurie' (flowery) perfectly captures the cru's characteristic violet and rose-petal aromatics from this granitic terroir.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "stable"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Michel Chignard", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="The reference domaine for traditional Fleurie — Michel and Eric Chignard produce old-vine Gamay from the Morier and Les Moriers parcels using a mix of whole-bunch and destemmed fruit in large oval vats, expressing Fleurie's floral, granitic character with exceptional purity.",
    reputation_narrative="Fleurie's most revered traditional estate; consistently cited as the appellation's benchmark producer.",
    price_positioning="mid_range")

prod4b_id = P("Clos de la Roilette", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="Alain Coudert's Clos de la Roilette is a historic walled vineyard in Fleurie — one of Beaujolais's few genuine clos, producing consistently elegant, floral Gamay that ages beautifully over 5-10 years from the cru's finest pink granite soils.",
    reputation_narrative="One of Fleurie's most historically significant and consistently excellent estates; Clos de la Roilette is a cru reference.",
    price_positioning="mid_range")

prod4a, new4a = PROD("Michel Chignard Fleurie Les Moriers", "wine_still", prod4a_id, r4, "France",
    subcategory="Gamay",
    description="From the Moriers parcel on pink granite — Chignard's benchmark Fleurie showing the cru's signature: violet, cherry blossom, red strawberry, and granitic mineral with silky texture and a freshness that makes it endlessly drinkable without sacrificing complexity.",
    price_tier="mid_range")
if new4a:
    PAIR(prod4a, "Saucisson chaud lyonnais with potato salad and mustard vinaigrette", "complement", "classic", "main",
         "Lyon's classic warm sausage dish with a Beaujolais cru — the wine's acidity cuts through pork fat with ease.")
    PAIR(prod4a, "Salade niçoise with high-quality canned tuna and Dijon vinaigrette", "complement", "established", "main",
         "Light, floral Fleurie bridges the salad's diverse flavours — olives, tuna, and egg find equal harmony.")
    PAIR(prod4a, "Chicken liver mousse with Cognac and brioche soldiers", "complement", "established", "starter",
         "Delicate liver mousse with floral Gamay — the wine's lightness contrasts richly without overwhelming.")
    PAIR(prod4a, "Tome des Bauges with walnuts and wildflower honey", "complement", "established", "cheese",
         "Semi-hard Savoie cheese with pink granite Gamay — both carry the same alpine freshness and mineral delicacy.")

prod4b, new4b = PROD("Clos de la Roilette Fleurie", "wine_still", prod4b_id, r4, "France",
    subcategory="Gamay",
    description="From Fleurie's historic walled clos on pink granite — Clos de la Roilette's Fleurie combines the cru's characteristic violet and cherry character with a structure from the sheltered site that allows graceful aging over 7-10 years.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Roasted quail with fig and wild thyme", "complement", "established", "main",
         "Delicate game bird with floral Gamay — fig echoes the wine's red fruit while thyme mirrors the granite herbal note.")
    PAIR(prod4b, "Pissaladière (Niçoise onion tart) with anchovy and olive", "complement", "established", "starter",
         "Provençal onion tart with southern French Gamay — a cross-regional French pairing through light red fruit.")
    PAIR(prod4b, "Rosette sausage with baby gherkins and mustard", "complement", "classic", "casual",
         "The bouchon Lyonnais standard with a clos Beaujolais — charcuterie and local Gamay is a cultural archetype.")
    PAIR(prod4b, "Époisses at the peak of ripeness, alone", "complement", "adventurous", "cheese",
         "Fleurie's floral Gamay offers a surprising bridge to pungent washed-rind Époisses — delicacy meets funk.")

# ── Region 5: Mâconnais ───────────────────────────────────────────────────────
print("\n=== Region 5: Mâconnais ===")
r5 = R("Mâconnais", "France", "wine",
    designation_type="AOC",
    designation_name="Mâcon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Burgundy's southernmost and most accessible wine region, producing Chardonnay from limestone and clay soils between Tournus and Mâcon. The finest expressions come from the limestone outcrops of Pouilly-Fuissé (France's most celebrated Mâconnais appellation), Saint-Véran, and Viré-Clessé. Mâconnais Chardonnay is more generous and peachy than Chablis or the Côte de Beaune — approachable young but increasingly showing aging potential from village-level producers pushing quality boundaries.",
    key_producers="Olivier Merlin, Château de la Saule, Domaine de la Soufrandière, Jean-Marie Guffens",
    historical_context="The Mâconnais was Burgundy's workhouse for centuries, producing bulk wine for northern France; the arrival of Jean-Marie Guffens from Belgium in the 1970s and his Verget négociant house transformed perceptions of Mâconnais quality; today Pouilly-Fuissé has premier cru status since 2020.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "very_good", "stable"),
    (2021, "excellent", "stable"), (2020, "very_good", "stable"), (2019, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Olivier Merlin", "winery", r5, "France",
    production_philosophy="terroir_focused",
    philosophy_description="One of the Mâconnais's most quality-focused estates — Olivier Merlin produces benchmark Mâcon La Roche Vineuse and Saint-Véran from single-parcel limestone sites, demonstrating that careful viticulture and winemaking can extract genuine terroir complexity from Mâconnais Chardonnay.",
    reputation_narrative="The reference estate for understanding Mâconnais quality potential; consistently praised by international critics.",
    price_positioning="mid_range")

prod5b_id = P("Domaine de la Soufrandière", "winery", r5, "France",
    production_philosophy="biodynamic",
    philosophy_description="The Bret Brothers' Bâtard-Montrachet-adjacent Pouilly-Vinzelles estate demonstrates that certified biodynamic farming on the Mâconnais's finest limestone soils can produce white wines of near-Côte de Beaune complexity at accessible prices.",
    reputation_narrative="One of the Mâconnais's most distinctive biodynamic producers; Quintaine Viré-Clessé is a benchmark.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Olivier Merlin Mâcon La Roche Vineuse Vieilles Vignes", "wine_still", prod5a_id, r5, "France",
    subcategory="Chardonnay",
    description="From old-vine Chardonnay on the limestone outcrop of La Roche Vineuse — Merlin's benchmark Mâconnais demonstrating that careful single-parcel viticulture can produce wines of real complexity: white peach, hazelnut, limestone mineral, and freshness that challenges village-level Côte de Beaune.",
    price_tier="mid_range")
if new5a:
    PAIR(prod5a, "Gratin Dauphinois with Comté and thyme", "complement", "established", "main",
         "Classic Burgundian potato gratin with its regional white wine — cream and cheese gratin meets Chardonnay's richness.")
    PAIR(prod5a, "Quenelles de brochet with Nantua sauce (crayfish cream)", "complement", "classic", "main",
         "Burgundy's classic pike dumpling with crayfish cream — old-school French luxury with a regional white wine.")
    PAIR(prod5a, "Jambon persillé (parsley ham terrine) with Dijon mustard", "complement", "classic", "starter",
         "Burgundy's traditional ham and parsley terrine with a regional Mâconnais Chardonnay — a genuine local pairing.")
    PAIR(prod5a, "Époisses with crusty baguette and a touch of marc de Bourgogne", "bridge", "established", "cheese",
         "Burgundy's great washed-rind cheese with its great grape-based spirit and a regional Chardonnay — terroir in three.")

prod5b, new5b = PROD("Soufrandière Pouilly-Vinzelles Klimon", "wine_still", prod5b_id, r5, "France",
    subcategory="Chardonnay",
    description="Biodynamic Chardonnay from the Klimon parcel in Pouilly-Vinzelles — a Mâconnais expression of remarkable tension and mineral precision, showing what the region's limestone soils can achieve with biodynamic farming and restraint in the cellar.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Moules farcies with herb butter and garlic", "complement", "established", "starter",
         "Stuffed mussels with herb butter — Mâconnais Chardonnay's freshness and mineral frame the shellfish and garlic.")
    PAIR(prod5b, "Roast free-range chicken with tarragon cream and pommes vapeur", "complement", "classic", "main",
         "Classic Sunday French lunch — roast chicken with tarragon cream and Mâconnais white is a timeless combination.")
    PAIR(prod5b, "Saint-Jacques (scallop) with cauliflower and hazelnut butter", "complement", "established", "starter",
         "Scallop with hazelnut butter echoes Mâconnais Chardonnay's hazelnut and mineral character in a textural pairing.")
    PAIR(prod5b, "Chaource young cheese with apple and walnut bread", "complement", "established", "cheese",
         "Young mushroomy Chaource with Mâconnais Chardonnay — soft and fresh cheese with a soft, fresh white wine.")

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
