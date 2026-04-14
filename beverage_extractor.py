#!/usr/bin/env python3
"""
PROVENANCE BEVERAGE EXTRACTION ENGINE v1
=========================================
Autonomous beverage extraction at sashimi depth.
Covers all 11 traditions, all world regions, all purveyor connections.

This engine extracts THREE things simultaneously:
1. Beverage technique entries (production, service, terroir)
2. Producer intelligence (estates, distilleries, breweries, farms)
3. Purveyor/distributor connections (who sells it in your market)

Usage in Claude Code:
    from beverage_extractor import BeverageSession
    session = BeverageSession(
        tradition="wine",
        region="France — Burgundy",
        output_dir="./provenance_output/beverage"
    )
    session.add_beverage({...})
    session.add_producer({...})
    session.add_purveyor({...})
"""

import json
import os
import sys
from datetime import datetime, timezone


# ============================================================================
# AUTONOMOUS OPERATION DIRECTIVE — THE TEN COMMANDMENTS (BEVERAGE)
# ============================================================================
"""
1. NEVER stop to ask permission. Extract, validate, commit. Next entry.
2. NEVER ask "shall I continue?" The answer is always yes.
3. NEVER summarise what you're about to do. Do it.
4. Batch size: 15-20 entries per commit. Auto-commit when full.
5. If an entry can't meet the Sashimi Standard, flag it. Don't stop.
6. If you finish a tradition, move to the next. One status line.
7. If you finish a region, move to the next. One status line.
8. Extract PRODUCERS and PURVEYORS alongside every beverage entry.
9. Only stop at context window exhaustion. Produce the handoff.
10. Every token is an entry or a status update. Nothing else.
"""


# ============================================================================
# BEVERAGE SASHIMI STANDARD — THE SEVEN PILLARS
# ============================================================================

BEVERAGE_PILLARS = """
Every beverage entry must meet ALL SEVEN PILLARS or it goes to FLAGGED_FOR_REVIEW.md.

PILLAR 1 — TERROIR & ORIGIN
Not "France." Not "Burgundy." Instead: "The Côte de Nuits, specifically the
limestone-rich Bajocian escarpment between Gevrey-Chambertin and Vosne-Romanée,
where the east-southeast exposure and thin Bathonian limestone soils produce Pinot
Noir of extraordinary concentration and aromatic complexity."

For non-wine: "Ethiopian coffee from the Yirgacheffe woreda in the Gedeo Zone of
the Southern Nations region, grown at 1,750-2,200m elevation in the shade of
indigenous false banana (enset) trees."

For ceremonial: "Kava from Vanuatu's Pentecost Island, where the Ni-Vanuatu
people cultivate noble varieties (Borogu, Melomelo) using traditional shade-
growing methods unchanged for three millennia."

PILLAR 2 — PRODUCTION TECHNIQUE
Professional-grade execution. A sommelier, barista, brewmaster, or distiller
must be able to understand the complete production chain from this description.

Wine: vineyard management → harvest decision → crush → fermentation → malo →
ageing → blending → fining → bottling. Each step specific to THIS producer.

Spirits: raw material → mashing/fermenting → distillation (pot/column/hybrid,
number of passes, cut points) → ageing (vessel, duration, climate) → blending
→ proofing → bottling.

Coffee: cultivar → altitude → processing (washed/natural/honey) → drying →
milling → grading → roasting profile → extraction method.

Tea: cultivar → terroir → harvest (flush, plucking standard) → withering →
oxidation level → firing/drying → shaping → ageing (if applicable).

Ceremonial: source material → preparation ritual → service protocol → cultural
context → who may prepare it → who may consume it → what it means.

PILLAR 3 — CROSS-TRADITION PARALLELS
Minimum 2 genuine parallels. These illuminate — they don't decorate.

"Goan feni's double-distillation in clay pots parallels mezcal's earthen-pit
roasting in that both derive terroir character from the vessel itself — the clay
imparts mineral notes just as the earth pit imparts smoke. Both traditions also
share a resistance to industrialisation that keeps production artisanal by
necessity, not nostalgia."

NOT: "Both are spirits." That's a category, not a parallel.

PILLAR 4 — SENSORY PROFILE (Deductive Method)
For wine and spirits: follow the CMS deductive grid.
  Appearance: clarity, colour depth, colour hue
  Nose: condition, fruit character, earth/mineral, oak/ageing, secondary
  Palate: sweetness, acidity, tannin (if applicable), body, flavour intensity,
          flavour characteristics, finish length
  Conclusion: quality level, readiness, identity

For coffee: fragrance (dry), aroma (wet), flavour, aftertaste, acidity,
body, balance, sweetness, clean cup, uniformity, overall (SCA protocol).

For tea: appearance (dry leaf, liquor), aroma (dry, wet, infusion), flavour,
body, astringency, sweetness, finish, number of infusions.

For beer: appearance, aroma, flavour, mouthfeel, overall (BJCP protocol).

For ceremonial: the complete sensory experience including non-flavour elements
(visual ceremony, sounds, textures, aromas of the space, emotional register).

PILLAR 5 — QUALITY HIERARCHY
Four tiers. Specific, measurable criteria at each level.

4 — RESERVE: The benchmark. Award-winning. The version that defines the
    category. Specific markers described.
3 — ESTATE: Professional-grade. Distinctive character. Minor imperfections
    acceptable. What distinguishes it from Reserve named.
2 — MARKET: Competent commercial product. Functional but undistinguished.
    What's missing compared to Estate named.
1 — HOUSE: Entry-level. Recognisable as the category. Common flaws described
    so the professional can identify and avoid.

PILLAR 6 — SERVICE INTELLIGENCE
How this beverage is served at professional level. The MOF standard.

Wine: temperature (exact °C), glass (specific shape and why), decanting
decision (yes/no/when, with rationale), pour volume, service sequence in
a multi-course programme, verbal presentation to guest.

Spirits: neat/rocks/mixed, glass, temperature, water addition (if applicable),
garnish (if applicable), service timing in programme.

Coffee: extraction method, water temperature, ratio, grind size, extraction
time, cup/vessel, service accompaniments.

Tea: water temperature, steep time, vessel, number of infusions, service
ceremony (if applicable).

Beer: glass shape, temperature, pour technique (head management), draught
vs. bottle/can distinction.

Ceremonial: complete service ritual. Who prepares. Who serves. The sequence.
The words spoken. The physical movements. The cultural meaning.

PILLAR 7 — PURVEYOR INTELLIGENCE
WHO MAKES IT. WHO SELLS IT. HOW TO SOURCE IT.

Producer: name, location, key person (winemaker/distiller/roaster/brewmaster),
production volume, notable products, certifications (organic/biodynamic/etc).

Distributor/Importer: Pat's Rule applies — ORIGIN (benchmark producer, cited
for authority) and PROVIDER (regional distributor, gets the click-through,
filtered by user's region).

CRITICAL: NEVER fabricate a producer, distributor, or supplier name. If you
don't know the distributor for a specific market, leave the field as
"[PROVIDER: verify for {region}]". Known fabricated names to NEVER use:
Italco, Gourmet Cargo, WA Imports, Cocoberry.

For every beverage entry, attempt to identify:
- The benchmark producer (ORIGIN)
- The BC/Canadian distributor (if known)
- The US distributor (if known)
- The certification status (organic, biodynamic, sustainable, etc.)
"""


