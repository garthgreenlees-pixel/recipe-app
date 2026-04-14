#!/usr/bin/env python3
"""B146 — Santorini PDO, Nemea PDO, Naoussa PDO, Muscat of Samos PDO, Mantinia PDO (Greece)"""
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

# ── 1. Santorini PDO ─────────────────────────────────────────────────────────
print("=== Santorini PDO ===")
r1 = R("Santorini PDO", "Greece", "wine",
        designation_type="PDO", designation_name="Santorini",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Santorini produces some of the world's most distinctive white wines from ancient Assyrtiko vines grown in the volcanic pumice soils of the caldera. The island's extreme conditions — fierce Aegean winds, drought, and volcanic ash — stress the vines to produce grapes of extraordinary concentration, acidity, and mineral intensity. The traditional basket-shaped vines (kouloura) protect grapes from the wind and preserve moisture.",
        key_producers="Domaine Sigalas, Gaia Wines, Hatzidakis Winery, Estate Argyros",
        historical_context="Wine has been made on Santorini for over 3,000 years, predating the Minoan eruption of the 16th century BC that formed the caldera. The ancient Vinsanto (Vin Santo-style sweet wine) was traded across the Byzantine Empire. The island's modern wine renaissance began in the 1990s with producers like Domaine Sigalas elevating Assyrtiko to global recognition.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r1, yr, qd, pt)

p1a = P("Domaine Sigalas", "winery", r1, "Greece",
         production_philosophy="terroir_expression",
         philosophy_description="Paris Sigalas is the foremost champion of Assyrtiko, producing wines from old volcanic-ash bush vines that have brought Santorini to global attention. His barrel-fermented Kavalieros is widely considered the island's greatest wine.",
         reputation_narrative="Domaine Sigalas is Santorini's most internationally respected producer, with Paris Sigalas's obsessive focus on Assyrtiko's mineral potential having defined the variety's world-class credentials. His wines appear on the lists of the finest restaurants globally.",
         price_positioning="premium")

prod1a1, new1 = PROD("Sigalas Assyrtiko Santorini PDO", "wine_still", p1a, r1, "Greece",
                      subcategory="Assyrtiko", price_tier="mid_range",
                      description="The estate Assyrtiko from ancient Santorini bush vines, capturing the variety's signature electric acidity, citrus peel, and saline volcanic minerality. Aged in stainless steel to preserve freshness, this wine demonstrates why Assyrtiko is considered one of the world's great white varieties.")
if new1:
    PAIR(prod1a1, "Grilled octopus with lemon, olive oil, and dried oregano", "complement", "classic", "starter", "The definitive Santorini pairing: the wine's saline minerality and citrus acidity mirror the octopus's oceanic character; dried oregano adds an aromatic bridge while lemon amplifies the wine's citrus.")
    PAIR(prod1a1, "Sea bream in salt crust with herbs and lemon", "complement", "classic", "fish_course", "Assyrtiko's electric acidity and salt-mineral character are ideal for delicate fish in salt crust; the wine's precision lifts the fish's sweetness while the herbs create an aromatic connection.")
    PAIR(prod1a1, "Santorini fava (yellow split pea dip) with capers and onion", "complement", "classic", "starter", "A profound local pairing: Santorini fava's creamy earthiness and the wine's volcanic minerality are two expressions of the same terroir; capers and onion add the acidity that bridges both.")
    PAIR(prod1a1, "Oysters on the half shell with mignonette", "complement", "classic", "aperitif", "Assyrtiko's saline mineral depth makes it one of the world's great oyster wines; mignonette's vinegar sharpens the wine's acidity while amplifying the oyster's brine.")

prod1a2, new2 = PROD("Sigalas Kavalieros Barrel Assyrtiko Santorini", "wine_still", p1a, r1, "Greece",
                      subcategory="Assyrtiko", price_tier="premium",
                      description="From the single Kavalieros vineyard, fermented and aged in French oak barrels, this is Santorini's most complex dry white wine. The barrel adds hazelnut and toast while amplifying Assyrtiko's natural mineral depth; the result is a wine of extraordinary tension and longevity.")
if new2:
    PAIR(prod1a2, "Seared scallops with cauliflower purée and truffle vinaigrette", "complement", "classic", "fish_course", "The barrel-fermented complexity and mineral depth of Kavalieros are equipped to handle truffle; scallop's sweetness is complemented by the wine's richness while cauliflower provides the earthy bridge.")
    PAIR(prod1a2, "Lobster thermidor with tarragon and Gruyère", "complement", "established", "main", "Kavalieros's hazelnut oak and volcanic mineral character create a profound match for lobster thermidor; Gruyère's nuttiness echoes the wine's oak while tarragon adds aromatic lift.")
    PAIR(prod1a2, "White asparagus with Hollandaise and bottarga", "complement", "established", "starter", "The wine's mineral depth and barrel complexity handle asparagus and Hollandaise's richness; bottarga's umami salinity amplifies the wine's volcanic character.")
    PAIR(prod1a2, "Aged Graviera cheese with honey and walnut", "complement", "classic", "cheese", "Graviera is the cheese of the Greek islands; the wine's barrel complexity and volcanic mineral depth find perfect resonance with the aged sheep's milk cheese, while honey bridges the wine's citrus core.")

p1b = P("Estate Argyros", "winery", r1, "Greece",
         production_philosophy="terroir_expression",
         philosophy_description="Estate Argyros is one of Santorini's largest private vineyards, with some of the island's oldest vines. Their Assyrtiko Single Vineyard and Vinsanto are benchmarks for the island's two most iconic wine styles.",
         reputation_narrative="Argyros's pre-eminence in Vinsanto production has brought international attention to Santorini's ancient sweet wine tradition, while their dry Assyrtiko demonstrates the variety's full range from fresh through to barrel-aged complexity.",
         price_positioning="premium")

prod1b1, new3 = PROD("Argyros Assyrtiko Santorini PDO Single Vineyard", "wine_still", p1b, r1, "Greece",
                      subcategory="Assyrtiko", price_tier="premium",
                      description="From one of Santorini's oldest vine blocks, this single-vineyard Assyrtiko offers greater concentration and mineral depth than the estate bottling, with lemon pith, white peach, and the distinctive saline mineral finish of ancient volcanic-ash vines.")
if new3:
    PAIR(prod1b1, "Grilled tuna with capers, olives, and tomato confit", "complement", "established", "main", "The wine's concentration and mineral depth match tuna's meaty richness; capers and olives add the briny Mediterranean notes that echo the wine's saline character.")
    PAIR(prod1b1, "Sea urchin pasta with lemon and olive oil", "complement", "classic", "main", "Assyrtiko's saline minerality is one of the few wines that can embrace sea urchin's intense oceanic quality; lemon amplifies the wine's citrus while pasta softens the urchin's intensity.")
    PAIR(prod1b1, "Grilled langoustines with garlic and herb butter", "complement", "classic", "fish_course", "The wine's mineral precision and citrus acidity frame langoustine's sweetness perfectly; garlic butter adds the savoury richness that the wine's structure can absorb.")
    PAIR(prod1b1, "Fresh sheep's milk cheese with thyme honey and pistachios", "complement", "established", "cheese", "Greek fresh cheese and Assyrtiko is a local classic; thyme honey bridges the wine's mineral citrus while pistachios add the savoury-green note that completes the pairing.")

prod1b2, new4 = PROD("Argyros Vinsanto Santorini PDO", "wine_still", p1b, r1, "Greece",
                      subcategory="Assyrtiko", price_tier="ultra_premium",
                      description="The ancient sweet wine of Santorini, made from sun-dried Assyrtiko and Aidani grapes aged for many years in small oak casks. Vinsanto is among the world's great dessert wines: concentrated dried apricot, coffee, caramel, and volcanic mineral with extraordinary acidity that prevents cloying sweetness. Can age for decades.")
if new4:
    PAIR(prod1b2, "Walnut baklava with orange blossom syrup and pistachios", "complement", "classic", "dessert", "The wine's caramel and dried-fruit concentration is the ideal partner for baklava's honey richness; orange blossom mirrors the wine's floral notes while walnut echoes its roasted depth.")
    PAIR(prod1b2, "Aged Pecorino with dried fig and dark chocolate", "complement", "classic", "cheese", "Vinsanto's coffee and apricot character finds a complex partner in aged Pecorino; dark chocolate adds bitterness that balances the wine's sweetness while dried fig creates a direct flavour bridge.")
    PAIR(prod1b2, "Cinnamon-spiced lamb in phyllo with dried fruits and nuts", "complement", "established", "main", "The wine's Mediterranean character and dried-fruit concentration resonate with this traditional preparation; cinnamon spice echoes the wine's own warm complexity.")
    PAIR(prod1b2, "Blue cheese with honeycomb and toasted walnuts", "contrast", "classic", "cheese", "The wine's sweetness and concentrated fruit contrast powerfully with blue cheese's intensity; honeycomb creates a bridge while walnuts add a bitter counterpoint that prolongs the finish.")

# ── 2. Nemea PDO ─────────────────────────────────────────────────────────────
print("=== Nemea PDO ===")
r2 = R("Nemea PDO", "Greece", "wine",
        designation_type="PDO", designation_name="Nemea",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Nemea, in the Peloponnese, is home to Agiorgitiko — 'St. George's grape' — one of Greece's most versatile red varieties. The appellation ranges from deep valley floor vineyards producing rich, tannic reds to high-altitude slopes yielding elegant, age-worthy wines. Nemea produces everything from light, fruity reds to serious, cellar-worthy expressions.",
        key_producers="Domaine Skouras, Gaia Wines, Domaine Papaioannou, Boutari",
        historical_context="Nemea was home to the mythological Nemean Lion slain by Hercules, and the ancient Nemean Games were held here. The region's winemaking history is equally ancient, with Agiorgitiko cultivated for millennia. The PDO designation, established in 1971, recognised Nemea as one of Greece's most significant wine regions.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "stable"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Domaine Skouras", "winery", r2, "Greece",
         production_philosophy="artisanal",
         philosophy_description="George Skouras is one of Greece's most respected winemakers, combining Agiorgitiko from Nemea with international varieties and Peloponnese terroir to produce wines that bridge Greek tradition and international appeal.",
         reputation_narrative="Domaine Skouras is one of Greece's most celebrated estates, with George Skouras's Megas Oenos leading the charge for world-class Greek red wine. His advocacy for Greek varieties internationally has been instrumental in the country's wine reputation.",
         price_positioning="premium")

prod2a1, new5 = PROD("Skouras Megas Oenos Nemea", "wine_still", p2a, r2, "Greece",
                      subcategory="Agiorgitiko", price_tier="premium",
                      description="Domaine Skouras's flagship red, a Cabernet Sauvignon and Agiorgitiko blend from Nemea that demonstrates how Greek varieties can achieve international standing when blended with Bordeaux varieties. Rich, complex, with plum, spice, and a long, structured finish.")
if new5:
    PAIR(prod2a1, "Roasted lamb with oregano and lemon potatoes", "complement", "classic", "main", "The definitive Greek pairing: Agiorgitiko's plum fruit and the Cabernet's structure are the natural companion to Greek roasted lamb; lemon potatoes add the acidity that keeps the pairing vibrant.")
    PAIR(prod2a1, "Pastitsio (baked pasta with spiced meat and béchamel)", "complement", "classic", "main", "Megas Oenos's richness and structure can handle the full complexity of pastitsio; the wine's plum fruit resonates with the spiced meat while the béchamel's richness is balanced by the wine's tannin.")
    PAIR(prod2a1, "Slow-braised goat with hilopites (egg pasta) and tomato", "complement", "established", "main", "Goat's intensity and the Agiorgitiko's tannic depth are natural companions; the tomato sauce's acidity bridges the wine's fruit while hilopites absorbs the rich braising liquid.")
    PAIR(prod2a1, "Aged Kefalotyri cheese with roasted peppers and olives", "complement", "established", "cheese", "Greek aged sheep's milk cheese and Agiorgitiko is a natural regional pairing; roasted peppers add sweetness that bridges the wine's fruit while olives echo its Mediterranean character.")

prod2a2, new6 = PROD("Skouras Agiorgitiko Saint George Nemea", "wine_still", p2a, r2, "Greece",
                      subcategory="Agiorgitiko", price_tier="mid_range",
                      description="A pure expression of Agiorgitiko from Nemea, aged in French and American oak, displaying the variety's classic character: ripe red plum, dried herbs, and leather with medium tannin and a lingering, spicy finish. An excellent ambassador for Greek red wine.")
if new6:
    PAIR(prod2a2, "Moussaka with Kefalotyri and béchamel", "complement", "classic", "main", "The quintessential Greek pairing: Agiorgitiko's medium weight and plum fruit are perfectly calibrated for moussaka's layered richness; the wine's tannin cuts through the béchamel while the spiced meat resonates with its dried-herb character.")
    PAIR(prod2a2, "Grilled lamb chops with tzatziki and pita", "complement", "classic", "main", "The everyday Greek table pairing: Agiorgitiko's fruit and acidity frame grilled lamb perfectly; tzatziki's cool yogurt contrasts the wine's warmth while pita absorbs the flavour between bites.")
    PAIR(prod2a2, "Beef stifado (spiced beef stew with pearl onions)", "complement", "established", "main", "Stifado's warming spices — cinnamon, allspice, cloves — resonate deeply with Agiorgitiko's own dried-herb and spice character; the pearl onions' sweetness bridges the wine's fruit.")
    PAIR(prod2a2, "Halloumi with watermelon and fresh mint", "contrast", "established", "casual", "The wine's fruit weight contrasts with halloumi's squeaky saltiness; watermelon adds refreshing sweetness while mint bridges the wine's herbal character in this summer-Greek combination.")

p2b = P("Gaia Wines Nemea", "winery", r2, "Greece",
         production_philosophy="terroir_expression",
         philosophy_description="Gaia is one of Greece's most innovative wineries, producing both Nemea Agiorgitiko and Santorini Assyrtiko with a philosophy of terroir expression and minimal intervention. Their Thalassitis Assyrtiko and Agiorgitiko from Nemea have brought Greek wine to global attention.",
         reputation_narrative="Gaia has established itself as one of Greece's most progressive producers, with wines that consistently appear on international lists. Their ability to work with both Nemea's red varieties and Santorini's whites demonstrates a deep understanding of Greek terroir.",
         price_positioning="premium")

prod2b1, new7 = PROD("Gaia Estate Agiorgitiko Nemea", "wine_still", p2b, r2, "Greece",
                      subcategory="Agiorgitiko", price_tier="premium",
                      description="From high-altitude Nemea vineyards, Gaia's flagship Agiorgitiko displays remarkable elegance and concentration: dark plum, violet, and an earthy spice character with a long, structured finish that rewards extended cellaring.")
if new7:
    PAIR(prod2b1, "Braised short rib with root vegetables and thyme jus", "complement", "established", "main", "Gaia Estate's structural elegance and dark-fruit depth demand this level of preparation; root vegetables add sweetness while thyme echoes the wine's herbal complexity.")
    PAIR(prod2b1, "Venison with pomegranate and spiced lentils", "complement", "established", "main", "The wine's dark fruit and earthy spice find resonance with venison's iron character; pomegranate adds tartness that balances the wine's tannin while lentils provide earthy depth.")
    PAIR(prod2b1, "Duck leg confit with fig compote and bulgur wheat", "complement", "established", "main", "Duck confit's richness and the wine's plum-fig depth are natural companions; fig compote creates a direct flavour bridge while bulgur wheat's nuttiness grounds the pairing.")
    PAIR(prod2b1, "Aged Graviera with dried figs and Kalamata olives", "complement", "classic", "cheese", "Aged Greek cheese and Agiorgitiko is a quintessential regional pairing; dried figs mirror the wine's fruit while Kalamata olives add the briny depth that echoes the wine's Mediterranean character.")

prod2b2, new8 = PROD("Gaia Thalassitis Assyrtiko Santorini", "wine_still", p2b, r1, "Greece",
                      subcategory="Assyrtiko", price_tier="premium",
                      description="Gaia's Santorini Assyrtiko, named for the sea ('thalassa'), captures the variety's oceanic mineral character: lemon pith, white peach, and the distinctive saline volcanic minerality that places Santorini Assyrtiko among the world's great white wines.")
if new8:
    PAIR(prod2b2, "Grilled sea bream with lemon, herbs, and olive oil", "complement", "classic", "fish_course", "The island's definitive pairing: Thalassitis's saline mineral depth and citrus acidity are perfectly calibrated for fresh Mediterranean fish; herbs add aromatic complexity while lemon amplifies the wine's citrus.")
    PAIR(prod2b2, "Prawn saganaki with tomato and feta", "complement", "established", "main", "The wine's bright acidity and mineral character navigate the tomato's acidity and feta's saltiness with ease; the saganaki sauce's depth finds resonance in the wine's volcanic character.")
    PAIR(prod2b2, "Taramasalata with warm pita and pickled vegetables", "complement", "classic", "aperitif", "Assyrtiko's briny mineral depth is a natural foil for taramasalata's rich, salty fish roe; the wine's acidity cuts through the spread's creaminess while pickled vegetables echo its tartness.")
    PAIR(prod2b2, "Smoked trout with crème fraîche and dill on rye", "complement", "established", "starter", "The wine's saline mineral character and bright acidity are ideal for smoked fish; crème fraîche softens the wine's acidity while dill echoes its aromatic freshness.")

# ── 3. Naoussa PDO ───────────────────────────────────────────────────────────
print("=== Naoussa PDO ===")
r3 = R("Naoussa PDO", "Greece", "wine",
        designation_type="PDO", designation_name="Naoussa",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Naoussa in Macedonia, northern Greece, is home to Xinomavro — arguably Greece's greatest red grape variety. Growing on the slopes of Mount Vermio, Xinomavro produces wines of remarkable complexity, with high acidity, firm tannin, and a savoury, olive-tinged character that bears comparison with Nebbiolo. The region's wines can age for decades.",
        key_producers="Domaine Thymiopoulos, Boutari, Kir-Yianni, Alpha Estate",
        historical_context="Naoussa has been producing wine since antiquity, with its reputation for serious red wine established in the modern era by Boutari, whose 1980 Naoussa wines demonstrated international standing. The region's recent renaissance has been led by Apostolos Thymiopoulos and Stellios Boutaris (Kir-Yianni), who have repositioned Xinomavro as Greece's answer to Barolo.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r3, yr, qd, pt)

p3a = P("Domaine Thymiopoulos", "winery", r3, "Greece",
         production_philosophy="minimal_intervention",
         philosophy_description="Apostolos Thymiopoulos has transformed Naoussa's international reputation with a range of Xinomavro wines from young vines through to old-vine expressions that challenge the world's finest Nebbiolos on terroir expressiveness and ageability.",
         reputation_narrative="Thymiopoulos is widely regarded as Naoussa's most exciting young producer, with his Uranos old-vine Xinomavro earning consistent 95+ scores and placing Naoussa on the international fine wine map. His commitment to indigenous varieties has inspired a generation of Greek winemakers.",
         price_positioning="premium")

prod3a1, new9 = PROD("Thymiopoulos Uranos Naoussa PDO", "wine_still", p3a, r3, "Greece",
                      subcategory="Xinomavro", price_tier="premium",
                      description="From old Xinomavro vines on the slopes of Mount Vermio, Uranos is Thymiopoulos's finest expression: intense, complex, and demanding. Dried tomato, olive, rose petal, and tar with assertive tannin and electric acidity that demand years of cellaring or careful food pairing.")
if new9:
    PAIR(prod3a1, "Braised lamb shanks with olives and orzo", "complement", "classic", "main", "Xinomavro's tannic structure and savoury depth call for long-braised meat; olives echo the wine's own olive character while orzo absorbs the rich braising liquid.")
    PAIR(prod3a1, "Roasted leg of lamb with Greek herbs and lemon potatoes", "complement", "classic", "main", "The benchmark Xinomavro pairing: lamb's richness meets the wine's tannin head-on while Greek herbs resonate with the wine's dried-herb complexity and lemon potatoes cut through the fat.")
    PAIR(prod3a1, "Veal ossobuco with gremolata and saffron risotto", "complement", "established", "main", "Xinomavro's Nebbiolo-like structure and acidity make it a natural partner for ossobuco; gremolata's citrus and herb character echoes the wine's own complexity while saffron risotto grounds the pairing.")
    PAIR(prod3a1, "Aged Kefalotyri with quince paste and walnut bread", "complement", "established", "cheese", "Old-vine Xinomavro's tannin and complexity demand an aged sheep's milk cheese; quince paste bridges the wine's fruit while walnut bread echoes its earthy depth.")

prod3a2, new10 = PROD("Thymiopoulos Earth and Sky Naoussa PDO", "wine_still", p3a, r3, "Greece",
                       subcategory="Xinomavro", price_tier="mid_range",
                       description="A more approachable Xinomavro from younger vines, Earth and Sky displays the variety's signature savoury character — tomato, olive, dried herbs — with a lighter touch and greater approachability on release, while still demonstrating Naoussa's distinctive terroir.")
if new10:
    PAIR(prod3a2, "Grilled lamb kebabs with tzatziki and tomato salad", "complement", "classic", "main", "Xinomavro's tomato and dried-herb character creates an unexpected resonance with grilled lamb and fresh tomato; tzatziki's cool yogurt contrasts the wine's acidity.")
    PAIR(prod3a2, "Moussaka with cinnamon-spiced lamb and béchamel", "complement", "classic", "main", "Xinomavro's warming spice and savory depth navigate moussaka's complex layers; the béchamel's richness is cut by the wine's firm acidity while the cinnamon echoes the wine's own spice.")
    PAIR(prod3a2, "Pasta with slow-cooked beef and tomato sauce", "complement", "established", "main", "The wine's tomato-tinged savoury character creates a bridge with tomato-based pasta sauces; slow-cooked beef's richness is balanced by the wine's firm but approachable tannin.")
    PAIR(prod3a2, "Grilled halloumi with fig and prosciutto", "complement", "established", "starter", "Xinomavro's savoury olive character and firm acidity navigate the saltiness of halloumi; fig adds sweetness that bridges the wine's fruit while prosciutto deepens the savoury connection.")

p3b = P("Kir-Yianni Estate", "winery", r3, "Greece",
         production_philosophy="terroir_expression",
         philosophy_description="Founded by Stellios Boutaris who left the family Boutari company to create this personal estate in Naoussa, Kir-Yianni produces some of the appellation's most elegant Xinomavro wines alongside Assyrtiko in Amyndeon.",
         reputation_narrative="Kir-Yianni is one of northern Greece's most respected estates, with Ramnista Xinomavro consistently cited as a benchmark for the variety's elegance and ageing potential. The estate's commitment to Macedonian terroir has helped establish the region's global reputation.",
         price_positioning="premium")

prod3b1, new11 = PROD("Kir-Yianni Ramnista Naoussa PDO", "wine_still", p3b, r3, "Greece",
                       subcategory="Xinomavro", price_tier="premium",
                       description="Kir-Yianni's flagship Naoussa, Ramnista is an old-vine Xinomavro of remarkable concentration and elegance. Named after the hamlet where the estate is located, it displays classic Xinomavro: dried tomato, rose, dried herbs, and earth with firm, refined tannin that rewards ten or more years of cellaring.")
if new11:
    PAIR(prod3b1, "Slow-roasted pork with sage, rosemary, and roasted vegetables", "complement", "established", "main", "Ramnista's herbal complexity and firm structure are at home with herb-roasted pork; the wine's dried-herb character resonates with sage and rosemary while roasted vegetables add sweetness.")
    PAIR(prod3b1, "Braised rabbit with olives, capers, and tomato sauce", "complement", "established", "main", "Xinomavro's olive and tomato character creates an unexpected flavour echo with this traditional preparation; rabbit's delicacy contrasts with the wine's power in a compelling pairing.")
    PAIR(prod3b1, "Grilled beef ribs with chimichurri and corn salad", "complement", "established", "main", "Ramnista's structure and savoury depth can handle grilled beef ribs; chimichurri's herb and vinegar character echoes the wine's own acidity and herbal complexity.")
    PAIR(prod3b1, "Aged Gruyère with rosemary honey and toasted pine nuts", "complement", "established", "cheese", "The wine's dried-herb character and firm tannin find resonance with aged Gruyère; rosemary honey mirrors the wine's herbal notes while pine nuts add a resinous, Mediterranean complexity.")

prod3b2, new12 = PROD("Kir-Yianni Parparoussis Xinomavro Naoussa", "wine_still", p3b, r3, "Greece",
                       subcategory="Xinomavro", price_tier="mid_range",
                       description="Kir-Yianni's entry-level Naoussa, the Parparoussis offers an accessible introduction to Xinomavro's character with lighter structure and earlier approachability while retaining the variety's signature savoury dried-herb and olive notes.")
if new12:
    PAIR(prod3b2, "Yemista (stuffed tomatoes and peppers with rice and herbs)", "complement", "classic", "main", "The wine's tomato-tinged character and herb notes create an extraordinary resonance with yemista; the rice absorbs the rich filling while the wine's acidity keeps the pairing fresh.")
    PAIR(prod3b2, "Spanakopita (spinach and feta pie in phyllo)", "complement", "established", "casual", "Xinomavro's savoury depth and bright acidity are well suited to spanakopita's herby, salty filling; the phyllo's buttery crispness provides textural contrast while feta's tang echoes the wine's acidity.")
    PAIR(prod3b2, "Lamb kofta with hummus and warm pita", "complement", "classic", "casual", "The wine's spice and dark fruit complement the kofta's ground lamb and spice mixture; hummus's creaminess buffers the wine's firm acidity while pita grounds the combination.")
    PAIR(prod3b2, "Grilled sardines with lemon, capers, and crusty bread", "contrast", "adventurous", "starter", "Sardines and a light red wine is a Mediterranean tradition; Xinomavro's acidity and savoury character complement the sardines' oiliness while lemon and capers bridge the contrast.")

# ── 4. Muscat of Samos PDO ───────────────────────────────────────────────────
print("=== Muscat of Samos PDO ===")
r4 = R("Muscat of Samos PDO", "Greece", "wine",
        designation_type="PDO", designation_name="Muscat of Samos",
        reputation_tier="respected",
        quality_trajectory="established",
        description="The island of Samos in the eastern Aegean produces one of the world's most celebrated sweet Muscat wines, made from the Muscat Blanc à Petits Grains variety grown on dramatic terraced hillside vineyards. Samos Muscat ranges from lightly sweet Anthemis to the intensely concentrated Nectar made from sun-dried grapes. The wines have been traded since antiquity.",
        key_producers="Samos Wine Union (Kooperative), Mercouri Estate",
        historical_context="Samos has produced Muscat wine since at least the 10th century, traded throughout the Byzantine Empire and later across Europe. The island's cooperative, the Samos Wine Union founded in 1934, produces nearly all the island's wine and has maintained quality standards that have kept Samos Muscat among the world's great sweet wines for centuries.")

for yr, qd, pt in [
    (2019, "excellent", "stable"), (2020, "very_good", "stable"), (2021, "excellent", "stable"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r4, yr, qd, pt)

p4a = P("Samos Wine Union", "winery", r4, "Greece",
         production_philosophy="classical",
         philosophy_description="The Samos Wine Union cooperative, established in 1934, is the primary custodian of Samos Muscat, overseeing production from 3,000 grower members across the island's terraced vineyards. Their range spans from the young Anthemis to the 10-year-aged Nectar.",
         reputation_narrative="The Samos Wine Union has maintained Samos Muscat's centuries-old reputation for quality, producing wines that consistently win international awards and appear on the dessert wine lists of the world's finest restaurants.",
         price_positioning="mid_range")

prod4a1, new13 = PROD("Samos Wine Union Muscat Grand Cru Samos", "wine_still", p4a, r4, "Greece",
                       subcategory="Muscat Blanc", price_tier="mid_range",
                       description="The flagship of the Samos range, Grand Cru is made from the oldest Muscat Blanc à Petits Grains vines on the island's high-altitude terraces. Intensely aromatic with orange blossom, apricot, and honey, balanced by the variety's natural acidity — one of the world's benchmark dessert Muscats.")
if new13:
    PAIR(prod4a1, "Fresh baklava with pistachio and rose water syrup", "complement", "classic", "dessert", "Samos Grand Cru's orange blossom and honey character is a natural echo of baklava's syrup; pistachio's earthiness provides a savoury counterpoint while rose water mirrors the wine's floral depth.")
    PAIR(prod4a1, "Peach tarte tatin with Greek yogurt and honey", "complement", "established", "dessert", "The wine's peach and apricot character mirrors the tarte's stone fruit; Greek yogurt's tartness bridges the wine's natural acidity while honey creates a direct flavour connection.")
    PAIR(prod4a1, "Galaktoboureko (custard in phyllo with syrup)", "complement", "classic", "dessert", "The wine's orange blossom and honey sweetness is a natural complement to this traditional Greek custard pastry; phyllo's buttery crispness provides textural contrast to the wine's liquid richness.")
    PAIR(prod4a1, "Aged Roquefort with toasted brioche and dried apricot", "contrast", "classic", "cheese", "Sweet Muscat and blue cheese is a classic dessert contrast; Roquefort's intense salinity and pungency are tamed by the wine's sweetness while dried apricot creates a bridge between wine and cheese.")

prod4a2, new14 = PROD("Samos Wine Union Nectar Samos PDO", "wine_still", p4a, r4, "Greece",
                       subcategory="Muscat Blanc", price_tier="premium",
                       description="Made from sun-dried Muscat grapes and aged for ten years in oak barrels, Nectar is one of Greece's most extraordinary wines: concentrated coffee, raisin, dried orange peel, and walnut with remarkable acidity that prevents cloying sweetness. A wine of profound complexity and almost limitless ageing potential.")
if new14:
    PAIR(prod4a2, "Walnut cake with honey syrup and cinnamon", "complement", "classic", "dessert", "Nectar's walnut and coffee character creates a profound resonance with walnut cake; honey syrup bridges the wine's sweetness while cinnamon echoes its warm spice.")
    PAIR(prod4a2, "Dark chocolate torta with sea salt and caramel", "complement", "established", "dessert", "The wine's coffee and raisin complexity can stand alongside dark chocolate; sea salt amplifies both while caramel echoes the wine's caramelised dried-fruit depth.")
    PAIR(prod4a2, "Aged Pecorino with truffle honey and dried black figs", "complement", "classic", "cheese", "Nectar's concentration and complexity demand an aged sheep's milk cheese; truffle honey bridges its coffee-walnut depth while dried figs mirror the wine's raisin character.")
    PAIR(prod4a2, "Christmas pudding with brandy cream and toasted almonds", "complement", "established", "dessert", "Nectar's dried-fruit concentration and warming spice are a natural match for Christmas pudding; brandy cream echoes the wine's fortified depth while almonds add a roasted note.")

p4b = P("Estate Argyros Samos", "winery", r4, "Greece",
         production_philosophy="artisanal",
         philosophy_description="While primarily known for their Santorini Assyrtiko, Estate Argyros also produces a limited Samos Muscat that demonstrates the variety's potential under careful artisanal management outside the cooperative system.",
         reputation_narrative="Estate Argyros's Samos Muscat provides a fascinating artisanal contrast to the cooperative's production, demonstrating that individual estate focus can reveal additional complexity in this ancient variety.",
         price_positioning="mid_range")

prod4b1, new15 = PROD("Argyros Muscat Vin Doux Samos", "wine_still", p4b, r4, "Greece",
                       subcategory="Muscat Blanc", price_tier="mid_range",
                       description="Estate Argyros's naturally sweet Muscat from Samos, lightly fortified in the vin doux naturel style to preserve the grape's full aromatic freshness while adding concentration. Orange blossom, lychee, and white peach with a silky sweetness and clean, fresh finish.")
if new15:
    PAIR(prod4b1, "Greek honey cake (melopita) with mastic-spiced cream", "complement", "classic", "dessert", "The wine's honey and orange blossom character resonate with this traditional Greek honey cake; mastic spice adds a distinctively Greek aromatic note that bridges wine and dessert.")
    PAIR(prod4b1, "Fresh fruit pavlova with passion fruit curd and cream", "complement", "established", "dessert", "The wine's fresh lychee and white peach character mirrors the pavlova's tropical freshness; passion fruit curd adds tartness that echoes the wine's natural acidity.")
    PAIR(prod4b1, "Chilled melon with prosciutto and fresh mint", "bridge", "established", "aperitif", "The wine's perfumed sweetness and melon character create a bridge with the fruit's sweetness; prosciutto's saltiness provides a contrast while mint adds aromatic freshness.")
    PAIR(prod4b1, "Soft goat cheese with lavender honey and pistachios", "complement", "suggested", "cheese", "The wine's floral sweetness and honey notes find a gentle match in soft goat cheese; lavender honey echoes the wine's aromatic character while pistachios add savoury-green depth.")

# ── 5. Mantinia PDO ──────────────────────────────────────────────────────────
print("=== Mantinia PDO ===")
r5 = R("Mantinia PDO", "Greece", "wine",
        designation_type="PDO", designation_name="Mantinia",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Mantinia, in the high-altitude Arcadia region of the Peloponnese, produces delicate white wines from the indigenous Moschofilero variety — a pink-skinned grape of extraordinary aromatic intensity. At 600+ metres elevation, the cool climate preserves Moschofilero's natural acidity and floral character, producing wines that are simultaneously aromatic and refreshing.",
        key_producers="Tselepos Winery, Domaine Spiropoulos, Boutari Mantinia",
        historical_context="Mantinia's ancient history is tied to the myths of Arcadia — this pastoral landscape of ancient Greece was home to Pan and the satyrs. The region's cool climate and the indigenous Moschofilero variety create a distinctive wine style that has been praised since ancient times. The modern PDO, established in 1971, recognised the region's unique character.")

for yr, qd, pt in [
    (2019, "very_good", "stable"), (2020, "good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "very_good", "rising")]:
    VIN(r5, yr, qd, pt)

p5a = P("Tselepos Winery", "winery", r5, "Greece",
         production_philosophy="terroir_expression",
         philosophy_description="Yannis Tselepos is Mantinia's most respected champion, producing Moschofilero of extraordinary aromatic precision and freshness that has brought international attention to this high-altitude Arcadian variety.",
         reputation_narrative="Tselepos Winery has established Moschofilero as Greece's most food-friendly aromatic variety, producing wines that critics and sommeliers worldwide praise for their precision, freshness, and versatility at the table.",
         price_positioning="mid_range")

prod5a1, new17 = PROD("Tselepos Moschofilero Mantinia PDO", "wine_still", p5a, r5, "Greece",
                       subcategory="Moschofilero", price_tier="mid_range",
                       description="The benchmark expression of Moschofilero from Mantinia, displaying the variety's signature aromatic intensity: rose petal, orange blossom, grapefruit, and white peach. Refreshing, precise, and with a long, floral finish — one of Greece's most food-friendly white wines.")
if new17:
    PAIR(prod5a1, "Grilled prawns with lemon, garlic, and fresh herbs", "complement", "classic", "starter", "Moschofilero's floral aromatics and bright acidity are a natural companion for grilled shellfish; lemon amplifies the wine's citrus while herbs echo its own aromatic character.")
    PAIR(prod5a1, "Greek salad with barrel-aged feta and olives", "complement", "classic", "starter", "The wine's freshness and floral precision pair beautifully with the simplicity of Greek salad; barrel-aged feta's tang and saltiness are balanced by the wine's acidity while olives add Mediterranean depth.")
    PAIR(prod5a1, "Sea bass tartare with cucumber, dill, and lemon crème fraîche", "complement", "established", "starter", "Moschofilero's delicate floral lift and citrus acidity are ideal for delicate raw fish; dill echoes the wine's herbaceous notes while cucumber adds a cooling freshness.")
    PAIR(prod5a1, "Zucchini blossoms stuffed with ricotta and herbs", "complement", "classic", "starter", "The wine's floral rose-petal character creates a magical echo with zucchini blossoms; ricotta's creaminess is balanced by the wine's acidity while herbs amplify its aromatic character.")

prod5a2, new18 = PROD("Tselepos Amalia Brut Moschofilero Mantinia", "wine_sparkling", p5a, r5, "Greece",
                       subcategory="Moschofilero", price_tier="mid_range",
                       description="A sparkling wine made from Moschofilero in the traditional method, displaying the variety's extraordinary aromatics enhanced by autolytic yeast character. Rose petal, brioche, and citrus combine in one of Greece's most distinctive sparkling wines.")
if new18:
    PAIR(prod5a2, "Loukoumades (honey donuts) with cinnamon and walnuts", "complement", "suggested", "dessert", "The wine's floral sweetness and fine bubbles create an unexpected bridge with loukoumades; honey mirrors the wine's aromatic depth while cinnamon adds warming spice.")
    PAIR(prod5a2, "Fresh oysters with rose water mignonette", "complement", "established", "aperitif", "Moschofilero's floral character and fine bubbles find a harmonious companion in oysters; rose water mignonette creates an aromatic bridge between the wine's rose petal notes and the oyster's brine.")
    PAIR(prod5a2, "Smoked salmon blinis with crème fraîche and dill", "complement", "established", "aperitif", "The wine's citrus freshness and fine mousse are ideal for a blini canapé; crème fraîche's acidity bridges the wine while dill echoes its aromatic lift.")
    PAIR(prod5a2, "Strawberry and fresh cream pavlova", "complement", "suggested", "dessert", "The wine's strawberry and rose character creates a direct flavour echo with fresh strawberries; cream softens the wine's acidity while the pavlova's meringue adds a complementary sweetness.")

p5b = P("Domaine Spiropoulos", "winery", r5, "Greece",
         production_philosophy="sustainable",
         philosophy_description="One of the Peloponnese's most committed organic producers, Domaine Spiropoulos farms biodynamically in Mantinia and Nemea, producing Moschofilero and Agiorgitiko with minimal intervention and genuine terroir expression.",
         reputation_narrative="Spiropoulos is respected for its commitment to organic and biodynamic farming in the challenging Peloponnese climate, producing wines of genuine integrity that express Greek terroir without compromise.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Spiropoulos Moschofilero Mantinia Organic", "wine_still", p5b, r5, "Greece",
                       subcategory="Moschofilero", price_tier="mid_range",
                       description="Biodynamically grown Moschofilero from Mantinia's high-altitude vineyards, displaying the variety's aromatic precision with an added mineral freshness that comes from organic farming practices. Rose petal, citrus blossom, and a long, clean finish.")
if new19:
    PAIR(prod5b1, "Horiatiki salad with aged feta and village bread", "complement", "classic", "casual", "Moschofilero's floral freshness and Greek character are perfectly matched with the village salad; feta's tang is balanced by the wine's acidity while village bread grounds the combination.")
    PAIR(prod5b1, "Spanakopita triangles with herb-spiced feta filling", "complement", "established", "casual", "The wine's floral lift and bright acidity navigate spanakopita's herby, salty filling; the phyllo's butteriness is refreshed by each sip of the wine's aromatic freshness.")
    PAIR(prod5b1, "Grilled sardines with olive oil, lemon, and parsley", "complement", "established", "starter", "Organic Moschofilero's citrus acidity and aromatic lift cut through sardines' oiliness; lemon amplifies the wine's citrus while parsley adds herbaceous depth.")
    PAIR(prod5b1, "Fresh goat cheese with thyme honey and crusty bread", "complement", "classic", "aperitif", "The wine's floral character and bright acidity are a classic match for fresh goat cheese; thyme honey bridges the wine's aromatic depth while crusty bread grounds the pairing.")

prod5b2, new20 = PROD("Spiropoulos Agiorgitiko Nemea Biodynamic", "wine_still", p5b, r2, "Greece",
                       subcategory="Agiorgitiko", price_tier="mid_range",
                       description="Biodynamically farmed Agiorgitiko from Nemea by Spiropoulos, displaying the variety's classic plum fruit and dried-herb character with an added earthiness and freshness that comes from biodynamic farming. A genuine, food-friendly expression of Greek red wine.")
if new20:
    PAIR(prod5b2, "Grilled lamb chops with tzatziki and Greek salad", "complement", "classic", "main", "Biodynamic Agiorgitiko's plum fruit and herbal character are the natural companion for grilled lamb; tzatziki's yogurt cools the wine's warmth while Greek salad adds freshness.")
    PAIR(prod5b2, "Kleftiko (slow-cooked lamb in parchment with vegetables)", "complement", "classic", "main", "Kleftiko's slow-cooked intensity and herb character are a benchmark Agiorgitiko pairing; the wine's medium structure and fruit depth match the tender lamb without overwhelming it.")
    PAIR(prod5b2, "Giouvetsi (lamb and orzo baked with tomato and cinnamon)", "complement", "established", "main", "The wine's cinnamon spice and tomato-tinged character resonate with giouvetsi's warming spices and tomato sauce; orzo absorbs the flavours while the wine's acidity keeps the dish fresh.")
    PAIR(prod5b2, "Cheese saganaki with honey and sesame", "complement", "established", "starter", "The wine's fruit and herbs find a playful partner in fried cheese with honey; sesame adds a nutty depth while honey bridges the wine's fruit with the cheese's salty richness.")

# ── Summary ──────────────────────────────────────────────────────────────────
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
print("B146 complete.")
conn.close()
