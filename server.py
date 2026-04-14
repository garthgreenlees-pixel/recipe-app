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
import html as html_mod
import base64
import secrets
import shutil
import collections
import threading
import queue as _queue
from pathlib import Path

import io
import time as _time
import re as _re
import urllib.parse as _urllib_parse
import psycopg2
import psycopg2.extras
import requests as http_requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file, Response, render_template, render_template_string, g, session, redirect, url_for, flash
from flask_cors import CORS
import anthropic
import fal_client
import stripe
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * 30  # 30 days

# ─── Stripe ───────────────────────────────────────────────────────────────────

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

PRICE_MAP = {
    "kitchen": {
        "monthly": os.environ.get("STRIPE_PRICE_KITCHEN_MONTHLY"),
        "yearly":  os.environ.get("STRIPE_PRICE_KITCHEN_YEARLY"),
    },
    "library": {
        "monthly": os.environ.get("STRIPE_PRICE_LIBRARY_MONTHLY"),
        "yearly":  os.environ.get("STRIPE_PRICE_LIBRARY_YEARLY"),
    },
    "profession": {
        "monthly": os.environ.get("STRIPE_PRICE_PROFESSION_MONTHLY"),
        "yearly":  os.environ.get("STRIPE_PRICE_PROFESSION_YEARLY"),
    },
    "trade": {
        "monthly": os.environ.get("STRIPE_PRICE_TRADE_MONTHLY"),
        "yearly":  os.environ.get("STRIPE_PRICE_TRADE_YEARLY"),
    },
}

TIER_HIERARCHY = ["free", "kitchen", "library", "profession", "trade"]

# ─── Jinja2 Filters ───────────────────────────────────────────────────────────

import re as _re
from markupsafe import Markup, escape as _escape

# Cuisines that have browse pages with meaningful results
_LINKABLE_CUISINES = [
    'Cantonese', 'Sichuan', 'Italian', 'Indian', 'Mexican', 'Japanese',
    'Chinese', 'French', 'Korean', 'Thai', 'Vietnamese',
]
_CUISINE_PATTERN = _re.compile(
    r'\b(' + '|'.join(_re.escape(c) for c in _LINKABLE_CUISINES) + r')\b'
)

@app.template_filter('linkify_cuisines')
def linkify_cuisines_filter(text):
    """Wrap known cuisine names in technique browse links. Safe for HTML output."""
    if not text:
        return text
    escaped = str(_escape(text))
    def _replace(m):
        name = m.group(1)
        return (f'<a href="/techniques/browse?cuisine={name}" '
                f'style="color:inherit;text-decoration:underline;'
                f'text-decoration-color:rgba(201,168,76,0.3)">{name}</a>')
    return Markup(_CUISINE_PATTERN.sub(_replace, escaped))


CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://provenance.kitchen",
            "https://www.provenance.kitchen",
            "https://provenance-tester-1.fly.dev",
        ]
    }
})

# ─── API Security ─────────────────────────────────────────────────────────────

PROVENANCE_API_KEY = os.environ.get("PROVENANCE_API_KEY", "")

# ── Rate limiter: 10 req/min/IP for unauthenticated access ────────────────────
_RL_STORE: dict = collections.defaultdict(list)
_RL_LOCK = threading.Lock()
RL_MAX = 10
RL_WINDOW = 60  # seconds

# ── Scrape detection: >100 unique technique pages/hour → 24-hour block ────────
_SCRAPE_TRACKER: dict = {}   # ip -> (hour_bucket, set_of_slugs)
_SCRAPE_LOCK = threading.Lock()
SCRAPE_LIMIT = 100
SCRAPE_BLOCK_HOURS = 24

# ── Blocked IPs: ip -> expiry epoch (0 = permanent) ──────────────────────────
_BLOCKED_IPS: dict = {}
_BLOCK_LOCK = threading.Lock()

# ── Async access log queue ────────────────────────────────────────────────────
_LOG_QUEUE: _queue.Queue = _queue.Queue()

def _log_worker():
    while True:
        try:
            ip, endpoint, api_key_hint, code = _LOG_QUEUE.get(timeout=5)
            write_url = DATABASE_URL_WRITE if DATABASE_URL_WRITE else DATABASE_URL
            if write_url:
                try:
                    conn = psycopg2.connect(write_url)
                    conn.autocommit = True
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO api_access_log (ip_address, endpoint, api_key_used, response_code)"
                        " VALUES (%s, %s, %s, %s)",
                        (ip, endpoint, api_key_hint, code),
                    )
                    cur.close()
                    conn.close()
                except Exception:
                    pass
            _LOG_QUEUE.task_done()
        except _queue.Empty:
            continue

_log_thread = threading.Thread(target=_log_worker, daemon=True)
_log_thread.start()

# ── Trusted referrer domains ──────────────────────────────────────────────────
_TRUSTED_HOSTS = {"provenance.kitchen", "www.provenance.kitchen", "provenance-tester-1.fly.dev"}


def _get_client_ip() -> str:
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _has_valid_api_key() -> bool:
    return bool(PROVENANCE_API_KEY and request.headers.get("X-API-Key") == PROVENANCE_API_KEY)


def _has_valid_referrer() -> bool:
    """True if the request Referer comes from a trusted domain."""
    referer = request.headers.get("Referer", "")
    if not referer:
        return False
    try:
        host = _urllib_parse.urlparse(referer).netloc.lower().split(":")[0]
        return host in _TRUSTED_HOSTS
    except Exception:
        return False


def _is_blocked(ip: str) -> bool:
    with _BLOCK_LOCK:
        expiry = _BLOCKED_IPS.get(ip)
        if expiry is None:
            return False
        if expiry == 0 or _time.time() < expiry:
            return True
        del _BLOCKED_IPS[ip]
        return False


def _block_ip(ip: str, permanent: bool = False, hours: int = SCRAPE_BLOCK_HOURS):
    expiry = 0 if permanent else (_time.time() + hours * 3600)
    with _BLOCK_LOCK:
        _BLOCKED_IPS[ip] = expiry


def _track_scrape(ip: str, slug: str) -> bool:
    """Record a unique page visit. Returns True when the IP hits SCRAPE_LIMIT."""
    hour = int(_time.time() // 3600)
    with _SCRAPE_LOCK:
        entry = _SCRAPE_TRACKER.get(ip)
        if entry is None or entry[0] != hour:
            _SCRAPE_TRACKER[ip] = (hour, {slug})
            return False
        slugs = entry[1]
        slugs.add(slug)
        return len(slugs) >= SCRAPE_LIMIT


def _rl_consume(ip: str):
    """Consume one rate-limit slot. Returns (allowed, remaining, reset_epoch)."""
    now = _time.time()
    cutoff = now - RL_WINDOW
    with _RL_LOCK:
        ts = _RL_STORE[ip]
        ts[:] = [t for t in ts if t > cutoff]
        if len(ts) >= RL_MAX:
            reset_at = int(ts[0] + RL_WINDOW)
            return False, 0, reset_at
        ts.append(now)
        remaining = RL_MAX - len(ts)
        reset_at = int(now + RL_WINDOW)
        return True, remaining, reset_at


@app.before_request
def enforce_security():
    """Global security: block detection, scrape tracking, bulk auth, rate limiting."""
    ip = _get_client_ip()

    # ── Blocked IP ────────────────────────────────────────────────────────────
    if _is_blocked(ip):
        return jsonify(error="Access denied"), 403

    # ── HTML technique pages: scrape tracking only ────────────────────────────
    for _html_prefix in ("/technique/", "/why/", "/beyond/"):
        if request.path.startswith(_html_prefix):
            slug = request.path[len(_html_prefix):]
            if slug and _track_scrape(ip, "html:" + slug):
                _block_ip(ip, hours=SCRAPE_BLOCK_HOURS)
                return jsonify(error="Access denied — automated access detected"), 403
            return

    # ── Only /api/ routes below ───────────────────────────────────────────────
    if not request.path.startswith("/api/"):
        return

    # Config endpoint: always reachable for key bootstrapping
    if request.path == "/api/config":
        return

    # Bulk endpoints always require a valid API key
    if request.path.endswith("/bulk") and not _has_valid_api_key():
        return jsonify(error="API key required for bulk operations"), 403

    # Authenticated or trusted referrer: bypass rate limit, still scrape-track
    if _has_valid_api_key() or _has_valid_referrer():
        g.rl_active = False
        if request.path.startswith("/api/techniques/"):
            slug = request.path[len("/api/techniques/"):]
            if slug and not slug.isdigit() and _track_scrape(ip, "api:" + slug):
                _block_ip(ip, hours=SCRAPE_BLOCK_HOURS)
        return

    # Unauthenticated: rate limit
    allowed, remaining, reset_at = _rl_consume(ip)
    g.rl_active = True
    g.rl_remaining = remaining
    g.rl_reset = reset_at
    if not allowed:
        resp = jsonify(
            error="Rate limit exceeded",
            message=(
                "Unauthenticated access is limited to 10 requests per minute. "
                "Include a valid X-API-Key header for full access."
            ),
            retry_after=max(0, reset_at - int(_time.time())),
        )
        resp.status_code = 429
        resp.headers["X-RateLimit-Limit"] = str(RL_MAX)
        resp.headers["X-RateLimit-Remaining"] = "0"
        resp.headers["X-RateLimit-Reset"] = str(reset_at)
        resp.headers["Retry-After"] = str(max(0, reset_at - int(_time.time())))
        return resp

    # Scrape-track unauthenticated technique slug requests
    if request.path.startswith("/api/techniques/"):
        slug = request.path[len("/api/techniques/"):]
        if slug and not slug.isdigit() and _track_scrape(ip, "api:" + slug):
            _block_ip(ip, hours=SCRAPE_BLOCK_HOURS)


@app.after_request
def finalize_response(response):
    """Add rate-limit headers and queue an access log entry for every /api/ request."""
    if getattr(g, "rl_active", False):
        response.headers["X-RateLimit-Limit"] = str(RL_MAX)
        response.headers["X-RateLimit-Remaining"] = str(getattr(g, "rl_remaining", 0))
        response.headers["X-RateLimit-Reset"] = str(getattr(g, "rl_reset", 0))

    if request.path.startswith("/api/"):
        ip = _get_client_ip()
        key_header = request.headers.get("X-API-Key", "")
        if _has_valid_api_key():
            key_hint = "valid"
        elif key_header:
            key_hint = key_header[:8] + "..."
        else:
            key_hint = "none"
        try:
            _LOG_QUEUE.put_nowait((ip, request.path, key_hint, response.status_code))
        except Exception:
            pass

    return response


@app.route("/api/config")
def client_config():
    """Return client-side config (including API key) so the web app can authenticate."""
    return jsonify({"apiKey": PROVENANCE_API_KEY})


@app.route("/api/me")
def api_me():
    """Return current user info for client-side auth nav in static HTML files."""
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False}), 200
    return jsonify({
        "authenticated": True,
        "display_name": user.get("display_name") or user.get("email", "Account"),
        "tier": user.get("subscription_tier", "free"),
    }), 200


@app.route("/api/v2/export-all", methods=["GET", "POST"])
def honeypot_export_all():
    """Honey pot — permanently blocks any IP that hits this endpoint."""
    ip = _get_client_ip()
    _block_ip(ip, permanent=True)
    try:
        _LOG_QUEUE.put_nowait((ip, "/api/v2/export-all [HONEYPOT HIT]", "none", 404))
    except Exception:
        pass
    return jsonify(error="Not found"), 404


@app.route("/api/admin/access-log")
def admin_access_log():
    """Show the last 100 API access log entries. Requires valid API key."""
    if not _has_valid_api_key():
        return jsonify(error="Unauthorized"), 401
    if not DATABASE_URL:
        return jsonify(error="Database not configured"), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, ip_address, endpoint, api_key_used, response_code, timestamp"
        " FROM api_access_log ORDER BY id DESC LIMIT 100"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for row in rows:
        if row.get("timestamp"):
            row["timestamp"] = row["timestamp"].isoformat()
    return jsonify(rows)


@app.route("/api/p1000-recipes")
def p1000_recipes():
    """Return technique_references entries as P1000 recipe cards (paginated, searchable)."""
    if not DATABASE_URL:
        return jsonify(error="Database not configured"), 503
    page = max(1, request.args.get("page", 1, type=int))
    per_page = min(700, max(1, request.args.get("per_page", 48, type=int)))
    q = request.args.get("q", "").strip()
    offset = (page - 1) * per_page
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cols = "id, name, slug, category, origin, description, flavour_context, trigger_keywords, authority_tier, image_url"
    if q:
        cur.execute(
            f"SELECT {cols} FROM technique_references"
            " WHERE category LIKE %s AND (name ILIKE %s OR category ILIKE %s OR origin ILIKE %s)"
            " ORDER BY name LIMIT %s OFFSET %s",
            ("Provenance 1000%", f"%{q}%", f"%{q}%", f"%{q}%", per_page + 1, offset),
        )
    else:
        cur.execute(
            f"SELECT {cols} FROM technique_references"
            " WHERE category LIKE %s ORDER BY name LIMIT %s OFFSET %s",
            ("Provenance 1000%", per_page + 1, offset),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    has_more = len(rows) > per_page
    rows = rows[:per_page]
    return jsonify(results=rows, page=page, per_page=per_page, has_more=has_more)


# ──────────────────────────────────────────────────────────────────────────────

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data" if Path("/data").is_dir() else "./data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

RECIPES_FILE = DATA_DIR / "recipes.json"
EXTRACTED_DIR = DATA_DIR / "extracted"
EXTRACTED_DIR.mkdir(exist_ok=True)
SHARE_TOKENS_FILE = DATA_DIR / "share_tokens.json"

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
# Write user for INSERT/UPDATE/DELETE and background threads.
# Falls back to DATABASE_URL if not set (single-user mode).
DATABASE_URL_WRITE = os.environ.get("DATABASE_URL_WRITE") or DATABASE_URL


def get_db():
    """Return a DB connection. Auto-selects write user for mutating HTTP methods."""
    try:
        use_write = request.method in ("POST", "PUT", "DELETE", "PATCH")
    except RuntimeError:
        # Outside a request context (init_db, background threads)
        use_write = True
    url = DATABASE_URL_WRITE if use_write else DATABASE_URL
    last_exc = None
    for attempt in range(3):
        try:
            conn = psycopg2.connect(url)
            conn.autocommit = True
            return conn
        except psycopg2.OperationalError as e:
            last_exc = e
            if attempt < 2:
                _time.sleep(0.4 * (attempt + 1))
    raise last_exc


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
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS origin TEXT",
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS flavour_context TEXT",
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS slug VARCHAR(300)",
        "CREATE INDEX IF NOT EXISTS idx_technique_slug ON technique_references(slug)",
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS image_url TEXT",
    ]:
        cur.execute(stmt)
    cur.execute("""
        UPDATE technique_references
        SET slug = LOWER(REGEXP_REPLACE(REGEXP_REPLACE(name, '[^a-zA-Z0-9 -]', '', 'g'), ' +', '-', 'g'))
        WHERE slug IS NULL OR slug = ''
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS api_access_log (
            id SERIAL,
            ip_address VARCHAR(45),
            endpoint VARCHAR(255),
            api_key_used VARCHAR(64),
            response_code INTEGER,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            display_name VARCHAR(255),
            subscription_tier VARCHAR(50) DEFAULT 'free',
            stripe_customer_id VARCHAR(255),
            stripe_subscription_id VARCHAR(255),
            subscription_status VARCHAR(50) DEFAULT 'inactive',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # ── Recipe Costing Engine ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_prices (
            id SERIAL PRIMARY KEY,
            ingredient_name VARCHAR(500) NOT NULL,
            ingredient_name_normalized VARCHAR(500) NOT NULL,
            unit_price DECIMAL(10,4) NOT NULL,
            unit VARCHAR(50) NOT NULL,
            currency CHAR(3) DEFAULT 'CAD',
            supplier_name VARCHAR(500),
            invoice_date DATE,
            yield_factor DECIMAL(4,3) DEFAULT 1.000,
            effective_cost DECIMAL(10,4) GENERATED ALWAYS AS (unit_price / NULLIF(yield_factor, 0)) STORED,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(ingredient_name_normalized, supplier_name)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ing_price_name ON ingredient_prices(ingredient_name_normalized)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ing_price_supplier ON ingredient_prices(supplier_name)")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS yield_factors (
            id SERIAL PRIMARY KEY,
            category VARCHAR(100) NOT NULL,
            ingredient_pattern VARCHAR(255),
            default_yield DECIMAL(4,3) NOT NULL,
            description TEXT,
            UNIQUE(category)
        )
    """)
    cur.execute("""
        INSERT INTO yield_factors (category, ingredient_pattern, default_yield, description) VALUES
            ('whole_fish_round', '%salmon%whole%', 0.550, 'Head, bones, skin, pin bones — 45% loss'),
            ('whole_fish_flat', '%halibut%whole%', 0.500, 'Flat fish — 50% loss'),
            ('fish_fillet_skin_on', '%fillet%skin%on%', 0.900, 'Pin bones, trim — 10% loss'),
            ('fish_fillet_skinless', '%fillet%skinless%', 0.950, 'Minor trim only — 5% loss'),
            ('beef_tenderloin', '%tenderloin%whole%', 0.700, 'Chain, silver skin, trim — 30% loss'),
            ('beef_striploin', '%striploin%', 0.850, 'Fat cap, trim — 15% loss'),
            ('beef_short_rib', '%short%rib%', 0.850, 'Bone weight, membrane — 15% loss'),
            ('lamb_rack', '%lamb%rack%', 0.650, 'French trim, chine, fat — 35% loss'),
            ('lamb_leg', '%lamb%leg%', 0.750, 'Bone, fat, sinew — 25% loss'),
            ('chicken_whole', '%chicken%whole%', 0.650, 'Bones, fat, skin — 35% loss'),
            ('duck_whole', '%duck%whole%', 0.500, 'Heavy bone, fat — 50% loss'),
            ('herbs_picked', '%cilantro%', 0.650, 'Stems, roots, unusable leaves — 35% loss'),
            ('herbs_parsley', '%parsley%', 0.650, 'Stems, roots — 35% loss'),
            ('herbs_basil', '%basil%', 0.650, 'Stems — 35% loss'),
            ('herbs_hardy', '%rosemary%', 0.800, 'Woody stems — 20% loss'),
            ('herbs_thyme', '%thyme%', 0.800, 'Woody stems — 20% loss'),
            ('onion', '%onion%', 0.900, 'Skin, root end — 10% loss'),
            ('garlic', '%garlic%', 0.850, 'Skin, root — 15% loss'),
            ('potato', '%potato%', 0.850, 'Peel, eyes — 15% loss'),
            ('carrot', '%carrot%', 0.850, 'Peel, ends — 15% loss'),
            ('citrus_juice', '%lemon%', 0.350, 'Juice yield — 65% loss'),
            ('citrus_lime', '%lime%', 0.350, 'Juice yield — 65% loss'),
            ('shellfish_whole', '%lobster%whole%', 0.350, 'Shell — 65% loss'),
            ('shrimp_shell_on', '%shrimp%shell%', 0.550, 'Head, shell, vein — 45% loss'),
            ('shrimp_peeled', '%shrimp%peeled%', 0.900, 'Vein, minor trim — 10% loss'),
            ('no_loss_butter', '%butter%', 1.000, 'No preparation loss'),
            ('no_loss_cream', '%cream%', 1.000, 'No preparation loss'),
            ('no_loss_flour', '%flour%', 1.000, 'No preparation loss'),
            ('no_loss_oil', '%oil%', 1.000, 'No preparation loss'),
            ('no_loss_sugar', '%sugar%', 1.000, 'No preparation loss'),
            ('no_loss_salt', '%salt%', 1.000, 'No preparation loss'),
            ('no_loss_stock', '%stock%', 1.000, 'No preparation loss')
        ON CONFLICT (category) DO NOTHING
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipe_costs (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER,
            recipe_slug VARCHAR(500),
            total_cost DECIMAL(10,2),
            portions INTEGER DEFAULT 4,
            cost_per_portion DECIMAL(10,2),
            target_food_cost_pct DECIMAL(5,2) DEFAULT 30.00,
            menu_price DECIMAL(10,2),
            actual_food_cost_pct DECIMAL(5,2),
            currency CHAR(3) DEFAULT 'CAD',
            last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ingredient_breakdown JSONB,
            over_target BOOLEAN DEFAULT FALSE,
            UNIQUE(recipe_slug)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS invoice_scans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            supplier_name VARCHAR(500),
            invoice_date DATE,
            image_url TEXT,
            items_extracted INTEGER DEFAULT 0,
            prices_updated INTEGER DEFAULT 0,
            raw_extraction JSONB,
            status VARCHAR(50) DEFAULT 'processed',
            currency CHAR(3) DEFAULT 'CAD',
            invoice_total DECIMAL(10,2)
        )
    """)
    cur.close()
    conn.close()


init_db()


# ─── Static files ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file("index.html")


@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html")


@app.route("/recipes")
def recipes_page():
    return send_file("recipes.html")


PHOTO_SASHIMI_RULES = """
PHOTO ACCURACY STANDARDS — APPLY TO EVERY IMAGE:

1. PREPARATION STATE
   — State the cooking method explicitly: raw, cured, braised, fried,
     fermented, smoked, grilled, steamed, etc.
   — For raw preparations: use "raw", "uncooked", "citrus-cured", etc.
   — NEVER allow ambiguity about whether food is cooked or uncooked.

2. PRIMARY INGREDIENT ACCURACY
   — Name proteins at species level: "white sea bass" not "fish",
     "guanciale" not "bacon", "soba" not "noodles"
   — Name key produce specifically: "teff flatbread" not "flatbread",
     "kombu and katsuobushi" not "seaweed"

3. GARNISH ACCURACY
   — List ONLY garnishes found in the authentic traditional preparation
   — No herbs, flowers, or decorations not found in the technique entry
   — State garnishes specifically: "sesame seeds and dried mulato chilli"
     not "garnished"

4. VESSEL AND PLATING ACCURACY
   — Match the cultural serving tradition exactly
   — Japanese: minimalist white or earthenware ceramic, overhead
   — Ethiopian: communal woven basket or clay, overhead
   — French classical: deep bowl or rustic terracotta, 3/4 angle
   — Peruvian: dark ceramic bowl, overhead
   — Mexican: clay vessel or dark ceramic, overhead
   — Italian: wide rimmed pasta bowl, slight overhead

5. SAUCE AND LIQUID FIDELITY
   — Name the sauce or liquid correctly: "leche de tigre" not "sauce",
     "dashi broth" not "broth", "mole negro" not "dark sauce"

6. EXPLICIT PROHIBITIONS
   — Do NOT add cream to carbonara, bolognese, or any Roman pasta
   — Do NOT cook ceviche, sashimi, crudo, or any citrus-cured preparation
   — Do NOT add melted cheese to dishes where it does not appear
   — Do NOT westernise Asian plating with garnishes not in the tradition
   — Do NOT show mise en place or raw ingredients unless the dish IS
     a raw preparation
"""


def get_dish_accuracy_brief(recipe_name, cuisine, description, technique_notes=None):
    """Layer 2: pre-generation research via Claude Haiku (~$0.001)."""
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        return None

    client = anthropic.Anthropic(api_key=anthropic_key)

    query = f"""You are a professional chef and culinary historian reviewing
image generation accuracy for a professional culinary knowledge platform.

Dish: {recipe_name}
Cuisine: {cuisine or 'Unknown'}
Description: {description or 'No description available'}

Provide a BRIEF visual accuracy brief in JSON format:
{{
  "preparation_state": "exact state - e.g. raw/citrus-cured/braised/fermented",
  "key_visual_identifiers": ["list", "of", "what makes this dish visually distinctive"],
  "common_ai_mistakes": ["what image models typically get wrong about this dish"],
  "must_include": ["specific visual elements that MUST appear"],
  "must_exclude": ["things that must NOT appear"],
  "traditional_vessel": "exact serving vessel description",
  "plating_angle": "overhead/3quarter/side",
  "prompt_phrase": "one precise sentence describing the dish for an image model"
}}

Respond with valid JSON only. No other text."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": query}]
        )
        import json as _json
        raw = response.content[0].text
        s, e = raw.find('{'), raw.rfind('}')
        if s == -1 or e == -1 or s >= e:
            raise ValueError(f"No JSON object in response: {raw[:100]!r}")
        brief = _json.loads(raw[s:e + 1])
        return brief
    except Exception as e:
        print(f"Accuracy brief failed: {e}")
        return None


def build_provenance_food_prompt(recipe_name, cuisine=None, ingredients=None,
                                  description=None, accuracy_brief=None):
    """Build a Sashimi Standard photo prompt. Uses accuracy brief when available."""
    if accuracy_brief:
        core = accuracy_brief.get("prompt_phrase", "")
        vessel = accuracy_brief.get("traditional_vessel", "matte dark ceramic plate")
        angle = accuracy_brief.get("plating_angle", "overhead")
        must_include = accuracy_brief.get("must_include", [])
        must_exclude = accuracy_brief.get("must_exclude", [])

        include_str = (". ".join(must_include) + ". ") if must_include else ""
        exclude_str = ("NOT: " + ", ".join(must_exclude) + ". ") if must_exclude else ""

        angle_phrase = {
            "overhead": "overhead angle",
            "3quarter": "three-quarter angle",
            "side": "side angle"
        }.get(angle, "slight overhead angle")

        prompt = (
            f"Professional editorial food photography of {recipe_name}. "
            f"{core} "
            f"{include_str}"
            f"Served in {vessel}. "
            f"{exclude_str}"
            f"Shot from {angle_phrase}. "
        )
    else:
        cuisine_str = f"{cuisine} cuisine. " if cuisine else ""
        ing_str = ""
        if ingredients:
            names = []
            for i in ingredients[:5]:
                if isinstance(i, dict):
                    name = (i.get('name') or i.get('ingredient_name') or
                            i.get('item') or str(i)).strip()
                else:
                    name = str(i).strip()
                if name and len(name) > 1:
                    names.append(name)
            if names:
                ing_str = f"Key ingredients: {', '.join(names)}. "
        prompt = (
            f"Professional editorial food photography of {recipe_name}. "
            f"{cuisine_str}{ing_str}"
        )

    prompt += (
        "Very dark almost black background. "
        "Single directional side lighting, deep dramatic shadows. "
        "Moody, minimal, high contrast. "
        "No people, no text, no watermarks, no logos. "
        "Shot on medium format camera. "
        "Michelin-starred restaurant plating."
    )
    return prompt


def verify_dish_image(image_url, recipe_name, accuracy_brief):
    """Layer 3: post-generation visual verification via Claude Vision (~$0.003)."""
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key or not accuracy_brief:
        return True, "Verification skipped — no API key or brief", ""

    client = anthropic.Anthropic(api_key=anthropic_key)

    preparation_state = accuracy_brief.get("preparation_state", "")
    must_include = accuracy_brief.get("must_include", [])
    must_exclude = accuracy_brief.get("must_exclude", [])

    check_prompt = f"""You are a professional chef verifying food photography accuracy
