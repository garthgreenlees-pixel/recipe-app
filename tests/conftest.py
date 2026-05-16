"""
Pytest configuration for provenance-tester-1 tests.

Sets DATABASE_URL="" before server.py is imported so that init_db() and
_init_beverage_db() both short-circuit on their `if not DATABASE_URL: return`
guards — preventing any real DB connection during the test run.

load_dotenv() in server.py does NOT override existing env vars, so setting
DATABASE_URL here (before server.py is imported) keeps the empty value.
"""

import os

# Must be set before server.py is imported (and before load_dotenv() runs).
os.environ["DATABASE_URL"] = ""
os.environ["DATABASE_URL_WRITE"] = ""
os.environ["SKIP_INIT_DB"] = "1"
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")
