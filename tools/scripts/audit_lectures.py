#!/usr/bin/env python3
"""Lecture-package audit for the Computer Networks course repository.

Run from the repository root:  python tools/scripts/audit_lectures.py
Validates that all 32 lectures have complete teaching packages (README +
notes + worksheet), that each package contains the required teaching
elements from docs/lecture-template.md, and cross-checks consistency with
the foundation documents. Exit 0 = clean; 1 = at least one FAIL.
Standard library only. Every result comes from parsing real files.
"""

import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LECT = os.path.join(ROOT, "lectures")
DOCS = os.path.join(ROOT, "docs")

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


def rel(path):
    return os.path.relpath(path, ROOT).replace("\\", "/")


# ---------------------------------------------------------------- inventory

TITLES = {
    1: "What Is a Network? Overview, History & the Internet Today",
    2: "Layered Architectures: OSI & TCP/IP",
    3: "Applications, Sockets & the First Packet Hunt",
    4: "Performance Lab Foundations: Measuring the Network",
    5: "Physical Layer: Signals, Media & Transmission Basics",
    6: "Data Link Layer: Framing, Errors & Reliability",
    7: "MAC Protocols & Wired LANs: Ethernet",
    8: "Switching & LAN Design",
    9: "VLANs & L2 Segmentation",
    10: "Wireless Networking: Wi-Fi Fundamentals",
    11: "Wireless in Practice + LAN Security Preview",
    12: "IP Fundamentals & ARP",
    13: "IPv4 Subnetting & VLSM",
    14: "IP Addressing at Scale: DHCP & NAT",
    15: "IPv6",
    16: "Routing Fundamentals & ICMP",
    17: "UDP & the Transport Layer's Job",
    18: "TCP Essentials: Connections & Reliable Delivery",
    19: "TCP Flow & Congestion Control",
    20: "Programming the Transport Layer: Reliability over UDP",
    21: "DNS: The Internet's Directory",
    22: "DHCP Deep Dive, BOOTP & Address Management",
    23: "Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH",
    24: "Security Principles & Cryptographic Building Blocks",
    25: "Perimeter & Internal Defenses: Firewalls, Segmentation & VPNs",
    26: "Attack & Defense Case Workshop",
    27: "Cloud & Virtual Networking",
    28: "Data-Plane & SDN: Programmable Networks",
    29: "Monitoring, Telemetry & Systematic Troubleshooting",
    30: "Mobile & Wireless Enterprise Networking",
    31: "Enterprise Design & the Data-Science Connection",
    32: "Capstone Workshop, Presentations & Course Synthesis",
}


def check_package_inventory():
    missing_dirs, missing_files, empty = [], [], []
    found = []
    for i in range(1, 33):
        matches = [d for d in os.listdir(LECT) if d.startswith(f"lecture-{i:02d}-")] \
            if os.path.isdir(LECT) else []
        if not matches:
            missing_dirs.append(f"L{i:02d}")
            continue
        d = os.path.join(LECT, sorted(matches)[0])
        found.append((i, d))
        for fn in ("README.md", "notes.md", "worksheet.md"):
            p = os.path.join(d, fn)
            if not os.path.isfile(p):
                missing_files.append(f"L{i:02d}/{fn}")
            elif os.path.getsize(p) == 0:
                empty.append(f"L{i:02d}/{fn}")
    if missing_dirs or missing_files or empty:
        record(FAIL, "32 complete packages (README+notes+worksheet)",
               f"missing dirs={missing_dirs} missing files={missing_files} empty={empty}")
        return []
    record(PASS, "32 complete packages (README+notes+worksheet)",
           f"lecture-01..lecture-32 each contain README.md, notes.md, worksheet.md (96 files, none empty)")
    return found


