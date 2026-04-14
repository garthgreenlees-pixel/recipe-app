#!/usr/bin/env python3
"""Mediterranean Session — Batch 4: Rhône Valley
Producers, Products, beverage_references, pairing_intelligence.
Region IDs: Rhône Valley=131, Northern Rhône=132, Côte-Rôtie=133, Hermitage=134,
Cornas=135, Saint-Joseph=136, Condrieu=137, Southern Rhône=138,
Châteauneuf-du-Pape=139, Gigondas=140, Vacqueyras=141, Tavel=142.
"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PAIR

conn, cur = get_conn()

# ════════════════════════════════════════════════════════════════════════════════
# RHÔNE PRODUCERS
# ════════════════════════════════════════════════════════════════════════════════
print("=== RHÔNE PRODUCERS ===")

guigal = P(cur, "E. Guigal", "winery", 133, "France",
    production_philosophy="northern_rhone_pioneer",
    philosophy_description="The most famous and commercially important Rhône producer. Marcel Guigal took a small négociant operation started by his father Étienne in 1946 and built it into the dominant Rhône house. The 'la-las' (La Mouline, La Landonne, La Turque — the three single-vineyard Côte-Rôtie) are aged 42 months in new oak and released ~5 years after vintage. They are consistently among France's most allocated wines and have driven global interest in Syrah and the Northern Rhône. Also produces Côtes du Rhône at the other end of the range — a reference value Rhône.",
    key_personnel=[{"role": "winemaker/director", "name": "Philippe Guigal"},
                   {"role": "founder", "name": "Marcel Guigal"}],
    production_details={"flagship": "La Mouline / La Landonne / La Turque (Côte-Rôtie)",
                        "bc_importer": "Mark Anthony Group [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Marcel Guigal received the Decanter Man of the Year award in 2000 — the only négociant-producer in the award's history to be so recognised. The la-las are among the most sought-after French wines after DRC.",
    price_positioning="ultra_premium", authority_tier=1)

chave = P(cur, "Domaine Jean-Louis Chave", "winery", 134, "France",
    production_philosophy="hermitage_absolute",
    philosophy_description="The reference Hermitage estate — arguably the Northern Rhône's equivalent of DRC for the absolute benchmark of the appellation. The Chave family has made Hermitage since 1481 (one of the oldest continuous wine-producing family estates on earth). Jean-Louis Chave is the current winemaker and winemaking perfectionist. The Hermitage rouge is a blend of multiple lieux-dits across the hill — Chave owns parcels in Le Méal, L'Ermite, Le Bessards, and others. He blends them annually for the grand vin and reserves the finest for Cathelin (an extraordinary single-vineyard cuvée made only in exceptional years: 1990, 1991, 1995, 1998, 2003, 2013, 2015).",
    key_personnel=[{"role": "winemaker", "name": "Jean-Louis Chave"}],
    production_details={"parcels": "Le Méal, L'Ermite, Le Bessards, others",
                        "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Chave Hermitage Cathelin is one of the rarest wines in the world — produced fewer than 10 times in 40 years. Chave Hermitage rouge is the baseline reference for Northern Rhône Syrah.",
    price_positioning="ultra_premium", authority_tier=1)

chapoutier = P(cur, "Chapoutier", "winery", 134, "France",
    production_philosophy="biodynamic_rhone",
    philosophy_description="One of the great Rhône négociant-domaine houses, converting to biodynamics in 1991 — the first major Rhône producer to do so. Michel Chapoutier (the current generation) is a charismatic figure who has taken Chapoutier to Australia (Pyrenees) and Portugal. The single-vineyard Ermitage bottlings (Le Méal, L'Ermite, Le Pavillon) are produced in tiny quantities and aged without fining or filtration. The labels are written in both French and Braille — a personal commitment to accessibility.",
    key_personnel=[{"role": "director", "name": "Michel Chapoutier"}],
    production_details={"farming": "biodynamic", "bc_importer": "Authentic Wine & Spirits [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

clape = P(cur, "Domaine Auguste Clape", "winery", 135, "France",
    production_philosophy="cornas_tradition",
    philosophy_description="The patriarch producer of Cornas — Auguste Clape (now his son Pierre-Marie and grandson Olivier) represents the traditional approach to the most rustic Northern Rhône appellation. Old vines (some over 80 years), whole-cluster fermentation, old wood ageing, no fining or filtration. The wines need 10+ years of cellaring to reveal their extraordinary complexity. The Cornas Renaissance (young-vine cuvée) is an accessible entry point. The Clape family epitomises Cornas: the wines are almost brutally austere when young — dense, tannic, peppery — but magnificent at 15–25 years.",
    key_personnel=[{"role": "winemaker", "name": "Olivier Clape"}],
    production_details={"bc_importer": "Classic Wine Imports [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

château_rayas = P(cur, "Château Rayas", "winery", 139, "France",
    production_philosophy="grenache_absolute",
    philosophy_description="The most idiosyncratic and celebrated estate in Châteauneuf-du-Pape. The Reynaud family has run Rayas for generations. Emmanuel Reynaud (current winemaker) is reclusive, rarely seen in public, and the château itself is deliberately obscure in location. The wine is produced from 100% Grenache — when most Châteauneuf blends Grenache with Mourvèdre, Syrah, and others, Rayas insists on pure Grenache from old vines (30–90+ years) planted in unusual sandy soils that produce naturally lower yields. The result is one of the world's most ethereal red wines — not the densest or most powerful but the most translucent expression of southern Grenache. The white Rayas Châteauneuf-du-Pape Blanc is equally celebrated.",
    key_personnel=[{"role": "winemaker", "name": "Emmanuel Reynaud"}],
    production_details={"grapes": "100% Grenache", "soils": "sandy — unusual for Châteauneuf",
                        "bc_importer": "Pacific Wine & Spirits / Cas-Dri [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Rayas is often compared to DRC and Pétrus for its cult status and essentially unobtainable allocation. Emmanuel Reynaud is as reclusive as the wine is celebrated. Prices have risen 500% in the last decade.",
    allocation_notes="Essentially unobtainable. Auction or specialist allocation only.",
    price_positioning="ultra_premium", authority_tier=1)

beaucastel = P(cur, "Château Beaucastel", "winery", 139, "France",
    production_philosophy="mourvèdre_southern_rhone",
    philosophy_description="The most complex and age-worthy Châteauneuf-du-Pape from a classically structured estate. The Perrin family (fifth generation) grows all 13 permitted varieties — the most traditional approach in the appellation. Mourvèdre is the backbone variety (30% — extraordinary for the southern Rhône, where Grenache usually dominates). The result is Châteauneuf of exceptional longevity: 20–40 years. The Hommage à Jacques Perrin (a super-concentrated, Mourvèdre-dominant cuvée) is produced in exceptional years. Also produces excellent whites (Roussanne old vines) and the value Côtes du Rhône (Coudoulet de Beaucastel).",
    key_personnel=[{"role": "director", "name": "Marc Perrin"}, {"role": "director", "name": "Mathieu Perrin"}],
    production_details={"grapes": "all 13 permitted varieties; Mourvèdre 30% backbone",
                        "bc_importer": "Pacific Wine & Spirits [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

jaboulet = P(cur, "Paul Jaboulet Aîné", "winery", 134, "France",
    production_philosophy="hermitage_la_chapelle",
    philosophy_description="Historic Rhône négociant house, founded in 1834. The legendary La Chapelle (Hermitage rouge) is named after the small chapel at the top of the Hermitage hill. The 1961 La Chapelle is considered one of the greatest wines of the 20th century — still extraordinary at 60 years of age. The Frey family purchased Jaboulet in 2006 after decades of commercial compromise, and quality has been dramatically restored under Jean-Luc Thunevin's guidance.",
    production_details={"flagship": "La Chapelle (Hermitage rouge)", "bc_importer": "Pacific Wine & Spirits [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

vernay = P(cur, "Domaine Georges Vernay", "winery", 137, "France",
    production_philosophy="condrieu_guardian",
    philosophy_description="The estate that saved Condrieu from extinction. In the 1960s, only 15 hectares of Condrieu remained — Georges Vernay ('the guardian of Condrieu') almost single-handedly replanted and promoted the appellation. Now run by daughter Christine Vernay. The Coteau de Vernon single-vineyard Condrieu (from 70+-year-old vines on the most extreme slopes) is the reference single-vineyard Viognier in the world.",
    key_personnel=[{"role": "winemaker", "name": "Christine Vernay"}],
    production_details={"bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="premium", authority_tier=1)

# ════════════════════════════════════════════════════════════════════════════════
# RHÔNE PRODUCTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== RHÔNE PRODUCTS ===")

guigal_la_mouline = PROD(cur, "Guigal La Mouline Côte-Rôtie", "wine_still", guigal, 133,
    subcategory="syrah viognier blend",
    description="The most perfumed and elegant of Guigal's three single-vineyard 'la-las.' La Mouline is from the Côte Blonde — sandier, paler soil — with 11% Viognier co-fermented with the Syrah. The Viognier co-fermentation adds a violet-apricot perfume that is unmistakeable in great vintages. Aged 42 months in 100% new oak — yet the wine absorbs this without domination due to its extraordinary fruit extract and concentration. Produced in approximately 3,000 bottles per year. BC: allocation through Mark Anthony Group.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet-purple", "nose": "violet, apricot, bacon, olive, dark cherry — the Viognier co-ferment is distinctive",
                       "palate": "most silky of the la-las; 20–30 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["violet", "apricot", "bacon fat", "olive", "dark cherry", "spice"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$500–$1,500")

guigal_la_landonne = PROD(cur, "Guigal La Landonne Côte-Rôtie", "wine_still", guigal, 133,
    subcategory="syrah",
    description="The most powerful and structured of Guigal's la-las. La Landonne is from the Côte Brune — iron-rich, schist-clay soils. 100% Syrah (no Viognier). Dark, dense, almost inky in youth. The wine represents the iron-muscular side of Northern Rhône Syrah. 42 months in new oak. Needs 20+ years minimum. Only produced in certain vintages — not made in lighter years. ~3,000 bottles per year.",
    quality_tier="reserve",
    deductive_profile={"colour": "opaque purple-garnet", "nose": "iron, graphite, dark fruit, bacon, earth, game",
                       "palate": "massive tannin structure, full body, 25–40 year potential"},
    service_specs={"temp_c": 18, "decant_minutes": 90},
    flavour_markers=["iron", "graphite", "dark cherry", "bacon", "earth", "game"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$500–$1,200")

chave_hermitage_r = PROD(cur, "Chave Hermitage Rouge", "wine_still", chave, 134,
    subcategory="syrah",
    description="The reference Hermitage — a blend of multiple lieux-dits across the Hermitage hill, unified annually by Jean-Louis Chave's genius. The wine is the most complete expression of Northern Rhône Syrah: granite mineral backbone, dark fruit, olive tapenade, pepper, smoked meat, extraordinary length. Needs 15–20 years minimum; outstanding examples age 40–60 years. The 1990, 1991, 1995, 1998, 2003, 2010, 2015 are the modern benchmarks. BC: Lifford.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "granite mineral, dark cherry, olive, white pepper, smoked meat, earth",
                       "palate": "full body, firm granite tannins, extraordinary length; 15–40 year ageing"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["granite mineral", "dark cherry", "olive tapenade", "white pepper", "smoked meat", "graphite"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$200–$500")

jaboulet_la_chapelle = PROD(cur, "Jaboulet La Chapelle Hermitage", "wine_still", jaboulet, 134,
    subcategory="syrah",
    description="One of the most celebrated Hermitage wines — the 1961 La Chapelle is consistently cited among the greatest red wines ever produced. Paul Jaboulet Aîné's flagship, produced from old-vine Syrah on the Hermitage hill. Named for the small chapel at the summit. The wine demonstrates the best of structured, age-worthy Northern Rhône Syrah: dark fruit, iron, granite mineral, smoked meat, exceptional length. Great vintages: 1961, 1978, 1990, 2010, 2015, 2019. BC: Pacific Wine & Spirits.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "dark berry, iron, graphite, smoked meat, pepper",
                       "palate": "structured, tannic, 20–40 year potential in great vintages"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["dark berry", "iron", "graphite", "smoked meat", "white pepper"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$100–$300")

clape_cornas = PROD(cur, "Clape Cornas", "wine_still", clape, 135,
    subcategory="syrah",
    description="The reference Cornas — the most complete expression of this powerful, rustic appellation. Auguste Clape established the template: dense Syrah from old granite vines, traditional maceration, old-barrel ageing, no fining or filtration. The wine is almost brutally austere when young (3–5 years from vintage) — dark, inky, peppery, tannic. At 15–25 years, extraordinary complexity emerges: dark fruit, game, earth, iron, liquorice. An essential reference for tannin management education. BC: Classic Wine Imports.",
    quality_tier="reserve",
    deductive_profile={"colour": "opaque dark garnet", "nose": "dark cherry, game, earth, iron, white and black pepper",
                       "palate": "massive tannins young; extraordinary depth at 15+ years"},
    service_specs={"temp_c": 17, "decant_minutes": 90, "note": "requires 10+ years cellaring before drinking"},
    flavour_markers=["dark cherry", "game", "earth", "iron", "black pepper", "liquorice"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$80–$150")

rayas_rouge = PROD(cur, "Château Rayas Châteauneuf-du-Pape Rouge", "wine_still", château_rayas, 139,
    subcategory="grenache",
    description="The most ethereal expression of Southern Rhône Grenache. 100% old-vine Grenache from sandy soils — which create naturally lower yields and translucent wines. Unlike most Châteauneuf (dark, concentrated, Mediterranean power), Rayas is pale, almost translucent, perfumed, and otherworldly in its delicacy. The wine confounds all expectations of Southern Rhône: raspberry, rose, garrigue, iron. Vintage variation is extreme — only a perfect year produces the grand Rayas. BC: essentially auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "pale garnet — shockingly pale for Châteauneuf", "nose": "raspberry, rose, garrigue, iron mineral — ethereal",
                       "palate": "lighter body than expected; silky tannins; 20–35 year ageing"},
    service_specs={"temp_c": 16, "decant_minutes": 30},
    flavour_markers=["raspberry", "rose petal", "garrigue", "iron", "wild herb", "tea rose"],
    flavour_weight="medium", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$500–$2,000")

beaucastel_rouge = PROD(cur, "Beaucastel Châteauneuf-du-Pape Rouge", "wine_still", beaucastel, 139,
    subcategory="grenache mourvèdre blend",
    description="The most complex and age-worthy classic-style Châteauneuf-du-Pape. The Perrin family's 30% Mourvèdre backbone creates a wine of structure and longevity unusual in the Southern Rhône. Full 13 permitted varieties in the blend. The wine has a distinctive 'animal' quality (from Mourvèdre's signature leather/game character) plus spice, garrigue, dark fruit, and Provençal herb. Needs 10–15 years minimum; outstanding in great vintages (1981, 1989, 1990, 2000, 2009, 2010, 2016). BC: Pacific Wine & Spirits.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "dark fruit, leather, garrigue, spice, Provençal herb, animal character",
                       "palate": "full body, structured Mourvèdre tannin, 15–30 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["dark fruit", "leather", "garrigue", "Provençal herb", "spice", "animal character"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$80–$200")

vernay_coteau = PROD(cur, "Vernay Coteau de Vernon Condrieu", "wine_still", vernay, 137,
    subcategory="viognier",
    description="The reference single-vineyard Condrieu — from 70+-year-old vines on the Coteau de Vernon, the most extreme slope. Pure Viognier from granite. Apricot, white peach, violet, white blossom, and a rich but not heavy palate. The Vernay family's dedication to these steep, almost-abandoned terraces has been the model for Condrieu's revival. Drink within 5–7 years of vintage for maximum aromatic freshness, though it can age longer. BC: Lifford.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep gold", "nose": "apricot, white peach, violet, white blossom, rich and perfumed",
                       "palate": "rich but not heavy; generous fruit; 5–7 year drinking window"},
    service_specs={"temp_c": 13, "decant_minutes": 0},
    flavour_markers=["apricot", "white peach", "violet", "white blossom", "honeysuckle"],
    flavour_weight="full", flavour_profile_type="varietal_dominant",
    price_tier="ultra_premium", price_range_cad="$80–$150")

# ════════════════════════════════════════════════════════════════════════════════
# RHÔNE REFERENCES
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== RHÔNE REFERENCES ===")

REF(cur,
    "Northern Rhône — Syrah and the Granite Terroir",
    "wine_regions",
    description="The Northern Rhône is Syrah's spiritual homeland — a narrow corridor of steep granite terraces and schist slopes where Syrah reaches its most intellectual, mineral, and age-worthy expression. Unlike the warm, generous Southern Rhône Syrah or the fruit-forward New World expressions, Northern Rhône Syrah is characterised by its granite minerality, iron backbone, peppery spice, and earned complexity.",
    key_principles="""THE GRANITE DIFFERENCE:
