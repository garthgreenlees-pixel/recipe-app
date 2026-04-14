#!/usr/bin/env python3
"""Terminal 4 — Batch 6: pairing_intelligence for all new products"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO pairing_intelligence
  (beverage_product_id, beverage_category, beverage_style,
   beverage_description, food_category, food_flavour_profile,
   food_description, pairing_type, flavour_logic, meal_context,
   confidence, confidence_rationale, authority_tier, source_text, is_published)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
RETURNING id"""

# Product IDs (from batch 3):
# 154 = Taki Mai Noble Kava Waka
# 161 = Del Maguey Vida Mezcal
# 171 = Fortaleza Blanco Tequila
# 172 = Buffalo Trace Kentucky Bourbon
# 173 = Uncle Nearest 1884
# 174 = Clairin Sajous
# 175 = Opus One 2019
# 176 = Ridge Monte Bello
# 177 = Penfolds Grange
# 178 = Henschke Hill of Grace
# 179 = Cloudy Bay Sauvignon Blanc
# 180 = Felton Road Block 3 Pinot Noir
# 181 = Catena Adrianna Fortuna Terrae Malbec
# 182 = Sadie Family Columella
# 183 = Macallan 12 Sherry Oak
# 184 = Ardbeg 10 Year Old
# 185 = Springbank 10 Year Old
# 186 = Cantillon Gueuze
# 187 = Weihenstephan Hefeweissbier
# 188 = Leitz Eins Zwei Zero Riesling
# 189 = Seedlip Spice 94
# 190 = GT's Synergy Gingerade Kombucha

