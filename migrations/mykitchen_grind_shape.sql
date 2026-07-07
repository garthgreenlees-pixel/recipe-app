-- MyKitchen grind SHAPE — per-recipe shelf notes the grind lane composes.
-- Mirrors the cellar's beverage_preparations.is_published gate exactly:
-- the grind lane writes rows unpublished; only is_published rows ever render.
-- Built early (rule 5) so the grind lane composes in parallel through the night.

CREATE TABLE IF NOT EXISTS recipe_shelf_notes (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_slug   TEXT NOT NULL,
    scope         TEXT NOT NULL DEFAULT 'canon',   -- 'canon' shared; room for per-user later
    note_md       TEXT NOT NULL,                    -- composed kitchen-note (markdown)
    summary       TEXT,                             -- one-line for the card, optional
    is_published  BOOLEAN NOT NULL DEFAULT FALSE,   -- THE GRIND GATE
    source        TEXT NOT NULL DEFAULT 'grind',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (recipe_slug, scope)
);

CREATE INDEX IF NOT EXISTS idx_shelf_notes_slug_pub
    ON recipe_shelf_notes (recipe_slug, is_published);

-- One seed row (UNPUBLISHED) so the grind lane sees the exact shape it writes.
INSERT INTO recipe_shelf_notes (recipe_slug, scope, note_md, summary, is_published, source)
VALUES (
    '__grind_shape_example__', 'canon',
    'The kitchen note lives here — a short, canon-held paragraph the cook reads before they start: what this dish lives or dies on, the one move that matters, the tell that it is right. The grind lane composes this; it stays invisible until is_published = true.',
    'The one move that matters, in a line.',
    FALSE, 'grind'
)
ON CONFLICT (recipe_slug, scope) DO NOTHING;
