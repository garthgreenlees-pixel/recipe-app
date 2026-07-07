-- Cycle 2: Collections (named recipe groups with a spine colour) + cook log.

CREATE TABLE IF NOT EXISTS user_collections (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    colour      TEXT NOT NULL DEFAULT '#3F6090',
    sort_order  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_collections_user ON user_collections (user_id, sort_order);

CREATE TABLE IF NOT EXISTS collection_recipes (
    collection_id UUID NOT NULL REFERENCES user_collections(id) ON DELETE CASCADE,
    recipe_ref    TEXT NOT NULL,          -- user_kitchen_recipes.uuid
    added_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (collection_id, recipe_ref)
);

CREATE TABLE IF NOT EXISTS recipe_cook_log (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_ref TEXT NOT NULL,             -- recipe uuid or slug
    cooked_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_cook_log_user_time ON recipe_cook_log (user_id, cooked_at DESC);
