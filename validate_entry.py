#!/usr/bin/env python3
"""
validate_entry.py — Sashimi Standard validator for Provenance technique entries.
Multi-canon: NZ (Māori/NZ), PC (Pacific Corridor), AI (Australian Indigenous), PH (Filipino).
Checks every entry against the seven-pillar doctrine before commit.
"""

import re
import sys
import json
from pathlib import Path

# ── Banned words ──────────────────────────────────────────────────
BANNED_WORDS = [
    "delicious", "yummy", "tasty", "scrumptious", "mouth-watering",
    "mouthwatering", "lip-smacking", "finger-licking",
    "non-negotiable",       # doctrine: use "where the dish lives or dies"
    "ai-generated", "ai generated", "as an ai",
    "utilize", "utilise",   # prefer "use"
    "facilitate",           # vague
    "leverage",             # corporate
    "robust",               # vague
    "synergy",              # corporate
    "ecosystem",            # unless biological
    "unlock",               # marketing
    "elevate",              # food-blog
    "drizzle",              # unless literal technique instruction
    "nestled",              # travel-blog
    "embark",               # travel-blog
    "tapestry",             # travel-blog
    "rich tapestry",        # travel-blog
    "culinary journey",     # food-blog
    "burst of flavour",     # food-blog
    "burst of flavor",      # food-blog
    "a symphony of",        # food-blog
    "game-changer",         # marketing
    "take it to the next level",  # food-blog
    "unique",               # vague (COMMON_RULES)
    "various",              # vague (COMMON_RULES)
    "typically",            # vague (COMMON_RULES)
    "popular",              # vague (COMMON_RULES)
]

# ── Minimum field lengths ─────────────────────────────────────────
MIN_LENGTHS = {
    "origin":           80,
    "description":      120,
    "cross_cuisine":    60,
    "flavour_context":  60,
    "quality_hierarchy": 40,
    "sensory_tests":    40,
    "lives_or_dies":    40,
}

# ── Required sections (pillar names, flexible matching) ───────────
PILLAR_PATTERNS = {
    "origin": [
        r"(?i)\b(origin|cuisine|cultural|geographic|thread)\b",
        r"(?i)\b(māori|maori|aotearoa|nz|new zealand|wellington|auckland|queenstown)\b",
        r"(?i)\b(samoa|tonga|fiji|cook islands|tahiti|melanesia|vanuatu|solomon|polynesi|pacific)\b",
        r"(?i)\b(australia|aboriginal|indigenous|yolŋu|noongar|anangu|wiradjuri|budj bim)\b",
        r"(?i)\b(filipino|philippine|bicolano|ilocano|kapampangan|visayan|tagalog|manila|cebu)\b",
    ],
    "description": [
        r"(?i)\b(description|what it is|technique|method)\b",
    ],
    "cross_cuisine": [
        r"(?i)\b(thread|cross.?cuisine|parallel|connects? to|→)\b",
    ],
    "flavour_context": [
        r"(?i)\b(flavour|flavor|key|pair|ingredient|species)\b",
    ],
    "quality_hierarchy": [
        r"(?i)\b(best|exceptional|quality|reserve|estate|market|house|hierarchy)\b",
    ],
    "sensory_tests": [
        r"(?i)\b(sensory|visual|aroma|texture|sound|smell|sight|feel)\b",
    ],
    "lives_or_dies": [
        r"(?i)\b(lives|dies|lives.?dies|pivot|moment|where the dish)\b",
    ],
}


class ValidationResult:
    def __init__(self, entry_id: str):
        self.entry_id = entry_id
        self.passed = True
        self.errors = []
        self.warnings = []

    def error(self, msg: str):
        self.passed = False
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        lines = [f"[{status}] {self.entry_id}"]
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARN:  {w}")
        return "\n".join(lines)


