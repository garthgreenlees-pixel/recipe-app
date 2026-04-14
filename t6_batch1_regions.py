#!/usr/bin/env python3
"""Terminal 6 — Batch 1: Regions — Japanese Whisky, Irish Whiskey, Caribbean Rum"""
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

# ─── JAPANESE WHISKY ───────────────────────────────────────────────────────────
print("=== JAPANESE WHISKY REGIONS ===")
yamazaki = R("Yamazaki — Suntory Distillery", "Japan", "spirits",
    reputation_tier="iconic", quality_trajectory="established",
    key_producers="Suntory Spirits (The Yamazaki, The Hakushu)",
    description=(
        "Yamazaki Distillery, established 1923 at the confluence of three rivers south of Kyoto, "
        "is the founding expression of Japanese whisky and the style-defining site for the category worldwide. "
        "Suntory's first master blender Masataka Taketsuru trained in Scotland before returning to build "
        "a whisky that synthesises Scottish technique with Japanese precision aesthetics (monozukuri). "
        "The site's unique microclimate — high humidity, frequent mist, extreme temperature swings — "
        "produces a faster and more complex maturation than Scottish conditions. "
        "Yamazaki 12 and 18 Year Old are the most recognised Japanese whiskies internationally; "
        "the 25 Year Old commands auction prices exceeding €5,000 per bottle. "
        "The distillery operates multiple still types (pot and column), multiple wood types "
        "(ex-bourbon, ex-sherry, Mizunara oak), and a large spirit library, allowing master blenders "
        "to construct the characteristic Japanese house style: layered, sweet-fruited, perfumed, and silky."
    ),
    historical_context=(
        "Masataka Taketsuru founded Yamazaki in 1923 after studying at Hazelburn and Longmorn distilleries in Scotland. "
        "He later left Suntory to found Nikka Whisky (Yoichi, 1934). Whisky & Spirits Competition named "
        "Yamazaki Single Malt Sherry Cask 2013 the world's best whisky — triggering global demand that "
        "led to the NAS (No Age Statement) era. Yamazaki is now Japan's most visited distillery "
        "with 500,000 annual visitors."
    ),
    authority_tier=1)

yoichi = R("Yoichi — Nikka Distillery", "Japan", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="Nikka Whisky (Yoichi Single Malt, Nikka From the Barrel, Pure Malt)",
    description=(
        "Yoichi Distillery, established 1934 on Hokkaido's Shakotan Peninsula by Masataka Taketsuru, "
        "produces Japan's most peated and powerful single malt — a deliberate echo of the Highland and "
        "Campbeltown styles Taketsuru mastered in Scotland. The ocean air, cold climate, and hard water "
        "from Mount Yotei create a whisky of maritime salinity, peat smoke, and dried fruit concentration "
        "very different from the delicate sweetness of Yamazaki. "
        "The direct coal-fired pot stills — rare in Japan and disappearing in Scotland — produce a heavy, "
        "oily spirit character that gains waxy complexity through long maturation in damp stone warehouses. "
        "Yoichi 10 Year Old was discontinued in 2015 to protect stock; the NAS 'Yoichi' expression "
        "replaced it but commands significant secondary market premiums."
    ),
    historical_context=(
        "Taketsuru chose Hokkaido for Nikka because the climate and terrain most closely resembled "
        "the Scottish conditions he knew from his training. His Scottish wife, Jessie Roberta Cowan (Rita), "
        "is celebrated in Nikka's marketing. 'Massan' NHK television series (2014) dramatised their story "
        "and triggered a domestic Japanese whisky renaissance. Nikka was acquired by Asahi Breweries in 2001."
    ),
    authority_tier=1)

