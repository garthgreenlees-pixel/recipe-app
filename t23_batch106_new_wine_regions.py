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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
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
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Region 1: Colares ─────────────────────────────────────────────────────────
print("=== Region 1: Colares ===")
r = R("Colares", "Portugal", "wine",
      designation_type="DOC", designation_name="Colares DOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Portugal's most historic and endangered wine appellation on Atlantic sand dunes northwest of Lisbon; Ramisco (red) and Malvasia de Colares (white) from pre-phylloxera ungrafted vines; extraordinarily long-lived.",
      key_producers="Adega Regional de Colares, António Bernardino Paulo da Silva, Casal Santa Maria",
      historical_context="Colares vines survived phylloxera in sandy soil where the louse cannot survive; the last ungrafted Ramisco vineyards date to the 12th century; only 12 hectares remain; critically endangered.")
VIN(r, 2019, "excellent", "rising", "Good Colares vintage; Ramisco of characteristic iron-mineral austerity.")
VIN(r, 2018, "very_good", "stable", "Reliable year; Colares white and red of good aging potential.")
VIN(r, 2017, "excellent", "stable", "Classic profile; Ramisco of fine tannic structure and mineral depth.")
VIN(r, 2016, "exceptional", "rising", "Outstanding Colares year; Ramisco of extraordinary longevity potential.")
VIN(r, 2015, "very_good", "stable", "Good decade vintage; wines aging well and showing typical Atlantic character.")
p1 = P("Adega Regional de Colares", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="The historic cooperative of Colares (1931); guardian of the pre-phylloxera Ramisco; wines aged for years in oak before release; historic cellar in Colares village.",
       reputation_narrative="The Adega Regional is the only major producer of serious Colares; without their work, Ramisco would have vanished; their wines are among Portugal's most historically significant.",
       price_positioning="mid_range")
p2 = P("Casal Santa Maria", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Boutique family estate reviving Colares; estate-grown Ramisco from sand dunes; Malvasia de Colares white also produced; working with MW students to document remaining vineyards.",
       reputation_narrative="Casal Santa Maria is the new wave of Colares producers; bringing attention to the endangered appellation through premium, small-production wines.",
       price_positioning="mid_range")
pr1, n1 = PROD("Adega Regional de Colares Ramisco Tinto", "wine_still", p1, r, "Portugal",
               subcategory="Ramisco", price_tier="mid_range",
               description="Pre-phylloxera Ramisco from Atlantic sand dunes; extraordinarily austere in youth — iron, tar, dried herbs, Atlantic salt and massive tannins; needs 10-20 years; one of Portugal's most unique wines.")
if n1:
    PAIR(pr1, "Aged Iberian cured ham with figs", "complement", "established", "aperitif", "Pre-phylloxera tannin structure suits aged Iberian ham; iron and tar echo cured fat depth.")
    PAIR(pr1, "Braised octopus with black beans and coriander", "complement", "classic", "main", "Portuguese Atlantic tradition; iron mineral and herb notes echo octopus and coriander.")
    PAIR(pr1, "Wild boar ragù with pappardelle", "complement", "established", "main", "Ramisco's tannic austerity suits wild boar's earthiness; iron bridges herb-tomato sauce.")
    PAIR(pr1, "Aged Serra da Estrela cheese with quince", "complement", "classic", "cheese", "Portuguese regional pairing; massive tannins soften against aged mountain sheep cheese.")
pr2, n2 = PROD("Casal Santa Maria Colares Ramisco Reserva", "wine_still", p2, r, "Portugal",
               subcategory="Ramisco", price_tier="premium",
               description="Boutique Ramisco Reserva from ancient sand-dune vines; more polished than the cooperative — iron, Atlantic minerality, dried violets and firm but finer tannins; a modern interpretation of this historic variety.")
