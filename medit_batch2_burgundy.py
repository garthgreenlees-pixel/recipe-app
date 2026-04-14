#!/usr/bin/env python3
"""Mediterranean Session — Batch 2: Burgundy
Producers, Products, beverage_references, pairing_intelligence.
Region IDs: Burgundy=104, Côte de Nuits=105, Gevrey-Chambertin=106, Morey-Saint-Denis=107,
Chambolle-Musigny=108, Vougeot=109, Vosne-Romanée=110, Nuits-Saint-Georges=111,
Côte de Beaune=112, Aloxe-Corton=113, Beaune=114, Pommard=115, Volnay=116,
Meursault=117, Puligny-Montrachet=118, Chassagne-Montrachet=119, Chablis=120.
"""
import psycopg2, json, re

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    return s.strip('-')

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def P(name, producer_type, region_id, country="France",
      production_philosophy=None, philosophy_description=None,
      key_personnel=None, production_details=None,
      quality_tier=None, reputation_narrative=None,
      allocation_notes=None, price_positioning=None, authority_tier=1):
    slug = slugify(name)
    # Check existence first
    cur.execute("SELECT id FROM beverage_producers WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ PRODUCER: {name} exists (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_producers
          (name, slug, producer_type, region_id, country, production_philosophy,
           philosophy_description, key_personnel, production_details, quality_tier,
           reputation_narrative, allocation_notes, price_positioning, authority_tier,
           is_verified, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE,TRUE)
        RETURNING id
    """, (name, slug, producer_type, region_id, country,
          production_philosophy, philosophy_description,
          json.dumps(key_personnel) if key_personnel else None,
          json.dumps(production_details) if production_details else None,
          quality_tier, reputation_narrative, allocation_notes, price_positioning, authority_tier))
    row = cur.fetchone()
    if row:
        print(f"  ✓ PRODUCER: {name} (id={row[0]})")
        return row[0]
    return None

def PROD(name, category, producer_id, region_id, origin_country="France",
         subcategory=None, description=None, quality_tier=None,
         quality_hierarchy=None, deductive_profile=None, service_specs=None,
         flavour_markers=None, flavour_weight=None, flavour_profile_type=None,
         price_tier=None, price_range_cad=None, technical_specs=None):
    slug = slugify(name)
    # Check existence first
    cur.execute("SELECT id FROM beverage_products WHERE LOWER(name)=LOWER(%s)", (name,))
    row = cur.fetchone()
    if row:
        print(f"    ~ PRODUCT: {name} exists (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, slug, category, subcategory, producer_id, region_id, origin_country,
           description, quality_tier, quality_hierarchy, deductive_profile, service_specs,
           flavour_markers, flavour_weight, flavour_profile_type,
           price_tier, price_range_cad, technical_specs, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, slug, category, subcategory, producer_id, region_id, origin_country,
          description, quality_tier,
          json.dumps(quality_hierarchy) if quality_hierarchy else None,
          json.dumps(deductive_profile) if deductive_profile else None,
          json.dumps(service_specs) if service_specs else None,
          flavour_markers, flavour_weight, flavour_profile_type,
          price_tier, price_range_cad,
          json.dumps(technical_specs) if technical_specs else None))
    row = cur.fetchone()
    if row:
        print(f"    ✓ PRODUCT: {name} (id={row[0]})")
        return row[0]
    return None

def REF(name, category, description, key_principles,
        skill_level="advanced", service_context=None, source_text=None, authority_tier=1):
    cur.execute("""
        INSERT INTO beverage_references
          (name, category, description, key_principles,
           skill_level, service_context, source_text, authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, category, description, key_principles,
          skill_level, service_context, source_text, authority_tier))
    row = cur.fetchone()
    if row:
        print(f"  ✓ REF: {name} (id={row[0]})")
        return row[0]
    return None

def PROTOCOL(name, category, beverage_family, procedure, description=None,
             rationale=None, common_errors=None, service_context=None,
             equipment_required=None, guest_communication=None,
             skill_level="advanced", authority_tier=1, source_text=None):
    cur.execute("""
        INSERT INTO service_protocols
          (name, category, beverage_family, description, procedure, rationale,
           common_errors, service_context, equipment_required, guest_communication,
           skill_level, authority_tier, source_text, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        RETURNING id
    """, (name, category, beverage_family, description, procedure, rationale,
          common_errors, service_context, equipment_required, guest_communication,
          skill_level, authority_tier, source_text))
    row = cur.fetchone()
    if row:
        print(f"  ✓ PROTOCOL: {name} (id={row[0]})")
        return row[0]
    return None

def PAIR(food_description, food_category, beverage_category, meal_context,
         confidence, pairing_type, flavour_logic, product_id,
         food_flavour_profile=None):
    # meal_context valid: aperitif, amuse, starter, fish_course, main, cheese, pre_dessert, dessert, digestif, celebration, casual, any
    cur.execute("""
        INSERT INTO pairing_intelligence
          (food_description, food_category, food_flavour_profile, beverage_category,
           meal_context, confidence, pairing_type, flavour_logic, beverage_product_id,
           authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,1,TRUE) RETURNING id
    """, (food_description, food_category, food_flavour_profile, beverage_category,
          meal_context, confidence, pairing_type, flavour_logic, product_id))
    row = cur.fetchone()
    if row:
        return row[0]
    return None

# ════════════════════════════════════════════════════════════════════════════════
# BURGUNDY PRODUCERS
# ════════════════════════════════════════════════════════════════════════════════
print("=== BURGUNDY PRODUCERS ===")

