# Stage 4 Backlog — logged, not yet worked

Items parked for Stage 4 (the audit fix-list stage), each with a one-line reason.

## From the credential rotation (2026-07-06)
- **Batch scripts → env vars.** ~280 tracked scripts hardcode
  `provenance_tester_1:GBN1MbQJ…` (add_recipes_*, backfill_*, publish_*,
  kristang_*, t23_batch*, scripts/promote_canon.py, …). They now FAIL auth
  (the leaked password refuses). Move them to read `DATABASE_URL_WRITE` from
  env; do not re-hardcode. Grind work — step-down eligible.
- **Managed Postgres migration — its own future project.** `provenance-tester-1-db`
  is legacy unmanaged `postgres-flex 17.2`; Fly won't support credential
  rotation or ops on it. Migrating to Fly Managed Postgres (MPG) is the
  durable fix for the whole credential class. Scope it as a standalone project
  (dump/restore, cutover window, secret repoint) — not a quick fix.
- **iMac jobs — verify against the new role.** This morning's ~14h password
  revert points to an external periodic re-provisioner; this Mac is clean, so
  the likely culprit is a launchd/cron job on the iMac. When the iMac is next
  reachable: find any job that connects as or re-passwords `provenance_tester_1`,
  and repoint/kill it against the new `prov_app_write` credential. Watch
  signal in the meantime: if `GBN1MbQJ…` ever authenticates again, that job
  is live.
- **Reader password rotation — SEQUENCED BEFORE/ALONGSIDE STRIPE GO-LIVE
  (founder, 2026-07-06).** `provenance_reader` is still leaked in the repo
  (batch_generate_images.py, .env, ~/live_db_uri.txt) and still live. Lower
  stakes than the writer (read-only), but it **must not still be live when
  real member data starts accumulating** — so rotate it before or in the same
  window as Stripe going live, not after. Same pattern as the writer rotation
  tonight: create a fresh reader role (`prov_app_read`) with a new
  non-committed password + least privilege (SELECT only), repoint the app's
  `DATABASE_URL` secret and local `.env` in the same window, prove the old
  `provenance_reader` password refuses, and repoint the operational
  db-watcher (which authenticates as the reader — see [[credential-rotation-status]]).
  Retire the leaked `~/live_db_uri.txt` copy too.
- **prov_app_write least-privilege.** It is SUPERUSER because `init_db()` runs
  boot-time DDL on the write connection. Remove boot DDL (guard init_db to
  skip when tables exist), then downgrade the role to DML + owned-object
  rights.

## From Stage 3b discovery (2026-07-06)
- ~~**Product publish flag decision.**~~ RESOLVED 2026-07-06: founder ruled
  "invisible everywhere, one doctrine for the whole cellar." Product publish
  gate enforced across all public surfaces (commit 482568a), proven on
  staging, queued as live cargo. No longer a Stage 4 item.
- **Batch-publish vetted products.** With the gate enforced, only 405 of
  5,771 products are public. The 553-producer load + product publishing (spec
  L1–L4) is the path to opening the rest — 3b data-load work, step-down
  eligible, founder decides which products publish.

## Discovered during 3b onboarding (2026-07-06)
- **Pre-existing role-case mismatch in beverage_product_suppliers.** The CHECK
  constraint allows lowercase `origin`/`provider`, but the menu-suggest
  queries (server.py ~16357/16411) filter uppercase `'PROVIDER'`/`'ORIGIN'` —
  they can never match, which is one reason the junction sat empty. The 3b
  onboarding wiring uses constraint-valid lowercase `provider` and renders via
  the product-detail supplier block (no role filter). Reconcile the menu-suggest
  queries to lowercase so wired providers also surface in menu beverage
  suggestions. Not blocking the onboarding path.

## Grind-lane log from pairing-grammar diagnosis (2026-07-06, founder-ordered 2.3b)
- **flavour_weight thin on two families.** All 405 published pours carry
  flavour_markers (100% coverage, every family) — the croissant silence was
  ranking logic, since fixed, NOT missing data. But `flavour_weight` is
  missing on tea (43 of 64 published) and baijiu (8 of 8); those pours fall
  back to a neutral weight in the grammar's rank. Grind lane: backfill
  flavour_weight for tea and baijiu published rows. Data-only; no code.
