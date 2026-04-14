---
date: 2026-03-03
topic: beta-readiness
---

# Beta Readiness Audit

## What We're Building
Getting Provenance ready to share with chef friends as a beta test. Two goals: fix broken features, polish UI to look professional.

## Key Decisions
- Fix P0 blockers first (broken images, proxy loop, local dev path)
- Then P1 UI polish (serving text, empty state, button styling, mobile)
- Sample recipes should show gracefully without images rather than broken `<img>` tags
- Local dev and Fly.io should both work without code changes (env-based data path)

## Priority List

### P0 — Blocking
1. Sample recipe images missing → set `hasImage: false`
2. Image proxy self-loop on production → remove production fallback
3. Local dev data path `/data/` fails → env-based path with local fallback

### P1 — Rough Edges
4. "Serves 4 serve" awkward text
5. No empty state for grid
6. Import URL button inline styling + no gap
7. Hardcoded `lang !== 'ru'` filter
8. tsp/tbsp converting to ml in metric mode
9. No loading indicator on startup
10. Mobile header button overflow

### P2 — Polish
11. No favicon
12. Dead `loadPdfJs()` code
13. No error state for failed recipe fetch
14. `_method` field leaks into saved recipes

## Next Steps
→ Work through fixes in priority order