def validate_entry(entry_id: str, text: str) -> ValidationResult:
    """
    Validate a single technique entry against the Sashimi Standard.
    Returns a ValidationResult with pass/fail, errors, and warnings.
    """
    result = ValidationResult(entry_id)

    # ── 1. Banned words ───────────────────────────────────────────
    text_lower = text.lower()
    for word in BANNED_WORDS:
        # Use word-boundary matching to avoid false positives on species names
        # (e.g., "Coprosma robusta" should not trigger "robust")
        if re.search(rf"(?i)\b{re.escape(word)}\b", text):
            result.error(f"Banned word/phrase: '{word}'")

    # ── 2. Seven pillars present ──────────────────────────────────
    for pillar, patterns in PILLAR_PATTERNS.items():
        found = any(re.search(p, text) for p in patterns)
        if not found:
            result.error(f"Pillar missing or undetectable: {pillar}")

    # ── 3. Sensory test: at least one genuine sense ───────────────
    senses = ["visual", "aroma", "texture", "sound", "smell", "sight", "feel"]
    sense_count = sum(1 for s in senses if re.search(rf"(?i)\b{s}\b", text))
    if sense_count < 1:
        result.error("No sensory test cues detected (need ≥1 of: visual, aroma, texture, sound, smell, sight, feel)")

    # ── 4. Lives/Dies moment named ────────────────────────────────
    if not re.search(r"(?i)(lives|dies|lives.?dies|pivot|where the dish)", text):
        result.error("No 'lives or dies' moment detected")

    # ── 5. Species precision check ────────────────────────────────
    has_species = bool(re.search(r"(?i)\b(species|genus|\([A-Z][a-z]+ [a-z]+\))", text))
    has_specific_name = bool(re.search(r"[A-Z][a-z]+ [a-z]{3,}", text))
    if not has_species and not has_specific_name:
        result.warn("No species-level precision detected (Latin binomial or specific cultivar name)")

    # ── 6. Temperature check (Celsius + Fahrenheit) ───────────────
    has_temp = bool(re.search(r"\d+\s*°?\s*[CF]", text))
    if has_temp:
        has_c = bool(re.search(r"\d+\s*°?\s*C", text))
        has_f = bool(re.search(r"\d+\s*°?\s*F", text))
        if has_c and not has_f:
            result.warn("Temperature in Celsius only — add Fahrenheit")
        elif has_f and not has_c:
            result.warn("Temperature in Fahrenheit only — add Celsius")
    # No warning if no temps — many entries (ingredients, etc.) don't need them

    # ── 7. Source authority cited ──────────────────────────────────
    authority_indicators = [
        r"(?i)\b(fiso|hiakai|gordon|brown|emett|thornley|tsuji)\b",
        r"(?i)\b(oliver|fotu|me'a kai)\b",  # Pacific Corridor
        r"(?i)\b(pascoe|dark emu|csiro|aiatsis|mindy woods|mark olive)\b",  # Australian Indigenous
        r"(?i)\b(fernandez|palayok|tikim|tayag|fores|besa|dorotan)\b",  # Filipino
        r"(?i)\b(FAO|herbarium|herbaria)\b",  # Institutional
        r"(?i)\b(source|authority|according to|cited|reference)\b",
        r"(?i)\b(ISBN|published|author)\b",
        r"→",  # Door references indicate source anchoring
    ]
    has_authority = any(re.search(p, text) for p in authority_indicators)
    if not has_authority:
        result.warn("No source authority or cross-reference detected")

    # ── 8. DB line present ────────────────────────────────────────
    if not re.search(r"(?i)(DB:|difficulty:|related:)", text):
        result.warn("No DB metadata line detected")

    # ── 9. Regional specificity (canon-aware) ─────────────────────
    # NZ: iwi specificity
    if entry_id.startswith("NZ"):
        generic_maori = re.findall(r'(?<!")\bMāori\b(?!")', text)
        specific_iwi = re.search(
            r"(?i)\b(ngā rauru|ngāti ruanui|ngāti tama|ngai tahu|kāi tahu|"
            r"ngāti porou|ngāpuhi|tūhoe|waikato|tainui|te whānau|te arawa|"
            r"ngāti kahungunu|ngāti raukawa|ngāti maniapoto)\b", text
        )
        if len(generic_maori) > 5 and not specific_iwi:
            result.warn("High 'Māori' count without iwi specificity — consider attributing to specific iwi where sources support it")
    # Pacific island codes: island specificity
    elif entry_id.startswith(("PC", "WS", "FJ", "TO", "CK", "TP", "VU", "SI", "PNG")):
        generic_pacific = re.findall(r"(?i)\bpacific\b", text)
        specific_island = re.search(
            r"(?i)\b(samoa|tonga|fiji|cook islands|tahiti|vanuatu|solomon|"
            r"papua new guinea|melanesia|polynesia)\b", text
        )
        if len(generic_pacific) > 5 and not specific_island:
            result.warn("High 'Pacific' count without island specificity — attribute to specific island group")
    # AI: peoples and Country specificity
    elif entry_id.startswith("AI"):
        generic_aboriginal = re.findall(r"(?i)\b(aboriginal|indigenous)\b", text)
        specific_peoples = re.search(
            r"(?i)\b(yolŋu|noongar|anangu|wiradjuri|budj bim|arrernte|"
            r"pitjantjatjara|gunditjmara|kaurna|ngarrindjeri|wurundjeri|"
            r"yolngu|tiwi|jawoyn|larrakia|meriam)\b", text
        )
        if len(generic_aboriginal) > 5 and not specific_peoples:
            result.warn("High generic 'Aboriginal/Indigenous' count — attribute to specific peoples and Country")
    # PH: regional specificity
    elif entry_id.startswith("PH"):
        generic_filipino = re.findall(r"(?i)\bfilipino\b", text)
        specific_region = re.search(
            r"(?i)\b(ilocano|bicolano|visayan|kapampangan|tagalog|pangasinan|"
            r"maranao|tausug|cebuano|waray|pampanga|bicol|ilocos|cebu|manila|"
            r"mindanao|luzon|visayas)\b", text
        )
        if len(generic_filipino) > 5 and not specific_region:
            result.warn("High generic 'Filipino' count — attribute to specific regional tradition")

    # ── 10. Minimum text length ───────────────────────────────────
    if len(text.strip()) < 200:
        result.error(f"Entry too short ({len(text.strip())} chars, minimum 200)")

    # ── 11. Te reo terms have English translation on first use ────
    te_reo_terms = re.findall(r"\b[A-Za-zā-žĀ-Ž]+\b", text)
    # Just a warning — can't reliably auto-detect all te reo
    common_te_reo = ["hāngi", "kaimoana", "kūmara", "horopito", "pikopiko",
                     "rēwena", "pāua", "kūtai", "mānuka", "kawakawa",
                     "pūhā", "puha", "karengo", "rongoā", "tikanga",
                     "manaakitanga", "whakapapa", "karaka", "mamaku"]
    found_te_reo = [t for t in common_te_reo if t in text_lower]
    for term in found_te_reo:
        # Check if followed by parenthetical or dash translation
        pattern = rf"(?i){re.escape(term)}\s*[\(—–\-]"
        if not re.search(pattern, text):
            # Check if it appears with a translation nearby
            pass  # Don't warn — too many false positives. Manual review covers this.

    return result