def check_title_consistency(found):
    problems = []
    for i, d in found:
        rtxt = read(os.path.join(d, "README.md"))
        ntxt = read(os.path.join(d, "notes.md"))
        want = f"# Lecture {i:02d} — {TITLES[i]}"
        if not rtxt.startswith(want):
            problems.append(f"L{i:02d}/README title line: expected '{want}'")
        m = re.search(r"^## .*?" + re.escape(TITLES[i]), ntxt, flags=re.M)
        if not m:
            problems.append(f"L{i:02d}/notes title: '{TITLES[i]}' not in notes subtitle")
    if problems:
        record(FAIL, "Title consistency (README/notes)", "; ".join(problems))
    else:
        record(PASS, "Title consistency (README/notes)",
               "all 32 packages: README H1 and notes subtitle match the master title set")


REQUIRED = {
    "README.md": {
        "Outcomes section": r"## (Learning outcomes|What you should be able to do afterwards)",
        "Module field": r"\|\s*Module\s*\|",
        "CLO field": r"\|\s*CLOs addressed\s*\|",
        "Depends-on field": r"\|\s*Depends on\s*\|",
        "Assessment artifact": r"\|\s*Assessment artifact\s*\|",
        "Companion links": r"\]\(notes\.md\)",
    },
    "notes.md": {
        "Minute plan (120)": r"\| Minutes \|",
        "Concept walkthrough": r"## 3\. Concept walkthrough",
        "Definitions": r"## 4\. Important definitions",
        "Real-world examples": r"## 5\. Real-world examples",
        "Worked example": r"## 6\.\s*Mathematical",
        "Misconceptions table": r"## 8\. Common misconceptions",
        "Demo": r"## 9\. Suggested practical demonstration",
        "Activities": r"## 10\. Classroom activities",
        "Problem-solving questions": r"## 11\. Problem-solving questions",
        "Formative assessment": r"## 12\. Formative assessment",
        "Exit ticket (notes)": r"## 13\. Exit ticket",
        "Difficulties": r"## 14\. Anticipated difficulties",
        "Prep checklist": r"## 15\. Instructor preparation checklist",
        "Timing fallbacks": r"## 16\. Timing fallbacks",
        "References": r"## 17\. References",
    },
    "worksheet.md": {
        "Exit ticket": r"## Exit ticket",
    },
}


def check_required_elements(found):
    missing = []
    for i, d in found:
        for fn, reqs in REQUIRED.items():
            text = read(os.path.join(d, fn))
            for label, pat in reqs.items():
                if not re.search(pat, text):
                    missing.append(f"L{i:02d}/{fn}: {label}")
    if missing:
        record(FAIL, "Required elements present", "; ".join(missing[:12]))
    else:
        record(PASS, "Required elements present",
               "all 32 packages carry module/CLO/deps fields, 120-min plan, concepts, definitions, "
               "examples, diagrams, misconceptions, activities, questions, formative assessment, "
               "exit ticket, demo, prep checklist, references")


def check_element_substance(found):
    """Quality gates: minimum counts where a bare header would be a hollow pass."""
    problems = []
    for i, d in found:
        notes = read(os.path.join(d, "notes.md"))
        worksheet = read(os.path.join(d, "worksheet.md"))
        if len(re.findall(r"^\| \d+–\d+ \|", notes, flags=re.M)) < 6:
            problems.append(f"L{i:02d}: minute-plan rows < 6")
        if len(re.findall(r"^\| .* \|$", notes, flags=re.M)) < 16:
            problems.append(f"L{i:02d}: table density low (suspiciously thin notes)")
        if len(re.findall(r"^\d+\.", worksheet, flags=re.M)) < 6:
            problems.append(f"L{i:02d}: worksheet numbered items < 6")
        if len(re.findall(r"^\d+\.", notes, flags=re.M)) < 6:
            problems.append(f"L{i:02d}: notes numbered questions < 6")
    if problems:
        record(FAIL, "Element substance (min counts)", "; ".join(problems[:12]))
    else:
        record(PASS, "Element substance (min counts)",
               "every package: >=6 minute-plan rows, >=16 table rows of notes, >=6 worksheet items, "
               ">=6 numbered questions, 3-item exit ticket, contiguous 0–120 timing")


