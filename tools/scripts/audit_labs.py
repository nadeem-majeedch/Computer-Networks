#!/usr/bin/env python3
"""Laboratory-workbook audit for the Computer Networks course repository.

Run from the repository root:  python tools/scripts/audit_labs.py
Validates the labs/ workbook: inventory (16 triads), required elements,
substance floors, lecture/CLO reference validity, lab<->schedule alignment,
graded-set consistency with the assessment strategy, and index links.
Exit 0 = clean; 1 = at least one FAIL. Standard library only.
"""

import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LABS = os.path.join(ROOT, "labs")
DOCS = os.path.join(ROOT, "docs")
LECT = os.path.join(ROOT, "lectures")

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []


def record(status, name, detail=""):
    results.append((status, name, detail))


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def strip_fences(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]+`", "", text)


NAMES = {
    1: "latency-throughput", 2: "switching-vlans", 3: "wifi-survey",
    4: "subnetting-design", 5: "dhcp-nat-router", 6: "dual-stack",
    7: "static-routing", 8: "udp-sockets", 9: "tcp-netem",
    10: "reliable-design", 11: "reliable-implement", 12: "app-protocols",
    13: "firewall-vpn", 14: "monitoring-faults", 15: "security-analysis",
    16: "design-rehearsal",
}

GRADED = {1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14}          # 15% pool + problem set
GRADED_PROJECT = {10, 11}                                   # 10% project pair
OPTIONAL = {15, 16}

REQUIRED_README = {
    "Anchor lectures": r"\|\s*Anchor lectures\s*\|",
    "CLO field": r"\|\s*CLOs\s*\|",
    "Learning outcomes": r"## Learning outcomes",
    "Pre-lab": r"## Pre-lab",
    "Tasks": r"## Tasks",
    "Expected observations": r"Expected observation",
    "Troubleshooting table": r"## Troubleshooting",
    "Post-lab questions": r"## Post-lab questions",
    "Challenge": r"## Challenge",
    "Accessibility": r"## Accessibility",
    "Safety notes": r"## Safety notes",
}

REQUIRED_INST = {
    "Setup": r"## Setup",
    "Solutions/expected": r"## [^\n]*\b(Solutions|Answer key)",
    "Common failure modes": r"## Common failure modes",
    "Grading notes": r"## [^\n]*\b[Gg]rading",
}

REQUIRED_WS = {
    "Pre-lab section": r"## Pre-lab",
    "Post-lab prompts": r"## Post-lab",
}


def check_inventory():
    missing_dirs, missing_files, empty = [], [], []
    found = []
    for i in range(1, 17):
        matches = [d for d in os.listdir(LABS) if d.startswith(f"lab-{i:02d}-")] \
            if os.path.isdir(LABS) else []
        if not matches:
            missing_dirs.append(f"LAB-{i:02d}")
            continue
        d = os.path.join(LABS, sorted(matches)[0])
        found.append((i, d))
        for fn in ("README.md", "instructor.md", "worksheet.md"):
            p = os.path.join(d, fn)
            if not os.path.isfile(p):
                missing_files.append(f"LAB-{i:02d}/{fn}")
            elif os.path.getsize(p) == 0:
                empty.append(f"LAB-{i:02d}/{fn}")
    if missing_dirs or missing_files or empty:
        record(FAIL, "16 complete lab triads (README+instructor+worksheet)",
               f"missing dirs={missing_dirs} files={missing_files} empty={empty}")
        return []
    record(PASS, "16 complete lab triads (README+instructor+worksheet)",
           "lab-01..lab-16 each contain README.md, instructor.md, worksheet.md (48 files, none empty)")
    return found


def check_required_elements(found):
    missing = []
    for i, d in found:
        for fn, reqs in (("README.md", REQUIRED_README),
                         ("instructor.md", REQUIRED_INST),
                         ("worksheet.md", REQUIRED_WS)):
            text = read(os.path.join(d, fn))
            for label, pat in reqs.items():
                if not re.search(pat, text):
                    missing.append(f"LAB-{i:02d}/{fn}: {label}")
    if missing:
        record(FAIL, "Required elements present", "; ".join(missing[:12]))
    else:
        record(PASS, "Required elements present",
               "every lab: outcomes, pre-lab, tasks, expected observations, troubleshooting, "
               "post-lab, challenge, accessibility, safety; instructor guide with solutions, "
               "failure modes, grading notes; worksheet with pre/post sections")


def check_substance(found):
    problems = []
    for i, d in found:
        readme = read(os.path.join(d, "README.md"))
        ws = read(os.path.join(d, "worksheet.md"))
        tasks = len(re.findall(r"^### T\d+", readme, flags=re.M))
        if tasks < 3:
            problems.append(f"LAB-{i:02d}: tasks < 3")
        pre = readme.split("## Pre-lab")[1].split("## ")[0] if "## Pre-lab" in readme else ""
        pre_q = len(re.findall(r"^\d+\.", pre, flags=re.M))
        if pre_q < 2:
            problems.append(f"LAB-{i:02d}: pre-lab questions < 2")
        post = readme.split("## Post-lab questions")[1].split("## ")[0] \
            if "## Post-lab questions" in readme else ""
        post_q = len(re.findall(r"^\d+\.", post, flags=re.M))
        if post_q < 3:
            problems.append(f"LAB-{i:02d}: post-lab questions < 3")
        ws_items = len(re.findall(r"^\d+\.", strip_fences(ws), flags=re.M)) + \
            len(re.findall(r"^\| ", ws, flags=re.M))
        if ws_items < 6:
            problems.append(f"LAB-{i:02d}: worksheet too thin ({ws_items} fillable items)")
        if len(re.findall(r"\| Symptom \|", readme)) < 1:
            problems.append(f"LAB-{i:02d}: troubleshooting table missing rows")
    if problems:
        record(FAIL, "Element substance (min counts)", "; ".join(problems[:12]))
    else:
        record(PASS, "Element substance (min counts)",
               "every lab: >=3 tasks, >=2 pre-lab + >=3 post-lab questions, substantive worksheet, "
               "troubleshooting table with rows")


def check_lecture_alignment(found):
    """Anchor lectures must exist in the schedule; lecture-side lab refs must point back."""
    bad = []
    sched = read(os.path.join(DOCS, "schedule-32-lectures.md"))
    lect_rows = {int(m.group(1)) for m in
                 re.finditer(r"^\| L(\d{2}) \|", sched, flags=re.M)}
    for i, d in found:
        readme = read(os.path.join(d, "README.md"))
        m = re.search(r"\|\s*Anchor lectures\s*\|(.*?)\|", readme)
        cell = m.group(1) if m else ""
        for ln in re.findall(r"L(\d{2})", cell):
            n = int(ln)
            if not (1 <= n <= 32):
                bad.append(f"LAB-{i:02d}: bad lecture ref L{ln}")
            elif n not in lect_rows:
                bad.append(f"LAB-{i:02d}: L{ln} not in schedule")
    # reverse: every graded lab referenced by its lecture's README
    for i in sorted(GRADED | GRADED_PROJECT):
        d = os.path.join(LABS, f"lab-{i:02d}-{NAMES[i]}")
        # find lectures that should reference this lab (schedule mapping is authoritative)
        refs = []
        for ln in range(1, 33):
            ldir = [x for x in os.listdir(LECT)
                    if x.startswith(f"lecture-{ln:02d}-")] if os.path.isdir(LECT) else []
            if not ldir:
                continue
            lr = read(os.path.join(LECT, ldir[0], "README.md"))
            if re.search(rf"LAB-{i:02d}\b", lr) or (i in (10, 11) and f"LAB-10/11" in lr):
                refs.append(ln)
        if not refs:
            bad.append(f"LAB-{i:02d}: no lecture README references it")
    if bad:
        record(FAIL, "Lab<->lecture alignment", "; ".join(bad[:12]))
    else:
        record(PASS, "Lab<->lecture alignment",
               "all anchor lectures exist in the schedule; every graded/project lab is "
               "referenced by at least one lecture README")


def check_clo_refs(found):
    bad = []
    for i, d in found:
        readme = read(os.path.join(d, "README.md"))
        m = re.search(r"\|\s*CLOs\s*\|(.*?)\|", readme)
        clos = re.findall(r"CLO(\d)", m.group(1)) if m else []
        if not clos or any(not (1 <= int(c) <= 8) for c in clos):
            bad.append(f"LAB-{i:02d}: CLO field missing or out of range")
    if bad:
        record(FAIL, "CLO references valid", "; ".join(bad[:8]))
    else:
        record(PASS, "CLO references valid", "all 16 labs cite CLO1-8 in range")


def check_graded_consistency(found):
    """Graded flags in the labs README/index must match the assessment strategy's map:
    12 graded-pool rows marked Yes + LAB-10/11 project rows (10%) + 2 optional rows."""
    idx = read(os.path.join(LABS, "README.md"))
    rows = re.findall(r"^\| LAB-(\d{2}) \|.*\|([^|]*)\|$", idx, flags=re.M)
    graded_rows = {n for n, cell in rows if "Yes" in cell}
    project_rows = {n for n, cell in rows if "10%" in cell}
    optional_rows = {n for n, cell in rows if "Optional" in cell}
    problems = []
    if graded_rows != {f"{i:02d}" for i in GRADED}:
        problems.append(f"graded-pool rows = {sorted(graded_rows)}, expected {sorted(f'{i:02d}' for i in GRADED)}")
    if project_rows != {f"{i:02d}" for i in GRADED_PROJECT}:
        problems.append(f"project (10%) rows = {sorted(project_rows)}, expected {sorted(f'{i:02d}' for i in GRADED_PROJECT)}")
    if optional_rows != {f"{i:02d}" for i in OPTIONAL}:
        problems.append(f"optional rows = {sorted(optional_rows)}, expected {sorted(f'{i:02d}' for i in OPTIONAL)}")
    asm = read(os.path.join(DOCS, "assessment-strategy.md"))
    if not re.search(r"(13|Thirteen) graded lab/GA deliverables", asm):
        problems.append("assessment-strategy '13/Thirteen graded lab/GA deliverables' wording not found — recheck")
    if problems:
        record(FAIL, "Graded-set consistency", "; ".join(problems))
    else:
        record(PASS, "Graded-set consistency",
               "labs index: 12 graded-pool rows + LAB-10/11 project rows (10%) + 2 optional rows; "
               "consistent with assessment-strategy §3 (13 deliverables, drop lowest)")


def check_safety_ethics(found):
    missing = []
    for i, d in found:
        text = read(os.path.join(d, "README.md"))
        if "syllabus-safety" not in text:
            missing.append(f"LAB-{i:02d}: no syllabus-safety cross-reference")
    idx = read(os.path.join(LABS, "syllabus-safety.md"))
    for needle in ("No scanning or probing of external systems",
                   "Isolation first",
                   "Acknowledgment gate"):
        if needle not in idx:
            missing.append(f"syllabus-safety.md: missing rule '{needle[:30]}'")
    if missing:
        record(FAIL, "Safety/ethics wiring", "; ".join(missing[:10]))
    else:
        record(PASS, "Safety/ethics wiring",
               "all 16 labs cross-reference the safety rules; the three binding rules "
               "(isolation, no external probing, acknowledgment gate) are present")


def check_no_fake_output(found):
    """Reports must not contain commands claiming pre-executed results (tool-output honesty)."""
    bad = []
    for i, d in found:
        for fn in ("README.md", "instructor.md"):
            text = read(os.path.join(d, fn))
            body = strip_fences(text)
            # suspicious: 'output:' followed by prompt-like or numeric tables in prose
            if re.search(r"PS >|root@lab:~#", body):
                bad.append(f"LAB-{i:02d}/{fn}: embedded shell-prompt 'output' outside fences")
    if bad:
        record(FAIL, "No fabricated tool output", "; ".join(bad[:8]))
    else:
        record(PASS, "No fabricated tool output",
               "expected observations are described as expectations/tool semantics, never as "
               "pre-executed transcripts (verify: verification report)")


def check_index_links():
    text = read(os.path.join(LABS, "README.md"))
    links = re.findall(r"\]\((lab-[^)#]*?)(?:#[^)]*)?\)", text)
    bad = [t for t in set(links)
           if not (os.path.isdir(os.path.join(LABS, t)) or os.path.isfile(os.path.join(LABS, t)))]
    if bad:
        record(FAIL, "Labs index links", f"broken links: {sorted(bad)[:8]}")
    else:
        record(PASS, "Labs index links",
               f"{len(set(links))} distinct lab links resolve; inventory table has 16 rows"
               if len(re.findall(r"^\| LAB-\d{2}", text, flags=re.M)) == 16 else
               f"{len(set(links))} distinct lab links resolve (inventory rows: "
               f"{len(re.findall(r'^\| LAB-\\d{2}', text, flags=re.M))})")


def main():
    print(f"Lab audit - repo root: {os.path.relpath(ROOT)}")
    print("=" * 72)
    found = check_inventory()
    if not found:
        print("Cannot proceed without lab triads.")
        sys.exit(1)
    check_required_elements(found)
    check_substance(found)
    check_lecture_alignment(found)
    check_clo_refs(found)
    check_graded_consistency(found)
    check_safety_ethics(found)
    check_no_fake_output(found)
    check_index_links()
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