miyagikyo = R("Miyagikyo — Nikka Distillery", "Japan", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="Nikka Whisky (Miyagikyo Single Malt, Nikka Coffey Grain, Nikka Coffey Malt)",
    description=(
        "Miyagikyo Distillery, founded 1969 by Masataka Taketsuru in the Nikkagawa gorge near Sendai, "
        "was designed as Nikka's lighter, more floral counterpart to Yoichi's power. "
        "The site's cool mountain air, pure river water, and Coffey (continuous column) stills "
        "produce elegant, fruity spirit characters — apple blossom, peach, vanilla, chocolate — "
        "radically different from Yoichi's maritime smoke. "
        "The Coffey Grain and Coffey Malt expressions are unique: most distilleries use column stills "
        "only for grain whisky, but Nikka passes malt wash through Coffey stills to produce a rich, "
        "confected spirit prized by blenders and increasingly sold as a standalone premium. "
        "Miyagikyo is the core of Nikka blended expressions including 'From The Barrel'."
    ),
    historical_context=(
        "Miyagikyo opened 33 years after Yoichi, giving Nikka a second production site and style axis. "
        "The original Coffey stills were imported from Scotland and have operated continuously since 1963 "
        "(relocated from an earlier Nikka site). The distillery sits in the Nikkagawa gorge selected "
        "personally by Taketsuru after tasting the local river water."
    ),
    authority_tier=1)

