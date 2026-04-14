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
        return (row[0], False)
    cur.execute("""INSERT INTO beverage_products
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
        (name, category, subcategory, producer_id, region_id, origin_country, description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  Product: {name} ({pid})")
    return (pid, True)

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic):
    cur.execute("""INSERT INTO pairing_intelligence
        (beverage_product_id, food_description, pairing_type, confidence,
         meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,1)""",
        (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic))

# ── Batch 71 ──────────────────────────────────────────────────────────────────
# Regions: Swartland, Franschhoek, Walker Bay, Robertson, Elim

# ── Region 1: Swartland ───────────────────────────────────────────────────────
print("\n=== Region 1: Swartland ===")
r1 = R("Swartland", "South Africa", "wine",
    designation_type="WO",
    designation_name="Swartland WO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Rugged, arid region north of Cape Town producing South Africa's most exciting natural and minimal-intervention wines from old dry-farmed bush vines — Chenin Blanc, Syrah, Grenache and Cinsault.",
    key_producers="Eben Sadie (Sadie Family Wines), Mullineux, AA Badenhorst, Leeuwenkuil, Testalonga",
    historical_context="The Swartland Revolution, led by Eben Sadie and Charles Melton, transformed South African wine in the 2000s from a commodity to one of the world's most exciting terroir-driven wine regions."
)
VIN(r1, 2022, "excellent", "rising", "Cool La Niña year with excellent retention of freshness; Chenin Blanc of exceptional tension and Syrah of great elegance.")
VIN(r1, 2021, "very_good", "stable", "Balanced season with good diurnal variation; wines show purity and depth.")
VIN(r1, 2020, "excellent", "rising", "One of Swartland's best recent vintages; wines of remarkable concentration and freshness.")
VIN(r1, 2019, "good", "stable", "Slightly warm year; concentrated but approachable wines with generous fruit.")
VIN(r1, 2018, "very_good", "stable", "Good overall quality; Chenin Blanc shows particular brilliance in this cooler-than-average year.")

p1a = P("Sadie Family Wines", "winery", r1, "South Africa",
    production_philosophy="biodynamic",
    philosophy_description="Eben Sadie's landmark estate producing Columella (Syrah/Mourvèdre) and Palladius (white blend) — South Africa's most celebrated wines from Swartland old vines.",
    reputation_narrative="Sadie Family Wines defines Swartland's global reputation; Columella and Palladius are considered among the world's finest expressions of their respective varieties.",
    price_positioning="ultra_premium")
prod1a, new1a = PROD("Sadie Family Columella", "wine_still", p1a, r1, "South Africa",
    subcategory="Syrah blend",
    description="South Africa's most celebrated red: old-vine Syrah with Mourvèdre, Grenache and Cinsault from Swartland schist — violet, smoked meat, dark fruit and extraordinary mineral length.",
    price_tier="ultra_premium")
if new1a:
    PAIR(prod1a, "Slow-roasted lamb shoulder with preserved lemon and olives", "complement", "classic", "main", "The North African-inflected lamb resonates with Swartland's schist and spiced Syrah character.")
    PAIR(prod1a, "Venison loin with wild herb crust and beetroot", "complement", "established", "main", "Gamey venison and earthy beetroot match Columella's dark fruit and iron minerality.")
    PAIR(prod1a, "Aged Karoo lamb chops on a braai", "complement", "classic", "main", "Terroir-to-terroir: Swartland wine and Karoo lamb are South African culinary patrimony.")
    PAIR(prod1a, "Smoked ostrich carpaccio with shaved truffle", "complement", "adventurous", "starter", "Lean, iron-rich ostrich and truffle align with the wine's smoked meat and mineral notes.")

p1b = P("Mullineux Family Wines", "winery", r1, "South Africa",
    production_philosophy="minimal_intervention",
    philosophy_description="Chris and Andrea Mullineux's estate specialising in single-origin Chenin Blanc and Syrah from Swartland's schist, granite and iron soils.",
    reputation_narrative="Mullineux is South Africa's most acclaimed producer for terroir-differentiated Chenin Blanc; the Granite and Schist Chenins are global benchmarks.",
    price_positioning="premium")
prod1b, new1b = PROD("Mullineux Schist Syrah", "wine_still", p1b, r1, "South Africa",
    subcategory="Syrah",
    description="Single-soil Swartland Syrah from schist vineyards — dark olive, cured meat, violet, iron and graphite with restrained alcohol and northern Rhône-like precision.",
    price_tier="premium")
if new1b:
    PAIR(prod1b, "Grilled lamb merguez sausage with flatbread and harissa", "complement", "established", "main", "Spiced lamb amplifies Syrah's pepper and iron notes; harissa heat matches the wine's depth.")
    PAIR(prod1b, "Braised oxtail with root vegetables and red wine", "complement", "classic", "main", "Rich braised meat aligns with the wine's mineral weight; root vegetables add earthiness.")
    PAIR(prod1b, "Mushroom and olive tapenade crostini", "bridge", "suggested", "amuse", "Earthy olive and mushroom resonate with the wine's iron and dark fruit character.")
    PAIR(prod1b, "Aged Pecorino with black truffle honey", "complement", "established", "cheese", "Hard ewes' milk mirrors wine structure; truffle honey bridges mineral and fruit.")

# ── Region 2: Franschhoek ─────────────────────────────────────────────────────
print("\n=== Region 2: Franschhoek ===")
r2 = R("Franschhoek", "South Africa", "wine",
    designation_type="WO",
    designation_name="Franschhoek WO",
    reputation_tier="prestigious",
    quality_trajectory="established",
    description="Picturesque valley east of Cape Town, founded by French Huguenots in 1688, producing elegant Chenin Blanc, Semillon, Chardonnay and Cabernet Sauvignon with mountain-influenced freshness.",
    key_producers="Boekenhoutskloof, Morgenster, La Motte, Chamonix, Grande Provence",
    historical_context="Franschhoek's French Huguenot heritage gave South Africa its oldest wine culture; Semillon has been grown here since the 17th century and remains a compelling regional specialty."
)
VIN(r2, 2022, "excellent", "stable", "Cool year with good mountain air freshness; Semillon and Chenin of particular elegance.")
VIN(r2, 2021, "very_good", "stable", "Balanced season; wines show restraint and food-friendly acidity.")
VIN(r2, 2020, "good", "stable", "Good quality overall; approachable whites with fresh citrus character.")
VIN(r2, 2019, "excellent", "rising", "Outstanding vintage for both reds and whites; wines of exceptional structure and balance.")
VIN(r2, 2018, "very_good", "stable", "Consistent quality; Semillon and Cabernet both performed strongly.")

p2a = P("Boekenhoutskloof", "winery", r2, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="Franschhoek estate famous for iconic Syrah and Semillon, plus the The Chocolate Block and Wolftrap ranges demonstrating regional versatility.",
    reputation_narrative="Boekenhoutskloof Syrah is considered South Africa's finest single-varietal Syrah; The Chocolate Block is one of South Africa's most successful fine wine blends.",
    price_positioning="premium")
prod2a, new2a = PROD("Boekenhoutskloof Syrah", "wine_still", p2a, r2, "South Africa",
    subcategory="Syrah",
    description="South Africa's most acclaimed single-varietal Syrah — violet, smoked olive, white pepper, dark berry and savoury complexity with remarkable restraint and elegance.",
    price_tier="premium")
if new2a:
    PAIR(prod2a, "Slow-roasted pork belly with five-spice and plum glaze", "complement", "classic", "main", "Five-spice and pork fat align with Syrah's spiced dark fruit; plum glaze bridges primary fruit.")
    PAIR(prod2a, "Duck confit with lentils and smoked paprika", "complement", "established", "main", "Smoked paprika echoes the wine's olive and pepper notes; duck's gamey richness matches Syrah weight.")
    PAIR(prod2a, "Grilled ostrich fillet with red wine jus", "complement", "established", "main", "Iron-rich lean protein and Syrah's mineral backbone are a natural South African pairing.")
    PAIR(prod2a, "Aged Gruyère with fig jam", "bridge", "suggested", "cheese", "Nutty cheese and fig bridge Syrah's dark fruit; aged texture softens tannin.")

p2b = P("Chamonix Wine Farm", "winery", r2, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="High-altitude Franschhoek estate producing elegant mountain Chardonnay, Pinot Noir and age-worthy Cabernet from cool slopes.",
    reputation_narrative="Chamonix's Chardonnay and Pinot Noir are consistently ranked among Franschhoek's finest; the altitude gives wines exceptional freshness.",
    price_positioning="premium")
prod2b, new2b = PROD("Chamonix Chardonnay", "wine_still", p2b, r2, "South Africa",
    subcategory="Chardonnay",
    description="High-altitude Franschhoek Chardonnay with white peach, lemon curd, grilled hazelnut and vibrant mountain freshness; restrained and elegant in style.",
    price_tier="premium")
if new2b:
    PAIR(prod2b, "Grilled Cape snoek with lemon and apricot jam", "complement", "adventurous", "main", "Traditional South African coastal fish and the country's mountain Chardonnay — a terroir pairing.")
    PAIR(prod2b, "Butter-poached Cape crayfish (rock lobster)", "complement", "classic", "main", "Rich crustacean and Chardonnay is a global classic; Cape crayfish makes it distinctly South African.")
    PAIR(prod2b, "Chicken and mushroom vol-au-vent with cream sauce", "complement", "established", "main", "Classic rich poultry-and-cream dish aligns perfectly with the wine's weight and texture.")
    PAIR(prod2b, "Brie de Meaux with toasted brioche", "bridge", "suggested", "cheese", "Creamy cheese aligns with Chardonnay richness; brioche sweetness bridges the acidity.")

# ── Region 3: Walker Bay ──────────────────────────────────────────────────────
print("\n=== Region 3: Walker Bay ===")
r3 = R("Walker Bay", "South Africa", "wine",
    designation_type="WO",
    designation_name="Walker Bay WO",
    reputation_tier="prestigious",
    quality_trajectory="ascending",
    description="Cool coastal zone south-east of Cape Town encompassing Hemel-en-Aarde, Hermanus and Raka, producing South Africa's finest Pinot Noir and Chardonnay under strong ocean influence.",
    key_producers="Hamilton Russell Vineyards, Bouchard Finlayson, Creation Wines, Ataraxia, Storm Wines",
    historical_context="Tim Hamilton Russell pioneered Walker Bay in the 1970s, demonstrating that South Africa could produce world-class Pinot Noir and Chardonnay from cool maritime terroir."
)
VIN(r3, 2022, "excellent", "rising", "Outstanding cool vintage; Pinot Noir of Burgundian elegance and Chardonnay of exceptional minerality.")
VIN(r3, 2021, "very_good", "stable", "Balanced maritime season; wines show purity and aromatic precision.")
VIN(r3, 2020, "good", "stable", "Good quality; approachable Pinot with red fruit and gentle acidity.")
VIN(r3, 2019, "exceptional", "rising", "Benchmark Walker Bay vintage; Pinot Noir of extraordinary complexity and ageing potential.")
VIN(r3, 2018, "very_good", "stable", "Consistent quality; Chardonnay particularly strong, showing excellent tension and mineral drive.")

p3a = P("Hamilton Russell Vineyards", "winery", r3, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="Tim Hamilton Russell's pioneering estate in Hemel-en-Aarde Valley — the southernmost point of Africa's wine production — specialising in Pinot Noir and Chardonnay.",
    reputation_narrative="Hamilton Russell is South Africa's most internationally recognised Pinot Noir and Chardonnay producer; the estate wine is a consistent world-class benchmark.",
    price_positioning="premium")
prod3a, new3a = PROD("Hamilton Russell Vineyards Pinot Noir", "wine_still", p3a, r3, "South Africa",
    subcategory="Pinot Noir",
    description="South Africa's benchmark Pinot Noir — red cherry, dried rose, forest floor, fynbos (Cape flora) and gentle minerality with silky tannins and persistent length.",
    price_tier="premium")
if new3a:
    PAIR(prod3a, "Grilled duck breast with cherry and balsamic reduction", "complement", "classic", "main", "Classic Pinot pairing; duck's gamey richness and cherry sauce mirror the wine's profile exactly.")
    PAIR(prod3a, "Braised mushroom and truffle risotto", "complement", "established", "main", "Earthy forest floor in the wine aligns with mushroom and truffle; risotto cream matches silky tannins.")
    PAIR(prod3a, "Grilled Cape salmon with lentil and herb salad", "bridge", "established", "fish_course", "Fatty salmon can handle light Pinot; lentil bridges wine's earthy quality to fish.")
    PAIR(prod3a, "Aged Comté with candied walnut", "complement", "established", "cheese", "Nutty aged cheese and Pinot is a classic pairing; walnut amplifies the wine's earthy notes.")

p3b = P("Creation Wines", "winery", r3, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="Walker Bay estate known for innovative food-and-wine pairing hospitality and elegant Pinot Noir, Chardonnay and Syrah from cool maritime terroir.",
    reputation_narrative="Creation's Art of Pairing philosophy makes it one of South Africa's most celebrated wine and food destinations; the wines are equally refined.",
    price_positioning="premium")
prod3b, new3b = PROD("Creation Wines Chardonnay", "wine_still", p3b, r3, "South Africa",
    subcategory="Chardonnay",
    description="Cool Walker Bay Chardonnay with citrus, white flower, nectarine, grilled nut and a long saline mineral finish — precise, restrained and deeply satisfying.",
    price_tier="premium")
if new3b:
    PAIR(prod3b, "Pan-roasted Cape sole with caper beurre blanc", "complement", "classic", "fish_course", "Delicate coastal fish and mineral Chardonnay; caper beurre blanc amplifies the wine's citrus edge.")
    PAIR(prod3b, "Smoked trout rillettes with cucumber and dill", "complement", "established", "starter", "Smoked fish and Chardonnay is a classic; cucumber and dill bridge the wine's fresh herbal note.")
    PAIR(prod3b, "Seared scallops with pea purée and pancetta", "complement", "classic", "fish_course", "Sweet scallop and pea align with Chardonnay; pancetta adds savoury depth.")
    PAIR(prod3b, "Camembert with green apple and celery", "bridge", "suggested", "cheese", "Soft cheese's cream aligns with wine texture; green apple bridges acidity and stone fruit.")

# ── Region 4: Robertson ───────────────────────────────────────────────────────
print("\n=== Region 4: Robertson ===")
r4 = R("Robertson", "South Africa", "wine",
    designation_type="WO",
    designation_name="Robertson WO",
    reputation_tier="respected",
    quality_trajectory="established",
    description="Inland valley east of Cape Town on the Breede River, known for Chardonnay, Colombard, Cabernet Sauvignon and Shiraz produced on limestone-rich, calcium-bearing soils.",
    key_producers="Graham Beck, Springfield Estate, Bon Courage, De Wetshof",
    historical_context="Robertson's unique calcium-rich soils give wines a distinctive mineral character; Graham Beck Brut is internationally famous as the Méthode Cap Classique of choice at state occasions."
)
VIN(r4, 2022, "very_good", "stable", "Good overall quality; Chardonnay and Colombard show crisp freshness from limestone soils.")
VIN(r4, 2021, "good", "stable", "Consistent vintage; reliable, well-priced wines across all varieties.")
VIN(r4, 2020, "very_good", "stable", "Excellent Chardonnay year; limestone minerality shows clearly in the wine's structure.")
VIN(r4, 2019, "excellent", "rising", "Outstanding vintage; Graham Beck Brut vintage release was exceptional; also great Cabernet.")
VIN(r4, 2018, "good", "stable", "Reliable quality; commercial-focused but well-made reds and whites.")

p4a = P("Springfield Estate", "winery", r4, "South Africa",
    production_philosophy="minimal_intervention",
    philosophy_description="Benchmark Robertson estate producing wild-fermented, unfined Sauvignon Blanc and certified-organic Méthode Ancienne Chardonnay without any oak influence.",
    reputation_narrative="Springfield's Wild Yeast Sauvignon Blanc and Méthode Ancienne Chardonnay are considered South Africa's most distinctive whites for natural winemaking purity.",
    price_positioning="premium")
prod4a, new4a = PROD("Springfield Wild Yeast Sauvignon Blanc", "wine_still", p4a, r4, "South Africa",
    subcategory="Sauvignon Blanc",
    description="Wild-fermented Robertson Sauvignon Blanc with gooseberry, grapefruit, fig leaf and a chalky mineral finish; complex and textured for the variety.",
    price_tier="premium")
if new4a:
    PAIR(prod4a, "Oysters Rockefeller with spinach and Pernod", "complement", "classic", "aperitif", "Wild ferment complexity matches the rich dressed oyster; Pernod's anise bridges the wine's herbaceous edge.")
    PAIR(prod4a, "Grilled asparagus with hollandaise and shaved Parmesan", "complement", "classic", "starter", "Green vegetal asparagus is a natural match for herbaceous Sauvignon Blanc.")
    PAIR(prod4a, "Smoked salmon with crème fraîche and cucumber ribbons", "complement", "established", "starter", "Smoked fish and crisp Sauvignon is a proven pairing; crème fraîche mirrors the wine's texture.")
    PAIR(prod4a, "Goat's cheese tart with herbs and roasted garlic", "complement", "established", "starter", "Tangy chèvre and Sauvignon Blanc are natural companions; roasted garlic adds depth.")

p4b = P("Graham Beck Wines", "winery", r4, "South Africa",
    production_philosophy="traditional",
    philosophy_description="Robertson estate producing South Africa's most celebrated sparkling wine by Méthode Cap Classique, alongside premium still wines.",
    reputation_narrative="Graham Beck Brut NV was served at Nelson Mandela's inauguration and Barack Obama's election celebration; it remains South Africa's most iconic bubbles.",
    price_positioning="mid_range")
prod4b, new4b = PROD("Graham Beck Brut NV", "wine_sparkling", p4b, r4, "South Africa",
    subcategory="Méthode Cap Classique",
    description="South Africa's most celebrated sparkling wine — Chardonnay and Pinot Noir by traditional method, with lemon, brioche, green apple and persistent fine bubbles.",
    price_tier="mid_range")
if new4b:
    PAIR(prod4b, "Smoked salmon blinis with crème fraîche and chive", "complement", "classic", "aperitif", "Classic Champagne-method pairing; smoked fish and brioche notes align with the wine's toast character.")
    PAIR(prod4b, "Fried chicken with lemon and herb seasoning", "contrast", "established", "casual", "Bubbles and acidity cut through fried chicken fat; a celebratory contrast pairing.")
    PAIR(prod4b, "Cape Malay seafood curry (mild)", "bridge", "suggested", "main", "South African sparkling with traditional Cape Malay flavours; spice is bridged by the wine's acidity.")
    PAIR(prod4b, "Strawberry and cream pavlova", "complement", "classic", "dessert", "Sweet fruit dessert and Brut rosé is a classic; acidity prevents cloying sweetness.")

# ── Region 5: Elim ────────────────────────────────────────────────────────────
print("\n=== Region 5: Elim ===")
r5 = R("Elim", "South Africa", "wine",
    designation_type="WO",
    designation_name="Elim WO",
    reputation_tier="emerging",
    quality_trajectory="ascending",
    description="South Africa's southernmost wine ward at the tip of the Agulhas Plain, producing some of the country's most precise and cool-climate Sauvignon Blanc and Syrah under extreme Southern Ocean influence.",
    key_producers="Black Oystercatcher, Strandveld Vineyards, Luddite Wines",
    historical_context="Elim is South Africa's newest and southernmost wine region, established in the early 2000s, offering strikingly cool and precise wines unlike anything produced in the warmer Cape regions."
)
VIN(r5, 2022, "excellent", "rising", "Exceptional cool vintage; Sauvignon Blanc of extraordinary freshness and mineral precision.")
VIN(r5, 2021, "very_good", "stable", "Good Southern Ocean influence; wines show restraint and aromatic clarity.")
VIN(r5, 2020, "good", "stable", "Consistent quality; Sauvignon Blanc and Syrah both performed well.")
VIN(r5, 2019, "excellent", "rising", "Benchmark Elim vintage; wines of remarkable precision and mineral character.")
VIN(r5, 2018, "very_good", "stable", "Cold season with intense Southern Ocean influence; wines of exceptional delicacy and tension.")

p5a = P("Black Oystercatcher", "winery", r5, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="Elim's flagship producer named for the endangered African black oystercatcher, producing crisp Sauvignon Blanc and Shiraz from South Africa's windiest vineyards.",
    reputation_narrative="Black Oystercatcher Blanc Fumé is South Africa's most intriguing cool-climate Sauvignon Blanc, with a smoky, mineral character unlike any other Cape wine.",
    price_positioning="premium")
prod5a, new5a = PROD("Black Oystercatcher Blanc Fumé", "wine_still", p5a, r5, "South Africa",
    subcategory="Sauvignon Blanc",
    description="South Africa's southernmost Sauvignon Blanc — smoky flint, grapefruit, white asparagus and a piercing mineral finish with extreme ocean-influenced freshness.",
    price_tier="premium")
if new5a:
    PAIR(prod5a, "Oysters with lemon mignonette", "complement", "classic", "aperitif", "Flint minerality and ocean-influenced acidity are the perfect companion to fresh raw oysters.")
    PAIR(prod5a, "Grilled tiger prawns with lemon and herb butter", "complement", "established", "starter", "The wine's citrus and mineral notes amplify prawn sweetness; herb butter bridges both.")
    PAIR(prod5a, "Yellowtail sashimi with ponzu and pickled ginger", "complement", "established", "starter", "Cool-climate precision and saline mineral note align with delicate sashimi; ponzu mirrors the wine's acidity.")
    PAIR(prod5a, "Asparagus and Gruyère quiche", "complement", "suggested", "main", "Green asparagus and Sauvignon is a classic; Gruyère adds nutty richness to the pairing.")

p5b = P("Strandveld Vineyards", "winery", r5, "South Africa",
    production_philosophy="terroir_expression",
    philosophy_description="Pioneering Elim estate producing wines that express the unique character of South Africa's southernmost wine region — cooling Southern Ocean winds and ancient Agulhas Plain soils.",
    reputation_narrative="Strandveld's Adamastor white blend and Pofadder Cinsault have earned international recognition for their singular cool-climate Cape identity.",
    price_positioning="premium")
prod5b, new5b = PROD("Strandveld Adamastor", "wine_still", p5b, r5, "South Africa",
    subcategory="Sauvignon Blanc blend",
    description="Elim's signature white blend of Sauvignon Blanc, Sémillon and Viognier — floral, citrus, apricot and gravel minerality with textural complexity and ocean-driven precision.",
    price_tier="premium")
if new5b:
    PAIR(prod5b, "Steamed West Coast mussels with white wine and fennel", "complement", "established", "starter", "Local shellfish and the region's white blend is a terroir pairing; fennel echoes the wine's floral note.")
    PAIR(prod5b, "Crayfish bisque with cream and tarragon", "complement", "classic", "starter", "Rich coastal bisque aligns with the wine's texture; tarragon bridges its aromatic complexity.")
    PAIR(prod5b, "Seared Cape sole with brown butter and capers", "complement", "established", "fish_course", "Delicate fish and complex white blend is ideal; butter and capers mirror the wine's texture and acidity.")
    PAIR(prod5b, "Camembert with poached pear and walnut", "bridge", "suggested", "cheese", "Soft cheese with stone fruit bridges the wine's apricot and floral notes; walnut adds earthy depth.")

# ── Final count ───────────────────────────────────────────────────────────────
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
