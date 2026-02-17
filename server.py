import os
import json
import uuid
import base64
import shutil
from pathlib import Path

import requests as http_requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
from flask_cors import CORS
import anthropic

PRODUCTION_HOST = "https://garth-recipe-browser.fly.dev"

load_dotenv()

app = Flask(__name__)
CORS(app)

RECIPES_FILE = Path(__file__).parent / "recipes.json"
EXTRACTED_DIR = Path(__file__).parent / "extracted"
EXTRACTED_DIR.mkdir(exist_ok=True)

client = anthropic.Anthropic()


# ─── Static files ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/recipes.json")
def recipes_json():
    return send_file(RECIPES_FILE, mimetype="application/json")


# ─── Image serving ───────────────────────────────────────────────────────────

@app.route("/images/<recipe_uuid>/<filename>")
def serve_image(recipe_uuid, filename):
    # Serve locally if available
    image_dir = EXTRACTED_DIR / recipe_uuid
    filepath = image_dir / filename
    if filepath.is_file():
        return send_file(filepath)

    # Proxy from production server and cache locally
    remote_url = f"{PRODUCTION_HOST}/images/{recipe_uuid}/{filename}"
    try:
        resp = http_requests.get(remote_url, timeout=10)
        if resp.status_code == 200:
            image_dir.mkdir(parents=True, exist_ok=True)
            filepath.write_bytes(resp.content)
            return Response(resp.content, content_type=resp.headers.get("Content-Type", "image/jpeg"))
    except Exception:
        pass
    return jsonify(error="Not found"), 404


# ─── Helpers ─────────────────────────────────────────────────────────────────

def load_recipes():
    if not RECIPES_FILE.exists():
        return []
    with open(RECIPES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_recipes(recipes):
    with open(RECIPES_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)


def save_hero_image(recipe_uuid, image_b64):
    """Save a base64-encoded image as the hero (main + miniature) for a recipe."""
    image_dir = EXTRACTED_DIR / recipe_uuid
    image_dir.mkdir(parents=True, exist_ok=True)

    image_bytes = base64.b64decode(image_b64)
    (image_dir / "main.jpg").write_bytes(image_bytes)
    (image_dir / "miniature.jpg").write_bytes(image_bytes)


# ─── Scan (AI recipe extraction) ────────────────────────────────────────────

@app.route("/api/scan", methods=["POST"])
def scan_recipe():
    # Collect uploaded images
    images = []
    images_b64 = []
    images_media_types = []

    for key in sorted(request.files.keys()):
        f = request.files[key]
        data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        media_type = f.content_type or "image/jpeg"
        images.append({"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}})
        images_b64.append(b64)
        images_media_types.append(media_type)

    if not images:
        return jsonify(error="No images uploaded"), 400

    prompt_text = """Extract the recipe from these cookbook page images. Return a JSON object with these fields:
{
  "title": "Recipe title",
  "preamble": "Brief description or headnote",
  "tags": ["tag1", "tag2"],
  "time": {"active": "20 mins", "total": "1 hour"},
  "servings": [{"count": "4", "unit": "serve"}],
  "ingredients": [
    {"count": "2", "unit": "cups", "name": "flour", "info": "sifted", "group": ""}
  ],
  "steps": ["Step 1 text", "Step 2 text"]
}

Rules:
- Extract ALL ingredients with precise quantities
- Include ALL steps in full detail
- Use lowercase tags
- Infer reasonable tags from the recipe type (e.g. "dessert", "vegetarian", "italian")
- If there are ingredient groups (e.g. "For the sauce"), set the group field
- Return ONLY valid JSON, no markdown fences"""

    content = images + [{"type": "text", "text": prompt_text}]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": content}],
        )

        response_text = response.content[0].text.strip()
        # Strip markdown fences if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = lines[1:]  # remove opening fence
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        recipe = json.loads(response_text)
        recipe["_images_b64"] = images_b64
        recipe["_images_media_types"] = images_media_types
        return jsonify(recipe)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Classify pages (PDF import) ────────────────────────────────────────────

@app.route("/api/classify-pages", methods=["POST"])
def classify_pages():
    data = request.get_json()
    images_data = data.get("images", [])

    if not images_data:
        return jsonify(error="No images provided"), 400

    content = []
    for i, img in enumerate(images_data):
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": img.get("media_type", "image/jpeg"),
                "data": img["data"],
            },
        })
        content.append({"type": "text", "text": f"[Page {i}]"})

    content.append({
        "type": "text",
        "text": """Classify these cookbook pages. Identify which pages contain recipes and group multi-page recipes together.

Return a JSON object:
{
  "recipes": [
    {"title": "Recipe Name", "pages": [0, 1]},
    {"title": "Another Recipe", "pages": [2]}
  ],
  "skipped_pages": [3, 4]
}

Rules:
- pages array uses 0-based indices matching the [Page N] labels above
- Group consecutive pages that belong to the same recipe
- Skip table of contents, intro pages, ads, etc.
- Return ONLY valid JSON, no markdown fences""",
    })

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": content}],
        )

        response_text = response.content[0].text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        result = json.loads(response_text)
        return jsonify(result)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Import from URL ─────────────────────────────────────────────────────────

