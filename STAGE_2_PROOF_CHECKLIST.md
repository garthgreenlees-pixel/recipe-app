# Stage 2 — Stripe Test-Payment Proof · HOT CHECKLIST
# Parked on founder's Stripe-dashboard recovery. The moment you confirm the
# staging secrets are set, this fires with zero warm-up.

## What YOU set on staging (provenance-staging) when the dashboard is back
fly secrets set -a provenance-staging \
  STRIPE_SECRET_KEY=sk_test_… \
  STRIPE_WEBHOOK_SECRET=whsec_… \
  STRIPE_PRICE_KITCHEN_MONTHLY=price_… STRIPE_PRICE_KITCHEN_YEARLY=price_… \
  STRIPE_PRICE_LIBRARY_MONTHLY=price_… STRIPE_PRICE_LIBRARY_YEARLY=price_… \
  STRIPE_PRICE_PROFESSION_MONTHLY=price_… STRIPE_PRICE_PROFESSION_YEARLY=price_… \
  STRIPE_PRICE_TRADE_MONTHLY=price_… STRIPE_PRICE_TRADE_YEARLY=price_… \
  SENTRY_DSN=https://…            # so the webhook's Sentry-on-error path is provable
# Test webhook endpoint in the Stripe TEST dashboard →
#   URL: https://provenance-staging.fly.dev/webhook/stripe
#   events: checkout.session.completed, customer.subscription.updated/deleted,
#           invoice.payment_failed   (copy its whsec_ into the secret above)
# Then tell me "secrets are set" — nothing else needed from you.

## What I FIRE immediately on your "secrets are set" (zero warm-up)
1. Redeploy staging so it picks up the secrets (fly deploy --config fly.staging.toml).
2. Confirm test-mode: staging /pricing renders, keys are sk_test.
3. Drive a checkout on staging as the smoke account (smoke@test.local) through
   /subscribe/kitchen — card 4242 4242 4242 4242 — to the receipt.
4. PROOF A — recorded: read the staging users row back — subscription_tier,
   subscription_status='active', stripe_customer_id, stripe_subscription_id set
   by checkout.session.completed.
5. PROOF B — retries on failure: temporarily point the write DSN at a bad value
   (or trigger a handled failure), re-send the event from the Stripe dashboard,
   confirm the webhook returns HTTP 500 and Stripe marks it for retry; restore.
6. PROOF C — Sentry sees errors: confirm the 500 produced a
   sentry_sdk.capture_exception event in the staging Sentry project.
7. Browser walk of the staging flow as a brand-new member; screenshot the
   receipt + the unlocked tier.
8. Prepare (NOT run) the live promotion of commit 3fc2555 (the webhook fix)
   labeled THIS GOES TO: LIVE, waiting for "push it live".

## The fix under proof (already in code, commit 3fc2555, NOT yet on live)
- Webhook wraps event handling: sentry_sdk.capture_exception(e) + return 500 so
  Stripe retries (server.py ~13836–13883).
- update_user / update_user_by_stripe_customer re-raise instead of swallowing.
- Records onto users table on checkout.session.completed.