Northern Rhône soils are predominantly granite (with schist in some areas). Granite drains rapidly, retains heat, and forces vine roots deep for water and nutrients. The result: low yields, concentrated fruit, high acidity, and a distinctive mineral-iron character that never appears in warmer, richer soils.

VIOGNIER CO-FERMENTATION:
Côte-Rôtie may co-ferment up to 20% Viognier with Syrah. This is legally permitted and produces wines of greater perfume, floral lift, and aromatic complexity. Guigal's La Mouline uses 11% Viognier — the most famous co-fermented example. The Viognier does not add sweetness or body but instead contributes aroma molecules (linalool, nerol) that enhance the wine's floral character. This technique is one of the world's oldest documented wine production practices.

THE LIEUX-DITS OF HERMITAGE:
Hermitage is a single hill divided into named plots (lieux-dits):
- Les Bessards (the heaviest, most tannic — granite and sand, dark fruit and iron)
- Le Méal (the most complete — warm, structured, deep)
- L'Ermite (the finest, most ethereal — shallow schist at the summit)
- La Chapelle (the Jaboulet monopole — rich, generous)
- Les Rocoules / Chante-Alouette (white wine — Marsanne and Roussanne)
Jean-Louis Chave blends from multiple plots annually; Chapoutier produces single-lieu-dit bottlings.