for a professional culinary knowledge platform with zero tolerance for errors.

Dish: {recipe_name}
Expected preparation state: {preparation_state}
Must include: {', '.join(must_include)}
Must NOT include: {', '.join(must_exclude)}

Look at this image carefully and answer:
1. PASS or FAIL
2. What preparation state does the food appear to be in?
3. What specific accuracy problems do you see, if any?
4. If FAIL: one sentence of guidance to fix the prompt

Respond in JSON:
{{"result": "PASS" or "FAIL",
  "preparation_state_observed": "...",
  "problems": ["list of problems or empty"],
  "retry_guidance": "one sentence or empty string"}}

Be strict. A cooked ceviche is a FAIL. Cream in carbonara is a FAIL.
Wrong protein is a FAIL. Respond with valid JSON only."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "url", "url": image_url}
                    },
                    {"type": "text", "text": check_prompt}
                ]
            }]
        )
        import json as _json
        raw = response.content[0].text
        s, e = raw.find('{'), raw.rfind('}')
        if s == -1 or e == -1 or s >= e:
            raise ValueError(f"No JSON in verification response: {raw[:100]!r}")
        result = _json.loads(raw[s:e + 1])
        passed = result.get("result") == "PASS"
        problems = result.get("problems", [])
        guidance = result.get("retry_guidance", "")
        obs = "; ".join(problems) if problems else "All checks passed"
        return passed, obs, guidance
    except Exception as e:
        print(f"Verification failed: {e}")
        return True, f"Verification error: {e}", ""


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/api/recipe/<slug>/generate-image", methods=["POST"])
def generate_recipe_image(slug):
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        return jsonify({"error": "FAL_KEY not configured"}), 503
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json(silent=True) or {}
    max_attempts = min(int(data.get("max_attempts", 3)), 3)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, name, cuisine, description, ingredients FROM recipes "
        "WHERE slug = %s LIMIT 1", (slug,)
    )
    recipe = cur.fetchone()
    if not recipe:
        cur.close(); conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    ingredients = recipe.get('ingredients') or []
    if isinstance(ingredients, str):
        import json as _json
        ingredients = _json.loads(ingredients)

    # ── Layer 2: pre-generation accuracy brief ──
    accuracy_brief = get_dish_accuracy_brief(
        recipe_name=recipe['name'],
        cuisine=recipe.get('cuisine'),
        description=recipe.get('description', '')
    )

    attempts = []
    final_url = None
    final_passed = False

    os.environ["FAL_KEY"] = fal_key

    for attempt in range(max_attempts):
        retry_guidance = attempts[-1].get('retry_guidance', '') if attempts else ''

        if retry_guidance and accuracy_brief:
            accuracy_brief['prompt_phrase'] = (
                accuracy_brief.get('prompt_phrase', '') + ' ' + retry_guidance
            )

        prompt = build_provenance_food_prompt(
            recipe_name=recipe['name'],
            cuisine=recipe.get('cuisine'),
            ingredients=ingredients,
            description=recipe.get('description', ''),
            accuracy_brief=accuracy_brief
        )

        try:
            result = fal_client.subscribe(
                "fal-ai/flux-pro/v1.1",
                arguments={
                    "prompt": prompt,
                    "width": 1280,
                    "height": 768,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                }
            )
            image_url = result["images"][0]["url"]

            # ── Layer 3: post-generation verification ──
            passed, observations, retry_guidance = verify_dish_image(
                image_url, recipe['name'], accuracy_brief
            )

            attempts.append({
                "attempt": attempt + 1,
                "image_url": image_url,
                "passed": passed,
                "observations": observations,
                "retry_guidance": retry_guidance,
                "prompt": prompt
            })

            if passed:
                final_url = image_url
                final_passed = True
                break
            elif attempt == max_attempts - 1:
                final_url = image_url
                final_passed = False

        except Exception as e:
            attempts.append({
                "attempt": attempt + 1,
                "error": str(e),
                "passed": False
            })

    if not final_url:
        cur.close(); conn.close()
        return jsonify({"error": "All generation attempts failed", "attempts": attempts}), 500

    cur.execute("UPDATE recipes SET image_url = %s WHERE id = %s", (final_url, recipe['id']))
    conn.commit()
    cur.close(); conn.close()

    return jsonify({
        "image_url": final_url,
        "saved": True,
        "verified": final_passed,
        "attempts": len(attempts),
        "attempt_log": attempts,
        "accuracy_brief": accuracy_brief
    })


@app.route("/api/technique/<slug>/generate-image", methods=["POST"])
def generate_technique_image(slug):
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        return jsonify({"error": "FAL_KEY not configured"}), 503
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json(silent=True) or {}
    max_attempts = min(int(data.get("max_attempts", 3)), 3)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, name, origin, description, flavour_context, trigger_keywords "
        "FROM technique_references WHERE slug = %s LIMIT 1", (slug,)
    )
    tech = cur.fetchone()
    if not tech:
        cur.close(); conn.close()
        return jsonify({"error": "Technique not found"}), 404

    keywords = tech.get("trigger_keywords") or []
    if isinstance(keywords, str):
        import json as _json
        keywords = _json.loads(keywords)

    description = " ".join(filter(None, [tech.get("description", ""), tech.get("flavour_context", "")]))

    accuracy_brief = get_dish_accuracy_brief(
        recipe_name=tech["name"],
        cuisine=tech.get("origin"),
        description=tech.get("description", "")
    )

    attempts = []
    final_url = None
    final_passed = False
    os.environ["FAL_KEY"] = fal_key

    for attempt in range(max_attempts):
        retry_guidance = attempts[-1].get("retry_guidance", "") if attempts else ""
        if retry_guidance and accuracy_brief:
            accuracy_brief["prompt_phrase"] = accuracy_brief.get("prompt_phrase", "") + " " + retry_guidance

        prompt = build_provenance_food_prompt(
            recipe_name=tech["name"],
            cuisine=tech.get("origin"),
            ingredients=keywords,
            description=description,
            accuracy_brief=accuracy_brief
        )

        try:
            result = fal_client.subscribe(
                "fal-ai/flux-pro/v1.1",
                arguments={
                    "prompt": prompt,
                    "width": 1280,
                    "height": 768,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                }
            )
            image_url = result["images"][0]["url"]
            passed, observations, retry_guidance = verify_dish_image(
                image_url, tech["name"], accuracy_brief
            )
            attempts.append({
                "attempt": attempt + 1,
                "image_url": image_url,
                "passed": passed,
                "observations": observations,
                "retry_guidance": retry_guidance,
                "prompt": prompt
            })
            if passed:
                final_url = image_url
                final_passed = True
                break
            elif attempt == max_attempts - 1:
                final_url = image_url
                final_passed = False
        except Exception as e:
            attempts.append({"attempt": attempt + 1, "error": str(e), "passed": False})

    if not final_url:
        cur.close(); conn.close()
        return jsonify({"error": "All generation attempts failed", "attempts": attempts}), 500

    cur.execute("UPDATE technique_references SET image_url = %s WHERE id = %s", (final_url, tech["id"]))
    conn.commit()
    cur.close(); conn.close()

    return jsonify({
        "image_url": final_url,
        "saved": True,
        "verified": final_passed,
        "attempts": len(attempts),
        "attempt_log": attempts,
        "accuracy_brief": accuracy_brief
    })


@app.route("/api/recipe/<slug>/upload-image", methods=["POST"])
def upload_recipe_image(slug):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    data = request.get_json(silent=True) or {}
    image_url = data.get("image_url", "").strip()
    if not image_url or not image_url.startswith("http"):
        return jsonify({"error": "Valid image URL required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "UPDATE recipes SET image_url = %s WHERE slug = %s RETURNING id, name",
        (image_url, slug)
    )
    result = cur.fetchone()
    conn.commit(); cur.close(); conn.close()
    if not result:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify({"saved": True, "image_url": image_url})


# ── Beverage category → glassware/vessel/angle mapping ──────────────────────
_BEV_VESSEL_MAP = {
    "wine_still":       ("appropriate wine glass (Burgundy for Pinot, Bordeaux for Cabernet, white wine glass for whites)", "three-quarter"),
    "wine_sparkling":   ("tall champagne flute or coupe, condensation visible on glass", "three-quarter"),
    "wine_fortified":   ("small copita or port glass, 60ml pour", "three-quarter"),
    "wine_dessert":     ("small dessert wine glass, honeyed liquid catching light", "three-quarter"),
    "spirits_whiskey":  ("crystal rocks glass, neat or single large ice cube", "three-quarter"),
    "spirits_brandy":   ("wide balloon snifter, 30ml pour, hand-warming", "three-quarter"),
    "spirits_agave":    ("traditional clay copita or narrow rocks glass", "three-quarter"),
    "spirits_gin":      ("highball or balloon gin glass with botanicals visible", "three-quarter"),
    "spirits_rum":      ("rocks glass or coupe, neat", "three-quarter"),
    "spirits_vodka":    ("chilled shot glass or martini glass, crystal clear", "three-quarter"),
    "spirits_liqueur":  ("small stemmed liqueur glass or coupe, 45ml", "three-quarter"),
    "sake":             ("traditional white ceramic tokkuri pouring vessel and ochoko cup", "overhead"),
    "shochu":           ("small ceramic yunomi cup, mizuwari style with ice", "overhead"),
    "umeshu":           ("rocks glass over crushed ice, deep amber colour", "three-quarter"),
    "baijiu":           ("small tulip-shaped 30ml shot glass, clear spirit", "three-quarter"),
    "beer_ale":         ("tulip pint glass showing colour, 4cm white foam crown", "three-quarter"),
    "beer_lager":       ("pilsner glass, crystal clear, fine persistent bubbles", "three-quarter"),
    "beer_wild":        ("tulip glass, hazy, complex colour showing terroir", "three-quarter"),
    "cider":            ("tulip glass or wine glass, golden-amber, fine bubbles", "three-quarter"),
    "tea":              ("authentic gaiwan or kyusu teapot, steam rising, side light", "overhead"),
    "coffee":           ("white espresso demitasse or clear pour-over vessel, crema visible", "overhead"),
    "na_crafted":       ("highball or stemless wine glass, garnish minimal and precise", "three-quarter"),
    "na_fermented":     ("ceramic cup or small jar, active culture visible", "overhead"),
    "na_dealcoholised": ("appropriate wine or cocktail glass, same aesthetic as alcoholic counterpart", "three-quarter"),
    "traditional_cultural": ("traditional cultural vessel — clay, wood, gourd, or woven, culturally accurate", "overhead"),
}


def build_beverage_prompt(name, category, description=None, origin_country=None,
                           subcategory=None, flavour_markers=None):
    """Build a Photo Sashimi Standard prompt for a beverage product."""
    vessel, angle = _BEV_VESSEL_MAP.get(
        category, ("appropriate glass for the tradition", "three-quarter")
    )
    angle_phrase = {"overhead": "overhead angle", "three-quarter": "three-quarter angle"}.get(angle, "three-quarter angle")

    origin_str = f" from {origin_country}" if origin_country else ""
    cat_label = category.replace("_", " ").replace("wine still", "still wine").replace("wine sparkling", "sparkling wine")
    flavour_str = ""
    if flavour_markers:
        flavour_str = f" Flavour notes: {', '.join(flavour_markers[:4])}."

    desc_str = f" {description[:120]}." if description else ""

    prompt = (
        f"Professional editorial beverage photography of {name}, a {cat_label}{origin_str}."
        f"{desc_str}{flavour_str} "
        f"Served in {vessel}. "
        f"Shot from {angle_phrase}. "
        "Very dark almost black background. "
        "Single directional side lighting catching liquid colour, clarity, and surface tension. "
        "Deep dramatic shadows, high contrast. "
        "Moody, minimal, no people, no text, no watermarks, no logos. "
        "Bottle or vessel only — no food. "
        "Shot on medium format camera. "
        "Museum-quality product photography."
    )
    return prompt


def verify_beverage_image(image_url, name, category):
    """Post-generation visual verification for beverages via Claude Vision."""
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        return True, "Verification skipped", ""
    client = anthropic.Anthropic(api_key=anthropic_key)
    cat_label = category.replace("_", " ")
    check_prompt = f"""You are a beverage photography editor for a professional culinary platform.

Product: {name}
Category: {cat_label}

Review this image and answer:
1. PASS or FAIL
2. Is the correct glassware/vessel visible for this beverage category?
3. Any accuracy problems? (wrong glass, food present, watermarks, wrong beverage type shown)
4. If FAIL: one fix sentence

Respond JSON only: {{"result": "PASS" or "FAIL", "problems": ["list or empty"], "retry_guidance": "one sentence or empty"}}"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "url", "url": image_url}},
                {"type": "text", "text": check_prompt}
            ]}]
        )
        import json as _json
        raw = response.content[0].text
        s, e = raw.find('{'), raw.rfind('}')
        if s == -1 or e <= s:
            return True, "Parse error in verification", ""
        result = _json.loads(raw[s:e+1])
        passed = result.get("result") == "PASS"
        problems = "; ".join(result.get("problems", [])) or "All checks passed"
        return passed, problems, result.get("retry_guidance", "")
    except Exception as ex:
        return True, f"Verification error: {ex}", ""


@app.route("/api/beverage/<int:product_id>/generate-image", methods=["POST"])
def generate_beverage_image(product_id):
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        return jsonify({"error": "FAL_KEY not configured"}), 503
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json(silent=True) or {}
    max_attempts = min(int(data.get("max_attempts", 2)), 3)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT id, name, category, subcategory, description, origin_country, flavour_markers "
        "FROM beverage_products WHERE id = %s LIMIT 1", (product_id,)
    )
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        return jsonify({"error": "Beverage product not found"}), 404

    os.environ["FAL_KEY"] = fal_key
    attempts = []
    final_url = None
    final_passed = False
    retry_guidance = ""

    for attempt in range(max_attempts):
        extra = (" " + retry_guidance) if retry_guidance else ""
        prompt = build_beverage_prompt(
            name=product["name"],
            category=product["category"],
            description=(product.get("description") or "") + extra,
            origin_country=product.get("origin_country"),
            subcategory=product.get("subcategory"),
            flavour_markers=product.get("flavour_markers") or [],
        )
        try:
            result = fal_client.subscribe(
                "fal-ai/flux-pro/v1.1",
                arguments={
                    "prompt": prompt,
                    "width": 1280,
                    "height": 768,
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                }
            )
            image_url = result["images"][0]["url"]
            passed, observations, retry_guidance = verify_beverage_image(
                image_url, product["name"], product["category"]
            )
            attempts.append({
                "attempt": attempt + 1,
                "image_url": image_url,
                "passed": passed,
                "observations": observations,
                "prompt": prompt,
            })
            if passed:
                final_url = image_url
                final_passed = True
                break
            elif attempt == max_attempts - 1:
                final_url = image_url
                final_passed = False
        except Exception as e:
            attempts.append({"attempt": attempt + 1, "error": str(e), "passed": False})

    if not final_url:
        cur.close(); conn.close()
        return jsonify({"error": "All generation attempts failed", "attempts": attempts}), 500

    cur.execute("UPDATE beverage_products SET image_url = %s WHERE id = %s", (final_url, product["id"]))
    conn.commit()
    cur.close(); conn.close()

    return jsonify({
        "image_url": final_url,
        "saved": True,
        "verified": final_passed,
        "attempts": len(attempts),
        "attempt_log": attempts,
    })


@app.route("/for-professionals")
def for_professionals_page():
    return render_template("for_professionals.html")


@app.route("/methodology")
def methodology_page():
    return render_template("methodology.html")


@app.route("/provenance-originals")
def provenance_originals_page():
    return render_template("provenance_originals.html")


@app.route("/suppliers")
def suppliers_page():
    if not DATABASE_URL:
        return render_template("suppliers.html", suppliers=[])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT s.id, s.name, s.notes, s.website, s.service_region,
               COUNT(ps.id) as product_count
        FROM suppliers s
        LEFT JOIN product_suppliers ps ON s.id = ps.supplier_id
        GROUP BY s.id
        ORDER BY product_count DESC
    """)
    suppliers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("suppliers.html", suppliers=suppliers)


