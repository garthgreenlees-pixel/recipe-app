#!/usr/bin/env python3
"""Mediterranean Session — Batch 3: Bordeaux
Producers, Products, beverage_references, pairing_intelligence.
Region IDs: Bordeaux=121, Médoc=122, Pauillac=123, Saint-Julien=124, Margaux=125,
Saint-Estèphe=126, Pessac-Léognan=127, Saint-Émilion=128, Pomerol=129, Fronsac=130.
"""
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, P, PROD, REF, PAIR, PROTOCOL

conn, cur = get_conn()

# ════════════════════════════════════════════════════════════════════════════════
# BORDEAUX PRODUCERS
# ════════════════════════════════════════════════════════════════════════════════
print("=== BORDEAUX PRODUCERS ===")

# Left Bank — Pauillac
lafite = P(cur, "Château Lafite Rothschild", "winery", 123, "France",
    production_philosophy="premier_cru_left_bank",
    philosophy_description="The most famous wine name in the world. The Rothschild family (Baron Eric de Rothschild until 2018, now Saskia de Rothschild) runs one of Bordeaux's most meticulous estates. The grand vin uses approximately 85% Cabernet Sauvignon. The second wine Carruades de Lafite was introduced in 1974 — now one of the most demanded second labels. The estate includes Château Duhart-Milon (Pauillac, 4th Growth) and Château l'Évangile (Pomerol). BC importer: Lifford Wine Agency / Select Wine Merchants [NEEDS VERIFICATION].",
    key_personnel=[{"role": "director", "name": "Saskia de Rothschild"}],
    production_details={"second_wine": "Carruades de Lafite", "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Lafite commands the highest average auction prices of any Bordeaux estate. The brand's mystique in Asian markets (China particularly) drove prices to extraordinary levels 2010–2015.",
    allocation_notes="By strict allocation. BC availability through restaurant allocation programs.",
    price_positioning="ultra_premium", authority_tier=1)

mouton = P(cur, "Château Mouton Rothschild", "winery", 123, "France",
    production_philosophy="artiste_premier_cru",
    philosophy_description="The only wine to be reclassified in the 1855 system — elevated from Second Growth to First Growth in 1973 by a decree of Jacques Chirac, then Agriculture Minister, at the request of Baron Philippe de Rothschild. The estate is famous for commissioning a different artist for each vintage label: Picasso (1973), Dalí (1958), Andy Warhol (1975), Balthus (1993), Lucian Freud (2006). Also home to the Mouton Rothschild wine museum. Cabernet Sauvignon dominant (90%+).",
    key_personnel=[{"role": "director", "name": "Philippe Sereys de Rothschild"}],
    production_details={"second_wine": "Le Petit Mouton", "label_artists": "commissioned annually",
                        "bc_importer": "Select Wine Merchants [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Baron Philippe de Rothschild's famous motto on elevation to First Growth: 'Premier je suis, second je fus, Mouton ne change' (First I am, Second I was, Mouton does not change — updating from the previous motto: Premier je fus, second je suis, Mouton ne change).",
    price_positioning="ultra_premium", authority_tier=1)

latour = P(cur, "Château Latour", "winery", 123, "France",
    production_philosophy="the_most_age_worthy",
    philosophy_description="The First Growth most respected for longevity. François Pinault (Kering luxury group) purchased Latour in 1993. In 2012, Latour withdrew from the en primeur (futures) system entirely — a landmark decision that changed the Bordeaux market. Now releases wines when deemed ready. The grand vin's 'Enclos' (the walled vineyard immediately around the tower) produces the most age-worthy Pauillac — 50-year bottles are the expectation, not the exception. Second wine: Les Forts de Latour (a wine in its own right, superior to many First Growths).",
    key_personnel=[{"role": "director", "name": "Frédéric Engerer"}],
    production_details={"second_wine": "Les Forts de Latour", "en_primeur": "withdrew 2012",
                        "bc_importer": "Lifford / Pacific Wine & Spirits [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Latour's withdrawal from the en primeur system was the most significant structural challenge to Bordeaux's futures market in its history. The 2012 decision caused other châteaux to consider the same; none of similar stature has followed.",
    price_positioning="ultra_premium", authority_tier=1)

margaux_ch = P(cur, "Château Margaux", "winery", 125, "France",
    production_philosophy="elegance_not_power",
    philosophy_description="The most perfumed and elegant First Growth. André Mentzelopoulos purchased the neglected estate in 1977 and transformed it over 20 years; his daughter Corinne Mentzelopoulos now runs it. The estate covers 800 hectares (only 87 planted to vines). The gravelly-sandy Margaux soils allow Cabernet Sauvignon to reach a perfumed elegance unmatched in the Médoc. The pavillon rouge (second wine) is one of Bordeaux's finest. The white Pavillon Blanc de Château Margaux is one of Bordeaux's finest whites (100% Sauvignon Blanc).",
    key_personnel=[{"role": "director", "name": "Corinne Mentzelopoulos"},
                   {"role": "winemaker", "name": "Philippe Bascaules"}],
    production_details={"second_wine": "Pavillon Rouge", "white_wine": "Pavillon Blanc",
                        "bc_importer": "Lifford Wine Agency [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

haut_brion = P(cur, "Château Haut-Brion", "winery", 127, "France",
    production_philosophy="urban_terroir",
    philosophy_description="The only non-Médoc château in the 1855 Classification (classified as First Growth). Located in what is now suburban Bordeaux (Pessac) — the vines are surrounded by urban development. The urban heat island effect and gravel-clay soils create an earlier-ripening microclimate unique in Bordeaux. The Dillon family (through Domaine Clarence Dillon) also owns La Mission Haut-Brion, Quintus (Saint-Émilion), and Clarendelle (entry-level range). The estate has been classified since 1855 and has never changed ownership in the Dillon era (since 1935).",
    key_personnel=[{"role": "director", "name": "Jean-Philippe Delmas"},
                   {"role": "owner", "name": "Prince Robert de Luxembourg"}],
    production_details={"bc_importer": "Select Wine Merchants [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

leoville_lascases = P(cur, "Château Léoville Las Cases", "winery", 124, "France",
    production_philosophy="super_second",
    philosophy_description="The leading 'Super Second' — a Second Growth (1855 classification) that consistently produces wine at First Growth quality. The Grand Enclos du Château de Léoville (the walled vineyard, a smaller, superior plot) is the source of the grand vin. Jean-Hubert Delon is the fiercely demanding proprietor. The second wine Clos du Marquis is itself considered one of Bordeaux's finest; the third wine La Petite Marquise was introduced for younger-drinking enjoyment.",
    key_personnel=[{"role": "director", "name": "Jean-Hubert Delon"}],
    production_details={"second_wine": "Clos du Marquis", "bc_importer": "Authentic Wine & Spirits [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Las Cases is consistently placed alongside the First Growths in comparative tastings. The 2000 vintage is considered a reference Bordeaux of the modern era.",
    price_positioning="ultra_premium", authority_tier=1)

ducru = P(cur, "Château Ducru-Beaucaillou", "winery", 124, "France",
    production_philosophy="saint_julien_precision",
    philosophy_description="The other leading Saint-Julien 'Super Second' alongside Las Cases. Bruno-Eugène Borie family. The château's name references the 'beautiful pebbles' (beaux cailloux) of the riverside gravel — the finest terroir in Saint-Julien. The wine is considered the most elegant and floral expression of Saint-Julien — more Margaux-like than Pauillac-like in character.",
    key_personnel=[{"role": "director", "name": "Bruno-Eugène Borie"}],
    production_details={"second_wine": "La Croix de Beaucaillou", "bc_importer": "Lifford [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

cos_destournel = P(cur, "Château Cos d'Estournel", "winery", 126, "France",
    production_philosophy="orientalist_saint_estephe",
    philosophy_description="Saint-Estèphe's most celebrated estate — the pagoda-topped château building is one of Bordeaux's most recognisable. The Michel Reybier family (through Taillan group) runs the estate. The wine is the most 'modern' and polished of the Saint-Estèphe First and Second Growths — rounder, more accessible than Montrose. The winemaking team uses gravity-flow and temperature-controlled fermentation with meticulous precision.",
    production_details={"second_wine": "Les Pagodes de Cos", "bc_importer": "Select Wine Merchants [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

# Right Bank — Pomerol
petrus = P(cur, "Château Pétrus", "winery", 129, "France",
    production_philosophy="merlot_absolute",
    philosophy_description="The most celebrated and expensive red wine in the world that has no official classification (Pomerol has never created a classification). The Moueix family (Jean-Pierre Moueix, now Jean-Claude Moueix) manages the estate. The defining soil is the plateau of blue clay in the centre of Pomerol — this clay's ability to retain water creates consistently riper Merlot while the Cabernet Franc that normally joins Merlot in Bordeaux rarely ripens well here. Harvested in the afternoon — the Pétrus team waits for morning dew to evaporate, then picks before the afternoon heat. Result: perfect physiological ripeness in every vintage. Also: no sorting table — every berry picked by hand to the standard required.",
    key_personnel=[{"role": "manager", "name": "Jean-Claude Moueix"}],
    production_details={"grapes": "100% Merlot in most vintages", "harvest": "afternoon picking only",
                        "bc_importer": "BCLDB special order / auction only [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="Pétrus 1947 is considered one of the two or three greatest wines ever made — 14% alcohol, residual sugar from incomplete fermentation, an almost port-like richness. The 1961, 1964, 1982, 2000, and 2009 are the modern era benchmarks.",
    allocation_notes="Essentially unobtainable commercially. Auction only for most collectors.",
    price_positioning="ultra_premium", authority_tier=1)

le_pin = P(cur, "Le Pin", "winery", 129, "France",
    production_philosophy="garage_wine_origin",
    philosophy_description="The world's most expensive wine per case. Jacques Thienpont (Belgian) purchased a 2.3-hectare estate in 1979 for almost nothing — at the time, Pomerol was not fashionable. The vineyard sits on sandy gravel with a pocket of clay. Merlot dominant. Thienpont's minimalist winemaking in a tiny garage operation produced wines that Robert Parker described as perfect (100 points) from the early 1980s. The term 'garage wine' derives from operations like Le Pin — small, unclassified, expensive. Fewer than 500 cases per year. BC: auction only.",
    key_personnel=[{"role": "proprietor", "name": "Jacques Thienpont"}],
    production_details={"production": "~500 cases/year", "bc_importer": "auction only"},
    quality_tier="reserve", reputation_narrative="Le Pin consistently sells for more per case than Pétrus at auction. The 1982 ($10,000+ per bottle) and 2009 are reference benchmarks. The concept of 'garage wines' (Garagiste movement in Saint-Émilion) was inspired by operations like Le Pin.",
    price_positioning="ultra_premium", authority_tier=1)

cheval_blanc = P(cur, "Château Cheval Blanc", "winery", 128, "France",
    production_philosophy="right_bank_first_growth",
    philosophy_description="The most unusual First Growth: Cabernet Franc dominant (typically 55–60%) — unusual for the Right Bank, where Merlot normally dominates. The sandy clay soils of Saint-Émilion's northwest sector suit Cabernet Franc exceptionally well. The 1947 vintage is considered by many experts the greatest wine ever produced — an extraordinary, almost-sweet concentration from a heat-stressed vintage fermented without temperature control. LVMH purchased Cheval Blanc along with Château d'Yquem in 1998.",
    key_personnel=[{"role": "CEO", "name": "Pierre-Olivier Clouet"}],
    production_details={"grape_blend": "~55% Cabernet Franc, 45% Merlot",
                        "bc_importer": "Mark Anthony Group / BCLDB [NEEDS VERIFICATION]"},
    quality_tier="reserve", reputation_narrative="The 1947 Cheval Blanc was fermented naturally during a brutal heat wave — the wine had 13.5% natural alcohol and 10+ g/L residual sugar from incomplete fermentation. Tasters describe it as 'voluptuous,' 'caramelised,' 'unlike any other wine.' Peter Koff (MS) describes it as the finest wine he has tasted in 40 years.",
    price_positioning="ultra_premium", authority_tier=1)

ausone = P(cur, "Château Ausone", "winery", 128, "France",
    production_philosophy="limestone_terroir_right_bank",
    philosophy_description="The other Saint-Émilion Premier Grand Cru Classé A alongside Cheval Blanc. Built on the limestone plateau of Saint-Émilion — the highest and most mineral terroir in the appellation. Alain Vauthier's family runs the estate; he famously forced a reclassification of the Saint-Émilion system in 2012 when Ausone's ranking was perceived as inadequate. Only 7,000 bottles per year of the grand vin. The wines are unusually structured, mineral, and age-worthy for Right Bank — needing 20+ years to open.",
    key_personnel=[{"role": "proprietor", "name": "Alain Vauthier"}],
    production_details={"production": "~7,000 bottles/year", "bc_importer": "Select Wine Merchants [NEEDS VERIFICATION]"},
    quality_tier="reserve", price_positioning="ultra_premium", authority_tier=1)

# ════════════════════════════════════════════════════════════════════════════════
# BORDEAUX PRODUCTS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BORDEAUX PRODUCTS ===")

lafite_vin = PROD(cur, "Château Lafite Rothschild", "wine_still", lafite, 123,
    subcategory="cabernet sauvignon blend",
    description="The world's most famous wine name. Pauillac First Growth. Typically 85–90% Cabernet Sauvignon, remainder Merlot and Petit Verdot. The style is the most refined and elegant of the Pauillac First Growths — pencil shavings, cedar, blackcurrant, violet, with remarkable finesse despite the structure. Needs 20–30 years of cellaring in great vintages (1982, 1986, 1996, 2000, 2003, 2005, 2009, 2010, 2022 are the benchmark years). BC importer: Lifford Wine Agency. CAD $1,500–$3,500 per bottle (recent vintages).",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "pencil shavings, cedar, blackcurrant, violet, subtle tobacco",
                       "palate": "medium-full body, elegant tannins, great length, 20–30 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60, "glass": "large Bordeaux tulip"},
    flavour_markers=["pencil shavings", "cedar", "blackcurrant", "violet", "tobacco leaf", "earth"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,500–$3,500")

mouton_vin = PROD(cur, "Château Mouton Rothschild", "wine_still", mouton, 123,
    subcategory="cabernet sauvignon blend",
    description="Pauillac First Growth. The most powerful and opulent of the First Growths — 90%+ Cabernet Sauvignon. More flamboyant than Lafite: dark fruit (cassis, blackberry), graphite, tobacco, new oak visible. The famous artist-labelled bottle makes it the world's most collected wine label (literal art collection value). 2009 and 2010 are considered the most perfect modern expressions. BC: Select Wine Merchants.",
    quality_tier="reserve",
    deductive_profile={"colour": "opaque garnet", "nose": "cassis, graphite, tobacco, new oak, dark spice",
                       "palate": "full body, powerful tannins, 25–40 year potential"},
    service_specs={"temp_c": 18, "decant_minutes": 90},
    flavour_markers=["cassis", "graphite", "tobacco", "new oak", "dark spice", "blackberry"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,200–$3,000")

latour_vin = PROD(cur, "Château Latour", "wine_still", latour, 123,
    subcategory="cabernet sauvignon blend",
    description="Pauillac First Growth — the most age-worthy wine in Bordeaux. The grand vin is produced only from the Enclos (the walled vineyard around the tower, 47 hectares). Withdrawn from en primeur since 2012 — released when deemed ready. The 1961, 1982, 2000, 2003, and 2010 are legendary. Needs minimum 20 years from vintage in good years, 35–50 in great years. The wine that most demands patience of all the First Growths.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep ruby-garnet, opaque when young", "nose": "blackcurrant, iron, graphite, cedar, earth",
                       "palate": "firm, structured, grip; 25–50 year potential in great years"},
    service_specs={"temp_c": 17, "decant_minutes": 90, "note": "can be served with a hard decant 2+ hours for young vintages"},
    flavour_markers=["blackcurrant", "iron", "graphite", "cedar", "earth", "tobacco"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,500–$4,000")

margaux_vin = PROD(cur, "Château Margaux Grand Vin", "wine_still", margaux_ch, 125,
    subcategory="cabernet sauvignon blend",
    description="The most perfumed and elegant First Growth — the 'feminine' Médoc. The gravelly Margaux soils produce Cabernet Sauvignon of unusual aromatic delicacy: violet, rose, cassis, cedar. Not the most powerful but the most seductive at any age. The 1900 is considered one of the greatest wines ever recorded. Modern benchmarks: 2000, 2009, 2010, 2015. The second wine Pavillon Rouge is consistently one of Bordeaux's finest second labels.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "violet, rose, cassis, cedar, earth — the most perfumed Médoc",
                       "palate": "silky, polished tannins; greatest elegance of the First Growths; 20–30 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["violet", "rose", "cassis", "cedar", "earth", "refined spice"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,200–$3,000")

haut_brion_vin = PROD(cur, "Château Haut-Brion", "wine_still", haut_brion, 127,
    subcategory="cabernet sauvignon blend",
    description="The only non-Médoc First Growth. Pessac-Léognan. Typically 45% Cabernet Sauvignon, 37% Merlot, 18% Cabernet Franc — the most Merlot-friendly blend of the First Growths. The wine has a distinctive earthy, smoky, even slightly roasted character unique to Pessac-Léognan's urban gravel soil. The Merlot component makes it the most approachable young First Growth, yet still ages 25–40 years. Also produces an exceptional dry white (Haut-Brion Blanc — often considered France's finest dry white after Le Montrachet).",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "earthy, smoky, tobacco, leather, blackcurrant — distinctive 'gravel terroir' character",
                       "palate": "rounder than Médoc First Growths due to Merlot; 20–35 year ageing"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["earthy", "smoky", "tobacco", "blackcurrant", "leather", "roasted notes"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,000–$2,500")

petrus_vin = PROD(cur, "Château Pétrus", "wine_still", petrus, 129,
    subcategory="merlot",
    description="The world's most famous Merlot and most expensive unclassified wine. 100% Merlot from blue clay in the centre of Pomerol. The wine is voluptuous, hedonistic, and immediately impressive even when young — yet also exceptionally long-lived (50+ years in great vintages). Key flavours: plum, truffle, chocolate, iron, violet, caramel with age. The 1947, 1961, 1964, 1982, 2000, 2009, and 2010 are the legendary vintages. Pétrus has no second wine — if not included in the grand vin, declassified entirely. BC: auction only.",
    quality_tier="reserve",
    deductive_profile={"colour": "opaque garnet-purple", "nose": "plum, truffle, chocolate, iron mineral, violet, new oak",
                       "palate": "extraordinary concentration; velvety tannins; 30–50 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["plum", "truffle", "chocolate", "iron mineral", "violet", "mocha"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$5,000–$20,000")

cheval_vin = PROD(cur, "Château Cheval Blanc", "wine_still", cheval_blanc, 128,
    subcategory="cabernet franc blend",
    description="Saint-Émilion's most unusual First Growth — Cabernet Franc dominant (55–60%), the only First Growth of the right bank to be structured around Franc rather than Merlot. The wine is the finest expression of Cabernet Franc in the world: violet, pencil shavings, earth, blackberry — with exceptional freshness and minerality from the sandy clay soils. The 1947 is one of the greatest wines ever made. Modern benchmarks: 2000, 2009, 2010, 2020.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "violet, pencil, earth, blackberry, subtle spice — classic Franc character",
                       "palate": "silky yet structured; less opulent than Pétrus; 20–40 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["violet", "pencil shavings", "earth", "blackberry", "subtle herb"],
    flavour_weight="full", flavour_profile_type="terroir_expressive",
    price_tier="ultra_premium", price_range_cad="$1,500–$4,000")

pavillon_blanc = PROD(cur, "Pavillon Blanc de Château Margaux", "wine_still", margaux_ch, 125,
    subcategory="sauvignon blanc",
    description="The remarkable dry white wine of Château Margaux — 100% Sauvignon Blanc from a parcel within the château estate. This is considered one of the three greatest Sauvignon Blancs in France (alongside Sancerre from top producers and certain Pouilly-Fumé). Rich, complex, oak-influenced, with a depth and weight that recalls great white Burgundy more than Loire Sauvignon. Barrel-fermented in new French oak. Ages 10–15 years. Extremely rare in BC.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep gold", "nose": "citrus, white flower, mineral, subtle oak, gunflint",
                       "palate": "rich, complex, oak-integrated; 10–15 year ageing"},
    service_specs={"temp_c": 13, "decant_minutes": 10},
    flavour_markers=["citrus", "white flower", "mineral", "gunflint", "oak", "tropical (with age)"],
    flavour_weight="full", flavour_profile_type="mineral",
    price_tier="ultra_premium", price_range_cad="$400–$700")

leoville_lc_vin = PROD(cur, "Léoville Las Cases Grand Clos", "wine_still", leoville_lascases, 124,
    subcategory="cabernet sauvignon blend",
    description="The leading 'Super Second' of Bordeaux — Saint-Julien Second Growth that regularly challenges the First Growths in comparative tastings. The Grand Enclos (walled plot) fruit produces the grand vin. Jean-Hubert Delon's exacting standards create a wine of extraordinary precision and longevity. 2016 and 2022 considered modern masterpieces. BC: Authentic Wine & Spirits [NEEDS VERIFICATION].",
    quality_tier="reserve",
    deductive_profile={"colour": "deep ruby", "nose": "cassis, cedar, graphite, tobacco, earth",
                       "palate": "firm structure, First Growth quality; 20–30 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["cassis", "cedar", "graphite", "tobacco", "earth"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$200–$400")

cos_vin = PROD(cur, "Cos d'Estournel", "wine_still", cos_destournel, 126,
    subcategory="cabernet sauvignon blend",
    description="Saint-Estèphe's finest wine — Second Growth in 1855 classification. More polished and approachable than Montrose, with a characteristic cedar, dark fruit, and structured tannic backbone typical of Saint-Estèphe's heavier clay soils. The wine has improved dramatically since the late 1990s and now consistently achieves prices close to the First Growths. The pagoda architecture of the château is Bordeaux's most iconic.",
    quality_tier="reserve",
    deductive_profile={"colour": "deep garnet", "nose": "cassis, cedar, dark spice, tobacco, earthier notes than Pauillac",
                       "palate": "full body, firm tannin structure, Saint-Estèphe clay character; 15–25 year potential"},
    service_specs={"temp_c": 17, "decant_minutes": 60},
    flavour_markers=["cassis", "cedar", "dark spice", "tobacco", "clay mineral"],
    flavour_weight="full", price_tier="ultra_premium", price_range_cad="$150–$300")

# ════════════════════════════════════════════════════════════════════════════════
# BORDEAUX REFERENCES
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BORDEAUX REFERENCES ===")

REF(cur,
    "Bordeaux — The 1855 Classification and the Classified Growths",
    "wine_regions",
    description="The 1855 Classification of the Médoc is the most famous wine hierarchy in existence — and the most controversial, because it has barely changed in 170 years despite enormous shifts in quality. Commissioned by Napoleon III for the 1855 Paris Exhibition, the classification ranked 61 Médoc châteaux (plus Château Haut-Brion) into five tiers of Cru Classé based on their market price at the time. Only one subsequent change: Mouton Rothschild elevated from Second to First Growth in 1973.",
    key_principles="""THE 1855 FIVE-TIER CLASSIFICATION:

PREMIER CRU (First Growth) — 5 estates:
1. Château Lafite Rothschild (Pauillac)
2. Château Mouton Rothschild (Pauillac) — elevated from 2nd to 1st in 1973
3. Château Latour (Pauillac)
4. Château Margaux (Margaux)
5. Château Haut-Brion (Pessac-Léognan) — the only non-Médoc inclusion

DEUXIÈME CRU (Second Growth) — 14 estates including: Léoville Las Cases, Léoville Poyferré, Léoville Barton, Gruaud Larose, Ducru-Beaucaillou (Saint-Julien); Cos d'Estournel, Montrose (Saint-Estèphe); Pichon-Longueville Baron, Pichon Longueville Comtesse (Pauillac); Rauzan-Ségla, Rauzan-Gassies (Margaux).

TROISIÈME CRU (Third Growth) — 14 estates: includes Palmer, Giscours, Kirwan, Malescot St-Exupéry (Margaux); La Lagune (Haut-Médoc); Langoa Barton (Saint-Julien).

QUATRIÈME CRU (Fourth Growth) — 10 estates: includes Duhart-Milon, Talbot (Saint-Julien).

CINQUIÈME CRU (Fifth Growth) — 18 estates: includes Lynch-Bages, Grand-Puy-Lacoste (Pauillac); Pontet-Canet (which has dramatically improved and now prices itself near Second Growth).

THE GREAT ANOMALIES:
1. POMEROL is not classified at all — the appellation never established a classification. Pétrus is unclassified yet worth more than any First Growth.
2. SAINT-ÉMILION has its own separate classification (revised periodically), using Grand Cru Classé A, B, and Grand Cru designations. Cheval Blanc and Ausone are Premier Grand Cru Classé A.
3. THE 'SUPER SECONDS': Several Second Growths (Las Cases, Ducru-Beaucaillou, Palmer, Cos d'Estournel, Montrose) consistently produce wines of First Growth quality. They command prices approaching the First Growths but without the formal ranking.

THE EN PRIMEUR SYSTEM (Futures):
Bordeaux sells wines 'en primeur' (as futures) while still in barrel — typically 18–24 months before bottling. Buyers pay now and receive the wine 2 years later. The system creates speculative pricing based on Parker/critics' barrel tastings. Latour withdrew from en primeur in 2012 — the most significant market challenge in decades.

THE PLACE DE BORDEAUX:
The Bordeaux trade system involves négociants (merchants) as intermediaries between châteaux and global buyers. Most First Growth and premium wine is sold through the Place de Bordeaux négociant network (Châteaux → Négociants → Importers → Retailers/Restaurants). This creates multiple layers of markup. Direct-to-consumer sales are essentially non-existent for the grandes maisons.""",
    skill_level="advanced", authority_tier=1,
    source_text="Bordeaux CIVB / WSET Diploma Level 4")

REF(cur,
    "Bordeaux — Left Bank vs Right Bank: The Two Philosophies",
    "wine_regions",
    description="The Gironde estuary divides Bordeaux into two philosophically distinct wine traditions. The Left Bank (Cabernet Sauvignon dominant) and Right Bank (Merlot dominant) are not merely stylistic differences but reflect fundamentally different soils, drainage, varieties, and winemaking approaches.",
    key_principles="""LEFT BANK (MÉDOC + PESSAC-LÉOGNAN):
SOIL: Deep gravel, gravel terraces over clay and sand. The gravel's rapid drainage forces vines to stress productively. The gravel also absorbs and reflects heat, accelerating ripening of late-maturing Cabernet Sauvignon.
DOMINANT VARIETY: Cabernet Sauvignon (typically 60–80% in the grand vin). Merlot is a secondary component for suppleness and early approachability.
STYLE: Firm structure, cassis-forward fruit, cedar, graphite, tobacco. Slow development — typically needs 10–20+ years of cellaring for the greatest expressions. The 'classic' Bordeaux style that the world has been trained to expect.
KEY APPELLATIONS: Pauillac, Saint-Julien, Margaux, Saint-Estèphe, Pessac-Léognan.
FIRST GROWTHS: Lafite, Mouton, Latour, Margaux, Haut-Brion.
AGEING POTENTIAL: 20–50+ years for the greatest vintages.

RIGHT BANK (SAINT-ÉMILION + POMEROL):
SOIL: Clay and limestone on the Saint-Émilion plateau; blue clay on the Pomerol plateau; gravel and sand in lower sections. The clay retains moisture and warmth — ideal for Merlot.
DOMINANT VARIETY: Merlot (typically 70–95%). Cabernet Franc provides backbone and aromatic lift. Cabernet Sauvignon rarely thrives in these cooler, wetter clay soils.
STYLE: Rounder, more immediately approachable, richer fruit character (plum, chocolate, violet). Earlier drinking than Left Bank but the finest examples (Pétrus, Cheval Blanc, Ausone) have extraordinary longevity.
KEY APPELLATIONS: Saint-Émilion, Pomerol, Fronsac.
GREAT ESTATES: Pétrus (unclassified), Cheval Blanc (PGCC A), Ausone (PGCC A), Le Pin.

THE GREAT VINTAGES:
Great years for BOTH banks: 1961, 1982, 2000, 2009, 2010, 2015, 2016, 2022.
Right Bank advantage (warmer, earlier ripening): 1964, 1971, 2012 (difficult Left Bank year).
Left Bank advantage (later-ripening Cabernet): 1986, 1996.
The vintage of the century debated between 1961 (post-frost, tiny crop, extraordinary concentration) and 2009 (perfect growing season, textbook ripeness).

BORDEAUX BLENDING PHILOSOPHY:
Traditional Bordeaux blending adds Merlot to Cabernet for softness, Cabernet Franc for herbal lift, Petit Verdot for colour and spice, Malbec for body (now rare). The blend is calibrated annually to the vintage conditions — no fixed percentages. This flexibility is why Bordeaux produces good wine in difficult years where Burgundy might fail: a hot year sees more Merlot in the blend; a wet year sees less.

THE GARAGE WINE MOVEMENT (Garagistes):
From the 1990s, small-production, micro-managed, cult wines emerged in Saint-Émilion and Pomerol — inspired by Le Pin's success. Notable: Valandraud (Jean-Luc Thunevin), La Mondotte. These wines used radical techniques (micro-oxygenation, very low yields, 100% new oak) to create concentrated, high-scoring wines from modest classified or unclassified sites. The movement challenged the established hierarchy and created a new category of collectors.""",
    skill_level="advanced", authority_tier=1,
    source_text="Jancis Robinson MW / Oz Clarke / WSET Diploma")

# ════════════════════════════════════════════════════════════════════════════════
# BORDEAUX PAIRINGS
# ════════════════════════════════════════════════════════════════════════════════
print("\n=== BORDEAUX PAIRINGS ===")

# Lafite
PAIR(cur, "Roast rack of lamb with rosemary jus and gratin dauphinois", "main", "main",
     "classic", "complement",
     "The textbook Médoc pairing: lamb's relatively lean fat and herb character perfectly mirrors Pauillac's cedar-cassis-tobacco profile. The rosemary echoes the wine's tertiary herbal notes; the potato gratin provides the starchy body to absorb the tannin structure. This pairing is encoded in French culinary consciousness.",
     lafite_vin)

PAIR(cur, "Roasted leg of Pauillac lamb with haricots verts and fleur de sel", "main", "main",
     "classic", "complement",
     "The Pauillac AOP lamb (raised on the salt marshes near the château) is the ultimate terroir pairing — the lamb literally grazes the same region as the vines. The salt-marsh grass imparts a distinctive iodine character that mirrors the wine's mineral backbone. A pairing of perfect geographical completeness.",
     lafite_vin)

# Latour
PAIR(cur, "Côte de boeuf aged 45 days with béarnaise and bone marrow", "main", "main",
     "classic", "complement",
     "Château Latour — the most powerful, age-worthy Pauillac — demands red meat of equivalent structure. Aged côte de boeuf provides the fat, protein, and intensity to absorb Latour's formidable tannic architecture. Bone marrow adds unctuous richness; béarnaise provides herbal-acid counterpoint.",
     latour_vin)

# Pétrus
PAIR(cur, "Truffle risotto with aged Parmigiano-Reggiano", "main", "main",
     "classic", "bridge",
     "Pétrus's truffle-chocolate-iron profile meets black truffle's earthy umami richness. The risotto's creamy starchy body tames the wine's weight; Parmigiano's crystalline sharpness provides textural contrast. A pairing that emphasises Pétrus's earthy nobility rather than its fruit.",
     petrus_vin)

PAIR(cur, "Roasted duck breast with cherry reduction and Périgord truffle", "main", "main",
     "classic", "complement",
     "Merlot-dominant Pétrus loves duck — the bird's rich fat and slight sweetness are natural complements to the wine's plum and chocolate character. The cherry reduction mirrors the wine's fruit; truffle amplifies its tertiary earthiness.",
     petrus_vin)

# Cheval Blanc
PAIR(cur, "Roasted pigeon with foie gras, lentils, and rosemary jus", "main", "main",
     "classic", "complement",
     "Cabernet Franc dominant Cheval Blanc's violet-pencil character aligns perfectly with pigeon's subtly gamey richness. The foie gras adds luxury fat; lentils provide earthy minerality; rosemary echoes the Franc's herbaceous lift. A pairing of extreme elegance.",
     cheval_vin)

# Haut-Brion
PAIR(cur, "Grilled côtelettes d'agneau with truffle jus and spring vegetables", "main", "main",
     "classic", "complement",
     "Haut-Brion's distinctive smoky-earthy character (from Pessac-Léognan's urban gravel) is amplified by the smokiness of grilled lamb. The truffle jus bridges the wine's tertiary character; spring vegetables add freshness to balance the wine's weight.",
     haut_brion_vin)

print("\n✅ Bordeaux batch complete.")
cur.close()
conn.close()
