#!/usr/bin/env python3
"""
Import technique entries from markdown files into the Provenance API.

Reads all .md files under ~/Desktop/Provenance/Technical/Technique_Entry_Data/files/,
parses each ENTRY block into a technique_references-compatible JSON object,
prints the first parsed entry for review, then bulk-uploads in batches of 50.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests

API_BASE = "https://provenance-tester-1.fly.dev/api/techniques"
API_BULK = f"{API_BASE}/bulk"
SOURCE_DIR = Path.home() / "Desktop/Provenance/Technical/Technique_Entry_Data/files"

# ─── Category mapping ─────────────────────────────────────────────────────────
# Map free-form markdown categories to the canonical set used in the DB.

CATEGORY_MAP = {
    "egg": "preparation",
    "knife": "knife_skills",
    "foundational knife": "knife_skills",
    "cutting": "knife_skills",
    "sauce": "sauce_making",
    "stock": "sauce_making",
    "stocks": "sauce_making",
    "mother sauce": "sauce_making",
    "emulsion": "sauce_making",
    "dressing": "sauce_making",
    "condiment": "sauce_making",
    "chutney": "sauce_making",
    "relish": "sauce_making",
    "pickle": "preparation",
    "ferment": "preparation",
    "preserve": "preparation",
    "cur": "preparation",  # curing, curry base
    "marinade": "flavour_building",
    "spice": "flavour_building",
    "aromatic": "flavour_building",
    "flavour": "flavour_building",
    "seasoning": "flavour_building",
    "umami": "flavour_building",
    "heat": "heat_application",
    "grill": "heat_application",
    "roast": "heat_application",
    "sear": "heat_application",
    "fry": "heat_application",
    "stir-fry": "heat_application",
    "wok": "heat_application",
    "sauté": "heat_application",
    "saute": "heat_application",
    "deep-fry": "heat_application",
    "smoke": "heat_application",
    "char": "heat_application",
    "brais": "wet_heat",
    "stew": "wet_heat",
    "poach": "wet_heat",
    "boil": "wet_heat",
    "blanch": "wet_heat",
    "steam": "wet_heat",
    "simmer": "wet_heat",
    "slow-cook": "wet_heat",
    "slow cook": "wet_heat",
    "confit": "wet_heat",
    "soup": "wet_heat",
    "pastry": "pastry_technique",
    "bake": "pastry_technique",
    "baking": "pastry_technique",
    "bread": "grains_and_dough",
    "dough": "grains_and_dough",
    "grain": "grains_and_dough",
    "rice": "grains_and_dough",
    "noodle": "grains_and_dough",
    "pasta": "grains_and_dough",
    "masa": "grains_and_dough",
    "tortilla": "grains_and_dough",
    "dumpling": "grains_and_dough",
    "finish": "finishing",
    "garnish": "finishing",
    "glaze": "finishing",
    "tableside": "finishing_tableside",
    "flambé": "finishing_tableside",
    "flambe": "finishing_tableside",
    "carving": "finishing_tableside",
    "guéridon": "finishing_tableside",
    "at table": "finishing_tableside",
    "plating": "presentation_and_philosophy",
    "presentation": "presentation_and_philosophy",
    "philosophy": "presentation_and_philosophy",
    "principle": "presentation_and_philosophy",
    "architecture": "presentation_and_philosophy",
    "composition": "presentation_and_philosophy",
    "assembled": "preparation_and_service",
    "assembly": "preparation_and_service",
    "service": "preparation_and_service",
    "street food": "preparation_and_service",
    "beverage": "preparation_and_service",
    "dessert": "pastry_technique",
    "sweet": "pastry_technique",
    "confection": "pastry_technique",
    "chocolate": "pastry_technique",
    "sugar": "pastry_technique",
    "cream": "pastry_technique",
    "custard": "pastry_technique",
    "preparation": "preparation",
    "butcher": "preparation",
    "charcuterie": "preparation",
    "equipment": "preparation",
    "dairy": "preparation",
    "cheese": "preparation",
    "raw fish": "preparation",
    "seafood": "preparation",
    "vegetable": "preparation",
    "salad": "preparation",
    "fruit": "preparation",
    "tofu": "preparation",
    "egg cookery": "preparation",
    "core technique": "heat_application",
    "core equipment": "preparation",
    "foundational": "preparation",
    "advanced": "heat_application",
    "modernist": "heat_application",
    "molecular": "heat_application",
    "sous vide": "heat_application",
    "science": "heat_application",
}

VALID_CATEGORIES = {
    "heat_application", "knife_skills", "sauce_making", "flavour_building",
    "preparation", "wet_heat", "pastry_technique", "finishing", "finishing_tableside",
    "grains_and_dough", "presentation_and_philosophy", "preparation_and_service",
}


def classify_category(raw_category: str) -> str:
    """Map a free-form category string to one of the canonical categories."""
    raw_lower = raw_category.lower().strip()

    # Direct match to valid category
    normed = raw_lower.replace(" ", "_").replace("-", "_").replace("/", "_")
    if normed in VALID_CATEGORIES:
        return normed

    # Keyword search through the map
    for keyword, cat in CATEGORY_MAP.items():
        if keyword in raw_lower:
            return cat

    return "preparation"  # safe default


# ─── Authority tier mapping ───────────────────────────────────────────────────

def parse_authority_tier(raw: str) -> int:
    """Extract an integer tier (1-3) from the free-form authority tier string."""
    raw_lower = raw.lower().strip()
    if "modernist" in raw_lower or "contemporary" in raw_lower:
        return 2
    if "regional" in raw_lower or "master" in raw_lower:
        return 2
    if "classical" in raw_lower or "foundation" in raw_lower:
        return 1
    # Try to find a plain integer
    m = re.search(r'\b([1-3])\b', raw)
    if m:
        return int(m.group(1))
    return 1


# ─── Entry parser ─────────────────────────────────────────────────────────────

def extract_section(text: str, header: str) -> str:
    """Extract content under a ### header OR **Header:** bold-label format."""
    # Try ### Header format first
    pattern = rf'###\s*{re.escape(header)}\s*\n(.*?)(?=\n###\s|\n##\s|\n---|\Z)'
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Try **Header:** bold-label format — match both Title Case and lowercase
    # Terminates at next **field:** or ## heading or ---
    esc_header = re.escape(header)
    pattern2 = rf'\*\*{esc_header}:\*\*\s*\n(.*?)(?=\n\*\*[A-Za-z].*?:\*\*|\n###\s|\n##\s|\n---|\Z)'
    m2 = re.search(pattern2, text, re.DOTALL | re.IGNORECASE)
    if m2:
        return m2.group(1).strip()

    # Try **Header:** with inline content on the same line
    pattern3 = rf'\*\*{esc_header}:\*\*\s*(.+?)(?=\n\*\*[A-Za-z].*?:\*\*|\n###\s|\n##\s|\n---|\Z)'
    m3 = re.search(pattern3, text, re.DOTALL | re.IGNORECASE)
    if m3:
        return m3.group(1).strip()

    return ""