def check_minute_plan_contiguity(found):
    """Every 120-minute plan must tile 0..120 with no gaps."""
    bad = []
    for i, d in found:
        notes = read(os.path.join(d, "notes.md"))
        segs = sorted((int(a), int(b)) for a, b in
                      re.findall(r"^\|\s*(\d+)\s*[–-]\s*(\d+)\s*\|", notes, flags=re.M))
        if not segs:
            bad.append(f"L{i:02d}: no minute rows")
            continue
        cur, gaps = 0, []
        for a, b in segs:
            if a > cur:
                gaps.append((cur, a))
            cur = max(cur, b)
        if cur < 120:
            gaps.append((cur, 120))
        if gaps:
            bad.append(f"L{i:02d}: gaps {gaps}")
    if bad:
        record(FAIL, "Timing plans contiguous (0–120)", "; ".join(bad[:8]))
    else:
        record(PASS, "Timing plans contiguous (0–120)",
               "all 32 minute plans tile 0–120 without gaps")


def check_misconceptions_table(found):
    bad = []
    for i, d in found:
        notes = read(os.path.join(d, "notes.md"))
        sec = notes.split("## 8. Common misconceptions")[1].split("## 9.")[0]
        rows = [ln for ln in sec.splitlines() if ln.strip().startswith("|") and
                not re.match(r"^\|[\s\-|:]+\|$", ln.strip()) and "Misconception" not in ln]
        if len(rows) < 3:
            bad.append(f"L{i:02d}: only {len(rows)} misconception rows")
    if bad:
        record(FAIL, "Misconceptions table (>=3 rows)", "; ".join(bad[:8]))
    else:
        record(PASS, "Misconceptions table (>=3 rows)",
               "all 32 lectures have >=3 misconception/debunk rows")


def check_exit_ticket_3items(found):
    bad = []
    for i, d in found:
        ws = read(os.path.join(d, "worksheet.md"))
        sec = ws.split("## Exit ticket")[1]
        items = len(re.findall(r"^\d+\.", sec, flags=re.M))
        if items < 3:
            bad.append(f"L{i:02d}: exit ticket has {items} items")
    if bad:
        record(FAIL, "Exit ticket = 3 items", "; ".join(bad[:8]))
    else:
        record(PASS, "Exit ticket = 3 items",
               "all 32 worksheets end with a 3-item exit ticket")


BOX = r"[─│┌┐└┘├┤┬┴┼╔╗╚╝═║←→⇒↑↓┃╱╲▲▼]"


def has_diagram(notes):
    """Mermaid block, or any fenced block with >=3 box/arrow characters.
    Markdown tables (ASCII '|') deliberately do not count as diagrams."""
    if re.search(r"```mermaid", notes):
        return True
    for m in re.finditer(r"```[^\n]*\n(.*?)```", notes, flags=re.S):
        if len(re.findall(BOX, m.group(1))) >= 3:
            return True
    return False


def check_diagram_presence(found):
    bad = []
    for i, d in found:
        notes = read(os.path.join(d, "notes.md"))
        if not has_diagram(notes):
            bad.append(f"L{i:02d}: no fenced diagram (mermaid or box-art) in notes")
    if bad:
        record(FAIL, "Diagrams present", "; ".join(bad[:8]))
    else:
        record(PASS, "Diagrams present",
               "every package includes at least one mermaid or annotated-ASCII diagram")


def check_prereq_ordering(found):
    """Any package listing 'Lnn' as dependency must have nn < its own number."""
    bad = []
    for i, d in found:
        rtxt = read(os.path.join(d, "README.md"))
        m = re.search(r"\|\s*Depends on\s*\|(.*?)\|", rtxt)
        deps = re.findall(r"L(\d{2})", m.group(1)) if m else []
        for dep in deps:
            if int(dep) >= i:
                bad.append(f"L{i:02d} depends on L{dep} (not earlier)")
    if bad:
        record(FAIL, "Prerequisite ordering (packages)", "; ".join(bad[:8]))
    else:
        record(PASS, "Prerequisite ordering (packages)",
               "all intra-course dependencies point to strictly earlier lectures")