SYRAH PEPPERY CHARACTER:
The distinctive pepper-spice note in Northern Rhône Syrah (black pepper, white pepper, cracked black pepper) is not from oak but from a naturally occurring compound: rotundone. Rotundone is found at higher concentrations in Syrah grown in cooler climates and granite soils. It is the wine world's clearest example of a variety-specific aromatic compound expressing terroir.

THE NORTHERN RHÔNE STYLE GRADIENT (north to south):
Côte-Rôtie: Most elegant, Viognier-influenced, earliest drinking (10–25 years)
Condrieu: White only — Viognier, aromatic, drink 3–7 years
Saint-Joseph: Most accessible red, good value, 8–15 years
Hermitage: The summit — the most structured and age-worthy (20–60 years)
Cornas: The most rustic, most masculine, most tannic (15–30 years)
Crozes-Hermitage: The broad zone around Hermitage — good value introduction to the style""",
    skill_level="advanced", authority_tier=1,
    source_text="Clive Coates MW / Jancis Robinson / WSET Diploma")

REF(cur,
    "Châteauneuf-du-Pape — The 13 Varieties and Southern Rhône Complexity",
    "wine_regions",
    description="Châteauneuf-du-Pape is the most complex wine appellation in France by the number of permitted grape varieties — 13 (or 18 counting both red and white variants). The appellation also permits three colours (red, white, rosé) and has the most complex soil mosaic in the Rhône. It is the textbook example of Mediterranean wine character and the reference for understanding Southern Rhône blending.",
    key_principles="""THE 13 PERMITTED VARIETIES:
Red: Grenache Noir (dominant — typically 60–80%), Syrah, Mourvèdre, Cinsault, Muscardin, Counoise, Vaccarèse, Terret Noir
White: Grenache Blanc, Clairette, Bourboulenc, Picpoul, Roussanne (Picardin and Ugni Blanc were permitted until 2009)

THE SOIL TYPES:
Châteauneuf is not a single terroir — it is a mosaic of soils:
1. GALETS ROULÉS: The famous rounded river pebbles — absorb heat during day, release at night, reducing diurnal temperature variation. Found mainly in the north and centre of the appellation.
2. SABLES (SANDS): Lighter sandy soils in the south (including Château Rayas). Lower yields, more translucent wines, faster ripening.
3. ARGILO-CALCAIRE (CLAY-LIMESTONE): Red clay with limestone — structured, mineral wines with good acidity.
4. BLUE CLAY: Less common; found near Courthézon — deep, structured wines.

THE GRENACHE CHARACTER:
Grenache (Garnacha) is the backbone of Southern Rhône: high alcohol (naturally 14–16% in warm years), spiced red fruit (raspberry, cherry, garrigue), earthy, low tannin, and susceptible to oxidation without winemaking care. The finest old-vine Grenache (Rayas, Vieux Télégraphe, Clos des Papes) achieves extraordinary complexity and longevity.

