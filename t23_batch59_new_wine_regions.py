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

def P(name, country, region_id, producer_type="winery", description=None):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  Producer exists: {name} ({row[0]})")
        return row[0]
    cur.execute("""INSERT INTO beverage_producers
        (name, country, region_id, producer_type, reputation_narrative, authority_tier)
        VALUES (%s,%s,%s,%s,%s,1) RETURNING id""",
        (name, country, region_id, producer_type, description))
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

# ── REGION 1: Greco di Tufo DOCG (Italy/Campania) ──────────────────────────
print("\n=== Region 1: Greco di Tufo ===")
r1 = R("Greco di Tufo", "Italy", "wine",
    designation_type="DOCG", designation_name="Greco di Tufo DOCG",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Greco di Tufo is one of Campania's premier white wine DOCGs, produced from the ancient Greco grape on volcanic tuff soils around the village of Tufo. The wines are characterised by mineral precision, smoky complexity, stone fruit, and a distinctive saline finish — a direct expression of the volcanic terroir.",
    key_producers="Feudi di San Gregorio, Terredora di Paolo, Benito Ferrara, Mastroberardino",
    historical_context="The Greco grape was brought to Campania by ancient Greeks and has been cultivated around Tufo for over 2,000 years. The DOCG was established in 1992. The unique tuff (tufo) volcanic soil — a yellowish limestone formed from volcanic ash — is central to the wine's mineral character.")

VIN(r1, 2023, "very_good", "stable", "Excellent aromatic freshness; volcanic mineral character well expressed with good stone fruit depth")
VIN(r1, 2022, "excellent", "rising", "Outstanding Campanian vintage; full, mineral Greco with remarkable concentration and length")
VIN(r1, 2021, "good", "stable", "Cooler year producing leaner, more austere style with excellent mineral definition")
VIN(r1, 2020, "excellent", "rising", "Powerful vintage; rich and concentrated with volcanic mineral intensity and impressive depth")
VIN(r1, 2019, "very_good", "stable", "Classic Greco expression with fine balance between stone fruit richness and mineral acidity")

prod1a_id = P("Feudi di San Gregorio", "Italy", r1, "winery",
    "The flagship producer of Campanian viticulture; Feudi di San Gregorio has elevated the entire region's reputation with benchmark Greco di Tufo, Fiano di Avellino, and Aglianico from the Irpinia hills.")
prod1a, new1a = PROD("Feudi di San Gregorio Greco di Tufo", "wine_still", prod1a_id, r1, "Italy",
    subcategory="white", price_tier="mid_range",
    description="The benchmark entry to Greco di Tufo: mineral, savoury white with smoky volcanic notes, white peach, and almond. Crisp acidity and a distinctive saline finish from the tuff soils. The reference wine for the DOCG.")
if new1a:
    PAIR(prod1a, "Grilled swordfish with capers, olives, and lemon", "complement", "classic", "fish_course",
        "Mediterranean fish and Greco is the Campanian classic; capers amplify mineral salinity while lemon mirrors the wine's bright acidity")
    PAIR(prod1a, "Burrata with roasted cherry tomatoes and basil", "complement", "classic", "starter",
        "Campanian pairing: fresh dairy richness is refreshed by Greco's acidity; tomato sweetness meets the wine's stone fruit")
    PAIR(prod1a, "Pasta alle vongole with white wine and parsley", "complement", "classic", "main",
        "Clam's brine and sea salinity amplifies Greco's mineral-saline character; volcanic soil expression and ocean converge")
    PAIR(prod1a, "Grilled octopus with nduja oil and pickled fennel", "complement", "established", "starter",
        "Octopus's char and nduja spice meets Greco's smoky mineral complexity; fennel acidity provides a cleansing counterpoint")

prod1b_id = P("Benito Ferrara", "Italy", r1, "winery",
    "A small, highly regarded family estate in Tufo; Gabriella Ferrara produces single-vineyard Greco di Tufo of exceptional mineral precision and terroir authenticity from old vines grown on the volcanic tuff soils.")
prod1b, new1b = PROD("Ferrara Greco di Tufo Vigna Cicogna", "wine_still", prod1b_id, r1, "Italy",
    subcategory="white", price_tier="premium",
    description="Single-vineyard Greco di Tufo from Vigna Cicogna: old vines on pure tuff soil producing intense mineral complexity, white smoke, and stone fruit with extraordinary saline length. A benchmark for volcanic terroir expression.")
