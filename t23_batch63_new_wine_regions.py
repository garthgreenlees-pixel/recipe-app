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

# ── REGION 1: Bekaa Valley (Lebanon) ────────────────────────────────────────
print("\n=== Region 1: Bekaa Valley ===")
r1 = R("Bekaa Valley", "Lebanon", "wine",
    designation_type="appellation", designation_name="Bekaa Valley",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="The Bekaa Valley is Lebanon's principal wine region, a high-altitude plateau (900-1100m) between the Lebanon and Anti-Lebanon mountain ranges that provides an unlikely Mediterranean viticulture with cool nights, intense sun, and minimal rainfall. Château Musar has brought international fame to the region's Cabernet Sauvignon, Cinsault, and Carignan blends; a new generation produces Rhône-influenced reds and aromatic whites.",
    key_producers="Château Musar, Massaya, Château Ksara, Domaine des Tourelles",
    historical_context="Lebanon's winemaking tradition dates to the Phoenicians — among history's great wine traders. Modern viticulture was established by Jesuit missionaries at Château Ksara in 1857. Château Musar, founded in 1930 by Gaston Hochar, survived the Lebanese Civil War and became the region's global ambassador when Jancis Robinson championed the wines at the 1979 Bristol Wine Fair.")

VIN(r1, 2022, "excellent", "rising", "Outstanding Bekaa Valley vintage; exceptional concentration and mineral definition from the high-altitude conditions")
VIN(r1, 2021, "very_good", "stable", "Fine balanced year with good Cabernet-Cinsault complexity and the valley's characteristic mineral freshness")
VIN(r1, 2020, "good", "stable", "Difficult year due to regional instability; wines made showed excellent varietal character despite challenges")
VIN(r1, 2019, "excellent", "rising", "Benchmark vintage; classic Musar-region complexity with extraordinary aging potential")
VIN(r1, 2018, "very_good", "stable", "Excellent year with fine Cinsault-Cabernet integration and good structure for medium-term aging")

prod1a_id = P("Château Musar", "Lebanon", r1, "winery",
    "Lebanon's most celebrated winery and one of the world's most idiosyncratic and compelling wine producers; Serge and later Gaston Hochar's Cabernet-Cinsault blends aged for 7 years before release achieve remarkable complexity — earthy, oxidative, and uniquely Lebanese. Survived the Civil War without missing a vintage.")
prod1a, new1a = PROD("Château Musar Rouge", "wine_still", prod1a_id, r1, "Lebanon",
    subcategory="red", price_tier="premium",
    description="Lebanon's iconic red: Cabernet Sauvignon, Cinsault, and Carignan from 45-year-old Bekaa Valley vines, aged 7 years before release. Earthy, complex, and utterly individual — leather, cedar, dried cherry, oriental spice, and a distinctive oxidative depth. Requires patience and rewards generously.")
if new1a:
    PAIR(prod1a, "Slow-braised lamb shoulder with pomegranate molasses and pine nuts", "complement", "classic", "main",
        "Lebanese slow-cooked lamb with pomegranate is a direct regional pairing; the wine's dried cherry and spice mirror the molasses's sweet-sour depth")
    PAIR(prod1a, "Kibbeh nayyeh (raw lamb tartare) with bulgur, onion, and fresh mint", "complement", "classic", "starter",
        "Lebanon's most refined raw lamb preparation meets Musar's earthy Cinsault character; mint adds refreshing contrast to the wine's spice")
    PAIR(prod1a, "Grilled lamb kofta with labneh, sumac, and flatbread", "complement", "classic", "main",
        "The Bekaa Valley's quintessential lamb pairing; sumac's tartness cuts through Musar's earthy richness and cedar depth")
    PAIR(prod1a, "Aged Halloumi grilled with thyme and pomegranate seeds", "complement", "established", "cheese",
        "Grilled Halloumi's char and salt meet the wine's earthy complexity; pomegranate adds sweet-tart fruit to bridge the cedar and dried cherry")

prod1b_id = P("Massaya", "Lebanon", r1, "winery",
    "A dynamic modern Bekaa Valley producer with French Rhône Valley partners; Massaya produces both accessible everyday wines and serious single-vineyard expressions that showcase the Bekaa's potential for sophisticated Rhône-style blends.")
