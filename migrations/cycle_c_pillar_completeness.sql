-- Canon Render Cycle C: additive migration
-- Adds pillar_completeness jsonb for internal census only — never rendered.
-- Safe to run multiple times (IF NOT EXISTS).
ALTER TABLE technique_references
  ADD COLUMN IF NOT EXISTS pillar_completeness jsonb;