import re as _re

def _extract_jsonld_recipe(html_text):
    """Try to extract a Recipe from JSON-LD structured data in the HTML."""
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    blocks = _re.findall(pattern, html_text, _re.DOTALL | _re.IGNORECASE)

    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue

        items = []
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            if data.get("@graph"):
                items = data["@graph"]
            else:
                items = [data]

        for item in items:
            if not isinstance(item, dict):
                continue
            item_type = item.get("@type", "")
            if isinstance(item_type, list):
                item_type = " ".join(item_type)
            if "Recipe" in item_type:
                return item
    return None


def _parse_duration(iso_str):
    """Convert ISO 8601 duration (PT1H30M) to readable string."""
    if not iso_str or not isinstance(iso_str, str):
        return ""
    m = _re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_str, _re.IGNORECASE)
    if not m:
        return iso_str
    hours, mins, secs = m.groups()
    parts = []
    if hours:
        parts.append(f"{hours} hr{'s' if int(hours) > 1 else ''}")
    if mins:
        parts.append(f"{mins} min")
    if secs and not parts:
        parts.append(f"{secs} sec")
    return " ".join(parts) if parts else iso_str


def _jsonld_to_recipe(ld):
    """Convert a JSON-LD Recipe object to our app's recipe format."""
    ingredients = []
    for ing_str in (ld.get("recipeIngredient") or []):
        ingredients.append({
            "count": "",
            "unit": "",
            "name": str(ing_str).strip(),
            "info": "",
            "group": "",
        })

    steps = []
    raw_steps = ld.get("recipeInstructions") or []
    if isinstance(raw_steps, str):
        steps = [s.strip() for s in raw_steps.split('\n') if s.strip()]
    else:
        for step in raw_steps:
            if isinstance(step, str):
                steps.append(step.strip())
            elif isinstance(step, dict):
                if step.get("@type") == "HowToSection":
                    for sub in (step.get("itemListElement") or []):
                        if isinstance(sub, dict):
                            steps.append(sub.get("text", str(sub)))
                        else:
                            steps.append(str(sub))
                else:
                    steps.append(step.get("text", str(step)))

    tags = []
    for field in ["recipeCategory", "recipeCuisine", "keywords"]:
        val = ld.get(field)
        if isinstance(val, str):
            tags.extend([t.strip().lower() for t in val.split(",") if t.strip()])
        elif isinstance(val, list):
            tags.extend([str(t).strip().lower() for t in val if t])
    tags = list(dict.fromkeys(tags))[:10]

    servings = []
    yield_val = ld.get("recipeYield")
    if yield_val:
        if isinstance(yield_val, list):
            yield_val = yield_val[0]
        servings = [{"count": str(yield_val), "unit": "serve"}]

    image_url = ""
    img = ld.get("image")
    if isinstance(img, str):
        image_url = img
    elif isinstance(img, list) and img:
        image_url = img[0] if isinstance(img[0], str) else (img[0].get("url", "") if isinstance(img[0], dict) else "")
    elif isinstance(img, dict):
        image_url = img.get("url", "")

    return {
        "title": ld.get("name", "Untitled"),
        "preamble": ld.get("description", ""),
        "tags": tags,
        "time": {
            "active": _parse_duration(ld.get("prepTime", "")),
            "total": _parse_duration(ld.get("totalTime", "")),
        },
        "servings": servings,
        "ingredients": ingredients,
        "steps": steps,
        "source": {"name": "", "address": ""},
        "_image_url": image_url,
    }


