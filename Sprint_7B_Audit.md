# Sprint 7B Audit — Pricing Flow Architecture

*Cycle 7B, 2026-05-21. No code changes. No commits. Review-gated artifact.*

---

## Status: Step 1 — Cycle 7A Closed

`git stash` applied cleanly. `git status` shows working tree clean (untracked files only — pre-existing, not from 7A). Server.py line 11899 confirmed: `def _resolve_ingredient_master_id(cur, name):` — original 2-arg signature, no `_cost7a` parameter, no `[COST-7A]` lines anywhere in the file.

Current DB population (for orientation):
- `ingredient_master`: 1,799 rows
- `ingredient_aliases`: 1,991 rows — source breakdown: canonical=1,796, recipe=141, invoice=36 (31 linked, 5 NULL-linked), legacy_pricing=17, user=1, ai_seed=0
- `price_history`: 82 rows (from a prior period when DUAL_WRITE was briefly on)

---

## Audit 2a — Call Sites of `_resolve_ingredient_master_id`

Six call sites across three contexts. Definition at line 11899.

### Call site 1 — `_cost_ingredient_loop`, new model path (line 12039)

```
Route/function: _cost_ingredient_loop (shared helper)
Line: master_id, was_resolved = _resolve_ingredient_master_id(cur, normalized)
Context: READ_NEW_INGREDIENT_MODEL=1 branch — resolves recipe term to
         ingredient_id, then queries price_history for user/global price.
Result used for: ingredient_id FK into price_history SELECT.
Effect of flipping DUAL_WRITE=1: none — this call site is read-only,
  reads price_history. DUAL_WRITE affects writers. No interaction.
Effect of flipping READ_NEW_MODEL=1: activates this path (currently dormant).
```

### Call site 2 — `_cost_ingredient_loop`, old model alias bridge (line 12099)

```
Route/function: _cost_ingredient_loop (shared helper)
Line: _master_id, _was_resolved = _resolve_ingredient_master_id(cur, normalized)
Context: OLD model (READ_NEW_INGREDIENT_MODEL=0) fallback — fires only when
         both ILIKE passes against ingredient_pricing and ingredient_prices fail.
         Resolves recipe term to canonical_name, retries both pricing tables
         with canonical.
Result used for: canonical_name lookup, then ILIKE retry on both tables.
Effect of flipping DUAL_WRITE=1: none — this is a read path.
Notes: THIS IS THE ACTIVE PATH today. The ILIKE+word-boundary bridge
       exposed by Cycle 7A probes. Fails when recipe term is not a
       contiguous substring of supplier text AND ingredient_master has no entry.
```

### Call site 3 — `costing_compare` admin parity endpoint (line 12504)

```
Route/function: GET /api/internal/costing-compare/<slug> (admin-only, X-Admin-Token)
Line: master_id, was_resolved = _resolve_ingredient_master_id(cur, ing_name)
Context: Phase 3 diagnostic tool. Runs both old-model (ingredient_pricing ILIKE)
         and new-model (price_history via resolver) side by side and reports
         parity: "match", "diff", "old_only", "new_only", "neither".
Result used for: per-ingredient parity dict returned to admin caller.
Effect of flipping DUAL_WRITE=1: new-model column populates as invoices are
  applied → parity results become meaningful rather than showing "old_only"
  for everything.
Notes: Read-only diagnostic. Safe at all times. Requires ADMIN_TOKEN header.
```

### Call site 4 — `invoices/scan` dual-write block (line 12833)

```
Route/function: POST /api/invoices/scan — inside _dual_write_enabled() gate
Line: ingredient_master_id, was_resolved = _resolve_ingredient_master_id(cur, raw_desc)
Context: At invoice SCAN time (OCR step), before the user edits/confirms lines.
         If resolved: writes ingredient_aliases row with source='invoice',
           ingredient_id=master_id, ON CONFLICT DO NOTHING.
         If unresolved: writes ingredient_aliases row with ingredient_id=NULL,
           source='invoice', ON CONFLICT DO NOTHING (dangling placeholder).
Result used for: alias INSERT into ingredient_aliases (linked or NULL-linked).
Effect of flipping DUAL_WRITE=1: ACTIVATES this path. Every OCR line starts
  creating alias rows. Unresolved OCR lines create NULL-linked rows.
⚠ FLAG: NULL-linked rows (ingredient_id=NULL) created here silently block
  7C's ai_seed INSERTs for the same alias_lower via ON CONFLICT DO NOTHING.
  See Audit 2c for full analysis.
```

