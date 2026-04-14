#!/usr/bin/env python3
"""Terminal 4 — Batch 3: beverage_products for all new regions"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO beverage_products
  (name, category, subcategory, producer_id, region_id, origin_country,
   description, quality_tier, quality_hierarchy, deductive_profile,
   service_specs, flavour_markers, flavour_weight, flavour_profile_type,
   origin_brand, price_tier, price_range_cad, technical_specs, is_published, slug)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING RETURNING id, name"""

# Producer IDs: 150=Fiji Kava Ltd, 151=Taki Mai, 152=Bula Kava House
# 153=Kona Kava Farm, 154=Lakan Lambanog, 155=Clairin Sajous
# 156=Clairin Vaval, 157=Uncle Nearest, 158=Buffalo Trace, 159=Maker's Mark
# 160=YCFCU, 161=SCFCU, 162=OCFCU, 163=49th Parallel
# 164=Opus One, 165=Stag's Leap, 166=Williams Selyem, 167=Ridge
# 168=Penfolds, 169=Henschke, 170=Giant Steps
# 171=Cloudy Bay, 172=Felton Road, 173=Catena Zapata, 174=Concha y Toro
# 175=Sadie Family, 176=Mullineux, 177=Kanonkop
# 178=Macallan, 179=Ardbeg, 180=Springbank, 181=Laphroaig
# 182=Del Maguey, 183=Fortaleza, 184=Cantillon, 185=Weihenstephan, 186=3 Fonteinen

