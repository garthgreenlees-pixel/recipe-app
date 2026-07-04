# Founder Folio List
#
# Authorised open_folio slugs — the ONLY technique_references rows that may
# carry open_folio = TRUE in production.
#
# FORMAT
#   One slug per line.  Blank lines and lines starting with # are ignored.
#   Use ## <canon_slug> headings to organise by canon (headings are comments,
#   they do not affect parsing).  Dashes at the start of a line are stripped
#   (- some-slug is treated identically to some-slug).
#
# HOW THE GATES USE THIS FILE
#   gate-a  Live open_folio flags must be a subset of this list.  Any live
#           flag not listed here causes gate-a to FAIL and prints cleanup SQL
#           for the operator to approve separately.
#   gate-b  promote_canon.py <canon> refuses to promote unless at least one
#           slug in this file belongs to that canon's staging entries.
#
# WORKFLOW
#   1. Review the CANDIDATE SUGGESTIONS below (derived from pillar_completeness).
#   2. Uncomment the slugs you want to open (remove the leading '# - ').
#   3. Add any additional slugs you want to open; delete any you don't.
#   4. Run: python3 scripts/promote_canon.py japanese   (dry-run)
#   5. When all gates pass, re-run with --execute.

## japanese
#
# CANDIDATE SUGGESTIONS — FOUNDER APPROVAL REQUIRED.
# Generated from top-2 entries per chapter by pillar_completeness score.
# Uncomment a slug to authorise it.  Delete lines you don't want opened.
#
# chapter: overview-cultural-context  (229 entries)
# - abalone-awabi-grilled-live-and-preparation-methods                        (pc: 4)
# - abalone-awabi-japans-most-prized-shellfish-and-its-cultural-significance   (pc: 4)
#
# chapter: the-method  (1448 entries)
# - salt-b1-10-katsuobushi-production-b1                                      (pc: 7  ← highest in canon)
# - misoyaki-miso-glazed-fish                                                  (pc: 6)
#
# chapter: the-canonical-dishes  (1102 entries)
# - abura-natto-fried-tofu-pockets-inari                                       (pc: 4)
# - aburi-flame-searing-technique-in-sushi-and-sashimi                         (pc: 4)
#
# (Other chapters currently have 0 published entries in staging.)
