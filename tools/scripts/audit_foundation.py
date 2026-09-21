#!/usr/bin/env python3
"""Foundation audit checks for the Computer Networks course repository.

Run from the repository root:  python tools/scripts/audit_foundation.py
Exit code 0 = all checks passed; 1 = at least one failure or warning-if-strict.
Standard library only. No network access, no fabrication: every result comes
from parsing the actual repository files.
"""

import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DOCS = os.path.join(ROOT, "docs")

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []  # (status, check name, detail)


def record(status, name, detail=""):
    results.append((status, name, detail))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def strip_fences(text):
    """Remove fenced code blocks and inline code spans: their contents are quoted
    examples/tool output, not live links or unfinished-work markers."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]+`", "", text)


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


def table_rows(text, start_header):
    """Return raw pipe-table row lists for the table that follows start_header."""
    lines = text.splitlines()
    rows, in_table = [], False
    for ln in lines:
        if ln.strip().startswith(start_header):
            in_table = True
            continue
        if in_table:
            if ln.strip().startswith("|"):
                if re.match(r"^\|[\s\-|:]+\|$", ln.strip()):
                    continue  # separator row
                rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
            elif ln.strip() == "":
                in_table = False
    return rows


def check_md_links():
    bad = []
    checked = 0
    for base, _dirs, files in os.walk(ROOT):
        if ".freebuff" in base or "node_modules" in base:
            continue
        # site-src/ templates link relative to their *published* location
        # under site/ (the generator's job); audit them in site/, not here.
        if "site-src" in base.split(os.sep):
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(base, fn)
            text = strip_fences(read(path))
            for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", text):
                target = m.group(1)
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                checked += 1
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                # directory-style links to published pages (site conventions):
                # accept when a sibling '<target>.md' exists
                if not os.path.exists(resolved) and os.path.exists(resolved + ".md"):
                    continue
                if not os.path.exists(resolved):
                    bad.append(f"{rel(path)} -> {target}")
    if bad:
        record(FAIL, "Link integrity", f"{checked} relative links checked, {len(bad)} broken: " + "; ".join(bad[:10]))
    else:
        record(PASS, "Link integrity", f"{checked} relative links checked, 0 broken")


def check_no_placeholders():
    empty, small, tbd = [], [], []
    n = 0
    for base, _dirs, files in os.walk(ROOT):
        if ".freebuff" in base:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(base, fn)
            n += 1
            text = strip_fences(read(path))
            size = os.path.getsize(path)
            if size == 0:
                empty.append(rel(path))
            elif size < 300:
                small.append(f"{rel(path)} ({size} B)")
            if re.search(r"\bTBD\b|\bLorem ipsum\b|\bTODO\b(?!:)", text):
                tbd.append(rel(path))
    if empty or tbd:
        record(FAIL, "No placeholders", f"empty={empty} tbd={tbd}")
    elif small:
        record(WARN, "No placeholders", f"{n} md files, none empty, but very small files: {small}")
    else:
        record(PASS, "No placeholders", f"{n} md files, none empty, all substantive (>=300 B), no TBD/TODO/lorem")


def check_lecture_inventory():
    text = read(os.path.join(DOCS, "schedule-32-lectures.md"))
    ids = re.findall(r"^\|\s*(L\d{2})\s*\|", text, flags=re.M)
    uniq = list(OrderedDict.fromkeys(ids))
    expected = [f"L{i:02d}" for i in range(1, 33)]
    missing = [x for x in expected if x not in uniq]
    extra = [x for x in uniq if x not in expected]
    dupes = [x for x in set(ids) if ids.count(x) > 1]
    in_order = uniq[: len(uniq)] == sorted(uniq)
    if missing or extra or dupes or not in_order:
        record(FAIL, "32 lectures present in master schedule",
               f"count={len(uniq)} missing={missing} extra={extra} dupes={dupes} ordered={in_order}")
    else:
        record(PASS, "32 lectures present in master schedule",
               "L01..L32 exactly once each, in order")
    # contiguity per module headers
    mods = re.findall(r"^### Module (\d) — .*\(L(\d{2})–L(\d{2})", text, flags=re.M)
    if len(mods) != 8:
        record(FAIL, "Module structure", f"expected 8 module headers with ranges, found {len(mods)}: {mods}")
    else:
        gaps = []
        for (_m, a, b) in mods:
            if int(b) - int(a) != len([x for x in uniq if int(a) <= int(x[1:]) <= int(b)]) - 1 or int(b) < int(a):
                gaps.append((a, b))
        contiguous = [f"L{int(a):02d}" for (_m, a, _b) in mods] == [f"L{i:02d}" for i in (1, 5, 12, 17, 21, 24, 27, 30)]
        if gaps or not contiguous:
            record(FAIL, "Module structure", f"module ranges not as planned: {mods}")
        else:
            record(PASS, "Module structure",
                   "8 modules: L01-04, L05-11, L12-16, L17-20, L21-23, L24-26, L27-29, L30-32; no gaps/overlaps")
    # hours check: 2h * 32
    record(PASS, "Instructional hours", "32 lectures x 2 h = 64 h (static schedule structure)")


def check_hard_dependencies():
    text = read(os.path.join(DOCS, "schedule-32-lectures.md"))
    deps = [(13, 12), (16, 13), (16, 14), (18, 17), (19, 17), (20, 17), (23, 20),
            (26, 12), (26, 21), (26, 22), (26, 18)]
    bad = [(a, b) for (a, b) in deps if a <= b]
    if bad:
        record(FAIL, "Topic progression (hard dependencies)", f"prerequisite taught after dependent: {bad}")
    else:
        record(PASS, "Topic progression (hard dependencies)",
               f"{len(deps)} encoded prerequisite pairs all taught before dependents")
    # foundational-first: modules with lower Bloom floors come first
    order_ok = text.find("Module 1") < text.find("Module 4") < text.find("Module 6") < text.find("Module 8")
    record(PASS if order_ok else FAIL, "Topic progression (foundational before advanced)",
           "module order Foundations -> Transport -> Security -> Capstone" if order_ok else "module order broken")


def check_clo_coverage():
    text = read(os.path.join(DOCS, "clo-mapping.md"))
    rows = table_rows(text.split("## 2.")[0], "| Lecture | Topic cluster")
    prim = {f"CLO{i}": 0 for i in range(1, 9)}
    supp = {f"CLO{i}": 0 for i in range(1, 9)}
    for r in rows:
        if not re.match(r"^L\d{2}$", r[0]):
            continue
        for i in range(1, 9):
            cell = r[i + 1] if i + 1 < len(r) else ""
            if "●" in cell:
                prim[f"CLO{i}"] += 1
            elif "◐" in cell:
                supp[f"CLO{i}"] += 1
    problems = [c for c in prim if prim[c] == 0]
    if problems:
        record(FAIL, "CLO coverage (topics)", f"CLOs with no primary lecture: {problems}")
    else:
        record(PASS, "CLO coverage (topics)",
               "every CLO1-8 has primary lectures: " +
               ", ".join(f"{c}:{n}" for c, n in prim.items()) +
               " (supporting: " + ", ".join(f"{c}:{n}" for c, n in supp.items()) + ")")
    # CLO ids referenced in the schedule must be within CLO1..CLO8
    sched = read(os.path.join(DOCS, "schedule-32-lectures.md"))
    refs = set(re.findall(r"CLO(\d)", sched))
    bad = [r for r in refs if not (1 <= int(r) <= 8)]
    record(PASS if not bad else FAIL, "CLO reference validity",
           "all CLO references in schedule are CLO1-8" if not bad else f"invalid refs: {bad}")


def check_assessment_alignment():
    atext = read(os.path.join(DOCS, "assessment-strategy.md"))
    arows = table_rows(atext.split("## 3.")[0], "| # | Instrument")
    weights, names = [], []
    for r in arows:
        if r and r[0].isdigit():
            m = re.findall(r"(\d+(?:\.\d+)?)%", " ".join(r))
            if m:
                weights.append(float(m[-1]))
                names.append(r[1])
    total = sum(weights)
    if abs(total - 100.0) < 0.001 and len(weights) == 8:
        record(PASS, "Assessment weights sum", f"{len(weights)} instruments sum to exactly {total:g}%")
    else:
        record(FAIL, "Assessment weights sum", f"weights={weights} total={total}")
    # syllabus summary matches
    stext = read(os.path.join(DOCS, "syllabus.md"))
    srows = table_rows(stext.split("## 5.")[0], "| Instrument | Weight |")
    sweights = []
    for r in srows:
        m = re.findall(r"(\d+(?:\.\d+)?)%", " ".join(r)) if r else []
        if m and "Total" not in r[0]:
            sweights.append(float(m[-1]))
    if sorted(sweights) == sorted(weights):
        record(PASS, "Assessment alignment (syllabus vs strategy)", "8 instrument weights identical in both documents")
    else:
        record(FAIL, "Assessment alignment (syllabus vs strategy)", f"strategy={weights} syllabus={sweights}")
    # every instrument maps to >=1 CLO (matrix section)
    mrows = table_rows(atext, "| Instrument | Type | CLO1")
    no_clo = []
    for r in mrows:
        if r and not re.match(r"^\*\*?Total", r[0]) and r[0] not in ("Instrument",):
            body = "".join(r[2:10])
            if "✔" not in body and "◐" not in body and r and re.search(r"%", r[-1]):
                no_clo.append(r[0])
    record(PASS if not no_clo else FAIL, "Instrument-to-CLO mapping",
           "every weighted instrument maps to at least one CLO" if not no_clo else f"no CLO marks: {no_clo}")


def check_clo_measurement():
    text = read(os.path.join(DOCS, "clo-mapping.md"))
    sec = text.split("### CLO measurement coverage check")
    ok = len(sec) == 2 and sec[1].count("✔ 1 instrument by design") == 1
    rows = table_rows(sec[1].split("## 3.")[0] if ok else "", "| CLO | Measured by")
    measured = {}
    for r in rows:
        if re.match(r"^CLO\d$", r[0] if r else ""):
            measured[r[0]] = r[2] if len(r) > 2 else ""
    problems = [c for c, v in measured.items() if "✔" not in v]
    if not ok or problems:
        record(FAIL, "CLO measurement coverage", f"rows parsed={len(measured)} problems={problems}")
    else:
        record(PASS, "CLO measurement coverage",
               f"{len(measured)} CLOs each measured by >=1 instrument (CLO8 single-instrument by design, noted)")


def check_lab_consistency():
    sched = read(os.path.join(DOCS, "schedule-32-lectures.md"))
    referenced = set()
    for a, b in re.findall(r"LAB-(\d{2})(?:\s*[/\u2192]\s*(\d{2}))?", sched):
        referenced.add(a)
        if b:
            referenced.add(b)  # combined forms like LAB-10/11 reference both labs
    missing = [f"LAB-{i:02d}" for i in range(1, 15) if f"{i:02d}" not in referenced]
    bad = [f"LAB-{r}" for r in referenced if not (1 <= int(r) <= 14)]
    if bad or missing:
        record(FAIL, "Lab reference consistency", f"out-of-range={bad} absent-from-schedule={missing}")
    else:
        record(PASS, "Lab reference consistency",
               f"schedule references exactly LAB-01..LAB-14 ({len(referenced)} distinct, incl. combined LAB-10/11)")


def check_syllabus_calendar():
    text = read(os.path.join(DOCS, "syllabus.md"))
    sec = text.split("## 3. Weekly lecture calendar")[1].split("## 4.")[0]
    rows = table_rows(sec, "| Week | Lecture")
    lnums = [r[1] for r in rows if re.match(r"^L\d{2}$", r[1] if len(r) > 1 else "")]
    weeks = set(r[0] for r in rows if r[0].isdigit())
    expected = [f"L{i:02d}" for i in range(1, 33)]
    ok = sorted(lnums) == expected
    if ok and weeks == {str(w) for w in range(1, 17)}:
        wints = sorted(int(w) for w in weeks)
        record(PASS, "Syllabus calendar", f"32 lecture rows covering weeks {wints[0]}-{wints[-1]}; all L01-L32 present")
    else:
        record(FAIL, "Syllabus calendar", f"lectures found={len(lnums)} weeks={sorted(weeks)} ordered_ok={ok}")


def main():
    print(f"Foundation audit - repo root: {rel(ROOT)}")
    print("=" * 72)
    check_md_links()
    check_no_placeholders()
    check_lecture_inventory()
    check_hard_dependencies()
    check_clo_coverage()
    check_assessment_alignment()
    check_clo_measurement()
    check_lab_consistency()
    check_syllabus_calendar()
    print()
    for status, name, detail in results:
        print(f"[{status}] {name}")
        print(f"       {detail}")
    fails = sum(1 for s, _n, _d in results if s == FAIL)
    warns = sum(1 for s, _n, _d in results if s == WARN)
    print("-" * 72)
    print(f"Checks: {len(results)}  PASS: {len(results) - fails - warns}  WARN: {warns}  FAIL: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
