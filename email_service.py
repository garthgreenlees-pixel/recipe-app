"""
Email service for Provenance — powered by Resend.
Sender: hello@provenance.kitchen

Never raises to caller. All failures are logged.
"""
import os
import logging

logger = logging.getLogger(__name__)

try:
    import resend
    resend.api_key = os.environ.get("RESEND_API_KEY", "")
    _RESEND_AVAILABLE = True
except ImportError:
    _RESEND_AVAILABLE = False
    logger.warning("resend package not installed — email sending disabled")


_FROM = "Provenance <hello@provenance.kitchen>"

_HTML_WRAPPER = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body {{ margin:0; padding:0; background:#0A0A09; font-family: -apple-system, 'Segoe UI', sans-serif; color:#F5F1E9; }}
  .wrap {{ max-width:520px; margin:40px auto; background:#111113; border:1px solid rgba(201,168,76,0.12); border-radius:6px; padding:40px; }}
  .wordmark {{ font-size:1.1rem; color:#C9A961; letter-spacing:0.05em; margin-bottom:32px; display:block; }}
  h1 {{ font-size:1.4rem; font-weight:400; color:#F5F1E9; margin:0 0 12px; }}
  p {{ font-size:0.9rem; color:rgba(245,241,233,0.7); line-height:1.65; margin:0 0 20px; }}
  .btn {{ display:inline-block; padding:12px 28px; background:rgba(201,168,76,0.12); border:1px solid rgba(201,168,76,0.3); border-radius:4px; color:#C9A961; text-decoration:none; font-size:0.875rem; letter-spacing:0.03em; }}
  .divider {{ border:none; border-top:1px solid rgba(201,168,76,0.08); margin:28px 0; }}
  .small {{ font-size:0.78rem; color:rgba(245,241,233,0.35); }}
  a.plain {{ color:#C9A961; word-break:break-all; }}
</style>
</head>
<body>
<div class="wrap">
  <span class="wordmark">Provenance</span>
  {body}
  <hr class="divider">
  <p class="small">Provenance Culinary Intelligence Inc. &mdash; BC, Canada<br>
  If you did not request this email, you can safely ignore it.</p>
</div>
</body>
</html>"""


def send_password_reset_email(to_email: str, reset_url: str) -> bool:
    """Send password reset email. Returns True on success, False on failure."""
    if not _RESEND_AVAILABLE:
        logger.error("Cannot send password reset email: resend not installed")
        return False

    subject = "Reset your Provenance password"

    text = (
        f"You requested a password reset for your Provenance account.\n\n"
        f"Click the link below to set a new password. This link expires in 24 hours and can only be used once.\n\n"
        f"{reset_url}\n\n"
        f"If you did not request a password reset, you can safely ignore this email.\n\n"
        f"— Provenance"
    )

    body_html = f"""
  <h1>Reset your password</h1>
  <p>You requested a password reset for your Provenance account. Click below to set a new password.</p>
  <p>This link expires in <strong>24 hours</strong> and can only be used once.</p>
  <p><a href="{reset_url}" class="btn">Reset Password →</a></p>
  <p class="small">Or copy this link: <a href="{reset_url}" class="plain">{reset_url}</a></p>
"""

    html = _HTML_WRAPPER.format(body=body_html)

    try:
        resend.Emails.send({
            "from": _FROM,
            "to": [to_email],
            "subject": subject,
            "text": text,
            "html": html,
            "tags": [{"name": "category", "value": "transactional"}],
            "headers": {"X-Entity-Ref-ID": to_email},
        })
        logger.info("Password reset email sent to %s", to_email)
        return True
    except Exception as exc:
        logger.error("Failed to send password reset email to %s: %s", to_email, exc)
        return False


def send_verification_email(to_email: str, verify_url: str) -> bool:
    """Send email verification link. Returns True on success, False on failure."""
    if not _RESEND_AVAILABLE:
        logger.error("Cannot send verification email: resend not installed")
        return False

    subject = "Verify your Provenance email"

    text = (
        f"Welcome to Provenance.\n\n"
        f"Click the link below to verify your email address and enable password recovery. "
        f"This link expires in 7 days.\n\n"
        f"{verify_url}\n\n"
        f"Your account is already active — verification just unlocks password reset.\n\n"
        f"— Provenance"
    )

    body_html = f"""
  <h1>Verify your email</h1>
  <p>Welcome to Provenance. Click below to verify your email address and enable password recovery.</p>
  <p>This link expires in <strong>7 days</strong>. Your account is already active — verification just unlocks password reset.</p>
  <p><a href="{verify_url}" class="btn">Verify Email →</a></p>
  <p class="small">Or copy this link: <a href="{verify_url}" class="plain">{verify_url}</a></p>
"""

    html = _HTML_WRAPPER.format(body=body_html)

    try:
        resend.Emails.send({
            "from": _FROM,
            "to": [to_email],
            "subject": subject,
            "text": text,
            "html": html,
            "tags": [{"name": "category", "value": "transactional"}],
            "headers": {"X-Entity-Ref-ID": to_email},
        })
        logger.info("Verification email sent to %s", to_email)
        return True
    except Exception as exc:
        logger.error("Failed to send verification email to %s: %s", to_email, exc)
        return False


def send_editorial_review_email(to_email: str, d: dict) -> bool:
    """Send structured editorial review notification. Returns True on success."""
    if not _RESEND_AVAILABLE:
        logger.error("Cannot send editorial review email: resend not installed")
        return False

    title = d.get("recipe_title", "")
    chef  = d.get("chef_name", "")
    subject = f"Provenance — recipe submitted for review: {title} — by {chef}"

    # ── Plain text ────────────────────────────────────────────────────────────
    audit_lines = "\n".join(f"  - {i}" for i in d.get("audit_issues", [])) or "  (none)"
    text = (
        f"PROVENANCE — RECIPE SUBMITTED FOR REVIEW\n\n"
        f"Recipe: {title}\n"
        f"Submitted by: {chef} <{d.get('chef_email','')}>\n"
        f"Submitted at: {d.get('submitted_at','')}\n\n"
        f"View the recipe:\n"
        f"https://provenance.kitchen/recipe/{d.get('slug','')}\n\n"
        f"Recipe summary\n"
        f"Yield: {d.get('yield_text','') or 'not set'}\n"
        f"Active time: {d.get('active_time','not set')}\n"
        f"Total time: {d.get('total_time','not set')}\n"
        f"Tradition tags: {d.get('tags','none')}\n"
        f"Sashimi line: {d.get('sashimi_line','') or '(not set)'}\n\n"
        f"Provenance Audit\n"
        f"Issues flagged: {d.get('audit_issue_count',0)}\n"
        f"{audit_lines}\n\n"
        f"Sourcing\n"
        f"{d.get('producer_count',0)} producers, {d.get('product_count',0)} products\n"
        f"Suppliers: {d.get('supplier_names','none')}\n\n"
        f"Method\n"
        f"{d.get('step_count',0)} steps\n"
        f"Notes populated on {d.get('steps_with_notes',0)} of {d.get('step_count',0)} steps\n\n"
        f"---\n"
        f"Submission ID: {d.get('submission_id','')}\n"
    )

    # ── HTML ──────────────────────────────────────────────────────────────────
    audit_html = "".join(f"<li>{i}</li>" for i in d.get("audit_issues", []))
    recipe_url = f"https://provenance.kitchen/recipe/{d.get('slug','')}"
    body_html = f"""
  <h1 style="font-family:Georgia,serif;font-weight:400;font-size:1.3rem;color:#F5F1E9;margin:0 0 20px">
    Recipe submitted for review
  </h1>
  <table style="width:100%;border-collapse:collapse;font-size:0.85rem;margin-bottom:24px">
    <tr><td style="padding:4px 0;color:rgba(245,241,233,0.5);width:130px">Recipe</td><td style="color:#F5F1E9"><strong>{title}</strong></td></tr>
    <tr><td style="padding:4px 0;color:rgba(245,241,233,0.5)">Submitted by</td><td style="color:#F5F1E9">{chef} &lt;{d.get('chef_email','')}&gt;</td></tr>
    <tr><td style="padding:4px 0;color:rgba(245,241,233,0.5)">Submitted at</td><td style="color:#F5F1E9">{d.get('submitted_at','')}</td></tr>
  </table>
  <p><a href="{recipe_url}" class="btn">View recipe &rarr;</a></p>
  <hr class="divider">
  <p style="font-size:0.78rem;color:rgba(245,241,233,0.5);text-transform:uppercase;letter-spacing:0.1em;margin:20px 0 8px">Recipe summary</p>
  <table style="width:100%;border-collapse:collapse;font-size:0.82rem;margin-bottom:20px">
    <tr><td style="padding:3px 0;color:rgba(245,241,233,0.5);width:130px">Yield</td><td style="color:#F5F1E9">{d.get('yield_text','') or 'not set'}</td></tr>
    <tr><td style="padding:3px 0;color:rgba(245,241,233,0.5)">Active time</td><td style="color:#F5F1E9">{d.get('active_time','not set')}</td></tr>
    <tr><td style="padding:3px 0;color:rgba(245,241,233,0.5)">Total time</td><td style="color:#F5F1E9">{d.get('total_time','not set')}</td></tr>
    <tr><td style="padding:3px 0;color:rgba(245,241,233,0.5)">Tags</td><td style="color:#F5F1E9">{d.get('tags','none')}</td></tr>
    <tr><td style="padding:3px 0;color:rgba(245,241,233,0.5)">Sashimi line</td><td style="color:#F5F1E9;font-style:italic">{d.get('sashimi_line','') or '(not set)'}</td></tr>
  </table>
  <p style="font-size:0.78rem;color:rgba(245,241,233,0.5);text-transform:uppercase;letter-spacing:0.1em;margin:0 0 8px">Provenance Audit — {d.get('audit_issue_count',0)} issue(s)</p>
  {'<ul style="margin:0 0 20px;padding-left:18px;font-size:0.82rem;color:#F5F1E9">' + audit_html + '</ul>' if audit_html else '<p style="font-size:0.82rem;color:rgba(245,241,233,0.5);margin:0 0 20px">No issues flagged.</p>'}
  <p style="font-size:0.78rem;color:rgba(245,241,233,0.5);text-transform:uppercase;letter-spacing:0.1em;margin:0 0 8px">Sourcing</p>
  <p style="font-size:0.82rem;color:#F5F1E9;margin:0 0 4px">{d.get('producer_count',0)} producers &middot; {d.get('product_count',0)} products</p>
  <p style="font-size:0.82rem;color:#F5F1E9;margin:0 0 20px">Suppliers: {d.get('supplier_names','none')}</p>
  <p style="font-size:0.78rem;color:rgba(245,241,233,0.5);text-transform:uppercase;letter-spacing:0.1em;margin:0 0 8px">Method</p>
  <p style="font-size:0.82rem;color:#F5F1E9;margin:0 0 20px">{d.get('step_count',0)} steps &middot; notes on {d.get('steps_with_notes',0)} of {d.get('step_count',0)}</p>
  <hr class="divider">
  <p class="small">Submission ID: {d.get('submission_id','')}</p>
"""

    html = _HTML_WRAPPER.format(body=body_html)

    try:
        resend.Emails.send({
            "from": _FROM,
            "to": [to_email],
            "subject": subject,
            "text": text,
            "html": html,
            "tags": [{"name": "category", "value": "editorial"}],
        })
        logger.info("Editorial review email sent to %s for submission %s", to_email, d.get("submission_id"))
        return True
    except Exception as exc:
        logger.error("Failed to send editorial review email: %s", exc)
        return False


def send_supplier_suggestion_email(d: dict) -> bool:
    """Send supplier suggestion notification to garth.greenlees@gmail.com.
    d keys: supplier_name, supplier_website, what_they_make, chef_name, chef_email, recipe_slug.
    """
    if not _RESEND_AVAILABLE:
        logger.error("Cannot send supplier suggestion email: resend not installed")
        return False

    supplier_name = d.get("supplier_name", "")
    subject = f"Provenance — Supplier suggestion: {supplier_name}"

    ctx_line = (
        f"Recipe context: https://provenance.kitchen/recipe/{d['recipe_slug']}"
        if d.get("recipe_slug")
        else "Recipe context: (suggested outside a recipe)"
    )
    text = "\n".join([
        "PROVENANCE — SUPPLIER SUGGESTION",
        "",
        f"Supplier name:  {supplier_name}",
        f"Website:        {d.get('supplier_website') or '(not provided)'}",
        f"What they make: {d.get('what_they_make') or '(not provided)'}",
        "",
        f"Suggested by: {d.get('chef_name') or '(anonymous)'}",
        f"Chef email:   {d.get('chef_email') or '(not provided)'}",
        "",
        ctx_line,
    ])

    params: dict = {
        "from": _FROM,
        "to": ["garth.greenlees@gmail.com"],
        "subject": subject,
        "text": text,
    }
    if d.get("chef_email"):
        params["reply_to"] = d["chef_email"]

    try:
        resend.Emails.send(params)
        logger.info("Supplier suggestion email sent for: %s", supplier_name)
        return True
    except Exception as exc:
        logger.error("Failed to send supplier suggestion email: %s", exc)
        return False
