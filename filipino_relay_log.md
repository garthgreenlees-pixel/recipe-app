# Relay Log — Directive 05: Filipino

## Session Summary
- **Directive:** 05_filipino.md
- **Session type:** Depth pass (directive noted ~11 entries in DB; actual DB check found 0 PH entries — this was the initial extraction)
- **Entries planned:** 21
- **Entries committed:** 21
- **Validation failures:** 2 (all fixed before commit)
- **Supplier mentions queued:** 0 (5 brand/venue references retained as documentary, not endorsement)

## Authorities Web-Verified
| Authority | Status | Notes |
|-----------|--------|-------|
| Doreen Fernandez | VERIFIED | Palayok (Bookmark Inc, 2000, ISBN 978-9715693776); Tikim (Anvil, 1994, ISBN 978-9712703836). Foundational authority. Died 2002. |
| Claude Tayag | VERIFIED | Food Tour (Anvil, 2006, ISBN 978-9712718328); Linamnam (Anvil, 2012, ISBN 978-9712726408); The Ultimate Filipino Adobo (FSI, 2022, ISBN 978-9715521796); Kulinarya co-author. Kapampangan authority. |
| Margarita Fores | VERIFIED | Kulinarya co-author (Anvil, 2008, ISBN 978-9712721083). Asia's Best Female Chef 2016. No solo book. Died Feb 2025. |
| Amy Besa & Romy Dorotan | VERIFIED | Memories of Philippine Kitchens (Harry N. Abrams, 2006, ISBN 978-1584794516). IACP Jane Grigson Award 2007. |

## Batch Log

### Batch 1 — Adobo Technique Family (PH-1 to PH-6)
- **Entries:** PH-1 (Manila adobo — baseline technique), PH-2 (adobo sa gata — Bicolano coconut), PH-3 (adobo sa dilaw — Visayan turmeric), PH-4 (adobong Ilocano — dry-rendered), PH-5 (adobong Kapampangan — pork-fat doctrine), PH-6 (adobong puti — white/pre-colonial)
- **Validation:** 1 fail (PH-5: "typically" banned word), fixed ("uses"), 6/6 PASS
- **Commit:** 5165613

### Batch 2 — Acid + Fermentation (PH-7 to PH-11)
- **Entries:** PH-7 (kinilaw — acid-denatured raw fish), PH-8 (kilawin — acid-denatured offal/grilled meat), PH-9 (bagoong — fermented shrimp/fish paste), PH-10 (patis — fish sauce), PH-11 (buro — fermented rice-fish)
- **Validation:** 1 fail (PH-11: "various" banned word), fixed ("secondary flavour compounds (acetaldehyde, diacetyl, ethanol)"), 5/5 PASS
- **Commit:** 68f722c

### Batch 3 — Regional Techniques (PH-12 to PH-16)
- **Entries:** PH-12 (pinakbet — Ilocano vegetable technique), PH-13 (Bicol Express — Bicolano chile-coconut), PH-14 (sisig — Kapampangan offal transformation), PH-15 (paksiw — vinegar-braising family), PH-16 (sinigang — tamarind-acid souring)
- **Validation:** 5/5 PASS (no failures)
- **Commit:** 1529505

### Batch 4 — Techniques + Colonial/Trade Threads (PH-17 to PH-21)
- **Entries:** PH-17 (lechon — whole-roast pig), PH-18 (sinuglaw — grilled + acid compound), PH-19 (dinuguan — blood stew), PH-20 (pancit — Chinese-Filipino noodle family), PH-21 (estofado/mechado — Spanish-colonial braising)
- **Validation:** 5/5 PASS (no failures)
- **Commit:** 30dd499

## Regional Attribution
All 21 entries attribute to specific regional traditions:
- **Tagalog/Manila:** PH-1, PH-16, PH-17 (Manila lechon), PH-19, PH-20, PH-21
- **Ilocano:** PH-4, PH-8 (kilawing kambing), PH-12
- **Bicolano:** PH-2, PH-13
- **Visayan/Cebuano:** PH-3, PH-7, PH-17 (Cebuano lechon), PH-18
- **Kapampangan:** PH-5, PH-11, PH-14
- **Pan-Philippine:** PH-6, PH-9, PH-10, PH-15

## Cross-References Created
- PH → Pacific Corridor: PH-2↔WS-4 (coconut cream), PH-7↔TP-1/CK-2/TO-3/FJ-2 (acid denaturation), PH-13↔FJ-5 (coconut cream braising)
- PH internal: extensive cross-referencing across all 21 entries (adobo family PH-1–6 cross-linked; fermented larder PH-9–11 cross-linked; regional techniques cross-linked to fermented larder)
- PH → Colonial threads: PH-21 documents Spanish-colonial braising; PH-20 documents Chinese-trade noodle adaptation
