#!/usr/bin/env python3
"""
Cycle 7C: Seed cross-language ingredient catalog.

Parses Sprint_7_Catalog_Seed_List.md and populates:
  - ingredient_master  (canonical English names)
  - ingredient_aliases (foreign trade-name aliases + canonical self-pointer)

Usage:
  venv/bin/python3 seed_cross_language_catalog.py --target=tester
  venv/bin/python3 seed_cross_language_catalog.py --target=production
"""
import os, re, sys, argparse
from pathlib import Path

# ── .env loader ──────────────────────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

import psycopg2, psycopg2.extras


# ── YAML block parser (no external deps) ─────────────────────────────────

def _parse_block(block: str) -> dict | None:
    """Parse one YAML block from the seed list. Returns {canonical, aliases} or None."""
    entry = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # Top-level list item with canonical key
        m = re.match(r'^[-\s]*canonical:\s*(.+)$', line)
        if m:
            entry["canonical"] = m.group(1).strip()
            i += 1
            continue
        # aliases: block
        if re.match(r'^\s+aliases:\s*$', line):
            aliases = []
            i += 1
            while i < len(lines):
                am = re.match(r'^\s+-\s+(.+)$', lines[i])
                if am:
                    aliases.append(am.group(1).strip())
                    i += 1
                else:
                    break
            entry["aliases"] = aliases
            continue
        i += 1
    if "canonical" in entry and "aliases" in entry:
        return entry
    return None


def parse_seed_file(md_path: Path) -> list[dict]:
    text = md_path.read_text()
    raw_blocks = re.findall(r"```yaml(.*?)```", text, re.DOTALL)
    entries = []
    for raw in raw_blocks:
        raw = raw.strip()
        if not raw or "canonical:" not in raw:
            continue
        entry = _parse_block(raw)
        if entry:
            entries.append(entry)
        else:
            print(f"WARN: skipped unparseable block starting: {raw[:60]!r}")
    return entries


# ── DB helpers ────────────────────────────────────────────────────────────

def get_connection(target: str):
    if target == "tester":
        url = os.environ.get("DATABASE_URL_WRITE")
        if not url:
            sys.exit("ERROR: DATABASE_URL_WRITE not set")
    elif target == "production":
        url = os.environ.get("PROD_DATABASE_URL") or os.environ.get("DATABASE_URL_WRITE")
        if not url:
            sys.exit("ERROR: PROD_DATABASE_URL not set")
        if not os.environ.get("PROD_DATABASE_URL"):
            print("NOTE: PROD_DATABASE_URL not set — using DATABASE_URL_WRITE (same DB)")
    else:
        sys.exit(f"ERROR: unknown target '{target}'")
    conn = psycopg2.connect(url)
    conn.autocommit = False
    return conn


def seed_entry(cur, entry: dict) -> dict:
    """Seed one canonical entry + all its aliases. Returns per-entry counts."""
    canonical = entry["canonical"].strip()
    aliases = [str(a).strip() for a in entry.get("aliases", []) if str(a).strip()]

    # ── 1. Upsert ingredient_master ───────────────────────────────────────
    cur.execute("""
        INSERT INTO ingredient_master (canonical_name)
        VALUES (%s)
        ON CONFLICT (lower(canonical_name)) DO UPDATE
          SET canonical_name = EXCLUDED.canonical_name
        RETURNING id, (xmax = 0) AS was_inserted
    """, (canonical,))
    row = cur.fetchone()
    master_id = row["id"]
    master_was_inserted = bool(row["was_inserted"])

    # ── 2. Canonical self-alias (source='canonical') ──────────────────────
    cur.execute("""
        INSERT INTO ingredient_aliases (alias, ingredient_id, source)
        VALUES (%s, %s, 'canonical')
        ON CONFLICT (alias_lower) DO NOTHING
    """, (canonical, master_id))

    # ── 3. Foreign aliases (source='ai_seed') with NULL rescue ───────────
    ai_inserted = 0
    ai_rescued = 0
    ai_skipped = 0

    for alias in aliases:
        cur.execute("""
            INSERT INTO ingredient_aliases (alias, ingredient_id, source)
            VALUES (%s, %s, 'ai_seed')
            ON CONFLICT (alias_lower) DO UPDATE
              SET ingredient_id = EXCLUDED.ingredient_id,
                  source        = EXCLUDED.source
              WHERE ingredient_aliases.ingredient_id IS NULL
            RETURNING id, (xmax = 0) AS was_inserted
        """, (alias, master_id))
        result = cur.fetchone()
        if result is None:
            # Conflict, WHERE was false → row already linked to a (possibly different) master
            ai_skipped += 1
        elif result["was_inserted"]:
            ai_inserted += 1
        else:
            # Conflict, WHERE was true → was NULL-linked, now rescued
            ai_rescued += 1

    return {
        "master_was_inserted": master_was_inserted,
        "ai_inserted":         ai_inserted,
        "ai_rescued":          ai_rescued,
        "ai_skipped":          ai_skipped,
    }


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, choices=["tester", "production"])
    args = ap.parse_args()

    md_path = Path(__file__).parent / "Sprint_7_Catalog_Seed_List.md"
    if not md_path.exists():
        sys.exit(f"ERROR: {md_path} not found")

    entries = parse_seed_file(md_path)
    print(f"Parsed {len(entries)} entries from seed list.")
    if not entries:
        sys.exit("ERROR: no entries parsed — check markdown format")

    conn = get_connection(args.target)
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    print(f"Connected ({args.target}).\n")

    totals = dict(master_inserted=0, master_existed=0,
                  aliases_inserted=0, aliases_rescued=0,
                  aliases_skipped_already_linked=0)
    errors = []

    for i, entry in enumerate(entries, 1):
        canonical = entry.get("canonical", "?")
        try:
            c = seed_entry(cur, entry)
            conn.commit()
            totals["master_inserted"  ] += int( c["master_was_inserted"])
            totals["master_existed"   ] += int(not c["master_was_inserted"])
            totals["aliases_inserted" ] += c["ai_inserted"]
            totals["aliases_rescued"  ] += c["ai_rescued"]
            totals["aliases_skipped_already_linked"] += c["ai_skipped"]
            tag = "NEW   " if c["master_was_inserted"] else "EXISTS"
            print(f"  [{i:3d}] {tag} | {canonical[:50]:<50} "
                  f"+{c['ai_inserted']:2d} ins  "
                  f"{c['ai_rescued']:1d} rescued  "
                  f"{c['ai_skipped']:1d} skipped")
        except Exception as e:
            conn.rollback()
            errors.append((canonical, str(e)))
            print(f"  [{i:3d}] ERROR  | {canonical}: {e}")

    cur.close()
    conn.close()

    w = 34
    print("\n" + "=" * 60)
    print(f"{'TARGET':<{w}} {args.target}")
    print(f"{'master_inserted':<{w}} {totals['master_inserted']}")
    print(f"{'master_existed':<{w}} {totals['master_existed']}")
    print(f"{'aliases_inserted':<{w}} {totals['aliases_inserted']}")
    print(f"{'aliases_rescued':<{w}} {totals['aliases_rescued']}")
    print(f"{'aliases_skipped_already_linked':<{w}} {totals['aliases_skipped_already_linked']}")
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for name, msg in errors:
            print(f"  {name}: {msg}")
    else:
        print("\nNo errors.")
    print("=" * 60)


if __name__ == "__main__":
    main()
