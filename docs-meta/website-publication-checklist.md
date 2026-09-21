# Website Publication Checklist & Manual Commit Instructions — 2026-09-20

Companion to `docs-meta/final-course-inventory.md` (inventory & readiness) and
`docs-meta/github-pages-deployment-report.md` (deployment detail).

## 1. Pre-publication state (verified)

- [x] `mkdocs.yml` — Material theme, strict mode, subpath URLs, Mermaid, search
- [x] `requirements.txt` — floor-pinned deps, installed clean in a venv
- [x] `.github/workflows/deploy-pages.yml` — YAML-verified, official actions, strict build gate
- [x] `tools/scripts/build_site_docs.py` — 302-file generated tree; student/instructor separation enforced
- [x] `tools/scripts/validate_site.py` — 26/26 PASS (config, inventory, leaks, nav, HTML paths, workflow)
- [x] `mkdocs build --strict` — 0 warnings
- [x] Canonical URL: `https://nadeem-majeedch.github.io/Computer-Networks/` in home page head
- [x] `site/`, `_build/` are `.gitignore`d — generated output never committed
- [ ] **Instructor eyeball pass of the rendered site** (browser, once deployed)
- [ ] **Mermaid render check** (diagrams are syntax-audited, not visually rendered here)

## 2. Publication steps (manual, in order)

1. **Create the GitHub repository** `nadeem-majeedch/Computer-Networks` if not
   already present (currently the remote exists but is empty).
2. **Initialize and commit locally** (commands in §3).
3. **Push to `main`** (commands in §3).
4. **Enable Pages**: GitHub → repository → *Settings* → *Pages* →
   **Source: GitHub Actions** (one time; the workflow does the rest).
5. **Watch the workflow**: *Actions* tab → "Deploy site to GitHub Pages" — it
   must end green. A red build = the strict gate caught something; read the log.
6. **Verify the live site** at
   `https://nadeem-majeedch.github.io/Computer-Networks/` — check: home loads,
   one lecture page renders a Mermaid diagram, one case page shows **no**
   instructor content, calendar dates match `_calendar.yml`, search works.
7. Until step 6 passes, the site is *expected*, not *verified* — no success may
   be claimed on the basis of this handover.

## 3. Manual commit and push (run yourself; nothing below has been executed)

```bash
cd <this workspace>

# 1. Review what will be committed (generated output is already ignored):
git init -b main
git add -A
git status                      # confirm: no site/, no _build/ staged
git diff --cached --stat        # skim the ~590 markdown files + configs

# 2. Commit:
git commit -m "Computer Networks course: 32 lectures, labs, cases, assessments, site

- 32 lecture packages (notes, slides, worksheets) aligned to master schedule
- 16-lab workbook with instructor keys; safety and setup guides
- 65-case practice bank + assessment package (quizzes, banks, exams, rubrics)
- MkDocs Material site with generated nav, calendar, ICS/CSV exports
- Validation suite: 9 audit/verification tools, all green"

# 3. Connect and push:
git remote add origin https://github.com/nadeem-majeedch/Computer-Networks.git
git push -u origin main
```

Then perform steps 4–7 above. Re-dating a future semester: edit
`site-src/_calendar.yml`, run `python tools/scripts/calendar_lib.py --validate`,
commit, push — the workflow redeploys automatically.

## 4. Rollback / safety notes

- The deployment is atomic (GitHub Pages artifact swap); a bad build simply
  fails before deploy.
- Re-running the workflow (Actions → Re-run) is always safe.
- Generated files are reproducible: `python tools/scripts/build_site_docs.py`
  then `mkdocs build --strict` must both succeed with zero warnings before any
  content change is published.
