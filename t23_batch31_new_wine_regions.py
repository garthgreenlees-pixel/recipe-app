#!/usr/bin/env python3
"""T23 Batch 31 — New wine regions: Swartland WO (South Africa), Minervois AOC (France), Jurançon AOC (France), Eden Valley GI (Australia), Walla Walla AVA (USA)"""

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

# ── SWARTLAND WO (SOUTH AFRICA) ───────────────────────────────────
print("\n=== Swartland WO (South Africa) ===")
r_swa = R("Swartland", "South Africa", "wine",
           designation_type="WO",
           designation_name="Swartland WO",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="South Africa's most exciting and internationally celebrated wine revolution — the granite, schist, and ancient Skurfberg shale hills north of Cape Town around the town of Malmesbury, producing Syrah, Grenache, Mourvèdre, and Chenin Blanc from dryland farmed old bush vines in the hot, dry Mediterranean climate. The Swartland Revolution (founded by Eben Sadie and others in 2010) declared war on irrigation, commercial yeast, new oak, and the Cape's established wine industry — producing wines of extraordinary terroir expression, mineral intensity, and soul. The movement transformed South Africa's international wine reputation from 'Pinotage and cheap Sauvignon Blanc' to one of the world's most exciting natural wine regions.",
           key_producers="Sadie Family Wines, Mullineux, Thorne & Daughters, Leeuwenkuil, Aaron Arendse, Donovan Rall",
           historical_context="The Swartland Revolution began in earnest in 2010 when Eben Sadie, Andrea and Chris Mullineux, and a group of like-minded producers held the first Swartland Revolution weekend — a manifesto-driven celebration of natural winemaking, terroir expression, and the rejection of the commercial Cape wine industry's homogenizing tendencies. The movement produced a manifesto: no irrigation, minimal intervention, indigenous yeasts, no recipes, and a commitment to expressing Swartland's unique ancient soils and hot Mediterranean climate. Within five years, Swartland Revolution wines had appeared on the lists of the world's finest restaurants and attracted collectors from 40 countries.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Swartland vintage; Syrah and Chenin Blanc from ancient granite showed extraordinary mineral intensity and the signature wild, fynbos-inflected complexity."),
    (2021, "very_good", "stable", "Classic vintage; dryland farming's stress conditions produced wines of excellent concentration and the characteristic Swartland iron-mineral freshness."),
    (2020, "excellent", "stable", "Benchmark year; Sadie Columella and Mullineux Iron Syrah both received extraordinary critical attention; South African natural wine confirmed globally."),
    (2019, "excellent", "rising", "Outstanding vintage; Chenin Blanc from ancient Skurfberg soils of exceptional mineral depth; Syrah of unusual freshness within the typical power."),
    (2018, "very_good", "stable", "Warm vintage by Swartland standards; dryland bush vine stress produced wines of good concentration and the characteristic fynbos herb complexity."),
]:
    VIN(r_swa, yr, qd, pt, sn)

p_sad = P("Sadie Family Wines", "South Africa", r_swa,
           description="Eben Sadie's Swartland estate — the producer who catalyzed the Swartland Revolution and South Africa's entire natural wine movement. The Columella (Syrah-dominant) and Palladius (Chenin Blanc-dominant white blend) are South Africa's most internationally acclaimed and sought-after wines; the single-vineyard 'Ouwingerdreeks' (Old Vine Series) wines have elevated Swartland's reputation to the level of the world's finest natural wine regions. Sadie's obsessive attention to ancient vine sites and minimal intervention has changed what South African wine means internationally.")
