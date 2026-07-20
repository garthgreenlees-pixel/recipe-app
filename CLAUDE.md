# PROVENANCE — STANDING RULES (CLAUDE.md)
1. Authoritative documents are locked: SASHIMI_STANDARD.md, Recipe Card Template, all wireframes, Foundation Principles, Brand Voice & Lexicon, Printable Doctrine, Master Build Plan V4 Audit, V4 Sprint Checklist (the score — it wins over chat), most recent Sprint Closing Handoff, every "Locked"/"Canonical" marker. Apply them; never relitigate.
2. When conversation contradicts a locked document, apply the document and flag the conflict.
3. No options when doctrine exists. State the answer.
4. Layman's English in all operator-facing output. Dev-speak stays in code and commits.
5. One question at a time, only when documents can't answer it.
6. Voice rules: never "AI" in user-facing content; never "non-negotiable" (use "where the dish lives or dies"); never "Sign out" (use "Leave"); MyKitchen one word title case; HACCP stays HACCP.
7. Pillar orders are locked. RECIPES: Ingredients, Method, Quality Hierarchy, Sensory Tests, Cross-Cuisine Parallels, Beverage Pairings, Origin & Lineage. TECHNIQUES: Origin, Description, Thread, Flavour Context, Quality Hierarchy, Sensory Tests, Where the Dish Lives or Dies.
8. Tier gates locked: Kitchen $49, Library $149, Profession $299, Trade $999 per the Sashimi Standard.
9. Pat's Rule: every ingredient and beverage shows origin producer + local provider, region-filtered.
10. Never fabricate business entities. Verify by web search before naming any real supplier or brand.
11. Never touch the public recipes table without explicit confirmation. "My collection" = user_kitchen_recipes scoped to user_id = 1.
12. Sprint pattern: discovery cycle first, surgical edits, one commit per cycle by named file (never git add .), deploy at end.
13. Nothing is shipped until the operator smoke-walks the live URL. Tests passing is not shipped.
14. Two-Site safety: staging (provenance-staging.fly.dev) is always the default target. Every deploy block names its destination at the top. Production (provenance.kitchen) moves only on the explicit words "push it live."
15. Every factual claim in a report carries an evidence line: the command run and its actual output. No evidence, no claim.
16. Cycle reports: write with a cat heredoc to ~/provenance-tester-1/last_cycle_report.md AND publish to the staging reports endpoint so the report reaches https://provenance-staging.fly.dev/images/reports/cycle_report_latest.txt.