def extract_section_fuzzy(text: str, keywords: list[str]) -> str:
    """Try multiple header names, return the first match."""
    for kw in keywords:
        result = extract_section(text, kw)
        if result:
            return result
    return ""


def parse_entry(block: str, file_source_book: str) -> dict | None:
    """Parse a single ENTRY block into a technique_references dict."""

    # Extract name — try multiple header formats:
    # Format 1: ## ENTRY AK-01 — Name
    # Format 2: ### FD-36 | CANTONESE STEAMED FISH (ZHENG YU)
    # Format 3: ## AF01 — Name  or  ## FP01: Name
    header_match = re.search(
        r'^##\s+ENTRY\s+\S+\s*[—–-]\s*(.+)', block, re.MULTILINE
    )
    if not header_match:
        header_match = re.search(
            r'^###\s+\S+\s*\|\s*(.+)', block, re.MULTILINE
        )
    if not header_match:
        # Format 3: ## AF01 — Name  or  ## FP01: Name
        header_match = re.search(
            r'^##\s+[A-Z]{2,}\d+\s*[—–:\-]\s*(.+)', block, re.MULTILINE
        )
    if not header_match:
        # Format 3b: ## FP01: Name (colon without space before name)
        header_match = re.search(
            r'^##\s+[A-Z]{2,}\d+:\s*(.+)', block, re.MULTILINE
        )
    if not header_match:
        # Format 4: ## ID-PRES-01 | Name (Indonesian Batch 12-17)
        header_match = re.search(
            r'^##\s+ID-[A-Z]+-\d+\s*\|\s*(.+)', block, re.MULTILINE
        )
    if not header_match:
        # Format 5: ## THOMPSON ENTRY 1 — Name (Thompson Thai early format)
        header_match = re.search(
            r'^##\s+THOMPSON ENTRY\s+\d+\s*[—–-]\s*(.+)', block, re.MULTILINE
        )
    if not header_match:
        return None
    name = header_match.group(1).strip()
    # Clean up name: remove trailing markers, colons
    name = re.sub(r'\s*[—–-]\s*(COMPLETE|DATABASE COMPLETE)\s*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*:\s*$', '', name)

    # Extract the metadata line: **Category:** ... | **Authority Tier:** ...
    raw_category = ""
    raw_tier = ""
    raw_source = ""

    meta_match = re.search(r'\*\*Category:\*\*\s*(.+)', block)
    if meta_match:
        meta_line = meta_match.group(1)
        parts = re.split(r'\s*\|\s*', meta_line)
        for part in parts:
            part_clean = re.sub(r'\*\*.*?\*\*\s*', '', part).strip()
            part_lower = part.lower()
            if "category" not in part_lower and "tier" not in part_lower and "source" not in part_lower:
                # First part is category
                if not raw_category:
                    raw_category = part_clean
            if "tier" in part_lower:
                raw_tier = part_clean
            if "source" in part_lower:
                raw_source = part_clean
        if not raw_category:
            raw_category = parts[0].strip()
            raw_category = re.sub(r'\*\*.*?\*\*\s*', '', raw_category).strip()

    # Sections — try all known field name variants across formats
    description = extract_section_fuzzy(block, [
        "Description", "technique", "What This Changed",
        "Production Stages", "The Preparation", "Why It Matters",
    ])
    origin = extract_section_fuzzy(block, ["Origin", "Origins", "origin"])
    key_principles = extract_section_fuzzy(block, [
        "Key Principles", "Key principles", "quality_hierarchy",
        "Quality Hierarchy",
    ])
    common_mistakes = extract_section_fuzzy(block, [
        "Common Mistakes", "Common mistakes",
        "Failure Recognition", "Failure recognition",
    ])
    pro_tips = extract_section_fuzzy(block, [
        "Pro Tips", "Pro tips",
        "Cooking Protocol", "Supplier Note",
    ])
    flavour_context = extract_section_fuzzy(block, [
        "Flavour Context", "Flavor Context",
        "Flavour context", "Flavor context",
        "flavour_context",
    ])
    cross_cuisine_raw = extract_section_fuzzy(block, [
        "Cross-Cuisine Parallels", "Cross-cuisine parallels",
        "Cross Cuisine Parallels", "Cross cuisine parallels",
        "cross_cuisine_parallels",
    ])
    trigger_kw_raw = extract_section_fuzzy(block, [
        "Trigger Keywords", "Trigger keywords",
    ])

    # Also grab sensory tests and decisive moment — fold into key_principles
    sensory = extract_section_fuzzy(block, [
        "Sensory Tests", "Sensory tests", "sensory_tests",
    ])
    decisive = extract_section_fuzzy(block, [
        "The Decisive Moment", "Decisive Moment", "Decisive moment",
    ])

    # Build key_principles with sensory/decisive appended
    kp_parts = [key_principles]
    if decisive:
        kp_parts.append(f"\nDecisive moment: {decisive}")
    if sensory:
        kp_parts.append(f"\nSensory tests: {sensory}")
    key_principles = "\n".join(p for p in kp_parts if p).strip()

    # Parse trigger keywords (comma-separated line)
    trigger_keywords = []
    if trigger_kw_raw:
        trigger_keywords = [
            kw.strip() for kw in trigger_kw_raw.split(",") if kw.strip()
        ]
    # Also try **tags:** field (used in ZIP 2 format)
    if not trigger_keywords:
        tags_raw = extract_section_fuzzy(block, ["tags"])
        if tags_raw:
            trigger_keywords = [
                kw.strip() for kw in tags_raw.split(",") if kw.strip()
            ]

    # Parse cross-cuisine parallels into an array of short strings
    cross_cuisine = []
    if cross_cuisine_raw:
        # Try to extract meaningful short references
        # If it's a short list, split on commas or periods
        sentences = [s.strip() for s in re.split(r'[.;]', cross_cuisine_raw) if s.strip()]
        cross_cuisine = [s[:200] for s in sentences if len(s) > 5]

    # Source book: prefer the per-entry source, fall back to file-level
    source_book = raw_source if raw_source else file_source_book

    # Category and tier — also try **cuisine:**/tags for category inference
    if not raw_category:
        cuisine_raw = extract_section_fuzzy(block, ["cuisine"])
        tags_for_cat = extract_section_fuzzy(block, ["tags"])
        raw_category = cuisine_raw or tags_for_cat or name
    category = classify_category(raw_category)
    authority_tier = parse_authority_tier(raw_tier if raw_tier else "")

    # Try subtitle line as description (Batch 12-17: **Name — Subtitle**)
    if not description:
        subtitle_match = re.search(r'^\*\*(.+?)\*\*\s*$', block, re.MULTILINE)
        if subtitle_match:
            sub = subtitle_match.group(1).strip()
            # Only use if it's not a field label (no colon at end)
            if not sub.endswith(':') and len(sub) > 10:
                description = sub

    # If description is empty but origin has substantial content, use origin as description
    if not description and origin and len(origin) > 50:
        description = origin
        origin = None

    # Skip entries with no meaningful content
    if not description and not key_principles:
        return None

    return {
        "name": name,
        "category": category,
        "description": description,
        "key_principles": key_principles,
        "common_mistakes": common_mistakes,
        "pro_tips": pro_tips,
        "trigger_keywords": trigger_keywords,
        "authority_tier": authority_tier,
        "related_techniques": [],
        "tier_level": "standard",
        "source_book": source_book or None,
        "cross_cuisine_parallels": cross_cuisine,
        "origin": origin or None,
        "flavour_context": flavour_context or None,
    }


