# Canon Depth Ledger

> **Canon identity field:** `canon_slug` on `technique_references`.
> Section-level structure carried by `section_slug`.

## Per-Session Rules

1. **Minimum floor:** every extraction session owes **80 entries** against an enumerated structure. A depth-pass top-up session owes **40 entries**.
2. **"Covered" is never a stopping condition.** Only the floor, the wave plan, or an explicit stop-rule ends a run.
3. Sessions must name their target canon and wave before beginning work.
4. Entries land in the wave/section they were planned against — no orphan dumps.

---

## Live Canon Census

*Snapshot: 2026-06-12 — 12 629 total entries across 56 canon slugs.*

### Band Definitions

| Band | Label | Entry Range | Character |
|------|-------|-------------|-----------|
| **A** | Civilizational | 800 + | Deep multi-wave; sub-canon wave structure required |
| **B** | Major National | 300–799 | Broad single-thread; wave structure recommended |
| **C** | Focused Regional | 80–299 | Targeted passes; session-sized |
| **D** | Seed / Emerging | < 80 | Bootstrapping; needs full first-wave plan |

---

### Band A — Civilizational Canons

| Canon | Live Count | Band | Sub-Canon Wave Structure |
|-------|-----------|------|--------------------------|
| **japanese** | 3 809 | A | See [Wave Table: Japanese](#wave-table-japanese) |
| **italian** | 1 622 | A | See [Wave Table: Italian](#wave-table-italian) |
| **french** | 1 526 | A | See [Wave Table: French](#wave-table-french) |
| **chinese** | 937 | A | See [Wave Table: Chinese](#wave-table-chinese) |
| **beverage-terroir** | 879 | A | See [Wave Table: Beverage-Terroir](#wave-table-beverage-terroir) |

### Band B — Major National Canons

| Canon | Live Count | Band | Next Planned Wave |
|-------|-----------|------|-------------------|
| **indian** | 431 | B | Regional depth: Rajasthani, Chettinad, Malayali — target 500+ |
| **thai** | 402 | B | Regional depth: Isan, Southern, Northern hill — target 500 |
| **mexican** | 313 | B | Method wave (the-method section is empty); regional consolidation — target 450 |
| **korean** | 257 | C→B | Fermentation + banchan depth pass — target 350 |

### Band C — Focused Regional Canons

| Canon | Live Count | Band | Next Planned Wave |
|-------|-----------|------|-------------------|
| **general** | 261 | C | Poissonnier + entremetier completion |
| **null (food-science/modernist)** | 256 | C | Assign canon_slug; consolidate under `modernist` |
| **indonesian** | 205 | C | Canonical-dishes wave (currently 0 in that section) |
| **american** | 194 | C | Regional BBQ + soul-food depth |
| **hawaiian** | 171 | C | Plate-lunch + poke depth pass |
| **spanish** | 166 | C | Regional tapas: Basque, Andalusian, Galician |
| **levantine** | 150 | C | Meze + preservation techniques |
| **provenance-1000** | 134 | C | Cross-canon showcase rotation |
| **corsican** | 97 | C | Charcuterie + cheese depth |
| **moroccan** | 81 | C | Tagine variants + pastilla family |

### Band D — Seed / Emerging Canons

| Canon | Live Count | Band | Next Planned Wave |
|-------|-----------|------|-------------------|
| **kristang** | 76 | D | Debal + curry devil depth — target 100 |
| **turkish** | 68 | D | Kebab family + meze — target 120 |
| **vietnamese** | 61 | D | Pho + bún family + fermentation — target 120 |
| **portuguese** | 59 | D | Bacalhau family + pastéis — target 120 |
| **latin-american** | 46 | D | Consolidation pass; move entries to national canons where possible |
| **middle-eastern** | 41 | D | Merge/disambiguate with levantine; kibbeh + flatbread |
| **scandinavian** | 38 | D | Curing + fermentation + smørrebrød — target 100 |
| **british** | 35 | D | Pies, puddings, roasts — target 100 |
| **greek-levantine** | 35 | D | Merge/disambiguate with levantine; phyllo + meze |
| **filipino** | 24 | D | Active relay (Relay-05); adobo + kinilaw + regional — target 100 |
| **maori** | 23 | D | Hāngi + kai moana depth — target 80 |
| **caribbean** | 20 | D | Jerk family + rice-and-peas — target 80 |
| **argentine** | 19 | D | Asado + empanada + chimichurri — target 80 |
| **burmese** | 18 | D | Mohinga + laphet + curries — target 80 |
| **british-irish** | 15 | D | Merge with british or split; stews + baking |
| **ethiopian** | 14 | D | Injera + wot family — target 80 |
| **german-austrian** | 14 | D | Sausage + bread + schnitzel family — target 80 |
| **jewish-diaspora** | 14 | D | Ashkenazi + Sephardi splits — target 80 |
| **brazilian** | 13 | D | Churrasco + moqueca + feijoada — target 80 |
| **peruvian** | 13 | D | Ceviche + anticuchos + ají — target 80 |
| **southeast-asian** | 12 | D | Redistribute to national canons; umbrella cleanup |
| **lao** | 11 | D | Laap + or lam + fermentation — target 80 |
| **cambodian** | 8 | D | Prahok + amok + kroeung — target 80 |
| **nigerian** | 8 | D | Jollof + egusi + pepper soup — target 80 |
| **georgian** | 7 | D | Khinkali + khachapuri + satsivi — target 80 |
| **indigenous-australian** | 7 | D | Bush-tucker + earth-oven — target 40 (respectful scope) |
| **sri-lanka** | 6 | D | Hoppers + sambols + curries — target 80 |
| **east-african** | 5 | D | Merge with ethiopian or split regional |
| **central-asian** | 4 | D | Plov + manti + lagman — target 80 |
| **uzbek** | 4 | D | Merge into central-asian; plov + samsa |
| **ghanaian** | 4 | D | Jollof + fufu + groundnut soup — target 80 |
| **west-african** | 4 | D | Redistribute to national canons; umbrella cleanup |
| **senegalese** | 3 | D | Thiéboudienne + yassa — target 80 |
| **swahili-coast** | 3 | D | Pilau + biryani-coast + coconut — target 80 |
| **uyghur** | 3 | D | Merge into central-asian; laghman + kawap |
| **central-african-bantu** | 2 | D | Fufu + saka-saka — target 40 |
| **kazakh** | 1 | D | Merge into central-asian; beshbarmak |

---

## Civilizational Sub-Canon Wave Structure

### Wave Table: Japanese

| Wave | Section Slug | Current Count | Status |
|------|-------------|---------------|--------|
| J-W1 | `the-method` | 1 448 | Active — depth passes continue |
| J-W2 | `the-canonical-dishes` | 1 102 | Active — dish registration continues |
| J-W3 | `overview-cultural-context` | 229 | Active — cultural threads |
| J-W4 | *(unassigned / NULL section)* | 852 | Cleanup: assign to W1–W3 or new wave |
| J-W5 | `food-culture-and-tradition` | 28 | Seed wave |
| J-W6 | `ingredients-and-procurement` | 27 | Seed wave |
| J-W7 | Minor sections (< 15 each) | 123 | Consolidate or merge |
| **Next wave:** | J-W4 cleanup + J-W5/W6 depth to 80 each | | |

### Wave Table: Italian

| Wave | Section Slug | Current Count | Status |
|------|-------------|---------------|--------|
| I-W1 | `the-canonical-dishes` | 1 573 | Primary thread — deep |
| I-W2 | `the-method` | 49 | **Underdeveloped** — next priority |
| **Next wave:** | I-W2 method depth pass — target 200 | | |

### Wave Table: French

| Wave | Section Slug | Current Count | Status |
|------|-------------|---------------|--------|
| F-W1 | `the-canonical-dishes` | 1 388 | Primary thread — deep |
| F-W2 | `the-method` | 138 | Growing — depth pass warranted |
| **Next wave:** | F-W2 method depth pass — target 300 | | |

### Wave Table: Chinese

| Wave | Section Slug | Current Count | Status |
|------|-------------|---------------|--------|
| C-W1 | `the-canonical-dishes` | 715 | Primary thread |
| C-W2 | `the-method` | 222 | Growing |
| **Next wave:** | C-W1 regional dish expansion (Sichuan, Cantonese, Fujian, Hunan) — target 1 000 | | |

### Wave Table: Beverage-Terroir

| Wave | Section Slug(s) | Current Count | Status |
|------|----------------|---------------|--------|
| B-W1 | `beverage-and-pairing` | 146 | Core pairing reference |
| B-W2 | `provenance-500-drinks-*` (10 sections) | 500 | Structured 500 initiative |
| B-W3 | Regional wine terroir sections | ~60 | Scattered; needs consolidation |
| B-W4 | Tea culture sections | ~25 | Chinese tea deep-dive |
| B-W5 | Spirits + craft sections | ~148 | Mixed; needs section cleanup |
| **Next wave:** | B-W3 consolidation + B-W4 depth to 80 | | |

---

## Campaign Priority Queue

1. **Italian W2** — `the-method` has only 49 entries against 1 573 dishes. Severe imbalance.
2. **Japanese W4** — 852 entries with NULL `section_slug` need assignment.
3. **Chinese W1** — Regional dish expansion toward 1 000.
4. **Korean** — Promote to Band B; fermentation + banchan wave.
5. **Mexican** — Method section build-out; regional consolidation.
6. **Filipino** — Active relay; continue to 100.
7. **Band D first-wave targets** — Any canon below 80 needs a bootstrap session.
