#!/usr/bin/env python3
"""
Promote a canon's technique_references from staging to live.

DEFAULT: dry-run — reads staging + live, prints what would happen, touches nothing.
LIVE:    --execute, then interactive confirmation:
             operator must type "<canon_slug> PROMOTE TO LIVE"

Usage:
    python3 scripts/promote_canon.py japanese           # dry-run
    python3 scripts/promote_canon.py japanese --execute # live (requires confirmation)

Precondition gates (all checked before any write):
    a. Live open_folio flags match the founder list in founder_folio_list.md.
       If live carries slugs not on that list, refuse and print cleanup SQL.
    b. founder_folio_list.md exists and names at least one folio for this canon.
    c. Every source_book stamped on the canon's staging entries has a
       signed-off verification sheet in verification_sheets/.

Promotion (--execute only, after all gates pass):
    - technique_references: INSERT new rows (staging slug not in live),
      UPDATE existing rows matched by slug. NEVER delete live rows.
      NEVER touch the recipes table. Live row ids are preserved.
    - canon_sections: DELETE-then-INSERT for this canon (refresh).
    - published flags carry over exactly as they stand on staging.
    - Wrapped in a single transaction; any error rolls back fully.

Connections:
    Staging read : DATABASE_URL_STAGING  (or DATABASE_URL with 5433→5434)
    Live read    : DATABASE_URL
    Live write   : DATABASE_URL_WRITE    (only opened with --execute)
"""

import argparse
import os
import re
import sys

import psycopg2
import psycopg2.extras

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS_DIR = os.path.join(ROOT, "verification_sheets")
FOUNDER_LIST_PATH = os.path.join(ROOT, "founder_folio_list.md")


# ── Environment ───────────────────────────────────────────────────────────────

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


def _dsns(env):
    def _e(key):
        return os.environ.get(key) or env.get(key, "")

    live_read  = _e("DATABASE_URL")
    live_write = _e("DATABASE_URL_WRITE") or live_read
    staging_explicit = _e("DATABASE_URL_STAGING")
    if staging_explicit:
        staging = staging_explicit
    elif ":5433/" in live_read:
        staging = re.sub(r":5433/", ":5434/", live_read)
    else:
        staging = live_read  # local dev fallback: same DB
    return staging, live_read, live_write


def _connect_ro(dsn, label):
    try:
        conn = psycopg2.connect(dsn)
        conn.set_session(readonly=True)
        return conn
    except Exception as exc:
        sys.exit(f"ERROR: Cannot connect to {label}: {exc}")


def _connect_rw(dsn, label):
    try:
        return psycopg2.connect(dsn)
    except Exception as exc:
        sys.exit(f"ERROR: Cannot connect to {label}: {exc}")


# ── Founder list ──────────────────────────────────────────────────────────────

def _load_founder_list(path):
    """Return set of authorised open_folio slugs, or None if file is missing."""
    try:
        lines = open(path).read().splitlines()
    except FileNotFoundError:
        return None
    slugs = set()
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.lstrip("-").strip()
        if line and not line.startswith("#"):
            slugs.add(line)
    return slugs


# ── Gates ─────────────────────────────────────────────────────────────────────

def _gate_a(live_cur, founder_slugs):
    """Live open_folio flags must exactly match the founder list."""
    live_cur.execute(
        "SELECT slug FROM technique_references WHERE open_folio = TRUE ORDER BY slug"
    )
    live_open = {r["slug"] for r in live_cur.fetchall()}
    stray = live_open - founder_slugs

    if not stray:
        print(
            f"  [gate-a] PASS  — live open_folio matches founder list "
            f"({len(live_open)} authorised slug(s))"
        )
        return True

    print(
        f"  [gate-a] FAIL  — {len(stray)} live row(s) carry open_folio=TRUE "
        f"that are not on the founder list."
    )
    print()
    print("  Cleanup SQL (review carefully, then run manually as a separate step):")
    print("  " + "-" * 66)
    slug_list = ",\n    ".join(f"'{s}'" for s in sorted(stray))
    print(
        f"  UPDATE technique_references\n"
        f"  SET    open_folio = FALSE\n"
        f"  WHERE  slug IN (\n"
        f"    {slug_list}\n"
        f"  );"
    )
    print("  " + "-" * 66)
    missing_from_live = founder_slugs - live_open
    if missing_from_live:
        print(
            f"\n  NOTE: {len(missing_from_live)} founder-list slug(s) are not "
            f"open_folio=TRUE in live — may be intentional."
        )
    return False


