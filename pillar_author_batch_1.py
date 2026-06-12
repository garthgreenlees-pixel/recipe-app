#!/usr/bin/env python3
"""
Pillar Authoring Funnel — Pilot Batch 1 (authoring pass)
Drafts sensory_tests cue + lives_or_dies line for 50 richest
recipe-bearing entries via Haiku, graded GREEN/AMBER.

Output: /tmp/pillar_pilot_results.json + tasting sheet at
~/Desktop/Provenance/Pillar_Pilot_Batch_1.md

NEVER modifies any database table. Read-only + file output.
"""
import os, sys, json, time, random, math, datetime
sys.stdout.reconfigure(line_buffering=True)

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
DB_READ = ENV.get('DATABASE_URL', '')
ANTHROPIC_KEY = ENV.get('ANTHROPIC_API_KEY', '')
HAIKU_MODEL = "claude-haiku-4-5-20251001"

# ── Exclusions — entries that are not technique entries ────────────────────────
# These slugs are excluded from all pillar-authoring worklists.
EXCLUDED_SLUGS = [
    # Philosophy/manifesto, not a technique — founder ruling 2026-06-12
    "the-last-dish-provenance-original",
]

AUTHOR_SYSTEM = """\
You are the Provenance Pillar Author. You distil two pillar lines from
an existing technique entry. You NEVER invent — you compress and
sharpen what the source text already says.

Return ONLY raw JSON (NO markdown fences). Keep ALL values SHORT
(under 40 words each). Keys: sensory_cue, lives_or_dies,
anchor_summary, grade, grade_note, least_sure.

grade is GREEN or AMBER. grade_note only if AMBER. least_sure only
if you had doubts.

Rules:
- Anchor ONLY to the data below.
- GREEN = famous technique, rich source text, consistent distillation.
- AMBER = thin source, obscure technique, or you had to stretch.
- Library voice: head chef at the pass. Short. Active. Present tense.
- Never use banned words: database, entries, CRM, AI, algorithm, etc.
- Return ONLY the JSON object."""


