#!/usr/bin/env python3
"""Terminal 5 — Batch 7: Vintages for all new regions (Germany, Austria, Portugal, Port, Madeira)"""
import psycopg2, json

CONN = "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:15432/provenance_tester_1?sslmode=disable"
conn = psycopg2.connect(CONN)
conn.autocommit = True
cur = conn.cursor()

# Region IDs
MOSEL=221; SAAR=222; RHEINGAU=223; NAHE=224; PFALZ=225
WACHAU=226; KAMPTAL=227; KREMSTAL=228; BURGENLAND=229
DOURO_TABLE=230; VINHO_VERDE=231; ALENTEJO=232; BAIRRADA=233; DAO=234
PORTO_DOURO=235; MADEIRA_REGION=236

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

# ─── GERMANY — MOSEL (all 5 regions use same key vintages) ───────────────────
print("=== MOSEL VINTAGES ===")
V(MOSEL, 2015, 97, "exceptional", "A benchmark Mosel vintage — perfect balance of warm summer and dry autumn. Riesling achieved full phenolic ripeness without losing acidity. Spätlese and Auslese of extraordinary precision. The Saar and Ruwer produced particularly brilliant wines.", "rising", 2025, 2050)
V(MOSEL, 2017, 95, "exceptional", "Followed 2015 as the second exceptional vintage in three years — hot, dry summer with critical September rain. Riesling Kabinett and Spätlese of remarkable tension and precision. GGs show power without losing Mosel delicacy.", "stable", 2022, 2040)
V(MOSEL, 2019, 96, "exceptional", "The third exceptional vintage of the decade — warm growing season without 2018's excess heat. Riesling achieved textbook ripeness: intense fruit, electric acidity, 8-9% ABV Spätlese with 20yr cellaring potential.", "rising", 2024, 2045)
V(MOSEL, 2018, 88, "very_good", "Extremely hot and dry — the hottest German growing season on record. Riesling risks over-ripeness; excellent producers managed to preserve acidity. GGs show power; traditional off-dry styles better in 2017 or 2019.", "stable", 2023, 2035)
V(MOSEL, 2020, 90, "excellent", "Covid vintage — difficult logistics but excellent quality. Late September rains threatened but most top producers harvested perfectly. Mosel Kabinett and Spätlese of excellent freshness and precision.", "stable", 2025, 2038)
V(MOSEL, 2021, 82, "good", "Challenging growing season — cool, wet spring and summer with disease pressure. Careful viticulture rewarded; best producers made wines of genuine character if not 2015/2017/2019 depth.", "stable", 2026, 2036)
V(MOSEL, 2022, 91, "excellent", "Hot, dry growing season — Mosel performed better than many hotter regions. Riesling preserved its characteristic acidity despite the heat; Spätlese and Kabinett of excellent freshness. GGs show power.", "stable", 2027, 2040)
V(MOSEL, 2016, 87, "very_good", "Uneven growing season; September rains created selective harvest pressure. Top producers made excellent Spätlese and Auslese through careful selection. Not a uniform vintage but excellent from committed producers.", "stable", 2024, 2036)

print("\n=== SAAR VINTAGES ===")
V(SAAR, 2015, 98, "exceptional", "The Saar's greatest vintage in 30 years — the extreme summer heat that challenged other regions was moderated by the Saar valley's altitude and river influence. Egon Müller's TBA from this vintage is one of Germany's most celebrated wines.", "rising", 2030, 2060)
V(SAAR, 2017, 96, "exceptional", "Perfect Saar conditions — warm but not extreme, preserving the Scharzhofberg's signature steely acidity alongside excellent ripeness. Kabinett and Spätlese of extraordinary tension.", "stable", 2025, 2045)
V(SAAR, 2019, 97, "exceptional", "Another benchmark year for the Saar — extended warm autumn allowed selective harvesting of Auslese and above. Egon Müller's wines from 2019 are considered equal to 2015.", "rising", 2026, 2050)
V(SAAR, 2007, 96, "exceptional", "The great German vintage of the 2000s — warm, late harvest enabled BA, TBA, and Eiswein production across the Saar. These wines are now in prime drinking window (2023-2035).", "speculative", 2015, 2045)

