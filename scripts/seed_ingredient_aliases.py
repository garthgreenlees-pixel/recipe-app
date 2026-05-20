#!/usr/bin/env python3
"""
scripts/seed_ingredient_aliases.py

Two subcommands:

  propose  -- Walk ingredient_master by category, call Haiku with a
              chef+supplier-perspective prompt, write cluster JSON.

  apply    -- Read cluster JSON, pick the primary per cluster by
              pricing row count, insert aliases via ON CONFLICT DO NOTHING.

Usage:
  python scripts/seed_ingredient_aliases.py propose \\
    --output proposed_clusters.json \\
    [--category "charcuterie_cured"]

  python scripts/seed_ingredient_aliases.py apply \\
    --input proposed_clusters.json \\
    --min-confidence 0.85
"""

import argparse
import json
import os
import sys
from datetime import date

import anthropic
import psycopg2
import psycopg2.extras


# ---------------------------------------------------------------------------
# DB connections
# ---------------------------------------------------------------------------

def get_read_conn():
    url = os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_URL_WRITE")
    if not url:
        print("ERROR: DATABASE_URL must be set.", file=sys.stderr)
        sys.exit(1)
    return psycopg2.connect(url)


def get_write_conn():
    url = os.environ.get("DATABASE_URL_WRITE") or os.environ.get("DATABASE_URL")
    if not url:
        print("ERROR: DATABASE_URL_WRITE must be set for writes.", file=sys.stderr)
        sys.exit(1)
    return psycopg2.connect(url)


# ---------------------------------------------------------------------------
# Haiku prompt (verbatim per spec)
# ---------------------------------------------------------------------------

_CHEF_SUPPLIER_PROMPT = """\
You are an executive chef AND a supplier representative with 20 years between \
the two roles. You are reviewing a culinary database's ingredient catalog, \
looking for clusters of entries that a working kitchen would treat as the same \
product for cooking purposes.

Critical operating principle: the invoice is the kitchen's reality. When a \
sous chef writes "parmesan" in a recipe but the kitchen has \
"Parmigiano Reggiano 72-Month DOP" on the invoice, that's the product the \
dish is actually made with. The catalog should bridge descriptive recipe \
language to the specific products the kitchen has in the pantry.

PERMISSIVE on cooking-equivalent variations:
  - Age grades: "Parmigiano Reggiano 24-Month" ↔ "Parmigiano Reggiano 36-Month" \
↔ "Parmigiano Reggiano 72-Month"
  - DOP / IGP / AOP / PDO designations: "Pecorino Romano" ↔ "Pecorino Romano DOP"
  - Origin descriptors when the product is cooking-equivalent: \
"Tellicherry Black Pepper" ↔ "Lampong Black Pepper" ↔ "Sarawak Black Pepper" \
(all whole peppercorn; origin matters at fine-dining altitude only)
  - Brand variations: "De Cecco Spaghetti" ↔ "Barilla Spaghetti" \
(brand doesn't change cooking)
  - Format / cut descriptors: "Pecorino Romano (wheel cut)" ↔ \
"Pecorino Romano (grated)" (same product, different cut)
  - Generic ↔ specific: "Parmesan" ↔ "Parmigiano Reggiano" \
(one is the chef's shorthand for the other)

STRICT on cooking-distinct ingredients that share a family but cook differently:
  - Pancetta ≠ Guanciale ≠ Lardo (different cured pork cuts, different cooking \
properties)
  - Parmigiano Reggiano ≠ Grana Padano (different cheeses, both aged Italian hard)
  - Pecorino Romano ≠ Pecorino Sardo ≠ Pecorino Toscano \
(different sheep cheeses, distinct profiles)
  - Arborio ≠ Carnaroli ≠ Vialone Nano (all risotto rice, but absorption \
properties differ enough to affect risotto)
  - Sweet ≠ Hot variants of the same spice (sweet Spanish paprika vs hot \
Spanish paprika)
  - Smoked ≠ unsmoked variants (cooking outcomes differ)

For each cluster you identify, output a JSON object:

  {
    "members": [
      {"id": <ingredient_master.id>, "name": "<canonical_name>"},
      ...
    ],
    "confidence": <0.0-1.0>,
    "reasoning": "<one or two sentences from the chef-supplier perspective on \
why these are equivalent>"
  }

Confidence calibration:
  - 0.95-1.00: Obvious cluster a chef would never question \
(DOP variants, age grades of the same cheese)
  - 0.80-0.94: Strong cluster with one or two edge cases worth flagging in \
the reasoning
  - 0.60-0.79: Plausible cluster but with cooking distinctions a chef might \
want to preserve — keep but flag in reasoning
  - Below 0.60: Don't output. Leave as separate entries.

Output format: a JSON array of cluster objects. Each cluster must contain at \
least 2 members. Singletons are not output. If the category has no clusters, \
return an empty array: [].

Output ONLY the JSON array. No prose preamble or explanation outside the JSON.\
"""


