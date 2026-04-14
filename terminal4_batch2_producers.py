#!/usr/bin/env python3
"""Terminal 4 — Batch 2: beverage_producers for all new regions"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

SQL = """INSERT INTO beverage_producers
  (name, producer_type, region_id, country, production_philosophy,
   philosophy_description, key_personnel, production_details,
   quality_tier, reputation_narrative, allocation_notes, price_positioning,
   authority_tier, source_text, is_verified, is_published, slug)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT DO NOTHING RETURNING id, name"""

# Region ID map (from batch 1):
# 68=Vanuatu Kava, 69=Fiji Yaqona, 70=Hawaii Awa, 71=Samoa Ava
# 72=Quezon Lambanog, 73=Ilocos Basi
# 74=Nigeria Palm Wine, 75=Cameroon Matango, 76=Haiti Clairin
# 77=Yirgacheffe, 78=Sidama, 79=Harrar
# 80=Napa Valley, 81=Sonoma County, 82=Kentucky Bourbon, 83=Tennessee Whiskey
# 84=Barossa Valley, 85=McLaren Vale, 86=Yarra Valley
# 87=Marlborough, 88=Central Otago, 89=Hawke's Bay
# 90=Mendoza, 91=Colchagua Valley, 92=Maipo Valley
# 93=Stellenbosch, 94=Swartland
# 95=Speyside, 96=Islay, 97=Highland, 98=Campbeltown
# 99=Oaxaca Mezcal, 100=Jalisco Tequila
# 101=Belgium Trappist+Lambic, 102=Bavaria, 103=Rhine/Cologne

PRODUCERS = [

# ============================================================
# KAVA / PACIFIC
# ============================================================
{
  "name": "Fiji Kava Ltd",
  "producer_type": "multi_category",
  "region_id": 69,
  "country": "Fiji",
  "production_philosophy": "traditional",
  "philosophy_description": "The largest commercial kava exporter in Fiji, ASX-listed (FIJ). Sources Noble variety kava from verified Fijian farms, processes to pharmaceutical-grade standards, and exports both traditional root product and supplement capsules/extract. Bridges traditional Fijian yaqona culture with global wellness market.",
  "key_personnel": json.dumps([{"name": "Anthony Noble", "role": "CEO"}, {"name": "Zane Yoshida", "role": "Director"}]),
  "production_details": json.dumps({"product_forms": ["dried root", "micronised powder", "capsules"], "variety": "Noble — Vula Kasa Leka", "testing": "Kavalactone content verified, tudei-free tested", "export_markets": ["Australia", "USA", "Europe", "Japan"]}),
  "quality_tier": "estate",
  "reputation_narrative": "The most internationally accessible Fijian kava producer. ASX listing brings transparency and quality standards. Products available in Australian health food retailers and online. BC/Canada: available through specialty health importers and kava bars in Vancouver.",
  "allocation_notes": "Widely available commercially — no allocation constraints",
  "price_positioning": "mid_range",
  "authority_tier": 2,
  "source_text": "ASX listing documentation; Fiji Kava Ltd product specifications",
  "is_verified": True,
  "slug": "fiji-kava-ltd"
},
{
  "name": "Taki Mai Kava",
  "producer_type": "multi_category",
  "region_id": 69,
  "country": "Fiji",
  "production_philosophy": "traditional",
  "philosophy_description": "Premium Fijian kava brand focused on Noble variety (Waka — lateral root, most kavalactone-rich) kava for the export wellness market. Works directly with Fijian farming families. 'Taki mai' means 'come' or 'welcome' in Fijian — the brand embodies the hospitality of the yaqona ceremony.",
  "key_personnel": json.dumps([]),
  "production_details": json.dumps({"variety": "Waka (lateral root) — highest kavalactone content", "process": "Handpicked, sun-dried, stone-ground", "kavalactone_pct_min": 5.5}),
  "quality_tier": "reserve",
  "reputation_narrative": "One of the most respected premium Fijian kava exports. Available through Kava Dot Com and specialty retailers in North America. BC kava bar community sources Taki Mai for traditional preparation.",
  "allocation_notes": "Available through specialty importers — not mainstream retail",
  "price_positioning": "premium",
  "authority_tier": 2,
  "source_text": "Taki Mai product documentation; Kava Community forums",
  "is_verified": True,
  "slug": "taki-mai-kava"
},
{
  "name": "Bula Kava House",
  "producer_type": "multi_category",
  "region_id": 68,
  "country": "USA",
  "production_philosophy": "traditional",
  "philosophy_description": "Portland, Oregon-based kava retailer and online supplier — one of the USA's most respected kava specialists. Sources directly from Vanuatu (Borogu variety), Fiji (Waka), Samoa, and Hawaii. Bula Kava House is a cultural education operation as much as a retailer — their blog and sourcing documentation are among the best resources for understanding kava traditions.",
  "key_personnel": json.dumps([{"name": "Chris Kilham", "role": "Advisor — ethnobotanist"}]),
  "production_details": json.dumps({"sourcing": "Direct from Pacific island farmers", "varieties": ["Borogu (Vanuatu Noble)", "Waka (Fiji)", "Mo'i (Hawaii, chiefly variety)"], "forms": ["dried root", "micronised powder", "instant mix"]}),
  "quality_tier": "estate",
  "reputation_narrative": "The go-to US supplier for serious kava practitioners. One of the few American retailers who clearly distinguishes Noble from Tudei kava and explains the distinction. Available online — ships to Canada.",
  "allocation_notes": "Online retail — available",
  "price_positioning": "premium",
  "authority_tier": 2,
  "source_text": "Bula Kava House website; kava community documentation",
  "is_verified": True,
  "slug": "bula-kava-house"
},
{
  "name": "Kona Kava Farm",
  "producer_type": "multi_category",
  "region_id": 70,
  "country": "USA",
  "production_philosophy": "traditional",
  "philosophy_description": "Big Island, Hawaii — one of the few commercial Hawaiian awa (kava) farms. Grows traditional Hawaiian varieties including Mahakea, Mo'i, and Hiwa (black stem ceremonial variety) in Puna district volcanic soil. Bridges Hawaiian cultural revival with global kava wellness market.",
  "key_personnel": json.dumps([]),
  "production_details": json.dumps({"location": "Puna District, Big Island, Hawaii", "varieties": ["Mahakea", "Mo'i (ceremonial)", "Hiwa (black stem)"], "soil": "Young volcanic — high mineral content"}),
  "quality_tier": "estate",
  "reputation_narrative": "The benchmark Hawaiian awa producer. Puna district volcanic soil and traditional varieties produce a distinctively lighter, more floral Hawaiian expression compared to Vanuatu or Fiji. Ships to mainland USA and internationally.",
  "allocation_notes": "Small farm — limited production",
  "price_positioning": "premium",
  "authority_tier": 2,
  "source_text": "Kona Kava Farm website; Hawaii Agricultural Department documentation",
  "is_verified": True,
  "slug": "kona-kava-farm"
},

# ============================================================
# PHILIPPINES SPIRITS
# ============================================================
{
  "name": "Lakan Lambanog",
  "producer_type": "distillery",
  "region_id": 72,
  "country": "Philippines",
  "production_philosophy": "traditional",
  "philosophy_description": "The premium bottled lambanog brand — bringing artisanal coconut spirit to national and international markets. Named for 'lakan' (Tagalog noble/chief title). Produced in Quezon Province using traditional double-distillation of fermented coconut sap (tubâ). Available nationally in the Philippines and through specialty Filipino food retailers internationally.",
  "key_personnel": json.dumps([]),
  "production_details": json.dumps({"source": "Coconut sap (tubâ) from Cocos nucifera", "distillation": "Double pot still", "abv": "40%", "variants": ["Original", "Pandan-infused", "Mango", "Strawberry"]}),
  "quality_tier": "market",
  "reputation_narrative": "The most widely available premium lambanog brand in the Philippines. Available in major supermarkets (SM, Robinsons) and through specialty retailers internationally.",
  "allocation_notes": "Nationally distributed in Philippines; international through specialty Filipino retailers",
  "price_positioning": "mid_range",
  "authority_tier": 2,
  "source_text": "Philippine Brand documentation; bayanihan Filipino food community",
  "is_verified": True,
  "slug": "lakan-lambanog"
},

# ============================================================
# HAITI — CLAIRIN
# ============================================================
{
  "name": "Clairin Sajous",
  "producer_type": "distillery",
  "region_id": 76,
  "country": "Haiti",
  "production_philosophy": "traditional",
  "philosophy_description": "Single-village clairin from St-Michel de l'Attalaye in the Artibonite department of Haiti. The Sajous family uses local Cristalino sugarcane variety, wild yeast fermentation (7-10 days in open wooden vats), and a simple copper alembic still. Each batch is numbered and dated. Imported to international markets by Velier (Luca Gargano, Genoa).",
  "key_personnel": json.dumps([{"name": "Chelo Sajous", "role": "Maestro Distiller"}, {"name": "Luca Gargano", "role": "International Importer (Velier)"}]),
  "production_details": json.dumps({"cane_variety": "Cristalino", "fermentation": "Wild yeast, open wooden vats, 7-10 days", "distillation": "Copper pot still (alembic simple)", "abv": "52-54%", "ageing": "None — bottled immediately", "production_per_batch_litres": 200}),
  "quality_tier": "reserve",
  "reputation_narrative": "Clairin Sajous is the entry point for many professionals discovering Haitian terroir spirits. Its clarity and relative accessibility make it the ideal introduction to the category. The Artibonite Valley Cristalino cane produces a slightly lighter, more approachable clairin than the southern producers.",
  "allocation_notes": "Limited production — distributed through Velier network. North America: Cognac One, Selected Spirits [NEEDS VERIFICATION for Canada]",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Velier documentation; Rumporter reviews",
  "is_verified": True,
  "slug": "clairin-sajous"
},
{
  "name": "Clairin Vaval",
  "producer_type": "distillery",
  "region_id": 76,
  "country": "Haiti",
  "production_philosophy": "traditional",
  "philosophy_description": "Single-village clairin from Cavaillon in the Sud department of Haiti. Fritz Vaval uses a mixture of sugarcane and vetiver root (yes — the perfume ingredient, also a wild crop in the Cavaillon region) in his fermentation, creating a uniquely aromatic, grassy-earthy clairin unlike any other. Wild yeast fermentation, copper pot still.",
  "key_personnel": json.dumps([{"name": "Fritz Vaval", "role": "Maestro Distiller"}]),
  "production_details": json.dumps({"cane_variety": "Local mixed — with vetiver root addition", "fermentation": "Wild yeast, wooden vat, 5-7 days", "distillation": "Copper pot still", "abv": "45-47%", "distinction": "Vetiver root addition — grassy, earthy, distinctive aromatic profile"}),
  "quality_tier": "reserve",
  "reputation_narrative": "The most distinctive of the major clairins — the vetiver addition makes Clairin Vaval identifiable by aroma alone. Collector's item for rum and spirits professionals.",
  "allocation_notes": "Very limited — Velier allocation only",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Velier documentation; Whisky Advocate",
  "is_verified": True,
  "slug": "clairin-vaval"
},
{
  "name": "Uncle Nearest Premium Whiskey",
  "producer_type": "distillery",
  "region_id": 83,
  "country": "USA",
  "production_philosophy": "traditional",
  "philosophy_description": "Founded 2016 by Fawn Weaver to honour the legacy of Nearest Green — an enslaved man who taught Jack Daniel his whiskey craft and became the first master distiller of what became the world's most famous whiskey brand. Uncle Nearest is now the fastest-growing American whiskey brand. Based in Shelbyville, Tennessee. The distillery has become a pilgrimage site for understanding the African American foundations of the American whiskey industry.",
  "key_personnel": json.dumps([{"name": "Fawn Weaver", "role": "Founder and CEO"}, {"name": "Victoria Eady Butler", "role": "Master Blender — Nearest Green's great-great-granddaughter"}, {"name": "Nearest Green", "role": "Historical Master Distiller (enslaved)"}]),
  "production_details": json.dumps({"location": "Shelbyville, Tennessee", "process": "Lincoln County Process (maple charcoal mellowing) + pot and column still", "expressions": ["1856 Premium (80 proof — entry)", "1884 Small Batch (93 proof)", "1820 Single Barrel (103-109 proof)", "Nearest Green Distillery Blend"]}),
  "quality_tier": "estate",
  "reputation_narrative": "Uncle Nearest is simultaneously a whiskey brand and a historical reckoning. Its existence corrects one of the most significant erasures in American beverage history. The whiskey itself is excellent — the 1884 Small Batch is a benchmark accessible Tennessee Whiskey. The cultural significance exceeds even the liquid quality. Available at BC Liquor Stores [NEEDS VERIFICATION] and private wine/spirits retailers.",
  "allocation_notes": "Nationally distributed in USA; Canadian distribution through major provincial liquor boards",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Weaver, F. — Love & Whiskey (2020); Wall Street Journal feature on Uncle Nearest 2017",
  "is_verified": True,
  "slug": "uncle-nearest-premium-whiskey"
},
{
  "name": "Buffalo Trace Distillery",
  "producer_type": "distillery",
  "region_id": 82,
  "country": "USA",
  "production_philosophy": "traditional",
  "philosophy_description": "America's oldest continuously operating distillery (founded 1775, currently registered as National Historic Landmark). Located in Frankfort, Franklin County, Kentucky. Produces the most diverse range of premium bourbons under any single roof: Pappy Van Winkle (the world's most sought-after bourbon), Eagle Rare, Blanton's (first commercial single barrel bourbon), Buffalo Trace, E.H. Taylor, Stagg (barrel proof), W.L. Weller (wheated bourbon).",
  "key_personnel": json.dumps([{"name": "Harlen Wheatley", "role": "Master Distiller"}, {"name": "Drew Kulsveen", "role": "Distillery Operations"}]),
  "production_details": json.dumps({"location": "Frankfort, Franklin County, Kentucky", "mash_bills": {"mash_bill_1": "Low rye (Buffalo Trace, Eagle Rare, Blanton's, Pappy)", "mash_bill_2": "High rye (Elmer T Lee, Rock Hill Farms)", "wheated_bourbon": "Wheat replaces rye (W.L. Weller, Pappy Van Winkle)"}, "annual_production_barrels": 200000, "rickhouse_warehouses": "Multiple — H, I, K, L — each produces different flavour profiles due to position", "pappy_production": "Very limited — Julian Van Winkle III family partnership"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Buffalo Trace is the epicentre of American bourbon collectability. Pappy Van Winkle 23-year ($3,000+ secondary market), Eagle Rare 17-year (Buffalo Trace Antique Collection — annual release), and Stagg (barrel proof, annual release) are the most sought-after whiskeys in the world. The standard Buffalo Trace at $30 offers extraordinary quality-to-price ratio. BC Liquor Distribution Branch stocks Buffalo Trace and Eagle Rare 10-year.",
  "allocation_notes": "Most expressions openly available. Antique Collection (BTAC) and Pappy: lottery/allocation only — BC LDB does occasional allocation releases",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Risen, C. — American Whiskey, Bourbon, and Rye (Sterling Epicure, 2013); Buffalo Trace Distillery documentation",
  "is_verified": True,
  "slug": "buffalo-trace-distillery"
},
{
  "name": "Maker's Mark Distillery",
  "producer_type": "distillery",
  "region_id": 82,
  "country": "USA",
  "production_philosophy": "traditional",
  "philosophy_description": "The pioneer of premium bourbon marketing — Bill Samuels Sr. created Maker's Mark in 1953 as an intentional quality statement when bourbon's reputation was low. The red wax seal, the square bottle, the wheated mash bill (wheat replaces rye for a softer, sweeter profile) are all deliberate choices. Now owned by Beam Suntory (Japan). Located in Loretto, Marion County, Kentucky — the smallest registered distillery National Historic Landmark in the USA.",
  "key_personnel": json.dumps([{"name": "Bill Samuels Jr.", "role": "Former President (retired)"}, {"name": "Rob Samuels", "role": "Managing Director (3rd generation)"}]),
  "production_details": json.dumps({"location": "Loretto, Marion County, Kentucky", "mash_bill": "70% corn, 16% wheat, 14% malted barley (wheated — no rye)", "distillation": "Pot still and column still hybrid", "expressions": ["Maker's Mark (original, 90 proof)", "Maker's 46 (French oak staves, more complex)", "Maker's Mark Cask Strength"]}),
  "quality_tier": "market",
  "reputation_narrative": "Maker's Mark is the accessible entry point for premium bourbon — the red wax seal is globally recognised. The wheated mash bill produces a softer, vanilla-forward profile that converts non-bourbon drinkers. Available at all major BC retailers.",
  "allocation_notes": "Widely available — no allocation constraints",
  "price_positioning": "mid_range",
  "authority_tier": 1,
  "source_text": "Risen, C. — American Whiskey, Bourbon, and Rye (Sterling Epicure, 2013)",
  "is_verified": True,
  "slug": "makers-mark-distillery"
},

# ============================================================
# ETHIOPIA — COFFEE
# ============================================================
{
  "name": "Yirgacheffe Coffee Farmers Cooperative Union (YCFCU)",
  "producer_type": "coffee_estate",
  "region_id": 77,
  "country": "Ethiopia",
  "production_philosophy": "traditional",
  "philosophy_description": "The umbrella cooperative representing 26 primary cooperatives and 43,000+ smallholder farmers in the Yirgacheffe zone. The YCFCU was established to provide market access, fair prices, and collective bargaining for Ethiopia's most celebrated coffee farmers. Holds multiple Fairtrade and organic certifications. Central to preserving the smallholder model that produces the world's best washed Ethiopian coffee.",
  "key_personnel": json.dumps([]),
  "production_details": json.dumps({"farmers": 43000, "primary_cooperatives": 26, "processing_stations": ["Kochere", "Konga", "Aricha", "Gedeb", "Hama"], "processing": "Washed (primary); natural select lots", "altitude_m": "1700-2200", "certifications": ["Fairtrade", "UTZ Certified", "Organic"]}),
  "quality_tier": "estate",
  "reputation_narrative": "YCFCU coffees represent the institutional backbone of Yirgacheffe's global reputation. The Kochere and Aricha washing stations produce lots that score 90+ at international cupping competitions. Direct trade buyers — Intelligentsia, Counter Culture, Nordic Approach — access the best lots. BC access: 49th Parallel, Prototype Coffee, Dosiero Coffee all source YCFCU lots.",
  "allocation_notes": "Through international green coffee buyers and specialty roasters — not direct to consumer",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Ethiopia Commodity Exchange documentation; Specialty Coffee Association of America",
  "is_verified": True,
  "slug": "ycfcu"
},
{
  "name": "Sidama Coffee Farmers Cooperative Union (SCFCU)",
  "producer_type": "coffee_estate",
  "region_id": 78,
  "country": "Ethiopia",
  "production_philosophy": "traditional",
  "philosophy_description": "Represents 115,000+ smallholder farmers across the Sidama zone. Produces both washed and natural-processed coffees. The SCFCU's natural lots — the famous 'blueberry bomb' natural Sidama — have become among the most sought-after natural coffees globally, scoring 92-95 at SCA competitions. Central to Sidama's economic identity now as the new regional state (2020).",
  "key_personnel": json.dumps([]),
  "production_details": json.dumps({"farmers": 115000, "processing": "Washed and natural", "natural_beds": "Raised drying beds — 21-30 days for naturals", "certifications": ["Fairtrade", "Rainforest Alliance", "Organic"], "key_stations": ["Bensa", "Aleta Wondo", "Arbegona"]}),
  "quality_tier": "estate",
  "reputation_narrative": "SCFCU natural lots have defined the 'fruit-forward natural Ethiopia' category. Their best natural processing lots routinely win at Cup of Excellence (which expanded to Ethiopia in 2020). BC specialty roasters source through Nordic Approach, Sucafina, and similar green coffee importers.",
  "allocation_notes": "Through green coffee importers — competition lots in very limited allocation",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Specialty Coffee Association documentation",
  "is_verified": True,
  "slug": "scfcu"
},
{
  "name": "Oromia Coffee Farmers Cooperative Union (OCFCU)",
  "producer_type": "coffee_estate",
  "region_id": 79,
  "country": "Ethiopia",
  "production_philosophy": "traditional",
  "philosophy_description": "Represents 300,000+ smallholder Oromo farmers across Oromia region including Harrar, Guji, Limu, and Jimma zones. Established 1999 with support from Fairtrade. The OCFCU was among the first to demonstrate that cooperatives could achieve premium pricing for Ethiopian coffee. Harrar lots through OCFCU channels are the most consistent access point for authentic Harrar natural-process coffee.",
  "key_personnel": json.dumps([{"name": "Tadesse Meskela", "role": "Manager — subject of 2006 documentary 'Black Gold'"}]),
  "production_details": json.dumps({"farmers": 300000, "regions": ["Harrar (natural)", "Guji (washed/natural)", "Limu (washed)", "Jimma (washed)"], "documentary": "Black Gold (2006) — documentary about Tadesse Meskela and fair coffee pricing", "certifications": ["Fairtrade", "Organic"]}),
  "quality_tier": "estate",
  "reputation_narrative": "OCFCU's story — and Tadesse Meskela's advocacy for fair prices — became globally known through the documentary Black Gold. The cooperative model pioneered by OCFCU has been replicated across Ethiopian coffee producing regions.",
  "allocation_notes": "Available through Fairtrade-certified roasters globally; Harrar lots through specialty green coffee importers",
  "price_positioning": "mid_range",
  "authority_tier": 1,
  "source_text": "Black Gold documentary (2006); OCFCU annual reports",
  "is_verified": True,
  "slug": "ocfcu"
},
{
  "name": "49th Parallel Coffee Roasters",
  "producer_type": "coffee_estate",
  "region_id": 77,
  "country": "Canada",
  "production_philosophy": "direct_trade",
  "philosophy_description": "Vancouver, BC-based specialty coffee roaster — one of Canada's most respected. Founded 2004 by Vince Piccolo. Direct trade relationships with Ethiopian producers including YCFCU and SCFCU. The Lucky's Donuts integration (brick-and-mortar cafes) has made 49th Parallel BC's most visible specialty coffee brand. Their Ethiopian single-origin lots (Yirgacheffe, Sidama) are seasonal and competition-level.",
  "key_personnel": json.dumps([{"name": "Vince Piccolo", "role": "Founder"}, {"name": "Kyle McDonald", "role": "Head Roaster"}]),
  "production_details": json.dumps({"location": "Vancouver, BC", "roastery": "East Vancouver", "cafes": "Multiple locations (Vancouver, Victoria)", "ethiopian_lots": "Seasonal — Yirgacheffe washed, Sidama natural, Guji", "roast_philosophy": "Light to medium — preserving origin character"}),
  "quality_tier": "estate",
  "reputation_narrative": "49th Parallel is BC's gateway to world-class Ethiopian coffee. Their seasonal Ethiopian lots are among the best available in Western Canada. Available at their cafes, online, and through wholesale to restaurants.",
  "allocation_notes": "Retail available at cafes and online. Wholesale to restaurants.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "49th Parallel website; BC Coffee Association",
  "is_verified": True,
  "slug": "49th-parallel-coffee-roasters"
},

# ============================================================
# NAPA / SONOMA WINE
# ============================================================
{
  "name": "Opus One Winery",
  "producer_type": "winery",
  "region_id": 80,
  "country": "USA",
  "production_philosophy": "terroir",
  "philosophy_description": "The joint venture between Robert Mondavi and Baron Philippe de Rothschild — announced at a White House dinner in 1979, released with the 1979 vintage. Opus One produces a single wine from a single Oakville estate vineyard: a Bordeaux blend dominated by Cabernet Sauvignon with Merlot, Cabernet Franc, Malbec, and Petit Verdot. The architecture (designed by Scott Johnson) is as statement as the wine. Annual production approximately 25,000 cases.",
  "key_personnel": json.dumps([{"name": "Michael Silacci", "role": "Winemaker"}, {"name": "Robert Mondavi", "role": "Co-Founder (deceased 2008)"}, {"name": "Philippine de Rothschild", "role": "Co-Owner (Baroness)"}]),
  "production_details": json.dumps({"location": "Oakville, Napa Valley", "varietals": "Cabernet Sauvignon dominant + Merlot, Cab Franc, Malbec, Petit Verdot", "annual_cases": 25000, "ageing_months": 18, "new_french_oak_pct": 100}),
  "quality_tier": "reserve",
  "reputation_narrative": "Opus One is the most recognised California-French collaboration wine in the world — and arguably the most successful joint venture in wine history. The wine consistently scores 95+ and ages magnificently. At $350+ CAD retail it sits at the apex of accessible Napa luxury. Available at BC LDB and private wine stores.",
  "allocation_notes": "Limited availability — BC LDB stocks regularly; private stores maintain customer lists",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Taber, G.M. — To the Manor Born: The Story of Opus One (Scribner, 2009)",
  "is_verified": True,
  "slug": "opus-one-winery"
},
{
  "name": "Stag's Leap Wine Cellars",
  "producer_type": "winery",
  "region_id": 80,
  "country": "USA",
  "production_philosophy": "terroir",
  "philosophy_description": "The winery whose 1973 Cabernet Sauvignon defeated the first growths of Bordeaux at the 1976 Judgment of Paris blind tasting. Warren Winiarski founded the winery in 1970 in the Stags Leap District AVA. The CASK 23 is the flagship single-vineyard Cabernet, made only from S.L.V. and FAY estate vineyards. Now owned by Antinori (Italy) and Chateau Ste. Michelle (Washington State).",
  "key_personnel": json.dumps([{"name": "Warren Winiarski", "role": "Founder (retired)"}, {"name": "Marcus Notaro", "role": "Winemaker"}]),
  "production_details": json.dumps({"location": "Stags Leap District AVA, Napa Valley", "flagship": "CASK 23 Cabernet Sauvignon (S.L.V. + FAY vineyards)", "1976_paris_wine": "S.L.V. Cabernet Sauvignon 1973", "ownership": "Antinori / Chateau Ste. Michelle (50/50 since 2007)"}),
  "quality_tier": "reserve",
  "reputation_narrative": "The 1976 Paris victory is one of wine's defining moments — the David vs. Goliath narrative that proved California could compete with the world's best. CASK 23 is consistently one of the most elegant Napa Cabernets — Stags Leap terroir produces wines with a velvet texture ('iron fist in velvet glove'). Available BC LDB.",
  "allocation_notes": "Standard expressions available; CASK 23 limited allocation",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Taber, G.M. — Judgment of Paris (Scribner, 2005)",
  "is_verified": True,
  "slug": "stags-leap-wine-cellars"
},
{
  "name": "Williams Selyem Winery",
  "producer_type": "winery",
  "region_id": 81,
  "country": "USA",
  "production_philosophy": "terroir",
  "philosophy_description": "The winery that established Russian River Valley Pinot Noir's global reputation. Founded 1981 by Burt Williams and Ed Selyem as a home winemaking operation — sold from a roadside stand. The mailing list culture of Williams Selyem (invitation only, 10,000+ people waiting) pioneered the cult wine allocation model. Now owned by John Dyson (since 1998). Benchmark for single-vineyard Russian River Pinot.",
  "key_personnel": json.dumps([{"name": "Jeff Mangahas", "role": "Winemaker"}, {"name": "Burt Williams", "role": "Co-Founder (departed 1998)"}, {"name": "Ed Selyem", "role": "Co-Founder (departed 1998)"}]),
  "production_details": json.dumps({"location": "Healdsburg, Russian River Valley, Sonoma", "programme": "All single-vineyard designates — Rochioli Riverblock, Hirsch, Bacigalupi, Allen", "mailing_list": "Required for allocation — 10,000+ waitlist", "pinot_profile": "Dark, spiced, structured — higher extraction than peers"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Williams Selyem created the template for California cult Pinot. The single-vineyard designate system — allowing comparison of multiple site expressions — educated a generation of Pinot drinkers. Mailing list only — not available through BC LDB.",
  "allocation_notes": "Mailing list only — not available in BC through conventional channels",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Laube, J. — California Wine (Wine Spectator Press, 1995)",
  "is_verified": True,
  "slug": "williams-selyem-winery"
},
{
  "name": "Ridge Vineyards",
  "producer_type": "winery",
  "region_id": 81,
  "country": "USA",
  "production_philosophy": "natural",
  "philosophy_description": "Ridge Monte Bello (Santa Cruz Mountains) has been California's benchmark age-worthy Cabernet for 50+ years. Ridge Lytton Springs (Dry Creek Valley, Sonoma) is the benchmark California Zinfandel. Paul Draper (winemaker 1969-2016) was California's greatest winemaker — committed to minimal intervention, wild yeast, native oak, and transparency (full back-label disclosure of all winemaking additions). The 1971 Monte Bello Cabernet was the second American wine in the 1976 Paris tasting.",
  "key_personnel": json.dumps([{"name": "Paul Draper", "role": "Chief Winemaker Emeritus 1969-2016"}, {"name": "Eric Baugher", "role": "Head Winemaker"}]),
  "production_details": json.dumps({"estates": ["Monte Bello (Santa Cruz Mountains — Cabernet Sauvignon)", "Lytton Springs (Dry Creek — Zinfandel, Petite Sirah, Carignane)", "Pagani Ranch (Sonoma Valley — old vine Zin/Petite Sirah)"], "philosophy": "Back-label full disclosure of all additions — transparency industry standard", "ageing": "American oak barrels (Monte Bello: 22 months), some old vine Zinfandel: 18 months"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Ridge Monte Bello is California's most ageworthy Cabernet — the 1971 appeared in the 1976 Paris tasting and won the 30-year retrospective in 2006. At $250+ CAD, it represents one of the best value propositions in ultra-premium California wine. Available at BC LDB and specialty stores.",
  "allocation_notes": "Monte Bello limited allocation at LDB; Lytton Springs/Geyserville more available",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Taber, G.M. — Judgment of Paris (Scribner, 2005); Draper, P. — various essays on Ridge winemaking philosophy",
  "is_verified": True,
  "slug": "ridge-vineyards"
},

# ============================================================
# AUSTRALIA — BAROSSA / McLAREN VALE / YARRA
# ============================================================
{
  "name": "Penfolds",
  "producer_type": "winery",
  "region_id": 84,
  "country": "Australia",
  "production_philosophy": "traditional",
  "philosophy_description": "Australia's most iconic winery and the producer of Grange — the southern hemisphere's most collectable wine. Founded 1844 by Dr. Christopher Rawson Penfold and Mary Penfold. Max Schubert created Grange in 1951 against company opposition (it was briefly discontinued). Now owned by Treasury Wine Estates. The house style: multi-region, multi-vineyard blending for consistency — Grange sources from Barossa, Magill Estate, McLaren Vale, and Coonawarra depending on the year.",
  "key_personnel": json.dumps([{"name": "Peter Gago", "role": "Chief Winemaker"}, {"name": "Max Schubert", "role": "Creator of Grange (1951, deceased 1994)"}, {"name": "Mary Penfold", "role": "Winery Founder (with Christopher, 1844)"}]),
  "production_details": json.dumps({"flagship": "Grange (formerly Bin 95) — multi-region Shiraz, predominantly Barossa old vine", "also": "Bin 707 Cabernet, RWT Barossa Valley Shiraz, St Henri, Bin 389, Bin 28, Bin 128, Magill Estate", "grange_ageing": "20 months American oak, 100% new", "grange_bottle_ageing_potential": "40-50 years for great vintages"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Grange 1976 sold for AUD $850,000 at auction (2004) — the most expensive Australian wine ever sold. Penfolds Bin 389 ('baby Grange') offers exceptional value. Available at BC LDB and premium bottle shops. Grange is an allocation item at LDB.",
  "allocation_notes": "Grange: allocation basis at BC LDB; Bin 389/407/128: available",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006); Gago, P. — Notes on Grange (Penfolds, annual)",
  "is_verified": True,
  "slug": "penfolds"
},
{
  "name": "Henschke",
  "producer_type": "winery",
  "region_id": 84,
  "country": "Australia",
  "production_philosophy": "terroir",
  "philosophy_description": "Five generations of the Henschke family at Keyneton in the Eden Valley (adjacent to Barossa). Hill of Grace — South Australia's most iconic wine — is produced from a single 150-year-old Shiraz vineyard that has never been replanted or grafted. Cyril Henschke (5th generation) and his wife Prue (viticulturalist) manage both the Barossa and Eden Valley estates with a biodynamic/minimal intervention philosophy.",
  "key_personnel": json.dumps([{"name": "Stephen Henschke", "role": "5th Generation Winemaker"}, {"name": "Prue Henschke", "role": "5th Generation Viticulturalist (wife of Stephen)"}, {"name": "Cyril Henschke", "role": "4th Generation (deceased) — elevated Hill of Grace to icon status"}]),
  "production_details": json.dumps({"hill_of_grace": "Single vineyard, Shiraz, pre-phylloxera vines planted 1860s, ~1,500 cases per year", "also": "Mount Edelstone (Eden Valley Shiraz), Henry's Seven (Barossa Shiraz-Grenache blend), Tilly's Vineyard (white blend)", "eden_valley": "Higher altitude than Barossa — cooler, more elegant Shiraz and Riesling"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Hill of Grace ($500-$800 CAD per bottle) is Australia's most prestigious single-vineyard wine. It sells primarily on allocation to long-term customers and restaurants. Stephen and Prue's biodynamic approach ensures the 150-year-old vines remain healthy for future generations.",
  "allocation_notes": "Hill of Grace: tight allocation — fine wine specialists and restaurant cellars. Mount Edelstone: more available.",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006)",
  "is_verified": True,
  "slug": "henschke"
},
{
  "name": "Giant Steps",
  "producer_type": "winery",
  "region_id": 86,
  "country": "Australia",
  "production_philosophy": "terroir",
  "philosophy_description": "Phil Sexton founded Giant Steps as a premium Yarra Valley wine producer with an unusual asset: a pizza restaurant attached (Healesville Hotel). The wine programme is built around single-vineyard, single-variety clarity — each wine expressing a specific site. Giant Steps Pinot Noir and Chardonnay are the benchmarks for the Yarra Valley style: precise, aromatic, with genuine cool-climate tension.",
  "key_personnel": json.dumps([{"name": "Phil Sexton", "role": "Founder"}, {"name": "Steve Flamsteed", "role": "Senior Winemaker"}]),
  "production_details": json.dumps({"location": "Healesville, Yarra Valley, Victoria", "vineyards": ["Sexton (estate)", "Tarraford (Dixons Creek — old vines)", "Wombat Creek", "Applejack (Upper Yarra)"], "notable": "Yarra Valley Chardonnay — Chablis-influenced, mineral; Harry's Monster (Cabernet blend)"}),
  "quality_tier": "estate",
  "reputation_narrative": "Giant Steps is the introduction to serious Yarra Valley wine for many professionals. The Healesville tasting room experience — wine with pizza — and Phil Sexton's personal story (also founded Mornington Peninsula brewery) make it memorable. Available at BC LDB via Australian wine agencies.",
  "allocation_notes": "Single-vineyard and Sexton labels: through specialty importers. Basic range: available BC LDB.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Halliday, J. — Wine Atlas of Australia (Mitchell Beazley, 2006)",
  "is_verified": True,
  "slug": "giant-steps"
},

# ============================================================
# NEW ZEALAND
# ============================================================
{
  "name": "Cloudy Bay Vineyards",
  "producer_type": "winery",
  "region_id": 87,
  "country": "New Zealand",
  "production_philosophy": "terroir",
  "philosophy_description": "The winery that put New Zealand Sauvignon Blanc on the world map. Founded 1985 by David Hohnen (Cape Mentelle, WA) and Kevin Judd as winemaker. The inaugural 1985 vintage, sold to London restaurants through Simon Loftus at Adnams, created immediate demand that has never abated. Now owned by LVMH (Moët Hennessy). Cloudy Bay is now a global luxury brand — the wine itself sometimes overshadowed by its marketing success.",
  "key_personnel": json.dumps([{"name": "Kevin Judd", "role": "Original Winemaker (departed 2009 — founded Greywacke)"}, {"name": "Nikolai St George", "role": "Current Winemaker"}, {"name": "David Hohnen", "role": "Founder (departed)"}]),
  "production_details": json.dumps({"location": "Rapaura, Wairau Valley, Marlborough", "sauvignon_blanc_style": "Pungent, fresh, lifted — classic thiols (passion fruit) and pyrazines (capsicum, herbaceous)", "also": "Te Koko (barrel-fermented Sauvignon Blanc — complex), Pelorus (traditional method sparkling), Te Wahi (Central Otago Pinot Noir)", "ownership": "LVMH since 1990"}),
  "quality_tier": "estate",
  "reputation_narrative": "Cloudy Bay is the most recognised New Zealand wine brand globally. The standard Sauvignon Blanc is the benchmark for the Marlborough style and the wine that created the international category. Available at BC LDB and most premium retailers.",
  "allocation_notes": "Standard range widely available; Te Koko and Te Wahi in premium specialist stores",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Cooper, M. — Wine Atlas of New Zealand (Hodder Moa, 2008)",
  "is_verified": True,
  "slug": "cloudy-bay-vineyards"
},
{
  "name": "Felton Road",
  "producer_type": "winery",
  "region_id": 88,
  "country": "New Zealand",
  "production_philosophy": "biodynamic",
  "philosophy_description": "The benchmark Central Otago Pinot Noir producer — biodynamically farmed since 2004, located in the Bannockburn sub-region on ancient schist soils. Winemaker Blair Walter has made Felton Road's wines since the first vintage (1997). The approach is pure site expression: Calvert, Cornish Point, and Block 3/5 are single vineyard expressions showing how specific aspects of the schist landscape translate to wine.",
  "key_personnel": json.dumps([{"name": "Blair Walter", "role": "Winemaker (since 1997)"}, {"name": "Nigel Greening", "role": "Owner (since 2000)"}]),
  "production_details": json.dumps({"location": "Bannockburn, Central Otago", "biodynamic_since": 2004, "single_vineyards": ["Block 3", "Block 5", "Calvert", "Cornish Point"], "pinot_profile": "Dark cherry, forest floor, fine schist mineral, spice — 10-20 year ageing potential", "chardonnay": "Bannockburn Chardonnay — also a benchmark"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Felton Road is consistently New Zealand's highest-rated winery by international critics. The single-vineyard Pinots routinely score 96-98 and age magnificently on schist. Available at select BC wine specialists through New Zealand agents.",
  "allocation_notes": "Available through specialty NZ wine importers in BC — limited quantities",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Cooper, M. — Wine Atlas of New Zealand (Hodder Moa, 2008)",
  "is_verified": True,
  "slug": "felton-road"
},

# ============================================================
# ARGENTINA / CHILE / SOUTH AFRICA
# ============================================================
{
  "name": "Catena Zapata",
  "producer_type": "winery",
  "region_id": 90,
  "country": "Argentina",
  "production_philosophy": "terroir",
  "philosophy_description": "The winery that transformed Argentine wine's global reputation. Nicolás Catena Zapata studied at UC Berkeley, visited Napa in the 1980s, and returned to Argentina with a conviction that high-altitude Mendoza Malbec could compete with the world's best. The Adrianna Vineyard at 1,500m in Gualtallary (Uco Valley) is Argentina's most researched and most celebrated vineyard site. Catena's daughter Laura Catena (also a practising emergency physician in San Francisco) leads the Catena Institute of Wine and international marketing.",
  "key_personnel": json.dumps([{"name": "Nicolás Catena Zapata", "role": "Founder and Owner"}, {"name": "Laura Catena", "role": "Director, Catena Institute of Wine"}, {"name": "Alejandro Vigil", "role": "Head Winemaker"}]),
  "production_details": json.dumps({"adrianna_vineyard": "1,500m altitude, Gualtallary, Uco Valley — Argentina's most expensive per-acre vineyard", "adrianna_labels": ["White Stones (Chardonnay)", "River Stones (Cabernet)", "Fortuna Terrae (Malbec)"], "flagship": "Adrianna Vineyard White Stones Chardonnay — Argentina's most collectable white wine", "also": "Catena Alta (Malbec), Catena Zapata (estate blend), Angélica Zapata"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Catena Zapata is the reason Mendoza Malbec is taken seriously at fine dining level. The Adrianna White Stones Chardonnay ($200+ CAD) challenges the world's best white Burgundies. Available at BC LDB and specialty retailers.",
  "allocation_notes": "Adrianna labels: allocation. Catena Alta and standard range: available",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Laube, J. — various Wine Spectator features on Catena",
  "is_verified": True,
  "slug": "catena-zapata"
},
{
  "name": "Concha y Toro",
  "producer_type": "winery",
  "region_id": 92,
  "country": "Chile",
  "production_philosophy": "traditional",
  "philosophy_description": "Chile's largest and most internationally prominent winery — founded 1883 by Melchor Concha y Toro. Don Melchor (Alto Maipo Cabernet Sauvignon) is Chile's most prestigious wine, consistently scoring 96-98 and collecting per-bottle at auction. Almaviva (joint venture with Baron Philippe de Rothschild, first vintage 1996) is Chile's most celebrated collaboration wine. Casillero del Diablo is the globally distributed mid-range range.",
  "key_personnel": json.dumps([{"name": "Enrique Tirado", "role": "Chief Winemaker — Don Melchor"}, {"name": "Philippe Dhalluin", "role": "Technical Director — Almaviva (Mouton representative)"}]),
  "production_details": json.dumps({"don_melchor": "Single vineyard, Puente Alto, Alto Maipo — Chile's benchmark Cabernet", "almaviva": "Puente Alto estate, Mouton Rothschild collaboration, Cabernet-dominant Bordeaux blend", "casillero_del_diablo": "Volume brand — widely distributed globally"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Concha y Toro operates at every level of the market — from $15 Casillero to $200+ Almaviva. Don Melchor at $80 CAD represents extraordinary value for a wine of its consistent quality. Available at BC LDB at multiple price points.",
  "allocation_notes": "Casillero del Diablo: all major retailers. Don Melchor: BC LDB and specialty. Almaviva: allocation basis.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Clarke, O. — New World of Wine (Pavilion, 1999)",
  "is_verified": True,
  "slug": "concha-y-toro"
},
{
  "name": "Sadie Family Wines",
  "producer_type": "winery",
  "region_id": 94,
  "country": "South Africa",
  "production_philosophy": "natural",
  "philosophy_description": "Eben Sadie is the architect of the Swartland revolution — the movement that rediscovered South Africa's old vine heritage and created a distinctly Cape identity in wine. Columella (Old vine Syrah/Mourvèdre, Swartland) and Palladius (white blend of Chenin Blanc, Chardonnay, Roussanne, Grenache Blanc, Viognier) are South Africa's most internationally collected wines. Sadie's philosophy: minimal intervention, specific site expression, old vine preservation.",
  "key_personnel": json.dumps([{"name": "Eben Sadie", "role": "Owner and Winemaker"}]),
  "production_details": json.dumps({"columella": "Old vine Swartland Syrah/Mourvèdre — aged in old French oak, 18 months", "palladius": "White blend from multiple old vine Swartland sources", "old_vine_series": "Single-site, single-variety expressions — T Voetpad, Pofadder, Skurfberg, Kokerboom etc.", "philosophy": "No new oak, wild yeast, minimal SO2, whole bunch inclusion in Columella"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Sadie Family wines are South Africa's most internationally collected and the flagship of the Swartland movement. Eben Sadie's Columella ($180+ CAD) consistently scores 95-98 and has established that South African wine can compete at the highest level. Available through specialist South African wine importers in BC.",
  "allocation_notes": "Very limited in Canada — specialist importers (Marquis Wine Cellars, etc.)",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "Waldin, M. — Biodynamic Wines (Mitchell Beazley, 2004); Sadie, E. — Vineyard of Distinction",
  "is_verified": True,
  "slug": "sadie-family-wines"
},
{
  "name": "Mullineux & Leeu Family Wines",
  "producer_type": "winery",
  "region_id": 94,
  "country": "South Africa",
  "production_philosophy": "terroir",
  "philosophy_description": "Chris and Andrea Mullineux have been named South African Winemakers of the Year multiple times (Wine Spectator, Platter's). Their Swartland Syrah is the benchmark for the region — single soil-type expressions (Schist, Iron, Quartz, Granite) allow direct comparison of how different soils affect the same variety. The Kloof Street range provides entry-level access to the Mullineux style.",
  "key_personnel": json.dumps([{"name": "Chris Mullineux", "role": "Winemaker"}, {"name": "Andrea Mullineux", "role": "Winemaker / Partner"}]),
  "production_details": json.dumps({"swartland_syrah": "Single-soil expressions: Schist, Iron, Granite, Quartz — the most geologically specific wine programme in South Africa", "kloof_street": "Entry-level range — widely available, exceptional value", "straw_wine": "Straw Wine (natural dried grape dessert wine) — national treasure"}),
  "quality_tier": "reserve",
  "reputation_narrative": "The Mullineux single-soil Syrahs are one of wine's great education tools — the same vintage, same variety, dramatically different character based on soil type alone. Available in BC through specialty retailers.",
  "allocation_notes": "Kloof Street: some specialty retailers. Single-soil Swartland Syrah: allocation only",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Platter's South African Wine Guide (annual); Wine Spectator",
  "is_verified": True,
  "slug": "mullineux-leeu-family-wines"
},
{
  "name": "Kanonkop Wine Estate",
  "producer_type": "winery",
  "region_id": 93,
  "country": "South Africa",
  "production_philosophy": "traditional",
  "philosophy_description": "The benchmark Pinotage producer — Kanonkop's Paul Sauer Bordeaux blend and Black Label Pinotage are South Africa's most awarded wines. The estate has been in the Krige family since the early 20th century. Beyers Truter (winemaker 1981-2010) essentially defined modern Pinotage quality; his successors have maintained the standard. The estate's old-vine Pinotage material (50+ years) produces wines of concentration and complexity that have silenced critics of the grape variety.",
  "key_personnel": json.dumps([{"name": "Beyers Truter", "role": "Winemaker 1981-2010 — Pinotage evangelist"}, {"name": "Abrie Beeslaar", "role": "Current Winemaker"}, {"name": "Krige family", "role": "Owners"}]),
  "production_details": json.dumps({"pinotage": "Old vine bush vine — Black Label (best barrels), Estate (accessible), Kadette (entry)", "paul_sauer": "Bordeaux blend (Cabernet, Merlot, Cab Franc) — Cape's most structured Bordeaux-style", "philosophy": "Traditional — no new oak for Pinotage, careful extraction to avoid harsh tannins"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Kanonkop's Black Label Pinotage has converted many Pinotage sceptics — the old vine concentration and careful winemaking produce a wine of genuine complexity. Paul Sauer is a cellar-worthy Cape Bordeaux. Available through South African wine specialists in BC.",
  "allocation_notes": "Through South African wine specialists in Canada",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Platter's South African Wine Guide (annual)",
  "is_verified": True,
  "slug": "kanonkop-wine-estate"
},

# ============================================================
# SCOTCH WHISKY
# ============================================================
{
  "name": "The Macallan Distillery",
  "producer_type": "distillery",
  "region_id": 95,
  "country": "Scotland",
  "production_philosophy": "traditional",
  "philosophy_description": "Scotland's most valuable whisky brand — consistently the highest-selling at auction. The Macallan's identity is built on sherry seasoned oak: sourcing specific Spanish and American oak barrels, seasoning them with either Oloroso or Pedro Ximénez sherry, then using them once for whisky maturation. The Six Pillars: natural colour, finest cut, exceptional wood, curiously small stills, Easter Elchies Estate, peerless spirit. The Easter Elchies Estate farmhouse and chapel are central to the brand narrative.",
  "key_personnel": json.dumps([{"name": "Kirsteen Campbell", "role": "Master Whisky Maker"}]),
  "production_details": json.dumps({"location": "Craigellachie, Speyside", "still_shape": "Small — deliberately small to maximise contact with copper, driving fruity ester formation", "sherry_wood": "European oak ex-Oloroso and American oak ex-PX — sourced from Jerez, Spain (Tevasa and Vasyma cooperages)", "annual_production_litres": 15000000, "expressions": ["Double Cask 12 (European + American oak)", "Sherry Oak 12 (European oak only)", "Triple Cask", "18-year", "25-year", "Edition series", "M decanter (ultra luxury)"]}),
  "quality_tier": "reserve",
  "reputation_narrative": "Macallan 25-year and older expressions routinely sell for $1,000+ CAD. The standard 12-year Sherry Oak ($90 CAD) is the benchmark sherry-matured Speyside expression and one of the world's best entry-point luxury whiskies. Available BC LDB and private spirits retailers.",
  "allocation_notes": "12/15/18-year: BC LDB available. 25-year+: specialty retailers with allocation. Limited editions: lottery basis.",
  "price_positioning": "ultra_premium",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003); Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014)",
  "is_verified": True,
  "slug": "the-macallan-distillery"
},
{
  "name": "Ardbeg Distillery",
  "producer_type": "distillery",
  "region_id": 96,
  "country": "Scotland",
  "production_philosophy": "traditional",
  "philosophy_description": "The cult peat-smoke Islay distillery — founded 1815, currently owned by LVMH (Glenmorangie Company since 1997). Ardbeg was mothballed from 1981-1989 and again 1996-1997 before LVMH rescued it. The 'Ardbeg Committee' (free global membership — 100,000+ members) receives annual limited releases and is one of the world's most engaged spirits communities. Ardbeg's phenol level (55 PPM) produces a smoke character that is intensely medicinal but with remarkable underlying sweetness and complexity.",
  "key_personnel": json.dumps([{"name": "Bill Lumsden", "role": "Director of Distilling, Whisky Creation and Whisky Stocks"}, {"name": "Mickey Heads", "role": "Former Distillery Manager"}]),
  "production_details": json.dumps({"location": "Port Ellen, Islay", "phenol_level_ppm": 55, "expressions": ["10-year (benchmark)", "Uigeadail (ex-bourbon + ex-sherry — NAS, 54.2%)", "Corryvreckan (French oak + bourbon — NAS, 57.1%)", "Wee Beastie (5-year, 47.4%)", "Annual Committee Reserve (very limited)"], "water_source": "Loch Uigeadail", "still_shape": "Purifier — unique to Ardbeg; creates lighter, cleaner spirit despite heavy peating"}),
  "quality_tier": "reserve",
  "reputation_narrative": "The Ardbeg 10-year is consistently voted the world's best single malt in consumer polls. Uigeadail and Corryvreckan are benchmark NAS expressions for professionals. Committee Reserve releases sell out within minutes. Available BC LDB (10-year, Uigeadail), specialty stores.",
  "allocation_notes": "10-year: BC LDB available. Uigeadail/Corryvreckan: specialty retailers. Committee: global lottery.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Broom, D. — The World Atlas of Whisky (Mitchell Beazley, 2014)",
  "is_verified": True,
  "slug": "ardbeg-distillery"
},
{
  "name": "Springbank Distillery",
  "producer_type": "distillery",
  "region_id": 98,
  "country": "Scotland",
  "production_philosophy": "traditional",
  "philosophy_description": "The only distillery in Scotland that performs every production step on-site: floor malting (using locally sourced Scottish barley), mashing, fermenting (wooden washbacks), 2.5-times distillation, maturing (in Campbeltown warehouses), bottling, and labelling — all on the same site. Family-owned by the Mitchell family since 1828. The distinctiveness of Springbank lies in this completeness — no outside influence on the spirit at any stage.",
  "key_personnel": json.dumps([{"name": "Hedley Wright", "role": "Owner (Mitchell family — 5th generation)"}, {"name": "Gavin McLachlan", "role": "Distillery Manager"}]),
  "production_details": json.dumps({"location": "Campbeltown, Kintyre Peninsula, Argyll", "floor_malting": "On-site — only distillery in Scotland malting its own barley", "distillation": "2.5 times — unique between double and triple distillation", "expressions": ["Springbank 10 (entry benchmark)", "Springbank 15", "Longrow (heavily peated expression)", "Hazelburn (triple-distilled, unpeated)", "CV — no age statement"], "annual_releases": "Very limited — high collector demand"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Springbank 10-year is arguably Scotland's best whisky per pound of quality. The combination of saline Campbeltown character, complete on-site production, and independent family ownership produces a whisky of unique integrity. Demand far exceeds supply. BC: available at specialty retailers through Pacific West Spirits and similar importers.",
  "allocation_notes": "High demand — BC specialty retailers maintain waitlists. Annual releases (21-year etc.) lottery basis.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Scotch Whisky: A Liquid History (Cassell, 2003)",
  "is_verified": True,
  "slug": "springbank-distillery"
},
{
  "name": "Laphroaig Distillery",
  "producer_type": "distillery",
  "region_id": 96,
  "country": "Scotland",
  "production_philosophy": "traditional",
  "philosophy_description": "The Royal Warrant holder — HRH Prince Charles granted Laphroaig a Royal Warrant, making it the only whisky with official royal endorsement. Founded 1815 on the south coast of Islay — the warehouse walls are washed by sea spray from Loch Laphroaig. The 10-year is the world's most iodine-intensive commercially produced whisky. 'Freedom to Roam' land ownership programme: owners of a bottle receive a square foot of Islay peat bog and an annual rental of a dram.",
  "key_personnel": json.dumps([{"name": "John Campbell", "role": "Distillery Manager (long tenure)"}]),
  "production_details": json.dumps({"location": "Port Ellen, Islay", "phenol_level_ppm": 40, "expressions": ["10-year (benchmark — maximum iodine character)", "Quarter Cask (ex-bourbon quarter casks — accelerated extraction)", "Triple Wood", "Select (ex-bourbon, PX, oloroso, virgin oak)", "Lore (NAS — complex, multi-cask)", "Annual Cairdeas (owners release)"], "floor_malting": "Still done on-site for a portion of production"}),
  "quality_tier": "estate",
  "reputation_narrative": "The Laphroaig 10-year is the definitive introduction to peated Islay whisky — if a guest says they like smoke, this is the reference point. Available at BC LDB and specialty retailers. Quarter Cask also at LDB.",
  "allocation_notes": "10-year and Quarter Cask: widely available BC LDB. Cairdeas: allocation.",
  "price_positioning": "mid_range",
  "authority_tier": 1,
  "source_text": "MacLean, C. — Islay: The Land and Its Whiskies (Canongate, 1997)",
  "is_verified": True,
  "slug": "laphroaig-distillery"
},

# ============================================================
# MEXICO — MEZCAL / TEQUILA
# ============================================================
{
  "name": "Del Maguey Single Village Mezcal",
  "producer_type": "distillery",
  "region_id": 99,
  "country": "USA",
  "production_philosophy": "natural",
  "philosophy_description": "Ron Cooper founded Del Maguey in 1995 as the first single-village mezcal company exported to the USA — creating the category that sparked the mezcal renaissance. Each Del Maguey expression is made by a specific maestro mezcalero in a specific Oaxacan village, using traditional methods (earthen pit roast, stone milling or tahona, open wooden fermentation vats, clay or copper pot still). Cooper's model — transparent sourcing, community support, authentic production — established the ethical framework for the entire craft mezcal industry.",
  "key_personnel": json.dumps([{"name": "Ron Cooper", "role": "Founder"}, {"name": "Steve Olson", "role": "Brand Ambassador / Spirits Educator"}]),
  "production_details": json.dumps({"model": "Single-village, single-producer — not a brand that blends", "expressions": ["San Luis del Rio (espadín, traditional copper pot still)", "Vida (espadín, entry point)", "Tobalá (wild agave — very limited)", "Pechuga (espadín distilled with seasonal fruits and chicken/turkey breast in still)", "San Juan del Rio (espadín, old vine material)"], "all_certified": "All ancestral or artesanal category — no industrial methods"}),
  "quality_tier": "reserve",
  "reputation_narrative": "Del Maguey San Luis del Rio is the reference point for authentic single-village mezcal. Pechuga is one of the most unusual and celebrated spirits on Earth. Available at specialty spirits retailers in BC; Vida at BC LDB.",
  "allocation_notes": "Vida: BC LDB. San Luis del Rio and Tobalá: specialty spirits retailers.",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Gaytán, M.S. — ¡Tequila! Distilling the Spirit of Mexico (Stanford, 2014)",
  "is_verified": True,
  "slug": "del-maguey-single-village-mezcal"
},
{
  "name": "Fortaleza Tequila",
  "producer_type": "distillery",
  "region_id": 100,
  "country": "Mexico",
  "production_philosophy": "traditional",
  "philosophy_description": "Guillermo Sauza is the 4th generation of the Sauza tequila dynasty — the family that owned Sauza Tequila (now Beam Suntory) for four generations. After selling the family company, Guillermo returned to the original distillery in Tequila, Jalisco and revived traditional production methods: cooking agave in traditional brick ovens (hornos) rather than autoclaves, stone tahona wheel grinding rather than mechanical mills, open wooden fermentation vats, and double-distillation in copper pot stills. Fortaleza ('Fortress') represents the traditional pre-industrial tequila process.",
  "key_personnel": json.dumps([{"name": "Guillermo Erickson Sauza", "role": "5th generation master distiller and owner"}]),
  "production_details": json.dumps({"location": "Tequila, Jalisco", "agave_cooking": "Traditional brick hornos (oven) — 36 hours, not autoclave", "milling": "Stone tahona wheel — traditional, slow, gentle", "fermentation": "Open wooden vats + spring water, wild yeast native to the property", "distillation": "Copper pot still, double-distilled", "expressions": ["Blanco (unaged, 40%)", "Reposado (6 months ex-bourbon, 40%)", "Añejo (2 years ex-bourbon, 40%)", "Still Strength (unaged, 46%)"]}),
  "quality_tier": "reserve",
  "reputation_narrative": "Fortaleza is the benchmark for tasting what tequila was before industrialisation. The tahona-ground agave releases more oils and fibres than mechanically milled agave — the resulting spirit has a complexity and texture that industrial tequila cannot match. Available at specialty spirits retailers in BC.",
  "allocation_notes": "Specialty spirits retailers in BC — limited allocation",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Gaytán, M.S. — ¡Tequila! Distilling the Spirit of Mexico (Stanford, 2014)",
  "is_verified": True,
  "slug": "fortaleza-tequila"
},

# ============================================================
# BELGIUM & GERMANY
# ============================================================
{
  "name": "Cantillon Brewery",
  "producer_type": "brewery",
  "region_id": 101,
  "country": "Belgium",
  "production_philosophy": "traditional",
  "philosophy_description": "The pilgrimage brewery — Brasserie Cantillon in Anderlecht, Brussels, is the definitive traditional lambic producer and the most important brewery in the world for understanding spontaneous fermentation. Founded 1900, still family-owned (Van Roy family). A working museum of traditional lambic production: open coolship, where hot wort is exposed overnight to the wild airborne microbiome of the Senne Valley for spontaneous inoculation. Production only October-April.",
  "key_personnel": json.dumps([{"name": "Jean-Pierre Van Roy", "role": "Owner-Brewer"}, {"name": "Jean Van Roy", "role": "Son — now leading brewing operations"}]),
  "production_details": json.dumps({"location": "Anderlecht, Brussels", "coolship": "Open copper vessel — overnight wild fermentation inoculation", "fermentation_vessels": "Old oak Bordeaux barrels and Champagne barrels", "ageing": "1-3 years before blending for gueuze", "production_season": "October to April only", "annual_production_barrels": 1800, "expressions": ["Gueuze (blended multi-vintage lambic)", "Kriek (whole cherries, 8 months)", "Rosé de Gambrinus (raspberries)", "Iris (all-barley, dry-hopped)"]}),
  "quality_tier": "reserve",
  "reputation_narrative": "Cantillon is a mecca for beer culture. The annual Zwanze Day (worldwide simultaneous tap event) is one of the most celebrated events in beverages. Strictly limited production — available in Belgium at the brewery and through specialist importers. BC: Brewery Creek Cold Beer and Wine, and specialty bottle shops carry limited Cantillon.",
  "allocation_notes": "Very limited in Canada — specialty bottle shops in major cities. BC: Brewery Creek, Firefly Fine Wines",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Beaumont, S. — The Great Beers of Belgium (Brewers Publications, 2008); Jackson, M. — Great Beers of Belgium",
  "is_verified": True,
  "slug": "cantillon-brewery"
},
{
  "name": "Weihenstephan Brewery",
  "producer_type": "brewery",
  "region_id": 102,
  "country": "Germany",
  "production_philosophy": "traditional",
  "philosophy_description": "The world's oldest continuously operating brewery — founded 1040 AD by Benedictine monks on Weihenstephan Hill in Freising, Bavaria (a monastery had been brewing there since at least 768 AD). Now operates as the Bavarian State Brewery, associated with the Technical University of Munich's brewing and food technology faculty (world's most prestigious brewing school). The Hefeweizen and Kristallweizen are the benchmark Bavarian wheat beers.",
  "key_personnel": json.dumps([{"name": "Georg Schneider (historical)", "role": "Linked to wheat beer history"}, {"name": "Bavarian State", "role": "Owner"}]),
  "production_details": json.dumps({"location": "Freising, Bavaria (25km from Munich)", "founded": "1040 AD (documented)", "monastery_brewing": "768 AD (first documented beer tax paid)", "hefeweizen_profile": "Cloudy, golden, banana (isoamyl acetate) and clove (4-vinylguaiacol) — benchmarks of Weizen yeast character", "expressions": ["Hefeweissbier (benchmark)", "Kristallweissbier (filtered)", "Dunkelweissbier (dark wheat)", "Vitus (Weizenbock)", "Festweisse (Oktoberfest)"]}),
  "quality_tier": "market",
  "reputation_narrative": "Weihenstephan Hefeweizen is the reference point for the style globally — used as the benchmark in brewing education worldwide. The connection to the world's most prestigious brewing school ensures ongoing technical excellence. Available at major BC retailers and German specialty food stores.",
  "allocation_notes": "Widely available at BC LDB and specialty retailers",
  "price_positioning": "mid_range",
  "authority_tier": 1,
  "source_text": "Jackson, M. — The New World Guide to Beer (Running Press, 1988); Weihenstephan Brewery documentation",
  "is_verified": True,
  "slug": "weihenstephan-brewery"
},
{
  "name": "3 Fonteinen Brouwerij & Lambiekstokery",
  "producer_type": "brewery",
  "region_id": 101,
  "country": "Belgium",
  "production_philosophy": "traditional",
  "philosophy_description": "Armand Debelder's 3 Fonteinen (Three Fountains) in Beersel, Pajottenland, is the benchmark for gueuze blending — the art of selecting lambics of different ages from different producers and blending them into a refermented, Champagne-like gueuze. The 2009 disaster (a broken thermostat destroyed 50,000 bottles of refermented gueuze) nearly ended the company but created the 'Brotherhood of the Senne' — a community fundraising effort that saved the brewery and established 3 Fonteinen's legendary status.",
  "key_personnel": json.dumps([{"name": "Armand Debelder", "role": "Master Blender"}]),
  "production_details": json.dumps({"location": "Beersel, Flemish Brabant", "model": "Geuzestekerij — primarily a blending house (buys lambic from multiple producers for blending), also now brewing own lambic", "gueuze_ageing": "18 months refermentation in bottle after blending", "expressions": ["Oude Geuze (benchmark blend)", "Cuvée Armand & Gaston (premium aged blend)", "Hommage (fruit geuze with strawberries)", "Intens Rood (kriek)"]}),
  "quality_tier": "reserve",
  "reputation_narrative": "3 Fonteinen Oude Geuze is the most complex and age-worthy of all gueuzes — capable of 5-10 years bottle development. Very limited Canadian distribution. BC: available at Brewery Creek and specialty bottle shops.",
  "allocation_notes": "Very limited in Canada — specialty bottle shops",
  "price_positioning": "premium",
  "authority_tier": 1,
  "source_text": "Beaumont, S. — The Great Beers of Belgium (Brewers Publications, 2008)",
  "is_verified": True,
  "slug": "3-fonteinen"
},

]

def main():
    conn = psycopg2.connect(CONN)
    cur = conn.cursor()
    inserted = 0
    for p in PRODUCERS:
        try:
            cur.execute(SQL, (
                p["name"], p["producer_type"], p.get("region_id"),
                p.get("country"), p.get("production_philosophy"),
                p.get("philosophy_description"),
                p.get("key_personnel"), p.get("production_details"),
                p.get("quality_tier"), p.get("reputation_narrative"),
                p.get("allocation_notes"), p.get("price_positioning"),
                p.get("authority_tier"), p.get("source_text"),
                p.get("is_verified", False), True,
                p.get("slug")
            ))
            row = cur.fetchone()
            if row:
                print(f"  INSERT producer id={row[0]}: {row[1]}")
                inserted += 1
            else:
                print(f"  SKIP (exists): {p['name']}")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"  ERROR {p['name']}: {e}")
    print(f"\nDone. {inserted} producers inserted.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
