# Provenance — Master Build Plan V4 Sprint Checklist

**Source:** `Provenance_Master_Build_Plan_V4_Audit.md` (15 May 2026)
**Purpose:** Living checklist. Tick items as they ship. Reference at session kickoffs to confirm scope before any work begins.
**Sprint numbering:** V4 sprints (Sprint 2 onward). V3 Sprint 1 has shipped. V3 item numbers preserved in brackets for cross-reference.

---

## V4 Doctrines (read before every sprint)

1. **Edit, never rewrite.** Surgical edits to wireframe-pattern HTML, never full replacements.
2. **Wireframe is the target.** Every item references which wireframe panel it builds toward. If a panel is queued without a wireframe, that wireframe is its own deliverable.
3. **Logic survives layout.** Auth gates, error handling, null guards, routing decisions carry into new templates. V4 specs note where these inherit so they're never re-implemented or dropped.

---

# Phase I — Logic and Foundations (~3 weeks)

*Backend, data, components that every surface rebuild will consume.*

## V4 Sprint 2 — Wireframe Drafting Block (~1–2 weeks)

*Design work, not code. Output: HTML wireframe files in the Foundation pattern. Four wireframes needed to clear the "saleable product" Stage 2 gate.*

- [ ] `/pricing` wireframe drafted
- [ ] `/kitchen` wireframe drafted
- [ ] `/recipe/<slug>` wireframe drafted
- [ ] `/auth/account` wireframe drafted

## V4 Sprint 3 — Working Kitchen Reliability (~5–6 days)

*V3 Sprint 3 verbatim. Runs early because document-idle bugs may be blocking audit tools needed for later rebuilds.*

- [ ] [3.1] Session lifetime extended
- [ ] [3.2] Auth redirect preserves URL
- [ ] [3.3] Document-idle root cause investigation
- [ ] [3.4] Document-idle fix
- [ ] [3.5] Lighthouse re-baseline

## V4 Sprint 4 — Logic Foundations (~7–8 days)

*The components and gates every surface rebuild consumes.*

- [ ] [2.1] Component-level tier-gating helper
- [ ] [2.2] Tier-aware upgrade-prompt component
- [ ] [2.3] HACCP Plan tool gated
- [ ] [2.4] Cost This Recipe tool gated
- [ ] [2.5] Named-producer beverage pairings gated
- [ ] [2.6] Quality Hierarchy gated to Library
- [ ] [4.2] Unified header component built to wireframe nav spec
- [ ] [4.5] MyKitchen product-name canonical rendering (cross-cut copy pass)
- [ ] [7.1] `/api/stats` endpoint — replace hardcoded counts
- [ ] [7.5] Stat Inconsistency Matrix resolved (falls out of 7.1 — read from `/api/stats` everywhere)

---

# Phase II — Surface Migration to Wireframe (~12–14 weeks)

*Each sprint is a single-surface rebuild to a locked wireframe. Wireframes for each surface drafted at sprint kickoff unless already done in Sprint 2.*

## V4 Sprint 5 — Homepage Migration (~5 days)

*Foundation wireframe already locked — no drafting cost.*

- [ ] Homepage rebuilt to Foundation wireframe
- [ ] [4.1] Four Doors persona block (Cook / Sommelier / Chef / Supplier) absorbed
- [ ] [7.6] Homepage metadata + OG absorbed
- [ ] [7.7] Primary nav reshape (The Canon · The Atlases · The Routes · The Table) absorbed
- [ ] [7.8] CTA architecture (three CTAs of escalating commitment) absorbed
- [ ] Stats band rendering against `/api/stats`

## V4 Sprint 6 — MyKitchen + Recipe Detail Migration (~10–12 days)

*Two surfaces ship together — they share too much template logic to separate.*

