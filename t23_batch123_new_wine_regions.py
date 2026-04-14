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
    prod_id = cur.fetchone()[0]
    print(f"      Product inserted: {name} ({prod_id})")
    return prod_id, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── B123 ─────────────────────────────────────────────────────────────────────
# Targets: Pfalz (Germany), Nahe (Germany), Ahr (Germany),
#          Priorat DOQ (Spain), Empordà DO (Spain)

# 1. PFALZ — Germany
print("=== Pfalz ===")
r1 = R("Pfalz", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Pfalz",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="Germany's second largest wine region stretching south from the Rheinhessen along the eastern edge of the Haardt mountains. The warmest of Germany's classic regions, with a Mediterranean-influenced climate producing Germany's fullest-bodied Riesling alongside impressive Spätburgunder (Pinot Noir) and Weissburgunder. The Mittelhaardt, including Forst, Deidesheim and Ruppertsberg, is the finest zone. Grosses Gewächs from VDP estates rival the Mosel and Rhine.",
        key_producers="Dr. Bürklin-Wolf, Bassermann-Jordan, von Winning, Rebholz, Friedrich Becker",
        historical_context="Pfalz (formerly Rheinpfalz) was historically Germany's most productive wine region. The quality revolution began in the 1980s-90s as producers adopted dry styles and GG classification. Friedrich Becker's Spätburgunder proved German Pinot Noir could rival Burgundy.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"excellent","rising")]:
    VIN(r1, yr, qd, pt, f"Pfalz {yr}: warmest German region; full-bodied Riesling and Spätburgunder of exceptional ripeness")

p1a = P("Dr. Bürklin-Wolf", "winery", r1, "Germany",
        production_philosophy="biodynamic",
        philosophy_description="Biodynamic Pfalz estate; benchmark Forster Jesuitengarten and Kirchenstück GG Riesling from prime Mittelhaardt sites.",
        reputation_narrative="Germany's largest VDP estate in Wachenheim; biodynamic conversion under Bettina Bürklin-von Guradze; benchmark GG whites.",
        price_positioning="ultra_premium")
pr1a1, n = PROD("Bürklin-Wolf Forster Jesuitengarten Riesling GG", "wine_still", p1a, r1, "Germany",
                subcategory="Riesling Grosses Gewächs", price_tier="ultra_premium",
                description="Forster Jesuitengarten GG; one of Germany's great Riesling sites — volcanic basalt soils with peach, spice and mineral depth.")
if n:
    PAIR(pr1a1, "Spargel (white asparagus) with hollandaise", "complement", "classic", "main", "Pfalz Riesling is Germany's traditional asparagus wine; basalt mineral meets rich hollandaise")
    PAIR(pr1a1, "Grilled river crayfish with herb butter", "complement", "classic", "main", "Full-bodied Pfalz Riesling frames freshwater crayfish beautifully")
    PAIR(pr1a1, "Baked carp with bread stuffing", "complement", "established", "main", "Riesling's acidity lifts the delicate richness of freshwater carp")
    PAIR(pr1a1, "Leberknödel soup (liver dumpling)", "complement", "established", "starter", "Mineral Pfalz Riesling provides the ideal counterpoint to earthy liver dumplings")

pr1a2, n = PROD("Bürklin-Wolf Riesling Estate", "wine_still", p1a, r1, "Germany",
                subcategory="Riesling", price_tier="mid_range",
                description="Entry biodynamic Pfalz Riesling; crisp green apple, mineral and a touch of residual sweetness — versatile and food-friendly.")
if n:
    PAIR(pr1a2, "Flammkuchen with crème fraîche and lardons", "complement", "classic", "main", "Alsatian-style Flammkuchen is the natural companion for Pfalz Riesling")
    PAIR(pr1a2, "Käsekuchen (cheese cake German style)", "complement", "established", "dessert", "Off-dry Riesling complements the tangy-sweet German cheese cake")
    PAIR(pr1a2, "Grilled sea bass with preserved lemon", "complement", "established", "main", "Riesling's citrus mineral is a reliable white fish companion")
    PAIR(pr1a2, "Vietnamese pho with herbs and chilli", "complement", "established", "main", "Off-dry Riesling is the classic pairing for aromatic Vietnamese soup")

p1b = P("Friedrich Becker", "winery", r1, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="Spätburgunder pioneer; vineyards straddling German-French border produce Germany's finest Pinot Noir.",
        reputation_narrative="Friedrich and son Martin Becker farm both Pfalz and Alsace vineyards; their Spätburgunder proved German Pinot Noir can compete with Burgundy.",
        price_positioning="ultra_premium")
pr1b1, n = PROD("Friedrich Becker Spätburgunder GG", "wine_still", p1b, r1, "Germany",
                subcategory="Spätburgunder", price_tier="ultra_premium",
                description="Pfalz-Alsace border Spätburgunder; silky red cherry, mushroom, earthy spice and fine-grained tannins of Burgundian quality.")
if n:
    PAIR(pr1b1, "Roast venison saddle with juniper and red cabbage", "complement", "classic", "main", "German Pinot Noir and venison; the great red wine pairing of the Pfalz")
    PAIR(pr1b1, "Duck breast with cherry and balsamic", "complement", "established", "main", "Silky cherry-fruited Spätburgunder is a natural match for duck")
    PAIR(pr1b1, "Wild mushroom tart with Gruyère", "complement", "established", "main", "Earthy Spätburgunder finds harmony with wild mushroom and nutty cheese")
    PAIR(pr1b1, "Pinot Noir-braised beef cheeks", "complement", "established", "main", "Rich braised beef cheeks mirror the Spätburgunder used in the braise")

pr1b2, n = PROD("Friedrich Becker Weissburgunder", "wine_still", p1b, r1, "Germany",
                subcategory="Weissburgunder", price_tier="premium",
                description="Pfalz Weissburgunder (Pinot Blanc); rounded, creamy and mineral with pear, white flower and gentle oak.")
if n:
    PAIR(pr1b2, "Quiche Lorraine with lardons", "complement", "established", "main", "Rounded Weissburgunder complements the cream-and-bacon savoury tart")
    PAIR(pr1b2, "Grilled sole with lemon butter", "complement", "established", "main", "Creamy mineral Pinot Blanc lifts delicate sole with textural harmony")
    PAIR(pr1b2, "Cream of cauliflower soup", "complement", "established", "starter", "Rounded pear texture of Weissburgunder mirrors cream vegetable soups")
    PAIR(pr1b2, "Pork medallions with apple-cream sauce", "complement", "classic", "main", "Pfalz Weissburgunder and pork-apple is a classic regional pairing")

# 2. NAHE — Germany
print("=== Nahe ===")
r2 = R("Nahe", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Nahe",
        reputation_tier="prestigious",
        quality_trajectory="ascending",
        description="The Nahe river valley, joining the Rhine at Bingen, produces extraordinarily diverse Riesling from extraordinary volcanic and porphyry soils. The Schlossböckelheimer Kupfergrube and Niederhauser Hermannshöhle are among Germany's greatest single vineyards. Wines range from delicate Saar-like precision to fuller Rheingau-style depth. Dönnhoff is the acknowledged benchmark producer and one of Germany's most acclaimed estates.",
        key_producers="Dönnhoff, Schäfer-Fröhlich, Emrich-Schönleber, Kruger-Rumpf",
        historical_context="The Nahe was historically overshadowed by the Rhine and Mosel but has achieved dramatic recognition since the 1990s. The volcanic porphyry and red slate of the Nahe's middle section are uniquely expressive; Nahe Riesling is considered among Germany's most diverse and complex.")
for yr, qd, pt in [(2018,"exceptional","rising"),(2019,"excellent","rising"),(2020,"exceptional","rising"),(2021,"excellent","rising"),(2022,"exceptional","rising")]:
    VIN(r2, yr, qd, pt, f"Nahe {yr}: volcanic porphyry soils; Riesling of extraordinary mineral diversity and complexity")

p2a = P("Dönnhoff", "winery", r2, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="The definitive Nahe producer; Hermannshöhle and Kupfergrube GG are benchmarks for German Riesling terroir expression.",
        reputation_narrative="Helmut Dönnhoff and son Cornelius farm multiple extraordinary Nahe sites; considered Germany's greatest Riesling family alongside Prüm and Müller.",
        price_positioning="ultra_premium")
pr2a1, n = PROD("Dönnhoff Niederhäuser Hermannshöhle Riesling Spätlese", "wine_still", p2a, r2, "Germany",
                subcategory="Riesling Spätlese", price_tier="ultra_premium",
                description="Hermannshöhle Spätlese from volcanic porphyry; legendary Nahe Riesling with peach blossom, mineral and electric Spätlese tension.")
if n:
    PAIR(pr2a1, "Crab with ginger and shiso", "complement", "established", "starter", "Hermannshöhle's precision and peach note lifts delicate crab-ginger combinations")
    PAIR(pr2a1, "Smoked salmon with caper cream", "complement", "classic", "starter", "German tradition: off-dry Nahe Spätlese and cured salmon")
    PAIR(pr2a1, "Lobster thermidor", "complement", "established", "main", "Rich cream lobster finds its counterpoint in Hermannshöhle's tension and fruit")
    PAIR(pr2a1, "Peach and almond tart", "complement", "suggested", "dessert", "Spätlese's peach-blossom mirrors the tart's almond-peach combination")

pr2a2, n = PROD("Dönnhoff Riesling Estate Nahe", "wine_still", p2a, r2, "Germany",
                subcategory="Riesling", price_tier="premium",
                description="Entry Dönnhoff Riesling; fresh and mineral with peach, apricot and slate — the benchmark Nahe everyday white.")
if n:
    PAIR(pr2a2, "Sushi and sashimi platter", "complement", "established", "main", "Nahe mineral Riesling is an outstanding sushi companion")
    PAIR(pr2a2, "Thai green curry with prawns", "complement", "established", "main", "Off-dry Nahe Riesling bridges aromatic spice and coconut sweetness")
    PAIR(pr2a2, "Grilled whole trout with herbs", "complement", "classic", "main", "Fresh mineral Riesling is Germany's universal trout companion")
    PAIR(pr2a2, "White bean hummus with smoked paprika", "complement", "suggested", "starter", "Mineral acidity and gentle sweetness complement spiced legume dips")

p2b = P("Emrich-Schönleber", "winery", r2, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="Upper Nahe estate; Monzinger Halenberg and Frühlingsplätzchen are defining sites for this quieter section of the valley.",
        reputation_narrative="Frank Schönleber's estate in Monzingen produces Riesling of crystalline precision; internationally recognised as among Germany's elite.",
        price_positioning="premium")
pr2b1, n = PROD("Emrich-Schönleber Monzinger Halenberg Riesling GG", "wine_still", p2b, r2, "Germany",
                subcategory="Riesling Grosses Gewächs", price_tier="premium",
                description="Halenberg GG; ancient red slate soils produce Riesling of extraordinary tension — citrus, mineral and 15-year ageing potential.")
if n:
    PAIR(pr2b1, "Poached sole with saffron beurre blanc", "complement", "established", "main", "Halenberg's tension and citrus mineral lifts sole and saffron beautifully")
    PAIR(pr2b1, "Oysters Rockefeller (baked with cream)", "complement", "established", "starter", "Slate mineral GG balances the cream and herb richness of baked oyster")
    PAIR(pr2b1, "Asparagus and smoked ham salad", "complement", "classic", "starter", "Nahe Riesling and asparagus is an irresistible German spring combination")
    PAIR(pr2b1, "Zander (pike-perch) with mustard sauce", "complement", "established", "main", "GG precision is the perfect match for freshwater fish in mustard cream")

pr2b2, n = PROD("Emrich-Schönleber Nahe Riesling Mineral", "wine_still", p2b, r2, "Germany",
                subcategory="Riesling", price_tier="mid_range",
                description="Mineral-label entry Nahe Riesling; crunchy apple, grapefruit and a distinctly stony mineral finish from upper Nahe slate.")
if n:
    PAIR(pr2b2, "Grilled scallops with lemon oil", "complement", "established", "main", "Mineral acidity and citrus lift scallop sweetness with precision")
    PAIR(pr2b2, "Asian noodle salad with sesame dressing", "complement", "established", "main", "Mineral Riesling complements the sesame-citrus note of an Asian noodle salad")
    PAIR(pr2b2, "Smoked mackerel with horseradish", "complement", "established", "starter", "Riesling's acidity cuts through oily mackerel and balances horseradish heat")
    PAIR(pr2b2, "Grilled chicken shawarma", "complement", "suggested", "main", "Off-dry mineral Riesling is an underrated companion for spiced chicken shawarma")

# 3. AHR — Germany
print("=== Ahr ===")
r3 = R("Ahr", "Germany", "wine",
        designation_type="Anbaugebiet",
        designation_name="Ahr",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Germany's most northerly red wine region, in the steep Ahr valley south of Bonn. Almost exclusively Spätburgunder (Pinot Noir) and Frühburgunder (Pinot Noir Précoce) on steep volcanic slate and greywacke. Tiny production from Germany's smallest important wine region. Quality has soared in recent decades with producers making wines of considerable elegance and minerality. The 2021 flood devastated vineyards and cellars across the valley.",
        key_producers="Jean Stodden, Meyer-Näkel, Deutzerhof, Kreuzberg, Mayschoss cooperative",
        historical_context="The Ahr became famous for its red wines in the 19th century when the region supplied the Prussian court. Almost all wine is Spätburgunder. The 2021 Ahr flood was a regional catastrophe; the wine community's survival is considered one of Germany's great resilience stories.")
for yr, qd, pt in [(2018,"exceptional","rising"),(2019,"excellent","rising"),(2020,"very_good","stable"),(2021,"good","rising"),(2022,"excellent","rising")]:
    VIN(r3, yr, qd, pt, f"Ahr {yr}: steep slate valley; Spätburgunder of considerable elegance from tiny northern German region")

p3a = P("Meyer-Näkel", "winery", r3, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="The Ahr's defining modern estate; single-vineyard Spätburgunder from Dernauer Pfarrwingert and Walporzheimer Kräuterberg.",
        reputation_narrative="Werner Näkel transformed his family estate into Germany's Ahr benchmark; daughters Meike and Dörte continue the legacy of mineral, elegant Pinot Noir.",
        price_positioning="premium")
pr3a1, n = PROD("Meyer-Näkel Dernauer Pfarrwingert Spätburgunder GG", "wine_still", p3a, r3, "Germany",
                subcategory="Spätburgunder", price_tier="premium",
                description="Pfarrwingert GG on steep Devonian slate; elegant red cherry, mineral and silky Burgundian tannins of great refinement.")
if n:
    PAIR(pr3a1, "Roast venison with lingonberry and dumpling", "complement", "classic", "main", "German hunting tradition: Ahr Spätburgunder is the natural partner for venison")
    PAIR(pr3a1, "Duck confit with braised lentils", "complement", "established", "main", "Silky cherry and mineral Spätburgunder complements duck's richness perfectly")
    PAIR(pr3a1, "Lamb chops with herb crust", "complement", "established", "main", "Elegant Ahr Pinot frames herb-crusted lamb with precision")
    PAIR(pr3a1, "Wild salmon with pinot noir reduction", "complement", "established", "main", "Salmon's fattiness is lifted by the red berry freshness of slate-soil Spätburgunder")

pr3a2, n = PROD("Meyer-Näkel Spätburgunder Ahr Classic", "wine_still", p3a, r3, "Germany",
                subcategory="Spätburgunder", price_tier="mid_range",
                description="Entry Ahr Spätburgunder; bright red cherry, light tannins and a refreshing mineral finish — elegant everyday drinking.")
if n:
    PAIR(pr3a2, "Gegrillte Blutwurst (blood sausage) with apple", "complement", "established", "main", "Ahr Spätburgunder and blood sausage is a Rhineland regional tradition")
    PAIR(pr3a2, "Beef brisket with potato gratin", "complement", "established", "main", "Light Spätburgunder tannins complement slow-cooked beef and potato")
    PAIR(pr3a2, "Mushroom and thyme tart", "complement", "established", "main", "Earthy mushroom with red-fruited Spätburgunder is a natural pairing")
    PAIR(pr3a2, "Grilled salmon fillet with dill sauce", "complement", "established", "main", "Light Ahr Pinot and salmon is Germany's most celebrated fish-red combination")

p3b = P("Jean Stodden", "winery", r3, "Germany",
        production_philosophy="terroir_driven",
        philosophy_description="Historic Ahr estate; Recher Herrenberg is the family's signature site; classic Ahr Spätburgunder and Frühburgunder.",
        reputation_narrative="Gerhard Stodden's family estate dates to 1960s production; benchmark Recher Herrenberg Spätburgunder is one of Ahr's most sought-after bottles.",
        price_positioning="premium")
pr3b1, n = PROD("Jean Stodden Recher Herrenberg Spätburgunder", "wine_still", p3b, r3, "Germany",
                subcategory="Spätburgunder", price_tier="premium",
                description="Recher Herrenberg Spätburgunder from slate slopes; refined red cherry, violets and silky Pinot texture with long mineral finish.")
if n:
    PAIR(pr3b1, "Spit-roasted duck with cherry sauce", "complement", "classic", "main", "Ahr Spätburgunder cherry fruit mirrors and lifts the cherry-duck combination")
    PAIR(pr3b1, "Mushroom risotto with truffle oil", "complement", "established", "main", "Silky Ahr Pinot and truffled mushroom risotto is a sophisticated pairing")
    PAIR(pr3b1, "Pâté de campagne with cornichons", "complement", "established", "starter", "Light Ahr Spätburgunder is the classic companion for rustic pork pâté")
    PAIR(pr3b1, "Seared tuna tataki with ponzu", "complement", "established", "main", "Delicate Ahr red lifts tuna's meatiness without dominating the ponzu freshness")

pr3b2, n = PROD("Jean Stodden Frühburgunder Ahr", "wine_still", p3b, r3, "Germany",
                subcategory="Frühburgunder", price_tier="premium",
                description="Ahr Frühburgunder (Pinot Noir Précoce); earlier-ripening variant with darker fruit, deeper colour and more earthiness than Spätburgunder.")
if n:
    PAIR(pr3b2, "Wildschwein-Ragout (wild boar ragù)", "complement", "established", "main", "Darker Frühburgunder holds up to the bold earthiness of wild boar ragù")
    PAIR(pr3b2, "Smoked goose breast with root vegetables", "complement", "established", "main", "Dark fruit Frühburgunder complements the smoky richness of preserved goose")
    PAIR(pr3b2, "Aged Rohmilchkäse (raw milk cheese)", "complement", "established", "cheese", "Earthy Frühburgunder finds harmony with complex aged raw-milk German cheese")
    PAIR(pr3b2, "Braised beef short rib with root purée", "complement", "established", "main", "Deep Frühburgunder is the natural companion for slow-braised beef short rib")

# 4. PRIORAT DOQ — Spain
print("=== Priorat DOQ ===")
r4 = R("Priorat DOQ", "Spain", "wine",
        designation_type="DOQ",
        designation_name="Priorat DOQ",
        reputation_tier="iconic",
        quality_trajectory="established",
        description="Spain's most prestigious red wine appellation, in the Tarragona mountains of Catalonia. Llicorella soils — black and red slate with mica chips — impart extraordinary mineral concentration to Garnacha and Cariñena blends. The steep terraced vineyards, sometimes at gradients exceeding 60°, are entirely hand-tended. Priorat was awarded DOQ (the highest Spanish designation, shared only with Rioja) in 2001. Wines of extraordinary density, mineral depth and longevity.",
        key_producers="Álvaro Palacios, Clos Mogador, Mas Doix, Terroir al Límit, Vall Llach",
        historical_context="Priorat's modern era began when René Barbier and Álvaro Palacios arrived in 1989, creating the legendary 'Clos' wines. The region had been abandoned after phylloxera; old Garnacha vines on llicorella were the raw material for a global sensation. L'Ermita became one of the world's most expensive wines.")
for yr, qd, pt in [(2018,"excellent","rising"),(2019,"exceptional","rising"),(2020,"very_good","stable"),(2021,"exceptional","rising"),(2022,"excellent","rising")]:
    VIN(r4, yr, qd, pt, f"Priorat {yr}: llicorella slate harvest; extraordinary mineral concentration from steep terraced Garnacha")

p4a = P("Álvaro Palacios", "winery", r4, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The founder of modern Priorat; L'Ermita and Finca Dofí are among Spain's most celebrated and expensive wines.",
        reputation_narrative="Álvaro Palacios arrived in Priorat in 1989 from Rioja's Palacios family; his L'Ermita from centenarian vines on llicorella became a global icon.",
        price_positioning="ultra_premium")
pr4a1, n = PROD("Álvaro Palacios L'Ermita", "wine_still", p4a, r4, "Spain",
                subcategory="Garnacha", price_tier="ultra_premium",
                description="Spain's most iconic wine; centenarian Garnacha from L'Ermita vineyard on llicorella — mineral, profound and almost impossibly long.")
if n:
    PAIR(pr4a1, "Roasted leg of lamb with thyme and garlic", "complement", "classic", "main", "Garnacha's mineral depth and fruit elevation frames slow-roasted lamb perfectly")
    PAIR(pr4a1, "Ibérico bellota loin (caña de lomo)", "complement", "classic", "main", "Spain's finest wine with Spain's finest cured pork product; a complete expression")
    PAIR(pr4a1, "Braised oxtail with chocolate and sherry", "complement", "established", "main", "L'Ermita's concentration matches the deep complexity of braised oxtail")
    PAIR(pr4a1, "Aged Manchego (3 year)", "complement", "classic", "cheese", "Slate mineral Garnacha finds harmony with aged sheep's milk Manchego")

pr4a2, n = PROD("Álvaro Palacios Camins del Priorat", "wine_still", p4a, r4, "Spain",
                subcategory="Garnacha-Cariñena blend", price_tier="mid_range",
                description="Entry Palacios Priorat; Garnacha and Cariñena with ripe dark fruit, mineral and spice — his most accessible expression.")
if n:
    PAIR(pr4a2, "Grilled lamb chops with romesco", "complement", "classic", "main", "Priorat Garnacha and Catalan romesco sauce is a classic regional pairing")
    PAIR(pr4a2, "Catalan botifarra sausage with white beans", "complement", "classic", "main", "The traditional Catalan sausage-and-bean dish finds its natural Priorat companion")
    PAIR(pr4a2, "Grilled beef entrecôte with herb oil", "complement", "established", "main", "Dark-fruited Priorat complements charred beef with mineral and spice")
    PAIR(pr4a2, "Pan con tomate and manchego", "complement", "classic", "starter", "Catalan bread-and-tomato with sheep's cheese finds natural wine in young Priorat")

p4b = P("Terroir al Límit", "winery", r4, "Spain",
        production_philosophy="natural",
        philosophy_description="Natural winemaking from South African-German partnership; indigenous yeasts, old barrels and minimal intervention in Priorat.",
        reputation_narrative="Dominik Huber and Eben Sadie's project produces some of Priorat's most refined and mineral wines; a counterpoint to power-driven styles.",
        price_positioning="premium")
pr4b1, n = PROD("Terroir al Límit Les Tosses Garnacha", "wine_still", p4b, r4, "Spain",
                subcategory="Garnacha", price_tier="premium",
                description="Old-vine Garnacha from Les Tosses; elegant rather than massive, with red fruit, mineral and herbal freshness on llicorella slate.")
if n:
    PAIR(pr4b1, "Confit rabbit with rosemary and garlic", "complement", "established", "main", "Elegant Garnacha lifts slow-cooked rabbit with herbal-mineral precision")
    PAIR(pr4b1, "Grilled pork ribs with smoked paprika", "complement", "classic", "main", "Catalan paprika-pork and Garnacha is a classic Iberian combination")
    PAIR(pr4b1, "Cuttlefish ink rice (arròs negre)", "bridge", "established", "main", "Earthy mineral Garnacha bridges the intense umami of Catalan ink rice")
    PAIR(pr4b1, "Chargrilled spring onions (calçots) with romesco", "complement", "classic", "main", "Calçotada tradition: Priorat Garnacha and chargrilled spring onions with romesco")

pr4b2, n = PROD("Terroir al Límit Arbossar Cariñena", "wine_still", p4b, r4, "Spain",
                subcategory="Cariñena", price_tier="premium",
                description="Single-varietal Cariñena from steep llicorella terraces; high acidity, dark fruit, iron mineral and a firm tannic spine.")
if n:
    PAIR(pr4b2, "Wild mushroom fricassee with polenta", "complement", "established", "main", "Earthy Cariñena's mineral and acidity complement wild mushroom depth")
    PAIR(pr4b2, "Lamb shoulder slow-roasted with herbs", "complement", "established", "main", "Cariñena's firm tannins are ideal alongside long-braised lamb shoulder")
    PAIR(pr4b2, "Aged sheep's cheese with quince membrillo", "complement", "established", "cheese", "Firm mineral Cariñena pairs naturally with aged ovine cheese and quince")
    PAIR(pr4b2, "Braised pig cheeks with mashed potato", "complement", "established", "main", "High-acid Cariñena cuts through the rich gelatin of braised pig cheeks")

# 5. EMPORDÀ DO — Spain
print("=== Empordà DO ===")
r5 = R("Empordà DO", "Spain", "wine",
        designation_type="DO",
        designation_name="Empordà DO",
        reputation_tier="respected",
        quality_trajectory="ascending",
        description="Northernmost Catalan appellation on the Costa Brava border with France, in the foothills of the Pyrenees. Garnacha and Cariñena dominate reds; Garnatxa Blanca and Muscat produce interesting whites. Famous for its naturally sweet Garnatxa d'Empordà fortified wine. The tramuntana wind, blowing from the Pyrenees, shapes vine physiology and contributes to freshness. Home of Dalí's surrealism; the region's wines have their own eccentric character.",
        key_producers="Perelada, Espelt, Mas Estela, Martín Faixó, Celler d'en Guilla",
        historical_context="Empordà (formerly Ampurdán-Costa Brava) was granted DO in 1975. The region's fortified Garnatxa wine has medieval origins. The Costa Brava's wine-and-gastronomy scene, centred on El Celler de Can Roca in Girona, has amplified international interest in Empordà wines.")
for yr, qd, pt in [(2018,"very_good","stable"),(2019,"excellent","stable"),(2020,"very_good","stable"),(2021,"excellent","rising"),(2022,"very_good","stable")]:
    VIN(r5, yr, qd, pt, f"Empordà {yr}: tramuntana-wind harvest; Garnacha shows fresh character from Pyrenean foothills")

p5a = P("Espelt Viticultors", "winery", r5, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="Empordà estate farming old-vine Garnacha and Cariñena in the Albera foothills; freshness-focused winemaking.",
        reputation_narrative="Anna Maria Espelt's estate is one of Empordà's quality leaders; Comabruna Cariñena from old-vine parcels is the flagship.",
        price_positioning="mid_range")
pr5a1, n = PROD("Espelt Comabruna Cariñena", "wine_still", p5a, r5, "Spain",
                subcategory="Cariñena", price_tier="mid_range",
                description="Old-vine Empordà Cariñena from Albera foothills; dark berry, spice and mineral with firm acidity and length.")
if n:
    PAIR(pr5a1, "Suquet de peix (Catalan fish stew)", "complement", "established", "main", "Empordà Cariñena's freshness and acidity is an unexpected delight with the regional fish stew")
    PAIR(pr5a1, "Grilled botifarra negra (blood sausage)", "complement", "classic", "main", "Catalan blood sausage and Cariñena is a classic Costa Brava regional pairing")
    PAIR(pr5a1, "Braised chicken with prunes and pine nuts", "complement", "established", "main", "The sweet-savoury Catalan combination finds balance in mineral Cariñena")
    PAIR(pr5a1, "Anchovies from l'Escala with bread and butter", "bridge", "established", "starter", "High-acid Cariñena bridges the salinity of famous Empordà anchovies")

pr5a2, n = PROD("Espelt Sauló Garnacha Blanca", "wine_still", p5a, r5, "Spain",
                subcategory="Garnacha Blanca", price_tier="mid_range",
                description="Empordà Garnatxa Blanca from granite (sauló) soils; orange blossom, peach and a mineral freshness from the tramuntana influence.")
if n:
    PAIR(pr5a2, "Grilled razor clams with garlic and parsley", "complement", "established", "starter", "Floral Garnacha Blanca lifts the clean ocean flavour of grilled razor clams")
    PAIR(pr5a2, "Fideuà (Catalan seafood noodle paella)", "complement", "classic", "main", "The regional noodle-seafood dish finds its natural white wine companion")
    PAIR(pr5a2, "Escalivada (roasted peppers and aubergine)", "complement", "established", "starter", "Floral-mineral white mirrors the sweet smokiness of fire-roasted vegetables")
    PAIR(pr5a2, "Crab croquetas with aioli", "complement", "established", "starter", "Fresh Empordà white cleanses crab croqueta richness between each bite")

p5b = P("Celler de Perelada", "winery", r5, "Spain",
        production_philosophy="terroir_driven",
        philosophy_description="The historic Empordà castle estate; broad range from sparkling to fortified Garnatxa; flagship Grand Claustro red.",
        reputation_narrative="Perelada's Castell de Perelada is one of Catalonia's most important wine estates; its Grand Claustro Reserva and Garnatxa d'Empordà are region-defining.",
        price_positioning="mid_range")
pr5b1, n = PROD("Perelada Gran Claustro Reserva", "wine_still", p5b, r5, "Spain",
                subcategory="Cariñena-Garnacha-Cabernet blend", price_tier="premium",
                description="Flagship Perelada Reserva; Cariñena-led blend with ripe dark fruit, spice, cedar and polished tannins for ageing.")
if n:
    PAIR(pr5b1, "Roast duck with orange and apricot glaze", "complement", "established", "main", "Full-bodied Empordà blend lifts duck's richness with dark fruit and spice")
    PAIR(pr5b1, "Beef tenderloin with Catalan picada sauce", "complement", "established", "main", "Herb-nut picada sauce and structured Perelada find natural harmony")
    PAIR(pr5b1, "Aged Garrotxa goat's cheese", "complement", "established", "cheese", "Gran Claustro's structure and dark fruit complement the complex Catalan goat's cheese")
    PAIR(pr5b1, "Wild boar sausage with white beans", "complement", "established", "main", "Robust Empordà red and the regional hearty legume-and-game combination")

pr5b2, n = PROD("Perelada Garnatxa d'Empordà", "wine_fortified", p5b, r5, "Spain",
                subcategory="Garnatxa d'Empordà", price_tier="mid_range",
                description="Traditional Empordà fortified Garnatxa; amber with dried fig, raisin, walnut and a long oxidative finish.")
if n:
    PAIR(pr5b2, "Crema catalana (Catalan crème brûlée)", "complement", "classic", "dessert", "The Catalan fortified wine with its own regional custard is a perfect pairing")
    PAIR(pr5b2, "Dark chocolate fondant with cherry", "complement", "established", "dessert", "Dried fig and walnut Garnatxa mirrors the richness of dark chocolate fondant")
    PAIR(pr5b2, "Churros with thick chocolate sauce", "complement", "classic", "dessert", "The Spanish tradition of sweet fortified wine and churros is warmly celebrated")
    PAIR(pr5b2, "Stilton or Cabrales blue cheese", "contrast", "established", "cheese", "Concentrated Garnatxa sweetness powerfully contrasts with pungent Spanish blue")

# Final counts
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

cur.close()
conn.close()
print("B123 complete.")
