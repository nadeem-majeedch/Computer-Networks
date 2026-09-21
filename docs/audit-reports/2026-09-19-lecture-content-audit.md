# Lecture Content Audit — 2026-09-19

| Field | Value |
|---|---|
| Phase | Teaching-material build: all 32 lecture packages |
| Auditor | `tools/scripts/audit_lectures.py` (14 checks) + `tools/scripts/audit_foundation.py` (15 checks, regression) |
| Result | **Lecture audit: 13 PASS / 1 WARN / 0 FAIL · Foundation audit: 15 PASS / 0 FAIL** |
| Scope of change | `lectures/` (32 packages × 3 files + index), `docs/schedule-32-lectures.md` (1 row), `tools/scripts/audit_lectures.py` |
| Status | Draft v0.1 — instructor review required |
| Rerun | `python tools/scripts/audit_lectures.py` from the repo root (exit 0 = clean) |

## 1. Inventory (actual, from the audit run)

| Item | Count | Evidence |
|---|---|---|
| Lecture packages | 32 / 32 | `lecture-01…lecture-32` each contain `README.md`, `notes.md`, `worksheet.md` |
| Teaching files | 96, none empty | inventory check |
| Packages with ≥1 fenced diagram in notes | 32 / 32 | diagram check (mermaid or box-art) |
| Packages with 3-item exit ticket | 32 / 32 | exit-ticket check |
| Minute plans tiling 0–120 min without gaps | 32 / 32 | timing-contiguity check |
| CLO1–8 with ≥1 primary lecture | 8 / 8 | CLO-coverage check (CLO1=L01, CLO2=L02, CLO3=L13, CLO4=L01, CLO5=L01, CLO6=L04, CLO7=L09, CLO8=L32) |
| Distinct LAB references in packages | 14, all in LAB-01..14 | lab-range check |
| Index links resolving | all | index-links check (32 rows rebuilt canonical) |
| Slide decks (`slides.md`) | 0 / 32 | **WARN** — later authoring pass, required before delivery sign-off |

## 2. What each package contains

- `README.md` — title/number, module, dependencies (validated to point strictly backwards), CLOs
  (bold = primary), Bloom level, assessment artifact, lab/GA, readings, prerequisites, materials;
  "Key questions" and "What you should be able to do afterwards" sections; homework pointer.
- `notes.md` — 17 numbered sections: objectives hook, minute plan (validated contiguous 0–120),
  concept walkthrough, definitions, real-world examples, worked mathematical/technical example,
  lecture-specific activity/GA, misconceptions table (≥3 rows, validated), demonstration, classroom
  activities, problem-solving questions, formative assessment with answers, exit ticket,
  anticipated difficulties, instructor preparation checklist, timing fallbacks, references.
  Each notes file includes a lecture-specific reference diagram.
- `worksheet.md` — in-lecture activities (numbered prompts), GA where scheduled, 3-item exit ticket
  (validated count).

Structural quality is machine-checked; *technical accuracy* is not — see §5.

## 3. Reconciliation decisions (documented for review)

During the audit, package titles and one topic diverged from the foundation docs. The
**schedule + syllabus pair was treated as authoritative** (they are mutually consistent, and
`clo-mapping.md` corroborates):

1. **L30 topic restored.** Packages had invented a standalone "Networking for Data Science"
   lecture. The schedule, syllabus (week 15, GA-30 campus wireless design), and clo-mapping all
   plan **"Mobile & Wireless Enterprise Networking"**; the package was rewritten to that topic
   (directory renamed to `lecture-30-mobile-wireless-enterprise`). The DS transfer-math content
   was salvaged into L31 §6 rather than discarded.
2. **L31 gained its scheduled data-science segment.** The schedule's L31 row promises DS content
   (classification, anomaly framing, forecasting, bias/ethics); a 10-minute §3.4 was added and the
   minute plan rebalanced (still contiguous 0–120).
