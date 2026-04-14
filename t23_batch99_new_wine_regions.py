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

# ── Region 1: Chinon ─────────────────────────────────────────────────────────
print("=== Region 1: Chinon ===")
r = R("Chinon", "France", "wine",
      designation_type="AOC", designation_name="Chinon AOC",
      reputation_tier="prestigious", quality_trajectory="established",
      description="Loire Valley's most celebrated Cabernet Franc appellation; sandy, gravelly and tuffeau limestone soils produce reds of elegant minerality, graphite and violet; whites from Chenin Blanc.",
      key_producers="Charles Joguet, Olga Raffault, Philippe Alliet, Bernard Baudry",
      historical_context="Rabelais (born Chinon, 1494) praised the wines of his homeland; Clos de l'Echo and Clos de la Dioterie are Chinon's most historic vineyard sites.")
VIN(r, 2022, "excellent", "rising", "Classic Loire year; Cabernet Franc of remarkable graphite precision and violet lift.")
VIN(r, 2021, "exceptional", "rising", "Benchmark Chinon vintage; cool and long; wines of extraordinary finesse and aging potential.")
VIN(r, 2020, "excellent", "stable", "Warm year retained freshness; concentrated Cab Franc with good structure.")
VIN(r, 2019, "very_good", "stable", "Warm, generous year; accessible, fruit-forward Chinon.")
VIN(r, 2018, "excellent", "stable", "Classic year; structured reds with tuffeau mineral character.")
p1 = P("Bernard Baudry", "winery", r, "France",
       production_philosophy="terroir_focused",
       philosophy_description="Matthias Baudry's benchmark Chinon estate; single-vineyard Cabernet Franc from gravels, clay and tuffeau; La Croix Boissée from clay is their most structured wine.",
       reputation_narrative="Baudry is Chinon's most acclaimed producer; La Croix Boissée and Les Grezeaux are Loire Cabernet Franc benchmarks.",
       price_positioning="mid_range")
p2 = P("Olga Raffault", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Historic family estate; Les Picasses from tuffeau limestone is their legendary long-aging Chinon; Sylvie Raffault continues the traditional style of her grandmother.",
       reputation_narrative="Raffault's Les Picasses is one of the Loire Valley's greatest reds; tuffeau limestone Chinon that ages for 20+ years.",
       price_positioning="mid_range")
pr1, n1 = PROD("Bernard Baudry La Croix Boissée Chinon Rouge", "wine_still", p1, r, "France",
               subcategory="Cabernet Franc", price_tier="mid_range",
               description="Single-vineyard Cabernet Franc from clay soils; graphite, violet, black cherry and firm tannins; more structured and age-worthy than lighter Chinon; excellent with food.")
if n1:
    PAIR(pr1, "Rillons de Tours (pork belly confit)", "complement", "classic", "main", "Loire regional classic; Cabernet Franc cuts pork belly fat; graphite and cherry echo cured pork.")
    PAIR(pr1, "Grilled lamb cutlets with herbes de Loire", "complement", "established", "main", "Violet and graphite Chinon suits lamb's delicacy; Touraine herbs bridge floral notes.")
    PAIR(pr1, "Mushroom vol-au-vent with tarragon cream", "complement", "suggested", "starter", "Graphite and earthy notes echo mushroom; tarragon bridges herbal register.")
    PAIR(pr1, "Aged Crottin de Chavignol goat's cheese", "complement", "classic", "cheese", "Classic Loire pairing; Chinon's tannins soften goat's cheese tang; cherry bridges.")
pr2, n2 = PROD("Olga Raffault Les Picasses Chinon", "wine_still", p2, r, "France",
               subcategory="Cabernet Franc", price_tier="mid_range",
               description="Historic tuffeau limestone Chinon; pencil shavings, cassis, violet, chalk mineral; built for 15-20 years aging; one of the Loire Valley's great age-worthy reds.")