### Call site 5 — `invoices_apply` dual-write block (line 12950)

```
Route/function: POST /api/invoices/<id>/apply — inside _dual_write_enabled() gate
Line: master_id, was_resolved = _resolve_ingredient_master_id(cur, ingredient_name)
Context: At invoice APPLY time (user confirmed the ingredient name).
         ingredient_name here is the user-edited OCR text (raw supplier string).
         If resolved: writes price_history row, writes ingredient_aliases row
           source='invoice', ON CONFLICT DO NOTHING.
         If unresolved: logs warning, skips price_history write, skips alias.
Result used for: price_history INSERT (canonical FK), alias INSERT.
Effect of flipping DUAL_WRITE=1: ACTIVATES this path. Invoice applies start
  populating price_history. Only resolves if ingredient_name matches an
  existing alias or ingredient_master entry — raw supplier text (e.g.
  "Tellicherry Black Pepper DOP wheel cut") will resolve IF "black pepper"
  is a substring of the canonical name or alias.
Notes: This is the PRIMARY target for Cycle 7F (canonical normalization at
  apply time). See Step 4 / diagnosis section.
```

### Call site 6 — `pricing_manual` dual-write block (line 13156)

```
Route/function: PUT/POST /api/pricing/manual — inside _dual_write_enabled() gate
Line: master_id, was_resolved = _resolve_ingredient_master_id(cur, ingredient_name)
Context: User manually enters an ingredient name and price.
         Same pattern as invoices_apply: if resolved, writes price_history
         and alias row. If unresolved, logs and skips.
Result used for: price_history INSERT, alias INSERT.
Effect of flipping DUAL_WRITE=1: activates. Manual entries start populating
  price_history. User-typed ingredient names are generally cleaner than OCR
  output, so resolution rate expected to be higher than invoice scan.
```

---

## Audit 2b — Read Paths Touching `price_history`

No `price_history` references found in any HTML template. All read paths are in `server.py`.

### Read path 1 — `_cost_ingredient_loop`, new model (lines 12044, 12058)

```
Guard: _read_new_model_enabled() — currently OFF (READ_NEW_INGREDIENT_MODEL not in .env)
Queries:
  (1) price_history WHERE ingredient_id=%s AND user_id=%s AND source IN
      ('invoice','manual','backfill_legacy') ORDER BY effective_date DESC LIMIT 1
  (2) price_history WHERE ingredient_id=%s AND is_global=true
      ORDER BY effective_date DESC LIMIT 1 (fallback if no user row)
Defensiveness: LIMIT 1 + fetchone() — returns None if table is empty. Safe.
Risk if DUAL_WRITE turns on: None. This path is dormant until READ_NEW_MODEL=1.
  Populating price_history via DUAL_WRITE does not activate this reader.
```

### Read path 2 — `costing_compare` parity check (lines 12477–12513)

```
Guard: admin X-Admin-Token — not gated on feature flags; always runs both paths
Queries:
  COUNT(*) from price_history WHERE user_id=%s AND source IN ('invoice','manual')
  Per-ingredient: price_history WHERE ingredient_id=%s AND user_id=%s LIMIT 1
Defensiveness: COUNT returns 0 (not NULL) if empty. Per-ingredient fetchone()
  returns None → parity="old_only". Fully defensive.
Risk: None. Diagnostic-only, no writes.
```

### Read path 3 — `GET /api/pricing/user`, new model (lines 13079–13093)

```
Guard: _read_new_model_enabled() — currently OFF
Query: price_history ph LEFT JOIN ingredient_master im WHERE ph.user_id=%s
       AND ph.source IN ('invoice','manual','backfill_legacy')
       ORDER BY ph.effective_date DESC, im.canonical_name ASC
Defensiveness: LEFT JOIN means even if ingredient_master row is missing
  (shouldn't happen with FK), COALESCE supplies a fallback string.
  Returns empty list if price_history is empty. Safe.
Risk: None while OFF. One subtle issue for later: this path reads ALL
  price_history rows for the user regardless of is_active. The old model
  has an is_active boolean for deactivation. The new model doesn't have
  an equivalent — deactivation in price_history is implicit (most recent
  row wins via ORDER BY date). Confirm this matches the intended behavior
  before flipping READ_NEW_MODEL=1.
```