if n2:
    PAIR(pr2, "Bacalhau com broa (salt cod with cornbread)", "complement", "classic", "main", "Portuguese regional classic; Atlantic mineral Ramisco echoes salt cod; iron bridges cornbread.")
    PAIR(pr2, "Roasted suckling pig (leitão da Bairrada)", "complement", "established", "main", "Portuguese table tradition; structured Ramisco tannins grip suckling pig crackling.")
    PAIR(pr2, "Grilled Atlantic sea bass with coriander rice", "complement", "adventurous", "fish_course", "Atlantic mineral iron pairing with fish — unusual but compelling; coriander bridges herb notes.")
    PAIR(pr2, "Azeitão cheese with pine nuts and honey", "complement", "suggested", "cheese", "Setúbal peninsula pairing; Atlantic mineral Ramisco suits soft sheep's cheese; pine nut echoes.")

# ── Region 2: Setúbal ─────────────────────────────────────────────────────────
print("=== Region 2: Setúbal ===")
r = R("Setúbal", "Portugal", "wine",
      designation_type="DOC", designation_name="Setúbal DOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Setúbal Peninsula south of Lisbon; Moscatel de Setúbal (fortified Muscat) is Portugal's most extraordinary dessert wine — extraordinary aging, evolving over 50+ years; also serious table wines.",
      key_producers="José Maria da Fonseca, Bacalhôa, Quinta de Alcube",
      historical_context="Moscatel de Setúbal was the wine of Portuguese royalty; José Maria da Fonseca (est. 1834) has been producing it continuously; old reserves from 1900s still in the cellar.")
VIN(r, 2019, "exceptional", "rising", "Outstanding Moscatel year; concentration and acidity for century-long aging.")
VIN(r, 2018, "excellent", "rising", "Classic year; Moscatel de Setúbal of fine orange-raisin depth.")
VIN(r, 2017, "very_good", "stable", "Good vintage; consistent Moscatel of characteristic oxidative complexity.")
VIN(r, 2015, "excellent", "stable", "Reliable Moscatel; wines now beginning their long development arc.")
VIN(r, 2010, "exceptional", "rising", "Benchmark decade vintage; 10-year Moscatel showing extraordinary complexity.")
p1 = P("José Maria da Fonseca", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="Portugal's oldest private wine company (1834); Moscatel de Setúbal 20-year, 50-year and solera vintages; table wines under various brands; cellar with Moscatel dating to the 1900s.",
       reputation_narrative="Fonseca is the greatest Moscatel de Setúbal producer; their aged reserves are national treasures; the 50-year Moscatel is one of Portugal's most extraordinary wines.",
       price_positioning="mid_range")
p2 = P("Bacalhôa Vinhos de Portugal", "winery", r, "Portugal",
       production_philosophy="sustainable",
       philosophy_description="American-owned historic Setúbal estate; range from modern table wines to Moscatel de Setúbal; Quinta da Bacalhôa is their prestige wine; Azeitão sub-regional estate wines.",
       reputation_narrative="Bacalhôa produces serious Setúbal wines alongside reliable Moscatel; their Quinta da Bacalhôa Castelão is Portugal's most internationally recognised Setúbal red.",
       price_positioning="mid_range")
pr1, n1 = PROD("José Maria da Fonseca Moscatel de Setúbal 20 Year", "wine_fortified", p1, r, "Portugal",
               subcategory="Muscat", price_tier="premium",
               description="20-year aged Moscatel de Setúbal; extraordinarily complex — dried orange peel, raisin, walnut, saffron, honey and a remarkable rancio character; one of Portugal's greatest dessert wines.")
if n1:
    PAIR(pr1, "Toucinho do Céu (Portuguese almond cake)", "complement", "classic", "dessert", "Portuguese classic pairing; almond and honey in wine echo traditional convent cake sweetness.")
    PAIR(pr1, "Burnt caramel and orange tart", "complement", "established", "dessert", "Dried orange peel in wine mirrors caramelised orange; rancio bridges caramel depth.")
    PAIR(pr1, "Roquefort with dried figs and toasted almonds", "complement", "established", "cheese", "Sweet-oxidative Moscatel stands up to Roquefort; raisin and fig echo wine's dried fruit.")
    PAIR(pr1, "Seared foie gras with orange marmalade", "complement", "established", "starter", "Oxidative-sweet Moscatel bridges foie richness; orange and walnut echo the accompaniments.")
