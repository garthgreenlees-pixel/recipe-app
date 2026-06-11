#!/usr/bin/env python3
"""
Cycle B2 — recover 281 unparsed recipe_card rows.
1. Extended strict parser (Yield:/Makes: + name-line skip + flexible separators)
2. Claude Haiku sweep for the remainder
3. Batch writes ≤400 rows / 15 min (watcher alert threshold is 500)
4. Verification report

NEVER modifies pro_tips. NEVER touches the recipes table.
"""
import os, sys, re, json, time, random
import psycopg2, psycopg2.extras

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

# ── Extended strict parser ───────────────────────────────────────────────────
META_KEYS = ('serves', 'yield', 'makes', 'portions', 'technique demo on')

def _parse_meta(meta_line):
    """Parse meta line: Yield: X | Prep: Y | Total: Z → {serves, prep, total}"""
    result = {'serves': None, 'prep': None, 'total': None}
    for part in meta_line.split('|'):
        part = part.strip()
        lower = part.lower()
        if lower.startswith('yield:') or lower.startswith('serves:') or \
           lower.startswith('makes:') or lower.startswith('portions:') or \
           lower.startswith('technique demo on:'):
            colon = part.index(':')
            result['serves'] = part[colon+1:].strip()
        elif lower.startswith('prep:'):
            result['prep'] = part.split(':', 1)[1].strip()
        elif lower.startswith('total:') or lower.startswith('time:'):
            result['total'] = part.split(':', 1)[1].strip()
        elif lower.startswith('fermentation:') or lower.startswith('resting:'):
            result['total'] = part.split(':', 1)[1].strip()
    return result


def parse_recipe_blob_extended(text):
    """Extended parser — handles Yield: variants, name-first blobs, flexible ---."""
    if not text or 'RECIPE:' not in text:
        return None
    idx = text.find('RECIPE:')
    blob = text[idx:]
    lines = blob.split('\n')

    # Skip RECIPE: line (pos=0) + blanks
    pos = 1
    while pos < len(lines) and not lines[pos].strip():
        pos += 1
    if pos >= len(lines):
        return None

    meta_line = lines[pos].strip()
    pos += 1

    # If first non-blank line doesn't look like a meta line, try treating
    # it as a recipe name and look at the next non-blank line
    if not any(meta_line.lower().startswith(k) for k in META_KEYS):
        # Skip optional title line and look for meta on the next non-blank line
        while pos < len(lines) and not lines[pos].strip():
            pos += 1
        if pos < len(lines):
            candidate = lines[pos].strip()
            if any(candidate.lower().startswith(k) for k in META_KEYS):
                meta_line = candidate
                pos += 1
            else:
                return None  # no recognisable meta line found
        else:
            return None

    meta = _parse_meta(meta_line)
    if not meta['serves']:
        return None

    # Find first --- separator
    while pos < len(lines) and lines[pos].strip() != '---':
        pos += 1
    if pos >= len(lines):
        return None
    pos += 1

    # Collect ingredients until next --- (or end of blob)
    ingredients = []
    sep2_pos = None
    scan = pos
    while scan < len(lines):
        if lines[scan].strip() == '---':
            sep2_pos = scan
            break
        line = lines[scan].strip()
        if line:
            ingredients.append(line)
        scan += 1

    if not ingredients:
        return None

    # Collect steps
    steps = []
    step_start = (sep2_pos + 1) if sep2_pos is not None else scan
    for i in range(step_start, len(lines)):
        line = lines[i].strip()
        if line == '---':
            continue  # skip extra separators inside steps
        if line:
            clean = re.sub(r'^\d+[\.\)]\s*', '', line)
            if clean:
                steps.append(clean)

    if not steps:
        return None

    return {
        'serves': meta['serves'],
        'prep':   meta['prep'],
        'total':  meta['total'],
        'ingredients': ingredients,
        'steps':  steps,
    }


# ── Claude Haiku sweep ───────────────────────────────────────────────────────
HAIKU_MODEL = "claude-haiku-4-5-20251001"
# Cost estimate per row (generous): 1200 input tokens + 400 output tokens
COST_INPUT_PER_MTOK  = 0.80  # USD
COST_OUTPUT_PER_MTOK = 4.00
AVG_INPUT_TOKS  = 1200
AVG_OUTPUT_TOKS = 400

