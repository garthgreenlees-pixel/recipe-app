#!/usr/bin/env python3
"""Terminal 16 — Batch 1: Portuguese wine depth (Alentejo + Bairrada + Vinho Verde) + vintages"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs
ALENTEJO    = 232
BAIRRADA    = 233
VINHO_VERDE = 231

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

def V(region_id, year, rating, descriptor, narrative, price_traj="stable", window_from=None, window_to=None):
    cur.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory,
           drinking_window, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,1)
        ON CONFLICT (region_id, vintage_year) DO NOTHING
    """, (region_id, year, rating, descriptor, narrative, price_traj,
          json.dumps({"from": window_from, "to": window_to}) if window_from else None))
    action = "✓" if cur.rowcount else "~"
    print(f"  {action} {year} → region {region_id}: {descriptor} ({rating})")

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:55]}... → product {product_id}")

# ─── ALENTEJO DEPTH ──────────────────────────────────────────────────────────
print("=== ALENTEJO DOC DEPTH ===")

HERDADE_MOUCHAO = P(
    "Herdade do Mouchão", "winery", ALENTEJO, "Portugal",
    production_philosophy="Historic Alentejo estate — old-vine Trincadeira and Aragonez blends",
    philosophy_description=(
        "Herdade do Mouchão is one of the most historic wine estates in Alentejo — a working "
        "agricultural estate producing wine since the 17th century. The estate's unique blend "
        "of Trincadeira (Tinta Amarela) and Aragonez (Tempranillo) from old vines on the "
        "schist and red clay soils of the Mourão plateau produces wines of extraordinary "
        "character: cedar, dark plum, dried herbs, and a distinctive rustic complexity that "
        "can only come from decades of vine age in Alentejo's extreme continental climate. "
        "The Mouchão Tinto is considered one of the most authentic and age-worthy wines in "
        "all of Portugal — resistant to modernisation, proud of its tradition."
    ),
    reputation_narrative=(
        "Herdade do Mouchão is a living monument to traditional Alentejo winemaking — one "
        "of the most historically authentic estates in Portugal and the benchmark for age-"
        "worthy Alentejo red wine."
    ),
    price_positioning="premium"
)

MONTE_PECEGUINA = P(
    "Monte da Peceguina", "winery", ALENTEJO, "Portugal",
    production_philosophy="Natural wine approach in Alentejo — old indigenous varieties, biodynamic",
    philosophy_description=(
        "Monte da Peceguina (Malhadinha Nova's estate wine) is among the most admired "
        "natural wine producers in Portugal — farming biodynamically on the Serra de "
        "Grândola's elevated soils to produce wines of extraordinary freshness and "
        "precision rare in Alentejo's warm climate. The entry Peceguina blend demonstrates "
        "that Alentejo can produce lighter, more food-friendly reds without sacrificing "
        "character; the Malhadinha label shows the estate's capacity for concentration and "
        "age-worthiness at the premium level."
    ),
    reputation_narrative=(
        "Monte da Peceguina is one of Portugal's most admired natural wine estates — a "
        "benchmark for restrained, food-friendly Alentejo red wine."
    ),
    price_positioning="premium"
)

ESPORAO_WHITE = PROD(
    "Esporão Reserva Branco",
    "wine_still", 471, ALENTEJO, "Portugal",  # Esporão Herdade (existing producer)
    subcategory="white",
    description=(
        "Esporão Reserva Branco is one of the finest white wines in Portugal — a blend of "
        "Antão Vaz, Arinto, and Roupeiro from the estate's certified organic vineyards on "
        "the Alentejo plain. Fermented in French oak barrels, the wine shows extraordinary "
        "complexity: lemon curd, white peach, toasted almond, and the characteristic dried "
        "herb and mineral character of Alentejo's continental soils. The wine ages "
        "magnificently for 8-12 years. Among the greatest southern Portuguese white wines."
    ),
    price_tier="premium"
)

MOUCHAO_TINTO = PROD(
    "Herdade do Mouchão Tinto",
    "wine_still", HERDADE_MOUCHAO, ALENTEJO, "Portugal",
    subcategory="red",
    description=(
        "One of Portugal's most authentic and age-worthy reds — Mouchão Tinto from old-vine "
        "Trincadeira and Aragonez on the schist plateau of Mourão. The wine's traditional "
        "approach (native yeast, old barrels, extended maceration) produces extraordinary "
        "complexity: cedar, dark plum, dried fig, tobacco, and the distinctive dusty mineral "
        "of Alentejo's red clay. Resistant to modernisation — the 1966 and 1969 vintages "
        "are legendary. Current vintages need 8-15 years. A Portuguese national treasure."
    ),
    price_tier="premium"
)

