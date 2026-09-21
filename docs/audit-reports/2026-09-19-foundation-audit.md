# Foundation Audit Report — 2026-09-19

| Field | Value |
|---|---|
| Audit type | Foundation-phase validation (architecture & documentation) |
| Scope | All files present at audit time: `README.md` + 13 `docs/` documents + this report |
| Method | Automated checks (`tools/scripts/audit_foundation.py`) + manual review pass |
| Course version | v0.1 (draft, unreviewed) |
| Auditor | Course generator (automated) — human instructor sign-off still required |

> This report records **actual results** from running the audit script against the
> repository as it stands. Nothing here is projected or assumed. This directory is
> append-only; future audits add new dated files.

---

## 1. Deliverables completed

| Requirement (from the foundation task) | Status | Where |
|---|---|---|
| README.md | ✔ Created | [`/README.md`](../../README.md) |
| Course syllabus | ✔ Created | [`syllabus.md`](../syllabus.md) |
| Course learning objectives | ✔ Created (O1–O7) | [`course-objectives.md`](../course-objectives.md) |
| Course learning outcomes (CLOs) | ✔ Created (CLO1–CLO8, Bloom-tagged) | [`learning-outcomes-clos.md`](../learning-outcomes-clos.md) |
| CLO-to-topic mapping | ✔ Created (32-row matrix + coverage summary) | [`clo-mapping.md`](../clo-mapping.md) §1 |
| CLO-to-assessment mapping | ✔ Created (instrument matrix + measurement check) | [`clo-mapping.md`](../clo-mapping.md) §2 |
| Prerequisites | ✔ Created (coursework, skills checklist, environment, ethics gate) | [`prerequisites.md`](../prerequisites.md) |
| 32-lecture master schedule | ✔ Created (8 modules, pacing, labs, case studies, dependencies) | [`schedule-32-lectures.md`](../schedule-32-lectures.md) |
| Assessment strategy | ✔ Created (8 instruments, weights, rubrics, integrity rules) | [`assessment-strategy.md`](../assessment-strategy.md) |
| Textbooks & references | ✔ Created (real texts, RFCs, IEEE standards, tool docs) | [`textbooks-references.md`](../textbooks-references.md) |
| Teaching methodology | ✔ Created (lecture pattern, demo standards, misconceptions, inclusivity) | [`teaching-methodology.md`](../teaching-methodology.md) |
| Laboratory strategy | ✔ Created (14 labs + GAs, environments, rubric, verification list) | [`lab-strategy.md`](../lab-strategy.md) |
| Case study strategy | ✔ Created (Meridian narrative, CS-01–CS-04, capstone rubric) | [`case-study-strategy.md`](../case-study-strategy.md) |
| Repository directory structure | ✔ Created (target layout + existence status; no empty dirs created) | [`repository-structure.md`](../repository-structure.md) |
| Contribution & instructor review guidance | ✔ Created (roles, workflow, checklists, stamps) | [`contributing-instructor-review.md`](../contributing-instructor-review.md) |
| Foundation audit report | ✔ This document | — |

Supporting artifacts also produced: [`lecture-template.md`](../lecture-template.md)
(standard for the content phase) and [`tools/scripts/audit_foundation.py`](../../tools/scripts/audit_foundation.py)
(re-runnable validation).

## 2. Automated validation results (actual script output)

Final run of `python tools/scripts/audit_foundation.py` on 2026-09-19: **15 checks — 15 PASS, 0 WARN, 0 FAIL** (three earlier runs returned 5, 1, and 1 failures; see §5 for what was found and fixed).

| Check | Result | Evidence (from script output) |
|---|---|---|
| Link integrity | PASS | 107 relative links checked, 0 broken |
| No placeholders | PASS | 15 md files, none empty, all ≥300 B, `no TBD/TODO/lorem` |
| 32 lectures present | PASS | L01..L32 exactly once each, in order |
| Module structure | PASS | 8 modules: L01-04, L05-11, L12-16, L17-20, L21-23, L24-26, L27-29, L30-32; no gaps/overlaps |
| Instructional hours | PASS | 32 × 2 h = 64 h |
| Topic progression (dependencies) | PASS | 11 encoded prerequisite pairs all taught before dependents |
| Topic progression (ordering) | PASS | Foundations → Transport → Security → Capstone |
| CLO coverage (topics) | PASS | every CLO1–8 has primary lectures (CLO1:3, CLO2:8, CLO3:4, CLO4:10, CLO5:5, CLO6:10, CLO7:3, CLO8:1) |
| CLO reference validity | PASS | all CLO references in schedule are CLO1–8 |
| Assessment weights sum | PASS | 8 instruments sum to exactly 100% |
| Assessment alignment (syllabus vs strategy) | PASS | 8 instrument weights identical in both documents |
| Instrument-to-CLO mapping | PASS | every weighted instrument maps to ≥1 CLO |
| CLO measurement coverage | PASS | 8 CLOs each measured by ≥1 instrument (CLO8 single-instrument by design) |
| Lab reference consistency | PASS | schedule references exactly LAB-01..LAB-14 |
| Syllabus calendar | PASS | 32 lecture rows covering weeks 1–16; all L01–L32 present |

Reproduce with: `python tools/scripts/audit_foundation.py` (exit code 0 expected).

## 3. Manual verification (checks the script cannot make)

