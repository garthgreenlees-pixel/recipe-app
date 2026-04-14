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
    # valid pairing_type: complement, contrast, bridge, cleanse, elevate
    # valid confidence: classic, established, suggested, adventurous, experimental
    cur.execute("""INSERT INTO pairing_intelligence
      (beverage_product_id, food_description, pairing_type, confidence,
       meal_context, flavour_logic, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,1)""",
      (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# === NAHE (Germany) ===
print("\n=== Nahe (Germany) ===")
r_nahe = R(
    name="Nahe",
    country="Germany",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Nahe",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="One of Germany's most diverse and under-appreciated wine regions, where the Nahe river cuts through dramatically varied volcanic, slate, and sandstone soils producing Rieslings of extraordinary individuality. No other German region matches the Nahe's geological complexity — soils change within metres, creating wines that range from steely and mineral to tropical and floral. The Dönnhoff estate alone has elevated the Nahe to international prestige.",
    key_producers="Weingut Dönnhoff, Schlossgut Diel, Emrich-Schönleber, Gut Hermannsberg",
    historical_context="The Nahe was historically overshadowed by the Mosel and Rhine despite producing wines of comparable quality. The modern renaissance was driven by Helmut Dönnhoff in the 1970s–80s, whose Hermannshöhle and Niederhäuser Hermannsberg wines demonstrated the region's world-class potential. The VDP classification of Erste Lage and Grosse Lage sites has since elevated awareness significantly."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Cool, fresh vintage producing Rieslings of exceptional mineral purity and aging potential. Dönnhoff Hermannshöhle particularly impressive."),
    (2020, "very_good", "rising", "Warm year with good natural acidity. Rich yet precise wines across the diversity of Nahe soils."),
    (2019, "exceptional", "rising", "Third consecutive warm vintage. Concentrated, complex wines with remarkable site expression."),
    (2018, "excellent", "stable", "Full, rich wines from the hot summer. Lower acidity compensated by depth of extract and flavour."),
    (2017, "very_good", "stable", "Late frosts reduced yields. Survivors showed excellent concentration and mineral focus."),
]:
    VIN(r_nahe, yr, qd, pt, sn)

p_donnhoff = P(
    name="Weingut Dönnhoff",
    country="Germany",
    region_id=r_nahe,
    producer_type="winery",
    description="The greatest producer of the Nahe and among Germany's finest wine estates. Helmut Dönnhoff and his son Cornelius craft Rieslings of extraordinary precision from the great Grosses Gewächs sites — Hermannshöhle, Oberhäuser Brücke, Niederhäuser Hermannsberg. The wines balance power and delicacy with a finesse that rivals the best Mosel and Rheingau. Their Beerenauslesen and TBAs from Oberhäuser Brücke are among Germany's most sought-after sweet wines."
)
prod_don, new = PROD(
    name="Dönnhoff Oberhäuser Brücke Riesling Grosses Gewächs",
    category="wine_still",
    subcategory="Riesling",
    producer_id=p_donnhoff,
    region_id=r_nahe,
    origin_country="Germany",
    description="One of the Nahe's greatest dry Rieslings, from the monopole Oberhäuser Brücke — a dramatic volcanic porphyry slope above Oberhausen. Fermented and aged in traditional Fuder casks with no SO2 addition, it develops extraordinary complexity: volcanic stone, citrus zest, white flowers, exotic fruit, and a mineral precision that is unique to this remarkable site. Among Germany's most collectable dry white wines.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_don, "Grilled sole with lemon butter and fine herbs", "complement", "classic", "main", "The wine's mineral precision and citrus acidity are perfectly matched to delicate sole. Lemon butter echoes its brightness while the volcanic mineral depth elevates the fish beyond its simplicity.")
    PAIR(prod_don, "White asparagus with Hollandaise, prosciutto, and chervil", "complement", "classic", "starter", "The Nahe's most celebrated Riesling with Germany's most celebrated spring vegetable — a regional and seasonal rite. The wine's floral notes and mineral acidity complement asparagus's subtle bitterness.")
    PAIR(prod_don, "Pickled herring with cream, dill, and rye crispbread", "complement", "established", "starter", "High-acid Nahe Riesling with pickled fish — a North European classic. The wine's acidity mirrors the pickle, its fruit offsets the cream, and volcanic mineral echoes the oceanic herring.")
    PAIR(prod_don, "Spiced quince tart with vanilla cream", "complement", "suggested", "dessert", "The GG's slight residual sweetness and stone fruit character bridge to quince. Spice echoes its volcanic mineral complexity.")

p_emrich = P(
    name="Emrich-Schönleber",
    country="Germany",
    region_id=r_nahe,
    producer_type="winery",
    description="One of the Nahe's finest estates, producing benchmark Rieslings from the Monzinger Halenberg and Frühlingsplätzchen sites — steep, blue slate slopes above the village of Monzingen. Frank Schönleber's wines have a distinctive aromatic intensity and mineral transparency that sets them apart from Dönnhoff's volcanic power. The Grosses Gewächs wines age magnificently over decades."
)
prod_emrich, new = PROD(
    name="Emrich-Schönleber Monzinger Halenberg Riesling Grosses Gewächs",
    category="wine_still",
    subcategory="Riesling",
    producer_id=p_emrich,
    region_id=r_nahe,
    origin_country="Germany",
    description="From the steep blue-slate Halenberg site above Monzingen — the Nahe's most celebrated slate-based Riesling. Aromatic, transparent, and deeply mineral with blue fruit, lime zest, white flowers, graphite, and a vibrating slate minerality that evolves magnificently over 10–20 years. A counterpoint to Dönnhoff's volcanic power, this is slate finesse at the highest level.",
    price_tier="ultra_premium"
)
if new:
    PAIR(prod_emrich, "Trout meunière with almonds, lemon, and parsley", "complement", "classic", "main", "Classic Nahe pairing — freshwater trout from the river with the region's finest slate Riesling. The wine's mineral precision and citrus acidity elevate the simple preparation.")
    PAIR(prod_emrich, "Crab bisque with tarragon cream and fennel oil", "complement", "established", "starter", "Slate Riesling and shellfish bisque — the wine's mineral depth anchors the bisque's richness, tarragon bridges to its herbal notes, and fennel oil mirrors its cool aromatics.")
    PAIR(prod_emrich, "Sauerkraut with juniper-cured pork and caraway", "complement", "established", "main", "High-acidity Riesling with fermented cabbage and cured pork — a classical German combination that demonstrates the grape's extraordinary affinity with preserved and fermented foods.")
    PAIR(prod_emrich, "Chèvre with wildflower honey and walnuts", "complement", "suggested", "cheese", "Slate mineral Riesling with goat cheese — the wine's citrus and mineral lift cuts through chèvre's tanginess. Honey adds sweetness while walnuts mirror the wine's subtle bitterness.")

# === GAILLAC AOC (France) ===
print("\n=== Gaillac AOC (France) ===")
r_gaillac = R(
    name="Gaillac",
    country="France",
    beverage_family="wine",
    designation_type="appellation",
    designation_name="Gaillac AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="One of France's oldest and most eccentric wine appellations, centred on the Tarn river east of Toulouse in Southwest France. Gaillac is a treasure trove of obscure indigenous varieties — Mauzac, Len de l'El, Ondenc, Braucol (Fer Servadou), Duras, Prunelart — producing wines of genuine originality. The region encompasses sparkling wines (méthode gaillacoise with natural bubbles), dry whites, sweet whites, and tannic reds that share nothing with the international mainstream.",
    key_producers="Domaine Plageoles, Château Lastours, Causse Marine, Mas d'Aurel",
    historical_context="Gaillac claims to be one of France's oldest wine regions, with Roman-era viticulture documented around the town of Gaillac. The appellation was officially recognised in 1938. The modern resurgence was led by Robert and Bernard Plageoles, who dedicated their estate to preserving Gaillac's ancient indigenous varieties — some of which survive only in their vineyards."
)
for yr, qd, pt, sn in [
    (2021, "very_good", "stable", "Cool, rainy spring followed by dry summer. Indigenous varieties showed excellent character and freshness."),
    (2020, "excellent", "rising", "Hot, dry vintage ideal for the region's thick-skinned indigenous reds. Rich, concentrated wines with good structure."),
    (2019, "very_good", "stable", "Long, warm growing season. Exceptional sweet wines from Mauzac and Ondenc."),
    (2018, "excellent", "stable", "Outstanding vintage across all styles. Len de l'El whites of particular aromatic intensity."),
    (2017, "good", "stable", "Spring frosts reduced yields. Surviving fruit concentrated and interesting."),
]:
    VIN(r_gaillac, yr, qd, pt, sn)

p_plageoles = P(
    name="Domaine Plageoles",
    country="France",
    region_id=r_gaillac,
    producer_type="winery",
    description="The guardian of Gaillac's ancient viticultural heritage. Robert Plageoles and now his son Bernard have dedicated their estate to preserving and showcasing indigenous varieties that would otherwise have disappeared — Ondenc, Verdanel, Mauzac Roux, and others found nowhere else in France. Their wines are idiosyncratic, authentic, and impossible to categorise within the mainstream fine wine world. Vin d'Autan (Ondenc botrytis dessert wine) is considered one of France's great forgotten treasures."
)
prod_plageoles, new = PROD(
    name="Domaine Plageoles Mauzac Nature Gaillac",
    category="wine_sparkling",
    subcategory="Mauzac",
    producer_id=p_plageoles,
    region_id=r_gaillac,
    origin_country="France",
    description="A sparkling wine made by the ancestral méthode gaillacoise — the wine is bottled before fermentation finishes, creating natural bubbles from the wine's own sugars with no disgorgement. Slightly cloudy, gently sparkling, bone dry, and intensely aromatic: apple, quince, white flowers, chalk, and a completely unique character that modern champagne cannot replicate. One of France's most original traditional sparkling wines.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_plageoles, "Charcuterie and pâté with cornichons and mustard", "complement", "classic", "starter", "The wine's crisp bubble and apple freshness cut through the fat of charcuterie. Cornichons echo its acidity while mustard bridges to its spice notes — a classic Southwest French apéritif pairing.")
    PAIR(prod_plageoles, "Fresh goat cheese with herbs and olive oil", "complement", "established", "starter", "The wine's chalky mineral character and bright acidity are natural partners for fresh goat cheese. Herbs echo its floral complexity.")
    PAIR(prod_plageoles, "Apple tart Tatin with crème fraîche", "complement", "classic", "dessert", "Mauzac's dominant apple character bridges perfectly to tarte Tatin. The wine's gentle sweetness and natural bubbles provide refreshing contrast to the caramelised apple.")
    PAIR(prod_plageoles, "Oysters with shallot vinegar and rye bread", "complement", "established", "starter", "The ancestral method's natural residual sweetness and chalky mineral quality mirror oysters' saline and mineral character. A natural pairing for a wine with ancient roots.")

p_causse = P(
    name="Causse Marine",
    country="France",
    region_id=r_gaillac,
    producer_type="winery",
    description="Patrice Lescarret's biodynamic estate on the limestone Causse plateau north of Gaillac, producing some of the region's most intellectually serious wines. The estate uses only indigenous varieties and traditional methods — low sulphur, indigenous yeasts, no fining or filtration. Their Peyrouzelles (Braucol) and Rasdu (Duras) reds show what Gaillac's obscure native varieties can achieve with minimal intervention."
)
prod_causse, new = PROD(
    name="Causse Marine Peyrouzelles Gaillac Rouge",
    category="wine_still",
    subcategory="Braucol",
    producer_id=p_causse,
    region_id=r_gaillac,
    origin_country="France",
    description="A pure expression of Braucol (Fer Servadou) from biodynamic limestone soils on the Causse plateau. Dark ruby, aromatic, and earthy with red cherry, violet, garrigue herbs, iron mineral, and a distinctive tannic structure that is firmly regional. Fermented with indigenous yeasts, aged in old barrels with minimal SO2. One of the most authentic expressions of a variety found almost nowhere else in the world.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_causse, "Cassoulet with duck confit, Toulouse sausage, and haricot beans", "complement", "classic", "main", "The quintessential Southwest French pairing — the region's iconic dish with its most traditional grape variety. Braucol's earthy tannins and iron mineral complement the cassoulet's richness and the duck's depth.")
    PAIR(prod_causse, "Grilled lamb chops with herbs de Provence and flageolet beans", "complement", "established", "main", "Regional lamb with indigenous red — the wine's garrigue herbs mirror the Provençal herbs, iron mineral bridges the lamb's character, and acidity lifts the beans.")
    PAIR(prod_causse, "Roquefort with walnut bread and dried figs", "contrast", "adventurous", "cheese", "Tannic, earthy Braucol with blue cheese is an unconventional pairing that works through contrast — the wine's iron and garrigue cut through Roquefort's creaminess while figs moderate the tannins.")
    PAIR(prod_causse, "Duck magret with green peppercorn sauce and celeriac purée", "complement", "established", "main", "Duck and Braucol is a Southwest classic. Green pepper echoes the wine's spice while celeriac's earthy sweetness bridges to its mineral depth.")

# === ROUSSILLON (France) ===
print("\n=== Roussillon (France) ===")
r_roussillon = R(
    name="Roussillon",
    country="France",
    beverage_family="wine",
    designation_type="regional",
    designation_name="IGP Côtes Catalanes / AOP Roussillon",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="France's most southerly wine region, pressed against the Spanish border in the Pyrénées-Orientales department. The Catalan character of Roussillon is evident in its varieties — Grenache Noir, Gris, and Blanc; Carignan; Mourvèdre; Macabeo; Tourbat — and its traditions, which include the great Vins Doux Naturels of Banyuls, Maury, and Rivesaltes. The modern era has brought a wave of natural wine producers drawn by the extreme sunshine, ancient schist vineyards, and low land prices.",
    key_producers="Domaine Gauby, Mas Amiel, Domaine de la Rectorie, Domaine Matassa",
    historical_context="Roussillon was part of Catalonia until the Treaty of the Pyrenees in 1659 ceded it to France. The vinous tradition of Vins Doux Naturels — fortified wines from Grenache — dates to the 13th century and the work of Arnau de Vilanova. The modern dry wine movement began in the 1980s with Gérard Gauby and has since attracted producers from across France and internationally."
)
for yr, qd, pt, sn in [
    (2021, "excellent", "rising", "Good freshness despite warm summer. Schist-based wines showed excellent mineral tension."),
    (2020, "very_good", "stable", "Hot, dry year — challenging for freshness but rewarding for concentration. Grenache particularly successful."),
    (2019, "excellent", "rising", "Ideal conditions across the region. Natural wine producers achieved remarkable results."),
    (2018, "very_good", "stable", "Classic warm Roussillon vintage with good balance of richness and structure."),
    (2017, "excellent", "stable", "Long, dry summer with beneficial cooling winds. Exceptional Grenache Gris whites and Carignan reds."),
]:
    VIN(r_roussillon, yr, qd, pt, sn)

p_gauby = P(
    name="Domaine Gauby",
    country="France",
    region_id=r_roussillon,
    producer_type="winery",
    description="The reference producer of modern Roussillon — Gérard and Ghislaine Gauby essentially invented the idea of serious dry wine in a region known primarily for fortified Vins Doux Naturels. Operating biodynamically from schist vineyards above Calce, they produce Grenache Gris whites and old-vine Grenache/Carignan reds of extraordinary mineral depth and freshness. The estate has inspired a generation of producers to see Roussillon's potential beyond the traditional sweet wine category."
)
prod_gauby, new = PROD(
    name="Domaine Gauby La Muntada Roussillon Rouge",
    category="wine_still",
    subcategory="Grenache",
    producer_id=p_gauby,
    region_id=r_roussillon,
    origin_country="France",
    description="The flagship red from Roussillon's reference estate — old-vine Grenache Noir from steep schist terraces above Calce, biodynamically farmed and produced with minimal intervention. Dense, complex, and mineral with black olive, dark cherry, garrigue, lavender, iron mineral, and the explosive concentration that comes from 60–80 year old dryland bush vines in extreme Mediterranean conditions. One of France's great natural wines.",
    price_tier="premium"
)
if new:
    PAIR(prod_gauby, "Wild boar stew with black olives, tomato, and orange zest", "complement", "classic", "main", "The Catalan flavour profile of the dish mirrors the wine's garrigue and Mediterranean character. Black olive echoes the wine's olive notes, tomato brightens its acidity, and orange zest mirrors its warm fruit.")
    PAIR(prod_gauby, "Grilled lamb with anchovy, rosemary, and roasted aubergine", "complement", "established", "main", "Southern French lamb with Grenache — the wine's garrigue and lavender echo the rosemary, anchovy adds saline depth to mirror the mineral schist, and aubergine bridges to the wine's earthy density.")
    PAIR(prod_gauby, "Duck confit with tapenade and lentilles du Puy", "complement", "established", "main", "Duck confit with old-vine Grenache is a Languedoc-Roussillon classic. Tapenade echoes the wine's olive character while lentils bridge to its earthy mineral depth.")
    PAIR(prod_gauby, "Aged Ossau-Iraty with cherry preserve and walnuts", "complement", "suggested", "cheese", "Basque sheep's milk cheese with Roussillon Grenache — the wine's dark fruit and mineral complexity complement the cheese's nuttiness. Cherry preserve echoes its fruit while walnuts mirror its earthy depth.")

p_matassa = P(
    name="Domaine Matassa",
    country="France",
    region_id=r_roussillon,
    producer_type="winery",
    description="Tom Lubbe's biodynamic estate in the village of Calce, producing some of Roussillon's most sought-after natural wines. Lubbe — a South African-born winemaker — works with old-vine Grenache Gris, Macabeo, and Carignan on white granite and gneiss soils in the Côtes Catalanes. The wines have a distinctive freshness, salinity, and aromatic complexity that has attracted a devoted following in the natural wine world."
)
prod_matassa, new = PROD(
    name="Domaine Matassa Blanc Côtes Catalanes",
    category="wine_still",
    subcategory="Grenache Gris",
    producer_id=p_matassa,
    region_id=r_roussillon,
    origin_country="France",
    description="A remarkable white from old-vine Grenache Gris and Macabeo grown on white granite and gneiss soils in Calce. Golden, textured, and aromatic with dried orange peel, white stone fruit, fennel seed, sea salt, and a distinctive saline-mineral finish that speaks of its coastal proximity and ancient granite soils. Fermented with indigenous yeasts in old barrels, this is Roussillon white wine at its most original and compelling.",
    price_tier="premium"
)
if new:
    PAIR(prod_matassa, "Grilled sea bass with fennel, pastis, and lemon", "complement", "classic", "main", "The wine's fennel and saline character mirrors both the sea bass and the fennel garnish. Pastis amplifies the anise connection while lemon echoes its citrus brightness.")
    PAIR(prod_matassa, "Salt cod brandade with roasted peppers and herbs", "complement", "established", "main", "The wine's salinity and dried citrus peel notes bridge perfectly to salt cod. Roasted peppers add sweetness while herbs echo its Mediterranean aromatic complexity.")
    PAIR(prod_matassa, "Boquerones with tomato, capers, and olive oil", "complement", "classic", "starter", "Catalan white with Catalan ingredients — the wine's saline mineral quality lifts the marinated anchovies, capers echo its briny edge, and tomato bridges to its bright acidity.")
    PAIR(prod_matassa, "Aged Manchego with quince paste and almonds", "complement", "suggested", "cheese", "The wine's dried fruit and saline character pairs beautifully with aged sheep's milk cheese. Quince echoes its stone fruit while almonds bridge to its textured, slightly oxidative complexity.")

# === ALENTEJO (Portugal) ===
print("\n=== Alentejo (Portugal) ===")
r_alentejo = R(
    name="Alentejo",
    country="Portugal",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Alentejo DOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Portugal's largest and most commercially successful wine region, covering the vast inland plain south of Lisbon between the Tagus and Algarve. Despite the brutal heat of the Alentejo summer, modern temperature-controlled winemaking has produced wines of real quality — powerful, ripe Aragonez (Tempranillo) and Alicante Bouschet reds alongside aromatic Antão Vaz and Arinto whites. The historic marble and granite fortress towns of Évora, Estremoz, and Monsaraz dot a landscape of cork oak, olive, and ancient schist soils.",
    key_producers="Herdade do Esporão, Niepoort (Herdade do Peso), Herdade dos Grous, Quinta do Crasto Alentejo",
    historical_context="The Alentejo has been cultivated since Roman times — the region supplied Rome with wine, oil, and grain. Modern wine quality only emerged from the 1990s when technology and investment transformed the region. The Herdade do Esporão was the pioneer, producing internationally competitive wines that opened export markets. Today the region accounts for nearly half of Portugal's domestic wine consumption."
)
for yr, qd, pt, sn in [
    (2021, "very_good", "stable", "Good freshness despite the hot summer, with cooler nights preserving acidity. Reds of excellent balance."),
    (2020, "excellent", "rising", "Outstanding year with ideal ripening conditions. Alicante Bouschet achieved remarkable depth and structure."),
    (2019, "excellent", "rising", "Long, dry summer with moderate temperatures. Wines of exceptional concentration and aging potential."),
    (2018, "very_good", "stable", "Hot year with early harvest. Rich, approachable wines with good natural fruit character."),
    (2017, "excellent", "stable", "Exceptional vintage — the best in a decade according to many producers. Concentrated, complex reds."),
]:
    VIN(r_alentejo, yr, qd, pt, sn)

p_esporao = P(
    name="Herdade do Esporão",
    country="Portugal",
    region_id=r_alentejo,
    producer_type="winery",
    description="The estate that pioneered modern Alentejo wine. Founded in 1973 by the Roquette family, Esporão assembled 1,000 hectares near Reguengos de Monsaraz and built a technically advanced winery that produced wines capable of competing internationally. Today under Australian winemaker David Baverstock, the estate produces a comprehensive range from the reliable Esporão Reserva to the prestige Esporão Private Selection and Torre collection — all with a commitment to indigenous varieties and sustainable farming."
)
prod_esporao, new = PROD(
    name="Esporão Reserva Tinto Alentejo",
    category="wine_still",
    subcategory="Aragonez",
    producer_id=p_esporao,
    region_id=r_alentejo,
    origin_country="Portugal",
    description="The benchmark Alentejo red — a blend of Aragonez, Trincadeira, and Alicante Bouschet from 30-year-old vines on schist soils, aged in French and American oak. Medium-full bodied with ripe dark cherry, plum, dark chocolate, dried herbs, and a warm, spiced finish. One of Portugal's most consistent quality-value wines and the wine that put Alentejo on the international map.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_esporao, "Slow-roasted black pork (porco preto) with migas and grilled peppers", "complement", "classic", "main", "The quintessential Alentejo pairing — the region's iconic black Iberian pig with its most celebrated wine. The wine's ripe dark fruit and warm spice complement the pork's richness while herbs bridge the migas.")
    PAIR(prod_esporao, "Açorda alentejana (bread soup with garlic, coriander, and poached egg)", "complement", "established", "main", "The Alentejo's most humble yet deeply satisfying dish pairs naturally with the regional red. The wine's warmth and fruit echo the soup's garlic and herb depth.")
    PAIR(prod_esporao, "Lamb stew with chickpeas, cumin, and fresh coriander", "complement", "established", "main", "Southern Portuguese lamb stew with indigenous red — the wine's warmth and spice mirror the cumin while its fruit complements the lamb. Coriander adds a herbaceous bridge.")
    PAIR(prod_esporao, "Queijo de Serpa (Portuguese sheep's milk cheese) with quince paste", "complement", "classic", "cheese", "Portugal's most celebrated soft sheep's milk cheese with a regional red — the wine's warm spice and dark fruit balance the cheese's intense savouriness. Quince paste echoes the wine's plum notes.")

p_grous = P(
    name="Herdade dos Grous",
    country="Portugal",
    region_id=r_alentejo,
    producer_type="winery",
    description="A biodynamic estate in the Beja sub-region of Alentejo, producing wines of organic purity and regional character. The estate has committed to biodiversity and sustainable farming while producing wines that include the rare Moon Harvested range — picked by moonlight during the cool night to preserve freshness. The estate produces both whites from Antão Vaz and reds from Alicante Bouschet and Touriga Nacional."
)
prod_grous, new = PROD(
    name="Herdade dos Grous Moon Harvested Alentejo Branco",
    category="wine_still",
    subcategory="Antão Vaz",
    producer_id=p_grous,
    region_id=r_alentejo,
    origin_country="Portugal",
    description="A distinctive white wine harvested by moonlight during cool nights to preserve aromatic freshness — an innovative response to the Alentejo's challenging summer heat. Primarily Antão Vaz with Arinto, it shows tropical fruit, white peach, citrus blossom, and fresh herbs with a mineral freshness that belies the region's fierce sunshine. One of Alentejo's most characterful and original whites.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_grous, "Grilled sea bream with lemon, oregano, and roasted tomatoes", "complement", "established", "main", "The wine's citrus freshness and herb notes complement grilled Mediterranean fish. Oregano echoes its herb character while roasted tomato sweetness bridges to its stone fruit.")
    PAIR(prod_grous, "Fried salt cod croquettes with lemon aioli and parsley", "complement", "classic", "starter", "Portuguese salt cod paired with Alentejo white — the wine's freshness and citrus acidity cut through the fried coating while echoing the cod's salt. Lemon aioli mirrors its citrus notes.")
    PAIR(prod_grous, "Chilled gazpacho with cucumber, red pepper, and croutons", "complement", "established", "starter", "The wine's herbal freshness and slight tropical character mirror the cold vegetable soup's brightness. A summer pairing with obvious regional logic.")
    PAIR(prod_grous, "Fresh ricotta with roasted figs and thyme honey", "bridge", "suggested", "dessert", "The wine's stone fruit and floral character bridges to sweet figs and honey. Thyme echoes its herbal notes while ricotta's freshness mirrors its clean finish.")

# === KAKHETI (Georgia) ===
print("\n=== Kakheti (Georgia) ===")
r_kakheti = R(
    name="Kakheti",
    country="Georgia",
    beverage_family="wine",
    designation_type="regional",
    designation_name="Kakheti PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The heartland of Georgian winemaking and home to the world's oldest continuous wine culture — 8,000 years of viticulture evidenced by ancient qvevri (clay vessel) fragments. Kakheti produces around 70% of Georgia's wine, centred on the Alazani Valley and Iori plateaux east of Tbilisi. The region is home to over 400 indigenous varieties, with Rkatsiteli, Kisi, and Mtsvane for whites, and Saperavi — Georgia's greatest red variety — producing deeply coloured, tannic wines of remarkable intensity. The Kakhetian method of fermenting whites with grape skins in qvevri for 6 months produces the world's original 'orange wines' — a tradition now influencing winemakers globally.",
    key_producers="Alaverdi Monastery, Pheasant's Tears, Kindzmarauli Marani, Telavi Wine Cellar",
    historical_context="Neolithic settlements in the Caucasus dating to 6000 BCE show evidence of cultivated grape seeds and fermentation — making Georgia the world's oldest known wine culture. The qvevri tradition — burying large clay vessels in the earth for fermentation and aging — has been UNESCO-recognised since 2013. Georgia's wine renaissance began in the late Soviet era when producers began reclaiming ancient varieties and methods from collectivised agriculture."
)
for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Warm summer with ideal autumn conditions for Saperavi. Qvevri whites of exceptional complexity and depth of colour."),
    (2021, "very_good", "stable", "Classic Kakheti vintage — long growing season producing well-balanced reds and textured amber whites."),
    (2020, "excellent", "rising", "Outstanding year for Saperavi — deeply coloured, tannic wines with remarkable aging potential."),
    (2019, "very_good", "stable", "Good conditions across the region. Rkatsiteli qvevri whites of particular depth and tannic structure."),
    (2018, "very_good", "stable", "Warm, dry vintage producing full, concentrated wines. Saperavi of great intensity and longevity."),
]:
    VIN(r_kakheti, yr, qd, pt, sn)

p_pheasant = P(
    name="Pheasant's Tears",
    country="Georgia",
    region_id=r_kakheti,
    producer_type="winery",
    description="The most internationally celebrated natural wine estate in Georgia, founded by American painter John Wurdeman and Georgian winemaker Gela Patalishvili in the village of Sighnaghi. Pheasant's Tears produces wines exclusively in qvevri using indigenous varieties and zero intervention — no added sulphur, no filtering, no fining. Their wines have introduced a global audience to Georgian amber wines and native varieties like Rkatsiteli, Kisi, Chinuri, and Tavkveri, becoming reference points for the natural wine movement worldwide."
)
prod_pheasant, new = PROD(
    name="Pheasant's Tears Rkatsiteli Kakheti",
    category="wine_still",
    subcategory="Rkatsiteli",
    producer_id=p_pheasant,
    region_id=r_kakheti,
    origin_country="Georgia",
    description="The definitive expression of Georgia's most important white variety — Rkatsiteli fermented and aged 6 months on skins in traditional qvevri. Amber-gold in colour, it shows dried apricot, orange peel, beeswax, saffron, walnut, and a deep tannic structure from the extended skin contact that is unique to the Kakhetian method. A wine of ancient character and modern relevance — one of the world's most original and important expressions of the amber wine tradition.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_pheasant, "Slow-cooked chicken with walnut sauce (satsivi) and Georgian flatbread", "complement", "classic", "main", "The traditional Georgian pairing for amber Rkatsiteli — satsivi's walnut and spice are direct mirrors of the wine's own walnut and dried fruit character. Flatbread absorbs the rich sauce.")
    PAIR(prod_pheasant, "Grilled lamb kebab (mtsvadi) with tkemali (plum sauce) and fresh herbs", "complement", "classic", "main", "Georgia's most iconic outdoor dish with its most authentic wine — the wine's tannins and oxidative depth complement the charred lamb, tkemali bridges to its dried fruit complexity.")
    PAIR(prod_pheasant, "Khinkali (Georgian soup dumplings) with chilli and fresh coriander", "complement", "established", "main", "The amber wine's tannins and weight can handle the richness of meat-filled dumplings. Coriander bridges to the wine's herbal notes while chilli heat is moderated by its dried fruit complexity.")
    PAIR(prod_pheasant, "Aged sheep's milk cheese with quince preserve and walnuts", "complement", "established", "cheese", "The wine's walnut and dried fruit character perfectly mirrors this cheese board's components. Tannins from skin contact cut through the fat of aged sheep's milk cheese.")

p_alaverdi = P(
    name="Alaverdi Monastery",
    country="Georgia",
    region_id=r_kakheti,
    producer_type="winery",
    description="One of the world's most ancient wine-producing monasteries, with viticulture documented on this site since the 6th century CE. The Alaverdi Cathedral estate was restored in the 2000s under Bishop David, reclaiming ancient qvevri and indigenous variety plantings. The monastery produces wines using exclusively traditional Kakhetian methods — extended maceration in qvevri, no technology intervention — as an act of cultural and spiritual preservation as much as commercial winemaking."
)
prod_alaverdi, new = PROD(
    name="Alaverdi Monastery Saperavi Kakheti",
    category="wine_still",
    subcategory="Saperavi",
    producer_id=p_alaverdi,
    region_id=r_kakheti,
    origin_country="Georgia",
    description="From one of the world's oldest continuously producing wine estates — Saperavi grown on Alaverdi's historic vineyards and fermented traditionally in qvevri. Saperavi is one of the world's rare naturally teinturier varieties (red flesh as well as skin), producing wines of near-black depth and dense tannic structure. Aromas of dark cherry, blackberry, leather, dark chocolate, dried herbs, and earth — powerful, traditional, and ancient in character.",
    price_tier="mid_range"
)
if new:
    PAIR(prod_alaverdi, "Slow-braised beef with pomegranate, cinnamon, and fenugreek (chakapuli)", "complement", "classic", "main", "Georgian beef stew with the country's greatest red variety — the wine's tannic power supports the richness of braised beef, pomegranate echoes its dark fruit, and the warm spice bridges its earthy depth.")
    PAIR(prod_alaverdi, "Pkhali (spinach and walnut rolls) with pomegranate seeds", "complement", "established", "starter", "Georgian vegetable appetisers with Saperavi — the wine's tannin and dark fruit cut through the richness of walnut filling. Pomegranate seeds echo the wine's tart edge.")
    PAIR(prod_alaverdi, "Wild mushroom and cheese-stuffed khachapuri", "complement", "established", "main", "Georgia's iconic cheese bread with wild mushroom filling pairs naturally with Saperavi. The wine's earthy depth echoes the mushrooms while its tannins cut through the melted cheese richness.")
    PAIR(prod_alaverdi, "Dark chocolate with dried cherry and almond", "complement", "suggested", "dessert", "Saperavi's near-black depth and dark cherry character bridges naturally to dark chocolate. Dried cherry amplifies the wine's fruit while almond echoes its earthy bitterness.")

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