PECEGUINA_RED = PROD(
    "Monte da Peceguina Tinto",
    "wine_still", MONTE_PECEGUINA, ALENTEJO, "Portugal",
    subcategory="red",
    description=(
        "Monte da Peceguina's natural wine Alentejo Tinto from biodynamic vineyards on "
        "Serra de Grândola — lighter, fresher, and more food-friendly than typical Alentejo "
        "reds. The indigenous varieties (Aragonez, Trincadeira, Touriga Nacional) are farmed "
        "for freshness rather than extraction: red cherry, dried herb, dark plum, and a "
        "mineral precision rare in southern Portugal. The most approachable gateway to "
        "serious Alentejo wine for fine dining lists seeking Portuguese identity."
    ),
    price_tier="mid_range"
)

# ─── BAIRRADA DEPTH ──────────────────────────────────────────────────────────
print("\n=== BAIRRADA DOC DEPTH ===")

FILIPA_PATO = P(
    "Filipa Pato", "winery", BAIRRADA, "Portugal",
    production_philosophy="Natural Bairrada Baga and sparkling wine — daughter of Luis Pato",
    philosophy_description=(
        "Filipa Pato (daughter of Bairrada icon Luis Pato) has established her own distinctive "
        "identity — producing natural, minimal-intervention wines from Baga and Bical in the "
        "clay and limestone soils of Bairrada. Her approach emphasises freshness and elegance "
        "over the traditional tannic power of Baga — the Nossa Calcário (Our Limestone) red "
        "and the sparkling Blanc de Blancs Bruto represent the most exciting new direction "
        "for one of Portugal's most underrated appellations."
    ),
    reputation_narrative=(
        "Filipa Pato is one of Portugal's most exciting emerging winemakers — bringing natural "
        "wine thinking to Bairrada's great indigenous variety Baga. Her wines appear on the "
        "most forward-thinking Portuguese wine lists."
    ),
    price_positioning="premium"
)

SIDONIO = P(
    "Sidonio de Sousa", "winery", BAIRRADA, "Portugal",
    production_philosophy="Traditional Bairrada Baga — the most tannic, age-worthy style",
    philosophy_description=(
        "Sidonio de Sousa is the most traditional producer in Bairrada — producing old-school "
        "Baga of extraordinary tannic structure and aging potential from the appellation's "
        "heaviest clay soils. The wines are not for the impatient: 5-10 years is minimum "
        "to soften the ferocious tannin of young Baga from this estate. But at 15-20 years, "
        "Sidonio de Sousa's Bairrada reveals one of Portugal's most complex and distinctive "
        "red wine profiles: dark cherry, tobacco, cedar, leather, and an almost Barolo-like "
        "mineral precision from the clay."
    ),
    reputation_narrative=(
        "Sidonio de Sousa is the most traditional voice in Bairrada — a reference for the "
        "traditional, long-lived style of Baga that can rival aged Barolo in complexity."
    ),
    price_positioning="premium"
)

FILIPA_CALCARIO = PROD(
    "Filipa Pato Nossa Calcário Baga",
    "wine_still", FILIPA_PATO, BAIRRADA, "Portugal",
    subcategory="red",
    description=(
        "Filipa Pato's 'Nossa Calcário' (Our Limestone) is the most elegant and food-friendly "
        "expression of Baga — aged in large neutral oak for minimal intervention. From "
        "limestone-over-clay soils in the heart of Bairrada: lighter ruby, with dried "
        "cherry, red plum, dried herb, and an earthy mineral character. The wine's natural "
        "approach preserves Baga's freshness without the aggressive tannin of traditional "
        "Bairrada. Ready at 3-5 years; drinks beautifully for 10 years."
    ),
    price_tier="mid_range"
)

SIDONIO_BAGA = PROD(
    "Sidonio de Sousa Bairrada Garrafeira",
    "wine_still", SIDONIO, BAIRRADA, "Portugal",
    subcategory="red",
    description=(
        "Sidonio de Sousa's traditional Bairrada Garrafeira is one of the most challenging "
        "and ultimately rewarding wines in Portugal — Baga in its most uncompromising form. "
        "Heavy clay soils produce wine of formidable tannic structure: dark cherry, bitter "
        "chocolate, leather, tar, and dried herb with a tannin backbone that requires "
        "10-15 years. At full maturity, the Garrafeira rivals aged Barolo and traditional "
        "Rioja Gran Reserva for complexity and structure. A wine for collectors and "
        "sommeliers who understand Portugal's most underrated red wine tradition."
    ),
    price_tier="premium"
)