if n2:
    PAIR(pr2, "Roast pigeon with cherry and foie gras stuffing", "complement", "established", "main", "Tuffeau Chinon's pencil-and-cherry notes suit game bird; foie adds richness.")
    PAIR(pr2, "Mushroom and truffle pot-au-feu", "complement", "established", "main", "Aged Chinon's earthy graphite echoes truffle and mushroom; chalk mineral bridges.")
    PAIR(pr2, "Roquefort with Sauternes-soaked raisins", "contrast", "adventurous", "cheese", "Firm tannins stand up to Roquefort; raisins echo wine's dried-fruit notes in age.")
    PAIR(pr2, "Duck rillettes with cornichons and Dijon", "complement", "classic", "starter", "Loire rillettes tradition; Chinon graphite and cherry bridge duck fat and mustard.")

# ── Region 2: Bourgueil ──────────────────────────────────────────────────────
print("=== Region 2: Bourgueil ===")
r = R("Bourgueil", "France", "wine",
      designation_type="AOC", designation_name="Bourgueil AOC",
      reputation_tier="respected", quality_trajectory="rediscovering",
      description="Loire Valley Cabernet Franc appellation on the north bank of the Loire; sand-and-gravel and tuffeau limestone soils; lighter, more floral style than Chinon; excellent value.",
      key_producers="Domaine de la Chevalerie, Pierre-Jacques Druet, Yannick Amirault",
      historical_context="Bourgueil was the preferred wine of the Loire aristocracy before Chinon's modern rise; the sandy soils near the river produce some of France's most ethereal light reds.")
VIN(r, 2022, "excellent", "stable", "Good Loire year; elegant, floral Cabernet Franc of fine mineral precision.")
VIN(r, 2021, "exceptional", "rising", "Outstanding cool vintage; Bourgueil of extraordinary finesse and aging potential.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer style; accessible and food-friendly.")
VIN(r, 2019, "very_good", "stable", "Good balance; vibrant, cherry-driven Bourgueil.")
VIN(r, 2018, "excellent", "stable", "Classic year; mineral, structured Bourgueil from tuffeau sites.")
p1 = P("Domaine de la Chevalerie", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Pierre Caslot's estate with century-old Cabernet Franc vines; Galichets from tuffeau limestone is their flagship; minimal intervention, long maceration.",
       reputation_narrative="La Chevalerie's Galichets is one of Loire Valley's most age-worthy reds; benchmark for serious tuffeau Bourgueil.",
       price_positioning="mid_range")
p2 = P("Yannick Amirault", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Leading Bourgueil producer with estate vineyards; La Mine and Les Malgagnes are their top single-vineyard bottlings; certified sustainable; whole-cluster pressed for whites.",
       reputation_narrative="Amirault is Bourgueil's most internationally recognized producer; wines of consistent elegance and food-friendly character.",
       price_positioning="mid_range")
pr1, n1 = PROD("Domaine de la Chevalerie Galichets Bourgueil", "wine_still", p1, r, "France",
               subcategory="Cabernet Franc", price_tier="mid_range",
               description="Old-vine tuffeau limestone Bourgueil; red berry, chalk, violet and persistent mineral finish; lighter than Chinon but structured and long-aging; demands a decade.")
if n1:
    PAIR(pr1, "Andouillette grillée with Dijon mustard", "complement", "classic", "main", "Loire bistro classic; mineral Cabernet Franc suits offal's intensity; mustard bridges acidity.")
    PAIR(pr1, "Coq au vin with lardons and chanterelles", "complement", "established", "main", "Loire tradition; Bourgueil's red fruit and earth suit slow-braised chicken.")
    PAIR(pr1, "Rabbit terrine with herbs and pistachios", "complement", "suggested", "starter", "Light tuffeau red suits rabbit's delicacy; herb notes echo violet; pistachio bridges richness.")
    PAIR(pr1, "Camembert de Normandie with apple and walnuts", "complement", "established", "cheese", "Mineral Bourgueil suits creamy Camembert; apple echoes wine's red fruit; walnut bridges.")