def extract_file_source(text: str) -> str:
    """Try to extract the book/source from the file header."""
    # Look for **Source:** or **Sources:** in the preamble (before first entry)
    # Find the first entry header of any format
    first_entry = len(text)
    for pat in [r'^## ENTRY\s', r'^### \S+\s*\|', r'^## [A-Z]{2,}\d+[\s—–:\-]', r'^## ID-[A-Z]+-\d+\s*\|']:
        m = re.search(pat, text, re.MULTILINE)
        if m and m.start() < first_entry:
            first_entry = m.start()
    preamble = text[:first_entry] if first_entry < len(text) else text[:500]

    m = re.search(r'\*\*Sources?:\*\*\s*(.+)', preamble)
    if m:
        return m.group(1).strip()

    # Try the file's H1 or H2 header for book info
    for line in preamble.split("\n")[:5]:
        if line.startswith("# ") or line.startswith("## "):
            clean = re.sub(r'^#+\s*', '', line).strip()
            # Skip generic titles like "Provenance — ..."
            clean = re.sub(r'^Provenance\s*[—–-]\s*', '', clean).strip()
            if clean and len(clean) > 5:
                return clean
    return ""


def split_entries(text: str) -> list[str]:
    """Split a markdown file into individual ENTRY blocks."""
    # Try format 1: ## ENTRY ...
    positions = [m.start() for m in re.finditer(r'^## ENTRY\s', text, re.MULTILINE)]

    # Try format 2: ### ID | NAME (Dunlop-style), but only if no format 1 found
    if not positions:
        positions = [m.start() for m in re.finditer(
            r'^### \S+\s*\|', text, re.MULTILINE
        )]

    # Try format 3: ## AF01 — Name  or  ## FP01: Name (ID-style headers)
    if not positions:
        positions = [m.start() for m in re.finditer(
            r'^## [A-Z]{2,}\d+[\s—–:\-]', text, re.MULTILINE
        )]

    # Try format 4: ## ID-PRES-01 | Name (Indonesian Batch 12-17)
    if not positions:
        positions = [m.start() for m in re.finditer(
            r'^## ID-[A-Z]+-\d+\s*\|', text, re.MULTILINE
        )]

    # Try format 5: ## THOMPSON ENTRY N — Name (Thompson Thai early format)
    if not positions:
        positions = [m.start() for m in re.finditer(
            r'^## THOMPSON ENTRY\s+\d+', text, re.MULTILINE
        )]

    if not positions:
        return []

    blocks = []
    for i, pos in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        blocks.append(text[pos:end])
    return blocks