# ─── VINHO VERDE DEPTH ───────────────────────────────────────────────────────
print("\n=== VINHO VERDE DEPTH ===")

ANSELMO_MENDES = P(
    "Anselmo Mendes", "winery", VINHO_VERDE, "Portugal",
    production_philosophy="Vinho Verde specialist — from simple Vinho Verde to single-vineyard Alvarinho",
    philosophy_description=(
        "Anselmo Mendes is the most respected Vinho Verde specialist in Portugal — "
        "producing wines across the full range of the appellation from accessible, "
        "fresh Loureiro-based Vinho Verde to highly concentrated single-vineyard "
        "Alvarinho from the Monção e Melgaço subzone. The 'Parcela Única' single-vineyard "
        "Alvarinho is produced from a single parcel of old-vine Alvarinho on granite soils "
        "above the Lima River — a wine of extraordinary mineral depth and aging potential "
        "that rivals Soalheiro and Do Ferreiro for seriousness. Mendes's work helped "
        "establish Alvarinho's international reputation."
    ),
    reputation_narrative=(
        "Anselmo Mendes is the most important producer in Vinho Verde for establishing the "
        "appellation's premium credentials — Parcela Única Alvarinho is among the finest "
        "white wines produced in northern Portugal."
    ),
    price_positioning="premium"
)

QUINTA_CRASTO_VV = P(
    "Quinta de Gomariz", "winery", VINHO_VERDE, "Portugal",
    production_philosophy="Single-estate Vinho Verde from Lima subzone — Loureiro specialist",
    philosophy_description=(
        "Quinta de Gomariz in the Lima subzone is one of Vinho Verde's most respected "
        "single estates — farming Loureiro on granite soils to produce wines of remarkable "
        "aromatic complexity and mineral freshness. The estate Vinho Verde Loureiro shows "
        "the variety's characteristic white flower, citrus, and mineral character at its "
        "most expressive. The Seleção de Vinhas Velhas (old vine selection) demonstrates "
        "that Vinho Verde can achieve complexity and concentration rarely associated with "
        "the appellation's light, fresh reputation."
    ),
    reputation_narrative=(
        "Quinta de Gomariz is one of Vinho Verde's most admired estate producers — "
        "a reference for Loureiro in the Lima subzone's granite terroir."
    ),
    price_positioning="mid_range"
)

ANSELMO_PARCELA = PROD(
    "Anselmo Mendes Parcela Única Alvarinho",
    "wine_still", ANSELMO_MENDES, VINHO_VERDE, "Portugal",
    subcategory="white",
    description=(
        "Anselmo Mendes' Parcela Única is among the most serious expressions of Alvarinho "
        "from Monção e Melgaço — a single-vineyard from old-vine Alvarinho on granite soils "
        "above the Lima River. The wine transcends the fresh, immediate style of standard "
        "Vinho Verde: white peach, apricot, jasmine, and deep granite mineral with a "
        "structure that ages beautifully for 5-10 years. Rivals Soalheiro for concentration "
        "and mineral depth at the Alvarinho appellation's summit."
    ),
    price_tier="premium"
)

GOMARIZ_LOUREIRO = PROD(
    "Quinta de Gomariz Vinho Verde Loureiro",
    "wine_still", QUINTA_CRASTO_VV, VINHO_VERDE, "Portugal",
    subcategory="white",
    description=(
        "Quinta de Gomariz's Vinho Verde Loureiro from the Lima subzone is one of Portugal's "
        "most refreshing and aromatics-driven white wines: white blossom, lime zest, peach, "
        "and a granite mineral freshness unique to the Lima's granitic soils. The wine's "
        "natural acidity and vibrant aromatics make it one of the world's great seafood "
        "and aperitif wines. Drink within 2-3 years for maximum aromatic expression."
    ),
    price_tier="mid_range"
)

# ─── BAIRRADA VINTAGES (missing!) ─────────────────────────────────────────────
print("\n=== BAIRRADA VINTAGES ===")
V(BAIRRADA, 2013, 94, "exceptional",
  "A legendary Bairrada vintage — the finest for Baga in a generation. The cool, rainy "
  "Atlantic climate produced perfect conditions for the variety's demanding character: "
  "full natural acidity, structured tannin, and extraordinary mineral precision from the "
  "clay soils. Luis Pato's 2013 Baga wines are considered reference points for the "
  "appellation's greatest potential. Age 15-25 years with confidence.",
  "rising", 2020, 2038)

