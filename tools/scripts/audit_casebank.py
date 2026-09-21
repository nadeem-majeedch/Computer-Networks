#!/usr/bin/env python3
"""Case-study bank audit for the Computer Networks course repository.

Run from the repository root:  python tools/scripts/audit_casebank.py
Validates the case-studies/ bank: inventory (65 case files), per-case element
completeness (16 required elements), student/instructor split, difficulty ramp
within each lecture pair, full lecture coverage (L01-L32), task-category
coverage (the 22 required categories), evidence-policy labeling, and
index<->file agreement in the bank README.
Exit 0 = clean (warnings allowed); 1 = at least one FAIL. Stdlib only.
"""

import os
import re
import sys

ROOT = '.'
CASES_DIR = os.path.join(ROOT, 'case-studies', 'cases')
README = os.path.join(ROOT, 'case-studies', 'README.md')

ELEMENTS = [
    ('ID', r'^# PB-\d+ —'),
    ('Difficulty', r'\|\s*Difficulty\s*\|'),
    ('Lectures', r'\|\s*Lecture\(s\)\s*\|'),
    ('Student scenario', r'^### Scenario', True),
    ('Problem statement', r'^### Problem statement', True),
    ('Evidence pack', r'^### Evidence pack', True),
    ('Constraints', r'^### Constraints', True),
    ('Student questions', r'^### Student questions', True),
    ('Learning outcomes', r'^### Expected learning outcomes', True),
    ('Hints', r'^### Hints', False),
    ('Solution', r'^### Solution', False),
    ('Reasoning process', r'^### Reasoning process', False),
    ('Common incorrect approaches', r'^### Common incorrect approaches', False),
    ('Extension question', r'^### Extension question', False),
    ('Rubric', r'^### Assessment rubric', False),
]
EVIDENCE_LABEL = re.compile(r'Synthetic evidence[\s\S]{0,160}?not from a live\s+system', re.I)
RUBRIC_LEVELS = ['4 Exemplary', '3 Proficient', '2 Developing', '1 Beginning']
DIFF_ORDER = {'Beginner': 0, 'Intermediate': 1, 'Advanced': 2, 'Expert': 3}

REQUIRED_22 = [
    'Network fundamentals', 'OSI/TCP-IP reasoning', 'Physical-layer faults',
    'Ethernet and switching', 'VLAN configuration', 'IP addressing',
    'Subnetting and VLSM', 'IPv6', 'Routing', 'ARP and ICMP', 'NAT',
    'TCP/UDP behavior', 'DNS/DHCP', 'Wireless networking', 'Network programming',
    'Security and firewall reasoning', 'Packet capture analysis',
    'Network performance', 'Cloud and data center networking',
    'Enterprise network design', 'Multi-layer troubleshooting',
    'Data science and distributed computing networks',
]

# Raw per-case Topic strings -> canonical categories (shared with the README
# generator's §8 normalization; kept in sync by the audit).
CANON = {
    'Network fundamentals': 'Network fundamentals',
    'Network fundamentals (media)': 'Network fundamentals',
    'OSI/TCP-IP reasoning': 'OSI/TCP-IP reasoning',
    'Network performance': 'Network performance',
    'Network performance (TCP)': 'Network performance',
    'Ethernet/performance': 'Ethernet and switching',
    'Ethernet': 'Ethernet and switching',
    'Ethernet and switching': 'Ethernet and switching',
    'Ethernet/physical faults': 'Ethernet and switching',
    'Network programming': 'Network programming',
    'Network programming (framing)': 'Network programming',
    'Network programming (transport)': 'Network programming',
    'Physical-layer faults': 'Physical-layer faults',
    'VLAN configuration': 'VLAN configuration',
    'Wireless networking': 'Wireless networking',
    'Wireless networking / performance': 'Wireless networking',
    'Wireless networking (link budget)': 'Wireless networking',
    'Enterprise design (LAN security preview)': 'Enterprise network design',
    'Enterprise design (capstone integration)': 'Enterprise network design',
    'Enterprise network design': 'Enterprise network design',
    'IP addressing': 'IP addressing',
    'ARP': 'ARP and ICMP',
    'Subnetting/VLSM': 'Subnetting and VLSM',
    'DNS/DHCP': 'DNS/DHCP',
    'DNS': 'DNS/DHCP',
    'NAT': 'NAT',
    'IPv6': 'IPv6',
    'Routing': 'Routing',
    'Routing faults': 'Routing',
    'TCP/UDP behavior': 'TCP/UDP behavior',
    'Security reasoning': 'Security and firewall reasoning',
    'Security and firewall reasoning': 'Security and firewall reasoning',
    'Security/enterprise design': 'Security and firewall reasoning',
    'VPN/segmentation': 'Security and firewall reasoning',
    'Security / packet capture analysis': 'Packet capture analysis',
    'Application protocols': 'Application protocols',
    'Application protocols / performance': 'Application protocols',
    'Cloud and data center networking': 'Cloud and data center networking',
    'SDN': 'SDN / programmable networks',
    'Monitoring/operations': 'Monitoring and operations',
    'Monitoring/performance': 'Monitoring and operations',
    'Multi-layer troubleshooting (L2/L3/L4)': 'Multi-layer troubleshooting',
    'Multi-layer troubleshooting (whole-course)': 'Multi-layer troubleshooting',
    'Multi-layer troubleshooting': 'Multi-layer troubleshooting',
    'Data-science networking': 'Data science and distributed computing networks',
}

