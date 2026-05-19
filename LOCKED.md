# LOCKED.md

## Purpose
This file lists every Provenance component, pipeline, schema element, and architectural decision that is verified to work and is not to be modified without explicit approval from Garth.

The goal: stop rebuilding things that already work. When a fix is needed near a locked component, port or extend the existing component — don't rewrite it. When a fix is needed inside a locked component, surface the proposed change here for approval first.

This file replaces tribal memory. Anything not here is either WIP or hasn't been formally locked yet.

## How to use this file

Before writing code for any Provenance task:
1. Read this file end to end.
2. Identify whether the work touches any locked component.
3. If yes — propose the change in the chat first. State which lock you'd be modifying, why, and what the impact is. Wait for explicit approval before editing the locked file or feature.
4. If no — proceed normally, but if your work creates a new component that should be locked once it's verified, add it to the "Pending lock review" section below for promotion later.

If a locked component appears broken on a live page, the lock isn't wrong — the data feeding it might be. Investigate the data layer before assuming the locked code is at fault. (Example: paste 22 Sourced section is locked, but a recipe with no ingredient-product matches will correctly render an empty section. That's the lock working, not failing.)

## Status legend

- **LOCKED** — verified working on production, not to be modified.
- **PARTIAL** — works in most paths, known gaps documented; modifications must preserve the working paths.
- **WIP** — under active development, not yet eligible for locking.

---

## Locked components

### Recipe page UI (kitchen-import template)

Location: `templates/user_kitchen_recipe.html`

| Component | Status | Notes |
|---|---|---|
| Top action bar (Cook / Edit / Publish or Pending review / bookmark / share / print) | LOCKED | Paste 7. Edit currently routes to `/recipe/<slug>/edit` — modal upgrade is paste 18 (WIP). |
| Eyebrow + title (Georgia) + subtitle | LOCKED | Standard hero. |
| Tradition tags row | LOCKED | Paste 1. Renders on every import that has tags populated. |
| Sashimi pull-quote position (above meta strip) | LOCKED | Paste 1. Visual styling (italic + gold rules) is paste 17 (WIP). |
| Meta strip — yield + active + total | LOCKED | Pastes 7, 12, 19, 20. Yield handles ranges and plural correctly post-paste 19. |
| Personal origin block | PARTIAL | Renders correctly. Multi-paragraph trim with "Read more →" is paste 16 (WIP). |
| ORIGIN & PROVENANCE auto-context | LOCKED | Auto-generates on import. |
| Provenance Audit panel | LOCKED (passive) | Detection works and surfaces flags. Active fix proposals are paste 25 (WIP). |
| Quality Hierarchy section | LOCKED | Auto-generates on import. |
| Sensory Tests section | LOCKED | Auto-generates on import. |
| Cross-cuisine Parallels (collapsed accordion) | LOCKED | Paste 4. |
| Sourced By Provenance — Pat's Rule two-tier | LOCKED | Paste 22. "The benchmark" (ORIGIN, region-agnostic) + "Find it locally" (PROVIDER, T1 region-filtered). Persistent invite bar (paste 28) renders at accordion bottom regardless of supplier count. |
| TO DRINK pairings section | LOCKED | Paste 24. Three constraints enforced: one non-alcoholic floor, category diversity (no two alike), specific named drinks with real producers. COMPLEMENT / BRIDGE / CONTRAST tier eyebrows. Null-slot fallback to "→ pairing not yet matched" renders cleanly. Provider attachment to bottle shops awaits Perry's data. |
| QUESTIONS / FAQ accordion | LOCKED | Pastes 9 + 20. |
| Action buttons row (HACCP / Kitchen notes / Cost this recipe / Scale recipe) | LOCKED | Each opens its respective modal. |
| Notes panel with "Your kitchen, your hand" tagline | LOCKED | Per-step Notes via gold dot click. |
| Bio block (collapsed row) | PARTIAL | Renders. Click-expand is paste 17 (WIP). |
| M/I metric/imperial toggle | LOCKED | Paste 5. `.r-unit-toggle`. |
| Method — Arabic numerals, gold dots, no ★ | PARTIAL | Step-level ★ removed (paste 11). Section heading ★ removal is paste 17 (WIP). |
| Hero image rendering | LOCKED | Standard hero block. |

### Modals

| Modal | Status | Location |
|---|---|---|
| HACCP plan modal | LOCKED | Existing v3 modal. Reused on kitchen-import via the action button row. |
| Kitchen notes modal | LOCKED | Existing v3 modal. Reused on kitchen-import via the action button row. |
| Cost this recipe v3 modal (3 tabs: Cost / Invoices / Pricing) | LOCKED | Paste 15. Ported from v3 demos to kitchen-import. Partial-cost banner, supplier+price column, total + per-portion calculated from real prices only. |
| ProvenanceProcessing overlay (breathing wordmark + 3 rotating italic sentences) | LOCKED | `static/css/processing_overlay.css`. Pattern: `ProvenanceProcessing.show({messages:[...]})` at start, `.hide()` in `finally{}`. Wired to HACCP, Kitchen notes, and import-time enrichment. |