if new1b:
    PAIR(prod1b, "Risotto ai frutti di mare with saffron and bottarga", "complement", "established", "main",
        "Seafood risotto with bottarga's umami saline depth mirrors Greco's volcanic mineral character; saffron amplifies exotic spice")
    PAIR(prod1b, "Neapolitan pizza margherita DOC with buffalo mozzarella", "complement", "classic", "casual",
        "The Campanian pairing: regional pizza and Greco share volcanic soil heritage; buffalo mozzarella richness is refreshed by Greco's acidity")
    PAIR(prod1b, "Zuppa di cozze (mussel soup) with chilli and garlic", "complement", "classic", "fish_course",
        "Mussel brine and garlic are natural partners for Greco's saline mineral precision; chilli heat is tamed by the wine's body")
    PAIR(prod1b, "Sfogliatella with ricotta and candied citrus peel", "contrast", "adventurous", "dessert",
        "Neapolitan pastry sweetness contrasts Greco's mineral dryness; the citrus peel creates aromatic bridge to the wine's freshness")

# ── REGION 2: Fiano di Avellino DOCG (Italy/Campania) ──────────────────────
print("\n=== Region 2: Fiano di Avellino ===")
r2 = R("Fiano di Avellino", "Italy", "wine",
    designation_type="DOCG", designation_name="Fiano di Avellino DOCG",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Fiano di Avellino is widely regarded as Campania's greatest white wine DOCG, produced from the ancient Fiano grape on limestone and volcanic soils in the Irpinia hills. The wines show hazelnut, honey, white flowers, and mineral depth, gaining extraordinary complexity with age — unusual for southern Italian whites.",
    key_producers="Mastroberardino, Feudi di San Gregorio, Ciro Picariello, Villa Diamante",
    historical_context="The Fiano grape was documented by Pliny the Elder and prized for making wine enjoyed by ancient Romans. Nearly extinct by the mid-20th century, it was revived by Mastroberardino in the 1970s. The DOCG was established in 2003. Fiano has since become a reference point for fine Italian white wine.")

VIN(r2, 2023, "excellent", "rising", "Outstanding aromatic complexity; hazelnut and white flower character beautifully expressed with fine acidity")
VIN(r2, 2022, "very_good", "stable", "Rich and full vintage with excellent Fiano depth; honey and stone fruit notes well developed")
VIN(r2, 2021, "good", "stable", "Elegant, restrained year with crisp acidity and defined mineral character; good aging potential")
VIN(r2, 2020, "exceptional", "rising", "Benchmark Irpinia vintage; extraordinary Fiano with hazelnut complexity, mineral depth, and rare aging potential")
VIN(r2, 2019, "very_good", "stable", "Classic Fiano expression; textbook hazelnut, honey, and white flower with saline minerality")

prod2a_id = P("Mastroberardino", "Italy", r2, "winery",
    "The historic guardian of Campanian heritage varieties; Mastroberardino single-handedly preserved Fiano, Greco, and Aglianico when they were near extinction. Their Fiano di Avellino Radici is the historic benchmark for the DOCG.")
prod2a, new2a = PROD("Mastroberardino Fiano di Avellino Radici", "wine_still", prod2a_id, r2, "Italy",
    subcategory="white", price_tier="premium",
    description="The historic benchmark: Mastroberardino's Radici Fiano from Irpinia's finest sites. Hazelnut, white flowers, honey, and remarkable mineral depth on volcanic limestone soils. Gains complexity for 10-15 years in bottle — exceptional for a southern Italian white.")
if new2a:
    PAIR(prod2a, "Linguine with sea urchin, bottarga, and extra virgin olive oil", "complement", "classic", "fish_course",
        "Sea urchin's intense marine sweetness and iodine depth are amplified by Fiano's mineral salinity and hazelnut richness")
    PAIR(prod2a, "Roasted langoustine with nduja butter and sea herbs", "complement", "established", "fish_course",
        "Crustacean sweetness meets Fiano's honeyed depth; nduja spice adds a Campanian dimension to the wine's mineral framework")
    PAIR(prod2a, "Aged Provolone del Monaco with acacia honey", "bridge", "classic", "cheese",
        "Semi-hard Campanian cheese with honey bridges Fiano's hazelnut-honey character; a regional pairing of genuine authenticity")
    PAIR(prod2a, "Vitello tonnato with capers and anchovies", "complement", "established", "starter",
        "The northern Italian classic works beautifully with Fiano's savoury mineral depth; tonnato's umami amplifies the wine's complexity")

