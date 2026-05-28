#!/usr/bin/env python3
"""Beverage pairing suggester runner.

Selects the top 50 canon recipes (by created_at DESC), runs the priority-chain
scorer, and inserts pending suggestions into beverage_pairing_suggestions.

DO NOT run this script automatically. Operator runs it manually after Step 7
closes the sprint and Deploy B is live.

Usage:
    DATABASE_URL_WRITE=<url> python scripts/run_pairing_suggester.py
"""

import os
import sys
import json
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ.get("DATABASE_URL_WRITE") or os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL_WRITE (or DATABASE_URL) must be set.")
    sys.exit(1)

# Import the helper from the app module.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SKIP_INIT_DB", "1")  # skip heavy startup when importing server

from server import _suggest_beverages_for_recipe  # noqa: E402


def run():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT id, slug, name, cuisine, tradition_tags, tags
        FROM recipes
        ORDER BY created_at DESC
        LIMIT 50
    """)
    recipes = cur.fetchall()

    suggested_total = 0
    processed = 0

    for recipe in recipes:
        recipe_ref = f"canon:{recipe['slug']}"

        cur.execute("""
            SELECT COUNT(*) AS n FROM beverage_pairing_suggestions
            WHERE recipe_ref = %s AND status = 'pending'
        """, (recipe_ref,))
        pending_count = cur.fetchone()["n"]
        if pending_count >= 3:
            continue

        suggestions = _suggest_beverages_for_recipe(recipe, limit=3, cur=cur)
        if not suggestions:
            continue

        ins_cur = conn.cursor()
        for s in suggestions:
            ins_cur.execute("""
                INSERT INTO beverage_pairing_suggestions
                    (recipe_ref, beverage_product_id, source_tier, role, descriptor,
                     match_score, match_reasoning, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            """, (
                recipe_ref,
                s["beverage_product_id"],
                s["source_tier"],
                s.get("role"),
                s.get("descriptor"),
                s.get("match_score"),
                s.get("match_reasoning"),
            ))
            suggested_total += 1
        ins_cur.close()
        processed += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Suggested {suggested_total} pairings across {processed} recipes. Review queue: /admin/pairings")


if __name__ == "__main__":
    run()
