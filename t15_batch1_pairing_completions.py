#!/usr/bin/env python3
"""Terminal 15 — Batch 1: Second pairings for all products with only 1 pairing"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"  ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== SECOND PAIRINGS FOR UNDER-PAIRED PRODUCTS ===\n")

# 651 — Ramonet Bâtard-Montrachet Grand Cru
PAIR(651, "Pan-roasted lobster with bisque and black truffle emulsion",
    "elevate", "established", "main",
    "Ramonet Bâtard-Montrachet's extraordinary mineral density and power elevates whole "
    "lobster at the highest level: the crustacean's natural sweetness amplifies the Grand Cru "
    "Chardonnay's weight; bisque bridges the wine's hazelnut and almond complexity; black "
    "truffle emulsion echoes the Bâtard's signature earthy mineral note. A luxury pairing "
    "of equal grandeur between Burgundy and the sea.")

# 650 — Ramonet Le Montrachet Grand Cru
PAIR(650, "Steamed sea bass with lemon oil, caviar, and chive beurre blanc",
    "elevate", "established", "fish_course",
    "Ramonet Le Montrachet — one of the world's greatest white wines — achieves its most "
    "complete expression with the finest fish preparations. Steamed sea bass with caviar "
    "is the ultimate test: the Montrachet's mineral depth amplifies both the fish and the "
    "caviar's brine; chive beurre blanc bridges wine and sauce; lemon oil mirrors the wine's "
    "citrus precision. A pairing of transcendent luxury.")

# 627 — Hermann J. Wiemer Dry Riesling
PAIR(627, "Vietnamese spring rolls with herb, prawn, and nuoc cham",
    "complement", "established", "starter",
    "Wiemer Dry Riesling's vivid acidity and citrus precision is the ideal partner for "
    "fresh Vietnamese spring rolls — the wine's lime and floral character amplifies the "
    "herbs; the nuoc cham's fish sauce salinity bridges the wine's minerality; the prawns' "
    "sweetness is amplified by the Riesling's natural fruit. A pairing that demonstrates "
    "Finger Lakes Riesling's versatility with global cuisine.")

# 641 — Château Brane-Cantenac Margaux
PAIR(641, "Roasted duck breast with violet jus and confit shallots",
    "complement", "established", "main",
    "Brane-Cantenac's perfumed Margaux violet character achieves perfect resonance with "
    "duck breast finished with a violet-infused jus — the wine's signature floral note "
    "amplifies the sauce's aromatic character; confit shallots provide sweetness that "
    "softens the Cabernet Sauvignon's silky tannin; the duck's richness bridges the wine's "
    "feminine elegance. A Margaux pairing of textbook floral harmony.")

# 644 — Billecart-Salmon Blanc de Blancs
PAIR(644, "Seared scallops with cauliflower purée and caviar",
    "elevate", "classic", "starter",
    "Billecart-Salmon Blanc de Blancs' pristine Chardonnay precision and mineral clarity "
    "elevates the classic scallop and cauliflower combination. The wine's chalk mineral "
    "amplifies the scallop's natural sweetness; the cauliflower purée's gentle creaminess "
    "bridges the wine's acidity; caviar adds a brine-mineral dimension that echoes the "
    "Chardonnay's precision. A luxury starter pairing of complete harmony.")

# 645 — Billecart-Salmon Nicolas François Billecart Vintage
PAIR(645, "Aged Brie de Meaux with black truffle",
    "complement", "established", "cheese",
    "Nicolas François Billecart's prestige cuvée — with Pinot Noir richness and Chardonnay "
    "precision — finds a magnificent partner in Brie de Meaux at peak ripeness. The wine's "
    "brioche and red fruit character amplifies the cheese's mushroom complexity; black "
    "truffle bridges the wine's Pinot depth with the Brie's earthy character. A luxury "
    "cheese pairing for France's greatest Champagne maison.")

# 653 — Domaine Leroy Nuits-Saint-Georges Les Allots 1er Cru
PAIR(653, "Slow-roasted venison with beetroot and juniper",
    "complement", "established", "main",
    "Domaine Leroy's extraordinary Nuits-Saint-Georges — concentrated beyond its classification "
    "through biodynamic precision — achieves a powerful pairing with game venison. The wine's "
    "dark cherry, iron, and truffle concentration matches venison's intensity; beetroot's "
    "earthy sweetness bridges the wine's mineral character; juniper amplifies the wine's "
    "forest-floor complexity. A pairing for Burgundy's most powerful village wines.")

# 634 — Château La Mission Haut-Brion Pessac-Léognan
PAIR(634, "Roasted rib of beef with bone marrow butter and potato dauphinoise",
    "complement", "classic", "main",
    "La Mission Haut-Brion's extraordinary concentration and graphite-mineral depth "
    "demands the richest beef preparation: rib roasted on the bone. The bone marrow "
    "butter softens the wine's powerful structure while amplifying its intensity; "
    "potato dauphinoise provides the starchy richness the wine's tannin needs to "
    "integrate. A pairing of equal power between Pessac's greatest wine and the kitchen.")

# 636 — Domaine de Chevalier Pessac-Léognan Rouge
PAIR(636, "Roasted partridge with lentils du Puy and Périgueux sauce",
    "complement", "established", "main",
    "Domaine de Chevalier Rouge's forest-influenced freshness and cedar complexity "
    "finds its natural partner in roasted partridge — the game bird's delicate flavour "
    "is elevated rather than overwhelmed by the wine's tobacco and cassis character. "
    "Lentils du Puy provide an earthy protein base; Périgueux sauce bridges Chevalier's "
    "Graves character with Périgord's truffle tradition.")

# 640 — Vieux Château Certan Pomerol
PAIR(640, "Duck confit with cherry sauce and celeriac gratin",
    "complement", "classic", "main",
    "VCC's structured Pomerol — with its significant Cabernet Franc influence — pairs "
    "magnificently with duck confit. The wine's tobacco and cedar character bridges the "
    "duck's richness while the Cabernet Franc's herbaceous note amplifies the cherry sauce. "
    "Celeriac gratin provides the earthy, starchy base the wine's structure needs. "
    "A pairing that demonstrates VCC's unique position between right-bank richness and "
    "left-bank restraint.")

# 649 — Sauzet Bâtard-Montrachet Grand Cru
PAIR(649, "Roasted scallops with truffle butter and cauliflower",
    "elevate", "established", "starter",
    "Sauzet Bâtard-Montrachet's mineral power and Chardonnay depth elevates roasted "
    "scallops to grand cru level: the wine's almond and lemon oil character amplifies "
    "the scallop's natural sweetness; truffle butter echoes the Bâtard's earthy mineral; "
    "cauliflower provides a creamy neutral base. A starter of absolute luxury logic.")

# 648 — Sauzet Puligny-Montrachet Les Combettes 1er Cru
PAIR(648, "Grilled halibut with asparagus, hollandaise, and chervil",
    "complement", "classic", "fish_course",
    "Sauzet Les Combettes' mineral Puligny precision finds perfect harmony with grilled "
    "halibut and hollandaise — one of fine dining's classic white Burgundy pairings. "
    "The wine's lemon and almond character amplifies the hollandaise's richness; asparagus "
    "echoes the Chardonnay's herb mineral note; chervil bridges wine and sauce. A Puligny "
    "pairing of Burgundy's most beloved white wine tradition.")

# 613 — Fillaboa Monte Alto Single Vineyard Albariño
PAIR(613, "Grilled sea bream with salsa verde and lemon",
    "complement", "classic", "main",
    "Fillaboa Monte Alto's structured, elevated Albariño from Condado do Tea pairs "
    "beautifully with grilled sea bream — the wine's citrus precision and mineral spine "
    "cuts through the fish's delicate oil while the salsa verde amplifies the wine's "
    "herbal character. Lemon bridges the wine's characteristic citrus expression. "
    "A Galician fish and wine pairing in its most versatile form.")

# 612 — Granbazan Ambar Albariño
PAIR(612, "Prawn and saffron risotto with aioli crouton",
    "complement", "established", "main",
    "Granbazan Ambar's vivid fresh Albariño achieves an elegant match with prawn and "
    "saffron risotto — the wine's stone fruit and citrus character amplifies the saffron's "
    "aromatic depth; the prawn's natural sweetness is bridged by the Albariño's maritime "
    "mineral; aioli echoes the wine's garlic-citrus character. A Mediterranean fusion "
    "pairing at its most approachable.")

# 611 — Pazo de Señorans Selección de Añada Albariño
PAIR(611, "Slow-cooked octopus with smoked paprika oil and lemon",
    "complement", "established", "main",
    "Señorans Selección at 5-8 years age — showing honeyed complexity alongside its "
    "saline Atlantic minerality — achieves a sophisticated match with slow-cooked octopus. "
    "The wine's oxidative depth bridges the octopus's texture; smoked paprika amplifies "
    "the wine's aromatic complexity; lemon echoes the Albariño's citrus precision. "
    "A Galician pairing that showcases aged Albariño's unexpected versatility.")

# 624 — José Pariente Cimentum Verdejo
PAIR(624, "Steamed mussels with white wine, garlic, and parsley",
    "complement", "classic", "starter",
    "José Pariente Cimentum's old-vine Verdejo structure and mineral intensity pairs "
    "classically with steamed mussels — the wine's fennel and citrus character amplifies "
    "the mussels' brine; garlic bridges the Verdejo's herbal aromatics; parsley echoes "
    "the wine's green herb character. The old-vine concentration provides the depth "
    "that standard Verdejo cannot achieve with shellfish.")

# 625 — Naia Verdejo
PAIR(625, "Tempura prawns with yuzu aioli and shiso",
    "complement", "established", "starter",
    "Naia Verdejo's biodynamic precision and mineral purity creates a fresh pairing "
    "with tempura prawns — the wine's citrus and fennel character amplifies the yuzu's "
    "aromatic brightness; shiso echoes the Verdejo's herbal character; the light tempura "
    "batter allows the prawn's sweetness to bridge with the wine's fruit. A pairing "
    "that brings Spanish Verdejo into Japanese-influenced fine dining.")

# 638 — Château Ausone Saint-Émilion Grand Cru
PAIR(638, "Wild mushroom and truffle risotto with Parmigiano Reggiano",
    "complement", "established", "main",
    "Château Ausone's mineral limestone precision and Cabernet Franc elegance achieves "
    "a distinguished pairing with wild mushroom and truffle risotto — the wine's graphite "
    "and iron mineral amplifies the truffle's earthiness; wild mushrooms provide an earthy "
    "base; Parmigiano's umami depth bridges wine and food. An unexpected but classically "
    "aligned pairing for one of Saint-Émilion's most intellectual wines.")

# 632 — Château Calon-Ségur Saint-Estèphe
PAIR(632, "Braised ox cheek with parsnip purée and bordelaise sauce",
    "complement", "classic", "main",
    "Calon-Ségur's structured clay-limestone Saint-Estèphe and slow-braised ox cheek: "
    "the wine's formidable tannin is the perfect foil for braised collagen-rich beef. "
    "The ox cheek's rendered fat and deep meaty flavour softens the wine's structure "
    "while amplifying its iron mineral character; parsnip purée provides earthy sweetness; "
    "bordelaise sauce creates complete Bordeaux harmony.")

# 633 — Château Montrose Saint-Estèphe
PAIR(633, "Venison haunch with blackberry reduction and celeriac dauphinoise",
    "complement", "established", "main",
    "Montrose's powerful Saint-Estèphe — the most concentrated in the appellation — "
    "demands game at its most intense. Venison haunch's deep, gamey richness matches the "
    "wine's massive Cabernet Sauvignon tannin and iron mineral; blackberry reduction "
    "amplifies the wine's dark fruit; celeriac dauphinoise provides the starchy richness "
    "required by Montrose's extraordinary structure. A pairing for the most powerful wines.")

# 621 — Polz Hochgrassnitzberg Sauvignon Blanc
PAIR(621, "Grilled king prawns with mango salsa and lime",
    "complement", "established", "starter",
    "Polz Hochgrassnitzberg's tropical-fruit Styrian Sauvignon Blanc finds unexpected "
    "harmony with king prawns and mango — the wine's passion fruit and guava character "
    "mirrors the mango's tropical sweetness; lime amplifies the wine's citrus precision; "
    "the prawn's natural sweetness bridges wine and tropical accompaniment. A pairing "
    "that reveals the tropical dimension of Steiermark Sauvignon Blanc.")

# 622 — Weingut Gross Nussberg Morillon
PAIR(622, "Roast Styrian free-range chicken with wild garlic and potato",
    "complement", "classic", "main",
    "Gross Nussberg Morillon (Chardonnay) — Steiermark's finest expression of the variety "
    "— achieves its most natural regional pairing with roasted Styrian chicken. The wine's "
    "apple and butter character amplifies the free-range chicken's richness; wild garlic "
    "bridges the Morillon's herbal mineral note; potato provides the classic Austrian "
    "starch base. A pairing of complete regional identity from Austria's southern wine region.")

cur.close()
conn.close()
print(f"\n✅ Terminal 15 Batch 1 — Second pairings for 22 products complete.")