# ============================================================================
# VOICE RULES — Applied to Every Beverage Entry
# ============================================================================

VOICE_RULES = """
- Write like a Master Sommelier speaks: precise, warm, authoritative, never condescending
- Write like a MOF examiner evaluates: technically exact, sensory-specific, service-aware
- Never say "AI" anywhere in any entry
- Never say "platform," "leverage," "seamless," "elevate," "utilize"
- Never say "notes of" without specifying WHAT and WHY (the compound, the process)
- Never say "pairs well with" without the pairing TYPE and RATIONALE
- Never say "easy drinking" or "approachable" — these are evasions of description
- French wine terms preserved (terroir, cru, appellation, cuvée, assemblage)
- Japanese sake terms preserved (junmai, ginjō, daiginjō, nihonshu-do, SMV)
- Kristang/Portuguese terms preserved where they exist (feni, cachaça, ginjinha)
- The word "terroir" is earned. It means the complete expression of place in flavour —
  soil, climate, altitude, exposure, microflora, human practice, and time.
- No exclamation marks. No enthusiasm. Precision is the only acceptable tone.
"""


# ============================================================================
# SCHEMA — Beverage Entry
# ============================================================================

BEVERAGE_ENTRY_TEMPLATE = {
    # Identity
    "entry_id": "",           # Auto-generated: {tradition_code}-{region_code}-{number}
    "tradition": "",          # wine | spirits | sake | coffee | beer | tea | ceremonial | fortified | na | fermented | water
    "sub_tradition": "",      # e.g., "still red", "single malt", "junmai ginjō", "gongfu oolong"
    "region": "",             # Specific appellation/origin
    "name": "",               # Product or technique name

    # The Seven Pillars
    "terroir_origin": "",                # Pillar 1
    "production_technique": "",          # Pillar 2
    "cross_tradition_parallels": [       # Pillar 3
        {"tradition": "", "beverage": "", "connection": ""},
        {"tradition": "", "beverage": "", "connection": ""}
    ],
    "sensory_profile": {                 # Pillar 4
        "appearance": "",
        "nose": "",
        "palate": "",
        "conclusion": ""
    },
    "quality_hierarchy": [               # Pillar 5
        {"tier": 4, "tier_name": "Reserve", "criteria": "", "markers": ""},
        {"tier": 3, "tier_name": "Estate", "criteria": "", "markers": ""},
        {"tier": 2, "tier_name": "Market", "criteria": "", "markers": ""},
        {"tier": 1, "tier_name": "House", "criteria": "", "markers": ""}
    ],
    "service_intelligence": {            # Pillar 6
        "temperature": "",
        "vessel": "",
        "technique": "",
        "programme_position": "",
        "verbal_presentation": ""
    },
    "purveyor_intelligence": {           # Pillar 7
        "benchmark_producer": "",
        "producer_location": "",
        "key_person": "",
        "production_volume": "",
        "certifications": [],
        "bc_distributor": "",
        "us_distributor": "",
        "uk_distributor": "",
        "price_tier": "",       # Reserve/Estate/Market/House
        "availability_notes": ""
    },

    # Trail connections
    "trail_connection": "",   # PCT-1, PMT-5, WADT-3, etc. Empty if none.
    "trail_note": "",
    "food_pairings": [        # Links to technique database entries
        {"technique_id": "", "dish": "", "pairing_type": "", "rationale": ""}
    ],

    # Metadata
    "source": "",
    "extracted_at": "",
    "batch_number": 0
}

