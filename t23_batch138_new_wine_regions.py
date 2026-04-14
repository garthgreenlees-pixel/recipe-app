#!/usr/bin/env python3
"""B138 — Setúbal DOC (Portugal), Valpolicella DOC (Italy), Soave Classico DOC (Italy),
   Bardolino DOC (Italy), Lugana DOC (Italy)
All constraints verified from B136/B137:
  quality_descriptor: exceptional/excellent/very_good/good/average/challenging/poor
  price_trajectory: rising/stable/declining/speculative/unavailable
  reputation_tier: iconic/prestigious/respected/emerging/overlooked
  quality_trajectory: ascending/established/declining/emerging/rediscovering
  producer_type: winery (for all wine estates)
  meal_context: aperitif/amuse/starter/fish_course/main/cheese/pre_dessert/dessert/digestif/celebration/casual/any
  pairing_type: complement/contrast/bridge/cleanse/elevate
  confidence: classic/established/suggested/adventurous/experimental
  price_tier: ultra_premium/premium/mid_range/value/entry
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

# ── SETÚBAL DOC (Portugal) ────────────────────────────────────────────────────
print("=== Setúbal DOC ===")
r = R("Setúbal DOC", "Portugal", "wine",
      designation_type="DOC",
      designation_name="Setúbal DOC",
      reputation_tier="overlooked",
      quality_trajectory="ascending",
      description="Portugal's Setúbal Peninsula produces both dry table wines and the historic fortified Moscatel de Setúbal, one of the world's great dessert wines. Sandy soils and Atlantic influence create distinctive conditions south of Lisbon. The region is best known for its luscious, amber-hued Moscatel with extraordinary aging potential.",
      key_producers="José Maria da Fonseca, João Pires, Bacalhôa Vinhos",
      historical_context="Setúbal's wine history dates to Phoenician settlement at Arrábida. The Moscatel de Setúbal became famous across Europe in the 18th century, particularly the 20-year and 30-year aged versions. José Maria da Fonseca, founded 1834, is one of Portugal's oldest and most storied wine companies.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Ideal Atlantic conditions for Moscatel ripening; extraordinary sugar concentration with balancing acidity."),
    (2019, "very_good", "stable", "Good vintage for both table wines and Moscatel; characteristic aromatic intensity."),
    (2020, "good", "stable", "Warm conditions; Moscatel harvest benefited but some table wines lacked freshness."),
    (2021, "very_good", "stable", "Cool Atlantic influence maintained freshness; Moscatel of delicate floral intensity."),
    (2022, "excellent", "rising", "Outstanding ripening on sandy soils; Moscatel of benchmark aromatic richness."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("José Maria da Fonseca", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="Founded in 1834, José Maria da Fonseca is Portugal's oldest continuously operating wine company. Their Moscatel de Setúbal is produced through partial fermentation arrested by grape spirit, with extended skin contact for colour and complexity, then aged in old casks.",
       reputation_narrative="The defining producer of Moscatel de Setúbal, José Maria da Fonseca's aged expressions (20-year, 30-year) are among Portugal's most celebrated wines and among the world's great dessert wines.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("José Maria da Fonseca Moscatel de Setúbal 20 Anos", "wine_fortified", p1, r, "Portugal",
    subcategory="fortified_sweet", price_tier="ultra_premium",
    description="Twenty-year-old Moscatel de Setúbal; amber-mahogany, with extraordinary complexity of dried apricot, orange peel, toffee, roasted nut and spice. A benchmark Portuguese dessert wine of world stature.")
if is_new:
    PAIR(prod, "Tarte de amêndoa (almond tart) with clotted cream", "complement", "classic", "dessert", "Almond-caramel tart depth mirrors the roasted nut and toffee complexity of 20-year Moscatel de Setúbal.")
    PAIR(prod, "Arroz doce (Portuguese rice pudding with cinnamon)", "complement", "classic", "dessert", "Portugal's most beloved dessert — rice pudding with cinnamon — is the natural companion for aged Moscatel.")
    PAIR(prod, "Stilton or Gorgonzola with dried apricot", "contrast", "classic", "cheese", "Aged Moscatel's sweet complexity contrasts dramatically with blue cheese saltiness in a classic pairing.")
    PAIR(prod, "Crème brûlée with orange zest", "complement", "established", "dessert", "Caramel-orange notes in the Moscatel mirror the brûlée caramel and orange zest perfectly.")

prod, is_new = PROD("José Maria da Fonseca Periquita Reserva Setúbal", "wine_still", p1, r, "Portugal",
    subcategory="red", price_tier="mid_range",
    description="Historic Castelão-based red from the Setúbal Peninsula; warm, earthy and food-friendly with dark cherry and Mediterranean herb character from the sandy soils south of Lisbon.")
if is_new:
    PAIR(prod, "Carne de porco com amêijoas (pork with clams)", "complement", "classic", "main", "Portugal's most beloved pork-clam combination is a natural match for sandy-soil Castelão.")
    PAIR(prod, "Grilled sardines with tomato and olive oil salad", "complement", "classic", "casual", "Setúbal Peninsula sardines with summer tomato salad are the quintessential regional pairing.")
    PAIR(prod, "Açorda de bacalhau (salt cod bread soup)", "complement", "established", "main", "Warm, earthy Castelão red suits the garlic-coriander richness of Alentejo-style bacalhau açorda.")
    PAIR(prod, "Queijo de Azeitão sheep cheese", "complement", "established", "cheese", "Local runny sheep cheese from Azeitão across the Serra is the natural regional companion for Periquita.")

p2 = P("Bacalhôa Vinhos de Portugal", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Bacalhôa operates some of the Setúbal Peninsula's most important historic estates, combining traditional Portuguese varieties with international winemaking expertise to produce the region's most complete range of wines.",
       reputation_narrative="One of Portugal's largest quality producers, Bacalhôa's Setúbal estates are responsible for some of the region's most commercially successful and critically respected wines.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Bacalhôa Moscatel de Setúbal", "wine_fortified", p2, r, "Portugal",
    subcategory="fortified_sweet", price_tier="premium",
    description="Classic Moscatel de Setúbal from Bacalhôa; amber-gold, with floral orange blossom, apricot, honey and spice character. An accessible introduction to Setúbal's great fortified tradition.")
if is_new:
    PAIR(prod, "Pastel de nata (custard tart) with cinnamon", "complement", "classic", "dessert", "Portugal's national pastry with custard and cinnamon finds a perfect aromatic companion in Moscatel.")
    PAIR(prod, "Fresh figs with honeycomb and ricotta", "complement", "established", "dessert", "Floral, honey Moscatel character mirrors fresh fig sweetness with honeycomb depth and fresh cheese.")
    PAIR(prod, "Peach tarte tatin with vanilla ice cream", "complement", "established", "dessert", "Apricot and orange blossom Moscatel echoes the caramelised peach and vanilla combination.")
    PAIR(prod, "Brie de Meaux or triple-cream cheese with apricot jam", "complement", "suggested", "cheese", "Floral, honeyed Moscatel suits creamy brie's richness with the apricot jam echoing the wine's stone fruit.")

prod, is_new = PROD("Bacalhôa Catarina Branco Setúbal", "wine_still", p2, r, "Portugal",
    subcategory="white", price_tier="mid_range",
    description="Fresh, aromatic Setúbal Peninsula white from Moscatel, Chardonnay and Fernão Pires; tropical, citrus-fresh and food-friendly with Atlantic coastal influence.")
if is_new:
    PAIR(prod, "Gambas piri-piri with lemon and parsley", "complement", "classic", "casual", "Tropical-aromatic white cuts through chilli-prawn heat with refreshing citrus freshness.")
    PAIR(prod, "Grilled lúcio (pike-perch) with herbs and lemon", "complement", "established", "main", "Aromatic, Atlantic-fresh white suits freshwater fish with lemon-herb seasoning.")
    PAIR(prod, "Arroz de tamboril (monkfish rice)", "complement", "established", "main", "Portuguese monkfish rice benefits from the aromatic freshness of this Setúbal coastal white.")
    PAIR(prod, "Queijo fresco with tomato and olive oil", "complement", "suggested", "casual", "Fresh Portuguese cheese, tomato and olive oil find aromatic freshness in this light coastal white.")

# ── VALPOLICELLA DOC (Italy) ──────────────────────────────────────────────────
print("=== Valpolicella DOC ===")
r = R("Valpolicella DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Valpolicella DOC",
      reputation_tier="respected",
      quality_trajectory="established",
      description="Verona's most celebrated red wine appellation, ranging from the light, cherry-bright Valpolicella Classico to the profound Amarone della Valpolicella DOCG. Corvina, Corvinone and Rondinella grapes are dried (appassimento) to produce Amarone's concentration, while Ripasso (wine refermented on Amarone pomace) bridges the styles. The Classico zone on limestone-clay hills is the heartland.",
      key_producers="Allegrini, Dal Forno Romano, Quintarelli, Zenato",
      historical_context="Valpolicella wine culture dates to Roman times when Pliny praised the wines of Verona. The term 'Valpolicella' appears in documents from 1117. Amarone, now the appellation's most prestigious style, was accidentally discovered in the mid-20th century when a barrel of Recioto fermented dry. DOC status 1968.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Superb appassimento conditions; Amarone of exceptional concentration and fine tannin structure."),
    (2019, "very_good", "stable", "Well-balanced vintage; Classico wines of freshness and Amarone of depth and elegance."),
    (2020, "very_good", "stable", "Excellent Amarone from careful drying; ripe and concentrated with good structure."),
    (2021, "excellent", "rising", "Benchmark vintage for the full Valpolicella range; cool nights preserved freshness in Amarone."),
    (2022, "very_good", "stable", "Good ripeness with characteristic Valpolicella cherry and spice character throughout the range."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Allegrini", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="One of Valpolicella's most dynamic families, Allegrini has pioneered single-vineyard Classico wines and quality-focused Amarone production, championing the Classico sub-zone and indigenous varieties against the tide of international styles.",
       reputation_narrative="Allegrini's La Poja single-vineyard Corvina and La Grola demonstrate that Valpolicella's indigenous varieties can produce great wine beyond the Amarone style, while their Amarone remains one of the appellation's most reliable benchmarks.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Allegrini Amarone della Valpolicella Classico", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="Benchmark Amarone from Allegrini's Classico vineyards; rich, dried-fruit concentrated with cherry, chocolate, dried fig and spice from extended appassimento of Corvina and Corvinone. Enormous depth and 20+ year potential.")
if is_new:
    PAIR(prod, "Brasato al Barolo (Verona style — braised beef in Amarone)", "complement", "classic", "main", "Amarone della Valpolicella braised beef is the definitive regional pairing — wine and food are one.")
    PAIR(prod, "Wild boar ragù with pappardelle and aged Pecorino", "complement", "classic", "main", "Dark game ragù and dried-fruit Amarone concentration create the richest of Italian pasta pairings.")
    PAIR(prod, "Pigeon with dried cherry, cacao and game jus", "complement", "established", "main", "Game bird and dried cherry sauce mirror Amarone's own dried cherry-cacao complexity beautifully.")
    PAIR(prod, "Aged Parmigiano-Reggiano 36-month with balsamic", "complement", "established", "cheese", "Long-aged Parmesan crystals and traditional balsamic vinegar meet the concentrated depth of Amarone.")

prod, is_new = PROD("Allegrini Palazzo della Torre Valpolicella Ripasso", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="premium",
    description="Valpolicella Ripasso refermented on Amarone pomace; structured, cherry-rich and complex with dried fruit, spice and the characteristic Ripasso richness between Classico and Amarone.")
if is_new:
    PAIR(prod, "Risotto all'Amarone with aged Parmesan", "complement", "classic", "main", "Amarone-braised risotto and its wine-reduction richness find the perfect partner in Ripasso's structure.")
    PAIR(prod, "Grilled tagliata with rosemary and rocket", "complement", "classic", "main", "Sliced rib-eye with rocket and Parmigiano shavings is the Italian steakhouse classic for Ripasso.")
    PAIR(prod, "Lasagne al forno with beef and béchamel", "complement", "established", "main", "Rich baked pasta with beef and cream meets Ripasso's dried-fruit spice and structured cherry.")
    PAIR(prod, "Pecorino Romano with Calabrian honey", "complement", "established", "cheese", "Sharp aged sheep cheese with southern Italian honey finds resonance in Ripasso's dried fruit complexity.")

p2 = P("Zenato", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Zenato is one of Valpolicella's most respected traditional producers, working with old Classico vineyards and using extended traditional vinification to produce Amarone and Valpolicella of genuine depth and age-worthiness.",
       reputation_narrative="Zenato's Riserva Sergio Zenato Amarone is one of the appellation's most decorated and long-lived wines, a benchmark for understanding the style's ultimate potential.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Zenato Amarone della Valpolicella Classico Riserva", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="ultra_premium",
    description="Icon Amarone from Zenato's best Classico parcels; profound, age-worthy and complex with dried plum, dark chocolate, leather, tobacco and Mediterranean spice. Requires a decade of cellaring.")
if is_new:
    PAIR(prod, "Ossibuco alla milanese with gremolata and saffron risotto", "complement", "classic", "main", "Braised veal shank and saffron risotto require the depth and structure of a serious Amarone Riserva.")
    PAIR(prod, "Faisán asado (roast pheasant) with mushroom and Madeira", "complement", "established", "main", "Game bird with mushroom-fortified wine sauce finds its structural equal in aged Amarone Riserva.")
    PAIR(prod, "Tartufo nero (black truffle) and beef carpaccio", "complement", "established", "starter", "Black truffle and cured beef rawness find the mineral-depth frame of aged Amarone Riserva.")
    PAIR(prod, "Grana Padano 24-month with acacia honey", "complement", "established", "cheese", "Aged Italian hard cheese crystals and floral honey contrast the dried-fruit intensity of Amarone Riserva.")

prod, is_new = PROD("Zenato Valpolicella Classico Superiore", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Classic Valpolicella from the Classico heartland; bright cherry, wild herbs and limestone mineral character with the freshness and lift that defines authentic Classico style.")
if is_new:
    PAIR(prod, "Pasta e fagioli (pasta and bean soup)", "complement", "classic", "casual", "Bright, cherry-fresh Classico is the natural Veronese companion for this hearty pasta and bean soup.")
    PAIR(prod, "Pizza margherita with buffalo mozzarella and basil", "complement", "classic", "casual", "Light, aromatic Valpolicella Classico is the quintessential pizza pairing — Italian comfort at its best.")
    PAIR(prod, "Grilled polpettine (Italian meatballs) with tomato sauce", "complement", "established", "casual", "Bright cherry and herb character of Classico mirrors the tomato-herb sauce of classic meatballs.")
    PAIR(prod, "Sopressa Vicentina (Veneto salumi) with grissini", "complement", "established", "casual", "Regional Veneto cured sausage finds its natural light wine companion in fresh Valpolicella Classico.")

# ── SOAVE CLASSICO DOC (Italy) ────────────────────────────────────────────────
print("=== Soave Classico DOC ===")
r = R("Soave Classico DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Soave Classico DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Verona's classic white wine appellation producing Garganega-dominant wines from volcanic basalt soils in the historic Classico zone. Long dismissed as mass-market neutral, the Classico zone has undergone a quality revolution revealing wines of genuine mineral depth, floral aromatics and age-worthiness that rival great Burgundy whites.",
      key_producers="Pieropan, Gini, Prà, Coffele",
      historical_context="Soave's reputation peaked in the 1970s as one of Italy's most exported wines, then collapsed under the weight of overproduction. The revival of the Classico zone from the 1990s, led by Pieropan and Gini, has restored the appellation's credibility through strict quality standards and old-vine volcanic terroir expression.")
for yr, qd, pt, sn in [
    (2018, "excellent", "rising", "Volcanic basalt Garganega showed exceptional mineral depth and aromatic complexity."),
    (2019, "very_good", "stable", "Well-balanced vintage; Soave Classico of the characteristic floral-almond freshness."),
    (2020, "very_good", "stable", "Good structure and mineral character; top Classico wines showing excellent aging potential."),
    (2021, "excellent", "rising", "Benchmark vintage for Soave Classico quality revival; wines of extraordinary freshness and mineral precision."),
    (2022, "very_good", "stable", "Consistent quality from volcanic basalt; Garganega of genuine depth and aromatic complexity."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Pieropan", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Leonildo Pieropan was the founding champion of Soave Classico quality, insisting on old-vine Garganega from the volcanic Classico hills at a time when the rest of the appellation chased production volume. His single-vineyard La Rocca remains the reference point for world-class Soave.",
       reputation_narrative="Pieropan is Soave Classico's defining estate, responsible almost singlehandedly for the appellation's quality reputation. La Rocca demonstrates that Garganega on volcanic basalt can produce one of Italy's great whites.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Pieropan Soave Classico La Rocca", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Benchmark single-vineyard Soave from old Garganega on volcanic basalt; profound mineral depth, almond blossom, stone fruit and saline character with extraordinary longevity for a Soave white.")
if is_new:
    PAIR(prod, "Grilled branzino with lemon, capers and olive oil", "complement", "classic", "main", "Volcanic mineral Soave is the definitive Italian companion for whole grilled sea bass with lemon.")
    PAIR(prod, "Risotto al limone con gamberi (lemon prawn risotto)", "complement", "classic", "main", "Mineral, floral Garganega suits the delicate cream-citrus richness of Veronese prawn risotto.")
    PAIR(prod, "Vitello tonnato (veal with tuna sauce)", "complement", "classic", "starter", "Soave Classico's mineral freshness is the traditional northern Italian companion for this classic antipasto.")
    PAIR(prod, "Burrata with heirloom tomatoes and basil oil", "complement", "established", "casual", "Mineral, floral Soave suits the creaminess of burrata and the acidity of ripe summer tomatoes.")

prod, is_new = PROD("Pieropan Soave Classico", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Estate Soave Classico from Pieropan's volcanic Classico vineyards; floral, mineral and precise with almond, white peach and citrus blossom character from Garganega on basalt.")
if is_new:
    PAIR(prod, "Fritto misto di mare (mixed seafood fry)", "complement", "classic", "casual", "Classic Verona-Venice fritto misto of calamari, prawns and fish is the natural companion for Soave Classico.")
    PAIR(prod, "Asparagus di Bassano with fried egg and Parmesan", "complement", "classic", "casual", "Veneto's prized white asparagus with egg and Parmesan finds its ideal pairing in mineral Soave.")
    PAIR(prod, "Carpaccio di branzino con erbe e limone", "complement", "established", "starter", "Raw sea bass with herb-lemon dressing is lifted by the mineral precision of Soave Classico.")
    PAIR(prod, "Monte Veronese or Asiago Pressato cheese", "complement", "established", "cheese", "Mild Veneto cow's milk cheeses find natural resonance with the floral mineral character of Soave Classico.")

p2 = P("Gini", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Claudio and Sandro Gini farm old-vine Garganega in Soave's Classico heartland, producing wines that showcase the volcanic basalt terroir through minimal intervention and extended lees aging.",
       reputation_narrative="Gini's Salvarenza Vecchie Vigne is one of Soave Classico's most prized single-vineyard wines, demonstrating the aging potential of old-vine Garganega from the best volcanic sites.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Gini Salvarenza Vecchie Vigne Soave Classico", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Old-vine Soave from Garganega vines over 70 years on volcanic basalt; profound mineral depth, smoky, complex and textured with stone fruit and almond character requiring years to fully express itself.")
if is_new:
    PAIR(prod, "Risotto ai funghi porcini con tartufo bianco", "complement", "established", "main", "Mineral, smoky old-vine Soave is the ideal white wine for truffle-porcini risotto of the Veneto.")
    PAIR(prod, "Baccalà mantecato (creamed salt cod) on polenta", "complement", "classic", "casual", "Venice's classic whipped salt cod on grilled polenta requires a white of this mineral depth and texture.")
    PAIR(prod, "Grilled cuttlefish with herb oil and lemon", "complement", "established", "main", "Smoky, complex Soave from volcanic basalt suits the delicate sweetness of grilled cuttlefish.")
    PAIR(prod, "Aged Asiago d'Allevo cheese with honeycomb", "complement", "established", "cheese", "Aged Veneto sheep-cow cheese with honeycomb sweetness finds a match in the complex old-vine Soave.")

prod, is_new = PROD("Gini Col Foscarin Soave Classico", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Soave from basalt; elegant, floral and mineral with the characteristic Gini freshness and depth from volcanic Classico terroir.")
if is_new:
    PAIR(prod, "Tagliolini al granchio (crab pasta with herbs)", "complement", "classic", "main", "Fresh crab pasta with parsley finds the perfect mineral-floral frame in elegant basalt Soave.")
    PAIR(prod, "Zuppa di vongole (Veneto clam soup)", "complement", "classic", "main", "Briny clam soup with white wine and herbs is the traditional Veneto pairing for elegant Soave.")
    PAIR(prod, "Mozzarella in carrozza (fried mozzarella in bread)", "complement", "established", "casual", "Light, floral Soave cuts through the fried cheese richness with mineral freshness.")
    PAIR(prod, "Sarde in saor (Venetian sweet-sour sardines)", "complement", "established", "casual", "The sweet-sour agrodolce of Venetian marinated sardines finds balance in mineral Soave's freshness.")

# ── BARDOLINO DOC (Italy) ─────────────────────────────────────────────────────
print("=== Bardolino DOC ===")
r = R("Bardolino DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Bardolino DOC",
      reputation_tier="overlooked",
      quality_trajectory="ascending",
      description="The lighter, fresher face of Verona's reds, produced from Corvina, Corvinone and Rondinella on glacial moraine soils around Lake Garda's eastern shore. Bardolino at its best is vivid, sour-cherry bright and refreshing — a wine of elegance rather than power. The Chiaretto rosé is one of Italy's most distinctive.",
      key_producers="Guerrieri Rizzardi, Corte Gardoni, Zeni",
      historical_context="Bardolino is one of northeast Italy's oldest documented wine regions, with viticulture recorded since the 13th century around the medieval lakeside village of Bardolino. The glacial soils of Lake Garda's eastern shore, combined with the lake's moderating influence, produce wines of remarkable freshness. DOC 1968.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Ideal lake conditions; Bardolino Classico of vivid cherry freshness and elegant mineral character."),
    (2020, "very_good", "stable", "Good balance of freshness and fruit; Chiaretto rosé of benchmark delicacy."),
    (2021, "excellent", "rising", "Outstanding vintage; Bardolino showing characteristic lightness with unexpected mineral depth."),
    (2022, "very_good", "stable", "Consistent quality; lake influence maintained freshness in what was a warm year regionally."),
    (2023, "excellent", "rising", "Benchmark lake vintage; Chiaretto of extraordinary delicacy and Classico of vivid cherry precision."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Guerrieri Rizzardi", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Historic estate around Lake Garda farming Bardolino and Soave from glacial moraine soils, producing wines that celebrate the lake's moderating influence and glacial terroir with elegant, food-focused wines.",
       reputation_narrative="One of Bardolino's historic family estates, Guerrieri Rizzardi demonstrates that the region can produce wines of genuine complexity and elegance beyond the simple fruit-forward style.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Guerrieri Rizzardi Tacchetto Bardolino Classico", "wine_still", p1, r, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Single-vineyard Bardolino Classico from glacial moraine above Lake Garda; vivid sour cherry, wild herbs and mineral freshness with characteristic Bardolino light body and refreshing lift.")
if is_new:
    PAIR(prod, "Pizza with prosciutto crudo, rocket and Parmesan shavings", "complement", "classic", "casual", "Light, cherry-bright Bardolino is the Italian lakeside companion for this Roman-style thin pizza.")
    PAIR(prod, "Risotto al lago (lake fish risotto with herbs)", "complement", "classic", "main", "Lake Garda fish risotto with fresh herbs is the quintessential Bardolino pairing from the region.")
    PAIR(prod, "Pasta al pomodoro fresco with basil and Parmesan", "complement", "classic", "casual", "Bright cherry Corvina and fresh tomato pasta are a simple, perfect pairing of Italian lakeside cuisine.")
    PAIR(prod, "Bresaola della Valtellina with olive oil and lemon", "complement", "established", "casual", "Cured beef bresaola with lemon finds the light, fresh cherry character of Bardolino Classico ideal.")

prod, is_new = PROD("Guerrieri Rizzardi Chiaretto Rosa di Bardolino", "wine_still", p1, r, "Italy",
    subcategory="rosé", price_tier="mid_range",
    description="Classic Bardolino Chiaretto rosé from Corvina on glacial moraine; pale coral-pink, delicate and fresh with sour cherry, rose petal and mineral freshness from Lake Garda's influence.")
if is_new:
    PAIR(prod, "Insalata di mare (seafood salad with olive oil and lemon)", "complement", "classic", "casual", "Delicate lakeside rosé suits the mixed seafood salad with its citrus-olive freshness perfectly.")
    PAIR(prod, "Grilled gamberi with lemon and parsley", "complement", "classic", "casual", "Pale Chiaretto's delicate cherry-citrus freshness is an elegant match for simply grilled prawns.")
    PAIR(prod, "Vitello tonnato with capers and anchovy", "complement", "established", "starter", "Delicate rosé freshness suits the rich tuna-mayo sauce over cold veal without overpowering.")
    PAIR(prod, "Caprese salad with heirloom tomatoes and basil", "complement", "established", "casual", "Rose petal freshness of Chiaretto is a charming companion for summer tomato and buffalo mozzarella.")

p2 = P("Corte Gardoni", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Piccoli family at Corte Gardoni produces wines of exceptional freshness and terroir transparency from Bardolino's glacial moraine soils, working with both Corvina-based reds and the delicate Chiaretto rosé.",
       reputation_narrative="Corte Gardoni's Bardolino wines are consistently among the appellation's finest, demonstrating that the glacial lake-influenced terroir can produce wines of genuine mineral character and lasting elegance.",
       price_positioning="mid_range",
       authority_tier=1)

prod, is_new = PROD("Corte Gardoni Bardolino Classico", "wine_still", p2, r, "Italy",
    subcategory="red", price_tier="mid_range",
    description="Authentic Bardolino from Corvina, Rondinella and Molinara on glacial moraine; vibrant sour cherry, herbs and mineral freshness with the characteristic light elegance of Lake Garda's red wine.")
if is_new:
    PAIR(prod, "Carpaccio di manzo with truffle oil and Parmigiano", "complement", "established", "starter", "Light Bardolino's freshness suits raw beef carpaccio without overpowering the delicate flavours.")
    PAIR(prod, "Pasta al ragù bianco (white meat ragù)", "complement", "established", "casual", "Pale veal ragù without tomato is the ideal light Italian companion for cherry-bright Bardolino.")
    PAIR(prod, "Grilled trota di lago (lake trout) with herbs", "complement", "classic", "main", "Lake Garda trout and Bardolino's lakeside freshness are an authentic regional pairing.")
    PAIR(prod, "Salumi misti with giardiniera and grissini", "complement", "classic", "casual", "Italian mixed cured meats and pickled vegetables are natural companions for fresh, light Bardolino.")

prod, is_new = PROD("Corte Gardoni Chiaretto di Bardolino", "wine_still", p2, r, "Italy",
    subcategory="rosé", price_tier="mid_range",
    description="Benchmark Bardolino Chiaretto from the Piccoli family; ethereally pale, delicate and precise with sour cherry blossom, mineral freshness and the signature lake-influence elegance.")
if is_new:
    PAIR(prod, "Crudo di branzino with citrus dressing", "complement", "classic", "starter", "Ethereally pale Chiaretto suits raw sea bass with citrus with delicate precision and mineral freshness.")
    PAIR(prod, "Prosciutto di San Daniele with cantaloupe melon", "complement", "classic", "casual", "The Italian summer classic of prosciutto and melon meets the delicate cherry-floral Chiaretto.")
    PAIR(prod, "Zucchini blossoms stuffed with ricotta and herbs", "complement", "established", "casual", "Floral, delicate Chiaretto echoes the squash blossom's gentle character with fresh herb stuffing.")
    PAIR(prod, "Grilled spiedini di mare (seafood skewers)", "complement", "established", "casual", "Mixed seafood skewers with the mineral lake freshness of pale Bardolino Chiaretto — Italian perfection.")

# ── LUGANA DOC (Italy) ────────────────────────────────────────────────────────
print("=== Lugana DOC ===")
r = R("Lugana DOC", "Italy", "wine",
      designation_type="DOC",
      designation_name="Lugana DOC",
      reputation_tier="respected",
      quality_trajectory="ascending",
      description="Lake Garda's white wine appellation producing Trebbiano di Lugana (Turbiana) from unique clay-limestone soils on the lake's southern shore between Verona and Brescia. Lugana produces wines of remarkable texture, mineral depth and aging potential — among northern Italy's most distinctive whites.",
      key_producers="Zenato, Ca' dei Frati, Ottella",
      historical_context="Lugana's unique clay-limestone moraine soils — deposited by glaciers and compressed over millennia — give Trebbiano di Lugana (Turbiana) a complexity unavailable from other soils. The DOC was established 1967 but quality revolution began in the 1990s. Today Lugana is among Italy's fastest-growing and most respected white wine DOCs.")
for yr, qd, pt, sn in [
    (2019, "excellent", "rising", "Clay-limestone Turbiana showed exceptional mineral depth and aromatic complexity."),
    (2020, "very_good", "stable", "Good vintage; Lugana of characteristic texture and stone fruit mineral character."),
    (2021, "excellent", "rising", "Benchmark Lugana vintage; wines of extraordinary mineral precision and aging potential."),
    (2022, "very_good", "stable", "Consistent quality; Lugana Superiore and Riserva showing excellent aging structure."),
    (2023, "excellent", "rising", "Outstanding clay-limestone vintage; Turbiana of exceptional freshness and mineral depth."),
]:
    VIN(r, yr, qd, pt, sn)

p1 = P("Ca' dei Frati", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Dal Cero family at Ca' dei Frati is the leading ambassador of Lugana's quality potential, producing wines from Turbiana on the unique compressed clay-limestone soils that express the appellation's singular mineral character.",
       reputation_narrative="Ca' dei Frati's I Frati Lugana and Brolettino Riserva are benchmarks for the appellation's full quality range, demonstrating that Turbiana from clay-limestone can rival northern Italy's finest whites.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Ca' dei Frati Brolettino Lugana Riserva", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Benchmark Lugana Riserva from clay-limestone; profound, aged Turbiana with honeyed stone fruit, almond, mineral depth and waxy texture that develops extraordinary complexity over 5-10 years.")
if is_new:
    PAIR(prod, "Risotto al pesce persico con burro e salvia (lake perch risotto)", "complement", "classic", "main", "Lake Garda perch risotto with butter and sage is the quintessential Lugana Riserva pairing.")
    PAIR(prod, "Grilled turbot with herb butter and Lugana wine sauce", "complement", "classic", "main", "Complex, aged Turbiana handles the sweet richness of turbot with mineral precision and textural depth.")
    PAIR(prod, "Capesante (scallops) gratinate with herbs and lemon", "complement", "established", "main", "Gratin scallops with herb breadcrumbs find the mineral-almond texture of Lugana Riserva ideal.")
    PAIR(prod, "Aged Monte Veronese d'Allevo with acacia honey", "complement", "established", "cheese", "Complex, aged Italian cow's milk cheese with honey echoes the almond-honey complexity of Riserva.")

prod, is_new = PROD("Ca' dei Frati I Frati Lugana", "wine_still", p1, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Flagship Lugana from Ca' dei Frati's clay-limestone Turbiana; fresh, mineral and aromatic with stone fruit, almond blossom and characteristic Lugana texture and depth.")
if is_new:
    PAIR(prod, "Fritto misto di lago (fried lake fish and vegetables)", "complement", "classic", "casual", "Lake Garda's classic fried fish and vegetable platter finds its natural white wine companion in Lugana.")
    PAIR(prod, "Grilled persico (lake perch) with lemon and sage", "complement", "classic", "main", "Lake perch with lemon-sage is the traditional Garda companion for Lugana — a quintessential regional pairing.")
    PAIR(prod, "Carpaccio di salmone con limone e erbe fresche", "complement", "established", "starter", "Raw salmon with lemon-herb dressing finds mineral precision and stone fruit freshness in Lugana.")
    PAIR(prod, "Stracchino or Crescenza fresh cheese with truffle honey", "complement", "established", "cheese", "Fresh, runny Italian cheese with truffle honey finds the mineral-almond texture of Lugana ideal.")

p2 = P("Ottella", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="The Montresor family at Ottella farms organically on Lugana's clay-limestone soils, producing single-vineyard and biologically certified Lugana that showcase the unique geological character of this compressed glacial moraine terroir.",
       reputation_narrative="Ottella's Le Creete single-vineyard Lugana is one of the appellation's most distinctive and mineral expressions, demonstrating the power of clay-limestone terroir over Turbiana.",
       price_positioning="premium",
       authority_tier=1)

prod, is_new = PROD("Ottella Le Creete Lugana", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="ultra_premium",
    description="Single-vineyard organic Lugana from clay-limestone; intensely mineral, saline and textured Turbiana with stone fruit, lime zest and a chalky mineral finish that ages magnificently.")
if is_new:
    PAIR(prod, "Zuppa di pesce alla gardesana (Garda-style fish soup)", "complement", "classic", "main", "Mineral, complex Lugana blanc is the authentic companion for Lake Garda's mixed fish soup tradition.")
    PAIR(prod, "Linguine alle vongole veraci with white wine and parsley", "complement", "classic", "main", "Mineral, saline Turbiana mirrors the ocean intensity of vongole veraci with its chalky precision.")
    PAIR(prod, "Grilled branzino in sale (salt-crusted sea bass)", "complement", "established", "main", "Salt-crust baking amplifies the sea mineral intensity that Lugana Le Creete mirrors perfectly.")
    PAIR(prod, "Capellini with sea urchin and lemon zest", "complement", "established", "main", "Saline, mineral Lugana is the ideal Italian white for the ocean intensity of sea urchin pasta.")

prod, is_new = PROD("Ottella Molceo Lugana Riserva", "wine_still", p2, r, "Italy",
    subcategory="white", price_tier="premium",
    description="Organic Lugana Riserva from clay-limestone moraine; aged on fine lees with texture, almond complexity and the characteristic mineral precision of Ottella's biological farming approach.")
if is_new:
    PAIR(prod, "Asparagus with prosciutto crudo, poached egg and Parmesan", "complement", "established", "starter", "Lees-aged Lugana texture suits the asparagus-ham-egg combination with mineral precision.")
    PAIR(prod, "Baccalà alla Vicentina (creamed salt cod with polenta)", "complement", "classic", "main", "Veneto's classic creamed salt cod and polenta requires a white of this mineral depth and textural richness.")
    PAIR(prod, "Risotto ai frutti di mare (mixed seafood risotto)", "complement", "established", "main", "Lees texture and mineral depth of Riserva Lugana suit the mixed seafood richness of this classic.")
    PAIR(prod, "Grana Padano 18-month with fig mostarda", "complement", "established", "cheese", "Aged Italian cheese with fig mostarda finds the mineral-lees complexity of Lugana Riserva ideal.")

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
print("B138 complete.")
conn.close()