pr2, n2 = PROD("Yannick Amirault La Mine Bourgueil", "wine_still", p2, r, "France",
               subcategory="Cabernet Franc", price_tier="mid_range",
               description="Sand and gravel site Bourgueil; more floral and lighter than tuffeau expressions; fresh cherry, raspberry, violet and silky tannins; drink younger than La Chevalerie.")
if n2:
    PAIR(pr2, "Grilled salmon with tarragon butter sauce", "complement", "established", "fish_course", "Light Cabernet Franc suits salmon; red fruit bridges buttery sauce; tarragon echoes herb.")
    PAIR(pr2, "Charcuterie board with rillettes and pâté", "complement", "classic", "aperitif", "Classic Loire aperitif; fresh Bourgueil cherry cuts pork fat; floral notes lift.")
    PAIR(pr2, "Beet and goat's cheese salad with walnuts", "complement", "suggested", "starter", "Earthy beet echoes wine's mineral; goat's cheese is a Loire classic; walnuts bridge.")
    PAIR(pr2, "Duck confit with cherry reduction and lentils", "complement", "established", "main", "Cherry-forward Bourgueil mirrors cherry sauce; light tannins suit confit duck.")

# ── Region 3: Madeira ────────────────────────────────────────────────────────
print("=== Region 3: Madeira ===")
r = R("Madeira", "Portugal", "wine",
      designation_type="DOC", designation_name="Madeira DOC",
      reputation_tier="iconic", quality_trajectory="rediscovering",
      description="Atlantic island volcanic wine producing one of the world's longest-lived fortified wines; Sercial, Verdelho, Bual and Malvasia grapes; unique estufagem or canteiro aging; extraordinary longevity.",
      key_producers="Barbeito, Blandy's, Henriques & Henriques, D'Oliveiras",
      historical_context="Thomas Jefferson drank Madeira at both the signing of the Declaration of Independence and his own inauguration; 19th-century Bual can still be alive at 200 years.")
VIN(r, 2011, "exceptional", "rising", "Declared vintage; exceptional concentration and acidity from Sercial and Bual; 100-year wines in the making.")
VIN(r, 2009, "excellent", "rising", "Strong vintage; Verdelho of remarkable complexity; wines now showing impressive development.")
VIN(r, 2005, "exceptional", "rising", "Outstanding declared vintage; benchmark across all varieties; extraordinary aging trajectory.")
VIN(r, 2000, "excellent", "stable", "Millennium vintage; Bual and Malvasia of fine concentration and balance.")
VIN(r, 1995, "very_good", "stable", "Reliable vintage; 10-year-old wines now showing classic development.")
p1 = P("Barbeito", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="Ricardo Barbeito's artisan house; canteiro aging only (no estufagem); single-cask and old-vintage releases; Sercial, Verdelho and Bual of extraordinary age-worthiness.",
       reputation_narrative="Barbeito is considered Madeira's finest artisan producer; their old canteiro releases are among the world's most complex fortified wines.",
       price_positioning="premium")
p2 = P("Blandy's", "winery", r, "Portugal",
       production_philosophy="traditional",
       philosophy_description="The Blandy family's 200-year-old Madeira house; range from 5-year to 50-year expressions; Frasqueira (vintage) and Colheita releases from top years.",
       reputation_narrative="The most recognisable Madeira brand globally; Blandy's Bual and Verdelho 10-year are the definitive entry to serious Madeira.",
       price_positioning="mid_range")
pr1, n1 = PROD("Barbeito Bual 10 Year Old Madeira", "wine_fortified", p1, r, "Portugal",
               subcategory="Bual", price_tier="premium",
               description="Medium-rich Bual with 10 years canteiro aging; dried apricot, caramel, walnut, smoke and a long sweet-sour finish; extraordinary complexity at this level of maturity.")