- [ ] `/kitchen` rebuilt to its wireframe (uses Recipe Card Template for card grid)
- [ ] `/recipe/<slug>` rebuilt to its wireframe (full seven-pillar display per Recipe Card Template)
- [ ] [4.4] "My Kitchen" eyebrow dropped on cards
- [ ] [5.8] Seven pillars on recipe page (Pillars III–VII added: Quality Hierarchy, Sensory Tests, Cross-Cuisine Parallels, Beverage Pairings, Origin & Lineage)
- [ ] [6.8] Card teaser rendered as italic span inside title (no new schema column)
- [ ] [7.3] Beverage pairing template — role-labelled list + producer-named card, with Pat's Rule (origin_producer + local_provider) on every pairing
- [ ] [7.4] Pat's Rule discipline pass on ingredients
- [ ] [7.10] Global header on recipe page

## V4 Sprint 7 — Cook Mode Build — FULLY CLOSED 2026-05-27

- [x] `/recipe/<slug>/cook` wireframe drafted — Cycle 2
- [x] [2.11] Semantic `<ol>` method rendering — Cycle 3 / commit `49e0cf7`
- [x] [2.11] Step navigation — Cycle 4 / commit `5130964`
- [x] [2.11] Tappable timers — Cycle 11 / commit `567e2c5` + audio alarm Cycle 11.5 / commit `c535d76`
- [x] [2.11] Wake-lock indicator — V3 baseline preserved
- [x] [2.11] Scale propagation across all panels — Cycle 10 (Serves ± stepper)
- [x] [2.11] Tool integration — Cycles 5, 6, 9, 9.5
- [x] [2.11] Ingredient-line bugfix — Cycle 3 / commit `f79a384`

## V4 Sprint 8 — Menu Builder Build (~10 days, includes 2 days wireframe drafting)

- [ ] `/menu-builder` wireframe drafted
- [ ] [2.12] Recipe selection grid
- [ ] [2.12] Cross-recipe allergen matrix (Hidden HACCP doctrine)
- [ ] [2.12] Food-cost aggregation panel
- [ ] [2.12] Exports
- [ ] [2.12] Tier gating

## V4 Sprint 9 — Generative Surfaces (~7 days, includes 1–2 days wireframe drafting)

- [ ] `/atelier` (Compose Menu) wireframe drafted
- [ ] `/compose` (Compose Recipe) wireframe drafted
- [ ] [2.7–2.10] `/atelier` rebuilt — brief input → composed-menu output, Reserve-gated
- [ ] [2.7–2.10] `/compose` rebuilt — brief input → composed-recipe output, Reserve-gated
- [ ] Consistent "Compose" verb across both surfaces

### 🟢 Stage 2 / Pre-Launch gate reachable after Sprint 9 + Data parallel reaching minimum thresholds

## V4 Sprint 10 — Spine Surfaces (~3 weeks, includes ~1 week wireframe drafting)

*The PMT walking surface is the highest-leverage build — Phaidon book, dinner series, founding partner all converge there.*

- [ ] `/canon` wireframe drafted
- [ ] `/explorer` wireframe drafted
- [ ] `/route` index wireframe drafted
- [ ] `/route/pacific-migration-trail` wireframe drafted (the big one)
- [ ] `/cuisines` redesigned wireframe drafted
- [ ] `/protocols` wireframe drafted
- [ ] [5.1] `/canon` built (typed index by Regional / Route / Method / Meta)
- [ ] [5.2] `/explorer` built (regrouped by canon type)
- [ ] [5.3] `/route` index built (the five Spice Routes)
- [ ] [5.4] `/route/pacific-migration-trail` built (walking surface)
- [ ] [6.4] `/cuisines` redesigned (curated ~50–80 named canons with regional/route/method/meta typing)
- [ ] [5.6] `/protocols` built (Library-gated walking surface)

## Canon Audit + Tightening Pass — queued after Sprint 10

*Pre-requisite: Sprint 10 complete.*

Once Sprint 10 has established the canon structure / spine, audit every existing technique entry against the new structure. Score against the seven Sashimi pillars. Identify entries at full standard, entries needing expansion, entries to cut. Tighten the rescuable. Mark exemplars. Resolve /why/ and /beyond/ doctrinal home (specific pillar subsets or formal retirement of the routes).

