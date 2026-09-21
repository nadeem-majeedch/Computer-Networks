# Assessment Package Audit Report (2026-09-20)

| Field | Value |
|---|---|
| Phase | Assessment package build (`assessments/`) |
| Auditors | `tools/scripts/audit_assessment.py` (12 checks) + `tools/scripts/verify_assessment_numbers.py` (99 numeric checks) + full regression of the four existing audit tools |
| Result | **Assessment: 12 PASS / 0 WARN / 0 FAIL · Numerics: 99/99 PASS · Foundation 15/15 · Lectures 13 PASS + 1 WARN · Labs 9/9 · Lab syntax PASS · Case bank 10/10** |
| Scope of change | `assessments/` (45 files), `tools/scripts/audit_assessment.py` (new), `tools/scripts/verify_assessment_numbers.py` (new); no prior content modified except status lines |
| Commit status | Nothing committed or pushed (per workflow) |

## 1. What was built

| Component | Files | Contents |
|---|---|---|
| Top-level | 4 | README (weighting caveat, key-separation conventions), CLO item-level mapping, academic-integrity guidance, shared marking guide |
| Weekly quizzes | 16 | W01–W16, each covering its week's 2 lectures (W1=L01–02 … W16=L31–32), 6–8 items + instructor key |
| Review sets | 8 | By module (M1–M8), 3–4 questions per lecture + self-check keys |
| Question banks | 7 | Conceptual (35), numerical/subnetting (25), packet-analysis (15 + 7 synthetic excerpts), routing/troubleshooting (16), short-answer (27), long-answer (13 with marking outlines), practical (13) |
| Assignment briefs | 4 | Subnetting problem set (5% instrument) + reliable-transport project (10% instrument), student & instructor versions each |
| Exams | 4 | Midterm (90 min, 60 marks, Modules 1–3) and Final (120 min, 70 marks, cumulative M4–8 emphasis + synthesis), student & instructor versions with marking schemes |
| Rubrics | 2 | Practical-work (40/30/20/10 per strategy §3.2) and capstone (stage weights 25/20/20/20/15 per strategy §3.7, peer factor ±10%) |

## 2. Alignment results (from `audit_assessment.py` output)

- **Inventory**: all 45 expected files present; student/instructor separation enforced (keys fenced in quizzes/reviews/banks; separate files for exams/assignments).
- **Duplicate stems**: 112 distinct stems across the package, **zero cross-file duplicates** — the README §3 reuse rule holds mechanically for exact duplication.
- **Tag validity**: only CLO1–CLO8 and B/I/A/E difficulty tags occur.
- **Exam consistency**: parsed from the papers themselves — midterm 18+24+18 = 60 at 90 min; final 21+28+21 = 70 at 120 min.
- **Coverage**: every CLO is item-mapped (`clo-assessment-mapping.md`); the strategy's instrument set is fully realized — the only unbuilt instrument remains the CS-01…03 evidence bundles (owned by the case-study phase, see §5).

## 3. Numerical verification (`verify_assessment_numbers.py`, 99 checks)

Machine-checked with the standard-library `ipaddress` module and direct arithmetic:
all [MC]-tagged subnet ranges/masks/membership tests, VLSM allocations (incl. the
quiz-W07, review-M3-Q4, bank-N-05, and both exam plans), Nyquist/Shannon values, BDP
and implied-window calculations, TCP seq/ack arithmetic (quiz W09, bank N-14, exam
C-items), growth compounding (N-22), and efficiency/overhead percentages.

**Errors the verification pass caught and fixed during the build** (real key bugs):

1. Bank N-06: 250 GB was misconverted (1.6×10¹³ bits / 16 000 s); corrected to
   2.5×10¹¹ B = 2×10¹² bits = **2 000 s ≈ 33.3 min**.
2. Review M3 Q4: the original subnet sizes (100/50/30/10/10/2 = 260 addresses needed)
   **cannot fit** a /24; the question now uses feasible sizes (100/50/30/10/6/2 = 252)
   with a clean key, and the instructor note documents the overflow variant.
3. Two checker bugs in `verify_assessment_numbers.py` itself (an over-narrow broadcast
   pattern; integer vs dotted-quad rendering) — fixed; content was correct.

## 4. Audit findings fixed before sign-off

| Finding | Resolution |
|---|---|
| 5 banks missing a difficulty tier (B/I/A/E) | One new item each added with key: N-25 (E, multi-constraint VLSM design), PA-15 (E, latency attribution on synthetic excerpt G), RT-16 (B, return-path checklist), SA-27 (A, window–RTT mechanism), LA-13 (B, taxonomy narrative) |
| Exam-consistency check string-matched instead of parsing | Checker now parses section marks and verifies the sum against the paper's total |
| Broken link `../docs/references-policy.md` in academic-integrity.md | Replaced with the real reference discipline (syllabus reading list + lecture References sections) |

## 5. Honest limitations (all flagged in-package)

1. **No item has been sat by real students.** Every instrument still requires an
   instructor solve-through before first use (the strategy's ITI rule); [DC]-tagged
   (desk-check-only) answers in instructor keys must be re-verified then.
2. **Weightings are the proposed plan** (strategy §2 draft) — the package marks
   instrument-local totals (60/70 marks) so any final weighting survives.
3. **Graded-quiz windows disagree across foundation docs** (strategy §2: W04/W07/W10/
   W13 best-two-of-four; syllabus+schedule: W04/W12). The weekly papers support either
   resolution; `audit_assessment.py` keeps the reconciliation note visible (README §5)
   until the instructor resolves it.
4. **Near-duplicate review** (same skill, reworded) is not mechanically checkable —
   listed as a pre-release instructor task.
5. **Exam duration for the final (120 min) is proposed** — strategy §3.8 fixes format,
   not duration.

## 6. Regression status

| Tool | Result |
|---|---|
| `audit_foundation.py` | 15 PASS / 0 FAIL |
| `audit_lectures.py` | 13 PASS + 1 WARN (slide decks — pre-existing) / 0 FAIL |
| `audit_labs.py` | 9 PASS / 0 FAIL |
| `check_lab_syntax.py` | 36/36 blocks parse |
| `audit_casebank.py` | 10 PASS / 0 FAIL |
| `audit_assessment.py` (new) | 12 PASS / 0 FAIL |
| `verify_assessment_numbers.py` (new) | 99/99 PASS |
