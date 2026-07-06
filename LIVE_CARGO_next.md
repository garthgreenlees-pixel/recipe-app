# ══════════════════════════════════════════════════
#  THIS GOES TO: LIVE — NEXT CARGO, waiting for "push it live"
# ══════════════════════════════════════════════════
Assembled 2026-07-06. Nothing here has run against live.

## Cargo A — the two publish gates (code)
Both proven on staging; both close public exposure on live:
- **d62278c** — producer publish gate (closes the 429 unpublished producers
  publicly reachable by raw id today)
- **<products gate commit>** — product publish gate (5,366 unpublished
  products invisible to the public everywhere; published untouched)
- Plus the 3b build commits on dev (producer page rebuild, onboarding flow).

The live deploy is the same move as the Stage 1 promotion: cherry-pick /
deploy the dev branch to provenance-tester-1. Recommend deploying the whole
proven-on-staging dev branch as one promotion when you give the word, rather
than cherry-picking gate-by-gate.

## Cargo B — the two new tables (LIVE DDL)
Applied to STAGING already; LIVE needs this run (schema change — your words):
```
-- against the LIVE database provenance-tester-1-db, guarded:
SELECT current_database();   -- must be provenance_tester_1 or STOP
\i migrations/3b_supplier_onboarding.sql
```
The migration is idempotent (CREATE TABLE IF NOT EXISTS). Without these
tables the suggest-a-supplier route and the onboard admin page will error on
live, so the DDL must land in the same window as Cargo A.

## Proof already on staging
- Producer/product unpublished → 404; published → 200
- Public product count 5,771 → 405 everywhere (door, API, sitemap)
- Suggestion POST → queue row at 'suggested' + demand-ledger event
- /admin/beverages/onboard → login-gated (302), renders the queue for admin

## Still your ruling before any of this rides
The words: **push it live**.