prod1b, new1b = PROD("Massaya Classic Rouge", "wine_still", prod1b_id, r1, "Lebanon",
    subcategory="red", price_tier="mid_range",
    description="Massaya's accessible Bekaa Valley red: Cinsault, Cabernet Sauvignon, and Syrah blended in Rhône style with Lebanese terroir. Dark cherry, Mediterranean herbs, and mineral freshness from the high-altitude plateau. Excellent value introduction to Lebanese wine.")
if new1b:
    PAIR(prod1b, "Shawarma lamb with garlic sauce, pickle, and flatbread", "complement", "established", "casual",
        "The Levant's iconic street food with its spiced lamb and sharp garlic is a natural vehicle for Massaya's fruit-forward Cinsault blend")
    PAIR(prod1b, "Moussaka with lamb, aubergine, and béchamel", "complement", "classic", "main",
        "Eastern Mediterranean baked lamb and aubergine with its rich béchamel is elevated by the wine's dark cherry and herb complexity")
    PAIR(prod1b, "Spiced lamb chops with fattoush salad and hummus", "complement", "classic", "main",
        "A spread of Lebanese mezze with lamb is the natural setting for Massaya; the Rhône-inspired blend handles both the meat and the herb-bright salad")
    PAIR(prod1b, "Maghmour (slow-cooked aubergine with chickpeas and tomatoes)", "complement", "established", "main",
        "Lebanese vegan comfort food with earthy aubergine and chickpeas is amplified by the wine's fruit and Mediterranean herb character")

# ── REGION 2: Kakheti (Georgia) ─────────────────────────────────────────────
print("\n=== Region 2: Kakheti ===")
r2 = R("Kakheti", "Georgia", "wine",
    designation_type="appellation", designation_name="Kakheti",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Kakheti is Georgia's principal wine region and the birthplace of the ancient Qvevri (clay amphora) winemaking tradition — arguably the world's oldest winemaking method at 8,000 years. Extended skin contact (6 months to a year) produces amber or orange wines of extraordinary tannic structure and complexity from native varieties like Rkatsiteli and Mtsvane. The technique is on UNESCO's Intangible Cultural Heritage list.",
    key_producers="Pheasant's Tears, Alaverdi Monastery, Teliani Valley, Château Mukhrani",
    historical_context="Georgia's winemaking tradition dates to approximately 6000 BC — the world's oldest confirmed wine production. The Qvevri (egg-shaped terracotta amphora buried in the earth) has been the vessel for fermentation, aging, and storage for millennia. The natural wine movement's global interest in skin-contact whites has brought unprecedented international attention to Georgian Qvevri wines from the 2000s onward.")

VIN(r2, 2023, "very_good", "rising", "Good Kakheti growing season; native varieties achieved excellent aromatic complexity with strong Qvevri fermentation character")
VIN(r2, 2022, "excellent", "rising", "Outstanding vintage; exceptional tannin and amber complexity from extended maceration in Qvevri across multiple estates")
VIN(r2, 2021, "good", "stable", "Balanced year with fine Rkatsiteli expression; good acidity and orange wine structure for medium-term aging")
VIN(r2, 2020, "very_good", "stable", "Concentrated vintage with excellent skin-contact tannins and dried fruit complexity from Kakheti's clay terroir")
VIN(r2, 2019, "excellent", "rising", "Benchmark Kakheti vintage; extraordinary Qvevri amber wines with deep amber colour, walnut, and dried apricot character")

prod2a_id = P("Pheasant's Tears", "Georgia", r2, "winery",
    "The most internationally celebrated Qvevri winery and ambassador for Georgian natural wine; founded by American artist John Wurdeman and Georgian winemaker Gela Patalishvili, Pheasant's Tears produces single-variety, single-vineyard Qvevri wines from rescued native Georgian varieties.")
