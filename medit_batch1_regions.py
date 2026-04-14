#!/usr/bin/env python3
"""Mediterranean Session — Batch 1: European Beverage Regions
Inserts all parent + child regions for France, Italy, Spain, Greece, Lebanon, Morocco, Turkey.
Uses actual beverage_regions schema.
"""
import psycopg2, re

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

def R(name, country, beverage_family, parent_id=None, description=None,
      reputation_tier=None, quality_trajectory='established',
      key_producers=None, historical_context=None, authority_tier=1):
    slug = slugify(name)
    cur.execute("""
        INSERT INTO beverage_regions
          (name, slug, country, beverage_family, parent_region_id, description,
           reputation_tier, quality_trajectory, key_producers, historical_context,
           authority_tier, is_published)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,TRUE)
        ON CONFLICT DO NOTHING RETURNING id
    """, (name, slug, country, beverage_family, parent_id, description,
          reputation_tier, quality_trajectory, key_producers, historical_context, authority_tier))
    row = cur.fetchone()
    if row:
        print(f"  ✓ {name} (id={row[0]})")
        return row[0]
    cur.execute("SELECT id FROM beverage_regions WHERE slug=%s", (slug,))
    row = cur.fetchone()
    if row:
        print(f"  ~ {name} exists (id={row[0]})")
        return row[0]
    return None

# ─── FRANCE — BURGUNDY ────────────────────────────────────────────────────────
print("=== FRANCE — BURGUNDY ===")
burgundy = R("Burgundy", "France", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine de la Romanée-Conti, Domaine Leroy, Domaine Rousseau, Domaine Roumier, Domaine Leflaive, Domaine Coche-Dury, Domaine Roulot, Maison Louis Jadot, Maison Drouhin",
    description="France's most celebrated wine region. Home to Pinot Noir and Chardonnay in their most complex, terroir-transparent expressions. The classification system — Grand Cru, Premier Cru, Village, Régionale — is the definitive model of site hierarchy. Fragmented ownership (80+ owners of Clos de Vougeot alone) creates enormous producer-dependent quality variation.",
    historical_context="Cistercian monks of Cîteaux codified Burgundy's vineyard hierarchy from the 11th century. The Confrérie des Chevaliers du Tastevin, founded 1934, perpetuates the tradition. The Hospices de Beaune charity auction (third Sunday of November) sets international price benchmarks annually.")

cote_nuits = R("Côte de Nuits", "France", "wine", parent_id=burgundy,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine de la Romanée-Conti, Domaine Leroy, Domaine Rousseau, Domaine Roumier, Domaine Mugnier, Domaine Dujac",
    description="Northern half of the Côte d'Or, 20km from Marsannay to Corgoloin. Almost entirely Pinot Noir. Home to the greatest concentration of Grand Cru vineyards: Chambertin, Musigny, Clos de Vougeot, Richebourg, La Romanée-Conti. The global benchmark for age-worthy, terroir-transparent red wine.")

R("Gevrey-Chambertin", "France", "wine", parent_id=cote_nuits,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine Rousseau, Domaine Dujac, Domaine Drouhin-Laroze, Rossignol-Trapet",
    description="Largest Côte de Nuits appellation, home to nine Grand Crus including Chambertin and Chambertin Clos de Bèze. Napoleon reportedly drank only Chambertin. Full-bodied for Pinot Noir — structured, earthily powerful, capable of 30-year cellaring. BC importer for Rousseau: Lifford Wine Agency [NEEDS VERIFICATION].",
    historical_context="Chambertin named after a local peasant Bertin whose field (champ) adjoined the Abbey of Bèze vineyard. The name 'Chambertin' means literally 'Bertin's field.'")

R("Morey-Saint-Denis", "France", "wine", parent_id=cote_nuits,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine Dujac, Domaine Ponsot, Clos de Tart (Mommessin)",
    description="Five Grand Crus: Clos de la Roche, Clos Saint-Denis, Clos des Lambrays, Clos de Tart (Mommessin monopole), Bonnes Mares (partial). More muscular and mineral than neighbours. Dujac is the reference estate — elegant, Burgundy at its most textured. BC importer for Dujac: Classic Wine Imports [NEEDS VERIFICATION].")

R("Chambolle-Musigny", "France", "wine", parent_id=cote_nuits,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine Roumier, Domaine Mugnier, Maison Drouhin",
    description="The most elegant Côte de Nuits appellation. Grand Crus: Musigny (silky, ethereal — Pinot Noir at its most celestial), Bonnes Mares (shared with Morey). Premier Cru Les Amoureuses fetches Grand Cru prices. Roumier's Musigny is one of the five greatest Burgundies made. BC importer: Skye Import / Lifford [NEEDS VERIFICATION].")

R("Vougeot", "France", "wine", parent_id=cote_nuits,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Méo-Camuzet, Leroy, Domaine de la Vougeraie (upper-slope parcels)",
    description="Dominated by the 50-hectare Clos de Vougeot — over 80 different owners, wildly inconsistent quality. Best parcels are in the upper third of the slope. Established by Cistercian monks in the 14th century; the château is headquarters of the Confrérie des Chevaliers du Tastevin.",
    historical_context="The Cistercians of Cîteaux completed the stone wall enclosing Clos de Vougeot in the 14th century. 'Clos' means walled vineyard.")

R("Vosne-Romanée", "France", "wine", parent_id=cote_nuits,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine de la Romanée-Conti, Domaine Leroy, Méo-Camuzet, Domaine du Comte Liger-Belair",
    description="The most prestigious village in Burgundy. Six Grand Crus: La Romanée-Conti (DRC monopole), La Tâche (DRC monopole), Richebourg, Romanée-Saint-Vivant, Échézeaux, Grands Échézeaux. DRC La Romanée-Conti is the world's most expensive wine by the bottle. BC importer for DRC: by allocation through BCLDB special order [NEEDS VERIFICATION].")

R("Nuits-Saint-Georges", "France", "wine", parent_id=cote_nuits,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine Henri Gouges, Domaine Faiveley, Domaine Robert Chevillon",
    description="Commercial capital of the Côte de Nuits. No Grand Crus but many excellent Premier Crus. Structured, earthy, meaty Pinot Noir — slower to open than northern neighbours. Henri Gouges is the benchmark domaine. The négociant tradition (Faiveley, Moillard) is centred here.")

cote_beaune = R("Côte de Beaune", "France", "wine", parent_id=burgundy,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine Leflaive, Domaine Coche-Dury, Domaine Roulot, Domaine Comtes Lafon, Bonneau du Martray",
    description="Southern Côte d'Or. Home to Burgundy's greatest whites: Corton-Charlemagne, Meursault, Puligny-Montrachet, Chassagne-Montrachet. Beaune is the commercial capital. Also produces excellent reds in Pommard and Volnay.")

R("Aloxe-Corton", "France", "wine", parent_id=cote_beaune,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Bonneau du Martray, Domaine Michel Juillot, Louis Latour",
    description="Northernmost Côte de Beaune appellation. The Corton hill: red Grand Cru Corton (the Côte de Beaune's only red Grand Cru), white Grand Cru Corton-Charlemagne (shared with Pernand-Vergelesses and Ladoix). Bonneau du Martray holds the largest single Corton-Charlemagne plot.")

R("Beaune", "France", "wine", parent_id=cote_beaune,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Maison Joseph Drouhin, Maison Louis Jadot, Domaine Bouchard Père et Fils",
    description="Administrative and commercial heart of Burgundy. No Grand Crus but 36 Premier Crus. The Hospices de Beaune annual charity auction (third Sunday of November) sets international price benchmarks. Major négociant houses — Drouhin, Jadot, Bouchard — are based here.",
    historical_context="The Hôtel-Dieu (Hospices de Beaune) was founded in 1443 by Nicolas Rolin. Its annual wine auction has been held since 1859 and remains a global barometer of Burgundy prices.")

