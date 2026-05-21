#!/usr/bin/env python3
"""
scripts/seed_ingredient_aliases.py

Reads a cluster JSON file produced externally (e.g. by Claude Code reasoning)
and inserts aliases into ingredient_aliases.

Usage:
  python scripts/seed_ingredient_aliases.py apply \\
    --input proposed_clusters.json \\
    --min-confidence 0.85

Input JSON format:
  [
    {
      "category": "<category name>",
      "members": [
        {"id": <ingredient_master.id>, "name": "<canonical_name>"},
        ...
      ],
      "confidence": <0.0-1.0>,
      "reasoning": "<chef-supplier perspective on equivalence>"
    },
    ...
  ]

Primary selection: within each cluster, the member whose name has the most
active rows in ingredient_pricing wins. Tie-break: most recent effective_date.
Clusters where no member has any pricing rows are skipped — the bridge has
nothing to resolve to.
"""

import argparse
import json
import os
import sys
from datetime import date

import psycopg2
import psycopg2.extras


# ---------------------------------------------------------------------------
# DB connection
# ---------------------------------------------------------------------------

def get_write_conn():
    url = os.environ.get("DATABASE_URL_WRITE") or os.environ.get("DATABASE_URL")
    if not url:
        print("ERROR: DATABASE_URL_WRITE (or DATABASE_URL) must be set.", file=sys.stderr)
        sys.exit(1)
    return psycopg2.connect(url)


# ---------------------------------------------------------------------------
# Primary selection
# ---------------------------------------------------------------------------

def _pick_primary(cur, members):
    """
    Return (primary_member, stats_list).

    primary_member is the cluster member whose lower(ingredient_name) has the
    most active rows in ingredient_pricing. Tie-break: most recent
    effective_date. Returns (None, stats_list) if all members have row_count=0
    — the bridge would have nothing to resolve to.
    """
    stats = []
    for m in members:
        cur.execute(
            """
            SELECT COUNT(*) AS row_count,
                   MAX(effective_date) AS latest
            FROM ingredient_pricing
            WHERE lower(ingredient_name) = lower(%s)
              AND is_active = true
            """,
            (m["name"],),
        )
        row = cur.fetchone()
        stats.append(
            {
                "member": m,
                "row_count": row["row_count"] if row else 0,
                "latest": row["latest"] if row else None,
            }
        )

    if all(s["row_count"] == 0 for s in stats):
        return None, stats

    stats.sort(
        key=lambda s: (s["row_count"], s["latest"] or date.min),
        reverse=True,
    )
    return stats[0]["member"], stats


# ---------------------------------------------------------------------------
# apply subcommand
# ---------------------------------------------------------------------------

def cmd_apply(args):
    with open(args.input) as f:
        all_clusters = json.load(f)

    min_conf = args.min_confidence

    conn = get_write_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    processed = 0
    skipped_no_pricing = 0
    inserted = 0
    conflicts = 0

    for cluster in all_clusters:
        confidence = cluster.get("confidence", 0)
        if confidence < min_conf:
            continue

        members = cluster.get("members", [])
        if len(members) < 2:
            continue

        reasoning = cluster.get("reasoning", "")
        processed += 1

        primary, stats = _pick_primary(cur, members)
        if primary is None:
            skipped_no_pricing += 1
            names = ", ".join(m["name"] for m in members)
            print(f"  SKIP (no pricing): {names}")
            continue

        primary_id = primary["id"]
        primary_name_lower = primary["name"].lower()

        for m in members:
            if m["id"] == primary_id:
                continue
            if m["name"].lower() == primary_name_lower:
                continue

            cur.execute(
                """
                INSERT INTO ingredient_aliases
                    (ingredient_id, alias, source, confidence,
                     reasoning, approved_at, created_at)
                VALUES (%s, %s, 'ai_seed', %s, %s, NOW(), NOW())
                ON CONFLICT (alias_lower) DO NOTHING
                """,
                (
                    primary_id,
                    m["name"],
                    float(confidence),
                    reasoning,
                ),
            )
            if cur.rowcount == 1:
                inserted += 1
            else:
                conflicts += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"\nApply complete:")
    print(f"  Clusters processed (confidence >= {min_conf}): {processed}")
    print(f"  Clusters skipped (no pricing data for any member): {skipped_no_pricing}")
    print(f"  Aliases inserted (new rows): {inserted}")
    print(f"  Aliases skipped (alias_lower conflict): {conflicts}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Provenance ingredient alias seeder.\n"
            "Reads cluster JSON and inserts aliases into ingredient_aliases.\n\n"
            "Cluster JSON is produced by external reasoning (e.g. Claude Code),\n"
            "reviewed by a human, then fed to 'apply'."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_apply = sub.add_parser(
        "apply",
        help="Read cluster JSON and insert aliases into ingredient_aliases",
    )
    p_apply.add_argument(
        "--input", required=True,
        help="Path to the cluster JSON file",
    )
    p_apply.add_argument(
        "--min-confidence", type=float, default=0.85, dest="min_confidence",
        help="Minimum confidence threshold to apply (default: 0.85)",
    )

    args = parser.parse_args()

    if args.command == "apply":
        cmd_apply(args)


if __name__ == "__main__":
    main()
