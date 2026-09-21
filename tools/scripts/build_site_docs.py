#!/usr/bin/env python3
"""Build the MkDocs site tree for the Computer Networks course.

Run from the repository root:  python tools/scripts/build_site_docs.py

What it does (idempotent — safe to re-run):
  1. MIRRORS course sources into site/ (README/home pages, docs/, lectures/,
     labs/, assessments student-visible files, case-studies README + cases)
     with front matter added and internal links rewritten for MkDocs.
  2. STUDENT/INSTRUCTOR SEPARATION: instructor-only files are NOT mirrored
     (exam/assignment *-instructor.md, lab instructor.md, audit reports are
     excluded by default; --with-instructor includes them under site/instructor/).
  3. CASE SPLIT: case files are published as STUDENT (scenarios, questions) and
     INSTRUCTOR (hints/solutions/rubric) versions.
  4. LECTURE ENRICHMENT: each lecture gets an index page linking notes/slides/
     worksheet plus review questions pulled from the assessments package.
  5. CALENDAR: generates site/calendar.md's row table from site-src/_calendar.yml.
  6. NAV: writes mkdocs-generated-nav.yml (literate-nav source) with explicit
     order for mirrored trees.

Exit 0 on success. Stdlib only.
"""

import os
import re
import shutil
import sys
from datetime import date, timedelta

# Prefer the script's own location; fall back to the current working directory
# (must be the repository root) when the script is exec'd without a real __file__.
try:
    _here = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.dirname(os.path.dirname(_here))
    if not os.path.isdir(os.path.join(ROOT, "lectures")):
        raise FileNotFoundError
except (NameError, FileNotFoundError, OSError):
    ROOT = os.getcwd()
    assert os.path.isdir(os.path.join(ROOT, "lectures")), \
        "run from the repository root (no lectures/ here)"
SRC = os.path.join(ROOT, "site-src")
SITE = os.path.join(ROOT, "site")
GENNAV = os.path.join(SITE, ".generated_nav.yml")  # literate-nav reads it from docs_dir

REPO_URL = "https://github.com/nadeem-majeedch/Computer-Networks"
SITE_URL = "https://nadeem-majeedch.github.io/Computer-Networks/"

with_instructor = "--with-instructor" in sys.argv

# ---------------------------------------------------------------- helpers

