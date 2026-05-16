"""
Unit tests for /api/stats endpoint.
V4 Sprint 4.6 — public counts with 60-second server-side cache.

Run: pytest tests/test_api_stats.py -v
(Use the project venv: source venv/bin/activate)
"""

import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# conftest.py has already zeroed DATABASE_URL before this module is imported.
import server as _server

app = _server.app

EXPECTED_KEYS = (
    "technique_count",
    "recipe_count",
    "beverage_count",
    "supplier_count",
    "drink_count",
    "canon_count",
    "route_count",
)


def reset_cache():
    """Clear the module-level cache so tests don't bleed into each other."""
    _server._stats_cache["data"] = None
    _server._stats_cache["timestamp"] = 0.0


def _make_conn(fetchone_return=(100,), fail_on_sql=None):
    """
    Build a mock connection whose cursor.fetchone() returns fetchone_return.
    If fail_on_sql is a string, any execute() call whose sql contains that
    string raises an exception (simulates a missing table).
    """
    def _execute(sql, *args):
        if fail_on_sql and fail_on_sql in sql:
            raise Exception(f"simulated DB error for: {sql}")

    cursor = MagicMock()
    cursor.execute.side_effect = _execute
    cursor.fetchone.return_value = fetchone_return

    conn = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestApiStats:

    def test_api_stats_returns_json_with_expected_keys(self):
        """200 OK with all expected count keys in the JSON body."""
        reset_cache()
        conn, _ = _make_conn(fetchone_return=(100,))

        with patch.object(_server, "get_db", return_value=conn), \
             patch.object(_server, "DATABASE_URL", "postgres://fake"):
            with app.test_client() as c:
                resp = c.get("/api/stats")

        assert resp.status_code == 200
        data = resp.get_json()
        assert data is not None, "Response body should parse as JSON"
        for key in EXPECTED_KEYS:
            assert key in data, f"Missing expected key: {key!r}"
        # route_count must be the hardcoded 5 (no DB table)
        assert data["route_count"] == 5

    def test_api_stats_returns_cached_result_on_second_call(self):
        """Second call within TTL must not hit the database again."""
        reset_cache()
        db_call_count = [0]

        def counting_get_db():
            db_call_count[0] += 1
            conn, _ = _make_conn(fetchone_return=(50,))
            return conn

        with patch.object(_server, "get_db", side_effect=counting_get_db), \
             patch.object(_server, "DATABASE_URL", "postgres://fake"):
            with app.test_client() as c:
                c.get("/api/stats")  # populates cache
                c.get("/api/stats")  # must be a cache hit

        assert db_call_count[0] == 1, (
            f"Expected exactly 1 DB call (second should be cache hit), got {db_call_count[0]}"
        )

    def test_api_stats_handles_missing_table_gracefully(self):
        """A broken query on one table must not 500 — that field returns null."""
        reset_cache()
        # Simulate the canons table not existing
        conn, _ = _make_conn(fetchone_return=(42,), fail_on_sql="canons")

        with patch.object(_server, "get_db", return_value=conn), \
             patch.object(_server, "DATABASE_URL", "postgres://fake"):
            with app.test_client() as c:
                resp = c.get("/api/stats")

        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.get_json()
        assert data["canon_count"] is None, (
            "canon_count should be null when its query fails"
        )
        # Other counts should still be populated
        assert data["technique_count"] == 42
        assert data["recipe_count"] == 42
        assert data["route_count"] == 5