def _build_prompt(category, members):
    lines = []
    for m in members:
        parts = [f"id={m['id']}", f"name={m['canonical_name']!r}"]
        if m.get("origin_country"):
            parts.append(f"origin={m['origin_country']!r}")
        if m.get("origin_brand"):
            parts.append(f"brand={m['origin_brand']!r}")
        if m.get("base_unit"):
            parts.append(f"base_unit={m['base_unit']!r}")
        if m.get("description"):
            parts.append(f"desc={m['description'][:80]!r}")
        lines.append("  - " + ", ".join(parts))

    entries_block = "\n".join(lines)
    return (
        f"{_CHEF_SUPPLIER_PROMPT}\n\n"
        f"Category: {category}\n"
        f"Entries ({len(members)} total):\n{entries_block}"
    )


# ---------------------------------------------------------------------------
# propose subcommand
# ---------------------------------------------------------------------------

def cmd_propose(args):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY must be set.", file=sys.stderr)
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)

    conn = get_read_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if args.category:
        cur.execute(
            "SELECT DISTINCT category FROM ingredient_master WHERE category = %s",
            (args.category,),
        )
        categories = [r["category"] for r in cur.fetchall()]
        if not categories:
            print(
                f"ERROR: category {args.category!r} not found in ingredient_master.",
                file=sys.stderr,
            )
            cur.close(); conn.close()
            sys.exit(1)
    else:
        cur.execute(
            "SELECT DISTINCT category FROM ingredient_master ORDER BY category"
        )
        categories = [r["category"] for r in cur.fetchall()]

    all_clusters = []

    for category in categories:
        cur.execute(
            """
            SELECT id, canonical_name, base_unit, origin_country, origin_brand,
                   description
            FROM ingredient_master
            WHERE category = %s
            ORDER BY canonical_name
            """,
            (category,),
        )
        members = [dict(r) for r in cur.fetchall()]
        if len(members) < 2:
            print(
                f"[{category}] skipped — only {len(members)} entry, "
                "no clusters possible"
            )
            continue

        prompt = _build_prompt(category, members)
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as e:
            print(f"[{category}] ERROR calling Haiku: {e}", file=sys.stderr)
            continue

        raw = response.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        try:
            clusters = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"[{category}] ERROR parsing JSON: {e}", file=sys.stderr)
            print(f"  Raw (first 300 chars): {raw[:300]}", file=sys.stderr)
            continue

        if not isinstance(clusters, list):
            print(
                f"[{category}] ERROR: expected JSON array, got "
                f"{type(clusters).__name__}",
                file=sys.stderr,
            )
            continue

        for cluster in clusters:
            cluster["category"] = category
        all_clusters.extend(clusters)

        high   = sum(1 for c in clusters if c.get("confidence", 0) >= 0.95)
        medium = sum(1 for c in clusters if 0.80 <= c.get("confidence", 0) < 0.95)
        flagged = sum(1 for c in clusters if 0.60 <= c.get("confidence", 0) < 0.80)
        print(
            f"[{category}] sent {len(members)} members → "
            f"received {len(clusters)} clusters"
        )
        print(f"  high-conf (≥0.95): {high}")
        print(f"  medium-conf (0.80–0.94): {medium}")
        print(f"  flagged (0.60–0.79): {flagged}")

    cur.close()
    conn.close()

    with open(args.output, "w") as f:
        json.dump(all_clusters, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(all_clusters)} clusters to {args.output}")


# ---------------------------------------------------------------------------
# apply subcommand — primary selection
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
                    (ingredient_id, alias, alias_lower, source, confidence,
                     reasoning, approved_at, created_at)
                VALUES (%s, %s, %s, 'ai_seed', %s, %s, NOW(), NOW())
                ON CONFLICT (alias_lower) DO NOTHING
                """,
                (
                    primary_id,
                    m["name"],
                    m["name"].lower(),
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
            "Provenance ingredient alias seeder — chef+supplier perspective.\n"
            "Run 'propose' first, review the JSON, then run 'apply'."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_propose = sub.add_parser(
        "propose",
        help="Call Haiku per category and write cluster JSON to --output",
    )
    p_propose.add_argument(
        "--output", required=True,
        help="Path to write the proposed clusters JSON (e.g. proposed_clusters.json)",
    )
    p_propose.add_argument(
        "--category",
        help=(
            "Limit to a single category for a dry-run "
            "(e.g. 'charcuterie_cured'). Omit to run all categories."
        ),
    )

    p_apply = sub.add_parser(
        "apply",
        help="Read cluster JSON and insert aliases into ingredient_aliases",
    )
    p_apply.add_argument(
        "--input", required=True,
        help="Path to the proposed clusters JSON",
    )
    p_apply.add_argument(
        "--min-confidence", type=float, default=0.85, dest="min_confidence",
        help="Minimum confidence threshold to apply (default: 0.85)",
    )

    args = parser.parse_args()

    if args.command == "propose":
        cmd_propose(args)
    elif args.command == "apply":
        cmd_apply(args)


if __name__ == "__main__":
    main()