if n1:
    PAIR(pr1, "Blue cheese soufflé with walnut salad", "complement", "established", "cheese", "Medium-rich Madeira suits blue cheese; walnut echo; caramel balances cheese pungency.")
    PAIR(pr1, "Pecan and maple tart with crème fraîche", "complement", "classic", "dessert", "Caramel and walnut notes in wine echo pecan and maple; crème fraîche bridges acidity.")
    PAIR(pr1, "Dark chocolate and orange terrine", "complement", "established", "dessert", "Smoke and dried fruit bridge dark chocolate; orange mirrors wine's citrus acidity.")
    PAIR(pr1, "Foie gras with dried apricot chutney", "complement", "established", "starter", "Sweet-sour Bual balances foie richness; dried apricot echoes wine's stone fruit.")
pr2, n2 = PROD("Blandy's Sercial 10 Year Old Madeira", "wine_fortified", p2, r, "Portugal",
               subcategory="Sercial", price_tier="mid_range",
               description="Dry, bone-dry Sercial Madeira; hazelnut, dried lemon peel, sea spray, walnut and electrifying acidity; the most food-versatile of all Madeira styles.")
if n2:
    PAIR(pr2, "Seafood risotto with lobster and saffron", "complement", "classic", "main", "Dry Sercial's acidity and sea-spray minerality echo lobster richness; saffron bridges.")
    PAIR(pr2, "Charcuterie and mature cheddar board", "complement", "established", "aperitif", "Bone-dry Madeira as aperitif; walnut-hazelnut notes suit cured meats and aged cheese.")
    PAIR(pr2, "Turtle soup (historical pairing)", "complement", "classic", "main", "The classic 18th-century pairing; Sercial's acidity cut rich turtle soup historically.")
    PAIR(pr2, "Sautéed wild mushrooms on toast with parsley", "complement", "suggested", "starter", "Hazelnut-walnut notes echo wild mushroom; acidity and toast note bridge parsley.")

# ── Region 4: Minho (Vinho Regional) ─────────────────────────────────────────
print("=== Region 4: Terras do Minho ===")
r = R("Terras do Minho", "Portugal", "wine",
      designation_type="VR", designation_name="Terras do Minho VR",
      reputation_tier="respected", quality_trajectory="ascending",
      description="Northwestern Portugal's broader regional appellation surrounding the Vinho Verde DOC; includes wines from outside the strict Vinho Verde rules; Alvarinho, Loureiro and innovative red varieties.",
      key_producers="Anselmo Mendes, Quinta do Ameal, Quinta de Couselo",
      historical_context="The Minho River marks the border with Spain's Galicia; shared culture of Albariño/Alvarinho; wines from here predate Portugal's formal designation system.")
VIN(r, 2023, "excellent", "stable", "Atlantic coolness delivered precise, aromatic Alvarinho and Loureiro.")
VIN(r, 2022, "very_good", "stable", "Warmer year; richer whites with more body; good Loureiro florals.")
VIN(r, 2021, "excellent", "stable", "Classic Atlantic profile; mineral, fresh whites of fine character.")
VIN(r, 2020, "very_good", "stable", "Good balance; food-friendly Alvarinho and Loureiro blends.")
VIN(r, 2019, "excellent", "rising", "Outstanding year; Alvarinho from top sub-regions showed great depth.")
p1 = P("Quinta do Ameal", "winery", r, "Portugal",
       production_philosophy="terroir_focused",
       philosophy_description="Pedro Araújo's benchmark Lima Valley estate; Loureiro from granite soils; Escolha (selection) aged on lees; demonstrates Loureiro's complexity and aging potential.",
       reputation_narrative="Quinta do Ameal is Portugal's reference for serious single-variety Loureiro; their Escolha rivals top Alvarinho in complexity.",
       price_positioning="mid_range")