drc = P("Domaine de la Romanée-Conti", "winery", 110, "France",
    production_philosophy="terroir_purist",
    philosophy_description="DRC produces from six Grand Cru monopoles and major holdings in the greatest vineyards of the Côte de Nuits. Biodynamic farming throughout. All wines are unfiltered. The winemaking is deliberately minimal — traditional Burgundian methods unchanged for generations. New oak is used judiciously — typically 100% new for the Grand Crus but the wine absorbs it without domination due to the extract and concentration of the fruit. The estate employs no guest winemakers and accepts no outside consultants. The wines are sold exclusively through a strict négociant allocation system; no direct-to-consumer sales.",
    key_personnel=[{"role": "co-director", "name": "Aubert de Villaine"},
                   {"role": "co-director", "name": "Bertrand de Villaine"}],
    production_details={"farming": "biodynamic", "vinification": "traditional", "oak": "100% new Grand Cru",
                        "bc_importer": "BCLDB Special Order / Allocation [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="DRC is the world's most revered wine producer. A single bottle of La Romanée-Conti routinely sells at auction for $30,000–$50,000 USD. The estate is a joint venture — 50% owned by the de Villaine family, 50% by the Leroy family (Lalou Bize-Leroy departed in 1992 following a dispute). The wines are essentially impossible to buy at retail.",
    allocation_notes="By allocation through a handful of global importers. In BC, BCLDB special ordering or private auction only. No regular retail availability.",
    price_positioning="ultra_premium", authority_tier=1)

leroy = P("Domaine Leroy", "winery", 104, "France",
    production_philosophy="biodynamic_pioneer",
    philosophy_description="Lalou Bize-Leroy, after her departure from DRC in 1992, purchased Domaine Charles Noëllat and transformed it into Domaine Leroy. Ultra-biodynamic farming — yields are sometimes below 10 hl/ha (normal is 40–60). No chemicals of any kind, ever. Extensive use of herbal preparations (compost teas, horn silica, horn manure). Hand-harvesting in multiple passes. The results are wines of extraordinary concentration and longevity. Prices have surpassed DRC at auction for some cuvées.",
    key_personnel=[{"role": "founder-proprietor", "name": "Lalou Bize-Leroy"}],
    production_details={"farming": "biodynamic Demeter certified", "yields": "5–15 hl/ha extreme",
                        "bc_importer": "Allocation only [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Lalou Bize-Leroy (born 1932) is Burgundy's most formidable character — intellectually ferocious, obsessively perfectionist. Her Chambertin has sold at auction for $12,000+ per bottle. The domaine now includes Musigny, Richebourg, Romanée-Saint-Vivant, Clos de Vougeot, and 20+ other Grand Cru and Premier Cru sites.",
    allocation_notes="Essentially unobtainable. Waitlists measured in decades. Auction only in most markets.",
    price_positioning="ultra_premium", authority_tier=1)

rousseau = P("Domaine Armand Rousseau", "winery", 106, "France",
    production_philosophy="traditional_excellence",
    philosophy_description="The reference Gevrey-Chambertin estate. Founded by Armand Rousseau in the 1930s; now run by grandson Eric Rousseau. Traditional winemaking with 20–30% new oak for Grand Crus. Whole-cluster fermentation a key tool — depends on vintage and ripeness. The estate owns parcels in Chambertin, Chambertin Clos de Bèze, Mazis-Chambertin, Clos Saint-Jacques (Premier Cru — considered Grand Cru quality), and Gevrey-Chambertin village.",
    key_personnel=[{"role": "winemaker", "name": "Eric Rousseau"}],
    production_details={"farming": "lutte raisonnée", "whole_cluster": "partial",
                        "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Rousseau Chambertin is considered alongside DRC and Leroy as one of Burgundy's trinity of Grand Cru pinnacles. The Clos Saint-Jacques is routinely described as the finest Premier Cru in the Côte d'Or. Allocation is tight; restaurant wine lists and private clients claim most of the production.",
    allocation_notes="Available through Lifford Wine Agency allocation. Restaurant-first allocation model.",
    price_positioning="ultra_premium", authority_tier=1)

roumier = P("Domaine Georges Roumier", "winery", 108, "France",
    production_philosophy="precision_terroir",
    philosophy_description="The reference Chambolle-Musigny estate. Founded by Georges Roumier; now run by Christophe Roumier — widely considered one of the five greatest living Burgundy winemakers. Meticulous sorting, native yeasts only, modest new oak (typically 20–30% for Grand Crus). The estate owns exceptional Musigny, Bonnes Mares, Ruchottes-Chambertin, and multiple Chambolle Premier Crus. The Musigny is produced in tiny quantities (rarely more than 3 barrels).",
    key_personnel=[{"role": "winemaker", "name": "Christophe Roumier"}],
    production_details={"farming": "lutte raisonnée", "native_yeasts": True,
                        "bc_importer": "Skye Import [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Roumier Musigny ($5,000–$8,000 per bottle at auction) is one of the five wines that defines the upper limit of Burgundy's capacity for elegance and complexity. Christophe Roumier is almost reclusive — he rarely gives interviews and does not travel to sell his wine. The wine sells itself.",
    allocation_notes="By allocation. Extremely difficult to source in BC.",
    price_positioning="ultra_premium", authority_tier=1)

leflaive = P("Domaine Leflaive", "winery", 118, "France",
    production_philosophy="biodynamic_white_burgundy",
    philosophy_description="The reference estate for white Burgundy. Biodynamic since 1997 (Demeter certified 1997). Anne-Claude Leflaive converted the entire domaine — a controversial and expensive decision. Now run by Brice de la Morandière. The estate owns parcels in Le Montrachet, Chevalier-Montrachet, Bâtard-Montrachet, Bienvenues-Bâtard-Montrachet, and multiple Puligny Premier Crus. Burgundy's most celebrated white wine producer.",
    key_personnel=[{"role": "director", "name": "Brice de la Morandière"},
                   {"role": "winemaker", "name": "Pierre Vincent"}],
    production_details={"farming": "biodynamic Demeter", "oak": "no new oak for village, 15-20% new for Premier Cru, 30% new for Grand Cru",
                        "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Anne-Claude Leflaive (died 2015) was one of the most important figures in late-20th-century Burgundy. Under her direction, biodynamics transformed the estate's quality — the wines became richer, more complex, and more defined. Her Montrachet is typically the most expensive white wine from the appellation.",
    allocation_notes="Available through Lifford allocation. Limited quantities.",
    price_positioning="ultra_premium", authority_tier=1)

coche_dury = P("Domaine Coche-Dury", "winery", 117, "France",
    production_philosophy="reductive_precision",
    philosophy_description="The most coveted white Burgundy producer outside Le Montrachet Grand Cru. Jean-François Coche-Dury's Meursault wines — particularly Perrières and the rare Corton-Charlemagne — command prices that rival Leflaive's Montrachet. The philosophy is reductive winemaking to maximum: the wines are aged in barrel with minimal intervention, no fining, no filtration, and the result is wines of extraordinary concentration and longevity from what are technically 'village' and 'Premier Cru' appellations. Now run by son Raphaël.",
    key_personnel=[{"role": "winemaker", "name": "Raphaël Coche-Dury"},
                   {"role": "founder", "name": "Jean-François Coche-Dury"}],
    production_details={"farming": "lutte raisonnée", "vinification": "reductive, minimal intervention",
                        "bc_importer": "Cas-Dri Pacific [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Coche-Dury Meursault Perrières Premier Cru often sells for more than Leflaive's Bâtard-Montrachet Grand Cru — an astonishing reversal of the hierarchy. The Corton-Charlemagne (only ~120 bottles produced per year) is essentially mythological in availability. Production is 2,000–3,000 bottles per cuvée.",
    allocation_notes="Essentially unobtainable commercially. Restaurant allocation only. BCLDB special order if available.",
    price_positioning="ultra_premium", authority_tier=1)

roulot = P("Domaine Guy Roulot", "winery", 117, "France",
    production_philosophy="mineral_precision",
    philosophy_description="Guy Roulot founded the estate; now run by Jean-Marc Roulot (also an actor in French films — a famous dual career). The wines are the most pure and mineral expressions of Meursault — the antithesis of the rich, buttery international Chardonnay stereotype. Old vines, low yields, native yeasts, minimal new oak. The Tessons monopole is the flagship. The philosophy is that the wine should taste of the terroir, not of the winemaker.",
    key_personnel=[{"role": "winemaker", "name": "Jean-Marc Roulot"}],
    production_details={"farming": "lutte raisonnée", "philosophy": "purity over richness",
                        "bc_importer": "Classic Wine Imports [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Jean-Marc Roulot has been increasingly cited as the finest young Meursault producer — his wines are sought by those who want Meursault without the excess richness. His prices have risen dramatically in the 2010s–2020s as Coche-Dury becomes unobtainable.",
    price_positioning="ultra_premium", authority_tier=1)

mugnier = P("Domaine J.-F. Mugnier", "winery", 108, "France",
    production_philosophy="minimalist_elegance",
    philosophy_description="Frédéric Mugnier took back the Chambolle vineyards that were previously rented out and began making wine himself in 1985. His approach is the most minimalist in Burgundy — he describes his role as 'not making wine, but allowing wine to make itself.' No additions, no new oak (or minimal), native yeasts, and whole-cluster fermentation a key tool. His Musigny is produced in around 800 bottles per year — possibly the smallest Grand Cru production in the Côte d'Or.",
    key_personnel=[{"role": "winemaker", "name": "Frédéric Mugnier"}],
    production_details={"farming": "lutte raisonnée", "whole_cluster": "significant use",
                        "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Mugnier's Musigny is arguably the most elegant Grand Cru in Burgundy — purity and translucency as aesthetic principles. The Chambolle village wine and Premier Cru Les Amoureuses are often the most accessible entry points.",
    allocation_notes="Tiny production. Wait-listed at most importers.",
    price_positioning="ultra_premium", authority_tier=1)

dujac = P("Domaine Dujac", "winery", 107, "France",
    production_philosophy="whole_cluster_elegance",
    philosophy_description="Jacques Seysses founded Dujac in 1967 — one of the first 'outsider' domaines (Seysses was not from a wine-making family). Now run with his son Jeremy. The defining style marker is 100% whole-cluster fermentation — uncrushed grape bunches that release carbon dioxide, maintaining purity and freshness. The wines are lighter in colour than peers, highly aromatic, and more translucent in style. Key holdings: Clos de la Roche, Clos Saint-Denis, Bonnes Mares, Échézeaux, Chambolle Premier Crus.",
    key_personnel=[{"role": "winemaker", "name": "Jeremy Seysses"},
                   {"role": "founder", "name": "Jacques Seysses"}],
    production_details={"farming": "certified organic", "whole_cluster": "100%",
                        "bc_importer": "Classic Wine Imports [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Dujac is the reference estate for whole-cluster fermentation in Burgundy. Jeremy Seysses is also the founder of La Paulée — the annual charity dinner in New York that raises funds for wine education. The wines are elegant, aromatic, and consistently compelling.",
    price_positioning="ultra_premium", authority_tier=1)

raveneau = P("Domaine François Raveneau", "winery", 120, "France",
    production_philosophy="traditional_chablis_mineral",
    philosophy_description="The reference Chablis producer — traditional methods, barrel ageing (in old oak, not new), no malolactic fermentation (preserving the natural acidity of Kimmeridgian-terroir Chardonnay). Jean-Marie Raveneau now runs the estate with his son. The wines are produced in tiny quantities from exceptional Grand Cru and Premier Cru parcels. No concession to fashion — the mineral, saline, long-ageing style has not changed in 50 years.",
    key_personnel=[{"role": "winemaker", "name": "Jean-Marie Raveneau"}],
    production_details={"farming": "lutte raisonnée", "malolactic": "blocked", "oak": "old oak only",
                        "bc_importer": "Extremely allocated, BCLDB special order [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Raveneau is to Chablis what DRC is to Vosne-Romanée — the undisputed summit. The Les Clos Grand Cru ages 20+ years. Production is tiny; the wines appear at auction for $400–$800 CAD per bottle.",
    allocation_notes="Essentially unobtainable commercially in BC.",
    price_positioning="ultra_premium", authority_tier=1)

dauvissat = P("Domaine René & Vincent Dauvissat", "winery", 120, "France",
    production_philosophy="traditional_chablis_mineral",
    philosophy_description="The second great traditional Chablis estate alongside Raveneau. Vincent Dauvissat runs the domaine with the same commitment to barrel ageing, no malolactic, and long-lived mineral wines. His Premier Cru La Forest and Grand Cru Les Clos are defining expressions of Kimmeridgian terroir.",
    key_personnel=[{"role": "winemaker", "name": "Vincent Dauvissat"}],
    production_details={"farming": "lutte raisonnée", "malolactic": "blocked",
                        "bc_importer": "Cas-Dri Pacific [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Dauvissat is Raveneau's equal at the top of Chablis. The two estates together define what great Chablis can be — and they produce it in almost identical ways. Dauvissat's prices are slightly lower than Raveneau's, making it the 'entry point' for the upper tier of Chablis.",
    price_positioning="ultra_premium", authority_tier=1)

jadot = P("Maison Louis Jadot", "winery", 114, "France",
    production_philosophy="négociant_quality",
    philosophy_description="One of Burgundy's great négociant houses — also a significant domaine producer in its own right (Domaine des Héritiers Louis Jadot). The house philosophy is quality at all price points, from village Beaune to Grand Cru Musigny. Jadot owns or farms vineyards across the Côte d'Or and Chablis. Their négociant wines are among the most consistent reference points for students of Burgundy.",
    key_personnel=[{"role": "winemaker", "name": "Frédéric Barnier"}],
    production_details={"bc_importer": "Mark Anthony Group / Lifford [NEEDS VERIFICATION]"},
    quality_tier="estate", price_positioning="premium", authority_tier=2)

faiveley = P("Domaine Faiveley", "winery", 111, "France",
    production_philosophy="classic_négociant",
    philosophy_description="One of Burgundy's largest domain-négociant operations. The Faiveley family have been in Nuits-Saint-Georges since 1825. Key holdings: Corton-Charlemagne, Chambertin Clos de Bèze, Gevrey-Chambertin, Nuits-Saint-Georges Premier Crus. Erwan Faiveley now runs the estate. The wines are more accessible and consistent than the ultra-allocations.",
    key_personnel=[{"role": "director", "name": "Erwan Faiveley"}],
    production_details={"bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="estate", price_positioning="premium", authority_tier=2)

# ════════════════════════════════════════════════════════════════════════════════
# BURGUNDY PRODUCTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BURGUNDY PRODUCTS ===")

# DRC wines
drc_rct = PROD(
    "DRC La Romanée-Conti Grand Cru", "wine_still", drc, 110,
    subcategory="pinot noir",
    description="The most celebrated wine on earth. A 1.8-hectare Grand Cru monopole in Vosne-Romanée — the only plot in Burgundy producing a wine named for itself. Ungrafted vines (a small plot survived phylloxera on sand). Yields typically below 15 hl/ha. The wine is never the darkest, never the most tannic, never the most immediately impressive at DRC — yet within 20 years it transcends all peers. The 'Grand Cru' is a BYOB event for the world's most serious collectors. BC availability: auction only.",
    quality_tier="reserve",
    quality_hierarchy=[
        {"level": "Grand Cru", "appellation": "Vosne-Romanée", "note": "monopole — only one owner"},
        {"level": "Production", "detail": "~6,000 bottles per year"},
        {"level": "Rarity", "detail": "Waitlist measured in decades; retail impossible"}
    ],
    deductive_profile={"colour": "garnet to brick", "nose": "violet, roses, forest floor, earth, cherry",
                       "palate": "silk tannins, ethereal acidity, 30–60 year ageing potential",
                       "signature": "translucency — the wine's power is invisible until the finish"},
    service_specs={"temp_c": 16, "decant_minutes": 45, "glass": "large Burgundy Grand Cru",
                   "serve_sequence": "last — the summit of any tasting"},
    flavour_markers=["violet", "rose petal", "black cherry", "forest floor", "earth", "spice", "truffle"],
    flavour_weight="medium-full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$30,000–$50,000+ per bottle at auction")

# DRC La Tâche
drc_lt = PROD(
    "DRC La Tâche Grand Cru", "wine_still", drc, 110,
    subcategory="pinot noir",
    description="DRC's second monopole — 6 hectares in Vosne-Romanée. More powerful and structured than La Romanée-Conti, but from the same biodynamic farming and minimal winemaking approach. La Tâche is often described as 'DRC's greatest red wine' — more consistent vintage to vintage than La Romanée-Conti. Produces approximately 25,000 bottles per year — still extraordinarily rare. The flavour profile is darker and more structured than La Romanée-Conti, with intense spice, earth, and gamey complexity.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "dark cherry, earth, spice, game, violet",
                       "palate": "more structured than Romanée-Conti; dense tannins, 25–50 year potential"},
    service_specs={"temp_c": 16, "decant_minutes": 60, "glass": "large Burgundy Grand Cru"},
    flavour_markers=["dark cherry", "earth", "game", "spice", "violet", "truffle", "iron"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$5,000–$15,000 per bottle at auction")

# Rousseau Chambertin
rousseau_chambertin = PROD(
    "Rousseau Chambertin Grand Cru", "wine_still", rousseau, 106,
    subcategory="pinot noir",
    description="Rousseau's 2.15-hectare parcel in the Chambertin Grand Cru — the jewel of Gevrey-Chambertin. The wine is the definition of powerful Gevrey Pinot Noir: dark fruit, iron, earth, and structure that demands 15–25 years of cellaring. Unlike DRC (which is ethereal), Chambertin from Rousseau is imposing — the 'king' in full regal power. Partial whole-cluster fermentation adds aromatic lift. Around 9,000 bottles per year. BC importer: Lifford Wine Agency [NEEDS VERIFICATION].",
    quality_tier="reserve",
    deductive_profile={"colour": "deep ruby-garnet", "nose": "black cherry, cassis, iron, earth, tobacco",
                       "palate": "full body, firm tannin structure, 15–25 year ageing minimum"},
    service_specs={"temp_c": 16, "decant_minutes": 60},
    flavour_markers=["black cherry", "cassis", "iron", "earth", "tobacco", "dark spice", "game"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,500–$3,000 per bottle")

# Roumier Musigny
roumier_musigny = PROD(
    "Roumier Musigny Grand Cru", "wine_still", roumier, 108,
    subcategory="pinot noir",
    description="Christophe Roumier's 0.1-hectare parcel in Le Musigny — one of the smallest Grand Cru holdings in Burgundy, producing approximately 300–400 bottles per year. The wine is considered the most pure expression of Musigny's feminine elegance: silk over steel, violet-rose perfume, and an extraordinary capacity to age. Because of the tiny production, it is one of the hardest wines to obtain anywhere in the world. Secondary market prices exceed $8,000 per bottle. BC: auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale garnet, translucent", "nose": "violet, rose, wild strawberry, mineral",
                       "palate": "the most silky tannin structure in Burgundy; 20–40 year ageing"},
    service_specs={"temp_c": 15, "decant_minutes": 30, "note": "serve younger than other Grand Crus — the freshness is the point"},
    flavour_markers=["violet", "rose", "wild strawberry", "mineral", "earth", "silk"],
    flavour_weight="medium", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$5,000–$10,000 per bottle at auction")

# Leflaive Montrachet
leflaive_montrachet = PROD(
    "Leflaive Le Montrachet Grand Cru", "wine_still", leflaive, 118,
    subcategory="chardonnay",
    description="Domaine Leflaive's 0.08-hectare parcel in Le Montrachet — the world's most celebrated white wine vineyard. Produces approximately 200–300 bottles per year. The wine that annually 'proves' that dry white wine can achieve the complexity, concentration, and longevity associated only with the greatest reds. White Burgundy at its absolute summit: honeyed richness, electric acidity, Kimmeridgian chalk minerality, and an aftertaste measured in minutes rather than seconds. BC: auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep golden", "nose": "white flower, citrus, almond, honey, chalk mineral",
                       "palate": "extraordinary concentration with electric acidity; 20–30 year ageing"},
    service_specs={"temp_c": 13, "decant_minutes": 20, "glass": "white Burgundy Grand Cru",
                   "note": "serve slightly cooler than red Grand Cru to preserve aromatics"},
    flavour_markers=["white flower", "citrus peel", "almond", "honey", "chalk mineral", "toasted hazelnut"],
    flavour_weight="full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$3,000–$8,000 per bottle at auction")

# Coche-Dury Meursault Perrières
coche_perrierres = PROD(
    "Coche-Dury Meursault Perrières Premier Cru", "wine_still", coche_dury, 117,
    subcategory="chardonnay",
    description="The wine that proves a Premier Cru can transcend the Grand Cru hierarchy. Jean-François Coche-Dury's parcel in the Perrières Premier Cru — the finest Premier Cru vineyard in Meursault — produces approximately 400–600 bottles per year. The wine is reductively vinified to preserve maximum mineral precision. The result is a Meursault of extraordinary tension and longevity — it does not drink well young (it is almost shut down) but after 10+ years becomes one of the world's great white wines. Secondary market: $800–$2,500 per bottle. BC: auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale gold", "nose": "green apple, mineral, chalk, white flower, subtle oak",
                       "palate": "tight and closed young; after 10 years, extraordinary complexity; 20+ year potential"},
    service_specs={"temp_c": 13, "decant_minutes": 15, "note": "requires 10+ years cellaring before drinking"},
    flavour_markers=["green apple", "mineral", "chalk", "white flower", "lemon curd", "brioche (with age)"],
    flavour_weight="medium-full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$800–$2,500 per bottle")

# Raveneau Chablis Grand Cru Les Clos
raveneau_les_clos = PROD(
    "Raveneau Chablis Grand Cru Les Clos", "wine_still", raveneau, 120,
    subcategory="chardonnay",
    description="The reference wine for Chablis Grand Cru and for Kimmeridgian chalk-sourced Chardonnay. Les Clos is considered the finest of Chablis' seven Grand Cru vineyards — the steepest, most concentrated, and most structured. Raveneau's parcel produces a wine of exceptional longevity (20+ years in great vintages). The hallmark is almost saline mineral precision — oyster shell, lemon, chalk — with no obvious oak character despite barrel ageing in old wood. The wine demonstrates the 'terroir transparency' that makes the greatest white Burgundies unique.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale gold with green tints", "nose": "oyster shell, lemon, chalk, white flower",
                       "palate": "searingly dry and mineral; 15–20 year ageing potential"},
    service_specs={"temp_c": 12, "decant_minutes": 10},
    flavour_markers=["oyster shell", "lemon", "chalk", "white flower", "green apple", "mineral", "iodine"],
    flavour_weight="medium", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$400–$800 per bottle")

# Mugnier Musigny
mugnier_musigny = PROD(
    "Mugnier Musigny Grand Cru", "wine_still", mugnier, 108,
    subcategory="pinot noir",
    description="Frédéric Mugnier's 0.5-hectare parcel in Le Musigny — one of the great Burgundy unicorns. Around 800 bottles per year. The philosophy is absolute minimalism — whole-cluster fermentation, native yeasts, no new oak, no additions. The wine is astonishingly pale and translucent yet achingly complex. Considered by many sommeliers to be the finest red wine on earth at its peak — around 15 years from vintage. BC: auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "very pale garnet, translucent", "nose": "rose petal, violet, earth, spice, red fruit",
                       "palate": "ethereal — silk texture, long acid line, 20–30 year potential"},
    service_specs={"temp_c": 15, "decant_minutes": 20},
    flavour_markers=["rose petal", "violet", "red cherry", "earth", "mineral", "spice"],
    flavour_weight="medium-light", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$3,000–$8,000 per bottle at auction")

# Jadot Chambertin Clos de Bèze
jadot_beze = PROD(
    "Jadot Chambertin Clos de Bèze Grand Cru", "wine_still", jadot, 106,
    subcategory="pinot noir",
    description="Louis Jadot's parcel in Chambertin Clos de Bèze — one of Gevrey's two greatest Grand Crus (legally permitted to add 'Chambertin' to its name). The négociant-domaine's most prestigious bottling. More accessible pricing than Rousseau or DRC, making it the entry point for serious Gevrey Grand Cru on BC wine lists. Around 3,000–4,000 bottles per year. BC importer: Mark Anthony Group / Lifford.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "dark cherry, earth, iron, tobacco",
                       "palate": "firm tannins, full body, 15–25 year ageing"},
    service_specs={"temp_c": 16, "decant_minutes": 60},
    flavour_markers=["dark cherry", "earth", "iron", "tobacco", "spice"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$400–$700 per bottle")

# Dauvissat Chablis Premier Cru La Forest
dauvissat_forest = PROD(
    "Dauvissat Chablis Premier Cru La Forest", "wine_still", dauvissat, 120,
    subcategory="chardonnay",
    description="Vincent Dauvissat's parcel in the La Forest Premier Cru — one of Chablis' finest single-vineyard sites, adjacent to Grand Cru Les Clos. Barrel-aged in old oak, no malolactic, long lees contact. The wine is tighter and more mineral-driven than the Grand Cru bottlings but achieves similar longevity. The entry point for serious Dauvissat study. BC importer: Cas-Dri Pacific [NEEDS VERIFICATION].",
    quality_tier="reserve",
    deductive_profile={"colour": "pale gold", "nose": "oyster shell, chalk, lemon, mineral",
                       "palate": "taut, dry, mineral; 10–15 year ageing"},
    service_specs={"temp_c": 12, "decant_minutes": 0},
    flavour_markers=["oyster shell", "chalk", "lemon", "mineral", "green herb"],
    flavour_weight="medium", flavour_profile_type="mineral",
    price_tier="premium", price_range_cad="$180–$300 per bottle")

# Roulot Meursault Charmes
roulot_charmes = PROD(
    "Roulot Meursault Les Charmes Premier Cru", "wine_still", roulot, 117,
    subcategory="chardonnay",
    description="Jean-Marc Roulot's parcel in Les Charmes — the most generous and approachable of Meursault's Premier Crus. The wine is structured and mineral rather than rich and buttery — it represents the antithesis of the Meursault cliché. Produced with native yeasts, used oak only, and no reductive winemaking (the opposite of Coche-Dury's approach). BC importer: Classic Wine Imports [NEEDS VERIFICATION].",
    quality_tier="reserve",
    deductive_profile={"colour": "medium gold", "nose": "lemon, white flower, almond, mineral",
                       "palate": "mineral and precise; less rich than typical Meursault; 8–15 year ageing"},
    service_specs={"temp_c": 13, "decant_minutes": 0},
    flavour_markers=["lemon", "white flower", "almond", "mineral", "chalky"],
    flavour_weight="medium-full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$300–$600 per bottle")

# Faiveley Corton-Charlemagne Grand Cru
faiveley_cc = PROD(
    "Faiveley Corton-Charlemagne Grand Cru", "wine_still", faiveley, 113,
    subcategory="chardonnay",
    description="Domaine Faiveley's parcel in the Corton-Charlemagne Grand Cru — the most powerful white wine Grand Cru in the Côte de Beaune. Corton-Charlemagne is richer and more structured than Meursault Premier Cru, with more mineral backbone and higher ageing potential. Faiveley's expression is consistent and well-priced relative to Bonneau du Martray (the single-estate benchmark). BC importer: Lifford Wine Agency.",
    quality_tier="estate",
    deductive_profile={"colour": "deep gold", "nose": "green apple, citrus, mineral, subtle oak",
                       "palate": "full body, firm acid, 10–20 year ageing"},
    service_specs={"temp_c": 13, "decant_minutes": 15},
    flavour_markers=["green apple", "lemon", "chalk mineral", "subtle oak", "toasted almond"],
    flavour_weight="full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$200–$350 per bottle")

# ════════════════════════════════════════════════════════════════════════════════
# BURGUNDY BEVERAGE REFERENCES
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BURGUNDY REFERENCES ===")

REF(
    "Burgundy Classification System — The Hierarchy",
    "wine_regions",
    description="The Burgundy classification system is the most precise site-quality hierarchy in the wine world — and the model that all other fine wine regions have borrowed or reacted against. Unlike Bordeaux (classified by château) or Champagne (classified by village), Burgundy's system classifies individual plots of land (lieux-dits and délimités) irrespective of ownership. The same Grand Cru vineyard may have 80+ different owners producing wines of wildly different quality — the hierarchy classifies the land, not the producer.",
    key_principles="""FOUR-TIER HIERARCHY (ascending quality):

1. RÉGIONALE (Regional): The broadest category. Wines may be sourced from anywhere within the broader region. Examples: Bourgogne Rouge, Bourgogne Blanc, Bourgogne Aligoté. Can include declassified premier and grand cru fruit in a bad year. This is the entry level of the appellation system.

2. VILLAGE (Communale): Wines from within a single named village or commune. The village name appears on the label. Example: Gevrey-Chambertin (village), Meursault (village), Vosne-Romanée (village). Quality here depends almost entirely on producer — a Roulot Meursault village wine is better than a lesser producer's Premier Cru.

3. PREMIER CRU (1er Cru): Individual named vineyards within a village that have been officially designated superior by the INAO. There are approximately 640 Premier Cru vineyards across Burgundy. They appear on the label as: "Gevrey-Chambertin Premier Cru Les Cazetiers" or "Gevrey-Chambertin 1er Cru." Quality varies enormously — the best Premier Crus (Volnay Caillerets, Chambolle Les Amoureuses, Gevrey Clos Saint-Jacques) are consistently better than many Grand Crus.

4. GRAND CRU: The summit — 33 Grand Cru vineyards (plus 8 shared between communes, giving approximately 33 distinct names). The Grand Cru stands alone on the label — the village name is NOT included. Example: "Chambertin" (not "Gevrey-Chambertin Chambertin"). The 33 Grand Crus are (roughly north to south): Chambertin, Chambertin Clos de Bèze, Chapelle-Chambertin, Charmes-Chambertin, Gevrey-Chambertin Grands Crus + Clos Saint-Denis, Clos de la Roche (Morey) + Clos des Lambrays, Clos de Tart, Bonnes Mares (shared Morey/Chambolle), Musigny (Chambolle), Clos de Vougeot (Vougeot), Échézeaux and Grands Échézeaux (Flagey-Échézeaux), Richebourg, La Romanée, Romanée-Conti, Romanée-Saint-Vivant, La Tâche (Vosne-Romanée), Corton (red; Aloxe-Corton), Corton-Charlemagne (white; Aloxe-Corton/Pernand-Vergelesses), Bâtard-Montrachet, Bienvenues-Bâtard-Montrachet (shared Puligny/Chassagne), Chevalier-Montrachet, Le Montrachet (shared Puligny/Chassagne), Criots-Bâtard-Montrachet (Chassagne only).

MS EXAM CRITICAL DISTINCTION: The Grand Cru label reads ONLY the vineyard name — no village. A label reading "Musigny Grand Cru" stands alone; "Chambolle-Musigny Musigny" is incorrect.

PRODUCER MATTERS MORE THAN VINEYARD: In Burgundy, producer quality can override hierarchy. A village wine from Rousseau or Roulot will be better than a Grand Cru from a careless producer. The hierarchy classifies the land; the producer determines whether the land's potential is realised.

THE NÉGOCIANT SYSTEM: Burgundy's fragmented ownership model created the négociant — a merchant who purchases grapes or juice from multiple growers and produces wines under their own label. Jadot, Drouhin, Bouchard, Faiveley operate both as domaines (owning vineyards) and as négociants (purchasing from others). The distinction matters: a domaine wine is estate-grown; a négociant wine may be from purchased grapes of variable quality.""",
    skill_level="advanced",
    source_text="WSET Diploma / Court of Master Sommeliers Certified and Advanced Curriculum")

REF(
    "Burgundy — Pinot Noir Deductive Tasting Framework",
    "blind_tasting",
    description="Pinot Noir is the world's most site-sensitive red grape variety — the tasting differences between a Gevrey-Chambertin, a Chambolle-Musigny, and a Vosne-Romanée are measurable and learnable. This framework applies the Court of Master Sommeliers SAT (Systematic Approach to Tasting) to Burgundy's Pinot Noir with commune-by-commune terroir fingerprints.",
    key_principles="""COMMUNE CHARACTER PROFILES (for blind tasting):

GEVREY-CHAMBERTIN: The most powerful commune. Deep ruby-garnet colour (for Pinot Noir). Nose: dark cherry, blackcurrant, iron/mineral, tobacco, earth, wild game (especially older vintages). Palate: Full-bodied for Pinot Noir, firm tannin structure, high acidity, long finish with iron mineral note. Key indicator: if Burgundy feels 'dense' and 'structured,' think Gevrey-Chambertin or its neighbours (Morey-Saint-Denis).

CHAMBOLLE-MUSIGNY: The most elegant commune. Lighter, more transparent colour. Nose: red cherry, rose petal, violet, wild strawberry, mineral. Palate: Silky tannins (the most silky in Burgundy), moderate-to-high acidity, ethereal finish. Key indicator: if red Burgundy seems almost translucent and perfumed, think Chambolle-Musigny or Volnay.

VOSNE-ROMANÉE: The 'middle path' of the Côte de Nuits — combining power with elegance. Deep garnet. Nose: complex spice, black cherry, violet, earth, forest floor, subtle game. Palate: Rich tannin structure but not as dense as Gevrey; exceptional length; the most 'complete' commune profile.

NUITS-SAINT-GEORGES: Earthy and meaty. Darker colour than Chambolle. Nose: black cherry, dried plum, earth, leather, game, truffle. Palate: More rustic tannins, full body, earthy finish. Key indicator: earthy, gamy Burgundy with broad tannin = often Nuits.

POMMARD (Côte de Beaune): The most structured Côte de Beaune red. Iron-rich clay creates density unusual for the commune. Often confused with Côte de Nuits at blind tasting. Nose: dark plum, iron, earth. Palate: firm, drying tannins.

VOLNAY: The most elegant Côte de Beaune red — often confused with Chambolle at blind tasting. Lighter colour. Nose: violets, red cherry, mineral. Palate: silky tannins, high acidity.

COLOUR/AGE INDICATORS:
- Young Burgundy (1–5 years): Ruby-garnet, vibrant red-fruit nose, tannins apparent
- Mid-age (6–15 years): Garnet to brick rim, secondary aromas (earth, game, forest floor) emerging
- Older (15+ years): Brick to amber rim, tertiary aromas (leather, mushroom, truffle), silky tannins

CLASSIC BURGUNDY BLIND TASTING ERROR: Confusing old Burgundy (pale, brick-rimmed, earthy) with a Pinot Noir from Alsace or Germany — similar colour and structure. The key differentiator is Burgundy's greater acidity and mineral backbone.""",
    skill_level="advanced",
    source_text="Court of Master Sommeliers Advanced Theory")

REF(
    "Chablis — Kimmeridgian Terroir and the Mineral Palate",
    "wine_regions",
    description="Chablis is the world's most famous example of mineral terroir — the hypothesis that soil chemistry and structure are directly expressible in the flavour of wine. The Kimmeridgian limestone of Chablis contains fossilised Exogyra virgula oyster shells from a prehistoric inland sea, 150 million years old. Whether the perceived 'oyster shell' or 'saline' flavour is literally derived from these fossils or is a phenomenological experience created by acidity and pH is debated — but the perceptual reality of 'mineral' Chablis is beyond question.",
    key_principles="""THE KIMMERIDGIAN LIMESTONE:
Named after Kimmeridge Bay in Dorset, England, where the same geological formation appears. In Chablis, this Jurassic-era chalk and clay (with calcite and fossil-rich layers) creates the defining soil of the Grand Cru and Premier Cru vineyards on the right bank of the Serein river.

PORTLANDIAN LIMESTONE: The less prestigious soils of the expanded Chablis and Petit Chablis appellations. Younger, less fossil-rich, produces more straightforward, less mineral wines.

WHY CHABLIS IS TART: Northern latitude (47.8°N — equivalent to Bordeaux north of its latitude limit), coolest wine climate in Burgundy, and limestone soils that maintain low pH. The resulting wine naturally has high acid and crisp citrus character.

FOUR QUALITY TIERS:
1. Petit Chablis: Portlandian limestone, flatlands. Fresh, simple, drink young.
2. Chablis (Village): Mix of soils. Clean, crisp, mineral. 2–5 year drinking.
3. Chablis Premier Cru: 40 named vineyards grouped into 17 designations. Best: Montée de Tonnerre (consistently finest), Montmains, Côte de Léchet, Vaillons. 5–12 year drinking.
4. Chablis Grand Cru: 7 named Grand Crus on a single contiguous south/southeast-facing slope: Blanchot, Bougros, Les Clos (greatest), Grenouilles, Preuses, Vaudésir, Valmur. 10–25 year drinking for top producers.

OAK OR NO OAK:
The central stylistic debate in Chablis. Traditional camp (Raveneau, Dauvissat): old oak barrels for secondary fermentation, creating texture without oak flavour. Modern camp (William Fèvre, Domaine Laroche): stainless steel tanks, maximum freshness and primary fruit.
MS position: Neither approach is universally superior — the terroir expresses itself equally through both methods in the right hands.

MALOLACTIC FERMENTATION:
Traditional Chablis blocks or partially blocks malolactic to preserve acidity. Modern Chablis may allow full malolactic for a rounder, less tart style. The no-malolactic approach is most consistent with Grand Cru ambitions.

SERVICE NOTES:
Temperature: 10–13°C. No decanting required. If Premier Cru or Grand Cru is less than 5 years old, allow to open in the glass for 15 minutes.""",
    skill_level="advanced",
    source_text="Jancis Robinson's Wine Course / WSET Diploma")

# ════════════════════════════════════════════════════════════════════════════════
# BURGUNDY PAIRING INTELLIGENCE
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BURGUNDY PAIRINGS ===")

# DRC La Romanée-Conti pairings
PAIR("Roasted squab with truffle jus and wild mushroom ragù", "main",
     "wine_still", "main", "classic", "complement",
     "The ethereal silk and forest-floor character of La Romanée-Conti meets roasted squab's gamey richness — the truffle jus bridges the wine's tertiary character while mushroom ragù echoes the Grand Cru's earthiness. The wine's tannin is so fine it barely needs food; the squab is its equal.",
     drc_rct)

PAIR("Seared Périgord foie gras with cherry compote", "amuse",
     "wine_still", "amuse", "adventurous", "bridge",
     "The fat of foie gras coats the palate, allowing DRC's silky tannin to appear even more ethereal. The cherry compote mirrors the wine's red fruit. A legendary pairing for high-ceremony dining.",
     drc_rct)

PAIR("Aged comté cheese — 36 months", "cheese",
     "wine_still", "cheese", "classic", "complement",
     "Aged Comté with its crystalline texture, caramel-salt, and mushroom notes is the textbook pairing for mature Grand Cru Pinot Noir. The umami richness of the cheese amplifies the wine's earthiness without overwhelming it.",
     drc_rct)

# Rousseau Chambertin pairings
PAIR("Braised wild boar shoulder with black truffle and lardons", "main",
     "wine_still", "main", "classic", "complement",
     "The power of Chambertin — iron, dark fruit, earth — demands equally assertive food. Wild boar's gamey richness and the truffle's earthiness mirror the Grand Cru's tertiary complexity. Classic Burgundian alignment.",
     rousseau_chambertin)

PAIR("Duck confit with Puy lentils and thyme jus", "main",
     "wine_still", "main", "established", "complement",
     "Duck confit's rendered fat and Puy lentils' earthy minerality create a foil for structured Gevrey Pinot Noir. The thyme jus provides herbal lift that echoes the wine's secondary aromatics.",
     rousseau_chambertin)

# Roumier Musigny pairings
PAIR("Seared pigeon with wild strawberry and beet jus", "main",
     "wine_still", "main", "classic", "complement",
     "Musigny's ethereal violet-strawberry perfume aligns with pigeon's subtle game and the sweet-acidic wild strawberry sauce. The beet jus adds earthiness without weight — matching Musigny's delicacy.",
     roumier_musigny)

PAIR("Ravioli of Époisses cheese with brown butter", "starter",
     "wine_still", "starter", "adventurous", "bridge",
     "Époisses — the great washed-rind cheese of Burgundy — in pasta form creates a rich, pungent foil for Musigny's silk. The brown butter adds nuttiness. A luxurious Burgundian self-reference pairing.",
     roumier_musigny)

# Leflaive Montrachet pairings
PAIR("Butter-poached Breton lobster with caviar and leek cream", "fish_course",
     "wine_still", "main", "classic", "complement",
     "The world's greatest dry white wine meets the world's greatest crustacean. Butter-poached lobster's fat richness is cut by Montrachet's electric acidity; caviar adds saline mineral counterpoint; leek cream provides herbaceous lift. The textbook grand occasion white wine pairing.",
     leflaive_montrachet)

PAIR("Roasted turbot with morel mushrooms and Montrachet butter sauce", "fish_course",
     "wine_still", "main", "classic", "complement",
     "Turbot — the king of flatfish — has sufficient fat and firmness to match Montrachet's concentration. Morel mushrooms add earthy complexity. A Montrachet butter sauce (using the wine itself) creates a self-referential mirror.",
     leflaive_montrachet)

# Coche-Dury Meursault Perrières pairings
PAIR("Sweetbread with capers, lemon, and sauce gribiche", "main",
     "wine_still", "main", "established", "bridge",
     "Veal sweetbread's creamy richness and subtle sweetness is cut by Perrières' mineral tension. The capers and gribiche provide acidic counterpoint that extends the wine's length. A great Meursault Premier Cru demands food with fat content to balance its compressed mineral structure.",
     coche_perrierres)

PAIR("Scallop and black truffle with celeriac puree", "fish_course",
     "wine_still", "main", "classic", "complement",
     "Scallop's natural sweetness and iodine note pairs naturally with Chablis and Meursault styles. The black truffle adds earthiness that meets the wine's mineral depth; celeriac puree provides a starchy counter to Perrières' acidity.",
     coche_perrierres)

# Raveneau Les Clos pairings
PAIR("Belon oysters with mignonette", "starter",
     "wine_still", "amuse", "classic", "complement",
     "The textbook match for Chablis Grand Cru: the Kimmeridgian soil of Les Clos contains fossilised oyster shells, and the wine's saline mineral palate mirrors the oyster's brininess. Serve both very cold. The mignonette's vinegar acidity is absorbed by the wine's acid backbone.",
     raveneau_les_clos)

PAIR("Sole meunière with haricots verts and caper beurre blanc", "fish_course",
     "wine_still", "main", "classic", "complement",
     "Classic Chablis Grand Cru pairing: sole's delicacy and the meunière butter amplified by the wine's mineral salinity. The caper acidity mirrors Chablis' characteristic tartness. Simple, perfect — the pairing requires no elaboration.",
     raveneau_les_clos)

PAIR("Grilled langoustine with garlic butter", "fish_course",
     "wine_still", "main", "established", "complement",
     "Langoustine's sweet, delicate flesh and garlic butter create a rich but focused foil for Chablis Grand Cru's clean mineral acidity. A coastal pairing in a landlocked wine — Chablis 'remembers' the sea through its Kimmeridgian fossil soil.",
     raveneau_les_clos)

print("\n✅ Burgundy batch complete.")
print(f"Producers: DRC, Leroy, Rousseau, Roumier, Leflaive, Coche-Dury, Roulot, Mugnier, Dujac, Raveneau, Dauvissat, Jadot, Faiveley")
print(f"Products: 12 wines including DRC Romanée-Conti, La Tâche, Rousseau Chambertin, Roumier Musigny, Leflaive Montrachet, Coche-Dury Perrières, Raveneau Les Clos, Mugnier Musigny, Jadot Clos de Bèze, Dauvissat La Forest, Roulot Charmes, Faiveley Corton-Charlemagne")
print(f"References: 3 (Classification, Pinot Noir Tasting, Chablis Terroir)")

cur.close()
conn.close()
