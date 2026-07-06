# THE BEVERAGE EXPERIENCE — Stage 3a Specification v1
**Date:** 2026-07-05 · **Status:** AWAITING FOUNDER APPROVAL — nothing below is built until approved
**Governing doctrine:** `Doctrines/VISIBILITY_DOCTRINE.md` — *local by default, global by discovery; the gap is the signal.*
**Governing standard:** The Sashimi Standard, applied to beverage entries exactly as to food.
**Founder rulings encoded:** interview answers Q1–Q9 (2026-07-05) + the two-week push directives.

---

## 0 · What this is

/beverages is not repaired — it is rebuilt into a revenue-earning, sommelier-grade
experience, integral to the site. This document names every page, every gate, and
every data load required. Scope discipline: this stage builds the visibility rules
and the signal capture — NOT a marketplace, NOT supplier messaging, NOT commerce.
The ledger accumulates; the business acts on it later.

Beverage is the proving ground, not the boundary — §12 names where this extends
to ingredients and the whole Pantry.

---

## 1 · The reader journey (the spine of the experience)

Homepage → **the region door** (/beverages — "your cellar") → **a producer** →
**a bottle** (or bag, or tin — the product) → **the pairing** → **the local
provider** (Pat's Rule gold link) — or, where no provider exists, the **honest
origin-only rendering** and a quiet mark in the demand ledger.

Every step reads in the sommelier register: a head sommelier explaining to a
capable cook. Reasoning always shown — what bridges, what contrasts, what cuts.
Never a list of names. Voice rules apply in full (no banned words; "Enter";
empty states in the house style).

---

## 2 · The region model (Q1)

- **Matching grain: province/state** (BC, WA, OR, ON, …), because supplier
  service regions are already shaped that way. **City is recorded in the demand
  ledger when known**, never used to wall content.
- **Detection:** auto-detect (existing `get_user_location()` — Accept-Language
  fallback), with a **visible region switch** on every beverage surface:
  "You're standing in **British Columbia's** cellar — change region."
- **Persistence:** members' chosen region is remembered (stored on the user
  record); visitors' choice lives in the session.
- Region NEVER filters existence — it filters *ordering and provider display
  only* (Doctrine §1–§2).

## 3 · The region door — `/beverages` (Q2, Q8)

**Nav label stays "Beverages." Interior language: "your cellar," lowercase.**

- Opens as the reader's own cellar: their region's producers and products
  first, the world one step away.
- **Category equality (push directive 2):** wine, spirits, beer & cider,
  coffee, tea, sake, fortified, non-alcoholic — equal shelves on the door,
  equal citizens of the pairing grammar and producer pages. A Vancouver
  roaster stands beside a Naramata grower.