prod2b_id = P("Ciro Picariello", "Italy", r2, "winery",
    "Artisan producer making some of Avellino's most precise, terroir-focused Fiano; Ciro Picariello's small-production wines from old vines achieve extraordinary complexity with minimal intervention and genuine volcanic soil expression.")
prod2b, new2b = PROD("Picariello Fiano di Avellino 906", "wine_still", prod2b_id, r2, "Italy",
    subcategory="white", price_tier="premium",
    description="Picariello's single-vineyard Fiano named for its altitude (906 metres); minimal intervention, long skin contact produces extraordinary mineral tension, saline length, and hazelnut depth. Gaining cult status among Italian wine enthusiasts.")
if new2b:
    PAIR(prod2b, "Pasta e fagioli with clams and wild fennel", "complement", "classic", "main",
        "Rustic Campanian bean and clam pasta meets Fiano's savoury mineral depth; wild fennel creates aromatic harmony with the wine's floral notes")
    PAIR(prod2b, "Grilled whole sea bream with lemon, caper, and herb", "complement", "classic", "fish_course",
        "Sea bream's delicate white flesh and marine freshness echo Fiano's mineral-saline structure; a perfect Campanian seaside pairing")
    PAIR(prod2b, "Truffle arancini with fontina and black truffle", "complement", "adventurous", "starter",
        "Truffle's earthy depth meets Fiano's hazelnut character — both share an autumnal, forest floor quality that creates resonance")
    PAIR(prod2b, "White asparagus with hollandaise and shaved bottarga", "complement", "established", "starter",
        "Asparagus's vegetal bitterness and hollandaise richness are balanced by Fiano's acidity; bottarga adds marine salinity to echo the wine's minerality")

# ── REGION 3: Picpoul de Pinet AOP (France/Languedoc) ──────────────────────
print("\n=== Region 3: Picpoul de Pinet ===")
r3 = R("Picpoul de Pinet", "France", "wine",
    designation_type="AOP", designation_name="Picpoul de Pinet AOP",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Picpoul de Pinet produces France's most distinctive coastal white from the indigenous Picpoul Blanc grape on limestone soils near the Étang de Thau oyster lagoon in the Languedoc. The wines are defined by electric acidity, citrus freshness, and saline minerality — purpose-built for oysters and Mediterranean seafood.",
    key_producers="Château de Pinet, Domaine Félines Jourdan, Mas de Bellone, Cave Coopérative de Pinet",
    historical_context="Picpoul — meaning 'lip-stinger' in Occitan — has been cultivated around Pinet since at least the 17th century. The wine was historically consumed by oyster farmers on the Étang de Thau. The AOP (then AOC) was granted in 1985, elevating a local staple to regional recognition.")

VIN(r3, 2023, "excellent", "stable", "Bright and vibrant vintage; exceptional citrus freshness and saline expression from the lagoon terroir")
VIN(r3, 2022, "very_good", "stable", "Good balance between freshness and texture; richer style without losing the defining acidity")
VIN(r3, 2021, "good", "stable", "Cooler year with excellent acidity; classic Picpoul character — lean, fresh, and mineral")
VIN(r3, 2020, "very_good", "stable", "Warm year; slightly fuller body with excellent Picpoul citrus character; good balance maintained")
VIN(r3, 2019, "excellent", "stable", "Benchmark vintage; textbook lip-stinging acidity and salinity with fine lemon-lime precision")

prod3a_id = P("Domaine Félines Jourdan", "France", r3, "winery",
    "The most internationally recognised Picpoul de Pinet producer; Claude Jourdan's estate bottles the definitive expression of the appellation — pure, saline, and refreshing — exported globally and synonymous with the style.")
prod3a, new3a = PROD("Félines Jourdan Picpoul de Pinet", "wine_still", prod3a_id, r3, "France",
    subcategory="white", price_tier="mid_range",
    description="The benchmark Picpoul de Pinet: crisp, citrus-driven, and minerally saline. Electric acidity with lemon, green apple, and subtle white flower notes. The definitive apéritif and oyster wine of the Languedoc coast.")