p2 = P("Quinta de Couselo", "winery", r, "Portugal",
       production_philosophy="sustainable",
       philosophy_description="Galicia-border estate producing Albarino (Portuguese side); blends of Alvarinho-Loureiro; Turonia Albarino is named after the ancient regional title; sustainable certified.",
       reputation_narrative="One of the Minho's most expressive producers; Turonia shows the Alvarinho-Loureiro blend's versatility and Atlantic freshness.",
       price_positioning="mid_range")
pr1, n1 = PROD("Quinta do Ameal Loureiro Escolha", "wine_still", p1, r, "Portugal",
               subcategory="Loureiro", price_tier="mid_range",
               description="Granite-soil Loureiro aged on lees; jasmine, lime blossom, apricot and a persistent mineral salinity; more textured than Alvarinho with a distinctive floral character.")
if n1:
    PAIR(pr1, "Bacalhau à brás (salt cod with eggs and potatoes)", "complement", "classic", "main", "Classic Portuguese pairing; floral mineral Loureiro suits salt cod's salinity and egg richness.")
    PAIR(pr1, "Arroz de lingueirão (razor clam rice)", "complement", "established", "main", "Atlantic mineral echoes razor clam brine; floral notes bridge rice and herb character.")
    PAIR(pr1, "Baked sea bass with fennel and sea salt", "complement", "established", "fish_course", "Jasmine and lime blossom echo fennel; mineral salinity amplifies sea bass delicacy.")
    PAIR(pr1, "Goat's cheese with lemon thyme honey", "complement", "suggested", "cheese", "Floral mineral Loureiro suits goat's cheese; honey mediates; lime blossom echoes thyme.")
pr2, n2 = PROD("Quinta de Couselo Turonia Albarino", "wine_still", p2, r, "Portugal",
               subcategory="Alvarinho", price_tier="mid_range",
               description="Atlantic-facing Alvarinho (Portuguese Albarino) from Minho granite; lime, peach, grapefruit and saline mineral; bright, crisp and ideal for Galician-style seafood.")
if n2:
    PAIR(pr2, "Steamed vongole with coriander and lime", "complement", "established", "starter", "Saline citrus wine echoes clam brine; coriander bridges floral; lime note amplifies.")
    PAIR(pr2, "Grilled lamprey (lampreia) with rice", "complement", "classic", "main", "Minho regional speciality; Atlantic Alvarinho's mineral salinity suits lamprey's richness.")
    PAIR(pr2, "Ceviche of river trout with herbs and citrus", "complement", "suggested", "starter", "Citrus-mineral wine echoes ceviche marinade; freshness amplifies delicate river fish.")
    PAIR(pr2, "Ameijoas na cataplana with chouriço", "complement", "classic", "main", "Portuguese coastal classic; saline Alvarinho mirrors clam brine; acidity bridges chouriço spice.")

# ── Region 5: Pacherenc du Vic-Bilh ──────────────────────────────────────────
print("=== Region 5: Pacherenc du Vic-Bilh ===")
r = R("Pacherenc du Vic-Bilh", "France", "wine",
      designation_type="AOC", designation_name="Pacherenc du Vic-Bilh AOC",
      reputation_tier="overlooked", quality_trajectory="rediscovering",
      description="Southwest French appellation adjacent to Madiran; produces exceptional dry and sweet whites from Petit Manseng, Gros Manseng and Arrufiac; holiday-season sweet Pacherenc is a Gascon tradition.",
      key_producers="Château Bouscassé, Château Montus, Domaine Berthoumieu",
      historical_context="Pacherenc ('stakes in rows' in Gascon dialect) was named for the ancient training method; Alain Brumont's revival of Madiran also rescued Pacherenc; sweet Vendange de Noël released at Christmas.")