MOURVÈDRE'S ROLE:
Mourvèdre (Monastrell in Spain) adds tannin, structure, and the distinctive 'animal' character (leather, game, forest floor) that distinguishes classically-styled Châteauneuf from simple Grenache fruit bombs. Beaucastel (30% Mourvèdre) is the greatest example of Mourvèdre's contribution to Châteauneuf complexity and longevity.

THE GALETS ROULÉS MYTH:
The popular belief that galets roulés heat-radiate and ripen grapes overnight is partially incorrect. Research shows the stones reflect light upward during the day rather than storing significant heat. The stones more importantly aid drainage and prevent surface erosion. The wines from galets zones (Père Caboche, La Nerthe) tend to be more structured and mineral than the sandy zones.

CHÂTEAUNEUF SERVICE:
Temperature: 16–17°C. Decant young examples (under 10 years) for 45–60 minutes. Older expressions may show better with a brief decant (30 minutes). Mourvèdre-dominant styles (Beaucastel) need more time than Grenache-dominant (Rayas) — the tannin structure requires oxidation to soften.

BC IMPORTERS: Pacific Wine & Spirits, Authentic Wine & Spirits handle most Châteauneuf in BC.""",
    skill_level="advanced", authority_tier=1,
    source_text="Robert Parker / Wine Advocate / WSET Diploma")

# ════════════════════════════════════════════════════════════════════════════════
# RHÔNE PAIRINGS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== RHÔNE PAIRINGS ===")

PAIR(cur, "Grilled côte de boeuf with tapenade crust and ratatouille", "main", "main",
     "classic", "complement",
     "Côte-Rôtie La Mouline's violet-apricot-bacon character aligns perfectly with grilled beef's Maillard crust. The olive tapenade mirrors the wine's olive tapenade note (a characteristic of co-fermented Viognier Syrah). The ratatouille's Mediterranean vegetables echo the Southern French context.",
     guigal_la_mouline)

PAIR(cur, "Venison loin with black truffle and bitter chocolate jus", "main", "main",
     "classic", "complement",
     "La Landonne's iron-graphite-game character is perfectly suited to venison — the gamey red meat amplifies the wine's natural game notes. Black truffle bridges the wine's earthiness; bitter chocolate in the jus mirrors the wine's dark intensity without sweetness.",
     guigal_la_landonne)

PAIR(cur, "Braised lamb shoulder with olive, rosemary, and flageolet beans", "main", "main",
     "classic", "complement",
     "Chave Hermitage's granite-mineral-olive-pepper character finds its natural pairing in slow-braised lamb. Olive and rosemary echo the wine's Provençal character; flageolet beans provide starchy body to absorb the formidable tannin structure.",
     chave_hermitage_r)

PAIR(cur, "Slow-roasted wild boar with black olive jus and polenta", "main", "main",
     "classic", "complement",
     "Clape Cornas's brutal tannic power demands food of equivalent weight and intensity. Wild boar's gamey richness and the black olive jus mirror the wine's iron-earthy-game character. The polenta provides the necessary starchy body to soften the tannin grip.",
     clape_cornas)

PAIR(cur, "Roasted whole chicken with garrigue herbs and aioli", "main", "main",
     "classic", "complement",
     "Château Rayas's pale, translucent Grenache paradox: despite its ethereal delicacy, it has the structure for fine poultry. Whole chicken's fat and sweet meat balance Rayas's fine tannin; garrigue herbs (thyme, lavender, rosemary) are a direct mirror of the wine's herbal terroir signature.",
     rayas_rouge)

PAIR(cur, "Roast Provençal lamb (gigot) with lavender and tapenade", "main", "main",
     "classic", "complement",
     "Beaucastel's Mourvèdre-animal-garrigue character meets Provençal lamb — a perfect geographical and flavour alignment. The lavender echoes the wine's floral depth; tapenade mirrors the wine's olive-earthy backbone. The most classically Mediterranean of all Rhône pairings.",
     beaucastel_rouge)

PAIR(cur, "Seared langoustine with apricot beurre blanc and chervil", "fish_course", "fish_course",
     "classic", "complement",
     "Condrieu's apricot-white peach-blossom character (pure Viognier) is the natural companion to langoustine's sweet, delicate flesh. The apricot beurre blanc creates an almost self-referential mirror. The chervil adds anise-herbal lift that amplifies the wine's aromatics.",
     vernay_coteau)

print("\n✅ Rhône batch complete.")
cur.close()
conn.close()