PRODUCER_TEMPLATE = {
    "producer_id": "",
    "name": "",
    "location": "",
    "country": "",
    "region": "",
    "tradition": "",          # wine | spirits | coffee | etc.
    "key_person": "",         # winemaker, distiller, roaster, brewmaster
    "founded": "",
    "production_volume": "",
    "notable_products": [],
    "certifications": [],
    "website": "",
    "philosophy": "",         # 1-2 sentences on their approach
    "trail_connection": "",
    "source": "",
    "verified": False         # Must be web-searched to set True
}

PURVEYOR_TEMPLATE = {
    "purveyor_id": "",
    "name": "",
    "type": "",               # importer | distributor | agent | direct
    "location": "",
    "markets_served": [],     # ["BC", "Alberta", "Ontario", "Washington", "Oregon"]
    "traditions_carried": [], # ["wine", "spirits", "sake"]
    "producer_relationships": [],  # Producer IDs they distribute for
    "website": "",
    "contact": "",
    "minimum_order": "",
    "delivery_notes": "",
    "verified": False
}


# ============================================================================
# VALIDATOR — Beverage Sashimi Standard
# ============================================================================

class BeverageSashimiValidator:
    """Validates beverage entries against the Sashimi Standard."""

    FORBIDDEN_WORDS = [
        "platform", "leverage", "seamless", "elevate", "utilize",
        "easy drinking", "approachable", "quaffable", "crowd-pleaser"
    ]

    VAGUE_DESCRIPTORS = [
        "notes of", "hints of", "touch of", "pairs well with",
        "goes great with", "perfect for", "ideal with"
    ]

    def validate(self, entry: dict) -> tuple[bool, list[str]]:
        failures = []
        import re

        # Pillar 1: Terroir & Origin
        terroir = entry.get("terroir_origin", "")
        if not terroir or len(terroir) < 50:
            failures.append("TERROIR: Missing or too brief (min 50 chars)")
        country_only = ["France", "Italy", "Spain", "Japan", "USA", "Australia",
                        "Portugal", "Germany", "Chile", "Argentina", "New Zealand"]
        for c in country_only:
            if terroir.strip().startswith(c) and len(terroir) < 80:
                failures.append(f"TERROIR: '{c}' alone is not terroir. Name the specific region/appellation/estate.")
                break

        # Pillar 2: Production Technique
        prod = entry.get("production_technique", "")
        if not prod or len(prod) < 100:
            failures.append("PRODUCTION: Missing or too brief (min 100 chars for professional depth)")

        # Pillar 3: Cross-Tradition Parallels (min 2)
        parallels = entry.get("cross_tradition_parallels", [])
        if len(parallels) < 2:
            failures.append(f"PARALLELS: Only {len(parallels)}, need minimum 2")
        for i, p in enumerate(parallels):
            if isinstance(p, dict) and len(p.get("connection", "")) < 30:
                failures.append(f"PARALLELS[{i}]: Connection too brief — must illuminate")

        # Pillar 4: Sensory Profile
        sensory = entry.get("sensory_profile", {})
        if isinstance(sensory, dict):
            for field in ["appearance", "nose", "palate"]:
                if not sensory.get(field) or len(sensory.get(field, "")) < 20:
                    failures.append(f"SENSORY: '{field}' missing or too brief")
        else:
            failures.append("SENSORY: Profile missing entirely")

        # Pillar 5: Quality Hierarchy (4 tiers)
        hierarchy = entry.get("quality_hierarchy", [])
        if len(hierarchy) < 4:
            failures.append(f"QUALITY: Only {len(hierarchy)} tiers, need all 4")
        for level in hierarchy:
            if isinstance(level, dict):
                if not level.get("criteria") or len(level.get("criteria", "")) < 20:
                    failures.append(f"QUALITY[{level.get('tier_name', '?')}]: Criteria too brief")

        # Pillar 6: Service Intelligence
        service = entry.get("service_intelligence", {})
        if isinstance(service, dict):
            if not service.get("temperature"):
                failures.append("SERVICE: Temperature missing")
            if not service.get("vessel"):
                failures.append("SERVICE: Vessel/glass missing")
        else:
            failures.append("SERVICE: Intelligence missing entirely")

        # Pillar 7: Purveyor Intelligence
        purveyor = entry.get("purveyor_intelligence", {})
        if isinstance(purveyor, dict):
            if not purveyor.get("benchmark_producer"):
                failures.append("PURVEYOR: Benchmark producer missing")
        else:
            failures.append("PURVEYOR: Intelligence missing entirely")

        # Voice check
        full_text = " ".join([
            entry.get("terroir_origin", ""),
            entry.get("production_technique", ""),
            str(entry.get("sensory_profile", {})),
            str(entry.get("service_intelligence", {}))
        ])

        for forbidden in self.FORBIDDEN_WORDS:
            if forbidden.lower() in full_text.lower():
                failures.append(f"VOICE: Forbidden phrase '{forbidden}' found")

        for vague in self.VAGUE_DESCRIPTORS:
            if vague.lower() in full_text.lower():
                # Allow "notes of" if followed by a specific compound
                if vague == "notes of":
                    context = full_text.lower()
                    idx = context.find("notes of")
                    if idx >= 0:
                        after = context[idx+8:idx+50]
                        has_specific = any(w in after for w in [
                            "vanillin", "linalool", "geraniol", "terpene",
                            "ester", "phenol", "lactone", "aldehyde",
                            "caused by", "from the", "due to", "resulting"
                        ])
                        if not has_specific:
                            failures.append(f"VOICE: '{vague}' used without specifying the compound or cause")
                else:
                    failures.append(f"VOICE: Vague descriptor '{vague}' — specify the pairing type and rationale")

        # "AI" check — case-sensitive word boundary
        if re.search(r'\bAI\b', full_text):
            failures.append("VOICE: Forbidden word 'AI' found")

        # Required fields
        for field in ["tradition", "region", "name"]:
            if not entry.get(field):
                failures.append(f"REQUIRED: '{field}' is empty")

        return len(failures) == 0, failures