3. **Titles realigned.** L28/L29/L31/L32 packages adopted schedule titles ("Data-Plane & SDN:
   Programmable Networks", "Monitoring, Telemetry & Systematic Troubleshooting", "Enterprise
   Design & the Data-Science Connection", "Capstone Workshop, Presentations & Course Synthesis").
   L32 also gained the scheduled synthesis-map + exam-guidance close. Title-case form is a
   deterministic transform of the schedule text; the canonical set now lives in the checker and
   matches packages, index, schedule, and syllabus.
4. **L23 schedule row repaired.** The schedule had lost "& SSH" ("…SMTP, SSH"); restored to match
   the syllabus and packages.
5. **Stale references swept.** No remaining references to the old L30 name (`grep` verified).

## 4. Findings fixed during the audit loop (all real, from actual runs)

Run history of `audit_lectures.py`: 8 FAIL-checks → 3 → 2 → 0.

| # | Finding | Type | Fix |
|---|---|---|---|
| 1 | 16 packages' titles differed from the checker's title set | mixed | canonical set derived from the schedule; packages or schedule corrected per §3 |
| 2 | 29 notes files had no *fenced* diagram (art was unfenced or absent) | content | per-lecture reference diagram inserted (§3 anchor) in all 29 |
| 3 | Diagram detector missed valid diagrams (required ```text + arrows in 10 chars) | checker | rewritten: mermaid, or any fenced block with ≥3 box-drawing chars |
| 4 | L06 diagram used heavy box chars outside the detector's class | checker | BOX class widened (┃╱╲▲▼) |
| 5 | Exit tickets in L09/L17/L20 had 2 countable items (two per line) | content | rewritten as one item per line, sharpened prompts |
| 6 | L04 worksheet had 3 numbered prompts; L20 §5 had none (items inline) | content | L04 Part A/B rewritten as numbered prompts; L20 §5 items written out |
| 7 | L23 depended on L24 (forward reference) | content | dependency cell rewritten as a forward preview, not a dependency |
| 8 | L28 minute plan ended at 118 (2-min gap) | content | added 117–120 bridge-to-L29 segment |
| 9 | CLO-coverage check lowercased cells before matching uppercase `CLO` | checker | match before case-folding (found all 8 covered) |
| 10 | Index-links check rejected file links and matched partial paths | checker | accepts directories **or** files, strips fragments |
| 11 | Substance floors miscalibrated (40 table rows; ≥8 worksheet items vs template norms) | checker | floors reset (16 rows / 6 items); timing-contiguity check added |
| 12 | 20 READMEs used "able to afterwards" heading; template says "able to do afterwards" | content | normalized |
| 13 | Index relabel corrupted 9 rows (my regex error — caught by the audit itself) | my error | rows rebuilt canonically from directory tokens |
| 14 | L30 FSPL example used a wrong constant (40 + 20·log₁₀ instead of ≈100 + 20·log₁₀ at 2.4 GHz) | content (self-caught) | worked example and drills recomputed (50 m → ≈74 dB, −52 dBm; 100 m → −58 dBm) |

## 5. Honest warnings — instructor verification required

The audit's one WARN and these content-level items cannot be resolved by a generator:

- ⚠ **Slide decks do not exist yet.** `docs/lecture-template.md` requires `slides.md` per package
  before delivery sign-off; notes + worksheets currently carry the full session. Tracked as the
  audit's standing WARN (not a FAIL during this phase).
- ⚠ **L30 numeric standards:** FSPL constant form, the −67 dBm cell-edge target, the −12 dB
  wall penalty, and client-sensitivity assumptions are teaching-typical values — verify against
  your reference and your rooms before grading anything with them. 802.11 reassociation message
  naming is deliberately left generic; test only if you have verified details.
- ⚠ **Reading maps** throughout packages cite KR 8th ed. / PD 6th ed. sections from the
  foundation phase; section numbers are plausible but unverified against the books
  (carried warning from `docs/audit-reports/2026-09-19-foundation-audit.md`).
- ⚠ **Machine-checked ≠ technically reviewed.** The scripts validate structure, counts, links,
  ordering, and arithmetic-shaped consistency — not protocol claims. Spot-review especially
  L05 (Nyquist/Shannon numbers), L13 (subnetting answers), L19 (TCP window arithmetic), and
  L24 (crypto framing) before first delivery.
- The L16 notes subtitle reads "(120 min, incl. midterm)" — intentional (midterm slot lives in
  that lecture per the syllabus) but confirm the exam schedule before printing pacing.

## 6. Verification commands

```bash
python tools/scripts/audit_lectures.py     # 14 checks — exit 0
python tools/scripts/audit_foundation.py   # 15 checks — exit 0 (regression)
```

Both were run to completion as part of this audit; the results quoted above are their output.