V(BAIRRADA, 2015, 92, "excellent",
  "A warm, precocious Bairrada vintage that produced more immediately accessible Baga "
  "than the cool-climate norm. The heat managed to ripen the thick-skinned Baga while "
  "retaining good acidity. Best drunk 2020-2028; less age-worthy than 2013 but showing "
  "the variety's dark fruit character in a more generous, approachable form.",
  "stable", 2018, 2028)

V(BAIRRADA, 2017, 91, "excellent",
  "Good Bairrada vintage with consistent quality across the appellation. The Atlantic "
  "influence moderated the warm conditions of the year, preserving the characteristic "
  "Baga acidity. Wines are approachable at 5-8 years and will drink well to 2027.",
  "stable", 2022, 2027)

V(BAIRRADA, 2019, 93, "exceptional",
  "Outstanding Bairrada vintage — an ideal Atlantic growing season produced Baga of "
  "pristine mineral precision and natural acidity. Filipa Pato and Sidonio de Sousa "
  "produced benchmark wines from this vintage. The clay-limestone terroir expressed "
  "its mineral character at its most defined. Age-worthy for 15-20 years.",
  "stable", 2024, 2035)

V(BAIRRADA, 2021, 90, "excellent",
  "Classic Bairrada vintage: cool, Atlantic, with Baga's characteristic high acidity "
  "and tannic structure. The wines need time — 8-12 years minimum for the best "
  "expressions to integrate. Drink 2029-2033 for full maturity.",
  "stable", 2029, 2033)

# ─── PAIRINGS ─────────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Alentejo pairings
PAIR(ESPORAO_WHITE, "Grilled swordfish with lemon, olive oil, and capers",
    "complement", "classic", "fish_course",
    "Esporão Reserva Branco's lemon curd and oak complexity pairs beautifully with "
    "grilled swordfish — the wine's acidity cuts through the fish's meaty richness; "
    "capers amplify the wine's mineral character; olive oil bridges the Alentejo's "
    "Mediterranean heritage with the fish's texture. One of Portugal's great white "
    "wine and fish pairings.")

PAIR(ESPORAO_WHITE, "Roasted cod (bacalhau) with olive oil, garlic, and potato",
    "complement", "classic", "main",
    "Esporão Reserva Branco and bacalhau: the quintessential Portuguese white wine pairing. "
    "The wine's lemon and mineral character cuts through the salt cod's richness; garlic "
    "amplifies the wine's aromatic complexity; olive oil bridges the Alentejo's warmth "
    "with the cod's classic preparation. A pairing of Portuguese national identity.")

PAIR(MOUCHAO_TINTO, "Slow-braised Alentejo black pork with lentils and chouriço",
    "complement", "classic", "main",
    "Herdade do Mouchão's traditional Alentejo Tinto achieves its natural home with "
    "black Alentejo pork — the most celebrated local ingredient. The wine's cedar, plum, "
    "and dried herb character amplifies the pork's distinctive earthy richness; chouriço "
    "adds smoked paprika depth; lentils provide the earthy base for the wine's mineral "
    "character. A pairing of deep Alentejo cultural and culinary identity.")

PAIR(MOUCHAO_TINTO, "Grilled Ibérico presa steak with piri-piri and tomato salad",
    "complement", "established", "main",
    "Mouchão Tinto's old-vine Trincadeira and Aragonez structure provides the perfect "
    "counterpart to Ibérico pork's extraordinary marbled fat. The wine's tannin integrates "
    "with the fat while its dried herb character amplifies piri-piri's aromatic heat; "
    "tomato salad provides the acidic freshness that bridges wine and rich pork.")

PAIR(PECEGUINA_RED, "Roasted free-range chicken with chickpeas and paprika",
    "complement", "classic", "main",
    "Monte da Peceguina's lighter, fresher Alentejo red finds its ideal regional pairing "
    "with roasted chicken and chickpeas — a Portuguese staple. The wine's red cherry and "
    "dried herb character integrates naturally with the chicken's simplicity; paprika "
    "amplifies the wine's earthy character; chickpeas provide the starchy base that "
    "this accessible, food-friendly wine was designed to accompany.")

PAIR(PECEGUINA_RED, "Pan-fried cured pork tenderloin (lombo) with migas and greens",
    "complement", "classic", "casual",
    "Peceguina Tinto and traditional Alentejo migas — the most honest Portuguese pairing. "
    "The wine's fresh red fruit and mineral character bridges the cured pork's richness "
    "while cutting through the fried breadcrumb migas. Greens provide freshness that "
    "amplifies the wine's herbal character. A pairing rooted in Alentejo's peasant tradition.")

