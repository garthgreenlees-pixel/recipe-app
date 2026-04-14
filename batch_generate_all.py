#!/usr/bin/env python3
"""
FULL batch image generation for Provenance.
Generates images for ALL recipes and ALL beverages that don't already have
a fal.media image. Uses the existing generate-image endpoints on the live server.

Photo Sashimi Standard. Dark editorial aesthetic. No stopping.
"""
import requests
import time
import json
import sys
from datetime import datetime

BASE_URL = "https://provenance.kitchen"
DELAY = 3  # seconds between generations
LOG_FILE = f"batch_image_log_{datetime.now().strftime('%Y%m%d_%H%M')}.json"


def get_api_key():
    """Fetch the PROVENANCE_API_KEY from the live server."""
    try:
        resp = requests.get(f"{BASE_URL}/api/config", timeout=10)
        if resp.status_code == 200:
            key = resp.json().get("apiKey", "")
            if key:
                print(f"  API key loaded ({key[:4]}...{key[-4:]})")
                return key
        print(f"  WARNING: Could not fetch API key (status {resp.status_code}) — requests may be rate-limited")
        return ""
    except Exception as e:
        print(f"  WARNING: Could not fetch API key: {e} — requests may be rate-limited")
        return ""


def get_all_recipes():
    """Fetch all P1000 recipes in one shot (max 700)."""
    resp = requests.get(f"{BASE_URL}/api/p1000-recipes", params={"per_page": 700, "page": 1}, timeout=30)
    if resp.status_code != 200:
        print(f"  Failed to fetch recipes: {resp.status_code}")
        return []
    data = resp.json()
    results = data.get("results", [])
    print(f"  Fetched {len(results)} recipes")
    return results


def get_all_beverages():
    """Fetch all beverage products via /api/beverage/products with pagination."""
    beverages = []
    offset = 0
    limit = 500
    while True:
        resp = requests.get(
            f"{BASE_URL}/api/beverage/products",
            params={"limit": limit, "offset": offset},
            timeout=30
        )
        if resp.status_code != 200:
            print(f"  Failed to fetch beverages at offset {offset}: {resp.status_code}")
            break
        batch = resp.json()
        if isinstance(batch, list):
            results = batch
        else:
            results = batch.get("products", batch.get("results", []))
        if not results:
            break
        beverages.extend(results)
        print(f"  Fetched offset {offset}: {len(results)} beverages (total so far: {len(beverages)})")
        if len(results) < limit:
            break
        offset += limit
    return beverages


def needs_image(item):
    """Return True if item has no fal.media image."""
    img = item.get("image_url") or ""
    return "fal.media" not in img


