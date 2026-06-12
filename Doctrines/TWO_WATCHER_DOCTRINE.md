# THE PROVENANCE TWO-WATCHER DOCTRINE

**Version 1.0 — April 19, 2026**
**Durable rule. Save to `~/Desktop/Provenance/Doctrines/` for reuse across all future sessions.**

---

## Purpose

Provenance uses two distinct watcher architectures. They serve different jobs, run on different cadences, and exist at different layers of the stack. Never conflated. If any Claude session, human, or document refers to "watchers" without specifying which of the two, the default is to ask once and clarify, then proceed.

---

## Watcher One — The Operational Watcher

**What it watches:** the extraction pipeline's operational health.

**What it catches:** stalled terminals, proxy drops, silent partial writes, foreign-key orphans, NULL-citation writes, `sashimi_validated=false` rows, repeated error patterns, connection refused, HTTP errors, token-limit exceptions.

**How it works:** two small Python scripts (`db_state_watcher.py` and `log_tail_watcher.py`) running as macOS `launchd` daemons. Polls the production database every 15 minutes and tails the extractor log in real time. Writes to `WATCHER_REPORT.md` and `WATCHER_ALERTS.md`.

**AI involvement:** none. Pure SQL plus pattern-matching Python. Free to run.

**Phase:** deploy first. Must run clean for 24 hours before the content watcher deploys.

**Setup cost:** ~10 minutes in Claude Code.

**Runtime cost:** zero tokens.

---

## Watcher Two — The Content Watcher

**What it watches:** the quality and voice of entries the extractor produces.

**What it catches:** voice drift, banned-word regressions, missing pillars, Sashimi Standard structural failures, temperature-unit failures, species-precision failures, depth-of-content failures that regex validators cannot detect.

**How it works:** `content_watcher.py` running as a `launchd` daemon on an hourly schedule. Reads the five most-recently-written `technique_references` rows, sends them to Haiku 4.5 with the Sashimi Standard specification plus the Lexicon, receives a PASS / MINOR FLAG / MAJOR FLAG evaluation, writes to `WATCHER_CONTENT_REPORT.md`. More than one MAJOR FLAG in an hour escalates to `WATCHER_ALERTS.md`.

**AI involvement:** yes. Haiku 4.5 (cheap, fast, sufficient).

**Phase:** deploy second. Only after operational watcher has reported clean for 24 hours, so content watcher is never evaluating entries from a silently-stalled extractor.

**Setup cost:** ~15 minutes in Claude Code.

**Runtime cost:** ~$0.25 to $1.00 per day. Budget $30 per month.

---

## When a Request References "Watchers" or "Watcher Methodology"

The request is ambiguous by default. The correct response is to ask ONE clarifying question:

> "Do you mean the operational watcher (pipeline health) or the content watcher (entry quality)?"

Then proceed with the specified phase.

---

## Never Conflate These With

- **"Extraction with live validation"** (the Sashimi validator — a different thing, enforced at the commit layer inside the extraction script itself, NOT a separate watcher)
- **"Autonomous batch extraction from source corpus"** (the extractor's own run mode, NOT a watcher)
- **"Library cleanup sweep"** (a retrospective quality pass, distinct from watchers that monitor ongoing extraction)

---

## Phasing Discipline

- **Phase 1** = Operational Watcher. Deploy first. Free. Always on.
- **Phase 2** = Content Watcher. Deploy after Phase 1 is clean for 24hr. Cheap. Always on.
- **Phase 3** = Active-Veto Staging Watcher. Deferred. Only if Phase 1+2 prove insufficient.
- **Phase 4** = Multi-Watcher Orchestrator. Deferred until post-launch scale requires it.

**Amendment 1 — 2026-06-11 (founder-approved, Halfmoon Bay):**
Operator-present supervision of a first run substitutes for the
24-hour unattended clean window. The 24-hour window remains the rule
for any unattended deploy. Context: the original window assumed the
operator was leaving the machine unattended; with the operator
physically present and monitoring, a supervised first run provides
equivalent or better assurance.

---

## Rule for Any Future Session

If the operator asks about watchers, assume the request is Phase 1 or Phase 2 unless stated otherwise. If Phase 1 is not yet deployed, build Phase 1 first regardless of what was asked for. **The operational floor comes before the content ceiling.**

---

**END DOCTRINE.**
