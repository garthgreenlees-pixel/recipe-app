#!/usr/bin/env python3
"""
Generate physical-copy verification sheets for a canon's source books.

Usage:
    python3 scripts/generate_verification_sheets.py <canon_slug>

Reads from STAGING. Connection priority:
  1. DATABASE_URL_STAGING env var
  2. DATABASE_URL with :5433/ replaced by :5434/
  3. DATABASE_URL as-is (local dev fallback)

Writes verification_sheets/<canon>_<book_slug>.md — one file per distinct
source_book found on the canon's entries.  Samples 15 entries per book,
seeded on canon_slug + book name so the sample is reproducible across runs.
"""
import argparse
import json
import os
import random
import re
import sys

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


def _slugify(text):
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:60]


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
    hits = list(dict.fromkeys(_TEMP_TIME_RE.findall(blob)))
    return hits[:6]


def _render_entry(entry):
    name = entry.get("name") or "(no name)"
    slug = entry.get("slug") or "(no slug)"
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
            "- [ ] PASS / [ ] FAIL — **Temp/Time:** *(none detected in record — check manually)*"
        )

    lines.append(
        f"- [ ] PASS / [ ] FAIL — **Lives-or-dies pivot:** "
        f"{lives_or_dies or '*(not recorded)*'}"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate verification sheets for a canon's source books."
    )
    parser.add_argument("canon_slug", help="e.g. japanese")
    args = parser.parse_args()
    canon_slug = args.canon_slug

    env = _load_env()
    dsn, dsn_label = _staging_dsn(env)
    if not dsn:
        sys.exit("ERROR: No database URL found. Set DATABASE_URL_STAGING or DATABASE_URL.")

    print(f"Connecting to staging via {dsn_label} …")
    try:
        conn = psycopg2.connect(dsn)
        conn.set_session(readonly=True)
    except Exception as exc:
        sys.exit(f"ERROR: Cannot connect to staging DB: {exc}")

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        """
        SELECT name, slug, origin, lives_or_dies, source_book,
               description, key_principles, quality_hierarchy, sensory_tests
        FROM   technique_references
        WHERE  canon_slug = %s
          AND  published IS NOT FALSE
          AND  source_book IS NOT NULL
          AND  source_book <> ''
        ORDER  BY source_book, slug
        """,
        (canon_slug,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()

    if not rows:
        print(
            f"No published entries with a source_book found for canon '{canon_slug}'. "
            "Nothing to generate."
        )
        sys.exit(0)

    books = {}
    for row in rows:
        books.setdefault(row["source_book"], []).append(row)

    os.makedirs(SHEETS_DIR, exist_ok=True)
    written = []
    used_slugs = {}  # base_slug → count, for deduplication

    for book, entries in sorted(books.items()):
        base_slug = _slugify(book)
        if base_slug in used_slugs:
            used_slugs[base_slug] += 1
            book_slug = f"{base_slug}-{used_slugs[base_slug]}"
        else:
            used_slugs[base_slug] = 0
            book_slug = base_slug
        rng = random.Random(f"{canon_slug}:{book}")
        sample = rng.sample(entries, min(SAMPLE_SIZE, len(entries)))
        sample.sort(key=lambda e: e.get("slug") or "")

        filename = f"{canon_slug}_{book_slug}.md"
        path = os.path.join(SHEETS_DIR, filename)

        header = [
            f"# Verification Sheet: {canon_slug} / {book}",
            "",
            f"**Canon:** `{canon_slug}`  ",
            f"**Source book:** {book}  ",
            f"**Total entries in canon with this book:** {len(entries)}  ",
            f"**Sample size:** {len(sample)} (seeded, reproducible)  ",
            "",
            "---",
            "",
            "## Entries",
            "",
        ]

        entry_blocks = []
        for entry in sample:
            entry_blocks.append(_render_entry(entry))
            entry_blocks.append("")

        footer = [
            "---",
            "",
            "## Sign-off",
            "",
            "All sampled entries above have been verified against a physical copy "
            "of the source book. Complete each checkbox above, then sign below.",
            "",
            "**Verified against physical copy — operator: _______________, "
            "date: _______________**",
            "",
        ]

        with open(path, "w") as fh:
            fh.write("\n".join(header + entry_blocks + footer))

        print(f"  wrote  {path}  ({len(sample)}/{len(entries)} entries sampled)")
        written.append(path)

    print(f"\nDone — {len(written)} sheet(s) written for canon '{canon_slug}'.")


if __name__ == "__main__":
    main()
