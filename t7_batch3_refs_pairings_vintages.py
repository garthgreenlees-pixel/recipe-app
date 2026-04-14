#!/usr/bin/env python3
"""Terminal 7 — Batch 3: Refs, Pairings, Vintages for Speyside + Islay"""
import psycopg2, psycopg2.extras, json
import sys
sys.path.insert(0, '/Users/garthgreenlees/Desktop/provenance-tester-1')
from medit_helpers import get_conn, REF, PAIR

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn, cur = get_conn()

# Product IDs
GLENFIDDICH_18 = 519
BALVENIE_17    = 520
GLENLIVET_18   = 521
GLENFARCLAS_21 = 522
ABERLOUR_AB    = 523
MORTLACH_16    = 524
LAPHROAIG_10   = 525
LAGAVULIN_16   = 526
PORT_CHARLOTTE = 527
BOWMORE_18     = 528
CAOL_ILA_12    = 529

# ─── REFERENCES ────────────────────────────────────────────────────────────────
print("=== BEVERAGE REFERENCES ===")

REF(cur,
    name="Speyside Scotch: style spectrum from Glenlivet to Mortlach",
    category="spirits_knowledge",
    description=(
        "Speyside is Scotland's most productive and prestigious whisky region — home to over "
        "half of Scotland's working distilleries, concentrated in the valleys of the Spey, "
        "Livet, Fiddich, and Dullan rivers. The defining character: fruity, honeyed, and elegant "
        "with a pronounced cereal sweetness — quite different from Highland's range or Islay's peat. "
        "But Speyside's range is broader than most understand: "
        "Light end: Glenlivet (floral, tropical fruit), Glenfiddich (apple, pear, vanilla) "
        "Middle: Balvenie (honey, spice, doublewood), Aberlour (dried fruit, Christmas cake) "
        "Sherried end: Glenfarclas (rich sherry, direct-fired, independent), Macallan "
        "Heavy end: Mortlach (meaty, waxy, truffle — the complete outlier). "
        "Speyside is the baseline reference for most blended Scotch (80%+ of Speyside "
        "production goes to blends — Glenfiddich, Balvenie are exceptions)."
    ),
    key_principles=(
        "Know the style spectrum: Glenlivet/Glenfiddich (accessible, fruit-forward) → "
        "Balvenie/Aberlour (medium, wood-influenced) → Glenfarclas/Macallan (sherried, full) → "
        "Mortlach (heavy, savoury). "
        "The doublewood/triple wood process (Balvenie): maturation in bourbon oak then sherry finishing. "
        "The cask strength sherry bomb (A'Bunadh): no age statement, 59-61%, non-chill-filtered. "
        "Independent vs. corporate: Glenfarclas (family-owned), Balvenie (William Grant) vs. "
        "Glenlivet (Pernod Ricard), Macallan (Edrington)."
    ),
    common_mistakes=(
        "Treating all Speyside as 'light and fruity' — Mortlach and Glenfarclas are full-bodied sherried whiskies. "
        "Not knowing that most Speyside production goes to blends — Glenfiddich was the pioneer of single malt marketing. "
        "Confusing Macallan's sherry-heavy style with all Speyside — Glenlivet is the complete opposite."
    ),
    pro_tips=(
        "For a Speyside flight: Glenlivet 18 (light) → Balvenie DoubleWood 17 (medium) → Glenfarclas 21 (rich) → A'Bunadh (intense). "
        "Mortlach 16 pairs exceptionally with beef tartare or truffle preparations — the savoury whisky pairing."
    ),
    skill_level="advanced",
    service_context="spirits bar, Scotch dinner, whisky flight",
    authority_tier=1)