@app.route("/api/import-url", methods=["POST"])
def import_url():
    data = request.get_json()
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify(error="No URL provided"), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = http_requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        html_text = resp.text
    except Exception as e:
        return jsonify(error=f"Could not fetch URL: {e}"), 400

    # Try JSON-LD extraction first (fast, no API cost)
    ld_recipe = _extract_jsonld_recipe(html_text)
    if ld_recipe:
        recipe = _jsonld_to_recipe(ld_recipe)
        recipe["source"] = {"name": "", "address": url}
        recipe["_method"] = "jsonld"

        # Try to download hero image, fall back to passing URL to browser
        if recipe.get("_image_url"):
            hero_downloaded = False
            try:
                img_resp = http_requests.get(recipe["_image_url"], headers=headers, timeout=10)
                if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                    recipe["_hero_b64"] = base64.b64encode(img_resp.content).decode("utf-8")
                    hero_downloaded = True
            except Exception:
                pass
            if not hero_downloaded:
                recipe["_hero_url"] = recipe["_image_url"]
            del recipe["_image_url"]

        return jsonify(recipe)

    # Fallback: send page text to Claude for extraction
    text_only = _re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=_re.DOTALL | _re.IGNORECASE)
    text_only = _re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=_re.DOTALL | _re.IGNORECASE)
    text_only = _re.sub(r'<[^>]+>', ' ', text_only)
    text_only = _re.sub(r'\s+', ' ', text_only).strip()[:8000]

    prompt = f"""Extract the recipe from this webpage text. Return a JSON object with these fields:
{{
  "title": "Recipe title",
  "preamble": "Brief description or headnote",
  "tags": ["tag1", "tag2"],
  "time": {{"active": "20 mins", "total": "1 hour"}},
  "servings": [{{"count": "4", "unit": "serve"}}],
  "ingredients": [
    {{"count": "2", "unit": "cups", "name": "flour", "info": "sifted", "group": ""}}
  ],
  "steps": ["Step 1 text", "Step 2 text"]
}}

Rules:
- Extract ALL ingredients with precise quantities
- Include ALL steps in full detail
- Use lowercase tags
- Return ONLY valid JSON, no markdown fences

Webpage text:
{text_only}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = response.content[0].text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        recipe = json.loads(response_text)
        recipe["source"] = {"name": "", "address": url}
        recipe["_method"] = "ai"
        return jsonify(recipe)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Image proxy (for URL import hero images) ───────────────────────────────

@app.route("/api/proxy-image")
def proxy_image():
    url = request.args.get("url", "").strip()
    if not url:
        return jsonify(error="No URL"), 400
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = http_requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "image/jpeg")
        return Response(resp.content, content_type=ct)
    except Exception:
        return jsonify(error="Failed to fetch image"), 400


# ─── CRUD endpoints ─────────────────────────────────────────────────────────

@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    recipes = load_recipes()

    recipe_uuid = str(uuid.uuid4()).upper()
    recipe = {
        "uuid": recipe_uuid,
        "title": data.get("title", "Untitled"),
        "lang": "",
        "version": "1",
        "favourite": False,
        "rating": 0.0,
        "updated": "",
        "importDate": "",
        "hasImage": False,
        "time": data.get("time", {"active": "", "total": ""}),
        "cooking": {"times": "0", "last": ""},
        "tags": data.get("tags", []),
        "servings": data.get("servings", []),
        "ingredients": data.get("ingredients", []),
        "steps": data.get("steps", []),
        "preamble": data.get("preamble", ""),
        "source": data.get("source", {"name": "", "address": ""}),
    }

    # Handle hero image from scanned images
    images_b64 = data.get("_images_b64", [])
    images_media_types = data.get("_images_media_types", [])
    hero_index = data.get("_hero_index", 0)
    hero_custom_b64 = data.get("_hero_custom_b64")

    if hero_custom_b64:
        save_hero_image(recipe_uuid, hero_custom_b64)
        recipe["hasImage"] = True
    elif images_b64 and 0 <= hero_index < len(images_b64):
        save_hero_image(recipe_uuid, images_b64[hero_index])
        recipe["hasImage"] = True

    # Save all scanned page images
    if images_b64:
        image_dir = EXTRACTED_DIR / recipe_uuid
        image_dir.mkdir(parents=True, exist_ok=True)
        for i, (b64, mt) in enumerate(zip(images_b64, images_media_types)):
            ext = "jpg" if "jpeg" in mt or "jpg" in mt else "png"
            (image_dir / f"page_{i}.{ext}").write_bytes(base64.b64decode(b64))

    recipes.append(recipe)
    save_recipes(recipes)
    return jsonify(recipe), 201


@app.route("/api/recipes/<recipe_uuid>", methods=["PUT"])
def update_recipe(recipe_uuid):
    data = request.get_json()
    recipes = load_recipes()

    idx = next((i for i, r in enumerate(recipes) if r["uuid"] == recipe_uuid), None)
    if idx is None:
        return jsonify(error="Recipe not found"), 404

    recipe = recipes[idx]

    # Update fields
    for field in ["title", "preamble", "tags", "time", "servings", "ingredients", "steps", "source"]:
        if field in data:
            recipe[field] = data[field]

    # Handle hero image update
    hero_b64 = data.get("_hero_b64")
    if hero_b64:
        save_hero_image(recipe_uuid, hero_b64)
        recipe["hasImage"] = True

    recipes[idx] = recipe
    save_recipes(recipes)
    return jsonify(recipe)


@app.route("/api/recipes/<recipe_uuid>", methods=["DELETE"])
def delete_recipe(recipe_uuid):
    recipes = load_recipes()

    idx = next((i for i, r in enumerate(recipes) if r["uuid"] == recipe_uuid), None)
    if idx is None:
        return jsonify(error="Recipe not found"), 404

    recipes.pop(idx)
    save_recipes(recipes)

    # Remove images
    image_dir = EXTRACTED_DIR / recipe_uuid
    if image_dir.is_dir():
        shutil.rmtree(image_dir)

    return jsonify(success=True)


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