prod_sad, new = PROD("Sadie Family Wines Columella Swartland", "wine_still", p_sad, r_swa, "South Africa",
                     subcategory="Syrah",
                     description="South Africa's most internationally celebrated red wine — Eben Sadie's Columella from ancient granite and schist Swartland bush vines. Predominantly Syrah with Mourvèdre and other Rhône varieties: dark cherry, olive, fynbos herbs, iron mineral, smoked meat, and a haunting wildness that is unmistakably South African yet universally compelling. Develops magnificently over 15+ years. The wine that changed the world's perception of South Africa.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_sad, "Braai sosaties (Cape Malay-spiced lamb skewers) with apricot, cumin, and fenugreek", "complement", "classic", "main", "South Africa's braai tradition and its most celebrated Swartland Syrah — Columella's olive and wild herb character bridges the Cape Malay spice of the lamb; apricot mirrors the wine's dark fruit; iron mineral bridges the lamb's charred fat")
    PAIR(prod_sad, "Springbok loin (South African springbok) with wild rosemary jus and roasted rooibos carrots", "complement", "established", "main", "South Africa's iconic game and its finest Syrah — springbok's lean, mineral game character is bridged by Columella's wild herb and iron mineral; rooibos adds a distinctly South African bridge; wild rosemary mirrors the fynbos herb complexity")

p_mul = P("Mullineux", "South Africa", r_swa,
           description="Andrea and Chris Mullineux's Swartland estate — producing the most internationally celebrated Chenin Blanc (Kloof Street Old Vine White) and Syrah (Iron Syrah from the ironstone soils) in the Swartland Revolution. The Mullineux Single-Terroir series (Iron, Granite, Schist, Clay) demonstrates the profound influence of Swartland's different soils on Syrah's character — a Burgundian terroir concept applied to a Mediterranean hot-climate grape. Andrea Mullineux has been named Winemaker of the Year by multiple international publications.")
prod_mul, new = PROD("Mullineux Iron Syrah Swartland", "wine_still", p_mul, r_swa, "South Africa",
                     subcategory="Syrah",
                     description="The most internationally discussed single-terroir Syrah in South Africa — Mullineux's Syrah from the ironstone-rich soils of the Swartland granite hills. Iron mineral, dark cherry, smoked olive, fynbos herbs, violet, and a structural precision that distinguishes ironstone Syrah from the schist or granite expressions. Develops magnificently over 10+ years. The wine that introduced the concept of South African terroir specificity to international collectors.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_mul, "Karoo lamb cutlets on open coals with salt, thyme, and Cape brandy butter", "complement", "classic", "main", "The Karoo lamb and Swartland Syrah — the most authentically South African food-wine pairing; Columella's iron mineral and olive character bridges the lamb's herbed fat; Cape brandy butter bridges the wine's fynbos complexity")
    PAIR(prod_mul, "Bobotie (Cape Malay minced lamb with egg custard, dried fruit, and bay leaves) with yellow rice", "complement", "established", "main", "South Africa's national dish and its Swartland Syrah — the wine's olive and iron character provides an unusual but effective bridge to bobotie's sweet-savoury complexity; dried fruit mirrors the dark cherry; the wine's mineral cuts through the egg custard")

# ── MINERVOIS AOC (FRANCE) ────────────────────────────────────────
print("\n=== Minervois AOC (France) ===")
r_min = R("Minervois", "France", "wine",
           designation_type="AOC",
           designation_name="Minervois AOC",
           reputation_tier="respected",
           quality_trajectory="ascending",
           description="Languedoc's most historically significant and geologically diverse wine appellation — the semi-circular amphitheatre of hillsides north of the Canal du Midi in the Hérault and Aude departments, producing Grenache, Syrah, Mourvèdre, and Carignan blends of warming Mediterranean character from limestone, schist, and clay soils. The sub-zone La Livinière produces some of Languedoc's most concentrated and age-worthy reds. Minervois also produces Muscat de Saint-Jean-de-Minervois (the richest of all Languedoc Muscats) and small quantities of white Roussanne-Marsanne-Viognier blends of genuine quality.",
           key_producers="Clos Centeilles, Château Canet, Domaine de l'Hortus, Château Villerambert-Julien, Château Maris",
           historical_context="The Minervois takes its name from the Cathar fortress of Minerve — where in 1210, during the Albigensian Crusade, 180 Cathar perfecti were burned alive by Simon de Montfort's crusaders who offered them the option of conversion or death. Wine has been produced here continuously since Phoenician traders brought viticulture to Narbonne in the 6th century BC. The Canal du Midi — built between 1666-1681 by Pierre-Paul Riquet under Louis XIV — brought commercial wine distribution to the region, allowing Minervois wine to reach markets throughout France and beyond. La Livinière's separate sub-appellation status (2000) recognized the highest-altitude limestone plateau's superior wines.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Minervois vintage; Grenache and Syrah from La Livinière limestone showed extraordinary dark fruit concentration and Mediterranean herb complexity."),
    (2021, "very_good", "stable", "Classic vintage; the limestone amphitheatre produced wines of excellent freshness; Carignan from old vines of particular aromatic interest."),
    (2020, "excellent", "stable", "Benchmark year; La Livinière sub-zone wines of exceptional concentration and longevity; international critics' rediscovery of serious Languedoc Minervois."),
    (2019, "excellent", "rising", "Outstanding vintage; Grenache-Syrah blends of extraordinary garrigue herb complexity and dark fruit intensity; Minervois's reputation continues to rise."),
    (2018, "very_good", "stable", "Warm vintage producing generous Minervois of good concentration; Mediterranean conditions ideal for Grenache's natural richness."),
]:
    VIN(r_min, yr, qd, pt, sn)

p_cen = P("Clos Centeilles", "France", r_min,
           description="Patricia Domergue's biodynamic La Livinière estate — the most critically acclaimed and internationally recognized Minervois producer. The Clos Centeilles and Campagne de Centeilles wines from the limestone plateau demonstrate that Languedoc can produce wines of genuine complexity and mineral depth. Patricia's philosophy of working with the full Languedoc palette of varieties (including rare Picpoul Noir and Oeillade) has created a distinctive regional identity unique in the appellation.")
prod_cen, new = PROD("Clos Centeilles La Livinière Minervois", "wine_still", p_cen, r_min, "France",
                     subcategory="Syrah",
                     description="The benchmark for La Livinière's highest-altitude limestone plateau — Patricia Domergue's biodynamic Syrah and Grenache from the sub-zone's finest limestone parcels. Dark cherry, olive, wild herbs (garrigue: thyme, rosemary, cistus), iron mineral, and a Languedoc character that rivals the southern Rhône's finest villages. Develops magnificently over 8-10 years. The definitive expression of what La Livinière limestone can achieve.",
                     price_tier="mid_range")
if new:
    PAIR(prod_cen, "Cassoulet de Carcassonne (Languedoc cassoulet with duck confit, Toulouse sausage, and white beans)", "complement", "classic", "main", "The Languedoc's most iconic dish and its finest red — Minervois's herb complexity and dark fruit bridges the cassoulet's accumulated richness; duck confit's fat is matched by the wine's structure; white beans soften the garrigue herb intensity")
    PAIR(prod_cen, "Daurade royale rôtie avec tapenade, tomates confites et herbes de Provence", "complement", "established", "main", "The Mediterranean fish roasted with the region's aromatic landscape — Minervois's garrigue herb character bridges the sea bream's Mediterranean character; tapenade's olive mirrors the wine's olive note; tomato's acidity contrasts the dark fruit")

p_can_m = P("Château Canet", "France", r_min,
             description="The Duran family's Minervois estate — producing consistently excellent Grenache-Syrah-Mourvèdre blends from the varied soils of the Minervois AOC. Château Canet's wines represent the benchmark for traditional-style Minervois: concentrated, herbal, and food-friendly with the characteristic Languedoc warmth and garrigue complexity that makes this appellation one of France's most versatile red wine regions.")
prod_can_m, new = PROD("Château Canet Minervois Rouge", "wine_still", p_can_m, r_min, "France",
                        subcategory="Grenache",
                        description="The approachable face of serious Minervois — Grenache, Syrah, and Mourvèdre from varied Minervois limestone and clay, aged in old oak. Dark cherry, blackberry, thyme, rosemary, leather, and the warming Languedoc generosity that makes Minervois one of France's most food-friendly AOCs. Accessible from release; develops over 5-7 years. The reliable everyday-luxury Languedoc red.",
                        price_tier="mid_range")
if new:
    PAIR(prod_can_m, "Agneau de l'Aveyron aux herbes (Aveyron mountain lamb with garlic and Languedoc herbs)", "complement", "classic", "main", "Mediterranean lamb and the Mediterranean red — Minervois's garrigue herb character mirrors the lamb's herb coating; the wine's dark cherry bridges the lamb's richness; the regional synergy of herb-herb and fruit-fat is Languedoc at its most direct")
    PAIR(prod_can_m, "Ratatouille niçoise with grilled magret de canard and balsamic reduction", "complement", "classic", "main", "Provence's vegetable masterpiece and Languedoc's warming red — the wine's garrigue herbs mirror the ratatouille's aromatic complexity; duck breast's rich fat is matched by the wine's Grenache warmth; balsamic bridges the dark fruit")

# ── JURANÇON AOC (FRANCE) ─────────────────────────────────────────
print("\n=== Jurançon AOC (France) ===")
r_jur = R("Jurançon", "France", "wine",
           designation_type="AOC",
           designation_name="Jurançon AOC",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="Southwest France's most distinctive and internationally celebrated dessert wine AOC — the steep hillsides of the Pyrenean foothills south of Pau producing both dry Jurançon Sec and sweet Jurançon Moelleux and Vendange Tardive from Petit Manseng (primarily) and Gros Manseng. The late autumn foehn winds that dry the grapes on the vine (passerillage) concentrate the sugars without botrytis, creating wines of extraordinary freshness and citrus intensity alongside the sweetness. The finest Jurançon Moelleux — particularly from Clos Uroulat and Domaine Cauhapé — age 20-40 years, developing extraordinary complexity.",
           key_producers="Clos Uroulat (Charles Hours), Domaine Cauhapé, Domaine de Souch, Clos Lapeyre, Cave de Gan",
           historical_context="Henri IV — King of France and most beloved Gascon — was baptized with a few drops of Jurançon wine when he was born in Pau in 1553, and the wine has been associated with French royalty ever since. The appellation's unusual vinification method — allowing the grapes to passeriller (raisin on the vine) in the autumn mountain winds rather than using botrytis — creates the distinctive combination of sweetness and freshness unique to Jurançon. Colette described tasting Jurançon for the first time as 'an imperious and treacherous little wine, perfumed as a rose, full of pride and treachery.' Charles Hours of Clos Uroulat began producing the appellation's most serious and internationally recognized wines in the 1980s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Jurançon vintage; Petit Manseng concentrated beautifully in the mountain foehn; moelleux wines of extraordinary citrus-honey sweetness and mineral tension."),
    (2021, "very_good", "stable", "Classic vintage; Pyrenean conditions produced wines of excellent natural acidity and the characteristic Jurançon combination of sweetness and mountain freshness."),
    (2020, "excellent", "stable", "Benchmark year; Clos Uroulat and Cauhapé both produced moelleux of extraordinary depth; Vendange Tardive wines of exceptional concentration and longevity."),
    (2019, "exceptional", "rising", "Greatest Jurançon vintage of the era; passerillage was perfect; moelleux wines of legendary citrus-honey sweetness and 30+ year aging potential."),
    (2018, "excellent", "stable", "Excellent vintage for dry and sweet Jurançon; foehn winds consistent; Petit Manseng of exceptional concentration and tropical complexity."),
]:
    VIN(r_jur, yr, qd, pt, sn)