def is_technique_file(text: str) -> bool:
    """Check if a file contains technique entries (vs. CRM docs, briefs, etc.)."""
    if re.search(r'^## ENTRY\s', text, re.MULTILINE):
        return True
    # Dunlop-style: ### FD-36 | NAME with **Category:** metadata
    if re.search(r'^### \S+\s*\|', text, re.MULTILINE) and \
       re.search(r'\*\*Category:\*\*', text):
        return True
    # Format 3: ## AF01 — Name  or  ## FP01: Name (ID-style headers with bold fields)
    if re.search(r'^## [A-Z]{2,}\d+[\s—–:\-]', text, re.MULTILINE) and \
       re.search(r'\*\*(?:origin|technique|Origin|Description):', text):
        return True
    # Format 4: ## ID-PRES-01 | Name (Indonesian Batch 12-17 style)
    if re.search(r'^## ID-[A-Z]+-\d+\s*\|', text, re.MULTILINE) and \
       re.search(r'\*\*(?:Origin|Quality Hierarchy|Sensory)', text, re.IGNORECASE):
        return True
    # Format 5: ## THOMPSON ENTRY N — Name (Thompson Thai early format)
    if re.search(r'^## THOMPSON ENTRY\s+\d+', text, re.MULTILINE):
        return True
    return False


