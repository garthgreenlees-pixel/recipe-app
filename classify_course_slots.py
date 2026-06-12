#!/usr/bin/env python3
"""
Canon cookbook — course_slots classification for recipe-bearing entries.
1. Classify via Anthropic Haiku: name + description + recipe_card headline → course
2. Grade pass: 10% resample for disagreement check (>5% = STOP)
3. Batch writes ≤400 rows / 15 min (watcher alert threshold is 500)
4. Verification report

Writes to technique_references.course_slots (jsonb).
NEVER modifies pro_tips, recipe_card, or the recipes table.
"""
import os, sys, json, time, random, math
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
import psycopg2, psycopg2.extras

# ── Course vocabulary ────────────────────────────────────────────────────────
# Dual-slot rule (founder-approved 2026-06-11): festive enriched breads
# (colomba, panettone, stollen, etc.) dual-slot across pastry AND breads.
COURSES = [
    "soups",
    "salads",
    "appetizers",
    "mains",
    "sides",
    "desserts",
    "pastry",
    "breads",
    "sauces-and-bases",
    "drinks-and-accompaniments",
    "uncategorized",
]

COURSES_CSV = ", ".join(COURSES)

# ── DB connection ────────────────────────────────────────────────────────────
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    vals = {}
    for line in open(env_path).read().splitlines():
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals

ENV = load_env()
DB_READ  = ENV.get('DATABASE_URL', '')
DB_WRITE = ENV.get('DATABASE_URL_WRITE') or DB_READ
ANTHROPIC_KEY = ENV.get('ANTHROPIC_API_KEY', '')

def get_db_read():
    return psycopg2.connect(DB_READ, connect_timeout=10)

def get_db_write():
    conn = psycopg2.connect(DB_WRITE, connect_timeout=10)
    conn.autocommit = False
    return conn

# ── Claude classification ────────────────────────────────────────────────────
HAIKU_MODEL = "claude-haiku-4-5-20251001"
# Cost per row (generous): ~300 input tokens + ~20 output tokens
COST_INPUT_PER_MTOK  = 0.80
COST_OUTPUT_PER_MTOK = 4.00
AVG_INPUT_TOKS  = 300
AVG_OUTPUT_TOKS = 20

def estimate_cost(n_rows, passes=1):
    input_cost  = (n_rows * AVG_INPUT_TOKS  / 1_000_000) * COST_INPUT_PER_MTOK * passes
    output_cost = (n_rows * AVG_OUTPUT_TOKS / 1_000_000) * COST_OUTPUT_PER_MTOK * passes
    return input_cost + output_cost


CLASSIFY_SYSTEM = f"""\
Classify this recipe into exactly ONE course category from this fixed list:
{COURSES_CSV}

Rules:
- Return ONLY the category string, nothing else. No quotes, no JSON, no explanation.
- "uncategorized" only if genuinely none of the others fit.
- "sauces-and-bases" for stocks, mother sauces, condiments, vinaigrettes, rubs, marinades.
- "drinks-and-accompaniments" for cocktails, teas, coffees, infusions, shrubs, syrups served as drinks.
- "pastry" for pastry technique entries (puff pastry, choux, pie dough, laminated dough).
- "breads" for bread, flatbreads, pizza dough, naan, focaccia.
- "appetizers" for small plates, mezze, tapas, amuse-bouche, canapés, dips, spreads.
- "sides" for vegetable dishes, grains, rice dishes, pickles served as accompaniment.
- "desserts" for sweet courses, ice cream, custard, mousse, fruit desserts.
- "mains" for protein-centred dishes, stews, curries, roasts, pasta mains, main-course soups.
- "soups" for soups served as a distinct course (not stew-like mains).
- "salads" for composed salads, slaws, dressed vegetable dishes served cold/room temp."""


def _make_classify_prompt(name, description, recipe_card):
    """Build the user prompt for classification."""
    parts = [f"Name: {name}"]
    if description:
        parts.append(f"Description: {description[:300]}")
    if recipe_card:
        card = recipe_card if isinstance(recipe_card, dict) else json.loads(recipe_card)
        ings = card.get('ingredients', [])
        if ings:
            parts.append(f"Key ingredients: {', '.join(ings[:5])}")
        steps = card.get('steps', [])
        if steps:
            parts.append(f"Method headline: {steps[0][:120]}")
        serves = card.get('serves')
        if serves:
            parts.append(f"Serves: {serves}")
    return "\n".join(parts)


def classify_one(client, name, description, recipe_card):
    """Call Haiku to classify one entry. Returns course string or None."""
    try:
        prompt = _make_classify_prompt(name, description, recipe_card)
        resp = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=30,
            system=CLASSIFY_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
            timeout=15.0,
        )
        raw = resp.content[0].text.strip().lower().strip('"').strip("'")
        if raw in COURSES:
            return raw
        # Fuzzy match: strip whitespace/dashes variations
        normalised = raw.replace(' ', '-').replace('_', '-')
        if normalised in COURSES:
            return normalised
        print(f"    WARNING: unexpected classification '{raw}' for {name[:40]}", file=sys.stderr)
        return "uncategorized"
    except Exception as e:
        print(f"    Claude error: {e}", file=sys.stderr)
        return None