def estimate_claude_cost(n_rows):
    input_cost  = (n_rows * AVG_INPUT_TOKS  / 1_000_000) * COST_INPUT_PER_MTOK
    output_cost = (n_rows * AVG_OUTPUT_TOKS / 1_000_000) * COST_OUTPUT_PER_MTOK
    return input_cost + output_cost


HAIKU_SYSTEM = """\
Extract a structured recipe from the following culinary technique text.
Return STRICT JSON only — no markdown, no explanation.

Required shape (return null if no recipe is present):
{
  "serves": "string or null",
  "prep": "string or null",
  "total": "string or null",
  "ingredients": ["list of ingredient strings"],
  "steps": ["list of method step strings (no numbers)"]
}

Rules:
- ingredients: one item per list element, preserve measurements and qualifiers
- steps: clean prose steps, strip leading numbers/bullets
- serves/prep/total: extract from Yield:, Serves:, Makes:, Prep:, Total: etc.
- If the text contains no actual recipe (only theory/history/framework), return {"recipe":null}
- Return only the JSON object, nothing else."""


def claude_extract(name, pro_tips_excerpt):
    """Call Haiku to extract a recipe_card dict. Returns dict or None."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        prompt = f"Technique: {name}\n\n{pro_tips_excerpt}"
        resp = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=800,
            system=HAIKU_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
            timeout=30.0,
        )
        raw = resp.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith('```'):
            raw = raw.split('```', 2)[1]
            if raw.startswith('json'):
                raw = raw[4:]
            raw = raw.rsplit('```', 1)[0].strip()
        data = json.loads(raw)
        # Handle {"recipe": null} sentinel
        if 'recipe' in data and data['recipe'] is None:
            return None
        # Validate required structure
        if not data.get('ingredients') or not data.get('steps'):
            return None
        if len(data.get('ingredients', [])) < 2 or len(data.get('steps', [])) < 1:
            return None
        return data
    except Exception as e:
        print(f"    Claude error: {e}", file=sys.stderr)
        return None


# ── Batch write with pacing ──────────────────────────────────────────────────
BATCH_SIZE = 400
BATCH_WINDOW_SECS = 900  # 15 min

def write_batch(conn, updates):
    """Write a list of (id, card_dict) to technique_references."""
    cur = conn.cursor()
    for rid, card in updates:
        cur.execute(
            "UPDATE technique_references SET recipe_card = %s WHERE id = %s",
            (json.dumps(card), rid)
        )
    conn.commit()
    cur.close()


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    conn_r = get_db_read()
    cur = conn_r.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Baseline
    cur.execute("SELECT COUNT(*) AS n FROM technique_references WHERE recipe_card IS NOT NULL")
    baseline = cur.fetchone()['n']
    print(f"Baseline recipe_card count: {baseline}")

    # Get pro_tips checksum for safety (confirm pro_tips not modified at end)
    cur.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) AS ck FROM technique_references")
    pt_checksum_before = cur.fetchone()['ck']

    # The 281
    cur.execute("""
        SELECT id, slug, name, pro_tips
        FROM technique_references
        WHERE pro_tips LIKE '%RECIPE:%' AND recipe_card IS NULL
        ORDER BY id
    """)
    unparsed = cur.fetchall()
    cur.close(); conn_r.close()

    print(f"Unparsed rows to recover: {len(unparsed)}")

    # ── Step 1: Extended parser ──
    parser_hits   = []
    parser_misses = []

    for row in unparsed:
        idx = row['pro_tips'].find('RECIPE:')
        blob = row['pro_tips'][idx:]
        card = parse_recipe_blob_extended(blob)
        if card:
            parser_hits.append((row['id'], row['slug'], row['name'], card))
        else:
            parser_misses.append(row)

    print(f"\nStep 1 — Extended parser:")
    print(f"  Recovered: {len(parser_hits)}")
    print(f"  Remaining for Claude: {len(parser_misses)}")

    # ── Step 2: Cost estimate ──
    if parser_misses:
        est_cost = estimate_claude_cost(len(parser_misses))
        print(f"\nStep 2 — Claude Haiku estimate for {len(parser_misses)} rows:")
        print(f"  Projected cost: ${est_cost:.2f}")
        if est_cost > 3.00:
            print("  OVER $3 BUDGET — stopping. Manual review needed.")
            # Write parser hits only
        else:
            print(f"  Under $3 — proceeding.")

    # ── Step 3: Claude sweep ──
    claude_hits   = []
    claude_skipped = []

    if parser_misses:
        if not ANTHROPIC_KEY:
            print("  No ANTHROPIC_API_KEY — skipping Claude sweep.")
            claude_skipped = parser_misses
        elif est_cost <= 3.00:
            print(f"\n  Sending {len(parser_misses)} rows to Haiku...")
            for i, row in enumerate(parser_misses):
                idx = row['pro_tips'].find('RECIPE:')
                excerpt = row['pro_tips'][idx:idx+2000]
                card = claude_extract(row['name'], excerpt)
                if card:
                    claude_hits.append((row['id'], row['slug'], row['name'], card))
                else:
                    claude_skipped.append(row)
                if (i + 1) % 10 == 0:
                    print(f"    {i+1}/{len(parser_misses)} rows processed...")
                time.sleep(0.3)  # gentle pacing

            print(f"  Claude recovered: {len(claude_hits)}")
            print(f"  Claude yielded null (no recipe): {len(claude_skipped)}")

    # ── Step 3: Write in batches ──
    all_updates = [(rid, card) for rid, slug, name, card in parser_hits + claude_hits]
    print(f"\nStep 3 — Writing {len(all_updates)} rows in batches ≤{BATCH_SIZE}")

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
            print(f"  Pacing — waiting for 15-min window...")
            time.sleep(BATCH_WINDOW_SECS)

    conn_w.close()

    # ── Step 4: Verification ──
    conn_r2 = get_db_read()
    cur2 = conn_r2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur2.execute("SELECT COUNT(*) AS n FROM technique_references WHERE recipe_card IS NOT NULL")
    final_count = cur2.fetchone()['n']

    # Confirm pro_tips unchanged
    cur2.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) AS ck FROM technique_references")
    pt_checksum_after = cur2.fetchone()['ck']

    # Random sample 5 recovered cards
    written_ids = [rid for rid, card in all_updates]
    sample_ids = random.sample(written_ids, min(5, len(written_ids)))
    cur2.execute(
        "SELECT id, slug, name, recipe_card FROM technique_references WHERE id = ANY(%s)",
        (sample_ids,)
    )
    samples = cur2.fetchall()

    # Spot-check list: 20 recovered slugs
    spot_slugs = [slug for rid, slug, name, card in (parser_hits + claude_hits)][:20]

    cur2.close(); conn_r2.close()

    # ── Report ──
    print("\n" + "="*60)
    print("VERIFICATION REPORT")
    print("="*60)
    print(f"recipe_card count before: {baseline}")
    print(f"recipe_card count after:  {final_count}")
    print(f"Net new:                  {final_count - baseline}")
    print(f"parser_hits:              {len(parser_hits)}")
    print(f"claude_hits:              {len(claude_hits)}")
    print(f"not recovered (null):     {len(claude_skipped)}")
    print(f"pro_tips checksum match:  {pt_checksum_before == pt_checksum_after}")
    print()
    print("5 random samples:")
    for row in samples:
        card = row['recipe_card']
        if isinstance(card, str):
            card = json.loads(card)
        print(f"  slug={row['slug']!r}")
        print(f"    serves={card.get('serves')!r} prep={card.get('prep')!r} total={card.get('total')!r}")
        print(f"    ingredients[0]={card['ingredients'][0]!r}")
        print(f"    steps[0]={card['steps'][0][:100]!r}")
    print()
    print("20-slug spot-check list for morning:")
    for i, s in enumerate(spot_slugs, 1):
        print(f"  {i:2d}. {s}")


if __name__ == "__main__":
    main()