p_hou = P("Clos Uroulat", "France", r_jur,
           description="Charles Hours's Jurançon estate — producing the appellation's most internationally acclaimed and consistently excellent wines in both dry and sweet styles. The Cuvée Marie (moelleux) and the dry Clos Uroulat are considered the definitive expressions of Petit Manseng's capacity for complexity and longevity. Hours's obsessive attention to passerillage conditions and minimal cellar intervention has made Clos Uroulat the reference address for serious Jurançon.")
prod_hou, new = PROD("Clos Uroulat Cuvée Marie Jurançon Moelleux", "wine_still", p_hou, r_jur, "France",
                     subcategory="Petit Manseng",
                     description="The appellation's benchmark moelleux — Charles Hours's Petit Manseng concentrated by mountain foehn without botrytis, fermented with indigenous yeasts and aged in old oak. Extraordinary freshness within great sweetness: candied citrus, mango, quince, honey, pineapple, ginger, and the characteristic Jurançon mineral tension from the Pyrenean clay-sandstone soils. Develops magnificently over 15-30 years. France's most original and underrated sweet wine.",
                     price_tier="premium")
if new:
    PAIR(prod_hou, "Foie gras de canard mi-cuit with Jurançon moelleux gelée, toasted brioche, and pain d'épices", "complement", "classic", "starter", "Southwest France's luxury production and its most sophisticated wine — the wine appears in the gelée; Jurançon's citrus-honey sweetness is perfectly balanced by foie gras's richness; pain d'épices bridges the ginger note; the circular Gascon pairing")
    PAIR(prod_hou, "Roquefort with Jurançon poached pears, walnut bread, and bitter orange marmalade", "complement", "classic", "cheese", "Jurançon's sweet-acid tension against Roquefort's salt — the wine's citrus freshness contrasts the blue cheese's intensity; pears bridge the sweet wine; walnut bread bridges the wine's mineral depth; marmalade mirrors the citrus character")

