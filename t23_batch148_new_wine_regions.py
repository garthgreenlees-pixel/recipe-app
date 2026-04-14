#!/usr/bin/env python3
"""B148 — Central Otago (NZ), Hawke's Bay (NZ), Eden Valley (AU), McLaren Vale (AU), Columbia Valley AVA (WA)"""
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

# ── 1. Central Otago (New Zealand) ───────────────────────────────────────────
print("=== Central Otago (New Zealand) ===")
r1 = R("Central Otago", "New Zealand", "wine",
        designation_type="GI", designation_name="Central Otago",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Central Otago, in New Zealand's South Island, is the world's southernmost wine region and the only significant wine zone with a continental rather than maritime climate. At 200–450 metres elevation in a dramatic landscape of mountains and rivers, it produces Pinot Noir of extraordinary intensity, colour, and precision. The region's extreme diurnal temperature variation preserves remarkable natural acidity alongside powerful fruit.",
        key_producers="Felton Road, Mount Difficulty, Rippon, Quartz Reef, Ata Rangi",
        historical_context="Gold miners introduced viticulture to Central Otago in the 1860s, but serious wine production did not begin until the 1970s. The region's rapid rise to global prominence was spearheaded by Felton Road and Rippon in the 1990s, and today Central Otago Pinot Noir is considered one of the New World's definitive expressions of the variety.")

for yr, qd, pt in [
    (2019, "exceptional", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "exceptional", "rising"), (2023, "very_good", "rising")]:
    VIN(r1, yr, qd, pt)

p1a = P("Felton Road", "winery", r1, "New Zealand",
         production_philosophy="minimal_intervention",
         philosophy_description="Felton Road, established in 1992 on the Bannockburn Silt soil of Central Otago, has become one of New Zealand's most celebrated estates through its biodynamic farming, minimal intervention winemaking, and three distinctive single-vineyard Pinot Noirs.",
         reputation_narrative="Felton Road's Block 3, Block 5, and Calvert single-vineyard Pinot Noirs are among the southern hemisphere's most awarded wines, consistently earning 95+ point scores and appearing on the lists of the world's finest restaurants. The estate's biodynamic approach and site specificity have set the standard for Central Otago.",
         price_positioning="premium")

prod1a1, new1 = PROD("Felton Road Block 5 Pinot Noir Central Otago", "wine_still", p1a, r1, "New Zealand",
                      subcategory="Pinot Noir", price_tier="premium",
                      description="From Felton Road's oldest biodynamic block on the Bannockburn terrace, Block 5 is consistently one of Central Otago's most celebrated wines: intense ruby colour, wild cherry, violet, and earthy complexity with firm, precise tannin and remarkable ageing potential.")
if new1:
    PAIR(prod1a1, "Seared duck breast with cherry and lavender reduction", "complement", "classic", "main", "Block 5's cherry and violet character find their most natural expression with duck; lavender echoes the wine's floral lift while the cherry reduction creates a direct flavour bridge between glass and plate.")
    PAIR(prod1a1, "Roasted whole pigeon with wild mushroom and thyme jus", "complement", "classic", "main", "Felton Road's intense concentration and earthy complexity demand game bird of this delicacy; wild mushroom and thyme echo the wine's forest-floor character while the whole roast amplifies its spice.")
    PAIR(prod1a1, "New Zealand lamb rack with herb crust and red wine reduction", "complement", "classic", "main", "Central Otago Pinot and NZ lamb is the country's benchmark pairing; herb crust resonates with the wine's earthy depth while the reduction creates a wine-based bridge between plate and glass.")
    PAIR(prod1a1, "Aged Pinot Noir cheese from Whitestone Dairy with cherry compote", "complement", "established", "cheese", "A New Zealand celebration: Whitestone's washed-rind cheese matured with Pinot Noir finds its ideal companion in the glass; cherry compote bridges both while the wine's structure cuts the cheese's pungency.")

prod1a2, new2 = PROD("Felton Road Bannockburn Pinot Noir Central Otago", "wine_still", p1a, r1, "New Zealand",
                      subcategory="Pinot Noir", price_tier="premium",
                      description="The estate Bannockburn bottling, sourcing from multiple Felton Road blocks on the Bannockburn terrace. More accessible than the single blocks on release, the wine displays classic Central Otago character: vibrant red fruit, dried herb, and a silky, precisely structured finish.")
if new2:
    PAIR(prod1a2, "Pan-seared salmon with beetroot purée and citrus butter", "complement", "classic", "fish_course", "The wine's bright cherry and precise structure bridge salmon's richness; beetroot's earthy sweetness mirrors the wine's own earth character while citrus butter adds the acidity that lifts the pairing.")
    PAIR(prod1a2, "Mushroom and leek tart with aged Gruyère", "complement", "established", "main", "Felton Road's earthy, forest-floor character resonates with mushroom and leek; Gruyère's nuttiness adds the savoury depth that extends the wine's finish while the pastry provides textural contrast.")
    PAIR(prod1a2, "Venison medallions with blackcurrant sauce and celeriac", "complement", "classic", "main", "New Zealand venison and Central Otago Pinot is a regional benchmark; blackcurrant's tartness echoes the wine's dark-fruit character while celeriac's earthy sweetness softens the game's intensity.")
    PAIR(prod1a2, "Aged Camembert with cherry jam and hazelnut bread", "complement", "established", "cheese", "The wine's cherry and forest-floor depth find resonance with aged Camembert; cherry jam creates a direct flavour bridge while hazelnut bread's earthiness extends the wine's secondary character.")

p1b = P("Rippon Vineyard", "winery", r1, "New Zealand",
         production_philosophy="biodynamic",
         philosophy_description="Rippon, perched on the shores of Lake Wānaka, is one of New Zealand's most dramatically situated and spiritually motivated wineries. The Mills family has farmed biodynamically since 2003, producing Pinot Noir and Riesling from one of the country's most beautiful vineyard landscapes.",
         reputation_narrative="Rippon's Mature Vine Pinot Noir is one of New Zealand's most admired wines, combining the intensity of Central Otago with a unique lakeside terroir and decades of biodynamic farming that produces wines of singular complexity and sense of place.",
         price_positioning="premium")

