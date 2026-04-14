#!/usr/bin/env python3
"""Terminal 5 — Batch 1: Regions — Germany wine, Austria, Portugal wine + Port + Madeira"""
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

# ─── GERMANY — WINE ────────────────────────────────────────────────────────────
print("=== GERMANY — WINE REGIONS ===")
mosel = R("Mosel", "Germany", "wine",
    reputation_tier="iconic", quality_trajectory="rediscovering",
    key_producers="Egon Müller, Joh. Jos. Prüm, Fritz Haag, Markus Molitor, Clemens Busch, Moselland",
    description="Germany's most celebrated wine region — a dramatic amphitheatre of Devonian slate cliffs rising 200–400m above the serpentine river between Trier and Koblenz. The Mosel (with tributaries Saar and Ruwer) produces Riesling of towering precision: razor acidity, crystalline minerality, and a sugar/acid balance that enables 50-year cellaring. The Prädikat system — Kabinett, Spätlese, Auslese, Beerenauslese, Eiswein, Trockenbeerenauslese — maps residual sugar against natural concentration. Blue Devonian slate terraces retain warmth to ripen Riesling in the coolest German conditions. At their finest, Mosel Riesling wines achieve a paradox: featherlight alcohol (7–8% Kabinett) combined with extraordinary depth, longevity, and complexity.",
    historical_context="Roman settlement at Augusta Treverorum (Trier) was Germany's wine capital. Charlemagne mandated Riesling cultivation in 812 CE. The Bernkasteler Doktor vineyard was named when the Archbishop of Trier allegedly cured the ailing Emperor Wenzel IV of Bohemia in 1360. Mosel wines were served at the Congress of Vienna (1815).",
    authority_tier=1)

saar = R("Saar", "Germany", "wine", parent_id=mosel,
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Egon Müller-Scharzhof, Van Volxem, Peter Lauer, Weingut Nik Weis",
    description="The Saar tributary south of Trier represents Mosel-Saar-Ruwer's most austere, mineral extreme. Scharzhofberg and Ockfener Bockstein are the benchmark vineyards. Egon Müller's Scharzhofberger TBA routinely achieves six-figure auction prices — the most expensive German wine. In average vintages the Saar's extreme coolness can produce barely ripe Riesling; in exceptional vintages it produces Kabinett and Spätlese of unparalleled steely precision.",
    authority_tier=1)

rheingau = R("Rheingau", "Germany", "wine",
    reputation_tier="prestigious", quality_trajectory="rediscovering",
    key_producers="Georg Breuer, Künstler, Schloss Vollrads, Weil, Robert Weil, Josef Leitz, Balthasar Ress",
    description="The Rheingau is where the Rhine briefly flows east-west, giving south-facing slopes of Taunus quartzite and slate maximum sun exposure. The 30km stretch from Hochheim to Rüdesheim produces Riesling of power, richness, and structure — different from Mosel's ethereal delicacy. Schloss Johannisberg, planted by Benedictines in 1130, is credited with discovering Spätlese (late harvest) wine after a messenger was delayed bringing harvest permission. Erstes Gewächs (First Growth) classification introduced 1999 parallels Burgundy's Premier Cru.",
    historical_context="Cistercian monks of Eberbach Abbey were the Rheingau's defining producers for 800 years. The Rheingauer Riesling Route now runs 120km through the region. Hochheimer Daubhaus ('Hock') gave English wine drinkers the word 'hock' for all German wine.",
    authority_tier=1)

nahe = R("Nahe", "Germany", "wine",
    reputation_tier="respected", quality_trajectory="ascending",
    key_producers="Dönnhoff, Schäfer-Fröhlich, Emrich-Schönleber, Kruger-Rumpf",
    description="The Nahe, flowing into the Rhine at Bingen, produces Germany's most geologically diverse wines: porphyry, quartzite, basalt, sandstone, and slate all appear within a small area. Dönnhoff's Oberhäuser Brücke Riesling is the Nahe's most sought single-vineyard expression — combining Mosel tension with Rheingau weight. Often considered undervalued relative to quality, making Nahe the best QPR region in Germany.",
    authority_tier=1)

