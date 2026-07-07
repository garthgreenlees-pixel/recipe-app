-- Cycle 2: migrate the flat 'partial' pairings to the approved three-tier
-- grammar (spec v1.1 §6). The original CHECK predates the spec and lacks
-- 'unverified', so it is widened first. verification_level is 'auto' on all
-- rows (no prior human review evidence), so per founder rule ALL land at
-- unverified; founder sign-off promotes to editorial. Idempotent.
ALTER TABLE technique_beverage_pairings
  DROP CONSTRAINT IF EXISTS technique_beverage_pairings_confidence_status_check;
ALTER TABLE technique_beverage_pairings
  ADD CONSTRAINT technique_beverage_pairings_confidence_status_check
  CHECK (confidence_status IN ('unverified','reviewed','editorial','partial'));
UPDATE technique_beverage_pairings
   SET confidence_status = 'unverified'
 WHERE confidence_status = 'partial';