- [ ] Row-level pillar audit (0–7 score per entry)
- [ ] Full-standard entries marked as exemplars
- [ ] Expansion candidates identified and queued
- [ ] Cut candidates flagged for operator decision
- [ ] /why/ and /beyond/ doctrinal fate resolved

## V4 Sprint 11 — Pricing + Auxiliary Surfaces (~2 weeks)

- [ ] `/pricing` wireframe drafted (if not in Sprint 2)
- [ ] `/suppliers` wireframe drafted
- [ ] `/recipes` (browse) wireframe drafted
- [ ] [4.6] `/pricing` member-aware
- [ ] [5.7] "Three Spice Routes complete" copy correction absorbed into `/pricing`
- [ ] [5.9] "Programme builder" vs Menu Builder clarification absorbed into `/pricing`
- [ ] [4.7] Trade tier surfaced on `/auth/account`
- [ ] `/auth/account` rebuilt (leave action wired through Sprint 1's 1.9/1.10 once they ship)
- [ ] [6.3] Founding-partner editorial placement on `/suppliers`
- [ ] [6.9] Geographic tag normalisation on `/suppliers`
- [ ] [7.2] Three-filter system on `/recipes` (Cuisine / Section / Facet)
- [ ] [7.11–7.23] Session D modal polish items folded in (modal cleanup, suggest-supplier polish)
- [ ] `/enhance` full retirement — Sprint 7 carry-in (deferred 2026-05-27)
- [ ] `/kitchen` toolbar Group/Filter dropdowns + filter pills row — Sprint 7 carry-in (deferred 2026-05-27)
- [ ] Write-from-scratch structured per-row ingredient inputs — Sprint 7 carry-in (deferred 2026-05-27)

### 🟢 Stage 3 / Public Launch gate reachable after Sprint 11

---

# Phase III — Data Parallel Track (runs alongside Phase II from Sprint 4 onward)

## V4 Sprint 12 — Data Integrity & Canon Tagging (multi-week, parallel)

- [ ] [6.1] `product_suppliers` backfill for supplier ID 19
- [ ] [6.2] `/suppliers` count query reads from join (no more hardcoded counts)
- [ ] [6.5] General-bucket canon tagging — 6,431 entries
- [ ] [6.6] African canons surfaced on `/recipes` cuisine filter (gated by 6.5)
- [ ] [6.7] Spice Routes as first-class canons on `/explorer` (gated by 6.5 + 5.4/5.5)
- [ ] [7.24] Beverage extraction sprint (ongoing, parallel)

---

## V4 Sprint 12B — International Expansion Hook (parallel track, Japan first)

Pre-launch international SEO probe. One discoverable Japanese-language landing page linked to seed canon entries. Inbound JP traffic is the cue to invest in full localization. Reusable template for France, Italy, Mexico, Australia, SE Asia when each region's turn comes.

Full strategy: `~/Desktop/Provenance/International/Provenance_International_Expansion_Strategy_v1_2026-05-27.md`

### Cycle JP-A — Discoverable page (engineering, 1–2 cycles)

- [ ] Add route `/ja` with Japanese landing page template
- [ ] Noto Sans JP + Shippori Mincho font loading
- [ ] `<html lang="ja">`, hreflang alternates (ja/en/x-default), schema.org `inLanguage: "ja"`, JP Open Graph
- [ ] Sitemap entry for `/ja` with hreflang alternate
- [ ] Submit Google Search Console JP property

### Cycle JP-B — Seed canon entries (data work, ongoing)

- [ ] Write 5–10 canonical Japanese technique entries in Sashimi Standard format
- [ ] Link from `/ja` landing page
- [ ] Source authority: Tsuji's *Japanese Cooking: A Simple Art* (already in canon source list)

Seed targets: 出汁の引き方 (dashi), 刺身, 寿司酢, 天ぷら衣, 蕎麦打ち, 出汁巻き玉子, 茶碗蒸し, 焼き鳥, すき焼き, 懐石料理.

### Cycle JP-C — Localization data schema (engineering, 1 cycle)

- [ ] Create `food_safety_authorities` table — keyed by `(country_code, region_code)`
- [ ] Create `allergen_set` table — keyed by `country_code`
- [ ] Seed Japan rows: Kyoto City Medical Health Center (4 branches: 北東部 075-746-7211, 中部 075-746-7212, 南東部 075-746-7213, 西部 075-746-7214), 8 mandatory allergens (特定原材料: えび, かに, くるみ, 小麦, そば, 卵, 乳, 落花生) + 20 recommended, 食品衛生責任者 role
- [ ] Codex Alimentarius generic fallback row

### Cycle JP-D — HACCP brief localization (engineering, 1 cycle)

- [ ] Modify `build_haccp_system_prompt()` to read from `food_safety_authorities` + `allergen_set` based on recipe origin region or chef operating region
- [ ] Brief renders 食品衛生責任者 sign-off line, Japan allergen pills, JP authority footer when target region = Japan

### Trigger gates beyond JP-D

- [ ] Monitor JP traffic via Google Analytics on `/ja` page
- [ ] Threshold: 500 unique JP visitors/month sustained for 3 months
- [ ] If hit → kickoff full Japanese platform translation (new sprint, estimated post-Stage 3)
- [ ] If not hit after 6 months → reassess (different region first? different content on /ja?)
- [ ] At 100+ JP chef signups → consider partnership with 京都市食品衛生協会 or 公益社団法人京都府食品衛生協会 for endorsement

**Decisions recorded:**

- **Discoverable-page-first is now Provenance doctrine for international expansion.** Applies to France, Italy, Mexico, Australia, SE Asia. Each region adds one landing page route, 5–10 seed canon entries, one `food_safety_authorities` row, one `allergen_set` mapping. No platform engineering changes per region — only data.
- **HACCP regulatory framework localization is the differentiator vs existing operational HACCP software** (FoodDocs, FoodReady, Jolt, Safefood 360°, etc.). They sell daily monitoring; Provenance generates the regulatory brief from the recipe technique itself. Closest real competitor is the UK food safety consultant charging £2,000–8,000 per bespoke HACCP plan.

**To close:** Cycles JP-A → JP-D are the buildable scope. Trigger gates beyond JP-D wait on real traffic data. No prerequisite on other sprints — can run in parallel with Sprint 8 onward.

---

## V4 Sprint 13 — Remaining Route Walking Surfaces (~2 days each, one per fortnight)

*Uses PMT wireframe as template — each is a fast templated build.*

- [ ] WADT (West African Diaspora Trail) walking surface
- [ ] PCT (Phoenician Coastal Trail) walking surface
- [ ] Trans-Saharan walking surface
- [ ] Indian Ocean walking surface

---

# Phase IV — Voice and Polish (~2 weeks)

## V4 Sprint 14 — Voice and Polish Pass

- [ ] [4.8] Heading hierarchy targeted pass on surfaces NOT rebuilt
- [ ] [7.9] Cuisine label normalisation (Title Case, no slugs)
- [ ] `/about` copy + heading pass
- [ ] `/for-professionals` copy + heading pass
- [ ] `/techniques/browse` copy + heading pass
- [ ] `/beverages` copy + heading pass
- [ ] `/drinks` copy + heading pass
- [ ] Cross-cut voice cleanup
- [ ] Branded 404 (pending from Sprint 1 deferrals)

---

# Parallel / Out-of-Main-Path

## V3 Sprint 0.5 — International Launch Architecture

*Pure backend, "invisible until launch markets commit." CARRY verbatim. Decision pending on when to land.*

- [ ] CARRY verbatim (land before V4 begins, OR parallel during Sprints 3–6, OR defer until V4 complete)

## V3 Sprint 8 — Editor Surface

*Post-launch infrastructure. Out of V4 main path; runs once Stage 3 lands.*

- [ ] CARRY verbatim (ships after Stage 3 / Public Launch gate)

---

# Wireframe Drafting Queue (priority order)

*Reference list of all surfaces requiring wireframes before code rebuilds can start. The four asterisked are the "saleable product" Stage 2 minimum set drafted in V4 Sprint 2.*

1. `*/pricing` *
2. `/kitchen` (MyKitchen home) *
3. `/recipe/<slug>` (detail) *
4. `/auth/account` *
5. `/recipe/<slug>/cook` (Cook Mode)
6. `/menu-builder`
7. `/atelier` (Compose Menu)
8. `/compose` (Compose Recipe)
9. `/suppliers`
10. `/canon`
11. `/explorer`
12. `/route` (index)
13. `/route/pacific-migration-trail`
14. `/cuisines` (redesigned)
15. `/protocols`
16. `/recipes` (browse)
17. `/recipe/<slug>/edit`
18. Three import modals (Scan / Import unified / Write from scratch)

Plus smaller: branded 404 · `/suggest-supplier` (minor polish) · `/about` + `/for-professionals` (likely copy + heading pass, no full rebuild)

---

# Open Doctrine Questions

*These need answers — not checkboxes. Resolve before the relevant sprint starts.*

1. **Wireframe drafting in-chat vs separate design pass?** Recommendation: Option C (Sprint 2 drafts the 4 Stage 2 wireframes; remaining drafted at start of their own sprint).
2. **V3 Sprint 0.5 (International Launch Architecture) — when?** Depends on Japan/France launch timeline confidence. If 12–24 months firm: parallel during Sprints 3–6. If unclear: defer until V4 main path complete.
3. **V3 item 5.8 — confirm doctrine option?** Recommendation: Option A (ship the remaining three pillars so "Full seven-pillar depth" pricing promise becomes true, baked into Sprint 6).
4. **`/cuisines` redesign scope?** Recommendation: keep ~50–80 named canons with regional/route/method/meta typing, drop the rest of the 9,291.
5. **Sprint 6 sub-ordering?** Recommendation: `/kitchen` and `/recipe` ship together — too much shared template logic to separate.
6. **Recipe Card "five states" timing?** Recommendation: Sprint 6 ships imported / enhanced / canon. Composed lands when Sprint 9 ships. Member is post-launch.

---

# Critical-Path Timing Estimate

| Phase | Sprints | Weeks |
|---|---|---|
| I — Logic & Foundations | 2, 3, 4 | ~3 weeks |
| II — Surface Migration | 5, 6, 7, 8, 9, 10, 11 | ~12–14 weeks |
| III — Data parallel | 12, 13 | runs alongside; doesn't add to critical path |
| IV — Polish | 14 | ~2 weeks |
| **Critical-path total** | | **~17–19 weeks** |

Structural wins over V3: no template gets fixed then rebuilt; Stage 2 gate reachable earlier in surface migration (after Sprint 9 + data thresholds).

---

# Out-of-Plan Work Log

*Track any work shipped outside the V4 plan — including the cycle that surfaced its existence. Use this to catch drift early.*

- [x] **Cross-Language Pricing Cycle (2026-05-21)** — 135-entry cross-language ingredient catalog seeded, alias-retry bridge code shipped to tester, duplicate-master pattern discovered. Chef-facing REAL/CHILD/NOISE duplicate resolution UX is the carry-forward and needs deliberate slotting into V4 Sprint 11 (`/pricing` rebuild) rather than auto-numbered as Sprint 8.
- [x] **SEO Recovery — Sprint 14 parked line item (closed 2026-05-28)** — Closed via Cycle 2 (Googlebot 403 fix, commit `c7dec25`) and Cycle 3b (canonical tags + sitemap exclusion on /why/ and /beyond/). Cycle 1 diagnosed the scrape-tracker 403 storm; Cycle 2 shipped three-state DNS classifier; Cycle 3a confirmed /why/ and /beyond/ are same-row content (64–68% token overlap with /technique/); Cycle 3b added rel="canonical" pointing both surfaces at /technique/ master and removed /why/ and /beyond/ from sitemap.xml.

---

*Living document. Update as sprints close. Pair with the wireframe queue at every kickoff — no code work begins on a surface whose wireframe hasn't been drafted.*
