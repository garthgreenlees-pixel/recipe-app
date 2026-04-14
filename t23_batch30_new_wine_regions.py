#!/usr/bin/env python3
"""T23 Batch 30 — New wine regions: Bairrada DOC (Portugal), Pomerol AOC (France), Chambolle-Musigny AOC (France), Vosne-Romanée AOC (France), Patrimonio AOC (Corsica/France)"""

import psycopg2

conn = psycopg2.connect(
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
)
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
       reputation_tier, quality_trajectory, description, key_producers,
       historical_context, authority_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1) RETURNING id""",
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
    cur.execute("SELECT id FROM beverage_products WHERE name=%s AND producer_id=%s",
                (name, producer_id))
    row = cur.fetchone()
    if row:
        print(f"  Product exists: {name} ({row[0]})")
        return row[0], False
    cur.execute("""INSERT INTO beverage_products
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
      (name, category, subcategory, producer_id, region_id, origin_country,
       description, price_tier))
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

# ── BAIRRADA DOC (PORTUGAL) ───────────────────────────────────────
print("\n=== Bairrada DOC (Portugal) ===")
r_bai = R("Bairrada", "Portugal", "wine",
           designation_type="DOC",
           designation_name="Bairrada DOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Portugal's most dramatic and uncompromising red wine DOC — the Atlantic coastal clay soils of the Beira Litoral between Coimbra and Aveiro producing Baga, one of the world's most extreme red wine grapes: tiny berries, extraordinarily thick skins, very high tannin and acidity, demanding 10-20+ years to soften. In lesser hands Baga produces harsh, astringent wine; in the hands of Luís Pato and other committed producers it achieves extraordinary age-worthy complexity rivaling the finest European red wines. The region also produces outstanding Bical-based whites and Bairrada Espumante (traditional method sparkling wine of real distinction).",
           key_producers="Luís Pato, Filipa Pato, Quinta do Encontro, Sidónio de Sousa, Caves Aliança, João Portugal Ramos",
           historical_context="Baga — whose name means 'berry' in Portuguese — is likely one of Portugal's most ancient indigenous varieties, adapted to the Atlantic coastal clay's cool, humid climate. The variety's extraordinary tannin and acidity made it ideally suited to aging in the large oak tonels that were Bairrada's traditional vessels, and the finest pre-1970s Bairradas from estates like Sidónio de Sousa still drink magnificently today. Luís Pato — the 'Baron of Baga' — dedicated his career to proving that low yields and careful winemaking could transform Baga's natural astringency into complexity. His daughter Filipa Pato has taken the region further in the natural wine direction, adding terroir precision and minimal-intervention elegance.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Bairrada vintage; Baga from Atlantic coastal clay showed extraordinary concentration and the variety's characteristic iron-mineral structure with unusual freshness."),
    (2021, "very_good", "stable", "Classic vintage; Atlantic influence maintained the cool, humid conditions that Baga needs; wines of excellent natural acidity and dark cherry depth."),
    (2020, "excellent", "stable", "Benchmark year; Luís Pato and Filipa Pato both produced wines of extraordinary depth; the vintage's freshness revealed Baga's age-worthy character at its most compelling."),
    (2019, "excellent", "rising", "Outstanding vintage; Baga of historic concentration and longevity; the natural wine community's discovery of Bairrada accelerated internationally."),
    (2018, "very_good", "stable", "Warm vintage by Bairrada standards; Baga of good concentration and the characteristic dark cherry-iron structure; more accessible than cooler vintages."),
]:
    VIN(r_bai, yr, qd, pt, sn)

p_lpa = P("Luís Pato", "Portugal", r_bai,
           description="The 'Baron of Baga' — Luís Pato's decades of commitment to proving Baga's potential for world-class red wine production has fundamentally changed international perception of Bairrada. His Vinha Pan, Vinha Formal, and Quinta do Ribeirinho Pe Franco (pre-phylloxera ungrafted vines) are the appellation's benchmark wines. Pato's obsessive low-yield approach and his deep understanding of each clay parcel's character makes him Portugal's most respected academic and practitioner of indigenous wine varieties.")
