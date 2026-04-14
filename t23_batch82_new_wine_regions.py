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

# ── Region 1: Gevrey-Chambertin ──────────────────────────────────────────────
print("\n=== Region 1: Gevrey-Chambertin ===")
r1 = R("Gevrey-Chambertin", "France", "wine",
    designation_type="AOC",
    designation_name="Gevrey-Chambertin AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="The largest and most storied commune in the Côte de Nuits, home to nine Grand Crus including Chambertin and Clos de Bèze — vineyards Napoleon reportedly never marched without. The village's limestone-clay soils produce Pinot Noir of unmatched structure, depth, and aging potential, with a characteristic earthy power that distinguishes it from its neighbours.",
    key_producers="Rousseau, Leroy, Denis Mortet, Rossignol-Trapet, Faiveley",
    historical_context="Chambertin's fame dates to the 12th century via Cistercian monks of Clos de Bèze; Napoleon's devotion amplified the commune's prestige across Europe.")

for yr, qd, pt in [
    (2023, "very_good", "rising"), (2022, "exceptional", "rising"),
    (2021, "excellent", "stable"), (2020, "exceptional", "stable"), (2019, "exceptional", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("Domaine Armand Rousseau", "winery", r1, "France",
    production_philosophy="traditional",
    philosophy_description="The benchmark Gevrey-Chambertin estate, holding Chambertin, Clos de Bèze, and six further Grand Crus. Rousseau's wines are the gold standard of the Côte de Nuits — silky, precise, and hauntingly mineral.",
    reputation_narrative="Universally cited as Burgundy's reference estate; allocations distributed to a small global list of loyal buyers.",
    price_positioning="ultra_premium")

prod1b_id = P("Denis Mortet", "winery", r1, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Founded by the late Denis Mortet, now run by son Arnaud, this domaine produces Gevrey's most concentrated and modern expressions — rich, structured, and deeply aromatic Village to Grand Cru wines.",
    reputation_narrative="One of Gevrey's most dynamic estates; Arnaud Mortet has continued his father's legacy of quality and precision.",
    price_positioning="ultra_premium")

prod1a, new1a = PROD("Armand Rousseau Chambertin Grand Cru", "wine_still", prod1a_id, r1, "France",
    subcategory="Pinot Noir",
    description="The greatest wine of Gevrey-Chambertin and one of Burgundy's most coveted bottles — Rousseau's Chambertin combines extraordinary concentration with ethereal finesse, requiring two decades to fully open.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Roasted Bresse chicken with black truffle butter under the skin", "elevate", "classic", "main",
         "Burgundy's ultimate table — Chambertin and Bresse chicken share the same hallowed terroir and mutual elevation.")
    PAIR(prod1a, "Braised short rib with celeriac purée and bone marrow gremolata", "complement", "established", "main",
         "Grand Cru structure and depth equal the richness of braised beef collagen; marrow echoes the wine's body.")
    PAIR(prod1a, "Époisses aged cheese with baguette", "bridge", "classic", "cheese",
         "Burgundy's great cheese with Burgundy's great wine — pungent, washed-rind Époisses meets Pinot's red-fruit depth.")
    PAIR(prod1a, "Wild hare à la royale with foie gras and cognac", "complement", "classic", "main",
         "The grandest game preparation in French cuisine requires the grandest Burgundy in equal measure.")

prod1b, new1b = PROD("Denis Mortet Gevrey-Chambertin Village", "wine_still", prod1b_id, r1, "France",
    subcategory="Pinot Noir",
    description="A concentrated, aromatic village Gevrey from old vines across the commune — dark cherry, violets, and iron minerality with Mortet's signature richness and structure at an approachable tier.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Duck leg confit with lentils du Puy and lardon", "complement", "classic", "main",
         "Classic French bistro pairing — confit richness meets Pinot's red-fruit and earthy structure.")
    PAIR(prod1b, "Mushroom velouté with black truffle and crème fraîche", "elevate", "established", "starter",
         "Earthiness amplifies both ways — Gevrey's iron-mineral note meets fungal umami in perfect accord.")
    PAIR(prod1b, "Grilled salmon pavé with pinot noir reduction", "bridge", "established", "fish_course",
         "Village Pinot's lighter body bridges the fatty richness of salmon in a classic contemporary pairing.")
    PAIR(prod1b, "Comté 18-month with toasted hazelnuts", "complement", "established", "cheese",
         "Aged Comté's nutty-crystalline texture aligns with the wine's depth and mineral complexity.")

# ── Region 2: Vosne-Romanée ──────────────────────────────────────────────────
print("\n=== Region 2: Vosne-Romanée ===")
r2 = R("Vosne-Romanée", "France", "wine",
    designation_type="AOC",
    designation_name="Vosne-Romanée AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Perhaps the most fabled wine village on earth, home to Romanée-Conti, La Tâche, Richebourg, and four other Grand Crus. Vosne-Romanée Pinot Noir is the apex of complexity, combining red-fruit delicacy with extraordinary depth, florality, and an almost spiritual expression of limestone-clay terroir over weathered Jurassic limestone.",
    key_producers="DRC, Leroy, Méo-Camuzet, Anne Gros, Emmanuel Rouget",
    historical_context="The Romanée-Conti vineyard was purchased by the Prince de Conti in 1760 specifically to deny it to Madame de Pompadour; its fame as the world's most expensive wine was already established by the 18th century.")

for yr, qd, pt in [
    (2023, "very_good", "rising"), (2022, "exceptional", "rising"),
    (2021, "exceptional", "stable"), (2020, "exceptional", "stable"), (2019, "exceptional", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Méo-Camuzet", "winery", r2, "France",
    production_philosophy="traditional",
    philosophy_description="One of Vosne's finest private estates, holding Cros Parantoux (shared with Henri Jayer's memory), Richebourg, and premier crus of exceptional quality. Jean-Nicolas Méo has refined the estate's wines toward purity and elegance.",
    reputation_narrative="Holder of Cros Parantoux and Richebourg; among Vosne's most sought-after estates after DRC and Leroy.",
    price_positioning="ultra_premium")

prod2b_id = P("Anne Gros", "winery", r2, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Anne Gros produces benchmark Vosne village wines and Richebourg Grand Cru, combining traditional long maceration with a modern emphasis on freshness and purity of fruit expression.",
    reputation_narrative="One of Vosne's most respected independent producers; Richebourg is a benchmark for the appellation.",
    price_positioning="ultra_premium")

prod2a, new2a = PROD("Méo-Camuzet Vosne-Romanée Cros Parantoux 1er Cru", "wine_still", prod2a_id, r2, "France",
    subcategory="Pinot Noir",
    description="Cros Parantoux is one of Burgundy's most storied premier crus — reclaimed from a former swamp by Henri Jayer. Méo-Camuzet's portion expresses extraordinary concentration and terroir transparency from old vines on steep limestone soil.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Pigeon rôti en croûte with black truffle and foie gras", "elevate", "classic", "main",
         "The pinnacle of French game cookery requires first-growth Burgundy; truffle bridges wine and bird.")
    PAIR(prod2a, "Slow-cooked venison shoulder with juniper and wild berries", "complement", "established", "main",
         "Wild game and Pinot share a forest-floor vocabulary; Vosne's elegance lifts without overwhelming.")
    PAIR(prod2a, "Beaufort d'Été with truffle honey", "complement", "established", "cheese",
         "Alpine cheese with summer character mirrors Cros Parantoux's floral, mineral depth.")
    PAIR(prod2a, "Sweetbreads in a Madeira cream with morel mushrooms", "bridge", "classic", "main",
         "Veal offal richness and Madeira's sweetness bridge perfectly with premier cru complexity.")

prod2b, new2b = PROD("Anne Gros Vosne-Romanée Village", "wine_still", prod2b_id, r2, "France",
    subcategory="Pinot Noir",
    description="Benchmark village Vosne-Romanée from Anne Gros — expressing the commune's characteristic violet, cherry, and iron-mineral complexity at the village level with precision and finesse.",
    price_tier="ultra_premium")
if new2b:
    PAIR(prod2b, "Coq au vin with pearl onions and lardons", "complement", "classic", "main",
         "The original Burgundy wine pairing — slow-cooked chicken in Pinot Noir sauce with the same wine in the glass.")
    PAIR(prod2b, "Pan-seared foie gras with cherry compote and brioche", "contrast", "established", "starter",
         "Village Vosne's cherry and acidity cut through foie's richness while echoing the cherry compote.")
    PAIR(prod2b, "Rabbit terrine with cornichons and Dijon", "bridge", "established", "starter",
         "Light, gamey rabbit terrine harmonises with Vosne's delicate Pinot without either overwhelming.")
    PAIR(prod2b, "Pont-l'Évêque cheese with walnut bread", "complement", "established", "cheese",
         "Normandy washed-rind cheese with complex Burgundy red — contrasting regions in complementary harmony.")

# ── Region 3: Gevrey-Chambertin sub (Chambolle-Musigny) ─────────────────────
print("\n=== Region 3: Chambolle-Musigny ===")
r3 = R("Chambolle-Musigny", "France", "wine",
    designation_type="AOC",
    designation_name="Chambolle-Musigny AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="The most feminine commune of the Côte de Nuits, producing Pinot Noir of extraordinary delicacy, perfume, and silky texture. Musigny Grand Cru and Les Amoureuses premier cru are two of Burgundy's most desired wines. The pure limestone soils and northeast-facing aspect create wines of haunting florality and gossamer tannin.",
    key_producers="Roumier, Mugnier, Leroy, Vogüé, de Vogue",
    historical_context="The Musigny vineyard was among Burgundy's earliest documented Grand Crus, recorded by Cistercian monks in the 12th century; the vineyard's ability to produce both red and an impossibly rare white Pinot Noir has fascinated collectors for centuries.")

for yr, qd, pt in [
    (2023, "very_good", "rising"), (2022, "exceptional", "rising"),
    (2021, "exceptional", "stable"), (2020, "excellent", "stable"), (2019, "exceptional", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Domaine Georges Roumier", "winery", r3, "France",
    production_philosophy="traditional",
    philosophy_description="Roumier is Chambolle's reference estate — holding Les Amoureuses, Bonnes-Mares, and Musigny, crafting wines of extraordinary purity and terroir expression through meticulous viticulture and classical cellar work.",
    reputation_narrative="Arguably Chambolle's greatest producer; Les Amoureuses is among Burgundy's most coveted premier crus.",
    price_positioning="ultra_premium")

prod3b_id = P("Domaine J.F. Mugnier", "winery", r3, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Frédéric Mugnier produces Chambolle's most ethereal wines from Musigny Grand Cru, Les Amoureuses, and a tiny parcel of white Musigny — emphasising restraint, transparency, and extreme vineyard expression.",
    reputation_narrative="Mugnier's Musigny is one of the world's most profound wines; collector demand far exceeds supply.",
    price_positioning="ultra_premium")

prod3a, new3a = PROD("Georges Roumier Chambolle-Musigny Les Amoureuses 1er Cru", "wine_still", prod3a_id, r3, "France",
    subcategory="Pinot Noir",
    description="Les Amoureuses — 'the lovers' — is Chambolle's most romantic vineyard and arguably Burgundy's finest premier cru. Roumier's portion produces wine of extraordinary perfume, silky texture, and Grand Cru-level complexity.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Roasted squab with rose hip jus and violet reduction", "elevate", "classic", "main",
         "Chambolle's celebrated floral character — violets and rose petals — echoed in the preparation itself.")
    PAIR(prod3a, "Grilled sea bass with beurre blanc and fine herbs", "complement", "adventurous", "fish_course",
         "Chambolle's silky texture and light body bridge the gap between red wine and fine white fish.")
    PAIR(prod3a, "Rabbit saddle with tarragon cream and wild mushrooms", "complement", "established", "main",
         "Delicate game with herbal cream mirrors the wine's light-bodied florality without overwhelming.")
    PAIR(prod3a, "Langres cheese with a splash of Champagne", "bridge", "classic", "cheese",
         "Langres with bubbles is a classic Burgundian aperitif; Les Amoureuses offers a more complex bridge.")

prod3b, new3b = PROD("J.F. Mugnier Chambolle-Musigny Village", "wine_still", prod3b_id, r3, "France",
    subcategory="Pinot Noir",
    description="Mugnier's village Chambolle epitomises the commune's style — gossamer tannin, violets, red cherry, and mineral precision; a genuine gateway to understanding Chambolle's delicate terroir expression.",
    price_tier="ultra_premium")
if new3b:
    PAIR(prod3b, "Chicken suprême poached in Chambolle Pinot", "bridge", "classic", "main",
         "Regional harmony — delicate chicken poached in the same grape variety as the wine in the glass.")
    PAIR(prod3b, "Smoked duck breast with cherry gel and hazelnut", "complement", "established", "main",
         "Chambolle's cherry-rose character bridges smoke and cherry in the preparation with elegant ease.")
    PAIR(prod3b, "Brie de Meaux at peak ripeness with walnuts", "complement", "classic", "cheese",
         "Soft, ripe Brie with silky Chambolle Pinot — both share a delicate, yielding texture and richness.")
    PAIR(prod3b, "Tartare of tuna with sesame and ginger", "contrast", "adventurous", "starter",
         "Silky Chambolle Pinot's red-fruit acidity contrasts and refreshes against raw tuna's oceanic depth.")

# ── Region 4: Nuits-Saint-Georges ───────────────────────────────────────────
print("\n=== Region 4: Nuits-Saint-Georges ===")
r4 = R("Nuits-Saint-Georges", "France", "wine",
    designation_type="AOC",
    designation_name="Nuits-Saint-Georges AOC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="The commercial capital of the Côte de Nuits, producing robust, earthy, and structured Pinot Noir from two distinct sectors: the northern sector bordering Vosne (lighter, more elegant) and the southern sector bordering Premeaux (denser, more tannic). No Grand Crus but 41 premier cru vineyards. Wines are built for long aging and food-friendly structure.",
    key_producers="Gouges, Chevillon, Leroy, Michel Gros, Jayer-Gilles",
    historical_context="Nuits-Saint-Georges gained renown in the 18th century when Louis XIV's physician reportedly prescribed the wine for the king's ailments; the town added 'Saint-Georges' to its name after its most famous premier cru in 1892.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "excellent", "stable"),
    (2020, "exceptional", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Domaine Henri Gouges", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="The historic Gouges estate is the standard-bearer of Nuits-Saint-Georges, holding five premier crus including the rare Pinot Blanc mutation in Les Perrières. Pierre and Christian Gouges maintain traditional large-format cellar practices.",
    reputation_narrative="Nuits-Saint-Georges reference estate since the early 20th century; Les Saint-Georges is a benchmark premier cru.",
    price_positioning="premium")

prod4b_id = P("Domaine Robert Chevillon", "winery", r4, "France",
    production_philosophy="traditional",
    philosophy_description="Robert Chevillon and sons produce authentic, old-vine Nuits from premier cru sites Les Saint-Georges, Les Vaucrains, and Les Cailles — structured wines with earthy depth and classical Nuits robustness.",
    reputation_narrative="Among Nuits-Saint-Georges' most respected family estates; vines averaging 50+ years.",
    price_positioning="premium")

prod4a, new4a = PROD("Henri Gouges Nuits-Saint-Georges Les Saint-Georges 1er Cru", "wine_still", prod4a_id, r4, "France",
    subcategory="Pinot Noir",
    description="Les Saint-Georges is the premier cru many believe deserves Grand Cru elevation — deep red soils over limestone, producing dense, iron-mineral Pinot Noir of extraordinary concentration and longevity.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Beef bourguignon with button mushrooms and pearl onions", "complement", "classic", "main",
         "The defining Burgundian stew paired with Nuits's robust, earthy Pinot — a regional archetype.")
    PAIR(prod4a, "Roasted rack of venison with blackcurrant jus", "complement", "established", "main",
         "Game meets robust premier cru — blackcurrant echoes the wine's fruit while venison matches its structure.")
    PAIR(prod4a, "Pâté en croûte with pistachios and duck liver", "bridge", "established", "starter",
         "Rich charcuterie with earthy wine — the iron-mineral note bridges pâté's savoury depth.")
    PAIR(prod4a, "Munster with caraway seeds", "contrast", "suggested", "cheese",
         "Pungent Alsatian cheese with structured Nuits Pinot — a provocative pairing of power and funk.")

prod4b, new4b = PROD("Robert Chevillon Nuits-Saint-Georges Les Vaucrains 1er Cru", "wine_still", prod4b_id, r4, "France",
    subcategory="Pinot Noir",
    description="Les Vaucrains is Nuits' most powerful and tannic premier cru — red clay over limestone producing wines of extraordinary concentration and density, requiring at least a decade of cellaring to resolve.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Braised ox cheek with horseradish cream and red wine reduction", "complement", "classic", "main",
         "Les Vaucrains' powerful tannin structure handles the deep collagen richness with ease.")
    PAIR(prod4b, "Wild boar terrine with black pepper and cornichons", "complement", "established", "starter",
         "Rustic game terrine suits the earthy, iron-mineral character of this structured premier cru.")
    PAIR(prod4b, "Aged Mimolette with fig and hazelnut", "complement", "established", "cheese",
         "Hard aged Mimolette's caramel richness bridges with the wine's dark fruit and tannic backbone.")
    PAIR(prod4b, "Magret de canard with cherry compote and bitter chocolate jus", "complement", "established", "main",
         "Duck breast with dark accompaniments echoes the wine's depth, dark fruit, and bitter mineral finish.")

# ── Region 5: Pomerol ───────────────────────────────────────────────────────
print("\n=== Region 5: Pomerol ===")
r5 = R("Pomerol", "France", "wine",
    designation_type="AOC",
    designation_name="Pomerol AOC",
    reputation_tier="iconic",
    quality_trajectory="established",
    description="Bordeaux's smallest and most exclusive appellation on the Right Bank, producing Merlot-dominant wines of extraordinary opulence and complexity from a unique plateau of deep blue clay over iron-rich gravel ('crasse de fer'). No official classification but Pétrus is recognised as one of the world's greatest wines. The appellation's ~800 hectares produce the world's most coveted Merlot.",
    key_producers="Pétrus, Le Pin, Lafleur, Vieux Château Certan, Clinet",
    historical_context="Pomerol's rise to global prominence came only in the 20th century — largely through the promotion of négociant Jean-Pierre Moueix, who championed Pétrus internationally from the 1940s onwards.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "excellent", "stable"),
    (2020, "exceptional", "rising"), (2019, "exceptional", "stable"), (2018, "excellent", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Vieux Château Certan", "winery", r5, "France",
    production_philosophy="traditional",
    philosophy_description="Under Alexandre Thienpont, VCC produces Pomerol's most Cabernet-influenced wine — a rare Right Bank blend heavy in Cabernet Franc that delivers extraordinary complexity and aging potential, often described as Pomerol's answer to Pétrus for Cabernet lovers.",
    reputation_narrative="Regularly cited as Pomerol's second estate; the 2009 and 2010 are considered among the century's great wines.",
    price_positioning="ultra_premium")

prod5b_id = P("Clinet", "winery", r5, "France",
    production_philosophy="terroir_focused",
    philosophy_description="Clinet's deep clay plateau produces exceptionally concentrated, velvety Merlot that benefits from its proximity to Pétrus. Under Ronan Laborde's management, Clinet has reclaimed its position among Pomerol's finest estates.",
    reputation_narrative="Consistently placed among Pomerol's top tier estates; approachable yet age-worthy.",
    price_positioning="ultra_premium")

prod5a, new5a = PROD("Vieux Château Certan", "wine_still", prod5a_id, r5, "France",
    subcategory="Merlot-Cabernet Franc Blend",
    description="Pomerol's most distinctive wine — a Merlot-dominated blend with significant Cabernet Franc contribution creating extraordinary complexity, structure, and finesse. Silky texture with great aging potential from old vines on deep gravelly clay.",
    price_tier="ultra_premium")
if new5a:
    PAIR(prod5a, "Roast lamb with black truffle and potato dauphinoise", "complement", "classic", "main",
         "Right Bank Bordeaux's classic pairing — spring lamb with deep clay terroir wines is a Bordeaux tradition.")
    PAIR(prod5a, "Pan-roasted sweetbreads with morel cream and asparagus", "elevate", "classic", "main",
         "Delicate offal with spring garnishes meets Pomerol's silky texture in a French haute cuisine archetype.")
    PAIR(prod5a, "Truffle mac and cheese with aged Gruyère crust", "complement", "established", "main",
         "Indulgent luxury ingredient pairing — Pomerol's velvet texture mirrors the dish's cream and truffle.")
    PAIR(prod5a, "Roquefort with walnuts and honey on pain Poilâne", "contrast", "established", "cheese",
         "Blue cheese's bold saltiness contrasts with VCC's fruit depth while honey bridges both elements.")

prod5b, new5b = PROD("Clinet Pomerol", "wine_still", prod5b_id, r5, "France",
    subcategory="Merlot",
    description="A rich, opulent Pomerol from the appellation's clay core — concentrated dark plum, mocha, and violet with Clinet's signature velvety texture and long, structured finish. More approachable young than Pétrus while sharing similar terroir.",
    price_tier="ultra_premium")
if new5b:
    PAIR(prod5b, "Slow-roasted beef fillet with red wine reduction and bone marrow", "complement", "classic", "main",
         "Pomerol's lush Merlot texture mirrors the tender beef and amplifies the marrow's richness.")
    PAIR(prod5b, "Duck magret with figs, foie gras, and Port reduction", "complement", "established", "main",
         "Right Bank luxury pairing — duck, foie, and Merlot share a rich, fruit-forward vocabulary.")
    PAIR(prod5b, "Burrata with black truffle shavings and aged balsamic", "complement", "established", "starter",
         "Velvet Merlot texture mirrors creamy burrata; truffle unifies the plate and wine.")
    PAIR(prod5b, "Saint-Nectaire with black pepper and dried fruits", "complement", "established", "cheese",
         "Semi-soft Auvergne cheese with earthy pepper suits the velvet richness of Pomerol Merlot.")

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