def _gate_b(path, canon_slug, staging_cur):
    """founder_folio_list.md must exist and name at least one folio for this canon."""
    if not os.path.exists(path):
        print(
            f"  [gate-b] FAIL  — {path} not found. "
            "Create and populate it before promoting."
        )
        return False

    founder_slugs = _load_founder_list(path) or set()
    staging_cur.execute(
        "SELECT slug FROM technique_references WHERE canon_slug = %s",
        (canon_slug,),
    )
    canon_slugs = {r["slug"] for r in staging_cur.fetchall()}
    named = canon_slugs & founder_slugs

    if not named:
        print(
            f"  [gate-b] FAIL  — founder_folio_list.md exists but names no folios "
            f"for canon '{canon_slug}'. Populate it for this canon first."
        )
        return False

    print(
        f"  [gate-b] PASS  — {len(named)} folio(s) for '{canon_slug}' "
        "named in founder_folio_list.md"
    )
    return True


def _gate_c(canon_slug, staging_cur):
    """Every source_book on staging entries must have a signed-off sheet."""
    staging_cur.execute(
        """
        SELECT DISTINCT source_book
        FROM   technique_references
        WHERE  canon_slug = %s
          AND  published IS NOT FALSE
          AND  source_book IS NOT NULL
          AND  source_book <> ''
        ORDER  BY source_book
        """,
        (canon_slug,),
    )
    books = [r["source_book"] for r in staging_cur.fetchall()]

    if not books:
        print(
            f"  [gate-c] PASS  — no source_books stamped on '{canon_slug}' entries "
            "(nothing to verify)"
        )
        return True

    def _slugify(text):
        s = text.lower().strip()
        return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]

    def _is_signed(sheet_path):
        try:
            content = open(sheet_path).read()
        except FileNotFoundError:
            return False, "sheet not found"
        for line in content.splitlines():
            if "Verified against physical copy —" in line or \
               "Verified against physical copy --" in line or \
               "Verified against physical copy —" in line:
                signed = "___" not in line
                return signed, "sign-off line present" if signed else "sign-off line blank"
        return False, "sign-off line missing from sheet"

    all_ok = True
    for book in books:
        sheet_path = os.path.join(SHEETS_DIR, f"{canon_slug}_{_slugify(book)}.md")
        signed, reason = _is_signed(sheet_path)
        status = "PASS" if signed else "FAIL"
        rel = os.path.relpath(sheet_path, ROOT)
        print(f"  [gate-c] {status}  — '{book}' → {rel}: {reason}")
        if not signed:
            all_ok = False

    return all_ok


# ── Dry-run report ────────────────────────────────────────────────────────────

