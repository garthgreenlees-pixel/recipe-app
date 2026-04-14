#!/usr/bin/env python3
"""Terminal 14 — Batch 1: Bordeaux depth (Saint-Julien, Saint-Estèphe, Pessac-Léognan, Saint-Émilion, Pomerol)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs (existing)
SAINT_JULIEN   = 124
SAINT_ESTEPHE  = 126
PESSAC         = 127
SAINT_EMILION  = 128
POMEROL        = 129
MEDOC          = 122
MARGAUX        = 125

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def P(name, producer_type, region_id, country,
      production_philosophy=None, philosophy_description=None,
      reputation_narrative=None, price_positioning=None, authority_tier=1):
    cur.execute("SELECT id FROM beverage_producers WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS producer: {name} (id={row[0]})")
        return row[0]
    philo_short = (production_philosophy or "")[:100] or None
    cur.execute("""
        INSERT INTO beverage_producers
          (name, producer_type, region_id, country,
           production_philosophy, philosophy_description,
           reputation_narrative, price_positioning, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, producer_type, region_id, country, philo_short,
          philosophy_description, reputation_narrative, price_positioning, authority_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ NEW producer: {name} (id={pid})")
    return pid

def PROD(name, category, producer_id, region_id, origin_country,
         subcategory=None, description=None, price_tier=None):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS product: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_products
          (name, category, subcategory, producer_id, region_id, origin_country,
           description, price_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (name, category, subcategory, producer_id, region_id, origin_country,
          description, price_tier))
    pid = cur.fetchone()[0]
    print(f"  ✓ NEW product: {name} (id={pid})")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ─── SAINT-JULIEN ─────────────────────────────────────────────────────────────
print("=== SAINT-JULIEN ===")

DUCRU = P(
    "Château Ducru-Beaucaillou", "winery", SAINT_JULIEN, "France",
    production_philosophy="Second Growth Saint-Julien, the archetypal expression of the appellation",
    philosophy_description=(
        "Château Ducru-Beaucaillou is widely regarded as the finest expression of Saint-Julien — "
        "the 'Beaucaillou' (beautiful pebbles) estate on the plateau above the Gironde produces "
        "Cabernet Sauvignon-dominant wines of extraordinary elegance, restraint, and longevity. "
        "The estate's perfect balance of power and finesse epitomises the Saint-Julien style: "
        "cedar, blackcurrant, graphite, and a silky texture that makes it uniquely food-compatible. "
        "Jean-Eugène Borie and Bruno Borie have maintained the estate's position as one of Médoc's "
        "most consistent overperforming Second Growths."
    ),
    reputation_narrative=(
        "Ducru-Beaucaillou is consistently rated as the finest wine of Saint-Julien and among the "
        "greatest of all Médoc Cru Classé. It is the benchmark for restrained Bordeaux elegance."
    ),
    price_positioning="ultra_premium"
)

LEOVILLE_BARTON = P(
    "Château Léoville-Barton", "winery", SAINT_JULIEN, "France",
    production_philosophy="Traditional Saint-Julien from the historic Barton family estate",
    philosophy_description=(
        "The Barton family (Anglo-Irish négociants established in Bordeaux since 1725) produce "
        "arguably the best-value Grand Cru Classé in the Médoc. Léoville-Barton's traditional "
        "winemaking — no new oak excess, long maceration, careful cellaring — produces wines of "
        "remarkable depth, structure, and longevity at prices far below Ducru-Beaucaillou. "
        "The wines are quintessential Saint-Julien: cedar, blackcurrant, plum, and a firm tannic "
        "backbone that softens beautifully over 15-25 years."
    ),
    reputation_narrative=(
        "Léoville-Barton is one of Bordeaux's greatest value propositions among classified growths — "
        "consistently outperforming its price. A benchmark for traditional, age-worthy Médoc style."
    ),
    price_positioning="premium"
)

DUCRU_WINE = PROD(
    "Château Ducru-Beaucaillou Saint-Julien",
    "wine_still", DUCRU, SAINT_JULIEN, "France",
    subcategory="red",
    description=(
        "The quintessential Saint-Julien: a Cabernet Sauvignon-dominant (75%+) Grand Cru Classé "
        "of extraordinary elegance and longevity. Ducru-Beaucaillou shows the unique Saint-Julien "
        "character — neither as powerful as Pauillac nor as floral as Margaux, but perfectly "
        "poised between them: cedar, blackcurrant, graphite, tobacco, and a silky tannic texture "
        "that makes this the most food-compatible of all Médoc classified growths. "
        "Best at 15-30 years; exceptional vintages (2016, 2019) can age 40+ years."
    ),
    price_tier="ultra_premium"
)

LEOVILLE_BARTON_WINE = PROD(
    "Château Léoville-Barton Saint-Julien",
    "wine_still", LEOVILLE_BARTON, SAINT_JULIEN, "France",
    subcategory="red",
    description=(
        "The Barton family's traditional Saint-Julien is one of the most compelling value "
        "propositions in classified Bordeaux — a wine of deep structure, remarkable concentration, "
        "and 20-30 year aging potential at prices well below super-second quality. Classic "
        "Médoc character: blackcurrant, cassis, cedar, dried herbs, and firm tannin that softens "
        "into extraordinary complexity. A wine for patient collectors and fine dining lists that "
        "seek Bordeaux depth without ultra-premium pricing."
    ),
    price_tier="premium"
)

# ─── SAINT-ESTÈPHE ────────────────────────────────────────────────────────────
print("\n=== SAINT-ESTÈPHE ===")

CALON_SEGUR = P(
    "Château Calon-Ségur", "winery", SAINT_ESTEPHE, "France",
    production_philosophy="The most Pauillac-like Saint-Estèphe, historic third growth with unique terroir",
    philosophy_description=(
        "Château Calon-Ségur — the most northern of the Médoc classified growths — produces "
        "wines of extraordinary structure and longevity that transcend their Third Growth status. "
        "The estate's unique position on Saint-Estèphe's clay-limestone plateau produces wines "
        "with even more tannin and aging potential than neighbours Cos d'Estournel or Montrose. "
        "Famously the favourite estate of Marquis de Ségur (who owned Pétrus, Latour, and Mouton), "
        "the heart on the label ('My heart belongs to Calon') remains one of Bordeaux's most "
        "recognisable symbols. The 2012-onward era under new ownership has seen spectacular quality "
        "improvement."
    ),
    reputation_narrative=(
        "Calon-Ségur is one of the most historic and beloved châteaux in the Médoc. Recent vintages "
        "under the Capbern-Gasqueton/Suravenir ownership rank with the greatest Saint-Estèphes ever made."
    ),
    price_positioning="ultra_premium"
)

MONTROSE = P(
    "Château Montrose", "winery", SAINT_ESTEPHE, "France",
    production_philosophy="Second Growth Saint-Estèphe, the most powerful and structured expression of the appellation",
    philosophy_description=(
        "Château Montrose is Saint-Estèphe's most powerful wine — a Second Growth of extraordinary "
        "concentration and aging potential. The estate's unique position directly on the Gironde "
        "estuary, with deep gravel soils over clay, produces Cabernet Sauvignon of maximum "
        "concentration: blackcurrant, iron, graphite, dark chocolate, and massive tannic structure "
        "that demands 15-25 years. Montrose 1989 and 1990 are among the greatest Bordeaux wines "
        "of the 20th century. The 2009 and 2010 vintages are benchmarks for the appellation's "
        "classical power style."
    ),
    reputation_narrative=(
        "Montrose is Saint-Estèphe's most powerful wine and one of the Médoc's most age-worthy "
        "classified growths. It is a collector's benchmark for structured, long-lived Bordeaux."
    ),
    price_positioning="ultra_premium"
)

CALON_WINE = PROD(
    "Château Calon-Ségur Saint-Estèphe",
    "wine_still", CALON_SEGUR, SAINT_ESTEPHE, "France",
    subcategory="red",
    description=(
        "Calon-Ségur's third growth Saint-Estèphe is one of Bordeaux's most distinctive classified "
        "wines — structured, mineral, and long-lived, with a unique personality derived from the "
        "clay-limestone terroir at the appellation's northern extreme. Blackcurrant, plum, iron, "
        "graphite, and dried herbs with formidable tannic structure requiring 12-20 years to "
        "resolve. Recent vintages (2016, 2018, 2019) are among the finest Calon has ever produced. "
        "The iconic heart label makes it one of the most recognisable wines in the world."
    ),
    price_tier="ultra_premium"
)

MONTROSE_WINE = PROD(
    "Château Montrose Saint-Estèphe",
    "wine_still", MONTROSE, SAINT_ESTEPHE, "France",
    subcategory="red",
    description=(
        "Saint-Estèphe's most powerful Second Growth — Montrose produces Bordeaux of extraordinary "
        "concentration and aging potential. The deep gravel-over-clay soils produce Cabernet "
        "Sauvignon (65%+) of maximum density: blackcurrant, iron mineral, dark chocolate, graphite, "
        "and cedar with massive structure requiring 15-25 years. Legendary vintages: 1989, 1990, "
        "2009, 2010, 2016. A wine for the most serious cellars and long-term fine dining lists."
    ),
    price_tier="ultra_premium"
)

# ─── PESSAC-LÉOGNAN ──────────────────────────────────────────────────────────
print("\n=== PESSAC-LÉOGNAN ===")

LA_MISSION = P(
    "Château La Mission Haut-Brion", "winery", PESSAC, "France",
    production_philosophy="The great neighbour and rival of Haut-Brion — Pessac's second icon",
    philosophy_description=(
        "Château La Mission Haut-Brion shares the same legendary plateau of deep gravel as its "
        "neighbour Haut-Brion — they have been owned by the same family (Dillon/Domaine Clarence "
        "Dillon) since 1983. La Mission produces a wine of even greater concentration and power "
        "than Haut-Brion: darker in colour, more tannic, more mineral, and arguably even more "
        "age-worthy. In the greatest vintages (1959, 1975, 1989, 2016), La Mission rivals any "
        "wine in Bordeaux. The whites (La Mission Haut-Brion Blanc) are among the finest in the "
        "entire Bordeaux appellation."
    ),
    reputation_narrative=(
        "La Mission Haut-Brion is considered equal in quality to its more famous neighbour "
        "Haut-Brion. In top vintages it is one of the most collectible wines in the world."
    ),
    price_positioning="ultra_premium"
)

CHEVALIER = P(
    "Domaine de Chevalier", "winery", PESSAC, "France",
    production_philosophy="Intellectual Pessac-Léognan with outstanding whites and reds of great longevity",
    philosophy_description=(
        "Domaine de Chevalier is among the most admired estates in Pessac-Léognan — known equally "
        "for exceptional white and red wines of great longevity. The estate's unique situation in "
        "the forest of Léognan provides a naturally cooling influence that preserves acidity in "
        "both colours. The white (100% Sauvignon Blanc with some Sémillon) is aged in barrel for "
        "18 months and can age for 20-30 years — one of the world's longest-lived dry white wines. "
        "The red shows great cedar, tobacco, and graphite complexity that develops for 15-25 years."
    ),
    reputation_narrative=(
        "Domaine de Chevalier's white is one of the greatest dry white wines in the world — "
        "a wine that evolves over decades and challenges the finest white Burgundy for longevity. "
        "The red is among Pessac-Léognan's finest values."
    ),
    price_positioning="premium"
)

LA_MISSION_WINE = PROD(
    "Château La Mission Haut-Brion Pessac-Léognan",
    "wine_still", LA_MISSION, PESSAC, "France",
    subcategory="red",
    description=(
        "La Mission Haut-Brion is Pessac-Léognan's second icon — more concentrated and powerful "
        "than its neighbour Haut-Brion, with even greater aging potential. From deep gravel soils "
        "on the legendary plateau: intense blackcurrant, graphite, iron mineral, tobacco, and "
        "extraordinary density of fruit and tannin. In great vintages (1959, 1975, 1989, 2016, "
        "2019) La Mission reaches a level that few wines anywhere can match. Best at 20-40 years."
    ),
    price_tier="ultra_premium"
)

CHEVALIER_WHITE = PROD(
    "Domaine de Chevalier Pessac-Léognan Blanc",
    "wine_still", CHEVALIER, PESSAC, "France",
    subcategory="white",
    description=(
        "One of the world's greatest dry white wines — Domaine de Chevalier Blanc (70% Sauvignon "
        "Blanc, 30% Sémillon) is fermented and aged in French oak barriques, producing a wine of "
        "extraordinary complexity that develops for 20-30 years. Young, the wine shows grapefruit, "
        "white peach, and new oak; at 10-15 years it reveals lanolin, beeswax, honey, and the "
        "distinctive Graves mineral character. A rival to the finest white Burgundy for longevity "
        "and intellectual complexity. One of fine dining's most compelling cellar selections."
    ),
    price_tier="ultra_premium"
)

CHEVALIER_RED = PROD(
    "Domaine de Chevalier Pessac-Léognan Rouge",
    "wine_still", CHEVALIER, PESSAC, "France",
    subcategory="red",
    description=(
        "Domaine de Chevalier's red is a wine of remarkable cedar, tobacco, and graphite complexity "
        "— a restrained, elegant Pessac-Léognan that develops beautifully over 15-25 years. The "
        "forest influence preserves fresh acidity in Cabernet Sauvignon-dominant blends: cassis, "
        "cedar, dried herbs, leather, and mineral depth. An outstanding value among the finest "
        "Pessac-Léognan classified growths."
    ),
    price_tier="premium"
)

# ─── SAINT-ÉMILION ────────────────────────────────────────────────────────────
print("\n=== SAINT-ÉMILION ===")

ANGELUS = P(
    "Château Angélus", "winery", SAINT_EMILION, "France",
    production_philosophy="Premier Grand Cru Classé A Saint-Émilion — power and modernity",
    philosophy_description=(
        "Château Angélus achieved the ultimate elevation to Premier Grand Cru Classé A in 2012 "
        "alongside Ausone and Cheval Blanc, making it one of only four wines at the apex of "
        "Saint-Émilion's classification. The Boüard de Laforest family's Merlot-dominant blend "
        "from clay-limestone and sandy-gravel soils produces wines of extraordinary richness and "
        "modern opulence: dark fruit, chocolate, toasted oak, and powerful extraction that polarises "
        "traditionalists but attracts the world's most prestigious cellars. Now in the hands of "
        "Stéphanie de Boüard, the estate is experiencing a new era of precision."
    ),
    reputation_narrative=(
        "Angélus is one of the world's most collectible wines — a Premier Grand Cru Classé A and "
        "the face of modern Saint-Émilion's ambition. Its bell-tower label is instantly recognisable."
    ),
    price_positioning="ultra_premium"
)

AUSONE = P(
    "Château Ausone", "winery", SAINT_EMILION, "France",
    production_philosophy="The most historic Premier Grand Cru Classé A — Saint-Émilion's most age-worthy wine",
    philosophy_description=(
        "Château Ausone occupies the most spectacular site in Saint-Émilion — a steep south-facing "
        "limestone cliff plateau above the ancient Roman town, named after the 4th-century Latin poet "
        "Ausonius. The production is minuscule (just 2,000 cases per vintage) from a unique "
        "combination of clay-limestone and limestone rock that produces wines of extraordinary "
        "minerality, precision, and longevity. Where Angélus represents modern richness, Ausone "
        "represents historical restraint: elegant, mineral, with a lifespan of 30-50+ years. "
        "Under Alain Vauthier's stewardship (1995-2019), Ausone achieved iconic status."
    ),
    reputation_narrative=(
        "Château Ausone is the most historically significant Premier Grand Cru Classé A — the wine "
        "most associated with Saint-Émilion's ancient heritage. In top vintages it is one of the "
        "world's most collectible and long-lived wines."
    ),
    price_positioning="ultra_premium"
)

ANGELUS_WINE = PROD(
    "Château Angélus Saint-Émilion Grand Cru",
    "wine_still", ANGELUS, SAINT_EMILION, "France",
    subcategory="red",
    description=(
        "Premier Grand Cru Classé A Saint-Émilion — Angélus is the most modern and opulent of "
        "the appellation's elite. Merlot-dominant (60%+) with Cabernet Franc: dark cherry, plum, "
        "dark chocolate, toasted oak, and extraordinary density. The wine requires 8-15 years to "
        "integrate but offers immediate hedonistic pleasure. James Suckling, Robert Parker, and "
        "Wine Spectator regularly award 97-100 points. One of the world's most famous wine labels "
        "— the iconic Saint-Émilion bell tower is universally recognised."
    ),
    price_tier="ultra_premium"
)

AUSONE_WINE = PROD(
    "Château Ausone Saint-Émilion Grand Cru",
    "wine_still", AUSONE, SAINT_EMILION, "France",
    subcategory="red",
    description=(
        "The most historic wine in Saint-Émilion — Château Ausone Premier Grand Cru Classé A from "
        "the unique limestone cliff site above the ancient town. Production is minuscule (just 2,000 "
        "cases). Cabernet Franc-dominant (55%+) with Merlot: extraordinary mineral precision, "
        "graphite, iron, red currant, cherry, and a limestone-clay structure that ages for 30-50 "
        "years. Where Angélus is hedonistic power, Ausone is intellectual precision — the most "
        "Burgundian Bordeaux in the world. Consistently among the 10 greatest wines on Earth."
    ),
    price_tier="ultra_premium"
)

# ─── POMEROL ──────────────────────────────────────────────────────────────────
print("\n=== POMEROL ===")

LE_PIN = P(
    "Château Le Pin", "winery", POMEROL, "France",
    production_philosophy="The ultimate micro-cuvée — Pomerol's rarest and most sought-after wine",
    philosophy_description=(
        "Château Le Pin is the world's most expensive wine by production size per bottle — just "
        "700 cases per vintage from 2 hectares of pure Pomerol clay, producing Merlot of "
        "extraordinary concentration, texture, and hedonism. Jacques Thienpont purchased the "
        "almost-forgotten estate in 1979; by the early 1980s Le Pin had become a phenomenon. "
        "The wine's extraordinary density, silky tannin, and almost Burgundian (rather than "
        "Bordeaux) aromatic profile make it unique among the world's great wines. "
        "Allocations are virtually unobtainable; secondary market prices rival or exceed Pétrus."
    ),
    reputation_narrative=(
        "Le Pin is among the world's most sought-after wines — a micro-production Pomerol of "
        "legendary concentration and rarity. Secondary market prices exceed $2,000 per bottle "
        "for top vintages. A true unicorn wine."
    ),
    price_positioning="ultra_premium"
)

VCC = P(
    "Vieux Château Certan", "winery", POMEROL, "France",
    production_philosophy="The most Cabernet-influenced wine in Pomerol — restrained elegance over power",
    philosophy_description=(
        "Vieux Château Certan is unique in Pomerol for its significant Cabernet Franc and Cabernet "
        "Sauvignon content alongside Merlot — the Thienpont family estate (purchased 1924) produces "
        "the most structured, age-worthy, and intellectually complex wine in the appellation. "
        "Where Pétrus offers pure hedonistic Merlot power, VCC offers restraint, complexity, "
        "and extraordinary longevity: cedar, tobacco, plum, iron mineral, and fine tannin that "
        "unfolds over 15-30 years. A wine beloved by those who prefer Bordeaux's cerebral side."
    ),
    reputation_narrative=(
        "Vieux Château Certan is the most intellectual wine in Pomerol — beloved by Bordeaux "
        "traditionalists for its restraint, Cabernet influence, and 30+ year aging potential. "
        "One of the appellation's most reliable overperformers."
    ),
    price_positioning="ultra_premium"
)

LE_PIN_WINE = PROD(
    "Château Le Pin Pomerol",
    "wine_still", LE_PIN, POMEROL, "France",
    subcategory="red",
    description=(
        "The world's most sought-after micro-cuvée — Château Le Pin from just 2 hectares of "
        "pure Pomerol clay produces 700 cases of pure Merlot that is unlike any other Bordeaux. "
        "The wine's extraordinary density, silky tannin, and almost Burgundian aromatic profile "
        "(dark cherry, truffle, chocolate, violet) make it the most hedonistic wine in the "
        "appellation. Secondary market prices for top vintages (1982, 1990, 2012, 2019) "
        "exceed Pétrus. Virtually unobtainable at release."
    ),
    price_tier="ultra_premium"
)

VCC_WINE = PROD(
    "Vieux Château Certan Pomerol",
    "wine_still", VCC, POMEROL, "France",
    subcategory="red",
    description=(
        "The most restrained and intellectual wine in Pomerol — VCC's significant Cabernet Franc "
        "content makes it unique in the appellation. Plum, cherry, tobacco, cedar, and iron mineral "
        "with a structured tannic backbone that unfolds over 15-30 years. The Thienpont family "
        "estate produces a wine of Médoc-like discipline on Pomerol's clay plateau: complex, "
        "age-worthy, and among the finest values among the appellation's elite."
    ),
    price_tier="ultra_premium"
)

# ─── MARGAUX DEPTH ────────────────────────────────────────────────────────────
print("\n=== MARGAUX DEPTH ===")

BRANE_CANTENAC = P(
    "Château Brane-Cantenac", "winery", MARGAUX, "France",
    production_philosophy="Second Growth Margaux — the quintessential floral, feminine Margaux style",
    philosophy_description=(
        "Château Brane-Cantenac is the quintessential Second Growth Margaux — the estate that "
        "defines the appellation's famous floral, feminine style: violet, rose petal, blackcurrant, "
        "and silky tannin. The Lurton family estate on the finest deep-gravel plateau of Cantenac "
        "produces wines of pure Margaux character that are among the appellation's most reliable "
        "performers at a fraction of Château Margaux's price. Henri Lurton's modern approach "
        "emphasises freshness, precision, and the classic perfumed Margaux style."
    ),
    reputation_narrative=(
        "Brane-Cantenac is considered among the finest value propositions in Margaux — a Second "
        "Growth that reliably delivers the appellation's signature floral, silky character."
    ),
    price_positioning="premium"
)

BRANE_WINE = PROD(
    "Château Brane-Cantenac Margaux",
    "wine_still", BRANE_CANTENAC, MARGAUX, "France",
    subcategory="red",
    description=(
        "Second Growth Margaux in its most classic floral expression: violet, rose petal, cassis, "
        "tobacco, and silky Cabernet Sauvignon tannin from Cantenac's legendary deep-gravel "
        "plateau. Brane-Cantenac delivers the Margaux appellation character at a fraction of "
        "Château Margaux's price — the most accessible route to authentic perfumed Médoc style. "
        "Best at 10-20 years; exceptional vintages (2015, 2016, 2019) age for 30 years."
    ),
    price_tier="premium"
)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Saint-Julien pairings
PAIR(DUCRU_WINE, "Roasted rack of lamb with rosemary jus and Pauillac lamb",
    "complement", "classic", "main",
    "Château Ducru-Beaucaillou and rack of lamb: the quintessential Saint-Julien pairing. "
    "The wine's cedar, cassis, and graphite character finds its perfect partner in roasted "
    "lamb — the rosemary jus amplifies the Cabernet Sauvignon's herb character while the "
    "lamb fat softens the wine's firm tannin. Saint-Julien's balance of power and finesse "
    "makes Ducru the most food-compatible of all Médoc classified growths.")

PAIR(DUCRU_WINE, "Côte de boeuf with bone marrow and Bordelaise sauce",
    "complement", "classic", "main",
    "The classic Bordeaux beef pairing: Ducru-Beaucaillou and côte de boeuf with traditional "
    "Bordelaise sauce. The wine's structure and Cabernet fruit amplifies the beef's marbling "
    "while the marrow sauce echoes the wine's richness. The Bordelaise (bone marrow, shallots, "
    "red wine) creates perfect harmony between Médoc and Gascon culinary tradition.")

PAIR(LEOVILLE_BARTON_WINE, "Navarin of lamb with spring vegetables",
    "complement", "classic", "main",
    "Léoville-Barton's traditional Saint-Julien and a classic French navarin: the wine's "
    "blackcurrant and firm tannic structure integrates beautifully with slow-braised lamb. "
    "Spring vegetables (peas, carrots, turnips) amplify the wine's fresh aromatic character "
    "while the lamb broth deepens its savory complexity. A classically French restaurant pairing.")

PAIR(LEOVILLE_BARTON_WINE, "Aged Comté with walnuts and honey",
    "complement", "established", "cheese",
    "Léoville-Barton at 10-15 years age with Comté: a classic Bordelaise cheese pairing. "
    "The wine's cedar and tobacco development amplifies the aged Comté's caramel depth; "
    "walnuts echo the wine's earthy complexity; honey bridges the tannin and fat. "
    "A pairing that demonstrates traditional French wine-and-cheese culture at its finest.")

# Saint-Estèphe pairings
PAIR(CALON_WINE, "Slow-roasted shoulder of beef with root vegetable gratin",
    "complement", "classic", "main",
    "Calon-Ségur's firm clay-limestone structure demands the richness of slow-roasted beef. "
    "The wine's formidable tannin and iron mineral character is softened by the beef's collagen "
    "while the root vegetable gratin provides earthy sweetness. A pairing for the patience that "
    "great Saint-Estèphe requires — both wine and dish improve with time.")

PAIR(MONTROSE_WINE, "Grilled ribeye with truffle butter and potato gratin",
    "complement", "classic", "main",
    "Montrose's massive Saint-Estèphe structure — the most powerful wine in the appellation — "
    "demands grilled ribeye as its equal partner. The beef's marbling softens the wine's "
    "formidable tannin while truffle amplifies Montrose's earthy, iron mineral depth. "
    "Potato gratin provides the starchy base for the wine's concentrated extract. "
    "A pairing of equal power between Gironde and kitchen.")

# Pessac-Léognan pairings
PAIR(LA_MISSION_WINE, "Roasted pigeon with foie gras and Pomerol jus",
    "elevate", "established", "main",
    "La Mission Haut-Brion's extraordinary concentration and power elevates the classic French "
    "luxury pairing of roasted pigeon with foie gras. The wine's graphite and blackcurrant depth "
    "amplifies the pigeon's gaminess while the foie gras richness tempers the wine's formidable "
    "structure. Pomerol jus bridges the right-bank richness with left-bank Graves tradition. "
    "A pairing for the finest tasting menus.")

PAIR(CHEVALIER_WHITE, "Sautéed langoustines with bisque, tarragon, and Sauternes cream",
    "elevate", "classic", "fish_course",
    "Domaine de Chevalier Blanc — one of the world's greatest dry whites — achieves its finest "
    "expression with langoustines and bisque. The wine's grapefruit and honeyed barrel complexity "
    "amplifies the langoustine's natural sweetness; the tarragon bridges the wine's herbal "
    "character; Sauternes cream adds a sweet-rich dimension the Chevalier white handles with "
    "authority. A Pessac-Léognan fine dining pairing of the highest order.")

PAIR(CHEVALIER_WHITE, "Roasted turbot with beurre blanc and caviar",
    "elevate", "established", "fish_course",
    "At 8-12 years, Domaine de Chevalier Blanc's honeyed Graves complexity and extraordinary "
    "mineral depth creates one of the world's great white wine and fish pairings: the turbot's "
    "firm flesh and delicate flavour is amplified rather than overwhelmed by the wine's richness. "
    "Caviar adds a brine-mineral note that echoes the wine's Graves terroir character.")

PAIR(CHEVALIER_RED, "Herb-roasted leg of Pauillac lamb with flageolet beans",
    "complement", "classic", "main",
    "Domaine de Chevalier Rouge and Pauillac lamb — a Graves tradition. The wine's cedar "
    "and tobacco complexity bridges the lamb's herb-roasted character while the flageolet "
    "beans provide an earthy protein base. Chevalier's forest influence gives a freshness "
    "that integrates beautifully with the classic French preparation.")

# Saint-Émilion pairings
PAIR(ANGELUS_WINE, "Roasted suckling pig with black truffle and Périgueux sauce",
    "complement", "classic", "main",
    "Angélus's rich Merlot opulence meets the luxurious combination of suckling pig and "
    "black truffle. The wine's dark fruit and chocolate richness amplifies the pig's fat; "
    "truffle amplifies the wine's earthy complexity; Périgueux sauce (truffle and Madeira) "
    "creates perfect luxury alignment between Saint-Émilion and Périgord tradition. "
    "A pairing worthy of a Premier Grand Cru Classé A.")

PAIR(ANGELUS_WINE, "Wagyu beef with bone marrow butter and roasted mushroom",
    "complement", "established", "main",
    "Angélus's concentrated Merlot richness and modern power is the natural companion for "
    "the world's most marbled beef. The wagyu's extraordinary fat content softens the wine's "
    "powerful extraction; bone marrow butter amplifies the wine's richness; roasted mushroom "
    "provides an earthy counterpoint to the wine's dark fruit character.")

PAIR(AUSONE_WINE, "Roasted squab (pigeon) with lentils du Puy and foie gras",
    "elevate", "established", "main",
    "Château Ausone's mineral, Cabernet Franc-influenced precision elevates the classic game "
    "bird pairing. The pigeon's gamey richness matches the wine's iron and graphite mineral "
    "depth; lentils du Puy add earthy protein structure; foie gras provides the luxury richness "
    "the wine can penetrate with its limestone mineral precision. A pairing of Saint-Émilion's "
    "most intellectual wine with France's most refined game tradition.")

# Pomerol pairings
PAIR(LE_PIN_WINE, "Roasted duck breast with black cherry, aged balsamic, and pomme sarladaise",
    "complement", "classic", "main",
    "Château Le Pin's pure hedonistic Merlot — almost Burgundian in its silky density — "
    "achieves its greatest expression with duck breast and black cherry sauce. The wine's "
    "dark cherry, truffle, and chocolate character amplifies the duck's richness; the cherry "
    "sauce bridges both; pomme sarladaise (potatoes cooked in duck fat) provides the "
    "Pomerol clay richness that Le Pin was born to accompany.")

PAIR(LE_PIN_WINE, "Black truffle risotto with aged Parmigiano Reggiano",
    "elevate", "established", "main",
    "Le Pin's extraordinary truffle and dark cherry character creates a natural bridge to "
    "black truffle risotto — one of the rare instances where the world's most expensive "
    "Bordeaux meets a non-meat main course. The wine's silky Merlot texture integrates "
    "beautifully with the risotto's starchy richness; Parmigiano amplifies the wine's "
    "savoury umami depth. A luxury pairing of rare Italian-French alignment.")

PAIR(VCC_WINE, "Roasted rack of lamb with tapenade crust and green olive jus",
    "complement", "classic", "main",
    "Vieux Château Certan's Cabernet Franc influence and structured restraint finds its "
    "natural partner in herb-crusted rack of lamb. The wine's tobacco and cedar character "
    "amplifies the olive tapenade; green olive jus bridges the wine's mineral character "
    "with the lamb's richness. A pairing that demonstrates VCC's unique position in Pomerol: "
    "as food-compatible as the finest Médoc, as lush as right-bank tradition.")

PAIR(BRANE_WINE, "Pan-roasted veal chop with truffle jus and morel mushroom",
    "complement", "established", "main",
    "Brane-Cantenac's perfumed Margaux style — violet, cassis, silky tannin — finds perfect "
    "expression with pan-roasted veal and truffle. The wine's floral aromatics amplify the "
    "truffle's earthy perfume; morel mushroom adds depth that the Margaux's silk can bridge; "
    "the veal's delicacy matches the wine's feminine, restrained power. Classic grand cru Médoc.")

cur.close()
conn.close()
print("\n✅ Terminal 14 Batch 1 — Bordeaux depth complete.")
