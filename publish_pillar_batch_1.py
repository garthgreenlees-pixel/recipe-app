#!/usr/bin/env python3
"""
Pillar Authoring Funnel — Pilot Batch 1 (publish pass)
Reads founder-approved results from /tmp/pillar_pilot_results.json,
writes sensory_tests + lives_or_dies + pillar_provenance to
technique_references for all 50 entries.

sensory_tests shape matches existing list-format:
  [{"cue": "...", "sense": "visual|auditory|...", "fail_indicator": "..."}]

NEVER touches the public recipes table.
"""
# ── Exclusions — entries that are not technique entries ────────────────────────
# These slugs are excluded from all pillar-authoring worklists.
EXCLUDED_SLUGS = [
    # Philosophy/manifesto, not a technique — founder ruling 2026-06-12
    "the-last-dish-provenance-original",
]

import os, sys, json
sys.stdout.reconfigure(line_buffering=True)
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


def detect_sense(cue):
    """Detect dominant sense from cue text."""
    cue_lower = cue.lower()[:40]
    if cue_lower.startswith('watch') or cue_lower.startswith('look'):
        return 'visual'
    if cue_lower.startswith('listen'):
        return 'auditory'
    if cue_lower.startswith('feel') or cue_lower.startswith('touch'):
        return 'tactile'
    if cue_lower.startswith('taste') or cue_lower.startswith('the cup hits'):
        return 'taste'
    if cue_lower.startswith('smell') or cue_lower.startswith('nose'):
        return 'olfactory'
    if 'watch' in cue_lower or 'colour' in cue_lower:
        return 'visual'
    if 'listen' in cue_lower or 'sound' in cue_lower:
        return 'auditory'
    if 'smell' in cue_lower or 'aroma' in cue_lower:
        return 'olfactory'
    if 'feel' in cue_lower or 'texture' in cue_lower:
        return 'tactile'
    if 'taste' in cue_lower or 'palate' in cue_lower or 'sip' in cue_lower:
        return 'taste'
    if 'terroir' in cue_lower or 'roasted' in cue_lower.lower():
        return 'olfactory'
    return 'visual'


def infer_anchor_fields(anchor_summary):
    """Infer which DB fields were used as anchor material."""
    a = anchor_summary.lower()
    fields = []
    if 'description' in a or 'distilled from' in a:
        fields.append('description')
    if 'key principles' in a or 'principles' in a:
        fields.append('key_principles')
    if 'common mistakes' in a or 'mistake' in a:
        fields.append('common_mistakes')
    if 'source' in a or 'codified' in a or 'escoffier' in a:
        fields.append('source_book')
    if 'origin' in a or 'tradition' in a:
        fields.append('origin')
    return fields or ['description', 'key_principles']


def main():
    with open('/tmp/pillar_pilot_results.json') as f:
        results = json.load(f)
    print(f"Loaded {len(results)} pilot results")

    # ── Build updates ──
    updates = []
    for r in results:
        sense = detect_sense(r['sensory_cue'])
        sensory_tests = [{
            "cue": r['sensory_cue'],
            "sense": sense,
            "fail_indicator": r['lives_or_dies']
        }]
        anchor_fields = infer_anchor_fields(r.get('anchor_summary', ''))
        grade = r.get('grade', 'GREEN').lower()

        prov_base = {
            "drafted_by": "claude-pilot-batch-1",
            "anchored_to": anchor_fields,
            "grade": grade,
            "reviewed_by": "founder",
            "review_date": "2026-06-11",
            "batch": "pilot-1"
        }
        pillar_prov = {
            "sensory_tests": dict(prov_base),
            "lives_or_dies": dict(prov_base)
        }
        if r['slug'] == 'brazilian-coffee-body-chocolate-and-scale':
            note = ("founder-approved: extraction temperature consistency "
                    "is standard practice across beans")
            pillar_prov['sensory_tests']['founder_note'] = note
            pillar_prov['lives_or_dies']['founder_note'] = note

        updates.append({
            'id': r['id'],
            'slug': r['slug'],
            'sensory_tests': sensory_tests,
            'lives_or_dies': r['lives_or_dies'],
            'pillar_provenance': pillar_prov,
        })

    # ── Baselines ──
    conn_r = psycopg2.connect(DB_READ, connect_timeout=10)
    cur_r = conn_r.cursor()

    cur_r.execute("SELECT COUNT(*) FROM technique_references "
                  "WHERE sensory_tests IS NOT NULL AND sensory_tests != 'null'::jsonb "
                  "AND sensory_tests::text NOT IN ('{}','[]')")
    baseline_sensory = cur_r.fetchone()[0]

    cur_r.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) "
                  "FROM technique_references")
    pt_ck_before = cur_r.fetchone()[0]

    cur_r.execute("SELECT MD5(STRING_AGG(COALESCE(recipe_card::text,''), '' ORDER BY id)) "
                  "FROM technique_references")
    rc_ck_before = cur_r.fetchone()[0]

    cur_r.execute("SELECT COUNT(*) FROM recipes")
    recipes_before = cur_r.fetchone()[0]
    cur_r.close(); conn_r.close()

    print(f"Baseline sensory_tests: {baseline_sensory}")

    # ── Write ──
    conn_w = psycopg2.connect(DB_WRITE, connect_timeout=10)
    conn_w.autocommit = False
    cur_w = conn_w.cursor()

    for u in updates:
        cur_w.execute("""
            UPDATE technique_references
            SET sensory_tests = %s,
                lives_or_dies = %s,
                pillar_provenance = %s
            WHERE id = %s
        """, (
            json.dumps(u['sensory_tests']),
            u['lives_or_dies'],
            json.dumps(u['pillar_provenance']),
            u['id']
        ))
    conn_w.commit()
    cur_w.close(); conn_w.close()
    print(f"Wrote {len(updates)} rows.")

    # ── Verify ──
    conn_v = psycopg2.connect(DB_READ, connect_timeout=10)
    cur_v = conn_v.cursor()

    cur_v.execute("SELECT COUNT(*) FROM technique_references "
                  "WHERE sensory_tests IS NOT NULL AND sensory_tests != 'null'::jsonb "
                  "AND sensory_tests::text NOT IN ('{}','[]')")
    after_sensory = cur_v.fetchone()[0]

    cur_v.execute("SELECT MD5(STRING_AGG(COALESCE(pro_tips,''), '' ORDER BY id)) "
                  "FROM technique_references")
    pt_ck_after = cur_v.fetchone()[0]

    cur_v.execute("SELECT MD5(STRING_AGG(COALESCE(recipe_card::text,''), '' ORDER BY id)) "
                  "FROM technique_references")
    rc_ck_after = cur_v.fetchone()[0]

    cur_v.execute("SELECT COUNT(*) FROM recipes")
    recipes_after = cur_v.fetchone()[0]
    cur_v.close(); conn_v.close()

    print(f"\nVerification:")
    print(f"  sensory_tests: {baseline_sensory} -> {after_sensory}")
    print(f"  pro_tips checksum match:    {pt_ck_before == pt_ck_after}")
    print(f"  recipe_card checksum match: {rc_ck_before == rc_ck_after}")
    print(f"  recipes table:              {recipes_before} -> {recipes_after}")


if __name__ == "__main__":
    main()
