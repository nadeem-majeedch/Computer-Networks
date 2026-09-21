# GitHub Pages Deployment Report — Computer Networks

| Field | Value |
|---|---|
| Date | 2026-09-20 |
| Phase | GitHub Pages website (MkDocs Material) |
| Status | **Build validated locally; deployment NOT yet performed** (see §7) |
| Repository | https://github.com/nadeem-majeedch/Computer-Networks |
| Expected site URL | https://nadeem-majeedch.github.io/Computer-Networks/ |
| Committed / pushed | **No** — per project rules, all changes await manual review |

## 1. Repository inspection (Phase 1 findings)

- **Local workspace**: no `.git` directory — this is a content workspace, not a
  live clone. Git history/branch inspection was therefore not possible locally.
- **Remote**: `git ls-remote` against
  `https://github.com/nadeem-majeedch/Computer-Networks.git` returned **zero
  refs** — the GitHub repository is currently **empty** (reachable, but no
  commits). Consequence: there is no server-side default branch to inspect;
  the workflow targets `main` explicitly, which will be the default branch of
  the first push.
- **Existing content**: substantial and preserved — `docs/` (16 foundation
  documents), `lectures/` (32 packages × 4 files), `labs/` (16 labs),
  `assessments/` (45 files), `case-studies/` (65 cases), `tools/scripts/`
  (audit + verification tooling), `docs/audit-reports/` (5 phase reports).
- **No prior documentation framework**: no `mkdocs.yml`, `requirements.txt`,
  workflows, or site tooling existed. MkDocs Material was selected (Phase 2)
  rather than migrated to.

## 2. Framework and architecture

| Component | Choice | Rationale |
|---|---|---|
| Static-site generator | **MkDocs 1.6+ with Material 9.5+** | University-course standard; search, nav, Mermaid, code annotation support |
| Source of truth | Existing course trees (`lectures/`, `labs/`, …) | The website mirrors them; no content duplication or fork |
| Generator | `tools/scripts/build_site_docs.py` | Mirrors sources into `site/` (student-visible only), enriches pages, generates nav and calendar |
| Nav | Literate-nav file generated inside the tree | All 32 lectures + sections appear in navigation deterministically |
| Build | `mkdocs build --strict` | Any broken link or nav entry fails the build, locally and in CI |

**Key design decision — README.md as section index.** MkDocs treats
`README.md` as the directory index and *auto-rewrites relative `.md` links* at
build time. The generator therefore enriches the mirrored `README.md` files
(appends navigation blocks) instead of emitting `index.md` copies, and
original content links resolve without transformation. Instructor-only files
(`*-instructor.md`, lab `instructor.md`, `INSTRUCTOR KEY` sections) are
excluded or stripped during mirroring; case files' `## Instructor version`
blocks are removed.

## 3. Files created or updated

| File | Purpose |
|---|---|
| `mkdocs.yml` | Site config: subpath URLs, Material theme, strict mode, Mermaid fence, search |
| `requirements.txt` | Pinned-floor dependencies (mkdocs, material, literate-nav, section-index, pymdown-extensions, PyYAML) |
| `.gitignore` | Excludes `site/`, `_build/`, caches |
| `.github/workflows/deploy-pages.yml` | Pages deployment: generate → strict build → upload → deploy |
| `tools/scripts/build_site_docs.py` | Site generator/mirror/enricher (see §2) |
| `tools/scripts/validate_site.py` | 26-check site validation (§5) |
| `site-src/index.md` | Home page: course summary, audience, module map, entry links |
| `site-src/overview/index.md` | Course overview: prerequisites, CLOs, assessment strategy, references |
| `site-src/calendar.md` + `site-src/_calendar.yml` | Semester calendar; dates derive from configurable start + Mon/Wed slots + holidays |
| `site-src/references.md` | Textbooks and standards with attribution |
| `site-src/instructors/index.md` | Instructor gateway; documents what is student-visible vs repository-only |
| `lectures/README.md` | 2 links fixed to `.md` targets (L32 row, assessments pointer) |
| `assessments/README.md` | 1 repository-pointer link made absolute (target not part of the site tree) |
| `docs-meta/github-pages-deployment-report.md` | This report (published under Site Reports on the site) |

Generated, never committed: `site/`, `_build/`, `.generated_nav.yml` (inside `site/`).

## 4. Site content coverage (Phase 3)

- **Home** — title, description, 32-lecture × 2 h structure, CLO summary,
  navigation to all sections.
- **Course overview** — description, prerequisites, 8 CLOs, progression,
  assessment strategy (with the *proposed-weightings* caveat preserved),
  learning expectations.
- **Lectures** — all 32 packages (README + notes + slides + worksheet each),
  grouped by 8 modules in nav; per-package navigation block; module review
  links; case-study links.
- **Labs** — 16 lab pages + setup/safety; instructor guides stay repository-only.
- **Case studies** — 65 student case pages + bank index with flattened
  per-case table (ID / lecture / difficulty); solutions repository-only.