PAIRINGS = [

# ============================================================
# KAVA
# ============================================================
{"beverage_product_id": 154, "beverage_category": "traditional_cultural", "beverage_style": "Noble kava — Waka grade, Fijian",
 "beverage_description": "Peppery, earthy, bitter, numbing — anxiolytic, muscle-relaxing",
 "food_category": "pre-ceremony", "food_flavour_profile": "light-neutral",
 "food_description": "Nothing — kava is best on an empty stomach; absorption is faster and cleaner",
 "pairing_type": "complement", "meal_context": "aperitif",
 "flavour_logic": "Kava is traditionally consumed without food — a full stomach slows kavalactone absorption significantly. If serving alongside food, very light preparations (raw vegetables, plain crackers) are less disruptive than rich or fatty foods.",
 "confidence": "classic", "confidence_rationale": "Traditional Pacific practice — kava is always consumed on an empty stomach for maximum effect",
 "authority_tier": 1, "source_text": "Lebot et al. — Kava: The Pacific Elixir (Yale, 1992)"},

{"beverage_product_id": 154, "beverage_category": "traditional_cultural", "beverage_style": "Noble kava",
 "beverage_description": "Earthy, peppery, numbing",
 "food_category": "Pacific Islander", "food_flavour_profile": "starchy-mild",
 "food_description": "Taro (poi, steamed), cassava, breadfruit — the Pacific staple starch family",
 "pairing_type": "bridge", "meal_context": "casual",
 "flavour_logic": "In Pacific cultures, kava is often followed (not accompanied) by a starchy meal. The earthy character of kava bridges naturally to the earthy, starchy character of taro. The bitterness of the kava is counterbalanced by the starchy mildness of poi.",
 "confidence": "established", "confidence_rationale": "Traditional Pacific post-nakamal food consumption",
 "authority_tier": 2, "source_text": "Tomlinson, M. — Ritual Textuality (Oxford, 2014)"},

{"beverage_product_id": 154, "beverage_category": "traditional_cultural", "beverage_style": "Noble kava",
 "beverage_description": "Earthy, peppery, bitter, numbing",
 "food_category": "seafood", "food_flavour_profile": "clean-ocean",
 "food_description": "Raw oysters, clams — shell-on, no sauce, pure ocean brine",
 "pairing_type": "contrast", "meal_context": "amuse",
 "flavour_logic": "The earthiness of kava contrasts cleanly with the pure ocean brine of raw shellfish. The numbing from kava actually heightens the perception of salinity and the cool temperature of raw shellfish. An experimental but sophisticated pairing.",
 "confidence": "adventurous", "confidence_rationale": "Cross-cultural contrast pairing — not traditional but logical flavour contrast",
 "authority_tier": 3, "source_text": "Original pairing logic — Provenance Development"},

# ============================================================
# MEZCAL
# ============================================================
{"beverage_product_id": 161, "beverage_category": "spirits_agave", "beverage_style": "Artesanal mezcal — espadín, pit-roasted",
 "beverage_description": "Campfire smoke, cooked agave, tropical fruit, green herb, mineral",
 "food_category": "grilled", "food_flavour_profile": "charred-smoky",
 "food_description": "Carne asada — charcoal-grilled skirt steak, Mexican spicing",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "Smoke meets smoke — the mesquite pit-roast smoke of mezcal bridges directly to the charcoal char on the carne asada. The agave sweetness lifts the charred meat character. The most instinctive mezcal pairing.",
 "confidence": "classic", "confidence_rationale": "Traditional Oaxacan pairing — mezcal and asado are culturally inseparable",
 "authority_tier": 1, "source_text": "Gaytán, M.S. — ¡Tequila! (Stanford, 2014)"},

{"beverage_product_id": 161, "beverage_category": "spirits_agave", "beverage_style": "Artesanal mezcal",
 "beverage_description": "Campfire smoke, cooked agave, mineral",
 "food_category": "vegetables", "food_flavour_profile": "charred-sweet",
 "food_description": "Elotes (Mexican street corn) — grilled, mayo, cotija cheese, chili, lime",
 "pairing_type": "elevate", "meal_context": "amuse",
 "flavour_logic": "The smoke of mezcal elevates the charred sweetness of grilled corn. Cotija's saltiness provides contrast to agave sweetness. The lime in elotes mirrors the citrus notes in the mezcal. One of the best cocktail food pairings in Mexican cuisine.",
 "confidence": "classic", "confidence_rationale": "Classic Oaxacan street food pairing",
 "authority_tier": 1, "source_text": "Traditional Oaxacan food culture"},

{"beverage_product_id": 161, "beverage_category": "spirits_agave", "beverage_style": "Artesanal mezcal",
 "beverage_description": "Campfire smoke, mineral, tropical fruit",
 "food_category": "chocolate", "food_flavour_profile": "dark-bitter",
 "food_description": "Oaxacan chocolate mole — dark, bitter, spiced, served with turkey or chicken",
 "pairing_type": "bridge", "meal_context": "main",
 "flavour_logic": "Mezcal and Oaxacan mole are from the same cultural tradition — the earthiness of the agave and the bitterness of the chocolate mole are a bridge pairing of extraordinary depth. Both carry the Zapotec flavour vocabulary of smoke, earth, and bitterness.",
 "confidence": "classic", "confidence_rationale": "Traditional Oaxacan cultural pairing — mole and mezcal share terroir",
 "authority_tier": 1, "source_text": "Oaxacan culinary tradition"},

{"beverage_product_id": 161, "beverage_category": "spirits_agave", "beverage_style": "Artesanal mezcal",
 "beverage_description": "Earthy smoke, green herb, mineral",
 "food_category": "fermented", "food_flavour_profile": "funky-sour",
 "food_description": "Chapulines (toasted grasshoppers) with lime and salt — the classic mezcal snack",
 "pairing_type": "complement", "meal_context": "casual",
 "flavour_logic": "Chapulines are the traditional accompaniment to mezcal in Oaxaca — the nutty, earthy, lime-acidic character of the grasshoppers complements the earthy smoke of the mezcal. This is the regional tradition that connects two indigenous protein and beverage sources.",
 "confidence": "classic", "confidence_rationale": "Traditional Oaxacan pairing of indigenous origin",
 "authority_tier": 1, "source_text": "Oaxacan culinary tradition"},

# ============================================================
# TEQUILA
# ============================================================
{"beverage_product_id": 171, "beverage_category": "spirits_agave", "beverage_style": "Traditional-method tequila blanco — tahona-ground",
 "beverage_description": "Cooked agave, citrus, white pepper, floral, herbal",
 "food_category": "seafood", "food_flavour_profile": "citrus-clean",
 "food_description": "Ceviche — Mexican-style, lime, serrano, cilantro, fresh white fish",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The citrus in both the Fortaleza Blanco and the ceviche creates an amplification pairing — lime in the ceviche mirrors lime in the tequila. The herbal agave character bridges to the cilantro. The white pepper in the tequila mirrors the serrano heat without competing.",
 "confidence": "classic", "confidence_rationale": "Classic Mexican cultural pairing — ceviche and tequila are culturally linked",
 "authority_tier": 1, "source_text": "Mexican culinary tradition"},

{"beverage_product_id": 171, "beverage_category": "spirits_agave", "beverage_style": "Tequila blanco — tahona",
 "beverage_description": "Agave sweet, citrus, mineral",
 "food_category": "cheese", "food_flavour_profile": "salty-fresh",
 "food_description": "Queso fresco — fresh Mexican cheese, mild, slightly salty, crumbly",
 "pairing_type": "contrast", "meal_context": "amuse",
 "flavour_logic": "The clean agave sweetness of Fortaleza Blanco contrasts effectively with the milky, lactic saltiness of queso fresco. The mineral character in the tequila bridges to the stone-like texture of the cheese. Both are expressions of Mexican terroir.",
 "confidence": "established", "confidence_rationale": "Established Mexican cheese and tequila pairing tradition",
 "authority_tier": 2, "source_text": "Mexican culinary tradition"},

# ============================================================
# BOURBON
# ============================================================
{"beverage_product_id": 172, "beverage_category": "spirits_whiskey", "beverage_style": "Kentucky Straight Bourbon — balanced sweet-spice",
 "beverage_description": "Vanilla, caramel, corn sweet, rye spice, oak",
 "food_category": "beef", "food_flavour_profile": "rich-fat",
 "food_description": "Dry-aged ribeye — simple preparation, coarse salt crust, full fat expression",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The caramelised vanilla character of bourbon mirrors the Maillard reaction products in a hard-seared ribeye. The rye spice cuts through the fat without over-competing. The corn sweetness amplifies the natural sweetness of dry-aged beef.",
 "confidence": "classic", "confidence_rationale": "Classic American bourbon and beef pairing — the most established in the category",
 "authority_tier": 1, "source_text": "Kentucky Bourbon Trail documentation; traditional American pairing culture"},

{"beverage_product_id": 172, "beverage_category": "spirits_whiskey", "beverage_style": "Bourbon",
 "beverage_description": "Vanilla, caramel, brown sugar, oak",
 "food_category": "sweet", "food_flavour_profile": "caramel-nutty",
 "food_description": "Pecan tart — brown sugar, butter, toasted pecans, caramel sauce",
 "pairing_type": "complement", "meal_context": "dessert",
 "flavour_logic": "The caramel and toasted nut flavours in a pecan tart are amplified by the caramelised oak character of the bourbon. Brown sugar in both creates a complementary resonance. The slight tannin in the bourbon prevents the sweetness from becoming cloying.",
 "confidence": "classic", "confidence_rationale": "Classic American dessert pairing — pecan pie and bourbon is a cultural institution",
 "authority_tier": 1, "source_text": "Southern American culinary tradition"},

{"beverage_product_id": 172, "beverage_category": "spirits_whiskey", "beverage_style": "Bourbon",
 "beverage_description": "Vanilla, caramel, gentle rye spice",
 "food_category": "cheese", "food_flavour_profile": "sharp-tangy",
 "food_description": "Aged white cheddar — 12-18 month, sharp, slightly crystalline",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "The caramel sweetness of bourbon softens the sharp acidity of aged cheddar. The subtle rye spice in Buffalo Trace matches the spicy lactic notes that develop in aged cheddar. A classic American pairing that needs no justification beyond how good it tastes.",
 "confidence": "classic", "confidence_rationale": "Classic American cheese and whiskey pairing",
 "authority_tier": 1, "source_text": "American culinary tradition"},

# ============================================================
# UNCLE NEAREST
# ============================================================
{"beverage_product_id": 173, "beverage_category": "spirits_whiskey", "beverage_style": "Tennessee Whiskey — smooth, maple-sweet",
 "beverage_description": "Vanilla, maple, honey, butterscotch, silky",
 "food_category": "pork", "food_flavour_profile": "smoky-sweet",
 "food_description": "Smoked pulled pork — slow-smoked over hickory, apple cider vinegar mop",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The maple-sweet character of Uncle Nearest 1884 bridges directly to hickory-smoked pork's natural sweetness. The Lincoln County Process produces a softness that prevents the whiskey from competing with smoke. The apple cider vinegar in the mop mirrors the fruit notes in the whiskey.",
 "confidence": "classic", "confidence_rationale": "Southern BBQ and Tennessee Whiskey is the defining regional pairing",
 "authority_tier": 1, "source_text": "Southern American culinary tradition"},

{"beverage_product_id": 173, "beverage_category": "spirits_whiskey", "beverage_style": "Tennessee Whiskey",
 "beverage_description": "Honey, vanilla, maple, dried fruit",
 "food_category": "dessert", "food_flavour_profile": "banana-warm",
 "food_description": "Banana pudding — Southern-style, vanilla wafers, whipped cream, caramelised banana",
 "pairing_type": "complement", "meal_context": "dessert",
 "flavour_logic": "The vanilla and caramelised banana notes in Southern banana pudding create a complementary resonance with Uncle Nearest's vanilla-maple profile. The Lincoln County Process smoothness means the whiskey sits alongside the dessert rather than competing with it.",
 "confidence": "established", "confidence_rationale": "Southern dessert and Tennessee Whiskey pairing tradition",
 "authority_tier": 2, "source_text": "Southern American culinary tradition"},

# ============================================================
# CLAIRIN
# ============================================================
{"beverage_product_id": 174, "beverage_category": "spirits_rum", "beverage_style": "Haitian clairin — unaged, terroir-driven cane spirit",
 "beverage_description": "Sugarcane fresh, citrus, green herb, mineral, tropical fruit",
 "food_category": "Haitian", "food_flavour_profile": "spiced-savory",
 "food_description": "Griot — Haitian fried pork marinated in citrus and scotch bonnet, served with pikliz (spiced cabbage slaw)",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "Clairin and griot are Haiti's national pairing — the fresh citrus in both the clairin and the griot marinade creates complementary resonance. The scotch bonnet heat is moderated by the clairin's mineral freshness. This is the cultural pairing, the one that exists before any analytical framework.",
 "confidence": "classic", "confidence_rationale": "Traditional Haitian cultural pairing",
 "authority_tier": 1, "source_text": "Haitian culinary tradition; Velier documentation"},

{"beverage_product_id": 174, "beverage_category": "spirits_rum", "beverage_style": "Clairin",
 "beverage_description": "Cane juice fresh, citrus, mineral",
 "food_category": "tropical fruit", "food_flavour_profile": "tropical-sweet",
 "food_description": "Akasan — Haitian corn porridge with cinnamon, vanilla, and star anise",
 "pairing_type": "bridge", "meal_context": "casual",
 "flavour_logic": "The warmth of cinnamon and star anise in akasan bridges to the herbaceous-mineral character of clairin. The corn character in akasan echoes the grain-like quality of raw sugarcane. A culturally authentic Haitian beverage-food bridge.",
 "confidence": "established", "confidence_rationale": "Haitian cultural tradition",
 "authority_tier": 2, "source_text": "Haitian culinary tradition"},

# ============================================================
# OPUS ONE
# ============================================================
{"beverage_product_id": 175, "beverage_category": "wine_still", "beverage_style": "Napa Bordeaux blend — Cabernet dominant",
 "beverage_description": "Cassis, blackcurrant, cedar, graphite, dark chocolate, violets",
 "food_category": "beef", "food_flavour_profile": "rich-mineral",
 "food_description": "Prime rib — slow-roasted, rare, natural jus, Yorkshire pudding",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The deep cassis and graphite character of Opus One complements the mineral richness of prime rib. The fine-grained tannins grip the protein of the rare beef, bridging the wine's structure to the meat's texture. The natural jus's umami amplifies the wine's fruit depth.",
 "confidence": "classic", "confidence_rationale": "Classic Bordeaux-style red wine and prime rib pairing",
 "authority_tier": 1, "source_text": "Napa Valley Vintners culinary pairing documentation"},

{"beverage_product_id": 175, "beverage_category": "wine_still", "beverage_style": "Napa Cabernet blend",
 "beverage_description": "Blackcurrant, cedar, chocolate, graphite",
 "food_category": "lamb", "food_flavour_profile": "herbal-rich",
 "food_description": "Rack of lamb — herb crust (rosemary, thyme), garlic, lamb jus, roasted root vegetables",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The herbal character of the lamb's crust (rosemary, thyme) creates a botanical bridge to the cedar and graphite of Opus One. The lamb fat's richness is gripped by the structured tannins. The violets in the wine mirror the lavender-like quality of rosemary at the edge of perception.",
 "confidence": "classic", "confidence_rationale": "Classic Bordeaux/Napa Cabernet and lamb pairing",
 "authority_tier": 1, "source_text": "Wine and food pairing tradition"},

# ============================================================
# RIDGE MONTE BELLO
# ============================================================
{"beverage_product_id": 176, "beverage_category": "wine_still", "beverage_style": "California Cabernet — mountain mineral, age-worthy",
 "beverage_description": "Cassis, mineral, eucalyptus, chalk, iron, cedar",
 "food_category": "game", "food_flavour_profile": "mineral-herbal",
 "food_description": "Venison loin — seared, blackberry reduction, wild thyme, roasted beetroot",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "Ridge Monte Bello's mineral-iron character resonates powerfully with venison — both carry iron-mineral character from their respective sources (mountain soils, game muscle). The blackberry reduction bridges the wine's cassis. The chalky mineral character provides structure to carry the beetroot's earthiness.",
 "confidence": "established", "confidence_rationale": "Mountain Cabernet and game pairing — the mineral-iron parallel is the key logic",
 "authority_tier": 1, "source_text": "Ridge Vineyards pairing documentation"},

# ============================================================
# PENFOLDS GRANGE
# ============================================================
{"beverage_product_id": 177, "beverage_category": "wine_still", "beverage_style": "Australian Shiraz — massive, powerful, old vine Barossa",
 "beverage_description": "Blackberry, blueberry, dark chocolate, American oak, iron, leather",
 "food_category": "lamb", "food_flavour_profile": "rich-gamey",
 "food_description": "Slow-roasted lamb shoulder — 6-hour, Middle Eastern spices (sumac, cumin, coriander), pomegranate molasses",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "Grange's enormous concentration and dark fruit need a preparation of equal weight. The slow-roasted lamb shoulder at 6 hours develops the fat-rendered richness to support Grange's power. Pomegranate molasses bridges to Grange's plum-dark fruit. This is Garth's personal pairing memory from working with Australian lamb.",
 "confidence": "classic", "confidence_rationale": "Classic Australian Shiraz and lamb pairing — culturally inseparable",
 "authority_tier": 1, "source_text": "Penfolds pairing documentation; Australian culinary tradition"},

{"beverage_product_id": 177, "beverage_category": "wine_still", "beverage_style": "Barossa old vine Shiraz",
 "beverage_description": "Blackberry, chocolate, leather, American oak vanilla",
 "food_category": "cheese", "food_flavour_profile": "washed-pungent",
 "food_description": "Aged washed-rind Australian cheese (Milawa Gold, or similar) — pungent, buttery, semi-soft",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "The power of Grange requires equally powerful cheese — a mild cheese is overwhelmed. Washed-rind's pungency and umami depth match Grange's concentration. The American oak vanilla in the wine softens the cheese's ammonia character. Australian wine with Australian cheese is the cultural bridge.",
 "confidence": "established", "confidence_rationale": "Australian artisan cheese and Australian wine pairing logic",
 "authority_tier": 2, "source_text": "Australian cheese and wine pairing tradition"},

# ============================================================
# CLOUDY BAY SAUVIGNON BLANC
# ============================================================
{"beverage_product_id": 179, "beverage_category": "wine_still", "beverage_style": "Marlborough Sauvignon Blanc — pungent, herbaceous",
 "beverage_description": "Passion fruit, grapefruit, capsicum, lemongrass, crisp acid",
 "food_category": "seafood", "food_flavour_profile": "briny-clean",
 "food_description": "Pacific oysters — freshly shucked, no garnish, pure ocean brine, Fanny Bay or Tofino",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The high acid and citrus of Marlborough Sauvignon Blanc mirrors the saline acidity of a Pacific oyster. The lemongrass and citrus in the wine brings out the sweetness of the oyster flesh. The capsicum/green herb character bridges to the slight iodine of the shell. The BC oyster and NZ wine combination is a Pacific Rim expression — both flavours derived from cold Pacific waters.",
 "confidence": "classic", "confidence_rationale": "Classic Sauvignon Blanc and oyster pairing — universally recognised",
 "authority_tier": 1, "source_text": "Wine and food pairing tradition; NZ Winegrowers documentation"},

{"beverage_product_id": 179, "beverage_category": "wine_still", "beverage_style": "Marlborough Sauvignon Blanc",
 "beverage_description": "Passion fruit, citrus, capsicum, herbaceous",
 "food_category": "Asian", "food_flavour_profile": "bright-herbal",
 "food_description": "Vietnamese fresh spring rolls — rice paper, prawn, mint, coriander, lime dipping sauce",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The herbaceous-citrus character of Sauvignon Blanc is one of the most effective bridges to South-East Asian cuisine. The mint and coriander in Vietnamese spring rolls amplify the wine's own herbal thiols. The lime dipping sauce mirrors the wine's citrus. The prawn's sweetness contrasts cleanly with the wine's acidity.",
 "confidence": "established", "confidence_rationale": "Established Sauvignon Blanc and Vietnamese cuisine pairing",
 "authority_tier": 1, "source_text": "Wine and food pairing tradition"},

{"beverage_product_id": 179, "beverage_category": "wine_still", "beverage_style": "Marlborough Sauvignon Blanc",
 "beverage_description": "Passion fruit, grapefruit, clean acid",
 "food_category": "cheese", "food_flavour_profile": "goat-tangy",
 "food_description": "Chèvre frais — fresh goat cheese, possibly with lemon and herbs",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "The Loire classic — Sancerre with chèvre — is replicated in the New World by Marlborough Sauvignon Blanc with fresh goat cheese. The wine's grapefruit acidity balances the lactic tang of the cheese. Both have a mineralness derived from their respective terroirs. Classic and reliable.",
 "confidence": "classic", "confidence_rationale": "Classic Sauvignon Blanc and chèvre pairing — the Loire/NZ parallel",
 "authority_tier": 1, "source_text": "Wine and food pairing tradition"},

{"beverage_product_id": 179, "beverage_category": "wine_still", "beverage_style": "Marlborough Sauvignon Blanc",
 "beverage_description": "Herbaceous, citrus, passion fruit",
 "food_category": "salmon", "food_flavour_profile": "salmon-rich",
 "food_description": "Pacific salmon sashimi — Pacific sockeye, soy, wasabi, pickled ginger",
 "pairing_type": "complement", "meal_context": "fish_course",
 "flavour_logic": "The citrus-herbaceous character of Cloudy Bay navigates the rich fat of Pacific sockeye without overpowering it. The wine's acidity cuts through the salmon's fat in the same way soy-citrus does in the Japanese tradition. The ginger amplifies the lemongrass notes in the wine.",
 "confidence": "established", "confidence_rationale": "Pacific salmon and NZ Sauvignon Blanc — Pacific Rim pairing logic",
 "authority_tier": 1, "source_text": "Pacific Rim cuisine pairing tradition"},

# ============================================================
# FELTON ROAD PINOT NOIR
# ============================================================
{"beverage_product_id": 180, "beverage_category": "wine_still", "beverage_style": "Central Otago Pinot Noir — schist mineral, whole bunch spice",
 "beverage_description": "Dark cherry, forest floor, schist mineral, five-spice, silky tannins",
 "food_category": "duck", "food_flavour_profile": "rich-gamey",
 "food_description": "Duck breast — seared skin-on, five-spice rub, cherry reduction, wilted greens",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The five-spice in the duck preparation mirrors the whole-bunch five-spice character in the Felton Road Block 3 — this is a textbook bridge pairing. The cherry reduction amplifies the wine's cherry fruit. The duck fat's richness is gripped by the silky but present tannins. One of the great modern NZ wine and food pairings.",
 "confidence": "classic", "confidence_rationale": "Central Otago Pinot Noir and duck pairing — consistent benchmark",
 "authority_tier": 1, "source_text": "Felton Road pairing documentation; NZ culinary tradition"},

{"beverage_product_id": 180, "beverage_category": "wine_still", "beverage_style": "Central Otago Pinot Noir",
 "beverage_description": "Dark cherry, forest floor, mineral, spice",
 "food_category": "venison", "food_flavour_profile": "gamey-mineral",
 "food_description": "New Zealand venison medallions — pan-seared, manuka honey and thyme jus, roasted kumara",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "New Zealand venison and Central Otago Pinot Noir is a national identity pairing — both products of the same alpine environment. The mineral-iron character of the venison resonates with the schist mineral in the wine. The manuka honey in the jus bridges to the slight floral sweetness in the wine's fruit.",
 "confidence": "classic", "confidence_rationale": "NZ venison and Central Otago Pinot — national identity pairing",
 "authority_tier": 1, "source_text": "New Zealand culinary and wine tradition"},

{"beverage_product_id": 180, "beverage_category": "wine_still", "beverage_style": "Central Otago Pinot Noir",
 "beverage_description": "Cherry, mineral, forest floor, silky",
 "food_category": "salmon", "food_flavour_profile": "rich-mineral",
 "food_description": "Ora King salmon — lightly cured, dill oil, cucumber, preserved lemon",
 "pairing_type": "complement", "meal_context": "fish_course",
 "flavour_logic": "Ora King salmon (Marlborough farmed king salmon — world's highest Omega-3 content) has the fat richness to support Pinot Noir's structure. The dill and cucumber bring a fresh green note that mirrors the wine's herbal character from whole-bunch inclusion. Preserved lemon amplifies the wine's citrus edge.",
 "confidence": "established", "confidence_rationale": "NZ wine with NZ premium salmon — terroir coherence pairing",
 "authority_tier": 1, "source_text": "NZ culinary and wine tradition"},

# ============================================================
# MACALLAN 12 SHERRY OAK
# ============================================================
{"beverage_product_id": 183, "beverage_category": "spirits_whiskey", "beverage_style": "Speyside single malt — sherry-matured, full, fruit-forward",
 "beverage_description": "Dried fruit, orange peel, Christmas cake, chocolate, nutmeg, ginger spice",
 "food_category": "chocolate", "food_flavour_profile": "dark-complex",
 "food_description": "Valrhona dark chocolate (70%) — sea salt flake, single origin",
 "pairing_type": "complement", "meal_context": "digestif",
 "flavour_logic": "The chocolate and orange character of Macallan 12 Sherry Oak creates a direct bridge to dark chocolate — both are dried fruit and cocoa expressions. The sea salt on the chocolate amplifies the mineral character of the whisky. At 70% cacao the chocolate retains sufficient bitterness to contrast with the whisky's sweetness.",
 "confidence": "classic", "confidence_rationale": "Classic Speyside single malt and dark chocolate pairing",
 "authority_tier": 1, "source_text": "Whisky and food pairing tradition; Macallan documentation"},

{"beverage_product_id": 183, "beverage_category": "spirits_whiskey", "beverage_style": "Sherry-matured Speyside",
 "beverage_description": "Christmas cake, dried fruit, orange, spice",
 "food_category": "cheese", "food_flavour_profile": "blue-rich",
 "food_description": "Stilton — traditional British blue cheese, creamy, intense, complex",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "The sherry-matured dried fruit and orange peel in Macallan 12 creates a perfect contrast-complement with Stilton's salt-cream-blue intensity. The salt of the Stilton amplifies the whisky's fruit sweetness. The cream fat is gripped by the whisky's structure. The classic British cheese and whisky pairing.",
 "confidence": "classic", "confidence_rationale": "Classic British Stilton and single malt pairing",
 "authority_tier": 1, "source_text": "British food and whisky tradition"},

# ============================================================
# ARDBEG 10
# ============================================================
{"beverage_product_id": 184, "beverage_category": "spirits_whiskey", "beverage_style": "Islay single malt — heavily peated, medicinal, iodine",
 "beverage_description": "Peat smoke, iodine, seaweed, medicinal, vanilla underneath, honey",
 "food_category": "seafood", "food_flavour_profile": "smoked-briny",
 "food_description": "Hot smoked salmon — natural wood smoke, salmon oil, barely cooked, crème fraîche and dill",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The fundamental pairing logic for Ardbeg: smoke meets smoke. The peat smoke of Islay whisky bridges directly to wood-smoked salmon — both carry phenolic smoke compounds that resonate. The iodine-seaweed character mirrors the ocean flavor of salmon. The vanilla underneath the Ardbeg softens the smoky amplitude.",
 "confidence": "classic", "confidence_rationale": "Classic Islay whisky and smoked fish pairing — the most instinctive expression",
 "authority_tier": 1, "source_text": "Scottish culinary tradition; Ardbeg pairing documentation"},

{"beverage_product_id": 184, "beverage_category": "spirits_whiskey", "beverage_style": "Islay heavily peated",
 "beverage_description": "Iodine, seaweed, smoke, vanilla",
 "food_category": "seafood", "food_flavour_profile": "briny-mineral",
 "food_description": "Smoked oysters — wood-smoked Pacific oysters, served warm with bread",
 "pairing_type": "complement", "meal_context": "amuse",
 "flavour_logic": "Islay whisky and smoked oysters is the most Scottish of all food pairings — the peat smoke and iodine of the whisky amplify the sea-smoke character of the oyster. The vanilla underneath the Ardbeg prevents the pairing from becoming overwhelming. One shell, one small measure — a perfect pre-dinner amuse.",
 "confidence": "classic", "confidence_rationale": "Traditional Scottish pairing — Islay whisky with smoked shellfish",
 "authority_tier": 1, "source_text": "Scottish culinary tradition"},

{"beverage_product_id": 184, "beverage_category": "spirits_whiskey", "beverage_style": "Ardbeg — medicinal smoke",
 "beverage_description": "Peat, iodine, seaweed, vanilla",
 "food_category": "cheese", "food_flavour_profile": "aged-crystalline",
 "food_description": "24-month Parmigiano-Reggiano — hard, crystalline, umami-rich, slightly caramelised",
 "pairing_type": "contrast", "meal_context": "cheese",
 "flavour_logic": "The smoke of Ardbeg contrasts boldly with the crystalline, caramelised umami of aged Parmigiano. The salt crystals in the cheese amplify the vanilla sweetness under the smoke. An unexpected but powerful pairing — the cheese's 24-month caramelisation creates enough weight to support the whisky's intensity.",
 "confidence": "adventurous", "confidence_rationale": "Non-traditional pairing — Islay whisky with Italian hard cheese",
 "authority_tier": 2, "source_text": "Whisky and cheese pairing tradition"},

# ============================================================
# SPRINGBANK 10
# ============================================================
{"beverage_product_id": 185, "beverage_category": "spirits_whiskey", "beverage_style": "Campbeltown single malt — saline, briny, orchard fruit",
 "beverage_description": "Sea salt, brine, orchard fruit, slight peat, vanilla",
 "food_category": "seafood", "food_flavour_profile": "oceanic-mineral",
 "food_description": "Scottish kippers — traditionally smoked herring, served with brown bread and butter",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The saline, briny character of Springbank is the most direct expression of its coastal Campbeltown origin. Kippers — the most coastal of all smoked fish preparations — share this saline-smoky character. The orchard fruit in the whisky provides contrast to the oily richness of the herring.",
 "confidence": "classic", "confidence_rationale": "Traditional Scottish coastal pairing",
 "authority_tier": 1, "source_text": "Scottish culinary tradition; Springbank Distillery documentation"},

{"beverage_product_id": 185, "beverage_category": "spirits_whiskey", "beverage_style": "Campbeltown single malt",
 "beverage_description": "Sea salt, brine, light orchard, vanilla",
 "food_category": "butter", "food_flavour_profile": "rich-salt",
 "food_description": "Cultured butter with sea salt — on rye crispbread or sourdough",
 "pairing_type": "complement", "meal_context": "amuse",
 "flavour_logic": "The saline character of Springbank complements the salt in cultured butter — both are expressions of sea and land. The slight acidity of cultured butter (lactic fermentation) bridges to the whisky's complex background fermentation character. Simple but precise.",
 "confidence": "established", "confidence_rationale": "Sea salt and briny whisky complement pairing",
 "authority_tier": 2, "source_text": "Whisky and food pairing tradition"},

# ============================================================
# CANTILLON GUEUZE
# ============================================================
{"beverage_product_id": 186, "beverage_category": "beer_wild", "beverage_style": "Traditional gueuze lambic — spontaneous fermentation, aged, dry",
 "beverage_description": "Lemon, hay, Brett funk, apple, tart acid, mineral, dry",
 "food_category": "shellfish", "food_flavour_profile": "briny-clean",
 "food_description": "Moules marinières — steamed mussels, white wine, shallots, cream, parsley",
 "pairing_type": "complement", "meal_context": "main",
 "flavour_logic": "The acid-driven, dry, lemon-mineral character of gueuze is one of the most effective beverage matches for mussels — as effective as the white wine traditionally cooked with them. The Brett-hay character of the gueuze bridges to the briny, oceanic quality of the mussel liquor. This is the classic Flemish pairing.",
 "confidence": "classic", "confidence_rationale": "Classic Belgian moules-gueuze pairing — traditional Flemish food culture",
 "authority_tier": 1, "source_text": "Belgian culinary tradition; Cantillon documentation"},

{"beverage_product_id": 186, "beverage_category": "beer_wild", "beverage_style": "Gueuze lambic",
 "beverage_description": "Tart, dry, lemon, hay, funky",
 "food_category": "cheese", "food_flavour_profile": "aged-hard",
 "food_description": "Aged Gouda (36-month) — sweet-caramel-crystalline, complex, significant umami",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "Aged Gouda's caramel sweetness provides a counterpoint to gueuze's extreme dryness and acidity. The cheese's crystalline umami depth matches the Brett complexity of the gueuze. The salt crystals in the cheese amplify the whisky's mineral character.",
 "confidence": "classic", "confidence_rationale": "Classic Belgian gueuze and aged Gouda pairing",
 "authority_tier": 1, "source_text": "Belgian culinary tradition"},

{"beverage_product_id": 186, "beverage_category": "beer_wild", "beverage_style": "Gueuze lambic",
 "beverage_description": "Lemon, tart acid, hay, mineral",
 "food_category": "charcuterie", "food_flavour_profile": "fermented-rich",
 "food_description": "Flemish carbonnade — beef braised in gueuze/lambic, thyme, bay, brown sugar",
 "pairing_type": "bridge", "meal_context": "main",
 "flavour_logic": "Drinking the same liquid used in cooking creates the ultimate bridge pairing. Carbonnade traditionally uses lambic or gueuze in the braise — the residual Brett characters in the dish are amplified by drinking Cantillon alongside. The brown sugar in the carbonnade contrasts with the gueuze's dryness.",
 "confidence": "classic", "confidence_rationale": "Traditional Flemish pairing — the beverage IS in the dish",
 "authority_tier": 1, "source_text": "Traditional Belgian culinary culture"},

# ============================================================
# WEIHENSTEPHAN HEFEWEIZEN
# ============================================================
{"beverage_product_id": 187, "beverage_category": "beer_ale", "beverage_style": "Bavarian Hefeweizen — banana-clove, cloudy",
 "beverage_description": "Banana, clove, bubblegum, wheat, gentle citrus, refreshing",
 "food_category": "sausage", "food_flavour_profile": "herbal-mild",
 "food_description": "Weisswurst — Bavarian white veal sausage, lightly poached, served with sweet mustard and pretzel",
 "pairing_type": "complement", "meal_context": "casual",
 "flavour_logic": "The defining Bavarian pairing — Weihenstephan and Weisswurst. The banana and clove of the Hefeweizen bridge to the subtle veal sweetness and the white pepper in the sausage. The gentle carbonation cleanses between bites. Sweet mustard amplifies the banana ester in the beer.",
 "confidence": "classic", "confidence_rationale": "Traditional Bavarian cultural pairing — inseparable",
 "authority_tier": 1, "source_text": "Bavarian culinary tradition; Weihenstephan documentation"},

{"beverage_product_id": 187, "beverage_category": "beer_ale", "beverage_style": "Hefeweizen",
 "beverage_description": "Banana, clove, wheat, refreshing",
 "food_category": "fish", "food_flavour_profile": "delicate-fried",
 "food_description": "Fish and chips — light beer batter, mild white fish (halibut or cod), malt vinegar",
 "pairing_type": "cleanse", "meal_context": "casual",
 "flavour_logic": "The high carbonation and refreshing acidity of Hefeweizen cuts through the fat of beer-battered fish. The banana ester bridges to the sweetness of the white fish. The wheat malt is a natural pairing with wheat-flour batter. The malt vinegar on the chips mirrors the slight acidic twang of the Hefeweizen.",
 "confidence": "established", "confidence_rationale": "Hefeweizen and fish pairing — refreshing carbonation cuts fat",
 "authority_tier": 2, "source_text": "Beer and food pairing tradition"},

# ============================================================
# LEITZ NA RIESLING
# ============================================================
{"beverage_product_id": 188, "beverage_category": "na_dealcoholised", "beverage_style": "Dealcoholised Riesling — mineral, citrus",
 "beverage_description": "Citrus, slate mineral, lime, apple, white peach",
 "food_category": "seafood", "food_flavour_profile": "briny-delicate",
 "food_description": "Pacific Dungeness crab — poached, cold, with aioli and lemon",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The citrus-mineral character of Leitz Riesling EZZ pairs with Dungeness crab in exactly the same way the alcoholic Riesling would — the acidity bridges the sweetness of the crab, the mineral character provides structure. The pairing logic is identical to the alcoholic version. The guest choosing non-alcoholic deserves this insight: the experience is genuinely equivalent to a Mosel Riesling with crab.",
 "confidence": "established", "confidence_rationale": "NA Riesling and Dungeness crab — pairing logic identical to alcoholic Riesling",
 "authority_tier": 1, "source_text": "Provenance pairing development; Leitz Eins Zwei Zero documentation"},

{"beverage_product_id": 188, "beverage_category": "na_dealcoholised", "beverage_style": "Dealcoholised Riesling",
 "beverage_description": "Citrus, mineral, fresh apple",
 "food_category": "Asian", "food_flavour_profile": "spiced-aromatic",
 "food_description": "Thai green curry — coconut, lemongrass, Thai basil, kaffir lime, moderate heat",
 "pairing_type": "cleanse", "meal_context": "main",
 "flavour_logic": "The high residual sweetness and acid of a dealcoholised Riesling moderates spice heat effectively — the sugar provides heat relief while the acidity refreshes. The lemongrass in the curry mirrors the lemongrass-citrus in the Leitz. No alcohol means no alcohol-heat amplification of the spice.",
 "confidence": "established", "confidence_rationale": "Riesling and Thai curry pairing — the NA version is arguably better than the alcoholic for spice moderation",
 "authority_tier": 1, "source_text": "Wine and Asian food pairing tradition; NA programme development"},

# ============================================================
# SEEDLIP
# ============================================================
{"beverage_product_id": 189, "beverage_category": "na_crafted", "beverage_style": "Distilled NA spirit — botanical-spiced, gin-like",
 "beverage_description": "Allspice, cardamom, oak bark, citrus peel, warm spice, dry bitter",
 "food_category": "aperitif food", "food_flavour_profile": "salty-crisp",
 "food_description": "Spiced nuts — cashews, almonds, rosemary, cayenne, sea salt",
 "pairing_type": "complement", "meal_context": "aperitif",
 "flavour_logic": "The warm spice and cardamom of Seedlip Spice 94 bridges directly to spiced nuts. The salt amplifies the oak bark character of the distillate. The cayenne heat mirrors the pepper notes in the allspice. This is the perfect aperitif pairing for the NA guest — complex, satisfying, and genuinely food-appropriate.",
 "confidence": "established", "confidence_rationale": "Botanical NA spirit and spiced nuts — complementary spice profile",
 "authority_tier": 2, "source_text": "Seedlip pairing documentation"},

# ============================================================
# KOMBUCHA
# ============================================================
{"beverage_product_id": 190, "beverage_category": "na_fermented", "beverage_style": "Raw kombucha — ginger, tart, live cultures",
 "beverage_description": "Ginger, acetic acid, tea, apple, effervescent",
 "food_category": "sushi", "food_flavour_profile": "clean-umami",
 "food_description": "Sashimi selection — Pacific salmon, Albacore tuna, halibut, pickled ginger",
 "pairing_type": "complement", "meal_context": "starter",
 "flavour_logic": "The ginger-acid character of GT's Synergy Gingerade is structurally similar to the pickled ginger served alongside sashimi — both are acidic ginger preparations that refresh the palate between bites of raw fish. The live culture acid of kombucha bridges to the clean umami of sashimi grade fish without competing.",
 "confidence": "established", "confidence_rationale": "Ginger kombucha and sashimi — the ginger-acid bridge to Japanese fish culture",
 "authority_tier": 2, "source_text": "NA programme development; Pacific Rim food pairing tradition"},

{"beverage_product_id": 190, "beverage_category": "na_fermented", "beverage_style": "Kombucha — ginger, acidic",
 "beverage_description": "Ginger, tart, apple cider vinegar, tea, effervescent",
 "food_category": "cheese", "food_flavour_profile": "soft-mild",
 "food_description": "Brie de Meaux — ripe, oozy, earthy rind, gentle mushroom character",
 "pairing_type": "complement", "meal_context": "cheese",
 "flavour_logic": "The acetic-lactic acid character of kombucha bridges to the lactic richness of Brie in the same way that a sour beer bridges to soft French cheese. The ginger provides enough spice to contrast with the cream fat. The effervescence refreshes the palate between bites. An elegant NA cheese pairing.",
 "confidence": "suggested", "confidence_rationale": "NA cheese pairing — kombucha acid and Brie cream are a compatible pairing",
 "authority_tier": 3, "source_text": "Provenance pairing development"},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for p in PAIRINGS:
        try:
            cur.execute(SQL, (
                p["beverage_product_id"], p["beverage_category"],
                p.get("beverage_style"), p.get("beverage_description"),
                p.get("food_category"), p.get("food_flavour_profile"),
                p.get("food_description"), p["pairing_type"],
                p["flavour_logic"], p.get("meal_context"),
                p["confidence"], p.get("confidence_rationale"),
                p.get("authority_tier"), p.get("source_text"), True
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT pairing id={row[0]}: bev={p['beverage_product_id']} + {p['food_description'][:50]}")
                inserted += 1
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR bev={p['beverage_product_id']}: {e}")
    print(f"\nDone. {inserted} pairings inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