**Summary:** All three price_history read paths are gated behind feature flags or are diagnostic-only. Populating price_history via `DUAL_WRITE=1` will not affect any live user-facing read until `READ_NEW_MODEL=1` is also set. Safe to enable DUAL_WRITE independently.

---

## Audit 2c — `ingredient_aliases` Read/Write Surface

### Write sites

**W1 — `invoices/scan` dual-write, resolved (line 12836):**
```sql
INSERT INTO ingredient_aliases (ingredient_id, alias, source)
VALUES (%s, %s, 'invoice')
ON CONFLICT (alias_lower) DO NOTHING
```
Source: `'invoice'` ✅ (in check constraint)

**W2 — `invoices/scan` dual-write, unresolved (line 12842):**
```sql
INSERT INTO ingredient_aliases (ingredient_id, alias, source)
VALUES (NULL, %s, 'invoice')
ON CONFLICT (alias_lower) DO NOTHING
```
Source: `'invoice'` ✅. ingredient_id: NULL — creates dangling placeholder.

**W3 — `invoices_apply` dual-write (line 12976):**
```sql
INSERT INTO ingredient_aliases (ingredient_id, alias, source)
VALUES (%s, %s, 'invoice')
ON CONFLICT (alias_lower) DO NOTHING
```
Source: `'invoice'` ✅

**W4 — `pricing_manual` dual-write (line 13176):**
Same pattern as W3. Source: `'invoice'` ✅

**Planned 7C seed source:** `'ai_seed'` ✅ (added in Cycle 6J-3, present in constraint)

### Read sites

**R1 — `_resolve_ingredient_master_id`, path 1 (line 11917):**
```sql
SELECT ingredient_id FROM ingredient_aliases
WHERE alias_lower = %s AND ingredient_id IS NOT NULL
LIMIT 1
```
No ORDER BY. Safe because `alias_lower` has a UNIQUE index — at most one row per alias_lower. LIMIT 1 is redundant but harmless.

### Conflict between dual-write scan (W2) and 7C seed

⚠ **FLAG — NULL-linked alias blocks 7C seed:**

Currently 5 NULL-linked `source='invoice'` rows exist. If any of their `alias_lower` values overlap with 7C seed entries, the 7C seed's `ON CONFLICT DO NOTHING` will silently skip those entries. The resolver (R1) ignores NULL-linked rows (`ingredient_id IS NOT NULL` filter), so those aliases are effectively invisible to the cost loop.

**Recommended fix for 7C seed script:** Use `ON CONFLICT (alias_lower) DO UPDATE SET ingredient_id = EXCLUDED.ingredient_id, source = EXCLUDED.source` when `ingredient_id` is being upgraded from NULL to a real ID. Alternatively, add a pre-seed step: `DELETE FROM ingredient_aliases WHERE ingredient_id IS NULL AND source = 'invoice'` — safe since these rows are non-functional anyway.

### Source constraint (current, from init_db line 1027)
```
CHECK (source IN ('canonical', 'recipe', 'invoice', 'user', 'legacy_pricing', 'ai_seed'))
```
All dual-write write sites use `'invoice'` ✅. 7C seeder will use `'ai_seed'` ✅. No mismatch.

---

## Audit 2d — Schema Verification

### `ingredient_master`

| Column | Type | Nullable | Default |
|---|---|---|---|
| id | integer | NOT NULL | GENERATED ALWAYS AS IDENTITY |
| canonical_name | text | NOT NULL | — |
| category | text | nullable | — |
| base_unit | text | NOT NULL | `'g'` |
| yield_factor | numeric(5,4) | NOT NULL | `1.0000` |
| allergen_tags | text[] | nullable | `'{}'` |
| origin_country | text | nullable | — |
| origin_brand | text | nullable | — |
| description | text | nullable | — |
| purveyor_tier | text | nullable | — |
| region_tags | jsonb | nullable | — |
| source_product_id | integer | nullable | — |
| is_active | boolean | nullable | `true` |
| created_at | timestamp | nullable | `now()` |
| updated_at | timestamp | nullable | `now()` |