PRODUCTS = [

# ============================================================
# KAVA / PACIFIC
# ============================================================
{
  "name": "Taki Mai Noble Kava — Waka Premium",
  "category": "traditional_cultural",
  "subcategory": "kava_noble",
  "producer_id": 151,
  "region_id": 69,
  "origin_country": "Fiji",
  "description": "Premium Fijian Noble kava — Waka (lateral root) grade, the highest kavalactone content of any part of the kava plant. Traditionally prepared: ground root mixed with cold water (not hot — heat degrades kavalactones), strained through muslin or kava cloth, consumed fresh. The Waka grade produces a drink that is powerfully sedating and anxiolytic: significant leg and facial numbness within 15 minutes, muscle relaxation, sensory calm. NOT alcoholic. NOT hallucinogenic. A distinct pharmacological category.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "Waka (lateral root — highest kavalactone)", "position": 1}, {"label": "Lawena (basal stump — medium)", "position": 2}, {"label": "Kasa (aerial stem — weakest)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Light grey-tan", "clarity": "Opaque, cloudy", "aroma": "Earthy, peppery, dusty, slight floral", "flavour": "Bitter, astringent, numbing, earthy, pepper, slight sweetness in fresh kava", "texture": "Slightly thick, oily", "finish": "Prolonged numbness in lips and tongue, dry earthy aftertaste"}),
  "service_specs": json.dumps({"vessel": "Coconut shell half (bilo)", "temp_c": "Room temperature — never hot", "preparation": "60-80g ground root per litre cold water, 10 min kneading in cloth, strain thoroughly", "serving_size_ml": 150, "etiquette": "Receive with both hands, clap once, drink in one go (grog it), clap three times", "session_structure": "Served in rounds — declining a shell requires covering with palm of hand"}),
  "flavour_markers": ["pepper", "earth", "bitter", "numbing", "dusty", "floral-subtle"],
  "flavour_weight": "medium",
  "flavour_profile_type": "earthy-bitter",
  "origin_brand": "Taki Mai",
  "price_tier": "premium",
  "price_range_cad": "$45-65 / 500g",
  "technical_specs": json.dumps({"kavalactone_pct": ">5.5", "variety": "Waka (lateral root)", "abv_pct": 0, "active_compounds": ["kavain", "dihydrokavain", "yangonin", "desmethoxyyangonin", "methysticin", "dihydromethysticin"], "pharmacology": "GABA-ergic, anxiolytic, muscle relaxant — non-addictive at traditional doses"}),
  "slug": "taki-mai-noble-kava-waka"
},
{
  "name": "Del Maguey Vida Mezcal",
  "category": "spirits_agave",
  "subcategory": "mezcal_artesanal",
  "producer_id": 182,
  "region_id": 99,
  "origin_country": "Mexico",
  "description": "Del Maguey's entry-level single-village mezcal — made from cultivated espadín (Agave angustifolia) in San Luis del Rio, Oaxaca. Traditional production: earthen pit roast with mesquite wood (3-4 days), stone milling (tahona), open wooden fermentation vat (wild yeast, 7-10 days), copper pot still double distillation. Vida is the accessible introduction to authentic single-village mezcal — demonstrating the smoke-fruit-mineral complexity that no industrial spirit can produce.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "Vida (espadín, accessible)", "position": 1}, {"label": "San Luis del Rio (espadín, complex — Ron Cooper's flagship)", "position": 2}, {"label": "Tobalá (wild agave — very limited, expensive)", "position": 3}, {"label": "Pechuga (triple-distilled with seasonal fruits and fowl)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Crystal clear", "aroma": "Smoke, charcoal, tropical fruit (banana, pineapple), green herb, citrus peel", "flavour": "Campfire smoke upfront, then agave sweetness, tropical fruit, mineral, slight pepper finish", "finish": "Warm, lingering smoke with sweet agave echo", "texture": "Full, oily mouthfeel — more viscous than tequila"}),
  "service_specs": json.dumps({"glass": "Copita or small snifter — NOT cocktail glass", "temp_c": "Room temperature", "food_pairing": "Chapulines (grasshoppers), tlayuda, mole negro, grilled corn, dark chocolate", "water": "Small glass of plain water alongside — palate reset, not dilution", "sal_de_gusano": "Optional: sal de gusano (salt with dried agave worm and chilli) on rim"}),
  "flavour_markers": ["campfire-smoke", "mesquite", "agave-sweetness", "tropical-fruit", "green-herb", "mineral", "pepper"],
  "flavour_weight": "medium-full",
  "flavour_profile_type": "smoky-complex",
  "origin_brand": "Del Maguey",
  "price_tier": "premium",
  "price_range_cad": "$75-90",
  "technical_specs": json.dumps({"abv_pct": 42, "agave_species": "Agave angustifolia (espadín)", "agave_age_years": "7-9", "pit_fuel": "Mesquite wood", "fermentation": "Wild yeast, open wooden vat, 7-10 days", "distillation": "Copper pot still, double-distilled", "category_official": "Artesanal mezcal"}),
  "slug": "del-maguey-vida-mezcal"
},
{
  "name": "Fortaleza Blanco Tequila",
  "category": "spirits_agave",
  "subcategory": "tequila_blanco",
  "producer_id": 183,
  "region_id": 100,
  "origin_country": "Mexico",
  "description": "The benchmark for traditional-method tequila — tahona stone-ground agave cooked in brick hornos, fermented in open wooden vats with spring water and wild yeast, double-distilled in copper pot stills, bottled without ageing. Fortaleza Blanco is the clearest expression of what blue agave tastes like when processed without industrial shortcuts — the tahona grinding releases more oils and fibres, producing a complexity and texture that industrial tequila cannot replicate. Guillermo Sauza's testament to pre-industrial tradition.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "Blanco (unaged, most agave expression)", "position": 1}, {"label": "Reposado (6 months, ex-bourbon integration)", "position": 2}, {"label": "Añejo (2 years — most complex)", "position": 3}, {"label": "Still Strength (46% — maximum intensity)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Crystal clear", "aroma": "Blue agave, cooked agave (sweet potato), citrus, pepper, floral", "flavour": "Sweet agave upfront (herbal, slightly vegetal), citrus, white pepper, mineral, floral mid-palate", "finish": "Long, clean, agave-sweet with gentle pepper warmth", "texture": "Full, slightly oily — tahona adds body"}),
  "service_specs": json.dumps({"glass": "Copita or brandy snifter — nose it first", "temp_c": "Slightly below room temperature", "food_pairing": "Ceviche, grilled fish tacos, elotes, Oaxacan cheese, guacamole", "cocktail": "Tommy's Margarita (lime, agave syrup only — no triple sec) is the definitive serve"}),
  "flavour_markers": ["agave-sweet", "herbal", "cooked-agave", "citrus", "white-pepper", "floral", "mineral"],
  "flavour_weight": "medium",
  "flavour_profile_type": "herbal-mineral",
  "origin_brand": "Fortaleza",
  "price_tier": "premium",
  "price_range_cad": "$80-100",
  "technical_specs": json.dumps({"abv_pct": 40, "agave_species": "Agave tequilana Weber azul (Blue Agave)", "cooking": "Brick hornos (36 hours)", "milling": "Stone tahona wheel", "fermentation": "Open wooden vats, spring water, wild yeast — 72-96 hours", "distillation": "Copper pot still, double-distilled", "category_official": "Tequila Blanco"}),
  "slug": "fortaleza-blanco-tequila"
},

# ============================================================
# BOURBON / TENNESSEE
# ============================================================
{
  "name": "Buffalo Trace Kentucky Straight Bourbon Whiskey",
  "category": "spirits_whiskey",
  "subcategory": "bourbon_kentucky",
  "producer_id": 158,
  "region_id": 82,
  "origin_country": "USA",
  "description": "The flagship expression from America's oldest continuously operating distillery (1775). Buffalo Trace is the benchmark for accessible, balanced Kentucky Bourbon — corn sweetness, rye spice, vanilla and caramel from new charred American oak, and the distinctive mineral quality of Frankfort limestone-filtered water. At under $50 CAD, it represents the single best quality-to-price ratio in the bourbon category. The foundation of the Buffalo Trace Antique Collection (BTAC) allocation programme.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "Buffalo Trace (entry — remarkable QPR)", "position": 1}, {"label": "Eagle Rare 10-year (single barrel)", "position": 2}, {"label": "Blanton's Original (first commercial single barrel)", "position": 3}, {"label": "E.H. Taylor Small Batch / Single Barrel", "position": 4}, {"label": "George T. Stagg (BTAC — barrel proof, annual release)", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Amber gold", "aroma": "Vanilla, caramel, brown sugar, slight floral, subtle rye spice", "flavour": "Sweet corn, vanilla, caramel, honey, gentle rye, dark fruit", "finish": "Medium, warm, spicy, oak tannin", "texture": "Medium body, smooth"}),
  "service_specs": json.dumps({"glass": "NEAT glass or rocks glass", "temp_c": "Room temperature or with one large ice cube", "food_pairing": "Aged cheddar, pecans, bourbon-glazed bacon, peach dessert", "cocktail_uses": ["Old Fashioned", "Manhattan", "Boulevardier"]}),
  "flavour_markers": ["vanilla", "caramel", "corn-sweet", "rye-spice", "brown-sugar", "dark-fruit", "oak"],
  "flavour_weight": "medium",
  "flavour_profile_type": "sweet-spice",
  "origin_brand": "Buffalo Trace",
  "price_tier": "mid_range",
  "price_range_cad": "$45-55",
  "technical_specs": json.dumps({"abv_pct": 45, "mash_bill": "Mash Bill 1 — corn, rye, malted barley (low rye)", "ageing": "New charred American white oak barrels, minimum 8 years (unspecified)", "distilled_at": "Buffalo Trace Distillery, Frankfort, Kentucky", "limestone_water": "Frankfort, Kentucky aquifer — calcium-rich, iron-free"}),
  "slug": "buffalo-trace-kentucky-bourbon"
},
{
  "name": "Uncle Nearest 1884 Small Batch Whiskey",
  "category": "spirits_whiskey",
  "subcategory": "tennessee_whiskey",
  "producer_id": 157,
  "region_id": 83,
  "origin_country": "USA",
  "description": "Named for the year Nearest Green's son George Green became master distiller of the Lynchburg, Tennessee distillery after his father. The 1884 is Uncle Nearest's signature expression — a blend of single barrels selected by Victoria Eady Butler (Nearest Green's great-great-granddaughter, now Uncle Nearest's master blender). The whiskey is Tennessee-style: Lincoln County Process charcoal filtering before barrel ageing, producing a characteristically smooth, lighter Tennessee expression. This is a culturally significant spirit — drinking it is an act of acknowledgment.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "1856 Premium (entry, 80 proof)", "position": 1}, {"label": "1884 Small Batch (93 proof — benchmark)", "position": 2}, {"label": "1820 Single Barrel (103-109 proof — premium)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Deep amber", "aroma": "Vanilla, caramel, maple, butterscotch, dried fruit, gentle spice", "flavour": "Honey, vanilla, maple syrup, dried fruit, gentle grain, smooth spice", "finish": "Long, clean, slightly sweet — maple and vanilla linger", "texture": "Silky — the Lincoln County Process removes rougher congeners"}),
  "service_specs": json.dumps({"glass": "Rocks glass or NEAT glass", "temp_c": "Room temperature", "food_pairing": "Pecan pie, smoked ribs, sharp cheddar, dark chocolate", "cocktail_uses": ["Tennessee Mule", "Lynchburg Lemonade", "Simple on the rocks"]}),
  "flavour_markers": ["vanilla", "maple", "honey", "butterscotch", "dried-fruit", "silky", "gentle-spice"],
  "flavour_weight": "medium",
  "flavour_profile_type": "smooth-sweet",
  "origin_brand": "Uncle Nearest",
  "price_tier": "premium",
  "price_range_cad": "$70-85",
  "technical_specs": json.dumps({"abv_pct": 46.5, "process": "Lincoln County Process (maple charcoal filtering before barrel)", "ageing": "Minimum 3 years new charred American oak", "distilled_at": "Shelbyville, Tennessee (sourced and blended from Tennessee stocks)", "notable": "Blended by Victoria Eady Butler — Nearest Green's great-great-granddaughter"}),
  "slug": "uncle-nearest-1884-small-batch"
},
{
  "name": "Clairin Sajous",
  "category": "spirits_rum",
  "subcategory": "clairin_artisanal",
  "producer_id": 155,
  "region_id": 76,
  "origin_country": "Haiti",
  "description": "Single-village, single-producer Haitian artisanal cane spirit from St-Michel de l'Attalaye, Artibonite department. The Sajous family uses local Cristalino sugarcane, wild indigenous yeast fermentation in open wooden vats (7-10 days), and a simple copper alembic still. Imported by Luca Gargano of Velier (Genoa). Bottled at cask strength without filtration or colouring. Clairin Sajous is the entry point to understanding Haitian terroir — lighter and more accessible than the southern clairins, with remarkable clarity of sugarcane character.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Sajous (Artibonite — lighter, more floral)", "position": 1}, {"label": "Vaval (Cavaillon — vetiver, herbal, complex)", "position": 2}, {"label": "Le Rocher (Baradères — full, funky)", "position": 3}, {"label": "Casimir (Léogâne — coastal, complex)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Crystal clear", "aroma": "Fresh sugarcane, green herb, citrus, tropical fruit, slight floral, subtle earth", "flavour": "Cane juice, lime zest, green grass, tropical fruit, mineral, slight funk", "finish": "Clean, dry, lingering cane sweetness with mineral edge", "texture": "Light to medium body — cleaner than agricole rum"}),
  "service_specs": json.dumps({"glass": "Copita or glencairn", "temp_c": "Room temperature", "water": "Small splash unlocks aromatics", "food_pairing": "Plantain, griot (fried pork), habanero peppers, tropical fruit", "cocktail": "Ti' Punch adaptation — lime, cane syrup"}),
  "flavour_markers": ["sugarcane-fresh", "citrus", "tropical-fruit", "green-herb", "mineral", "floral"],
  "flavour_weight": "light",
  "flavour_profile_type": "fresh-mineral",
  "origin_brand": "Clairin Sajous / Velier",
  "price_tier": "premium",
  "price_range_cad": "$80-100",
  "technical_specs": json.dumps({"abv_pct": 52, "cane_variety": "Cristalino", "fermentation": "Wild yeast, open wooden vats, 7-10 days", "distillation": "Copper pot still (alembic simple)", "ageing": "None", "filtration": "None", "colouring": "None"}),
  "slug": "clairin-sajous"
},