prod1b1, new3 = PROD("Rippon Mature Vine Pinot Noir Lake Wānaka", "wine_still", p1b, r1, "New Zealand",
                      subcategory="Pinot Noir", price_tier="premium",
                      description="From mature vines on the shores of Lake Wānaka, Rippon's flagship Pinot Noir is a wine of extraordinary sense of place: lake-reflected light seems to infuse the wine's translucent colour, while its wild cherry, dried herbs, and fine mineral structure speak of biodynamic farming and one of the world's most stunning vineyard settings.")
if new3:
    PAIR(prod1b1, "Slow-roasted duck with cherry and star anise reduction", "complement", "classic", "main", "Rippon Pinot's cherry character and dried-herb depth are perfectly aligned with this preparation; star anise adds an aromatic dimension that mirrors the wine's own complex spice profile.")
    PAIR(prod1b1, "Wild hare terrine with preserved cherry and toasted brioche", "complement", "established", "starter", "The wine's wild, earthy character finds its match in hare terrine; preserved cherry echoes the wine's fruit while brioche's richness provides the luxurious contrast the wine's delicacy demands.")
    PAIR(prod1b1, "Lake Wānaka trout with brown butter, capers, and almonds", "complement", "established", "fish_course", "A pairing of profound local significance: the lake trout from Rippon's own waters with the estate's Pinot Noir creates a complete expression of place; brown butter and almonds deepen the savoury connection.")
    PAIR(prod1b1, "Aged sheep's milk cheese with wild thyme honey and walnuts", "complement", "classic", "cheese", "The wine's biodynamic earthiness and cherry depth find resonance with aged sheep's milk; thyme honey bridges the wine's herbal character while walnuts echo its earthy complexity.")

prod1b2, new4 = PROD("Rippon Emma's Block Riesling Central Otago", "wine_still", p1b, r1, "New Zealand",
                      subcategory="Riesling", price_tier="mid_range",
                      description="From the Emma's Block vineyard on Rippon's biodynamic estate, this Riesling displays the concentrated, mineral precision of Central Otago Riesling: lime blossom, white peach, and a saline mineral finish with natural residual sweetness that balances the variety's electric acidity.")
if new4:
    PAIR(prod1b2, "Seared scallops with lime butter and finger lime caviar", "complement", "classic", "fish_course", "The wine's lime and mineral character are a natural companion for scallops; finger lime's native citrus pearls echo the wine's own citrus depth while lime butter adds the richness that grounds the pairing.")
    PAIR(prod1b2, "Thai larb salad with pork, lime, and fresh herbs", "complement", "established", "casual", "Central Otago Riesling's concentrated citrus and slight sweetness navigate the heat and herb intensity of larb; lime bridges the wine's own acidity while the wine's residual sugar tames the chili.")
    PAIR(prod1b2, "Blue cheese and honey tart with walnut pastry", "complement", "classic", "cheese", "Riesling's sweetness and acidity are among the most powerful tools for blue cheese; honey bridges the wine's residual sweetness while walnut pastry adds the savoury-bitter depth the combination needs.")
    PAIR(prod1b2, "Smoked whitebait fritters with lemon and herb cream", "complement", "classic", "starter", "New Zealand whitebait is one of the country's iconic seasonal ingredients; the wine's lime acidity and mineral depth frame the delicate smoked fish while herb cream adds aromatic richness.")