prod2a, new2a = PROD("Pheasant's Tears Rkatsiteli", "wine_still", prod2a_id, r2, "Georgia",
    subcategory="white", price_tier="mid_range",
    description="Pheasant's Tears' benchmark Qvevri Rkatsiteli: whole-cluster fermentation with extended skin contact (6+ months) in buried Qvevri amphora. Deep amber colour; walnut, dried apricot, orange peel, and extraordinary tannic structure — the definitive introduction to Georgian amber wine.")
if new2a:
    PAIR(prod2a, "Sulguni cheese with walnut paste and fresh herbs (Pkhali)", "complement", "classic", "starter",
        "Georgian Pkhali — herb-walnut spread — is the defining regional food for Rkatsiteli; walnut mirrors the wine's skin-contact tannin and nut character")
    PAIR(prod2a, "Chicken in walnut sauce (Satsivi) with Georgian bread", "complement", "classic", "main",
        "Satsivi's walnut and spice sauce is the quintessential Georgian pairing for Rkatsiteli; the wine's tannic amber structure matches the dish's richness")
    PAIR(prod2a, "Aged Manchego with quince paste and Marcona almonds", "complement", "established", "cheese",
        "Semi-hard aged sheep cheese with quince echoes the wine's dried fruit and tannic structure; almonds mirror the walnut character")
    PAIR(prod2a, "Slow-cooked lamb shoulder with pomegranate, coriander, and walnuts", "complement", "established", "main",
        "Caucasian slow-lamb with pomegranate and walnut is the wine's natural culinary territory; spice and fruit integrate with Qvevri tannin")

prod2b_id = P("Alaverdi Monastery", "Georgia", r2, "winery",
    "One of Georgia's oldest and most culturally significant wineries; the monks of Alaverdi Monastery have produced Qvevri wine continuously since the 11th century. Their wines are made following centuries-old tradition — among the most authentic and historically significant wines in the world.")
prod2b, new2b = PROD("Alaverdi Monastery Rkatsiteli Amber", "wine_still", prod2b_id, r2, "Georgia",
    subcategory="white", price_tier="mid_range",
    description="Alaverdi Monastery's traditional Qvevri Rkatsiteli: full skin contact, wild fermentation, and aging in beeswax-sealed Qvevri amphora following 11th-century monastic methods. Deep amber; beeswax, walnut, dried fruit, and extraordinary tannin — one of the world's most historically resonant wines.")
if new2b:
    PAIR(prod2b, "Mtsvadi (Georgian pork skewers over vine cuttings)", "complement", "classic", "main",
        "Georgia's iconic grilled pork over wood is the country's defining food; Alaverdi's amber tannin matches the smoke and char of vine-cutting grilling")
    PAIR(prod2b, "Badrijani nigvzit (aubergine rolls with walnut filling)", "complement", "classic", "starter",
        "Georgian aubergine stuffed with walnut paste is a perfect marriage with Rkatsiteli amber; walnut-to-walnut resonance is deeply satisfying")
    PAIR(prod2b, "Chakapuli (spring lamb stew with tarragon and tkemali)", "complement", "classic", "main",
        "Georgia's spring festival lamb stew with tarragon and sour plum sauce creates the ceremonial pairing for this monastic wine")
    PAIR(prod2b, "Hummus with roasted aubergine, pomegranate, and pine nuts", "complement", "established", "starter",
        "Eastern Mediterranean mezze with pomegranate's sweet-tart character and aubergine's smokiness bridges beautifully to Qvevri amber's dried fruit complexity")

# ── REGION 3: Naoussa PDO (Greece) ──────────────────────────────────────────
print("\n=== Region 3: Naoussa ===")
r3 = R("Naoussa", "Greece", "wine",
    designation_type="PDO", designation_name="Naoussa PDO",
    reputation_tier="respected",
    quality_trajectory="ascending",
    description="Naoussa is northern Greece's most distinguished red wine PDO, produced entirely from the indigenous Xinomavro variety on the granite and clay slopes of the Vermio mountain in Macedonia. Xinomavro is Greece's great red grape — high acid, high tannin, and extraordinary aging potential. Its tomato-olive-herb aromatic profile at its finest rivals Nebbiolo in structural complexity.",
    key_producers="Kyr-Yianni, Thymiopoulos, Domaine Dalamara, Boutari",
    historical_context="Naoussa has been producing wine since ancient times; the area was known for wine production during Byzantine rule and Ottoman occupation. Modern recognition began in 1971 when Naoussa became one of Greece's first appellations. The arrival of Antonis Kyr-Yianni and later Apostolos Thymiopoulos from the 1990s-2000s transformed the appellation's international reputation, revealing Xinomavro's world-class potential.")