# ============================================================
# WINE — NAPA / SONOMA
# ============================================================
{
  "name": "Opus One 2019",
  "category": "wine_still",
  "subcategory": "bordeaux_blend_napa",
  "producer_id": 164,
  "region_id": 80,
  "origin_country": "USA",
  "description": "The flagship collaboration of Robert Mondavi and Baron Philippe de Rothschild — first vintage 1979, released 1984. Opus One is a single estate Bordeaux blend (Cabernet Sauvignon dominant) from Oakville, Napa Valley. The 2019 vintage captures a warm-but-balanced Napa growing season: deep cassis, graphite, and cedar on the nose; full-bodied with refined tannins and the signature Opus integration of California fruit weight with Bordelais structure.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Opus One (single wine, single estate — no second wine)", "position": 1}]),
  "deductive_profile": json.dumps({"colour": "Deep ruby-garnet", "clarity": "Clear, brilliant", "aroma": "Cassis, blackcurrant, cedar, graphite, dark chocolate, violets, tobacco", "flavour": "Full-bodied, concentrated blackcurrant, plum, dark cherry, graphite, cedar, fine-grained tannins", "finish": "Very long — 60+ seconds — polished, cassis and cedar echo", "acid_level": "Medium+", "tannin_level": "Medium-high, fine-grained"}),
  "service_specs": json.dumps({"decant_minutes": 60, "glass": "Large Bordeaux glass (Riedel Bordeaux or equivalent)", "serve_temp_c": 17, "ageing_potential_years": "15-20+", "food_pairing": "Prime rib, rack of lamb, truffle risotto, aged Comté"}),
  "flavour_markers": ["cassis", "blackcurrant", "cedar", "graphite", "dark-chocolate", "violets", "tobacco", "plum"],
  "flavour_weight": "full",
  "flavour_profile_type": "bordeaux-napa",
  "origin_brand": "Opus One",
  "price_tier": "ultra_premium",
  "price_range_cad": "$380-450",
  "technical_specs": json.dumps({"vintage": 2019, "blend": "Cabernet Sauvignon 76%, Merlot 10%, Cabernet Franc 7%, Petit Verdot 4%, Malbec 3%", "abv_pct": 15.5, "new_french_oak_pct": 100, "ageing_months": 18}),
  "slug": "opus-one-2019"
},
{
  "name": "Ridge Monte Bello Cabernet Sauvignon",
  "category": "wine_still",
  "subcategory": "cabernet_sauvignon_california",
  "producer_id": 167,
  "region_id": 81,
  "origin_country": "USA",
  "description": "California's most age-worthy Cabernet — produced from the Monte Bello Ridge above Cupertino in the Santa Cruz Mountains at 760m altitude. The 1971 Ridge Monte Bello was one of the five Californian reds in the 1976 Paris tasting; the 2006 retrospective had it placing first. Paul Draper's legacy winemaking philosophy — minimal intervention, wild yeast, full disclosure on back label — produces a wine of extraordinary elegance and longevity. At 20+ years, Ridge Monte Bello reveals a complexity that rivals the finest Bordeaux.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Monte Bello (Santa Cruz Mountains — Cabernet dominant)", "position": 1}, {"label": "Geyserville (Sonoma — Zinfandel dominant, field blend)", "position": 2}, {"label": "Lytton Springs (Dry Creek — Zinfandel benchmark)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Deep ruby with garnet rim on older vintages", "aroma": "Cassis, blackcurrant, eucalyptus, cedar, mineral, dark fruit, subtle oak", "flavour": "Tightly structured cassis, mineral, iron, chalk, cedar — austere in youth, revelatory with 15+ years bottle age", "finish": "Extraordinary length — mineral, cassis, chalk echo", "ageing_profile": "Needs 10-15 years minimum; best at 20-30 years"}),
  "service_specs": json.dumps({"decant_minutes": 90, "glass": "Burgundy or large Bordeaux glass", "serve_temp_c": 16, "ageing_potential_years": "25-35+", "food_pairing": "Lamb chops, dry-aged ribeye, hard cheese, roasted mushrooms"}),
  "flavour_markers": ["cassis", "mineral", "eucalyptus", "cedar", "chalk", "iron", "dark-fruit"],
  "flavour_weight": "full",
  "flavour_profile_type": "mineral-structured",
  "origin_brand": "Ridge Vineyards",
  "price_tier": "ultra_premium",
  "price_range_cad": "$280-350",
  "technical_specs": json.dumps({"blend": "Cabernet Sauvignon ~70-80%, Merlot, Petit Verdot, Cabernet Franc", "abv_pct": 13.5, "ageing": "22 months American oak (60% new)", "philosophy": "Back-label full disclosure of all additions"}),
  "slug": "ridge-monte-bello-cabernet"
},