pr2, n2 = PROD("Bacalhôa Quinta da Bacalhôa Castelão", "wine_still", p2, r, "Portugal",
               subcategory="Castelão", price_tier="mid_range",
               description="Prestige Setúbal Castelão from historic quinta; dark plum, dried herbs, leather and a structured tannic finish; one of Portugal's most distinguished indigenous red varieties in full expression.")
if n2:
    PAIR(pr2, "Roast suckling pig with orange and herbs", "complement", "classic", "main", "Portuguese tradition; structured Castelão tannins grip pork crackling; plum bridges.")
    PAIR(pr2, "Grilled Iberian pork cheeks with migas", "complement", "established", "main", "Alentejo-adjacent pairing; dark plum and leather Castelão suits braised pork richness.")
    PAIR(pr2, "Arroz de pato (Portuguese duck rice)", "complement", "classic", "main", "National dish pairing; Castelão's structure and plum suit duck-enriched rice.")
    PAIR(pr2, "Azeitão cheese with black fig jam", "complement", "classic", "cheese", "Setúbal regional pairing; Castelão's structure suits local sheep's milk; fig bridges dark fruit.")

# ── Region 3: Douro Whites ────────────────────────────────────────────────────
print("=== Region 3: Douro Branco ===")
r = R("Douro Branco", "Portugal", "wine",
      designation_type="DOC", designation_name="Douro DOC White",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Douro Valley's increasingly celebrated dry whites from indigenous varieties — Rabigato, Gouveio, Códega, Viosinho and Malvasia Fina; grown at altitude in schist terroir; complex, mineral and age-worthy.",
      key_producers="Dirk Niepoort, Quinta do Crasto, Ramos Pinto, Quinta de Roriz",
      historical_context="Port's homeland also produces table wine; the indigenous white varieties that once went into white Port are now vinified dry; altitude sites (600-900m) create genuinely complex whites.")
VIN(r, 2022, "excellent", "rising", "Outstanding Douro year for whites; altitude freshness and schist mineral at their best.")
VIN(r, 2021, "very_good", "stable", "Good balance; Douro whites of fine acidity and aromatic complexity.")
VIN(r, 2020, "excellent", "stable", "Warm year; concentrated, textured whites with food-friendly acidity.")
VIN(r, 2019, "exceptional", "rising", "Benchmark Douro vintage; Branco wines of extraordinary depth and aging potential.")
VIN(r, 2018, "very_good", "stable", "Good vintage; reliable Douro whites of consistent mineral quality.")
p1 = P("Ramos Pinto", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="Historic Port house also producing prestige dry wines; Adriano Ramos Pinto founded 1880; Duas Quintas Branco from altitude Douro vineyards; indigenous white varieties vinified dry.",
       reputation_narrative="Ramos Pinto's Duas Quintas demonstrates that Douro whites can be as compelling as the Port; benchmark for the DOC's emerging white wine reputation.",
       price_positioning="mid_range")
p2 = P("Quinta de Roriz", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Symington family's historic Douro quinta; Prazo de Roriz Branco from schist at altitude; indigenous varieties vinified with precision; demonstrates Douro white's serious potential.",
       reputation_narrative="Quinta de Roriz's Branco is one of the Douro's most elegant whites; the Symington approach to indigenous varieties proves the region's white wine future.",
       price_positioning="mid_range")
pr1, n1 = PROD("Ramos Pinto Duas Quintas Branco", "wine_still", p1, r, "Portugal",
               subcategory="Rabigato Malvasia Fina", price_tier="mid_range",
               description="Altitude Douro white from indigenous Rabigato and Malvasia Fina; schist mineral, white peach, apricot and hazelnut; textured, complex and food-friendly with good aging potential.")