pfalz = R("Pfalz", "Germany", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Dr. Bürklin-Wolf, Rebholz, Bassermann-Jordan, Friedrich Becker, A. Christmann",
    description="Germany's second-largest wine region, sheltered by the Haardt Mountains from Atlantic rainfall. The warmest of Germany's Riesling regions — capable of producing Burgundy-rivalling Spätburgunder (Pinot Noir) and Weissburgunder (Pinot Blanc). The Mittelhaardt, home to Forst and Deidesheim, produces Riesling GGs (Grosses Gewächs) of extraordinary power and concentration. Dr. Bürklin-Wolf's Kirchenstück is one of Germany's greatest single-vineyard expressions.",
    authority_tier=1)

# ─── AUSTRIA — WINE ───────────────────────────────────────────────────────────
print("\n=== AUSTRIA — WINE REGIONS ===")
wachau = R("Wachau", "Austria", "wine",
    reputation_tier="iconic", quality_trajectory="established",
    key_producers="F.X. Pichler, Emmerich Knoll, Rudi Pichler, Prager, Nikolaihof, Veyder-Malberg",
    description="The Wachau, a 30km stretch of the Danube between Melk and Krems, is one of Europe's most visually dramatic wine regions — baroque monasteries and terraced granite vineyards rising 300m above the river. Produces Austria's most celebrated Grüner Veltliner and Riesling under the Vinea Wachau Nobilis Districtus three-tier classification: Steinfeder (light, max 11.5% ABV), Federspiel (medium, 11.5–12.5%), Smaragd (full, 12.5%+). Smaragd wines, named for the local emerald lizard, represent extreme concentration from hand-harvested, perfectly mature grapes. The terraced Loess and gneiss-granite soils produce wines of mineral precision and extraordinary longevity.",
    historical_context="Winemaking in the Wachau dates to Celtic settlement 2,000 years ago. Benedictine monks of Dürnstein and Göttweig maintained production through the medieval period. The Vinea Wachau association, formed 1983, created the classification system that brought international recognition.",
    authority_tier=1)

kamptal = R("Kamptal", "Austria", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Bründlmayer, Hirsch, Loimer, Schloss Gobelsburg, Steininger",
    description="Kamptal DAC (Districtus Austriae Controllatus) covers the Kamp river valley north of Krems. Primary variety: Grüner Veltliner and Riesling from Zöbinger Heiligenstein — a 350m volcanic rhyolite outcrop that is one of Austria's most distinctive single vineyard sites. Bründlmayer is the reference estate — their Lamm Riesling GV and Zöbinger Heiligenstein Riesling achieve Wachau Smaragd levels of concentration with slightly more aromatic openness. The loess-dominated valley floor versus the rocky upper slopes creates significant quality stratification.",
    authority_tier=1)

kremstal = R("Kremstal", "Austria", "wine",
    reputation_tier="respected", quality_trajectory="established",
    key_producers="Nigl, Stadt Krems, Salomon Undhof, Mantlerhof",
    description="Kremstal DAC surrounds the ancient city of Krems at the Danube-Kamp confluence. A transitional zone between the granitic Wachau and the loess-rich Kamptal — producing Grüner Veltliner and Riesling of intermediate character: more structured than Kamptal but less mineral-austere than Wachau Smaragd. Nigl produces some of the DAC's most serious Riesling from volcanic Senftenberg slopes.",
    authority_tier=1)

burgenland = R("Burgenland", "Austria", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Umathum, Heinrich, Gut Oggau, Ernst Triebaumer, Willi Opitz, Paul Achs, Moric",
    description="Burgenland, bordering Hungary along the shallow Neusiedlersee lake, produces Austria's most distinctive red wines and the world's greatest botrytised dessert wines. Blaufränkisch — Burgenland's indigenous red grape — produces concentrated, spiced, iron-mineral wines from iron-rich slate soils (Eisenberg, Mittelburgenland). The Neusiedlersee lake generates consistent autumn fog enabling noble rot (Botrytis cinerea), producing Ausbruch and TBA dessert wines of 500+ g/L residual sugar. Gut Oggau's amphora-aged wines and Moric's single-vineyard Blaufränkisch have brought international recognition.",
    authority_tier=1)

