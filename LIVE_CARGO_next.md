# ══════════════════════════════════════════════════
#  THIS GOES TO: LIVE — FULL 3b PACKAGE, waiting for "push it live"
# ══════════════════════════════════════════════════
Assembled 2026-07-06. Nothing here has run against live. Schema change pre-ruled
by the founder (approved to ride this package, guarded, on words only).

## The package — assembled and ready
Branch **live-promo-3b** (@ dd01c49), built from the exact live code (519826c)
+ only the 9 beverage gate/3b code commits cherry-picked clean. 4 files change
vs live: server.py, templates/beverage_producer.html,
templates/admin_beverages_onboard.html, migrations/3b_supplier_onboarding.sql.
Compiles. The held work (reading spread, library shelf, Stripe webhook fix)
does NOT ride — surgical, per the Stage 1 promise.

Contents, all proven on staging:
- Producer publish gate (closes the 429 unpublished producers reachable by id)
- Product publish gate (5,366 unpublished products invisible everywhere;
  public cellar 5,771 → 405, consistent across door/API/sitemap)
- Producer page rebuilt to the mockup standard
- Suggest-a-Supplier flow + demand ledger + admin onboarding surface
- Verification-check ladder (honest checks) + product-wiring → gold links
- Supplier render gate (only verified_provider suppliers show as gold links)
- 4 pre-existing bugs fixed (service_region array, country NOT NULL, role-case
  constraint, bps.notes → bps.availability)

## THE RUN, on your words "push it live" — in order:

### Step 1 — schema first (guarded), against the LIVE database
```
fly proxy 15500:5432 -a provenance-tester-1-db   # then, as the write user:
psql -h 127.0.0.1 -p 15500 -U prov_app_write -d provenance_tester_1 \
  -c "SELECT current_database();"                # must print provenance_tester_1 or STOP
psql ... -f migrations/3b_supplier_onboarding.sql # idempotent CREATE TABLE IF NOT EXISTS
```
Schema before code, so the onboarding routes have their tables the moment the
new code boots.

### Step 2 — code
```
cd /tmp/promo3b   # (worktree on branch live-promo-3b)
fly deploy --config fly.toml --app provenance-tester-1
```

## Proof plan (I run immediately after, report back)
1. Route sweep 200: / · /beverages · /beverage/<slug> · /drinks · a technique
   page · /library
2. Gates: an unpublished producer id → 404; an unpublished product id → 404;
   public product count = 405 on the door + API + sitemap agree
3. Onboarding: /admin/beverages/onboard is login-gated (302 anon); the
   suggest-a-supplier POST records a queue row + a demand-ledger event
4. Wiring: (you or I, as founder) run checks → wire a real supplier → confirm
   the gold link renders on that product; confirm a verified_listed supplier
   does NOT render
5. Browser walk of a producer page + your hard-refresh walk

## Rollback (one line each)
- Code: `fly deploy` the previous release, or redeploy branch live-promo-stage1
  (519826c) — the exact code live runs right now.
- Schema: the tables are additive (CREATE TABLE IF NOT EXISTS) and nothing
  else reads them yet, so rollback = leave them (harmless) or
  `DROP TABLE beverage_demand_ledger, supplier_verification_queue;` guarded.
- The gates are pure query filters — reverting the code reverts them wholesale.

## Not in this package (by design)
- Stripe webhook fix (3fc2555) — waits for Stage 2 proof on staging.
- Reading spread / library shelf — their own stages.

Waiting on: **push it live**.