if n1:
    PAIR(pr1, "Bacalhau à Gomes de Sá (flaked salt cod with potato)", "complement", "classic", "main", "Portuguese national dish; schist mineral and hazelnut mirror salt cod's complexity; texture bridges potato.")
    PAIR(pr1, "Grilled Douro river trout with herbs", "complement", "classic", "fish_course", "Douro regional pairing; mineral white suits freshwater trout; herb notes align.")
    PAIR(pr1, "Caldo verde with chouriço", "complement", "established", "starter", "Portuguese kale soup; schist mineral and peach bridge the soup's richness; chouriço spice suits wine's warmth.")
    PAIR(pr1, "Queijo da Serra da Estrela at room temperature", "complement", "classic", "cheese", "Douro-Beira regional pairing; textured white suits runny mountain sheep cheese.")
pr2, n2 = PROD("Quinta de Roriz Prazo de Roriz Branco", "wine_still", p2, r, "Portugal",
               subcategory="Rabigato Viosinho", price_tier="mid_range",
               description="Schist-altitude Douro white from Rabigato and Viosinho; flint, white stone fruit, fennel and a mineral precision that rivals white Burgundy; structured and age-worthy.")
if n2:
    PAIR(pr2, "Arroz de lingueirão (razor clam rice)", "complement", "established", "main", "Douro mineral white and rice-based seafood; schist flint echoes razor clam's mineral brine.")
    PAIR(pr2, "Sautéed cuttlefish with garlic and coriander", "complement", "established", "main", "Douro mineral and fennel note bridge cuttlefish; coriander echoes wine's herb register.")
    PAIR(pr2, "Grilled line-caught sea bass with capers", "complement", "established", "fish_course", "Schist mineral and flint suit sea bass; caper echoes wine's saline mineral precision.")
    PAIR(pr2, "Ameijoas bulhão pato (clams with garlic and coriander)", "complement", "classic", "starter", "Portuguese classic; mineral white echoes clam brine; fennel bridges coriander and garlic.")

# ── Region 4: Moscato d'Asti ─────────────────────────────────────────────────
print("=== Region 4: Moscato d'Asti ===")
r = R("Moscato d'Asti", "Italy", "wine",
      designation_type="DOCG", designation_name="Moscato d'Asti DOCG",
      reputation_tier="prestigious", quality_trajectory="established",
      description="Piedmont's delicate low-alcohol sweet sparkling Muscat; Moscato Bianco from Canelli and Santo Stefano Belbo; frizzante (slightly sparkling), 5-5.5% alcohol; peach, apricot, orange blossom and natural sweetness.",
      key_producers="Ceretto, Saracco, La Spinetta, Bera",
      historical_context="Moscato d'Asti is produced by arresting fermentation before all sugar is consumed; naturally low alcohol; drunk as dessert wine in Piedmont since at least the 16th century.")
VIN(r, 2023, "excellent", "stable", "Classic Moscato year; peach and apricot of fine aromatic freshness.")
VIN(r, 2022, "very_good", "stable", "Warm year; fuller Moscato with tropical richness; good frizzante.")
VIN(r, 2021, "excellent", "stable", "Cool year; precise, aromatic Moscato of great elegance.")
VIN(r, 2020, "very_good", "stable", "Good balance; reliable, delicate Moscato d'Asti.")
VIN(r, 2019, "excellent", "stable", "Classic profile; textbook apricot-orange blossom Moscato.")
p1 = P("Paolo Saracco", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Paolo Saracco's benchmark Canelli Moscato estate; Moscato d'Asti from old-vine Muscat on chalk-limestone; the most elegant and age-worthy expression of the DOCG.",
       reputation_narrative="Saracco is Moscato d'Asti's reference producer; their wine demonstrates the variety's extraordinary aromatic purity and delicacy.",
       price_positioning="mid_range")
p2 = P("Bera", "winery", r, "Italy",
       production_philosophy="natural",
       philosophy_description="Walter Bera's natural Moscato estate; biodynamic practices; ancestral Moscato Nature (no sulphur); Moscato d'Asti and still Moscato from old Canelli vines.",
       reputation_narrative="Bera is Moscato d'Asti's most celebrated natural producer; Moscato Nature has cult status among natural wine lovers.",
       price_positioning="mid_range")