### Backend endpoints & pipelines

Location: `server.py`

| Endpoint / Pipeline | Status | Notes |
|---|---|---|
| `GET /api/costing/recipe/<slug>` | LOCKED | Paste 2. Lookup falls through to `user_kitchen_recipes` for user_id=1. Returns actual_food_cost_pct, breakdown[], cost_warning_message. |
| `POST /api/recipe/submit-for-review` | LOCKED | Paste 14. Creates `recipe_submissions` row, sends email to `EDITORIAL_REVIEW_EMAIL`. |
| Always-run enrichment on import (beverage pairings + active/total times + FAQs) | LOCKED | Paste 20. Three subroutines run in parallel via ThreadPoolExecutor at the end of `create_recipe()`. Beverage pairings rewritten in paste 24 to use LLM with three hard constraints. |
| `_enrich_beverage_pairings()` | LOCKED | Paste 24. LLM (Haiku) generates 3 pairings with post-validation: non-alcoholic floor + category diversity + specific named drinks. Re-prompts once on failure; nulls bad slots on second failure. |
| `POST /api/recipe/<slug>/re-enrich-pairings` | LOCKED | Paste 24. Founder/admin only. Re-runs pairing enrichment for an existing kitchen recipe; writes result to `beverage_pairings` JSONB. |
| Yield text normalizer (ranges and plural) | LOCKED | Paste 19. |
| `_get_kitchen_recipe_suppliers_from_markers()` + `_supplier_in_region()` | LOCKED | Paste 22 + paste 29 + paste 32. Reads pre-resolved `ingredient_origin_markers` JSONB (set at import time) instead of fuzzy-matching at render time. Pantry stop list filters noise ingredients ("salt", "water"). Stem-on-stem substring filter removes false-positive products (watermelon when recipe has manuka honey). One DB query for role + service_region only. T1 region filter (paste 22). ~~Pastes 30, 30a (SQL regex — silently threw in production) and paste 31 (ILIKE fuzzy match) superseded by paste 32.~~ |
| Sashimi Pipeline (Quality Hierarchy + Sensory Tests + Cross-cuisine Parallels + ORIGIN & PROVENANCE auto-context + Sourced base query) | LOCKED | Pre-existing. Runs on every import. |
| `backfill_enrichments.py` | LOCKED | Paste 20 backfill script. Run with `DATABASE_URL` + `DATABASE_URL_WRITE` env vars. Supports `--dry-run`, `--limit N`, `--force`. |
| `GET /suggest-supplier` + `POST /suggest-supplier` | LOCKED | Paste 28. Form page + submission handler. Emails garth.greenlees@gmail.com via Resend. `reply_to` set to chef_email if provided. Always logs submission even if email fails. |

### Database schema

| Table / Column | Status | Notes |
|---|---|---|
| `user_kitchen_recipes` (hash-suffixed slug pattern) | LOCKED | Recipe storage for user_id=1. |
| `recipe_submissions` (id, recipe_id, status, reviewed_at, reviewer_notes, approved_destination) | LOCKED | Paste 14. |
| `product_suppliers.role` (ORIGIN | PROVIDER) | LOCKED | Verified clean 2026-05-08: 0 NULL roles, 554 ORIGIN, 2639 PROVIDER. |
| `product_suppliers.region` | PARTIAL | 104 of 3193 rows have empty region; T1 filter falls back to `s.service_region`. Working as designed. |
| `suppliers.service_region` (with `Western_Canada` umbrella support) | LOCKED | Used by T1 filter. |
| `recipes.beverage_pairings` JSONB | LOCKED | Paste 20. |
| `recipes.faqs` JSONB | LOCKED | Paste 20. |
| `recipes.active_time_minutes`, `recipes.total_time_minutes` | LOCKED | Paste 20. |
| `recipes.enrichment_locked` JSONB | LOCKED | Per-field locks. Flip a key to `true` to protect a field from re-enrichment. Used by Edit flow. |

### Reference files

| File | Status | Notes |
|---|---|---|
| `provenance_recipe_card_duck.html` | REFERENCE | Canonical design source for the four sections (Sourced, Notes, Beverage pairing, Actions). Lives in Garth's Downloads; should be copied into `designs/` for codebase access. |

---

## Locked architecture decisions

