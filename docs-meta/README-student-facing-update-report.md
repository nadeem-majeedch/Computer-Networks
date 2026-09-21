# README Student-Facing Update Report — 2026-09-21

| Field | Value |
|---|---|
| Phase | Main README transformation: deployment-manual → public student-facing course homepage |
| Evidence basis | Direct file inspection + new link validator (`tools/scripts/check_readme_links.py`) + live curl checks + full audit-tool regression |
| Result | **138/138 relative links resolve · live course-site and external URLs checked (results in §5) · full audit suite green after changes** |
| Scope of change | `README.md` (full rewrite) · `case-studies/README.md` (2 stale header lines fixed) · `docs/repository-structure.md` (1 row updated) · `tools/scripts/check_readme_links.py` (new) · this report |
| Not changed | `mkdocs.yml`, `.github/workflows/deploy-pages.yml`, all course content, site generator — deployment verified working, untouched |
| Committed / pushed | **No** — left for manual review per project rules |

## 1. What was inspected

- `README.md` (old version read in full), `mkdocs.yml`, `requirements.txt`
- Directory trees: `docs/` (15 files + `audit-reports/`), `lectures/` (32 packages × 4 files + index), `labs/` (16 folders × 3 files + 3 top-level guides), `case-studies/` (65 case files + index), `assessments/` (45 files: quizzes W01–W16, review M1–M8, 7 banks, 2 assignment pairs, 4 exam files, 2 rubrics, integrity/marking guides), `site-src/`, `docs-meta/`, `tools/scripts/` (11 scripts), `.github/workflows/deploy-pages.yml`
- Baseline audits re-run on the live tree **before** editing: foundation 15/15 · lectures 14/14 · labs 9/9 · case bank 10/10 · assessment 12/12 — all green
- Live site verified before editing: home, `/lectures/`, `/calendar/`, `/case-studies/`, `/labs/`, `/assessments/`, `/overview/`, `/references/`, `/instructors/` all **HTTP 200** on the production URL

## 2. Actual learning resources found (inventory the README now reflects)

| Resource | Actual count | Link basis |
|---|---|---|
| Lecture packages | 32/32 (README + notes + slides + worksheet each) | `lectures/lecture-NN-*/` — every one linked |
| Labs | 16 (each: student README, instructor guide, worksheet) | All 16 linked individually |
| Case studies | 65 (PB-001…PB-065) | Index + per-lecture/difficulty/topic tables |
| Quizzes / review sets / banks | 16 / 8 / 7 | Directory + package index |
| Assignments | 2 (subnetting set, reliable-transport project) — student files linked, instructor files not exposed | `assessments/assignments/*-student.md` |
| Exams | Midterm + final, student/instructor split | `assessments/exams/` directory |
| Rubrics | 2 (practical work, capstone) | Direct file links |
| Calendar | Configurable site page + ICS/CSV exports | `site-src/calendar.md` |
| Documentation set | 15 docs + audit reports | Direct links |

## 3. README sections created (required structure → status)

All 18 requested sections present: title/intro · start-here table (9 verified links) · course website CTA · course description (CS + DS rationale) · 8 measurable CLOs (actual, from `docs/learning-outcomes-clos.md`) · prerequisites (actual entry-skills checklist) · full 8-module × 32-lecture map with links · lecture-materials table with student/instructor separation · labs section (purpose, tools, safety, per-lab links) · case-studies section (4-level progression + method) · assessments table (weightings marked *proposed*) · calendar (no invented dates) · 8-step learning path adapted to real materials · tools table (8 rows, all genuinely used, official URLs) · references (real, verified; free primary text highlighted) · For Instructors (secondary position) · contribution/usage (**no license invented** — status stated as rights-reserved-by-default) · repository/website links with deployment demoted to a collapsed `<details>` block.

## 4. Links validated (actual results)

