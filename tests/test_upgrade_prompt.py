"""
Unit tests for the upgrade_prompt Jinja macro.
V4 Sprint 4.2 — tier-aware upgrade-prompt component.

Run: pytest tests/test_upgrade_prompt.py -v
(Use the project venv: source venv/bin/activate)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# conftest.py has already zeroed DATABASE_URL before this module is imported.
import server as _server

app = _server.app

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# `with context` is required so the macro can read `current_user` from the
# template context — Jinja macros have isolated scope by default.
TEMPLATE_SRC = (
    "{% from '_partials/upgrade_prompt.html' import upgrade_prompt with context %}"
    "{{ upgrade_prompt(required_tier, context) }}"
)

TEMPLATE_SRC_NO_CONTEXT = (
    "{% from '_partials/upgrade_prompt.html' import upgrade_prompt with context %}"
    "{{ upgrade_prompt(required_tier) }}"
)


def render(required_tier, context=None, current_user=None):
    """Render the macro with the given args and user context.

    Pass current_user to mirror what @app.context_processor injects into
    real templates (key is 'current_user', not 'user').
    """
    src = TEMPLATE_SRC if context is not None else TEMPLATE_SRC_NO_CONTEXT
    tmpl = app.jinja_env.from_string(src)
    kwargs = {"required_tier": required_tier, "current_user": current_user}
    if context is not None:
        kwargs["context"] = context
    return tmpl.render(**kwargs)


def kitchen_user():
    return {"subscription_tier": "kitchen", "subscription_status": "active", "role": "user"}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestUpgradePrompt:

    def test_logged_in_kitchen_user_sees_library_prompt(self):
        """Kitchen user below library tier sees correct door, phrase and pricing link."""
        out = render("library", context="quality_hierarchy", current_user=kitchen_user())
        assert "Open" in out
        assert "The Library" in out
        assert "to read the full Quality Hierarchy" in out
        assert 'href="/pricing#library"' in out

    def test_haccp_context_phrase(self):
        """HACCP context renders the correct phrase and profession door."""
        out = render("profession", context="haccp", current_user=kitchen_user())
        assert "to generate the HACCP brief" in out
        assert "The Profession" in out

    def test_cost_context_phrase(self):
        """Cost context renders the correct phrase."""
        out = render("profession", context="cost", current_user=kitchen_user())
        assert "to cost this recipe" in out

    def test_beverage_context_phrase(self):
        """Beverage context renders the correct phrase."""
        out = render("library", context="beverage", current_user=kitchen_user())
        assert "to see the named producers" in out

    def test_default_context_phrase(self):
        """Omitting context argument falls back to the default phrase."""
        out = render("library", current_user=kitchen_user())
        assert "for full access" in out

    def test_logged_out_links_to_signup_with_tier(self):
        """Logged-out visitor gets a signup link with tier param, not a pricing link."""
        out = render("library", context="quality_hierarchy", current_user=None)
        assert 'href="/auth/signup?tier=library"' in out
        assert "/pricing" not in out

    def test_logged_in_links_to_pricing_with_anchor(self):
        """Logged-in visitor gets a pricing anchor link, not a signup link."""
        out = render("profession", context="haccp", current_user=kitchen_user())
        assert 'href="/pricing#profession"' in out
        assert "/auth/signup" not in out

    def test_voice_check_no_saas_phrases(self):
        """No SaaS/growth-copy language anywhere in any rendering."""
        forbidden = ["Upgrade", "Sign up now", "Get started", "non-negotiable"]
        tiers = ["kitchen", "library", "profession", "trade"]
        contexts = ["haccp", "cost", "beverage", "quality_hierarchy", "default"]
        for tier in tiers:
            for ctx in contexts:
                out = render(tier, context=ctx, current_user=kitchen_user())
                for phrase in forbidden:
                    assert phrase not in out, (
                        f"Forbidden phrase '{phrase}' found in render("
                        f"tier={tier!r}, context={ctx!r})"
                    )
                assert "Open The" in out, (
                    f"Expected 'Open The' pattern missing in render("
                    f"tier={tier!r}, context={ctx!r})"
                )

    def test_unknown_context_falls_back_to_default(self):
        """An unrecognised context key silently falls back to the default phrase."""
        out = render("library", context="made_up_garbage", current_user=kitchen_user())
        assert "for full access" in out
