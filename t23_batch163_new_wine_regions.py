#!/usr/bin/env python3
"""B163 — Spanish + Greek wine regions: Rueda DO, Txakoli DO, Jerez DO, Santorini PDO, Nemea PDO"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
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
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, country, beverage_family, designation_type, designation_name,
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

# === RUEDA DO ===
print("=== Rueda DO ===")
r1 = R("Rueda DO", "Spain", "wine",
       designation_type="DO",
       designation_name="Denominación de Origen Rueda",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Spain's premier white wine DO, Rueda on the Castilian plateau produces bright, aromatic Verdejo wines of increasing quality and seriousness. The high-altitude vineyards (700–900m) and extreme continental climate yield Verdejo with distinctive herbal, citrus, and mineral character. Once known for oxidative whites, Rueda now leads Spain's white wine renaissance with fresh, vibrant modern styles.",
       key_producers="Belondrade y Lurton, Ossian, Bodegas Shaya, Marques de Riscal Rueda",
       historical_context="Rueda was granted DO status in 1980 and has since undergone a transformation from producing fortified oxidative wines to the fresh, aromatic Verdejo-based whites now exported worldwide.")
for yr, qd, pt, sn in [
    (2019,"excellent","stable","A fine vintage in Rueda with textbook Verdejo aromatics and crisp acidity."),
    (2020,"very_good","stable","Good ripeness with retained freshness; reliable quality across the DO."),
    (2021,"excellent","rising","Widely praised vintage for aromatic intensity and natural acidity in Verdejo."),
    (2022,"very_good","stable","Warm year; wines showing richer fruit while retaining Rueda's characteristic herbal notes."),
    (2023,"excellent","rising","Exceptional vintage with ideal conditions producing vibrant, age-worthy Verdejo."),
]:
    VIN(r1, yr, qd, pt, sn)

p1 = P("Belondrade y Lurton", "winery", r1, "Spain",
       production_philosophy="terroir_expression",
       philosophy_description="French-Spanish partnership producing Rueda's most prestigious Verdejo, barrel-fermented and aged on lees for complexity beyond the typical fresh style. A benchmark for serious Rueda white wine.",
       reputation_narrative="Belondrade y Lurton's flagship Verdejo is Spain's most celebrated white wine from the plateau — rich, complex, and demonstrating that Verdejo can rival Burgundy's finest whites in structure and longevity.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Belondrade y Lurton Rueda Verdejo", "wine_still", p1, r1, "Spain",
                    subcategory="white", description="Barrel-fermented single-vineyard Verdejo from Rueda, aged 6 months on fine lees. Rich stone fruit, fennel, citrus blossom, almond, and a mineral backbone — Spain's most serious Verdejo.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled lobster with lemon butter sauce", "complement", "classic", "main", "The wine's richness and mineral acidity complement lobster's sweetness; barrel-fermented complexity adds depth.")
    PAIR(prod, "White asparagus with hollandaise and smoked salmon", "complement", "established", "starter", "Herbal Verdejo notes mirror asparagus's vegetal character; acidity cuts through hollandaise richness.")
    PAIR(prod, "Roasted sea bass with fennel and saffron", "complement", "classic", "main", "Fennel notes in the wine mirror the roasted fennel; saffron's mineral depth echoes Verdejo's terroir.")
    PAIR(prod, "Manchego aged 6 months with membrillo", "bridge", "established", "cheese", "Almond notes in the wine bridge to manchego's nuttiness; membrillo sweetness contrasts the wine's herbal freshness.")

p2 = P("Ossian Bodegas", "winery", r1, "Spain",
       production_philosophy="minimal_intervention",
       philosophy_description="Ossian produces Verdejo from pre-phylloxera old vines using minimal intervention, natural fermentation, and extended lees contact. These pre-phylloxera roots, some over 150 years old, produce Verdejo of extraordinary concentration and complexity.",
       reputation_narrative="Ossian's old-vine Verdejo from ungrafted pre-phylloxera roots represents the pinnacle of what this grape can achieve, with wines of remarkable concentration, freshness, and longevity.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Ossian Verdejo Rueda", "wine_still", p2, r1, "Spain",
                    subcategory="white", description="Pre-phylloxera old-vine Verdejo, naturally fermented and aged on lees. Extraordinary concentration — peach, anise, fennel, citrus zest, and a volcanic-mineral backbone unparalleled in Spanish white wine.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Whole-roasted turbot with herb butter", "complement", "classic", "main", "The wine's intensity matches turbot's richness; herbal complexity bridges to the butter sauce perfectly.")
    PAIR(prod, "Cured ibérico ham with melon", "complement", "adventurous", "starter", "Old-vine Verdejo's mineral depth and anise notes complement ibérico's nutty, savoury richness.")
    PAIR(prod, "Seared foie gras with quince reduction", "contrast", "adventurous", "starter", "The wine's acidity cuts through foie's fat; anise and mineral notes create an unexpected but compelling bridge.")
    PAIR(prod, "Aged Idiazabal cheese with walnuts", "complement", "established", "cheese", "Smoky Idiazabal mirrors the wine's mineral depth; walnut bitterness balances old-vine Verdejo's richness.")

# === TXAKOLI DO ===
print("=== Txakoli DO ===")
r2 = R("Txakoli DO", "Spain", "wine",
       designation_type="DO",
       designation_name="Getariako Txakolina DO",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Txakoli (Chacoli) from the Basque Country of northern Spain is one of Europe's most distinctive wine styles — bone dry, high acid, low alcohol, lightly petillant whites from the Hondarrabi Zuri grape. The wines are traditionally poured with great ceremony from a height to aerate and create natural froth. From Atlantic coastal vineyards, they are the perfect partner for Basque pintxos.",
       key_producers="Txomin Etxaniz, Ameztoi, Hiruzta, Zapiain",
       historical_context="Txakoli has been produced in the Basque Country for centuries, with Getaria the most prestigious of the three DOs (also including Bizkaia and Álava). The wines nearly disappeared in the 20th century but experienced a revival as Basque cuisine rose to global prominence.")
for yr, qd, pt, sn in [
    (2020,"very_good","stable","A successful vintage for Txakoli with excellent freshness and mineral character."),
    (2021,"excellent","rising","Outstanding year — textbook Txakoli acidity with unusual aromatic intensity."),
    (2022,"good","stable","Warm year challenged acidity retention; careful winemaking preserved the style."),
    (2023,"very_good","stable","Fresh Atlantic conditions produced crisp, vibrant Txakoli of classic character."),
    (2024,"excellent","rising","Exceptional vintage for Hondarrabi Zuri — mineral, racy, and aromatic."),
]:
    VIN(r2, yr, qd, pt, sn)

p3 = P("Txomin Etxaniz", "winery", r2, "Spain",
       production_philosophy="terroir_expression",
       philosophy_description="The benchmark producer of Getariako Txakolina, Txomin Etxaniz has defined the style of great Txakoli for decades. Coastal Atlantic vineyards produce Hondarrabi Zuri of exceptional mineral freshness and natural effervescence.",
       reputation_narrative="Txomin Etxaniz is the reference producer for Basque Txakoli — their wines embody the style: racy, saline, petillant, and inseparable from the Basque pintxo culture that has conquered the world's restaurant scene.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Txomin Etxaniz Getariako Txakolina", "wine_still", p3, r2, "Spain",
                    subcategory="white", description="Classic Getariako Txakolina from coastal Atlantic vineyards. Bone dry, pétillant, with lime zest, green apple, sea spray, and a bracing mineral acidity. Low alcohol (10.5%) makes it supremely food-friendly.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Pintxos — anchovy and olive on bread", "complement", "classic", "amuse", "The quintessential Basque pairing — Txakoli's salinity and acidity are the perfect foil for anchovy's intensity and olive's richness.")
    PAIR(prod, "Grilled baby squid with olive oil and parsley", "complement", "classic", "starter", "The wine's sea-spray mineral character mirrors the squid's brininess; acidity cuts through olive oil.")
    PAIR(prod, "Razor clams with garlic and white wine", "complement", "classic", "starter", "One of the great matches in Basque cuisine — Txakoli's salinity and low alcohol mirror razor clams' delicate sweetness.")
    PAIR(prod, "Grilled white asparagus with romesco", "complement", "established", "starter", "The wine's green apple and mineral notes lift asparagus's vegetality; romesco's nuttiness bridges the pairing.")

p4 = P("Ameztoi Txakoli", "winery", r2, "Spain",
       production_philosophy="terroir_expression",
       philosophy_description="A leading Txakoli producer from Getaria, Ameztoi produces both classic still Txakoli and an acclaimed rosado (rosé) from Hondarrabi Beltza that has brought international attention to the DO.",
       reputation_narrative="Ameztoi's rosado Rubentis has become the most celebrated Txakoli wine internationally, introducing the style to a new generation of wine lovers while the estate's classic white remains a Basque benchmark.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Ameztoi Rubentis Txakoli Rosado", "wine_still", p4, r2, "Spain",
                    subcategory="rose", description="Pale copper rosé from Hondarrabi Beltza with classic Txakoli pétillance — strawberry, citrus, sea spray, and a dry, saline finish. One of Europe's most distinctive rosés.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Grilled prawns with sea salt and lemon", "complement", "classic", "starter", "The rosé's salinity and bright acidity mirror prawn sweetness; sea spray notes echo the sea.")
    PAIR(prod, "Tuna tataki with ponzu and sesame", "complement", "established", "starter", "Txakoli's bright acidity mirrors ponzu's citrus; the wine's bubbles cleanse sesame richness.")
    PAIR(prod, "Salt cod croquetas with aioli", "complement", "established", "amuse", "Classic Basque pintxo pairing — the wine's mineral acidity cuts through the fried croqueta's richness.")
    PAIR(prod, "Chilled gazpacho with cucumber and basil oil", "complement", "established", "starter", "The rosé's freshness and gentle effervescence mirror gazpacho's bright vegetal acidity.")

# === JEREZ DO (SHERRY) ===
print("=== Jerez DO ===")
r3 = R("Jerez DO", "Spain", "wine",
       designation_type="DO",
       designation_name="Denominación de Origen Jerez-Xérès-Sherry",
       reputation_tier="prestigious",
       quality_trajectory="rediscovering",
       description="Sherry, from the towns of Jerez de la Frontera, Sanlúcar de Barrameda, and El Puerto de Santa María in Andalusia, is one of the world's great wine styles — a diverse family of fortified wines ranging from bone-dry Fino and Manzanilla to rich, sweet Pedro Ximénez. Made via the complex solera system of fractional blending, Sherries offer extraordinary complexity. The albariza (chalk-white limestone) soils and Atlantic-influenced climate are the secret to Palomino Fino's brilliance.",
       key_producers="Equipo Navazos, Barbadillo, González Byass, Valdespino, Hidalgo La Gitana",
       historical_context="Sherry's history spans over 3,000 years, and it was England's most popular wine in Elizabethan times. After falling out of fashion, the finest Sherries are now experiencing a renaissance among sommeliers and food lovers who recognize their extraordinary food affinity and complexity.")
for yr, qd, pt, sn in [
    (2010,"exceptional","stable","A legendary Sherry vintage for single-harvest Amontillado and Oloroso releases."),
    (2015,"excellent","stable","Excellent year for Fino and Manzanilla freshness; great Palomino character."),
    (2018,"very_good","stable","Fine vintage producing bright, saline Manzanilla and structured Amontillado."),
    (2020,"very_good","rising","Atlantic conditions ideal for flor development — exceptional Fino and Manzanilla."),
    (2022,"excellent","rising","Outstanding vintage for premium Sherry categories across all styles."),
]:
    VIN(r3, yr, qd, pt, sn)

p5 = P("Equipo Navazos", "winery", r3, "Spain",
       production_philosophy="minimal_intervention",
       philosophy_description="Equipo Navazos is Sherry's most celebrated small-production producer, releasing limited quantities of single-cask, unfiltered Sherries from historic bodegas. These La Bota bottlings represent the pinnacle of what Sherry can be — raw, complex, and utterly compelling.",
       reputation_narrative="Equipo Navazos has single-handedly revived international interest in premium Sherry through their La Bota series. Their single-cask releases are among the most sought-after wines in Spain.",
       price_positioning="ultra_premium",
       authority_tier=1)
prod, is_new = PROD("Equipo Navazos La Bota de Manzanilla Pasada", "wine_still", p5, r3, "Spain",
                    subcategory="sherry_manzanilla", description="Single-cask Manzanilla Pasada from Sanlúcar de Barrameda — bone dry, saline, intensely complex. Fresh almonds, chamomile, Atlantic sea salt, and a yeasty, flor-influenced complexity that is unique in the wine world.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Jamón ibérico de bellota with pan con tomate", "complement", "classic", "starter", "The definitive Sherry pairing — Manzanilla's salinity and nuttiness mirror the acorn-fed jamón's extraordinary depth.")
    PAIR(prod, "Sushi and sashimi — especially fatty tuna", "complement", "adventurous", "main", "One of wine's great unexpected matches — Manzanilla's saline, umami-laden depth mirrors tuna's richness perfectly.")
    PAIR(prod, "Grilled langoustines with sea salt", "complement", "classic", "starter", "Sea salt and live yeast character in the wine mirror langoustine brininess; the match is sublime.")
    PAIR(prod, "Parmesan reggiano aged 36 months", "complement", "established", "cheese", "Flor yeast notes and almonds in the wine bridge to Parmesan's intense umami; a classic oxidative match.")
prod, is_new = PROD("Equipo Navazos La Bota de Amontillado", "wine_still", p5, r3, "Spain",
                    subcategory="sherry_amontillado", description="Single-cask Amontillado of extraordinary complexity — began life under flor as Fino then lost biological ageing to reveal oxidative depth. Hazelnut, dried fig, orange peel, leather, and a piercing, saline finish.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Chicken consommé with truffle", "complement", "classic", "starter", "Amontillado's nutty, oxidative complexity mirrors consommé's reduction depth; truffle bridges the savoury umami.")
    PAIR(prod, "Roasted almonds with smoked paprika and sea salt", "complement", "classic", "amuse", "Hazelnut and almond in the wine mirror the nuts themselves; smoked paprika echoes the wine's earthy depth.")
    PAIR(prod, "Oxtail braised in Sherry", "complement", "classic", "main", "A natural affinity — the wine is literally in the dish. Amontillado's nuttiness and richness deepen the braise.")
    PAIR(prod, "Aged Mahón or Comté with walnuts", "complement", "established", "cheese", "Oxidative complexity bridges to hard aged cheeses; walnut bitterness echoes the wine's nut-skin dryness.")

p6 = P("Hidalgo La Gitana", "winery", r3, "Spain",
       production_philosophy="traditional_methods",
       philosophy_description="One of Sanlúcar's most celebrated Manzanilla houses, Hidalgo has produced La Gitana — one of the world's most recognized Sherries — since 1792. Their vintage Manzanilla pasada and Amontillado releases are reference expressions of Sanlúcar's finest styles.",
       reputation_narrative="Hidalgo's La Gitana is the gateway Manzanilla that has introduced millions to dry Sherry. Their premium Pastrana and Napoleon releases represent Sanlúcar's finest expressions at the highest level.",
       price_positioning="mid_range",
       authority_tier=1)
prod, is_new = PROD("Hidalgo La Gitana Manzanilla", "wine_still", p6, r3, "Spain",
                    subcategory="sherry_manzanilla", description="The world's most recognized Manzanilla — pale straw, intensely saline, with chamomile, fresh almond, and brine. Light, dry, and endlessly refreshing from its Sanlúcar solera.", price_tier="mid_range")
if is_new:
    PAIR(prod, "Fried boquerones (fresh anchovies) with lemon", "complement", "classic", "starter", "The quintessential tapas pairing — Manzanilla's salinity mirrors the anchovies; acidity cuts through the fry.")
    PAIR(prod, "Clams with garlic and parsley — almejas a la marinera", "complement", "classic", "starter", "Briny clams and saline Manzanilla share the same Atlantic DNA; the match is pure Andalusian harmony.")
    PAIR(prod, "Salmorejo (thick Sevillian gazpacho) with jamon", "complement", "established", "starter", "The wine's dry freshness contrasts salmorejo's richness; jamón's salt echoes Manzanilla's saline core.")
    PAIR(prod, "Fried fish — pescaíto frito mix", "complement", "classic", "main", "A timeless Andalusian pairing — Manzanilla is made for fried fish; acidity cuts, salinity echoes the sea.")

# === SANTORINI PDO ===
print("=== Santorini PDO ===")
r4 = R("Santorini PDO", "Greece", "wine",
       designation_type="PDO",
       designation_name="Santorini Protected Designation of Origin",
       reputation_tier="prestigious",
       quality_trajectory="ascending",
       description="The volcanic island of Santorini produces one of the world's most distinctive white wines from the Assyrtiko grape — a variety uniquely adapted to the island's harsh, windswept conditions. Ancient vines (some over 200 years old) are trained in the traditional kouloura (basket) shape to protect from fierce winds. The black volcanic pumice soils, intense sunshine, and sea breezes produce Assyrtiko of extraordinary minerality, acidity, and concentration. The sweet Vinsanto, from sun-dried Assyrtiko and Aidani, is among Greece's greatest wines.",
       key_producers="Domaine Sigalas, Hatzidakis, Gavalas, Santo Wines, Domaine Argyros",
       historical_context="Santorini's viticulture dates back 3,500 years, with the Minoan civilization trading wine from the island. The phylloxera louse never reached the volcanic island, making Santorini one of the world's last refuges of ungrafted pre-phylloxera vines.")
for yr, qd, pt, sn in [
    (2018,"excellent","rising","A landmark vintage for Santorini Assyrtiko — concentrated, mineral, and age-worthy."),
    (2019,"very_good","stable","Good vintage with typical volcanic minerality and bright citrus-driven acidity."),
    (2020,"excellent","rising","Outstanding year producing wines of extraordinary depth and laser-like precision."),
    (2021,"very_good","stable","Fine conditions; Assyrtiko of classic style with saline mineral backbone."),
    (2022,"very_good","stable","Warm vintage; wines showing richer fruit while retaining volcanic minerality."),
    (2023,"excellent","rising","Exceptional vintage across all categories — especially noteworthy for barrel-fermented Assyrtiko."),
]:
    VIN(r4, yr, qd, pt, sn)

p7 = P("Domaine Sigalas", "winery", r4, "Greece",
       production_philosophy="terroir_expression",
       philosophy_description="Founded by Paris Sigalas, Domaine Sigalas is Santorini's most acclaimed producer, making both a fresh, precise estate Assyrtiko and a barrel-fermented version that demonstrates the grape's ability to rival great Burgundy whites. The estate's old-vine kouloura vines produce wines of extraordinary concentration.",
       reputation_narrative="Sigalas Santorini is the reference for modern Assyrtiko — the barrel-fermented Kavalieros has placed Santorini among the world's great white wine regions, demonstrating volcanic terroir's unique contribution to flavour.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Sigalas Santorini Assyrtiko", "wine_still", p7, r4, "Greece",
                    subcategory="white", description="Classic Santorini Assyrtiko from old-vine kouloura-trained vines on volcanic pumice. Laser-sharp acidity, citrus pith, sea salt, wet stone, and white peach — one of the Mediterranean's greatest white wines.", price_tier="premium")
if is_new:
    PAIR(prod, "Grilled whole sea bream with lemon and thyme", "complement", "classic", "main", "Volcanic minerality and citrus acidity complement the bream's delicate sweetness — a Greek island classic.")
    PAIR(prod, "Fresh oysters with lemon and mignonette", "complement", "classic", "amuse", "Saline, mineral Assyrtiko is the textbook match for briny oysters — both carry the essence of the sea.")
    PAIR(prod, "Taramasalata with warm pita bread", "complement", "established", "starter", "The wine's acidity cuts through the rich tarama; citrus notes brighten the smoky fish roe.")
    PAIR(prod, "Grilled octopus with olive oil and oregano", "complement", "classic", "main", "A Santorini classic — volcanic mineral Assyrtiko mirrors octopus's oceanic depth; olive oil bridges both.")
prod, is_new = PROD("Sigalas Barrel Assyrtiko Santorini", "wine_still", p7, r4, "Greece",
                    subcategory="white", description="Barrel-fermented Assyrtiko aged on lees — the 'Kavalieros' style. More complex, with stone fruit, toasted almond, beeswax, and an extraordinary volcanic mineral backbone. Ageable for 10+ years.", price_tier="ultra_premium")
if is_new:
    PAIR(prod, "Lobster with drawn butter and herbs", "complement", "classic", "main", "The barrel-fermented richness and volcanic depth match lobster's luxury; herbs echo the wine's complexity.")
    PAIR(prod, "Grilled swordfish with caper-lemon butter", "complement", "established", "main", "Meaty swordfish demands a richer white — the barrel Assyrtiko's texture and acidity are perfectly calibrated.")
    PAIR(prod, "Feta and watermelon salad with mint", "complement", "established", "starter", "A Cycladic summer pairing — wine's salinity echoes feta; citrus notes bridge the watermelon's sweetness.")
    PAIR(prod, "Aged graviera cheese with honey and walnuts", "bridge", "established", "cheese", "Greek graviera's nuttiness bridges to the wine's barrel notes; honey ties the volcanic mineral finish.")

# === NEMEA PDO ===
print("=== Nemea PDO ===")
r5 = R("Nemea PDO", "Greece", "wine",
       designation_type="PDO",
       designation_name="Nemea Protected Designation of Origin",
       reputation_tier="respected",
       quality_trajectory="ascending",
       description="Nemea in the northeastern Peloponnese is Greece's most important red wine region, producing wines exclusively from the Agiorgitiko ('St. George') grape. The region spans three distinct altitudinal zones, with the highest-altitude vineyards (600–800m) yielding the most structured, age-worthy wines. Agiorgitiko produces velvety, dark fruit-forward reds with good acidity, sometimes compared to Merlot but with a distinctly Greek character.",
       key_producers="Gaia Wines, Skouras, Domaine Spiropoulos, Palivou Estate",
       historical_context="Nemea has been producing wine since antiquity — the region is associated with the mythological lion slain by Hercules. The Agiorgitiko grape's name references Saint George, patron saint of the region.")
for yr, qd, pt, sn in [
    (2018,"very_good","stable","A fine Nemea vintage with ripe, velvety Agiorgitiko showing good structure."),
    (2019,"excellent","rising","Landmark vintage for Nemea — wines of exceptional concentration and freshness."),
    (2020,"very_good","stable","Good vintage; high-altitude vineyards particularly successful for structured reds."),
    (2021,"excellent","rising","Outstanding year producing age-worthy Agiorgitiko with impressive balance."),
    (2022,"very_good","stable","Warm vintage; generous, fruit-forward wines with soft tannins for earlier drinking."),
    (2023,"excellent","rising","Exceptional conditions produced Nemea's finest high-altitude wines in a decade."),
]:
    VIN(r5, yr, qd, pt, sn)

p8 = P("Gaia Wines Nemea", "winery", r5, "Greece",
       production_philosophy="terroir_expression",
       philosophy_description="Gaia Wines produces benchmark Agiorgitiko from Nemea's high-altitude Koutsi vineyard, alongside celebrated Assyrtiko from Santorini. Yiannis Paraskevopoulos's approach focuses on expressing Greek terroir at the highest level.",
       reputation_narrative="Gaia's Estate Agiorgitiko from Koutsi is one of Greece's most acclaimed red wines, demonstrating that Nemea can produce age-worthy, internationally competitive reds from this indigenous variety.",
       price_positioning="premium",
       authority_tier=1)
prod, is_new = PROD("Gaia Estate Agiorgitiko Nemea", "wine_still", p8, r5, "Greece",
                    subcategory="red", description="High-altitude Koutsi vineyard Agiorgitiko — deep violet, plum, blackberry, violet, dark spice, and smooth tannins. One of Greece's finest reds, structured for ageing 10+ years.", price_tier="premium")
if is_new:
    PAIR(prod, "Roasted leg of lamb with lemon, garlic and oregano", "complement", "classic", "main", "The definitive Greek red meat pairing — Agiorgitiko's dark fruit and smooth tannins complement lamb's richness; oregano bridges the wine's herbal notes.")
    PAIR(prod, "Moussaka with bechamel", "complement", "classic", "main", "Velvety Agiorgitiko tannins cut through bechamel's richness; spiced meat echoes the wine's dark fruit depth.")
    PAIR(prod, "Grilled pork souvlaki with tzatziki", "complement", "established", "main", "Smooth tannins complement grilled pork; tzatziki's brightness and garlic mirror the wine's herbal dimension.")
    PAIR(prod, "Aged kefalotiri cheese with olive oil", "complement", "established", "cheese", "Hard Greek cheese's saltiness and sharpness are softened by Agiorgitiko's fruit; olive oil bridges the minerality.")
prod, is_new = PROD("Gaia Notios Red Peloponnese", "wine_still", p8, r5, "Greece",
                    subcategory="red", description="Accessible Agiorgitiko blend from the Peloponnese — ripe plum, cherry, soft spice, and silky tannins. Fresh and food-friendly with the classic Nemea character at an everyday price.", price_tier="value")
if is_new:
    PAIR(prod, "Lamb kebabs with pita and tzatziki", "complement", "classic", "main", "A classic Greek taverna pairing — smooth Agiorgitiko fruit complements spiced lamb; tzatziki's acidity freshens.")
    PAIR(prod, "Grilled chicken with lemon and herbs", "complement", "established", "main", "Lighter-bodied Agiorgitiko pairs beautifully with grilled poultry; lemon echoes the wine's bright fruit.")
    PAIR(prod, "Spanakopita (spinach and feta pie)", "complement", "established", "starter", "The wine's soft tannins and fruit complement the feta's saltiness and the pastry's richness.")
    PAIR(prod, "Dolmades with avgolemono sauce", "complement", "established", "starter", "Rice-stuffed grape leaves with citrus-egg sauce mirror the wine's fresh, herbal character.")

# === DB STATE ===
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
print("B163 complete.")
cur.close()
conn.close()