prod_lpa, new = PROD("Luís Pato Vinha Pan Bairrada Baga", "wine_still", p_lpa, r_bai, "Portugal",
                     subcategory="Baga",
                     description="The most internationally recognized serious Baga — Luís Pato's Vinha Pan from Atlantic coastal clay soils, aged in large Portuguese oak. Extraordinary dark cherry, blackberry, iron mineral, dried herbs, leather, and the characteristic Baga tannin that softens over 10+ years into extraordinary complexity. The wine that proved Baga deserves to be spoken of alongside the world's great age-worthy red varieties. Portugal's most distinctively indigenous red.",
                     price_tier="premium")
if new:
    PAIR(prod_lpa, "Leitão da Bairrada (Bairrada roast suckling pig) with orange, cumin, and bay", "complement", "classic", "main", "The most famous food-wine pairing in Portugal — Bairrada's suckling pig and its Baga wine; the wine's iron tannin and dark cherry cuts through the pig's extraordinary crackled fat; orange mirrors the wine's acidity; cumin bridges the herbal complexity")
    PAIR(prod_lpa, "Chanfana (old goat braised in red wine with paprika, garlic, and bay) on broa", "complement", "classic", "main", "The Centre-North's mountain preparation and its Baga wine — old goat's intense flavour is bridged by the wine's dark cherry and iron mineral; the wine appears in the braising liquid; paprika bridges the wine's spice")

p_fpa = P("Filipa Pato", "Portugal", r_bai,
           description="Luís Pato's daughter — Filipa Pato's natural wine approach to Bairrada and Baga has added a terroir-precise, minimal-intervention dimension that complements her father's more traditional approach. Her 3B wines (3 Bicas — the local name for Baga clusters) and the Nossa Calcário (on limestone soils) demonstrate Baga's capacity for elegance and freshness alongside its natural power. Filipa Pato is considered one of Portugal's most exciting winemakers and has brought Bairrada to the international natural wine community.")