def _dry_run_report(canon_slug, staging_rows, live_cur):
    live_cur.execute(
        "SELECT slug FROM technique_references WHERE canon_slug = %s", (canon_slug,)
    )
    live_slugs = {r["slug"] for r in live_cur.fetchall()}
    staging_slugs = {r.get("slug") for r in staging_rows}

    would_insert = [r for r in staging_rows if r.get("slug") not in live_slugs]
    would_update = [r for r in staging_rows if r.get("slug") in live_slugs]

    print(f"\n  technique_references [{canon_slug}]")
    print(f"    staging rows  : {len(staging_rows)}")
    print(f"    live rows     : {len(live_slugs)}")
    print(f"    would INSERT  : {len(would_insert)}")
    print(f"    would UPDATE  : {len(would_update)}")
    print(f"    live-only     : {len(live_slugs - staging_slugs)}  (would be untouched)")

    if would_insert:
        print("    INSERT:")
        for r in sorted(would_insert, key=lambda x: x.get("slug") or ""):
            pub = "pub" if r.get("published") is not False else "unpub"
            print(f"      +  {r.get('slug')}  [{pub}]")

    if would_update:
        display = sorted(would_update, key=lambda x: x.get("slug") or "")
        print(f"    UPDATE (first {min(10, len(display))}):")
        for r in display[:10]:
            pub = "pub" if r.get("published") is not False else "unpub"
            print(f"      ~  {r.get('slug')}  [{pub}]")
        if len(would_update) > 10:
            print(f"      … and {len(would_update) - 10} more")

    # canon_sections
    live_cur.execute(
        "SELECT section_slug FROM canon_sections WHERE canon_slug = %s", (canon_slug,)
    )
    live_secs = [r["section_slug"] for r in live_cur.fetchall()]
    print(f"\n  canon_sections [{canon_slug}]")
    print(f"    live sections : {len(live_secs)}  {live_secs}")
    print(f"    (staging sections fetched at runtime — shown as part of promotion)")


# ── Promotion (execute only) ──────────────────────────────────────────────────

