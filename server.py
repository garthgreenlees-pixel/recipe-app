# COMPLIANCE GATES: See COMPLIANCE_ROADMAP.md.
# Current stage: BETA.
# Next gate: PRE-LAUNCH — Termly ToS+Privacy, cookie consent, food safety disclaimer, photo consent.

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
from functools import wraps

import io
import time as _time
import re as _re
import urllib.parse as _urllib_parse
import socket
import concurrent.futures as _futures
import psycopg2
import psycopg2.extras
import requests as http_requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file, Response, render_template, render_template_string, g, session, redirect, url_for, flash, abort
from flask_cors import CORS
import anthropic
import fal_client
import stripe
from werkzeug.security import generate_password_hash, check_password_hash
from email_service import send_password_reset_email, send_verification_email
from datetime import datetime as _dt, timedelta as _timedelta
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")
app.config["SESSION_COOKIE_SECURE"] = not bool(os.environ.get("LOCAL_DEV"))
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * 30  # 30-day default

from flask.sessions import SecureCookieSessionInterface as _SCSessionInterface

class _RememberMeSessionInterface(_SCSessionInterface):
    """Extend cookie to 30 days when session['_remember'] is set, else use 7-day default."""
    def get_expiration_time(self, app, session):
        if session.get("_remember"):
            return _dt.utcnow() + _timedelta(days=30)
        return super().get_expiration_time(app, session)

app.session_interface = _RememberMeSessionInterface()

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


def requires_tier(min_tier: str):
    """
    Route decorator. Returns 401 JSON if not logged in, 403 JSON if tier insufficient.
    Usage: @requires_tier("kitchen")
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"error": "Login required"}), 401
            if not user_can_access(min_tier):
                return jsonify({"error": f"{min_tier.title()} tier required"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


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

@app.template_filter('format_event_date')
def format_event_date_filter(value):
    """Format an ISO date string or date object as '14 March 2027'."""
    if not value:
        return ''
    try:
        from datetime import datetime, date
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.split('T')[0])
        elif isinstance(value, date):
            dt = datetime.combine(value, datetime.min.time())
        else:
            dt = value
        return dt.strftime('%-d %B %Y')
    except Exception:
        return str(value)


@app.template_filter('format_timer')
def format_timer(seconds):
    try:
        s = int(seconds)
    except (TypeError, ValueError):
        return ''
    if s < 60:
        return f"{s}s"
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


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

# ── Crawler verification cache: ip -> (verdict: str, expiry: float) ──────────
_crawler_verification_cache: dict = {}
_CRAWLER_CACHE_LOCK = threading.Lock()
CRAWLER_CACHE_TTL = 86400  # 24 hours
_BOT_DNS_POOL = _futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="bot_dns")

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


_CRAWLER_DOMAINS = (
    ".googlebot.com",
    ".google.com",
    ".search.msn.com",
    ".applebot.apple.com",
    ".duckduckgo.com",
)

_CRAWLER_UA_TOKENS = ("googlebot", "bingbot", "applebot", "duckduckbot")


def _dns_classify_crawler(ip: str) -> str:
    """Reverse-DNS verify ip. Returns 'verified', 'non_crawler', or 'inconclusive'."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        if not any(hostname.endswith(d) for d in _CRAWLER_DOMAINS):
            return "non_crawler"
        resolved = socket.gethostbyname(hostname)
        return "verified" if resolved == ip else "non_crawler"
    except (socket.herror, socket.gaierror, socket.timeout, OSError):
        return "inconclusive"


def _classify_crawler(ip: str, ua: str) -> str:
    """Return cached 'verified', 'non_crawler', or 'inconclusive' verdict for this IP/UA."""
    if not any(t in ua.lower() for t in _CRAWLER_UA_TOKENS):
        return "non_crawler"
    now = _time.time()
    with _CRAWLER_CACHE_LOCK:
        entry = _crawler_verification_cache.get(ip)
        if entry is not None and now < entry[1]:
            return entry[0]
    try:
        future = _BOT_DNS_POOL.submit(_dns_classify_crawler, ip)
        verdict = future.result(timeout=3.0)
    except (_futures.TimeoutError, Exception):
        verdict = "inconclusive"
    with _CRAWLER_CACHE_LOCK:
        _crawler_verification_cache[ip] = (verdict, now + CRAWLER_CACHE_TTL)
    return verdict


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


# ── Global error handlers: keep /api/ responses as JSON, never HTML ──────────
from werkzeug.exceptions import HTTPException as _HTTPException


@app.errorhandler(_HTTPException)
def handle_http_exception(e):
    """Convert any Werkzeug HTTP error on /api/ paths to JSON."""
    if request.path.startswith("/api/"):
        import traceback
        app.logger.error(
            f"HTTP {e.code} on {request.path}: {e.description}\n{traceback.format_exc()}"
        )
        return jsonify({"error": e.description or str(e)}), e.code
    if getattr(e, "code", None) == 404:
        return render_template("404.html"), 404
    return e


@app.errorhandler(Exception)
def handle_unhandled_exception(e):
    """Catch any non-HTTP exception that escaped route handlers."""
    if request.path.startswith("/api/"):
        import traceback
        app.logger.error(
            f"Unhandled exception on {request.path}: {traceback.format_exc()}"
        )
        return jsonify({"error": f"Internal error: {str(e)}"}), 500
    return None  # let Flask use default HTML handling for non-API routes


@app.errorhandler(500)
def handle_server_error(e):
    """Branded 500 for HTML paths; JSON for API paths. Crash-proof fallback."""
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error"}), 500
    try:
        return render_template("error_500.html"), 500
    except Exception:
        return (
            '<!DOCTYPE html><html><head><title>Error — Provenance</title>'
            '<meta charset="utf-8"></head><body style="font-family:Georgia,serif;'
            'text-align:center;padding:10vh 24px;color:#1F1B16">'
            '<p style="font-size:12px;letter-spacing:2px;color:#C9A84C">PROVENANCE</p>'
            '<h1 style="font-size:36px;margin:16px 0">Something went wrong.</h1>'
            '<p style="color:#6B6258">Try again, or head back to '
            '<a href="/library" style="color:#C9A84C">the Library</a>.</p>'
            '</body></html>'
        ), 500


@app.before_request
def enforce_security():
    """Global security: block detection, scrape tracking, bulk auth, rate limiting."""
    ip = _get_client_ip()
    ua = request.headers.get("User-Agent", "")

    # ── Blocked IP ────────────────────────────────────────────────────────────
    if _is_blocked(ip):
        return jsonify(error="Access denied"), 403

    # ── Crawler classification ────────────────────────────────────────────────
    _crawler_status = _classify_crawler(ip, ua)
    if _crawler_status == "verified":
        return  # confirmed search-engine bot: bypass all limits
    if _crawler_status == "inconclusive" and any(t in ua.lower() for t in _CRAWLER_UA_TOKENS):
        return  # DNS unresolvable but UA claims known crawler: let through without counting

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

    if response.status_code == 403:
        ua = request.headers.get("User-Agent", "")
        if "bot" in ua.lower() or "spider" in ua.lower() or "crawler" in ua.lower():
            app.logger.warning("[BOT_403] ip=%s path=%s ua=%s",
                               _get_client_ip(), request.path, ua[:120])

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
    cols = "id, name, slug, category, section_slug, facet_technique, origin, description, flavour_context, trigger_keywords, authority_tier, image_url, thumb_url"
    if q:
        cur.execute(
            f"SELECT {cols} FROM technique_references"
            " WHERE category LIKE %s AND published IS NOT FALSE AND (name ILIKE %s OR category ILIKE %s OR origin ILIKE %s)"
            " ORDER BY name LIMIT %s OFFSET %s",
            ("Provenance 1000%", f"%{q}%", f"%{q}%", f"%{q}%", per_page + 1, offset),
        )
    else:
        cur.execute(
            f"SELECT {cols} FROM technique_references"
            " WHERE category LIKE %s AND published IS NOT FALSE ORDER BY name LIMIT %s OFFSET %s",
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
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS open_folio BOOLEAN DEFAULT FALSE",
        """CREATE TABLE IF NOT EXISTS reading_ribbons (
            user_id INT, canon_slug TEXT, section_slug TEXT,
            entry_slug TEXT, entry_name TEXT,
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            PRIMARY KEY (user_id, canon_slug))""",
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
    # ── Costing engine v2 — per-user invoices + pricing ──────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier_invoices (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT NOT NULL,
            supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
            supplier_name TEXT NOT NULL,
            invoice_number TEXT,
            invoice_date DATE,
            invoice_total NUMERIC(10,2),
            currency TEXT DEFAULT 'CAD',
            raw_text TEXT,
            source_pdf_path TEXT,
            extraction_warnings JSONB DEFAULT '[]'::jsonb,
            created_at TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier_invoice_lines (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            invoice_id uuid REFERENCES supplier_invoices(id) ON DELETE CASCADE,
            line_number INTEGER,
            raw_description TEXT NOT NULL,
            quantity NUMERIC(10,3),
            unit TEXT,
            unit_price NUMERIC(10,2),
            line_total NUMERIC(10,2),
            matched_ingredient_id INTEGER REFERENCES ingredient_products(id) ON DELETE SET NULL,
            matched_ingredient_name TEXT,
            match_confidence NUMERIC(3,2),
            created_at TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_pricing (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT NOT NULL,
            ingredient_name TEXT NOT NULL,
            supplier_id INTEGER REFERENCES suppliers(id) ON DELETE SET NULL,
            supplier_name TEXT,
            price_per_unit NUMERIC(10,4) NOT NULL,
            unit TEXT NOT NULL,
            invoice_id uuid REFERENCES supplier_invoices(id) ON DELETE SET NULL,
            invoice_line_id uuid REFERENCES supplier_invoice_lines(id) ON DELETE SET NULL,
            effective_date DATE NOT NULL,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_pricing_user_ingredient_date
        ON ingredient_pricing(user_id, ingredient_name, effective_date DESC)
        WHERE is_active = true
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kitchen_notes (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            recipe_slug TEXT NOT NULL,
            body        TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT now(),
            updated_at  TIMESTAMP DEFAULT now()
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_kitchen_notes_user_recipe
        ON kitchen_notes(user_id, recipe_slug)
    """)
    # ── Recipe v2 columns (additive, all nullable) ─────────────────────────────
    for stmt in [
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS subtitle TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS editorial_showcase BOOLEAN DEFAULT FALSE",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS cuisine_canon VARCHAR(100)",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS eyebrow_override TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS sashimi_standard TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS origin_provenance TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS tradition_tags JSONB DEFAULT '[]'::jsonb",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS markers JSONB DEFAULT '[]'::jsonb",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS flourish TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS pairings JSONB DEFAULT '[]'::jsonb",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS cross_cuisine_parallels JSONB DEFAULT '[]'::jsonb",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS yield_desc TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS active_time TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS total_time TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS glass TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS ice_spec TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS build_method TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS abv TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS vintage TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS wine_region TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS producer TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS drinking_window TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS style TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS brewery TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS abv_ibu TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS serving_temp TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS brew_method TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS yield_volume TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS brew_time TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS origin_estate TEXT",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS last_cooked_at TIMESTAMP",
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS cook_count INTEGER DEFAULT 0",
        # User location for proximity-based supplier ranking (Global Sashimi Rule)
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS user_location TEXT",
        # Costing engine — supplier flags
        "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS user_added BOOLEAN DEFAULT false",
        "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS verification_status TEXT DEFAULT 'verified'",
        # Kitchen notes → recipe_annotations rename (idempotent — fails silently if already done)
        "ALTER TABLE kitchen_notes RENAME TO recipe_annotations",
    ]:
        try:
            cur.execute(stmt)
        except Exception:
            pass
    # ── recipe_kitchen_notes_cache ────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipe_kitchen_notes_cache (
            recipe_slug   TEXT PRIMARY KEY,
            content       JSONB NOT NULL,
            generated_at  TIMESTAMP DEFAULT now()
        )
    """)
    # Grant access to both DB roles. GET requests use provenance_reader (read
    # user) but the cache INSERT also runs in that connection, so it needs
    # INSERT/UPDATE too. Wrapped individually so a missing role doesn't abort.
    for _grant in [
        "GRANT SELECT, INSERT, UPDATE, DELETE ON recipe_kitchen_notes_cache TO provenance_tester_1",
        "GRANT SELECT, INSERT, UPDATE ON recipe_kitchen_notes_cache TO provenance_reader",
    ]:
        try:
            cur.execute(_grant)
        except Exception:
            pass
    # ── user_recipe_markers_read ───────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_recipe_markers_read (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            recipe_slug VARCHAR(500) NOT NULL,
            marker_index INTEGER NOT NULL,
            opened_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(user_id, recipe_slug, marker_index)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_urmr_user_slug ON user_recipe_markers_read(user_id, recipe_slug)")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_kitchen_recipes (
            uuid TEXT PRIMARY KEY,
            user_id INTEGER,
            title TEXT NOT NULL,
            slug TEXT,
            preamble TEXT DEFAULT '',
            tags JSONB DEFAULT '[]',
            ingredients JSONB DEFAULT '[]',
            steps JSONB DEFAULT '[]',
            original_steps JSONB DEFAULT '[]',
            enhanced_steps JSONB DEFAULT '[]',
            time_active TEXT DEFAULT '',
            time_total TEXT DEFAULT '',
            servings JSONB DEFAULT '[]',
            source_name TEXT DEFAULT '',
            source_url TEXT DEFAULT '',
            has_image BOOLEAN DEFAULT FALSE,
            is_draft BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    # Idempotent migration: add slug column to existing installations
    cur.execute("ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS slug TEXT")
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_ukr_slug
        ON user_kitchen_recipes(slug) WHERE slug IS NOT NULL
    """)
    # Backfill slugs for any rows that don't have one yet
    cur.execute("""
        UPDATE user_kitchen_recipes SET
            slug = LOWER(REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(
                title, '[^a-zA-Z0-9 ]', '', 'g'),
                ' +', '-', 'g'), '-+', '-', 'g')) || '-' || LOWER(LEFT(uuid, 6))
        WHERE slug IS NULL
    """)
    # ── user_kitchen_recipes v2 columns (Sashimi Pipeline) ────────────────────
    for stmt in [
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_title TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_author TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_publisher TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_year INTEGER",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_isbn TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_book_page TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS origin TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS quality_hierarchy JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS sensory_tests JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS cross_cuisine_parallels JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS flavour_context TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS lives_or_dies TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS quality_warnings JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS ingredient_origin_markers JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_units_raw JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS servings_text TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS servings_count INTEGER",
        "ALTER TABLE supplier_invoices ADD COLUMN IF NOT EXISTS page_count INTEGER DEFAULT 1",
        # Auth — email verification
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP",
        # v3 recipe cards
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS recipe_content_jsonb JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS template_version VARCHAR(8) DEFAULT 'legacy'",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS faqs JSONB DEFAULT NULL",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS beverage_pairings JSONB DEFAULT NULL",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS enrichment_locked JSONB DEFAULT NULL",
        "ALTER TABLE ingredient_products ADD COLUMN IF NOT EXISTS review_status TEXT",
    ]:
        try:
            cur.execute(stmt)
        except Exception:
            pass
    # Backfill review_status for existing ai-augmented rows
    try:
        cur.execute("""
            UPDATE ingredient_products
            SET review_status = 'pending'
            WHERE source = 'ai-augmented' AND review_status IS NULL
        """)
    except Exception:
        pass
    # ── Password reset tokens ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token VARCHAR(64) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_password_reset_tokens_token ON password_reset_tokens(token)")
    # ── Email verification tokens ─────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token VARCHAR(64) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_email_verification_tokens_token ON email_verification_tokens(token)")
    # ── Auth rate limits ──────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS auth_rate_limits (
            id SERIAL PRIMARY KEY,
            identifier VARCHAR(255) NOT NULL,
            action VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_auth_rate_limits ON auth_rate_limits(identifier, action, created_at)")
    # ── Recipe submissions (editorial review pipeline) ────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipe_submissions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_kitchen_recipe_id TEXT NOT NULL REFERENCES user_kitchen_recipes(uuid) ON DELETE CASCADE,
            submitted_at TIMESTAMPTZ DEFAULT NOW(),
            submitted_by_user_id INTEGER REFERENCES users(id),
            status TEXT DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected','withdrawn')),
            reviewed_at TIMESTAMPTZ,
            reviewer_notes TEXT,
            approved_destination TEXT CHECK (approved_destination IN ('network','provenance_1000') OR approved_destination IS NULL)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_recipe_submissions_recipe_status
        ON recipe_submissions(user_kitchen_recipe_id, status)
    """)
    for stmt in [
        "ALTER TABLE ingredient_aliases ADD COLUMN IF NOT EXISTS confidence NUMERIC(3,2)",
        "ALTER TABLE ingredient_aliases ADD COLUMN IF NOT EXISTS reasoning TEXT",
        "ALTER TABLE ingredient_aliases ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP",
    ]:
        cur.execute(stmt)
    cur.execute("ALTER TABLE ingredient_aliases DROP CONSTRAINT IF EXISTS ingredient_aliases_source_check")
    cur.execute("""
        ALTER TABLE ingredient_aliases
        ADD CONSTRAINT ingredient_aliases_source_check
        CHECK (source IN ('canonical', 'recipe', 'invoice',
                          'user', 'legacy_pricing', 'ai_seed'))
    """)
    # ── Duplicate resolution (Cycle B.2) ──────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_duplicate_candidates (
            id               SERIAL PRIMARY KEY,
            master_id_a      INTEGER NOT NULL REFERENCES ingredient_master(id),
            master_id_b      INTEGER NOT NULL REFERENCES ingredient_master(id),
            similarity_score NUMERIC(4,3) NULL,
            source           TEXT NOT NULL DEFAULT 'sprint_7d_audit',
            created_at       TIMESTAMP DEFAULT NOW(),
            CHECK (master_id_a < master_id_b),
            UNIQUE (master_id_a, master_id_b)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_dup_candidates_a
        ON ingredient_duplicate_candidates(master_id_a)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_dup_candidates_b
        ON ingredient_duplicate_candidates(master_id_b)
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_duplicate_dismissals (
            id           SERIAL PRIMARY KEY,
            user_id      INTEGER NOT NULL REFERENCES users(id),
            master_id_a  INTEGER NOT NULL REFERENCES ingredient_master(id),
            master_id_b  INTEGER NOT NULL REFERENCES ingredient_master(id),
            dismissed_at TIMESTAMP DEFAULT NOW(),
            CHECK (master_id_a < master_id_b),
            UNIQUE (user_id, master_id_a, master_id_b)
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_dup_dismissals_user
        ON ingredient_duplicate_dismissals(user_id)
    """)
    cur.execute("""
        ALTER TABLE ingredient_master
        ADD COLUMN IF NOT EXISTS variant_of INTEGER NULL REFERENCES ingredient_master(id)
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_ingredient_master_variant_of
        ON ingredient_master(variant_of) WHERE variant_of IS NOT NULL
    """)
    # ── Sprint 8 — Menu Builder scaffold ─────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menus (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            slug TEXT NOT NULL UNIQUE,
            owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            event_date DATE,
            cover_count INTEGER NOT NULL DEFAULT 1,
            menu_price DECIMAL(10,2),
            chef_notes TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            last_exported_at TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_menus_owner_user_id ON menus(owner_user_id)
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu_recipes (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            menu_id UUID NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
            recipe_ref TEXT NOT NULL,
            course_name TEXT NOT NULL,
            course_order INTEGER NOT NULL,
            dish_order_within_course INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_menu_recipes_menu_id ON menu_recipes(menu_id)
    """)
    for stmt in [
        "ALTER TABLE recipes ADD COLUMN IF NOT EXISTS allergens JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS allergens JSONB",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS cuisine TEXT",
        "ALTER TABLE user_kitchen_recipes ADD COLUMN IF NOT EXISTS source_pages_count INTEGER DEFAULT 0",
        "ALTER TABLE menus ADD COLUMN IF NOT EXISTS allergen_notes JSONB DEFAULT '{}'::jsonb",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS has_atelier_addon BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS closed_at TIMESTAMP",
        "ALTER TABLE technique_references ADD COLUMN IF NOT EXISTS facet_technique TEXT",
    ]:
        try:
            cur.execute(stmt)
        except Exception:
            pass
    # ── Sprint 8 — l'Atelier composition scaffold ─────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS composition_events (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            kind TEXT NOT NULL,
            menu_id UUID,
            course_name TEXT,
            recipe_id UUID,
            brief TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_composition_events_user_month
            ON composition_events(user_id, created_at)
    """)
    # ── Sprint 8.5 — Beverage pairing suggestions queue ───────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS beverage_pairing_suggestions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            recipe_ref TEXT NOT NULL,
            beverage_product_id INTEGER NOT NULL REFERENCES beverage_products(id) ON DELETE CASCADE,
            source_tier TEXT NOT NULL,
            role TEXT,
            descriptor TEXT,
            match_score NUMERIC,
            match_reasoning TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            suggested_at TIMESTAMP NOT NULL DEFAULT NOW(),
            reviewed_at TIMESTAMP,
            reviewed_by INTEGER REFERENCES users(id),
            CONSTRAINT bps_status_values CHECK (status IN ('pending','approved','rejected'))
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_bev_pair_sugg_status_ref
            ON beverage_pairing_suggestions(status, recipe_ref)
    """)
    cur.close()
    conn.close()


import os
if not os.environ.get("SKIP_INIT_DB"):
    init_db()


# ─── Tag sanitizer ───────────────────────────────────────────────────────────

_TAG_STOPWORDS = frozenset({
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'as', 'it', 'its', 'this', 'that', 'into', 'out', 'up', 'if', 'no',
    'not', 'so', 'do', 'did', 'does', 'he', 'she', 'we', 'you', 'i',
    'my', 'your', 'our', 'their', 'which', 'who', 'what', 'likely',
    'development', 'than', 'about',
})

def _sanitize_tags(tags, limit=6):
    """Return ≤limit clean facet tags: strip punctuation, drop stopword-only tokens, reject >3-word phrases."""
    import re as _re2
    out = []
    seen = set()
    for t in (tags or []):
        t = _re2.sub(r"[^\w\s\-]", "", str(t)).strip().lower()
        if not t or t in seen:
            continue
        words = t.split()
        if not words:
            continue
        if len(words) == 1 and words[0] in _TAG_STOPWORDS:
            continue
        if len(words) > 3:
            continue
        seen.add(t)
        out.append(t)
        if len(out) >= limit:
            break
    return out


_KNOWN_CUISINES = frozenset({
    'british', 'english', 'scottish', 'welsh', 'irish',
    'french', 'italian', 'spanish', 'portuguese', 'greek',
    'german', 'austrian', 'swiss', 'belgian', 'dutch',
    'swedish', 'danish', 'norwegian', 'finnish',
    'russian', 'polish', 'hungarian', 'czech',
    'turkish', 'lebanese', 'syrian', 'moroccan', 'persian',
    'egyptian', 'israeli',
    'indian', 'pakistani', 'bangladeshi', 'sri lankan',
    'chinese', 'japanese', 'korean', 'vietnamese', 'thai',
    'cambodian', 'indonesian', 'malaysian', 'filipino',
    'mexican', 'peruvian', 'colombian', 'brazilian', 'argentinian',
    'cuban', 'jamaican', 'caribbean', 'dominican',
    'american', 'southern', 'cajun', 'creole',
    'west african', 'east african', 'ethiopian', 'nigerian',
    'mediterranean', 'eastern mediterranean', 'middle eastern',
    'latin american', 'south asian', 'southeast asian',
    'central asian', 'nordic', 'scandinavian',
    'georgian', 'armenian', 'azerbaijani', 'balinese', 'acehnese',
    'sundanese', 'sicilian', 'venetian', 'provencal',
})

def _sanitize_cuisine(cuisine):
    """Return a short cuisine label (≤3 words) or None if input is prose."""
    import re as _re3
    if not cuisine:
        return None
    s = _re3.sub(r'[^\w\s\-/]', '', str(cuisine)).strip().lower()
    if not s:
        return None
    words = s.split()
    if len(words) <= 3:
        return s
    # Too long — it's prose. Try to extract a known cuisine name.
    for n in range(3, 0, -1):
        for i in range(len(words) - n + 1):
            candidate = ' '.join(words[i:i + n])
            if candidate in _KNOWN_CUISINES:
                return candidate
    return None


# ─── Static files ────────────────────────────────────────────────────────────

def _format_cuisine(raw):
    """Normalise a cuisine DB key for display.

    INDIGENOUS_AUSTRALIAN → 'Indigenous Australian'
    FRENCH_BURGUNDY       → 'French · Burgundy'
    None / '' / 'MY KITCHEN' placeholders → 'Uncategorised'
    """
    if not raw or not str(raw).strip():
        return "Uncategorised"
    s = str(raw).strip()
    if s.upper() in ("MY KITCHEN", "MY_KITCHEN", "MYKITCHEN"):
        return "Uncategorised"
    parts = s.replace("_", " ").split()
    if len(parts) == 1:
        return parts[0].title()
    return " · ".join(p.title() for p in parts)


_SOURCE_PANTRY_STOP = {
    "water", "salt", "kosher salt", "sea salt", "flaky sea salt", "fine salt",
    "pepper", "black pepper", "cracked black pepper", "white pepper",
    "butter", "unsalted butter", "salted butter",
    "oil", "olive oil", "vegetable oil", "neutral oil",
    "flour", "all-purpose flour", "ap flour",
    "sugar", "granulated sugar", "white sugar",
    "ice", "ice water", "boiling water", "tamarind water",
}


def _is_recent(dt, days=14):
    """True if a timestamp is within the last `days` (for the Recently-added chip)."""
    if not dt:
        return False
    try:
        now = _dt.now(dt.tzinfo) if getattr(dt, "tzinfo", None) else _dt.now()
        return (now - dt) <= _timedelta(days=days)
    except Exception:
        return False


def _recipe_has_sourcing(markers):
    """Cheap per-card 'Sourced' verdict: True if any non-pantry ingredient marker
    carries at least one resolved supplier. Deliberately DB-free (the full
    origin/provider classification in _get_kitchen_recipe_suppliers_from_markers
    is too heavy to run per card in the kitchen list)."""
    if isinstance(markers, str):
        try:
            markers = json.loads(markers)
        except Exception:
            return False
    if not markers:
        return False
    for m in markers:
        if not isinstance(m, dict):
            continue
        name = (m.get("ingredient_name") or "").strip().lower()
        if name in _SOURCE_PANTRY_STOP:
            continue
        if m.get("suppliers") or m.get("matched_supplier_ids"):
            return True
    return False


def _query_user_recipes(user_id, state="imported"):
    """Return a list of card-ready dicts from user_kitchen_recipes for one user.

    State is derived (no DB column): 'enhanced' when recipe_content_jsonb is
    populated or template_version is 'v3'; 'imported' otherwise.
    """
    if not DATABASE_URL:
        return []
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT uuid, title, slug, has_image, origin, cuisine, time_total,
                   servings_count, servings_text, template_version,
                   recipe_content_jsonb, tags,
                   quality_hierarchy, sensory_tests, cross_cuisine_parallels,
                   lives_or_dies, beverage_pairings, ingredients, steps,
                   ingredient_origin_markers, created_at
            FROM user_kitchen_recipes
            WHERE user_id = %s AND is_draft = FALSE AND slug IS NOT NULL
            ORDER BY updated_at DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        out = []
        for r in rows:
            is_enhanced = (
                r.get("template_version") == "v3"
                or (r.get("recipe_content_jsonb") is not None)
            )
            row_state = "enhanced" if is_enhanced else "imported"
            if row_state != state:
                continue
            # Pillar fill count: ingredients, steps, quality_hierarchy,
            # sensory_tests, cross_cuisine_parallels, lives_or_dies, beverage_pairings
            filled = sum([
                bool(r.get("ingredients")),
                bool(r.get("steps") or (r.get("recipe_content_jsonb") or {}).get("steps")),
                bool(r.get("quality_hierarchy")),
                bool(r.get("sensory_tests")),
                bool(r.get("cross_cuisine_parallels")),
                bool(r.get("lives_or_dies")),
                bool(r.get("beverage_pairings")),
            ])
            # Cuisine: prefer content_jsonb cuisine key, fall back to origin
            content = r.get("recipe_content_jsonb") or {}
            cuisine = r.get("cuisine") or content.get("cuisine") or _sanitize_cuisine(r.get("origin")) or ""
            # Time: prefer content_jsonb, fall back to raw text field
            time_raw = content.get("time_total") or r.get("time_total") or ""
            serves_raw = r.get("servings_count") or r.get("servings_text") or ""
            image_url = f"/images/{r['uuid']}/hero.jpg" if r.get("has_image") else None
            raw_tags = r.get("tags") or []
            if isinstance(raw_tags, str):
                try:
                    raw_tags = json.loads(raw_tags)
                except Exception:
                    raw_tags = []
            out.append({
                "uuid": r["uuid"],
                "slug": r["slug"],
                "title": r.get("title") or "Untitled",
                "image_url": image_url,
                "cuisine": cuisine,
                "state": row_state,
                "pillars_filled": filled,
                "time_display": time_raw,
                "serves": serves_raw,
                "requires_haccp": _detect_raw_served(*_recipe_dict_to_haccp_inputs(r)),
                "card_tags": _sanitize_tags(raw_tags, limit=2),
                "sourced": _recipe_has_sourcing(r.get("ingredient_origin_markers")),
                "recent": _is_recent(r.get("created_at")),
            })
        return out
    except Exception as e:
        app.logger.warning(f"_query_user_recipes failed: {e}")
        return []


def _query_user_saved_canon_recipes(user_id):
    """Return canon recipes saved by the user. Feature not yet built — returns empty."""
    return []


def _query_compose_drafts(user_id):
    """Return compose-draft kitchen recipes for a user (is_draft=TRUE rows from l'Atelier)."""
    if not DATABASE_URL:
        return []
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT uuid, title, slug, has_image, origin, cuisine, time_total,
                   servings_count, servings_text, template_version,
                   recipe_content_jsonb, tags,
                   quality_hierarchy, sensory_tests, cross_cuisine_parallels,
                   lives_or_dies, beverage_pairings, ingredients, steps,
                   ingredient_origin_markers, created_at
            FROM user_kitchen_recipes
            WHERE user_id = %s AND is_draft = TRUE AND slug IS NOT NULL
            ORDER BY updated_at DESC
        """, (user_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        out = []
        for r in rows:
            filled = sum([
                bool(r.get("ingredients")),
                bool(r.get("steps") or (r.get("recipe_content_jsonb") or {}).get("steps")),
                bool(r.get("quality_hierarchy")),
                bool(r.get("sensory_tests")),
                bool(r.get("cross_cuisine_parallels")),
                bool(r.get("lives_or_dies")),
                bool(r.get("beverage_pairings")),
            ])
            content = r.get("recipe_content_jsonb") or {}
            cuisine = r.get("cuisine") or content.get("cuisine") or _sanitize_cuisine(r.get("origin")) or ""
            time_raw = content.get("time_total") or r.get("time_total") or ""
            serves_raw = r.get("servings_count") or r.get("servings_text") or ""
            image_url = f"/images/{r['uuid']}/hero.jpg" if r.get("has_image") else None
            raw_tags = r.get("tags") or []
            if isinstance(raw_tags, str):
                try:
                    raw_tags = json.loads(raw_tags)
                except Exception:
                    raw_tags = []
            out.append({
                "uuid": r["uuid"],
                "slug": r["slug"],
                "title": r.get("title") or "Untitled",
                "image_url": image_url,
                "cuisine": cuisine,
                "state": "compose_draft",
                "pillars_filled": filled,
                "time_display": time_raw,
                "serves": serves_raw,
                "requires_haccp": _detect_raw_served(*_recipe_dict_to_haccp_inputs(r)),
                "card_tags": _sanitize_tags(raw_tags, limit=2),
                "sourced": _recipe_has_sourcing(r.get("ingredient_origin_markers")),
                "recent": _is_recent(r.get("created_at")),
            })
        return out
    except Exception as e:
        app.logger.warning(f"_query_compose_drafts failed: {e}")
        return []


@app.route("/")
def index():
    counts_techniques = 0
    counts_recipes = 0
    img_carbonara = ""
    img_phatthai = ""
    img_beurreblanc = ""
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT
                  (SELECT COUNT(*) FROM technique_references WHERE published IS NOT FALSE) AS techniques,
                  (SELECT COUNT(*) FROM technique_references WHERE category LIKE 'Provenance 1000%%' AND published IS NOT FALSE) AS recipes_std
            """)
            row = cur.fetchone()
            if row:
                counts_techniques = "{:,}".format(row[0])
                counts_recipes = "{:,}".format(row[1])
            cur.execute(
                "SELECT name, image_url FROM recipes WHERE lower(name) LIKE %s AND is_curated = TRUE LIMIT 1",
                ('%carbonara%',)
            )
            r = cur.fetchone()
            if r:
                img_carbonara = r[1] or ""
            cur.execute(
                "SELECT name, image_url FROM recipes WHERE (lower(name) LIKE %s OR lower(name) LIKE %s) AND is_curated = TRUE LIMIT 1",
                ('%phat thai%', '%pad thai%')
            )
            r = cur.fetchone()
            if r:
                img_phatthai = r[1] or ""
            cur.execute(
                "SELECT name, image_url FROM technique_references"
                " WHERE lower(name) LIKE %s AND published IS NOT FALSE ORDER BY id LIMIT 1",
                ('%beurre blanc%',)
            )
            r = cur.fetchone()
            if r:
                img_beurreblanc = r[1] or ""
            cur.close()
            conn.close()
        except Exception as e:
            app.logger.error("homepage counts/images query failed: %s", e)
            sentry_sdk.capture_exception(e)
    return render_template(
        "homepage_landing.html",
        counts_techniques=counts_techniques,
        counts_recipes=counts_recipes,
        img_carbonara=img_carbonara,
        img_phatthai=img_phatthai,
        img_beurreblanc=img_beurreblanc,
    )


@app.route("/kitchen")
def kitchen():
    user = get_current_user()
    if not user:
        return _login_redirect()
    user_id = user["id"]
    recipes_by_state = {
        "imported": _query_user_recipes(user_id, state="imported"),
        "enhanced": _query_user_recipes(user_id, state="enhanced"),
        "canon_saved": _query_user_saved_canon_recipes(user_id),
        "compose_draft": _query_compose_drafts(user_id),
    }
    total = sum(len(v) for v in recipes_by_state.values())
    # ── Menus (Library+) ──
    has_library = user_can_access("library")
    user_menus = []
    if has_library:
        _mc = get_db()
        _mcur = _mc.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        _mcur.execute("""
            SELECT m.id, m.slug, m.title, m.event_date, m.cover_count, m.updated_at,
                   COUNT(DISTINCT mr.course_name) AS course_count,
                   COUNT(mr.id) AS dish_count
            FROM menus m
            LEFT JOIN menu_recipes mr ON mr.menu_id = m.id
            WHERE m.owner_user_id = %s
            GROUP BY m.id
            ORDER BY m.event_date DESC NULLS LAST, m.updated_at DESC
        """, (user_id,))
        user_menus = [dict(r) for r in _mcur.fetchall()]
        for m in user_menus:
            m["id"] = str(m["id"])
            m["course_count"] = int(m["course_count"])
            m["dish_count"] = int(m["dish_count"])
            if m.get("event_date"):
                m["event_date"] = m["event_date"].isoformat()
            if m.get("updated_at"):
                m["updated_at"] = m["updated_at"].isoformat()
        _mcur.close(); _mc.close()
    # Real stat counts for the working-shelf band. Sourced is now real (derived
    # from ingredient_origin_markers per card). Enhanced/Drafts kept as honest
    # substitutes per founder ruling until Collections + Cooked-this-week land
    # (Cycle 2), when the design's canonical four go fully real.
    _sourced_count = sum(
        1 for _lst in recipes_by_state.values() for _r in _lst if _r.get("sourced")
    )
    kitchen_stats = {
        "recipes": total,
        "sourced": _sourced_count,
        "enhanced": len(recipes_by_state["enhanced"]),
        "drafts": len(recipes_by_state["compose_draft"]),
        "menus": len(user_menus),
    }
    # cuisines present in the shelf, for the filter chips (real, from the cards)
    _cuis = []
    for _lst in recipes_by_state.values():
        for _r in _lst:
            _c = (_r.get("cuisine") or "").split("·")[0].split(",")[0].strip()
            if _c and _c not in _cuis:
                _cuis.append(_c)
    kitchen_cuisines = sorted(_cuis)[:6]
    return render_template(
        "kitchen.html",
        recipes_by_state=recipes_by_state,
        recipe_total=total,
        kitchen_stats=kitchen_stats,
        kitchen_cuisines=kitchen_cuisines,
        format_cuisine=_format_cuisine,
        has_library=has_library,
        user_menus=user_menus,
    )


@app.route("/table")
def table():
    return render_template("table.html")


def _normalize_member_recipe(kitchen_recipe):
    """Return a dict that matches the field names recipe.html expects.

    Handles both legacy member recipes (flat steps/ingredients) and v3 recipes
    (data in recipe_content_jsonb with ingredient_groups / method_steps).
    Always adds image_url derived from has_image + uuid.
    """
    row = dict(kitchen_recipe)
    content = row.get("recipe_content_jsonb") or {}

    # Title
    row.setdefault("name", row.get("title") or content.get("title") or "Untitled")

    # Image URL
    if row.get("has_image") and row.get("uuid"):
        row["image_url"] = f"/images/{row['uuid']}/hero.jpg"
    else:
        row.setdefault("image_url", None)

    # Cuisine — dedicated column, then content_jsonb, then sanitize origin prose
    if not row.get("cuisine"):
        row["cuisine"] = content.get("cuisine") or _sanitize_cuisine(row.get("origin")) or ""

    # Ingredients — v3 uses ingredient_groups; legacy uses raw ingredients list
    if not row.get("ingredients"):
        grps = content.get("ingredient_groups", [])
        if grps:
            row["ingredients"] = [
                {
                    "group": g.get("group", ""),
                    "items": [
                        {"name": item.get("name", ""), "amount": item.get("amount", ""), "unit": ""}
                        for item in g.get("items", [])
                    ],
                }
                for g in grps
            ]

    # Steps — v3 uses method_steps; legacy uses steps
    if not row.get("steps"):
        m_steps = content.get("method_steps", [])
        if m_steps:
            row["steps"] = [
                {"instruction": s.get("body", "") or s.get("title", "")}
                for s in m_steps
            ]

    # Sensory tests — lives_or_dies already in row; v3 may use sensory_standard
    if not row.get("sashimi_standard"):
        row["sashimi_standard"] = (
            row.get("lives_or_dies")
            or content.get("sensory_standard")
            or content.get("sashimi_standard")
        )

    # Origin / lineage
    if not row.get("origin_provenance"):
        row["origin_provenance"] = (
            row.get("origin")
            or content.get("origin")
            or content.get("cultural_origin")
        )

    # Map kitchen tags → tradition_tags for recipe page display (clamped to 6)
    if not row.get("tradition_tags"):
        raw_tags = row.get("tags") or []
        if isinstance(raw_tags, str):
            try:
                raw_tags = json.loads(raw_tags)
            except Exception:
                raw_tags = []
        row["tradition_tags"] = _sanitize_tags(raw_tags, limit=6)

    return row


def _get_allergens_for_region(recipe, region):
    """Allergen detection stub — returns empty until allergen data lands in DB."""
    return []


# Keyword map for CA Priority 11 allergens (ingredient-name based matching)
_ALLERGEN_KEYWORDS = {
    "eggs": ["egg", "eggs", "mayonnaise", "mayo", "aioli", "hollandaise", "meringue",
             "custard", "omelette", "omelet", "frittata", "quiche"],
    "milk": ["milk", "cream", "butter", "cheese", "yogurt", "yoghurt", "ghee", "beurre",
             "whey", "casein", "lactose", "dairy", "ricotta", "mozzarella", "parmesan",
             "cheddar", "brie", "camembert", "feta", "mascarpone", "creme fraiche",
             "crème fraîche", "crème", "dulce de leche", "bechamel", "béchamel"],
    "mustard": ["mustard", "dijon", "moutarde"],
    "peanuts": ["peanut", "groundnut", "groundnut oil"],
    "crustaceans_molluscs": ["shrimp", "prawn", "crab", "lobster", "langoustine",
                             "crawfish", "crayfish", "mussel", "oyster", "scallop",
                             "clam", "squid", "octopus", "calamari", "abalone",
                             "whelk", "cockle", "periwinkle"],
    "fish": ["salmon", "tuna", "cod", "halibut", "sea bass", "anchov", "sardine",
             "mackerel", "herring", "haddock", "tilapia", "trout", "bream",
             "snapper", "flounder", "sole", "mahi", "swordfish", "pollock",
             "fish sauce", "fish stock", "worcestershire", "worcester"],
    "sesame": ["sesame", "tahini", "hummus"],
    "soy": ["soy", "soya", "tofu", "miso", "tempeh", "edamame", "tamari",
            "natto", "soy sauce", "shoyu"],
    "sulphites": ["wine", "white wine", "red wine", "wine vinegar", "champagne",
                  "dried apricot", "dried fruit", "raisin", "sultana", "currant",
                  "beer", "cider", "pickle", "pickled"],
    "tree_nuts": ["almond", "walnut", "pecan", "cashew", "pistachio", "hazelnut",
                  "macadamia", "brazil nut", "chestnut", "pine nut", "pine kernel",
                  "praline", "marzipan", "nougat"],
    "wheat_triticale": ["wheat", "flour", "bread", "pasta", "noodle", "couscous",
                        "semolina", "bulgur", "barley", "rye", "crouton",
                        "breadcrumb", "batter", "crust", "dough", "seitan",
                        "panko", "tortilla", "roux", "soba"],
}


def _detect_allergens_for_recipe(recipe_dict, region="CA"):
    """Keyword-based allergen detection from ingredient list + steps text.

    Returns a cache dict: {"region": region, "detected": [list], "detected_at": iso}.
    Always writes a result so subsequent adds read from cache rather than re-detecting.
    """
    import datetime
    try:
        ingredients, method_steps = _recipe_dict_to_haccp_inputs(recipe_dict)
        all_text = " ".join(ingredients + method_steps).lower()
        detected = []
        for allergen, keywords in _ALLERGEN_KEYWORDS.items():
            if any(kw in all_text for kw in keywords):
                detected.append(allergen)
        return {
            "region": region,
            "detected": detected,
            "detected_at": datetime.datetime.utcnow().isoformat(),
        }
    except Exception as exc:
        import datetime
        return {
            "region": region,
            "detected": [],
            "detected_at": datetime.datetime.utcnow().isoformat(),
            "error": str(exc),
        }


def _is_raw_served(recipe_dict):
    return _detect_raw_served(*_recipe_dict_to_haccp_inputs(recipe_dict))


def _generate_haccp_brief_internal(title, ingredients, method_steps, allergen_region):
    """Call the HACCP generator and return the parsed JSON dict, or None on failure."""
    system_prompt = build_haccp_system_prompt(title, ingredients, allergen_region)
    ingredients_text = json.dumps(ingredients, ensure_ascii=False)
    method_text = json.dumps(method_steps, ensure_ascii=False)
    user_message = (
        f"Recipe: {title}\n"
        f"Ingredients (JSON): {ingredients_text}\n"
        f"Method steps (JSON): {method_text}\n\n"
        f"Generate the structured HACCP brief now. Return JSON only."
    )
    required_keys = {"schema_version", "recipe_name", "allergens", "process_flow", "ccp_table"}
    for attempt in range(1, 3):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=8192,
                timeout=90.0,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            raw_text = resp.content[0].text.strip()
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```", 2)[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.rsplit("```", 1)[0].strip()
            brief = json.loads(raw_text)
            missing = required_keys - set(brief.keys())
            if missing:
                raise ValueError(f"Missing required sections: {', '.join(sorted(missing))}")
            from datetime import datetime as _dt_inner, timezone as _tz_inner
            brief["generated_at"] = _dt_inner.now(_tz_inner.utc).isoformat()
            return brief
        except Exception as e:
            app.logger.warning(f"[HACCP internal] attempt {attempt}/2 failed: {e}")
            if attempt < 2:
                _time.sleep(1)
    return None


def _get_or_build_haccp_brief(recipe, region):
    """Look up a saved HACCP brief for this recipe at Profession tier. Never auto-generates."""
    if not user_can_access("profession"):
        return None
    user = get_current_user()
    if not user:
        return None
    recipe_slug = recipe.get("slug") or recipe.get("recipe_slug")
    if not recipe_slug:
        return None
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT id, version, brief_json, edits_json, pic_name, pic_signed_at, created_at
            FROM haccp_briefs
            WHERE user_id = %s AND recipe_slug = %s
            ORDER BY version DESC LIMIT 1
        """, (user["id"], recipe_slug))
        row = cur.fetchone()
        cur.close()
        conn.close()
    except Exception:
        return None
    if not row:
        return None
    brief = row["brief_json"]
    if isinstance(brief, str):
        brief = json.loads(brief)
    edits = row["edits_json"] or {}
    if isinstance(edits, str):
        edits = json.loads(edits)
    brief = _apply_haccp_edits(brief, edits)
    brief["_db_id"] = row["id"]
    brief["_version"] = row["version"]
    brief["_pic_name"] = row["pic_name"]
    brief["_pic_signed_at"] = row["pic_signed_at"].isoformat() if row["pic_signed_at"] else None
    brief["_generated_at"] = row["created_at"].isoformat() if row["created_at"] else None
    brief["_edits"] = edits  # flat user edits (calibration, signoff fields, dates)
    return brief


def _compute_recipe_cost(recipe, region):
    """Server-render cost breakdown for recipe.html. Returns None if no ingredients."""
    slug = recipe.get("slug", "")
    ingredients = recipe.get("ingredients") or []
    if isinstance(ingredients, str):
        try:
            ingredients = json.loads(ingredients)
        except Exception:
            ingredients = []
    if not ingredients:
        return None

    user = get_current_user()
    user_id = str(user["id"]) if user else None
    use_user_pricing = user_id is not None and user_can_access("kitchen")

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM recipe_costs WHERE recipe_slug = %s", (slug,))
    cached = cur.fetchone()

    breakdown, total_cost, unpriced, unit_warning_items = _cost_ingredient_loop(
        ingredients, user_id, use_user_pricing, cur
    )

    cur.close()
    conn.close()

    servings_raw = recipe.get("servings") or []
    if isinstance(servings_raw, str):
        try:
            servings_raw = json.loads(servings_raw)
        except Exception:
            servings_raw = []
    portions = 4
    if isinstance(servings_raw, list) and servings_raw:
        try:
            portions = int(float(servings_raw[0].get("count", 4)))
        except Exception:
            portions = 4
    elif isinstance(servings_raw, (int, float)):
        portions = int(servings_raw)
    portions = portions or 4

    cost_per_portion = round(total_cost / portions, 2)
    target_pct = float(cached["target_food_cost_pct"]) if cached and cached.get("target_food_cost_pct") else 30.0
    menu_price = float(cached["menu_price"]) if cached and cached.get("menu_price") else None
    actual_pct = round((cost_per_portion / menu_price) * 100, 1) if menu_price and menu_price > 0 else None
    over_target = actual_pct > target_pct if actual_pct is not None else False

    return {
        "slug": slug,
        "portions": portions,
        "total_cost": round(total_cost, 2),
        "cost_per_portion": cost_per_portion,
        "target_food_cost_pct": target_pct,
        "menu_price": menu_price,
        "actual_food_cost_pct": actual_pct,
        "over_target": over_target,
        "priced_count": len(breakdown) - len(unpriced) - len(unit_warning_items),
        "unpriced_count": len(unpriced),
        "unpriced_items": unpriced,
        "unit_warning_count": len(unit_warning_items),
        "unit_warning_items": unit_warning_items,
        "breakdown": breakdown,
    }


def _resolve_recipe_ref(ref, user_id, cur):
    """Resolve a polymorphic recipe_ref to a recipe dict.

    "canon:<slug>"   → recipes table (public, no ownership check).
    "kitchen:<uuid>" → user_kitchen_recipes (scoped to user_id).
    Returns dict on success, None on miss. Raises ValueError on malformed ref.
    """
    if not ref or ':' not in ref:
        raise ValueError(f"Malformed recipe_ref: {ref!r}")
    prefix, _, key = ref.partition(':')
    if prefix == 'canon':
        cur.execute("SELECT * FROM recipes WHERE slug = %s LIMIT 1", (key,))
    elif prefix == 'technique':
        cur.execute("SELECT * FROM technique_references WHERE slug = %s AND published IS NOT FALSE LIMIT 1", (key,))
    elif prefix == 'kitchen':
        if not user_id:
            return None
        cur.execute(
            "SELECT * FROM user_kitchen_recipes WHERE uuid = %s AND user_id = %s LIMIT 1",
            (key, int(user_id))
        )
    else:
        raise ValueError(f"Unknown recipe_ref prefix: {prefix!r}")
    row = cur.fetchone()
    return dict(row) if row else None


_P1000_CAT_RE = _re.compile(r'^Provenance 1000\s*[—\-]\s*')

@app.route("/recipes")
def recipes_page():
    initial_recipes = []
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                "SELECT id, name, slug, category, section_slug, facet_technique, image_url, thumb_url"
                " FROM technique_references"
                " WHERE category LIKE %s ORDER BY name LIMIT 24",
                ("Provenance 1000%",)
            )
            for row in cur.fetchall():
                r = dict(row)
                r['cat_label'] = _P1000_CAT_RE.sub('', r.get('category') or '')
                initial_recipes.append(r)
            cur.close()
            conn.close()
        except Exception:
            initial_recipes = []
    return render_template("recipes.html", initial_recipes=initial_recipes)


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
    stats = {"techniques": 12198, "p1000": 686, "beverages": 3654, "suppliers": 91}
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT
                  (SELECT COUNT(*) FROM technique_references) AS techniques,
                  (SELECT COUNT(*) FROM technique_references WHERE category LIKE 'Provenance 1000%%') AS p1000,
                  (SELECT COUNT(*) FROM beverage_products WHERE is_published IS TRUE) AS beverages,
                  (SELECT COUNT(*) FROM suppliers) AS suppliers
            """)
            row = cur.fetchone()
            cur.close(); conn.close()
            if row:
                stats = {"techniques": row[0], "p1000": row[1], "beverages": row[2], "suppliers": row[3]}
        except Exception:
            pass
    return render_template("about.html", stats=stats)


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


@app.route("/api/kitchen-recipe/<slug>/generate-image", methods=["POST"])
def generate_kitchen_recipe_image(slug):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        return jsonify({"error": "FAL_KEY not configured"}), 503

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            "SELECT uuid, user_id, title, preamble, tags, ingredients, origin, has_image "
            "FROM user_kitchen_recipes WHERE slug = %s LIMIT 1",
            (slug,)
        )
        recipe = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    if recipe["user_id"] != user["id"]:
        return jsonify({"error": "Not your recipe"}), 403

    recipe_uuid = recipe["uuid"]

    if recipe.get("has_image"):
        return jsonify({"ok": True, "url": f"/images/{recipe_uuid}/hero.jpg"})

    tags = recipe.get("tags") or []
    if isinstance(tags, str):
        tags = json.loads(tags)
    cuisine = (tags[0] if tags else None) or recipe.get("origin")
    description = recipe.get("preamble") or ""
    ingredients = recipe.get("ingredients") or []
    if isinstance(ingredients, str):
        ingredients = json.loads(ingredients)

    accuracy_brief = get_dish_accuracy_brief(
        recipe_name=recipe["title"],
        cuisine=cuisine,
        description=description
    )

    attempts = []
    final_url = None
    final_passed = False
    max_attempts = 3

    os.environ["FAL_KEY"] = fal_key

    for attempt in range(max_attempts):
        retry_guidance = attempts[-1].get("retry_guidance", "") if attempts else ""
        if retry_guidance and accuracy_brief:
            accuracy_brief["prompt_phrase"] = (
                accuracy_brief.get("prompt_phrase", "") + " " + retry_guidance
            )
        prompt = build_provenance_food_prompt(
            recipe_name=recipe["title"],
            cuisine=cuisine,
            ingredients=ingredients,
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
                image_url, recipe["title"], accuracy_brief
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
        return jsonify({"ok": False, "error": "All generation attempts failed", "attempts": attempts}), 502

    img_bytes = http_requests.get(final_url, timeout=30).content
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    save_hero_image(recipe_uuid, img_b64)
    image_dir = EXTRACTED_DIR / recipe_uuid
    image_dir.mkdir(parents=True, exist_ok=True)
    (image_dir / "hero.jpg").write_bytes(img_bytes)
    conn2 = get_db()
    cur2 = conn2.cursor()
    cur2.execute("UPDATE user_kitchen_recipes SET has_image = TRUE WHERE uuid = %s", (recipe_uuid,))
    conn2.commit()
    cur2.close()
    conn2.close()

    return jsonify({"ok": True, "url": f"/images/{recipe_uuid}/hero.jpg"})


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

    try:
        thumb = _make_card_thumbnail(final_url)
        if thumb:
            tconn = get_db()
            tcur = tconn.cursor()
            tcur.execute("UPDATE technique_references SET thumb_url = %s WHERE id = %s", (thumb, tech["id"]))
            tconn.commit()
            tcur.close(); tconn.close()
    except Exception:
        pass

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


_REGION_TOKEN_MAP = {
    'nationwide_US': 'Nationwide US',
    'nationwide_CA': 'Nationwide Canada',
    'nationwide_UK': 'Nationwide UK',
    'nationwide_AU': 'Nationwide Australia',
    'nationwide_NZ': 'Nationwide NZ',
    'worldwide': 'Worldwide',
    'worldwide_export': 'Worldwide',
    'BC': 'British Columbia',
    'AB': 'Alberta',
    'WA': 'Washington',
    'OR': 'Oregon',
    'PNW': 'Pacific Northwest',
    'Western_Canada': 'Western Canada',
    'UK': 'United Kingdom',
    'Southeast_Asia': 'Southeast Asia',
    'Saudi_Arabia': 'Saudi Arabia',
    'Hong_Kong': 'Hong Kong',
}
_REGION_DROP = {'wholesale', 'nationwide_shipping'}
_COUNTRY_MAP = {
    'US': 'United States', 'CA': 'Canada', 'UK': 'United Kingdom',
    'GB': 'United Kingdom', 'NZ': 'New Zealand', 'AU': 'Australia',
    'SG': 'Singapore', 'FR': 'France', 'ID': 'Indonesia', 'JP': 'Japan',
}

def _normalise_supplier_regions(service_region, country=None):
    def _fmt(tok):
        tok = tok.strip()
        if not tok:
            return None
        if tok.lower() in _REGION_DROP:
            return None
        if tok in _REGION_TOKEN_MAP:
            return _REGION_TOKEN_MAP[tok]
        parts = tok.split('_')
        return ' '.join(p if p.isupper() else p.title() for p in parts)

    if not service_region:
        if country:
            return _COUNTRY_MAP.get(country, country)
        return 'Region not specified'

    tokens = [service_region] if isinstance(service_region, str) else list(service_region)
    seen, result = set(), []
    for tok in tokens:
        display = _fmt(tok)
        if display is None:
            continue
        key = display.lower()
        if key not in seen:
            seen.add(key)
            result.append(display)

    if not result:
        if country:
            return _COUNTRY_MAP.get(country, country)
        return 'Region not specified'

    if len(result) > 5:
        return ' · '.join(result[:5]) + f' · +{len(result) - 5} more'
    return ' · '.join(result)


@app.route("/suppliers")
def suppliers_page():
    if not DATABASE_URL:
        return render_template("suppliers.html", suppliers=[])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    product_id = request.args.get('product_id', type=int)
    if product_id:
        cur.execute("""
            SELECT s.id, s.name, s.notes, s.website, s.service_region,
                   s.is_featured, s.country,
                   COUNT(ps.id) as product_count
            FROM suppliers s
            JOIN product_suppliers ps ON s.id = ps.supplier_id
            WHERE ps.product_id = %s AND UPPER(ps.role) = 'PROVIDER'
            GROUP BY s.id
            ORDER BY s.is_featured DESC NULLS LAST, product_count DESC
        """, (product_id,))
    else:
        cur.execute("""
            SELECT s.id, s.name, s.notes, s.website, s.service_region,
                   s.is_featured, s.country,
                   COUNT(ps.id) as product_count
            FROM suppliers s
            LEFT JOIN product_suppliers ps ON s.id = ps.supplier_id
            GROUP BY s.id
            ORDER BY s.is_featured DESC NULLS LAST, product_count DESC
        """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    suppliers = []
    for row in rows:
        s = dict(row)
        s['region_display'] = _normalise_supplier_regions(s.get('service_region'), s.get('country'))
        suppliers.append(s)
    return render_template("suppliers.html", suppliers=suppliers)


# ── Global Sashimi Rule — proximity-based supplier ranking ───────────────
# Adjacent cross-border regions as (country, region_or_None) pairs.
# Same-country tiers are handled by the country-match logic; only
# cross-border adjacencies need explicit entries here.
REGION_ADJACENCY = {
    "CA-BC": [("US", "WA"), ("US", "OR"), ("US", "AK")],
    "US-WA": [("CA", "BC")],
    "US-OR": [("CA", "BC")],
    "US-AK": [("CA", "BC")],
    "US-ID": [("CA", "BC")],
    "GB-LND": [("IE", None)],
    "GB-SCT": [("IE", None)],
    "GB-ENG": [("IE", None)],
    "AU-NSW": [("NZ", None)],
    "AU-VIC": [("NZ", None)],
    "AU-WA":  [("NZ", None)],
    "AU-QLD": [("NZ", None)],
    "AU-SA":  [("NZ", None)],
    "NZ":     [("AU", None)],
    "JP-13":  [("KR", None), ("TW", None)],
    "KR":     [("JP", None)],
    "TW":     [("JP", None)],
    "IE":     [("GB", None)],
}

# Non-ISO country codes used in the DB → ISO 3166-1 alpha-2 normalisation
_COUNTRY_NORM = {"UK": "GB"}

# City names associated with ISO sub-region codes (all lowercase).
# Used to match suppliers whose state_province is null but city is known.
_REGION_CITIES = {
    "LND": {"london"},
    "NSW": {"sydney", "alexandria", "newcastle", "wollongong"},
    "VIC": {"melbourne", "geelong"},
    "WA":  {"perth", "fremantle"},
    "QLD": {"brisbane", "gold coast"},
    "SA":  {"adelaide"},
    "BC":  {"vancouver", "victoria", "burnaby", "richmond", "surrey", "north vancouver"},
    "ON":  {"toronto", "ottawa", "mississauga"},
    "AB":  {"calgary", "edmonton"},
    "NY":  {"new york", "brooklyn", "queens", "bronx"},
    "CA":  {"san francisco", "los angeles", "san diego", "oakland", "sacramento"},
    "WA-ST": {"seattle", "tacoma", "bellevue"},  # US-WA
    "13":  {"tokyo"},
}


def _norm_country(c):
    c = (c or "").upper()
    return _COUNTRY_NORM.get(c, c)


def get_proximity_tier(s_country, s_state, s_city, s_service_regions, user_loc):
    """Return proximity tier 1–4 for a supplier vs. user location.

    1 = local/same-region   2 = same-country   3 = adjacent   4 = global

    Tier 1 rules (any of):
      • service_region explicitly names the user's region code (any supplier country)
      • supplier state_province == user region, same country
      • supplier city is a known city for the user's region, same country
    """
    if not user_loc or user_loc.upper() == "GLOBAL":
        return 4

    parts = user_loc.upper().split("-", 1)
    u_country = parts[0]                                # e.g. "CA"
    u_region  = parts[1] if len(parts) > 1 else ""     # e.g. "BC"

    sup_country = _norm_country(s_country)
    sup_state   = (s_state or "").upper()
    sup_city    = (s_city or "").lower()
    sup_regions = [r.upper() for r in (s_service_regions or [])]

    # ── Tier 1 ─────────────────────────────────────────────────────────────
    if u_region:
        # Any supplier that explicitly serves the user's region
        if u_region in sup_regions:
            return 1
        if sup_country == u_country:
            if sup_state == u_region:
                return 1
            # City-based match for suppliers with no state_province (e.g. London)
            if sup_city and sup_city in _REGION_CITIES.get(u_region, set()):
                return 1

    # ── Tier 2: same country, or explicit nationwide-<country> flag ────────
    if sup_country == u_country:
        return 2
    nationwide_key = f"NATIONWIDE_{u_country}"
    if nationwide_key in sup_regions:
        return 2

    # ── Tier 3: explicitly adjacent cross-border region ────────────────────
    for adj_country, adj_region in REGION_ADJACENCY.get(user_loc.upper(), []):
        adj_country = adj_country.upper()
        adj_region  = adj_region.upper() if adj_region else None
        if sup_country == adj_country:
            if adj_region is None:          # whole adjacent country qualifies
                return 3
            if sup_state == adj_region:
                return 3
            if adj_region in sup_regions:
                return 3

    return 4


def get_user_location():
    """Resolve requesting user's ISO region code (e.g. 'CA-BC').

    Priority: ?loc= query param (dev/test) → stored user preference →
              Accept-Language country code → 'global'
    """
    loc = request.args.get("loc", "").strip()
    if loc:
        return loc.upper()
    user = get_current_user()
    if user and user.get("user_location"):
        return str(user["user_location"]).upper()
    # Parse Accept-Language header for country code.
    # e.g. "en-CA,en-US;q=0.9,en;q=0.8" → "CA"
    al = request.headers.get("Accept-Language", "")
    for tag in _re.split(r"[,;]", al):
        tag = tag.strip().split(";")[0].strip()
        if "-" in tag:
            country = tag.split("-")[-1].upper()
            if len(country) == 2 and country.isalpha():
                return country
    return "global"


# Region codes accepted for user_location — derived from supplier data + proximity matching logic.
# Format: ISO country (+ "-" + sub-region where useful for tier-1 matching).
VALID_REGIONS = [
    ("CA-BC",  "British Columbia, Canada"),
    ("CA-AB",  "Alberta, Canada"),
    ("CA-ON",  "Ontario, Canada"),
    ("US-CA",  "California, USA"),
    ("US-WA",  "Washington, USA"),
    ("US-OR",  "Oregon, USA"),
    ("US-NY",  "New York, USA"),
    ("AU-NSW", "New South Wales, Australia"),
    ("AU-VIC", "Victoria, Australia"),
    ("AU-WA",  "Western Australia"),
    ("AU-QLD", "Queensland, Australia"),
    ("AU-SA",  "South Australia"),
    ("NZ",     "New Zealand"),
    ("GB-LND", "London, UK"),
    ("SG",     "Singapore"),
    ("FR",     "France"),
    ("JP",     "Japan"),
]
_VALID_REGION_CODES = {code for code, _ in VALID_REGIONS}


def _find_pairings_for_user_recipe(recipe_title, limit=3):
    """Return up to `limit` beverage pairings for a user kitchen recipe.

    Two-level heuristic (no LLM cost):
    1. Match title tokens against technique_references.name →
       pull rows from technique_beverage_pairings (534 curated entries).
    2. Fallback: map title keywords to food_category →
       pull published rows from pairing_intelligence (1,984 rows).
    Returns [] when nothing matches — caller handles graceful empty state.
    """
    if not recipe_title or not DATABASE_URL:
        return []

    # ── keyword → food_category map (pairing_intelligence fallback) ──────────
    KEYWORD_CATEGORY = {
        "beef": "red_meat", "steak": "red_meat", "brisket": "red_meat",
        "ribeye": "red_meat", "short rib": "red_meat",
        "lamb": "lamb", "mutton": "lamb",
        "pork": "meat", "bacon": "meat", "ham": "meat",
        "chicken": "meat_poultry", "poultry": "meat_poultry",
        "duck": "poultry", "turkey": "meat_poultry",
        "salmon": "fish", "tuna": "fish", "cod": "fish",
        "trout": "fish", "snapper": "fish", "fish": "fish",
        "crab": "shellfish", "lobster": "shellfish",
        "prawn": "shellfish", "shrimp": "shellfish",
        "scallop": "shellfish", "oyster": "shellfish",
        "mussel": "shellfish", "clam": "shellfish",
        "mushroom": "mushroom", "truffle": "fungi_truffles",
        "pasta": "pasta_grain", "risotto": "pasta_grain",
        "ravioli": "pasta_grain", "lasagna": "pasta_grain",
        "spaghetti": "pasta_grain", "linguine": "pasta_grain",
        "fettuccine": "pasta_grain", "penne": "pasta_grain",
        "tagliatelle": "pasta_grain", "pappardelle": "pasta_grain",
        "gnocchi": "pasta_grain", "noodle": "noodles",
        "chocolate": "chocolate", "cocoa": "chocolate",
        "cheese": "cheese", "gruyere": "cheese",
        "dessert": "dessert", "cake": "dessert",
        "tart": "dessert", "pudding": "dessert",
        "lentil": "vegetables_legumes", "bean": "vegetables_legumes",
        "legume": "vegetables_legumes", "chickpea": "vegetables_legumes",
        "vegetable": "vegetables", "salad": "salad",
        "soup": "vegetables", "charcuterie": "charcuterie",
        "venison": "game", "rabbit": "game",
        "rice": "grain", "grain": "grain",
    }

    title_lower = recipe_title.lower()

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # ── Level 1: technique name match → technique_beverage_pairings ──────
        STOPWORDS = {
            "the", "a", "an", "and", "or", "with", "of", "for", "in", "on",
            "recipe", "easy", "simple", "classic", "homemade", "quick", "best",
        }
        tokens = [t.strip(",.()[]'\"—-&").lower() for t in recipe_title.split() if len(t) >= 4]
        tokens = [t for t in tokens if t not in STOPWORDS]

        # Only use significant tokens (5+ chars, not generic cooking words) for
        # Level 1 to avoid "soup" matching "French Onion Soup" for unrelated recipes.
        GENERIC_COOKING = {
            "soup", "salad", "dish", "food", "meal", "plate", "baked", "fried",
            "roast", "braise", "grill", "steam", "sauce", "spice", "herbs",
            "herb", "style", "style", "saute", "stew", "boil", "blend",
        }
        significant_tokens = [t for t in tokens if len(t) >= 5 and t not in GENERIC_COOKING]

        if significant_tokens:
            conditions = " OR ".join(["LOWER(tr.name) LIKE %s"] * len(significant_tokens))
            params = [f"%{t}%" for t in significant_tokens]
            cur.execute(f"""
                SELECT tr.id AS technique_id, tr.name AS technique_name,
                       tbp.pairing_type, tbp.beverage_category, tbp.pairing_rationale,
                       tbp.confidence_status,
                       bp.name AS product_name,
                       bprod.name AS producer_name
                FROM technique_references tr
                JOIN technique_beverage_pairings tbp ON tbp.technique_id = tr.id
                LEFT JOIN beverage_products bp ON bp.id = tbp.beverage_product_id
                     AND bp.is_published IS TRUE
                LEFT JOIN beverage_producers bprod ON bprod.id = tbp.beverage_producer_id
                     AND bprod.is_published IS TRUE
                WHERE tbp.confidence_status IN ('editorial', 'reviewed')
                  AND (tbp.beverage_producer_id IS NULL OR bprod.id IS NOT NULL)
                  AND (tbp.beverage_product_id IS NULL OR bp.id IS NOT NULL)
                  AND ({conditions})
                ORDER BY tr.id DESC,
                         CASE tbp.confidence_status
                           WHEN 'editorial' THEN 1
                           WHEN 'reviewed' THEN 2
                           ELSE 3
                         END,
                         tbp.display_order
                LIMIT %s
            """, params + [limit])
            rows = cur.fetchall()
            if rows:
                results = []
                for r in rows:
                    _name = r["product_name"] or r["producer_name"] or ""
                    results.append({
                        "beverage_category": r["beverage_category"] or "",
                        "beverage_style": _name,
                        "beverage_name": _name,
                        "beverage_description": r["pairing_rationale"] or "",
                        "flavour_logic": "",
                        "confidence": r["confidence_status"] or "partial",
                        "pairing_type": r["pairing_type"] or "",
                        "source": "technique_match",
                        "matched_on": r["technique_name"],
                        "beverage_product_id": None,
                        "pantry_url": None,
                    })
                return results

        # ── Level 2: keyword → food_category → pairing_intelligence ──────────
        matched_category = None
        for kw, cat in KEYWORD_CATEGORY.items():
            if kw in title_lower:
                matched_category = cat
                break

        if not matched_category:
            return []

        cur.execute("""
            SELECT pi.beverage_category, pi.beverage_style, pi.beverage_description,
                   pi.flavour_logic, pi.confidence, pi.pairing_type, pi.food_category,
                   pi.beverage_product_id,
                   bp.name AS bp_name, bp.slug AS bp_slug
            FROM pairing_intelligence pi
            LEFT JOIN beverage_products bp ON bp.id = pi.beverage_product_id AND bp.is_published IS TRUE
            WHERE pi.is_published = TRUE
              AND pi.food_category = %s
              AND pi.beverage_category IS NOT NULL
            ORDER BY CASE pi.confidence
                       WHEN 'classic'     THEN 1
                       WHEN 'established' THEN 2
                       WHEN 'suggested'   THEN 3
                       ELSE 4
                     END
            LIMIT %s
        """, (matched_category, limit))
        rows = cur.fetchall()
        results = []
        for r in rows:
            bp_id = r["beverage_product_id"]
            results.append({
                "beverage_category": r["beverage_category"] or "",
                "beverage_style": r["beverage_style"] or "",
                "beverage_name": r["bp_name"] or r["beverage_style"] or "",
                "beverage_description": r["beverage_description"] or "",
                "flavour_logic": r["flavour_logic"] or "",
                "confidence": r["confidence"] or "",
                "pairing_type": r["pairing_type"] or "",
                "source": "category_match",
                "matched_on": r["food_category"],
                "beverage_product_id": bp_id,
                "pantry_url": f"/beverage/products/{bp_id}" if bp_id else None,
            })
        if results:
            return results

        # ── Level 3 (founder ruling 2.1): the cellar's deduction — the block
        # never renders empty while the 534 await sign-off. Structure derived
        # from the recipe title's own words; honestly labeled downstream.
        try:
            axes, aromatics = _dish_axes_from_text(recipe_title, recipe_title)
            if any(axes.get(k) for k in ("fat", "salt", "acid", "sweet", "smoke", "heat")) or aromatics:
                dish = {"name": recipe_title, "axes": axes, "aromatics": aromatics}
                picks = _grammar_resolve(dish, get_user_location(), limit=3)
                return [{
                    "beverage_category": pk["product"].get("category") or "",
                    "beverage_style": "",
                    "beverage_name": pk["product"]["name"] + (f" — {pk['expression']}" if pk.get("expression") else ""),
                    "name": pk["product"]["name"] + (f" — {pk['expression']}" if pk.get("expression") else ""),
                    "region": pk["product"].get("region_name") or "",
                    "beverage_description": pk["why"],
                    "why": pk["why"],
                    "flavour_logic": "",
                    "confidence": "deduction",
                    "pairing_type": pk["move"],
                    "relationship_type": pk["move"],
                    "source": "cellar_deduction",
                    "matched_on": recipe_title,
                    "carried": pk["carried"],
                    "beverage_product_id": None if pk.get("is_preparation") else pk["product"]["id"],
                    "pantry_url": (None if pk.get("is_preparation")
                                   else f"/beverage/products/{pk['product']['id']}"),
                } for pk in picks]
        except Exception as _de:
            app.logger.warning(f"recipe pairing deduction failed: {_de}")
        return []

    except Exception:
        return []
    finally:
        cur.close()
        conn.close()


def _suggested_beverages_for_recipe(recipe_name, cur, limit=4):
    """Return beverage product suggestions for a recipe by matching its name to technique names."""
    if not recipe_name:
        return []
    STOPWORDS = {"the", "a", "an", "and", "or", "with", "of", "for", "in", "on",
                 "recipe", "easy", "simple", "classic", "homemade", "quick", "best"}
    tokens = [t.strip(",.()[]'\"—–-&").lower() for t in recipe_name.split()]
    tokens = [t for t in tokens if len(t) >= 4 and t not in STOPWORDS]
    if not tokens:
        return []
    conditions = " OR ".join(["LOWER(tr.name) LIKE %s"] * len(tokens))
    params = [f"%{t}%" for t in tokens] + [limit]
    cur.execute(f"""
        SELECT DISTINCT
            bp.id,
            bp.name,
            br.name AS region,
            bpr.name AS origin_producer,
            tbp.pairing_type AS relationship_type
        FROM technique_references tr
        JOIN technique_beverage_pairings tbp ON tbp.technique_id = tr.id
        JOIN beverage_products bp ON bp.id = tbp.beverage_product_id AND bp.is_published IS TRUE
        LEFT JOIN beverage_regions br ON br.id = bp.region_id
        LEFT JOIN beverage_producers bpr ON bpr.id = bp.producer_id
             AND bpr.is_published IS TRUE
        WHERE {conditions}
        ORDER BY bp.name ASC
        LIMIT %s
    """, params)
    return [dict(r) for r in cur.fetchall()]


def _recipes_using_beverage(beverage_id, cur, limit=6):
    """Return recipes whose names match techniques that pair with this beverage."""
    cur.execute("""
        SELECT DISTINCT
            r.id,
            r.slug,
            r.name,
            r.cuisine AS origin,
            tbp.pairing_type AS relationship_type
        FROM technique_beverage_pairings tbp
        JOIN technique_references tr ON tr.id = tbp.technique_id
        JOIN recipes r ON (
            LOWER(r.name) LIKE '%%' || LOWER(tr.name) || '%%'
            OR LOWER(tr.name) LIKE '%%' || LOWER(r.name) || '%%'
        )
        WHERE tbp.beverage_product_id = %s
        ORDER BY r.name ASC
        LIMIT %s
    """, (beverage_id, limit))
    return [dict(r) for r in cur.fetchall()]


# ── v3 recipe card JSON-LD helpers ────────────────────────────────────────────

def _build_v3_recipe_jsonld(d):
    instructions = []
    for s in d.get("method_steps", []):
        clean = _re.sub(r"<[^>]+>", "", s.get("body", ""))
        instructions.append({"@type": "HowToStep", "name": s.get("title", ""), "text": clean})
    cuisine = d.get("cuisine", "")
    if d.get("region"):
        cuisine = f"{cuisine} · {d['region']}"
    tradition_tags = d.get("tradition_tags", [])
    # Strip HTML entities for keywords
    keywords = d.get("keywords", ", ".join(_re.sub(r"&[a-z]+;", "&", t) for t in tradition_tags))
    schema = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": d.get("title", ""),
        "image": [f"https://provenance.kitchen/og/{d.get('url_slug', '')}.jpg"],
        "description": d.get("meta_description", ""),
        "recipeCategory": d.get("recipe_category", "Main course"),
        "recipeCuisine": cuisine,
        "keywords": keywords,
        "recipeYield": f"{d.get('yield_default', '')} {d.get('yield_unit', '')}",
        "prepTime": d.get("iso_prep_time", ""),
        "cookTime": d.get("iso_cook_time", ""),
        "totalTime": d.get("iso_total_time", ""),
        "datePublished": "2026-05-07",
        "isAccessibleForFree": True,
        "author": {
            "@type": "Person",
            "name": "Chef Garth Greenlees",
            "url": "https://provenance.kitchen/chef/garth-greenlees",
            "jobTitle": "Editor, Provenance Culinary Intelligence",
        },
        "publisher": {
            "@type": "Organization",
            "name": "Provenance",
            "url": "https://provenance.kitchen",
            "logo": {"@type": "ImageObject", "url": "https://provenance.kitchen/logo.png"},
        },
        "recipeIngredient": [
            f"{item.get('amount', '')} {item.get('name', '')}" + (f" — {item.get('prep', '')}" if item.get("prep") else "")
            for grp in d.get("ingredient_groups", [])
            for item in grp.get("items", [])
        ],
        "recipeInstructions": instructions,
        "tool": d.get("equipment", []),
    }
    if d.get("citation"):
        schema["citation"] = d["citation"]
    return schema


def _build_v3_faq_jsonld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f.get("q", ""),
                "acceptedAnswer": {"@type": "Answer", "text": f.get("a", "")},
            }
            for f in faqs
        ],
    }


def _build_v3_breadcrumb_jsonld(d):
    items = [
        {"@type": "ListItem", "position": 1, "name": "Provenance", "item": "https://provenance.kitchen"},
        {"@type": "ListItem", "position": 2, "name": "Cuisines", "item": "https://provenance.kitchen/cuisines"},
    ]
    pos = 3
    for crumb in d.get("canon_path", []):
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": crumb,
            "item": f"https://provenance.kitchen/cuisines/{crumb.lower().replace(' ', '-')}",
        })
        pos += 1
    items.append({"@type": "ListItem", "position": pos, "name": d.get("title", "")})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


@app.route("/recipe/<slug>")
def recipe_page(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recipes WHERE slug = %s", (slug,))
    recipe = cur.fetchone()
    if not recipe:
        # Check user kitchen recipes
        cur.execute("SELECT * FROM user_kitchen_recipes WHERE slug = %s", (slug,))
        kitchen_recipe = cur.fetchone()
        if kitchen_recipe:
            user = get_current_user()
            if not user or user.get("id") != kitchen_recipe.get("user_id"):
                cur.close(); conn.close()
                abort(404)
            # Normalize yield text before anything else
            _row = dict(kitchen_recipe)
            _st = (_row.get("servings_text") or "").rstrip()
            for _bad in (" serves", " serve"):
                if _st.endswith(_bad):
                    _row["servings_text"] = _st[:-len(_bad)].rstrip() + " servings"
                    break
            if not _row.get("servings_text") and _row.get("servings"):
                _norm_yield, _ = _parse_yield(_row["servings"])
                if _norm_yield:
                    _row["servings_text"] = _norm_yield
            _recipe_dict = _normalize_member_recipe(_row)
            _recipe_dict["requires_haccp"] = _detect_raw_served(*_recipe_dict_to_haccp_inputs(_recipe_dict))
            # Pairings — stored JSONB first, then LLM-derived fallback
            _stored_pairings = kitchen_recipe.get("beverage_pairings")
            _pairings = _stored_pairings if _stored_pairings else _find_pairings_for_user_recipe(kitchen_recipe.get("title", ""))
            _sourced = _get_kitchen_recipe_suppliers_from_markers(kitchen_recipe, get_user_location())
            _region = get_user_location() or "CA"
            cur.close()
            conn.close()
            # Deduplicate: a supplier with both ORIGIN and PROVIDER rows in product_suppliers
            # can appear in both lists. Origin classification wins (appears first).
            _seen_sids = set()
            _deduped_suppliers = []
            for _sup in _sourced["origin"] + _sourced["providers"]:
                if _sup.get("id") not in _seen_sids:
                    _seen_sids.add(_sup.get("id"))
                    _deduped_suppliers.append(_sup)
            return render_template(
                "recipe.html",
                recipe=_recipe_dict,
                pairings=_pairings,
                recipe_suppliers=_deduped_suppliers,
                allergens=[],
                haccp_brief=None,
                cost_breakdown=None,
                region=_region,
                format_cuisine=_format_cuisine,
                is_owner=bool(user and user.get("id") == kitchen_recipe.get("user_id")),
            )
        cur.close()
        conn.close()
        abort(404)

    # Find suppliers linked to this recipe's ingredients.
    # Forward ILIKE only: product name contains the ingredient token.
    # The reverse arm ("ingredient contains product name") is dropped — it was the
    # primary source of false positives (e.g. product "Tomato" matching "tomato paste").
    # Form-mismatch disqualifier: if the matched product carries a specificity word
    # (paste, powder, aged, dried, smoked, fermented) that the recipe ingredient
    # doesn't, the match is discarded.
    # Confidence: the ingredient token must cover ≥60% of the shorter of the two names.
    recipe_suppliers = []
    user_loc = get_user_location()
    try:
        ingredients = recipe.get("ingredients") or []
        ingredient_names = [ing.get("name", "") for ing in ingredients if ing.get("name")]
        if ingredient_names:
            patterns = [f"%{n}%" for n in ingredient_names[:20]]
            cur.execute("""
                SELECT DISTINCT ON (s.id, ip.name)
                    s.id, s.name, s.website, s.city, s.state_province, s.country,
                    s.service_region,
                    ip.name AS product_name,
                    LEFT(ip.description, 140) AS product_desc
                FROM ingredient_products ip
                JOIN product_suppliers ps ON ip.id = ps.product_id
                JOIN suppliers s ON ps.supplier_id = s.id
                WHERE ip.name ILIKE ANY(%s)
                ORDER BY s.id, ip.name, s.name
            """, (patterns,))
            rows = cur.fetchall()

            _FORM_WORDS = {"paste", "powder", "aged", "dried", "smoked", "fermented"}

            def _match_ok(ing, prod):
                il, pl = ing.lower(), prod.lower()
                for fw in _FORM_WORDS:
                    if fw in pl and fw not in il:
                        return False
                shorter = min(len(il), len(pl))
                return shorter > 0 and len(il) / shorter >= 0.6

            supplier_map = {}
            for row in rows:
                prod_name = row['product_name'] or ''
                if not any(_match_ok(ing, prod_name) for ing in ingredient_names):
                    continue
                sid = row['id']
                if sid not in supplier_map:
                    supplier_map[sid] = {
                        'id': sid, 'name': row['name'], 'website': row['website'],
                        'city': row['city'], 'state_province': row['state_province'],
                        'country': row['country'],
                        'service_region': list(row['service_region'] or []),
                        'products': []
                    }
                if prod_name:
                    supplier_map[sid]['products'].append({
                        'name': prod_name,
                        'desc': row['product_desc'] or ''
                    })
            # Deduplicate products within each supplier (DB may have duplicate entries)
            for sup in supplier_map.values():
                seen_products = set()
                deduped = []
                for p in sup['products']:
                    key = p['name'].lower()
                    if key not in seen_products:
                        seen_products.add(key)
                        deduped.append(p)
                sup['products'] = deduped
            # Assign proximity tier then sort (tier ASC, name ASC)
            for sup in supplier_map.values():
                sup['tier'] = get_proximity_tier(
                    sup['country'], sup['state_province'], sup['city'],
                    sup['service_region'], user_loc
                )
            recipe_suppliers = sorted(
                supplier_map.values(),
                key=lambda s: (s['tier'], s['name'].lower())
            )
    except Exception:
        recipe_suppliers = []

    suggested_beverages = []
    try:
        suggested_beverages = _suggested_beverages_for_recipe(recipe.get('name', ''), cur)
    except Exception as e:
        app.logger.warning(f"beverage suggestion failed for recipe {recipe.get('id')}: {e}")

    cur.close()
    conn.close()
    _region = user_loc or "CA"
    _user = get_current_user()
    _pub_recipe = dict(recipe)
    _pub_recipe["requires_haccp"] = _detect_raw_served(*_recipe_dict_to_haccp_inputs(_pub_recipe))
    return render_template(
        "recipe.html",
        recipe=_pub_recipe,
        recipe_suppliers=recipe_suppliers,
        suggested_beverages=suggested_beverages,
        user_location=user_loc,
        pairings=suggested_beverages,
        allergens=_get_allergens_for_region(recipe, _region),
        haccp_brief=_get_or_build_haccp_brief(recipe, _region),
        cost_breakdown=_compute_recipe_cost(recipe, _region),
        region=_region,
        format_cuisine=_format_cuisine,
        is_owner=bool(_user and recipe.get("user_id") and _user.get("id") == recipe.get("user_id")),
    )


@app.route("/recipe/<slug>/cook")
def recipe_cook_mode(slug):
    """Cook mode — phone-first minimal view with Wake Lock for on-the-line use."""
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Kitchen recipes take priority (user-imported, Cook button lives on that page)
    cur.execute("SELECT * FROM user_kitchen_recipes WHERE slug = %s", (slug,))
    kitchen_recipe = cur.fetchone()
    if kitchen_recipe:
        _cook_user = get_current_user()
        if not _cook_user or _cook_user.get("id") != kitchen_recipe.get("user_id"):
            cur.close(); conn.close()
            abort(404)
        cur.close()
        conn.close()
        _recipe_dict = dict(kitchen_recipe)
        # Normalize yield text — same logic as recipe_page
        _st = (_recipe_dict.get("servings_text") or "").rstrip()
        for _bad in (" serves", " serve"):
            if _st.endswith(_bad):
                _recipe_dict["servings_text"] = _st[:-len(_bad)].rstrip() + " servings"
                break
        if not _recipe_dict.get("servings_text") and _recipe_dict.get("servings"):
            _norm, _ = _parse_yield(_recipe_dict["servings"])
            if _norm:
                _recipe_dict["servings_text"] = _norm
        # Prefer enhanced_steps when available — normalize to {instruction, insight} shape
        # so the template accessor (step.instruction) works for both data sources.
        _enhanced = _recipe_dict.get("enhanced_steps")
        if _enhanced and isinstance(_enhanced, list) and len(_enhanced) > 0:
            _recipe_dict["steps"] = [
                {"instruction": s.get("enhanced_step", ""), "insight": s.get("insight", ""), "timer_seconds": s.get("timer_seconds")}
                if isinstance(s, dict) else {"instruction": str(s), "insight": "", "timer_seconds": None}
                for s in _enhanced
            ]
        _recipe_dict["requires_haccp"] = _detect_raw_served(*_recipe_dict_to_haccp_inputs(_recipe_dict))
        return render_template("cook_mode.html", recipe=_recipe_dict)
    # Fall back to public recipes table
    cur.execute("SELECT * FROM recipes WHERE slug = %s", (slug,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if not recipe:
        abort(404)
    _canon_recipe = dict(recipe)
    _canon_recipe["requires_haccp"] = _detect_raw_served(*_recipe_dict_to_haccp_inputs(_canon_recipe))
    return render_template("cook_mode.html", recipe=_canon_recipe)


@app.route("/suggest-supplier", methods=["GET"])
def suggest_supplier_form():
    """Render the supplier suggestion form. Optional ?recipe=<slug> for context."""
    recipe_slug = request.args.get("recipe", "")
    recipe_title = ""
    if recipe_slug and DATABASE_URL:
        try:
            user = get_current_user()
            if user and user.get("id"):
                conn = get_db()
                cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cur.execute(
                    "SELECT title FROM user_kitchen_recipes WHERE slug = %s AND user_id = %s",
                    (recipe_slug, user["id"]),
                )
                row = cur.fetchone()
                if row:
                    recipe_title = row["title"]
                cur.close()
                conn.close()
        except Exception:
            pass
    return render_template("suggest_supplier.html", recipe_slug=recipe_slug, recipe_title=recipe_title)


@app.route("/suggest-supplier", methods=["POST"])
def suggest_supplier_submit():
    """Process supplier suggestion and email Garth."""
    supplier_name = (request.form.get("supplier_name") or "").strip()
    supplier_website = (request.form.get("supplier_website") or "").strip()
    what_they_make = (request.form.get("what_they_make") or "").strip()
    chef_name = (request.form.get("chef_name") or "").strip()
    chef_email = (request.form.get("chef_email") or "").strip()
    recipe_slug = (request.form.get("recipe_slug") or "").strip()

    if not supplier_name:
        return render_template(
            "suggest_supplier.html",
            error="Supplier name is required.",
            recipe_slug=recipe_slug,
            recipe_title="",
        ), 400

    try:
        from email_service import send_supplier_suggestion_email
        send_supplier_suggestion_email({
            "supplier_name": supplier_name,
            "supplier_website": supplier_website,
            "what_they_make": what_they_make,
            "chef_name": chef_name,
            "chef_email": chef_email,
            "recipe_slug": recipe_slug,
        })
    except Exception as e:
        app.logger.warning(f"[suggest_supplier_submit] email failed: {e}")
        app.logger.info(
            f"[suggest_supplier_submit] Supplier={supplier_name!r} "
            f"Website={supplier_website!r} WhatTheyMake={what_they_make!r} "
            f"Name={chef_name!r} Email={chef_email!r} Recipe={recipe_slug!r}"
        )

    return render_template(
        "suggest_supplier_thanks.html",
        supplier_name=supplier_name,
        recipe_slug=recipe_slug,
    )


@app.route("/api/recipe/<slug>/re-enrich-pairings", methods=["POST"])
def re_enrich_pairings(slug):
    """Re-run LLM beverage pairing enrichment for a kitchen recipe. Founder/admin only."""
    user = get_current_user()
    if not user or user.get("role") not in ("founder", "admin"):
        return jsonify({"error": "forbidden"}), 403
    if not DATABASE_URL_WRITE:
        return jsonify({"error": "no write DB"}), 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM user_kitchen_recipes WHERE slug = %s", (slug,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if not recipe:
        return jsonify({"error": "recipe not found"}), 404
    _ing_lines = "\n".join(
        f"{i.get('count', '')} {i.get('unit', '')} {i.get('name', '')}".strip()
        for i in (recipe.get("ingredients") or [])
        if isinstance(i, dict)
    )
    pairings = _enrich_beverage_pairings(recipe["title"], _ing_lines)
    if not pairings:
        return jsonify({"error": "enrichment returned nothing"}), 500
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE user_kitchen_recipes SET beverage_pairings = %s WHERE slug = %s",
        (json.dumps(pairings), slug),
    )
    cur.close()
    conn.close()
    return jsonify({"ok": True, "slug": slug, "pairings": pairings})


@app.route("/api/recipe/<slug>/edit", methods=["POST"])
def recipe_v3_edit(slug):
    """Update editable fields on a v3 user kitchen recipe."""
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    if not DATABASE_URL_WRITE:
        return jsonify({"success": False, "error": "Database not configured"}), 503

    conn = psycopg2.connect(DATABASE_URL_WRITE)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            "SELECT id, user_id, recipe_content_jsonb FROM user_kitchen_recipes WHERE slug = %s",
            (slug,)
        )
        row = cur.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Recipe not found"}), 404
        if row["user_id"] != user["id"]:
            return jsonify({"success": False, "error": "Forbidden"}), 403

        content = dict(row["recipe_content_jsonb"] or {})

        # Text fields
        for field in ("title", "subtitle", "notes_placeholder"):
            val = request.form.get(field)
            if val is not None:
                content[field] = val.strip()

        for field in ("source_attribution", "sashimi"):
            val = request.form.get(field)
            if val is not None:
                content[field] = val

        # Hero image — file upload takes priority over URL
        hero_file = request.files.get("hero_image_file")
        hero_url = (request.form.get("hero_image_url") or "").strip()

        if hero_file and hero_file.filename:
            import time
            ext = os.path.splitext(hero_file.filename)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".webp"):
                return jsonify({"success": False, "error": "Unsupported image format"}), 400
            if hero_file.content_length and hero_file.content_length > 5 * 1024 * 1024:
                return jsonify({"success": False, "error": "Image too large (max 5 MB)"}), 400
            upload_dir = os.path.join("static", "uploads", "recipes", str(user["id"]))
            os.makedirs(upload_dir, exist_ok=True)
            ts = int(time.time())
            filename = f"{slug}-hero-{ts}{ext}"
            save_path = os.path.join(upload_dir, filename)
            hero_file.save(save_path)
            content["hero_image"] = f"/static/uploads/recipes/{user['id']}/{filename}"
        elif hero_url and hero_url.startswith("https://"):
            content["hero_image"] = hero_url

        cur.execute(
            "UPDATE user_kitchen_recipes SET recipe_content_jsonb = %s WHERE id = %s",
            (json.dumps(content), row["id"])
        )
        return jsonify({"success": True, "redirect": f"/recipe/{slug}"})
    except Exception as e:
        app.logger.error(f"recipe_v3_edit error for {slug}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/api/curated-recipes")
def curated_recipes():
    """Return curated catalog recipes + user kitchen recipes."""
    if not DATABASE_URL:
        return jsonify({"recipes": []}), 200
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, slug, cuisine, description, image_url, recipe_type, is_curated
        FROM recipes ORDER BY is_curated DESC, id ASC
    """)
    catalog = [dict(r) for r in cur.fetchall()]
    # Also include user kitchen recipes (prepended — user's own recipes shown first)
    user_recipes = []
    try:
        cur.execute("""
            SELECT uuid, title, slug, preamble,
                   CASE WHEN jsonb_array_length(COALESCE(tags,'[]'::jsonb)) > 0
                        THEN tags->>0 ELSE NULL END AS cuisine,
                   CASE WHEN has_image
                        THEN '/images/' || uuid || '/miniature.jpg' ELSE NULL END AS image_url
            FROM user_kitchen_recipes
            WHERE is_draft = FALSE
            ORDER BY created_at DESC
        """)
        for r in cur.fetchall():
            user_recipes.append({
                "id": r["uuid"],
                "name": r["title"],
                "slug": r["slug"],
                "cuisine": r["cuisine"],
                "description": r["preamble"] or "",
                "image_url": r["image_url"],
                "recipe_type": "user_kitchen",
                "is_curated": False,
            })
    except Exception as e:
        app.logger.warning(f"[curated-recipes] user_kitchen_recipes query failed: {e}")
    cur.close()
    conn.close()
    return jsonify({"recipes": user_recipes + catalog})


@app.route("/api/recipe/submit-for-review", methods=["POST"])
def submit_recipe_for_review():
    """Submit a user kitchen recipe for editorial review."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    if not DATABASE_URL_WRITE:
        return jsonify({"error": "Database not configured"}), 503

    data = request.get_json() or {}
    recipe_id = data.get("recipe_id")
    if not recipe_id:
        return jsonify({"error": "recipe_id required"}), 400

    # Verify recipe exists and belongs to this user
    try:
        rconn = psycopg2.connect(DATABASE_URL)
        rconn.autocommit = True
        rcur = rconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        rcur.execute("SELECT * FROM user_kitchen_recipes WHERE uuid = %s", (recipe_id,))
        recipe = rcur.fetchone()
        if not recipe or recipe["user_id"] != user["id"]:
            rcur.close(); rconn.close()
            return jsonify({"error": "Recipe not found"}), 404
        # Check for existing pending submission
        rcur.execute(
            "SELECT id FROM recipe_submissions WHERE user_kitchen_recipe_id = %s AND status = 'pending' LIMIT 1",
            (recipe_id,)
        )
        existing = rcur.fetchone()
        rcur.close(); rconn.close()
    except Exception as exc:
        app.logger.error("submit-for-review DB read error: %s", exc)
        return jsonify({"error": "Database error"}), 500

    if existing:
        return jsonify({"error": "Already submitted for review"}), 409

    # Insert submission
    try:
        wconn = psycopg2.connect(DATABASE_URL_WRITE)
        wconn.autocommit = True
        wcur = wconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        wcur.execute(
            "INSERT INTO recipe_submissions (user_kitchen_recipe_id, submitted_by_user_id) VALUES (%s, %s) RETURNING id, submitted_at, status",
            (recipe_id, user["id"])
        )
        submission = wcur.fetchone()
        wcur.close(); wconn.close()
    except Exception as exc:
        app.logger.error("submit-for-review DB write error: %s", exc)
        return jsonify({"error": "Could not save submission"}), 500

    submission_id = str(submission["id"])
    submitted_at = submission["submitted_at"]

    # Build email data
    recipe_dict = dict(recipe)
    steps = recipe_dict.get("enhanced_steps") or recipe_dict.get("steps") or []
    if isinstance(steps, str):
        try: steps = json.loads(steps)
        except Exception: steps = []
    steps_with_notes = sum(1 for s in steps if isinstance(s, dict) and s.get("insight"))

    quality_warnings = recipe_dict.get("quality_warnings") or []
    if isinstance(quality_warnings, str):
        try: quality_warnings = json.loads(quality_warnings)
        except Exception: quality_warnings = []

    origin_markers = recipe_dict.get("ingredient_origin_markers") or []
    if isinstance(origin_markers, str):
        try: origin_markers = json.loads(origin_markers)
        except Exception: origin_markers = []
    producers, products, supplier_names = set(), set(), set()
    for m in origin_markers:
        for s in (m.get("suppliers") or []):
            if s.get("name"): supplier_names.add(s["name"])
        if m.get("product_name"): products.add(m["product_name"])
        if m.get("origin"): producers.add(m["origin"])

    tags = recipe_dict.get("tags") or []
    if isinstance(tags, str):
        try: tags = json.loads(tags)
        except Exception: tags = []

    at_fmt = submitted_at.strftime("%Y-%m-%d %H:%M UTC") if hasattr(submitted_at, "strftime") else str(submitted_at)
    chef_name = user.get("display_name") or user["email"].split("@")[0]

    email_data = {
        "recipe_title": recipe_dict.get("title", recipe_id),
        "chef_name": chef_name,
        "chef_email": user["email"],
        "submitted_at": at_fmt,
        "slug": recipe_dict.get("slug", ""),
        "yield_text": recipe_dict.get("servings_text") or str(recipe_dict.get("servings_count") or ""),
        "active_time": recipe_dict.get("time_active") or "not set",
        "total_time": recipe_dict.get("time_total") or "not set",
        "tags": ", ".join(tags) if tags else "none",
        "sashimi_line": recipe_dict.get("lives_or_dies") or "",
        "audit_issue_count": len(quality_warnings),
        "audit_issues": [w.get("title", str(w)) if isinstance(w, dict) else str(w) for w in quality_warnings],
        "producer_count": len(producers),
        "product_count": len(products),
        "supplier_names": ", ".join(filter(None, supplier_names)) or "none",
        "step_count": len(steps),
        "steps_with_notes": steps_with_notes,
        "submission_id": submission_id,
    }

    editorial_email = os.environ.get("EDITORIAL_REVIEW_EMAIL")
    if editorial_email:
        from email_service import send_editorial_review_email
        try:
            send_editorial_review_email(editorial_email, email_data)
        except Exception as exc:
            app.logger.error("Editorial review email failed for submission %s: %s", submission_id, exc)
    else:
        app.logger.warning("EDITORIAL_REVIEW_EMAIL not set — submission %s recorded but not emailed", submission_id)

    return jsonify({
        "submission_id": submission_id,
        "status": "pending",
        "submitted_at": submitted_at.isoformat() if hasattr(submitted_at, "isoformat") else str(submitted_at),
    })


@app.route("/api/kitchen/recipes")
def kitchen_recipes():
    """Return recipes for the My Kitchen page (DB + file-based, merged)."""
    recipes_out = []

    # 1. DB recipes
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("""
                SELECT id, name, slug, cuisine, cuisine_canon, recipe_type,
                       image_url, description, tradition_tags, pairings,
                       last_cooked_at, cook_count, is_curated, user_id,
                       ingredients, created_at
                FROM recipes
                WHERE slug IS NOT NULL AND slug != ''
                ORDER BY is_curated DESC, id DESC
                LIMIT 200
            """)
            for r in cur.fetchall():
                row = dict(r)
                # Build primary_ingredients from ingredients JSONB
                ings = row.get("ingredients") or []
                if isinstance(ings, str):
                    try:
                        ings = json.loads(ings)
                    except Exception:
                        ings = []
                pi = []
                for ing in (ings[:5] if isinstance(ings, list) else []):
                    if isinstance(ing, dict):
                        pi.append(ing.get("name") or "")
                    elif isinstance(ing, str):
                        pi.append(ing)
                recipes_out.append({
                    "id": row["id"],
                    "slug": row["slug"],
                    "title": row["name"] or "",
                    "recipe_type": row["recipe_type"] or "food",
                    "hero_image_url": row["image_url"] or "",
                    "cuisine_canon": row["cuisine_canon"] or row["cuisine"] or "",
                    "cuisine": row["cuisine"] or "",
                    "primary_ingredients": [p for p in pi if p],
                    "has_pairing": bool(row.get("pairings") and row["pairings"] != "[]"),
                    "source_type": "curated" if row["is_curated"] else "url_import",
                    "last_cooked_at": row["last_cooked_at"].isoformat() if row.get("last_cooked_at") else None,
                    "cook_count": row.get("cook_count") or 0,
                    "_source": "db",
                })
            cur.close()
            conn.close()
        except Exception:
            pass

    # 2. File-based recipes (recipes.json) — uuid-based
    try:
        file_recipes = load_recipes()
        for r in file_recipes:
            slug = r.get("slug") or r.get("uuid")
            if not slug:
                continue
            title = r.get("title") or r.get("name") or "Untitled"
            tags = r.get("tags") or []
            ings = r.get("ingredients") or []
            pi = []
            for ing in (ings[:5] if isinstance(ings, list) else []):
                if isinstance(ing, dict):
                    pi.append(ing.get("name") or "")
                elif isinstance(ing, str):
                    pi.append(ing)
            source_type = "url_import"
            if r.get("hasImage") and not r.get("source", {}).get("address", "").startswith("http"):
                source_type = "photographed"
            elif any(t in tags for t in ("conceived", "ai")):
                source_type = "conceived"
            recipes_out.append({
                "id": None,
                "slug": slug,
                "title": title,
                "recipe_type": "cocktail" if any(t in tags for t in ("cocktail", "drink", "beverage")) else "food",
                "hero_image_url": f"/images/{r['uuid']}/main.jpg" if r.get("uuid") and r.get("hasImage") else "",
                "cuisine_canon": (tags[0] if tags else ""),
                "cuisine": (tags[0] if tags else ""),
                "primary_ingredients": [p for p in pi if p],
                "has_pairing": False,
                "source_type": source_type,
                "last_cooked_at": r.get("cooking", {}).get("last") or None,
                "cook_count": int(r.get("cooking", {}).get("times") or 0),
                "_source": "file",
            })
    except Exception:
        pass

    return jsonify({"recipes": recipes_out, "total": len(recipes_out)})


@app.route("/api/kitchen/marker-read", methods=["POST"])
def kitchen_marker_read():
    """Record that a user has opened a gold-star marker."""
    user = get_current_user()
    if not user or not DATABASE_URL_WRITE:
        return jsonify({"ok": False}), 401
    data = request.get_json() or {}
    slug = data.get("slug")
    idx = data.get("marker_index")
    if not slug or idx is None:
        return jsonify({"ok": False}), 400
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_recipe_markers_read (user_id, recipe_slug, marker_index)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, recipe_slug, marker_index) DO NOTHING
        """, (user["id"], slug, int(idx)))
        cur.close()
        conn.close()
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/kitchen/markers-read/<slug>")
def kitchen_markers_read(slug):
    """Return set of marker indices the current user has read for a recipe."""
    user = get_current_user()
    if not user or not DATABASE_URL:
        return jsonify({"read": []})
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT marker_index FROM user_recipe_markers_read WHERE user_id = %s AND recipe_slug = %s",
            (user["id"], slug)
        )
        indices = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify({"read": indices})
    except Exception:
        return jsonify({"read": []})


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
    """Serve user's personal kitchen recipes. DB is source of truth; flat file is fallback."""
    if DATABASE_URL:
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("""
                SELECT uuid, title, preamble, tags, ingredients, steps,
                       original_steps, enhanced_steps, time_active, time_total,
                       servings, source_name, source_url, has_image, is_draft
                FROM user_kitchen_recipes
                ORDER BY created_at ASC
            """)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            recipes = []
            for r in rows:
                recipes.append({
                    "uuid": r["uuid"],
                    "title": r["title"],
                    "lang": "", "version": "1", "favourite": False, "rating": 0.0,
                    "updated": "", "importDate": "",
                    "hasImage": r["has_image"] or False,
                    "time": {"active": r["time_active"] or "", "total": r["time_total"] or ""},
                    "cooking": {"times": "0", "last": ""},
                    "tags": r["tags"] or [],
                    "servings": r["servings"] or [],
                    "ingredients": r["ingredients"] or [],
                    "steps": r["steps"] or [],
                    "original_steps": r["original_steps"] or [],
                    "enhanced_steps": r["enhanced_steps"] or [],
                    "preamble": r["preamble"] or "",
                    "source": {"name": r["source_name"] or "", "address": r["source_url"] or ""},
                    "_draft": r["is_draft"] or False,
                })
            return Response(json.dumps(recipes), mimetype="application/json")
        except Exception as e:
            app.logger.error(f"[recipes.json] DB read failed, falling back to flat file: {e}")
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


def make_kitchen_slug(title: str, uuid_prefix: str) -> str:
    """Generate a URL-safe slug from a recipe title + 6-char uuid suffix."""
    base = _re.sub(r'[^a-z0-9]+', '-', title.lower().strip())
    base = base.strip('-')[:60] or 'recipe'
    return f"{base}-{uuid_prefix.lower()[:6]}"


# Unicode vulgar fraction → decimal value. Used by _normalize_fractions.
_UNICODE_FRACTIONS = {
    '½': 0.5,   '¼': 0.25,  '¾': 0.75,
    '⅓': 1/3,   '⅔': 2/3,
    '⅕': 0.2,   '⅖': 0.4,   '⅗': 0.6,   '⅘': 0.8,
    '⅙': 1/6,   '⅚': 5/6,
    '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875,
    '⅐': 1/7,   '⅑': 1/9,   '⅒': 0.1,
}

def _normalize_fractions(line: str) -> str:
    """Convert '1 ½' → '1.5' and standalone '½' → '0.5' before the regex tokeniser runs."""
    if not line:
        return line
    frac_chars = ''.join(_UNICODE_FRACTIONS.keys())
    def _mixed(m):
        return f'{int(m.group(1)) + _UNICODE_FRACTIONS[m.group(2)]:g}'
    line = _re.sub(r'(\d+)\s*([' + frac_chars + r'])', _mixed, line)
    for ch, val in _UNICODE_FRACTIONS.items():
        line = line.replace(ch, f'{val:g}')
    return line


def _parse_ingredient_line(line):
    """Parse a free-text ingredient line into structured form.
    Returns dict: {count, unit, name, info, group} or None for empty lines.
    """
    line = _normalize_fractions((line or "").strip())
    if not line:
        return None
    # Group heading
    if line.startswith("##") or line.startswith("**"):
        return {"count": "", "unit": "", "name": line.lstrip("#* ").strip().rstrip(":"), "info": "", "group": "heading"}
    UNITS = ["tablespoons", "tablespoon", "teaspoons", "teaspoon", "tbsp", "tsp",
             "cups", "cup", "pints", "pint", "quarts", "quart", "gallons", "gallon",
             "fl oz", "ounces", "ounce", "oz", "pounds", "pound", "lbs", "lb",
             "grams", "gram", "kilograms", "kilogram", "kg", "g", "mg",
             "milliliters", "milliliter", "ml", "liters", "liter", "l",
             "pinch", "dash", "handful", "splash", "drop", "drops", "cloves", "clove",
             "stick", "sticks", "slice", "slices", "can", "cans", "bunch", "bunches"]
    num_pat = _re.compile(r'^\s*(\d+/\d+|\d+(?:\s+\d+/\d+)?(?:\.\d+)?)\s*')
    m = num_pat.match(line)
    count, rest = ("", line)
    if m:
        count = m.group(1).strip()
        rest = line[m.end():].strip()
    unit = ""
    rest_lower = rest.lower()
    for u in UNITS:
        if rest_lower == u or rest_lower.startswith(u + " ") or rest_lower.startswith(u + ","):
            unit = u
            rest = rest[len(u):].strip().lstrip(",").strip()
            if rest.lower().startswith("of "):
                rest = rest[3:].strip()
            break
    # Handle fused "200g" pattern (count present, unit fused at start of rest)
    if count and not unit:
        fused = _re.match(r'^([a-z]+)(?:\s|,|$)', rest, _re.IGNORECASE)
        if fused and fused.group(1).lower() in [u for u in UNITS if " " not in u]:
            unit = fused.group(1).lower()
            rest = rest[fused.end():].strip().lstrip(",").strip()
    # "Pinch of X" / "Dash of X" — no count
    if not count and not unit:
        for u in ["pinch", "dash", "handful", "splash"]:
            if rest_lower.startswith(u + " "):
                unit = u
                rest = rest[len(u):].strip()
                if rest.lower().startswith("of "):
                    rest = rest[3:].strip()
                break
    name = rest
    info = ""
    paren = _re.search(r'\s*\(([^)]+)\)', name)
    if paren:
        info = paren.group(1).strip()
        name = name[:paren.start()].strip()
    if "," in name and not info:
        parts = name.split(",", 1)
        name = parts[0].strip()
        info = parts[1].strip()
    return {"count": count, "unit": unit, "name": name, "info": info, "group": ""}


def _parse_ingredients_text(text):
    """Convert multi-line ingredients textarea into structured array."""
    if isinstance(text, list):
        return text
    return [p for p in (_parse_ingredient_line(l) for l in (text or "").splitlines()) if p]


def _parse_steps_text(text):
    """Convert multi-line steps textarea into structured array."""
    if isinstance(text, list):
        return text
    step_prefix = _re.compile(r'^\s*(?:\d+[\.\)]\s*|step\s+\d+:?\s*)', _re.IGNORECASE)
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        clean = step_prefix.sub('', line).strip()
        if clean:
            out.append(clean)
    return out


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


def _make_card_thumbnail(image_url):
    """Fetch full image, resize to ≤440px wide, upload to fal CDN. Returns URL or None."""
    try:
        resp = http_requests.get(image_url, timeout=10)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
        img.thumbnail((440, 9999), Image.Resampling.LANCZOS)
        return fal_client.upload_image(img, format='jpeg')
    except Exception:
        return None


# ─── Scan (AI recipe extraction) ────────────────────────────────────────────

_SCAN_PROMPT = """Extract the recipe from these cookbook page images. Return a JSON object with these fields:
{
  "title": "Recipe title",
  "preamble": "Brief description or headnote",
  "tags": ["tag1", "tag2"],
  "time": {"active": "20 mins", "total": "1 hour"},
  "servings": [{"count": "4", "unit": "serve"}],
  "ingredients": [
    {"count": "2", "unit": "cups", "name": "flour", "info": "sifted", "group": ""}
  ],
  "steps": ["Step 1 text verbatim", "Step 2 text verbatim"],
  "source_book": {"title": null, "author": null, "publisher": null, "year": null, "isbn": null, "page": null}
}

Rules:
- Extract ALL ingredients with precise quantities — do not simplify or combine
- Include ALL steps verbatim — do not rewrite, merge, or add steps
- Include at most 6 tags: clean facet labels only — lowercase short noun phrases like cuisine, dish family, or key technique (e.g. "italian", "braised", "pasta"); no stopwords, no punctuation, no more than 3 words each, never a sentence fragment
- If there are ingredient groups (e.g. "For the sauce"), set the group field
- If the page shows book title/author/publisher info, populate source_book; otherwise leave null
- Return ONLY valid JSON, no markdown fences"""


def _scan_call(content):
    """One Anthropic scan call. Returns parsed dict or raises."""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        lines = text.split("\n")[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return json.loads(text)


def _scan_with_retry(content, label="batch"):
    """Try twice; return (recipe_dict, None) or (None, last_exception)."""
    last_exc = None
    for attempt in range(2):
        try:
            return _scan_call(content), None
        except Exception as exc:
            app.logger.warning("scan %s attempt %d failed: %s", label, attempt + 1, exc)
            last_exc = exc
            if attempt == 0:
                _time.sleep(2)
    return None, last_exc


def _merge_scan_pages(pages):
    """Merge per-page scan results into one recipe dict."""
    base = dict(pages[0])
    for p in pages[1:]:
        base["ingredients"] = (base.get("ingredients") or []) + (p.get("ingredients") or [])
        base["steps"] = (base.get("steps") or []) + (p.get("steps") or [])
        if not base.get("title") and p.get("title"):
            base["title"] = p["title"]
    return base


@app.route("/api/scan", methods=["POST"])
def scan_recipe():
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

    content = images + [{"type": "text", "text": _SCAN_PROMPT}]

    # Attempt full batch (with one automatic retry)
    recipe, err = _scan_with_retry(content, label=f"{len(images)}-page batch")
    if recipe:
        recipe["_images_b64"] = images_b64
        recipe["_images_media_types"] = images_media_types
        return jsonify(recipe)

    # Batch failed — try per-page fallback if multiple pages
    if len(images) == 1:
        app.logger.error("scan: single page unreadable after retry: %s", err)
        return jsonify(error="unreadable")

    app.logger.warning("scan: batch failed (%d pages), trying per-page fallback", len(images))
    page_results = []
    failed_pages = []
    for i, img in enumerate(images):
        single_content = [img, {"type": "text", "text": _SCAN_PROMPT}]
        r, e2 = _scan_with_retry(single_content, label=f"page {i + 1}")
        if r:
            page_results.append(r)
        else:
            app.logger.error("scan: page %d unreadable: %s", i + 1, e2)
            failed_pages.append(i + 1)

    if not page_results:
        return jsonify(error="unreadable")

    merged = _merge_scan_pages(page_results)
    merged["_images_b64"] = images_b64
    merged["_images_media_types"] = images_media_types
    merged["failed_pages"] = failed_pages
    return jsonify(merged)


# ─── Cover OCR ───────────────────────────────────────────────────────────────

@app.route("/api/scan-cover", methods=["POST"])
def scan_cover():
    """Extract book metadata from a cover image using Claude vision."""
    f = request.files.get("file")
    if not f:
        # Also accept base64 JSON
        data = request.get_json(silent=True) or {}
        b64 = data.get("image_b64")
        media_type = data.get("media_type", "image/jpeg")
        if not b64:
            return jsonify(error="No image provided"), 400
    else:
        raw = f.read()
        data_bytes, media_type = _prepare_image(raw)
        b64 = base64.b64encode(data_bytes).decode("utf-8")

    content = [
        {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": b64},
        },
        {
            "type": "text",
            "text": (
                "Extract book metadata from this cover image. "
                'Return ONLY valid JSON: {"title": "...", "author": "...", "publisher": "...", "year": null, "isbn": null}'
            ),
        },
    ]
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": content}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")
            resp_text = "\n".join(lines[1:-1] if lines and lines[-1].strip() == "```" else lines[1:])
        return jsonify(json.loads(resp_text))
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/recipes/recent-cookbooks")
def recent_cookbooks():
    """Return distinct cookbooks recently used for scan imports."""
    if not DATABASE_URL:
        return jsonify([])
    try:
        user = get_current_user()
        user_id = user["id"] if user else None
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT DISTINCT ON (source_book_title)
                source_book_title, source_book_author, source_book_publisher, source_book_year
            FROM user_kitchen_recipes
            WHERE source_book_title IS NOT NULL
              AND (%s IS NULL OR user_id = %s)
            ORDER BY source_book_title, MAX(created_at) OVER (PARTITION BY source_book_title) DESC
            LIMIT 20
        """, (user_id, user_id))
        rows = [dict(r) for r in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        app.logger.warning(f"[recent_cookbooks] {e}")
        return jsonify([])


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
            model="claude-sonnet-4-6",
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
        return jsonify(error=f"Failed to parse the response: {e}"), 500
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
        parsed = _parse_ingredient_line(str(ing_str).strip())
        if parsed:
            parsed["group"] = ""
            ingredients.append(parsed)
        else:
            ingredients.append({"count": "", "unit": "", "name": str(ing_str).strip(), "info": "", "group": ""})

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
    tags = _sanitize_tags(list(dict.fromkeys(tags)))

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
  "steps": ["Step 1 text verbatim", "Step 2 text verbatim"],
  "source_book": null
}}

Rules:
- Extract ALL ingredients with precise quantities — do not simplify or combine
- Include ALL steps verbatim — do not rewrite, merge, or add steps
- Include at most 6 tags: clean facet labels only — lowercase short noun phrases like cuisine, dish family, or key technique (e.g. "italian", "braised", "pasta"); no stopwords, no punctuation, no more than 3 words each, never a sentence fragment
- source_book is always null for URL imports
- Populate "group" with the section heading for each ingredient that belongs to a named section (e.g. "Marinade", "Spice blend", "For the cassava"); use "" if the recipe has no sections or the ingredient belongs to the unlabelled main list
- Return ONLY valid JSON, no markdown fences

Webpage text:
{text_only}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
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
        return jsonify(error=f"Failed to parse the response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/api/recipes/extract-from-text", methods=["POST"])
def extract_from_text():
    data = request.get_json()
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify(error="No text provided"), 400

    text_truncated = text[:8000]

    prompt = f"""Extract the recipe from this text. Return a JSON object with these fields:
{{
  "title": "Recipe title",
  "preamble": "Brief description or headnote",
  "tags": ["tag1", "tag2"],
  "time": {{"active": "20 mins", "total": "1 hour"}},
  "servings": [{{"count": "4", "unit": "serve"}}],
  "ingredients": [
    {{"count": "2", "unit": "cups", "name": "flour", "info": "sifted", "group": ""}}
  ],
  "steps": ["Step 1 text verbatim", "Step 2 text verbatim"],
  "source_book": {{"title": null, "author": null, "publisher": null, "year": null, "isbn": null, "page": null}}
}}

Rules:
- Extract ALL ingredients with precise quantities — do not simplify or combine
- Include ALL steps verbatim — do not rewrite, merge, or add steps
- Include at most 6 tags: clean facet labels only — lowercase short noun phrases like cuisine, dish family, or key technique (e.g. "italian", "braised", "pasta"); no stopwords, no punctuation, no more than 3 words each, never a sentence fragment
- If this appears to be from a cookbook, populate source_book; otherwise leave null
- Return ONLY valid JSON, no markdown fences

Recipe text:
{text_truncated}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
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
        recipe["_method"] = "text"
        return jsonify(recipe)
    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse the response: {e}"), 500
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
                LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
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
  "provenance_notes": "1-2 sentences on the cultural preservation significance — what knowledge this dish keeps alive",
  "origin": "2-3 sentences: the cultural and historical lineage of this dish or approach. Institutional register, Larousse-grade.",
  "flavour_context": "2-3 sentences on the flavour logic — how the principal flavours balance and why it works on the palate.",
  "lives_or_dies": "2-4 sentences naming the one technical moment that makes or breaks this dish, with the rescue if it slips (e.g. 'beurre blanc breaks above 58C — pull the pan, drop in a cold cube of butter, whisk it back').",
  "quality_hierarchy": [
    {{"ingredient": "ingredient name", "reserve": "the benchmark, best-in-class version", "house": "the solid everyday version", "swap_cost": "what you lose stepping down"}}
  ],
  "sensory_tests": [
    {{"sense": "touch | sight | sound | smell | taste", "cue": "what 'right' is — concrete and physical, e.g. 'bark like damp leather'", "fail_indicator": "the tell that it has gone wrong"}}
  ],
  "cross_cuisine_parallels": [
    {{"cuisine": "the other cuisine", "dish": "the parallel dish or technique", "mechanism": "the shared underlying mechanism — why they are cousins"}}
  ]
}}

Rules:
- If the brief asks for a historical period, be historically accurate about what existed then
- If the brief mentions a specific cuisine, techniques must be authentic to that cuisine
- Every ingredient must serve a purpose — no garnish-for-the-sake-of-garnish
- The preamble and provenance_notes are what make this a Provenance recipe, not just a recipe
- Minimum 8 ingredients, 6 steps
- If uncertain about historical specifics, note what is known and what is a respectful approximation
- quality_hierarchy: at least 3 entries. sensory_tests: at least 4. cross_cuisine_parallels: at least 2.
- origin, flavour_context, lives_or_dies and every cue must be in Provenance's voice — chef at the pass, institutional reference. Never use the words "AI", "curated", "seamless", "leverage", or "discover"."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            resp_text = "\n".join(lines)

        rdata = json.loads(resp_text)

        _ing_text = "\n".join(
            f"- {i.get('count','')} {i.get('unit','')} {i.get('name','')}".strip()
            for i in rdata.get("ingredients", [])
        )
        _origin            = rdata.get("origin")
        _quality_hierarchy = rdata.get("quality_hierarchy") or []
        _sensory_tests     = rdata.get("sensory_tests") or []
        _cross_cuisine     = rdata.get("cross_cuisine_parallels") or []
        _flavour_context   = rdata.get("flavour_context")
        _lives_or_dies     = rdata.get("lives_or_dies")
        try:
            _beverage_pairings = _enrich_beverage_pairings(rdata.get("title", ""), _ing_text)
        except Exception:
            _beverage_pairings = None

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

        # Save to user_kitchen_recipes so /recipe/<slug>/edit works
        if DATABASE_URL:
            try:
                user = get_current_user()
                user_id = user["id"] if user else None
                slug_base = _slugify(rdata.get("title", "composed-recipe"))
                slug = slug_base
                conn2 = get_db()
                cur2 = conn2.cursor()
                suffix = 1
                while suffix < 100:
                    cur2.execute(
                        "SELECT uuid FROM user_kitchen_recipes WHERE slug = %s AND user_id IS NOT DISTINCT FROM %s",
                        (slug, user_id)
                    )
                    if not cur2.fetchone():
                        break
                    slug = f"{slug_base}-{suffix}"
                    suffix += 1
                time_dict = rdata.get("time", {})
                if not isinstance(time_dict, dict):
                    time_dict = {}
                cur2.execute("""
                    INSERT INTO user_kitchen_recipes
                        (uuid, user_id, title, slug, preamble, tags, ingredients, steps,
                         time_active, time_total, servings, is_draft,
                         origin, quality_hierarchy, sensory_tests, cross_cuisine_parallels,
                         flavour_context, lives_or_dies, beverage_pairings)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE,
                            %s, %s, %s, %s, %s, %s, %s)
                """, (
                    recipe_uuid,
                    user_id,
                    rdata.get("title", "Composed Recipe"),
                    slug,
                    rdata.get("preamble", ""),
                    json.dumps(rdata.get("tags", [])),
                    json.dumps(rdata.get("ingredients", [])),
                    json.dumps(rdata.get("steps", [])),
                    time_dict.get("active", ""),
                    time_dict.get("total", ""),
                    json.dumps(rdata.get("servings", [])),
                    _origin,
                    json.dumps(_quality_hierarchy) if _quality_hierarchy else None,
                    json.dumps(_sensory_tests) if _sensory_tests else None,
                    json.dumps(_cross_cuisine) if _cross_cuisine else None,
                    _flavour_context,
                    _lives_or_dies,
                    json.dumps(_beverage_pairings) if _beverage_pairings else None,
                ))
                conn2.commit()
                cur2.close()
                conn2.close()
                recipe["slug"] = slug
            except Exception as e:
                app.logger.error(f"[COMPOSE] db_write=FAILED err={e}")
                recipe["slug"] = None

        return jsonify(recipe)

    except json.JSONDecodeError as e:
        return jsonify(error=f"Failed to parse the response: {e}"), 500
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
    recipe_slug = make_kitchen_slug("Untitled Recipe", recipe_uuid)
    recipe["slug"] = recipe_slug
    if DATABASE_URL_WRITE:
        try:
            user = get_current_user()
            user_id = user["id"] if user else None
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_kitchen_recipes
                    (uuid, user_id, title, slug, tags, ingredients, steps, servings, is_draft)
                VALUES (%s, %s, %s, %s, '[]', '[]', '[]', '[]', TRUE)
                ON CONFLICT (uuid) DO NOTHING
            """, (recipe_uuid, user_id, "Untitled Recipe", recipe_slug))
            cur.close()
            conn.close()
        except Exception as e:
            app.logger.error(f"[CREATE_BLANK_RECIPE] uuid={recipe_uuid} db_write=FAILED err={e}")
    return jsonify(recipe)


@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    # Accept free-text textarea input for ingredients and steps
    if isinstance(data.get("ingredients"), str):
        data["ingredients"] = _parse_ingredients_text(data["ingredients"])
    if isinstance(data.get("steps"), str):
        data["steps"] = _parse_steps_text(data["steps"])
    if "method_steps" in data and "steps" not in data:
        raw = data["method_steps"]
        data["steps"] = _parse_steps_text(raw) if isinstance(raw, str) else raw
    # Clean ingredient names — strip editorial refs, page citations, trailing punctuation
    _ings = data.get("ingredients", [])
    if isinstance(_ings, list):
        for _ing in _ings:
            if isinstance(_ing, dict) and _ing.get("name"):
                _ing["name"] = _clean_ingredient_name(_ing["name"])
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
        "tags": _sanitize_tags(data.get("tags", [])),
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

    # Save all scanned page images as source files (never use as hero)
    if images_b64:
        image_dir = EXTRACTED_DIR / recipe_uuid
        image_dir.mkdir(parents=True, exist_ok=True)
        for i, b64 in enumerate(images_b64):
            (image_dir / f"source-{i}.jpg").write_bytes(base64.b64decode(b64))

    # ── Sashimi Pipeline ────────────────────────────────────────────────────────

    # Step 1: Parse yield
    raw_servings = recipe.get("servings", [])
    servings_text, servings_count = _parse_yield(raw_servings)

    # Step 2: Unit conversion
    converted_ingredients, source_units_raw, unit_warnings = _convert_to_metric(
        recipe.get("ingredients", [])
    )
    recipe["ingredients"] = converted_ingredients

    # Build ingredient strings for Claude calls
    ingredient_strings = []
    for ing in converted_ingredients:
        if not isinstance(ing, dict):
            ingredient_strings.append(str(ing))
            continue
        parts = []
        if ing.get("count"):
            parts.append(str(ing["count"]))
        if ing.get("unit"):
            parts.append(ing["unit"])
        parts.append(ing.get("name", ""))
        if ing.get("info"):
            parts.append(f"({ing['info']})")
        ingredient_strings.append(" ".join(parts).strip())

    # Step 3: Extract book metadata
    source_book = data.get("source_book") or {}
    source_book_title = source_book.get("title") or data.get("source_book_title")
    source_book_author = source_book.get("author") or data.get("source_book_author")
    source_book_publisher = source_book.get("publisher") or data.get("source_book_publisher")
    source_book_year = source_book.get("year") or data.get("source_book_year")
    source_book_isbn = source_book.get("isbn") or data.get("source_book_isbn")
    source_book_page = source_book.get("page") or data.get("source_book_page")

    # Step 4: Add step insights (verbatim steps — no rewriting)
    steps = list(recipe.get("steps", []))
    enhanced_steps = []
    try:
        enhanced_steps = _add_step_insights(recipe["title"], ingredient_strings, steps)
        recipe["original_steps"] = steps
        recipe["enhanced_steps"] = enhanced_steps
        # steps column stays verbatim — do NOT overwrite recipe["steps"]
    except Exception:
        pass

    # Step 5: Enhance recipe structure
    structure = {}
    quality_warnings = list(unit_warnings)
    try:
        ingredients_text = "\n".join(f"- {s}" for s in ingredient_strings)
        steps_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
        structure = _enhance_recipe_structure(recipe["title"], ingredients_text, steps_text)
        if structure.get("quality_warnings"):
            quality_warnings.extend(structure["quality_warnings"])
    except Exception:
        pass

    # Step 6: Match suppliers and merge with origin markers
    ingredient_names = [ing.get("name", "") for ing in converted_ingredients
                        if isinstance(ing, dict) and ing.get("name")]
    supplier_matches = _match_suppliers_for_ingredients(ingredient_names)

    # Build ingredient→supplier lookup
    supplier_by_ingredient = {}
    for s in supplier_matches:
        for prod in s.get("products", []):
            pname = (prod.get("name") or "").lower()
            for iname in ingredient_names:
                if iname.lower() in pname or pname in iname.lower():
                    supplier_by_ingredient.setdefault(iname, [])
                    if s not in supplier_by_ingredient[iname]:
                        supplier_by_ingredient[iname].append(s)

    origin_markers = structure.get("ingredient_origin_markers", [])
    ingredient_origin_markers = []
    for marker in origin_markers:
        iname = marker.get("ingredient_name", "")
        entry = dict(marker)
        matched_sups = supplier_by_ingredient.get(iname, [])
        if not matched_sups:
            for k, v in supplier_by_ingredient.items():
                if iname.lower() in k.lower() or k.lower() in iname.lower():
                    matched_sups = v
                    break
        entry["matched_supplier_ids"] = [s["id"] for s in matched_sups]
        entry["suppliers"] = matched_sups
        ingredient_origin_markers.append(entry)

    # Append suppliers not yet in origin_markers
    already_marked = {m.get("ingredient_name", "").lower() for m in ingredient_origin_markers}
    for iname, sups in supplier_by_ingredient.items():
        if iname.lower() not in already_marked:
            ingredient_origin_markers.append({
                "ingredient_name": iname,
                "origin_marker": "",
                "matched_supplier_ids": [s["id"] for s in sups],
                "suppliers": sups,
            })

    # ── Post-parse enrichment (beverage pairings, time estimates, FAQs) ───────
    _enrich_pairings_result = []
    _enrich_faqs_result = []
    try:
        from concurrent.futures import ThreadPoolExecutor
        _ex_active = recipe.get("time", {}).get("active", "").strip()
        _ex_total  = recipe.get("time", {}).get("total", "").strip()
        _ing_lines = "\n".join(
            f"{i.get('count', '')} {i.get('unit', '')} {i.get('name', '')}".strip()
            for i in converted_ingredients
        )
        _steps_lines = "\n".join(
            f"{idx + 1}. {(enhanced_steps[idx].get('text', '') if idx < len(enhanced_steps) else '') or (steps[idx] if idx < len(steps) else '')}"
            for idx in range(len(steps))
        )
        with ThreadPoolExecutor(max_workers=3) as _pool:
            _fp = _pool.submit(_enrich_beverage_pairings, recipe["title"], _ing_lines)
            _ff = _pool.submit(_enrich_faqs, recipe["title"], _ing_lines, _steps_lines)
            _ft = _pool.submit(_enrich_time_estimates, recipe["title"], _ing_lines, _steps_lines, _ex_active, _ex_total)
            _enrich_pairings_result = _fp.result(timeout=30) or []
            _enrich_faqs_result     = _ff.result(timeout=30) or []
            _at, _tt = _ft.result(timeout=30)
        if _at:
            recipe.setdefault("time", {})["active"] = _at
        if _tt:
            recipe.setdefault("time", {})["total"] = _tt
    except Exception as _enrich_err:
        app.logger.warning(f"[CREATE_RECIPE] enrichment stage failed: {_enrich_err}")

    recipe_slug = make_kitchen_slug(recipe["title"], recipe_uuid)
    recipe["slug"] = recipe_slug
    recipes.append(recipe)
    save_recipes(recipes)

    # Persist to PostgreSQL (source of truth — flat file is ephemeral on Fly.io)
    if DATABASE_URL_WRITE:
        try:
            user = get_current_user()
            user_id = user["id"] if user else None
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_kitchen_recipes
                    (uuid, user_id, title, slug, preamble, tags, ingredients, steps,
                     original_steps, enhanced_steps, time_active, time_total,
                     servings, source_name, source_url, has_image, is_draft,
                     source_book_title, source_book_author, source_book_publisher,
                     source_book_year, source_book_isbn, source_book_page,
                     origin, cuisine, source_pages_count, quality_hierarchy, sensory_tests, cross_cuisine_parallels,
                     flavour_context, lives_or_dies, quality_warnings,
                     ingredient_origin_markers, source_units_raw,
                     servings_text, servings_count,
                     beverage_pairings, faqs)
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (uuid) DO NOTHING
            """, (
                recipe_uuid,
                user_id,
                recipe["title"],
                recipe_slug,
                recipe.get("preamble", ""),
                json.dumps(recipe.get("tags", [])),
                json.dumps(converted_ingredients),
                json.dumps(steps),                          # verbatim original steps
                json.dumps(steps),                          # original_steps
                json.dumps(enhanced_steps),
                recipe.get("time", {}).get("active", ""),
                recipe.get("time", {}).get("total", ""),
                json.dumps(raw_servings),
                recipe.get("source", {}).get("name", ""),
                recipe.get("source", {}).get("address", ""),
                recipe.get("hasImage", False),
                recipe.get("_draft", False),
                source_book_title,
                source_book_author,
                source_book_publisher,
                source_book_year,
                source_book_isbn,
                source_book_page,
                structure.get("origin"),
                _sanitize_cuisine(structure.get("cuisine")),
                len(images_b64),
                json.dumps(structure["quality_hierarchy"]) if structure.get("quality_hierarchy") else None,
                json.dumps(structure["sensory_tests"]) if structure.get("sensory_tests") else None,
                json.dumps(structure["cross_cuisine_parallels"]) if structure.get("cross_cuisine_parallels") else None,
                structure.get("flavour_context"),
                structure.get("lives_or_dies"),
                json.dumps(quality_warnings) if quality_warnings else None,
                json.dumps(ingredient_origin_markers) if ingredient_origin_markers else None,
                json.dumps(source_units_raw) if source_units_raw else None,
                servings_text,
                servings_count,
                json.dumps(_enrich_pairings_result) if _enrich_pairings_result else None,
                json.dumps(_enrich_faqs_result) if _enrich_faqs_result else None,
            ))
            cur.close()
            conn.close()
            app.logger.info(
                f"[CREATE_RECIPE] title={recipe['title']!r} uuid={recipe_uuid} "
                f"user_id={user_id} db_write=SUCCESS"
            )
        except Exception as e:
            app.logger.error(
                f"[CREATE_RECIPE] title={recipe['title']!r} uuid={recipe_uuid} "
                f"db_write=FAILED err={e}"
            )
    else:
        app.logger.warning(
            f"[CREATE_RECIPE] title={recipe['title']!r} uuid={recipe_uuid} "
            f"db_write=SKIPPED (no DATABASE_URL_WRITE)"
        )

    return jsonify(recipe), 201


@app.route("/api/recipes/<slug>", methods=["GET"])
def get_recipe_api(slug):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT uuid, slug, title, preamble, ingredients, steps,
                   time_active, time_total, servings, tags,
                   source_name, source_url, is_draft, has_image
            FROM user_kitchen_recipes
            WHERE slug = %s AND user_id = %s
            LIMIT 1
        """, (slug, user["id"]))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Not found or not yours"}), 404
        return jsonify(dict(row))
    finally:
        cur.close()
        conn.close()


@app.route("/api/recipes/<recipe_uuid>", methods=["PUT"])
def update_recipe(recipe_uuid):
    data = request.get_json()
    if isinstance(data.get("ingredients"), str):
        data["ingredients"] = _parse_ingredients_text(data["ingredients"])
    if isinstance(data.get("steps"), str):
        data["steps"] = _parse_steps_text(data["steps"])
    if "method_steps" in data and "steps" not in data:
        raw = data["method_steps"]
        data["steps"] = _parse_steps_text(raw) if isinstance(raw, str) else raw
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

    # Sync to PostgreSQL
    if DATABASE_URL_WRITE:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE user_kitchen_recipes SET
                    title = %s, preamble = %s, tags = %s, ingredients = %s,
                    steps = %s, original_steps = %s, enhanced_steps = %s,
                    time_active = %s, time_total = %s, servings = %s,
                    source_name = %s, source_url = %s, has_image = %s,
                    is_draft = %s, updated_at = NOW()
                WHERE uuid = %s
            """, (
                recipe["title"],
                recipe.get("preamble", ""),
                json.dumps(recipe.get("tags", [])),
                json.dumps(recipe.get("ingredients", [])),
                json.dumps(recipe.get("steps", [])),
                json.dumps(recipe.get("original_steps", [])),
                json.dumps(recipe.get("enhanced_steps", [])),
                recipe.get("time", {}).get("active", ""),
                recipe.get("time", {}).get("total", ""),
                json.dumps(recipe.get("servings", [])),
                recipe.get("source", {}).get("name", ""),
                recipe.get("source", {}).get("address", ""),
                data.get("has_image", recipe.get("hasImage", False)),
                recipe.get("_draft", False),
                recipe_uuid,
            ))
            cur.close()
            conn.close()
        except Exception as e:
            app.logger.error(f"[UPDATE_RECIPE] uuid={recipe_uuid} db_sync=FAILED err={e}")

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

    # Sync delete to PostgreSQL
    if DATABASE_URL_WRITE:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM user_kitchen_recipes WHERE uuid = %s", (recipe_uuid,))
            cur.close()
            conn.close()
        except Exception as e:
            app.logger.error(f"[DELETE_RECIPE] uuid={recipe_uuid} db_sync=FAILED err={e}")

    return jsonify(success=True)


# ─── Recipe editor ────────────────────────────────────────────────────────────

@app.route("/api/recipes/by-slug/<slug>", methods=["GET"])
def get_user_recipe_by_slug(slug):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT uuid, slug, title, preamble, ingredients, steps,
                   time_active, time_total, servings, tags,
                   source_name, source_url, is_draft, has_image
            FROM user_kitchen_recipes
            WHERE slug = %s AND user_id = %s
            LIMIT 1
        """, (slug, user["id"]))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Recipe not found or not yours"}), 404
        return jsonify(dict(row))
    finally:
        cur.close()
        conn.close()


@app.route("/api/recipes/<slug>/upload-image", methods=["POST"])
def upload_user_recipe_image(slug):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files["file"]
    if not f or not f.filename:
        return jsonify({"error": "No file"}), 400
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in {"jpg", "jpeg", "png", "webp"}:
        return jsonify({"error": "Use jpeg, png, or webp"}), 400
    f.seek(0, 2)
    size = f.tell()
    f.seek(0)
    if size > 5 * 1024 * 1024:
        return jsonify({"error": "File too large. Max 5MB"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            "SELECT uuid FROM user_kitchen_recipes WHERE slug = %s AND user_id = %s",
            (slug, user["id"])
        )
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Recipe not found"}), 404
        recipe_uuid = row["uuid"]
        img_bytes = f.read()
        image_dir = EXTRACTED_DIR / recipe_uuid
        image_dir.mkdir(parents=True, exist_ok=True)
        (image_dir / "hero.jpg").write_bytes(img_bytes)
        (image_dir / "main.jpg").write_bytes(img_bytes)
        cur.execute(
            "UPDATE user_kitchen_recipes SET has_image = TRUE WHERE uuid = %s AND user_id = %s",
            (recipe_uuid, user["id"])
        )
        conn.commit()
        return jsonify({"ok": True, "url": f"/images/{recipe_uuid}/hero.jpg"})
    finally:
        cur.close()
        conn.close()


@app.route("/recipe/<slug>/edit")
def recipe_editor(slug):
    user = get_current_user()
    if not user:
        return _login_redirect()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT uuid, slug, title, preamble, ingredients, steps,
                   time_active, time_total, servings, tags,
                   source_name, source_url, is_draft, has_image,
                   quality_warnings, source_pages_count
            FROM user_kitchen_recipes
            WHERE slug = %s AND user_id = %s
            LIMIT 1
        """, (slug, user["id"]))
        row = cur.fetchone()
        if not row:
            return redirect("/kitchen")
        _row = dict(row)
        _row["quality_warnings"] = _row.get("quality_warnings") or []
        # Normalize string flags to structured form
        normalized = []
        for i, w in enumerate(_row["quality_warnings"]):
            if isinstance(w, str):
                normalized.append({"section": "general", "message": w, "dismissed": False, "_idx": i})
            elif isinstance(w, dict):
                w2 = dict(w)
                w2.setdefault("section", "general")
                w2.setdefault("dismissed", False)
                w2["_idx"] = i
                normalized.append(w2)
        _row["quality_warnings"] = normalized
        _row["source_pages_count"] = _row.get("source_pages_count") or 0
        return render_template("recipe_editor.html", recipe=_row)
    finally:
        cur.close()
        conn.close()


@app.route("/api/recipes/<recipe_uuid>/flag-dismiss", methods=["POST"])
def dismiss_recipe_flag(recipe_uuid):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    data = request.get_json() or {}
    idx = data.get("index")
    if idx is None or not isinstance(idx, int):
        return jsonify({"error": "index required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(
            "SELECT quality_warnings FROM user_kitchen_recipes WHERE uuid = %s AND user_id = %s LIMIT 1",
            (recipe_uuid, user["id"])
        )
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Not found"}), 404
        warnings = row["quality_warnings"] or []
        if isinstance(warnings, str):
            try:
                warnings = json.loads(warnings)
            except Exception:
                warnings = []
        if 0 <= idx < len(warnings):
            w = warnings[idx]
            if isinstance(w, str):
                warnings[idx] = {"section": "general", "message": w, "dismissed": True}
            elif isinstance(w, dict):
                w["dismissed"] = True
        cur.execute(
            "UPDATE user_kitchen_recipes SET quality_warnings = %s::jsonb WHERE uuid = %s AND user_id = %s",
            (json.dumps(warnings), recipe_uuid, user["id"])
        )
        return jsonify({"ok": True})
    finally:
        cur.close()
        conn.close()


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
        abort(404)

    recipes = load_recipes()
    recipe = next((r for r in recipes if r["uuid"] == recipe_uuid), None)
    if not recipe:
        abort(404)

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
                "SELECT * FROM technique_references WHERE published IS NOT FALSE ORDER BY id LIMIT %s OFFSET %s",
                (per_page, (page - 1) * per_page),
            )
        else:
            cur.execute("SELECT * FROM technique_references WHERE published IS NOT FALSE ORDER BY id")
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
        "SELECT * FROM technique_references WHERE published IS NOT FALSE ORDER BY id LIMIT %s OFFSET %s",
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
    cur.execute("SELECT * FROM technique_references WHERE published IS NOT FALSE ORDER BY id")
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


# ─── Sashimi validator ────────────────────────────────────────────────────────
# Applies to INSERTs and UPDATEs only. Existing rows with NULL in new pillar
# columns are not retroactively failed. Content watcher handles backlog enrichment.

_SASHIMI_BANNED_WORDS = [
    "ai-powered", " ai ", "platform", "solution", "non-negotiable",
    "revolutionary", "game-changing", "world-class", "premium",
    "leverage", "unlock", "seamless", "cutting-edge",
]

_SASHIMI_CHECKED_FIELDS = [
    "origin", "description", "flavour_context", "species_precision",
    "quality_hierarchy", "sensory_tests", "key_principles",
]


def _validate_technique_entry(e: dict) -> list[str]:
    """
    Validate a technique entry at commit time. Returns a list of error strings.
    Empty list means the entry passes.

    Rules (new inserts must satisfy all):
    1. Four existing pillars: origin, description, key_principles, flavour_context — all non-empty.
    2. Three new pillars: quality_hierarchy, sensory_tests, species_precision — all non-empty.
    3. quality_hierarchy must be a list with at least one item.
    4. sensory_tests must be a list of dicts, each with sense/cue/fail_indicator keys.
    5. At least one technique_ingredients row present (ingredients list non-empty).
    6. Every ingredient row has a tier value.
    7. No banned words in any text field.
    """
    errors = []

    # Rule 1 — four existing pillars
    for field in ("origin", "description", "key_principles", "flavour_context"):
        val = e.get(field)
        if not val or (isinstance(val, str) and not val.strip()):
            errors.append(f"Missing required pillar: {field}")

    # Rule 2 — three new pillars
    for field in ("quality_hierarchy", "sensory_tests", "species_precision"):
        val = e.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            errors.append(f"Missing required new pillar: {field}")

    # Rule 3 — quality_hierarchy must be a non-empty list
    qh = e.get("quality_hierarchy")
    if qh is not None:
        if not isinstance(qh, list) or len(qh) == 0:
            errors.append("quality_hierarchy must be a non-empty list")

    # Rule 4 — sensory_tests must be a list of dicts with sense/cue/fail_indicator
    st = e.get("sensory_tests")
    if st is not None:
        if not isinstance(st, list) or len(st) == 0:
            errors.append("sensory_tests must be a non-empty list")
        else:
            for i, test in enumerate(st):
                if not isinstance(test, dict):
                    errors.append(f"sensory_tests[{i}] must be a dict with sense/cue/fail_indicator")
                else:
                    for key in ("sense", "cue", "fail_indicator"):
                        if not test.get(key):
                            errors.append(f"sensory_tests[{i}] missing key: {key}")

    # Rule 5 — at least one ingredient
    ingredients = e.get("ingredients", [])
    if not ingredients:
        errors.append("At least one technique_ingredients row required")

    # Rule 6 — every ingredient must have a tier
    if isinstance(ingredients, list):
        for i, ing in enumerate(ingredients):
            if isinstance(ing, dict) and not ing.get("tier"):
                errors.append(f"ingredients[{i}] missing tier value")

    # Rule 7 — banned words across text fields
    for field in _SASHIMI_CHECKED_FIELDS:
        val = e.get(field)
        if val is None:
            continue
        text = val if isinstance(val, str) else json.dumps(val)
        text_lower = text.lower()
        for bw in _SASHIMI_BANNED_WORDS:
            if bw in text_lower:
                errors.append(f"Banned word '{bw.strip()}' found in {field}")

    return errors


def _resolve_supplier_id(cur, supplier_name: str) -> int | None:
    """Look up a supplier by name (case-insensitive). Returns id or None."""
    if not supplier_name:
        return None
    cur.execute(
        "SELECT id FROM suppliers WHERE LOWER(name) = LOWER(%s) LIMIT 1",
        (supplier_name,)
    )
    row = cur.fetchone()
    return row[0] if row else None


@app.route("/api/techniques/bulk", methods=["POST"])
def bulk_create_techniques():
    entries = request.get_json()
    if not isinstance(entries, list):
        return jsonify(error="Expected a JSON array"), 400

    conn = get_db()
    cur = conn.cursor()
    count = 0
    validation_errors = []

    for e in entries:
        # Run Sashimi validator — collect errors but do not hard-block legacy imports
        # that lack the new pillars (those use the old import path without ingredients).
        # Hard-block only if the entry explicitly includes new-schema fields.
        is_new_schema = "ingredients" in e or "quality_hierarchy" in e
        if is_new_schema:
            errs = _validate_technique_entry(e)
            if errs:
                validation_errors.append({"entry": e.get("name", "?"), "errors": errs})
                continue  # skip this entry — do not commit a failing entry

        cur.execute(
            """INSERT INTO technique_references
               (name, category, description, key_principles, common_mistakes, pro_tips,
                trigger_keywords, authority_tier, related_techniques, tier_level,
                source_book, cross_cuisine_parallels, origin, flavour_context,
                quality_hierarchy, sensory_tests, species_precision)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
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
                json.dumps(e["quality_hierarchy"]) if e.get("quality_hierarchy") is not None else None,
                json.dumps(e["sensory_tests"]) if e.get("sensory_tests") is not None else None,
                e.get("species_precision"),
            ),
        )
        technique_id = cur.fetchone()[0]

        # Write technique_ingredients rows — one transaction with the parent row
        ingredients = e.get("ingredients", [])
        for idx, ing in enumerate(ingredients):
            if not isinstance(ing, dict):
                continue
            provider_id = ing.get("provider_supplier_id")
            if provider_id is None and ing.get("provider_supplier_name"):
                provider_id = _resolve_supplier_id(cur, ing["provider_supplier_name"])
            cur.execute(
                """INSERT INTO technique_ingredients
                   (technique_id, ingredient_name, origin_brand, provider_supplier_id, tier, display_order)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    technique_id,
                    ing.get("name", ""),
                    ing.get("origin_brand"),
                    provider_id,
                    ing.get("tier"),
                    ing.get("display_order", idx),
                ),
            )
        count += 1

    cur.close()
    conn.close()

    response = {"inserted": count}
    if validation_errors:
        response["validation_errors"] = validation_errors
        response["skipped"] = len(validation_errors)
    return jsonify(response), 201


@app.route("/api/techniques/<int:technique_id>", methods=["GET"])
def get_technique(technique_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE id = %s AND published IS NOT FALSE", (technique_id,))
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
        "species_precision": str,
    }
    json_fields = {
        "trigger_keywords", "related_techniques", "cross_cuisine_parallels",
        "quality_hierarchy", "sensory_tests",
    }

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


@app.route("/admin/wireframe/atelier")
def admin_wireframe_atelier():
    user = get_current_user()
    if not user or user.get("role") not in ("founder", "admin"):
        return redirect(url_for("index"))
    return send_from_directory("static", "wireframe-atelier.html")


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
            model="claude-sonnet-4-6",
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
        return jsonify(error=f"Failed to parse the response: {e}"), 500
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


# ─── Sashimi-Grade Ingestion Pipeline Helpers ────────────────────────────────

UNIT_CONVERSIONS = {
    'cup': ('ml', 240), 'cups': ('ml', 240),
    'tablespoon': ('ml', 15), 'tablespoons': ('ml', 15), 'tbsp': ('ml', 15),
    'teaspoon': ('ml', 5), 'teaspoons': ('ml', 5), 'tsp': ('ml', 5),
    'oz': ('g', 28.35), 'ounce': ('g', 28.35), 'ounces': ('g', 28.35),
    'lb': ('g', 453.6), 'pound': ('g', 453.6), 'pounds': ('g', 453.6),
    'fl oz': ('ml', 29.57),
    'quart': ('ml', 946), 'quarts': ('ml', 946),
    'pint': ('ml', 473), 'pints': ('ml', 473),
}

TEMP_PATTERN = _re.compile(r'(\d+(?:\.\d+)?)\s*°F')

ENCODING_FIXES = [
    ('â€™', '\u2019'), ('â€˜', '\u2018'), ('â€œ', '\u201c'), ('â€\x9d', '\u201d'),
    ('â€"', '\u2013'), ('â€"', '\u2014'), ('Ã©', 'é'), ('Ã¨', 'è'),
    ('Ã\xa0', 'à'), ('Ã§', 'ç'), ('Ã®', 'î'), ('Ã´', 'ô'),
    ('Ã¢', 'â'), ('Ã»', 'û'), ('Ã¹', 'ù'), ('Ã«', 'ë'),
    ('â€¦', '…'), ('â€¢', '•'),
]


def _cleanup_raw_text(text):
    """Fix encoding artifacts, smart quotes, PDF artifacts, OCR hyphenation.
    Returns (cleaned_text, list_of_corrections)."""
    corrections = []
    result = text

    for bad, good in ENCODING_FIXES:
        if bad in result:
            result = result.replace(bad, good)
            corrections.append(f"encoding: {bad!r}")

    # Smart quotes / dashes normalization
    result = result.replace('\u201c', '"').replace('\u201d', '"')
    result = result.replace('\u2018', "'").replace('\u2019', "'")
    result = result.replace('\u2013', '–').replace('\u2014', '—')

    # PDF column artifact: 4+ spaces → single space
    result = _re.sub(r' {4,}', ' ', result)

    # OCR hyphenation: word-\nnewword → wordnewword
    result = _re.sub(r'(\w)-\n(\w)', r'\1\2', result)

    # Remove lone page numbers and duplicate consecutive lines
    lines = result.split('\n')
    filtered_lines = []
    prev_stripped = None
    for line in lines:
        stripped = line.strip()
        if _re.match(r'^\d{1,4}$', stripped):
            corrections.append(f"removed page number: {stripped!r}")
            continue
        if stripped and stripped == prev_stripped:
            corrections.append(f"removed duplicate: {stripped[:50]!r}")
            continue
        filtered_lines.append(line)
        if stripped:
            prev_stripped = stripped

    # Join mid-sentence line breaks (no terminal punct + next line starts lowercase)
    joined_lines = []
    i = 0
    while i < len(filtered_lines):
        line = filtered_lines[i]
        stripped = line.strip()
        if (i + 1 < len(filtered_lines)
                and stripped
                and stripped[-1] not in '.!?:;'
                and filtered_lines[i + 1].strip()
                and filtered_lines[i + 1].strip()[0].islower()):
            joined_lines.append(stripped + ' ' + filtered_lines[i + 1].strip())
            corrections.append("joined mid-sentence line break")
            i += 2
        else:
            joined_lines.append(line)
            i += 1

    result = '\n'.join(joined_lines)
    result = _re.sub(r'\n{3,}', '\n\n', result)
    return result.strip(), corrections


def _clean_ingredient_name(name):
    """Strip cookbook editorial refs, page citations, and trailing punctuation from ingredient names."""
    import re as _re2
    s = (name or "").strip()
    # "see Yuca con Mojo [page 119]" / "(see Tips ...)" / "[page N]" / "(page N)"
    s = _re2.sub(r'\s*[\[(]?see\s+[^\])\n]+[\])]?', '', s, flags=_re2.IGNORECASE).strip()
    s = _re2.sub(r'\s*\[page\s+\d+\]', '', s, flags=_re2.IGNORECASE).strip()
    s = _re2.sub(r'\s*\(page\s+\d+\)', '', s, flags=_re2.IGNORECASE).strip()
    # trailing lone parenthetical that is just a measure echo e.g. " (2 tsp)" / "(optional)"
    s = _re2.sub(r'\s*\(\s*\d[\d/\s]*\s*\w{1,5}\s*\)\s*$', '', s).strip()
    # trailing commas / semicolons / stray whitespace
    s = s.rstrip(',;').strip()
    return s or name  # never return empty — fall back to original if over-stripped


def _count_to_float(s):
    """Parse any count string to float: integer, decimal, 'a/b', or 'a b/c'."""
    s = (s or "").strip()
    try:
        from fractions import Fraction
        if " " in s and "/" in s:
            whole, frac = s.split(" ", 1)
            return float(whole) + float(Fraction(frac))
        if "/" in s:
            return float(Fraction(s))
        return float(s)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def _convert_to_metric(ingredients):
    """Convert imperial measurements to metric-primary with imperial in parens.
    Returns (converted_ingredients, source_units_raw, quality_warnings)."""
    source_units_raw = [dict(ing) if isinstance(ing, dict) else ing for ing in ingredients]
    converted = []
    has_imperial = False
    has_metric = False

    for ing in ingredients:
        if not isinstance(ing, dict):
            converted.append(ing)
            continue

        new_ing = dict(ing)
        unit = (ing.get('unit') or '').strip().lower()
        count_str = str(ing.get('count') or '').strip()

        if unit in UNIT_CONVERSIONS:
            metric_unit, factor = UNIT_CONVERSIONS[unit]
            count_val = _count_to_float(count_str)
            if count_val is not None:
                metric_val = count_val * factor
                rounded = round(metric_val / 5) * 5 if metric_val > 20 else round(metric_val, 1)
                imperial_str = f"{count_str} {unit}"
                new_ing['unit'] = metric_unit
                new_ing['count'] = str(int(rounded) if rounded == int(rounded) else rounded)
                existing_info = new_ing.get('info', '') or ''
                new_ing['info'] = (f"{existing_info} ({imperial_str})".strip())
                has_imperial = True
        elif unit in ('g', 'kg', 'ml', 'l', 'cl', 'dl'):
            has_metric = True

        converted.append(new_ing)

    quality_warnings = []
    if has_imperial and has_metric:
        quality_warnings.append({
            "type": "mixed_units",
            "detail": "Recipe mixes imperial and metric measurements",
        })

    return converted, source_units_raw, quality_warnings


def _parse_yield(servings_raw):
    """Parse servings JSONB array → (servings_text: str, servings_count: int|None)."""
    if not servings_raw:
        return None, None

    if isinstance(servings_raw, list) and servings_raw:
        first = servings_raw[0]
        if isinstance(first, dict):
            count_str = str(first.get('count') or '').strip()
            unit_str = (first.get('unit') or '').strip()
            raw_str = f"{count_str} {unit_str}".strip()
        else:
            raw_str = str(first)
            count_str = raw_str
            unit_str = ''
    else:
        raw_str = str(servings_raw)
        count_str = raw_str
        unit_str = ''

    raw_lower = raw_str.lower()

    yield_patterns = [
        (_re.compile(r'makes?\s+~?(\d+)\s*(ml|g|jar|cup|jars|cups)', _re.I),
         lambda m: (f"Makes ~{m.group(1)}{m.group(2)}", None)),
        (_re.compile(r'makes?\s+(\d+)', _re.I),
         lambda m: (f"Makes {m.group(1)}", int(m.group(1)))),
        (_re.compile(r'yields?\s+(\d+)', _re.I),
         lambda m: (f"Yields {m.group(1)}", int(m.group(1)))),
        (_re.compile(r'serves?\s+(\d+)(?:\s*[-\u2013]\s*(\d+))?', _re.I),
         lambda m: (
             f"Serves {m.group(1)}–{m.group(2)}" if m.group(2) else f"Serves {m.group(1)}",
             int(m.group(1))
         )),
        (_re.compile(r'(\d+)\s+to\s+(\d+)\s+(?:servings?|serves?)', _re.I),
         lambda m: (f"{m.group(1)} to {m.group(2)} servings", int(m.group(1)))),
        (_re.compile(r'(\d+)(?:\s*[-\u2013]\s*(\d+))?\s+(?:servings?|serves?)', _re.I),
         lambda m: (
             f"{m.group(1)}–{m.group(2)} servings" if m.group(2)
             else f"{m.group(1)} serving{'s' if int(m.group(1)) != 1 else ''}",
             int(m.group(1))
         )),
        (_re.compile(r'(\d+)\s+portions?', _re.I),
         lambda m: (f"{m.group(1)} portions", int(m.group(1)))),
        (_re.compile(r'feeds?\s+(\d+)', _re.I),
         lambda m: (f"Feeds {m.group(1)}", int(m.group(1)))),
    ]

    for pattern, handler in yield_patterns:
        m = pattern.search(raw_lower)
        if m:
            return handler(m)

    # Fallback: try to extract number directly from count_str
    try:
        count_int = int(float(count_str))
        label = unit_str if unit_str and unit_str not in ('serve', 'serves') \
            else ('serving' if count_int == 1 else 'servings')
        return f"{count_int} {label}", count_int
    except (ValueError, TypeError):
        pass

    return raw_str.strip() or None, None


def _add_step_insights(title, ingredients, steps):
    """Add professional insights to steps WITHOUT rewriting them.
    Returns list of {original_step, enhanced_step (verbatim), insight, matched_techniques}."""
    if not steps:
        return []

    ingredient_block = "\n".join(f"- {ing}" for ing in ingredients)
    result_steps = []

    insight_system = (
        "You are a culinary annotation engine. For each recipe step, write a 1–2 sentence "
        "professional insight explaining the underlying technique principle. "
        "Do NOT rewrite the step. Do NOT add steps. "
        'Return JSON: {"insight": "..."}'
    )

    for i, step_text in enumerate(steps):
        matched = _match_techniques_for_step(step_text)

        technique_block = ""
        if matched:
            parts = [
                f"Technique: {t['name']}\nKey principles: {t['key_principles']}\nPro tips: {t['pro_tips']}"
                for t in matched
            ]
            technique_block = "\n\nMatched technique references:\n" + "\n---\n".join(parts)

        user_prompt = (
            f"Recipe: {title}\n\nIngredients:\n{ingredient_block}\n\n"
            f"Step {i + 1}: {step_text}"
            f"{technique_block}\n\n"
            "Write a 1–2 sentence professional insight for this step only. "
            'Return JSON: {"insight": "..."}'
        )

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=insight_system,
                messages=[{"role": "user", "content": user_prompt}],
            )
            resp_text = response.content[0].text.strip()
            if resp_text.startswith("```"):
                lines = resp_text.split("\n")
                resp_text = "\n".join(lines[1:-1] if lines and lines[-1].strip() == "```" else lines[1:])
            insight = json.loads(resp_text).get("insight", "")
        except Exception:
            insight = ""

        result_steps.append({
            "original_step": step_text,
            "enhanced_step": step_text,   # verbatim — never rewritten
            "insight": insight,
            "matched_techniques": [t["name"] for t in matched],
        })

    return result_steps


def _enhance_recipe_structure(title, ingredients_text, steps_text):
    """Generate recipe-level structural metadata. Returns dict."""
    prompt = (
        f"You are a culinary intelligence engine. Analyse this recipe and return structural metadata.\n"
        f"You may NOT modify the steps or ingredients. You add structural metadata only.\n"
        f"Flag errors in quality_warnings — do not silently correct them.\n\n"
        f"Recipe: {title}\n\nIngredients:\n{ingredients_text}\n\nSteps:\n{steps_text}\n\n"
        'Return ONLY valid JSON — no markdown fences:\n'
        '{\n'
        '  "cuisine": "short label — 1 or 2 words, lowercase (e.g. \\"british\\", \\"japanese\\", \\"eastern mediterranean\\"); null if uncertain",\n'
        '  "origin": "1–2 sentence geographic/historical placement",\n'
        '  "quality_hierarchy": [\n'
        '    {"ingredient": "name", "reserve": "best-quality option", "house": "everyday option", "swap_cost": "what you lose"}\n'
        '  ],\n'
        '  "sensory_tests": [\n'
        '    {"sense": "visual|aroma|texture|taste|sound", "cue": "...", "fail_indicator": "..."}\n'
        '  ],\n'
        '  "cross_cuisine_parallels": [\n'
        '    {"cuisine": "...", "dish": "...", "mechanism": "..."}\n'
        '  ],\n'
        '  "flavour_context": "Food-science reasoning. No waffle.",\n'
        '  "lives_or_dies": "The one principle this dish stands or falls on. One sentence.",\n'
        '  "quality_warnings": [{"section": "ingredients|method|general", "message": "one-line issue description"}],\n'
        '  "ingredient_origin_markers": [\n'
        '    {"ingredient_name": "name from recipe", "origin_marker": "1 sentence on provenance"}\n'
        '  ]\n'
        '}\n\n'
        'quality_warnings: flag contradictory storage, mixed units, step reference gaps, fragments — each as {"section": "ingredients|method|general", "message": "..."}. '
        'Empty array if clean. Return 2–4 sensory_tests. '
        'ingredient_origin_markers: only ingredients with a meaningful origin story.'
    )
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")
            resp_text = "\n".join(lines[1:-1] if lines and lines[-1].strip() == "```" else lines[1:])
        return json.loads(resp_text)
    except Exception as e:
        app.logger.warning(f"[_enhance_recipe_structure] failed: {e}")
        return {}


# ── Pairing constraint constants ──────────────────────────────────────────────
_GENERIC_NAME_RE = _re.compile(
    r"^(beer(\s+(ale|lager|stout|porter|ipa|pilsner))?|sake|wines?|red\s+wine|white\s+wine|"
    r"ros[eé]|spirits?|tea|coffee|kombucha|sparkling\s+wine|mocktail|soft\s+drink)$",
    _re.IGNORECASE,
)
_ALCOHOLIC_CATS = frozenset({
    "red_wine", "white_wine", "sparkling_wine", "rosé", "rose",
    "sake", "beer", "spirit_cocktail",
})
_TIER_DEFAULTS = ["complement", "bridge", "contrast"]


def _enrich_beverage_pairings(title, ingredients_text=""):
    """LLM-based pairing generation at import time.

    Three hard constraints enforced with post-validation + one re-prompt:
    1. Non-alcoholic floor  — at least one of three pairings is non-alcoholic.
    2. Category diversity   — no two pairings share a category.
    3. Specific named drinks — name must be producer + product, never a bare label.
    Returns list of 3 dicts conforming to the pairings_for_recipe template schema.
    Non-compliant slots on final failure get name=None → template shows placeholder.
    """
    SYSTEM = (
        "You are a professional sommelier and beverage curator for Provenance, a culinary platform.\n"
        "Generate exactly three beverage pairings for a recipe. Follow ALL THREE rules:\n\n"
        "RULE 1 — NON-ALCOHOLIC FLOOR: At least one pairing must be non-alcoholic. "
        "Suitable: tea (sencha, hojicha, oolong, genmaicha, buckwheat tea), coffee, kombucha, "
        "herbal soda, sparkling water with culinary garnish, mocktail.\n\n"
        "RULE 2 — CATEGORY DIVERSITY: Each pairing must use a different category. "
        "Valid categories: red_wine, white_wine, sparkling_wine, rosé, sake, beer, "
        "spirit_cocktail, tea, coffee, soft_drink, mocktail, kombucha.\n\n"
        "RULE 3 — SPECIFIC NAMED DRINKS: Every name must be a real specific drink — "
        "producer + product name (e.g. 'Domaine Weinbach Riesling Cuvée Théo', "
        "'En Nichi Hojicha Roasted Green Tea'). "
        "Never use a bare category label such as 'sake', 'beer ale', or 'tea'. "
        "If you cannot name a specific drink with high confidence, return null for that name.\n\n"
        "Label by slot: slot 0 = complement, slot 1 = bridge, slot 2 = contrast.\n\n"
        "Example — Bouillabaisse (Provençal fish stew, saffron, rouille):\n"
        "[\n"
        '  {"name": "Château Simone Palette Blanc", "category": "white_wine", '
        '"pairing_type": "complement", '
        '"tasting_note": "Clairette and Grenache Blanc from Palette AOC — saline minerality '
        'mirrors the saffron broth; weight holds against the rouille."},\n'
        '  {"name": "Kizakura Josen Ginjo", "category": "sake", "pairing_type": "bridge", '
        '"tasting_note": "Light umami backbone from Fushimi water ties to the shellfish stock; '
        'the rice sweetness echoes the fennel."},\n'
        '  {"name": "Mariage Frères Thé du Hammam", "category": "tea", '
        '"pairing_type": "contrast", '
        '"tasting_note": "Gunpowder green with rose and citrus — cuts the saffron heat; '
        'serve at 80°C alongside or after."}\n'
        "]\n\n"
        "Return ONLY valid JSON — a list of exactly 3 objects. "
        "No markdown fences. No text outside the array."
    )

    def _call(user_content):
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=700,
            system=SYSTEM,
            messages=[{"role": "user", "content": user_content}],
        )
        raw = resp.content[0].text.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        return json.loads(raw)

    def _violations(pairings):
        if not isinstance(pairings, list) or len(pairings) != 3:
            return ["not a list of 3"]
        cats, flags = [], []
        has_na = False
        for p in pairings:
            name = (p.get("name") or "").strip()
            cat = (p.get("category") or "").lower().strip()
            if name and _GENERIC_NAME_RE.match(name):
                flags.append(f"generic name {name!r}")
            if cat not in _ALCOHOLIC_CATS:
                has_na = True
            cats.append(cat)
        if not has_na:
            flags.append("all alcoholic")
        if len(set(cats)) < 3:
            flags.append(f"duplicate categories {cats}")
        return flags

    def _to_schema(pairings):
        result = []
        for i, p in enumerate(pairings[:3]):
            name = (p.get("name") or "").strip() or None
            if name and _GENERIC_NAME_RE.match(name):
                name = None
            cat = (p.get("category") or "").lower().replace(" ", "_")
            tier = (p.get("pairing_type") or _TIER_DEFAULTS[i]).lower()
            result.append({
                "beverage_name": name,
                "beverage_style": name or "",
                "beverage_category": cat,
                "beverage_description": (p.get("tasting_note") or "").strip(),
                "flavour_logic": "",
                "pairing_type": tier,
                "tier_label": tier.upper(),
                "confidence": "editorial",
                "source": "llm_generated",
                "beverage_product_id": None,
                "pantry_url": None,
            })
        # Pad to 3 with null slots if response was short
        null_tiers = ["COMPLEMENT", "BRIDGE", "CONTRAST"]
        while len(result) < 3:
            i = len(result)
            result.append({
                "beverage_name": None, "beverage_style": "",
                "beverage_category": "", "beverage_description": "",
                "flavour_logic": "", "pairing_type": _TIER_DEFAULTS[i],
                "tier_label": null_tiers[i], "confidence": "",
                "source": "llm_generated",
                "beverage_product_id": None, "pantry_url": None,
            })
        return result

    try:
        base_msg = f"Recipe: {title}"
        if ingredients_text:
            base_msg += f"\n\nKey ingredients:\n{ingredients_text[:600]}"

        pairings = _call(base_msg)
        v = _violations(pairings)
        if v:
            app.logger.info(f"[_enrich_beverage_pairings] first-pass violations: {v} — re-prompting")
            retry_msg = (
                f"{base_msg}\n\nYour previous response had these issues: {'; '.join(v)}. "
                "Fix them: (1) include at least one non-alcoholic category, "
                "(2) use three different categories, (3) use specific producer+product names."
            )
            pairings = _call(retry_msg)
            v2 = _violations(pairings)
            if v2:
                app.logger.warning(f"[_enrich_beverage_pairings] second-pass violations: {v2} — nulling bad slots")
                for p in pairings:
                    n = (p.get("name") or "").strip()
                    if n and _GENERIC_NAME_RE.match(n):
                        p["name"] = None
        return _to_schema(pairings)
    except Exception as e:
        app.logger.warning(f"[_enrich_beverage_pairings] failed: {e}")
        return []


def _enrich_time_estimates(title, ingredients_text, steps_text, existing_active="", existing_total=""):
    """Estimate active/total time via Haiku if either field is blank.
    Returns (active_text, total_text) — either value is None if already set."""
    if existing_active and existing_total:
        return None, None
    prompt = (
        f"You are a culinary timing expert. Estimate preparation times for this recipe.\n"
        f"Recipe: {title}\n\nIngredients:\n{ingredients_text}\n\nSteps:\n{steps_text}\n\n"
        "Return ONLY valid JSON with no markdown fences:\n"
        '{"active_time": "X mins", "total_time": "Y hours Z mins"}\n\n'
        "active_time = hands-on prep + cooking time. "
        "total_time = active_time + inactive time (marinating, resting, chilling). "
        'Use "X mins" for under 1 hour, "X hr Y mins" for 1+ hours. '
        "If total equals active, repeat the value."
    )
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=80,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")
            resp_text = "\n".join(lines[1:-1] if lines and lines[-1].strip() == "```" else lines[1:])
        d = json.loads(resp_text)
        active_out = d.get("active_time") if not existing_active else None
        total_out  = d.get("total_time")  if not existing_total  else None
        return active_out, total_out
    except Exception as e:
        app.logger.warning(f"[_enrich_time_estimates] failed: {e}")
        return None, None


def _enrich_faqs(title, ingredients_text, steps_text):
    """Generate 3–5 cook's FAQs via Haiku. Returns [{q, a}] list."""
    prompt = (
        f"You are a culinary instructor. Generate 3 to 5 practical cook's questions and answers "
        f"for this recipe.\n"
        f"Recipe: {title}\n\nIngredients:\n{ingredients_text}\n\nSteps:\n{steps_text}\n\n"
        "Focus on common mistakes, substitutions, make-ahead tips, and technique clarifications.\n"
        "Return ONLY valid JSON with no markdown fences:\n"
        '[{"q": "...", "a": "..."}, ...]\n\n'
        "Keep answers under 50 words. No waffle. Practical only."
    )
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        resp_text = response.content[0].text.strip()
        if resp_text.startswith("```"):
            lines = resp_text.split("\n")
            resp_text = "\n".join(lines[1:-1] if lines and lines[-1].strip() == "```" else lines[1:])
        result = json.loads(resp_text)
        if isinstance(result, list):
            return [{"q": str(i.get("q", "")), "a": str(i.get("a", ""))} for i in result if i.get("q")]
        return []
    except Exception as e:
        app.logger.warning(f"[_enrich_faqs] failed: {e}")
        return []


def _match_suppliers_for_ingredients(ingredient_names):
    """Reusable supplier matching. Returns list of supplier dicts with products[].

    Mirrors canon recipe page Path B guards: forward-only ILIKE, _FORM_WORDS
    disqualifier, and _match_ok() 60%-coverage check.
    """
    if not ingredient_names or not DATABASE_URL:
        return []
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        names = [n for n in ingredient_names[:20] if n]
        patterns = [f"%{n}%" for n in names]
        cur.execute("""
            SELECT DISTINCT ON (s.id, ip.name)
                s.id, s.name, s.website, s.city, s.state_province, s.country,
                ip.name AS product_name,
                LEFT(ip.description, 140) AS product_desc
            FROM ingredient_products ip
            JOIN product_suppliers ps ON ip.id = ps.product_id
            JOIN suppliers s ON ps.supplier_id = s.id
            WHERE ip.name ILIKE ANY(%s)
            ORDER BY s.id, ip.name, s.name
        """, (patterns,))
        rows = cur.fetchall()

        _FORM_WORDS = {"paste", "powder", "aged", "dried", "smoked", "fermented"}

        def _match_ok(ing, prod):
            il, pl = ing.lower(), prod.lower()
            for fw in _FORM_WORDS:
                if fw in pl and fw not in il:
                    return False
            shorter = min(len(il), len(pl))
            return shorter > 0 and len(il) / shorter >= 0.6

        supplier_map = {}
        for row in rows:
            prod_name = row['product_name'] or ''
            if not any(_match_ok(ing, prod_name) for ing in names):
                continue
            sid = row['id']
            if sid not in supplier_map:
                supplier_map[sid] = {
                    'id': sid, 'name': row['name'], 'website': row['website'],
                    'city': row['city'], 'state_province': row['state_province'],
                    'country': row['country'], 'products': [],
                }
            if prod_name:
                supplier_map[sid]['products'].append({
                    'name': prod_name,
                    'desc': row['product_desc'] or '',
                })
        cur.close()
        conn.close()
        return list(supplier_map.values())
    except Exception as e:
        app.logger.warning(f"[_match_suppliers_for_ingredients] failed: {e}")
        return []


def _supplier_in_region(row, region_code):
    """True if supplier is T1 for the given region code (or region_code is None → show all)."""
    if not region_code:
        return True  # global user: show all providers
    state = row.get("state_province") or ""
    svc   = row.get("service_region") or []
    _WESTERN_CA = {"BC", "AB", "SK", "MB"}
    if state == region_code:
        return True
    if region_code in svc:
        return True
    if region_code in _WESTERN_CA and "Western_Canada" in svc:
        return True
    return False


def _get_kitchen_recipe_suppliers_from_markers(recipe_dict, user_loc="global"):
    """
    Build the Sourced section from the recipe's pre-resolved ingredient_origin_markers.
    Each marker carries the supplier objects (id, name, city, state_province, country,
    website, products) that were resolved at import time. We collect supplier IDs from
    the markers, apply a pantry stop list and stem-based product filter, then do a
    single DB query for role + service_region to classify ORIGIN vs PROVIDER.

    Marker shape (from DB):
      [{"ingredient_name": "Fresh-As Manuka Honey Chunk",
        "suppliers": [{"id": 19, "name": "Purely Artisan Foods", ...}]}, ...]

    Returns: {"origin": [supplier_dict, ...], "providers": [supplier_dict, ...]}
    Paste 32.
    """
    if not DATABASE_URL:
        return {"origin": [], "providers": []}

    markers = recipe_dict.get("ingredient_origin_markers") or []
    if not markers:
        return {"origin": [], "providers": []}

    region_code = None
    if user_loc and user_loc != "global":
        parts = user_loc.split("-", 1)
        if len(parts) == 2:
            region_code = parts[1]

    # ── Pantry stop list — never meaningful as sourced ingredients ─────────────
    _PANTRY_STOP = {
        "water", "salt", "kosher salt", "sea salt", "flaky sea salt", "fine salt",
        "pepper", "black pepper", "cracked black pepper", "white pepper",
        "butter", "unsalted butter", "salted butter",
        "oil", "olive oil", "vegetable oil", "neutral oil",
        "flour", "all-purpose flour", "ap flour",
        "sugar", "granulated sugar", "white sugar",
        "ice", "ice water", "boiling water", "tamarind water",
    }

    # ── Helpers (same as paste 30 dedup layer, kept for product quality scoring) ─
    def _product_formality_score(product_name):
        n = (product_name or "").strip()
        if not n:
            return 0
        score = len(n)
        lower_n = n.lower()
        if lower_n.startswith("fresh-as"):
            score += 50
        if lower_n.startswith("freeze-dried"):
            score += 30
        if "(" in n and ")" in n:
            score += 20
        if n[0].isupper():
            score += 5
        return score

    def _ingredient_stem_local(product_name):
        """Strip brand prefix + form suffix + plurals to reveal core ingredient."""
        n = (product_name or "").lower().strip()
        for prefix in ("fresh-as ", "freeze-dried ", "fresh as "):
            if n.startswith(prefix):
                n = n[len(prefix):]
                break
        for suffix in (" chunks", " chunk", " powder", " whole", " flakes", " flake",
                       " juice", " sauce", " extract"):
            if n.endswith(suffix):
                n = n[:-len(suffix)]
                break
        if n.endswith("ies") and len(n) > 4:
            n = n[:-3] + "y"
        elif n.endswith("es") and len(n) > 3 and not n.endswith("oes"):
            n = n[:-2]
        elif n.endswith("s") and len(n) > 2 and not n.endswith("ss") and not n.endswith("us"):
            n = n[:-1]
        return n.strip()

    # ── Read markers: collect supplier_id → set of ingredient names ───────────
    # Marker shape: {"ingredient_name": "...", "suppliers": [{"id": N, ...}]}
    supplier_ingredients = {}  # sid -> set of ingredient names this supplier is linked to

    for m in markers:
        if not isinstance(m, dict):
            continue
        ing_name = (m.get("ingredient_name") or "").strip()
        if not ing_name or ing_name.lower() in _PANTRY_STOP:
            continue
        for s in (m.get("suppliers") or []):
            if not isinstance(s, dict):
                continue
            sid = s.get("id")
            if not sid:
                continue
            try:
                sid = int(sid)
            except (TypeError, ValueError):
                continue
            if sid not in supplier_ingredients:
                supplier_ingredients[sid] = set()
            supplier_ingredients[sid].add(ing_name)

    if not supplier_ingredients:
        return {"origin": [], "providers": []}

    supplier_ids = list(supplier_ingredients.keys())

    # ── Pre-compute ingredient stems per supplier ──────────────────────────────
    # Used to filter which products to show: product_stem must overlap with
    # at least one ingredient stem for that supplier in this recipe.
    supplier_ingredient_stems = {}
    for sid, ing_names in supplier_ingredients.items():
        stems = set()
        for n in ing_names:
            st = _ingredient_stem_local(n)
            if st:
                stems.add(st)
        supplier_ingredient_stems[sid] = stems

    def _product_matches_recipe(product_name, ingredient_stems):
        """True if product_stem overlaps with any ingredient_stem (substring check)."""
        pstem = _ingredient_stem_local(product_name)
        if not pstem:
            return False
        for istem in ingredient_stems:
            if pstem == istem or pstem in istem or istem in pstem:
                return True
        return False

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # One DB query: role + service_region + product catalog per supplier
        cur.execute("""
            SELECT
                s.id, s.name, s.website, s.city, s.state_province, s.country,
                s.service_region,
                ps.role, ps.is_primary,
                ip.name AS matched_product_name,
                LEFT(ip.description, 200) AS product_desc
            FROM suppliers s
            LEFT JOIN product_suppliers ps ON ps.supplier_id = s.id
            LEFT JOIN ingredient_products ip ON ip.id = ps.product_id
            WHERE s.id = ANY(%s)
              AND s.is_active = TRUE
            ORDER BY s.id, ps.role, ps.is_primary DESC NULLS LAST, ip.name
        """, (supplier_ids,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        origin_map = {}
        provider_map = {}

        for row in rows:
            sid = row["id"]
            role = row.get("role")
            pname = row.get("matched_product_name")

            # Precision filter: only include products whose stem overlaps with
            # the ingredient names this supplier is linked to in this recipe.
            if pname and not _product_matches_recipe(
                pname, supplier_ingredient_stems.get(sid, set())
            ):
                continue

            if role == "ORIGIN":
                target_map = origin_map
                eligible = True
            elif role == "PROVIDER":
                target_map = provider_map
                eligible = _supplier_in_region(row, region_code)
            else:
                # Supplier present in markers but no product_suppliers rows yet
                target_map = provider_map
                eligible = _supplier_in_region(row, region_code)

            if not eligible:
                continue

            if sid not in target_map:
                target_map[sid] = {
                    "id": sid, "name": row["name"], "website": row["website"],
                    "city": row["city"], "state_province": row["state_province"],
                    "country": row["country"],
                    "_products_by_stem": {},
                }

            if pname:
                stem = _ingredient_stem_local(pname)
                score = _product_formality_score(pname)
                by_stem = target_map[sid]["_products_by_stem"]
                if stem not in by_stem or score > by_stem[stem]["_score"]:
                    by_stem[stem] = {
                        "name": pname,
                        "desc": row["product_desc"] or "",
                        "_score": score,
                    }

        # Flatten _products_by_stem → products list
        for sup in list(origin_map.values()) + list(provider_map.values()):
            sup["products"] = [
                {"name": v["name"], "desc": v["desc"]}
                for v in sup["_products_by_stem"].values()
            ]
            del sup["_products_by_stem"]

        return {"origin": list(origin_map.values()), "providers": list(provider_map.values())}
    except Exception as e:
        app.logger.warning(f"[_get_kitchen_recipe_suppliers_from_markers] failed: {e}")
        return {"origin": [], "providers": []}


def _get_kitchen_recipe_suppliers_LEGACY_DO_NOT_USE(ingredient_names, user_loc="global"):
    """
    LEGACY — superseded by _get_kitchen_recipe_suppliers_from_markers (paste 32).
    Kept for reference during supplier infrastructure rework. DO NOT CALL.

    Fetch Origin (benchmark) and Provider (local) suppliers for a kitchen recipe.
    Returns: {"origin": [supplier_dict, ...], "providers": [supplier_dict, ...]}

    Origin   = ps.role='ORIGIN' — region-agnostic, global benchmark reference
    Provider = ps.role='PROVIDER' — hard-filtered to user's T1 region:
               s.state_province matches user's region code, OR
               region code appears explicitly in s.service_region (NOT nationwide_ umbrella)

    Paste 22: T1 region filter.
    Paste 29: full products list per supplier.
    Paste 31: Python whole-word precision filter; SQL kept simple (ILIKE); pantry stop-list.
    """
    if not ingredient_names or not DATABASE_URL:
        return {"origin": [], "providers": []}

    region_code = None
    if user_loc and user_loc != "global":
        parts = user_loc.split("-", 1)
        if len(parts) == 2:
            region_code = parts[1]  # e.g. "BC", "WA"

    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        names = [n for n in ingredient_names[:20] if n]

        # ── Pantry-basic stop list ─────────────────────────────────────────────
        # These are never sourced as branded products and generate false matches.
        _PANTRY_STOP = {
            "water", "salt", "kosher salt", "sea salt", "flaky sea salt", "fine salt",
            "pepper", "black pepper", "cracked black pepper", "white pepper",
            "butter", "unsalted butter", "salted butter",
            "oil", "olive oil", "vegetable oil", "neutral oil",
            "flour", "all-purpose flour", "ap flour",
            "sugar", "granulated sugar", "white sugar",
            "ice", "ice water", "boiling water",
        }
        names = [n for n in names if n.strip().lower() not in _PANTRY_STOP]
        if not names:
            cur.close()
            conn.close()
            return {"origin": [], "providers": []}

        # ── Helpers: formal-name preference dedup ─────────────────────────────
        def _product_formality_score(product_name):
            """Higher = more formal. Branded/longer names rank above generic stubs."""
            n = (product_name or "").strip()
            if not n:
                return 0
            score = len(n)
            lower_n = n.lower()
            if lower_n.startswith("fresh-as"):
                score += 50
            if lower_n.startswith("freeze-dried"):
                score += 30
            if "(" in n and ")" in n:
                score += 20
            if n[0].isupper():
                score += 5
            return score

        def _ingredient_stem(product_name):
            """Strip brand prefixes, form suffixes, and plurals to reveal the core ingredient."""
            n = (product_name or "").lower().strip()
            for prefix in ("fresh-as ", "freeze-dried ", "fresh as "):
                if n.startswith(prefix):
                    n = n[len(prefix):]
                    break
            for suffix in (" chunks", " chunk", " powder", " whole", " flakes", " flake"):
                if n.endswith(suffix):
                    n = n[:-len(suffix)]
                    break
            # Simple plural normalisation — raspberries→raspberry, flakes→flake, etc.
            if n.endswith("ies") and len(n) > 4:
                n = n[:-3] + "y"
            elif n.endswith("es") and len(n) > 3 and not n.endswith("oes"):
                n = n[:-2]
            elif n.endswith("s") and len(n) > 2 and not n.endswith("ss") and not n.endswith("us"):
                n = n[:-1]
            return n.strip()

        # ── Step 1: broad-match SQL — cast a wide net with ILIKE ──────────────
        # SQL is intentionally permissive. Python filters for precision below.
        patterns = [f"%{n}%" for n in names]
        cur.execute("""
            SELECT DISTINCT ip.id AS product_id, ip.name AS product_name
            FROM ingredient_products ip
            WHERE ip.name ILIKE ANY(%s)
               OR EXISTS (
                   SELECT 1 FROM unnest(%s::text[]) AS ri(nm)
                   WHERE ri.nm ILIKE '%%' || ip.name || '%%'
               )
        """, (patterns, names))
        product_rows = cur.fetchall()
        product_ids = [r["product_id"] for r in product_rows]
        product_id_to_name = {r["product_id"]: r["product_name"] for r in product_rows}

        if not product_ids:
            cur.close()
            conn.close()
            return {"origin": [], "providers": []}

        # ── Python precision filter ────────────────────────────────────────────
        # SQL matched substrings (e.g. "water" → "watermelon"). Python filters by
        # whole significant-word overlap so only genuine matches survive.
        def _normalize_for_match(text):
            return _re.sub(r'[^\w\s\-]', ' ', (text or '').lower())

        def _significant_words(text, min_len=4):
            _STOP_WORDS = {
                'with', 'from', 'into', 'about', 'each', 'small', 'medium',
                'large', 'whole', 'half', 'plus', 'more', 'less', 'than',
                'when', 'where', 'which', 'recipe', 'recipes', 'ingredient',
                'ingredients', 'cooking', 'roast', 'roasted', 'piece', 'pieces',
                'powder', 'flake', 'flakes', 'chunk', 'chunks',
            }
            words = _re.findall(r'\b[a-z][a-z\-]{' + str(min_len - 1) + r',}\b',
                                _normalize_for_match(text))
            return {w for w in words if w not in _STOP_WORDS}

        recipe_words = set()
        for ing_name in names:
            recipe_words |= _significant_words(ing_name)

        filtered_product_ids = [
            pid for pid in product_ids
            if bool(_significant_words(product_id_to_name.get(pid, '')) & recipe_words)
        ]

        if not filtered_product_ids:
            cur.close()
            conn.close()
            return {"origin": [], "providers": []}

        # ── Step 2: fetch ORIGIN + PROVIDER suppliers for those products ───────
        cur.execute("""
            SELECT
                s.id, s.name, s.website, s.city, s.state_province, s.country,
                s.service_region,
                ps.role, ps.is_primary,
                ip.name AS matched_product_name,
                LEFT(ip.description, 200) AS product_desc
            FROM ingredient_products ip
            JOIN product_suppliers ps ON ip.id = ps.product_id
            JOIN suppliers s ON ps.supplier_id = s.id
            WHERE ip.id = ANY(%s)
              AND s.is_active = TRUE
            ORDER BY s.id, ps.role, ps.is_primary DESC NULLS LAST, ip.name
        """, (filtered_product_ids,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        origin_map = {}
        provider_map = {}
        for row in rows:
            sid = row["id"]
            role = row["role"]
            pname = row["matched_product_name"]

            if role == "ORIGIN":
                target_map = origin_map
                eligible = True
            elif role == "PROVIDER":
                target_map = provider_map
                eligible = _supplier_in_region(row, region_code)
            else:
                continue

            if not eligible:
                continue

            if sid not in target_map:
                target_map[sid] = {
                    "id": sid, "name": row["name"], "website": row["website"],
                    "city": row["city"], "state_province": row["state_province"],
                    "country": row["country"],
                    "_products_by_stem": {},
                }

            if pname:
                stem = _ingredient_stem(pname)
                score = _product_formality_score(pname)
                by_stem = target_map[sid]["_products_by_stem"]
                if stem not in by_stem or score > by_stem[stem]["_score"]:
                    by_stem[stem] = {
                        "name": pname,
                        "desc": row["product_desc"] or "",
                        "_score": score,
                    }

        # Flatten _products_by_stem → products list, drop helper key
        for sup in list(origin_map.values()) + list(provider_map.values()):
            sup["products"] = [
                {"name": v["name"], "desc": v["desc"]}
                for v in sup["_products_by_stem"].values()
            ]
            del sup["_products_by_stem"]

        return {"origin": list(origin_map.values()), "providers": list(provider_map.values())}
    except Exception as e:
        app.logger.warning(f"[_get_kitchen_recipe_suppliers_LEGACY] failed: {e}")
        return {"origin": [], "providers": []}


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
    """Delegates to _add_step_insights(). Returns (step_strings, step_objects) or None on failure."""
    if not steps:
        return None
    try:
        objects = _add_step_insights(title, ingredients, steps)
        strings = [s["original_step"] for s in objects]
        return (strings, objects)
    except Exception:
        return None


def _build_recipe_user_msg(title, ingredients, method_steps):
    msg = f"Recipe: {title}\n\nIngredients:\n"
    for ing in ingredients:
        msg += f"- {ing}\n"
    msg += "\nMethod:\n"
    for i, step in enumerate(method_steps, 1):
        msg += f"{i}. {step}\n"
    return msg


def _recipe_dict_to_haccp_inputs(d):
    """Extract flat text strings from a recipe dict for _detect_raw_served."""
    content = d.get("recipe_content_jsonb") or {}
    raw_ings = d.get("ingredients") or content.get("ingredients") or []
    if isinstance(raw_ings, str):
        try:
            raw_ings = json.loads(raw_ings)
        except Exception:
            raw_ings = []
    ingredients = []
    for ing in (raw_ings if isinstance(raw_ings, list) else []):
        if isinstance(ing, dict):
            name = str(ing.get("name") or "").strip()
            qty = str(ing.get("qty") or ing.get("quantity") or "").strip()
            line = " ".join(filter(None, [qty, name]))
            if line:
                ingredients.append(line)
        elif isinstance(ing, str) and ing.strip():
            ingredients.append(ing.strip())
    steps_raw = d.get("enhanced_steps") or d.get("steps") or content.get("steps") or []
    if isinstance(steps_raw, str):
        try:
            steps_raw = json.loads(steps_raw)
        except Exception:
            steps_raw = []
    method_steps = []
    for s in (steps_raw if isinstance(steps_raw, list) else []):
        if isinstance(s, dict):
            text = (s.get("enhanced_step") or s.get("instruction") or s.get("text") or "").strip()
            if text:
                method_steps.append(text)
        elif isinstance(s, str) and s.strip():
            method_steps.append(s.strip())
    return ingredients, method_steps


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


# ── HACCP Structured Brief — Codex Alimentarius CXC 1-1969 ──

HACCP_ALLERGEN_REGIONS = {
    "US": {
        "label": "United States (Big 9)",
        "allergens": ["milk", "eggs", "fish", "crustacean_shellfish", "tree_nuts",
                      "peanuts", "wheat", "soy", "sesame"]
    },
    "EU": {
        "label": "European Union / United Kingdom (Big 14)",
        "allergens": ["cereals_containing_gluten", "crustaceans", "eggs", "fish",
                      "peanuts", "soybeans", "milk", "nuts", "celery", "mustard",
                      "sesame_seeds", "sulphites", "lupin", "molluscs"]
    },
    "CA": {
        "label": "Canada (Priority 11)",
        "allergens": ["eggs", "milk", "mustard", "peanuts", "crustaceans_molluscs",
                      "fish", "sesame", "soy", "sulphites", "tree_nuts", "wheat_triticale"]
    },
    "AU_NZ": {
        "label": "Australia / New Zealand (10)",
        "allergens": ["cereals_containing_gluten", "crustacea", "egg", "fish", "milk",
                      "peanuts", "sesame_seeds", "soybeans", "tree_nuts", "lupin"]
    }
}

HACCP_DEFAULT_REGION = "EU"
HACCP_SCHEMA_VERSION = "1.0"


def build_haccp_system_prompt(recipe_name, recipe_ingredients, allergen_region):
    region_info = HACCP_ALLERGEN_REGIONS.get(allergen_region, HACCP_ALLERGEN_REGIONS[HACCP_DEFAULT_REGION])
    region_allergens = ", ".join(region_info["allergens"])

    return f"""You are a HACCP (Hazard Analysis and Critical Control Point) consultant writing a brief for a working professional kitchen. Your output will be reviewed by health inspectors and used in a real food preparation environment.

FRAMEWORK: Codex Alimentarius CXC 1-1969 (General Principles of Food Hygiene), 7 HACCP principles, 12-step framework.

VOICE: Speak like a senior chef writing for the line. Direct. Specific. No filler. No reference to artificial intelligence, language models, or generation. The inspector should believe a HACCP-trained chef wrote this.

OUTPUT FORMAT: Return STRICT JSON only — no markdown fences, no preamble, no closing remarks. The JSON must validate against this exact schema:

{{
  "schema_version": "{HACCP_SCHEMA_VERSION}",
  "recipe_name": "string",
  "framework": "Codex Alimentarius CXC 1-1969",

  "allergens": {{
    "region": "{allergen_region}",
    "region_label": "{region_info['label']}",
    "detected": ["list", "of", "detected", "allergens", "from", "this", "region's", "list"],
    "rationale": "Brief one-sentence explanation of which ingredients triggered which allergens"
  }},

  "process_flow": [
    {{"id": "receiving", "label": "Receiving & Purchasing"}},
    {{"id": "storage", "label": "Storage"}},
    {{"id": "preparation", "label": "Preparation"}},
    {{"id": "cooking", "label": "Cooking"}},
    {{"id": "service", "label": "Hot Hold & Service"}}
  ],

  "receiving_criteria": [
    {{
      "ingredient": "specific ingredient name",
      "delivery_temp_max_c": 4.0,
      "accept_criteria": "Sensory + visual + packaging criteria for acceptance",
      "reject_criteria": "Specific reject criteria — what does spoiled/unsafe look, smell, feel like"
    }}
  ],

  "ccp_table": [
    {{
      "step": "Step name (e.g. Cooking, Cooling, Hot Hold)",
      "step_id": "matching id from process_flow",
      "ingredient_or_process": "what this CCP applies to",
      "hazard_category": "Biological | Chemical | Physical",
      "hazard": "specific hazard (e.g. Salmonella spp., Listeria monocytogenes, Staphylococcus aureus enterotoxin)",
      "is_ccp": true,
      "decision_tree": {{
        "q1_control_measures_exist": {{
          "answer": "Yes | No",
          "rationale": "one sentence explaining whether preventive control measures exist for this hazard at this step"
        }},
        "q2_step_designed_to_eliminate": {{
          "answer": "Yes | No",
          "rationale": "one sentence explaining whether this step is specifically designed to eliminate or reduce the hazard to an acceptable level"
        }},
        "q3_contamination_could_exceed": {{
          "answer": "Yes | No",
          "rationale": "one sentence on whether contamination could occur in excess of acceptable levels or could increase to unacceptable levels at this step"
        }},
        "q4_subsequent_step_eliminates": {{
          "answer": "Yes | No | N/A",
          "rationale": "one sentence on whether a subsequent step will eliminate the hazard or reduce it to acceptable levels"
        }},
        "conclusion": "One sentence stating why this step is or isn't a CCP based on the four answers above. Cite the Codex decision tree logic."
      }},
      "critical_limit": "Specific measurable limit — temperature, time, pH, water activity (e.g. 'Core temperature ≥75°C for ≥15 seconds')",
      "monitoring": "What is monitored, how, frequency, by whom (e.g. 'Calibrated probe thermometer, every batch, by station chef')",
      "corrective_action": "Specific action if the limit is breached",
      "records": "Where this is logged (e.g. 'Cook Log CL-01')"
    }}
  ],

  "non_ccp_steps": [
    {{
      "step": "step name",
      "rationale": "why this step is not a CCP (e.g. 'subsequent cooking eliminates the hazard')"
    }}
  ],

  "hazard_analysis": [
    {{
      "step": "step id or label from process_flow",
      "agents": [
        {{
          "category": "Biological | Chemical | Physical",
          "agent": "specific organism or hazard (e.g. Salmonella spp., allergen cross-contact, glass fragment)",
          "source": "how this hazard enters at this step",
          "severity": "High | Medium | Low",
          "likelihood": "High | Medium | Low",
          "significant": true
        }}
      ]
    }}
  ],

  "verification": {{
    "activities": [
      "Calibrate all probe thermometers against a certified reference before each service. Log calibration date, result, and initials.",
      "Supervisory review of all completed monitoring logs at end of each service.",
      "Internal HACCP audit conducted quarterly. Document findings and corrective actions.",
      "Finished product temperature check randomly once per service by PIC."
    ],
    "frequency_note": "one sentence summarising how often the full HACCP plan is formally reviewed and updated"
  }},

  "pic_signoff_required": true,
  "footer_note": "Brief structure follows Codex Alimentarius CXC 1-1969 (General Principles of Food Hygiene). Implementation is the responsibility of the operator."
}}

ALLERGEN INSTRUCTIONS:
- The region is {allergen_region} ({region_info['label']})
- The region's allergen list is: {region_allergens}
- Include ONLY allergens that this region's regulator requires labeling for
- Detect allergens from the ingredient list. Match conservatively: if dairy is present, flag "milk"; if any egg product, flag "eggs"; if any wheat-based, flag accordingly per region
- Provide a one-sentence rationale stating which ingredient triggered which allergen

DECISION TREE LOGIC (Codex):
- Apply the four questions to EVERY step in the process flow
- A step is a CCP if Q3 = Yes AND Q4 = No (contamination could exceed limits AND no subsequent step eliminates it)
- A step is NOT a CCP if Q4 = Yes (a subsequent step handles the hazard) OR Q3 = No (contamination cannot reach unacceptable levels)
- Be honest about non-CCPs — list them in the non_ccp_steps array. Inspectors prefer a tight list of real CCPs to a bloated list of nominal ones.

QUALITY RULES:
- Critical limits must be measurable. Numbers, units, time bounds. No vague language.
- Monitoring must specify: what, how, frequency, who. Not "regularly" — say "every two hours by the station chef."
- Corrective actions must be specific actions, not policies.
- Receiving criteria must be sensory and verifiable by a cook with a thermometer and their own senses.

The recipe is "{recipe_name}". The ingredient list and method steps are below. Generate the brief."""


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
@requires_tier("profession")
def haccp_analysis():
    print("[HACCP] route entered", flush=True)
    from datetime import datetime, timezone
    data = request.get_json() or {}
    title = data.get("title", "Untitled")
    ingredients = data.get("ingredients", [])
    method_steps = data.get("method_steps", [])

    if not method_steps and not ingredients:
        return jsonify(error="No recipe data provided"), 400

    # Per-request region override, then user profile, then default EU
    requested_region = (data.get("allergen_region") or "").upper()

    user = get_current_user()
    allergen_region = HACCP_DEFAULT_REGION
    if user and user.get("haccp_allergen_region"):
        r = user["haccp_allergen_region"].upper()
        if r in HACCP_ALLERGEN_REGIONS:
            allergen_region = r
    if requested_region and requested_region in HACCP_ALLERGEN_REGIONS:
        allergen_region = requested_region

    print(f"[HACCP] building prompt; title={title!r} ingredients={len(ingredients)} steps={len(method_steps)} region={allergen_region}", flush=True)

    system_prompt = build_haccp_system_prompt(title, ingredients, allergen_region)

    ingredients_text = json.dumps(ingredients, ensure_ascii=False)
    method_text = json.dumps(method_steps, ensure_ascii=False)
    user_message = (
        f"Recipe: {title}\n"
        f"Ingredients (JSON): {ingredients_text}\n"
        f"Method steps (JSON): {method_text}\n\n"
        f"Generate the structured HACCP brief now. Return JSON only."
    )

    print(f"[HACCP] calling Anthropic API; prompt_chars={len(system_prompt)} user_msg_chars={len(user_message)}", flush=True)

    MAX_ATTEMPTS = 2
    required_keys = {"schema_version", "recipe_name", "allergens", "process_flow", "ccp_table"}
    last_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=8192,
                timeout=90.0,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            raw_text = resp.content[0].text.strip()
            print(f"[HACCP] attempt {attempt}/{MAX_ATTEMPTS} LLM returned; raw_chars={len(raw_text)}", flush=True)

            # Strip any accidental markdown fences
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```", 2)[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.rsplit("```", 1)[0].strip()

            brief = json.loads(raw_text)

            # Validate required top-level keys
            missing = required_keys - set(brief.keys())
            if missing:
                raise ValueError(f"Missing required sections: {', '.join(sorted(missing))}")

            brief["generated_at"] = datetime.now(timezone.utc).isoformat()
            return jsonify(brief)

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            app.logger.warning(
                f"[HACCP] Attempt {attempt}/{MAX_ATTEMPTS} failed for recipe {title!r}: "
                f"{type(e).__name__}: {e}"
            )
            if attempt < MAX_ATTEMPTS:
                _time.sleep(1)
                continue

        except Exception as e:
            app.logger.error(f"[HACCP] Non-retryable error on attempt {attempt}/{MAX_ATTEMPTS} for recipe {title!r}: {e}")
            return jsonify(error=str(e)), 500

    app.logger.error(
        f"[HACCP] All {MAX_ATTEMPTS} attempts exhausted for recipe {title!r}. Last error: {last_error}"
    )
    return jsonify({
        "error": "Brief generation incomplete",
        "detail": "The brief came back in an unexpected format. Please regenerate.",
        "regenerate_recommended": True
    }), 502


# ── HACCP Persistence Routes ──

def _apply_haccp_edits(brief, edits):
    """Apply user edits on top of generated brief.
    Editable: ccp_table[].monitoring/corrective_action/records,
              receiving_criteria[].accept_criteria/reject_criteria.
    NOT editable: critical_limit, decision_tree."""
    if not edits:
        return brief
    out = json.loads(json.dumps(brief))
    ccp_edits = edits.get("ccp_table") or {}
    for row in out.get("ccp_table", []):
        sid = row.get("step_id")
        if sid and sid in ccp_edits:
            for fld in ("monitoring", "corrective_action", "records"):
                if fld in ccp_edits[sid]:
                    row[fld] = ccp_edits[sid][fld]
    rc_edits = edits.get("receiving_criteria") or {}
    for row in out.get("receiving_criteria", []):
        ing = row.get("ingredient")
        if ing and ing in rc_edits:
            for fld in ("accept_criteria", "reject_criteria"):
                if fld in rc_edits[ing]:
                    row[fld] = rc_edits[ing][fld]
    return out


@app.route("/api/haccp/generate-for-recipe", methods=["POST"])
@requires_tier("profession")
def haccp_generate_for_recipe():
    """Generate and save a HACCP brief for a recipe by slug. Called by the on-demand button."""
    user = get_current_user()
    data = request.get_json() or {}
    recipe_slug = data.get("recipe_slug", "").strip()
    if not recipe_slug:
        return jsonify({"error": "recipe_slug required"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM recipes WHERE slug = %s LIMIT 1", (recipe_slug,))
    recipe = cur.fetchone()
    if not recipe:
        cur.execute(
            "SELECT * FROM user_kitchen_recipes WHERE slug = %s AND user_id = %s LIMIT 1",
            (recipe_slug, user["id"]),
        )
        recipe = cur.fetchone()
    cur.close()
    conn.close()

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    title = recipe.get("name") or recipe.get("title") or "Untitled"
    ingredients = recipe.get("ingredients") or []
    if isinstance(ingredients, str):
        try:
            ingredients = json.loads(ingredients)
        except Exception:
            ingredients = []
    steps = recipe.get("steps") or []
    if isinstance(steps, str):
        try:
            steps = json.loads(steps)
        except Exception:
            steps = []

    allergen_region = HACCP_DEFAULT_REGION
    if user.get("haccp_allergen_region"):
        r = user["haccp_allergen_region"].upper()
        if r in HACCP_ALLERGEN_REGIONS:
            allergen_region = r

    brief = _generate_haccp_brief_internal(title, ingredients, steps, allergen_region)
    if not brief:
        return jsonify({"error": "Brief generation failed — please try again."}), 502

    try:
        conn2 = psycopg2.connect(DATABASE_URL_WRITE)
        conn2.autocommit = True
        cur2 = conn2.cursor()
        cur2.execute(
            "SELECT COALESCE(MAX(version), 0) + 1 FROM haccp_briefs WHERE user_id = %s AND recipe_slug = %s",
            (user["id"], recipe_slug),
        )
        next_version = cur2.fetchone()[0]
        cur2.execute("""
            INSERT INTO haccp_briefs
                (user_id, recipe_slug, recipe_name, version, schema_version,
                 allergen_region, brief_json, edits_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s, '{}')
            RETURNING id
        """, (
            user["id"], recipe_slug, title, next_version,
            brief.get("schema_version", "1.0"), allergen_region,
            json.dumps(brief),
        ))
        brief_id = cur2.fetchone()[0]
        cur2.close()
        conn2.close()
    except Exception as e:
        app.logger.error(f"[HACCP] save failed after generation for {recipe_slug}: {e}")
        return jsonify({"error": "Brief generated but could not be saved — please try again."}), 500

    return jsonify({"ok": True, "brief_id": brief_id})


@app.route("/api/haccp/save", methods=["POST"])
@requires_tier("profession")
def save_haccp_brief():
    user = get_current_user()  # safe — decorator verified user exists
    data = request.get_json() or {}
    brief = data.get("brief")
    edits = data.get("edits") or {}
    recipe_slug = data.get("recipe_slug") or (brief or {}).get("recipe_slug")
    if not brief or not recipe_slug:
        return jsonify({"error": "brief with recipe_slug required"}), 400
    recipe_name = brief.get("recipe_name", "")
    allergen_region = (brief.get("allergens", {}).get("region") or "EU").upper()
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT COALESCE(MAX(version), 0) + 1
            FROM haccp_briefs
            WHERE user_id = %s AND recipe_slug = %s
        """, (user["id"], recipe_slug))
        next_version = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO haccp_briefs
                (user_id, recipe_slug, recipe_name, version, schema_version,
                 allergen_region, brief_json, edits_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, version, created_at
        """, (
            user["id"], recipe_slug, recipe_name, next_version,
            brief.get("schema_version", "1.0"), allergen_region,
            json.dumps(brief), json.dumps(edits)
        ))
        row = cur.fetchone()
        return jsonify({"ok": True, "id": row[0], "version": row[1], "saved_at": row[2].isoformat()})
    except Exception as e:
        app.logger.exception("HACCP save failed")
        return jsonify({"error": "Save failed", "detail": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/api/haccp/latest/<recipe_slug>", methods=["GET"])
@requires_tier("kitchen")
def get_latest_haccp_brief(recipe_slug):
    user = get_current_user()  # safe — decorator verified user exists
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT id, version, schema_version, brief_json, edits_json,
                   pic_name, pic_signed_at, generated_at, created_at
            FROM haccp_briefs
            WHERE user_id = %s AND recipe_slug = %s
            ORDER BY version DESC LIMIT 1
        """, (user["id"], recipe_slug))
        row = cur.fetchone()
        if not row:
            return jsonify({"exists": False}), 200
        brief = row["brief_json"]
        if isinstance(brief, str):
            brief = json.loads(brief)
        edits = row["edits_json"] or {}
        if isinstance(edits, str):
            edits = json.loads(edits)
        applied = _apply_haccp_edits(brief, edits)
        return jsonify({
            "exists": True, "id": row["id"], "version": row["version"],
            "schema_version": row["schema_version"], "brief": applied, "edits": edits,
            "pic_name": row["pic_name"],
            "pic_signed_at": row["pic_signed_at"].isoformat() if row["pic_signed_at"] else None,
            "saved_at": row["created_at"].isoformat()
        })
    finally:
        cur.close()
        conn.close()


@app.route("/api/haccp/history/<recipe_slug>", methods=["GET"])
@requires_tier("kitchen")
def get_haccp_history(recipe_slug):
    user = get_current_user()  # safe — decorator verified user exists
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT id, version, pic_name, pic_signed_at, created_at
            FROM haccp_briefs
            WHERE user_id = %s AND recipe_slug = %s
            ORDER BY version DESC
        """, (user["id"], recipe_slug))
        rows = cur.fetchall()
        return jsonify({"history": [{
            "id": r["id"], "version": r["version"], "pic_name": r["pic_name"],
            "pic_signed_at": r["pic_signed_at"].isoformat() if r["pic_signed_at"] else None,
            "saved_at": r["created_at"].isoformat()
        } for r in rows]})
    finally:
        cur.close()
        conn.close()


@app.route("/api/haccp/sign", methods=["POST"])
@requires_tier("profession")
def sign_haccp_brief():
    user = get_current_user()  # safe — decorator verified user exists
    data = request.get_json() or {}
    brief_id = data.get("id")
    pic_name = (data.get("pic_name") or "").strip()
    if not brief_id or not pic_name:
        return jsonify({"error": "id and pic_name required"}), 400
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE haccp_briefs
            SET pic_name = %s, pic_signed_at = NOW()
            WHERE id = %s AND user_id = %s
            RETURNING pic_signed_at
        """, (pic_name, brief_id, user["id"]))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Brief not found"}), 404
        return jsonify({"ok": True, "pic_signed_at": row[0].isoformat()})
    except Exception as e:
        return jsonify({"error": "Sign failed", "detail": str(e)}), 500
    finally:
        cur.close()
        conn.close()


def _annotation_create(user, slug, body):
    """Shared insert for recipe_annotations."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO recipe_annotations (user_id, recipe_slug, body) VALUES (%s, %s, %s) RETURNING *",
        (str(user["id"]), slug, body)
    )
    note = dict(cur.fetchone())
    note["created_at"] = note["created_at"].isoformat()
    note["updated_at"] = note["updated_at"].isoformat()
    cur.close()
    conn.close()
    return note


def _annotation_list(user, slug):
    """Shared list for recipe_annotations."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "SELECT * FROM recipe_annotations WHERE user_id = %s AND recipe_slug = %s ORDER BY created_at DESC",
        (str(user["id"]), slug)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    notes = []
    for r in rows:
        n = dict(r)
        n["created_at"] = n["created_at"].isoformat()
        n["updated_at"] = n["updated_at"].isoformat()
        notes.append(n)
    return notes


# ── /api/annotations/ — personal notepad (renamed from kitchen_notes) ──────

@app.route("/api/annotations", methods=["POST"])
def annotations_create():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403
    data = request.get_json() or {}
    slug = (data.get("slug") or "").strip()
    body = (data.get("body") or "").strip()
    if not slug or not body:
        return jsonify({"error": "slug and body required"}), 400
    return jsonify(_annotation_create(user, slug, body)), 201


@app.route("/api/annotations/<slug>", methods=["GET"])
def annotations_list(slug):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403
    return jsonify(_annotation_list(user, slug))


@app.route("/api/annotations/note/<note_id>", methods=["PUT"])
def annotations_update(note_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403
    data = request.get_json() or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"error": "body required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "UPDATE recipe_annotations SET body = %s, updated_at = now() WHERE id = %s AND user_id = %s RETURNING *",
        (body, note_id, str(user["id"]))
    )
    note = cur.fetchone()
    cur.close()
    conn.close()
    if not note:
        return jsonify({"error": "Not found"}), 404
    note = dict(note)
    note["created_at"] = note["created_at"].isoformat()
    note["updated_at"] = note["updated_at"].isoformat()
    return jsonify(note)


@app.route("/api/annotations/note/<note_id>", methods=["DELETE"])
def annotations_delete(note_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM recipe_annotations WHERE id = %s AND user_id = %s",
        (note_id, str(user["id"]))
    )
    deleted = cur.rowcount
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"ok": True})


# ── /api/kitchen-notes/<slug> — AI-generated HACCP safety card ─────────────

@app.route("/api/kitchen-notes/<slug>", methods=["GET"])
def kitchen_notes_card(slug):
    """Return auto-generated kitchen safety card (CCPs, temps, allergens, etc.).
    Cached per recipe. Re-generates if cache is absent."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Serve from cache if available
    cur.execute(
        "SELECT content FROM recipe_kitchen_notes_cache WHERE recipe_slug = %s",
        (slug,)
    )
    cached = cur.fetchone()
    if cached:
        cur.close()
        conn.close()
        return jsonify(cached["content"])

    # Fetch recipe data
    cur.execute("SELECT * FROM recipes WHERE slug = %s LIMIT 1", (slug,))
    recipe = cur.fetchone()
    if not recipe:
        cur.close()
        conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    name         = recipe.get("name") or slug
    cuisine      = recipe.get("cuisine") or ""
    recipe_type  = recipe.get("recipe_type") or "food"
    description  = recipe.get("sashimi_standard") or recipe.get("description") or ""

    # Build ingredients text — handle flat list and grouped list
    raw_ings = recipe.get("ingredients") or []
    ing_lines = []
    for item in raw_ings:
        if not isinstance(item, dict):
            continue
        if "items" in item:  # grouped
            if item.get("group"):
                ing_lines.append(f"[{item['group']}]")
            for sub in (item.get("items") or []):
                if sub.get("name"):
                    qty  = sub.get("quantity") or ""
                    unit = sub.get("unit") or ""
                    ing_lines.append(f"  {qty} {unit} {sub['name']}".strip())
        elif item.get("name"):
            qty  = item.get("quantity") or ""
            unit = item.get("unit") or ""
            ing_lines.append(f"{qty} {unit} {item['name']}".strip())
    ingredients_text = "\n".join(ing_lines) or "Not specified"

    # Build method text
    raw_steps = recipe.get("steps") or recipe.get("method") or []
    step_lines = []
    for idx, s in enumerate(raw_steps, 1):
        if isinstance(s, dict):
            text = s.get("text") or s.get("step") or s.get("instruction") or ""
        else:
            text = str(s)
        if text:
            step_lines.append(f"{idx}. {text}")
    steps_text = "\n".join(step_lines) or description or "Not specified"

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        cur.close()
        conn.close()
        return jsonify({"error": "Service not configured"}), 500

    prompt = f"""You are a food safety advisor for working chefs. Analyse this recipe and return a concise kitchen safety card as structured JSON.

RECIPE: {name}
CUISINE: {cuisine or 'Not specified'}
TYPE: {recipe_type}

INGREDIENTS:
{ingredients_text}

METHOD:
{steps_text}

Return a JSON object with exactly these keys:
- "ccps": Critical Control Points. One sentence each. Cover: protein/dairy/egg storage temps, cook-through temps, time-temperature danger zone, hot-hold/cold-hold, reheating. Only include what applies to this recipe.
- "temperatures": Temperature windows that matter for this dish — doneness, food-safety thresholds, texture-critical zones (e.g. egg coagulation). Give the range, not just a single number.
- "allergens": Flat array of allergen strings. Labels: egg, gluten, milk, shellfish, fish, tree nuts, peanuts, soy, sesame, sulphites. Add source in parentheses where helpful (e.g. "milk (Pecorino, Parmigiano)"). List only allergens present.
- "cross_contamination": Contamination-risk strings. Flag: raw protein near cooked surfaces, allergen cross-contact, board/knife separation, multi-use equipment risks.
- "shelf_life_signals": Storage and service-life strings. Cover: prepared components, opened ingredients, hot-hold limits, how long mise en place holds.

Rules:
- Working-chef voice. Blunt and precise. Not academic, not legal. No "please ensure" or "it is recommended."
- Maximum 5 items per section. Minimum 1 per section if relevant.
- If a section genuinely has no items (e.g. no allergens), return an empty array [].
- Be specific: "63°C core" not "piping hot." "72h refrigerated" not "a few days."
- Return ONLY valid JSON. No markdown fences, no commentary outside the JSON object."""

    client = anthropic.Anthropic(api_key=anthropic_key)
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = resp.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        card_data = json.loads(raw)
        # Ensure all 5 keys present
        for k in ("ccps", "temperatures", "allergens", "cross_contamination", "shelf_life_signals"):
            if k not in card_data or not isinstance(card_data[k], list):
                card_data[k] = []
        # Cache result
        cur.execute("""
            INSERT INTO recipe_kitchen_notes_cache (recipe_slug, content)
            VALUES (%s, %s)
            ON CONFLICT (recipe_slug) DO UPDATE
              SET content = EXCLUDED.content, generated_at = now()
        """, (slug, json.dumps(card_data)))
        cur.close()
        conn.close()
        return jsonify(card_data)
    except Exception as e:
        import traceback
        app.logger.error(f"Kitchen notes generation failed for {slug}: {traceback.format_exc()}")
        if conn:
            try:
                cur.close()
                conn.close()
            except Exception:
                pass
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500


@app.route("/api/haccp/<slug>/pdf")
@requires_tier("profession")
def haccp_pdf(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime

    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT id, version, schema_version, brief_json, edits_json,
                   pic_name, pic_signed_at, generated_at, created_at
            FROM haccp_briefs
            WHERE user_id = %s AND recipe_slug = %s
            ORDER BY version DESC LIMIT 1
        """, (user["id"], slug))
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "No saved HACCP brief for this recipe"}), 404

    brief = row["brief_json"]
    if isinstance(brief, str):
        brief = json.loads(brief)
    edits = row["edits_json"] or {}
    if isinstance(edits, str):
        edits = json.loads(edits)
    brief = _apply_haccp_edits(brief, edits)

    def _esc(v):
        return html_mod.escape(str(v)) if v is not None else ''

    now = datetime.now()
    date_human = now.strftime('%-d %B %Y')
    gen_stamp = now.strftime('%-d %B %Y · %H:%M')
    date_str = now.strftime('%Y-%m-%d')

    recipe_name = brief.get("recipe_name") or slug
    schema_ver = row.get("schema_version") or brief.get("schema_version") or "1.0"
    version_num = row["version"]
    pic_name = row.get("pic_name") or ""
    pic_signed_at = row.get("pic_signed_at")
    is_signed = bool(pic_signed_at)

    if is_signed:
        signed_date_str = pic_signed_at.strftime('%-d %b %Y') if pic_signed_at else ""
        version_label = f'v{version_num} — SIGNED · {html_mod.escape(pic_name)} · {signed_date_str}'
        badge_cls = 'version-badge signed'
    else:
        version_label = f'v{version_num} — DRAFT — UNSIGNED'
        badge_cls = 'version-badge'

    # Allergens
    allergens = brief.get("allergens") or {}
    region_code = (allergens.get("region") or "EU").upper()
    region_info = HACCP_ALLERGEN_REGIONS.get(region_code, HACCP_ALLERGEN_REGIONS.get("EU", {}))
    region_label_text = allergens.get("region_label") or region_info.get("label", region_code)
    all_allergens_list = region_info.get("allergens") or allergens.get("detected") or []
    detected_set = set(a.lower() for a in (allergens.get("detected") or []))
    allergen_pills_html = "".join(
        '<span class="allergen-pill allergen-pill-detected">' + _esc(a.replace("_", " ")) + '</span>'
        if a.lower() in detected_set else
        '<span class="allergen-pill allergen-pill-clear">' + _esc(a.replace("_", " ")) + '</span>'
        for a in all_allergens_list
    )
    allergen_rationale_text = _esc(allergens.get("rationale") or "")
    allergen_rationale_html = (
        '<p class="allergen-rationale">' + allergen_rationale_text + '</p>'
        if allergen_rationale_text else ''
    )

    # Process flow
    process_flow = brief.get("process_flow") or []
    flow_items = "".join(
        '<li class="flow-step"><span class="flow-num">' + str(i + 1) + '</span>'
        '<span class="flow-label">' + _esc(s.get("label", "")) + '</span></li>'
        for i, s in enumerate(process_flow)
    )

    # Receiving criteria (hazard analysis for incoming materials)
    receiving = brief.get("receiving_criteria") or []
    if receiving:
        rc_rows = []
        for it in receiving:
            temp = ('≤' + str(it['delivery_temp_max_c']) + '°C') if it.get('delivery_temp_max_c') is not None else '—'
            rc_rows.append(
                '<tr>'
                '<td><strong>' + _esc(it.get('ingredient', '')) + '</strong></td>'
                '<td class="mono">' + _esc(temp) + '</td>'
                '<td class="accept">' + _esc(it.get('accept_criteria', '')) + '</td>'
                '<td class="reject">' + _esc(it.get('reject_criteria', '')) + '</td>'
                '</tr>'
            )
        receiving_section_html = (
            '<section class="doc-section">'
            '<h2 class="section-head">Receiving Criteria</h2>'
            '<table class="data-table">'
            '<thead><tr><th>Ingredient</th><th>Temp. max</th><th>Accept</th><th>Reject</th></tr></thead>'
            '<tbody>' + ''.join(rc_rows) + '</tbody>'
            '</table></section>'
        )
    else:
        receiving_section_html = ''

    # "Where the dish lives or dies" — most critical CCP, shown above the table
    ccps = brief.get("ccp_table") or []
    lives_ccp = next((c for c in ccps if (c.get("hazard_category") or "").lower() == "biological"), None)
    if not lives_ccp and ccps:
        lives_ccp = ccps[0]
    if lives_ccp:
        lives_html = (
            '<div class="lives-callout">'
            '<div class="lives-eyebrow">Where the dish lives or dies</div>'
            '<div class="lives-step">' + _esc(lives_ccp.get("step", "")) + '</div>'
            '<div class="lives-detail">' + _esc(lives_ccp.get("critical_limit", "")) +
            ' — ' + _esc(lives_ccp.get("hazard", "")) + '</div>'
            '</div>'
        )
    else:
        lives_html = ''

    # CCP table rows with inline Codex Decision Tree notes
    ccp_rows_parts = []
    for ccp in ccps:
        cat = (ccp.get("hazard_category") or "").lower()
        sub_html = (
            '<div class="ccp-sub">' + _esc(ccp.get("ingredient_or_process", "")) + '</div>'
            if ccp.get("ingredient_or_process") else ''
        )
        ccp_rows_parts.append(
            '<tr class="ccp-row">'
            '<td><strong>' + _esc(ccp.get("step", "")) + '</strong>' + sub_html + '</td>'
            '<td><span class="hazard-cat hazard-' + _esc(cat) + '">' + _esc(ccp.get("hazard_category", "")) + '</span>'
            '<div class="ccp-sub">' + _esc(ccp.get("hazard", "")) + '</div></td>'
            '<td class="mono">' + _esc(ccp.get("critical_limit", "")) + '</td>'
            '<td>' + _esc(ccp.get("monitoring", "")) + '</td>'
            '<td>' + _esc(ccp.get("corrective_action", "")) + '</td>'
            '<td>' + _esc(ccp.get("records", "")) + '</td>'
            '</tr>'
        )
        dt = ccp.get("decision_tree") or {}
        dt_parts = []
        for qn, key in [
            ("Q1", "q1_control_measures_exist"),
            ("Q2", "q2_step_designed_to_eliminate"),
            ("Q3", "q3_contamination_could_exceed"),
            ("Q4", "q4_subsequent_step_eliminates"),
        ]:
            qobj = dt.get(key)
            if qobj:
                ans = qobj.get("answer", "")
                rat = qobj.get("rationale", "")
                dt_parts.append(qn + ': ' + _esc(ans) + (' — ' + _esc(rat) if rat else ''))
        if dt.get("conclusion"):
            dt_parts.append('Conclusion: ' + _esc(dt["conclusion"]))
        if dt_parts:
            ccp_rows_parts.append(
                '<tr class="dt-row"><td colspan="6" class="dt-cell">'
                'Codex Decision Tree — ' + ' · '.join(dt_parts) +
                '</td></tr>'
            )
    ccp_rows_html = ''.join(ccp_rows_parts)

    # Non-CCP steps
    non_ccp = brief.get("non_ccp_steps") or []
    if non_ccp:
        nc_items = ''.join(
            '<li><strong>' + _esc(s.get("step", "")) + '</strong> — ' + _esc(s.get("rationale", "")) + '</li>'
            for s in non_ccp
        )
        non_ccp_section_html = (
            '<section class="doc-section">'
            '<h2 class="section-head">Non-CCP Steps</h2>'
            '<ul class="simple-list">' + nc_items + '</ul>'
            '</section>'
        )
    else:
        non_ccp_section_html = ''

    # Sign-off block — filled if signed, ruled lines if draft
    if is_signed:
        signed_display = pic_signed_at.strftime('%-d %B %Y') if pic_signed_at else '—'
        signoff_html = (
            '<div class="signoff-grid">'
            '<div class="signoff-field"><div class="signoff-label">Full name</div>'
            '<div class="signoff-value">' + _esc(pic_name) + '</div></div>'
            '<div class="signoff-field"><div class="signoff-label">Signature (digital)</div>'
            '<div class="signoff-value signoff-sig">' + _esc(pic_name) + '</div></div>'
            '<div class="signoff-field"><div class="signoff-label">Date signed</div>'
            '<div class="signoff-value">' + _esc(signed_display) + '</div></div>'
            '</div>'
        )
    else:
        signoff_html = (
            '<div class="signoff-grid">'
            '<div class="signoff-field"><div class="signoff-label">Full name</div>'
            '<div class="signoff-line"></div></div>'
            '<div class="signoff-field"><div class="signoff-label">Signature</div>'
            '<div class="signoff-line"></div></div>'
            '<div class="signoff-field"><div class="signoff-label">Date</div>'
            '<div class="signoff-line"></div></div>'
            '</div>'
        )

    footer_note = _esc(
        brief.get("footer_note") or
        "Brief structure follows Codex Alimentarius CXC 1-1969 (General Principles of Food Hygiene). "
        "Implementation is the responsibility of the operator."
    )
    allergen_comm = (
        "Allergen status is communicated to all kitchen staff at briefing prior to service. "
        "Front-of-house staff are briefed on allergen presence in this dish. "
        "Customers with allergies are notified verbally of cross-contamination risk and offered alternatives."
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>HACCP Brief — {_esc(recipe_name)}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=DM+Sans:wght@300;500&family=DM+Mono:wght@400;500&display=swap');

@page {{
  size: A4;
  margin: 2cm 2cm 3cm 2cm;
  @bottom-left {{
    content: "PROVENANCE \00b7 provenance.kitchen";
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
  @bottom-center {{
    content: "/recipe/{_esc(slug)}  \00b7  Page " counter(page) " of " counter(pages);
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
  @bottom-right {{
    content: "Generated {gen_stamp}";
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
}}
body {{ font-family: 'DM Sans', sans-serif; font-weight: 300; color: #1f1b16; margin: 0; padding: 0; }}
.header {{ display: flex; justify-content: space-between; align-items: baseline; font-family: 'DM Mono', monospace; font-size: 10pt; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; }}
.header__wordmark {{ color: #C9A84C; }}
.header__doctype {{ color: #1f1b16; }}
.title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 22pt; font-weight: 400; letter-spacing: -0.005em; line-height: 1.15; margin: 5mm 0 0 0; color: #1f1b16; }}
.gold-rule {{ width: 1.5cm; height: 1px; background: #C9A84C; margin: 6mm 0; border: none; }}
.meta-strip {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #807462; margin-bottom: 8mm; }}
.meta-sep {{ color: #c4b89e; margin: 0 2mm; }}
.version-badge {{ display: inline-block; font-family: 'DM Mono', monospace; font-size: 8pt; letter-spacing: 0.1em; text-transform: uppercase; padding: 1mm 3mm; margin-bottom: 5mm; border: 1px solid #c4b89e; color: #807462; }}
.version-badge.signed {{ border-color: #a85a3f; color: #a85a3f; }}
.doc-ctrl-grid {{ display: flex; gap: 8mm; margin-bottom: 6mm; }}
.doc-ctrl-field {{ flex: 1; }}
.doc-ctrl-label {{ font-family: 'DM Mono', monospace; font-size: 8pt; letter-spacing: 0.1em; text-transform: uppercase; color: #807462; margin-bottom: 2mm; }}
.doc-ctrl-line {{ border-bottom: 1px solid #807462; height: 5mm; }}
.doc-section {{ margin-bottom: 8mm; page-break-inside: avoid; }}
.section-head {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 13pt; font-weight: 400; color: #1f1b16; margin: 0 0 3mm; border: none; }}
.allergen-box {{ background: #f5f1e9; border-left: 3px solid #a85a3f; padding: 3mm 4mm; margin-bottom: 6mm; page-break-inside: avoid; }}
.allergen-region {{ font-family: 'DM Mono', monospace; font-size: 8pt; letter-spacing: 0.1em; text-transform: uppercase; color: #807462; margin-bottom: 2mm; }}
.allergen-pills {{ display: flex; flex-wrap: wrap; gap: 2mm; margin-bottom: 2mm; }}
.allergen-pill {{ font-family: 'DM Mono', monospace; font-size: 8pt; padding: 0.5mm 2.5mm; border-radius: 2px; }}
.allergen-pill-detected {{ background: rgba(168,90,63,0.15); color: #a85a3f; border: 1px solid rgba(168,90,63,0.4); }}
.allergen-pill-clear {{ background: rgba(0,0,0,0.04); color: #b4b2a9; border: 1px solid rgba(0,0,0,0.08); text-decoration: line-through; }}
.allergen-rationale {{ font-size: 9pt; color: #4a3f33; line-height: 1.45; margin: 0; }}
.flow-list {{ list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 2mm; }}
.flow-step {{ display: flex; align-items: center; gap: 1.5mm; background: #f5f1e9; border: 1px solid #d9d0b6; padding: 1.5mm 3mm; font-size: 9pt; }}
.flow-num {{ display: inline-flex; align-items: center; justify-content: center; min-width: 5mm; height: 5mm; border-radius: 50%; background: rgba(201,168,76,0.2); color: #C9A84C; font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 500; }}
.lives-callout {{ background: #f5f1e9; border-left: 3px solid #a85a3f; padding: 3mm 4mm; margin-bottom: 5mm; page-break-inside: avoid; }}
.lives-eyebrow {{ font-family: 'DM Mono', monospace; font-size: 8pt; letter-spacing: 0.12em; text-transform: uppercase; color: #a85a3f; margin-bottom: 1mm; }}
.lives-step {{ font-family: 'Playfair Display', Georgia, serif; font-size: 12pt; color: #1f1b16; margin-bottom: 1mm; }}
.lives-detail {{ font-size: 9pt; color: #4a3f33; }}
.data-table {{ width: 100%; border-collapse: collapse; background: #f5f1e9; border: 1px solid #d9d0b6; font-size: 9pt; }}
.data-table thead {{ background: #ece6d7; }}
.data-table thead th {{ font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #807462; text-align: left; padding: 2mm 3mm; border-bottom: 1px solid #d9d0b6; }}
.data-table tbody td {{ padding: 2.5mm 3mm; border-bottom: 1px dotted #d9d0b6; vertical-align: top; line-height: 1.4; }}
.data-table tbody tr:last-child td {{ border-bottom: none; }}
.mono {{ font-family: 'DM Mono', monospace; font-size: 8.5pt; }}
.accept {{ color: #2d5a3d; }}
.reject {{ color: #a85a3f; }}
.ccp-sub {{ font-size: 8pt; color: #807462; margin-top: 1mm; font-style: italic; }}
.hazard-cat {{ display: inline-block; font-family: 'DM Mono', monospace; font-size: 7.5pt; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.5mm 2mm; margin-bottom: 1mm; }}
.hazard-biological {{ background: rgba(168,90,63,0.12); color: #a85a3f; }}
.hazard-chemical {{ background: rgba(180,140,60,0.12); color: #7a5f10; }}
.hazard-physical {{ background: rgba(60,100,160,0.12); color: #3c64a0; }}
.dt-row td {{ background: #f0ece4; }}
.dt-cell {{ font-size: 8pt; color: #4a3f33; padding: 2mm 3mm; font-style: italic; border-bottom: 1px solid #d9d0b6; }}
.simple-list {{ list-style: none; padding: 0; margin: 0; }}
.simple-list li {{ padding: 1.5mm 0; border-bottom: 1px dotted #d9d0b6; font-size: 9.5pt; }}
.simple-list li:last-child {{ border-bottom: none; }}
.annotation {{ font-size: 9.5pt; color: #1f1b16; line-height: 1.55; background: #f5f1e9; padding: 3mm 4mm; }}
.signoff-grid {{ display: flex; gap: 8mm; margin-top: 3mm; }}
.signoff-field {{ flex: 1; }}
.signoff-label {{ font-family: 'DM Mono', monospace; font-size: 8pt; letter-spacing: 0.1em; text-transform: uppercase; color: #807462; margin-bottom: 2mm; }}
.signoff-value {{ font-size: 10pt; color: #1f1b16; padding-bottom: 1mm; border-bottom: 1px solid #1f1b16; }}
.signoff-sig {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 12pt; }}
.signoff-line {{ border-bottom: 1px solid #807462; height: 6mm; }}
.page-footer {{ font-size: 8pt; color: #807462; border-top: 1px dotted #d9d0b6; padding-top: 3mm; margin-top: 8mm; font-family: 'DM Mono', monospace; letter-spacing: 0.06em; }}
</style>
</head>
<body>

<div class="header">
  <span class="header__wordmark">PROVENANCE</span>
  <span class="header__doctype">HACCP BRIEF</span>
</div>

<h1 class="title">{_esc(recipe_name)}</h1>
<hr class="gold-rule">
<div class="meta-strip">
  <span>{date_human}</span><span class="meta-sep">·</span><span>/recipe/{_esc(slug)}</span><span class="meta-sep">·</span><span>Schema {_esc(schema_ver)}</span><span class="meta-sep">·</span><span>Profession tier</span>
</div>

<section class="doc-section">
  <div class="{badge_cls}">{version_label}</div>
  <div class="doc-ctrl-grid">
    <div class="doc-ctrl-field"><div class="doc-ctrl-label">Effective date</div><div class="doc-ctrl-line"></div></div>
    <div class="doc-ctrl-field"><div class="doc-ctrl-label">Next review</div><div class="doc-ctrl-line"></div></div>
  </div>
</section>

<section class="doc-section">
  <h2 class="section-head">Allergens</h2>
  <div class="allergen-box">
    <div class="allergen-region">{_esc(region_label_text)}</div>
    <div class="allergen-pills">{allergen_pills_html}</div>
    {allergen_rationale_html}
  </div>
</section>

<section class="doc-section">
  <h2 class="section-head">Process Flow</h2>
  <ol class="flow-list">{flow_items}</ol>
</section>

{receiving_section_html}

<section class="doc-section">
  <h2 class="section-head">Critical Control Points</h2>
  {lives_html}
  <table class="data-table">
    <thead>
      <tr>
        <th style="width:16%">Step</th>
        <th style="width:18%">Hazard</th>
        <th style="width:14%">Critical Limit</th>
        <th style="width:18%">Monitoring</th>
        <th style="width:18%">Corrective Action</th>
        <th style="width:16%">Records</th>
      </tr>
    </thead>
    <tbody>{ccp_rows_html}</tbody>
  </table>
</section>

{non_ccp_section_html}

<section class="doc-section">
  <h2 class="section-head">Allergen Communication</h2>
  <div class="annotation">{_esc(allergen_comm)}</div>
</section>

<section class="doc-section">
  <h2 class="section-head">Verification</h2>
  <div class="annotation">Internal HACCP audit conducted quarterly. Document findings and corrective actions taken. Results reviewed by the Person in Charge and retained for inspection.</div>
</section>

<section class="doc-section">
  <h2 class="section-head">Record Retention</h2>
  <div class="annotation">All HACCP records, monitoring logs, and corrective action documentation are retained for a minimum period compliant with applicable local regulatory requirements.</div>
</section>

<section class="doc-section">
  <h2 class="section-head">Equipment Calibration Verification</h2>
  <div class="doc-ctrl-grid">
    <div class="doc-ctrl-field"><div class="doc-ctrl-label">Thermometers calibrated</div><div class="doc-ctrl-line"></div></div>
    <div class="doc-ctrl-field"><div class="doc-ctrl-label">Calibrated by</div><div class="doc-ctrl-line"></div></div>
  </div>
</section>

<section class="doc-section">
  <h2 class="section-head">Person in Charge Sign-Off</h2>
  {signoff_html}
</section>

<div class="page-footer">{footer_note}</div>

</body>
</html>"""

    try:
        pdf_bytes = WeasyHTML(string=html_content).write_pdf()
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'haccp-{slug}-{date_str}.pdf'
        )
    except Exception as e:
        app.logger.exception(f"WeasyPrint error for HACCP brief {slug}")
        return jsonify({"error": str(e)}), 500


def _render_costing_pdf(data):
    """Render a costing sheet PDF per Provenance Printable Doctrine.

    Expects `data` dict with keys: recipe, slug, portions, total_cost,
    cost_per_portion, menu_price (optional), food_cost_pct (optional),
    target_food_cost_pct (optional), breakdown (list of rows).

    Each breakdown row should have: ingredient (or ingredient_name),
    quantity, unit, line_cost. Optional per-row: ingredient_origin,
    origin_producer, local_provider, local_provider_region,
    local_provider_price.

    Returns PDF bytes.
    """
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime
    from html import escape

    def _esc(v):
        return escape(str(v)) if v is not None else ''

    now = datetime.now()
    date_human = now.strftime('%-d %B %Y')
    gen_stamp = now.strftime('%-d %B %Y · %H:%M')
    portions = data.get('portions') or 4
    breakdown = data.get('breakdown') or []
    menu_price = data.get('menu_price')
    food_cost_pct = data.get('food_cost_pct')
    target_food_cost_pct = data.get('target_food_cost_pct', 30.0)
    tier_label = data.get('tier_label', 'Profession tier')
    recipe_name = data.get('recipe', data.get('slug', 'Recipe'))
    title_italic = data.get('title_italic', '')

    # Build ingredient table rows per doctrine §9
    rows_html = []
    for row in breakdown:
        ing_name = _esc(row.get('ingredient') or row.get('ingredient_name', ''))
        ing_origin_text = _esc(row.get('ingredient_origin', ''))
        qty = _esc(row.get('quantity', ''))
        unit = _esc(row.get('unit', ''))
        line_cost = row.get('line_cost')
        line_cost_str = f"CAD {line_cost:.2f}" if line_cost is not None else "—"

        origin_producer = row.get('origin_producer')
        local_provider = row.get('local_provider')
        local_provider_region = row.get('local_provider_region')
        local_provider_price = row.get('local_provider_price')

        # Doctrine §9: em-dash when neither origin nor provider exists;
        # origin alone when origin exists but local provider doesn't;
        # both stacked when both exist.
        if origin_producer and local_provider:
            provider_html = (
                f'<div class="provider__origin">{_esc(origin_producer)}</div>'
                f'<div class="provider__local">↳ {_esc(local_provider_region or "")} · {_esc(local_provider_price or "")}</div>'
            )
        elif origin_producer:
            provider_html = f'<div class="provider__origin">{_esc(origin_producer)}</div>'
        elif local_provider:
            price_line = (
                f'<div class="provider__local-meta">{_esc(local_provider_price)}</div>'
                if local_provider_price else ''
            )
            provider_html = (
                f'<div class="provider__origin">{_esc(local_provider)}</div>'
                f'{price_line}'
            )
        else:
            provider_html = '<div class="provider__origin provider__origin--empty">—</div>'

        origin_subline = (
            f'<div class="ingredient__origin">{ing_origin_text}</div>'
            if ing_origin_text else ''
        )

        rows_html.append(f"""
        <tr>
          <td>
            <div class="ingredient__name">{ing_name}</div>
            {origin_subline}
          </td>
          <td class="ingredient__qty">{qty} {unit}</td>
          <td>{provider_html}</td>
          <td class="line-cost">{line_cost_str}</td>
        </tr>""")
    rows_joined = ''.join(rows_html)

    # Build totals + menu price block per doctrine §10
    total_cost = data.get('total_cost') or 0.0
    cost_per_portion = data.get('cost_per_portion') or 0.0

    menu_price_block = ''
    if menu_price is not None:
        fc_line = (
            f'<div class="menu-price-block__row"><span>Food cost</span>'
            f'<span class="menu-price-block__row__value--filled">{food_cost_pct:.1f}%</span></div>'
        ) if food_cost_pct is not None else ''
        menu_price_block = f"""
        <div class="menu-price-block">
          <div class="menu-price-block__row"><span>Menu price</span><span class="menu-price-block__row__value--filled">CAD {menu_price:.2f}</span></div>
          {fc_line}
          <div class="menu-price-block__row"><span>Target food cost</span><span>&le; {target_food_cost_pct:.1f}%</span></div>
        </div>"""

    title_italic_html = (
        f'<br><span class="title__italic">{_esc(title_italic)}</span>'
        if title_italic else ''
    )

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Costing Sheet — {_esc(recipe_name)}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=DM+Sans:wght@300;500&family=DM+Mono:wght@400;500&display=swap');

@page {{
  size: A4;
  margin: 2cm;
  @bottom-left {{
    content: "PROVENANCE · provenance.kitchen";
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
  @bottom-center {{
    content: "/recipe/{_esc(data.get('slug', ''))}   ·   Page " counter(page) " of " counter(pages);
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
  @bottom-right {{
    content: "Generated {gen_stamp}";
    font-family: 'DM Mono', monospace; font-size: 8pt; font-weight: 400;
    letter-spacing: 0.12em; text-transform: uppercase; color: #807462;
  }}
}}

body {{ font-family: 'DM Sans', sans-serif; font-weight: 300; color: #1f1b16; margin: 0; padding: 0; }}

.header {{ display: flex; justify-content: space-between; align-items: baseline; font-family: 'DM Mono', monospace; font-size: 10pt; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; }}
.header__wordmark {{ color: #C9A84C; }}
.header__doctype {{ color: #1f1b16; }}

.title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 22pt; font-weight: 400; letter-spacing: -0.005em; line-height: 1.15; margin: 5mm 0 0 0; color: #1f1b16; }}
.title__italic {{ font-style: italic; color: #4a3f33; }}

.gold-rule {{ width: 1.5cm; height: 1px; background: #C9A84C; margin: 6mm 0; border: none; }}

.meta-strip {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #807462; margin-bottom: 12mm; }}
.meta-strip__divider {{ color: #c4b89e; margin: 0 2mm; }}

.section__head {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4mm; }}
.section__head h2 {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 14pt; font-weight: 400; color: #1f1b16; margin: 0; }}
.section__head__meta {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #807462; }}

table.ingredient-table {{ width: 100%; background: #F5F1E9; border: 1px solid #d9d0b6; border-collapse: collapse; }}
table.ingredient-table thead {{ background: #ece6d7; }}
table.ingredient-table thead th {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #807462; text-align: left; padding: 2.5mm 4mm; border-bottom: 1px solid #d9d0b6; }}
table.ingredient-table thead th.col-cost {{ text-align: right; }}
table.ingredient-table tbody tr {{ page-break-inside: avoid; }}
table.ingredient-table tbody td {{ padding: 3mm 4mm; border-bottom: 1px dotted #d9d0b6; vertical-align: top; }}
table.ingredient-table tbody tr:last-child td {{ border-bottom: none; }}

.ingredient__name {{ font-family: 'DM Sans', sans-serif; font-size: 11pt; font-weight: 300; color: #1f1b16; line-height: 1.35; }}
.ingredient__origin {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 10pt; color: #4a3f33; line-height: 1.35; margin-top: 1mm; }}
.ingredient__qty {{ font-family: 'DM Mono', monospace; font-size: 10pt; font-weight: 400; color: #1f1b16; line-height: 1.35; }}

.provider__origin {{ font-family: 'Playfair Display', Georgia, serif; font-style: italic; font-size: 10pt; color: #4a3f33; line-height: 1.35; }}
.provider__origin--empty {{ color: #b4b2a9; }}
.provider__local {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 400; color: #807462; line-height: 1.35; margin-top: 1mm; padding-left: 6mm; letter-spacing: 0.02em; }}
.provider__local-meta {{ font-family: 'DM Mono', monospace; font-size: 9pt; font-weight: 400; color: #807462; line-height: 1.35; margin-top: 1mm; letter-spacing: 0.02em; }}

.line-cost {{ font-family: 'DM Mono', monospace; font-size: 10pt; font-weight: 400; color: #1f1b16; text-align: right; line-height: 1.35; }}

.totals {{ margin-top: 8mm; page-break-inside: avoid; }}
.totals__row {{ display: flex; justify-content: space-between; padding: 1.5mm 4mm; font-size: 11pt; color: #1f1b16; }}
.totals__row--primary {{ font-family: 'DM Mono', monospace; font-size: 11pt; font-weight: 500; padding-top: 3mm; border-top: 1px solid #C9A84C; margin-top: 1mm; }}
.totals__row--primary .totals__label {{ font-family: 'DM Mono', monospace; font-weight: 500; }}
.totals__row .totals__value {{ font-family: 'DM Mono', monospace; }}

.menu-price-block {{ margin-top: 6mm; background: #ece6d7; border-left: 3px solid #d9bf75; padding: 4mm 5mm; font-family: 'DM Mono', monospace; font-size: 10pt; color: #4a3f33; page-break-inside: avoid; }}
.menu-price-block__row {{ display: flex; justify-content: space-between; padding: 1mm 0; }}
.menu-price-block__row__value--filled {{ color: #1f1b16; font-weight: 500; }}
</style>
</head>
<body>

<div class="header">
  <span class="header__wordmark">PROVENANCE</span>
  <span class="header__doctype">COSTING SHEET</span>
</div>

<h1 class="title">{_esc(recipe_name)}{title_italic_html}</h1>

<hr class="gold-rule">

<div class="meta-strip">
  <span>{date_human}</span><span class="meta-strip__divider">·</span><span>/recipe/{_esc(data.get('slug', ''))}</span><span class="meta-strip__divider">·</span><span>Portions · {portions}</span><span class="meta-strip__divider">·</span><span>{_esc(tier_label)}</span>
</div>

<div class="section__head">
  <h2>Ingredient cost · at {portions} portions</h2>
  <span class="section__head__meta">Pat's Rule applied</span>
</div>

<table class="ingredient-table">
  <thead>
    <tr>
      <th style="width: 42%;">Ingredient · origin</th>
      <th style="width: 14%;">Quantity</th>
      <th style="width: 30%;">Provider</th>
      <th class="col-cost" style="width: 14%;">Line cost</th>
    </tr>
  </thead>
  <tbody>{rows_joined}</tbody>
</table>

<div class="totals">
  <div class="totals__row totals__row--primary">
    <span class="totals__label">Total ingredient cost</span>
    <span class="totals__value">CAD {total_cost:.2f}</span>
  </div>
  <div class="totals__row">
    <span>Cost per portion ({portions})</span>
    <span class="totals__value">CAD {cost_per_portion:.2f}</span>
  </div>
</div>

{menu_price_block}

</body>
</html>"""

    return WeasyHTML(string=html_content).write_pdf()


# ── Platform counts — shared by /api/stats and template context processor ──
_stats_cache = {"data": None, "timestamp": 0.0}
_STATS_CACHE_TTL_SECONDS = 60


def _compute_platform_counts():
    """Compute and cache platform counts. Returns dict with full *_count keys.
    Shared by /api/stats (JSON) and inject_stats (template context).
    60-second cache. (V4 Sprint 4.7)"""
    import time
    now = time.monotonic()
    if _stats_cache["data"] is not None and (now - _stats_cache["timestamp"]) < _STATS_CACHE_TTL_SECONDS:
        return _stats_cache["data"]

    if not DATABASE_URL:
        # Don't cache the no-DB fallback; let it retry if DB comes online
        return {
            "technique_count": None, "recipe_count": None, "beverage_count": None,
            "supplier_count": None, "drink_count": None, "canon_count": None,
            "p1000_count": None, "pairing_count": None, "route_count": 5,
            "service_protocol_count": None,
        }

    conn = get_db()
    cur = conn.cursor()
    try:
        counts = {}
        queries = [
            ("technique_count", "SELECT COUNT(*) FROM technique_references"),
            ("recipe_count",    "SELECT COUNT(*) FROM recipes"),
            ("beverage_count",  "SELECT COUNT(*) FROM beverage_products WHERE is_published IS TRUE"),
            ("supplier_count",  "SELECT COUNT(DISTINCT s.id) FROM suppliers s JOIN product_suppliers ps ON ps.supplier_id = s.id WHERE s.is_active = TRUE"),
            ("drink_count",     "SELECT COUNT(*) FROM technique_references WHERE category LIKE 'Provenance 500 Drinks%'"),
            ("canon_count",     "SELECT COUNT(*) FROM canons WHERE status != 'archived'"),
            ("p1000_count",              "SELECT COUNT(*) FROM technique_references WHERE category LIKE 'Provenance 1000%'"),
            ("pairing_count",            "SELECT COUNT(*) FROM pairing_intelligence"),
            ("service_protocol_count",   "SELECT COUNT(*) FROM service_protocols"),
        ]
        for key, sql in queries:
            try:
                cur.execute(sql)
                counts[key] = cur.fetchone()[0]
            except Exception:
                counts[key] = None
        counts["route_count"] = 5  # Five trade/spice routes — editorial fixed list, not a DB table

        _stats_cache["data"] = counts
        _stats_cache["timestamp"] = now
        return counts
    finally:
        cur.close()


@app.route("/api/stats")
def api_stats():
    """Public platform counts. 60-second server-side cache. No auth required."""
    return jsonify(_compute_platform_counts())


@app.context_processor
def inject_stats():
    """Inject `stats` dict (short keys) into every template render.
    Routes that pass their own `stats` kwarg override this via Flask precedence."""
    counts = _compute_platform_counts()
    return {
        "stats": {
            "techniques": counts.get("technique_count"),
            "recipes":    counts.get("recipe_count"),
            "beverages":  counts.get("beverage_count"),
            "drinks":     counts.get("drink_count"),
            "suppliers":  counts.get("supplier_count"),
            "canons":     counts.get("canon_count"),
            "routes":     counts.get("route_count"),
            "p1000":              counts.get("p1000_count"),
            "pairings":           counts.get("pairing_count"),
            "service_protocols":  counts.get("service_protocol_count"),
        }
    }


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
        "products_fmt": f"{total_products:,}",
        "suppliers_fmt": f"{total_suppliers:,}",
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

    # Shelves — benchmark producers with editorial depth, grouped by category
    cur.execute("""
        WITH qualifying AS (
            SELECT id, name, origin_brand, origin_country, description, category,
                   COUNT(*) OVER (PARTITION BY category) AS cat_count,
                   ROW_NUMBER() OVER (
                       PARTITION BY category ORDER BY LENGTH(description) DESC
                   ) AS rn
            FROM ingredient_products
            -- preserved_pickled excluded: known miscategorisation hotspot, returns after recategorisation pass
            WHERE origin_brand IS NOT NULL AND origin_brand != ''
              AND description IS NOT NULL AND LENGTH(description) > 30
              AND category != 'preserved_pickled'
        ),
        top_cats AS (
            SELECT DISTINCT category, cat_count,
                CASE category
                    WHEN 'oils_vinegars'         THEN 1
                    WHEN 'spices_seasonings'     THEN 2
                    WHEN 'flour_baking'          THEN 3
                    WHEN 'rice_grains'           THEN 4
                    WHEN 'seafood_general'       THEN 5
                    WHEN 'wagyu_premium_protein' THEN 6
                    WHEN 'dairy_fermented'       THEN 7
                    WHEN 'produce_specialty'     THEN 8
                    ELSE 99
                END AS shelf_order
            FROM qualifying
            WHERE category IN (
                'oils_vinegars','spices_seasonings','flour_baking','rice_grains',
                'seafood_general','wagyu_premium_protein','dairy_fermented','produce_specialty'
            )
        )
        SELECT q.id, q.name, q.origin_brand, q.origin_country, q.description,
               q.category, q.cat_count,
               EXISTS (
                   SELECT 1 FROM product_suppliers ps
                   WHERE ps.product_id = q.id AND UPPER(ps.role) = 'PROVIDER'
               ) AS has_provider
        FROM qualifying q
        JOIN top_cats tc ON q.category = tc.category
        WHERE q.rn <= 6
        ORDER BY tc.shelf_order, q.rn
    """)

    _cat_labels = {
        'spices_seasonings': 'Spices & Seasonings',
        'produce_specialty': 'Specialty Produce',
        'preserved_pickled': 'Preserved & Pickled',
        'flour_baking': 'Flour & Baking',
        'wagyu_premium_protein': 'Wagyu & Premium Protein',
        'oils_vinegars': 'Oils & Vinegars',
        'rice_grains': 'Rice & Grains',
        'seafood_general': 'Seafood',
        'dairy_fermented': 'Dairy & Fermented',
        'chocolate_confection': 'Chocolate & Confection',
        'charcuterie_cured': 'Charcuterie & Cured',
    }

    def _truncate(text, limit=160):
        if not text or len(text) <= limit:
            return text or ''
        return text[:limit].rsplit(' ', 1)[0] + '…'

    shelves = []
    _shelf_index = {}
    for row in cur.fetchall():
        cat = row['category']
        if cat not in _shelf_index:
            _shelf_index[cat] = len(shelves)
            shelves.append({
                'category': cat,
                'label': _cat_labels.get(cat, cat.replace('_', ' ').title()),
                'products': [],
            })
        shelves[_shelf_index[cat]]['products'].append({
            'id': row['id'],
            'name': row['name'],
            'origin_brand': row['origin_brand'],
            'origin_country': row['origin_country'],
            'description': _truncate(row['description']),
            'has_provider': row['has_provider'],
        })

    cur.close()
    conn.close()

    return render_template("ingredients_showcase.html",
        stats=stats,
        top_suppliers=top_suppliers,
        categories=categories,
        countries=countries,
        chain_rows=chain_rows,
        recent_products=recent_products,
        shelves=shelves,
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


# ─── Canon Cycle E: Pat's Rule — pantry origin matcher ───────────────────────

def _match_pantry_for_recipe(ingredient_lines, cur):
    """Match recipe ingredient lines against ingredient_master by word boundary.

    Conservative: exact word-boundary match, case-insensitive. Never fuzzy.
    First match per ingredient line wins. Returns nothing for unmatched lines.

    Returns dict:
      {ingredient_line: {pantry_name, origin_brand, origin_country,
                         supplier_name, supplier_website, supplier_id}}
    """
    if not ingredient_lines:
        return {}

    combined = ' '.join(ingredient_lines).lower()

    cur.execute("""
        SELECT DISTINCT ON (im.canonical_name)
               im.canonical_name,
               im.origin_brand,
               im.origin_country,
               s.name     AS supplier_name,
               s.website  AS supplier_website,
               s.id       AS supplier_id
        FROM ingredient_master im
        LEFT JOIN ingredient_products ip
               ON LOWER(im.canonical_name) = LOWER(ip.name)
        LEFT JOIN product_suppliers ps ON ip.id = ps.product_id
        LEFT JOIN suppliers s ON ps.supplier_id = s.id
        WHERE (im.origin_brand IS NOT NULL AND im.origin_brand != '')
           OR (im.origin_country IS NOT NULL AND im.origin_country != '')
        ORDER BY im.canonical_name,
                 CASE WHEN s.state_province IN ('BC','British Columbia') THEN 0
                      WHEN s.state_province IN ('WA','OR','ID') THEN 1
                      WHEN s.country = 'CA' THEN 2
                      ELSE 3 END,
                 s.id NULLS LAST
    """)
    pantry_rows = cur.fetchall()

    # Pre-filter to only entries whose name is a substring of the ingredient text.
    # Access by column name — cursor is always RealDictCursor in technique_page.
    patterns = []
    for row in pantry_rows:
        name = row['canonical_name']
        if not name or name.lower() not in combined:
            continue
        pat = _re.compile(r'\b' + _re.escape(name.lower()) + r'\b', _re.IGNORECASE)
        patterns.append((name, row['origin_brand'], row['origin_country'],
                         row['supplier_name'], row['supplier_website'],
                         row['supplier_id'], pat))

    result = {}
    for ing_line in ingredient_lines:
        for pname, brand, country, sup_name, sup_url, sup_id, pat in patterns:
            if pat.search(ing_line):
                result[ing_line] = {
                    'pantry_name': pname,
                    'origin_brand': brand,
                    'origin_country': country,
                    'supplier_name': sup_name,
                    'supplier_website': sup_url,
                    'supplier_id': sup_id,
                }
                break  # first match per ingredient line
    return result


# ─── Canon Cycle D: frost helpers ────────────────────────────────────────────

def _frost_words(text, n):
    """Return first n words of text with trailing ellipsis if truncated."""
    if not text:
        return ''
    words = str(text).split()
    return ' '.join(words[:n]) + ('…' if len(words) > n else '')

def _frost_excerpt(technique, user_tier):
    """Build server-side excerpts for free-tier frost band.

    Returns (frosts dict, has_frost bool).
    For paid tiers returns ({}, False) — no excerpts needed.
    Caller must strip full gated fields from technique after calling this.
    """
    if user_tier != 'free':
        return {}, False

    qh = technique.get('quality_hierarchy')
    st = technique.get('sensory_tests')
    lod = technique.get('lives_or_dies')
    rc = technique.get('recipe_card')

    # Quality Hierarchy: first 2 rungs, ~30 words
    qh_ex = None
    if qh:
        items = (qh if isinstance(qh, list) else [qh])[:2]
        parts = []
        for item in items:
            if isinstance(item, dict):
                text = item.get('criteria') or item.get('tier_name') or ''
            else:
                text = str(item)
            w = _frost_words(text, 15)
            if w:
                parts.append(w)
        qh_ex = ' '.join(parts) or None

    # Sensory Tests: first test, ~20 words
    st_ex = None
    if st:
        if isinstance(st, dict):
            k = next(iter(st))
            st_ex = f"{k}: {_frost_words(st[k], 20)}"
        elif isinstance(st, list) and st:
            t = st[0]
            if isinstance(t, dict):
                sense = t.get('sense', '')
                cue = t.get('cue', '')
                text = f"{sense}: {cue}" if sense else cue
            else:
                text = str(t)
            st_ex = _frost_words(text, 20)

    # Lives or Dies: first ~25 words
    lod_ex = _frost_words(lod, 25) if lod else None

    # Recipe card: serves/prep/total + first 3 ingredients + counts; no steps
    rc_ex = None
    if rc:
        ings = rc.get('ingredients') or []
        steps = rc.get('steps') or []
        rc_ex = {
            'serves': rc.get('serves'),
            'prep': rc.get('prep'),
            'total': rc.get('total'),
            'ingredients_preview': ings[:3],
            'ingredient_count': len(ings),
            'step_count': len(steps),
        }

    frosts = {
        'quality_hierarchy': qh_ex,
        'sensory_tests': st_ex,
        'lives_or_dies': lod_ex,
        'recipe_card': rc_ex,
    }
    has_frost = any(v for v in frosts.values() if v)
    return frosts, has_frost


# ─── Canon Cycle B: recipe card parser ───────────────────────────────────────

def parse_recipe_blob(text):
    """Parse a RECIPE: blob from pro_tips. Returns dict or None on any ambiguity.

    Expected shape:
        RECIPE:
        Serves: N | Prep: X min | Total: Y min
        ---
        ingredient line
        ...
        ---
        1. step line
        ...
    """
    if not text or 'RECIPE:' not in text:
        return None

    idx = text.find('RECIPE:')
    blob = text[idx:]
    lines = blob.split('\n')

    pos = 1  # skip 'RECIPE:' header line

    # Find metadata line (first non-empty line after header)
    while pos < len(lines) and not lines[pos].strip():
        pos += 1
    if pos >= len(lines):
        return None
    meta_line = lines[pos].strip()
    pos += 1

    if 'Serves' not in meta_line:
        return None

    # Parse "Serves: N | Prep: X | Total: Y"
    serves = prep = total = None
    for part in meta_line.split('|'):
        part = part.strip()
        if part.lower().startswith('serves:'):
            serves = part.split(':', 1)[1].strip()
        elif part.lower().startswith('prep:'):
            prep = part.split(':', 1)[1].strip()
        elif part.lower().startswith('total:'):
            total = part.split(':', 1)[1].strip()

    if not serves:
        return None

    # Find first --- delimiter
    while pos < len(lines) and lines[pos].strip() != '---':
        pos += 1
    if pos >= len(lines):
        return None
    pos += 1  # skip ---

    # Collect ingredients until second ---
    ingredients = []
    while pos < len(lines) and lines[pos].strip() != '---':
        line = lines[pos].strip()
        if line:
            ingredients.append(line)
        pos += 1

    if not ingredients or pos >= len(lines):
        return None
    pos += 1  # skip second ---

    # Collect steps to end of blob
    steps = []
    while pos < len(lines):
        line = lines[pos].strip()
        if line:
            clean = _re.sub(r'^\d+[\.\)]\s*', '', line)
            if clean:
                steps.append(clean)
        pos += 1

    if not steps:
        return None

    return {
        'serves': serves,
        'prep': prep,
        'total': total,
        'ingredients': ingredients,
        'steps': steps,
    }


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

    query = "SELECT bp.*, br.name AS region_name, br.country AS region_country FROM beverage_products bp LEFT JOIN beverage_regions br ON bp.region_id = br.id WHERE 1=1 AND bp.is_published IS TRUE"
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
        WHERE bp.id = %s AND bp.is_published IS TRUE
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
        WHERE bpp.product_id = %s AND pr.is_published IS TRUE
    """, (product_id,))
    result["producers"] = [_serialize_row(r) for r in cur.fetchall()]

    # Suppliers
    try:
        cur.execute("""
            SELECT s.id, s.name, s.city, s.state_province, s.country,
                   s.supplier_type, s.website, bps.region, bps.availability
            FROM beverage_product_suppliers bps
            JOIN suppliers s ON bps.supplier_id = s.id AND s.verification_status = 'verified_provider'
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
               WHERE bp.is_published IS TRUE"""
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
        WHERE bp.id = %s AND bp.is_published IS TRUE
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
        WHERE bpp.producer_id = %s AND p.is_published IS TRUE
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
        LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
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
        LEFT JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
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
            model="claude-sonnet-4-6",
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
        return jsonify(error=f"Failed to parse the response: {e}"), 500
    except anthropic.RateLimitError as e:
        return jsonify(error=f"rate limit: {e}"), 429
    except Exception as e:
        return jsonify(error=str(e)), 500


# ─── Beverage browse page ─────────────────────────────────────────────────────

@app.route("/beverage")
def beverage_singular_redirect():
    return redirect("/beverages", code=301)


@app.route("/beverages")
def beverage_browse():
    """The region door — the reader's cellar (Visibility Doctrine / spec v1.1 §3).
    Local by default, global by discovery. Replaces the old Browse by Tradition page."""
    return _render_cellar(None)


@app.route("/beverages/cellar/")
def beverage_cellar_index():
    return redirect("/beverages")


@app.route("/beverages/cellar/<slug>")
def beverage_cellar(slug):
    """The atlas: stand in any other region's cellar. Region guides, never walls."""
    countries = _cellar_countries()
    for c in countries:
        if c["slug"] == slug:
            return _render_cellar(c["country"])
    abort(404)


# The six shelves (founder-approved mockup 1) — producer_type -> shelf.
_SHELVES = [
    ("wine",        "Wine",         ["winery"]),
    ("coffee",      "Coffee",       ["coffee_estate"]),
    ("spirits",     "Spirits",      ["distillery"]),
    ("beer-cider",  "Beer & Cider", ["brewery", "kombucha_brewery"]),
    ("tea",         "Tea",          ["tea_garden"]),
    ("sake",        "Sake",         ["sake_brewery"]),
]

# Reader region token prefix -> beverage country label (as stored in the data).
_TOKEN_COUNTRY = {
    "CA": "Canada", "US": "USA", "AU": "Australia", "NZ": "New Zealand",
    "FR": "France", "IT": "Italy", "JP": "Japan", "DE": "Germany",
    "ES": "Spain", "PT": "Portugal", "AT": "Austria", "GR": "Greece",
    "CN": "China", "TW": "Taiwan", "IN": "India", "MX": "Mexico",
}


def _country_slug(country):
    return _re.sub(r"[^a-z0-9]+", "-", (country or "").lower()).strip("-")


def _cellar_countries():
    """Countries with a published presence, for the atlas. Published-only counts."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT country, SUM(producers) AS producers, SUM(products) AS products FROM (
            SELECT bpr.country, COUNT(*) AS producers, 0 AS products
            FROM beverage_producers bpr
            WHERE bpr.is_published IS TRUE AND bpr.country IS NOT NULL
            GROUP BY bpr.country
            UNION ALL
            SELECT br.country, 0, COUNT(*)
            FROM beverage_products bp
            JOIN beverage_regions br ON bp.region_id = br.id
            WHERE bp.is_published IS TRUE AND br.country IS NOT NULL
            GROUP BY br.country
        ) x GROUP BY country ORDER BY SUM(producers) + SUM(products) DESC
    """)
    out = []
    for r in cur.fetchall():
        out.append({"country": r["country"], "slug": _country_slug(r["country"]),
                    "producers": int(r["producers"]), "products": int(r["products"])})
    cur.close(); conn.close()
    return out


def _render_cellar(country):
    """Render a cellar. country=None -> the reader's own cellar (local by default)."""
    if not DATABASE_URL:
        abort(503)
    reader_token = get_user_location()
    reader_label = dict(VALID_REGIONS).get(reader_token, reader_token)
    home = country is not None
    if country is None:
        country = _TOKEN_COUNTRY.get((reader_token or "").split("-")[0].upper())
    cellar_label = country or "the world"
    if not home and country and reader_token != "global":
        # the reader's own door keeps the province-grain label (spec §2)
        cellar_label = reader_label if reader_token in dict(VALID_REGIONS) else country

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cscope = "AND bpr.country = %(country)s" if country else ""
    params = {"country": country}

    shelves = []
    for key, label, types in _SHELVES:
        cur.execute(f"""
            SELECT bpr.id, bpr.name, bpr.producer_type, bpr.quality_tier,
                   bpr.reputation_narrative, bpr.philosophy_description,
                   br.name AS region_name, bpr.country
            FROM beverage_producers bpr
            LEFT JOIN beverage_regions br ON bpr.region_id = br.id
            WHERE bpr.is_published IS TRUE AND bpr.producer_type = ANY(%(types)s) {cscope}
            ORDER BY (bpr.reputation_narrative IS NOT NULL) DESC, bpr.name
            LIMIT 3
        """, {**params, "types": types})
        rows = [_serialize_row(r) for r in cur.fetchall()]
        cur.execute(f"""
            SELECT COUNT(*) AS n FROM beverage_producers bpr
            WHERE bpr.is_published IS TRUE AND bpr.producer_type = ANY(%(types)s) {cscope}
        """, {**params, "types": types})
        total = cur.fetchone()["n"]
        shelves.append({"key": key, "label": label, "producers": rows, "count": total})

    # honest counts, published only, same scope the shelves use
    cur.execute(f"""
        SELECT COUNT(*) AS n FROM beverage_producers bpr
        WHERE bpr.is_published IS TRUE {cscope}
    """, params)
    total_producers = cur.fetchone()["n"]
    if country:
        cur.execute("""
            SELECT COUNT(*) AS n FROM beverage_products bp
            JOIN beverage_regions br ON bp.region_id = br.id
            WHERE bp.is_published IS TRUE AND br.country = %(country)s
        """, params)
    else:
        cur.execute("SELECT COUNT(*) AS n FROM beverage_products WHERE is_published IS TRUE")
    total_products = cur.fetchone()["n"]
    cur.close(); conn.close()

    countries = _cellar_countries()
    # The atlas invites, it doesn't inventory: full tiles only for cellars with
    # real depth (>=3 published producers, top 12); the long tail collapses.
    ranked = sorted(countries, key=lambda c: (-c["producers"], c["country"]))
    atlas_main = [c for c in ranked if c["producers"] >= 3][:12]
    _main = {c["slug"] for c in atlas_main}
    atlas_rest = sorted((c for c in countries if c["slug"] not in _main),
                        key=lambda c: c["country"])
    return render_template("beverages_cellar.html",
        cellar_label=cellar_label, cellar_country=country, is_home=(not home),
        reader_token=reader_token, reader_label=reader_label,
        shelves=shelves, total_producers=total_producers, total_products=total_products,
        atlas_main=atlas_main, atlas_rest=atlas_rest, valid_regions=VALID_REGIONS,
        canonical_url=("https://provenance.kitchen/beverages" if not home
                       else f"https://provenance.kitchen/beverages/cellar/{_country_slug(country)}"),
    )



# ─── The Pairing Grammar — dish structure → bottles (spec v1.1 §6, mockup 3) ──
# Deterministic and evidence-based: every "why" quotes a real marker from the
# bottle's own flavour data. No category habit — wine, sake, tea, coffee, beer
# and spirits all answer on structural merit.

PAIRING_DISHES = {
    "scallops-vanilla-shiso": {
        "name": "Seared scallops, vanilla nage, shiso tempura",
        "axes": {"weight": 2, "fat": 3, "salt": 2, "acid": 1, "sweet": 2, "smoke": 0, "heat": 0},
        "aromatics": ["vanilla", "shiso", "anise", "herbal", "cream", "brine"],
        "structure_line": "light-to-mid weight · nage fat · sweet shellfish · vanilla and shiso leading",
    },
    "spanish-paella": {
        "name": "Spanish paella",
        "axes": {"weight": 4, "fat": 2, "salt": 3, "acid": 1, "sweet": 1, "smoke": 3, "heat": 1},
        "aromatics": ["saffron", "smoke", "toast", "brine", "pepper"],
        "structure_line": "mid-full weight · socarrat smoke · saffron · sea-salt savour",
    },
    "pnw-clam-chowder": {
        "name": "Pacific Northwest clam chowder",
        "axes": {"weight": 5, "fat": 5, "salt": 4, "acid": 0, "sweet": 1, "smoke": 2, "heat": 0},
        "aromatics": ["brine", "cream", "smoke", "bacon", "thyme"],
        "structure_line": "full weight · cream and bacon fat · clam brine · a thread of smoke",
    },
}

_WEIGHT_MAP = {"light": 1, "medium-light": 2, "medium": 3, "medium-full": 4, "full": 5}

_AXIS_VOCAB = {
    "acid":  ["acid", "acidity", "racy", "crisp", "citrus", "lemon", "lime", "zesty",
              "tart", "green apple", "grapefruit", "yuzu"],
    "carb":  ["sparkling", "bubbles", "mousse", "carbonation", "effervescent", "pétillant", "spritz"],
    "sweet": ["sweet", "off-dry", "honey", "demi-sec", "kabinett", "nigori", "late harvest",
              "botrytis", "ice wine", "jaggery", "caramel", "maple", "apricot", "candied"],
    "tannin": ["tannin", "tannic", "grip", "structured", "black tea", "oak", "cedar", "astringen"],
    "smoke": ["smoke", "smoky", "peat", "peated", "lapsang", "charred", "roasted", "toasted",
              "bonfire", "ember", "mezcal", "gunflint"],
    "umami": ["umami", "savoury", "savory", "koji", "rice", "flor", "yeast", "lees", "broth",
              "mushroom", "seaweed", "dashi"],
    "saline": ["saline", "salinity", "briny", "brine", "maritime", "coastal", "sea spray",
               "oyster", "manzanilla", "fino", "mineral"],
    "cream": ["cream", "creamy", "silk", "silky", "round", "buttery", "texture", "weight"],
}

_CATEGORY_BASE = {
    "wine_sparkling": {"acid": 4, "carb": 5},
    "wine_still": {"acid": 3},
    "wine_fortified": {"umami": 3, "saline": 2},
    "wine_dessert": {"sweet": 5, "acid": 3},
    "sake": {"umami": 4, "cream": 3, "acid": 1},
    "shochu": {"umami": 2},
    "tea": {"tannin": 3},
    "coffee": {"smoke": 2, "tannin": 2},
    "beer_ale": {"carb": 4, "tannin": 1},
    "beer_wild": {"carb": 4, "acid": 4},
    "spirits_whiskey": {"smoke": 2, "tannin": 2},
    "spirits_agave": {"smoke": 3},
    "baijiu": {"umami": 3},
    "na_fermented": {"carb": 3, "acid": 3},
    "na_dealcoholised": {"acid": 2},
}


def _bottle_axes(prod):
    """Derive structural axes + quotable evidence from the bottle's own data."""
    text_bits = []
    markers = prod.get("flavour_markers") or []
    if isinstance(markers, str):
        markers = [m.strip(' "{}') for m in markers.split(",") if m.strip()]
    text_bits.extend(markers)
    dp = prod.get("deductive_profile") or {}
    if isinstance(dp, dict):
        text_bits.extend(str(v) for v in dp.values())
    for f in ("description", "flavour_profile_type", "subcategory", "name"):
        if prod.get(f):
            text_bits.append(str(prod[f]))
    blob = " · ".join(text_bits).lower()

    axes = dict(_CATEGORY_BASE.get(prod.get("category") or "", {}))
    evidence = {}
    for axis, words in _AXIS_VOCAB.items():
        hits = [w for w in words if w in blob]
        if hits:
            axes[axis] = min(5, axes.get(axis, 0) + 1 + len(hits))
            # quote the most specific real marker containing the hit
            src = next((m for m in markers if any(w in str(m).lower() for w in hits)), None)
            evidence[axis] = str(src) if src else None
    axes["weight"] = _WEIGHT_MAP.get(prod.get("flavour_weight") or "", 3)
    aromatics = {str(m).lower() for m in markers}
    return axes, evidence, aromatics


def _grammar_move(dish, axes, evidence, aromatics):
    """Return (move, score, why) for the strongest structural relationship, or
    None. Every why is one honest sommelier sentence; quotes are real markers."""
    d = dish["axes"]
    briny = "brine" in dish["aromatics"]
    cands = []

    def _ev(axis, default):
        m = evidence.get(axis)
        return (f"'{m}'", True) if m else (default, False)

    # CUT — acid, bead or tannin scrubs fat and salt.
    richness = d["fat"] + d["salt"]
    if richness >= 5:
        rich_word = "cream and salt" if d["fat"] >= 4 else ("salt and savour" if d["salt"] >= d["fat"] else "fat")
        agents = [("carb", "the bead", "a fine, persistent bead"),
                  ("acid", "the acidity", "bright acidity")]
        if not briny:  # tannin against brine turns metallic — never the cut agent on a briny dish
            agents.append(("tannin", "the tannin", "fine-grained tannin"))
        for axis, what, default in agents:
            if axes.get(axis, 0) >= 3:
                ev, _ = _ev(axis, default)
                why = (f"Cut — {what} ({ev}) scrubs the {rich_word} between bites; "
                       f"the palate arrives clean at every pass.")
                cands.append(("Cut", axes[axis] + richness * 0.45, why))

    # BRIDGE — every shared note evaluated; the strongest carries.
    if d["smoke"] >= 2 and axes.get("smoke", 0) >= 2:
        ev, _ = _ev("smoke", "a smoky register")
        cands.append(("Bridge", 3.5 + axes["smoke"],
                      f"Bridge — the dish's smoke meets {ev} in the pour; smoke speaking to smoke."))
    if briny and axes.get("saline", 0) >= 2:
        ev, _ = _ev("saline", "a saline edge")
        cands.append(("Bridge", 3.0 + axes["saline"],
                      f"Bridge — the dish's brine meets {ev} in the glass; salt water on both sides."))
    if d["sweet"] >= 2 and 2 <= axes.get("sweet", 0) <= 4:
        ev, _ = _ev("sweet", "gentle sweetness")
        cands.append(("Bridge", 2.5 + axes["sweet"],
                      f"Bridge — the dish's sweetness answers {ev} without either tipping over."))
    if axes.get("umami", 0) >= 3 and (d["salt"] >= 3 or briny):
        ev, _ = _ev("umami", "deep umami")
        cands.append(("Bridge", 2.5 + axes["umami"],
                      f"Bridge — {ev} in the pour meets the dish's savour underneath; depth answering depth."))
    overlap = set()
    for a in dish["aromatics"]:
        for m in aromatics:
            if a in m or (len(m) > 3 and m in a):
                overlap.add(m)
    if overlap:
        m = max(overlap, key=len)
        cands.append(("Bridge", 4.2,
                      f"Bridge — the dish's {next(a for a in dish['aromatics'] if a in m or m in a)} "
                      f"finds '{m}' in the glass; a shared note, carried across."))

    # CONTRAST — an opposition that teaches.
    if d["salt"] >= 3 and axes.get("sweet", 0) >= 3:
        ev, _ = _ev("sweet", "its sweetness")
        cands.append(("Contrast", axes["sweet"] + d["salt"] * 0.4,
                      f"Contrast — set {ev} against the dish's salt and both sharpen; the opposition teaches."))
    elif d["sweet"] >= 2 and d["fat"] >= 3 and axes.get("saline", 0) >= 3 and axes.get("sweet", 0) <= 1:
        ev, _ = _ev("saline", "a mineral cut")
        cands.append(("Contrast", axes["saline"] + 1,
                      f"Contrast — bone-dry and saline ({ev}) against a sweet, creamy plate; "
                      f"each makes the other speak louder."))

    if not cands:
        return None
    move, score, why = max(cands, key=lambda c: c[1])
    # weight agreement nudges the rank, never creates a match
    score += 1.5 - abs(axes.get("weight", 3) - d["weight"]) * 0.3
    return move, score, why

# ── The dish door (cycle 2.2): Library-first search + chef-built structure ──

_DISH_VOCAB = {
    "fat":   ["butter", "cream", "lard", "guanciale", "bacon", "pork belly", "duck fat", "confit",
              "coconut milk", "cheese", "egg yolk", "yolk", "fried", "tempura", "ghee", "aioli",
              "mayonnaise", "marbl", "sausage", "chorizo", "olive oil", "brown butter"],
    "salt":  ["cured", "brined", "soy", "fish sauce", "miso", "anchov", "salted", "caper",
              "olive", "parmesan", "pecorino", "prosciutto", "salt", "nam pla", "bottarga", "feta"],
    "acid":  ["vinegar", "citrus", "lime", "lemon", "tamarind", "yuzu", "pickle", "sour",
              "verjus", "sumac", "kefir", "buttermilk", "gastrique"],
    "sweet": ["sugar", "honey", "caramel", "mirin", "sweet", "jaggery", "palm sugar", "glaze",
              "maple", "molasses", "hoisin", "kecap manis", "date"],
    "smoke": ["smoked", "smoke", "grill", "char", "barbecue", "bbq", "socarrat", "tandoor",
              "ember", "fire-roasted", "burnt", "bonfire", "lapsang"],
    "heat":  ["chili", "chilli", "cayenne", "gochujang", "sambal", "spicy", "harissa",
              "sichuan", "peppercorn", "black pepper", "jalape", "bird's eye", "wasabi"],
}
_DISH_HEAVY = ["braise", "stew", "roast", "confit", "short rib", "oxtail", "cassoulet",
               "gratin", "chowder", "ragu", "rag\u00f9", "curry", "lasagn", "daube"]
_DISH_LIGHT = ["salad", "crudo", "ceviche", "raw", "steam", "poach", "broth", "consomm",
               "tartare", "carpaccio", "sashimi", "granita"]
_DISH_AROMATIC = ["vanilla", "shiso", "saffron", "basil", "thyme", "rosemary", "anise",
                  "fennel", "dill", "mint", "coriander", "cilantro", "lemongrass", "ginger",
                  "truffle", "mushroom", "cherry", "apple", "cardamom", "cinnamon", "nutmeg",
                  "star anise", "kaffir", "makrut", "juniper", "sage", "tarragon", "oregano",
                  "smoke", "brine", "toast", "pepper", "cream", "bacon"]
_DISH_BRINE = ["clam", "oyster", "mussel", "scallop", "anchov", "seaweed", "kombu", "dashi",
               "fish sauce", "shellfish", "prawn", "shrimp", "crab", "uni", "roe", "brine",
               "nori", "sea urchin", "squid", "octopus"]


def _dish_axes_from_text(name, blob):
    """Derive the eight structural axes from Library text. Deterministic,
    evidence-counted; never invents what the text does not say."""
    low = (name + " \u00b7 " + blob).lower()
    axes = {}
    for axis, words in _DISH_VOCAB.items():
        hits = sum(1 for w in words if w in low)
        axes[axis] = min(5, hits and hits + 1)
    weight = 3
    weight += sum(1 for w in _DISH_HEAVY if w in low)
    weight -= sum(1 for w in _DISH_LIGHT if w in low)
    axes["weight"] = max(1, min(5, weight))
    aromatics = [a for a in _DISH_AROMATIC if a in low]
    if any(b in low for b in _DISH_BRINE) and "brine" not in aromatics:
        aromatics.append("brine")
    return axes, aromatics[:8]


_MORNING_TOKENS = ["breakfast", "viennoiserie", "morning", "brunch", "petit d\u00e9jeuner",
                   "petit dejeuner", "congee", "tamago kake gohan", "porridge",
                   # ruling 2.4(b): a text stating a named morning serve signals
                   # morning service exactly as "breakfast" does \u2014 stated, not inferred
                   "caf\u00e9 au lait", "cafe au lait", "espresso", "cappuccino",
                   "flat white", "macchiato", "americano", "breakfast tea",
                   "english breakfast"]


def _dish_service_context(blob):
    """Meal-context axis (ruling 2.3a): derived from the entry's own text only —
    never invented. Ambiguous -> None (no alcohol filter)."""
    low = blob.lower()
    if any(t in low for t in _MORNING_TOKENS):
        return "morning"
    return None


def _dish_from_technique(tid):
    """Library-first: read a technique's structure from the platform's own data."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, slug, origin, description, flavour_context, recipe_card
        FROM technique_references
        WHERE id = %s AND published IS NOT FALSE
    """, (tid,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return None
    blob = " ".join(str(row.get(f) or "") for f in ("description", "flavour_context"))
    if row.get("recipe_card"):
        blob += " " + str(row["recipe_card"])
    axes, aromatics = _dish_axes_from_text(row["name"], blob)
    context = _dish_service_context(row["name"] + " " + blob)
    line = " \u00b7 ".join(f"{k} {axes[k]}" for k in
                            ("weight", "fat", "salt", "acid", "sweet", "smoke", "heat"))
    return {
        "name": row["name"],
        "axes": axes,
        "aromatics": aromatics,
        "context": context,
        "structure_line": f"read from the Library entry \u2014 {line}"
                          + (f" \u00b7 aromatics: {', '.join(aromatics)}" if aromatics else "")
                          + (f" \u00b7 service: {context}" if context else ""),
        "tid": row["id"],
    }


def _dish_from_params(args):
    """Chef's own structure: the eight controls, set by hand. No inference."""
    axes = {}
    for k in ("weight", "fat", "salt", "acid", "sweet", "smoke", "heat"):
        try:
            axes[k] = max(0, min(5, int(args.get(k, 0))))
        except (TypeError, ValueError):
            axes[k] = 0
    axes["weight"] = max(1, axes["weight"] or 3)
    aromatics = [a.strip().lower() for a in (args.get("aromatic") or "").split(",") if a.strip()][:8]
    line = " \u00b7 ".join(f"{k} {axes[k]}" for k in
                            ("weight", "fat", "salt", "acid", "sweet", "smoke", "heat"))
    return {
        "name": args.get("plate_name") or "Your plate",
        "axes": axes,
        "aromatics": aromatics,
        "structure_line": f"your plate, as set \u2014 {line}"
                          + (f" \u00b7 aromatics: {', '.join(aromatics)}" if aromatics else ""),
    }


def _grammar_resolve(dish, reader_token, limit=6, per_cat_cap=2):
    """Resolve a dish structure against the published cellar. Shared by the
    pairing room and the interim bridge (founder ruling 2.1): returns picks
    [{move, why, product, carried}] — the cellar's deduction, never editorial."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bp.id, bp.name, bp.slug, bp.category, bp.subcategory, bp.description,
               bp.flavour_markers, bp.flavour_weight, bp.flavour_profile_type,
               bp.deductive_profile, bp.quality_tier,
               bpr.name AS producer_name, br.name AS region_name, br.country
        FROM beverage_products bp
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.is_published IS TRUE
    """)
    products = [_serialize_row(r) for r in cur.fetchall()]

    # Ruling 2.4: pairings name DRINKS, not beans. Canonical serves come from
    # beverage_preparations; coffee/tea PRODUCTS never surface as picks —
    # they may only appear as the expression of a serve.
    preparations = []
    try:
        cur.execute("""
            SELECT id, name, slug, category, description, flavour_markers,
                   flavour_weight, flavour_profile_type, deductive_profile
            FROM beverage_preparations WHERE is_published IS TRUE
        """)
        preparations = [_serialize_row(r) for r in cur.fetchall()]
    except Exception:
        pass  # table may not exist on live until the migration rides

    _SERVE_FAMS = {"coffee", "tea"}
    scored, expr_best = [], {}
    for prod in products:
        axes, evidence, aromatics = _bottle_axes(prod)
        res = _grammar_move(dish, axes, evidence, aromatics)
        if not res:
            continue
        move, score, why = res
        fam = (prod.get("category") or "").split("_")[0]
        if fam in _SERVE_FAMS:
            # bean/leaf: candidate EXPRESSION only, never the pick itself
            cur_best = expr_best.get(prod.get("category"))
            if cur_best is None or score > cur_best[0]:
                expr_best[prod.get("category")] = (score, prod)
            continue
        scored.append((score, move, why, prod))
    for prep in preparations:
        axes, evidence, aromatics = _bottle_axes(prep)
        res = _grammar_move(dish, axes, evidence, aromatics)
        if res:
            move, score, why = res
            prep["is_preparation"] = True
            scored.append((score, move, why, prep))
    scored.sort(key=lambda t: -t[0])

    _NA_FAMS = {"coffee", "tea", "na", "water"}

    def _fam(prod):
        return (prod.get("category") or "").split("_")[0]

    def _fill(cands, limit_n, per_cat, picks, quiet=False):
        for score, move, why, prod in cands:
            cat = _fam(prod)
            if per_cat.get(cat, 0) >= per_cat_cap:
                continue
            picks.append({"move": move, "why": why, "product": prod,
                          "score": round(score, 2), "quiet": quiet})
            per_cat[cat] = per_cat.get(cat, 0) + 1
            if len(picks) >= limit_n:
                break

    picks, per_cat = [], {}
    if dish.get("context") == "morning":
        # Ruling 2.3a: morning dishes answer FIRST with coffee, tea and other
        # morning-appropriate pours; alcohol only behind them, quietly.
        na = [c for c in scored if _fam(c[3]) in _NA_FAMS]
        # coffee and tea are the morning pours of record — they lead within NA
        na.sort(key=lambda c: -(c[0] + (1.5 if _fam(c[3]) in ("coffee", "tea") else 0)))
        # round-robin by family (2.4 proof: "a tea by serve" must seat when it
        # holds a move) — best of each NA family first, then second-bests
        by_fam = {}
        for c in na:
            by_fam.setdefault(_fam(c[3]), []).append(c)
        rr = []
        rnd = 0
        while any(len(v) > rnd for v in by_fam.values()):
            for f in ("coffee", "tea", "na", "water"):
                if f in by_fam and len(by_fam[f]) > rnd:
                    rr.append(by_fam[f][rnd])
            rnd += 1
        _fill(rr, limit, per_cat, picks)
        alc = [c for c in scored if _fam(c[3]) not in _NA_FAMS]
        _fill(alc, min(len(picks) + 2, limit + 2), per_cat, picks, quiet=True)
    else:
        _fill(scored, limit, per_cat, picks)
        # Every dish's answer includes a non-alcoholic pour whenever one can
        # honestly bridge or cut (ruling 2.3a) — NA is a first-class citizen.
        if picks and not any(_fam(p["product"]) in _NA_FAMS for p in picks):
            best_na = next((c for c in scored if _fam(c[3]) in _NA_FAMS), None)
            if best_na:
                score, move, why, prod = best_na
                picks[-1] = {"move": move, "why": why, "product": prod,
                             "score": round(score, 2), "quiet": False}
    # a serve is expressed through a published bean/leaf where one earned a move
    for p in picks:
        prod = p["product"]
        if prod.get("is_preparation"):
            p["is_preparation"] = True
            exp = expr_best.get(prod.get("category"))
            if exp:
                # coffee: any bean honestly expresses the serve; tea: only a
                # leaf of the same style (serve name inside the product name)
                if prod.get("category") == "tea":
                    if prod["name"].split()[0].lower() in exp[1]["name"].lower():
                        p["expression"] = exp[1]["name"]
                else:
                    p["expression"] = exp[1]["name"]
    ids = [p["product"]["id"] for p in picks if not p.get("is_preparation")]
    carried = set()
    if ids:
        cur.execute("""
            SELECT DISTINCT bps.product_id
            FROM beverage_product_suppliers bps
            JOIN suppliers s ON s.id = bps.supplier_id
                 AND s.verification_status = 'verified_provider'
            WHERE bps.product_id = ANY(%s) AND %s = ANY(bps.region)
        """, (ids, reader_token))
        carried = {r["product_id"] for r in cur.fetchall()}
    cur.close(); conn.close()
    for p in picks:
        # a serve is a drink, not a bottle — the §4 carried mark doesn't apply
        p["carried"] = True if p.get("is_preparation") else (p["product"]["id"] in carried)
    return picks


@app.route("/api/pairing/dish-search")
def pairing_dish_search():
    """Library-first search for the dish door. Published entries only."""
    if not DATABASE_URL:
        return jsonify([])
    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify([])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, origin,
               similarity(lower(name), lower(%s)) AS sim
        FROM technique_references
        WHERE published IS NOT FALSE
          AND (lower(name) ILIKE %s OR similarity(lower(name), lower(%s)) > 0.25)
        ORDER BY sim DESC, name
        LIMIT 10
    """, (q, f"%{q.lower()}%", q))
    rows = [{"id": r["id"], "name": r["name"], "origin": (r["origin"] or "").split(",")[0][:40]}
            for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(rows)


from urllib.parse import quote as _q


@app.route("/beverages/pairing")
def pairing_room():
    """The pairing room — start with the plate (spec v1.1 §6, mockup 3)."""
    if not DATABASE_URL:
        abort(503)
    # The dish door: Library entry (tid) > chef-built plate (custom) > worked example
    dish_key = request.args.get("dish")
    dish_source = "example"
    tid = request.args.get("tid", type=int)
    if tid:
        dish = _dish_from_technique(tid)
        if dish is None:
            abort(404)
        dish_key = None
        dish_source = "library"
    elif request.args.get("custom"):
        dish = _dish_from_params(request.args)
        dish_key = None
        dish_source = "custom"
    else:
        dish_key = dish_key or "scallops-vanilla-shiso"
        dish = PAIRING_DISHES.get(dish_key)
        if dish is None:
            abort(404)
    reader_token = get_user_location()
    reader_label = dict(VALID_REGIONS).get(reader_token, reader_token)

    picks = _grammar_resolve(dish, reader_token)

    # cycle 3.1: bottles opened from the room carry the plate home with them
    _plate_keys = ("dish", "tid", "custom", "weight", "fat", "salt", "acid",
                   "sweet", "smoke", "heat", "aromatic", "plate_name")
    plate_qs = "&".join(f"{k}={_q(str(request.args[k]))}"
                        for k in _plate_keys if request.args.get(k)) or (f"dish={dish_key}" if dish_key else "")
    return render_template("pairing_room.html",
        dishes=PAIRING_DISHES, dish_key=dish_key, dish=dish, picks=picks,
        plate_qs=plate_qs,
        dish_source=dish_source, tid=tid,
        reader_token=reader_token, reader_label=reader_label,
        canonical_url="https://provenance.kitchen/beverages/pairing"
                      + (f"?dish={dish_key}" if dish_key else ""))


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
        abort(404)
    region = _serialize_row(region)

    cur.execute("SELECT * FROM beverage_regions WHERE parent_region_id = %s ORDER BY name", (region_id,))
    sub_regions = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT bp.*, bpr.name AS producer_name
        FROM beverage_products bp
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
        WHERE bp.region_id = %s AND bp.is_published IS TRUE
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
        WHERE bp.id = %s AND bp.is_published IS TRUE
    """, (product_id,))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        abort(404)
    product = _serialize_row(product)

    cur.execute("""
        SELECT pr.* FROM beverage_producers pr
        JOIN beverage_product_producers bpp ON pr.id = bpp.producer_id
        WHERE bpp.product_id = %s AND pr.is_published IS TRUE
    """, (product_id,))
    producers = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT pi.* FROM pairing_intelligence pi
        WHERE pi.beverage_product_id = %s
        ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 ELSE 3 END
    """, (product_id,))
    pairings = [_serialize_row(r) for r in cur.fetchall()]

    recipes_using = []
    try:
        recipes_using = _recipes_using_beverage(product_id, cur)
    except Exception as e:
        app.logger.warning(f"recipes-using lookup failed for beverage {product_id}: {e}")

    # navigation seams (cycle 3.1): the bottle knows its cellar and its shelf
    _SHELF_OF = {"wine": "wine", "coffee": "coffee", "tea": "tea", "sake": "sake",
                 "beer": "beer-cider", "spirits": "spirits", "baijiu": "spirits",
                 "shochu": "spirits"}
    shelf_key = _SHELF_OF.get((product.get("category") or "").split("_")[0])
    cellar_slug = _country_slug(product.get("region_country")) if product.get("region_country") else None
    plate_qs = (request.args.get("plate") or "").strip() or None

    # Pat's Rule: verified providers for the reader's region (Visibility Doctrine).
    reader_region = get_user_location()
    providers = []
    try:
        cur.execute("""
            SELECT s.id, s.name, s.website, s.city, s.state_province, s.country,
                   bps.region, bps.availability
            FROM beverage_product_suppliers bps
            JOIN suppliers s ON bps.supplier_id = s.id
                 AND s.verification_status = 'verified_provider'
            WHERE bps.product_id = %s
        """, (product_id,))
        for r in cur.fetchall():
            r = _serialize_row(r)
            regs = r.get("region") or []
            if not regs or reader_region == "global" or reader_region in regs:
                providers.append(r)
    except Exception as e:
        app.logger.warning(f"providers lookup failed for beverage {product_id}: {e}")

    cur.close()
    conn.close()

    # No local provider → this view is a demand signal (the gap is the signal).
    if not providers:
        _fire_demand_event("view", product_id=product_id,
                           origin_region=(product.get("region_name") or product.get("region_country")))

    product_slug = product.get('slug') or _slugify(product['name'])
    canonical_url = f"https://provenance.kitchen/beverage/{product_slug}"
    return render_template("beverage_product.html",
        product=product, producers=producers, pairings=pairings,
        recipes_using=recipes_using, providers=providers,
        reader_region=reader_region, shelf_key=shelf_key,
        cellar_slug=cellar_slug, plate_qs=plate_qs,
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
        WHERE bp.id = %s AND bp.is_published IS TRUE
    """, (producer_id,))
    producer = cur.fetchone()
    if not producer:
        cur.close(); conn.close()
        abort(404)
    producer = _serialize_row(producer)

    cur.execute("""
        SELECT p.id, p.name, p.category, p.quality_tier, p.description,
               br.name AS region_name, br.id AS region_id
        FROM beverage_products p
        JOIN beverage_product_producers bpp ON p.id = bpp.product_id
        LEFT JOIN beverage_regions br ON p.region_id = br.id
        WHERE bpp.producer_id = %s AND p.is_published IS TRUE
        ORDER BY p.quality_tier, p.name
    """, (producer_id,))
    products = [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    # Visibility Doctrine §3: no local provider wired yet → this view is a demand signal.
    _fire_demand_event("view", producer_id=producer_id,
                       origin_region=producer.get("region_name") or producer.get("country"))

    canonical_url = f"https://provenance.kitchen/beverage/producers/{producer_id}"
    return render_template("beverage_producer.html",
        producer=producer, products=products, canonical_url=canonical_url)


# ─── Visibility Doctrine: demand ledger + supplier onboarding (spec v1.1 §7/§8) ──

def _fire_demand_event(kind, *, product_id=None, producer_id=None,
                       origin_region=None, search_terms=None):
    """Best-effort demand-ledger write. Region only — never personal data.
    Fire-and-forget: any failure is swallowed so it can never break a page."""
    if not DATABASE_URL_WRITE:
        return
    try:
        reader_region = get_user_location()
    except Exception:
        reader_region = "global"
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO beverage_demand_ledger
                 (product_id, producer_id, origin_region, reader_region,
                  event_kind, search_terms, local_provider_absent)
               VALUES (%s, %s, %s, %s, %s, %s, TRUE)""",
            (product_id, producer_id, origin_region, reader_region, kind, search_terms),
        )
        cur.close()
    except Exception as e:
        try:
            sentry_sdk.capture_exception(e)
        except Exception:
            pass
    finally:
        if conn:
            conn.close()


@app.route("/beverages/suggest-supplier", methods=["POST"])
def suggest_supplier():
    """Suggest-a-Supplier (spec §8B). One tap, four fields. Every suggestion:
    enters the verification queue at SUGGESTED, fires a demand-ledger event,
    is attributed to the suggesting member (queue row only, never the ledger)."""
    if not DATABASE_URL_WRITE:
        return jsonify(error="unavailable"), 503
    data = request.get_json(silent=True) or request.form
    business_name = (data.get("business_name") or "").strip()
    if not business_name:
        return jsonify(error="business name required"), 400
    region = (data.get("region") or "").strip() or get_user_location()
    website = (data.get("website") or "").strip() or None
    note = (data.get("note") or "").strip() or None
    ctx_product = data.get("product_id") or None
    ctx_producer = data.get("producer_id") or None
    try:
        ctx_product = int(ctx_product) if ctx_product else None
    except (TypeError, ValueError):
        ctx_product = None
    try:
        ctx_producer = int(ctx_producer) if ctx_producer else None
    except (TypeError, ValueError):
        ctx_producer = None
    user = get_current_user()
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO supplier_verification_queue
                 (business_name, website, claimed_regions, source,
                  suggested_by_user_id, context_product_id, context_producer_id,
                  note, status)
               VALUES (%s, %s, %s, 'member_suggestion', %s, %s, %s, %s, 'suggested')""",
            (business_name, website, [region] if region else None,
             user.get("id") if user else None, ctx_product, ctx_producer, note),
        )
        cur.close()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return jsonify(error="could not record"), 500
    finally:
        if conn:
            conn.close()
    # Fire the demand-ledger 'suggestion' event (region only — attribution stays in the queue).
    _fire_demand_event("suggestion", product_id=ctx_product, producer_id=ctx_producer)
    return jsonify(ok=True, message="Noted — if the checks confirm them, your cellar gets deeper.")


@app.route("/admin/beverages/onboard")
def admin_beverages_onboard():
    """The assisted lane (spec §8C) + the suggestion pipeline. Admin-only.
    Lists the verification queue; the founder rules on it. Read-only view for
    now (verification checks + product wiring are the next increment)."""
    g = _admin_guard()
    if g:
        return g
    if (get_current_user() or {}).get("role") not in ("admin", "founder"):
        abort(403)
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT q.*,
               bp.name  AS product_name,
               bpr.name AS producer_name
        FROM supplier_verification_queue q
        LEFT JOIN beverage_products  bp  ON bp.id  = q.context_product_id
        LEFT JOIN beverage_producers bpr ON bpr.id = q.context_producer_id
        ORDER BY
          CASE q.status WHEN 'suggested' THEN 1 WHEN 'checks_running' THEN 2
                        WHEN 'verified_listed' THEN 3 WHEN 'claim_pending' THEN 4
                        WHEN 'flagged' THEN 5 ELSE 6 END,
          q.created_at DESC
        LIMIT 500
    """)
    queue = [_serialize_row(r) for r in cur.fetchall()]
    cur.execute("SELECT status, COUNT(*) AS n FROM supplier_verification_queue GROUP BY status")
    counts = {r["status"]: r["n"] for r in cur.fetchall()}
    cur.close(); conn.close()
    return render_template("admin_beverages_onboard.html", queue=queue, counts=counts)


def _run_supplier_checks(business_name, website, claimed_regions):
    """The automated VERIFIED-LISTED checks (spec §8A) — HONEST about limits.
    Verifies existence/identity/region. Does NOT verify merit or stock.
    Returns (results_dict, passed_bool, flag_reason_or_None)."""
    results = {}
    passed_site = False
    passed_identity = False
    # 1 · website liveness + valid TLS
    if not website:
        results["website"] = {"status": "fail", "detail": "no website provided"}
    else:
        url = website if website.startswith("http") else "https://" + website
        try:
            import requests as _rq
            r = _rq.get(url, timeout=8, allow_redirects=True,
                        headers={"User-Agent": "ProvenanceVerifier/1.0"})
            tls_ok = r.url.startswith("https://")
            passed_site = (r.status_code < 400)
            results["website"] = {
                "status": "pass" if passed_site else "fail",
                "http_status": r.status_code, "final_url": r.url, "tls": tls_ok,
            }
            # 2 · identity — business name tokens appear in the page
            body = (r.text or "").lower()
            toks = [t for t in _re.split(r"[^a-z0-9]+", business_name.lower()) if len(t) >= 3]
            hits = sum(1 for t in toks if t in body)
            passed_identity = bool(toks) and hits >= max(1, len(toks) // 2)
            results["identity"] = {
                "status": "pass" if passed_identity else "flag",
                "detail": f"{hits}/{len(toks)} name tokens found on page",
            }
        except Exception as e:
            results["website"] = {"status": "fail", "detail": f"unreachable: {type(e).__name__}"}
    # 3 · region — claimed, not independently confirmable here
    results["region"] = {
        "status": "claimed" if claimed_regions else "missing",
        "detail": (", ".join(claimed_regions) if claimed_regions else "no region claimed"),
    }
    # 4 · registry cross-check — honest: no automated registry wired
    results["registry"] = {"status": "unchecked",
                           "detail": "no automated registry for this jurisdiction — manual confirm"}
    passed = passed_site and passed_identity and bool(claimed_regions)
    flag = None
    if not passed:
        why = []
        if not passed_site: why.append("website not live/identifiable")
        if not passed_identity: why.append("business name not found on site")
        if not claimed_regions: why.append("no region")
        flag = "; ".join(why)
    return results, passed, flag


@app.route("/admin/beverages/verify/<int:qid>", methods=["POST"])
def admin_beverages_verify(qid):
    """Run the automated checks on a queue row → verified_listed or flagged."""
    g = _admin_guard_api()
    if g:
        return g
    if (get_current_user() or {}).get("role") not in ("admin", "founder"):
        return jsonify(error="forbidden"), 403
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM supplier_verification_queue WHERE id = %s", (qid,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify(error="not found"), 404
    results, passed, flag = _run_supplier_checks(
        row["business_name"], row.get("website"), row.get("claimed_regions") or [])
    new_status = "verified_listed" if passed else "flagged"
    wconn = psycopg2.connect(DATABASE_URL_WRITE); wconn.autocommit = True
    wcur = wconn.cursor()
    wcur.execute(
        """UPDATE supplier_verification_queue
             SET status = %s, check_results = %s, flag_reason = %s
           WHERE id = %s""",
        (new_status, psycopg2.extras.Json(results), flag, qid))
    wcur.close(); wconn.close()
    cur.close(); conn.close()
    return jsonify(ok=True, status=new_status, check_results=results, flag_reason=flag)


@app.route("/admin/beverages/product-search")
def admin_beverages_product_search():
    """Fuzzy product search for the wiring UI (published products only)."""
    g = _admin_guard_api()
    if g:
        return g
    if (get_current_user() or {}).get("role") not in ("admin", "founder"):
        return jsonify(error="forbidden"), 403
    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify([])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bp.id, bp.name, bp.category, bpr.name AS producer_name, br.name AS region_name
        FROM beverage_products bp
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.is_published IS TRUE AND bp.name ILIKE %s
        ORDER BY bp.name LIMIT 20
    """, (f"%{q}%",))
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(rows)


@app.route("/admin/beverages/wire/<int:qid>", methods=["POST"])
def admin_beverages_wire(qid):
    """The assisted lane's wiring (spec §8C): create/select the supplier,
    insert beverage_product_suppliers rows for the confirmed products, and
    promote to VERIFIED PROVIDER — gold links go live for its region."""
    g = _admin_guard_api()
    if g:
        return g
    if (get_current_user() or {}).get("role") not in ("admin", "founder"):
        return jsonify(error="forbidden"), 403
    data = request.get_json(silent=True) or {}
    product_ids = data.get("product_ids") or []
    supplier_type = (data.get("supplier_type") or "distributor").strip()
    if supplier_type not in ("producer", "importer", "distributor", "retailer", "direct_to_chef"):
        supplier_type = "distributor"
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM supplier_verification_queue WHERE id = %s", (qid,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        return jsonify(error="not found"), 404
    if row["status"] not in ("verified_listed", "claim_pending", "verified_provider"):
        return jsonify(error="run checks first — must be verified_listed"), 409
    regions = row.get("claimed_regions") or []
    wconn = psycopg2.connect(DATABASE_URL_WRITE); wconn.autocommit = True
    wcur = wconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # create/select the supplier (verified_provider — the claim is completed here, §8C)
        wcur.execute("SELECT id FROM suppliers WHERE lower(name) = lower(%s) LIMIT 1",
                     (row["business_name"],))
        s = wcur.fetchone()
        if s:
            supplier_id = s["id"]
            wcur.execute("""UPDATE suppliers SET verification_status='verified_provider',
                              verified_date=NOW(), verification_source='onboard',
                              website=COALESCE(website,%s), supplier_type=%s WHERE id=%s""",
                         (row.get("website"), supplier_type, supplier_id))
        else:
            # country is NOT NULL on suppliers; derive from the region token
            # (e.g. 'CA-BC' -> 'CA'); service_region is text[].
            country = "Unknown"
            if regions:
                country = regions[0].split("-")[0].upper() or "Unknown"
            wcur.execute("""INSERT INTO suppliers
                              (name, website, country, service_region, supplier_type,
                               verification_status, verified_date, verification_source, is_active)
                            VALUES (%s,%s,%s,%s,%s,'verified_provider',NOW(),'onboard',TRUE)
                            RETURNING id""",
                         (row["business_name"], row.get("website"), country,
                          regions or None, supplier_type))
            supplier_id = wcur.fetchone()["id"]
        wired = 0
        for pid in product_ids:
            try:
                pid = int(pid)
            except (TypeError, ValueError):
                continue
            wcur.execute("""INSERT INTO beverage_product_suppliers
                              (product_id, supplier_id, role, region, availability, last_verified)
                            VALUES (%s,%s,'provider',%s,'stocked',NOW())
                            ON CONFLICT DO NOTHING""",
                         (pid, supplier_id, regions or None))
            wired += 1
        wcur.execute("""UPDATE supplier_verification_queue
                          SET status='verified_provider', resolved_at=NOW() WHERE id=%s""", (qid,))
    except Exception as e:
        sentry_sdk.capture_exception(e)
        wcur.close(); wconn.close()
        return jsonify(error="wiring failed"), 500
    wcur.close(); wconn.close()
    return jsonify(ok=True, supplier_id=supplier_id, products_wired=wired,
                   status="verified_provider",
                   message="Gold links live for this region — the supplier can see their listing now.")


@app.route("/beverage/producers/<path:rest>")
def legacy_producer_slug(rest):
    return "<h1>Gone</h1>", 410


@app.route("/beverage/regions/<path:rest>")
def legacy_region_slug(rest):
    return "<h1>Gone</h1>", 410


# ─── Technique public page ────────────────────────────────────────────────────

@app.route("/technique/<slug>")
def technique_page(slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_references WHERE slug = %s AND published IS NOT FALSE", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close()
        conn.close()
        abort(404)
    technique = _serialize_row(technique)

    # Normalize cross_cuisine_parallels to always be a list for the template
    ccp = technique.get('cross_cuisine_parallels')
    if ccp is not None:
        if isinstance(ccp, str):
            technique['cross_cuisine_parallels'] = [ccp] if ccp.strip() else []
        elif not isinstance(ccp, list):
            technique['cross_cuisine_parallels'] = list(ccp)

    # Step 0b: Resolve Thread links — mark _slug only for technique codes that
    # exist as real slugs. Unresolved codes render as plain text in the template.
    _ccp = technique.get('cross_cuisine_parallels') or []
    if isinstance(_ccp, list) and _ccp:
        _tech_codes = [item['technique'].lower() for item in _ccp
                       if isinstance(item, dict) and item.get('technique')]
        if _tech_codes:
            cur.execute("SELECT slug FROM technique_references WHERE slug = ANY(%s)",
                        (_tech_codes,))
            _valid_slugs = {r['slug'] for r in cur.fetchall()}
        else:
            _valid_slugs = set()
        for item in _ccp:
            if isinstance(item, dict):
                _code = (item.get('technique') or '').lower()
                item['_slug'] = _code if _code in _valid_slugs else None

    # Related: same cuisine/origin, excluding self — cap at 6, deduped by slug
    related_techniques = []
    if technique.get('origin'):
        cur.execute("""
            SELECT id, name, slug, category, description, origin, authority_tier
            FROM technique_references
            WHERE origin = %s AND id != %s
            ORDER BY authority_tier ASC, name
            LIMIT 12
        """, (technique['origin'], technique['id']))
        _seen_slugs = set()
        for _r in cur.fetchall():
            _row = _serialize_row(_r)
            if _row['slug'] not in _seen_slugs:
                _seen_slugs.add(_row['slug'])
                related_techniques.append(_row)
            if len(related_techniques) >= 6:
                break

    # Fetch Pat's Rule ingredients for this technique
    cur.execute("""
        SELECT ti.ingredient_name, ti.origin_brand, ti.tier, ti.display_order,
               s.name AS supplier_name
        FROM technique_ingredients ti
        LEFT JOIN suppliers s ON s.id = ti.provider_supplier_id
        WHERE ti.technique_id = %s
        ORDER BY ti.display_order, ti.id
    """, (technique['id'],))
    technique_ingredients = [dict(r) for r in cur.fetchall()]

    # Fetch technique-beverage pairings (Tier 1 editorial + Tier 2 partial)
    user = get_current_user()
    user_tier = user.get("subscription_tier", "free") if user else "free"
    user_region = user.get("region", "") if user else ""

    _tbp_base = """
        SELECT tbp.id, tbp.pairing_type, tbp.pairing_rationale,
               tbp.confidence_status, tbp.display_order,
               bp.id   AS product_id,
               bp.name AS product_name,
               bp.slug AS product_slug,
               bp.category AS product_category,
               bpr.name AS producer_name,
               br.name  AS region_name
        FROM technique_beverage_pairings tbp
        LEFT JOIN beverage_products  bp  ON tbp.beverage_product_id = bp.id
             AND bp.is_published IS TRUE
        LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, tbp.beverage_producer_id) = bpr.id
             AND bpr.is_published IS TRUE
        LEFT JOIN beverage_regions   br  ON bp.region_id = br.id
        WHERE tbp.technique_id = %s
          AND (tbp.beverage_producer_id IS NULL OR bpr.id IS NOT NULL)
          AND (tbp.beverage_product_id IS NULL OR bp.id IS NOT NULL)
    """
    _tbp_order = """
        ORDER BY
            CASE tbp.confidence_status
                WHEN 'editorial'  THEN 1
                WHEN 'reviewed'   THEN 2
                WHEN 'unverified' THEN 3
                WHEN 'partial'    THEN 3
                ELSE 4
            END,
            tbp.display_order, tbp.id
    """
    if user_region:
        cur.execute(
            _tbp_base + """
              AND (tbp.region_filter IS NULL
                   OR tbp.region_filter->'include' = '[]'::jsonb
                   OR tbp.region_filter->'include' ? %s)
            """ + _tbp_order,
            (technique['id'], user_region),
        )
    else:
        cur.execute(_tbp_base + _tbp_order, (technique['id'],))

    _all_pairings = [_serialize_row(r) for r in cur.fetchall()]
    technique_pairings_editorial = [p for p in _all_pairings if p['confidence_status'] in ('editorial', 'reviewed')]
    # Spec v1.1 §6: unverified renders on admin/staging surfaces only —
    # founders/admins see it (to sign off); the public does not.
    _viewer_role = (get_current_user() or {}).get('role')
    if _viewer_role in ('admin', 'founder'):
        technique_pairings_partial = [p for p in _all_pairings
                                      if p['confidence_status'] in ('partial', 'unverified')]
    else:
        technique_pairings_partial = []
    # Founder ruling 2.1 — the interim bridge: where no editorial pairing
    # exists, the block renders the grammar's live deduction, honestly
    # labeled. Editorial replaces deduction as the founder signs off.
    technique_pairings_deduction = []
    if not technique_pairings_editorial:
        try:
            _bridge_dish = _dish_from_technique(technique['id'])
            if _bridge_dish:
                technique_pairings_deduction = _grammar_resolve(
                    _bridge_dish, user_region or get_user_location(), limit=4)
        except Exception as _bridge_e:
            app.logger.warning(f"pairing bridge failed for technique {technique['id']}: {_bridge_e}")

    # Cycle E: Pat's Rule — match recipe ingredients against pantry for members.
    # Computed at render; no writes. Free viewers get nothing (recipe_card stripped).
    # Structural guard: ANY failure returns {} so the page never goes down.
    ingredient_origins = {}
    if user_tier != 'free':
        _rc = technique.get('recipe_card')
        if _rc and isinstance(_rc, dict):
            _ings = [i for i in (_rc.get('ingredients') or []) if i]
            if _ings:
                try:
                    ingredient_origins = _match_pantry_for_recipe(_ings, cur)
                except Exception as _e:
                    app.logger.warning(
                        f"[pantry_match] {slug}: {type(_e).__name__}: {_e}"
                    )

    # Cycle F Job 3: Named shelf line — count of sibling entries in same collection.
    shelf_line = None
    try:
        _sb = technique.get('source_book')
        _cat = technique.get('category')
        if _sb:
            cur.execute("SELECT COUNT(*) AS n FROM technique_references WHERE source_book = %s",
                        (_sb,))
            _n = cur.fetchone()['n']
            if _n > 1:
                from urllib.parse import urlencode as _ue
                shelf_line = {
                    'count': _n,
                    'name': _sb,
                    'url': '/techniques/browse?' + _ue({'source_book': _sb}),
                }
        elif _cat and _cat.lower() not in ('general',):
            cur.execute("SELECT COUNT(*) AS n FROM technique_references WHERE category = %s",
                        (_cat,))
            _n = cur.fetchone()['n']
            if _n > 1:
                from urllib.parse import urlencode as _ue
                shelf_line = {
                    'count': _n,
                    'name': _cat,
                    'url': '/techniques/browse?' + _ue({'category': _cat}),
                }
    except Exception as _e:
        app.logger.warning(f"[shelf_line] {slug}: {_e}")

    # Thumb-index: top 10 sections for current canon, ordered by entry count
    thumb_sections = []
    _canon_slug = technique.get('canon_slug')
    if _canon_slug:
        try:
            cur.execute("""
                SELECT tr.section_slug, cs.name AS section_name, COUNT(*) AS n
                FROM technique_references tr
                LEFT JOIN canon_sections cs ON cs.canon_slug = tr.canon_slug
                    AND cs.section_slug = tr.section_slug
                WHERE tr.canon_slug = %s AND tr.published IS NOT FALSE
                  AND tr.section_slug IS NOT NULL
                GROUP BY tr.section_slug, cs.name
                ORDER BY COUNT(*) DESC, tr.section_slug
                LIMIT 10
            """, (_canon_slug,))
            thumb_sections = [{'slug': r['section_slug'], 'name': r['section_name'] or r['section_slug'].replace('-', ' ').title()} for r in cur.fetchall()]
        except Exception as _e:
            app.logger.warning(f"[thumb_sections] {slug}: {_e}")

    # Page-turn: prev/next non-thin published neighbours in same canon+section, ordered by name
    prev_entry = next_entry = section_url = None
    _s_slug = technique.get('section_slug')
    if _canon_slug and _s_slug:
        section_url = f"/canon/{_canon_slug}/{_s_slug}/"
        try:
            cur.execute("""
                WITH ordered AS (
                  SELECT slug, name,
                         LAG(slug) OVER (ORDER BY name, id)  AS prev_slug,
                         LAG(name) OVER (ORDER BY name, id)  AS prev_name,
                         LEAD(slug) OVER (ORDER BY name, id) AS next_slug,
                         LEAD(name) OVER (ORDER BY name, id) AS next_name
                  FROM technique_references
                  WHERE canon_slug = %s AND section_slug = %s
                    AND published IS NOT FALSE
                    AND (
                      (CASE WHEN origin IS NOT NULL THEN 1 ELSE 0 END) +
                      (CASE WHEN description IS NOT NULL THEN 1 ELSE 0 END) +
                      (CASE WHEN flavour_context IS NOT NULL THEN 1 ELSE 0 END) +
                      (CASE WHEN quality_hierarchy IS NOT NULL THEN 1 ELSE 0 END) >= 2
                      OR recipe_card IS NOT NULL
                    )
                )
                SELECT prev_slug, prev_name, next_slug, next_name
                FROM ordered WHERE slug = %s
            """, (_canon_slug, _s_slug, slug))
            _pt = cur.fetchone()
            if _pt:
                if _pt['prev_slug']:
                    prev_entry = {'slug': _pt['prev_slug'], 'name': _pt['prev_name']}
                if _pt['next_slug']:
                    next_entry = {'slug': _pt['next_slug'], 'name': _pt['next_name']}
        except Exception as _e:
            app.logger.warning(f"[page_turn] {slug}: {_e}")

    # Riffle: ordered sibling list for fore-edge hold (cap 250, non-thin only)
    siblings = []
    if _canon_slug and _s_slug:
        try:
            cur.execute("""
                SELECT slug, name FROM technique_references
                WHERE canon_slug = %s AND section_slug = %s
                  AND published IS NOT FALSE
                  AND (
                    (CASE WHEN origin IS NOT NULL THEN 1 ELSE 0 END) +
                    (CASE WHEN description IS NOT NULL THEN 1 ELSE 0 END) +
                    (CASE WHEN flavour_context IS NOT NULL THEN 1 ELSE 0 END) +
                    (CASE WHEN quality_hierarchy IS NOT NULL THEN 1 ELSE 0 END) >= 2
                    OR recipe_card IS NOT NULL
                  )
                ORDER BY name LIMIT 250
            """, (_canon_slug, _s_slug))
            siblings = [{'slug': r['slug'], 'name': r['name']} for r in cur.fetchall()]
        except Exception as _e:
            app.logger.warning(f"[riffle] {slug}: {_e}")

    cur.close()
    conn.close()

    # Ribbon: track reading position per logged-in user per canon
    _uid = session.get("user_id")
    if _uid and _canon_slug and DATABASE_URL_WRITE:
        try:
            _wconn = psycopg2.connect(DATABASE_URL_WRITE)
            _wcur = _wconn.cursor()
            _wcur.execute("""
                INSERT INTO reading_ribbons (user_id, canon_slug, section_slug, entry_slug, entry_name)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, canon_slug) DO UPDATE
                SET section_slug=EXCLUDED.section_slug, entry_slug=EXCLUDED.entry_slug,
                    entry_name=EXCLUDED.entry_name, updated_at=NOW()
            """, (_uid, _canon_slug, technique.get('section_slug'), slug, technique.get('name')))
            _wconn.commit()
            _wcur.close()
            _wconn.close()
            app.logger.info(f"[ribbon] uid={_uid} canon={_canon_slug} entry={slug}")
        except Exception as _ribbon_err:
            app.logger.warning(f"[ribbon] upsert failed: {_ribbon_err}")

    # Derive a short cuisine label from origin for the cuisine browse link.
    # Split on first comma, period-space, or em-dash; hide if >30 chars,
    # contains digits, or still contains an em-dash after splitting.
    cuisine_label = None
    _origin = technique.get('origin') or ''
    if _origin:
        _first = _re.split(r',|\. | — ', _origin, maxsplit=1)[0].strip()
        if _first and len(_first) <= 30 and not any(c.isdigit() for c in _first) and '—' not in _first:
            cuisine_label = _first

    canonical_url = f"https://provenance.kitchen/technique/{slug}"

    # Cycle D: build frost excerpts BEFORE stripping — full values must not
    # reach the template for free viewers.
    # open_folio entries bypass the strip so logged-out users see full content.
    frosts, has_frost = _frost_excerpt(technique, user_tier)
    if user_tier == 'free' and not technique.get('open_folio'):
        technique['quality_hierarchy'] = None
        technique['sensory_tests'] = None
        technique['lives_or_dies'] = None
        technique['recipe_card'] = None   # frosted version served in band

    # Split RECIPE: blob out of pro_tips display. Check the raw pro_tips text
    # directly — do NOT gate on recipe_card being present, because recipe_card
    # is stripped to None for free viewers before this point, which would
    # otherwise leave the full RECIPE: blob visible in the Pro Tips section.
    _pt = technique.get('pro_tips') or ''
    if 'RECIPE:' in _pt:
        pro_tips_display = _pt[:_pt.find('RECIPE:')].rstrip()
    else:
        pro_tips_display = _pt

    spread_mode = (request.args.get('classic') != '1')

    return render_template("technique.html",
        technique=technique,
        canonical_url=canonical_url,
        related_techniques=related_techniques,
        user_tier=user_tier,
        user_region=user_region,
        technique_ingredients=technique_ingredients,
        technique_pairings_editorial=technique_pairings_editorial,
        technique_pairings_deduction=technique_pairings_deduction,
        technique_pairings_partial=technique_pairings_partial,
        cuisine_label=cuisine_label,
        pro_tips_display=pro_tips_display,
        frosts=frosts,
        has_frost=has_frost,
        ingredient_origins=ingredient_origins,
        shelf_line=shelf_line,
        spread_mode=spread_mode,
        thumb_sections=thumb_sections,
        prev_entry=prev_entry,
        next_entry=next_entry,
        section_url=section_url,
        siblings=siblings,
    )


# ─── Beverage product integer-ID redirect ─────────────────────────────────────

@app.route("/beverage/<int:product_id>")
def beverage_by_int_id(product_id):
    from flask import redirect
    return redirect(f"/beverage/products/{product_id}", 301)


# ─── Beverage product slug page ───────────────────────────────────────────────

@app.route("/beverage/<slug>")
def beverage_by_slug(slug):
    if slug in ('regions', 'products', 'producers'):
        abort(404)
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bp.*, br.name AS region_name, br.country AS region_country
        FROM beverage_products bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE (bp.slug = %s
           OR LOWER(REGEXP_REPLACE(REGEXP_REPLACE(bp.name, '[^a-zA-Z0-9 -]', '', 'g'), ' +', '-', 'g')) = %s)
          AND bp.is_published IS TRUE
        LIMIT 1
    """, (slug, slug))
    product = cur.fetchone()
    if not product:
        cur.close(); conn.close()
        abort(404)
    product = _serialize_row(product)
    product_id = product['id']

    cur.execute("""
        SELECT pr.* FROM beverage_producers pr
        JOIN beverage_product_producers bpp ON pr.id = bpp.producer_id
        WHERE bpp.product_id = %s AND pr.is_published IS TRUE
    """, (product_id,))
    producers = [_serialize_row(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT pi.* FROM pairing_intelligence pi
        WHERE pi.beverage_product_id = %s
        ORDER BY CASE pi.confidence WHEN 'classic' THEN 1 WHEN 'established' THEN 2 ELSE 3 END
    """, (product_id,))
    pairings = [_serialize_row(r) for r in cur.fetchall()]

    recipes_using = []
    try:
        recipes_using = _recipes_using_beverage(product_id, cur)
    except Exception as e:
        app.logger.warning(f"recipes-using lookup failed for beverage {product_id}: {e}")

    cur.close()
    conn.close()

    canonical_url = f"https://provenance.kitchen/beverage/{slug}"
    return render_template("beverage_product.html",
        product=product, producers=producers, pairings=pairings,
        recipes_using=recipes_using, canonical_url=canonical_url)


# ─── Discovery browse pages ──────────────────────────────────────────────────

@app.route("/api/stats")
def platform_stats():
    if not DATABASE_URL:
        return jsonify(total_techniques=0, total_drinks=0, featured_cuisines=[])
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT COUNT(*) AS count FROM technique_references WHERE published IS NOT FALSE")
    total_techniques = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_products WHERE is_published IS TRUE")
    total_drinks = cur.fetchone()["count"]
    cur.execute("""
        SELECT origin AS cuisine, COUNT(*) AS count
        FROM technique_references
        WHERE origin IS NOT NULL AND origin != '' AND published IS NOT FALSE
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
    # Limit to cuisines with ≥2 techniques and cap at 300 rows.
    # The full origin field has ~9k distinct free-text values that inflate
    # the DOM to 2.4 MB, preventing document_idle (Session D Finding 4.1).
    # The V4 Sprint 10 wireframe-first rebuild will replace this with a
    # curated canon hierarchy; this cap is the minimal 3.4 stability fix.
    cur.execute("""
        SELECT origin AS cuisine, COUNT(*) AS count
        FROM technique_references
        WHERE origin IS NOT NULL AND origin != '' AND published IS NOT FALSE
        GROUP BY origin
        HAVING COUNT(*) >= 2
        ORDER BY count DESC
        LIMIT 300
    """)
    cuisines = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) AS count FROM technique_references WHERE published IS NOT FALSE")
    total_techniques = cur.fetchone()["count"]
    cur.close()
    conn.close()
    return render_template("cuisines.html", cuisines=cuisines, total_techniques=total_techniques)


@app.route("/techniques/browse")
def techniques_browse():
    _tb_fallback = dict(techniques=[], total=0, page=1, total_pages=1, per_page=50,
        cuisine="", category="", q="")
    if not DATABASE_URL:
        return render_template("techniques_browse.html", **_tb_fallback)
    try:
        conn = get_db()
    except psycopg2.OperationalError:
        return render_template("techniques_browse.html", **_tb_fallback)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cuisine = request.args.get("cuisine", "").strip()
    category = request.args.get("category", "").strip()
    source_book = request.args.get("source_book", "").strip()
    q = request.args.get("q", "").strip()
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    per_page = 50
    offset = (page - 1) * per_page

    # ── Nav N1b: token processing — strip filler, AND-match each token ──
    _SEARCH_FILLER = {
        'recipe','recipes','recipie','how','to','make','cook','cooking',
        'best','easy','authentic','real','a','an','the','for','with',
        'of','and','what','is','do','i',
    }
    if q:
        _words = [w for w in q.lower().split() if w not in _SEARCH_FILLER]
        _tokens = _words if _words else [q.strip()]
        _cleaned_q = " ".join(_words) if _words else q.strip()
    else:
        _tokens = []
        _cleaned_q = ""

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
    if source_book:
        # Exact match on source_book for named shelf line links
        conditions.append("source_book = %s")
        params.append(source_book)
    if _tokens:
        # AND across tokens: every token must appear in name OR description
        for _tok in _tokens:
            conditions.append("(name ILIKE %s OR description ILIKE %s)")
            params.extend([f"%{_tok}%", f"%{_tok}%"])

    conditions.insert(0, "published IS NOT FALSE")
    where = "WHERE " + " AND ".join(conditions)

    # Deduplicated count (collapse duplicate names)
    cur.execute(
        f"SELECT COUNT(*) AS count FROM (SELECT DISTINCT lower(name) FROM technique_references {where}) _c",
        params
    )
    total = cur.fetchone()["count"]

    # Nav N1c: include recipe/completeness columns so outer ORDER BY can use them
    cols = (
        "id, name, slug, category, origin, authority_tier, tier_level, description,"
        " (recipe_card IS NOT NULL) AS has_recipe,"
        " (pillar_completeness->>'count')::int AS pillar_count"
    )
    if _tokens:
        # Relevance rank using cleaned phrase: exact > prefix > phrase-contains > description-only
        rank_expr = (
            "CASE"
            " WHEN lower(name) = lower(%s) THEN 0"
            " WHEN lower(name) LIKE lower(%s) || '%%' THEN 1"
            " WHEN name ILIKE '%%' || %s || '%%' THEN 2"
            " ELSE 3 END AS _rank"
        )
        cur.execute(
            f"SELECT * FROM ("
            f"  SELECT DISTINCT ON (lower(name)) {cols}, {rank_expr}"
            f"  FROM technique_references {where}"
            f"  ORDER BY lower(name), (recipe_card IS NOT NULL) DESC,"
            f"    (pillar_completeness->>'count')::int DESC NULLS LAST, id"
            f") _d ORDER BY has_recipe DESC, _rank, pillar_count DESC NULLS LAST, name LIMIT %s OFFSET %s",
            [_cleaned_q, _cleaned_q, _cleaned_q] + params + [per_page, offset]
        )
    else:
        cur.execute(
            f"SELECT * FROM ("
            f"  SELECT DISTINCT ON (lower(name)) {cols}"
            f"  FROM technique_references {where}"
            f"  ORDER BY lower(name), (recipe_card IS NOT NULL) DESC,"
            f"    (pillar_completeness->>'count')::int DESC NULLS LAST, id"
            f") _d ORDER BY has_recipe DESC, pillar_count DESC NULLS LAST, name LIMIT %s OFFSET %s",
            params + [per_page, offset]
        )
    techniques = [_serialize_row(r) for r in cur.fetchall()]

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
    )


@app.route("/api/filter-options/cuisines")
def api_filter_cuisines():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT DISTINCT origin AS cuisine_name
            FROM technique_references
            WHERE origin IS NOT NULL AND origin != '' AND published IS NOT FALSE
            ORDER BY origin
        """)
        items = [r["cuisine_name"] for r in cur.fetchall() if r["cuisine_name"]]
        cur.close()
        conn.close()
    except Exception:
        items = []
    resp = jsonify(items)
    resp.headers["Cache-Control"] = "public, max-age=3600"
    return resp


@app.route("/api/filter-options/categories")
def api_filter_categories():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT DISTINCT
                CASE WHEN category LIKE '%% — %%' THEN TRIM(SPLIT_PART(category, ' — ', 1)) ELSE category END
                AS cat_group
            FROM technique_references
            WHERE category IS NOT NULL AND category != '' AND published IS NOT FALSE
            ORDER BY cat_group
        """)
        items = [r["cat_group"] for r in cur.fetchall() if r["cat_group"]]
        cur.close()
        conn.close()
    except Exception:
        items = []
    resp = jsonify(items)
    resp.headers["Cache-Control"] = "public, max-age=3600"
    return resp


@app.route("/drinks")
def drinks_page():
    if not DATABASE_URL:
        return render_template("drinks_home.html", categories=[], total_drinks=None, p500_total=None)
    try:
        conn = get_db()
    except psycopg2.OperationalError:
        return render_template("drinks_home.html", categories=[], total_drinks=None, p500_total=None)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT category, COUNT(*) AS count
        FROM beverage_products
        WHERE category IS NOT NULL AND is_published IS TRUE
        GROUP BY category
        ORDER BY count DESC
    """)
    categories = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) AS count FROM beverage_products WHERE is_published IS TRUE")
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
    cur.execute("SELECT * FROM technique_references WHERE slug = %s AND published IS NOT FALSE", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close(); conn.close()
        abort(404)
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
    cur.execute("SELECT * FROM technique_references WHERE slug = %s AND published IS NOT FALSE", (slug,))
    technique = cur.fetchone()
    if not technique:
        cur.close(); conn.close()
        abort(404)
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
            WHERE origin = %s AND id != %s AND published IS NOT FALSE
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
        return redirect(url_for("kitchen"))

    url = request.form.get("url", "").strip()
    if not url:
        return redirect(url_for("kitchen"))

    try:
        recipe_data = _fetch_and_parse_recipe(url)
    except Exception as e:
        app.logger.warning(f"[enhance] fetch failed: {e}")
        return redirect(url_for("kitchen"))

    user = get_current_user()
    if user and DATABASE_URL_WRITE:
        try:
            recipe_uuid = str(uuid.uuid4())
            title = recipe_data.get("title", "Imported Recipe")
            slug = make_kitchen_slug(title, recipe_uuid)
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO user_kitchen_recipes
                    (uuid, user_id, title, slug, preamble, tags, source_url, ingredients, steps, is_draft)
                VALUES (%s, %s, %s, %s, %s, '[]', %s, %s, %s, FALSE)
                ON CONFLICT (uuid) DO NOTHING
            """, (
                recipe_uuid,
                user["id"],
                title,
                slug,
                recipe_data.get("description", ""),
                url,
                json.dumps([str(i) for i in recipe_data.get("ingredients", [])]),
                json.dumps([str(s) for s in recipe_data.get("instructions", [])]),
            ))
            cur.close()
            conn.close()
        except Exception as e:
            app.logger.error(f"[enhance] db_save failed: {e}")

    return redirect(url_for("kitchen"))


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
        JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
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
        LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE bp.id = %s AND bp.is_published IS TRUE
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
            LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
            LEFT JOIN beverage_regions br ON bp.region_id = br.id
            WHERE (similarity(LOWER(bp.name), LOWER(%s)) > 0.15 OR LOWER(bp.name) ILIKE %s)
              AND (%s = '' OR bp.category ILIKE %s)
              AND bp.is_published IS TRUE
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
            LEFT JOIN beverage_producers bpr ON bp.producer_id = bpr.id AND bpr.is_published IS TRUE
            LEFT JOIN beverage_regions br ON bp.region_id = br.id
            WHERE bp.category ILIKE %s AND bp.is_published IS TRUE
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
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET {cols}, updated_at = NOW() WHERE id = %s", vals)
        cur.close()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
    finally:
        if conn:
            conn.close()


def update_user_by_stripe_customer(customer_id, **kwargs):
    """Update user columns matched by stripe_customer_id."""
    if not kwargs or not DATABASE_URL_WRITE:
        return
    cols = ", ".join(f"{k} = %s" for k in kwargs)
    vals = list(kwargs.values()) + [customer_id]
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET {cols}, updated_at = NOW() WHERE stripe_customer_id = %s", vals)
        cur.close()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
    finally:
        if conn:
            conn.close()


def user_can_access(required_tier):
    """Check if the current user's tier meets the required tier."""
    user = get_current_user()
    if not user:
        return False
    if user.get("role") in ("founder", "admin"):
        return True
    user_tier = user.get("subscription_tier", "free")
    user_status = user.get("subscription_status", "inactive")
    if required_tier == "free":
        return True
    if user_status not in ("active", "past_due"):
        return False
    user_level = TIER_HIERARCHY.index(user_tier) if user_tier in TIER_HIERARCHY else 0
    required_level = TIER_HIERARCHY.index(required_tier) if required_tier in TIER_HIERARCHY else 999
    return user_level >= required_level


def gate_for_tier(required_tier: str) -> str:
    """
    Returns the render state for a tier-gated template region.
    States: "full_content" | "preview_then_prompt" | "gate_block"
    Use in Jinja: {% if gate_for_tier('library') == 'full_content' %}
    """
    user = get_current_user()
    if required_tier == "free":
        return "full_content"
    if not user:
        return "gate_block"
    if user.get("role") in ("founder", "admin"):
        return "full_content"
    user_status = user.get("subscription_status", "inactive")
    if user_status not in ("active", "past_due"):
        return "gate_block"
    user_tier = user.get("subscription_tier", "free")
    user_level = TIER_HIERARCHY.index(user_tier) if user_tier in TIER_HIERARCHY else 0
    required_level = TIER_HIERARCHY.index(required_tier) if required_tier in TIER_HIERARCHY else 999
    if user_level >= required_level:
        return "full_content"
    return "preview_then_prompt"


app.jinja_env.globals["gate_for_tier"] = gate_for_tier
app.jinja_env.globals["format_cuisine"] = _format_cuisine


def gate_for_addon(addon_name):
    user = get_current_user()
    if not user:
        return False
    if user.get("role") in ("founder", "admin"):
        return True
    if addon_name == "atelier":
        return bool(user.get("has_atelier_addon"))
    return False


@app.context_processor
def inject_user():
    user = get_current_user()
    return {
        "current_user": user,
        "user_tier": user.get("subscription_tier", "free") if user else "free",
        "user_role": user.get("role", "user") if user else "user",
        "is_authenticated": user is not None,
    }


# ─── Auth routes ─────────────────────────────────────────────────────────────

def _safe_next(default="/"):
    """Sanitize ?next= param. Only accept relative paths — reject open-redirect attempts."""
    nxt = request.args.get("next", "")
    if (nxt
            and nxt.startswith("/")
            and not nxt.startswith("//")
            and not nxt.lower().startswith("/http")):
        return nxt
    return default


def _login_redirect():
    """Redirect to login, preserving the current path as ?next=."""
    path = _urllib_parse.quote(request.path, safe="/")
    return redirect(f"/auth/login?next={path}")


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
        user_id = row["id"]
        # Generate and send verification email (soft — account usable without verifying)
        try:
            token = secrets.token_hex(32)
            expires_at = _dt.utcnow() + _timedelta(days=7)
            conn2 = psycopg2.connect(DATABASE_URL_WRITE)
            conn2.autocommit = True
            cur2 = conn2.cursor()
            cur2.execute(
                "INSERT INTO email_verification_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
                (user_id, token, expires_at),
            )
            cur2.close()
            conn2.close()
            verify_url = request.url_root.rstrip("/") + "/auth/verify-email?token=" + token
            send_verification_email(email, verify_url)
        except Exception:
            pass  # Never block signup over email failure
        cur.close()
        conn.close()
        session.permanent = True
        session["user_id"] = user_id
        next_url = _safe_next(default="/")
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

    if user.get("closed_at"):
        return render_template("auth/login.html", error="This seat is closed. Contact us to reopen it.")

    session.permanent = True
    session["user_id"] = user["id"]
    if request.form.get("remember_me") == "on":
        session["_remember"] = True
    next_url = _safe_next(default="/kitchen")
    return redirect(next_url)


@app.route("/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return redirect("/")


@app.route("/auth/account")
def auth_account():
    user = get_current_user()
    if not user:
        return _login_redirect()
    subscribed = request.args.get("subscribed") == "true"
    cancelled = request.args.get("cancelled") == "true"
    return render_template("auth/account.html", user=user, subscribed=subscribed,
                           cancelled=cancelled, valid_regions=VALID_REGIONS)


@app.route("/auth/account/region", methods=["POST"])
def auth_account_region():
    user = get_current_user()
    if not user:
        return _login_redirect()
    loc = request.form.get("user_location", "").strip().upper()
    if loc not in _VALID_REGION_CODES:
        return redirect("/auth/account")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET user_location = %s WHERE id = %s", (loc, user["id"]))
    cur.close()
    conn.close()
    return redirect("/auth/account")


@app.route("/auth/account/close", methods=["GET"])
def auth_account_close_confirm():
    user = get_current_user()
    if not user:
        return _login_redirect()
    return render_template("auth/close_confirmation.html", user=user)


@app.route("/auth/account/close", methods=["POST"])
def auth_account_close():
    user = get_current_user()
    if not user:
        return _login_redirect()

    # Cancel active Stripe subscription — wrap so a Stripe failure never leaves the
    # account half-closed; the webhook will reconcile if needed.
    sub_id = user.get("stripe_subscription_id")
    if sub_id:
        try:
            stripe.Subscription.cancel(sub_id)
        except Exception as e:
            app.logger.warning("close-seat: Stripe cancel failed for sub %s: %s", sub_id, e)

    # Mark closed and downgrade tier — keep the row and all data intact.
    update_user(
        user["id"],
        closed_at=_dt.utcnow(),
        subscription_tier="free",
        subscription_status="inactive",
        stripe_subscription_id=None,
    )

    session.clear()
    return redirect("/auth/login?closed=1")


# ─── Password reset + email verification routes ───────────────────────────────

def _auth_rate_limit(identifier: str, action: str, limit: int, window_seconds: int) -> bool:
    """Return True if under limit, False if over limit."""
    try:
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cutoff = _dt.utcnow() - _timedelta(seconds=window_seconds)
        cur.execute(
            "SELECT COUNT(*) FROM auth_rate_limits WHERE identifier=%s AND action=%s AND created_at > %s",
            (identifier, action, cutoff),
        )
        count = cur.fetchone()[0]
        if count >= limit:
            cur.close(); conn.close()
            return False
        cur.execute(
            "INSERT INTO auth_rate_limits (identifier, action) VALUES (%s, %s)",
            (identifier, action),
        )
        cur.close(); conn.close()
        return True
    except Exception:
        return True  # Fail open — never block a user over a rate limit DB error


@app.route("/auth/forgot-password", methods=["GET"])
def auth_forgot_password():
    return render_template("auth/forgot_password.html")


@app.route("/api/auth/forgot-password", methods=["POST"])
def api_auth_forgot_password():
    """Always returns generic success to prevent account enumeration."""
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if not _auth_rate_limit(client_ip, "forgot_password", 5, 3600):
        return render_template("auth/email_sent.html")  # Still generic — don't reveal rate limiting

    email = request.form.get("email", "").strip().lower()
    if not email:
        return render_template("auth/email_sent.html")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close(); conn.close()
    except Exception:
        return render_template("auth/email_sent.html")

    if user:
        try:
            token = secrets.token_hex(32)
            expires_at = _dt.utcnow() + _timedelta(hours=24)
            conn2 = psycopg2.connect(DATABASE_URL_WRITE)
            conn2.autocommit = True
            cur2 = conn2.cursor()
            cur2.execute(
                "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
                (user["id"], token, expires_at),
            )
            cur2.close(); conn2.close()
            reset_url = request.url_root.rstrip("/") + "/auth/reset-password?token=" + token
            send_password_reset_email(email, reset_url)
        except Exception:
            pass  # Silent — generic response regardless

    return render_template("auth/email_sent.html")


@app.route("/auth/reset-password", methods=["GET"])
def auth_reset_password():
    token = request.args.get("token", "").strip()
    if not token:
        return redirect("/auth/forgot-password")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT * FROM password_reset_tokens WHERE token=%s AND used_at IS NULL AND expires_at > NOW()",
            (token,),
        )
        row = cur.fetchone()
        cur.close(); conn.close()
    except Exception:
        row = None

    if not row:
        return render_template("auth/forgot_password.html"), 400

    return render_template("auth/reset_password.html", token=token)


@app.route("/api/auth/reset-password", methods=["POST"])
def api_auth_reset_password():
    token = request.form.get("token", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")

    if not token or not password:
        return render_template("auth/reset_password.html", token=token, error="Token and password are required.")

    if password != confirm:
        return render_template("auth/reset_password.html", token=token, error="Passwords do not match.")

    if len(password) < 8:
        return render_template("auth/reset_password.html", token=token, error="Password must be at least 8 characters.")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT * FROM password_reset_tokens WHERE token=%s AND used_at IS NULL AND expires_at > NOW()",
            (token,),
        )
        row = cur.fetchone()
        cur.close(); conn.close()
    except Exception:
        return render_template("auth/reset_password.html", token=token, error="Something went wrong. Please try again.")

    if not row:
        return render_template("auth/forgot_password.html"), 400

    try:
        new_hash = generate_password_hash(password)
        conn2 = psycopg2.connect(DATABASE_URL_WRITE)
        conn2.autocommit = True
        cur2 = conn2.cursor()
        cur2.execute("UPDATE users SET password_hash=%s WHERE id=%s", (new_hash, row["user_id"]))
        cur2.execute("UPDATE password_reset_tokens SET used_at=NOW() WHERE id=%s", (row["id"],))
        cur2.close(); conn2.close()
    except Exception:
        return render_template("auth/reset_password.html", token=token, error="Something went wrong. Please try again.")

    return redirect("/auth/login?reset=1")


@app.route("/auth/verify-email", methods=["GET"])
def auth_verify_email():
    token = request.args.get("token", "").strip()
    if not token:
        return redirect("/kitchen")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT * FROM email_verification_tokens WHERE token=%s AND used_at IS NULL AND expires_at > NOW()",
            (token,),
        )
        row = cur.fetchone()
        cur.close(); conn.close()
    except Exception:
        return redirect("/kitchen")

    if not row:
        return redirect("/kitchen")

    try:
        conn2 = psycopg2.connect(DATABASE_URL_WRITE)
        conn2.autocommit = True
        cur2 = conn2.cursor()
        cur2.execute("UPDATE users SET email_verified=TRUE, email_verified_at=NOW() WHERE id=%s", (row["user_id"],))
        cur2.execute("UPDATE email_verification_tokens SET used_at=NOW() WHERE id=%s", (row["id"],))
        cur2.close(); conn2.close()
    except Exception:
        pass

    return redirect("/kitchen?verified=1")


@app.route("/api/auth/resend-verification", methods=["POST"])
def api_auth_resend_verification():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401

    if user.get("email_verified"):
        return jsonify({"ok": True, "message": "Already verified"})

    user_id = user["id"]
    if not _auth_rate_limit(str(user_id), "resend_verification", 3, 3600):
        return jsonify({"error": "Too many requests. Please wait before trying again."}), 429

    try:
        token = secrets.token_hex(32)
        expires_at = _dt.utcnow() + _timedelta(days=7)
        conn = psycopg2.connect(DATABASE_URL_WRITE)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO email_verification_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
            (user_id, token, expires_at),
        )
        cur.close(); conn.close()
        verify_url = request.url_root.rstrip("/") + "/auth/verify-email?token=" + token
        send_verification_email(user["email"], verify_url)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": "Failed to send verification email."}), 500


# ─── Legal pages ─────────────────────────────────────────────────────────────

@app.route("/terms")
def terms_page():
    return render_template("terms.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")


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
        return _login_redirect()

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
        return _login_redirect()

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

    try:
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

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return "Internal error", 500

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

    cur.execute("SELECT slug, updated_at FROM technique_references WHERE slug IS NOT NULL AND slug != '' AND published IS NOT FALSE ORDER BY id")
    techniques = cur.fetchall()

    cur.execute("SELECT slug, created_at AS updated_at FROM recipes WHERE slug IS NOT NULL AND slug != '' ORDER BY id")
    recipe_rows = cur.fetchall()

    cur.execute("""
        SELECT COALESCE(slug, LOWER(REGEXP_REPLACE(REGEXP_REPLACE(name, '[^a-zA-Z0-9 -]', '', 'g'), ' +', '-', 'g'))) AS slug,
               updated_at
        FROM beverage_products WHERE is_published IS TRUE ORDER BY id
    """)
    bev_products = cur.fetchall()

    cur.execute("SELECT id, updated_at FROM beverage_regions ORDER BY id")
    bev_regions = cur.fetchall()

    cur.execute("SELECT id, updated_at FROM beverage_producers WHERE is_published IS TRUE ORDER BY id")
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

# ── Costing Engine v2 — Unit Conversion ───────────────────────────────────────
# All weights reduce to grams; all volumes to ml; counts to each.
_WT = {'g':1,'gram':1,'grams':1,'kg':1000,'kilogram':1000,'kilograms':1000,
       'lb':453.592,'lbs':453.592,'pound':453.592,'pounds':453.592,
       'oz':28.3495,'ounce':28.3495,'ounces':28.3495}
_VL = {'ml':1,'milliliter':1,'milliliters':1,'millilitre':1,'millilitres':1,
       'l':1000,'liter':1000,'liters':1000,'litre':1000,'litres':1000,
       'cup':236.588,'cups':236.588,'tbsp':14.787,'tablespoon':14.787,'tablespoons':14.787,
       'tsp':4.929,'teaspoon':4.929,'teaspoons':4.929,
       'fl_oz':29.574,'fl oz':29.574,'floz':29.574,'fluid_oz':29.574}
_CT = {'each':1,'pcs':1,'piece':1,'pieces':1,'unit':1,'units':1,
       'dozen':12,'doz':12,'case':1}
# Pack size conversions: (ingredient_keyword, supplier_unit) -> grams per unit.
# Intentionally small — flag rather than guess for unlisted items.
PACK_SIZE_CONVERSIONS = {
    ("spaghetti", "case"): 12000,    # De Cecco standard: 24 × 500g
    ("pasta", "case"): 12000,
    ("rice", "case"): 25000,         # 25kg case standard
    ("flour", "case"): 25000,
    ("sugar", "case"): 25000,
    ("salt", "case"): 25000,
    ("olive oil", "case"): 12000,    # 12 × 1L (~1g/ml)
    ("vinegar", "case"): 12000,
    ("canned tomato", "case"): 2800, # 6 × ~400g cans (drained weight)
}
# Approximate g/ml density for common ingredients (volume↔weight bridge)
_DENSITY = {
    'salt':1.22,'sugar':0.845,'flour':0.593,'butter':0.911,'oil':0.92,
    'olive oil':0.91,'water':1.0,'milk':1.03,'cream':1.01,'honey':1.42,
    'rice':0.867,'pepper':0.50,'cocoa':0.52,'starch':0.60,'syrup':1.33,
}


def _unit_family(u):
    u = (u or '').lower().strip()
    if u in _WT: return 'weight'
    if u in _VL: return 'volume'
    if u in _CT: return 'count'
    return 'unknown'


def costing_convert(qty, recipe_unit, price_unit, ingredient_name=''):
    """Convert recipe qty (in recipe_unit) to price_unit for cost calculation.
    Returns (converted_qty: float, needs_estimate: bool).
    needs_estimate=True means vol↔weight bridge was used — caller should warn.
    """
    ru = (recipe_unit or '').lower().strip()
    pu = (price_unit or '').lower().strip()
    if ru == pu or not ru or not pu:
        return qty, False
    rf, pf = _unit_family(ru), _unit_family(pu)
    if rf == 'weight' and pf == 'weight':
        return qty * _WT[ru] / _WT[pu], False
    if rf == 'volume' and pf == 'volume':
        return qty * _VL[ru] / _VL[pu], False
    if rf == 'count' and pf == 'count':
        return qty * _CT.get(ru,1) / _CT.get(pu,1), False
    # Volume ↔ weight via density lookup
    density = None
    iname = ingredient_name.lower()
    for key, d in _DENSITY.items():
        if key in iname:
            density = d
            break
    if density is None:
        return qty, True   # can't convert; flag as estimate
    if rf == 'weight' and pf == 'volume':
        return (qty * _WT[ru] / density) / _VL[pu], True
    if rf == 'volume' and pf == 'weight':
        return (qty * _VL[ru] * density) / _WT[pu], True
    return qty, True


def _fuzzy_ingredient_match(cur, description):
    """Return (ingredient_products row, confidence) for the best name match, or (None, 0)."""
    desc_lower = description.lower().strip()
    # Exact substring match first
    cur.execute("""
        SELECT id, name FROM ingredient_products
        WHERE %s ILIKE '%%' || name || '%%' OR name ILIKE '%%' || %s || '%%'
        ORDER BY LENGTH(name) DESC LIMIT 1
    """, (desc_lower, desc_lower))
    row = cur.fetchone()
    if row:
        return row, 0.85
    # Trigram similarity via pg_trgm if available, else partial word match
    try:
        cur.execute("""
            SELECT id, name, similarity(name, %s) AS sim
            FROM ingredient_products
            WHERE similarity(name, %s) > 0.3
            ORDER BY sim DESC LIMIT 1
        """, (desc_lower, desc_lower))
        row = cur.fetchone()
        if row and float(row['sim']) > 0.3:
            return row, round(float(row['sim']), 2)
    except Exception:
        pass
    return None, 0.0


def _resolve_ingredient_master_id(cur, name):
    """
    Resolve an ingredient name to ingredient_master.id via ingredient_aliases.
    Returns (ingredient_id: int | None, was_resolved: bool).

    Resolution order:
      1. Exact alias_lower match in ingredient_aliases (ingredient_id NOT NULL)
      2. Substring containment against canonical_name in ingredient_master
      3. Trigram similarity > 0.4 (if pg_trgm available)

    Read-only — does NOT insert aliases. Used by Phase 3 dual-write paths.
    """
    if not name or not name.strip():
        return None, False
    n = name.strip().lower()

    # 1. Exact alias match
    cur.execute("""
        SELECT ingredient_id FROM ingredient_aliases
        WHERE alias_lower = %s AND ingredient_id IS NOT NULL
        LIMIT 1
    """, (n,))
    row = cur.fetchone()
    if row:
        return row[0] if isinstance(row, (list, tuple)) else row["ingredient_id"], True

    # 2. Substring containment (prefer foundational / shorter canonical names)
    # Guard on the second arm: only allow "canonical contains search" when the
    # search term is at least half the canonical's length.  Without this, a
    # short generic term ("pasta", "egg", "oil") can claim a long branded name
    # ("Gnocchi — Pasta d'Angelo") whose canonical merely contains it as a word.
    cur.execute("""
        SELECT id FROM ingredient_master
        WHERE %s LIKE '%%' || lower(canonical_name) || '%%'
           OR (lower(canonical_name) LIKE '%%' || %s || '%%'
               AND length(%s) * 2 >= length(canonical_name))
        ORDER BY
          CASE WHEN category LIKE 'foundational_%%' THEN 0 ELSE 1 END,
          length(canonical_name) ASC
        LIMIT 1
    """, (n, n, n))
    row = cur.fetchone()
    if row:
        return row[0] if isinstance(row, (list, tuple)) else row["id"], True

    # 3. Trigram similarity (best-effort)
    try:
        cur.execute("""
            SELECT id FROM ingredient_master
            WHERE similarity(canonical_name, %s) > 0.4
            ORDER BY similarity(canonical_name, %s) DESC LIMIT 1
        """, (name, name))
        row = cur.fetchone()
        if row:
            return row[0] if isinstance(row, (list, tuple)) else row["id"], True
    except Exception:
        pass

    return None, False


def _dw_resolve_supplier_id(cur, supplier_name):
    """
    Phase 3 dual-write: resolve a supplier name to suppliers.id via supplier_aliases.
    Returns (supplier_id: int | None, was_resolved: bool).
    Distinct from the older _resolve_supplier_id (line ~3675) which returns int|None only.
    """
    if not supplier_name or not supplier_name.strip():
        return None, False
    n = supplier_name.strip().lower()

    cur.execute("""
        SELECT supplier_id FROM supplier_aliases
        WHERE alias_lower = %s LIMIT 1
    """, (n,))
    row = cur.fetchone()
    if row:
        v = row[0] if isinstance(row, (list, tuple)) else row["supplier_id"]
        if v is not None:
            return v, True

    # Fallback: fuzzy match against suppliers.name
    cur.execute("""
        SELECT id FROM suppliers
        WHERE lower(name) = %s OR lower(name) LIKE %s
        ORDER BY length(name) ASC LIMIT 1
    """, (n, f"%{n[:20]}%"))
    row = cur.fetchone()
    if row:
        return row[0] if isinstance(row, (list, tuple)) else row["id"], True

    return None, False



@app.route("/api/costing/scan-invoice", methods=["POST"])
def costing_scan_invoice_legacy():
    """RETIRED in Phase 4. Use POST /api/invoices/scan instead."""
    return jsonify({
        "error": "This endpoint is retired.",
        "use_instead": "POST /api/invoices/scan",
        "phase": "4 — read switchover"
    }), 410


def _cost_ingredient_loop(ingredients, user_id, use_user_pricing, cur):
    """Shared ingredient pricing loop. Returns (breakdown, total_cost, unpriced, unit_warning_items)."""
    breakdown = []
    total_cost = 0.0
    unpriced = []
    unit_warning_items = []

    for ing in ingredients:
        name = ""
        qty = 0.0
        unit = ""
        if isinstance(ing, dict):
            name = ing.get("name") or ing.get("ingredient") or ""
            try:
                qty = float(ing.get("quantity") or ing.get("amount") or ing.get("count") or 0)
            except (ValueError, TypeError):
                qty = 0.0
            unit = ing.get("unit") or ""
        elif isinstance(ing, str):
            name = ing
            qty = 1.0
            unit = "each"
        if not name:
            continue

        normalized = name.lower().strip()
        price_row = None
        source = "global"
        unit_estimate = False

        master_id, was_resolved = _resolve_ingredient_master_id(cur, normalized)
        if was_resolved and use_user_pricing:
            cur.execute("""
                SELECT %s AS ingredient_name, price_per_unit AS unit_price, unit,
                       supplier_name, currency
                FROM price_history
                WHERE ingredient_id = %s AND user_id = %s
                  AND source IN ('invoice', 'manual', 'backfill_legacy')
                ORDER BY effective_date DESC, created_at DESC
                LIMIT 1
            """, (normalized, master_id, str(user_id) if user_id is not None else None))
            price_row = cur.fetchone()
            if price_row:
                source = "user"
        if was_resolved and not price_row:
            cur.execute("""
                SELECT %s AS ingredient_name, price_per_unit AS unit_price, unit,
                       yield_factor, NULL AS effective_cost,
                       supplier_name, currency
                FROM price_history
                WHERE ingredient_id = %s AND is_global = true
                ORDER BY effective_date DESC, created_at DESC
                LIMIT 1
            """, (normalized, master_id))
            price_row = cur.fetchone()
            if price_row:
                source = "global"

        if price_row:
            price_unit = price_row.get("unit", "each") or "each"
            raw_price = float(price_row.get("unit_price") or price_row.get("price_per_unit") or 0)
            yf = float(price_row.get("yield_factor") or 1.0)
            effective = raw_price / yf if yf else raw_price
            supplier_name = price_row.get("supplier_name") or ""
            currency = price_row.get("currency") or "CAD"

            costing_unit = unit if unit else "each"
            ru_family = _unit_family(costing_unit)
            pu_family = _unit_family(price_unit)
            cost_warning = None
            cost_warning_message = None
            line_cost = 0.0

            if pu_family == 'count' and ru_family in ('weight', 'volume'):
                pack_g = None
                name_lower = name.lower()
                pu_lower = price_unit.lower().strip()
                for (kw, su), grams in PACK_SIZE_CONVERSIONS.items():
                    if kw in name_lower and su == pu_lower:
                        pack_g = grams
                        break
                if pack_g:
                    qty_g = qty * _WT.get(unit.lower().strip(), 1) if ru_family == 'weight' \
                            else qty * _VL.get(unit.lower().strip(), 1)
                    cost_per_g = effective / pack_g
                    line_cost = round(cost_per_g * qty_g, 2)
                    unit_estimate = True
                else:
                    cost_warning = "needs_unit_info"
                    cost_warning_message = (
                        f"Can't confidently price this — supplier price is "
                        f"{currency} {raw_price:.2f}/{price_unit} but the pack size "
                        f"isn't known. Edit the price manually or re-scan the invoice "
                        f"with full pack details."
                    )
            else:
                cqty, unit_estimate = costing_convert(qty, costing_unit, price_unit, name)
                line_cost = round(cqty * effective, 2)
                if ru_family == 'weight' and effective > 0 and qty > 0:
                    qty_g = qty * _WT.get(unit.lower().strip(), 1)
                    if qty_g > 0:
                        cost_per_g = line_cost / qty_g
                        if cost_per_g > 5.0:
                            cost_warning = "needs_unit_info"
                            cost_warning_message = (
                                f"Can't confidently price this — computed cost implies "
                                f"{currency} {cost_per_g * 1000:.0f}/kg which looks incorrect. "
                                f"Edit the price manually or re-scan the invoice with full pack details."
                            )
                            line_cost = 0.0

            if cost_warning:
                unit_warning_items.append(name)

            breakdown.append({
                "ingredient": name,
                "quantity": qty,
                "unit": unit,
                "unit_price": raw_price,
                "price_unit": price_unit,
                "yield_factor": yf,
                "effective_cost": effective,
                "line_cost": line_cost if not cost_warning else None,
                "supplier": supplier_name,
                "currency": currency,
                "source": source,
                "unit_estimate": unit_estimate,
                "cost_warning": cost_warning,
                "cost_warning_message": cost_warning_message,
            })
            if not cost_warning:
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

    return breakdown, total_cost, unpriced, unit_warning_items


@app.route("/api/costing/recipe/<slug>")
def get_recipe_cost(slug):
    """Calculate cost breakdown for a recipe.
    Library+ users: uses per-user price_history first, falls back to global price_history rows.
    Unauthenticated / sub-library: still works but uses only global prices.
    """
    fmt = request.args.get("format", "").lower()
    user = get_current_user()
    user_id = str(user["id"]) if user else None
    use_user_pricing = user_id is not None and user_can_access("kitchen")

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM recipes WHERE slug = %s LIMIT 1", (slug,))
    recipe = cur.fetchone()
    if not recipe and user_id:
        cur.execute(
            "SELECT * FROM user_kitchen_recipes WHERE slug = %s AND user_id = %s LIMIT 1",
            (slug, user_id),
        )
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

    breakdown, total_cost, unpriced, unit_warning_items = _cost_ingredient_loop(
        ingredients, user_id, use_user_pricing, cur
    )

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

    if fmt == "pdf":
        pdf_payload = {
            "recipe": recipe.get("name") or recipe.get("title") or slug,
            "slug": slug,
            "portions": portions,
            "total_cost": total_cost,
            "cost_per_portion": cost_per_portion,
            "menu_price": menu_price,
            "food_cost_pct": actual_pct,
            "target_food_cost_pct": target_pct,
            "tier_label": "Profession tier",
            "breakdown": [
                {
                    **row,
                    "local_provider": row.get("supplier_name") or row.get("supplier"),
                    "local_provider_price": (
                        f"CAD {row['unit_price']:.2f}/{row.get('price_unit') or row.get('unit', 'each')}"
                        if row.get("unit_price") is not None else None
                    ),
                }
                for row in breakdown
            ],
        }
        filename = f"costing-{slug}-{_dt.now().strftime('%Y-%m-%d')}.pdf"
        pdf_bytes = _render_costing_pdf(pdf_payload)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename,
        )

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
        "priced_count": len(breakdown) - len(unpriced) - len(unit_warning_items),
        "unpriced_count": len(unpriced),
        "unpriced_items": unpriced,
        "unit_warning_count": len(unit_warning_items),
        "unit_warning_items": unit_warning_items,
        "breakdown": breakdown,
    })


@app.route("/api/costing/recipe/<slug>/set-target", methods=["POST"])
@requires_tier("profession")
def set_recipe_cost_target(slug):
    """Set the menu price and target food cost % for a recipe."""
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



@app.route("/api/invoices/scan", methods=["POST"])
@requires_tier("profession")
def invoices_scan():
    """Scan a supplier invoice (images or PDF, multi-page) via Claude Vision.
    Accepts files[] (multiple pages) or legacy single 'invoice' field.
    Saves to supplier_invoices + supplier_invoice_lines.
    Returns a review structure with extracted lines for user confirmation.
    """
    try:
        app.logger.info(
            f"[SCAN] POST /api/invoices/scan ct={request.content_type!r} "
            f"files={list(request.files.keys())!r} len={request.content_length}"
        )
        user = get_current_user()
        _CLAUDE_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

        # Collect uploaded files — support files[] (multi-page) or legacy 'invoice' (single)
        uploaded = request.files.getlist("files[]")
        if not uploaded:
            f = request.files.get("invoice")
            if f:
                uploaded = [f]

        content = []   # Claude content blocks (multiple image blocks for multi-page)
        page_count = 0
        _json = request.get_json(silent=True)  # safe on multipart — returns None instead of raising 415

        if uploaded:
            for file in uploaded:
                raw_bytes = file.read()
                is_pdf = (file.content_type == "application/pdf"
                          or (file.filename or "").lower().endswith(".pdf"))
                if is_pdf:
                    try:
                        from pdf2image import convert_from_bytes
                        import io as _io
                        pages = convert_from_bytes(raw_bytes, dpi=200, first_page=1, last_page=5)
                        for page_img in pages:
                            buf = _io.BytesIO()
                            page_img.save(buf, format="PNG")
                            img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                            content.append({"type": "image", "source": {
                                "type": "base64", "media_type": "image/png", "data": img_b64}})
                            page_count += 1
                    except Exception:
                        # pdf2image unavailable — send as native PDF document
                        img_b64 = base64.b64encode(raw_bytes).decode("utf-8")
                        content.append({"type": "document", "source": {
                            "type": "base64", "media_type": "application/pdf", "data": img_b64}})
                        page_count += 1
                else:
                    # Image: use _prepare_image to handle HEIC → JPEG conversion
                    img_bytes, media_type = _prepare_image(raw_bytes)
                    if media_type not in _CLAUDE_IMAGE_TYPES:
                        media_type = "image/jpeg"
                    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                    content.append({"type": "image", "source": {
                        "type": "base64", "media_type": media_type, "data": img_b64}})
                    page_count += 1
        elif _json:
            raw = _json.get("image", "")
            if raw:
                img_b64 = raw.split(",")[1] if "," in raw else raw
                raw_type = _json.get("media_type") or "image/jpeg"
                media_type = raw_type if raw_type in _CLAUDE_IMAGE_TYPES else "image/jpeg"
                content.append({"type": "image", "source": {
                    "type": "base64", "media_type": media_type, "data": img_b64}})
                page_count = 1
            elif _json.get("image_url"):
                content.append({"type": "image", "source": {
                    "type": "url", "url": _json["image_url"]}})
                page_count = 1

        if not content:
            return jsonify({"error": "No invoice image provided"}), 400

        currency = request.form.get("currency") or (_json.get("currency") if _json else None) or "CAD"

        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            return jsonify({"error": "Vision API not configured"}), 500

        client = anthropic.Anthropic(api_key=anthropic_key)
        page_note = f"This is a {page_count}-page invoice. " if page_count > 1 else ""
        content.append({"type": "text", "text": (
            f"{page_note}Extract ALL line items from this supplier invoice precisely. "
            "For each item return: item_name (exactly as printed on invoice), "
            "quantity (numeric), quantity_unit (kg/lb/g/L/ml/case/bunch/each/dozen/box/etc.), "
            "unit_price (price per one unit), line_total. "
            "Also extract at document level: supplier_name, supplier_address, "
            "invoice_number (or PO number), invoice_date (YYYY-MM-DD), "
            "invoice_total (bottom-line total), currency (default " + currency + "). "
            "Respond with the JSON object ONLY. No markdown fences. No prose. No explanation. Begin your response with { and end with }.\n"
            '{"supplier_name":"","supplier_address":"","invoice_number":"","invoice_date":"YYYY-MM-DD",'
            '"invoice_total":0.00,"currency":"CAD",'
            '"items":[{"item_name":"","quantity":0,"quantity_unit":"kg","unit_price":0.00,"line_total":0.00}]}'
        )})
    except Exception as _pre:
        import traceback
        app.logger.error(f"Invoice scan pre-flight crashed: {traceback.format_exc()}")
        return jsonify({"error": f"Scan failed: {str(_pre)}"}), 500


    try:
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": content}]
        )
        raw_text = resp.content[0].text.strip() if resp.content else ""
        app.logger.info(
            f"[SCAN] Vision response stop_reason={resp.stop_reason!r} "
            f"content_blocks={len(resp.content)} len={len(raw_text)} "
            f"preview={raw_text[:300]!r}"
        )
        if not raw_text:
            return jsonify({"error": "Vision API returned empty response — check model PDF support"}), 500

        import re as _re

        # Strip markdown code fences if present
        fence_match = _re.search(r'```(?:json)?\s*(.*?)\s*```', raw_text, _re.DOTALL)
        if fence_match:
            raw_text = fence_match.group(1).strip()

        # Skip any leading prose before the opening brace
        if not raw_text.startswith('{'):
            brace_start = raw_text.find('{')
            if brace_start == -1:
                app.logger.error(f"[SCAN] No JSON object found: {raw_text[:500]!r}")
                return jsonify({"error": "Invoice extraction returned no JSON object"}), 500
            raw_text = raw_text[brace_start:]

        # Walk forward counting braces to find the actual end of the JSON object,
        # discarding any trailing prose that follows the closing brace.
        depth = 0
        end_idx = 0
        in_string = False
        escape = False
        for i, ch in enumerate(raw_text):
            if escape:
                escape = False
                continue
            if ch == '\\':
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i + 1
                    break

        if end_idx == 0:
            app.logger.error(f"[SCAN] Unterminated JSON object: {raw_text[:500]!r}")
            return jsonify({"error": "Invoice extraction returned malformed JSON"}), 500

        raw_text = raw_text[:end_idx]
        invoice_data = json.loads(raw_text)
    except Exception as e:
        import traceback
        app.logger.error(f"[SCAN] Vision call/parse failed: {traceback.format_exc()}")
        return jsonify({"error": f"Invoice extraction failed: {str(e)}"}), 500

    conn = None
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Match or auto-create supplier
        supplier_name = (invoice_data.get("supplier_name") or "Unknown Supplier").strip()
        supplier_id = None
        sup_found_existing = False

        try:
            resolved_id, was_resolved = _dw_resolve_supplier_id(cur, supplier_name)
            if was_resolved:
                supplier_id = resolved_id
                sup_found_existing = True
        except Exception as e:
            app.logger.warning(f"[scan] supplier alias lookup failed: {e}")

        # Original exact/prefix match (fallback)
        if supplier_id is None:
            cur.execute("""
                SELECT id FROM suppliers
                WHERE name ILIKE %s OR name ILIKE %s LIMIT 1
            """, (supplier_name, f"%{supplier_name[:20]}%"))
            sup_row = cur.fetchone()
            if sup_row:
                supplier_id = sup_row["id"]
                sup_found_existing = True

        if not supplier_id:
            # Auto-create unverified supplier
            try:
                cur.execute("""
                    INSERT INTO suppliers
                        (name, country, supplier_type, verified_date, verification_source,
                         is_active, user_added, verification_status)
                    VALUES (%s, 'CA', 'distributor', NOW(), 'invoice_scan', true, true, 'unverified')
                    ON CONFLICT (name) DO NOTHING RETURNING id
                """, (supplier_name,))
                new_row = cur.fetchone()
                if new_row:
                    supplier_id = new_row["id"]
                    try:
                        cur.execute("""
                            INSERT INTO supplier_aliases (supplier_id, alias, source)
                            VALUES (%s, %s, 'invoice')
                            ON CONFLICT (alias_lower) DO NOTHING
                        """, (supplier_id, supplier_name))
                    except Exception as e:
                        app.logger.warning(f"[scan] supplier_aliases insert failed: {e}")
                else:
                    cur.execute("SELECT id FROM suppliers WHERE name = %s", (supplier_name,))
                    r = cur.fetchone()
                    if r:
                        supplier_id = r["id"]
                        sup_found_existing = True
            except Exception:
                pass

        # Insert supplier_invoices row
        cur.execute("""
            INSERT INTO supplier_invoices
                (user_id, supplier_id, supplier_name, invoice_number, invoice_date,
                 invoice_total, currency, raw_text, page_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            str(user["id"]), supplier_id, supplier_name,
            invoice_data.get("invoice_number"),
            invoice_data.get("invoice_date"),
            invoice_data.get("invoice_total"),
            invoice_data.get("currency") or currency,
            json.dumps(invoice_data),
            page_count,
        ))
        invoice_id = str(cur.fetchone()["id"])

        # Insert invoice lines + fuzzy-match ingredients
        lines_out = []
        for i, item in enumerate(invoice_data.get("items", []), 1):
            raw_desc = (item.get("item_name") or "").strip()
            if not raw_desc:
                continue
            qty = item.get("quantity")
            unit = (item.get("quantity_unit") or "each").lower()
            unit_price = item.get("unit_price")
            line_total = item.get("line_total")

            matched_row, confidence = _fuzzy_ingredient_match(cur, raw_desc)
            matched_id = matched_row["id"] if matched_row else None
            matched_name = matched_row["name"] if matched_row else None

            try:
                ingredient_master_id, was_resolved = _resolve_ingredient_master_id(cur, raw_desc)
                if was_resolved and raw_desc:
                    cur.execute("""
                        INSERT INTO ingredient_aliases (ingredient_id, alias, source)
                        VALUES (%s, %s, 'invoice')
                        ON CONFLICT (alias_lower) DO NOTHING
                    """, (ingredient_master_id, raw_desc))
                elif raw_desc:
                    cur.execute("""
                        INSERT INTO ingredient_aliases (ingredient_id, alias, source)
                        VALUES (NULL, %s, 'invoice')
                        ON CONFLICT (alias_lower) DO NOTHING
                    """, (raw_desc,))
            except Exception as e:
                app.logger.warning(f"[scan] ingredient resolution failed for '{raw_desc}': {e}")

            cur.execute("""
                INSERT INTO supplier_invoice_lines
                    (invoice_id, line_number, raw_description, quantity, unit,
                     unit_price, line_total, matched_ingredient_id,
                     matched_ingredient_name, match_confidence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (invoice_id, i, raw_desc, qty, unit, unit_price, line_total,
                  matched_id, matched_name, confidence if confidence > 0 else None))
            line_id = str(cur.fetchone()["id"])
            lines_out.append({
                "id": line_id,
                "line_number": i,
                "raw_description": raw_desc,
                "quantity": float(qty) if qty is not None else None,
                "unit": unit,
                "unit_price": float(unit_price) if unit_price is not None else None,
                "line_total": float(line_total) if line_total is not None else None,
                "matched_ingredient_name": matched_name or raw_desc,
                "match_confidence": float(confidence) if confidence else 0.0,
                "confirmed": confidence >= 0.7,
            })

        cur.close()
        conn.close()

        return jsonify({
            "invoice_id": invoice_id,
            "supplier_name": supplier_name,
            "supplier_id": supplier_id,
            "invoice_date": invoice_data.get("invoice_date"),
            "invoice_number": invoice_data.get("invoice_number"),
            "invoice_total": invoice_data.get("invoice_total"),
            "currency": invoice_data.get("currency") or currency,
            "page_count": page_count,
            "lines": lines_out,
            "auto_created_supplier": not sup_found_existing,
        })
    except Exception as e:
        import traceback
        app.logger.error(f"Invoice scan DB failed: {traceback.format_exc()}")
        if conn:
            try:
                conn.close()
            except Exception:
                pass
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500


@app.route("/api/invoices/<invoice_id>/apply", methods=["POST"])
@requires_tier("profession")
def invoices_apply(invoice_id):
    """Apply user-confirmed invoice lines to price_history."""
    user = get_current_user()

    data = request.get_json() or {}
    lines = data.get("lines", [])   # [{line_id, ingredient_name, price_per_unit, unit}]
    if not lines:
        return jsonify({"error": "No lines provided"}), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Verify invoice belongs to this user
    cur.execute("SELECT * FROM supplier_invoices WHERE id = %s AND user_id = %s",
                (invoice_id, str(user["id"])))
    inv = cur.fetchone()
    if not inv:
        cur.close(); conn.close()
        return jsonify({"error": "Invoice not found"}), 404

    effective_date = inv["invoice_date"] or __import__("datetime").date.today().isoformat()
    supplier_id = inv["supplier_id"]
    supplier_name = inv["supplier_name"]
    applied = 0
    skipped = 0
    skipped_lines = []

    for line in lines:
        ingredient_name = (line.get("ingredient_name") or "").strip()
        price_per_unit = line.get("price_per_unit")
        unit = (line.get("unit") or "each").strip()
        line_id = line.get("line_id")
        if not ingredient_name or price_per_unit is None:
            skipped += 1
            continue
        master_id, was_resolved = _resolve_ingredient_master_id(cur, ingredient_name)
        if not was_resolved:
            app.logger.info(f"[apply] '{ingredient_name}' unresolved — skipping")
            skipped += 1
            skipped_lines.append({"line_id": str(line_id) if line_id else None,
                                   "ingredient_name": ingredient_name,
                                   "price_per_unit": float(price_per_unit) if price_per_unit is not None else None,
                                   "unit": unit, "supplier_name": supplier_name})
            continue
        cur.execute("""
            SELECT COALESCE(currency, 'CAD') AS currency
            FROM supplier_invoices WHERE id = %s
        """, (invoice_id,))
        curr_row = cur.fetchone()
        currency = curr_row["currency"] if curr_row else "CAD"
        cur.execute("""
            INSERT INTO price_history (
                ingredient_id, user_id, is_global,
                supplier_id, supplier_name,
                price_per_unit, unit, currency, yield_factor,
                invoice_id, invoice_line_id,
                effective_date, source
            )
            VALUES (%s, %s, false, %s, %s, %s, %s, %s, 1.0, %s, %s, %s, 'invoice')
        """, (
            master_id, str(user["id"]),
            supplier_id, supplier_name,
            float(price_per_unit), unit, currency,
            invoice_id, line_id, effective_date
        ))
        cur.execute("""
            INSERT INTO ingredient_aliases (ingredient_id, alias, source)
            VALUES (%s, %s, 'invoice')
            ON CONFLICT (alias_lower) DO NOTHING
        """, (master_id, ingredient_name))
        applied += 1

    cur.close()
    conn.close()
    return jsonify({"applied": applied, "skipped": skipped,
                    "skipped_lines": skipped_lines, "invoice_id": str(invoice_id)})


@app.route("/api/invoices")
@requires_tier("profession")
def invoices_list():
    """List supplier invoices for the current user."""
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT si.id, si.supplier_name, si.invoice_number, si.invoice_date,
               si.invoice_total, si.currency, si.created_at,
               COALESCE(si.page_count, 1) AS page_count,
               COUNT(sil.id) AS line_count
        FROM supplier_invoices si
        LEFT JOIN supplier_invoice_lines sil ON sil.invoice_id = si.id
        WHERE si.user_id = %s
        GROUP BY si.id
        ORDER BY si.created_at DESC
    """, (str(user["id"]),))
    rows = cur.fetchall()
    invoices = []
    for r in rows:
        invoices.append({
            "id": str(r["id"]),
            "supplier_name": r["supplier_name"],
            "invoice_number": r["invoice_number"],
            "invoice_date": str(r["invoice_date"]) if r["invoice_date"] else None,
            "invoice_total": float(r["invoice_total"]) if r["invoice_total"] else None,
            "currency": r["currency"],
            "line_count": int(r["line_count"]),
            "page_count": int(r["page_count"]),
            "created_at": str(r["created_at"]),
        })
    cur.close()
    conn.close()
    return jsonify({"invoices": invoices})


@app.route("/api/invoices/<invoice_id>/lines")
@requires_tier("profession")
def invoice_lines(invoice_id):
    """Return all line items for a specific invoice (for review UI)."""
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT supplier_name, invoice_date FROM supplier_invoices WHERE id = %s AND user_id = %s",
                (invoice_id, str(user["id"])))
    inv = cur.fetchone()
    if not inv:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("""
        SELECT id, line_number, raw_description, quantity, unit,
               unit_price, line_total, matched_ingredient_name, match_confidence
        FROM supplier_invoice_lines WHERE invoice_id = %s ORDER BY line_number
    """, (invoice_id,))
    lines = []
    for r in cur.fetchall():
        lines.append({
            "id": str(r["id"]),
            "line_number": r["line_number"],
            "raw_description": r["raw_description"],
            "quantity": float(r["quantity"]) if r["quantity"] is not None else None,
            "unit": r["unit"],
            "unit_price": float(r["unit_price"]) if r["unit_price"] is not None else None,
            "line_total": float(r["line_total"]) if r["line_total"] is not None else None,
            "matched_ingredient_name": r["matched_ingredient_name"] or r["raw_description"],
            "match_confidence": float(r["match_confidence"]) if r["match_confidence"] else 0.0,
        })
    cur.close()
    conn.close()
    return jsonify({
        "invoice_id": invoice_id,
        "supplier_name": inv["supplier_name"],
        "invoice_date": str(inv["invoice_date"]) if inv["invoice_date"] else None,
        "lines": lines,
    })


@app.route("/api/pricing/user")
def pricing_user():
    """Return the current user's active ingredient pricing table."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("kitchen"):
        return jsonify({"error": "Kitchen tier required"}), 403
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT
            ph.id::text AS id,
            COALESCE(im.canonical_name,
                     'Unknown ingredient (master_id ' || ph.ingredient_id || ')')
                AS ingredient_name,
            ph.price_per_unit, ph.unit, ph.supplier_name,
            ph.effective_date, ph.invoice_id::text AS invoice_id, ph.created_at,
            ph.source
        FROM price_history ph
        LEFT JOIN ingredient_master im ON im.id = ph.ingredient_id
        WHERE ph.user_id = %s
          AND ph.source IN ('invoice', 'manual', 'backfill_legacy')
        ORDER BY ph.effective_date DESC, im.canonical_name ASC
    """, (str(user["id"]),))
    rows = cur.fetchall()
    pricing = []
    for r in rows:
        pricing.append({
            "id": str(r["id"]),
            "ingredient_name": r["ingredient_name"],
            "price_per_unit": float(r["price_per_unit"]),
            "unit": r["unit"],
            "supplier_name": r["supplier_name"],
            "effective_date": str(r["effective_date"]) if r["effective_date"] else None,
            "invoice_id": str(r["invoice_id"]) if r.get("invoice_id") else None,
            "invoice_number": r.get("invoice_number"),
            "source": r.get("source") or ("invoice" if r.get("invoice_id") else "manual"),
        })
    cur.close()
    conn.close()
    return jsonify({"pricing": pricing})


@app.route("/api/pricing/manual", methods=["PUT", "POST"])
def pricing_manual():
    """Manually set/update an ingredient price for the current user."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401
    if not user_can_access("profession"):
        return jsonify({"error": "Profession tier required"}), 403
    data = request.get_json() or {}
    ingredient_name = (data.get("ingredient_name") or "").strip()
    price_per_unit = data.get("price_per_unit")
    unit = (data.get("unit") or "each").strip()
    supplier_name = (data.get("supplier_name") or "").strip() or None
    if not ingredient_name or price_per_unit is None:
        return jsonify({"error": "ingredient_name and price_per_unit required"}), 400
    import datetime
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM ingredient_master
        WHERE LOWER(canonical_name) = LOWER(%s) AND is_active = TRUE
        LIMIT 1
    """, (ingredient_name,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify({"error": f"'{ingredient_name}' is not in the ingredient catalog — add it first."}), 422
    master_id = row[0]
    currency = data.get('currency', 'CAD')
    cur.execute("""
        INSERT INTO price_history (
            ingredient_id, user_id, is_global,
            supplier_name,
            price_per_unit, unit, currency, yield_factor,
            effective_date, source
        )
        VALUES (%s, %s, false, %s, %s, %s, %s, 1.0, %s, 'manual')
    """, (
        master_id, str(user["id"]),
        supplier_name,
        float(price_per_unit), unit, currency,
        datetime.date.today()
    ))
    cur.execute("""
        INSERT INTO ingredient_aliases (ingredient_id, alias, source)
        VALUES (%s, %s, 'user')
        ON CONFLICT (alias_lower) DO NOTHING
    """, (master_id, ingredient_name))
    cur.close()
    conn.close()
    return jsonify({"success": True, "ingredient_name": ingredient_name,
                    "price_per_unit": float(price_per_unit), "unit": unit})


# ─── Ingredient catalog helpers (Cycle B.3) ──────────────────────────────────

@app.route("/api/ingredients/near-matches")
@requires_tier("profession")
def ingredients_near_matches():
    """Return up to 3 catalog entries similar to ?name=X, excluding chef-dismissed pairs."""
    name = (request.args.get("name") or "").strip()
    if not name:
        return jsonify({"matches": []})
    user = get_current_user()
    user_id = user["id"]
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # Branch 1: canonical name matches full query (substring or trigram).
        # Branch 2: alias_lower matches full query, returns linked canonical.
        # UNION ALL + GROUP BY MAX(score) deduplicates when a row hits both branches.
        cur.execute("""
            WITH q AS (SELECT LOWER(%s) AS full_q)
            SELECT id, canonical_name, ROUND(MAX(score)::numeric, 3) AS score
            FROM (
                SELECT m.id, m.canonical_name,
                       similarity(LOWER(m.canonical_name), q.full_q) AS score
                FROM ingredient_master m, q
                WHERE (
                    LOWER(m.canonical_name) LIKE '%%' || q.full_q || '%%'
                    OR similarity(LOWER(m.canonical_name), q.full_q) > 0.3
                )
                  AND NOT EXISTS (
                    SELECT 1 FROM ingredient_duplicate_dismissals d
                    WHERE d.user_id = %s
                      AND (d.master_id_a = m.id OR d.master_id_b = m.id)
                  )
                UNION ALL
                SELECT m.id, m.canonical_name,
                       similarity(ia.alias_lower, q.full_q) AS score
                FROM ingredient_aliases ia
                JOIN ingredient_master m ON m.id = ia.ingredient_id
                CROSS JOIN q
                WHERE ia.ingredient_id IS NOT NULL
                  AND (
                      ia.alias_lower LIKE q.full_q || '%%'
                      OR ia.alias_lower LIKE '%%' || q.full_q || '%%'
                      OR similarity(ia.alias_lower, q.full_q) > 0.3
                  )
                  AND NOT EXISTS (
                    SELECT 1 FROM ingredient_duplicate_dismissals d
                    WHERE d.user_id = %s
                      AND (d.master_id_a = m.id OR d.master_id_b = m.id)
                  )
            ) sub
            GROUP BY id, canonical_name
            ORDER BY score DESC, canonical_name
            LIMIT 3
        """, (name, user_id, user_id))
        rows = cur.fetchall()
        matches = [{"id": r["id"], "canonical_name": r["canonical_name"],
                    "score": float(r["score"])} for r in rows]
    except Exception:
        # pg_trgm unavailable — fall back to ILIKE substring (alias branch included)
        app.logger.warning("near-matches: pg_trgm unavailable, using ILIKE fallback")
        cur.execute("""
            SELECT id, canonical_name, 0.5 AS score
            FROM (
                SELECT m.id, m.canonical_name
                FROM ingredient_master m
                WHERE LOWER(m.canonical_name) LIKE %s
                  AND NOT EXISTS (
                    SELECT 1 FROM ingredient_duplicate_dismissals d
                    WHERE d.user_id = %s
                      AND (d.master_id_a = m.id OR d.master_id_b = m.id)
                  )
                UNION
                SELECT m.id, m.canonical_name
                FROM ingredient_aliases ia
                JOIN ingredient_master m ON m.id = ia.ingredient_id
                WHERE ia.alias_lower LIKE %s
                  AND ia.ingredient_id IS NOT NULL
                  AND NOT EXISTS (
                    SELECT 1 FROM ingredient_duplicate_dismissals d
                    WHERE d.user_id = %s
                      AND (d.master_id_a = m.id OR d.master_id_b = m.id)
                  )
            ) sub
            ORDER BY length(canonical_name) ASC
            LIMIT 3
        """, (f"%{name.lower()}%", user_id, f"%{name.lower()}%", user_id))
        rows = cur.fetchall()
        matches = [{"id": r["id"], "canonical_name": r["canonical_name"],
                    "score": float(r["score"])} for r in rows]
    cur.close()
    conn.close()
    return jsonify({"matches": matches})


@app.route("/api/ingredients/add-to-catalog", methods=["POST"])
@requires_tier("profession")
def ingredients_add_to_catalog():
    """Create a new ingredient_master entry from a chef-typed name."""
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    if len(name) > 200:
        return jsonify({"error": "name must be 200 characters or fewer"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Avoid exact-duplicate canonical names
    cur.execute("SELECT id, canonical_name FROM ingredient_master WHERE LOWER(canonical_name) = LOWER(%s) LIMIT 1", (name,))
    existing = cur.fetchone()
    if existing:
        cur.close(); conn.close()
        return jsonify({"id": existing["id"], "canonical_name": existing["canonical_name"], "already_existed": True})
    cur.execute("""
        INSERT INTO ingredient_master (canonical_name, is_active, created_at, updated_at)
        VALUES (%s, true, NOW(), NOW())
        RETURNING id, canonical_name
    """, (name,))
    row = cur.fetchone()
    # Register canonical alias so the resolver can find it immediately
    cur.execute("""
        INSERT INTO ingredient_aliases (ingredient_id, alias, source)
        VALUES (%s, %s, 'user')
        ON CONFLICT (alias_lower) DO NOTHING
    """, (row["id"], name))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": row["id"], "canonical_name": row["canonical_name"], "already_existed": False})


@app.route("/api/ingredients/dismiss-duplicate", methods=["POST"])
@requires_tier("profession")
def ingredients_dismiss_duplicate():
    """Record a chef's decision that two catalog entries are not duplicates."""
    data = request.get_json() or {}
    try:
        id_a = int(data.get("master_id_a", 0))
        id_b = int(data.get("master_id_b", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "master_id_a and master_id_b must be integers"}), 400
    if not id_a or not id_b or id_a == id_b:
        return jsonify({"error": "Two distinct master IDs required"}), 400
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ingredient_duplicate_dismissals (user_id, master_id_a, master_id_b)
        VALUES (%s, LEAST(%s,%s), GREATEST(%s,%s))
        ON CONFLICT (user_id, master_id_a, master_id_b) DO NOTHING
    """, (user["id"], id_a, id_b, id_a, id_b))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"dismissed": True})


@app.route("/api/invoices/<invoice_id>/resolve-line", methods=["POST"])
@requires_tier("profession")
def invoices_resolve_line(invoice_id):
    """Resolve a previously-skipped invoice line to a catalog master, then write price_history."""
    import datetime
    data = request.get_json() or {}
    line_id = data.get("line_id")
    master_id = data.get("master_id")
    if not line_id or not master_id:
        return jsonify({"error": "line_id and master_id required"}), 400
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Verify invoice belongs to user
    cur.execute("SELECT * FROM supplier_invoices WHERE id = %s AND user_id = %s",
                (invoice_id, str(user["id"])))
    inv = cur.fetchone()
    if not inv:
        cur.close(); conn.close()
        return jsonify({"error": "Invoice not found"}), 404
    # Look up the original line for price/unit data
    cur.execute("SELECT unit_price, unit, raw_description FROM supplier_invoice_lines WHERE id = %s AND invoice_id = %s",
                (line_id, invoice_id))
    sil = cur.fetchone()
    price_per_unit = float(sil["unit_price"]) if sil and sil["unit_price"] is not None else data.get("price_per_unit", 0)
    unit = (sil["unit"] if sil and sil["unit"] else data.get("unit", "each")) or "each"
    ingredient_name = sil["raw_description"] if sil else data.get("ingredient_name", "")
    effective_date = inv["invoice_date"] or datetime.date.today().isoformat()
    currency = inv.get("currency") or "CAD"
    supplier_id = inv["supplier_id"]
    supplier_name = inv["supplier_name"]
    cur.execute("""
        INSERT INTO price_history (
            ingredient_id, user_id, is_global,
            supplier_id, supplier_name,
            price_per_unit, unit, currency, yield_factor,
            invoice_id, invoice_line_id,
            effective_date, source
        )
        VALUES (%s, %s, false, %s, %s, %s, %s, %s, 1.0, %s, %s, %s, 'invoice')
    """, (master_id, str(user["id"]), supplier_id, supplier_name,
          price_per_unit, unit, currency, invoice_id, line_id, effective_date))
    cur.execute("""
        INSERT INTO ingredient_aliases (ingredient_id, alias, source)
        VALUES (%s, %s, 'invoice')
        ON CONFLICT (alias_lower) DO NOTHING
    """, (master_id, ingredient_name))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"resolved": True})


# ─── Sprint 8 — Recipe Search Endpoint ──────────────────────────────────────

@app.route("/api/recipes/search")
def recipes_search():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Login required"}), 401

    q = request.args.get("q", "").strip()
    include_canon = request.args.get("include_canon", "true").lower() != "false"
    include_kitchen = request.args.get("include_kitchen", "true").lower() != "false"
    limit = min(200, max(1, request.args.get("limit", 50, type=int)))
    user_id = user["id"]
    results = []

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # ── Kitchen recipes (user-scoped, shown first) ───────────────────────────
    if include_kitchen:
        pattern = f"%{q}%" if q else "%"
        cur.execute("""
            SELECT uuid, title, slug, has_image, origin, template_version,
                   recipe_content_jsonb, ingredients, steps,
                   quality_hierarchy, sensory_tests, cross_cuisine_parallels,
                   lives_or_dies, beverage_pairings
            FROM user_kitchen_recipes
            WHERE user_id = %s AND is_draft = FALSE AND slug IS NOT NULL
              AND (title ILIKE %s OR origin ILIKE %s)
            ORDER BY title ASC
            LIMIT %s
        """, (user_id, pattern, pattern, limit))
        for r in cur.fetchall():
            is_enhanced = (
                r.get("template_version") == "v3"
                or r.get("recipe_content_jsonb") is not None
            )
            state = "enhanced" if is_enhanced else "imported"
            content = r.get("recipe_content_jsonb") or {}
            cuisine = content.get("cuisine") or r.get("origin") or ""
            filled = sum([
                bool(r.get("ingredients")),
                bool(r.get("steps") or content.get("steps")),
                bool(r.get("quality_hierarchy")),
                bool(r.get("sensory_tests")),
                bool(r.get("cross_cuisine_parallels")),
                bool(r.get("lives_or_dies")),
                bool(r.get("beverage_pairings")),
            ])
            image_url = f"/images/{r['uuid']}/hero.jpg" if r.get("has_image") else None
            results.append({
                "recipe_ref": f"kitchen:{r['uuid']}",
                "state": state,
                "title": r.get("title") or "Untitled",
                "cuisine": cuisine,
                "image_url": image_url,
                "requires_haccp": _detect_raw_served(*_recipe_dict_to_haccp_inputs(r)),
                "pillars_filled": filled,
            })

    # ── Canon recipes ────────────────────────────────────────────────────────
    if include_canon:
        pattern = f"%{q}%" if q else "%"
        cur.execute("""
            SELECT slug, name, cuisine, image_url, ingredients, steps,
                   cross_cuisine_parallels, description, pairings
            FROM recipes
            WHERE slug IS NOT NULL AND slug != ''
              AND (name ILIKE %s OR cuisine ILIKE %s)
            ORDER BY name ASC
            LIMIT %s
        """, (pattern, pattern, limit))
        for r in cur.fetchall():
            filled = sum([
                bool(r.get("ingredients")),
                bool(r.get("steps")),
                bool(r.get("cross_cuisine_parallels")),
                bool(r.get("description")),
                bool(r.get("pairings")),
            ])
            results.append({
                "recipe_ref": f"canon:{r['slug']}",
                "state": "canon",
                "title": r.get("name") or "Untitled",
                "cuisine": r.get("cuisine") or "",
                "image_url": r.get("image_url") or None,
                "requires_haccp": _detect_raw_served(*_recipe_dict_to_haccp_inputs(r)),
                "pillars_filled": filled,
            })

    cur.close()
    conn.close()
    return jsonify({"results": results, "total_count": len(results)})


# ─── Sprint 8 — Menu Builder Page Routes ────────────────────────────────────

@app.route("/menu/new")
def menu_new_page():
    user = get_current_user()
    if not user:
        return _login_redirect()
    if not user_can_access("library"):
        return redirect("/pricing")
    return render_template("menu_new.html")


@app.route("/menu/<slug>")
def menu_detail_page(slug):
    user = get_current_user()
    if not user:
        return _login_redirect()
    if not user_can_access("library"):
        return redirect("/pricing")
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        abort(404)
    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu["id"],))
    mr_rows = cur.fetchall()
    _DEFAULT_COURSES = [
        ("Amuse", 1), ("Starter", 2), ("Main", 3), ("Cheese", 4), ("Dessert", 5)
    ]
    courses_map = {name: {"name": name, "order": order, "dishes": []} for name, order in _DEFAULT_COURSES}
    for mr in mr_rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user["id"], cur)
        except ValueError:
            recipe = None
        cn = mr["course_name"]
        if cn not in courses_map:
            courses_map[cn] = {"name": cn, "order": mr["course_order"], "dishes": []}
        courses_map[cn]["dishes"].append({
            "menu_recipe_id": str(mr["id"]),
            "recipe_ref": mr["recipe_ref"],
            "dish_order_within_course": mr["dish_order_within_course"],
            "recipe": dict(recipe) if recipe else None,
            "is_raw_served": _is_raw_served(recipe) if recipe else False,
        })
    courses = sorted(courses_map.values(), key=lambda c: c["order"])

    # ── Allergen aggregation for template ────────────────────────────────────
    allergen_data = _build_menu_allergens(str(menu["id"]), user["id"], cur)
    aggregated_allergens = allergen_data["aggregated_allergens"]
    allergens_by_course = allergen_data["allergens_by_course"]
    # ── Beverage pairing aggregation ─────────────────────────────────────────
    pairings_by_course = {}
    for course in courses:
        for dish in course["dishes"]:
            r = dish.get("recipe") or {}
            ref = dish.get("recipe_ref", "")
            prefix = ref.split(":")[0] if ":" in ref else ""
            raw = r.get("pairings") if prefix == "canon" else r.get("beverage_pairings")
            pairings_by_course.setdefault(course["name"], []).append({
                "course_order": course["order"],
                "dish_title": r.get("name") or r.get("title") or dish.get("recipe_ref", ""),
                "dish_image": r.get("image_url") or None,
                "pairings": _normalize_beverage_pairings(raw),
            })
    has_any_pairings = any(
        e["pairings"] for entries in pairings_by_course.values() for e in entries
    )

    user_can_see_cost = user_can_access("profession")
    user_can_print = user_can_access("profession")
    cost_data = None
    if user_can_see_cost:
        region = get_user_location() or "CA"
        covers = int(menu.get("cover_count") or 1)
        menu_price = menu.get("menu_price")
        cost_data = _compute_menu_cost(str(menu["id"]), covers, menu_price, user["id"], region, cur)

    compositions = _compositions_state(user["id"], cur)

    cur.close(); conn.close()
    menu_dict = dict(menu)
    menu_dict["id"] = str(menu_dict["id"])
    for k in ("event_date", "created_at", "updated_at", "last_exported_at"):
        if menu_dict.get(k) is not None:
            menu_dict[k] = menu_dict[k].isoformat()
    allergen_notes = allergen_data["allergen_notes"]
    return render_template(
        "menu_detail.html",
        menu=menu_dict,
        courses=courses,
        aggregated_allergens=aggregated_allergens,
        allergens_by_course=allergens_by_course,
        allergen_notes=allergen_notes,
        pairings_by_course=pairings_by_course,
        has_any_pairings=has_any_pairings,
        user_can_see_cost=user_can_see_cost,
        cost_data=cost_data,
        user_can_print=user_can_print,
        compositions=compositions,
    )


@app.route("/menu/<slug>/print/menu-card")
@requires_tier("profession")
def print_menu_card(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime

    user = get_current_user()
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        abort(404)

    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu["id"],))
    mr_rows = cur.fetchall()
    _DEFAULT_COURSES = [("Amuse", 1), ("Starter", 2), ("Main", 3), ("Cheese", 4), ("Dessert", 5)]
    courses_map = {name: {"name": name, "order": order, "dishes": []} for name, order in _DEFAULT_COURSES}
    for mr in mr_rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user["id"], cur)
        except ValueError:
            recipe = None
        cn = mr["course_name"]
        if cn not in courses_map:
            courses_map[cn] = {"name": cn, "order": mr["course_order"], "dishes": []}
        courses_map[cn]["dishes"].append({
            "menu_recipe_id": str(mr["id"]),
            "recipe_ref": mr["recipe_ref"],
            "dish_order_within_course": mr["dish_order_within_course"],
            "recipe": dict(recipe) if recipe else None,
        })
    courses = sorted(courses_map.values(), key=lambda c: c["order"])

    allergen_data = _build_menu_allergens(str(menu["id"]), user["id"], cur)
    aggregated_allergens = allergen_data["aggregated_allergens"]

    def _build_allergen_sentence(allergens):
        if not allergens:
            return "This menu has been reviewed for common allergens. Please tell us if any concern your table."
        fmt = [a.lower() for a in allergens]
        if len(fmt) == 1:
            return f"This menu contains {fmt[0]}. Please tell us if it concerns your table."
        joined = ", ".join(fmt[:-1]) + ", and " + fmt[-1]
        return f"This menu contains {joined}. Please tell us if any of these are a concern at your table."

    allergen_sentence = _build_allergen_sentence(aggregated_allergens)

    cur.execute("UPDATE menus SET last_exported_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()

    menu_dict = dict(menu)
    menu_dict["id"] = str(menu_dict["id"])
    for k in ("event_date", "created_at", "updated_at", "last_exported_at"):
        if menu_dict.get(k) is not None:
            menu_dict[k] = menu_dict[k].isoformat()

    gen_stamp = datetime.now().strftime('%-d %B %Y · %H:%M')

    html = render_template(
        "print/menu_card.html",
        menu=menu_dict,
        courses=courses,
        aggregated_allergens=aggregated_allergens,
        allergen_sentence=allergen_sentence,
        gen_stamp=gen_stamp,
    )

    try:
        pdf_bytes = WeasyHTML(string=html, base_url=request.host_url).write_pdf()
    except Exception:
        app.logger.exception(f"WeasyPrint error for menu-card {slug}")
        abort(500)

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f'inline; filename="menu-card-{slug}.pdf"'},
    )


@app.route("/menu/<slug>/print/costing-sheet")
@requires_tier("profession")
def print_costing_sheet(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime

    user = get_current_user()
    region = get_user_location() or "CA"
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        abort(404)

    covers = int(menu.get("cover_count") or 1)
    menu_price = menu.get("menu_price")
    cost = _compute_menu_cost_with_provenance(str(menu["id"]), covers, menu_price, user["id"], region, cur)

    cur.execute("UPDATE menus SET last_exported_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()

    menu_dict = dict(menu)
    menu_dict["id"] = str(menu_dict["id"])
    for k in ("event_date", "created_at", "updated_at", "last_exported_at"):
        if menu_dict.get(k) is not None:
            menu_dict[k] = menu_dict[k].isoformat()

    gen_stamp = datetime.now().strftime('%-d %B %Y · %H:%M')

    html = render_template(
        "print/costing_sheet.html",
        menu=menu_dict,
        cost=cost,
        gen_stamp=gen_stamp,
    )

    try:
        pdf_bytes = WeasyHTML(string=html, base_url=request.host_url).write_pdf()
    except Exception:
        app.logger.exception(f"WeasyPrint error for costing-sheet {slug}")
        abort(500)

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f'inline; filename="costing-sheet-{slug}.pdf"'},
    )


@app.route("/menu/<slug>/print/allergen-card")
@requires_tier("profession")
def print_allergen_card(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime

    user = get_current_user()
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        abort(404)

    allergen_data = _build_menu_allergens(str(menu["id"]), user["id"], cur)
    aggregated_allergens = allergen_data["aggregated_allergens"]
    allergens_by_course = allergen_data["allergens_by_course"]
    allergen_notes = allergen_data["allergen_notes"]

    # Build flat per-dish list for the grid (one row per dish, all its allergens)
    dishes_allergens = {}
    for allergen, dishes in allergens_by_course.items():
        for d in dishes:
            mid = d["menu_recipe_id"]
            if mid not in dishes_allergens:
                dishes_allergens[mid] = {
                    "course_name": d["course_name"],
                    "dish_title": d["dish_title"],
                    "course_order": d.get("course_order", 0),
                    "dish_order": d.get("dish_order_within_course", 0),
                    "allergens": [],
                }
            dishes_allergens[mid]["allergens"].append(allergen)
    dishes_allergens_list = sorted(
        dishes_allergens.values(),
        key=lambda x: (x["course_order"], x["dish_order"]),
    )

    cur.execute("UPDATE menus SET last_exported_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()

    menu_dict = dict(menu)
    menu_dict["id"] = str(menu_dict["id"])
    for k in ("event_date", "created_at", "updated_at", "last_exported_at"):
        if menu_dict.get(k) is not None:
            menu_dict[k] = menu_dict[k].isoformat()

    gen_stamp = datetime.now().strftime('%-d %B %Y · %H:%M')

    html = render_template(
        "print/allergen_card.html",
        menu=menu_dict,
        aggregated_allergens=aggregated_allergens,
        allergens_by_course=allergens_by_course,
        allergen_notes=allergen_notes,
        dishes_allergens_list=dishes_allergens_list,
        gen_stamp=gen_stamp,
    )

    try:
        pdf_bytes = WeasyHTML(string=html, base_url=request.host_url).write_pdf()
    except Exception:
        app.logger.exception(f"WeasyPrint error for allergen-card {slug}")
        abort(500)

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f'inline; filename="allergen-card-{slug}.pdf"'},
    )


@app.route("/menu/<slug>/print/beverage-program")
@requires_tier("profession")
def print_beverage_program(slug):
    from weasyprint import HTML as WeasyHTML
    from datetime import datetime

    user = get_current_user()
    region = get_user_location() or "CA"
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        abort(404)

    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu["id"],))
    mr_rows = cur.fetchall()
    _DEFAULT_COURSES = [("Amuse", 1), ("Starter", 2), ("Main", 3), ("Cheese", 4), ("Dessert", 5)]
    courses_map = {name: {"name": name, "order": order, "dishes": []} for name, order in _DEFAULT_COURSES}
    for mr in mr_rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user["id"], cur)
        except ValueError:
            recipe = None
        cn = mr["course_name"]
        if cn not in courses_map:
            courses_map[cn] = {"name": cn, "order": mr["course_order"], "dishes": []}
        courses_map[cn]["dishes"].append({
            "menu_recipe_id": str(mr["id"]),
            "recipe_ref": mr["recipe_ref"],
            "dish_order_within_course": mr["dish_order_within_course"],
            "recipe": dict(recipe) if recipe else None,
        })
    courses = sorted(courses_map.values(), key=lambda c: c["order"])

    pairings_by_course = {}
    all_product_ids = []
    for course in courses:
        for dish in course["dishes"]:
            r = dish.get("recipe") or {}
            ref = dish.get("recipe_ref", "")
            prefix = ref.split(":")[0] if ":" in ref else ""
            raw = r.get("pairings") if prefix == "canon" else r.get("beverage_pairings")
            pairings = _normalize_beverage_pairings(raw)
            for p in pairings:
                if p.get("product_id") is not None:
                    all_product_ids.append(p["product_id"])
            pairings_by_course.setdefault(course["name"], []).append({
                "course_order": course["order"],
                "dish_title": r.get("name") or r.get("title") or dish.get("recipe_ref", ""),
                "dish_image": r.get("image_url") or None,
                "pairings": pairings,
            })

    provider_lookup = _pats_rule_for_beverages(all_product_ids, region, cur)
    for entries in pairings_by_course.values():
        for entry in entries:
            for p in entry["pairings"]:
                p["local_provider"] = provider_lookup.get(p.get("product_id"))

    has_any_pairings = any(
        e["pairings"] for entries in pairings_by_course.values() for e in entries
    )

    cur.execute("UPDATE menus SET last_exported_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()

    menu_dict = dict(menu)
    menu_dict["id"] = str(menu_dict["id"])
    for k in ("event_date", "created_at", "updated_at", "last_exported_at"):
        if menu_dict.get(k) is not None:
            menu_dict[k] = menu_dict[k].isoformat()

    gen_stamp = datetime.now().strftime('%-d %B %Y · %H:%M')

    html = render_template(
        "print/beverage_program.html",
        menu=menu_dict,
        courses=courses,
        pairings_by_course=pairings_by_course,
        has_any_pairings=has_any_pairings,
        region=region,
        gen_stamp=gen_stamp,
    )

    try:
        pdf_bytes = WeasyHTML(string=html, base_url=request.host_url).write_pdf()
    except Exception:
        app.logger.exception(f"WeasyPrint error for beverage-program {slug}")
        abort(500)

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f'inline; filename="beverage-program-{slug}.pdf"'},
    )


# ─── Sprint 8 — Menu Builder Routes ─────────────────────────────────────────

def _normalize_beverage_pairings(raw):
    """Normalize beverage_pairings (kitchen) or pairings (canon) to [{role, descriptor, producer, product_id}].
    product_id is sourced from beverage_product_id on kitchen pairing dicts; used by print routes for Pat's Rule.
    Screen rendering ignores the new field — only reads role/descriptor/producer.
    """
    if not raw or not isinstance(raw, list):
        return []
    out = []
    for p in raw:
        if isinstance(p, str):
            if p.strip():
                out.append({"role": "", "descriptor": p.strip(), "producer": "", "product_id": None})
        elif isinstance(p, dict):
            tier = (p.get("tier_label") or "").strip()
            ptype = (p.get("pairing_type") or "").strip()
            role = tier.title() if tier else ptype.title() if ptype else ""
            desc = (p.get("flavour_logic") or p.get("beverage_description") or "").strip()
            producer = (p.get("beverage_name") or "").strip()
            product_id = p.get("beverage_product_id")
            if producer or desc:
                out.append({"role": role, "descriptor": desc, "producer": producer, "product_id": product_id})
    return out


def _compute_menu_cost(menu_id, covers, menu_price, user_id, region, cur):
    """Aggregate food cost across all dishes in a menu. Returns cost breakdown dict."""
    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu_id,))
    rows = cur.fetchall()
    per_dish = []
    total_food_cost = 0.0
    any_missing_cost = False
    for mr in rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user_id, cur)
        except ValueError:
            recipe = None
        dish_title = mr["recipe_ref"]
        dish_image = None
        if recipe:
            dish_title = recipe.get("name") or recipe.get("title") or mr["recipe_ref"]
            dish_image = recipe.get("image_url") or None
        cost_result = _compute_recipe_cost(recipe, region) if recipe else None
        if not cost_result or not cost_result.get("cost_per_portion"):
            per_dish.append({
                "menu_recipe_id": str(mr["id"]),
                "course_name": mr["course_name"],
                "dish_title": dish_title,
                "dish_image": dish_image,
                "cost_per_serving": None,
                "cost_for_menu": None,
                "has_cost_data": False,
            })
            any_missing_cost = True
        else:
            cps = cost_result["cost_per_portion"]
            cfm = round(cps * covers, 2)
            total_food_cost += cfm
            per_dish.append({
                "menu_recipe_id": str(mr["id"]),
                "course_name": mr["course_name"],
                "dish_title": dish_title,
                "dish_image": dish_image,
                "cost_per_serving": round(cps, 2),
                "cost_for_menu": cfm,
                "has_cost_data": True,
            })
    total_food_cost = round(total_food_cost, 2)
    cost_per_cover = round(total_food_cost / covers, 2) if covers > 0 else 0.0
    mp = float(menu_price) if menu_price else None
    projected_food_cost_pct = None
    if mp and mp > 0 and covers > 0:
        revenue = mp * covers
        projected_food_cost_pct = round((total_food_cost / revenue) * 100, 1) if revenue > 0 else None
    return {
        "covers": covers,
        "menu_price": mp,
        "per_dish": per_dish,
        "total_food_cost": total_food_cost,
        "cost_per_cover": cost_per_cover,
        "projected_food_cost_pct": projected_food_cost_pct,
        "target_window": {"low": 28.0, "high": 35.0},
        "any_missing_cost": any_missing_cost,
    }


def _build_menu_allergens(menu_id, user_id, cur):
    """Aggregate allergen data for a menu. Single source of truth used by menu_detail_page,
    all print routes, and the get_menu API.

    Returns dict:
      aggregated_allergens  — sorted list of allergen strings
      allergens_by_course   — dict: allergen → [{course_name, dish_title, menu_recipe_id,
                                                  recipe_image, course_order,
                                                  dish_order_within_course}]
      allergen_notes        — dict: allergen → chef's note string (from menus.allergen_notes)
    """
    cur.execute("""
        SELECT id, recipe_ref, course_name, course_order, dish_order_within_course
        FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu_id,))
    mr_rows = cur.fetchall()

    allergens_by_course = {}
    for mr in mr_rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user_id, cur)
        except ValueError:
            recipe = None
        r = dict(recipe) if recipe else {}
        allergen_cache = r.get("allergens") or {}
        detected = allergen_cache.get("detected", []) if isinstance(allergen_cache, dict) else []
        dish_title = r.get("name") or r.get("title") or mr["recipe_ref"]
        for allergen in detected:
            allergens_by_course.setdefault(allergen, []).append({
                "course_name": mr["course_name"],
                "dish_title": dish_title,
                "menu_recipe_id": str(mr["id"]),
                "recipe_image": r.get("image_url") or None,
                "course_order": mr["course_order"],
                "dish_order_within_course": mr["dish_order_within_course"],
            })

    cur.execute("SELECT allergen_notes FROM menus WHERE id = %s", (menu_id,))
    row = cur.fetchone()
    allergen_notes = (row["allergen_notes"] if row else None) or {}

    return {
        "aggregated_allergens": sorted(allergens_by_course.keys()),
        "allergens_by_course": allergens_by_course,
        "allergen_notes": allergen_notes,
    }


def _pats_rule_for_ingredients(ingredient_names, region, cur):
    """Batch resolve origin producer + local provider for a list of ingredient names.

    Pat's Rule: ingredient_master.source_product_id → product_suppliers (ORIGIN always,
    PROVIDER region-filtered) → suppliers.name.

    Returns dict keyed by lowercase name: {origin_producer: str|None, local_provider: str|None}.
    """
    if not ingredient_names:
        return {}

    _CA_PROVINCES = {'BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'NT', 'YT', 'NU'}
    region_terms = [region] if region else ['nowhere']
    if region in _CA_PROVINCES:
        region_terms += ['nationwide_CA', 'Western_Canada']
    elif region:
        region_terms += ['nationwide_US']

    # Step 1: resolve names → master_ids
    name_to_master = {}
    for name in ingredient_names:
        n = name.lower().strip()
        if not n:
            continue
        master_id, ok = _resolve_ingredient_master_id(cur, n)
        if ok and master_id:
            name_to_master[n] = master_id

    empty = {name.lower().strip(): {"origin_producer": None, "local_provider": None} for name in ingredient_names}
    if not name_to_master:
        return empty

    # Step 2: master_ids → source_product_ids
    master_ids = list(set(name_to_master.values()))
    cur.execute(
        "SELECT id, source_product_id FROM ingredient_master WHERE id = ANY(%s) AND source_product_id IS NOT NULL",
        (master_ids,),
    )
    master_to_product = {row["id"]: row["source_product_id"] for row in cur.fetchall()}

    product_ids = list(set(master_to_product.values()))
    if not product_ids:
        return empty

    # Step 3: product_ids → origin + region-filtered provider suppliers
    cur.execute("""
        SELECT ps.product_id, ps.role, ps.is_primary, s.name AS supplier_name
        FROM product_suppliers ps
        JOIN suppliers s ON ps.supplier_id = s.id
        WHERE ps.product_id = ANY(%s)
          AND (ps.role = 'ORIGIN' OR (ps.role = 'PROVIDER' AND ps.region && %s::text[]))
        ORDER BY ps.product_id, ps.role, ps.is_primary DESC, s.name
    """, (product_ids, region_terms))

    product_prov = {}
    for row in cur.fetchall():
        pid = row["product_id"]
        if pid not in product_prov:
            product_prov[pid] = {"origin_producer": None, "local_provider": None}
        if row["role"] == "ORIGIN" and not product_prov[pid]["origin_producer"]:
            product_prov[pid]["origin_producer"] = row["supplier_name"]
        elif row["role"] == "PROVIDER" and not product_prov[pid]["local_provider"]:
            product_prov[pid]["local_provider"] = row["supplier_name"]

    result = {}
    for name in ingredient_names:
        n = name.lower().strip()
        master_id = name_to_master.get(n)
        product_id = master_to_product.get(master_id) if master_id else None
        result[n] = product_prov.get(product_id) or {"origin_producer": None, "local_provider": None}
    return result


def _pats_rule_for_beverages(product_ids, region, cur):
    """Batch resolve local provider for a list of beverage_product_ids.

    Symmetric counterpart to _pats_rule_for_ingredients. Skips the master_id step
    because product_id is already known on each pairing. beverage_product_suppliers
    has no is_primary column — first alphabetical match per product wins.

    Returns dict keyed by product_id → local_provider supplier name (str) or None.
    Fails gracefully if beverage_product_suppliers is empty or missing.
    """
    if not product_ids:
        return {}

    _CA_PROVINCES = {'BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'NT', 'YT', 'NU'}
    region_terms = [region] if region else ['nowhere']
    if region in _CA_PROVINCES:
        region_terms += ['nationwide_CA', 'Western_Canada']
    elif region:
        region_terms += ['nationwide_US']

    valid_ids = [int(pid) for pid in product_ids if pid is not None]
    result = {pid: None for pid in product_ids}
    if not valid_ids:
        return result

    try:
        cur.execute("""
            SELECT bps.product_id, s.name AS supplier_name
            FROM beverage_product_suppliers bps
            JOIN suppliers s ON bps.supplier_id = s.id AND s.verification_status = 'verified_provider'
            WHERE bps.product_id = ANY(%s)
              AND bps.role = 'PROVIDER'
              AND bps.region && %s::text[]
            ORDER BY bps.product_id, s.name
        """, (valid_ids, region_terms))
        seen = set()
        for row in cur.fetchall():
            pid = row["product_id"]
            if pid not in seen:
                seen.add(pid)
                result[pid] = row["supplier_name"]
    except Exception:
        app.logger.warning("_pats_rule_for_beverages query failed — returning all None")
    return result


def _suggest_beverages_for_recipe(recipe, limit=5, cur=None):
    """Score beverage pairings for a recipe using the locked priority chain.

    Priority: supplier (×1.0) > canon (×0.7) > web (×0.5, stub until web_verified flag added).
    Matching is against pairing_intelligence.food_category / food_profile.
    Always preserves at least one supplier-tier result when any exist.
    Returns list of dicts sorted by weighted score desc.
    """
    if cur is None:
        return []

    food_category = None
    food_terms = []
    tags = recipe.get("tradition_tags") or recipe.get("tags") or []
    if isinstance(tags, list) and tags:
        food_category = tags[0]
    elif isinstance(tags, str):
        food_category = tags
    title = recipe.get("name") or recipe.get("title") or ""
    cuisine = recipe.get("cuisine") or ""
    for term in [food_category, cuisine] + title.split():
        t = (term or "").strip().lower()
        if t and len(t) >= 3:
            food_terms.append(t)
    food_terms = list(dict.fromkeys(food_terms))[:4]

    _ROLE_MAP = {
        "complement": "Complement",
        "contrast":   "Contrast",
        "regional":   "Bridge",
        "tradition":  "Bridge",
        "bridge":     "Bridge",
    }
    _NA_CATEGORIES = {"tea", "coffee", "soda", "juice", "infusion", "mocktail",
                      "soft_drink", "kombucha", "sparkling_water"}

    def _score_rows(rows, multiplier, tier):
        out = []
        for r in rows:
            raw = float(r.get("confidence") or 0.5)
            pt = (r.get("pairing_type") or "").lower()
            bev_cat = (r.get("category") or "").lower()
            role = "Non-alcoholic" if bev_cat in _NA_CATEGORIES else _ROLE_MAP.get(pt, "Complement")
            fc = r.get("food_category") or ""
            reasoning = f"source: {tier} · category: {fc} · pairing: {pt}"
            out.append({
                "beverage_product_id": r["beverage_product_id"],
                "source_tier": tier,
                "role": role,
                "descriptor": r.get("flavour_logic") or "",
                "match_score": round(raw * multiplier, 4),
                "match_reasoning": reasoning,
            })
        return out

    seen_ids = set()
    results = []

    # PASS 1 — Trade-tier supplier beverages.
    # suppliers table has no tier column yet; this pass returns empty until that column is added.
    try:
        if food_category:
            cur.execute("""
                SELECT pi.food_profile, pi.food_category, pi.pairing_type, pi.flavour_logic,
                       pi.confidence, bp.id AS beverage_product_id, bp.category
                FROM pairing_intelligence pi
                JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
                JOIN beverage_product_suppliers bps ON bps.product_id = bp.id
                JOIN suppliers s ON bps.supplier_id = s.id AND s.verification_status = 'verified_provider'
                WHERE pi.food_category ILIKE %s
                  AND pi.beverage_product_id IS NOT NULL
                  AND s.tier = 'trade'
                ORDER BY pi.confidence DESC
                LIMIT %s
            """, (f"%{food_category}%", limit))
            supplier_rows = cur.fetchall()
            for row in _score_rows(supplier_rows, 1.0, "supplier"):
                if row["beverage_product_id"] not in seen_ids:
                    seen_ids.add(row["beverage_product_id"])
                    results.append(row)
    except Exception:
        pass  # tier column absent — pass 1 yields nothing until schema is extended

    supplier_count = len(results)

    # PASS 2 — Beverage canon (pairing_intelligence → beverage_products, no supplier filter).
    try:
        conditions, params = [], []
        if food_category:
            conditions.append("pi.food_category ILIKE %s")
            params.append(f"%{food_category}%")
        elif food_terms:
            or_clauses = " OR ".join("pi.food_profile ILIKE %s" for _ in food_terms[:3])
            conditions.append(f"({or_clauses})")
            params.extend(f"%{t}%" for t in food_terms[:3])
        if not conditions:
            conditions.append("TRUE")
        where = " AND ".join(conditions)
        params.append(limit * 3)
        cur.execute(f"""
            SELECT pi.food_profile, pi.food_category, pi.pairing_type, pi.flavour_logic,
                   pi.confidence, bp.id AS beverage_product_id, bp.category
            FROM pairing_intelligence pi
            JOIN beverage_products bp ON pi.beverage_product_id = bp.id AND bp.is_published IS TRUE
            WHERE {where}
              AND pi.beverage_product_id IS NOT NULL
            ORDER BY pi.confidence DESC
            LIMIT %s
        """, params)
        for row in _score_rows(cur.fetchall(), 0.7, "canon"):
            if row["beverage_product_id"] not in seen_ids:
                seen_ids.add(row["beverage_product_id"])
                results.append(row)
    except Exception as e:
        app.logger.warning("_suggest_beverages pass 2 failed: %s", e)

    # PASS 3 — Sashimi-verified web suppliers (stub — no web_verified flag exists yet).
    # Slot reserved; no-op until beverage_products.web_verified is added.

    results.sort(key=lambda r: r["match_score"], reverse=True)
    # Guarantee at least one supplier-tier result at the front when any exist.
    if supplier_count > 0 and results and results[0]["source_tier"] != "supplier":
        supplier_items = [r for r in results if r["source_tier"] == "supplier"]
        other_items = [r for r in results if r["source_tier"] != "supplier"]
        results = supplier_items[:1] + other_items
    return results[:limit]


def _extract_method_steps(recipe):
    """Return a list of step strings from a recipe dict. Handles multiple shapes:
    1. recipe['steps'] JSONB list of dicts with 'instruction' key (canon recipes)
    2. recipe['method_steps'] list of strings or dicts
    3. recipe['recipe_content_jsonb']['method_steps'] (user_kitchen_recipes)
    4. recipe['full_content']['method_steps'] or ['steps'] (canon JSONB blob)
    Returns [] if none populated.
    """
    fc = recipe.get("full_content") or {}
    candidates = [
        recipe.get("steps"),
        recipe.get("method_steps"),
        (recipe.get("recipe_content_jsonb") or {}).get("method_steps"),
        fc.get("method_steps"),
        fc.get("steps"),
    ]
    for c in candidates:
        if not c:
            continue
        if isinstance(c, list):
            out = []
            for s in c:
                if isinstance(s, str) and s.strip():
                    out.append(s.strip())
                elif isinstance(s, dict):
                    text = s.get("instruction") or s.get("text") or s.get("step") or ""
                    if text.strip():
                        out.append(text.strip())
            if out:
                return out
        elif isinstance(c, str) and c.strip():
            return [c.strip()]
    return []


def _extract_service_notes(recipe):
    """Return service_notes string or None.
    service_notes is not a first-class DB column (Step 1 discovery) —
    only read from recipe_content_jsonb.
    """
    jsonb = recipe.get("recipe_content_jsonb") or {}
    val = jsonb.get("service_notes") or jsonb.get("service_note")
    if isinstance(val, str) and val.strip():
        return val.strip()
    return None


def _compute_menu_cost_with_provenance(menu_id, covers, menu_price, user_id, region, cur):
    """Like _compute_menu_cost but enriches each ingredient line with Pat's Rule provenance."""
    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu_id,))
    rows = cur.fetchall()

    per_dish = []
    total_food_cost = 0.0
    any_missing_cost = False

    for mr in rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user_id, cur)
        except ValueError:
            recipe = None

        dish_title = mr["recipe_ref"]
        dish_image = None
        if recipe:
            dish_title = recipe.get("name") or recipe.get("title") or mr["recipe_ref"]
            dish_image = recipe.get("image_url") or None

        if not recipe:
            per_dish.append({
                "menu_recipe_id": str(mr["id"]),
                "course_name": mr["course_name"],
                "dish_title": dish_title,
                "dish_image": dish_image,
                "ingredients": [],
                "dish_total_cost": None,
                "dish_cost_per_cover": None,
                "has_cost_data": False,
                "method_steps": [],
                "service_notes": None,
            })
            any_missing_cost = True
            continue

        ingredients = recipe.get("ingredients") or []
        if isinstance(ingredients, str):
            try:
                import json as _json
                ingredients = _json.loads(ingredients)
            except Exception:
                ingredients = []

        _srv = recipe.get("servings") or recipe.get("yield_count") or 1
        if isinstance(_srv, dict):
            _srv = _srv.get("count") or 1
        elif isinstance(_srv, str) and not _srv.strip().lstrip("-").replace(".", "", 1).isdigit():
            try:
                import json as _json
                _p = _json.loads(_srv.replace("'", '"'))
                _srv = _p.get("count", 1) if isinstance(_p, dict) else 1
            except Exception:
                _srv = 1
        try:
            recipe_portions = max(int(float(_srv or 1)), 1)
        except (ValueError, TypeError):
            recipe_portions = 1
        scale = covers / recipe_portions

        breakdown, dish_base_cost, unpriced, _ = _cost_ingredient_loop(
            ingredients, user_id, True, cur
        )
        # dish_base_cost is the total for recipe_portions; scale to covers
        dish_cost_for_menu = round(dish_base_cost * scale, 2)
        dish_cost_per_cover = round(dish_base_cost / recipe_portions, 2)

        ing_names = [(item.get("ingredient") or item.get("name") or "") for item in breakdown]
        provenance = _pats_rule_for_ingredients(ing_names, region, cur)

        enriched = []
        for item in breakdown:
            ing_name = item.get("ingredient") or item.get("name") or ""
            prov = provenance.get(ing_name.lower().strip()) or {}
            lc = item.get("line_cost")
            enriched.append({
                "ingredient": ing_name,
                "quantity": item.get("quantity"),
                "unit": item.get("unit"),
                "line_cost": round(lc * scale, 2) if lc is not None else None,
                "origin_producer": prov.get("origin_producer"),
                "local_provider": prov.get("local_provider"),
                "currency": item.get("currency") or "CAD",
            })

        if unpriced:
            any_missing_cost = True

        total_food_cost += dish_cost_for_menu
        per_dish.append({
            "menu_recipe_id": str(mr["id"]),
            "course_name": mr["course_name"],
            "dish_title": dish_title,
            "dish_image": dish_image,
            "ingredients": enriched,
            "dish_total_cost": dish_cost_for_menu,
            "dish_cost_per_cover": dish_cost_per_cover,
            "has_cost_data": dish_base_cost > 0,
            "method_steps": _extract_method_steps(recipe),
            "service_notes": _extract_service_notes(recipe),
        })

    total_food_cost = round(total_food_cost, 2)
    cost_per_cover = round(total_food_cost / covers, 2) if covers > 0 else 0.0
    mp = float(menu_price) if menu_price else None
    projected_food_cost_pct = None
    if mp and mp > 0 and covers > 0:
        revenue = mp * covers
        projected_food_cost_pct = round((total_food_cost / revenue) * 100, 1) if revenue > 0 else None
    return {
        "covers": covers,
        "menu_price": mp,
        "per_dish": per_dish,
        "total_food_cost": total_food_cost,
        "cost_per_cover": cost_per_cover,
        "projected_food_cost_pct": projected_food_cost_pct,
        "target_window": {"low": 28.0, "high": 35.0},
        "any_missing_cost": any_missing_cost,
    }


def _compositions_state(user_id, cur):
    """Return composition state dict for the given user.

    Returns {has_atelier, used_this_month, free_limit, remaining, can_compose}.
    free_limit is fixed at 20 for beta. l'Atelier members (has_atelier=True) can_compose
    regardless of remaining count.
    """
    cur.execute(
        "SELECT COALESCE(has_atelier_addon, FALSE) AS has_atelier FROM users WHERE id = %s",
        (user_id,),
    )
    row = cur.fetchone()
    has_atelier = bool(row["has_atelier"]) if row else False

    cur.execute("""
        SELECT COUNT(*) AS n FROM composition_events
        WHERE user_id = %s AND created_at >= date_trunc('month', NOW())
    """, (user_id,))
    used = int((cur.fetchone() or {}).get("n", 0) or 0)

    free_limit = 20
    remaining = max(free_limit - used, 0)
    can_compose = remaining > 0 or has_atelier

    return {
        "has_atelier": has_atelier,
        "used_this_month": used,
        "free_limit": free_limit,
        "remaining": remaining,
        "can_compose": can_compose,
    }


def _menu_slug_unique(base, cur):
    """Return base slug, appending -2, -3, etc. until unique in menus."""
    candidate, n = base, 2
    while True:
        cur.execute("SELECT 1 FROM menus WHERE slug = %s", (candidate,))
        if not cur.fetchone():
            return candidate
        candidate = f"{base}-{n}"
        n += 1


def _menu_to_dict(row):
    """Convert a menus row to a JSON-safe dict."""
    d = dict(row)
    d['id'] = str(d['id'])
    for k in ('event_date', 'created_at', 'updated_at', 'last_exported_at'):
        if d.get(k) is not None:
            d[k] = d[k].isoformat()
    return d


def _menu_recipe_to_dict(row):
    """Convert a menu_recipes row to a JSON-safe dict."""
    d = dict(row)
    d['id'] = str(d['id'])
    d['menu_id'] = str(d['menu_id'])
    if d.get('created_at') is not None:
        d['created_at'] = d['created_at'].isoformat()
    return d


@app.route("/api/menus", methods=["GET"])
@requires_tier("library")
def list_menus():
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT m.id, m.slug, m.title, m.event_date, m.cover_count, m.updated_at,
               COUNT(DISTINCT mr.course_name) AS course_count,
               COUNT(mr.id) AS dish_count
        FROM menus m
        LEFT JOIN menu_recipes mr ON mr.menu_id = m.id
        WHERE m.owner_user_id = %s
        GROUP BY m.id
        ORDER BY m.event_date DESC NULLS LAST, m.updated_at DESC
    """, (user["id"],))
    rows = cur.fetchall()
    cur.close(); conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d['id'] = str(d['id'])
        d['course_count'] = int(d['course_count'])
        d['dish_count'] = int(d['dish_count'])
        if d.get('event_date') is not None:
            d['event_date'] = d['event_date'].isoformat()
        if d.get('updated_at') is not None:
            d['updated_at'] = d['updated_at'].isoformat()
        result.append(d)
    return jsonify(result)


@app.route("/api/menus", methods=["POST"])
@requires_tier("library")
def create_menu():
    user = get_current_user()
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    slug_base = (_slugify(title) or 'menu')[:80]
    slug = _menu_slug_unique(slug_base, cur)
    cur.execute("""
        INSERT INTO menus (slug, owner_user_id, title, event_date, cover_count, chef_notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
    """, (
        slug, user["id"], title,
        data.get("event_date") or None,
        int(data.get("cover_count", 1)),
        data.get("chef_notes") or None,
    ))
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(_menu_to_dict(row)), 201


@app.route("/api/menu/<slug>", methods=["GET"])
@requires_tier("library")
def get_menu(slug):
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("""
        SELECT * FROM menu_recipes WHERE menu_id = %s
        ORDER BY course_order, dish_order_within_course
    """, (menu["id"],))
    mr_rows = cur.fetchall()
    courses_map = {}
    for mr in mr_rows:
        try:
            recipe = _resolve_recipe_ref(mr["recipe_ref"], user["id"], cur)
        except ValueError:
            recipe = None
        cn = mr["course_name"]
        if cn not in courses_map:
            courses_map[cn] = {"name": cn, "order": mr["course_order"], "dishes": []}
        courses_map[cn]["dishes"].append({
            "menu_recipe_id": str(mr["id"]),
            "recipe_ref": mr["recipe_ref"],
            "dish_order_within_course": mr["dish_order_within_course"],
            "recipe": dict(recipe) if recipe else None,
        })
    # ── Allergen aggregation ─────────────────────────────────────────────────
    allergen_data = _build_menu_allergens(str(menu["id"]), user["id"], cur)
    aggregated_allergens = allergen_data["aggregated_allergens"]
    allergens_by_course = allergen_data["allergens_by_course"]
    # ── Beverage pairing aggregation ─────────────────────────────────────────
    pairings_by_course = {}
    for course in sorted(courses_map.values(), key=lambda c: c["order"]):
        for dish in course["dishes"]:
            r = dish.get("recipe") or {}
            ref = dish.get("recipe_ref", "")
            prefix = ref.split(":")[0] if ":" in ref else ""
            raw = r.get("pairings") if prefix == "canon" else r.get("beverage_pairings")
            pairings_by_course.setdefault(course["name"], []).append({
                "course_order": course["order"],
                "dish_title": r.get("name") or r.get("title") or dish.get("recipe_ref", ""),
                "dish_image": r.get("image_url") or None,
                "pairings": _normalize_beverage_pairings(raw),
            })
    result = _menu_to_dict(menu)
    result["courses"] = sorted(courses_map.values(), key=lambda c: c["order"])
    result["aggregated_allergens"] = aggregated_allergens
    result["allergens_by_course"] = allergens_by_course
    result["allergen_notes"] = allergen_data["allergen_notes"]
    result["pairings_by_course"] = pairings_by_course
    cur.close(); conn.close()
    return jsonify(result)


@app.route("/api/menu/<slug>", methods=["PATCH"])
@requires_tier("library")
def update_menu(slug):
    user = get_current_user()
    data = request.get_json() or {}
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    if not cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    allowed = ("title", "event_date", "cover_count", "menu_price", "chef_notes")
    updates = {k: data[k] for k in allowed if k in data}
    allergen_notes_patch = data.get("allergen_notes")

    if not updates and allergen_notes_patch is None:
        cur.close(); conn.close()
        return jsonify({"error": "No valid fields to update"}), 400

    if allergen_notes_patch is not None and isinstance(allergen_notes_patch, dict):
        # Build a merge patch: remove keys with empty-string values, merge the rest
        to_merge = {}
        to_delete_keys = []
        for k, v in allergen_notes_patch.items():
            if v == "":
                to_delete_keys.append(k)
            else:
                to_merge[k] = v
        if to_merge:
            cur.execute(
                "UPDATE menus SET allergen_notes = COALESCE(allergen_notes, '{}'::jsonb) || %s::jsonb, "
                "updated_at = NOW() WHERE slug = %s AND owner_user_id = %s",
                (json.dumps(to_merge), slug, user["id"]),
            )
        for k in to_delete_keys:
            cur.execute(
                "UPDATE menus SET allergen_notes = allergen_notes - %s, "
                "updated_at = NOW() WHERE slug = %s AND owner_user_id = %s",
                (k, slug, user["id"]),
            )

    if updates:
        set_parts = ", ".join(f"{k} = %s" for k in updates)
        vals = list(updates.values()) + [slug, user["id"]]
        cur.execute(
            f"UPDATE menus SET {set_parts}, updated_at = NOW() "
            f"WHERE slug = %s AND owner_user_id = %s",
            vals
        )

    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(_menu_to_dict(row))


@app.route("/api/menu/<slug>", methods=["DELETE"])
@requires_tier("library")
def delete_menu(slug):
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    if not cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("DELETE FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    cur.close(); conn.close()
    return '', 204


@app.route("/api/menu/<slug>/cost")
@requires_tier("profession")
def get_menu_cost(slug):
    user = get_current_user()
    region = get_user_location() or "CA"
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    covers = int(menu["cover_count"] or 1)
    menu_price = menu.get("menu_price")
    cost = _compute_menu_cost(str(menu["id"]), covers, menu_price, user["id"], region, cur)
    cur.close(); conn.close()
    return jsonify(cost)


@app.route("/api/menu/<slug>/recipes", methods=["POST"])
@requires_tier("library")
def add_menu_recipe(slug):
    user = get_current_user()
    data = request.get_json() or {}
    recipe_ref = (data.get("recipe_ref") or "").strip()
    course_name = (data.get("course_name") or "").strip()
    course_order = data.get("course_order")
    if not recipe_ref or not course_name or course_order is None:
        return jsonify({"error": "recipe_ref, course_name, and course_order are required"}), 400
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    try:
        recipe = _resolve_recipe_ref(recipe_ref, user["id"], cur)
    except ValueError as e:
        cur.close(); conn.close()
        return jsonify({"error": str(e)}), 400
    if recipe is None:
        cur.close(); conn.close()
        return jsonify({"error": "Recipe not found"}), 404

    # ── Allergen cache: detect on first add, skip if already cached ──────────
    if recipe.get("allergens") is None:
        allergen_cache = _detect_allergens_for_recipe(recipe)
        cache_json = json.dumps(allergen_cache)
        prefix = recipe_ref.split(":")[0]
        try:
            if prefix == "canon":
                cur.execute(
                    "UPDATE recipes SET allergens = %s::jsonb WHERE slug = %s",
                    (cache_json, recipe_ref.split(":", 1)[1]),
                )
            elif prefix == "kitchen":
                cur.execute(
                    "UPDATE user_kitchen_recipes SET allergens = %s::jsonb WHERE uuid = %s",
                    (cache_json, recipe_ref.split(":", 1)[1]),
                )
            recipe = dict(recipe)
            recipe["allergens"] = allergen_cache
        except Exception as exc:
            app.logger.warning(f"Allergen cache write failed for {recipe_ref}: {exc}")

    cur.execute("""
        INSERT INTO menu_recipes (menu_id, recipe_ref, course_name, course_order, dish_order_within_course)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
    """, (menu["id"], recipe_ref, course_name, int(course_order), int(data.get("dish_order_within_course", 1))))
    mr = cur.fetchone()
    cur.execute("UPDATE menus SET updated_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()
    result = _menu_recipe_to_dict(mr)
    result["recipe"] = dict(recipe)
    result["is_raw_served"] = _is_raw_served(recipe)
    return jsonify(result), 201


@app.route("/api/menu/<slug>/recipes/<menu_recipe_id>", methods=["PATCH"])
@requires_tier("library")
def update_menu_recipe(slug, menu_recipe_id):
    user = get_current_user()
    data = request.get_json() or {}
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("SELECT id FROM menu_recipes WHERE id = %s AND menu_id = %s", (menu_recipe_id, menu["id"]))
    if not cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    allowed = ("course_name", "course_order", "dish_order_within_course")
    updates = {k: data[k] for k in allowed if k in data}
    if not updates:
        cur.close(); conn.close()
        return jsonify({"error": "No valid fields to update"}), 400
    set_parts = ", ".join(f"{k} = %s" for k in updates)
    vals = list(updates.values()) + [menu_recipe_id, str(menu["id"])]
    cur.execute(
        f"UPDATE menu_recipes SET {set_parts} WHERE id = %s AND menu_id = %s RETURNING *",
        vals
    )
    mr = cur.fetchone()
    cur.execute("UPDATE menus SET updated_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()
    return jsonify(_menu_recipe_to_dict(mr))


@app.route("/api/menu/<slug>/recipes/<menu_recipe_id>", methods=["DELETE"])
@requires_tier("library")
def delete_menu_recipe(slug, menu_recipe_id):
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id FROM menus WHERE slug = %s AND owner_user_id = %s", (slug, user["id"]))
    menu = cur.fetchone()
    if not menu:
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("SELECT id FROM menu_recipes WHERE id = %s AND menu_id = %s", (menu_recipe_id, menu["id"]))
    if not cur.fetchone():
        cur.close(); conn.close()
        return jsonify({"error": "Not found"}), 404
    cur.execute("DELETE FROM menu_recipes WHERE id = %s", (menu_recipe_id,))
    cur.execute("UPDATE menus SET updated_at = NOW() WHERE id = %s", (menu["id"],))
    cur.close(); conn.close()
    return '', 204


# ─── OPT3 Canon routes ───────────────────────────────────────────────────────

SPINE_STYLES = {
    'japanese':  {'ca': '#1B2848', 'cb': '#0F1730', 'title': '#D8BC7A', 'foil': '#D8BC7A', 'bespoke': True,  'font': "'Shippori Mincho', serif",   'weight': 600},
    'italian':   {'ca': '#6E2B22', 'cb': '#3A1410', 'title': '#E8D6AE',                                       'font': "'Cormorant', serif",          'weight': 600, 'transform': 'uppercase', 'ls': '3px'},
    'french':    {'ca': '#5A2230', 'cb': '#371018', 'title': '#D8BC7A', 'foil': '#D8BC7A', 'bespoke': True,  'font': "'Playfair Display', serif",   'weight': 600, 'italic': True},
    'chinese':   {'ca': '#9A2A1E', 'cb': '#4A1108', 'title': '#F0C652',                                       'font': "'Zilla Slab', serif",         'weight': 600, 'transform': 'uppercase', 'ls': '1.5px'},
    'indian':    {'ca': '#B5641A', 'cb': '#6E3608', 'title': '#FBE7C2',                                       'font': "'Rozha One', serif",          'weight': 400},
    'thai':      {'ca': '#186A5A', 'cb': '#0C3A30', 'title': '#F2C84B',                                       'font': "'Kanit', sans-serif",         'weight': 600, 'transform': 'uppercase', 'ls': '2px'},
    'korean':    {'ca': '#DCD8CC', 'cb': '#C6C0AE', 'title': '#2A6E72', 'light': True, 'accent': '#2A6E72',  'font': "'Nanum Myeongjo', serif",     'weight': 700},
    'levantine': {'ca': '#5A5320', 'cb': '#332E10', 'title': '#E3C982',                                       'font': "'Amiri', serif",              'weight': 700},
    'turkish':   {'ca': '#16585F', 'cb': '#0A3036', 'title': '#D98A4E',                                       'font': "'Amiri', serif",              'weight': 700},
}


@app.route("/library")
def library():
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Published canons — the live shelf
    cur.execute("""
        SELECT slug, name, design_palette, entry_count
        FROM canons
        WHERE status = 'published'
        ORDER BY entry_count DESC NULLS LAST, name
    """)
    canon_rows = [_serialize_row(r) for r in cur.fetchall()]

    # Ghost canons: top 3 non-published (exclude meta-canons), prepend pinned Pacific Northwest
    cur.execute("""
        SELECT c.slug, c.name,
               COUNT(tr.id) AS entry_count
        FROM canons c
        LEFT JOIN technique_references tr ON tr.canon_slug = c.slug
        WHERE c.status != 'published'
          AND c.slug NOT IN ('general', 'provenance-1000')
        GROUP BY c.slug, c.name
        ORDER BY COUNT(tr.id) DESC NULLS LAST, c.name
        LIMIT 3
    """)
    ghost_rows = [{'slug': 'pacific-northwest', 'name': 'Pacific Northwest', 'entry_count': 0}] + \
                 [_serialize_row(r) for r in cur.fetchall()]

    cur.close()
    conn.close()

    jitter = [6, -7, 11, -3, 8, -10, 4, -5, 9, -6]

    def build_spine(row, i, is_ghost=False):
        slug  = row.get('slug', '')
        count = row.get('entry_count') or 0
        palette = row.get('design_palette') or {}

        if is_ghost:
            height_px = 258 + ((i * 41) % 40)
            width_px  = 52  + ((i * 23) % 16)
        else:
            height_px = 252 + min(166, round(count / 22)) + jitter[i % 10]
            width_px  = round(46 + min(46, count / 55))

        font_size = max(12.5, min(18.5, width_px * 0.23))

        if is_ghost:
            ca             = '#2a2820'
            cb             = '#1a1610'
            title_color    = 'rgba(231,207,148,0.45)'
            mark_color     = title_color
            font_family    = "'Cormorant', serif"
            font_weight    = 600
            font_style     = 'normal'
            text_transform = 'none'
            letter_spacing = '0.4px'
            bespoke        = False
            foil           = None
            edge           = cb
            cloth_weave    = 'rgba(0,0,0,0.12)'
            href           = None
            foot           = 'Soon'
            light          = False
        else:
            st             = SPINE_STYLES.get(slug, {})
            light          = st.get('light', False)
            ca             = st.get('ca') or palette.get('cloth_a', '#3b3330')
            cb             = st.get('cb') or palette.get('cloth_b', '#241f1b')
            title_color    = st.get('title', '#E7CF94')
            foil           = st.get('foil')
            bespoke        = st.get('bespoke', False)
            font_family    = st.get('font', "'Cormorant', serif")
            font_weight    = st.get('weight', 600)
            font_style     = 'italic' if st.get('italic') else 'normal'
            text_transform = st.get('transform', 'none')
            letter_spacing = st.get('ls', '0.4px')
            mark_color     = foil or title_color
            cloth_weave    = 'rgba(0,0,0,0.045)' if light else 'rgba(0,0,0,0.12)'
            edge           = st.get('accent', '#9A7B3F') if light else cb
            href           = f"/canon/{slug}/"
            foot           = f"{count:,}" if count else '—'
            if light:
                ca, cb = '#EFE8D8', '#D8CFB9'

        cloth_bg = (
            f"repeating-linear-gradient(0deg,{cloth_weave} 0 1px,transparent 1px 3px),"
            f"linear-gradient(165deg,{ca},{cb})"
        )

        return {
            'name':           row.get('name', ''),
            'slug':           slug,
            'href':           href,
            'height_px':      height_px,
            'width_px':       width_px,
            'font_size':      round(font_size, 2),
            'cloth_bg':       cloth_bg,
            'edge':           edge,
            'title_color':    title_color,
            'mark_color':     mark_color,
            'font_family':    font_family,
            'font_weight':    font_weight,
            'font_style':     font_style,
            'text_transform': text_transform,
            'letter_spacing': letter_spacing,
            'bespoke':        bespoke,
            'foil':           foil,
            'foot':           foot,
            'is_ghost':       is_ghost,
            'light':          light,
        }

    spines = [build_spine(r, i, False) for i, r in enumerate(canon_rows)]
    ghosts = [build_spine(r, i, True)  for i, r in enumerate(ghost_rows)]

    # Trade-tier ribbon marks: highlight spines with a saved reading position
    _uid_lib = session.get("user_id")
    _user_lib = get_current_user() if _uid_lib else None
    if _user_lib and _user_lib.get('subscription_tier') == 'trade' and DATABASE_URL:
        try:
            _rconn = get_db()
            _rcur = _rconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            _rcur.execute("SELECT canon_slug FROM reading_ribbons WHERE user_id=%s", (_uid_lib,))
            _ribbon_slugs = {r['canon_slug'] for r in _rcur.fetchall()}
            _rcur.close(); _rconn.close()
            for s in spines:
                s['ribbon_mark'] = s['slug'] in _ribbon_slugs
        except Exception:
            pass

    _words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
              7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve'}
    published_count = _words.get(len(spines), str(len(spines)))

    return render_template(
        "library.html",
        canons=canon_rows,           # backwards compat
        spines=spines,
        ghosts=ghosts,
        published_count=published_count,
    )


@app.route("/api/canon/<canon_slug>/search")
def api_canon_search(canon_slug):
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])
    if not DATABASE_URL:
        return jsonify([]), 503
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT tr.name, tr.slug, tr.section_slug,
              cs.name AS chapter_name,
              ((CASE WHEN tr.origin IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN tr.description IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN tr.flavour_context IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN tr.quality_hierarchy IS NOT NULL THEN 1 ELSE 0 END) >= 2
               OR tr.recipe_card IS NOT NULL) AS is_full
            FROM technique_references tr
            LEFT JOIN canon_sections cs ON cs.canon_slug = tr.canon_slug
              AND cs.section_slug = tr.section_slug
            WHERE tr.canon_slug = %s
              AND tr.published IS NOT FALSE
              AND tr.name ILIKE %s
            ORDER BY tr.name
            LIMIT 24
        """, (canon_slug, f'%{q}%'))
        rows = cur.fetchall()
        cur.close(); conn.close()
        chapters = {}
        chapter_order = []
        for r in rows:
            ch = r['chapter_name'] or r['section_slug'] or 'General'
            if ch not in chapters:
                chapters[ch] = []
                chapter_order.append(ch)
            chapters[ch].append({
                'name': r['name'],
                'slug': r['slug'],
                'thin': not bool(r['is_full']),
                'chapter': ch,
            })
        return jsonify([{'chapter': ch, 'entries': chapters[ch]} for ch in chapter_order])
    except Exception as e:
        app.logger.error(f"[canon_search] {canon_slug}: {e}")
        return jsonify([]), 500


@app.route("/canons-v2/")
def canons_index():
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT slug, name, description, entry_count, status, display_order
        FROM canons
        WHERE status != 'archived'
        ORDER BY display_order, name
    """)
    canons = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("canons_index.html", canons=canons)


_SECTION_DOCTRINE = {
    'the-method':                    'The foundational moves that define the cuisine.',
    'the-canonical-dishes':          'The dishes every cook must know cold.',
    'overview-cultural-context':     'Where the cuisine comes from and why it matters.',
    'food-culture-and-tradition':    'The rituals and values that shape how this food is made.',
    'ingredients-and-procurement':   'What to buy, where to find it, and why quality matters.',
    'ingredient-knowledge':          'The raw materials that make the cuisine.',
    'techniques':                    'Technique as the foundation of understanding.',
    'preparation':                   'The core preparation methods.',
    'regional-cuisine':              'The regional variations and local distinctions.',
    'pastry-technique':              'The sweet discipline and its standards.',
    'charcuterie-curing':            'Preservation and transformation through salt and time.',
    'wet-heat':                      'Braise, steam, poach — water as the medium.',
    'grains-and-dough':              'Bread, pasta, rice — the backbone of the canon.',
    'the-canonical-recipes':         'The canon condensed to its most essential recipes.',
    'general':                       'General techniques and shared principles.',
}


@app.route("/canon/<canon_slug>/")
def canon_book(canon_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM canons WHERE slug = %s", (canon_slug,))
    canon = cur.fetchone()
    if not canon:
        cur.close()
        conn.close()
        abort(404)
    canon = _serialize_row(canon)
    # Per-section real counts + full-depth counts
    cur.execute("""
        SELECT cs.section_slug, cs.name, cs.description, cs.display_order,
               COUNT(tr.id) AS real_count,
               SUM(CASE WHEN (
                 (CASE WHEN tr.origin IS NOT NULL THEN 1 ELSE 0 END) +
                 (CASE WHEN tr.description IS NOT NULL THEN 1 ELSE 0 END) +
                 (CASE WHEN tr.flavour_context IS NOT NULL THEN 1 ELSE 0 END) +
                 (CASE WHEN tr.quality_hierarchy IS NOT NULL THEN 1 ELSE 0 END)
               ) >= 2 OR tr.recipe_card IS NOT NULL THEN 1 ELSE 0 END) AS full_count
        FROM canon_sections cs
        LEFT JOIN technique_references tr
          ON tr.canon_slug = cs.canon_slug
          AND tr.section_slug = cs.section_slug
          AND tr.published IS NOT FALSE
        WHERE cs.canon_slug = %s
        GROUP BY cs.section_slug, cs.name, cs.description, cs.display_order
        ORDER BY cs.display_order, cs.section_slug
    """, (canon_slug,))
    sections = []
    for r in cur.fetchall():
        s = _serialize_row(r)
        s['real_count'] = int(s.get('real_count') or 0)
        s['full_count'] = int(s.get('full_count') or 0)
        # Resolve description: DB value → doctrine fallback → empty
        raw_desc = s.get('description')
        if not raw_desc or str(raw_desc).strip() in ('', 'None'):
            raw_desc = _SECTION_DOCTRINE.get(s['section_slug'], '')
        s['display_desc'] = raw_desc or ''
        sections.append(s)
    # Up to 3 highlight entries per section (highest pillar_completeness)
    cur.execute("""
        SELECT slug, name, section_slug FROM (
          SELECT slug, name, section_slug,
                 ROW_NUMBER() OVER (
                   PARTITION BY section_slug
                   ORDER BY (pillar_completeness->>'count')::int DESC NULLS LAST, name
                 ) AS rn
          FROM technique_references
          WHERE canon_slug = %s AND published IS NOT FALSE
            AND pillar_completeness IS NOT NULL
        ) sub WHERE rn <= 3
    """, (canon_slug,))
    highlights = {}
    for r in cur.fetchall():
        sec = r['section_slug']
        highlights.setdefault(sec, []).append({'slug': r['slug'], 'name': r['name']})
    cur.execute("""
        SELECT id, name, slug, cuisine, recipe_type, description, image_url
        FROM recipes
        WHERE cuisine_canon = %s
        ORDER BY is_curated DESC, recipe_type, name
    """, (canon_slug,))
    recipes = [_serialize_row(r) for r in cur.fetchall()]
    palette = canon.get("design_palette") or {}
    ribbon = None
    try:
        _uid = session.get("user_id")
        if _uid:
            cur.execute("SELECT entry_slug, entry_name FROM reading_ribbons WHERE user_id=%s AND canon_slug=%s", (_uid, canon_slug))
            _r = cur.fetchone()
            if _r:
                ribbon = {'entry_slug': _r['entry_slug'], 'entry_name': _r['entry_name']}
    except Exception:
        pass
    cur.close()
    conn.close()
    return render_template("canon_book.html", canon=canon, sections=sections, recipes=recipes,
                           palette=palette, book_mode=True, highlights=highlights, ribbon=ribbon)


REGION_LABELS = {
    # French regions
    'classical':             'The Classical Repertoire',
    'provence':              'Provence',
    'burgundy':              'Burgundy',
    'lyonnais':              'Lyonnais',
    'alsace':                'Alsace',
    'normandy':              'Normandy',
    'brittany':              'Brittany',
    'southwest':             'The Southwest',
    'bordelais':             'Bordelais',
    'languedoc-roussillon':  'Languedoc-Roussillon',
    'savoy':                 'Savoy',
    'auvergne':              'Auvergne',
    'lorraine':              'Lorraine',
    'nord':                  'The North',
    'loire':                 'Loire',
    'champagne':             'Champagne',
    'jura-franche-comte':    'Jura & Franche-Comté',
    'dauphine':              'Dauphiné',
    # Italian regions
    'piedmont':              'Piedmont',
    'aosta-valley':          'Aosta Valley',
    'lombardy':              'Lombardy',
    'trentino-alto-adige':   'Trentino-Alto Adige',
    'veneto':                'Veneto',
    'friuli-venezia-giulia': 'Friuli-Venezia Giulia',
    'liguria':               'Liguria',
    'emilia-romagna':        'Emilia-Romagna',
    'tuscany':               'Tuscany',
    'marche':                'Marche',
    'umbria':                'Umbria',
    'lazio':                 'Lazio',
    'abruzzo':               'Abruzzo',
    'molise':                'Molise',
    'campania':              'Campania',
    'puglia':                'Puglia',
    'basilicata':            'Basilicata',
    'calabria':              'Calabria',
    'sicily':                'Sicily',
    'sardinia':              'Sardinia',
    'pan-italian':           'The Italian Foundation',
    # Japanese disciplines (interior cut for The Method + The Canonical Dishes)
    'dashi-stock':           'Dashi & Stock',
    'rice':                  'Rice',
    'hocho-knife':           'Hōchō — Knife Discipline',
    'koji-fermentation':     'Koji & Fermentation',
    'tempura-agemono':       'Tempura / Agemono',
    'yakimono':              'Yakimono',
    'nimono-mushimono':      'Nimono & Mushimono',
    'kaiseki':               'Kaiseki',
    'sushi':                 'Sushi',
    'ramen-noodle':          'Ramen & Noodle',
    'wagashi':               'Wagashi & Confectionery',
    # Shared
    'other-regional':        'Other Regions',
}

_REGION_ORDER = {
    # Italian regions (north → south)
    'aosta-valley': 1, 'piedmont': 2, 'lombardy': 3, 'trentino-alto-adige': 4,
    'veneto': 5, 'friuli-venezia-giulia': 6, 'liguria': 7, 'emilia-romagna': 8,
    'tuscany': 9, 'marche': 10, 'umbria': 11, 'lazio': 12, 'abruzzo': 13,
    'molise': 14, 'campania': 15, 'puglia': 16, 'basilicata': 17, 'calabria': 18,
    'sicily': 19, 'sardinia': 20,
    # Japanese disciplines (method 31-37, canonical dishes 41-44)
    'dashi-stock': 31, 'rice': 32, 'hocho-knife': 33, 'koji-fermentation': 34,
    'tempura-agemono': 35, 'yakimono': 36, 'nimono-mushimono': 37,
    'kaiseki': 41, 'sushi': 42, 'ramen-noodle': 43, 'wagashi': 44,
}

_BEV_TOP_BY_CANON = {
    'french': [
        (104, 'Burgundy'), (121, 'Bordeaux'), (131, 'Rhône Valley'),
        (147, 'Loire Valley'), (143, 'Champagne'), (155, 'Alsace'),
        (288, 'Beaujolais'), (283, 'Languedoc'), (289, 'Roussillon'),
        (159, 'Provence'), (250, 'Jura'), (333, 'Savoie'),
        (156, 'Cognac'), (157, 'Armagnac'), (158, 'Normandy'),
    ],
    'japanese': [
        (45, 'Niigata'), (46, 'Nada'), (47, 'Fushimi'), (49, 'Yamagata'),
        (55, 'Oita'), (50, 'Fukui'), (48, 'Yamaguchi'), (52, 'Shizuoka'),
        (237, 'Yamazaki — Suntory Distillery'), (238, 'Yoichi — Nikka Distillery'),
        (239, 'Miyagikyo — Nikka Distillery'), (240, "Chichibu — Ichiro's Malt"),
        (779, 'Hokkaido Wine Region'), (754, 'Yamanashi Wine Region'),
        (780, 'Nagano Wine Region'), (449, 'Yamanashi'),
        (54, 'Kagoshima Shochu'), (56, 'Okinawa'),
        (51, 'Uji'), (53, 'Kagoshima'),
    ],
    'indian': [
        (65, 'Darjeeling'), (309, 'Nashik'), (67, 'Nilgiri'), (66, 'Assam'),
        (759, 'Nashik Valley GI'), (819, 'India Nandi Hills Wine Region'),
    ],
    'chinese': [
        (60, 'Guangdong'), (57, 'Yunnan'), (58, 'Fujian'), (59, 'Zhejiang'),
        (61, 'Guizhou'), (62, 'Sichuan'),
        (508, 'Ningxia'), (825, 'Yunnan China Wine Region'),
        (777, 'Xinjiang Wine Region'), (813, 'China Shandong Wine Region'),
    ],
    'levantine': [
        (182, 'Bekaa Valley'),
        (701, 'Judean Hills'),
        (298, 'Galilee'),
        (405, 'Golan Heights'),
        (804, 'Jordan Madaba Wine Region'),
    ],
    'turkish': [
        (184, 'Turkey'),
        (760, 'Thrace'),
        (766, 'Cappadocia Wine Region'),
        (510, 'Cappadocia'),
    ],
}

_BEV_COUNTRY_BY_CANON = {
    'french':   'France',
    'japanese': 'Japan',
    'indian':   'India',
    'chinese':  'China',
    'levantine': 'Lebanon',
    'turkish':   'Turkey',
}

def _sort_regions(slugs):
    def key(s):
        if s in ('classical', 'pan-italian'): return (0, 0, '')
        if s == 'other-regional':             return (2, 0, '')
        label = REGION_LABELS.get(s, s.replace('-', ' ').title())
        return (1, _REGION_ORDER.get(s, 50), label)
    return sorted(slugs, key=key)


@app.route("/canon/<canon_slug>/index/")
def canon_index(canon_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM canons WHERE slug = %s", (canon_slug,))
    canon = cur.fetchone()
    if not canon:
        cur.close(); conn.close()
        abort(404)
    canon = _serialize_row(canon)
    palette = canon.get("design_palette") or {}
    cur.execute("""
        SELECT name, slug
        FROM technique_references
        WHERE canon_slug = %s AND slug IS NOT NULL
        ORDER BY LOWER(name)
    """, (canon_slug,))
    entries = [_serialize_row(r) for r in cur.fetchall()]
    cur.close(); conn.close()

    import unicodedata
    def _first_letter(e):
        for ch in (e.get("name") or ""):
            if ch.isalpha():
                nfd = unicodedata.normalize('NFD', ch)
                base = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn').upper()
                return base if (base and base.isascii() and base.isalpha()) else '#'
        return '#'

    grouped_dict = {}
    for entry in entries:
        letter = _first_letter(entry)
        grouped_dict.setdefault(letter, []).append(entry)
    latin_letters = sorted(l for l in grouped_dict if l != '#')
    letters = latin_letters + (['#'] if '#' in grouped_dict else [])
    grouped = [(l, grouped_dict[l]) for l in letters]
    default_letter = max(grouped_dict, key=lambda l: len(grouped_dict[l])) if grouped_dict else (letters[0] if letters else '')

    return render_template("canon_index.html",
        canon=canon, palette=palette,
        grouped=grouped, letters=letters,
        total_count=len(entries),
        default_letter=default_letter,
        book_mode=True)


@app.route("/canon/<canon_slug>/colophon/")
def canon_colophon(canon_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM canons WHERE slug = %s", (canon_slug,))
    canon = cur.fetchone()
    if not canon:
        cur.close(); conn.close()
        abort(404)
    canon = _serialize_row(canon)
    palette = canon.get("design_palette") or {}
    cur.execute("""
        SELECT COUNT(*) AS entry_count
        FROM technique_references
        WHERE canon_slug = %s AND slug IS NOT NULL
    """, (canon_slug,))
    row = cur.fetchone()
    entry_count = row["entry_count"] if row else 0
    cur.close(); conn.close()
    return render_template("canon_colophon.html",
        canon=canon, palette=palette,
        entry_count=entry_count,
        book_mode=True)


@app.route("/canon/<canon_slug>/<section_slug>/")
def canon_section(canon_slug, section_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM canons WHERE slug = %s", (canon_slug,))
    canon = cur.fetchone()
    if not canon:
        cur.close()
        conn.close()
        abort(404)
    canon = _serialize_row(canon)
    cur.execute("""
        SELECT * FROM canon_sections
        WHERE canon_slug = %s AND section_slug = %s
    """, (canon_slug, section_slug))
    section = cur.fetchone()
    if not section:
        cur.close()
        conn.close()
        abort(404)
    section = _serialize_row(section)
    palette = canon.get("design_palette") or {}

    if section_slug == 'the-pantry':
        _PANTRY_CATEGORY_LABELS = {
            'charcuterie_cured':        'Charcuterie & Cured',
            'chocolate_confection':     'Chocolate & Confection',
            'dairy_fermented':          'Dairy & Fermented',
            'flour_baking':             'Flour & Baking',
            'freeze_dried_condiment':   'Freeze-Dried & Condiment',
            'freeze_dried_herb_powder': 'Herb Powders',
            'oils_vinegars':            'Oils & Vinegars',
            'preserved_pickled':        'Preserved & Pickled',
            'produce_specialty':        'Specialty Produce',
            'rice_grains':              'Rice & Grains',
            'seafood_general':          'Seafood',
            'seafood_sashimi':          'Seafood — Sashimi Grade',
            'spices_seasonings':        'Spices & Seasonings',
            'wagyu_premium_protein':    'Wagyu & Premium Protein',
        }
        if canon_slug == 'japanese':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('japan', 'jp', 'japanese')
                       OR region_tags @> '["japanese"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        elif canon_slug == 'indian':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('india', 'in', 'indian')
                       OR region_tags @> '["indian"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        elif canon_slug == 'chinese':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('china', 'cn', 'chinese')
                       OR region_tags @> '["chinese"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        elif canon_slug == 'korean':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('korea', 'south korea', 'kr', 'korean')
                       OR region_tags @> '["korean"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        elif canon_slug == 'levantine':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('lebanon', 'syria', 'palestine', 'jordan', 'israel')
                       OR region_tags @> '["levantine"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        elif canon_slug == 'turkish':
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('turkey', 'türkiye', 'turkish')
                       OR region_tags @> '["turkish"]')
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        else:
            cur.execute("""
                SELECT id, canonical_name, category, origin_country, origin_brand
                FROM ingredient_master
                WHERE (lower(origin_country) IN ('france', 'fr', 'french')
                       OR region_tags @> '["french"]')
                  AND category != 'wagyu_premium_protein'
                  AND is_active = true
                ORDER BY category, canonical_name
            """)
        rows = [_serialize_row(r) for r in cur.fetchall()]
        from collections import defaultdict as _defaultdict
        _grouped = _defaultdict(list)
        for row in rows:
            _grouped[row['category']].append(row)
        categories = [
            {
                'slug': cat,
                'label': _PANTRY_CATEGORY_LABELS.get(cat, cat.replace('_', ' ').title()),
                'ingredients': _grouped[cat],
            }
            for cat in sorted(_grouped.keys())
        ]
        cur.close()
        conn.close()
        return render_template("canon_pantry.html",
            canon=canon, section=section, categories=categories, palette=palette, book_mode=True)

    if section_slug == 'the-beverage-tradition':
        bev_top = _BEV_TOP_BY_CANON.get(canon_slug, [])
        bev_country = _BEV_COUNTRY_BY_CANON.get(canon_slug, 'France')
        top_ids = [r[0] for r in bev_top]
        cur.execute("""
            WITH RECURSIVE subtree AS (
                SELECT id, id AS top_id FROM beverage_regions WHERE id = ANY(%s)
                UNION ALL
                SELECT r.id, s.top_id FROM beverage_regions r
                JOIN subtree s ON r.parent_region_id = s.id
            )
            SELECT s.top_id, COUNT(DISTINCT bp.id) AS n
            FROM subtree s
            LEFT JOIN beverage_producers bp ON bp.region_id = s.id
              AND bp.is_published = true AND bp.country = %s
            GROUP BY s.top_id
        """, (top_ids, bev_country))
        counts = {row['top_id']: row['n'] for row in cur.fetchall()}
        bev_regions = [
            {'region_id': rid, 'label': name, 'producer_count': counts.get(rid, 0)}
            for rid, name in bev_top
            if counts.get(rid, 0) > 0
        ]
        cur.close()
        conn.close()
        return render_template("canon_beverage.html",
            canon=canon, section=section, bev_regions=bev_regions, palette=palette, book_mode=True)

    cur.execute("""
        SELECT id, name, slug, entry_slug, decimal_id, description, origin, authority_tier,
               facets->>'region_slug' AS region_slug,
               (CASE WHEN origin IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN description IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN flavour_context IS NOT NULL THEN 1 ELSE 0 END) +
               (CASE WHEN quality_hierarchy IS NOT NULL THEN 1 ELSE 0 END) AS left_pillar_count,
               (recipe_card IS NOT NULL) AS has_recipe
        FROM technique_references
        WHERE canon_slug = %s AND section_slug = %s AND published IS NOT FALSE
        ORDER BY decimal_id, name
    """, (canon_slug, section_slug))
    entries = []
    for r in cur.fetchall():
        e = _serialize_row(r)
        e['is_full'] = (e.get('left_pillar_count') or 0) >= 2 or bool(e.get('has_recipe'))
        entries.append(e)
    section_total = len(entries)
    section_full  = sum(1 for e in entries if e['is_full'])
    region_slugs = [e["region_slug"] for e in entries if e.get("region_slug")]
    has_regions = bool(region_slugs)
    regions = []
    if has_regions:
        distinct_slugs = list(dict.fromkeys(region_slugs))
        for rs in _sort_regions(distinct_slugs):
            regions.append({"slug": rs, "label": REGION_LABELS.get(rs, rs.replace('-', ' ').title())})
    # Dictionary tabs: top-10 sections for chapter-wall fore-edge
    thumb_sections = []
    try:
        cur.execute("""
            SELECT tr.section_slug, cs.name AS section_name, COUNT(*) AS n
            FROM technique_references tr
            LEFT JOIN canon_sections cs ON cs.canon_slug = tr.canon_slug
                AND cs.section_slug = tr.section_slug
            WHERE tr.canon_slug = %s AND tr.published IS NOT FALSE
              AND tr.section_slug IS NOT NULL
            GROUP BY tr.section_slug, cs.name
            ORDER BY COUNT(*) DESC, tr.section_slug
            LIMIT 10
        """, (canon_slug,))
        thumb_sections = [{'slug': r['section_slug'], 'name': r['section_name'] or r['section_slug'].replace('-', ' ').title()} for r in cur.fetchall()]
    except Exception:
        pass
    cur.close()
    conn.close()
    return render_template("canon_section.html",
        canon=canon, section=section, entries=entries,
        palette=palette, has_regions=has_regions, regions=regions,
        section_total=section_total, section_full=section_full, book_mode=True,
        thumb_sections=thumb_sections)


@app.route("/canon/<canon_slug>/<section_slug>/<region_slug>/")
def canon_region(canon_slug, section_slug, region_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM canons WHERE slug = %s", (canon_slug,))
    canon = cur.fetchone()
    if not canon:
        cur.close()
        conn.close()
        abort(404)
    canon = _serialize_row(canon)
    cur.execute("""
        SELECT * FROM canon_sections
        WHERE canon_slug = %s AND section_slug = %s
    """, (canon_slug, section_slug))
    section = cur.fetchone()
    if not section:
        cur.close()
        conn.close()
        abort(404)
    section = _serialize_row(section)
    palette = canon.get("design_palette") or {}

    if section_slug == 'the-beverage-tradition':
        try:
            region_id = int(region_slug)
        except (ValueError, TypeError):
            cur.close()
            conn.close()
            abort(404)
        # Region display name from the curated list or DB
        _bev_labels = {rid: name for rid, name in _BEV_TOP_BY_CANON.get(canon_slug, [])}
        bev_country = _BEV_COUNTRY_BY_CANON.get(canon_slug, 'France')
        cur.execute("SELECT name FROM beverage_regions WHERE id = %s", (region_id,))
        reg_row = cur.fetchone()
        if not reg_row:
            cur.close()
            conn.close()
            abort(404)
        region_label = _bev_labels.get(region_id, reg_row['name'])
        # Recursive subtree of this region
        cur.execute("""
            WITH RECURSIVE subtree AS (
                SELECT id FROM beverage_regions WHERE id = %s
                UNION ALL
                SELECT r.id FROM beverage_regions r
                JOIN subtree s ON r.parent_region_id = s.id
            )
            SELECT bp.id, bp.name, bp.slug AS producer_slug,
                   br.name AS appellation
            FROM beverage_producers bp
            JOIN beverage_regions br ON br.id = bp.region_id
            WHERE bp.region_id IN (SELECT id FROM subtree)
              AND bp.is_published = true AND bp.country = %s
            ORDER BY br.name, bp.name
        """, (region_id, bev_country))
        producers = [_serialize_row(r) for r in cur.fetchall()]
        cur.close()
        conn.close()
        return render_template("canon_beverage_region.html",
            canon=canon, section=section, producers=producers,
            palette=palette, region_id=region_id, region_label=region_label, book_mode=True)

    cur.execute("""
        SELECT id, name, slug, entry_slug, decimal_id, description, origin, authority_tier
        FROM technique_references
        WHERE canon_slug = %s AND section_slug = %s
          AND facets->>'region_slug' = %s
        ORDER BY decimal_id, name
    """, (canon_slug, section_slug, region_slug))
    entries = [_serialize_row(r) for r in cur.fetchall()]
    region_label = REGION_LABELS.get(region_slug, region_slug.replace('-', ' ').title())
    cur.close()
    conn.close()
    return render_template("canon_region.html",
        canon=canon, section=section, entries=entries,
        palette=palette, region_slug=region_slug, region_label=region_label, book_mode=True)


@app.route("/canon/<canon_slug>/<section_slug>/<entry_slug>")
def canon_entry(canon_slug, section_slug, entry_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM technique_references
        WHERE canon_slug = %s AND section_slug = %s AND entry_slug = %s
    """, (canon_slug, section_slug, entry_slug))
    technique = cur.fetchone()
    if not technique:
        cur.close()
        conn.close()
        abort(404)
    technique = _serialize_row(technique)
    # Redirect to canonical slug-based URL preserving existing page
    cur.close()
    conn.close()
    from flask import redirect, url_for
    return redirect(url_for("technique_page", slug=technique["slug"]), code=301)


@app.route("/explorer")
def canon_explorer():
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT slug, name, entry_count, status
        FROM canons
        WHERE status != 'archived' AND entry_count > 0
        ORDER BY entry_count DESC, name
        LIMIT 50
    """)
    canons = [_serialize_row(r) for r in cur.fetchall()]
    cur.execute("""
        SELECT canon_slug, COUNT(*) as n
        FROM technique_references
        WHERE canon_slug IS NOT NULL
        GROUP BY canon_slug
        ORDER BY n DESC LIMIT 50
    """)
    canon_counts = {r["canon_slug"]: r["n"] for r in cur.fetchall()}
    cur.execute("""
        SELECT v.slug, v.name, COUNT(ve.entry_id) as count
        FROM volumes v
        LEFT JOIN volume_entries ve ON ve.volume_slug = v.slug
        WHERE v.volume_type = 'route'
        GROUP BY v.slug, v.name
        HAVING COUNT(ve.entry_id) > 0
        ORDER BY v.slug
    """)
    routes = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("explorer.html", canons=canons, canon_counts=canon_counts, routes=routes)


@app.route("/atlas/<volume_slug>")
def atlas_volume(volume_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM volumes WHERE slug = %s AND volume_type = 'atlas'", (volume_slug,))
    volume = cur.fetchone()
    if not volume:
        cur.close()
        conn.close()
        abort(404)
    volume = _serialize_row(volume)
    cur.execute("""
        SELECT ve.display_order, ve.editorial_note,
               tr.id, tr.name, tr.slug, tr.entry_slug, tr.decimal_id,
               tr.description, tr.origin, tr.canon_slug, tr.section_slug
        FROM volume_entries ve
        JOIN technique_references tr ON tr.id = ve.entry_id
        WHERE ve.volume_slug = %s
        ORDER BY ve.display_order, tr.name
    """, (volume_slug,))
    entries = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("atlas_volume.html", volume=volume, entries=entries)


_PMT_NARRATIVE = {
    "overture": {
        "eyebrow": "The Routes · A Spice Route of the Provenance Canon",
        "scene1": 'A waka comes in on a grey morning, into a harbour on the north island of a country no one has named yet. The paddlers have been at sea for weeks. In the hull, wrapped against the salt, are the things that matter most — and among them, seed tubers of <span class="lift">kūmara</span> — a sweet potato that, alone in this hull, did not travel the trail these people travelled. Children are lifted onto the sand. Someone speaks the first words said here.',
        "scene2": 'That landing is the <span class="lift">end</span> of the longest sea migration in human history. The people who paddle in trace back five thousand years and four thousand miles, to the coast of Taiwan. But the kūmara in the hull does not — it is a New World plant, carried home from South America by voyagers who reached the Americas and returned, centuries before any European crossed this ocean. To understand both, you have to go back to the start and travel the whole way down.',
        "begin": "Begin the journey",
    },
    "stops": {
        "Spine": {
            "way": "The trail itself",
            "display_name": "The Spine",
            "coord": "Austronesian expansion · pan-Pacific",
            "intro": 'One technique runs the length of this journey, almost unchanged: <span class="lift">the earth oven</span> — a pit of fire-heated stones, food laid on top, the whole thing buried to cook. It appears at every stop, from the barapen of Borneo to the lovo of Fiji, the imu of Hawaiʿi, the hāngī of Aotearoa. Every island kitchen on this trail is a variation on a single inheritance, carried in the hull of a canoe.',
        },
        "Taiwan": {
            "way": "Where the trail begins",
            "display_name": "Taiwan",
            "coord": "Origin · c. 3000 BCE",
            "intro": 'On the coast of Taiwan, a people who had mastered the outrigger canoe began to leave. They grew taro and millet, fermented rice into wine, cooked on hot stones, preserved meat in highland smoke — and they carried all of it onto the water. Everything that follows begins with what these people <span class="lift">loaded into a hull and paddled south.</span>',
        },
        "Philippines": {
            "way": "The first branching",
            "display_name": "The Philippines",
            "coord": "c. 2200 BCE · the islands fill",
            "intro": 'In the Philippine archipelago the voyagers found a thousand islands and a warmer world. The coconut entered the larder for good; the banana leaf became plate and parcel; the reef gave fish eaten raw and bright with acid. This is where the single Taiwanese kitchen <span class="lift">began to become many.</span>',
        },
        "Indonesia": {
            "way": "The crossroads",
            "display_name": "Indonesia",
            "coord": "The fermentation heart · the spice islands",
            "intro": 'Seventeen thousand islands, and the richest larder on the trail. Indonesia is where the Pacific learned to <span class="lift">ferment</span> — soybean into tempeh, rice into brem, shrimp into terasi, fish into paste and sauce. It is also where the cloves and nutmeg grew that the Austronesians had always had, and that Europe would cross the world to seize. Here the journey meets recorded history.',
        },
        "Melanesia": {
            "way": "The deep water",
            "display_name": "Melanesia",
            "coord": "Fiji · Vanuatu · the open ocean",
            "intro": 'Now the islands are scattered across true ocean, and the voyaging is a feat. In Fiji the whole grammar of the trail is visible at once: the earth oven, raw fish in coconut, taro leaf in coconut, the ceremonial root drunk at dusk. This is the Pacific kitchen <span class="lift">fully itself</span> — coconut as butter, the reef as larder, the lovo as hearth.',
        },
        "Polynesia": {
            "way": "The hub",
            "display_name": "Polynesia",
            "coord": "Tonga · Samoa · the central Pacific",
            "intro": 'Tonga and Samoa first, then the Cook Islands and Tahiti — the centre of the Polynesian world, settled and held for a thousand years. From this hub the two great founding voyages set out. Everything in Hawaiʿi and everything in Aotearoa <span class="lift">launched from here.</span>',
        },
        "Hawaii": {
            "way": "The northern reach",
            "display_name": "Hawaiʿi",
            "coord": "The fulcrum · ancient larder &amp; the melting pot",
            "intro": 'The trail’s fulcrum. First the ancient larder, carried north intact — taro pounded to poi, the imu, the fishpond, the raw reef fish. Then, far later, the plantation era, when Chinese, Japanese, Korean, Portuguese and Filipino workers met on the same islands and the trail did its oldest trick one more time: <span class="lift">it absorbed everything, and made it one plate.</span>',
        },
        "Aotearoa": {
            "way": "Journey’s end",
            "display_name": "Aotearoa",
            "coord": "New Zealand · the last landfall",
            "intro": 'The longest voyage, to the coldest country. Here taro could not grow — but the kūmara could, and it became the reason this chapter exists: a New World plant the voyagers had carried home from South America, now learning a southern winter. Every deep thread that opened in Taiwan lands on this shore — the earth oven as the hāngī, the raw fish as kaimoana, the heat-leaf as horopito, the seaweed as karengo. <span class="lift">This is where the trail comes to rest.</span>',
        },
    },
    "transforms": {
        "Taiwan": {"glyph": "≈", "text": "From the Taiwan coast the canoes crossed the strait into the islands of the Philippines. Here the larder met the tropics — coconut, banana leaf, the heat of the equator — and the cooking began to change."},
        "Philippines": {"glyph": "≈", "text": "South and west into the great archipelago of Indonesia — the crossroads of the whole dispersal, where the trail learned to ferment everything it touched, and where the spice it carried would one day pull the rest of the world in after it."},
        "Indonesia": {"glyph": "≈", "text": "Out past the last of the great islands into open Pacific — into Melanesia, the deep-water leg, where the canoes were truly oceangoing and the earth oven became the lovo."},
        "Melanesia": {"glyph": "≈", "text": "Into the heart of the ocean — Polynesia, the homeland and the hub. Here the canoe paused for a thousand years before launching its two longest voyages: north to Hawaiʿi, and south to Aotearoa."},
        "Polynesia": {"glyph": "↑", "text": "North, against the trade winds, on the longest open-ocean voyage yet attempted — two and a half thousand miles to a chain of volcanic islands no human had ever seen. Hawaiʿi."},
        "Hawaii": {"glyph": "↓", "text": "And the other voyage — south, across the equator, to the last and largest land the Polynesians ever found, and the coldest. The waka that opened this page is on the water now, a New World tuber wrapped in its hull."},
    },
    "closing": {
        "way": "The trail comes to rest",
        "text": 'The waka that opened this page comes ashore here. The kūmara is carried up the beach and planted in cold ground, and to keep it alive through the southern winter the people dig the rua kūmara — the storage pit that becomes a tradition. <span class="lift">The earth oven becomes the hāngī; the raw fish from a Taiwan reef becomes kaimoana on a southern shore; taro, the mother crop, gives way to the kūmara.</span> And the kūmara is the proof of the strangest truth on the trail: this was never a one-way line. To carry a South American plant to a New Zealand beach, the voyagers had crossed the whole ocean and come back. The journey ends where it began for us — on a grey morning, on a northern shore, with a hull full of everything that mattered.',
    },
}


@app.route("/route/<volume_slug>")
def route_volume(volume_slug):
    if not DATABASE_URL:
        return "Database not configured", 503
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM volumes WHERE slug = %s AND volume_type = 'route'", (volume_slug,))
    volume = cur.fetchone()
    if not volume:
        cur.close()
        conn.close()
        abort(404)
    volume = _serialize_row(volume)
    cur.execute("""
        SELECT ve.display_order, ve.editorial_note,
               tr.id, tr.name, tr.slug, tr.entry_slug, tr.decimal_id,
               tr.description, tr.migration_thread, tr.origin, tr.canon_slug, tr.section_slug
        FROM volume_entries ve
        JOIN technique_references tr ON tr.id = ve.entry_id
        WHERE ve.volume_slug = %s
        ORDER BY ve.display_order, tr.name
    """, (volume_slug,))
    entries = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    _STOP_ORDER = ["Spine", "Taiwan", "Philippines", "Indonesia",
                   "Melanesia", "Polynesia", "Hawaii", "Aotearoa"]
    _stop_map = {}
    for e in entries:
        label = e.get("editorial_note") or "Uncategorised"
        _stop_map.setdefault(label, []).append(e)
    stops = [{"label": s, "entries": _stop_map[s]} for s in _STOP_ORDER if s in _stop_map]
    for label, group in _stop_map.items():
        if label not in set(_STOP_ORDER):
            stops.append({"label": label, "entries": group})
    return render_template("route_volume.html", volume=volume, entries=entries, stops=stops,
                           narrative=_PMT_NARRATIVE if volume_slug == 'pacific-migration-trail' else None)


@app.route("/protocols")
def protocols():
    user = get_current_user()
    has_library = user_can_access("library")
    return render_template("protocols.html", has_library=has_library, user=user)


# Legacy: integer ID redirect → canonical slug
@app.route("/technique/<int:tid>")
def technique_by_id(tid):
    if not DATABASE_URL:
        abort(404)
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT slug FROM technique_references WHERE id = %s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        abort(404)
    return redirect(url_for("technique_page", slug=row["slug"]), code=301)


# ─── Technique–Beverage Pairings ─────────────────────────────────────────────

@app.route("/api/technique-pairings/<int:technique_id>")
def technique_beverage_pairings(technique_id):
    """
    Returns pairings from technique_beverage_pairings for a given technique,
    grouped by tier: editorial+reviewed (full gold) and partial (muted).

    Query params:
        region  ISO 3166-2 subdivision code, e.g. "BC", "OR", "CA".
                When supplied, rows whose region_filter excludes this code are omitted.
                Rows with region_filter=null are always included.
    """
    if not DATABASE_URL:
        return jsonify({"editorial": [], "partial": []}), 200

    region = request.args.get("region", "").strip().upper() or None

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Build region filter clause
    # A row is visible when:
    #   - region_filter IS NULL  (unrestricted)
    #   - OR region param not supplied
    #   - OR region_filter->'include' is empty array
    #   - OR region_filter->'include' contains the requested region code
    if region:
        region_clause = """
            AND (
                tbp.region_filter IS NULL
                OR tbp.region_filter->'include' = '[]'::jsonb
                OR tbp.region_filter->'include' ? %(region)s
            )
        """
    else:
        region_clause = "AND (tbp.region_filter IS NULL OR TRUE)"

    cur.execute(
        f"""
        SELECT
            tbp.id,
            tbp.technique_id,
            tbp.pairing_type,
            tbp.pairing_rationale,
            tbp.confidence_status,
            tbp.verification_level,
            tbp.display_order,
            tbp.source_urls,
            tbp.beverage_category,
            -- product fields
            bp.id          AS product_id,
            bp.name        AS product_name,
            bp.category    AS product_category,
            bp.subcategory AS product_subcategory,
            bp.description AS product_description,
            bp.price_tier  AS product_price_tier,
            -- producer fields
            bpr.id         AS producer_id,
            bpr.name       AS producer_name,
            bpr.country    AS producer_country,
            -- region fields
            br.id          AS region_id,
            br.name        AS region_name,
            br.country     AS region_country
        FROM technique_beverage_pairings tbp
        LEFT JOIN beverage_products  bp  ON tbp.beverage_product_id  = bp.id
             AND bp.is_published IS TRUE
        LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, tbp.beverage_producer_id) = bpr.id
             AND bpr.is_published IS TRUE
        LEFT JOIN beverage_regions   br  ON bp.region_id = br.id
        WHERE tbp.technique_id = %(technique_id)s
          AND (tbp.beverage_producer_id IS NULL OR bpr.id IS NOT NULL)
          AND (tbp.beverage_product_id IS NULL OR bp.id IS NOT NULL)
          {region_clause}
        ORDER BY
            CASE tbp.confidence_status
                WHEN 'editorial'  THEN 1
                WHEN 'reviewed'   THEN 2
                WHEN 'unverified' THEN 3
                WHEN 'partial'    THEN 3
                ELSE 4
            END,
            tbp.display_order,
            tbp.id
        """,
        {"technique_id": technique_id, "region": region},
    )
    rows = [_serialize_row(r) for r in cur.fetchall()]
    cur.close()
    conn.close()

    # Split into rendering tiers
    editorial = [r for r in rows if r["confidence_status"] in ("editorial", "reviewed")]
    # unverified: admin/staging surfaces only (spec v1.1 §6)
    if (get_current_user() or {}).get("role") in ("admin", "founder"):
        partial = [r for r in rows if r["confidence_status"] in ("partial", "unverified")]
    else:
        partial = []

    return jsonify({
        "technique_id": technique_id,
        "region_filter_applied": region,
        "editorial": editorial,
        "partial": partial,
        "total": len(rows),
    })


# ─── Admin: Technique–Beverage Pairings ──────────────────────────────────────

def _admin_guard():
    """Redirect to login if no active session."""
    if not session.get("user_id"):
        return _login_redirect()
    return None


def _admin_guard_api():
    """Return 401 JSON if no active session."""
    if not session.get("user_id"):
        return jsonify(error="Unauthorized"), 401
    return None


# Route 1 — Dashboard
@app.route("/admin/technique-pairings/")
def admin_tbp_dashboard():
    g = _admin_guard()
    if g:
        return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT confidence_status, COUNT(*) AS n
        FROM technique_beverage_pairings
        GROUP BY confidence_status
    """)
    stats = {r["confidence_status"]: r["n"] for r in cur.fetchall()}

    cur.execute("""
        SELECT COUNT(*) AS n FROM technique_beverage_pairings_staging
        WHERE review_status = 'pending'
    """)
    staging_pending = cur.fetchone()["n"]

    cur.execute("""
        SELECT tr.id, tr.name, tr.slug, tr.canon_slug,
               COUNT(tbp.id) AS total,
               SUM(CASE WHEN tbp.confidence_status IN ('editorial','reviewed') THEN 1 ELSE 0 END) AS n_editorial,
               SUM(CASE WHEN tbp.confidence_status = 'partial' THEN 1 ELSE 0 END) AS n_partial
        FROM technique_references tr
        JOIN technique_beverage_pairings tbp ON tbp.technique_id = tr.id
        GROUP BY tr.id, tr.name, tr.slug, tr.canon_slug
        ORDER BY tr.canon_slug, tr.name
    """)
    techniques = cur.fetchall()
    canons = sorted({t["canon_slug"] for t in techniques})
    cur.close()

    return render_template("admin_tbp_dashboard.html",
        stats=stats,
        staging_pending=staging_pending,
        techniques=techniques,
        canons=canons,
    )


# Route 2 — Per-technique review
@app.route("/admin/technique-pairings/technique/<int:technique_id>")
def admin_tbp_technique(technique_id):
    g = _admin_guard()
    if g:
        return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT id, name, slug, canon_slug, origin FROM technique_references WHERE id = %s",
        (technique_id,),
    )
    technique = cur.fetchone()
    if not technique:
        cur.close()
        return "Technique not found", 404

    cur.execute("""
        SELECT tbp.id, tbp.pairing_type, tbp.pairing_rationale,
               tbp.confidence_status, tbp.verification_level,
               tbp.display_order, tbp.beverage_category,
               bp.id AS product_id, bp.name AS product_name, bp.slug AS product_slug,
               bp.subcategory AS product_subcategory,
               bpr.id AS producer_id, bpr.name AS producer_name,
               br.name AS region_name, br.country
        FROM technique_beverage_pairings tbp
        LEFT JOIN beverage_products  bp  ON tbp.beverage_product_id = bp.id
        LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, tbp.beverage_producer_id) = bpr.id
        LEFT JOIN beverage_regions   br  ON bp.region_id = br.id
        WHERE tbp.technique_id = %s
        ORDER BY
            CASE tbp.confidence_status
                WHEN 'editorial'  THEN 1
                WHEN 'reviewed'   THEN 2
                WHEN 'unverified' THEN 3
                WHEN 'partial'    THEN 3
                ELSE 4
            END,
            tbp.display_order, tbp.id
    """, (technique_id,))
    pairings = cur.fetchall()

    cur.execute("""
        SELECT s.id, s.pairing_type, s.pairing_rationale, s.source_urls,
               s.review_status, s.batch_id, s.generated_at,
               bp.name AS product_name, bpr.name AS producer_name
        FROM technique_beverage_pairings_staging s
        LEFT JOIN beverage_products  bp  ON s.beverage_product_id = bp.id
        LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, s.beverage_producer_id) = bpr.id
        WHERE s.technique_id = %s AND s.review_status = 'pending'
        ORDER BY s.generated_at DESC
    """, (technique_id,))
    staging = cur.fetchall()
    cur.close()

    return render_template("admin_tbp_technique.html",
        technique=technique,
        pairings=pairings,
        staging=staging,
    )


# Route 3 — AJAX: update a single pairing
@app.route("/admin/technique-pairings/pairing/<int:pairing_id>/update", methods=["POST"])
def admin_tbp_pairing_update(pairing_id):
    g = _admin_guard_api()
    if g:
        return g
    data = request.get_json(silent=True) or {}

    VALID_CONFIDENCE = ("partial", "reviewed", "editorial")
    VALID_TYPE = ("signature", "regional", "alternative", "contrast")

    sets, params = [], []
    if data.get("confidence_status") in VALID_CONFIDENCE:
        sets += ["confidence_status = %s", "verification_level = %s"]
        params += [
            data["confidence_status"],
            {"partial": "auto", "reviewed": "manual", "editorial": "editorial"}[data["confidence_status"]],
        ]
    if data.get("pairing_type") in VALID_TYPE:
        sets.append("pairing_type = %s")
        params.append(data["pairing_type"])
    if "pairing_rationale" in data:
        sets.append("pairing_rationale = %s")
        params.append(str(data["pairing_rationale"])[:1000])
    if "display_order" in data:
        try:
            sets.append("display_order = %s")
            params.append(int(data["display_order"]))
        except (TypeError, ValueError):
            pass
    if not sets:
        return jsonify(error="No valid fields"), 400

    sets.append("updated_at = NOW()")
    params.append(pairing_id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(f"UPDATE technique_beverage_pairings SET {', '.join(sets)} WHERE id = %s", params)
    cur.close()
    return jsonify(ok=True)


# Route 4 — AJAX: delete a pairing
@app.route("/admin/technique-pairings/pairing/<int:pairing_id>/delete", methods=["POST"])
def admin_tbp_pairing_delete(pairing_id):
    g = _admin_guard_api()
    if g:
        return g
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM technique_beverage_pairings WHERE id = %s", (pairing_id,))
    deleted = cur.rowcount
    cur.close()
    return jsonify(ok=True, deleted=deleted)


# Route 5 — AJAX: bulk-tag (preview then apply)
@app.route("/admin/technique-pairings/technique/<int:technique_id>/bulk", methods=["POST"])
def admin_tbp_bulk(technique_id):
    g = _admin_guard_api()
    if g:
        return g
    data = request.get_json(silent=True) or {}
    ids = [int(i) for i in data.get("ids", []) if str(i).isdigit()]
    action = data.get("action", "preview")
    new_confidence = data.get("confidence_status", "")
    new_type = data.get("pairing_type", "")

    VALID_CONFIDENCE = ("partial", "reviewed", "editorial")
    VALID_TYPE = ("signature", "regional", "alternative", "contrast")

    if not ids:
        return jsonify(error="No IDs"), 400
    if new_confidence and new_confidence not in VALID_CONFIDENCE:
        return jsonify(error="Invalid confidence_status"), 400
    if new_type and new_type not in VALID_TYPE:
        return jsonify(error="Invalid pairing_type"), 400
    if not new_confidence and not new_type:
        return jsonify(error="Specify confidence_status or pairing_type"), 400

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    ph = ",".join(["%s"] * len(ids))

    cur.execute(
        f"""SELECT tbp.id, tbp.confidence_status, tbp.pairing_type,
                   bp.name AS product_name, bpr.name AS producer_name
            FROM technique_beverage_pairings tbp
            LEFT JOIN beverage_products  bp  ON tbp.beverage_product_id = bp.id
            LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, tbp.beverage_producer_id) = bpr.id
            WHERE tbp.id IN ({ph}) AND tbp.technique_id = %s""",
        ids + [technique_id],
    )
    items = cur.fetchall()

    if action == "preview":
        cur.close()
        return jsonify(
            count=len(items),
            new_confidence=new_confidence or None,
            new_type=new_type or None,
            items=[{
                "id": r["id"],
                "product_name": r["product_name"],
                "producer_name": r["producer_name"],
                "current_confidence": r["confidence_status"],
                "current_type": r["pairing_type"],
            } for r in items],
        )

    sets, params = [], []
    if new_confidence:
        vl = {"partial": "auto", "reviewed": "manual", "editorial": "editorial"}[new_confidence]
        sets += ["confidence_status = %s", "verification_level = %s"]
        params += [new_confidence, vl]
    if new_type:
        sets.append("pairing_type = %s")
        params.append(new_type)
    sets.append("updated_at = NOW()")

    cur2 = conn.cursor()
    cur2.execute(
        f"UPDATE technique_beverage_pairings SET {', '.join(sets)} WHERE id IN ({ph}) AND technique_id = %s",
        params + ids + [technique_id],
    )
    updated = cur2.rowcount
    cur.close()
    cur2.close()
    return jsonify(ok=True, updated=updated)


# Route 6 — Staging queue
@app.route("/admin/technique-pairings/staging")
def admin_tbp_staging():
    g = _admin_guard()
    if g:
        return g
    batch_filter  = request.args.get("batch", "").strip()
    status_filter = request.args.get("status", "pending").strip()

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT DISTINCT batch_id FROM technique_beverage_pairings_staging ORDER BY batch_id DESC"
    )
    batches = [r["batch_id"] for r in cur.fetchall()]

    where, params = [], []
    if status_filter:
        where.append("s.review_status = %s")
        params.append(status_filter)
    if batch_filter:
        where.append("s.batch_id = %s")
        params.append(batch_filter)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    cur.execute(f"""
        SELECT s.id, s.technique_id, s.pairing_type, s.pairing_rationale,
               s.source_urls, s.review_status, s.batch_id, s.generated_at,
               tr.name AS technique_name, tr.slug AS technique_slug,
               bp.id  AS product_id,  bp.name  AS product_name,  bp.slug AS product_slug,
               bpr.id AS producer_id, bpr.name AS producer_name,
               br.name AS region_name
        FROM technique_beverage_pairings_staging s
        JOIN  technique_references tr  ON s.technique_id = tr.id
        LEFT JOIN beverage_products  bp  ON s.beverage_product_id = bp.id
        LEFT JOIN beverage_producers bpr ON COALESCE(bp.producer_id, s.beverage_producer_id) = bpr.id
        LEFT JOIN beverage_regions   br  ON bp.region_id = br.id
        {where_sql}
        ORDER BY s.generated_at DESC, s.id
        LIMIT 300
    """, params)
    items = cur.fetchall()
    cur.close()

    return render_template("admin_tbp_staging.html",
        items=items,
        batches=batches,
        batch_filter=batch_filter,
        status_filter=status_filter,
    )


# Route 7 — AJAX: staging decide (promote / reject / edit+promote)
@app.route("/admin/technique-pairings/staging/<int:staging_id>/decide", methods=["POST"])
def admin_tbp_staging_decide(staging_id):
    g = _admin_guard_api()
    if g:
        return g
    data   = request.get_json(silent=True) or {}
    action = data.get("action", "")
    if action not in ("approve", "reject", "edit_approve"):
        return jsonify(error="Invalid action"), 400

    conn = get_db()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM technique_beverage_pairings_staging WHERE id = %s", (staging_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return jsonify(error="Not found"), 404

    if action == "reject":
        cur.execute(
            "UPDATE technique_beverage_pairings_staging SET review_status='rejected', reviewed_at=NOW(), reviewer_notes=%s WHERE id=%s",
            (data.get("notes", ""), staging_id),
        )
        cur.close()
        return jsonify(ok=True, action="rejected")

    # approve or edit_approve — promote to primary
    VALID_TYPE = ("signature", "regional", "alternative", "contrast")
    pairing_type = data.get("pairing_type", row["pairing_type"])
    if pairing_type not in VALID_TYPE:
        pairing_type = row["pairing_type"]
    rationale = data.get("pairing_rationale", row["pairing_rationale"])

    bev_cat = "wine"
    if row["beverage_product_id"]:
        cur.execute("SELECT category FROM beverage_products WHERE id = %s", (row["beverage_product_id"],))
        prod = cur.fetchone()
        if prod:
            c = prod["category"] or ""
            bev_cat = "wine" if c.startswith("wine_") else (c if c in (
                "beer", "sake", "tea", "coffee", "kombucha", "spirit", "non_alcoholic"
            ) else "wine")

    src = row["source_urls"]
    src_json = json.dumps(src if isinstance(src, list) else [])

    cur.execute("""
        INSERT INTO technique_beverage_pairings
            (technique_id, beverage_product_id, beverage_producer_id,
             pairing_type, pairing_rationale, confidence_status, verification_level,
             display_order, source_urls, beverage_category)
        VALUES (%s, %s, %s, %s, %s, 'partial', 'auto', 100, %s::jsonb, %s)
        ON CONFLICT (technique_id, beverage_product_id) DO NOTHING
    """, (
        row["technique_id"], row["beverage_product_id"], row["beverage_producer_id"],
        pairing_type, rationale, src_json, bev_cat,
    ))
    promoted = cur.rowcount
    cur.execute(
        "UPDATE technique_beverage_pairings_staging SET review_status='approved', reviewed_at=NOW() WHERE id=%s",
        (staging_id,),
    )
    cur.close()
    return jsonify(ok=True, action="promoted", inserted=promoted)


# Route 8 — Producer inverse view
@app.route("/admin/technique-pairings/producer/<int:producer_id>")
def admin_tbp_producer(producer_id):
    g = _admin_guard()
    if g:
        return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        "SELECT id, name, country, producer_type FROM beverage_producers WHERE id = %s",
        (producer_id,),
    )
    producer = cur.fetchone()
    if not producer:
        cur.close()
        return "Producer not found", 404

    cur.execute("""
        SELECT bp.id AS product_id, bp.name AS product_name, bp.slug AS product_slug,
               bp.subcategory,
               COUNT(tbp.id) AS pairing_count,
               SUM(CASE WHEN tbp.confidence_status IN ('editorial','reviewed') THEN 1 ELSE 0 END) AS editorial_count
        FROM beverage_products bp
        LEFT JOIN technique_beverage_pairings tbp ON tbp.beverage_product_id = bp.id
        WHERE bp.producer_id = %s
        GROUP BY bp.id, bp.name, bp.slug, bp.subcategory
        ORDER BY pairing_count DESC, bp.name
    """, (producer_id,))
    products = cur.fetchall()

    cur.execute("""
        SELECT tbp.id AS pairing_id, tbp.pairing_type, tbp.confidence_status,
               tbp.pairing_rationale, tbp.display_order,
               tr.id  AS technique_id, tr.name AS technique_name,
               tr.slug AS technique_slug, tr.canon_slug,
               bp.id  AS product_id,   bp.name AS product_name, bp.slug AS product_slug
        FROM technique_beverage_pairings tbp
        JOIN technique_references tr ON tbp.technique_id = tr.id
        LEFT JOIN beverage_products bp ON tbp.beverage_product_id = bp.id
        WHERE bp.producer_id = %s OR tbp.beverage_producer_id = %s
        ORDER BY tr.canon_slug, tr.name, tbp.confidence_status, tbp.display_order
    """, (producer_id, producer_id))
    pairings = cur.fetchall()
    cur.close()

    return render_template("admin_tbp_producer.html",
        producer=producer,
        products=products,
        pairings=pairings,
    )


# ─── Admin: Producer Warnings ────────────────────────────────────────────────

@app.route("/admin/producers/review")
def admin_producer_review():
    g = _admin_guard()
    if g: return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT bp.id, bp.name, bp.country, bp.slug,
               bp.producer_type, bp.price_positioning, bp.is_published,
               bp.warnings, jsonb_array_length(bp.warnings) AS warning_count,
               br.name AS region_name, br.country AS region_country,
               bp.created_at
        FROM beverage_producers bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE jsonb_array_length(bp.warnings) > 0
        ORDER BY jsonb_array_length(bp.warnings) DESC, bp.created_at DESC
        LIMIT 200
    """)
    flagged = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT
            COUNT(*)                                                              AS total,
            SUM(CASE WHEN jsonb_array_length(warnings) > 0 THEN 1 ELSE 0 END)  AS flagged,
            SUM(CASE WHEN jsonb_array_length(warnings) = 0 THEN 1 ELSE 0 END)  AS clean
        FROM beverage_producers
    """)
    stats = dict(cur.fetchone())

    # Warning-code frequency across flagged rows
    cur.execute("""
        SELECT w->>'code' AS code, COUNT(*) AS n
        FROM beverage_producers, jsonb_array_elements(warnings) AS w
        GROUP BY code ORDER BY n DESC
    """)
    code_freq = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()
    return render_template("admin_producer_review.html",
        flagged=flagged,
        stats=stats,
        code_freq=code_freq,
        is_sample_view=False,
        sample=[],
    )


@app.route("/admin/producers/<int:producer_id>/dismiss-warning", methods=["POST"])
def admin_producer_dismiss_warning(producer_id):
    g = _admin_guard_api()
    if g: return g
    data = request.get_json(force=True)
    code = (data.get("code") or "").strip()
    if not code:
        return jsonify({"ok": False, "error": "Missing warning code"})
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        UPDATE beverage_producers
        SET warnings = (
                SELECT COALESCE(jsonb_agg(w), '[]'::jsonb)
                FROM jsonb_array_elements(warnings) AS w
                WHERE w->>'code' <> %s
            ),
            updated_at = NOW()
        WHERE id = %s
        RETURNING jsonb_array_length(warnings) AS remaining
    """, (code, producer_id))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"ok": False, "error": "Producer not found"})
    return jsonify({"ok": True, "remaining": row["remaining"]})


@app.route("/admin/producers/sample")
def admin_producer_sample():
    """Weekly 1% random sample from non-warning producers for Haiku failure-mode detection."""
    g = _admin_guard()
    if g: return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Clamp sample size: 1% of clean producers, min 5, max 50
    cur.execute("""
        SELECT GREATEST(5, LEAST(50, COUNT(*) / 100))::int AS n
        FROM beverage_producers
        WHERE jsonb_array_length(warnings) = 0
    """)
    sample_n = cur.fetchone()["n"]

    cur.execute("""
        SELECT bp.id, bp.name, bp.country, bp.slug,
               bp.producer_type, bp.production_philosophy,
               LEFT(bp.philosophy_description, 240) AS philosophy_snippet,
               LEFT(bp.reputation_narrative,   240) AS narrative_snippet,
               bp.is_published, bp.created_at,
               br.name AS region_name
        FROM beverage_producers bp
        LEFT JOIN beverage_regions br ON bp.region_id = br.id
        WHERE jsonb_array_length(bp.warnings) = 0
        ORDER BY RANDOM()
        LIMIT %s
    """, (sample_n,))
    sample = [dict(r) for r in cur.fetchall()]

    cur.close()
    conn.close()
    return render_template("admin_producer_review.html",
        flagged=[],
        stats=None,
        code_freq=[],
        is_sample_view=True,
        sample=sample,
    )


# ─── l'Atelier — Menu Composition API ───────────────────────────────────────

_ATELIER_OCCASION_TYPES = {
    "wedding", "funeral", "birthday", "anniversary",
    "christmas_eve", "christmas_day", "thanksgiving", "easter",
    "halloween", "new_years_eve", "new_years_day",
    "lunar_new_year", "diwali", "eid_al_fitr", "eid_al_adha",
    "passover", "hanukkah", "bar_mitzvah", "bat_mitzvah",
    "quinceañera", "baby_shower", "corporate", "retirement",
    "graduation", "valentines", "mothers_day", "fathers_day",
    "harvest_seasonal", "summer_bbq", "day_of_the_dead",
    "mardi_gras", "st_patricks", "oktoberfest",
}

_ATELIER_SEASONS = {"spring", "summer", "autumn", "winter", "any"}

_ATELIER_MENU_FORMAT_TYPES = {
    "tasting_menu", "communal_feast", "canapé_reception",
    "family_style_centerpiece", "ritual_progression", "buffet",
    "cocktail_reception", "multi_course_seated",
    "shared_plates", "single_dish_inventive",
}

_ATELIER_OUTPUT_SHAPES = {"single_recipe", "menu"}

_ATELIER_PARSE_SYSTEM_PROMPT = """\
You are a culinary brief parser for Provenance, a professional chef's tool. \
A chef has written a free-form brief describing a meal they want to compose. \
Parse it into structured JSON.

Return ONLY a single JSON object — no prose, no markdown fences, no explanation. \
The object must have exactly two top-level keys: "brief_parsed" and "confidence".

"brief_parsed" schema (use null for any field you are uncertain about):
{
  "occasion_type": <string|null — must be one of the 33 values listed below, or null>,
  "guest_count": <integer|null>,
  "dietary_constraints": <array of strings — empty array if none mentioned>,
  "primary_cuisine": <string|null — cuisine slug, e.g. "japanese", "polish", "thai">,
  "secondary_cuisines": <array of strings — empty array if none>,
  "season": <string|null — must be one of: spring, summer, autumn, winter, any — or null>,
  "beverage_preferences": <array of strings — empty array if none mentioned>,
  "home_tradition": <string|null — the chef's training tradition or home cuisine, if stated>,
  "current_location": <string|null — where they are cooking, if stated>,
  "output_shape_hint": <string|null — must be "single_recipe" or "menu" or null>,
  "course_count_target": <integer|null>,
  "menu_format_hint": <string|null — must be one of the 10 values listed below, or null>,
  "user_notes": <string|null — anything relevant that doesn't fit the above fields>
}

"confidence" schema — parallel to "brief_parsed", same keys, values 0.0–1.0:
  1.0 = explicitly stated fact in the brief
  0.5–0.8 = clearly inferable from context (e.g. "May" implies "spring")
  0.0–0.5 = speculative

Valid occasion_type values (use exactly as written, or null):
wedding, funeral, birthday, anniversary, christmas_eve, christmas_day,
thanksgiving, easter, halloween, new_years_eve, new_years_day,
lunar_new_year, diwali, eid_al_fitr, eid_al_adha, passover, hanukkah,
bar_mitzvah, bat_mitzvah, quinceañera, baby_shower, corporate, retirement,
graduation, valentines, mothers_day, fathers_day, harvest_seasonal,
summer_bbq, day_of_the_dead, mardi_gras, st_patricks, oktoberfest

Valid menu_format_hint values (use exactly as written, or null):
tasting_menu, communal_feast, canapé_reception, family_style_centerpiece,
ritual_progression, buffet, cocktail_reception, multi_course_seated,
shared_plates, single_dish_inventive

If a field is ambiguous or not mentioned, return null for that field and a low confidence score. \
Never fabricate details not present or clearly inferable from the brief.\
"""


@app.route("/api/atelier/parse-brief", methods=["POST"])
def atelier_parse_brief():
    from datetime import datetime
    print("[ATELIER PARSE] route entered", flush=True)

    user = get_current_user()
    if not user:
        return jsonify(error="Login required"), 401

    data = request.get_json() or {}
    brief_text = (data.get("brief_text") or "").strip()
    if not brief_text or len(brief_text) < 20:
        return jsonify(error="brief_text must be at least 20 characters"), 400

    title_override = (data.get("title") or "").strip() or None

    user_message = (
        "Parse the following chef's brief into the JSON structure described in your instructions.\n\n"
        f"<<<BRIEF>>>\n{brief_text}\n<<<END BRIEF>>>\n\n"
        "Return ONLY the JSON object now."
    )

    print(f"[ATELIER PARSE] calling Anthropic API; brief_chars={len(brief_text)}", flush=True)

    MAX_ATTEMPTS = 2
    required_keys = {"occasion_type", "output_shape_hint"}
    last_error = None
    warnings = []

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2048,
                timeout=30.0,
                system=_ATELIER_PARSE_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            raw_text = resp.content[0].text.strip()
            print(
                f"[ATELIER PARSE] attempt {attempt}/{MAX_ATTEMPTS} LLM returned; "
                f"raw_chars={len(raw_text)}",
                flush=True,
            )

            # Strip accidental markdown fences (same as HACCP)
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```", 2)[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
                raw_text = raw_text.rsplit("```", 1)[0].strip()

            parsed = json.loads(raw_text)

            # Require top-level wrapper keys
            missing = required_keys - set((parsed.get("brief_parsed") or {}).keys())
            if "brief_parsed" not in parsed or "confidence" not in parsed:
                raise ValueError("Response missing 'brief_parsed' or 'confidence' wrapper")
            # required_keys must be present in brief_parsed (null is fine)
            bp = parsed["brief_parsed"]
            for k in required_keys:
                if k not in bp:
                    raise ValueError(f"brief_parsed missing required key: {k!r}")

            print(f"[ATELIER PARSE] attempt {attempt}/{MAX_ATTEMPTS} succeeded", flush=True)
            break  # success

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            app.logger.warning(
                f"[ATELIER PARSE] attempt {attempt}/{MAX_ATTEMPTS} failed: "
                f"{type(e).__name__}: {e}"
            )
            if attempt < MAX_ATTEMPTS:
                _time.sleep(1)
                continue

        except Exception as e:
            app.logger.error(
                f"[ATELIER PARSE] non-retryable error on attempt {attempt}/{MAX_ATTEMPTS}: {e}"
            )
            return jsonify(error=str(e)), 500

    else:
        app.logger.error(
            f"[ATELIER PARSE] all {MAX_ATTEMPTS} attempts exhausted. Last error: {last_error}"
        )
        return jsonify(
            error="Brief parsing incomplete",
            detail="The parser returned an unexpected format. Please try again.",
            regenerate_recommended=True,
        ), 502

    bp = parsed["brief_parsed"]
    confidence = parsed["confidence"]

    # ── Constrained-enum normalization ────────────────────────────────────────
    def _normalize(field, valid_set):
        val = bp.get(field)
        if val is not None and val not in valid_set:
            warnings.append(
                f"Could not match {field}={val!r} to a known value."
            )
            bp[field] = None
            confidence[field] = 0.0

    _normalize("occasion_type", _ATELIER_OCCASION_TYPES)
    _normalize("season", _ATELIER_SEASONS)
    _normalize("menu_format_hint", _ATELIER_MENU_FORMAT_TYPES)
    _normalize("output_shape_hint", _ATELIER_OUTPUT_SHAPES)

    # ── output_shape for compositions (NOT NULL) ──────────────────────────────
    output_shape = bp.get("output_shape_hint") or "menu"
    if not bp.get("output_shape_hint"):
        warnings.append("output_shape_hint was null; defaulted to 'menu'.")

    # ── Title generation ──────────────────────────────────────────────────────
    if title_override:
        title = title_override
    else:
        segments = []
        if bp.get("occasion_type"):
            segments.append(bp["occasion_type"].replace("_", " ").title())
        elif bp.get("primary_cuisine"):
            segments.append(bp["primary_cuisine"].title())
        segments.append(datetime.now().strftime("%-d %b %Y"))
        title = "Composition · " + " · ".join(segments)

    # ── INSERT into compositions ──────────────────────────────────────────────
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO compositions
          (user_id, title, brief_text, brief_parsed,
           occasion_type, guest_count, dietary_constraints,
           season, home_tradition, current_location,
           output_shape, status)
        VALUES
          (%s, %s, %s, %s::jsonb,
           %s, %s, %s::jsonb,
           %s, %s, %s,
           %s, 'draft')
        RETURNING id
        """,
        (
            user["id"],
            title,
            brief_text,
            json.dumps(bp),
            bp.get("occasion_type"),
            bp.get("guest_count"),
            json.dumps(bp.get("dietary_constraints") or []),
            bp.get("season"),
            bp.get("home_tradition"),
            bp.get("current_location"),
            output_shape,
        ),
    )
    composition_id = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(f"[ATELIER PARSE] saved composition_id={composition_id} title={title!r}", flush=True)

    return jsonify(
        composition_id=composition_id,
        title=title,
        brief_parsed=bp,
        confidence=confidence,
        warnings=warnings,
    )


# ─── l'Atelier — Compose Engine (Phase B thin slice) ────────────────────────
# Canon-anchored only. Every slot → Invention via Haiku 4.5.
# Real-components rule enforced: lineage IDs validated against candidate pools.
# Mirrors HACCP retry pattern (MAX_ATTEMPTS=2, fence strip, 1s sleep).

_ATELIER_COMPOSE_MODEL = "claude-haiku-4-5-20251001"
_ATELIER_COMPOSE_MAX_ATTEMPTS = 2

INGREDIENT_AUGMENTATION_MODEL = 'claude-haiku-4-5-20251001'
INGREDIENT_AUGMENTATION_PROMPT_VERSION = 'INGREDIENT_AUGMENTATION_PROMPT_V2'
INGREDIENT_AUGMENTATION_THRESHOLD = 0.5
INGREDIENT_AUGMENTATION_FUZZY_THRESHOLD = 0.6

INGREDIENT_AUGMENTATION_PLACEHOLDER_NAMES = frozenset({
    'salt', 'sugar', 'butter', 'oil', 'water', 'pepper', 'flour',
    'milk', 'cream', 'heavy cream', 'eggs', 'egg', 'pasta', 'dried pasta',
    'vinegar', 'wine', 'chocolate', 'dark chocolate', 'olive oil',
    'black pepper', 'white pepper', 'vegetables', 'spring vegetables',
})

INGREDIENT_AUGMENTATION_SYSTEM_PROMPT_V2 = """\
You are writing for Provenance, a structured culinary library held to the standard of Larousse Gastronomique. When a dish's ingredient list is missing the ingredients that define it authentically, your task is to identify the signature ingredients \u2014 what a chef teaching this dish at examination depth would name as essential.

Rules:
- Return ONLY a JSON array of ingredient names. No prose, no markdown fence, no commentary.
- Use canonical culinary English with regional, varietal, or grade specificity. Examples: "Pecorino Romano DOP", "Guanciale", "Tonnarelli", "Veal cutlets", "Prosciutto di Parma", "Sage leaves", "Marsala wine", "Tellicherry black pepper", "Maldon sea salt flakes", "\u00c9chir\u00e9 cultured butter", "Spring asparagus", "Heirloom tomatoes".
- Names a chef in Tokyo or Lisbon would recognize as canonical \u2014 not regional shorthand, not branded supplier names.
- No producer names, no brands, no suppliers, no restaurants. "Veal" is correct. "Two Rivers veal" is wrong.
- NEVER return single-word generic names: Salt, Sugar, Butter, Oil, Water, Pepper, Flour, Milk, Cream, Eggs, Pasta, Vinegar, Wine, Chocolate, Vegetables. If a basic is signature to the dish, name it with precision ("Tellicherry black pepper", "Maldon flake salt", "00 Caputo flour", "Marans egg yolks"). If it cannot be specified, do not include it.
- Include basics ONLY when they are part of the dish identity itself \u2014 typically when the ingredient appears in the dish name (Cacio e Pepe \u2192 black pepper at Tellicherry grade; Salt-Crusted Branzino \u2192 salt at Maldon grade). If the basic is just kitchen support (butter to mount a sauce, salt to season a vegetable), exclude it.
- Where a regional variant matters, name it precisely ("Pecorino Romano DOP", not generic pecorino; "Marsala wine", not generic fortified wine).
- Better 4 canonical names than 8 mixed-quality names. Return 3\u20138 names total."""


# ─── Canon keyword extraction (tradition-agnostic) ──────────────────────────

_CANON_KEYWORD_STOPWORDS = frozenset({
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'has', 'have', 'had', 'this', 'that', 'these', 'those', 'as', 'it',
    'its', 'can', 'will', 'would', 'could', 'should', 'may', 'might',
    'must', 'shall', 'do', 'does', 'did', 'one', 'two', 'three', 'four',
    'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'course', 'courses', 'menu', 'meal', 'dish', 'dishes', 'food', 'foods',
    'cooking', 'cook', 'cooked', 'kitchen', 'served', 'serve', 'serves',
    'eaten', 'eating', 'recipe', 'recipes', 'traditional', 'traditionally',
    'usually', 'often', 'sometimes', 'including', 'such', 'other', 'others',
    'each', 'every', 'some', 'most', 'many', 'much', 'more', 'less',
    'where', 'when', 'what', 'which', 'who', 'whom', 'whose', 'why', 'how',
    'before', 'after', 'during', 'between', 'about', 'into', 'onto', 'over',
    'under', 'above', 'below', 'across', 'around', 'through',
})


def _extract_canon_keywords(canon, max_keywords=80):
    """
    Extract content keywords from a canon entry to scope the candidate pool.
    Tradition-agnostic — pulls from the canon's name, description, origin,
    and course_slots slot names. Same code works for kaiseki, wigilia, mezze,
    sri lankan rice & curry, italian sunday lunch — every canon.
    """
    text_parts = []
    # name and origin first — short, high-signal
    for field in ('name', 'origin'):
        val = canon.get(field)
        if val:
            text_parts.append(str(val))

    # course_slots notes BEFORE description — slot notes contain the richest
    # tradition-specific vocabulary (matsutake, dashi, hamaguri, pierogi, etc.)
    # and must not be crowded out by the prose description budget.
    slots = canon.get('course_slots') or []
    if isinstance(slots, list):
        for slot in slots:
            if not isinstance(slot, dict):
                continue
            for key in ('slot_name', 'slot_role', 'notes'):
                v = slot.get(key)
                if v:
                    text_parts.append(str(v))

    # Description last — often generic prose, padded after slot vocabulary
    if canon.get('description'):
        text_parts.append(str(canon['description']))

    text = ' '.join(text_parts).lower()
    # Alphabetic runs of length >= 4 (handles unicode for non-English canons)
    tokens = _re.findall(r"[a-zà-ÿäöüß'-]{4,}", text)
    keywords = []
    seen = set()
    for tok in tokens:
        tok = tok.strip("'-")
        if len(tok) < 4 or tok in _CANON_KEYWORD_STOPWORDS or tok in seen:
            continue
        seen.add(tok)
        keywords.append(tok)
        if len(keywords) >= max_keywords:
            break
    return keywords


def _build_candidate_pools_for_canon(canon, parsed_brief=None):
    """
    Pre-fetch real DB rows for the Haiku candidate pool.
    Filter is canon-derived keywords (tradition-agnostic) — same code works
    for any canon. The keywords come from the canon entry itself, so a kaiseki
    canon scopes the pool around 'matsutake/sake/dashi' and a wigilia canon
    scopes around 'carp/beetroot/pierogi/poppy', without code change.

    parsed_brief is optional. When present, the brief's primary_cuisine expands
    into CUISINE_SYNONYMS and ORed into each query so an Italian brief also
    pulls Italian-origin content even if the canon keywords don't include
    geographic terms.
    """
    keywords = _extract_canon_keywords(canon)
    kw_pattern = '|'.join(_re.escape(k) for k in keywords) if keywords else 'zzzzz_no_match'

    # Cuisine expansion — adds geo/sub-cuisine terms as a second OR branch
    cuisine_synonyms = _expand_cuisine((parsed_brief or {}).get('primary_cuisine'))
    cuisine_regex = '|'.join(_re.escape(s) for s in cuisine_synonyms) if cuisine_synonyms else None
    cuisine_countries = _expand_cuisine_countries((parsed_brief or {}).get('primary_cuisine'))
    app.logger.info(f"[ATELIER DIAG] cuisine_patterns={cuisine_synonyms} cuisine_regex={cuisine_regex}")

    app.logger.info(
        f"[ATELIER POOL] canon {canon['id']} "
        f"keywords={keywords[:10]}{'...' if len(keywords) > 10 else ''} "
        f"cuisine_regex={cuisine_regex!r:.60}"
    )

    pools = {"techniques": [], "ingredients": [], "beverages": [], "_keywords": keywords}

    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            # Techniques — match keywords OR cuisine synonyms; deterministic relevance ranking
            if cuisine_regex:
                cur.execute(
                    """SELECT id, name, description FROM technique_references
                       WHERE id IS DISTINCT FROM %s
                         AND (
                               COALESCE(origin, '')      ~* %s
                            OR name                      ~* %s
                            OR COALESCE(description, '') ~* %s
                            OR COALESCE(origin, '')      ~* %s
                            OR name                      ~* %s
                            OR COALESCE(description, '') ~* %s
                         )
                       ORDER BY (CASE WHEN COALESCE(origin,'') ~* %s THEN 0
                                      WHEN name                ~* %s THEN 1
                                      ELSE 2 END),
                                id
                       LIMIT 100""",
                    (canon['id'],
                     kw_pattern, kw_pattern, kw_pattern,
                     cuisine_regex, cuisine_regex, cuisine_regex,
                     cuisine_regex, cuisine_regex),
                )
            else:
                cur.execute(
                    """SELECT id, name, description FROM technique_references
                       WHERE id IS DISTINCT FROM %s
                         AND (
                               COALESCE(origin, '')      ~* %s
                            OR name                      ~* %s
                            OR COALESCE(description, '') ~* %s
                         )
                       ORDER BY (CASE WHEN name ~* %s THEN 0 ELSE 1 END), id
                       LIMIT 100""",
                    (canon['id'], kw_pattern, kw_pattern, kw_pattern, kw_pattern),
                )
            pools["techniques"] = [dict(r) for r in cur.fetchall()]

            # Full cuisine valid-set: all matching IDs (no limit) for validation below
            if cuisine_regex:
                cur.execute(
                    """SELECT id FROM technique_references
                       WHERE COALESCE(origin,'')      ~* %s
                          OR name                     ~* %s
                          OR COALESCE(description,'') ~* %s""",
                    (cuisine_regex, cuisine_regex, cuisine_regex),
                )
                pools["_all_cuisine_technique_ids"] = {r["id"] for r in cur.fetchall()}
            else:
                pools["_all_cuisine_technique_ids"] = None

            # Ingredients — match against name / description / origin_country
            try:
                if cuisine_regex:
                    cur.execute(
                        """SELECT id, name, COALESCE(description, '') AS description
                           FROM ingredient_products
                           WHERE (
                                   name                         ~* %s
                              OR COALESCE(description, '')    ~* %s
                              OR COALESCE(origin_country, '') ~* %s
                              OR name                         ~* %s
                              OR COALESCE(description, '')    ~* %s
                              OR COALESCE(origin_country, '') ~* %s
                           )
                           AND NOT (source = 'ai-augmented' AND validated IS NOT TRUE)
                           ORDER BY (CASE WHEN COALESCE(origin_country,'') ~* %s THEN 0 ELSE 1 END),
                                    RANDOM()
                           LIMIT 150""",
                        (kw_pattern, kw_pattern, kw_pattern,
                         cuisine_regex, cuisine_regex, cuisine_regex,
                         cuisine_regex),
                    )
                else:
                    cur.execute(
                        """SELECT id, name, COALESCE(description, '') AS description
                           FROM ingredient_products
                           WHERE (
                                   name                         ~* %s
                              OR COALESCE(description, '')    ~* %s
                              OR COALESCE(origin_country, '') ~* %s
                           )
                           AND NOT (source = 'ai-augmented' AND validated IS NOT TRUE)
                           ORDER BY RANDOM()
                           LIMIT 150""",
                        (kw_pattern, kw_pattern, kw_pattern),
                    )
                pools["ingredients"] = [dict(r) for r in cur.fetchall()]
            except Exception as e:
                app.logger.warning(f"[ATELIER POOL] ingredients query failed: {e}")
                pools["ingredients"] = []

            # Beverages — country-anchored when cuisine is known; cuisine_regex
            # is a secondary allow for sub-regional names within that country.
            try:
                if cuisine_countries:
                    cur.execute(
                        """SELECT bp.id, bp.name, br.name AS region
                           FROM beverage_products bp
                           LEFT JOIN beverage_regions br ON br.id = bp.region_id
                           WHERE (br.country = ANY(%s)
                              OR bp.name ~* %s)
                              AND bp.is_published IS TRUE
                           ORDER BY bp.id LIMIT 80""",
                        (cuisine_countries, cuisine_regex or 'zzzz_no_match'),
                    )
                elif cuisine_regex:
                    cur.execute(
                        """SELECT bp.id, bp.name, br.name AS region
                           FROM beverage_products bp
                           LEFT JOIN beverage_regions br ON br.id = bp.region_id
                           WHERE (bp.name                  ~* %s
                              OR COALESCE(br.name,    '') ~* %s
                              OR COALESCE(br.country, '') ~* %s
                              OR bp.name                  ~* %s
                              OR COALESCE(br.name,    '') ~* %s
                              OR COALESCE(br.country, '') ~* %s)
                              AND bp.is_published IS TRUE
                           ORDER BY bp.id LIMIT 80""",
                        (kw_pattern, kw_pattern, kw_pattern,
                         cuisine_regex, cuisine_regex, cuisine_regex),
                    )
                else:
                    cur.execute(
                        """SELECT bp.id, bp.name, br.name AS region
                           FROM beverage_products bp
                           LEFT JOIN beverage_regions br ON br.id = bp.region_id
                           WHERE (bp.name                  ~* %s
                              OR COALESCE(br.name,    '') ~* %s
                              OR COALESCE(br.country, '') ~* %s)
                              AND bp.is_published IS TRUE
                           ORDER BY bp.id LIMIT 80""",
                        (kw_pattern, kw_pattern, kw_pattern),
                    )
                pools["beverages"] = [dict(r) for r in cur.fetchall()]
            except Exception as e:
                app.logger.warning(f"[ATELIER POOL] beverages query failed: {e}")
                pools["beverages"] = []
        finally:
            cur.close()
    finally:
        conn.close()

    app.logger.info(f"[ATELIER DIAG] pool sizes: techniques={len(pools.get('techniques',[]))} ingredients={len(pools.get('ingredients',[]))} beverages={len(pools.get('beverages',[]))}")
    return pools


# ─── Cuisine synonym map ─────────────────────────────────────────────────────

CUISINE_SYNONYMS = {
    'italian':   ['italian', 'italy', 'italia', 'roman', 'tuscan', 'tuscany',
                  'sicilian', 'sicily', 'neapolitan', 'naples', 'venetian', 'venice',
                  'lombard', 'piedmontese', 'piedmont', 'umbrian', 'emilian',
                  'apulian', 'calabrian', 'sardinian', 'ligurian'],
    'french':    ['french', 'france', 'burgundian', 'burgundy', 'bordelaise', 'bordeaux',
                  'provençal', 'provencal', 'provence', 'alsatian', 'alsace',
                  'gascon', 'gascony', 'normand', 'normandy', 'savoyard', 'savoy',
                  'breton', 'brittany', 'lyonnaise', 'lyon', 'parisian', 'paris'],
    'japanese':  ['japanese', 'japan', 'kaiseki', 'washoku', 'edomae', 'kansai',
                  'kanto', 'okinawan', 'okinawa', 'kyoto', 'osaka', 'hokkaido',
                  'kyushu', 'tohoku'],
    'chinese':   ['chinese', 'china', 'cantonese', 'guangdong', 'sichuan', 'szechuan',
                  'hunan', 'shanghainese', 'shanghai', 'beijing', 'pekinese',
                  'fujian', 'shandong', 'jiangsu', 'taiwanese', 'taiwan'],
    'mexican':   ['mexican', 'mexico', 'oaxacan', 'oaxaca', 'yucatecan', 'yucatan',
                  'jalisco', 'pueblan', 'puebla', 'veracruz', 'sonoran', 'baja'],
    'thai':      ['thai', 'thailand', 'isan', 'lanna', 'central thai', 'southern thai'],
    'indian':    ['indian', 'india', 'punjabi', 'punjab', 'bengali', 'bengal',
                  'goan', 'goa', 'kerala', 'tamil', 'rajasthani', 'mughlai',
                  'gujarati', 'maharashtrian', 'kashmir'],
    'spanish':   ['spanish', 'spain', 'catalan', 'catalonia', 'basque', 'andalusian',
                  'andalucia', 'galician', 'galicia', 'castilian', 'castile',
                  'valencian', 'valencia'],
    'greek':     ['greek', 'greece', 'cretan', 'crete', 'macedonian', 'thessaloniki',
                  'cycladic', 'peloponnesian', 'epirote'],
    'korean':    ['korean', 'korea', 'jeolla', 'gyeongsang', 'seoul', 'busan'],
    'vietnamese':['vietnamese', 'vietnam', 'hanoi', 'saigon', 'mekong', 'hue'],
    'lebanese':  ['lebanese', 'lebanon', 'levantine', 'levant'],
    'moroccan':  ['moroccan', 'morocco', 'maghrebi', 'maghreb', 'fez', 'marrakech'],
    'north african': ['north african', 'north africa', 'moroccan', 'morocco',
                      'tunisian', 'tunisia', 'algerian', 'algeria',
                      'maghrebi', 'maghreb', 'libyan', 'libya',
                      'egyptian', 'egypt', 'berber',
                      'marrakech', 'fez', 'casablanca', 'tunis'],
    'peruvian':  ['peruvian', 'peru', 'limeño', 'limeno', 'lima', 'andean', 'amazonian'],
    'ukrainian': ['ukrainian', 'ukraine', 'kyiv', 'lviv', 'odessa', 'galician',
                  'cossack', 'carpathian', 'eastern european'],
}


def _expand_cuisine(cuisine_str):
    """Return the synonym list for a cuisine key, or [key] if unknown."""
    if not cuisine_str:
        return []
    key = cuisine_str.strip().lower()
    return CUISINE_SYNONYMS.get(key, [key])


CUISINE_TO_COUNTRIES = {
    'italian':    ['Italy'],
    'french':     ['France'],
    'japanese':   ['Japan'],
    'chinese':    ['China'],
    'mexican':    ['Mexico'],
    'thai':       ['Thailand'],
    'indian':     ['India'],
    'spanish':    ['Spain'],
    'greek':      ['Greece'],
    'korean':     ['South Korea', 'Korea'],
    'vietnamese': ['Vietnam'],
    'lebanese':   ['Lebanon'],
    'moroccan':   ['Morocco'],
    'north african': ['Morocco', 'Tunisia', 'Algeria', 'Libya', 'Egypt'],
    'peruvian':   ['Peru'],
    'ukrainian':  ['Ukraine'],
}


def _expand_cuisine_countries(cuisine_str):
    if not cuisine_str:
        return []
    return CUISINE_TO_COUNTRIES.get(cuisine_str.strip().lower(), [])


def _ingredient_signature_overlap(invention):
    """
    Returns the fraction of significant Latin-script tokens from the dish name
    that appear in any lineage_ingredient name.
    Non-Latin-script names (Japanese, Korean, Chinese, etc.) produce no tokens.
    When that happens, the result depends on whether lineage is populated:
      - empty lineage → 0.0 (trigger augmentation — ingredients genuinely missing)
      - populated lineage → 1.0 (trust it — can't verify but don't discard)
    """
    _OVERLAP_STOPWORDS = frozenset({
        'and', 'with', 'for', 'the', 'di', 'alla', 'con', 'alle', 'della',
        'del', 'all', 'da', 'dal', 'in', 'on', 'of', 'le', 'la', 'et',
    })
    dish_name = invention.get('name') or ''
    tokens = [
        t.lower() for t in _re.findall(r'[a-zA-Z]{3,}', dish_name)
        if t.lower() not in _OVERLAP_STOPWORDS
    ]
    if not tokens:
        # Can't tokenise (non-Latin script or all-stopword name).
        # If lineage is also empty, it genuinely needs augmentation → 0.0.
        # If lineage is already populated, trust it → 1.0.
        if not (invention.get('lineage_ingredients') or []):
            return 0.0
        return 1.0
    ingredients = invention.get('lineage_ingredients') or []
    ing_text = ' '.join(
        (i.get('name') if isinstance(i, dict) else str(i)).lower()
        for i in ingredients
    )
    matched = sum(1 for t in tokens if t in ing_text)
    return matched / len(tokens)


def _augment_ingredients_via_haiku(invention, parsed_brief, cur):
    """
    Calls Haiku to identify signature ingredients for a dish whose
    lineage_ingredients list is sparse. Resolves returned names against
    ingredient_products via exact match, parenthetical-stripped match,
    pg_trgm fuzzy match, or INSERT as a new ai-augmented row.
    Mutates invention['lineage_ingredients'] in place.
    Any exception is caught and printed; augmentation never crashes compose.
    """
    import json as _json

    try:
        # ── Check pg_trgm availability (read-only; never auto-enable) ──────────
        cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm'")
        trgm_available = cur.fetchone() is not None
        if not trgm_available:
            print("[AUGMENT] pg_trgm not enabled — fuzzy match disabled", flush=True)

        # ── Build user prompt ────────────────────────────────────────────────────
        current_names = [
            i.get('name', i) if isinstance(i, dict) else str(i)
            for i in (invention.get('lineage_ingredients') or [])
        ]
        user_prompt = (
            f"Dish: {invention['name']}\n"
            f"Description: {invention.get('description') or '(none)'}\n"
            f"Cuisine: {parsed_brief.get('primary_cuisine') or 'unspecified'}\n"
            f"Current ingredient list (incomplete): {current_names}\n\n"
            f"Return the signature ingredients for this dish."
        )

        # ── Call Haiku ──────────────────────────────────────────────────────────
        response = client.messages.create(
            model=INGREDIENT_AUGMENTATION_MODEL,
            max_tokens=256,
            system=INGREDIENT_AUGMENTATION_SYSTEM_PROMPT_V2,
            messages=[{"role": "user", "content": user_prompt}],
        )
        raw = response.content[0].text.strip()

        # ── Parse JSON array ─────────────────────────────────────────────────────
        s, e = raw.find('['), raw.rfind(']')
        if s == -1 or e == -1 or s >= e:
            print(
                f"[AUGMENT] Haiku returned non-array for dish "
                f"{invention['name']!r}: {raw[:120]!r}",
                flush=True,
            )
            return invention
        returned_names = _json.loads(raw[s:e + 1])
        if not isinstance(returned_names, list):
            print(
                f"[AUGMENT] parsed result is not a list for {invention['name']!r}",
                flush=True,
            )
            return invention

        # ── Derive origin_country from cuisine ──────────────────────────────────
        cuisine_str = (parsed_brief.get('primary_cuisine') or '').strip().lower()
        country_list = CUISINE_TO_COUNTRIES.get(cuisine_str, [])
        origin_country = country_list[0] if country_list else None

        # ── Resolve / insert each name ──────────────────────────────────────────
        existing_ids = {
            i['id'] for i in (invention.get('lineage_ingredients') or [])
            if isinstance(i, dict) and i.get('id') is not None
        }
        new_entries = []

        for ing_name in returned_names:
            ing_name = str(ing_name).strip()
            if not ing_name:
                continue

            # FIX 2B — reject generic placeholder names before any DB work
            if ing_name.lower() in INGREDIENT_AUGMENTATION_PLACEHOLDER_NAMES:
                print(
                    f"[AUGMENT] rejected placeholder name: {ing_name!r} "
                    f"for {invention.get('name')!r}",
                    flush=True,
                )
                continue

            # 1. Exact case-insensitive match
            cur.execute(
                "SELECT id, name FROM ingredient_products "
                "WHERE lower(name) = lower(%s) LIMIT 1",
                (ing_name,),
            )
            row = cur.fetchone()
            if row:
                entry = dict(row)
                if entry['id'] not in existing_ids:
                    new_entries.append(entry)
                    existing_ids.add(entry['id'])
                continue

            # 1b. Parenthetical-stripped match — resolves "Bottarga di Muggine"
            # against "Bottarga di Muggine (Grey Mullet Roe)" and vice versa.
            cur.execute(
                r"SELECT id, name FROM ingredient_products "
                r"WHERE lower(regexp_replace(name, '\s*\([^)]*\)\s*', '')) "
                r"    = lower(regexp_replace(%s,  '\s*\([^)]*\)\s*', '')) "
                r"LIMIT 1",
                (ing_name,),
            )
            row = cur.fetchone()
            if row:
                entry = dict(row)
                if entry['id'] not in existing_ids:
                    new_entries.append(entry)
                    existing_ids.add(entry['id'])
                continue

            # 2. Fuzzy trigram match (threshold INGREDIENT_AUGMENTATION_FUZZY_THRESHOLD)
            if trgm_available:
                cur.execute(
                    """SELECT id, name, similarity(name, %s) AS sim
                       FROM ingredient_products
                       WHERE similarity(name, %s) >= %s
                       ORDER BY sim DESC
                       LIMIT 1""",
                    (ing_name, ing_name, INGREDIENT_AUGMENTATION_FUZZY_THRESHOLD),
                )
                row = cur.fetchone()
                if row:
                    entry = {'id': row['id'], 'name': row['name']}
                    if entry['id'] not in existing_ids:
                        new_entries.append(entry)
                        existing_ids.add(entry['id'])
                    continue

            # 3. INSERT new ai-augmented row.
            # category is NOT NULL with no default — 'produce_specialty' is used
            # as the most generic valid category for ai-augmented entries.
            # (Judgment call documented in Phase 1 build report.)
            try:
                cur.execute(
                    """INSERT INTO ingredient_products
                           (name, category, origin_country,
                            source, validated, model_version, prompt_version)
                       VALUES (%s, 'produce_specialty', %s,
                               'ai-augmented', false, %s, %s)
                       RETURNING id, name""",
                    (
                        ing_name,
                        origin_country,
                        INGREDIENT_AUGMENTATION_MODEL,
                        INGREDIENT_AUGMENTATION_PROMPT_VERSION,
                    ),
                )
                new_row = cur.fetchone()
                if new_row:
                    entry = dict(new_row)
                    new_entries.append(entry)
                    existing_ids.add(entry['id'])
            except Exception as insert_exc:
                print(
                    f"[AUGMENT] INSERT failed for {ing_name!r}: {insert_exc}",
                    flush=True,
                )
                continue

        # ── Merge into lineage_ingredients (dedupe by id, preserve order) ───────
        existing_list = [
            i for i in (invention.get('lineage_ingredients') or [])
            if isinstance(i, dict)
        ]
        invention['lineage_ingredients'] = existing_list + new_entries

        print(
            f"[AUGMENT] {invention['name']!r}: added {len(new_entries)} ingredient(s) "
            f"via Haiku augmentation",
            flush=True,
        )

    except Exception as exc:
        print(
            f"[AUGMENT] augmentation failed for {invention.get('name')!r}: {exc}",
            flush=True,
        )

    return invention


# ─── Canon matcher, free-form slot generator, lineage enricher ───────────────

def _match_library_recipe_for_slot(slot, parsed_brief, cur, threshold=0.03, invention=None):
    """
    Find the best curated library recipe matching this slot via PostgreSQL FTS.
    Returns dict {id, slug, name, cuisine, description, score} or None.
    Only searches is_curated=true recipes (public library, not user recipes).

    Query strategy: ingredient names from the generated invention, OR-joined via
    websearch_to_tsquery. Invention name and slot_role are excluded — dish names
    are too specific for sister-dish matching, and slot_role terms like "pasta course"
    produce dead stop-word constraints ('cours') that kill AND matches.
    OR-based scoring sits in the 0.03–0.06 range for true positives; threshold=0.03.
    """
    # Ingredient names are the highest-signal stable terms across sister dishes.
    # Exclude invention name (too dish-specific) and slot/occasion terms (stop words).
    query_parts = []
    if invention:
        for ing in (invention.get('lineage_ingredients') or [])[:5]:
            ing_name = ing.get('name') if isinstance(ing, dict) else ing
            if ing_name:
                query_parts.append(str(ing_name))

    if not query_parts:
        return None

    # OR-join so any matching ingredient hits the recipe; plainto_tsquery AND would
    # require all terms to appear verbatim, which sister dishes rarely satisfy.
    query_text = ' OR '.join(query_parts)

    cuisine_synonyms = _expand_cuisine(parsed_brief.get('primary_cuisine'))
    cuisine_re = '|'.join(cuisine_synonyms) if cuisine_synonyms else None

    try:
        cur.execute(
            """SELECT id, slug, name, cuisine, description,
                      ts_rank(
                          to_tsvector('english',
                              COALESCE(name, '') || ' ' ||
                              COALESCE(cuisine, '') || ' ' ||
                              COALESCE(description, '')
                          ),
                          websearch_to_tsquery('english', %s)
                      ) AS score
               FROM recipes
               WHERE is_curated = true
                 AND to_tsvector('english',
                         COALESCE(name, '') || ' ' ||
                         COALESCE(cuisine, '') || ' ' ||
                         COALESCE(description, '')
                     ) @@ websearch_to_tsquery('english', %s)
               ORDER BY score DESC
               LIMIT 5""",
            (query_text, query_text),
        )
        candidates = [dict(r) for r in cur.fetchall()]

        # Prefer cuisine-matching candidates; fall back to all if none match
        if cuisine_re and candidates:
            matching = [c for c in candidates
                        if c.get('cuisine')
                        and _re.search(cuisine_re, c['cuisine'], _re.IGNORECASE)]
            if matching:
                candidates = matching

        best = candidates[0] if candidates else None
        if best and float(best.get('score', 0)) >= threshold:
            return {
                'id':          best['id'],
                'slug':        best.get('slug'),
                'name':        best['name'],
                'cuisine':     best.get('cuisine'),
                'description': best.get('description'),
                'score':       float(best['score']),
            }
    except Exception as exc:
        app.logger.warning(
            f"[ATELIER LIBRARY] recipe match failed for slot "
            f"{slot.get('slot_name')!r}: {exc}"
        )

    # Fallback: name-based FTS when ingredient path produced nothing.
    # Fires only when both existing paths above would return None.
    # Stricter threshold (0.05 vs 0.03) — a bad name match is worse than no match.
    fallback_threshold = 0.05
    fallback_parts = []
    if invention:
        dish_name = invention.get('name') or ''
        for token in dish_name.split():
            clean = token.strip('.,;:\'"()[]').strip()
            if len(clean) >= 5:
                fallback_parts.append(clean)

    if fallback_parts:
        fallback_query = ' OR '.join(fallback_parts)
        try:
            cur.execute(
                """SELECT id, slug, name, cuisine, description,
                          ts_rank(
                              to_tsvector('english',
                                  COALESCE(name, '') || ' ' ||
                                  COALESCE(cuisine, '') || ' ' ||
                                  COALESCE(description, '')
                              ),
                              websearch_to_tsquery('english', %s)
                          ) AS score
                   FROM recipes
                   WHERE is_curated = true
                     AND to_tsvector('english',
                             COALESCE(name, '') || ' ' ||
                             COALESCE(cuisine, '') || ' ' ||
                             COALESCE(description, '')
                         ) @@ websearch_to_tsquery('english', %s)
                   ORDER BY score DESC
                   LIMIT 5""",
                (fallback_query, fallback_query),
            )
            fb_candidates = [dict(r) for r in cur.fetchall()]

            if cuisine_re and fb_candidates:
                fb_matching = [c for c in fb_candidates
                               if c.get('cuisine')
                               and _re.search(cuisine_re, c['cuisine'], _re.IGNORECASE)]
                if fb_matching:
                    fb_candidates = fb_matching

            fb_best = fb_candidates[0] if fb_candidates else None
            if fb_best and float(fb_best.get('score', 0)) >= fallback_threshold:
                app.logger.info(
                    f"[ATELIER LIBRARY] name-fallback hit for slot "
                    f"{slot.get('slot_name')!r}: {fb_best['name']!r} "
                    f"score={float(fb_best['score']):.4f}"
                )
                return {
                    'id':          fb_best['id'],
                    'slug':        fb_best.get('slug'),
                    'name':        fb_best['name'],
                    'cuisine':     fb_best.get('cuisine'),
                    'description': fb_best.get('description'),
                    'score':       float(fb_best['score']),
                }
        except Exception as fb_exc:
            app.logger.warning(
                f"[ATELIER LIBRARY] name-fallback failed for slot "
                f"{slot.get('slot_name')!r}: {fb_exc}"
            )

    return None


def _match_canon_for_brief(parsed_brief, cur):
    """
    Rules-based canon matcher. No LLM. Returns (canon_id, canon_name) or (None, None).
    Searches technique_references where canon_tier IS NOT NULL and course_slots IS NOT NULL.
    Tries primary_cuisine, home_tradition, secondary_cuisines in order.
    """
    terms = []
    for field in ('primary_cuisine', 'home_tradition'):
        val = parsed_brief.get(field)
        if val:
            terms.append(str(val).lower().replace('_', ' '))
    for val in (parsed_brief.get('secondary_cuisines') or []):
        terms.append(str(val).lower().replace('_', ' '))

    for term in terms:
        if len(term) < 3:
            continue
        cur.execute(
            """SELECT id, name FROM technique_references
               WHERE canon_tier IS NOT NULL
                 AND course_slots IS NOT NULL
                 AND (LOWER(name) ILIKE %s OR LOWER(origin) ILIKE %s)
               ORDER BY canon_tier ASC
               LIMIT 1""",
            (f'%{term}%', f'%{term}%'),
        )
        row = cur.fetchone()
        if row:
            return row['id'], row['name']

    return None, None


def _generate_freeform_slots(parsed_brief):
    """
    When no canon matches, call Haiku once to generate a slot structure shaped
    like course_slots JSONB. Falls back to a minimal structure on failure.
    """
    cuisine  = parsed_brief.get('primary_cuisine') or 'contemporary'
    season   = parsed_brief.get('season') or 'any'
    course_n = parsed_brief.get('course_count_target') or 5
    occasion = parsed_brief.get('occasion_type') or 'dinner'

    cuisine_hint = ""
    if parsed_brief.get('primary_cuisine'):
        c = parsed_brief['primary_cuisine']
        cuisine_hint = (
            f"\n\nIMPORTANT: The cuisine is **{c}**. Use cuisine-appropriate course "
            f"nomenclature in slot_name fields — never default to French restaurant "
            f"terms unless the cuisine is French or unspecified. Examples:\n"
            f"  italian → antipasto, primo, secondo, contorno, formaggi, dolce\n"
            f"  french  → amuse-bouche, entrée, plat principal, fromage, dessert\n"
            f"  japanese → zensai, mukozuke, hassun, takiawase, yakimono, gohan\n"
            f"  chinese → liang cai, re cai, zhu shi, tang, tian dian\n"
            f"  mexican → entrada, sopa, plato fuerte, guarnición, postre\n"
            f"  spanish → tapas, primero, segundo, postre\n"
            f"  ukrainian → zakuski, soup course, fish or vegetable course, main, sweet course\n"
            f"If the cuisine is not listed, use authentic course terminology from "
            f"that culture's tradition."
        )

    prompt = (
        f"Design a {course_n}-course menu structure for a {cuisine} "
        f"{occasion} in {season}.\n\n"
        f"Return a JSON array of exactly {course_n} slot objects. Each must have:\n"
        "  \"position\": integer (1-indexed),\n"
        "  \"slot_name\": short name using cuisine-appropriate terminology,\n"
        "  \"slot_role\": one-word role (e.g. starter, fish_course, main, dessert),\n"
        "  \"typical_temperature\": \"hot\" | \"warm\" | \"cool\" | \"cold\",\n"
        "  \"notes\": 1-2 sentences on what this slot should achieve.\n\n"
        "Return ONLY the JSON array, no markdown fence, no prose."
        + cuisine_hint
    )

    last_err = None
    for attempt in range(_ATELIER_COMPOSE_MAX_ATTEMPTS):
        try:
            resp = client.messages.create(
                model=_ATELIER_COMPOSE_MODEL,
                max_tokens=800,
                timeout=30.0,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```", 2)[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.rsplit("```", 1)[0].strip()
            slots = json.loads(raw)
            if not isinstance(slots, list) or not slots:
                raise ValueError("Expected non-empty list")
            for i, s in enumerate(slots):
                s.setdefault("position", i + 1)
                s.setdefault("slot_name", f"course_{i + 1}")
                s.setdefault("slot_role", "course")
                s.setdefault("typical_temperature", "warm")
                s.setdefault("notes", "")
            return slots
        except Exception as exc:
            last_err = exc
            if attempt < _ATELIER_COMPOSE_MAX_ATTEMPTS - 1:
                _time.sleep(1)

    app.logger.error(f"[ATELIER FREEFORM] slot generation failed: {last_err}")
    n = course_n if isinstance(course_n, int) else 5
    return [
        {"position": i + 1, "slot_name": f"course_{i + 1}",
         "slot_role": "course", "typical_temperature": "warm", "notes": ""}
        for i in range(n)
    ]


def _enrich_invention_lineage(invention, cur):
    """
    Resolve lineage ID lists to dicts with id/name (and slug for techniques).
    Replaces the raw ID lists on the invention dict in-place and returns it.
    beverage_references have no public page route — name only, no URL.
    """
    def resolve_techniques(id_list):
        if not id_list:
            return []
        cur.execute(
            "SELECT id, name, slug FROM technique_references WHERE id = ANY(%s)",
            (id_list,)
        )
        by_id = {r['id']: dict(r) for r in cur.fetchall()}
        return [by_id[i] for i in id_list if i in by_id]

    def resolve_ingredients(id_list):
        if not id_list:
            return []
        cur.execute(
            "SELECT id, name FROM ingredient_products WHERE id = ANY(%s)",
            (id_list,)
        )
        by_id = {r['id']: dict(r) for r in cur.fetchall()}
        return [by_id[i] for i in id_list if i in by_id]

    def resolve_beverages(id_list):
        if not id_list:
            return []
        cur.execute(
            """SELECT bp.id, bp.name, br.name AS region
               FROM beverage_products bp
               LEFT JOIN beverage_regions br ON br.id = bp.region_id
               WHERE bp.id = ANY(%s) AND bp.is_published IS TRUE""",
            (id_list,)
        )
        by_id = {r['id']: dict(r) for r in cur.fetchall()}
        return [by_id[i] for i in id_list if i in by_id]

    invention['lineage_techniques']  = resolve_techniques(invention.get('lineage_techniques')  or [])
    invention['lineage_ingredients'] = resolve_ingredients(invention.get('lineage_ingredients') or [])
    invention['lineage_beverages']   = resolve_beverages(invention.get('lineage_beverages')    or [])
    return invention


def _atelier_build_slot_prompt(slot, slot_index, slot_count, canon, brief_parsed, pools):
    techniques_str = "\n".join(
        f"  [id={t['id']}] {t['name']} — {(t.get('description') or '')[:100]}"
        for t in pools["techniques"]
    ) or "  (none available)"

    ingredients_str = "\n".join(
        f"  [id={i['id']}] {i['name']} — {(i.get('description') or '')[:80]}"
        for i in pools["ingredients"]
    ) or "  (none available)"

    beverages_str = "\n".join(
        f"  [id={b['id']}] {b['name']} ({(b.get('origin') or '')[:60]})"
        for b in pools["beverages"]
    ) or "  (none available)"

    return (
        f"You are composing one course of a {canon['menu_format_type']} menu, "
        f"anchored to the canon \"{canon['name']}\".\n\n"
        "VOICE: Short active sentences. Second person where natural. Present tense. "
        "Chef-to-peer prose. No marketing language. No AI reference. Examination depth.\n\n"
        "SLOT TO FILL\n"
        f"  Position: course {slot_index + 1} of {slot_count}\n"
        f"  Slot name: {slot.get('slot_name', 'unnamed')}\n"
        f"  Slot role: {slot.get('slot_role', 'not specified')}\n"
        f"  Temperature register: {slot.get('typical_temperature', 'unspecified')}\n"
        f"  Liturgical rule: {slot.get('liturgical_rule') or 'none'}\n"
        f"  Canon notes: {slot.get('notes', '')}\n\n"
        "USER BRIEF\n"
        f"{json.dumps(brief_parsed, indent=2, ensure_ascii=False)}\n\n"
        "REAL-COMPONENTS RULE (HARD CONSTRAINT)\n"
        "Select ONLY from the numbered pools below. Reference by integer id.\n"
        "Any id outside the pools will be rejected and the slot retried.\n"
        "You may include zero beverages if none fit the slot.\n\n"
        f"AVAILABLE TECHNIQUES (pick 1–3 central to this course)\n{techniques_str}\n\n"
        f"AVAILABLE INGREDIENTS (pick 2–6 that define this course)\n{ingredients_str}\n\n"
        f"AVAILABLE BEVERAGES (pick 0–2 that pair with this course)\n{beverages_str}\n\n"
        "OUTPUT: Return ONE JSON object. No markdown fence. No prose before or after.\n\n"
        "{\n"
        '  "name": "Course name in Provenance voice — specific, not generic",\n'
        '  "description": "2–4 sentences. Name the technique, cut/temperature/time, '
        'and the moment where the dish lives or dies.",\n'
        '  "lineage_techniques": [<integer ids from techniques pool>],\n'
        '  "lineage_ingredients": [<integer ids from ingredients pool>],\n'
        '  "lineage_beverages": [<integer ids from beverages pool, may be empty list>]\n'
        "}"
    )


def _atelier_compose_slot(slot, slot_index, slot_count, canon, brief_parsed, pools, valid_pools=None):
    """
    Compose one Invention for one slot via Haiku 4.5.
    Mirrors HACCP retry: MAX_ATTEMPTS=2, fence strip, 1s sleep on retryable failure.
    Validates real-components rule before returning.
    Raises RuntimeError after exhaustion.

    pools       — displayed candidate list (may be filtered to exclude already-used items)
    valid_pools — full original pool used for ID validation; defaults to pools if not provided
    """
    if valid_pools is None:
        valid_pools = pools
    # Use full cuisine technique set when available (wider than the shown sample)
    _full_ids = valid_pools.get("_all_cuisine_technique_ids")
    valid_technique_ids = _full_ids if _full_ids is not None else {t["id"] for t in valid_pools["techniques"]}
    valid_ingredient_ids = {i["id"] for i in valid_pools["ingredients"]}
    valid_beverage_ids = {b["id"] for b in valid_pools["beverages"]}

    prompt = _atelier_build_slot_prompt(
        slot, slot_index, slot_count, canon, brief_parsed, pools
    )
    last_error = None

    for attempt in range(1, _ATELIER_COMPOSE_MAX_ATTEMPTS + 1):
        try:
            resp = client.messages.create(
                model=_ATELIER_COMPOSE_MODEL,
                max_tokens=1500,
                timeout=45.0,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()

            # Strip accidental markdown fences (mirrors HACCP)
            if raw.startswith("```"):
                raw = raw.split("```", 2)[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.rsplit("```", 1)[0].strip()

            invention = json.loads(raw)

            if not invention.get("name"):
                raise ValueError("missing 'name'")
            if not invention.get("description"):
                raise ValueError("missing 'description'")

            invention.setdefault("lineage_techniques", [])
            invention.setdefault("lineage_ingredients", [])
            invention.setdefault("lineage_beverages", [])

            # Real-components rule — hard check
            for tid in invention["lineage_techniques"]:
                if tid not in valid_technique_ids:
                    raise ValueError(f"technique id {tid} not in candidate pool")
            for iid in invention["lineage_ingredients"]:
                if iid not in valid_ingredient_ids:
                    raise ValueError(f"ingredient id {iid} not in candidate pool")
            for bid in invention["lineage_beverages"]:
                if bid not in valid_beverage_ids:
                    raise ValueError(f"beverage id {bid} not in candidate pool")

            app.logger.info(
                f"[ATELIER COMPOSE] slot {slot_index + 1} "
                f"attempt {attempt}/{_ATELIER_COMPOSE_MAX_ATTEMPTS} succeeded"
            )
            return invention

        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            app.logger.warning(
                f"[ATELIER COMPOSE] slot {slot_index + 1} "
                f"attempt {attempt}/{_ATELIER_COMPOSE_MAX_ATTEMPTS} failed: "
                f"{type(e).__name__}: {e}"
            )
            if attempt < _ATELIER_COMPOSE_MAX_ATTEMPTS:
                _time.sleep(1)
                continue

        except Exception as e:
            app.logger.error(
                f"[ATELIER COMPOSE] slot {slot_index + 1} non-retryable error: {e}"
            )
            raise

    app.logger.error(
        f"[ATELIER COMPOSE] slot {slot_index + 1} ({slot.get('slot_name')}) "
        f"exhausted {_ATELIER_COMPOSE_MAX_ATTEMPTS} attempts. Last error: {last_error}"
    )
    raise RuntimeError(
        f"Could not compose slot {slot_index + 1} ({slot.get('slot_name')}) "
        f"after {_ATELIER_COMPOSE_MAX_ATTEMPTS} attempts: {last_error}"
    )


def _atelier_compose_inner(user):
    from datetime import datetime

    data = request.get_json() or {}
    brief_parsed   = data.get("brief_parsed") or {}
    canon_entry_id = data.get("canon_entry_id")   # None unless explicitly supplied
    app.logger.info(f"[ATELIER DIAG] parsed_brief = {brief_parsed}")

    # ── 1. Resolve canon / slot structure (Mode A / B / C) ───────────────────
    conn = get_db()
    cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if canon_entry_id:
        # Mode A — explicit canon_id supplied
        compose_mode = "canon_anchored"
        cur.execute(
            """SELECT id, name, origin, description,
                      menu_format_type, canon_tier, course_slots
               FROM technique_references WHERE id = %s""",
            (int(canon_entry_id),),
        )
        canon_row = cur.fetchone()
        cur.close(); conn.close()
        if not canon_row:
            return jsonify(error=f"canon entry {canon_entry_id} not found"), 404
        canon = dict(canon_row)
        if not canon.get("course_slots"):
            return jsonify(error=f"canon entry {canon_entry_id} has no course_slots"), 400
        course_slots = canon["course_slots"]

    else:
        # Mode B — try rules-based matcher
        matched_id, matched_name = _match_canon_for_brief(brief_parsed, cur)
        app.logger.info(f"[ATELIER DIAG] canon_match: id={matched_id} name={matched_name}")

        if matched_id:
            compose_mode = "canon_anchored"
            cur.execute(
                """SELECT id, name, origin, description,
                          menu_format_type, canon_tier, course_slots
                   FROM technique_references WHERE id = %s""",
                (matched_id,),
            )
            canon = dict(cur.fetchone())
            course_slots = canon["course_slots"]
            cur.close(); conn.close()
        else:
            cur.close(); conn.close()
            # Mode C — free-form: synthesise slot structure with Haiku
            compose_mode = "free_form"
            canon = {
                "id":               None,
                "name":             (brief_parsed.get("primary_cuisine") or "Contemporary").title(),
                "origin":           brief_parsed.get("current_location") or "",
                "description":      "",
                "menu_format_type": brief_parsed.get("menu_format_hint") or "tasting_menu",
                "canon_tier":       None,
                "course_slots":     None,
            }
            course_slots = _generate_freeform_slots(brief_parsed)
            canon["course_slots"] = course_slots

    print(
        f"[ATELIER COMPOSE] mode={compose_mode} canon_id={canon.get('id')} "
        f"name={canon['name'][:40]!r} slots={len(course_slots)} "
        f"format={canon.get('menu_format_type')}",
        flush=True,
    )

    # ── 2. Build candidate pools ──────────────────────────────────────────────
    pools = _build_candidate_pools_for_canon(canon, parsed_brief=brief_parsed)
    app.logger.info(
        f"[ATELIER COMPOSE] pools: {len(pools['techniques'])} techniques, "
        f"{len(pools['ingredients'])} ingredients, "
        f"{len(pools['beverages'])} beverages"
    )

    # ── 3. Insert Composition row ─────────────────────────────────────────────
    occasion    = (brief_parsed.get("occasion_type") or "").replace("_", " ").title()
    today_str   = datetime.now().strftime("%-d %b %Y")
    canon_label = canon["name"][:40]
    comp_title  = (
        f"Composition · {occasion or canon_label} · {today_str}".strip(" ·")
    )
    based_on_id = canon.get("id")  # None for free_form

    conn = get_db()
    cur  = conn.cursor()
    cur.execute(
        """INSERT INTO compositions
             (user_id, title, brief_parsed, based_on_canon_id, output_shape, status)
           VALUES (%s, %s, %s::jsonb, %s, 'menu', 'draft')
           RETURNING id""",
        (user["id"], comp_title, json.dumps(brief_parsed), based_on_id),
    )
    composition_id = cur.fetchone()[0]
    cur.close(); conn.close()

    print(f"[ATELIER COMPOSE] composition_id={composition_id} title={comp_title!r}", flush=True)

    # ── 4. Compose each slot → Invention → composition_course ─────────────────
    courses      = []
    enrich_conn  = get_db()
    enrich_cur   = enrich_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    used_technique_ids  = set()
    used_ingredient_ids = set()

    for slot_index, slot in enumerate(course_slots):
        print(
            f"[ATELIER COMPOSE] slot {slot_index + 1}/{len(course_slots)}: "
            f"{slot.get('slot_name')}",
            flush=True,
        )

        remaining_slots = len(course_slots) - slot_index
        # Only filter when there is enough depth; late courses fall back to full pool.
        filtered_techniques  = [t for t in pools["techniques"]  if t["id"] not in used_technique_ids]
        filtered_ingredients = [i for i in pools["ingredients"] if i["id"] not in used_ingredient_ids]
        use_filtered = (
            len(filtered_techniques)  > remaining_slots * 3 and
            len(filtered_ingredients) > remaining_slots * 2
        )
        slot_pools = {
            "techniques":  filtered_techniques  if use_filtered else pools["techniques"],
            "ingredients": filtered_ingredients if use_filtered else pools["ingredients"],
            "beverages":   pools["beverages"],
            "_keywords":   pools.get("_keywords", []),
        }

        try:
            invention = _atelier_compose_slot(
                slot=slot,
                slot_index=slot_index,
                slot_count=len(course_slots),
                canon=canon,
                brief_parsed=brief_parsed,
                pools=slot_pools,
                valid_pools=pools,
            )

            used_technique_ids.update(invention.get("lineage_techniques", []))
            used_ingredient_ids.update(invention.get("lineage_ingredients", []))

            # Persist Invention then link via composition_course
            conn2 = get_db()
            cur2  = conn2.cursor()
            cur2.execute(
                """INSERT INTO user_inventions
                     (user_id, name, description,
                      derived_from_techniques, derived_from_ingredients,
                      derived_from_beverages, composed_by_brief_id)
                   VALUES (%s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s)
                   RETURNING id""",
                (
                    user["id"],
                    invention["name"],
                    invention["description"],
                    json.dumps(invention.get("lineage_techniques", [])),
                    json.dumps(invention.get("lineage_ingredients", [])),
                    json.dumps(invention.get("lineage_beverages", [])),
                    composition_id,
                ),
            )
            invention_id = cur2.fetchone()[0]

            # XOR constraint: recipe_id must be NULL when invention_id is set
            cur2.execute(
                """INSERT INTO composition_courses
                     (composition_id, position, slot_name, slot_role, invention_id, recipe_id)
                   VALUES (%s, %s, %s, %s, %s, NULL)""",
                (
                    composition_id,
                    slot_index + 1,
                    slot.get("slot_name"),
                    slot.get("slot_role"),
                    invention_id,
                ),
            )
            cur2.close(); conn2.close()

            # Enrich lineage: replace raw ID lists with dicts {id, name, slug}
            _enrich_invention_lineage(invention, enrich_cur)

            # Augment lineage_ingredients via Haiku if signature overlap is low
            if _ingredient_signature_overlap(invention) < INGREDIENT_AUGMENTATION_THRESHOLD:
                _augment_ingredients_via_haiku(invention, brief_parsed, enrich_cur)

            # Match a curated library recipe for this slot (may be None)
            library_recipe = _match_library_recipe_for_slot(slot, brief_parsed, enrich_cur, invention=invention)

            courses.append(
                {
                    "position":            slot_index + 1,
                    "slot_name":           slot.get("slot_name"),
                    "slot_role":           slot.get("slot_role"),
                    "invention_id":        invention_id,
                    "name":                invention["name"],
                    "description":         invention["description"],
                    "lineage_techniques":  invention.get("lineage_techniques", []),
                    "lineage_ingredients": invention.get("lineage_ingredients", []),
                    "lineage_beverages":   invention.get("lineage_beverages", []),
                    "library_recipe":      library_recipe,
                }
            )

        except Exception as _slot_err:
            app.logger.error(
                f"[ATELIER COMPOSE] slot {slot_index + 1} ({slot.get('slot_name')}) "
                f"failed — inserting draft slot: {_slot_err}"
            )
            try:
                conn_d = get_db()
                cur_d  = conn_d.cursor()
                cur_d.execute(
                    """INSERT INTO composition_courses
                         (composition_id, position, slot_name, slot_role, invention_id, recipe_id)
                       VALUES (%s, %s, %s, %s, NULL, NULL)""",
                    (composition_id, slot_index + 1, slot.get("slot_name"), slot.get("slot_role")),
                )
                cur_d.close(); conn_d.close()
            except Exception:
                pass
            courses.append({
                "position":            slot_index + 1,
                "slot_name":           slot.get("slot_name"),
                "slot_role":           slot.get("slot_role"),
                "is_draft":            True,
                "name":                "Open course — awaiting a library match.",
                "description":         "",
                "lineage_techniques":  [],
                "lineage_ingredients": [],
                "lineage_beverages":   [],
                "library_recipe":      None,
            })

    enrich_cur.close(); enrich_conn.close()

    print(
        f"[ATELIER COMPOSE] complete. composition_id={composition_id} "
        f"courses={len(courses)}",
        flush=True,
    )

    return jsonify(
        composition_id=composition_id,
        title=comp_title,
        compose_mode=compose_mode,
        canon_name=canon["name"],
        based_on_canon_id=based_on_id,
        menu_format_type=canon.get("menu_format_type"),
        slot_count=len(courses),
        courses=courses,
    )


@app.route("/api/atelier/compose", methods=["POST"])
def atelier_compose():
    print("[ATELIER COMPOSE] route entered", flush=True)
    user = get_current_user()
    if not user:
        return jsonify(error="Login required"), 401
    try:
        return _atelier_compose_inner(user)
    except Exception as _outer:
        app.logger.error(f"[ATELIER COMPOSE] unhandled: {_outer}", exc_info=True)
        return jsonify(error="The composer is busy right now — try again in a moment."), 503


def _compose_course_recipe_body(name, description, techniques, ingredients, covers=None):
    """
    One Haiku call: compose a professional recipe body grounded in real lineage components.
    techniques: list of {name, key_principles, pro_tips}
    ingredients: list of {canonical_name, category}
    Returns {ingredients: [...dicts...], steps: [...strings...]} or {} on failure.
    """
    covers_note = f"Scale for {covers} covers." if covers else "Scale for 4 covers."

    technique_block = ""
    if techniques:
        parts = []
        for t in techniques:
            line = t["name"]
            if t.get("key_principles"):
                line += f" — {str(t['key_principles'])[:120]}"
            parts.append(line)
        technique_block = "TECHNIQUES TO APPLY:\n" + "\n".join(f"- {p}" for p in parts)

    ingredient_block = ""
    if ingredients:
        names = [i["canonical_name"] for i in ingredients]
        ingredient_block = "CORE INGREDIENTS (use these; ordinary pantry staples are also fine):\n" + "\n".join(f"- {n}" for n in names)

    prompt = (
        f"You are composing a professional kitchen recipe for a chef's personal collection. "
        f"Institutional register. No superlatives. No food-magazine prose.\n\n"
        f"COURSE: {name}\n"
        f"CONCEPT: {description}\n\n"
        f"{technique_block}\n\n"
        f"{ingredient_block}\n\n"
        f"RULES:\n"
        f"- {covers_note}\n"
        f"- Build from the named techniques and core ingredients above.\n"
        f"- Ordinary pantry staples (salt, oil, butter, flour, stock, aromatics) are fine.\n"
        f"- Do NOT invent exotic, branded, or obscure items not derivable from the listed ingredients.\n"
        f"- ingredients array: each item has count (number or weight as string), unit, name, info (prep note).\n"
        f"- steps array: ordered method strings that apply the named techniques. Professional but clear.\n"
        f"- Aim for 6–14 ingredients; 4–8 steps.\n\n"
        f"Return ONE JSON object. No markdown fence. No prose before or after.\n"
        f'{{\n'
        f'  "ingredients": [\n'
        f'    {{"count": "200", "unit": "g", "name": "jasmine rice", "info": "rinsed"}}\n'
        f'  ],\n'
        f'  "steps": [\n'
        f'    "Bring 400 ml water to a rolling boil in a heavy-based saucepan."\n'
        f'  ]\n'
        f'}}'
    )

    last_err = None
    for attempt in range(1, _ATELIER_COMPOSE_MAX_ATTEMPTS + 1):
        try:
            resp = client.messages.create(
                model=_ATELIER_COMPOSE_MODEL,
                max_tokens=1800,
                timeout=45.0,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```", 2)[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.rsplit("```", 1)[0].strip()
            body = json.loads(raw)
            if not body.get("ingredients") or not body.get("steps"):
                raise ValueError("missing ingredients or steps in response")
            return body
        except Exception as e:
            last_err = e
            app.logger.warning(f"[_compose_course_recipe_body] attempt {attempt} failed: {e}")
            if attempt < _ATELIER_COMPOSE_MAX_ATTEMPTS:
                _time.sleep(1)

    app.logger.error(
        f"[_compose_course_recipe_body] {name!r}: exhausted {_ATELIER_COMPOSE_MAX_ATTEMPTS} attempts — {last_err}"
    )
    return {}


def _create_kitchen_recipe_from_invention(invention, owner_user_id, write_cur):
    """Insert a user_kitchen_recipes row from a user_invention dict. Returns the uuid string."""
    new_uuid = str(uuid.uuid4())
    slug = make_kitchen_slug(invention.get("name") or "draft", new_uuid)
    suffix = 2
    while True:
        write_cur.execute("SELECT 1 FROM user_kitchen_recipes WHERE slug = %s", (slug,))
        if not write_cur.fetchone():
            break
        slug = f"{make_kitchen_slug(invention.get('name') or 'draft', new_uuid)}-{suffix}"
        suffix += 1
    write_cur.execute("""
        INSERT INTO user_kitchen_recipes
            (uuid, user_id, title, slug, preamble, origin, flavour_context,
             lives_or_dies, quality_hierarchy, sensory_tests, is_draft)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
    """, (
        new_uuid,
        owner_user_id,
        invention.get("name") or "Untitled draft",
        slug,
        invention.get("description") or "",
        invention.get("origin") or "",
        invention.get("flavour_context") or "",
        invention.get("lives_or_dies") or "",
        json.dumps(invention.get("quality_hierarchy") or {}),
        json.dumps(invention.get("sensory_tests") or []),
    ))
    return new_uuid


def _resolve_course_recipe_ref(course, invention, owner_user_id, read_cur, write_cur):
    """
    Returns the recipe_ref string for a composition_course row.
    Canon (recipe_id set)  → "technique:<slug>" — resolved via technique_references.
    Draft (invention_id set) → inserts a kitchen recipe, returns "kitchen:<uuid>".
    """
    if course.get("recipe_id"):
        read_cur.execute(
            "SELECT slug FROM technique_references WHERE id = %s", (course["recipe_id"],)
        )
        row = read_cur.fetchone()
        slug = row["slug"] if row and row.get("slug") else str(course["recipe_id"])
        return f"technique:{slug}"
    else:
        new_uuid = _create_kitchen_recipe_from_invention(invention, owner_user_id, write_cur)
        return f"kitchen:{new_uuid}"


@app.route("/api/atelier/promote", methods=["POST"])
def atelier_promote():
    user = get_current_user()
    if not user:
        return jsonify(error="Login required"), 401
    if not gate_for_addon("atelier"):
        return jsonify(error="Reserve add-on required"), 403

    data = request.get_json() or {}
    composition_id = data.get("composition_id")
    if not composition_id:
        return jsonify(error="composition_id required"), 400

    if not DATABASE_URL_WRITE:
        return jsonify(error="Write DB unavailable"), 503

    # ── Read phase ────────────────────────────────────────────────────────────
    read_conn = psycopg2.connect(DATABASE_URL)
    read_conn.autocommit = True
    read_cur = read_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        read_cur.execute(
            "SELECT * FROM compositions WHERE id = %s AND user_id = %s",
            (int(composition_id), user["id"])
        )
        comp = read_cur.fetchone()
        if not comp:
            return jsonify(error="Composition not found or not yours"), 404

        read_cur.execute("""
            SELECT cc.*,
                   ui.name      AS inv_name,
                   ui.description AS inv_desc,
                   ui.origin    AS inv_origin,
                   ui.flavour_context AS inv_flavour,
                   ui.lives_or_dies   AS inv_lives_or_dies,
                   ui.quality_hierarchy AS inv_quality_hierarchy,
                   ui.sensory_tests    AS inv_sensory_tests
            FROM composition_courses cc
            LEFT JOIN user_inventions ui ON ui.id = cc.invention_id
            WHERE cc.composition_id = %s
            ORDER BY cc.position
        """, (int(composition_id),))
        courses = [dict(r) for r in read_cur.fetchall()]
    finally:
        read_cur.close()
        read_conn.close()

    if not courses:
        return jsonify(error="Composition has no courses"), 400

    # ── Write phase — single transaction ──────────────────────────────────────
    write_conn = psycopg2.connect(DATABASE_URL_WRITE)
    write_cur = write_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    read_conn2 = psycopg2.connect(DATABASE_URL)
    read_conn2.autocommit = True
    read_cur2 = read_conn2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        slug_base = (_slugify(comp["title"]) or "menu")[:80]
        menu_slug = _menu_slug_unique(slug_base, read_cur2)

        write_cur.execute("""
            INSERT INTO menus (slug, owner_user_id, title)
            VALUES (%s, %s, %s)
            RETURNING id, slug
        """, (menu_slug, user["id"], comp["title"]))
        menu_row = write_cur.fetchone()
        menu_id = menu_row["id"]

        kitchen_courses = []  # [{kitchen_uuid, invention_id}] for per-course recipe composition
        for course in courses:
            invention = None
            if course.get("invention_id"):
                invention = {
                    "name": course.get("inv_name") or course.get("slot_name") or "Draft course",
                    "description": course.get("inv_desc") or "",
                    "origin": course.get("inv_origin") or "",
                    "flavour_context": course.get("inv_flavour") or "",
                    "lives_or_dies": course.get("inv_lives_or_dies") or "",
                    "quality_hierarchy": course.get("inv_quality_hierarchy"),
                    "sensory_tests": course.get("inv_sensory_tests"),
                }
            recipe_ref = _resolve_course_recipe_ref(
                course, invention, user["id"], read_cur2, write_cur
            )
            if recipe_ref.startswith("kitchen:"):
                ku = recipe_ref[len("kitchen:"):]
                kitchen_courses.append({
                    "kitchen_uuid": ku,
                    "invention_id": course["invention_id"],
                })
            course_name = (
                course.get("slot_role") or course.get("slot_name")
                or f"Course {course['position']}"
            )
            write_cur.execute("""
                INSERT INTO menu_recipes (menu_id, recipe_ref, course_name, course_order)
                VALUES (%s, %s, %s, %s)
            """, (menu_id, recipe_ref, course_name, int(course["position"])))

        write_conn.commit()
        return jsonify(menu_id=str(menu_id), menu_slug=menu_slug,
                       kitchen_courses=kitchen_courses), 201

    except Exception as e:
        write_conn.rollback()
        app.logger.error(f"[ATELIER PROMOTE] failed: {e}")
        return jsonify(error="Promote failed", detail=str(e)), 500
    finally:
        write_cur.close()
        write_conn.close()
        read_cur2.close()
        read_conn2.close()


@app.route("/api/atelier/write-course-recipe", methods=["POST"])
def atelier_write_course_recipe():
    """
    Compose a full recipe body (ingredients + steps + seven pillars) for one atelier course.
    Called per-course after promote so no single request times out.
    Writes ONLY to user_kitchen_recipes (UPDATE — row already exists from promote).
    Never touches the public recipes table.
    """
    user = get_current_user()
    if not user:
        return jsonify(error="Login required"), 401

    data = request.get_json() or {}
    kitchen_uuid = data.get("kitchen_uuid")
    invention_id = data.get("invention_id")

    if not kitchen_uuid or not invention_id:
        return jsonify(error="kitchen_uuid and invention_id required"), 400

    if not DATABASE_URL_WRITE:
        return jsonify(error="Write DB unavailable"), 503

    # ── 1. Read invention + verify kitchen recipe ownership ───────────────────
    read_conn = psycopg2.connect(DATABASE_URL)
    read_conn.autocommit = True
    read_cur = read_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        read_cur.execute(
            "SELECT * FROM user_inventions WHERE id = %s AND user_id = %s",
            (int(invention_id), user["id"])
        )
        inv_row = read_cur.fetchone()
        if not inv_row:
            return jsonify(error="Invention not found or not yours"), 404
        invention = dict(inv_row)

        read_cur.execute(
            "SELECT uuid, title FROM user_kitchen_recipes WHERE uuid = %s AND user_id = %s",
            (kitchen_uuid, user["id"])
        )
        kitchen_row = read_cur.fetchone()
        if not kitchen_row:
            return jsonify(error="Kitchen recipe not found or not yours"), 404

        # ── 2. Resolve real component names from lineage ──────────────────────
        technique_ids = invention.get("derived_from_techniques") or []
        ingredient_ids = invention.get("derived_from_ingredients") or []

        techniques = []
        if technique_ids:
            read_cur.execute(
                """SELECT name, key_principles, pro_tips
                   FROM technique_references WHERE id = ANY(%s)""",
                (technique_ids,)
            )
            techniques = [dict(r) for r in read_cur.fetchall()]

        ingredients_lineage = []
        if ingredient_ids:
            read_cur.execute(
                "SELECT canonical_name, category FROM ingredient_master WHERE id = ANY(%s)",
                (ingredient_ids,)
            )
            ingredients_lineage = [dict(r) for r in read_cur.fetchall()]

        # Covers from the originating composition's brief
        covers = None
        if invention.get("composed_by_brief_id"):
            read_cur.execute(
                "SELECT brief_parsed FROM compositions WHERE id = %s",
                (invention["composed_by_brief_id"],)
            )
            comp_row = read_cur.fetchone()
            if comp_row and comp_row.get("brief_parsed"):
                covers = comp_row["brief_parsed"].get("covers")
    finally:
        read_cur.close()
        read_conn.close()

    # ── 3. Compose recipe body ─────────────────────────────────────────────────
    body = _compose_course_recipe_body(
        name=invention["name"],
        description=invention.get("description") or "",
        techniques=techniques,
        ingredients=ingredients_lineage,
        covers=covers,
    )
    if not body:
        return jsonify(error="Recipe body composition failed — try again in a moment."), 503

    ingredients = body.get("ingredients", [])
    steps = body.get("steps", [])

    # ── 4. Build ingredient strings for enrichment functions ──────────────────
    ingredient_strings = []
    for ing in ingredients:
        if isinstance(ing, dict):
            parts = [str(ing.get("count") or ""), ing.get("unit") or "", ing.get("name") or ""]
            info = ing.get("info") or ""
            parts = [p for p in parts if p]
            line = " ".join(parts)
            if info:
                line += f" ({info})"
            ingredient_strings.append(line.strip())
        else:
            ingredient_strings.append(str(ing))

    ingredients_text = "\n".join(f"- {s}" for s in ingredient_strings)
    steps_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
    title = invention["name"]

    # ── 5. Run enrichment pipeline ────────────────────────────────────────────
    enhanced_steps = []
    try:
        enhanced_steps = _add_step_insights(title, ingredient_strings, steps)
    except Exception as _e:
        app.logger.warning(f"[WRITE_COURSE_RECIPE] step insights failed for {title!r}: {_e}")

    structure = {}
    try:
        structure = _enhance_recipe_structure(title, ingredients_text, steps_text)
    except Exception as _e:
        app.logger.warning(f"[WRITE_COURSE_RECIPE] structure failed for {title!r}: {_e}")

    pairings = []
    try:
        pairings = _enrich_beverage_pairings(title, ingredients_text)
    except Exception as _e:
        app.logger.warning(f"[WRITE_COURSE_RECIPE] pairings failed for {title!r}: {_e}")

    # ── 6. UPDATE user_kitchen_recipes (never touches public recipes table) ───
    write_conn = psycopg2.connect(DATABASE_URL_WRITE)
    write_cur = write_conn.cursor()
    try:
        write_cur.execute("""
            UPDATE user_kitchen_recipes
            SET ingredients              = %s::jsonb,
                steps                    = %s::jsonb,
                original_steps           = %s::jsonb,
                enhanced_steps           = %s::jsonb,
                origin                   = COALESCE(NULLIF(%s, ''), origin),
                quality_hierarchy        = %s::jsonb,
                sensory_tests            = %s::jsonb,
                cross_cuisine_parallels  = %s::jsonb,
                flavour_context          = COALESCE(NULLIF(%s, ''), flavour_context),
                lives_or_dies            = COALESCE(NULLIF(%s, ''), lives_or_dies),
                quality_warnings         = %s::jsonb,
                ingredient_origin_markers = %s::jsonb,
                beverage_pairings        = %s::jsonb,
                updated_at               = NOW()
            WHERE uuid = %s AND user_id = %s
        """, (
            json.dumps(ingredients),
            json.dumps(steps),
            json.dumps(steps),           # original_steps verbatim
            json.dumps(enhanced_steps),
            structure.get("origin") or invention.get("origin") or "",
            json.dumps(structure["quality_hierarchy"]) if structure.get("quality_hierarchy") else None,
            json.dumps(structure["sensory_tests"]) if structure.get("sensory_tests") else None,
            json.dumps(structure["cross_cuisine_parallels"]) if structure.get("cross_cuisine_parallels") else None,
            structure.get("flavour_context") or invention.get("flavour_context") or "",
            structure.get("lives_or_dies") or invention.get("lives_or_dies") or "",
            json.dumps(structure.get("quality_warnings") or []),
            json.dumps(structure.get("ingredient_origin_markers") or []),
            json.dumps(pairings) if pairings else None,
            kitchen_uuid,
            user["id"],
        ))
        write_conn.commit()
        app.logger.info(
            f"[WRITE_COURSE_RECIPE] completed: kitchen_uuid={kitchen_uuid} "
            f"title={title!r} ingredients={len(ingredients)} steps={len(steps)}"
        )
    except Exception as e:
        write_conn.rollback()
        app.logger.error(f"[WRITE_COURSE_RECIPE] db write failed: {e}")
        return jsonify(error="Write failed", detail=str(e)), 500
    finally:
        write_cur.close()
        write_conn.close()

    return jsonify(ok=True, kitchen_uuid=kitchen_uuid), 200


@app.route("/atelier")
def atelier():
    user = get_current_user()
    if not user:
        return _login_redirect()
    has_addon = gate_for_addon("atelier")
    return render_template("atelier.html", has_addon=has_addon, user=user)


# ─── Admin — Pairing review queue ────────────────────────────────────────────
# TODO: migrate gate to a Trade-tier permission check once that column exists.

@app.route("/admin/pairings")
def admin_pairings():
    g = _admin_guard()
    if g:
        return g
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bps.id, bps.recipe_ref, bps.source_tier, bps.role,
               bps.descriptor, bps.match_score, bps.match_reasoning,
               bps.status, bps.suggested_at,
               bp.name AS beverage_name, bp.slug AS beverage_slug,
               bp.category AS beverage_category,
               bpr.name AS producer_name
        FROM beverage_pairing_suggestions bps
        JOIN beverage_products bp ON bp.id = bps.beverage_product_id
        LEFT JOIN beverage_producers bpr ON bpr.id = bp.producer_id
        WHERE bps.status = 'pending'
        ORDER BY bps.recipe_ref, bps.match_score DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Group by recipe_ref for template display
    from collections import OrderedDict
    grouped = OrderedDict()
    for row in rows:
        ref = row["recipe_ref"]
        if ref not in grouped:
            grouped[ref] = []
        grouped[ref].append(row)

    return render_template("admin_pairings.html", grouped=grouped)


@app.route("/admin/pairings/<uuid:suggestion_id>/approve", methods=["POST"])
def admin_pairings_approve(suggestion_id):
    g = _admin_guard_api()
    if g:
        return g
    if not DATABASE_URL_WRITE:
        return jsonify(error="no write DB"), 503
    user_id = session.get("user_id")
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT bps.*, bp.name AS beverage_name, bp.category AS beverage_category,
               bpr.name AS producer_name
        FROM beverage_pairing_suggestions bps
        JOIN beverage_products bp ON bp.id = bps.beverage_product_id
        LEFT JOIN beverage_producers bpr ON bpr.id = bp.producer_id
        WHERE bps.id = %s
    """, (str(suggestion_id),))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        return jsonify(error="suggestion not found"), 404
    if row["status"] != "pending":
        cur.close(); conn.close()
        return jsonify(error="already decided"), 409

    recipe_ref = row["recipe_ref"]
    pairing_entry = {
        "name": f"{row['producer_name'] + ' ' if row['producer_name'] else ''}{row['beverage_name']}".strip(),
        "category": (row["beverage_category"] or "").lower().replace(" ", "_"),
        "pairing_type": (row["role"] or "complement").lower(),
        "tasting_note": row["descriptor"] or "",
    }

    write_conn = psycopg2.connect(DATABASE_URL_WRITE)
    write_cur = write_conn.cursor()
    if recipe_ref.startswith("canon:"):
        slug = recipe_ref[len("canon:"):]
        write_cur.execute("""
            UPDATE recipes
            SET pairings = COALESCE(pairings, '[]'::jsonb) || %s::jsonb
            WHERE slug = %s
        """, (json.dumps([pairing_entry]), slug))
    elif recipe_ref.startswith("kitchen:"):
        ukr_id = recipe_ref[len("kitchen:"):]
        write_cur.execute("""
            UPDATE user_kitchen_recipes
            SET beverage_pairings = COALESCE(beverage_pairings, '[]'::jsonb) || %s::jsonb
            WHERE id = %s OR slug = %s
        """, (json.dumps([pairing_entry]), ukr_id, ukr_id))
    write_conn.commit()
    write_cur.close()
    write_conn.close()

    cur.execute("""
        UPDATE beverage_pairing_suggestions
        SET status = 'approved', reviewed_at = NOW(), reviewed_by = %s
        WHERE id = %s
    """, (user_id, str(suggestion_id)))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(ok=True, recipe_ref=recipe_ref)


@app.route("/admin/pairings/<uuid:suggestion_id>/reject", methods=["POST"])
def admin_pairings_reject(suggestion_id):
    g = _admin_guard_api()
    if g:
        return g
    user_id = session.get("user_id")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE beverage_pairing_suggestions
        SET status = 'rejected', reviewed_at = NOW(), reviewed_by = %s
        WHERE id = %s AND status = 'pending'
    """, (user_id, str(suggestion_id)))
    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if not affected:
        return jsonify(error="suggestion not found or already decided"), 404
    return jsonify(ok=True)


# ─── Atelier ingredient review desk ──────────────────────────────────────────

@app.route("/admin/review/ingredients")
def admin_review_ingredients():
    user = get_current_user()
    if not user or user.get("role") not in ("founder", "admin"):
        return redirect("/")
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT id, name, category, origin_country, model_version, prompt_version, created_at
        FROM ingredient_products
        WHERE source = 'ai-augmented'
          AND COALESCE(review_status, 'pending') = 'pending'
        ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    cur.close(); conn.close()
    return render_template("admin_review_ingredients.html", rows=rows)


@app.route("/admin/review/ingredients/<int:ingredient_id>/approve", methods=["POST"])
def admin_review_ingredients_approve(ingredient_id):
    user = get_current_user()
    if not user or user.get("role") not in ("founder", "admin"):
        return jsonify(error="forbidden"), 403
    if not DATABASE_URL_WRITE:
        return jsonify(error="no write DB"), 503
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE ingredient_products
            SET validated = true, review_status = 'approved', updated_at = NOW()
            WHERE id = %s AND source = 'ai-augmented'
        """, (ingredient_id,))
        affected = cur.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close(); conn.close()
        app.logger.error(f"[REVIEW INGREDIENTS] approve {ingredient_id} failed: {e}")
        return jsonify(error="Update failed"), 500
    cur.close(); conn.close()
    if not affected:
        return jsonify(error="ingredient not found or not ai-augmented"), 404
    return redirect("/admin/review/ingredients")


@app.route("/admin/review/ingredients/<int:ingredient_id>/reject", methods=["POST"])
def admin_review_ingredients_reject(ingredient_id):
    user = get_current_user()
    if not user or user.get("role") not in ("founder", "admin"):
        return jsonify(error="forbidden"), 403
    if not DATABASE_URL_WRITE:
        return jsonify(error="no write DB"), 503
    conn = psycopg2.connect(DATABASE_URL_WRITE)
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE ingredient_products
            SET review_status = 'rejected', updated_at = NOW()
            WHERE id = %s AND source = 'ai-augmented'
        """, (ingredient_id,))
        affected = cur.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        cur.close(); conn.close()
        app.logger.error(f"[REVIEW INGREDIENTS] reject {ingredient_id} failed: {e}")
        return jsonify(error="Update failed"), 500
    cur.close(); conn.close()
    if not affected:
        return jsonify(error="ingredient not found or not ai-augmented"), 404
    return redirect("/admin/review/ingredients")


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