# ── Batch write with pacing ──────────────────────────────────────────────────
BATCH_SIZE = 400
BATCH_WINDOW_SECS = 900

def write_batch(conn, updates):
    """Write a list of (id, course_list) to technique_references.course_slots."""
    cur = conn.cursor()
    for rid, course_list in updates:
        cur.execute(
            "UPDATE technique_references SET course_slots = %s WHERE id = %s",
            (json.dumps(course_list), rid)
        )
    conn.commit()
    cur.close()


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    import anthropic

    conn_r = get_db_read()
    cur = conn_r.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Baseline
    cur.execute("SELECT COUNT(*) AS n FROM technique_references WHERE course_slots IS NOT NULL")
    baseline_slots = cur.fetchone()['n']
    print(f"Baseline course_slots populated: {baseline_slots}")

    # pro_tips checksum (safety — must not change)
    cur.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) AS ck FROM technique_references")
    pt_checksum_before = cur.fetchone()['ck']

    # recipe_card checksum (safety — must not change)
    cur.execute("""SELECT MD5(STRING_AGG(COALESCE(recipe_card::text,''), '' ORDER BY id)) AS ck
                   FROM technique_references""")
    rc_checksum_before = cur.fetchone()['ck']

    # recipes table count (safety baseline)
    try:
        cur.execute("SELECT COUNT(*) AS n FROM recipes")
        recipes_count_before = cur.fetchone()['n']
    except Exception:
        recipes_count_before = None

    # All recipe-bearing entries without course_slots
    cur.execute("""
        SELECT id, slug, name, description, recipe_card
        FROM technique_references
        WHERE recipe_card IS NOT NULL AND course_slots IS NULL
        ORDER BY id
    """)
    rows = cur.fetchall()
    cur.close(); conn_r.close()

    print(f"Rows to classify: {len(rows)}")
    if not rows:
        print("Nothing to do.")
        return

    # ── Step 2: Budget guard ──
    # Classification pass + 10% grade pass
    grade_n = max(1, math.ceil(len(rows) * 0.10))
    total_calls = len(rows) + grade_n
    est_cost = estimate_cost(total_calls)
    print(f"\nBudget estimate: {total_calls} API calls (classify={len(rows)}, grade={grade_n})")
    print(f"  Projected cost: ${est_cost:.2f}")
    if est_cost > 4.00:
        print("  OVER $4 BUDGET — STOPPING. Report cost and exit.")
        print(f"\n  To proceed, reduce row count or increase budget.")
        return

    print(f"  Under $4 — proceeding.\n")

    # ── Step 2: Classify ──
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    classifications = []  # list of (id, slug, name, course)
    errors = []

    print(f"Classifying {len(rows)} entries...")
    for i, row in enumerate(rows):
        course = classify_one(client, row['name'], row['description'], row['recipe_card'])
        if course:
            classifications.append((row['id'], row['slug'], row['name'], course))
        else:
            errors.append(row)
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(rows)} classified...")
        time.sleep(0.1)  # gentle pacing

    print(f"Classified: {len(classifications)}")
    print(f"Errors (skipped): {len(errors)}")

    # ── Step 3: Grade pass — 10% resample ──
    print(f"\nGrade pass: re-classifying {grade_n} entries...")
    grade_sample = random.sample(classifications, min(grade_n, len(classifications)))
    disagreements = []

    for rid, slug, name, original_course in grade_sample:
        # Find the original row data
        row_data = next((r for r in rows if r['id'] == rid), None)
        if not row_data:
            continue
        recheck = classify_one(client, row_data['name'], row_data['description'],
                               row_data['recipe_card'])
        if recheck and recheck != original_course:
            disagreements.append({
                'slug': slug,
                'name': name,
                'original': original_course,
                'recheck': recheck,
            })
        time.sleep(0.1)

    disagree_rate = len(disagreements) / max(1, len(grade_sample))
    print(f"  Disagreements: {len(disagreements)}/{len(grade_sample)} ({disagree_rate:.1%})")

    if disagree_rate > 0.05:
        print(f"\n  DISAGREEMENT RATE {disagree_rate:.1%} > 5% — STOPPING.")
        print("  Awaiting operator call before any writes.")
        print("\n  Disagreement details:")
        for d in disagreements:
            print(f"    {d['slug']}: {d['original']} vs {d['recheck']}")
        # Write the report but do NOT write to DB
        _write_report(baseline_slots, len(classifications), classifications,
                       grade_sample, disagreements, disagree_rate,
                       0, pt_checksum_before, None, rc_checksum_before, None,
                       recipes_count_before, None, errors, wrote=False)
        return

    print(f"  Grade pass OK ({disagree_rate:.1%} ≤ 5%).\n")

    # ── Step 4: Write in batches ──
    # course_slots format: simple JSON array of course strings
    all_updates = [(rid, [course]) for rid, slug, name, course in classifications]
    print(f"Writing {len(all_updates)} rows in batches ≤{BATCH_SIZE}")

    conn_w = get_db_write()
    total_written = 0
    batch_num = 0

    for start in range(0, len(all_updates), BATCH_SIZE):
        batch = all_updates[start:start + BATCH_SIZE]
        batch_num += 1
        t0 = time.time()
        write_batch(conn_w, batch)
        elapsed = time.time() - t0
        total_written += len(batch)
        print(f"  Batch {batch_num}: wrote {len(batch)} rows in {elapsed:.1f}s "
              f"({total_written}/{len(all_updates)} total)")
        if start + BATCH_SIZE < len(all_updates):
            remaining = len(all_updates) - (start + BATCH_SIZE)
            print(f"  Pacing — waiting 15 min before next batch ({remaining} remaining)...")
            time.sleep(BATCH_WINDOW_SECS)

    conn_w.close()

    # ── Step 5: Verification ──
    conn_r2 = get_db_read()
    cur2 = conn_r2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur2.execute("SELECT COUNT(*) AS n FROM technique_references WHERE course_slots IS NOT NULL")
    final_slots = cur2.fetchone()['n']

    cur2.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) AS ck FROM technique_references")
    pt_checksum_after = cur2.fetchone()['ck']

    cur2.execute("""SELECT MD5(STRING_AGG(COALESCE(recipe_card::text,''), '' ORDER BY id)) AS ck
                    FROM technique_references""")
    rc_checksum_after = cur2.fetchone()['ck']

    try:
        cur2.execute("SELECT COUNT(*) AS n FROM recipes")
        recipes_count_after = cur2.fetchone()['n']
    except Exception:
        recipes_count_after = None

    cur2.close(); conn_r2.close()

    _write_report(baseline_slots, final_slots, classifications,
                   grade_sample, disagreements, disagree_rate,
                   total_written, pt_checksum_before, pt_checksum_after,
                   rc_checksum_before, rc_checksum_after,
                   recipes_count_before, recipes_count_after, errors, wrote=True)