R("Pommard", "France", "wine", parent_id=cote_beaune,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine du Comte Armand, Domaine Lejeune, Domaine Michel Gaunoux",
    description="Most structured Côte de Beaune red. No Grand Crus but Premier Crus Les Rugiens and Clos des Épeneaux (Comte Armand monopole) are exceptional. Iron-rich clay soils produce dense, powerful Pinot Noir that outlasts many Côte de Nuits wines in the cellar.")

R("Volnay", "France", "wine", parent_id=cote_beaune,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine de la Pousse d'Or, Marquis d'Angerville, Domaine Michel Lafarge",
    description="Most elegant Côte de Beaune red — the feminine counterpart to Pommard. Limestone soils produce silky, aromatic, medium-weight Pinot Noir. Premier Crus Caillerets, Champans, Clos des Chênes. Marquis d'Angerville is the historic benchmark family estate.")

R("Meursault", "France", "wine", parent_id=cote_beaune,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine Coche-Dury, Domaine Roulot, Domaine Comtes Lafon, Domaine Pierre Morey",
    description="Burgundy's capital of white wine — the most commercially important Chardonnay appellation on earth. No Grand Crus (a historic anomaly given the quality) but Premier Crus Perrières, Charmes, Genevrières are world-class. Famous for the Paulée de Meursault lunch — the greatest harvest celebration in Burgundy. BC importer for Coche-Dury: ultra-allocated, primarily through Cas-Dri Pacific [NEEDS VERIFICATION].",
    historical_context="The Paulée de Meursault originated in 1923. Every grower brings bottles from their own cellar; guests bring bottles to share. The meal runs for six hours.")

R("Puligny-Montrachet", "France", "wine", parent_id=cote_beaune,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Domaine Leflaive, Domaine Carillon, Domaine Sauzet, Maison Chartron et Trébuchet",
    description="Apex of white Burgundy. Grand Crus: Le Montrachet (shared with Chassagne — the world's greatest dry white wine), Chevalier-Montrachet, Bâtard-Montrachet (shared), Bienvenues-Bâtard-Montrachet. Crisp, mineral, taut in youth; profoundly honeyed with age. Domaine Leflaive is the reference estate. BC importer for Leflaive: Lifford Wine Agency [NEEDS VERIFICATION].")

R("Chassagne-Montrachet", "France", "wine", parent_id=cote_beaune,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine Ramonet, Domaine Colin, Domaine Moreau-Naudet",
    description="Shares Le Montrachet and Bâtard-Montrachet Grand Crus with Puligny. Best-value entry point to white Burgundy at village level. Ramonet is the undisputed benchmark. Also underrated reds from Pinot Noir. BC importer: Classic Wine Imports [NEEDS VERIFICATION].")

chablis = R("Chablis", "France", "wine", parent_id=burgundy,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine Raveneau, Domaine Dauvissat, William Fèvre, Domaine Long-Depaquit",
    description="Northernmost Burgundy, 110km from the Côte d'Or. Kimmeridgian limestone soil — chalk and fossilised oyster shells from a prehistoric sea — creates piercing mineral salinity. Chardonnay only. Four tiers: Petit Chablis, Chablis, Premier Cru (40 vineyards, 17 grouped designations), Grand Cru (7 named vineyards: Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Vaudésir, Valmur). No new oak in serious expressions — purity of terroir paramount. BC importer for Raveneau: extremely allocated [NEEDS VERIFICATION].",
    historical_context="The Kimmeridgian soil formed 150 million years ago when the area was covered by a shallow sea — the fossilised shells of Exogyra virgula oysters are visible in the soil to this day.")

# ─── FRANCE — BORDEAUX ────────────────────────────────────────────────────────
print("\n=== FRANCE — BORDEAUX ===")
bordeaux = R("Bordeaux", "France", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Lafite Rothschild, Château Mouton Rothschild, Château Latour, Château Margaux, Château Haut-Brion, Château Pétrus, Château Cheval Blanc, Château Ausone",
    description="World's largest fine wine region. Two banks of the Gironde: Left Bank (Cabernet dominant — power, structure, 20–50 year cellaring) and Right Bank (Merlot dominant — more accessible). The 1855 Classification of the Médoc remains the most famous wine hierarchy in existence. The Place de Bordeaux négociant system and en primeur (futures) define global fine wine trade.",
    historical_context="The 1855 Classification was commissioned by Napoleon III for the Paris Exhibition. It ranked 61 Médoc estates and Sauternes. Only one change has ever been made: Mouton Rothschild elevated from Second to First Growth in 1973 by presidential decree.")

medoc = R("Médoc", "France", "wine", parent_id=bordeaux,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Léoville Las Cases, Château Léoville Barton, Château Pichon Baron, Château Cos d'Estournel",
    description="Left-bank peninsula north of Bordeaux, 80km along the Gironde. Gravelly soils warm quickly, drain perfectly — ideal for Cabernet Sauvignon. The Haut-Médoc communes (Pauillac, Saint-Julien, Margaux, Saint-Estèphe) contain the 1855 classified properties.")

R("Pauillac", "France", "wine", parent_id=medoc,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Lafite Rothschild, Château Mouton Rothschild, Château Latour, Château Pichon-Longueville-Baron, Château Lynch-Bages",
    description="The most powerful Médoc commune. Three of five First Growths: Lafite Rothschild, Mouton Rothschild, and Latour — the 'Holy Trinity.' Deep gravel terraces on the Gironde. Latour's Grand Vin is among the most age-worthy reds on earth — 50-year bottles are routine. BC importer: Select Wine Merchants / Lifford [NEEDS VERIFICATION].")

R("Saint-Julien", "France", "wine", parent_id=medoc,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Léoville Las Cases, Château Léoville Poyferré, Château Léoville Barton, Château Ducru-Beaucaillou, Château Gruaud Larose",
    description="Most consistent Médoc commune. No First Growths but finest concentration of Second Growths. Elegant, proportioned, cedar-scented Cabernet Sauvignon. The commune that best represents Médoc style without extreme concentration or extraction.")

R("Margaux", "France", "wine", parent_id=medoc,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Margaux, Château Palmer, Château Brane-Cantenac, Château Rauzan-Ségla",
    description="Most perfumed and silky Médoc commune. Château Margaux is the sole First Growth. Sandy-gravel soils produce Cabernet Sauvignon of extraordinary elegance — violet, black fruit, cedar — rather than raw power. The most 'feminine' of the great Médoc communes. BC importer: Lifford Wine Agency [NEEDS VERIFICATION].")

R("Saint-Estèphe", "France", "wine", parent_id=medoc,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Château Cos d'Estournel, Château Montrose, Château Calon-Ségur",
    description="Northernmost Haut-Médoc commune. Heavier clay soils produce more tannic, austere, slower-developing wines. No First Growths, but Cos d'Estournel (Second Growth) achieves exceptional quality. The most structured and age-demanding of the Médoc communes.")

R("Pessac-Léognan", "France", "wine", parent_id=bordeaux,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Haut-Brion, Château La Mission Haut-Brion, Château Pape Clément, Château Smith Haut Lafitte",
    description="Quality heartland of the Graves appellation, closest to Bordeaux city. Home to the only Left Bank First Growth outside the Médoc: Château Haut-Brion (and La Mission Haut-Brion, under same ownership). Unique combination of clay-gravel soils, urban heat, and early ripening produces wines with a distinct smokiness, earthiness, and tobacco note. Outstanding dry whites from Sauvignon Blanc/Sémillon.")