VIN(r, 2022, "excellent", "stable", "Good Gascony year; Petit Manseng dry whites of remarkable freshness and purity.")
VIN(r, 2021, "excellent", "stable", "Cool year; aromatic dry Pacherenc with fine acid structure; sweet wines of fine botrytis.")
VIN(r, 2020, "very_good", "stable", "Warm year; richer dry whites; late-harvest Petit Manseng of great concentration.")
VIN(r, 2019, "exceptional", "rising", "Outstanding year; both dry and sweet Pacherenc of rare depth and complexity.")
VIN(r, 2018, "very_good", "stable", "Good balance; accessible dry whites and reliable sweet Pacherenc.")
p1 = P("Château Bouscassé", "winery", r, "France",
       production_philosophy="traditional",
       philosophy_description="Alain Brumont's traditional estate alongside Château Montus; Pacherenc Sec (dry) from Arrufiac, Petit Courbu and Petit Manseng; Pacherenc Moelleux from late-harvested Petit Manseng.",
       reputation_narrative="Alain Brumont is the titan of modern Gascon wine; his Pacherenc Moelleux rivals Jurançon's great sweet wines.",
       price_positioning="mid_range")
p2 = P("Domaine Berthoumieu", "winery", r, "France",
       production_philosophy="sustainable",
       philosophy_description="Didier Barré's organic Madiran-Pacherenc estate; Haute Tradition dry Pacherenc from Petit Manseng; Charles de Batz sweet from passerillage-dried Petit Manseng.",
       reputation_narrative="Berthoumieu is Pacherenc's most consistent quality producer at accessible prices; Charles de Batz sweet is a Gascon classic.",
       price_positioning="mid_range")
pr1, n1 = PROD("Château Bouscassé Pacherenc du Vic-Bilh Sec", "wine_still", p1, r, "France",
               subcategory="Petit Manseng", price_tier="mid_range",
               description="Dry Pacherenc from Arrufiac, Petit Courbu and Petit Manseng; exotic — mango, passion fruit, grapefruit, white flower and a long fresh finish; unlike any other dry French white.")
if n1:
    PAIR(pr1, "Foie gras poêlé with exotic fruit chutney", "complement", "classic", "starter", "Gascon regional pairing; exotic fruit acidity cuts foie richness; tropical notes echo chutney.")
    PAIR(pr1, "Grilled langoustines with passion fruit beurre blanc", "complement", "established", "fish_course", "Passion fruit in wine echoes beurre blanc; mango bridges crustacean sweetness.")
    PAIR(pr1, "Piperade basquaise with Bayonne ham", "complement", "classic", "main", "Southwest regional pairing; exotic fruit acidity mirrors pepper sweetness; ham bridges.")
    PAIR(pr1, "Thai mango and prawn salad", "complement", "adventurous", "starter", "Mango-passion fruit in wine echoes tropical salad; grapefruit bridges lime in dressing.")
pr2, n2 = PROD("Berthoumieu Charles de Batz Pacherenc Moelleux", "wine_dessert", p2, r, "France",
               subcategory="Petit Manseng", price_tier="mid_range",
               description="Passerillage sweet Pacherenc from dried Petit Manseng; extraordinary — mango, Sauternes-like apricot, honey, candied orange and remarkable balancing acidity; Gascon's answer to Jurançon.")
if n2:
    PAIR(pr2, "Foie gras terrine with fig and walnut", "complement", "classic", "starter", "Gascon great pairing; sweet Pacherenc's acidity balances foie richness; fig echoes wine's fruit.")
    PAIR(pr2, "Roquefort with dried apricots and candied walnuts", "complement", "established", "cheese", "Sweet Pacherenc's acidity bridges Roquefort pungency; apricot echoes wine's stone fruit.")
    PAIR(pr2, "Mango tarte tatin with crème fraîche", "complement", "suggested", "dessert", "Mango mirrors wine; acidity prevents cloying; crème fraîche bridges richness.")
    PAIR(pr2, "Seared duck breast with orange and honey glaze", "bridge", "adventurous", "main", "Sweet Gascony wine bridges orange-honey glaze and duck fat; mango echoes fruit sauce.")

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