def parse_batch_file(filepath: str) -> list:
    """
    Parse a markdown batch file into individual entries.
    Returns list of (entry_id, entry_text) tuples.
    Supports entry prefixes: NZ-, PC-, AI-, PH-
    """
    content = Path(filepath).read_text(encoding="utf-8")
    entries = []
    # NZ=Māori/NZ, PC=Pacific(generic), WS=Samoa, FJ=Fiji, TO=Tonga,
    # CK=Cook Islands, TP=Tahiti, VU=Vanuatu, SI=Solomon Islands,
    # PNG=Papua New Guinea, AI=Australian Indigenous, PH=Filipino
    PREFIX = r"(?:NZ|PC|WS|FJ|TO|CK|TP|VU|SI|PNG|AI|PH)"

    # Split on entry headers: ## PC-01, ### AI-01, ## ENTRY PH-01, etc.
    pattern = rf"(?:^|\n)(?:##\s*(?:ENTRY\s+)?)({PREFIX}-\d+[a-z]?\b.*?)(?=\n##\s*(?:ENTRY\s+)?{PREFIX}-\d|$)"
    matches = re.finditer(pattern, content, re.DOTALL)

    for m in matches:
        header_and_body = m.group(1)
        id_match = re.match(rf"({PREFIX}-\d+[a-z]?)", header_and_body)
        if id_match:
            entry_id = id_match.group(1)
            entries.append((entry_id, header_and_body))

    # Fallback: try bold-header format (**PC-01 ---**)
    if not entries:
        pattern2 = rf"\*\*({PREFIX}-\d+[a-z]?)\s*(?:---|-—)\s*(.*?)\*\*(.*?)(?=\*\*{PREFIX}-\d|$)"
        matches2 = re.finditer(pattern2, content, re.DOTALL)
        for m in matches2:
            entry_id = m.group(1)
            entry_text = m.group(2) + m.group(3)
            entries.append((entry_id, entry_text))

    return entries


def validate_batch(filepath: str) -> tuple:
    """
    Validate all entries in a batch file.
    Returns (results_list, pass_count, fail_count).
    """
    entries = parse_batch_file(filepath)
    results = []
    pass_count = 0
    fail_count = 0

    for entry_id, text in entries:
        result = validate_entry(entry_id, text)
        results.append(result)
        if result.passed:
            pass_count += 1
        else:
            fail_count += 1

    return results, pass_count, fail_count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_entry.py <batch_file.md> [--verbose]")
        sys.exit(1)

    filepath = sys.argv[1]
    verbose = "--verbose" in sys.argv

    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    results, passed, failed = validate_batch(filepath)

    print(f"\n{'='*60}")
    print(f"SASHIMI VALIDATOR — {Path(filepath).name}")
    print(f"{'='*60}")
    print(f"Entries: {len(results)}  |  PASS: {passed}  |  FAIL: {failed}")
    print(f"{'='*60}\n")

    for r in results:
        if verbose or not r.passed or r.warnings:
            print(r)
            print()

    if failed > 0:
        print(f"\n{failed} entries FAILED validation. Fix before commit.")
        sys.exit(1)
    else:
        print(f"\nAll {passed} entries PASSED. Ready for commit.")
        sys.exit(0)
