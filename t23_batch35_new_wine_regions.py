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
    cur.execute("""
        INSERT INTO beverage_regions
          (name, country, beverage_family, designation_type, designation_name,
           reputation_tier, quality_trajectory, description, key_producers, historical_context)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
          reputation_tier, quality_trajectory, description, key_producers, historical_context))
    rid = cur.fetchone()[0]
    print(f"  Region: {name} ({rid})")
    return rid

def VIN(region_id, year, quality_descriptor, price_trajectory, season_narrative=None):
    cur.execute("""INSERT INTO beverage_vintages
      (region_id, vintage_year, quality_descriptor, price_trajectory, season_narrative)
      VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
      (region_id, year, quality_descriptor, price_trajectory, season_narrative))

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id
    """, (name, country, region_id, producer_type, description))
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
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return pid, True

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === COMMANDARIA (Cyprus) ===
print("\n=== Commandaria PDO (Cyprus) ===")
r_commandaria = R(
    name="Commandaria",
    country="Cyprus",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Commandaria PDO",
    reputation_tier="respected",
    quality_trajectory="rediscovering",
    description="The world's oldest named wine still in production, Commandaria is a naturally sweet wine produced in the foothills of the Troodos Mountains from sun-dried Xynisteri (white) and Mavro (red) grapes. The name dates to the Knights Hospitaller who governed the region as the Commanderie during the Crusades (12th–13th centuries), though wine production here predates even that by millennia. The wine is made by harvesting ripe grapes and leaving them to dry in the sun for 10–14 days, concentrating sugars to extraordinary levels before slow fermentation and aging, often in a fractional blending solera system.",
    key_producers="ETKO Olympus, KEO St. John Commandaria, Loel Alasia, Tsiakkas Winery",
    historical_context="Historical records trace Commandaria back to 800 BCE. Richard the Lion-Heart described it as 'the wine of kings and the king of wines' after capturing Cyprus in 1191. It was famously served at a banquet of European monarchs in Paris in 1393. The modern Commandaria PDO was established in 1993 and defines 14 villages in the Troodos foothills as the production zone."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Ideal drying conditions with low humidity. Concentrated, complex Commandaria with balanced sweetness."),
    (2020, "very_good", "stable", "Good vintage for sun-drying — hot, dry autumn winds helped concentrate the grapes."),
    (2019, "excellent", "rising", "Outstanding year — exceptional sugar concentration and natural acidity produced wines of great balance."),
    (2018, "very_good", "stable", "Reliable vintage with good natural sweetness and the characteristic dried fruit complexity."),
    (2017, "very_good", "stable", "Classic Commandaria conditions. Well-balanced wines with good aging potential."),
]:
    VIN(r_commandaria, yr, qd, pt, sn)

p_etko = P(
    name="ETKO Olympus",
    country="Cyprus",
    region_id=r_commandaria,
    producer_type="winery",
    description="One of Cyprus's oldest wine producers, established in 1844 and one of the four major producers of Commandaria. ETKO's Olympus Commandaria is produced from the oldest approved villages in the Commandaria PDO zone, with Xynisteri and Mavro grapes sun-dried on matts before slow fermentation and barrel aging. The solera system used by ETKO means the wine is a blend of many vintages, producing a consistent, complex style with notes of dried fruit, coffee, and balsamic."
)
prod_etko, new = PROD(
    name="ETKO Olympus Commandaria Cyprus",
    category="wine_dessert",
    subcategory="Xynisteri",
    producer_id=p_etko,
    region_id=r_commandaria,
    origin_country="Cyprus",
    description="The world's oldest named wine — Commandaria produced from sun-dried Xynisteri and Mavro grapes in the Troodos foothills. Amber-brown, viscous, and intensely concentrated with dried fig, date, raisin, carob, coffee, toffee, and a balsamic acidity that prevents cloying sweetness. Aged in a fractional solera blending vintages across decades. A wine of ancient character and profound historical significance — one of the wine world's most unique and irreplaceable expressions.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_etko, "Melomakarona (Greek honey and walnut Christmas cookies)", "complement", "classic", "dessert", "Commandaria with honey-spiced cookies is a Cypriot and Greek tradition. The wine's dried fruit and honey character mirrors the cookie's filling, while its balsamic edge provides contrast to the sweetness.")
    PAIR(prod_etko, "Aged Halloumi with dried figs and thyme honey", "complement", "classic", "cheese", "Cyprus's most iconic cheese with its most iconic wine — the wine's concentrated sweetness contrasts with Halloumi's salt while dried figs echo its dried fruit complexity. Thyme honey bridges the two.")
    PAIR(prod_etko, "Duck liver pâté with brioche and Morello cherry preserve", "complement", "established", "starter", "The wine's balsamic acidity and dried fruit sweetness complement rich pâté in the manner of Sauternes with foie gras. Morello cherry echoes its fruit complexity.")
    PAIR(prod_etko, "Dark chocolate fondant with sea salt and olive oil ice cream", "bridge", "suggested", "dessert", "Commandaria's dried fruit and coffee notes bridge to dark chocolate. Sea salt mirrors its balsamic edge while olive oil ice cream connects to Cyprus's Mediterranean terroir.")

p_tsiakkas = P(
    name="Tsiakkas Winery",
    country="Cyprus",
    region_id=r_commandaria,
    producer_type="winery",
    description="A small, family-run Commandaria producer in the village of Pelendri — one of the 14 approved Commandaria villages — producing wines with more artisanal character than the large commercial producers. Costas Tsiakkas is committed to showcasing individual village character and indigenous varieties. His Commandaria from single-village Pelendri shows the terroir expression that larger blended productions cannot achieve."
)
prod_tsiakkas, new = PROD(
    name="Tsiakkas Commandaria Pelendri Cyprus",
    category="wine_dessert",
    subcategory="Mavro",
    producer_id=p_tsiakkas,
    region_id=r_commandaria,
    origin_country="Cyprus",
    description="A village-specific Commandaria from Pelendri in the Troodos Mountains — predominantly Mavro (the ancient Cypriot red variety) with some Xynisteri. Darker and more tannic than Xynisteri-dominant Commandaria, with dried black cherry, prune, dark chocolate, carob, and a more structured finish. Sun-dried and slowly fermented, aged in old barrels. The most characterful small-producer Commandaria available — a connection to ancient Cyprus.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_tsiakkas, "Baklava with pistachios, honey, and rose water", "complement", "classic", "dessert", "The wine's dried fruit sweetness and aromatic complexity bridge to honey-soaked baklava. Rose water echoes its floral note while pistachios add texture.")
    PAIR(prod_tsiakkas, "Slow-cooked lamb with cinnamon, allspice, and apricots (kleftiko)", "complement", "established", "main", "Cypriot slow-roasted lamb with sweet-spiced aromatics — the wine's dried fruit and warm spice notes mirror the dish's cinnamon and apricot while Mavro's tannins support the lamb's richness.")
    PAIR(prod_tsiakkas, "Prune and almond tart with crème fraîche", "complement", "established", "dessert", "The wine's prune and dried cherry character bridges naturally to prune tart. Almonds echo its bitterness while crème fraîche contrasts its sweetness.")
    PAIR(prod_tsiakkas, "Strong espresso with lokumades (honey doughnuts)", "complement", "suggested", "dessert", "The wine's coffee and dark dried fruit notes create a natural affinity with espresso. Honey doughnuts echo its sweetness while the coffee contrast highlights its balsamic complexity.")

# === VALAIS (Switzerland) ===
print("\n=== Valais (Switzerland) ===")
r_valais = R(
    name="Valais",
    country="Switzerland",
    beverage_family="wine",
    designation_type="regional",
    designation_name="AOC Valais",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Switzerland's largest and most prestigious wine region, occupying the dramatic high-altitude valley of the Rhône river as it flows west through the Alps toward Lake Geneva. The Valais is a world of extremes: Europe's highest commercial vineyards (above 1,200m), intense Alpine sunshine, thin sandy-granite soils, and the protective föhn wind that enables grapes to ripen at altitude. Indigenous varieties include the nearly extinct Humagne Blanc and Rouge, Cornalin (Rouge du Pays), and Petite Arvine — all producing wines of extraordinary character found nowhere else. Fendant (Chasselas) and Dôle (Pinot Noir/Gamay) are the workhorse styles, but it is the rare indigenous varieties that define Valais's unique viticultural identity.",
    key_producers="Marie-Thérèse Chappaz, Domaine de Beudon, Jean-René Germanier, Provins Valais",
    historical_context="Wine production in the Valais dates to Roman times, with medieval records showing the importance of wine to the local monastic economy. The region's isolation in the Alpine valley meant varieties that disappeared elsewhere survived here — the Valais is now one of Europe's most important repositories of ancient vine material. The modern prestige era was established by Marie-Thérèse Chappaz, whose biodynamic estate has produced Switzerland's most internationally acclaimed wines."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Exceptional vintage with ideal balance of heat and cool nights. Petite Arvine of extraordinary freshness and complexity."),
    (2020, "very_good", "stable", "Warm, dry year producing full, rich wines. Cornalin and Humagne Rouge of excellent concentration."),
    (2019, "excellent", "rising", "Outstanding across all categories. The indigenous varieties showed remarkable site expression."),
    (2018, "excellent", "stable", "Hot summer produced powerful wines with good natural acidity from the cool altitude."),
    (2017, "very_good", "stable", "Good vintage, though some frost impact in early season. Chasselas and Petite Arvine particularly successful."),
]:
    VIN(r_valais, yr, qd, pt, sn)

p_chappaz = P(
    name="Marie-Thérèse Chappaz",
    country="Switzerland",
    region_id=r_valais,
    producer_type="winery",
    description="Switzerland's greatest winemaker and the person most responsible for bringing Valais wines to international attention. Marie-Thérèse Chappaz's biodynamic estate in Fully produces the benchmark wines of every Valais variety — her Petite Arvine, Cornalin, and Grain Noble dessert wines have been recognised as some of Europe's finest. Chappaz essentially invented the concept of serious Swiss fine wine and demonstrated that Alpine viticulture could produce wines worthy of international cellar collections."
)
prod_chappaz, new = PROD(
    name="Marie-Thérèse Chappaz Petite Arvine Valais",
    category="wine_still",
    subcategory="Petite Arvine",
    producer_id=p_chappaz,
    region_id=r_valais,
    origin_country="Switzerland",
    description="The definitive expression of Petite Arvine — Switzerland's most individual indigenous white variety, found only in the Valais and Valle d'Aosta. Chappaz's biodynamic Petite Arvine from Fully shows the variety's extraordinary character: intensely aromatic with grapefruit, white flowers, mountain herbs, mineral-saline finish, and a unique salty bitterness at the end that is the hallmark of the grape. Among the world's most distinctive and original white wines.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_chappaz, "Freshwater perch from Lake Geneva with lemon butter and capers", "complement", "classic", "main", "The classic Swiss pairing — Lac Léman perch with Petite Arvine from the Valais. The wine's saline-mineral finish mirrors the freshwater fish's delicate character, lemon bridges its citrus notes, and capers echo its salty bitterness.")
    PAIR(prod_chappaz, "Raclette with mountain potatoes, cornichons, and dried meat", "complement", "classic", "main", "The quintessential Swiss Alpine meal with the region's most celebrated white wine. Petite Arvine's saline bite cuts through melted Raclette cheese, its mineral freshness contrasts the richness, and dried meat bridges its complex aromatics.")
    PAIR(prod_chappaz, "Asparagus from Valais with mimosa dressing and prosciutto", "complement", "established", "starter", "White asparagus from the Rhône valley with the valley's greatest white wine — a regional pairing of seasonal and geographic logic. The wine's grapefruit and mineral character complement asparagus's subtle bitterness.")
    PAIR(prod_chappaz, "Mountain goat cheese with Alpine honey and walnuts", "complement", "established", "cheese", "Alpine goat cheese with Alpine wine — the wine's floral complexity and saline mineral finish complement the cheese's tanginess. Honey bridges its fruit while walnuts echo its mineral depth.")

p_germanier = P(
    name="Jean-René Germanier",
    country="Switzerland",
    region_id=r_valais,
    producer_type="winery",
    description="One of the Valais's most innovative and internationally-minded estates, producing benchmark wines from both classic and indigenous varieties. Germanier is particularly known for Cayas — a barrel-fermented Syrah from granite soils in Vétroz that demonstrates the Rhône valley's potential for the variety shared with its Northern Rhône counterpart to the west. Also produces exceptional Amigne — another rare Valais indigenous white variety."
)
prod_germanier, new = PROD(
    name="Jean-René Germanier Cayas Syrah Valais",
    category="wine_still",
    subcategory="Syrah",
    producer_id=p_germanier,
    region_id=r_valais,
    origin_country="Switzerland",
    description="The benchmark Valais Syrah — from granite soils in Vétroz, the wine shows how the Rhône valley's most famous grape variety achieves Alpine expression. Cool nights and intense Alpine sunshine produce a Syrah of remarkable freshness and aromatic complexity: violet, black olive, smoked meat, black pepper, and graphite mineral — more reminiscent of Northern Rhône Syrah than the warmer southern styles. One of Switzerland's most internationally competitive wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_germanier, "Grilled Alpine ibex or chamois with juniper and wild mushrooms", "complement", "established", "main", "Alpine game with Alpine Syrah — the wine's cool-climate freshness and floral quality complement lean mountain game. Juniper echoes its pepper spice while wild mushrooms bridge its earthy depth.")
    PAIR(prod_germanier, "Braised beef short ribs with Alpine herbs and root vegetables", "complement", "established", "main", "Cool-climate Syrah's freshness and structure are well-suited to braised beef. Alpine herbs echo the wine's mineral and herbal complexity while root vegetables provide earthy grounding.")
    PAIR(prod_germanier, "Gruyère fondue with bread, pickled onion, and white wine", "contrast", "adventurous", "main", "The classic Alpine pairing reversed — instead of white wine with fondue, Syrah's pepper and olive notes provide contrast to the melted Gruyère's richness. An unconventional but compelling combination.")
    PAIR(prod_germanier, "Wild salmon with red wine butter, lentils, and thyme", "bridge", "suggested", "main", "Cool-climate Syrah bridges elegantly to salmon when prepared with red wine reduction. Lentils provide earthy grounding while thyme echoes the wine's herbal complexity.")

# === JUMILLA DO (Spain) ===
print("\n=== Jumilla DO (Spain) ===")
r_jumilla = R(
    name="Jumilla",
    country="Spain",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Jumilla DO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="A high-altitude inland DO in the Murcia-Castilla-La Mancha border area of southeastern Spain, home to some of Europe's oldest ungrafted Monastrell (Mourvèdre) vines. The extreme continental climate — scorching summers, harsh winters, minimal rainfall — and chalk-limestone soils produce Monastrell of extraordinary concentration, dark fruit, and robust structure. Phylloxera never successfully attacked the sandy soils here, so many vineyards have pre-phylloxera ungrafted vines stretching back 80–150 years. The best wines show compelling depth and authenticity at remarkable value.",
    key_producers="Casa Castillo, Bodegas Juan Gil, Bodegas Castaño, Clos Mesorah",
    historical_context="Monastrell has been grown in Jumilla since at least the 8th century CE, though much of the wine was produced in bulk for blending with lighter northern European wines through the 20th century. The transformation to quality focused production began in the 1990s when Casa Castillo and others demonstrated the potential of old ungrafted Monastrell vines. The phylloxera immunity of the sandy soils means some vines are among the oldest in Europe."
)
for yr, qd, pt, sn in [
    (2020, "excellent", "rising", "Outstanding year — the combination of heat and cold nights produced Monastrell of remarkable concentration and freshness."),
    (2019, "very_good", "stable", "Reliable vintage with good natural character from old ungrafted vines."),
    (2018, "excellent", "rising", "Hot, dry year particularly suited to Monastrell's thick skin. Dense, powerful wines with excellent structure."),
    (2017, "very_good", "stable", "Good vintage across the DO. Old-vine wines of excellent depth."),
    (2016, "excellent", "stable", "One of Jumilla's best recent vintages — concentrated, complex wines with impressive longevity."),
]:
    VIN(r_jumilla, yr, qd, pt, sn)

p_castillo = P(
    name="Casa Castillo",
    country="Spain",
    region_id=r_jumilla,
    producer_type="winery",
    description="The estate that put Jumilla on the international fine wine map — José María Vicente's pioneering property on the Sierra del Carche at 700–800m altitude, producing benchmark Monastrell from 70–100 year old ungrafted vines. Their Pie Franco (ungrafted, pre-phylloxera) and Las Gravas wines have been recognised internationally as among Spain's most compelling and original wines. Casa Castillo's commitment to old-vine authenticity and sustainable farming has inspired a generation of Jumilla producers."
)
prod_castillo, new = PROD(
    name="Casa Castillo Las Gravas Jumilla",
    category="wine_still",
    subcategory="Monastrell",
    producer_id=p_castillo,
    region_id=r_jumilla,
    origin_country="Spain",
    description="The benchmark Las Gravas — old-vine Monastrell from chalky-limestone gravel soils at 700m altitude, from vines averaging 70 years of age on their own ungrafted roots. Dense, concentrated, and complex with blackberry, dried herbs, dark chocolate, earth, and the distinctive iron-mineral character of limestone Monastrell. Fermented in concrete with extended maceration, aged in French oak. A wine of genuine originality and remarkable value.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_castillo, "Slow-braised lamb shoulder with saffron, almonds, and dried fruits (Moorish-style)", "complement", "classic", "main", "The wine's dark fruit, earthy depth, and warm spice are natural companions to Moorish-influenced lamb preparations that reflect the historical Arab influence in Murcia. Saffron bridges its mineral quality.")
    PAIR(prod_castillo, "Grilled Monastrell-marinated Iberian pork with romesco", "complement", "classic", "main", "Monastrell with Iberian pork — a southeastern Spanish pairing of obvious regional logic. Romesco's charred pepper and almond character bridges the wine's fruit while pork's fat is balanced by its tannins.")
    PAIR(prod_castillo, "Wild boar sausage with white beans and smoked paprika", "complement", "established", "main", "The wine's earthy, robust character is ideal for game sausage with legumes. Smoked paprika echoes its warm spice while white beans provide earthy grounding.")
    PAIR(prod_castillo, "Dark chocolate ganache with espresso and sea salt", "complement", "suggested", "dessert", "Old-vine Monastrell's dark chocolate and coffee notes bridge naturally to dark chocolate ganache. Sea salt mirrors the wine's chalky mineral quality.")

p_juan_gil = P(
    name="Bodegas Juan Gil",
    country="Spain",
    region_id=r_jumilla,
    producer_type="winery",
    description="One of Jumilla's largest and most consistently excellent producers, producing Monastrell wines from 40–80 year old vines across multiple price levels. The Juan Gil 12 Meses (aged 12 months in oak) is one of Spain's most extraordinary quality-value propositions — a wine of genuine complexity from old ungrafted vines at a fraction of the price of comparable Rhône or Italian wines. The family also produces the El Nido prestige cuvée (with a portion of Cabernet Sauvignon)."
)
prod_juan_gil, new = PROD(
    name="Juan Gil Monastrell 12 Meses Jumilla",
    category="wine_still",
    subcategory="Monastrell",
    producer_id=p_juan_gil,
    region_id=r_jumilla,
    origin_country="Spain",
    description="Spain's most celebrated quality-value Monastrell — from 40-year-old ungrafted vines on chalky limestone soils, aged 12 months in French and American oak. Intensely coloured with blackberry, plum, dark chocolate, espresso, dried herbs, and a warm, structured finish. Rivals wines at three times its price for sheer hedonistic appeal and complexity. The definitive introduction to Jumilla's remarkable old-vine Monastrell character.",
    price_tier="value"
)
if new:
    PAIR(prod_juan_gil, "Grilled chistorra (thin chorizo) with crusty bread and alioli", "complement", "classic", "starter", "The wine's dark fruit and robust character are ideal for Spanish charcuterie. Chorizo's paprika spice echoes the wine's warmth while alioli adds richness.")
    PAIR(prod_juan_gil, "Cocido murciano (Murcian chickpea stew with vegetables and meat)", "complement", "classic", "main", "The regional stew of Murcia with the region's signature grape — Monastrell's earthy robustness and dark fruit complement the hearty chickpea stew's depth.")
    PAIR(prod_juan_gil, "Aged Manchego with quince paste and Marcona almonds", "complement", "established", "cheese", "The wine's dark fruit and oak spice complement aged sheep's milk cheese. Quince echoes Monastrell's fruit while almonds bridge its earthy mineral depth.")
    PAIR(prod_juan_gil, "Beef burger with caramelised onions, aged cheddar, and bacon", "complement", "established", "main", "Old-vine Monastrell's dark fruit, chocolate, and robust structure are excellent companions for a substantial burger. The wine's tannins cut through fat while its fruit matches the caramelised onions.")

# === BRDA (Slovenia) ===
print("\n=== Brda (Slovenia) ===")
r_brda = R(
    name="Brda",
    country="Slovenia",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Goriška Brda",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Slovenia's most prestigious wine region — the Slovenian side of the border hills shared with Italy's Collio DOC, where the same opoka (clay-marl flysch) soils produce wines of remarkable textural complexity and aromatic richness. Brda's continental-Mediterranean microclimate, warm days, cool nights, and poor flysch soils are ideal for Rebula (Ribolla Gialla), Pinot Gris, and Chardonnay whites, as well as Merlot-based reds. The region is also a hub for the natural and orange wine movement — producers like Movia and Klinec are internationally renowned for their extended-maceration wines.",
    key_producers="Movia, Klinec, Edi Simčič, Marjan Simčič",
    historical_context="The Brda hills have been cultivated since at least the Roman era, but the region was divided by the post-WWII border between Yugoslavia and Italy that split the Collio-Brda wine zone in two. Since Slovenian independence in 1991 and EU accession in 2004, Brda has rapidly built its reputation for quality wine and now hosts the Brda Wine Festival, attracting international producers and critics annually."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, elegant vintage producing whites of exceptional minerality and aging potential. Rebula of great freshness."),
    (2020, "very_good", "stable", "Good conditions across the region. Merlot-based reds of excellent structure."),
    (2019, "excellent", "rising", "Outstanding vintage — warm summer with cool autumn produced wines of great complexity across all varieties."),
    (2018, "very_good", "stable", "Warm year producing full, rich wines. Pinot Gris and Chardonnay of remarkable concentration."),
    (2017, "excellent", "stable", "Classic Brda vintage — balanced, elegant wines with excellent aging potential."),
]:
    VIN(r_brda, yr, qd, pt, sn)

p_movia = P(
    name="Movia",
    country="Slovenia",
    region_id=r_brda,
    producer_type="winery",
    description="The most internationally celebrated natural wine estate in Slovenia — Aleš Kristančič's historic family estate on the Slovenian-Italian border, producing wines of extraordinary character through extended maceration, indigenous yeast fermentation, and zero-sulphur winemaking. Movia's amphora-aged Rebula (Ribolla Gialla) and the sparkling Puro — a pétillant naturel disgorged only at the table — have become icons of the natural wine movement. Kristančič embodies the Slovenian wine revolution."
)
prod_movia, new = PROD(
    name="Movia Lunar Rebula Brda",
    category="wine_still",
    subcategory="Rebula",
    producer_id=p_movia,
    region_id=r_brda,
    origin_country="Slovenia",
    description="A six-month skin-contact Rebula (Ribolla Gialla) from Movia's oldest vines — the definitive Slovenian orange wine and a reference point for the global skin-contact movement. Amber-golden with aromas of dried apricot, orange peel, chamomile, beeswax, wild herbs, and a tannic structure from the extended skin contact that gives it remarkable aging potential. Fermented with indigenous yeasts in old barrels without sulphur. One of the world's most original and authentic natural wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_movia, "Fuži (Istrian pasta) with wild mushroom and truffle sauce", "complement", "classic", "main", "The wine's tannic texture and oxidative complexity bridge beautifully to earthy mushroom and truffle. A cross-border Adriatic pairing that connects Slovenian wine to its Italian-influenced cuisine.")
    PAIR(prod_movia, "Prosciutto di San Daniele with fig, aged sheep's cheese, and rocket", "complement", "established", "starter", "The wine's dried fruit and earthy complexity bridge naturally to cured meat and aged cheese. Fig echoes its concentrated fruit while rocket's bitterness mirrors its tannin.")
    PAIR(prod_movia, "Roasted suckling pig with fennel, apple, and sage stuffing", "complement", "established", "main", "The wine's textured tannin and complexity from skin contact can support rich roasted pork. Fennel and apple echo its dried fruit and herbal notes.")
    PAIR(prod_movia, "Aged Tolminc (Slovenian Alpine cheese) with honey and walnuts", "complement", "established", "cheese", "Slovenian mountain cheese with Slovenian natural wine — the wine's tannic structure and dried fruit character balance the cheese's semi-hard richness. Honey and walnuts echo its fruit and mineral complexity.")

p_edi_simcic = P(
    name="Edi Simčič",
    country="Slovenia",
    region_id=r_brda,
    producer_type="winery",
    description="One of Brda's most technically accomplished estates, producing polished, internationally competitive wines from flysch soils with a focus on Chardonnay, Sauvignon Blanc, and Merlot blends. Edi Simčič's wines show the refinement and elegance that opoka soils can achieve — the estate's Teodora (Chardonnay) and Kolos (Merlot-dominant blend) are regularly ranked among Slovenia's finest wines and have brought Brda to international wine fair attention."
)
prod_simcic, new = PROD(
    name="Edi Simčič Kolos Brda",
    category="wine_still",
    subcategory="Merlot",
    producer_id=p_edi_simcic,
    region_id=r_brda,
    origin_country="Slovenia",
    description="The prestige Merlot-dominant blend from Brda's most technically accomplished estate — Merlot with Cabernet Sauvignon and Cabernet Franc from opoka (flysch marl) soils on the Slovenian-Italian border. The wine shows remarkable elegance and complexity: dark cherry, cedar, violet, fine tannins, and a mineral-earthy quality that reflects the flysch terroir. More refined and European in style than many Merlot-based wines, with genuine aging potential. Slovenia's most serious red wine.",
    price_tier="premium"
)
if new:
    PAIR(prod_simcic, "Veal cheeks braised with red wine, mushrooms, and tarragon gremolata", "complement", "established", "main", "Merlot-dominant Brda with braised veal — the wine's elegance and mineral refinement complement the delicate braised veal. Mushrooms bridge its earthy depth while tarragon gremolata adds fresh aromatic contrast.")
    PAIR(prod_simcic, "Duck breast with cherry reduction and grilled polenta", "complement", "established", "main", "The wine's dark cherry character mirrors the cherry reduction precisely. Duck's richness is balanced by Merlot's tannin and acidity while polenta provides earthy grounding.")
    PAIR(prod_simcic, "Lamb rack with herb crust, lentils, and red wine jus", "complement", "established", "main", "A classic Merlot-lamb pairing elevated by the wine's European refinement. Herbs echo its aromatic complexity while lentils bridge its mineral depth.")
    PAIR(prod_simcic, "Aged Bovec cheese with Brda cherries and hazelnuts", "complement", "suggested", "cheese", "Slovenian sheep's milk cheese with cherries from Brda — a hyperlocal pairing. The wine's dark cherry character echoes the fruit while aged cheese's density is balanced by Merlot's elegance.")

# === MÂCON (France) ===
print("\n=== Mâcon (France) ===")
r_macon = R(
    name="Mâcon",
    country="France",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Mâcon AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The southern gateway to Burgundy, where Chardonnay grown on Jurassic limestone and clay soils produces wines of genuine charm, freshness, and value. The Mâconnais stretches from Tournus in the north to Pouilly-Fuissé in the south, with village appellations (Mâcon-Villages, then specific village names like Mâcon-Lugny, Mâcon-Solutré) offering progressive complexity and site expression. The region's best wines — particularly from the Solutré and Chasselas villages near the Rock of Solutré — offer Burgundian terroir character at prices far below the Côte d'Or.",
    key_producers="Domaine Bret Brothers, Domaine de la Bongran, Domaine Valette, Clos des Rocs",
    historical_context="The Mâconnais has been cultivated since Roman times and the region's wine capital, Mâcon, was an important medieval wine trading centre. The region suffered from the loss of its Paris market after the railway connected Burgundy to the capital, but the modern era has seen a revival through the recognition of individual village wines and the emergence of small-scale artisan producers working with old vines."
)
for yr, qd, pt, sn in [
    (2022, "very_good", "stable", "Good vintage despite early summer heat. Chardonnay showed good natural acidity from the limestone soils."),
    (2021, "excellent", "rising", "Cool, precise vintage producing Mâcon whites of extraordinary freshness and mineral clarity."),
    (2020, "very_good", "stable", "Warm year producing riper, richer styles. Good village wines for early drinking."),
    (2019, "excellent", "rising", "Outstanding vintage — long, warm growing season produced complex, age-worthy Mâcon from top sites."),
    (2018, "very_good", "stable", "Rich, full wines from the hot summer. Less tension than cooler vintages but good fruit character."),
]:
    VIN(r_macon, yr, qd, pt, sn)

p_bret = P(
    name="Domaine Bret Brothers",
    country="France",
    region_id=r_macon,
    producer_type="winery",
    description="Jean-Guillaume and Marc Bret's biodynamic estate based in Vinzelles, producing benchmark Mâcon-Villages and Pouilly-Vinzelles from multiple village sites across the Mâconnais. The brothers are among the region's most innovative producers, bottling individual village wines under lieu-dit designations that reveal the remarkable terroir variation within the appellation. Their wines are unfined and unfiltered, showing the depth and complexity achievable from Mâcon's best limestone sites."
)
prod_bret, new = PROD(
    name="Bret Brothers La Soufrandière Mâcon-Vinzelles",
    category="wine_still",
    subcategory="Chardonnay",
    producer_id=p_bret,
    region_id=r_macon,
    origin_country="France",
    description="From the La Soufrandière lieu-dit in Vinzelles — biodynamically farmed Chardonnay on Jurassic limestone producing a wine of remarkable purity and Burgundian character. Fermented with indigenous yeasts in old Burgundy barrels, aged on lees without fining or filtration. Lemon zest, white peach, hazelnut, chalk, and a mineral limestone tension that defines the Mâconnais at its finest. A genuine alternative to Côte de Beaune at a fraction of the price.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_bret, "Beurre blanc basted halibut with pea shoots and lemon oil", "complement", "classic", "main", "Burgundian Chardonnay with beurre blanc — a classical pairing. The wine's hazelnut and butter notes mirror the sauce while its mineral acidity lifts the halibut.")
    PAIR(prod_bret, "Comté affinage with walnut bread and quince", "complement", "classic", "cheese", "The wine's hazelnut and limestone mineral notes are naturally aligned with aged Comté. Walnut bread echoes its nutty complexity while quince mirrors its stone fruit brightness.")
    PAIR(prod_bret, "Quenelles de brochet with Nantua sauce (crayfish bisque)", "complement", "classic", "main", "The classic Lyon-Mâcon pairing — pike dumplings in crayfish sauce with a crisp Mâcon white. The wine's acidity cuts through the rich bisque while its limestone mineral complements the freshwater fish.")
    PAIR(prod_bret, "Sautéed girolles with parsley, garlic, and grilled sourdough", "complement", "established", "starter", "The wine's hazelnut and earthy secondary notes bridge to girolle mushrooms. Garlic adds aromatic depth while sourdough provides texture that absorbs the wine's richness.")

p_valette = P(
    name="Domaine Valette",
    country="France",
    region_id=r_macon,
    producer_type="winery",
    description="One of the Mâconnais's most idiosyncratic and celebrated estates — Philippe and Chantal Valette produce Mâcon from very old Chardonnay vines (up to 80 years) on Solutré limestone, aged exclusively in old Burgundy barrels for extended periods without racking. The wines are distinctly Burgundian in style — textured, complex, and long-lived — challenging the perception of Mâcon as entry-level Burgundy. Their Mâcon-Chaintre and Pouilly-Fuissé are cult wines in informed circles."
)
prod_valette, new = PROD(
    name="Domaine Valette Mâcon-Chaintré Tradition",
    category="wine_still",
    subcategory="Chardonnay",
    producer_id=p_valette,
    region_id=r_macon,
    origin_country="France",
    description="From 70–80 year old Chardonnay vines on Solutré limestone — one of the Mâconnais's most complex and age-worthy wines. Extended aging in old Burgundy barrels without racking produces a wine of extraordinary texture, depth, and mineral complexity: white truffle, hazelnut, warm brioche, lemon curd, chalk, and an almost Meursault-like depth that develops magnificently over a decade. The definitive argument against Mâcon as simple early-drinking wine.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_valette, "Veal fricassee with morel mushrooms, cream, and tarragon", "complement", "classic", "main", "Old-vine Mâcon with morels — the wine's truffle and hazelnut complexity bridge to the earthy mushrooms while its acidity cuts through the cream. Tarragon adds aromatic freshness.")
    PAIR(prod_valette, "Pan-seared foie gras with caramelised apple and brioche", "complement", "established", "starter", "Textured old-vine Mâcon Chardonnay with foie gras — the wine's richness and acidity balance the liver's fat. Caramelised apple echoes its stone fruit while brioche mirrors its buttery texture.")
    PAIR(prod_valette, "Poulet de Bresse en croûte with black truffle cream sauce", "complement", "classic", "main", "France's finest chicken with its regional white wine — Bresse poultry with Mâcon Chardonnay is a classic Burgundian table pairing. Black truffle bridges to the wine's earthy secondary notes.")
    PAIR(prod_valette, "Saint-Nectaire with truffle honey and toasted walnuts", "complement", "established", "cheese", "The wine's truffle and hazelnut notes mirror Saint-Nectaire's earthy, semi-soft character. Truffle honey amplifies the connection while walnuts echo its mineral complexity.")

# Final counts
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
print("\nDone.")
cur.close()
conn.close()
