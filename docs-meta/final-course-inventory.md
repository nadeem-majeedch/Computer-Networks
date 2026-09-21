# Final Course Inventory & Teaching-Package Readiness — 2026-09-20

| Field | Value |
|---|---|
| Purpose | Handover inventory for manual instructor review, commit, and publication |
| Evidence basis | Direct file inspection (`ls`/`grep` counts below) + fresh runs of all 10 validation tools on the final tree |
| Validation state | foundation 15/15 · lectures 14/14 · labs 9/9 · lab syntax 36/36 · case bank 10/10 · assessment 12/12 · assessment numerics 99/99 · calendar 21/21 · site validation 26/26 · `mkdocs build --strict` clean |
| Repository state | No git history exists in this workspace; **nothing has ever been committed or pushed from here** |

## 1. Inventory (actual counts, verified by inspection)

| Category | Location | Count | Notes |
|---|---|---|---|
| Course documentation | `docs/*.md` | 15 | syllabus, CLOs, mapping, strategies, schedule, calendar guide, references, template, structure, contributing |
| Audit & QA reports | `docs/audit-reports/*.md` | 7 | one per build phase + course-wide QA review |
| Lecture packages | `lectures/lecture-*/` | 32 | L01–L32, 4 files each: README, notes, slides, worksheet (128 files) |
| — slide decks | `lectures/*/slides.md` | 32 | 548 slides total; every slide has a speaker note |
| — speaker notes | `lectures/*/notes.md` | 32 | instructor-facing; 120-min pacing plans |
| — student worksheets | `lectures/*/worksheet.md` | 32 | GA tasks + exit tickets; keys in notes §6 only |
| — diagrams | decks + notes | 43 Mermaid + 55 ASCII blocks in decks, 2 Mermaid in notes | all original; no copyrighted figures; no fake screenshots |
| Laboratory workbook | `labs/` | 16 labs | each: README (student) + worksheet + instructor key (19 lab-root docs incl. safety/setup) |
| — lab instructor keys | `labs/lab-*/instructor.md` | 16 | solutions, setup notes, offline-capture alternatives |
| Case studies (practice) | `case-studies/cases/*.md` | 65 | student version + instructor section per file; index `case-studies/README.md` |
| Graded case bundles | — | **0** | CS-01…CS-04 defined in `case-study-strategy.md` but **not built** (known gap H-2) |
| Assessments — quizzes | `assessments/quizzes/` | 16 | W01–W16, keyed in-file (fenced) |
| — review sets | `assessments/review/` | 8 | M1–M8 |
| — question banks | `assessments/banks/` | 7 | conceptual, numerical/subnetting, packet-analysis, routing/troubleshooting, short/long-answer, practical |
| — assignment briefs | `assessments/assignments/` | 4 | subnetting PS + transport project, student+instructor versions |
| — exams | `assessments/exams/` | 4 | midterm + final, student+instructor versions with marking schemes |
| — rubrics | `assessments/rubrics/` | 2 | practical work; capstone |
| — package docs | `assessments/*.md` | 4 | README, CLO mapping, integrity, marking guide |
| Website source pages | `site-src/` | 6 files | home, overview, calendar + `_calendar.yml`, references, instructors |
| Website (generated) | `site/` → `_build/site/` | 302 docs → 299 URLs | built by generator; **never committed** |
| Build/validation scripts | `tools/scripts/*.py` | 10 | 5 audits, generator, calendar lib, lab-env checker, lab-syntax checker, site validator |
| Verification scripts | (included above) | — | `verify_assessment_numbers.py` (99 numeric claims), `check_lab_syntax.py` (bash -n on all fences) |
| GitHub Actions workflow | `.github/workflows/deploy-pages.yml` | 1 | push to main + manual dispatch; strict build; official Pages actions |
| Deployment docs | `docs-meta/github-pages-deployment-report.md` | 1 | Phase 9 report with manual steps |
| Calendar resources | `_calendar.yml` + `calendar_lib.py` + `docs/calendar-guide.md` + site exports | — | ICS/CSV exports ship with the site |
| Root | `README.md`, `mkdocs.yml`, `requirements.txt`, `.gitignore` | 4 | |
| **Total markdown** | — | **≈ 590 files** | |

## 2. Teaching-package readiness (per-lecture)

Every one of the 32 packages contains the full quartet (README, notes, slides,
worksheet) with metadata tables matching the master schedule (audit check),
pacing plans, speaker notes on every slide, and CLO-tagged exit tickets.

| Readiness dimension | State |
|---|---|
| Structure & completeness | ✔ 32/32 (audit-enforced) |
| Curriculum alignment | ✔ schedule ↔ packages ↔ CLO matrix consistent (audit-enforced) |
| Technical accuracy | ✔ after QA review; CRC examples in L06 corrected with machine-verified values; all 99 assessment numeric claims re-computed by script |
| Demo assets (traces, captures) | ⚠ referenced by 11 decks but not present in repo — instructor must capture/provide (H-3) |
| VM-image verification gate | ⚠ template requires "demo verified on current VM image" — no image exists yet (H-1) |
| Instructor sign-off | ⚠ none stamped yet — `contributing-instructor-review.md` process not yet run |

**Readiness verdict: content-ready, delivery-assets pending.** A semester can be
planned and reviewed now; live teaching additionally needs the VM image, the
promised captures, and the graded CS bundles.

## 3. Verification of prior audit claims (this handover re-checked them)

| Claim from earlier phases | Re-verified? |
|---|---|
| All tools green (7 tool suites) | ✔ fresh runs on final tree, same results |
| 32 lectures × 4 files, slides=notes | ✔ counts above |
| 65-case bank, labeled synthetic evidence, ramp | ✔ audit + grep (`0` files missing the synthetic label) |
| No placeholder markers in content trees | ✔ the foundation audit's placeholder scan (whose token list is deliberately not quoted here, to avoid tripping the scanner) reports 0 hits |
| Instructor/student separation on the site | ✔ `grep -rl "INSTRUCTOR KEY" site/` = 3 hits, all *documentation* of the convention (assessments README, instructors page, deployment report) — no leaked keys; lab instructor files absent from `site/` (confirmed by `ls`) |
| No fabricated "we measured X" claims | ✔ 3 grep hits inspected — all are L32's *rhetorical template* for students' own answers, none is a course measurement |
| Site strict build + 26 site checks | ✔ clean; sitemap = 299 URLs |
| No commit / no push | ✔ workspace has **no `.git` at all** — impossible to have committed or pushed; stale artifacts (`mkdocs-generated-nav.yml`, `__pycache__`) removed this pass |
