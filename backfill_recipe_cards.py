"""
Canon Render Cycle B — backfill script.
Parses RECIPE: blobs in pro_tips, writes to recipe_card column.
pro_tips is never modified.
Run once with DATABASE_URL_WRITE.
"""
import os, sys, re as _re, json, psycopg2
from psycopg2.extras import RealDictCursor


def parse_recipe_blob(text):
    """Strict parser — returns dict or None on any ambiguity."""
    if not text or 'RECIPE:' not in text:
        return None
    idx = text.find('RECIPE:')
    blob = text[idx:]
    lines = blob.split('\n')
    pos = 1
    while pos < len(lines) and not lines[pos].strip():
        pos += 1
    if pos >= len(lines):
        return None
    meta_line = lines[pos].strip()
    pos += 1
    if 'Serves' not in meta_line:
        return None
    serves = prep = total = None
    for part in meta_line.split('|'):
        part = part.strip()
        if part.lower().startswith('serves:'):
            serves = part.split(':', 1)[1].strip()
        elif part.lower().startswith('prep:'):
            prep = part.split(':', 1)[1].strip()
        elif part.lower().startswith('total:'):
            total = part.split(':', 1)[1].strip()
    if not serves:
        return None
    while pos < len(lines) and lines[pos].strip() != '---':
        pos += 1
    if pos >= len(lines):
        return None
    pos += 1
    ingredients = []
    while pos < len(lines) and lines[pos].strip() != '---':
        line = lines[pos].strip()
        if line:
            ingredients.append(line)
        pos += 1
    if not ingredients or pos >= len(lines):
        return None
    pos += 1
    steps = []
    while pos < len(lines):
        line = lines[pos].strip()
        if line:
            clean = _re.sub(r'^\d+[\.\)]\s*', '', line)
            if clean:
                steps.append(clean)
        pos += 1
    if not steps:
        return None
    return {'serves': serves, 'prep': prep, 'total': total,
            'ingredients': ingredients, 'steps': steps}


db_url = os.environ.get('DATABASE_URL_WRITE') or os.environ.get('DATABASE_URL')
if not db_url:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith('DATABASE_URL_WRITE='):
                db_url = line.split('=', 1)[1]
                break
        if not db_url:
            for line in open(env_path):
                line = line.strip()
                if line.startswith('DATABASE_URL=') and 'WRITE' not in line:
                    db_url = line.split('=', 1)[1]
                    break

if not db_url:
    sys.exit('ERROR: DATABASE_URL_WRITE not found')

conn = psycopg2.connect(db_url)
conn.autocommit = False
cur = conn.cursor(cursor_factory=RealDictCursor)

# Fetch all candidate rows
cur.execute("""
    SELECT id, name, pro_tips FROM technique_references
    WHERE pro_tips LIKE '%RECIPE:%'
""")
rows = cur.fetchall()

parsed_rows = []
skipped_rows = []

for row in rows:
    result = parse_recipe_blob(row['pro_tips'])
    if result:
        parsed_rows.append((row['id'], row['name'], result))
    else:
        skipped_rows.append((row['id'], row['name']))

print(f"Candidate rows with RECIPE: marker: {len(rows)}")
print(f"Parsed successfully:                {len(parsed_rows)}")
print(f"Skipped (ambiguous/malformed):      {len(skipped_rows)}")
print()

print("Sample parsed (up to 3):")
for rid, name, card in parsed_rows[:3]:
    print(f"  id={rid}  {name!r}")
    print(f"    serves={card['serves']}  prep={card['prep']}  total={card['total']}")
    print(f"    ingredients={len(card['ingredients'])}  steps={len(card['steps'])}")

print()
print("Sample skipped (up to 3):")
for rid, name in skipped_rows[:3]:
    print(f"  id={rid}  {name!r}")

if not parsed_rows:
    print("Nothing to write — exiting.")
    conn.close()
    sys.exit(0)

# Write recipe_card for parsed rows
write_cur = conn.cursor()
for rid, name, card in parsed_rows:
    write_cur.execute(
        "UPDATE technique_references SET recipe_card = %s WHERE id = %s",
        (json.dumps(card), rid)
    )

conn.commit()
print(f"\nWrote recipe_card to {len(parsed_rows)} rows. Committed.")
conn.close()
