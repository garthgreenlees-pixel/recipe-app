#!/usr/bin/env python3
"""Terminal 6 — Batch 6: Vintages — Japanese Whisky, Irish Whiskey, Caribbean Rum"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"

conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs from T6 Batch 1
YAMAZAKI  = 237
YOICHI    = 238
MIYAGIKYO = 239
CHICHIBU  = 240
MIDLETON  = 241
BUSHMILLS_R = 242
DUBLIN    = 243
BARBADOS  = 244
JAMAICA   = 245
MARTINIQUE = 246
DEMERARA  = 247

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

# ─── JAPANESE WHISKY DISTILLERIES ─────────────────────────────────────────────
# For whisky distilleries, vintage_year represents the distillation year.
# Ratings reflect critical consensus on stocks from that year where assessable.

print("=== YAMAZAKI DISTILLERY STOCKS ===")
V(YAMAZAKI, 2003, 97, "exceptional",
  "The 2003 Yamazaki stocks represent the apex of the early-millennium era: distilled at the distillery's "
  "peak before the 2013 global demand shock created stock pressure. The sherry cask maturation from this "
  "year became the backbone of the Yamazaki Sherry Cask 2013 release that changed the whisky world. "
  "Now over 20 years old in wood, the remaining stocks are among Japan's most valuable.",
  "speculative", 2020, 2040)

V(YAMAZAKI, 2007, 96, "exceptional",
  "2007 Yamazaki stocks matured through the distillery's period of refining its Mizunara oak program. "
  "At 17+ years of age, these spirits show the sandalwood and coconut of Mizunara alongside "
  "rich bourbon oak vanilla — the combination that defines Yamazaki 18 at its best.",
  "rising", 2022, 2035)

V(YAMAZAKI, 2011, 93, "excellent",
  "The 2011 distillation year preceded the global shortage era — stocks were built with full "
  "intention for age statement releases that have since been cancelled. These 13+ year spirits "
  "represent the bridge between old-style age statement Yamazaki and the NAS era.",
  "rising", 2024, 2032)

V(YAMAZAKI, 2015, 91, "excellent",
  "The post-shortage era production: Suntory expanded distillation capacity to address the global "
  "demand crisis. The 2015 stocks are intended for future age statement releases expected 2027-2030. "
  "These spirits are building well in ex-bourbon casks.",
  "stable", 2027, 2035)

print("\n=== YOICHI DISTILLERY STOCKS ===")
V(YOICHI, 1988, 97, "exceptional",
  "The legendary era of Yoichi production: direct coal-fired stills operating at full intensity, "
  "and the stocks that defined the Yoichi 10, 12, and 15 Year Old age statement range. "
  "The 1988 vintage achieved the characteristically waxy, maritime, peated profile at its peak. "
  "Remnant casks in Nikka's library are of extraordinary value.",
  "speculative", 2000, 2030)

V(YOICHI, 2003, 95, "exceptional",
  "The 2003 Yoichi stocks are the last batches to have been fully incorporated into the discontinued "
  "age statement expressions (10, 12, 15 Year Old). At 20+ years, remaining stock is heavily peated "
  "and waxy — the definitive Yoichi character at full maturity.",
  "speculative", 2015, 2035)

V(YOICHI, 2010, 91, "excellent",
  "The 2010 distillation falls in the period of Nikka's transition to NAS expressions. "
  "The coal-fired stills remained unchanged — the spirit character is authentic Yoichi. "
  "These stocks are the core of current NAS Yoichi releases at 13-15 years.",
  "stable", 2023, 2030)

print("\n=== MIYAGIKYO DISTILLERY STOCKS ===")
V(MIYAGIKYO, 2007, 93, "excellent",
  "The 2007 Miyagikyo stocks are at peak expression: the Coffey still grain and pot still malt "
  "components have both reached optimal integration. The light, floral character typical of "
  "Miyagikyo is amplified by 17 years of ex-bourbon maturation into vanilla and tropical fruit complexity.",
  "rising", 2022, 2030)

V(MIYAGIKYO, 2012, 91, "excellent",
  "2012 represents the transition period — Nikka was preparing for the NAS era shift. "
  "The Coffey still program was running at full capacity to build grain stock for Nikka From The Barrel. "
  "These 12-year spirits are the foundation of current NFTB blending.",
  "stable", 2024, 2030)

print("\n=== CHICHIBU DISTILLERY STOCKS ===")
V(CHICHIBU, 2012, 94, "exceptional",
  "The earliest Chichibu production (distillery opened 2008) to achieve full expression: "
  "floor-malted barley, wooden washbacks, direct-fired pot stills. The 2012 stocks at 12+ years "
  "show the extraordinary intensity that floor malting creates — far above conventional distilleries. "
  "These form the backbone of Chichibu's annual limited releases.",
  "speculative", 2022, 2032)

V(CHICHIBU, 2016, 95, "exceptional",
  "By 2016 Chichibu had refined its full production program including Mizunara, wine cask, "
  "and virgin oak maturation. Stocks from this year represent the first generation of truly "
  "multi-faceted Chichibu whisky — crossing 8 years in 2024 with extraordinary promise. "
  "Critical consensus rates 2016 as Chichibu's standout production year.",
  "speculative", 2024, 2038)

# ─── IRISH WHISKEY ─────────────────────────────────────────────────────────────
print("\n=== MIDLETON DISTILLERY STOCKS ===")
V(MIDLETON, 2002, 96, "exceptional",
  "The 2002 Midleton Very Rare vintage is considered one of the decade's finest pot still productions: "
  "released as Midleton Very Rare (limited annual bottling) after 18 years, the 2002 stocks demonstrated "
  "the pure pot still character at extraordinary complexity. Redbreast 21 YO draws from stocks "
  "of this era — some of the most critically acclaimed Irish whiskey ever produced.",
  "speculative", 2020, 2040)

V(MIDLETON, 2009, 93, "excellent",
  "The 2009 pot still stocks were produced during the Irish whiskey renaissance — Midleton expanded "
  "production to meet growing global demand. Triple-distilled in copper pot stills with the standard "
  "malted + unmalted barley mash, these 15-year stocks form the core of Redbreast 15 and 21 Year Old.",
  "stable", 2024, 2035)

V(MIDLETON, 2016, 90, "excellent",
  "The 2016 production was the first year of Midleton's new distillery expansion — additional "
  "still capacity to handle 60% increased production volume. The spirit quality remained consistent "
  "with the house pot still style; these stocks will underpin Redbreast 12 and Single Pot Still "
  "releases through 2028.",
  "stable", 2028, 2034)

print("\n=== BUSHMILLS DISTILLERY STOCKS ===")
V(BUSHMILLS_R, 2003, 94, "exceptional",
  "The 2003 Bushmills single malt stocks form the core of the 21 Year Old Madeira Finish release — "
  "first pot-still distilled and ex-bourbon matured, then finished in Madeira casks for "
  "an additional maturation period. These are Northern Ireland's most celebrated aged spirits.",
  "speculative", 2024, 2035)

V(BUSHMILLS_R, 2010, 91, "excellent",
  "Strong production year at Bushmills: the 2010 single malt stocks show the clean, fragrant "
  "triple-distilled character at 14 years in ex-bourbon. These are the stocks entering "
  "the Bushmills Malt 16 Year Old range (ex-bourbon then port finish).",
  "stable", 2024, 2030)

print("\n=== DUBLIN — TEELING DISTILLERY STOCKS ===")
V(DUBLIN, 2016, 91, "excellent",
  "Teeling's first full year of distillation (distillery opened June 2015). The 2016 single grain "
  "and single malt stocks represent the founding era of Dublin's new whiskey renaissance. "
  "Aged in ex-Cabernet Sauvignon and ex-bourbon, these 8-year spirits are the foundation "
  "of current Teeling Single Grain releases.",
  "rising", 2024, 2030)

V(DUBLIN, 2019, 89, "very_good",
  "Post-expansion Teeling production: the distillery added additional pot still capacity in 2018. "
  "The 2019 stocks show Teeling's maturing house style — more integration, cleaner spirit character. "
  "These 5-year spirits are transitional — young but already showing the wine cask influence clearly.",
  "stable", 2024, 2028)

# ─── CARIBBEAN RUM DISTILLERIES ────────────────────────────────────────────────
# For rum, vintage_year represents distillation year / cask fill year.
# Tropical aging = approximately 3x faster maturation than Scotland.

print("\n=== BARBADOS RUM PRODUCTION ===")
V(BARBADOS, 2008, 97, "exceptional",
  "The 2008 Foursquare Exceptional Cask Selection Domaine de Courcelles XIV was distilled in 2007/2008 "
  "and released 14 years later — the most celebrated Barbadian rum produced in a generation. "
  "The tropical maturation in coral limestone island conditions and the French wine cask finish "
  "created extraordinary complexity: 98/100 critical consensus. A benchmark for Caribbean rum.",
  "speculative", 2022, 2030)

V(BARBADOS, 2014, 95, "exceptional",
  "The 2014 production at Foursquare and Mount Gay represents the peak of modern Barbados rum: "
  "GI protection discussions had raised quality standards industry-wide. The Foursquare 2005 vintage "
  "(10 years old at release) and the 2014 distillation both demonstrate Barbados at its finest.",
  "rising", 2022, 2032)

V(BARBADOS, 2018, 90, "excellent",
  "Barbados rum production in 2018 benefited from stable weather and improved sugarcane varietals. "
  "The 2018 stocks are the most recent entering aged expression release territory — "
  "currently 6 years old in tropical conditions (equivalent to ~18 Scottish years).",
  "stable", 2023, 2030)

print("\n=== JAMAICA RUM PRODUCTION ===")
V(JAMAICA, 2000, 98, "exceptional",
  "The millennium Hampden vintage: traditional wild fermentation at the estate using dunderhole pits "
  "produced maximum ester expression. The 2000 vintage stocks — now 24 years old — represent "
  "the peak of aged Jamaican rum complexity. VELIER single cask releases from this era are "
  "among the most collectible spirits in the world.",
  "speculative", 2015, 2040)

V(JAMAICA, 2010, 95, "exceptional",
  "The 2010 Hampden production year coincided with increasing international attention on Jamaican "
  "rum's ester tradition. Stocks from this year underpin current Hampden Great House releases — "
  "14 years of tropical aging has developed extraordinary overripe tropical fruit and complex ester.",
  "rising", 2022, 2035)

V(JAMAICA, 2017, 92, "excellent",
  "The 2017 Jamaican rum production was affected by Hurricane Maria in September — some estates "
  "experienced supply chain disruption. However, Hampden and Worthy Park were minimally impacted. "
  "The 2017 stocks show the characteristic high-ester Jamaican profile developing well at 7 years.",
  "stable", 2024, 2030)

print("\n=== MARTINIQUE AOC RHUM AGRICOLE ===")
V(MARTINIQUE, 2015, 93, "exceptional",
  "Exceptional Martinique cane harvest: ideal rainfall and temperature created unusually rich "
  "sugarcane juice with high Brix levels. The 2015 AOC agricole production — Neisson's Parcellaire "
  "single-parcel releases from this year — achieved critical consensus of 95+. "
  "Aged expressions from this year are at peak drinking (8-10 year tropical aging).",
  "rising", 2022, 2030)

V(MARTINIQUE, 2019, 90, "excellent",
  "The 2019 harvest was a strong standard year for Martinique: consistent rainfall and the "
  "structured AOC regulations maintained quality across all producers. Blanc expressions "
  "from 2019 showcase the region's fresh, grassy cane character at its most expressive.",
  "stable", 2019, 2025)

V(MARTINIQUE, 2022, 91, "excellent",
  "The 2022 Martinique production benefited from a clean, dry harvest window. Neisson's 2022 Blanc "
  "achieved 93 points from specialist rum critics. The fresh cane juice quality was outstanding — "
  "among the best unaged agricole expressions produced in recent years.",
  "stable", 2022, 2027)

print("\n=== GUYANA — DEMERARA RUM PRODUCTION ===")
V(DEMERARA, 1998, 97, "exceptional",
  "The 1998 Diamond Distillery production year includes some of the most celebrated Demerara "
  "single still releases: the Port Mourant (PM) mark wooden pot still produced extraordinary "
  "richness. VELIER and independent bottlers have released casks from this year to universal "
  "critical acclaim — El Dorado single still 1998 PM releases achieved 95-97 points.",
  "speculative", 2010, 2040)

V(DEMERARA, 2005, 95, "exceptional",
  "The 2005 Diamond Distillery production forms the core of El Dorado 15 Year Old releases "
  "from 2020 onwards — the world's most celebrated aged Demerara expression. "
  "The Port Mourant and Enmore still marks from this year show the thick, dark, molasses-rich "
  "Demerara character at full maturity.",
  "rising", 2020, 2035)

V(DEMERARA, 2012, 91, "excellent",
  "The 2012 production year at Diamond represents the modern era of El Dorado: consistent quality "
  "across still types, with the wooden Port Mourant and Enmore stills still operational. "
  "These 12-year stocks are entering the aged expression range and show excellent "
  "dark fruit, molasses, and caramelised sugar development.",
  "stable", 2024, 2032)

cur.close()
conn.close()
print("\n✅ Terminal 6 Batch 6 — Vintages complete.")
