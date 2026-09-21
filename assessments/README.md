# Assessment Package

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — **all weightings are the proposed plan** from [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) §2; adopt institutional weightings only after faculty approval |
| Parent documents | [`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) · [`../docs/clo-mapping.md`](../docs/clo-mapping.md) · [`../docs/syllabus.md`](../docs/syllabus.md) |

## 1. What lives here

| Path | Contents |
|---|---|
| [`clo-assessment-mapping.md`](clo-assessment-mapping.md) | Item-level CLO coverage: which package artifacts measure each CLO |
| [`quizzes/`](quizzes/) | 16 **weekly formative quizzes** (W01–W16, student questions + instructor key per file). Graded-quiz windows per strategy §2: W04, W07, W10, W13 |
| [`review/`](review/) | Lecture review questions by module (M1–M8), with answers — self-study |
| [`banks/`](banks/) | Question banks: conceptual · numerical/subnetting · packet-analysis · routing/troubleshooting · short-answer · long-answer · practical |
| [`assignments/`](assignments/) | Assignment briefs: subnetting problem set (5%), reliable-transport project (10%) |
| [`exams/`](exams/) | Midterm (W8) and Final (W16): separate student and instructor papers, marking schemes included |
| [`rubrics/`](rubrics/) | Consolidated rubrics: practical work (labs/GA) and capstone |
| [`academic-integrity.md`](academic-integrity.md) | Integrity, collaboration, AI-use and evidence-reproducibility rules |
| [`marking-guide.md`](marking-guide.md) | Marking conventions shared by every scheme in this package |

## 2. How student / instructor material is separated

- **Exams and assignment briefs** ship as separate `*-student.md` and `*-instructor.md`
  files — distribute only the student file.
- **Quizzes, review sets, and banks** are single files with the instructor key in a
  clearly fenced section at the end (`INSTRUCTOR KEY — DO NOT DISTRIBUTE`). Split them
  before publishing if your LMS cannot enforce access.

## 3. Question tagging convention

Every item carries `Difficulty` (**B**eginner / **I**ntermediate / **A**dvanced /
**E**xpert), `CLO(s)`, and `Source` (lecture `Lxx`, lab `LAB-xx`, GA-xx, case `PB-xxx`/
`CS-xx`). Banks and quizzes never reuse an item verbatim across instruments; where two
instruments test the same skill at different stakes (e.g., quiz item ↔ exam problem), the
numbers or the scenario differ.

## 4. Weighting caveat (read before use)

All percentage weights in this package are the **proposed plan** in
[`../docs/assessment-strategy.md`](../docs/assessment-strategy.md) §2 (draft v0.1,
awaiting instructor review). They are internally consistent and sum to 100%, but they are
**not** confirmed institutional policy. Marking schemes therefore award marks out of
instrument-local totals (e.g., midterm /60) rather than out of 100, so the papers survive
any final weighting decision.

## 5. Known open items flagged for instructor reconciliation

1. **Graded-quiz windows disagree across foundation docs.** Strategy §2/§3.1 schedule four
   windows (W04, W07, W10, W13, best two count); the syllabus calendar and
   [`../docs/schedule-32-lectures.md`](../docs/schedule-32-lectures.md) event table show
   two (W04, W12). The weekly papers cover either resolution — ⚠ VERIFY before release
   and amend the losing document.
2. **Letter-grade bands** in strategy §4 are recommended-internal only (⚠ VERIFY against
   university policy).
3. **No item in this package has been sat by real students.** Numerical answers were
   machine-checked where flagged (see §6); all items still require an instructor
   solve-through before first use (`ITI` in [`../docs/clo-mapping.md`](../docs/clo-mapping.md) §2).

## 6. Verification status of numerical answers

- Answers marked **[MC]** in instructor keys were verified by script
  (`tools/scripts/verify_assessment_numbers.py`): subnet arithmetic via Python's
  `ipaddress`, plus throughput/delay/window arithmetic.
- Answers marked **[DC]** were desk-checked by hand only — re-verify before first use.
- The verification script and its exact checks are documented in the assessment audit
  report under [`../docs/audit-reports/`](https://github.com/nadeem-majeedch/Computer-Networks/blob/main/docs/audit-reports/).
