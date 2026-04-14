#!/usr/bin/env python3
"""B151 — Bolgheri DOC (IT), Morellino di Scansano DOCG (IT), Yakima Valley AVA (WA), Red Mountain AVA (WA), Bodega Garzón (Uruguay)"""
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

# ── 1. Bolgheri DOC ──────────────────────────────────────────────────────────
print("=== Bolgheri DOC ===")
r1 = R("Bolgheri DOC", "Italy", "wine",
        designation_type="DOC", designation_name="Bolgheri",
        reputation_tier="iconic",
        quality_trajectory="established",
        description="Bolgheri, on the Tuscan coast south of Livorno, is one of the world's most famous modern wine appellations, home to Sassicaia, Ornellaia, and Masseto — wines that challenged the Bordeaux establishment and transformed Italian fine wine's international standing. The coastal climate, maritime influence, and gravelly soils create ideal conditions for Cabernet Sauvignon, Merlot, and Cabernet Franc that bear genuine comparison to Bordeaux's finest.",
        key_producers="Tenuta San Guido (Sassicaia), Ornellaia, Masseto, Grattamacco, Michele Satta",
        historical_context="Bolgheri's transformation from coastal scrubland to world-famous wine region is one of viticulture's great stories. Marchese Mario Incisa della Rocchetta first planted Cabernet Sauvignon at Tenuta San Guido in the 1940s, producing Sassicaia for family use only. When Antinori began distributing Sassicaia commercially in 1978, its success challenged Italy's entire wine classification system and inspired the 'Super Tuscan' revolution. Bolgheri received its own DOC in 1983; Sassicaia its unique sub-appellation in 1994.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r1, yr, qd, pt)

p1a = P("Tenuta San Guido", "winery", r1, "Italy",
         production_philosophy="classical",
         philosophy_description="Tenuta San Guido is the birthplace of Sassicaia and the Super Tuscan revolution, founded by Marchese Mario Incisa della Rocchetta in the 1940s. Today the estate, managed by the Incisa della Rocchetta family, produces Sassicaia — the only Italian wine with its own individual DOC — and Guidalberto.",
         reputation_narrative="Tenuta San Guido's Sassicaia is one of Italy's most collected and internationally recognised wines, consistently earning 95+ scores and landmark auction prices. Its creation of the Super Tuscan category transformed Italian wine's global standing and inspired a generation of coastal Tuscan producers.",
         price_positioning="ultra_premium")

prod1a1, new1 = PROD("Sassicaia Bolgheri Sassicaia DOC", "wine_still", p1a, r1, "Italy",
                      subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                      description="Italy's most famous Bordeaux-style red, a Cabernet Sauvignon-Cabernet Franc blend from the unique Sassicaia sub-DOC. The wine's distinctive character — cassis, blackcurrant leaf, cedar, tobacco, and mineral precision — reflects the Bolgheri coastal terroir and 80 years of winemaking refinement. Ageable for 25+ years.")
if new1:
    PAIR(prod1a1, "Bistecca alla Fiorentina with Tuscan olive oil and rosemary", "complement", "classic", "main", "Italy's greatest Cabernet with Italy's greatest steak preparation: Sassicaia's cassis and cedar find perfect resonance with the T-bone's charred intensity while rosemary echoes the wine's herbal character.")
    PAIR(prod1a1, "Slow-roasted leg of lamb with garlic, sage, and white wine", "complement", "classic", "main", "Sassicaia's Bordeaux character and coastal Tuscan elegance are a natural companion for slow-roasted lamb; sage echoes the wine's herbal complexity while white wine in the braising liquid creates a wine-based bridge.")
    PAIR(prod1a1, "Aged Parmigiano-Reggiano with black truffle and aged balsamic", "complement", "classic", "cheese", "Italy's greatest wine and greatest cheese create a pairing of cultural significance; black truffle deepens the earthy resonance while aged balsamic's sweet-sour complexity mirrors the wine's own multi-layered character.")
    PAIR(prod1a1, "Wild boar ragù with handmade pici pasta and Pecorino", "complement", "established", "main", "Super Tuscan power and Tuscan game ragù is a coastal classic; wild boar's earthy intensity resonates with Sassicaia's cassis depth while pici pasta's rustic thickness absorbs the rich sauce.")

prod1a2, new2 = PROD("Guidalberto Bolgheri DOC", "wine_still", p1a, r1, "Italy",
                      subcategory="Cabernet Sauvignon blend", price_tier="premium",
                      description="Sassicaia's second wine, a Cabernet Sauvignon and Merlot blend from younger Tenuta San Guido vineyards. Guidalberto delivers the estate's signature coastal Tuscan character — cassis, cedar, and mineral precision — in a more accessible style that is drinking beautifully within 5-8 years of the vintage.")
if new2:
    PAIR(prod1a2, "Grilled veal chop with sage butter and roasted potatoes", "complement", "classic", "main", "Guidalberto's elegance and cassis character are well-matched to veal; sage butter echoes the wine's herbal complexity while roasted potatoes absorb the rich butter and ground the pairing.")
    PAIR(prod1a2, "Tagliata di manzo with rocket, Parmigiano, and olive oil", "complement", "classic", "main", "The quintessential Tuscan bistro pairing: the wine's cassis and cedar complement the beef while rocket's bitterness and Parmigiano's umami add the complexity the wine's structure demands.")
    PAIR(prod1a2, "Duck confit with lentils, sage, and Vin Santo reduction", "complement", "established", "main", "The wine's Bolgheri character navigates duck confit's richness with Italian composure; Vin Santo reduction adds a Tuscan-specific sweetness while sage echoes the wine's herbal dimension.")
    PAIR(prod1a2, "Aged Pecorino Toscano with fig jam and walnuts", "complement", "established", "cheese", "Bolgheri's coastal Tuscan red with Tuscan sheep's cheese is a regional pairing of genuine synergy; fig jam bridges the wine's cassis fruit while walnuts add savoury depth.")

p1b = P("Ornellaia Winery", "winery", r1, "Italy",
         production_philosophy="classical",
         philosophy_description="Ornellaia, established by Lodovico Antinori in 1981, produces one of Italy's most internationally recognised Super Tuscans from a Bolgheri estate that combines Cabernet Sauvignon, Merlot, and Cabernet Franc in a Bordeaux-inspired blend of exceptional elegance.",
         reputation_narrative="Ornellaia is Italy's most successful Bordeaux-style blend after Sassicaia, consistently earning 96-100 point scores and commanding prices that rival Premier Cru Bordeaux. Its acquisition by the Frescobaldi family brought additional resources and the now-famous annual 'Vendemmia d'Artista' art label series.",
         price_positioning="ultra_premium")

prod1b1, new3 = PROD("Ornellaia Bolgheri Superiore DOC", "wine_still", p1b, r1, "Italy",
                      subcategory="Cabernet Sauvignon blend", price_tier="ultra_premium",
                      description="One of Italy's greatest wines, Ornellaia is a Cabernet Sauvignon-dominated blend with Merlot and Cabernet Franc, displaying extraordinary complexity: cassis, dark cherry, graphite, cedar, and Bolgheri's distinctive sea-breeze minerality with a tannin structure built for 20+ years of development.")
if new3:
    PAIR(prod1b1, "Wagyu beef fillet with black truffle and Parmesan gratin", "complement", "classic", "main", "Ornellaia's prestige demands preparation of equal standing; black truffle deepens the earthy mineral resonance while Parmesan gratin adds the umami depth that bridges Italy's greatest wine with Italy's most luxurious beef preparation.")
    PAIR(prod1b1, "Rack of lamb with Tuscan herb crust and Chianti reduction", "complement", "classic", "main", "The wine's Bolgheri character and Bordeaux inspiration make lamb its most natural companion; Tuscan herb crust echoes the wine's complexity while Chianti reduction adds regional depth.")
    PAIR(prod1b1, "Aged Parmigiano-Reggiano 36-month with Modena balsamic", "complement", "classic", "cheese", "Italy's finest wine and finest aged cheese: 36-month Parmigiano's crystalline depth and Ornellaia's concentration create a pairing of extraordinary resonance; Modena balsamic adds the sweet-acidic bridge.")
    PAIR(prod1b1, "Whole roasted pigeon with black olive sauce and polenta", "complement", "established", "main", "The wine's complexity and coastal mineral depth find a compelling match in pigeon with olive; polenta's rustic simplicity grounds the luxury while black olive echoes the wine's mineral depth.")

prod1b2, new4 = PROD("Le Serre Nuove dell'Ornellaia Bolgheri DOC", "wine_still", p1b, r1, "Italy",
                      subcategory="Merlot blend", price_tier="premium",
                      description="Ornellaia's second wine, more Merlot-dominant than the flagship, displaying the estate's hallmark coastal elegance in a more approachable style. Le Serre Nuove delivers plum, dark cherry, and cedar with the supple texture characteristic of the estate's Merlot component.")
if new4:
    PAIR(prod1b2, "Pasta con ragù di anatra (duck ragù with pappardelle)", "complement", "classic", "main", "The wine's Merlot-driven plum character and silky texture are natural companions for duck ragù; pappardelle's width holds the rich sauce while the wine's acidity prevents the preparation from feeling heavy.")
    PAIR(prod1b2, "Grilled Florentine T-bone with sage and white beans", "complement", "classic", "main", "Le Serre Nuove's accessible elegance and dark cherry character make it the more approachable choice for the famous T-bone; sage adds herbal complexity while white beans provide the starchy foil.")
    PAIR(prod1b2, "Eggplant parmigiana with San Marzano tomatoes and basil", "complement", "established", "main", "The wine's plum depth and Tuscan character are well-matched to the richness of parmigiana; tomato's acidity bridges the wine while basil adds the aromatic note that echoes its herbal character.")
    PAIR(prod1b2, "Aged Asiago with prosciutto di Parma and melon", "complement", "established", "cheese", "Le Serre Nuove's plum and silky texture find resonance with aged Asiago's nutty depth; prosciutto's salt and fat add the savoury dimension while melon's sweetness bridges the wine's fruit.")

# ── 2. Morellino di Scansano DOCG ────────────────────────────────────────────
print("=== Morellino di Scansano DOCG ===")
r2 = R("Morellino di Scansano DOCG", "Italy", "wine",
        designation_type="DOCG", designation_name="Morellino di Scansano",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Morellino di Scansano, in the Maremma Grossetana of southern Tuscany, produces Sangiovese-based reds of remarkable warmth and accessibility. The local name 'Morellino' for Sangiovese reflects the variety's small, dark-skinned expression in this coastal zone, where the Mediterranean influence tempers the acidity and adds plummy richness unusual in traditional Sangiovese wines.",
        key_producers="Moris Farms, Erik Banti, Sassotondo, Fattoria Le Pupille, Rocca di Frassinello",
        historical_context="Morellino di Scansano was awarded DOC status in 1978 and DOCG in 2007, recognising the distinctive character of Sangiovese grown in the Maremma's warm coastal zone. The wine's warmth and accessibility compared to Chianti Classico made it popular as an everyday Italian red, while the arrival of producers like Rocca di Frassinello (Mondavi and Frescobaldi) added prestige to the denomination.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Fattoria Le Pupille", "winery", r2, "Italy",
         production_philosophy="terroir_expression",
         philosophy_description="Fattoria Le Pupille is Morellino di Scansano's most prestigious estate, founded by Elisabetta Geppetti in the 1980s and now run with her daughter Clara. Their Saffredi — a Super Tuscan of Cabernet, Syrah, and Alicante — is considered one of Maremma's greatest wines.",
         reputation_narrative="Le Pupille has elevated Morellino di Scansano to the international stage, with Elisabetta Geppetti's pioneering Maremma production demonstrating that southern Tuscany can produce wines worthy of serious attention alongside the better-known Chianti Classico and Brunello zones.",
         price_positioning="premium")

prod2a1, new5 = PROD("Fattoria Le Pupille Morellino di Scansano DOCG", "wine_still", p2a, r2, "Italy",
                      subcategory="Sangiovese", price_tier="mid_range",
                      description="The estate Morellino, from Le Pupille's coastal Maremma vineyards, displays the variety's characteristic warmth and accessibility: dark cherry, dried herbs, tobacco, and a plummy richness that sets Morellino apart from the more austere Chianti styles. One of southern Tuscany's most reliable everyday reds.")
if new5:
    PAIR(prod2a1, "Pasta al ragù di cinghiale (wild boar pasta)", "complement", "classic", "main", "Wild boar ragù is the Maremma's most celebrated dish, and Morellino di Scansano its natural companion; the wine's warmth and dark cherry character resonate with the game's earthy intensity while the pasta's starchiness softens the tannin.")
    PAIR(prod2a1, "Grilled Tuscan sausages with white beans and sage", "complement", "classic", "main", "Morellino's accessible structure and fruit depth are ideal for Tuscan sausages; white beans provide the starchy foil while sage echoes the wine's herbal character in a genuinely regional combination.")
    PAIR(prod2a1, "Cacciucco alla Livornese (Livornese fish stew with red wine)", "complement", "established", "main", "The unusual red wine fish stew of the Tyrrhenian coast is Morellino's most distinctive food pairing; the wine's warmth and relatively light tannin can navigate the stew's rich tomato and garlic base.")
    PAIR(prod2a1, "Aged Pecorino from Pienza with truffle honey and farro bread", "complement", "classic", "cheese", "Tuscan sheep's milk cheese and Morellino is a regional classic; truffle honey bridges the wine's warmth while farro bread's nutty earthiness grounds the simple but complete Maremma pairing.")

prod2a2, new6 = PROD("Fattoria Le Pupille Poggio Valente Morellino Riserva", "wine_still", p2a, r2, "Italy",
                      subcategory="Sangiovese", price_tier="premium",
                      description="The estate's prestige Morellino, from the Poggio Valente single vineyard on the highest Scansano slopes. Extended oak ageing produces a wine of greater complexity and age-worthiness than the estate label: concentrated dark cherry, tobacco, leather, and mineral depth that rewards 8-10 years of cellaring.")
if new6:
    PAIR(prod2a2, "Braised wild boar with dark chocolate and Maremma herbs (peposo style)", "complement", "classic", "main", "Poggio Valente's depth and concentration demand this most elaborate Maremman game preparation; dark chocolate adds the bitter-sweet counterpoint that mirrors the wine's concentrated fruit while Maremma herbs echo its herbal depth.")
    PAIR(prod2a2, "Bistecca con le erbe (T-bone with Tuscan herbs)", "complement", "classic", "main", "The riserva's structure and concentrated dark fruit can stand up to the full force of Tuscan grilled beef; Tuscan herbs create the aromatic bridge between wine and preparation.")
    PAIR(prod2a2, "Aged Pecorino di Manciano with aged balsamic and figs", "complement", "established", "cheese", "The appellation's own aged Pecorino di Manciano is the natural companion for Poggio Valente; aged balsamic's sweetness bridges the wine's fruit while figs provide the warmth that extends the Maremma pairing.")
    PAIR(prod2a2, "Pappardelle al ragù di lepre (hare ragù)", "complement", "classic", "main", "Wild hare ragù is southern Tuscany's most celebrated pasta preparation for aged Sangiovese; the wine's concentrated dark fruit and leather character resonate with hare's gamey intensity while pappardelle absorbs the rich sauce.")

p2b = P("Moris Farms", "winery", r2, "Italy",
         production_philosophy="sustainable",
         philosophy_description="Moris Farms is one of Morellino di Scansano's founding estates, with winemaking roots in the Maremma going back to 1971. Their Avvoltore Super Tuscan alongside the estate Morellino has established the farm as one of the denomination's most reliable producers.",
         reputation_narrative="Moris Farms represents the genuine heart of Maremma winemaking — a family estate that has built its reputation on consistent quality and authentic expression of the region's distinctive Sangiovese character over more than 50 years.",
         price_positioning="mid_range")

prod2b1, new7 = PROD("Moris Farms Morellino di Scansano DOCG", "wine_still", p2b, r2, "Italy",
                      subcategory="Sangiovese", price_tier="mid_range",
                      description="The estate Morellino from Moris Farms' Maremma vineyards, offering authentic Morellino character at excellent value: warm, cherry-dominated fruit with the Mediterranean influence giving the wine a plummy approachability that has made it a restaurant favourite throughout Italy and beyond.")
if new7:
    PAIR(prod2b1, "Pizza rustica with Maremma salumi and local mushrooms", "complement", "classic", "casual", "Morellino's warmth and accessibility make it the ideal casual pairing for rustic pizza; local salumi and mushrooms echo the wine's earthy character while the pizza's tomato provides the acidity that keeps the pairing fresh.")
    PAIR(prod2b1, "Ribollita (Tuscan bread soup with vegetables and beans)", "complement", "classic", "main", "The quintessential Tuscan pairing: Morellino's accessibility and warmth are ideally suited to ribollita's hearty simplicity; the wine's cherry character bridges the soup's vegetable sweetness while its acidity cuts through the bread's starchiness.")
    PAIR(prod2b1, "Grilled Chianina beef with salt, olive oil, and rocket", "complement", "classic", "main", "The wine's approachable fruit and medium structure make it an everyday companion for Tuscan grilled beef; salt and olive oil enhance the meat's natural character while rocket's bitterness provides a clean vegetable contrast.")
    PAIR(prod2b1, "Caciotta Toscana with chestnut honey and black pepper", "complement", "established", "cheese", "The wine's warmth and accessibility find a pleasant match in this mild Tuscan semi-aged cheese; chestnut honey bridges the wine's warmth while black pepper adds the spice that echoes the wine's own character.")

prod2b2, new8 = PROD("Moris Farms Avvoltore Maremma Toscana IGT", "wine_still", p2b, r2, "Italy",
                      subcategory="Cabernet Sauvignon blend", price_tier="premium",
                      description="Moris Farms' Super Tuscan, a Sangiovese-Cabernet Sauvignon-Syrah blend from their finest Maremma vineyards. Avvoltore displays greater concentration and complexity than the Morellino: dark cherry, blackberry, tobacco, and the distinctive coastal Maremma mineral character in a wine of serious ambition.")
if new8:
    PAIR(prod2b2, "Wild boar stew with Maremma herbs and polenta", "complement", "classic", "main", "Avvoltore's Super Tuscan structure and dark-fruit concentration are natural companions for the Maremma's iconic game stew; polenta absorbs the richness while Maremma herbs echo the wine's complexity.")
    PAIR(prod2b2, "Tagliata with aged Parmesan, rocket, and lemon", "complement", "classic", "main", "The wine's Cabernet character and concentration make it an ideal tagliata companion; Parmesan's umami bridges the tannin while lemon's acidity echoes the wine's own freshness and prevents the rich meat from feeling heavy.")
    PAIR(prod2b2, "Aged Pecorino Stagionato with black truffle and olive oil", "complement", "established", "cheese", "Avvoltore's Super Tuscan ambition demands an aged hard cheese; black truffle deepens the earthy resonance while olive oil bridges its Mediterranean coastal character.")
    PAIR(prod2b2, "Grilled lamb chops with rosemary, garlic, and Maremma olive oil", "complement", "classic", "main", "The wine's Syrah and Cabernet character find a natural home with grilled lamb; rosemary and garlic echo the wine's herbal complexity while Maremma olive oil grounds the pairing in local terroir.")

# ── 3. Yakima Valley AVA ─────────────────────────────────────────────────────
print("=== Yakima Valley AVA ===")
r3 = R("Yakima Valley AVA", "USA", "wine",
        designation_type="AVA", designation_name="Yakima Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Yakima Valley, in south-central Washington State, was the first designated American Viticultural Area in the Pacific Northwest (1983). The valley's arid high-desert climate, volcanic basalt soils, and dramatic diurnal temperature swings produce wines of exceptional concentration and natural acidity, particularly Cabernet Sauvignon, Merlot, Syrah, and Riesling. Yakima Valley contains several of Washington's most important sub-AVAs including Red Mountain and Horse Heaven Hills.",
        key_producers="Château Ste. Michelle (Ethos), Kiona Vineyards, Hogue Cellars, Two Mountain Winery, Owen Roe",
        historical_context="Yakima Valley's agricultural heritage predates wine: the valley is famous for hops, apples, and asparagus, with an irrigation infrastructure that also benefits viticulture. William Bridgman planted the first commercial Vitis vinifera vines in 1917, and the valley's modern wine era began in earnest in the 1960s with Château Ste. Michelle's founding. The 1983 AVA designation was Washington's and the Northwest's first, recognising Yakima's pioneering role in Pacific Northwest viticulture.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "stable"), (2023, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

p3a = P("Kiona Vineyards", "winery", r3, "USA",
         production_philosophy="terroir_expression",
         philosophy_description="Kiona is one of Washington's oldest family estate wineries, established in 1975 on the slopes of Red Mountain within Yakima Valley. Their Lemberger and Cabernet Sauvignon from the Red Mountain sub-AVA have been benchmarks of Pacific Northwest winemaking for over 40 years.",
         reputation_narrative="Kiona is a pioneering Washington estate whose four decades of consistent quality have established Red Mountain and Yakima Valley as world-class wine appellations. Their commitment to the Red Mountain terroir has made them essential to any understanding of Washington wine history.",
         price_positioning="mid_range")

prod3a1, new9 = PROD("Kiona Vineyards Estate Cabernet Sauvignon Red Mountain", "wine_still", p3a, r3, "USA",
                      subcategory="Cabernet Sauvignon", price_tier="mid_range",
                      description="From Kiona's historic Red Mountain estate, this Yakima Valley Cabernet delivers the sub-zone's signature combination of intense cassis, firm tannin, and mineral depth. One of Washington's most authentic expressions of Red Mountain Cabernet, aged in American and French oak for accessibility with structure.")
if new9:
    PAIR(prod3a1, "Grilled ribeye with compound herb butter and roasted potatoes", "complement", "classic", "main", "Yakima Valley Cabernet and Pacific Northwest beef is a regional benchmark; compound herb butter echoes the wine's herbal character while roasted potatoes provide the starchy foil that softens the tannin.")
    PAIR(prod3a1, "Elk medallions with huckleberry sauce and celeriac", "complement", "classic", "main", "Pacific Northwest game and Washington Cabernet is a regional pairing of genuine authenticity; huckleberry's tartness echoes the wine's dark fruit while elk's lean intensity demands the structure of Red Mountain Cabernet.")
    PAIR(prod3a1, "Smoked brisket with Yakima Valley cherry barbecue sauce", "complement", "classic", "main", "The wine's dark cherry and firm structure are ideal for smoked brisket; Yakima Valley cherries in the BBQ sauce create a regional bridge between the wine's fruit and the meat's smokiness.")
    PAIR(prod3a1, "Aged Tillamook Cheddar with dried Yakima cherries and walnuts", "complement", "established", "cheese", "A Pacific Northwest cheese board with local cherries mirrors the wine's dark-fruit character; Tillamook's aged sharpness finds traction against the Cabernet's firm tannin while walnuts add savoury depth.")

prod3a2, new10 = PROD("Kiona Vineyards Lemberger Yakima Valley", "wine_still", p3a, r3, "USA",
                       subcategory="Lemberger", price_tier="mid_range",
                       description="Washington's most distinctive red variety, Lemberger (Blaufränkisch) produces wines of vibrant acidity, red cherry, and spice in Yakima Valley's continental climate. Kiona's Lemberger is a benchmark — genuinely approachable yet with enough structure and character to stand alongside any Pacific Northwest red.")
if new10:
    PAIR(prod3a2, "Grilled pork chops with apple chutney and sauerkraut", "complement", "classic", "main", "Lemberger's bright acidity and cherry character find a Central European-inspired match with pork and apple; sauerkraut's fermented tartness echoes the wine's own acidity while apple chutney bridges its fruit.")
    PAIR(prod3a2, "Wild mushroom and herb frittata with local goat cheese", "complement", "established", "casual", "The wine's versatility and medium weight are ideal for egg preparations; mushrooms echo its earthy character while local goat cheese adds the tangy counterpoint that amplifies its acidity.")
    PAIR(prod3a2, "Roasted duck with cherry sauce and potato gratin", "complement", "classic", "main", "Lemberger's cherry fruit and spice are natural companions for duck; cherry sauce creates a direct flavour bridge while potato gratin's cream richness is balanced by the wine's bright acidity.")
    PAIR(prod3a2, "Grilled Bavarian-style sausages with mustard and pretzel bread", "complement", "established", "casual", "The wine's Central European heritage and cherry character are ideally matched to Bavarian sausage; mustard's pungency amplifies the wine's spice while pretzel bread grounds the combination.")

p3b = P("Owen Roe Winery", "winery", r3, "USA",
         production_philosophy="artisanal",
         philosophy_description="Owen Roe produces wines from both Oregon and Washington, with their Yakima Valley Cabernet and Red Willow Vineyard wines demonstrating the Pacific Northwest's capacity for artisanal quality across state lines.",
         reputation_narrative="Owen Roe is respected throughout the Pacific Northwest for their multi-regional approach, producing wines that capture the distinct terroir expression of specific Yakima Valley and Willamette Valley sites with genuine craft.",
         price_positioning="mid_range")

prod3b1, new11 = PROD("Owen Roe Abbot's Table Red Yakima Valley", "wine_still", p3b, r3, "USA",
                       subcategory="Red blend", price_tier="mid_range",
                       description="A Yakima Valley-sourced red blend in the classic Pacific Northwest style: Cabernet Sauvignon, Merlot, and Syrah delivering generous dark fruit, chocolate, and spice with supple tannin and a long, warming finish. An excellent introduction to Yakima Valley's diverse red wine potential.")
if new11:
    PAIR(prod3b1, "Grilled lamb burgers with tzatziki and roasted pepper", "complement", "established", "casual", "The wine's accessible fruit and gentle structure are ideal for a well-made lamb burger; tzatziki's yogurt bridges the wine's acidity while roasted pepper adds Mediterranean sweetness.")
    PAIR(prod3b1, "Beef and mushroom stew with rustic bread", "complement", "classic", "main", "Yakima Valley's versatile red blend is an ideal everyday companion for hearty beef stew; mushroom's umami deepens the wine's own earthy character while bread absorbs the rich braising liquid.")
    PAIR(prod3b1, "BBQ chicken with smoky rub and corn on the cob", "complement", "established", "casual", "The wine's generous fruit and medium tannin handle BBQ chicken's smokiness with ease; corn on the cob adds sweetness that bridges the wine's dark fruit while the smoky rub echoes its spice.")
    PAIR(prod3b1, "Aged Manchego with cherry preserves and almonds", "complement", "established", "cheese", "The wine's dark cherry and chocolate find resonance with Manchego's nuttiness; cherry preserves mirror the wine's fruit while almonds provide the savoury-bitter depth that extends the finish.")

prod3b2, new12 = PROD("Owen Roe DuBrul Vineyard Cabernet Sauvignon Yakima", "wine_still", p3b, r3, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="premium",
                       description="From the famous DuBrul Vineyard in the Yakima Valley, considered one of Washington's finest vineyard sites. The wine delivers focused cassis, graphite, and floral notes with a firm, age-worthy structure that reflects DuBrul's exceptional growing conditions.")
if new12:
    PAIR(prod3b2, "Slow-roasted prime rib with horseradish cream and Yorkshire pudding", "complement", "classic", "main", "DuBrul Cabernet's focus and structure demand this most classic of roast beef preparations; horseradish cream provides the pungent contrast that keeps the luxury pairing vibrant while Yorkshire pudding absorbs the rich juices.")
    PAIR(prod3b2, "Rack of lamb with herb crust and Washington wine reduction", "complement", "classic", "main", "DuBrul Cabernet and Washington lamb rack is a Pacific Northwest prestige pairing; the wine reduction creates a regional bridge while herb crust echoes the wine's herbal complexity.")
    PAIR(prod3b2, "Wild Pacific mushroom and truffle risotto with Parmesan", "complement", "established", "main", "The wine's focused cassis and graphite find an unexpected harmony with Pacific mushroom and truffle; Parmesan's umami bridges the tannin while risotto's creaminess softens the wine's structure.")
    PAIR(prod3b2, "Aged Tillamook Vintage White Cheddar with Bing cherry jam", "complement", "established", "cheese", "DuBrul Cabernet's graphite and cassis find resonance with this aged Pacific Northwest cheddar; Bing cherry jam — grown in the Yakima Valley — creates a regional bridge between wine and cheese.")

# ── 4. Red Mountain AVA ──────────────────────────────────────────────────────
print("=== Red Mountain AVA ===")
r4 = R("Red Mountain AVA", "USA", "wine",
        designation_type="AVA", designation_name="Red Mountain",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Red Mountain, a small southwest-facing ridge within Yakima Valley in Washington State, is the state's most prestigious wine appellation — tiny at just 4,040 acres, yet producing some of America's finest Cabernet Sauvignon. The AVA's high mineral content soils, intense sun exposure, and warm temperatures produce wines of extraordinary concentration, tannin, and ageing potential that have propelled Washington's reputation to world-class status.",
        key_producers="Quilceda Creek (Red Mountain), Col Solare, Betz Family Winery, Hedges Family Estate, Cadence",
        historical_context="Red Mountain's viticultural history began in the 1970s with Kiona Vineyards, but its international reputation as Washington's premier sub-appellation was cemented through the extraordinary critical success of Quilceda Creek's Red Mountain Cabernet and Col Solare — the collaboration between Château Ste. Michelle and Antinori — in the early 2000s. The AVA's tiny size (a fraction of Napa Valley) and singular terroir have made Red Mountain Washington's most sought-after and expensive wine appellation.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "rising")]:
    VIN(r4, yr, qd, pt)

p4a = P("Col Solare Winery", "winery", r4, "USA",
         production_philosophy="classical",
         philosophy_description="Col Solare is the result of a collaboration between Chateau Ste. Michelle and Antinori of Tuscany, combining Washington's finest Red Mountain fruit with Antinori's Italian winemaking philosophy. The result is a Cabernet Sauvignon-dominated blend of remarkable elegance and concentration from one of America's most prestigious wine sites.",
         reputation_narrative="Col Solare has achieved world-class recognition as one of Washington State's finest wines, combining the intensity of Red Mountain terroir with the refinement of Italian winemaking. The Antinori-Ste. Michelle collaboration has produced a wine that regularly earns 95+ scores.",
         price_positioning="ultra_premium")

prod4a1, new13 = PROD("Col Solare Red Mountain", "wine_still", p4a, r4, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                       description="The flagship Ste. Michelle-Antinori collaboration, a Cabernet Sauvignon-dominated blend from the Red Mountain hilltop estate. Col Solare displays the unique combination of Red Mountain's concentration and mineral depth with Antinori's Italian elegance: dense cassis, graphite, cedar, and a tannin structure built for 15-20 years of cellaring.")
if new13:
    PAIR(prod4a1, "Bistecca Fiorentina with Tuscan olive oil and rosemary", "complement", "classic", "main", "The Antinori-Washington collaboration makes Florentine-style beef an ideal pairing; the Italian-influenced wine's cassis and cedar find resonance with the T-bone's charred intensity while rosemary echoes its herbal complexity.")
    PAIR(prod4a1, "Slow-roasted lamb saddle with black olive jus and polenta", "complement", "classic", "main", "Col Solare's prestige demands this level of preparation; black olive jus adds the Mediterranean depth that bridges the wine's Italian-Washington character while polenta grounds the pairing.")
    PAIR(prod4a1, "Wagyu beef short rib with truffle and Parmesan polenta", "complement", "classic", "main", "Red Mountain's finest Cabernet demands wagyu's extraordinary marbling; truffle deepens the earthy mineral resonance while Parmesan polenta adds the Italian character that reflects the wine's heritage.")
    PAIR(prod4a1, "Aged Parmigiano-Reggiano with Bing cherry preserve and truffle", "complement", "established", "cheese", "The Italian-Washington collaboration finds its cheese companion in Italy's greatest aged cheese; Bing cherry preserve from Yakima Valley's orchards creates a regional bridge while truffle deepens the earthy resonance.")

prod4a2, new14 = PROD("Hedges Family Estate CMS Red Mountain", "wine_still", p4a, r4, "USA",
                       subcategory="Cabernet Sauvignon blend", price_tier="mid_range",
                       description="The CMS (Cabernet-Merlot-Syrah) from Hedges Family Estate on Red Mountain is one of the AVA's most accessible wines, delivering the sub-zone's characteristic concentration and structure in an earlier-drinking style — Red Mountain terroir at a value price point that has introduced many wine lovers to the appellation.")
if new14:
    PAIR(prod4a2, "Grilled beef burgers with aged Cheddar and caramelised onions", "complement", "classic", "casual", "Red Mountain's accessibility and dark-fruit character are ideal for an elevated burger; aged Cheddar adds sharpness while caramelised onions' sweetness bridges the wine's cassis depth.")
    PAIR(prod4a2, "Barbecued pulled pork with Washington cherry BBQ sauce", "complement", "classic", "casual", "The wine's dark cherry and generous structure are a natural companion for pulled pork; Washington cherry BBQ sauce creates a regional connection that bridges the wine's fruit and the meat's smokiness.")
    PAIR(prod4a2, "Roasted chicken thighs with herbs and roasted vegetables", "complement", "classic", "main", "CMS's accessible structure and dark fruit are ideal for a well-made roast chicken; herbs echo the wine's aromatic character while roasted vegetables add sweetness that softens the tannin.")
    PAIR(prod4a2, "Sharp Cheddar and Gouda board with Pacific Northwest honey", "complement", "established", "cheese", "The wine's accessible Red Mountain character and dark fruit pair well with the cheese board's variety; Pacific Northwest honey adds the sweet bridge that softens the wine's tannin.")

p4b = P("Betz Family Winery", "winery", r4, "USA",
         production_philosophy="artisanal",
         philosophy_description="Bob Betz MW established this small family winery to produce Red Mountain and Columbia Valley wines of the highest quality, with a focus on Bordeaux and Rhône varieties that express Washington State's unique volcanic terroir.",
         reputation_narrative="Betz Family Winery is one of Washington State's most respected small producers, with Bob Betz's Master of Wine credentials and meticulous approach producing wines of consistent excellence that appear on the lists of the Pacific Northwest's finest restaurants.",
         price_positioning="premium")

prod4b1, new15 = PROD("Betz Family Père de Famille Cabernet Sauvignon Red Mountain", "wine_still", p4b, r4, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="premium",
                       description="Bob Betz MW's flagship Red Mountain Cabernet, produced from the finest Columbia and Yakima Valley sites. Père de Famille displays an Old World-influenced restraint unusual in Washington: graphite, cassis, and cedar with firm but refined tannin that rewards a decade of cellaring.")
if new15:
    PAIR(prod4b1, "Roasted rack of lamb with mint jelly and roasted garlic", "complement", "classic", "main", "Betz's Old World-influenced Cabernet and roasted lamb rack is a classic pairing that bridges European tradition and Pacific Northwest terroir; mint jelly adds the traditional contrast while roasted garlic provides savoury depth.")
    PAIR(prod4b1, "Grilled duck breast with black currant sauce and potato gratin", "complement", "established", "main", "The wine's restrained power and cassis depth find a natural match in duck with blackcurrant; potato gratin's cream richness is balanced by the wine's firm acidity while the currant sauce bridges its fruit.")
    PAIR(prod4b1, "Beef tenderloin with wild mushroom jus and roasted asparagus", "complement", "classic", "main", "Père de Famille's elegant Cabernet finds its most natural expression with beef tenderloin; mushroom jus deepens the earthy connection while asparagus adds the vegetable minerality that mirrors the wine's graphite character.")
    PAIR(prod4b1, "Aged Manchego with Bing cherry preserve and Marcona almonds", "complement", "established", "cheese", "The wine's cassis and restrained elegance find resonance with aged Manchego; Bing cherry preserve echoes the wine's fruit while Marcona almonds add the savoury-bitter note that extends the finish.")

prod4b2, new16 = PROD("Betz Family Clos de Betz Red Mountain", "wine_still", p4b, r4, "USA",
                       subcategory="Merlot blend", price_tier="premium",
                       description="A Merlot-dominated blend from Red Mountain, displaying the sub-zone's signature density in a slightly softer, more accessible style: plum, dark cherry, and mocha with supple tannin that drinks earlier than the Père de Famille Cabernet while maintaining serious depth.")
if new16:
    PAIR(prod4b2, "Duck confit with lentils du Puy and Bing cherry reduction", "complement", "classic", "main", "Merlot's plum and mocha character are natural companions for duck confit; Bing cherry reduction bridges the wine's fruit while lentils add the earthy depth that grounds the pairing.")
    PAIR(prod4b2, "Roasted pork tenderloin with dried cherry and port reduction", "complement", "established", "main", "The wine's plum and dark-cherry character find a direct bridge with dried cherry and port; pork tenderloin's lean richness provides the protein base that the wine's supple tannin can embrace.")
    PAIR(prod4b2, "Double cream Brie with fig jam and toasted hazelnuts", "complement", "established", "cheese", "Merlot's plum and mocha character find a rich partner in double cream brie; fig jam bridges the wine's dark fruit while hazelnuts echo its mocha depth in an accessible, elegant combination.")
    PAIR(prod4b2, "Wild mushroom and Gruyère tart with thyme", "complement", "established", "main", "Clos de Betz's plum and mocha depth find resonance with mushroom and Gruyère; thyme adds the herbal note that echoes the wine's complexity while the tart's pastry provides textural contrast.")

# ── 5. Bodega Garzón (Uruguay) ────────────────────────────────────────────────
print("=== Garzon Wine Region (Uruguay) ===")
r5 = R("Garzon Wine Region", "Uruguay", "wine",
        designation_type="region", designation_name="Garzon",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Uruguay's wine region, centred on Montevideo and the southeast coastal zones near the Garzon lagoon, produces Tannat — the country's signature grape — of extraordinary depth and character. Uruguay's maritime climate moderates the heat, producing Tannat wines far more elegant than the variety's native Madiran home in southwestern France. The country has established itself as South America's most distinctive wine country.",
        key_producers="Bodega Garzón, Establecimiento Juanicó, Pisano Winery, Carrau Winery",
        historical_context="Tannat arrived in Uruguay with Basque immigrants in the 1870s, quickly adapting to the country's maritime climate and Atlantic soils. Where Madiran's Tannat is often harsh and tannic, Uruguay's Tannat — softened by maritime influence and longer hang time — produces wines of unexpected elegance. Bodega Garzón's recent international investment and world-class facilities have transformed Uruguay's global wine profile, with Garzón Tannat Reserve receiving global critical acclaim.")

for yr, qd, pt in [
    (2018, "excellent", "rising"), (2019, "excellent", "rising"), (2020, "very_good", "stable"),
    (2021, "exceptional", "rising"), (2022, "excellent", "rising")]:
    VIN(r5, yr, qd, pt)

p5a = P("Bodega Garzón", "winery", r5, "Uruguay",
         production_philosophy="sustainable",
         philosophy_description="Bodega Garzón, built by Alejandro Bulgheroni with investment that has made it one of South America's most technically advanced wineries, produces Tannat and Albariño from Uruguay's southeast coastal zone with biodynamic farming principles and precision winemaking.",
         reputation_narrative="Bodega Garzón has transformed Uruguay's international wine reputation, with Wine Enthusiast naming it 2019 New World Winery of the Year. Their Single Vineyard Tannat is considered the finest expression of the variety outside Madiran and has placed Uruguay firmly on the global fine wine map.",
         price_positioning="premium")

prod5a1, new17 = PROD("Bodega Garzón Single Vineyard Tannat Uruguay", "wine_still", p5a, r5, "Uruguay",
                       subcategory="Tannat", price_tier="premium",
                       description="Uruguay's benchmark Tannat, from biodynamically farmed granite and gneiss hillside plots above the Garzon lagoon. This single-vineyard expression displays Tannat's maritime Uruguayan character: dark plum, blueberry, and graphite with notably softer tannin than Madiran and a long, mineral finish that reflects the Atlantic coastal influence.")
if new17:
    PAIR(prod5a1, "Asado Uruguayo — beef short ribs and chorizos over wood fire", "complement", "classic", "main", "Uruguay's Tannat over the national barbecue tradition is the country's defining food and wine pairing; the wine's dark fruit and firm-but-supple tannin frame the asado's varied preparations while the wood smoke adds depth.")
    PAIR(prod5a1, "Chivito al pan (Uruguay's national sandwich with beef, egg, and ham)", "complement", "classic", "casual", "The chivito is Uruguay's most beloved sandwich; Garzón Tannat's dark fruit and structure are a bold but authentic companion, the wine's tannin cutting through the egg and cured meat richness.")
    PAIR(prod5a1, "Slow-braised lamb shoulder with chimichurri and mashed potato", "complement", "classic", "main", "Tannat's dark depth and firm tannin demand slow-cooked meat; chimichurri's herb brightness provides the contrast while mashed potato's richness softens the wine's structure.")
    PAIR(prod5a1, "Aged Colonia cheese with Uruguayan quince paste and walnuts", "complement", "established", "cheese", "Uruguay's own aged cheese with the country's signature wine is a pairing of authentic regional identity; quince paste bridges the wine's dark fruit while walnuts echo its earthy depth.")

prod5a2, new18 = PROD("Bodega Garzón Reserve Albariño Uruguay", "wine_still", p5a, r5, "Uruguay",
                       subcategory="Albariño", price_tier="mid_range",
                       description="An unusual but compelling expression of Albariño in Uruguay's maritime climate, displaying the variety's characteristic stone fruit and saline mineral character with an additional Atlantic Ocean freshness. One of South America's most distinctive white wine personalities.")
if new18:
    PAIR(prod5a2, "Grilled corvina (drum fish) with lemon and olive oil", "complement", "classic", "fish_course", "Uruguay's Atlantic coastal fish with Garzón Albariño is a genuine maritime pairing; the wine's saline mineral character echoes the fish's ocean origin while lemon bridges its citrus acidity.")
    PAIR(prod5a2, "Paella de mariscos with saffron and Uruguayan seafood", "complement", "established", "main", "Albariño's mineral freshness and stone-fruit character are natural companions for seafood paella; saffron's floral mineral note echoes the wine's own character while the seafood's brine bridges its saline depth.")
    PAIR(prod5a2, "Sea bass ceviche with lime, ají, and coriander", "complement", "established", "starter", "The wine's citrus acidity and saline mineral character are ideal for ceviche's lime-cured freshness; ají's warmth provides the contrast that keeps the pairing vibrant while coriander adds aromatic freshness.")
    PAIR(prod5a2, "Fresh oysters with mignonette and sea herbs", "complement", "classic", "aperitif", "Uruguay's Atlantic oysters with Atlantic-influenced Albariño is a maritime pairing of extraordinary coherence; mignonette's vinegar sharpens the wine's acidity while sea herbs echo the wine's own coastal mineral character.")

p5b = P("Pisano Family Wines", "winery", r5, "Uruguay",
         production_philosophy="artisanal",
         philosophy_description="Pisano is one of Uruguay's oldest family wine producers, with roots dating to 1924 and a commitment to traditional Tannat winemaking that has made them one of the country's most respected artisanal producers.",
         reputation_narrative="Pisano Family Wines represents the authentic heritage of Uruguayan winemaking, with their ARRETXEA and RPF Tannat wines demonstrating what the variety achieves in more traditional, family-scale production — less polished than Garzón but deeply expressive of Uruguayan Tannat's historic character.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Pisano RPF Tannat Uruguay", "wine_still", p5b, r5, "Uruguay",
                       subcategory="Tannat", price_tier="mid_range",
                       description="Pisano's flagship Tannat, from their family vineyards near Progreso in the Canelones region, displaying the variety's traditional Uruguayan character: dense dark fruit, firm tannin, and an earthy depth that reflects the Atlantic maritime influence on this robustly structured variety.")
if new19:
    PAIR(prod5b1, "Grilled black Angus steak with chimichurri and roasted peppers", "complement", "classic", "main", "Tannat's robust structure and dark fruit are the natural companion for South American grass-fed beef; chimichurri's herb brightness provides the contrast while roasted peppers add the sweetness that balances the tannin.")
    PAIR(prod5b1, "Slow-cooked lamb ribs with malbec and herb reduction", "complement", "established", "main", "Tannat's power and structure demand slow-cooked ribs; the Malbec reduction creates a wine-based bridge while herbs add the aromatic complexity that mirrors the wine's own depth.")
    PAIR(prod5b1, "Churrasco de costilla (beef rib grilled over wood)", "complement", "classic", "main", "Wood-grilled beef ribs are the everyday companion for Uruguayan Tannat; the wine's dark fruit and firm structure cut through the fat while the wood smoke adds a complementary depth.")
    PAIR(prod5b1, "Aged Queso Colonia with dulce de leche and toasted bread", "complement", "established", "cheese", "Uruguay's most beloved aged cheese with dulce de leche is a quintessentially Uruguayan combination; dulce de leche's caramel sweetness bridges the wine's dark fruit while aged Colonia's tang provides the contrast.")

prod5b2, new20 = PROD("Pisano ARRETXEA Tannat Reserva Uruguay", "wine_still", p5b, r5, "Uruguay",
                       subcategory="Tannat", price_tier="mid_range",
                       description="Pisano's reserve Tannat, aged in French oak for 18 months, displaying a more refined expression of the variety's power: dark cherry, blackberry, spice, and chocolate with softer, more integrated tannin that makes this one of Uruguay's most approachable premium Tannats.")
if new20:
    PAIR(prod5b2, "Braised beef cheeks with red wine and root vegetables", "complement", "established", "main", "ARRETXEA's refined Tannat and braised beef cheeks is an elevated Uruguayan pairing; the wine's chocolate depth and oak integration create a luxurious match for the slow-braised collagen richness.")
    PAIR(prod5b2, "Duck magret with blackberry reduction and polenta", "complement", "established", "main", "The wine's dark-cherry and chocolate character find a natural home with duck magret; blackberry reduction creates a direct flavour bridge while polenta absorbs the rich duck fat.")
    PAIR(prod5b2, "Rack of lamb with Uruguayan herbs and roasted vegetables", "complement", "classic", "main", "Reserve Tannat's refined power is well-matched to rack of lamb; the wine's structure frames the lamb's richness while local herbs echo its own aromatic character in a genuinely Uruguayan expression.")
    PAIR(prod5b2, "Aged manchego and Colonia cheese board with local honey", "complement", "established", "cheese", "The wine's refined tannin and dark fruit find resonance with both Spanish Manchego and Uruguayan aged Colonia; local honey bridges both cheeses with the wine's sweetness.")

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
print("B151 complete.")
conn.close()