p_cau = P("Domaine Cauhapé", "France", r_jur,
           description="Henri Ramonteu's Jurançon estate — producing the widest and most internationally distributed range of Jurançon wines from dry to late-harvest sweet. The Symphonie de Novembre (Vendange Tardive) from the latest-harvested, most concentrated Petit Manseng is one of France's greatest sweet wines; the dry Ballet d'Octobre demonstrates that Gros Manseng can produce serious, complex dry wine alongside Petit Manseng's sweetness.")
prod_cau, new = PROD("Domaine Cauhapé Ballet d'Octobre Jurançon Sec", "wine_still", p_cau, r_jur, "France",
                     subcategory="Gros Manseng",
                     description="Southwest France's most distinctive dry white — Henri Ramonteu's Gros Manseng from Pyrenean clay-sandstone, late-harvested for maximum concentration but fermented to dryness. Citrus blossom, grapefruit pith, tropical fruit, white pepper, mountain mineral, and a structure that develops over 5-8 years. The wine that demonstrates that Jurançon Sec can rival serious white wines from anywhere in France. Individual and irreplaceable.",
                     price_tier="mid_range")
if new:
    PAIR(prod_cau, "Palombe rôtie (Pyrenean wood pigeon) with cèpes, chestnuts, and Armagnac jus", "complement", "classic", "main", "The Pyrenees's autumnal tradition and its dry Jurançon wine — the wine's grapefruit and mountain mineral bridges the palombe's rich, gamey character; cèpes' earthy depth mirrors the wine's mineral complexity; Armagnac bridges the wine's regional identity")
    PAIR(prod_cau, "Axoa d'Espalette (Basque veal and Espelette pepper stew) with corn bread", "complement", "classic", "main", "The Basque-Pyrenean tradition and its Gascon white — Jurançon Sec's citrus and white pepper character bridges the Espelette pepper's gentle heat; veal's delicacy allows the wine's complexity to lead; corn bread provides a neutral base")

