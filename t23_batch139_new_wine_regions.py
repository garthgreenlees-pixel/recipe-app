#!/usr/bin/env python3
"""B139 — Franciacorta DOCG (Italy), Trento DOC (Italy), Alto Adige DOC (Italy),
   Etna DOC (Italy), Nerello Mascalese (Etna supplement), Cerasuolo di Vittoria DOCG (Italy)
All constraints verified from B136-B138.
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

# ── FRANCIACORTA DOCG (Italy) ─────────────────────────────────────────────────
print("=== Franciacorta DOCG ===")
r = R("Franciacorta DOCG", "Italy", "wine",
      designation_type="DOCG",
      designation_name="Franciacorta DOCG",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="Italy's premier sparkling wine appellation from glacial moraines south of Lake Iseo in Lombardy. Traditional method (metodo classico) wines from Chardonnay, Pinot Nero and Pinot Bianco with mandatory extended lees aging. Franciacorta Riserva requires 60+ months on lees, producing complexity that rivals Champagne.",
      key_producers="Bellavista, Ca' del Bosco, Berlucchi",
      historical_context="Franciacorta's modern history begins with Berlucchi's first traditional method sparkling wine in 1961. DOCG status in 1995 was the first awarded to an Italian metodo classico wine. The appellation's strict production rules — minimum 18 months on lees for non-vintage, 30 for vintage, 60 for Riserva — have made Franciacorta Italy's most credible Champagne alternative.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Ideal Chardonnay vintage on glacial moraine; wines of exceptional freshness and fine bead."),
    (2019, "very_good", "stable", "Good balance of ripeness and acidity for traditional method wines of elegance."),
    (2020, "excellent", "rising", "Low yields produced Franciacorta of concentration; whites and Pinot Nero of depth."),
    (2021, "very_good", "stable", "Consistent quality; fresh acid backbone ideal for long lees aging in Riserva production."),
    (2022, "excellent", "rising", "Outstanding vintage; Chardonnay of benchmark mineral precision and longevity for Franciacorta."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Bellavista", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Vittorio Moretti's Bellavista is Franciacorta's most intellectually ambitious producer, pursuing single-vineyard, single-variety and terroir-specific expressions of traditional method wine that rival Champagne's complexity and age-worthiness.",
       reputation_narrative="Bellavista's Vittorio Moretti Riserva and single-vineyard wines are among Italy's most celebrated sparkling wines, demonstrating that Franciacorta can produce exceptional wines of international stature.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Bellavista Franciacorta Alma Gran Cuvée Brut", "wine_sparkling", p1, r, "Italy",
    subcategory="sparkling_white", price_tier="ultra_premium",
    description="Bellavista's flagship Franciacorta from Chardonnay with Pinot Nero; 30 months on lees, profound mineral depth, brioche, stone fruit and fine persistent bead. A Champagne rival of genuine stature.")
if is_new:
    PAIR(prod, "Risotto alla Milanese with saffron and marrow butter", "complement", "classic", "main", "Franciacorta's fine bead and mineral depth suit the richness of the Milanese classic saffron risotto.")
    PAIR(prod, "Vitello tonnato with capers and anchovy", "complement", "classic", "starter", "Fine Franciacorta bubbles cut through the tuna mayonnaise richness of this Piemontese-Lombard classic.")
    PAIR(prod, "Grilled gamberi with lemon butter and herbs", "complement", "established", "main", "Mineral brioche Franciacorta suits grilled prawns with lemon-butter with precision and elegance.")
    PAIR(prod, "Aged Parmigiano-Reggiano with acacia honey", "complement", "established", "cheese", "Crystal Parmesan and floral honey find the fine bubbles and mineral complexity of Franciacorta ideal.")

prod, is_new = PROD("Bellavista Franciacorta Satèn Brut", "wine_sparkling", p1, r, "Italy",
    subcategory="sparkling_white", price_tier="ultra_premium",
    description="100% Chardonnay Franciacorta Satèn (lower pressure, creamier texture); silk-textured, mineral and complex with stone fruit, cream and the characteristic gentle bead of the Satèn style.")
if is_new:
    PAIR(prod, "Burrata with white truffle shavings", "complement", "classic", "starter", "Satèn's silky texture and mineral depth are the ideal Italian fine wine pairing for burrata and truffle.")
    PAIR(prod, "Poached Breton lobster with caviar butter sauce", "elevate", "established", "main", "Silk-textured Franciacorta Satèn's mineral-cream character elevates lobster and caviar richness perfectly.")
    PAIR(prod, "Linguine with white asparagus, bottarga and lemon oil", "complement", "established", "main", "Satèn's textured creaminess suits the mineral-saline combination of asparagus and bottarga pasta.")
    PAIR(prod, "Pecorino di Fossa with honey and walnut", "complement", "established", "cheese", "Aged pit-ripened sheep cheese and walnut-honey find the silk mineral complexity of Satèn ideal.")

p2 = P("Ca' del Bosco", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Maurizio Zanella at Ca' del Bosco has spent 50 years developing Franciacorta as a world-class sparkling wine destination, producing traditional method wines of consistent excellence from a range of single-variety and blended expressions.",
       reputation_narrative="Ca' del Bosco's Cuvée Prestige and Vintage Collection are defining benchmarks for Franciacorta quality, known for their consistent excellence, accessibility and sophisticated expression of the appellation's terroir.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Ca' del Bosco Franciacorta Cuvée Prestige Brut", "wine_sparkling", p2, r, "Italy",
    subcategory="sparkling_white", price_tier="premium",
    description="Ca' del Bosco's flagship non-vintage Franciacorta; elegant, fresh and consistent with green apple, citrus and fine brioche character from Chardonnay, Pinot Nero and Pinot Bianco on glacial moraines.")
if is_new:
    PAIR(prod, "Capesante al naturale (raw scallop) with citrus", "complement", "classic", "casual", "Delicate raw scallop with citrus finds the fine mineral bead and freshness of Franciacorta ideal.")
    PAIR(prod, "Prosciutto crudo San Daniele with grissini", "complement", "classic", "casual", "The classic Italian aperitivo — fine cured ham with breadsticks — meets Franciacorta's fine bead.")
    PAIR(prod, "Grana Padano fritters with honey dip", "complement", "established", "casual", "Fried aged cheese with honey is a natural Lombard companion for Franciacorta Brut.")
    PAIR(prod, "Tagliolini al tartufo bianco d'Alba", "complement", "established", "main", "White truffle pasta from Alba finds Franciacorta's fine bead and mineral depth an exceptional match.")

prod, is_new = PROD("Ca' del Bosco Franciacorta Vintage Collection Brut", "wine_sparkling", p2, r, "Italy",
    subcategory="sparkling_white", price_tier="ultra_premium",
    description="Vintage Franciacorta with 30+ months on lees; structured, complex and mineral with layers of brioche, stone fruit and fine mineral character from the year's best Chardonnay and Pinot Nero.")
if is_new:
    PAIR(prod, "Whole roasted chicken with morel sauce and lemon", "complement", "established", "main", "Vintage Franciacorta's complex mineral-brioche character handles roasted chicken with umami morel sauce.")
    PAIR(prod, "Risotto al pesce persico con burro e salvia", "complement", "classic", "main", "Lake fish risotto with butter-sage is the Lombardy classic that needs Franciacorta's fine structured bubbles.")
    PAIR(prod, "Turbot au beurre blanc with oyster leaves", "complement", "established", "main", "Vintage Franciacorta suits the classic French-Italian combination of turbot with buttery white wine sauce.")
    PAIR(prod, "Sbrinz or aged Parmigiano with Aceto Balsamico Tradizionale", "complement", "established", "cheese", "Traditional 25-year balsamic with aged Italian hard cheese is the Lombard companion for vintage Franciacorta.")

# ── TRENTO DOC (Italy) ────────────────────────────────────────────────────────
print("=== Trento DOC ===")
r = R("Trento DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Trento DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Alpine Italy's finest traditional method sparkling wine appellation from steep Dolomite slopes in Trentino. Chardonnay and Pinot Nero grown at high altitude (500-900m) on porphyry and limestone produce spumante of extraordinary freshness, mineral precision and aging capacity. Ferrari is the dominant producer.",
      key_producers="Ferrari, Mezzacorona, Abate Nero",
      historical_context="Ferrari Trento's Giulio Ferrari created Italy's first methode champenoise wine in 1902, inspired by training in Champagne. Trento DOC was established 1993, the second Italian metodo classico DOC after Franciacorta. The extreme alpine altitude of the vineyards gives Trento spumante a freshness and mineral tension unavailable in warmer Italian regions.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Alpine Chardonnay of exceptional freshness from high-altitude porphyry vineyards."),
    (2019, "very_good", "stable", "Good acid backbone for traditional method; wines of characteristic Trentino mineral precision."),
    (2020, "excellent", "rising", "Alpine conditions delivered outstanding freshness; Trento DOC of superb lees-aging potential."),
    (2021, "very_good", "stable", "Consistent high-altitude quality; Chardonnay and Pinot Nero of fine acid structure."),
    (2022, "excellent", "rising", "Outstanding alpine vintage; Trento DOC wines of benchmark mineral freshness and longevity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Ferrari Trento", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Ferrari Trento is Italy's most historic metodo classico house, producing traditional method wines from high-altitude Trentino Chardonnay since 1902. The Giulio Ferrari Riserva, aged 10+ years on lees, is Italy's most acclaimed non-Champagne sparkling wine.",
       reputation_narrative="Ferrari Trento is Italy's greatest sparkling wine house by both history and quality. The Giulio Ferrari Riserva del Fondatore is considered Italy's most prestigious sparkling wine and a genuine rival to prestige Champagne.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Ferrari Trento Giulio Ferrari Riserva del Fondatore", "wine_sparkling", p1, r, "Italy",
    subcategory="sparkling_white", price_tier="ultra_premium",
    description="Italy's greatest sparkling wine — Giulio Ferrari's Blanc de Blancs from a single Chardonnay vineyard, aged 10+ years on lees. Profound mineral depth, toasted hazelnut, stone fruit and extraordinary persistent fine mousse.")
if is_new:
    PAIR(prod, "Oscietra caviar with blini and crème fraîche", "complement", "classic", "celebration", "Italy's greatest sparkling wine meets caviar's ocean mineral intensity in a celebration of maximum luxury.")
    PAIR(prod, "Whole Breton lobster à la nage with truffle butter", "complement", "classic", "main", "Toasted hazelnut mineral complexity of aged Giulio Ferrari elevates lobster with truffle butter to transcendence.")
    PAIR(prod, "Risotto with white truffle d'Alba, aged Parmesan and butter", "elevate", "classic", "main", "White truffle risotto with Parmesan is the defining Italian fine dining companion for Giulio Ferrari Riserva.")
    PAIR(prod, "Aged Parmigiano-Reggiano 48-month with traditional balsamic", "complement", "classic", "cheese", "48-month Parmesan crystals and 25-year balsamic match the mineral depth and aged complexity of Giulio Ferrari.")

prod, is_new = PROD("Ferrari Trento Brut", "wine_sparkling", p1, r, "Italy",
    subcategory="sparkling_white", price_tier="premium",
    description="Ferrari's flagship non-vintage Trento Brut; elegant, precise and consistent with green apple, lemon zest and chalky mineral character from high-altitude Trentino Chardonnay and Pinot Nero.")
if is_new:
    PAIR(prod, "Speck Alto Adige and gorgonzola bruschetta", "complement", "classic", "casual", "Smoked Alpine ham and blue cheese find the fine alpine mineral bead of Ferrari Trento Brut ideal.")
    PAIR(prod, "Grilled trota salmonata (salmon trout) with herbs", "complement", "classic", "main", "Alpine salmon trout with fresh herbs is a natural Trentino companion for Ferrari Brut's mineral freshness.")
    PAIR(prod, "Vitello tonnato with salted capers", "complement", "established", "starter", "Classic northern Italian cold veal with tuna sauce is the traditional aperitivo for Ferrari Brut.")
    PAIR(prod, "Canederli (bread dumplings) with mushroom broth", "bridge", "established", "main", "Trentino bread dumplings in mushroom broth find Ferrari Brut's alpine mineral precision a natural bridge.")

p2 = P("Abate Nero", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Abate Nero is one of Trento DOC's most respected artisan producers, working with high-altitude Chardonnay and Pinot Nero vineyards in the Trentino's most pristine alpine terroirs to produce traditional method wines of exceptional freshness.",
       reputation_narrative="Among Trento DOC's finest artisan producers, Abate Nero's Cuvée dell'Abate is one of Italy's most acclaimed non-Champagne sparkling wines for its extreme mineral precision.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Abate Nero Cuvée dell'Abate Brut Trento DOC", "wine_sparkling", p2, r, "Italy",
    subcategory="sparkling_white", price_tier="ultra_premium",
    description="Prestige cuvée from high-altitude Trentino Chardonnay and Pinot Nero; mineral, fine-bead and complex with apple blossom, toasted hazelnuts and alpine freshness from extended lees aging.")
if is_new:
    PAIR(prod, "Carpaccio di capriolo (venison carpaccio) with truffle and Parmesan", "complement", "established", "starter", "Alpine venison carpaccio with truffle finds the mineral complexity of Trentino's finest sparkling wine ideal.")
    PAIR(prod, "Grilled scampi with alpine herb butter", "complement", "established", "main", "Fine alpine mineral bead suits the sweetness of scampi with aromatic mountain herb butter.")
    PAIR(prod, "Trota al burro fuso (butter-basted trout) with sage", "complement", "classic", "main", "Alpine trout with sage butter is the quintessential Trentino companion for high-altitude traditional method.")
    PAIR(prod, "Mozzarella di bufala with San Marzano tomatoes and basil oil", "complement", "established", "casual", "Delicate buffalo mozzarella and fresh tomato find the fine mineral precision of alpine Trento DOC ideal.")

prod, is_new = PROD("Abate Nero Trento Brut Riserva", "wine_sparkling", p2, r, "Italy",
    subcategory="sparkling_white", price_tier="premium",
    description="Trentino Brut Riserva with extended lees aging; structured, mineral and complex with brioche, stone fruit and alpine freshness from the high-altitude porphyry and limestone vineyards.")
if is_new:
    PAIR(prod, "Risotto con funghi porcini e tartufo nero", "complement", "established", "main", "Brioche-mineral Riserva suits the earthy complexity of porcini risotto with black truffle shavings.")
    PAIR(prod, "Salmone al vapore con salsa verde e capperi", "complement", "established", "main", "Steamed salmon with salsa verde and capers finds the mineral-fresh structure of Trento Riserva ideal.")
    PAIR(prod, "Formaggio di Fossa with acacia honey and walnuts", "complement", "established", "cheese", "Pit-aged Italian cheese with honey and walnuts echoes the mineral-brioche complexity of the Riserva.")
    PAIR(prod, "Tagliatelle con ragù di cervo e tartufo", "complement", "suggested", "main", "Venison ragù with truffle pasta meets the structured mineral depth of this alpine traditional method wine.")

# ── ETNA DOC (Italy) ──────────────────────────────────────────────────────────
print("=== Etna DOC ===")
r = R("Etna DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Etna DOC",
      reputation_tier="prestigious",
      quality_trajectory="ascending",
      description="Italy's most exciting volcanic wine appellation on the slopes of Europe's most active volcano. Pre-phylloxera old-vine Nerello Mascalese produces reds of extraordinary mineral complexity, transparency and elegance, often compared to Burgundy. Carricante whites from the eastern slopes show remarkable tension and salinity. Altitude (600-1000m) combined with volcanic basalt creates unique terroir.",
      key_producers="Benanti, Cornelissen, Passopisciaro, Terre Nere",
      historical_context="Etna's vineyards were planted before phylloxera devastated mainland European viticulture in the 19th century. The island's volcanic soils provided protection, leaving centenarian and even bicentennial ungrafted vines. The modern Etna renaissance began with Andrea Franchetti (Passopisciaro) and Marc Cornelissen in the early 2000s, transforming the region's image from bulk wine source to Italy's most fashionable fine wine destination.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Outstanding volcanic vintage; Nerello Mascalese of extraordinary mineral depth and Burgundian elegance."),
    (2019, "very_good", "stable", "Well-balanced year on the volcano; wines of characteristic transparency and floral mineral character."),
    (2020, "very_good", "stable", "Good Etna vintage; high-altitude sites delivered exceptional freshness despite warm conditions."),
    (2021, "excellent", "rising", "Benchmark Etna vintage; Nerello Mascalese showing finest mineral precision and transparency in years."),
    (2022, "very_good", "stable", "Consistent quality across Etna's diverse contrade; volcanic mineral character throughout the range."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Terre Nere", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Marco de Grazia at Terre Nere pioneered the contrade (single-vineyard) concept for Etna, mapping the volcano's diverse basalt terroirs and producing wines that demonstrate how dramatically the expression of Nerello Mascalese changes across Etna's different slopes and altitudes.",
       reputation_narrative="Terre Nere is responsible for establishing Etna as Italy's most terroir-complex fine wine region. De Grazia's single-contrada wines are among Italy's most sought-after reds.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Terre Nere Etna Rosso Santo Spirito", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="Single-contrada Nerello Mascalese from the Santo Spirito volcanic terroir on Etna's north slope; ethereal, transparent and profoundly mineral with cherry, rose petal, iron and volcanic basalt precision.")
if is_new:
    PAIR(prod, "Arancino di carne (Sicilian rice croquette with meat ragù)", "complement", "classic", "casual", "Etna's regional snack — filled rice croquette — is the natural volcanic companion for this mineral red.")
    PAIR(prod, "Roasted pigeon with lentils and volcanic herbs", "complement", "classic", "main", "Delicate game bird on volcanic lentils mirrors the iron-mineral transparency of Santo Spirito Nerello.")
    PAIR(prod, "Pasta alla Norma (eggplant, tomato, salted ricotta)", "complement", "classic", "casual", "Sicily's most celebrated pasta dish with aubergine and salted ricotta is inseparable from volcanic Etna red.")
    PAIR(prod, "Grilled red tuna with sesame crust and ponzu", "complement", "established", "main", "Transparent, mineral Nerello's delicate iron character suits the meaty richness of Mediterranean bluefin tuna.")

prod, is_new = PROD("Terre Nere Etna Rosso", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Estate Etna Rosso from Nerello Mascalese across Terre Nere's north-slope contrade; vivid cherry, volcanic mineral, rose petal and elegant structure — an accessible entry to Etna's Burgundian style.")
if is_new:
    PAIR(prod, "Spaghetti con le sarde (pasta with sardines, pine nuts, raisins)", "complement", "classic", "main", "Sicily's most beloved pasta — sardines with sweet-savoury saffron-raisin — meets volcanic red elegantly.")
    PAIR(prod, "Grilled swordfish with capers, olive and tomato", "complement", "established", "main", "Sicilian swordfish preparation with Mediterranean garnishes suits the transparent mineral Etna red.")
    PAIR(prod, "Caponata (Sicilian sweet-sour aubergine)", "complement", "established", "casual", "Agrodolce aubergine with pine nuts and raisins finds the cherry-mineral lightness of Etna rosso ideal.")
    PAIR(prod, "Primo sale or Pecorino Siciliano with dried tomatoes", "complement", "established", "cheese", "Fresh or young Sicilian sheep cheese with sun-dried tomatoes mirrors the volcanic mineral character of Etna.")

p2 = P("Passopisciaro", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Andrea Franchetti at Passopisciaro was one of the modern Etna renaissance's founding pioneers, producing single-contrada Nerello Mascalese wines that opened the world's eyes to the volcano's extraordinary terroir potential.",
       reputation_narrative="Passopisciaro's Contrade wines — each named for a specific volcanic zone — are among Etna's most celebrated, demonstrating the extraordinary diversity of terroir expression on Mount Etna's slopes.",
       price_positioning="ultra_premium",
       authority_tier=1)

prod, is_new = PROD("Passopisciaro Contrada C Etna Rosso", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="Single-contrada Nerello Mascalese from Passopisciaro's Chiappemacine zone; powerful volcanic mineral, dark cherry and iron character from old ungrafted vines on basalt at 750m altitude.")
if is_new:
    PAIR(prod, "Wild boar with volcanic herbs and olive oil aglio e olio", "complement", "classic", "main", "Powerful volcanic Nerello handles wild game with its iron-mineral depth and old-vine structure.")
    PAIR(prod, "Braised rabbit alla Siciliana with olives, capers and rosemary", "complement", "classic", "main", "Sicilian rabbit braised with Pantelleria capers and olives matches the volcanic mineral intensity of Contrada C.")
    PAIR(prod, "Porcini mushroom ragù with maltagliati pasta", "complement", "established", "main", "Iron-mineral, earthy old-vine Nerello resonates deeply with porcini mushroom ragù and rough-cut pasta.")
    PAIR(prod, "Grilled lamb chops with Sicilian herbs and caponata", "complement", "established", "main", "Volcanic mineral structure of Passopisciaro suits lamb chops with the sweet-sour aubergine side.")

prod, is_new = PROD("Passopisciaro Etna Bianco Guardiola", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Passopisciaro's Etna Bianco from Carricante on the volcanic eastern slopes; tense, saline and mineral with citrus peel, volcanic ash character and extraordinary freshness from altitude on Etna's Milo terroir.")
if is_new:
    PAIR(prod, "Grilled spigola (sea bass) with olive oil and Sicilian salt", "complement", "classic", "main", "Saline, mineral volcanic Etna Bianco suits sea bass cooked with the island's simplest, finest ingredients.")
    PAIR(prod, "Crudo di gambero rosso di Mazara with lemon ice", "complement", "classic", "starter", "Sicily's prized red prawns served raw find the saline volcanic mineral of Etna Bianco a perfect match.")
    PAIR(prod, "Linguine con ricci di mare (sea urchin pasta)", "complement", "classic", "main", "Volcanic mineral Carricante's saline intensity is the ideal match for the ocean richness of sea urchin pasta.")
    PAIR(prod, "Grilled calamari with lemon oil and volcanic herb salt", "complement", "established", "main", "Clean, mineral volcanic white suits the sweetness of simply grilled squid with citrus and herbs.")

# ── CERASUOLO DI VITTORIA DOCG (Italy) ────────────────────────────────────────
print("=== Cerasuolo di Vittoria DOCG ===")
r = R("Cerasuolo di Vittoria DOCG", "Italy", "wine",
      designation_type="DOCG",
      designation_name="Cerasuolo di Vittoria DOCG",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Sicily's only DOCG appellation producing a unique blend of Nero d'Avola (minimum 50%) and Frappato from limestone soils in the province of Ragusa. The Nero d'Avola provides structure while Frappato adds floral fragrance, creating wines of remarkable freshness and elegance unusual for the hot Sicilian interior.",
      key_producers="COS, Arianna Occhipinti, Valle dell'Acate",
      historical_context="Cerasuolo di Vittoria's distinctive combination of Nero d'Avola and Frappato was already established by the 17th century. The appellation was awarded Sicily's first and only DOCG in 2005. The natural wine revolution led by COS and Arianna Occhipinti transformed the region from rustic relic to fashionable destination for wine lovers seeking authentic Sicilian character.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Frappato showed extraordinary floral fragrance alongside structured Nero d'Avola in ideal limestone conditions."),
    (2019, "very_good", "stable", "Good balance of freshness and structure; COS and Occhipinti showed exceptional results."),
    (2020, "very_good", "stable", "Warm but managed; wines of characteristic Sicilian warmth with retained Frappato freshness."),
    (2021, "excellent", "rising", "Outstanding vintage; benchmark Cerasuolo with the finest balance of Frappato floral character and Nero structure."),
    (2022, "very_good", "stable", "Consistent quality on limestone; Cerasuolo showing characteristic cherry-floral elegance."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("COS", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Giusto Occhipinti and Cirino Strano at COS were pioneers of both natural winemaking in Sicily and the amphora fermentation revival, producing wines from Nero d'Avola and Frappato that are vinified in terracotta pithos to produce wines of remarkable freshness and complexity.",
       reputation_narrative="COS is the defining producer of Cerasuolo di Vittoria, responsible for transforming the DOCG's international reputation through their amphora-fermented, minimal-intervention approach to Sicilian winemaking.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("COS Cerasuolo di Vittoria Classico", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Amphora-fermented Cerasuolo di Vittoria from COS; Nero d'Avola and Frappato from limestone soils, alive with cherry, violet and Sicilian herb character. Natural, mineral and distinctive — the defining wine of the DOCG.")
if is_new:
    PAIR(prod, "Pasta alla Norma with salted ricotta and basil", "complement", "classic", "casual", "Sicily's defining pasta and its salted ricotta finds the natural cherry-floral Cerasuolo ideal.")
    PAIR(prod, "Grilled triglie (red mullet) alla livornese", "complement", "established", "main", "Lighter, floral Cerasuolo suits the distinctive flavour of red mullet in tomato and caper sauce.")
    PAIR(prod, "Polpette di maiale con salsa di pomodoro e basilico", "complement", "classic", "casual", "Pork meatballs in fresh tomato-basil sauce find the cherry-herb freshness of Cerasuolo natural.")
    PAIR(prod, "Caciocavallo Ragusano with wild Sicilian oregano honey", "complement", "established", "cheese", "Stretched-curd Ragusa cheese with oregano honey echoes the volcanic-mineral and floral complexity of COS.")

prod, is_new = PROD("COS Pithos Rosso Sicilia", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="COS's iconic amphora-fermented Nero d'Avola and Frappato; deeply natural, mineral and complex with dark cherry, dried herbs and terracotta minerality from weeks of skin contact in ancient vessels.")
if is_new:
    PAIR(prod, "Agnello alla brace con aglio e rosmarino", "complement", "classic", "main", "Grilled lamb with garlic and rosemary meets the amphora-mineral depth of Pithos Rosso in a Sicilian classic.")
    PAIR(prod, "Involtini di maiale con capperi e olive", "complement", "established", "main", "Rolled pork with Pantelleria capers and olives finds the amphora-Nero d'Avola structure ideal.")
    PAIR(prod, "Grilled tuna belly (ventresca) with volcanic salt", "complement", "established", "main", "Fatty tuna belly and volcanic mineral salt are a natural Sicilian pairing for amphora-natural Nero d'Avola.")
    PAIR(prod, "Parmigiana di melanzane (Sicilian aubergine bake)", "complement", "classic", "casual", "The richest Sicilian vegetable bake — aubergine, tomato, mozzarella — needs the depth of Pithos Rosso.")

p2 = P("Arianna Occhipinti", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Giusto Occhipinti's niece Arianna is one of Italy's most celebrated natural winemakers, farming biodynamically in the Vittoria zone to produce Nero d'Avola and Frappato wines of extraordinary freshness, fragrance and authenticity.",
       reputation_narrative="Arianna Occhipinti's SP68 became one of Italy's most sought-after wines, representing a new generation's vision of what Sicilian wine could be — natural, fragrant, elegant and deeply tied to place.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Arianna Occhipinti SP68 Rosso Sicilia", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Arianna Occhipinti's iconic natural Nero d'Avola and Frappato from limestone; vivid cherry, violet, wild herbs and mineral freshness — one of Italy's most discussed and sought-after natural wines.")
if is_new:
    PAIR(prod, "Grilled ricciola (amberjack) with Pantelleria caper salsa", "complement", "established", "main", "Vivid cherry-violet Frappato suits amberjack with capers in a Sicilian pairing of sea and land.")
    PAIR(prod, "Pasta con broccoli siciliani e acciughe (pasta with broccoli and anchovy)", "complement", "classic", "casual", "Sicilian broccoli pasta with anchovy finds the natural cherry-mineral freshness of SP68 ideal.")
    PAIR(prod, "Arancine di riso al burro (butter rice balls)", "complement", "established", "casual", "The lighter Palermitan arancini variant finds the vivid freshness of Occhipinti's natural Frappato perfect.")
    PAIR(prod, "Pecorino Siciliano fresco with sun-dried tomatoes", "complement", "established", "casual", "Fresh Sicilian sheep cheese and sun-dried tomatoes mirror the cherry-herb freshness of natural SP68.")

prod, is_new = PROD("Arianna Occhipinti Cerasuolo di Vittoria Classico", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Arianna's Cerasuolo di Vittoria from biodynamic Nero d'Avola and Frappato on limestone; more structured than SP68, with deeper cherry, mineral and herbal complexity from the DOCG's finest soils.")
if is_new:
    PAIR(prod, "Coniglio all'agrodolce siciliana (sweet-sour rabbit)", "complement", "classic", "main", "Sicilian agrodolce rabbit with pine nuts and raisins finds Cerasuolo's cherry-herbal freshness ideal.")
    PAIR(prod, "Pork sausage with fennel seeds and roasted pepper", "complement", "established", "casual", "Sicilian fennel sausage and roasted peppers mirror the herbal complexity and cherry fruit of Cerasuolo.")
    PAIR(prod, "Melanzane sott'olio with capers and chilli", "complement", "established", "casual", "Preserved aubergine with capers and chilli heat is a natural Sicilian companion for biodynamic Cerasuolo.")
    PAIR(prod, "Ricotta al forno with honey and pistachios", "complement", "suggested", "dessert", "Baked ricotta with Sicilian honey and Bronte pistachios suits the floral freshness of Cerasuolo Classico.")

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
print("B139 complete.")
conn.close()
