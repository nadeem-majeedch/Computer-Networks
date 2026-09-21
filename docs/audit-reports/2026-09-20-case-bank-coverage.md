# Case Study Bank — Coverage & Quality Report (2026-09-20)

| Field | Value |
|---|---|
| Phase | Problem-solving case bank (`case-studies/`) |
| Auditor | `tools/scripts/audit_casebank.py` (10 checks) + full regression of the four existing audit tools |
| Result | **Case bank: 10 PASS / 0 WARN / 0 FAIL · Foundation 15/15 · Lectures 13 PASS + 1 WARN · Labs 9/9 · Lab syntax: PASS** |
| Scope of change | `case-studies/` (66 files: 65 cases + README), `tools/scripts/audit_casebank.py` (new), README/`docs/repository-structure.md` status rows |
| Status | Draft v0.1 — awaiting instructor review. Nothing committed or pushed. |

---

## 1. What was built

**65 case files** (`PB-001…PB-065`), each a single Markdown file with a student-facing
top half and an instructor-only bottom half (`<!-- INSTRUCTOR-ONLY BELOW -->`), plus a
regenerated bank README with machine-built indexes (§5 DS list, §6 by-lecture,
§7 by-difficulty, §8 by-topic). Per-case element set (16, audit-enforced): ID ·
difficulty · mapped lecture(s)+CLOs+slot+topic · scenario · problem statement ·
labeled synthetic evidence pack · constraints · ≥3 student questions · expected
learning outcomes · hints (instructor half only) · instructor solution · reasoning
process · common incorrect approaches · extension question · 4-level rubric ·
references.

**Counting decision (exceeds the 64 target, explained):** 65 cases — exactly two per
lecture for L01–L27 and L30–L32, **three for L29** (monitoring: PB-056 probe design,
PB-057 polling-vs-events, PB-058 counter-arithmetic audit) and **two for L28** after a
late gap (PB-065) was filled. The brief's "at least 64, two per lecture where
educationally appropriate" is met; the L29 bonus reflects monitoring's three distinct
sub-skills (probe design, sampling vs events, measurement integrity).

## 2. Coverage

| Dimension | Result |
|---|---|
| Lecture coverage | **32/32** (audit: lecture-coverage PASS); every lecture has ≥2 cases |
| Task categories | **22/22 required categories** present (audit: topic-coverage PASS), plus 3 course-specific extras (Application protocols, SDN, Monitoring) — 25 topic rows in §8 |
| Difficulty ramp | Beginner 26 / Intermediate 29 / Advanced 7 / Expert 3; **second case ≥ first within every lecture pair** (audit: ramp PASS); A/E concentrate in Modules 4–8 |
| DS integration | **19 DS-flagged cases** (curated list, §5): transfer/overhead math, window-bound and overhead-bound regimes, telemetry design, measurement bias, cluster sync design |
| Case-type mix | Calculation (≈14), diagnostic (≈28), conceptual/evidence-reading (≈10), design/trade-off (≈13) — not a configuration-exercise bank |

## 3. The one editorial decision worth knowing

IDs were assigned in writing order, which produced two lectures where the second case
was *easier* than the first (L27: Intermediate then Beginner; L31: Advanced then
Intermediate). Rather than weaken the ramp rule, **PB-053↔PB-054 and PB-061↔PB-062 were
swapped** (filenames, H1s, and the four affected cross-references: PB-061's two
references and PB-064's reference list). The bank README was regenerated from disk
afterwards, so §6 links match the new layout. Cross-reference integrity is now:
PB-062 (campus) ← PB-061 (small files) ← PB-064 (capstone defense); PB-006 ← PB-008 ←
PB-062; PB-016 ← PB-063.

## 4. What the audit verified (actual checks, not claims)

1. Inventory: 65 files, IDs sequential, no duplicates.
2. All 16 elements present in every case (zone-correct: student vs instructor half).
3. Student/instructor split present everywhere.
4. Difficulty ramp within each lecture.
5. Lecture coverage 32/32 with per-lecture counts of 2–3.
6. Task-category coverage: all 22 required categories (via a normalization map shared
   with the README generator — single source of truth for topic names).
7. Difficulty distribution sanity (beginner share ≥20%).
8. README index ↔ disk agreement: every case linked, no broken paths, total line
   matches.
9. Evidence policy: labeled synthetic evidence in every student half; no unlabeled
   command transcripts.
10. ID namespace: practice bank uses `PB-`; graded `CS-01…04` untouched.

Regression after the build: foundation audit 15/15, lecture audit 13 PASS + 1 WARN
(slide decks still pending — unchanged), lab audit 9/9, lab-syntax tool PASS.

## 5. Honest limitations (what the audit does NOT verify)

- **Numerics are desk-checked, not machine-verified.** Every calculation case's
  arithmetic was checked by hand during writing (FSPL 32.44 constant, BDP/window
  arithmetic, counter-wrap modular walks, detection probabilities), but the audit
  validates *structure*, not physics. The ⚠-flagged items inside cases (FSPL constant,
  802.11 thresholds, vendor fail-mode semantics, IW=10 model, MIB-II behavior) require
  instructor verification before first delivery — the per-case ⚠ marks are the checklist.
- **Expert tier is intentionally small (3).** Expert is defined strictly (incomplete
  requirements, no single right answer, defense-graded): PB-022, PB-052, PB-064. Several
  Advanced cases (PB-058, PB-061, PB-063) carry expert-like ambiguity; the report does
  not inflate the tier to look better.
- **PB-015 contains a deliberate internal inconsistency** (a note-taker's "unicast"
  label contradicted by the receive-set), resolved in the instructor guide. Instructors
  should read the instructor half before presenting — the case is designed to teach
  facts-vs-assumptions by being *slightly wrong on purpose*.
- **No real packet captures, logs, or measurements exist anywhere in the bank** — every
  evidence pack is labeled synthetic; captures students need are produced in the labs
  (LAB-01…16), whose own evidence rules govern them.
- The audit cannot judge pedagogy: whether a case's difficulty label matches a given
  cohort is an instructor judgment; the difficulty table in README §2 describes design
  intent.

## 6. Suggested instructor workflow

1. Skim both cases per lecture before teaching it (≈20 min each); swap any that clash
   with demo timing.
2. Verify the ⚠-flagged standards/vendor claims against your editions (the L30 FSPL
   constant and L29 MIB-II semantics first — they carry arithmetic).
3. Use the §6 index for in-lecture slots; the §7 index for tutorial/exam-pack assembly;
   §5 for DS-section assignments.