pr1, n1 = PROD("Paolo Saracco Moscato d'Asti", "wine_sparkling", p1, r, "Italy",
               subcategory="Moscato Bianco", price_tier="mid_range",
               description="The benchmark Moscato d'Asti; old-vine Canelli Muscat; extraordinary — peach, apricot, orange blossom, jasmine and a gentle, silky frizzante; low alcohol, naturally sweet and utterly delicious.")
if n1:
    PAIR(pr1, "Panettone di Natale with mascarpone", "complement", "classic", "dessert", "Piedmont Christmas tradition; Moscato's peach and apricot mirror panettone citrus; frizzante lifts.")
    PAIR(pr1, "Peach tart with crème pâtissière", "complement", "classic", "dessert", "Peach mirror; orange blossom bridges pastry; frizzante prevents sweetness from overwhelming.")
    PAIR(pr1, "Hazelnuts and Baci chocolates (Perugina)", "complement", "classic", "dessert", "Piedmont classic; Moscato and Piedmont hazelnuts; apricot bridges chocolate sweetness.")
    PAIR(pr1, "Savoiardi (ladyfinger) tiramisu", "complement", "classic", "dessert", "Piedmont dessert classic; apricot and jasmine Moscato bridges coffee and mascarpone.")
pr2, n2 = PROD("Bera Moscato Nature d'Asti", "wine_sparkling", p2, r, "Italy",
               subcategory="Moscato Bianco", price_tier="mid_range",
               description="Zero-sulphur natural Moscato d'Asti from biodynamic Canelli vines; wilder and more complex than conventional — white peach, wild flower, ginger and a delicate frizzante; natural energy.")
if n2:
    PAIR(pr2, "Fresh strawberry granita with cream", "complement", "established", "dessert", "Floral natural Moscato suits light fruit granita; wild flower bridges strawberry; ginger adds.")
    PAIR(pr2, "Torta di nocciole (Piedmont hazelnut cake)", "complement", "classic", "dessert", "Biodynamic Moscato and Piedmont hazelnuts; wild flower bridges; natural energy suits dense cake.")
    PAIR(pr2, "Peaches in white wine with vanilla", "complement", "classic", "dessert", "Piedmont summer classic; peach mirror; ginger and wild flower add complexity to the simple dish.")
    PAIR(pr2, "Fresh fig and honey panna cotta", "complement", "suggested", "dessert", "Fig-honey notes echo wine's apricot-wild flower; delicate frizzante bridges panna cotta richness.")

# ── Region 5: Trento DOC ─────────────────────────────────────────────────────
print("=== Region 5: Trento DOC ===")
r = R("Trento DOC", "Italy", "wine",
      designation_type="DOC", designation_name="Trento DOC",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Italy's highest-altitude traditional method sparkling wine; Chardonnay, Pinot Nero, Pinot Bianco and Meunier from Alpine terraces; Ferrari is Italy's most prestigious sparkling wine house.",
      key_producers="Ferrari, Letrari, Abate Nero, Methius",
      historical_context="Ferrari Fratelli was founded in 1902 by Giulio Ferrari who trained in Épernay; Ferrari has supplied Italian state dinners for decades; Trento DOC created in 1993 for the traditional method.")
VIN(r, 2019, "exceptional", "rising", "Trento benchmark vintage; Chardonnay of rare precision and aging potential.")
VIN(r, 2018, "excellent", "rising", "Outstanding mountain year; Ferrari Giulio Reserve of extraordinary complexity.")
VIN(r, 2017, "excellent", "stable", "Good vintage; Trento DOC wines aging well; Pinot Nero Blanc de Noirs excelled.")
VIN(r, 2016, "very_good", "stable", "Reliable vintage; consistent Ferrari and Letrari Trento DOC.")
VIN(r, 2015, "exceptional", "rising", "Landmark vintage; Giulio Ferrari Riserva of incredible depth and length.")
p1 = P("Ferrari Fratelli", "winery", r, "Italy",
       production_philosophy="traditional",
       philosophy_description="Italy's most prestigious sparkling house (1902); Giulio Ferrari Riserva del Fondatore (vintage, 10+ years on lees) is Italy's answer to Krug; Perlé Blanc de Blancs; wide range from NV to prestige.",
       reputation_narrative="Ferrari is Italy's undisputed finest sparkling wine house; Giulio Ferrari Riserva del Fondatore is one of the world's great wines; served at Italian state occasions since 1974.",
       price_positioning="premium")
