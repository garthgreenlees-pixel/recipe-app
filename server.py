import os
import sentry_sdk

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,
)

import json
import uuid
import base64
import shutil
from pathlib import Path

import io
import psycopg2
import psycopg2.extras
import requests as http_requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
from flask_cors import CORS
import anthropic
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

load_dotenv()

app = Flask(__name__)
CORS(app)

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data" if Path("/data").is_dir() else "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

RECIPES_FILE = DATA_DIR / "recipes.json"
EXTRACTED_DIR = DATA_DIR / "extracted"
EXTRACTED_DIR.mkdir(exist_ok=True)

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

client = anthropic.Anthropic()

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def init_db():
    if not DATABASE_URL:
        return
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS technique_references (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            key_principles TEXT NOT NULL,
            common_mistakes TEXT NOT NULL,
            pro_tips TEXT NOT NULL,
            trigger_keywords JSONB NOT NULL,
            authority_tier INTEGER NOT NULL,
            related_techniques JSONB,
            tier_level VARCHAR(20) DEFAULT 'standard',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_technique_trigger_keywords
        ON technique_references USING GIN (trigger_keywords)
    """)
    # Add columns introduced after initial schema
    for stmt in [
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS source_book TEXT",
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS cross_cuisine_parallels JSONB DEFAULT '[]'::jsonb",
    ]:
        cur.execute(stmt)
    cur.close()
    conn.close()


init_db()


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
    image_dir = EXTRACTED_DIR / recipe_uuid
    filepath = image_dir / filename
    if filepath.is_file():
        return send_file(filepath)
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


# ─── Media type detection + HEIC conversion ──────────────────────────────────

def _detect_media_type(data: bytes) -> str:
    """Detect actual image format from file header bytes."""
    if data[:3] == b'\xff\xd8\xff':
        return "image/jpeg"
    if data[:4] == b'\x89PNG':
        return "image/png"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return "image/webp"
    if data[:4] in (b'GIF8',):
        return "image/gif"
    # HEIC/HEIF: ftyp box with heic/heix/mif1 brand
    if len(data) >= 12 and data[4:8] == b'ftyp':
        brand = data[8:12]
        if brand in (b'heic', b'heix', b'mif1', b'hevc'):
            return "image/heic"
    return "image/jpeg"


def _prepare_image(data: bytes) -> tuple[bytes, str]:
    """Detect format and convert HEIC to JPEG. Returns (image_bytes, media_type)."""
    media_type = _detect_media_type(data)
    if media_type == "image/heic":
        img = Image.open(io.BytesIO(data))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=92)
        return buf.getvalue(), "image/jpeg"
    return data, media_type


# ─── Scan (AI recipe extraction) ────────────────────────────────────────────

@app.route("/api/scan", methods=["POST"])
def scan_recipe():
    # Collect uploaded images
    images = []
    images_b64 = []
    images_media_types = []

    for key in sorted(request.files.keys()):
        f = request.files[key]
        raw = f.read()
        data, media_type = _prepare_image(raw)
        b64 = base64.b64encode(data).decode("utf-8")
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

    # Enhance steps automatically
    try:
        ingredient_strings = []
        for ing in recipe.get("ingredients", []):
            parts = []
            if ing.get("count"):
                parts.append(ing["count"])
            if ing.get("unit"):
                parts.append(ing["unit"])
            parts.append(ing.get("name", ""))
            if ing.get("info"):
                parts.append(f"({ing['info']})")
            ingredient_strings.append(" ".join(parts).strip())

        result = _enhance_recipe_steps(recipe["title"], ingredient_strings, recipe["steps"])
        if result:
            enhanced_strings, enhanced_objects = result
            recipe["original_steps"] = list(recipe["steps"])
            recipe["enhanced_steps"] = enhanced_objects
            recipe["steps"] = enhanced_strings
    except Exception:
        pass  # Enhancement failure doesn't block saving

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

    # Re-enhance if steps were updated
    if "steps" in data:
        try:
            ingredient_strings = []
            for ing in recipe.get("ingredients", []):
                parts = []
                if ing.get("count"):
                    parts.append(ing["count"])
                if ing.get("unit"):
                    parts.append(ing["unit"])
                parts.append(ing.get("name", ""))
                if ing.get("info"):
                    parts.append(f"({ing['info']})")
                ingredient_strings.append(" ".join(parts).strip())

            result = _enhance_recipe_steps(recipe["title"], ingredient_strings, recipe["steps"])
            if result:
                enhanced_strings, enhanced_objects = result
                recipe["original_steps"] = list(recipe["steps"])
                recipe["enhanced_steps"] = enhanced_objects
                recipe["steps"] = enhanced_strings
        except Exception:
            pass  # Enhancement failure doesn't block saving

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


# ─── Technique reference endpoints ───────────────────────────────────────────

@app.route("/api/techniques")
def list_techniques():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Convert datetime objects to strings for JSON serialization
    for row in rows:
        for key in ("created_at", "updated_at"):
            if row.get(key):
                row[key] = row[key].isoformat()
    return jsonify(rows)


def _match_techniques_for_step(step_text):
    """Return technique rows matching a step (internal helper, no HTTP)."""
    step_lower = step_text.lower()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    matches = []
    for row in rows:
        keywords = row.get("trigger_keywords", [])
        if any(kw.lower() in step_lower for kw in keywords):
            for key in ("created_at", "updated_at"):
                if row.get(key):
                    row[key] = row[key].isoformat()
            matches.append(row)
    return matches


@app.route("/api/techniques/match")
def match_techniques():
    step = request.args.get("step", "").strip()
    if not step:
        return jsonify(error="No step text provided"), 400
    return jsonify(_match_techniques_for_step(step))


@app.route("/api/techniques/bulk", methods=["POST"])
def bulk_create_techniques():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO technique_references
               (name, category, description, key_principles, common_mistakes, pro_tips,
                trigger_keywords, authority_tier, related_techniques, tier_level,
                source_book, cross_cuisine_parallels)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                e.get("name", ""),
                e.get("category", ""),
                e.get("description", ""),
                e.get("key_principles", ""),
                e.get("common_mistakes", ""),
                e.get("pro_tips", ""),
                json.dumps(e.get("trigger_keywords", [])),
                e.get("authority_tier", 1),
                json.dumps(e.get("related_techniques", [])),
                e.get("tier_level", "standard"),
                e.get("source_book"),
                json.dumps(e.get("cross_cuisine_parallels", [])),
            ),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


@app.route("/api/techniques/<int:technique_id>", methods=["GET"])
def get_technique(technique_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE id = %s", (technique_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify(error="Not found"), 404
    for key in ("created_at", "updated_at"):
        if row.get(key):
            row[key] = row[key].isoformat()
    return jsonify(row)


@app.route("/api/techniques/<int:technique_id>", methods=["PUT"])
def update_technique(technique_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM technique_references WHERE id = %s", (technique_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify(error="Not found"), 404
    cur.execute(
        """UPDATE technique_references SET
           name=%s, category=%s, description=%s, key_principles=%s,
           common_mistakes=%s, pro_tips=%s, trigger_keywords=%s,
           authority_tier=%s, related_techniques=%s, tier_level=%s,
           source_book=%s, cross_cuisine_parallels=%s,
           updated_at=NOW()
           WHERE id=%s""",
        (
            data.get("name", ""),
            data.get("category", ""),
            data.get("description", ""),
            data.get("key_principles", ""),
            data.get("common_mistakes", ""),
            data.get("pro_tips", ""),
            json.dumps(data.get("trigger_keywords", [])),
            data.get("authority_tier", 1),
            json.dumps(data.get("related_techniques", [])),
            data.get("tier_level", "standard"),
            data.get("source_book"),
            json.dumps(data.get("cross_cuisine_parallels", [])),
            technique_id,
        ),
    )
    cur.close()
    conn.close()
    return jsonify(success=True)


@app.route("/api/techniques/<int:technique_id>", methods=["DELETE"])
def delete_technique(technique_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM technique_references WHERE id = %s RETURNING id", (technique_id,))
    deleted = cur.fetchone()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify(error="Not found"), 404
    return jsonify(success=True)


@app.route("/admin/techniques")
def admin_techniques():
    return send_file("admin_techniques.html")


@app.route("/admin/technique-builder")
def admin_technique_builder():
    return send_file("admin_technique_builder.html")


# ─── Technique extraction (AI) ───────────────────────────────────────────────

TECHNIQUE_EXTRACTION_PROMPT = (
    "You are a culinary technique extraction engine working for Provenance. "
    "Read these cookbook pages and extract ONLY technique knowledge — not recipes, "
    "not ingredient lists, not serving suggestions. For each distinct technique you find, "
    "output valid JSON matching this exact schema: "
    '[{name, category, description, key_principles, common_mistakes, pro_tips, '
    'trigger_keywords (array of strings), authority_tier (integer 1-3), '
    'related_techniques (array of strings), tier_level (either \'standard\' or \'professional\')}]. '
    "Categories must be one of: heat_application, knife_skills, sauce_making, flavour_building, "
    "preparation, wet_heat, pastry_technique, finishing, grains_and_dough, "
    "presentation_and_philosophy, preparation_and_service. "
    "Include the book title and author context in descriptions. "
    "Extract the author's unique insights — what makes their explanation authoritative. "
    "If a page has no extractable technique knowledge, return an empty array []."
)


@app.route("/api/extract-techniques", methods=["POST"])
def extract_techniques():
    images = []
    for key in sorted(request.files.keys()):
        f = request.files[key]
        raw = f.read()
        data, media_type = _prepare_image(raw)
        b64 = base64.b64encode(data).decode("utf-8")
        images.append({"type": "image", "source": {"type": "base64", "media_type": media_type, "data": b64}})

    if not images:
        return jsonify(error="No images uploaded"), 400

    book_title = request.form.get("book_title", "").strip()

    user_text = "Extract all cooking techniques from these cookbook pages."
    if book_title:
        user_text = f"These pages are from: {book_title}. Extract all cooking techniques from them."

    content = images + [{"type": "text", "text": user_text}]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            system=TECHNIQUE_EXTRACTION_PROMPT,
            messages=[{"role": "user", "content": content}],
        )

        response_text = response.content[0].text.strip()
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response_text = "\n".join(lines)

        techniques = json.loads(response_text)
        if isinstance(techniques, dict):
            techniques = [techniques]
        # Coerce array-valued text fields to newline-joined strings
        for t in techniques:
            for field in ("description", "key_principles", "common_mistakes", "pro_tips"):
                if isinstance(t.get(field), list):
                    t[field] = "\n".join(str(s) for s in t[field])
        return jsonify(techniques)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Technique builder processing log ─────────────────────────────────────────

TECHNIQUE_BUILDER_LOG_FILE = DATA_DIR / "technique_builder_log.json"


@app.route("/api/technique-builder/log", methods=["GET"])
def get_technique_builder_log():
    if not TECHNIQUE_BUILDER_LOG_FILE.exists():
        return jsonify([])
    with open(TECHNIQUE_BUILDER_LOG_FILE, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/api/technique-builder/log", methods=["POST"])
def post_technique_builder_log():
    entry = request.get_json()
    log = []
    if TECHNIQUE_BUILDER_LOG_FILE.exists():
        with open(TECHNIQUE_BUILDER_LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
    log.append(entry)
    with open(TECHNIQUE_BUILDER_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    return jsonify(success=True), 201


# ─── Recipe enhancement pipeline ─────────────────────────────────────────────

ENHANCE_SYSTEM_PROMPT = (
    "You are Provenance, a culinary intelligence engine. You enhance recipe methods "
    "to professional standard. Write in the voice of a senior chef talking to a "
    "capable cook — direct, specific, never condescending. Always include temperatures, "
    "timing, and quantities where appropriate. For each step, return JSON with two "
    "fields: enhanced_step (the rewritten method step) and insight (a 1-2 sentence "
    "explanation of WHY the technique matters — this powers an optional learning feature)."
)


def _enhance_recipe_steps(title, ingredients, steps):
    """Enhance recipe steps using Claude and technique matching.

    Returns (enhanced_step_strings, enhanced_step_objects) or None on failure.
    """
    if not steps:
        return None

    ingredient_block = "\n".join(f"- {ing}" for ing in ingredients)
    enhanced_steps = []

    for i, step_text in enumerate(steps):
        matched = _match_techniques_for_step(step_text)

        technique_block = ""
        if matched:
            parts = []
            for t in matched:
                parts.append(
                    f"Technique: {t['name']}\n"
                    f"Key principles: {t['key_principles']}\n"
                    f"Common mistakes: {t['common_mistakes']}\n"
                    f"Pro tips: {t['pro_tips']}"
                )
            technique_block = (
                "\n\nMatched technique references:\n"
                + "\n---\n".join(parts)
            )

        user_prompt = (
            f"Recipe: {title}\n\n"
            f"Ingredients:\n{ingredient_block}\n\n"
            f"Original step {i + 1}: {step_text}"
            f"{technique_block}\n\n"
            "Enhance this step. Fix technique errors. Add missing temperatures, "
            "timing, quantities. If the step is vague, expand it into proper method. "
            "If it references a technique that should be multiple steps, split it. "
            'Return JSON: {"enhanced_step": "string", "insight": "string"}'
        )

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=ENHANCE_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            resp_text = response.content[0].text.strip()
            if resp_text.startswith("```"):
                lines = resp_text.split("\n")
                lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                resp_text = "\n".join(lines)
            result = json.loads(resp_text)
        except (json.JSONDecodeError, Exception) as e:
            result = {"enhanced_step": step_text, "insight": f"Enhancement failed: {e}"}

        enhanced_steps.append({
            "enhanced_step": result.get("enhanced_step", step_text),
            "insight": result.get("insight", ""),
            "matched_techniques": [t["name"] for t in matched],
        })

    enhanced_strings = [s["enhanced_step"] for s in enhanced_steps]
    return (enhanced_strings, enhanced_steps)


@app.route("/api/enhance-recipe", methods=["POST"])
def enhance_recipe():
    data = request.get_json()
    recipe_title = data.get("recipe_title", "Untitled")
    ingredients = data.get("ingredients", [])
    steps = data.get("steps", [])

    if not steps:
        return jsonify(error="No steps provided"), 400

    result = _enhance_recipe_steps(recipe_title, ingredients, steps)
    if result is None:
        return jsonify(error="Enhancement failed"), 500

    enhanced_strings, enhanced_steps = result
    return jsonify({
        "recipe_title": recipe_title,
        "ingredients": ingredients,
        "original_steps": steps,
        "enhanced_steps": enhanced_steps,
    })


@app.route("/test/enhance")
def test_enhance_page():
    return send_file("test_enhance.html")


@app.route("/test/enhance-barramundi")
def test_enhance_barramundi_page():
    return send_file("test_enhance_barramundi.html")


# ─── Sentry test route ───────────────────────────────────────────────────────

@app.route("/debug-sentry")
def trigger_error():
    division_by_zero = 1 / 0


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
