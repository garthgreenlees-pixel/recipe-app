"""
Backfill thumb_url for technique_references rows that have image_url but no thumb_url.
Idempotent + resumable: only processes WHERE image_url IS NOT NULL AND thumb_url IS NULL.
Run on the Fly machine: fly ssh console --command "python3 backfill_thumbs.py"
"""
import io
import os
import sys
import time

import fal_client
import psycopg2
import requests
from PIL import Image

WRITE_URL = os.environ.get("DATABASE_URL_WRITE") or os.environ.get("DATABASE_URL")
FAL_KEY = os.environ.get("FAL_KEY")

if not FAL_KEY:
    print("ABORT: FAL_KEY not set in environment.")
    sys.exit(1)

os.environ["FAL_KEY"] = FAL_KEY  # ensure fal_client picks it up

if not WRITE_URL:
    print("ABORT: No DATABASE_URL_WRITE or DATABASE_URL found.")
    sys.exit(1)


def make_thumbnail(image_url):
    """Fetch, resize to ≤440px wide, upload. Returns (thumb_url, orig_kb, thumb_kb, thumb_dims)."""
    resp = requests.get(image_url, timeout=15)
    resp.raise_for_status()
    orig_kb = len(resp.content) / 1024

    img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    img.thumbnail((440, 9999), Image.Resampling.LANCZOS)
    thumb_dims = img.size

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    thumb_kb = len(buf.getvalue()) / 1024

    url = fal_client.upload_image(img, format="jpeg")
    return url, orig_kb, thumb_kb, thumb_dims


conn = psycopg2.connect(WRITE_URL)
cur = conn.cursor()

cur.execute(
    "SELECT id, image_url FROM technique_references"
    " WHERE image_url IS NOT NULL AND thumb_url IS NULL ORDER BY id"
)
rows = cur.fetchall()
cur.close()

total = len(rows)
print(f"To process: {total} rows")

if total == 0:
    print("Nothing to do — all rows already have thumb_url.")
    conn.close()
    sys.exit(0)

succeeded = 0
failed = 0
proof_done = False
sample_sizes = []

for i, (row_id, image_url) in enumerate(rows):
    try:
        thumb_url, orig_kb, thumb_kb, dims = make_thumbnail(image_url)

        wcur = conn.cursor()
        wcur.execute(
            "UPDATE technique_references SET thumb_url = %s WHERE id = %s",
            (thumb_url, row_id)
        )
        conn.commit()
        wcur.close()

        succeeded += 1

        if not proof_done:
            print(f"\nPROOF (id={row_id}):")
            print(f"  original : {orig_kb:.1f} KB")
            print(f"  thumbnail: {thumb_kb:.1f} KB  {dims[0]}×{dims[1]}px")
            print(f"  savings  : {100*(1 - thumb_kb/orig_kb):.0f}%")
            print(f"  url      : {thumb_url[:80]}...")
            print()
            proof_done = True

        if len(sample_sizes) < 5:
            sample_sizes.append((row_id, orig_kb, thumb_kb, dims))

        if succeeded % 25 == 0:
            print(f"  [{succeeded}/{total}] processed so far …")

    except Exception as e:
        failed += 1
        if failed <= 5:
            print(f"  FAIL id={row_id}: {e}")

    # Small pause to avoid hammering fal CDN
    time.sleep(0.2)

conn.close()

print(f"\n=== BACKFILL COMPLETE ===")
print(f"  to-process : {total}")
print(f"  succeeded  : {succeeded}")
print(f"  failed/NULL: {failed}")
print()
print("Sample size comparisons:")
for (sid, ok, tk, d) in sample_sizes[:3]:
    print(f"  id={sid}: {ok:.1f} KB → {tk:.1f} KB  ({d[0]}×{d[1]})  savings {100*(1-tk/ok):.0f}%")