REF(cur,
    name="Islay Scotch: peat spectrum from Caol Ila to Laphroaig",
    category="spirits_knowledge",
    description=(
        "Islay (pronounced 'EYE-lah') is Scotland's most celebrated whisky island — producing "
        "8 working distilleries on a land mass of 620 sq km, all known for peat-smoked whisky. "
        "The peat level (phenol content) is the key differentiator across Islay distilleries: "
        "Lowest: Bruichladdich Classic Laddie (unpeated!), Caol Ila Moch (lightly peated) "
        "Medium: Caol Ila 12 (~35 ppm), Bowmore 12 (~25 ppm), Bunnahabhain (~3 ppm) "
        "Heavy: Lagavulin 16 (~35-40 ppm), Ardbeg 10 (~55 ppm), Port Charlotte (~40 ppm) "
        "Extreme: Laphroaig 10 (~45-50 ppm), Octomore (200-309 ppm — world record) "
        "The peat character also differs by style: medicinal/iodine (Laphroaig), "
        "maritime/smoke (Lagavulin, Caol Ila), clean/farm peat (Bruichladdich/Port Charlotte)."
    ),
    key_principles=(
        "PPM (phenol parts per million) in the malt is the standard measurement — "
        "but the final PPM in the bottle is typically 30-50% lower than in the malt. "
        "Islay peat types: iodine/medicinal (east coast, seaweed-influenced) vs. "
        "maritime/smoke (south coast warehouses). "
        "The pronunciation 'EYE-lah' is worth knowing for service contexts — "
        "guests saying 'ISS-lay' reveal unfamiliarity. "
        "Not all Islay is peated: Bunnahabhain and Classic Laddie are unpeated."
    ),
    common_mistakes=(
        "Serving peated Islay cold — temperature suppresses the smoke aromatics. "
        "Not warning guests about Laphroaig's medicinal character — the TCP/antiseptic note "
        "surprises uninitiated drinkers who expect 'whisky flavour'. "
        "Assuming Bruichladdich is peated — it produces multiple peating levels including unpeated."
    ),
    pro_tips=(
        "For a peated flight: Caol Ila 12 (lightest) → Lagavulin 16 → Laphroaig 10 (most extreme). "
        "The 'peat conversion flight': start with Caol Ila for approachability, end with Lagavulin "
        "for complexity — avoids the shock of Laphroaig as first impression. "
        "Lagavulin pairs with oysters: the Islay maritime terroir pairing."
    ),
    skill_level="advanced",
    service_context="spirits bar, Scotch tasting, Islay dinner",
    authority_tier=1)

# ─── PAIRINGS ──────────────────────────────────────────────────────────────────
print("\n=== PAIRINGS ===")

# Speyside pairings
PAIR(cur,
    food_description="Poached salmon with lemon butter — fruity Speyside mirrors delicate fish",
    food_category="seafood_general", meal_context="fish_course",
    confidence="established", pairing_type="complement",
    flavour_logic="Glenfiddich 18's dried apricot and vanilla oak notes complement the delicate "
                  "buttery richness of poached salmon without overpowering the fish's natural sweetness.",
    product_id=GLENFIDDICH_18,
    food_flavour_profile="delicate, buttery, citrus, rich",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Christmas cake with marzipan — the definitive DoubleWood pairing",
    food_category="flour_baking", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="Balvenie DoubleWood 17's Christmas cake, honey, and sherry notes find "
                  "direct equivalence in rich Christmas cake with marzipan — this is Scotch's "
                  "most natural dessert pairing.",
    product_id=BALVENIE_17,
    food_flavour_profile="rich, fruity, marzipan, sweet",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Grilled scallops with vanilla butter — tropical Speyside elegance",
    food_category="seafood_sashimi", meal_context="starter",
    confidence="established", pairing_type="complement",
    flavour_logic="Glenlivet 18's pineapple, citrus, and honey notes complement the natural "
                  "sweetness of scallops — the vanilla butter bridges the whisky and the seafood.",
    product_id=GLENLIVET_18,
    food_flavour_profile="sweet, vanilla, delicate, oceanic",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Roquefort with walnuts and dark honey — sherried Speyside and blue cheese",
    food_category="dairy_cheese", meal_context="cheese",
    confidence="classic", pairing_type="complement",
    flavour_logic="Glenfarclas 21's rich sherry, dried fruit, and coffee character finds complementary "
                  "intensity in Roquefort's savoury funk, while the walnuts and honey bridge sweetness.",
    product_id=GLENFARCLAS_21,
    food_flavour_profile="funky, salty, rich, crystalline",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Dark chocolate truffles — cask strength sherry bomb and dark chocolate",
    food_category="chocolate_confection", meal_context="dessert",
    confidence="classic", pairing_type="complement",
    flavour_logic="A'Bunadh's 60%+ ABV cask strength, dark cherry, and Christmas pudding character "
                  "finds perfect complementary intensity in dark chocolate truffles — especially "
                  "those with cherry or espresso centres.",
    product_id=ABERLOUR_AB,
    food_flavour_profile="dark, bitter, intense, rich",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Aged beef tartare with truffle oil — the meaty Speyside match",
    food_category="wagyu_premium_protein", meal_context="starter",
    confidence="adventurous", pairing_type="complement",
    flavour_logic="Mortlach 16's extraordinary meaty, waxy, truffle character finds direct "
                  "complementarity in aged beef tartare with truffle — this is the closest "
                  "a whisky comes to tasting like the food it is paired with.",
    product_id=MORTLACH_16,
    food_flavour_profile="meaty, earthy, savoury, rich",
    beverage_category="spirits_whiskey")

