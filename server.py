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