VIN(r3, 2023, "excellent", "rising", "Outstanding Naoussa vintage; Xinomavro achieved exceptional tannin ripeness and aromatic complexity on the Vermio slopes")
VIN(r3, 2022, "very_good", "stable", "Fine balanced year with elegant Xinomavro; good typicity with tomato-herb character and firm tannic structure")
VIN(r3, 2021, "good", "stable", "Cooler year with lighter body; excellent acidity and varietal aromatic precision")
VIN(r3, 2020, "excellent", "rising", "Hot year producing powerful, concentrated Xinomavro with exceptional aging potential")
VIN(r3, 2019, "very_good", "rising", "Classic vintage with fine Xinomavro expression; olive, sun-dried tomato, and mineral depth in balance")

prod3a_id = P("Kyr-Yianni", "Greece", r3, "winery",
    "The transformative producer of modern Naoussa; Yiannis Boutaris founded the estate in 1997 after leaving the family Boutari company and has since produced Xinomavro wines of international stature — demonstrating the variety's capacity for Nebbiolo-like complexity and longevity.")
prod3a, new3a = PROD("Kyr-Yianni Ramnista Naoussa", "wine_still", prod3a_id, r3, "Greece",
    subcategory="red", price_tier="premium",
    description="Kyr-Yianni's flagship single-vineyard Naoussa from the Ramnista vineyard: 100% Xinomavro aged in French oak. Olive, sun-dried tomato, fresh herb, and mineral depth with the variety's characteristic high acidity and firm tannin. The benchmark for ambitious Naoussa and Greek red wine of genuine seriousness.")
if new3a:
    PAIR(prod3a, "Slow-braised lamb with tomato, cinnamon, and orzo (Stifado)", "complement", "classic", "main",
        "Stifado's tomato-cinnamon-lamb combination mirrors Xinomavro's own sun-dried tomato and spice character — a direct aromatic parallel")
    PAIR(prod3a, "Roasted whole lamb with lemon, wild oregano, and garlic (Arni sti souvla)", "complement", "classic", "main",
        "Greek Easter lamb on the spit with oregano is the defining Naoussa pairing; the wine's herb and mineral character meets the lamb's fat and citrus")
    PAIR(prod3a, "Pastitsio (Greek baked pasta with meat sauce and béchamel)", "complement", "classic", "main",
        "Greece's comfort casserole with rich béchamel and cinnamon-spiced meat sauce is amplified by Xinomavro's acidity cutting through the richness")
    PAIR(prod3a, "Aged Kefalograviera with black olive and dried fig", "bridge", "classic", "cheese",
        "Hard Greek sheep-goat cheese with olive and fig creates the regional cheese pairing for Naoussa's complex mineral Xinomavro")

prod3b_id = P("Thymiopoulos Vineyards", "Greece", r3, "winery",
    "The young visionary of Naoussa; Apostolos Thymiopoulos's biodynamic estate produces Xinomavro of extraordinary freshness and terroir precision — the winemaker who most clearly revealed the variety's Pinot Noir-like delicacy alongside its structural power.")
prod3b, new3b = PROD("Thymiopoulos Earth and Sky Xinomavro Naoussa", "wine_still", prod3b_id, r3, "Greece",
    subcategory="red", price_tier="mid_range",
    description="Thymiopoulos's benchmark Naoussa: old vine Xinomavro fermented with indigenous yeasts and aged in neutral oak to preserve varietal purity. Elegant olive, fresh tomato, mineral, and dried herb with the variety's signature high acidity — among Greece's most compelling and terroir-faithful reds.")