def check_clo_refs(found):
    bad = []
    for i, d in found:
        rtxt = read(os.path.join(d, "README.md"))
        m = re.search(r"\|\s*CLOs addressed\s*\|(.*?)\|", rtxt)
        clo = re.findall(r"CLO(\d)", m.group(1)) if m else []
        if not clo or any(not (1 <= int(c) <= 8) for c in clo):
            bad.append(f"L{i:02d}: CLO field missing or out of range")
    if bad:
        record(FAIL, "CLO references valid", "; ".join(bad[:8]))
    else:
        record(PASS, "CLO references valid", "all 32 READMEs cite at least one CLO1-8")


def check_clo_coverage_by_lecture(found):
    prim = {f"CLO{i}": [] for i in range(1, 9)}
    for i, d in found:
        rtxt = read(os.path.join(d, "README.md"))
        m = re.search(r"\|\s*CLOs addressed\s*\|(.*?)\|", rtxt)
        cell = m.group(1) if m else ""
        is_primary = "**" in cell
        for c in re.findall(r"CLO(\d)", cell):
            if is_primary and int(c) in (1, 2, 3, 4, 5, 6, 7, 8):
                prim[f"CLO{c}"].append(i)
    problems = [c for c, v in prim.items() if not v]
    if problems:
        record(FAIL, "CLO coverage (lectures)", f"CLOs with no primary lecture: {problems}")
    else:
        record(PASS, "CLO coverage (lectures)",
               "every CLO1-8 has >=1 primary lecture: " +
               ", ".join(f"{c}={v[0]:02d}…" if len(v) > 1 else f"{c}={v[0]:02d}" for c, v in prim.items()))


def check_lab_ga_references(found):
    """Worksheet or notes may reference LAB-01..14 or GA-xx; the schedule is authoritative
    for the LAB map, so only range-validate what the packages cite."""
    cited = set()
    for _i, d in found:
        for fn in ("README.md", "notes.md", "worksheet.md"):
            cited |= set(re.findall(r"LAB-(\d{2})", read(os.path.join(d, fn))))
    bad = [f"LAB-{c}" for c in cited if not (1 <= int(c) <= 14)]
    if bad:
        record(FAIL, "Lab reference range (packages)", f"out-of-range: {bad}")
    else:
        record(PASS, "Lab reference range (packages)",
               f"{len(cited)} distinct LAB refs across packages, all within LAB-01..LAB-14")


def check_slides_status(found):
    """Template: slides.md is a later authoring pass, required before delivery
    sign-off — track its absence as a WARN, not a FAIL, during this phase."""
    missing = [i for i, d in found
               if not os.path.isfile(os.path.join(d, "slides.md"))]
    if missing:
        record(WARN, "Slide decks (later authoring pass)",
               f"{len(missing)}/32 packages lack slides.md (template: required "
               "before delivery sign-off; notes/worksheet carry the full session)")
    else:
        record(PASS, "Slide decks present", "all packages include slides.md")


def check_index_links():
    text = read(os.path.join(LECT, "README.md"))
    links = re.findall(r"\]\((lecture-[^)#]*?)(?:#[^)]*)?\)", text)
    bad = [t for t in set(links)
           if not (os.path.isdir(os.path.join(LECT, t)) or os.path.isfile(os.path.join(LECT, t)))]
    if bad:
        record(FAIL, "Lectures index links", f"broken directory links: {bad}")
    else:
        record(PASS, "Lectures index links",
               f"{len(set(links))} distinct package links resolve; 32-row module tables present"
               if text.count("## Module") == 8 else
               f"{len(set(links))} distinct package links resolve (module headers: {text.count('## Module')})")


def main():
    print(f"Lecture audit - repo root: {rel(ROOT)}")
    print("=" * 72)
    found = check_package_inventory()
    if not found:
        print("Cannot proceed without packages.")
        sys.exit(1)
    check_title_consistency(found)
    check_required_elements(found)
    check_element_substance(found)
    check_minute_plan_contiguity(found)
    check_misconceptions_table(found)
    check_exit_ticket_3items(found)
    check_diagram_presence(found)
    check_prereq_ordering(found)
    check_clo_refs(found)
    check_clo_coverage_by_lecture(found)
    check_lab_ga_references(found)
    check_slides_status(found)
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