# ── EDEN VALLEY GI (AUSTRALIA) ────────────────────────────────────
print("\n=== Eden Valley GI (Australia) ===")
r_ede = R("Eden Valley", "Australia", "wine",
           designation_type="GI",
           designation_name="Eden Valley GI",
           reputation_tier="prestigious",
           quality_trajectory="established",
           description="South Australia's most celebrated cool-climate wine GI — the elevated plateau (400-500m) east of the Barossa Valley floor, producing Australia's finest Riesling and some of its most elegant Shiraz and Viognier from the ancient, highly weathered Precambrian granite and loamy soils. Eden Valley's altitude and its exposure to cool Adelaide Hills breezes creates conditions that allow Riesling to ripen with natural acidity and citrus-lime precision entirely different from the warmer Barossa floor. The sub-zone of High Eden (above 400m) is recognized for the highest elevation and most mineral Riesling expressions. Henschke's Hill of Grace Shiraz — from 150-year-old 'Eden' vines on Eden Valley soils — is Australia's most famous and expensive wine.",
           key_producers="Henschke, Pewsey Vale, Eden Hall, Penfolds (Eden Valley component), Yalumba (The Virgilius Viognier)",
           historical_context="The Eden Valley's wine history begins with Johann Gramp's planting of Riesling at Jacob's Creek in 1847 — establishing the variety's foundational position in Australian wine. The Eden Valley Riesling style — austere, lime-scented, mineral, with extraordinary 20+ year aging potential — became Australia's premier cool-climate white wine identity. Cyril Henschke's planting of the Hill of Grace Shiraz vineyard in 1860 from cuttings of unknown origin created what would become Australia's most iconic single-vineyard wine. The Hill of Grace vine block — named after the local Lutheran church — remained unrecognized for a century before Prue Henschke's winemaking genius elevated it to global fame in the 1990s.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Eden Valley vintage; Riesling from granite soils showed extraordinary lime-citrus precision and the mineral freshness that defines this cooler plateau."),
    (2021, "very_good", "stable", "Classic vintage; cool conditions from altitude and Adelaide Hills breezes produced Riesling of excellent natural acidity and long-term aging potential."),
    (2020, "excellent", "stable", "Benchmark year; Henschke Hill of Grace and Pewsey Vale Riesling both produced wines of extraordinary depth; Eden Valley's cool-climate credentials confirmed."),
    (2019, "excellent", "rising", "Outstanding vintage; Riesling of exceptional lime-mineral complexity; Shiraz from old Eden vines of unusual freshness alongside expected depth."),
    (2018, "very_good", "stable", "Warm vintage by Eden Valley standards; altitude maintained freshness; Riesling of good concentration; Shiraz of unusual richness from the warm season."),
]:
    VIN(r_ede, yr, qd, pt, sn)

