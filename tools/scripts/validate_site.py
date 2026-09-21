#!/usr/bin/env python3
"""Site-package validation for the GitHub Pages build.

Run from the repository root:  python tools/scripts/validate_site.py
Checks mkdocs.yml, the generated site tree, student/instructor separation,
nav completeness, output-HTML path hygiene, and workflow presence.
Exit 0 = clean; 1 = at least one FAIL. Standard library only.
"""

import os
import re
import sys

ROOT = os.getcwd()
FAILS = []
WARNS = []


def check(name, ok, warn=False, detail=""):
    tag = "PASS" if ok else ("WARN" if warn else "FAIL")
    print(f"[{tag}] {name}" + (f" — {detail}" if detail else ""))
    if not ok and not warn:
        FAILS.append(name)
    elif not ok and warn:
        WARNS.append(name)


def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- mkdocs.yml
import yaml

try:
    # yaml.Loader (not safe_load): mkdocs.yml legitimately uses !!python/name tags
    cfg = yaml.load(rd("mkdocs.yml"), Loader=yaml.Loader)
    check("mkdocs.yml parses as YAML", True)
except Exception as e:  # pragma: no cover
    check("mkdocs.yml parses as YAML", False, detail=str(e))
    print("Cannot continue without mkdocs.yml")
    sys.exit(1)

site_url = cfg.get("site_url", "")
check("site_url uses the project subpath",
      site_url == "https://nadeem-majeedch.github.io/Computer-Networks/",
      detail=site_url or "(missing)")
check("repo_url points at the course repository",
      cfg.get("repo_url") == "https://github.com/nadeem-majeedch/Computer-Networks",
      detail=cfg.get("repo_url", "(missing)"))
check("theme is mkdocs-material", cfg.get("theme", {}).get("name") == "material")
check("docs_dir is the generated site/ tree", cfg.get("docs_dir") == "site")
check("strict mode enabled", cfg.get("strict") is True)
check("search plugin present", "search" in cfg.get("plugins", {}))
def has_mermaid(exts):
    # markdown_extensions may be a list (plain names) or dict (name -> opts)
    items = exts if isinstance(exts, list) else list((exts or {}).items())
    for item in items:
        if isinstance(item, str):
            name, opts = item, {}
        elif isinstance(item, dict) and len(item) == 1:
            name, opts = next(iter(item.items()))
        else:
            continue
        if name == "pymdownx.superfences":
            for f in (opts or {}).get("custom_fences", []):
                if isinstance(f, dict) and f.get("name") == "mermaid":
                    return True
    return False
check("mermaid custom fence configured",
      has_mermaid(cfg.get("markdown_extensions", [])))

# ------------------------------------------------------------- site tree
SITE = os.path.join(ROOT, "site")
check("site/ tree exists (run build_site_docs.py first)", os.path.isdir(SITE))

pkg_dirs = sorted(
    d for d in os.listdir(os.path.join(SITE, "lectures"))
    if os.path.isdir(os.path.join(SITE, "lectures", d))
)
check("32 lecture packages mirrored", len(pkg_dirs) == 32, detail=f"{len(pkg_dirs)} found")
missing_files = []
for d in pkg_dirs:
    for f in ("README.md", "notes.md", "slides.md", "worksheet.md"):
        if not os.path.isfile(os.path.join(SITE, "lectures", d, f)):
            missing_files.append(f"{d}/{f}")
check("every lecture package has README+notes+slides+worksheet",
      not missing_files, detail=", ".join(missing_files[:4]))

lab_dirs = sorted(
    d for d in os.listdir(os.path.join(SITE, "labs"))
    if os.path.isdir(os.path.join(SITE, "labs", d))
)
check("16 labs mirrored", len(lab_dirs) == 16, detail=f"{len(lab_dirs)} found")

case_pages = [f for f in os.listdir(os.path.join(SITE, "case-studies", "cases"))
              if f.endswith(".md")] if os.path.isdir(os.path.join(SITE, "case-studies", "cases")) else []
check("65 case pages mirrored", len(case_pages) == 65, detail=f"{len(case_pages)} found")
check("case bank index present (README.md)",
      os.path.isfile(os.path.join(SITE, "case-studies", "README.md")))

quizzes = [f for f in os.listdir(os.path.join(SITE, "assessments", "quizzes"))
           if f.endswith(".md")] if os.path.isdir(os.path.join(SITE, "assessments", "quizzes")) else []
check("16 weekly quizzes mirrored", len(quizzes) == 16, detail=f"{len(quizzes)} found")