@app.route("/recipe/<slug>")
def recipe_page(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recipes WHERE slug = %s", (slug,))
    recipe = cur.fetchone()
    if not recipe:
        cur.close()
        conn.close()
        return "Recipe not found", 404

    # Find suppliers (ORIGIN and PROVIDER) linked to this recipe's ingredients by name
    recipe_suppliers = []
    try:
        ingredients = recipe.get("ingredients") or []
        ingredient_names = [ing.get("name", "") for ing in ingredients if ing.get("name")]
        if ingredient_names:
            patterns = [f"%{n}%" for n in ingredient_names[:20]]
            # Bidirectional: product name contains ingredient fragment OR
            # ingredient name contains product name (e.g. "fresh spearmint" contains "mint")
            cur.execute("""
                SELECT DISTINCT ON (s.id, ip.name)
                    s.id, s.name, s.website, s.city, s.state_province, s.country,
                    ip.name AS product_name,
                    LEFT(ip.description, 140) AS product_desc
                FROM ingredient_products ip
                JOIN product_suppliers ps ON ip.id = ps.product_id
                JOIN suppliers s ON ps.supplier_id = s.id
                WHERE (
                    ip.name ILIKE ANY(%s)
                    OR EXISTS (
                        SELECT 1 FROM unnest(%s::text[]) AS ri(nm)
                        WHERE ri.nm ILIKE '%%' || ip.name || '%%'
                    )
                )
                ORDER BY s.id, ip.name, s.name
            """, (patterns, ingredient_names[:20]))
            rows = cur.fetchall()
            # Group products by supplier
            from collections import defaultdict
            supplier_map = {}
            for row in rows:
                sid = row['id']
                if sid not in supplier_map:
                    supplier_map[sid] = {
                        'id': sid, 'name': row['name'], 'website': row['website'],
                        'city': row['city'], 'state_province': row['state_province'],
                        'country': row['country'], 'products': []
                    }
                if row['product_name']:
                    supplier_map[sid]['products'].append({
                        'name': row['product_name'],
                        'desc': row['product_desc'] or ''
                    })
            recipe_suppliers = list(supplier_map.values())
    except Exception:
        recipe_suppliers = []

    cur.close()
    conn.close()
    return render_template("recipe.html", recipe=recipe, recipe_suppliers=recipe_suppliers)


@app.route("/api/curated-recipes")
def curated_recipes():
    """Return all recipes from the recipes table (curated + user-built)."""
    if not DATABASE_URL:
        return jsonify({"recipes": []}), 200
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, slug, cuisine, description, image_url, recipe_type, is_curated
        FROM recipes ORDER BY is_curated DESC, id ASC
    """)
    recipes = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify({"recipes": recipes})


@app.route("/manifest.json")
def pwa_manifest():
    return app.send_static_file('manifest.json')


@app.route("/sw.js")
def service_worker():
    """Serve SW from root scope so it can control the entire site."""
    response = app.send_static_file('sw.js')
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
Allow: /
Allow: /techniques/
Allow: /technique/
Allow: /recipes/
Allow: /recipe/
Allow: /drinks/
Allow: /cuisines/
Allow: /beverage/
Allow: /about
Allow: /suppliers
Allow: /for-professionals
Allow: /methodology

Disallow: /kitchen
Disallow: /api/
Disallow: /admin/
Disallow: /static/

Sitemap: https://provenance.kitchen/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


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


def load_share_tokens():
    if not SHARE_TOKENS_FILE.exists():
        return {}
    with open(SHARE_TOKENS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_share_tokens(tokens):
    with open(SHARE_TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)


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

_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

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
        fetch_headers = {**_BROWSER_HEADERS, "Referer": "https://www.google.com/"}
        resp = http_requests.get(url, headers=fetch_headers, timeout=15)
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
                img_resp = http_requests.get(recipe["_image_url"], headers=fetch_headers, timeout=10)
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
        resp = http_requests.get(url, headers=_BROWSER_HEADERS, timeout=15)
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "image/jpeg")
        return Response(resp.content, content_type=ct)
    except Exception:
        return jsonify(error="Failed to fetch image"), 400


# ─── Compose endpoint ────────────────────────────────────────────────────────

@app.route("/api/recipes/compose", methods=["POST"])
def compose_recipe():
    """Generate an original recipe from a creative brief using the technique database as knowledge."""
    data = request.get_json() or {}
    brief = (data.get("brief") or "").strip()

    if not brief:
        return jsonify(error="Please describe what you want to create"), 400

    techniques = []
    products = []
    pairings = []

    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            words = [w.strip(".,!?'\"") for w in brief.lower().split() if len(w) > 3]
            kw_patterns = [f"%{w}%" for w in words[:8]]

            # Relevant techniques via keyword matching
            cur.execute("""
                SELECT name, category, key_principles, pro_tips, origin, cross_cuisine_parallels, flavour_context
                FROM technique_references
                WHERE (name || ' ' || COALESCE(category,'') || ' ' || COALESCE(key_principles,'') || ' ' || COALESCE(origin,''))
                      ILIKE ANY(%s)
                ORDER BY RANDOM()
                LIMIT 12
            """, (kw_patterns,))
            techniques = [dict(r) for r in cur.fetchall()]

            # Top up with random techniques if too few matched
            if len(techniques) < 6:
                cur.execute("""
                    SELECT name, category, key_principles, pro_tips, origin
                    FROM technique_references
                    WHERE key_principles IS NOT NULL AND key_principles != ''
                    ORDER BY RANDOM()
                    LIMIT %s
                """, (10 - len(techniques),))
                techniques.extend([dict(r) for r in cur.fetchall()])

            # Matching ingredient products
            cur.execute("""
                SELECT ip.name, ip.origin_description, ip.country_of_origin,
                       s.name AS supplier_name, s.city, s.state_province
                FROM ingredient_products ip
                LEFT JOIN product_suppliers ps ON ip.id = ps.product_id
                LEFT JOIN suppliers s ON ps.supplier_id = s.id
                WHERE ip.name ILIKE ANY(%s)
                LIMIT 8
            """, (kw_patterns,))
            products = [dict(r) for r in cur.fetchall()]

            # Relevant beverage pairings
            cur.execute("""
                SELECT pi.pairing_type, pi.flavour_logic, pi.food_category, pi.meal_context,
                       bp.name AS beverage_name, bp.category AS beverage_category
                FROM pairing_intelligence pi
                LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id
                WHERE pi.food_category ILIKE ANY(%s)
                   OR pi.food_flavour_profile ILIKE ANY(%s)
                ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 ELSE 3 END
                LIMIT 4
            """, (kw_patterns, kw_patterns))
            pairings = [dict(r) for r in cur.fetchall()]

            cur.close()
            conn.close()
        except Exception:
            pass

    # Build context blocks
    tech_lines = []
    for t in techniques:
        line = f"- {t['name']}"
        if t.get("category"):
            line += f" [{t['category']}]"
        if t.get("origin"):
            line += f" — Origin: {(t['origin'] or '')[:120]}"
        if t.get("key_principles"):
            line += f" — {(t['key_principles'] or '')[:120]}"
        if t.get("cross_cuisine_parallels"):
            line += f" — Cross-cuisine: {str(t['cross_cuisine_parallels'])[:100]}"
        tech_lines.append(line)
    tech_block = "\n".join(tech_lines) if tech_lines else "No specific matches — use your professional knowledge."

    prod_lines = []
    for p in products:
        line = f"- {p['name']}"
        if p.get("origin_description"):
            line += f": {(p['origin_description'] or '')[:80]}"
        if p.get("supplier_name"):
            line += f" (available from {p['supplier_name']}, {p.get('city','')}, {p.get('state_province','')})"
        prod_lines.append(line)
    prod_block = "\n".join(prod_lines) if prod_lines else "No specific product matches in the database yet."

    pair_lines = []
    for p in pairings:
        bev = p.get("beverage_name") or p.get("beverage_category") or ""
        if bev:
            pair_lines.append(f"- {bev}: {(p.get('flavour_logic') or '')[:100]}")
    pair_block = "\n".join(pair_lines) if pair_lines else "No specific pairing matches — suggest an appropriate pairing."

    prompt = f"""You are an executive chef with 30 years experience across French, Japanese, Southeast Asian, Pacific Island, Indigenous Australian, and Latin American kitchens. You have deep knowledge of food history, diaspora cooking, and indigenous food systems.

A chef has given you this creative brief:
"{brief}"

Using your knowledge and the technique database context below, compose ONE original recipe that:
- Directly addresses what the chef asked for
- Is historically and culturally accurate (if the brief references a time period or culture, research it properly)
- Uses specific, named ingredients (not generic — Tellicherry pepper, not "pepper")
- Includes professional method steps with temperatures, timings, and sensory cues
- Makes culinary sense — every ingredient combination must work on the palate
- Tells a story — the preamble should explain the cultural connection or historical reasoning

TECHNIQUE DATABASE CONTEXT (from Provenance's {len(techniques)} matching entries):
{tech_block}

AVAILABLE INGREDIENTS AND SUPPLIERS:
{prod_block}

SUGGESTED BEVERAGE PAIRINGS:
{pair_block}

Return ONLY valid JSON — no markdown, no backticks:
{{
  "title": "Evocative dish name",
  "preamble": "2-4 sentences explaining the cultural story, the historical connection, why this dish exists. Speak like Ducasse or Larousse — with reverence, not explanation.",
  "tags": ["cuisine1", "cuisine2", "primary_ingredient", "technique"],
  "servings": [{{"count": "4", "unit": "portions"}}],
  "time": {{"active": "45 min", "total": "2 hours"}},
  "ingredients": [
    {{"name": "specific ingredient", "count": "qty", "unit": "unit", "info": "prep note or cultural context"}}
  ],
  "steps": [
    "Detailed professional step with temperature, timing, and sensory cues."
  ],
  "suggested_pairing": {{
    "beverage": "Specific beverage name",
    "reasoning": "Why this pairing works with this specific dish"
  }},
  "provenance_notes": "1-2 sentences on the cultural preservation significance — what knowledge this dish keeps alive"
}}

Rules:
- If the brief asks for a historical period, be historically accurate about what existed then
- If the brief mentions a specific cuisine, techniques must be authentic to that cuisine
- Every ingredient must serve a purpose — no garnish-for-the-sake-of-garnish
- The preamble and provenance_notes are what make this a Provenance recipe, not just a recipe
- Minimum 8 ingredients, 6 steps
- If uncertain about historical specifics, note what is known and what is a respectful approximation"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            resp_text = "\n".join(lines)

        rdata = json.loads(resp_text)
        recipe_uuid = str(uuid.uuid4()).upper()
        recipe = {
            "uuid": recipe_uuid,
            "title": rdata.get("title", "Composed Recipe"),
            "lang": "",
            "version": "1",
            "favourite": False,
            "rating": 0.0,
            "updated": "",
            "importDate": "",
            "hasImage": False,
            "time": rdata.get("time", {"active": "", "total": ""}),
            "cooking": {"times": "0", "last": ""},
            "tags": rdata.get("tags", []),
            "servings": rdata.get("servings", []),
            "ingredients": rdata.get("ingredients", []),
            "steps": rdata.get("steps", []),
            "preamble": rdata.get("preamble", ""),
            "source": {"name": "Provenance Compose", "address": ""},
            "_composed": True,
            "_brief": brief,
            "_provenance_notes": rdata.get("provenance_notes", ""),
            "_suggested_pairing": rdata.get("suggested_pairing", {}),
        }
        recipes_list = load_recipes()
        recipes_list.append(recipe)
        save_recipes(recipes_list)

        # Also save to the recipes table so /recipe/<slug> works
        if DATABASE_URL:
            try:
                slug_base = _slugify(rdata.get("title", "composed-recipe"))
                slug = slug_base
                conn2 = get_db()
                cur2 = conn2.cursor()
                suffix = 1
                while suffix < 100:
                    cur2.execute("SELECT id FROM recipes WHERE slug = %s", (slug,))
                    if not cur2.fetchone():
                        break
                    slug = f"{slug_base}-{suffix}"
                    suffix += 1
                # Determine servings count
                srv_raw = rdata.get("servings", [{}])
                try:
                    srv_count = int(srv_raw[0].get("count", 4)) if srv_raw else 4
                except (IndexError, AttributeError, ValueError, TypeError):
                    srv_count = 4
                tags = rdata.get("tags", [])
                recipe_type = "drink" if any(t in ("cocktail", "drink", "beverage", "cocktails") for t in tags) else "food"
                full_content = {
                    "origin": rdata.get("preamble", ""),
                    "provenance_notes": rdata.get("provenance_notes", ""),
                    "suggested_pairing": rdata.get("suggested_pairing", {}),
                }
                cur2.execute("""
                    INSERT INTO recipes (name, slug, cuisine, description, recipe_type,
                                        is_curated, full_content, ingredients, steps, servings)
                    VALUES (%s, %s, %s, %s, %s, FALSE, %s, %s, %s, %s)
                """, (
                    rdata.get("title", "Composed Recipe"),
                    slug,
                    tags[0] if tags else None,
                    (rdata.get("preamble", ""))[:500],
                    recipe_type,
                    json.dumps(full_content),
                    json.dumps(rdata.get("ingredients", [])),
                    json.dumps(rdata.get("steps", [])),
                    srv_count,
                ))
                conn2.commit()
                cur2.close()
                conn2.close()
                recipe["slug"] = slug
            except Exception:
                recipe["slug"] = None

        return jsonify(recipe)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── CRUD endpoints ─────────────────────────────────────────────────────────

@app.route("/api/recipes/new", methods=["POST"])
def create_blank_recipe():
    recipes = load_recipes()
    recipe_uuid = str(uuid.uuid4()).upper()
    recipe = {
        "uuid": recipe_uuid,
        "title": "Untitled Recipe",
        "lang": "",
        "version": "1",
        "favourite": False,
        "rating": 0.0,
        "updated": "",
        "importDate": "",
        "hasImage": False,
        "time": {"active": "", "total": ""},
        "cooking": {"times": "0", "last": ""},
        "tags": [],
        "servings": [],
        "ingredients": [],
        "steps": [],
        "preamble": "",
        "source": {"name": "", "address": ""},
        "_draft": True,
    }
    recipes.append(recipe)
    save_recipes(recipes)
    return jsonify(recipe)


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

    # Clear draft flag once saved with a real title
    if recipe.get("_draft") and recipe.get("title", "").strip() not in ("", "Untitled Recipe"):
        recipe.pop("_draft", None)

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


# ─── Share links ─────────────────────────────────────────────────────────────

@app.route("/api/share/<recipe_uuid>", methods=["POST"])
def create_share_link(recipe_uuid):
    recipes = load_recipes()
    recipe = next((r for r in recipes if r["uuid"] == recipe_uuid), None)
    if recipe is None:
        return jsonify(error="Recipe not found"), 404

    tokens = load_share_tokens()
    # Check if token already exists for this UUID
    existing = next((t for t, u in tokens.items() if u == recipe_uuid), None)
    if existing:
        return jsonify(share_url=f"/share/{existing}")

    token = secrets.token_urlsafe(6)
    tokens[token] = recipe_uuid
    save_share_tokens(tokens)
    return jsonify(share_url=f"/share/{token}")


@app.route("/share/<token>")
def view_shared_recipe(token):
    tokens = load_share_tokens()
    recipe_uuid = tokens.get(token)
    if not recipe_uuid:
        return "Not found", 404

    recipes = load_recipes()
    recipe = next((r for r in recipes if r["uuid"] == recipe_uuid), None)
    if not recipe:
        return "Not found", 404

    e = html_mod.escape
    title = e(recipe.get("title", "Untitled"))
    preamble = e(recipe.get("preamble", ""))

    img_html = ""
    if recipe.get("hasImage"):
        img_html = f'<img src="/images/{e(recipe_uuid)}/main.jpg" alt="" style="width:100%;max-height:400px;object-fit:cover;border-radius:8px;margin-bottom:1.5rem">'

    ingredients_html = ""
    for ing in recipe.get("ingredients", []):
        parts = []
        if ing.get("count"):
            parts.append(ing["count"])
        if ing.get("unit"):
            parts.append(ing["unit"])
        parts.append(ing.get("name", ""))
        text = " ".join(parts)
        if ing.get("info"):
            text += f" ({ing['info']})"
        ingredients_html += f"<li>{e(text.strip())}</li>"

    steps_html = ""
    for step in recipe.get("original_steps") or recipe.get("steps", []):
        steps_html += f"<li>{e(step)}</li>"

    tags_html = ""
    for tag in recipe.get("tags", []):
        tags_html += f'<span style="display:inline-block;background:#f0ede8;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.85rem;margin:0.15rem">{e(tag)}</span> '

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Provenance</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f0; color: #1a1a1a; line-height: 1.6; }}
  .container {{ max-width: 680px; margin: 2rem auto; padding: 0 1.25rem; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 0.5rem; }}
  .preamble {{ color: #666; margin-bottom: 1.5rem; }}
  h2 {{ font-size: 1.1rem; margin: 1.5rem 0 0.5rem; color: #44403C; }}
  ul {{ padding-left: 1.25rem; margin-bottom: 1rem; }}
  ol {{ padding-left: 1.25rem; }}
  li {{ margin-bottom: 0.4rem; }}
  .tags {{ margin-top: 1.5rem; }}
  .footer {{ margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #ddd; font-size: 0.85rem; color: #999; }}
  .footer a {{ color: #8B2C1A; text-decoration: none; }}
</style></head><body>
<div class="container">
  {img_html}
  <h1>{title}</h1>
  {'<p class="preamble">' + preamble + '</p>' if preamble else ''}
  <h2>Ingredients</h2>
  <ul>{ingredients_html}</ul>
  <h2>Method</h2>
  <ol>{steps_html}</ol>
  {'<div class="tags">' + tags_html + '</div>' if tags_html else ''}
  <div class="footer">Powered by <a href="/">Provenance</a></div>
</div>
</body></html>"""


# ─── Technique reference endpoints ───────────────────────────────────────────

@app.route("/api/techniques")
def list_techniques():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if _has_valid_api_key():
        # Authenticated: return all results (or honour optional ?page=&per_page= params)
        page = request.args.get("page", type=int)
        per_page = request.args.get("per_page", type=int)
        if page and per_page:
            cur.execute(
                "SELECT * FROM technique_references ORDER BY id LIMIT %s OFFSET %s",
                (per_page, (page - 1) * per_page),
            )
        else:
            cur.execute("SELECT * FROM technique_references ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            for k in ("created_at", "updated_at"):
                if row.get(k):
                    row[k] = row[k].isoformat()
        return jsonify(rows)

    # Unauthenticated: paginate, max 20 results per page, no total count exposed
    page = max(1, request.args.get("page", 1, type=int))
    per_page = min(20, max(1, request.args.get("per_page", 20, type=int)))
    offset = (page - 1) * per_page
    # Fetch one extra to determine has_more without revealing the total
    cur.execute(
        "SELECT * FROM technique_references ORDER BY id LIMIT %s OFFSET %s",
        (per_page + 1, offset),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    has_more = len(rows) > per_page
    rows = rows[:per_page]
    for row in rows:
        for k in ("created_at", "updated_at"):
            if row.get(k):
                row[k] = row[k].isoformat()
    return jsonify(
        results=rows,
        page=page,
        per_page=per_page,
        has_more=has_more,
    )


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
                source_book, cross_cuisine_parallels, origin, flavour_context)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
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
                e.get("origin"),
                e.get("flavour_context"),
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

    # Build SET clause dynamically — only update fields that are present in the request
    allowed = {
        "name": str, "category": str, "description": str, "key_principles": str,
        "common_mistakes": str, "pro_tips": str, "authority_tier": int,
        "tier_level": str, "source_book": str, "origin": str, "flavour_context": str,
    }
    json_fields = {"trigger_keywords", "related_techniques", "cross_cuisine_parallels"}

    sets = []
    vals = []
    for field, typ in allowed.items():
        if field in data:
            sets.append(f"{field} = %s")
            vals.append(data[field])
    for field in json_fields:
        if field in data:
            sets.append(f"{field} = %s")
            vals.append(json.dumps(data[field]))

    if not sets:
        cur.close()
        conn.close()
        return jsonify(error="No fields to update"), 400

    sets.append("updated_at = NOW()")
    vals.append(technique_id)
    sql = f"UPDATE technique_references SET {', '.join(sets)} WHERE id = %s"
    cur.execute(sql, vals)
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
    "preparation, wet_heat, pastry_technique, finishing, finishing_tableside, grains_and_dough, "
    "presentation_and_philosophy, preparation_and_service. "
    "Use finishing_tableside for techniques performed at the table such as flambé, tableside carving, guéridon service, or any presentation done in front of the diner. "
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


def _build_recipe_user_msg(title, ingredients, method_steps):
    msg = f"Recipe: {title}\n\nIngredients:\n"
    for ing in ingredients:
        msg += f"- {ing}\n"
    msg += "\nMethod:\n"
    for i, step in enumerate(method_steps, 1):
        msg += f"{i}. {step}\n"
    return msg


def _detect_raw_served(ingredients, method_steps):
    """
    Returns True if the recipe contains raw-served proteins
    with no kill step. Detects sashimi, tartare, ceviche,
    oysters, cold-smoked, cured-only, rare/blue preparations.
    Uses compound phrases to avoid false positives on cooked
    recipes that mention 'raw' in prep context.
    """
    raw_keywords = [
        'sashimi', 'sushi', 'tartare', 'tatar', 'ceviche',
        'crudo', 'carpaccio', 'blue steak', 'blue rare',
        'cold smoked', 'cold-smoked', 'gravlax', 'lox',
        'cured salmon', 'oyster', 'clam', 'mussel',
        'half shell', 'on the shell', 'tiradito',
        'poke', 'aguachile',
        'raw fish', 'raw seafood', 'raw shellfish',
        'raw oyster', 'raw scallop', 'served raw',
        'eat raw', 'consume raw', 'rare beef', 'rare tuna',
        'steak tartare', 'beef tartare',
    ]

    strong_cooking_escapes = [
        'braise', 'braised', 'braising', 'roast', 'roasted',
        'bake', 'baked', 'fry', 'fried', 'frying',
        'deep fry', 'pan fry', 'sauté', 'saute', 'sautéed',
        'poach', 'poached', 'steam', 'steamed', 'stew',
        'stewed', 'browned', 'sear', 'seared', 'render',
        'rendered', 'internal temperature', '74°c', '74c',
        'until cooked', 'cooked through', 'fully cooked',
    ]

    all_text = ' '.join(ingredients + method_steps).lower()

    has_raw_keyword = any(kw in all_text for kw in raw_keywords)
    has_strong_cooking = any(term in all_text for term in strong_cooking_escapes)

    # PARTIAL: both raw keywords and cooking present — use raw
    # framework as it's the higher-risk framework
    if has_raw_keyword:
        return True

    # Fish + no cooking indicators at all
    fish_terms = ['salmon', 'tuna', 'yellowtail', 'hamachi',
                  'halibut', 'snapper', 'sea bass', 'mackerel',
                  'scallop', 'flounder', 'sole', 'cod',
                  'amberjack', 'kingfish', 'bream', 'trout']

    cooking_terms = ['cook', 'bake', 'roast', 'fry', 'grill',
                     'sear', 'poach', 'steam', 'boil', 'braise',
                     'simmer', 'heat', 'warm', 'temperature',
                     '74', '63', '70', '75', '180', '165']

    has_fish = any(term in all_text for term in fish_terms)
    has_cooking = any(term in all_text for term in cooking_terms)

    if has_fish and not has_cooking and not has_strong_cooking:
        return True

    return False


RAW_SERVED_HACCP_PROMPT = """You are a certified HACCP consultant and food safety scientist writing professional food safety documentation for trained culinary professionals. This recipe contains RAW-SERVED proteins — ingredients consumed without a validated kill step. Apply the full raw-served hazard framework.

Do not use markdown bold (**text**) or markdown headers (## text). Use only plain section labels followed by an em dash. Do not use the terms 'sushi-grade' or 'sashimi-grade' — these have no legal definition in any jurisdiction and no regulatory standing.

Write exactly these sections, in order:

Receiving & Purchasing — For each raw-served protein, state: Core delivery temperature required (0°C–4°C for fresh fish). Species-specific physical inspection criteria (colour, odour, texture, eye clarity if whole, gill colour if applicable, packaging integrity). Specific rejection conditions stated as observable facts. For wild-caught marine finfish: supplier must provide written freezing certification documenting completion of the parasite-destruction protocol. State the applicable standard — Canadian CFIA: -20°C for minimum 7 days, OR -35°C for minimum 15 hours. FDA (US): -20°C (-4°F) for 7 days, OR -35°C (-31°F) until frozen solid then held at -35°C for 15 hours, OR -35°C until frozen solid then -20°C for 24 hours. For farmed Atlantic salmon with documented parasite-free pellet feed: note the freezing exemption and the supplier documentation required to verify it. For any tuna or scombroid species (mackerel, mahi-mahi, amberjack, sardines, anchovies): histamine forms during temperature abuse at any point in the supply chain and cannot be destroyed by freezing, cooking, or any subsequent treatment — the cold chain from catch to plate is the sole control. Request supplier temperature log covering harvest to delivery. State that "sushi-grade" or "sashimi-grade" labelling has no regulatory meaning — supplier freezing certification is required. Note that seafood mislabelling is documented at significant rates and visual species verification at receiving is required.

Thawing — If fish is or may be frozen: approved thaw methods only — refrigerator at 0°C–4°C (preferred), or under cold running water in sealed original packaging. Prohibited under any circumstances: ambient temperature thaw. Once thawed: use within 24 hours, do not refreeze. Time and temperature log required for HACCP records.

Preparation CCPs — State the following as named CCPs:

CCP 1 — Dedicated equipment. Hazard: cross-contamination with Listeria monocytogenes, Vibrio parahaemolyticus, and Norovirus. Control: designated cutting board, knife, and prep surface for raw-served items only — no shared equipment with cooked or ready-to-eat items without a full sanitisation cycle (200ppm quaternary ammonium solution, 30 seconds contact time). Verification: sanitiser concentration test at start of each service using test strips.

CCP 2 — Preparation temperature management. Hazard: Vibrio parahaemolyticus proliferation — this organism doubles every 9 minutes at 20°C. Critical limit: fish flesh surface temperature must remain at or below 4°C throughout portioning. Return to refrigeration if surface temperature reaches 7°C. Work in small batches of maximum 200g at a time. Monitoring: infrared surface thermometer on fish flesh during prep; log temperature and time. Corrective action: return to refrigeration immediately. Discard any portion confirmed above 10°C for more than 30 minutes cumulative.

Cooking CCPs — No cooking CCP applies to this preparation. The parasite-destruction control is the supplier freezing certification documented at receiving, not a kitchen process.

Hot & Cold Holding — Portioned raw-served items must not exceed 30 minutes at ambient room temperature before service (reduce to 15 minutes when kitchen ambient exceeds 25°C). If presented on ice: use potable-water ice only, vessel must actively drain — fish must not sit in standing meltwater as this accelerates bacterial growth. Replace ice when approximately 80% melted. Do not re-plate portions that have been at ambient temperature for the maximum time — discard.

Allergen Flags — List all allergens present using precise sub-category terminology. Finfish allergens are distinct from crustacean shellfish allergens — a customer with a shellfish (crustacean) allergy may safely consume finfish, and vice versa. State the specific species. Flag hidden allergen sources specific to this recipe: soy sauce contains soy and often gluten; tamari may contain wheat traces despite gluten-free labelling; wasabi served in most restaurants contains horseradish and mustard, not actual Wasabia japonica; sesame in ponzu, dipping sauces, or garnishes; sodium metabisulfite on imported crustaceans. Flag cross-contact risks at preparation.

Storage — Raw fish for raw service: 0°C–2°C maximum (not 4°C — raw fish held for raw consumption requires colder storage than the standard 4°C danger zone limit). Maximum 24–48 hours from delivery if fresh, or 24 hours from thaw if previously frozen. Store in leak-proof container on bottom shelf of dedicated fish refrigeration where possible. Label with: species name, supplier, delivery date and time, thaw date and time if applicable, use-by date and time, fish allergen declaration. Raw fish stored separately from raw meat at all times.

Personal Hygiene Triggers — Mandatory handwash after handling raw fish and before touching any ready-to-eat garnishes, serving vessels, or condiments. Change gloves between handling raw fish and handling any other ingredient. Any food handler experiencing gastrointestinal illness must be excluded from raw-served food preparation entirely — Norovirus is shed in large quantities before symptoms resolve and there is no kill step in this preparation to protect the consumer.

STANDARDS: Every critical limit must include a number and unit. Every CCP must state a corrective action. No vague language. No bullet-point walls — write in coherent professional prose. No repetition between sections."""


COOKED_HACCP_PROMPT = """You are a certified HACCP consultant writing professional food safety documentation for trained culinary professionals. This recipe involves cooked proteins — apply the standard cooked-protein HACCP framework.

Do not use markdown bold (**text**) or markdown headers (## text). Use only plain section labels followed by an em dash.

Write these sections, omitting any that genuinely do not apply:

Receiving & Purchasing — For each protein and high-risk ingredient: required delivery temperature (core temp), species-specific physical inspection criteria (colour, odour, texture, packaging integrity), specific rejection conditions as observable facts.

Preparation CCPs — Cross-contamination risks specific to this recipe. Name the organism (Salmonella, Campylobacter, Listeria as relevant to each protein). State the control measure and verification method. Name the specific handwash trigger points.

Cooking CCPs — For each protein: name the CCP, the specific pathogen targeted, the critical limit as internal temperature °C/°F AND minimum hold time at that temperature (not just the temperature alone), the monitoring method (probe placement, calibrated instrument), and the corrective action if the limit is not met.

Cooling — Only if components are cooked ahead. Two-stage requirement: Stage 1 — 60°C to 21°C within 2 hours. Stage 2 — 21°C to 4°C within a further 4 hours. Total maximum 6 hours. Monitoring: probe at 1-hour intervals, log times and temperatures. Corrective action: if Stage 1 not achieved in 2 hours, discard.

Hot & Cold Holding — Minimum hot hold 60°C, maximum cold hold 4°C. Maximum time in danger zone 4°C–60°C: 2 hours cumulative before mandatory discard.

Reheating — Only if applicable. Minimum 74°C held for 15 seconds, monitored with probe in thickest portion. Reheat once only — discard if temperature not achieved.

Allergen Flags — All major allergens present. Flag hidden sources specific to this recipe. Note cross-contact risks at preparation.

Storage — Refrigeration temperature, maximum duration, container type, label requirements (date, time, allergens). Separation requirements.

Personal Hygiene Triggers — Specific mandatory handwash and glove-change points for this recipe. 3–5 sentences.

STANDARDS: Every critical limit must include a number and unit. Every CCP must state a corrective action. No vague language. No bullet-point walls — write in coherent professional prose. No repetition."""


@app.route("/api/haccp", methods=["POST"])
def haccp_analysis():
    data = request.get_json()
    title = data.get("title", "Untitled")
    ingredients = data.get("ingredients", [])
    method_steps = data.get("method_steps", [])
    recipe_uuid = data.get("uuid")

    if not method_steps:
        return jsonify(error="No method steps provided"), 400

    try:
        is_raw = _detect_raw_served(ingredients, method_steps)
        system_prompt = RAW_SERVED_HACCP_PROMPT if is_raw else COOKED_HACCP_PROMPT

        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": _build_recipe_user_msg(title, ingredients, method_steps)}],
        )
        haccp_text = resp.content[0].text

        # Extract allergens via a cheap/fast second call
        allergens = []
        try:
            allergen_resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                system="Extract all food allergens mentioned in this HACCP brief. Return ONLY a JSON array of allergen name strings, e.g. [\"Milk\", \"Wheat\", \"Fish\"]. No other text.",
                messages=[{"role": "user", "content": haccp_text}],
            )
            allergens = json.loads(allergen_resp.content[0].text)
        except Exception:
            pass  # Allergen extraction failure doesn't block HACCP

        # Persist allergens to recipe if uuid provided
        if recipe_uuid and allergens:
            try:
                recipes = load_recipes()
                for r in recipes:
                    if r["uuid"] == recipe_uuid:
                        r["allergens"] = allergens
                        save_recipes(recipes)
                        break
            except Exception:
                pass  # Persistence failure doesn't block response

        return jsonify(haccp=haccp_text, allergens=allergens)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/kitchen-notes", methods=["POST"])
def kitchen_notes():
    data = request.get_json()
    title = data.get("title", "Untitled")
    ingredients = data.get("ingredients", [])
    method_steps = data.get("method_steps", [])

    if not method_steps:
        return jsonify(error="No method steps provided"), 400

    try:
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="You are a head chef writing a quick food safety reference card for your kitchen team. Write a concise, practical food safety note for this recipe — the kind that gets laminated and clipped to the pass.\n\nDo not use markdown bold (**text**) or markdown headers (## text). Use only plain section labels followed by an em dash.\n\nStructure with exactly these sections:\n\nKey Temperatures — list every temperature target in this recipe. Format: [Item]: [°C] / [°F]. Include cooking targets, holding temps, and fridge storage.\n\nWatch Points — the 2–3 moments in this recipe where a cook can make a food safety mistake. One sentence each. Plain language, not clinical.\n\nAllergens — list all allergens present. Flag any hidden ones a cook might miss.\n\nStorage — fridge temp, how long it keeps, container, label requirement. Two sentences maximum.\n\nHandwash Points — the specific moments in this recipe where hands must be washed. One sentence.\n\nTone: direct, practical, how a good head chef talks to their team. No jargon. No repetition. Punchy.",
            messages=[{"role": "user", "content": _build_recipe_user_msg(title, ingredients, method_steps)}],
        )
        return jsonify(notes=resp.content[0].text)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/haccp/<slug>/pdf")
def haccp_pdf(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT name, description FROM recipes WHERE slug = %s", (slug,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if not recipe:
        return "Recipe not found", 404
    name = html_mod.escape(recipe['name'])
    desc = html_mod.escape((recipe.get('description') or '')[:300])
    date_str = datetime.now().strftime('%Y-%m-%d')
    haccp_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{{font-family:Arial,sans-serif;font-size:11px;color:#333;margin:2cm}}
h1{{font-size:16px;border-bottom:2px solid #C9A84C;padding-bottom:8px}}
h2{{font-size:13px;margin-top:16px}}
.critical{{color:#cc0000;font-weight:bold}}
.footer{{font-size:9px;color:#999;border-top:1px solid #eee;padding-top:8px;margin-top:20px}}
</style></head><body>
<h1>HACCP Brief — {name}</h1>
<p>Generated: {date_str}</p>
{f'<p>{desc}</p>' if desc else ''}
<p class="footer">Provenance · Enhanced steps are AI-assisted suggestions. Always verify food safety temperatures with applicable local regulations.</p>
</body></html>"""
    try:
        pdf_bytes = WeasyHTML(string=haccp_html).write_pdf()
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                         as_attachment=True, download_name=f'haccp-{slug}.pdf')
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/export-pdf", methods=["POST"])
def export_pdf():
    from weasyprint import HTML as WeasyHTML

    data = request.get_json()
    title = html_mod.escape(data.get("title", "Untitled"))
    mode = html_mod.escape(data.get("mode", ""))
    content = data.get("content", "")
    date = html_mod.escape(data.get("date", ""))

    html_str = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  @page {{
    size: A4;
    margin: 2cm;
    @bottom-left {{ content: "Generated by Provenance"; font-size: 8pt; color: #999; }}
    @bottom-right {{ content: "Page " counter(page); font-size: 8pt; color: #999; }}
  }}
  body {{ font-family: Georgia, 'Times New Roman', serif; font-size: 11pt; line-height: 1.8; color: #1a1a1a; }}
  .wordmark {{ font-size: 10pt; font-weight: 700; color: #8B2C1A; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.25rem; }}
  h1 {{ font-size: 16pt; margin: 0.25rem 0 0.15rem; }}
  .mode-label {{ font-size: 9pt; color: #666; text-transform: uppercase; letter-spacing: 0.08em; }}
  .date {{ position: absolute; top: 0; right: 0; font-size: 9pt; color: #999; }}
  .header {{ position: relative; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 1px solid #ddd; }}
  h4 {{ font-size: 11pt; margin: 1.2rem 0 0.3rem; padding-left: 0.6rem; border-left: 3px solid #C0392B; }}
</style></head><body>
  <div class="header">
    <div class="wordmark">Provenance</div>
    <h1>{title}</h1>
    <div class="mode-label">{mode}</div>
    {f'<div class="date">{date}</div>' if date else ''}
  </div>
  {content}
</body></html>"""

    pdf_bytes = WeasyHTML(string=html_str).write_pdf()
    filename = f"{title.replace(' ', '_')}_{mode.replace(' ', '_')}.pdf"
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/allergens")
def allergen_matrix_page():
    return send_file("allergen_matrix.html")


@app.route("/api/allergen-matrix")
def allergen_matrix_data():
    recipes = load_recipes()
    result = [
        {"uuid": r["uuid"], "title": r["title"], "allergens": r["allergens"]}
        for r in recipes
        if r.get("allergens")
    ]
    result.sort(key=lambda x: x["title"].lower())
    return jsonify(result)


# ─── Ingredient Intelligence API ─────────────────────────────────────────────

@app.route("/ingredients")
def ingredients_crm():
    return send_file("ingredients_crm.html")


@app.route("/ingredients/showcase")
def ingredients_showcase():
    """Ingredient Intelligence dashboard with live DB data."""
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Hero stats
    cur.execute("SELECT COUNT(*) AS count FROM ingredient_products")
    total_products = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM suppliers WHERE is_active = TRUE")
    total_suppliers = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM product_suppliers")
    total_links = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(DISTINCT product_id) AS count FROM product_suppliers")
    connected_products = cur.fetchone()["count"]

    stats = {
        "products": total_products,
        "suppliers": total_suppliers,
        "links": total_links,
        "connected_products": connected_products,
    }

    # Top suppliers by product count
    cur.execute("""
        SELECT s.name, s.country, COUNT(*) AS products
        FROM product_suppliers ps
        JOIN suppliers s ON ps.supplier_id = s.id
        GROUP BY s.name, s.country
        ORDER BY products DESC
        LIMIT 20
    """)
    top_suppliers = [dict(r) for r in cur.fetchall()]

    # Products by category
    cur.execute("""
        SELECT category, COUNT(*) AS count
        FROM ingredient_products
        GROUP BY category
        ORDER BY count DESC
    """)
    categories = [dict(r) for r in cur.fetchall()]

    # Suppliers by country
    cur.execute("""
        SELECT country, COUNT(*) AS count
        FROM suppliers
        WHERE is_active = TRUE
        GROUP BY country
        ORDER BY count DESC
    """)
    countries = [dict(r) for r in cur.fetchall()]

    # Pat's Rule demo — soy sauce supply chain
    cur.execute("""
        SELECT ip.name AS product_name, s.name AS supplier_name, s.country,
               ps.role, ps.region
        FROM product_suppliers ps
        JOIN ingredient_products ip ON ps.product_id = ip.id
        JOIN suppliers s ON ps.supplier_id = s.id
        WHERE ip.name ILIKE '%%soy sauce%%'
        LIMIT 10
    """)
    chain_rows = [dict(r) for r in cur.fetchall()]

    # Recent products
    cur.execute("""
        SELECT name, category, origin_brand, origin_country
        FROM ingredient_products
        ORDER BY id DESC
        LIMIT 20
    """)
    recent_products = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("ingredients_showcase.html",
        stats=stats,
        top_suppliers=top_suppliers,
        categories=categories,
        countries=countries,
        chain_rows=chain_rows,
        recent_products=recent_products,
    )


@app.route("/api/ingredients/stats")
def ingredients_stats():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM ingredient_products")
    products = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM suppliers WHERE is_active = TRUE")
    suppliers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM product_suppliers")
    links = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({"products": products, "suppliers": suppliers, "links": links})


@app.route("/api/ingredients/suppliers")
def ingredient_suppliers():
    """Pat's Rule endpoint: find suppliers for a product, filtered by region."""
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    product_id = request.args.get("product_id", type=int)
    product_name = request.args.get("product_name", "").strip()
    region = request.args.get("region", "").strip()
    role = request.args.get("role", "").strip().upper()

    if not product_id and not product_name:
        return jsonify({"error": "Provide product_id or product_name"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Find the product
    if product_id:
        cur.execute("SELECT * FROM ingredient_products WHERE id = %s", (product_id,))
    else:
        cur.execute("SELECT * FROM ingredient_products WHERE LOWER(name) = LOWER(%s)", (product_name,))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        return jsonify({"error": "Product not found"}), 404

    pid = product["id"]

    # Build supplier query with optional filters
    query = """
        SELECT s.id, s.name, s.city, s.state_province, s.country,
               s.supplier_type, s.website, s.contact_email, s.contact_phone,
               ps.role, ps.region, ps.is_primary, ps.notes AS link_notes
        FROM product_suppliers ps
        JOIN suppliers s ON ps.supplier_id = s.id
        WHERE ps.product_id = %s
    """
    params = [pid]

    if role in ("ORIGIN", "PROVIDER"):
        query += " AND ps.role = %s"
        params.append(role)

    if region:
        # Expand region to cover nationwide/worldwide variants.
        # ORIGIN suppliers (provenance) always appear; region filter applies to PROVIDERs only.
        _CA_PROVINCES = {'BC','AB','SK','MB','ON','QC','NB','NS','PE','NL','NT','YT','NU'}
        region_terms = [region]
        if region in _CA_PROVINCES:
            region_terms += ['nationwide_CA', 'Western_Canada']
        else:
            region_terms += ['nationwide_US']
        query += " AND (ps.role = 'ORIGIN' OR ps.region && %s::text[])"
        params.append(region_terms)

    query += " ORDER BY ps.role, ps.is_primary DESC, s.name"
    cur.execute(query, params)
    rows = cur.fetchall()

    # Separate into origin and providers
    origin = None
    providers = []
    for row in rows:
        supplier_data = {
            "id": row["id"],
            "name": row["name"],
            "city": row["city"],
            "state_province": row["state_province"],
            "country": row["country"],
            "supplier_type": row["supplier_type"],
            "website": row["website"],
            "contact_email": row["contact_email"],
            "contact_phone": row["contact_phone"],
            "region": row["region"],
            "is_primary": row["is_primary"],
            "notes": row["link_notes"],
        }
        if row["role"] == "ORIGIN" and origin is None:
            origin = supplier_data
        elif row["role"] == "PROVIDER":
            providers.append(supplier_data)

    # Convert product row (RealDictRow) to plain dict for JSON
    product_data = {
        "id": product["id"],
        "name": product["name"],
        "category": product["category"],
        "description": product["description"],
        "origin_brand": product["origin_brand"],
        "origin_country": product["origin_country"],
        "region_tags": product["region_tags"],
    }

    cur.close()
    conn.close()

    return jsonify({
        "product": product_data,
        "origin": origin,
        "providers": providers,
    })


@app.route("/api/ingredients/products")
def ingredient_products_list():
    """List products with optional category/country filter."""
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    category = request.args.get("category", "").strip()
    country = request.args.get("country", "").strip()
    search = request.args.get("q", "").strip()
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT id, name, category, origin_brand, origin_country FROM ingredient_products WHERE 1=1"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)
    if country:
        query += " AND origin_country = %s"
        params.append(country)
    if search:
        query += " AND LOWER(name) LIKE %s"
        params.append(f"%{search.lower()}%")

    query += " ORDER BY name LIMIT %s OFFSET %s"
    params.extend([min(limit, 200), offset])

    cur.execute(query, params)
    products = [dict(row) for row in cur.fetchall()]

    # Get total count
    count_query = "SELECT COUNT(*) FROM ingredient_products WHERE 1=1"
    count_params = []
    if category:
        count_query += " AND category = %s"
        count_params.append(category)
    if country:
        count_query += " AND origin_country = %s"
        count_params.append(country)
    if search:
        count_query += " AND LOWER(name) LIKE %s"
        count_params.append(f"%{search.lower()}%")
    cur.execute(count_query, count_params)
    total = cur.fetchone()["count"]

    cur.close()
    conn.close()

    return jsonify({"products": products, "total": total, "limit": limit, "offset": offset})


# ─── Ingredient-to-product matching ──────────────────────────────────────────

_PREP_MODIFIERS = [
    "ground", "dried", "fresh", "pickled", "smoked", "roasted", "toasted",
    "fried", "fermented", "frozen", "canned", "powdered", "whole", "sliced",
    "chopped", "minced", "crushed", "grated", "shredded", "blanched",
    "preserved", "shaved", "zested", "cured", "infused",
    "salted", "marinated", "brined", "freeze-dried", "confit",
    "silken", "firm", "extra-firm",  # tofu texture grades
    "crudo", "cotto",               # Italian culinary terms: raw / cooked
]

# Prep states that fundamentally transform the ingredient — "ginger" ≠ "pickled ginger"
_STRONG_PREP_MODIFIERS = frozenset([
    "ground", "dried", "pickled", "smoked", "roasted", "toasted",
    "fried", "fermented", "frozen", "canned", "powdered", "preserved", "cured",
    "salted", "marinated", "brined", "freeze-dried", "confit",
])

_FALSE_FRIENDS = [
    # Structurally distinct ingredients sharing a base word
    ("kaffir lime", "lime"),
    ("lime leaves", "lime"),
    ("lime leaf", "lime"),
    ("lemongrass", "lemon"),
    ("lemon grass", "lemon"),
    ("galangal", "ginger"),
    ("fish sauce", "soy sauce"),
    ("coconut milk", "milk"),
    ("coconut cream", "cream"),
    ("palm sugar", "sugar"),
    # Note: ("rice wine", "wine") and ("rice vinegar", "vinegar") removed — scoring
    # naturally keeps these below threshold, and the pairs caused "rice wine vinegar"
    # ingredient to be blocked from rice vinegar products via substring matching.
    ("sesame oil", "olive oil"),
    # ("tamarind", "tamarind paste") removed — tamarind ingredient should match
    # tamarind paste/concentrate products since that's the common form available.
    ("star anise", "anise"),
    ("sichuan pepper", "black pepper"),
    ("szechuan pepper", "black pepper"),
    ("sichuan peppercorn", "black peppercorn"),
    ("szechuan peppercorn", "black peppercorn"),
    ("truffle", "truffle oil"),
    ("shiso", "basil"),
    ("dashi", "stock"),
    ("dashi", "broth"),
    # Specific varietals must not match the generic base ingredient
    ("finger lime", "lime"),
    ("blood lime", "lime"),
    ("desert lime", "lime"),
    ("makrut lime", "lime"),
    ("persian lime", "lime"),
    ("key lime", "lime"),
    # Processed/derived products must not match the raw source
    ("coconut milk", "coconut"),
    ("coconut cream", "coconut"),
    ("coconut water", "coconut"),
    ("coconut oil", "coconut"),
    # "cloves" the spice vs "garlic cloves" (unit/portion)
    ("ground cloves", "garlic"),
    ("whole cloves", "garlic"),
    # Botanically/culinarily distinct plants and spice blends that share a base name
    ("lemon myrtle", "lemon"),
    ("lemon thyme", "lemon"),
    ("lemon verbena", "lemon"),
    ("lemon pepper", "lemon"),
    # Transformed/processed varieties must not match the raw base
    ("black garlic", "garlic"),
    ("black cardamom", "cardamom"),
    ("coconut sugar", "sugar"),
    ("muscovado sugar", "sugar"),
    ("demerara sugar", "sugar"),
    # Geographic/contextual words that appear in unrelated product names
    ("moreton bay bug", "bay"),
    # Botanically distinct "lemon X" plants must not match the lemon fruit
    ("lemon eucalyptus", "lemon"),
    ("lemon aspen", "lemon"),
    # Chilli/pepper varieties vs the generic base
    ("ancho chilli", "chilli"),
    ("chipotle chilli", "chilli"),
    ("ancho chili", "chili"),
    ("chipotle chili", "chili"),
    ("kashmiri chilli", "chilli"),
    ("kashmiri chili", "chili"),
    ("calabrian chilli", "chilli"),
    ("calabrian chili", "chili"),
    # Freeze-dried/powdered fruit/herb ≠ fresh — spice powders are NOT listed here
    # (turmeric, cumin, coriander are nearly always used in dried/powder form)
    ("lemon powder", "lemon"),
    ("basil powder", "basil"),
    ("tomato powder", "tomato"),
    # Flavoured corn/snack products where the primary ingredient is NOT the flavouring
    ("chilli corn", "chilli"),
    ("chili corn", "chili"),
    # Oyster mushroom varieties must not match shellfish oyster, and vice versa
    ("king oyster", "oyster"),
    ("oyster mushroom", "oyster"),
    # Australian native plants with misleading common names
    ("strawberry gum", "strawberry"),
    # Fish species with misleading common names
    ("orange roughy", "orange"),
    # Note: floral waters ("orange blossom water", "rose water") are handled by
    # "water" in _CATEGORY_WORDS — no false-friend entries needed.
    # Spices derived from fruit ≠ the fruit itself
    ("mahlab", "cherry"),
    # Australian native / exotic species ≠ common fruit
    ("kakadu plum", "plum"), ("davidson plum", "plum"), ("illawarra plum", "plum"),
    # Compound-word fish/seafood names ≠ generic "fish"
    ("flying fish", "fish"), ("catfish", "fish"), ("swordfish", "fish"),
    ("blowfish", "fish"), ("cuttlefish", "fish"),
    # Fish roe ≠ the whole fish (skip logic allows "trout roe" ingredient → "Trout Roe" product)
    ("salmon roe", "salmon"), ("trout roe", "trout"), ("flying fish roe", "flying fish"),
    ("capelin roe", "capelin"), ("herring roe", "herring"),
    ("cod roe", "cod"), ("tuna roe", "tuna"), ("sturgeon roe", "sturgeon"),
    # Specialty / derived products ≠ generic ingredient
    ("pearl meat", "meat"), ("pearl oyster", "oyster"),
    # Specialty flours ≠ generic "flour"
    ("wattleseed flour", "flour"), ("almond flour", "flour"), ("buckwheat flour", "flour"),
    ("chickpea flour", "flour"), ("teff flour", "flour"), ("chestnut flour", "flour"),
    ("spelt flour", "flour"), ("rye flour", "flour"), ("corn flour", "flour"),
    ("coconut flour", "flour"), ("cassava flour", "flour"), ("tapioca flour", "flour"),
    ("rice flour", "flour"), ("rice flour", "rice"),
    # Exotic / specialty meats ≠ generic "meat"
    ("reindeer meat", "meat"), ("kangaroo meat", "meat"), ("venison", "meat"),
    ("bison meat", "meat"),
    # Molecular/food-science products ≠ their colloquial ingredient name
    ("transglutaminase", "meat"), ("meat glue", "meat"),
    # Traditional preparations ≠ the base ingredient
    ("tiger bone wine", "wine"), ("rice wine vinegar", "wine"),
    # Specific body parts / offal ≠ generic protein
    ("chicken feet", "chicken"), ("chicken liver", "chicken"), ("chicken wing", "chicken"),
    ("chicken cartilage", "chicken"), ("chicken heart", "chicken"), ("chicken gizzard", "chicken"),
    # Preserved/transformed egg products
    ("century egg", "egg"), ("salted egg", "egg"), ("tea egg", "egg"),
    # Garlic "cloves" (the part) ≠ clove (the spice Syzygium aromaticum)
    ("garlic cloves", "clove"),
    # Colour-plus-category confusion
    ("black pepper", "black bean"), ("black bean", "black pepper"),
    # Potato variety disambiguation — sweet potato ≠ regular potato
    ("sweet potato", "potato"),
    # Specialty molasses ≠ generic molasses (these are distinct condiments)
    ("pomegranate molasses", "molasses"), ("carob molasses", "molasses"),
    ("date molasses", "molasses"), ("grape molasses", "molasses"),
    ("dibs rumman", "molasses"),
    # Organ meat homonym — kidney bean ≠ kidney (offal)
    ("kidney beans", "kidney"),
    # Plant parts ≠ the fruit/vegetable itself
    ("banana blossom", "banana"), ("banana flower", "banana"),
    ("beach banana", "banana"),
    # Geographic/contextual words that appear in unrelated product names
    ("ariake bay", "bay"),
    # Curry flavor-type ≠ chicken curry paste
    ("green curry", "chicken"),
    ("red curry", "chicken"),
    ("yellow curry", "chicken"),
]

# Functional category words: if the ingredient contains one of these,
# the product must too — "rice vinegar" must not match a "rice" product.
# The check is bidirectional: "sesame" must not match "Sesame Oil" either.
_CATEGORY_WORDS = frozenset([
    "vinegar", "sauce", "oil", "paste", "syrup", "flour",
    "cream", "milk", "juice", "stock", "broth", "wine", "butter", "cheese",
    "honey", "evoo", "balsamic", "honeycomb",
    # jams / preserves — "strawberry" must not match "Strawberry Jam"
    "jam", "jelly", "marmalade", "chutney", "relish", "compote", "preserve",
    # fermented condiments / spice pastes — "rose" must not match "Rose Harissa"
    "gochujang", "miso", "doenjang", "ganjang", "doubanjiang", "harissa",
    # floral waters — "orange" must not match "Orange Blossom Water"
    "water",
    # pasta types — "chicken" must not match "Chicken Tortelloni" etc.
    "ravioli", "tortelloni", "tortellini", "cappelletti", "lasagna",
    "cannelloni", "linguine", "noodle", "tagliatelle", "pappardelle", "gnocchi",
    # spirits — "sweet potato" must not match "Shochu — Imo (Sweet Potato)"
    "shochu", "sake", "whisky", "whiskey", "bourbon", "rum", "vodka", "gin",
    "mezcal", "tequila", "brandy", "cognac", "calvados", "armagnac",
    # "powder" intentionally excluded: turmeric/cumin/coriander ≈ their powder forms
])

# Form/part words — descriptors of how an ingredient appears in a recipe that
# don't change what the ingredient fundamentally IS, so they shouldn't affect
# token overlap scoring.  e.g. "dried shiitake mushrooms" → core token "shiitake".
# NOTE: form words are only stripped when doing so leaves ≥1 content token;
#       if stripping would leave nothing, fall back to the prep-stripped set.
_FORM_WORDS = frozenset([
    "leaf", "leaves", "seed", "seeds", "sprig", "sprigs",
    "stalk", "stalks", "stick", "sticks",          # "cinnamon stick" → "cinnamon"
    "floret", "florets", "fillet", "fillets",
    "piece", "pieces", "mushroom", "mushrooms", "shaving", "shavings",
    # Geographic descriptor — "Cap Bon Region" adds no culinary identity
    "region", "regional",
    # Quality/origin certification acronyms — add no culinary meaning
    "dop", "igp", "aop", "aoc", "pdo", "pgi", "doc", "docg",
])

_CUISINE_TO_REGIONS = {
    "thai": ["southeast_asia", "thailand"],
    "indonesian": ["southeast_asia", "indonesia"],
    "malaysian": ["southeast_asia", "malaysia"],
    "vietnamese": ["southeast_asia", "vietnam"],
    "indian": ["south_asia", "india"],
    "japanese": ["east_asia", "japan"],
    "chinese": ["east_asia", "china"],
    "korean": ["east_asia", "korea"],
    "mexican": ["latin_america", "mexico"],
    "italian": ["europe", "italy"],
    "french": ["europe", "france"],
    "middle eastern": ["middle_east"],
}

_PRODUCTS_CACHE = (None, 0.0)  # (products_list, timestamp)
_PRODUCTS_CACHE_TTL = 300  # 5 minutes


# Spelling variants that map to canonical form used in the product database.
# Applied word-by-word in _normalise_ingredient ONLY — not to product names.
# Keep this list conservative: only add aliases where DB clearly uses one spelling.
_SPELLING_ALIASES = {
    "szechuan": "sichuan",
    "szechwan": "sichuan",
    "sechuan": "sichuan",
    "kecap": "ketjap",        # Indonesian soy sauce variant spellings
    # American "chili" → British "chilli" (product DB uses "chilli" spelling)
    "chili": "chilli",
    "chile": "chilli",
    "chiles": "chilli",
    # "parmesan" is the common English name for Parmigiano Reggiano
    "parmesan": "parmigiano",
    # "kaffir lime" is a deprecated name; product DB uses "makrut"
    "kaffir": "makrut",
    # Plural "leaves" → singular "leaf" so "kaffir lime leaves" → "makrut lime leaf"
    # and matches the "Makrut Lime Leaf" product (singular) correctly.
    "leaves": "leaf",
}

# Short stop-words and prepositions that should not participate in token scoring.
# Also applied to purely numeric tokens (batch numbers, percentages-as-ints, etc.)
_NOISE_TOKENS = frozenset([
    # English articles / prepositions
    "of", "the", "a", "an", "and", "or", "from", "in", "with", "by", "at",
    # French / Italian / Spanish / German prepositions that appear in place names
    "de", "du", "di", "da", "sur", "sous", "en", "aux",
    "von", "van", "le", "la", "les", "el", "al", "lo", "gli",
    # Administrative geographic suffixes — never culinary identifiers
    "prefecture",
    # Aging / time unit words — "72-Month", "10-Year" add no ingredient identity
    "month", "months", "year", "years",
])


def _normalise_ingredient(raw_name):
    """Strip parentheticals, trailing annotations, leading quantities; lowercase.
    Also applies spelling aliases (szechuan→sichuan, chilli→chili etc.)
    """
    s = raw_name.lower().strip()
    s = _re.sub(r'\([^)]*\)', '', s)  # remove (...)
    s = _re.sub(r',.*$', '', s)  # remove trailing annotations after comma
    s = _re.sub(r'^[\d./\s½¼¾⅓⅔]+', '', s)  # strip leading quantities
    s = _re.sub(r'^(cups?|tbsp|tsp|tablespoons?|teaspoons?|oz|g|kg|ml|l|lb|bunch|handful|pinch|dash)\b\s*', '', s)
    s = s.strip()
    # Apply word-level spelling aliases
    words = s.split()
    words = [_SPELLING_ALIASES.get(w, w) for w in words]
    return ' '.join(words)


def _normalise_product(name):
    """Primary normalisation for exact-match detection.

    Strips parentheticals and em-dash variant descriptors.
    e.g. "Pickled Ginger (Gari)" → "pickled ginger"
         "Galangal — Thai (Kha)" → "galangal"
         "Grove Avocado Oil — Lime Infused" → "grove avocado oil"
    """
    s = name.lower().strip()
    s = _re.sub(r'\([^)]*\)', '', s)          # strip (...) like "(Gari)", "(Organic)"
    s = _re.sub(r'\s*[—–\-]{2,}\s*.*$', '', s)  # strip " — Variant" / " -- Descriptor"
    s = _re.sub(r'\s*—\s*.*$', '', s)          # strip em-dash suffix "Galangal — Thai"
    s = _re.sub(r'\s+', ' ', s)
    return s.strip()


def _normalise_product_tokens(name):
    """Extended normalisation for token-based scoring.

    Keeps parenthetical CONTENT (removes only the paren characters) AND keeps
    words after the em-dash separator, so that prep modifiers and ingredient
    types embedded anywhere in the product name are visible for scoring.
    e.g. "Ikura (Salmon Roe) — Hokkaido Wild" → "ikura salmon roe hokkaido wild"
         "Fig — Kadota (Dried)"               → "fig kadota dried"
         "Pickled Ginger (Gari)"               → "pickled ginger gari"
    The primary form (_normalise_product) strips the em-dash for exact matching.
    """
    s = name.lower().strip()
    s = _re.sub(r'[()]', '', s)               # remove paren chars but keep content
    s = _re.sub(r'[—–]', ' ', s)             # replace em/en dashes with space (keep words)
    s = _re.sub(r'\s+', ' ', s)
    return s.strip()


def _extract_prep_modifier(normalised):
    """Detect first prep modifier in string."""
    for mod in _PREP_MODIFIERS:
        if mod in normalised.split():
            return mod
    return None


def _simple_stem(token):
    """Strip common plural/form suffixes so 'anchovies'=='anchovy', 'seeds'=='seed'.
    Also maps form-equivalent tokens: 'peppercorn' → 'pepper'.
    """
    # Form-equivalence mappings (same ingredient, different form word or spelling)
    if token in ("peppercorn", "peppercorns"):
        return "pepper"
    if token in ("chili", "chiles", "chile"):
        return "chilli"  # map American spelling to British (products use "chilli")
    if len(token) <= 4:
        return token
    if token.endswith('ies'):
        return token[:-3] + 'y'       # anchovies→anchovy, berries→berry
    if token.endswith('s') and not token.endswith('ss'):
        return token[:-1]              # seeds→seed, olives→olive, mushrooms→mushroom
    return token


def _is_false_friend(ing_norm, prod_norm):
    """Check both directions against false-friends list.

    When one pair member is a substring of the other (e.g. "lemon" ⊂ "lemon myrtle"),
    we skip blocking if BOTH strings share the longer term — that means they're about
    the same thing and just differ by a form word (e.g. "lemon myrtle leaf" vs "lemon myrtle").
    """
    for a, b in _FALSE_FRIENDS:
        if (a in ing_norm and b in prod_norm) or (b in ing_norm and a in prod_norm):
            longer = a if len(a) >= len(b) else b
            if longer in ing_norm and longer in prod_norm:
                continue  # same compound base — not actually false friends
            return True
    return False


def _score_match(ing_norm, ing_prep, prod_name_raw, prod_region_tags, cuisine_tags):
    """Score how well a product matches an ingredient.

    Returns 2.0 for an exact match (sentinel — beats any partial match),
    0.0 for a hard-blocked match, or a float in (0.0, 1.0] otherwise.
    """
    prod_name_norm = _normalise_product(prod_name_raw)
    # Extended form: keeps parenthetical content for richer token matching
    # e.g. "Ikura (Salmon Roe) — Hokkaido Wild" → "ikura salmon roe"
    prod_name_tokens_src = _normalise_product_tokens(prod_name_raw)

    # Rule 1 — Exact match: highest priority, no further checks needed
    if ing_norm == prod_name_norm:
        # Even on exact match, block if product's extended form reveals a strong prep that
        # the ingredient lacks — e.g. "fig" must not sentinel-match "Fig — Kadota (Dried)"
        _prod_src_tokens = set(prod_name_tokens_src.split())
        if not ing_prep and (_prod_src_tokens & _STRONG_PREP_MODIFIERS):
            pass  # fall through to full scoring (strong prep rule will block it)
        else:
            return 2.0

    # Rule 3 — False friends: check both primary form and extended (parenthetical-included) form,
    # since token scoring uses the extended form which may expose additional content.
    if _is_false_friend(ing_norm, prod_name_norm) or _is_false_friend(ing_norm, prod_name_tokens_src):
        return 0.0

    # Token-based scoring: exclude prep modifiers AND form/part words, then stem plurals
    _prep_excl = set(_PREP_MODIFIERS)
    _full_excl = _prep_excl | _FORM_WORDS

    def _clean_tokens(raw_set):
        """Remove noise: stop-words, pure numeric tokens (batch numbers, ages, %)."""
        result = set()
        for t in raw_set:
            if t in _NOISE_TOKENS:
                continue
            if _re.match(r'^\d+\.?\d*$', t):  # e.g. "1.34", "72", "400"
                continue
            result.add(t)
        return result

    ing_tokens_full = _clean_tokens(set(ing_norm.split()) - _full_excl)
    prod_tokens_full = _clean_tokens(set(prod_name_tokens_src.split()) - _full_excl)
    # Fallback: if form word removal empties the ingredient set (ingredient IS the form word,
    # e.g. bare "mushroom"), use prep-only exclusion for BOTH sides so the form word can
    # still match against products that have it (e.g. "Lobster Mushroom").
    ing_fell_back = not ing_tokens_full
    ing_tokens = ing_tokens_full if ing_tokens_full else _clean_tokens(set(ing_norm.split()) - _prep_excl)
    if ing_fell_back:
        prod_tokens = _clean_tokens(set(prod_name_tokens_src.split()) - _prep_excl)
    else:
        prod_tokens = prod_tokens_full if prod_tokens_full else _clean_tokens(set(prod_name_tokens_src.split()) - _prep_excl)

    if not ing_tokens or not prod_tokens:
        return 0.0

    # Stem plurals for comparison: anchovies→anchovy, seeds→seed, noodles→noodle
    # Must happen BEFORE category check so pluralised category words are caught
    ing_stems = {_simple_stem(t) for t in ing_tokens}
    prod_stems = {_simple_stem(t) for t in prod_tokens}

    # Category-word guard (bidirectional, uses stems):
    # "rice vinegar" must not match "rice"; "sesame" must not match "Sesame Oil";
    # "egg" must not match "Egg Noodles" (noodles→noodle in _CATEGORY_WORDS)
    ing_category = ing_stems & _CATEGORY_WORDS
    prod_category = prod_stems & _CATEGORY_WORDS
    if ing_category and not (ing_category & prod_stems):
        return 0.0
    if prod_category and not (prod_category & ing_stems):
        return 0.0

    intersection = ing_stems & prod_stems
    if not intersection:
        return 0.0

    # Jaccard similarity + containment (how well ingredient is covered)
    jaccard = len(intersection) / len(ing_stems | prod_stems)
    containment = len(intersection) / len(ing_stems)
    base = 0.5 * jaccard + 0.5 * containment

    # Single-token safety: if ingredient reduces to 1 content token (e.g. "bay" from "bay leaf"),
    # require a base score above 0.6 to avoid accidental geographic/contextual word matches.
    # Specific cases (e.g. "bay" → "Moreton Bay Bug") are handled via false friends.
    if len(ing_tokens) == 1 and base < 0.6:
        return 0.0

    # Rule 2 — Prep state logic
    prod_prep = _extract_prep_modifier(prod_name_tokens_src)
    prod_tokens_src_set = set(prod_name_tokens_src.split())
    prod_has_strong_prep = bool(prod_tokens_src_set & _STRONG_PREP_MODIFIERS)
    if ing_prep and prod_prep and ing_prep != prod_prep:
        # Hard block: explicit conflicting prep states (ground ≠ pickled)
        return 0.0
    elif not ing_prep and prod_has_strong_prep:
        # Hard block: ingredient unspecified, product strongly transformed
        # e.g. "ginger" must not match "pickled ginger"; "raspberry" must not match "freeze-dried raspberry"
        # Uses token-set intersection to catch ALL strong preps (not just the first one found)
        return 0.0
    elif ing_prep and not prod_prep:
        pass  # Generic product is acceptable for a prep-specified ingredient
    elif not ing_prep and prod_prep:
        base -= 0.1  # Slight penalty for mildly-specific product (e.g. "fresh")

    # Rule 4 — Cuisine context as tiebreaker
    if cuisine_tags and prod_region_tags:
        target_regions = set()
        for tag in cuisine_tags:
            target_regions.update(_CUISINE_TO_REGIONS.get(tag.lower(), []))
        if target_regions:
            prod_regions = set(r.lower() for r in prod_region_tags)
            if target_regions & prod_regions:
                base += 0.05

    return max(0.0, min(1.0, base))


def _get_all_products():
    """Fetch all products from ingredient_products, with TTL cache."""
    global _PRODUCTS_CACHE
    cached_products, cached_at = _PRODUCTS_CACHE
    if cached_products is not None and (_time.time() - cached_at) < _PRODUCTS_CACHE_TTL:
        return cached_products

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, category, description, origin_brand, origin_country, region_tags FROM ingredient_products")
    products = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()

    _PRODUCTS_CACHE = (products, _time.time())
    return products


def _get_suppliers_for_products(product_ids, region=None, country=None):
    """Batch-fetch suppliers for a list of product IDs.
    Returns dict: {product_id: {"origin": {...}|None, "providers": [...]}}
    Providers are sorted: regional > country > all, capped at 3.
    """
    if not product_ids:
        return {}
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ps.product_id, s.id, s.name, s.city, s.state_province, s.country,
               s.supplier_type, s.website, ps.role, ps.region AS ps_region, ps.is_primary
        FROM product_suppliers ps
        JOIN suppliers s ON ps.supplier_id = s.id
        WHERE ps.product_id = ANY(%s)
          AND s.is_active = TRUE
        ORDER BY ps.product_id, ps.is_primary DESC, s.name
    """, (list(product_ids),))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = {}
    for row in rows:
        pid = row[0]
        if pid not in result:
            result[pid] = {"origin": None, "providers": []}
        sup = {
            "id": row[1], "name": row[2], "city": row[3],
            "state_province": row[4], "country": row[5],
            "supplier_type": row[6], "website": row[7],
            "role": row[8], "ps_region": row[9] or [], "is_primary": row[10],
        }
        if sup["role"] == "ORIGIN":
            if result[pid]["origin"] is None:
                result[pid]["origin"] = sup
        else:
            result[pid]["providers"].append(sup)

    # Sort providers by regional proximity, cap at 3
    for pid, data in result.items():
        def _priority(s, _region=region, _country=country):
            if _region and (_region in (s["state_province"] or "") or _region in (s["ps_region"] or [])):
                return 0
            if _country and s["country"] == _country:
                return 1
            return 2
        data["providers"] = sorted(data["providers"], key=_priority)[:3]

    return result


def _format_supplier(s):
    if not s:
        return None
    return {k: s[k] for k in ("name", "city", "state_province", "country", "supplier_type", "website")}


@app.route("/api/ingredients/match", methods=["POST"])
def ingredients_match():
    """Smart ingredient-to-product matching with scoring."""
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json(silent=True) or {}
    ingredients = data.get("ingredients", [])
    cuisine_tags = data.get("cuisine_tags", [])
    region = data.get("region") or None
    country = data.get("country") or None

    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    products = _get_all_products()
    threshold = 0.5
    matches = {}

    for raw_name in ingredients:
        ing_norm = _normalise_ingredient(raw_name)
        ing_prep = _extract_prep_modifier(ing_norm)

        best_score = 0.0
        best_product = None

        for prod in products:
            score = _score_match(
                ing_norm, ing_prep, prod["name"],
                prod.get("region_tags") or [], cuisine_tags
            )
            if score > best_score:
                best_score = score
                best_product = prod

        # Rule 5 — No match is better than a wrong match
        # (exact match returns 2.0 sentinel; partial matches must clear 0.5)
        if best_score >= threshold and best_product:
            matches[raw_name] = {
                "id": best_product["id"],
                "name": best_product["name"],
                "category": best_product["category"],
                "description": best_product["description"],
                "origin_brand": best_product["origin_brand"],
                "origin_country": best_product["origin_country"],
                "score": min(round(best_score, 3), 1.0),  # cap 2.0 sentinel
            }
        else:
            matches[raw_name] = None

    if (region or country) and any(v is not None for v in matches.values()):
        matched_ids = [v["id"] for v in matches.values() if v]
        suppliers = _get_suppliers_for_products(matched_ids, region=region, country=country)
        for v in matches.values():
            if v:
                sup = suppliers.get(v["id"], {})
                v["origin"] = _format_supplier(sup.get("origin"))
                v["providers"] = [_format_supplier(p) for p in sup.get("providers", [])]

    return jsonify({"matches": matches})


@app.route("/api/ingredients/suppliers/list")
def suppliers_list():
    """List all suppliers with optional filters."""
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    country = request.args.get("country", "").strip()
    supplier_type = request.args.get("type", "").strip()

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """SELECT id, name, city, state_province, country, supplier_type,
               website, contact_email, service_region, categories_served
               FROM suppliers WHERE is_active = TRUE"""
    params = []

    if country:
        query += " AND country = %s"
        params.append(country)
    if supplier_type:
        query += " AND supplier_type = %s"
        params.append(supplier_type)

    query += " ORDER BY name"
    cur.execute(query, params)
    suppliers = [dict(row) for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify({"suppliers": suppliers, "total": len(suppliers)})


@app.route("/api/search/fuzzy")
def fuzzy_search():
    """F6 — Trigram fuzzy search over ingredient products and techniques.
    Uses pg_trgm similarity. Requires idx_products_name_trgm and
    idx_techniques_name_trgm indexes (already present in DB).
    Query params:
      q        — search term (required)
      type     — 'products', 'techniques', or 'all' (default 'all')
      limit    — max results per type (default 10, max 50)
      threshold — similarity threshold 0-1 (default 0.25)
    """
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "q is required"}), 400

    search_type = request.args.get("type", "all").lower()
    limit = min(request.args.get("limit", 10, type=int), 50)
    threshold = request.args.get("threshold", 0.25, type=float)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    results = {}

    if search_type in ("products", "all"):
        cur.execute("""
            SELECT id, name, category, origin_brand, origin_country,
                   similarity(name, %s) AS sim
            FROM ingredient_products
            WHERE similarity(name, %s) > %s
            ORDER BY sim DESC
            LIMIT %s
        """, (q, q, threshold, limit))
        results["products"] = [dict(r) for r in cur.fetchall()]

    if search_type in ("techniques", "all"):
        cur.execute("""
            SELECT id, name, slug, category, origin,
                   similarity(name, %s) AS sim
            FROM technique_references
            WHERE similarity(name, %s) > %s
            ORDER BY sim DESC
            LIMIT %s
        """, (q, q, threshold, limit))
        results["techniques"] = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify({"query": q, "results": results})


@app.route("/api/autocomplete")
def autocomplete():
    """F7 — Autocomplete suggestions for search inputs.
    Uses ILIKE prefix + pg_trgm fallback for short queries.
    Query params:
      q     — partial search term (required, min 2 chars)
      type  — 'products', 'techniques', 'recipes', or 'all' (default 'all')
      limit — max results (default 8, max 20)
    Returns flat list of {id, name, type, hint} objects.
    """
    if not DATABASE_URL:
        return jsonify({"suggestions": []}), 200

    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify({"suggestions": []})

    search_type = request.args.get("type", "all").lower()
    limit = min(request.args.get("limit", 8, type=int), 20)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    suggestions = []
    per_type = max(3, limit // 3) if search_type == "all" else limit

    if search_type in ("products", "all"):
        cur.execute("""
            SELECT id, name, category AS hint
            FROM ingredient_products
            WHERE name ILIKE %s
            ORDER BY name
            LIMIT %s
        """, (q + "%", per_type))
        for row in cur.fetchall():
            suggestions.append({"id": row["id"], "name": row["name"],
                                 "hint": row["hint"], "type": "product"})

    if search_type in ("techniques", "all"):
        cur.execute("""
            SELECT id, name, origin AS hint, slug
            FROM technique_references
            WHERE name ILIKE %s
            ORDER BY name
            LIMIT %s
        """, (q + "%", per_type))
        for row in cur.fetchall():
            suggestions.append({"id": row["id"], "name": row["name"],
                                 "hint": row["hint"], "slug": row.get("slug"),
                                 "type": "technique"})

    if search_type in ("recipes", "all"):
        cur.execute("""
            SELECT id, name, cuisine AS hint, slug
            FROM recipes
            WHERE name ILIKE %s
            ORDER BY is_curated DESC, name
            LIMIT %s
        """, (q + "%", per_type))
        for row in cur.fetchall():
            suggestions.append({"id": str(row["id"]), "name": row["name"],
                                 "hint": row["hint"], "slug": row.get("slug"),
                                 "type": "recipe"})

    # If prefix search returned fewer than half the requested results,
    # supplement with trigram similarity matches (avoids duplicates by name).
    if len(suggestions) < limit // 2 and search_type in ("products", "all"):
        existing_names = {s["name"] for s in suggestions}
        cur.execute("""
            SELECT id, name, category AS hint
            FROM ingredient_products
            WHERE similarity(name, %s) > 0.2
              AND name NOT ILIKE %s
            ORDER BY similarity(name, %s) DESC
            LIMIT %s
        """, (q, q + "%", q, per_type))
        for row in cur.fetchall():
            if row["name"] not in existing_names:
                suggestions.append({"id": row["id"], "name": row["name"],
                                     "hint": row["hint"], "type": "product"})

    cur.close()
    conn.close()

    return jsonify({"suggestions": suggestions[:limit]})


@app.route("/api/supplier/notify", methods=["POST"])
def supplier_notify():
    """F8 — Supplier notification: log that a supplier was referenced in a recipe.
    Records the reference in supplier_notifications if the table exists,
    otherwise logs to stderr. Email delivery is intentionally out-of-scope
    for this endpoint (use a background job or webhook).
    Body (JSON):
      supplier_id   — int (required)
      recipe_slug   — str (required)
      recipe_name   — str (optional)
      context       — str (optional, free text note)
    """
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json(silent=True) or {}
    supplier_id = data.get("supplier_id")
    recipe_slug = data.get("recipe_slug", "").strip()

    if not supplier_id or not recipe_slug:
        return jsonify({"error": "supplier_id and recipe_slug are required"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Verify supplier exists and get contact info
    cur.execute("""
        SELECT id, name, contact_email, website FROM suppliers WHERE id = %s
    """, (supplier_id,))
    supplier = cur.fetchone()
    if not supplier:
        cur.close(); conn.close()
        return jsonify({"error": "Supplier not found"}), 404

    # Insert notification record (table may not exist yet — graceful fallback)
    notification_id = None
    try:
        cur.execute("""
            INSERT INTO supplier_notifications
              (supplier_id, recipe_slug, recipe_name, context, notified_at)
            VALUES (%s, %s, %s, %s, NOW())
            RETURNING id
        """, (
            supplier_id,
            recipe_slug,
            data.get("recipe_name", ""),
            data.get("context", ""),
        ))
        row = cur.fetchone()
        notification_id = row["id"] if row else None
    except Exception:
        # Table doesn't exist or other DB error — log and continue; don't fail the request
        import sys
        print(f"[supplier_notify] insert failed; "
              f"supplier={supplier['name']} recipe={recipe_slug}", file=sys.stderr)

    cur.close()
    conn.close()

    return jsonify({
        "ok": True,
        "supplier": {"id": supplier["id"], "name": supplier["name"],
                     "has_email": bool(supplier["contact_email"])},
        "notification_id": notification_id,
    })


@app.route("/test/enhance")
def test_enhance_page():
    return send_file("test_enhance.html")


@app.route("/test/enhance-barramundi")
def test_enhance_barramundi_page():
    return send_file("test_enhance_barramundi.html")


# ─── Demo pages ──────────────────────────────────────────────────────────────

@app.route("/demo")
def demo_index():
    demos = [{"name": "Rendang", "cuisine": "Indonesian (Minangkabau)", "url": "/demo/rendang"}]
    return render_template_string("""
    <html><head><title>Provenance Demos</title>
    <style>body{font-family:-apple-system,sans-serif;max-width:600px;margin:80px auto;padding:20px}
    a{color:#8B6914;font-size:18px}</style></head>
    <body><h1>Provenance Reserve Demos</h1>
    <p>Full Reserve-tier experience with Pat's Rule supplier chains.</p>
    <ul style="line-height:2.5">
    {% for d in demos %}<li><a href="{{d.url}}">{{d.name}} &mdash; {{d.cuisine}}</a></li>{% endfor %}
    </ul></body></html>""", demos=demos)


@app.route("/demo/rendang")
def demo_rendang():
    return render_template("demo_rendang.html")


# ─── Sentry test route ───────────────────────────────────────────────────────

@app.route("/debug-sentry")
def trigger_error():
    division_by_zero = 1 / 0


# ─── Beverage DB init ─────────────────────────────────────────────────────────

def _init_beverage_db():
    """Create beverage tables if they don't exist. Safe to call on every startup."""
    if not DATABASE_URL:
        return
    conn = get_db()
    cur = conn.cursor()

    stmts = [
        """CREATE TABLE IF NOT EXISTS beverage_regions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200),
            country VARCHAR(100),
            family VARCHAR(50),
            parent_region_id INTEGER REFERENCES beverage_regions(id),
            description TEXT,
            latitude NUMERIC(9,6),
            longitude NUMERIC(9,6),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_producers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200),
            producer_type VARCHAR(100),
            region_id INTEGER REFERENCES beverage_regions(id),
            description TEXT,
            verified BOOLEAN DEFAULT FALSE,
            website VARCHAR(500),
            country VARCHAR(100),
            city VARCHAR(100),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200),
            category VARCHAR(100),
            quality_tier VARCHAR(50),
            region_id INTEGER REFERENCES beverage_regions(id),
            producer_id INTEGER REFERENCES beverage_producers(id),
            description TEXT,
            tasting_notes TEXT,
            production_method TEXT,
            abv NUMERIC(5,2),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_product_producers (
            product_id INTEGER NOT NULL REFERENCES beverage_products(id) ON DELETE CASCADE,
            producer_id INTEGER NOT NULL REFERENCES beverage_producers(id) ON DELETE CASCADE,
            PRIMARY KEY (product_id, producer_id)
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_product_suppliers (
            product_id INTEGER NOT NULL REFERENCES beverage_products(id) ON DELETE CASCADE,
            supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
            region VARCHAR(100)[],
            notes TEXT,
            PRIMARY KEY (product_id, supplier_id)
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_vintages (
            id SERIAL PRIMARY KEY,
            region_id INTEGER REFERENCES beverage_regions(id),
            year INTEGER NOT NULL,
            quality_rating NUMERIC(4,2),
            notes TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_references (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200),
            category VARCHAR(100),
            description TEXT,
            key_principles TEXT,
            skill_level VARCHAR(50),
            service_context VARCHAR(100),
            beverage_family VARCHAR(50),
            source_text TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS service_protocols (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            slug VARCHAR(200),
            category VARCHAR(100),
            beverage_family VARCHAR(50),
            skill_level VARCHAR(50),
            description TEXT,
            steps TEXT,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS pairing_intelligence (
            id SERIAL PRIMARY KEY,
            food_profile VARCHAR(200),
            food_category VARCHAR(100),
            beverage_category VARCHAR(100),
            meal_context VARCHAR(100),
            confidence VARCHAR(50),
            pairing_type VARCHAR(50),
            flavour_logic TEXT,
            beverage_product_id INTEGER REFERENCES beverage_products(id),
            technique_id INTEGER REFERENCES technique_references(id),
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS programme_templates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            programme_type VARCHAR(100),
            venue_type VARCHAR(100),
            description TEXT,
            structure JSONB,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS saved_programmes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(300) NOT NULL,
            event_date DATE,
            covers INTEGER DEFAULT 1,
            courses JSONB DEFAULT '[]'::jsonb,
            notes TEXT,
            is_demo BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )""",
        """CREATE TABLE IF NOT EXISTS beverage_technique_products (
            reference_id INTEGER NOT NULL REFERENCES beverage_references(id) ON DELETE CASCADE,
            product_id INTEGER NOT NULL REFERENCES beverage_products(id) ON DELETE CASCADE,
            PRIMARY KEY (reference_id, product_id)
        )""",
    ]

    for stmt in stmts:
        try:
            cur.execute(stmt)
        except Exception:
            pass  # Table likely already exists with different schema

    # Add slug columns to existing tables (idempotent)
    for stmt in [
        "ALTER TABLE beverage_products ADD COLUMN IF NOT EXISTS slug VARCHAR(300)",
        "ALTER TABLE beverage_regions ADD COLUMN IF NOT EXISTS slug VARCHAR(300)",
        "ALTER TABLE beverage_producers ADD COLUMN IF NOT EXISTS slug VARCHAR(300)",
        "CREATE INDEX IF NOT EXISTS idx_beverage_products_slug ON beverage_products(slug)",
        "CREATE INDEX IF NOT EXISTS idx_beverage_regions_slug ON beverage_regions(slug)",
        "CREATE INDEX IF NOT EXISTS idx_beverage_producers_slug ON beverage_producers(slug)",
    ]:
        try:
            cur.execute(stmt)
        except Exception:
            pass

    cur.close()
    conn.close()


_init_beverage_db()


def _seed_demo_programme():
    """Insert the Bahia Collision demo programme if no demo exists yet."""
    if not DATABASE_URL:
        return
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM saved_programmes WHERE is_demo = TRUE LIMIT 1")
        if cur.fetchone():
            cur.close()
            conn.close()
            return
        demo_courses = json.dumps([
            {"position": 0, "type": "aperitif", "technique_id": None,
             "dish_name": "Aperitif", "beverage_id": None,
             "beverage_name": "Champagne Brut NV",
             "pairing_type": "cleanse",
             "pairing_rationale": "Before the trails converge, a clean palate. Non-vintage brut — precision without declaration.",
             "service_notes": "Flute · 6–8°C · 120ml"},
            {"position": 1, "type": "course", "technique_id": None,
             "dish_name": "Poke — Pacific Migration Trail",
             "beverage_id": None, "beverage_name": "Junmai Ginjō Sake",
             "pairing_type": "bridge",
             "pairing_rationale": "The rice wine meets the raw fish at the Pacific's edge. Japanese technique and Hawaiian form share the same ocean.",
             "service_notes": "Ochoko or white wine glass · 10–12°C · 90ml"},
            {"position": 2, "type": "course", "technique_id": None,
             "dish_name": "Bacalhau Fritter — Portuguese Colonial Trail",
             "beverage_id": None, "beverage_name": "Vinho Verde, Alvarinho",
             "pairing_type": "bridge",
             "pairing_rationale": "Atlantic mineral acidity mirrors Atlantic salt cod. Monção and Melgaço — the river that divides Portugal from Spain.",
             "service_notes": "Small white wine glass · 8–10°C · 90ml"},
            {"position": 3, "type": "course", "technique_id": None,
             "dish_name": "Acarajé — West African Diaspora Trail",
             "beverage_id": None, "beverage_name": "Crémant de Loire, Brut",
             "pairing_type": "contrast",
             "pairing_rationale": "French bubbles cut through Yoruba palm oil. The contrast is the point — two empires, one plate.",
             "service_notes": "Flute · 6–8°C · 120ml"},
            {"position": 4, "type": "course", "technique_id": None,
             "dish_name": "Moqueca Baiana — The Collision (PCT × WADT × Indigenous)",
             "beverage_id": None, "beverage_name": "Cachaça with lime and palm sugar",
             "pairing_type": "complement",
             "pairing_rationale": "Portuguese stew, African dendê, Indigenous coconut — the drink carries all three trails. Brazil in a glass.",
             "service_notes": "Rocks glass · room temperature · 60ml + 120ml mixer"},
            {"position": 5, "type": "course", "technique_id": None,
             "dish_name": "Tempura Vegetables — Portuguese Colonial Trail",
             "beverage_id": None, "beverage_name": "Junmai Sake",
             "pairing_type": "cleanse",
             "pairing_rationale": "The circle closes — Portuguese technique returned to Japanese form. Sake cleanses the trail's complexity.",
             "service_notes": "Ochoko · 10–12°C · 90ml"},
            {"position": 6, "type": "course", "technique_id": None,
             "dish_name": "Feijoada — West African Diaspora Trail",
             "beverage_id": None, "beverage_name": "Malbec, Mendoza",
             "pairing_type": "bridge",
             "pairing_rationale": "Beans and pork find their match in Argentine tannin. The diaspora crossed the Atlantic twice.",
             "service_notes": "Large red wine glass · 16–18°C · 150ml"},
            {"position": 7, "type": "course", "technique_id": None,
             "dish_name": "Bebinca — Portuguese Colonial Trail (Goa, 16-layer coconut cake)",
             "beverage_id": None, "beverage_name": "20-Year Tawny Port, Taylor's",
             "pairing_type": "complement",
             "pairing_rationale": "The trail ends where it began. Portugal. The Douro. Tawny mirrors the coconut caramel of Goa.",
             "service_notes": "Copita · 14–16°C · 60ml"},
            {"position": 8, "type": "digestif", "technique_id": None,
             "dish_name": "Digestif",
             "beverage_id": None, "beverage_name": "Cachaça, aged in amburana wood",
             "pairing_type": "cleanse",
             "pairing_rationale": "Brazil. Where all three trails meet. The final glass.",
             "service_notes": "Snifter · room temperature · 45ml"},
        ])
        cur.execute(
            """INSERT INTO saved_programmes (name, event_date, covers, courses, notes, is_demo)
               VALUES (%s, %s, %s, %s, %s, TRUE)""",
            ("Provenance Table — The Collision",
             "2027-03-15", 16, demo_courses,
             "Three trails. Four continents. Five centuries. One table.")
        )
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Demo programme seed failed (non-fatal): {e}")


_seed_demo_programme()


# ─── Beverage helper ──────────────────────────────────────────────────────────

def _serialize_row(row):
    """Convert a RealDictRow to a JSON-serializable dict."""
    d = dict(row)
    for key, val in d.items():
        if hasattr(val, 'isoformat'):
            d[key] = val.isoformat()
    return d


def _slugify(text):
    """Generate a URL-safe slug from text."""
    s = text.lower().strip()
    s = _re.sub(r'[^a-z0-9\s-]', '', s)
    s = _re.sub(r'\s+', '-', s)
    s = _re.sub(r'-+', '-', s)
    return s.strip('-')


# ─── Beverage region endpoints ────────────────────────────────────────────────

@app.route("/api/beverage/regions")
def beverage_regions_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT * FROM beverage_regions WHERE 1=1"
    params = []

    country = request.args.get("country", "").strip()
    family = request.args.get("family", "").strip()
    parent_id = request.args.get("parent_id", type=int)

    if country:
        query += " AND country = %s"
        params.append(country)
    if family:
        query += " AND family = %s"
        params.append(family)
    if parent_id is not None:
        query += " AND parent_region_id = %s"
        params.append(parent_id)

    query += " ORDER BY country, name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/beverage/regions/<int:region_id>")
def beverage_region_detail(region_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM beverage_regions WHERE id = %s", (region_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404

    result = _serialize_row(row)

    cur.execute("SELECT * FROM beverage_regions WHERE parent_region_id = %s ORDER BY name", (region_id,))
    result["sub_regions"] = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()
    return jsonify(result)


@app.route("/api/beverage/regions/bulk", methods=["POST"])
def beverage_regions_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO beverage_regions
               (name, country, beverage_family, parent_region_id, description)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("name"), e.get("country"), e.get("beverage_family") or e.get("family"),
             e.get("parent_region_id"), e.get("description")),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Beverage product endpoints ───────────────────────────────────────────────

@app.route("/api/beverage/products")
def beverage_products_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT bp.*, br.name AS region_name, br.country AS region_country FROM beverage_products bp LEFT JOIN beverage_regions br ON bp.region_id = br.id WHERE 1=1"
    params = []

    category = request.args.get("category", "").strip()
    region_id = request.args.get("region_id", type=int)
    quality_tier = request.args.get("quality_tier", "").strip()
    limit = request.args.get("limit", 100, type=int)
    offset = request.args.get("offset", 0, type=int)

    if category:
        # Family-level match: "wine" matches wine_still, wine_sparkling, etc.
        query += " AND bp.category LIKE %s"
        params.append(category.rstrip("%") + "%")
    if region_id is not None:
        query += " AND bp.region_id = %s"
        params.append(region_id)
    if quality_tier:
        query += " AND bp.quality_tier = %s"
        params.append(quality_tier)

    query += " ORDER BY bp.name LIMIT %s OFFSET %s"
    params.extend([min(limit, 500), offset])

    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/beverage/products/<int:product_id>")
def beverage_product_detail(product_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.*, br.name AS region_name, br.country AS region_country
        FROM beverage_products bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s
    """, (product_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404

    result = _serialize_row(row)

    # Producers via junction or direct foreign key
    cur.execute("""
        SELECT pr.* FROM beverage_producers pr
        JOIN beverage_product_producers bpp ON pr.id = bpp.producer_id
        WHERE bpp.product_id = %s
    """, (product_id,))
    result["producers"] = [_serialize_row(r) for r in cur.fetchall()]

    # Suppliers
    try:
        cur.execute("""
            SELECT s.id, s.name, s.city, s.state_province, s.country,
                   s.supplier_type, s.website, bps.region, bps.notes
            FROM beverage_product_suppliers bps
            JOIN suppliers s ON bps.supplier_id = s.id
            WHERE bps.product_id = %s
        """, (product_id,))
        result["suppliers"] = [_serialize_row(r) for r in cur.fetchall()]
    except Exception:
        result["suppliers"] = []

    cur.close()
    conn.close()
    return jsonify(result)


@app.route("/api/beverage/products/bulk", methods=["POST"])
def beverage_products_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO beverage_products
               (name, category, quality_tier, region_id, producer_id, description)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("name"), e.get("category"), e.get("quality_tier"),
             e.get("region_id"), e.get("producer_id"), e.get("description")),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Beverage producer endpoints ──────────────────────────────────────────────

@app.route("/api/beverage/producers")
def beverage_producers_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """SELECT bp.*, br.name AS region_name, br.country AS region_country
               FROM beverage_producers bp
               LEFT JOIN beverage_regions br ON bp.region_id = br.id
               WHERE 1=1"""
    params = []

    producer_type = request.args.get("type", "").strip()
    region_id = request.args.get("region_id", type=int)
    verified = request.args.get("verified", "").strip()

    if producer_type:
        query += " AND bp.producer_type = %s"
        params.append(producer_type)
    if region_id is not None:
        query += " AND bp.region_id = %s"
        params.append(region_id)
    if verified.lower() == "true":
        query += " AND bp.is_verified = TRUE"
    elif verified.lower() == "false":
        query += " AND bp.is_verified = FALSE"

    query += " ORDER BY bp.name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/beverage/producers/<int:producer_id>")
def beverage_producer_detail(producer_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.*, br.name AS region_name
        FROM beverage_producers bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s
    """, (producer_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404

    result = _serialize_row(row)

    cur.execute("""
        SELECT p.id, p.name, p.category, p.quality_tier, p.description
        FROM beverage_products p
        JOIN beverage_product_producers bpp ON p.id = bpp.product_id
        WHERE bpp.producer_id = %s
        ORDER BY p.name
    """, (producer_id,))
    result["products"] = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()
    return jsonify(result)


@app.route("/api/beverage/producers/bulk", methods=["POST"])
def beverage_producers_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO beverage_producers
               (name, producer_type, region_id, country, philosophy_description, is_verified)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("name"), e.get("producer_type"), e.get("region_id"),
             e.get("country"), e.get("description") or e.get("philosophy_description"),
             e.get("is_verified") or e.get("verified", False)),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Beverage technique (reference) endpoints ─────────────────────────────────

@app.route("/api/beverage/techniques")
def beverage_techniques_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT * FROM beverage_references WHERE 1=1"
    params = []

    category = request.args.get("category", "").strip()
    skill_level = request.args.get("skill_level", "").strip()
    service_context = request.args.get("service_context", "").strip()

    if category:
        query += " AND category = %s"
        params.append(category)
    if skill_level:
        query += " AND skill_level = %s"
        params.append(skill_level)
    if service_context:
        query += " AND service_context = %s"
        params.append(service_context)

    query += " ORDER BY name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/beverage/techniques/<int:technique_id>")
def beverage_technique_detail(technique_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM beverage_references WHERE id = %s", (technique_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404

    result = _serialize_row(row)
    cur.close()
    conn.close()
    return jsonify(result)


@app.route("/api/beverage/techniques/bulk", methods=["POST"])
def beverage_techniques_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO beverage_references
               (name, category, description, key_principles, skill_level,
                service_context, source_text)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("name"), e.get("category"), e.get("description"),
             e.get("key_principles"), e.get("skill_level"), e.get("service_context"),
             e.get("source_text")),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Beverage vintage endpoints ───────────────────────────────────────────────

@app.route("/api/beverage/vintages")
def beverage_vintages_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """SELECT bv.*, br.name AS region_name, br.country
               FROM beverage_vintages bv
               LEFT JOIN beverage_regions br ON bv.region_id = br.id
               WHERE 1=1"""
    params = []

    region_id = request.args.get("region_id", type=int)
    year = request.args.get("year", type=int)

    if region_id is not None:
        query += " AND bv.region_id = %s"
        params.append(region_id)
    if year is not None:
        query += " AND bv.vintage_year = %s"
        params.append(year)

    query += " ORDER BY bv.vintage_year DESC, br.name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


# ─── Service protocol endpoints ───────────────────────────────────────────────

@app.route("/api/beverage/protocols")
def beverage_protocols_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT * FROM service_protocols WHERE 1=1"
    params = []

    category = request.args.get("category", "").strip()
    beverage_family = request.args.get("beverage_family", "").strip()
    skill_level = request.args.get("skill_level", "").strip()

    if category:
        query += " AND category = %s"
        params.append(category)
    if beverage_family:
        query += " AND beverage_family = %s"
        params.append(beverage_family)
    if skill_level:
        query += " AND skill_level = %s"
        params.append(skill_level)

    query += " ORDER BY name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/beverage/protocols/bulk", methods=["POST"])
def beverage_protocols_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO service_protocols
               (name, category, beverage_family, skill_level, description, procedure)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("name"), e.get("category"), e.get("beverage_family"),
             e.get("skill_level"), e.get("description"), e.get("procedure") or e.get("steps")),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Programme template endpoints ─────────────────────────────────────────────

@app.route("/api/beverage/programmes")
def beverage_programmes_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = "SELECT * FROM programme_templates WHERE 1=1"
    params = []

    programme_type = request.args.get("type", "").strip()
    venue_type = request.args.get("venue_type", "").strip()

    if programme_type:
        query += " AND programme_type = %s"
        params.append(programme_type)
    if venue_type:
        query += " AND venue_type = %s"
        params.append(venue_type)

    query += " ORDER BY name"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


# ─── Pairing intelligence endpoints ──────────────────────────────────────────

@app.route("/api/pairings")
def pairings_list():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT pi.*,
               bp.name AS product_name, bp.category AS product_category,
               bp.quality_tier, bp.description AS product_description
        FROM pairing_intelligence pi
        LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id
        WHERE 1=1
    """
    params = []

    technique_id = request.args.get("technique_id", type=int)
    food_profile = request.args.get("food_profile", "").strip()
    food_category = request.args.get("food_category", "").strip()
    beverage_category = request.args.get("beverage_category", "").strip()
    meal_context = request.args.get("meal_context", "").strip()
    confidence = request.args.get("confidence", "").strip()
    pairing_type = request.args.get("pairing_type", "").strip()
    limit = request.args.get("limit", type=int)

    if technique_id is not None:
        query += " AND pi.food_technique_id = %s"
        params.append(technique_id)
    if food_profile:
        query += " AND pi.food_flavour_profile ILIKE %s"
        params.append(f"%{food_profile}%")
    if food_category:
        query += " AND pi.food_category = %s"
        params.append(food_category)
    if beverage_category:
        query += " AND pi.beverage_category = %s"
        params.append(beverage_category)
    if meal_context:
        query += " AND pi.meal_context = %s"
        params.append(meal_context)
    if confidence:
        query += " AND pi.confidence = %s"
        params.append(confidence)
    if pairing_type:
        query += " AND pi.pairing_type = %s"
        params.append(pairing_type)

    query += " ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 WHEN 'suggested' THEN 3 WHEN 'adventurous' THEN 4 ELSE 5 END, pi.id"
    if limit:
        query += f" LIMIT {int(limit)}"
    cur.execute(query, params)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/pairings/for-technique/<int:technique_id>")
def pairings_for_technique(technique_id):
    """Returns up to 6 pairings for a technique, ordered by confidence, always including NA if available."""
    if not DATABASE_URL:
        return jsonify([]), 200

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT pi.*,
               bp.name AS product_name, bp.category AS product_category,
               bp.quality_tier, bp.description AS product_description,
               bpr.name AS producer_name
        FROM pairing_intelligence pi
        LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
        WHERE pi.food_technique_id = %s
        ORDER BY
          CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2
            WHEN 'suggested' THEN 3 WHEN 'adventurous' THEN 4 ELSE 5 END,
          pi.id
        LIMIT 6
    """, (technique_id,))
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/pairings/bulk", methods=["POST"])
def pairings_bulk():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400
    conn = get_db()
    cur = conn.cursor()
    count = 0
    for e in entries:
        cur.execute(
            """INSERT INTO pairing_intelligence
               (food_flavour_profile, food_category, beverage_category, meal_context,
                confidence, pairing_type, flavour_logic, beverage_product_id, food_technique_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT DO NOTHING""",
            (e.get("food_flavour_profile"), e.get("food_category"), e.get("beverage_category"),
             e.get("meal_context"), e.get("confidence"), e.get("pairing_type"),
             e.get("flavour_logic"), e.get("beverage_product_id"), e.get("food_technique_id")),
        )
        count += 1
    cur.close()
    conn.close()
    return jsonify(inserted=count), 201


# ─── Recipe finishing AI endpoint ────────────────────────────────────────────

@app.route("/api/recipe/<recipe_uuid>/finishing")
def recipe_finishing(recipe_uuid):
    recipes = load_recipes()
    recipe = next((r for r in recipes if r.get("uuid") == recipe_uuid), None)
    if not recipe:
        return jsonify(error="Recipe not found"), 404

    title = recipe.get("title", "")

    ingredients = []
    for ing in recipe.get("ingredients", []):
        parts = []
        if ing.get("count"): parts.append(str(ing["count"]))
        if ing.get("unit"): parts.append(ing["unit"])
        if ing.get("name"): parts.append(ing["name"])
        if parts:
            ingredients.append(" ".join(parts))

    steps = recipe.get("steps", [])
    method_summary = " ".join(steps[:3]) if steps else ""

    prompt = f"""You are a 30-year professional chef. Based on this recipe, provide specific finishing instructions — what a chef does in the final 30 seconds before the plate leaves the pass and at the table when serving.

Recipe: {title}
Ingredients: {', '.join(ingredients)}
Method summary: {method_summary}

Respond in JSON only, no markdown, no backticks:
{{
  "at_the_pass": [
    {{
      "action": "specific finishing action — what to do",
      "reasoning": "why this matters — the science or craft behind it"
    }}
  ],
  "at_the_table": [
    {{
      "action": "specific tableside action",
      "reasoning": "why this creates the moment"
    }}
  ]
}}

Rules:
- Maximum 3 items for at_the_pass, maximum 1 for at_the_table
- Be SPECIFIC to this dish. "Fleur de sel on the scored duck skin" not "add salt"
- Include the WHY for everything. The reasoning is the value.
- Name specific ingredients: Tellicherry pepper, Maldon salt, Microplane zest — not "pepper" or "salt"
- If this dish doesn't benefit from tableside service, omit at_the_table entirely
- Think like a Michelin-starred chef finishing this exact plate
- Never suggest finishing that contradicts the dish (no deglazing for sushi, no flambe for salad)"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            resp_text = "\n".join(lines)
        result = json.loads(resp_text)
        return jsonify(result)
    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse AI response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Beverage browse page ─────────────────────────────────────────────────────

@app.route("/beverage")
@app.route("/beverages")
def beverage_browse():
    if not DATABASE_URL:
        return render_template("beverage.html",
            regions=[], categories=[], pairing_food_types=[],
            total_regions=0, total_products=0, total_producers=0,
            total_pairings=0, tradition_counts={t:0 for t in ['wine','spirits','sake','tea','coffee','beer','ceremonial','fortified','non_alcoholic','fermented','water']})

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Top-level regions (no parent)
    cur.execute("""
        SELECT br.*, COUNT(bp.id) AS product_count
        FROM beverage_regions br
        LEFT JOIN beverage_products bp ON bp.region_id = br.id
        WHERE br.parent_region_id IS NULL
        GROUP BY br.id
        ORDER BY br.country, br.name
    """)
    regions = [_serialize_row(r) for r in cur.fetchall()]

    # Categories with counts
    cur.execute("""
        SELECT category, COUNT(*) AS count
        FROM beverage_products
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
    """)
    categories = [_serialize_row(r) for r in cur.fetchall()]

    # Food profiles for pairing browse
    cur.execute("""
        SELECT DISTINCT food_category, COUNT(*) AS count
        FROM pairing_intelligence
        WHERE food_category IS NOT NULL
        GROUP BY food_category
        ORDER BY count DESC
    """)
    pairing_food_types = [_serialize_row(r) for r in cur.fetchall()]

    # Stats
    cur.execute("SELECT COUNT(*) AS count FROM beverage_regions")
    total_regions = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_products")
    total_products = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_producers")
    total_producers = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM pairing_intelligence")
    total_pairings = cur.fetchone()["count"]

    # Tradition counts (group DB categories into 11 traditions)
    _cat_to_trad = {
        # fortified — checked BEFORE wine so wine_fortified doesn't fall into wine
        'wine_fortified': 'fortified', 'fortified': 'fortified',
        # wine — excludes wine_fortified (handled above)
        'wine_still': 'wine', 'wine_sparkling': 'wine',
        'wine_dessert': 'wine', 'wine_orange': 'wine', 'wine_natural': 'wine',
        'wine_rose': 'wine', 'wine': 'wine', 'sparkling': 'wine',
        # spirits
        'spirits_whiskey': 'spirits', 'spirits_brandy': 'spirits',
        'spirits_gin': 'spirits', 'spirits_rum': 'spirits', 'spirits_agave': 'spirits',
        'spirits_liqueur': 'spirits', 'spirits_vodka': 'spirits', 'spirits_tequila': 'spirits',
        'gin': 'spirits', 'baijiu': 'spirits', 'shochu': 'spirits',
        # sake
        'sake': 'sake',
        # coffee
        'coffee': 'coffee',
        # beer
        'beer_ale': 'beer', 'beer_lager': 'beer', 'beer_wild': 'beer',
        'wild beer': 'beer', 'beer': 'beer',
        # tea
        'tea': 'tea',
        # fermented — checked BEFORE na so na_fermented doesn't fall into non_alcoholic
        'na_fermented': 'fermented', 'fermented': 'fermented',
        # non-alcoholic — excludes na_fermented (handled above)
        'na_crafted': 'non_alcoholic', 'na_dealcoholised': 'non_alcoholic',
        'NA': 'non_alcoholic', 'non_alcoholic': 'non_alcoholic',
        # ceremonial / traditional
        'ceremonial': 'ceremonial', 'traditional_cultural': 'ceremonial',
        # water
        'water': 'water',
    }
    tradition_counts = {t: 0 for t in ['wine','spirits','sake','tea','coffee','beer','ceremonial','fortified','non_alcoholic','fermented','water']}
    for cat_row in categories:
        trad = _cat_to_trad.get(cat_row['category'])
        if trad:
            tradition_counts[trad] += int(cat_row['count'])

    cur.close()
    conn.close()

    return render_template("beverage.html",
        regions=regions,
        categories=categories,
        pairing_food_types=pairing_food_types,
        total_regions=total_regions,
        total_products=total_products,
        total_producers=total_producers,
        total_pairings=total_pairings,
        tradition_counts=tradition_counts,
    )


# ─── Beverage individual page routes ─────────────────────────────────────────

@app.route("/beverage/regions/<int:region_id>")
def beverage_region_page(region_id):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM beverage_regions WHERE id = %s", (region_id,))
    region = cur.fetchone()
    if not region:
        cur.close(); conn.close()
        return "Not found", 404
    region = _serialize_row(region)

    cur.execute("SELECT * FROM beverage_regions WHERE parent_region_id = %s ORDER BY name", (region_id,))
    sub_regions = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT bp.*, bpr.name AS producer_name
        FROM beverage_products bp
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
        WHERE bp.region_id = %s
        ORDER BY bp.quality_tier, bp.name
    """, (region_id,))
    products = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT * FROM beverage_vintages WHERE region_id = %s ORDER BY vintage_year DESC LIMIT 10
    """, (region_id,))
    vintages = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    canonical_url = f"https://provenance.kitchen/beverage/regions/{region_id}"
    return render_template("beverage_region.html",
        region=region, sub_regions=sub_regions, products=products, vintages=vintages,
        canonical_url=canonical_url)


@app.route("/beverage/products/<int:product_id>")
def beverage_product_page(product_id):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.*, br.name AS region_name, br.country AS region_country
        FROM beverage_products bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s
    """, (product_id,))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        return "Not found", 404
    product = _serialize_row(product)

    cur.execute("""
        SELECT pr.* FROM beverage_producers pr
        JOIN beverage_product_producers bpp ON pr.id = bpp.producer_id
        WHERE bpp.product_id = %s
    """, (product_id,))
    producers = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT pi.* FROM pairing_intelligence pi
        WHERE pi.beverage_product_id = %s
        ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 ELSE 3 END
    """, (product_id,))
    pairings = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    product_slug = product.get('slug') or _slugify(product['name'])
    canonical_url = f"https://provenance.kitchen/beverage/{product_slug}"
    return render_template("beverage_product.html",
        product=product, producers=producers, pairings=pairings,
        canonical_url=canonical_url)


@app.route("/beverage/producers/<int:producer_id>")
def beverage_producer_page(producer_id):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.*, br.name AS region_name, br.id AS region_id
        FROM beverage_producers bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s
    """, (producer_id,))
    producer = cur.fetchone()
    if not producer:
        cur.close(); conn.close()
        return "Not found", 404
    producer = _serialize_row(producer)

    cur.execute("""
        SELECT p.id, p.name, p.category, p.quality_tier, p.description,
               br.name AS region_name, br.id AS region_id
        FROM beverage_products p
        JOIN beverage_product_producers bpp ON p.id = bpp.product_id
        LEFT JOIN beverage_regions br ON p.region_id = br.id
        WHERE bpp.producer_id = %s
        ORDER BY p.quality_tier, p.name
    """, (producer_id,))
    products = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    canonical_url = f"https://provenance.kitchen/beverage/producers/{producer_id}"
    return render_template("beverage_producer.html",
        producer=producer, products=products, canonical_url=canonical_url)


# ─── Technique public page ────────────────────────────────────────────────────

@app.route("/technique/<slug>")
def technique_page(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE slug = %s", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close()
        conn.close()
        return "Not found", 404
    technique = _serialize_row(technique)

    # Normalize cross_cuisine_parallels to always be a list for the template
    ccp = technique.get('cross_cuisine_parallels')
    if ccp is not None:
        if isinstance(ccp, str):
            technique['cross_cuisine_parallels'] = [ccp] if ccp.strip() else []
        elif not isinstance(ccp, list):
            technique['cross_cuisine_parallels'] = list(ccp)

    # Related: same cuisine/origin, excluding self
    related_techniques = []
    if technique.get('origin'):
        cur.execute("""
            SELECT id, name, slug, category, description, origin, authority_tier
            FROM technique_references
            WHERE origin = %s AND id != %s
            ORDER BY authority_tier ASC, name
            LIMIT 4
        """, (technique['origin'], technique['id']))
        related_techniques = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()
    canonical_url = f"https://provenance.kitchen/technique/{slug}"
    return render_template("technique.html",
        technique=technique,
        canonical_url=canonical_url,
        related_techniques=related_techniques,
    )


# ─── Beverage product slug page ───────────────────────────────────────────────

@app.route("/beverage/<slug>")
def beverage_by_slug(slug):
    if slug in ('regions', 'products', 'producers'):
        return "Not found", 404
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bp.*, br.name AS region_name, br.country AS region_country
        FROM beverage_products bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.slug = %s
           OR LOWER(REGEXP_REPLACE(REGEXP_REPLACE(bp.name, '[^a-zA-Z0-9 -]', '', 'g'), ' +', '-', 'g')) = %s
        LIMIT 1
    """, (slug, slug))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        return "Not found", 404
    product = _serialize_row(product)
    product_id = product['id']

    cur.execute("""
        SELECT pr.* FROM beverage_producers pr
        JOIN beverage_product_producers bpp ON pr.id = bpp.producer_id
        WHERE bpp.product_id = %s
    """, (product_id,))
    producers = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT pi.* FROM pairing_intelligence pi
        WHERE pi.beverage_product_id = %s
        ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 ELSE 3 END
    """, (product_id,))
    pairings = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    canonical_url = f"https://provenance.kitchen/beverage/{slug}"
    return render_template("beverage_product.html",
        product=product, producers=producers, pairings=pairings,
        canonical_url=canonical_url)


# ─── Discovery browse pages ──────────────────────────────────────────────────

@app.route("/api/stats")
def platform_stats():
    if not DATABASE_URL:
        return jsonify(total_techniques=0, total_drinks=0, featured_cuisines=[])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT COUNT(*) AS count FROM technique_references")
    total_techniques = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_products")
    total_drinks = cur.fetchone()["count"]
    cur.execute("""
        SELECT origin AS cuisine, COUNT(*) AS count
        FROM technique_references
        WHERE origin IS NOT NULL AND origin != ''
        GROUP BY origin
        ORDER BY count DESC
        LIMIT 8
    """)
    featured_cuisines = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(total_techniques=total_techniques, total_drinks=total_drinks, featured_cuisines=featured_cuisines)


@app.route("/cuisines")
def cuisines_page():
    if not DATABASE_URL:
        return render_template("cuisines.html", cuisines=[], total_techniques=0)
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT origin AS cuisine, COUNT(*) AS count
        FROM technique_references
        WHERE origin IS NOT NULL AND origin != ''
        GROUP BY origin
        ORDER BY count DESC
    """)
    cuisines = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) AS count FROM technique_references")
    total_techniques = cur.fetchone()["count"]
    cur.close()
    conn.close()
    return render_template("cuisines.html", cuisines=cuisines, total_techniques=total_techniques)


@app.route("/techniques/browse")
def techniques_browse():
    _tb_fallback = dict(techniques=[], total=0, page=1, total_pages=1, per_page=50,
        cuisine="", category="", q="", all_cuisines=[], all_categories=[])
    if not DATABASE_URL:
        return render_template("techniques_browse.html", **_tb_fallback)
    try:
        conn = get_db()
    except psycopg2.OperationalError:
        return render_template("techniques_browse.html", **_tb_fallback)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cuisine = request.args.get("cuisine", "").strip()
    category = request.args.get("category", "").strip()
    q = request.args.get("q", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    per_page = 50
    offset = (page - 1) * per_page

    conditions = []
    params = []
    if cuisine:
        # Match cuisine against the origin field (same field used by /cuisines page)
        conditions.append("origin ILIKE %s")
        params.append(f"%{cuisine}%")
    if category:
        # Support prefix-style matching for top-level groups like "Provenance 1000" or "Provenance 500"
        conditions.append("category ILIKE %s")
        params.append(f"{category}%")
    if q:
        conditions.append("(name ILIKE %s OR description ILIKE %s)")
        params.extend([f"%{q}%", f"%{q}%"])

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    cur.execute(f"SELECT COUNT(*) AS count FROM technique_references {where}", params)
    total = cur.fetchone()["count"]
    cur.execute(
        f"SELECT id, name, slug, category, origin, authority_tier, tier_level, description "
        f"FROM technique_references {where} ORDER BY name LIMIT %s OFFSET %s",
        params + [per_page, offset]
    )
    techniques = [_serialize_row(r) for r in cur.fetchall()]

    # Cuisine dropdown: use origin field directly (matches /cuisines page)
    cur.execute("""
        SELECT DISTINCT origin AS cuisine_name
        FROM technique_references
        WHERE origin IS NOT NULL AND origin != ''
        ORDER BY origin
    """)
    all_cuisines = [r["cuisine_name"] for r in cur.fetchall() if r["cuisine_name"]]

    # Category dropdown: show the top-level group prefix (before " — ")
    cur.execute("""
        SELECT DISTINCT
            CASE WHEN category LIKE '% — %' THEN TRIM(SPLIT_PART(category, ' — ', 1)) ELSE category END
            AS cat_group
        FROM technique_references
        WHERE category IS NOT NULL AND category != ''
        ORDER BY cat_group
    """)
    all_categories = [r["cat_group"] for r in cur.fetchall() if r["cat_group"]]

    cur.close()
    conn.close()

    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template("techniques_browse.html",
        techniques=techniques,
        total=total,
        page=page,
        total_pages=total_pages,
        per_page=per_page,
        cuisine=cuisine,
        category=category,
        q=q,
        all_cuisines=all_cuisines,
        all_categories=all_categories,
    )


@app.route("/drinks")
def drinks_page():
    if not DATABASE_URL:
        return render_template("drinks_home.html", categories=[], total_drinks=363, p500_total=0)
    try:
        conn = get_db()
    except psycopg2.OperationalError:
        return render_template("drinks_home.html", categories=[], total_drinks=363, p500_total=0)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT category, COUNT(*) AS count
        FROM beverage_products
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
    """)
    categories = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_products")
    total_drinks = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM technique_references WHERE category LIKE 'Provenance 500 Drinks%%'")
    p500_total = cur.fetchone()["count"]
    cur.close()
    conn.close()
    return render_template("drinks_home.html", categories=categories, total_drinks=total_drinks, p500_total=p500_total)


@app.route("/api/drinks/p500")
def api_drinks_p500():
    if not DATABASE_URL:
        return jsonify([])
    try:
        limit = min(int(request.args.get("limit", "500")), 500)
    except (ValueError, TypeError):
        limit = 500
    category = request.args.get("category", "").strip()
    cat_map = {
        "Cocktails":         "Provenance 500 Drinks \u2014 Cocktails",
        "Wine":              "Provenance 500 Drinks \u2014 Wine",
        "Beer":              "Provenance 500 Drinks \u2014 Beer",
        "Spirits":           "Provenance 500 Drinks \u2014 Spirits",
        "Sake & East Asian": "Provenance 500 Drinks \u2014 Sake & East Asian",
        "Coffee":            "Provenance 500 Drinks \u2014 Coffee",
        "Tea":               "Provenance 500 Drinks \u2014 Tea",
        "Non-Alcoholic":     "Provenance 500 Drinks \u2014 Non-Alcoholic",
        "Traditional":       "Provenance 500 Drinks \u2014 Traditional and Cultural",
        "Pairing Guides":    "Provenance 500 Drinks \u2014 Pairing Guides",
    }
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if category in cat_map:
        cur.execute(
            "SELECT id, name, slug, category FROM technique_references WHERE category = %s ORDER BY id LIMIT %s",
            (cat_map[category], limit)
        )
    else:
        cur.execute(
            "SELECT id, name, slug, category FROM technique_references WHERE category LIKE 'Provenance 500 Drinks%%' ORDER BY category, id LIMIT %s",
            (limit,)
        )
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


# ─── Why It Works pages ──────────────────────────────────────────────────────

@app.route("/why/<slug>")
def why_it_works(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE slug = %s", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close(); conn.close()
        return "Not found", 404
    technique = _serialize_row(technique)

    ccp = technique.get('cross_cuisine_parallels')
    if ccp is not None:
        if isinstance(ccp, str):
            technique['cross_cuisine_parallels'] = [ccp] if ccp.strip() else []
        elif not isinstance(ccp, list):
            technique['cross_cuisine_parallels'] = list(ccp)

    house_tier = None
    qh = technique.get('quality_hierarchy')
    if isinstance(qh, list):
        for tier in qh:
            if isinstance(tier, dict):
                if tier.get('tier') == 1 or str(tier.get('tier_name', '')).lower() == 'house':
                    house_tier = tier
                    break

    faqs = []
    if technique.get('flavour_context'):
        faqs.append({
            'question': f"Why does {technique['name']} taste the way it does?",
            'answer': technique['flavour_context'][:500],
        })
    if house_tier and house_tier.get('criteria'):
        faqs.append({
            'question': f"What are common mistakes when making {technique['name']}?",
            'answer': house_tier['criteria'][:500],
        })
    elif technique.get('common_mistakes'):
        faqs.append({
            'question': f"What are common mistakes when making {technique['name']}?",
            'answer': technique['common_mistakes'][:500],
        })
    if technique.get('species_precision'):
        faqs.append({
            'question': f"What are the best ingredients for {technique['name']}?",
            'answer': technique['species_precision'][:500],
        })
    ccp_list = technique.get('cross_cuisine_parallels', [])
    if ccp_list:
        first = ccp_list[0]
        if isinstance(first, dict):
            names = [p.get('technique', '') for p in ccp_list[:3] if isinstance(p, dict)]
            connection = first.get('connection', '')
        else:
            names = [str(p)[:80] for p in ccp_list[:3]]
            connection = ''
        if names:
            ans = f"{technique['name']} connects to similar techniques: {', '.join(n for n in names if n)}."
            if connection:
                ans += ' ' + connection[:200]
            faqs.append({
                'question': f"What dishes are similar to {technique['name']} in other cuisines?",
                'answer': ans,
            })

    cur.close(); conn.close()
    canonical_url = f"https://provenance.kitchen/why/{slug}"
    return render_template("why_it_works.html",
        technique=technique,
        faqs=faqs,
        house_tier=house_tier,
        canonical_url=canonical_url,
    )


# ─── Beyond the Recipe pages ─────────────────────────────────────────────────

@app.route("/beyond/<slug>")
def beyond_recipe(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE slug = %s", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close(); conn.close()
        return "Not found", 404
    technique = _serialize_row(technique)

    ccp = technique.get('cross_cuisine_parallels')
    if ccp is not None:
        if isinstance(ccp, str):
            technique['cross_cuisine_parallels'] = [ccp] if ccp.strip() else []
        elif not isinstance(ccp, list):
            technique['cross_cuisine_parallels'] = list(ccp)

    related_techniques = []
    if technique.get('origin'):
        cur.execute("""
            SELECT id, name, slug, category, description, origin
            FROM technique_references
            WHERE origin = %s AND id != %s
            ORDER BY authority_tier ASC, name
            LIMIT 4
        """, (technique['origin'], technique['id']))
        related_techniques = [_serialize_row(r) for r in cur.fetchall()]

    cur.close(); conn.close()
    canonical_url = f"https://provenance.kitchen/beyond/{slug}"
    return render_template("beyond_recipe.html",
        technique=technique,
        related_techniques=related_techniques,
        canonical_url=canonical_url,
    )


# ─── Recipe enhancement page ─────────────────────────────────────────────────

def _parse_schema_recipe(data):
    ingredients = data.get('recipeIngredient', [])
    if isinstance(ingredients, str):
        ingredients = [ingredients]
    instructions = []
    raw = data.get('recipeInstructions', [])
    if isinstance(raw, str):
        instructions = [raw]
    elif isinstance(raw, list):
        for step in raw:
            if isinstance(step, str):
                instructions.append(step)
            elif isinstance(step, dict):
                instructions.append(step.get('text', ''))
    return {
        'title': data.get('name', 'Imported Recipe'),
        'source': data.get('url', ''),
        'ingredients': [str(i) for i in ingredients if i],
        'instructions': [str(s) for s in instructions if s],
        'cuisine': data.get('recipeCuisine', ''),
        'description': data.get('description', ''),
    }


def _fetch_and_parse_recipe(url):
    import ipaddress
    import json as _json_mod
    parsed = _urllib_parse.urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        raise ValueError("Only http/https URLs are supported")
    hostname = parsed.hostname or ''
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_private or addr.is_loopback or addr.is_link_local:
            raise ValueError("URL resolves to a private/internal address")
    except ValueError as e:
        if 'private' in str(e) or 'loopback' in str(e) or 'internal' in str(e):
            raise

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError("beautifulsoup4 not installed")

    headers = {'User-Agent': 'Provenance Recipe Enhancer/1.0 (+https://provenance.kitchen)'}
    resp = http_requests.get(url, headers=headers, timeout=10, allow_redirects=True)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = _json_mod.loads(script.string or '')
            candidates = data if isinstance(data, list) else data.get('@graph', [data])
            for item in candidates:
                if isinstance(item, dict) and item.get('@type') == 'Recipe':
                    return _parse_schema_recipe(item)
        except Exception:
            continue

    title_el = soup.find('h1')
    return {
        'title': title_el.get_text().strip() if title_el else 'Imported Recipe',
        'source': url,
        'ingredients': [],
        'instructions': [],
        'cuisine': '',
        'description': '',
    }


def _extract_key_terms(text):
    culinary_terms = [
        'sear', 'braise', 'roast', 'grill', 'smoke', 'cure', 'ferment',
        'emulsion', 'reduction', 'caramelise', 'caramelize', 'deglaze',
        'blanch', 'confit', 'tempering', 'lamination', 'fold', 'knead',
        'proof', 'brine', 'marinade', 'roux', 'stock', 'dashi', 'miso',
        'tahini', 'harissa', 'gochujang', 'sambal', 'soffritto', 'mirepoix',
        'rempah', 'tadka',
    ]
    text_lower = text.lower()
    return [t for t in culinary_terms if t in text_lower]


def _match_techniques_for_enhance(recipe_data):
    if not DATABASE_URL:
        return []
    matches = []
    seen_ids = set()
    title = recipe_data.get('title', '').lower()
    cuisine = recipe_data.get('cuisine', '').lower()
    full_text = ' '.join(recipe_data.get('ingredients', []) + recipe_data.get('instructions', []))

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if title:
        cur.execute("""
            SELECT id, name, slug, category, origin, description,
                   similarity(LOWER(name), %s) AS sim
            FROM technique_references
            WHERE similarity(LOWER(name), %s) > 0.25
            ORDER BY sim DESC
            LIMIT 8
        """, (title, title))
        for row in cur.fetchall():
            if row['id'] not in seen_ids:
                seen_ids.add(row['id'])
                matches.append({
                    'name': row['name'],
                    'slug': row['slug'] or '',
                    'origin': row['origin'] or '',
                    'description': (row['description'] or '')[:180],
                    'relevance': f"Direct match for {recipe_data.get('title', '')}",
                })

    for term in _extract_key_terms(full_text)[:5]:
        cur.execute("""
            SELECT id, name, slug, category, origin, description
            FROM technique_references
            WHERE LOWER(name) LIKE %s
            LIMIT 3
        """, (f"%{term}%",))
        for row in cur.fetchall():
            if row['id'] not in seen_ids:
                seen_ids.add(row['id'])
                matches.append({
                    'name': row['name'],
                    'slug': row['slug'] or '',
                    'origin': row['origin'] or '',
                    'description': (row['description'] or '')[:180],
                    'relevance': f"Related to technique: {term}",
                })

    if cuisine and len(matches) < 10:
        cur.execute("""
            SELECT id, name, slug, category, origin, description
            FROM technique_references
            WHERE LOWER(origin) LIKE %s
            ORDER BY authority_tier ASC, name
            LIMIT 5
        """, (f"%{cuisine}%",))
        for row in cur.fetchall():
            if row['id'] not in seen_ids:
                seen_ids.add(row['id'])
                matches.append({
                    'name': row['name'],
                    'slug': row['slug'] or '',
                    'origin': row['origin'] or '',
                    'description': (row['description'] or '')[:180],
                    'relevance': f"Related {row['origin'] or cuisine} technique",
                })

    cur.close(); conn.close()
    return matches[:15]


@app.route("/enhance", methods=["GET", "POST"])
def enhance_recipe_page():
    if request.method == "GET":
        return render_template("enhance.html")

    url = request.form.get('url', '').strip()
    if not url:
        return render_template("enhance.html", error="Please enter a recipe URL.")

    try:
        recipe_data = _fetch_and_parse_recipe(url)
    except Exception as e:
        return render_template("enhance.html", error=f"Could not parse that URL: {str(e)}")

    technique_matches = _match_techniques_for_enhance(recipe_data)

    return render_template("enhance_result.html",
        recipe=recipe_data,
        techniques=technique_matches,
        source_url=url,
    )


# ─── Programme builder ───────────────────────────────────────────────────────

@app.route("/programme")
def programme_builder():
    demo = None
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM saved_programmes WHERE is_demo = TRUE ORDER BY id LIMIT 1")
            row = cur.fetchone()
            if row:
                demo = _serialize_row(row)
            cur.close()
            conn.close()
        except Exception:
            pass
    return render_template("programme.html", demo=demo)


@app.route("/api/programme/search-techniques")
def programme_search_techniques():
    if not DATABASE_URL:
        return jsonify([])
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    limit = min(request.args.get("limit", 10, type=int), 30)
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, slug, category, origin,
               LEFT(description, 150) AS description,
               similarity(LOWER(name), LOWER(%s)) AS sim
        FROM technique_references
        WHERE similarity(LOWER(name), LOWER(%s)) > 0.15
           OR LOWER(name) ILIKE %s
        ORDER BY similarity(LOWER(name), LOWER(%s)) DESC, name
        LIMIT %s
    """, (q, q, f"%{q.lower()}%", q, limit))
    results = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(results)


@app.route("/api/programme/pairings")
def programme_pairings():
    if not DATABASE_URL:
        return jsonify({"technique": None, "pairings": {}})
    technique_id = request.args.get("technique_id", type=int)
    if not technique_id:
        return jsonify({"error": "technique_id required"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Get the technique
    cur.execute("SELECT id, name, slug, category, origin FROM technique_references WHERE id = %s", (technique_id,))
    tech_row = cur.fetchone()
    if not tech_row:
        cur.close(); conn.close()
        return jsonify({"error": "Technique not found"}), 404
    technique = _serialize_row(tech_row)

    _pairing_select = """
        SELECT pi.id, pi.pairing_type, pi.confidence, pi.flavour_logic,
               pi.food_category, pi.meal_context,
               bp.id AS beverage_id, bp.name AS beverage_name,
               bp.category AS beverage_category, bp.quality_tier,
               bp.description AS beverage_description,
               bpr.name AS producer_name,
               br.name AS region_name
        FROM pairing_intelligence pi
        JOIN beverage_products bp ON pi.beverage_product_id = bp.id
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
    """

    # Get pairings from pairing_intelligence
    cur.execute(_pairing_select + """
        WHERE pi.food_technique_id = %s
        ORDER BY
          CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2
            WHEN 'suggested' THEN 3 WHEN 'adventurous' THEN 4 ELSE 5 END,
          pi.id
    """, (technique_id,))
    rows = [_serialize_row(r) for r in cur.fetchall()]

    # If no direct pairings, fall back to category-based pairings
    if not rows:
        cuisine = (technique.get("origin") or technique.get("category") or "").split(",")[0].strip()
        cur.execute(_pairing_select + """
            WHERE pi.food_category ILIKE %s
            ORDER BY
              CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2
                WHEN 'suggested' THEN 3 WHEN 'adventurous' THEN 4 ELSE 5 END
            LIMIT 15
        """, (f"%{cuisine}%",))
        rows = [_serialize_row(r) for r in cur.fetchall()]
        for r in rows:
            r["_general_suggestion"] = True

        # If still nothing, just grab the top classic/established pairings
        if not rows:
            cur.execute(_pairing_select + """
                WHERE pi.confidence IN ('classic', 'established')
                ORDER BY RANDOM()
                LIMIT 10
            """)
            rows = [_serialize_row(r) for r in cur.fetchall()]
            for r in rows:
                r["_general_suggestion"] = True

    cur.close(); conn.close()

    # Group by pairing_type
    grouped = {"complement": [], "contrast": [], "bridge": [], "cleanse": [], "elevate": []}
    for r in rows:
        pt = r.get("pairing_type") or "complement"
        if pt not in grouped:
            pt = "complement"
        grouped[pt].append({
            "pairing_id": r.get("id"),
            "beverage_id": r.get("beverage_id"),
            "beverage_name": r.get("beverage_name"),
            "beverage_category": r.get("beverage_category"),
            "producer": r.get("producer_name"),
            "region": r.get("region_name"),
            "confidence": r.get("confidence"),
            "rationale": r.get("flavour_logic") or "",
            "general_suggestion": r.get("_general_suggestion", False),
        })

    return jsonify({"technique": technique, "pairings": grouped})


@app.route("/api/programme/service")
def programme_service():
    if not DATABASE_URL:
        return jsonify({})
    beverage_id = request.args.get("beverage_id", type=int)
    if not beverage_id:
        return jsonify({"error": "beverage_id required"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.*, bpr.name AS producer_name,
               br.name AS region_name, br.country
        FROM beverage_products bp
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s
    """, (beverage_id,))
    prod_row = cur.fetchone()
    if not prod_row:
        cur.close(); conn.close()
        return jsonify({"error": "Beverage not found"}), 404
    product = _serialize_row(prod_row)

    # Find matching service protocol by beverage family
    cat = (product.get("category") or "").lower()
    family_map = {
        "wine": "wine", "sparkling": "sparkling_wine", "sake": "sake",
        "spirits_whiskey": "whisky", "spirits_brandy": "brandy", "gin": "gin",
        "coffee": "coffee", "beer_ale": "beer", "beer_lager": "beer",
        "wild beer": "beer", "NA": "non_alcoholic", "na_dealcoholised": "non_alcoholic",
    }
    family = family_map.get(cat, cat)

    cur.execute("""
        SELECT *
        FROM service_protocols
        WHERE LOWER(beverage_family) = LOWER(%s)
           OR LOWER(category) ILIKE %s
        ORDER BY id LIMIT 1
    """, (family, f"%{cat}%"))
    proto_row = cur.fetchone()
    protocol = _serialize_row(proto_row) if proto_row else {}

    cur.close(); conn.close()

    # Build service summary from default knowledge for each category
    _service_defaults = {
        "wine": {"temperature": "12–16°C", "vessel": "Large red or white wine glass", "pour": "150ml"},
        "sparkling": {"temperature": "6–8°C", "vessel": "Flute or coupe", "pour": "120ml"},
        "sake": {"temperature": "10–12°C (ginjō)", "vessel": "Ochoko or white wine glass", "pour": "90ml"},
        "spirits_whiskey": {"temperature": "Room temperature", "vessel": "Tulip glass or snifter", "pour": "45ml"},
        "spirits_brandy": {"temperature": "Room temperature", "vessel": "Balloon snifter", "pour": "45ml"},
        "gin": {"temperature": "Chilled", "vessel": "Copa glass", "pour": "45ml + 150ml tonic"},
        "coffee": {"temperature": "70–80°C", "vessel": "Demitasse or V60", "pour": "200ml"},
        "beer_ale": {"temperature": "8–12°C", "vessel": "Pint or tulip", "pour": "330ml"},
        "beer_lager": {"temperature": "4–7°C", "vessel": "Pilsner glass", "pour": "330ml"},
        "NA": {"temperature": "8–12°C", "vessel": "White wine glass or highball", "pour": "150ml"},
    }
    defaults = _service_defaults.get(cat, {"temperature": "As appropriate", "vessel": "Appropriate glass", "pour": "As required"})

    return jsonify({
        "product": product,
        "protocol": protocol,
        "service": defaults,
    })


@app.route("/api/programme/beverages")
def programme_beverages():
    """Search beverage products by name for aperitif/digestif selection."""
    if not DATABASE_URL:
        return jsonify([])
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    limit = min(request.args.get("limit", 10, type=int), 30)

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if q:
        cur.execute("""
            SELECT bp.id, bp.name, bp.category, bp.quality_tier,
                   bpr.name AS producer_name, br.name AS region_name,
                   similarity(LOWER(bp.name), LOWER(%s)) AS sim
            FROM beverage_products bp
            LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
            LEFT JOIN beverage_regions br ON bp.region_id = br.id
            WHERE (similarity(LOWER(bp.name), LOWER(%s)) > 0.15 OR LOWER(bp.name) ILIKE %s)
              AND (%s = '' OR bp.category ILIKE %s)
            ORDER BY sim DESC, bp.name
            LIMIT %s
        """, (q, q, f"%{q.lower()}%", category, f"%{category}%", limit))
    else:
        # Default: return aperitif suggestions (sparkling/wine) or digestif (spirits/fortified)
        cat_filter = f"%{category}%" if category else "%"
        cur.execute("""
            SELECT bp.id, bp.name, bp.category, bp.quality_tier,
                   bpr.name AS producer_name, br.name AS region_name
            FROM beverage_products bp
            LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
            LEFT JOIN beverage_regions br ON bp.region_id = br.id
            WHERE bp.category ILIKE %s
            ORDER BY bp.quality_tier, bp.name
            LIMIT %s
        """, (cat_filter, limit))

    results = [_serialize_row(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(results)


@app.route("/api/programme/save", methods=["POST"])
def programme_save():
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Programme name required"}), 400

    event_date = data.get("date") or None
    covers = data.get("covers") or 1
    courses = json.dumps(data.get("courses") or [])
    notes = data.get("notes") or None

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO saved_programmes (name, event_date, covers, courses, notes, is_demo)
        VALUES (%s, %s, %s, %s, %s, FALSE)
        RETURNING id
    """, (name, event_date, covers, courses, notes))
    row = cur.fetchone()
    new_id = row[0]
    cur.close(); conn.close()
    return jsonify({"id": new_id, "name": name}), 201


@app.route("/api/programme/list")
def programme_list():
    if not DATABASE_URL:
        return jsonify([])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, event_date, covers, notes, is_demo, created_at
        FROM saved_programmes
        ORDER BY is_demo DESC, created_at DESC
        LIMIT 50
    """)
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(rows)


@app.route("/api/programme/<int:programme_id>")
def programme_get(programme_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM saved_programmes WHERE id = %s", (programme_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return jsonify({"error": "Programme not found"}), 404
    return jsonify(_serialize_row(row))


@app.route("/api/programme/export/<int:programme_id>")
def programme_export(programme_id):
    if not DATABASE_URL:
        return jsonify({"error": "Database not configured"}), 503

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM saved_programmes WHERE id = %s", (programme_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return jsonify({"error": "Programme not found"}), 404

    prog = _serialize_row(row)
    courses = prog.get("courses") or []
    if isinstance(courses, str):
        courses = json.loads(courses)

    fmt = request.args.get("format", "pdf").lower()

    _type_labels = {
        "complement": "COMPLEMENT", "contrast": "CONTRAST",
        "bridge": "BRIDGE", "cleanse": "CLEANSE", "elevate": "ELEVATE",
    }

    def _course_html(c, idx):
        ctype = c.get("type", "course")
        if ctype == "aperitif":
            header = "APERITIF"
        elif ctype == "digestif":
            header = "DIGESTIF"
        else:
            header = f"COURSE {idx}"
        dish = c.get("dish_name", "")
        bev = c.get("beverage_name", "")
        pt = _type_labels.get(c.get("pairing_type", ""), "")
        rationale = c.get("pairing_rationale", "")
        service = c.get("service_notes", "")
        pt_part = f'<span class="pt">{pt}</span> ' if pt else ""
        return f"""
        <div class="course">
          <div class="course-header">{header}</div>
          <div class="dish">{dish}</div>
          <div class="beverage">{pt_part}{bev}</div>
          {"<div class='service'>" + service + "</div>" if service else ""}
          {"<div class='rationale'>&ldquo;" + rationale + "&rdquo;</div>" if rationale else ""}
        </div>"""

    courses_html = ""
    course_num = 0
    for c in courses:
        ctype = c.get("type", "course")
        if ctype not in ("aperitif", "digestif"):
            course_num += 1
        courses_html += _course_html(c, course_num)

    event_date = prog.get("event_date") or ""
    covers = prog.get("covers") or ""
    notes = prog.get("notes") or ""
    subtitle = " · ".join(filter(None, [str(event_date), f"{covers} covers" if covers else ""]))

    html_content = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=DM+Mono:wght@400&display=swap');
  body {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    background: #08080A; color: #F5F1E9;
    margin: 0; padding: 40px 48px; max-width: 600px;
    font-size: 14px; line-height: 1.6;
  }}
  .rule {{ border: none; border-top: 1px solid rgba(201,168,76,0.4); margin: 20px 0; }}
  .prog-title {{ font-size: 20px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #C9A84C; margin-bottom: 4px; }}
  .prog-subtitle {{ font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(245,241,233,0.45); margin-bottom: 8px; }}
  .course {{ margin: 16px 0; padding: 14px 0; border-bottom: 1px solid rgba(201,168,76,0.1); }}
  .course-header {{ font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 2px; text-transform: uppercase; color: rgba(201,168,76,0.55); margin-bottom: 4px; }}
  .dish {{ font-size: 15px; font-weight: 600; color: #F5F1E9; margin-bottom: 4px; }}
  .beverage {{ font-size: 14px; color: rgba(245,241,233,0.85); margin-bottom: 4px; }}
  .pt {{ font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 1px; color: #C9A84C; text-transform: uppercase; margin-right: 6px; }}
  .service {{ font-family: 'DM Mono', monospace; font-size: 9px; color: rgba(245,241,233,0.45); margin-top: 3px; letter-spacing: 0.5px; }}
  .rationale {{ font-style: italic; font-size: 12px; color: rgba(245,241,233,0.55); margin-top: 6px; }}
  .notes {{ font-style: italic; font-size: 12px; color: rgba(245,241,233,0.45); margin-top: 20px; border-top: 1px solid rgba(201,168,76,0.15); padding-top: 16px; }}
  .footer {{ font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 1px; color: rgba(201,168,76,0.3); text-transform: uppercase; margin-top: 24px; text-align: center; }}
</style>
</head><body>
<div class="prog-title">{prog['name']}</div>
{"<div class='prog-subtitle'>" + subtitle + "</div>" if subtitle else ""}
<hr class="rule">
{courses_html}
{"<div class='notes'>" + notes + "</div>" if notes else ""}
<div class="footer">Programme designed with Provenance &middot; provenance.kitchen</div>
</body></html>"""

    if fmt == "html":
        return Response(html_content, mimetype="text/html")

    # PDF via WeasyPrint
    try:
        from weasyprint import HTML as WP_HTML
        pdf_bytes = WP_HTML(string=html_content).write_pdf()
        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="programme-{programme_id}.pdf"'}
        )
    except Exception as e:
        return jsonify({"error": f"PDF generation failed: {e}"}), 500


# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_current_user():
    """Return the logged-in user dict or None."""
    user_id = session.get("user_id")
    if not user_id or not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return dict(user) if user else None
    except Exception:
        return None


def update_user(user_id, **kwargs):
    """Update arbitrary columns on a user row."""
    if not kwargs or not DATABASE_URL_WRITE:
        return
    cols = ", ".join(f"{k} = %s" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET {cols}, updated_at = NOW() WHERE id = %s", vals)
        cur.close()
        conn.close()
    except Exception:
        pass


def update_user_by_stripe_customer(customer_id, **kwargs):
    """Update user columns matched by stripe_customer_id."""
    if not kwargs or not DATABASE_URL_WRITE:
        return
    cols = ", ".join(f"{k} = %s" for k in kwargs)
    vals = list(kwargs.values()) + [customer_id]
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET {cols}, updated_at = NOW() WHERE stripe_customer_id = %s", vals)
        cur.close()
        conn.close()
    except Exception:
        pass


def user_can_access(required_tier):
    """Check if the current user's tier meets the required tier."""
    user = get_current_user()
    if not user:
        return False
    user_tier = user.get("subscription_tier", "free")
    user_status = user.get("subscription_status", "inactive")
    if required_tier == "free":
        return True
    if user_status not in ("active", "past_due"):
        return False
    user_level = TIER_HIERARCHY.index(user_tier) if user_tier in TIER_HIERARCHY else 0
    required_level = TIER_HIERARCHY.index(required_tier) if required_tier in TIER_HIERARCHY else 999
    return user_level >= required_level


@app.context_processor
def inject_user():
    user = get_current_user()
    return {
        "current_user": user,
        "user_tier": user.get("subscription_tier", "free") if user else "free",
        "is_authenticated": user is not None,
    }


# ─── Auth routes ─────────────────────────────────────────────────────────────

@app.route("/auth/signup", methods=["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signup.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("auth/signup.html", error="Email and password are required.")

    password_hash = generate_password_hash(password)
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "INSERT INTO users (email, password_hash, display_name) VALUES (%s, %s, %s) RETURNING id",
            (email, password_hash, name or None),
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        session["user_id"] = row["id"]
        next_url = request.args.get("next", "/")
        return redirect(next_url)
    except psycopg2.errors.UniqueViolation:
        return render_template("auth/signup.html", error="An account with that email already exists.")
    except Exception as e:
        return render_template("auth/signup.html", error="Something went wrong. Please try again.")


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("auth/login.html", error="Email and password are required.")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except Exception:
        return render_template("auth/login.html", error="Something went wrong. Please try again.")

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("auth/login.html", error="Incorrect email or password.")

    session.permanent = True
    session["user_id"] = user["id"]
    next_url = request.args.get("next", "/")
    return redirect(next_url)


@app.route("/auth/logout")
def auth_logout():
    session.clear()
    return redirect("/")


@app.route("/auth/account")
def auth_account():
    user = get_current_user()
    if not user:
        return redirect("/auth/login?next=/auth/account")
    subscribed = request.args.get("subscribed") == "true"
    cancelled = request.args.get("cancelled") == "true"
    return render_template("auth/account.html", user=user, subscribed=subscribed, cancelled=cancelled)


# ─── Stripe routes ───────────────────────────────────────────────────────────

@app.route("/subscribe/<tier>")
@app.route("/subscribe/<tier>/<period>")
def subscribe(tier, period="yearly"):
    if tier not in PRICE_MAP:
        return "Invalid tier", 400
    if period not in ("monthly", "yearly"):
        period = "yearly"

    price_id = PRICE_MAP[tier][period]
    if not price_id:
        return "Pricing not configured", 500

    user = get_current_user()
    if not user:
        return redirect(f"/auth/login?next=/subscribe/{tier}/{period}")

    if not user.get("stripe_customer_id"):
        customer = stripe.Customer.create(
            email=user["email"],
            name=user.get("display_name", ""),
            metadata={"provenance_user_id": user["id"]},
        )
        update_user(user["id"], stripe_customer_id=customer.id)
        customer_id = customer.id
    else:
        customer_id = user["stripe_customer_id"]

    checkout_session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url="https://provenance.kitchen/auth/account?subscribed=true",
        cancel_url="https://provenance.kitchen/auth/account?cancelled=true",
        metadata={
            "provenance_user_id": str(user["id"]),
            "tier": tier,
        },
        allow_promotion_codes=True,
    )

    return redirect(checkout_session.url)


@app.route("/billing")
def billing_portal():
    user = get_current_user()
    if not user or not user.get("stripe_customer_id"):
        return redirect("/auth/login")

    portal_session = stripe.billing_portal.Session.create(
        customer=user["stripe_customer_id"],
        return_url="https://provenance.kitchen/auth/account",
    )
    return redirect(portal_session.url)


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return "Invalid signature", 400

    if event.type == "checkout.session.completed":
        s = event.data.object
        user_id = s.metadata.get("provenance_user_id")
        tier = s.metadata.get("tier", "kitchen")
        subscription_id = getattr(s, "subscription", None)
        customer_id = getattr(s, "customer", None)
        if user_id:
            update_user(
                int(user_id),
                subscription_tier=tier,
                subscription_status="active",
                stripe_subscription_id=subscription_id,
                stripe_customer_id=customer_id,
            )

    elif event.type == "customer.subscription.updated":
        sub = event.data.object
        customer_id = sub.customer
        status = sub.status
        if status in ("active", "trialing"):
            sub_status = "active"
        elif status == "past_due":
            sub_status = "past_due"
        else:
            sub_status = "inactive"
        update_user_by_stripe_customer(customer_id, subscription_status=sub_status)

    elif event.type == "customer.subscription.deleted":
        sub = event.data.object
        customer_id = sub.customer
        update_user_by_stripe_customer(
            customer_id,
            subscription_tier="free",
            subscription_status="inactive",
            stripe_subscription_id=None,
        )

    elif event.type == "invoice.payment_failed":
        invoice = event.data.object
        customer_id = invoice.customer
        update_user_by_stripe_customer(customer_id, subscription_status="past_due")

    return "", 200


# ─── Pricing page ────────────────────────────────────────────────────────────

@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")


# ─── Sitemap ─────────────────────────────────────────────────────────────────

@app.route("/sitemap.xml")
def sitemap():
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT slug, updated_at FROM technique_references WHERE slug IS NOT NULL AND slug != '' ORDER BY id")
    techniques = cur.fetchall()

    cur.execute("SELECT slug, created_at AS updated_at FROM recipes WHERE slug IS NOT NULL AND slug != '' ORDER BY id")
    recipe_rows = cur.fetchall()

    cur.execute("""
        SELECT COALESCE(slug, LOWER(REGEXP_REPLACE(REGEXP_REPLACE(name, '[^a-zA-Z0-9 -]', '', 'g'), ' +', '-', 'g'))) AS slug,
               updated_at
        FROM beverage_products ORDER BY id
    """)
    bev_products = cur.fetchall()

    cur.execute("SELECT id, updated_at FROM beverage_regions ORDER BY id")
    bev_regions = cur.fetchall()

    cur.execute("SELECT id, updated_at FROM beverage_producers ORDER BY id")
    bev_producers = cur.fetchall()

    cur.close()
    conn.close()

    from datetime import date as _date
    base = "https://provenance.kitchen"
    today = _date.today().isoformat()

    def _lastmod(row, field='updated_at'):
        val = row.get(field) if isinstance(row, dict) else row[field]
        if val and hasattr(val, 'strftime'):
            return val.strftime('%Y-%m-%d')
        return today

    def _url(loc, priority, changefreq, lastmod=None):
        s = f'  <url>\n    <loc>{loc}</loc>\n    <priority>{priority}</priority>\n    <changefreq>{changefreq}</changefreq>'
        if lastmod:
            s += f'\n    <lastmod>{lastmod}</lastmod>'
        s += '\n  </url>'
        return s

    urls = []
    urls.append(_url(f'{base}/',                   '1.0', 'daily',   today))
    urls.append(_url(f'{base}/techniques/browse',  '0.9', 'daily',   today))
    urls.append(_url(f'{base}/recipes',            '0.8', 'daily',   today))
    urls.append(_url(f'{base}/beverages',          '0.8', 'daily',   today))
    urls.append(_url(f'{base}/cuisines',           '0.8', 'weekly',  today))
    urls.append(_url(f'{base}/drinks',             '0.7', 'weekly',  today))
    urls.append(_url(f'{base}/about',              '0.5', 'monthly', today))
    urls.append(_url(f'{base}/for-professionals',  '0.6', 'monthly', today))
    urls.append(_url(f'{base}/methodology',        '0.5', 'monthly', today))
    urls.append(_url(f'{base}/suppliers',          '0.7', 'weekly',  today))

    for r in recipe_rows:
        urls.append(_url(f'{base}/recipe/{r["slug"]}', '0.7', 'monthly', _lastmod(r)))

    for t in techniques:
        urls.append(_url(f'{base}/technique/{t["slug"]}', '0.7', 'weekly', _lastmod(t)))

    for t in techniques:
        urls.append(_url(f'{base}/why/{t["slug"]}', '0.8', 'weekly', _lastmod(t)))

    for t in techniques:
        urls.append(_url(f'{base}/beyond/{t["slug"]}', '0.8', 'weekly', _lastmod(t)))

    for p in bev_products:
        urls.append(_url(f'{base}/beverage/{p["slug"]}', '0.6', 'weekly', _lastmod(p)))

    for r in bev_regions:
        urls.append(_url(f'{base}/beverage/regions/{r["id"]}', '0.6', 'weekly', _lastmod(r)))

    for pr in bev_producers:
        urls.append(_url(f'{base}/beverage/producers/{pr["id"]}', '0.5', 'weekly', _lastmod(pr)))

    total = len(urls)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- {total} URLs -->',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ] + urls + ['</urlset>']

    return Response('\n'.join(lines), mimetype='application/xml')


# ─── Recipe Costing Engine ────────────────────────────────────────────────────

@app.route("/api/costing/scan-invoice", methods=["POST"])
def scan_invoice():
    """Scan a supplier invoice photo via Claude Vision. Extracts line items and updates ingredient prices."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401

    image_data = None
    image_url = None
    media_type = "image/jpeg"

    if request.files.get("invoice"):
        file = request.files["invoice"]
        image_data = base64.b64encode(file.read()).decode("utf-8")
        media_type = file.content_type or "image/jpeg"
    elif request.json and request.json.get("image_url"):
        image_url = request.json["image_url"]
    else:
        return jsonify({"error": "No invoice image provided"}), 400

    currency = (request.form.get("currency")
                or (request.json.get("currency") if request.json else None)
                or "CAD")

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        return jsonify({"error": "Vision API not configured"}), 500

    client = anthropic.Anthropic(api_key=anthropic_key)

    content = []
    if image_data:
        content.append({"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}})
    elif image_url:
        content.append({"type": "image", "source": {"type": "url", "url": image_url}})

    content.append({"type": "text", "text": (
        "Extract ALL line items from this supplier invoice. "
        "For each item return: item_name (exactly as printed), quantity, quantity_unit (kg/lb/case/bunch/each/L/dozen/etc.), "
        "unit_price (price per unit), line_total. "
        "Also extract: supplier_name, invoice_date (YYYY-MM-DD), invoice_total, currency (detect from invoice, default " + currency + "). "
        "Return ONLY valid JSON, no markdown:\n"
        '{"supplier_name":"...","invoice_date":"YYYY-MM-DD","invoice_total":0.00,"currency":"CAD",'
        '"items":[{"item_name":"...","quantity":0,"quantity_unit":"kg","unit_price":0.00,"line_total":0.00}]}'
    )})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": content}]
        )
        raw_text = response.content[0].text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        invoice_data = json.loads(raw_text)
    except Exception as e:
        return jsonify({"error": f"Invoice scan failed: {str(e)}"}), 500

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    items_extracted = len(invoice_data.get("items", []))
    prices_updated = 0

    for item in invoice_data.get("items", []):
        name = (item.get("item_name") or "").strip()
        if not name:
            continue
        normalized = name.lower().strip()
        unit_price = float(item.get("unit_price") or 0)
        unit = (item.get("quantity_unit") or "each").lower()
        supplier = invoice_data.get("supplier_name") or "Unknown"
        inv_date = invoice_data.get("invoice_date")
        curr = invoice_data.get("currency") or currency
        if unit_price <= 0:
            continue

        # Look up yield factor
        cur.execute("""
            SELECT default_yield FROM yield_factors
            WHERE %s ILIKE ingredient_pattern
            ORDER BY LENGTH(ingredient_pattern) DESC LIMIT 1
        """, (normalized,))
        yield_row = cur.fetchone()
        yield_factor = float(yield_row["default_yield"]) if yield_row else 1.0

        cur.execute("""
            INSERT INTO ingredient_prices
                (ingredient_name, ingredient_name_normalized, unit_price, unit, currency,
                 supplier_name, invoice_date, yield_factor, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (ingredient_name_normalized, supplier_name)
            DO UPDATE SET
                unit_price = EXCLUDED.unit_price,
                unit = EXCLUDED.unit,
                currency = EXCLUDED.currency,
                invoice_date = EXCLUDED.invoice_date,
                updated_at = NOW()
        """, (name, normalized, unit_price, unit, curr, supplier, inv_date, yield_factor))
        prices_updated += 1

    cur.execute("""
        INSERT INTO invoice_scans
            (user_id, supplier_name, invoice_date, items_extracted, prices_updated,
             raw_extraction, currency, invoice_total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (user["id"], invoice_data.get("supplier_name"), invoice_data.get("invoice_date"),
          items_extracted, prices_updated, json.dumps(invoice_data), currency,
          invoice_data.get("invoice_total")))

    cur.close()
    conn.close()

    return jsonify({
        "success": True,
        "supplier": invoice_data.get("supplier_name"),
        "invoice_date": invoice_data.get("invoice_date"),
        "items_extracted": items_extracted,
        "prices_updated": prices_updated,
        "invoice_total": invoice_data.get("invoice_total"),
        "currency": currency,
        "items": invoice_data.get("items", []),
    })


@app.route("/api/costing/recipe/<slug>")
def get_recipe_cost(slug):
    """Calculate and return the cost breakdown for a recipe."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM recipes WHERE slug = %s LIMIT 1", (slug,))
    recipe = cur.fetchone()
    if not recipe:
        cur.close(); conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    ingredients = recipe.get("ingredients") or []
    if isinstance(ingredients, str):
        try:
            ingredients = json.loads(ingredients)
        except Exception:
            ingredients = []

    cur.execute("SELECT * FROM recipe_costs WHERE recipe_slug = %s", (slug,))
    cached = cur.fetchone()

    breakdown = []
    total_cost = 0.0
    unpriced = []

    for ing in ingredients:
        name = ""
        qty = 0.0
        unit = ""
        if isinstance(ing, dict):
            name = ing.get("name") or ing.get("ingredient") or ""
            qty = float(ing.get("quantity") or ing.get("amount") or 0)
            unit = ing.get("unit") or ""
        elif isinstance(ing, str):
            name = ing
            qty = 1.0
            unit = "each"
        if not name:
            continue

        normalized = name.lower().strip()
        cur.execute("""
            SELECT ingredient_name, unit_price, unit, yield_factor, effective_cost,
                   supplier_name, currency
            FROM ingredient_prices
            WHERE ingredient_name_normalized ILIKE %s
            ORDER BY updated_at DESC LIMIT 1
        """, (f"%{normalized}%",))
        price_row = cur.fetchone()

        if price_row:
            effective = float(price_row["effective_cost"] or price_row["unit_price"])
            # If priced per kg and qty looks like grams, convert
            if price_row["unit"] == "kg" and qty >= 10:
                line_cost = round((qty / 1000) * effective, 2)
            else:
                line_cost = round(qty * effective, 2)
            breakdown.append({
                "ingredient": name,
                "quantity": qty,
                "unit": unit,
                "unit_price": float(price_row["unit_price"]),
                "price_unit": price_row["unit"],
                "yield_factor": float(price_row["yield_factor"]),
                "effective_cost": effective,
                "line_cost": line_cost,
                "supplier": price_row["supplier_name"],
                "currency": price_row["currency"],
            })
            total_cost += line_cost
        else:
            unpriced.append(name)
            breakdown.append({
                "ingredient": name,
                "quantity": qty,
                "unit": unit,
                "unit_price": None,
                "line_cost": 0,
                "status": "no_price_data",
            })

    # servings is JSONB: [{"count": "4", "unit": "serve"}]
    servings_raw = recipe.get("servings") or []
    if isinstance(servings_raw, str):
        try:
            servings_raw = json.loads(servings_raw)
        except Exception:
            servings_raw = []
    portions = 4
    if servings_raw and isinstance(servings_raw, list) and servings_raw[0]:
        try:
            portions = int(float(servings_raw[0].get("count", 4)))
        except Exception:
            portions = 4
    portions = portions or 4
    cost_per_portion = round(total_cost / portions, 2)
    target_pct = float(cached["target_food_cost_pct"]) if cached and cached.get("target_food_cost_pct") else 30.0
    menu_price = float(cached["menu_price"]) if cached and cached.get("menu_price") else None
    actual_pct = round((cost_per_portion / menu_price) * 100, 1) if menu_price and menu_price > 0 else None
    over_target = actual_pct > target_pct if actual_pct is not None else False

    try:
        wconn = psycopg2.connect(DATABASE_URL_WRITE)
        wconn.autocommit = True
        wcur = wconn.cursor()
        wcur.execute("""
            INSERT INTO recipe_costs
                (recipe_slug, total_cost, portions, cost_per_portion,
                 target_food_cost_pct, menu_price, actual_food_cost_pct,
                 ingredient_breakdown, over_target, last_calculated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (recipe_slug) DO UPDATE SET
                total_cost = EXCLUDED.total_cost,
                cost_per_portion = EXCLUDED.cost_per_portion,
                actual_food_cost_pct = EXCLUDED.actual_food_cost_pct,
                ingredient_breakdown = EXCLUDED.ingredient_breakdown,
                over_target = EXCLUDED.over_target,
                last_calculated = NOW()
        """, (slug, total_cost, portions, cost_per_portion, target_pct,
              menu_price, actual_pct, json.dumps(breakdown), over_target))
        wcur.close()
        wconn.close()
    except Exception:
        pass

    cur.close()
    conn.close()

    return jsonify({
        "recipe": recipe.get("name", slug),
        "slug": slug,
        "portions": portions,
        "total_cost": round(total_cost, 2),
        "cost_per_portion": cost_per_portion,
        "target_food_cost_pct": target_pct,
        "menu_price": menu_price,
        "actual_food_cost_pct": actual_pct,
        "over_target": over_target,
        "priced_count": len(breakdown) - len(unpriced),
        "unpriced_count": len(unpriced),
        "unpriced_items": unpriced,
        "breakdown": breakdown,
    })


@app.route("/api/costing/recipe/<slug>/set-target", methods=["POST"])
def set_recipe_cost_target(slug):
    """Set the menu price and target food cost % for a recipe."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    data = request.get_json() or {}
    menu_price = data.get("menu_price")
    target_pct = data.get("target_food_cost_pct", 30.0)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO recipe_costs (recipe_slug, menu_price, target_food_cost_pct)
        VALUES (%s, %s, %s)
        ON CONFLICT (recipe_slug) DO UPDATE SET
            menu_price = EXCLUDED.menu_price,
            target_food_cost_pct = EXCLUDED.target_food_cost_pct
    """, (slug, menu_price, target_pct))
    cur.close()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/costing/weekly-summary")
def weekly_cost_summary():
    """Weekly food cost summary — invoices scanned, prices updated, dishes over target."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT COUNT(*) as scan_count,
               SUM(items_extracted) as total_items,
               SUM(prices_updated) as total_updates,
               SUM(invoice_total) as total_spend
        FROM invoice_scans
        WHERE user_id = %s AND scan_date >= NOW() - INTERVAL '7 days'
    """, (user["id"],))
    scans = cur.fetchone()
    cur.execute("""
        SELECT recipe_slug, cost_per_portion, actual_food_cost_pct,
               target_food_cost_pct, menu_price
        FROM recipe_costs
        WHERE over_target = true
        ORDER BY actual_food_cost_pct DESC
    """)
    over_target = [dict(r) for r in cur.fetchall()]
    cur.execute("""
        SELECT AVG(actual_food_cost_pct) as avg_food_cost,
               MIN(actual_food_cost_pct) as lowest,
               MAX(actual_food_cost_pct) as highest,
               COUNT(*) as costed_dishes
        FROM recipe_costs
        WHERE actual_food_cost_pct IS NOT NULL
    """)
    avg = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({
        "period": "last_7_days",
        "invoices_scanned": int(scans["scan_count"] or 0),
        "items_extracted": int(scans["total_items"] or 0),
        "prices_updated": int(scans["total_updates"] or 0),
        "total_invoiced_spend": float(scans["total_spend"] or 0),
        "menu_avg_food_cost_pct": round(float(avg["avg_food_cost"] or 0), 1),
        "lowest_food_cost_pct": round(float(avg["lowest"] or 0), 1),
        "highest_food_cost_pct": round(float(avg["highest"] or 0), 1),
        "costed_dishes": int(avg["costed_dishes"] or 0),
        "over_target_count": len(over_target),
        "over_target_dishes": over_target,
    })


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