p_hen = P("Henschke", "Australia", r_ede,
           description="The Henschke family's Eden Valley estate — producing Australia's most famous wine (Hill of Grace Shiraz from 150+ year old vines) and the acclaimed Mount Edelstone Shiraz alongside exceptional Eden Valley Riesling. Prue Henschke's winemaking and Stephen Henschke's viticulture have elevated the estate to international cult status; Hill of Grace is now Australia's most expensive and sought-after wine, comparable in price and prestige to the finest Barossa Shiraz from Penfolds Grange.")
prod_hen, new = PROD("Henschke Cyril Henschke Eden Valley Cabernet Sauvignon", "wine_still", p_hen, r_ede, "Australia",
                     subcategory="Cabernet Sauvignon",
                     description="Henschke's cooler-climate Cabernet Sauvignon from Eden Valley granite — named for the patriarch Cyril Henschke who planted the vineyard. Blackcurrant, cedar, dried herb, graphite, and the cool-climate precision that distinguishes Eden Valley Cabernet from the warmer Coonawarra or Barossa styles. Develops magnificently over 15+ years. One of Australia's most underrated fine Cabernets.",
                     price_tier="premium")
if new:
    PAIR(prod_hen, "Roast rack of Kangaroo Island lamb with native herb crust and warrigal greens", "complement", "classic", "main", "South Australia's finest lamb and its Eden Valley Cabernet — the wine's graphite and black fruit bridges the lamb's herb crust; warrigal greens provide a distinctly Australian vegetable bridge")
    PAIR(prod_hen, "Wagyu beef (Australian full-blood, MB9+) seared with native pepper berry, saltbush, and wattle seed jus", "complement", "classic", "main", "The premium Australian beef and Eden Valley's finest Cabernet — the wine's structure and dark fruit handles the wagyu's extraordinary marbling; native pepper berry bridges the wine's herbal complexity; saltbush mirrors the wine's mineral precision")

p_pew = P("Pewsey Vale", "Australia", r_ede,
           description="Yalumba's Eden Valley Riesling estate — producing one of Australia's most consistent and internationally distributed Rieslings from the high Eden Valley granite soils. The Pewsey Vale Contours (Museum Reserve) and the regular Prima Riesling demonstrate the extraordinary aging potential of Eden Valley's lime-mineral style; the Contours at 10 years shows the kerosene-petrol development characteristic of great aged Riesling.")
