#!/usr/bin/env python3
"""Terminal 10 — Batch 1: Kremstal, Dão DOC, Tennessee, Chianti Classico, Priorat"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs
KREMSTAL   = 228
DAO        = 234
TENNESSEE  = 83
CHIANTI    = 166
PRIORAT    = 177
RIOJA      = 178  # check if this is right
PIEDMONT   = 161
BAROLO_REG = 162  # will need to confirm

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          reputation_narrative, price_positioning, authority_tier))
    row = cur.fetchone()
    print(f"  ✓ {name} (id={row[0]})")
    return row[0]

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"    ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, producer_id, region_id, origin_country,
           subcategory, description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, producer_id, region_id, origin_country,
          subcategory, description, price_tier))
    row = cur.fetchone()
    print(f"    ✓ {name} (id={row[0]})")
    return row[0]

# ═══════════════════════════════════════════════════════════════════════════
# KREMSTAL — AUSTRIA (0 PRODUCTS → FIX)
# ═══════════════════════════════════════════════════════════════════════════
print("=== KREMSTAL — AUSTRIA (0 → products) ===")

nigl = P("Weingut Nigl", "winery", KREMSTAL, "Austria",
    production_philosophy="Kremstal's benchmark for Grüner Veltliner and Riesling precision",
    philosophy_description="Weingut Nigl has been the defining producer of Kremstal's finest terroir since Martin Nigl took over in 1993. The estate produces single-vineyard Grüner Veltliner and Riesling from ancient volcanic gneis and primary rock terraces above the Krems river valley. The Privat expressions — from the estate's deepest single parcels — are among Austria's most sought-after wines.",
    key_personnel=[{"name": "Martin Nigl", "role": "Owner/Winemaker"}],
    production_details={"soils": "volcanic gneis and primary rock", "elevation": "up to 400m", "regions": "Kremstal DAC"},
    reputation_narrative="Weingut Nigl is consistently Falstaff and Wine Advocate's top-rated Kremstal producer — the Privat Grüner Veltliner and Privat Riesling achieve 93-97 points internationally. Martin Nigl's work has defined Kremstal's identity as a great terroir region distinct from the more famous Wachau.",
    price_positioning="premium")

PROD("Nigl Privat Grüner Veltliner", "wine_still", nigl, KREMSTAL, "Austria",
    subcategory="gruner_veltliner_kremstal",
    description="Weingut Nigl's flagship single-parcel Grüner Veltliner from volcanic gneis terraces in the Kremstal — one of Austria's most expressive Grüner Veltliner beyond the Wachau. Hand-picked from old vines on steep slopes; aged in large Austrian oak casks. White pepper, wild herbs, lemon zest, and the characteristic Grüner Veltliner 'pfeffer' spice — with the weight and complexity of primary rock mineral. Exceptional food versatility: serves where white Burgundy would and challenges it at half the price. 93-96 points from Falstaff.",
    price_tier="premium")

PROD("Nigl Kremstal Grüner Veltliner", "wine_still", nigl, KREMSTAL, "Austria",
    subcategory="gruner_veltliner_kremstal",
    description="Nigl's entry expression of Kremstal Grüner Veltliner — from estate vineyards across the appellation. The quintessential food wine: white pepper, green apple, citrus, and stony minerals with pristine acidity. Fermented in stainless steel; no oak. At 12-13% alcohol, the most versatile food pairing wine in the Austrian portfolio. Exemplifies why Grüner Veltliner is the sommelier's choice for difficult food pairings.",
    price_tier="mid_range")

mayer_kremstal = P("Weingut Salomon-Undhof", "winery", KREMSTAL, "Austria",
    production_philosophy="Kremstal's oldest estate — Roman cellar, Riesling from primary rock terraces",
    philosophy_description="Salomon-Undhof traces its history to Roman viticulture along the Krems river — the estate's cellar dates to the 2nd century. The Steiner Hund Riesling, from primary rock terraces overlooking the Danube, is one of Austria's most historically significant wine sites. Bertold Salomon's biodynamic conversion has heightened the terroir expression of these ancient sites.",
    key_personnel=[{"name": "Bertold Salomon", "role": "Owner/Winemaker"}],
    production_details={"history": "Roman origins, 2nd century cellar", "flagship": "Steiner Hund Riesling", "viticulture": "biodynamic"},
    reputation_narrative="Salomon-Undhof is one of Austria's most historically significant wine estates — the Roman-era cellar and ancient Steiner Hund site represent Kremstal's deep viticultural heritage. The Steiner Hund Riesling is considered among Austria's finest Rieslings outside the Mosel-parallel Wachau.",
    price_positioning="premium")

PROD("Salomon Steiner Hund Riesling", "wine_still", mayer_kremstal, KREMSTAL, "Austria",
    subcategory="riesling_kremstal",
    description="Kremstal's most historically significant wine — from primary rock terraces at Stein (across the Danube from the Wachau border) that have been cultivated since Roman times. The Steiner Hund site produces biodynamic Riesling of extraordinary minerality: citrus blossom, white stone fruit, and a salty, smoking mineral quality from the ancient rock. Ages beautifully for a decade. Austria's counter-argument to Wachau Riesling: equally complex at more accessible prices.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# DÃO DOC — PORTUGAL (0 PRODUCTS → FIX)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== DÃO DOC — PORTUGAL (0 → products) ===")

quinta_da_pellada = P("Quinta da Pellada", "winery", DAO, "Portugal",
    production_philosophy="Dão's benchmark — old-vine granite Touriga Nacional from ancient pre-phylloxera sites",
    philosophy_description="Alvaro Castro's Quinta da Pellada estate is the defining expression of Dão DOC's potential — old-vine Touriga Nacional on granite and schist at 700-900m altitude. The estate farms without irrigation using traditional inter-planting of multiple indigenous varieties. The Primus and Carrocel bottlings demonstrate that Dão can produce Portugal's most elegant and age-worthy reds alongside Douro.",
    key_personnel=[{"name": "Álvaro Castro", "role": "Owner/Winemaker"}],
    production_details={"altitude": "700-900m granite and schist", "varieties": "Touriga Nacional dominant, field blend", "style": "minimal intervention, old vine"},
    reputation_narrative="Quinta da Pellada is considered Dão DOC's finest estate — the high-altitude granite terroir and ancient vines produce Touriga Nacional of extraordinary elegance. Alvaro Castro's wines have demonstrated that Dão can rival Douro for complexity while surpassing it for finesse and food-friendliness. Internationally allocated.",
    price_positioning="ultra_premium")

PROD("Quinta da Pellada Primus Dão Red", "wine_still", quinta_da_pellada, DAO, "Portugal",
    subcategory="touriga_nacional_dao",
    description="The pinnacle of Dão DOC — old-vine Touriga Nacional and field-blend varieties from granite and schist terraces at 800m altitude in Dão's Serra da Estrela foothills. Minimal intervention; aged in old Portuguese oak and large French tonneaux. Dark cherry, violet, dried herbs, granite minerality, and the silky, fine-grained tannin structure that distinguishes Dão from Douro. Portugal's most elegant red wine region. Ages beautifully for 15-20 years. Consistently 93-97 points from international critics.",
    price_tier="ultra_premium")

PROD("Quinta da Pellada Dão Red", "wine_still", quinta_da_pellada, DAO, "Portugal",
    subcategory="touriga_nacional_dao",
    description="Alvaro Castro's estate-level Dão DOC red from old-vine granite sites — a field blend of Touriga Nacional, Tinta Roriz, Alfrocheiro, and Jaen. Aged in large format Portuguese and French oak. Red cherry, violet, dried herbs, and the characteristic granite minerality of the Dão highlands. Lighter and more elegant than Douro — the ideal fine dining red for complex preparations requiring acidity and structure rather than power.",
    price_tier="premium")

niepoort_dao = P("Niepoort Vinhos (Dão)", "winery", DAO, "Portugal",
    production_philosophy="Dão old-vine field blends — Dirk Niepoort's exploration of Portugal's most underrated red region",
    philosophy_description="Dirk Niepoort — the Douro legend — turned his attention to Dão DOC seeking Portugal's most age-worthy reds from high-altitude granite. The Nat'Cool Dão and Dialogo Dão demonstrate that indigenous varieties farmed at altitude on granite produce wines of extraordinary freshness, elegance, and longevity — different in every way from the power of Douro.",
    key_personnel=[{"name": "Dirk Niepoort", "role": "Owner/Winemaker"}],
    production_details={"region_focus": "high altitude Dão granite", "style": "fresh, natural, age-worthy"},
    reputation_narrative="Dirk Niepoort's Dão project has accelerated the region's international recognition — his advocacy for Dão's unique terroir and indigenous varieties has brought global attention to a region long overshadowed by Douro. The Dialogo Dão is consistently considered Portugal's greatest value in fine red wine.",
    price_positioning="premium")

PROD("Niepoort Dialogo Dão Red", "wine_still", niepoort_dao, DAO, "Portugal",
    subcategory="touriga_nacional_dao",
    description="Dirk Niepoort's entry into Dão DOC — an old-vine field blend of indigenous varieties (Touriga Nacional, Alfrocheiro, Tinta Roriz) from high-altitude granite schist. Wild fermentation; aged in large old Portuguese balseiro. Vivid red cherry, violet, dried herbs, granite minerality, and extraordinary freshness from altitude acidity. Portugal's most compelling value in structured red wine. The case study for Dão's potential alongside Douro at a fraction of the price.",
    price_tier="mid_range")

# ═══════════════════════════════════════════════════════════════════════════
# TENNESSEE WHISKEY — DEPTH
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== TENNESSEE WHISKEY REGION — USA ===")

jack_daniels_dist = P("Jack Daniel Distillery", "distillery", TENNESSEE, "USA",
    production_philosophy="Lincoln County Process charcoal filtering — the Tennessee whiskey distinction",
    philosophy_description="Jack Daniel's is the world's most recognised whiskey brand — and the world's most produced premium distilled spirit. Established in 1866 in Lynchburg, Tennessee, the distillery is famous for the Lincoln County Process: filtering the new-make spirit through 10 feet of sugar maple charcoal before barreling. This process adds smoothness and removes harsh congeners, creating the distinctive Tennessee whiskey style separate from bourbon. Single Barrel Select is the pinnacle of the portfolio.",
    key_personnel=[{"name": "Chris Fletcher", "role": "Master Distiller"}],
    production_details={"process": "Lincoln County Process charcoal mellowing", "established": "1866", "location": "Lynchburg, Moore County, TN"},
    reputation_narrative="Jack Daniel's Old No. 7 is the world's best-selling whiskey. The Single Barrel Select program — launched in 1997 — elevated the brand from accessible everyday whiskey to a collector's category: each barrel individually tested and hand-selected, bottled at 94-100 proof. Single Barrel represents the pinnacle of what the Lincoln County Process creates.",
    price_positioning="premium")

PROD("Jack Daniel's Single Barrel Select Tennessee Whiskey", "spirits_whiskey", jack_daniels_dist, TENNESSEE, "USA",
    subcategory="Tennessee Straight Whiskey — Single Barrel Select",
    description="Jack Daniel's flagship collector expression — each barrel individually selected by the Distillery's master tasters and bottled at natural barrel proof (94-100 proof). The Lincoln County Process charcoal mellowing followed by single-barrel maturation in the top floors of the iron-free Lynchburg rickhouses creates extraordinary vanilla, caramel, toasted oak, and maple sweetness with the characteristic JD smoothness and a long, warming finish. World's most recognised single-barrel whiskey program.",
    price_tier="premium")

PROD("Jack Daniel's Old No. 7 Tennessee Whiskey", "spirits_whiskey", jack_daniels_dist, TENNESSEE, "USA",
    subcategory="Tennessee Straight Whiskey — Black Label",
    description="The world's best-selling whiskey — the benchmark expression of Tennessee whiskey and the Lincoln County Process. Made from an 80% corn, 8% rye, 12% malt mash bill; charcoal mellowed through 10 feet of sugar maple charcoal; matured in new American oak. Characteristic vanilla, banana, caramel, and toasted oak with the smoky-sweet smoothness unique to the Tennessee whiskey style. 80 proof. The reference for recognising Tennessee vs Kentucky bourbon styles.",
    price_tier="mid_range")

george_dickel = P("George Dickel Distillery", "distillery", TENNESSEE, "USA",
    production_philosophy="Tennessee's second tradition — chill-filtered charcoal mellowing and old-fashioned craftsmanship",
    philosophy_description="George Dickel is Tennessee's oldest surviving distillery after Prohibition, established at Cascade Hollow in Tullahoma. The distillery uses the Lincoln County Process — charcoal mellowing in chill-filtered 40°F spirit — which they claim produces a smoother whisky (they spell it without the 'e'). The No. 12 Superior Grade is the flagship expression and Tennessee's most awarded whisky outside Jack Daniel's.",
    key_personnel=[{"name": "Allisa Henley", "role": "Head Distiller"}],
    production_details={"established": "1870", "location": "Tullahoma, Tennessee", "distinction": "chill-filtered Lincoln County Process"},
    reputation_narrative="George Dickel No. 12 is the critical darling of Tennessee whisky — consistent 90+ scores from all major rating publications, and consistently cited by whisky experts as the superior quality alternative to the Jack Daniel's Black Label. A necessary inclusion in any serious spirits program.",
    price_positioning="mid_range")

PROD("George Dickel No. 12 Superior Grade Tennessee Whisky", "spirits_whiskey", george_dickel, TENNESSEE, "USA",
    subcategory="Tennessee Straight Whisky — Charcoal Mellowed",
    description="Tennessee's most critically acclaimed whisky outside the Jack Daniel's portfolio — the No. 12 is George Dickel's flagship expression, chill-filtered through sugar maple charcoal before barreling (the Dickel distinction). 90 proof; corn-forward mash bill; medium-aged. Vanilla cream, caramel, cinnamon spice, and a characteristic 'chilly filtered' smoothness. Consistently 91-93 points from Whisky Advocate and a best-buy designation across publications. The benchmark for comparing Tennessee's two great whisky traditions.",
    price_tier="mid_range")

# ═══════════════════════════════════════════════════════════════════════════
# CHIANTI CLASSICO DOCG — DEPTH (current 1 product is mis-categorized)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== CHIANTI CLASSICO DOCG — ITALY ===")

antinori = P("Marchesi Antinori", "winery", CHIANTI, "Italy",
    production_philosophy="26 generations of Florentine wine — Tignanello and the Super Tuscan revolution",
    philosophy_description="The Antinori family has been making wine in Tuscany since 1385 — 26 generations. The estate's Villa Antinori Chianti Classico is the benchmark for classically structured Sangiovese, while Tignanello (their Super Tuscan, first made in 1971) permanently altered the Italian wine landscape by demonstrating that Sangiovese blended with Cabernet Sauvignon could challenge Bordeaux's finest. The estate's Pèppoli is the approachable expression; Badia a Passignano is the Riserva pinnacle.",
    key_personnel=[{"name": "Albiera Antinori", "role": "President"}, {"name": "Marchese Piero Antinori", "role": "Founding Director"}],
    production_details={"established": "1385", "estates": "Tignanello, Badia a Passignano, Pèppoli", "heritage": "26 generations Florentine family"},
    reputation_narrative="Antinori is one of the world's most historically significant wine dynasties — the Florentine family that created the Super Tuscan category with Tignanello in 1971 and Solaia in 1978. Their Chianti Classico program demonstrates the full range from accessible Pèppoli to the Gran Selezione pinnacle at Badia a Passignano.",
    price_positioning="premium")

PROD("Antinori Tignanello", "wine_still", antinori, CHIANTI, "Italy",
    subcategory="super_tuscan_sangiovese_cabernet",
    description="The wine that created the Super Tuscan category — Tignanello (named for the estate vineyard on the Antinori's Santa Cristina estate) was the first modern Sangiovese blended with Cabernet Sauvignon (80/15/5 with Cabernet Franc), aged in small French barriques. First made in 1971, it broke all Italian wine law conventions and created a new category. Dark cherry, graphite, leather, tobacco, and violet with the elegant structure of Florentine Sangiovese reinforced by Cabernet. One of Italy's most consistently rated wines — 93-97 points annually.",
    price_tier="premium")

PROD("Antinori Badia a Passignano Chianti Classico Gran Selezione", "wine_still", antinori, CHIANTI, "Italy",
    subcategory="chianti_classico_gran_selezione",
    description="Antinori's pinnacle Chianti Classico — single-estate 100% Sangiovese from the historic Badia a Passignano monastery estate (in Antinori ownership since 1987). Gran Selezione: minimum 30 months aging, single-vineyard or best-barrel selection. Aged in French barriques and Slavonian oak. Wild cherry, leather, dried rose, tobacco, and the distinctive iron-mineral of Sangiovese at full maturity. The counterargument to Super Tuscan: pure Sangiovese at its Chianti Classico finest.",
    price_tier="ultra_premium")

fontodi = P("Fontodi", "winery", CHIANTI, "Italy",
    production_philosophy="Panzano 'conca d'oro' Sangiovese — Chianti Classico's most distinctive terroir",
    philosophy_description="Giovanni Manetti's Fontodi estate sits in the 'Golden Shell' of Panzano in Chianti — a south-facing amphitheatre of galestro schist and alberese clay that produces Sangiovese of extraordinary concentration and elegance. The Flaccianello della Pieve (100% Sangiovese, first made 1981) is considered Italy's greatest pure Sangiovese expression. Organic and biodynamic farming since 2000.",
    key_personnel=[{"name": "Giovanni Manetti", "role": "Owner/Director"}],
    production_details={"terroir": "Panzano conca d'oro galestro", "farming": "certified organic/biodynamic", "flagship": "Flaccianello della Pieve IGT"},
    reputation_narrative="Fontodi's Flaccianello della Pieve is considered by many critics to be Italy's finest pure Sangiovese expression — consistently rated 96-100 by Wine Advocate, Wine Spectator, and Gambero Rosso. The Panzano 'conca d'oro' terroir creates Sangiovese of extraordinary concentration and elegance that defines the benchmark for the grape variety.",
    price_positioning="ultra_premium")

PROD("Fontodi Chianti Classico Gran Selezione Vigna del Sorbo", "wine_still", fontodi, CHIANTI, "Italy",
    subcategory="chianti_classico_gran_selezione",
    description="Fontodi's single-vineyard Gran Selezione from the Vigna del Sorbo — 100% Sangiovese from biodynamic galestro schist soils in the Panzano conca d'oro. Extended maceration; aged 22 months in barriques (33% new French). Dark cherry, rose petal, leather, tobacco, iron mineral, and the extraordinary sour cherry freshness of Panzano Sangiovese. More accessible than Flaccianello but the same terroir expression with recognisable DOCG structure. 93-97 points consistently.",
    price_tier="ultra_premium")

PROD("Fontodi Chianti Classico", "wine_still", fontodi, CHIANTI, "Italy",
    subcategory="chianti_classico",
    description="Fontodi's estate Chianti Classico DOCG — 100% Sangiovese from biodynamic galestro soils in Panzano. Aged 14 months in large Slavonian oak. The benchmark expression of Chianti Classico: vivid sour cherry, dried rose, leather, iron mineral, and the characteristic high acidity that makes Chianti the world's most food-friendly red. At this level, demonstrates why Sangiovese from the right galestro terroir represents extraordinary value in fine Italian red wine.",
    price_tier="premium")

# ═══════════════════════════════════════════════════════════════════════════
# PRIORAT DOCa — SPAIN (ADD TO EXISTING 1 PRODUCT)
# ═══════════════════════════════════════════════════════════════════════════
print("\n=== PRIORAT DOCa — SPAIN ===")

clos_mogador = P("Clos Mogador", "winery", PRIORAT, "Spain",
    production_philosophy="Priorat's founding estate — René Barbier's llicorella schist revolution",
    philosophy_description="René Barbier established Clos Mogador in 1989 as one of the five original Priorat producers who revolutionised this historic Catalan region. The llicorella schist soils (flaky slate with quartz) and the extreme Mediterranean-continental climate create Grenache and Carinyena (Carignan) of extraordinary concentration and mineral intensity. Clos Mogador is considered Priorat's original reference — before Alvaro Palacios arrived.",
    key_personnel=[{"name": "René Barbier", "role": "Founder/Winemaker"}, {"name": "Sara Pérez", "role": "Winemaker"}],
    production_details={"established": "1989", "terroir": "llicorella schist", "varieties": "Grenache, Carinyena, Cabernet, Syrah"},
    reputation_narrative="Clos Mogador is Priorat's original reference estate — René Barbier and the 'Quintet' founders created the modern Priorat appellation in 1989 when the region was abandoned. The Clos Mogador wine demonstrates Priorat's distinctive combination of concentrated Grenache power with llicorella mineral precision. Consistently 94-98 points internationally.",
    price_positioning="ultra_premium")

PROD("Clos Mogador Priorat", "wine_still", clos_mogador, PRIORAT, "Spain",
    subcategory="grenache_carinyena_priorat",
    description="Priorat's founding estate wine — Grenache, Carinyena (Carignan), Cabernet Sauvignon, and Syrah from llicorella schist soils. Aged 12-14 months in French and American oak barriques. Dark cherry, black plum, dried herbs, black olive, mineral schist, and warming spice from the extreme Priorat climate. The original expression of what llicorella schist produces when farmed with old-vine Grenache and Carinyena. Consistently one of Spain's greatest wines: 94-98 points from Robert Parker and Wine Advocate.",
    price_tier="ultra_premium")

cur.close()
conn.close()
print("\n✅ Terminal 10 Batch 1 — Kremstal, Dão, Tennessee, Chianti, Priorat complete.")