p2 = P("Letrari", "winery", r, "Italy",
       production_philosophy="terroir_focused",
       philosophy_description="Family estate from historic Trento sparkling pioneers; Riserva 976 (10 years on lees) and Blanc de Blancs of alpine precision; Leonello Letrari's legacy continued by next generation.",
       reputation_narrative="Letrari is Trento DOC's most celebrated family estate; 976 Riserva demonstrates that Ferrari is not the only world-class producer in the denomination.",
       price_positioning="premium")
pr1, n1 = PROD("Ferrari Perlé Blanc de Blancs Trento DOC", "wine_sparkling", p1, r, "Italy",
               subcategory="Chardonnay", price_tier="premium",
               description="Prestige Trento DOC Blanc de Blancs from high-altitude Chardonnay; Alpine mineral, lemon, apple blossom, brioche and a fine, persistent perlage; Italy's most celebrated Blanc de Blancs.")
if n1:
    PAIR(pr1, "Truffled scrambled eggs on Alpine brioche", "complement", "classic", "starter", "Italian luxury aperitif; Alpine mineral and brioche bridge truffle and egg richness.")
    PAIR(pr1, "Grilled lake whitefish (lavarello) with lemon butter", "complement", "classic", "fish_course", "Trentino lake tradition; Alpine mineral mirrors delicate lake fish; lemon bridges butter sauce.")
    PAIR(pr1, "Speck Alto Adige with fig and Trentino honey", "complement", "classic", "aperitif", "Alpine aperitif tradition; fine Trento perlage and Alpine-cured speck; fig bridges acidity.")
    PAIR(pr1, "Seared scallops with Alpine herb butter", "complement", "established", "fish_course", "Ferrari's precision suits scallop sweetness; Alpine herb butter echoes wine's mountain character.")
pr2, n2 = PROD("Letrari 976 Riserva Trento DOC Brut", "wine_sparkling", p2, r, "Italy",
               subcategory="Chardonnay Pinot Nero", price_tier="premium",
               description="10-years-on-lees Trento DOC Riserva; extraordinary Alpine complexity — toasted almond, dried apple, chalk mineral, brioche and a fine, creamy mousse; rivals Ferrari in depth and character.")
if n2:
    PAIR(pr2, "Tagliatelle al tartufo bianco d'Alba", "complement", "established", "main", "Riserva complexity suits white truffle pasta; almond and chalk mineral bridge truffle richness.")
    PAIR(pr2, "Risotto al vino bianco with Parmigiano reggiano", "complement", "classic", "main", "Alpine classic; 10-year complexity suits aged Parmigiano richness; wine used in the risotto base.")
    PAIR(pr2, "Grilled wild mushrooms with garlic, thyme and polenta", "complement", "established", "main", "Mountain Alpine pairing; toasted almond-almond note echoes mushroom earthiness; polenta bridges.")
    PAIR(pr2, "Aged Asiago d'allevo with mountain honey", "complement", "established", "cheese", "Trentino regional pairing; 10-year Riserva complexity suits aged Asiago; honey bridges almond.")

cur.execute("SELECT COUNT(*) FROM beverage_regions")
print(f"Total regions: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_producers")
print(f"Total producers: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_products")
print(f"Total products: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM pairing_intelligence")
print(f"Total pairings: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM beverage_vintages")
print(f"Total vintages: {cur.fetchone()[0]}")
print("Done.")
conn.close()