prod_pew, new = PROD("Pewsey Vale The Contours Eden Valley Riesling", "wine_still", p_pew, r_ede, "Australia",
                     subcategory="Riesling",
                     description="Australia's most celebrated Museum Reserve Riesling — Eden Valley Riesling released after 5+ years of cellar aging, showing the development that makes Australian Riesling so compelling. Lime oil, lime curd, petrol, slate, toasted almond, and the extraordinary mineral precision that develops over time. At peak (8-15 years) rivals the finest Mosel Spätlese for mineral complexity and character. The wine that demonstrates Australian Riesling's world-class aging potential.",
                     price_tier="mid_range")
if new:
    PAIR(prod_pew, "Barramundi with lime, finger lime caviar, coconut cream, and lemongrass", "complement", "classic", "main", "Australia's most beloved fish and Eden Valley's lime-mineral Riesling — the wine's lime curd and petrol development bridges the barramundi's delicate flesh; finger lime caviar amplifies the citrus intensity; lemongrass bridges the wine's aromatic complexity")
    PAIR(prod_pew, "Szechuan-spiced ocean trout with pickled cucumber and sesame dressing", "complement", "classic", "main", "The modern Australian multicultural kitchen and its Riesling — the wine's lime-petrol character bridges the Szechuan spice's complexity; pickled cucumber mirrors the wine's acidity; sesame provides a nutty bridge to the mineral slate")

# ── WALLA WALLA AVA (USA) ─────────────────────────────────────────
print("\n=== Walla Walla AVA (USA) ===")
r_wal = R("Walla Walla Valley", "USA", "wine",
           designation_type="AVA",
           designation_name="Walla Walla Valley AVA",
           reputation_tier="prestigious",
           quality_trajectory="ascending",
           description="Washington State's most prestigious and historically important wine AVA — the plateau and rolling hills of southeastern Washington and northeastern Oregon around the city of Walla Walla, producing Cabernet Sauvignon, Merlot, Syrah, and red Rhône blends from cobblestone and basalt volcanic soils in a semi-arid continental climate with dramatic diurnal temperature variation. Walla Walla's combination of daytime heat, cool nights, and concentrated growing season creates wines of intense dark fruit, mineral depth, and a distinctly Pacific Northwest character. The AVA also extends into Oregon's Seven Hills and Rocks District, where basalt soils produce extraordinary Merlot and Rhône varieties.",
           key_producers="Leonetti Cellar, Cayuse Vineyards, L'Ecole No 41, Woodward Canyon, DeLille Cellars, Dunham Cellars",
           historical_context="Walla Walla's wine industry was founded by Gary Figgins of Leonetti Cellar in 1977 — initially producing wine in his garage from grapes he purchased from Sagemoor Farms on the Columbia River. His 1978 Leonetti Merlot was rated the finest in the country by Wine Spectator, creating the first major American wine from Washington. Christophe Baron of Cayuse Vineyards discovered the cobblestone-covered Rocks District in 1997 and immediately recognized the similarity to Châteauneuf-du-Pape's galets roulés, planting Syrah and other Rhône varieties in what became Washington's most distinctive sub-appellation.")

for yr, qd, pt, sn in [
    (2022, "excellent", "rising", "Outstanding Walla Walla vintage; Cabernet Sauvignon and Syrah from cobblestone soils showed extraordinary concentration and the characteristic Walla Walla iron-mineral depth."),
    (2021, "excellent", "stable", "Benchmark year; the semi-arid plateau produced wines of excellent dark fruit concentration and the characteristic cooling diurnal variation that distinguishes Washington State Cabernet."),
    (2020, "very_good", "stable", "Classic vintage; some smoke impact from regional wildfires but the finest producers made elegant wines of good structure and dark fruit depth."),
    (2019, "exceptional", "rising", "Greatest Walla Walla vintage of the era; cobblestone and basalt Syrah of historic mineral intensity; Cayuse and Leonetti both produced wines of 20+ year potential."),
    (2018, "excellent", "stable", "Warm vintage producing Walla Walla reds of excellent concentration; diurnal variation maintained freshness; Merlot of unusual richness from the warm season."),
]:
    VIN(r_wal, yr, qd, pt, sn)