- **The atlas:** one tap opens every other region's cellar —
  `/beverages/cellar/<region-slug>` (e.g. `/beverages/cellar/oregon`).
  A Tokyo reader can stand in British Columbia's cellar and look around;
  provider links inside a *visited* cellar still render for the READER's
  region (Pat's Rule is about the reader, not the room).
- Honest counts only (§1d of the kickoff): every number on the door uses the
  same published-only filters the shelves use.

## 4 · Producer pages (Q3, Q4 + push directives 1 & 3)

**Route:** `/beverages/producer/<slug>` (canonical; the raw-id route 301s to it).
**Template is producer-type aware:** grower, distiller, brewer, cidermaker,
roaster, tea garden, sake brewery — one template, type-tuned labels.

**Page holds:** name · region and country · type · the reputation narrative
(the story that sells at the table) · philosophy and practice · signature
products · importer lines (importer_us / uk / japan where present) ·
"carried in your region by …" provider block per Pat's Rule — or the honest
origin-only block per Doctrine §4.

**The publish gate (enforced everywhere, not just here):**
- A producer renders publicly **only if `is_published` is TRUE**.
- `is_published` may be TRUE only when: **`is_verified` TRUE + reputation
  narrative present + region set** (Q3).
- Enforcement lands in every producer-surfacing query (detail page, shelves,
  search, pairing cards). Unpublished → 404 for the public, visible to admin.
- **STAGE 3B PRIORITY ONE (founder-logged):** 429 unpublished producers are
  publicly reachable on live today by raw id. Gate enforcement closes that
  exposure first, before anything else ships.
- The founder has ALREADY vetted the 553 pass2 producers — no batch-by-batch
  re-review. The 108 missing reputation narratives are **composed in Stage 3b
  (step-down eligible)**; those producers cannot clear the bar until written.
  Publish flips in **one batch pass** once the gate is enforced and narratives
  are in.

## 5 · Product pages ("the bottle page" — also the bag, the tin)

**Route:** `/beverages/product/<slug>`.

**Free (Q6):** origin, plain description, the region story.
**Library:** the deductive profile (CMS-style for wine; SCA for coffee; BJCP
for beer; SSI for sake — per the Beverage Canon frameworks), the quality
ladder, full pairing reasoning.
**Profession:** the provider gold links — Pat's Rule live.
The frost falls exactly there, per the locked ladder. Frosted glass shows that
depth exists; it never apologises.

**The provider block — the doctrine rendered:**
- Provider(s) matching the reader's region → gold-underlined provider link(s),
  ORIGIN cited above them, always.
- **No provider in the reader's region → the honest rendering (Doctrine §4):**
  origin named in full, then plain confident copy — *"Not yet carried in
  British Columbia. It comes from [origin]. The cellar door is open — this
  page is how it gets here."* An invitation, never an apology. And the view
  is counted (§7).

## 6 · The pairing grammar (Q5)

- **Three confidence tiers restored** per the April 2026 architecture doc:
  `editorial` (founder-signed) · `reviewed` · `unverified`. Today's flat
  "partial" on all 534 rows **migrates to `unverified`** in Stage 3b; the
  founder's sign-off promotes to editorial.
- Rendering: editorial = full gold; reviewed = muted gold; unverified =
  admin/staging surfaces only. (Rendering weights per the architecture doc.)
- **The move is always named and reasoned**: Bridge (shared note) · Contrast
  (opposition) · Cut (cleanse) — with the why written out, sommelier register.
- **A suggestion MAY name a bottle with no local carrier** (Q5): it renders
  with the origin-only rules of Doctrine §4, and the click into that bottle's
  page fires the ledger like any other provider-absent view. The pairing
  grammar is a first-class source of demand signal.
- Non-alcoholic pours (tea, coffee, zero-proof) appear in every pairing set
  where genuine — category equality applies to the grammar itself.

## 7 · The demand ledger (Q7) — the gap is the signal

**New table (schema change — stop-point 2, built in 3b after approval):**

```sql
CREATE TABLE beverage_demand_ledger (
    id                  BIGSERIAL PRIMARY KEY,
    product_id          INTEGER REFERENCES beverage_products(id) ON DELETE SET NULL,
    producer_id         INTEGER REFERENCES beverage_producers(id) ON DELETE SET NULL,
    origin_region       TEXT,            -- producer's origin (region/country label)
    reader_region       TEXT NOT NULL,   -- province/state grain
    reader_city         TEXT,            -- when known; never required
    event_kind          TEXT NOT NULL CHECK (event_kind IN ('view','search')),
    search_terms        TEXT,            -- 'search' events only
    local_provider_absent BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- No user id. No session id. No IP. Region only — nothing else, ever.
```

**Firing points (server-side, both, all readers incl. anonymous):**
1. **`view`** — a product page renders and no `beverage_product_suppliers`
   row matches the reader's region → one row.
2. **`search`** — a cellar search returns results none of which have a local
   provider (or returns nothing local for a product-shaped query) → one row.

Write is fire-and-forget (never blocks or breaks the page). This ledger is a
foundational Trade-tier asset; aggregation views for Trade come later — in
this stage it only accumulates.

## 8 · The supplier onboarding path (push directive 1)

**The concrete route from a handshake to live gold links — one supplier in
one sitting.** Standing rule unchanged: **no business entity ships on a
public page unverified** (web-verified presence before anything renders).

**What the founder collects (one page of questions, on paper or phone):**
1. Business name, website, and public evidence (catalogue/storefront/licence)
2. Type: importer · distributor · retailer · producer-direct
3. Regions served (province/state tokens; multiple allowed)
4. Contact (internal only — never rendered)
5. Their carried list relevant to the canon (names, or their catalogue export)

**The wiring (admin surface — `/admin/beverages/onboard`):**
1. Create/select the supplier row (the Network's existing `suppliers` table —
   same table as the ingredient Network; a supplier can serve both worlds).
   Verification fields filled; unverified suppliers cannot be saved as
   renderable.
2. Paste their carried list → the tool fuzzy-matches against
   `beverage_products` (name + producer + region), founder confirms each
   match — misses are logged for later product creation, never guessed.
3. Confirmed matches insert `beverage_product_suppliers` rows
   (product · supplier · region availability · stocked/ordered-in note).
4. **Gold links are live for that region the moment the rows land.** The
   founder can show the supplier their own listing the same sitting.

Producer-direct onboarding (a distillery selling at the door) uses the same
path — the producer is both ORIGIN and their region's PROVIDER.

## 9 · Data loads (two-databases rule — every load names its target)

| # | Load | Target database | When |
|---|---|---|---|
| L1 | 553 pass2_pilot_v1 producer JSONs (founder-vetted) | **STAGING — provenance-staging-db** (`fly proxy 5435:5433`), `is_published=FALSE` on load | 3b, early |
| L2 | 108 reputation narratives composed (step-down eligible; Sashimi voice check on each) | STAGING first | 3b |
| L3 | Pairing tier migration: `partial` → `unverified` (534 rows) | STAGING first, live rides promotion | 3b |
| L4 | One-batch publish flip (gate rules satisfied) | STAGING first | 3b |
| L5 | Live load of all of the above | **LIVE — provenance-tester-1-db** — rides the Stage 3b promotion, on "push it live" only | 3b close |
| L6 | Supplier onboarding rows from the two-week push | LIVE (they are real, verified, and the founder wires them live in the sitting) — each block labeled THIS GOES TO: LIVE | during push |

## 10 · Stage 3b build order — sequenced for the two-week push (push directive 3)

**Week-one ships (everything a recruited contact can be shown):**
1. **Publish-gate enforcement** — closes the 429-producer exposure on live. Priority one.
2. **Producer pages presentable** — slug routes, mockup-2 design, category-equal.
3. **The supplier onboarding path** — admin surface + wiring, one sitting per supplier.

**Then:** 4. region model + region door rebuild · 5. L1–L2 loads + narratives
(step-down) · 6. pairing-tier migration + grammar rendering · 7. demand ledger
+ firing points · 8. cellar search · 9. product pages full depth ·
10. promotion to live per the Two-Site rules.

Model step-down recommendation (§5 of the kickoff): items 2, 5, and the
narrative composition are step-down eligible; items 1, 6, 7 stay at judgment
level.

## 11 · Gates, stops, and standards (unchanged, restated)

- Schema changes in §7 (+any migration in §9) are **stop-point 2** — named
  here, built only after this spec is approved.
- All 3b work: build on dev → walk on staging → queue for live; live moves on
  "push it live" only. Every deploy block opens with its THIS GOES TO: line.
- Sashimi Standard applies to every producer narrative, product entry, and
  pairing rationale — one compromised entry degrades the whole.
- Never fabricate a business, address, or price. Web search verifies before
  any real entity is named. (The mockups carry SAMPLE watermarks for exactly
  this reason.)

## 12 · Where the doctrine extends next (proving ground, not boundary)

The identical pattern — region grain, local-by-default rendering, honest
origin-only fallback, demand ledger — extends to **ingredients and the whole
Pantry**: `suppliers.service_region` already exists; the ingredient gold
links already render by region; a `pantry_demand_ledger` twin (or a
`domain` column on the same ledger) captures ingredient gaps. Not in this
stage. The beverage build is deliberately shaped so that extension is a
column, not a rewrite.

---

## The three mockups (Q9)

Delivered beside this spec, self-contained HTML, in `mockups/stage3a/`:
1. `1_region_door.html` — your cellar, category-equal shelves, the atlas
2. `2_producer_page.html` — a PNW roaster (category equality made visible),
   narrative, verified badge, provider block
3. `3_bottle_page.html` — pairing grammar with named moves + a region toggle
   showing the SAME product to a BC reader (gold provider link) and a Tokyo
   reader (origin-only honest rendering + the ledger counting the look)

**HARD STOP. Nothing in this document is built until the founder approves.**