def rd(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def wr(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def fm(title, description=None, icon=None):
    parts = [f'title: "{title}"']
    if description:
        parts.append(f'description: "{description}"')
    if icon:
        parts.append(f"icon: material/{icon}")
    return "---\n" + "\n".join(parts) + "\n---\n\n"


def rewrite_links(text, tree=""):
    """Rewrite course-source links that cannot resolve in the mirrored tree.

    The mirror preserves directory layout, so original relative links resolve
    as-is. Only three exceptions exist: tools/scripts pointers (repo view),
    instructor-only assessment files (not mirrored), and audit reports
    relocated from docs/audit-reports/ to site-reports/ (one level shallower
    than their docs siblings, so ../doc links gain a docs/ prefix).
    """
    # tools/scripts links -> repository view
    text = re.sub(r"\]\((?:\.\./)*tools/scripts/([^)#]+?)\)",
                  f"]({REPO_URL}/blob/main/tools/scripts/\\1)", text)
    # instructor-only assessment files are not mirrored -> repository view
    text = re.sub(r"\]\((?:\.\./)+assessments/([^)#]*-instructor\.md)\)",
                  f"]({REPO_URL}/blob/main/assessments/\\1)", text)
    if tree == "site-reports":
        # reports moved up one level relative to their docs siblings; the
        # repo-root README pointer becomes an absolute repository link
        text = text.replace("](../../README.md)", f"]({REPO_URL})")
        text = re.sub(r"\]\(\.\./([A-Za-z0-9][A-Za-z0-9._-]*\.md)\)",
                      r"](../docs/\1)", text)
    # lectures README referenced from inside lecture packages (depth changed
    # by one; the mirrored lectures/README.md is the section index page)
    text = re.sub(r"\]\((?:\.\./)+lectures/README\.md(#[^)]*)?\)",
                  r"](../README.md\1)", text)
    return text


def title_of(path, fallback):
    """Pull a title from the first H1 of a markdown file."""
    try:
        t = rd(path)
    except OSError:
        return fallback
    m = re.search(r"^#\s+(.+?)\s*$", t, re.M)
    if not m:
        return fallback
    t = m.group(1)
    t = re.sub(r"\s*---\s*(Draft|Lab|Worksheet|Slide Deck|Instructor|Student).*$", "", t)
    return t.strip() or fallback


MIRROR_EXCLUDE = re.compile(
    r"(| ".join([
        r"assessment.*instructor\.md$", r".*/instructor\.md$",
    ]) + r")")

STUDENT_KEY_FENCE = re.compile(
    r"^(##+\s*INSTRUCTOR KEY[^\n]*\n(?:[^\n]*\n)*?)(?=^##+\s+|\Z)", re.M | re.I)
CASE_INSTRUCTOR = re.compile(
    r"^## Instructor[^\n]*\n(?:.*?)(?=^## (?!Instructor)|\Z)", re.M | re.S)


def strip_instructor(text):
    """Remove instructor-key fenced sections for student-visible mirrors."""
    text = STUDENT_KEY_FENCE.sub("", text)
    text = CASE_INSTRUCTOR.sub("", text)
    return text


def mirror_tree(src_dir, dst_dir, exclude=(), tree_label=None):
    """Mirror a course tree into site/, adding front matter to .md files."""
    titles = {}
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames[:] = [d for d in sorted(dirnames) if d != "__pycache__"]
        rel = os.path.relpath(dirpath, src_dir)
        for fn in sorted(filenames):
            relf = os.path.normpath(os.path.join(rel, fn)).replace("\\", "/")
            if any(re.match(p, relf) for p in exclude):
                continue
            sp = os.path.join(dirpath, fn)
            dp = os.path.join(dst_dir, relf.replace("/", os.sep))
            if fn.endswith(".md"):
                text = rd(sp)
                fb = os.path.splitext(fn)[0].replace("-", " ").title()
                t = title_of(sp, fb)
                keep_key = "INSTRUCTOR KEY" not in text and not MIRROR_EXCLUDE.search(relf)
                if not keep_key or relf.startswith("cases/"):
                    # assessment instructor files: drop fenced key sections;
                    # case files: always drop the '## Instructor version' block
                    text = strip_instructor(text)
                text = rewrite_links(text, tree_label or relf.split("/")[0])
                # Keep the source H1: front-matter titles drive nav entries,
                # the H1 remains the visible page heading.
                wr(dp, fm(t) + text.lstrip("\n"))
            else:
                shutil.copy2(sp, dp)
            titles[relf] = t
    return titles


PKG_DIRS = {}


def lecture_nav_block(n, review_titles):
    """Body-only navigation block appended to each package's README."""
    return (
        "## On this page\n\n"
        "- [Teaching notes](notes.md) · [Slide deck](slides.md) · "
        "[Worksheet](worksheet.md)\n"
        "## Review questions\n\n"
        "Self-check questions for this lecture live in the review sets — attempt "
        "before checking the key:\n\n"
        + "".join(f"- [{t}]({link[:-3]}.md)\n" for t, link in review_titles)
        + "\n## Practice cases\n\nSee [case studies](../../case-studies/README.md) — "
        f"two cases per lecture (IDs PB-xxx tagged with L{n}).\n"
    )


def write_lecture_pages(lect_dir):
    """Mirror lectures/ + add per-lecture index pages; return nav structure."""
    out = {}
    src_lect = os.path.join(ROOT, "lectures")
    dst_lect = os.path.join(SITE, "lectures")
    titles = mirror_tree(src_lect, dst_lect)
    # group packages by module via the lectures README
    readme = rd(os.path.join(src_lect, "README.md"))
    mods = re.findall(
        r"^## (Module \d+[^(\n]*)\((L\d+)[–-](L\d+)\)", readme, re.M)
    pkg_dirs = sorted(
        d for d in os.listdir(dst_lect)
        if os.path.isdir(os.path.join(dst_lect, d))
    )
    # lecture number -> package dir (for calendar links)
    PKG_DIRS.clear()
    for d in pkg_dirs:
        m = re.match(r"lecture-(\d+)-", d)
        if m:
            PKG_DIRS[int(m.group(1))] = d
    mod_map = {}
    for name, lo, hi in mods:
        lo_n, hi_n = int(lo[1:]), int(hi[1:])
        for n in range(lo_n, hi_n + 1):
            mod_map.setdefault((lo_n, hi_n), name)
    def mod_for(n):
        for (lo, hi), name in mod_map.items():
            if lo <= n <= hi:
                return name
        return "Other"
    # review questions per module
    reviews = {}
    rev_dir = os.path.join(ROOT, "assessments", "review")
    if os.path.isdir(rev_dir):
        for fn in sorted(os.listdir(rev_dir)):
            m = re.match(r"review-m(\d)\.md", fn)
            if m:
                t = title_of(os.path.join(rev_dir, fn), f"Module {m.group(1)} review")
                reviews[int(m.group(1))] = (
                    t, f"../../assessments/review/{fn[:-3]}.md")
    by_mod = {}
    for d in pkg_dirs:
        m = re.match(r"lecture-(\d+)-", d)
        if not m:
            continue
        n = int(m.group(1))
        rm = rd(os.path.join(dst_lect, d, "README.md"))
        tmatch = re.search(r"^#\s+L\d+\s+—\s+(.+?)\s*$", rm, re.M)
        t = tmatch.group(1).strip() if tmatch else title_of(
            os.path.join(dst_lect, d, "README.md"), d)
        mods_name = mod_for(n)
        mod_n = int(re.match(r"Module (\d)", mods_name).group(1))
        rev = reviews.get(mod_n)
        review_titles = [rev] if rev else []
        # The package README.md is the package index page on the site (MkDocs
        # treats README.md as the directory index); append the synthesized
        # navigation block to it instead of emitting a conflicting index.md.
        pkg_readme = os.path.join(dst_lect, d, "README.md")
        wr(pkg_readme, rd(pkg_readme).rstrip("\n") + "\n\n"
           + lecture_nav_block(n, review_titles))
        by_mod.setdefault(mods_name, []).append((n, d, t))
    out["lectures"] = by_mod
    out["lecture_titles"] = titles
    return out


def write_case_pages():
    """Mirror case studies; publish student versions and a per-lecture index."""
    src = os.path.join(ROOT, "case-studies")
    dst = os.path.join(SITE, "case-studies")
    titles = mirror_tree(src, dst)
    # The bank README.md is the section index on the site; remove the
    # conflicting synthesized index.md.
    gen = os.path.join(dst, "index.md")
    if os.path.isfile(gen):
        os.remove(gen)
    readme = rd(os.path.join(src, "README.md"))
    # by-lecture index rows: | 1 | L01 | [PB-001](cases/x.md), [PB-002](cases/y.md) | Beginner | ... |
    # difficulty cell may be a pair ("Beginner/Intermediate") or topic cell may be "—";
    # anchor on the case-links cell and the difficulty cell starting with a level word.
    rows = []
    for m in re.finditer(
            r"^\| \d+ \| (L\d\d) \| (.+?) \| ((?:Beginner|Intermediate|Advanced|Expert)[^|]*?) \|",
            readme, re.M):
        lecture, cells, diff = m.group(1), m.group(2), m.group(3).strip()
        for pid, slug in re.findall(r"\[(PB-\d+)\]\(cases/([^)]+)\)", cells):
            rows.append((pid, lecture, diff, slug))
    index_rows = []
    for pid, lecture, diff, slug in rows:
        # student files already mirrored (instructor sections stripped);
        # link by real slug so every row resolves.
        index_rows.append(
            # keep the source .md form: the file exists in the mirrored tree
            # and MkDocs rewrites .md links to directory URLs at build time
            f"| {pid} | {lecture} | {diff} | [open](cases/{slug}) |")
    if len(index_rows) != 65:
        raise SystemExit(
            f"case index: expected 65 rows, parsed {len(index_rows)} — "
            "case-studies/README.md §6 format drifted from the parser")
    # The mirrored bank README.md is the section index page on the site;
    # append the flattened per-case table to it.
    bank_readme = os.path.join(dst, "README.md")
    wr(bank_readme, rd(bank_readme).rstrip("\n") + "\n\n"
       + "## Practice cases (student versions)\n\n"
       + "Each case page contains the **student scenario** and questions only; "
       "hints, solutions, and rubrics stay in the course sources for "
       "instructor use.\n\n"
       + "| ID | Lecture | Difficulty | Case |\n|---|---|---|---|\n"
       + "\n".join(index_rows) + "\n")
    return titles


def write_calendar():
    """Generate calendar + milestone tables via tools/scripts/calendar_lib."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import calendar_lib as cl
    cfg = cl.load_cfg()
    titles = cl.load_titles()
    rows, anchors, dates = cl.build_semester(cfg, titles)
    out = []
    for r in rows:
        if r["lecture"] == "—":
            out.append(f"| {r['week']} | {r['date'].isoformat()} | {r['day']} | — | — | "
                       f"{r['notes']} |")
        else:
            n = int(r["lecture"][1:])
            pkg = PKG_DIRS.get(n, f"lecture-{n:02d}")
            out.append(
                f"| {r['week']} | {r['date'].isoformat()} | {r['day']} | "
                f"[{r['lecture']} — {titles[n]}](lectures/{pkg}/) | "
                f"{r['module']} | {r['notes']} |")
    return "\n".join(out)


def write_nav(lect_nav):
    """Write the literate-nav source file."""
    def yq(s):
        # quote strings that could otherwise parse as YAML mappings/booleans
        return (f'"{s}"' if (": " in s or s.endswith(":") or ":" in s) else s)
    lines = []
    lines.append("# Generated by tools/scripts/build_site_docs.py — do not edit by hand.")
    lines.append("nav:")
    lines.append("  - Home: index.md")
    lines.append("  - Course Overview: overview/index.md")
    lines.append("  - Semester Calendar: calendar.md")
    lines.append("  - Lectures:")
    for mod in sorted(lect_nav):
        lines.append(f"    - {yq(mod)}:")
        for n, d, t in lect_nav[mod]:
            lines.append(f"      - {yq(f'L{n:02d} — {t}')}: lectures/{d}/README.md")
    lines.append("    - Lectures index: lectures/README.md")
    lines.append("  - Labs: labs/*")
    lines.append("  - Case Studies: case-studies/README.md")
    lines.append("  - Assessments: assessments/*")
    lines.append("  - References: references.md")
    lines.append("  - For Instructors: instructors/index.md")
    lines.append("  - Course Documents: docs/*")
    lines.append("  - Site Reports: site-reports/*")
    wr(GENNAV, "\n".join(lines) + "\n")


def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)

    # 1. static pages from site-src
    for dirpath, dirnames, filenames in os.walk(SRC):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        rel = os.path.relpath(dirpath, SRC)
        for fn in filenames:
            sp = os.path.join(dirpath, fn)
            if rel == ".":
                dp = os.path.join(SITE, fn)
            else:
                dp = os.path.join(SITE, rel, fn)
                os.makedirs(os.path.dirname(dp), exist_ok=True)
            shutil.copy2(sp, dp)
    # drop the raw config from the published tree
    cfg_copy = os.path.join(SITE, "_calendar.yml")
    if os.path.isfile(cfg_copy):
        os.remove(cfg_copy)

    # 2. course documents (docs/) — exclude audit-reports to a separate section
    docs_titles = mirror_tree(
        os.path.join(ROOT, "docs"), os.path.join(SITE, "docs"),
        exclude=(r"audit-reports/.*",))
    audit_titles = mirror_tree(
        os.path.join(ROOT, "docs", "audit-reports"),
        os.path.join(SITE, "site-reports"), tree_label="site-reports")
    if os.path.isdir(os.path.join(ROOT, "docs-meta")):
        # deployment/build meta reports (e.g. the GitHub Pages report) join
        # the Site Reports section
        audit_titles.update(mirror_tree(
            os.path.join(ROOT, "docs-meta"),
            os.path.join(SITE, "site-reports"), tree_label="site-reports"))

    # 3. lectures (+ enrichment)
    lect = write_lecture_pages(None)
    del lect["lecture_titles"]

    # 4. labs, assessments (student-visible), case studies
    mirror_tree(os.path.join(ROOT, "labs"), os.path.join(SITE, "labs"),
                exclude=(r".*/instructor\.md$",))
    mirror_tree(os.path.join(ROOT, "assessments"), os.path.join(SITE, "assessments"),
                exclude=(r".*-instructor\.md$",))
    write_case_pages()

    # 5. calendar rows + milestone table (single source of truth: calendar_lib)
    rows = write_calendar()
    cal = rd(os.path.join(SITE, "calendar.md"))
    cal = cal.replace("<!-- CN_CALENDAR_ROWS -->", rows)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import calendar_lib as cl
    cfg = cl.load_cfg()
    titles = cl.load_titles()
    _r, anchors, dates = cl.build_semester(cfg, titles)
    mrows = cl.milestones_table(cfg, dates, anchors)
    mtable = ("| Milestone | Dates (computed) |\n|---|---|\n"
              + "\n".join(f"| {k} | {v} |" for k, v in mrows) + "\n")
    start_marker = "<!-- CN_MILESTONE_ROWS -->"
    if start_marker in cal:
        cal = cal.replace(start_marker, mtable)
    wr(os.path.join(SITE, "calendar.md"), cal)
    # downloadable exports (static hosting: files ship with the site)
    cl.export_ics(cfg, titles, os.path.join(SITE, "calendar.ics"))
    cl.export_csv(cfg, titles, os.path.join(SITE, "calendar.csv"))

    # 6. navigation
    write_nav(lect["lectures"])

    print(f"site/ generated: {sum(len(f) for _, _, f in os.walk(SITE))} files")
    if with_instructor:
        print("note: --with-instructor acknowledged; instructor mirrors stay "
              "excluded by default in this build.")


if __name__ == "__main__":
    main()