p_leo = P("Leonetti Cellar", "USA", r_wal,
           description="Gary and Nancy Figgins's Walla Walla founding estate — the winery that created Washington State's fine wine identity with Gary's 1978 garage Merlot rated America's finest. The Leonetti Cellar Cabernet Sauvignon and Reserve are among the Pacific Northwest's most allocated and sought-after wines. Gary's son Chris continues the tradition with equal obsession and his own mark on Washington's most historic winery.")
prod_leo, new = PROD("Leonetti Cellar Reserve Walla Walla Valley Cabernet Sauvignon", "wine_still", p_leo, r_wal, "USA",
                     subcategory="Cabernet Sauvignon",
                     description="Washington State's most historically significant wine — Leonetti's Reserve Cabernet Sauvignon from the Walla Walla cobblestone and basalt plateau. Blackcurrant, cedar, iron mineral, dark chocolate, tobacco, and the distinct continental dryness of Washington's semi-arid inland climate. Develops magnificently over 15-20 years. The wine that proved Washington State's Cabernet could rival Napa and Bordeaux.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_leo, "Grilled Walla Walla sweet onion (the region's famous onion) stuffed with Washington State blue cheese and herbs", "complement", "classic", "aperitif", "The AVA's most famous agricultural product and its founding wine — Walla Walla sweet onion's caramelized sweetness is bridged by the Cabernet's dark fruit; blue cheese's richness mirrors the wine's depth; herbs bridge the cedar complexity")
    PAIR(prod_leo, "Elk tenderloin (Pacific Northwest elk) with wild huckleberry jus and root vegetable gratin", "complement", "classic", "main", "The Pacific Northwest's iconic game and Washington's finest Cabernet — elk's lean mineral game character is bridged by Leonetti's iron mineral and dark fruit; huckleberry mirrors the wine's dark berry character; root vegetable gratin provides starchy richness")

p_cay = P("Cayuse Vineyards", "USA", r_wal,
           description="Christophe Baron's Rocks District estate — the French winemaker who discovered the cobblestone-covered basalt soils of the Rocks District in 1997 and recognized their similarity to Châteauneuf-du-Pape, planting Syrah, Grenache, Tempranillo, and Viognier. The Cailloux (Stones) Syrah from pure cobblestone soils is considered Washington State's most extraordinary terroir wine and one of the world's finest Syrahs — consistently receiving the state's highest critical scores.")
prod_cay, new = PROD("Cayuse Cailloux Vineyard Syrah Walla Walla Valley", "wine_still", p_cay, r_wal, "USA",
                     subcategory="Syrah",
                     description="Washington State's most distinctive terroir wine — Christophe Baron's Syrah from the ancient cobblestone basalt soils of the Rocks District, immediately reminiscent of Châteauneuf-du-Pape's galets roulés. Dark cherry, olive, iron, smoked meat, violet, and the extraordinary mineral depth imparted by the cobblestone soils. Biodynamically farmed; develops magnificently over 12-15 years. The wine that proves Washington can produce world-class Syrah.",
                     price_tier="ultra_premium")
if new:
    PAIR(prod_cay, "Pacific Northwest Columbia River king salmon with black olive tapenade and fennel-citrus salad", "complement", "established", "main", "The Pacific Northwest's finest fish and its most distinctive Syrah — the wine's olive and iron mineral character surprisingly bridges the king salmon's rich oil; tapenade amplifies the olive note; fennel mirrors the wine's herbal complexity; the adventurous red-with-salmon pairing")
    PAIR(prod_cay, "Walla Walla Valley dry-aged beef ribeye (28 days) with compound butter, watercress, and bone marrow", "complement", "classic", "main", "The age-old beef-Syrah pairing adapted for Washington's most mineral expression — the cobblestone mineral and dark cherry bridges the dry-aged beef's concentrated umami; bone marrow adds fatty richness that the wine's structure supports; watercress contrasts with bitter freshness")

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