def generate_recipe_image(slug, api_key=""):
    """Call the generate-image endpoint for a technique (P1000 recipe)."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    try:
        resp = requests.post(
            f"{BASE_URL}/api/technique/{slug}/generate-image",
            json={},
            headers=headers,
            timeout=180
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "status": "success",
                "image_url": data.get("image_url", ""),
                "verified": data.get("verified"),
            }
        return {"status": "error", "code": resp.status_code, "message": resp.text[:200]}
    except requests.exceptions.Timeout:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def generate_beverage_image(product_id, api_key=""):
    """Call the generate-image endpoint for a beverage product."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    try:
        resp = requests.post(
            f"{BASE_URL}/api/beverage/{product_id}/generate-image",
            json={},
            headers=headers,
            timeout=180
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "status": "success",
                "image_url": data.get("image_url", ""),
                "verified": data.get("verified"),
            }
        return {"status": "error", "code": resp.status_code, "message": resp.text[:200]}
    except requests.exceptions.Timeout:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    start_time = datetime.now()

    print("=" * 70)
    print("PROVENANCE — FULL BATCH IMAGE GENERATION")
    print("Photo Sashimi Standard · Dark Editorial Aesthetic")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\nFetching API key...")
    api_key = get_api_key()

    results = {
        "started": start_time.isoformat(),
        "recipes": {"generated": [], "skipped": [], "failed": []},
        "beverages": {"generated": [], "skipped": [], "failed": []},
    }

    # ── PHASE 1: ALL RECIPES ──────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("PHASE 1: RECIPES")
    print("─" * 70)

    print("Fetching all recipes...")
    all_recipes = get_all_recipes()

    # Deduplicate by slug
    seen_slugs = set()
    recipes = []
    for r in all_recipes:
        slug = r.get("slug") or r.get("name", "").lower().replace(" ", "-")
        if slug and slug not in seen_slugs:
            seen_slugs.add(slug)
            recipes.append(r)

    need_gen = [r for r in recipes if needs_image(r)]
    already_have = len(recipes) - len(need_gen)
    print(f"Total unique recipes: {len(recipes)}")
    print(f"Already have fal.media images: {already_have}")
    print(f"Need generation: {len(need_gen)}")

    recipe_success = 0
    recipe_fail = 0

    for i, recipe in enumerate(need_gen):
        slug = recipe.get("slug") or recipe.get("name", "").lower().replace(" ", "-")
        name = recipe.get("name", slug)
        print(f"\n[RECIPE {i+1}/{len(need_gen)}] {name}")

        result = generate_recipe_image(slug, api_key=api_key)
        result["name"] = name
        result["slug"] = slug

        if result["status"] == "success":
            recipe_success += 1
            results["recipes"]["generated"].append(result)
            verified = "✓ verified" if result.get("verified") else "~ unverified"
            print(f"  ✓ Generated {verified}  {result.get('image_url','')[:70]}...")
        else:
            recipe_fail += 1
            results["recipes"]["failed"].append(result)
            print(f"  ✗ {result['status']}: {result.get('message', result.get('code', ''))[:80]}")

        # Progress checkpoint every 25
        if (i + 1) % 25 == 0:
            elapsed = (datetime.now() - start_time).total_seconds() / 60
            print(f"\n  ── Progress: {i+1}/{len(need_gen)} recipes — "
                  f"{recipe_success} ok, {recipe_fail} failed — "
                  f"{elapsed:.1f} min elapsed ──\n")
            # Save interim log
            with open(LOG_FILE, "w") as f:
                json.dump(results, f, indent=2)

        if i < len(need_gen) - 1:
            time.sleep(DELAY)

    # ── PHASE 2: ALL BEVERAGES ────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("PHASE 2: BEVERAGES")
    print("─" * 70)

    print("Fetching all beverages...")
    all_beverages = get_all_beverages()
    print(f"Total beverages: {len(all_beverages)}")

    bev_need_gen = [b for b in all_beverages if needs_image(b)]
    bev_already = len(all_beverages) - len(bev_need_gen)
    print(f"Already have fal.media images: {bev_already}")
    print(f"Need generation: {len(bev_need_gen)}")

    bev_success = 0
    bev_fail = 0

    for i, bev in enumerate(bev_need_gen):
        product_id = bev.get("id")
        name = bev.get("name", f"beverage-{product_id}")
        category = bev.get("category", "")

        if not product_id:
            print(f"\n[BEV {i+1}/{len(bev_need_gen)}] {name} — NO ID, skipping")
            results["beverages"]["failed"].append({"name": name, "status": "no_id"})
            bev_fail += 1
            continue

        print(f"\n[BEV {i+1}/{len(bev_need_gen)}] {name} ({category})")

        result = generate_beverage_image(product_id, api_key=api_key)
        result["name"] = name
        result["id"] = product_id
        result["category"] = category

        if result["status"] == "success":
            bev_success += 1
            results["beverages"]["generated"].append(result)
            verified = "✓ verified" if result.get("verified") else "~ unverified"
            print(f"  ✓ Generated {verified}  {result.get('image_url','')[:70]}...")
        else:
            bev_fail += 1
            results["beverages"]["failed"].append(result)
            print(f"  ✗ {result['status']}: {result.get('message', result.get('code', ''))[:80]}")

        # Progress checkpoint every 50
        if (i + 1) % 50 == 0:
            elapsed = (datetime.now() - start_time).total_seconds() / 60
            print(f"\n  ── Progress: {i+1}/{len(bev_need_gen)} beverages — "
                  f"{bev_success} ok, {bev_fail} failed — "
                  f"{elapsed:.1f} min elapsed ──\n")
            # Save interim log
            with open(LOG_FILE, "w") as f:
                json.dump(results, f, indent=2)

        if i < len(bev_need_gen) - 1:
            time.sleep(DELAY)

    # ── FINAL REPORT ─────────────────────────────────────────────────────────
    end_time = datetime.now()
    elapsed_min = (end_time - start_time).total_seconds() / 60
    total_generated = recipe_success + bev_success
    total_failed = recipe_fail + bev_fail
    estimated_cost = total_generated * 0.045

    results["completed"] = end_time.isoformat()
    results["elapsed_minutes"] = round(elapsed_min, 1)
    results["total_generated"] = total_generated
    results["total_failed"] = total_failed
    results["estimated_cost_usd"] = round(estimated_cost, 2)

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"""
RECIPES:
  Already had images:  {already_have}
  Generated:           {recipe_success}
  Failed:              {recipe_fail}
  Total:               {len(recipes)}

BEVERAGES:
  Already had images:  {bev_already}
  Generated:           {bev_success}
  Failed:              {bev_fail}
  Total:               {len(all_beverages)}

TOTALS:
  Generated:           {total_generated}
  Failed:              {total_failed}
  Estimated cost:      ${estimated_cost:.2f}
  Time:                {elapsed_min:.1f} minutes

Results saved to: {LOG_FILE}
""")

    if total_failed > 0:
        print("FAILED ITEMS:")
        for item in results["recipes"]["failed"][:20]:
            print(f"  [RECIPE] {item.get('name','?')}: {item.get('status','')} {item.get('message','')[:60]}")
        for item in results["beverages"]["failed"][:20]:
            print(f"  [BEV]    {item.get('name','?')}: {item.get('status','')} {item.get('message','')[:60]}")

    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {total_generated} images generated in {elapsed_min:.1f} minutes.")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
