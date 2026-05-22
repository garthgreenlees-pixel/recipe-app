#!/usr/bin/env python3
"""
Ingest Sprint 7D duplicate-candidate pairs into ingredient_duplicate_candidates.

Parses Sprint_7D_Duplicates_Review.md and inserts each (7C canonical, pre-existing)
pair using the IDs already embedded in the file headers. Idempotent — re-running
is safe due to ON CONFLICT DO NOTHING.

Usage:
    python3 scripts/ingest_sprint_7d_candidates.py
"""

import os
import re
import sys
import psycopg2

REVIEW_FILE = os.path.join(os.path.dirname(__file__), "..", "Sprint_7D_Duplicates_Review.md")

WRITE_URL = os.environ.get(
    "DATABASE_URL_WRITE",
    "postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW"
    "@localhost:5433/provenance_tester_1?sslmode=disable",
)

# Patterns
SECTION_RE = re.compile(r"^## .+\(7C id:\s*(\d+)\)")
PREEXISTING_RE = re.compile(r"\*\*Pre-existing id\s+(\d+):")


def parse_pairs(path):
    pairs = []
    current_7c_id = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = SECTION_RE.match(line.strip())
            if m:
                current_7c_id = int(m.group(1))
                continue
            m = PREEXISTING_RE.search(line)
            if m and current_7c_id is not None:
                pre_id = int(m.group(1))
                a, b = sorted([current_7c_id, pre_id])
                pairs.append((a, b))
    return pairs


def main():
    pairs = parse_pairs(REVIEW_FILE)
    print(f"Parsed {len(pairs)} candidate pairs from Sprint_7D_Duplicates_Review.md")

    conn = psycopg2.connect(WRITE_URL)
    cur = conn.cursor()

    # Verify all IDs exist in ingredient_master
    all_ids = set(id_ for pair in pairs for id_ in pair)
    cur.execute("SELECT id FROM ingredient_master WHERE id = ANY(%s)", (list(all_ids),))
    found_ids = {row[0] for row in cur.fetchall()}
    missing = all_ids - found_ids
    if missing:
        print(f"WARNING: {len(missing)} IDs not found in ingredient_master: {sorted(missing)}")

    inserted = 0
    skipped = 0
    unresolved = 0

    for a, b in pairs:
        if a in missing or b in missing:
            print(f"  SKIP (unresolved): pair ({a}, {b})")
            unresolved += 1
            continue
        cur.execute(
            """
            INSERT INTO ingredient_duplicate_candidates (master_id_a, master_id_b, source)
            VALUES (%s, %s, 'sprint_7d_audit')
            ON CONFLICT (master_id_a, master_id_b) DO NOTHING
            """,
            (a, b),
        )
        if cur.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"\nIngest complete:")
    print(f"  Inserted : {inserted}")
    print(f"  Skipped  : {skipped} (already present)")
    print(f"  Unresolved IDs : {unresolved} pairs had missing ingredient_master IDs")


if __name__ == "__main__":
    main()