if new3a:
    PAIR(prod3a, "Freshly shucked Étang de Thau flat oysters with mignonette", "complement", "classic", "aperitif",
        "The defining pairing: oysters from the same lagoon as the wine; saline match and citrus acidity cut through the oyster's brine")
    PAIR(prod3a, "Grilled sea bass with rouille and Mediterranean vegetables", "complement", "classic", "fish_course",
        "Sea bass's delicate white flesh is refreshed by Picpoul's electric acidity; rouille's richness is balanced by the wine's citrus precision")
    PAIR(prod3a, "Moules marinières with white wine, shallot, and parsley", "complement", "classic", "starter",
        "Mussel brine amplifies Picpoul's salinity; the same white wine used in cooking creates seamless continuity")
    PAIR(prod3a, "Tapenade and anchovy crostini with marinated olives", "complement", "established", "aperitif",
        "Southern French apéritif classics — salty, savoury, olive-forward — are the natural vehicle for Picpoul's refreshing acidity")

prod3b_id = P("Château de Pinet", "France", r3, "winery",
    "One of Picpoul de Pinet's most historic estates; Château de Pinet produces mineral, elegant Picpoul from limestone soils near the lagoon, emphasising the appellation's freshness and citrus-saline identity.")
prod3b, new3b = PROD("Château de Pinet Picpoul de Pinet", "wine_still", prod3b_id, r3, "France",
    subcategory="white", price_tier="value",
    description="Classic Picpoul from the historic Château de Pinet estate; bright lemon, green apple, and saline mineral precision. Unoaked, fresh, and immediate — the archetypal expression of this coastal appellation at accessible price.")
if new3b:
    PAIR(prod3b, "Bouillabaisse with rouille-topped croutons and Gruyère", "complement", "established", "main",
        "Provence's iconic seafood stew is amplified by Picpoul's fresh acidity; rouille's richness needs the wine's bite to balance")
    PAIR(prod3b, "Grilled prawns with garlic butter, chilli, and lemon", "complement", "classic", "starter",
        "Prawn sweetness and garlic butter are refreshed by Picpoul's acidity; lemon in the dish mirrors the wine's citrus precision")
    PAIR(prod3b, "Salade niçoise with good-quality tuna, eggs, and olives", "complement", "classic", "casual",
        "The quintessential French coastal salad with Picpoul is a Languedoc staple; olive salinity and tuna umami elevate the wine's freshness")
    PAIR(prod3b, "Ceviche with lime, red onion, coriander, and jalapeño", "complement", "established", "starter",
        "Picpoul's citrus acidity mirrors ceviche's lime marinade; the wine's salinity bridges to the fresh seafood")

# ── REGION 4: Etna DOC (Italy/Sicily) ──────────────────────────────────────
print("\n=== Region 4: Etna DOC ===")
r4 = R("Etna", "Italy", "wine",
    designation_type="DOC", designation_name="Etna DOC",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Etna is one of the world's most dramatic wine regions, producing wines from high-altitude volcanic slopes of the active Mount Etna in Sicily. Nerello Mascalese dominates the reds — elegant, high-acid wines of haunting complexity and Burgundian-like precision. Carricante whites show extraordinary mineral purity. The altitude (600-1000m) gives freshness impossible at lower Sicilian elevations.",
    key_producers="Benanti, Cornelissen, Passopisciaro, Terre Nere, Calabretta",
    historical_context="Wine production on Etna dates to antiquity but the modern reputation began with Andrea Benanti in the 1980s. International attention arrived in the 2000s with producers like Frank Cornelissen and Marco de Grazia (Terre Nere). The volcanic soils, pre-phylloxera old vines (some 100+ years), and elevation create conditions unlike anywhere else in Italy.")

VIN(r4, 2023, "very_good", "rising", "Excellent vintage on Etna; ideal growing season with volcanic mineral intensity and freshness preserved")
VIN(r4, 2022, "excellent", "rising", "Outstanding Etna year; concentrated Nerello Mascalese with remarkable depth and Burgundian elegance")
VIN(r4, 2021, "good", "stable", "Cooler year with elegant, lighter Nerello; excellent acidity and mineral definition but less concentration")
VIN(r4, 2020, "very_good", "rising", "Strong vintage with good ripeness; volcanic mineral character prominent with dense but refined tannins")
VIN(r4, 2019, "excellent", "rising", "Benchmark Etna vintage; complex, age-worthy Nerello Mascalese with extraordinary mineral precision and length")

