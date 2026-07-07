# MyKitchen — COMPLETE Build Manifest (full history, build-ordered)
**Deadline: tomorrow night. Confirm in one pass; I build straight through.**

This replaces the homepage-only draft. It is the whole MyKitchen surface as
promised across the design files AND Sprints 6/7/11 — reconciled against what
is ALREADY BUILT in code, so every line has a real starting point.

Status legend: ✅ **BUILT** (exists in code, may need surfacing) · ⚠️ **DEBT**
(flagged deferred in a sprint) · 🔨 **ABSENT** (net-new) · 🌾 **GRIND** (content).

The big reconciliation: MyKitchen already has a deep engine. Cook mode, step
timers, costing, HACCP notes, ingredient scaling, the recipe toolbar — all
shipped. They live on `recipe.html` + `cook_mode.html`, not yet joined to the
new dark homepage. So most of "finish" is JOIN + close real gaps + clear debts.

---

## A. HOMEPAGE SURFACE (the dark MyKitchen shell)

| Item | Status | Where / note |
|------|--------|--------------|
| Dark hero, search, Add-a-recipe dropdown | ✅ | shipped last cycle |
| Add-a-recipe → URL/Scan/PDF/Write flows | ✅ | `/api/import-url`, `/api/scan`, `/api/classify-pages`, `/api/recipes/new` |
| Recipe card → **Recipe Card.dc.html spec** | 🔨 | monogram header, status badge "State · N of 7", cuisine eyebrow, tags, title, meta "time · Serves N", **blue Sourced dot**. Replaces generic card on the shelf |
| Sourced stat + per-card sourced flag | ✅data | derive from `ingredient_origin_markers` via `_get_kitchen_recipe_suppliers_from_markers` (server.py:7060) |
| Collections stat + **coloured-spine shelf** | 🔨 | RULED BUILD — new tables + CRUD (§C) |
| Cooked-this-week stat | 🔨 | RULED BUILD — via cook-mode tracking (§C) |
| Enhanced / Drafts substitute stats | ✅ | RULED KEEP as honest substitutes |
| Chip row: Recently-added / states / cuisines / Vegetarian | ✅ | created_at + tags back these |
| Course chips (Mains/Baking/Sides) | ◐ | no `course` field → inferred from tags/title, honestly |
| Menus → folder + count + "Next up" row | ✅data | `menus`/`menu_recipes`, counts derived (server.py:1568) |
| Migrate panel + "Bring your whole library" | 🔨 | RULED REAL — panel ships wired to existing add paths NOW; bulk parse §D |
| Load-more, footer "One standard, no exceptions", Evening theme | 🔨 | homepage polish |
| Grind shelf-note render slot (published only) | 🌾 | table live on staging; render slot wired |

## B. THE RECIPE + COOK SURFACES (mostly built — join + finish)