def _write_report(baseline_slots, final_or_classified, classifications,
                   grade_sample, disagreements, disagree_rate,
                   total_written, pt_ck_before, pt_ck_after,
                   rc_ck_before, rc_ck_after,
                   recipes_before, recipes_after, errors, wrote=True):
    """Print report to stdout."""
    # Course distribution
    dist = {}
    for _, slug, name, course in classifications:
        dist[course] = dist.get(course, 0) + 1

    # 10 random samples for taste-check
    sample_10 = random.sample(classifications, min(10, len(classifications)))

    # 20-slug spot-check list
    spot_20 = random.sample(classifications, min(20, len(classifications)))

    print("\n" + "=" * 60)
    print("COURSE CLASSIFICATION REPORT")
    print("=" * 60)

    if wrote:
        print(f"course_slots before: {baseline_slots}")
        print(f"course_slots after:  {final_or_classified}")
        print(f"Net new:             {final_or_classified - baseline_slots}")
    else:
        print(f"course_slots before: {baseline_slots}")
        print(f"Classified (NOT written — grade fail): {len(classifications)}")

    print(f"Rows classified:     {len(classifications)}")
    print(f"Errors (skipped):    {len(errors)}")
    print(f"Total written:       {total_written}")

    print(f"\nGrade pass: {len(disagreements)}/{len(grade_sample)} disagreements ({disagree_rate:.1%})")
    if disagreements:
        for d in disagreements:
            print(f"  {d['slug']}: {d['original']} → {d['recheck']}")

    print(f"\nCourse distribution:")
    for course in COURSES:
        count = dist.get(course, 0)
        if count:
            print(f"  {course:30s} {count:4d}")
    print(f"  {'TOTAL':30s} {sum(dist.values()):4d}")

    if wrote:
        print(f"\nSafety checks:")
        print(f"  pro_tips checksum match:    {pt_ck_before == pt_ck_after}")
        print(f"  recipe_card checksum match: {rc_ck_before == rc_ck_after}")
        if recipes_before is not None and recipes_after is not None:
            print(f"  recipes table count:        {recipes_before} → {recipes_after} (unchanged: {recipes_before == recipes_after})")

    print(f"\n10 random samples (name → course):")
    for _, slug, name, course in sample_10:
        print(f"  {name[:50]:50s} → {course}")

    print(f"\n20-slug spot-check list for morning:")
    for i, (_, slug, name, course) in enumerate(spot_20, 1):
        print(f"  {i:2d}. {slug} → {course}")


if __name__ == "__main__":
    main()