prod4a_id = P("Terre Nere", "Italy", r4, "winery",
    "Marco de Grazia's pioneering estate credited with bringing Etna to international attention; Terre Nere crafts single-contrada Nerello Mascalese from pre-phylloxera old vines that showcase the volcanic terroir with Burgundian precision.")
prod4a, new4a = PROD("Terre Nere Etna Rosso", "wine_still", prod4a_id, r4, "Italy",
    subcategory="red", price_tier="premium",
    description="Terre Nere's estate Etna Rosso: Nerello Mascalese from multiple high-altitude contrade, blended to show Etna's volcanic character. Red cherry, ash, dried herbs, and extraordinary mineral length. Elegant and age-worthy — the accessible introduction to the estate.")
if new4a:
    PAIR(prod4a, "Roasted rabbit with wild herbs, capers, and tomatoes alla siciliana", "complement", "classic", "main",
        "Sicilian rabbit's lean, herby richness meets Nerello's elegance; capers add briny depth to echo the volcanic mineral note")
    PAIR(prod4a, "Pasta alla Norma with aubergine, ricotta salata, and basil", "complement", "classic", "main",
        "Sicily's iconic pasta — aubergine's smoky richness and ricotta salata's salinity match Nerello's volcanic mineral expression")
    PAIR(prod4a, "Grilled tuna with olive oil, oregano, and caponata", "complement", "established", "fish_course",
        "Tuna's firm red flesh and Sicilian caponata's sweet-sour balance mirror Nerello's acidity and red fruit character")
    PAIR(prod4a, "Aged Ragusano with honey and toasted almonds", "bridge", "established", "cheese",
        "Sicilian hard cheese with sweet accompaniment bridges Nerello's tannin and mineral acidity; almonds echo the volcanic ash note")

prod4b_id = P("Benanti", "Italy", r4, "winery",
    "The pioneer of modern Etna wine; Giuseppe Benanti's estate established the benchmark for high-altitude Nerello Mascalese and Carricante in the 1980s, proving Etna's potential for world-class wine from pre-phylloxera old vines.")
prod4b, new4b = PROD("Benanti Etna Rosso Rovittello", "wine_still", prod4b_id, r4, "Italy",
    subcategory="red", price_tier="premium",
    description="Benanti's single-contrada Nerello Mascalese from Rovittello on Etna's north face; complex and age-worthy with volcanic minerality, red cherry, ash, and dried rose petal. One of Etna's original benchmark bottlings.")
if new4b:
    PAIR(prod4b, "Pigeon breast with black olive crust and beet gastrique", "complement", "established", "main",
        "Game bird's delicacy and iron notes match Nerello's elegant red fruit and minerality; olive adds Sicilian savouriness")
    PAIR(prod4b, "Sarde a beccafico with pine nuts, raisins, and saffron", "complement", "classic", "fish_course",
        "This Sicilian sweet-sour sardine preparation's agrodolce character is a natural match for Nerello's lively acidity and mineral depth")
    PAIR(prod4b, "Slow-roasted pork shoulder with Sicilian herbs and orange", "complement", "established", "main",
        "Pork's fat richness is cut by Nerello's bright acidity; orange zest amplifies the wine's red fruit and adds aromatic lift")
    PAIR(prod4b, "Caponata with aubergine, celery, capers, and dark chocolate", "bridge", "adventurous", "starter",
        "Etna's volcanic complexity mirrors caponata's agrodolce layers; dark chocolate adds a bitter bridge to Nerello's mineral depth")

# ── REGION 5: Gaillac AOC (France/Southwest) ───────────────────────────────
print("\n=== Region 5: Gaillac ===")
r5 = R("Gaillac", "France", "wine",
    designation_type="AOC", designation_name="Gaillac AOC",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Gaillac is one of France's oldest wine regions, producing a diverse range of styles from indigenous varieties rarely found elsewhere — Mauzac, Len de l'El, Ondenc for whites; Duras, Fer Servadou (Braucol), and Prunelard for reds. The diversity is remarkable: dry, sparkling, off-dry, and sweet whites; fresh reds; and the unique perlé style. A stronghold of native biodiversity.",
    key_producers="Domaine Plageoles, Château Clément Termes, Domaine Rotier, Labastide de Levis",
    historical_context="Gaillac has been producing wine since Roman times and possibly before, with documentation dating to the 1st century AD. The region was significant in medieval trade, its wines shipped along the Tarn River to Bordeaux. The revival of indigenous varieties by producers like Robert and Bernard Plageoles from the 1970s onward has repositioned Gaillac as a reference for French wine biodiversity.")

