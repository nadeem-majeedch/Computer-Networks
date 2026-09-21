# Repository Structure

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`contributing-instructor-review.md`](contributing-instructor-review.md) · [`lecture-template.md`](lecture-template.md) |

This document defines the **target** repository layout, what each directory is for, and
what currently exists. Directories are created only when real content lands in them —
no empty placeholders.

## 1. Layout

```
/
├── README.md                        # Front door: course at a glance, navigation, status
├── docs/                            # Foundation & policy documents (this foundation phase)
│   ├── syllabus.md
│   ├── course-objectives.md
│   ├── learning-outcomes-clos.md
│   ├── clo-mapping.md
│   ├── prerequisites.md
│   ├── schedule-32-lectures.md
│   ├── assessment-strategy.md
│   ├── textbooks-references.md
│   ├── teaching-methodology.md
│   ├── lab-strategy.md
│   ├── case-study-strategy.md
│   ├── repository-structure.md      # This file
│   ├── lecture-template.md          # Standard for building lecture folders
│   ├── contributing-instructor-review.md
│   └── audit-reports/               # Validation/audit outputs (dated, append-only):
│       ├── 2026-09-19-foundation-audit.md
│       ├── 2026-09-19-lecture-content-audit.md
│       └── 2026-09-19-lab-workbook-verification.md
├── lectures/                        # One folder per lecture, built from lecture-template.md
│   ├── README.md                    # Index table: lecture → folder → status
│   └── lecture-NN-short-name/
│       ├── README.md                # Overview, outcomes, key questions, readings
│       ├── notes.md                 # Instructor-facing teaching notes
│       ├── slides.md                # Marp-compatible slide source
│       ├── worksheet.md             # Guided activity / exit ticket (if applicable)
│       ├── demo/                    # Pre-verified demo configs, commands, scripts
│       └── assets/                  # Traces, images specific to this lecture
├── labs/                            # Workbook: 16 triads (LAB-01…LAB-16; 15/16 optional)
│   ├── README.md                    # Index, inventory, topic-coverage map
│   ├── syllabus-safety.md           # Lab syllabus + binding safety/ethics rules
│   ├── setup-environment.md         # Tooling setup + environment routes
│   └── lab-NN-short-name/
│       ├── README.md                # Student handout: outcomes, pre-lab, tasks,
│       │                            #   expected observations, troubleshooting, alternatives
│       ├── instructor.md            # INSTRUCTOR-ONLY: solutions, failure modes, rubric notes
│       └── worksheet.md             # Print/fill worksheet: pre/post answers, task records
├── case-studies/                    # Practice bank (PB-001…PB-065) + graded thread plan
│   ├── README.md                    # Bank index by lecture/difficulty/topic + evidence policy
│   └── cases/                       # One file per case: student half + instructor half
│   │                                # (graded CS-01…04 bundles planned per case-study-strategy.md)
│   ├── (planned) cs-01-network-feels-slow/
│   ├── (planned) cs-02-segmented-lan/
│   ├── (planned) cs-03-service-outage/
│   └── (planned) cs-04-capstone-meridian-redesign/
├── assessments/                     # Quizzes, banks, exams, rubrics — student/instructor split enforced
│   ├── rubrics/
│   ├── quizzes/
│   └── exams/
├── assets/                          # Shared images, logos, shared trace library
│   ├── images/
│   └── traces/
├── tools/                           # Environment build & maintenance
│   ├── vm/                          # Course VM image build scripts + README + hashes
│   └── scripts/                     # Grading/validation helpers (e.g., audit checks)
└── instructor/                      # Semester operations
    ├── setup-checklist.md           # Per-semester prep (from teaching-methodology §10)
    └── misconception-log.md         # Running record from exit-ticket data
```

## 2. Conventions

| Concern | Convention |
|---|---|
| Naming | Lowercase, hyphen-separated; lecture folders prefixed `lecture-NN`; labs `lab-NN` |
| Identifiers | `L01`…`L32` (lectures), `LAB-01`…`LAB-16` (14 curriculum labs + 2 optional extensions), `GA-01`…`GA-31`, `CS-01`…`CS-04`, `CLO1`…`CLO8` |
| Links | Relative Markdown links only (works on GitHub Pages and local preview) |
| Images | `assets/images/` for shared; per-lecture `assets/` for specific; always with alt text |
| Traces | `.pcapng` preferred; each accompanied by a `.md` describing what it shows and how it was produced |
| Instructor-only | Anything under `solution/` or `assessments/exams/` — keep out of student-visible Pages builds (⚠ VERIFY GitHub Pages path/filter configuration when deploying) |
| Encoding | UTF-8; no file exceeds ~1,500 lines (split instead) |

## 3. Existence status

| Path | Exists now | Planned phase |
|---|---|---|
| `README.md`, `docs/` foundation set | ✔ | Foundation (this phase) |
| `docs/audit-reports/` | ✔ (foundation + lecture-content audits) | Both phases |
| `docs/calendar-guide.md`, `site-src/_calendar.yml`, `tools/scripts/calendar_lib.py` | ✔ | One-click semester calendar: configurable start/days/holidays, computed milestones, ICS/CSV exports, 21 date-calculation validation tests |
| `lectures/` (32 packages × README/notes/worksheet/slides + index) | ✔ | Content (lecture packages incl. slide decks, 548 slides) — audited 14/14 PASS |
| `labs/` (16 folders) | ✔ | Lab workbook — audited + command-syntax-verified; execution pending |
| `case-studies/` (bank: 65 cases + index) | ✔ (practice bank) | Graded CS-01…04 bundles still pending, per [`case-study-strategy.md`](case-study-strategy.md) |
| `assessments/` | ✔ | Package built: quizzes W01–W16, review sets M1–M8, 7 banks, briefs, exams, rubrics (`docs/audit-reports/2026-09-20-assessment-package-audit.md`) |
| `assets/`, `instructor/` | ✖ | Content phase (created when first used) |
| `site-src/`, `mkdocs.yml`, `requirements.txt`, `.github/workflows/deploy-pages.yml`, `tools/scripts/build_site_docs.py`, `tools/scripts/validate_site.py` | ✔ | GitHub Pages site (MkDocs Material) — mirrors course sources student-visible-only; strict build + 26-check validation green (`docs-meta/github-pages-deployment-report.md`) |
| `tools/scripts/` (audit/verification tools) | ✔ | Grows with each content phase — includes `check_readme_links.py` (relative-link/anchor validator) and `check_lab_env.py` (student host-tool self-check) |

Rule: a directory may be added only together with at least one real file inside it.