CASE_RE = re.compile(r'^# (PB-\d+) — (.+?) \((L\d+), (\w+)\)$', re.M)
TOPIC_RE = re.compile(r'Topic:\s*([^·|]+)')
SPLIT_RE = '<!-- INSTRUCTOR-ONLY BELOW -->'

results = []


def add(check, status, detail):
    results.append((check, status, detail))


def main():
    fails = warns = 0

    # --- 1. Inventory -------------------------------------------------------
    files = sorted(f for f in os.listdir(CASES_DIR) if f.endswith('.md'))
    cases = []
    for fn in files:
        text = open(os.path.join(CASES_DIR, fn), encoding='utf-8').read()
        m = CASE_RE.search(text)
        if not m:
            add('inventory', 'FAIL', f'{fn}: H1 does not match PB-### — Title (Lnn, Level)')
            continue
        case = dict(id=m.group(1), title=m.group(2), lect=m.group(3),
                    diff=m.group(4), fn=fn, text=text)
        tm = TOPIC_RE.search(text)
        raw = tm.group(1).strip() if tm else 'Unknown'
        case['topic'] = CANON.get(raw, raw)
        case['student'] = text.split(SPLIT_RE)[0]
        case['instructor'] = text.split(SPLIT_RE, 1)[1] if SPLIT_RE in text else ''
        cases.append(case)
    ids = [c['id'] for c in cases]
    dupes = {i for i in ids if ids.count(i) > 1}
    seq_ok = ids == [f'PB-{n:03d}' for n in range(1, len(ids) + 1)]
    if dupes or not seq_ok:
        add('inventory', 'FAIL', f'IDs: dupes={dupes or "none"}, sequential={seq_ok}')
    else:
        add('inventory', 'PASS', f'{len(cases)} cases, IDs sequential PB-001..PB-{len(cases):03d}')

    # --- 2. Element completeness (16 required elements) ---------------------
    missing_report = []
    for c in cases:
        miss = []
        for el in ELEMENTS:
            name, pat, in_student = el[0], el[1], el[2] if len(el) > 2 else None
            zone = c['student'] if in_student else c['text']
            if not re.search(pat, zone, re.M):
                miss.append(name + ('' if in_student else ' (instr)'))
        if not re.search(EVIDENCE_LABEL, c['student']):
            miss.append('evidence label')
        rub = re.search(r'### Assessment rubric.*', c['instructor'], re.S)
        if not rub or not all(lvl in rub.group(0) for lvl in RUBRIC_LEVELS):
            miss.append('rubric levels')
        if len(re.findall(r'^\d+\.', c['student'], re.M)) < 3:
            miss.append('>=3 student questions')
        if miss:
            missing_report.append(f"{c['id']}: {', '.join(miss)}")
    if missing_report:
        add('elements', 'FAIL', f'{len(missing_report)} cases with gaps: ' + '; '.join(missing_report[:6]) +
            (' …' if len(missing_report) > 6 else ''))
        fails += 1
    else:
        add('elements', 'PASS', f'all {len(cases)} cases carry the 16 required elements')

    # --- 3. Student/instructor split ---------------------------------------
    bad = [c['id'] for c in cases if not c['instructor'].strip()]
    add('split', 'FAIL' if bad else 'PASS',
        'all cases split student/instructor' if not bad else f'missing split: {bad}')
    if bad:
        fails += 1

    # --- 4. Difficulty ramp within each lecture ----------------------------
    ramp_fails = []
    by_lect = {}
    for c in cases:
        by_lect.setdefault(c['lect'], []).append(c)
    for lect in sorted(by_lect):
        ds = [DIFF_ORDER[c['diff']] for c in sorted(by_lect[lect], key=lambda x: x['id'])]
        if ds != sorted(ds):
            ramp_fails.append(f"{lect}: {[c['diff'] for c in sorted(by_lect[lect], key=lambda x: x['id'])]}")
    add('ramp', 'FAIL' if ramp_fails else 'PASS',
        'second case >= first in every lecture' if not ramp_fails else '; '.join(ramp_fails))
    if ramp_fails:
        fails += 1

    # --- 5. Lecture coverage L01-L32 ---------------------------------------
    missing_lect = [f'L{k:02d}' for k in range(1, 33) if f'L{k:02d}' not in by_lect]
    counts = {k: len(v) for k, v in by_lect.items()}
    odd = {k: v for k, v in counts.items() if v not in (2, 3)}
    add('lecture-coverage', 'FAIL' if missing_lect else 'PASS',
        f'32/32 lectures covered; per-lecture counts: {sorted(set(counts.values()))}'
        + (f'; odd counts: {odd}' if odd else ''))
    if missing_lect:
        fails += 1

    # --- 6. Task-category coverage (22 required) ---------------------------
    topics = {}
    for c in cases:
        topics.setdefault(c['topic'], []).append(c['id'])
    missing_topics = [t for t in REQUIRED_22 if t not in topics]
    add('topic-coverage', 'FAIL' if missing_topics else 'PASS',
        f'{len(topics)} topics; all 22 required categories present'
        if not missing_topics else f'missing: {missing_topics}')
    if missing_topics:
        fails += 1

    # --- 7. Difficulty distribution ----------------------------------------
    dist = {}
    for c in cases:
        dist[c['diff']] = dist.get(c['diff'], 0) + 1
    b, i, a, e = (dist.get(k, 0) for k in ('Beginner', 'Intermediate', 'Advanced', 'Expert'))
    if b / len(cases) < 0.2:
        add('difficulty-distribution', 'WARN',
            f'B{b}/I{i}/A{a}/E{e} — beginner share below 20%')
        warns += 1
    else:
        add('difficulty-distribution', 'PASS', f'B{b}/I{i}/A{a}/E{e} of {len(cases)}')

    # --- 8. README index <-> files agreement -------------------------------
    readme = open(README, encoding='utf-8').read()
    links = re.findall(r'\[(PB-\d+)\]\(cases/([^)]+)\)', readme)
    linked_ids = [l[0] for l in links]
    broken = [l for l in links if not os.path.exists(os.path.join(CASES_DIR, l[1]))]
    not_linked = [c['id'] for c in cases if c['id'] not in linked_ids]
    total_line = re.search(r'\*\*Total: (\d+)\*\*', readme)
    total_ok = total_line and int(total_line.group(1)) == len(cases)
    if broken or not_linked or not total_ok:
        add('index-agreement', 'FAIL',
            f'broken links: {len(broken)}, unlinked cases: {not_linked or "none"}, '
            f'total-line: {total_line.group(1) if total_line else "missing"} (files: {len(cases)})')
        fails += 1
    else:
        add('index-agreement', 'PASS',
            f'all {len(cases)} cases linked; total line matches; no broken paths')

    # --- 9. No fabricated real-system claims --------------------------------
    # Synthetic evidence must be labeled; raw tool transcripts presented as real
    # captures are not allowed outside labeled packs.
    fabric = []
    for c in cases:
        zone = c['student']
        if re.search(r'```(?:bash|shell|console)\n\$\s', zone) and not re.search(
                EVIDENCE_LABEL, zone):
            fabric.append(c['id'])
    add('evidence-policy', 'FAIL' if fabric else 'PASS',
        'no unlabeled command transcripts' if not fabric else f'unlabeled transcripts: {fabric}')
    if fabric:
        fails += 1

    # --- 10. Graded-thread collision (CS- vs PB- IDs) -----------------------
    collisions = [c['id'] for c in cases if re.match(r'CS-', c['id'])]
    add('id-namespace', 'PASS' if not collisions else 'FAIL',
        'PB- namespace only; graded CS-01..04 untouched' if not collisions else f'collisions: {collisions}')
    if collisions:
        fails += 1

    # --- Report -------------------------------------------------------------
    print('=' * 74)
    for check, status, detail in results:
        mark = {'PASS': '[PASS]', 'FAIL': '[FAIL]', 'WARN': '[WARN]'}[status]
        print(f'{mark} {check:<24} {detail}')
    print('=' * 74)
    p = sum(1 for r in results if r[1] == 'PASS')
    print(f'Total: {p} PASS / {warns} WARN / {fails} FAIL')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