| Area | Result | Notes |
|---|---|---|
| Topic progression (coherence review) | ✔ Sound | Fundamentals precede advanced everywhere; hard prerequisites honored (subnetting after IP addressing, TCP after UDP/transport intro, attack workshop after ARP/DNS/DHCP/TCP, capstone last). Spiral revisits (TLS, DHCP, UDP/QUIC) are labeled as such in the objectives document. |
| Required vs enrichment separation | ✔ Present | Every schedule row labels `(enr)` topics; coverage verdicts in the CLO matrix use core content only. |
| Vendor neutrality | ✔ Maintained | Standards-based (IEEE 802, RFCs); no certification-track content; a vendor-neutral "certification paths overview" appears only as L31 enrichment. |
| Syllabus ↔ schedule ↔ assessment coherence | ✔ Consistent | Calendar rows mirror the schedule; due dates and weights match; the script cross-checks weights and lab references mechanically. |
| Audience fit (semester 4) | ✔ Appropriate | Prerequisites gate assumes CS1/CS2/discrete math; programming scope is bounded (sockets, standard library); no graduate-level digressions. |
| No fabricated sources | ✔ Verified | All references are real, well-known texts/standards; tools referenced have official documentation. No invented results or tool output anywhere in the foundation docs. |

## 4. Warnings and items requiring instructor verification (⚠)

These are **known, flagged gaps** — the course foundation is not "done" until they are resolved:

| # | Item | Location | Why it can't be resolved by the generator |
|---|---|---|---|
| 1 | CLO→PLO mapping table is empty by design | [`clo-mapping.md`](../clo-mapping.md) §4 | Depends on the university's accredited PLO list |
| 2 | Textbook editions must be confirmed against what's current when the course runs | [`textbooks-references.md`](../textbooks-references.md) §1 | Editions change; section numbers in the reading map depend on it |
| 3 | Credit-hour equivalence, attendance/late/AI policies | [`syllabus.md`](../syllabus.md) header + §5 | University-specific regulations |
| 4 | VM image build, hash publication, hypervisor compatibility | [`lab-strategy.md`](../lab-strategy.md) §2, §7 | Environment-dependent |
| 5 | LAB-03 Wi-Fi survey feasibility in local RF environment | [`lab-strategy.md`](../lab-strategy.md) §7 | Site-dependent |
| 6 | LAB-07 simulator (GNS3) licensing/images — or kernel-namespace alternative | [`lab-strategy.md`](../lab-strategy.md) §2 | Licensing choice |
| 7 | GA-27 cloud sandbox provider/quota/cost ceiling | [`lab-strategy.md`](../lab-strategy.md) §2 | Procurement decision |
| 8 | LAB-12 external HTTP/3 endpoints reachability + local fallback | [`lab-strategy.md`](../lab-strategy.md) §7 | Network-dependent |
| 9 | Midterm/capstone dates vs actual academic calendar | [`syllabus.md`](../syllabus.md) §3 note | Calendar-dependent |
| 10 | Grading scale bands pending university mapping | [`assessment-strategy.md`](../assessment-strategy.md) §4 | University-specific |
| 11 | Generative-AI policy for students pending program rules | [`assessment-strategy.md`](../assessment-strategy.md) §5 | University-specific |
| 12 | Dataset license/stability checks for L28/L31 and LAB-14 sources | [`textbooks-references.md`](../textbooks-references.md) §5 | License-dependent |
| 13 | GitHub Pages build must exclude `solution/` and `assessments/exams/` | [`repository-structure.md`](../repository-structure.md) §2 | Deployment configuration |

## 5. Issues found during auditing and their resolution (actual history)

| Run | Finding | Disposition |
|---|---|---|
| Run 1 | 5 FAIL: 5 broken links (3 were template *examples* inside fenced code blocks; 2 pointed at this audit report before it existed) | Template examples are not live links — the checker now strips fenced code blocks; the audit-report links became valid once this report was written. |
| Run 1 | FAIL: literal `TBD` string in [`lecture-template.md`](../lecture-template.md) (it was describing the rule, not violating it) | Reworded to "to-be-decided"; checker also strips fenced blocks and code spans before scanning. |
| Run 1 | FAIL: assessment weights parsed as empty | Checker bug — it read only the last table cell; fixed to scan the whole row. Real weights were correct (100%). |
| Run 1 | FAIL: LAB-11 "absent from schedule" | Schedule used the arrow form `LAB-10→11`; normalized to `LAB-10/11` and taught the checker the combined form. |
| Run 1 | Cosmetic: mojibake in the script's console title on Windows consoles | Replaced the em dash with a hyphen. |
| Run 2 | 1 FAIL: the two audit-report links in the README (this file did not yet exist) | Resolved by writing this report. |
| Run 3 | 1 FAIL: the placeholder checker flagged this report's own evidence text that quoted the checker's output string | Quoted tool output is now written in code spans, which the checker (correctly) treats as quoted content rather than unfinished-work markers. |
| Run 4 (final) | 15/15 PASS | — |

Consistency corrections made while drafting (caught in self-review, before the first audit run): security/operations module numbering (7–8, not 6–7) in the objectives/CLO docs; ARP moved to L12 with all cross-references updated; UDP lecture fixed at L17; lab thread extended to LAB-01…LAB-14; CS-04 kickoff aligned to L26 across schedule, case-study strategy, and CLO mapping.

## 6. What this audit does NOT cover (out of scope)

- The 32 lecture folders, 14 lab handouts, case-study evidence bundles, assessments, and VM
  image — these belong to the **content phase** and do not exist yet (see the README's
  "Current state").
- Pedagogical effectiveness (requires delivery and student feedback).
- Any live infrastructure, servers, or networks — none were touched; the audit is a
  static documentation/code review plus scripted checks.

## 7. Verdict

**Foundation phase: COMPLETE and internally consistent, pending instructor review.**
All 16 requested foundation deliverables exist as substantive content, all automated checks
pass, and all environment/university-dependent items are explicitly flagged rather than
assumed. Next step: instructor review and stamping per
[`contributing-instructor-review.md`](../contributing-instructor-review.md), then the
content phase (lecture folders first, following [`lecture-template.md`](../lecture-template.md)).
