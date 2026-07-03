#!/usr/bin/env python3
"""
thin_entries_report.py — read-only audit of published technique_references
with fewer than 2 of the four left-page pillars populated, or
pillar_completeness count below 3.

Output: thin_entries_ledger.md grouped by canon, largest canon first.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    sys.exit("DATABASE_URL not set")

LEFT_PILLARS = ["origin", "description", "cross_cuisine_parallels", "flavour_context"]
PC_THRESHOLD = 3  # pillar_completeness count below this is thin


def count_left(row):
    return sum(1 for p in LEFT_PILLARS if row.get(p) not in (None, "", [], {}))


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            slug, name, canon_slug, section_slug,
            origin, description, cross_cuisine_parallels, flavour_context,
            pillar_completeness
        FROM technique_references
        WHERE published IS NOT FALSE
        ORDER BY canon_slug NULLS LAST, slug
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    thin = []
    for row in rows:
        row = dict(row)
        left_count = count_left(row)
        pc = row.get("pillar_completeness") or {}
        pc_count = int(pc.get("count", 0)) if isinstance(pc, dict) else 0
        if left_count < 2 or pc_count < PC_THRESHOLD:
            row["_left_count"] = left_count
            row["_pc_count"] = pc_count
            thin.append(row)

    # Group by canon_slug, order by group size desc
    from collections import defaultdict
    by_canon = defaultdict(list)
    for row in thin:
        by_canon[row["canon_slug"] or "_none"].append(row)

    canon_order = sorted(by_canon.keys(), key=lambda c: -len(by_canon[c]))

    lines = [
        "# Thin Entries Ledger\n",
        f"Entries with <2 left pillars populated OR pillar_completeness count <{PC_THRESHOLD}.\n",
        f"Total thin: {len(thin)} of {len(rows)} published.\n",
    ]

    for canon in canon_order:
        entries = by_canon[canon]
        label = canon if canon != "_none" else "(no canon)"
        lines.append(f"\n## {label} ({len(entries)} thin)\n")
        for e in entries:
            left_str = f"left={e['_left_count']}/4"
            pc_str = f"pc={e['_pc_count']}"
            slug = e["slug"] or "—"
            name = e["name"] or slug
            section = e["section_slug"] or ""
            section_str = f" [{section}]" if section else ""
            lines.append(f"- `{slug}`{section_str} — {name} ({left_str}, {pc_str})\n")

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "thin_entries_ledger.md",
    )
    with open(out_path, "w") as f:
        f.writelines(lines)

    print(f"Written: {out_path}")
    print(f"Total published: {len(rows)}")
    print(f"Total thin: {len(thin)}")
    for canon in canon_order[:8]:
        print(f"  {canon or '(no canon)'}: {len(by_canon[canon])}")
    if len(canon_order) > 8:
        print(f"  ... and {len(canon_order) - 8} more canons")


if __name__ == "__main__":
    main()