def select_candidates(n=50):
    import psycopg2, psycopg2.extras
    conn = psycopg2.connect(DB_READ, connect_timeout=10)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''
        SELECT DISTINCT ON (slug)
               id, slug, name, description, key_principles, common_mistakes,
               pro_tips, source_book, source, origin, flavour_context, recipe_card,
               LENGTH(COALESCE(description,'')) + LENGTH(COALESCE(key_principles,''))
                 + LENGTH(COALESCE(common_mistakes,'')) AS anchor_len
        FROM technique_references
        WHERE recipe_card IS NOT NULL
          AND (sensory_tests IS NULL OR sensory_tests = 'null'::jsonb
               OR sensory_tests::text IN ('{}','[]'))
          AND (lives_or_dies IS NULL OR lives_or_dies = '')
          AND slug NOT IN %s
        ORDER BY slug, anchor_len DESC
    ''', (tuple(EXCLUDED_SLUGS),))
    all_rows = cur.fetchall()
    all_rows.sort(key=lambda r: r['anchor_len'], reverse=True)
    cur.close(); conn.close()
    return all_rows[:n]


def classify_one(client, row):
    parts = [f"TECHNIQUE: {row['name']}"]
    if row.get('description'):
        parts.append(f"DESCRIPTION: {row['description'][:800]}")
    if row.get('key_principles'):
        parts.append(f"KEY PRINCIPLES: {row['key_principles'][:600]}")
    if row.get('common_mistakes'):
        parts.append(f"COMMON MISTAKES: {row['common_mistakes'][:400]}")
    if row.get('origin'):
        parts.append(f"ORIGIN: {row['origin'][:300]}")
    if row.get('source_book') or row.get('source'):
        src = row.get('source_book') or row.get('source') or ''
        parts.append(f"SOURCE: {src[:200]}")

    try:
        resp = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=200,
            system=AUTHOR_SYSTEM,
            messages=[{"role": "user", "content": "\n".join(parts)}],
            timeout=20.0,
        )
        raw = resp.content[0].text.strip()
        if raw.startswith('```'):
            raw = raw.split('```', 2)[1]
            if raw.startswith('json'):
                raw = raw[4:]
            raw = raw.rsplit('```', 1)[0].strip()
        data = json.loads(raw)
        return {
            "id": row['id'],
            "slug": row['slug'],
            "name": row['name'],
            "sensory_cue": data.get('sensory_cue', ''),
            "lives_or_dies": data.get('lives_or_dies', ''),
            "anchor_summary": data.get('anchor_summary', ''),
            "grade": data.get('grade', 'AMBER'),
            "grade_note": data.get('grade_note', ''),
            "least_sure": data.get('least_sure', ''),
        }
    except Exception as e:
        return {
            "id": row['id'],
            "slug": row['slug'],
            "name": row['name'],
            "sensory_cue": "",
            "lives_or_dies": "",
            "anchor_summary": "",
            "grade": "AMBER",
            "grade_note": f"API error: {str(e)[:80]}",
            "least_sure": "",
        }


def write_tasting_sheet(results, outpath):
    today = datetime.date.today().strftime("%Y-%m-%d")
    greens = [r for r in results if r['grade'] == 'GREEN']
    ambers = [r for r in results if r['grade'] != 'GREEN']

    lines = []
    lines.append(f"TASTING SHEET — Pilot Batch 1 — {today}. Read the greens. "
                 f"Note the NUMBERS of any entry to strike. Verdict = a list of "
                 f"numbers; nothing in this file needs editing.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## GREENS")
    lines.append("")

    for i, r in enumerate(greens, 1):
        lines.append(f"{i:02d} · {r['name'].upper()} ({r['slug']})")
        lines.append(f"SENSE:        {r['sensory_cue']}")
        lines.append(f"LIVES/DIES:   {r['lives_or_dies']}")
        lines.append(f"ANCHOR:       {r['anchor_summary']}")
        if r.get('least_sure'):
            lines.append(f"LEAST-SURE:   {r['least_sure']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## AMBERS")
    lines.append("")

    for i, r in enumerate(ambers, 1):
        lines.append(f"A{i} · {r['name'].upper()} ({r['slug']})")
        lines.append(f"SENSE:        {r['sensory_cue']}")
        lines.append(f"LIVES/DIES:   {r['lives_or_dies']}")
        lines.append(f"ANCHOR:       {r['anchor_summary']}")
        reason = r.get('grade_note', '') or 'No specific reason provided'
        lines.append(f"AMBER:        {reason}")
        if r.get('least_sure'):
            lines.append(f"LEAST-SURE:   {r['least_sure']}")
        lines.append("")

    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w') as f:
        f.write("\n".join(lines))


def main():
    import anthropic

    rows = select_candidates(50)
    print(f"Selected {len(rows)} candidates (anchor range: "
          f"{rows[-1]['anchor_len']}–{rows[0]['anchor_len']})")

    # Budget guard
    est_calls = len(rows)
    est_cost = (est_calls * 800 / 1e6) * 0.80 + (est_calls * 100 / 1e6) * 4.00
    print(f"Budget: {est_calls} calls, ~${est_cost:.3f}")
    if est_cost > 5.0:
        print("OVER $5 — STOPPING.")
        return

    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    results = []

    for i, row in enumerate(rows):
        result = classify_one(client, row)
        results.append(result)
        g = result['grade']
        print(f"{i+1:2d}/{len(rows)} {g:5s} {row['slug'][:55]}")
        time.sleep(0.15)

    # Save JSON
    with open('/tmp/pillar_pilot_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Write tasting sheet
    outpath = os.path.expanduser(
        "~/Desktop/Provenance/Pillar_Pilot_Batch_1.md")
    write_tasting_sheet(results, outpath)

    greens = sum(1 for r in results if r['grade'] == 'GREEN')
    ambers = sum(1 for r in results if r['grade'] != 'GREEN')
    print(f"\nDone. GREEN={greens} AMBER={ambers}")
    print(f"Tasting sheet: {outpath}")


if __name__ == "__main__":
    main()