# ============================================================================
# EXTRACTION SESSION
# ============================================================================

class BeverageSession:
    """Manages a beverage extraction session with parallel producer/purveyor tracking."""

    BATCH_SIZE = 15

    def __init__(self, tradition, region, output_dir="./provenance_output/beverage",
                 starting_entry=1, session_number=1, running_total=0):
        self.tradition = tradition
        self.region = region
        self.output_dir = output_dir
        self.current_entry = starting_entry
        self.session_number = session_number
        self.running_total = running_total
        self.batch_number = 0
        self.current_batch = []
        self.producers_found = []
        self.purveyors_found = []
        self.session_beverages = 0
        self.session_producers = 0
        self.session_purveyors = 0
        self.session_flagged = 0
        self.completed_regions = []
        self.validator = BeverageSashimiValidator()
        self.session_start = datetime.now(timezone.utc).isoformat()

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "batches"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "producers"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "purveyors"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "sessions"), exist_ok=True)

        for logfile in ["FLAGGED_FOR_REVIEW.md", "PURVEYOR_LEADS.md", "PRODUCER_DIRECTORY.md"]:
            fp = os.path.join(output_dir, logfile)
            if not os.path.exists(fp):
                with open(fp, "w") as f:
                    f.write(f"# {logfile.replace('.md','').replace('_',' ').title()}\n\n---\n\n")

        self._load_state()

        print(f"[SESSION START] Tradition: {tradition} | Region: {region}")
        print(f"[SESSION START] Starting entry #{starting_entry} | Running total: {running_total}")
        print(f"[SESSION START] Autonomous mode: ON — extract beverages + producers + purveyors continuously")
        print("=" * 70)

    def _load_state(self):
        state_file = os.path.join(self.output_dir, "session_state.json")
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)
                self.running_total = max(self.running_total, state.get("running_total", 0))
                self.completed_regions = state.get("completed_regions", [])
                key = f"{self.tradition}_{self.region}"
                highest = state.get("highest_entries", {}).get(key, 0)
                if highest >= self.current_entry:
                    self.current_entry = highest + 1
                    print(f"[RESUME] Continuing from entry #{self.current_entry}")

    def _save_state(self):
        state_file = os.path.join(self.output_dir, "session_state.json")
        state = {}
        if os.path.exists(state_file):
            with open(state_file, "r") as f:
                state = json.load(f)

        key = f"{self.tradition}_{self.region}"
        highest = state.get("highest_entries", {})
        highest[key] = self.current_entry - 1
        state["highest_entries"] = highest
        state["running_total"] = self.running_total
        state["completed_regions"] = self.completed_regions
        state["last_tradition"] = self.tradition
        state["last_region"] = self.region

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)

    def _tradition_code(self, tradition=None):
        codes = {
            "wine": "WIN", "spirits": "SPR", "sake": "SAK", "coffee": "COF",
            "beer": "BER", "tea": "TEA", "ceremonial": "CER", "fortified": "FOR",
            "na": "NAL", "fermented": "FER", "water": "WAT"
        }
        return codes.get(tradition or self.tradition, "BEV")

    def _region_code(self, region=None):
        r = (region or self.region).lower()
        # Generate a short code from region name
        words = r.replace("—", " ").replace("-", " ").split()
        if len(words) >= 2:
            return (words[0][:3] + words[1][:3]).upper()
        return words[0][:6].upper() if words else "REG"

    def add_beverage(self, entry_data: dict) -> str:
        tc = self._tradition_code(entry_data.get("tradition", self.tradition))
        rc = self._region_code(entry_data.get("region", self.region))
        entry_data["entry_id"] = f"{tc}-{rc}-{self.current_entry:03d}"
        entry_data["tradition"] = entry_data.get("tradition", self.tradition)
        entry_data["region"] = entry_data.get("region", self.region)
        entry_data["extracted_at"] = datetime.now(timezone.utc).isoformat()
        entry_data["batch_number"] = self.batch_number + 1

        passed, failures = self.validator.validate(entry_data)

        if passed:
            self.current_batch.append(entry_data)
            self.current_entry += 1
            self.session_beverages += 1
            self.running_total += 1
            print(f"[BEVERAGE] {entry_data['entry_id']} | {entry_data.get('name', '')} | {entry_data.get('tradition', '')} | ✓ Sashimi")
            if len(self.current_batch) >= self.BATCH_SIZE:
                self.commit_batch()
            return entry_data["entry_id"]
        else:
            self._flag_entry(entry_data, failures)
            self.current_entry += 1
            self.session_flagged += 1
            print(f"[FLAGGED] {entry_data['entry_id']} | {entry_data.get('name', '')} | Missing: {', '.join([f.split(':')[0] for f in failures])}")
            return entry_data["entry_id"]

    def add_producer(self, producer_data: dict):
        tc = self._tradition_code(producer_data.get("tradition"))
        producer_data["producer_id"] = f"PROD-{tc}-{len(self.producers_found)+1:03d}"
        self.producers_found.append(producer_data)
        self.session_producers += 1

        # Log to producer directory
        fp = os.path.join(self.output_dir, "PRODUCER_DIRECTORY.md")
        with open(fp, "a") as f:
            f.write(f"### {producer_data.get('name', 'Unknown')}\n")
            f.write(f"**Location:** {producer_data.get('location', '')}\n")
            f.write(f"**Tradition:** {producer_data.get('tradition', '')}\n")
            f.write(f"**Key Person:** {producer_data.get('key_person', '')}\n")
            if producer_data.get("trail_connection"):
                f.write(f"**Trail:** {producer_data['trail_connection']}\n")
            f.write(f"**Verified:** {'Yes' if producer_data.get('verified') else 'NEEDS VERIFICATION'}\n\n---\n\n")

        print(f"[PRODUCER] {producer_data['producer_id']} | {producer_data.get('name', '')} | {producer_data.get('location', '')}")

    def add_purveyor(self, purveyor_data: dict):
        purveyor_data["purveyor_id"] = f"PURV-{len(self.purveyors_found)+1:03d}"
        self.purveyors_found.append(purveyor_data)
        self.session_purveyors += 1

        fp = os.path.join(self.output_dir, "PURVEYOR_LEADS.md")
        with open(fp, "a") as f:
            f.write(f"### {purveyor_data.get('name', 'Unknown')}\n")
            f.write(f"**Type:** {purveyor_data.get('type', '')}\n")
            f.write(f"**Markets:** {', '.join(purveyor_data.get('markets_served', []))}\n")
            f.write(f"**Traditions:** {', '.join(purveyor_data.get('traditions_carried', []))}\n")
            if purveyor_data.get("website"):
                f.write(f"**Website:** {purveyor_data['website']}\n")
            f.write(f"**Verified:** {'Yes' if purveyor_data.get('verified') else 'NEEDS VERIFICATION'}\n\n---\n\n")

        print(f"[PURVEYOR] {purveyor_data['purveyor_id']} | {purveyor_data.get('name', '')} | {', '.join(purveyor_data.get('markets_served', []))}")

    def commit_batch(self):
        if not self.current_batch:
            return
        self.batch_number += 1
        batch_file = os.path.join(
            self.output_dir, "batches",
            f"{self._tradition_code()}_{self._region_code()}_batch_{self.batch_number:03d}.json"
        )
        with open(batch_file, "w") as f:
            json.dump({
                "tradition": self.tradition,
                "region": self.region,
                "batch_number": self.batch_number,
                "entry_count": len(self.current_batch),
                "extracted_at": datetime.now(timezone.utc).isoformat(),
                "entries": self.current_batch
            }, f, indent=2, ensure_ascii=False)

        count = len(self.current_batch)
        self.current_batch = []
        self._save_state()

        # Also save producers and purveyors periodically
        if self.producers_found:
            prod_file = os.path.join(self.output_dir, "producers", f"producers_{self.batch_number:03d}.json")
            with open(prod_file, "w") as f:
                json.dump(self.producers_found, f, indent=2, ensure_ascii=False)

        if self.purveyors_found:
            purv_file = os.path.join(self.output_dir, "purveyors", f"purveyors_{self.batch_number:03d}.json")
            with open(purv_file, "w") as f:
                json.dump(self.purveyors_found, f, indent=2, ensure_ascii=False)

        print(f"[BATCH] {count} beverages | {self.session_producers} producers | {self.session_purveyors} purveyors | "
              f"Flagged: {self.session_flagged} | Running total: {self.running_total}")

    def _flag_entry(self, entry_data, failures):
        fp = os.path.join(self.output_dir, "FLAGGED_FOR_REVIEW.md")
        with open(fp, "a") as f:
            f.write(f"### {entry_data.get('entry_id', '?')} — {entry_data.get('name', '?')}\n")
            f.write(f"**Tradition:** {entry_data.get('tradition', '')}\n")
            f.write(f"**Region:** {entry_data.get('region', '')}\n")
            for failure in failures:
                f.write(f"- {failure}\n")
            f.write(f"\n---\n\n")

    def switch_region(self, new_tradition, new_region):
        if self.current_batch:
            self.commit_batch()
        self.completed_regions.append(f"{self.tradition} — {self.region}")
        old = f"{self.tradition} — {self.region}"
        self.tradition = new_tradition
        self.region = new_region
        self.current_entry = 1
        self._load_state()
        self._save_state()
        print(f"[REGION COMPLETE] {old} | [OPENING] {new_tradition} — {new_region}")

    def finish(self):
        if self.current_batch:
            self.commit_batch()
        self._save_state()
        handoff = self._generate_handoff()
        hf = os.path.join(self.output_dir, "sessions",
                          f"HANDOFF_{datetime.now().strftime('%Y%m%d')}_{self.session_number:02d}.md")
        with open(hf, "w") as f:
            f.write(handoff)
        print("=" * 70)
        print(handoff)
        return handoff

    def _generate_handoff(self):
        return f"""BEVERAGE EXTRACTION HANDOFF
===========================
Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
Session: #{self.session_number}
Tradition: {self.tradition}
Region: {self.region}
Beverages this session: {self.session_beverages}
Producers this session: {self.session_producers}
Purveyors this session: {self.session_purveyors}
Flagged: {self.session_flagged}
Batches written: {self.batch_number}
Running total: {self.running_total}
Completed regions: {', '.join(self.completed_regions) if self.completed_regions else 'none'}
Next entry: {self._tradition_code()}-{self._region_code()}-{self.current_entry:03d}
"""