chichibu = R("Chichibu — Ichiro's Malt", "Japan", "spirits",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Venture Whisky (Ichiro's Malt, Chichibu On The Way, Chichibu The Floor Malted)",
    description=(
        "Chichibu Distillery, founded 2008 by Ichiro Akuto in Saitama Prefecture, is the standard-bearer "
        "of Japan's craft whisky revolution. Ichiro Akuto saved the legendary Hanyu Distillery stock "
        "(since closed) before founding Chichibu — releasing the Hanyu 'Card Series' (54 casks) at "
        "auction to international acclaim and funding the new distillery. "
        "Chichibu is tiny by industry standards (100,000 litres per year) but operates with artisanal "
        "attention: floor malting of Japanese barley, open-top fermenters, direct-fired pot stills, "
        "and a wood policy that includes Mizunara, virgin American oak, ex-sherry, and ex-wine casks. "
        "The resulting whisky is celebrated for intensity far beyond its age — complex, estery, and "
        "experimental. Releases routinely sell out within minutes and command 3-5x retail on secondary markets."
    ),
    historical_context=(
        "The Hanyu Distillery (1941-2000) was Japan's most celebrated lost distillery. Ichiro Akuto's "
        "grandfather founded it; Ichiro rescued 400 remaining casks before it closed. The 'Card Series' "
        "(one bottling per playing card, 54 total) completed in 2014 and is considered the most important "
        "whisky collection of the 21st century. Chichibu opened in 2008 as Ichiro's new chapter."
    ),
    authority_tier=1)

# ─── IRISH WHISKEY ─────────────────────────────────────────────────────────────
print("\n=== IRISH WHISKEY REGIONS ===")
midleton = R("County Cork — Midleton Distillery", "Ireland", "spirits",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Irish Distillers / Pernod Ricard (Jameson, Redbreast, Green Spot, Method & Madness, Powers)",
    description=(
        "Midleton Distillery in County Cork is the largest and most productive whiskey distillery in Ireland, "
        "operated by Irish Distillers (Pernod Ricard). It is the production site for Jameson — the world's "
        "best-selling Irish whiskey and third best-selling whiskey globally — as well as the acclaimed "
        "Redbreast pot still series, Green Spot, Yellow Spot, Method & Madness, and Powers. "
        "Irish pot still whiskey — triple-distilled from a mash of malted and unmalted barley — is the "
        "defining style: creamy, spiced, and approachable. Midleton's master distillers blend from "
        "an enormous variety of casks (ex-bourbon, ex-sherry, ex-port, Mizunara) across dozens of "
        "different spirit types (pot still, grain, malt), giving extraordinary blending flexibility. "
        "The Redbreast range (12, 15, 21, 27 Year Old, Lustau Edition) is considered the finest "
        "expression of pure pot still Irish whiskey in production."
    ),
    historical_context=(
        "The original Old Midleton Distillery (1825) was the world's largest pot still distillery by 1880, "
        "with the world's largest pot still (150,000 litre capacity). It closed in 1975 when the "
        "new Midleton complex opened. Irish Distillers was formed in 1966 as a merger of surviving "
        "distilleries — consolidating the industry devastated by Prohibition (loss of US market), "
        "Irish independence (loss of British Empire market), and the rise of Scotch."
    ),
    authority_tier=1)

bushmills = R("County Antrim — Bushmills Distillery", "United Kingdom", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="Bushmills (Original, Black Bush, Bushmills Malt 10, 16, 21 Year Old)",
    description=(
        "Old Bushmills Distillery in County Antrim, Northern Ireland, holds a licence dated 1608 — "
        "making it the oldest licensed distillery in the world. Bushmills produces a range of "
        "single malt and blended Irish whiskies triple-distilled in copper pot stills, then matured "
        "in ex-bourbon American oak and ex-sherry Oloroso casks. "
        "The Bushmills style is lighter and more fragrant than southern Irish pot still whiskey: "
        "honey, vanilla, dried fruit, and a delicate floral note from the triple distillation. "
        "Black Bush is the flagship blended expression (80% single malt, 20% grain, aged in oloroso); "
        "Bushmills Malt 10 Year Old is a pure single malt; the 16 and 21 Year Old are aged in "
        "ex-bourbon then finished in port and Madeira casks respectively. "
        "Owned by Jose Cuervo since 2014."
    ),
    historical_context=(
        "The 1608 licence was granted by King James I to the Old County of Antrim for distillation. "
        "The current distillery was built in 1784 after the original burned. It survived the Irish "
        "whiskey industry's near-collapse by focusing on export markets. The distillery is 10km "
        "from the Giant's Causeway — Northern Ireland's most visited tourist site."
    ),
    authority_tier=1)

dublin_whiskey = R("Dublin — New Wave Irish Whiskey", "Ireland", "spirits",
    reputation_tier="respected", quality_trajectory="ascending",
    key_producers="Teeling Distillery, Pearse Lyons, Roe & Co, Proper No. Twelve, Lambay",
    description=(
        "Dublin's whiskey renaissance has transformed the Irish capital from a distillery desert "
        "(after the 1976 closure of John Power's and John Jameson's original Dublin distilleries) "
        "into a thriving new-wave hub. Teeling Distillery (2015) was the first new Dublin distillery "
        "in 125 years; it has been followed by several others on Thomas Street and across the Liberties — "
        "the historic heart of Dublin distilling. "
        "New Dublin whiskey embraces experimentation: wine cask finishes, single pot still revival, "
        "innovative mash bills, and premium age statements. Teeling Single Grain (Cabernet Sauvignon cask), "
        "Teeling Single Malt (5-cask maturation), and Teeling Single Pot Still define the category. "
        "The Dublin style tends toward fresh fruit, wine influence, and creative wood management."
    ),
    historical_context=(
        "Dublin was the world's whisky capital in the 1800s: John Jameson, John Power, and George Roe "
        "operated three of the world's largest distilleries within 500m of each other. All closed by 1976. "
        "The Liberties area — where most distilleries operated — is now experiencing its third wave "
        "of distilling activity, anchored by Teeling's 2015 opening."
    ),
    authority_tier=1)

# ─── CARIBBEAN RUM ─────────────────────────────────────────────────────────────
print("\n=== CARIBBEAN RUM REGIONS ===")
barbados = R("Barbados — Rum", "Barbados", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="Foursquare Distillery, Mount Gay, St. Nicholas Abbey, Plantation Barbados",
    description=(
        "Barbados is the birthplace of rum: the earliest documented rum distillation records date to "
        "the 1620s on the island's sugar plantations. Barbados rum is characterised by a pot-and-column "
        "distillation system producing elegant, complex spirits of remarkable finesse — quite different "
        "from the heavier Jamaican style or lighter Cuban style. "
        "Foursquare Distillery under master distiller Richard Seale is widely regarded as producing "
        "the world's finest rum: the annual Exceptional Cask Selection releases are allocated globally "
        "and command collector premiums. Mount Gay is the world's oldest continuously operating rum "
        "brand (est. 1703). The Barbados style: medium-bodied, dried tropical fruit, vanilla, baking "
        "spice, and a distinctive minerality from the coral limestone aquifer water."
    ),
    historical_context=(
        "The 1620 Barbados records describe 'kill-devil' (raw cane spirit) being traded among enslaved "
        "workers — the first documented rum. By 1657 Barbados had 100 distilleries. The island's rum "
        "industry was foundational to the Triangular Trade that shaped the Atlantic world. "
        "The Barbados Rum industry is now formally protected as a Geographical Indication (GI)."
    ),
    authority_tier=1)

jamaica = R("Jamaica — Rum", "Jamaica", "spirits",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Hampden Estate, Appleton Estate, Worthy Park, Monymusk, Smith & Cross",
    description=(
        "Jamaican rum is defined by ester intensity — the highest in the world for pot-still spirits. "
        "The traditional production method involves wild fermentation (no commercial yeast) in "
        "open wooden vats ('dunderhole' pits), using dunder (spent wash residue) and cane vinegar "
        "to create extreme bacterial activity. The resulting 'high ester' spirit contains hundreds "
        "of ester compounds at concentrations ten to fifty times higher than other rum styles. "
        "At its most extreme (Hampden Estate's >1,600 g/hLaa esters), Jamaican rum smells of "
        "overripe tropical fruit, glue, nail polish, and orange blossom — paradoxically becoming "
        "intensely tropical and floral when diluted. "
        "Appleton Estate (medium ester, aged pot-and-column) is the approachable style; "
        "Worthy Park and Hampden are purist funk extremes. All are pot-distilled in direct-fired copper stills."
    ),
    historical_context=(
        "Jamaican rum's ester tradition developed as a deliberate quality marker in the 18th century, "
        "when London rum merchants demanded high-funk spirits for the continental 'Rum-verschnitt' "
        "blending market. The 'plummer', 'wedderburn', and 'continental flavoured' marks classify "
        "ester levels from low to extreme. Hampden Estate's Hoti, Lrok, and C<>H marks represent "
        "the highest commercial ester productions in the world."
    ),
    authority_tier=1)

martinique = R("Martinique AOC — Rhum Agricole", "France", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="Neisson, Rhum J.M, Clément, Trois Rivières, La Favorite, Saint James",
    description=(
        "Martinique is the only rum-producing territory with a French AOC (Appellation d'Origine "
        "Contrôlée) — granted in 1996 for Rhum Agricole. The AOC mandates that rum be distilled "
        "exclusively from fresh-pressed sugarcane juice (not molasses), at specific still types, "
        "and from approved cane varieties grown in designated parcels of the island. "
        "The result is a radically different product from molasses-based rum: grassy, vegetal, "
        "funky in a green-cane sense rather than fruity-funk, with a freshness and terroir expression "
        "that changes by plantation, cane variety, and harvest timing. "
        "Blanc (unaged) is consumed locally with food; Elevé sous Bois (3 months wood) bridges "
        "raw to aged; Vieux (aged minimum 3 years) develops vanilla, spice, and dried fruit. "
        "Single vintage 'Millésime' expressions — comparable to vintage Cognac — are the pinnacle."
    ),
    historical_context=(
        "Martinique's AOC was the first in the world for rum and remains the only one. "
        "The fresh-cane juice tradition survived because sugar refining (which produces molasses) "
        "was concentrated on Guadeloupe; Martinique's smaller sugar mills pressed juice directly. "
        "The rhum agricole style influenced every high-quality rum producer globally from the 1990s onward."
    ),
    authority_tier=1)

demerara = R("Guyana — Demerara Rum", "Guyana", "spirits",
    reputation_tier="prestigious", quality_trajectory="established",
    key_producers="El Dorado (Demerara Distillers), Diamond Distillery, Port Mourant wooden stills",
    description=(
        "Demerara District on the Guyanese coast was once the greatest sugar-producing region in "
        "the British Empire — home to hundreds of rum distilleries in the 18th and 19th centuries. "
        "Today a single operation, Diamond Distillery (Demerara Distillers), controls the site "
        "and operates the world's most diverse collection of historic still types: "
        "the last working wooden pot stills in the world (Port Mourant double retort pot still, "
        "Enmore wooden Coffey still), a Versailles single wooden pot, and various continuous stills. "
        "Each still produces a dramatically different spirit character; blending across still marks "
        "creates El Dorado's complex aged expressions (3, 8, 12, 15, 21, 25 Year Old). "
        "The Demerara style: dark, intensely rich, molasses and dried fruit, caramelised sugar, "
        "with a thick, almost syrupy texture — the most 'dessert wine-like' of all rum styles."
    ),
    historical_context=(
        "In 1800, the Demerara colony had over 300 sugar estates, each with a rum still. "
        "Dutch colonisers developed the Demerara sugar and rum industry before the British takeover in 1814. "
        "The Port Mourant wooden double retort pot still dates to approximately 1732 — "
        "the world's oldest continually operating rum distillation vessel. "
        "El Dorado 15 Year Old was the world's first rum to win a major spirits competition (IWSC 1992)."
    ),
    authority_tier=1)

cur.close()
conn.close()
print("\n✅ Terminal 6 Batch 1 — Regions complete.")