- **New validator** (`tools/scripts/check_readme_links.py`): every relative link in README.md checked for target existence, directory-index validity, and GitHub-style heading-anchor slugs. Final: **138 relative links, 0 broken**; 9 intentional GitHub directory-listing links (all non-empty directories) reported as notes.
- **Live course site** (curl, production URL): home + 8 key sections **HTTP 200** (see §1).
- **External URLs** (curl at validation time): wireshark.org 200 · systemsapproach.org 200 · hpbn.co 200 · rfc-editor.org 200 · github repo 200 · **tcpipguide.com: HTTPS did not connect (000) but plain HTTP returned 200** — site is up and the reference (also present unchanged in `docs/textbooks-references.md` and `site-src/references.md`) is left as-is; the occasional HTTPS/TLS quirk of that host is noted here rather than silently removed.
- **Issues found and fixed during validation:**
  1. Two links initially pointed at `assessments/review/` and `assessments/banks/` (bare listings) — repointed to the descriptive package index anchor `assessments/README.md#1-what-lives-here` (validated).
  2. Case-bank README header still said "PB-001…PB-064 / 64 practice cases" while its own index and files total **65** — corrected to PB-001…PB-065 / 65 cases, two per lecture with L29 carrying three (matches the §6 index). `audit_casebank.py` re-run: 10/10 PASS.

## 5. Student-facing quality review (Phase 4 questions)

1. *Understand the course in one minute* — yes: title block, audience/format/approach table, and a one-paragraph pitch precede everything.
2. *Find all resources* — yes: 9-row start-here table + full map; every claim backed by a validated link.
3. *Navigation clear* — yes: modules in teaching order, dependency-correct.
4. *Links working* — yes (§4); no anchors guessed — all fragment targets slug-verified.
5. *Accessible description* — yes: no protocol jargon in the intro; DS relevance stated concretely.
6. *Learning order* — yes: the recommended path follows the actual calendar sequence.
7. *Instructor-only separation* — yes: answer keys/exams marked as withheld; a dedicated callout explains where instructor material lives and that the website excludes it; no instructor file is presented as a student resource. (Known, documented convention: `lectures/*/notes.md` mixes teaching plans with student-readable explanations; labeled as such rather than hidden.)
8. *More than a deployment guide* — yes: deployment reduced to a collapsed maintainer footnote.
9. *Encourages independent learning* — yes: free-primary-text emphasis, self-check path, worksheets-before-lookup advice.
10. *Represents actual content* — yes: only verified resources linked; the two known gaps (graded CS-01…CS-04 bundles, VM image) are not advertised as available anywhere in the README.

## 6. Supporting updates (Phase 5) — minimal by design

| File | Change | Why |
|---|---|---|
| `case-studies/README.md` | Header/Scope rows: 64 → 65, PB-064 → PB-065 | Stale count contradicted the file tree and its own index |
| `docs/repository-structure.md` | Tools row now names `check_readme_links.py` | Inventory accuracy |
| `tools/scripts/check_readme_links.py` | New (stdlib-only link/anchor validator) | Repeatable validation for future README edits |

Nothing else touched: no course content, no site configuration, no workflow.

## 7. Verification (post-change regression, actual results)

- `mkdocs build --strict` (clean `site/` + `_build/`, venv interpreter): **0 errors** (2 pre-existing accepted INFO directory-link notices)
- Full audit suite re-run: foundation **15/15** · lectures **14/14** · labs **9/9** · lab syntax **36/36** · case bank **10/10** · assessment **12/12** · numerics **all [MC] verified** · calendar **0 FAIL** · site validation **0 FAIL, 0 WARN**
- Mirrored site case index confirmed to carry the corrected 65-case count
- No commit, no push performed (workspace left for manual review)

## 8. Warnings and unresolved items

1. **tcpipguide.com HTTPS** — connects only over HTTP from this environment at validation time; reference kept (it is correct and widely used); no action taken on the deployed site.
2. **External URLs are point-in-time** — live checks reflect 2026-09-21; re-verify before each semester (the ⚠-flag convention in the docs covers this).
3. **No license file** — README states rights-reserved-by-default honestly; choosing a license (e.g., CC BY-NC-SA for OER) is an instructor decision and was **not** invented.
4. **Pre-existing content gaps unchanged** (documented in prior handovers, not README-visible): graded CS-01…CS-04 bundles and the VM teaching image remain unbuilt.
5. The two L30/L31 INFO notices in the site build are the same accepted directory-style links documented in the deployment report; not a regression.