| Decision | Notes |
|---|---|
| **Truth or zero costing** | No fabricated prices. Real prices come from manual entry, invoice ingestion (Claude Vision), or supplier pricelist ingestion. Each carries provenance (source, document, date). |
| **Pat's Rule** | Origin tier = cited benchmark, region-agnostic, role='ORIGIN' in product_suppliers. Provider tier = verified-partner local, T1 region-filtered, role='PROVIDER'. |
| **Always-run enrichment on import** | Beverage pairings, active/total times, FAQs auto-generate for every new import. Users edit out via Edit; locked fields aren't overwritten. |
| **Editorial review by email** | Publish doesn't auto-publish. Submission lands in `EDITORIAL_REVIEW_EMAIL`. Garth assigns rules and destination tier outside the system. |
| **No fabricating retailers, suppliers, or business entities** | Web search to verify before listing. Empty state ("provider not yet matched", "request one →") is the honest state. |
| **HACCP terminology unchanged** | Regulated term. Stays on buttons, panel titles, PDFs. The May 6 ruling reverses the April 3 rename. |
| **Brand voice rules** | Six protected words (Library, Pantry, Method, Thread, Brief, Network). Banned phrases including "non-negotiable" → "where the dish lives or dies." Never say "AI" in user-facing copy. Sentence-case body. Larousse / Ducasse register. Paste 21 enforces this in auto-generated content (WIP). |
| **T1 region filter for Provider tier** | State match OR explicit region in service_region OR `Western_Canada` umbrella for BC/AB/SK/MB. |
| **Python filtering, not SQL gymnastics** | Filtering decisions inside `_get_kitchen_recipe_suppliers` happen in Python because the result set is small (≤20 products → bounded result) and Python handles the empty-region fallback cleanly. |
| **Provenance recipes table is read-only by default** | Never touch the public `recipes` table without explicit approval. "My collection" defaults to `user_kitchen_recipes` scoped to user_id=1. Public recipe edits/deletes always require explicit confirmation. |

---

## Locked process rules

| Rule | Why |
|---|---|
| **Search past chats / read this file before proposing a fix** | Stops drift into rebuilding what works. |
| **Port what exists, don't rebuild** | The recipe card design files, v3 demo templates, and existing modals are the canonical sources. New work ports from them. |
| **Read Garth's words literally** | "Nothing happens" means nothing visual. Don't reinterpret. |
| **One change per cycle. No bundling.** | Ship a paste, verify on the live URL, decide what's next. |
| **State top-level goal at session start** | Prevents work expanding outside the goal. |
| **End-of-session list: shipped / blocked / next** | Hand-off discipline. |
| **Live on production (provenance.kitchen), never on tester** | Tester drift has cost real time. |
| **No fabricating user content** | Garth picks the recipes, performs the imports. Claude observes. |
| **Live URL test, not mockups** | Mockups have produced wrong information and wild goose chases. |
| **Navy SEAL standard of attention to detail** | When a source document exists, extract every item line by line. Verify: "Is there ANY item in this source NOT in my output?" |

---

## Pending — not yet locked

These ship next. Each promotes to LOCKED once verified on the live URL.

- Paste 16 — Personal origin trim (collapse multi-paragraph stories to first paragraph + "Read more →")
- Paste 17 — Sashimi italic Georgia + gold rules; remove ★ from method section heading; bio click-expand wiring
- Paste 18 — Edit modal with hero image swap + 5 core text fields (Title / Subtitle / Tradition tags / Sashimi line / Personal origin)
- Paste 21 — Brand voice enforcement in auto-generated content (banned phrases, six protected words, post-validation pass)
- ~~Paste 23 — Sourced section empty-state — superseded by paste 28 persistent invite bar (LOCKED 2026-05-09).~~
- Paste 25 — Audit becomes invisible hand (AI proposals on flagged issues with Accept / Reject / Edit, applied via Edit pipeline)
## Pending lock review

Components that may belong in LOCKED but haven't been verified across enough recipes to formally promote:

- Brand voice enforcement (paste 21) — once shipped and one full import cycle confirms no banned phrases appear in auto-generated content, promote.
- ~~Beverage pairing constraints (paste 24) — PROMOTED TO LOCKED 2026-05-09.~~
- ~~Suggest-a-supplier invite bar + form (paste 28) — PROMOTED TO LOCKED 2026-05-09.~~
- Audit invisible hand (paste 25) — needs separate review process given scope.

---

## How to add a lock

When something new ships and is verified to work on the live URL across at least two different recipes:

1. Add the component to the appropriate "Locked components" subsection above with status LOCKED.
2. Note the paste number, the file location(s), and one-line description.
3. If the new lock supersedes a previous one (e.g. paste 22 superseded the original Sourced section), strike through the old entry rather than deleting — keeps the history visible.
4. Commit this file as part of the same change. The lock and the working code travel together.

## Recommended companion practice — git tags

After every batch of paste shipments, tag the commit:
