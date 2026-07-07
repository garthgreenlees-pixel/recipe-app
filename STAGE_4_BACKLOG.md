# Stage 4 Backlog — logged, not yet worked

Items parked for Stage 4 (the audit fix-list stage), each with a one-line reason.

## Image storage + secrets ops — founder-logged 2026-07-07 (from the scan cycle)
- **staging password-reset emails silently fail — no email key.** No
  RESEND_API_KEY (or SMTP/email secret) is set on `provenance-staging`, so the
  password-reset flow can't send mail — resets fail silently. Set an email secret
  on staging (or make the flow surface a clear error when no mailer is configured).
- **Staging image volume — images die on deploy.** `EXTRACTED_DIR` on
  `provenance-staging` is ephemeral (no persistent volume), so scanned/uploaded
  hero images (`main.jpg`) vanish on every deploy/restart — that's why staging
  cards fall back to the monogram. Attach a Fly volume to staging and mount the
  image dir on it so images survive deploys.
- **`fly secrets set` needs a machine restart to apply.** After setting a secret
  the value shows "Staged" and a subsequent `fly deploy` re-stages it; the running
  machine keeps the old value until `fly machine restart`. Bit us on the scan key.
  Document in the deploy runbook: after any secret change, restart the machine and
  verify before proving.
- **Verify LIVE's image volume exists BEFORE promotion.** The `hero.jpg→main.jpg`
  alias fixes serving, but images only persist if a volume is mounted. Confirm
  `provenance-tester-1` has a persistent volume for the image dir (and that
  existing hero images are on it) before promoting anything image-dependent.

## Stable walk access — founder-ordered 2026-07-07 (do AFTER MyKitchen ships)
**Problem:** staging logins break repeatedly and there is no self-service reset
(staging has no outbound email, so the password-reset flow is dead). Fixing a
login by hand is costing the founder real walk time — and the founder's walks
ARE the quality gate, so access to them must never be the bottleneck.
Scope this as ONE small cycle:
- **Deploy-durable walk seats.** Idempotent seeding of fixed walk accounts
  (e.g. `smoke@test.local`, plus one per tier: kitchen/library/profession) with
  a known, non-secret, **pbkdf2** password hash (NOT scrypt — local `hashlib`
  on this Mac lacks `scrypt`, which silently produced a blank hash before). Run
  the upsert on every boot / as a re-applied migration so no deploy can wipe or
  drift it. The seat survives every deploy by construction.
- **Login proven as a deploy proof-step.** "Walk seat login proven ✓" becomes a
  standard line in EVERY cycle report — the walk credential is verified as part
  of the same machine-proof that checks the feature. (Adopt this line now, ahead
  of the cycle, since each cycle already logs in to prove.)
- **Founder one-liner reset.** A tiny script — `scripts/staging_reset_pw.sh
  <email> <password>` — that opens the staging DB proxy, writes a pbkdf2 hash,
  and confirms, so the founder can reset any staging password without a
  conversation. (Same shape usable for live via a separate guarded flag.)
- Interim (works today): `smoke@test.local` / `walk_2026` (pbkdf2), 14-recipe
  seat; reset by hand via the staging proxy when it drifts.

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
- **service_specs backfill (grind lane).** 97 of 405 published pours carry no
  service_specs (temperature/vessel/pour). Data-only; the sommelier panel's
  service rows render only where data exists.

## FINDING 3 — the ceviche gap (founder-logged 2026-07-06; becomes CYCLE 4 after MyKitchen)
Leche de tigre resolved to nothing sharp. Causes and fixes in founder's order:
(a) mixed drinks — the ~500 drink recipes become pairable entries with
structure and markers (a michelada or chicha morada should have answered);
(b) world non-alcoholic serves (Thai and beyond) join beverage_preparations —
grind-lane content once shapes exist; (c) free-text dish entry (dish door
item 3) — founder sets ANTHROPIC_API_KEY on staging himself. Cycle 4 must be
scoped precisely against approved spec v1.1 and STOP for founder approval of
the plan before any build — must not balloon.