if new3b:
    PAIR(prod3b, "Moussaka with spiced lamb, aubergine, and Kefalotiri béchamel", "complement", "classic", "main",
        "The Greek national dish and Xinomavro make an excellent match; the wine's tomato-herb aromatic profile mirrors the meat sauce while acidity cuts the béchamel")
    PAIR(prod3b, "Grilled octopus with lemon, olive oil, and caper berries", "complement", "established", "starter",
        "Grilled octopus's char and sea salinity are complemented by Xinomavro's acidity and herb character; caper berry's brine amplifies the mineral depth")
    PAIR(prod3b, "Spanakopitta (spinach and feta pie with filo pastry)", "complement", "established", "starter",
        "Feta's salt and spinach's mineral bitterness meet Xinomavro's acidity in the classic Greek meze pairing")
    PAIR(prod3b, "Lamb chops with tzatziki, lemon, and fresh mint", "complement", "classic", "main",
        "Simple grilled lamb with tzatziki and lemon is Thymiopoulos's natural food partner; the wine's freshness and herb depth match the dish's precision")

# ── REGION 4: Central Otago (New Zealand) ───────────────────────────────────
print("\n=== Region 4: Central Otago ===")
r4 = R("Central Otago", "New Zealand", "wine",
    designation_type="appellation", designation_name="Central Otago GI",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Central Otago is New Zealand's most dramatic wine region — a semi-arid inland plateau in the South Island surrounded by the Southern Alps, producing the world's southernmost commercial Pinot Noir. The extreme continental climate (hot days, cold nights, thin air) concentrates flavours in short growing seasons. The wines show dark cherry, spice, dried herb, and a distinctive mineral-schist character unlike any other Pinot Noir region.",
    key_producers="Felton Road, Rippon, Mt Difficulty, Amisfield, Burn Cottage",
    historical_context="Central Otago's wine industry is remarkably young — the first modern vines were planted by Ann Pinckney in 1976. Felton Road, established in 1992, is credited with establishing the region's Pinot Noir benchmark. The region grew rapidly in the 2000s and is now globally recognised as one of Pinot Noir's great new-world homes, regularly commanding New Burgundy-level prices.")

VIN(r4, 2023, "excellent", "rising", "Outstanding vintage; perfect growing season gave exceptional Pinot Noir concentration with signature dark cherry and schist minerality")
VIN(r4, 2022, "very_good", "stable", "Fine balanced year with elegant, perfumed Central Otago Pinot; good typicity with dark fruit and mineral precision")
VIN(r4, 2021, "good", "stable", "More restrained year; lighter-bodied Pinot with excellent acidity and delicate red fruit character")
VIN(r4, 2020, "excellent", "rising", "Powerful vintage with concentrated dark cherry and exceptional structural depth; age-worthy")
VIN(r4, 2019, "excellent", "rising", "One of Central Otago's finest vintages; textbook schist mineral character and dark fruit complexity")

prod4a_id = P("Felton Road", "New Zealand", r4, "winery",
    "The benchmark producer of Central Otago Pinot Noir; biodynamic Felton Road's single-vineyard bottlings from Bannockburn define the region's finest character — concentrated, mineral, and capable of Burgundy-rivalling aging complexity.")
prod4a, new4a = PROD("Felton Road Block 3 Pinot Noir", "wine_still", prod4a_id, r4, "New Zealand",
    subcategory="red", price_tier="ultra_premium",
    description="The most celebrated Central Otago Pinot Noir; Felton Road's biodynamic Block 3 from the Bannockburn schist shows extraordinary dark cherry, spice, and mineral precision. The benchmark for New Zealand Pinot Noir and a wine that regularly challenges Burgundy premier cru in quality and price.")
if new4a:
    PAIR(prod4a, "Pan-roasted duck breast with cherry reduction and wilted watercress", "complement", "classic", "main",
        "Duck and Pinot Noir is the universal luxury pairing; cherry reduction echoes Block 3's dark cherry core while watercress adds mineral bitterness")
    PAIR(prod4a, "Roasted Canterbury lamb rack with rosemary and pinot noir jus", "complement", "classic", "main",
        "New Zealand's finest lamb from Canterbury with a Pinot-based sauce creates regional unity and the wine's dark fruit matches the lamb's delicacy")
    PAIR(prod4a, "Mushroom and truffle risotto with aged Parmigiano", "complement", "established", "main",
        "Earthy truffle and mushroom amplify Central Otago Pinot's schist mineral depth; Parmigiano adds saline umami to bridge the wine's fruit")
    PAIR(prod4a, "Grilled salmon with beurre rouge and micro herbs", "complement", "adventurous", "fish_course",
        "Wild salmon's fattiness and iron character work beautifully with light-touch Pinot Noir; beurre rouge (red wine butter) bridges salmon and wine")