# ============================================================
# WINE — AUSTRALIA
# ============================================================
{
  "name": "Penfolds Grange",
  "category": "wine_still",
  "subcategory": "shiraz_barossa",
  "producer_id": 168,
  "region_id": 84,
  "origin_country": "Australia",
  "description": "Australia's most iconic wine — created by Max Schubert in 1951 against company orders, briefly discontinued, then revealed to be Australia's greatest wine. Grange is a multi-vineyard, multi-region Shiraz (and small amount of Cabernet Sauvignon) blended from the finest barrels of the vintage. In great years it sources from Barossa, Magill Estate (Adelaide suburban vineyard — heritage site), McLaren Vale, and sometimes Clare Valley. 100% new American oak for 20 months. Capable of 40-50 years ageing in great vintages.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Grange — multi-region (the icon)", "position": 1}, {"label": "Bin 707 Cabernet Sauvignon (Grange's red twin)", "position": 2}, {"label": "RWT Barossa Valley Shiraz (French oak counterpoint)", "position": 3}, {"label": "St Henri (no new oak — different Grange philosophy)", "position": 4}, {"label": "Bin 389 (Cabernet-Shiraz — 'Baby Grange')", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Opaque deep ruby-purple in youth, garnet at 20 years", "aroma": "Blackberry, blueberry, dark chocolate, American oak (vanilla, coconut, cedar), leather, tar, iron", "flavour": "Massive concentration — blackberry, plum, chocolate, American oak vanilla, iron, leather", "finish": "60+ seconds — dark fruit, oak, iron, dust echo", "youth_profile": "Almost inaccessible at release — needs minimum 10 years", "maturity_profile": "At 20-30 years: dried fruit, leather, iron ore, cedar, complex mushroom development"}),
  "service_specs": json.dumps({"decant_minutes": 120, "glass": "Large Burgundy or Bordeaux glass", "serve_temp_c": 17, "ageing_potential_years": "30-50+", "food_pairing": "Slow-roasted lamb shoulder, kangaroo with bush tomato, washed-rind cheese"}),
  "flavour_markers": ["blackberry", "blueberry", "dark-chocolate", "american-oak-vanilla", "iron", "leather", "tar", "eucalyptus"],
  "flavour_weight": "full",
  "flavour_profile_type": "powerful-structured",
  "origin_brand": "Penfolds",
  "price_tier": "ultra_premium",
  "price_range_cad": "$900-1200",
  "technical_specs": json.dumps({"varietal_composition": "Shiraz ~97% + Cabernet Sauvignon ~3% (varies by vintage)", "abv_pct": 14.5, "new_american_oak_pct": 100, "ageing_months": 20, "source_regions": ["Barossa Valley", "McLaren Vale", "Magill Estate (Adelaide)"]}),
  "slug": "penfolds-grange"
},
{
  "name": "Henschke Hill of Grace Shiraz",
  "category": "wine_still",
  "subcategory": "shiraz_eden_valley",
  "producer_id": 169,
  "region_id": 84,
  "origin_country": "Australia",
  "description": "Australia's most reverently regarded single-vineyard wine — produced from a single block of Shiraz vines planted in the 1860s next to Gnadenberg Lutheran church in the Eden Valley, South Australia. The vines are pre-phylloxera and ungrafted — 150+ years old, producing tiny yields of extraordinary concentration. Stephen and Prue Henschke (biodynamic management) produce approximately 1,500-2,000 cases per year. Hill of Grace in great vintages (1990, 1998, 2008, 2010, 2012) is among the most complex wines on Earth.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Hill of Grace (single vineyard icon)", "position": 1}, {"label": "Mount Edelstone (Eden Valley Shiraz — single vineyard, benchmark entry)", "position": 2}, {"label": "Henry's Seven (Barossa blend, accessible)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Opaque deep ruby in youth, evolving garnet-brick at 20+ years", "aroma": "Blueberry, violets, black pepper, iron ore, licorice, eucalyptus, fine tannin", "flavour": "Eden Valley is more refined than Barossa — higher natural acidity, more floral, less jam; Old vine concentration without Barossa earthiness", "finish": "50+ seconds, violet-mineral-cedar echo", "key_distinction": "Eden Valley altitude = more acid, more aromatics than Barossa valley floor"}),
  "service_specs": json.dumps({"decant_minutes": 120, "glass": "Large Burgundy glass", "serve_temp_c": 17, "ageing_potential_years": "30-50+", "food_pairing": "Spring lamb, aged Gruyère, kangaroo tataki, porcini mushroom"}),
  "flavour_markers": ["blueberry", "violets", "black-pepper", "iron-ore", "licorice", "eucalyptus", "floral"],
  "flavour_weight": "full",
  "flavour_profile_type": "elegant-powerful",
  "origin_brand": "Henschke",
  "price_tier": "ultra_premium",
  "price_range_cad": "$500-800",
  "technical_specs": json.dumps({"varietal_composition": "Shiraz 100%", "vine_age": "150+ years (planted 1860s)", "abv_pct": 14, "ageing": "18 months French and American oak (used, not new)", "viticulture": "Biodynamic (certified Demeter)"}),
  "slug": "henschke-hill-of-grace"
},

# ============================================================
# WINE — NEW ZEALAND
# ============================================================
{
  "name": "Cloudy Bay Sauvignon Blanc",
  "category": "wine_still",
  "subcategory": "sauvignon_blanc_marlborough",
  "producer_id": 171,
  "region_id": 87,
  "origin_country": "New Zealand",
  "description": "The wine that created the Marlborough Sauvignon Blanc category. Kevin Judd's inaugural 1985 vintage established the pungent, lifted, passion-fruit-and-capsicum style that redefined New Zealand wine internationally. The current wine maintains the house style: lifted thiols (passion fruit, guava, grapefruit), methoxypyrazines (capsicum, green bean), and the clean, razor-sharp acidity of the Wairau Valley floor. Non-vintage blend of Wairau and Awatere sources.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "Sauvignon Blanc (the category benchmark)", "position": 1}, {"label": "Te Koko (barrel-fermented, complex — wild yeast)", "position": 2}, {"label": "Pelorus (traditional method sparkling)", "position": 3}, {"label": "Te Wahi (Central Otago Pinot Noir — premium)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Pale straw-gold", "clarity": "Clear, brilliant", "aroma": "Passion fruit, grapefruit, white peach, capsicum, cut grass, lemongrass", "flavour": "Vivid, high-toned — passion fruit and grapefruit upfront, capsicum/green herb, refreshing acidity", "finish": "Clean, crisp, medium length — citrus and mineral echo", "style_notes": "The defining Marlborough style — deliberately aromatic, fresh, exuberant"}),
  "service_specs": json.dumps({"glass": "Sauvignon Blanc glass (medium bowl, upright)", "serve_temp_c": 8, "food_pairing": "Oysters, Pacific salmon sashimi, fresh chèvre, Vietnamese spring rolls, green salads, asparagus", "no_decanting": True}),
  "flavour_markers": ["passion-fruit", "grapefruit", "capsicum", "lemongrass", "white-peach", "cut-grass", "crisp-acid"],
  "flavour_weight": "light",
  "flavour_profile_type": "aromatic-herbaceous",
  "origin_brand": "Cloudy Bay",
  "price_tier": "premium",
  "price_range_cad": "$30-38",
  "technical_specs": json.dumps({"abv_pct": 13, "varieties": "Sauvignon Blanc 100%", "sources": "Wairau Valley (primary) + Awatere Valley", "fermentation": "Stainless steel, cool fermentation to preserve aromatics", "malolactic": False}),
  "slug": "cloudy-bay-sauvignon-blanc"
},
{
  "name": "Felton Road Block 3 Pinot Noir",
  "category": "wine_still",
  "subcategory": "pinot_noir_central_otago",
  "producer_id": 172,
  "region_id": 88,
  "origin_country": "New Zealand",
  "description": "One of New Zealand's most collected wines — from a single block of biodynamically farmed Pinot Noir on decomposed schist soils in Bannockburn, Central Otago. Block 3 is the oldest planting on the Felton Road estate (1991) and produces the most complex and age-worthy of the single-block expressions. Blair Walter's winemaking philosophy: whole-bunch inclusion, wild yeast only, very gentle extraction, no fining or filtration. The result is Pinot of extraordinary spice, earth, and mineral depth that rewards a decade of patience.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Bannockburn Pinot Noir (estate blend, entry)", "position": 1}, {"label": "Block 3 (oldest vines, most complex)", "position": 2}, {"label": "Block 5 (more Burgundian, elegant)", "position": 3}, {"label": "Calvert (distinct terroir — neighbouring vineyard)", "position": 4}, {"label": "Cornish Point (dramatic schist face)", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Translucent ruby, slight brick at 8+ years", "clarity": "Unfined — may have slight haze", "aroma": "Dark cherry, forest floor, schist mineral, five-spice, violets, black tea, dried herbs", "flavour": "Dark cherry, plum, whole-bunch spice (star anise, dried herbs), schist mineral, silky tannins", "finish": "Long, fine — mineral and spice echo 50+ seconds", "ageing_profile": "Wines open at 5 years but best at 8-15+"}),
  "service_specs": json.dumps({"decant_minutes": 30, "glass": "Large Burgundy glass", "serve_temp_c": 15, "ageing_potential_years": "15-20+", "food_pairing": "Duck breast, venison, salmon, pinot-friendly mushroom dishes, goat cheese"}),
  "flavour_markers": ["dark-cherry", "forest-floor", "schist-mineral", "five-spice", "violets", "black-tea", "dried-herbs"],
  "flavour_weight": "medium",
  "flavour_profile_type": "mineral-spiced",
  "origin_brand": "Felton Road",
  "price_tier": "ultra_premium",
  "price_range_cad": "$120-160",
  "technical_specs": json.dumps({"abv_pct": 14, "variety": "Pinot Noir 100%", "vine_age_years": 30, "viticulture": "Biodynamic (Demeter certified)", "fermentation": "Wild yeast, whole bunch inclusion ~30%", "ageing_months": 16, "oak": "French oak, 30% new"}),
  "slug": "felton-road-block-3-pinot-noir"
},