print("\n=== RHEINGAU VINTAGES ===")
V(RHEINGAU, 2015, 94, "exceptional", "Excellent Rheingau vintage — powerful, concentrated GGs from Berg Schlossberg, Steinberg, and Schloss Johannisberg. The warmth suited the Rheingau's naturally fuller style; Georg Breuer's GGs are particular highlights.", "stable", 2022, 2040)
V(RHEINGAU, 2017, 93, "exceptional", "Hot, dry vintage — Rheingau GGs of considerable power and body. The Trocken style particularly successful; excellent food-pairing wines with 12-15yr cellaring potential.", "stable", 2022, 2038)
V(RHEINGAU, 2019, 95, "exceptional", "Benchmark Rheingau year — warm summer with critical moisture preserved acidity. Berg Schlossberg GG of extraordinary mineral precision. The consensus finest Rheingau vintage since 2015.", "rising", 2025, 2042)
V(RHEINGAU, 2022, 90, "excellent", "Warm vintage favoured the Rheingau's naturally fuller style. GGs show immediate appeal; drinking window begins earlier than cooler years.", "stable", 2026, 2038)

print("\n=== NAHE VINTAGES ===")
V(NAHE, 2015, 96, "exceptional", "Perhaps Dönnhoff's finest vintage — Oberhäuser Brücke Spätlese from 2015 is considered one of Germany's greatest single bottles. The exotic tropical-volcanic character of Brücke was fully expressed.", "rising", 2025, 2050)
V(NAHE, 2017, 94, "exceptional", "Excellent Nahe vintage — warm growing season with precision harvest timing. Hermannshöhle and Brücke both produced wines of extraordinary character.", "stable", 2022, 2040)
V(NAHE, 2019, 95, "exceptional", "Third exceptional Nahe vintage in five years — the Dönnhoff estate's consistency across 2015, 2017, and 2019 is unparalleled in any German region.", "stable", 2024, 2044)
V(NAHE, 2022, 89, "very_good", "Warm vintage; Nahe performed well. Dönnhoff's Brücke showed its usual exotic precision despite the heat. Slightly less tension than 2019.", "stable", 2026, 2038)

print("\n=== PFALZ VINTAGES ===")
V(PFALZ, 2015, 95, "exceptional", "Benchmark Pfalz GG vintage — Kirchenstück, Jesuitengarten, and Ungeheuer from Bürklin-Wolf achieved extraordinary concentration balanced by the site's natural acidity. The basalt terroir's heat retention was perfectly calibrated.", "rising", 2022, 2042)
V(PFALZ, 2017, 94, "exceptional", "Hot, powerful vintage — Pfalz GGs of considerable density and richness. Rebholz's Kastanienbusch showed particular precision from the sandstone terroir. GG drinking windows begin immediately.", "stable", 2022, 2038)
V(PFALZ, 2019, 95, "exceptional", "Equal to 2015 for the Pfalz — Kirchenstück GG of extraordinary depth. The decade's finest Pfalz vintage alongside 2015.", "rising", 2024, 2044)
V(PFALZ, 2022, 91, "excellent", "Another warm vintage; Pfalz handled the heat well. GGs show immediate power. Rebholz's sandstone terroir preserved freshness.", "stable", 2026, 2040)

# ─── AUSTRIA ──────────────────────────────────────────────────────────────────
print("\n=== WACHAU VINTAGES ===")
V(WACHAU, 2015, 97, "exceptional", "Austria's finest vintage of the modern era — hot, dry summer with perfect September conditions. F.X. Pichler and Knoll produced Smaragd of extraordinary concentration and mineral depth. Both GV and Riesling exceptional.", "rising", 2025, 2050)
V(WACHAU, 2017, 95, "exceptional", "Following 2015's benchmark with nearly equal quality — warm growing season, perfect harvest timing. The Smaragd wines of 2017 are now entering prime drinking window.", "stable", 2022, 2042)
V(WACHAU, 2019, 96, "exceptional", "The third exceptional Wachau vintage in five years. F.X. Pichler's Kellerberg GV from 2019 is considered equal to 2015. The gneiss-granite terroir was perfectly expressed.", "rising", 2024, 2046)
V(WACHAU, 2013, 93, "exceptional", "The underrated Wachau vintage — cool growing season produced wines of exceptional acidity and mineral precision. Slower to develop than 2015 but potentially equal longevity.", "stable", 2023, 2045)
V(WACHAU, 2018, 87, "very_good", "Extremely hot vintage — exceptional viticulture required. Best producers preserved Wachau's signature acidity; some wines show heat. GV handled the vintage better than Riesling.", "stable", 2023, 2035)
V(WACHAU, 2022, 91, "excellent", "Warm but not extreme — Wachau performed well. Smaragd wines of good concentration with preserved freshness. Drinking window begins 2027.", "stable", 2027, 2040)