prod4b_id = P("Rippon", "New Zealand", r4, "winery",
    "The most scenically iconic Central Otago estate, set dramatically above Lake Wanaka; Rippon's biodynamic Pinot Noirs from the estate's lake-edge schist and gneiss soils show extraordinary elegance and mineral tension — the most 'European' expression of Central Otago's character.")
prod4b, new4b = PROD("Rippon Mature Vine Pinot Noir", "wine_still", prod4b_id, r4, "New Zealand",
    subcategory="red", price_tier="premium",
    description="Rippon's estate Pinot Noir from mature vines above Lake Wanaka: biodynamic and whole-bunch fermented for aromatic complexity. Red cherry, dried herb, rose hip, and a distinctive lake-mineral precision. More elegantly structured than most Central Otago Pinot — closer to Chambolle-Musigny than Gevrey in spirit.")
if new4b:
    PAIR(prod4b, "Cervena venison loin with blackberry jus and celeriac purée", "complement", "classic", "main",
        "New Zealand farmed venison with blackberry is the South Island's great game pairing for Pinot Noir; celeriac adds earthy mineral to bridge the schist")
    PAIR(prod4b, "Whole roasted quail with thyme, wild mushroom, and grilled polenta", "complement", "established", "main",
        "Small game bird with mushroom and polenta matches Rippon's elegant Pinot structure; the whole-bunch fermentation adds stems-herb complexity")
    PAIR(prod4b, "Aged Gouda with dried cranberry and walnut", "bridge", "established", "cheese",
        "Semi-hard Gouda's caramel notes and cranberry bridge Rippon's red fruit and rose hip character; walnuts add mineral bitterness")
    PAIR(prod4b, "Seared tuna with olive oil, lemon, and capers", "complement", "adventurous", "fish_course",
        "Tuna's firm red flesh and saline character work with Rippon's lighter-touch Pinot; capers add brine to echo the lake-mineral quality")

# ── REGION 5: Coonawarra (Australia) ────────────────────────────────────────
print("\n=== Region 5: Coonawarra ===")
r5 = R("Coonawarra", "Australia", "wine",
    designation_type="GI", designation_name="Coonawarra GI",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Coonawarra is Australia's most celebrated Cabernet Sauvignon appellation, built on a narrow strip of terra rossa (red iron-rich soil over limestone) in South Australia's Limestone Coast. The distinctive red earth imparts elegant, structured Cabernet with cassis, cedar, mint, and eucalyptus character — Australia's closest approach to a Bordeaux-like minerally refined Cabernet. The cigar-shaped terra rossa strip is only 12km long and 2km wide.",
    key_producers="Wynns Coonawarra Estate, Penfolds (Bin 707), Balnaves, Parker Coonawarra Estate",
    historical_context="Coonawarra was first planted by John Riddoch in 1890 who recognised the terra rossa soil's unique agricultural properties. Cabernet Sauvignon's suitability was confirmed in the 1950s-60s, and the region's international reputation was built through the 1980s by producers like Wynns whose Black Label Cabernet became Australia's first great single-region Cabernet benchmark.")

VIN(r5, 2022, "very_good", "stable", "Good Coonawarra vintage with excellent terra rossa Cabernet expression; cassis and cedar well integrated")
VIN(r5, 2021, "excellent", "rising", "Outstanding South Australian vintage; exceptional Cabernet concentration with the characteristic terra rossa mineral precision")
VIN(r5, 2020, "good", "stable", "Wildfire smoke affected some parcels; cleaner sites showed excellent Cabernet character with good aging potential")
VIN(r5, 2019, "excellent", "rising", "Benchmark Coonawarra vintage; textbook cassis, cedar, and mint-eucalyptus with fine tannic structure")
VIN(r5, 2018, "very_good", "stable", "Classic year with excellent Cabernet depth and the characteristic limestone-derived mineral length")