# ─── Main ─────────────────────────────────────────────────────────────────────

def fetch_existing_names() -> set[str]:
    """Fetch all existing technique names directly from DB (case-insensitive)."""
    print("Fetching existing technique names from database...")
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()
        read_dsn = os.environ.get("DATABASE_URL")
        if not read_dsn:
            print("  ERROR: DATABASE_URL is not set (check .env)")
            sys.exit(1)
        conn = psycopg2.connect(read_dsn)
        cur = conn.cursor()
        cur.execute("SELECT lower(name) FROM technique_references")
        names = {row[0] for row in cur.fetchall()}
        cur.close()
        conn.close()
        print(f"  Found {len(names)} existing techniques\n")
        return names
    except Exception as e:
        print(f"  ERROR fetching existing techniques: {e}")
        sys.exit(1)


def main():
    source_dir = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else SOURCE_DIR
    if not source_dir.is_dir():
        print(f"Source directory not found: {source_dir}")
        sys.exit(1)

    # Step 1: Get existing technique names from the database
    existing_names = fetch_existing_names()

    # Step 2: Parse all .md files
    md_files = sorted(source_dir.glob("*.md"))
    print(f"Found {len(md_files)} .md files in {source_dir}\n")

    all_entries = []
    skipped_existing = []
    file_stats = []
    skipped_files = []

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")

        if not is_technique_file(text):
            skipped_files.append(md_file.name)
            continue

        file_source = extract_file_source(text)
        blocks = split_entries(text)
        parsed_count = 0
        new_count = 0

        for block in blocks:
            entry = parse_entry(block, file_source)
            if entry:
                parsed_count += 1
                if entry["name"].strip().lower() in existing_names:
                    skipped_existing.append(entry["name"])
                else:
                    all_entries.append(entry)
                    new_count += 1

        file_stats.append((md_file.name, len(blocks), parsed_count, new_count))

    # Report
    total_parsed = sum(s[2] for s in file_stats)
    print(f"Parsed {total_parsed} technique entries from {len(file_stats)} files")
    print(f"  New (to import): {len(all_entries)}")
    print(f"  Already in DB:   {len(skipped_existing)}")
    if skipped_files:
        print(f"Skipped {len(skipped_files)} non-technique files: {', '.join(skipped_files)}")
    print()

    # File-by-file stats
    for fname, blocks, parsed, new in file_stats:
        existing = parsed - new
        notes = []
        if blocks != parsed:
            notes.append(f"{blocks - parsed} unparseable")
        if existing:
            notes.append(f"{existing} already in DB")
        note_str = f" ({', '.join(notes)})" if notes else ""
        print(f"  {fname}: {new} new / {parsed} total{note_str}")
    print()

    if not all_entries:
        print("No new entries to import. Database is up to date.")
        sys.exit(0)

    # Show first new entry for review
    print("=" * 70)
    print("FIRST NEW ENTRY (for review):")
    print("=" * 70)
    print(json.dumps(all_entries[0], indent=2, ensure_ascii=False))
    print("=" * 70)
    print()

    # Category distribution of new entries
    cat_counts = {}
    for e in all_entries:
        cat_counts[e["category"]] = cat_counts.get(e["category"], 0) + 1
    print("Category distribution (new entries only):")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print()

    # Wait for confirmation
    resp = input(f"Import {len(all_entries)} NEW entries to {API_BULK}? [y/N] ").strip().lower()
    if resp != "y":
        print("Aborted.")
        sys.exit(0)

    # Upload in batches of 50
    batch_size = 50
    total_success = 0
    total_failed = 0

    for i in range(0, len(all_entries), batch_size):
        batch = all_entries[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(all_entries) + batch_size - 1) // batch_size

        try:
            r = requests.post(API_BULK, json=batch, timeout=30)
            if r.ok:
                result = r.json()
                inserted = result.get("inserted", len(batch))
                total_success += inserted
                print(f"  Batch {batch_num}/{total_batches}: {inserted} inserted (running total: {total_success})")
            else:
                total_failed += len(batch)
                print(f"  Batch {batch_num}/{total_batches}: FAILED ({r.status_code}: {r.text[:200]})")
        except Exception as e:
            total_failed += len(batch)
            print(f"  Batch {batch_num}/{total_batches}: ERROR ({e})")

    # Final summary
    print()
    print("=" * 70)
    print(f"IMPORT COMPLETE")
    print(f"  New imported: {total_success}")
    print(f"  Failed:       {total_failed}")
    print(f"  Skipped (already in DB): {len(skipped_existing)}")
    print("=" * 70)

    # Verify total count
    try:
        r = requests.get(API_BASE, timeout=15)
        if r.ok:
            total_in_db = len(r.json())
            print(f"\nTotal techniques now in database: {total_in_db}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