VIN(r5, 2023, "very_good", "stable", "Excellent year for both indigenous whites and reds; good ripeness with balanced acidity across varieties")
VIN(r5, 2022, "excellent", "rising", "Outstanding Gaillac vintage; intense and concentrated with fine expression of indigenous character")
VIN(r5, 2021, "good", "stable", "Cooler year suited to the fresher white styles; elegant, aromatic Mauzac and perlé with great tension")
VIN(r5, 2020, "excellent", "rising", "Hot year producing powerful reds and rich sweet whites; Ondenc sweet wines of remarkable depth")
VIN(r5, 2019, "very_good", "stable", "Classic Gaillac vintage with good varietal typicity across the range; reds and dry whites well balanced")

prod5a_id = P("Domaine Plageoles", "France", r5, "winery",
    "The guardian of Gaillac's indigenous variety heritage; Robert and Bernard Plageoles spent decades reviving near-extinct grapes like Ondenc, Verdanel, and Prunelard — their work is fundamental to French wine biodiversity and the recovery of Gaillac's historic identity.")
prod5a, new5a = PROD("Plageoles Mauzac Nature", "wine_sparkling", prod5a_id, r5, "France",
    subcategory="sparkling_white", price_tier="mid_range",
    description="Domaine Plageoles' iconic ancestral-method sparkling Mauzac — the original Gaillac pétillant style predating Champagne's méthode. Gentle perlé bubbles, apple and quince character, slight sweetness from residual sugar, low alcohol. Utterly unique.")
if new5a:
    PAIR(prod5a, "Oysters with apple mignonette and chive", "complement", "established", "aperitif",
        "The gentle bubbles and apple character mirror oyster brine; a more rustic, authentic alternative to Champagne for oyster service")
    PAIR(prod5a, "Rillettes de canard with cornichons on country bread", "complement", "established", "starter",
        "Duck rillettes' richness is refreshed by Mauzac's apple freshness and light effervescence; classic Southwest aperitif pairing")
    PAIR(prod5a, "Apple tarte fine with crème fraîche and calvados", "complement", "adventurous", "dessert",
        "Apple flavour echo between wine and dessert; the slight sweetness of ancestral-method Mauzac integrates with caramelised fruit")
    PAIR(prod5a, "Cassoulet toulousain with confit duck and Toulouse sausage", "cleanse", "established", "main",
        "The effervescence and freshness of Mauzac Nature cleanse the rich fat of cassoulet; a regional pairing rarely seen but highly effective")

prod5b_id = P("Domaine Rotier", "France", r5, "winery",
    "A leading Gaillac estate producing serious, terroir-driven wines from both indigenous and international varieties; Alain Rotier's reds from Duras and Braucol and sweet Renaissance whites have brought critical acclaim to the appellation.")
prod5b, new5b = PROD("Rotier Gaillac Renaissance Doux", "wine_dessert", prod5b_id, r5, "France",
    subcategory="sweet_white", price_tier="mid_range",
    description="Domaine Rotier's signature sweet white from Ondenc and Mauzac; late-harvest with noble rot concentration producing honey, quince, and beeswax complexity. Gaillac's answer to Sauternes at a fraction of the notoriety — and price.")
if new5b:
    PAIR(prod5b, "Roquefort with toasted walnut bread and acacia honey", "contrast", "classic", "cheese",
        "Blue cheese's powerful salt and funk contrasts Gaillac sweet Ondenc's honey sweetness; a Southwest classic cheese course")
    PAIR(prod5b, "Foie gras poêlé with peach and ginger gastrique", "complement", "classic", "starter",
        "Sweet wine and seared foie gras is the Southwest's great pairing; peach echoes Ondenc's stone fruit while ginger adds spice depth")
    PAIR(prod5b, "Crème caramel with caramelised banana and rum", "complement", "established", "dessert",
        "Caramelised sweetness echoes the wine's honey notes; banana and rum add tropical depth against the Ondenc's quince character")
    PAIR(prod5b, "Époisses with dried apricot and toasted hazelnuts", "contrast", "adventurous", "cheese",
        "Washed-rind pungency meets sweet white wine in the great French contrast tradition; apricot bridges the fruit character")

# ── Summary ──────────────────────────────────────────────────────────────────
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
conn.close()
