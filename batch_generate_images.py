#!/usr/bin/env python3
"""
Batch AI image generation for Provenance.
Generates images for recipes (unsplash/missing) + 40 beverage products.
Photo Sashimi Standard · Dark Editorial Aesthetic
"""
import requests
import time
import json

BASE_URL = "https://provenance.kitchen"
DELAY = 6  # seconds between calls


def generate_recipe_image(slug):
    try:
        r = requests.post(
            f"{BASE_URL}/api/recipe/{slug}/generate-image",
            json={},
            timeout=180,
        )
        if r.status_code == 200:
            d = r.json()
            return {"status": "success", "image_url": d.get("image_url", ""),
                    "verified": d.get("verified"), "attempts": d.get("attempts")}
        return {"status": "error", "code": r.status_code, "message": r.text[:200]}
    except requests.exceptions.Timeout:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def generate_beverage_image(product_id):
    try:
        r = requests.post(
            f"{BASE_URL}/api/beverage/{product_id}/generate-image",
            json={},
            timeout=180,
        )
        if r.status_code == 200:
            d = r.json()
            return {"status": "success", "image_url": d.get("image_url", ""),
                    "verified": d.get("verified"), "attempts": d.get("attempts")}
        return {"status": "error", "code": r.status_code, "message": r.text[:200]}
    except requests.exceptions.Timeout:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_recipes_needing_images():
    r = requests.get(f"{BASE_URL}/api/curated-recipes", timeout=30)
    recipes = r.json().get("recipes", [])
    return [
        rec for rec in recipes
        if not rec.get("image_url")
        or "unsplash" in (rec.get("image_url") or "").lower()
    ]


def get_beverages_for_batch(limit=40):
    """Get first N beverage products — prioritise those without images."""
    import psycopg2
    import psycopg2.extras
    conn = psycopg2.connect(
        "postgres://provenance_reader:wRmgMcmVihfeW8Qaa1E9dMA-cz4SR-bW"
        "@localhost:15432/provenance_tester_1?sslmode=disable"
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, category, origin_country, image_url
        FROM beverage_products
        ORDER BY
            (image_url IS NULL) DESC,
            category,
            id
        LIMIT %s
    """, (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return rows


def main():
    print("=" * 62)
    print("PROVENANCE — BATCH IMAGE GENERATION")
    print("Photo Sashimi Standard · Dark Editorial Aesthetic")
    print("=" * 62)

    results = {"recipes": [], "beverages": []}

    # ── PHASE 1: RECIPES ────────────────────────────────────────
    print("\n── PHASE 1: RECIPES ──")
    recipes = get_recipes_needing_images()
    print(f"Found {len(recipes)} recipes needing images\n")

    for i, rec in enumerate(recipes):
        slug = rec["slug"]
        name = rec["name"]
        print(f"[R {i+1}/{len(recipes)}] {name}")
        result = generate_recipe_image(slug)
        result["name"] = name
        result["slug"] = slug
        results["recipes"].append(result)
        if result["status"] == "success":
            v = "✓ verified" if result.get("verified") else "~ unverified"
            print(f"  ✓ {v}  {result['image_url'][:70]}...")
        else:
            print(f"  ✗ {result['status']}: {result.get('message','')[:80]}")
        if i < len(recipes) - 1:
            time.sleep(DELAY)

    # ── PHASE 2: BEVERAGES ──────────────────────────────────────
    print("\n── PHASE 2: BEVERAGES ──")
    beverages = get_beverages_for_batch(40)
    print(f"Found {len(beverages)} beverages for generation\n")

    for i, bev in enumerate(beverages):
        pid = bev["id"]
        name = bev["name"]
        cat = bev["category"]
        existing = "HAS IMG" if bev.get("image_url") else "no img"
        print(f"[B {i+1}/{len(beverages)}] {name} [{cat}] ({existing})")
        result = generate_beverage_image(pid)
        result["name"] = name
        result["id"] = pid
        result["category"] = cat
        results["beverages"].append(result)
        if result["status"] == "success":
            v = "✓ verified" if result.get("verified") else "~ unverified"
            print(f"  ✓ {v}  {result['image_url'][:70]}...")
        else:
            print(f"  ✗ {result['status']}: {result.get('message','')[:80]}")
        if i < len(beverages) - 1:
            time.sleep(DELAY)

    # ── SUMMARY ─────────────────────────────────────────────────
    print("\n" + "=" * 62)
    print("RESULTS SUMMARY")
    print("=" * 62)

    r_ok = sum(1 for r in results["recipes"] if r["status"] == "success")
    r_fail = len(results["recipes"]) - r_ok
    b_ok = sum(1 for r in results["beverages"] if r["status"] == "success")
    b_fail = len(results["beverages"]) - b_ok
    total_ok = r_ok + b_ok

    print(f"\nRecipes:   {r_ok} generated, {r_fail} failed  (of {len(results['recipes'])})")
    print(f"Beverages: {b_ok} generated, {b_fail} failed  (of {len(results['beverages'])})")
    print(f"Total:     {total_ok} images generated")
    print(f"Est. cost: ~${total_ok * 0.045:.2f} (Flux Pro × $0.045)")

    if r_fail + b_fail > 0:
        print("\nFailed:")
        for r in results["recipes"] + results["beverages"]:
            if r["status"] != "success":
                label = r.get("slug") or r.get("id")
                print(f"  - {r['name']} ({label}): {r['status']} {r.get('message','')[:60]}")

    with open("batch_image_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nFull log → batch_image_results.json")


if __name__ == "__main__":
    main()