print("\n=== KAMPTAL VINTAGES ===")
V(KAMPTAL, 2015, 96, "exceptional", "Kamptal's finest modern vintage alongside 2017 — Bründlmayer's Heiligenstein Riesling from 2015 is considered one of Austria's ten greatest wines. Lamm GV of extraordinary white pepper concentration.", "rising", 2024, 2048)
V(KAMPTAL, 2017, 95, "exceptional", "Equal to 2015 for Kamptal — the rhyolite Heiligenstein expressed its volcanic character with great clarity. Lamm GV showing extraordinary longevity potential.", "stable", 2022, 2044)
V(KAMPTAL, 2019, 95, "exceptional", "Third exceptional Kamptal vintage — consistent with the Austrian pattern of 2015/2017/2019 dominance.", "rising", 2024, 2044)
V(KAMPTAL, 2022, 89, "very_good", "Warm vintage; Kamptal handled heat better than some DAC regions. Heiligenstein's altitude provided cooling. Good wines from committed producers.", "stable", 2026, 2038)

print("\n=== BURGENLAND VINTAGES ===")
V(BURGENLAND, 2015, 96, "exceptional", "Burgenland's greatest Blaufränkisch vintage of the 21st century — hot, dry conditions produced Moric Alte Reben of extraordinary graphite-mineral concentration. Umathum Hallebühl equally impressive. Also produced exceptional TBA from Neusiedlersee botrytis.", "rising", 2025, 2050)
V(BURGENLAND, 2017, 94, "exceptional", "Excellent Burgenland vintage — warm and dry with September precision. Blaufränkisch of excellent structure and longevity.", "stable", 2022, 2042)
V(BURGENLAND, 2013, 95, "exceptional", "The decade's most critically acclaimed Burgenland red vintage — perfectly ripe Blaufränkisch with exceptional natural acidity. Moric 2013 Lutzmannsburg is regularly cited as the finest Blaufränkisch ever made.", "rising", 2023, 2048)
V(BURGENLAND, 2019, 93, "exceptional", "Third excellent Burgenland vintage in four years — Blaufränkisch of excellent character and longevity.", "stable", 2024, 2042)

# ─── PORTUGAL ────────────────────────────────────────────────────────────────
print("\n=== DOURO TABLE WINE VINTAGES ===")
V(DOURO_TABLE, 2017, 97, "exceptional", "Portugal's finest Douro vintage in 20 years — perfect growing conditions throughout the region. Vale Meão, Niepoort, and Crasto all produced wines of extraordinary concentration and mineral depth. The defining vintage for the Douro DOC's international reputation.", "rising", 2027, 2052)
V(DOURO_TABLE, 2016, 94, "exceptional", "Excellent Douro vintage — very warm, dry growing season with critical September coolness. Douro Superior estates (Vale Meão) particular highlights. Wines of excellent concentration and ageing potential.", "stable", 2024, 2045)
V(DOURO_TABLE, 2019, 93, "exceptional", "Another strong Douro vintage — the region's consistency from 2015-2019 establishes it as one of the world's most reliable fine wine regions.", "stable", 2026, 2044)
V(DOURO_TABLE, 2011, 95, "exceptional", "The Port vintage of the decade also produced extraordinary Douro table wines. Vale Meão 2011 is considered the estate's greatest expression of its Douro Superior terroir.", "rising", 2021, 2046)
V(DOURO_TABLE, 2015, 92, "excellent", "Very good Douro vintage — slightly less exceptional than 2017 but wines of excellent structure and dark fruit concentration.", "stable", 2023, 2042)
V(DOURO_TABLE, 2020, 89, "very_good", "Warm, dry growing season — Douro table wines of good concentration. Not a benchmark year but consistently good quality from established producers.", "stable", 2025, 2038)