| Item | Status | Where / note |
|------|--------|--------------|
| Cook mode (full-screen, wakelock/keep-awake) | ✅ | `/recipe/<slug>/cook`, `cook_mode.html` |
| Step **timers** (countdown, start/pause/reset, alarm) | ✅ | `cook_mode.html:185-198,1337-1380`; `format_timer` (server.py:147) |
| **Step-duration parsing → populate `timer_seconds`** | 🔨 | timers exist but `timer_seconds` is never filled from step text — the real timer gap |
| **Ingredient checkboxes / mise-en-place** in cook mode | 🔨 | design shows them (Cook Mode.dc.html:30-39); ABSENT in code |
| Structured ingredient rows (qty/unit/item/group) | ✅ | `recipe.html:735-776`; `_parse_ingredients_text` |
| Ingredient **scaling** (serves ±) | ✅ | `recipe.html:714-719,1148-1154` |
| Write-from-scratch **structured per-row inputs** | ⚠️ | V4 debt (`V4_Sprint_Checklist.md:161`) |
| Recipe **costing** (per-serve, food-cost %, menu price) | ✅ | `_compute_recipe_cost` (server.py:1852), `/api/costing/...`, Profession-gated |
| **Costing surface joined to MyKitchen** (cost in card/hero) | ⚠️ | shipped 6.5 then not on new shell — resurface |
| Recipe toolbar (Cook/Save/Print/Share/Edit/HACCP/Notes/Cost/Scale) | ✅ | `recipe.html:695-705,1058-1076` |
| Kitchen notes (user annotations) + HACCP cards | ✅ | `recipe_annotations`, `recipe_kitchen_notes_cache` |
| **Kitchen-notes LEGAL BOUNDARY / food-safety disclaimer** | 🔨 | COMPLIANCE_ROADMAP.md:8,21 — PRE-LAUNCH requirement, currently NOT displayed. The "legal boundary" the founder means |
| Toolbar **Group / Filter dropdowns + filter pills** | ⚠️ | Sprint 6/7 debt (`V4_Sprint_Checklist.md:160-161`) |
| Add-to-menu button on recipe | 🔨 | ABSENT |
| Recipe PDF export UI (endpoint exists, unwired) | ⚠️ | `/api/export-pdf` (server.py:9143) unused for recipes |
| Shopping list / cross-recipe aggregation | 🔨 | ABSENT — scope decision (in/out for launch?) |

## C. NET-NEW (ruled to build)

- **Collections** 🔨 — `user_collections` + `collection_recipes`, CRUD, coloured-spine shelf, "+ New collection", add-to-collection from any card, Collections stat.
- **Cook-log / Cooked-this-week** 🔨 — `recipe_cook_log`; the cook-mode "Finish" logs a cook event; stat counts last-7-days.
- **Bulk migrate importer** 🔨 — parsers for Paprika/Mela/CSV/JSON behind the dropzone, each recipe → `/api/recipes` canon pipeline; AnyList/NYT via CSV.

## D. CARRIED DEBTS (clear or explicitly park)

- ⚠️ "The Table" → MyKitchen nav rename (`_header.html`) — quick.
- ⚠️ `/enhance` dead stub cleanup (server.py:11284) — quick.
- ⚠️ Quality-Hierarchy legacy data migration (pre-Q11 recipes) — script.
- ⚠️ Menu Builder full / enhance.html / allergen auto-detect / member-verified + composed card states — park with one-line reason unless you say otherwise.

---

## BUILD ORDER — aggressive cycles, one walk each

**CYCLE 1 (tonight):** Homepage fidelity — Recipe Card to spec + Sourced stat/dot
+ migrate panel wired to existing paths + Recently-added/course chips + footer +
Evening toggle + grind render slot. **Walk 1.**

**CYCLE 2 (tomorrow AM):** Collections (tables+CRUD+spine shelf) + Menus folder/Next-up
+ cook-log with cook-mode "Finish" → Cooked-this-week. Stats 5,7 go real. **Walk 2.**

**CYCLE 3 (tomorrow PM):** The recipe/cook debts — step-duration→timer_seconds,
mise-en-place checkboxes, toolbar Group/Filter+pills, add-to-menu, costing
resurfaced, **the food-safety legal boundary**, write-from-scratch structured rows.
**Walk 3.**

**CYCLE 4 (tomorrow PM/eve):** Bulk importer parsers behind the dropzone. **Walk 4.**

**PROMOTION (tomorrow night):** package, staging walked, live on your word.

## BLOCKERS (one line each — clear early)
- **B1** `ANTHROPIC_API_KEY` on staging → walk real imports (else fixture).
- **B2** one real Paprika/Mela/CSV export each → prove bulk parse on Walk 4.
- **B3** grind note = shared canon narrative, published-gated (built). Confirm/redirect.
- **B4** Shopping list — IN or OUT for this deadline? (one word)
- **B5** Legal-boundary wording — I'll draft a food-safety disclaimer; you approve the exact text before it ships public.
