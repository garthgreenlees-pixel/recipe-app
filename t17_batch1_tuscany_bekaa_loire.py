#!/usr/bin/env python3
"""Terminal 17 — Batch 1: Tuscany + Bekaa Valley + Loire + Fronsac + Vallée de la Marne
Adds second wine producers/products to single-product international regions.
"""
import psycopg2

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# ── helpers ────────────────────────────────────────────────────────────────────

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
    print(f"  ✓ Producer [{pid}]: {name}")
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
    print(f"  ✓ Product [{pid}]: {name}")
    return pid

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR [{product_id}]: {food_description[:55]}...")

print("=== T17 BATCH 1: TUSCANY + BEKAA + LOIRE + FRONSAC + VALLÉE DE LA MARNE ===\n")

# ═══════════════════════════════════════════════════════════════════════════════
# TUSCANY (region 165) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── TUSCANY — Masseto ──")
p_masseto = P(
    "Masseto",
    "winery", 165, "Italy",
    production_philosophy="Tuscany's most celebrated Merlot: a single-vineyard icon from the Ornellaia estate producing Italy's answer to Pomerol",
    philosophy_description=(
        "Masseto is Italy's most extraordinary Merlot — a single-vineyard estate carved from the original "
        "Ornellaia property in Bolgheri, now entirely dedicated to a 7.2-hectare parcel of deep blue clay "
        "soils that represent the ideal terroir for Merlot. Separated from Ornellaia as an independent "
        "estate in 2019, Masseto is now wholly owned by Frescobaldi. The wine has been produced since "
        "1986 — each vintage from a single bloc of clay-dominated soil that retains moisture in the coastal "
        "Maremma heat and produces Merlot of extraordinary concentration, texture, and depth. "
        "Masseto is Tuscany's collectible icon par excellence."
    ),
    reputation_narrative=(
        "Masseto is consistently rated among Italy's greatest wines by all major critics. Wine Advocate "
        "(Antonio Galloni, Eric Asimov) and Decanter award 95-100 points in exceptional vintages. "
        "It is one of Europe's most expensive and collectible wines — rivalling Pétrus and Le Pin in "
        "auction demand. Jancis Robinson cites Masseto as the definitive proof that Tuscany can produce "
        "world-class single-variety Merlot rivalling Pomerol at the highest level."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_masseto = PROD(
    "Masseto IGT Toscana",
    "wine_still", p_masseto, 165, "Italy",
    subcategory="red_merlot",
    description=(
        "Masseto is Italy's greatest Merlot — produced from a single 7.2-hectare parcel of blue clay "
        "on the Bolgheri coast that provides the ideal microclimate for the variety. Deep opaque ruby "
        "with black cherry, plum, mocha, chocolate, cassis, and a velvety texture of extraordinary "
        "density. The wine has a Pomerol-like plushness combined with the energy of the Tuscan coast. "
        "Requires 15-20 years' aging for full expression — among Italy's most age-worthy wines."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_masseto,
    "Pan-roasted Wagyu bavette with Barolo reduction and celeriac",
    "elevate", "established", "main",
    "Masseto's extraordinary Merlot concentration and velvety depth demands a protein of matching "
    "intensity: aged Wagyu bavette provides the fat-marbling and depth that can absorb and elevate "
    "the wine's structure. Barolo reduction bridges Tuscany's wine heritage with the dish; celeriac "
    "provides earthy balance. A pairing that positions Masseto at the absolute peak of Italian "
    "wine-food luxury — the Pomerol-meets-Tuscany experience.")
PAIR(prod_masseto,
    "Truffled tagliatelle with Parmigiano Reggiano and aged Comté",
    "complement", "established", "main",
    "Masseto's plush Merlot concentration and mocha depth achieves remarkable harmony with fresh "
    "truffled pasta — one of Tuscany's most luxurious pairings. The wine's velvety texture mirrors "
    "the pasta's silk; black truffle amplifies Masseto's earthy secondary character; Parmigiano's "
    "crystalline umami depth creates a wine-food bridge of profound luxury. An unexpected but "
    "classically aligned pairing for Italy's most opulent red wine.")

# ═══════════════════════════════════════════════════════════════════════════════
# BEKAA VALLEY (region 182) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── BEKAA VALLEY — Château Ksara ──")
p_ksara = P(
    "Château Ksara",
    "winery", 182, "Lebanon",
    production_philosophy="Lebanon's oldest and largest winery: 2,000-year-old cellars in the Bekaa Valley producing Lebanon's most historically significant wines",
    philosophy_description=(
        "Château Ksara is Lebanon's most historically significant winery — founded in 1857 by Jesuit monks "
        "who discovered Roman-era underground cellars at the site, now used for wine aging. The estate holds "
        "300 hectares of vineyard across the Bekaa Valley at 1,000m altitude, producing wines from Cabernet "
        "Sauvignon, Merlot, Syrah, Chardonnay, and the indigenous Obaideh grape. Their Château Ksara white "
        "from Chardonnay and Muscat Blanc is one of the Middle East's most refined white wines — a reminder "
        "that the Bekaa Valley's altitude and continental climate suits white varieties of surprising elegance."
    ),
    reputation_narrative=(
        "Château Ksara is Lebanon's most internationally distributed fine wine — exported to 35+ countries "
        "and a regular in Michelin-starred restaurant lists across Europe and the Gulf states. Wine Advocate "
        "and Decanter have covered the estate's 150-year history as an emblem of Lebanon's winemaking "
        "tradition. Their Blanc de l'Observatoire is considered the benchmark for Lebanese white wine."
    ),
    price_positioning="mid_range",
    authority_tier=2
)

prod_ksara = PROD(
    "Château Ksara Blanc de l'Observatoire",
    "wine_still", p_ksara, 182, "Lebanon",
    subcategory="white",
    description=(
        "Château Ksara's Blanc de l'Observatoire is Lebanon's most refined white wine — a blend of "
        "Chardonnay and Muscat Blanc vinified separately and unified in old oak. Pale gold with "
        "apricot, citrus blossom, honey, and a distinctive mineral salinity from the Bekaa Valley's "
        "limestone soils at 1,000m altitude. The wine has unusual elegance for the region — aromatic "
        "intensity of Muscat with Chardonnay's textural weight and mineral freshness."
    ),
    price_tier="mid_range"
)
PAIR(prod_ksara,
    "Mezze of labneh, fattoush, hummus, and grilled halloumi",
    "complement", "classic", "starter",
    "Château Ksara Blanc de l'Observatoire's citrus blossom and mineral character is the natural "
    "companion to the Levantine mezze tradition — the wine's apricot aromatics amplify labneh's "
    "subtle tang; the mineral acidity bridges fattoush's lemon dressing; hummus' earthy depth "
    "is refreshed by the wine's citrus precision. The Muscat's aromatic character echoes the "
    "Middle Eastern spice palette. A pairing of complete regional identity.")
PAIR(prod_ksara,
    "Grilled sea bass with chermoula and preserved lemon",
    "complement", "established", "fish_course",
    "Ksara Blanc's Chardonnay-Muscat blend finds a natural match with chermoula-dressed grilled "
    "sea bass — a bridge between Lebanese coastal cuisine and North African spice tradition. "
    "The wine's citrus blossom character amplifies preserved lemon's aromatic complexity; "
    "chermoula's herb-spice profile bridges the wine's aromatic personality; sea bass's "
    "delicate white flesh benefits from the wine's weight without being overwhelmed.")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVENNIÈRES (region 154) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── SAVENNIÈRES — Domaine des Baumard ──")
p_baumard = P(
    "Domaine des Baumard",
    "winery", 154, "France",
    production_philosophy="Savennières's most technically accomplished estate: old-vine Chenin Blanc from Clos Saint-Yves and La Genièvre producing the appellation's most food-friendly wines",
    philosophy_description=(
        "Domaine des Baumard is one of Savennières's most important estates — a 35-hectare holding that "
        "encompasses the prestigious Clos du Papillon, Clos Saint-Yves, and La Genièvre parcels on "
        "Savennières's volcanic schist slopes. Unlike the biodynamic extremes of Nicolas Joly's Coulee de "
        "Serrant, Baumard's approach is precise and technically meticulous: temperature-controlled ferment, "
        "indigenous yeasts, and careful sulphur management. The result is Chenin Blanc of extraordinary "
        "mineral precision and age-worthiness without the oxidative risk of natural production. "
        "Their Clos du Papillon is the finest wine — a 9-hectare Savennières monopole of legendary quality."
    ),
    reputation_narrative=(
        "Domaine des Baumard is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Loire specialist "
        "Jacky Blot as Savennières's most consistent producer — a counterpoint to Nicolas Joly's biodynamic "
        "philosophy with equally compelling results. Their Clos du Papillon and Clos Saint-Yves demonstrate "
        "that Savennières Chenin Blanc can achieve extraordinary complexity, minerality, and age-worthiness "
        "through technical precision rather than radical natural winemaking."
    ),
    price_positioning="premium",
    authority_tier=1
)

prod_baumard = PROD(
    "Domaine des Baumard Savennières Clos du Papillon",
    "wine_still", p_baumard, 154, "France",
    subcategory="white_chenin_blanc",
    description=(
        "Baumard's Clos du Papillon is Savennières at its most elegant: a 9-hectare monopole on volcanic "
        "schist slopes producing Chenin Blanc of extraordinary mineral precision. Pale gold with quince, "
        "beeswax, white peach, oyster shell mineral, and a distinctive schist salinity. The wine is "
        "dry, complex, and hauntingly mineral — demonstrating Savennières's ability to produce the "
        "Loire's most compelling dry Chenin Blanc. Develops extraordinary complexity over 10-20 years."
    ),
    price_tier="premium"
)
PAIR(prod_baumard,
    "Roasted turbot with beurre blanc and samphire",
    "complement", "classic", "fish_course",
    "Domaine des Baumard Savennières Clos du Papillon's dry Chenin minerality and beeswax depth "
    "achieves the Loire's most celebrated fish pairing with turbot and beurre blanc. The wine's "
    "oyster-shell mineral character bridges the turbot's oceanic depth; beurre blanc amplifies "
    "the Chenin's natural richness; samphire's maritime salinity echoes the wine's Loire mineral "
    "character. A classic Loire fish pairing of complete regional identity.")
PAIR(prod_baumard,
    "Veal sweetbreads with morels, cream, and chervil",
    "complement", "established", "main",
    "Baumard Clos du Papillon's textural richness and quince complexity finds a distinguished partner "
    "in veal sweetbreads with morel mushrooms — one of Savennières's most elevated food pairings. "
    "The wine's beeswax and quince character bridges the sweetbread's delicate richness; morels' "
    "earthy depth echoes the Chenin's mineral complexity; cream softens the wine's structured acidity. "
    "A pairing of Loire gastronomic tradition at its most refined.")

# ═══════════════════════════════════════════════════════════════════════════════
# MUSCADET / PAYS NANTAIS (region 148) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── MUSCADET — Luneau-Papin ──")
p_luneau = P(
    "Domaine Luneau-Papin",
    "winery", 148, "France",
    production_philosophy="Muscadet's intellectual benchmark: single-vineyard Melon de Bourgogne from Sèvre et Maine's best granite terroirs, aged sur lie for 3-10 years",
    philosophy_description=(
        "Domaine Luneau-Papin is Muscadet's quality benchmark — the Luneau-Papin family hold 30 hectares "
        "of the finest Sèvre et Maine terroirs: granite, gneiss, and gabbro soils that produce Melon de "
        "Bourgogne of extraordinary minerality. Their L d'Or cuvée is aged on lees for 3+ years in foudre "
        "before release — the extended sur lie contact developing complex autolytic notes alongside Muscadet's "
        "signature mineral freshness. Their 'Vieilles Vignes' and single-parcel expressions (Orthogneiss, "
        "Le L d'Or) have redefined expectations for what Muscadet can achieve."
    ),
    reputation_narrative=(
        "Domaine Luneau-Papin is cited by Jancis Robinson, Wine Advocate (Neal Martin), and Revue du Vin "
        "de France as the producer most responsible for elevating Muscadet's international reputation. "
        "Their extended sur lie cuvées consistently score 90-94 and demonstrate that Muscadet can achieve "
        "genuine complexity — competing with Chablis premier cru and Burgundy Aligoté for serious sommeliers "
        "seeking mineral Loire whites at accessible price points."
    ),
    price_positioning="mid_range",
    authority_tier=1
)

prod_luneau = PROD(
    "Luneau-Papin Le L d'Or Muscadet Sèvre et Maine Sur Lie",
    "wine_still", p_luneau, 148, "France",
    subcategory="white_melon_de_bourgogne",
    description=(
        "Luneau-Papin's Le L d'Or is Muscadet at its most complex: Melon de Bourgogne from 60+ year old "
        "vines on granite and gneiss soils in Sèvre et Maine, aged 36+ months on lees in foudre. "
        "Pale gold with oyster shell, citrus, white flowers, yeast-lees autolytic complexity, and a "
        "saline mineral finish of extraordinary precision. The extended sur lie contact transforms "
        "Muscadet's characteristic freshness into genuine complexity. A world-class mineral white."
    ),
    price_tier="premium"
)
PAIR(prod_luneau,
    "Oysters Rockefeller with spinach, Pernod, and breadcrumb gratin",
    "complement", "classic", "starter",
    "Luneau-Papin Le L d'Or's oyster-shell mineral and saline autolytic character achieves the "
    "Loire's most instinctive pairing — Muscadet sur lie with native oysters. The wine's extended "
    "sur lie complexity amplifies the oyster's brine; spinach's earthy green note bridges the "
    "wine's mineral freshness; the Pernod-anise dimension echoes the wine's herbal Loire character. "
    "A pairing of complete Loire maritime harmony.")
PAIR(prod_luneau,
    "Moules marinières with white wine, shallots, and parsley",
    "complement", "classic", "starter",
    "Luneau-Papin Le L d'Or's mineral freshness and oyster character is the textbook companion to "
    "moules marinières — one of Loire's most deeply traditional wine-food pairings. The wine's "
    "sur lie complexity amplifies the mussel's brine; the white wine in the marinière mirrors the "
    "Muscadet itself; shallot's sweetness bridges wine and cooking liquor. A pairing of the Loire "
    "seafood tradition at its most authentic and satisfying.")

# ═══════════════════════════════════════════════════════════════════════════════
# FRONSAC (region 130) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── FRONSAC — Château Fontenil ──")
p_fontenil = P(
    "Château Fontenil",
    "winery", 130, "France",
    production_philosophy="Michel Rolland's personal Fronsac estate: precise Merlot-Cabernet Franc blends demonstrating Fronsac's finest clay-limestone terroir",
    philosophy_description=(
        "Château Fontenil is the personal estate of Michel Rolland — Bordeaux's most celebrated consultant "
        "winemaker — and his wife Dany. The 9-hectare estate in Fronsac is farmed on clay-limestone soils "
        "ideally suited to Merlot: the variety that defines Fronsac's most successful wines. Fontenil is "
        "the showcase for Rolland's philosophy at his most personal: meticulous vine management, late "
        "harvesting for full phenolic maturity, and precision winemaking that extracts Fronsac's terroir "
        "character without over-extraction. The wine demonstrates that Fronsac can achieve quality "
        "comparable to Pomerol and Saint-Émilion at a fraction of the price."
    ),
    reputation_narrative=(
        "Château Fontenil is considered by Wine Advocate and Decanter as Fronsac's finest wine — the "
        "personal estate of the world's most influential wine consultant lends the property unique authority. "
        "Scoring regularly 91-95, Fontenil demonstrates Michel Rolland's ability to translate his global "
        "consulting philosophy into exceptional Bordeaux terroir expression. A benchmark for the quality "
        "potential of the often-overlooked Fronsac appellation."
    ),
    price_positioning="premium",
    authority_tier=2
)

prod_fontenil = PROD(
    "Château Fontenil Fronsac",
    "wine_still", p_fontenil, 130, "France",
    subcategory="red_merlot_blend",
    description=(
        "Château Fontenil is Michel Rolland's personal Fronsac — a Merlot-dominated blend (90%) with "
        "Cabernet Franc from clay-limestone soils at the foot of the Fronsac côte. Deep ruby with "
        "ripe plum, cassis, dark chocolate, cedar, and a mineral limestone freshness that lifts the "
        "wine's Merlot richness. The wine has Pomerol-like generosity combined with Fronsac's "
        "characteristic tannic firmness — requiring 6-10 years' aging for full expression."
    ),
    price_tier="premium"
)
PAIR(prod_fontenil,
    "Slow-braised lamb shoulder with root vegetables and thyme jus",
    "complement", "classic", "main",
    "Château Fontenil's Merlot-dominated Fronsac finds its natural pairing in slow-braised lamb — "
    "the collagen-rich shoulder softens the wine's firm clay-limestone tannin while amplifying "
    "its dark fruit. Root vegetables provide earthy sweetness; thyme jus bridges Bordeaux's herb "
    "dimension with the lamb's richness. A pairing that reveals Fronsac's resemblance to "
    "Pomerol in structure with a more rustic, satisfying character.")
PAIR(prod_fontenil,
    "Duck magret with fig reduction and pommes sarladaises",
    "complement", "established", "main",
    "Fontenil Fronsac's plum and cassis Merlot character achieves a natural Gascon pairing "
    "with duck magret — the breast's rendered fat integrates the wine's firm structure while "
    "fig reduction amplifies the Merlot's primary fruit. Pommes sarladaises provide the rich "
    "potato-duck fat base that Fronsac's tannin demands. A southwest Bordeaux pairing that "
    "showcases Fronsac's undervalued potential.")

# ═══════════════════════════════════════════════════════════════════════════════
# VALLÉE DE LA MARNE (region 146) — second wine product
# ═══════════════════════════════════════════════════════════════════════════════

print("\n── VALLÉE DE LA MARNE — Egly-Ouriet ──")
p_egly = P(
    "Egly-Ouriet",
    "winery", 146, "France",
    production_philosophy="The Marne Valley's greatest grower-Champagne: old-vine Pinot Meunier and Pinot Noir vinified with Burgundian precision and extended aging",
    philosophy_description=(
        "Egly-Ouriet is the Vallée de la Marne's most celebrated grower-Champagne producer — Francis "
        "Egly's 9-hectare domaine in Ambonnay and the Marne Valley represents grower Champagne at its "
        "most ambitious. His Blanc de Noirs Vieilles Vignes is made exclusively from 70+ year old Pinot "
        "Noir and Pinot Meunier vines, vinified in old barrel with indigenous yeasts and aged 4+ years "
        "on lees before disgorgement. The resulting Champagne has a depth and complexity that challenges "
        "many prestige cuvées — demonstrating the extraordinary potential of old-vine Pinot Meunier "
        "from the Marne Valley's chalky-clay terroir."
    ),
    reputation_narrative=(
        "Egly-Ouriet is considered by Terry Theise, Lyle Fass, and Peter Liem (Champagne Report) to be "
        "one of the 10 greatest Champagne producers. Their Blanc de Noirs Vieilles Vignes consistently "
        "scores 93-98 from Wine Advocate and Decanter — rivalling Jacques Selosse and Krug in complexity "
        "and depth. Allocation is extremely limited; the wines are held by the world's top Champagne "
        "sommeliers as benchmark grower expressions."
    ),
    price_positioning="ultra_premium",
    authority_tier=1
)

prod_egly = PROD(
    "Egly-Ouriet Blanc de Noirs Vieilles Vignes Champagne",
    "wine_sparkling", p_egly, 146, "France",
    subcategory="blanc_de_noirs",
    description=(
        "Egly-Ouriet's Blanc de Noirs Vieilles Vignes is one of Champagne's most profound wines: "
        "old-vine Pinot Noir and Pinot Meunier (70+ years) from the Marne Valley and Ambonnay, "
        "vinified in old barrique and aged 4+ years on lees. Deep gold with extraordinary complexity: "
        "red berry, brioche, hazelnut, mushroom, chalk, and umami depth. The wine has the structure "
        "of a great Burgundy with Champagne's mineral precision. One of the grower Champagne world's "
        "greatest expressions. Extremely limited allocation."
    ),
    price_tier="ultra_premium"
)
PAIR(prod_egly,
    "Roasted Bresse chicken with black truffle and jus gras",
    "elevate", "established", "main",
    "Egly-Ouriet Blanc de Noirs Vieilles Vignes — with its extraordinary Pinot Noir depth and "
    "red berry-mushroom complexity — achieves one of Champagne's most ambitious food pairings "
    "with roasted Bresse chicken and truffle. The wine's structured Pinot character stands up to "
    "the richness of truffle-stuffed chicken; jus gras amplifies the Champagne's umami depth; "
    "the wine's extended lees aging creates a textural bridge with the roasted skin. "
    "A grower Champagne pairing of extraordinary ambition.")
PAIR(prod_egly,
    "Lightly smoked duck breast with cherry and hazelnut",
    "complement", "established", "main",
    "Egly-Ouriet Blanc de Noirs' red berry character and brioche-hazelnut complexity achieves "
    "remarkable harmony with smoked duck breast — the wine's Pinot Noir depth supports the duck's "
    "smoke character while cherry amplifies the wine's red fruit. Hazelnut echoes the Champagne's "
    "autolytic complexity. A pairing that positions grower Champagne as a genuine fine dining red "
    "wine alternative — pushing Champagne's versatility to its most ambitious expression.")

# ─────────────────────────────────────────────────────────────────────────────
cur.close()
conn.close()
print(f"\n✅ T17 Batch 1 complete — 6 producers, 6 products, 12 pairings.")
print("Regions covered: Tuscany, Bekaa Valley, Savennières, Muscadet, Fronsac, Vallée de la Marne")
