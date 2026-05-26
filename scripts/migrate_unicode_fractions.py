#!/usr/bin/env python3
"""
One-shot migration: re-parse ingredient lines whose count is empty and whose
name begins with a Unicode vulgar fraction. Operates ONLY on user_kitchen_recipes
where user_id = 1.

Usage:
  python3 scripts/migrate_unicode_fractions.py            # dry run (default)
  python3 scripts/migrate_unicode_fractions.py --apply    # actually write changes

Requires the Fly proxy to be active:
  flyctl proxy 5433:5432 -a provenance-tester-db
"""
import os
import sys
import json
import argparse
import re

# ─── Fraction normalisation (duplicated here so the script is standalone) ────
_UNICODE_FRACTIONS = {
    '½': 0.5,   '¼': 0.25,  '¾': 0.75,
    '⅓': 1/3,   '⅔': 2/3,
    '⅕': 0.2,   '⅖': 0.4,   '⅗': 0.6,   '⅘': 0.8,
    '⅙': 1/6,   '⅚': 5/6,
    '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875,
    '⅐': 1/7,   '⅑': 1/9,   '⅒': 0.1,
}

FRACTION_CHARS = set(_UNICODE_FRACTIONS.keys())


def _normalize_fractions(line):
    if not line:
        return line
    frac_chars = ''.join(_UNICODE_FRACTIONS.keys())
    def _mixed(m):
        return f'{int(m.group(1)) + _UNICODE_FRACTIONS[m.group(2)]:g}'
    line = re.sub(r'(\d+)\s+([' + frac_chars + r'])', _mixed, line)
    for ch, val in _UNICODE_FRACTIONS.items():
        line = line.replace(ch, f'{val:g}')
    return line


UNITS = [
    "tablespoons", "tablespoon", "teaspoons", "teaspoon", "tbsp", "tsp",
    "cups", "cup", "pints", "pint", "quarts", "quart", "gallons", "gallon",
    "fl oz", "ounces", "ounce", "oz", "pounds", "pound", "lbs", "lb",
    "grams", "gram", "kilograms", "kilogram", "kg", "g", "mg",
    "milliliters", "milliliter", "ml", "liters", "liter", "l",
    "pinch", "dash", "handful", "splash", "drop", "drops", "cloves", "clove",
    "stick", "sticks", "slice", "slices", "can", "cans", "bunch", "bunches",
]


def _parse_ingredient_line(line):
    line = _normalize_fractions((line or "").strip())
    if not line:
        return None
    num_pat = re.compile(r'^\s*(\d+(?:\s+\d+/\d+)?(?:\.\d+)?|\d+/\d+)\s*')
    m = num_pat.match(line)
    count, rest = ("", line)
    if m:
        count = m.group(1).strip()
        rest = line[m.end():].strip()
    unit = ""
    rest_lower = rest.lower()
    for u in UNITS:
        if rest_lower == u or rest_lower.startswith(u + " ") or rest_lower.startswith(u + ","):
            unit = u
            rest = rest[len(u):].strip().lstrip(",").strip()
            if rest.lower().startswith("of "):
                rest = rest[3:].strip()
            break
    if count and not unit:
        fused = re.match(r'^([a-z]+)(?:\s|,|$)', rest, re.IGNORECASE)
        if fused and fused.group(1).lower() in [u for u in UNITS if " " not in u]:
            unit = fused.group(1).lower()
            rest = rest[fused.end():].strip().lstrip(",").strip()
    if not count and not unit:
        for u in ["pinch", "dash", "handful", "splash"]:
            if rest_lower.startswith(u + " "):
                unit = u
                rest = rest[len(u):].strip()
                if rest.lower().startswith("of "):
                    rest = rest[3:].strip()
                break
    name = rest
    info = ""
    paren = re.search(r'\s*\(([^)]+)\)', name)
    if paren:
        info = paren.group(1).strip()
        name = name[:paren.start()].strip()
    if "," in name and not info:
        parts = name.split(",", 1)
        name = parts[0].strip()
        info = parts[1].strip()
    return {"count": count, "unit": unit, "name": name, "info": info, "group": ""}


def has_unicode_fraction(text):
    return any(ch in text for ch in FRACTION_CHARS) if text else False


DATABASE_URL = (
    os.environ.get('DATABASE_URL_WRITE')
    or 'postgres://provenance_tester_1:GBN1MbQJMbe_7Ze2Is6dZQSK4hGwXkbW@localhost:5433/provenance_tester_1?sslmode=disable'
)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apply', action='store_true', help='Write changes (default is dry run)')
    args = ap.parse_args()

    import psycopg2
    from psycopg2.extras import RealDictCursor

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT uuid, slug, title, ingredients
        FROM user_kitchen_recipes
        WHERE user_id = 1
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    print(f'Scanned {len(rows)} recipes belonging to user_id=1')
    print()

    total_recipes_touched = 0
    total_ingredients_fixed = 0

    for row in rows:
        ingredients = row['ingredients'] or []
        if not isinstance(ingredients, list):
            continue

        recipe_changed = False
        new_ingredients = []
        for ing in ingredients:
            count = (ing.get('count') or '').strip()
            name = (ing.get('name') or '').strip()

            # Heuristic: empty count AND fraction anywhere in name → re-parse
            if not count and has_unicode_fraction(name):
                reparsed = _parse_ingredient_line(name)
                if reparsed and reparsed.get('count'):
                    new_ing = {
                        'count': reparsed['count'],
                        'unit': reparsed.get('unit', ''),
                        'name': reparsed['name'],
                        'info': ing.get('info', ''),
                        'group': ing.get('group', ''),
                    }
                    new_ingredients.append(new_ing)
                    recipe_changed = True
                    total_ingredients_fixed += 1
                    print(f"  [{row['slug']}] BEFORE: count='' name={name!r}")
                    print(f"  [{row['slug']}]  AFTER: count={new_ing['count']!r} unit={new_ing['unit']!r} name={new_ing['name']!r}")
                else:
                    new_ingredients.append(ing)
            else:
                new_ingredients.append(ing)

        if recipe_changed:
            total_recipes_touched += 1
            if args.apply:
                cur.execute(
                    "UPDATE user_kitchen_recipes SET ingredients = %s::jsonb WHERE uuid = %s",
                    (json.dumps(new_ingredients), row['uuid'])
                )

    print()
    if args.apply:
        conn.commit()
        print(f'Applied: {total_ingredients_fixed} ingredients fixed across {total_recipes_touched} recipes')
    else:
        print(f'(dry run) Would fix {total_ingredients_fixed} ingredients across {total_recipes_touched} recipes')
        print('Re-run with --apply to write the changes')

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
