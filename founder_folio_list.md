# Founder Folio List
#
# Authorised open_folio slugs — the ONLY technique_references rows that may
# carry open_folio = TRUE in production.
#
# Format: one slug per line. Blank lines and lines starting with # are ignored.
# Dashes at the start of a line are stripped (- slug is the same as slug).
#
# A canon's folios must be listed here before promote_canon.py will allow
# promotion (gate-b). Gate-a refuses promotion if live carries any open_folio
# row whose slug is NOT listed here; it prints cleanup SQL for the operator.
#
# Populate this file with the intentionally-open folios before first use.
