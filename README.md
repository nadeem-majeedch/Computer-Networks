# Computer Networks — Course Repository

A complete, open course for **4th-semester BS Computer Science and BS Data Science**
students: **32 lectures × 2 hours = 64 instructional hours**, combining theory, packet
analysis (Wireshark), Python/Linux labs, network emulation, progressive case studies, and a
team capstone.

| Field | Value |
|---|---|
| Status | **Foundation + lecture-content + lab-workbook + practice-case-bank + assessment-package + slide-deck + GitHub Pages site phases complete — graded case bundles/VM image not started.** Draft v0.1, awaiting instructor review |
| Audience | Undergraduate CS & Data Science, semester 4 |
| Scope | Networking fundamentals → OSI/TCP-IP → L2/L3 → transport → applications → security → operations/cloud → capstone |
| Vendor policy | Strictly vendor-neutral; open standards (IEEE 802, IETF RFCs) only |
| Tooling | Wireshark, Python 3.10+, Linux (iproute2, netem, nftables, dnsmasq), iperf3, VMs; simulators only where kernel networking cannot reach |
| Review status | Unreviewed drafts; ⚠ items flagged for instructor verification throughout |

## Quick navigation

| Document | Purpose |
|---|---|
| [`docs/syllabus.md`](docs/syllabus.md) | **Start here** — catalog description, weekly calendar, policies |
| [`docs/schedule-32-lectures.md`](docs/schedule-32-lectures.md) | The 32-lecture master schedule with modules, pacing, labs, case studies |
| [`docs/course-objectives.md`](docs/course-objectives.md) | Instructor-facing course objectives (O1–O7) |
| [`docs/learning-outcomes-clos.md`](docs/learning-outcomes-clos.md) | The 8 measurable CLOs with Bloom levels |
| [`docs/clo-mapping.md`](docs/clo-mapping.md) | CLO ↔ topic ↔ assessment matrices + PLO mapping (pending) |
| [`docs/prerequisites.md`](docs/prerequisites.md) | Entry skills, required coursework, environment, ethics gate |
| [`docs/assessment-strategy.md`](docs/assessment-strategy.md) | Instruments, weights, rubrics, integrity rules |
| [`docs/textbooks-references.md`](docs/textbooks-references.md) | Required/supplementary texts, RFCs, IEEE standards, tool docs |
| [`docs/teaching-methodology.md`](docs/teaching-methodology.md) | Lecture pattern, demo standards, two-audience design, misconception register |
| [`docs/lab-strategy.md`](docs/lab-strategy.md) | The 14 labs, environments, rubric, verification list |
| [`docs/case-study-strategy.md`](docs/case-study-strategy.md) | Meridian Systems narrative: CS-01…CS-04 + capstone |
| [`docs/repository-structure.md`](docs/repository-structure.md) | Target layout and what exists when |
| [`docs/lecture-template.md`](docs/lecture-template.md) | Standard for building the 32 lecture folders |
| [`docs/contributing-instructor-review.md`](docs/contributing-instructor-review.md) | Workflow, review checklists, contributor policy |
| [`docs/audit-reports/`](docs/audit-reports/) | Validation & audit reports (append-only) |

## Course at a glance

- **8 modules:** Foundations · Physical/Data Link · Internetworking (IPv4/IPv6) · Transport ·
  Applications · Security · Operations/Monitoring/Cloud · Integration & Capstone.
- **14 numbered labs** + in-lecture guided activities; one course VM image; no paid software.
- **One storyline:** fictional company "Meridian Systems" escalates from a slow morning to a
  full multi-site redesign capstone.
- **8 CLOs** mapped to topics and instruments; weights sum to exactly 100%.

## Current state (honest)

✔ Foundation documents (`docs/` set) — complete, drafted, **not yet instructor-reviewed**.
✔ 32 lecture teaching packages (`lectures/`) — README + instructor notes + worksheet each;
  machine-audited (14 checks clean); slide decks still pending.
✔ 16-lab workbook (`labs/`) — student README + instructor guide + worksheet per lab, plus
  syllabus/safety, setup guide, and index; audited (9 checks) and command-syntax-verified
  (36 fenced blocks); **no lab executed end-to-end yet** — instructor run-through required
  (see [`docs/audit-reports/2026-09-19-lab-workbook-verification.md`](docs/audit-reports/2026-09-19-lab-workbook-verification.md) §5).
✔ 65-case practice bank (`case-studies/`) — PB-001…PB-065, two per lecture (+1 for L29),
  student/instructor split per case; audited (10 checks: 16-element completeness, ramp,
  lecture + category coverage, index agreement); graded CS-01…04 bundles still pending
  (see [`docs/audit-reports/2026-09-20-case-bank-coverage.md`](docs/audit-reports/2026-09-20-case-bank-coverage.md)).
✔ Assessment package (`assessments/`) — 45 files: weekly quizzes W01–W16, module
  review sets M1–M8, seven question banks, assignment briefs, midterm + final papers
  (student/instructor split), practical + capstone rubrics, integrity and marking
  guides; audited (12 checks) with 99 machine-verified numeric answers
  (see [`docs/audit-reports/2026-09-20-assessment-package-audit.md`](docs/audit-reports/2026-09-20-assessment-package-audit.md)).
✔ Slide decks (`lectures/*/slides.md`) — 32 decks, 548 slides with per-slide speaker
  notes, original Mermaid/ASCII diagrams covering all visual topics, worked examples,
  demo instructions with offline fallbacks; lecture audit now 14/14 PASS
  (see [`docs/audit-reports/2026-09-20-slide-decks-audit.md`](docs/audit-reports/2026-09-20-slide-decks-audit.md)).
✖ Slide decks (`slides.md` per lecture) — not started (standing WARN in the lecture audit).
✖ Graded case-study evidence bundles (CS-01…CS-04) — not started (see [`docs/case-study-strategy.md`](docs/case-study-strategy.md) §2; the practice bank rehearses but does not replace them).
✖ VM image build — not started (see [`docs/lab-strategy.md`](docs/lab-strategy.md) §2).
✖ PLO mapping, exam papers — pending instructor action (flagged ⚠ in the CLO document).

## For the instructor: first actions

1. Read [`docs/syllabus.md`](docs/syllabus.md), then
   [`docs/audit-reports/2026-09-19-foundation-audit.md`](docs/audit-reports/2026-09-19-foundation-audit.md)
   for the validation summary and open warnings.
2. Complete the PLO mapping in [`docs/clo-mapping.md`](docs/clo-mapping.md) §4.
3. Verify the flagged items (editions, VM image, cloud quotas, calendar dates) — every one is
   marked ⚠ VERIFY with its location in [`docs/contributing-instructor-review.md`](docs/contributing-instructor-review.md)
   and [`docs/lab-strategy.md`](docs/lab-strategy.md) §7.
4. Review and stamp the foundation documents and the lecture packages (see
   [`docs/audit-reports/2026-09-19-lecture-content-audit.md`](docs/audit-reports/2026-09-19-lecture-content-audit.md)
   §5 for what needs human verification), then green-light the labs/slides phase.

## Contributing

See [`docs/contributing-instructor-review.md`](docs/contributing-instructor-review.md).
Branch → PR → review; technical claims need named sources; no fabricated evidence; nothing
is committed by the course generator itself.