# Bairrada pairings
PAIR(FILIPA_CALCARIO, "Leitão da Bairrada (Bairrada suckling pig) with orange and herbs",
    "complement", "classic", "main",
    "The most authentic Bairrada pairing: leitão (suckling pig roasted until the skin "
    "is shatteringly crispy) and Filipa Pato's lighter-style Baga. The wine's dried "
    "cherry and herbal precision cuts through the rich, fatty pig skin while the "
    "granite mineral echoes the crackling's mineral character. Orange amplifies the "
    "wine's citrus freshness. A pairing of absolute regional identity.")

PAIR(FILIPA_CALCARIO, "Smoked duck breast with beetroot and aged vinegar",
    "complement", "established", "starter",
    "Filipa Pato's natural Baga — lighter and fresher than traditional Bairrada — "
    "finds an elegant pairing with smoked duck breast. The wine's dried cherry and "
    "earthy herb character bridges the smoke; beetroot's earthy sweetness amplifies "
    "the wine's mineral note; aged vinegar provides the acid bridge. A sophisticated "
    "Bairrada pairing for the natural wine enthusiast.")

PAIR(SIDONIO_BAGA, "Slow-roasted shoulder of beef with carrots and bay leaf",
    "complement", "classic", "main",
    "Sidonio de Sousa's traditional Bairrada Garrafeira — at 10-15 years — achieves its "
    "finest expression with slow-roasted beef. The wine's extraordinary tannin has "
    "softened into leather and cedar; the beef's collagen-rich slow cooking provides "
    "the fat that integrates the wine's structure. Bay leaf echoes the wine's dried "
    "herb character; carrots provide sweetness that bridges the wine's tannin. "
    "A pairing of traditional Portuguese wine and French-influenced braising tradition.")

PAIR(SIDONIO_BAGA, "Aged Serra da Estrela cheese",
    "complement", "established", "cheese",
    "Sidonio de Sousa Garrafeira's mature tannic structure finds its match in Serra da "
    "Estrela — Portugal's greatest cheese. The wine's leather and tobacco complexity "
    "amplifies the cheese's buttery depth; the tannin cuts through the fat; the wine's "
    "mineral character bridges with the sheep's milk terroir. A pairing of Portugal's "
    "most age-worthy red with its most celebrated cheese.")

# Vinho Verde pairings
PAIR(ANSELMO_PARCELA, "Steamed barnacles (percebes) with lemon and sea salt",
    "complement", "classic", "starter",
    "Anselmo Mendes Parcela Única Alvarinho and percebes: the Minho's definitive pairing. "
    "The wine's granite mineral depth mirrors the barnacle's oceanic brine; its floral "
    "aromatics and citrus precision amplify the percebes' pure marine flavour. Sea salt "
    "bridges the wine's mineral salinity. A pairing that defines northern Portuguese "
    "coastal wine culture.")

PAIR(ANSELMO_PARCELA, "Bacalhau à Brás (salt cod with egg, potato, and olives)",
    "complement", "classic", "main",
    "Anselmo Mendes Parcela Única's mineral concentration and acidity makes it one of "
    "the most versatile Portuguese white wines — including with bacalhau à Brás. The "
    "wine's stone fruit and mineral character cuts through the egg's richness; olives "
    "bridge the wine's Mediterranean mineral; the potato absorbs the wine's acidity "
    "into a complete harmony. A traditional Minho pairing with Portugal's most beloved dish.")

PAIR(GOMARIZ_LOUREIRO, "Grilled sardines with lemon and sea salt",
    "complement", "classic", "main",
    "Quinta de Gomariz Loureiro and freshly grilled sardines: the most Portuguese "
    "of all pairings. The wine's white blossom and lime zest character amplifies "
    "the sardine's oil and brine; sea salt bridges the wine's mineral freshness; "
    "lemon echoes the Loureiro's characteristic citrus precision. A pairing of "
    "absolute national authenticity — fresh Vinho Verde and Atlantic sardines.")

PAIR(GOMARIZ_LOUREIRO, "Steamed cockles with garlic, white wine, and coriander",
    "complement", "classic", "starter",
    "Vinho Verde Loureiro and cockles: a classic northern Portuguese pairing. The wine's "
    "vibrant acidity and floral aromatics match the cockles' brine; garlic and coriander "
    "amplify the wine's aromatic freshness; white wine in the sauce creates perfect "
    "self-referential harmony. The most refreshing shellfish pairing in the Portuguese canon.")

cur.close()
conn.close()
print("\n✅ Terminal 16 Batch 1 — Portuguese depth complete.")