print("\n=== PORTO DOURO (PORT WINE) VINTAGES ===")
V(PORTO_DOURO, 2017, 99, "exceptional", "Declared as a universal vintage by all major Port houses — the first since 2011, and potentially the greatest Vintage Port since 1945. Taylor, Noval, Graham's, and Fonseca all produced wines of extraordinary concentration and longevity. 30+ year cellaring mandatory. The defining Port vintage of the 21st century.", "speculative", 2047, 2070)
V(PORTO_DOURO, 2016, 93, "excellent", "Declared by Quinta do Crasto, Ramos Pinto, and select single quintas. Not universally declared but Quinta do Noval's expression is considered exceptional.", "stable", 2030, 2050)
V(PORTO_DOURO, 2011, 97, "exceptional", "Universally declared — the decade's signature Port vintage before 2017. All major houses produced exceptional wines. Now entering early drinking window for patient consumers.", "rising", 2031, 2055)
V(PORTO_DOURO, 2007, 95, "exceptional", "The late 2000s' most universally praised Vintage Port declaration. Wines now 15-16 years old — approaching first drinking window but capable of 20 more years.", "stable", 2025, 2045)
V(PORTO_DOURO, 2003, 91, "excellent", "Hot, controversial vintage — early maturity was predicted but wines have developed well. Some houses produced exceptional wines; others overripe.", "stable", 2023, 2040)
V(PORTO_DOURO, 2000, 94, "exceptional", "Century vintage — universally declared and universally excellent. Taylor's and Fonseca's 2000 VPs are benchmark expressions now entering prime drinking.", "stable", 2022, 2045)

print("\n=== VINHO VERDE VINTAGES ===")
V(VINHO_VERDE, 2020, 93, "exceptional", "Excellent Vinho Verde vintage — sufficient Atlantic rainfall maintained freshness while warmer temperatures than usual enabled fuller phenolic development. Soalheiro Alvarinho of exceptional stone fruit and mineral precision.", "stable", 2021, 2028)
V(VINHO_VERDE, 2019, 91, "excellent", "Very good Monção e Melgaço vintage — warm enough to ripen Alvarinho fully without losing the sub-zone's characteristic saline minerality.", "stable", 2020, 2026)
V(VINHO_VERDE, 2022, 92, "excellent", "Warm, dry vintage — atypical for Vinho Verde but produced Alvarinho of excellent concentration. Stone fruit more prominent than saline character.", "stable", 2023, 2028)

print("\n=== ALENTEJO VINTAGES ===")
V(ALENTEJO, 2019, 94, "exceptional", "Alentejo's finest recent vintage — warm, dry growing season with excellent diurnal variation preserving freshness. Esporão Reserva from 2019 among the estate's finest expressions.", "stable", 2022, 2038)
V(ALENTEJO, 2017, 93, "exceptional", "Very hot, dry vintage — typical Alentejo strength. Full-bodied wines of excellent concentration with the usual dark fruit intensity.", "stable", 2021, 2036)
V(ALENTEJO, 2022, 90, "excellent", "Warm vintage — consistent with Alentejo's overall hot, dry character. Good wines from all major estates.", "stable", 2024, 2034)

print("\n=== MADEIRA VINTAGES ===")
# Madeira vintages work differently — wines last centuries; key recent declarations
V(MADEIRA_REGION, 1976, 96, "exceptional", "The benchmark year for modern vintage Madeira — producing wines of extraordinary complexity now 47+ years old. Blandy's and D'Oliveiras 1976 Sercial and Bual are reference examples of mid-century quality.", "speculative", 2000, 2080)
V(MADEIRA_REGION, 1990, 94, "exceptional", "Excellent Madeira harvest — the wines are now entering prime complexity at 33+ years. Particularly successful for Bual and Malmsey.", "speculative", 2005, 2070)
V(MADEIRA_REGION, 2000, 92, "excellent", "Millennium harvest — a useful benchmark for understanding younger vintage Madeira development. These wines are now 23 years old and showing early complexity.", "stable", 2010, 2060)
V(MADEIRA_REGION, 2010, 93, "exceptional", "One of the finest Madeira harvests of the 21st century — canteiro-aged expressions now 13+ years old and in excellent early development.", "rising", 2020, 2060)

print("\n✅ Terminal 5 Batch 7 — Vintages complete.")
