# COMMON RULES — Every Relay Session

These rails apply to every canon directive in this folder without exception.

---

## 1. Source-Anchored Method

Entries are written FRESH in Provenance voice against recognized, web-verified authorities drawn from Library_Manifest Tier 1 titles and established external references. Every factual claim must be traceable to a named source. Unverifiable facts carry `[VERIFY]`; guesses are never written.

## 2. Validation Gate

Every entry passes `validate_entry()` before commit:

- Pillar depth check (technique anatomy present)
- Banned-word scan (no vague terms: "delicious", "unique", "various", "typically", "often", "sometimes", "popular")
- Regional specificity check (no pan-region flattening)
- Te-reo / native-term preservation: first use carries the term; English translation follows in parentheses on first occurrence; subsequent uses may use the term alone
- Minimum length thresholds per entry type

## 3. Selectivity Principle

- 100% cultural and reference architecture
- 30–50% canonical recipes
- Zero author-fusion (do not blend two sources into one entry — each entry names its source)
- Zero Western accommodations (no "you can substitute…", no apology for unfamiliar ingredients)

## 4. Supplier Mentions

Supplier mentions → `SUPPLIER_MENTIONS_<CANON>.md` in the repo. Each entry web-verified (producer exists, product is real). Never invented.

## 5. Operational Discipline

- Batch commits with neighbour-table checksums after each batch
- `recipes` table is untouched
- No deploys during relay sessions
- Pace: ≤ 75 rows per 15 minutes

## 6. Heartbeat

After each batch: write one `HEARTBEAT` line to `~/Desktop/Provenance/Watcher/WEEKEND_STATUS.md` naming the canon, batch number, rows committed, and running total.

Full log per canon written to the repo (filename: `<canon>_relay_log.md`).

## 7. Batch Plan First

Before writing begins: report the batch plan (entry list with types) to the status file. Only then start writing.

## 8. Stop Conditions

Stop entirely (do not proceed to next directive) if:

- The same validation error recurs across two consecutive batches
- A checksum anomaly is detected on any neighbour table
- Any ambiguity arises about cultural attribution or source authority