# ── 2. Hawke's Bay (New Zealand) ─────────────────────────────────────────────
print("=== Hawke's Bay (New Zealand) ===")
r2 = R("Hawke's Bay", "New Zealand", "wine",
        designation_type="GI", designation_name="Hawke's Bay",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Hawke's Bay, on the east coast of New Zealand's North Island, is the country's second-largest and arguably most versatile wine region. The legendary Gimblett Gravels sub-zone — a warm, stony riverbed — produces world-class Cabernet Sauvignon, Merlot, and Syrah of remarkable concentration and complexity. Hawke's Bay also produces excellent Chardonnay from cooler sites.",
        key_producers="Craggy Range, Trinity Hill, Te Mata Estate, Elephant Hill, Vidal Estate",
        historical_context="Hawke's Bay's wine history dates to 1851 when Marist brothers established Mission Estate — still operating today as New Zealand's oldest winery. The modern era was defined by the 1997 discovery that the gravel bed of the old Ngaruroro River, now known as Gimblett Gravels, produced exceptional warm-climate reds. This sub-zone has since become New Zealand's most discussed terroir for Bordeaux varieties.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

p2a = P("Craggy Range Winery", "winery", r2, "New Zealand",
         production_philosophy="terroir_expression",
         philosophy_description="Craggy Range was founded in 1998 by Terry Peabody with the vision of creating a world-class New Zealand wine estate. Working with Steve Smith MW, the estate produces single-vineyard wines from Hawke's Bay and Martinborough that are benchmarks for their respective regions.",
         reputation_narrative="Craggy Range has become New Zealand's most internationally recognised estate through Le Sol Syrah and Sophia Merlot-Malbec from the Gimblett Gravels, alongside Aroha Pinot Noir from Te Muna Road in Martinborough. Their wines consistently earn 95+ scores and appear at the world's top restaurants.",
         price_positioning="premium")

prod2a1, new5 = PROD("Craggy Range Le Sol Syrah Gimblett Gravels", "wine_still", p2a, r2, "New Zealand",
                      subcategory="Syrah", price_tier="premium",
                      description="One of New Zealand's greatest red wines, Le Sol is a Gimblett Gravels Syrah of extraordinary depth and elegance: violet, black olive, white pepper, and dark fruit with a silky texture and a long, mineral finish. Consistently one of the southern hemisphere's most celebrated Syrah wines.")
if new5:
    PAIR(prod2a1, "Roasted lamb shoulder with olive tapenade and roasted tomatoes", "complement", "classic", "main", "Le Sol's olive and violet character find their most natural expression with lamb and olive; tapenade deepens the savoury connection while roasted tomatoes add Mediterranean sweetness.")
    PAIR(prod2a1, "Grilled duck breast with blueberry reduction and spiced lentils", "complement", "classic", "main", "Gimblett Gravels Syrah's violet and dark-fruit character are a natural match for duck; blueberry reduction mirrors the wine's fruit while spiced lentils echo its warm, peppery character.")
    PAIR(prod2a1, "Venison loin with black pepper crust and blackcurrant jus", "complement", "classic", "main", "Le Sol's white pepper and dark-fruit depth are perfectly aligned with pepper-crusted venison; blackcurrant jus echoes the wine's fruit while the game's iron character resonates with the wine's mineral spine.")
    PAIR(prod2a1, "Aged Manchego with black olive paste and sourdough", "complement", "established", "cheese", "The wine's olive character and structure find resonance with aged Manchego's nuttiness; black olive paste creates a direct flavour bridge while sourdough grounds the combination.")

prod2a2, new6 = PROD("Craggy Range Sophia Merlot-Malbec Gimblett Gravels", "wine_still", p2a, r2, "New Zealand",
                      subcategory="Merlot blend", price_tier="premium",
                      description="Named after Terry Peabody's wife, Sophia is a Merlot-dominant blend with Malbec from the Gimblett Gravels. The wine displays the gravels' characteristic warmth in a silky, plum-dark fruit expression with velvet tannin and a long, savoury finish.")
if new6:
    PAIR(prod2a2, "Beef fillet with roasted garlic butter and potato dauphinoise", "complement", "classic", "main", "Sophia's silky tannin and plum-dark fruit are perfectly calibrated for beef fillet; roasted garlic butter adds savoury depth while dauphinoise's cream richness is balanced by the wine's acidity.")
    PAIR(prod2a2, "NZ lamb rack with herb crust and Gimblett Gravels Merlot jus", "complement", "classic", "main", "A wine-region pairing: Sophia with Hawke's Bay lamb and a Merlot jus creates a complete terroir expression; herb crust resonates with the wine's own herbal notes while the reduction deepens the connection.")
    PAIR(prod2a2, "Wild mushroom and truffle risotto with aged Parmesan", "complement", "established", "main", "Sophia's plum depth and velvet texture are natural companions for truffle risotto; Parmesan's umami amplifies the savoury connection while the risotto's creaminess mirrors the wine's silkiness.")
    PAIR(prod2a2, "Double cream brie with fig jam and walnut bread", "complement", "established", "cheese", "The wine's plum and silky texture find resonance with ripe double cream brie; fig jam echoes the wine's dark fruit while walnut bread adds savoury earthiness.")

p2b = P("Te Mata Estate", "winery", r2, "New Zealand",
         production_philosophy="classical",
         philosophy_description="Te Mata is New Zealand's oldest continuously producing winery, established in 1896. Their Coleraine is considered New Zealand's most age-worthy red wine, while Elston Chardonnay is the country's benchmark for the variety.",
         reputation_narrative="Te Mata's Coleraine, a Cabernet Sauvignon-Merlot blend from Hawke's Bay, is consistently cited as New Zealand's greatest red wine — a wine that demonstrates Hawke's Bay's capacity to produce Bordeaux-quality reds with genuine New Zealand character.",
         price_positioning="premium")

prod2b1, new7 = PROD("Te Mata Coleraine Hawke's Bay", "wine_still", p2b, r2, "New Zealand",
                      subcategory="Cabernet Sauvignon blend", price_tier="premium",
                      description="New Zealand's most iconic red wine, a Cabernet Sauvignon-Merlot-Cabernet Franc blend from Te Mata's hillside vineyards. Coleraine is elegant rather than powerful, displaying the Bordeaux-influenced restraint that makes it New Zealand's most age-worthy red: cassis, cedar, dried herb, and a long, mineral finish.")
if new7:
    PAIR(prod2b1, "Slow-roasted lamb shoulder with herbs and vegetables", "complement", "classic", "main", "Coleraine's Bordeaux character and elegant restraint are a natural companion for roasted NZ lamb; herbs echo the wine's dried-herb character while slow cooking creates the richness the wine's tannin can absorb.")
    PAIR(prod2b1, "Beef tenderloin with wild mushroom sauce and gratin", "complement", "classic", "main", "Te Mata Coleraine's elegance and precision are ideal for this refined preparation; mushroom sauce deepens the earthy connection while gratin's cream richness is balanced by the wine's structure.")
    PAIR(prod2b1, "Aged Canterbury Cheddar with quince paste and hazelnuts", "complement", "established", "cheese", "New Zealand's finest Cabernet blend and aged NZ Cheddar is a national luxury pairing; quince paste bridges the wine's fruit while hazelnuts add savoury-nutty complexity.")
    PAIR(prod2b1, "Venison ragù with fresh pappardelle and truffle oil", "complement", "established", "main", "Coleraine's structure and dried-herb character navigate venison ragù with Burgundian composure; truffle oil deepens the earthy resonance while pappardelle absorbs the rich sauce.")

prod2b2, new8 = PROD("Te Mata Elston Chardonnay Hawke's Bay", "wine_still", p2b, r2, "New Zealand",
                      subcategory="Chardonnay", price_tier="premium",
                      description="New Zealand's benchmark Chardonnay, aged in French oak with wild fermentation, Elston delivers a full-bodied, complex style: ripe peach, toasted hazelnut, and creamy texture with a long, mineral finish. Consistently New Zealand's most age-worthy Chardonnay.")
if new8:
    PAIR(prod2b2, "Roasted crayfish with herb butter and grilled corn", "complement", "classic", "main", "Elston's creamy richness and toasted hazelnut complement NZ crayfish's sweet intensity; herb butter adds aromatic freshness while grilled corn's sweetness echoes the wine's ripe fruit.")
    PAIR(prod2b2, "Seared scallops with cauliflower purée and crispy pancetta", "complement", "classic", "fish_course", "The wine's creamy texture and ripe fruit are ideal for the scallop-cauliflower combination; pancetta's salt and fat add the savoury dimension that amplifies the wine's complexity.")
    PAIR(prod2b2, "Grilled chicken with tarragon cream sauce and roasted vegetables", "complement", "classic", "main", "Elston Chardonnay's body and richness are natural companions for chicken in cream sauce; tarragon's anise note mirrors the wine's aromatic depth while roasted vegetables add the sweetness that grounds the pairing.")
    PAIR(prod2b2, "Aged Gruyère with apple and toasted walnuts on sourdough", "complement", "established", "cheese", "The wine's hazelnut and apple character creates a direct flavour bridge with the cheese board; Gruyère's crystalline nuttiness extends the wine's finish while sourdough provides the acidic base.")

# ── 3. Eden Valley (Australia) ───────────────────────────────────────────────
print("=== Eden Valley (Australia) ===")
r3 = R("Eden Valley", "Australia", "wine",
        designation_type="GI", designation_name="Eden Valley",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="Eden Valley, adjacent to the Barossa Valley on the Barossa Ranges, is one of Australia's premier cool-climate wine regions. At elevations of 400–550 metres, it produces Riesling of world-class quality alongside elegant Shiraz and increasingly admired Chardonnay. Eden Valley's granitic soils and cool nights create wines of precision, minerality, and extraordinary longevity — Australian Riesling at its finest.",
        key_producers="Henschke, Pewsey Vale, Mountadam, Yalumba Eden Valley",
        historical_context="Eden Valley was established as a distinct wine region in the late 19th century when German settlers planted Riesling vines at altitude above the warmer Barossa floor. The region's Cool Hill Eden Valley Rieslings, notably from Henschke's Pewsey Vale and the eponymous estate, are considered Australia's finest examples of the variety — wines that age for 20 or more years in great vintages.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "very_good", "stable"), (2023, "excellent", "rising")]:
    VIN(r3, yr, qd, pt)

p3a = P("Henschke Cellars", "winery", r3, "Australia",
         production_philosophy="terroir_expression",
         philosophy_description="Henschke is one of Australia's most storied wine families, with roots in the Barossa and Eden Valley since 1868. Their Hill of Grace, from ancient 150-year-old Shiraz vines in Eden Valley, is one of Australia's greatest wines, while their Rieslings from Pewsey Vale are the region's defining examples.",
         reputation_narrative="Henschke's Hill of Grace is Australia's most collected wine alongside Penfolds Grange, while their Julius Eden Valley Riesling is widely regarded as the country's benchmark for the variety. The fifth-generation Henschke family's combination of ancient vine heritage and meticulous winemaking has created an unparalleled body of Australian wine.",
         price_positioning="ultra_premium")

prod3a1, new9 = PROD("Henschke Julius Eden Valley Riesling", "wine_still", p3a, r3, "Australia",
                      subcategory="Riesling", price_tier="premium",
                      description="Australia's benchmark Eden Valley Riesling, from Henschke's cool-climate vineyards. Julius delivers the variety's full expressive potential: lime cordial, slate, and delicate florals on release, developing profound kerosene and toast complexity with 10+ years of cellaring. One of the southern hemisphere's most age-worthy whites.")
if new9:
    PAIR(prod3a1, "Barossa smoked trout with lime crème fraîche and herb oil", "complement", "classic", "starter", "Eden Valley Riesling's lime acidity and slate mineral character are the ideal partner for smoked trout; lime crème fraîche echoes the wine's own citrus while herb oil adds aromatic freshness.")
    PAIR(prod3a1, "Tiger prawns with Thai green curry paste and jasmine rice", "complement", "established", "main", "Julius's taut acidity and lime character navigate Thai curry heat beautifully; the wine's residual tension and aromatic lift act as a natural coolant for the curry's spice.")
    PAIR(prod3a1, "Chicken with lemon and herbs (roast with pan juices)", "complement", "classic", "main", "Australian Riesling and roasted chicken is a national classic; the wine's lime acidity cuts through the pan juices' richness while herbs echo its own aromatic character.")
    PAIR(prod3a1, "Aged Australian cheddar with lime pickle and sesame crackers", "complement", "established", "cheese", "The wine's lime and slate character find resonance with aged cheddar's sharpness; lime pickle echoes the wine's citrus while sesame crackers add a savoury-bitter depth.")

prod3a2, new10 = PROD("Henschke Mount Edelstone Eden Valley Shiraz", "wine_still", p3a, r3, "Australia",
                       subcategory="Shiraz", price_tier="ultra_premium",
                       description="From a single vineyard of old vines in Eden Valley, Mount Edelstone is one of Australia's greatest single-vineyard Shiraz wines — more elegant and cooler-climate in character than the valley floor benchmarks. Deep dark fruit, pepper, and earth with the refinement that only high-altitude, old-vine fruit can provide.")
if new10:
    PAIR(prod3a2, "Slow-roasted Barossa lamb with garlic and rosemary", "complement", "classic", "main", "Eden Valley old-vine Shiraz and South Australian lamb is a regional benchmark; rosemary and garlic echo the wine's herbal depth while slow roasting creates the richness the wine's structure demands.")
    PAIR(prod3a2, "Kangaroo loin with bush tomato sauce and native greens", "complement", "classic", "main", "Australian game and Eden Valley Shiraz is a profound regional pairing; bush tomato's acidic intensity provides the contrast that keeps the wine's dark fruit from overwhelming the delicate meat.")
    PAIR(prod3a2, "Braised beef cheeks with red wine and celeriac mash", "complement", "classic", "main", "Mount Edelstone's power and elegance are perfectly matched to long-braised beef cheeks; the wine's dark fruit and pepper character intensify through the red wine reduction while celeriac mash softens the tannin.")
    PAIR(prod3a2, "Aged Australian sheep's milk cheese with quince and walnut", "complement", "established", "cheese", "The wine's concentrated dark fruit and old-vine character demand aged hard cheese; quince bridges its fruit while walnut echoes its earthy complexity.")

p3b = P("Pewsey Vale Estate", "winery", r3, "Australia",
         production_philosophy="terroir_expression",
         philosophy_description="Pewsey Vale Estate, one of the Eden Valley's oldest vineyards, was established in 1847 and revived by Yalumba in 1961. Their The Contours Museum Reserve Riesling is consistently one of Australia's most celebrated white wines, combining Eden Valley's lime and slate character with extraordinary ageing potential.",
         reputation_narrative="Pewsey Vale is the iconic Eden Valley Riesling estate, with The Contours — released only in exceptional vintages — being one of Australia's most awarded white wines. The estate's position in the Adelaide Hills' coolest zone produces wines of remarkable tension and longevity.",
         price_positioning="mid_range")

prod3b1, new11 = PROD("Pewsey Vale The Contours Eden Valley Riesling", "wine_still", p3b, r3, "Australia",
                       subcategory="Riesling", price_tier="mid_range",
                       description="Pewsey Vale's reserve Riesling, released after extended bottle age, displaying the full development of Eden Valley Riesling: lime cordial, kerosene, toast, and a mineral depth that evolves over decades. One of Australia's most documented and celebrated white wines.")
if new11:
    PAIR(prod3b1, "Sashimi of ocean trout with lime zest and sesame", "complement", "classic", "fish_course", "The wine's lime acidity and slate mineral character are a Japanese-inspired match for sashimi; sesame adds a nutty depth while lime zest creates a direct flavour bridge between wine and fish.")
    PAIR(prod3b1, "Grilled barramundi with nam jim and Asian herb salad", "complement", "established", "main", "Australian Riesling and barramundi with Thai-inspired dressing is a modern Australian classic; nam jim's lime and chili character echoes the wine's own acidity while the herb salad amplifies its aromatics.")
    PAIR(prod3b1, "Choucroute garnie with pork, sausage, and caraway", "complement", "established", "main", "The Alsatian-adjacent style of Australian Riesling finds its natural food partner in choucroute garnie; the wine's acidity navigates the pork's richness while caraway mirrors its aromatic precision.")
    PAIR(prod3b1, "Triple cream brie with lemon curd and toasted almond", "complement", "established", "cheese", "The wine's lime and toast character find a rich partner in triple cream brie; lemon curd bridges the wine's citrus while almonds add the roasted note that echoes the Contours's aged complexity.")

prod3b2, new12 = PROD("Pewsey Vale Prima Eden Valley Riesling", "wine_still", p3b, r3, "Australia",
                       subcategory="Riesling", price_tier="mid_range",
                       description="Pewsey Vale's fresh, young Riesling for immediate enjoyment, displaying vivid lime blossom, apple, and mineral freshness with natural residual sweetness. An excellent introduction to Eden Valley Riesling's distinctive character.")
if new12:
    PAIR(prod3b2, "Thai fish cakes with sweet chili sauce and cucumber salad", "complement", "classic", "starter", "Young Eden Valley Riesling's lime freshness and residual sweetness are ideal for spiced fish cakes; sweet chili echoes the wine's own fruity sweetness while cucumber salad adds refreshing contrast.")
    PAIR(prod3b2, "Prawn dumplings with ginger-soy dipping sauce", "complement", "established", "starter", "The wine's lime acidity and aromatic freshness are ideal for delicate dumpling wrappers; ginger-soy's umami depth provides the savoury counterpoint that makes the pairing complete.")
    PAIR(prod3b2, "Soft goat cheese with honey and lavender on crispbread", "complement", "classic", "aperitif", "Young Riesling's lime freshness and hint of sweetness are a classic match for goat cheese; lavender honey echoes the wine's aromatic delicacy while crispbread grounds the combination.")
    PAIR(prod3b2, "Laksa with prawns, tofu, and coconut broth", "complement", "established", "main", "The wine's residual sweetness and lime acidity create a cooling effect against laksa's rich coconut and spice; lime character mirrors the soup's own citrus while sweetness tames the chili heat.")

# ── 4. McLaren Vale (Australia) ──────────────────────────────────────────────
print("=== McLaren Vale (Australia) ===")
r4 = R("McLaren Vale", "Australia", "wine",
        designation_type="GI", designation_name="McLaren Vale",
        reputation_tier="prestigious",
        quality_trajectory="established",
        description="McLaren Vale, south of Adelaide on the Fleurieu Peninsula, is one of Australia's most beloved wine regions, producing Shiraz and Grenache of extraordinary richness and concentration from old bush vines. The Mediterranean climate, diverse soils, and proximity to Gulf St Vincent create wines with a distinctive combination of power and freshness that has defined the 'Mclaren Vale style' for over a century.",
        key_producers="d'Arenberg, Wirra Wirra, Kay Brothers, Yangarra Estate, Clarendon Hills",
        historical_context="McLaren Vale's winemaking history dates to 1838, making it one of Australia's oldest wine regions. The region's old Shiraz and Grenache vines, some over 100 years old, have survived because McLaren Vale's diversified small-producer landscape avoided the large-scale replanting that eliminated old vines elsewhere in Australia. The region's 'Scarce Earth' project, which maps individual vineyard blocks, has pioneered site-specific expression in Australian wine.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "excellent", "rising"),
    (2022, "very_good", "stable"), (2023, "good", "stable")]:
    VIN(r4, yr, qd, pt)

p4a = P("d'Arenberg Wines", "winery", r4, "Australia",
         production_philosophy="artisanal",
         philosophy_description="d'Arenberg, founded in 1912 and led today by iconoclast Chester Osborn, is McLaren Vale's most individual producer, with a vast portfolio of named wines (The Dead Arm, The Footbolt) and a philosophy of high-density planting, foot-treading, and open-fermented old-vine wines.",
         reputation_narrative="Chester Osborn's idiosyncratic approach and d'Arenberg's century of production have produced one of Australia's most distinctive wine estates. The Dead Arm Shiraz is widely considered McLaren Vale's most age-worthy wine, consistently earning international acclaim.",
         price_positioning="premium")

prod4a1, new13 = PROD("d'Arenberg The Dead Arm Shiraz McLaren Vale", "wine_still", p4a, r4, "Australia",
                       subcategory="Shiraz", price_tier="premium",
                       description="One of Australia's most celebrated Shiraz wines, The Dead Arm takes its name from a dieback disease (dead arm/esca) that reduces vine yields and concentrates flavour in old vines. The result is profoundly concentrated: dark chocolate, blackberry, leather, and spice with velvety tannin and remarkable longevity.")
if new13:
    PAIR(prod4a1, "Slow-braised beef short rib with dark chocolate and red chili mole", "complement", "classic", "main", "The Dead Arm's dark chocolate character creates a profound resonance with chocolate mole; short rib's collagen richness is framed by the wine's velvety tannin while red chili echoes its warming spice.")
    PAIR(prod4a1, "Charcoal-grilled kangaroo with roasted beet and blackberry jus", "complement", "classic", "main", "Australian Shiraz and kangaroo is a national flagship pairing; the wine's dark fruit and leather depth mirror kangaroo's iron character while blackberry jus creates a direct flavour bridge.")
    PAIR(prod4a1, "Slow-roasted lamb shoulder with black olive and rosemary", "complement", "classic", "main", "Old-vine McLaren Vale Shiraz and slow-roasted lamb is the South Australian benchmark; black olive and rosemary add the Mediterranean depth that echoes the wine's own complexity.")
    PAIR(prod4a1, "Aged Manchego with dark chocolate and quince paste", "complement", "established", "cheese", "The Dead Arm's dark chocolate character creates an unusual but compelling bridge with dark chocolate shavings on the board; quince paste bridges the wine's fruit while Manchego's nuttiness adds the savoury depth.")

prod4a2, new14 = PROD("d'Arenberg The Stump Jump White McLaren Vale", "wine_still", p4a, r4, "Australia",
                       subcategory="Roussanne blend", price_tier="value",
                       description="d'Arenberg's accessible white, a Rhône-variety blend of Roussanne, Marsanne, and Viognier, displaying rich texture, white peach, and apricot with a long, spicy finish. Excellent value for a McLaren Vale white that expresses the region's Mediterranean warmth.")
if new14:
    PAIR(prod4a2, "Grilled prawns with roasted pepper and harissa aioli", "complement", "established", "starter", "The wine's Rhône-variety richness and warmth are ideal for Mediterranean shellfish preparations; harissa's warmth is tempered by the wine's fruit while roasted pepper adds sweet depth.")
    PAIR(prod4a2, "Roast chicken with preserved lemon and olives", "complement", "classic", "main", "Roussanne's rich texture and stone-fruit character are ideal for roast chicken; preserved lemon echoes the wine's freshness while olives add Mediterranean depth that bridges wine and food.")
    PAIR(prod4a2, "Grilled haloumi with roasted tomato and basil", "complement", "classic", "casual", "The wine's warmth and Mediterranean variety character find a natural partner in haloumi and roasted tomato; basil adds aromatic freshness that brightens the pairing.")
    PAIR(prod4a2, "White bean and roasted garlic crostini with aged balsamic", "complement", "established", "aperitif", "Roussanne's textural richness and apricot character find an unexpected harmony with white bean; aged balsamic's sweetness mirrors the wine's depth while roasted garlic adds the savoury anchor.")

p4b = P("Clarendon Hills", "winery", r4, "Australia",
         production_philosophy="minimal_intervention",
         philosophy_description="Roman Bratasiuk's Clarendon Hills produces some of McLaren Vale's most concentrated and sought-after single-vineyard Shiraz wines from ancient, dry-farmed bush vines. His approach — hand-harvesting, whole-bunch fermentation, minimal SO2 — produces wines of extraordinary intensity and individuality.",
         reputation_narrative="Clarendon Hills is McLaren Vale's most talked-about small producer, with Roman Bratasiuk's single-vineyard wines achieving extraordinary critical scores and cult collector status. His Astralis Shiraz is regularly cited alongside Hill of Grace and Grange as one of Australia's greatest red wines.",
         price_positioning="ultra_premium")

prod4b1, new15 = PROD("Clarendon Hills Astralis Syrah McLaren Vale", "wine_still", p4b, r4, "Australia",
                       subcategory="Syrah", price_tier="ultra_premium",
                       description="From the Clarendon subzone's oldest bush vines at 350 metres elevation, Astralis is one of Australia's most profound wines: extraordinary concentration, complexity, and structure that rewards 20+ years of cellaring. Dark plum, earth, iron, and mineral precision define a wine considered among the southern hemisphere's greatest Syrahs.")
if new15:
    PAIR(prod4b1, "Roasted whole saddle of lamb with anchovy and herb butter", "complement", "classic", "main", "Astralis's power and complexity demand whole-saddle luxury; anchovy butter's umami depth adds the savoury intensity that bridges the wine's mineral character while herbs echo its own complexity.")
    PAIR(prod4b1, "Charcoal-grilled kangaroo fillet with wild mushroom and truffle jus", "complement", "classic", "main", "Australia's most profound Syrah demands the country's most prestigious game; truffle jus deepens the earthy resonance while wild mushroom amplifies the iron-mineral connection between wine and meat.")
    PAIR(prod4b1, "Venison Wellington with mushroom duxelles and port reduction", "complement", "established", "main", "Astralis's structure and concentration can support this most ambitious preparation; mushroom duxelles and port reduction together provide the rich, savoury depth the wine's power demands.")
    PAIR(prod4b1, "Aged Comté with black truffle and walnut bread", "complement", "established", "cheese", "One of Australia's greatest wines demands the finest European cheese; black truffle deepens the earthy resonance while aged Comté's crystalline complexity extends the wine's extraordinary finish.")

prod4b2, new16 = PROD("Clarendon Hills Blewitt Springs Grenache McLaren Vale", "wine_still", p4b, r4, "Australia",
                       subcategory="Grenache", price_tier="premium",
                       description="From old-vine Grenache in the Blewitt Springs sub-zone, one of McLaren Vale's finest sand-over-clay sites. The wine displays the variety's hallmark red cherry and spice with an unusual combination of power and delicacy: lifted aromatics, silky tannin, and a long, savoury finish.")
if new16:
    PAIR(prod4b2, "Pork belly with cherry glaze and pickled cucumber", "complement", "established", "main", "Old-vine Grenache's red cherry and spice are a natural partner for pork; cherry glaze creates a direct flavour bridge while pickled cucumber's acidity cuts through the pork's rich fat.")
    PAIR(prod4b2, "Grilled lamb cutlets with salsa verde and roasted potatoes", "complement", "classic", "main", "McLaren Vale Grenache and lamb is the region's everyday classic; salsa verde's herb-vinegar character provides the bright contrast that keeps the pairing lively while roasted potatoes absorb the rich juices.")
    PAIR(prod4b2, "Duck liver parfait with cherry compote and brioche", "complement", "established", "starter", "Old-vine Grenache's cherry and spice find resonance with duck liver's richness; cherry compote creates a direct flavour bridge while brioche's butter provides the luxury texture the wine's delicacy demands.")
    PAIR(prod4b2, "Aged Manchego with strawberry preserve and Marcona almonds", "complement", "established", "cheese", "Grenache's strawberry and red-cherry character find harmony with Manchego's nuttiness; strawberry preserve echoes the wine's fruit while almonds add the savoury depth that grounds the pairing.")

# ── 5. Columbia Valley AVA (Washington State) ────────────────────────────────
print("=== Columbia Valley AVA (Washington State) ===")
r5 = R("Columbia Valley AVA", "USA", "wine",
        designation_type="AVA", designation_name="Columbia Valley",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Columbia Valley is Washington State's largest wine appellation, encompassing nearly all of the state's wine production in the rain shadow of the Cascades. The continental climate — hot days and cool nights — produces wines of exceptional concentration and natural acidity across Cabernet Sauvignon, Merlot, Syrah, and Riesling. Washington is America's second-largest wine state, with Columbia Valley at the core of its identity.",
        key_producers="Chateau Ste. Michelle, L'Ecole No 41, Andrew Will, Woodward Canyon, Quilceda Creek",
        historical_context="Serious viticulture in the Columbia Valley began in the 1960s with Chateau Ste. Michelle's founding, though Native American tribes had long noted the wild grape-growing potential of the region. The valley's volcanic basalt soils, extreme diurnal temperature swings, and abundant sunshine created the conditions for wines that distinguished themselves from California alternatives. The 1990s saw rapid quality escalation, and Washington now produces some of America's most celebrated Cabernet Sauvignon, Merlot, and Syrah.")

for yr, qd, pt in [
    (2019, "excellent", "rising"), (2020, "very_good", "stable"), (2021, "exceptional", "rising"),
    (2022, "excellent", "rising"), (2023, "very_good", "stable")]:
    VIN(r5, yr, qd, pt)

p5a = P("Quilceda Creek Vintners", "winery", r5, "USA",
         production_philosophy="classical",
         philosophy_description="Alex Golitzin established Quilceda Creek in 1978, producing one of Washington's first serious Cabernet Sauvignons. Today, his son Paul continues the tradition, producing Cabernet from Columbia Valley's finest sites that has earned Washington its first consecutive 100-point scores from Robert Parker.",
         reputation_narrative="Quilceda Creek is widely considered Washington State's finest Cabernet Sauvignon producer, with multiple 100-point scores from major critics and a reputation for producing America's most age-worthy Cabernet outside Napa Valley. The estate's Columbia Valley Cabernet is one of America's most collected wines.",
         price_positioning="ultra_premium")

prod5a1, new17 = PROD("Quilceda Creek Cabernet Sauvignon Columbia Valley", "wine_still", p5a, r5, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="ultra_premium",
                       description="Washington's most celebrated Cabernet Sauvignon, sourced from the finest sites across the Columbia Valley. Quilceda Creek Cab delivers a structured, age-worthy style: intense cassis, dark chocolate, and graphite with exceptional tannin management and a finish that evolves over 20+ years of cellaring.")
if new17:
    PAIR(prod5a1, "Prime beef ribeye with bone marrow butter and roasted garlic", "complement", "classic", "main", "Quilceda Creek's power and precision demand the finest cut of beef; bone marrow butter's richness mirrors the wine's concentration while roasted garlic adds the savoury depth that bridges meat and wine.")
    PAIR(prod5a1, "Wagyu beef short rib with red wine reduction and truffle potato", "complement", "classic", "main", "Washington's greatest Cabernet and wagyu short rib is a Pacific Northwest luxury pairing; truffle potato amplifies the earthy depth while red wine reduction creates a wine-based bridge.")
    PAIR(prod5a1, "Grilled lamb chops with mint chimichurri and cherry tomatoes", "complement", "classic", "main", "Quilceda Creek's structure and cassis depth are natural companions for grilled lamb; mint chimichurri provides the bright herbal contrast that keeps the luxury pairing fresh and vibrant.")
    PAIR(prod5a1, "Aged Tillamook Cheddar with Bing cherry preserve and walnuts", "complement", "established", "cheese", "Washington's finest Cab with Oregon's finest cheese creates a Pacific Northwest prestige pairing; Bing cherry preserve echoes the wine's dark-fruit depth while walnuts add earthy complexity.")

prod5a2, new18 = PROD("Quilceda Creek CVR Cabernet Sauvignon Columbia Valley", "wine_still", p5a, r5, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="premium",
                       description="The CVR (Columbia Valley Red) is Quilceda Creek's more accessible bottling, delivering the estate's signature concentration and precision at a slightly younger drinking window. Cassis, dark herb, and vanilla oak with firm, balanced tannin.")
if new18:
    PAIR(prod5a2, "Grilled New York strip with compound herb butter", "complement", "classic", "main", "CVR's structure and dark fruit are the quintessential Washington steakhouse pairing; compound herb butter echoes the wine's herbal character while the steak's sear complements its dark fruit.")
    PAIR(prod5a2, "Slow-braised lamb shoulder with olives and roasted garlic", "complement", "established", "main", "The wine's concentration and cassis depth complement slow-braised lamb; olives add Mediterranean depth while roasted garlic's sweetness softens the wine's firm tannin.")
    PAIR(prod5a2, "Smoked Gouda and aged Cheddar board with Bing cherries", "complement", "established", "cheese", "CVR's dark fruit and vanilla oak harmonise with smoked Gouda's complexity; aged Cheddar's sharpness provides contrast while Bing cherries echo the wine's Pacific Northwest character.")
    PAIR(prod5a2, "Duck confit with blackcurrant jus and lentils du Puy", "complement", "established", "main", "The wine's cassis depth and firm structure are ideal companions for duck confit; blackcurrant jus creates a direct flavour bridge while lentils add the earthy depth the wine's concentration demands.")

p5b = P("Chateau Ste. Michelle", "winery", r5, "USA",
         production_philosophy="classical",
         philosophy_description="Chateau Ste. Michelle, founded in 1934, is Washington State's oldest and largest winery, producing wines across the Columbia Valley's diverse sub-appellations. Their collaborations with Ernst Loosen (Eroica Riesling) and Antinori (Col Solare) have produced some of Washington's most celebrated wines.",
         reputation_narrative="Chateau Ste. Michelle is the foundation of Washington's wine industry, both historically and commercially. Their Eroica Riesling (with Ernst Loosen) is considered America's finest Riesling, while their Single Vineyard Cabernet Sauvignons demonstrate Columbia Valley's world-class potential.",
         price_positioning="mid_range")

prod5b1, new19 = PROD("Chateau Ste. Michelle Eroica Riesling Columbia Valley", "wine_still", p5b, r5, "USA",
                       subcategory="Riesling", price_tier="mid_range",
                       description="A collaboration between Chateau Ste. Michelle and Ernst Loosen of Germany's Mosel, Eroica is America's most celebrated Riesling: Columbia Valley's concentration and sun-drenched fruit meets Loosen's precision and European elegance. The result is a wine of lime blossom, peach, and mineral depth with a refreshing acidity and balanced residual sweetness.")
if new19:
    PAIR(prod5b1, "Pacific halibut with lemon-herb crust and pickled cucumber salad", "complement", "classic", "fish_course", "Eroica's lime and mineral character are an ideal companion for Pacific halibut; pickled cucumber echoes the wine's acidity while lemon-herb crust amplifies its aromatic character.")
    PAIR(prod5b1, "Dungeness crab with clarified butter and dill", "complement", "classic", "fish_course", "Pacific Northwest Riesling and Dungeness crab is a regional classic; Eroica's fruit and sweetness complement the crab's natural sweetness while the wine's acidity cuts through the butter's richness.")
    PAIR(prod5b1, "Vietnamese pho with beef, herbs, and bean sprouts", "complement", "established", "main", "The wine's residual sweetness and aromatic lift navigate pho's complex spice and anise broth with ease; the lime character mirrors the squeeze of lime traditionally added to the bowl.")
    PAIR(prod5b1, "Asian-spiced duck salad with papaya and lime dressing", "complement", "established", "casual", "Eroica's exotic fruit character and residual sweetness find a natural home with Asian-spiced duck; papaya mirrors the wine's tropical fruit while lime dressing echoes its own acidity.")

prod5b2, new20 = PROD("Chateau Ste. Michelle Indian Wells Cabernet Columbia Valley", "wine_still", p5b, r5, "USA",
                       subcategory="Cabernet Sauvignon", price_tier="mid_range",
                       description="From the warm Horse Heaven Hills and Wahluke Slope sub-zones, Indian Wells Cabernet delivers Columbia Valley's characteristic combination of ripe black fruit, cedar, and firm tannin at an accessible price point — one of Washington State's best value Cabernet Sauvignons.")
if new20:
    PAIR(prod5b2, "Grilled burgers with aged Cheddar and caramelised onions", "complement", "classic", "casual", "Columbia Valley Cabernet's ripe fruit and accessible tannin are ideal for an elevated burger; aged Cheddar adds sharpness while caramelised onions' sweetness bridges the wine's cassis depth.")
    PAIR(prod5b2, "Roasted chicken with garlic, herbs, and pan-roasted potatoes", "complement", "classic", "main", "Indian Wells's fruit and moderate tannin complement roast chicken's richness; herbs echo the wine's own aromatic character while garlic adds the savoury depth that grounds the pairing.")
    PAIR(prod5b2, "Beef and mushroom stew with root vegetables", "complement", "established", "main", "The wine's dark fruit and accessible structure are well matched to hearty beef stew; mushrooms add umami depth while root vegetables add sweetness that softens the tannin.")
    PAIR(prod5b2, "Aged Tillamook Cheddar with apple chutney and crackers", "complement", "established", "cheese", "Columbia Valley Cabernet and Pacific Northwest cheese is a regional pairing; apple chutney's sweet-sour character bridges the wine's fruit while crackers ground the combination.")

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
print("B148 complete.")
conn.close()