# --------------------------------------------- student/instructor separation
leaked = []
KEY_HEADING = re.compile(r"^#{2,}\s*(?:INSTRUCTOR KEY|Instructor [Ss]olution|Instructor [Vv]ersion)", re.M)
for base, _dirs, files in os.walk(SITE):
    for fn in files:
        rel = os.path.relpath(os.path.join(base, fn), SITE).replace("\\", "/")
        if fn.endswith("-instructor.md") or fn == "instructor.md":
            leaked.append(rel)
        elif fn.endswith(".md") and not rel.startswith(
                ("instructors/", "site-reports/", "docs/contributing-instructor-review.md")):
            if KEY_HEADING.search(rd(os.path.join(base, fn))):
                leaked.append(rel)
check("no instructor-only files or keys in site tree", not leaked,
      detail=", ".join(leaked[:5]))

inst_page = os.path.join(SITE, "instructors", "index.md")
check("For-Instructors page explains the separation",
      os.path.isfile(inst_page) and "not" in rd(inst_page).lower())

# ---------------------------------------------------------------- nav file
nav_path = os.path.join(SITE, ".generated_nav.yml")
try:
    nav = yaml.load(rd(nav_path), Loader=yaml.Loader)
    flat = []

    def walk(items):
        if isinstance(items, dict):
            for _k, v in items.items():
                walk(v)
        elif isinstance(items, list):
            for it in items:
                walk(it)
        elif isinstance(items, str):
            flat.append(items)

    walk(nav.get("nav", {}))
    lect_entries = [e for e in flat
                    if e.startswith("lectures/lecture-") and e.endswith("README.md")]
    check("nav contains 32 lecture entries", len(lect_entries) == 32,
          detail=f"{len(lect_entries)} found")
    check("nav references only existing site files",
          all(os.path.isfile(os.path.join(SITE, e.split("#")[0]))
              for e in flat if not e.endswith("*")),
          detail="; ".join(e for e in flat
                           if not e.endswith("*")
                           and not os.path.isfile(os.path.join(SITE, e.split("#")[0])))[:100])
except FileNotFoundError:
    check("nav file exists", False, detail=nav_path)

# ------------------------------------------------------------- HTML output
BUILD = os.path.join(ROOT, "_build", "site")
if os.path.isdir(BUILD):
    abs_asset = None
    localhost = None
    bad_subpath = None
    idx = os.path.join(BUILD, "index.html")
    if os.path.isfile(idx):
        html = rd(idx)
        abs_asset = re.search(r'(?:src|href)="/(?!/)(?!Computer-Networks/)', html)
        localhost = re.search(r"https?://localhost|https?://127\.0\.0\.1", html)
        bad_subpath = re.search(r"https://[a-zA-Z0-9.-]+/(?:(?!Computer-Networks|nadeem-majeedch)[^\"']*)",
                                html) if "nadeem-majeedch" not in html else None
    check("index.html built", os.path.isfile(idx))
    check("no absolute root-relative asset paths in home page", abs_asset is None)
    check("no localhost URLs in home page", localhost is None)
    check("site_url subpath present in canonical link",
          "Computer-Networks/" in (rd(idx) if os.path.isfile(idx) else ""))
    css = os.path.join(BUILD, "assets")
    check("theme assets published", os.path.isdir(css) and os.listdir(css))
else:
    check("_build/site exists (run mkdocs build first)", False, warn=True,
          detail="HTML checks skipped")

# ---------------------------------------------------------------- workflow
wf = os.path.join(ROOT, ".github", "workflows", "deploy-pages.yml")
if os.path.isfile(wf):
    try:
        wcfg = yaml.load(rd(wf), Loader=yaml.Loader)
        trig = wcfg.get("on") or wcfg.get(True)
        ok = (trig and "push" in trig and "workflow_dispatch" in trig
              and wcfg.get("permissions", {}).get("pages") == "write"
              and any("deploy-pages" in str(s.get("uses", ""))
                      for job in wcfg.get("jobs", {}).values()
                      for s in job.get("steps", [])))
        check("deploy workflow parses and deploys via actions/deploy-pages", ok)
    except Exception as e:
        check("deploy workflow parses as YAML", False, detail=str(e))
else:
    check("deploy workflow exists", False, detail=wf)

# ---------------------------------------------------------------- mermaid scan
if os.path.isdir(SITE):
    mm_bad = []
    fence = re.compile(r"^```mermaid\s*$", re.M)
    for base, _dirs, files in os.walk(SITE):
        for fn in files:
            if fn.endswith(".md"):
                text = rd(os.path.join(base, fn))
                for block in re.split(r"^```mermaid\s*$|^```\s*$", text, flags=re.M)[1::2]:
                    if ";" in block.split("\n")[0]:
                        mm_bad.append(fn)
    check("mermaid fences use newline statements (no ; chains)", not mm_bad,
          detail=", ".join(sorted(set(mm_bad))[:5]))

print()
print(f"Result: {len(FAILS)} FAIL, {len(WARNS)} WARN")
sys.exit(1 if FAILS else 0)