prod_fpa, new = PROD("Filipa Pato Nossa Calcário Bairrada Branco", "wine_still", p_fpa, r_bai, "Portugal",
                     subcategory="Bical",
                     description="Bairrada's most acclaimed white wine — Filipa Pato's Bical from the limestone soils of the Calcário parcel, minimal intervention and natural fermentation. Lemon oil, white peach, chalk mineral, hazelnut, and the distinctive saline freshness that limestone imparts to Atlantic Portuguese whites. Develops magnificently over 5-8 years into something resembling Loire valley Chenin Blanc. The white wine that revealed Bairrada's dual potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_fpa, "Amêijoas à Bulhão Pato (clams with white wine, garlic, lemon, and coriander)", "complement", "classic", "aperitif", "The Lisbon classic and the Atlantic Portuguese white — Bairrada Bical's chalk mineral and lemon oil character bridges the clams' oceanic brine; garlic mirrors the wine's complexity; coriander bridges the wine's herbal freshness")
    PAIR(prod_fpa, "Bacalhau com broa (salt cod with corn bread crust, potato, and olive oil)", "complement", "classic", "main", "Portugal's national dish and its Atlantic white — Bical's chalk mineral and lemon character bridges the salt cod's salinity; broa's corn sweetness contrasts the wine's mineral austerity; olive oil bridges the textural richness")

# ── POMEROL AOC (FRANCE) ──────────────────────────────────────────
print("\n=== Pomerol AOC (France) ===")
r_pom = R("Pomerol", "France", "wine",
           designation_type="AOC",
           designation_name="Pomerol AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Bordeaux's most prestigious right bank appellation and the spiritual home of Merlot — the tiny 800-hectare plateau northeast of Libourne on unique iron-rich clay (crasse de fer) soils over an iron-rich subsoil that gives Pomerol's Merlot its distinctive truffled, velvety, and plush character. Pomerol has no official classification — by convention, Petrus and Le Pin are considered the appellation's greatest estates, but dozens of other châteaux produce Merlot-dominated wines of extraordinary richness, complexity, and longevity. The best Pomerol — from the blue clay plateau's heart — develops extraordinary truffle, leather, and velvet complexity over 20-30 years.",
           key_producers="Château Petrus, Le Pin, Vieux Château Certan, Lafleur, Clinet, La Conseillante, Trotanoy, L'Eglise-Clinet",
           historical_context="Pomerol's rise to wine world eminence is one of the great modern wine stories — until the 1960s, the appellation's wines were largely sold through Libourne négociants at modest prices, considered inferior to the Médoc's classified growths. Jean-Pierre Moueix's promotion of Petrus through American import channels transformed the appellation into a luxury commodity, and Christian Moueix's famous 1982 vintage (released at $35 in the US, now selling at auction for $3,000+) made Pomerol internationally famous. The tiny Le Pin estate (2.5 hectares) owned by Jacques Thienpont produces Pomerol at prices occasionally exceeding Petrus — the world's most expensive wine per case.")

for yr, qd, pt, sn in [
    (2022, "exceptional", "rising", "One of the greatest Pomerol vintages ever; the blue clay plateau's iron-rich crasse de fer produced Merlot of legendary truffled complexity and 30+ year potential."),
    (2021, "excellent", "stable", "Outstanding vintage; right bank clay retained moisture in warm conditions; Merlot of excellent freshness and the characteristic Pomerol velvet texture."),
    (2020, "exceptional", "rising", "Legendary vintage; Petrus, La Fleur-Petrus, and Vieux Château Certan produced wines of historic quality; Pomerol's greatest decade-defining vintage."),
    (2019, "excellent", "stable", "Benchmark year; Merlot of generous richness and the distinctive crasse de fer truffle character; wines of 20+ year aging potential across the appellation."),
    (2018, "excellent", "stable", "Warm vintage producing Pomerol of unusual concentration; the iron-rich clay produced wines of good structure alongside the typical plush, velvety character."),
]:
    VIN(r_pom, yr, qd, pt, sn)

p_vtc = P("Vieux Château Certan", "France", r_pom,
           description="The Thienpont family's historic Pomerol estate — considered by many critics to be the finest wine in Pomerol after Petrus and Le Pin, and by some to surpass both. VCC's unique blend of Merlot, Cabernet Franc, and Cabernet Sauvignon (unusual in Pomerol) produces wines of extraordinary complexity, structure, and longevity that develop over 25+ years into something approaching Haut-Brion in depth. The 2012 and 2020 vintages are considered among the greatest Pomerol wines ever produced.")
prod_vtc, new = PROD("Vieux Château Certan Pomerol", "wine_still", p_vtc, r_pom, "France",
                     subcategory="Merlot",
                     description="Pomerol's most complex and age-worthy estate wine — the Thienpont family's unique Merlot, Cabernet Franc, and Cabernet Sauvignon blend from the plateau's iron-rich blue clay. Dark cherry, truffle, dark chocolate, cedar, violets, leather, and the extraordinary velvety texture of the finest Pomerol. More structured than many right bank wines; develops 25+ years. The intellectual alternative to Petrus's pure Merlot power.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_vtc, "Truffe noire entière baked in foie gras croûte with black truffle cream", "complement", "classic", "main", "The pinnacle of Périgord luxury and Pomerol's most complex estate wine — the wine's truffle and chocolate character finds direct resonance in the black truffle preparation; foie gras's richness meets Pomerol's velvet texture; the circular truffle pairing at its most extravagant")
    PAIR(prod_vtc, "Magret de canard confiture (duck breast with cherry jam reduction) and pommes allumettes", "complement", "classic", "main", "The Right Bank's classic preparation and its most complex estate wine — VCC's dark cherry and truffle character bridges the duck's rich fat; cherry reduction mirrors the wine's dark fruit; the wine's Cabernet Franc structure handles the richness")

p_con = P("Château La Conseillante", "France", r_pom,
           description="The Nicolas family's Pomerol estate adjacent to Petrus and Cheval Blanc — producing wines of extraordinary aromatic elegance and truffled complexity from the blue clay plateau's heart. La Conseillante is considered the most feminine and perfumed of the great Pomerol estates, valued for its silky texture, violet and truffle aromatics, and a consistency that makes it one of the appellation's most reliable fine wine purchases.")
prod_con, new = PROD("Château La Conseillante Pomerol", "wine_still", p_con, r_pom, "France",
                     subcategory="Merlot",
                     description="Pomerol's most perfumed and feminine estate wine — La Conseillante's Merlot with Cabernet Franc from the blue clay plateau adjacent to Petrus. Violet, truffle, dark cherry, raspberry coulis, cedar, and the extraordinary silky texture that makes this wine the most approachable of the great Pomerol estates. Develops magnificently over 15-20 years but offers pleasure earlier than VCC or Trotanoy. The perfumed face of Pomerol at its most seductive.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_con, "Selle d'agneau de lait rôtie (roasted milk-fed lamb saddle) with wild garlic and spring vegetables", "complement", "classic", "main", "Spring Pomerol pairing — the wine's violet and truffle aromatics bridge the milk-fed lamb's extraordinary delicacy; wild garlic mirrors the wine's floral complexity; spring vegetables provide a fresh contrast to the velvet richness")
    PAIR(prod_con, "Poitrine de pigeon en persillade (parsleyed pigeon breast) with lentils and foie gras", "complement", "classic", "main", "Pomerol's silky texture and violet perfume bridges the pigeon's rich, gamey breast; foie gras adds the luxury dimension that matches the wine's premium character; lentils provide earthiness that bridges the truffle note")

# ── CHAMBOLLE-MUSIGNY AOC (FRANCE) ────────────────────────────────
print("\n=== Chambolle-Musigny AOC (France) ===")
r_cha_m = R("Chambolle-Musigny", "France", "wine",
             designation_type="AOC",
             designation_name="Chambolle-Musigny AOC",
             reputation_tier="iconic",
             quality_trajectory="established",
             description="Burgundy's most ethereal and feminine village appellation — the limestone hillsides between Vougeot and Morey-Saint-Denis producing Pinot Noir of extraordinary delicacy, floral perfume, and silky texture from white limestone soils. Chambolle-Musigny contains two Grand Crus: Musigny (the most sought-after Pinot Noir Grand Cru in Burgundy alongside Romanée-Conti) and Bonnes Mares (shared with Morey-Saint-Denis, more powerful). The village's character — delicate red fruit, violet, rose petal, and mineral limestone — is instantly recognizable and universally loved. The finest Chambolle 1ers Crus (Les Amoureuses, Les Charmes) regularly fetch prices rivaling lesser Grand Crus.",
             key_producers="Domaine Jacques-Frédéric Mugnier, Domaine Roumier, Domaine Leroy, Comte de Vogüé, Domaine Drouhin, Anne Gros",
             historical_context="The village of Chambolle has a legendary association with love and femininity in wine literature — the 1ers Crus are named Les Amoureuses (The Lovers) and Les Charmes (The Charms). Alexandre Dumas père described Chambolle-Musigny as 'the most delicate wine in the world.' The Musigny Grand Cru produces only 5,000-6,000 bottles annually (at up to €2,000+ per bottle from DRC and Vogüé); Domaine Mugnier's Musigny is considered the appellation's definitive wine, combining power and delicacy in a way unique even within Burgundy.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Chambolle vintage; Pinot Noir from white limestone showed extraordinary floral delicacy and the characteristic violet-raspberry transparency of the finest village."),
    (2021, "exceptional", "rising", "Widely considered the finest Chambolle vintage of the century; wines of extraordinary aromatic complexity, mineral freshness, and 20+ year aging potential."),
    (2020, "excellent", "stable", "Benchmark year; Mugnier and Roumier both produced wines of outstanding quality; the vintage's heat produced more structured wines than typical but with good freshness."),
    (2019, "excellent", "stable", "Outstanding vintage; white limestone produced Chambolle of unusual depth and the characteristic violet-rose petal perfume; les Amoureuses received extraordinary attention."),
    (2018, "very_good", "stable", "Warm vintage; the limestone retained freshness; Chambolle-Musigny of generous red fruit and good silky texture; accessible earlier than cooler years."),
]:
    VIN(r_cha_m, yr, qd, pt, sn)

p_mug = P("Domaine Jacques-Frédéric Mugnier", "France", r_cha_m,
           description="Frédéric Mugnier's Chambolle-Musigny estate — considered the definitive address for the village's ethereal style. The Musigny Grand Cru (7 barrels), Les Amoureuses 1er Cru, and Chambolle-Musigny village wines all demonstrate the purest expression of the village's limestone-derived delicacy and floral perfume. Mugnier's Musigny is widely considered the most complete expression of what Pinot Noir Grand Cru can achieve in Burgundy.")
prod_mug, new = PROD("Domaine Mugnier Chambolle-Musigny Les Amoureuses Premier Cru", "wine_still", p_mug, r_cha_m, "France",
                     subcategory="Pinot Noir",
                     description="The most sought-after premier cru in Burgundy — Mugnier's Les Amoureuses from the parcel adjacent to Musigny Grand Cru, on white limestone of extraordinary purity. Translucent ruby, violet, raspberry, rose petal, chalk mineral, and a silky texture that develops over 15+ years into something of ineffable complexity. The wine that most clearly demonstrates why Chambolle-Musigny is called Burgundy's most feminine village.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mug, "Volaille de Bresse en demi-deuil (Bresse chicken with black truffle under skin, poached in broth)", "complement", "classic", "main", "The supreme expression of Burgundian luxury — Bresse chicken 'in mourning' (truffled) and Chambolle's most delicate 1er cru; the wine's violet and mineral depth bridges the truffle without overpowering the chicken's extraordinary flavour; the most refined of all Burgundy-food pairings")
    PAIR(prod_mug, "Carpaccio de Saint-Jacques (raw scallop carpaccio) with black truffle vinaigrette, sea salt, and micro herbs", "complement", "adventurous", "starter", "The ethereal wine and an equally ethereal starter — Chambolle's delicacy and floral mineral is one of the few reds that works with raw scallop; truffle bridges the wine's limestone mineral; the wine's silky texture mirrors the scallop's cream")

p_rou = P("Domaine Georges Roumier", "France", r_cha_m,
           description="Christophe Roumier's Chambolle-Musigny estate — producing wines across multiple appellation levels (village, 1er cru, Grand Cru Musigny and Charmes-Chambertin, Morey-Saint-Denis) that are universally considered among Burgundy's finest. The Les Amoureuses and Musigny are as eagerly anticipated as any wines in Burgundy; the village Chambolle-Musigny represents extraordinary quality at the 'accessible' end of Roumier's range.")
prod_rou, new = PROD("Domaine Georges Roumier Chambolle-Musigny Village", "wine_still", p_rou, r_cha_m, "France",
                     subcategory="Pinot Noir",
                     description="The benchmark for village-level Chambolle-Musigny from one of Burgundy's greatest producers — Roumier's village Pinot Noir from white limestone soils demonstrating the full aromatic expression of the village without premier cru price. Wild strawberry, violet, raspberry, chalk mineral, and the silky Chambolle texture. Approachable at 5 years but develops magnificently over 10-15. The finest entry point into understanding what Chambolle means.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_rou, "Suprême de pintade (guinea fowl supreme) with morels, cream, and vin jaune reduction", "complement", "classic", "main", "Burgundy's game bird and its most feminine village wine — guinea fowl's subtle gamey depth bridges the wine's delicacy; morels amplify the chalk mineral; vin jaune reduction adds an oxidative complexity that mirrors the wine's development")
    PAIR(prod_rou, "Époisses de Bourgogne (washed-rind) with walnuts and late-harvest Burgundy crackers", "complement", "adventurous", "cheese", "Burgundy's most pungent cheese and its most delicate wine — the contrast pairing that tests Chambolle's resilience; the wine's violet and mineral character is surprisingly resilient against Époisses's assertive washed-rind character; walnuts bridge the tannin")

# ── VOSNE-ROMANÉE AOC (FRANCE) ────────────────────────────────────
print("\n=== Vosne-Romanée AOC (France) ===")
r_vos = R("Vosne-Romanée", "France", "wine",
           designation_type="AOC",
           designation_name="Vosne-Romanée AOC",
           reputation_tier="iconic",
           quality_trajectory="established",
           description="Burgundy's most prestigious and valuable village — the red limestone and clay hillsides of Vosne-Romanée in the Côte de Nuits containing seven Grand Crus (Romanée-Conti, La Tâche, Richebourg, Romanée-Saint-Vivant, La Grande Rue, Romanée, La Grande Rue) that represent the pinnacle of Pinot Noir achievement worldwide. Domaine de la Romanée-Conti's monopoles (Romanée-Conti and La Tâche) regularly sell for $5,000-15,000+ per bottle at auction. The village wines and Premiers Crus (Les Suchots, Les Malconsorts, Aux Beaux Monts) provide the most accessible entry point to this extraordinary terroir.",
           key_producers="Domaine de la Romanée-Conti, Domaine Méo-Camuzet, Domaine Leroy, Anne Gros, Emmanuel Rouget, Domaine du Comte Liger-Belair",
           historical_context="The Romanée-Conti parcel (1.81 hectares, producing around 6,000 bottles annually) has been described as the world's most valuable agricultural land — a 2018 sale valued the estate at over $1 billion. The Prince of Conti purchased the monopole in 1760 over the objections of Madame de Pompadour (Louis XV's mistress), who had wanted it for herself — and renamed it from 'Romanée' to 'Romanée-Conti' to celebrate his victory. The domaine was confiscated during the Revolution and purchased by Duvault-Blochet in 1869; Aubert de Villaine's family purchased a share in 1942, and the co-director's leadership has defined the domaine's modern identity.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Vosne-Romanée vintage; Grand Cru Pinot Noir showed extraordinary mineral depth and the characteristic Vosne richness and spice complexity."),
    (2021, "exceptional", "rising", "Finest Vosne vintage of the century; wines of extraordinary aromatic complexity, mineral freshness, and the Vosne grand cru character that justifies the world's highest wine prices."),
    (2020, "excellent", "stable", "Benchmark year; DRC and Méo-Camuzet both produced Grand Crus of historic depth; the vintage's warmth produced an unusual richness within the typical Vosne precision."),
    (2019, "excellent", "stable", "Outstanding vintage; village and premier cru wines of exceptional concentration; Grand Crus destined for 25+ year development."),
    (2018, "very_good", "stable", "Warm vintage; generous Vosne of good concentration and the characteristic iron-spice mineral; accessible earlier than typical but still built for 15+ years."),
]:
    VIN(r_vos, yr, qd, pt, sn)

p_meo = P("Domaine Méo-Camuzet", "France", r_vos,
           description="Jean-Nicolas Méo's Vosne-Romanée estate — working with advice from Henri Jayer (the late legendary vigneron of Vosne-Romanée) to produce some of the village's most consistent and internationally celebrated wines. The Richebourg, Cros Parantoux (Henri Jayer's legendary premier cru), and Vosne-Romanée Les Brûlées and Aux Brûlées wines are among Burgundy's most sought-after.")
prod_meo, new = PROD("Domaine Méo-Camuzet Vosne-Romanée Premier Cru Les Brûlées", "wine_still", p_meo, r_vos, "France",
                     subcategory="Pinot Noir",
                     description="One of Vosne-Romanée's finest 1er crus from the late Henri Jayer's original mentor estate — Pinot Noir from the Les Brûlées parcel's red clay-limestone, with the characteristic iron-spice mineral of Vosne. Red cherry, raspberry, iron, violets, cedar, spice, and the magnificent depth that develops over 15-20 years. The entry point to Méo-Camuzet's extraordinary Vosne portfolio and one of the Côte de Nuits's finest premier crus.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_meo, "Canard sauvage rôti (roast wild duck) with Vosne-Romanée jus, cèpes, and braised cabbage", "complement", "classic", "main", "Wild duck and Vosne-Romanée — the wine's iron mineral and cherry bridges the wild duck's richness; cèpes' earth mirrors the wine's mineral depth; cabbage provides a savoury counterpoint to the fruit complexity")
    PAIR(prod_meo, "Filet de boeuf Rossini avec truffe noire du Périgord, foie gras poêlé, et pomme soufflée", "complement", "classic", "main", "The great French luxury preparation and Vosne's finest premier cru — the wine's iron-spice complexity bridges the truffle's depth; foie gras's richness meets the premier cru's mineral precision; pomme soufflée provides textural contrast")

p_gro = P("Anne Gros", "France", r_vos,
           description="Anne Gros's Vosne-Romanée estate — producing wines of consistent quality across village, premier cru, and Grand Cru Richebourg levels. The Richebourg Grand Cru is one of the appellation's most reliably excellent from this vine; the village Vosne-Romanée demonstrates the village character at an accessible entry point within the wider portfolio.")
prod_gro, new = PROD("Anne Gros Vosne-Romanée Village", "wine_still", p_gro, r_vos, "France",
                     subcategory="Pinot Noir",
                     description="Anne Gros's entry point to Vosne-Romanée — village Pinot Noir from the red clay-limestone soils demonstrating the characteristic iron-spice mineral complexity of this extraordinary village. Red cherry, raspberry, cinnamon, iron, violets, and the Vosne precision that distinguishes it from all neighbouring villages. Develops magnificently over 10+ years. The most accessible introduction to understanding why Vosne-Romanée commands such reverence.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_gro, "Lapin à la crème (rabbit in cream sauce) with whole grain mustard and tarragon", "complement", "classic", "main", "The Burgundy countryside's traditional preparation and its village wine — rabbit's delicacy allows Vosne's character to lead; cream bridges the wine's silky texture; tarragon mirrors the wine's herbal complexity; mustard bridges the iron mineral")
    PAIR(prod_gro, "Fromage de l'Ami du Chambertin (Gevrey monastery-style washed-rind) with walnut bread", "complement", "established", "cheese", "The Côte de Nuits cheese tradition and Vosne village wine — the washed-rind cheese's aromatic richness is bridged by the wine's iron mineral and cherry; walnut bread provides structural contrast; the wine's village-level approachability handles the cheese's intensity")

# ── PATRIMONIO AOC (CORSICA/FRANCE) ───────────────────────────────
print("\n=== Patrimonio AOC (France/Corsica) ===")
r_pat = R("Patrimonio", "France", "wine",
           designation_type="AOC",
           designation_name="Patrimonio AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Corsica's most prestigious and historically significant wine AOC — the limestone and schist hills north of Bastia in the Cap Corse peninsula producing wines from Nielluccio (Sangiovese — the variety was likely brought by Genoese colonists and represents over 95% of plantings in Patrimonio) and Vermentino (white). Patrimonio reds achieve a unique character: more aromatic and mineral than Tuscan Sangiovese, with a Mediterranean herb intensity and wild cherry quality that reflects the maquis-covered hillsides. The Grenache-dominant and Nielluccio rosés are also exceptional.",
           key_producers="Antoine Arena, Yves Leccia, Domaine Leccia, Domaine de Gioielli, Clos Marfisi",
           historical_context="Corsica was a Genoese colony from 1284 to 1768, when it was sold to France by the Genoese Republic (a year before Napoleon Bonaparte was born there). The Genoese brought Sangiovese cuttings from Tuscany, which developed over centuries into the Nielluccio biotype — now distinct enough from mainland Sangiovese to be considered a separate variety by some ampelographers. Antoine Arena's biodynamic estate at Morta Maio has been the catalyst for international recognition of Patrimonio — his minimal-intervention Nielluccio and Vermentino wines demonstrate the AOC's potential for serious, age-worthy wine. Patrimonio received AOC status in 1968 — the first Corsican appellation.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Patrimonio vintage; Nielluccio from limestone showed extraordinary aromatic intensity and the wild cherry-maquis herb character of the finest parcels."),
    (2021, "very_good", "stable", "Classic vintage; Mediterranean conditions produced wines of excellent freshness and the characteristic Corsican mineral-herb complexity that distinguishes Patrimonio."),
    (2020, "excellent", "stable", "Benchmark year; Antoine Arena and Yves Leccia both produced wines of international acclaim; Patrimonio's rediscovery by natural wine collectors accelerated."),
    (2019, "excellent", "rising", "Outstanding vintage; Nielluccio of extraordinary aromatic depth and longevity; the natural wine community's embrace of Corsican wines reached critical mass."),
    (2018, "very_good", "stable", "Warm Corsican vintage producing wines of good concentration; limestone retained freshness in the heat; Vermentino whites of excellent mineral intensity."),
]:
    VIN(r_pat, yr, qd, pt, sn)

p_are = P("Antoine Arena", "France", r_pat,
           description="The most celebrated and internationally recognized Patrimonio producer — Antoine Arena's biodynamic estate at Morta Maio produces Nielluccio and Vermentino of extraordinary purity and mineral depth that have introduced the world to Corsican wine's finest expression. His Carco and Morta Maio bottlings are allocated to collectors worldwide; his white Vermentino from limestone achieves a mineral complexity rivaling Burgundy. Arena's minimal-intervention approach and deep understanding of Corsican terroir makes him the island's defining wine personality.")
prod_are, new = PROD("Antoine Arena Patrimonio Rouge Carco", "wine_still", p_are, r_pat, "France",
                     subcategory="Nielluccio",
                     description="Corsica's most sought-after natural red wine — Antoine Arena's biodynamic Nielluccio (Sangiovese) from the limestone Carco parcel. Wild cherry, dried herbs (maquis: rosemary, thyme, cistus), iron mineral, violet, and the haunting Mediterranean depth that makes Patrimonio unlike any other Sangiovese-based wine. Develops magnificently over 8-10 years. The definitive expression of what Corsican Nielluccio can achieve in the right hands.",
                     price_tier="premium")
if new:
    PAIR(prod_are, "Veau Corse en daube (Corsican veal braised with olives, herbs, and rosé wine)", "complement", "classic", "main", "The island's traditional veal preparation and its natural Nielluccio — the wine's wild cherry and maquis herb character bridges the braised veal's Mediterranean depth; olives' bitterness mirrors the wine's mineral; rosé wine in the braise creates a lighter base that allows the Nielluccio to lead")
    PAIR(prod_are, "Fromage de brebis corse (Corsican sheep cheese) aged with maquis herbs, chestnut honey, and fig jam", "complement", "classic", "cheese", "The island's aged sheep cheese and its most celebrated red wine — Arena's wild cherry and maquis herb character bridges the brebis's rich sheep fat; chestnut honey mirrors the wine's sweetness; fig jam bridges the dark fruit; maquis herbs amplify the wine's herbal complexity")

p_lec = P("Yves Leccia", "France", r_pat,
           description="Yves Leccia's Patrimonio estate — producing wines across the full range of the appellation's styles: Nielluccio red, Vermentino white, and the appellation's excellent rosé from Nielluccio. Leccia's Orenga de Gaffory wines are among Patrimonio's most consistently excellent and internationally recognized, demonstrating the appellation's potential alongside Antoine Arena's more radical natural wine approach.")
prod_lec, new = PROD("Yves Leccia Patrimonio Blanc Vermentino", "wine_still", p_lec, r_pat, "France",
                     subcategory="Vermentino",
                     description="Corsica's benchmark Vermentino from the Patrimonio limestone — white peach, citrus blossom, almond, sea spray mineral, and the distinctive bitter almond finish that defines great Corsican Vermentino. More structured and mineral than Sardinian Vermentino; the limestone of Patrimonio adds a chalk depth unique on the island. Fresh and direct from vintage; develops hazelnut complexity over 3-5 years. The white wine that reveals Patrimonio's limestone character.",
                     price_tier="mid_range")
if new:
    PAIR(prod_lec, "Langoustes grillées (grilled rock lobster) from the Cap Corse with olive oil, lemon, and herbs", "complement", "classic", "main", "Corsica's prized Mediterranean crustacean and its limestone Vermentino — the wine's sea spray mineral and bitter almond bridges the rock lobster's oceanic sweetness; lemon mirrors the wine's citrus freshness; Corsican herbs bridge the almond finish")
    PAIR(prod_lec, "Figatellu grillé (Corsican liver and pork sausage) with chestnut polenta and maquis herbs", "complement", "classic", "aperitif", "Corsica's most traditional charcuterie and its white wine — Vermentino's bitter almond and mineral freshness is surprisingly effective against figatellu's liver richness; chestnut polenta provides starchy contrast; maquis herbs bridge the wine's herbal complexity")

# ── FINAL COUNT ──────────────────────────────────────────────────
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

cur.close()
conn.close()
print("\nDone.")
