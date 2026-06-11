-- Canon Render Cycle B: additive migration
-- Adds recipe_card jsonb column for cached parsed recipe blobs.
-- Safe to run multiple times (IF NOT EXISTS).
ALTER TABLE technique_references
  ADD COLUMN IF NOT EXISTS recipe_card jsonb;