# ─── PORTUGAL — WINE REGIONS ─────────────────────────────────────────────────
print("\n=== PORTUGAL — WINE REGIONS ===")
douro_table = R("Douro DOC", "Portugal", "wine",
    reputation_tier="prestigious", quality_trajectory="ascending",
    key_producers="Quinta do Vale Meão, Quinta do Crasto, Niepoort, Ramos Pinto, Quinta de la Rosa, Barca Velha (Ferreira)",
    description="The Douro DOC covers the same schist-terraced river valley as the Port wine region, but produces dry table wines of rapidly ascending international reputation. The same Touriga Nacional, Touriga Franca, Tinta Roriz, and Tinta Barroca grapes that make Port, when fully fermented dry at controlled temperatures, produce deeply concentrated red wines with black fruit, iron-mineral, and graphite character. The region is divided into three sub-zones: Baixo Corgo (westernmost, most Atlantic influence), Cima Corgo (benchmark — where the finest quintas are concentrated around Pinhão), and Douro Superior (furthest inland, most extreme continental climate). Barca Velha, produced by Ferreira only in exceptional years (1952 first release), was Portugal's first 'super wine' and the template for the modern Douro DOC movement.",
    historical_context="The Douro was demarcated in 1756 by the Marquis of Pombal — the world's first legally demarcated wine region. Phylloxera devastated vineyards in the 1870s–1890s. The shift from fortified-only to fine dry table wine began in the 1950s (Barca Velha) and accelerated post-EU membership (1986).",
    authority_tier=1)

vinho_verde = R("Vinho Verde DOC", "Portugal", "wine",
    reputation_tier="respected", quality_trajectory="ascending",
    key_producers="Soalheiro, Anselmo Mendes, Quinta de Soalheiro, Muros Antigos, Casa de Sezim, Quinta do Ameal",
    description="Vinho Verde ('green wine') covers Portugal's far northwest — the Minho region along the Spanish border, receiving Atlantic rainfall averaging 1,600mm annually. 'Verde' refers to youth and freshness, not colour. The region encompasses 9 sub-zones; the Monção e Melgaço sub-zone, planted exclusively with Alvarinho (Albariño in Galicia), produces Portugal's most elegant and ageable white wines. Standard Vinho Verde is a multi-variety blend — young, low-alcohol (9–11%), high-acid, with a light natural spritz from early bottling and secondary fermentation. Single-variety Alvarinho (Soalheiro, Anselmo Mendes) is a serious fine wine — stone fruit, citrus blossom, saline minerality, ageing 5–10 years.",
    authority_tier=1)

alentejo = R("Alentejo DOC", "Portugal", "wine",
    reputation_tier="respected", quality_trajectory="ascending",
    key_producers="Herdade do Esporão, Cartuxa, Herdade do Mouchão, Cortes de Cima, José de Sousa",
    description="Alentejo — 'beyond the Tagus' — covers southern Portugal's vast cork oak plains. The region's hot, dry continental climate produces the opposite of Vinho Verde's freshness: ripe, full-bodied reds from Aragonez (Tempranillo), Alicante Bouschet, Trincadeira, and Touriga Nacional. Cork is Alentejo's dominant agricultural product (Portugal produces 50% of the world's cork). The herdade (estate) system — large land holdings compared to northern Portugal's fragmented quintas — allows consistent commercial production. Esporão is the international benchmark; Mouchão's Tonel reserve is a cult wine commanding significant prices.",
    authority_tier=1)

bairrada = R("Bairrada DOC", "Portugal", "wine",
    reputation_tier="respected", quality_trajectory="rediscovering",
    key_producers="Luis Pato, Filipa Pato, Sidonio de Sousa, Caves São João, Quinta das Bágeiras",
    description="Bairrada, south of Porto, is dominated by Baga — one of Portugal's most site-specific indigenous varieties. Baga's extreme tannin and acidity demand extended ageing; in clay-limestone soils with Atlantic influence, it produces wines of extraordinary longevity (30–50 years). Luis Pato, the region's most visible advocate, has spent decades persuading the world that Baga, like Barolo's Nebbiolo, rewards patience. Often described as 'Portugal's Burgundy' — small parcels, indigenous variety, clay-limestone, age-worthy. Sparkling Bairrada (produced by traditional method) is also exceptional.",
    authority_tier=1)