# ============================================================
# WINE — ARGENTINA / CHILE / SOUTH AFRICA
# ============================================================
{
  "name": "Catena Zapata Adrianna Vineyard Fortuna Terrae Malbec",
  "category": "wine_still",
  "subcategory": "malbec_high_altitude",
  "producer_id": 173,
  "region_id": 90,
  "origin_country": "Argentina",
  "description": "From the Adrianna Vineyard at 1,500m altitude in Gualtallary, Uco Valley — Argentina's highest and most celebrated vineyard site. Fortuna Terrae ('Land of Fortune') is the single-parcel Malbec expression of Adrianna — a different story from the limestone-influenced White Stones Chardonnay. The extreme altitude produces intense UV radiation, driving thick-skinned grapes with extraordinary anthocyanin and polyphenol concentration. The resulting Malbec is unlike anything produced on valley floors: structured, mineral, violet-driven, with a refinement that defies the grape's reputation for rustic power.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Adrianna Vineyard Fortuna Terrae Malbec (icon)", "position": 1}, {"label": "Catena Alta Historic Rows Malbec (single block, ultra-old vine)", "position": 2}, {"label": "Catena Alta Malbec (estate — benchmark accessible)", "position": 3}, {"label": "Catena Zapata Malbec (entry estate)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Deep ruby-violet, almost opaque", "aroma": "Violets (high-altitude signature), blueberry, plum, graphite, black pepper, mineral, licorice", "flavour": "Violet-forward, structured — not the jammy valley Malbec; firm, fine tannins from altitude, mineral backbone", "finish": "Very long — violet, mineral, graphite echo", "altitude_signature": "The violet and mineral character are altitude-specific — lower-altitude Malbec lacks this lift"}),
  "service_specs": json.dumps({"decant_minutes": 60, "glass": "Large Bordeaux or Burgundy glass", "serve_temp_c": 17, "ageing_potential_years": "20-25+", "food_pairing": "Asado (Argentine grill), lamb, dry-aged beef, blue cheese"}),
  "flavour_markers": ["violets", "blueberry", "graphite", "black-pepper", "mineral", "licorice", "fine-tannin"],
  "flavour_weight": "full",
  "flavour_profile_type": "violet-mineral",
  "origin_brand": "Catena Zapata",
  "price_tier": "ultra_premium",
  "price_range_cad": "$250-350",
  "technical_specs": json.dumps({"abv_pct": 14.5, "variety": "Malbec 100%", "vineyard": "Adrianna Vineyard, Gualtallary, Uco Valley", "altitude_m": 1500, "viticulture": "Certified sustainable", "ageing_months": 18, "oak": "French and American oak (60% new)"}),
  "slug": "catena-adrianna-fortuna-terrae-malbec"
},
{
  "name": "Sadie Family Columella",
  "category": "wine_still",
  "subcategory": "syrah_mourvedre_swartland",
  "producer_id": 175,
  "region_id": 94,
  "origin_country": "South Africa",
  "description": "South Africa's most internationally collected wine — Eben Sadie's old-vine Swartland Syrah (dominant) and Mourvèdre blend from multiple parcels of dry-farmed bushvine material across different Swartland soil types. Columella has been the flagship of the Swartland revolution since 2001. No new oak, wild yeast, minimal intervention — the wine is a pure expression of Swartland terroir: the iron-red soil, the dry-farmed bushvines, the Paardeberg granite. Consistently scores 95-98 from international critics.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Columella (Syrah/Mourvèdre — the flagship red)", "position": 1}, {"label": "Palladius (white blend — Chenin dominant, Columella's counterpart)", "position": 2}, {"label": "T Voetpad / Pofadder (old vine series — single site)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Deep ruby with violet hints", "aroma": "Iron ore, dark olive, violets, black pepper, smoked meat, Provençal herbs, plum", "flavour": "Structured, mineral — iron, dark plum, black olive, dried herbs; NOT jammy California Syrah; closer to Northern Rhône but with Swartland iron character", "finish": "Exceptional length — iron mineral, dried herbs, olive echo", "ageing_profile": "Best at 8-15+ years — austere in youth"}),
  "service_specs": json.dumps({"decant_minutes": 90, "glass": "Large Burgundy or Rhône glass", "serve_temp_c": 17, "ageing_potential_years": "20-25+", "food_pairing": "Karoo lamb, boerewors, aged hard cheese, game birds"}),
  "flavour_markers": ["iron-ore", "dark-olive", "violets", "black-pepper", "smoked-meat", "provencal-herbs", "plum"],
  "flavour_weight": "full",
  "flavour_profile_type": "iron-mineral",
  "origin_brand": "Sadie Family Wines",
  "price_tier": "ultra_premium",
  "price_range_cad": "$180-220",
  "technical_specs": json.dumps({"abv_pct": 14.5, "blend": "Syrah ~80%, Mourvèdre ~15%, other Rhône varieties", "vine_age_avg_years": 45, "viticulture": "Organic, dry-farmed bushvine", "ageing_months": 18, "oak": "Old French oak barrels only — no new oak"}),
  "slug": "sadie-family-columella"
},