def _promote(canon_slug, staging_rows, staging_sections, write_conn):
    cur = write_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Resolve actual columns present in staging data
    if not staging_rows:
        print("  technique_references: 0 staging rows — nothing to promote")
        inserted = updated = 0
    else:
        sample = staging_rows[0]
        all_cols = list(sample.keys())
        # INSERT: all columns except id (let live DB assign id)
        insert_cols = [c for c in all_cols if c != "id"]
        # UPDATE: all columns except id (preserved) and slug (matching key)
        #         skip created_at too — preserve live creation timestamp
        update_cols = [c for c in all_cols if c not in ("id", "slug", "created_at")]

        cur.execute(
            "SELECT slug, id FROM technique_references WHERE canon_slug = %s",
            (canon_slug,),
        )
        live_slug_ids = {r["slug"]: r["id"] for r in cur.fetchall()}

        inserted = updated = 0
        for row in staging_rows:
            slug = row.get("slug")
            if slug in live_slug_ids:
                set_clause = ", ".join(f"{c} = %s" for c in update_cols)
                vals = [row.get(c) for c in update_cols] + [slug]
                cur.execute(
                    f"UPDATE technique_references SET {set_clause} WHERE slug = %s",
                    vals,
                )
                updated += 1
            else:
                cols_clause = ", ".join(insert_cols)
                vals_ph = ", ".join("%s" for _ in insert_cols)
                vals = [row.get(c) for c in insert_cols]
                cur.execute(
                    f"INSERT INTO technique_references ({cols_clause}) "
                    f"VALUES ({vals_ph})",
                    vals,
                )
                inserted += 1

        print(f"  technique_references: {inserted} inserted, {updated} updated")

    # canon_sections — delete existing for this canon, then re-insert from staging
    cur.execute("DELETE FROM canon_sections WHERE canon_slug = %s", (canon_slug,))
    deleted_secs = cur.rowcount

    if staging_sections:
        s_cols = [c for c in staging_sections[0].keys() if c != "id"]
        cols_clause = ", ".join(s_cols)
        vals_ph = ", ".join("%s" for _ in s_cols)
        for sec in staging_sections:
            vals = [sec.get(c) for c in s_cols]
            cur.execute(
                f"INSERT INTO canon_sections ({cols_clause}) VALUES ({vals_ph})", vals
            )
        print(
            f"  canon_sections: {deleted_secs} removed, "
            f"{len(staging_sections)} reinserted"
        )
    else:
        print(f"  canon_sections: {deleted_secs} removed, 0 staging rows to insert")

    cur.close()
    return inserted, updated


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Promote a canon staging→live (default: dry-run)."
    )
    parser.add_argument("canon_slug")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Write to live (requires interactive confirmation).",
    )
    args = parser.parse_args()
    canon_slug = args.canon_slug

    env = _load_env()
    staging_dsn, live_read_dsn, live_write_dsn = _dsns(env)
    mode = "LIVE EXECUTE" if args.execute else "DRY-RUN"

    print(f"\n{'='*62}")
    print(f"  promote_canon.py  —  {mode}")
    print(f"  canon: {canon_slug}")
    print(f"{'='*62}\n")

    staging_conn  = _connect_ro(staging_dsn,  "staging")
    live_read_conn = _connect_ro(live_read_dsn, "live (read)")

    staging_cur   = staging_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    live_read_cur = live_read_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Prefetch staging data once — used by gates + report + promote
    staging_cur.execute(
        "SELECT * FROM technique_references WHERE canon_slug = %s", (canon_slug,)
    )
    staging_rows = [dict(r) for r in staging_cur.fetchall()]

    staging_cur.execute(
        "SELECT * FROM canon_sections WHERE canon_slug = %s", (canon_slug,)
    )
    staging_sections = [dict(r) for r in staging_cur.fetchall()]

    print(
        f"Staging: {len(staging_rows)} technique_references row(s) for '{canon_slug}'"
    )
    print(
        f"Staging: {len(staging_sections)} canon_sections row(s) for '{canon_slug}'\n"
    )

    # ── Gate checks ────────────────────────────────────────────────────────────
    print("Checking gates …\n")
    founder_slugs = _load_founder_list(FOUNDER_LIST_PATH)

    if founder_slugs is None:
        print(
            f"  [gate-a] FAIL  — {FOUNDER_LIST_PATH} not found. "
            "Cannot compare live open_folio flags."
        )
        a_ok = False
    else:
        a_ok = _gate_a(live_read_cur, founder_slugs)

    b_ok = _gate_b(FOUNDER_LIST_PATH, canon_slug, staging_cur)
    c_ok = _gate_c(canon_slug, staging_cur)

    gates_ok = a_ok and b_ok and c_ok

    # ── Dry-run report ─────────────────────────────────────────────────────────
    print("\nDry-run report:")
    _dry_run_report(canon_slug, staging_rows, live_read_cur)

    staging_cur.close()
    staging_conn.close()
    live_read_cur.close()
    live_read_conn.close()

    if not args.execute:
        print(f"\n{'='*62}")
        print(f"  DRY-RUN COMPLETE — zero writes made")
        print(f"  Gates: {'ALL PASS' if gates_ok else 'ONE OR MORE FAILED'}")
        if not gates_ok:
            print(f"  Resolve all gate failures before running with --execute.")
        print(f"{'='*62}\n")
        sys.exit(0 if gates_ok else 1)

    # ── Live execute ───────────────────────────────────────────────────────────
    if not gates_ok:
        print(f"\nERROR: Gate failure(s) above — refusing to promote. Fix them first.")
        sys.exit(1)

    print(f"\n{'!'*62}")
    print(f"  LIVE EXECUTE requested for canon '{canon_slug}'.")
    print(f"  This will INSERT/UPDATE rows in the live database.")
    print(f"  Type exactly to confirm:")
    print(f"      {canon_slug} PROMOTE TO LIVE")
    print(f"{'!'*62}")
    try:
        confirmation = input("\n  Confirmation: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(1)

    if confirmation != f"{canon_slug} PROMOTE TO LIVE":
        print("\nAborted — confirmation text did not match.")
        sys.exit(1)

    print("\nOpening live write connection …")
    live_write_conn = _connect_rw(live_write_dsn, "live (write)")

    try:
        with live_write_conn:
            inserted, updated = _promote(
                canon_slug, staging_rows, staging_sections, live_write_conn
            )
        print("\n  Transaction committed.")
    except Exception as exc:
        print(f"\nERROR: Transaction rolled back. Reason: {exc}")
        sys.exit(1)
    finally:
        live_write_conn.close()

    print(f"\n{'='*62}")
    print(f"  PROMOTION COMPLETE")
    print(
        f"  Canon '{canon_slug}': {inserted} row(s) inserted, {updated} row(s) updated"
    )
    print(f"{'='*62}\n")


if __name__ == "__main__":
    main()