R("Saint-Émilion", "France", "wine", parent_id=bordeaux,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Cheval Blanc, Château Ausone, Château Angélus, Château Pavie, Château Figeac",
    description="Principal Right Bank appellation. Merlot dominant on limestone plateau and clay-limestone slopes. Two Premier Grand Cru Classé A: Château Ausone (limestone plateau — precise, structured, exceptional longevity) and Château Cheval Blanc (the 1947 is widely considered the greatest wine ever made; unique Cabernet Franc dominant for Right Bank). The classification is revised every 10 years — controversially.",
    historical_context="The medieval town of Saint-Émilion is a UNESCO World Heritage Site. The monolithic church — carved entirely into the limestone rock below the town — dates to the 12th century.")

R("Pomerol", "France", "wine", parent_id=bordeaux,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Pétrus, Le Pin, Château Lafleur, Vieux Château Certan, Château L'Évangile",
    description="Smallest major Bordeaux appellation — 800 hectares, no official classification, no château tourism. Blue clay soil produces purely Merlot of extraordinary concentration and complexity. Château Pétrus (Jean-Pierre Moueix) is the icon: harvested in the afternoon to avoid morning dew, unclassified yet worth more per bottle than any First Growth. Le Pin (Thienponts) is the ultimate garage wine.")

R("Fronsac", "France", "wine", parent_id=bordeaux,
    reputation_tier="respected", quality_trajectory="rediscovering", authority_tier=2,
    key_producers="Château Moulin Haut-Laroque, Château La Rivière, Château Dalem",
    description="Small Right Bank appellation northwest of Pomerol. Merlot-dominant on limestone and clay. Significantly undervalued relative to neighbours — 'the sleeping giant of Bordeaux.' Good value access to Right Bank quality and style.")

# ─── FRANCE — RHÔNE ─────────────────────────────────────────────────────────
print("\n=== FRANCE — RHÔNE VALLEY ===")
rhone = R("Rhône Valley", "France", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="E. Guigal, Chapoutier, Jean-Louis Chave, Château Rayas, Château Beaucastel, Jaboulet, Clape",
    description="France's third great wine region, 200km from Lyon to Avignon. Divided at Montélimar: Northern Rhône (narrow granite terraces; Syrah king; Viognier for whites) and Southern Rhône (broad, warm; Grenache-dominant blends up to 13 varieties). Syrah's spiritual home in both its most intellectual (Hermitage) and most complex blended (Châteauneuf-du-Pape) expressions.",
    historical_context="The Rhône has been France's wine highway since Roman times — the river was the transport artery for wines moving north from Marseille and south from Lyon.")

northern_rhone = R("Northern Rhône", "France", "wine", parent_id=rhone,
    reputation_tier="iconic", authority_tier=1,
    key_producers="E. Guigal, Jean-Louis Chave, Chapoutier, Jaboulet, Auguste Clape, Georges Vernay",
    description="70km corridor of steep granite terraces and river-carved schist from Vienne to Valence. Exclusively Syrah for reds (up to 20% Viognier co-fermented in Côte-Rôtie). Viognier alone for whites (Condrieu). Universal hand-harvesting. The most intellectual and age-worthy Syrah on earth.")

R("Côte-Rôtie", "France", "wine", parent_id=northern_rhone,
    reputation_tier="iconic", authority_tier=1,
    key_producers="E. Guigal, René Rostaing, Stéphane Ogier, Pierre Gaillard",
    description="'The Roasted Slope' — northernmost and most prestigious Northern Rhône appellation. Côte Brune (iron-rich, structured) and Côte Blonde (sand-silica, perfumed). Up to 20% Viognier co-fermented with Syrah adds violet lift. Guigal's single-vineyard La Mouline, La Landonne, La Turque — aged 42 months in new oak — are among France's greatest allocated wines. BC importer for Guigal: Mark Anthony Group [NEEDS VERIFICATION].",
    historical_context="The 'La-Las' (La Mouline, La Landonne, La Turque) were first released as single-vineyard wines in 1976, 1978, and 1985 respectively. Each vintage is released 4-5 years after harvest.")

