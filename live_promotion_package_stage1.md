# ══════════════════════════════════════════════════
#  THIS GOES TO: LIVE
#  Stage 1 Promotion Package — ASSEMBLED, NOT RUN
#  Waiting for the operator's words: "push it live"
# ══════════════════════════════════════════════════
Assembled: 2026-07-05 · Stage 1, Cycle 2

## What this package contains

Three parts. Each part names its target out loud. Nothing here has been
executed against live. Part C (open_folio zeroing) additionally requires
the founder folio review to be settled first.

---

## PART A — Code deploy to the live site

**Target: Fly app `provenance-tester-1` (provenance.kitchen)**

The branch `live-promo-stage1` (commit `519826c`) was built from the exact
code running on live today (baseline `5bb2c0b`, deployed Jun 25) plus ONLY
the four homepage commits, cherry-picked cleanly with no conflicts:

- `fb0a962` → Homepage transplant: recipe-first landing (press the seal)
- `f3e32cc` → Honest counts on landing page — published only
- `1b6a0c1` → Dark Plate Standard v1 — three landing plates
- `9f5888b` → The three fresh-eyes fixes (/beverage 301 redirect,
              plate-address weaving, no more silent zeros)

Nothing else on the dev branch (reading spread, library shelf, Stripe
webhook fix) rides along. The branch compiles. It sits checked out at
`/tmp/promo_stage1`.

**The command (NOT run):**
```
cd /tmp/promo_stage1 && fly deploy --config fly.toml --app provenance-tester-1
```

## PART B — Hero image addresses to the LIVE database

**Target: Postgres `provenance-tester-1-db`, database `provenance_tester_1`**
Slug-keyed, never id-keyed. Run through a proxy with the write user,
inside one transaction, with the database-name guard first.

```sql
-- GUARD: must print provenance_tester_1, or STOP.
SELECT current_database();

BEGIN;

UPDATE recipes
   SET image_url = 'https://v3b.fal.media/files/b/0aa0f3dc/F-usNegkG6GPh2qLPDP2K_610da61702bd4cc3bd370d0289712c70.jpg'
 WHERE slug = 'spaghetti-carbonara';                          -- expect: UPDATE 1

UPDATE recipes
   SET image_url = 'https://v3b.fal.media/files/b/0aa0f3dc/u8hOP6C1P4kmNmVz8Awmz_1fd7f03ac4ac453e82b328f9c308c796.jpg'
 WHERE slug = 'pad-thai';                                     -- expect: UPDATE 1

UPDATE technique_references
   SET image_url = 'https://v3b.fal.media/files/b/0aa0f3dc/XgdYLpA5t-MsjTsjncDgN_c38566f6a71644b3a02ed0ac0c943372.jpg'
 WHERE lower(name) = 'beurre blanc';                          -- expect: UPDATE 1

-- READ-BACK before COMMIT: three rows, three winner URLs.
SELECT slug, image_url FROM recipes WHERE slug IN ('spaghetti-carbonara','pad-thai');
SELECT name, image_url FROM technique_references WHERE lower(name) = 'beurre blanc';

COMMIT;  -- only if all three read back correctly; otherwise ROLLBACK;
```

## PART C — CANCELLED (founder ruling, 2026-07-06)

**There is no zeroing.** The founder walked all 134 open folios as a free
reader and ruled that every one stays open as a deliberate free sample.
The authoritative record is `founder_folio_list.md` (all 134 slugs
authorised). The package is now **Parts A and B only** — code, then hero
images.

## After the deploy — proof on live

1. `https://provenance.kitchen/` → 200, new landing, honest counts
2. Press all three seals — each plate blooms its photograph
3. `https://provenance.kitchen/beverage` → 301 → `/beverages`
4. A gated technique page as the smoke account — full pillars no longer
   served to free readers once open_folio is zeroed
5. Operator hard-refresh walk (Cmd+Shift+R) — nothing is shipped until
   you have walked it

# ══════════════════════════════════════════════════
#  END OF PACKAGE — NOTHING ABOVE HAS BEEN RUN
# ══════════════════════════════════════════════════
