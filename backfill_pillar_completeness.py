"""
Canon Render Cycle C — backfill script.
Writes pillar_completeness jsonb for every row.
Internal only — never rendered to readers.
Run with DATABASE_URL_WRITE.

Seven pillars:
  I   origin
  II  description
  III cross_cuisine_parallels (The Thread)
  IV  flavour_context
  V   quality_hierarchy
  VI  sensory_tests
  VII lives_or_dies
"""
import os, sys, json, psycopg2
from psycopg2.extras import RealDictCursor
from collections import Counter

db_url = os.environ.get('DATABASE_URL_WRITE') or os.environ.get('DATABASE_URL')
if not db_url:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line.startswith('DATABASE_URL_WRITE='):
                db_url = line.split('=', 1)[1]; break
    if not db_url:
        sys.exit('ERROR: DATABASE_URL_WRITE not found')

PILLARS = [
    ('origin',                'I'),
    ('description',           'II'),
    ('cross_cuisine_parallels','III'),
    ('flavour_context',       'IV'),
    ('quality_hierarchy',     'V'),
    ('sensory_tests',         'VI'),
    ('lives_or_dies',         'VII'),
]

conn = psycopg2.connect(db_url)
conn.autocommit = False
cur = conn.cursor(cursor_factory=RealDictCursor)

cur.execute("""
    SELECT id, origin, description, cross_cuisine_parallels,
           flavour_context, quality_hierarchy, sensory_tests, lives_or_dies
    FROM technique_references
""")
rows = cur.fetchall()

distribution = Counter()
updates = []

for row in rows:
    pc = {}
    count = 0
    for col, _ in PILLARS:
        val = row[col]
        present = False
        if val is None:
            present = False
        elif isinstance(val, str):
            present = bool(val.strip())
        elif isinstance(val, (list, dict)):
            present = bool(val)
        else:
            present = True
        pc[col] = present
        if present:
            count += 1
    pc['count'] = count
    distribution[count] += 1
    updates.append((json.dumps(pc), row['id']))

write_cur = conn.cursor()
write_cur.executemany(
    "UPDATE technique_references SET pillar_completeness = %s WHERE id = %s",
    updates
)
conn.commit()

print(f"Wrote pillar_completeness for {len(updates)} rows.")
print()
print("Completeness distribution (# pillars filled → # rows):")
print(f"  {'Pillars':>7}  {'Rows':>7}  {'%':>6}")
total = len(updates)
for n in range(7, -1, -1):
    count = distribution.get(n, 0)
    pct = count / total * 100 if total else 0
    bar = '█' * int(pct / 2)
    print(f"  {n:>7}  {count:>7}  {pct:>5.1f}%  {bar}")

conn.close()