R("Hermitage", "France", "wine", parent_id=northern_rhone,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Jean-Louis Chave, Jaboulet (La Chapelle), Chapoutier (Méal/L'Ermite), E. Guigal",
    description="The greatest Syrah appellation on earth. A single granite hill above Tain-l'Hermitage — 136 hectares, south-facing, divided into named lieux-dits (Le Méal, L'Ermite, Les Bessards). Red Hermitage from Chave and Jaboulet's La Chapelle ages 30–60 years. White Hermitage (Marsanne/Roussanne) is among France's rarest and longest-lived whites. BC importer: Lifford Wine Agency [NEEDS VERIFICATION].",
    historical_context="The first recorded mention of Hermitage as a fine wine is 1650. The hill was fortified in Roman times. The hermit legend — Gaspard de Stérimberg returning from the Crusades — is almost certainly apocryphal.")

R("Cornas", "France", "wine", parent_id=northern_rhone,
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Auguste Clape, Thierry Allemand, Vincent Paris, Alain Voge",
    description="Pure Syrah from granite terraces south of Hermitage. The most rustic and powerful Northern Rhône appellation — 'cor nas' means 'burnt earth' in Occitan. Dark, inky, peppery, slow-opening wines. Must be the most patient wine in the Rhône. Auguste Clape is the patriarch; Thierry Allemand is the modern perfectionist benchmark.")

R("Saint-Joseph", "France", "wine", parent_id=northern_rhone,
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=2,
    key_producers="Jean-Louis Chave, Gonon, Courbis, Pierre Gaillard",
    description="Longest Northern Rhône appellation, 60km along the west bank. Both reds (Syrah) and whites (Marsanne/Roussanne). Quality varies widely — best parcels are on granite adjacent to Hermitage. Top producers (Chave, Gonon) make serious, affordable wines — the BC entry point for Northern Rhône style.")

R("Condrieu", "France", "wine", parent_id=northern_rhone,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="E. Guigal, Georges Vernay, Yves Cuilleron, Gangloff",
    description="World home of Viognier — exclusively white wine. Apricot, peach, violet, white blossom — immediately recognisable. Rich and generous but can be short-lived; drink within 5 years except from top producers. The 20-hectare Château-Grillet within Condrieu is a separate single-estate Grand Cru appellation.",
    historical_context="Condrieu nearly disappeared in the 1960s — only 15 hectares remained. Georges Vernay ('the guardian of Condrieu') almost single-handedly preserved the appellation through the difficult decades.")

R("Southern Rhône", "France", "wine", parent_id=rhone,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Château Rayas, Château Beaucastel, Domaine du Vieux Télégraphe, Château la Nerthe",
    description="Vast Mediterranean plateau south of Montélimar. Hot, dry summers; the Mistral wind. Grenache dominant, supplemented by Syrah, Mourvèdre, Cinsault, Carignan, and many others. Wines of warmth, generosity, and spiced fruit. From simple Côtes du Rhône to the profound complexity of Châteauneuf-du-Pape.")

R("Châteauneuf-du-Pape", "France", "wine", parent_id=rhone,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Château Rayas, Château Beaucastel, Château la Nerthe, Domaine du Vieux Télégraphe, Clos des Papes",
    description="13 permitted grape varieties — the most of any French AOC. The galets roulés (large rounded pebbles) are iconic but cover only part of the zone; soils include clay, sand, limestone, and iron-rich red clay. Château Rayas (pure Grenache from 30-year-old estate, near-impossible to obtain) is often considered the greatest Grenache expression on earth. Beaucastel (Mourvèdre prominent) has exceptional longevity. BC importer: Pacific Wine & Spirits [NEEDS VERIFICATION].",
    historical_context="The 'New Castle of the Pope' was built by Pope John XXII in 1317 when the Papacy was in Avignon. The vineyards surrounding it became the papal estate. The castle was destroyed in WWI artillery.")

R("Gigondas", "France", "wine", parent_id=rhone,
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=2,
    key_producers="Domaine de la Gaulière, Les Pallières, Domaine Santa Duc, Château Raspail-Ay",
    description="Hillside appellation in the Dentelles de Montmirail. Grenache and Syrah dominant on limestone and clay soils at higher altitude than Châteauneuf. More structured and mineral. Excellent value compared to Châteauneuf. The 'baby Châteauneuf' of the trade.")

R("Vacqueyras", "France", "wine", parent_id=rhone,
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=2,
    key_producers="Domaine Le Sang des Cailloux, Château des Tours, Domaine La Fourmone",
    description="Elevated to AC in 1990. Neighbour to Gigondas, spicier and more herb-driven. Domaine Le Sang des Cailloux is the benchmark. Smaller, less-known, often underpriced relative to quality — reliable Rhône value for BC wine lists.")

R("Tavel", "France", "wine", parent_id=rhone,
    reputation_tier="prestigious", authority_tier=2,
    key_producers="Domaine de la Mordorée, Château d'Aquéria, Domaine Maby",
    description="France's most celebrated rosé-only appellation. Grenache-dominant (with Cinsault, Clairette, Mourvèdre) produces the fullest-bodied, most age-worthy French rosé. Salmon-copper in colour, dry and structured — not a pale Provençal blush. Can age 3–5 years. The only French appellation legally restricted to rosé.",
    historical_context="Tavel's reputation for rosé dates to the Middle Ages. Louis XIV and the Popes of Avignon were admirers. 'The best rosé in France' has been the refrain since the 18th century.")

# ─── FRANCE — CHAMPAGNE ──────────────────────────────────────────────────────
print("\n=== FRANCE — CHAMPAGNE ===")
champagne = R("Champagne", "France", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Krug, Dom Pérignon, Salon, Jacques Selosse, Pierre Péters, Egly-Ouriet, Bollinger, Louis Roederer, Gosset",
    description="160km northeast of Paris. Belemnite chalk subsoil — porous, water-retaining — is the geological foundation of Champagne's piercing minerality. Three main varieties: Chardonnay (crisp, citrus, minerality — Côte des Blancs), Pinot Noir (structure, red fruit — Montagne de Reims), Pinot Meunier (approachability — Vallée de la Marne). Traditional method in-bottle fermentation creates yeast autolysis character: brioche, toast, biscuit.",
    historical_context="Dom Pérignon did not 'invent' Champagne but was the cellar master at Hautvillers Abbey who systematised blending and cork closure in the late 17th century. The English were the first to consciously make sparkling Champagne — they had the coal-furnace technology to make glass strong enough to contain the pressure.")

R("Montagne de Reims", "France", "wine", parent_id=champagne,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Krug (Ambonnay), Bollinger (Ay), Egly-Ouriet (Ambonnay), Georges Laval",
    description="Forested plateau south of Reims. Pinot Noir dominant — most structured, vinous, age-worthy base wines. Grand Cru villages: Ambonnay, Bouzy, Ay. Krug's Ambonnay single-vineyard Blanc de Noirs is one of the world's rarest Champagnes.")

R("Côte des Blancs", "France", "wine", parent_id=champagne,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Salon (Le Mesnil-sur-Oger monopole), Pierre Péters, Guy Charlemagne, Agrapart",
    description="South-facing chalk slopes southeast of Épernay. Almost exclusively Chardonnay. Source of Champagne's finest blanc de blancs cuvées. Salon (Le Mesnil-sur-Oger monopole — only single village, single vintage, single variety, single vineyard blanc de blancs) is one of the world's great wines. Produced only in exceptional years.")

R("Vallée de la Marne", "France", "wine", parent_id=champagne,
    reputation_tier="respected", authority_tier=1,
    key_producers="Krug, Bollinger, Ayala, Deutz",
    description="River valley from Épernay westward toward Paris. Pinot Meunier dominant — most approachable, early-drinking variety. Grand Cru village of Ay (historic heart). House Champagnes use Meunier for accessibility and primary fruit character.",
    historical_context="The Vallée de la Marne was the first transport route for Champagne exports — the river leading to Paris. The great houses established their headquarters in Épernay precisely for river access.")

# ─── FRANCE — LOIRE VALLEY ──────────────────────────────────────────────────
print("\n=== FRANCE — LOIRE VALLEY ===")
loire = R("Loire Valley", "France", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Didier Dagueneau, Domaine Huet, Nicolas Joly, Domaine Vacheron, Henri Bourgeois",
    description="France's most diverse wine region — 1,020km from the Atlantic to Pouilly-Fumé. Four major zones: Pays Nantais (Muscadet/Melon de Bourgogne), Anjou-Saumur (Chenin Blanc and Cabernet Franc), Touraine (Vouvray/Chinon/Bourgueil), Loire Centre (Sancerre/Pouilly-Fumé). Styles range from bone-dry mineral whites to 100-year-lived botrytised sweet wines.")

R("Muscadet / Pays Nantais", "France", "wine", parent_id=loire,
    reputation_tier="respected", quality_trajectory="rediscovering", authority_tier=2,
    key_producers="Domaine de la Pépière, Domaine Michel Brégeon, Château du Cléray",
    description="Westernmost Loire, near Nantes. Melon de Bourgogne grape — high acid gains complexity through sur lie ageing (5–6+ months on fine lees). Best expressions (Muscadet Sèvre et Maine sur Lie, Cru Communaux) develop rich, saline-yeasty character. Textbook wine-food pairing: oysters and Muscadet. The Cru Communaux (Clisson, Gorges, Le Pallet) represent the apex of quality.",
    historical_context="Muscadet's reputation suffered commercially for 30 years — it became a synonym for cheap, acidic white wine. The Cru Communaux designation (2011) has re-elevated the appellation's best terroirs.")

R("Sancerre", "France", "wine", parent_id=loire,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Henri Bourgeois, Domaine Vacheron, Domaine Cotat, Domaine Henri Pellé",
    description="Most prestigious Loire Sauvignon Blanc appellation. Three soil types: silex (flint — mineral, smoky, taut), calcaires (limestone — rounder), terres blanches (Kimmeridgian — complex, structured). Also Pinot Noir red and rosé — the best 'rouges de Sancerre' are seriously competitive with light Burgundy. BC importer: Lifford [NEEDS VERIFICATION].")

R("Pouilly-Fumé", "France", "wine", parent_id=loire,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Didier Dagueneau (Silex, Pur Sang), Château de Tracy, De Ladoucette",
    description="Across the Loire from Sancerre. The 'fumé' refers to silex (gunflint) soil — a smoky, struck-match minerality. Didier Dagueneau's Silex and Pur Sang are among the world's great Sauvignon Blancs. Now produced by son Louis-Benjamin after Didier's death in 2008. BC importer for Dagueneau: Skye Import [NEEDS VERIFICATION].",
    historical_context="Didier Dagueneau introduced biodynamic farming, low yields, and the use of new oak barrels for Sauvignon Blanc — all controversial in the Loire — to create Pouilly-Fumé of Grand Cru status. His 2001 Silex sells at auction for $400+ CAD.")

R("Vouvray", "France", "wine", parent_id=loire,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Domaine Huet, Domaine du Clos Naudin, Château Moncontour",
    description="Capital of Chenin Blanc — most versatile white grape variety. Vouvray styles: sec (dry), sec-tendre (off-dry), demi-sec (medium), moelleux (sweet), pétillant/mousseux (sparkling). Vintage conditions determine which is made. Domaine Huet (three monopole vineyards: Clos du Bourg, Le Haut-Lieu, Le Mont — biodynamic since 1990) is the reference estate. A great Huet moelleux from a botrytised year can age 100 years.",
    historical_context="Huet's estate was biodynamic before the word was common in France. Noël Pinguet (Huet's son-in-law) introduced biodynamics in 1990. The estate produces in three styles each vintage — allowing comparison of the same site under different levels of residual sugar.")

R("Chinon", "France", "wine", parent_id=loire,
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Philippe Alliet, Domaine Bernard Baudry, Charles Joguet",
    description="The Loire's great red wine appellation. Cabernet Franc on tuffeau (elegant, floral), gravel-sand (lighter), and clay-gravel (structured). Philippe Alliet's Vieilles Vignes is the benchmark — earthy, pencil-graphite, serious Loire Franc. Serve at 14–15°C; decant at 45 minutes for structured cuvées.",
    historical_context="François Rabelais — author of Gargantua and Pantagruel — was born near Chinon in 1494 and wrote lovingly of the local wine. 'Drink always and never die' was his reported motto.")

R("Bourgueil", "France", "wine", parent_id=loire,
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=2,
    key_producers="Domaine Yannick Amirault, Domaine de la Chevalerie, Domaine Pierre-Jacques Druet",
    description="Across the Loire from Chinon. Cabernet Franc on tuffeau — lighter, more immediately aromatic than Chinon. Can be served slightly cool (14°C). Domaine Yannick Amirault is the benchmark. Saint-Nicolas-de-Bourgueil to the west has lighter, sandier soils producing the most approachable Loire reds.")

R("Savennières", "France", "wine", parent_id=loire,
    reputation_tier="prestigious", quality_trajectory="rediscovering", authority_tier=1,
    key_producers="Nicolas Joly, Domaine des Baumard, Château d'Épiré, Domaine du Closel",
    description="Most austere and age-worthy dry Chenin Blanc in the world. 350 hectares on schist slopes above the Loire near Angers. Searingly dry, mineral, needs 10–20 years to reveal complexity. Nicolas Joly's Coulée de Serrant (7-hectare Grand Cru monopole — biodynamic pioneer since 1980) is celebrated globally. BC importer for Joly: La Fête du Vin [NEEDS VERIFICATION].",
    historical_context="Nicolas Joly was the first high-profile French wine producer to convert to biodynamics, in 1980. He became an evangelist for the Demeter standard and his Coulée de Serrant is often cited as the wine that proves biodynamics is not merely mysticism.")

# ─── FRANCE — ALSACE ────────────────────────────────────────────────────────
print("\n=== FRANCE — ALSACE ===")
R("Alsace", "France", "wine",
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Trimbach (Clos Sainte Hune), Zind-Humbrecht, Domaine Weinbach, Hugel, Domaine Marcel Deiss",
    description="France's Germanic wine region — the Marseille Crossroads Doctrine in viticulture. On the Rhine border with Germany (Baden across the river). The Vosges mountains create a dramatic rain shadow — Colmar is the driest city in France outside the Mediterranean. Wines are labelled by variety (Riesling, Gewurztraminer, Pinot Gris, Muscat) rather than by appellation — opposite of Burgundy. 51 Grand Cru sites. Vendange Tardive (VT) and Sélection de Grains Nobles (SGN) are the botrytised sweet wine categories.",
    historical_context="Alsace has changed nationhood four times between France and Germany since 1870. The region was German from 1871–1918 and 1940–1944. This Franco-German duality explains why Alsace wines are bottled in tall, tapered German flûtes but labelled in French, and why the cuisine is choucroute garnie (French name for German Sauerkraut).")

# ─── FRANCE — SPIRITS ────────────────────────────────────────────────────────
print("\n=== FRANCE — SPIRITS REGIONS ===")
R("Cognac", "France", "spirits",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Rémy Martin, Hennessy, Martell, Delamain, Hine, Hardy, Pierre Ferrand, Frapin",
    description="AOC Cognac in the Charente département, northwest France. Six crus ranked by chalk content: Grande Champagne (finest, most delicate — required for XO labelling in blends), Petite Champagne, Borderies (small zone; violet character; Courvoisier source), Fins Bois, Bons Bois, Bois Ordinaires. Ugni Blanc (Trebbiano) — high acid, low alcohol — ideal for distillation. Double distillation in copper alambic charentais. Ageing in Limousin or Tronçais oak.",
    historical_context="The Dutch developed the Charentais distillation method in the 17th century to concentrate the thin, acidic Charente wines for export — they were surprised to find the resulting spirit was itself pleasurable. The port of La Rochelle made Cognac a global trade.")

R("Armagnac", "France", "spirits",
    reputation_tier="prestigious", quality_trajectory="rediscovering", authority_tier=1,
    key_producers="Darroze, Castarède, Delord, Armagnac de Montal, Domaine Boingnères",
    description="France's oldest brandy AOC — predating Cognac by a century. Single continuous distillation (alambic armagnacais column still) produces a more flavourful, rustic spirit than Cognac's double-distilled refinement. Three sub-regions: Bas-Armagnac (sandy soils; finest, most elegant), Ténarèze (clay-limestone; more structured), Haut-Armagnac (chalk; rarely bottled alone). Armagnac is the artisan alternative: smaller production, more vintage variation, more character. Vintage Armagnac (single-year) is more common than vintage Cognac.",
    historical_context="The first written record of Armagnac distillation dates to 1411. Armagnac was drunk medicinally before Cognac existed. Cardinal d'Armagnac reportedly prescribed it for 40 ailments including curing fevers and brightening the complexion.")

R("Normandy", "France", "spirits",
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Domaine Dupont, Boulard, Christian Drouin, Père Magloire",
    description="Premier apple-growing region of France. Source of Calvados (apple brandy) and Pommeau (unfermented apple juice + Calvados). The bocage landscape — hedgerow-enclosed orchards — defines Normandy's interior. Two Calvados AOCs: Calvados Pays d'Auge (double distillation required — finest, most aromatic; Dupont is the benchmark), Calvados Domfrontais (pear mandatory in the blend).",
    historical_context="Calvados takes its name from the Département du Calvados, created in 1790. The drink was known as 'eau de vie de cidre' (apple cider eau de vie) long before the regional name was attached. Normandy cider dates to the 8th century; distillation began in the 16th century.")

R("Provence", "France", "spirits",
    reputation_tier="prestigious", authority_tier=2,
    key_producers="Ricard, Pernod, Henri Bardouin, Janot, Casanis",
    description="Southeast France, Mediterranean coast. Cultural heartland of Provençal rosé (Grenache, Cinsault, Syrah; pale salmon; world's best-selling rosé style) and the spiritual home of pastis — the anise-flavoured spirit that replaced absinthe after the 1915 ban. Marseille is the pastis capital: Ricard headquarters, boules on the Prado, the ritual of the afternoon pastis. The connection: pastis sits in the Mediterranean anise family alongside ouzo (Greece), arak (Lebanon), raki (Turkey), and sambuca (Italy) — all sharing anethole as the defining molecule.",
    historical_context="Paul Ricard created Ricard pastis in Marseille in 1932, 17 years after the absinthe ban. He was 23 years old. Ricard became France's most profitable drinks company. The Ricard name is still on half of all pastis sold globally.")

# ─── ITALY ──────────────────────────────────────────────────────────────────
print("\n=== ITALY — PIEDMONT ===")
piedmont = R("Piedmont", "Italy", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Giacomo Conterno, Bartolo Mascarello, Bruno Giacosa, Gaja, Vietti, Produttori del Barbaresco, Domenico Clerico",
    description="Northwest Italy, 'foot of the Alps.' Home to Nebbiolo — Italy's answer to Pinot Noir: thin-skinned, high acid, high tannin, late-ripening, terroir-sensitive. Barolo and Barbaresco are the twin Grand Cru expressions. Also Barbera d'Asti (high acid, everyday), Dolcetto (soft, cherry-bitter), Moscato d'Asti (delicate sweet fizz), Gavi (Cortese — crisp mineral white). The autumn fog (la nebbia) names the grape variety.",
    historical_context="Barolo was created as a modern wine style in the 1860s — French enologist Louis Oudart (working for the Marchese di Barolo) introduced dry fermentation to eliminate the residual sugar in what had been a semi-sweet wine. General Govone and Cavour were also instrumental in elevating the style.")

R("Barolo DOCG", "Italy", "wine", parent_id=piedmont,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Giacomo Conterno, Bartolo Mascarello, Bruno Giacosa, Vietti, Elio Altare, Luciano Sandrone",
    description="'King of Italian Wines.' Nebbiolo from 11 communes in the Langhe hills south of Alba. MGA (Menzione Geografica Aggiuntiva) system — 181 named vineyards (2010). Traditional vs Modern debate: Traditional (long maceration, old large botti) vs Modern (short maceration, French barriques). Great Crus: Cannubi, Bricco Rocche (Castiglione Falletto), Vigna Rionda/Francia (Serralunga d'Alba), Brunate/Cerequio (La Morra). Giacomo Conterno's Monfortino (single vineyard, released only in exceptional years, aged 7+ years) is Italy's most sacred wine. BC importer: La Fête du Vin [NEEDS VERIFICATION].",
    historical_context="The traditional vs modern Barolo debate (the 'Barolo Wars') erupted in the 1980s when young winemakers including Elio Altare and Domenico Clerico introduced short maceration and French oak to create more immediately accessible wines. The debate has largely resolved — most producers now blend the approaches.")

R("Barbaresco DOCG", "Italy", "wine", parent_id=piedmont,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Gaja, Produttori del Barbaresco, Bruno Giacosa, Roagna, Nino Negri",
    description="'Queen of Italian Wines.' Nebbiolo from Barbaresco, Neive, and Treiso northeast of Alba. More elegant and earlier-maturing than Barolo — slightly warmer mesoclimate, more sandstone in soils. Gaja's single-vineyard wines (Sorì Tildìn, Sorì San Lorenzo, Costa Russi) brought Barbaresco to international prominence. Produttori del Barbaresco (cooperative) produces terroir-transparent benchmark wines at half Gaja's price. Bruno Giacosa's Riserva (red label) is the most sought-after Barbaresco. BC importer for Gaja: Select Wine Merchants [NEEDS VERIFICATION].",
    historical_context="Gaja Angelo (born 1940) took over his family estate in 1961 and transformed Barbaresco from a regional curiosity to an internationally celebrated wine, achieving prices comparable to Pétrus by the 1990s.")

R("Asti DOCG", "Italy", "wine", parent_id=piedmont,
    reputation_tier="respected", authority_tier=2,
    key_producers="G.D. Vajra, Ceretto, La Spinetta, Saracco, Cascina Castlèt",
    description="Two DOCG designations: Moscato d'Asti (delicate, low-alcohol 5.5% ABV sweet sparkling; peach, apricot, orange blossom; partial fermentation stopped by chilling — not traditional method) and Asti Spumante (fully sparkling, higher alcohol). Also Barbera d'Asti DOCG — Barbera's finest standalone appellation, high acid, excellent with pasta.")

R("Gavi DOCG", "Italy", "wine", parent_id=piedmont,
    reputation_tier="respected", authority_tier=2,
    key_producers="La Scolca, Villa Sparina, Broglia, Produttori del Gavi",
    description="Cortese grape from hills around the town of Gavi in southeastern Piedmont. Italy's finest dry white from a classic indigenous variety — crisp, mineral, almond-scented, bitter finish. La Scolca was the original commercialiser. Best examples age 5–8 years developing nutty, honeyed complexity. Gavi di Gavi indicates vineyards within the town of Gavi itself.")

print("\n=== ITALY — TUSCANY ===")
tuscany = R("Tuscany", "Italy", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="Biondi-Santi, Antinori, Sassicaia, Ornellaia, Fontodi, Isole e Olena, Soldera",
    description="Soul of Italian wine culture. Sangiovese — in many clonal expressions — defines the region. Three iconic DOCG hierarchies: Chianti Classico, Brunello di Montalcino, Vino Nobile di Montepulciano. The Super Tuscans (IGT wines — Sassicaia, Tignanello, Ornellaia) bypassed the DOC system from the 1970s using international varieties, rewriting the world's perception of Italian wine.",
    historical_context="The Super Tuscan revolution began with Marchese Mario Incisa della Rocchetta planting Cabernet Sauvignon in 1944 inspired by Bordeaux. Sassicaia was first commercially released in 1971. Antinori's Tignanello (1971) followed — then the category exploded globally.")

R("Chianti Classico DOCG", "Italy", "wine", parent_id=tuscany,
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Fontodi, Isole e Olena, Querciabella, Castello di Ama, San Felice, Riecine",
    description="Historic zone between Florence and Siena — the Gallo Nero (black rooster) symbol. Sangiovese mandatory 80–100%. Three quality tiers: Chianti Classico (12 months min ageing), Chianti Classico Riserva (24 months), Gran Selezione (single-vineyard, 30 months — introduced 2014). Galestro (friable sandstone-limestone) and alberese (hard clay-limestone) soils create firm tannin, high acid, cherry-tobacco Sangiovese. BC importer: Vinos del Mundo [NEEDS VERIFICATION].",
    historical_context="The Chianti Classico zone boundary was defined by the Grand Duchy of Tuscany in 1716 — one of the world's first legally delimited wine regions. The Gallo Nero consortium was founded in 1924 to protect quality.")

R("Brunello di Montalcino DOCG", "Italy", "wine", parent_id=tuscany,
    reputation_tier="iconic", authority_tier=1,
    key_producers="Biondi-Santi, Soldera (Case Basse), Salvioni, Ciacci Piccolomini, Poggio di Sotto",
    description="Italy's most age-worthy red. 100% Sangiovese Grosso (Brunello) from the hilltop town of Montalcino. Minimum ageing: 5 years (2 oak, 4 months bottle); Riserva 6 years. Needs 10–20 years minimum to reveal complexity. Biondi-Santi invented the appellation in 1888. Soldera (Case Basse) is the perfectionist boutique estate — never uses young vines, never releases early. BC importer for Biondi-Santi: Select Wine Merchants [NEEDS VERIFICATION].",
    historical_context="Ferruccio Biondi-Santi first isolated and planted the Brunello clone (a superior Sangiovese) in 1870. He was the first to vinify Brunello as a serious, long-aged dry red — the 1888 Biondi-Santi is reportedly still drinkable.")

R("Bolgheri DOC", "Italy", "wine", parent_id=tuscany,
    reputation_tier="iconic", quality_trajectory="established", authority_tier=1,
    key_producers="Sassicaia (Tenuta San Guido), Ornellaia, Masseto, Antinori (Guado al Tasso)",
    description="Birthplace of the Super Tuscans. Coastal Tuscany, 80km south of Livorno. Mediterranean climate — warm, maritime. Marchese Mario Incisa della Rocchetta planted Cabernet Sauvignon in 1944; first commercial release 1971. Ornellaia and Masseto (Merlot — Italy's answer to Pétrus) followed. Sassicaia has its own DOC sub-denomination (Bolgheri Sassicaia DOC). BC importer for Sassicaia: Lifford Wine Agency [NEEDS VERIFICATION].",
    historical_context="Sassicaia 1985 won a blind tasting competition organised by Decanter magazine in 1994, beating First Growth Bordeaux. The result shocked the wine world and established Italian Super Tuscans permanently on the fine wine map.")

R("Vino Nobile di Montepulciano DOCG", "Italy", "wine", parent_id=tuscany,
    reputation_tier="prestigious", authority_tier=2,
    key_producers="Avignonesi, Poliziano, Boscarelli, Bindella",
    description="Sangiovese (called Prugnolo Gentile locally) from the hilltop town of Montepulciano. Between Brunello and Chianti Classico in weight. Minimum 2 years ageing (3 for Riserva). Note: the town of Montepulciano should never be confused with the Abruzzo grape Montepulciano d'Abruzzo — entirely different variety, different region.",
    historical_context="'Vino Nobile' — 'noble wine' — reflects the wine's historical association with the Montepulciano aristocracy. Francesco Redi called it 'king of all wines' in 1685 in his poem Bacco in Toscana.")

R("Vernaccia di San Gimignano DOCG", "Italy", "wine", parent_id=tuscany,
    reputation_tier="respected", quality_trajectory="rediscovering", authority_tier=2,
    key_producers="Teruzzi & Puthod, Montenidoli, Casale-Falchini, Panizzi",
    description="Italy's first DOC (1966), subsequently DOCG. Vernaccia grape — indigenous, high acid, bitter almond finish. From the medieval tower town of San Gimignano. Commercial versions are often thin and forgettable; the serious single-vineyard versions (Montenidoli, Panizzi) are compelling. Now reviving through producer focus on terroir and lower yields.",
    historical_context="Michelangelo reportedly loved Vernaccia di San Gimignano. The Vernaccia grape is mentioned in Italian documents from 1276.")

print("\n=== ITALY — VENETO ===")
veneto = R("Veneto", "Italy", "wine",
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Quintarelli, Dal Forno Romano, Pieropan, Allegrini, Bertani, Tedeschi",
    description="Northeast Italy. Italy's largest DOC wine-producing region. The Soave-Valpolicella-Prosecco triangle defines the three pillars. The appassimento technique — drying harvested grapes to concentrate sugars and flavour — is the region's unique contribution to world winemaking, creating Amarone della Valpolicella.",
    historical_context="Verona has been a wine trade centre since Roman times — it sits at the junction of the Via Postumia (running east-west) and the route from Lake Garda to the Adriatic. The Roman amphitheatre in Verona still hosts opera and the Vinitaly wine fair is held annually.")

R("Valpolicella DOC", "Italy", "wine", parent_id=veneto,
    reputation_tier="prestigious", authority_tier=1,
    key_producers="Quintarelli, Dal Forno Romano, Allegrini, Bertani, Tedeschi, Zenato",
    description="Northwest of Verona. Corvina, Rondinella, and Molinara grape trio in three styles: Valpolicella (light, cherry-scented), Valpolicella Ripasso (refermented over Amarone pomace — medium-weight), Amarone della Valpolicella DOCG (appassimento — grapes dried 90–120 days; 14–17% ABV; dried cherry, chocolate, tobacco, spice concentration; minimum 2 years ageing). Also Recioto della Valpolicella (sweet version). Quintarelli is the undisputed master; Dal Forno is the modern super-concentrated style. BC importer: La Fête du Vin [NEEDS VERIFICATION].",
    historical_context="Amarone was a 'discovered accident' — a Recioto barrel that continued fermenting to dryness. The winemaker at Bertani reportedly tasted the dry version in 1936 and exclaimed 'This is amaro!' (bitter). The name Amarone stuck.")

R("Soave DOC", "Italy", "wine", parent_id=veneto,
    reputation_tier="respected", quality_trajectory="rediscovering", authority_tier=2,
    key_producers="Pieropan, Anselmi, Inama, Gini",
    description="East of Verona. Garganega grape (75%+ mandatory) — lemon, almond, white peach, mineral finish. Soave Classico (historic hillside zone, far superior) vs expanded flatland DOC. Soave Superiore DOCG from the classico. Pieropan proved Soave could be serious and age-worthy. Best examples age 8–10 years developing nutty complexity.",
    historical_context="Soave was Italy's most famous white wine export in the 1970s — then was massively over-expanded with inferior flat-land grapes, destroying its reputation. The classico zone producers have spent 40 years rebuilding credibility.")

R("Prosecco DOC / DOCG", "Italy", "wine", parent_id=veneto,
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=2,
    key_producers="Nino Franco, Bisol, Ruggeri, Adami, Col Vetoraz",
    description="Glera grape from hills northeast of Venice. Two quality tiers: Prosecco DOC (broad zone; Charmat/tank method; fresh, immediate) and Conegliano Valdobbiadene Prosecco Superiore DOCG (original hillside zone; Rive single-vineyard designation; Cartizze 107-hectare Grand Cru). Prosecco Col Fondo (ancestral method, naturally cloudy) is the artisan alternative. Prosecco now surpasses Champagne in global volume.",
    historical_context="The Prosecco DOCG was created in 2009. The Cartizze sub-zone (107 ha) was the original premium designation — grapes from its steep slopes are still the most expensive Prosecco fruit. The tank method (Charmat) was introduced in the 20th century to replace in-bottle refermentation.")

# ─── SPAIN ──────────────────────────────────────────────────────────────────
print("\n=== SPAIN ===")
R("Rioja DOCa", "Spain", "wine",
    reputation_tier="iconic", authority_tier=1,
    key_producers="López de Heredia, La Rioja Alta, CVNE, Muga, Roda, Artadi, Remírez de Ganuza",
    description="Spain's first DOCa (1991). Three sub-zones: Rioja Alta (Atlantic; Tempranillo dominant; elegance, age-worthiness), Rioja Alavesa (Basque; limestone; concentrated, mineral), Rioja Oriental/Baja (Mediterranean; Garnacha dominant; richer). Ageing classifications define legal identity: Joven (no oak requirement), Crianza (2 years min, 1 in oak), Reserva (3 years, 1 in oak), Gran Reserva (5 years, 2 in oak). Traditional style: American oak (vanilla, coconut). Modern: French oak, fresher fruit. BC importer: Authentic Wine & Spirits [NEEDS VERIFICATION].",
    historical_context="Rioja adopted Bordeaux winemaking techniques in the 1850s when Bordeaux vineyards were devastated by phylloxera and oidium. Bordeaux négociants (including the Rothschild representatives) crossed the Pyrenees, teaching barrel ageing in the Médoc tradition to Rioja producers.")

R("Ribera del Duero DO", "Spain", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Vega Sicilia, Pingus, Dominio de Pingus, Abadía Retuerta, Pesquera, Valbuena",
    description="High-altitude plateau (800–1000m) along the Duero. Extreme continental climate: blistering summer days, cold nights — preserves acidity. Tempranillo called Tinto Fino or Tinta del País locally. Darker, more structured than traditional Rioja. Vega Sicilia is Spain's most prestigious winery (Único aged 10+ years). Pingus (Peter Sisseck, Danish winemaker) is Spain's cult-wine leader. BC importer: Select Wine Merchants [NEEDS VERIFICATION].",
    historical_context="Vega Sicilia was planted in 1864 by Eloy Lecanda, who brought cuttings from Bordeaux after studying viticulture in France. The estate was considered the greatest in Spain but largely unknown internationally until the 1980s. Ribera del Duero DO was only granted in 1982.")

R("Priorat DOCa", "Spain", "wine",
    reputation_tier="iconic", quality_trajectory="ascending", authority_tier=1,
    key_producers="Álvaro Palacios (L'Ermita), Mas d'en Gil, Cims de Porrera, Ferrer Bobet, Clos Mogador",
    description="Spain's second DOCa after Rioja — tiny Catalan appellation. Llicorella soils (ancient black slate and mica schist) create extreme vine stress; yields 0.5–1 kg/vine. Old-vine Garnacha (Grenache) and Cariñena (Carignan) — many 70–100+ year old vines. Álvaro Palacios (L'Ermita — Spain's most expensive wine) pioneered the modern appellation from 1989. Style: black concentration, mineral iron, liquorice, tobacco, natural 14–17% ABV. BC importer: Vinos del Mundo [NEEDS VERIFICATION].",
    historical_context="Priorat was essentially abandoned by the early 1980s — fewer than 12 producers remained. Álvaro Palacios arrived in 1989 from Bordeaux training at Pétrus and within a decade had transformed Priorat into an international trophy appellation. The wine world refers to the 1990s Priorat revival as 'the resurrection.'")

R("Jerez DO", "Spain", "wine",
    reputation_tier="prestigious", quality_trajectory="rediscovering", authority_tier=1,
    key_producers="González Byass (Tío Pepe), Lustau, Valdespino, Equipo Navazos, Hidalgo-La Gitana",
    description="The sherry triangle: Jerez de la Frontera, Sanlúcar de Barrameda, El Puerto de Santa María. Albariza (white chalk) soils — best quality sites. Palomino Fino for dry styles; Pedro Ximénez for sweet. Two ageing pathways: biological (under flor yeast veil — Fino, Manzanilla, Amontillado) and oxidative (without flor — Oloroso, Palo Cortado). Solera system of fractional blending maintains house style. En Rama (unfiltered, seasonal release) is the benchmark of freshness. BC importer: Authentic Wine & Spirits [NEEDS VERIFICATION].",
    historical_context="Sherry has one of the oldest and most distinguished wine histories — the Phoenicians planted vines near Jerez in 1100 BCE. Shakespeare's Falstaff was an enthusiast. Nelson's body was preserved in a barrel of sherry for transport back to England after Trafalgar. The wine has an unbroken continuous tradition of 3,000 years.")

# ─── GREECE ─────────────────────────────────────────────────────────────────
print("\n=== GREECE ===")
R("Santorini PDO", "Greece", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending", authority_tier=1,
    key_producers="Domaine Sigalas, Hatzidakis, Gai'a, Estate Argyros, Domaine Santo",
    description="Volcanic Cycladic island. Assyrtiko from vines that burrow 15+ metres into volcanic pumice for moisture. The kouloura (basket-shaped) vine training — stems coiled flat to protect grapes from Aegean winds — is unique to Santorini. Volcanic soils (ash, pumice, basalt) are phylloxera-immune — many vines are 100–300+ year old ungrafted pre-phylloxera vines. Assyrtiko: extraordinary mineral salinity, electric acidity, lemon-citrus purity — the world's most minerally expressive white wine. Also Nykteri (barrel-aged Assyrtiko) and Vinsanto (sweet, sun-dried, barrel-aged). BC importer: La Fête du Vin [NEEDS VERIFICATION].",
    historical_context="Santorini's eruption circa 1600 BCE may have destroyed the Minoan civilisation. The island's wine tradition survived — the volcanic soils that killed Minoan civilization created the perfect substrate for great Assyrtiko vines. The phylloxera immunity of volcanic soils has preserved vine genetics found nowhere else in Europe.")

R("Naoussa PDO", "Greece", "wine",
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=1,
    key_producers="Kir-Yianni, Thymiopoulos, Domaine Dalamara, Boutari",
    description="Macedonia, northern Greece. Home of Xinomavro — 'acid black' — Greece's answer to Nebbiolo. High acid, high tannin, garnet colour with orange rim. Aged aromas: dried tomato, earth, leather, smoked meat. Mount Vermion slopes are the appellation's heartland. Thymiopoulos is the most critically acclaimed modern producer. Xinomavro ages 20+ years in the right hands — criminally undervalued internationally. BC importer: check locally with Greek specialty distributors [NEEDS VERIFICATION].",
    historical_context="Naoussa received PDO status in 1971 — the first PDO in Greece. Xinomavro was nearly replaced with French varieties in the 1970s until producers recognised the grape's unique identity and quality potential.")

R("Crete", "Greece", "wine",
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=2,
    key_producers="Lyrarakis, Douloufakis, Economou, Domaine Paterianakis",
    description="Greece's largest island, ancient wine-producing region. Revival of indigenous varieties: Vidiano (rich, textured white with tropical fruit and spice — the revelation of modern Greek winemaking), Kotsifali and Mandilaria (for reds). Tsikoudia/Raki (Cretan pomace spirit) is central to island identity — offered to guests as greeting, frames the meze table.",
    historical_context="Minoan Crete was the first significant wine-producing civilisation in Greece — wine storage vessels (pithoi) excavated at Knossos date to 2500 BCE. The Minoan trade routes spread wine culture throughout the ancient Mediterranean.")

# ─── LEBANON ─────────────────────────────────────────────────────────────────
print("\n=== LEBANON ===")
R("Bekaa Valley", "Lebanon", "wine",
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=1,
    key_producers="Château Musar, Château Ksara, Château Kefraya, Domaine des Tourelles",
    description="Lebanon's wine heartland — high-altitude valley (900–1100m) between the Lebanon and Anti-Lebanon mountain ranges. Continental climate: hot, dry summers, cold winters — ideal for Cabernet Sauvignon, Cinsault, Grenache, and local varieties. Château Musar (Serge Hochar) is the legend: Cabernet/Cinsault/Grenache blend that achieved iconic status globally, produced through civil war and Israeli invasions. Arak (triple-distilled grape spirit with anise) of the Bekaa is Lebanon's national drink. BC importer for Musar: Brix + Stone / Pacific Wine & Spirits [NEEDS VERIFICATION].",
    historical_context="Lebanon has the oldest continuous winemaking tradition in the world — the Phoenicians of Byblos spread viticulture throughout the Mediterranean circa 3000–1000 BCE. The ancient city of Baalbek (in the Bekaa Valley) had a temple to Bacchus. Wine production survived the Ottoman period and both World Wars.")

# ─── MOROCCO ─────────────────────────────────────────────────────────────────
print("\n=== MOROCCO ===")
R("Morocco", "Morocco", "traditional",
    reputation_tier="respected", quality_trajectory="ascending", authority_tier=2,
    key_producers="Les Celliers de Meknès, Domaine de la Zouina, Thalvin",
    description="North Africa's most significant wine producer and the cultural home of the Moroccan mint tea ceremony — one of the world's great ritual beverage traditions. Gunpowder green tea + fresh spearmint + sugar, served in three glasses ('the first is gentle as life, the second strong as love, the third bitter as death'), poured from height to aerate and cool. The silver teapot (tray-served to guests) is an icon of Maghrebi culture. Wine production centres in Meknès and the Marrakech/Benslimane zone. The country's tea culture connects to the Marseille Crossroads — North African tea culture met Provençal café culture in the port of Marseille.",
    historical_context="Morocco's tea ceremony tradition arrived with Sudanese trade routes in the 17th century. Gunpowder green tea was introduced by British traders in the 18th century — Morocco was never colonised by the British, who gained access through trade treaties. The specific three-glass ritual was formalised in the 19th century.")

# ─── TURKEY ─────────────────────────────────────────────────────────────────
print("\n=== TURKEY ===")
R("Turkey", "Turkey", "traditional",
    reputation_tier="respected", authority_tier=2,
    key_producers="Kavaklıdere, Doluca, Pamukkale Winery",
    description="Turkey bridges European and Asian coffee and wine culture. Anatolia is the genetic homeland of Vitis vinifera — wine was being made here 6,000+ years ago. Turkish coffee (prepared in the cezve/ibrik) is one of the world's great ceremonial beverages: ultra-fine grind, cold water start, three rises of foam, sugar added before brewing (sade/orta/şekerli). The ceremony represents the Ottoman empire's role in spreading coffee from Arabia to Europe through Constantinople. Also: Turkish Raki (pomace/grape spirit with anise — the Turkish equivalent of Lebanese arak and Greek ouzo).",
    historical_context="Coffee was brought to Constantinople from Yemen circa 1540 during the reign of Suleiman the Magnificent. The first coffeehouses (qahveh khane) opened in Istanbul in 1554 and became centres of intellectual and political life. The Ottoman empire spread the coffeehouse culture to Vienna (1683), Paris (1672), and London (1652). All European café culture descends from the Ottoman qahveh khane.")

cur.close()
conn.close()
print("\n✅ All European beverage regions inserted.")
