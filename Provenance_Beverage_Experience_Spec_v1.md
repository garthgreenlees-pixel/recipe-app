# THE BEVERAGE EXPERIENCE — Stage 3a Specification v1.1
**Date:** 2026-07-05 · **Status:** AWAITING FOUNDER APPROVAL — nothing below is built until approved
**v1.1 amendments (founder corrections):** verification at scale via the graded
trust ladder (§8A) · the Suggest-a-Supplier button as platform doctrine (§8B) ·
the founder's push onboarding recast as the assisted lane on the same ladder (§8C)
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
    event_kind          TEXT NOT NULL CHECK (event_kind IN ('view','search','suggestion')),
    search_terms        TEXT,            -- 'search' events only
    local_provider_absent BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- No user id. No session id. No IP. Region only — nothing else, ever.
```

**Firing points (server-side, all readers incl. anonymous):**
1. **`view`** — a product page renders and no `beverage_product_suppliers`
   row matches the reader's region → one row.
2. **`search`** — a cellar search returns results none of which have a local
   provider (or returns nothing local for a product-shaped query) → one row.
3. **`suggestion`** — a reader submits the Suggest-a-Supplier form (§8B) →
   one row, region only. The suggestion's attribution lives in the
   suggestion queue table, never in the ledger — the ledger stays
   personal-data-free without exception.

Write is fire-and-forget (never blocks or breaks the page). This ledger is a
foundational Trade-tier asset; aggregation views for Trade come later — in
this stage it only accumulates.

## 8 · Verification at scale — one system, two doors in

**The method changes; the standard does not.** Founder hand-vetting was the
founding pass, not the operating model. Verification is system-work on a
graded trust ladder; founder attention is **exceptions-only** — the system
flags what fails or looks wrong, the founder rules on flags, never on the
queue at large. The hard line stands: **nothing renders as a provider
without passing the checks; nothing unverified ships on a public page, ever.**

### 8A · The trust ladder

| Rung | Public? | What it means |
|---|---|---|
| **SUGGESTED** | No — queue only | Exists only in the verification queue. Nothing renders anywhere. |
| **VERIFIED-LISTED** | Yes — as a *listing* (name · region · website) | The automated checks passed. No gold links, no product wiring — a listing, not a provider. No human required. |
| **VERIFIED PROVIDER** | Yes — **gold links live** | The business itself has claimed the listing via its own-domain email AND its carried products are wired into `beverage_product_suppliers`. This is the Pat's Rule tier. |

**The automated checks (VERIFIED-LISTED bar) — concretely:**
1. **Website liveness & identity** — the claimed domain answers over valid
   TLS; the site's own content names the business; domain registration age
   recorded (young domains are auto-flagged, not auto-failed).
2. **Contact at the business's own domain** — the contact email's domain
   matches the business domain and the domain accepts mail (MX present).
   Free-mail contacts (gmail etc.) never pass this check alone → flag.
3. **Region confirmed** — a published address, service area, or phone
   prefix on the business's own site (or registry record) consistent with
   the claimed province/state.
4. **Registry / address cross-check where available** — BC & federal
   corporate registries, US state lookups, and public liquor-licence
   registers for alcohol categories. "Where available" is honest: coverage
   varies by jurisdiction; absence of a registry match records as
   *unchecked*, not as *failed*.

**The claim step (VERIFIED PROVIDER bar):** a confirmation link sent to the
own-domain address; the click is the claim. Then product wiring per §8C
step 2–3. Both must hold before a single gold link renders.

**What the checks can and cannot catch — stated honestly:**
- They verify **existence, identity, and region**. They do NOT verify
  merit, stock reliability, or service quality — merit stays editorial,
  and the quality bar for being *featured* (rather than merely listed)
  remains an editorial act.
- They can be fooled by a live website for a dying business, a reseller
  overstating its service region, or a determined spoof on a lookalike
  domain. Mitigations: domain-age flags, exact-domain email matching,
  registry cross-checks — and every anomaly (check disagreement, young
  domain, licence mismatch, duplicate-looking business) goes to the
  **founder flag queue**. Flags are the only place founder time is spent.
- A VERIFIED PROVIDER later failing a re-check (dead site, bounced domain
  mail) is auto-demoted to VERIFIED-LISTED and flagged — gold links come
  down before anyone has to notice.

**Queue shape (schema change — stop-point 2, built in 3b after approval):**

```sql
CREATE TABLE supplier_verification_queue (
    id                  BIGSERIAL PRIMARY KEY,
    business_name       TEXT NOT NULL,
    website             TEXT,
    claimed_regions     TEXT[],          -- province/state tokens
    supplier_type       TEXT,            -- importer/distributor/retailer/producer-direct
    source              TEXT NOT NULL CHECK (source IN ('member_suggestion','founder_assisted','inbound')),
    suggested_by_user_id INTEGER,        -- attribution lives HERE, never in the ledger
    context_product_id  INTEGER,         -- the page the suggestion came from, if any
    context_producer_id INTEGER,
    note                TEXT,
    status              TEXT NOT NULL DEFAULT 'suggested'
                        CHECK (status IN ('suggested','checks_running','verified_listed',
                                          'claim_pending','verified_provider','flagged','rejected')),
    check_results       JSONB DEFAULT '{}'::jsonb,   -- per-check pass/fail/unchecked + evidence URLs
    flag_reason         TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at         TIMESTAMPTZ
);
```

Rungs map onto the Network's `suppliers` table via a `verification_status`
column (same three values); renderers read the rung, nothing else.

### 8B · The Suggest-a-Supplier button — platform doctrine, not a footnote

**Placement:** every product page and every producer page — and **most
prominently on every origin-only rendering**, where it is the page's call
to action: *"Not yet carried in your region — know who should carry it?
Suggest a supplier."*

**Flow — one tap, four fields at most:** business name · region (prefilled
with the reader's region) · website · optional note. Nothing else asked.

**Every suggestion, on submit:**
1. Enters the verification queue at SUGGESTED (`source='member_suggestion'`,
   context product/producer recorded);
2. Fires a demand-ledger `suggestion` event (region only — §7);
3. Is attributed to the suggesting member in the QUEUE row (anonymous
   readers may still suggest; their rows simply carry no attribution).

**The close of the loop:** when a suggestion becomes a live listing, the
suggesting member is told — a note from Provenance, in the house voice:
their cellar got deeper because of them.

**The pipeline:** the suggestion queue doubles as a Trade-tier sales
pipeline — every suggested supplier is a pre-qualified lead for the
platform to onboard. **This stage captures and verifies. Outreach
automation is later work** — named here so nobody builds it early.

### 8C · The assisted lane — the founder's push onboarding (push directive 1)

The push path from v1 remains in full, recast as **the assisted lane on the
same ladder**: what the founder collects in one sitting simply completes
the VERIFIED PROVIDER checks in person. One system, two doors in — the
rungs and the bar are identical whichever door a supplier walks through.

**What the founder collects (one page, on paper or phone):**
1. Business name, website, and public evidence (catalogue/storefront/licence)
2. Type: importer · distributor · retailer · producer-direct
3. Regions served (province/state tokens; multiple allowed)
4. Contact at the business's own domain (internal only — never rendered)
5. Their carried list relevant to the canon (names, or a catalogue export)

**The wiring (admin surface — `/admin/beverages/onboard`):**
1. Create/select the supplier row (the Network's `suppliers` table — one
   table serves beverage and ingredient worlds). The §8A checklist renders
   inline; the founder confirms each check with evidence in hand —
   `source='founder_assisted'`, results recorded in `check_results` the
   same as the automated path. The claim step can complete on the spot
   (they open the confirmation mail at the table).
2. Paste their carried list → fuzzy-match against `beverage_products`
   (name + producer + region), founder confirms each match — misses are
   logged for later product creation, never guessed.
3. Confirmed matches insert `beverage_product_suppliers` rows
   (product · supplier · region availability · stocked/ordered-in note).
4. **Gold links live for that region the moment the rows land** — the
   supplier sees their own listing before the sitting ends.

Producer-direct onboarding (a distillery selling at the door) uses the same
lane — the producer is both ORIGIN and their region's PROVIDER.

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
+ firing points · 8. **the Suggest-a-Supplier button + verification queue and
automated checks (§8A/§8B)** — the button ships with the pages that carry it;
until the automated checks land, submissions queue as SUGGESTED and wait ·
9. cellar search · 10. product pages full depth · 11. promotion to live per
the Two-Site rules.

Note on the assisted lane: it does NOT wait for item 8 — the week-one
onboarding surface (item 3) records the §8A checklist manually, so the
founder's push runs from day one on the same ladder.

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
