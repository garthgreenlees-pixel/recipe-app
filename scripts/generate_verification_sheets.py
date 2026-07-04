#!/usr/bin/env python3
"""
Generate a canon-level verification sample sheet.

Usage:
    python3 scripts/generate_verification_sheets.py <canon_slug>

Reads from STAGING (DATABASE_URL_STAGING; falls back to DATABASE_URL with
5433→5434; falls back to DATABASE_URL as-is for local dev).

Produces ONE file: verification_sheets/<canon>_SAMPLE.md
  - 15 entries sampled to represent the canon
  - Spread across its sections (chapters), weighted toward most-cited source_books
  - Each entry: name, slug, origin / key temps+times / lives-or-dies pivot,
    with PASS/FAIL checkboxes
  - Single canon-level sign-off block at the foot; signing it marks the whole
    canon as sheet-verified for promote_canon.py gate-c

Also removes any legacy per-book sheets for this canon (files matching
<canon>_*.md that are NOT <canon>_SAMPLE.md) so the directory stays clean.
"""
import argparse
import json
import os
import random
import re
import sys
from collections import Counter

import psycopg2
import psycopg2.extras

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS_DIR = os.path.join(ROOT, "verification_sheets")
SAMPLE_SIZE = 15


def _load_env():
    env_path = os.path.join(ROOT, ".env")
    vals = {}
    try:
        for line in open(env_path).read().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                vals[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return vals


def _staging_dsn(env):
    explicit = os.environ.get("DATABASE_URL_STAGING") or env.get("DATABASE_URL_STAGING", "")
    if explicit:
        return explicit, "DATABASE_URL_STAGING"
    base = os.environ.get("DATABASE_URL") or env.get("DATABASE_URL", "")
    if ":5433/" in base:
        return re.sub(r":5433/", ":5434/", base), "DATABASE_URL (5433→5434)"
    return base, "DATABASE_URL (as-is)"


_TEMP_TIME_RE = re.compile(
    r"\b(\d+(?:\.\d+)?\s*(?:°\s*[CF]|degrees?\s*[CF]?|minutes?|mins?|hours?|hrs?|seconds?|secs?))\b",
    re.IGNORECASE,
)


def _extract_temps_times(fields):
    blob = " ".join(
        json.dumps(f) if isinstance(f, (dict, list)) else str(f)
        for f in fields
        if f is not None
    )
    return list(dict.fromkeys(_TEMP_TIME_RE.findall(blob)))[:6]


def _build_sample(entries, sections_meta, n, canon_slug):
    """
    Build an n-entry representative sample:
    - Restricted to entries that carry a source_book (physically verifiable)
    - Proportionally spread across sections, with remaining slots given to
      under-represented sections first (diversity)
    - Within each section, entries from the most-cited source_books are
      preferred; final pick is seeded-random within a top-K pool
    """
    sourced = [e for e in entries if e.get("source_book")]
    if not sourced:
        sourced = entries  # graceful fallback

    rng = random.Random(f"sample:{canon_slug}")
    source_counts = Counter(e.get("source_book", "") for e in sourced)

    by_section = {}
    for e in sourced:
        sec = e.get("section_slug") or "__none__"
        by_section.setdefault(sec, []).append(e)

    # Order sections by canonical display_order, then by entry count desc
    canon_order = {s["section_slug"]: s["display_order"] for s in sections_meta}
    section_keys = sorted(
        by_section.keys(),
        key=lambda s: (canon_order.get(s, 999), -len(by_section[s]), s),
    )

    total = len(sourced)

    # Floor-proportional allocation
    allocs = {sec: int(len(by_section[sec]) / total * n) for sec in section_keys}
    deficit = n - sum(allocs.values())

    # Distribute deficit: unrepresented (floor=0) sections first for breadth,
    # then by largest fractional remainder
    def _sort_key(s):
        frac = len(by_section[s]) / total * n - allocs[s]
        return (allocs[s] > 0, -frac)  # False < True so zeros come first

    for sec in sorted(section_keys, key=_sort_key):
        if deficit <= 0:
            break
        if allocs[sec] < len(by_section[sec]):
            allocs[sec] += 1
            deficit -= 1

    # Within each section: pool = top-(2×alloc, min 4) by source weight, then sample
    sample = []
    for sec in section_keys:
        alloc = allocs[sec]
        if alloc <= 0:
            continue
        sorted_sec = sorted(
            by_section[sec],
            key=lambda e: (-source_counts.get(e.get("source_book", ""), 0), e.get("slug", "")),
        )
        pool_size = min(len(sorted_sec), max(alloc * 2, 4))
        picked = rng.sample(sorted_sec[:pool_size], min(alloc, pool_size))
        sample.extend(picked)

    return sample[:n]


def _render_entry(entry):
    name = entry.get("name") or "(no name)"
    slug = entry.get("slug") or "(no slug)"
    section = entry.get("section_slug") or "—"
    source = entry.get("source_book") or "—"
    origin = (entry.get("origin") or "").strip()
    lives_or_dies = (entry.get("lives_or_dies") or "").strip()

    temps = _extract_temps_times([
        entry.get("description"),
        entry.get("key_principles"),
        entry.get("quality_hierarchy"),
        entry.get("sensory_tests"),
    ])

    lines = [
        f"### {name}",
        f"- **Slug:** `{slug}`",
        f"- **Chapter:** {section}",
        f"- **Source:** {source}",
        "",
        "**Checkable claims:**",
        "",
        f"- [ ] PASS / [ ] FAIL — **Origin:** {origin or '*(not recorded)*'}",
    ]

    if temps:
        for tt in temps:
            lines.append(f"- [ ] PASS / [ ] FAIL — **Temp/Time:** {tt}")
    else:
        lines.append(
            "- [ ] PASS / [ ] FAIL — **Temp/Time:** *(none detected — check manually)*"
        )

    lines.append(
        f"- [ ] PASS / [ ] FAIL — **Lives-or-dies pivot:** "
        f"{lives_or_dies or '*(not recorded)*'}"
    )
    return "\n".join(lines)


def _remove_legacy_sheets(canon_slug):
    """Delete old per-book sheets (<canon>_*.md that are not <canon>_SAMPLE.md)."""
    sample_name = f"{canon_slug}_SAMPLE.md"
    removed = 0
    try:
        for fname in os.listdir(SHEETS_DIR):
            if (
                fname.startswith(f"{canon_slug}_")
                and fname.endswith(".md")
                and fname != sample_name
            ):
                os.remove(os.path.join(SHEETS_DIR, fname))
                removed += 1
    except FileNotFoundError:
        pass
    return removed


def main():
    parser = argparse.ArgumentParser(
        description="Generate a canon-level verification sample sheet."
    )
    parser.add_argument("canon_slug", help="e.g. japanese")
    args = parser.parse_args()
    canon_slug = args.canon_slug

    env = _load_env()
    dsn, dsn_label = _staging_dsn(env)
    if not dsn:
        sys.exit("ERROR: No database URL. Set DATABASE_URL_STAGING or DATABASE_URL.")

    print(f"Connecting to staging via {dsn_label} …")
    try:
        conn = psycopg2.connect(dsn)
        conn.set_session(readonly=True)
    except Exception as exc:
        sys.exit(f"ERROR: Cannot connect to staging DB: {exc}")

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        """
        SELECT name, slug, section_slug, origin, lives_or_dies, source_book,
               description, key_principles, quality_hierarchy, sensory_tests
        FROM   technique_references
        WHERE  canon_slug = %s
          AND  published IS NOT FALSE
        ORDER  BY section_slug NULLS LAST, slug
        """,
        (canon_slug,),
    )
    all_entries = [dict(r) for r in cur.fetchall()]

    cur.execute(
        """
        SELECT section_slug, name AS section_name, display_order
        FROM   canon_sections
        WHERE  canon_slug = %s
        ORDER  BY display_order
        """,
        (canon_slug,),
    )
    sections_meta = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    if not all_entries:
        print(f"No published entries found for canon '{canon_slug}'. Nothing to generate.")
        sys.exit(0)

    sourced_count = sum(1 for e in all_entries if e.get("source_book"))
    print(f"  {len(all_entries)} total entries, {sourced_count} with a source_book stamp")

    sample = _build_sample(all_entries, sections_meta, SAMPLE_SIZE, canon_slug)

    # Sort by canonical section order, then slug
    sec_order = {s["section_slug"]: s["display_order"] for s in sections_meta}
    sample.sort(key=lambda e: (sec_order.get(e.get("section_slug"), 999), e.get("slug", "")))

    sections_covered = Counter(e.get("section_slug", "—") for e in sample)
    sources_covered = Counter(e.get("source_book", "—") for e in sample)

    os.makedirs(SHEETS_DIR, exist_ok=True)

    removed = _remove_legacy_sheets(canon_slug)
    if removed:
        print(f"  Removed {removed} legacy per-book sheet(s)")

    out_path = os.path.join(SHEETS_DIR, f"{canon_slug}_SAMPLE.md")

    header = [
        f"# Verification Sample Sheet — {canon_slug}",
        "",
        f"**Canon:** `{canon_slug}`  ",
        f"**Total entries:** {len(all_entries)} ({sourced_count} source-stamped)  ",
        f"**Sample:** {len(sample)} entries across "
        f"{len(sections_covered)} chapter(s), {len(sources_covered)} source(s)  ",
        "**Sampling method:** proportional by chapter, weighted toward most-cited "
        "sources, seeded for reproducibility  ",
        "",
        "---",
        "",
        "## Sample entries",
        "",
    ]

    entry_blocks = []
    for e in sample:
        entry_blocks.append(_render_entry(e))
        entry_blocks.append("")

    footer = [
        "---",
        "",
        "## Sign-off",
        "",
        "All entries above have been checked against physical copies of their source books.",
        "Complete each checkbox above, then sign below.",
        "**Signing this block marks the whole canon as sheet-verified for promotion.**",
        "",
        "**Sampled and verified against physical sources — "
        "operator: _______________, date: _______________**",
        "",
    ]

    with open(out_path, "w") as fh:
        fh.write("\n".join(header + entry_blocks + footer))

    print(f"  Wrote  {os.path.relpath(out_path, ROOT)}")
    print(f"  Covers {len(sections_covered)} chapter(s):")
    for sec, cnt in sorted(sections_covered.items(), key=lambda x: (x[0] is None, x[0] or "")):
        print(f"    {sec}: {cnt}")
    print(f"\nDone — {canon_slug}_SAMPLE.md generated.")


if __name__ == "__main__":
    main()