# ============================================================================
# EXTRACTION QUEUE — Global, Mediterranean-first, Trail-connected
# ============================================================================

BEVERAGE_EXTRACTION_QUEUE = [
    # PRIORITY A — Portuguese Colonial Trail Beverages (fill the trail architecture)
    {"tradition": "fortified", "region": "Portugal — Douro Valley (Port)", "code": "PCT-1", "priority": 1, "targets": 30},
    {"tradition": "fortified", "region": "Portugal — Madeira", "code": "PCT-2", "priority": 2, "targets": 15},
    {"tradition": "wine", "region": "Portugal — Vinho Verde, Dão, Alentejo", "code": "PCT-1", "priority": 3, "targets": 25},
    {"tradition": "spirits", "region": "Portugal — Ginjinha, Licor Beirão", "code": "PCT-1", "priority": 4, "targets": 10},
    {"tradition": "spirits", "region": "India — Goa (Feni)", "code": "PCT-8", "priority": 5, "targets": 10},
    {"tradition": "spirits", "region": "Brazil — Cachaça regions", "code": "PCT-13", "priority": 6, "targets": 20},
    {"tradition": "coffee", "region": "Brazil — Santos, Cerrado, Sul de Minas", "code": "PCT-13", "priority": 7, "targets": 15},
    {"tradition": "ceremonial", "region": "Malacca — Kristang beverage traditions", "code": "PCT-9", "priority": 8, "targets": 8},
    {"tradition": "coffee", "region": "Macau — Portuguese café culture", "code": "PCT-10", "priority": 9, "targets": 5},
    {"tradition": "spirits", "region": "Cape Verde — Grogue", "code": "PCT-4", "priority": 10, "targets": 5},
    {"tradition": "spirits", "region": "Caribbean — Rum (PCT×WADT)", "code": "PCT/WADT", "priority": 11, "targets": 25},
    {"tradition": "coffee", "region": "Hawaii — Kona, Ka'u (PCT×PMT)", "code": "PCT-14", "priority": 12, "targets": 10},

    # PRIORITY B — Pacific Migration Trail Beverages
    {"tradition": "ceremonial", "region": "Pacific Islands — Kava", "code": "PMT", "priority": 13, "targets": 20},
    {"tradition": "spirits", "region": "Philippines — Lambanog, Tuba", "code": "PMT-2", "priority": 14, "targets": 8},
    {"tradition": "fermented", "region": "Pacific — Coconut toddy traditions", "code": "PMT", "priority": 15, "targets": 10},

    # PRIORITY C — West African Diaspora Trail Beverages
    {"tradition": "fermented", "region": "West Africa — Palm wine", "code": "WADT-1", "priority": 16, "targets": 10},
    {"tradition": "spirits", "region": "USA — Bourbon (Nearest Green)", "code": "WADT-3", "priority": 17, "targets": 15},
    {"tradition": "spirits", "region": "Haiti — Clairin", "code": "WADT-2", "priority": 18, "targets": 8},
    {"tradition": "coffee", "region": "Ethiopia — Yirgacheffe, Sidamo, Harrar", "code": "WADT-1", "priority": 19, "targets": 15},
    {"tradition": "ceremonial", "region": "Ethiopia — Buna ceremony", "code": "WADT-1", "priority": 20, "targets": 5},

    # PRIORITY D — Mediterranean Beverages (connects to French collection)
    {"tradition": "wine", "region": "France — Burgundy", "priority": 21, "targets": 40},
    {"tradition": "wine", "region": "France — Bordeaux", "priority": 22, "targets": 35},
    {"tradition": "wine", "region": "France — Rhône", "priority": 23, "targets": 25},
    {"tradition": "wine", "region": "France — Champagne", "priority": 24, "targets": 20},
    {"tradition": "wine", "region": "France — Loire", "priority": 25, "targets": 20},
    {"tradition": "wine", "region": "France — Alsace", "priority": 26, "targets": 15},
    {"tradition": "spirits", "region": "France — Cognac, Armagnac, Calvados", "priority": 27, "targets": 20},
    {"tradition": "spirits", "region": "France — Pastis (Marseille crossroads)", "priority": 28, "targets": 5},
    {"tradition": "wine", "region": "Italy — Piedmont", "priority": 29, "targets": 30},
    {"tradition": "wine", "region": "Italy — Tuscany", "priority": 30, "targets": 25},
    {"tradition": "wine", "region": "Italy — Veneto", "priority": 31, "targets": 15},
    {"tradition": "spirits", "region": "Italy — Grappa, Amaro, Limoncello", "priority": 32, "targets": 15},
    {"tradition": "wine", "region": "Spain — Rioja, Ribera del Duero, Priorat", "priority": 33, "targets": 25},
    {"tradition": "fortified", "region": "Spain — Sherry (Jerez)", "priority": 34, "targets": 15},
    {"tradition": "wine", "region": "Greece — Santorini, Crete, Naoussa", "priority": 35, "targets": 15},
    {"tradition": "spirits", "region": "Greece — Ouzo, Tsipouro, Tsikoudia", "priority": 36, "targets": 8},
    {"tradition": "spirits", "region": "Lebanon — Arak", "priority": 37, "targets": 5},
    {"tradition": "ceremonial", "region": "Morocco — Mint tea ceremony", "priority": 38, "targets": 8},
    {"tradition": "ceremonial", "region": "Turkey — Coffee ceremony (ibrik)", "priority": 39, "targets": 5},

    # PRIORITY E — East Asian
    {"tradition": "sake", "region": "Japan — Niigata, Fushimi, Nada", "priority": 40, "targets": 30},
    {"tradition": "spirits", "region": "Japan — Shōchū, Awamori", "priority": 41, "targets": 15},
    {"tradition": "tea", "region": "Japan — Matcha, Sencha, Gyokuro", "priority": 42, "targets": 20},
    {"tradition": "ceremonial", "region": "Japan — Chanoyu tea ceremony", "priority": 43, "targets": 8},
    {"tradition": "tea", "region": "China — Gongfu (Pu-erh, Oolong, White, Green)", "priority": 44, "targets": 25},
    {"tradition": "spirits", "region": "China — Baijiu", "priority": 45, "targets": 10},
    {"tradition": "tea", "region": "Taiwan — High mountain oolong", "priority": 46, "targets": 10},
    {"tradition": "tea", "region": "India — Darjeeling, Assam, Nilgiri", "priority": 47, "targets": 15},

    # PRIORITY F — New World Wine & Spirits (expand PNW context)
    {"tradition": "wine", "region": "USA — Napa, Sonoma", "priority": 48, "targets": 25},
    {"tradition": "wine", "region": "Australia — Barossa, McLaren Vale, Yarra", "priority": 49, "targets": 20},
    {"tradition": "wine", "region": "New Zealand — Marlborough, Central Otago", "priority": 50, "targets": 15},
    {"tradition": "wine", "region": "Argentina — Mendoza", "priority": 51, "targets": 15},
    {"tradition": "wine", "region": "Chile — Colchagua, Maipo", "priority": 52, "targets": 15},
    {"tradition": "wine", "region": "South Africa — Stellenbosch, Swartland", "priority": 53, "targets": 15},
    {"tradition": "spirits", "region": "Scotland — Single Malt regions", "priority": 54, "targets": 25},
    {"tradition": "spirits", "region": "Mexico — Mezcal, Tequila", "priority": 55, "targets": 20},
    {"tradition": "beer", "region": "Belgium — Trappist, Lambic, Gueuze", "priority": 56, "targets": 20},
    {"tradition": "beer", "region": "Germany — Reinheitsgebot traditions", "priority": 57, "targets": 15},

    # PRIORITY G — Non-Alcoholic & Fermented (fastest-growing market)
    {"tradition": "na", "region": "Global — Dealcoholised wine", "priority": 58, "targets": 10},
    {"tradition": "na", "region": "Global — NA spirits", "priority": 59, "targets": 10},
    {"tradition": "fermented", "region": "Global — Kombucha, Kefir, Tepache", "priority": 60, "targets": 15},
    {"tradition": "ceremonial", "region": "Mesoamerica — Cacao ceremony", "priority": 61, "targets": 5},
    {"tradition": "ceremonial", "region": "Argentina — Mate", "priority": 62, "targets": 5},
]


# ============================================================================
# CLI
# ============================================================================

def print_queue():
    print("\nPROVENANCE BEVERAGE EXTRACTION QUEUE\n")
    print(f"{'#':<4} {'Tradition':<14} {'Region':<45} {'Trail':<10} {'Targets'}")
    print("-" * 90)
    total = 0
    for item in BEVERAGE_EXTRACTION_QUEUE:
        trail = item.get("code", "—")
        print(f"{item['priority']:<4} {item['tradition']:<14} {item['region']:<45} {trail:<10} {item['targets']}")
        total += item["targets"]
    print(f"\n{'TOTAL TARGETS:':<65} {total}")
    print(f"\nNote: Each target decomposes into 2-5 sub-technique entries at sashimi depth.")
    print(f"Estimated total entries: {total * 3}–{total * 4}")


def quick_start(tradition, region, **kwargs):
    return BeverageSession(tradition=tradition, region=region, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "queue":
        print_queue()
    else:
        print("PROVENANCE BEVERAGE EXTRACTION ENGINE v1")
        print("Commands: queue")
        print("\nOr import in Python:")
        print("  from beverage_extractor import BeverageSession")
        print("  session = BeverageSession('wine', 'France — Burgundy')")