prod5a_id = P("Wynns Coonawarra Estate", "Australia", r5, "winery",
    "The cornerstone of Coonawarra's history and reputation; Wynns Black Label Cabernet Sauvignon has been the benchmark for Australian Coonawarra Cabernet since the 1950s — age-worthy, mineral, and consistently among Australia's finest at an accessible price.")
prod5a, new5a = PROD("Wynns Black Label Cabernet Sauvignon", "wine_still", prod5a_id, r5, "Australia",
    subcategory="red", price_tier="mid_range",
    description="The iconic Coonawarra benchmark: Wynns Black Label Cabernet from the historic estate on the terra rossa strip. Cassis, cedar, fresh herb, and the distinctive eucalyptus-mint note of Coonawarra with limestone mineral length. Outstanding value for the quality and 10-20 year aging capability.")
if new5a:
    PAIR(prod5a, "Grilled Angus beef sirloin with green peppercorn sauce and dauphinoise", "complement", "classic", "main",
        "Australian beef and Coonawarra Cabernet is the country's defining pairing; green peppercorn sauce mirrors the wine's pepper and herb character")
    PAIR(prod5a, "Roasted lamb rack with mint jelly, rosemary, and garlic crust", "complement", "classic", "main",
        "Australian rack of lamb with mint is a direct echo of Coonawarra Cabernet's characteristic mint-eucalyptus note — a classic regional match")
    PAIR(prod5a, "Dry-aged ribeye with bone marrow, béarnaise, and truffle", "complement", "established", "main",
        "Dry-aged beef's concentrated flavour and bone marrow richness need Coonawarra's terra rossa tannin and mineral to balance; truffle amplifies the cedar note")
    PAIR(prod5a, "Aged Cheddar with quince paste and pecan nuts", "bridge", "established", "cheese",
        "Mature Cheddar with quince bridges Coonawarra's cassis fruit; pecan adds Southern Hemisphere nuttiness to echo the terra rossa mineral")

prod5b_id = P("Balnaves of Coonawarra", "Australia", r5, "winery",
    "A highly regarded family estate on the Coonawarra terra rossa strip; the Balnaves family produces benchmark single-vineyard Cabernet Sauvignon wines of restraint, elegance, and age-worthiness that represent Coonawarra at its most precise and terroir-faithful.")
prod5b, new5b = PROD("Balnaves The Tally Reserve Cabernet Sauvignon", "wine_still", prod5b_id, r5, "Australia",
    subcategory="red", price_tier="premium",
    description="Balnaves's flagship Coonawarra Cabernet: The Tally Reserve from old vines on the finest terra rossa soils. Concentrated cassis, cedar, graphite, and eucalyptus with extraordinary mineral precision from the limestone. Among Coonawarra's most refined and age-worthy expressions — 20+ year potential.")
if new5b:
    PAIR(prod5b, "Roasted rack of venison with beetroot purée, blackcurrant, and juniper", "complement", "established", "main",
        "Venison's lean game richness and blackcurrant echo Coonawarra's cassis; beetroot adds earthy mineral depth to echo the terra rossa")
    PAIR(prod5b, "Slow-braised oxtail with root vegetables, thyme, and red wine", "complement", "classic", "main",
        "Oxtail's rich gelatinous depth requires The Tally's tannic structure and mineral precision; red wine braising creates culinary unity")
    PAIR(prod5b, "Truffle and Gruyère toasted sandwich with dijon mustard", "complement", "adventurous", "casual",
        "An elevated everyday pairing: truffle's earthy intensity and Gruyère's nuttiness bridge Coonawarra Cabernet's mineral cedar character")
    PAIR(prod5b, "Smoked dark chocolate torte with sea salt and caramel", "complement", "adventurous", "dessert",
        "Dark chocolate's bitterness and smoke echo the wine's aged cedar; sea salt amplifies the terra rossa mineral while caramel adds richness")

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