# ============================================================
# SCOTCH WHISKY
# ============================================================
{
  "name": "The Macallan 12 Year Sherry Oak",
  "category": "spirits_whiskey",
  "subcategory": "single_malt_speyside",
  "producer_id": 178,
  "region_id": 95,
  "origin_country": "Scotland",
  "description": "The benchmark sherry-matured Speyside single malt — entirely matured in European oak casks seasoned with Oloroso sherry from Jerez, Spain. The Macallan 12 Sherry Oak is the definitive introduction to the sherry-wood style: dark amber colour from natural extraction (no caramel colouring in Sherry Oak series), dried fruit, Christmas cake, orange peel, spice, chocolate. The 12-year provides the entry point to the Macallan hierarchy — the same fundamental flavour profile, less developed, more accessible.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "12-year Double Cask (European + American oak)", "position": 1}, {"label": "12-year Sherry Oak (European oak only — more intense)", "position": 2}, {"label": "18-year Sherry Oak (the sweet spot)", "position": 3}, {"label": "25-year and 30-year (ultra-luxury — $1000+ CAD)", "position": 4}, {"label": "Edition / Rare Cask series (annual limited releases)", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Dark amber (natural from sherry cask — no colouring)", "aroma": "Dried fruit (raisins, sultanas, dates), orange peel, Christmas cake, nutmeg, dark chocolate, vanilla oak", "flavour": "Rich, full — dried fruit, orange peel, chocolate, ginger spice, butterscotch, subtle oak tannin", "finish": "Long, warming — dried fruit and chocolate echo, gentle oak spice", "age_statement": "12 years minimum — all wood European sherry oak"}),
  "service_specs": json.dumps({"glass": "Glencairn or tulip", "temp_c": "Room temperature or with 2-3ml cold water", "water_effect": "A few drops of water opens the wood spice and dried fruit enormously", "food_pairing": "Dark chocolate, pecan tart, blue cheese, Christmas pudding, cigars"}),
  "flavour_markers": ["dried-fruit", "orange-peel", "christmas-cake", "nutmeg", "dark-chocolate", "butterscotch", "ginger-spice"],
  "flavour_weight": "full",
  "flavour_profile_type": "sherry-fruit",
  "origin_brand": "The Macallan",
  "price_tier": "premium",
  "price_range_cad": "$85-100",
  "technical_specs": json.dumps({"abv_pct": 40, "age_years": 12, "cask_type": "European oak, ex-Oloroso sherry (exclusively)", "distillery": "Easter Elchies Estate, Craigellachie, Speyside", "natural_colour": True, "non_chill_filtered": False}),
  "slug": "macallan-12-sherry-oak"
},
{
  "name": "Ardbeg 10 Year Old Single Malt",
  "category": "spirits_whiskey",
  "subcategory": "single_malt_islay",
  "producer_id": 179,
  "region_id": 96,
  "origin_country": "Scotland",
  "description": "The world's most consistently praised heavily-peated whisky — repeatedly voted 'World's Best Single Malt' in consumer polls. The 10-year is the foundation of the Ardbeg range: 55 PPM phenols in the malt, producing the most medicinal, iodine-intensive smoke of any standard Islay expression, but with a remarkable underlying sweetness (vanilla, toffee from ex-bourbon barrels) and bright citrus that prevent it from being merely assertive. The purifier plate in Ardbeg's stills produces a lighter distillate than the phenol level would suggest.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "Ten (10-year — benchmark)", "position": 1}, {"label": "Uigeadail (NAS — ex-bourbon + ex-sherry, 54.2%)", "position": 2}, {"label": "Corryvreckan (NAS — ex-bourbon + French oak, 57.1%)", "position": 3}, {"label": "Wee Beastie (5-year, 47.4%)", "position": 4}, {"label": "Annual Committee Reserve (lottery basis)", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Pale gold", "aroma": "Peat smoke, iodine, seaweed, antiseptic (Betadine), vanilla, lemon, honey underneath", "flavour": "Smoke hits first — medicinal, seaweed, tar — then extraordinary sweetness emerges: vanilla, honey, citrus, white pepper", "finish": "Very long — smoke lingers 60+ seconds, vanilla-sweet echo underneath", "intensity_warning": "The most polarising mainstream whisky — guests who dislike smoke will dislike this; those who love it will never look back"}),
  "service_specs": json.dumps({"glass": "Glencairn (captures and concentrates the smoke) or small tulip", "temp_c": "Room temperature — never ice", "water": "A few drops unlocks hidden sweetness dramatically", "food_pairing": "Smoked fish (kippered salmon), oysters, blue cheese, dark chocolate sea salt, peat-smoked meat"}),
  "flavour_markers": ["peat-smoke", "iodine", "seaweed", "medicinal", "vanilla", "honey", "citrus", "tar"],
  "flavour_weight": "full",
  "flavour_profile_type": "medicinal-smoke",
  "origin_brand": "Ardbeg",
  "price_tier": "premium",
  "price_range_cad": "$70-85",
  "technical_specs": json.dumps({"abv_pct": 46, "age_years": 10, "phenol_level_ppm": 55, "cask_type": "Ex-bourbon American oak", "non_chill_filtered": True, "natural_colour": True, "still_feature": "Purifier plate — unique to Ardbeg"}),
  "slug": "ardbeg-10-year-old"
},
{
  "name": "Springbank 10 Year Old Campbeltown Single Malt",
  "category": "spirits_whiskey",
  "subcategory": "single_malt_campbeltown",
  "producer_id": 180,
  "region_id": 98,
  "origin_country": "Scotland",
  "description": "The only whisky in Scotland produced entirely on-site — malting, mashing, fermenting, distilling, maturing, bottling, all within the Campbeltown distillery walls. The house style: 2.5-times distillation (between double and triple) creates a medium-weight spirit that carries the distinctive Campbeltown character — saline, briny, slightly oily, with a hint of sherry and a damp cellar quality that is unique to this coastal peninsula. At 10 years it is already extraordinary; at 15 it is one of Scotland's finest.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "10-year (entry — benchmark value)", "position": 1}, {"label": "15-year (sherry wood finish — the sweet spot)", "position": 2}, {"label": "Longrow (heavily peated — separate distilling style)", "position": 3}, {"label": "Hazelburn (triple-distilled, unpeated — lighter)", "position": 4}, {"label": "18-year and 21-year (annual releases — collector items)", "position": 5}]),
  "deductive_profile": json.dumps({"colour": "Pale straw-gold (natural colour, not coloured)", "aroma": "Saline sea air, fresh brine, pear, apple, slight peat, vanilla, old cellar, slight rubber", "flavour": "Saline brine upfront, then orchard fruit, slight smoke, vanilla, old oak, damp stone", "finish": "Long, saline — the sea air is in the finish; mineral and slight smoke echo", "campbeltown_terroir": "The saline character is specific to Campbeltown — coastal peninsula on the Kintyre, surrounded by sea"}),
  "service_specs": json.dumps({"glass": "Glencairn or tulip", "temp_c": "Room temperature or with a few drops of water", "food_pairing": "Smoked oysters, aged cheddar, salt-baked fish, anchovies, farmhouse butter"}),
  "flavour_markers": ["sea-salt", "brine", "orchard-fruit", "slight-peat", "vanilla", "old-cellar", "mineral"],
  "flavour_weight": "medium",
  "flavour_profile_type": "saline-mineral",
  "origin_brand": "Springbank",
  "price_tier": "premium",
  "price_range_cad": "$80-100",
  "technical_specs": json.dumps({"abv_pct": 46, "age_years": 10, "distillation": "2.5 times — unique to Springbank", "floor_malted": True, "non_chill_filtered": True, "natural_colour": True, "cask_mix": "Approximately 50% fresh Bourbon, 25% Sherry, 25% refill"}),
  "slug": "springbank-10-year-old"
},

