-- Cycle 3b: the shopping list — a working chef shops from recipes.
CREATE TABLE IF NOT EXISTS shopping_list_items (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name         TEXT NOT NULL,
    qty          TEXT,
    unit         TEXT,
    source_slug  TEXT,
    source_title TEXT,
    is_checked   BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_shopping_user ON shopping_list_items (user_id, is_checked, created_at);