- **Assessments** — quizzes, review sets, student banks, assignment briefs
  (student versions), both exams (student versions), rubrics; all
  instructor versions excluded from the site.
- **Calendar** — 16-week Mon/Wed grid generated from `_calendar.yml`
  (`semester_start`, `lecture_days`, `holidays`), lecture links, assessment
  milestones; printable.
- **References** — textbooks + official standards, no fabricated entries.

## 5. Validation performed (actual results)

| Check | Result |
|---|---|
| `build_site_docs.py` generation | PASS — 297 files; 65-case index assertion enforced |
| `mkdocs build --strict` (clean venv) | PASS — 0 warnings, 0 errors |
| `tools/scripts/validate_site.py` | **26/26 PASS** — config, subpath URLs, theme, strictness, tree inventory (32/32 lectures, 16/16 labs, 65/65 cases, 16/16 quizzes), instructor-key leak scan, nav↔file agreement, HTML path hygiene, workflow integrity |
| Workflow YAML semantic check | PASS — triggers, permissions, action versions, deploy step |
| Serve test (static, mirrors GitHub Pages) | PASS — home, calendar, L01, PB-001/PB-065, labs, instructors, overview, references, site-reports, docs/syllabus all HTTP 200 |
| Canonical URL | `https://nadeem-majeedch.github.io/Computer-Networks/` present in home page head |
| Instructor separation | 0 instructor files, 0 instructor-version sections, 0 `INSTRUCTOR KEY` occurrences in the student tree |
| Clean-environment dependency install | PASS — fresh venv, floor constraints recorded in `requirements.txt` |

**Fixes made during validation** (all caught by the strict build or validator):
unbalanced-regex crashes in the link rewriter; nav YAML quoting (titles
containing `:`); README/index page conflicts (32 + 1); case-index parser
missing paired difficulties and `—` topics; case `Instructor version` leak;
depth-correct review-question links; two broken source links in
`lectures/README.md`; one repo-pointer link in `assessments/README.md` and
one template link in `site-src/calendar.md` (both caught by the foundation
audit's link check, which now also understands directory-style site links).

**Final full regression** (all tools): foundation 15/15 · lectures 14/14 ·
labs 9/9 · case bank 10/10 · assessment 12/12 + 99/99 numeric claims ·
site validation 26/26 · `mkdocs build --strict` clean.

**Not run**: browser rendering pass (no GUI in this environment — layout and
Mermaid rendering should be eyeballed once at the live URL); Lighthouse or
external link checking.

## 6. Deployment workflow (Phase 5)

`.github/workflows/deploy-pages.yml`: triggers on **push to `main`** and
**manual dispatch**; Python 3.12 with pip caching; installs
`requirements.txt`; runs the generator; runs `mkdocs build --strict`
(failures fail the workflow); `actions/configure-pages@v5`,
`actions/upload-pages-artifact@v3` (path `_build/site`),
`actions/deploy-pages@v4`; least-privilege permissions
(`contents: read`, `pages: write`, `id-token: write`); concurrency group
prevents overlapping deployments.

## 7. Manual steps required (cannot be done from here)

1. **Commit and push** the repository to `main` (first push; this workspace
   has no git history — `git init`, add remote, commit, push).
2. **GitHub Settings → Pages → Source**: select **GitHub Actions** (one time).
3. Watch the *Deploy site to GitHub Pages* workflow run; it must be green.
4. Verify the live site at the expected URL below (first load may lag a minute).

## 8. Expected URL

> https://nadeem-majeedch.github.io/Computer-Networks/

This URL is **expected, not verified** — no deployment has occurred yet, and
this report deliberately does not claim success. After step 3–4 above, check:
home loads, a lecture page renders Mermaid, a case page shows no instructor
content, the calendar dates match `_calendar.yml`, and search works.

## 9. Known warnings and limitations

- **Plugin warning during builds**: one installed plugin prints a notice
  claiming MkDocs is unmaintained and urging a switch to `properdocs`. This
  is unverified third-party marketing injected into tool output; the build
  itself succeeds. It is suppressed via `DISABLE_MKDOCS_2_WARNING=true` in
  CI; treat any such in-output install advice with suspicion.
- The GitHub repository is empty; the workflow's `main` branch assumption
  cannot be confirmed until the first push.
- Two directory-style links in `lectures/README.md` (L30/L31 rows) build with
  an INFO note; they resolve correctly in browsers but could be normalized
  for tidiness.
- `mkdocs serve` (dev server) returned 404s for subpages in this environment
  even though the built output is complete and correct via static serving;
  re-check `mkdocs serve` locally before relying on it for previewing.
- Calendar dates (2026-09-14 start) are placeholders in `site-src/_calendar.yml`
  — adjust `semester_start`, `lecture_days`, and `holidays` per semester.
