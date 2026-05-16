"""
Unit tests for gate_for_tier() render-state helper.
V4 Sprint 4.1 — tier-gating utility.

Run: pytest tests/test_tier_gating.py
(Use the project venv: source venv/bin/activate)
"""

import os
import sys

# Ensure server.py is importable from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

import server as _server

gate_for_tier = _server.gate_for_tier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user(tier="free", status="inactive", role="user"):
    return {"subscription_tier": tier, "subscription_status": status, "role": role}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGateForTier:

    def test_gate_logged_out_returns_block_for_any_paid_tier(self, monkeypatch):
        """Unauthenticated visitors get gate_block for paid tiers."""
        monkeypatch.setattr(_server, "get_current_user", lambda: None)
        assert gate_for_tier("library") == "gate_block"

    def test_gate_free_tier_always_returns_full_content(self, monkeypatch):
        """free required_tier is always accessible — even logged out."""
        monkeypatch.setattr(_server, "get_current_user", lambda: None)
        assert gate_for_tier("free") == "full_content"

    def test_gate_kitchen_user_against_library_returns_preview_then_prompt(self, monkeypatch):
        """Kitchen subscriber viewing library-gated content gets a preview prompt."""
        monkeypatch.setattr(_server, "get_current_user",
                            lambda: _user("kitchen", "active", "user"))
        assert gate_for_tier("library") == "preview_then_prompt"

    def test_gate_library_user_against_library_returns_full_content(self, monkeypatch):
        """Subscriber at exactly the required tier gets full content."""
        monkeypatch.setattr(_server, "get_current_user",
                            lambda: _user("library", "active", "user"))
        assert gate_for_tier("library") == "full_content"

    def test_gate_profession_user_against_library_returns_full_content(self, monkeypatch):
        """Subscriber above the required tier also gets full content."""
        monkeypatch.setattr(_server, "get_current_user",
                            lambda: _user("profession", "active", "user"))
        assert gate_for_tier("library") == "full_content"

    def test_gate_inactive_subscription_returns_block_even_at_correct_tier(self, monkeypatch):
        """Lapsed subscriber at the right tier still gets gate_block."""
        monkeypatch.setattr(_server, "get_current_user",
                            lambda: _user("library", "inactive", "user"))
        assert gate_for_tier("library") == "gate_block"

    def test_gate_founder_role_bypasses_all_tier_checks(self, monkeypatch):
        """founder role always returns full_content regardless of tier/status."""
        monkeypatch.setattr(_server, "get_current_user",
                            lambda: _user("free", "inactive", "founder"))
        assert gate_for_tier("trade") == "full_content"