dao = R("Dão DOC", "Portugal", "wine",
    reputation_tier="respected", quality_trajectory="ascending",
    key_producers="Quinta dos Roques, Rui Reguinga (Colinas do Douro), Casa de Santar, Alvaro Castro",
    description="Dão, inland from Bairrada in the granite highlands of central Portugal, is enclosed by mountains on three sides — a natural bowl that moderates Atlantic and continental extremes. Granite-sandy granitic soils produce elegant, perfumed reds from Touriga Nacional, Tinta Roriz, and Alfrocheiro — lighter in body than Douro, more structured than Alentejo. Often compared to Burgundy or northern Rhône for finesse over power. Historically dominated by cooperatives; the arrival of small private estates since the 1990s has transformed quality.",
    authority_tier=1)

porto_douro = R("Porto — Douro Valley", "Portugal", "wine",
    reputation_tier="iconic", quality_trajectory="established",
    key_producers="Taylor Fladgate, Quinta do Noval, Graham's, Dow's, Fonseca, Warre's, Ramos Pinto, Churchill",
    description="The Douro Valley DOC for Port wine encompasses the same schist terraces as the table wine Douro DOC, but with fortification. Port wine is produced by arresting fermentation with grape spirit (aguardente, 77% ABV), retaining 80–160 g/L residual sugar and fortifying to 19–22% ABV. The resulting wine matures in either large wooden vats (preserving fresh fruit — Ruby, LBV, Vintage) or small 550L pipes (developing oxidative character — Tawny, Colheita). The Symington Family (Graham's, Dow's, Warre's, Quinta do Vesuvio) and the Fladgate Partnership (Taylor's, Fonseca, Croft, Quinta de Roeda) dominate quality production. Vila Nova de Gaia, across the Douro from Porto, hosts the shippers' lodges.",
    historical_context="The Methuen Treaty (1703) gave Portuguese wines preferential tariffs in England, creating the British-controlled Port wine trade. The Douro was demarcated in 1756. The Symington family arrived 1882; Taylor's was established 1692 — making it the oldest Port house still in single family ownership.",
    authority_tier=1)

madeira_region = R("Madeira", "Portugal", "wine",
    reputation_tier="iconic", quality_trajectory="established",
    key_producers="Blandy's, D'Oliveiras, Barbeito, HM Borges, Justino's, Cossart Gordon, Henriques & Henriques",
    description="Madeira is the world's most indestructible wine — a volcanic Atlantic island 600km off the Moroccan coast producing wines of extraordinary longevity through a deliberate oxidation and heating process (estufagem or canteiro) that was originally accidental. The four noble varieties map to sweetness level: Sercial (driest, high acidity, 18–25 g/L RS), Verdelho (medium-dry, 25–65 g/L), Bual (medium-rich, 65–100 g/L), Malmsey/Malvasia (richest, 100–150 g/L). Vintage Madeira from pre-phylloxera vintages (1862, 1875, 1880) is still commercially available and drinkable — no wine in the world demonstrates longevity more conclusively. The Madeira Wine Institute (IVBAM) governs production. Blandy's, founded 1811, is the reference shipper.",
    historical_context="Madeira wine accompanied the first transatlantic voyages — Columbus stopped at Madeira in 1492 before sailing to the Americas. George Washington celebrated American independence with Madeira. The wine became durable through the 'Indian Road' — casks sent to India and back as ballast discovered that heat and motion improved rather than damaged the wine.",
    authority_tier=1)

print("\n✅ Terminal 5 Batch 1 — Regions complete.")
print(f"""
REGION ID SUMMARY (for use in batch 2+):
  mosel = {mosel}
  saar = {saar}
  rheingau = {rheingau}
  nahe = {nahe}
  pfalz = {pfalz}
  wachau = {wachau}
  kamptal = {kamptal}
  kremstal = {kremstal}
  burgenland = {burgenland}
  douro_table = {douro_table}
  vinho_verde = {vinho_verde}
  alentejo = {alentejo}
  bairrada = {bairrada}
  dao = {dao}
  porto_douro = {porto_douro}
  madeira_region = {madeira_region}
""")