# Islay pairings
PAIR(cur,
    food_description="Natural oysters with lemon — Laphroaig's medicinal note and ocean terroir",
    food_category="seafood_sashimi", meal_context="aperitif",
    confidence="classic", pairing_type="complement",
    flavour_logic="The iodine, seaweed, and sea salt of Laphroaig mirrors the oceanic terroir "
                  "of natural oysters — one of Scotch whisky's most celebrated pairings. "
                  "The lemon accent brightens both.",
    product_id=LAPHROAIG_10,
    food_flavour_profile="briny, oceanic, mineral, citrus",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Smoked Islay scallops with sea herbs — Lagavulin's peat meets ocean smoke",
    food_category="seafood_sashimi", meal_context="starter",
    confidence="classic", pairing_type="complement",
    flavour_logic="Lagavulin 16's peat smoke, sea salt, and maritime character finds its "
                  "culinary equivalent in smoked scallops — the Islay terroir pairing "
                  "where whisky and food share the same smoky, oceanic origin.",
    product_id=LAGAVULIN_16,
    food_flavour_profile="smoky, oceanic, delicate, rich",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Smoked salmon with cream cheese on rye — Port Charlotte's clean peat",
    food_category="seafood_general", meal_context="amuse",
    confidence="established", pairing_type="complement",
    flavour_logic="Port Charlotte's citrus-forward, cleaner peat character complements smoked "
                  "salmon without overwhelming it — the cream cheese fat coats the palate "
                  "between sips and softens the smoke.",
    product_id=PORT_CHARLOTTE,
    food_flavour_profile="smoky, fatty, saline, citrus",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Grilled lamb cutlets with rosemary — maritime peat and rich red meat",
    food_category="wagyu_premium_protein", meal_context="main",
    confidence="classic", pairing_type="complement",
    flavour_logic="Bowmore 18's maritime brine, gentle peat, and dark fruit character cuts through "
                  "lamb fat elegantly — the rosemary echoes herbal notes in the whisky.",
    product_id=BOWMORE_18,
    food_flavour_profile="rich, gamey, herbal, fatty",
    beverage_category="spirits_whiskey")

PAIR(cur,
    food_description="Smoked mackerel pâté — lighter Islay smoke with oily fish",
    food_category="seafood_general", meal_context="starter",
    confidence="established", pairing_type="complement",
    flavour_logic="Caol Ila 12's light maritime smoke and citrus character is an ideal match "
                  "for smoked mackerel pâté — the fish's oiliness and smoke complement "
                  "without competing.",
    product_id=CAOL_ILA_12,
    food_flavour_profile="smoky, oily, rich, saline",
    beverage_category="spirits_whiskey")

# ─── VINTAGES ──────────────────────────────────────────────────────────────────
print("\n=== VINTAGES ===")

conn2 = psycopg2.connect(CONN)
conn2.autocommit = True
cur2 = conn2.cursor()

cur.execute("SELECT id FROM beverage_regions WHERE name = 'Speyside' AND country = 'Scotland'")
SPEYSIDE = cur.fetchone()[0]
cur.execute("SELECT id FROM beverage_regions WHERE name = 'Islay' AND country = 'Scotland'")
ISLAY = cur.fetchone()[0]