**Unique index:** `lower(canonical_name)` — uniqueness enforced on lowercased name.
**7C must provide:** `canonical_name` only. `base_unit` defaults to `'g'`, `yield_factor` to `1.0`. All other columns nullable.
**Do NOT provide:** `id` (GENERATED ALWAYS — error if supplied).

### `ingredient_aliases`

| Column | Type | Nullable | Default |
|---|---|---|---|
| id | integer | NOT NULL | GENERATED ALWAYS AS IDENTITY |
| ingredient_id | integer | nullable | — |
| alias | text | NOT NULL | — |
| alias_lower | text | nullable | GENERATED ALWAYS AS `lower(alias)` STORED |
| source | text | NOT NULL | — |
| created_at | timestamp | nullable | `now()` |
| confidence | numeric(3,2) | nullable | — |
| reasoning | text | nullable | — |
| approved_at | timestamp | nullable | — |

**Unique index:** `alias_lower` — one row per unique lowercased alias globally.
**Check constraint:** `source IN ('canonical','recipe','invoice','user','legacy_pricing','ai_seed')`
**7C must provide:** `ingredient_id` (FK to ingredient_master.id), `alias`, `source='ai_seed'`.
**Do NOT provide:** `id` or `alias_lower` (both GENERATED ALWAYS).
**FK constraint:** `ingredient_id → ingredient_master(id) ON DELETE CASCADE`.

### `price_history`

| Column | Type | Nullable | Default |
|---|---|---|---|
| id | uuid | NOT NULL | `gen_random_uuid()` |
| ingredient_id | integer | NOT NULL | — |
| user_id | text | nullable | — |
| is_global | boolean | NOT NULL | `false` |
| supplier_id | integer | nullable | — |
| supplier_name | text | nullable | — |
| price_per_unit | numeric(12,4) | NOT NULL | — |
| unit | text | NOT NULL | — |
| currency | char(3) | NOT NULL | `'CAD'` |
| yield_factor | numeric(5,4) | NOT NULL | `1.0000` |
| invoice_id | uuid | nullable | — |
| invoice_line_id | uuid | nullable | — |
| effective_date | date | NOT NULL | — |
| source | text | nullable | — |
| created_at | timestamp | nullable | `now()` |

**Check constraint:** `source IN ('invoice','manual','backfill_legacy','backfill_global')`
**⚠ FLAG — `'ai_seed'` is NOT a valid source for price_history.** If 7C or any future cycle wants to seed global reference prices into price_history, use `source='backfill_global'`. Using `'ai_seed'` here would violate the check constraint and raise a DB error.
**Indexes:** `idx_price_history_global` (ingredient_id, is_global, effective_date DESC WHERE is_global=true), `idx_price_history_ingredient_user_date` (ingredient_id, user_id, effective_date DESC).

---

## Flags for 7C/7D Planning

1. **NULL-linked alias collision (HIGH):** 5 existing `source='invoice'`, `ingredient_id=NULL` rows in `ingredient_aliases`. 7C seed script must use `ON CONFLICT (alias_lower) DO UPDATE` (not `DO NOTHING`) to upgrade NULL-linked rows to properly-linked ones, OR pre-delete them. Otherwise some seed entries will silently vanish.

2. **price_history source constraint (MEDIUM):** `'ai_seed'` is not in `price_history`'s source check constraint. Any global seed pricing (7C or later) must use `source='backfill_global'`. Do not use 'ai_seed' for price_history rows.

3. **is_active has no equivalent in price_history (LOW):** The old model uses `ingredient_pricing.is_active=true` to deactivate superseded prices. The new model uses recency (ORDER BY effective_date DESC LIMIT 1). Before READ_NEW_MODEL=1 is flipped, verify that the "most recent row wins" semantic matches the product intent for price deactivation.

4. **DUAL_WRITE safe to enable independently (CONFIRMED):** All price_history read paths are gated behind READ_NEW_MODEL=1. Enabling DUAL_WRITE=1 alone will populate price_history without touching any live user-facing read. Parity check endpoint becomes useful once DUAL_WRITE=1 is on.
