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

# ── Region 1: Wachau ──────────────────────────────────────────────────────────
print("\n=== Region 1: Wachau ===")
r1 = R("Wachau", "Austria", "wine",
    designation_type="DAC",
    designation_name="Wachau DAC",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Austria's most celebrated white wine region, a UNESCO World Heritage site carved by the Danube River through dramatic terraced vineyards of gneiss and granite. Classified by the Vinea Wachau grower collective into Steinfeder, Federspiel, and Smaragd tiers. Riesling and Grüner Veltliner reach pinnacles of Alpine purity and mineral tension.",
    key_producers="F.X. Pichler, Rudi Pichler, Prager, Emmerich Knoll, Hirtzberger",
    historical_context="Medieval viniculture preserved through Habsburg patronage; the 1983 Austrian wine scandal actually elevated Wachau's reputation as producers doubled down on dry, unmanipulated wines.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "very_good", "stable"), (2019, "excellent", "stable"), (2018, "very_good", "stable")]:
    VIN(r1, yr, qd, pt)

prod1a_id = P("F.X. Pichler", "winery", r1, "Austria",
    production_philosophy="biodynamic",
    philosophy_description="FX Pichler defines Wachau's apex — single-vineyard Smaragd Rieslings from Kellerberg and Loibner Berg are benchmarks of Austrian viticulture, combining extreme ripeness with laser precision.",
    reputation_narrative="Consistently rated among Austria's most important estates; allocated wines with global collector following.",
    price_positioning="ultra_premium")

prod1b_id = P("Emmerich Knoll", "winery", r1, "Austria",
    production_philosophy="traditional",
    philosophy_description="Knoll's Riesling Vinothekfüllung and Smaragd Grüner Veltliner Schutt express Wachau's terroir through meticulous low-intervention winemaking across several generations of the family.",
    reputation_narrative="One of Austria's most respected traditional producers; cult following for Vinothekfüllung bottlings.",
    price_positioning="ultra_premium")

prod1a, new1a = PROD("F.X. Pichler Smaragd Riesling Kellerberg", "wine_still", prod1a_id, r1, "Austria",
    subcategory="Riesling",
    description="The pinnacle of Wachau Riesling from the iconic Kellerberg site — volcanic gneiss soil, extreme southern exposure, producing wines of breathtaking mineral precision and decades-long aging potential.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Grilled whole turbot with brown butter and capers", "complement", "classic", "fish_course",
         "Riesling's mineral tension cuts the richness of turbot while amplifying its oceanic salinity.")
    PAIR(prod1a, "Wiener Schnitzel with lingonberry jam", "bridge", "classic", "main",
         "Austrian regional harmony — the wine's acidity lifts the veal while the fruit echo mirrors the jam.")
    PAIR(prod1a, "River crayfish bisque with tarragon cream", "elevate", "established", "starter",
         "Alpine freshwater crustaceans echo the river-carved mineral terroir of the Kellerberg site.")
    PAIR(prod1a, "Aged Gruyère with honeycomb", "complement", "suggested", "cheese",
         "Smaragd's richness and acidity bridge the nutty cheese and floral sweetness with equal poise.")

prod1b, new1b = PROD("Emmerich Knoll Riesling Smaragd Loibenberg", "wine_still", prod1b_id, r1, "Austria",
    subcategory="Riesling",
    description="From the southeast-facing Loibenberg hill in Dürnstein, this Smaragd showcases the stony mineral character of Wachau's finest sites with extraordinary longevity and golden-apple aromatics.",
    price_tier="ultra_premium")
if new1b:
    PAIR(prod1b, "Pike-perch with Riesling sauce and market vegetables", "bridge", "classic", "fish_course",
         "Regional echo — wine in the sauce mirrors the wine in the glass, unifying the plate.")
    PAIR(prod1b, "Langoustine with white asparagus and morel cream", "elevate", "established", "starter",
         "Three luxury ingredients elevated by Riesling's acidic backbone and mineral lift.")
    PAIR(prod1b, "Braised veal cheek with herb spaetzle", "complement", "established", "main",
         "Smaragd weight matches veal's richness; the herbal spaetzle echoes the wine's alpine character.")
    PAIR(prod1b, "Apricot tart with vanilla crème fraîche", "bridge", "classic", "dessert",
         "Wachau's terroir-defining apricots mirror the wine's characteristic stone-fruit aromatics.")

# ── Region 2: Rioja Alavesa ──────────────────────────────────────────────────
print("\n=== Region 2: Rioja Alavesa ===")
r2 = R("Rioja Alavesa", "Spain", "wine",
    designation_type="DOCa",
    designation_name="Rioja DOCa",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="The Basque sub-zone of Rioja DOCa, defined by chalky clay soils (alberizas), higher altitude, and a cooler Atlantic influence from the Sierra Cantabria. Produces Tempranillo of greater freshness and aromatic complexity than the broader Rioja region. Village wines and single-vineyard labels are driving a quality revolution.",
    key_producers="Remírez de Ganuza, Artadi, Marqués de Vargas, Bodegas Ostatu, Baigorri",
    historical_context="Historically distinct from La Rioja, Rioja Alavesa belongs to the Basque Country (Álava province); its producers have led the movement for village and single-vineyard designations since the 2000s.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2019, "exceptional", "stable"), (2018, "excellent", "stable"), (2017, "very_good", "stable")]:
    VIN(r2, yr, qd, pt)

prod2a_id = P("Artadi", "winery", r2, "Spain",
    production_philosophy="terroir_focused",
    philosophy_description="Artadi left the Rioja DOCa in 2015 to bottle under Álava designation, emphasising single-vineyard Tempranillo without American oak. Their Viña El Pisón is one of Spain's most sought-after wines.",
    reputation_narrative="Pioneer of Rioja Alavesa single-vineyard movement; Viña El Pisón commands international collector attention.",
    price_positioning="ultra_premium")

prod2b_id = P("Remírez de Ganuza", "winery", r2, "Spain",
    production_philosophy="traditional",
    philosophy_description="Fernando Remírez de Ganuza crafts structured Gran Reserva and Reserva Tempranillos using old vines from Samaniego, incorporating innovative head and shoulder sorting of grape clusters.",
    reputation_narrative="One of Rioja's most iconic names; Trasnocho and Gran Reserva are benchmark Alavesa expressions.",
    price_positioning="ultra_premium")

prod2a, new2a = PROD("Artadi Viña El Pisón", "wine_still", prod2a_id, r2, "Spain",
    subcategory="Tempranillo",
    description="Single-vineyard Tempranillo from a 1.5-hectare plot in Laguardia planted in 1945. Aged in French oak, this is one of Spain's most complex and collectible red wines — silky, concentrated, and hauntingly mineral.",
    price_tier="ultra_premium")
if new2a:
    PAIR(prod2a, "Roast rack of suckling lamb with herbs de Navarra", "complement", "classic", "main",
         "The quintessential Basque pairing — Tempranillo's cherry fruit and fine tannin frame the lamb's sweetness.")
    PAIR(prod2a, "Wild mushroom risotto with aged Idiazabal", "bridge", "established", "main",
         "Earthy mushroom echoes the wine's tertiary complexity while Idiazabal's smoke mirrors oak integration.")
    PAIR(prod2a, "Ibérico ham croquetas with aioli", "complement", "classic", "starter",
         "Classic Spanish harmony — Tempranillo's acidity cuts the fat while amplifying cured pork umami.")
    PAIR(prod2a, "Dark chocolate fondant with Pedro Ximénez reduction", "contrast", "suggested", "dessert",
         "Ripe Tempranillo fruit plays against bitter chocolate; PX's sweetness bridges both elements.")

prod2b, new2b = PROD("Remírez de Ganuza Gran Reserva", "wine_still", prod2b_id, r2, "Spain",
    subcategory="Tempranillo",
    description="A grand expression of Rioja Alavesa tradition — old-vine Tempranillo from Samaniego aged for the full Gran Reserva minimum in French and American oak, producing wines of immense depth and structure.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Braised oxtail with root vegetable purée", "complement", "classic", "main",
         "Gran Reserva tannin structure and earthy complexity match the deeply savoury braised collagen.")
    PAIR(prod2b, "Roast wood pigeon with lentil purée and black truffle", "elevate", "established", "main",
         "Tempranillo's wild-berry fruit and oak spice harmonise with game and earthy truffle.")
    PAIR(prod2b, "Manchego Curado with membrillo", "complement", "classic", "cheese",
         "The Castilian cheese board archetype — medium-aged Manchego and quince paste with structured Tempranillo.")
    PAIR(prod2b, "Grilled beef rib with chimichurri", "complement", "established", "main",
         "Full-bodied Tempranillo with tobacco and leather notes frames red meat with confidence.")

# ── Region 3: Tasmania ───────────────────────────────────────────────────────
print("\n=== Region 3: Tasmania ===")
r3 = R("Tasmania", "Australia", "wine",
    designation_type="GI",
    designation_name="Tasmania GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Australia's coolest and most southerly wine island produces world-class sparkling wine, Pinot Noir, Chardonnay, and Riesling. The maritime climate, low yields, and UV-intense sunlight create wines of exceptional concentration and natural acidity. Both the Tamar Valley and Coal River Valley are key sub-regions.",
    key_producers="Bay of Fires, Jansz, Josef Chromy, Moorilla, Tolpuddle",
    historical_context="Commercial viticulture began in the 1950s; the sparkling wine industry blossomed in the 1980s when Champagne houses identified Tasmania as Australia's finest base-wine source.")

for yr, qd, pt in [
    (2023, "excellent", "rising"), (2022, "exceptional", "rising"),
    (2021, "very_good", "stable"), (2020, "excellent", "stable"), (2019, "very_good", "stable")]:
    VIN(r3, yr, qd, pt)

prod3a_id = P("Tolpuddle Vineyard", "winery", r3, "Australia",
    production_philosophy="terroir_focused",
    philosophy_description="A single Coal River Valley vineyard producing some of Australia's finest Pinot Noir and Chardonnay. Under Shaw + Smith ownership since 2011, Tolpuddle expresses cool Tasmanian terroir with Burgundian restraint and precision.",
    reputation_narrative="Regularly cited among Australia's top five Pinot Noirs; critical darling with collectors in Asia and the UK.",
    price_positioning="ultra_premium")

prod3b_id = P("Jansz Tasmania", "winery", r3, "Australia",
    production_philosophy="traditional",
    philosophy_description="Tasmania's dedicated sparkling producer crafts méthode traditionnelle wines using Chardonnay, Pinot Noir, and Pinot Meunier. The NV Premium Cuvée and vintage releases are benchmarks for Australian sparkling.",
    reputation_narrative="Founding member of Tasmania's sparkling wine industry; Piper-Heidsieck connection elevates global recognition.",
    price_positioning="premium")

prod3a, new3a = PROD("Tolpuddle Vineyard Pinot Noir", "wine_still", prod3a_id, r3, "Australia",
    subcategory="Pinot Noir",
    description="Single vineyard Pinot Noir from the Coal River Valley — a benchmark of Australian cool-climate expression, combining Tasmanian freshness with Burgundian depth, silky texture, and dark cherry intensity.",
    price_tier="ultra_premium")
if new3a:
    PAIR(prod3a, "Duck breast with cherry jus and celeriac purée", "complement", "classic", "main",
         "Cool-climate Pinot's cherry and spice notes echo duck's richness while acidity keeps it fresh.")
    PAIR(prod3a, "Seared ocean trout with beurre blanc and pea shoots", "bridge", "established", "fish_course",
         "Tasmania's ocean trout meets Tasmanian Pinot — regional harmony with the wine's silky texture.")
    PAIR(prod3a, "Mushroom duxelles tart with truffle crème fraîche", "elevate", "established", "starter",
         "Earthy fungal notes in the wine mirror and amplify the mushroom concentration.")
    PAIR(prod3a, "Époisses washed-rind cheese with quince paste", "contrast", "adventurous", "cheese",
         "Pungent washed rind creates dramatic contrast with Pinot's red-fruit delicacy — a bold pairing.")

prod3b, new3b = PROD("Jansz Tasmania Premium Vintage Cuvée", "wine_sparkling", prod3b_id, r3, "Australia",
    subcategory="Traditional Method Sparkling",
    description="A vintage expression of Tasmanian sparkling wine — Chardonnay-dominant blend aged for three-plus years on lees, producing biscuity, citrus-fresh bubbles with a creamy texture unique to the island's cool maritime terroir.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Tasmanian rock lobster with drawn butter", "complement", "classic", "main",
         "Regional luxury pairing — Tasmanian seafood with Tasmanian bubbles; biscuit and citrus lift the shellfish.")
    PAIR(prod3b, "Freshly shucked Sydney Rock Oysters", "cleanse", "classic", "aperitif",
         "Sparkling's acidity and brininess mirror the oyster's oceanic salinity in perfect equilibrium.")
    PAIR(prod3b, "Smoked salmon blini with crème fraîche and dill", "complement", "classic", "starter",
         "The classic celebratory pairing — lees-aged bubbles bridge smoke, fat, and fresh herbs.")
    PAIR(prod3b, "Lemon tart with Italian meringue", "contrast", "established", "dessert",
         "Vintage Cuvée's citrus tension amplifies the tart's acidity while bubbles cleanse the sweetness.")

# ── Region 4: Douro Valley ───────────────────────────────────────────────────
print("\n=== Region 4: Douro Valley ===")
r4 = R("Douro Valley", "Portugal", "wine",
    designation_type="DOC",
    designation_name="Douro DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Portugal's premier red wine DOC, known for schist-rich terraced vineyards along the Douro River. While the Douro's reputation was built on Port wine, its dry table wines from indigenous varieties (Touriga Nacional, Touriga Franca, Tinto Cão) have emerged as some of Europe's most exciting reds. The Upper Douro (Douro Superior) offers especially concentrated expressions.",
    key_producers="Niepoort, Quinta do Crasto, Ramos Pinto, Prats & Symington, Quinta do Vale Meão",
    historical_context="The Douro was demarcated for Port in 1756 by the Marquis of Pombal, making it one of the world's first protected wine regions. Dry wine production surged after Portugal joined the EU in 1986.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "exceptional", "rising"),
    (2020, "very_good", "stable"), (2019, "exceptional", "stable"), (2017, "excellent", "stable")]:
    VIN(r4, yr, qd, pt)

prod4a_id = P("Niepoort", "winery", r4, "Portugal",
    production_philosophy="biodynamic",
    philosophy_description="Dirk Niepoort is Portugal's most intellectually restless producer — his Batuta, Charme, and Redoma wines have redefined Douro table wine, blending traditional foot-treading with low-intervention cellaring across a dozen estates.",
    reputation_narrative="Douro's most celebrated boutique producer; Batuta is Portugal's defining prestige red wine.",
    price_positioning="ultra_premium")

prod4b_id = P("Quinta do Crasto", "winery", r4, "Portugal",
    production_philosophy="traditional",
    philosophy_description="One of the Douro's great quintas, Crasto produces structured reds from old-vine field blends alongside single-variety Touriga Nacional and Touriga Franca of exceptional depth and longevity.",
    reputation_narrative="Among the Douro's most reliable quality estates; their old vine Reserva is a benchmark for the DOC.",
    price_positioning="premium")

prod4a, new4a = PROD("Niepoort Batuta", "wine_still", prod4a_id, r4, "Portugal",
    subcategory="Touriga Nacional Blend",
    description="Niepoort's flagship Douro red — a blend of old vines from the Cima Corgo, aged in large old oak vats. Batuta represents the apex of restrained, complex Douro reds: mineral, floral, and age-worthy with extraordinary precision.",
    price_tier="ultra_premium")
if new4a:
    PAIR(prod4a, "Roast kid (cabrito) with garlic, rosemary, and potato", "complement", "classic", "main",
         "The Douro's traditional roast — Batuta's mineral complexity and fine tannin frame the delicate kid perfectly.")
    PAIR(prod4a, "Bacalhau à Brás with olive oil and black olives", "bridge", "established", "main",
         "Portugal's iconic salted cod dish harmonises with Touriga Nacional's iron-mineral core.")
    PAIR(prod4a, "Duck rice (arroz de pato) with chouriço", "complement", "established", "main",
         "A classic Douro table — smoky chouriço and duck fat echo the wine's depth and structure.")
    PAIR(prod4a, "Serpa aged sheep's cheese with honey", "elevate", "suggested", "cheese",
         "Portuguese artisan cheese with floral honey mirrors Batuta's rosewater and minerality.")

prod4b, new4b = PROD("Quinta do Crasto Reserva Old Vines", "wine_still", prod4b_id, r4, "Portugal",
    subcategory="Field Blend",
    description="Old-vine Douro field blend from granite and schist terraces planted pre-phylloxera. Rich, concentrated, and structured with dark berry, tobacco, and stone mineral notes — a classic expression of upper Douro viticulture.",
    price_tier="premium")
if new4b:
    PAIR(prod4b, "Braised wild boar with root vegetables and red wine", "complement", "classic", "main",
         "Rustic Douro game preparation suits the wine's structured tannin and earthy complexity.")
    PAIR(prod4b, "Slow-roasted lamb shoulder with piri piri", "complement", "established", "main",
         "Old-vine weight and spice capacity handle the heat while amplifying lamb's richness.")
    PAIR(prod4b, "Alheira sausage with fried egg and potatoes", "bridge", "established", "casual",
         "The Trás-os-Montes smoked sausage — a Portuguese soul food pairing with the Douro's robust table wine.")
    PAIR(prod4b, "Aged Manchego with fig jam", "complement", "established", "cheese",
         "Iberian cheese board — the wine's tannic backbone handles the cheese's fat while fig echoes dark fruit.")

# ── Region 5: Baga / Bairrada ────────────────────────────────────────────────
print("\n=== Region 5: Bairrada ===")
r5 = R("Bairrada", "Portugal", "wine",
    designation_type="DOC",
    designation_name="Bairrada DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Atlantic-influenced DOC in central Portugal built on the indigenous Baga grape — one of Europe's most original and challenging varieties. Baga's high tannin and acidity demand careful viticulture and vinification, rewarding patience with wines of extraordinary longevity and terroir expression. Clay-limestone soils over the coastal hills produce distinctively mineral, food-friendly reds and crisp sparkling wines.",
    key_producers="Luís Pato, Sidónio de Sousa, Quinta das Bágeiras, Filipa Pato",
    historical_context="Portugal's answer to Burgundy — Baga was once blended into commercial reds but Luís Pato's advocacy since the 1980s established it as a serious indigenous variety capable of world-class expression.")

for yr, qd, pt in [
    (2022, "excellent", "rising"), (2021, "very_good", "rising"),
    (2020, "excellent", "stable"), (2019, "very_good", "stable"), (2018, "good", "stable")]:
    VIN(r5, yr, qd, pt)

prod5a_id = P("Luís Pato", "winery", r5, "Portugal",
    production_philosophy="terroir_focused",
    philosophy_description="The patriarch of Bairrada, Luís Pato spent decades fighting for Baga's recognition as a world-class grape. His single-vineyard Vinha Pan and Vinha Formal Baga are monuments of Portuguese viticulture.",
    reputation_narrative="Undisputed ambassador of Bairrada; named one of Portugal's most important wine producers by international critics.",
    price_positioning="premium")

prod5b_id = P("Filipa Pato", "winery", r5, "Portugal",
    production_philosophy="natural",
    philosophy_description="Luís Pato's daughter brings a modern, low-intervention perspective to Bairrada, working with Bical and Baga in minimal-sulphur style with an emphasis on freshness and transparency of terroir.",
    reputation_narrative="One of Portugal's most exciting next-generation producers; praised for redefining Bairrada's contemporary identity.",
    price_positioning="mid_range")

prod5a, new5a = PROD("Luís Pato Vinha Pan Baga", "wine_still", prod5a_id, r5, "Portugal",
    subcategory="Baga",
    description="Single-vineyard Baga from one of Bairrada's oldest and most distinctive plots — a powerfully structured red with deep cherry, iron, and tobacco character; requires a decade of cellaring to fully express its complexity.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Roasted suckling pig (leitão da Bairrada) with orange salt", "complement", "classic", "main",
         "The region's signature dish — Bairrada's greatest wine with its iconic roast pig is an irreplaceable pairing.")
    PAIR(prod5a, "Braised oxtail with polenta and gremolata", "complement", "established", "main",
         "Baga's iron tannin and sour-cherry acidity cut through collagen-rich oxtail with precision.")
    PAIR(prod5a, "Duck confit with lentils and smoked paprika", "complement", "established", "main",
         "Game bird richness and smoky paprika echo the wine's dark fruit and tobacco complexity.")
    PAIR(prod5a, "Aged Cheddar with pickled walnuts", "contrast", "suggested", "cheese",
         "Sharp Cheddar's lactic acidity and the pickle's tang contrast beautifully with Baga's structured tannin.")

prod5b, new5b = PROD("Filipa Pato Nossa Calcário Branco", "wine_still", prod5b_id, r5, "Portugal",
    subcategory="Bical",
    description="A white Bairrada from Bical on limestone soils — textural, saline, and mineral with citrus blossom and green apple character. Filipa's minimalist approach reveals the Atlantic influence in every sip.",
    price_tier="mid_range")
if new5b:
    PAIR(prod5b, "Grilled sardines with charred lemon and sea salt", "complement", "classic", "main",
         "Atlantic sardines with Atlantic white wine — the saline minerality mirrors the fish's oceanic character.")
    PAIR(prod5b, "Steamed clams (ameijoas à Bulhão Pato) with garlic and coriander", "bridge", "classic", "starter",
         "Portugal's most beloved clam preparation with a coastal white — mineral wine reflects brine and herbs.")
    PAIR(prod5b, "Tempura courgette flowers with goat's cheese filling", "complement", "established", "starter",
         "Bical's citrus and chalk amplify the goat's cheese freshness through the crispy batter.")
    PAIR(prod5b, "Grilled sea bass with fennel and olive oil", "complement", "established", "fish_course",
         "Clean white fish with Atlantic white wine — the wine's salinity and acidity enhance the fennel notes.")

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