# ============================================================
# BEER — BELGIUM / GERMANY
# ============================================================
{
  "name": "Cantillon Gueuze — 100% Lambic Bio",
  "category": "beer_wild",
  "subcategory": "gueuze_lambic",
  "producer_id": 184,
  "region_id": 101,
  "origin_country": "Belgium",
  "description": "Cantillon's organic-certified gueuze — a blend of 1, 2, and 3-year-old lambics from the Anderlecht brewery, refermented in bottle for 12-18 months. The 100% Lambic Bio uses only organic barley, wheat, and hops (aged hops — fresh hops would kill the wild fermentation). This is perhaps the most wine-like of all beers: complex, acidic, funky, dry, with no sweetness — demanding the same attention and reverence as a Grand Cru Burgundy. The Brettanomyces character (hay, leather, horse blanket) develops over 3-5 years of bottle ageing.",
  "quality_tier": "reserve",
  "quality_hierarchy": json.dumps([{"label": "Gueuze 100% Lambic Bio (entry gueuze — but still extraordinary)", "position": 1}, {"label": "Lou Pepe Gueuze (premium aged blend)", "position": 2}, {"label": "Kriek (whole Belgian cherries, 8 months)", "position": 3}, {"label": "Rosé de Gambrinus (raspberries)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Golden amber, light effervescence, minimal head", "clarity": "Slightly hazy — unfiltered", "aroma": "Hay, lemon peel, oak, Brett funk (stable, horse blanket), apple, slight vinegar", "flavour": "Tart, dry, acidic — lemon, apple, hay, Brett leather, mineral, no sweetness whatsoever", "finish": "Long, dry, sour — lemon mineral echo", "food_wine_parallel": "Think dry Riesling Spätlese or aged Chablis — not 'beer' in the normal sense"}),
  "service_specs": json.dumps({"glass": "Champagne flute or tulip — not a pint glass", "temp_c": 10, "serve_in_bottle_aged_verticals": True, "food_pairing": "Flemish beef stew (carbonnade), aged Gouda, mussels, oysters, strong cheese", "cellaring": "Excellent: 5-10 years improves complexity"}),
  "flavour_markers": ["lemon", "hay", "brett-funk", "apple", "oak", "acidic", "dry", "mineral"],
  "flavour_weight": "light",
  "flavour_profile_type": "sour-mineral",
  "origin_brand": "Cantillon",
  "price_tier": "premium",
  "price_range_cad": "$28-38",
  "technical_specs": json.dumps({"abv_pct": 5, "brewing_season": "October-April only", "lambic_ages": "1, 2, and 3-year lambic blended", "wild_yeast": "Brettanomyces bruxellensis, Pediococcus, Lactobacillus — airborne from Senne Valley", "certified_organic": True, "refermentation": "18 months in bottle before release"}),
  "slug": "cantillon-gueuze-100-lambic-bio"
},
{
  "name": "Weihenstephan Hefeweissbier",
  "category": "beer_ale",
  "subcategory": "hefeweizen_bavarian",
  "producer_id": 185,
  "region_id": 102,
  "origin_country": "Germany",
  "description": "The world's oldest brewery's flagship wheat beer — the textbook reference for Bavarian Hefeweizen. The classic banana-clove balance is produced by the Weihenstephan proprietary yeast strain producing isoamyl acetate (banana ester) and 4-vinylguaiacol (clove phenol) during fermentation. Hazy golden, with a thick white head. This is the global benchmark for the style — used as the reference in brewing education courses worldwide.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "Hefeweissbier (benchmark — the reference expression)", "position": 1}, {"label": "Kristallweissbier (filtered — cleaner, crisper)", "position": 2}, {"label": "Dunkelweissbier (dark wheat — roast + banana)", "position": 3}, {"label": "Vitus (Weizenbock — stronger, 7.7%)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Hazy golden-amber", "clarity": "Hazy (yeast in suspension — the 'Hefe' = yeast)", "head": "Large, dense, persistent white head", "aroma": "Banana (isoamyl acetate), clove (4-VG), bubblegum, wheat, gentle citrus", "flavour": "Banana upfront, then clove/spice, soft wheat malt, gentle citrus, refreshing carbonation", "finish": "Clean, dry, spicy clove echo", "temperature_note": "Banana dominates at cold temperatures; clove becomes more prominent at 10-12°C"}),
  "service_specs": json.dumps({"glass": "Weizen glass (tall, curved — 500ml minimum)", "pour_technique": "Pour slowly at angle, leave 2cm in bottle, swirl bottle to suspend yeast, then pour remaining yeast into glass", "serve_temp_c": 8, "food_pairing": "Weisswurst (veal sausage), pretzel, grilled fish, schnitzel, light salads"}),
  "flavour_markers": ["banana", "clove", "bubblegum", "wheat", "citrus", "refreshing"],
  "flavour_weight": "light",
  "flavour_profile_type": "fruity-spiced",
  "origin_brand": "Weihenstephan",
  "price_tier": "value",
  "price_range_cad": "$6-8",
  "technical_specs": json.dumps({"abv_pct": 5.4, "ibu": 14, "srm": 5, "wheat_pct": 67, "founded": "1040 AD", "yeast": "Weihenstephan weizen yeast — top-fermenting"}),
  "slug": "weihenstephan-hefeweissbier"
},

# ============================================================
# NA — DEALCOHOLISED / SEEDLIP / KOMBUCHA
# ============================================================
{
  "name": "Leitz Eins Zwei Zero Riesling",
  "category": "na_dealcoholised",
  "subcategory": "dealcoholised_white",
  "producer_id": None,
  "region_id": None,
  "origin_country": "Germany",
  "description": "The global benchmark for dealcoholised wine — Johannes Leitz's Rheingau Riesling base wine, dealcoholised by spinning cone column (SCC) technology to below 0.5% ABV. The spinning cone column operates at low temperature under vacuum, preserving the volatile aromatic compounds (thiols, esters) that other dealcoholisation methods (heat distillation, reverse osmosis) destroy. Leitz Eins Zwei Zero Riesling retains the characteristic Riesling profile — slate mineral, citrus, petrol notes on aged wine — with a reduced body from the absent alcohol.",
  "quality_tier": "estate",
  "quality_hierarchy": json.dumps([{"label": "Leitz Eins Zwei Zero Riesling (white benchmark)", "position": 1}, {"label": "Leitz Eins Zwei Zero Rosé (benchmark dealcoholised rosé)", "position": 2}, {"label": "Torres Natureo Muscat (aromatic dealcoholised)", "position": 3}, {"label": "Gruvi Bubbly Rosé (carbonated, session)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Pale straw", "clarity": "Clear, brilliant", "aroma": "Citrus (lime, lemon), slate mineral, slight petrol, fresh apple, white peach", "flavour": "Riesling character intact — citrus, mineral, slight slate; body is noticeably lighter than alcoholic wine (alcohol provides mouthfeel)", "finish": "Clean, crisp, mineral — shorter than the alcoholic equivalent"}),
  "service_specs": json.dumps({"glass": "Standard white wine glass", "serve_temp_c": 8, "food_pairing": "Equally successful with food as the alcoholic equivalent — the pairing logic is the same: acidity bridges fat, mineral character works with seafood", "professional_note": "The best dealcoholised wines deserve the same food pairing analysis as any wine — the guest does not need the asterisk of 'but it has no alcohol'"}),
  "flavour_markers": ["citrus", "slate-mineral", "lime", "fresh-apple", "white-peach", "petrol-developing"],
  "flavour_weight": "light",
  "flavour_profile_type": "mineral-crisp",
  "origin_brand": "Leitz",
  "price_tier": "mid_range",
  "price_range_cad": "$22-28",
  "technical_specs": json.dumps({"abv_pct": 0.5, "base_variety": "Riesling", "base_origin": "Rheingau, Germany", "dealcoholisation_method": "Spinning cone column (SCC)", "preserves": "Volatile aromatics preserved by low-temperature vacuum process"}),
  "slug": "leitz-eins-zwei-zero-riesling"
},
{
  "name": "Seedlip Spice 94",
  "category": "na_crafted",
  "subcategory": "distilled_na_spirit",
  "producer_id": None,
  "region_id": None,
  "origin_country": "UK",
  "description": "The pioneer of the NA spirits category — Ben Branson founded Seedlip in 2015 after reading a 17th century distillation text, and sold the company to Diageo in 2019. Spice 94 (the number refers to the allspice sourced from 94°W longitude in Jamaica) is a distilled non-alcoholic spirit based on allspice berry, cardamom, oak bark, lemon peel, and grapefruit peel. It is not a dealcoholised spirit — it was never alcoholic. The innovation: providing a complex botanical distillate that mixes in cocktails like gin but without the ethanol.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "Spice 94 (warm, peppery, versatile)", "position": 1}, {"label": "Garden 108 (herb-focused, lighter)", "position": 2}, {"label": "Grove 42 (citrus-forward)", "position": 3}]),
  "deductive_profile": json.dumps({"colour": "Crystal clear", "aroma": "Allspice, cardamom, oak, citrus peel, warm spice", "flavour": "Warm spice upfront, oak, allspice, bitter finish (the oak tannin provides the 'grip' that alcohol normally provides)", "finish": "Dry, slightly bitter, spicy — the closest to gin-without-alcohol in terms of cocktail function", "limitation": "Lacks the mouthfeel and carrying power of alcohol — dilutes more noticeably in long cocktails"}),
  "service_specs": json.dumps({"cocktail": "Seedlip Spice 94 & Ginger Ale (simplest and best), Seedlip Spritz (Seedlip + soda + cucumber), NA Negroni substitute", "glass": "Rocks or highball", "garnish": "Grapefruit peel, cardamom pod, or ginger", "price_point_justification": "$15 NA cocktail: 50ml Seedlip + 100ml premium tonic + fresh garnish = meaningful experience + correct price"}),
  "flavour_markers": ["allspice", "cardamom", "oak-bark", "citrus-peel", "warm-spice", "dry-bitter"],
  "flavour_weight": "light",
  "flavour_profile_type": "botanical-spiced",
  "origin_brand": "Seedlip",
  "price_tier": "premium",
  "price_range_cad": "$35-45",
  "technical_specs": json.dumps({"abv_pct": 0, "botanicals": ["allspice berry", "cardamom", "oak bark", "lemon peel", "grapefruit peel"], "method": "Distillation — each botanical separately distilled and blended", "owned_by": "Diageo (since 2019)"}),
  "slug": "seedlip-spice-94"
},
{
  "name": "GT's Synergy Organic Kombucha — Gingerade",
  "category": "na_fermented",
  "subcategory": "kombucha_live",
  "producer_id": None,
  "region_id": None,
  "origin_country": "USA",
  "description": "GT's Living Foods was the company that created the commercial kombucha category in the USA (1995) — founder GT Dave began selling his mother's home kombucha recipe after it helped her during cancer treatment. GT's Synergy Gingerade is the brand's most recognisable expression: raw, unfiltred kombucha with fresh pressed ginger juice, producing an intensely gingery, pleasantly acidic, slightly effervescent drink that is genuinely complex and food-pairing worthy.",
  "quality_tier": "market",
  "quality_hierarchy": json.dumps([{"label": "GT's Original (unflavoured, most complex, vinegary)", "position": 1}, {"label": "Synergy Gingerade (ginger — most food-friendly)", "position": 2}, {"label": "Synergy Trilogy (lemon, ginger, raspberry)", "position": 3}, {"label": "Alive Cultures Seasoning (BC — sommelier's choice)", "position": 4}]),
  "deductive_profile": json.dumps({"colour": "Amber-gold (gingerade), slightly cloudy", "aroma": "Fresh ginger, apple cider vinegar, tea, slight effervescence", "flavour": "Tart, gingery, kombucha acidity, slight sweetness, fizzy", "finish": "Clean, ginger-spicy, refreshing acid"}),
  "service_specs": json.dumps({"glass": "Wine glass or highball (elevated presentation)", "serve_temp_c": 6, "food_pairing": "Grilled fish, sushi, dim sum, salads, steamed vegetables — the ginger-acid combination is enormously food-friendly", "professional_note": "Offer from a wine decanter or carafe at table — the experience is elevated significantly by the vessel and presentation"}),
  "flavour_markers": ["ginger", "acetic-acid", "tea", "apple", "effervescent", "refreshing"],
  "flavour_weight": "light",
  "flavour_profile_type": "acidic-effervescent",
  "origin_brand": "GT's Living Foods",
  "price_tier": "value",
  "price_range_cad": "$5-7",
  "technical_specs": json.dumps({"abv_pct": 0.5, "scoby": "Live SCOBY culture", "base_tea": "Black and green tea blend", "secondary_fermentation": "Bottle-conditioned — live cultures present", "raw_unpasteurised": True, "available_at": "BC Whole Foods, Choices, Thrifty Foods, independent grocers"}),
  "slug": "gts-synergy-gingerade-kombucha"
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for p in PRODUCTS:
        try:
            cur.execute(SQL, (
                p["name"], p["category"], p.get("subcategory"),
                p.get("producer_id"), p.get("region_id"), p.get("origin_country"),
                p.get("description"), p.get("quality_tier"),
                p.get("quality_hierarchy"), p.get("deductive_profile"),
                p.get("service_specs"), p.get("flavour_markers"),
                p.get("flavour_weight"), p.get("flavour_profile_type"),
                p.get("origin_brand"), p.get("price_tier"),
                p.get("price_range_cad"), p.get("technical_specs"),
                True, p.get("slug")
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT product id={row[0]}: {row[1]}")
                inserted += 1
            else:
                print(f"  SKIP (exists): {p['name']}")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR {p['name']}: {e}")
    print(f"\nDone. {inserted} products inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