def V(region_id, year, rating, descriptor, narrative, price_traj="stable", window_from=None, window_to=None):
    cur2.execute("""
        INSERT INTO beverage_vintages
          (region_id, vintage_year, quality_rating, quality_descriptor, season_narrative, price_trajectory,
           drinking_window, authority_tier)
        VALUES (%s,%s,%s,%s,%s,%s,%s,1)
        ON CONFLICT (region_id, vintage_year) DO NOTHING
    """, (region_id, year, rating, descriptor, narrative, price_traj,
          json.dumps({"from": window_from, "to": window_to}) if window_from else None))
    action = "✓" if cur2.rowcount else "~"
    print(f"  {action} {year} → region {region_id}: {descriptor} ({rating})")

print("\n-- SPEYSIDE VINTAGES --")
V(SPEYSIDE, 1997, 96, "exceptional",
  "The 1997 Speyside vintage is the decade's finest: a warm, dry summer allowed full barley "
  "ripening and produced spirit of extraordinary richness. Glenfiddich 21 Year Old, Balvenie 25, "
  "and Glenfarclas 30 draws all include 1997 stocks as core components. "
  "Independent bottlers' 1997 single casks from Speyside command significant premiums.",
  "speculative", 2015, 2040)

V(SPEYSIDE, 2003, 94, "exceptional",
  "The 2003 Speyside summer was the hottest in 500 years — barley ripened early and rapidly, "
  "producing a higher-sugar new make than usual. The resulting spirit is sweeter and more "
  "fruit-forward than average Speyside, with shorter optimal maturation windows. "
  "Glenfarclas 21 from 2003 stocks and Aberlour A'Bunadh Batch 50+ expressions show this character.",
  "rising", 2018, 2030)

V(SPEYSIDE, 2009, 92, "excellent",
  "A clean, consistent Speyside production year — not an exceptional vintage but "
  "producing reliable, well-structured spirit across all major distilleries. "
  "The 15-year stocks from 2009 are entering premium expressions now and showing "
  "excellent balance of fruit and wood.",
  "stable", 2024, 2035)

V(SPEYSIDE, 2015, 90, "excellent",
  "The 2015 Speyside production year is notable for Glenfiddich's expanded capacity — "
  "new still house came online. The additional volume maintained house character. "
  "These 9-year spirits are building well and will enter 12-year expressions in 2027.",
  "stable", 2027, 2033)

print("\n-- ISLAY VINTAGES --")
V(ISLAY, 1990, 97, "exceptional",
  "The 1990 Islay vintage is considered a generational high point: all eight distilleries "
  "producing in exceptional form. Lagavulin's '1990 Distillers Edition' Pedro Ximénez is "
  "the most celebrated single malt release from this era. Independent bottlings of 1990 "
  "Laphroaig, Caol Ila, and Bowmore achieve five-figure auction prices.",
  "speculative", 2002, 2035)

V(ISLAY, 2001, 95, "exceptional",
  "The 2001 Islay year represents Ardbeg's first vintage under the Glenmorangie stewardship — "
  "an exceptional production year that produced the stocks for the legendary Ardbeg Uigeadail "
  "and Corryvreckan releases. Lagavulin and Laphroaig stocks from 2001 at 20+ years "
  "are extraordinary.",
  "speculative", 2015, 2035)

V(ISLAY, 2009, 93, "excellent",
  "The 2009 Islay vintage coincided with Bruichladdich's revival era at full capacity — "
  "Octomore series 6, 7, and 8 draw on 2009 stocks for some expressions. "
  "Lagavulin 2009 stocks are entering the 16-year expression cycle and showing "
  "exceptional quality.",
  "stable", 2024, 2032)

V(ISLAY, 2014, 91, "excellent",
  "A solid, clean Islay production year with all major distilleries at full capacity. "
  "The 2014 stocks are entering the 10-year expression range and show typical "
  "distillery character well — no dramatic peaks or troughs.",
  "stable", 2024, 2030)

conn.commit()
cur.close()
conn.close()
cur2.close()
conn2.close()
print("\n✅ T7 Batch 3 — Refs, Pairings, Vintages complete.")
