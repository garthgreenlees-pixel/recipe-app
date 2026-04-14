#!/usr/bin/env python3
"""Terminal 9 — Batch 3: Refs + Pairings for NZ, Australia, Napa, Argentina, SA"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

def REF(name, category, description, authority_tier=1):
    cur.execute("SELECT id FROM beverage_references WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        print(f"  ~ EXISTS: {name} (id={row[0]})")
        return row[0]
    cur.execute("""
        INSERT INTO beverage_references (name, category, description, authority_tier)
        VALUES (%s,%s,%s,%s) RETURNING id
    """, (name, category, description, authority_tier))
    row = cur.fetchone()
    print(f"  ✓ REF: {name} (id={row[0]})")
    return row[0]

def PAIR(product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier=1):
    cur.execute("""
        INSERT INTO pairing_intelligence
          (beverage_product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (product_id, food_description, pairing_type, confidence, meal_context, flavour_logic, authority_tier))
    print(f"    ✓ PAIR: {food_description[:50]}... → product {product_id}")

def get_product(name):
    cur.execute("SELECT id FROM beverage_products WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"Product not found: {name}")

# ─── REFS ────────────────────────────────────────────────────────────────
print("=== BEVERAGE REFERENCES ===")

REF("New Zealand wine: Marlborough Sauvignon Blanc and Central Otago Pinot Noir",
    "wine_regions",
    "New Zealand's wine identity is defined by two regions and two grapes. Marlborough Sauvignon Blanc — created commercially by Cloudy Bay in 1985 — is the world's most distinctive varietal expression: intensely thiolic (passion fruit, guava), methoxypyrazi (capsicum, green bean), and razor-edged in acidity from the Wairau Valley floor. Wild-fermented expressions (Greywacke Wild Sauvignon, Dog Point Section 94) add Burgundian texture and complexity rarely seen in the category. Central Otago, the world's southernmost Pinot Noir region, produces from schist soils at 280-350m altitude: more powerful and structural than Marlborough Pinot, with dark fruit, cracked pepper, and iron mineral. Bannockburn (Mt Difficulty) is the most powerful sub-region; Wānaka (Rippon) the most delicate. Biodynamic farming is well-established in both regions.")

REF("Australian Shiraz: Barossa Valley and McLaren Vale old-vine terroir",
    "wine_regions",
    "Australia's most celebrated red wine category spans two distinct South Australian regions. Barossa Valley (Eden Valley foothills): the world's oldest continuously harvested Shiraz vines, some planted 1840s. Ancient dry-farmed bushvines on clay, ironstone, and alluvial soils produce Shiraz of extraordinary concentration. Penfolds Grange defined the style (rich, complex, American oak); Torbreck RunRig introduced the Rhône co-fermentation model. Sub-regional differences are dramatic: Marananga (warmer, richer), Eden Valley (cooler, more aromatic). McLaren Vale (30km south of Adelaide): maritime-influenced, with Blewett Springs sand-over-limestone producing the most delicate Australian Grenache (Yangarra High Sands). d'Arenberg's The Dead Arm demonstrates McLaren Vale's capacity for deeply concentrated old-vine Shiraz. The Bushard Vineyard (Chapel Hill) shows centenarian-vine intensity. Australian wine law requires 85% of stated region on label.")

REF("Napa Valley Cabernet Sauvignon: sub-regional terroir and the California benchmark",
    "wine_regions",
    "Napa Valley is California's benchmark Cabernet Sauvignon appellation — but the 30-mile-long valley contains dramatically different sub-regional terroir expressions. Rutherford Bench: deep clay loam producing the 'Rutherford Dust' tannin character — plush, full-bodied, accessible (Caymus). Stags Leap District: cooler, palisade-protected, producing Cabernet of exceptional elegance and structure (Stag's Leap Wine Cellars won the 1976 Paris Tasting blind). Oakville/Spring Mountain: diverse, home to Martha's Vineyard (Heitz) and Opus One. Key benchmark year: 1976 Judgment of Paris — Stag's Leap 1973 Cabernet defeated Bordeaux First Growths in a blind tasting, permanently legitimizing California fine wine. Napa's warm days and cool nights (diurnal swing up to 25°F) create the fruit ripeness and acid balance characteristic of the region's best Cabernets. Russian River Valley (Sonoma): the California benchmark for Pinot Noir — warm days, cool foggy afternoons, free-draining loam. Williams Selyem established the cult Pinot standard.")

# ─── PAIRINGS ─────────────────────────────────────────────────────────────
print("\n=== PAIRING INTELLIGENCE ===")

# Load product IDs
GW_WILD  = get_product("Greywacke Wild Sauvignon Blanc")
GW_STD   = get_product("Greywacke Sauvignon Blanc")
DP_94    = get_product("Dog Point Section 94 Sauvignon Blanc")
DP_STD   = get_product("Dog Point Vineyard Sauvignon Blanc")
SER_LEAH = get_product("Seresin Leah Pinot Noir")
MTD_BAN  = get_product("Mt Difficulty Bannockburn Pinot Noir")
MTD_LG   = get_product("Mt Difficulty Long Gully Single Vineyard Pinot Noir")
RIPPON   = get_product("Rippon Mature Vine Pinot Noir")
ACHAV    = get_product("Achaval Ferrer Malbec")
FINCA    = get_product("Achaval Ferrer Finca Altamira Single Vineyard Malbec")
CLOS     = get_product("Clos de los Siete Red Blend")
MULL_W   = get_product("Mullineux Signature White")
MULL_S   = get_product("Mullineux Swartland Syrah")
JORD     = get_product("Jordan Nine Yards Chardonnay")
RUNRIG   = get_product("Torbreck RunRig Shiraz Viognier")
STEADING = get_product("Torbreck The Steading")
ARES     = get_product("Two Hands Ares Shiraz")
HIGH_SDS = get_product("Yangarra High Sands Grenache")
YANG_SH  = get_product("Yangarra Estate Shiraz")
CHAPEL   = get_product("Chapel Hill Bushard Vineyard Shiraz")
MAC_PN   = get_product("Mac Forbes Woori Yallock Pinot Noir")
MAC_CH   = get_product("Mac Forbes Chardonnay")
DEB_PN   = get_product("De Bortoli Lusatia Park Vineyard Pinot Noir")
HEITZ    = get_product("Heitz Martha's Vineyard Cabernet Sauvignon")
CASK23   = get_product("Stag's Leap CASK 23 Cabernet Sauvignon")
SLV      = get_product("Stag's Leap S.L.V. Estate Cabernet Sauvignon")
CAY_SS   = get_product("Caymus Special Selection Cabernet Sauvignon")
CAY_NV   = get_product("Caymus Napa Valley Cabernet Sauvignon")
WS_ALLEN = get_product("Williams Selyem Allen Vineyard Pinot Noir")
print(f"Product IDs loaded: GW_WILD={GW_WILD}, DP_94={DP_94}, MTD_BAN={MTD_BAN}, RUNRIG={RUNRIG}, CASK23={CASK23}")

# Marlborough Sauvignon Blanc pairings
PAIR(GW_WILD, "Seared scallops with cauliflower purée and sea herbs",
    "elevate", "established", "starter",
    "The wild-fermented complexity and creamy texture of Greywacke Wild SB provides the textural bridge that conventional Marlborough SB cannot — the lees richness mirrors the cauliflower purée while the inherent SB acidity cuts through the scallop's sweetness.")

PAIR(GW_STD, "Baked green asparagus with hollandaise",
    "complement", "classic", "starter",
    "Classic Marlborough SB and asparagus pairing — the methoxypyrazine character of the wine amplifies the asparagus's vegetal notes while the wine's crisp acidity cuts the hollandaise's richness. The textbook expression of why Sauvignon Blanc was made for asparagus.")

PAIR(DP_94, "Braised turbot with white asparagus and beurre blanc",
    "elevate", "established", "fish_course",
    "Dog Point Section 94's wild-fermented weight and Burgundian texture demands a dish of comparable substance — the braised turbot provides the delicate richness while white asparagus echoes the wine's mineral, slightly saline character. The beurre blanc bridges the oak and lees texture.")

PAIR(DP_STD, "Roast chicken with herbs and lemon",
    "complement", "classic", "main",
    "The biodynamic estate precision of Dog Point standard SB shines alongside simple roast chicken — the wine's citrus and herb character mirrors the preparation while the acid cuts the chicken fat. Timeless, accessible, and completely satisfying.")

# Central Otago Pinot Noir pairings
PAIR(MTD_BAN, "Roasted duck breast with cherry jus and celeriac",
    "complement", "classic", "main",
    "Bannockburn Pinot Noir's dark fruit, structure, and schist minerality pairs classically with duck — the cherry jus echoes the wine's fruit, the schist tannins cut through duck fat, and the celeriac's earthiness matches the wine's savory depth.")

PAIR(MTD_LG, "Braised venison shoulder with juniper and root vegetables",
    "complement", "established", "main",
    "Long Gully's concentrated power and extended maceration structure demands a dish of comparable substance — braised venison's deep umami and gaminess are the perfect match for this dense, tannin-rich Pinot Noir. The juniper echoes the wine's dark herb and forest floor character.")

PAIR(RIPPON, "Seared salmon fillet with pinot noir sauce and mushroom duxelles",
    "elevate", "established", "main",
    "Rippon's extraordinary delicacy and lake-edge mineral character work brilliantly with salmon — one of the few proteins that matches the wine's colour, delicacy, and umami without overwhelming it. The Pinot sauce creates a deliberate bridge; mushroom duxelles echoes the wine's earthy depth.")

PAIR(SER_LEAH, "Roasted beetroot salad with goat's cheese and walnut",
    "complement", "established", "starter",
    "Seresin's Marlborough Pinot Noir works beautifully with roasted beetroot — the wine's dried rose and red cherry character mirrors the sweet earthiness of beetroot while the goat's cheese provides the acid-softening contrast the wine's tannins need.")

# Argentina Malbec pairings
PAIR(ACHAV, "Grilled ribeye steak with chimichurri",
    "complement", "classic", "main",
    "The classic Argentine Malbec-to-beef pairing in its most natural expression — chimichurri's herb and acid cuts through Malbec's fruit richness while the steak fat softens the wine's tannins. Achaval Ferrer's estate Malbec is made precisely for this pairing.")

PAIR(FINCA, "Dry-aged bone-in rib of beef with black truffle and bone marrow jus",
    "elevate", "established", "main",
    "Achaval Ferrer Finca Altamira's concentrated old-vine intensity demands a dish of equivalent weight and complexity — dry-aged beef provides the richness while truffle's earthy complexity matches the wine's graphite and iron mineral depth. Bone marrow jus provides the fat to tame the wine's dense tannin structure.")

PAIR(CLOS, "Braised short rib with polenta and gremolata",
    "complement", "established", "main",
    "Clos de los Siete's accessible structure and altitude-freshness pairs brilliantly with braised short rib — the generous fruit meets the deep umami while polenta provides a neutral textural base. Gremolata's brightness cuts through both the wine's fruit richness and the beef fat.")

# South Africa pairings
PAIR(MULL_W, "Grilled yellowtail with charred leek vinaigrette and pickled fennel",
    "complement", "established", "fish_course",
    "Mullineux Signature White's old-vine Swartland Chenin Blanc complexity — quince, beeswax, mineral — pairs beautifully with firm-fleshed grilled fish. The charred leek amplifies the wine's subtle oxidative notes while pickled fennel bridges the acid and the wine's mineral spine.")

PAIR(MULL_S, "Grilled lamb shoulder with za'atar and pomegranate",
    "complement", "established", "main",
    "Mullineux Swartland Syrah's Northern Rhône character — black olive, graphite, white pepper — pairs classically with lamb. The za'atar seasoning amplifies the wine's herbal character while pomegranate's tartness provides the acid contrast that the Syrah's structure needs.")

PAIR(JORD, "Pan-roasted halibut with leek fondue and chervil",
    "elevate", "established", "fish_course",
    "Jordan Nine Yards Chardonnay's Burgundian texture and granite mineral spine pairs superbly with pan-roasted halibut — the lees richness mirrors the leek fondue while the wine's acid structure cuts through the butter and fat. Chervil's delicate anise character bridges the herbal notes of the Chardonnay.")

# Australian pairings
PAIR(RUNRIG, "Braised wagyu short rib with Barossa pepper berry and chocolate jus",
    "complement", "classic", "main",
    "Torbreck RunRig's dense co-fermented Shiraz-Viognier demands the richest proteins — wagyu short rib provides the fat to integrate the wine's extraordinary concentration. Pepper berry amplifies the Viognier's floral lift while chocolate jus mirrors the wine's dark chocolate depth.")

PAIR(STEADING, "Roasted lamb rack with herb crust and eggplant",
    "complement", "established", "main",
    "Torbreck The Steading's ancient Grenache-driven GSM blend pairs naturally with lamb — the Grenache's red fruit and white pepper character amplifies the lamb's sweetness while eggplant's savory richness grounds the wine's lively fruit. The classic Rhône-lamb pairing translated to Barossa.")

PAIR(ARES, "Braised duck leg with plum sauce and star anise",
    "complement", "established", "main",
    "Two Hands Ares Marananga Shiraz's refined power and dark fruit profile pairs beautifully with braised duck — the plum sauce mirrors the wine's fruit concentration while star anise amplifies the spice notes characteristic of the Marananga sub-region's cooler climate Shiraz.")

PAIR(HIGH_SDS, "Roasted pork belly with apple purée and sage jus",
    "elevate", "established", "main",
    "Yangarra High Sands Grenache's extraordinary delicacy and old-vine purity demands a dish that doesn't overwhelm — pork belly (lighter than beef) provides the fat to integrate the wine's silky tannins while apple mirrors the Grenache's red fruit character. Sage jus adds the herbal depth the wine's terroir mineral finish needs.")

PAIR(YANG_SH, "Lamb shank with preserved lemon and olives",
    "complement", "established", "main",
    "Yangarra Estate Shiraz's restrained peppery character — biodynamic-influenced freshness — pairs perfectly with lamb braised with Mediterranean aromatics. The preserved lemon's brightness cuts the wine's fruit richness while olives amplify the wine's savory, mineral quality.")

PAIR(CHAPEL, "Chargrilled porterhouse steak with bone marrow butter",
    "complement", "classic", "main",
    "Chapel Hill Bushard Vineyard's centenarian-vine Shiraz intensity — deeply concentrated blackberry and leather — demands beef of comparable substance. The bone marrow butter softens the wine's age-worthy tannins while the char amplifies the wine's dark, smoky complexity.")

PAIR(MAC_PN, "Duck confit with cherry reduction and Puy lentils",
    "complement", "established", "main",
    "Mac Forbes Woori Yallock Pinot Noir's richness and warmth of fruit pairs naturally with duck confit — the concentrated dark cherry mirrors the wine's generous fruit while Puy lentils provide the earthy, mineral backdrop that amplifies the wine's forest floor character.")

PAIR(MAC_CH, "Roasted chicken with tarragon cream and blanched almonds",
    "complement", "classic", "main",
    "Mac Forbes Chardonnay's Burgundian restraint and struck-match reduction pairs classically with tarragon chicken — the wine's lemon curd and almond meal texture mirrors the cream sauce while tarragon amplifies the Chardonnay's herbal mineral finish.")

PAIR(DEB_PN, "Roasted quail with pinot noir reduction and wild mushrooms",
    "elevate", "established", "main",
    "De Bortoli Lusatia Park's exceptional delicacy and red fruit precision pairs best with fine-textured game birds — quail's gentle sweetness mirrors the wine's red cherry while wild mushrooms amplify the Pinot's earthy, forest floor character. The Pinot Noir reduction creates a deliberate varietal bridge.")

# Napa Valley pairings
PAIR(HEITZ, "Grilled lamb chops with rosemary, roasted garlic, and eucalyptus jus",
    "elevate", "adventurous", "main",
    "Heitz Martha's Vineyard's famous eucalyptus character creates the unique pairing opportunity: a rosemary-heavy lamb preparation with a eucalyptus-infused jus deliberately echoes the wine's most distinctive terroir signature. For sommelier-led tasting menus where the wine is the story.")

PAIR(CASK23, "Roasted Wagyu tenderloin with black truffle and Bordelaise",
    "elevate", "classic", "main",
    "Stag's Leap CASK 23's elegant Stags Leap District structure and cedar-tobacco complexity pairs perfectly with the finest beef and truffle — a pairing that matches the wine's historical significance with comparable culinary ambition. The Bordelaise sauce provides the wine-bridge; truffle amplifies the wine's mineral depth.")

PAIR(SLV, "Braised short rib with Napa Cabernet reduction and celery root",
    "complement", "established", "main",
    "S.L.V. Estate Cabernet's precision and dusty Stags Leap District tannins pair beautifully with braised short rib — the wine's acid structure penetrates the fat while celery root's earthy mineral quality mirrors the wine's cool-climate elegance. A Napa Cabernet reduction provides the varietal bridge.")

PAIR(CAY_SS, "Dry-aged prime rib with au jus and horseradish",
    "complement", "classic", "main",
    "Caymus Special Selection's plush Rutherford richness and lush blackberry fruit is made for prime rib — the most classic American Cabernet-to-beef pairing. The au jus provides the savory depth that integrates with the wine's concentration while horseradish cuts through both beef fat and Cabernet richness.")

PAIR(CAY_NV, "Grilled New York strip with compound herb butter",
    "complement", "classic", "main",
    "Caymus Napa Cabernet's accessible, generous style pairs perfectly with a well-grilled strip steak — the most democratic expression of the California Cabernet-and-beef tradition. Compound herb butter softens the tannins while amplifying the wine's cassis and vanilla character.")

PAIR(WS_ALLEN, "Roasted duck breast with cherry compote and pistachio",
    "complement", "classic", "main",
    "Williams Selyem Allen Vineyard's rich Russian River Pinot Noir — dark cherry, cola, and baking spice — pairs classically with duck. The cherry compote mirrors the wine's fruit character while pistachio adds the textural and slight bitterness that balances the wine's weight and sweetness.")

cur.close()
conn.close()
print("\n✅ Terminal 9 Batch 3 — Refs + Pairings complete.")
