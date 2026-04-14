---
title: "Replace generic sample recipes with curated Savourypot archive data"
date: 2026-03-03
category: data-migration
tags:
  - savourypot-archive
  - xml-to-json
  - recipe-data
  - fly-io-volumes
  - docker-image-bundling
  - seed-data
  - multi-app-deployment
severity: medium
time_to_resolve: "~1 hour"
components:
  - recipes.json
  - server.py (seed logic)
  - fly.toml (mount config)
  - extracted/ (image directory)
  - Dockerfile
symptoms:
  - 8 generic sample recipes with hasImage false do not showcase app image capabilities
  - Recipe grid shows text-only placeholders with no photos
  - App appears empty/demo-like rather than functional
root_cause: "Original seed data was hand-written placeholder recipes without images. Real recipe data existed in a Savourypot archive (.savouryarchive zip format) but had never been imported as seed data."
---

## Problem

Three Fly.io apps (provenance-tester-1, 2, 3) each had 8 generic sample recipes with `hasImage: false`. These text-only placeholders didn't showcase Provenance's core feature — displaying scanned cookbook recipes with images. The app looked empty rather than functional.

The user's Savourypot archive contained 598 real recipes with images, but in a different format (.savouryarchive with XML data).

## Solution

### Step 1: Located the archive

Found at `~/Desktop/Desktop Archive Feb 2026/Savoury pot backup/Savoury pot backup.savouryarchive`.

The `.savouryarchive` format is a **zip file** containing folders named `{UUID}.savourypot/`, each with:
- `data.xml` — recipe data in Savourypot XML schema
- `main.jpg` — full-size hero image
- `miniature.jpg` — thumbnail image

### Step 2: Built a scoring system

Python script parsed all 598 XML recipes and scored by:
- Image presence and file size (>10kb)
- Ingredient count (up to 15, weighted x2)
- Step count (up to 10, weighted x3)
- Average step length (detail indicator)
- Preamble quality (>20 chars)
- Tag count (>=2)
- English language preference

### Step 3: Curated 8 diverse recipes

Selected for cuisine diversity and technique variety:

| Recipe | Cuisine | Type | Image Size |
|--------|---------|------|-----------|
| Jerk Chicken | Caribbean | BBQ/Grilled | 789kb |
| Coq au Vin | French | Braise | 1.1MB |
| Arancini | Italian | Fried | 556kb |
| Pulled Jackfruit Tacos | Mexican/Vegan | Modern | 1.0MB |
| Japanese Mushroom Onigiri | Japanese | Snack | 751kb |
| Oven Fried Patatas Bravas | Spanish | Tapas | 546kb |
| Boston Cream Pie | American | Dessert | 352kb |
| Pasta with Caramelized Peppers | Italian | Weeknight | 933kb |

### Step 4: XML-to-JSON conversion

Key conversion challenges:

1. **Two XML root formats**: Some recipes use `<zrecipe>` directly, multilingual ones wrap in `<langs><zrecipe lang="en">`.

2. **Ingredient groups**: XML uses `<group>` elements interspersed between `<ingredient>` elements. Parser tracks `current_group` state:
   ```xml
   <ingredients>
     <group>Sauce</group>
     <ingredient name="soy sauce" unit="tbsp" count="2"/>
     <group>Main</group>
     <ingredient name="chicken" unit="kg" count="1"/>
   </ingredients>
   ```

3. **Nested info elements**: Some ingredients use `<info text="...">` child elements rather than `info` attributes.

4. **Compound tags**: Tags like `"jamaican chicken"` needed splitting into separate tags.

### Step 5: Image bundling

Copied `main.jpg` and `miniature.jpg` to `extracted/{UUID}/` in all 3 repo directories. Total ~6.7MB per app. The Dockerfile's `COPY . .` includes these in the Docker image.

### Step 6: Server seed logic update

Updated `server.py` to seed images alongside recipes.json:

```python
# Seed local data from repo on first run
if not RECIPES_FILE.exists():
    repo_dir = Path(__file__).parent
    repo_recipes = repo_dir / "recipes.json"
    if repo_recipes.exists():
        shutil.copy2(repo_recipes, RECIPES_FILE)
    # Also seed recipe images
    repo_extracted = repo_dir / "extracted"
    if repo_extracted.is_dir():
        for item in repo_extracted.iterdir():
            if item.is_dir():
                dest = EXTRACTED_DIR / item.name
                if not dest.exists():
                    shutil.copytree(item, dest)
```

### Step 7: Fly.io deployment fixes

**Apps 2 and 3 had volumes attached to machines but no `[[mounts]]` in fly.toml.** This caused `fly deploy` to fail with:
```
Warning! machine has a volume mounted but app config does not specify a volume.
Error: yes flag must be specified when not running interactively
```

Fix: Added `[[mounts]]` section to fly.toml:
```toml
[[mounts]]
  source = "provenance_data"
  destination = "/data"
```

Also updated apps 2 and 3 server.py to use `/data` volume paths (matching app 1) instead of local `Path(__file__).parent` paths, and removed the now-unnecessary image proxy logic.

### Step 8: Deployment and re-seeding

- **Apps 2 and 3**: `fly deploy --ha=false` — volumes were fresh/empty, seed logic ran automatically
- **App 1**: Volume had stale data. Required:
  1. Wake the machine: `curl https://provenance-tester-1.fly.dev/`
  2. Wipe old data: `fly ssh console -C "rm -f /data/recipes.json && rm -rf /data/extracted"`
  3. Restart: `fly machines restart <machine_id>`

### Step 9: Verification

```bash
# Verify recipes
curl -s https://provenance-tester-1.fly.dev/recipes.json | python3 -c "..."
# → 8 recipes, all hasImage=True

# Verify images
curl -s -o /dev/null -w "%{http_code}" \
  https://provenance-tester-1.fly.dev/images/AA9D735B-.../miniature.jpg
# → 200
```

## Prevention & Best Practices

### Keep fly.toml in sync with machine state
Before deploying, verify volumes match: `fly volumes list -a <app>`. If a machine has a volume, fly.toml must declare `[[mounts]]`.

### Seed all data, not just JSON
When seed logic copies recipes.json, it should also copy all supporting assets (images, etc.). Partial seeding leads to broken references.

### Consider seed versioning
A `SEED_VERSION` marker in the volume would allow re-seeding when seed data changes, without manual volume wipes. Currently requires SSH + restart.

### Keep app variants consistent
Apps 2 and 3 had divergent server.py (local paths, image proxy). This created maintenance burden. All apps should use the same data path strategy.

### Document archive formats
The .savouryarchive format (zip of `{UUID}.savourypot/` folders with `data.xml` + images) is proprietary. This document now serves as the reference.

## Related Documentation

- [PDF Import Timeout Optimization](/docs/solutions/performance-issues/pdf-import-timeout-optimization.md) — Server configuration, gunicorn timeouts
- [Beta Readiness Brainstorm](/docs/brainstorms/2026-03-03-beta-readiness-brainstorm.md) — Deployment and environment configuration
- `fly.toml` — Persistent data volume config (`provenance_data` at `/data`)
- `server.py:26-39` — Seed logic implementation
- `Dockerfile` — Container build (includes `extracted/` images via `COPY . .`)
